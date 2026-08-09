"""Abstract boundary for the Behavior Observation Window."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Mapping

from boe.candidate import Candidate
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.observation.observation_contract import ObservationPolicyContract
from boe.observation.observation_result import ObservationDecision
from boe.observation.termination_reason import TerminationReason
from boe.observation.bow_result import BOWResult


class BehaviorObservationWindowContract(ABC):
    """Strictly temporal collector. Interprets no behavior."""

    @abstractmethod
    def open(self, candidate: Candidate, timeline_id: str, current_timestamp: datetime) -> None:
        """Initialize the observation window for a specific candidate."""

    @abstractmethod
    def append_snapshot(
        self,
        snapshot: EnvironmentSnapshot,
        frame_id: str,
        behavior_state: str,
        behavior_strength: str,
        metadata: Mapping[str, object]
    ) -> None:
        """Construct and append an immutable BehaviorFrame to the active timeline."""

    @abstractmethod
    def evaluate_policy(
        self,
        current_timestamp: datetime,
        policy: ObservationPolicyContract
    ) -> ObservationDecision:
        """Consult the policy purely based on timeline statistics."""

    @abstractmethod
    def freeze(
        self,
        closed_timestamp: datetime,
        termination_reason: TerminationReason,
        timeline_metadata: Mapping[str, object] | None = None
    ) -> BOWResult:
        """Produce the immutable canonical timeline and result."""

    @abstractmethod
    def close(self) -> None:
        """Clean up the window explicitly."""
