"""Deterministic error hierarchy for the Replay Engine."""

from boe.detector_errors import DetectorError


class ReplayError(DetectorError):
    """Base class for all Replay deterministic errors."""


class MissingTimelineError(ReplayError):
    """Raised when the specified timeline cannot be loaded."""


class MissingSnapshotError(ReplayError):
    """Raised when an environment snapshot cannot be loaded for a frame."""


class InvalidReplayPositionError(ReplayError):
    """Raised when attempting to step out of bounds."""


class ReplayNotLoadedError(ReplayError):
    """Raised when attempting to operate on an unloaded replay engine."""


class ReplayAlreadyCompleteError(ReplayError):
    """Raised when attempting to step after the replay is complete."""


class RepositoryFailureError(ReplayError):
    """Raised when an underlying repository fails."""
