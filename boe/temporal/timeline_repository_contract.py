"""Abstract persistence boundary for immutable frozen behavior timelines."""

from abc import ABC, abstractmethod

from .frozen_behavior_timeline import FrozenBehaviorTimeline


class TimelineRepositoryContract(ABC):
    """Defines future persistent storage without providing an implementation."""

    @abstractmethod
    def save(self, timeline: FrozenBehaviorTimeline) -> None:
        """Persist one frozen timeline."""

    @abstractmethod
    def load(self, timeline_id: str) -> FrozenBehaviorTimeline:
        """Load one frozen timeline by its stable identity."""

    @abstractmethod
    def exists(self, timeline_id: str) -> bool:
        """Report whether a frozen timeline exists."""

    @abstractmethod
    def delete(self, timeline_id: str) -> None:
        """Delete one persisted frozen timeline."""
