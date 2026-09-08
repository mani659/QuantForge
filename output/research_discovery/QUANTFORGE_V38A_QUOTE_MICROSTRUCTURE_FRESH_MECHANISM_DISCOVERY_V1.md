# QUANTFORGE — V38A QUOTE MICROSTRUCTURE FRESH MECHANISM DISCOVERY V1

**Date:** 2026-09-08
**Status:** DISCOVERY COMPLETE — ZERO SURVIVORS
**Purpose:** Fresh, independent quote-level market-mechanism discovery following the §81 reconciliation of T01/T02/T03.

---

## 1. MISSION

Determine whether the canonical tick substrate contains any genuinely distinct market-generating mechanisms that have not already been explored or rejected. This is a discovery and novelty screening task only. No formulation, validation, economic testing, optimization, or implementation.

The authoritative state: §80 three-survivor verdict overturned. §81 reconciliation completed. MECH-T01 information-novel but mechanism novelty unestablished. MECH-T02 mechanism-equivalent to T01. MECH-T03 not genuinely distinct. Bid/ask independence remains a genuinely new information dimension.

---

## 2. AUTHORITATIVE SOURCES

| Source | Key insight |
|--------|-------------|
| SESSION_HANDOFF (through §81) | §80 overturned, §81 reconciliation, current governed state |
| §80 original discovery artifact | T01/T02/T03 definitions, original five-test claims |
| §81 reconciliation | Corrected statistics, reclassifications, negative knowledge |
| Tick Data Audit | Data capability boundary: bid, ask, spread, mid, timing; no trade events, no depth, no volume |
| Canonical Tick Specification | Schema: source_row_ordinal, date, time, bid, ask, last, vol, mid, spread |
| Canonical Tick Migration Report | 900M rows, 0 rejected, 4 validated symbols |
| V36 Exhausted Dimensions | 21 permanently exhausted mechanism families |
| V38A Novelty-Gated Discovery (M1) | X01/X02/X03/X04 all FAILED — M1 space exhaustively explored |
| MECH-F Distinctness Adjudication | F01=F02=F03 all PARTIALLY DISTINCT — mechanism-level failures documented |
| MECH-F Fresh Discovery | F01/F02/F03 definitions and exclusion sets |
| MECH-N New Discovery | N01/N02/N03 definitions |
| BASE-001 Adjudication | CLOSED / NOT BASE-ELIGIBLE |
| CAND-077/081 Governance Review | CAND-081 structural level failure trap, CAND-077 volatility transition |
| Prior spread research | Spread level, spread dynamics — covered by volatility and spread families |
| Prior event-intensity research | Event clustering (CAND-098) — exhausted |
| Prior intrabar-path research | Path-dependent sequence asymmetry — exhausted |
| Prior volatility-transition research | CAND-077/096/099 — exhausted or contradicted |
| Prior momentum/trend research | TSMOM, directional momentum — exhausted |
| Prior reversal research | Mean reversion (DISC-021) — exhausted |
| Prior gap/opening research | Settlement windows (CAND-074/075) — exhausted |

---

## 3. CANONICAL DATA CAPABILITY

### Directly supported

- Bid, ask (present on every tick, update independently)
- Spread (ask - bid, always positive)
- Mid (bid + ask / 2)
- Quote-event timing at 1-second resolution
- Duplicate timestamps (multiple quote updates per second preserved)
- Tick arrival intensity (ticks per second)
- Bid/ask independence (whether one or both sides change)
- Quote-update persistence (duration between updates)

### Not supported

- True transactions (no trade/quote flag)
- Trade volume (vol = 0)
- Aggressor direction (no trade classification)
- Order-book depth (top-of-book only)
- Institutional positioning
- Market-maker identity or intent
- Stop-loss execution
- Liquidity consumption

### Empirical observations (corrected per §81 audit)

| Symbol | One-sided adjustments | Both-side changes | Neither |
|--------|----------------------|-------------------|---------|
| XAGUSD | 13.5% | 75.4% | 11.0% |
| XAUUSD | 48.2% | 51.7% | 0.1% |
| BTCUSD | 49.6% | 47.9% | 2.5% |
| USATECHIDXUSD | 0.7% | 99.3% | 0.0% |

These cross-symbol variations are real and represent genuinely new information relative to M1 OHLCV.

---

## 4. PRIOR / EXHAUSTED MECHANISM SPACE

### 4.1 Permanently Exhausted Dimensions (21 from V36)

