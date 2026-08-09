"""Deterministic regression tests for the Replay Engine."""

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.temporal.behavior_frame import BehaviorFrame
from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline
from boe.temporal.environment_repository_contract import EnvironmentRepositoryContract
from boe.temporal.timeline_repository_contract import TimelineRepositoryContract

from boe.replay import (
    ReplayEngineContract,
    ReplayEngine,
    ReplayCursor,
    ReplayResult,
    ReplayState,
    ReplayError,
    MissingTimelineError,
    MissingSnapshotError,
    ReplayNotLoadedError,
    ReplayAlreadyCompleteError,
    RepositoryFailureError
)

class MockEnvironmentRepository(EnvironmentRepositoryContract):
    def __init__(self) -> None:
        self.snapshots: dict[str, EnvironmentSnapshot] = {}
        self.should_fail = False

    def save(self, snapshot: EnvironmentSnapshot) -> None:
        self.snapshots[snapshot.snapshot_id] = snapshot

    def load(self, snapshot_id: str) -> EnvironmentSnapshot:
        if self.should_fail:
            raise ValueError("Injected repository failure")
        if snapshot_id not in self.snapshots:
            return None # type: ignore
        return self.snapshots[snapshot_id]

    def exists(self, snapshot_id: str) -> bool:
        return snapshot_id in self.snapshots

    def delete(self, snapshot_id: str) -> None:
        pass

    def list(self) -> tuple[str, ...]:
        return tuple(self.snapshots.keys())


class MockTimelineRepository(TimelineRepositoryContract):
    def __init__(self) -> None:
        self.timelines: dict[str, FrozenBehaviorTimeline] = {}
        self.should_fail = False

    def save(self, timeline: FrozenBehaviorTimeline) -> None:
        self.timelines[timeline.timeline_id] = timeline

    def load(self, timeline_id: str) -> FrozenBehaviorTimeline:
        if self.should_fail:
            raise ValueError("Injected repository failure")
        if timeline_id not in self.timelines:
            return None # type: ignore
        return self.timelines[timeline_id]

    def load_by_candidate(self, candidate_id: str) -> tuple[FrozenBehaviorTimeline, ...]:
        return tuple(t for t in self.timelines.values() if t.candidate_id == candidate_id)

    def exists(self, timeline_id: str) -> bool:
        return timeline_id in self.timelines

    def delete(self, timeline_id: str) -> None:
        pass

    def list(self) -> tuple[str, ...]:
        return tuple(self.timelines.keys())


