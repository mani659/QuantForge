# QUANTFORGE — RARE-EVENT MARKET FEED REMEDIATION
# CAND-024 / CAND-035
# DATE: 2026-08-27

## 1. Original Blocker
**SYNTHETIC MARKET INPUT**
The integrity audit discovered the forward qualification daemon was actively fed by a deterministic synthetic market price generator (`time.sleep(1)` loop with fixed `bid: 15000, ask: 15002`) instead of a genuine market feed.

## 2. Remediation Objective
To construct a strict Read-Only Market Data Adapter interfacing with MetaTrader5, isolate all synthetic capabilities to `TEST` and `SMOKE` modes exclusively, and ensure that `FORWARD` mode strictly fails closed if live data is not fresh and genuine.

## 3. Authoritative Frozen Contracts
- CAND-024: `CAND-024:1.0:c49c5bb0`
- CAND-035: `CAND-035:1.0:a7c2132d`

## 4. MT5 Feed Architecture
A new `MT5MarketFeed` class was implemented in `mt5_market_feed.py`. This encapsulates MetaTrader5 SDK interactions natively without depending on order execution APIs.

## 5. MarketDataFeed Interface
- `latest_quote(symbol)`
- `latest_completed_bar(symbol, timeframe)`
- `connection_state()`
- `source_timestamp()`

## 6. Symbol Mapping
- Logical Instrument: `USATECHIDXUSD`
- Broker Symbol: `USATECHIDXUSD` (Expected matching naming convention in MT5 terminal)

## 7. Read-Only MT5 Boundary
The adapter employs solely data retrieval functions (`symbol_select`, `symbol_info_tick`, `copy_rates_from_pos`). Order and trade operations are entirely omitted.

## 8. TEST / SMOKE / FORWARD Mode Separation
The `rare_event_runner.py` now enforces a `--mode` parameter.
- `test`/`smoke`: Injects `MockFeed`.
- `forward`: Injects `MT5MarketFeed`. Rejects mock feeds.

## 9. Synthetic Feed Firewall
**SYNTHETIC FEED TEST/SMOKE ONLY**
Attempting to pass synthetic market data in `FORWARD` mode results in `STARTUP FAILURE`.

## 10. Historical Replay Firewall
**FORWARD FALLBACK FORBIDDEN**
No CSV, Parquet, or replay frameworks are accessible via `MT5MarketFeed`. The feed checks `time.time()` against `tick.time` to prevent historical re-injection.

## 11. Data Freshness Semantics
`DATA_STALE` is strictly enforced. If a quote's source timestamp is more than 60 seconds old, it is rejected. Stale data does NOT count as `NO_EVENT`.

## 12. Feed Loss Semantics
**STALE/DISCONNECTED ≠ NO_EVENT**
If the feed disconnects, the runner loop skips candidate evaluation and initiates exponential backoff reconnect logic. It does not fabricate continuity.

## 13. Completed Bar Semantics
The adapter requests index `1` with a count of `1` via `copy_rates_from_pos` to guarantee only fully completed bars are supplied to the engines.

## 14. Timezone / DST Integrity
**America/New_York** is strictly enforced via UTC baseline storage. `time.time()` and `tick.time` rely entirely on POSIX timestamps, naturally handling DST when explicitly decoded for session logic.

## 15. Market Calendar Integrity
Unchanged. Strategy frozen rules continue to determine Friday and Month-End conditions against the UTC feed.

## 16. Reconnect
Bounded exponential backoff is implemented (1s → max 30s) if `feed.connection_state()` returns `DISCONNECTED` or data is `FEED_UNAVAILABLE`.

## 17. Health / Heartbeat
The daemon records the status of the quote (`DATA_FRESH`, `DATA_STALE`, `DATA_INDETERMINATE`) and current runner mode (`smoke`/`forward`) continuously.

## 18. Event Ledger Semantics
If the feed fails, the event ledger is intentionally NOT written to. The system must observe a genuine market state to declare `NO_EVENT`.

## 19. Paper Execution Isolation
**SYNTHETIC PAPER ONLY**
- **NO REAL ORDER API**
- **NO DEMO ORDER API**
- **NO LIVE ORDER SUBMISSION**

## 20. Contract Hash Firewall
**PASS**
Hashes are enforced at engine instantiation and logged.

## 21. Automated Tests
- Passed: 6
- Failed: 0
- Skipped: 0

## 22. Synthetic Smoke Test
**PASS**
Successfully processed mock ticks.

## 23. Real MT5 Read-Only Smoke Test
**FAIL (BLOCKED)**
The `verify-feed` command returned `DATA_INDETERMINATE` for the symbol `USATECHIDXUSD`. A live MT5 terminal connection was established, but the terminal does not currently have active quote ticks for that symbol (either due to market closure, missing symbol configuration, or sandbox terminal environment). 

## 24. Qualification Clock
**NOT STARTED**

## 25. Launch Readiness
**REAL MARKET FEED NOT VERIFIED — QUALIFICATION BLOCKED**
The infrastructure remediation is complete, but true live-market conditions could not be verified in this environment.

## 26. Known Limitations
Requires manual validation of MT5 terminal symbol availability for `USATECHIDXUSD`.

## 27. Integrity
CAND-015 infrastructure and forward data remain entirely untouched and protected. No original research definitions were modified.
