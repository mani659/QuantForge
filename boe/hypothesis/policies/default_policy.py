"""Default decision-policy compatibility alias."""

from .strict_policy import StrictPolicy


DefaultPolicy = StrictPolicy

__all__ = ["DefaultPolicy"]
