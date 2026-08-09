from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import MappingProxyType
from typing import Tuple, Any
from datetime import datetime

from boe.decision.decision import Decision, DecisionAction
from boe.risk.risk_errors import (
    InvalidRiskModel,
    MissingDecision,
    UnsupportedDecision,
    RiskModelConstructionError
)

@dataclass(frozen=True)
class RiskDescriptor:
    """Immutable tuple mapping string names to values, describing risk characteristics."""
    name: str
    values: Tuple[str, ...]

    def __post_init__(self):
        if not self.name:
            raise RiskModelConstructionError("RiskDescriptor name cannot be empty.")
        if not isinstance(self.values, tuple):
            raise RiskModelConstructionError("RiskDescriptor values must be a tuple.")

@dataclass(frozen=True)
class RiskProfile:
    """
    Immutable description of capital exposure based on a Decision.
    Does NOT contain monetary calculations (no lots, leverage, SL/TP).
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    descriptors: Tuple[RiskDescriptor, ...]
    metadata: MappingProxyType[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if not self.candidate_id:
            raise RiskModelConstructionError("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise RiskModelConstructionError("timeline_id cannot be empty.")
        if not self.observation_id:
            raise RiskModelConstructionError("observation_id cannot be empty.")
        if not self.schema_version:
            raise RiskModelConstructionError("schema_version cannot be empty.")
        if not isinstance(self.descriptors, tuple):
            raise RiskModelConstructionError("descriptors must be a tuple.")
        if not isinstance(self.timestamp, datetime):
            raise RiskModelConstructionError("timestamp must be a datetime.")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.descriptors,
            frozenset(self.metadata.items()),
            self.timestamp
        ))

    def get_descriptor(self, name: str) -> RiskDescriptor:
        for desc in self.descriptors:
            if desc.name == name:
                return desc
        raise InvalidRiskModel(f"Descriptor '{name}' not found.")

class RiskModelContract(ABC):
    """
    Abstract contract for a Risk Model.
    Transforms Decision -> RiskProfile.
    """
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
        
    @abstractmethod
    def evaluate(self, decision: Decision, timestamp: datetime) -> RiskProfile:
        pass

class DefaultRiskModel(RiskModelContract):
    """
    Default Risk Model for v1.0.
    Describes risk exposure categories based on the Decision.
    """
    
    @property
    def model_name(self) -> str:
        return "DefaultRiskModel_v1.0"
        
    def evaluate(self, decision: Decision, timestamp: datetime) -> RiskProfile:
        if not decision:
            raise MissingDecision("Decision is required to evaluate risk.")
            
        if decision.action == DecisionAction.ACCEPT:
            risk_category = "Standard Exposure"
            exposure_class = "Active"
            max_exposure = "Normal"
            portfolio_interaction = "Independent"
            position_risk = "High"
        elif decision.action == DecisionAction.REQUIRE_MORE_EVIDENCE:
            risk_category = "Reduced Exposure"
            exposure_class = "Deferred"
            max_exposure = "Minimal"
            portfolio_interaction = "Dependent"
            position_risk = "Low"
        elif decision.action == DecisionAction.REJECT:
            risk_category = "No Exposure"
            exposure_class = "Inactive"
            max_exposure = "Zero"
            portfolio_interaction = "Isolated"
            position_risk = "Zero"
        elif decision.action == DecisionAction.DEFER:
            risk_category = "Pending Exposure"
            exposure_class = "Deferred"
            max_exposure = "Zero"
            portfolio_interaction = "Dependent"
            position_risk = "Pending"
        else:
            raise UnsupportedDecision(f"Unsupported decision action: {decision.action}")
            
        desc_cat = RiskDescriptor("Risk Category", (risk_category,))
        desc_class = RiskDescriptor("Exposure Class", (exposure_class,))
        desc_max = RiskDescriptor("Maximum Exposure Class", (max_exposure,))
        desc_interaction = RiskDescriptor("Portfolio Interaction Flag", (portfolio_interaction,))
        desc_pos = RiskDescriptor("Position Risk Profile", (position_risk,))
        
        return RiskProfile(
            candidate_id=decision.candidate_id,
            timeline_id=decision.timeline_id,
            observation_id=decision.observation_id,
            schema_version="1.0",
            descriptors=(desc_cat, desc_class, desc_max, desc_interaction, desc_pos),
            metadata=MappingProxyType({"model": self.model_name}),
            timestamp=timestamp
        )
