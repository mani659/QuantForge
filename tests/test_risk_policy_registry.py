import unittest
from datetime import datetime
from types import MappingProxyType

from boe.decision.decision import Decision, DecisionAction
from boe.risk.models import RiskProfile
from boe.risk.policy import RiskPolicyContract, RiskPolicyEvaluation, RiskPolicyAction
from boe.risk.registry import RiskPolicyRegistry
from boe.risk.risk_errors import (
    RiskPolicyNotFound,
    DuplicateRiskPolicy,
    InvalidRiskPolicy
)

class MockRiskPolicyA(RiskPolicyContract):
    @property
    def policy_name(self) -> str:
        return "MockRiskPolicyA"
        
    def evaluate(self, decision: Decision, profile: RiskProfile, timestamp: datetime) -> RiskPolicyEvaluation:
        return RiskPolicyEvaluation(
            candidate_id=decision.candidate_id,
            timeline_id=decision.timeline_id,
            observation_id=decision.observation_id,
            schema_version="1.0",
            action=RiskPolicyAction.APPROVE,
            rationale="Mock Policy A",
            metadata=MappingProxyType({"policy": self.policy_name}),
            timestamp=timestamp
        )

class MockRiskPolicyB(RiskPolicyContract):
    @property
    def policy_name(self) -> str:
        return "MockRiskPolicyB"
        
    def evaluate(self, decision: Decision, profile: RiskProfile, timestamp: datetime) -> RiskPolicyEvaluation:
        return RiskPolicyEvaluation(
            candidate_id=decision.candidate_id,
            timeline_id=decision.timeline_id,
            observation_id=decision.observation_id,
            schema_version="1.0",
            action=RiskPolicyAction.REJECT,
            rationale="Mock Policy B",
            metadata=MappingProxyType({"policy": self.policy_name}),
            timestamp=timestamp
        )

class InvalidMockPolicy:
    pass

class TestRiskPolicyRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = RiskPolicyRegistry()
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.decision = Decision(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            action=DecisionAction.ACCEPT,
            rationale="Test",
            metadata=MappingProxyType({}),
            timestamp=self.dt
        )
        self.profile = RiskProfile(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            descriptors=(),
            metadata=MappingProxyType({}),
            timestamp=self.dt
        )

    def test_registration_and_lookup(self):
        policy = MockRiskPolicyA()
        self.registry.register(policy)
        
        self.assertTrue(self.registry.has_policy("MockRiskPolicyA"))
        retrieved_policy = self.registry.get_policy("MockRiskPolicyA")
        self.assertIs(retrieved_policy, policy)

    def test_duplicate_registration_rejection(self):
        policy1 = MockRiskPolicyA()
        policy2 = MockRiskPolicyA()
        
        self.registry.register(policy1)
        with self.assertRaises(DuplicateRiskPolicy):
            self.registry.register(policy2)

    def test_missing_policy_lookup(self):
        self.assertFalse(self.registry.has_policy("UnknownPolicy"))
        with self.assertRaises(RiskPolicyNotFound):
            self.registry.get_policy("UnknownPolicy")

    def test_invalid_policy_registration(self):
        with self.assertRaises(InvalidRiskPolicy):
            self.registry.register(InvalidMockPolicy()) # type: ignore

    def test_deterministic_resolution_and_ordering(self):
        self.registry.register(MockRiskPolicyB())
        self.registry.register(MockRiskPolicyA())
        
        self.assertEqual(self.registry.registered_policies, ("MockRiskPolicyA", "MockRiskPolicyB"))

    def test_policy_selection_and_evaluation(self):
        self.registry.register(MockRiskPolicyA())
        self.registry.register(MockRiskPolicyB())
        
        selected_a = self.registry.get_policy("MockRiskPolicyA")
        eval_a = selected_a.evaluate(self.decision, self.profile, self.dt)
        self.assertEqual(eval_a.action, RiskPolicyAction.APPROVE)

        selected_b = self.registry.get_policy("MockRiskPolicyB")
        eval_b = selected_b.evaluate(self.decision, self.profile, self.dt)
        self.assertEqual(eval_b.action, RiskPolicyAction.REJECT)

    def test_immutable_configuration_via_init(self):
        initial_policies = (MockRiskPolicyA(), MockRiskPolicyB())
        registry2 = RiskPolicyRegistry(initial_policies)
        self.assertEqual(registry2.registered_policies, ("MockRiskPolicyA", "MockRiskPolicyB"))

if __name__ == '__main__':
    unittest.main()