class TestReplayEngine(unittest.TestCase):
    """Deterministic regression tests for ReplayEngine."""

    def setUp(self) -> None:
        self.env_repo = MockEnvironmentRepository()
        self.timeline_repo = MockTimelineRepository()
        self.engine = ReplayEngine(self.timeline_repo, self.env_repo)

        self.t0 = datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)
        self.t1 = datetime(2026, 7, 28, 12, 1, 0, tzinfo=timezone.utc)
        self.t2 = datetime(2026, 7, 28, 12, 2, 0, tzinfo=timezone.utc)

        self.snap0 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_00",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=self.t0,
            source="test",
            market_state={"price": 1.10}
        )
        self.snap1 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_01",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=self.t1,
            source="test",
            market_state={"price": 1.11}
        )
        self.snap2 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_02",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=self.t2,
            source="test",
            market_state={"price": 1.12}
        )

        self.env_repo.save(self.snap0)
        self.env_repo.save(self.snap1)
        self.env_repo.save(self.snap2)

        self.frame0 = BehaviorFrame(
            schema_version="1.0.0",
            frame_id="frame_0",
            timeline_id="tl_1",
            timestamp=self.t0,
            environment_snapshot_id="snap_00",
            behavior_state="BASE",
            behavior_strength="MODERATE",
            metadata={}
        )
        self.frame1 = BehaviorFrame(
            schema_version="1.0.0",
            frame_id="frame_1",
            timeline_id="tl_1",
            timestamp=self.t1,
            environment_snapshot_id="snap_01",
            behavior_state="BASE",
            behavior_strength="MODERATE",
            metadata={}
        )
        self.frame2 = BehaviorFrame(
            schema_version="1.0.0",
            frame_id="frame_2",
            timeline_id="tl_1",
            timestamp=self.t2,
            environment_snapshot_id="snap_02",
            behavior_state="BASE",
            behavior_strength="MODERATE",
            metadata={}
        )

        self.timeline = FrozenBehaviorTimeline(
            schema_version="1.0.0",
            timeline_id="tl_1",
            candidate_id="cand_1",
            created_timestamp=self.t0,
            closed_timestamp=self.t2,
            termination_reason="WINDOW_COMPLETE",
            frames=(self.frame0, self.frame1, self.frame2),
            timeline_metadata={}
        )
        self.timeline_repo.save(self.timeline)

        self.empty_timeline = FrozenBehaviorTimeline(
            schema_version="1.0.0",
            timeline_id="tl_empty",
            candidate_id="cand_1",
            created_timestamp=self.t0,
            closed_timestamp=self.t0,
            termination_reason="WINDOW_COMPLETE",
            frames=(),
            timeline_metadata={}
        )
        self.timeline_repo.save(self.empty_timeline)


    def test_contract_compliance(self) -> None:
        self.assertIsInstance(self.engine, ReplayEngineContract)

    def test_loading_replay(self) -> None:
        self.engine.load("tl_1")
        self.assertEqual(self.engine._status, ReplayState.LOADED)
        self.assertEqual(self.engine._timeline, self.timeline)

    def test_missing_timeline(self) -> None:
        with self.assertRaises(MissingTimelineError):
            self.engine.load("does_not_exist")

    def test_timeline_repo_failure(self) -> None:
        self.timeline_repo.should_fail = True
        with self.assertRaises(MissingTimelineError):
            self.engine.load("tl_1")

    def test_start_unloaded(self) -> None:
        with self.assertRaises(ReplayNotLoadedError):
            self.engine.start()

    def test_start_loaded(self) -> None:
        self.engine.load("tl_1")
        self.engine.start()
        self.assertEqual(self.engine._status, ReplayState.PLAYING)

    def test_start_empty_timeline(self) -> None:
        self.engine.load("tl_empty")
        self.engine.start()
        self.assertEqual(self.engine._status, ReplayState.COMPLETE)

    def test_single_step_replay(self) -> None:
        self.engine.load("tl_1")
        self.engine.start()
        
        cursor1 = self.engine.step()
        self.assertEqual(cursor1.position, 0)
        self.assertEqual(cursor1.total_frames, 3)
        self.assertEqual(cursor1.current_frame, self.frame0)
        self.assertEqual(cursor1.current_snapshot, self.snap0)
        self.assertEqual(cursor1.status, ReplayState.PLAYING)

    def test_full_replay(self) -> None:
        self.engine.load("tl_1")
        self.engine.start()
        
        cursors = self.engine.replay_all()
        self.assertEqual(len(cursors), 3)
        
        self.assertEqual(cursors[0].current_frame, self.frame0)
        self.assertEqual(cursors[1].current_frame, self.frame1)
        self.assertEqual(cursors[2].current_frame, self.frame2)
        
        self.assertEqual(cursors[2].status, ReplayState.COMPLETE)
        self.assertEqual(self.engine._status, ReplayState.COMPLETE)

    def test_restart(self) -> None:
        self.engine.load("tl_1")
        self.engine.start()
        self.engine.step()
        self.engine.step()
        
        self.engine.restart()
        self.assertEqual(self.engine._position, 0)
        self.assertEqual(self.engine._status, ReplayState.PLAYING)
        
        cursor = self.engine.step()
        self.assertEqual(cursor.current_frame, self.frame0)

    def test_end_of_stream(self) -> None:
        self.engine.load("tl_1")
        self.engine.start()
        self.engine.replay_all()
        
        with self.assertRaises(ReplayAlreadyCompleteError):
            self.engine.step()

    def test_missing_snapshot(self) -> None:
        self.engine.load("tl_1")
        self.engine.start()
        
        # Corrupt the repository
        self.env_repo.snapshots.pop("snap_00")
        
        with self.assertRaises(MissingSnapshotError):
            self.engine.step()

    def test_env_repo_failure(self) -> None:
        self.engine.load("tl_1")
        self.engine.start()
        self.env_repo.should_fail = True
        
        with self.assertRaises(MissingSnapshotError):
            self.engine.step()

    def test_replay_ordering(self) -> None:
        """Verify that playback depends ONLY upon stored timeline ordering."""
        self.engine.load("tl_1")
        self.engine.start()
        
        c0 = self.engine.step()
        c1 = self.engine.step()
        c2 = self.engine.step()
        
        self.assertEqual(c0.current_frame, self.frame0)
        self.assertEqual(c1.current_frame, self.frame1)
        self.assertEqual(c2.current_frame, self.frame2)

    def test_replay_determinism(self) -> None:
        """Verify bit-for-bit identical replay"""
        # Run replay 1
        self.engine.load("tl_1")
        self.engine.start()
        res1 = self.engine.replay_all()
        finish1 = self.engine.finish()
        
        # Run replay 2
        engine2 = ReplayEngine(self.timeline_repo, self.env_repo)
        engine2.load("tl_1")
        engine2.start()
        res2 = engine2.replay_all()
        finish2 = engine2.finish()
        
        self.assertEqual(res1, res2)
        self.assertEqual(finish1, finish2)
        self.assertIsInstance(finish1, ReplayResult)

if __name__ == "__main__":
    unittest.main()
