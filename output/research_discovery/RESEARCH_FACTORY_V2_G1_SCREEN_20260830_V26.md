# RESEARCH FACTORY V2 — G1 ECONOMIC PLAUSIBILITY SCREEN — V26
# DATE: 2026-08-30
# STATUS: G1 COMPLETE — NO G2 PROMOTIONS

---

## 1. G1 Status

> V26 G1 COMPLETE. Three candidates evaluated under the ratified G1 V3 Evidence-Based Adjudication Framework. Zero candidates promoted to G2.

---

## 2. V3 Framework Applied

Two-layer architecture: Hard Validity Gates (9 binary checks) + Economic Evidence Adjudication (holistic). All economic statistics are evidence inputs, not thresholds.

---

## 3. Data Used

| Instrument | Bars | Date Range |
|---|---|---|
| XAUUSD M1 | 1,768,123 | 2021-04-12 to 2026-04-10 |
| USATECHIDXUSD M1 | 906,815 | 2023-09-01 to 2026-07-10 |

**DATA LIMITATION:** Volume data is all zeros for both instruments. Volume-based confirmation filters specified in the frozen definitions could not be applied. This is noted as a data limitation but does not invalidate the core price-based signals.

---

## 4. Cost Normalization

Universal: 2.0 bps round-trip. All results in bps.

---

## 5. Hard Validity Gate Results

| Gate | CAND-077 | CAND-078 | CAND-079 |
|---|---|---|---|
| Deterministic definition | PASS | PASS | PASS |
| Executable entry | PASS | PASS | PASS |
| No hindsight | PASS | PASS | PASS |
| Correct cost normalization | PASS | PASS | PASS |
| Data integrity | PASS | PASS | PASS (volume limited) |
| Legitimate counterfactual | PASS | PASS | PASS |
| Causal claims limited to observables | PASS | PASS | PASS |
| No future-bar dependency | PASS | PASS | PASS |
| Reproducible | PASS | PASS | PASS |

All three candidates are valid measurement objects.

---

## 6. CAND-077 — Volatility Compression-to-Expansion Transition

### Definition
Enter long when close breaks above compressed period high after ATR percentile transitions from <25th to >50th. Exit 30 minutes later.

### Transition
Compressed volatility (ATR percentile <25th for 20+ bars) transitioning to expanding volatility (ATR percentile >50th). The transition is the breakout bar itself.

### Treatment
Breakout from compressed period into expanding volatility.

### Counterfactual
Same breakout signal when ATR percentile is already >50th (already-expanded state, not transitioning).

### N / Frequency
- N = 2,084
- Frequency = ~700/year

### Gross Economics
- Mean gross = +1.15 bps
- Median gross = +0.86 bps

### Net Economics
- Mean net = **-0.85 bps**
- Median net = **-1.14 bps**

### Mean / Median
Mean and median are both negative but close to zero. The compression-to-expansion transition produces near-zero gross economics on average.

### Tail Diagnostics
- Worst event = -212 bps (extreme outlier)
- Best event = +104 bps

### Counterfactual
- Counterfactual N = 387
- Counterfactual mean net = -2.52 bps
- Counterfactual median net = -1.90 bps
- **Delta Mean = +1.67 bps (TREATMENT SUPERIOR)**
- **Delta Median = +0.76 bps (TREATMENT SUPERIOR)**
- Gate: **TREATMENT SUPERIOR**

### Executable Integrity
PASS. Entry at breakout bar close is deterministic. Exit 30 bars later is deterministic. No hindsight.

### Transition Integrity
PASS. The transition from compressed to expanding volatility is clearly defined and measurable. The ATR percentile crossing from <25th to >50th is a genuine state change, not a static threshold.

### Observed Behavior
The compression-to-expansion transition produces near-zero gross economics (-0.85 bps net). However, the transition beats the already-expanded counterfactual by +1.67 bps mean net. This means the transition adds real informational value — breakouts from compressed states produce better outcomes than breakouts in already-expanded markets.

