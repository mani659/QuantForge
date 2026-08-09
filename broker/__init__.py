"""Broker adapter interfaces for QuantForge."""

from .mt5_adapter import MT5Adapter, MT5BrokerAdapter
from .mt5_connection import ConnectionStatus, MT5Connection, MT5ConnectionError
from .trade_result import TradeResult

__all__ = [
    "ConnectionStatus",
    "MT5Adapter",
    "MT5BrokerAdapter",
    "MT5Connection",
    "MT5ConnectionError",
    "TradeResult",
]
