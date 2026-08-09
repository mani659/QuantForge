"""Immutable public decision record produced by the Hypothesis Engine."""

from dataclasses import dataclass
from datetime import datetime
import re

from .hypothesis_errors import HypothesisError
from boe.detector_errors import VersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class HypothesisResult:
    """Abstract evidence interpretation, never a trade instruction or calculation."""

    schema_version: str
    hypothesis_id: str
    candidate_id: str
    accepted: bool
    overall_confidence: float
    supporting_evidence: tuple[str, ...]
    rejected_evidence: tuple[str, ...]
    evaluated_timestamp: datetime

    def __post_init__(self) -> None:
        """Validate public decision shape without exposing evidence calculations."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VersionMismatchError("HypothesisResult schema_version must be semantic versioning.")
        if not self.hypothesis_id or not self.candidate_id:
            raise HypothesisError("HypothesisResult hypothesis_id and candidate_id are required.")
        if not isinstance(self.accepted, bool):
            raise HypothesisError("HypothesisResult accepted must be a bool.")
        if not isinstance(self.overall_confidence, float) or not 0.0 <= self.overall_confidence <= 1.0:
            raise HypothesisError("HypothesisResult overall_confidence must be a float from 0.0 to 1.0.")
        for evidence in (self.supporting_evidence, self.rejected_evidence):
            if not isinstance(evidence, tuple) or not all(isinstance(item, str) for item in evidence):
                raise HypothesisError("HypothesisResult evidence must be tuples of strings.")
        if not isinstance(self.evaluated_timestamp, datetime):
            raise HypothesisError("HypothesisResult evaluated_timestamp must be a datetime.")