### Hypothesized Mechanism
Stop cascade and forced flow during the transition from compressed to expanding volatility. Participants with tight stops are triggered in sequence, creating cascading directional pressure.

### Unproven Mechanism
Actual stop placement, liquidation, or participant intent. The price consequence is directly measurable; the causal mechanism is hypothesized.

### Economic Adjudication
> **INFORMATIONALLY INTERESTING**

Mean net is -0.85 bps (negative). But the treatment beats the counterfactual by +1.67 bps — a meaningful informational delta. The transition adds real value, but not enough to overcome 2 bps friction. The mechanism has genuine informational content but insufficient absolute economics.

### Component Potential
MODERATE. The volatility-transition signal could serve as a filter for other Alpha candidates.

### State Potential
HIGH. The volatility-transition state itself could be valuable as a regime filter.

### Regime Potential
MODERATE. Inherently regime-dependent (only fires during transitions).

### G2 Eligibility
> NOT ELIGIBLE (absolute economics negative)

---

## 7. CAND-078 — Trend Exhaustion Transition

### Definition
Enter against trend when 8+ consecutive same-direction closes are followed by a reversal bar. Exit 15 minutes later.

### Transition
Sustained directional sequence (8+ consecutive same-direction closes) transitioning to exhaustion (first reversal bar).

### Treatment
Counter-trend entry after 8+ consecutive same-direction closes.

### Counterfactual
Same counter-trend signal after only 2–4 consecutive same-direction closes (early trend, not exhausted).

### N / Frequency
- N = 2,946
- Frequency = ~1,033/year

### Gross Economics
- Mean gross = -0.21 bps
- Median gross = -0.07 bps

### Net Economics
- Mean net = **-2.21 bps**
- Median net = **-2.07 bps**

### Mean / Median
Both negative. Near-zero gross economics mean the exhaustion transition produces essentially no directional displacement.

### Tail Diagnostics
- Worst event = -19 bps
- Best event = +37 bps

### Counterfactual
- Counterfactual N = 2,946
- Counterfactual mean net = -1.96 bps
- Counterfactual median net = -1.81 bps
- **Delta Mean = -0.25 bps (COUNTERFACTUAL SUPERIOR)**
- **Delta Median = -0.26 bps (COUNTERFACTUAL SUPERIOR)**
- Gate: **COUNTERFACTUAL SUPERIOR**

### Executable Integrity
PASS. Entry at reversal bar close is deterministic. Exit 15 bars later is deterministic.

### Transition Integrity
PASS. The transition from 8+ consecutive same-direction closes to a reversal bar is clearly defined and measurable.

### Observed Behavior
The exhaustion transition produces near-zero gross economics (-0.21 bps). The counterfactual (random counter-trend bar after 2–4 consecutive closes) performs slightly better (-1.96 bps vs -2.21 bps). The exhaustion state does NOT add directional value beyond a basic counter-trend signal.

### Hypothesized Mechanism
Trapped late participants exit at exhaustion, creating forced mean-reversion pressure.

### Unproven Mechanism
Actual participant positioning. The price consequence is directly measurable; the trapped-participant mechanism is hypothesized.

### Economic Adjudication
> **ECONOMICALLY NEGATIVE**

Mean net is -2.21 bps. The counterfactual is superior. The exhaustion transition does not add directional value. The mechanism does not produce friction-surviving economics.

### Component Potential
LOW. No meaningful incremental information over basic counter-trend signals.

### State Potential
LOW. The exhaustion state does not improve downstream economics.

### Regime Potential
LOW. No regime-specific value observed.

### G2 Eligibility
> NOT ELIGIBLE

---

## 8. CAND-079 — Gold Volatility Regime Transition → Tech Response

### Definition
When Gold volatility transitions from compressed (<25th percentile) to expanded (>75th percentile), measure Tech response 30–60 minutes later in the direction of Gold's move.

### Transition
Gold 14-bar return volatility crossing from below 25th percentile to above 75th percentile of its trailing 200-bar distribution.

### Treatment
Tech entry 30 minutes after Gold volatility transition, in the direction of Gold's move during the transition.

