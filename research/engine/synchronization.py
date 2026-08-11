import abc
from typing import Any

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.execution.contract import ExecutionEngineContract, ExecutionConfig
from boe.risk.specification import PositionSpecification


class MarketStateSynchronizerContract(abc.ABC):
    """
    Public interface for synchronizing market state to a downstream environment 
    (e.g., a simulation broker adapter) without exposing execution engine internals.
    """
    @abc.abstractmethod
    def sync_market_state(self, snapshot: EnvironmentSnapshot) -> None:
        pass


class NullMarketStateSynchronizer(MarketStateSynchronizerContract):
    """
    A no-op synchronizer for live execution or adapters that don't need explicit MTM state sync.
    """
    def sync_market_state(self, snapshot: EnvironmentSnapshot) -> None:
        pass


class AdapterMarketStateSynchronizer(MarketStateSynchronizerContract):
    """
    Synchronizes market state directly into an adapter that supports it.
    This encapsulates the adapter dependency so ResearchRunEngine only sees the interface.
    """
    def __init__(self, adapter: Any):
        self._adapter = adapter
        
    def sync_market_state(self, snapshot: EnvironmentSnapshot) -> None:
        if hasattr(self._adapter, "update_market_state"):
            self._adapter.update_market_state(snapshot)


class SynchronizedExecutionEngine(ExecutionEngineContract, MarketStateSynchronizerContract):
    """
    Decorator that bundles an ExecutionEngineContract with a MarketStateSynchronizerContract.
    This preserves the V1 signature Callable[[], ExecutionEngineContract] while 
    transparently providing market state synchronization.
    """
    def __init__(self, engine: ExecutionEngineContract, synchronizer: MarketStateSynchronizerContract):
        self._engine = engine
        self._synchronizer = synchronizer
        
    @property
    def config(self) -> ExecutionConfig:
        return self._engine.config
        
    def execute(self, specification: PositionSpecification) -> Any:
        return self._engine.execute(specification)
        
    def sync_market_state(self, snapshot: EnvironmentSnapshot) -> None:
        self._synchronizer.sync_market_state(snapshot)
