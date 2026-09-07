# QUANTFORGE — FROZEN MARKET ENVIRONMENT DISCOVERY
# CAND-024 / CAND-035
# DATE: 2026-08-27

## 1. Objective
Determine whether QuantForge currently possesses access to an environment, MT5 terminal, or broker dataset that can natively provide the exact frozen market object `USATECHIDXUSD` for forward validation of CAND-024 and CAND-035.

## 2. Frozen Market Object
- Symbol: `USATECHIDXUSD`
- Underlying: US Technology Equity Index (Nasdaq 100)
- Timezone: `America/New_York` (EST/EDT)
- Platform: MetaTrader 5
- Data Resolution: M1 (OHLCV) and Live Tick (Bid/Ask)

## 3. Repository Search
A comprehensive repository search for `USATECHIDXUSD` yielded:
- **Historical Source Data**: Present in `data/m1/USATECHIDXUSD_M1.csv` and `data/tick/USATECHIDXUSD_mt5_ticks.csv`.
- **Frozen Contracts**: Documented in `scripts/rare_events/contracts.py`.
- **Research Artifacts**: Widespread references in protocol definitions, execution audits, and scientific reports confirming it as the primary equity index object.
- **Broker Configuration**: The `QUANTFORGE_FROZEN_SYMBOL_MAPPING_DECISION_V1.md` artifact explicitly states the historical broker is "Unknown / Pre-existing repository dataset".
- **No other broker configurations or environment variables** referencing a live `USATECHIDXUSD` provider were found.

## 4. Historical Data Source
- The exact provenance of the historical dataset is undocumented. The `QUANTFORGE_PROGRAM_LEVEL_RESEARCH_ARCHITECTURE_AUDIT_V1.md` and `QUANTFORGE_FROZEN_SYMBOL_MAPPING_DECISION_V1.md` classify the source as an "Unknown / Pre-existing repository dataset".
- The data files are MT5 CSV exports (`_mt5_ticks.csv` and `_M1.csv`).

## 5. Local MT5 Terminals
A directory and process scan of the local machine revealed the following MT5 installations:
1. `C:\Program Files\MetaTrader 5 EXNESS` (Currently running as `terminal64.exe`)
2. `C:\Program Files\MetaTrader 5 EXNESS - Copy`
3. `C:\Program Files (x86)\MetaTrader 4 EXNESS`
4. `D:\Gold Scripts` (Origin trace only, no valid MT5 environment found)

## 6. Broker / Server Inventory
The only active broker environments available locally are provisioned by **Exness** (specifically, `Exness-MT5Trial15` as diagnosed in previous tasks). No alternative broker configurations (e.g., Eightcap, FTMO, Darwinex) that might provide different naming conventions were discovered.

## 7. Exact Symbol Availability
- The exact symbol `USATECHIDXUSD` is **NOT AVAILABLE** on the currently installed Exness terminals.
- Exness provides aliases (`USTECm`, `USTEC_x100m`).

## 8. Current Tick Availability
- Live tick data for `USATECHIDXUSD`: **UNAVAILABLE**.
- The API explicitly returns failure (`DATA_STALE` / Symbol Not Found) for the exact string.

## 9. M1 Availability
- Historical M1 data for `USATECHIDXUSD` is **AVAILABLE** (in `data/m1/USATECHIDXUSD_M1.csv`).
- Live M1 data stream for `USATECHIDXUSD` is **UNAVAILABLE**.

## 10. Historical Source Continuity
There is **NO EVIDENCE** connecting the historical `USATECHIDXUSD` dataset to the currently installed Exness MT5 environments. Given Exness uses `USTECm`, it is highly probable the historical data originated from a different broker entirely.

## 11. Session / Timezone Evidence
The historical data was modeled against `America/New_York` (EST/EDT) session boundaries (Friday 12:00-15:45 and Month-End 15:00-16:00). Without the original broker environment, the precise session continuity cannot be established.

## 12. Environment Matching Matrix
| Candidate Environment | Frozen Symbol Available | Current Tick | M1 Available | Same Broker/Source | Same Session Evidence | Confidence |
|---|---|---|---|---|---|---|
| Exness-MT5Trial15 | NO | NO | NO | NO | NO | 0% |
| Exness - Copy | NO | NO | NO | NO | NO | 0% |

## 13. CAND-024 Environment Decision
> ENVIRONMENT PROVISIONING REQUIRED

## 14. CAND-035 Environment Decision
> ENVIRONMENT PROVISIONING REQUIRED

## 15. Alias Status
`USTECm`: **NOT SAFE**
`USTEC_x100m`: **NOT SAFE**
(Governing decision preserved; aliases must not be substituted merely for convenience without separate governance).

## 16. CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

## 17. Qualification Clock
> NOT STARTED

## 18. System Assembly
> NOT EXECUTED

## 19. Next Required Action
The repository possesses no viable active environment providing the frozen market object. To proceed, QuantForge must pursue one of the following:
1. **PROVISION ENVIRONMENT PROVIDING USATECHIDXUSD** (Recommended: Find a broker matching the historical naming convention and deploy it).
2. **GOVERNANCE REVIEW FOR EXPLICIT NORMALIZATION** (Submit `USTECm` for formal re-qualification against historical metrics).

## 20. Integrity
This discovery was conducted purely via read-only file/process inspection and log parsing. No MT5 accounts were switched, no strategy logic was modified, no orders were submitted, and no forward observation engines were launched.
