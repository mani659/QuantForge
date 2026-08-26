import csv
import os

class EventLedger:
    def __init__(self, filepath, mode):
        self.filepath = filepath
        self.mode = mode
        
        self.headers = [
            "execution_id", "candidate_id", "event_id", 
            "research_symbol", "broker_symbol", "broker", "platform", "mode",
            "market_timestamp", "local_receipt_timestamp", "signal_timestamp", "decision_timestamp",
            "bid", "ask", "theoretical_reference_price", "paper_execution_price",
            "quote_execution_difference", "transaction_cost", "net_paper_result",
            "feed_observation_latency", "signal_processing_latency",
            "state", "implementation_sha", "feed_implementation_sha", "symbol_mapping_version",
            "signal_direction", "event_type", "price_source", "execution_price_type", "slippage_status"
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