1. Structural break conditioning
2. Volatility regime / state
3. Volatility acceleration / rate
4. Transition quality
5. Directional momentum / exhaustion
6. Shock magnitude / direction
7. Event recency / decay
8. Event clustering / density
9. Event ordering / sequencing
10. Multi-timeframe break coordination
11. Post-magnitude directional drift
12. Path-dependent sequence asymmetry
13. Directional run-length persistence
14. Mean reversion (DISC-021)
15. TSMOM (DISC-022)
16. Session-range compression (DISC-024)
17. Liquidity sweep / reversal (DISC-025)
18. Settlement / benchmark windows (CAND-074/075)
19. Intra-bar distribution (CAND-106)
20. Cross-asset lead-lag (CAND-105)
21. Cross-asset vol co-movement (CAND-107)

### 4.2 Closed Mechanism Families

- BASE-001 / MECH-N01: Structural level validation — CLOSED
- CAND-081: Structural level failure trap — STATE REVIEW ELIGIBLE (observation only)
- MECH-F01: Failed breakout inventory reversal — PARTIALLY DISTINCT (same mechanism as CAND-081)
- MECH-F02: Shock-induced position adjustment cascade — PARTIALLY DISTINCT (interpretive, not independently observable)
- MECH-F03: Overnight gap inventory rebalancing — PARTIALLY DISTINCT (gap-following decision rule)
- MECH-N02: Cross-asset hedging cascade — DEFERRED
- MECH-N03: Session-sequential trend quality — DEFERRED
- RF-001/002/003: Cross-market relational — RF-001 Stage 3 blocked, RF-002/003 DEFERRED
- F-01/F-02/F-03: Formulated — F-01 registered, F-02/F-03 DEFERRED

### 4.3 T01/T02/T03 Negative Knowledge (Binding)

- T01: Information-novel (bid/ask independence real) but mechanism novelty unestablished. "Directional pressure from quote makers" is participant hypothesis, not observed mechanism.
- T02: Mechanism-equivalent to T01. Same underlying events, different target variable.
- T03: Not genuinely distinct. Interaction term collapses to exhausted dimensions when tick-specific component removed.
- Feature novelty does not imply mechanism novelty.
- Different target variables over the same quote events do not create different mechanisms.
- Participant narratives require observable discriminators.
- Quote updates cannot be interpreted as trade aggression.

---

## 5. DISCOVERY METHODOLOGY

1. **Mechanism-first reasoning.** Each candidate begins with a market-generating process hypothesis, not an indicator or statistical pattern.
2. **Exclusion-first approach.** Complete exclusion set (Sections 3–4) before generating candidates.
3. **Five-test novelty gate.** Information novelty, mechanism novelty, quote-layer necessity, independent falsifiability, prospective observability, prior-art separation, mutual separation.
4. **Attempt to destroy.** For every candidate, actively attempt to reduce it to an exhausted mechanism.
5. **Feature ≠ mechanism enforcement.** A new observable becomes a mechanism only when it identifies a distinct market-generating process.
6. **Participant-story discipline.** Participant stories are hypotheses. No assertion of participant behavior without observable discriminator.
7. **Zero-survivor acceptability.** A result of zero survivors is scientifically preferable to a feature disguised as a mechanism.

---

## 6. CANDIDATE GENERATION

### Process

The discovery process began by identifying what market-generating processes could exist at quote resolution that have not been represented by the exhausted mechanism families. The canonical data provides: bid, ask, spread, mid, timing, quote-update events, bid/ask independence.

The following candidate concepts were generated through mechanism-first reasoning, then subjected to the exclusion set and destruction attempts.

---

## 7. CANDIDATE DEFINITIONS AND DISPOSITION

### MECH-Q01: Quote-Update Burstiness Regime

**Mechanism name:** Quote-Update Burstiness Regime

**Market process:** Quote updates arrive in temporal clusters (bursts) separated by quiet periods. The burst/quiet transition reflects a change in information arrival rate or market-maker participation state.

**Observable:** Distribution of inter-quote-update time gaps within a defined window. Transition from short gaps (burst) to long gaps (quiet) or vice versa.

**Mechanism hypothesis:** Burst periods reflect active price discovery (information arrival); quiet periods reflect information vacuum or market-maker withdrawal. Transitions between regimes alter the market's response to subsequent orders.

**Participant hypothesis:** During bursts, market makers update frequently in response to order flow. During quiet periods, market makers hold quotes steady due to low information or high conviction.

**Information advantage over M1:** M1 cannot distinguish burst from quiet periods within the bar.

**Why quote resolution is structurally necessary:** Inter-update timing requires tick-level timestamps.

