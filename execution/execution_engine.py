"""QuantForge Execution Engine v1.0: deterministic TradePlan-to-TradeOrder mapping."""

from typing import Any, Dict

from .trade_order import TradeOrder


class ExecutionEngine:
    """Validates approved TradePlans and constructs broker-independent TradeOrders."""

    _TRADEPLAN_SCHEMA_VERSION = "1.0"
    _EXECUTION_VERSION = "1.0.0"
    _ORDER_TYPE = "MARKET"
    _ORDER_STATUS = "READY"

    def create_order(self, trade_plan: Dict[str, Any]) -> TradeOrder:
        """Returns an immutable READY TradeOrder for a valid approved TradePlan."""
        self._validate_trade_plan(trade_plan)

        execution = trade_plan["execution"]
        return TradeOrder(
            schema_version=self._TRADEPLAN_SCHEMA_VERSION,
            order_id=f"order_{trade_plan['plan_id']}",
            timestamp=trade_plan["timestamp"],
            instrument=trade_plan["instrument"],
            timeframe=trade_plan["timeframe"],
            direction=trade_plan["direction"],
            order_type=self._ORDER_TYPE,
            volume=execution.get("lot_size"),
            stop_loss=execution.get("stop_distance"),
            take_profit=execution.get("take_profit_distance"),
            comment="QuantForge",
            status=self._ORDER_STATUS,
            metadata={
                "tradeplan_id": trade_plan["plan_id"],
                "execution_version": self._EXECUTION_VERSION,
            },
        )

    def _validate_trade_plan(self, trade_plan: Dict[str, Any]) -> None:
        """Raises deterministic errors when a TradePlan cannot be executed."""
        if not isinstance(trade_plan, dict):
            raise ValueError("TradePlan must be a dictionary.")

        required_fields = {
            "schema_version",
            "plan_id",
            "timestamp",
            "instrument",
            "timeframe",
            "direction",
            "trade_allowed",
            "risk",
            "execution",
        }
        missing_fields = required_fields.difference(trade_plan)
        if missing_fields:
            raise ValueError(
                f"TradePlan is missing required fields: {', '.join(sorted(missing_fields))}"
            )
        if trade_plan["schema_version"] != self._TRADEPLAN_SCHEMA_VERSION:
            raise ValueError("Invalid TradePlan schema version.")
        if trade_plan["trade_allowed"] is not True:
            raise ValueError("TradePlan is not approved for execution.")
        if not isinstance(trade_plan["instrument"], str) or not trade_plan["instrument"].strip():
            raise ValueError("TradePlan instrument must be a non-empty string.")
        if trade_plan["direction"] not in {"BUY", "SELL"}:
            raise ValueError("TradePlan direction must be BUY or SELL.")
        if not isinstance(trade_plan["risk"], dict):
            raise ValueError("TradePlan risk block must be a dictionary.")
        if not isinstance(trade_plan["execution"], dict):
            raise ValueError("TradePlan execution block must be a dictionary.")
