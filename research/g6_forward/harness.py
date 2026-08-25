import time
import pandas as pd
from datetime import datetime, timezone
import uuid

from .cand015_identity import FROZEN_CAND015_IDENTITY, verify_identity
from .data_feed import MarketDataFeed
from .signal_engine import Cand015SignalEngine
from .event_machine import EventStateMachine
from .paper_execution import PaperExecutionAdapter
from .ledger import EventLedger

class G6Harness:
    def __init__(self, mode="REPLAY_TEST", data_paths=None, ledger_path="ledger.csv"):
        self.mode = mode
        
        # 1. Identity Validation
        verify_identity()
        self.identity = FROZEN_CAND015_IDENTITY
        
        # 2. Components
        self.data_feed = MarketDataFeed(mode=self.mode, data_paths=data_paths)
        self.signal_engine = Cand015SignalEngine(identity=self.identity)
        self.event_machine = EventStateMachine()
        self.paper_execution = PaperExecutionAdapter(mode=self.mode, identity=self.identity)
        self.ledger = EventLedger(filepath=ledger_path, mode=self.mode)
        
        # State Tracking
        self.active_trade = None
        self.event_count = 0
        self.errors = 0
        
    def run_replay_fixture(self, limit_events=None):
        """Run the harness through the historical replay stream."""
        print(f"Starting G6 Harness in mode: {self.mode}")
        if self.mode != "REPLAY_TEST":
            raise ValueError("run_replay_fixture can only be called in REPLAY_TEST mode")
            
        last_heartbeat = time.time()
        
        # In a real event loop, we would poll independently. 
        # For replay, we interleave pulling from BTC and NDX by time.
        # However, data_feed.poll_next() as implemented just pulls sequential rows per symbol.
        # We need a unified time-sorted stream of events.
        # Since data_feed.generators has separate streams, we should pull the next chronologically.
        
        # Simplification for replay parity test:
        # Load both into a combined sorted list of ticks.
        # We will modify the data_feed slightly to allow this or do it here.
        
        # Actually, let's just use the generators and peak the next timestamp
        peeks = {}
        for sym in self.data_feed.generators:
            tick = self.data_feed.poll_next(sym)
            if tick:
                peeks[sym] = tick
                
        while peeks:
            # Find the earliest tick
            next_sym = min(peeks.keys(), key=lambda s: peeks[s]["observation_timestamp"])
            tick = peeks[next_sym]
            
            # Fetch next for this symbol
            next_tick = self.data_feed.poll_next(next_sym)
            if next_tick:
                peeks[next_sym] = next_tick
            else:
                del peeks[next_sym]
                
            self._process_tick(tick)
            
            if limit_events and self.event_count >= limit_events:
                break
                
            if time.time() - last_heartbeat > 5.0:
                print(f"Heartbeat: state={self.event_machine.state}, events={self.event_count}")
                last_heartbeat = time.time()
                
        print("Replay Fixture Complete.")
        
    def _process_tick(self, tick):
        ts = tick["observation_timestamp"]
        local_ts = pd.Timestamp.now(tz=timezone.utc)
        
        # 1. Feed to signal engine
        signal = self.signal_engine.process_tick(tick)
        
        # 2. State Machine Transitions
        if signal:
            if self.event_machine.handle_signal(signal, ts):
                # New event created
                self.active_trade = {
                    "execution_id": str(uuid.uuid4()),
                    "candidate_id": self.identity["candidate_id"],
                    "event_id": str(uuid.uuid4()),
                    "timestamp": ts,
                    "market": self.identity["opportunity_market"],
                    "event_type": signal["event_type"],
                    "signal_direction": signal["intended_direction"],
                    "intended_entry_price": tick["close"], # Just a placeholder intention
                    "implementation_sha": "simulated_sha_1234",
                    "data_source_identity": "M1_CSV_REPLAY"
                }
                
        # 3. Execution logic
        # If ENTRY_PENDING, we execute on the next available BTCUSD tick
        if self.event_machine.state == "ENTRY_PENDING" and tick["symbol"] == self.identity["opportunity_market"]:
            # Emulate next-quote execution
            entry_report = self.paper_execution.execute_entry(self.active_trade, tick, local_ts)
            self.event_machine.handle_entry(entry_report, ts)
            
            self.active_trade.update({
                "paper_entry": entry_report["execution_price"],
                "observed_bid": tick["bid"],
                "observed_ask": tick["ask"],
                "entry_time": ts,
                "price_source": entry_report["price_source"],
                "execution_price_type": entry_report["execution_price_type"],
                "slippage_status": entry_report["slippage_status"],
                "latency_status": entry_report["latency_status"],
                "latency_ms": entry_report["latency_ms"],
                "transaction_cost": entry_report["cost_bps"]
            })
            
        # Check Exit Condition (Time-based: 60 minutes after entry)
        if self.event_machine.state == "IN_POSITION" and tick["symbol"] == self.identity["opportunity_market"]:
            entry_time = self.active_trade.get("entry_time")
            if ts >= entry_time + pd.Timedelta(minutes=60):
                self.event_machine.trigger_exit(ts)
                
        if self.event_machine.state == "EXIT_PENDING" and tick["symbol"] == self.identity["opportunity_market"]:
            exit_report = self.paper_execution.execute_exit(tick, local_ts)
            self.event_machine.handle_exit(exit_report, ts)
            
            self.active_trade["paper_exit"] = exit_report["execution_price"]
            
            # Calculate results
            direction = self.active_trade["signal_direction"]
            entry_px = self.active_trade["paper_entry"]
            exit_px = self.active_trade["paper_exit"]
            
            if direction == 1:
                gross = (exit_px - entry_px) / entry_px * 10000
            else:
                gross = (entry_px - exit_px) / entry_px * 10000
                
            net = gross - self.active_trade["transaction_cost"]
            
            self.active_trade["gross_result"] = gross
            self.active_trade["net_result"] = net
            self.active_trade["state"] = "CLOSED"
            
            # Log to ledger
            self.ledger.record_trade(self.active_trade)
            self.event_count += 1
            self.active_trade = None
