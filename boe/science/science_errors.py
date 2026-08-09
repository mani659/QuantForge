class ScienceError(Exception):
    """Base exception for the Scientific Validation domain."""
    pass

class HypothesisError(ScienceError):
    """Base exception for Hypothesis related errors."""
    pass

class InvalidHypothesisData(HypothesisError):
    """Raised when a Hypothesis is instantiated with invalid data."""
    pass

class InvalidHypothesisStatus(HypothesisError):
    """Raised when a Hypothesis is given an invalid status."""
    pass

class ExperimentError(ScienceError):
    """Base exception for Experiment related errors."""
    pass

class InvalidExperimentData(ExperimentError):
    """Raised when an Experiment is instantiated with invalid data."""
    pass

class InvalidExperimentStatus(ExperimentError):
    """Raised when an Experiment is given an invalid status."""
    pass

class ValidationError(ScienceError):
    """Base exception for Validation related errors."""
    pass

class InvalidValidationData(ValidationError):
    """Raised when a Validation is instantiated with invalid data."""
    pass

class InvalidValidationStatus(ValidationError):
    """Raised when a Validation is given an invalid status."""
    pass

class ValidationServiceError(ScienceError):
    """Base exception for ValidationService related errors."""
    pass

class InvalidServiceOperation(ValidationServiceError):
    """Raised when a validation service operation violates lifecycle rules or linkage constraints."""
    pass
