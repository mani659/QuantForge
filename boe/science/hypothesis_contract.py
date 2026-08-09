from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from boe.science.science_errors import InvalidHypothesisData

class HypothesisStatus(Enum):
    """The lifecycle states of a scientific hypothesis."""
    DRAFT = auto()
    ACTIVE = auto()
    VALIDATED = auto()
    REJECTED = auto()
    ARCHIVED = auto()

@dataclass(frozen=True)
class Hypothesis:
    """
    A scientific claim proposed by a researcher.
    This exists in the Scientific Validation domain and is NOT part of the runtime.
    """
    identifier: str
    title: str
    description: str
    author: str
    created_timestamp: datetime
    status: HypothesisStatus

    def __post_init__(self):
        if not self.identifier or not self.identifier.strip():
            raise InvalidHypothesisData("Hypothesis identifier cannot be empty.")
        if not self.title or not self.title.strip():
            raise InvalidHypothesisData("Hypothesis title cannot be empty.")
        if not self.description or not self.description.strip():
            raise InvalidHypothesisData("Hypothesis description cannot be empty.")
        if not self.author or not self.author.strip():
            raise InvalidHypothesisData("Hypothesis author cannot be empty.")
        if not isinstance(self.created_timestamp, datetime):
            raise InvalidHypothesisData("Hypothesis created_timestamp must be a valid datetime.")
        if not isinstance(self.status, HypothesisStatus):
            raise InvalidHypothesisData("Hypothesis status must be a HypothesisStatus enum.")

class HypothesisContract(ABC):
    """
    Boundary contract for systems interacting with scientific hypotheses.
    """
    @abstractmethod
    def get_hypothesis(self, identifier: str) -> Hypothesis:
        """Retrieve a hypothesis by its unique identifier."""
        pass
