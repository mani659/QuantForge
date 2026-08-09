from enum import Enum, auto
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any

from boe.decision.decision import Decision, DecisionAction
from boe.risk.models import RiskProfile
from boe.risk.risk_errors import (
    MissingDecision,
    MissingRiskModel,
    RiskPolicyConstructionError
)

class RiskPolicyAction(Enum):
    APPROVE = auto()
    REJECT = auto()
    REDUCE_EXPOSURE = auto()
    REQUIRE_REVIEW = auto()

@dataclass(frozen=True)
class RiskPolicyEvaluation:
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    action: RiskPolicyAction
    rationale: str
    metadata: MappingProxyType[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if not self.candidate_id:
            raise RiskPolicyConstructionError("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise RiskPolicyConstructionError("timeline_id cannot be empty.")
        if not self.observation_id:
            raise RiskPolicyConstructionError("observation_id cannot be empty.")
        if not self.schema_version:
            raise RiskPolicyConstructionError("schema_version cannot be empty.")
        if not isinstance(self.action, RiskPolicyAction):
            raise RiskPolicyConstructionError("action must be a RiskPolicyAction enum.")
        if not self.rationale:
            raise RiskPolicyConstructionError("rationale cannot be empty.")
        if not isinstance(self.timestamp, datetime):
            raise RiskPolicyConstructionError("timestamp must be a datetime.")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.action,
            self.rationale,
            frozenset(self.metadata.items()),
            self.timestamp
        ))

@dataclass(frozen=True)
class RiskPolicyConfig:
    strict_mode: bool = True
    require_independent_interaction: bool = False

class RiskPolicyContract(ABC):
    @property
    @abstractmethod
    def policy_name(self) -> str:
        pass
        
    @abstractmethod
    def evaluate(self, decision: Decision, profile: RiskProfile, timestamp: datetime) -> RiskPolicyEvaluation:
        pass

class DefaultRiskPolicy(RiskPolicyContract):
    def __init__(self, config: RiskPolicyConfig = RiskPolicyConfig()):
        self._config = config

    @property
    def policy_name(self) -> str:
        return "DefaultRiskPolicy_v1.0"
        
    def evaluate(self, decision: Decision, profile: RiskProfile, timestamp: datetime) -> RiskPolicyEvaluation:
        if not decision:
            raise MissingDecision("Decision is required.")
        if not profile:
            raise MissingRiskModel("RiskProfile is required.")
            
        if decision.candidate_id != profile.candidate_id:
            raise RiskPolicyConstructionError("Decision and RiskProfile candidate_id mismatch.")
            
        # Default Logic: Evaluate Decision and Exposure Category
        try:
            interaction_desc = profile.get_descriptor("Portfolio Interaction Flag")
            interaction_val = interaction_desc.values[0]
        except Exception:
            interaction_val = "Unknown"
            
        if self._config.require_independent_interaction and interaction_val != "Independent":
            action = RiskPolicyAction.REJECT
            rationale = "Rejected: Portfolio Interaction is not Independent."
        elif decision.action == DecisionAction.ACCEPT:
            action = RiskPolicyAction.APPROVE
            rationale = "Approved: Standard execution parameters."
        elif decision.action == DecisionAction.REQUIRE_MORE_EVIDENCE:
            action = RiskPolicyAction.REDUCE_EXPOSURE
            rationale = "Reduced: More evidence required, deferring to partial exposure."
        elif decision.action == DecisionAction.DEFER:
            action = RiskPolicyAction.REQUIRE_REVIEW
            rationale = "Review: Decision deferred, awaiting manual oversight."
        else:
            action = RiskPolicyAction.REJECT
            rationale = "Rejected: Decision action precludes exposure."
            
        return RiskPolicyEvaluation(
            candidate_id=decision.candidate_id,
            timeline_id=decision.timeline_id,
            observation_id=decision.observation_id,
            schema_version="1.0",
            action=action,
            rationale=rationale,
            metadata=MappingProxyType({"policy": self.policy_name, "strict": self._config.strict_mode}),
            timestamp=timestamp
        )
