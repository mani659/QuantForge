"""Abstract boundary for the Replay Engine."""

from abc import ABC, abstractmethod

from boe.replay.replay_cursor import ReplayCursor
from boe.replay.replay_result import ReplayResult


class ReplayEngineContract(ABC):
    """Deterministic scientific playback engine."""

    @abstractmethod
    def load(self, timeline_id: str) -> None:
        """Load a frozen timeline by ID."""

    @abstractmethod
    def start(self) -> None:
        """Initialize playback position."""

    @abstractmethod
    def step(self) -> ReplayCursor:
        """Advance replay by one frame."""

    @abstractmethod
    def restart(self) -> None:
        """Reset replay position to the beginning."""

    @abstractmethod
    def replay_all(self) -> tuple[ReplayCursor, ...]:
        """Replay all frames from current position to completion."""

    @abstractmethod
    def finish(self) -> ReplayResult:
        """Conclude replay and produce final result."""
