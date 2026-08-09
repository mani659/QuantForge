"""Deterministic evidence interpreter for QuantForge behavioral hypotheses."""

from dataclasses import dataclass

from boe.candidate import Candidate
from boe.validators.validation_result import ValidationResult

from .hypothesis import Hypothesis
from .hypothesis_errors import DecisionPolicyError, EvidenceError
from .hypothesis_result import HypothesisResult
from .policies.decision_policy_contract import DecisionPolicyContract
from .policies.strict_policy import StrictPolicy


@dataclass(frozen=True)
class DeterministicDecisionPolicy(StrictPolicy):
    """Backward-compatible name for the original deterministic all-pass policy."""

    @property
    def policy_id(self) -> str:
        """Preserve the legacy stable policy identifier."""
        return "deterministic_all_pass"


class HypothesisEngine:
    """Creates stable hypotheses and delegates all interpretation to one policy."""

    HYPOTHESIS_VERSION = "1.0.0"

    def __init__(self, decision_policy: DecisionPolicyContract | None = None) -> None:
        self._decision_policy = decision_policy or StrictPolicy()
        if not isinstance(self._decision_policy, DecisionPolicyContract):
            raise DecisionPolicyError("HypothesisEngine requires a DecisionPolicyContract.")

    @property
    def decision_policy(self) -> DecisionPolicyContract:
        """Return the immutable-policy boundary used by this engine instance."""
        return self._decision_policy

    def evaluate(
        self,
        candidate: Candidate,
        validation_results: tuple[ValidationResult, ...],
    ) -> HypothesisResult:
        """Interpret candidate evidence without mutating candidate or validator output."""
        if not isinstance(candidate, Candidate):
            raise EvidenceError("HypothesisEngine candidate must be a Candidate.")
        if not isinstance(validation_results, tuple):
            raise EvidenceError("HypothesisEngine validation_results must be a tuple.")
        if not validation_results:
            raise EvidenceError("HypothesisEngine requires at least one ValidationResult.")
        if not all(isinstance(result, ValidationResult) for result in validation_results):
            raise EvidenceError("HypothesisEngine validation_results must contain ValidationResult values.")
        if any(result.candidate_id != candidate.candidate_id for result in validation_results):
            raise EvidenceError("ValidationResult candidate_id must match the Candidate.")

        hypothesis = Hypothesis(
            hypothesis_id=f"{candidate.candidate_id}:hypothesis:{candidate.revision}",
            candidate_id=candidate.candidate_id,
            hypothesis_version=self.HYPOTHESIS_VERSION,
            created_timestamp=candidate.updated_at,
        )
        result = self._decision_policy.evaluate(hypothesis, validation_results)
        if not isinstance(result, HypothesisResult):
            raise DecisionPolicyError("Decision policy must return HypothesisResult.")
        if result.hypothesis_id != hypothesis.hypothesis_id or result.candidate_id != candidate.candidate_id:
            raise DecisionPolicyError("Decision policy result must match the evaluated hypothesis.")
        return result
