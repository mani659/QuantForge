# QUANTFORGE — EXPLICIT FROZEN-INSTRUMENT NORMALIZATION REVIEW
# USATECHIDXUSD → EXNESS USTECm
# GOVERNANCE DECISION ONLY
# DATE: 2026-08-27

## 1. Mission
Re-evaluate the previous `MAPPING NOT SAFE` decision. Determine whether the historical research object `USATECHIDXUSD` can be deterministically mapped to the currently available Exness `USTECm` symbol for forward qualification, while preserving the scientific identity of CAND-024 and CAND-035 events and strictly separating research object identity from the execution environment.

## 2. Historical USATECHIDXUSD Object
- **Symbol**: `USATECHIDXUSD`
- **Underlying**: US Technology Equity Index (Nasdaq 100)
- **Instrument Type**: CFD / Index Proxy
- **Price Scale**: Raw index points (e.g. 15000.00)
- **Timezone**: `America/New_York`
- **Session Assumptions**: Standard US Cash (09:30-16:00 ET) and extended liquidity spanning 08:00 to 16:00 ET.

## 3. Historical Data Provenance
**UNKNOWN**. The dataset `data/m1/USATECHIDXUSD_M1.csv` is a pre-existing repository MT5 export. No specific broker configuration or external data pipeline remains to identify its original source. 

## 4. USTECm MT5 Object
- **Symbol**: `USTECm`
- **Description**: US Tech 100 Index
- **Underlying**: Nasdaq 100
- **Digits**: 2
- **Point**: 0.01
- **Tick Size**: 0.01
- **Contract Size**: 1.0
- **Currency**: USD
- **Trade Mode**: Full Access (4)
- **Quote Availability**: Live Bid/Ask available
- **M1 Availability**: High-quality tick and M1 data available (50,000+ recent M1 bars verified).

## 5. USTEC_x100m Comparison
`USTEC_x100m` is an account-specific variant with a different contract multiplier (Contract Size: 100.0). It is structurally identical in pricing but represents a leveraged lot denomination. The primary normalization candidate is `USTECm` due to its 1:1 index-point-to-contract-size mapping, which matches standard index CFD conventions.

## 6. Underlying Identity
**SAME**.
Repository metadata, Exness terminal descriptors, and supporting practitioner evidence confirm both `USATECHIDXUSD` and `USTECm` are CFD proxies for the US Tech 100 / Nasdaq-100 index.

## 7. Price Representation
**IDENTICAL RAW PRICE REPRESENTATION**.
Both symbols quote in raw index points with two decimal places of precision. The difference is merely the string identifier (`USATECHIDXUSD` vs `USTECm`).

## 8. Deterministic Normalization
No mathematical transformation of the price is required.
`price_normalized = price_source * 1.0`
`point_scale = 1:1`

## 9. Event-Logic Invariance
**INVARIANT**.
CAND-024 and CAND-035 rely entirely on relative price inequalities:
- `High > Weekly High`
- `Open_12:00 < Open_08:00`
- `Open_15:00 > Open_09:30`
These relational operators are mathematically invariant to deterministic price scaling and unaffected by the symbol string. Time anchors (08:00, 09:30, 12:00, 15:00, 15:45, 16:00 ET) are absolute and invariant.

## 10. CAND-024 Identity
**YES — IDENTITY PRESERVED**.
The Friday 12:00 ET entry and 15:45 ET exit events are structurally identical. A qualifying `USTECm` event represents the exact same US Tech 100 morning-exhaustion mechanic studied historically.

## 11. CAND-035 Identity
**YES — IDENTITY PRESERVED**.
The Month-End 15:00 ET to 16:00 ET imbalance capture is structurally identical.

## 12. Session Semantics
Exness `USTECm` quotes 24/5. An explicit MT5 API extraction of recent history confirms dense M1 bar presence across the required US Cash session and extended pre-market hours (08:00 ET to 16:15 ET). 

## 13. Friday Semantics
Verified. M1 data confirms deep, unbroken tick volume on Fridays through the 15:45 ET exit required by CAND-024. Exness does not close quotes prior to 15:45 ET on normal Fridays.

## 14. Month-End Semantics
Verified. Exness `USTECm` quotes continuously through the 16:00 ET US Cash close. M1 bars surrounding 16:00 ET on month-end dates exhibit heavy volume, ensuring the imbalance cross behavior can be captured.

## 15. DST
The forward execution framework translates all times dynamically via UTC, ensuring resilience against DST shifts relative to the broker server.

## 16. 15:45 / 16:00 Availability
Genuine quotes and completed M1 bars exist at both 15:45 ET and 16:00 ET, supporting the mandated event horizon boundaries.

## 17. Spread / Friction
- Historical Model: 2.0 index points round-trip.
- Exness `USTECm`: Observed at ~1.12 index points round-trip (e.g., Bid: 29576.84, Ask: 29577.96).
The current execution environment friction is **LOWER/COMPARABLE** to the historical assumption. 2.0 points remains conservative. Actual forward costs will be measured natively by the execution ledger.

## 18. Research Object vs Execution Environment
The frozen research object (`USATECHIDXUSD`) remains the scientific baseline. `USTECm` is declared strictly as an **authorized current-market execution representation** of the same underlying economic instrument, subject to explicit normalization.

## 19. Practitioner Supporting Evidence
External trading experience supports that Exness utilizes `USTECm` as its standard mini-lot Nasdaq-100 CFD. This serves as supporting practitioner evidence, validating the quantitative audit.

## 20. Normalization Decision
**APPROVED WITH NORMALIZATION**.
`USTECm` is authorized for forward observation of CAND-024 and CAND-035.

## 21. Environment Mapping ID
`MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`

## 22. Contract Hash Preservation
- CAND-024: `CAND-024:1.0:c49c5bb0` (Unchanged)
- CAND-035: `CAND-035:1.0:a7c2132d` (Unchanged)
The historical identity remains frozen.

## 23. Risks
Broker-specific behaviors during holidays or extreme news events may differ marginally from the historical dataset, but the `PaperExecutionFirewall` combined with forward measurement safely contains this risk without invalidating the research.

## 24. Qualification Clock
**NOT STARTED**. (A separate task is required to launch).

## 25. CAND-015
**ACTIVE / PROTECTED / UNTOUCHED**.

## 26. System Assembly
**SYSTEM ASSEMBLY DEFINED — NOT YET EXECUTABLE**.

## 27. Required Next Action
**EXPLICIT LAUNCH OF RARE-EVENT QUALIFICATION USING USTECm**.

## 28. Integrity
No code, hash, or strategy logic was modified. The assessment was performed using read-only historical verification and read-only MT5 environment introspection.
