from abc import ABC, abstractmethod
from typing import Optional
from types import MappingProxyType

from boe.profile.profile import BehaviourProfile
from boe.interpretation.interpretation import Interpretation

class InterpretationModelContract(ABC):
    """
    Abstract contract for an Interpretation Model.
    Models perform the actual interpretation logic, explaining what a BehaviourProfile most likely represents.
    """
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Returns the unique identifier for this interpretation model."""
        pass
        
    @abstractmethod
    def interpret(self, profile: BehaviourProfile) -> Optional[Interpretation]:
        """
        Converts a BehaviourProfile into an Interpretation.
        Returns None if this model cannot confidently interpret the profile.
        """
        pass

class DefaultInterpretationModel(InterpretationModelContract):
    """
    Default interpretation model for v1.0.
    Builds a scientific conclusion based on behavioural profile descriptors.
    """
    
    @property
    def model_name(self) -> str:
        return "DefaultInterpretationModel_v1.0"
        
    def interpret(self, profile: BehaviourProfile) -> Optional[Interpretation]:
        if not profile:
            return None
            
        try:
            traits_desc = profile.get_descriptor("Observed behavioural traits")
            traits = set(traits_desc.value)
        except Exception:
            traits = set()
            
        try:
            char_desc = profile.get_descriptor("Behaviour characteristics")
            characteristics = set(char_desc.value)
        except Exception:
            characteristics = set()
            
        if "Label_RECOIL" in traits and "RECOIL" in characteristics:
            conclusion = "Mean Reversion Candidate"
        elif "Label_PERSISTENCE" in traits:
            conclusion = "Trend Continuation Candidate"
        elif "Label_FAILURE" in traits:
            conclusion = "Failed Reversal"
        else:
            conclusion = "Behaviour Inconclusive"
            
        return Interpretation(
            candidate_id=profile.candidate_id,
            timeline_id=profile.timeline_id,
            observation_id=profile.observation_id,
            schema_version="1.0",
            conclusion=conclusion,
            supporting_evidence=tuple(sorted(traits.union(characteristics))),
            metadata=MappingProxyType({"model": self.model_name})
        )
