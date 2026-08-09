from enum import Enum
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any
from datetime import datetime

from boe.decision.decision_errors import InvalidDecision, DecisionConstructionError

class DecisionAction(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    DEFER = "DEFER"
    REQUIRE_MORE_EVIDENCE = "REQUIRE_MORE_EVIDENCE"

@dataclass(frozen=True)
class Decision:
    """
    Immutable scientific outcome derived from an Interpretation.
    Answers "Should this interpretation be acted upon?".
    It is NOT a trading order. No lots, SL, TP, execution, or risk.
    """
    candidate_id: str
    timeline_id: str
    observation_id: str
    schema_version: str
    action: DecisionAction
    rationale: str
    metadata: MappingProxyType[str, Any]
    timestamp: datetime

    def __post_init__(self):
        if not self.candidate_id:
            raise InvalidDecision("candidate_id cannot be empty.")
        if not self.timeline_id:
            raise InvalidDecision("timeline_id cannot be empty.")
        if not self.observation_id:
            raise InvalidDecision("observation_id cannot be empty.")
        if not self.schema_version:
            raise InvalidDecision("schema_version cannot be empty.")
        if not self.action:
            raise DecisionConstructionError("Decision action cannot be empty.")
        if not isinstance(self.action, DecisionAction):
            raise InvalidDecision("action must be a DecisionAction enum.")
        if not self.rationale:
            raise DecisionConstructionError("Decision rationale cannot be empty.")
        if not isinstance(self.timestamp, datetime):
            raise InvalidDecision("timestamp must be a valid datetime.")

    def __hash__(self):
        return hash((
            self.candidate_id,
            self.timeline_id,
            self.observation_id,
            self.schema_version,
            self.action,
            self.rationale,
            frozenset(self.metadata.items()),
            self.timestamp
        ))
