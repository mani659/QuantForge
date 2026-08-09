"""Immutable result container for the completed Behavior Observation Window."""

from dataclasses import dataclass

from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline
from boe.observation.termination_reason import TerminationReason


@dataclass(frozen=True)
class BOWResult:
    """Immutable final output from a completed observation window."""

    timeline: FrozenBehaviorTimeline
    termination_reason: TerminationReason
    frame_count: int
    duration_seconds: float
