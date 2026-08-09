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

from boe.observers.compression_observer import (
    CompressionObserver, 
    CompressionObserverConfig,
    CompressionObserverError
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


class TestCompressionObserver(unittest.TestCase):
    def setUp(self):
        self.ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.config = CompressionObserverConfig("1.0.0", {
            "NONE": 0,
            "WEAK": 1,
            "MODERATE": 2,
            "STRONG": 3,
            "EXTREME": 4,
            "SUPER_EXTREME": 5,
            "ULTRA_EXTREME": 6,
            "MEGA_EXTREME": 7,
            "GIGA_EXTREME": 8
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

    def test_behaviour_compresses(self):
        """Test when amplitude of changes strictly decreases."""
        # Ranks: 0, 4, 1, 3
        # Differences: |4-0|=4, |1-4|=3, |3-1|=2
        # Amplitudes: 3-4=-1, 2-3=-1
        # Expect: Compression
        cursors = [
            self._create_cursor("NONE"),
            self._create_cursor("EXTREME"),
            self._create_cursor("WEAK"),
            self._create_cursor("STRONG", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = CompressionObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertTrue(evidence.observed)
        self.assertTrue(evidence.metadata["CompressionObserved"])
        self.assertFalse(evidence.metadata["ExpansionObserved"])
        self.assertEqual(evidence.metadata["CompressionStrength"], 2)
        self.assertEqual(evidence.metadata["ExpansionStrength"], 0)
        self.assertEqual(evidence.metadata["CompressionConsistency"], 1.0)
        self.assertEqual(evidence.metadata["CompressionDuration"], 2)

    def test_behaviour_expands(self):
        """Test when amplitude of changes strictly increases."""
        # Ranks: 3, 2, 4, 1
        # Differences: |2-3|=1, |4-2|=2, |1-4|=3
        # Amplitudes: 2-1=1, 3-2=1
        # Expect: Expansion
        cursors = [
            self._create_cursor("STRONG"),
            self._create_cursor("MODERATE"),
            self._create_cursor("EXTREME"),
            self._create_cursor("WEAK", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = CompressionObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertFalse(evidence.observed)
        self.assertFalse(evidence.metadata["CompressionObserved"])
        self.assertTrue(evidence.metadata["ExpansionObserved"])
        self.assertEqual(evidence.metadata["CompressionStrength"], 0)
        self.assertEqual(evidence.metadata["ExpansionStrength"], 2)
        self.assertEqual(evidence.metadata["CompressionConsistency"], 0.0)
        self.assertEqual(evidence.metadata["CompressionDuration"], 0)

    def test_alternating_compression(self):
        """Test alternating expansion and compression."""
        # Ranks: 0, 2, 1, 4, 2
        # Diff: 2, 1, 3, 2
        # Amp: -1, +2, -1
        # Compr Strength = 2, Exp Strength = 2.
        # Neither observed as strictly greater.
        cursors = [
            self._create_cursor("NONE"),
            self._create_cursor("MODERATE"),
            self._create_cursor("WEAK"),
            self._create_cursor("EXTREME"),
            self._create_cursor("MODERATE", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = CompressionObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertFalse(evidence.observed)
        self.assertFalse(evidence.metadata["CompressionObserved"])
        self.assertFalse(evidence.metadata["ExpansionObserved"])
        self.assertEqual(evidence.metadata["CompressionStrength"], 2)
        self.assertEqual(evidence.metadata["ExpansionStrength"], 2)
        self.assertEqual(evidence.metadata["CompressionConsistency"], 2.0 / 3.0)
        self.assertEqual(evidence.metadata["CompressionDuration"], 1)

    def test_no_compression(self):
        """Test constant step changes (no acceleration of amplitude)."""
        # Ranks: 1, 2, 3, 4
        # Diff: 1, 1, 1
        # Amp: 0, 0
        cursors = [
            self._create_cursor("WEAK"),
            self._create_cursor("MODERATE"),
            self._create_cursor("STRONG"),
            self._create_cursor("EXTREME", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = CompressionObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertFalse(evidence.observed)
        self.assertFalse(evidence.metadata["CompressionObserved"])
        self.assertEqual(evidence.metadata["CompressionStrength"], 0)
        self.assertEqual(evidence.metadata["ExpansionStrength"], 0)
        self.assertEqual(evidence.metadata["CompressionConsistency"], 0.0)
        self.assertEqual(evidence.metadata["CompressionDuration"], 2)

    def test_single_frame(self):
        """Test with only a single frame."""
        cursors = [self._create_cursor("MODERATE", is_last=True)]
        engine = MockReplayEngine(cursors)
        observer = CompressionObserver(self.config, engine)
        
        evidence = observer.observe(self._create_timeline())
        
        self.assertFalse(evidence.observed)
        self.assertEqual(evidence.metadata["CompressionStrength"], 0)

    def test_empty_replay(self):
        """Test with an empty replay (should raise ObserverError)."""
        empty_cursor = ReplayCursor(0, 0, ReplayState.COMPLETE, None, None)
        engine = MockReplayEngine([empty_cursor])
        observer = CompressionObserver(self.config, engine)
        
        with self.assertRaises(CompressionObserverError):
            observer.observe(self._create_timeline())

    def test_config_parsing(self):
        """Test config parsing from JSON without magic strings."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump({
                "schema_version": "1.0.0",
                "compression_ranks": {"A": 1, "B": 2}
            }, f)
            path = f.name
            
        try:
            config = CompressionObserverConfig.from_json(path)
            self.assertEqual(config.compression_ranks["A"], 1)
        finally:
            Path(path).unlink()

    def test_determinism_and_immutability(self):
        """Test that Evidence is immutable and deterministic."""
        cursors = [
            self._create_cursor("NONE"),
            self._create_cursor("EXTREME"),
            self._create_cursor("WEAK"),
            self._create_cursor("STRONG", is_last=True)
        ]
        engine = MockReplayEngine(cursors)
        observer = CompressionObserver(self.config, engine)
        timeline = self._create_timeline()
        
        ev1 = observer.observe(timeline)
        engine.restart()
        ev2 = observer.observe(timeline)
        
        self.assertEqual(ev1, ev2)
        
        with self.assertRaises(Exception):
            ev1.confidence = 0.5
