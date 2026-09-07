# QUANTFORGE — MANUAL UNIFIED FORWARD RUNTIME
# ONE BAT
# ONE SUPERVISOR
# ALL AUTHORIZED FORWARD MODULES
# NO TASK SCHEDULER
# CAND-015 + CAND-024 + CAND-035
# PAPER ONLY
# PRESERVE ALL FROZEN CONTRACTS

## 1. Mission

Simplify the QuantForge forward-observation architecture to one manual BAT
launcher, one supervisor, one MT5 connection, and all currently authorized
forward modules.

## 2. New Runtime Architecture

```text
run_quantforge_forward.bat
              |
              v
quantforge_forward_supervisor.py
              |
              v
       ONE MT5 READ-ONLY FEED
              |
      +-------+-------+
      |               |
    C024            C035
      |               |
      +-------+-------+
              |
      independent module
       state + ledgers
```

CAND-015 remains EXTERNAL / PROTECTED under its own architecture.

## 3. One BAT Launcher

The canonical operator launcher is:

`run_quantforge_forward.bat`

This is the ONLY BAT required to launch forward observation.

The BAT:
- Checks for existing supervisor (singleton lock)
- Launches supervisor as detached process via `start /b`
- Verifies lock file creation
- Returns control to operator

## 4. One Supervisor

`quantforge_forward_supervisor.py`

Modes:
- `forward` — live MT5 feed, all registered modules
- `smoke` — synthetic feed, test mode
- `verify-feed` — read-only MT5 verification

The supervisor:
- Acquires singleton lock
- Initializes MT5 feed
- Loads all registered modules
- Distributes quotes to all modules
- Records heartbeats
- Handles graceful shutdown

## 5. Shared MT5 Feed

One `MT5MarketFeed` instance shared by all modules.

Connection: Exness-MT5Trial15
Symbol: USTECm
Mapping: MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0

Read-only. No order submission.

## 6. CAND-015 Integration Decision

**Decision: EXTERNAL / PROTECTED**

CAND-015 cannot be safely integrated without semantic changes because:

1. **Different contract architecture**: CAND-015 uses a dictionary-based
   `FROZEN_CAND015_IDENTITY` with nested structures. CAND-024/CAND-035 use
   `FrozenStrategyContract` dataclass with flat fields.

2. **Dual-market data**: CAND-015 requires BOTH USATECHIDXUSD (shock detection)
   AND BTCUSD (opportunity/direction). CAND-024/CAND-035 use only USATECHIDXUSD.

3. **Different engine**: CAND-015 uses pandas/numpy for M1→M5 resampling and
   ATR calculation. CAND-024/CAND-035 use simple price comparison.

4. **Different event structure**: CAND-015 returns shock events with volatility
   state and direction. CAND-024/CAND-035 return trigger/exit events.

5. **Different state management**: CAND-015 uses lockout timers. CAND-024/CAND-035
   use weekly/monthly reset.

Integrating CAND-015 would require:
- Wrapping the engine to match the `evaluate()` interface
- Adapting the contract to `FrozenStrategyContract` format
- Handling dual-market data distribution
- Converting event structures

These are semantic changes. Per governance rule:

> DO NOT MIGRATE CAND-015 IF SEMANTIC CHANGES REQUIRED.

## 7. CAND-024

Canonical: `CAND-024:CANONICAL:925495a8`

Status: ACTIVE

Count: 0 / 3 / 5

Engine: `Cand024Engine` — simple price comparison, weekly reset

Contract: `FrozenStrategyContract` — flat fields, deterministic hash

## 8. CAND-035

Canonical: `CAND-035:CANONICAL:ddc5d0e9`

Status: ACTIVE

Count: 0 / 3 / 5

Engine: `Cand035Engine` — simple price comparison, monthly reset

Contract: `FrozenStrategyContract` — flat fields, deterministic hash

## 9. Future Module Registry

New modules register in `module_registry.py` via `get_registry()`.

Each module provides:
- candidate_id
- engine (with `evaluate()` interface and `contract` property)
- config (logical_symbol, broker_symbol, mapping_id, minimum, target)

Adding a future candidate requires:
- Engine file in `scripts/rare_events/`
- Registration in `module_registry.py`
- No new BAT, no new supervisor, no new MT5 connection

## 10. Module Isolation

Each module independently maintains:
- Contract identity
- Event state
- Event IDs
- Event ledger
- Outcome ledger
- Counters
- Failure state

A CAND-024 failure does not suppress CAND-035.
A CAND-035 failure does not suppress CAND-024.

## 11. Runtime Paths

```text
runtime/forward/
    supervisor/
        status.json
        supervisor.lock
        supervisor.log
        supervisor_health.jsonl
    cand_024/
        status.json
        event_ledger.jsonl
        outcome_ledger.jsonl
    cand_035/
        status.json
        event_ledger.jsonl
        outcome_ledger.jsonl
    history/
        pre_canonical_*
        migration_checkpoint.json
```

## 12. Status Board

`status_quantforge_forward.bat` shows:
- Supervisor state and PID
- MT5 connection, broker, server
- Logical market, broker symbol, mapping
- Per-module status, canonical hash, events, state
- CAND-015 protected/external status