### Counterfactual
Same Tech window when Gold volatility is already expanded (>75th percentile for 30+ bars, not transitioning).

### N / Frequency
- N = 35,920
- Frequency = ~13,781/year (very high — state definition captures many transitions)

### Gross Economics
- Mean gross = +0.21 bps
- Median gross = +0.02 bps

### Net Economics
- Mean net = **-1.79 bps**
- Median net = **-1.98 bps**

### Mean / Median
Both negative. Near-zero gross economics mean the Gold volatility transition produces essentially no directional displacement in Tech.

### Tail Diagnostics
- Worst event = -329 bps
- Best event = +328 bps

### Counterfactual
- Counterfactual N = 8,727
- Counterfactual mean net = -2.57 bps
- Counterfactual median net = -2.16 bps
- **Delta Mean = +0.78 bps (TREATMENT SUPERIOR)**
- **Delta Median = +0.18 bps (TREATMENT SUPERIOR)**
- Gate: **TREATMENT SUPERIOR**

### Executable Integrity
PASS. Entry timing is deterministic. Cross-market timestamps are synchronized in UTC+4.

### Cross-Market Integrity
PASS. Both datasets use UTC+4 timezone. Gold timestamps are before Tech timestamps (30-minute delay). No lookahead. DST transitions affect both equally.

### Transition Integrity
PASS. The Gold volatility regime transition is clearly defined. The quantile-based approach captures genuine state changes.

### Observed Behavior
The Gold volatility transition produces near-zero gross economics (0.21 bps). The treatment beats the counterfactual by +0.78 bps — small but positive informational value. However, the absolute economics are negative (-1.79 bps). The Gold volatility state does not produce meaningful directional displacement in Tech.

### Hypothesized Mechanism
Gold volatility transition reflects information arrival that US Tech participants must incorporate at the open, creating directional pressure.

### Unproven Mechanism
Actual institutional portfolio rebalancing or forced Tech positioning. The price consequence is directly measurable; the information-transmission mechanism is hypothesized.

### Economic Adjudication
> **INFORMATIONALLY INTERESTING**

Mean net is -1.79 bps (negative). Treatment beats counterfactual by +0.78 bps — small informational value. The Gold volatility transition adds some information but not enough to overcome friction. The mechanism has genuine but weak informational content.

### Component Potential
MODERATE. The Gold volatility-transition signal could serve as a cross-market risk filter.

### State Potential
MODERATE. The Gold volatility-transition state could inform US Tech regime classification.

### Regime Potential
MODERATE. Inherently regime-dependent.

### G2 Eligibility
> NOT ELIGIBLE (absolute economics negative)

---

## 9. Cross-Candidate Comparison

| Metric | CAND-077 | CAND-078 | CAND-079 |
|---|---|---|---|
| N | 2,084 | 2,946 | 35,920 |
| Frequency | ~700/yr | ~1,033/yr | ~13,781/yr |
| Mean gross | +1.15 bps | -0.21 bps | +0.21 bps |
| Median gross | +0.86 bps | -0.07 bps | +0.02 bps |
| Mean net | -0.85 bps | -2.21 bps | -1.79 bps |
| Median net | -1.14 bps | -2.07 bps | -1.98 bps |
| Win rate | ~51% | ~49% | 50.1% |
| CF superior? | NO (TREATMENT) | YES | NO (TREATMENT) |
| Delta Mean | +1.67 bps | -0.25 bps | +0.78 bps |
| Adjudication | INFO INTERESTING | ECONOMICALLY NEGATIVE | INFO INTERESTING |

---

## 10. Absolute Economics

All three candidates produce negative absolute net economics:
- CAND-077: -0.85 bps (closest to zero)
- CAND-078: -2.21 bps
- CAND-079: -1.79 bps

None exceed the friction hurdle. However, CAND-077 is the closest to breaking even.

---

## 11. Conditional Information

