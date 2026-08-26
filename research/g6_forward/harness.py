import time
import pandas as pd
from datetime import datetime, timezone
import uuid
import json
import os

from .cand015_identity import FROZEN_CAND015_IDENTITY, verify_identity
from .data_feed import MarketDataFeed
from .signal_engine import Cand015SignalEngine
from .event_machine import EventStateMachine
from .paper_execution import PaperExecutionAdapter
from .ledger import EventLedger

class G6Harness:
    def __init__(self, mode="REPLAY_TEST", data_paths=None, ledger_path="ledger.csv", heartbeat_path=None, connection_path=None):
        self.mode = mode
        self.heartbeat_path = heartbeat_path
        self.connection_path = connection_path
        
        # 1. Identity Validation
        verify_identity()
        self.identity = FROZEN_CAND015_IDENTITY
        
        # 2. Components
        if self.mode == "FORWARD_PAPER":
            from .mt5_feed import MT5DataFeed
            self.data_feed = MT5DataFeed(mode=self.mode, identity=self.identity)
        else:
            self.data_feed = MarketDataFeed(mode=self.mode, data_paths=data_paths)
            
        self.signal_engine = Cand015SignalEngine(identity=self.identity)
        self.event_machine = EventStateMachine()
        self.paper_execution = PaperExecutionAdapter(mode=self.mode, identity=self.identity)
        self.ledger = EventLedger(filepath=ledger_path, mode=self.mode)
        
        # State Tracking
        self.active_trade = None
        self.event_count = 0
        self.paper_trade_count = 0
        self.errors = 0
        self.last_error_msg = None
        self._stop_event = False
        self.last_observations = {}
        
    def _log_connection_event(self, event_type, reason=""):
        if self.connection_path:
            with open(self.connection_path, 'a') as f:
                rec = {
                    "timestamp": str(pd.Timestamp.now(tz=timezone.utc)),
                    "event_type": event_type,
                    "reason": reason
                }
                f.write(json.dumps(rec) + "\\n")
                
    def _write_heartbeat(self):
        if self.heartbeat_path:
            with open(self.heartbeat_path, 'a') as f:
                hb = {
                    "utc_timestamp": str(pd.Timestamp.now(tz=timezone.utc)),
                    "mt5_status": "CONNECTED" if self.errors == 0 else "ERROR_STATE",
                    "last_ustec_tick": self.last_observations.get("USATECHIDXUSD", {}).get("observation_timestamp", "N/A"),
                    "last_btc_tick": self.last_observations.get("BTCUSD", {}).get("observation_timestamp", "N/A"),
                    "connection_status": "OK" if self.errors == 0 else "FAIL",
                    "disconnect_count": getattr(self, "disconnect_count", 0),
                    "reconnect_count": getattr(self, "reconnect_count", 0),
                    "current_outage_seconds": getattr(self, "current_outage_seconds", 0.0),
                    "signal_state": self.event_machine.state,
                    "current_event_state": self.event_machine.state,
                    "event_count": self.event_count,
                    "paper_trade_count": self.paper_trade_count,
                    "last_error": self.last_error_msg
                }
                # Convert timestamps to string if they are pandas timestamps
                for k, v in hb.items():
                    if isinstance(v, pd.Timestamp):
                        hb[k] = str(v)
                f.write(json.dumps(hb) + "\n")
    def run_replay_fixture(self, limit_events=None):
        """Run the harness through the historical replay stream."""
        print(f"Starting G6 Harness in mode: {self.mode}")
        if self.mode != "REPLAY_TEST":
            raise ValueError("run_replay_fixture can only be called in REPLAY_TEST mode")
            
        last_heartbeat = time.time()
        
        peeks = {}
        for sym in self.data_feed.generators:
            tick = self.data_feed.poll_next(sym)
            if tick:
                peeks[sym] = tick
                
        while peeks:
            next_sym = min(peeks.keys(), key=lambda s: peeks[s]["observation_timestamp"])
            tick = peeks[next_sym]
            
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
        
    def run_forward_observation(self, poll_interval_ms=100, max_duration_seconds=None):
        print(f"Starting G6 Harness FORWARD_PAPER observation.")
        if self.mode != "FORWARD_PAPER":
            raise ValueError("run_forward_observation requires FORWARD_PAPER mode")
            
        start_time = time.time()
        last_heartbeat = start_time
        
        self._log_connection_event("START", "Session started cleanly")
        
        try:
            while not self._stop_event:
                if max_duration_seconds and (time.time() - start_time) >= max_duration_seconds:
                    print("Reached max duration. Stopping observation.")
                    self._log_connection_event("STOP", "Reached max duration")
                    break
                    
                # Poll latest ticks
                try:
                    observations = self.data_feed.fetch_latest_observations()
                    self.errors = 0
                except Exception as e:
                    self.errors += 1
                    self.last_error_msg = str(e)
                    print(f"Data Feed Error: {e}")
                    self._log_connection_event("ERROR", str(e))
                    # Requirement 15: Do not silently continue. Stop or fail closed on these errors.
                    self._log_connection_event("FATAL", "Connection / Data failure. Failing closed.")
                    break
                    
                # Cross-market ordering: order by market_timestamp, with USTECm before BTCUSDm on ties.
                # USATECHIDXUSD should be processed before BTCUSD if timestamps are equal.
                observations.sort(key=lambda x: (x["observation_timestamp"], 0 if x["symbol"] == "USATECHIDXUSD" else 1))
                
                for obs in observations:
                    self.last_observations[obs["symbol"]] = obs
                    self._process_tick(obs)
                    
                time.sleep(poll_interval_ms / 1000.0)
                
                if time.time() - last_heartbeat > 10.0:
                    print(f"Forward Heartbeat: state={self.event_machine.state}, events={self.event_count}, errors={self.errors}")
                    self._write_heartbeat()
                    last_heartbeat = time.time()
        except KeyboardInterrupt:
            print("Stopped by KeyboardInterrupt")
            self._log_connection_event("STOP", "KeyboardInterrupt")
        finally:
            self.data_feed.shutdown()
            print("Observation safely stopped.")
            self._write_heartbeat()

    def _process_tick(self, tick):
        ts = tick["observation_timestamp"]
        local_ts = tick.get("local_timestamp", pd.Timestamp.now(tz=timezone.utc))
        
        decision_start_time = pd.Timestamp.now(tz=timezone.utc)
        
        # 1. Feed to signal engine
        signal = self.signal_engine.process_tick(tick)
        
        decision_end_time = pd.Timestamp.now(tz=timezone.utc)
        signal_processing_latency = (decision_end_time - local_ts).total_seconds() * 1000
        feed_latency = (local_ts - ts).total_seconds() * 1000
        
        # 2. State Machine Transitions
        if signal:
            if self.event_machine.handle_signal(signal, ts):
                self.active_trade = {
                    "execution_id": str(uuid.uuid4()),
                    "candidate_id": self.identity["candidate_id"],
                    "event_id": str(uuid.uuid4()),
                    "timestamp": ts,
                    "market": self.identity["opportunity_market"],
                    "event_type": signal["event_type"],
                    "signal_direction": signal["intended_direction"],
                    "intended_entry_price": tick["close"],
                    "implementation_sha": "simulated_sha_1234",
                    "data_source_identity": tick.get("feed_identity", "M1_CSV_REPLAY"),
                    "research_symbol": self.identity["opportunity_market"],
                    "broker_symbol": tick.get("broker_symbol", "N/A"),
                    "broker": getattr(self.data_feed, 'BROKER', 'N/A') if hasattr(self, 'data_feed') else 'N/A',
                    "platform": getattr(self.data_feed, 'PLATFORM', 'N/A') if hasattr(self, 'data_feed') else 'N/A',
                    "symbol_mapping_version": getattr(self.data_feed, 'MAPPING_VERSION', 'N/A') if hasattr(self, 'data_feed') else 'N/A',
                    "market_timestamp": ts,
                    "local_receipt_timestamp": local_ts,
                    "signal_timestamp": decision_start_time,
                    "decision_timestamp": decision_end_time,
                    "feed_observation_latency": feed_latency,
                    "signal_processing_latency": signal_processing_latency,
                    "feed_implementation_sha": "mt5_feed_sha_placeholder"
                }
                
        # 3. Execution logic
        if self.event_machine.state == "ENTRY_PENDING" and tick["symbol"] == self.identity["opportunity_market"]:
            entry_report = self.paper_execution.execute_entry(self.active_trade, tick, decision_end_time)
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
                "latency_ms": entry_report["latency_ms"] if "latency_ms" in entry_report else signal_processing_latency,
                "transaction_cost": entry_report["cost_bps"]
            })
            
        if self.event_machine.state == "IN_POSITION" and tick["symbol"] == self.identity["opportunity_market"]:
            entry_time = self.active_trade.get("entry_time")
            if ts >= entry_time + pd.Timedelta(minutes=60):
                self.event_machine.trigger_exit(ts)
                
        if self.event_machine.state == "EXIT_PENDING" and tick["symbol"] == self.identity["opportunity_market"]:
            exit_report = self.paper_execution.execute_exit(self.active_trade, tick, decision_end_time)
            self.event_machine.handle_exit(exit_report, ts)
            
            self.active_trade["paper_exit"] = exit_report["execution_price"]
            
            direction = self.active_trade["signal_direction"]
            entry_px = self.active_trade["paper_entry"]
            exit_px = self.active_trade["paper_exit"]
            intended_entry = self.active_trade["intended_entry_price"]
            
            # Quote execution difference
            if direction == 1:
                gross = (exit_px - entry_px) / entry_px * 10000
                q_diff = (entry_px - intended_entry) / intended_entry * 10000
            else:
                gross = (entry_px - exit_px) / entry_px * 10000
                q_diff = (intended_entry - entry_px) / intended_entry * 10000
                
            net = gross - self.active_trade["transaction_cost"]
            
            self.active_trade["gross_result"] = gross
            self.active_trade["quote_execution_difference"] = q_diff
            self.active_trade["net_result"] = net
            self.active_trade["net_paper_result"] = net
            self.active_trade["state"] = "CLOSED"
            self.active_trade["theoretical_reference_price"] = intended_entry
            self.active_trade["paper_execution_price"] = entry_px
            self.active_trade["bid"] = tick["bid"]
            self.active_trade["ask"] = tick["ask"]
            
            self.ledger.record_trade(self.active_trade)
            self.event_count += 1
            self.paper_trade_count += 1
            self.active_trade = None
