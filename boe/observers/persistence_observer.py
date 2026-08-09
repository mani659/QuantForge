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


class PersistenceObserverError(ObserverError):
    """Specific error for PersistenceObserver execution."""
    pass


@dataclass(frozen=True)
class PersistenceObserverConfig:
    """Immutable external configuration for PersistenceObserver."""
    schema_version: str
    price_field: str
    direction_field: str

    def __post_init__(self) -> None:
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise PersistenceObserverError("PersistenceObserverConfig schema_version must be semantic versioning.")
        if not self.price_field or not self.direction_field:
            raise PersistenceObserverError("PersistenceObserverConfig fields cannot be empty.")

    @classmethod
    def from_json(cls, config_path: Path | str) -> "PersistenceObserverConfig":
        path = Path(config_path)
        if not path.is_file():
            raise PersistenceObserverError(f"Persistence observer config not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        except json.JSONDecodeError as error:
            raise PersistenceObserverError(f"Persistence observer config contains invalid JSON: {path}") from error
        
        required_fields = {"schema_version", "price_field", "direction_field"}
        missing_fields = required_fields.difference(data)
        if missing_fields:
            raise PersistenceObserverError(f"Persistence observer config missing fields: {', '.join(sorted(missing_fields))}")
        
        return cls(
            schema_version=data["schema_version"],
            price_field=data["price_field"],
            direction_field=data["direction_field"],
        )


class PersistenceObserver(ObserverContract):
    """
    Scientific instrument that measures trend persistence over a timeline.
    It relies entirely upon the ReplayEngineContract to traverse the timeline
    and access EnvironmentSnapshots deterministically.
    """

    OBSERVER_NAME = "PersistenceObserver"
    OBSERVER_VERSION = "1.0.0"

    def __init__(self, config: PersistenceObserverConfig, engine: ReplayEngineContract) -> None:
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
        Replay the timeline and measure persistence mathematically.
        """
        direction = timeline.timeline_metadata.get(self._config.direction_field)
        if direction not in {"UP", "DOWN"}:
            raise PersistenceObserverError("Timeline metadata must contain expected direction 'UP' or 'DOWN'.")

        self._engine.load(timeline.timeline_id)
        self._engine.start()

        reference_value = None
        max_favorable_excursion = 0.0
        final_value = None
        favorable_frames_count = 0
        total_frames = 0

        while True:
            cursor = self._engine.step()
            
            if cursor.current_snapshot is None:
                raise PersistenceObserverError("Missing environment snapshot during replay.")
                
            market_state = cursor.current_snapshot.market_state
            
            if self._config.price_field not in market_state:
                raise PersistenceObserverError(f"Price field {self._config.price_field} not found in market state.")
                
            current_value = float(market_state[self._config.price_field])

            if reference_value is None:
                reference_value = current_value

            final_value = current_value
            total_frames += 1

            if direction == "UP":
                favorable = current_value > reference_value
                excursion = current_value - reference_value
            else:
                favorable = current_value < reference_value
                excursion = reference_value - current_value

            if favorable:
                favorable_frames_count += 1
                
            if excursion > max_favorable_excursion:
                max_favorable_excursion = excursion

            if cursor.status == ReplayState.COMPLETE:
                break

        if reference_value is None or final_value is None or total_frames == 0:
            return self._build_evidence(timeline, 0.0, 0, 0.0, direction, False)

        if direction == "UP":
            final_excursion = final_value - reference_value
        else:
            final_excursion = reference_value - final_value
            
        final_favorable_excursion = max(0.0, final_excursion)

        if max_favorable_excursion > 0:
            ratio = final_favorable_excursion / max_favorable_excursion
        else:
            ratio = 0.0

        stability = favorable_frames_count / total_frames
        observed = ratio > 0.0

        return self._build_evidence(
            timeline=timeline,
            ratio=ratio,
            duration=favorable_frames_count,
            stability=stability,
            direction=direction,
            observed=observed
        )

    def _build_evidence(
        self, 
        timeline: FrozenBehaviorTimeline, 
        ratio: float, 
        duration: int, 
        stability: float,
        direction: str, 
        observed: bool
    ) -> Evidence:
        metadata = {
            "PersistenceRatio": ratio,
            "PersistenceDuration": duration,
            "PersistenceStability": stability,
            "PersistenceDirection": direction,
            "PersistenceObserved": observed,
        }
        
        ts = timeline.closed_timestamp

        return Evidence(
            evidence_id=f"{timeline.timeline_id}_persistence",
            candidate_id=timeline.candidate_id,
            timeline_id=timeline.timeline_id,
            observer_name=self.name,
            observer_version=self.version,
            evidence_type="PERSISTENCE",
            confidence=1.0,
            observed=observed,
            evidence_labels=("PERSISTENCE_MEASURED",),
            metadata=MappingProxyType(metadata),
            timestamp=ts
        )
