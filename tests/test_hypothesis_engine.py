import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from boe.behavior_observation import BehaviorObservation
from boe.candidate_manager import CandidateManager
from boe.hypothesis.hypothesis import Hypothesis
from boe.hypothesis.hypothesis_contract import DecisionPolicyContract
from boe.hypothesis.hypothesis_engine import DeterministicDecisionPolicy, HypothesisEngine
from boe.hypothesis.hypothesis_errors import DecisionPolicyError, EvidenceError, HypothesisError
from boe.hypothesis.hypothesis_result import HypothesisResult
from boe.validators.validation_result import ValidationResult


class TestHypothesisEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.timestamp = datetime(2026, 7, 19, 14, 0, tzinfo=timezone.utc)
        observation = BehaviorObservation(
            schema_version="1.0.0",
            observation_id="observation_000001",
            environment_id="environment_000001",
            behavior_type="behavioral_mean_reversion",
            instrument="EURUSD",
            timeframe="M1",
            observed_at=self.timestamp,
            detector_id="test_detector",
            detector_version="1.0.0",
        )
        self.candidate = CandidateManager().create_candidate(
            "candidate_000001", observation, self.timestamp
        )
        self.engine = HypothesisEngine()

    def _result(self, validator_id: str, passed: bool) -> ValidationResult:
        return ValidationResult(
            schema_version="1.0.0",
            candidate_id=self.candidate.candidate_id,
            validator_id=validator_id,
            validator_version="1.0.0",
            passed=passed,
            confidence=1.0 if passed else 0.0,
            evidence=(f"{validator_id}_evidence",),
            timestamp=self.timestamp,
        )

    def test_hypothesis_and_result_are_immutable(self) -> None:
        hypothesis = Hypothesis("hypothesis_000001", self.candidate.candidate_id, "1.0.0", self.timestamp)
        result = self.engine.evaluate(self.candidate, (self._result("validator_a", True),))
        with self.assertRaises(FrozenInstanceError):
            hypothesis.candidate_id = "changed"
        with self.assertRaises(FrozenInstanceError):
            result.accepted = False

    def test_decision_policy_contract_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DecisionPolicyContract()
        self.assertEqual(DeterministicDecisionPolicy().CONTRACT_VERSION, "1.0.0")

    def test_all_passing_evidence_accepts_hypothesis(self) -> None:
        result = self.engine.evaluate(self.candidate, (self._result("validator_a", True), self._result("validator_b", True)))
        self.assertTrue(result.accepted)
        self.assertEqual(result.overall_confidence, 1.0)
        self.assertEqual(result.supporting_evidence, ("validator_a_evidence", "validator_b_evidence"))
        self.assertEqual(result.rejected_evidence, ())

    def test_rejected_and_mixed_evidence_reject_hypothesis(self) -> None:
        result = self.engine.evaluate(self.candidate, (self._result("validator_a", True), self._result("validator_b", False)))
        self.assertFalse(result.accepted)
        self.assertEqual(result.overall_confidence, 0.0)
        self.assertEqual(result.rejected_evidence, ("validator_b_evidence",))

    def test_evaluation_is_reproducible(self) -> None:
        evidence = (self._result("validator_a", True),)
        self.assertEqual(self.engine.evaluate(self.candidate, evidence), self.engine.evaluate(self.candidate, evidence))

    def test_exception_hierarchy_and_empty_evidence(self) -> None:
        self.assertTrue(issubclass(DecisionPolicyError, HypothesisError))
        self.assertTrue(issubclass(EvidenceError, HypothesisError))
        with self.assertRaises(EvidenceError):
            self.engine.evaluate(self.candidate, ())
        with self.assertRaises(DecisionPolicyError):
            HypothesisEngine(decision_policy=object())


if __name__ == "__main__":
    unittest.main()
