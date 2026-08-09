import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.interpretation.interpretation import Interpretation
from boe.decision.decision import Decision, DecisionAction
from boe.decision.policy import DefaultDecisionPolicy
from boe.decision.decision_errors import (
    InvalidDecision,
    DecisionConstructionError,
    MissingInterpretation
)

class TestDecisionPolicy(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"source": "test"})
        self.policy = DefaultDecisionPolicy()

    def _create_interpretation(self, conclusion: str = "Mean Reversion Candidate"):
        return Interpretation(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            conclusion=conclusion,
            supporting_evidence=("evidence_1",),
            metadata=self.metadata
        )

    def test_valid_interpretation_accept(self):
        interp = self._create_interpretation("Mean Reversion Candidate")
        decision = self.policy.evaluate(interp, self.dt)
        
        self.assertEqual(decision.action, DecisionAction.ACCEPT)
        self.assertIn("Accepted", decision.rationale)

    def test_valid_interpretation_reject(self):
        interp = self._create_interpretation("Failed Reversal")
        decision = self.policy.evaluate(interp, self.dt)
        
        self.assertEqual(decision.action, DecisionAction.REJECT)
        self.assertIn("Rejected", decision.rationale)

    def test_valid_interpretation_defer_or_require_more_evidence(self):
        interp = self._create_interpretation("Behaviour Inconclusive")
        decision = self.policy.evaluate(interp, self.dt)
        
        self.assertEqual(decision.action, DecisionAction.REQUIRE_MORE_EVIDENCE)
        self.assertIn("Insufficient evidence", decision.rationale)

    def test_missing_interpretation(self):
        with self.assertRaises(MissingInterpretation):
            self.policy.evaluate(None, self.dt) # type: ignore

    def test_immutable_decision(self):
        interp = self._create_interpretation()
        decision = self.policy.evaluate(interp, self.dt)
        
        with self.assertRaises(FrozenInstanceError):
            decision.rationale = "New Rationale"
        with self.assertRaises(FrozenInstanceError):
            decision.action = DecisionAction.REJECT

    def test_deterministic_outputs_and_repeatability(self):
        interp = self._create_interpretation()
        
        decision1 = self.policy.evaluate(interp, self.dt)
        decision2 = self.policy.evaluate(interp, self.dt)
        
        self.assertEqual(hash(decision1), hash(decision2))
        self.assertEqual(decision1, decision2)

    def test_schema_validation_and_error_handling(self):
        with self.assertRaises(InvalidDecision):
            Decision(
                candidate_id="",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                action=DecisionAction.ACCEPT,
                rationale="Reason",
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaises(DecisionConstructionError):
            Decision(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                action=DecisionAction.ACCEPT,
                rationale="", # Missing rationale
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaises(InvalidDecision):
            Decision(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                action="INVALID_ACTION", # type: ignore
                rationale="Reason",
                metadata=self.metadata,
                timestamp=self.dt
            )

    def test_extensibility(self):
        # We can implement a new policy without modifying existing code
        from boe.decision.policy import DecisionPolicyContract
        
        class AlwaysRejectPolicy(DecisionPolicyContract):
            @property
            def policy_name(self) -> str: return "AlwaysReject"
            
            def evaluate(self, interpretation: Interpretation, timestamp: datetime) -> Decision:
                return Decision(
                    candidate_id=interpretation.candidate_id,
                    timeline_id=interpretation.timeline_id,
                    observation_id=interpretation.observation_id,
                    schema_version="1.0",
                    action=DecisionAction.REJECT,
                    rationale="Always reject.",
                    metadata=MappingProxyType({}),
                    timestamp=timestamp
                )
                
        reject_policy = AlwaysRejectPolicy()
        decision = reject_policy.evaluate(self._create_interpretation(), self.dt)
        self.assertEqual(decision.action, DecisionAction.REJECT)

if __name__ == '__main__':
    unittest.main()
