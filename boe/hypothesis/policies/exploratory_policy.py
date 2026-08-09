"""Exploratory-policy extension point without probabilistic behavior."""

from dataclasses import dataclass

from .strict_policy import StrictPolicy


@dataclass(frozen=True)
class ExploratoryPolicy(StrictPolicy):
    """Immutable policy placeholder retaining strict behavior until research exists."""

    @property
    def policy_id(self) -> str:
        """Return the stable exploratory policy identifier."""
        return "exploratory"
