"""Replay lifecycle states."""

from enum import Enum


class ReplayState(str, Enum):
    """Immutable states for the Replay Engine."""

    LOADED = "LOADED"
    PLAYING = "PLAYING"
    COMPLETE = "COMPLETE"
