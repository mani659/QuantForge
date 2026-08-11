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


class AdapterMarketStateSynchronizer(MarketStateSynchronizerContract):
    """
    Synchronizes market state directly into an adapter that supports it.
    This encapsulates the adapter dependency so ResearchRunEngine only sees the interface.
    """
    def __init__(self, adapter: Any):
        if not hasattr(adapter, "update_market_state"):
            raise ValueError("Adapter does not support market-state synchronization")
        self._adapter = adapter
        
    def sync_market_state(self, snapshot: EnvironmentSnapshot) -> None:
        self._adapter.update_market_state(snapshot)
