import pandas as pd

class PaperExecutionAdapter:
    def __init__(self, mode, identity):
        self.mode = mode
        self.identity = identity
        self.friction_bps = identity["friction_bps"]
        
    def execute_entry(self, signal, tick, decision_timestamp):
        return self._execute(tick, decision_timestamp, "ENTRY")
        
    def execute_exit(self, tick, decision_timestamp):
        return self._execute(tick, decision_timestamp, "EXIT")
        
    def _execute(self, tick, decision_timestamp, action_type):
        market_ts = tick["observation_timestamp"]
        
        if self.mode == "REPLAY_TEST":
            exec_price = tick["open"]
            price_source = "OHLC_M1_OPEN"
            exec_price_type = "SYNTHETIC REPLAY EXECUTION PRICE"
            slippage_status = "UNMEASURED_REPLAY"
            latency_status = "HARNESS PROCESSING LATENCY"
            latency = (decision_timestamp - market_ts).total_seconds() * 1000 # ms
            cost = self.friction_bps
            
        elif self.mode == "FORWARD_PAPER":
            # For real forward paper, we would use tick["ask"] or tick["bid"] depending on direction
            # For now, it's blocked, but if it existed:
            exec_price = tick["ask"] if action_type == "ENTRY" else tick["bid"] # Simplified
            price_source = "LIVE_TICK"
            exec_price_type = "REAL EXECUTABLE PRICE"
            slippage_status = "MEASURED"
            latency_status = "LIVE MARKET LATENCY"
            latency = (decision_timestamp - market_ts).total_seconds() * 1000 # ms
            cost = self.friction_bps
            
        return {
            "execution_price": exec_price,
            "price_source": price_source,
            "execution_price_type": exec_price_type,
            "slippage_status": slippage_status,
            "latency_status": latency_status,
            "latency_ms": latency,
            "cost_bps": cost,
            "decision_timestamp": decision_timestamp,
            "market_timestamp": market_ts
        }
