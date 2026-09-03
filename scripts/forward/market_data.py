import time
import os
from typing import Dict, Any, Optional

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
