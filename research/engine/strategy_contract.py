from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.risk.specification import PositionSpecification

class ResearchStrategyContract(ABC):
    """
    Minimal contract for a strategy running inside the Research Engine.
    
    A Research Strategy:
    - Receives only causally available information (EnvironmentSnapshot).
    - Returns a PositionSpecification (what exposure it wants) or None.
    - Manages its own internal state (indicators, regimes).
    - Can be deterministically reset.
    """

    @property
    @abstractmethod
    def strategy_id(self) -> str:
        """The identity/name of the strategy."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """The version of the strategy logic."""
        pass

    @abstractmethod
    def initialize(self, parameters: Dict[str, Any]) -> None:
        """
        Configure the strategy before a run.
        This is where PRNG seeds, lookback lengths, and thresholds are set.
        """
        pass

    @abstractmethod
    def on_snapshot(self, snapshot: EnvironmentSnapshot) -> Optional[PositionSpecification]:
        """
        Process a single historical snapshot.
        Must not access future data.
        Returns a PositionSpecification describing the desired exposure, or None to maintain current state.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Clear all internal state (rolling windows, indicators, trade state).
        Ensures strict isolation between runs.
        """
        pass
