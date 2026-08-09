"""Deterministic errors for Candidate Manager lifecycle contracts."""


class CandidateError(ValueError):
    """Base error for a Candidate Manager contract violation."""


class InvalidStateTransitionError(CandidateError):
    """Raised when a requested candidate lifecycle transition is not allowed."""


class CandidateAlreadyFinalizedError(CandidateError):
    """Raised when a terminal candidate receives a further transition request."""


class CandidateNotFoundError(CandidateError):
    """Raised when no candidate exists for a supplied candidate identifier."""
