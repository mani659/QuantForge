import pandas as pd
from datetime import datetime, timezone
import time

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

class MT5DataFeed:
    def __init__(self, mode, identity):
        self.mode = mode
        self.identity = identity
        
        # Explicit Immutable Symbol Mapping
        self.MAPPING = {
            "USATECHIDXUSD": "USTECm",
            "BTCUSD": "BTCUSDm"
        }
        self.BROKER = "Exness"
        self.PLATFORM = "MT5"
        self.MAPPING_VERSION = "1.0"
        self.SOURCE_AUDIT = "CAND015_EXNESS_MT5_DATA_SOURCE_AUDIT_V1"
        
        self.last_observation_time = None
        self.stale_threshold_seconds = 300 # 5 minutes

        if self.mode == "FORWARD_PAPER":
            self._initialize_mt5_safety()
            
    def _initialize_mt5_safety(self):
        if not MT5_AVAILABLE:
            raise RuntimeError("FAIL CLOSED: MetaTrader5 package not installed.")
            
        if not mt5.initialize():
            raise RuntimeError(f"FAIL CLOSED: MT5 initialize() failed, error code = {mt5.last_error()}")
            
        terminal_info = mt5.terminal_info()
        if terminal_info is None or not terminal_info.connected:
            raise RuntimeError("FAIL CLOSED: MT5 terminal not connected.")
            
        account_info = mt5.account_info()
        if account_info is None:
            raise RuntimeError("FAIL CLOSED: MT5 account_info() failed.")
            
        if account_info.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
            raise RuntimeError("FAIL CLOSED: MT5 account is NOT DEMO. Forward mode requires a demo account.")
            
        # Verify required symbols
        for research_sym in ["USATECHIDXUSD", "BTCUSD"]:
            broker_sym = self.MAPPING.get(research_sym)
            if not broker_sym:
                raise RuntimeError(f"FAIL CLOSED: Missing mapping for {research_sym}")
                
            if not mt5.symbol_select(broker_sym, True):
                raise RuntimeError(f"FAIL CLOSED: Symbol {broker_sym} not available in MT5.")
                
            info = mt5.symbol_info(broker_sym)
            if info is None:
                raise RuntimeError(f"FAIL CLOSED: symbol_info failed for {broker_sym}.")
                
            # Verify basic tick functionality (time and bid/ask)
            if info.time == 0:
                pass # Can be 0 if market closed, but we'll check it in real-time.
                
    def fetch_latest_observations(self):
        """
        Returns a list of dicts with the latest observations for the required symbols.
        The caller will process them and order them deterministically.
        """
        if self.mode != "FORWARD_PAPER":
            raise RuntimeError("fetch_latest_observations only available in FORWARD_PAPER mode.")
            
        observations = []
        for research_sym in ["USATECHIDXUSD", "BTCUSD"]:
            broker_sym = self.MAPPING[research_sym]
            info = mt5.symbol_info(broker_sym)
            if info is None:
                raise RuntimeError(f"FAIL CLOSED: Disconnected or symbol_info failed for {broker_sym}")
                
            market_time_utc = pd.Timestamp(info.time, unit='s', tz='UTC')
            local_time_utc = pd.Timestamp.now(tz=timezone.utc)
            
            # Stale check
            if (local_time_utc - market_time_utc).total_seconds() > self.stale_threshold_seconds:
                raise RuntimeError(f"FAIL CLOSED: DATA STALE for {broker_sym}. Market time: {market_time_utc}, Local: {local_time_utc}")
            
            # Regression check
            if self.last_observation_time and market_time_utc < self.last_observation_time:
                # MT5 shouldn't go back in time, but allow equal.
                pass 
                
            # Get latest completed M1 bar to determine OHLC.
            # copy_rates_from_pos gets [oldest, ..., newest]. index 0 is oldest.
            # We want the newest COMPLETED bar. In MT5, index 0 is oldest, index -1 is current forming.
            # Index -2 is the last completed bar.
            # Actually, to be safe, we request 2 bars.
            rates = mt5.copy_rates_from_pos(broker_sym, mt5.TIMEFRAME_M1, 0, 2)
            if rates is None or len(rates) < 2:
                raise RuntimeError(f"FAIL CLOSED: Cannot fetch completed M1 bars for {broker_sym}")
                
            completed_bar = rates[-2] # The last fully formed bar
            
            # Ensure bid <= ask
            if info.bid <= 0 or info.ask <= 0 or info.bid > info.ask:
                raise RuntimeError(f"FAIL CLOSED: Invalid spread/quotes for {broker_sym}. Bid: {info.bid}, Ask: {info.ask}")
                
            obs = {
                "symbol": research_sym,
                "broker_symbol": broker_sym,
                "observation_timestamp": market_time_utc,
                "local_timestamp": local_time_utc,
                "open": completed_bar['open'],
                "high": completed_bar['high'],
                "low": completed_bar['low'],
                "close": completed_bar['close'],
                "bid": info.bid,
                "ask": info.ask,
                "last": getattr(info, 'last', 0.0),
                "true_spread": (info.ask - info.bid),
                "feed_identity": "EXNESS_MT5_DEMO"
            }
            observations.append(obs)
            
        return observations

    def shutdown(self):
        if self.mode == "FORWARD_PAPER" and MT5_AVAILABLE:
            mt5.shutdown()
