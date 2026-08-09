import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.behavior_observation import BehaviorObservation
from boe.candidate_errors import (
    CandidateAlreadyFinalizedError,
    CandidateNotFoundError,
    InvalidStateTransitionError,
)
from boe.candidate_events import CandidateEventType
from boe.candidate_manager import CandidateManager
from boe.candidate_state import CandidateState


class TestCandidateManager(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = CandidateManager()
        self.timestamp = datetime(2026, 7, 19, 12, 0, tzinfo=timezone.utc)
        self.observation = BehaviorObservation(
            schema_version="1.0.0",
            observation_id="observation_000001",
            environment_id="environment_000001",
            behavior_type="behavioral_mean_reversion",
            instrument="EURUSD",
            timeframe="M1",
            observed_at=self.timestamp,
            detector_id="test_detector",
            detector_version="1.0.0",
        )

    def _create_candidate(self):
        return self.manager.create_candidate("candidate_000001", self.observation, self.timestamp)

    def test_candidate_creation_generates_initial_event(self) -> None:
        candidate = self._create_candidate()
        self.assertEqual(candidate.state, CandidateState.NEW)
        self.assertEqual(candidate.revision, 0)
        self.assertEqual(len(candidate.event_history), 1)
        self.assertEqual(candidate.event_history[0].event_type, CandidateEventType.CANDIDATE_CREATED)

    def test_every_legal_transition_and_revision_increment(self) -> None:
        candidate = self._create_candidate()
        candidate = self.manager.start_observation(candidate.candidate_id, self.timestamp + timedelta(minutes=1))
        candidate = self.manager.start_validation(candidate.candidate_id, self.timestamp + timedelta(minutes=2))
        candidate = self.manager.qualify(candidate.candidate_id, self.timestamp + timedelta(minutes=3))
        candidate = self.manager.mark_executed(candidate.candidate_id, self.timestamp + timedelta(minutes=4))
        self.assertEqual(candidate.state, CandidateState.EXECUTED)
        self.assertEqual(candidate.revision, 4)
        self.assertEqual(len(candidate.event_history), 5)
        self.assertEqual(candidate.event_history[-1].event_type, CandidateEventType.CANDIDATE_EXECUTED)

    def test_rejection_and_expiration_paths(self) -> None:
        rejected = self._create_candidate()
        rejected = self.manager.start_observation(rejected.candidate_id, self.timestamp)
        rejected = self.manager.start_validation(rejected.candidate_id, self.timestamp)
        rejected = self.manager.reject(rejected.candidate_id, self.timestamp)
        self.assertEqual(rejected.state, CandidateState.REJECTED)

        expired = self.manager.create_candidate("candidate_000002", self.observation, self.timestamp)
        expired = self.manager.start_observation(expired.candidate_id, self.timestamp)
        expired = self.manager.expire(expired.candidate_id, self.timestamp)
        self.assertEqual(expired.state, CandidateState.EXPIRED)

        validating_expired = self.manager.create_candidate("candidate_000003", self.observation, self.timestamp)
        validating_expired = self.manager.start_observation(validating_expired.candidate_id, self.timestamp)
        validating_expired = self.manager.start_validation(validating_expired.candidate_id, self.timestamp)
        validating_expired = self.manager.expire(validating_expired.candidate_id, self.timestamp)
        self.assertEqual(validating_expired.state, CandidateState.EXPIRED)

    def test_every_illegal_transition_is_rejected(self) -> None:
        candidate = self._create_candidate()
        with self.assertRaises(InvalidStateTransitionError):
            self.manager.qualify(candidate.candidate_id, self.timestamp)
        candidate = self.manager.start_observation(candidate.candidate_id, self.timestamp)
        with self.assertRaises(InvalidStateTransitionError):
            self.manager.mark_executed(candidate.candidate_id, self.timestamp)

    def test_finalized_candidate_cannot_transition(self) -> None:
        candidate = self._create_candidate()
        candidate = self.manager.start_observation(candidate.candidate_id, self.timestamp)
        candidate = self.manager.expire(candidate.candidate_id, self.timestamp)
        with self.assertRaises(CandidateAlreadyFinalizedError):
            self.manager.start_validation(candidate.candidate_id, self.timestamp)

    def test_candidate_and_events_are_immutable(self) -> None:
        candidate = self._create_candidate()
        with self.assertRaises(FrozenInstanceError):
            candidate.state = CandidateState.OBSERVING
        with self.assertRaises(FrozenInstanceError):
            candidate.event_history[0].event_type = CandidateEventType.CANDIDATE_QUALIFIED

    def test_missing_candidate_raises_deterministic_error(self) -> None:
        with self.assertRaises(CandidateNotFoundError):
            self.manager.get_candidate("missing")


if __name__ == "__main__":
    unittest.main()
