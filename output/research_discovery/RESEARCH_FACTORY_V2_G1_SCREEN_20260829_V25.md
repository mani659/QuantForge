# RESEARCH FACTORY V2 — G1 ECONOMIC PLAUSIBILITY SCREEN — V25
# DATE: 2026-08-29
# STATUS: G1 COMPLETE — NO G2 PROMOTIONS

---

## 1. G1 Status

> V25 G1 COMPLETE. All three candidates evaluated under the ratified G1 V3 Evidence-Based Adjudication Framework. Zero candidates promoted to G2.

---

## 2. V3 Framework Applied

This screen uses the two-layer G1 V3 architecture:

**Layer 1 — Hard Validity Gates:** All three candidates pass all nine validity gates (deterministic definition, executable entry, no hindsight, correct cost normalization, data integrity, legitimate counterfactual, causal claims limited to observables, no future-bar dependency, reproducibility).

**Layer 2 — Economic Evidence Adjudication:** All economic statistics are evidence inputs, not thresholds. The G1 decision reads the total evidence profile.

---

## 3. Data Used

| Instrument | Bars | Date Range |
|---|---|---|
| XAUUSD M1 | 1,768,123 | 2021-04-12 to 2026-04-10 |
| USATECHIDXUSD M1 | 906,815 | 2023-09-01 to 2026-07-10 |

Timezone: UTC+4 (consistent with existing V24 infrastructure). DST transitions handled per candidate.

---

## 4. Cost / Friction Normalization

**Universal:** 2.0 bps round-trip (spread + slippage).

All economic results reported in basis points (bps). No mixing of price points, ticks, or currency units.

For XAUUSD: friction is 2.0 bps on gold price (~$3,300/oz), equivalent to ~$0.66/oz round-trip.

For USATECHIDXUSD: friction is 2.0 bps on index (~30,000), equivalent to ~6 index points round-trip.

---

## 5. Hard Validity Gate Results

| Gate | CAND-074 | CAND-075 | CAND-076 |
|---|---|---|---|
| Deterministic definition | PASS | PASS | PASS |
| Executable entry | PASS | PASS | PASS |
| No hindsight | PASS | PASS | PASS |
| Correct cost normalization | PASS | PASS | PASS |
| Data integrity | PASS | PASS | PASS |
| Legitimate counterfactual | PASS | PASS | PASS |
| Causal claims limited to observables | PASS | PASS | PASS |
| No future-bar dependency | PASS | PASS | PASS |
| Reproducible | PASS | PASS | PASS |

All three candidates are valid measurement objects. Economic failures are not validity failures.

---

## 6. CAND-074 — London Gold Fix Benchmark Execution Pressure

### Definition
Enter XAUUSD at 10:30 AM London time (London AM Fix) in the direction of the pre-fix move (10:00–10:30 AM London). Exit at 11:00 AM London (30 minutes after entry).

### Treatment
- Pre-fix directional move: XAUUSD return from 10:00 to 10:30 AM London
- Entry: 10:30 AM London, same direction as pre-fix move
- Exit: 11:00 AM London

### Counterfactual
Same time-of-day window (30-minute directional move → 30-minute outcome) on days where the pre-fix magnitude is applied to a random afternoon session window instead of the fix window. The counterfactual isolates whether the fix window itself adds directional value beyond general momentum.

### N / Frequency
- N = 1,285
- Frequency = 257.5/year

### Gross Economics
- Mean gross = +0.28 bps
- Median gross = -0.32 bps

### Net Economics
- Mean net = **-1.72 bps**
- Median net = **-2.32 bps**

### Distribution
- Win rate = 49.3%
- StdDev = 16.57 bps
- Worst event = -212.32 bps
- Best event = +104.44 bps

### Tail Diagnostics
- Exclude-best-event mean = -1.80 bps
- Payoff concentration = unreliable (total sum near zero)

### Counterfactual Delta
- Counterfactual N = 1,026
- Counterfactual mean net = -1.66 bps
- Counterfactual median net = -2.29 bps
- Delta mean = -0.06 bps (treatment WORSE than control)
- Delta median = -0.03 bps (treatment WORSE than control)
- Gate: **COUNTERFACTUAL SUPERIOR**

