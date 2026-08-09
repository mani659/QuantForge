"""Abstract contract for Observation Policy implementations."""

from abc import ABC, abstractmethod
from typing import ClassVar
from datetime import datetime

from .observation_config import ObservationConfig
from .observation_result import ObservationDecision


class ObservationPolicyContract(ABC):
    """Defines the boundary for observation lifecycle control.

    Every Observation Policy must implement this contract.
    The Behavior Observation Window consumes this contract only;
    replacing the policy must never require a BOW change.

    An Observation Policy answers one question:
    "Should observation continue?"

    It does NOT interpret behavior.
    It does NOT evaluate recoil, persistence, or context.
    It does NOT produce evidence.
    It ONLY controls the observation window lifecycle.
    """

    CONTRACT_VERSION: ClassVar[str] = "1.0.0"

    @property
    @abstractmethod
    def policy_id(self) -> str:
        """Return the stable identifier for this policy implementation."""

    @property
    @abstractmethod
    def policy_version(self) -> str:
        """Return the semantic version for this policy implementation."""

    @property
    @abstractmethod
    def config(self) -> ObservationConfig:
        """Return the immutable configuration governing this policy."""

    @abstractmethod
    def evaluate(
        self,
        current_timestamp: datetime,
        frame_count: int,
        elapsed_duration: float,
    ) -> ObservationDecision:
        """Evaluate whether observation should continue or terminate.

        Parameters
        ----------
        current_timestamp:
            The current timestamp to use for decision records.
        frame_count:
            Current number of frames collected in the observation window.
        elapsed_duration:
            Elapsed observation duration in the same units as config.max_duration.

        Returns
        -------
        ObservationDecision
            Immutable decision containing continue/terminate state and reason.
        """
