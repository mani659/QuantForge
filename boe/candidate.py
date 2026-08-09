"""Immutable behavioral hypothesis contract managed by the Candidate Manager."""

from dataclasses import dataclass
from datetime import datetime
import re

from .behavior_observation import BehaviorObservation
from .candidate_errors import CandidateError
from .candidate_events import CandidateEvent
from .candidate_state import CandidateState
from .detector_errors import VersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class Candidate:
    """An immutable tracked hypothesis created from one BehaviorObservation.

    The object intentionally stores lifecycle/provenance information only. It
    contains no detector calculations, risk data, order data, or execution data.
    """

    schema_version: str
    candidate_id: str
    observation: BehaviorObservation
    state: CandidateState
    created_at: datetime
    updated_at: datetime
    revision: int
    event_history: tuple[CandidateEvent, ...]

    def __post_init__(self) -> None:
        """Validate stable candidate identity and immutable event history shape."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VersionMismatchError("Candidate schema_version must be semantic versioning.")
        if not self.candidate_id:
            raise CandidateError("Candidate candidate_id is required.")
        if not isinstance(self.observation, BehaviorObservation):
            raise CandidateError("Candidate observation must be a BehaviorObservation.")
        if not isinstance(self.created_at, datetime) or not isinstance(self.updated_at, datetime):
            raise CandidateError("Candidate timestamps must be datetimes.")
        if self.revision < 0:
            raise CandidateError("Candidate revision cannot be negative.")
        if not isinstance(self.event_history, tuple):
            raise CandidateError("Candidate event_history must be a tuple.")
