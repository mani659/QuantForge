from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any

from boe.risk.assessment import RiskAssessment, AssessmentStatus
from boe.risk.risk_errors import (
    PositionSizingError,
    InvalidRiskAssessment
)

@dataclass(frozen=True)
class PositionSizingResult:
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    risk_units: float
    exposure_fraction: float
    position_size_multiplier: float
    metadata: MappingProxyType[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if not self.candidate_id:
            raise PositionSizingError("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise PositionSizingError("timeline_id cannot be empty.")
        if not self.observation_id:
            raise PositionSizingError("observation_id cannot be empty.")
        if not self.schema_version:
            raise PositionSizingError("schema_version cannot be empty.")
        if not isinstance(self.risk_units, (int, float)):
            raise PositionSizingError("risk_units must be numeric.")
        if not isinstance(self.exposure_fraction, (int, float)):
            raise PositionSizingError("exposure_fraction must be numeric.")
        if not isinstance(self.position_size_multiplier, (int, float)):
            raise PositionSizingError("position_size_multiplier must be numeric.")
        if not isinstance(self.timestamp, datetime):
            raise PositionSizingError("timestamp must be a datetime.")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.risk_units,
            self.exposure_fraction,
            self.position_size_multiplier,
            frozenset(self.metadata.items()),
            self.timestamp
        ))

@dataclass(frozen=True)
class PositionSizerConfig:
    base_risk_fraction: float = 0.01
    max_position_multiplier: float = 1.0

class PositionSizerContract(ABC):
    @property
    @abstractmethod
    def sizer_name(self) -> str:
        pass
        
    @abstractmethod
    def size_position(self, assessment: RiskAssessment, timestamp: datetime) -> PositionSizingResult:
        pass

class DefaultPositionSizer(PositionSizerContract):
    def __init__(self, config: PositionSizerConfig = PositionSizerConfig()):
        self._config = config

    @property
    def sizer_name(self) -> str:
        return "DefaultPositionSizer_v1.0"
        
    def size_position(self, assessment: RiskAssessment, timestamp: datetime) -> PositionSizingResult:
        if not assessment:
            raise InvalidRiskAssessment("RiskAssessment is required.")
            
        if assessment.status == AssessmentStatus.APPROVED:
            exposure_fraction = self._config.base_risk_fraction
            multiplier = 1.0
            risk_units = 1.0
        elif assessment.status == AssessmentStatus.REDUCED_EXPOSURE:
            exposure_fraction = self._config.base_risk_fraction * 0.5
            multiplier = 0.5
            risk_units = 0.5
        else:
            exposure_fraction = 0.0
            multiplier = 0.0
            risk_units = 0.0
            
        multiplier = min(multiplier, self._config.max_position_multiplier)

        return PositionSizingResult(
            candidate_id=assessment.candidate_id,
            timeline_id=assessment.timeline_id,
            observation_id=assessment.observation_id,
            schema_version="1.0",
            risk_units=risk_units,
            exposure_fraction=exposure_fraction,
            position_size_multiplier=multiplier,
            metadata=MappingProxyType({"sizer": self.sizer_name}),
            timestamp=timestamp
        )
