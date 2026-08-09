"""Deterministic tests for the Timeline Repository."""

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline
from boe.temporal.timeline_repository_contract import TimelineRepositoryContract
from boe.temporal.timeline_repository import InMemoryTimelineRepository
from boe.temporal.timeline_errors import TimelineError


class TestTimelineRepository(unittest.TestCase):
    """Deterministic tests for in-memory timeline repository."""

    def setUp(self) -> None:
        self.repo = InMemoryTimelineRepository()
        
        # Creating simple timelines for testing storage
        self.timeline1 = FrozenBehaviorTimeline(
            timeline_id="tl_001",
            candidate_id="cand_1",
            schema_version="1.0.0",
            created_timestamp=datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc),
            closed_timestamp=datetime(2026, 7, 28, 12, 1, tzinfo=timezone.utc),
            termination_reason="WINDOW_COMPLETE",
            frames=(),
            timeline_metadata={}
        )
        self.timeline2 = FrozenBehaviorTimeline(
            timeline_id="tl_002",
            candidate_id="cand_1",
            schema_version="1.0.0",
            created_timestamp=datetime(2026, 7, 28, 12, 1, tzinfo=timezone.utc),
            closed_timestamp=datetime(2026, 7, 28, 12, 2, tzinfo=timezone.utc),
            termination_reason="WINDOW_COMPLETE",
            frames=(),
            timeline_metadata={}
        )
        self.timeline3 = FrozenBehaviorTimeline(
            timeline_id="tl_003",
            candidate_id="cand_2",
            schema_version="1.0.0",
            created_timestamp=datetime(2026, 7, 28, 12, 2, tzinfo=timezone.utc),
            closed_timestamp=datetime(2026, 7, 28, 12, 3, tzinfo=timezone.utc),
            termination_reason="WINDOW_COMPLETE",
            frames=(),
            timeline_metadata={}
        )

    def test_contract_compliance(self) -> None:
        self.assertIsInstance(self.repo, TimelineRepositoryContract)

    def test_save_and_load(self) -> None:
        self.repo.save(self.timeline1)
        loaded = self.repo.load("tl_001")
        self.assertIs(loaded, self.timeline1)

    def test_save_duplicate_raises(self) -> None:
        self.repo.save(self.timeline1)
        with self.assertRaises(TimelineError):
            self.repo.save(self.timeline1)

    def test_save_invalid_type_raises(self) -> None:
        with self.assertRaises(TimelineError):
            self.repo.save("not_a_timeline") # type: ignore

    def test_load_not_found_raises(self) -> None:
        with self.assertRaises(TimelineError):
            self.repo.load("nonexistent")

    def test_load_by_candidate(self) -> None:
        self.repo.save(self.timeline1)
        self.repo.save(self.timeline2)
        self.repo.save(self.timeline3)
        
        cand1_timelines = self.repo.load_by_candidate("cand_1")
        self.assertEqual(len(cand1_timelines), 2)
        self.assertIn(self.timeline1, cand1_timelines)
        self.assertIn(self.timeline2, cand1_timelines)
        
        cand2_timelines = self.repo.load_by_candidate("cand_2")
        self.assertEqual(len(cand2_timelines), 1)
        self.assertIn(self.timeline3, cand2_timelines)
        
        cand3_timelines = self.repo.load_by_candidate("cand_3")
        self.assertEqual(len(cand3_timelines), 0)

    def test_exists(self) -> None:
        self.assertFalse(self.repo.exists("tl_001"))
        self.repo.save(self.timeline1)
        self.assertTrue(self.repo.exists("tl_001"))

    def test_delete(self) -> None:
        self.repo.save(self.timeline1)
        self.repo.delete("tl_001")
        self.assertFalse(self.repo.exists("tl_001"))

    def test_delete_not_found_raises(self) -> None:
        with self.assertRaises(TimelineError):
            self.repo.delete("nonexistent")

    def test_list(self) -> None:
        self.repo.save(self.timeline1)
        self.repo.save(self.timeline2)
        timelines = self.repo.list()
        self.assertEqual(len(timelines), 2)
        self.assertIs(timelines[0], self.timeline1)
        self.assertIs(timelines[1], self.timeline2)


if __name__ == "__main__":
    unittest.main()
