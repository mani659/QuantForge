from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Any, Tuple

from boe.evidence.evidence_contract import EvidenceContract
from boe.evidence.evidence_errors import (
    EvidenceError,
    PackageConstructionError,
    DuplicateEvidenceTypeError,
    MissingEvidenceError,
    InvalidEvidenceError
)


@dataclass(frozen=True)
class Evidence(EvidenceContract):
    """
    Immutable representation of a scientific observation.
    
    Evidence contains ONLY abstract conclusions (e.g. labels, confidence).
    It absolutely MUST NOT contain internal state, indicators, scores, 
    risk logic, or execution directives.
    """
    evidence_id: str
    candidate_id: str
    timeline_id: str
    observer_name: str
    observer_version: str
    evidence_type: str
    confidence: float
    observed: bool
    evidence_labels: Tuple[str, ...]
    metadata: MappingProxyType[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise EvidenceError("Confidence must be between 0.0 and 1.0.")
        if not self.evidence_id:
            raise EvidenceError("evidence_id cannot be empty.")
        if not self.candidate_id:
            raise EvidenceError("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise EvidenceError("timeline_id cannot be empty.")
        if not self.observer_name:
            raise EvidenceError("observer_name cannot be empty.")
        if not self.observer_version:
            raise EvidenceError("observer_version cannot be empty.")

    def __hash__(self):
        return hash((
            self.evidence_id,
            self.candidate_id,
            self.timeline_id,
            self.observer_name,
            self.observer_version,
            self.evidence_type,
            self.confidence,
            self.observed,
            self.evidence_labels,
            frozenset(self.metadata.items()),
            self.timestamp
        ))


@dataclass(frozen=True)
class EvidencePackage:
    """
    Immutable aggregate of Evidence.
    
    Contains a collection of Evidence objects for a specific candidate/timeline.
    It does not aggregate, interpret, or summarize the evidence. It only holds it.
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    evidence_version: str
    collection_timestamp: datetime
    evidence: Tuple[Evidence, ...]
    schema_version: str
    metadata: MappingProxyType[str, Any]
    observer_provenance: Tuple[str, ...] = field(init=False)

    def __post_init__(self):
        if not self.candidate_id:
            raise InvalidEvidenceError("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise InvalidEvidenceError("timeline_id cannot be empty.")
        if not self.observation_id:
            raise InvalidEvidenceError("observation_id cannot be empty.")
        if not self.evidence_version:
            raise InvalidEvidenceError("evidence_version cannot be empty.")
        if not self.schema_version:
            raise InvalidEvidenceError("schema_version cannot be empty.")
            
        if not self.evidence:
            raise MissingEvidenceError("EvidencePackage must contain evidence.")

        # Verify all evidence belongs to the correct candidate and timeline
        seen_types = set()
        provenance_list = []
        
        for ev in self.evidence:
            if ev.candidate_id != self.candidate_id:
                raise InvalidEvidenceError(f"Evidence {ev.evidence_id} candidate mismatch.")
            if ev.timeline_id != self.timeline_id:
                raise InvalidEvidenceError(f"Evidence {ev.evidence_id} timeline mismatch.")
            
            if ev.evidence_type in seen_types:
                raise DuplicateEvidenceTypeError(f"Duplicate evidence type found: {ev.evidence_type}")
            seen_types.add(ev.evidence_type)
            
            provenance = f"{ev.observer_name}@{ev.observer_version}"
            provenance_list.append(provenance)

        # Ensure determinism by sorting evidence based on type
        sorted_evidence = tuple(sorted(self.evidence, key=lambda e: e.evidence_type))
        object.__setattr__(self, 'evidence', sorted_evidence)

        # Ensure provenance is deterministic
        sorted_provenance = tuple(sorted(provenance_list))
        object.__setattr__(self, 'observer_provenance', sorted_provenance)

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.evidence_version,
            self.collection_timestamp,
            self.evidence,
            self.observer_provenance,
            self.schema_version,
            frozenset(self.metadata.items())
        ))
