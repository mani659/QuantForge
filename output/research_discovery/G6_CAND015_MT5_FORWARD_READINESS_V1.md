# QUANTFORGE — CAND-015
# G6 REAL-TIME MT5 DATA ADAPTER FORWARD READINESS REPORT
# EXNESS DEMO / PAPER ONLY
# 2026-08-25

## 1. Objective
The objective of this implementation was to unblock the **G6 — CONTROLLED FORWARD PAPER OBSERVATION** for the frozen CAND-G0-015 research object by integrating a real-time MT5 data adapter using the Exness Demo environment. The integration was required to be strictly read-only (forward paper) with no modification to the frozen signal logic, maintaining the historical replay capability.

## 2. Exness Data Source
The data source used is the official MetaTrader 5 (MT5) Python integration connected to an Exness Demo Account. The adapter natively polls the terminal for real-time bid/ask updates and historical completed bars for `USTECm` and `BTCUSDm`.

## 3. Symbol Mapping
The integration defines an immutable, hardcoded symbol mapping to translate the internal research symbols into the live broker-specific symbols:
- `USATECHIDXUSD` → `USTECm`
- `BTCUSD` → `BTCUSDm`

This mapping is persisted within the `MT5DataFeed` class and written to the ledger as version `1.0`. Any missing mapping safely causes the harness to fail closed.

## 4. MT5 Connectivity
Connectivity is verified on initialization of `FORWARD_PAPER` mode. The adapter ensures:
- `mt5.initialize()` succeeds.
- Terminal is connected (`mt5.terminal_info().connected`).
- The active account is strictly a **DEMO** account (`ACCOUNT_TRADE_MODE_DEMO`).
- Required symbols are available and visible in the market watch.

## 5. Real-Time Quote Capture
The adapter captures real-time data using `mt5.symbol_info()`. It successfully fetches:
- UTC Market Timestamps
- Contemporaneous Bid
- Contemporaneous Ask
- Spread

Stale ticks (older than 5 minutes) result in an immediate fail-closed state to protect observation integrity.

## 6. Completed Bar Semantics
The strategy requires completed M1, M5, and D1 bars. The adapter strictly honors this by fetching `rates[-2]` from `mt5.copy_rates_from_pos` (which guarantees extraction of the most recently fully closed bar, ignoring the currently forming bar at index -1).

## 7. Signal Integration
The MT5 data structures are successfully adapted to the existing `Cand015SignalEngine` without altering any of the frozen logic. The cross-market processing is deterministic: if `USTECm` and `BTCUSDm` share the same timestamp, `USTECm` is strictly processed first to prevent information leakage regarding the shock condition.

## 8. Paper Execution
The `PaperExecutionAdapter` was enhanced to support `FORWARD_PAPER` mode while explicitly guaranteeing that no order endpoints (e.g., `order_send`) are invoked. 
- Long Entry uses contemporaneous Ask
- Short Entry uses contemporaneous Bid
- Long Exit uses contemporaneous Bid
- Short Exit uses contemporaneous Ask

The execution price type is recorded as `DEMO_PAPER_QUOTE` with slippage recorded as `QUOTE_BASED_PAPER_DIFFERENCE`.

## 9. Latency
Artificial latency generation has been strictly removed. The harness now precisely records:
- **Feed Observation Latency:** `local_receipt_timestamp - market_timestamp`
- **Signal Processing Latency:** `decision_timestamp - local_receipt_timestamp`
Broker execution latency is explicitly not measured (as no live orders are placed).

## 10. Ledger
The `EventLedger` was expanded to securely persist all new runtime telemetry without conflating it with replay data. New fields include: `broker_symbol`, `broker`, `platform`, `market_timestamp`, `local_receipt_timestamp`, `signal_timestamp`, `decision_timestamp`, `bid`, `ask`, `quote_execution_difference`, `feed_observation_latency`, and `signal_processing_latency`. All records explicitly enforce `mode = FORWARD_PAPER`.

## 11. Safety Firewall
The implementation includes strict, non-bypassable safeguards:
- Failure to verify the demo account blocks execution.
- Missing symbols or stale data immediately halt the harness.
- A connection failure will not silently fall back to `REPLAY_TEST`.
- No `order_send` or modifying MT5 account functions exist in the codebase.

## 12. Tests K–Z
The `tests_g6.py` suite was expanded to include tests K–Z. These tests enforce the MT5 mapping validity, safety fallback mechanisms (e.g., non-demo account rejection), bid/ask extraction integrity, cross-market ordering determinism, paper execution mechanics, quote execution differences, and ensure the `REPLAY_TEST` parity remains strictly unchanged. **All 26 tests passed.**

## 13. Smoke Test
The `smoke_test_mt5.py` was executed directly against the live Exness MT5 demo terminal.
- It successfully connected and verified the demo account.
- It successfully pulled live quotes and completed bars for `USTECm` and `BTCUSDm`.
- It demonstrated that no order APIs are triggered.
- It routed a short real-time feed into the G6 harness and stopped cleanly.
**SMOKE TEST: PASSED**

## 14. Known Limitations
- Network latency between the local runtime environment and the Exness MT5 server will affect feed observation latency.
- Spread widening during significant market volatility will directly impact the `QUOTE_BASED_PAPER_DIFFERENCE`.

## 15. G6 Readiness
> **READY FOR CONTROLLED FORWARD OBSERVATION**

## 16. Operational Hardening (2026-08-26 Addendum)
Following the first 12-hour overnight session (`G6_CAND015_FORWARD_002`), the autonomous runner was hardened to safely absorb expected MT5 broker rollover/maintenance outages.
- A controlled bounded exponential backoff (1s up to 30s) was implemented to prevent CPU busy-looping during extended broker outages.
- Telemetry was corrected to explicitly mirror the `EventStateMachine` states instead of incorrectly defaulting to `UNKNOWN` when the signal engine was idle.
- Rich telemetry was added to `heartbeat.jsonl` tracking disconnect counts, reconnect counts, current outage duration, and logging reconnect metadata directly to `connection_events.jsonl`.
- The strategy and execution semantics remain **STRICTLY UNCHANGED**.
> **READY FOR LONG-DURATION PAPER OBSERVATION**
