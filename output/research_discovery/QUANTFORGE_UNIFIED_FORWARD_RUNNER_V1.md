# QUANTFORGE UNIFIED FORWARD RUNNER V1

## 1. Mission

Replace multiple forward-runner architecture with ONE simple manual forward
runner whose ONLY purpose is to gather prospective market observations/logs
for all currently authorized forward candidates.

This is NOT System Assembly. This is NOT strategy combination. This is NOT
signal aggregation. This is NOT portfolio construction. This is NOT risk
management. It is simply: ONE PROCESS RUNNING MULTIPLE INDEPENDENT CANDIDATE
OBSERVERS.

## 2. Architecture

```
                  ONE BAT
                    │
                    ▼
              ONE RUNNER
                    │
              ONE MT5 FEED
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      C015        C024        C035
     own rules   own rules   own rules
     own log     own log     own log
     own state   own state   own state
```

The runner obtains market data ONCE from the MT5 terminal and passes the
appropriate data to each independently governed candidate engine.

Each candidate keeps its own: contract, state, event detection, counters,
ledger, outcome, health, status.

No candidate's output may modify another candidate.

## 3. One BAT Launcher

`run_quantforge_forward.bat`

- Starts detached Python process via `start "" /b`
- Checks singleton lock before launching
- Returns control to operator after verifying lock creation

## 4. One Python Runner

`quantforge_forward_supervisor.py`

- Singleton process with file lock
- Shared MT5 market data connection
- Module registry with independent observers
- Main loop: get quote → distribute to all modules → write status → sleep

## 5. One MT5 Connection

- Read-only market data via MetaTrader5 Python package
- Server: Exness-MT5Trial15
- Symbol: USTECm (broker) → USATECHIDXUSD (logical)
- Mapping: `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`

## 6. Independent Candidates

### CAND-015 (Adapter-Integrated)

- Canonical: PROTECTED (dictionary-based identity, not hash-verified)
- Engine: `Cand015SignalEngine` from `research/g6_forward/signal_engine.py`
- Adapter: `scripts/forward/cand015_adapter.py`
- Interface: `process_tick()` with M1 bar data
- Data: USATECHIDXUSD M1 bars via adapter (USTECm → USATECHIDXUSD mapping)
- Note: BTCUSD data buffered but not used in current signal evaluation
- Status: ACTIVE (adapter-based integration, semantic不变)

### CAND-024

- Canonical: `CAND-024:CANONICAL:925495a8`
- Status: ACTIVE
- Count: `0 / 3 / 5`

### CAND-035

- Canonical: `CAND-035:CANONICAL:ddc5d0e9`
- Status: ACTIVE
- Count: `0 / 3 / 5`

## 7. CAND-015 Boundary

The CAND-015 adapter translates the shared MT5 feed into the interface that
the existing frozen engine expects:

- Runner provides: current quote (bid/ask/timestamp)
- Adapter fetches: latest completed M1 bar from MT5
- Adapter maps: USTECm → USATECHIDXUSD
- Adapter calls: `engine.process_tick(tick)` with M1 bar data
- Engine evaluates: shock detection, ATR calculation, lockout

The adapter does NOT rewrite the engine. The engine's internal logic (pandas
resampling, Wilder's ATR, M5/D1 calculations) remains unchanged.

Cold start: engine accumulates M1 bars over time. No signals until 30 days
of M5 bars are available for ATR calculation.

## 8. Future Candidate Registry

The runner registry supports `enabled = true` for future authorized modules.
Adding a candidate means: register adapter, register contract, register
runtime directory. It should NOT require another BAT, another MT5 connection,
or another Python process.

## 9. Independent Ledgers

Each candidate writes to separate directories:

```
runtime/forward/cand_015/
runtime/forward/cand_024/
runtime/forward/cand_035/
runtime/forward/supervisor/
```

Each candidate has: `status.json`, `event_ledger.jsonl`, `outcome_ledger.jsonl`,
`health.jsonl`. Ledgers are append-only. No merging.

## 10. Status

`status_quantforge_forward.bat` displays:

- Runner state, PID, uptime
- MT5 connection state, broker, server
- Logical symbol, broker symbol, mapping
- CAND-015: status, architectural note, event count
- CAND-024: status, canonical hash, event count
- CAND-035: status, canonical hash, event count

No combined strategy metrics.

## 11. Singleton

If `run_quantforge_forward.bat` is executed twice, the second invocation
reports "SUPERVISOR ALREADY RUNNING — PID XXXX" and exits.

## 12. Detached Execution

BAT uses `start "" /b` to launch detached. No hidden Windows services. No
Task Scheduler requirements. No background infrastructure beyond the one
Python process.

## 13. Shutdown

`stop_quantforge_forward.bat` writes `shutdown.req`. Runner detects file and
exits cleanly, releasing lock.

## 14. Feed Failure

If MT5 disconnects, runner attempts reconnect with exponential backoff.
Modules receive no quotes during outage. No fake NO_EVENT records.

## 15. Contract Validation

Runner validates CAND-024/CAND-035 canonical contracts at startup. If a
candidate's contract fails, that candidate is disabled. Others continue.

## 16. Timeline Preservation

CAND-024/CAND-035 valid canonical resume: `2026-08-27T12:05:15Z`
Preserved across consolidation. No counter reset.

## 17. Runtime Migration

Pre-existing supervisor data preserved. No state lost during consolidation.
CAND-015 adapter created fresh (no prior state to migrate).

## 18. Tests

52/52 passed:

- Canonical contracts: 10
- Engine consistency: 4
- Module registry: 8 (including CAND-015 adapter tests)
- Paper execution: 3
- Module processing: 3
- Supervisor: 4
- Ledgers: 3
- Market data: 3
- Status: 2
- Shutdown: 2
- BAT files: 5
- Canonical identity: 3
- CAND-015 integration: 2

## 19. Smoke Test

Synthetic data. No events counted toward qualification. All observers
initialize correctly.

## 20. Real Feed Test

MT5 connected. USTECm fresh. M1 bar retrieval verified. No events counted.

## 21. Task Scheduler

NOT REQUIRED. Manual BAT is canonical entry point. If old scheduler task
exists, it is not depended upon.

## 22. Operator Workflow

```
START:  run_quantforge_forward.bat
CHECK:  status_quantforge_forward.bat
STOP:   stop_quantforge_forward.bat
```

After PC restart: user manually starts `run_quantforge_forward.bat`.

## 23. Known Limitations

- CAND-015 cold start requires ~30 days of M1 data accumulation before
  signals can fire (ATR calculation requires 8641 M5 bars)
- CAND-015 BTCUSD data is buffered but not used in current engine logic
- CAND-015 uses pandas/numpy (heavier dependencies than CAND-024/035)

## 24. Integrity

- No signal combination
- No portfolio logic
- No shared decision-making
- No inter-module state
- No live orders
- No Task Scheduler dependency
- Each candidate: independent rules, independent state, independent logs
