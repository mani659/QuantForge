# QUANTFORGE UNIFIED FORWARD LAUNCHER OPERATOR AUDIT V1

## 1. User Requirement

One BAT → one command prompt → MT5 terminal ensured available → one forward
runner → independent candidate observers. Visible operator console. Clear
status messages for all conditions.

## 2. Previous BAT Behavior

- Checked lock file only
- Used `start "" /b` to run Python detached (command prompt closed immediately)
- Said "Supervisor may already be running" when lock existed (vague)
- Did not ensure MT5 terminal was running
- Did not set `QF_MT5_TERMINAL_PATH`
- Operator saw no command prompt after launch

## 3. Current Supervisor

- PID 6924 (running throughout audit)
- Mode: FORWARD
- CAND-024: ACTIVE, 0/3/5
- CAND-035: ACTIVE, 0/3/5
- CAND-015: ACTIVE / PROTECTED (adapter)

## 4. Root Cause of Silent Launch

The BAT used `start "" /b` which runs Python in background. The command
prompt window closed immediately after launch. The operator had no visible
feedback that the runner started.

When already running, the BAT printed a vague message and exited with code 1.

## 5. MT5 Startup Behavior

- MT5 terminal: `C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe`
- Python supervisor calls `mt5.initialize()` which connects to existing terminal
- If terminal not running, `mt5.initialize()` fails → "STARTUP BLOCKED"
- Previous BAT did not launch MT5 itself

## 6. Singleton Behavior

- Lock file: `runtime/forward/supervisor/supervisor.lock`
- Python supervisor uses `msvcrt.locking()` for file lock
- Lock contains JSON with PID, startup time, hostname, version
- If lock exists: prints "SUPERVISOR ALREADY RUNNING" and exits

## 7. New BAT Behavior

### Already Running
```
QUANTFORGE FORWARD RUNNER ALREADY RUNNING
PID: 6924
Started: 2026-08-27T...

Use status_quantforge_forward.bat to check status.
Use stop_quantforge_forward.bat to stop.
```

### MT5 Not Running
```
MT5 terminal not running. Starting Exness MT5...
Waiting for MT5 to initialize...
```

### Normal Start
```
Checking MT5 terminal...
MT5 terminal already running.

Starting QuantForge Forward Supervisor...
CAND-015 + CAND-024 + CAND-035

Press Ctrl+C to stop, or use stop_quantforge_forward.bat
```

### MT5 Not Found
```
WARNING: MT5 terminal not found at: ...
Please start MetaTrader 5 manually and re-run this BAT.
```

## 8. Command Window

Visible by default. Python runs in foreground (no `start /b`). Command
window shows all supervisor output. Closes when user presses Ctrl+C or
closes the window.

## 9. Broker Validation

- Expected: Exness-MT5Trial15
- Shown in supervisor startup output
- Status display reads from supervisor telemetry (not independent connection)

## 10. Symbol Validation

- Broker: USTECm
- Logical: USATECHIDXUSD
- Mapping: MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0

## 11. Supervisor Feed Validation

Status display now labels MT5 as "MT5 (from supervisor telemetry)" to
distinguish from independent status script connection.

## 12. CAND-015

> ACTIVE / PROTECTED / ADAPTER-INTEGRATED

## 13. CAND-024

> ACTIVE — 0 / 3 / 5

Canonical: `CAND-024:CANONICAL:925495a8`

## 14. CAND-035

> ACTIVE — 0 / 3 / 5

Canonical: `CAND-035:CANONICAL:ddc5d0e9`

## 15. Qualification Timeline

Preserved: original `2026-08-27T09:44:58Z`, valid resume `2026-08-27T12:05:15Z`

## 16. Task Scheduler

> NOT REQUIRED

Manual BAT is canonical entry point.

## 17. Final Operator Workflow

```
START:  run_quantforge_forward.bat
        → MT5 ensured available
        → One command prompt opens
        → Supervisor starts with clear status
        → CAND-015 + CAND-024 + CAND-035 observed

CHECK:  status_quantforge_forward.bat
        → Shows supervisor telemetry (PID, MT5, modules, counts)

STOP:   stop_quantforge_forward.bat
        → Sends shutdown request
        → Supervisor exits cleanly
```

## 18. Tests

130/130 pass (52 forward + 78 contract)

## 19. No Signal Combination

Confirmed. Each candidate observes independently.

## 20. No Portfolio Logic

Confirmed. No shared decision-making.

## 21. Paper Safety

No live / demo / real order.
