import os
import sys
import time
import json
import socket
import argparse
import subprocess
from datetime import datetime, timezone

# Windows-specific locking
try:
    import msvcrt
except ImportError:
    msvcrt = None

from market_data import MT5TimeoutMarketFeed, MT5MarketFeed
from mt5_timeout_manager import MT5TimeoutManager
from module_registry import get_registry
from supervisor_health import SupervisorHealthMonitor
from f01_observation_recorder import F01ObservationRecorder

HISTORICAL_START = "2026-08-27T09:44:58Z"
MIGRATION_TIME = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

SUPERVISOR_SCRIPT = "quantforge_forward_supervisor.py"


def _find_supervisor_pids():
    """Find all PIDs that are running quantforge_forward_supervisor.py via PowerShell."""
    pids = []
    try:
        ps_cmd = (
            "Get-CimInstance Win32_Process | "
            "Where-Object { $_.CommandLine -like '*quantforge_forward_supervisor.py*' -and "
            "$_.Name -like 'python*' } | "
            "Select-Object -ExpandProperty ProcessId"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if line:
                try:
                    pid = int(line)
                    if pid > 0:
                        pids.append(pid)
                except ValueError:
                    continue
    except Exception:
        pass
    return pids


def _is_pid_alive(pid):
    """Check if a PID exists on the system via tasklist."""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.strip()
        if "No tasks" in output or "no tasks" in output.lower():
            return False
        return str(pid) in output
    except Exception:
        return False


def _is_lock_stale(lock_path, current_pid):
    """Check if a lock file is stale."""
    if not os.path.exists(lock_path):
        return True
    try:
        with open(lock_path, "r") as f:
            lock_data = json.load(f)
        lock_pid = lock_data.get("pid")
    except Exception:
        return True
    if lock_pid is None:
        return True
    if lock_pid == current_pid:
        return False
    if _is_pid_alive(lock_pid):
        our_pids = _find_supervisor_pids()
        if lock_pid in our_pids:
            return False
        else:
            return True
    return True


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

        # Create MT5 timeout manager and timeout-protected feed
        self._mt5_manager = MT5TimeoutManager(
            request_timeout=5.0,
            startup_timeout=10.0,
            max_consecutive_failures=5,
        )
        self.feed = MT5TimeoutMarketFeed(self._mt5_manager)
        self.modules = get_registry(base_runtime_dir, self.feed)
        self.f01_recorder = F01ObservationRecorder(feed=self.feed)
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

        # Event deduplication
        self._printed_events = set()

        # Live display tracking
        self._last_live_display = 0
        self._live_display_interval = 10  # seconds between live status refreshes
        self._last_scan_count = 0

    def _clean_stale_lock(self):
        if _is_lock_stale(self.lock_file_path, os.getpid()):
            try:
                if os.path.exists(self.lock_file_path):
                    os.remove(self.lock_file_path)
                    print("  STALE LOCK DETECTED AND REMOVED")
            except Exception as e:
                print(f"  Warning: Could not remove stale lock: {e}")

    def acquire_lock(self):
        self._clean_stale_lock()
        if not msvcrt:
            print("Warning: msvcrt not available. Singleton lock is best-effort.")
            return True
        try:
            self.lock_fd = open(self.lock_file_path, "w")
            msvcrt.locking(self.lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
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
                lock_pid = data.get("pid", "UNKNOWN")
                if _is_pid_alive(lock_pid):
                    print("QUANTFORGE FORWARD RUNNER ALREADY RUNNING")
                    print(f"PID: {lock_pid}")
                    print(f"Started: {data.get('startup_utc', 'UNKNOWN')}")
                else:
                    print("STALE LOCK DETECTED — LOCK PID IS DEAD")
                    print(f"Stale PID: {lock_pid}")
                    print("Attempting to recover...")
                    try:
                        if self.lock_fd:
                            self.lock_fd.close()
                        os.remove(self.lock_file_path)
                        self.lock_fd = open(self.lock_file_path, "w")
                        msvcrt.locking(self.lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
                        json.dump({
                            "pid": os.getpid(),
                            "startup_utc": MIGRATION_TIME,
                            "hostname": socket.gethostname(),
                            "supervisor_version": self.version
                        }, self.lock_fd)
                        self.lock_fd.flush()
                        print("RECOVERY SUCCESSFUL — new lock acquired")
                        return True
                    except Exception as recovery_err:
                        print(f"RECOVERY FAILED: {recovery_err}")
                        return False
            except Exception:
                print("QUANTFORGE FORWARD RUNNER — UNABLE TO READ LOCK")
            print()
            print("Use status_quantforge_forward.bat to check status.")
            print("Use stop_quantforge_forward.bat to stop.")
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
        print()
        print("Shutdown requested via control file. Stopping safely...")
        self.save_status(state="STOPPING")
        if self.feed:
            self.feed.shutdown()
        # Shutdown the MT5 timeout manager
        if self._mt5_manager:
            self._mt5_manager.shutdown()
        try:
            os.remove(self.shutdown_req_path)
        except Exception:
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

    def _print_startup_banner(self, term_info):
        """Print the operator startup banner."""
        broker = term_info.get("broker", "UNKNOWN")
        server = term_info.get("server", "UNKNOWN")
        pid = os.getpid()

        print()
        print("========================================")
        print(" QUANTFORGE FORWARD RUNNER")
        print("========================================")
        print()
        print("MT5:")
        print("CONNECTED")
        print()
        print("Broker:")
        print(broker)
        print()
        print("Server:")
        print(server)
        print()
        print("Logical Market:")
        print("USATECHIDXUSD")
        print()
        print("Broker Symbol:")
        print("USTECm")
        print()
        print("Mapping:")
        print("MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0")
        print()
        print(f"Modules:")
        print(f"{len(self.modules)}")
        print()
        for m in self.modules:
            if m.candidate_id == "CAND-015":
                print(f"  {m.candidate_id}: ACTIVE / PROTECTED")
            else:
                print(f"  {m.candidate_id}: ACTIVE")
        print(f"  F-01 RECORDER: RAW CAPTURE (NO TRADING)")
        print()
        print("Runner:")
        print("LIVE AND RUNNING")
        print()
        print(f"PID: {pid}")
        print()
        print("Press Ctrl+C to stop,")
        print("or use stop_quantforge_forward.bat")
        print()

    def _print_live_status(self):
        """Print the compact live scanning display."""
        now = datetime.now(timezone.utc)
        ts = now.strftime("%H:%M:%S UTC")

        conn_state = self.feed.connection_state() if self.feed else "DISCONNECTED"
        feed_status = "OK" if conn_state == "CONNECTED" else conn_state

        print()
        print("============================================================")
        print(" QUANTFORGE FORWARD RUNNER — LIVE")
        print("============================================================")
        print()
        print("MT5:")
        print(f"{conn_state}")
        print()
        print("Broker Symbol:")
        print("USTECm")
        print()
        print("------------------------------------------------------------")
        print(" CANDIDATE MONITOR")
        print("------------------------------------------------------------")
        print()

        for m in self.modules:
            if m.candidate_id == "CAND-015":
                print("CAND-015:")
                print("ACTIVE / PROTECTED")
            else:
                state = m.engine.state
                contract_hash = m.engine.contract.hash[:8]
                stats = m.stats
                count = stats.get("captured_count", 0)
                minimum = m.config.get("minimum", 3)
                target = m.config.get("target", 5)
                print(f"{m.candidate_id}:")
                print(f"ACTIVE")
                print(f"Contract: {contract_hash}")
                print(f"Events: {count} / {minimum} / {target}")
                print(f"State: {state}")
            print()

        print("------------------------------------------------------------")
        print(" SCANNER")
        print("------------------------------------------------------------")
        print()
        print(f"Feed: {feed_status}")
        print(f"F-01 Recorder: ACTIVE (RAW CAPTURE)")
        print(f"Last Scan: {ts}")
        print(f"Runner: LIVE")
        print("============================================================")
        print()
        print("System is LIVE — scanning for authorized candidate events.")
        print("STOP: stop_quantforge_forward.bat")
        print("STATUS: status_quantforge_forward.bat")
        print()

    def _print_event_banner(self, event_state, candidate_id, event_id, contract_hash, ts_utc):
        """Print a major event banner."""
        print()
        print("============================================================")
        print(f" !!! QUANTFORGE EVENT {event_state.upper()} !!!")
        print("============================================================")
        print()
        print("Candidate:")
        print(f"{candidate_id}")
        print()
        print("Canonical:")
        print(f"{contract_hash[:8]}")
        print()
        print("Event ID:")
        print(f"{event_id}")
        print()
        print("State:")
        print(f"{event_state}")
        print()
        print("Event Time UTC:")
        print(f"{ts_utc}")
        print()
        print("Logical Market:")
        print("USATECHIDXUSD")
        print()
        print("Broker Symbol:")
        print("USTECm")
        print()
        print("============================================================")
        print()

    def _check_mt5_startup(self):
        """Check MT5 terminal and connection at startup."""
        mt5_path = os.getenv("QF_MT5_TERMINAL_PATH", "")
        mt5_running = False
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq terminal64.exe", "/NH"],
                capture_output=True, text=True, timeout=5
            )
            mt5_running = "terminal64.exe" in result.stdout
        except Exception:
            pass

        if not mt5_running:
            if mt5_path and os.path.exists(mt5_path):
                print("Launching MT5 terminal...")
                subprocess.Popen([mt5_path])
                time.sleep(8)
                try:
                    result = subprocess.run(
                        ["tasklist", "/FI", "IMAGENAME eq terminal64.exe", "/NH"],
                        capture_output=True, text=True, timeout=5
                    )
                    mt5_running = "terminal64.exe" in result.stdout
                except Exception:
                    pass
            if not mt5_running:
                return False, "FORWARD START BLOCKED\nReason: MT5 feed unavailable"

        if not self.feed.initialize():
            return False, "FORWARD START BLOCKED\nReason: MT5 initialization failed"

        term_info = self.feed.terminal_info()
        expected_server = "Exness-MT5Trial15"
        actual_server = term_info.get("server", "UNKNOWN")
        if actual_server != expected_server:
            return False, (
                f"FORWARD START BLOCKED\n"
                f"Expected: {expected_server}\n"
                f"Actual: {actual_server}"
            )

        # Verify USTECm symbol is available via timeout-protected feed
        quote = self.feed.latest_quote("USTECm")
        if quote.get("status") not in ("DATA_FRESH", "DATA_STALE"):
            return False, "FORWARD START BLOCKED\nReason: USTECm unavailable"

        return True, None

    def run(self):
        print("QuantForge Forward Runner v" + self.version)
        print(f"PID: {os.getpid()}")
        print("Verifying singleton...")

        if not self.acquire_lock():
            sys.exit(1)

        self.running = True
        self.save_status("STARTING")

        if self.mode in ("forward", "verify-feed"):
            ok, error_msg = self._check_mt5_startup()
            if not ok:
                print()
                print(error_msg)
                print()
                self.release_lock()
                sys.exit(1)

            term_info = self.feed.terminal_info()
            self._print_startup_banner(term_info)

        if self.mode == "verify-feed":
            self.run_verify_feed()
            self.feed.shutdown()
            self.release_lock()
            return

        if self.mode == "smoke":
            print("SMOKE TEST MODE ENABLED - Modules running with synthetic feed.")

        if self.check_shutdown():
            os.remove(self.shutdown_req_path)

        self.save_status("RUNNING")

        # Print initial live status
        self._print_live_status()
        self._last_live_display = time.time()

        while self.running:
            if self.check_shutdown():
                self.process_shutdown()
                break

            current_time = time.time()
            feed_ok = True

            if self.mode == "forward":
                conn_state = self.feed.connection_state()
                if conn_state != "CONNECTED":
                    feed_ok = False
                    time.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                    self.reconnect_count += 1
                    self.save_status("RUNNING")
                    # Show live status even during reconnect
                    if current_time - self._last_live_display >= self._live_display_interval:
                        self._print_live_status()
                        self._last_live_display = current_time
                    continue

                broker_symbol = "USTECm"
                quote_res = self.feed.latest_quote(broker_symbol)

                if quote_res.get("status") != "DATA_FRESH":
                    feed_ok = False
                    time.sleep(self.reconnect_delay)
                    self.reconnect_delay = min(self.reconnect_delay * 2, self.max_reconnect_delay)
                    if current_time - self._last_live_display >= self._live_display_interval:
                        self._print_live_status()
                        self._last_live_display = current_time
                    continue
                else:
                    self.reconnect_delay = 1
            else:
                quote_res = {
                    "status": "DATA_FRESH",
                    "symbol": "USTECm",
                    "bid": 15000 + (int(current_time) % 100),
                    "ask": 15002 + (int(current_time) % 100),
                    "source_timestamp": current_time,
                    "age": 0.1
                }
                time.sleep(1)

            # Distribute quote to modules
            for module in self.modules:
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

            # F-01 observation recorder: raw M1 capture sidecar (exception-safe)
            self.f01_recorder.on_tick(quote_res)

            # Heartbeat every ~60 seconds
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

            # Periodic live status refresh
            if current_time - self._last_live_display >= self._live_display_interval:
                self._print_live_status()
                self._last_live_display = current_time

            if self.mode == "forward":
                time.sleep(1)

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

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    runtime_dir = os.path.join(base_dir, "runtime", "forward")

    supervisor = Supervisor(mode=args.mode, base_runtime_dir=runtime_dir)
    supervisor.run()
