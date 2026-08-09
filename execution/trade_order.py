"""Immutable TradeOrder contract for QuantForge Execution Engine v1.0."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class TradeOrder:
    """A validated broker-independent order ready for a future broker adapter."""

    schema_version: str
    order_id: str
    timestamp: str
    instrument: str
    timeframe: str
    direction: str
    order_type: str
    volume: float | None
    stop_loss: float | None
    take_profit: float | None
    comment: str
    status: str
    metadata: Mapping[str, str]

    def __post_init__(self) -> None:
        """Prevent mutation through the metadata mapping after construction."""
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def to_dict(self) -> dict[str, Any]:
        """Returns a serializable representation matching the TradeOrder schema."""
        return {
            "schema_version": self.schema_version,
            "order_id": self.order_id,
            "timestamp": self.timestamp,
            "instrument": self.instrument,
            "timeframe": self.timeframe,
            "direction": self.direction,
            "order_type": self.order_type,
            "volume": self.volume,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "comment": self.comment,
            "status": self.status,
            "metadata": dict(self.metadata),
        }
