import unittest
from datetime import datetime, timezone
import json
import tempfile
from pathlib import Path

from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.replay.replay_cursor import ReplayCursor
from boe.replay.replay_state import ReplayState
from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_result import ReplayResult

from boe.observers.failure_observer import (
    FailureObserver, 
    FailureObserverConfig,
    FailureObserverError
)
from boe.evidence.evidence import Evidence


class MockReplayEngine(ReplayEngineContract):
    def __init__(self, cursors: list[ReplayCursor]):
        self.cursors = cursors
        self.idx = 0

    def load(self, timeline_id: str) -> None:
        pass

    def start(self) -> None:
        self.idx = 0

    def step(self) -> ReplayCursor:
        if self.idx >= len(self.cursors):
            return self.cursors[-1]
        c = self.cursors[self.idx]
        self.idx += 1
        return c

    def restart(self) -> None:
        self.idx = 0

    def replay_all(self) -> tuple[ReplayCursor, ...]:
        return tuple(self.cursors)

    def finish(self) -> ReplayResult:
        return ReplayResult("mock", len(self.cursors), ReplayState.COMPLETE)


class TestFailureObserver(unittest.TestCase):
    def setUp(self):
        self.ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.config = FailureObserverConfig("1.0.0", "price", "direction")

    def _create_timeline(self, direction: str, termination_reason: str = "TIMEOUT") -> FrozenBehaviorTimeline:
        return FrozenBehaviorTimeline(
            schema_version="1.0.0",
            timeline_id="time_001",
            candidate_id="cand_001",
            created_timestamp=self.ts,
            closed_timestamp=self.ts,
            termination_reason=termination_reason,
            frames=(),
            timeline_metadata={"direction": direction}
        )

    def _create_cursor(self, price: float, is_last: bool = False) -> ReplayCursor:
        snapshot = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_1",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=self.ts,
            source="test",
            market_state={"price": price}
        )
        return ReplayCursor(
            position=0,
            total_frames=1,
            status=ReplayState.COMPLETE if is_last else ReplayState.PLAYING,
            current_frame=None,
            current_snapshot=snapshot
        )

    def test_behaviour_never_fails(self):
        """Test when price never moves against the direction."""
        # UP expected. Prices: 100 -> 110 -> 120
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(110.0),
            self._create_cursor(120.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = FailureObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline("UP"))
        
        self.assertFalse(evidence.observed)
        self.assertEqual(evidence.metadata["FailureType"], "NONE")
        self.assertEqual(evidence.metadata["FailureSeverity"], 0.0)
        self.assertEqual(evidence.metadata["FailureDelay"], 0)

    def test_immediate_failure(self):
        """Test when price immediately moves against the direction."""
        # UP expected. Prices: 100 -> 90 -> 80
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(90.0),
            self._create_cursor(80.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = FailureObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline("UP"))
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["FailureType"], "IMMEDIATE_COLLAPSE")
        self.assertEqual(evidence.metadata["FailureSeverity"], 20.0)
        self.assertEqual(evidence.metadata["FailureDelay"], 1)

    def test_late_failure_and_direction_reversal(self):
        """Test when price goes favorable for a while, then fails."""
        # DOWN expected. Prices: 100 -> 90 -> 85 -> 110
        # Reference=100. Min=85. Max adverse=110.
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(90.0),
            self._create_cursor(85.0),
            self._create_cursor(110.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = FailureObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline("DOWN", "STOP_LOSS"))
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["FailureType"], "REVERSAL")
        self.assertEqual(evidence.metadata["FailureSeverity"], 10.0)
        self.assertEqual(evidence.metadata["FailureDelay"], 3)
        self.assertEqual(evidence.metadata["BehaviourTermination"], "STOP_LOSS")

    def test_gradual_collapse(self):
        """Test gradual adverse excursion over multiple frames."""
        # UP expected. Prices: 100 -> 99 -> 95 -> 90
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(99.0),
            self._create_cursor(95.0),
            self._create_cursor(90.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = FailureObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline("UP"))
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["FailureType"], "IMMEDIATE_COLLAPSE")
        self.assertEqual(evidence.metadata["FailureSeverity"], 10.0)
        self.assertEqual(evidence.metadata["FailureDelay"], 1)

    def test_single_frame(self):
        """Test with only a single frame."""
        cursors = [self._create_cursor(100.0, is_last=True)]
        engine = MockReplayEngine(cursors)
        observer = FailureObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline("UP"))
        
        self.assertFalse(evidence.observed)
        self.assertEqual(evidence.metadata["FailureType"], "NONE")
        self.assertEqual(evidence.metadata["FailureSeverity"], 0.0)
        self.assertEqual(evidence.metadata["FailureDelay"], 0)

    def test_empty_replay(self):
        """Test with an empty replay (should raise ObserverError)."""
        empty_cursor = ReplayCursor(0, 0, ReplayState.COMPLETE, None, None)
        engine = MockReplayEngine([empty_cursor])
        observer = FailureObserver(self.config, engine)
        
        with self.assertRaises(FailureObserverError):
            observer.observe(self._create_timeline("UP"))

    def test_invalid_direction(self):
        """Test invalid direction in timeline metadata."""
        engine = MockReplayEngine([])
        observer = FailureObserver(self.config, engine)
        
        with self.assertRaises(FailureObserverError):
            observer.observe(self._create_timeline("SIDEWAYS"))

    def test_config_parsing(self):
        """Test config parsing from JSON without magic strings."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump({
                "schema_version": "1.0.0",
                "price_field": "bid",
                "direction_field": "expected"
            }, f)
            path = f.name
            
        try:
            config = FailureObserverConfig.from_json(path)
            self.assertEqual(config.price_field, "bid")
            self.assertEqual(config.direction_field, "expected")
        finally:
            Path(path).unlink()

    def test_determinism_and_immutability(self):
        """Test that Evidence is immutable and deterministic."""
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(90.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = FailureObserver(self.config, engine)
        timeline = self._create_timeline("UP")
        
        ev1 = observer.observe(timeline)
        engine.restart()
        ev2 = observer.observe(timeline)
        
        self.assertEqual(ev1, ev2)
        
        with self.assertRaises(Exception):
            ev1.confidence = 0.5
