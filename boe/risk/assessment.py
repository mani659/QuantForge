from enum import Enum, auto
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any

from boe.risk.policy import RiskPolicyEvaluation, RiskPolicyAction
from boe.risk.risk_errors import (
    InvalidRiskAssessment,
    MissingRiskDecision,
    InvalidAssessmentState
)

class AssessmentStatus(Enum):
    APPROVED = auto()
    REJECTED = auto()
    REDUCED_EXPOSURE = auto()
    MANUAL_REVIEW = auto()

@dataclass(frozen=True)
class RiskAssessment:
    """
    Immutable output recording the final capital allocation outcome from the Risk Policy layer.
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    status: AssessmentStatus
    rationale: str
    metadata: MappingProxyType[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if not self.candidate_id:
            raise InvalidRiskAssessment("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise InvalidRiskAssessment("timeline_id cannot be empty.")
        if not self.observation_id:
            raise InvalidRiskAssessment("observation_id cannot be empty.")
        if not self.schema_version:
            raise InvalidRiskAssessment("schema_version cannot be empty.")
        if not isinstance(self.status, AssessmentStatus):
            raise InvalidAssessmentState("status must be an AssessmentStatus enum.")
        if not self.rationale:
            raise InvalidRiskAssessment("rationale cannot be empty.")
        if not isinstance(self.timestamp, datetime):
            raise InvalidRiskAssessment("timestamp must be a datetime.")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.status,
            self.rationale,
            frozenset(self.metadata.items()),
            self.timestamp
        ))

    @classmethod
    def from_policy_evaluation(cls, evaluation: RiskPolicyEvaluation, timestamp: datetime) -> 'RiskAssessment':
        if not evaluation:
            raise MissingRiskDecision("RiskPolicyEvaluation is required to create a RiskAssessment.")

        status_map = {
            RiskPolicyAction.APPROVE: AssessmentStatus.APPROVED,
            RiskPolicyAction.REJECT: AssessmentStatus.REJECTED,
            RiskPolicyAction.REDUCE_EXPOSURE: AssessmentStatus.REDUCED_EXPOSURE,
            RiskPolicyAction.REQUIRE_REVIEW: AssessmentStatus.MANUAL_REVIEW
        }

        if evaluation.action not in status_map:
            raise InvalidAssessmentState(f"Unsupported policy action: {evaluation.action}")

        return cls(
            candidate_id=evaluation.candidate_id,
            timeline_id=evaluation.timeline_id,
            observation_id=evaluation.observation_id,
            schema_version="1.0",
            status=status_map[evaluation.action],
            rationale=evaluation.rationale,
            metadata=MappingProxyType({"source_policy": evaluation.metadata.get("policy", "Unknown")}),
            timestamp=timestamp
        )
