"""Immutable output contract for the Observation Policy decisions."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .termination_reason import TerminationReason


@dataclass(frozen=True)
class ObservationDecision:
    """Immutable output from an Observation Policy evaluation."""

    continue_observation: bool
    terminate_observation: bool
    termination_reason: Optional[TerminationReason]
    policy_id: str
    policy_version: str
    timestamp: datetime

    def __post_init__(self) -> None:
        """Validate result immutability and basic fields."""
        if not isinstance(self.continue_observation, bool):
            raise TypeError("continue_observation must be a boolean.")
        if not isinstance(self.terminate_observation, bool):
            raise TypeError("terminate_observation must be a boolean.")
        if self.continue_observation == self.terminate_observation:
            raise ValueError("continue_observation and terminate_observation cannot be equal.")
        if self.terminate_observation:
            if not isinstance(self.termination_reason, TerminationReason):
                raise ValueError(f"Invalid termination_reason: {self.termination_reason}. Must be a TerminationReason")
        else:
            if self.termination_reason is not None:
                raise ValueError("termination_reason must be None when continue_observation is True.")
        if not isinstance(self.policy_id, str) or not self.policy_id:
            raise ValueError("policy_id must be a non-empty string.")
        if not isinstance(self.policy_version, str) or not self.policy_version:
            raise ValueError("policy_version must be a non-empty string.")
        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be a datetime.")
