from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any

from boe.risk.position_sizer import PositionSizingResult
from boe.risk.risk_errors import (
    InvalidPositionSpecification,
    InvalidSizingOutput,
    PositionSpecificationConstructionError
)

@dataclass(frozen=True)
class PositionSpecification:
    """
    Immutable, broker-independent specification for a future position.
    Generated exclusively from the PositionSizer layer.
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    position_size_multiplier: float
    exposure_fraction: float
    risk_units: float
    metadata: MappingProxyType[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if not self.candidate_id:
            raise InvalidPositionSpecification("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise InvalidPositionSpecification("timeline_id cannot be empty.")
        if not self.observation_id:
            raise InvalidPositionSpecification("observation_id cannot be empty.")
        if not self.schema_version:
            raise InvalidPositionSpecification("schema_version cannot be empty.")
        if not isinstance(self.position_size_multiplier, (int, float)):
            raise InvalidPositionSpecification("position_size_multiplier must be numeric.")
        if not isinstance(self.exposure_fraction, (int, float)):
            raise InvalidPositionSpecification("exposure_fraction must be numeric.")
        if not isinstance(self.risk_units, (int, float)):
            raise InvalidPositionSpecification("risk_units must be numeric.")
        if not isinstance(self.timestamp, datetime):
            raise InvalidPositionSpecification("timestamp must be a datetime.")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.position_size_multiplier,
            self.exposure_fraction,
            self.risk_units,
            frozenset(self.metadata.items()),
            self.timestamp
        ))

    @classmethod
    def from_sizing_result(cls, sizing_result: PositionSizingResult, timestamp: datetime) -> 'PositionSpecification':
        if not sizing_result:
            raise InvalidSizingOutput("PositionSizingResult is required to build a PositionSpecification.")

        try:
            return cls(
                candidate_id=sizing_result.candidate_id,
                timeline_id=sizing_result.timeline_id,
                observation_id=sizing_result.observation_id,
                schema_version="1.0",
                position_size_multiplier=sizing_result.position_size_multiplier,
                exposure_fraction=sizing_result.exposure_fraction,
                risk_units=sizing_result.risk_units,
                metadata=MappingProxyType({"source_sizer": sizing_result.metadata.get("sizer", "Unknown")}),
                timestamp=timestamp
            )
        except Exception as e:
            raise PositionSpecificationConstructionError(f"Failed to construct PositionSpecification: {e}")