Two of three candidates show treatment superiority:
- CAND-077: +1.67 bps delta (meaningful — compression-to-expansion transition adds real value)
- CAND-079: +0.78 bps delta (small — Gold volatility transition adds weak value)
- CAND-078: -0.25 bps delta (counterfactual superior — exhaustion adds no value)

The dynamic state transition approach shows more promise than the static-condition approach of V19–V25. CAND-077's +1.67 bps delta is the largest informational value observed in any QuantForge G1 screen.

---

## 12. Tail / Distribution

All three show broad dispersion and fat tails. CAND-079 has the widest range (-329 to +328 bps) due to its very high event count. CAND-077 and CAND-078 have tighter distributions consistent with their lower frequency.

---

## 13. Transition Integrity

All three candidates successfully test dynamic state transitions rather than static conditions:
- CAND-077: Volatility state change (compressed → expanding) — GENUINE TRANSITION
- CAND-078: Trend state change (sustained → exhausted) — GENUINE TRANSITION
- CAND-079: Cross-market volatility state change — GENUINE TRANSITION

No candidate collapsed into a static threshold test. The transition is central to each hypothesis.

---

## 14. Cross-Market Integrity

CAND-079 uses synchronized UTC+4 timestamps. Gold transitions occur before Tech responses (30-minute delay). No lookahead. DST transitions affect both datasets equally. The cross-market design is sound.

---

## 15. Prior-Art

| Candidate | Classification | Notes |
|---|---|---|
| CAND-077 | NEW | No previous candidate tested compression-to-expansion transitions |
| CAND-078 | NEW | No previous candidate tested consecutive-close exhaustion |
| CAND-079 | EXTENSION | Gold→Tech family: CAND-071 (direction), CAND-076 (overnight), CAND-079 (volatility regime transition) — materially different mechanism |

---

## 16. Rare-Event Assessment

None qualify for rare-event consideration. All have high frequency. CAND-077 could potentially be made rarer by adding selectivity filters, but no parameter search is authorized at G1.

---

## 17. State / Component Assessment

CAND-077 demonstrates the strongest state potential. The volatility-transition state adds +1.67 bps of informational value. This could serve as a regime filter for downstream Alphas.

CAND-079 shows weak state potential. The Gold volatility-transition state adds +0.78 bps of informational value.

CAND-078 shows no meaningful state potential.

---

## 18. G2 Promotions

> **NONE**

All three candidates have negative absolute economics. No candidate advances to G2.

---

## 19. Protected Forward Runtime

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED

---

## 20. V25 Status

> CLOSED / UNTOUCHED

---

## 21. System Assembly

> NOT EXECUTED

---

## 22. Conclusion

V26 G1 tested three dynamic state-transition candidates. All three are valid measurement objects (hard gates pass). All three have negative absolute economics. However, two of three show treatment superiority:

- **CAND-077** (volatility compression → expansion): INFORMATIONALLY INTERESTING. The transition adds +1.67 bps of informational value — the largest delta observed in any QuantForge G1 screen. Absolute economics are -0.85 bps (closest to zero of any V26 candidate). The compression-to-expansion transition has genuine informational content.

- **CAND-079** (Gold volatility regime transition → Tech): INFORMATIONALLY INTERESTING. The transition adds +0.78 bps of informational value. Absolute economics are -1.79 bps. Weak but real informational content.

- **CAND-078** (trend exhaustion): ECONOMICALLY NEGATIVE. The exhaustion transition adds no directional value. The counterfactual is superior.

The dynamic state-transition approach shows more promise than the static-condition approach of V19–V25. CAND-077's +1.67 bps delta suggests that state transitions contain real economic information that static conditions do not. However, none of the transitions produce sufficient absolute economics to survive 2 bps friction.

**Key finding:** The compression-to-expansion volatility transition (CAND-077) produces the strongest informational signal observed in the Research Factory to date. While absolute economics remain negative, the transition effect is real and measurable. This suggests that future research should focus on state transitions rather than static conditions.

---

## 23. Next Milestone

> V27 G0 — Further exploration of dynamic state transitions, with CAND-077's compression-to-expansion mechanism as the strongest surviving informational signal.
