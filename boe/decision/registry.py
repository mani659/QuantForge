from typing import Tuple, Dict

from boe.decision.policy import DecisionPolicyContract
from boe.decision.decision_errors import (
    DecisionPolicyNotFound,
    DuplicateDecisionPolicy,
    InvalidDecisionPolicy
)

class DecisionRegistry:
    """
    Registry for managing Decision Policies.
    It selects policies but DOES NOT make decisions itself.
    Follows Open/Closed Principle by allowing registration of new policies without modifying this class.
    Must be instantiated; no singleton/global mutable state.
    """
    
    def __init__(self, initial_policies: Tuple[DecisionPolicyContract, ...] = ()):
        self._policies: Dict[str, DecisionPolicyContract] = {}
        for policy in initial_policies:
            self.register(policy)
            
    def register(self, policy: DecisionPolicyContract) -> None:
        if not isinstance(policy, DecisionPolicyContract):
            raise InvalidDecisionPolicy("Policy must implement DecisionPolicyContract.")
            
        policy_name = policy.policy_name
        if not policy_name:
            raise InvalidDecisionPolicy("Policy must provide a non-empty policy_name.")
            
        if policy_name in self._policies:
            raise DuplicateDecisionPolicy(f"Policy '{policy_name}' is already registered.")
            
        self._policies[policy_name] = policy

    def get_policy(self, policy_name: str) -> DecisionPolicyContract:
        if not policy_name:
            raise DecisionPolicyNotFound("Policy name cannot be empty.")
            
        policy = self._policies.get(policy_name)
        if not policy:
            raise DecisionPolicyNotFound(f"Policy '{policy_name}' not found in registry.")
            
        return policy

    def has_policy(self, policy_name: str) -> bool:
        return policy_name in self._policies

    @property
    def registered_policies(self) -> Tuple[str, ...]:
        """Returns a deterministic, sorted tuple of registered policy names."""
        return tuple(sorted(self._policies.keys()))
