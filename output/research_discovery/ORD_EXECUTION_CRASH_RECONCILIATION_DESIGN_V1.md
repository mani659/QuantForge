# QUANTFORGE — EXECUTION CRASH RECONCILIATION DESIGN V1

## 1. Executive Verdict
**YES.** QuantForge can deterministically reconcile a process that died outside Python without losing evidence or falsely treating an incomplete execution as scientifically valid. This is achieved by binding the execution directory to an OS-level unique process identity `(PID, Process_Start_Time)` and providing a fail-closed, read-only reconciliation command that relies on evidence of process death rather than arbitrary timeouts. 

## 2. Failure Being Solved
When a research execution is catastrophically terminated by the OS (Out-Of-Memory kill, SIGKILL, power loss, or terminal closure), the Python process terminates immediately. It bypasses `try...except` and `finally` blocks, permanently stranding the `EventStudyRecorder` journal in the `RUNNING` state without generating an `execution_manifest.json`.

## 3. Current Recorder Limitation
The `EventStudyRecorder` only handles in-process exceptions. It does not record its own OS-level identity (PID or start time), does not maintain a heartbeat, and has no capacity to self-diagnose or clean up after a hard crash. A stranded `RUNNING` journal cannot be deterministically resolved by the current infrastructure without manual mutation, which violates governance.

## 4. Required Execution States
The infrastructure will explicitly distinguish:
- **STATE A (RUNNING / ALIVE)**: Process identity exists; process is active.
- **STATE B (RUNNING / STALE)**: Journal is `RUNNING`, but the process identity is provably dead.
- **STATE C (TERMINAL)**: Valid finalization reached (`COMPLETED`, `INTERRUPTED`, `INVALIDATED`).
- **STATE D (UNKNOWN / CORRUPTED)**: Process identity or journal is unreadable, ambiguous, or permissions fail. (Fails closed).

## 5. Process Identity Design
Relying on PID alone is unsafe because OS PIDs are reused. The absolute minimum identity tuple required to establish ownership safely is:
`{ "pid": 12345, "process_start_time": 1718293041.123, "execution_uuid": "EXECUTION_..." }`
This tuple is globally unique per boot cycle. The recorder will persist this to the execution directory at initialization.

## 6. Heartbeat Design
The recorder will write a lightweight heartbeat: `execution_heartbeat.json`. It will contain a monotonic timestamp, UTC timestamp, and current memory usage (RSS). 
- A delayed heartbeat alone **does not** prove death (could be system sleep or IO freeze).
- Death is proven exclusively by OS-level process absence or mismatched `Process_Start_Time`.
- The heartbeat's primary purpose is providing forensic evidence of peak resource usage leading up to the crash, not acting as a timeout trigger.

## 7. Reconciliation Design
A dedicated, read-only CLI command: `python scripts/reconcile_execution.py <execution_dir>`
It inspects the journal, identity tuple, and OS process table.
- **ALIVE**: If `(PID, Start_Time)` matches a living process, do nothing.
- **STALE / HARD-CRASHED**: If `(PID, Start_Time)` is absent or mismatched, write a terminal reconciliation record.
- **TERMINAL**: If journal is already terminal, do nothing.
- **UNKNOWN**: If data is missing or corrupted, do nothing (fails closed to manual review).

## 8. Terminal Crash State
A new terminal state will be introduced: **`CRASHED`** (or `ABORTED_EXTERNAL`).
This semantic makes it explicitly clear that:
- The execution died externally.
- There is no scientific result.
- Partial artifacts are preserved as forensics.
- The execution cannot be resumed; a fresh run requires a new UUID.

## 9. Partial Artifact Rules
Upon reconciliation, all partial artifacts (`.npy`, `.csv`, etc.) are unconditionally preserved. They are never overwritten or deleted. They remain in the original execution directory and are permanently associated with the failed execution ID. The reconciliation manifest explicitly marks the run as non-adjudicable, preventing these artifacts from ever being treated as scientific outputs.

## 10. Manifest / Provenance
External reconciliation will generate an `execution_manifest.json` on behalf of the dead process. It will identify:
- Execution UUID and original journal state (`RUNNING`).
- Process identity and detected stale state.
- Reconciliation timestamp.
- Protocol/Implementation hashes and Git HEAD (copied from `implementation_manifest.json`).
- Artifact inventory.
- Terminal status: `CRASHED`.
- **Scientific validity: FALSE / NON-ADJUDICABLE.**

