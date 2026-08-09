"""Deterministic tests for the Behavior Observation Window."""

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.candidate import Candidate
from boe.candidate_state import CandidateState
from boe.behavior_observation import BehaviorObservation
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.observation.observation_config import ObservationConfig
from boe.observation.observation_policy import DefaultObservationPolicy
from boe.observation.termination_reason import TerminationReason
from boe.observation.bow_contract import BehaviorObservationWindowContract
from boe.observation.bow import BehaviorObservationWindow
from boe.observation.bow_result import BOWResult
from boe.observation.bow_errors import (
    WindowAlreadyOpenError,
    WindowNotOpenError,
    InvalidSnapshotError,
    AppendAfterFreezeError,
    DoubleFreezeError,
    TimelineFailureError
)


class TestBehaviorObservationWindow(unittest.TestCase):
    """Deterministic regression tests for the BOW."""

    def setUp(self) -> None:
        self.bow = BehaviorObservationWindow()
        self.config = ObservationConfig(
            schema_version="1.0.0",
            max_frames=5,
            max_duration=60.0
        )
        self.policy = DefaultObservationPolicy(self.config)

        # Base timestamp for deterministic replay
        self.t0 = datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)
        
        self.candidate = Candidate(
            schema_version="1.0.0",
            candidate_id="cand_test_01",
            observation=BehaviorObservation(
                schema_version="1.0.0",
                observation_id="obs_01",
                environment_id="env_01",
                behavior_type="TEST",
                instrument="EURUSD",
                timeframe="M1",
                observed_at=self.t0,
                detector_id="det_01",
                detector_version="1.0.0"
            ),
            state=CandidateState.OBSERVING,
            created_at=self.t0,
            updated_at=self.t0,
            revision=0,
            event_history=()
        )

        self.snapshot1 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_01",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=datetime(2026, 7, 28, 12, 0, 10, tzinfo=timezone.utc),
            source="test",
            market_state={"price": 1.10}
        )
        
        self.snapshot2 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_02",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=datetime(2026, 7, 28, 12, 0, 20, tzinfo=timezone.utc),
            source="test",
            market_state={"price": 1.11}
        )

    def test_contract_compliance(self) -> None:
        self.assertIsInstance(self.bow, BehaviorObservationWindowContract)

    def test_open_window(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        self.assertEqual(self.bow._timeline._timeline_id, "tl_001") # type: ignore
        self.assertEqual(self.bow._timeline._candidate_id, "cand_test_01") # type: ignore
        self.assertEqual(self.bow._opened_timestamp, self.t0)

    def test_open_already_open_raises(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        with self.assertRaises(WindowAlreadyOpenError):
            self.bow.open(self.candidate, "tl_002", self.t0)

    def test_append_without_open_raises(self) -> None:
        with self.assertRaises(WindowNotOpenError):
            self.bow.append_snapshot(
                self.snapshot1, "frame_01", "STATE", "STRONG", {}
            )

    def test_append_snapshots(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        self.bow.append_snapshot(self.snapshot1, "frame_01", "STATE_1", "STRONG", {})
        self.bow.append_snapshot(self.snapshot2, "frame_02", "STATE_2", "WEAK", {})
        
        self.assertEqual(self.bow._timeline.frame_count(), 2) # type: ignore

    def test_append_invalid_snapshot_raises(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        with self.assertRaises(InvalidSnapshotError):
            self.bow.append_snapshot(
                "not_a_snapshot", "frame_01", "STATE_1", "STRONG", {} # type: ignore
            )

    def test_evaluate_policy_early_termination(self) -> None:
        """Tests that policy evaluates to TERMINATE when criteria met."""
        self.bow.open(self.candidate, "tl_001", self.t0)
        # Append 5 frames to hit max_frames=5
        for i in range(5):
            snap = EnvironmentSnapshot(
                schema_version="1.0.0",
                snapshot_id=f"snap_{i}",
                instrument="EURUSD",
                timeframe="M1",
                timestamp=self.t0,
                source="test",
                market_state={"price": 1.10}
            )
            self.bow.append_snapshot(snap, f"frame_{i}", "S", "S", {})
            
        t_eval = datetime(2026, 7, 28, 12, 0, 5, tzinfo=timezone.utc)
        decision = self.bow.evaluate_policy(t_eval, self.policy)
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.WINDOW_COMPLETE)

    def test_evaluate_policy_max_duration_termination(self) -> None:
        """Tests max duration termination."""
        self.bow.open(self.candidate, "tl_001", self.t0)
        self.bow.append_snapshot(self.snapshot1, "frame_01", "S", "S", {})
        
        # 61 seconds later
        t_eval = datetime(2026, 7, 28, 12, 1, 1, tzinfo=timezone.utc)
        decision = self.bow.evaluate_policy(t_eval, self.policy)
        
        self.assertTrue(decision.terminate_observation)
        self.assertEqual(decision.termination_reason, TerminationReason.MAX_DURATION)

    def test_freeze(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        self.bow.append_snapshot(self.snapshot1, "frame_01", "STATE_1", "STRONG", {})
        
        t_close = datetime(2026, 7, 28, 12, 0, 15, tzinfo=timezone.utc)
        result = self.bow.freeze(t_close, TerminationReason.WINDOW_COMPLETE, {"meta": "data"})
        
        self.assertIsInstance(result, BOWResult)
        self.assertEqual(result.termination_reason, TerminationReason.WINDOW_COMPLETE)
        self.assertEqual(result.frame_count, 1)
        self.assertEqual(result.duration_seconds, 15.0)
        self.assertEqual(result.timeline.termination_reason, "WINDOW_COMPLETE")
        self.assertEqual(len(result.timeline.frames), 1)

    def test_freeze_without_open_raises(self) -> None:
        t_close = datetime(2026, 7, 28, 12, 0, 15, tzinfo=timezone.utc)
        with self.assertRaises(WindowNotOpenError):
            self.bow.freeze(t_close, TerminationReason.WINDOW_COMPLETE)

    def test_double_freeze_rejection(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        t_close = datetime(2026, 7, 28, 12, 0, 15, tzinfo=timezone.utc)
        self.bow.freeze(t_close, TerminationReason.WINDOW_COMPLETE)
        
        with self.assertRaises(DoubleFreezeError):
            self.bow.freeze(t_close, TerminationReason.WINDOW_COMPLETE)

    def test_append_after_freeze_rejection(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        t_close = datetime(2026, 7, 28, 12, 0, 15, tzinfo=timezone.utc)
        self.bow.freeze(t_close, TerminationReason.WINDOW_COMPLETE)
        
        with self.assertRaises(AppendAfterFreezeError):
            self.bow.append_snapshot(self.snapshot1, "frame_01", "STATE_1", "STRONG", {})

    def test_timeline_integrity_and_immutable_frozen_output(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        self.bow.append_snapshot(self.snapshot1, "frame_01", "STATE_1", "STRONG", {"info": 1})
        self.bow.append_snapshot(self.snapshot2, "frame_02", "STATE_2", "WEAK", {"info": 2})
        
        t_close = datetime(2026, 7, 28, 12, 0, 30, tzinfo=timezone.utc)
        result = self.bow.freeze(t_close, TerminationReason.POLICY_TERMINATED)
        
        timeline = result.timeline
        self.assertEqual(timeline.timeline_id, "tl_001")
        self.assertEqual(timeline.candidate_id, "cand_test_01")
        self.assertEqual(timeline.created_timestamp, self.t0)
        self.assertEqual(timeline.closed_timestamp, t_close)
        self.assertEqual(len(timeline.frames), 2)
        self.assertEqual(timeline.frames[0].frame_id, "frame_01")
        self.assertEqual(timeline.frames[1].frame_id, "frame_02")
        
        # Test immutability via frozen dataclass
        import dataclasses
        with self.assertRaises(dataclasses.FrozenInstanceError):
            timeline.termination_reason = "CHANGED" # type: ignore

    def test_replay_determinism(self) -> None:
        """Tests that two identical sequences produce completely identical frozen output."""
        bow1 = BehaviorObservationWindow()
        bow2 = BehaviorObservationWindow()
        
        bow1.open(self.candidate, "tl_replay", self.t0)
        bow2.open(self.candidate, "tl_replay", self.t0)
        
        bow1.append_snapshot(self.snapshot1, "frame_1", "A", "B", {})
        bow2.append_snapshot(self.snapshot1, "frame_1", "A", "B", {})
        
        t_close = datetime(2026, 7, 28, 12, 0, 25, tzinfo=timezone.utc)
        
        result1 = bow1.freeze(t_close, TerminationReason.MAX_DURATION)
        result2 = bow2.freeze(t_close, TerminationReason.MAX_DURATION)
        
        self.assertEqual(result1.timeline, result2.timeline)

    def test_close_clears_state(self) -> None:
        self.bow.open(self.candidate, "tl_001", self.t0)
        self.bow.close()
        
        with self.assertRaises(WindowNotOpenError):
            self.bow.append_snapshot(self.snapshot1, "frame_01", "STATE_1", "STRONG", {})

        # Should be able to reopen
        self.bow.open(self.candidate, "tl_002", self.t0)
        self.assertEqual(self.bow._timeline._timeline_id, "tl_002") # type: ignore

if __name__ == "__main__":
    unittest.main()
