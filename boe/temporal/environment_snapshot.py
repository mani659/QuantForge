"""Immutable, opaque Market Reality input for the temporal domain."""

from dataclasses import dataclass
from datetime import datetime
import re
from types import MappingProxyType
from typing import Mapping

from .timeline_errors import TimelineError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class EnvironmentSnapshot:
    """Immutable supplied market state without detector or indicator interpretation."""

    schema_version: str
    snapshot_id: str
    instrument: str
    timeframe: str
    timestamp: datetime
    source: str
    market_state: Mapping[str, object]

    def __post_init__(self) -> None:
        """Validate public provenance and preserve the supplied opaque payload."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise TimelineError("EnvironmentSnapshot schema_version must be semantic versioning.")
        if not all(isinstance(value, str) and value for value in (
            self.snapshot_id, self.instrument, self.timeframe, self.source,
        )):
            raise TimelineError("EnvironmentSnapshot identity and provenance fields are required.")
        if not isinstance(self.timestamp, datetime):
            raise TimelineError("EnvironmentSnapshot timestamp must be a datetime.")
        if not isinstance(self.market_state, Mapping):
            raise TimelineError("EnvironmentSnapshot market_state must be an opaque mapping.")
        object.__setattr__(self, "market_state", MappingProxyType(dict(self.market_state)))