### Executable Integrity
PASS. Entry at fix time is deterministic. Exit at 11:00 AM London is deterministic. No hindsight.

### Observable Behavior
The London Gold Fix window produces mean gross returns of +0.28 bps (essentially zero). The fix window does NOT amplify the pre-fix direction. The counterfactual (same momentum applied to non-fix windows) produces slightly better economics. The fix window appears to be economically neutral — it neither amplifies nor dampens pre-existing momentum.

### Hypothesized Mechanism
The hypothesis was that fix participants' contractual obligation to transact at the fix would create concentrated, directional order flow that amplifies the pre-fix move. The data does not support this. The fix window does not produce measurably different directional behavior from random intraday windows.

### Causal Observability
The fix timing is observable. The price movement into and out of the fix is observable. The fix participant motivations (contractual obligation) are hypothesized but not directly observed. The price consequence is directly measurable: the fix window adds no directional value.

### Economic Adjudication
> **ECONOMICALLY NEGATIVE**

Mean net is -1.72 bps. The counterfactual is superior. The fix window does not add directional value. The mechanism does not produce friction-surviving economics.

### G2 Eligibility
> NOT ELIGIBLE

---

## 7. CAND-075 — US Equity Closing Auction Concentrated Order Flow

### Definition
Enter USATECHIDXUSD at 3:59 PM ET in the direction of the late-session move (3:50–3:59 PM ET). Exit at 4:00 PM ET (the closing auction).

### Treatment
- Late-session directional move: USATECHIDXUSD return from 3:50 to 3:59 PM ET
- Entry: 3:59 PM ET, same direction as late-session move
- Exit: 4:00 PM ET close

### Counterfactual
Same late-session momentum applied to a random midday window (12:00–12:10 PM ET direction → 12:10–12:20 PM outcome). The counterfactual isolates whether the closing auction itself adds directional value beyond general late-session momentum.

### N / Frequency
- N = 623
- Frequency = 218.2/year

### Gross Economics
- Mean gross = -0.15 bps
- Median gross = -0.28 bps

### Net Economics
- Mean net = **-2.15 bps**
- Median net = **-2.28 bps**

### Distribution
- Win rate = 45.7%
- StdDev = 5.32 bps
- Worst event = -19.27 bps
- Best event = +37.34 bps

### Tail Diagnostics
- Exclude-best-event mean = -2.21 bps

### Counterfactual Delta
- Counterfactual N = 526
- Counterfactual mean net = -2.07 bps
- Counterfactual median net = -2.09 bps
- Delta mean = -0.08 bps (treatment WORSE than control)
- Delta median = -0.19 bps (treatment WORSE than control)
- Gate: **COUNTERFACTUAL SUPERIOR**

### Executable Integrity
PASS. Entry at 3:59 PM ET is deterministic. Exit at 4:00 PM ET is deterministic. No hindsight.

### Observable Behavior
The closing auction window produces mean gross returns of -0.15 bps (essentially zero). The closing auction does NOT amplify late-session momentum. The counterfactual (same momentum at midday) produces slightly better economics. The closing auction appears to be economically neutral to slightly negative for directional momentum.

### Hypothesized Mechanism
The hypothesis was that MOC order flow concentrated in the final minutes would amplify late-session direction. The data does not support this. The closing auction does not produce measurably different directional behavior from random intraday windows. If anything, the closing auction slightly dampens momentum (possibly due to mean-reversion at the close).

### Causal Observability
The closing auction timing is observable. The price movement into and out of the close is observable. The MOC order flow motivations (mandate compliance) are hypothesized but not directly observed. The price consequence is directly measurable: the closing auction adds no directional value.

### Economic Adjudication
> **ECONOMICALLY NEGATIVE**

Mean net is -2.15 bps. The counterfactual is superior. The closing auction does not add directional value. The mechanism does not produce friction-surviving economics.

### G2 Eligibility
> NOT ELIGIBLE

---

## 8. CAND-076 — Gold Overnight Repricing → Tech Opening Direction

### Definition
Enter USATECHIDXUSD at 9:30 AM ET in the direction of the overnight Gold move (previous 4:00 PM ET close to current 9:00 AM ET price). Exit at 10:00 AM ET (30 minutes after entry).

