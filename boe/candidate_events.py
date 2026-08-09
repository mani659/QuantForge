"""Immutable lifecycle events emitted by the Candidate Manager."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re

from .candidate_errors import CandidateError
from .candidate_state import CandidateState
from .detector_errors import VersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


class CandidateEventType(str, Enum):
    """Stable event types corresponding to the frozen candidate lifecycle."""

    CANDIDATE_CREATED = "CandidateCreated"
    OBSERVATION_STARTED = "ObservationStarted"
    VALIDATION_STARTED = "ValidationStarted"
    CANDIDATE_QUALIFIED = "CandidateQualified"
    CANDIDATE_REJECTED = "CandidateRejected"
    CANDIDATE_EXPIRED = "CandidateExpired"
    CANDIDATE_EXECUTED = "CandidateExecuted"


@dataclass(frozen=True)
class CandidateEvent:
    """A replayable immutable record of one candidate lifecycle transition."""

    schema_version: str
    event_id: str
    candidate_id: str
    previous_state: CandidateState | None
    new_state: CandidateState
    timestamp: datetime
    event_type: CandidateEventType

    def __post_init__(self) -> None:
        """Validate event identity, version, and timestamp without side effects."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VersionMismatchError("CandidateEvent schema_version must be semantic versioning.")
        if not self.event_id or not self.candidate_id:
            raise CandidateError("CandidateEvent event_id and candidate_id are required.")
        if not isinstance(self.timestamp, datetime):
            raise CandidateError("CandidateEvent timestamp must be a datetime.")
