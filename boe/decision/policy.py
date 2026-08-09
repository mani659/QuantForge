from abc import ABC, abstractmethod
from types import MappingProxyType
from datetime import datetime

from boe.interpretation.interpretation import Interpretation
from boe.decision.decision import Decision, DecisionAction
from boe.decision.decision_errors import MissingInterpretation, UnsupportedInterpretation

class DecisionPolicyContract(ABC):
    """
    Abstract contract for a Decision Policy.
    Policies transform Interpretation -> Decision.
    They perform NO risk mapping, position sizing, or execution.
    """
    
    @property
    @abstractmethod
    def policy_name(self) -> str:
        pass
        
    @abstractmethod
    def evaluate(self, interpretation: Interpretation, timestamp: datetime) -> Decision:
        """
        Converts an Interpretation into a Decision.
        """
        pass

class DefaultDecisionPolicy(DecisionPolicyContract):
    """
    Default policy for v1.0.
    Accepts Mean Reversion Candidates and Trend Continuation Candidates.
    Rejects others. Requires more evidence for Inconclusive.
    """
    
    @property
    def policy_name(self) -> str:
        return "DefaultDecisionPolicy_v1.0"
        
    def evaluate(self, interpretation: Interpretation, timestamp: datetime) -> Decision:
        if not interpretation:
            raise MissingInterpretation("Interpretation is required for Decision Policy.")
            
        conclusion = interpretation.conclusion
        
        if conclusion in ("Mean Reversion Candidate", "Trend Continuation Candidate"):
            action = DecisionAction.ACCEPT
            rationale = f"Accepted scientific hypothesis: {conclusion}"
        elif conclusion == "Behaviour Inconclusive":
            action = DecisionAction.REQUIRE_MORE_EVIDENCE
            rationale = "Insufficient evidence to form a concrete conclusion."
        else:
            action = DecisionAction.REJECT
            rationale = f"Rejected conclusion: {conclusion}"
            
        return Decision(
            candidate_id=interpretation.candidate_id,
            timeline_id=interpretation.timeline_id,
            observation_id=interpretation.observation_id,
            schema_version="1.0",
            action=action,
            rationale=rationale,
            metadata=MappingProxyType({
                "policy": self.policy_name,
                "original_conclusion": conclusion
            }),
            timestamp=timestamp
        )
