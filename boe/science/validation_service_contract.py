from abc import ABC, abstractmethod
from datetime import datetime

from boe.science.hypothesis_contract import Hypothesis
from boe.science.experiment_contract import Experiment
from boe.science.validation_contract import Validation, ValidationStatus

class ValidationServiceContract(ABC):
    """
    Boundary contract for orchestrating the scientific validation lifecycle.
    """
    @abstractmethod
    def create_validation(
        self,
        identifier: str,
        hypothesis: Hypothesis,
        experiment: Experiment,
        summary: str,
        completed_timestamp: datetime,
        status: ValidationStatus
    ) -> Validation:
        """
        Constructs an immutable Validation object ensuring consistency between Hypothesis and Experiment.
        """
        pass
