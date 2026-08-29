"""
Process validation utilities for QuantForge Forward Runner.

Provides robust verification that a supervisor process is actually alive,
not just recorded in a stale status file.

Authoritative source: Windows process list, NOT status.json.

Uses PowerShell (Get-CimInstance Win32_Process) instead of deprecated WMIC.
"""

import os
import sys
import json
import subprocess
from typing import Optional, Dict, Any, Tuple

SUPERVISOR_SCRIPT = "quantforge_forward_supervisor.py"


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
        if "No tasks" in output or "no tasks" in output.lower():
            return False
        return str(pid) in output
    except Exception:
        return False


def find_supervisor_pid() -> Optional[int]:
    """
    Find the actual running supervisor process via PowerShell.
    Returns the PID if found, None otherwise.
    
    Uses Get-CimInstance Win32_Process (replaces deprecated WMIC).
    Filters for python processes whose CommandLine contains the supervisor script.
    """
    try:
        ps_cmd = (
            "Get-CimInstance Win32_Process | "
            "Where-Object { $_.CommandLine -like '*quantforge_forward_supervisor.py*' -and "
            "$_.Name -like 'python*' } | "
            "Select-Object -First 1 -ExpandProperty ProcessId"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        if output:
            try:
                pid = int(output.splitlines()[0].strip())
                if pid > 0 and is_process_alive(pid):
                    return pid
            except (ValueError, IndexError):
                pass
        return None
    except Exception:
        return None


def validate_supervisor_from_status(status_path: str) -> Dict[str, Any]:
    """
    Validate the supervisor status by checking the actual process.
    
    Returns a dict with:
        - running: bool
        - pid: Optional[int]
        - status_json_state: str
        - stale: bool
        - warning: Optional[str]
    """
    result = {
        "running": False,
        "pid": None,
        "status_json_state": "UNKNOWN",
        "stale": False,
        "warning": None,
    }

    recorded_pid = None
    if os.path.exists(status_path):
        try:
            with open(status_path, "r") as f:
                data = json.load(f)
            result["status_json_state"] = data.get("supervisor_state", "UNKNOWN")
            recorded_pid = data.get("pid")
        except Exception:
            result["status_json_state"] = "UNREADABLE"

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
        - valid: bool
        - stale: bool
        - lock_pid: Optional[int]
    """
    result = {
        "valid": False,
        "stale": False,
        "lock_pid": None,
    }

    if not os.path.exists(lock_path):
        return result

    try:
        with open(lock_path, "r") as f:
            lock_data = json.load(f)
        result["lock_pid"] = lock_data.get("pid")
    except Exception:
        result["stale"] = True
        return result

    pid = result["lock_pid"]
    if pid is None:
        result["stale"] = True
        return result

    if is_process_alive(pid):
        # Check it's actually a python process
        try:
            ps_cmd = (
                f"Get-CimInstance Win32_Process -Filter 'ProcessId={pid}' | "
                f"Select-Object -ExpandProperty Name"
            )
            r = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True, text=True, timeout=5
            )
            name = r.stdout.strip().lower()
            if "python" in name:
                result["valid"] = True
            else:
                result["stale"] = True
        except Exception:
            result["stale"] = True
    else:
        result["stale"] = True

    return result
