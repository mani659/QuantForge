# QUANTFORGE OPERATOR RUNTIME CORRECTION V1

Date: 2026-08-29
Status: COMPLETE
Classification: Runtime Architecture Correction

---

## 1. Incident

After a PC reboot on 2026-08-29, `status_quantforge_forward.bat` reported:

```
Supervisor: RUNNING
PID: 5080
Uptime: 717.6 seconds
```

Subsequent investigation revealed:

```
tasklist /FI "PID eq 5080"
→ No tasks are running which match the specified criteria.
```

```
wmic process where "CommandLine like '%%quantforge_forward_supervisor.py%%'" ...
→ No results.
```

**Conclusion**: status.json was stale. PID 5080 had died (likely during the reboot), but the persisted status file was never updated. The status script trusted the file blindly and reported a phantom process as alive.

**Root Cause**: The status script and launcher used file existence (`supervisor.lock`, `status.json`) as proof of process liveness. Neither verified the actual Windows process.

---

## 2. Stale Status Problem

`status.json` contained:

```json
{
  "supervisor_state": "RUNNING",
  "pid": 5080,
  "uptime_seconds": 717.577
}
```

The status script read this file and reported its contents without verifying the PID was alive. A persisted file is metadata, not runtime truth. The actual Windows process list is the authoritative source.

**Fix**: `status.py` now calls `find_supervisor_pid()` which scans for the actual process via `wmic`. Only if the real process is found does it report RUNNING.

---

## 3. Stale Lock Problem

`supervisor.lock` contained:

```json
{"pid": 5080, "startup_utc": "2026-08-27T13:43:02Z"}
```

The launcher (`run_quantforge_forward.bat`) checked for lock file existence and refused to start if present. It did not verify that the lock PID was alive.

**Fix**: The launcher now scans for the actual supervisor process via `wmic`. It only claims "already running" if the process is positively verified. Stale locks are cleaned automatically on startup.

---

## 4. Actual Process Authority

The fundamental principle established:

> **A persisted status file is NOT proof that the process is alive.**

The actual Windows process is the authoritative runtime state. All monitoring, launch decisions, and stop commands must verify the real process first.

Implementation:
- `process_validation.py` provides `find_supervisor_pid()`, `is_quantforge_supervisor()`, `is_process_alive()`
- These scan `wmic` for `CommandLine like '%quantforge_forward_supervisor.py%'`
- PID reuse protection: verify the PID is a Python process with the correct command line

---

## 5. Launcher Behavior

`run_quantforge_forward.bat` now:

1. Scans for an actual running supervisor process (not just lock file)
2. Verifies the found PID is alive and is our supervisor
3. If confirmed: reports PID and suggests status/stop commands
4. If no process found: cleans stale lock, starts fresh
5. No Task Scheduler, no hidden services, no background processes

---

## 6. MT5 Startup

The launcher checks for `terminal64.exe` via `tasklist`. If not running, launches:

```
C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe
```

The supervisor Python code additionally verifies:
- Broker: `Exness Technologies Ltd`
- Server: `Exness-MT5Trial15`
- Symbol: `USTECm` accessible

If any check fails, startup is blocked with a clear error message.

---

## 7. Visible Console

The operator gets a normal visible Command Prompt window. No hidden service mode, no Task Scheduler, no invisible PowerShell, no detached background processes. The window stays open while the experiment runs.

---

## 8. LIVE Banner

On successful startup, the console displays:

```
========================================
 QUANTFORGE FORWARD RUNNER
========================================

MT5:
CONNECTED

Broker:
Exness Technologies Ltd

Server:
Exness-MT5Trial15

Logical Market:
USATECHIDXUSD

Broker Symbol:
USTECm

Mapping:
MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0

Modules:
3

  CAND-015: ACTIVE / PROTECTED
  CAND-024: ACTIVE
  CAND-035: ACTIVE

Runner:
LIVE AND RUNNING

PID: <actual pid>

Press Ctrl+C to stop,
or use stop_quantforge_forward.bat
```

---

## 9. Major Event Notification

When a genuine candidate event transition occurs, the console prints:

```
============================================================
 QUANTFORGE EVENT
============================================================
Candidate: CAND-024
State: DETECTED
Event ID: <event-id>
Event Time UTC: <timestamp>
Logical Market: USATECHIDXUSD
Broker Symbol: USTECm
Canonical: 925495a8
============================================================
```

---

## 10. Event Deduplication

Each event is identified by `(event_id, event_state)`. The same combination is printed only once:

- `CAND-024 DETECTED` → printed
- `CAND-024 DETECTED` again → suppressed
- `CAND-024 CAPTURED` → printed (different state)
- `CAND-024 COMPLETED` → printed (different state)

