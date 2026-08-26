# QUANTFORGE — CAND-015
# G6 OPERATIONAL HARDENING REPORT
# 2026-08-26

## 1. Problem
During the `G6_CAND015_FORWARD_002` 12-hour overnight session, the MT5 broker entered a standard ~1 hour midnight rollover/maintenance outage. While the runner correctly kept the process alive without crashing, the tight loop (due to instantaneous return from `terminal_info()` failure and data fetch exceptions) executed rapidly. This resulted in 379,223 reconnect attempts and logged messages within the hour, indicating a busy-loop vulnerability. Additionally, the `heartbeat.jsonl` telemetry reported `signal_state: UNKNOWN`, which falsely looked like a signal-engine mathematical failure.

## 2. Reconnect Diagnosis
The `harness.py` gracefully caught the data fetch exception and safely terminated its inner observation loop, shutting down the MT5 connection in its `finally` block to prevent stale data reading. The standalone wrapper (`run_long_observation.py`) then correctly caught the disconnection and instantiated a new `MT5DataFeed`. However, because it lacked a backoff sleep timer upon successful instantiation (which would immediately fail on the next data fetch since the broker was down), it looped uncontrollably fast.

## 3. Backoff Design
To resolve this, a bounded exponential backoff was introduced in `run_long_observation.py`.
- **Initial Delay:** 1.0 second.
- **Scaling:** The backoff doubles (2s, 4s, 8s, 16s) if `harness.run_forward_observation` fails/returns in less than 10 seconds.
- **Cap:** The delay is capped at 30.0 seconds.
- **Reset:** If observation succeeds for more than 10 seconds, the backoff resets to 1.0 second.
This entirely eliminates CPU busy-looping while still providing sub-minute recovery resolution.

## 4. Telemetry Correction
- The `signal_state` variable was detached from the local `volatility_state` variable and now explicitly reflects `self.event_machine.state`. It reports standard, expected states such as `IDLE`, `EVENT_DETECTED`, `ENTRY_PENDING`, `IN_POSITION`, etc.
- Health telemetry in `heartbeat.jsonl` was expanded to explicitly track `disconnect_count`, `reconnect_count`, and `current_outage_seconds`.
- Disconnect metadata is now cleanly logged to `connection_events.jsonl` with precise downtime durations, avoiding log flooding.

## 5. Tests
Structural tests BA–BF were implemented in `tests_runner.py` using robust mocking frameworks to verify exponential backoff integrity, health metric reporting, and telemetry state tracking.
The entire regression suite (`tests_g6.py` and `tests_runner.py`) was executed.
**36/36 tests passed successfully.** No tests were weakened, and NO strategy code was modified.

## 6. MT5 Smoke Test
A real-time 2-minute smoke test was executed against the live MT5 environment using `run_cand015_forward.bat 0.033`. The runner successfully initialized the newly implemented exponential backoff logic, verified the firewall, output the corrected telemetry, and terminated gracefully. **PASS.**

## 7. Safety
The `CAND-015` strategy logic, mathematical thresholds, symbols, entry/exit semantics, and frozen identity are **STRICTLY UNCHANGED**. All modifications were purely bounded to operational wrappers, error handling, and state logging.
- NO ORDER API INVOKED
- NO DEMO ORDER PLACED
- NO REAL ORDER PLACED

## 8. Long-Run Readiness
> **READY FOR LONG-DURATION PAPER OBSERVATION**
