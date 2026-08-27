import os
import sys
import time
import json
import socket
import argparse
from datetime import datetime

# Windows-specific locking
try:
    import msvcrt
except ImportError:
    msvcrt = None

from market_data import MT5MarketFeed
from module_registry import get_registry
from supervisor_health import SupervisorHealthMonitor

# We want to record the exact start time to match the historical qualification clock, 
# if not already passed via arg or config. The user instructed to explicitly record
# the old observation gap and start. We'll do that in status.json.
HISTORICAL_START = "2026-08-27T09:44:58Z"
MIGRATION_TIME = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

class Supervisor:
    def __init__(self, mode, base_runtime_dir):
        self.mode = mode
        self.base_runtime_dir = base_runtime_dir
        self.supervisor_dir = os.path.join(base_runtime_dir, "supervisor")
        os.makedirs(self.supervisor_dir, exist_ok=True)
        
        self.lock_file_path = os.path.join(self.supervisor_dir, "supervisor.lock")
        self.shutdown_req_path = os.path.join(self.supervisor_dir, "shutdown.req")
        self.status_file = os.path.join(self.supervisor_dir, "status.json")
        self.health_ledger = SupervisorHealthMonitor(os.path.join(self.supervisor_dir, "supervisor_health.jsonl"))
        
        self.modules = get_registry(base_runtime_dir)
        self.feed = MT5MarketFeed()
        self.startup_time = time.time()
        self.uptime_seconds = 0
        self.reconnect_count = 0
        self.restart_count = 0
        self.reconnect_delay = 1
        self.max_reconnect_delay = 30
        self.last_heartbeat = 0
        self.version = "1.0.0-unified"
        
        self.lock_fd = None
        self.running = False

    def acquire_lock(self):
        if not msvcrt:
            print("Warning: msvcrt not available. Singleton lock is best-effort.")
            return True
            
        try:
            self.lock_fd = open(self.lock_file_path, "w")
            msvcrt.locking(self.lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
            
            # Write lock info
            lock_data = {
                "pid": os.getpid(),
                "startup_utc": MIGRATION_TIME,
                "hostname": socket.gethostname(),
                "supervisor_version": self.version
            }
            json.dump(lock_data, self.lock_fd)
            self.lock_fd.flush()
            return True
        except Exception:
            try:
                with open(self.lock_file_path, "r") as f:
                    data = json.load(f)
                    print(f"SUPERVISOR ALREADY RUNNING — PID {data.get('pid', 'UNKNOWN')}")
            except:
                print("SUPERVISOR ALREADY RUNNING — UNABLE TO READ PID")
            if self.lock_fd:
                self.lock_fd.close()
            return False

    def release_lock(self):
        if self.lock_fd and msvcrt:
            try:
                self.lock_fd.seek(0)
                msvcrt.locking(self.lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
                self.lock_fd.close()
                os.remove(self.lock_file_path)
            except Exception:
                pass

    def check_shutdown(self):
        return os.path.exists(self.shutdown_req_path)

    def process_shutdown(self):
        print("Shutdown requested via control file. Stopping safely...")
        self.save_status(state="STOPPING")
        if self.feed:
            self.feed.shutdown()
        # Clean up req file
        try:
            os.remove(self.shutdown_req_path)
        except:
            pass
        self.save_status(state="STOPPED")
        print("Shutdown complete.")
        
    def save_status(self, state="RUNNING"):
        self.uptime_seconds = time.time() - self.startup_time
        term_info = self.feed.terminal_info() if self.feed else {"broker": "UNKNOWN", "server": "UNKNOWN"}
        
        status = {
            "supervisor_state": state,
            "mode": self.mode,
            "pid": os.getpid(),
            "startup_timestamp": self.startup_time,
            "qualification_clock_start": HISTORICAL_START,
            "uptime_seconds": self.uptime_seconds,
            "mt5_connection": self.feed.connection_state() if self.feed else "DISCONNECTED",
            "broker": term_info["broker"],
            "server": term_info["server"],
            "reconnect_count": self.reconnect_count,
            "restart_count": self.restart_count,
            "last_heartbeat": self.last_heartbeat,
            "version": self.version,
            "modules_loaded": len(self.modules)
        }
        
        temp_file = self.status_file + ".tmp"
        try:
            with open(temp_file, "w") as f:
                json.dump(status, f, indent=2)
            os.replace(temp_file, self.status_file)
        except Exception:
            pass

    def run(self):
        if not self.acquire_lock():
            sys.exit(1)
            
        print(f"QuantForge Unified Forward Supervisor v{self.version} started.")
        self.running = True
        self.save_status("STARTING")

        if self.mode == "forward" or self.mode == "verify-feed":
            if not self.feed.initialize():
                print("STARTUP BLOCKED: MT5 initialization failed.")
                self.release_lock()
                sys.exit(1)

        if self.mode == "verify-feed":
            self.run_verify_feed()
            self.feed.shutdown()
            self.release_lock()
            return
            
        if self.mode == "smoke":
            print("SMOKE TEST MODE ENABLED - Modules running with synthetic feed.")
        
        # Ensure initial state is clean
        if self.check_shutdown():
            os.remove(self.shutdown_req_path)
            
        self.save_status("RUNNING")

        while self.running:
            if self.check_shutdown():
                self.process_shutdown()
                break

            current_time = time.time()
            if self.mode == "forward":
                conn_state = self.feed.connection_state()
                if conn_state != "CONNECTED":
                    print(f"Feed disconnected. Backing off {self.reconnect_delay}s")
                    time.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                    self.reconnect_count += 1
                    self.save_status("RUNNING")
                    continue
                    
                # The feed acts as shared market state. Modules might have different logical symbols 
                # but currently both use USATECHIDXUSD mapped to USTECm.
                # To be generic, we query the broker symbol needed by our modules.
                # Since both need USTECm, we query it once.
                broker_symbol = "USTECm"
                quote_res = self.feed.latest_quote(broker_symbol)
                
                if quote_res.get("status") != "DATA_FRESH":
                    status_str = quote_res.get("status", "FEED_UNAVAILABLE")
                    # Do NOT treat as NO_EVENT
                    time.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                    continue
                else:
                    self.reconnect_delay = 1
            else:
                # Smoke mode: generate synthetic
                quote_res = {
                    "status": "DATA_FRESH",
                    "symbol": "USTECm",
                    "bid": 15000 + (int(current_time) % 100),
                    "ask": 15002 + (int(current_time) % 100),
                    "source_timestamp": current_time,
                    "age": 0.1
                }
                time.sleep(1) # mock polling rate

            # Distribute quote to modules
            for module in self.modules:
                # Reconstruct quote with module's logical mapping
                mod_quote = {
                    "utc_timestamp": quote_res['source_timestamp'],
                    "symbol": module.config['logical_symbol'],
                    "broker_symbol": quote_res['symbol'],
                    "mapping_id": module.config['mapping_id'],
                    "bid": quote_res['bid'],
                    "ask": quote_res['ask'],
                    "age": quote_res.get('age', 0)
                }
                module.process_quote(mod_quote, f"supervisor_pid_{os.getpid()}")

            # Heartbeat every ~60 seconds based on current time
            if int(current_time) % 60 == 0 and current_time - self.last_heartbeat >= 60:
                self.last_heartbeat = current_time
                self.save_status("RUNNING")
                hb_data = {
                    "utc_timestamp": current_time,
                    "uptime_seconds": self.uptime_seconds,
                    "connection_state": self.feed.connection_state() if self.feed else "MOCK",
                    "reconnect_count": self.reconnect_count,
                    "modules": {m.candidate_id: m.engine.state for m in self.modules}
                }
                self.health_ledger.record_heartbeat(hb_data)

            if self.mode == "forward":
                time.sleep(1) # Base polling

        self.release_lock()

    def run_verify_feed(self):
        print("Running read-only MT5 feed verification...")
        print(f"Connection State: {self.feed.connection_state()}")
        info = self.feed.terminal_info()
        print(f"Broker: {info['broker']} | Server: {info['server']}")
        quote = self.feed.latest_quote("USTECm")
        print(f"Latest Quote: {quote}")
        bar = self.feed.latest_completed_bar("USTECm", "M1")
        print(f"Completed M1 Bar: {bar}")
        print("Read-only verification completed safely.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["smoke", "forward", "verify-feed"], required=True)
    args = parser.parse_args()
    
    # We resolve runtime dir from the script path:
    # __file__ is in scripts/forward/
    # runtime should be in runtime/forward/
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    runtime_dir = os.path.join(base_dir, "runtime", "forward")
    
    supervisor = Supervisor(mode=args.mode, base_runtime_dir=runtime_dir)
    supervisor.run()
