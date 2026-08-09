"""Thin, offline MT5 request adapter for QuantForge Milestone 1."""

from typing import Any, Dict

from execution.trade_order import TradeOrder

from .trade_result import TradeResult


class MT5Adapter:
    """Translates valid TradeOrders into MT5 request dictionaries without connecting."""

    _SCHEMA_VERSION = "1.0"
    _ADAPTER_VERSION = "1.0.0"

    def translate_order(self, trade_order: TradeOrder) -> Dict[str, Any]:
        """Builds the MT5 DEAL request dictionary for a validated MARKET order."""
        self._validate_trade_order(trade_order)
        return {
            "action": "DEAL",
            "symbol": trade_order.instrument,
            "volume": trade_order.volume,
            "type": trade_order.direction,
            "comment": trade_order.comment,
        }

    def create_trade_result(self, trade_order: TradeOrder) -> TradeResult:
        """Creates the deterministic Milestone 1 placeholder response for testing."""
        self.translate_order(trade_order)
        return TradeResult(
            schema_version=self._SCHEMA_VERSION,
            trade_id=f"trade_{trade_order.order_id}",
            order_id=trade_order.order_id,
            timestamp=trade_order.timestamp,
            instrument=trade_order.instrument,
            direction=trade_order.direction,
            status="FILLED",
            requested_volume=trade_order.volume,
            filled_volume=trade_order.volume,
            entry_price=0.0,
            stop_loss=trade_order.stop_loss,
            take_profit=trade_order.take_profit,
            commission=0.0,
            swap=0.0,
            comment=trade_order.comment,
            broker="MetaTrader5",
            metadata={"adapter_version": self._ADAPTER_VERSION},
        )

    def _validate_trade_order(self, trade_order: TradeOrder) -> None:
        """Raises deterministic exceptions for invalid TradeOrder v1.0 inputs."""
        if not isinstance(trade_order, TradeOrder):
            raise ValueError("TradeOrder must be a TradeOrder instance.")
        if trade_order.schema_version != self._SCHEMA_VERSION:
            raise ValueError("Invalid TradeOrder schema version.")
        if not isinstance(trade_order.instrument, str) or not trade_order.instrument.strip():
            raise ValueError("TradeOrder instrument must be a non-empty string.")
        if trade_order.direction not in {"BUY", "SELL"}:
            raise ValueError("TradeOrder direction must be BUY or SELL.")
        if trade_order.order_type != "MARKET":
            raise ValueError("TradeOrder order type must be MARKET.")
        if not isinstance(trade_order.volume, (int, float)) or isinstance(trade_order.volume, bool) or trade_order.volume <= 0:
            raise ValueError("TradeOrder volume must be a positive number.")
        if not isinstance(trade_order.comment, str):
            raise ValueError("TradeOrder comment must be a string.")


MT5BrokerAdapter = MT5Adapter
