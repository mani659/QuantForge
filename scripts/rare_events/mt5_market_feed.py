import time
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime, timezone

# Allow lazy import or dependency injection of MetaTrader5
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

    def source_timestamp(self) -> Optional[float]:
        if self.connection_state() != "CONNECTED":
            return None
        # Use local clock as the reference for source timestamp if MT5 does not expose a global server clock easily,
        # but symbol_info_tick gives us the actual exchange time for a symbol.
        return time.time()
        
    def latest_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        if self.connection_state() != "CONNECTED":
            return {"status": "FEED_UNAVAILABLE"}
            
        mt5 = self._get_mt5()
        mt5.symbol_select(symbol, True)
        tick = mt5.symbol_info_tick(symbol)
        
        if tick is None:
            return {"status": "DATA_INDETERMINATE"}
            
        # Time of the tick in seconds
        source_ts = tick.time
        receipt_ts = time.time()
        
        # Check freshness
        age = receipt_ts - source_ts
        if age > 60: # 60 seconds threshold for stale data
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
        
        # Retrieve 1 completed bar (offset 1 to avoid current forming bar)
        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 1, 1)
        if rates is None or len(rates) == 0:
            return {"status": "DATA_INDETERMINATE"}
            
        bar = rates[0]
        return {
            "status": "DATA_FRESH",
            "symbol": symbol,
            "time": bar['time'],
            "open": bar['open'],
            "high": bar['high'],
            "low": bar['low'],
            "close": bar['close']
        }
        
    def shutdown(self):
        if self._connected:
            mt5 = self._get_mt5()
            if mt5:
                mt5.shutdown()
            self._connected = False
