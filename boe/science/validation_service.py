from datetime import datetime

from boe.science.hypothesis_contract import Hypothesis
from boe.science.experiment_contract import Experiment
from boe.science.validation_contract import Validation, ValidationStatus
from boe.science.validation_service_contract import ValidationServiceContract
from boe.science.science_errors import InvalidServiceOperation

class ValidationService(ValidationServiceContract):
    """
    Orchestrates the Scientific Validation lifecycle without performing scientific analysis.
    Verifies object consistency and constructs immutable Validation objects.
    """
    def create_validation(
        self,
        identifier: str,
        hypothesis: Hypothesis,
        experiment: Experiment,
        summary: str,
        completed_timestamp: datetime,
        status: ValidationStatus
    ) -> Validation:
        
        # Verify object consistency
        if experiment.hypothesis_identifier != hypothesis.identifier:
            raise InvalidServiceOperation(
                f"Experiment {experiment.identifier} does not belong to Hypothesis {hypothesis.identifier}."
            )
            
        return Validation(
            identifier=identifier,
            experiment_identifier=experiment.identifier,
            hypothesis_identifier=hypothesis.identifier,
            summary=summary,
            completed_timestamp=completed_timestamp,
            status=status
        )
