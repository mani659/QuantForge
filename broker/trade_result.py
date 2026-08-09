"""Immutable TradeResult contract for the QuantForge MT5 adapter."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class TradeResult:
    """A broker-neutral representation of an MT5 adapter response."""

    schema_version: str
    trade_id: str
    order_id: str
    timestamp: str
    instrument: str
    direction: str
    status: str
    requested_volume: float
    filled_volume: float
    entry_price: float
    stop_loss: float | None
    take_profit: float | None
    commission: float
    swap: float
    comment: str
    broker: str
    metadata: Mapping[str, str]

    def __post_init__(self) -> None:
        """Protect metadata from mutation after result creation."""
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def to_dict(self) -> dict[str, Any]:
        """Returns the serializable TradeResult v1.0 schema."""
        return {
            "schema_version": self.schema_version,
            "trade_id": self.trade_id,
            "order_id": self.order_id,
            "timestamp": self.timestamp,
            "instrument": self.instrument,
            "direction": self.direction,
            "status": self.status,
            "requested_volume": self.requested_volume,
            "filled_volume": self.filled_volume,
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "commission": self.commission,
            "swap": self.swap,
            "comment": self.comment,
            "broker": self.broker,
            "metadata": dict(self.metadata),
        }
