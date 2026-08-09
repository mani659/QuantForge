"""Immutable public evidence contract produced by Behavioral Validators."""

from dataclasses import dataclass
from datetime import datetime
import re

from .validator_errors import ValidatorError, ValidatorVersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class ValidationResult:
    """Abstract validator evidence for a candidate, never implementation metrics.

    ``evidence`` holds stable textual or categorical evidence labels only. It
    intentionally excludes indicator readings, thresholds, distances, and
    durations so detector and validator implementation details remain private.
    """

    schema_version: str
    candidate_id: str
    validator_id: str
    validator_version: str
    passed: bool
    confidence: float
    evidence: tuple[str, ...]
    timestamp: datetime

    def __post_init__(self) -> None:
        """Validate public result shape without interpreting validator evidence."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise ValidatorVersionMismatchError(
                "ValidationResult schema_version must be semantic versioning."
            )
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.validator_version):
            raise ValidatorVersionMismatchError(
                "ValidationResult validator_version must be semantic versioning."
            )
        if not self.candidate_id or not self.validator_id:
            raise ValidatorError("ValidationResult candidate_id and validator_id are required.")
        if not isinstance(self.passed, bool):
            raise ValidatorError("ValidationResult passed must be a bool.")
        if not isinstance(self.confidence, float) or not 0.0 <= self.confidence <= 1.0:
            raise ValidatorError("ValidationResult confidence must be a float from 0.0 to 1.0.")
        if not isinstance(self.evidence, tuple) or not all(isinstance(item, str) for item in self.evidence):
            raise ValidatorError("ValidationResult evidence must be a tuple of strings.")
        if not isinstance(self.timestamp, datetime):
            raise ValidatorError("ValidationResult timestamp must be a datetime.")
