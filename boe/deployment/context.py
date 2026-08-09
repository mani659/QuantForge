from dataclasses import dataclass
from boe.strategy.strategy_contract import StrategyContract
from boe.interpretation.models import InterpretationModelContract
from boe.decision.policy import DecisionPolicyContract
from boe.risk.policy import RiskPolicyContract

class DeploymentConfigurationError(Exception):
    pass

@dataclass(frozen=True)
class DeploymentContext:
    """
    Immutable representation of a deployed strategy configuration.
    Stores references to the exact pipeline components assembled for execution.
    Contains no market data, runtime state, or orchestration.
    """
    strategy_manifest: StrategyContract
    interpretation_model: InterpretationModelContract
    decision_policy: DecisionPolicyContract
    risk_policy: RiskPolicyContract
    
    def __post_init__(self):
        if not isinstance(self.strategy_manifest, StrategyContract):
            raise DeploymentConfigurationError("strategy_manifest must implement StrategyContract")
        if not isinstance(self.interpretation_model, InterpretationModelContract):
            raise DeploymentConfigurationError("interpretation_model must implement InterpretationModelContract")
        if not isinstance(self.decision_policy, DecisionPolicyContract):
            raise DeploymentConfigurationError("decision_policy must implement DecisionPolicyContract")
        if not isinstance(self.risk_policy, RiskPolicyContract):
            raise DeploymentConfigurationError("risk_policy must implement RiskPolicyContract")
