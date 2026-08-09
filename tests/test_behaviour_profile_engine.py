import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.evidence.evidence import Evidence, EvidencePackage
from boe.profile.profile import BehaviourProfile, BehaviourDescriptor
from boe.profile.engine import BehaviourProfileEngine, default_descriptor_builder
from boe.profile.profile_errors import (
    InvalidBehaviourProfile,
    DuplicateBehaviourDescriptor,
    MissingBehaviourDescriptor,
    BehaviourProfileConstructionError
)

class TestBehaviourProfileEngine(unittest.TestCase):
    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"source": "test"})
        self.engine = BehaviourProfileEngine()

    def _create_evidence(self, ev_type: str, candidate_id="c_1", timeline_id="t_1"):
        return Evidence(
            evidence_id=f"e_{ev_type}",
            candidate_id=candidate_id,
            timeline_id=timeline_id,
            observer_name=f"{ev_type.capitalize()}Observer",
            observer_version="1.0.0",
            evidence_type=ev_type,
            confidence=0.9,
            observed=True,
            evidence_labels=(f"Label_{ev_type}",),
            metadata=self.metadata,
            timestamp=self.dt
        )

    def _create_evidence_package(self, ev_types):
        evidence_objects = tuple(self._create_evidence(t) for t in ev_types)
        return EvidencePackage(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            evidence_version="v1",
            collection_timestamp=self.dt,
            evidence=evidence_objects,
            schema_version="1.0",
            metadata=self.metadata
        )

    def test_single_descriptor(self):
        desc = BehaviourDescriptor(name="Test", value="Value")
        self.assertEqual(desc.name, "Test")
        self.assertEqual(desc.value, "Value")

    def test_descriptor_missing_name_fails(self):
        with self.assertRaises(BehaviourProfileConstructionError):
            BehaviourDescriptor(name="", value="Value")

    def test_profile_construction(self):
        desc1 = BehaviourDescriptor("Archetype", "Fast Recovery")
        desc2 = BehaviourDescriptor("Completeness", 1.0)
        
        profile = BehaviourProfile(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            descriptors=(desc1, desc2),
            observer_provenance=("Obs1@1.0", "Obs2@1.0"),
            evidence_provenance=("e_1", "e_2"),
            metadata=self.metadata
        )
        self.assertEqual(len(profile.descriptors), 2)
        # Verify deterministic sorting of provenance
        self.assertEqual(profile.evidence_provenance, ("e_1", "e_2"))

    def test_profile_missing_descriptor_fails(self):
        with self.assertRaises(MissingBehaviourDescriptor):
            BehaviourProfile(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                descriptors=(),
                observer_provenance=("Obs1@1.0",),
                evidence_provenance=("e_1",),
                metadata=self.metadata
            )

    def test_profile_duplicate_descriptor_fails(self):
        desc1 = BehaviourDescriptor("Archetype", "Fast Recovery")
        desc2 = BehaviourDescriptor("Archetype", "Weak Persistence")
        
        with self.assertRaises(DuplicateBehaviourDescriptor):
            BehaviourProfile(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="1.0",
                descriptors=(desc1, desc2),
                observer_provenance=("Obs1@1.0",),
                evidence_provenance=("e_1",),
                metadata=self.metadata
            )

    def test_profile_schema_validation_fails(self):
        desc = BehaviourDescriptor("Archetype", "Fast")
        with self.assertRaises(InvalidBehaviourProfile):
            BehaviourProfile(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                schema_version="",
                descriptors=(desc,),
                observer_provenance=("Obs1@1.0",),
                evidence_provenance=("e_1",),
                metadata=self.metadata
            )

    def test_engine_deterministic_ordering_and_repeatability(self):
        ev_types = ["VELOCITY", "RECOIL", "FAILURE"]
        pkg = self._create_evidence_package(ev_types)
        
        profile1 = self.engine.build_profile(pkg)
        profile2 = self.engine.build_profile(pkg)
        
        # Output should be perfectly repeatable
        self.assertEqual(hash(profile1), hash(profile2))
        self.assertEqual(profile1, profile2)
        
        # Test descriptor sorting
        expected_descriptor_names = (
            "Behaviour characteristics",
            "Behaviour completeness",
            "Observed behavioural traits"
        )
        actual_descriptor_names = tuple(d.name for d in profile1.descriptors)
        self.assertEqual(actual_descriptor_names, expected_descriptor_names)

        # Test provenance sorting
        expected_ev_provenance = tuple(sorted(["e_VELOCITY", "e_RECOIL", "e_FAILURE"]))
        self.assertEqual(profile1.evidence_provenance, expected_ev_provenance)

    def test_immutability(self):
        desc = BehaviourDescriptor("Archetype", "Fast")
        profile = BehaviourProfile(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            schema_version="1.0",
            descriptors=(desc,),
            observer_provenance=("Obs1@1.0",),
            evidence_provenance=("e_1",),
            metadata=self.metadata
        )
        with self.assertRaises(FrozenInstanceError):
            profile.schema_version = "2.0"
        with self.assertRaises(FrozenInstanceError):
            desc.name = "NewName"

    def test_engine_extensibility(self):
        # Create a custom builder
        def custom_builder(pkg: EvidencePackage):
            return (BehaviourDescriptor("Custom Trait", "Custom Value"),)
            
        custom_engine = BehaviourProfileEngine(builders=(default_descriptor_builder, custom_builder))
        
        pkg = self._create_evidence_package(["RECOIL"])
        profile = custom_engine.build_profile(pkg)
        
        # Should have the 3 default + 1 custom = 4 descriptors
        self.assertEqual(len(profile.descriptors), 4)
        custom_desc = profile.get_descriptor("Custom Trait")
        self.assertEqual(custom_desc.value, "Custom Value")

if __name__ == '__main__':
    unittest.main()