Normal polling, NO_EVENT, heartbeats, and routine operations produce no console output.

---

## 11. Status Validation

`status_quantforge_forward.bat` → `status.py` now:

1. Calls `find_supervisor_pid()` to scan for the real process
2. If found: reports RUNNING with actual PID and uptime from process creation time
3. If not found but status.json says RUNNING: reports NOT RUNNING with STALE warning
4. Validates lock file: if stale, shows STALE LOCK DETECTED warning
5. Computes uptime from actual process start time, not status.json

---

## 12. Stop Behavior

`stop_quantforge_forward.bat` now:

1. Scans for the actual supervisor process
2. If not found: prints "Supervisor not running" and exits
3. If found: sends `shutdown.req`, waits up to 30 seconds
4. Verifies process termination
5. Does not claim success for a non-existent process

---

## 13. Restart After Stop

The operator workflow works cleanly:

```
run_quantforge_forward.bat → runner starts
stop_quantforge_forward.bat → runner stops
run_quantforge_forward.bat → runner starts again cleanly
```

No stale locks. No stale status. No duplicate processes.

---

## 14. PC Restart Behavior

After a PC restart:

1. Nothing starts automatically
2. User runs `run_quantforge_forward.bat`
3. Launcher cleans any stale lock from previous run
4. MT5 starts if needed
5. Supervisor verifies broker/server/symbol
6. Console shows LIVE banner with actual PID

---

## 15. Task Scheduler

Task Scheduler is explicitly NOT REQUIRED for this architecture.

The manual launcher is the sole entry point. No automatic background execution, no scheduled tasks, no hidden services.

---

## 16. CAND-015

Status: ACTIVE / PROTECTED

Architecture: adapter-based (`Cand015Adapter`)

The unified runner calls its adapter. Signal semantics (ATR/M5/D1/BTCUSD) are not modified.

---

## 17. CAND-024

Status: ACTIVE — 0 / 3 / 5

Canonical: `CAND-024:CANONICAL:925495a8`

Full hash: `925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e`

---

## 18. CAND-035

Status: ACTIVE — 0 / 3 / 5

Canonical: `CAND-035:CANONICAL:ddc5d0e9`

Full hash: `ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5`

---

## 19. Contracts

Contract identity is preserved and tested:

- CAND-024: `CAND-024:CANONICAL:925495a8` ✓
- CAND-035: `CAND-035:CANONICAL:ddc5d0e9` ✓

No modification to contract hashes, strategy semantics, or qualification state.

---

## 20. Tests

Regression test suite: `scripts/forward/tests/test_process_validation.py`

| Category | Tests | Status |
|---|---|---|
| Process Alive | 5 | ALL PASS |
| Command Line | 4 | ALL PASS |
| Supervisor Detection | 5 | ALL PASS |
| Find PID | 4 | ALL PASS |
| Status Validation | 6 | ALL PASS |
| Lock Validation | 5 | ALL PASS |
| Stale Lock (Supervisor) | 3 | ALL PASS |
| Status Display | 1 | PASS |
| Event Console | 5 | ALL PASS |
| BAT Content | 8 | ALL PASS |
| Startup Banner | 1 | PASS |
| Uptime | 5 | ALL PASS |
| Paper Safety | 2 | ALL PASS |
| Candidate Independence | 4 | ALL PASS |
| Contract Firewall | 5 | ALL PASS |
| **Total New Tests** | **63** | **ALL PASS** |

Existing forward runtime tests: **54** ALL PASS

Combined: **117 tests passing**

---

## 21. Operator Workflow

```
USER DECIDES TO RUN EXPERIMENT
        ↓
double-click / run_quantforge_forward.bat
        ↓
NORMAL VISIBLE COMMAND PROMPT
        ↓
MT5 TERMINAL OPENS / ENSURES IT IS OPEN
        ↓
QuantForge Forward Runner starts
        ↓
CONSOLE SHOWS:
  SYSTEM LIVE
  MT5 CONNECTED
  CAND-015 ACTIVE
  CAND-024 ACTIVE
  CAND-035 ACTIVE
        ↓
NORMAL OPERATION = QUIET
        ↓
MAJOR EVENT OCCURS
        ↓
PRINT EVENT TO CONSOLE
        ↓
stop_quantforge_forward.bat
        ↓
NEXT TIME: manually run BAT again
```

---

## 22. Integrity

- No live/demo/real order capability (paper-only)
- No signal combination across candidates
- No portfolio logic
- No cross-candidate filtering
- Independent event ledgers per candidate
- Independent outcome ledgers per candidate
- CAND-015 adapter architecture preserved
- CAND-024/CAND-035 canonical contracts unchanged
- Qualification timeline preserved (0 / 3 / 5)
- Research results not modified
- Runtime ledgers not committed
- Forward data not committed
