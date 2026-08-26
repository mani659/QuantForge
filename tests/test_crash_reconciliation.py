import os
import shutil
import tempfile
import uuid
import json
import subprocess
import pytest
from pathlib import Path
from datetime import datetime, timezone
import psutil

RECONCILE_SCRIPT = Path(__file__).parent.parent / "scripts" / "reconcile_execution.py"

@pytest.fixture
def setup_reconciliation_env():
    temp_dir = Path(tempfile.mkdtemp())
    exec_uuid = str(uuid.uuid4())
    exec_dir = temp_dir / f"EXECUTION_20260818T000000Z_{exec_uuid}"
    exec_dir.mkdir(parents=True)
    
    # Write default RUNNING journal
    journal = {
        "execution_id": exec_dir.name,
        "state": "RUNNING",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    with open(exec_dir / "execution_journal.json", "w") as f:
        json.dump(journal, f)
        
    # Write default implementation_manifest
    impl = {
        "execution_id": exec_dir.name,
        "protocol_sha256": "dummy_sha",
        "entry_script_sha256": "dummy_sha",
        "git_head": "dummy_head"
    }
    with open(exec_dir / "implementation_manifest.json", "w") as f:
        json.dump(impl, f)
        
    # Default valid process identity (mocked as current live process)
    p = psutil.Process()
    proc_id = {
        "execution_id": exec_dir.name,
        "pid": p.pid,
        "process_start_time": p.create_time(),
        "boot_time": psutil.boot_time()
    }
    with open(exec_dir / "process_identity.json", "w") as f:
        json.dump(proc_id, f)
        
    yield {
        "temp_dir": temp_dir,
        "exec_dir": exec_dir,
        "proc_id": proc_id,
        "journal": journal
    }
    
    shutil.rmtree(temp_dir)

def run_reconciler(exec_dir):
    result = subprocess.run(
        ["python", str(RECONCILE_SCRIPT), str(exec_dir)],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def get_journal(exec_dir):
    with open(exec_dir / "execution_journal.json") as f:
        return json.load(f)

def test_1_running_matching_process(setup_reconciliation_env):
    """1. running process with matching PID/start time -> ALIVE (no mutation)."""
    env = setup_reconciliation_env
    out = run_reconciler(env["exec_dir"])
    assert "ALIVE:" in out
    assert get_journal(env["exec_dir"])["state"] == "RUNNING"

def test_2_dead_pid(setup_reconciliation_env):
    """2. dead PID -> CRASHED."""
    env = setup_reconciliation_env
    # Mutate process_id to an impossible/dead PID
    env["proc_id"]["pid"] = 999999
    with open(env["exec_dir"] / "process_identity.json", "w") as f:
        json.dump(env["proc_id"], f)
        
    out = run_reconciler(env["exec_dir"])
    assert "STALE:" in out
    assert "SUCCESS:" in out
    assert get_journal(env["exec_dir"])["state"] == "CRASHED"
    assert (env["exec_dir"] / "execution_manifest.json").exists()

def test_3_pid_reused_diff_start_time(setup_reconciliation_env):
    """3. PID reused with different start time -> CRASHED."""
    env = setup_reconciliation_env
    # Keep current PID, but change start time to simulate it's an old process
    env["proc_id"]["process_start_time"] -= 10000.0
    with open(env["exec_dir"] / "process_identity.json", "w") as f:
        json.dump(env["proc_id"], f)
        
    out = run_reconciler(env["exec_dir"])
    assert "STALE:" in out
    assert get_journal(env["exec_dir"])["state"] == "CRASHED"

def test_6_reboot_mismatch(setup_reconciliation_env):
    """6. reboot/boot-time mismatch -> CRASHED."""
    env = setup_reconciliation_env
    # Process start time is before current boot time
    env["proc_id"]["process_start_time"] = psutil.boot_time() - 10000.0
    with open(env["exec_dir"] / "process_identity.json", "w") as f:
        json.dump(env["proc_id"], f)
        
    out = run_reconciler(env["exec_dir"])
    assert "STALE:" in out
    assert get_journal(env["exec_dir"])["state"] == "CRASHED"

def test_7_missing_pid(setup_reconciliation_env):
    """7. missing PID -> UNKNOWN."""
    env = setup_reconciliation_env
    del env["proc_id"]["pid"]
    with open(env["exec_dir"] / "process_identity.json", "w") as f:
        json.dump(env["proc_id"], f)
        
    out = run_reconciler(env["exec_dir"])
    assert "UNKNOWN:" in out
    assert get_journal(env["exec_dir"])["state"] == "RUNNING"

def test_9_malformed_journal(setup_reconciliation_env):
    """9. malformed journal -> UNKNOWN."""
    env = setup_reconciliation_env
    with open(env["exec_dir"] / "execution_journal.json", "w") as f:
        f.write("{ bad json }")
        
    out = run_reconciler(env["exec_dir"])
    assert "UNKNOWN:" in out

def test_10_execution_uuid_mismatch(setup_reconciliation_env):
    """10. execution UUID mismatch -> UNKNOWN."""
    env = setup_reconciliation_env
    env["proc_id"]["execution_id"] = "EXECUTION_OTHER"
    with open(env["exec_dir"] / "process_identity.json", "w") as f:
        json.dump(env["proc_id"], f)
        
    out = run_reconciler(env["exec_dir"])
    assert "UNKNOWN:" in out
    assert get_journal(env["exec_dir"])["state"] == "RUNNING"

@pytest.mark.parametrize("terminal_state", ["COMPLETED", "INTERRUPTED", "INVALIDATED", "CRASHED"])
def test_terminal_states(setup_reconciliation_env, terminal_state):
    """12-15. already terminal -> NO MUTATION."""
    env = setup_reconciliation_env
    env["journal"]["state"] = terminal_state
    with open(env["exec_dir"] / "execution_journal.json", "w") as f:
        json.dump(env["journal"], f)
        
    out = run_reconciler(env["exec_dir"])
    assert "TERMINAL:" in out
    assert get_journal(env["exec_dir"])["state"] == terminal_state

def test_16_partial_artifacts_preserved(setup_reconciliation_env):
    """16. partial artifact directory -> CRASHED while preserving all artifacts."""
    env = setup_reconciliation_env
    # Create partial artifacts
    (env["exec_dir"] / "bootstrap_XAUUSD.npy").write_text("data")
    env["proc_id"]["pid"] = 999999
    with open(env["exec_dir"] / "process_identity.json", "w") as f:
        json.dump(env["proc_id"], f)
        
    out = run_reconciler(env["exec_dir"])
    assert "SUCCESS:" in out
    
    # Verify artifact preserved
    assert (env["exec_dir"] / "bootstrap_XAUUSD.npy").exists()
    
    # Verify manifest details
    with open(env["exec_dir"] / "execution_manifest.json") as f:
        manifest = json.load(f)
    assert manifest["final_state"] == "CRASHED"
    assert "bootstrap_XAUUSD.npy" in manifest["observed_artifacts"]
    assert manifest["scientific_validity"] is False
    assert manifest["scientific_adjudication"] == "NOT_ADJUDICABLE"

