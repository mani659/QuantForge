from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from boe.science.science_errors import InvalidValidationData

class ValidationStatus(Enum):
    """The lifecycle states of a scientific validation."""
    VALIDATED = auto()
    REJECTED = auto()
    PARTIALLY_VALIDATED = auto()
    INCONCLUSIVE = auto()

@dataclass(frozen=True)
class Validation:
    """
    A scientific conclusion of an Experiment.
    Records the outcome without explaining why or calculating confidence.
    """
    identifier: str
    experiment_identifier: str
    hypothesis_identifier: str
    summary: str
    completed_timestamp: datetime
    status: ValidationStatus

    def __post_init__(self):
        if not self.identifier or not self.identifier.strip():
            raise InvalidValidationData("Validation identifier cannot be empty.")
        if not self.experiment_identifier or not self.experiment_identifier.strip():
            raise InvalidValidationData("Validation experiment_identifier cannot be empty.")
        if not self.hypothesis_identifier or not self.hypothesis_identifier.strip():
            raise InvalidValidationData("Validation hypothesis_identifier cannot be empty.")
        if not self.summary or not self.summary.strip():
            raise InvalidValidationData("Validation summary cannot be empty.")
        if not isinstance(self.completed_timestamp, datetime):
            raise InvalidValidationData("Validation completed_timestamp must be a datetime.")
        if not isinstance(self.status, ValidationStatus):
            raise InvalidValidationData("Validation status must be a ValidationStatus enum.")

class ValidationContract(ABC):
    """
    Boundary contract for systems interacting with scientific validations.
    """
    @abstractmethod
    def get_validation(self, identifier: str) -> Validation:
        """Retrieve a validation by its unique identifier."""
        pass