## 11. Stale-Run Detection
A run is eligible for reconciliation ONLY IF there is OS-level proof of death:
- The PID does not exist in the OS process table.
- The PID exists, but its `Process_Start_Time` differs from the recorded identity.
- The machine's current boot time is strictly later than the recorded `Process_Start_Time`.
Timeouts/elapsed time are explicitly forbidden as a method of determining process death.

## 12. Concurrent Execution Safety
Safety is guaranteed by the UUID-prefixed directory and the strict `(PID, Start_Time)` tuple. A reconciliation command targeting UUID-A will only check the PID assigned to UUID-A. It cannot mutate UUID-B. It cannot accidentally resume a process, as reconciliation is strictly a state-closing operation.

## 13. Reboot / Power-Loss Handling
On reboot, the OS process table is cleared. Any process that restarts and happens to receive the same PID will have a new `Process_Start_Time` that is strictly greater than the machine's boot time. Because the old run's `Process_Start_Time` was before the boot time, the tuple mismatch is guaranteed, and the crashed run is safely identified as dead.

## 14. Resource/Termination Evidence
To address the OOM issue forensically, the heartbeat daemon will periodically record the process's Peak Working Set / RSS. When an OS OOM kill occurs, the final heartbeat will contain the memory footprint just milliseconds before termination, providing exact proof of the resource limit breach without altering the ORD scientific logic.

## 15. Fail-Closed Conditions
Reconciliation will refuse to mutate and return `UNKNOWN` if:
- PID or Start Time are missing from the execution directory.
- The journal is unreadable or malformed.
- The execution UUID in the files does not match the directory name.
- File system permissions prevent verifying integrity.
If in doubt, NO MUTATION occurs, forcing manual governance review.

## 16. Security
The mechanism will only record PID, start time, timestamps, and process memory statistics. It will never capture environment variables, secrets, credentials, or arbitrary OS logs. It will never rewrite Git history or research artifacts.

## 17. Test Strategy
The test suite must cover:
1. Normal completion (reconciler does nothing).
2. Python exception (reconciler does nothing, already `INVALIDATED`).
3. Graceful interruption (reconciler does nothing).
4. External process kill (`SIGKILL` simulation -> reconciler marks `CRASHED`).
5. OS OOM termination simulation.
6. PID reuse (mocked OS process with different start time).
7. Stale heartbeat (process alive but delayed heartbeat -> no mutation).
8. Active process with delayed heartbeat.
9. Reboot/restart (mocked OS boot time).
10. Corrupted journal.
11. Missing manifest.
12. Partial artifact directory.
13. Concurrent execution isolation.
14. Stale execution plus new execution simultaneously.
15. Reconciliation idempotency (running it twice does nothing the second time).
These tests must mathematically prove that reconciliation can never turn an incomplete execution into a scientifically valid execution.

## 18. EventStudyRecorder Integration
The recorder will be minimally augmented. At `preflight()`, it writes `process_identity.json` capturing the OS tuple. During `start()`, it spawns a lightweight daemon thread that wakes every few seconds to overwrite `execution_heartbeat.json` with current memory stats. The recorder's existing scientific gates, hash checks, and completion logic remain entirely untouched.

## 19. Scientific Firewall
The watchdog and reconciliation CLI are strictly infrastructure. They have zero knowledge of market names, bootstraps, horizons, returns, or scientific classification. A reconciled `CRASHED` execution is fundamentally sealed and permanently non-adjudicable.

## 20. Recommended Architecture
**A — PID + EXECUTION ID + HEARTBEAT + RECONCILIATION CLI**
This is the leanest, most deterministic architecture. It avoids the complexity of a standing supervisor service (which itself could crash). A simple CLI command provides exact closure without modifying the core research environment's scientific responsibilities.

## 21. Exact Next Task
> **EXECUTION INFRASTRUCTURE WATCHDOG / RECONCILIATION IMPLEMENTATION**

## 22. Integrity
- **No execution:** Confirmed.
- **No code changes:** Confirmed.
- **No Git changes:** Confirmed.
- **No scientific results:** Confirmed.
- **Artifacts untouched:** Confirmed.
