"""Deterministic factory for supported Hypothesis Engine decision policies."""

from .balanced_policy import BalancedPolicy
from .decision_policy_contract import DecisionPolicyContract
from .exploratory_policy import ExploratoryPolicy
from .strict_policy import StrictPolicy
from ..hypothesis_errors import DecisionPolicyError


class PolicyFactory:
    """Construct one supported immutable evidence policy from a stable name."""

    @staticmethod
    def create(policy_name: str = "default") -> DecisionPolicyContract:
        """Return the requested policy without reflection, plugins, or a registry."""
        if not isinstance(policy_name, str):
            raise DecisionPolicyError("Policy selection must be a string.")
        if policy_name in {"default", "strict"}:
            return StrictPolicy()
        if policy_name == "balanced":
            return BalancedPolicy()
        if policy_name == "exploratory":
            return ExploratoryPolicy()
        raise DecisionPolicyError(f"Unsupported decision policy: {policy_name}")
