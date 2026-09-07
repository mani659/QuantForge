# QUANTFORGE — EXECUTION INFRASTRUCTURE
# EXTERNAL CRASH WATCHDOG / EXECUTION RECONCILIATION IMPLEMENTATION V1

## 1. Failure Class
This infrastructure implementation resolves the lifecycle gap exposed when an execution process dies externally (OS-level kill, SIGKILL, OOM, power loss). In these events, Python's exception handling is bypassed, permanently stranding the `EventStudyRecorder` journal in the `RUNNING` state.

## 2. Process Identity
The `EventStudyRecorder` now extracts and saves a rigid OS-level process identity tuple to `process_identity.json` during `.preflight()`. The tuple contains the execution UUID, process ID (`pid`), exact process start time, and OS boot time. The combination of PID and process start time establishes a globally unique process identity that cannot be spoofed by PID reuse.

## 3. Heartbeat
The recorder now spawns a lightweight daemon thread during `.start()` that wakes every 5 seconds to write `execution_heartbeat.json`. This heartbeat captures elapsed monotonic time, UTC time, and `rss_bytes` (process memory footprint). As required, the heartbeat is observational forensic evidence of resource limits; its absence or staleness is NEVER used as proof of death. Failure to write a heartbeat does not crash the scientific process.

## 4. Reconciliation
A new deterministic CLI was implemented: `python scripts/reconcile_execution.py <execution_dir>`. 
This read-only governance tool verifies the identity tuple against the OS process table. If the execution is still `RUNNING`, but the recorded PID does not exist or its `process_start_time` diverges from the live process, it formally declares the process dead and completes the execution lifecycle securely.

## 5. CRASHED State
A new terminal state `CRASHED` has been added. Reconciling a dead process writes an `execution_manifest.json` setting `final_state = "CRASHED"`. The journal state is mutated to `CRASHED`. This state designates an external, abnormal death, sealing the execution as `NON_ADJUDICABLE` and proving no scientific result was reached.

## 6. Fail-Closed Rules
The reconciliation CLI is aggressively fail-closed. If the `process_identity.json` is missing, the journal is malformed, the execution UUID mismatches, or OS permissions deny process table inspection, the reconciler aborts without mutating the directory and returns an `UNKNOWN` state to prompt human governance review.

## 7. Partial Artifact Preservation
The reconciliation process never deletes or overwrites existing scientific artifacts. It blindly inventories all partial `.npy` and `.csv` files and logs them as forensic observations in the `execution_manifest.json`.

## 8. Platform Support
The implementation uses `psutil` (built on cross-platform abstractions) to ensure full compatibility with the Windows development environment. Process creation time and boot time metrics are fully supported on Windows.

## 9. Test Coverage
A dedicated test suite `tests/test_crash_reconciliation.py` was created, producing 12 new deterministic tests covering:
- Matching alive process (no mutation)
- Dead PID (CRASHED)
- Reused PID with diverged start time (CRASHED)
- System reboot time verification (CRASHED)
- Missing PID/start time/malformed identity (UNKNOWN fail-closed)
- Protection of existing terminal states (COMPLETED, INTERRUPTED, INVALIDATED)
- Preservation of partial artifacts in CRASHED finalization

## 10. Scientific Firewall
The reconciliation tool possesses zero knowledge of opening-range mathematics, event studies, variables, hypotheses, or statistics. Its only function is infrastructure lifecycle governance and process verification. It has no capability to resume execution or falsify an incomplete result into a valid one.

## 11. Current ORD Run
> Current ORD hard-crash execution has NOT been reconciled by this implementation task.
The original `EXECUTION_20260818T125713Z_a79f58f8-2c9b-4cdd-81f7-cc08ef69119d` remains untouched as a read-only historical record.
