import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.temporal import (
    ActiveObservationTimeline,
    BehaviorFrame,
    EnvironmentSnapshot,
    FrozenBehaviorTimeline,
    TimelineRepositoryContract,
)
from boe.temporal.timeline_errors import (
    DuplicateFrameError,
    InvalidFrameError,
    TimelineError,
    TimelineFreezeError,
    TimelineRepositoryError,
)


class TestTemporalOntology(unittest.TestCase):
    def setUp(self) -> None:
        self.created = datetime(2026, 7, 20, 10, 0, tzinfo=timezone.utc)
        self.closed = datetime(2026, 7, 20, 10, 1, tzinfo=timezone.utc)
        self.snapshot = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snapshot_000001",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=self.created,
            source="market_feed",
            market_state={"raw_bar": "opaque"},
        )
        self.builder = ActiveObservationTimeline(
            schema_version="1.0.0",
            timeline_id="timeline_000001",
            candidate_id="candidate_000001",
            created_timestamp=self.created,
        )

    def _frame(self, frame_id: str, timestamp: datetime | None = None) -> BehaviorFrame:
        return BehaviorFrame(
            schema_version="1.0.0",
            frame_id=frame_id,
            timeline_id="timeline_000001",
            timestamp=timestamp or self.created,
            environment_snapshot_id=self.snapshot.snapshot_id,
            behavior_state="OBSERVED",
            behavior_strength="PRESENT",
            metadata={"source": "behavior_domain"},
        )

    def test_snapshot_frame_and_frozen_timeline_are_immutable(self) -> None:
        frame = self._frame("frame_000001")
        timeline = FrozenBehaviorTimeline(
            "1.0.0", "timeline_000001", "candidate_000001", self.created,
            self.closed, "WINDOW_CLOSED", (frame,), {"scope": "temporal"},
        )
        with self.assertRaises(FrozenInstanceError):
            self.snapshot.instrument = "GBPUSD"
        with self.assertRaises(TypeError):
            frame.metadata["source"] = "changed"
        with self.assertRaises(FrozenInstanceError):
            timeline.termination_reason = "changed"

    def test_builder_append_lifecycle_and_frame_ordering(self) -> None:
        first = self._frame("frame_000001", self.created)
        second = self._frame("frame_000002", self.closed)
        self.assertEqual(self.builder.timeline_status(), "ACTIVE")
        self.builder.append_frame(first)
        self.builder.append_frame(second)
        self.assertEqual(self.builder.frame_count(), 2)
        timeline = self.builder.freeze(self.closed, "WINDOW_CLOSED", {"scope": "temporal"})
        self.assertEqual(self.builder.timeline_status(), "FROZEN")
        self.assertEqual(timeline.frames, (first, second))
        self.assertEqual(timeline.schema_version, "1.0.0")

    def test_double_freeze_and_append_after_freeze_are_rejected(self) -> None:
        self.builder.append_frame(self._frame("frame_000001"))
        self.builder.freeze(self.closed, "WINDOW_CLOSED")
        with self.assertRaises(TimelineFreezeError):
            self.builder.freeze(self.closed, "WINDOW_CLOSED")
        with self.assertRaises(TimelineFreezeError):
            self.builder.append_frame(self._frame("frame_000002"))

    def test_duplicate_and_invalid_frames_are_rejected(self) -> None:
        frame = self._frame("frame_000001")
        self.builder.append_frame(frame)
        with self.assertRaises(DuplicateFrameError):
            self.builder.append_frame(frame)
        wrong_timeline = BehaviorFrame(
            "1.0.0", "frame_000002", "timeline_other", self.created,
            self.snapshot.snapshot_id, "OBSERVED", "PRESENT", {},
        )
        with self.assertRaises(InvalidFrameError):
            self.builder.append_frame(wrong_timeline)

    def test_repository_contract_and_error_hierarchy(self) -> None:
        with self.assertRaises(TypeError):
            TimelineRepositoryContract()
        self.assertTrue(issubclass(TimelineFreezeError, TimelineError))
        self.assertTrue(issubclass(TimelineRepositoryError, TimelineError))
        self.assertTrue(issubclass(InvalidFrameError, TimelineError))
        self.assertTrue(issubclass(DuplicateFrameError, TimelineError))

    def test_schema_version_and_invalid_frame_shape(self) -> None:
        self.assertEqual(self.snapshot.schema_version, "1.0.0")
        with self.assertRaises(TimelineError):
            BehaviorFrame(
                "invalid", "frame_bad", "timeline_000001", self.created,
                self.snapshot.snapshot_id, "OBSERVED", "PRESENT", {},
            )


if __name__ == "__main__":
    unittest.main()
