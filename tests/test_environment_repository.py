"""Deterministic tests for the Environment Repository."""

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.temporal.environment_repository_contract import EnvironmentRepositoryContract
from boe.temporal.environment_repository import InMemoryEnvironmentRepository
from boe.temporal.timeline_errors import TimelineError


class TestEnvironmentRepository(unittest.TestCase):
    """Deterministic tests for in-memory environment repository."""

    def setUp(self) -> None:
        self.repo = InMemoryEnvironmentRepository()
        self.snapshot1 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_001",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=datetime(2026, 7, 28, 12, 0, tzinfo=timezone.utc),
            source="test",
            market_state={"price": 1.10}
        )
        self.snapshot2 = EnvironmentSnapshot(
            schema_version="1.0.0",
            snapshot_id="snap_002",
            instrument="EURUSD",
            timeframe="M1",
            timestamp=datetime(2026, 7, 28, 12, 1, tzinfo=timezone.utc),
            source="test",
            market_state={"price": 1.11}
        )

    def test_contract_compliance(self) -> None:
        self.assertIsInstance(self.repo, EnvironmentRepositoryContract)

    def test_save_and_load(self) -> None:
        self.repo.save(self.snapshot1)
        loaded = self.repo.load("snap_001")
        self.assertIs(loaded, self.snapshot1)

    def test_save_duplicate_raises(self) -> None:
        self.repo.save(self.snapshot1)
        with self.assertRaises(TimelineError):
            self.repo.save(self.snapshot1)

    def test_save_invalid_type_raises(self) -> None:
        with self.assertRaises(TimelineError):
            self.repo.save("not_a_snapshot") # type: ignore

    def test_load_not_found_raises(self) -> None:
        with self.assertRaises(TimelineError):
            self.repo.load("nonexistent")

    def test_exists(self) -> None:
        self.assertFalse(self.repo.exists("snap_001"))
        self.repo.save(self.snapshot1)
        self.assertTrue(self.repo.exists("snap_001"))

    def test_delete(self) -> None:
        self.repo.save(self.snapshot1)
        self.repo.delete("snap_001")
        self.assertFalse(self.repo.exists("snap_001"))

    def test_delete_not_found_raises(self) -> None:
        with self.assertRaises(TimelineError):
            self.repo.delete("nonexistent")

    def test_list(self) -> None:
        self.repo.save(self.snapshot1)
        self.repo.save(self.snapshot2)
        snapshots = self.repo.list()
        self.assertEqual(len(snapshots), 2)
        self.assertIs(snapshots[0], self.snapshot1)
        self.assertIs(snapshots[1], self.snapshot2)


if __name__ == "__main__":
    unittest.main()
