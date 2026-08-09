import unittest
from typing import Optional
from types import MappingProxyType
from datetime import datetime

from boe.profile.profile import BehaviourProfile, BehaviourDescriptor
from boe.interpretation.interpretation import Interpretation
from boe.interpretation.models import InterpretationModelContract, DefaultInterpretationModel
from boe.interpretation.registry import InterpretationRegistry
from boe.interpretation.interpretation_errors import (
    DuplicateInterpretationModel,
    InterpretationModelNotFound,
    InvalidInterpretationModel,
    RegistryConfigurationError
)

class MockModelA(InterpretationModelContract):
    @property
    def model_name(self) -> str:
        return "MockModelA"
        
    def interpret(self, profile: BehaviourProfile) -> Optional[Interpretation]:
        return Interpretation(
            candidate_id=profile.candidate_id,
            timeline_id=profile.timeline_id,
            observation_id=profile.observation_id,
            schema_version="1.0",
            conclusion="Model A Conclusion",
            supporting_evidence=(),
            metadata=MappingProxyType({"model": self.model_name})
        )

class MockModelB(InterpretationModelContract):
    @property
    def model_name(self) -> str:
        return "MockModelB"
        
    def interpret(self, profile: BehaviourProfile) -> Optional[Interpretation]:
        return None

class InvalidMockModel:
    pass

class TestInterpretationRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = InterpretationRegistry()
        self.metadata = MappingProxyType({"source": "test"})
        desc = BehaviourDescriptor("Trait", ("Value",))
        self.profile = BehaviourProfile(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            descriptors=(desc,),
            observer_provenance=("obs_1",),
            evidence_provenance=("ev_1",),
            metadata=self.metadata
        )

    def test_registration_and_lookup(self):
        model = MockModelA()
        self.registry.register(model)
        
        self.assertTrue(self.registry.has_model("MockModelA"))
        retrieved_model = self.registry.get_model("MockModelA")
        self.assertIs(retrieved_model, model)

    def test_duplicate_registration_rejection(self):
        model1 = MockModelA()
        model2 = MockModelA() # Same name
        
        self.registry.register(model1)
        with self.assertRaises(DuplicateInterpretationModel):
            self.registry.register(model2)

    def test_missing_model_lookup(self):
        self.assertFalse(self.registry.has_model("UnknownModel"))
        with self.assertRaises(InterpretationModelNotFound):
            self.registry.get_model("UnknownModel")

    def test_invalid_model_registration(self):
        with self.assertRaises(InvalidInterpretationModel):
            self.registry.register(InvalidMockModel()) # type: ignore

    def test_deterministic_output_and_ordering(self):
        # Register out of order
        self.registry.register(MockModelB())
        self.registry.register(MockModelA())
        
        # registered_models should return alphabetically sorted tuple
        self.assertEqual(self.registry.registered_models, ("MockModelA", "MockModelB"))

    def test_model_selection_and_interpretation(self):
        self.registry.register(MockModelA())
        self.registry.register(MockModelB())
        
        # Select MockModelA
        selected_model = self.registry.get_model("MockModelA")
        interp = selected_model.interpret(self.profile)
        
        self.assertIsNotNone(interp)
        if interp:
            self.assertEqual(interp.conclusion, "Model A Conclusion")
            self.assertEqual(interp.metadata["model"], "MockModelA")

        # Select MockModelB
        selected_model_b = self.registry.get_model("MockModelB")
        interp_b = selected_model_b.interpret(self.profile)
        self.assertIsNone(interp_b) # Model B returns None

    def test_immutable_configuration_via_init(self):
        # Test registry initialization with a tuple of models (immutable config mapping)
        initial_models = (MockModelA(), MockModelB())
        registry2 = InterpretationRegistry(initial_models)
        self.assertEqual(registry2.registered_models, ("MockModelA", "MockModelB"))

    def test_default_model_compliance(self):
        # Ensure DefaultInterpretationModel adheres to contract and works
        model = DefaultInterpretationModel()
        self.assertEqual(model.model_name, "DefaultInterpretationModel_v1.0")
        
        interp = model.interpret(self.profile)
        self.assertIsNotNone(interp)
        if interp:
            self.assertEqual(interp.conclusion, "Behaviour Inconclusive")
            
    def test_extensibility(self):
        # New model can be added at runtime without touching registry code
        class CustomModel(InterpretationModelContract):
            @property
            def model_name(self) -> str: return "Custom"
            def interpret(self, p): return None
            
        self.registry.register(CustomModel())
        self.assertTrue(self.registry.has_model("Custom"))

if __name__ == '__main__':
    unittest.main()
