import unittest
from datetime import datetime
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.evidence.evidence import Evidence, EvidencePackage
from boe.evidence.evidence_errors import (
    DuplicateEvidenceTypeError,
    MissingEvidenceError,
    InvalidEvidenceError
)

class TestEvidencePackage(unittest.TestCase):
    def setUp(self):
        self.dt = datetime(2026, 1, 1, 12, 0, 0)
        self.metadata = MappingProxyType({"source": "test"})
        
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
            evidence_labels=("test",),
            metadata=self.metadata,
            timestamp=self.dt
        )

    def test_single_evidence_construction(self):
        ev = self._create_evidence("VELOCITY")
        pkg = EvidencePackage(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            evidence_version="v1",
            collection_timestamp=self.dt,
            evidence=(ev,),
            schema_version="1.0",
            metadata=self.metadata
        )
        self.assertEqual(len(pkg.evidence), 1)
        self.assertEqual(pkg.observer_provenance, ("VelocityObserver@1.0.0",))

    def test_all_five_evidence_objects(self):
        ev_types = ["RECOIL", "PERSISTENCE", "FAILURE", "VELOCITY", "COMPRESSION"]
        evidence_objects = tuple(self._create_evidence(t) for t in ev_types)
        
        pkg = EvidencePackage(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            evidence_version="v1",
            collection_timestamp=self.dt,
            evidence=evidence_objects,
            schema_version="1.0",
            metadata=self.metadata
        )
        
        self.assertEqual(len(pkg.evidence), 5)
        # Should be alphabetically sorted by evidence_type:
        # COMPRESSION, FAILURE, PERSISTENCE, RECOIL, VELOCITY
        expected_order = ("COMPRESSION", "FAILURE", "PERSISTENCE", "RECOIL", "VELOCITY")
        actual_order = tuple(e.evidence_type for e in pkg.evidence)
        self.assertEqual(actual_order, expected_order)

    def test_ordering_preservation_deterministic(self):
        # Create evidence out of order
        ev_types = ["VELOCITY", "RECOIL", "FAILURE", "COMPRESSION", "PERSISTENCE"]
        evidence_objects = tuple(self._create_evidence(t) for t in ev_types)
        
        pkg = EvidencePackage(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            evidence_version="v1",
            collection_timestamp=self.dt,
            evidence=evidence_objects,
            schema_version="1.0",
            metadata=self.metadata
        )
        
        expected_order = ("COMPRESSION", "FAILURE", "PERSISTENCE", "RECOIL", "VELOCITY")
        actual_order = tuple(e.evidence_type for e in pkg.evidence)
        self.assertEqual(actual_order, expected_order)

    def test_duplicate_evidence_type_raises_error(self):
        ev1 = self._create_evidence("RECOIL")
        ev2 = self._create_evidence("RECOIL") # Same type
        
        with self.assertRaises(DuplicateEvidenceTypeError):
            EvidencePackage(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                evidence_version="v1",
                collection_timestamp=self.dt,
                evidence=(ev1, ev2),
                schema_version="1.0",
                metadata=self.metadata
            )

    def test_missing_evidence_raises_error(self):
        with self.assertRaises(MissingEvidenceError):
            EvidencePackage(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                evidence_version="v1",
                collection_timestamp=self.dt,
                evidence=(), # Empty
                schema_version="1.0",
                metadata=self.metadata
            )

    def test_mismatched_candidate_or_timeline_raises_error(self):
        ev_good = self._create_evidence("RECOIL", candidate_id="c_1")
        ev_bad = self._create_evidence("VELOCITY", candidate_id="c_OTHER")
        
        with self.assertRaises(InvalidEvidenceError):
            EvidencePackage(
                candidate_id="c_1",
                timeline_id="t_1",
                observation_id="obs_1",
                evidence_version="v1",
                collection_timestamp=self.dt,
                evidence=(ev_good, ev_bad),
                schema_version="1.0",
                metadata=self.metadata
            )

    def test_missing_required_fields_raises_invalid_error(self):
        ev = self._create_evidence("RECOIL")
        with self.assertRaises(InvalidEvidenceError):
            EvidencePackage(
                candidate_id="",
                timeline_id="t_1",
                observation_id="obs_1",
                evidence_version="v1",
                collection_timestamp=self.dt,
                evidence=(ev,),
                schema_version="1.0",
                metadata=self.metadata
            )

    def test_immutability(self):
        ev = self._create_evidence("RECOIL")
        pkg = EvidencePackage(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            evidence_version="v1",
            collection_timestamp=self.dt,
            evidence=(ev,),
            schema_version="1.0",
            metadata=self.metadata
        )
        with self.assertRaises(FrozenInstanceError):
            pkg.schema_version = "2.0"

    def test_deterministic_repeatability_and_hashing(self):
        ev_types = ["VELOCITY", "RECOIL", "FAILURE"]
        evidence_objects = tuple(self._create_evidence(t) for t in ev_types)
        
        pkg1 = EvidencePackage(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            evidence_version="v1",
            collection_timestamp=self.dt,
            evidence=evidence_objects,
            schema_version="1.0",
            metadata=self.metadata
        )

        pkg2 = EvidencePackage(
            candidate_id="c_1",
            timeline_id="t_1",
            observation_id="obs_1",
            evidence_version="v1",
            collection_timestamp=self.dt,
            evidence=evidence_objects[::-1], # Reverse order
            schema_version="1.0",
            metadata=self.metadata
        )

        # Hashes should match since order is deterministically sorted internally
        self.assertEqual(hash(pkg1), hash(pkg2))
        self.assertEqual(pkg1, pkg2)

if __name__ == '__main__':
    unittest.main()
