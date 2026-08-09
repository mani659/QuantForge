import unittest
from datetime import datetime, timezone
import json
import tempfile
from pathlib import Path

from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.temporal.behavior_frame import BehaviorFrame
from boe.replay.replay_cursor import ReplayCursor
from boe.replay.replay_state import ReplayState
from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_result import ReplayResult

from boe.observers.recoil_observer import (
    RecoilObserver, 
    RecoilObserverConfig,
    RecoilObserverError
)
from boe.evidence.evidence import Evidence


class MockReplayEngine(ReplayEngineContract):
    def __init__(self, cursors: list[ReplayCursor]):
        self.cursors = cursors
        self.idx = 0
        self.loaded_timeline_id = None

    def load(self, timeline_id: str) -> None:
        self.loaded_timeline_id = timeline_id

    def start(self) -> None:
        self.idx = 0

    def step(self) -> ReplayCursor:
        if self.idx >= len(self.cursors):
            # Should not happen in these tests if replay logic is correct
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


class TestRecoilObserver(unittest.TestCase):
    def setUp(self):
        self.ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.config = RecoilObserverConfig("1.0.0", "price", "direction")

    def _create_timeline(self, direction: str) -> FrozenBehaviorTimeline:
        return FrozenBehaviorTimeline(
            schema_version="1.0.0",
            timeline_id="time_001",
            candidate_id="cand_001",
            created_timestamp=self.ts,
            closed_timestamp=self.ts,
            termination_reason="TIMEOUT",
            frames=(),  # Observer doesn't read frames directly from here
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

    def test_perfect_recoil_up(self):
        """Test a perfect 1.0 recovery against an UP direction."""
        # Prices: 100 -> 90 -> 100
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(90.0),
            self._create_cursor(100.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = RecoilObserver(self.config, engine)
        
        timeline = self._create_timeline("UP")
        evidence = observer.observe(timeline)
        
        self.assertIsInstance(evidence, Evidence)
        self.assertEqual(evidence.confidence, 1.0)
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["RecoveryRatio"], 1.0)
        self.assertEqual(evidence.metadata["RecoveryDelay"], 1) # Frame 2 - Frame 1
        self.assertEqual(evidence.metadata["RecoveryDirection"], "UP")

    def test_partial_recoil_down(self):
        """Test a partial recovery against a DOWN direction."""
        # Prices: 100 -> 110 -> 105
        # Direction DOWN. Excursion UP to 110. Recovers DOWN to 105.
        # Max adverse excursion = 10
        # Recovered = 110 - 105 = 5
        # Ratio = 0.5
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(110.0),
            self._create_cursor(105.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = RecoilObserver(self.config, engine)
        
        timeline = self._create_timeline("DOWN")
        evidence = observer.observe(timeline)
        
        self.assertEqual(evidence.metadata["RecoveryRatio"], 0.5)

    def test_no_recoil(self):
        """Test when price never moves against the direction."""
        # Prices: 100 -> 110 -> 120
        # Direction UP. 
        # Excursion = 0.
        cursors = [
            self._create_cursor(100.0),
            self._create_cursor(110.0),
            self._create_cursor(120.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = RecoilObserver(self.config, engine)
        
        timeline = self._create_timeline("UP")
        evidence = observer.observe(timeline)
        
        self.assertEqual(evidence.metadata["RecoveryRatio"], 0.0)
        self.assertFalse(evidence.metadata["RecoveryObserved"])

    def test_single_frame(self):
        """Test with only a single frame."""
        cursors = [
            self._create_cursor(100.0, is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = RecoilObserver(self.config, engine)
        timeline = self._create_timeline("UP")
        
        evidence = observer.observe(timeline)
        self.assertEqual(evidence.metadata["RecoveryRatio"], 0.0)

    def test_empty_replay(self):
        """Test with zero frames in replay."""
        # A replay engine might step and immediately return COMPLETE with no snapshot
        # But step() normally returns a cursor. Let's say it raises or returns empty.
        # Actually our mock always returns something. Let's make an empty mock.
        class EmptyEngine(ReplayEngineContract):
            def load(self, t): pass
            def start(self): pass
            def step(self): raise StopIteration # But contract doesn't use exceptions for EOF usually
            def restart(self): pass
            def replay_all(self): return ()
            def finish(self): pass
            
        # The observer loops until cursor.status == COMPLETE.
        # If cursor has no snapshot, it raises RecoilObserverError.
        # We can mock a cursor with COMPLETE and no snapshot.
        empty_cursor = ReplayCursor(0, 0, ReplayState.COMPLETE, None, None)
        engine = MockReplayEngine([empty_cursor])
        observer = RecoilObserver(self.config, engine)
        timeline = self._create_timeline("UP")
        
        with self.assertRaises(RecoilObserverError):
            observer.observe(timeline)

    def test_invalid_timeline_direction(self):
        """Test when timeline has no direction."""
        engine = MockReplayEngine([])
        observer = RecoilObserver(self.config, engine)
        timeline = self._create_timeline("INVALID")
        
        with self.assertRaises(RecoilObserverError):
            observer.observe(timeline)

    def test_config_parsing(self):
        """Test config can be parsed from JSON without magic strings."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump({
                "schema_version": "1.0.0",
                "price_field": "close_price",
                "direction_field": "expected_dir"
            }, f)
            path = f.name
            
        try:
            config = RecoilObserverConfig.from_json(path)
            self.assertEqual(config.price_field, "close_price")
        finally:
            Path(path).unlink()

    def test_determinism_and_immutability(self):
        """Test output Evidence is completely immutable."""
        cursors = [self._create_cursor(100.0, is_last=True)]
        engine = MockReplayEngine(cursors)
        observer = RecoilObserver(self.config, engine)
        timeline = self._create_timeline("UP")
        
        ev1 = observer.observe(timeline)
        engine.restart()
        ev2 = observer.observe(timeline)
        
        # Exact same timestamp should result in same hash
        self.assertEqual(ev1, ev2)
        
        # Try mutation
        with self.assertRaises(Exception):
            ev1.confidence = 0.5
