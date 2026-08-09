"""Abstract contract implemented by all Behavioral Observation Engine detectors."""

from abc import ABC, abstractmethod
from typing import ClassVar

from .behavior_observation import BehaviorObservation
from .observation_environment import ObservationEnvironment


class BehaviorDetectorContract(ABC):
    """Defines the stable detector boundary without prescribing detection logic."""

    CONTRACT_VERSION: ClassVar[str] = "1.0.0"

    @property
    @abstractmethod
    def detector_id(self) -> str:
        """Return the stable identifier of the detector implementation."""

    @property
    @abstractmethod
    def detector_version(self) -> str:
        """Return the semantic version of the detector implementation."""

    @abstractmethod
    def observe(self, environment: ObservationEnvironment) -> BehaviorObservation | None:
        """Return a public observation when behavior is observed, otherwise None."""
