"""Immutable behavioral hypothesis contract for the Hypothesis Engine."""

from dataclasses import dataclass
from datetime import datetime
import re

from .hypothesis_errors import HypothesisError
from boe.detector_errors import VersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class Hypothesis:
    """A stable hypothesis identity derived from one behavioral candidate."""

    hypothesis_id: str
    candidate_id: str
    hypothesis_version: str
    created_timestamp: datetime

    def __post_init__(self) -> None:
        """Validate stable identity and version fields without interpreting evidence."""
        if not self.hypothesis_id or not self.candidate_id:
            raise HypothesisError("Hypothesis hypothesis_id and candidate_id are required.")
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.hypothesis_version):
            raise VersionMismatchError("Hypothesis hypothesis_version must be semantic versioning.")
        if not isinstance(self.created_timestamp, datetime):
            raise HypothesisError("Hypothesis created_timestamp must be a datetime.")
