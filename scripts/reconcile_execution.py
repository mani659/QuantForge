import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
import psutil
import hashlib


def sha256_file(path: Path) -> str:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Reconcile crashed execution directories deterministically.")
    parser.add_argument("execution_dir", type=str, help="Path to execution directory")
    args = parser.parse_args()

    exec_dir = Path(args.execution_dir).resolve()
    
    if not exec_dir.is_dir():
        print(f"UNKNOWN: Execution directory not found: {exec_dir}")
        sys.exit(0)
        
    journal_path = exec_dir / "execution_journal.json"
    process_id_path = exec_dir / "process_identity.json"
    impl_manifest_path = exec_dir / "implementation_manifest.json"
    
    if not journal_path.is_file():
        print(f"UNKNOWN: Missing execution_journal.json in {exec_dir}")
        sys.exit(0)
        
    try:
        with open(journal_path, "r", encoding="utf-8") as f:
            journal = json.load(f)
    except Exception as e:
        print(f"UNKNOWN: Malformed execution_journal.json: {e}")
        sys.exit(0)
        
    current_state = journal.get("state")
    if current_state in ("COMPLETED", "INTERRUPTED", "INVALIDATED", "CRASHED"):
        print(f"TERMINAL: State is already {current_state}. NO MUTATION.")
        sys.exit(0)
        
    if current_state != "RUNNING":
        print(f"UNKNOWN: Unexpected state {current_state}. NO MUTATION.")
        sys.exit(0)
        
    if not process_id_path.is_file():
        print(f"UNKNOWN: Missing process_identity.json. Cannot verify ownership. NO MUTATION.")
        sys.exit(0)
        
    try:
        with open(process_id_path, "r", encoding="utf-8") as f:
            process_id = json.load(f)
    except Exception as e:
        print(f"UNKNOWN: Malformed process_identity.json: {e}")
        sys.exit(0)
        
    recorded_pid = process_id.get("pid")
    recorded_start_time = process_id.get("process_start_time")
    recorded_uuid = process_id.get("execution_id")
    
    if recorded_pid is None or recorded_start_time is None or recorded_uuid is None:
        print(f"UNKNOWN: Incomplete process_identity.json. NO MUTATION.")
        sys.exit(0)
        
    if recorded_uuid != exec_dir.name:
        print(f"UNKNOWN: Execution ID mismatch ({recorded_uuid} != {exec_dir.name}). NO MUTATION.")
        sys.exit(0)
        
    # Process Verification
    is_dead = False
    try:
        current_boot_time = psutil.boot_time()
        # Strong evidence of death: machine rebooted after process started
        if recorded_start_time < current_boot_time:
            is_dead = True
        else:
            p = psutil.Process(recorded_pid)
            if p.create_time() != recorded_start_time:
                is_dead = True
    except psutil.NoSuchProcess:
        is_dead = True
    except Exception as e:
        print(f"UNKNOWN: Process lookup failed: {e}. NO MUTATION.")
        sys.exit(0)
        
    if not is_dead:
        print(f"ALIVE: Process {recorded_pid} is alive. NO MUTATION.")
        sys.exit(0)
        
    # State: RUNNING / STALE
    print(f"STALE: Process {recorded_pid} is dead. Reconciling to CRASHED.")
    
    try:
        with open(impl_manifest_path, "r", encoding="utf-8") as f:
            impl_manifest = json.load(f)
    except Exception as e:
        print(f"UNKNOWN: implementation_manifest.json missing or malformed: {e}. NO MUTATION.")
        sys.exit(0)
        
    # Inventory partial artifacts
    observed = []
    artifact_hashes = {}
    for p in exec_dir.iterdir():
        if p.is_file() and p.name != "execution_manifest.json":
            observed.append(p.name)
            artifact_hashes[p.name] = sha256_file(p)
            
    # Load expected artifacts from recorder assumption (we don't strictly have the list in impl_manifest)
    # However, for forensic preservation, the exact missing list is less important than preserving everything.
    # We will record missing as "UNKNOWN_DUE_TO_CRASH"
    
    reconciliation_manifest = {
        "execution_identity": recorded_uuid,
        "execution_dir": str(exec_dir),
        "original_state": "RUNNING",
        "final_state": "CRASHED",
        "pid": recorded_pid,
        "recorded_process_start_time": recorded_start_time,
        "observed_process_state": "DEAD",
        "reconciliation_timestamp": datetime.now(timezone.utc).isoformat(),
        "protocol_sha256": impl_manifest.get("protocol_sha256"),
        "implementation_identity": impl_manifest.get("entry_script_sha256"),
        "git_head": impl_manifest.get("git_head"),
        "expected_artifacts": [], # not strictly captured in impl_manifest, recorder usually tracks it
        "observed_artifacts": observed,
        "missing_artifacts": ["UNKNOWN_DUE_TO_CRASH"],
        "unexpected_artifacts": [],
        "artifact_hashes": artifact_hashes,
        "scientific_validity": False,
        "scientific_adjudication": "NOT_ADJUDICABLE",
        "reconciliation_reason": "Process died outside Python lifecycle without finalization."
    }
    
    # Write execution_manifest.json
    manifest_path = exec_dir / "execution_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(reconciliation_manifest, f, indent=2)
        
    # Update execution_journal.json
    journal["state"] = "CRASHED"
    journal["timestamp"] = datetime.now(timezone.utc).isoformat()
    journal["reason"] = "EXTERNAL_PROCESS_DEATH_RECONCILED"
    
    with open(journal_path, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=2)
        
    print(f"SUCCESS: Execution {recorded_uuid} formally reconciled as CRASHED.")

if __name__ == "__main__":
    main()
