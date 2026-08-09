"""Immutable detector input contract for the Behavioral Observation Engine."""

from dataclasses import dataclass
from datetime import datetime
import re
from types import MappingProxyType
from typing import Mapping

from .detector_errors import DataIntegrityError, VersionMismatchError


SEMANTIC_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class ObservationEnvironment:
    """Stable market context supplied to a behavior detector.

    ``market_snapshot`` deliberately contains only raw, opaque market records.
    Detectors may interpret it internally, but derived calculations and indicator
    values are not part of this contract.
    """

    schema_version: str
    environment_id: str
    instrument: str
    timeframe: str
    observed_at: datetime
    market_snapshot: tuple[Mapping[str, object], ...]

    def __post_init__(self) -> None:
        """Validate contract fields and protect supplied raw records from mutation."""
        if not SEMANTIC_VERSION_PATTERN.fullmatch(self.schema_version):
            raise VersionMismatchError("ObservationEnvironment schema_version must be semantic versioning.")
        if not self.environment_id:
            raise DataIntegrityError("ObservationEnvironment environment_id is required.")
        if not self.instrument:
            raise DataIntegrityError("ObservationEnvironment instrument is required.")
        if not self.timeframe:
            raise DataIntegrityError("ObservationEnvironment timeframe is required.")
        if not isinstance(self.observed_at, datetime):
            raise DataIntegrityError("ObservationEnvironment observed_at must be a datetime.")
        if not isinstance(self.market_snapshot, tuple) or not self.market_snapshot:
            raise DataIntegrityError("ObservationEnvironment market_snapshot must be a non-empty tuple.")
        if not all(isinstance(record, Mapping) for record in self.market_snapshot):
            raise DataIntegrityError("ObservationEnvironment market_snapshot records must be mappings.")
        object.__setattr__(
            self,
            "market_snapshot",
            tuple(MappingProxyType(dict(record)) for record in self.market_snapshot),
        )
