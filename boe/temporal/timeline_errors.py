"""Deterministic errors for immutable temporal-domain contracts."""


class TimelineError(ValueError):
    """Base error for a temporal-domain contract violation."""


class TimelineFreezeError(TimelineError):
    """Raised when an active timeline cannot be frozen or is already frozen."""


class TimelineRepositoryError(TimelineError):
    """Raised when a timeline repository violates its public contract."""


class InvalidFrameError(TimelineError):
    """Raised when a frame is incompatible with an active timeline."""


class DuplicateFrameError(TimelineError):
    """Raised when a timeline receives a duplicate frame identity."""
