from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Tuple
from boe.interpretation.interpretation_errors import InvalidInterpretation, InterpretationConstructionError

@dataclass(frozen=True)
class Interpretation:
    """
    Immutable scientific conclusion drawn from a BehaviourProfile.
    It ONLY explains "What does this behaviour most likely represent?".
    It MUST NOT authorize trades, score, or calculate position size.
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    conclusion: str
    supporting_evidence: Tuple[str, ...]
    metadata: MappingProxyType[str, Any]

    def __post_init__(self):
        if not self.candidate_id:
            raise InvalidInterpretation("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise InvalidInterpretation("timeline_id cannot be empty.")
        if not self.observation_id:
            raise InvalidInterpretation("observation_id cannot be empty.")
        if not self.schema_version:
            raise InvalidInterpretation("schema_version cannot be empty.")
        if not self.conclusion:
            raise InterpretationConstructionError("conclusion cannot be empty.")
            
        # Ensure determinism
        sorted_evidence = tuple(sorted(self.supporting_evidence))
        object.__setattr__(self, 'supporting_evidence', sorted_evidence)

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.conclusion,
            self.supporting_evidence,
            frozenset(self.metadata.items())
        ))
