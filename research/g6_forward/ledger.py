import csv
import os

class EventLedger:
    def __init__(self, filepath, mode):
        self.filepath = filepath
        self.mode = mode
        
        self.headers = [
            "execution_id", "candidate_id", "event_id", "timestamp", "market", 
            "event_type", "state", "signal_direction", "intended_entry_price", 
            "observed_bid", "observed_ask", "paper_entry", "paper_exit", 
            "gross_result", "transaction_cost", "net_result", "latency_ms", 
            "implementation_sha", "data_source_identity",
            "mode", "price_source", "execution_price_type", 
            "slippage_status", "latency_status"
        ]
        
        # Create file with headers if it doesn't exist
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
                
    def record_trade(self, trade_record):
        # Ensure mode is included
        trade_record["mode"] = self.mode
        
        with open(self.filepath, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers, extrasaction='ignore')
            writer.writerow(trade_record)
