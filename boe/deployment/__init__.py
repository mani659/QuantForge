"""
Phase 7 Deployment Layer (FROZEN)
Wires existing frozen components together to reduce the distance between
validated research and paper trading without introducing market logic.
"""

from boe.deployment.context import DeploymentContext
from boe.deployment.runtime import DeploymentRuntime
from boe.deployment.assembler import DeploymentAssembler
from boe.deployment.orchestrator import DeploymentOrchestrator
from boe.deployment.market_adapter import MarketDataAdapterContract, GenericMarketDataAdapter
from boe.deployment.paper_runner import PaperTradingRunner, RunnerResult
from boe.deployment.bootstrap import (
    DeploymentBootstrap, 
    DeployedPipeline, 
    DeploymentConfiguration, 
    DeploymentRegistries, 
    DeploymentDependencies
)

__all__ = [
    "DeploymentContext",
    "DeploymentRuntime",
    "DeploymentAssembler",
    "DeploymentOrchestrator",
    "MarketDataAdapterContract",
    "GenericMarketDataAdapter",
    "PaperTradingRunner",
    "RunnerResult",
    "DeploymentBootstrap",
    "DeployedPipeline",
    "DeploymentConfiguration",
    "DeploymentRegistries",
    "DeploymentDependencies"
]
