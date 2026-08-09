"""Strict deterministic evidence policy."""

from dataclasses import dataclass

from boe.validators.validation_result import ValidationResult

from ..hypothesis import Hypothesis
from ..hypothesis_errors import EvidenceError
from ..hypothesis_result import HypothesisResult
from .decision_policy_contract import DecisionPolicyContract


@dataclass(frozen=True)
class StrictPolicy(DecisionPolicyContract):
    """Accept a hypothesis only when every supplied validator result passed."""

    SCHEMA_VERSION = "1.0.0"

    @property
    def policy_id(self) -> str:
        """Return the stable strict policy identifier."""
        return "strict_all_pass"

    @property
    def policy_version(self) -> str:
        """Return the semantic version of this policy."""
        return "1.0.0"

    def evaluate(
        self,
        hypothesis: Hypothesis,
        validation_results: tuple[ValidationResult, ...],
    ) -> HypothesisResult:
        """Interpret evidence using the historical all-results-pass rule."""
        if not validation_results:
            raise EvidenceError("Hypothesis evaluation requires at least one ValidationResult.")

        accepted = all(result.passed for result in validation_results)
        supporting_evidence = tuple(
            evidence
            for result in validation_results
            if result.passed
            for evidence in result.evidence
        )
        rejected_evidence = tuple(
            evidence
            for result in validation_results
            if not result.passed
            for evidence in result.evidence
        )
        return HypothesisResult(
            schema_version=self.SCHEMA_VERSION,
            hypothesis_id=hypothesis.hypothesis_id,
            candidate_id=hypothesis.candidate_id,
            accepted=accepted,
            overall_confidence=1.0 if accepted else 0.0,
            supporting_evidence=supporting_evidence,
            rejected_evidence=rejected_evidence,
            evaluated_timestamp=hypothesis.created_timestamp,
        )
