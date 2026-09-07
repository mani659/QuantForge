# QUANTFORGE MANUAL LAUNCHER FINAL FIX V1

Date: 2026-08-29
Status: COMPLETE
Classification: Launcher UX/Runtime Detection Fix

---

## 1. Incident

`run_quantforge_forward.bat` had two problems:

1. Used deprecated WMIC for process detection, which behaves inconsistently on newer Windows 10 builds and can return the querying process itself.
2. Had no `pause` on failure paths — when double-clicked from Windows Explorer, any startup failure caused the CMD window to close immediately with no diagnostic information.

---

## 2. Root Cause

The WMIC query `wmic process where "CommandLine like '%%quantforge_forward_supervisor.py%%'"` could return the WMIC command itself, causing false-positive detection. Additionally, the BAT had no `pause >nul` on error paths, so double-click launches failed silently.

---

## 3. WMIC Replacement

All WMIC-based process detection replaced with PowerShell `Get-CimInstance Win32_Process`:

```powershell
Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -like '*quantforge_forward_supervisor.py*' -and
    $_.Name -like 'python*'
} | Select-Object -First 1 -ExpandProperty ProcessId
```

This reliably finds the supervisor by command-line content while excluding the querying process (filtered by `Name -like 'python*'`).

---

## 4. Actual Process Detection

The actual Windows process is the authoritative source for RUNNING/NOT RUNNING. PowerShell queries the live process table. A persisted status file or lock file is metadata only.

Hierarchy:
```
REAL PROCESS → actual running/not running
status.json  → metadata only
lock file    → coordination only
```

---

## 5. Stale Lock Handling

If `supervisor.lock` exists but no valid supervisor process is found:
- BAT prints "STALE SUPERVISOR LOCK DETECTED — Removing stale lock..."
- Safely removes the lock
- Proceeds with fresh startup

---

## 6. Stale Status Handling

If `status.json` claims RUNNING but the actual process is not found:
- `status.py` prints "NOT RUNNING" with "STALE STATUS RECORD DETECTED" warning
- Never reports RUNNING for a dead process

---

## 7. MT5 Startup

BAT checks `tasklist /FI "IMAGENAME eq terminal64.exe"`:
- If running: prints "MT5 terminal already running."
- If not running: launches `C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe` and waits 8 seconds
- If executable not found: prints "FORWARD START BLOCKED" with reason, pauses

---

## 8. Python Startup

BAT verifies Python is available before any other logic:
```bat
python --version >nul 2>&1
```
If unavailable: prints clear failure message and pauses.

---

## 9. Visible Console

The BAT runs in foreground. No `start /b`, no hidden PowerShell, no detached process. The command window stays open because the user wants to monitor the experiment directly.

---

## 10. Already-Running Behavior

If a real supervisor is detected:
```
========================================
 QUANTFORGE FORWARD RUNNER
========================================

 SUPERVISOR ALREADY RUNNING

 PID: <actual PID>

 Use status_quantforge_forward.bat
 to inspect the live system.

 Use stop_quantforge_forward.bat
 to stop it.
```
Then pauses (visible for double-click). No silent exit.

---

## 11. Event Console

Event notifications remain: DETECTED, CAPTURED, COMPLETED. Deduplication via `(event_id, event_state)`. No heartbeat/tick/NO_EVENT spam.

---

## 12. Status

`status_quantforge_forward.bat` → `status.py` verifies actual process via PowerShell before reporting RUNNING.

---

## 13. Stop

`stop_quantforge_forward.bat` uses PowerShell to find the actual supervisor, then sends `shutdown.req` and waits up to 30 seconds for clean exit.

---

## 14. Double-Click Test

BAT prints banner immediately. All failure paths include `pause >nul` so the window stays visible when launched from Windows Explorer.

---

## 15. Restart Test

```
run_quantforge_forward.bat → starts
stop_quantforge_forward.bat → stops
run_quantforge_forward.bat → starts again cleanly
```

---

## 16. CAND-015

Status: ACTIVE / PROTECTED (adapter-based, semantic unchanged)

---

## 17. CAND-024

Status: ACTIVE — 0 / 3 / 5
Canonical: `CAND-024:CANONICAL:925495a8`

---

## 18. CAND-035

Status: ACTIVE — 0 / 3 / 5
Canonical: `CAND-035:CANONICAL:ddc5d0e9`

---

## 19. Contracts

No modification to contract hashes, strategy semantics, or qualification state.

---

## 20. Qualification Timeline

Preserved: CAND-024 0/3/5, CAND-035 0/3/5
Original intended: `2026-08-27T09:44:58Z`
Valid canonical resume: `2026-08-27T12:05:15Z`

---

## 21. Task Scheduler

NOT REQUIRED. Manual BAT is the canonical entry point.

---

## 22. Operator Workflow

```
Double-click run_quantforge_forward.bat
→ visible CMD opens
→ banner appears
→ MT5 ensured
→ supervisor starts
→ console remains visible
→ major events printed
→ stop_quantforge_forward.bat to stop
→ manually run BAT again next time
```

---

## 23. Integrity

- No live/demo/real orders (paper-only)
- No signal combination across candidates
- No portfolio logic
- Independent event ledgers per candidate
- CAND-015 adapter architecture preserved
- CAND-024/CAND-035 canonical contracts unchanged
- Research results not modified
- 116/116 tests passing
