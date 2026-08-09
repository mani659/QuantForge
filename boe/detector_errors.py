"""Deterministic errors raised by Behavioral Observation Engine contracts."""


class DetectorError(ValueError):
    """Base error for a Behavioral Observation Engine contract violation."""


class DataIntegrityError(DetectorError):
    """Raised when supplied market or observation contract data is invalid."""


class ConfigurationError(DetectorError):
    """Raised when a detector is configured with an invalid stable identifier."""


class VersionMismatchError(DetectorError):
    """Raised when a contract schema version is unsupported or malformed."""
