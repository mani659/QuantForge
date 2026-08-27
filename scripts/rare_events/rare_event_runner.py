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
    def __init__(self, feed, mode):
        self.running = False
        self.mode = mode
        self.feed = feed
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

    def run(self):
        self.running = True
        signal.signal(signal.SIGINT, self.handle_sigint)
        
        # State Reconcile stub
        print(f"[{self.instance_id}] Reconciling state from ledgers in mode {self.mode}...")
        
        while self.running:
            try:
                conn_state = self.feed.connection_state()
                if conn_state != "CONNECTED":
                    self.health.mark_disconnect()
                    print(f"Feed disconnected/invalid. Backing off {self.reconnect_delay}s")
                    time.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                    continue
                    
                quote_res = self.feed.latest_quote("USATECHIDXUSD")
                
                if quote_res.get("status") != "DATA_FRESH":
                    status = quote_res.get("status", "FEED_UNAVAILABLE")
                    # Do NOT treat stale/disconnected as NO_EVENT. Just skip evaluation.
                    print(f"Data not fresh ({status}). Skipping evaluation.")
                    time.sleep(self.reconnect_delay)
                    self.health.mark_disconnect()
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                    continue
                    
                # Format to match existing quote dict expectation downstream
                quote = {
                    "utc_timestamp": quote_res['source_timestamp'],
                    "symbol": quote_res['symbol'],
                    "bid": quote_res['bid'],
                    "ask": quote_res['ask']
                }
                    
                self.reconnect_delay = 1 # Reset on successful data
                self.health.mark_reconnect()
                self._process_quote(quote)
                time.sleep(1) # Base polling rate
                
            except Exception as e:
                self.health.mark_disconnect()
                print(f"Data error: {e}. Backing off {self.reconnect_delay}s")
                time.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                
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
    from mt5_market_feed import MT5MarketFeed
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["test", "smoke", "forward", "verify-feed"], required=True)
    args = parser.parse_args()
    
    if args.mode == "smoke" or args.mode == "test":
        print(f"Running {args.mode} mode with synthetic feed...")
        # Mock feed for testing
        class MockFeed:
            def __init__(self):
                self.ticks = [
                    {"status": "DATA_FRESH", "source_timestamp": 1700000000, "symbol": "USATECHIDXUSD", "bid": 15000, "ask": 15002},
                    {"status": "DATA_FRESH", "source_timestamp": 1700000060, "symbol": "USATECHIDXUSD", "bid": 15010, "ask": 15012},
                    {"status": "DATA_FRESH", "source_timestamp": 1700000120, "symbol": "USATECHIDXUSD", "bid": 15020, "ask": 15022}
                ]
                self.idx = 0
            def connection_state(self):
                if self.idx < len(self.ticks):
                    return "CONNECTED"
                return "DISCONNECTED"
            def latest_quote(self, symbol):
                t = self.ticks[self.idx]
                self.idx += 1
                return t
                
        runner = RareEventRunner(feed=MockFeed(), mode=args.mode)
        runner.run()
        
    elif args.mode == "verify-feed":
        print("Running read-only MT5 feed verification...")
        feed = MT5MarketFeed()
        if not feed.initialize():
            print("MARKET FEED REMEDIATION BLOCKED: Could not initialize MT5.")
            sys.exit(1)
            
        print(f"Connection State: {feed.connection_state()}")
        quote = feed.latest_quote("USATECHIDXUSD")
        print(f"Latest Quote: {quote}")
        bar = feed.latest_completed_bar("USATECHIDXUSD", "M1")
        print(f"Completed M1 Bar: {bar}")
        feed.shutdown()
        print("Read-only verification completed safely. No observation launched.")
        
    elif args.mode == "forward":
        # Forward strictly requires real feed
        print("Launching Rare-Event Forward Observation Mode...")
        feed = MT5MarketFeed()
        if not feed.initialize():
            print("STARTUP FAILURE - INVALID FEED MODE / DISCONNECTED")
            sys.exit(1)
            
        runner = RareEventRunner(feed=feed, mode="forward")
        runner.run()
