import pandas as pd
from datetime import datetime, timezone
import time
import os

class MarketDataFeed:
    def __init__(self, mode, data_paths=None):
        """
        mode: 'REPLAY_TEST' or 'FORWARD_PAPER'
        data_paths: dict of symbol -> csv path (for REPLAY_TEST)
        """
        self.mode = mode
        self.data_paths = data_paths or {}
        
        if self.mode == "FORWARD_PAPER":
            # For forward mode, we require a real-time feed capability.
            # If we don't have one, we MUST block.
            raise NotImplementedError("FORWARD_PAPER = BLOCKED. No real-time data source available.")
            
        elif self.mode == "REPLAY_TEST":
            # Load historical data iterators
            self.generators = {}
            for symbol, path in self.data_paths.items():
                if os.path.exists(path):
                    df = pd.read_csv(path, parse_dates=['timestamp'])
                    df.sort_values('timestamp', inplace=True)
                    # We will yield row by row
                    self.generators[symbol] = df.itertuples()
                else:
                    raise FileNotFoundError(f"Replay data missing for {symbol}: {path}")
                    
    def poll_next(self, symbol):
        """
        Simulate polling a feed for the next tick/bar.
        """
        if self.mode == "REPLAY_TEST":
            gen = self.generators.get(symbol)
            if not gen:
                return None
                
            try:
                row = next(gen)
            except StopIteration:
                return None
                
            # Synthesize feed event
            return {
                "symbol": symbol,
                "observation_timestamp": row.timestamp,
                "local_timestamp": pd.Timestamp.now(tz=timezone.utc),
                "open": row.open,
                "high": row.high,
                "low": row.low,
                "close": row.close,
                "bid": "unavailable",
                "ask": "unavailable",
                "true_spread": "unavailable"
            }
