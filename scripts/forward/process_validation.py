"""
Process validation utilities for QuantForge Forward Runner.

Provides robust verification that a supervisor process is actually alive,
not just recorded in a stale status file.

Authoritative source: Windows process list, NOT status.json.
"""

import os
import sys
import json
import subprocess
from typing import Optional, Dict, Any, Tuple

# Expected identity markers for our supervisor
SUPERVISOR_SCRIPT = "quantforge_forward_supervisor.py"
SUPERVISOR_VERSION = "1.0.0-unified"


def is_process_alive(pid: int) -> bool:
    """Check if a process with the given PID exists on Windows."""
    if pid <= 0:
        return False
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.strip()
        # If the PID doesn't exist, tasklist returns "INFO: No tasks match"
        if "No tasks" in output or "no tasks" in output.lower():
            return False
        # If we get a line with the PID, it exists
        return str(pid) in output
    except Exception:
        return False


def get_process_commandline(pid: int) -> Optional[str]:
    """Get the command line of a process by PID using wmic."""
    if pid <= 0:
        return None
    try:
        result = subprocess.run(
            [
                "wmic", "process", "where",
                f"ProcessId={pid}",
                "get", "CommandLine", "/FORMAT:LIST"
            ],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout.strip()
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("CommandLine="):
                cmdline = line[len("CommandLine="):]
                return cmdline if cmdline else None
        return None
    except Exception:
        return None


def is_quantforge_supervisor(pid: int) -> bool:
    """
    Verify that the given PID is actually a QuantForge supervisor process.
    
    Checks:
    1. PID exists
    2. Process is Python
    3. Command line contains quantforge_forward_supervisor.py
    """
    if not is_process_alive(pid):
        return False
    
    cmdline = get_process_commandline(pid)
    if cmdline is None:
        return False
    
    cmdline_lower = cmdline.lower()
    if SUPERVISOR_SCRIPT.lower() not in cmdline_lower:
        return False
    
    # Also check it's a python process
    if "python" not in cmdline_lower:
        return False
    
    return True


def find_supervisor_pid() -> Optional[int]:
    """
    Find the actual running supervisor process by scanning for it.
    Returns the PID if found, None otherwise.
    """
    try:
        result = subprocess.run(
            [
                "wmic", "process", "where",
                f"CommandLine like '%{SUPERVISOR_SCRIPT}%'",
                "get", "ProcessId", "/FORMAT:LIST"
            ],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("ProcessId="):
                try:
                    pid = int(line[len("ProcessId="):])
                    if pid > 0 and is_process_alive(pid):
                        return pid
                except ValueError:
                    continue
        return None
    except Exception:
        return None


def validate_supervisor_from_status(status_path: str) -> Dict[str, Any]:
    """
    Validate the supervisor status by checking the actual process.
    
    Returns a dict with:
        - running: bool - whether the supervisor is actually running
        - pid: Optional[int] - the actual PID if running
        - status_json_state: str - what status.json claims
        - stale: bool - whether status.json is stale
        - warning: Optional[str] - warning message if stale
    """
    result = {
        "running": False,
        "pid": None,
        "status_json_state": "UNKNOWN",
        "stale": False,
        "warning": None,
    }
    
    # Read status.json if it exists
    recorded_pid = None
    if os.path.exists(status_path):
        try:
            with open(status_path, "r") as f:
                data = json.load(f)
            result["status_json_state"] = data.get("supervisor_state", "UNKNOWN")
            recorded_pid = data.get("pid")
        except Exception:
            result["status_json_state"] = "UNREADABLE"
    
    # Check if there's actually a running supervisor
    actual_pid = find_supervisor_pid()
    
    if actual_pid is not None:
        result["running"] = True
        result["pid"] = actual_pid
        if recorded_pid and recorded_pid != actual_pid:
            result["stale"] = True
            result["warning"] = (
                f"STALE STATUS RECORD DETECTED — status.json claims PID {recorded_pid} "
                f"but actual supervisor is PID {actual_pid}"
            )
    else:
        # No actual supervisor running
        if result["status_json_state"] == "RUNNING":
            result["stale"] = True
            result["warning"] = (
                f"STALE STATUS RECORD DETECTED — status.json claims RUNNING (PID {recorded_pid}) "
                f"but no supervisor process is alive"
            )
            result["status_json_state"] = "STALE_RUNNING"
    
    return result


def validate_lock_file(lock_path: str) -> Dict[str, Any]:
    """
    Validate the supervisor lock file by checking the actual process.
    
    Returns a dict with:
        - valid: bool - whether the lock is held by a live supervisor
        - stale: bool - whether the lock is stale
        - lock_pid: Optional[int] - PID from the lock file
    """
    result = {
        "valid": False,
        "stale": False,
        "lock_pid": None,
    }
    
    if not os.path.exists(lock_path):
        return result
    
    # Read lock file
    try:
        with open(lock_path, "r") as f:
            lock_data = json.load(f)
        result["lock_pid"] = lock_data.get("pid")
    except Exception:
        # Lock file exists but is unreadable/corrupt — treat as stale
        result["stale"] = True
        return result
    
    pid = result["lock_pid"]
    if pid is None:
        result["stale"] = True
        return result
    
    # Check if that PID is actually our supervisor
    if is_quantforge_supervisor(pid):
        result["valid"] = True
    else:
        result["stale"] = True
    
    return result


def validate_supervisor_for_bat() -> Tuple[bool, str, Optional[int]]:
    """
    Combined validation for BAT file use.
    
    Returns:
        (is_running, message, pid)
    """
    # First check via process scan
    actual_pid = find_supervisor_pid()
    if actual_pid is not None:
        return True, "RUNNING", actual_pid
    
    # No process found — check for stale status
    runtime_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "runtime", "forward"
    )
    status_path = os.path.join(runtime_dir, "supervisor", "status.json")
    
    if os.path.exists(status_path):
        try:
            with open(status_path, "r") as f:
                data = json.load(f)
            claimed_state = data.get("supervisor_state", "UNKNOWN")
            claimed_pid = data.get("pid")
            if claimed_state == "RUNNING":
                return False, "NOT RUNNING — STALE STATUS DETECTED", None
        except Exception:
            pass
    
    return False, "NOT RUNNING", None
