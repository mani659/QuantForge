# QUANTFORGE — MT5 USATECHIDXUSD FEED DIAGNOSTIC
# CAND-024 / CAND-035
# DATE: 2026-08-27

## 1. Diagnostic Objective
Determine why the read-only MT5 market feed adapter fails to obtain current ticks and completed M1 bars for `USATECHIDXUSD`, preventing the launch of the rare-event forward qualification observation.

## 2. Terminal Status
**CONNECTED**
Terminal initialization successfully connected. 
- Build: 6140
- Company: Exness Technologies Ltd
- Trade Allowed: True

## 3. MT5 Package Status
Operational. Interprocess communication (IPC) with MetaTrader5 package is functioning correctly.

## 4. Broker / Server
- Server: Exness-MT5Trial15
- Company: Exness Technologies Ltd

## 5. Symbol Existence
**FAIL**
`mt5.symbol_info("USATECHIDXUSD")` returns `None`. The symbol is not recognized by the terminal.

## 6. Symbol Visibility
**FAIL**
The symbol cannot be made visible or selected because it does not exist on this server.

## 7. Symbol Properties
N/A (Symbol does not exist)

## 8. Tick Availability
**FAIL** (DATA_INDETERMINATE)
`mt5.symbol_info_tick("USATECHIDXUSD")` returns `None`.

## 9. Tick API Error
Error Code: `-4` 
Description: `Terminal: Not found`

## 10. M1 Bar Availability
**FAIL** (DATA_INDETERMINATE)
`mt5.copy_rates_from_pos("USATECHIDXUSD", mt5.TIMEFRAME_M1, 0, 5)` returns `None`.

## 11. M1 API Error
Error Code: `-4` 
Description: `Terminal: Not found`

## 12. Historical Data Availability
**NOT AVAILABLE**
Since the symbol itself does not exist on this broker server, no history is available.

## 13. Current Time
- Local time.time(): 1787823038
- Local UTC: 2026-08-27 09:30:38 UTC

## 14. Terminal / Server Time
N/A (Derived from tick data, which is unavailable)

## 15. UTC / America-New-York Comparison
N/A (No market data to compare)

## 16. Feed Freshness
**UNKNOWN** (Feed unavailable)

## 17. Market Session Status
**UNKNOWN** (Session status for the symbol cannot be read from the terminal)

## 18. Related Symbol Diagnostics
The broker does support related instruments. A search of the MT5 universe yielded:
- `USTEC_x100m`
- `USTECm`

## 19. Root-Cause Classification
**SYMBOL**
The broker data source (Exness-MT5Trial15) simply does not provide the frozen instrument `USATECHIDXUSD`. It uses alternative naming conventions (e.g., `USTECm`) for the US Tech Index.

## 20. Feed Adapter Review
**PASS**
The adapter code in `mt5_market_feed.py` correctly identified the missing symbol, reported `DATA_INDETERMINATE`, and refused to supply fabricated quotes.

## 21. Runner Review
**PASS**
The runner logic successfully trapped the indeterminate feed status without classifying the period as a synthetic `NO_EVENT`.

## 22. Required Remediation
**BROKER DATA SOURCE DOES NOT PROVIDE FROZEN SYMBOL**
The system requires an MT5 terminal logged into a broker that natively provisions `USATECHIDXUSD` (the symbol under which the historical research and frozen contracts were executed), or explicit architectural authorization to implement a deterministic symbol-alias mapping layer.

## 23. Qualification Clock
**NOT STARTED**

## 24. CAND-015 Independence
**ACTIVE / PROTECTED / UNTOUCHED**
No changes made to CAND-015.

## 25. System Assembly
**NOT EXECUTED**

## 26. Integrity
This diagnostic was conducted strictly via read-only MT5 SDK calls. No configuration or strategy definitions were modified.
