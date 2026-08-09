"""Balanced-policy extension point without research weighting."""

from dataclasses import dataclass

from .strict_policy import StrictPolicy


@dataclass(frozen=True)
class BalancedPolicy(StrictPolicy):
    """Immutable policy placeholder retaining strict behavior until research exists."""

    @property
    def policy_id(self) -> str:
        """Return the stable balanced policy identifier."""
        return "balanced"
