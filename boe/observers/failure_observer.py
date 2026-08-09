import json
import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

from boe.evidence.evidence import Evidence
from boe.evidence.evidence_errors import ObserverError
from boe.evidence.observer_contract import ObserverContract
from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_state import ReplayState
from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


class FailureObserverError(ObserverError):
    """Specific error for FailureObserver execution."""
    pass


@dataclass(frozen=True)
class FailureObserverConfig:
    """Immutable external configuration for FailureObserver."""
    schema_version: str
    price_field: str
    direction_field: str

    def __post_init__(self) -> None:
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise FailureObserverError("FailureObserverConfig schema_version must be semantic versioning.")
        if not self.price_field or not self.direction_field:
            raise FailureObserverError("FailureObserverConfig fields cannot be empty.")

    @classmethod
    def from_json(cls, config_path: Path | str) -> "FailureObserverConfig":
        path = Path(config_path)
        if not path.is_file():
            raise FailureObserverError(f"Failure observer config not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        except json.JSONDecodeError as error:
            raise FailureObserverError(f"Failure observer config contains invalid JSON: {path}") from error
        
        required_fields = {"schema_version", "price_field", "direction_field"}
        missing_fields = required_fields.difference(data)
        if missing_fields:
            raise FailureObserverError(f"Failure observer config missing fields: {', '.join(sorted(missing_fields))}")
        
        return cls(
            schema_version=data["schema_version"],
            price_field=data["price_field"],
            direction_field=data["direction_field"],
        )


class FailureObserver(ObserverContract):
    """
    Scientific instrument that measures adverse behavioural failures over a timeline.
    It relies entirely upon the ReplayEngineContract to traverse the timeline
    and access EnvironmentSnapshots deterministically.
    """

    OBSERVER_NAME = "FailureObserver"
    OBSERVER_VERSION = "1.0.0"

    def __init__(self, config: FailureObserverConfig, engine: ReplayEngineContract) -> None:
        self._config = config
        self._engine = engine

    @property
    def name(self) -> str:
        return self.OBSERVER_NAME

    @property
    def version(self) -> str:
        return self.OBSERVER_VERSION

    def observe(self, timeline: FrozenBehaviorTimeline) -> Evidence:
        """
        Replay the timeline and measure failure properties mathematically.
        """
        direction = timeline.timeline_metadata.get(self._config.direction_field)
        if direction not in {"UP", "DOWN"}:
            raise FailureObserverError("Timeline metadata must contain expected direction 'UP' or 'DOWN'.")

        self._engine.load(timeline.timeline_id)
        self._engine.start()

        reference_value = None
        max_favorable_excursion = 0.0
        max_adverse_excursion = 0.0
        failure_delay = 0
        failure_observed = False
        
        current_frame_idx = 0

        while True:
            cursor = self._engine.step()
            
            if cursor.current_snapshot is None:
                raise FailureObserverError("Missing environment snapshot during replay.")
                
            market_state = cursor.current_snapshot.market_state
            
            if self._config.price_field not in market_state:
                raise FailureObserverError(f"Price field {self._config.price_field} not found in market state.")
                
            current_value = float(market_state[self._config.price_field])

            if reference_value is None:
                reference_value = current_value

            if direction == "UP":
                favorable = current_value - reference_value
                adverse = reference_value - current_value
            else:
                favorable = reference_value - current_value
                adverse = current_value - reference_value

            if favorable > max_favorable_excursion:
                max_favorable_excursion = favorable
                
            if adverse > max_adverse_excursion:
                max_adverse_excursion = adverse

            if adverse > 0 and not failure_observed:
                failure_observed = True
                failure_delay = current_frame_idx

            if cursor.status == ReplayState.COMPLETE:
                break
                
            current_frame_idx += 1

        if current_frame_idx == 0 and reference_value is None:
            return self._build_evidence(timeline, False, "NONE", 0, 0.0, direction)

        if not failure_observed:
            failure_type = "NONE"
        elif max_favorable_excursion <= 0:
            failure_type = "IMMEDIATE_COLLAPSE"
        else:
            failure_type = "REVERSAL"

        return self._build_evidence(
            timeline=timeline,
            observed=failure_observed,
            failure_type=failure_type,
            delay=failure_delay,
            severity=max_adverse_excursion,
            direction=direction
        )

    def _build_evidence(
        self, 
        timeline: FrozenBehaviorTimeline, 
        observed: bool,
        failure_type: str,
        delay: int,
        severity: float,
        direction: str
    ) -> Evidence:
        metadata = {
            "FailureObserved": observed,
            "FailureType": failure_type,
            "FailureDelay": delay,
            "FailureSeverity": severity,
            "FailureDirection": direction,
            "BehaviourTermination": timeline.termination_reason
        }
        
        ts = timeline.closed_timestamp

        return Evidence(
            evidence_id=f"{timeline.timeline_id}_failure",
            candidate_id=timeline.candidate_id,
            timeline_id=timeline.timeline_id,
            observer_name=self.name,
            observer_version=self.version,
            evidence_type="FAILURE",
            confidence=1.0,
            observed=observed,
            evidence_labels=("FAILURE_MEASURED",),
            metadata=MappingProxyType(metadata),
            timestamp=ts
        )
