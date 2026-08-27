import time
import os
import signal
import sys
from typing import Dict, Any

from event_ledger import EventLedger
from outcome_ledger import OutcomeLedger
from health import HealthMonitor
from cand_024_engine import Cand024Engine
from cand_035_engine import Cand035Engine
from paper_execution import PaperExecutionFirewall

class RareEventRunner:
    def __init__(self):
        self.running = False
        self.instance_id = f"runner_{int(time.time())}"
        
        # Isolation directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.event_ledger = EventLedger(os.path.join(self.base_dir, "event_ledger.jsonl"))
        self.outcome_ledger = OutcomeLedger(os.path.join(self.base_dir, "outcome_ledger.jsonl"))
        self.health = HealthMonitor(os.path.join(self.base_dir, "health.jsonl"))
        
        self.cand_024 = Cand024Engine()
        self.cand_035 = Cand035Engine()
        self.paper = PaperExecutionFirewall(friction=2.0)
        
        self.reconnect_delay = 1
        self.max_reconnect_delay = 30
        
    def handle_sigint(self, signum, frame):
        print("SIGINT received. Safely shutting down.")
        self.running = False

    def run(self, mock_feed=None):
        self.running = True
        signal.signal(signal.SIGINT, self.handle_sigint)
        
        # State Reconcile stub
        print(f"[{self.instance_id}] Reconciling state from ledgers...")
        
        while self.running:
            try:
                if mock_feed:
                    quote = mock_feed.get_next_quote()
                    if quote is None:
                        break # End of mock feed
                else:
                    # Fake sleep for live placeholder
                    time.sleep(1)
                    quote = {
                        "utc_timestamp": time.time(),
                        "symbol": "USATECHIDXUSD",
                        "bid": 15000.0,
                        "ask": 15002.0
                    }
                    
                self.reconnect_delay = 1 # Reset on successful data
                self._process_quote(quote)
                
            except Exception as e:
                self.health.mark_disconnect()
                print(f"Data error: {e}. Backing off {self.reconnect_delay}s")
                time.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                self.health.mark_reconnect()
                
        print(f"[{self.instance_id}] Runner shut down cleanly.")

    def _process_quote(self, quote: Dict[str, Any]):
        current_time = quote['utc_timestamp']
        
        # Process CAND-024
        event_24 = self.cand_024.evaluate(current_time, quote)
        self._handle_engine_event(self.cand_024, event_24, quote)
        
        # Process CAND-035
        event_35 = self.cand_035.evaluate(current_time, quote)
        self._handle_engine_event(self.cand_035, event_35, quote)
        
        # Heartbeat
        if int(current_time) % 60 == 0:
            self.health.record_heartbeat(
                self.instance_id, 
                "CONNECTED", 
                current_time, 
                {"CAND-024": self.cand_024.state, "CAND-035": self.cand_035.state}
            )

    def _handle_engine_event(self, engine, event, quote):
        if not event:
            return
            
        contract = engine.contract
        if event['action'] == "TRIGGER":
            # Record Detection
            self.event_ledger.record_event({
                "candidate_id": contract.candidate_id,
                "contract_version": contract.version,
                "contract_hash": contract.hash,
                "event_id": event['event_id'],
                "instrument": quote['symbol'],
                "utc_timestamp": quote['utc_timestamp'],
                "ny_timestamp": event['ny_time'],
                "event_state": "EVENT_DETECTED",
                "theoretical_entry": event['theoretical_entry'],
                "runner_instance_id": self.instance_id
            })
            
            # Paper execution
            paper_res = self.paper.execute_entry(event, quote)
            
            if paper_res['status'] == "PAPER_ENTRY_RECORDED":
                engine.state = "IN_POSITION"
                self.event_ledger.record_event({
                    "candidate_id": contract.candidate_id,
                    "event_id": event['event_id'],
                    "event_state": "PAPER_IN_POSITION",
                    "modeled_paper_entry": paper_res['paper_entry_price'],
                    "utc_timestamp": quote['utc_timestamp']
                })
                
        elif event['action'] == "EXIT":
            paper_res = self.paper.execute_exit(event, quote)
            if paper_res['status'] == "PAPER_EXIT_RECORDED":
                self.outcome_ledger.record_outcome({
                    "candidate_id": contract.candidate_id,
                    "contract_version": contract.version,
                    "contract_hash": contract.hash,
                    "event_id": event['event_id'],
                    "paper_entry_price": paper_res['paper_entry_price'],
                    "paper_exit_price": paper_res['paper_exit_price'],
                    "gross_result": paper_res['gross_result'],
                    "net_result": paper_res['net_result'],
                    "modeled_friction": paper_res['modeled_friction'],
                    "outcome_status": "COMPLETED"
                })

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args()
    
    if args.smoke_test:
        print("Running smoke test...")
        runner = RareEventRunner()
        # Mock feed for 3 ticks
        class MockFeed:
            def __init__(self):
                self.ticks = [
                    {"utc_timestamp": 1700000000, "symbol": "USATECHIDXUSD", "bid": 15000, "ask": 15002},
                    {"utc_timestamp": 1700000060, "symbol": "USATECHIDXUSD", "bid": 15010, "ask": 15012},
                    {"utc_timestamp": 1700000120, "symbol": "USATECHIDXUSD", "bid": 15020, "ask": 15022}
                ]
                self.idx = 0
            def get_next_quote(self):
                if self.idx < len(self.ticks):
                    t = self.ticks[self.idx]
                    self.idx += 1
                    return t
                return None
                
        runner.run(mock_feed=MockFeed())
    else:
        print("OBSERVATION NOT LAUNCHED. Start with real feed setup required.")
