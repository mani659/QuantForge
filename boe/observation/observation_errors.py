"""Deterministic error hierarchy for Observation Policy contracts."""

from boe.detector_errors import DetectorError


class ObservationPolicyError(DetectorError):
    """Base error for an Observation Policy contract violation."""


class ObservationConfigurationError(ObservationPolicyError):
    """Raised when an Observation Policy configuration is invalid or missing."""


class ObservationPolicyValidationError(ObservationPolicyError):
    """Raised when input parameters fail verification check."""
