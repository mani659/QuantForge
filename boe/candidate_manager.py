"""Deterministic lifecycle manager for Behavioral Observation Engine candidates."""

from datetime import datetime
from types import MappingProxyType
from typing import Dict

from .behavior_observation import BehaviorObservation
from .candidate import Candidate
from .candidate_errors import (
    CandidateAlreadyFinalizedError,
    CandidateError,
    CandidateNotFoundError,
    InvalidStateTransitionError,
)
from .candidate_events import CandidateEvent, CandidateEventType
from .candidate_state import CandidateState


class CandidateManager:
    """Owns candidate lifecycle transitions and emits replayable immutable events."""

    SCHEMA_VERSION = "1.0.0"
    _FINAL_STATES = frozenset({
        CandidateState.EXECUTED,
        CandidateState.REJECTED,
        CandidateState.EXPIRED,
    })
    _TRANSITIONS = MappingProxyType({
        (CandidateState.NEW, CandidateState.OBSERVING): CandidateEventType.OBSERVATION_STARTED,
        (CandidateState.OBSERVING, CandidateState.VALIDATING): CandidateEventType.VALIDATION_STARTED,
        (CandidateState.VALIDATING, CandidateState.QUALIFIED): CandidateEventType.CANDIDATE_QUALIFIED,
        (CandidateState.VALIDATING, CandidateState.REJECTED): CandidateEventType.CANDIDATE_REJECTED,
        (CandidateState.OBSERVING, CandidateState.EXPIRED): CandidateEventType.CANDIDATE_EXPIRED,
        (CandidateState.VALIDATING, CandidateState.EXPIRED): CandidateEventType.CANDIDATE_EXPIRED,
        (CandidateState.QUALIFIED, CandidateState.EXECUTED): CandidateEventType.CANDIDATE_EXECUTED,
    })

    def __init__(self) -> None:
        self._candidates: Dict[str, Candidate] = {}

    def create_candidate(
        self,
        candidate_id: str,
        observation: BehaviorObservation,
        timestamp: datetime,
    ) -> Candidate:
        """Create a NEW candidate and its deterministic CandidateCreated event."""
        if candidate_id in self._candidates:
            raise CandidateError(f"Candidate already exists: {candidate_id}")
        if not isinstance(observation, BehaviorObservation):
            raise CandidateError("Candidate observation must be a BehaviorObservation.")
        if not isinstance(timestamp, datetime):
            raise CandidateError("Candidate creation timestamp must be a datetime.")

        event = CandidateEvent(
            schema_version=self.SCHEMA_VERSION,
            event_id=f"{candidate_id}:0",
            candidate_id=candidate_id,
            previous_state=None,
            new_state=CandidateState.NEW,
            timestamp=timestamp,
            event_type=CandidateEventType.CANDIDATE_CREATED,
        )
        candidate = Candidate(
            schema_version=self.SCHEMA_VERSION,
            candidate_id=candidate_id,
            observation=observation,
            state=CandidateState.NEW,
            created_at=timestamp,
            updated_at=timestamp,
            revision=0,
            event_history=(event,),
        )
        self._candidates[candidate_id] = candidate
        return candidate

    def get_candidate(self, candidate_id: str) -> Candidate:
        """Return the current immutable candidate or raise a deterministic error."""
        try:
            return self._candidates[candidate_id]
        except KeyError as error:
            raise CandidateNotFoundError(f"Candidate was not found: {candidate_id}") from error

    def start_observation(self, candidate_id: str, timestamp: datetime) -> Candidate:
        """Transition a NEW candidate to OBSERVING."""
        return self._transition(candidate_id, CandidateState.OBSERVING, timestamp)

    def start_validation(self, candidate_id: str, timestamp: datetime) -> Candidate:
        """Transition an OBSERVING candidate to VALIDATING."""
        return self._transition(candidate_id, CandidateState.VALIDATING, timestamp)

    def qualify(self, candidate_id: str, timestamp: datetime) -> Candidate:
        """Transition a VALIDATING candidate to QUALIFIED."""
        return self._transition(candidate_id, CandidateState.QUALIFIED, timestamp)

    def reject(self, candidate_id: str, timestamp: datetime) -> Candidate:
        """Transition a VALIDATING candidate to REJECTED."""
        return self._transition(candidate_id, CandidateState.REJECTED, timestamp)

    def expire(self, candidate_id: str, timestamp: datetime) -> Candidate:
        """Transition an OBSERVING or VALIDATING candidate to EXPIRED."""
        return self._transition(candidate_id, CandidateState.EXPIRED, timestamp)

    def mark_executed(self, candidate_id: str, timestamp: datetime) -> Candidate:
        """Transition a QUALIFIED candidate to EXECUTED without creating an order."""
        return self._transition(candidate_id, CandidateState.EXECUTED, timestamp)

    def _transition(
        self,
        candidate_id: str,
        new_state: CandidateState,
        timestamp: datetime,
    ) -> Candidate:
        """Apply one permitted lifecycle transition and append its immutable event."""
        candidate = self.get_candidate(candidate_id)
        if candidate.state in self._FINAL_STATES:
            raise CandidateAlreadyFinalizedError(
                f"Candidate is finalized in state {candidate.state.value}: {candidate_id}"
            )
        if not isinstance(timestamp, datetime):
            raise CandidateError("Candidate transition timestamp must be a datetime.")

        event_type = self._TRANSITIONS.get((candidate.state, new_state))
        if event_type is None:
            raise InvalidStateTransitionError(
                f"Invalid candidate transition: {candidate.state.value} -> {new_state.value}"
            )

        revision = candidate.revision + 1
        event = CandidateEvent(
            schema_version=self.SCHEMA_VERSION,
            event_id=f"{candidate_id}:{revision}",
            candidate_id=candidate_id,
            previous_state=candidate.state,
            new_state=new_state,
            timestamp=timestamp,
            event_type=event_type,
        )
        updated_candidate = Candidate(
            schema_version=candidate.schema_version,
            candidate_id=candidate.candidate_id,
            observation=candidate.observation,
            state=new_state,
            created_at=candidate.created_at,
            updated_at=timestamp,
            revision=revision,
            event_history=(*candidate.event_history, event),
        )
        self._candidates[candidate_id] = updated_candidate
        return updated_candidate
