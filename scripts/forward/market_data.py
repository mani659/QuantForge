import time
import os
from typing import Dict, Any, Optional


class MT5TimeoutMarketFeed:
    """MT5 feed that routes all calls through a timeout-protected worker.

    This class provides the same interface as MT5MarketFeed but routes
    every MT5-bound call through a separate process via the timeout manager.
    This ensures a hung MT5 native call cannot freeze the supervisor.

    HARD TIMEOUT GUARANTEE:
      Every MT5 operation is dispatched with a deadline. If the worker
      does not respond within the deadline, the worker is terminated
      and replaced. The supervisor never waits indefinitely.

    F-01 FIREWALL:
      This class does NOT access F-01 data or modify any archives.
    """

    def __init__(self, timeout_manager):
        """Initialize with an existing MT5TimeoutManager.

        Args:
            timeout_manager: MT5TimeoutManager instance (must be started).
        """
        self._manager = timeout_manager
        self._connected = False
        self._initialized = False

    def initialize(self) -> bool:
        """Initialize MT5 via the timeout-protected worker."""
        terminal_path = os.getenv("QF_MT5_TERMINAL_PATH")
        result = self._manager.execute(
            "initialize",
            terminal_path=terminal_path,
            timeout=self._manager.startup_timeout,
        )
        if result["success"] and result["result"].get("initialized"):
            self._connected = True
            self._initialized = True
            return True
        self._connected = False
        return False

    def connection_state(self) -> str:
        """Check MT5 connection state via timeout-protected worker."""
        if not self._connected:
            return "DISCONNECTED"
        result = self._manager.execute("connection_state")
        if result["success"]:
            state = result["result"].get("state", "DISCONNECTED")
            if state == "DISCONNECTED":
                self._connected = False
            return state
        # Timeout or error — treat as disconnected
        self._connected = False
        return "DISCONNECTED"

    def terminal_info(self) -> Dict[str, Any]:
        """Get terminal info via timeout-protected worker."""
        if not self._connected:
            return {"broker": "UNKNOWN", "server": "UNKNOWN"}
        result = self._manager.execute("terminal_info")
        if result["success"]:
            return {
                "broker": result["result"].get("broker", "UNKNOWN"),
                "server": result["result"].get("server", "UNKNOWN"),
            }
        return {"broker": "UNKNOWN", "server": "UNKNOWN"}

    def latest_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get latest quote via timeout-protected worker."""
        if not self._connected:
            return {"status": "FEED_UNAVAILABLE"}
        result = self._manager.execute("latest_quote", symbol=symbol)
        if result["success"]:
            return result["result"]
        if result["timeout"]:
            return {"status": "FEED_UNAVAILABLE"}
        return {"status": "DATA_INDETERMINATE"}

    def latest_completed_bar(self, symbol: str, timeframe: str) -> Optional[Dict[str, Any]]:
        """Get latest completed bar via timeout-protected worker."""
        if not self._connected:
            return {"status": "FEED_UNAVAILABLE"}
        result = self._manager.execute(
            "latest_completed_bar", symbol=symbol, timeframe=timeframe
        )
        if result["success"]:
            return result["result"]
        if result["timeout"]:
            return {"status": "FEED_UNAVAILABLE"}
        return {"status": "DATA_INDETERMINATE"}

    def shutdown(self):
        """Shutdown MT5 via timeout-protected worker."""
        if self._connected:
            self._manager.execute("shutdown")
            self._connected = False

    @property
    def health_state(self):
        """Delegate health state to timeout manager."""
        return self._manager.health_state

    @property
    def stats(self):
        """Delegate stats to timeout manager."""
        return self._manager.stats


class MT5MarketFeed:
    def __init__(self, mt5_module=None):
        self._mt5 = mt5_module
        self._connected = False
        
    def _get_mt5(self):
        if self._mt5 is not None:
            return self._mt5
        try:
            import MetaTrader5 as mt5
            self._mt5 = mt5
            return mt5
        except ImportError:
            return None
            
    def initialize(self) -> bool:
        mt5 = self._get_mt5()
        if not mt5:
            return False
            
        terminal_path = os.getenv("QF_MT5_TERMINAL_PATH")
        if terminal_path and os.path.exists(terminal_path):
            self._connected = mt5.initialize(path=terminal_path)
        else:
            self._connected = mt5.initialize()
            
        return self._connected
        
    def connection_state(self) -> str:
        if not self._connected:
            return "DISCONNECTED"
        mt5 = self._get_mt5()
        if not mt5:
            return "INVALID"
            
        terminal_info = mt5.terminal_info()
        if terminal_info is None:
            self._connected = False
            return "DISCONNECTED"
            
        return "CONNECTED"

    def terminal_info(self) -> Dict[str, Any]:
        if self.connection_state() != "CONNECTED":
            return {"broker": "UNKNOWN", "server": "UNKNOWN"}
        mt5 = self._get_mt5()
        info = mt5.terminal_info()
        acc = mt5.account_info()
        broker = info.company if info else "UNKNOWN"
        server = acc.server if acc else "UNKNOWN"
        return {"broker": broker, "server": server}

    def latest_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        if self.connection_state() != "CONNECTED":
            return {"status": "FEED_UNAVAILABLE"}
            
        mt5 = self._get_mt5()
        mt5.symbol_select(symbol, True)
        tick = mt5.symbol_info_tick(symbol)
        
        if tick is None:
            return {"status": "DATA_INDETERMINATE"}
            
        source_ts = tick.time
        receipt_ts = time.time()
        
        age = receipt_ts - source_ts
        if age > 60:
            return {"status": "DATA_STALE", "age": age}
            
        return {
            "status": "DATA_FRESH",
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "source_timestamp": source_ts,
            "receipt_timestamp": receipt_ts,
            "age": age
        }
        
    def latest_completed_bar(self, symbol: str, timeframe: str) -> Optional[Dict[str, Any]]:
        if self.connection_state() != "CONNECTED":
            return {"status": "FEED_UNAVAILABLE"}
            
        mt5 = self._get_mt5()
        
        tf_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1
        }
        
        mt5_tf = tf_map.get(timeframe)
        if not mt5_tf:
            return {"status": "DATA_INDETERMINATE"}
            
        mt5.symbol_select(symbol, True)
        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 1, 1)
        if rates is None or len(rates) == 0:
            return {"status": "DATA_INDETERMINATE"}
            
        bar = rates[0]
        try:
            volume = int(bar['tick_volume'])
        except Exception:
            volume = 0
        return {
            "status": "DATA_FRESH",
            "symbol": symbol,
            "time": bar['time'],
            "open": bar['open'],
            "high": bar['high'],
            "low": bar['low'],
            "close": bar['close'],
            "volume": volume
        }

    def shutdown(self):
        if self._connected:
            mt5 = self._get_mt5()
            if mt5:
                mt5.shutdown()
            self._connected = False
