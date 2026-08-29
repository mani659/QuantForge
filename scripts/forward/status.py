import os
import sys
import json
import subprocess
from datetime import datetime

# Add the forward dir to path so we can import process_validation
forward_dir = os.path.dirname(os.path.abspath(__file__))
if forward_dir not in sys.path:
    sys.path.insert(0, forward_dir)

from process_validation import (
    find_supervisor_pid,
    validate_lock_file,
)


def get_process_start_time(pid):
    """Get the creation time of a process in UTC, as a timestamp."""
    try:
        result = subprocess.run(
            [
                "wmic", "process", "where",
                f"ProcessId={pid}",
                "get", "CreationDate", "/FORMAT:LIST"
            ],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.strip()
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("CreationDate="):
                # Format: 20260827134302.123456+480
                datestr = line[len("CreationDate="):]
                # Parse YYYYMMDDHHMMSS.ffffff
                dt = datetime.strptime(datestr[:14], "%Y%m%d%H%M%S")
                return dt.timestamp()
        return None
    except Exception:
        return None


def format_uptime(seconds):
    """Format seconds into a human-readable uptime string."""
    if seconds is None or seconds < 0:
        return "uptime unavailable"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def print_status():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    runtime_dir = os.path.join(base_dir, "runtime", "forward")
    supervisor_status_path = os.path.join(runtime_dir, "supervisor", "status.json")
    supervisor_lock_path = os.path.join(runtime_dir, "supervisor", "supervisor.lock")

    print()
    print("QUANTFORGE FORWARD STATUS")
    print("=========================")

    # ── Verify actual process ──
    actual_pid = find_supervisor_pid()
    process_alive = actual_pid is not None

    # ── Read status.json for metadata ──
    sup_status = {}
    if os.path.exists(supervisor_status_path):
        try:
            with open(supervisor_status_path, "r") as f:
                sup_status = json.load(f)
        except Exception:
            pass

    recorded_state = sup_status.get("supervisor_state", "UNKNOWN")
    recorded_pid = sup_status.get("pid")

    # ── Validate lock file ──
    lock_info = validate_lock_file(supervisor_lock_path)

    print()
    print("Supervisor:")

    if process_alive:
        print("RUNNING")
        print(f"PID: {actual_pid}")
        
        # Compute uptime from actual process creation time
        creation_time = get_process_start_time(actual_pid)
        if creation_time:
            uptime = datetime.utcnow().timestamp() - creation_time
            print(f"Uptime: {format_uptime(uptime)} (from process start)")
        else:
            # Fall back to status.json if process time unavailable
            uptime = sup_status.get("uptime_seconds")
            if uptime is not None:
                print(f"Uptime: {format_uptime(uptime)} (from status record)")
            else:
                print("Uptime: uptime unavailable")
    else:
        print("NOT RUNNING")
        if recorded_state == "RUNNING":
            print()
            print("Warning:")
            print("STALE STATUS RECORD DETECTED")
            print(f"  status.json claims RUNNING (PID {recorded_pid})")
            print(f"  but no supervisor process is alive.")
        if lock_info.get("stale"):
            print()
            print("Warning:")
            print("STALE LOCK DETECTED")
            lock_pid = lock_info.get("lock_pid")
            if lock_pid:
                print(f"  supervisor.lock claims PID {lock_pid}")
                print(f"  but that process is not a live QuantForge supervisor.")

    # ── MT5 status (from last known telemetry if supervisor not alive) ──
    print()
    print("MT5:")
    if process_alive:
        print(sup_status.get("mt5_connection", "UNKNOWN"))
    else:
        print("N/A (supervisor not running)")

    print()
    print("Broker:")
    print(sup_status.get("broker", "N/A") if process_alive else "N/A")

    print()
    print("Server:")
    print(sup_status.get("server", "N/A") if process_alive else "N/A")

    print()
    print("Logical Market:")
    print("USATECHIDXUSD")

    print()
    print("Broker Symbol:")
    print("USTECm")

    print()
    print("Mapping:")
    print("MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0")

    # ── Candidate statuses ──
    for cand in ["CAND-024", "CAND-035"]:
        cand_dir = cand.lower().replace("-", "_")
        cand_status_path = os.path.join(runtime_dir, cand_dir, "status.json")
        print()
        print(f"{cand}")
        print("-" * len(cand))

        c_status = {}
        if os.path.exists(cand_status_path):
            try:
                with open(cand_status_path, "r") as f:
                    c_status = json.load(f)
            except Exception:
                pass

        if not c_status:
            print("Status:")
            print("UNKNOWN / FILE MISSING")
            continue

        if process_alive:
            print("Status:")
            print("ACTIVE")
        else:
            print("Status:")
            print("OFFLINE")

        contract_hash = c_status.get("contract_hash", "N/A")
        if len(contract_hash) > 8:
            contract_hash = contract_hash[:8]
        print()
        print("Canonical Hash:")
        print(contract_hash)

        stats = c_status.get("stats", {})
        count = stats.get("captured_count", 0)
        minimum = c_status.get("minimum", 3)
        target = c_status.get("target", 5)

        print()
        print("Events:")
        print(f"{count} / {minimum} / {target}")

        print()
        print("State:")
        print(c_status.get("current_state", "N/A"))

    # ── CAND-015 ──
    cand015_status_path = os.path.join(runtime_dir, "cand_015", "status.json")
    print()
    print("CAND-015")
    print("--------")

    c015_status = {}
    if os.path.exists(cand015_status_path):
        try:
            with open(cand015_status_path, "r") as f:
                c015_status = json.load(f)
        except Exception:
            pass

    if not c015_status:
        print("Status:")
        print("EXTERNAL / PROTECTED")
        print("Note:")
        print("Adapter-based integration. Different contract architecture.")
    else:
        if process_alive:
            print("Status:")
            print("ACTIVE (ADAPTER)")
        else:
            print("Status:")
            print("OFFLINE (ADAPTER)")
        print()
        print("Architectural Note:")
        print(c015_status.get("architectural_note", "N/A"))
        stats = c015_status.get("stats", {})
        count = stats.get("captured_count", 0)
        print()
        print("Events:")
        print(f"{count} / 3 / 5")
    print("")


if __name__ == "__main__":
    print_status()
