"""Shared definition for observation termination reasons."""

from enum import Enum


class TerminationReason(str, Enum):
    """Canonical reasons for observation window termination."""

    WINDOW_COMPLETE = "WINDOW_COMPLETE"
    MAX_DURATION = "MAX_DURATION"
    POLICY_TERMINATED = "POLICY_TERMINATED"
    CANDIDATE_INVALIDATED = "CANDIDATE_INVALIDATED"
    MANUAL_ABORT = "MANUAL_ABORT"
    EARLY_POLICY_STOP = "EARLY_POLICY_STOP"
    INVALID_FRAME = "INVALID_FRAME"
    INVALID_TIMELINE = "INVALID_TIMELINE"
    COMPLETED = "COMPLETED"
    UNKNOWN = "UNKNOWN"
