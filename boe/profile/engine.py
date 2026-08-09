from typing import Callable, Tuple, List
from types import MappingProxyType

from boe.evidence.evidence import EvidencePackage
from boe.profile.profile import BehaviourProfile, BehaviourDescriptor

# A builder takes an EvidencePackage and returns a tuple of BehaviourDescriptors
DescriptorBuilderFunc = Callable[[EvidencePackage], Tuple[BehaviourDescriptor, ...]]

def default_descriptor_builder(package: EvidencePackage) -> Tuple[BehaviourDescriptor, ...]:
    """
    Default descriptor builder for v1.0.
    Builds descriptive (NOT interpretive) characteristics and traits.
    """
    traits = set()
    characteristics = set()
    
    for ev in package.evidence:
        traits.update(ev.evidence_labels)
        characteristics.add(ev.evidence_type)
        
    return (
        BehaviourDescriptor(name="Observed behavioural traits", value=tuple(sorted(traits))),
        BehaviourDescriptor(name="Behaviour characteristics", value=tuple(sorted(characteristics))),
        BehaviourDescriptor(name="Behaviour completeness", value=len(package.evidence)),
    )

class BehaviourProfileEngine:
    """
    Stateless engine to transform an EvidencePackage into a BehaviourProfile.
    Uses injected builder functions to allow future extension without modifying the core profile.
    """
    
    def __init__(self, builders: Tuple[DescriptorBuilderFunc, ...] = (default_descriptor_builder,), schema_version: str = "1.0"):
        self.builders = builders
        self.schema_version = schema_version
        
    def build_profile(self, evidence_package: EvidencePackage) -> BehaviourProfile:
        descriptors: List[BehaviourDescriptor] = []
        
        for builder in self.builders:
            descriptors.extend(builder(evidence_package))
            
        # Extract provenance from EvidencePackage
        obs_provenance = evidence_package.observer_provenance
        ev_provenance = tuple(sorted(ev.evidence_id for ev in evidence_package.evidence))
        
        return BehaviourProfile(
            candidate_id=evidence_package.candidate_id,
            timeline_id=evidence_package.timeline_id,
            observation_id=evidence_package.observation_id,
            schema_version=self.schema_version,
            descriptors=tuple(descriptors),
            observer_provenance=obs_provenance,
            evidence_provenance=ev_provenance,
            metadata=MappingProxyType({"engine": "BehaviourProfileEngine v1.0"})
        )
