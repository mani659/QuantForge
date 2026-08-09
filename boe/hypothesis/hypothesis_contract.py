"""Abstract decision-policy contract for deterministic hypothesis interpretation."""

from abc import ABC, abstractmethod
from typing import ClassVar

from boe.validators.validation_result import ValidationResult

from .hypothesis import Hypothesis
from .hypothesis_result import HypothesisResult


class DecisionPolicyContract(ABC):
    """Defines how immutable validator evidence is interpreted by the Hypothesis Engine."""

    CONTRACT_VERSION: ClassVar[str] = "1.0.0"

    @property
    @abstractmethod
    def policy_id(self) -> str:
        """Return the stable identifier for this policy implementation."""

    @property
    @abstractmethod
    def policy_version(self) -> str:
        """Return the semantic version for this policy implementation."""

    @abstractmethod
    def evaluate(
        self,
        hypothesis: Hypothesis,
        validation_results: tuple[ValidationResult, ...],
    ) -> HypothesisResult:
        """Interpret immutable evidence and return an immutable hypothesis result."""
