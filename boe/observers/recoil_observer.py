import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType

from boe.evidence.evidence import Evidence
from boe.evidence.evidence_errors import ObserverError
from boe.evidence.observer_contract import ObserverContract
from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_state import ReplayState
from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


class RecoilObserverError(ObserverError):
    """Specific error for RecoilObserver execution."""
    pass


@dataclass(frozen=True)
class RecoilObserverConfig:
    """Immutable external configuration for RecoilObserver."""
    schema_version: str
    price_field: str
    direction_field: str

    def __post_init__(self) -> None:
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise RecoilObserverError("RecoilObserverConfig schema_version must be semantic versioning.")
        if not self.price_field or not self.direction_field:
            raise RecoilObserverError("RecoilObserverConfig fields cannot be empty.")

    @classmethod
    def from_json(cls, config_path: Path | str) -> "RecoilObserverConfig":
        path = Path(config_path)
        if not path.is_file():
            raise RecoilObserverError(f"Recoil observer configuration not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        except json.JSONDecodeError as error:
            raise RecoilObserverError(f"Recoil observer config contains invalid JSON: {path}") from error
        
        required_fields = {"schema_version", "price_field", "direction_field"}
        missing_fields = required_fields.difference(data)
        if missing_fields:
            raise RecoilObserverError(f"Recoil observer config missing fields: {', '.join(sorted(missing_fields))}")
        
        return cls(
            schema_version=data["schema_version"],
            price_field=data["price_field"],
            direction_field=data["direction_field"],
        )


class RecoilObserver(ObserverContract):
    """
    Scientific instrument that measures recoil behaviour over a timeline.
    It relies entirely upon the ReplayEngineContract to traverse the timeline
    and access EnvironmentSnapshots deterministically.
    """

    OBSERVER_NAME = "RecoilObserver"
    OBSERVER_VERSION = "1.0.0"

    def __init__(self, config: RecoilObserverConfig, engine: ReplayEngineContract) -> None:
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
        Replay the timeline and measure recoil mathematically.
        """
        # Extract direction from timeline metadata
        direction = timeline.timeline_metadata.get(self._config.direction_field)
        if direction not in {"UP", "DOWN"}:
            raise RecoilObserverError("Timeline metadata must contain expected recoil direction 'UP' or 'DOWN'.")

        self._engine.load(timeline.timeline_id)
        self._engine.start()

        reference_value = None
        max_adverse_excursion = 0.0
        excursion_frame_idx = 0
        final_value = None
        current_frame_idx = 0

        while True:
            cursor = self._engine.step()
            
            # The current_snapshot should never be None during active replay if everything is valid
            if cursor.current_snapshot is None:
                raise RecoilObserverError("Missing environment snapshot during replay.")
                
            market_state = cursor.current_snapshot.market_state
            
            if self._config.price_field not in market_state:
                raise RecoilObserverError(f"Price field {self._config.price_field} not found in market state.")
                
            current_value = float(market_state[self._config.price_field])

            if reference_value is None:
                reference_value = current_value

            final_value = current_value

            if direction == "UP":
                # Recoil against UP is a drop in price
                drop = reference_value - current_value
                if drop > max_adverse_excursion:
                    max_adverse_excursion = drop
                    excursion_frame_idx = current_frame_idx
            else:
                # Recoil against DOWN is a rise in price
                rise = current_value - reference_value
                if rise > max_adverse_excursion:
                    max_adverse_excursion = rise
                    excursion_frame_idx = current_frame_idx

            if cursor.status == ReplayState.COMPLETE:
                break
                
            current_frame_idx += 1

        if reference_value is None or final_value is None:
            # Timeline was empty (no frames processed)
            return self._build_evidence(
                timeline=timeline,
                ratio=0.0,
                delay=0,
                direction=direction,
                observed=False
            )

        if max_adverse_excursion <= 0:
            # Price never moved against the direction
            return self._build_evidence(
                timeline=timeline,
                ratio=0.0,
                delay=0,
                direction=direction,
                observed=False
            )

        # Measure recovery
        if direction == "UP":
            # Recovering UP from the low
            min_price = reference_value - max_adverse_excursion
            recovered = final_value - min_price
        else:
            # Recovering DOWN from the high
            max_price = reference_value + max_adverse_excursion
            recovered = max_price - final_value

        recovery_ratio = recovered / max_adverse_excursion
        recovery_delay = current_frame_idx - excursion_frame_idx

        return self._build_evidence(
            timeline=timeline,
            ratio=recovery_ratio,
            delay=recovery_delay,
            direction=direction,
            observed=True
        )

    def _build_evidence(
        self, 
        timeline: FrozenBehaviorTimeline, 
        ratio: float, 
        delay: int, 
        direction: str, 
        observed: bool
    ) -> Evidence:
        metadata = {
            "RecoveryRatio": ratio,
            "RecoveryDelay": delay,
            "RecoveryDirection": direction,
            "RecoveryObserved": observed,
        }
        
        # Determine caller-supplied deterministic timestamp
        # Fallback to the timeline's closed_timestamp if we can't determine it
        ts = timeline.closed_timestamp

        return Evidence(
            evidence_id=f"{timeline.timeline_id}_recoil",
            candidate_id=timeline.candidate_id,
            timeline_id=timeline.timeline_id,
            observer_name=self.name,
            observer_version=self.version,
            evidence_type="RECOIL",
            confidence=1.0,
            observed=observed,
            evidence_labels=("RECOIL_MEASURED",),
            metadata=MappingProxyType(metadata),
            timestamp=ts
        )