**Destruction attempt:** Quote-update burstiness is a temporal characterization of event intensity. Event clustering/density (exhausted dimension 8) covers the same market process: activity intensity varies over time. Burstiness is a specific statistical measure of the same underlying phenomenon. **Collapses to exhausted event clustering.**

**Disposition: REJECTED** — overlaps with exhausted "event clustering / density" (CAND-098).

---

### MECH-Q02: Quote-Update Persistence Regime

**Mechanism name:** Quote-Update Persistence Regime

**Market process:** Quotes persist at the same price for varying durations. Extended persistence reflects low information flow or high market-maker conviction. Rapid updates reflect active price discovery. Transitions between persistence regimes alter market state.

**Observable:** Duration (in seconds) between consecutive quote updates for the same quote level. Distribution of persistence durations within a window.

**Mechanism hypothesis:** Persistence regime transitions (from high-persistence to low-persistence or vice versa) reflect changes in the information environment.

**Participant hypothesis:** High persistence = market makers confident in current quotes. Low persistence = market makers adjusting to new information.

**Information advantage over M1:** M1 cannot measure inter-update persistence.

**Why quote resolution is structurally necessary:** Persistence requires tick-level timestamps.

**Destruction attempt:** Persistence is the inverse of event frequency. High persistence = low event frequency. Low persistence = high event frequency. This is event intensity measured from the opposite direction. Volatility regime/state (exhausted dimension 2) and event clustering (exhausted dimension 8) cover the same market process. **Collapses to exhausted volatility regime and event clustering.**

**Disposition: REJECTED** — overlaps with exhausted "volatility regime / state" and "event clustering / density."

---

### MECH-Q03: Quote-Side Sequential Dominance

**Mechanism name:** Quote-Side Sequential Dominance

**Market process:** Over a window, bid-side quote updates may dominate ask-side updates (or vice versa). The sequential dominance pattern reveals which side of the quote is under more active adjustment pressure.

**Observable:** Over a window, count bid-only updates vs ask-only updates. The side with more updates is "dominant."

**Mechanism hypothesis:** Bid-dominant periods reflect buying pressure; ask-dominant periods reflect selling pressure. Dominance transitions predict subsequent mid-price direction.

**Participant hypothesis:** Bid-dominant = market makers adjusting bids upward (buying pressure). Ask-dominant = market makers adjusting asks downward (selling pressure).

**Information advantage over M1:** M1 cannot distinguish bid-dominant from ask-dominant periods.

**Why quote resolution is structurally necessary:** Requires counting individual bid-only and ask-only updates.

**Destruction attempt:** Quote-side sequential dominance counts one-sided adjustments per side. This is T01's one-sided adjustment asymmetry applied to a window count rather than a per-tick classification. The §81 audit established T01 as information-novel but mechanism novelty unestablished. The "buying pressure" / "selling pressure" interpretation is the same participant hypothesis that was rejected for T01. **Mechanistically equivalent to T01.**

**Disposition: REJECTED** — mechanism-equivalent to T01 (information-novel, mechanism novelty unestablished).

---

### MECH-Q04: Spread-Adjustment Consistency

**Mechanism name:** Spread-Adjustment Consistency

**Market process:** When spread changes occur, the *consistency* of which side drives the change may vary. Consistent bid-driven narrowing (bid repeatedly moving toward ask) is different from alternating bid/ask-driven narrowing.

**Observable:** Over a window of spread-change events, classify each event as bid-driven or ask-driven. Compute the consistency ratio (fraction of events driven by the same side).

**Mechanism hypothesis:** High consistency reflects one-sided directional pressure; low consistency reflects two-sided price discovery. Consistency level predicts subsequent spread behavior.

**Participant hypothesis:** High consistency = one side under sustained pressure. Low consistency = balanced two-way flow.

**Information advantage over M1:** M1 cannot observe the adjustment consistency.

**Why quote resolution is structurally necessary:** Requires classifying individual spread-change events by which side drove the change.

**Destruction attempt:** Spread-adjustment consistency measures the homogeneity of one-sided adjustments over a window. This is a statistical aggregation of T01's one-sided adjustment events. The underlying observable (which side drove the spread change) is the same as T01/T02. The "consistency" metric is a window-level summary of the same per-tick events. **Mechanistically equivalent to T01/T02.**

**Disposition: REJECTED** — mechanistically equivalent to T01/T02.

---

### MECH-Q05: Spread-Path Directional Coupling

**Mechanism name:** Spread-Path Directional Coupling

**Market process:** The trajectory of spread changes over a window may be correlated with mid-price direction. A specific spread-path pattern (e.g., narrowing-then-widening during an uptrend) may reflect a different market state than the reverse pattern.

