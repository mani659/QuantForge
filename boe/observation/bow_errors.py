"""Deterministic error hierarchy for the Behavior Observation Window."""

from boe.detector_errors import DetectorError


class BOWError(DetectorError):
    """Base class for all BOW deterministic errors."""


class WindowAlreadyOpenError(BOWError):
    """Raised when attempting to open an already open window."""


class WindowNotOpenError(BOWError):
    """Raised when attempting to operate on a closed or uninitialized window."""


class InvalidSnapshotError(BOWError):
    """Raised when appending an invalid or malformed EnvironmentSnapshot."""


class AppendAfterFreezeError(BOWError):
    """Raised when attempting to append after the window is frozen."""


class DoubleFreezeError(BOWError):
    """Raised when attempting to freeze a window more than once."""


class PolicyFailureError(BOWError):
    """Raised when the Observation Policy fails deterministically."""


class TimelineFailureError(BOWError):
    """Raised when the underlying timeline rejects an operation."""
