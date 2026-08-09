"""Deterministic in-memory implementation of the Environment Repository contract."""

from .environment_repository_contract import EnvironmentRepositoryContract
from .environment_snapshot import EnvironmentSnapshot
from .timeline_errors import TimelineError


class InMemoryEnvironmentRepository(EnvironmentRepositoryContract):
    """Append-only in-memory repository for EnvironmentSnapshots."""

    def __init__(self) -> None:
        self._snapshots: dict[str, EnvironmentSnapshot] = {}

    def save(self, snapshot: EnvironmentSnapshot) -> None:
        """Persist one immutable snapshot. Prevents duplicates."""
        if not isinstance(snapshot, EnvironmentSnapshot):
            raise TimelineError("Repository accepts only EnvironmentSnapshot instances.")
        if snapshot.snapshot_id in self._snapshots:
            raise TimelineError(f"Snapshot already exists: {snapshot.snapshot_id}")
        self._snapshots[snapshot.snapshot_id] = snapshot

    def load(self, snapshot_id: str) -> EnvironmentSnapshot:
        """Load one snapshot or raise an error if not found."""
        if snapshot_id not in self._snapshots:
            raise TimelineError(f"Snapshot not found: {snapshot_id}")
        return self._snapshots[snapshot_id]

    def exists(self, snapshot_id: str) -> bool:
        """Check if snapshot exists."""
        return snapshot_id in self._snapshots

    def delete(self, snapshot_id: str) -> None:
        """Delete a snapshot or raise an error if not found."""
        if snapshot_id not in self._snapshots:
            raise TimelineError(f"Snapshot not found: {snapshot_id}")
        del self._snapshots[snapshot_id]

    def list(self) -> tuple[EnvironmentSnapshot, ...]:
        """Return all snapshots in insertion order."""
        return tuple(self._snapshots.values())
