import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError
from typing import Optional

from boe.profile.profile import BehaviourProfile, BehaviourDescriptor
from boe.interpretation.interpretation import Interpretation
from boe.interpretation.engine import InterpretationEngine
from boe.interpretation.interpretation_errors import (
    InvalidInterpretation,
    MissingBehaviourProfile,
    InterpretationConflict,
    UnsupportedBehaviourProfile,
    InterpretationConstructionError
)

class TestInterpretationEngine(unittest.TestCase):
    def setUp(self):
        self.metadata = MappingProxyType({"source": "test"})
        self.engine = InterpretationEngine()

    def _create_profile(self, traits=("Label_RECOIL",), characteristics=("RECOIL",)):
        desc_traits = BehaviourDescriptor("Observed behavioural traits", traits)
        desc_chars = BehaviourDescriptor("Behaviour characteristics", characteristics)
        
        return BehaviourProfile(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            descriptors=(desc_traits, desc_chars),
            observer_provenance=("Obs1@1.0",),
            evidence_provenance=("e_1",),
            metadata=self.metadata
        )

    def test_valid_behaviour_profile(self):
        profile = self._create_profile(traits=("Label_RECOIL",), characteristics=("RECOIL",))
        interp = self.engine.build_interpretation(profile)
        
        self.assertEqual(interp.conclusion, "Mean Reversion Candidate")
        self.assertIn("Label_RECOIL", interp.supporting_evidence)
        self.assertIn("RECOIL", interp.supporting_evidence)

    def test_missing_behaviour_profile(self):
        with self.assertRaises(MissingBehaviourProfile):
            self.engine.build_interpretation(None)

    def test_unknown_descriptors(self):
        # Even if descriptors are completely unknown, the default engine should return inconclusive
        desc_unknown = BehaviourDescriptor("Unknown", ("Foo",))
        profile = BehaviourProfile(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            descriptors=(desc_unknown,),
            observer_provenance=("Obs1@1.0",),
            evidence_provenance=("e_1",),
            metadata=self.metadata
        )
        
        interp = self.engine.build_interpretation(profile)
        self.assertEqual(interp.conclusion, "Behaviour Inconclusive")
        self.assertEqual(len(interp.supporting_evidence), 0)

    def test_immutable_interpretation(self):
        profile = self._create_profile()
        interp = self.engine.build_interpretation(profile)
        
        with self.assertRaises(FrozenInstanceError):
            interp.conclusion = "Trend Continuation Candidate"
        with self.assertRaises(FrozenInstanceError):
            interp.schema_version = "2.0"

    def test_deterministic_outputs_and_repeatability(self):
        profile = self._create_profile(traits=("Label_FAILURE", "Label_RECOIL"), characteristics=("RECOIL", "FAILURE"))
        
        interp1 = self.engine.build_interpretation(profile)
        interp2 = self.engine.build_interpretation(profile)
        
        self.assertEqual(hash(interp1), hash(interp2))
        self.assertEqual(interp1, interp2)
        
        # Test sorting
        expected_evidence = tuple(sorted(["Label_FAILURE", "Label_RECOIL", "RECOIL", "FAILURE"]))
        self.assertEqual(interp1.supporting_evidence, expected_evidence)

    def test_schema_validation_and_error_conditions(self):
        with self.assertRaises(InvalidInterpretation):
            Interpretation(
                candidate_id="",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                conclusion="Valid",
                supporting_evidence=("evidence",),
                metadata=self.metadata
            )
            
        with self.assertRaises(InterpretationConstructionError):
            Interpretation(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                conclusion="", # empty conclusion
                supporting_evidence=("evidence",),
                metadata=self.metadata
            )

    def test_interpretation_conflict(self):
        def plugin1(p: BehaviourProfile) -> Optional[Interpretation]:
            return Interpretation(p.candidate_id, p.timeline_id, p.observation_id, "1.0", "Conclusion A", (), MappingProxyType({}))
            
        def plugin2(p: BehaviourProfile) -> Optional[Interpretation]:
            return Interpretation(p.candidate_id, p.timeline_id, p.observation_id, "1.0", "Conclusion B", (), MappingProxyType({}))
            
        conflict_engine = InterpretationEngine(plugins=(plugin1, plugin2))
        profile = self._create_profile()
        
        with self.assertRaises(InterpretationConflict):
            conflict_engine.build_interpretation(profile)

    def test_unsupported_behaviour_profile(self):
        def no_op_plugin(p: BehaviourProfile) -> Optional[Interpretation]:
            return None
            
        unsupported_engine = InterpretationEngine(plugins=(no_op_plugin,))
        profile = self._create_profile()
        
        with self.assertRaises(UnsupportedBehaviourProfile):
            unsupported_engine.build_interpretation(profile)

if __name__ == '__main__':
    unittest.main()
