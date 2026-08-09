import unittest
from datetime import datetime, timezone
import json
import tempfile
from pathlib import Path

from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline
from boe.temporal.behavior_frame import BehaviorFrame
from boe.replay.replay_cursor import ReplayCursor
from boe.replay.replay_state import ReplayState
from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_result import ReplayResult

from boe.observers.velocity_observer import (
    VelocityObserver, 
    VelocityObserverConfig,
    VelocityObserverError
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


class TestVelocityObserver(unittest.TestCase):
    def setUp(self):
        self.ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.config = VelocityObserverConfig("1.0.0", {
            "NONE": 0,
            "WEAK": 1,
            "MODERATE": 2,
            "STRONG": 3,
            "EXTREME": 4
        })

    def _create_timeline(self) -> FrozenBehaviorTimeline:
        return FrozenBehaviorTimeline(
            schema_version="1.0.0",
            timeline_id="time_001",
            candidate_id="cand_001",
            created_timestamp=self.ts,
            closed_timestamp=self.ts,
            termination_reason="TIMEOUT",
            frames=(),
            timeline_metadata={}
        )

    def _create_cursor(self, strength: str, is_last: bool = False) -> ReplayCursor:
        frame = BehaviorFrame(
            schema_version="1.0.0",
            frame_id="f1",
            timeline_id="time_001",
            timestamp=self.ts,
            environment_snapshot_id="snap_1",
            behavior_state="ACTIVE",
            behavior_strength=strength,
            metadata={}
        )
        return ReplayCursor(
            position=0,
            total_frames=1,
            status=ReplayState.COMPLETE if is_last else ReplayState.PLAYING,
            current_frame=frame,
            current_snapshot=None
        )

    def test_increasing_velocity(self):
        """Test monotonically increasing behavioural strength."""
        cursors = [
            self._create_cursor("WEAK"),
            self._create_cursor("MODERATE"),
            self._create_cursor("STRONG", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = VelocityObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["VelocityDirection"], "INCREASING")
        self.assertEqual(evidence.metadata["VelocityMagnitude"], 2) # STRONG(3) - WEAK(1)
        self.assertEqual(evidence.metadata["VelocityConsistency"], 1.0)
        self.assertEqual(evidence.metadata["VelocityStability"], 0.0)

    def test_decreasing_velocity(self):
        """Test monotonically decreasing behavioural strength."""
        cursors = [
            self._create_cursor("EXTREME"),
            self._create_cursor("STRONG"),
            self._create_cursor("MODERATE"),
            self._create_cursor("WEAK", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = VelocityObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["VelocityDirection"], "DECREASING")
        self.assertEqual(evidence.metadata["VelocityMagnitude"], -3) # WEAK(1) - EXTREME(4)
        self.assertEqual(evidence.metadata["VelocityConsistency"], 1.0)
        self.assertEqual(evidence.metadata["VelocityStability"], 0.0)

    def test_stable_behaviour(self):
        """Test completely stable behaviour."""
        cursors = [
            self._create_cursor("MODERATE"),
            self._create_cursor("MODERATE"),
            self._create_cursor("MODERATE", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = VelocityObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["VelocityDirection"], "STABLE")
        self.assertEqual(evidence.metadata["VelocityMagnitude"], 0)
        self.assertEqual(evidence.metadata["VelocityConsistency"], 0.0)
        self.assertEqual(evidence.metadata["VelocityStability"], 1.0)

    def test_oscillating_behaviour(self):
        """Test oscillating behaviour."""
        cursors = [
            self._create_cursor("MODERATE"),
            self._create_cursor("STRONG"),
            self._create_cursor("MODERATE"),
            self._create_cursor("STRONG", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = VelocityObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["VelocityDirection"], "OSCILLATING")
        self.assertEqual(evidence.metadata["VelocityMagnitude"], 1) # STRONG(3) - MODERATE(2)
        self.assertEqual(evidence.metadata["VelocityConsistency"], 2.0 / 3.0) # 2 ups, 1 down
        self.assertEqual(evidence.metadata["VelocityStability"], 0.0)

    def test_very_long_replay(self):
        """Test a long replay to verify stability/consistency calculations."""
        # 10 WEAK, 5 MODERATE, 5 WEAK
        cursors = [self._create_cursor("WEAK") for _ in range(10)]
        cursors += [self._create_cursor("MODERATE") for _ in range(5)]
        cursors += [self._create_cursor("WEAK") for _ in range(4)]
        cursors.append(self._create_cursor("WEAK", is_last=True))
        
        engine = MockReplayEngine(cursors)
        observer = VelocityObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertTrue(evidence.observed)
        self.assertEqual(evidence.metadata["VelocityDirection"], "OSCILLATING")
        self.assertEqual(evidence.metadata["VelocityMagnitude"], 0)
        
        # 19 steps total.
        # step 10: WEAK -> MODERATE (up)
        # step 15: MODERATE -> WEAK (down)
        # 17 steps: stable.
        self.assertEqual(evidence.metadata["VelocityStability"], 17.0 / 19.0)
        self.assertEqual(evidence.metadata["VelocityConsistency"], 1.0 / 19.0)

    def test_single_frame(self):
        """Test with only a single frame."""
        cursors = [self._create_cursor("MODERATE", is_last=True)]
        engine = MockReplayEngine(cursors)
        observer = VelocityObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertFalse(evidence.observed)
        self.assertEqual(evidence.metadata["VelocityDirection"], "STABLE")
        self.assertEqual(evidence.metadata["VelocityMagnitude"], 0)

    def test_empty_replay(self):
        """Test with an empty replay (should raise ObserverError)."""
        empty_cursor = ReplayCursor(0, 0, ReplayState.COMPLETE, None, None)
        engine = MockReplayEngine([empty_cursor])
        observer = VelocityObserver(self.config, engine)
        
        with self.assertRaises(VelocityObserverError):
            observer.observe(self._create_timeline())

    def test_config_parsing(self):
        """Test config parsing from JSON without magic strings."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump({
                "schema_version": "1.0.0",
                "strength_ranks": {"A": 1, "B": 2}
            }, f)
            path = f.name
            
        try:
            config = VelocityObserverConfig.from_json(path)
            self.assertEqual(config.strength_ranks["A"], 1)
        finally:
            Path(path).unlink()

    def test_determinism_and_immutability(self):
        """Test that Evidence is immutable and deterministic."""
        cursors = [
            self._create_cursor("WEAK"),
            self._create_cursor("MODERATE", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = VelocityObserver(self.config, engine)
        timeline = self._create_timeline()
        
        ev1 = observer.observe(timeline)
        engine.restart()
        ev2 = observer.observe(timeline)
        
        self.assertEqual(ev1, ev2)
        
        with self.assertRaises(Exception):
            ev1.confidence = 0.5
