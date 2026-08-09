from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Tuple
from boe.profile.profile_errors import (
    InvalidBehaviourProfile,
    DuplicateBehaviourDescriptor,
    MissingBehaviourDescriptor,
    BehaviourProfileConstructionError
)

@dataclass(frozen=True)
class BehaviourDescriptor:
    """
    Immutable representation of a specific behavioural attribute.
    It ONLY DESCRIBES behaviour and DOES NOT explain it.
    """
    name: str
    value: Any

    def __post_init__(self):
        if not self.name:
            raise BehaviourProfileConstructionError("Descriptor name cannot be empty.")
        
    def __hash__(self):
        # Using str(self.value) to handle unhashable types if they sneak in, 
        # though everything should be immutable domain objects.
        return hash((self.name, str(self.value)))

@dataclass(frozen=True)
class BehaviourProfile:
    """
    Immutable collection of behavioural descriptors derived from an EvidencePackage.
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    descriptors: Tuple[BehaviourDescriptor, ...]
    observer_provenance: Tuple[str, ...]
    evidence_provenance: Tuple[str, ...]
    metadata: MappingProxyType[str, Any]

    def __post_init__(self):
        if not self.candidate_id:
            raise InvalidBehaviourProfile("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise InvalidBehaviourProfile("timeline_id cannot be empty.")
        if not self.observation_id:
            raise InvalidBehaviourProfile("observation_id cannot be empty.")
        if not self.schema_version:
            raise InvalidBehaviourProfile("schema_version cannot be empty.")
        if not self.descriptors:
            raise MissingBehaviourDescriptor("BehaviourProfile must contain at least one descriptor.")

        names = set()
        for d in self.descriptors:
            if d.name in names:
                raise DuplicateBehaviourDescriptor(f"Duplicate descriptor found: {d.name}")
            names.add(d.name)
            
        # Ensure determinism by sorting descriptors and provenance
        sorted_desc = tuple(sorted(self.descriptors, key=lambda x: x.name))
        object.__setattr__(self, 'descriptors', sorted_desc)
        
        sorted_obs_prov = tuple(sorted(self.observer_provenance))
        object.__setattr__(self, 'observer_provenance', sorted_obs_prov)
        
        sorted_ev_prov = tuple(sorted(self.evidence_provenance))
        object.__setattr__(self, 'evidence_provenance', sorted_ev_prov)

    def get_descriptor(self, name: str) -> BehaviourDescriptor:
        for d in self.descriptors:
            if d.name == name:
                return d
        raise MissingBehaviourDescriptor(f"Descriptor {name} not found.")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.descriptors,
            self.observer_provenance,
            self.evidence_provenance,
            frozenset(self.metadata.items())
        ))
