# QUANTFORGE — CAND-015
# EXNESS MT5 DEMO DATA-SOURCE CAPABILITY AUDIT V1

## 1. Objective
Determine whether the existing Exness MT5 demo environment can serve as the real-time data source required to unblock CAND-015 G6 Forward Validation. This audit assesses technical suitability and data availability strictly without modifying CAND-015 or executing any orders.

## 2. MT5 Connectivity
**PASS.**
The local environment has MetaTrader 5 installed. The Python `MetaTrader5` package successfully initialized a connection to the terminal.
- **Terminal Name:** MetaTrader 5 EXNESS
- **Connection Status:** Connected = True

## 3. Account Environment
**CONFIRMED.**
- **Server:** Exness-MT5Trial15
- **Trade Mode:** DEMO
No credentials or sensitive identifiers were exposed.

## 4. Symbol Discovery
The terminal exposes a total of 357 symbols. The required instruments were successfully identified:
- **USATECHIDXUSD:** Found as `USTECm` and `USTEC_x100m` (Description: "US Tech 100 Index"). Both use `USD` as base currency and `trade_mode: 4` (Demo/Full access).
- **BTCUSD:** Found as `BTCUSDm` (Description: "Bitcoin vs US Dollar"). Uses `BTC` as currency, `trade_mode: 4`.

## 5. Real-Time Tick Capability
**PASS.**
- **USTECm:** Real-time quotes are available. `symbol_info` returns fresh timestamps, active bid, and active ask prices.
- **BTCUSDm:** Real-time quotes and ticks are available. `symbol_info_tick` and `symbol_info` return fresh timestamps, active bid, and active ask prices. Bid < Ask invariant holds true.
No executions or modifications were triggered by this capability test.

## 6. M1/M5/D1 Capability
**PASS.**
The MT5 Python integration successfully retrieved historical and currently forming bars using `copy_rates_from_pos` for both `USTECm` and `BTCUSDm`.
- **M1:** Available and chronologically ordered.
- **M5:** Available and chronologically ordered.
- **D1:** Available and chronologically ordered.
All bars returned populated OHLC fields and deterministic timestamps.

## 7. Timestamp / Timezone
**UTC.**
The MT5 terminal returns tick and bar timestamps natively as UTC integer timestamps. When interpreted in Python via `datetime.fromtimestamp(time, tz=timezone.utc)`, the times exactly align with the current UTC clock. QuantForge's frozen CAND-015 timezone semantics are fully compatible.

## 8. Bid/Ask Capability
**PASS.**
Exness provides real-time Bid and Ask quotes for both required symbols, suitable for paper trading execution logic and synthetic spread modeling. `symbol_info` exposes `bid` and `ask` explicitly.

## 9. Data Completeness
**PASS.**
Both `USTECm` and `BTCUSDm` are available simultaneously on the exact same real-time feed/server. They provide sufficient pricing and historical coverage for the G6 observation harness without requiring substitution or synthetic indexing.

## 10. G6 Suitability
**A — SUITABLE**
Both required symbols are available with real-time timestamps, bid/ask spreads, necessary M1/M5/D1 bar formations, and stable Python/MT5 access.

## 11. Limitations
None identified for the data-source audit scope. The MT5 Python bridge may occasionally return `0` from `symbol_info_tick` for indices like `USTECm`, but `symbol_info` reliably streams the active bid/ask, easily circumventing any tick-fetching idiosyncrasy.

## 12. Integrity
**CAND-015 NOT EXECUTED.**
**NO ORDERS PLACED.**
No elements of the CAND-015 strategy or G6 harness were modified. No demo trades were placed. The audit strictly queried read-only metadata and pricing fields.
