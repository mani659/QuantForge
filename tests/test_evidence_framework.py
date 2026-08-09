import unittest
from datetime import datetime, timezone
from types import MappingProxyType
from dataclasses import FrozenInstanceError

from boe.evidence.evidence_errors import EvidenceError
from boe.evidence.evidence import Evidence, EvidencePackage
from boe.evidence.evidence_contract import EvidenceContract
from boe.evidence.observer_contract import ObserverContract
from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline


class DummyObserver(ObserverContract):
    @property
    def name(self) -> str:
        return "DummyObserver"

    @property
    def version(self) -> str:
        return "1.0.0"

    def observe(self, timeline: FrozenBehaviorTimeline) -> Evidence:
        return Evidence(
            evidence_id="ev_001",
            candidate_id="cand_001",
            timeline_id=timeline.timeline_id if hasattr(timeline, "timeline_id") else "timeline_001",
            observer_name=self.name,
            observer_version=self.version,
            evidence_type="MOCK",
            confidence=1.0,
            observed=True,
            evidence_labels=("MOCK_OBSERVED",),
            metadata=MappingProxyType({"key": "value"}),
            timestamp=datetime.now(timezone.utc)
        )


class TestEvidenceFramework(unittest.TestCase):
    def setUp(self):
        self.valid_ts = datetime.now(timezone.utc)
        self.metadata = MappingProxyType({"foo": "bar"})

        self.valid_evidence = Evidence(
            evidence_id="ev_123",
            candidate_id="cand_abc",
            timeline_id="time_xyz",
            observer_name="TestObserver",
            observer_version="1.0.0",
            evidence_type="TEST",
            confidence=0.85,
            observed=True,
            evidence_labels=("LABEL_1", "LABEL_2"),
            metadata=self.metadata,
            timestamp=self.valid_ts
        )

    def test_evidence_immutability(self):
        """Test that Evidence is immutable after creation."""
        with self.assertRaises(FrozenInstanceError):
            self.valid_evidence.confidence = 0.5

    def test_evidence_contract_compliance(self):
        """Test that Evidence implements EvidenceContract correctly."""
        self.assertIsInstance(self.valid_evidence, EvidenceContract)
        self.assertEqual(self.valid_evidence.evidence_id, "ev_123")
        self.assertEqual(self.valid_evidence.candidate_id, "cand_abc")
        self.assertEqual(self.valid_evidence.timeline_id, "time_xyz")

    def test_confidence_bounds(self):
        """Test that confidence must be between 0.0 and 1.0."""
        # Lower bound fail
        with self.assertRaises(EvidenceError):
            Evidence(
                evidence_id="e", candidate_id="c", timeline_id="t",
                observer_name="o", observer_version="v", evidence_type="t",
                confidence=-0.1, observed=True, evidence_labels=(),
                metadata=self.metadata, timestamp=self.valid_ts
            )
            
        # Upper bound fail
        with self.assertRaises(EvidenceError):
            Evidence(
                evidence_id="e", candidate_id="c", timeline_id="t",
                observer_name="o", observer_version="v", evidence_type="t",
                confidence=1.1, observed=True, evidence_labels=(),
                metadata=self.metadata, timestamp=self.valid_ts
            )
            
        # Boundaries pass
        ev_low = Evidence(
            evidence_id="e", candidate_id="c", timeline_id="t",
            observer_name="o", observer_version="v", evidence_type="t",
            confidence=0.0, observed=True, evidence_labels=(),
            metadata=self.metadata, timestamp=self.valid_ts
        )
        self.assertEqual(ev_low.confidence, 0.0)

        ev_high = Evidence(
            evidence_id="e", candidate_id="c", timeline_id="t",
            observer_name="o", observer_version="v", evidence_type="t",
            confidence=1.0, observed=True, evidence_labels=(),
            metadata=self.metadata, timestamp=self.valid_ts
        )
        self.assertEqual(ev_high.confidence, 1.0)

    def test_empty_identities_rejected(self):
        """Test that empty string identifiers are rejected."""
        with self.assertRaises(EvidenceError):
            Evidence(
                evidence_id="", candidate_id="c", timeline_id="t",
                observer_name="o", observer_version="v", evidence_type="t",
                confidence=1.0, observed=True, evidence_labels=(),
                metadata=self.metadata, timestamp=self.valid_ts
            )
            
        with self.assertRaises(EvidenceError):
            Evidence(
                evidence_id="e", candidate_id="", timeline_id="t",
                observer_name="o", observer_version="v", evidence_type="t",
                confidence=1.0, observed=True, evidence_labels=(),
                metadata=self.metadata, timestamp=self.valid_ts
            )

    def test_evidence_equality_and_hashability(self):
        """Test that Evidence objects are hashable and equal based on values."""
        ev1 = Evidence(
            evidence_id="ev_123", candidate_id="cand_abc", timeline_id="time_xyz",
            observer_name="TestObserver", observer_version="1.0.0", evidence_type="TEST",
            confidence=0.85, observed=True, evidence_labels=("LABEL_1", "LABEL_2"),
            metadata=self.metadata, timestamp=self.valid_ts
        )
        
        self.assertEqual(self.valid_evidence, ev1)
        self.assertEqual(hash(self.valid_evidence), hash(ev1))

    def test_evidence_package_immutability(self):
        """Test that EvidencePackage is immutable."""
        pkg = EvidencePackage(
            candidate_id="cand_abc",
            timeline_id="time_xyz",
            observation_id="obs_123",
            evidence_version="v1",
            collection_timestamp=self.valid_ts,
            evidence=(self.valid_evidence,),
            schema_version="1.0",
            metadata=self.metadata
        )
        with self.assertRaises(FrozenInstanceError):
            pkg.candidate_id = "new_cand"

    def test_evidence_package_mismatch_rejected(self):
        """Test that EvidencePackage rejects evidence that doesn't match its IDs."""
        bad_evidence = Evidence(
            evidence_id="ev_999",
            candidate_id="WRONG_CANDIDATE",
            timeline_id="time_xyz",
            observer_name="Test",
            observer_version="1.0",
            evidence_type="TEST",
            confidence=1.0,
            observed=True,
            evidence_labels=(),
            metadata=self.metadata,
            timestamp=self.valid_ts
        )
        
        with self.assertRaises(EvidenceError):
            EvidencePackage(
                candidate_id="cand_abc",
                timeline_id="time_xyz",
                observation_id="obs_123",
                evidence_version="v1",
                collection_timestamp=self.valid_ts,
                evidence=(bad_evidence,),
                schema_version="1.0",
                metadata=self.metadata
            )

    def test_observer_contract_compliance(self):
        """Test that concrete observer must implement abstract methods."""
        class InvalidObserver(ObserverContract):
            pass

        with self.assertRaises(TypeError):
            InvalidObserver()

        dummy = DummyObserver()
        self.assertEqual(dummy.name, "DummyObserver")
        self.assertEqual(dummy.version, "1.0.0")
        
        # We mock timeline just as an object
        class MockTimeline:
            timeline_id = "mock_t"
            
        ev = dummy.observe(MockTimeline())
        self.assertIsInstance(ev, Evidence)
        self.assertEqual(ev.timeline_id, "mock_t")
