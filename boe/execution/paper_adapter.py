from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Dict, List

from boe.temporal.environment_snapshot import EnvironmentSnapshot
from boe.execution.broker_adapter_contract import BrokerAdapterContract, BrokerAdapterConfig
from boe.execution.result import ExecutionResult, ExecutionStatus
from boe.risk.specification import PositionSpecification
from boe.execution.execution_errors import (
    PaperTradingError,
    PaperConfigurationError,
    InvalidPaperExecution,
    PaperAccountError
)

@dataclass
class PaperTradingAccount:
    """Maintains the virtual state of the paper trading broker."""
    balance: float = 100000.0
    equity: float = 100000.0
    realised_pnl: float = 0.0
    unrealised_pnl: float = 0.0
    open_positions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    closed_positions: List[Dict[str, Any]] = field(default_factory=list)
    current_price: float = 100.0

    def update_market_price(self, price: float):
        if price <= 0:
            raise PaperAccountError("Market price must be positive.")
        self.current_price = price
        self._recalculate_equity()

    def _recalculate_equity(self):
        self.unrealised_pnl = 0.0
        for pos in self.open_positions.values():
            if pos["direction"] == "BUY":
                self.unrealised_pnl += (self.current_price - pos["entry_price"]) * pos["volume"]
            elif pos["direction"] == "SELL":
                self.unrealised_pnl += (pos["entry_price"] - self.current_price) * pos["volume"]
        self.equity = self.balance + self.unrealised_pnl

    def execute_trade(self, candidate_id: str, new_exposure: float) -> Dict[str, Any]:
        """
        Deterministically applies a new exposure. 
        """
        target_direction = "NONE" if new_exposure == 0.0 else ("BUY" if new_exposure > 0 else "SELL")
        target_volume = (self.equity * abs(new_exposure)) / self.current_price
        
        current_pos = self.open_positions.get(candidate_id)
        current_volume = current_pos["volume"] if current_pos else 0.0
        current_direction = current_pos["direction"] if current_pos else "NONE"
        current_entry_price = current_pos["entry_price"] if current_pos else 0.0

        if target_direction == current_direction and abs(target_volume - current_volume) < 1e-9:
            return {
                "account_balance": self.balance,
                "open_exposure": new_exposure,
                "leg_count": 1,
                "leg_0_action": "NONE",
                "leg_0_direction": "NONE",
                "leg_0_volume": 0.0,
                "leg_0_price": self.current_price,
                "leg_0_realized_pnl": 0.0
            }

        legs = []

        if current_volume > 0 and current_direction != target_direction:
            # Full close of existing position
            pnl = (self.current_price - current_entry_price) * current_volume if current_direction == "BUY" else (current_entry_price - self.current_price) * current_volume
            self.realised_pnl += pnl
            self.balance += pnl
            self.closed_positions.append({
                "candidate_id": candidate_id,
                "volume": current_volume,
                "close_price": self.current_price,
                "pnl": pnl,
                "direction": current_direction
            })
            del self.open_positions[candidate_id]
            legs.append({"action": "CLOSE", "direction": current_direction, "volume": current_volume, "price": self.current_price, "realized_pnl": pnl})
            current_volume = 0.0
            current_direction = "NONE"
            current_entry_price = 0.0

        if current_volume > target_volume + 1e-9 and target_direction == current_direction:
            # Partial Close
            closed_vol = current_volume - target_volume
            pnl = (self.current_price - current_entry_price) * closed_vol if current_direction == "BUY" else (current_entry_price - self.current_price) * closed_vol
            self.realised_pnl += pnl
            self.balance += pnl
            self.closed_positions.append({
                "candidate_id": candidate_id,
                "volume": closed_vol,
                "close_price": self.current_price,
                "pnl": pnl,
                "direction": current_direction
            })
            self.open_positions[candidate_id]["volume"] = target_volume
            legs.append({"action": "REDUCE", "direction": current_direction, "volume": closed_vol, "price": self.current_price, "realized_pnl": pnl})
            
        elif target_volume > current_volume + 1e-9 and (target_direction == current_direction or current_direction == "NONE"):
            # Increase or New Position
            added_vol = target_volume - current_volume
            new_entry_price = self.current_price if current_volume == 0.0 else ((current_entry_price * current_volume) + (self.current_price * added_vol)) / target_volume
            self.open_positions[candidate_id] = {
                "volume": target_volume,
                "entry_price": new_entry_price,
                "direction": target_direction,
                "exposure_fraction": new_exposure
            }
            legs.append({"action": target_direction, "direction": target_direction, "volume": added_vol, "price": self.current_price, "realized_pnl": 0.0})
            
        elif target_direction != "NONE" and current_direction == "NONE":
            # Reversal side (after close)
            self.open_positions[candidate_id] = {
                "volume": target_volume,
                "entry_price": self.current_price,
                "direction": target_direction,
                "exposure_fraction": new_exposure
            }
            legs.append({"action": target_direction, "direction": target_direction, "volume": target_volume, "price": self.current_price, "realized_pnl": 0.0})
             
        self._recalculate_equity()
             
        res = {
            "account_balance": self.balance,
            "open_exposure": new_exposure,
            "leg_count": len(legs)
        }
        for i, leg in enumerate(legs):
            res[f"leg_{i}_action"] = leg["action"]
            res[f"leg_{i}_direction"] = leg["direction"]
            res[f"leg_{i}_volume"] = leg["volume"]
            res[f"leg_{i}_price"] = leg["price"]
            res[f"leg_{i}_realized_pnl"] = leg["realized_pnl"]
            
        return res


