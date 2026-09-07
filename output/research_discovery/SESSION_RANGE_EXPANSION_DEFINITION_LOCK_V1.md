# QUANTFORGE — SESSION-ANCHORED RANGE EXPANSION SCIENTIFIC DEFINITION LOCK V1

## 1. Executive Verdict
**A — LEVEL 2 / READY FOR PRE-REGISTRATION**

All scientific choices required to test the candidate market behavior have been explicitly defined, frozen outcome-blind, and structurally decoupled from trading PnL. The scientific object is now a measurable, falsifiable behavioral hypothesis ready for formal protocol pre-registration.

## 2. Scientific Question
**GOVERNANCE DECISION:**
> Does a state of extreme pre-session range compression in USATECHIDXUSD reliably precede a statistically significant increase in subsequent US cash-session range expansion, compared to sessions that follow normal or expanded pre-session ranges?

This is strictly a behavioral hypothesis about volatility state transitions. It makes no claim about trading profitability.

## 3. Market / Data Scope
**GOVERNANCE DECISION:**
- **Primary Instrument:** `USATECHIDXUSD`
- **Primary Frequency:** M1 (1-minute bars)
- **Source:** Existing QuantForge validated M1 dataset.
- **Rationale:** `USATECHIDXUSD` maps directly to the institutional US technology equity market, which possesses the necessary liquidity, defined session structure, and historical intraday M1 depth to test session-anchored mechanics.
- **Restriction:** No new markets may be added during this phase. Tick data is excluded from the primary behavioral test and reserved for future economic/cost validation.

## 4. Session Definition
**GOVERNANCE DECISION:**
To prevent temporal leakage and daylight-saving (DST) misalignment, all session boundaries are defined strictly in `America/New_York` local exchange time and mapped to the UTC dataset.
- **US Cash Session (The Response Window):** 09:30 to 16:00 ET.
- **Pre-Session (The Observation Window):** 18:00 ET (prior day) to 09:30 ET (current day).
- **Weekends/Holidays:** Standard calendar filtering. Days lacking a full continuous 09:30-16:00 cash session (e.g., early holiday closes) are dropped from the evaluation.
- **Rolling vs Fixed:** The pre-session window is a fixed daily temporal block.

## 5. Pre-Session Range Definition
**GOVERNANCE DECISION:**
- **Raw Range ($R_{pre}$):** High - Low observed strictly between 18:00 ET and 09:30 ET.
- **Normalization:** To make ranges comparable across decades of varying index price levels, the raw range is normalized by the closing price of the pre-session window (09:29 ET): 
  $$Normalized\_R_{pre} = \frac{R_{pre}}{Close_{09:29}}$$
- **Rule:** This metric is purely mechanical and requires no look-ahead.

## 6. Compression-State Definition
**GOVERNANCE DECISION:**
While K-means was conceptually proposed, a **Deterministic Rolling Percentile** is scientifically superior for this specific test because it eliminates label-switching instability, guarantees exact out-of-sample mapping, and removes all ML-initialization variance.
- **Definition:** The pre-session state is classified as **COMPRESSED** if today's $Normalized\_R_{pre}$ falls into the bottom quartile ($\leq 25th$ percentile) of the trailing 63 trading days (approx. one rolling quarter).
- **Alternative State:** Otherwise, it is classified as **NORMAL/EXPANDED**.
- **Rule:** The 63-day rolling window uses strictly prior completed days.

## 7. K-Means Role and Constraints
**GOVERNANCE DECISION:**
- **Verdict:** REJECTED for this specific definition lock.
- **Rationale:** K-means (K=2) on a 1D range feature introduces unnecessary complexity (centroid drift, cluster label ambiguity) without improving the scientific measurement of "compression." A deterministic rank-based state (Section 6) achieves the exact structural goal of the screening task while being mathematically rigid.

## 8. Forward Response
**GOVERNANCE DECISION:**
The hypothesis measures the energetic release of the compressed state.
- **Primary Response:** Cash Session Normalized Range ($Normalized\_R_{cash}$), defined as:
  $$Normalized\_R_{cash} = \frac{High_{cash} - Low_{cash}}{Close_{16:00}}$$
  measured strictly between 09:30 ET and 16:00 ET.
- **Comparison:** The distribution of $Normalized\_R_{cash}$ on COMPRESSED days vs NORMAL/EXPANDED days.
- **Rule:** The response is evaluated entirely after 09:30 ET. No overlap exists with the state observation window.

