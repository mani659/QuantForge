"""The sole mutable builder in the temporal-domain ontology."""

from datetime import datetime

from .behavior_frame import BehaviorFrame
from .frozen_behavior_timeline import FrozenBehaviorTimeline
from .timeline_errors import DuplicateFrameError, InvalidFrameError, TimelineFreezeError


class ActiveObservationTimeline:
    """Collect ordered frames and freeze them into the immutable canonical timeline."""

    def __init__(
        self,
        schema_version: str,
        timeline_id: str,
        candidate_id: str,
        created_timestamp: datetime,
    ) -> None:
        self._schema_version = schema_version
        self._timeline_id = timeline_id
        self._candidate_id = candidate_id
        self._created_timestamp = created_timestamp
        self._frames: list[BehaviorFrame] = []
        self._frozen_timeline: FrozenBehaviorTimeline | None = None

    def append_frame(self, frame: BehaviorFrame) -> None:
        """Append one compatible frame, preserving caller-provided ordering."""
        if self._frozen_timeline is not None:
            raise TimelineFreezeError("Cannot append a frame after timeline freeze.")
        if not isinstance(frame, BehaviorFrame) or frame.timeline_id != self._timeline_id:
            raise InvalidFrameError("Frame must be a BehaviorFrame for this timeline.")
        if any(existing.frame_id == frame.frame_id for existing in self._frames):
            raise DuplicateFrameError(f"Duplicate frame: {frame.frame_id}")
        self._frames.append(frame)

    def frame_count(self) -> int:
        """Return the number of frames appended in caller-provided order."""
        return len(self._frames)

    def timeline_status(self) -> str:
        """Return the lifecycle state without applying any observation policy."""
        return "FROZEN" if self._frozen_timeline is not None else "ACTIVE"

    def freeze(
        self,
        closed_timestamp: datetime,
        termination_reason: str,
        timeline_metadata: dict[str, object] | None = None,
    ) -> FrozenBehaviorTimeline:
        """Create the one immutable aggregate permitted by this active builder."""
        if self._frozen_timeline is not None:
            raise TimelineFreezeError("ActiveObservationTimeline may be frozen only once.")
        self._frozen_timeline = FrozenBehaviorTimeline(
            schema_version=self._schema_version,
            timeline_id=self._timeline_id,
            candidate_id=self._candidate_id,
            created_timestamp=self._created_timestamp,
            closed_timestamp=closed_timestamp,
            termination_reason=termination_reason,
            frames=tuple(self._frames),
            timeline_metadata=timeline_metadata or {},
        )
        return self._frozen_timeline
