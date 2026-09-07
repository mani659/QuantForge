# QUANTFORGE — WINDOWS FORWARD SUPERVISOR PERSISTENCE HARDENING
# CAND-024 + CAND-035
# CONFIGURATION ONLY
# DO NOT INTERRUPT ACTIVE OBSERVATION
# CAND-015 PROTECTED
# NO RESEARCH EXECUTION

## 1. Current Scheduler State

Task Name: `QuantForgeForwardSupervisor`

Status: Ready (configured but not triggered by scheduler — supervisor was started manually)

Logon Mode: Interactive only

User: User10

Trigger: At system startup (BootTrigger)

Action: `cmd.exe /c ""C:\Users\User10\Documents\MRV\yuvi\QuantForge\run_quantforge_forward.bat"""`

Start In: N/A (not specified in task configuration)

Stop Task After: 72:00:00 (72 hours)

Restart Settings: None configured (RestartCount=0)

Power Management: Stop On Battery Mode, No Start On Batteries

Idle Behavior: Disabled (Duration=PT10M, WaitTimeout=PT1H, StopOnIdleEnd=true)

Last Result: 267011 (task has never been successfully triggered by scheduler)

Last Run Time: 11/30/1999 12:00:00 AM (never run by scheduler)

Next Run Time: N/A

Task History: Not available via schtasks /query

XML Configuration confirms:
- LogonType: InteractiveToken
- MultipleInstancesPolicy: IgnoreNew (singleton)
- ExecutionTimeLimit: PT72H (default, not explicitly set)
- RestartCount: 0
- RestartInterval: not set

## 2. Active Supervisor State

PID: 6924

Mode: FORWARD

MT5: CONNECTED

Broker: Exness Technologies Ltd

Server: Exness-MT5Trial15

Uptime: 904.1 seconds (at time of audit)

CAND-024: ACTIVE — 0 / 3 / 5

CAND-035: ACTIVE — 0 / 3 / 5

CAND-015: PROTECTED / EXTERNAL

Canonical Contracts Verified:
- CAND-024: `925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e`
- CAND-035: `ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5`

Mapping: `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`

Process was started manually, not by the Task Scheduler.

## 3. Current 72-Hour Limit

Current value: `PT72H` (72 hours)

Source: Default `schtasks /create` behavior — the install bat script does not explicitly set an execution time limit, so Windows applies the default 72-hour limit.

Impact: After 72 hours of continuous execution, the Task Scheduler will forcefully terminate the supervisor process. This is unacceptable for a months-long observation that must run continuously.

Required change: Set `ExecutionTimeLimit` to `PT0S` (no limit) or remove the limit entirely.

## 4. Restart-on-Failure

Current state: NOT CONFIGURED (RestartCount=0, RestartInterval empty)

Impact: If the supervisor crashes (e.g., MT5 disconnection, Python exception, resource exhaustion), it will NOT automatically restart. The observation will stop until manually restarted.

Required change: Configure RestartCount=3, RestartInterval=PT1M (restart after 1 minute, up to3 attempts).

## 5. Interactive Logon Analysis

Current setting: `InteractiveToken` (Interactive only)

Analysis:
- MT5 Python IPC requires an interactive desktop session to access the MT5 terminal
- The MetaQuotes/MT5 environment is bound to the User10 interactive logon session
- Changing to non-interactive (ServiceAccount, S4U, or Group Managed Service Account) would:
  - Require a different MT5 installation or MetaQuotes profile
  - Lose access to the User10 MT5 terminal and its data
  - Break the Python-to-MT5 IPC connection
  - Invalidate the current observation

Verdict: MUST REMAIN INTERACTIVE

Rationale: The MT5 terminal and its Python IPC environment are bound to the User10 interactive logon session. Changing this would break MT5 connectivity and invalidate the forward observation.

## 6. User Context

Current: `Run As User10`

Verdict: RETAIN — the MT5 terminal and MetaQuotes profile are bound to this user context.

Do NOT switch to SYSTEM — the same MT5 terminal/data environment would not be accessible.

## 7. Startup Configuration

Current: At system startup (BootTrigger)

Action: `cmd.exe /c ""C:\Users\User10\Documents\MRV\yuvi\QuantForge\run_quantforge_forward.bat"""`

The bat script uses `cd /d "%~dp0"` to change to the script's own directory, which is an absolute path. This is correct.

## 8. Working Directory

Current: Not specified in task (Start In = N/A)

The bat script handles this internally with `cd /d "%~dp0"`.

This is acceptable because the bat script explicitly changes to the correct directory.

No scheduler-level correction needed.

## 9. IDE Independence

Verified:
- The bat script uses absolute paths (`%~dp0`)
- No dependency on Gemini, IDE, or agent session
- No dependency on current shell directory
- Python interpreter is resolved from system PATH
- PYTHONPATH is set explicitly in the bat script

Verdict: YES — fully IDE independent.

## 10. MT5 Accessibility

Current: MT5 is CONNECTED and accessible via the User10 interactive session.

The MT5 terminal must remain accessible through the same User10 logon session.

Changing the logon type would break MT5 accessibility.

Verdict: PRESERVED (as long as Interactive logon mode is retained).

## 11. Single Task

Verified: Exactly one task exists: `QuantForgeForwardSupervisor`

No duplicate tasks detected.

No candidate-specific scheduler tasks exist.

## 12. Single Process

