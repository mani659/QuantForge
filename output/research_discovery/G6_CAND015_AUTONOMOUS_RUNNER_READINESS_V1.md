# QUANTFORGE — CAND-015
# G6 AUTONOMOUS RUNNER READINESS REPORT
# EXNESS MT5 / DEMO / PAPER ONLY
# 2026-08-25

## 1. Objective
Enable CAND-015 forward paper observation to run for long, uncontrolled durations (e.g. overnight or 24/7) independently of the IDE/LLM process, saving monitoring overhead while securely gathering true real-time execution statistics over a larger sample.

## 2. Runner Architecture
The runner is encapsulated in `research/g6_forward/run_long_observation.py`. It is strictly an operational wrapper around the previously validated `G6Harness`. It imports the exact same frozen logic, signal engine, and immutable symbol mapping. It manages session directories, log aggregation, and connection lifecycle independently of the IDE.

## 3. Configuration
Operational parameters are exposed via command-line arguments:
- `--duration-hours` (default: 12.0)
- `--poll-interval-ms` (default: 100)
- `--output-root` (default: `output/research_discovery`)
No strategy, filter, or risk parameters are exposed or configurable, securing the strategy's frozen identity.

## 4. Session Persistence
Every execution generates a uniquely suffixed session directory (e.g., `G6_CAND015_FORWARD_001`). Previous sessions are never overwritten. 
Persistent artifacts:
- `session_manifest.json`
- `process_identity.json`
- `runner.log`
- `event_ledger.csv`
- `execution_ledger.csv`
- `session_report.md`

## 5. Heartbeat
The runner writes to `heartbeat.jsonl` continuously at intervals governed by the harness polling. It logs the MT5 status, timestamps, and active state tracking metrics independent of signal activation to ensure liveness is constantly verifiable.

## 6. Logging
Standard logging is redirected to `runner.log` to track connection lifecycles, startup verification, graceful shutdowns, and errors without polluting standard output or storing sensitive secrets.

## 7. Connection Recovery
Transient errors are safely absorbed. The wrapper sleeps for 5 seconds upon a fatal `G6Harness` connection exception, then attempts `mt5.initialize()`. Crucially, before the loop is re-entered, the required MT5 symbols are re-verified.

## 8. Safety Firewall
The wrapper strictly enforces fail-closed operations on initialization and recovery:
- `ACCOUNT_TRADE_MODE_DEMO` is verified.
- Exness symbols `USTECm` and `BTCUSDm` are verified.
- The `FORWARD_PAPER` adapter maintains total isolation from order endpoints.

## 9. Tests
10 structural tests (AA–AJ) were implemented in `tests_runner.py` verifying file generation, duration bounding, graceful termination, firewall integrity, invalid mapping rejection, and zero-event artifact generation.
All tests in the combined suite (36/36) passed successfully.

## 10. Two-Minute Smoke Test
A 2-minute (`0.033` hours) dry run was executed via the BAT file.
- The runner initialized successfully.
- MT5 demo connection established.
- Logs and heartbeat files populated.
- Process exited cleanly with code `0`.
- Zero actual orders or endpoints invoked.

## 11. Long-Run Command
The exact command to launch the recommended 12-hour overnight session from a Command Prompt or PowerShell terminal is:
```bat
run_cand015_forward.bat 12
```
This process can run safely in the background while the IDE is closed.

## 12. Known Limitations
- Machine sleep/hibernate policies must be disabled during the 12-hour run.
- Prolonged internet disconnects exceeding the session length will prevent capturing observations.

## 13. Readiness Verdict
> **READY FOR LONG-DURATION AUTONOMOUS OBSERVATION**
