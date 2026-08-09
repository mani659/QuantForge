from typing import Callable, Tuple, List, Optional
from types import MappingProxyType

from boe.profile.profile import BehaviourProfile
from boe.interpretation.interpretation import Interpretation
from boe.interpretation.interpretation_errors import (
    MissingBehaviourProfile,
    InterpretationConflict,
    UnsupportedBehaviourProfile
)

# A plugin takes a BehaviourProfile and returns an optional Interpretation.
InterpretationPluginFunc = Callable[[BehaviourProfile], Optional[Interpretation]]

def default_interpretation_plugin(profile: BehaviourProfile) -> Optional[Interpretation]:
    """
    Default interpretation plugin for v1.0.
    Builds a scientific conclusion based on behavioural profile descriptors.
    """
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
        metadata=MappingProxyType({"engine": "InterpretationEngine v1.0"})
    )

class InterpretationEngine:
    """
    Stateless engine to transform a BehaviourProfile into an Interpretation.
    Uses injected interpretation models (plugins) to allow future replacement
    without modifying the BehaviourProfile.
    """
    
    def __init__(self, plugins: Tuple[InterpretationPluginFunc, ...] = (default_interpretation_plugin,), schema_version: str = "1.0"):
        self.plugins = plugins
        self.schema_version = schema_version
        
    def build_interpretation(self, profile: BehaviourProfile) -> Interpretation:
        if not profile:
            raise MissingBehaviourProfile("BehaviourProfile is required.")
            
        interpretations: List[Interpretation] = []
        
        for plugin in self.plugins:
            result = plugin(profile)
            if result:
                interpretations.append(result)
                
        if not interpretations:
            raise UnsupportedBehaviourProfile("No plugin could interpret this BehaviourProfile.")
            
        if len(interpretations) > 1:
            # If multiple plugins yield DIFFERENT conclusions, it's a conflict.
            first_conclusion = interpretations[0].conclusion
            for interp in interpretations[1:]:
                if interp.conclusion != first_conclusion:
                    raise InterpretationConflict(
                        f"Conflicting interpretations: {first_conclusion} vs {interp.conclusion}"
                    )
                    
        return interpretations[0]
