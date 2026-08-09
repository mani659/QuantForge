"""Immutable public observation contract for the Behavioral Observation Engine."""

from dataclasses import dataclass
from datetime import datetime
import re

from .detector_errors import DataIntegrityError, VersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class BehaviorObservation:
    """A successful behavioral observation, never a trade instruction.

    The contract records the observed behavior and its provenance only. Scores,
    thresholds, indicator values, candidate state, and trade decisions remain
    inside the detector or the future Candidate Ledger.
    """

    schema_version: str
    observation_id: str
    environment_id: str
    behavior_type: str
    instrument: str
    timeframe: str
    observed_at: datetime
    detector_id: str
    detector_version: str

    def __post_init__(self) -> None:
        """Validate public contract identity and semantic versions."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VersionMismatchError("BehaviorObservation schema_version must be semantic versioning.")
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.detector_version):
            raise VersionMismatchError("BehaviorObservation detector_version must be semantic versioning.")
        required_fields = {
            "observation_id": self.observation_id,
            "environment_id": self.environment_id,
            "behavior_type": self.behavior_type,
            "instrument": self.instrument,
            "timeframe": self.timeframe,
            "detector_id": self.detector_id,
        }
        missing_fields = sorted(name for name, value in required_fields.items() if not value)
        if missing_fields:
            raise DataIntegrityError(
                "BehaviorObservation missing required fields: " + ", ".join(missing_fields)
            )
        if not isinstance(self.observed_at, datetime):
            raise DataIntegrityError("BehaviorObservation observed_at must be a datetime.")
