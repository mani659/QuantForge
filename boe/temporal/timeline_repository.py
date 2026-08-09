"""Deterministic in-memory implementation of the Timeline Repository contract."""

from .frozen_behavior_timeline import FrozenBehaviorTimeline
from .timeline_repository_contract import TimelineRepositoryContract
from .timeline_errors import TimelineError


class InMemoryTimelineRepository(TimelineRepositoryContract):
    """Append-only in-memory repository for FrozenBehaviorTimelines."""

    def __init__(self) -> None:
        self._timelines: dict[str, FrozenBehaviorTimeline] = {}

    def save(self, timeline: FrozenBehaviorTimeline) -> None:
        """Persist one immutable timeline. Prevents duplicates."""
        if not isinstance(timeline, FrozenBehaviorTimeline):
            raise TimelineError("Repository accepts only FrozenBehaviorTimeline instances.")
        if timeline.timeline_id in self._timelines:
            raise TimelineError(f"Timeline already exists: {timeline.timeline_id}")
        self._timelines[timeline.timeline_id] = timeline

    def load(self, timeline_id: str) -> FrozenBehaviorTimeline:
        """Load one timeline by its ID or raise an error if not found."""
        if timeline_id not in self._timelines:
            raise TimelineError(f"Timeline not found: {timeline_id}")
        return self._timelines[timeline_id]

    def load_by_candidate(self, candidate_id: str) -> tuple[FrozenBehaviorTimeline, ...]:
        """Load all timelines associated with a specific candidate."""
        return tuple(t for t in self._timelines.values() if t.candidate_id == candidate_id)

    def exists(self, timeline_id: str) -> bool:
        """Check if timeline exists."""
        return timeline_id in self._timelines

    def delete(self, timeline_id: str) -> None:
        """Delete a timeline or raise an error if not found."""
        if timeline_id not in self._timelines:
            raise TimelineError(f"Timeline not found: {timeline_id}")
        del self._timelines[timeline_id]

    def list(self) -> tuple[FrozenBehaviorTimeline, ...]:
        """Return all timelines in insertion order."""
        return tuple(self._timelines.values())
