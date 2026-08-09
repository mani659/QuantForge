import json
import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from boe.evidence.evidence import Evidence
from boe.evidence.evidence_errors import ObserverError
from boe.evidence.observer_contract import ObserverContract
from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_state import ReplayState
from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


class VelocityObserverError(ObserverError):
    """Specific error for VelocityObserver execution."""
    pass


@dataclass(frozen=True)
class VelocityObserverConfig:
    """Immutable external configuration for VelocityObserver."""
    schema_version: str
    strength_ranks: Mapping[str, int]

    def __post_init__(self) -> None:
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VelocityObserverError("VelocityObserverConfig schema_version must be semantic versioning.")
        if not isinstance(self.strength_ranks, Mapping) or not self.strength_ranks:
            raise VelocityObserverError("VelocityObserverConfig strength_ranks must be a non-empty mapping.")
        object.__setattr__(self, "strength_ranks", MappingProxyType(dict(self.strength_ranks)))

    @classmethod
    def from_json(cls, config_path: Path | str) -> "VelocityObserverConfig":
        path = Path(config_path)
        if not path.is_file():
            raise VelocityObserverError(f"Velocity observer config not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        except json.JSONDecodeError as error:
            raise VelocityObserverError(f"Velocity observer config contains invalid JSON: {path}") from error
        
        required_fields = {"schema_version", "strength_ranks"}
        missing_fields = required_fields.difference(data)
        if missing_fields:
            raise VelocityObserverError(f"Velocity observer config missing fields: {', '.join(sorted(missing_fields))}")
        
        return cls(
            schema_version=data["schema_version"],
            strength_ranks=data["strength_ranks"]
        )


class VelocityObserver(ObserverContract):
    """
    Scientific instrument that measures behavioural evolution over a timeline.
    It maps categorical behaviour strengths to numerical ranks using external
    configuration to mathematically evaluate acceleration, stability, and consistency.
    """

    OBSERVER_NAME = "VelocityObserver"
    OBSERVER_VERSION = "1.0.0"

    def __init__(self, config: VelocityObserverConfig, engine: ReplayEngineContract) -> None:
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
        Replay the timeline and measure velocity properties mathematically.
        """
        self._engine.load(timeline.timeline_id)
        self._engine.start()

        ranks = []
        
        while True:
            cursor = self._engine.step()
            
            frame = cursor.current_frame
            if frame is None:
                raise VelocityObserverError("Missing behaviour frame during replay.")
                
            rank = self._config.strength_ranks.get(frame.behavior_strength, 0)
            ranks.append(rank)

            if cursor.status == ReplayState.COMPLETE:
                break

        if len(ranks) < 2:
            return self._build_evidence(
                timeline=timeline, 
                observed=False, 
                direction="STABLE", 
                magnitude=0, 
                consistency=0.0, 
                stability=1.0
            )

        positive_changes = 0
        negative_changes = 0
        zero_changes = 0
        
        for i in range(1, len(ranks)):
            diff = ranks[i] - ranks[i-1]
            if diff > 0:
                positive_changes += 1
            elif diff < 0:
                negative_changes += 1
            else:
                zero_changes += 1
                
        total_steps = len(ranks) - 1
        overall_magnitude = ranks[-1] - ranks[0]
        
        if positive_changes > 0 and negative_changes == 0:
            direction = "INCREASING"
        elif negative_changes > 0 and positive_changes == 0:
            direction = "DECREASING"
        elif positive_changes == 0 and negative_changes == 0:
            direction = "STABLE"
        else:
            direction = "OSCILLATING"
            
        consistency = max(positive_changes, negative_changes) / total_steps
        stability = zero_changes / total_steps

        return self._build_evidence(
            timeline=timeline,
            observed=True,
            direction=direction,
            magnitude=overall_magnitude,
            consistency=consistency,
            stability=stability
        )

    def _build_evidence(
        self, 
        timeline: FrozenBehaviorTimeline, 
        observed: bool,
        direction: str,
        magnitude: int,
        consistency: float,
        stability: float
    ) -> Evidence:
        metadata = {
            "VelocityObserved": observed,
            "VelocityDirection": direction,
            "VelocityMagnitude": magnitude,
            "VelocityConsistency": consistency,
            "VelocityStability": stability
        }
        
        ts = timeline.closed_timestamp

        return Evidence(
            evidence_id=f"{timeline.timeline_id}_velocity",
            candidate_id=timeline.candidate_id,
            timeline_id=timeline.timeline_id,
            observer_name=self.name,
            observer_version=self.version,
            evidence_type="VELOCITY",
            confidence=1.0,
            observed=observed,
            evidence_labels=("VELOCITY_MEASURED",),
            metadata=MappingProxyType(metadata),
            timestamp=ts
        )
