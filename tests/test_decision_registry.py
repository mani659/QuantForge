import unittest
from typing import Optional
from types import MappingProxyType
from datetime import datetime

from boe.interpretation.interpretation import Interpretation
from boe.decision.decision import Decision, DecisionAction
from boe.decision.policy import DecisionPolicyContract, DefaultDecisionPolicy
from boe.decision.registry import DecisionRegistry
from boe.decision.decision_errors import (
    DecisionPolicyNotFound,
    DuplicateDecisionPolicy,
    InvalidDecisionPolicy,
    RegistryConfigurationError
)

class MockPolicyA(DecisionPolicyContract):
    @property
    def policy_name(self) -> str:
        return "MockPolicyA"
        
    def evaluate(self, interpretation: Interpretation, timestamp: datetime) -> Decision:
        return Decision(
            candidate_id=interpretation.candidate_id,
            timeline_id=interpretation.timeline_id,
            observation_id=interpretation.observation_id,
            schema_version="1.0",
            action=DecisionAction.ACCEPT,
            rationale="Mock Policy A",
            metadata=MappingProxyType({"policy": self.policy_name}),
            timestamp=timestamp
        )

class MockPolicyB(DecisionPolicyContract):
    @property
    def policy_name(self) -> str:
        return "MockPolicyB"
        
    def evaluate(self, interpretation: Interpretation, timestamp: datetime) -> Decision:
        return Decision(
            candidate_id=interpretation.candidate_id,
            timeline_id=interpretation.timeline_id,
            observation_id=interpretation.observation_id,
            schema_version="1.0",
            action=DecisionAction.REJECT,
            rationale="Mock Policy B",
            metadata=MappingProxyType({"policy": self.policy_name}),
            timestamp=timestamp
        )

class InvalidMockPolicy:
    pass

class TestDecisionRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = DecisionRegistry()
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.interp = Interpretation(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            conclusion="Test Conclusion",
            supporting_evidence=(),
            metadata=MappingProxyType({})
        )

    def test_registration_and_lookup(self):
        policy = MockPolicyA()
        self.registry.register(policy)
        
        self.assertTrue(self.registry.has_policy("MockPolicyA"))
        retrieved_policy = self.registry.get_policy("MockPolicyA")
        self.assertIs(retrieved_policy, policy)

    def test_duplicate_registration_rejection(self):
        policy1 = MockPolicyA()
        policy2 = MockPolicyA()
        
        self.registry.register(policy1)
        with self.assertRaises(DuplicateDecisionPolicy):
            self.registry.register(policy2)

    def test_missing_policy_lookup(self):
        self.assertFalse(self.registry.has_policy("UnknownPolicy"))
        with self.assertRaises(DecisionPolicyNotFound):
            self.registry.get_policy("UnknownPolicy")

    def test_invalid_policy_registration(self):
        with self.assertRaises(InvalidDecisionPolicy):
            self.registry.register(InvalidMockPolicy()) # type: ignore

    def test_deterministic_resolution_and_ordering(self):
        self.registry.register(MockPolicyB())
        self.registry.register(MockPolicyA())
        
        self.assertEqual(self.registry.registered_policies, ("MockPolicyA", "MockPolicyB"))

    def test_policy_selection_and_evaluation(self):
        self.registry.register(MockPolicyA())
        self.registry.register(MockPolicyB())
        
        selected_a = self.registry.get_policy("MockPolicyA")
        dec_a = selected_a.evaluate(self.interp, self.dt)
        self.assertEqual(dec_a.action, DecisionAction.ACCEPT)

        selected_b = self.registry.get_policy("MockPolicyB")
        dec_b = selected_b.evaluate(self.interp, self.dt)
        self.assertEqual(dec_b.action, DecisionAction.REJECT)

    def test_immutable_configuration_via_init(self):
        initial_policies = (MockPolicyA(), MockPolicyB())
        registry2 = DecisionRegistry(initial_policies)
        self.assertEqual(registry2.registered_policies, ("MockPolicyA", "MockPolicyB"))

    def test_default_policy_compliance(self):
        policy = DefaultDecisionPolicy()
        self.assertEqual(policy.policy_name, "DefaultDecisionPolicy_v1.0")
        
    def test_extensibility(self):
        class CustomPolicy(DecisionPolicyContract):
            @property
            def policy_name(self) -> str: return "Custom"
            def evaluate(self, interp, ts): return None # type: ignore
            
        self.registry.register(CustomPolicy())
        self.assertTrue(self.registry.has_policy("Custom"))

if __name__ == '__main__':
    unittest.main()
