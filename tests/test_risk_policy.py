import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.decision.decision import Decision, DecisionAction
from boe.risk.models import RiskProfile, RiskDescriptor
from boe.risk.policy import (
    DefaultRiskPolicy,
    RiskPolicyConfig,
    RiskPolicyAction,
    RiskPolicyEvaluation
)
from boe.risk.risk_errors import (
    RiskPolicyConstructionError,
    MissingDecision,
    MissingRiskModel
)

class TestRiskPolicy(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"source": "test"})
        self.policy = DefaultRiskPolicy()

    def _create_decision(self, action: DecisionAction = DecisionAction.ACCEPT):
        return Decision(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            action=action,
            rationale="Test rationale",
            metadata=self.metadata,
            timestamp=self.dt
        )

    def _create_profile(self, candidate_id="c_1", interaction="Independent"):
        desc_interaction = RiskDescriptor("Portfolio Interaction Flag", (interaction,))
        return RiskProfile(
            candidate_id=candidate_id,
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            descriptors=(desc_interaction,),
            metadata=self.metadata,
            timestamp=self.dt
        )

    def test_valid_evaluation_approve(self):
        decision = self._create_decision(DecisionAction.ACCEPT)
        profile = self._create_profile()
        eval_result = self.policy.evaluate(decision, profile, self.dt)
        
        self.assertEqual(eval_result.action, RiskPolicyAction.APPROVE)
        self.assertEqual(eval_result.metadata["policy"], "DefaultRiskPolicy_v1.0")

    def test_valid_evaluation_reduce(self):
        decision = self._create_decision(DecisionAction.REQUIRE_MORE_EVIDENCE)
        profile = self._create_profile()
        eval_result = self.policy.evaluate(decision, profile, self.dt)
        
        self.assertEqual(eval_result.action, RiskPolicyAction.REDUCE_EXPOSURE)

    def test_strict_mode_rejects_non_independent(self):
        strict_policy = DefaultRiskPolicy(RiskPolicyConfig(require_independent_interaction=True))
        decision = self._create_decision(DecisionAction.ACCEPT)
        profile = self._create_profile(interaction="Dependent")
        
        eval_result = strict_policy.evaluate(decision, profile, self.dt)
        self.assertEqual(eval_result.action, RiskPolicyAction.REJECT)

    def test_missing_decision_or_profile(self):
        decision = self._create_decision()
        profile = self._create_profile()
        
        with self.assertRaises(MissingDecision):
            self.policy.evaluate(None, profile, self.dt) # type: ignore
            
        with self.assertRaises(MissingRiskModel):
            self.policy.evaluate(decision, None, self.dt) # type: ignore

    def test_mismatched_candidate_id(self):
        decision = self._create_decision()
        profile = self._create_profile(candidate_id="c_2")
        
        with self.assertRaises(RiskPolicyConstructionError):
            self.policy.evaluate(decision, profile, self.dt)

    def test_immutable_outputs(self):
        decision = self._create_decision()
        profile = self._create_profile()
        eval_result = self.policy.evaluate(decision, profile, self.dt)
        
        with self.assertRaises(FrozenInstanceError):
            eval_result.schema_version = "2.0"

    def test_deterministic_evaluation(self):
        decision = self._create_decision()
        profile = self._create_profile()
        
        eval1 = self.policy.evaluate(decision, profile, self.dt)
        eval2 = self.policy.evaluate(decision, profile, self.dt)
        
        self.assertEqual(eval1, eval2)
        self.assertEqual(hash(eval1), hash(eval2))

    def test_schema_validation(self):
        with self.assertRaises(RiskPolicyConstructionError):
            RiskPolicyEvaluation(
                candidate_id="",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                action=RiskPolicyAction.APPROVE,
                rationale="r",
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaises(RiskPolicyConstructionError):
            RiskPolicyEvaluation(
                candidate_id="c",
                timeline_id="t",
                observation_id="o",
                schema_version="1",
                action="NOT_AN_ENUM", # type: ignore
                rationale="r",
                metadata=self.metadata,
                timestamp=self.dt
            )

if __name__ == '__main__':
    unittest.main()