## 9. Directional Component
**GOVERNANCE DECISION:**
- **Primary Object (H-A):** Compression predicts RANGE expansion magnitude only.
- **Secondary Diagnostic (H-B):** Directional persistence. (e.g., If the cash session breaks the pre-session high, does the 16:00 ET close remain in the top quartile of the cash session range?).
- **Rationale:** Separating magnitude (H-A) from direction (H-B) prevents confounding. A market can expand violently but whip-saw (failing H-B while passing H-A). The primary behavioral gate is energetic expansion. Direction is explicitly secondary.

## 10. Horizon
**GOVERNANCE DECISION:**
- **Primary Horizon:** Exact session boundaries (09:30 ET to 16:00 ET).
- **Rule:** The response ends unconditionally at 16:00 ET. Overnight gaps, next-day drift, and extended-hours trading are explicitly excluded from the primary response.

## 11. Independence / Firewall
**GOVERNANCE DECISION:**
- **Vs. Mean Reversion:** This hypothesis does not require extreme price displacement or counter-trend movement.
- **Vs. 12/1 TSMOM:** This is an intraday phenomenon (hours), completely unrelated to 12-month macroeconomic trend persistence.
- **Vs. H01:** H01 measures inter-day shock-response asymmetry. This candidate measures intraday volatility state-transitions.
- **Integrity:** This is a 100% independent behavioral line.

## 12. Falsification
**GOVERNANCE DECISION:**
The hypothesis is formally falsified if:
1. The median $Normalized\_R_{cash}$ following COMPRESSED states is NOT statistically significantly greater than the median following NORMAL/EXPANDED states.
2. The effect is entirely localized to a single narrow chronological era (e.g., only exists in 2020-2021) and fails cross-era temporal stability checks.

## 13. Economic Relevance
**GOVERNANCE DECISION:**
If the behavioral hypothesis survives, the economic relevance is structural:
- An intraday session hold captures a large macro move (hours of index accumulation/distribution).
- The transaction cost (one entry, one exit) is amortized against a large expected excursion.
- It holds exactly zero overnight gap risk.
- (No PnL or spread impact will be calculated during the behavioral test).

## 14. Future Strategy Translation
**MODEL INFERENCE:**
*Conceptually only:* If Phase 5 (Adjudication) validates the behavior, Phase 6 (Strategy) will investigate:
- Entry triggers (e.g., price breaking the pre-session high/low).
- Stop-loss structures (e.g., opposite side of the pre-session range).
- Hit rate and reward-to-risk ratio.
- Exact transaction costs mapped against the tick dataset.

## 15. Discovery → Validation → Live Sequence
**GOVERNANCE DECISION:**
The frozen sequence for this specific candidate:
1. Scientific definition (THIS ARTIFACT).
2. Outcome-blind protocol pre-registration.
3. Independent audit of protocol.
4. Discovery experiment (calculating state and response distributions).
5. Independent adjudication of the behavioral claim.
6. Strategy translation (converting to rules).
7. Economic validation (tick-level execution math).
8. Forward/demo/live monitoring.

## 16. Definition Completeness
**GOVERNANCE DECISION:**
- Market: Defined.
- Session Boundaries: Defined (ET, mapped to UTC).
- Pre-session Range: Defined.
- State Classifier: Defined (63-day rolling 25th percentile).
- Primary Response: Defined.
- Falsification Criteria: Defined.

## 17. Governance Decision
**A — LEVEL 2 / READY FOR PRE-REGISTRATION**
The behavioral object is entirely deterministic, outcome-blind, and mathematically closed.

## 18. Exact Next Task
> **AUTHOR PROTOCOL FOR SESSION RANGE EXPANSION V1**

Construct the formal `EVENT_STUDY_PROTOCOL` that implements these frozen definitions into a reproducible statistical test plan.

## 19. Prohibited Follow-Up
- Writing backtest code before protocol registration.
- Sneaking K-means back into the definition to see if it "works better."
- Downloading new market data to test multiple symbols at once.
- Examining a price chart of USATECHIDXUSD to fine-tune the 63-day window.

## 20. Integrity
- No execution code was written.
- No PnL was modeled.
- No historical data was inspected to derive the 63-day or 25th-percentile parameters (these are standard, robust quarters/quartiles).
- The scientific object is strictly a behavioral test of volatility state transitions.