### Treatment
- Overnight Gold move: (XAUUSD at 9:00 AM ET - XAUUSD at previous 4:00 PM ET) / previous close × 10,000 bps
- Entry: 9:30 AM ET, same direction as overnight Gold move
- Exit: 10:00 AM ET

### Counterfactual
Same time window (9:30–10:00 AM ET) on days with small overnight Gold movement (< 5 bps). The counterfactual isolates whether Gold information provides value beyond normal morning momentum.

### N / Frequency
- N = 466
- Frequency = 178.8/year

### Gross Economics
- Mean gross = -0.14 bps
- Median gross = -0.83 bps

### Net Economics
- Mean net = **-2.14 bps**
- Median net = **-2.83 bps**

### Distribution
- Win rate = 47.9%
- StdDev = 21.27 bps
- Worst event = -83.56 bps
- Best event = +247.24 bps

### Tail Diagnostics
- Exclude-best-event mean = -2.68 bps

### Counterfactual Delta
- Counterfactual N = 90
- Counterfactual mean net = +0.05 bps
- Counterfactual median net = -0.84 bps
- Delta mean = -2.20 bps (treatment WORSE than control)
- Delta median = -1.99 bps (treatment WORSE than control)
- Gate: **COUNTERFACTUAL SUPERIOR**

### Executable Integrity
PASS. Entry at 9:30 AM ET is deterministic. Exit at 10:00 AM ET is deterministic. Gold overnight price is computable from available data. No hindsight.

### Observable Behavior
The overnight Gold direction signal applied to the US Tech open produces mean gross returns of -0.14 bps (essentially zero). The counterfactual (same time window without significant Gold movement) produces slightly better economics (+0.05 bps net). The Gold overnight move does NOT predict Tech opening direction in the same direction.

### Hypothesized Mechanism
The hypothesis was that Gold repricing overnight reflects risk sentiment shifts that US Tech participants incorporate at the open, creating a delayed directional reaction. The data shows the OPPOSITE pattern: on days with significant overnight Gold moves, Tech opening returns in the Gold direction are slightly negative. This may reflect a risk-off dynamic (Gold up → Tech down) rather than the hypothesized risk-on transmission (Gold up → Tech up). The mechanism is not validated.

### Causal Observability
Gold overnight movement is observable. US Tech opening direction is observable. The information transmission mechanism (Gold → risk sentiment → Tech repricing) is hypothesized but the observed pattern is inverse to the hypothesis. The data directly contradicts the registered directional hypothesis.

### Economic Adjudication
> **ECONOMICALLY NEGATIVE**

Mean net is -2.14 bps. The counterfactual is materially superior (+0.05 bps net vs -2.14 bps). The Gold overnight direction signal produces economics WORSE than having no Gold signal at all. The mechanism does not produce friction-surviving economics.

### G2 Eligibility
> NOT ELIGIBLE

---

## 9. Cross-Candidate Comparison

| Metric | CAND-074 | CAND-075 | CAND-076 |
|---|---|---|---|
| N | 1,285 | 623 | 466 |
| Frequency | 257.5/yr | 218.2/yr | 178.8/yr |
| Mean gross | +0.28 bps | -0.15 bps | -0.14 bps |
| Median gross | -0.32 bps | -0.28 bps | -0.83 bps |
| Mean net | -1.72 bps | -2.15 bps | -2.14 bps |
| Median net | -2.32 bps | -2.28 bps | -2.83 bps |
| Win rate | 49.3% | 45.7% | 47.9% |
| CF superior? | YES | YES | YES |
| Adjudication | NEGATIVE | NEGATIVE | NEGATIVE |

All three candidates show the same pattern: mean gross near zero, friction creates negative net economics, counterfactual is superior to treatment.

---

## 10. Absolute Economics

All three candidates produce negative absolute net economics:

- CAND-074: -1.72 bps mean net
- CAND-075: -2.15 bps mean net
- CAND-076: -2.14 bps mean net

None exceed the friction hurdle. The gross returns are essentially zero — these mechanisms do not produce meaningful directional movement.

---

## 11. Conditional Information Value

All three candidates show counterfactual superiority (the control outperforms the treatment). This means:

