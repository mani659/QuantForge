from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Dict, Any, List

from boe.science.science_errors import InvalidExperimentData

class ExperimentStatus(Enum):
    """The lifecycle states of a scientific experiment."""
    DRAFT = auto()
    READY = auto()
    RUNNING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

@dataclass(frozen=True)
class Experiment:
    """
    A reproducible scientific test for a Hypothesis.
    Specifies WHAT will be tested. Never performs the test.
    """
    identifier: str
    hypothesis_identifier: str
    title: str
    description: str
    markets: List[str]
    configuration: Dict[str, Any]
    analysis_period: Dict[str, datetime]
    created_timestamp: datetime
    status: ExperimentStatus

    def __post_init__(self):
        if not self.identifier or not self.identifier.strip():
            raise InvalidExperimentData("Experiment identifier cannot be empty.")
        if not self.hypothesis_identifier or not self.hypothesis_identifier.strip():
            raise InvalidExperimentData("Experiment hypothesis_identifier cannot be empty.")
        if not self.title or not self.title.strip():
            raise InvalidExperimentData("Experiment title cannot be empty.")
        if not self.description or not self.description.strip():
            raise InvalidExperimentData("Experiment description cannot be empty.")
        
        # Validate before conversion
        if not isinstance(self.markets, (list, tuple)) or not all(isinstance(m, str) and m.strip() for m in self.markets):
            raise InvalidExperimentData("Experiment markets must be a list/tuple of non-empty strings.")
        if not self.markets:
            raise InvalidExperimentData("Experiment markets cannot be empty.")
        if not isinstance(self.configuration, (dict, tuple)):
            raise InvalidExperimentData("Experiment configuration must be a dictionary/tuple.")
        if not isinstance(self.analysis_period, (dict, tuple)):
            raise InvalidExperimentData("Experiment analysis_period must be a dictionary/tuple.")
            
        ap = dict(self.analysis_period) if isinstance(self.analysis_period, tuple) else self.analysis_period
        
        if 'start' not in ap or 'end' not in ap:
            raise InvalidExperimentData("Experiment analysis_period must contain 'start' and 'end' keys.")
        if not isinstance(ap['start'], datetime) or not isinstance(ap['end'], datetime):
            raise InvalidExperimentData("Experiment analysis_period 'start' and 'end' must be datetimes.")
        if ap['start'] >= ap['end']:
            raise InvalidExperimentData("Experiment analysis_period 'start' must be before 'end'.")
        if not isinstance(self.created_timestamp, datetime):
            raise InvalidExperimentData("Experiment created_timestamp must be a datetime.")
        if not isinstance(self.status, ExperimentStatus):
            raise InvalidExperimentData("Experiment status must be an ExperimentStatus enum.")
            
        # Convert to immutable structures
        object.__setattr__(self, 'markets', tuple(self.markets))
        if isinstance(self.configuration, dict):
            object.__setattr__(self, 'configuration', tuple(sorted(self.configuration.items())))
        if isinstance(self.analysis_period, dict):
            object.__setattr__(self, 'analysis_period', tuple(sorted(self.analysis_period.items())))

class ExperimentContract(ABC):
    """
    Boundary contract for systems interacting with scientific experiments.
    """
    @abstractmethod
    def get_experiment(self, identifier: str) -> Experiment:
        """Retrieve an experiment by its unique identifier."""
        pass
