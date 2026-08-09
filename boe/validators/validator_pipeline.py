"""Deterministic sequential pipeline for Behavior Validator Framework results."""

from typing import Iterable

from boe.candidate import Candidate

from .validation_context import ValidationContext
from .validation_result import ValidationResult
from .validator_contract import BehaviorValidatorContract
from .validator_errors import PipelineConfigurationError, ValidatorError


class ValidatorPipeline:
    """Runs configured validators in order and returns all immutable results."""

    def __init__(self, validators: Iterable[BehaviorValidatorContract] = ()) -> None:
        self._validators = tuple(validators)
        if not all(isinstance(validator, BehaviorValidatorContract) for validator in self._validators):
            raise PipelineConfigurationError(
                "ValidatorPipeline validators must implement BehaviorValidatorContract."
            )

    @property
    def validators(self) -> tuple[BehaviorValidatorContract, ...]:
        """Return configured validators in their deterministic execution order."""
        return self._validators

    def validate(self, candidate: Candidate, context: ValidationContext) -> tuple[ValidationResult, ...]:
        """Execute every validator sequentially without interpretation or short-circuiting."""
        if not isinstance(candidate, Candidate):
            raise ValidatorError("ValidatorPipeline candidate must be a Candidate.")
        if not isinstance(context, ValidationContext):
            raise ValidatorError("ValidatorPipeline context must be a ValidationContext.")
        if context.candidate_id != candidate.candidate_id:
            raise ValidatorError("ValidationContext candidate_id must match the Candidate.")

        results = []
        for validator in self._validators:
            result = validator.validate(candidate, context)
            if not isinstance(result, ValidationResult):
                raise ValidatorError("Behavior validators must return ValidationResult.")
            if result.candidate_id != candidate.candidate_id:
                raise ValidatorError("ValidationResult candidate_id must match the Candidate.")
            if result.validator_id != validator.validator_id:
                raise ValidatorError("ValidationResult validator_id must match its validator.")
            if result.validator_version != validator.validator_version:
                raise ValidatorError("ValidationResult validator_version must match its validator.")
            results.append(result)
        return tuple(results)
