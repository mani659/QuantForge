"""Deterministic errors for Hypothesis Engine contracts."""


class HypothesisError(ValueError):
    """Base error for a Hypothesis Engine contract violation."""


class DecisionPolicyError(HypothesisError):
    """Raised when a decision policy is invalid or violates its contract."""


class EvidenceError(HypothesisError):
    """Raised when validation evidence cannot be interpreted safely."""