**Observable:** Joint classification of mid-direction and spread-change-direction at each tick, forming a trajectory through the 3x3 coupling matrix (mid-up/flat/down × spread-widen/flat/narrow) over time.

**Mechanism hypothesis:** Specific coupling trajectories (e.g., mid-rise with spread-narrow followed by mid-rise with spread-widen) reflect distinct market states that predict subsequent behavior.

**Participant hypothesis:** Coupling trajectories reflect the quality of price discovery (orderly vs disorderly).

**Information advantage over M1:** M1 cannot observe the coupling trajectory.

**Why quote resolution is structurally necessary:** Requires tick-level mid-direction and spread-change-direction.

**Destruction attempt:** This is T03's spread-midpath coupling extended to trajectory analysis. The §81 audit established T03 as "not genuinely distinct / exhausted-dimension interaction." The coupling trajectory is an interaction term between mid-direction (M1-available) and spread-change-direction (tick-specific). The audit found that "removing the tick-specific component maps the candidate to previously explored/exhausted dimensions." **Mechanistically equivalent to T03.**

**Disposition: REJECTED** — mechanistically equivalent to T03.

---

### MECH-Q06: Quote-Activity State Transition

**Mechanism name:** Quote-Activity State Transition

**Market process:** The market transitions between discrete quote-activity states (e.g., "active" = high update rate, "quiet" = low update rate, "one-sided" = bid or ask dominating). Transitions between states may predict subsequent spread or mid-price behavior.

**Observable:** Classify each time window into a quote-activity state based on: (a) update rate, (b) bid/ask balance, (c) spread-change frequency. Track state transitions over time.

**Mechanism hypothesis:** State transitions (e.g., from "quiet" to "active") reflect information arrival that alters the market's microstructure. The transition itself contains predictive information.

**Participant hypothesis:** State transitions reflect changes in market-maker participation or information flow.

**Information advantage over M1:** M1 cannot observe quote-activity states or transitions.

**Why quote resolution is structurally necessary:** Requires tick-level update rates, bid/ask balance, and spread-change frequency.

**Destruction attempt:** Quote-activity states combine: (a) update rate = event intensity (exhausted dimension 8), (b) bid/ask balance = T01 one-sided adjustments (information-novel, mechanism novelty unestablished), (c) spread-change frequency = spread dynamics (exhausted). State transitions = volatility regime transitions (exhausted dimension 2). The composite is an aggregation of exhausted and unestablished components. **Collapses to exhausted volatility regime and event clustering, plus T01.**

**Disposition: REJECTED** — composite of exhausted dimensions and T01.

---

## 8. NOVELTY GATE

All six candidates were rejected before reaching the formal five-test novelty gate. No candidate satisfied the prior-art separation requirement.

| Candidate | Primary rejection reason |
|-----------|------------------------|
| Q01 (Burstiness Regime) | Collapses to exhausted event clustering |
| Q02 (Persistence Regime) | Collapses to exhausted volatility regime and event clustering |
| Q03 (Sequential Dominance) | Mechanism-equivalent to T01 |
| Q04 (Spread-Adjustment Consistency) | Mechanism-equivalent to T01/T02 |
| Q05 (Spread-Path Coupling) | Mechanism-equivalent to T03 |
| Q06 (Activity State Transition) | Composite of exhausted dimensions and T01 |

No candidate reached the five-test novelty gate. All were rejected at the prior-art separation stage.

---

## 9. M1 EQUIVALENCE

Not applicable. No candidate survived to M1 equivalence testing. All candidates were rejected at prior-art separation.

---

## 10. MECHANISM EQUIVALENCE

Not applicable. No candidate survived to mechanism equivalence testing. All candidates were rejected at prior-art separation.

---

## 11. PRIOR-ART COMPARISON

| Candidate | Closest prior | Shared process | New element | Why not same mechanism | Verdict |
|-----------|--------------|----------------|-------------|----------------------|---------|
| Q01 | Event clustering (CAND-098) | Activity intensity varies over time | Burst/quiet temporal pattern | Same process, different statistical measure | REJECTED |
| Q02 | Volatility regime (CAND-077) / Event clustering | Quote persistence = inverse of event frequency | Persistence duration | Same process, opposite measurement | REJECTED |
| Q03 | T01 (one-sided adjustment asymmetry) | Counts one-sided adjustments per side | Window-level dominance count | Same mechanism, different aggregation | REJECTED |
| Q04 | T01/T02 (quote adjustment events) | Uses same underlying bid/ask adjustment events | Consistency ratio | Same mechanism, different summary statistic | REJECTED |
| Q05 | T03 (spread-midpath coupling) | Joint mid-spread trajectory | Trajectory analysis | Same mechanism, extended to time series | REJECTED |
| Q06 | Volatility regime + event clustering + T01 | Combines update rate, bid/ask balance, spread changes | Composite state classification | Composite of exhausted and unestablished components | REJECTED |

