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


class CompressionObserverError(ObserverError):
    """Specific error for CompressionObserver execution."""
    pass


@dataclass(frozen=True)
class CompressionObserverConfig:
    """Immutable external configuration for CompressionObserver."""
    schema_version: str
    compression_ranks: Mapping[str, int]

    def __post_init__(self) -> None:
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise CompressionObserverError("CompressionObserverConfig schema_version must be semantic versioning.")
        if not isinstance(self.compression_ranks, Mapping) or not self.compression_ranks:
            raise CompressionObserverError("CompressionObserverConfig compression_ranks must be a non-empty mapping.")
        object.__setattr__(self, "compression_ranks", MappingProxyType(dict(self.compression_ranks)))

    @classmethod
    def from_json(cls, config_path: Path | str) -> "CompressionObserverConfig":
        path = Path(config_path)
        if not path.is_file():
            raise CompressionObserverError(f"Compression observer config not found: {path}")
        try:
            with path.open("r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        except json.JSONDecodeError as error:
            raise CompressionObserverError(f"Compression observer config contains invalid JSON: {path}") from error
        
        required_fields = {"schema_version", "compression_ranks"}
        missing_fields = required_fields.difference(data)
        if missing_fields:
            raise CompressionObserverError(f"Compression config missing fields: {', '.join(sorted(missing_fields))}")
        
        return cls(
            schema_version=data["schema_version"],
            compression_ranks=data["compression_ranks"]
        )


class CompressionObserver(ObserverContract):
    """
    Scientific instrument that measures behavioural compression and expansion.
    It calculates the second-order derivative (amplitude changes) of the 
    categorical behaviour ranks over the timeline to determine compression.
    """

    OBSERVER_NAME = "CompressionObserver"
    OBSERVER_VERSION = "1.0.0"

    def __init__(self, config: CompressionObserverConfig, engine: ReplayEngineContract) -> None:
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
        Replay the timeline and measure compression properties mathematically.
        """
        self._engine.load(timeline.timeline_id)
        self._engine.start()

        ranks = []
        
        while True:
            cursor = self._engine.step()
            
            frame = cursor.current_frame
            if frame is None:
                raise CompressionObserverError("Missing behaviour frame during replay.")
                
            rank = self._config.compression_ranks.get(frame.behavior_strength, 0)
            ranks.append(rank)

            if cursor.status == ReplayState.COMPLETE:
                break

        if len(ranks) < 3:
            return self._build_evidence(
                timeline=timeline, 
                compression_observed=False, 
                compression_strength=0, 
                expansion_observed=False, 
                expansion_strength=0, 
                consistency=0.0, 
                duration=0
            )

        differences = []
        for i in range(1, len(ranks)):
            differences.append(abs(ranks[i] - ranks[i-1]))

        amplitudes = []
        for j in range(1, len(differences)):
            amplitudes.append(differences[j] - differences[j-1])

        compression_strength = 0
        expansion_strength = 0
        compression_steps = 0
        
        for a in amplitudes:
            if a < 0:
                compression_strength += abs(a)
                compression_steps += 1
            elif a > 0:
                expansion_strength += a

        compression_observed = compression_strength > expansion_strength
        expansion_observed = expansion_strength > compression_strength

        consistency = compression_steps / len(amplitudes) if amplitudes else 0.0

        compression_duration = 0
        for a in reversed(amplitudes):
            if a <= 0:
                compression_duration += 1
            else:
                break

        return self._build_evidence(
            timeline=timeline,
            compression_observed=compression_observed,
            compression_strength=compression_strength,
            expansion_observed=expansion_observed,
            expansion_strength=expansion_strength,
            consistency=consistency,
            duration=compression_duration
        )

    def _build_evidence(
        self, 
        timeline: FrozenBehaviorTimeline, 
        compression_observed: bool,
        compression_strength: int,
        expansion_observed: bool,
        expansion_strength: int,
        consistency: float,
        duration: int
    ) -> Evidence:
        metadata = {
            "CompressionObserved": compression_observed,
            "CompressionStrength": compression_strength,
            "CompressionDuration": duration,
            "CompressionConsistency": consistency,
            "ExpansionObserved": expansion_observed,
            "ExpansionStrength": expansion_strength
        }
        
        ts = timeline.closed_timestamp

        return Evidence(
            evidence_id=f"{timeline.timeline_id}_compression",
            candidate_id=timeline.candidate_id,
            timeline_id=timeline.timeline_id,
            observer_name=self.name,
            observer_version=self.version,
            evidence_type="COMPRESSION",
            confidence=1.0,
            observed=compression_observed,
            evidence_labels=("COMPRESSION_MEASURED",),
            metadata=MappingProxyType(metadata),
            timestamp=ts
        )
