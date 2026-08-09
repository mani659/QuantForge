"""Abstract contract implemented by all Behavioral Observation validators."""

from abc import ABC, abstractmethod
from typing import ClassVar

from boe.candidate import Candidate

from .validation_context import ValidationContext
from .validation_result import ValidationResult


class BehaviorValidatorContract(ABC):
    """Defines a pure validator boundary without prescribing validation logic."""

    CONTRACT_VERSION: ClassVar[str] = "1.0.0"

    @property
    @abstractmethod
    def validator_id(self) -> str:
        """Return the stable identifier for this validator implementation."""

    @property
    @abstractmethod
    def validator_name(self) -> str:
        """Return the human-readable stable name for this validator."""

    @property
    @abstractmethod
    def validator_version(self) -> str:
        """Return the semantic version of this validator implementation."""

    @abstractmethod
    def validate(self, candidate: Candidate, context: ValidationContext) -> ValidationResult:
        """Evaluate immutable candidate evidence and return an immutable result."""
