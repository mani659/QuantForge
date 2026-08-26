import pandas as pd

class PaperExecutionAdapter:
    def __init__(self, mode, identity):
        self.mode = mode
        self.identity = identity
        self.friction_bps = identity["friction_bps"]
        
    def execute_entry(self, active_trade, tick, decision_timestamp):
        return self._execute(active_trade, tick, decision_timestamp, "ENTRY")
        
    def execute_exit(self, active_trade, tick, decision_timestamp):
        return self._execute(active_trade, tick, decision_timestamp, "EXIT")
        
    def _execute(self, active_trade, tick, decision_timestamp, action_type):
        market_ts = tick["observation_timestamp"]
        direction = active_trade["signal_direction"]
        
        if self.mode == "REPLAY_TEST":
            exec_price = tick["open"]
            price_source = "OHLC_M1_OPEN"
            exec_price_type = "SYNTHETIC_REPLAY"
            slippage_status = "UNMEASURED_REPLAY"
            latency_status = "HARNESS PROCESSING LATENCY"
            cost = self.friction_bps
            
        elif self.mode == "FORWARD_PAPER":
            # Real-time bid/ask from tick
            if action_type == "ENTRY":
                if direction == 1:
                    exec_price = tick["ask"]
                else:
                    exec_price = tick["bid"]
            elif action_type == "EXIT":
                if direction == 1:
                    exec_price = tick["bid"]
                else:
                    exec_price = tick["ask"]
                    
            price_source = "LIVE_TICK"
            exec_price_type = "DEMO_PAPER_QUOTE"
            slippage_status = "QUOTE_BASED_PAPER_DIFFERENCE"
            latency_status = "SIGNAL PROCESSING LATENCY"
            cost = self.friction_bps
            
        return {
            "execution_price": exec_price,
            "price_source": price_source,
            "execution_price_type": exec_price_type,
            "slippage_status": slippage_status,
            "latency_status": latency_status,
            "cost_bps": cost,
            "decision_timestamp": decision_timestamp,
            "market_timestamp": market_ts
        }