- The fix window (CAND-074) adds no directional value beyond random momentum
- The closing auction (CAND-075) adds no directional value beyond random momentum
- The Gold overnight direction (CAND-076) is inversely related to Tech opening direction

None show meaningful incremental condition value. The counterfactual superiority is small in absolute terms (all deltas < 0.2 bps), indicating the mechanisms are economically neutral rather than harmful.

---

## 12. Payoff / Tail Structure

All three candidates show:
- Broad dispersion (StdDev 5–21 bps)
- Fat tails (worst events -19 to -212 bps)
- Near-zero mean gross
- Negative median gross

The payoff structure is dominated by friction, not by the mechanism. The mechanisms produce no meaningful asymmetry.

---

## 13. Counterfactual Summary

| Candidate | Treatment Net | CF Net | Delta | Gate |
|---|---|---|---|---|
| CAND-074 | -1.72 bps | -1.66 bps | -0.06 bps | CF SUPERIOR |
| CAND-075 | -2.15 bps | -2.07 bps | -0.08 bps | CF SUPERIOR |
| CAND-076 | -2.14 bps | +0.05 bps | -2.20 bps | CF SUPERIOR |

CAND-076 shows the largest counterfactual gap — the Gold direction signal actively underperforms no-signal control.

---

## 14. Data / Causal Limitations

- All candidates use available M1 data. No hidden data required.
- Fix participant motivations (CAND-074) and MOC order flow (CAND-075) are hypothesized, not directly observed.
- Gold → Tech information transmission mechanism (CAND-076) is hypothesized; the observed pattern is inverse to the hypothesis.
- DST transitions are handled approximately (hour-level), which could introduce small timing errors at seasonal boundaries.

---

## 15. Prior-Art

| Candidate | Classification | Notes |
|---|---|---|
| CAND-074 | NEW | No previous candidate tested London Gold Fix |
| CAND-075 | NEW | No previous candidate tested closing auction |
| CAND-076 | EXTENSION | CAND-071 tested Gold→Tech; CAND-076 uses different threshold (5 vs 30 bps) and different hypothesis |

CAND-076's inverse result is consistent with CAND-071's negative economics. The Gold→Tech direction signal does not produce positive returns in either formulation.

---

## 16. Rare-Event Assessment

None of the three candidates qualify for rare-event consideration:
- All three have high frequency (178–257/year)
- All three have negative absolute economics
- Low frequency would not rescue these candidates because per-event economics are also negative

---

## 17. State / Component Assessment

No V25 candidates demonstrate meaningful state or component potential:
- CAND-074: fix direction shows no incremental information
- CAND-075: late-session direction shows no incremental information
- CAND-076: Gold direction shows INVERSE information (not the hypothesized direction)

None are suitable as inputs to downstream Alpha qualification.

---

## 18. G2 Promotions

> **NONE**

All three candidates are ECONOMICALLY NEGATIVE. No candidate advances to G2.

---

## 19. Protected Forward Runtime

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED

No forward performance was inspected during this G1 screen.

---

## 20. System Assembly

> NOT EXECUTED

---

## 21. Conclusion

V25 G1 tested three candidates from two economic displacement mechanism families (Settlement/Benchmark and Cross-Market Transmission). All three failed the economic evidence gate:

- **CAND-074** (London Gold Fix): The fix window adds no directional value. Fix participants' concentrated order flow does not produce measurable price amplification.
- **CAND-075** (Closing Auction): The closing auction adds no directional value. MOC order flow does not produce measurable price amplification.
- **CAND-076** (Gold→Tech overnight): The Gold overnight direction signal is inversely related to Tech opening direction, contradicting the registered hypothesis.

All three candidates are valid measurement objects (hard gates pass). The economic evidence is clear: these mechanisms do not produce friction-surviving directional value.

This is the third consecutive G0 cycle (V24, V25) where all candidates failed G1. The V19-V24 meta-review pattern — conditionally informative but economically unmonetizable — continues into V25, though with an important distinction: V25 candidates from settlement/benchmark families also failed, suggesting the problem is not limited to price-pattern hypotheses.

---

## 22. Next Milestone

> V26 G0 — Continued mechanism diversity exploration, with explicit consideration of whether settlement/benchmark mechanisms require different testable formulations.
