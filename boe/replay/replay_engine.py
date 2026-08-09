"""Deterministic implementation of the Replay Engine."""

from boe.temporal.environment_repository_contract import EnvironmentRepositoryContract
from boe.temporal.timeline_repository_contract import TimelineRepositoryContract
from boe.temporal.frozen_behavior_timeline import FrozenBehaviorTimeline

from boe.replay.replay_engine_contract import ReplayEngineContract
from boe.replay.replay_cursor import ReplayCursor
from boe.replay.replay_result import ReplayResult
from boe.replay.replay_state import ReplayState
from boe.replay.replay_errors import (
    MissingTimelineError,
    MissingSnapshotError,
    ReplayNotLoadedError,
    ReplayAlreadyCompleteError,
    RepositoryFailureError
)


class ReplayEngine(ReplayEngineContract):
    """Strictly deterministic replay engine."""

    def __init__(
        self,
        timeline_repository: TimelineRepositoryContract,
        environment_repository: EnvironmentRepositoryContract
    ) -> None:
        self._timeline_repo = timeline_repository
        self._env_repo = environment_repository
        
        self._timeline: FrozenBehaviorTimeline | None = None
        self._position: int = 0
        self._status: ReplayState | None = None

    def load(self, timeline_id: str) -> None:
        try:
            self._timeline = self._timeline_repo.load(timeline_id)
        except Exception as e:
            raise MissingTimelineError(f"Failed to load timeline {timeline_id}: {str(e)}") from e
        
        if self._timeline is None:
            raise MissingTimelineError(f"Timeline {timeline_id} not found.")

        self._position = 0
        self._status = ReplayState.LOADED

    def start(self) -> None:
        if self._timeline is None or self._status is None:
            raise ReplayNotLoadedError("Replay Engine is not loaded.")
        
        self._position = 0
        self._status = ReplayState.PLAYING if len(self._timeline.frames) > 0 else ReplayState.COMPLETE

    def step(self) -> ReplayCursor:
        if self._timeline is None or self._status is None:
            raise ReplayNotLoadedError("Replay Engine is not loaded.")
        
        if self._status == ReplayState.COMPLETE or self._position >= len(self._timeline.frames):
            raise ReplayAlreadyCompleteError("Replay is already complete.")
        
        frame = self._timeline.frames[self._position]
        
        try:
            snapshot = self._env_repo.load(frame.environment_snapshot_id)
        except Exception as e:
            raise MissingSnapshotError(f"Failed to load snapshot {frame.environment_snapshot_id}: {str(e)}") from e
            
        if snapshot is None:
            raise MissingSnapshotError(f"Snapshot {frame.environment_snapshot_id} not found.")

        self._position += 1
        if self._position >= len(self._timeline.frames):
            self._status = ReplayState.COMPLETE
        
        return ReplayCursor(
            position=self._position - 1,
            total_frames=len(self._timeline.frames),
            status=self._status,
            current_frame=frame,
            current_snapshot=snapshot
        )

    def restart(self) -> None:
        if self._timeline is None or self._status is None:
            raise ReplayNotLoadedError("Replay Engine is not loaded.")
        
        self._position = 0
        self._status = ReplayState.PLAYING if len(self._timeline.frames) > 0 else ReplayState.COMPLETE

    def replay_all(self) -> tuple[ReplayCursor, ...]:
        if self._timeline is None or self._status is None:
            raise ReplayNotLoadedError("Replay Engine is not loaded.")
            
        cursors = []
        while self._status != ReplayState.COMPLETE:
            cursors.append(self.step())
            
        return tuple(cursors)

    def finish(self) -> ReplayResult:
        if self._timeline is None or self._status is None:
            raise ReplayNotLoadedError("Replay Engine is not loaded.")
            
        self._status = ReplayState.COMPLETE
        
        return ReplayResult(
            timeline_id=self._timeline.timeline_id,
            frames_processed=self._position,
            status=self._status
        )
