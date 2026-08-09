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
from boe.hypothesis.hypothesis_engine import DeterministicDecisionPolicy, HypothesisEngine
from boe.hypothesis.hypothesis_errors import DecisionPolicyError
from boe.hypothesis.policies import (
    BalancedPolicy,
    DefaultPolicy,
    ExploratoryPolicy,
    PolicyFactory,
    StrictPolicy,
)
from boe.validators.validation_result import ValidationResult


class TestDecisionPolicies(unittest.TestCase):
    def setUp(self) -> None:
        self.timestamp = datetime(2026, 7, 19, 16, 0, tzinfo=timezone.utc)
        observation = BehaviorObservation(
            schema_version="1.0.0",
            observation_id="observation_policy_000001",
            environment_id="environment_policy_000001",
            behavior_type="behavioral_mean_reversion",
            instrument="EURUSD",
            timeframe="M1",
            observed_at=self.timestamp,
            detector_id="test_detector",
            detector_version="1.0.0",
        )
        self.candidate = CandidateManager().create_candidate(
            "candidate_policy_000001", observation, self.timestamp
        )

    def _evidence(self, passed: bool) -> tuple[ValidationResult, ...]:
        return (
            ValidationResult(
                schema_version="1.0.0",
                candidate_id=self.candidate.candidate_id,
                validator_id="validator_a",
                validator_version="1.0.0",
                passed=passed,
                confidence=1.0 if passed else 0.0,
                evidence=("EVIDENCE_A",),
                timestamp=self.timestamp,
            ),
        )

    def test_strict_policy_retains_all_pass_behavior(self) -> None:
        engine = HypothesisEngine(StrictPolicy())
        self.assertTrue(engine.evaluate(self.candidate, self._evidence(True)).accepted)
        self.assertFalse(engine.evaluate(self.candidate, self._evidence(False)).accepted)

    def test_placeholder_policies_are_created_and_immutable(self) -> None:
        for policy_type in (BalancedPolicy, ExploratoryPolicy):
            policy = policy_type()
            self.assertIsInstance(policy, StrictPolicy)
            with self.assertRaises(FrozenInstanceError):
                policy.policy_id = "changed"

    def test_factory_selects_supported_policies(self) -> None:
        self.assertIsInstance(PolicyFactory.create(), StrictPolicy)
        self.assertIsInstance(PolicyFactory.create("strict"), StrictPolicy)
        self.assertIsInstance(PolicyFactory.create("balanced"), BalancedPolicy)
        self.assertIsInstance(PolicyFactory.create("exploratory"), ExploratoryPolicy)
        self.assertIs(DefaultPolicy, StrictPolicy)

    def test_policy_results_are_deterministic(self) -> None:
        evidence = self._evidence(True)
        engine = HypothesisEngine(PolicyFactory.create("balanced"))
        self.assertEqual(
            engine.evaluate(self.candidate, evidence),
            engine.evaluate(self.candidate, evidence),
        )

    def test_default_and_legacy_policy_are_backward_compatible(self) -> None:
        evidence = self._evidence(True)
        default_result = HypothesisEngine().evaluate(self.candidate, evidence)
        legacy_result = HypothesisEngine(DeterministicDecisionPolicy()).evaluate(
            self.candidate, evidence
        )
        self.assertEqual(default_result, legacy_result)

    def test_invalid_policy_selection_is_rejected(self) -> None:
        with self.assertRaises(DecisionPolicyError):
            PolicyFactory.create("unknown")
        with self.assertRaises(DecisionPolicyError):
            PolicyFactory.create(1)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