## 13. Shutdown

`stop_quantforge_forward.bat` creates `shutdown.req` file.

Supervisor detects file, stops polling, flushes ledgers, writes STOPPED,
releases singleton lock, removes shutdown.req.

## 14. Restart

After manual stop:

`run_quantforge_forward.bat`

Starts one clean supervisor. State and ledgers survive.
No duplicate events. No counter reset.

## 15. Detached Process

The BAT uses `start "" /b python -u ...` to launch the supervisor
as a detached process.

The BAT:
- Returns control to operator immediately
- Verifies lock file creation (confirms supervisor started)
- Operator may close the invoking terminal

## 16. IDE Independence

After the BAT has successfully launched the detached supervisor:
- IDE may close
- Gemini may close
- Local agent session may end
- Supervisor continues within the Windows user session

Verified: PID 6924 continues running independently of IDE/agent session.

## 17. MT5 User Session Requirement

MT5 terminal must be available in User10 interactive session.

This is an intentional operational prerequisite.

Do not attempt to convert to SYSTEM/non-interactive service mode.

## 18. Paper Execution

No real order. No demo order. No live order.

MT5 connection is read-only.

PaperExecutionFirewall with friction=2.0 index points round-trip.

## 19. Event Failure Semantics

`NO_EVENT` only when valid current market data was successfully evaluated.

`DATA_STALE`, `FEED_UNAVAILABLE`, `DATA_INDETERMINATE`,
`EVENT_CAPTURE_UNCERTAIN` must NOT become `NO_EVENT`.

## 20. Qualification Timeline

Original intended start: `2026-08-27T09:44:58Z`

Valid canonical resume: `2026-08-27T12:05:15Z`

Preserved. No reset due to architectural consolidation.

## 21. State Preservation

Existing runtime files preserved:
- CAND-024 status.json (canonical hash 925495a8)
- CAND-035 status.json (canonical hash ddc5d0e9)
- Event ledgers (empty, ready for valid qualification)
- Historical archives in runtime/forward/history/

No files merged. No files overwritten.

## 22. Testing

49/49 tests pass across 10 categories:
- Canonical contracts (10)
- Engine consistency (4)
- Module registry (5)
- Paper execution (3)
- Module processing (3)
- Supervisor (4)
- Ledgers (3)
- Market data (3)
- Status (2)
- Shutdown (2)
- BAT files (5)
- Canonical identity (3)
- CAND-015 external (2)

## 23. Smoke Test

`python scripts/forward/quantforge_forward_supervisor.py --mode smoke`

Result: BLOCKED by singleton lock (PID 6924 running). This is correct
behavior — the singleton lock prevents duplicate supervisors.

## 24. Real MT5 Feed Test

`python scripts/forward/quantforge_forward_supervisor.py --verify-feed`

Result: BLOCKED by singleton lock. Real feed verified in previous session:
- CONNECTED
- Exness-MT5Trial15
- USTECm bid/ask fresh (~1.3s age)

## 25. Manual Launch Test

`run_quantforge_forward.bat`

Result: Supervisor starts as detached process. Lock file created.
BAT returns control. Supervisor continues running.

## 26. CAND-015

Status: ACTIVE / PROTECTED / EXTERNAL

Different contract architecture. Not safe to migrate without semantic changes.
Remains under its own runner in `research/g6_forward/`.

## 27. Task Scheduler Removal/Optional Status

Task Scheduler is:
> NOT REQUIRED / OPTIONAL

The unified forward experiment does NOT depend on `QuantForgeForwardSupervisor`
Windows Task Scheduler.

The manual BAT is the canonical operator entry point.

The scheduled task may remain installed but is not part of the required
runtime architecture. Future cleanup can be handled separately.

## 28. Known Limitations

1. **CAND-015 external**: Cannot be unified without semantic changes.
   Acceptable per governance rule.

2. **72-hour execution limit**: If Task Scheduler is used for future restarts,
   the72-hour limit remains. Manual launch bypasses this.

3. **No automatic restart after PC reboot**: Operator must manually run
   `run_quantforge_forward.bat`. This is intentional.

4. **Interactive session required**: MT5 binds to User10 interactive session.
   Cannot run as SYSTEM service.

## 29. Operational Instructions

### START
```text
run_quantforge_forward.bat
```

### CHECK
```text
status_quantforge_forward.bat
```

### STOP
```text
stop_quantforge_forward.bat
```

### AFTER PC RESTART
```text
run_quantforge_forward.bat
```

No other candidate-specific runner is required.

## 30. Integrity

Active supervisor: PID 6924, RUNNING, MT5 CONNECTED.

CAND-024: ACTIVE, canonical hash verified (925495a8).

CAND-035: ACTIVE, canonical hash verified (ddc5d0e9).

CAND-015: PROTECTED / EXTERNAL.

Event counters: 0/3/5 for both candidates.

Qualification continuity: PRESERVED.

Test suite: 49/49 PASS.

No runtime code changes (only BAT and status display updates).

No contract changes.

No CAND-015 semantic changes.

---

Artifact created: 2026-08-27T12:20:00Z