@dataclass(frozen=True)
class PaperTradingAdapterConfig(BrokerAdapterConfig):
    """Immutable Paper Trading Adapter specific configuration."""
    pass

class PaperTradingAdapter(BrokerAdapterContract):
    """
    Virtual broker that tracks state (balance, positions) continuously.
    Does not communicate with any external broker or network.
    """
    def __init__(self, config: PaperTradingAdapterConfig):
        if not isinstance(config, PaperTradingAdapterConfig):
            raise PaperConfigurationError("config must be a PaperTradingAdapterConfig")
            
        self._config = config
        self._account = PaperTradingAccount()

    @property
    def config(self) -> PaperTradingAdapterConfig:
        return self._config
        
    @property
    def account(self) -> PaperTradingAccount:
        return self._account

    def update_market_state(self, snapshot: EnvironmentSnapshot):
        if not isinstance(snapshot, EnvironmentSnapshot):
            raise PaperAccountError("Invalid snapshot type.")
        if "close" in snapshot.market_state:
            self._account.update_market_price(snapshot.market_state["close"])

    def dispatch(self, specification: PositionSpecification) -> ExecutionResult:
        if not isinstance(specification, PositionSpecification):
            raise InvalidPaperExecution("PaperTradingAdapter can only execute PositionSpecifications")
            
        try:
            trade_details = self._account.execute_trade(
                candidate_id=specification.candidate_id,
                new_exposure=specification.exposure_fraction
            )
            
            # Deterministic paper trading metadata
            metadata = {
                "ticket": f"paper_{hash(specification.candidate_id) % 4294967295}",
                **trade_details
            }
            
            return ExecutionResult(
                candidate_id=specification.candidate_id,
                timeline_id=specification.timeline_id,
                observation_id=specification.observation_id,
                schema_version=specification.schema_version,
                status=ExecutionStatus.SUCCESS,
                metadata=MappingProxyType(metadata),
                timestamp=specification.timestamp
            )
        except Exception as e:
            # Trap any internal account errors and wrap them in an ExecutionResult
            return ExecutionResult(
                candidate_id=specification.candidate_id,
                timeline_id=specification.timeline_id,
                observation_id=specification.observation_id,
                schema_version=specification.schema_version,
                status=ExecutionStatus.FAILED,
                metadata=MappingProxyType({"error": str(e)}),
                timestamp=specification.timestamp
            )