The MultipleInstancesPolicy is `IgnoreNew` — if the supervisor is already running, new scheduler-triggered instances are ignored.

This preserves singleton behavior.

The currently running PID 6924 was started manually and is separate from the scheduler configuration.

## 13. Power Management

Current: Stop On Battery Mode, No Start On Batteries

For a VPS/desktop environment, this should be changed to:
- `AllowStartIfOnBatteries`: True
- `DontStopIfGoingOnBatteries`: True

This ensures the supervisor survives power state transitions.

## 14. Applied Scheduler Changes

BLOCKED — `Set-ScheduledTask` requires Administrator privileges.

The following changes are recommended but cannot be applied from a non-elevated shell:

### Required Changes (from elevated PowerShell):

```powershell
$newSettings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -AllowStartIfOnBatteries:$true `
    -DontStopIfGoingOnBatteries:$true `
    -StartWhenAvailable:$true `
    -MultipleInstances IgnoreNew

Set-ScheduledTask -TaskName QuantForgeForwardSupervisor -Settings $newSettings
```

### Alternative: Recreate from XML

Export current task, modify XML, reimport:

```powershell
# Export
schtasks /query /tn QuantForgeForwardSupervisor /xml > task.xml

# Manual edit: add <ExecutionTimeLimit>PT0S</ExecutionTimeLimit> under <Settings>
# Manual edit: add <RestartCount>3</RestartCount> and <RestartInterval>PT1M</RestartInterval>
# Manual edit: add <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
# Manual edit: add <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
# Manual edit: add <StartWhenAvailable>true</StartWhenAvailable>

# Reimport
schtasks /delete /tn QuantForgeForwardSupervisor /f
schtasks /create /tn QuantForgeForwardSupervisor /xml task.xml
```

### Alternative: Updated Install Script

Update `install_quantforge_forward_task.bat` to include hardened settings:

```bat
@echo off
setlocal

cd /d "%~dp0"

echo Installing QuantForge Forward Supervisor scheduled task...

schtasks /create /tn "QuantForgeForwardSupervisor" /tr "cmd.exe /c \"\"%~dp0run_quantforge_forward.bat\"\"" /sc onstart /ru "%USERNAME%" /rl limited /f

:: Note: schtasks /create does not support all hardening options.
:: For full hardening, use PowerShell Set-ScheduledTask from an elevated prompt.
:: See QUANTFORGE_WINDOWS_FORWARD_PERSISTENCE_HARDENING_V1.md for details.

echo.
echo Task installed. For full hardening (no 72-hour limit, restart-on-failure),
:: run the PowerShell hardening script from an elevated prompt.
```

## 15. Runtime Impact

No impact on the running supervisor (PID 6924).

Scheduler configuration changes only affect future startup/recovery behavior.

The running process is completely independent of the scheduler configuration.

No contract changes, no engine changes, no ledger changes.

## 16. Qualification Continuity

Original intended launch: `2026-08-27T09:44:58Z`

Valid canonical resume: `2026-08-27T12:05:15Z`

No integrity gap created — the running process was not interrupted.

No qualification clock changes.

## 17. CAND-024

Contract hash: `925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e`

Canonical identity: `CAND-024:CANONICAL:925495a8`

State: ACTIVE

Event count: 0 / 3 / 5

No changes.

## 18. CAND-035

Contract hash: `ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5`

Canonical identity: `CAND-035:CANONICAL:ddc5d0e9`

State: ACTIVE

Event count: 0 / 3 / 5

No changes.

## 19. CAND-015

Status: ACTIVE / PROTECTED / EXTERNAL / UNTOUCHED

No inspection, no modification.

## 20. System Assembly

Status: NOT EXECUTED

## 21. Final Persistence Classification

> OPERATIONAL — NON-CRITICAL LIMITATION REMAINS

The supervisor is running and collecting valid evidence. The72-hour execution limit is a non-critical limitation that will only affect the process if the machine reboots or the process crashes and restarts via the scheduler. The current manual start (PID 6924) will continue until the process exits or the machine reboots.

Hardening requires Administrator privileges to apply. The recommended PowerShell script is documented above.

## 22. Known Limitations

1. **72-hour execution limit remains** — Cannot be removed without Administrator privileges. If the machine reboots, the scheduler will start the supervisor but terminate it after 72 hours. Manual restart would be required.

2. **No restart-on-failure** — If the supervisor crashes, it will not automatically restart. Manual intervention required.

3. **Power management** — On battery-powered machines, the supervisor may stop. Not applicable for VPS/desktop with constant power.

4. **Interactive logon required** — MT5 binds to the interactive desktop session. This is a fundamental constraint of the MT5 Python IPC architecture.

5. **Task has never been triggered by scheduler** — The current supervisor (PID 6924) was started manually. The scheduler has never successfully triggered the task. This means the scheduler configuration has not been validated for actual startup behavior.

## 23. Integrity

Active supervisor: PID 6924, RUNNING, MT5 CONNECTED.

CAND-024: ACTIVE, canonical hash verified.

CAND-035: ACTIVE, canonical hash verified.

CAND-015: PROTECTED / EXTERNAL.

Event counters: 0/3/5 for both candidates.

Qualification continuity: PRESERVED.

No runtime changes applied.

No contract changes applied.

No scheduler changes applied (requires Administrator).

---

Hardening artifact created: 2026-08-27T12:10:00Z
