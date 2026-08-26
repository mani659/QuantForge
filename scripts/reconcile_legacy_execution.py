import json
import sys
from pathlib import Path
from datetime import datetime, timezone
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
    target_uuid = "EXECUTION_20260818T125713Z_a79f58f8-2c9b-4cdd-81f7-cc08ef69119d"
    target_dir = Path("output/research_discovery/ORD/V1.1.0") / target_uuid
    protocol_sha = "85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06"
    exception_path = Path("output/research_discovery/ORD_V1_1_0_LEGACY_CRASH_GOVERNANCE_EXCEPTION_V1.md")

    # 1. Exact execution directory name matches
    if not target_dir.exists():
        print("STOP — Directory does not exist.")
        sys.exit(1)

    journal_path = target_dir / "execution_journal.json"
    impl_path = target_dir / "implementation_manifest.json"
    manifest_path = target_dir / "execution_manifest.json"
    process_id_path = target_dir / "process_identity.json"

    # Validation
    if process_id_path.exists():
        print("STOP — process_identity.json exists, not a legacy execution.")
        sys.exit(1)

    if manifest_path.exists():
        print("STOP — execution_manifest.json already exists.")
        sys.exit(1)

    with open(journal_path, "r", encoding="utf-8") as f:
        journal = json.load(f)

    # 2. journal execution ID matches
    if journal.get("execution_id") != target_uuid:
        print("STOP — Journal execution_id mismatch.")
        sys.exit(1)

    # 3. journal current state = RUNNING
    if journal.get("state") != "RUNNING":
        print("STOP — Journal state is not RUNNING.")
        sys.exit(1)

    with open(impl_path, "r", encoding="utf-8") as f:
        impl = json.load(f)

    # 4. implementation manifest execution ID matches
    if impl.get("execution_id") != target_uuid:
        print("STOP — Implementation execution_id mismatch.")
        sys.exit(1)

    # 5. protocol SHA matches
    if impl.get("protocol_sha256") != protocol_sha:
        print("STOP — Protocol SHA mismatch.")
        sys.exit(1)

    # 6. governance exception artifact exists
    if not exception_path.exists():
        print("STOP — Exception artifact does not exist.")
        sys.exit(1)

    # 7. governance exception verdict
    with open(exception_path, "r", encoding="utf-8") as f:
        exception_text = f.read()
    if "EXCEPTION APPROVED — CLASSIFY AS CRASHED" not in exception_text:
        print("STOP — Exception verdict is missing or not approved.")
        sys.exit(1)

    # Inventory partial artifacts
    observed = []
    for p in target_dir.iterdir():
        if p.is_file() and p.name != "execution_manifest.json":
            observed.append(p.name)
            
    reconciliation_timestamp = datetime.now(timezone.utc).isoformat()

    # 8. Create execution manifest
    manifest = {
        "execution_id": target_uuid,
        "original_state": "RUNNING",
        "final_state": "CRASHED",
        "protocol_sha256": protocol_sha,
        "implementation_identity": impl.get("entry_script_sha256"),
        "git_head": impl.get("git_head"),
        "original_execution_timestamp": impl.get("start_timestamp"),
        "reconciliation_timestamp": reconciliation_timestamp,
        "governance_exception_identifier": "LEGACY_PRE_PROCESS_IDENTITY_GOVERNANCE_EXCEPTION",
        "observed_artifacts": observed,
        "missing_expected_artifacts": ["UNKNOWN_DUE_TO_CRASH"],
        "unexpected_artifacts": [],
        "scientific_validity": False,
        "scientific_adjudication": "NOT_ADJUDICABLE",
        "reconciliation_reason": "LEGACY_PRE_PROCESS_IDENTITY_GOVERNANCE_EXCEPTION"
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    # 7. Write execution_journal.json
    journal["state"] = "CRASHED"
    journal["reconciliation_reason"] = "LEGACY_PRE_PROCESS_IDENTITY_GOVERNANCE_EXCEPTION"
    journal["governance_exception_identifier"] = "LEGACY_PRE_PROCESS_IDENTITY_GOVERNANCE_EXCEPTION"
    journal["reconciliation_timestamp"] = reconciliation_timestamp
    journal["legacy_no_process_identity"] = True

    with open(journal_path, "w", encoding="utf-8") as f:
        json.dump(journal, f, indent=2)

    print("SUCCESS: Legacy execution transitioned to CRASHED.")

if __name__ == "__main__":
    main()
