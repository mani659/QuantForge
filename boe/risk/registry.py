from typing import Tuple, Dict

from boe.risk.policy import RiskPolicyContract
from boe.risk.risk_errors import (
    RiskPolicyNotFound,
    DuplicateRiskPolicy,
    InvalidRiskPolicy
)

class RiskPolicyRegistry:
    """
    Registry for managing Risk Policies.
    It selects policies but DOES NOT evaluate risk or size positions.
    Follows Open/Closed Principle by allowing registration of new risk policies without modifying this class.
    Must be instantiated; no singleton/global mutable state.
    """
    
    def __init__(self, initial_policies: Tuple[RiskPolicyContract, ...] = ()):
        self._policies: Dict[str, RiskPolicyContract] = {}
        for policy in initial_policies:
            self.register(policy)
            
    def register(self, policy: RiskPolicyContract) -> None:
        if not isinstance(policy, RiskPolicyContract):
            raise InvalidRiskPolicy("Policy must implement RiskPolicyContract.")
            
        policy_name = policy.policy_name
        if not policy_name:
            raise InvalidRiskPolicy("Policy must provide a non-empty policy_name.")
            
        if policy_name in self._policies:
            raise DuplicateRiskPolicy(f"Policy '{policy_name}' is already registered.")
            
        self._policies[policy_name] = policy

    def get_policy(self, policy_name: str) -> RiskPolicyContract:
        if not policy_name:
            raise RiskPolicyNotFound("Policy name cannot be empty.")
            
        policy = self._policies.get(policy_name)
        if not policy:
            raise RiskPolicyNotFound(f"Policy '{policy_name}' not found in registry.")
            
        return policy

    def has_policy(self, policy_name: str) -> bool:
        return policy_name in self._policies

    @property
    def registered_policies(self) -> Tuple[str, ...]:
        """Returns a deterministic, sorted tuple of registered policy names."""
        return tuple(sorted(self._policies.keys()))
