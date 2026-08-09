"""Immutable canonical temporal aggregate for the Behavior Domain."""

from dataclasses import dataclass
from datetime import datetime
import re
from types import MappingProxyType
from typing import Mapping

from .behavior_frame import BehaviorFrame
from .timeline_errors import TimelineError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class FrozenBehaviorTimeline:
    """Immutable ordered behavioral timeline ready for evidence and future replay."""

    schema_version: str
    timeline_id: str
    candidate_id: str
    created_timestamp: datetime
    closed_timestamp: datetime
    termination_reason: str
    frames: tuple[BehaviorFrame, ...]
    timeline_metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        """Validate immutable aggregate shape without interpreting its frames."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise TimelineError("FrozenBehaviorTimeline schema_version must be semantic versioning.")
        if not all(isinstance(value, str) and value for value in (
            self.timeline_id, self.candidate_id, self.termination_reason,
        )):
            raise TimelineError("FrozenBehaviorTimeline identity and termination fields are required.")
        if not isinstance(self.created_timestamp, datetime) or not isinstance(self.closed_timestamp, datetime):
            raise TimelineError("FrozenBehaviorTimeline timestamps must be datetimes.")
        if not isinstance(self.frames, tuple) or not all(isinstance(frame, BehaviorFrame) for frame in self.frames):
            raise TimelineError("FrozenBehaviorTimeline frames must be a tuple of BehaviorFrame values.")
        if any(frame.timeline_id != self.timeline_id for frame in self.frames):
            raise TimelineError("Every BehaviorFrame must belong to the FrozenBehaviorTimeline.")
        if not isinstance(self.timeline_metadata, Mapping):
            raise TimelineError("FrozenBehaviorTimeline timeline_metadata must be an opaque mapping.")
        object.__setattr__(self, "timeline_metadata", MappingProxyType(dict(self.timeline_metadata)))
