"""Deterministic implementation of the Behavior Observation Window."""

from datetime import datetime
from typing import Mapping

from boe.candidate import Candidate
from boe.temporal.active_observation_timeline import ActiveObservationTimeline
from boe.temporal.behavior_frame import BehaviorFrame
from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.temporal.timeline_errors import TimelineError, TimelineFreezeError
from boe.observation.observation_contract import ObservationPolicyContract
from boe.observation.observation_result import ObservationDecision
from boe.observation.termination_reason import TerminationReason
from boe.observation.bow_contract import BehaviorObservationWindowContract
from boe.observation.bow_result import BOWResult
from boe.observation.bow_errors import (
    WindowAlreadyOpenError,
    WindowNotOpenError,
    InvalidSnapshotError,
    AppendAfterFreezeError,
    DoubleFreezeError,
    TimelineFailureError
)


class BehaviorObservationWindow(BehaviorObservationWindowContract):
    """The strictly temporal runtime collector."""

    def __init__(self) -> None:
        self._timeline: ActiveObservationTimeline | None = None
        self._opened_timestamp: datetime | None = None

    def open(self, candidate: Candidate, timeline_id: str, current_timestamp: datetime) -> None:
        if self._timeline is not None:
            raise WindowAlreadyOpenError("Behavior Observation Window is already open.")
        
        self._timeline = ActiveObservationTimeline(
            schema_version="1.0.0",
            timeline_id=timeline_id,
            candidate_id=candidate.candidate_id,
            created_timestamp=current_timestamp
        )
        self._opened_timestamp = current_timestamp

    def append_snapshot(
        self,
        snapshot: EnvironmentSnapshot,
        frame_id: str,
        behavior_state: str,
        behavior_strength: str,
        metadata: Mapping[str, object]
    ) -> None:
        if self._timeline is None:
            raise WindowNotOpenError("Behavior Observation Window is not open.")
        if self._timeline.timeline_status() == "FROZEN":
            raise AppendAfterFreezeError("Cannot append after timeline is frozen.")
        if not isinstance(snapshot, EnvironmentSnapshot):
            raise InvalidSnapshotError("Appended snapshot must be an EnvironmentSnapshot.")

        try:
            frame = BehaviorFrame(
                schema_version="1.0.0",
                frame_id=frame_id,
                timeline_id=self._timeline._timeline_id,
                timestamp=snapshot.timestamp,
                environment_snapshot_id=snapshot.snapshot_id,
                behavior_state=behavior_state,
                behavior_strength=behavior_strength,
                metadata=metadata
            )
            self._timeline.append_frame(frame)
        except TimelineFreezeError as e:
            raise AppendAfterFreezeError(str(e)) from e
        except TimelineError as e:
            raise TimelineFailureError(str(e)) from e

    def evaluate_policy(
        self,
        current_timestamp: datetime,
        policy: ObservationPolicyContract
    ) -> ObservationDecision:
        if self._timeline is None or self._opened_timestamp is None:
            raise WindowNotOpenError("Behavior Observation Window is not open.")
        
        elapsed_duration = (current_timestamp - self._opened_timestamp).total_seconds()
        # elapsed_duration could theoretically be negative if current_timestamp < opened,
        # but policy validation will reject negative durations deterministically.

        return policy.evaluate(
            current_timestamp=current_timestamp,
            frame_count=self._timeline.frame_count(),
            elapsed_duration=elapsed_duration
        )

    def freeze(
        self,
        closed_timestamp: datetime,
        termination_reason: TerminationReason,
        timeline_metadata: Mapping[str, object] | None = None
    ) -> BOWResult:
        if self._timeline is None or self._opened_timestamp is None:
            raise WindowNotOpenError("Behavior Observation Window is not open.")
        if self._timeline.timeline_status() == "FROZEN":
            raise DoubleFreezeError("Behavior Observation Window is already frozen.")

        try:
            frozen_timeline = self._timeline.freeze(
                closed_timestamp=closed_timestamp,
                termination_reason=termination_reason.value,
                timeline_metadata=timeline_metadata
            )
        except TimelineFreezeError as e:
            raise DoubleFreezeError(str(e)) from e
        except TimelineError as e:
            raise TimelineFailureError(str(e)) from e

        elapsed_duration = (closed_timestamp - self._opened_timestamp).total_seconds()

        return BOWResult(
            timeline=frozen_timeline,
            termination_reason=termination_reason,
            frame_count=self._timeline.frame_count(),
            duration_seconds=elapsed_duration
        )

    def close(self) -> None:
        self._timeline = None
        self._opened_timestamp = None
