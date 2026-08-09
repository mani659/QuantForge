"""Immutable single temporal behavioral fact."""

from dataclasses import dataclass
from datetime import datetime
import re
from types import MappingProxyType
from typing import Mapping

from .timeline_errors import TimelineError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class BehaviorFrame:
    """One categorical behavioral observation linked to an environment snapshot.

    ``behavior_strength`` is an architectural category supplied by the caller,
    never a numerical indicator, threshold, or internal detector score.
    """

    schema_version: str
    frame_id: str
    timeline_id: str
    timestamp: datetime
    environment_snapshot_id: str
    behavior_state: str
    behavior_strength: str
    metadata: Mapping[str, object]

    def __post_init__(self) -> None:
        """Validate contract identity and make the opaque metadata immutable."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise TimelineError("BehaviorFrame schema_version must be semantic versioning.")
        if not all(isinstance(value, str) and value for value in (
            self.frame_id, self.timeline_id, self.environment_snapshot_id,
            self.behavior_state, self.behavior_strength,
        )):
            raise TimelineError("BehaviorFrame identity and categorical fields are required.")
        if not isinstance(self.timestamp, datetime):
            raise TimelineError("BehaviorFrame timestamp must be a datetime.")
        if not isinstance(self.metadata, Mapping):
            raise TimelineError("BehaviorFrame metadata must be an opaque mapping.")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
