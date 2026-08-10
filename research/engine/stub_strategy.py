from typing import Dict, Any, Optional
from types import MappingProxyType

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.risk.specification import PositionSpecification

from research.engine.strategy_contract import ResearchStrategyContract


class MovingAverageCrossoverStrategy(ResearchStrategyContract):
    """
    A simple stub strategy for V1 testing of the Research Run Engine.
    Uses a naive short vs long moving average crossover logic on the 'close' price.
    """

    def __init__(self):
        self._short_window = 3
        self._long_window = 10
        
        self._history = []
        self._current_exposure = 0.0

    @property
    def strategy_id(self) -> str:
        return "ma_crossover_stub"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, parameters: Dict[str, Any]) -> None:
        self._short_window = parameters.get("short_window", 3)
        self._long_window = parameters.get("long_window", 10)
        self.reset()

    def reset(self) -> None:
        self._history.clear()
        self._current_exposure = 0.0

    def on_snapshot(self, snapshot: EnvironmentSnapshot) -> Optional[PositionSpecification]:
        # Extract price
        price = snapshot.market_state.get("close")
        if price is None:
            return None
            
        self._history.append(price)
        
        # Keep only what we need
        if len(self._history) > self._long_window:
            self._history.pop(0)
            
        if len(self._history) < self._long_window:
            # Not enough data
            return None
            
        short_ma = sum(self._history[-self._short_window:]) / self._short_window
        long_ma = sum(self._history) / self._long_window
        
        target_exposure = 0.0
        if short_ma > long_ma:
            target_exposure = 1.0  # Go long
        elif short_ma < long_ma:
            target_exposure = -1.0 # Go short
            
        if target_exposure != self._current_exposure:
            self._current_exposure = target_exposure
            
            return PositionSpecification(
                candidate_id=f"run_{self.strategy_id}",
                timeline_id=snapshot.snapshot_id,
                observation_id=f"obs_{snapshot.snapshot_id}",
                schema_version="1.0.0",
                exposure_fraction=target_exposure,
                position_size_multiplier=1.0,
                risk_units=1.0,
                metadata=MappingProxyType({"reason": "crossover"}),
                timestamp=snapshot.timestamp
            )
            
        return None
