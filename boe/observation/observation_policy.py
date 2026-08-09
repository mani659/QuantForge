"""Default deterministic Observation Policy implementation."""

from datetime import datetime

from .observation_config import ObservationConfig
from .observation_contract import ObservationPolicyContract
from .observation_errors import ObservationPolicyValidationError
from .observation_result import ObservationDecision
from .termination_reason import TerminationReason


class DefaultObservationPolicy(ObservationPolicyContract):
    """Deterministic observation lifecycle policy.

    Terminates observation when either the configured maximum frame count
    or the configured maximum duration is reached.  Otherwise, observation
    continues.

    No market intelligence, heuristics, or behavioral interpretation
    is performed.
    """

    _POLICY_ID: str = "default_observation_policy"
    _POLICY_VERSION: str = "1.0.0"

    def __init__(self, config: ObservationConfig) -> None:
        if not isinstance(config, ObservationConfig):
            raise ObservationPolicyValidationError(
                "DefaultObservationPolicy requires an ObservationConfig instance."
            )
        self._config = config

    @property
    def policy_id(self) -> str:
        """Return the stable identifier for the default observation policy."""
        return self._POLICY_ID

    @property
    def policy_version(self) -> str:
        """Return the semantic version for the default observation policy."""
        return self._POLICY_VERSION

    @property
    def config(self) -> ObservationConfig:
        """Return the immutable configuration governing this policy."""
        return self._config

    def evaluate(
        self,
        current_timestamp: datetime,
        frame_count: int,
        elapsed_duration: float,
    ) -> ObservationDecision:
        """Evaluate whether observation should continue or terminate.

        Termination occurs when either configured limit is reached:
        - frame_count >= config.max_frames  → WINDOW_COMPLETE
        - elapsed_duration >= config.max_duration → MAX_DURATION

        Frame count is checked first for deterministic priority.
        """
        if not isinstance(current_timestamp, datetime):
            raise ObservationPolicyValidationError(
                "current_timestamp must be a datetime."
            )
        if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count < 0:
            raise ObservationPolicyValidationError(
                "frame_count must be a non-negative integer."
            )
        if not isinstance(elapsed_duration, (int, float)) or isinstance(elapsed_duration, bool) or elapsed_duration < 0.0:
            raise ObservationPolicyValidationError(
                "elapsed_duration must be a non-negative number."
            )

        if frame_count >= self._config.max_frames:
            return ObservationDecision(
                continue_observation=False,
                terminate_observation=True,
                termination_reason=TerminationReason.WINDOW_COMPLETE,
                policy_id=self._POLICY_ID,
                policy_version=self._POLICY_VERSION,
                timestamp=current_timestamp,
            )

        if elapsed_duration >= self._config.max_duration:
            return ObservationDecision(
                continue_observation=False,
                terminate_observation=True,
                termination_reason=TerminationReason.MAX_DURATION,
                policy_id=self._POLICY_ID,
                policy_version=self._POLICY_VERSION,
                timestamp=current_timestamp,
            )

        return ObservationDecision(
            continue_observation=True,
            terminate_observation=False,
            termination_reason=None,
            policy_id=self._POLICY_ID,
            policy_version=self._POLICY_VERSION,
            timestamp=current_timestamp,
        )
