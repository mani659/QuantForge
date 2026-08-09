"""Deterministic factory for supported Observation Policy implementations."""

from .observation_config import ObservationConfig
from .observation_contract import ObservationPolicyContract
from .observation_errors import ObservationPolicyError
from .observation_policy import DefaultObservationPolicy


class ObservationPolicyFactory:
    """Construct one supported observation policy from a stable name.

    No reflection, plugins, or registry loading.
    """

    @staticmethod
    def create(
        policy_name: str = "default",
        config: ObservationConfig | None = None,
    ) -> ObservationPolicyContract:
        """Return the requested observation policy.

        Parameters
        ----------
        policy_name:
            Stable policy name.  Currently supported: ``"default"``.
        config:
            Immutable external configuration.  Required for all current policies.

        Raises
        ------
        ObservationPolicyError
            If the policy name is not a string or is unsupported.
        ObservationPolicyError
            If config is not supplied.
        """
        if not isinstance(policy_name, str):
            raise ObservationPolicyError("Policy selection must be a string.")
        if config is None:
            raise ObservationPolicyError(
                "ObservationConfig is required for observation policy creation."
            )

        if policy_name == "default":
            return DefaultObservationPolicy(config)

        raise ObservationPolicyError(
            f"Unsupported observation policy: {policy_name}"
        )
