from dataclasses import dataclass
from datetime import datetime


class OperationalGovernanceError(Exception):
    """Base exception for the Operational Governance domain."""
    pass


class InvalidOperationalAuthorizationData(OperationalGovernanceError):
    """Raised when an OperationalAuthorization is instantiated with invalid data."""
    pass


@dataclass(frozen=True)
class OperationalAuthorization:
    """Immutable operational authorization fact for QuantForge.

    Represents the single permanent operational fact: an immutable record that 
    a specific, validated StrategyManifest was operationally cleared by an 
    identified human operator for a specific runtime deployment identity, 
    at a recorded time.
    """
    strategy_manifest_id: str
    deployment_identity: str
    operator_identity: str
    authorized_at: datetime

    def __post_init__(self) -> None:
        """Validate all fields at construction time."""
        if not isinstance(self.strategy_manifest_id, str) or not self.strategy_manifest_id.strip():
            raise InvalidOperationalAuthorizationData("strategy_manifest_id must be a non-empty string.")
        
        if not isinstance(self.deployment_identity, str) or not self.deployment_identity.strip():
            raise InvalidOperationalAuthorizationData("deployment_identity must be a non-empty string.")
        
        if not isinstance(self.operator_identity, str) or not self.operator_identity.strip():
            raise InvalidOperationalAuthorizationData("operator_identity must be a non-empty string.")
        
        if not isinstance(self.authorized_at, datetime):
            raise InvalidOperationalAuthorizationData("authorized_at must be a valid datetime.")

