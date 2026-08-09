from boe.strategy.strategy_contract import StrategyContract
from boe.interpretation.registry import InterpretationRegistry
from boe.decision.registry import DecisionRegistry
from boe.risk.registry import RiskPolicyRegistry
from boe.deployment.context import DeploymentContext, DeploymentConfigurationError
from boe.deployment.runtime import DeploymentRuntime

class DeploymentAssembler:
    """
    Assembles a DeploymentRuntime by resolving a StrategyManifest against
    the Interpretation, Decision, and Risk registries.
    No execution, orchestration, or candidate processing occurs here.
    Assembly is strictly deterministic.
    """
    
    def __init__(
        self,
        interpretation_registry: InterpretationRegistry,
        decision_registry: DecisionRegistry,
        risk_registry: RiskPolicyRegistry
    ):
        if not isinstance(interpretation_registry, InterpretationRegistry):
            raise DeploymentConfigurationError("interpretation_registry must be an InterpretationRegistry")
        if not isinstance(decision_registry, DecisionRegistry):
            raise DeploymentConfigurationError("decision_registry must be a DecisionRegistry")
        if not isinstance(risk_registry, RiskPolicyRegistry):
            raise DeploymentConfigurationError("risk_registry must be a RiskPolicyRegistry")
            
        self._interpretation_registry = interpretation_registry
        self._decision_registry = decision_registry
        self._risk_registry = risk_registry

    def assemble(self, strategy_manifest: StrategyContract) -> DeploymentRuntime:
        """
        Resolves components using the manifest and returns an assembled runtime.
        """
        if not isinstance(strategy_manifest, StrategyContract):
            raise DeploymentConfigurationError("strategy_manifest must be a StrategyContract")
            
        interpretation_model = self._interpretation_registry.get_model(
            strategy_manifest.interpretation_model_id
        )
        decision_policy = self._decision_registry.get_policy(
            strategy_manifest.decision_policy_id
        )
        risk_policy = self._risk_registry.get_policy(
            strategy_manifest.risk_policy_id
        )
        
        context = DeploymentContext(
            strategy_manifest=strategy_manifest,
            interpretation_model=interpretation_model,
            decision_policy=decision_policy,
            risk_policy=risk_policy
        )
        
        return DeploymentRuntime(context)