---

## 12. MUTUAL-DISTINCTNESS AUDIT

Not applicable. No candidate survived to mutual-distinctness testing. All candidates were rejected at prior-art separation.

---

## 13. REJECTION LOG

| Candidate | Rejection category | Specific reason |
|-----------|-------------------|-----------------|
| Q01 | Exhausted event clustering | Quote-update burstiness = event intensity temporal pattern |
| Q02 | Exhausted volatility regime + event clustering | Quote persistence = inverse of event frequency |
| Q03 | T01 mechanism-equivalent | Sequential dominance = T01's one-sided adjustments aggregated over window |
| Q04 | T01/T02 mechanism-equivalent | Spread-adjustment consistency = T01/T02 events with consistency metric |
| Q05 | T03 mechanism-equivalent | Spread-path coupling = T03's coupling extended to trajectory |
| Q06 | Composite of exhausted + T01 | Combines exhausted event clustering, volatility regime, and T01 |

---

## 14. SURVIVORS

**ZERO SURVIVORS.**

No candidate survived the prior-art separation gate. All six candidates collapsed to exhausted mechanism families or to T01/T02/T03 (which themselves did not establish mechanism novelty).

---

## 15. BASE-POTENTIAL CLASSIFICATION

Not applicable. No survivors.

---

## 16. QUALITATIVE PRIORITIZATION

Not applicable. No survivors.

---

## 17. OWNER-SELECTION ELIGIBILITY

**The owner-selection eligibility set is EMPTY.**

No mechanism survived the novelty gates. No mechanism is eligible for owner selection.

---

## 18. GOVERNANCE COMPLIANCE

| Check | Result |
|-------|--------|
| BASE-001 remains CLOSED / NOT BASE-ELIGIBLE | PASS |
| T01 remains INFORMATION-NOVEL / MECHANISM NOVELTY UNESTABLISHED | PASS |
| T02 remains MECHANISM-EQUIVALENT TO T01 | PASS |
| T03 remains NOT GENUINELY DISTINCT | PASS |
| MECH-F01/F02/F03 remain unselected | PASS |
| RF-001 unchanged | PASS |
| RF-002 unchanged | PASS |
| RF-003 unchanged | PASS |
| F-01 unchanged | PASS |
| F-02 unchanged | PASS |
| F-03 unchanged | PASS |
| FB-001 unchanged | PASS |
| Protected-forward states untouched | PASS |
| Live runner uninterrupted | PASS |
| No broker orders | PASS |
| No canonical data modifications | PASS |
| No schema modifications | PASS |
| No economic testing | PASS |
| No optimization | PASS |
| No formulation | PASS |
| No Base registration | PASS |
| No Stage 2 | PASS |
| No Stage 3 | PASS |
| No rescue of rejected mechanisms | PASS |
| No closed line reopened | PASS |

---

## 19. VERDICT

**QUOTE-MICROSTRUCTURE FRESH MECHANISM DISCOVERY COMPLETE — ZERO SURVIVORS**

Six candidates generated through mechanism-first reasoning. All six rejected at the prior-art separation gate. No candidate survived to the formal five-test novelty gate.

The exhaustion pattern is systematic:
- Quote-activity temporal patterns (Q01, Q02) collapse to exhausted event clustering and volatility regime.
- Quote-side counting patterns (Q03, Q04) collapse to T01/T02 (information-novel, mechanism novelty unestablished).
- Quote-price interaction patterns (Q05) collapse to T03 (not genuinely distinct).
- Composite patterns (Q06) combine exhausted dimensions with T01.

**The canonical tick substrate provides genuinely new information (bid/ask independence, quote-update timing, spread dynamics at tick resolution), but the exhausted mechanism families cover all plausible market-generating processes that could be constructed from this information.**

Feature novelty remains established. Mechanism novelty remains unestablished. The bid/ask independence dimension is a valid information-level discovery, but the first two discovery cycles (T01/T02/T03 and Q01–Q06) have not produced a survivor.

A zero-survivor result is scientifically preferable to a feature disguised as a mechanism.

---

**END OF V38A QUOTE MICROSTRUCTURE FRESH MECHANISM DISCOVERY V1**
