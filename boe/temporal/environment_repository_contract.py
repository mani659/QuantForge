"""Abstract boundary for persistent storage of environment snapshots."""

from abc import ABC, abstractmethod

from .environment_snapshot import EnvironmentSnapshot


class EnvironmentRepositoryContract(ABC):
    """Immutable repository abstraction for EnvironmentSnapshot persistence."""

    @abstractmethod
    def save(self, snapshot: EnvironmentSnapshot) -> None:
        """Persist an environment snapshot."""

    @abstractmethod
    def load(self, snapshot_id: str) -> EnvironmentSnapshot:
        """Load an environment snapshot by its unique identifier."""

    @abstractmethod
    def exists(self, snapshot_id: str) -> bool:
        """Check if an environment snapshot exists."""

    @abstractmethod
    def delete(self, snapshot_id: str) -> None:
        """Delete an environment snapshot by its unique identifier."""

    @abstractmethod
    def list(self) -> tuple[EnvironmentSnapshot, ...]:
        """List all stored environment snapshots."""
