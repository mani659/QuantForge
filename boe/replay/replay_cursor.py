"""Immutable position tracker for the Replay Engine."""

from dataclasses import dataclass

from boe.temporal.behavior_frame import BehaviorFrame
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.replay.replay_state import ReplayState


@dataclass(frozen=True)
class ReplayCursor:
    """Immutable snapshot of the current replay position."""

    position: int
    total_frames: int
    status: ReplayState
    current_frame: BehaviorFrame | None
    current_snapshot: EnvironmentSnapshot | None
