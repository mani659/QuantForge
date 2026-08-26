# QUANTFORGE — CAND-015
# G6 MT5 INTEGRATION FINAL AUDIT REPORT
# READ-ONLY / AUDIT VERDICT
# 2026-08-25

## 1. Executive Verdict
The engineering audit confirms that the Exness MT5 adapter and forward harness have been correctly implemented without compromising the integrity of the frozen CAND-G0-015 research object. Safety firewalls enforce fail-closed mechanics, paper-only simulation without actual execution, and immutable symbol mapping. The adapter correctly handles real-time tick and completed-bar ingestion.

**Final Classification: A — G6 READY**

## 2. Frozen Identity
- **Verdict: MATCH**
- **Analysis:** `cand015_identity.py` remains perfectly intact. The signal engine and harness inherit all properties (3× M5 ATR shock, pre-entry D1 ATR condition, 60-minute lockout, frozen 3.0 bp cost, frozen 60-minute exit) directly from the unified frozen dictionary. No divergence was found.

## 3. Replay Regression
- **Verdict: PASS**
- **Analysis:** `PaperExecutionAdapter` preserves the explicit `REPLAY_TEST` branch where execution occurs on synthetic OHLC `open` and is classified as `SYNTHETIC_REPLAY`. `harness.py` seamlessly supports polling `REPLAY_TEST` fixtures.

## 4. MT5 Quotes
- **Verdict: PASS**
- **Analysis:** `mt5_feed.py` correctly requests `mt5.symbol_info()` returning real-time bid and ask. It incorporates explicit staleness (5-minute max difference from local UTC time) and ensures the spread is valid (bid <= ask) before emitting quotes into the system.

## 5. Completed Bars
- **Verdict: PASS**
- **Analysis:** To extract M1/M5/D1 closed bars, the feed correctly uses `mt5.copy_rates_from_pos(..., 0, 2)` and selects index `[-2]`, completely avoiding index `[-1]` which represents the currently forming, uncompleted bar in MT5.

## 6. Cross-Market Ordering
- **Verdict: PASS**
- **Analysis:** `harness.py` sorts incoming ticks by `observation_timestamp`. On timestamp ties, a deterministic tiebreaker `0 if x["symbol"] == "USATECHIDXUSD" else 1` strictly processes `USTECm` before `BTCUSDm`, preventing look-ahead bias from future Nasdaq prices entering the BTC execution engine.

## 7. Paper Execution
- **Verdict: PASS**
- **Analysis:** `paper_execution.py` strictly routes long entries/short exits to `ask`, and short entries/long exits to `bid`. The 3.0 bp cost is recorded separately in the ledger and is never double counted within the quote-execution difference computation. No MT5 order API exists in the logic.

## 8. Latency
- **Verdict: PASS**
- **Analysis:** The harness captures `feed_observation_latency` (local receipt vs. market timestamp) and `signal_processing_latency` (decision timestamp vs. local receipt). Broker execution latency is strictly excluded from the schema as the implementation is entirely paper-based.

## 9. Loop Safety
- **Verdict: PASS**
- **Analysis:** `run_forward_observation` in `harness.py` utilizes a `_stop_event`, processes a graceful shutdown on `KeyboardInterrupt` (Ctrl+C), incorporates a configurable `max_duration_seconds`, properly shuts down MT5, and utilizes a non-busy sleep loop based on `poll_interval_ms`.

## 10. Forward Firewall
- **Verdict: PASS**
- **Analysis:** There is no execution endpoint (`order_send` / `order_check`) anywhere in the paper adapter, data feed, or harness. MT5 is securely verified for `ACCOUNT_TRADE_MODE_DEMO` on init, failing closed securely.

## 11. Ledger
- **Verdict: PASS**
- **Analysis:** `ledger.py` was correctly extended to preserve all necessary telemetry, including `broker_symbol`, `execution_price_type`, `slippage_status`, `latency`, `bid`, `ask`, and deterministic `FORWARD_PAPER` mode enforcement.

## 12. Test Quality
- **Verdict: STRONG**
- **Analysis:** Tests K–Z provide high-fidelity coverage of integration bounds. The mocks properly isolate external MT5 calls. Assertions rigorously evaluate MT5 fail-closed conditions, mapping invalidation, paper-quote divergence, and continuous-loop stop signals. Test suite successfully passed all 26 evaluations.

## 13. Smoke Test
- **Verdict: PASS**
- **Analysis:** The real `smoke_test_mt5.py` demonstrated the MT5 connection to Exness Demo, successfully logging actual `USTECm` and `BTCUSDm` quotes, M1/M5/D1 closed bars, and confirming `FORWARD_PAPER` ingestion limits under a brief 2-second safe runtime.

## 14. Security
- **Verdict: PASS**
- **Analysis:** No hardcoded credentials, account passwords, or broker API keys are stored in the codebase or ledger. All MT5 connections rely on local client state.

## 15. Scope
- **Verdict: PASS**
- **Analysis:** The implementation remains highly scoped to CAND-015 paper observation limits. It did not bloat into generic framework abstraction or multi-strategy logic.

## 16. Final Classification
**A — G6 READY**
The MT5 adapter and harness are safe and semantically faithful for controlled paper observation.

## 17. Observation Readiness
The implementation is authorized to advance to the controlled observation execution phase.
