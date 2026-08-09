"""
Deployment Bootstrap
Application entry point that wires completed deployment components into a runnable pipeline.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

from boe.strategy.strategy_contract import StrategyContract
from boe.interpretation.registry import InterpretationRegistry
from boe.decision.registry import DecisionRegistry
from boe.risk.registry import RiskPolicyRegistry
from boe.behavior_detector_contract import BehaviorDetectorContract
from boe.evidence.observer_contract import ObserverContract
from boe.profile.engine import BehaviourProfileEngine
from boe.risk.models import RiskModelContract
from boe.risk.position_sizer import PositionSizerContract
from boe.execution.contract import ExecutionEngineContract

from boe.deployment.assembler import DeploymentAssembler
from boe.deployment.orchestrator import DeploymentOrchestrator
from boe.deployment.market_adapter import GenericMarketDataAdapter, MarketDataAdapterContract
from boe.deployment.paper_runner import PaperTradingRunner


class DeploymentBootstrapError(Exception):
    """Base exception for bootstrap failure."""
    pass


@dataclass(frozen=True)
class DeploymentConfiguration:
    """Configuration specific to the deployed environment."""
    schema_version: str = "1.0.0"
    market_adapter_source: str = "bootstrap_feed"


@dataclass(frozen=True)
class DeploymentRegistries:
    """Container for required policy and interpretation registries."""
    interpretation: InterpretationRegistry
    decision: DecisionRegistry
    risk: RiskPolicyRegistry
    strategies: Dict[str, StrategyContract]


@dataclass(frozen=True)
class DeploymentDependencies:
    """Container for required runtime engines and models."""
    detector: BehaviorDetectorContract
    observers: Tuple[ObserverContract, ...]
    profile_engine: BehaviourProfileEngine
    risk_model: RiskModelContract
    position_sizer: PositionSizerContract
    execution_engine: ExecutionEngineContract


@dataclass(frozen=True)
class DeployedPipeline:
    """The final assembled pipeline ready for execution."""
    market_adapter: MarketDataAdapterContract
    runner: PaperTradingRunner


class DeploymentBootstrap:
    """
    Assembles a complete, immutable deployment pipeline from existing frozen components.
    Owns no business, market, or execution logic.
    """

    @staticmethod
    def create(
        strategy_id: str,
        config: DeploymentConfiguration,
        registries: DeploymentRegistries,
        dependencies: DeploymentDependencies
    ) -> DeployedPipeline:
        """
        Constructs the entire deployment hierarchy for a given strategy.
        
        Args:
            strategy_id: Identity of the strategy to deploy.
            config: Deployment configuration settings.
            registries: Populated registry instances for dynamic resolution.
            dependencies: Injected core BOE engines.
            
        Returns:
            DeployedPipeline: Fully wired adapter and runner.
            
        Raises:
            DeploymentBootstrapError: If registries are missing, strategy is invalid,
                or component assembly fails.
        """
        if not isinstance(strategy_id, str):
            raise DeploymentBootstrapError("strategy_id must be a string")
        if not isinstance(config, DeploymentConfiguration):
            raise DeploymentBootstrapError("config must be a DeploymentConfiguration")
        if not isinstance(registries, DeploymentRegistries):
            raise DeploymentBootstrapError("registries must be a DeploymentRegistries")
        if not isinstance(dependencies, DeploymentDependencies):
            raise DeploymentBootstrapError("dependencies must be a DeploymentDependencies")

        strategy = registries.strategies.get(strategy_id)
        if not strategy:
            raise DeploymentBootstrapError(f"Strategy '{strategy_id}' not found in provided strategies registry.")

        try:
            # 1. Assemble Runtime Policies
            assembler = DeploymentAssembler(
                interpretation_registry=registries.interpretation,
                decision_registry=registries.decision,
                risk_registry=registries.risk
            )
            runtime = assembler.assemble(strategy_manifest=strategy)

            # 2. Construct Orchestrator
            orchestrator = DeploymentOrchestrator(
                runtime=runtime,
                detector=dependencies.detector,
                observers=dependencies.observers,
                profile_engine=dependencies.profile_engine,
                risk_model=dependencies.risk_model,
                position_sizer=dependencies.position_sizer
            )

            # 3. Construct Market Data Adapter
            market_adapter = GenericMarketDataAdapter(
                schema_version=config.schema_version,
                source=config.market_adapter_source
            )

            # 4. Construct Paper Trading Runner
            runner = PaperTradingRunner(
                orchestrator=orchestrator,
                execution_engine=dependencies.execution_engine
            )

            return DeployedPipeline(
                market_adapter=market_adapter,
                runner=runner
            )

        except Exception as e:
            if isinstance(e, DeploymentBootstrapError):
                raise
            raise DeploymentBootstrapError(f"Bootstrap assembly failed: {str(e)}") from e
