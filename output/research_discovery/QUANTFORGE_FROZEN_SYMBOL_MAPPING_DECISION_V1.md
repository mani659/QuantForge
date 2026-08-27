# QUANTFORGE — FROZEN SYMBOL MAPPING DECISION
# CAND-024 / CAND-035
# DATE: 2026-08-27

## 1. Mission
Determine whether the missing MT5 symbol `USATECHIDXUSD` can legitimately be represented in the current Exness environment by `USTECm` or `USTEC_x100m` without changing the frozen research object.

## 2. Historical Market Object
- Logical Instrument: US Technology Equity Index (Nasdaq 100)
- Market Type: CFD / Index Proxy
- Historical Broker Data Source: Unknown / Pre-existing repository dataset
- Point Size / Price Unit: Index Points
- Friction Assumption: 2.0 index points round-trip
- Timezone: America/New_York (EST/EDT)

## 3. CAND-024 Market Dependency
- Friday 12:00 EST to 15:45 EST.
- Requires precise liquidity and spread behavior leading up to the Friday US cash close.
- Highly sensitive to broker-specific Friday early-close or pre-weekend spread widening mechanics.

## 4. CAND-035 Market Dependency
- Last trading day of the month, 15:00 ET to exactly 16:00 ET.
- Requires the CFD to accurately track the underlying US cash market's 16:00 ET closing imbalance cross.
- Highly sensitive to month-end liquidity, exact 16:00 ET price settlement, and whether the broker CFD tracks the cash close or detaches to track futures.

## 5. USTECm Inspection
- Exists: True
- Description: US Tech 100 Index
- Underlying: Nasdaq 100
- Price Scale (Digits): 2
- Point / Tick Size: 0.01 / 0.01
- Contract Size: 1.0
- Live Tick: Available
- M1 Availability: Available

## 6. USTEC_x100m Inspection
- Exists: True
- Description: US Tech 100 Index
- Underlying: Nasdaq 100
- Price Scale (Digits): 2
- Point / Tick Size: 0.01 / 0.01
- Contract Size: 100.0
- Live Tick: Available
- M1 Availability: Available

## 7. Attribute Comparison
| Attribute | Historical USATECHIDXUSD | USTECm | USTEC_x100m |
|---|---|---|---|
| Underlying | US Technology Equity Index | US Tech 100 Index | US Tech 100 Index |
| Market type | CFD / Index Proxy | CFD | CFD |
| Price unit | Index Points | Index Points | Index Points |
| Point size | (implied 1.0 or 0.1) | 0.01 | 0.01 |
| Contract scaling | (implied 1.0) | 1.0 | 100.0 |
| Trading hours | Standard US Cash | Unknown via API | Unknown via API |
| Session schedule | Standard US Cash | Unknown via API | Unknown via API |
| Timezone semantics | America/New_York | UTC (server) | UTC (server) |
| Quote source | Repository historical | Exness | Exness |

## 8. Price Scale
The price scale in raw index points matches. `USTECm` quotes raw index points (e.g., 29576.84) with 2 digits of precision.

## 9. Contract Scaling
`USTECm` uses a contract size of 1.0. `USTEC_x100m` uses a contract size of 100.0. A deterministic translation to match the `2.0 index points` friction assumption would be trivial (e.g., 1 lot of `USTECm`).

## 10. Session Semantics
**UNKNOWN**. The standard MetaTrader5 Python API (`symbol_info`) does not expose the session schedule string. Without historical data for `USTECm` or exact session bounds, we cannot verify if the broker closes quotes early on Fridays or behaves identically at the 16:00 ET month-end boundary.

## 11. Timezone / DST
The Exness server operates on UTC. Timezone translation to `America/New_York` is possible via Python, but the exact DST transition dates enforced by the broker's session schedule remain unknown.

## 12. Quote / Bar Availability
Current quotes and M1 bars are fully available for both `USTECm` and `USTEC_x100m`.

## 13. Historical Semantic Continuity
**UNKNOWN**. While the underlying is the same, we cannot prove that the Exness `USTECm` CFD possesses the same session boundaries, Friday spread behavior, and 16:00 ET closing mechanics as the original `USATECHIDXUSD` dataset without running a comparative historical analysis, which is forbidden.

## 14. USTECm Mapping Decision
**MAPPING NOT SAFE**. Semantic continuity of Friday and Month-End closing sessions cannot be guaranteed without historical verification.

## 15. USTEC_x100m Mapping Decision
**MAPPING NOT SAFE**. Identical reasoning as `USTECm`, plus a contract scale multiplier.

## 16. CAND-024 Decision
**MAPPING NOT SAFE**
The Friday 15:45 exit requires strict Friday session liquidity behavior that cannot be assumed identical across different broker CFDs.

## 17. CAND-035 Decision
**MAPPING NOT SAFE**
The Month-End 16:00 ET exit requires the CFD to perfectly track the cash imbalance cross, which varies significantly between brokers.

## 18. Shared Mapping Decision
**NOT SAFE**
No alias can be safely substituted without violating the frozen research identity.

## 19. Risks
Substituting the symbol would decouple the forward validation engine from the historical research dataset. If the forward track failed, we could not determine whether the underlying market behavior degraded or the broker's CFD session mechanics simply mismatched the historical baseline.

## 20. Required Next Action
**PROVISION MT5 ENVIRONMENT THAT PROVIDES FROZEN SYMBOL**
The system requires an MT5 environment natively provisioning `USATECHIDXUSD` to ensure strict semantic continuity.

## 21. Qualification Clock
**NOT STARTED**

## 22. CAND-015
**ACTIVE / PROTECTED / UNTOUCHED**

## 23. System Assembly
**NOT EXECUTED**

## 24. Integrity
The identity audit was conducted via strict read-only MT5 API calls. The candidate definitions, event engines, and forward runner remain entirely untouched.
