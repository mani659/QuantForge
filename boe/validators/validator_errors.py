"""Deterministic errors for Behavior Validator Framework contracts."""


class ValidatorError(ValueError):
    """Base error for a Behavior Validator Framework contract violation."""


class ValidationContextError(ValidatorError):
    """Raised when a ValidationContext does not satisfy its stable contract."""


class PipelineConfigurationError(ValidatorError):
    """Raised when a ValidatorPipeline receives an invalid validator configuration."""


class ValidatorVersionMismatchError(ValidatorError):
    """Raised when validator or validation-result semantic versions are invalid."""
