import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.decision.decision import Decision, DecisionAction
from boe.risk.models import DefaultRiskModel, RiskProfile, RiskDescriptor
from boe.risk.risk_errors import (
    RiskModelConstructionError,
    MissingDecision,
    InvalidRiskModel
)

class TestRiskModel(unittest.TestCase):

    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"source": "test"})
        self.model = DefaultRiskModel()

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

    def test_valid_decision_evaluation(self):
        decision = self._create_decision(DecisionAction.ACCEPT)
        profile = self.model.evaluate(decision, self.dt)
        
        self.assertEqual(profile.metadata["model"], "DefaultRiskModel_v1.0")
        
        cat_desc = profile.get_descriptor("Risk Category")
        self.assertEqual(cat_desc.values[0], "Standard Exposure")

    def test_rejected_decision_evaluation(self):
        decision = self._create_decision(DecisionAction.REJECT)
        profile = self.model.evaluate(decision, self.dt)
        
        cat_desc = profile.get_descriptor("Risk Category")
        self.assertEqual(cat_desc.values[0], "No Exposure")

    def test_missing_decision(self):
        with self.assertRaises(MissingDecision):
            self.model.evaluate(None, self.dt) # type: ignore

    def test_schema_validation_and_errors(self):
        with self.assertRaises(RiskModelConstructionError):
            RiskDescriptor(name="", values=("Test",))
            
        with self.assertRaises(RiskModelConstructionError):
            RiskDescriptor(name="Test", values="NotATuple") # type: ignore
            
        desc = RiskDescriptor("Test", ("Val",))
        
        with self.assertRaises(RiskModelConstructionError):
            RiskProfile(
                candidate_id="",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                descriptors=(desc,),
                metadata=self.metadata,
                timestamp=self.dt
            )
            
        with self.assertRaises(RiskModelConstructionError):
            RiskProfile(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                descriptors="NotATuple", # type: ignore
                metadata=self.metadata,
                timestamp=self.dt
            )

    def test_immutable_risk_model(self):
        decision = self._create_decision(DecisionAction.ACCEPT)
        profile = self.model.evaluate(decision, self.dt)
        
        with self.assertRaises(FrozenInstanceError):
            profile.schema_version = "2.0"
            
        desc = profile.descriptors[0]
        with self.assertRaises(FrozenInstanceError):
            desc.name = "New Name"

    def test_deterministic_outputs_and_repeatability(self):
        decision = self._create_decision(DecisionAction.ACCEPT)
        
        profile1 = self.model.evaluate(decision, self.dt)
        profile2 = self.model.evaluate(decision, self.dt)
        
        # Test equality and hashing
        self.assertEqual(profile1, profile2)
        self.assertEqual(hash(profile1), hash(profile2))

    def test_descriptor_lookup(self):
        decision = self._create_decision(DecisionAction.ACCEPT)
        profile = self.model.evaluate(decision, self.dt)
        
        desc = profile.get_descriptor("Exposure Class")
        self.assertEqual(desc.name, "Exposure Class")
        
        with self.assertRaises(InvalidRiskModel):
            profile.get_descriptor("Unknown Descriptor")

if __name__ == '__main__':
    unittest.main()
