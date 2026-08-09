"""Immutable final output from a completed replay."""

from dataclasses import dataclass

from boe.replay.replay_state import ReplayState


@dataclass(frozen=True)
class ReplayResult:
    """Immutable final output produced by Replay Engine finish()."""

    timeline_id: str
    frames_processed: int
    status: ReplayState
