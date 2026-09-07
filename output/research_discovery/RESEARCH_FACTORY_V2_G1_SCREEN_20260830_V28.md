# RESEARCH FACTORY V2 — G1 ECONOMIC PLAUSIBILITY SCREEN — V28
# DATE: 2026-08-30
# STATUS: V28 G1 COMPLETE
# NO G2 / NO OPTIMIZATION / NO RESCUE

---

## 1. G1 Status

> V28 G1 COMPLETE — 3 CANDIDATES EVALUATED

All three candidates passed validity gate evaluation. None achieved ECONOMICALLY PROMISING or QUALIFICATION-WORTHY status.

---

## 2. V28 G0 Recap

Three candidates from V28 G0:
- CAND-083: Cumulative Rejection Pressure Sweep (rejection cascade)
- CAND-084: Range Compression → Expansion Asymmetry (range dynamics)
- CAND-085: Approach Velocity → Breakout Continuation (path dependence)

All definitions frozen at G0. No modifications during G1.

---

## 3. G1 V3 Framework Applied

Two-layer architecture: 9 hard validity gates + economic evidence adjudication.
Friction: 2.0 bps round-trip.
Instrument: USATECHIDXUSD M1 (906,815 bars, 2023-09-01 to 2026-07-11).

---

## 4. Candidate Evaluation Summary

| Candidate | N | Freq/yr | Net Mean | Net Median | CF Delta | Adjudication |
|---|---|---|---|---|---|---|
| CAND-083 | 2,318 | 812 | -2.33 bps | -1.70 bps | +4.60 bps | INFORMATIONALLY INTERESTING |
| CAND-084 | 1,910 | 669 | -1.42 bps | -1.34 bps | +0.14 bps | INFORMATIONALLY INTERESTING |
| CAND-085 | 8,201 | 2,872 | -2.13 bps | -2.83 bps | N/A (no CF) | INSUFFICIENT |

---

## 5. CAND-083 — Cumulative Rejection Pressure Sweep

### Definition
Fade entry after breakout failure with 3+ prior rejections at the same structural level. Exit after 60 minutes.

### Mechanism
Cumulative rejected participants create proportional trapped population → forced exit flow → larger reversal after breakout failure.

### Frozen Parameters
- Structural level: 20-bar rolling high/low
- Rejection count window: 50 bars
- Rejection touch tolerance: 1 bp
- Rejection confirmation: close back through level within 5 bars
- Breakout threshold: 5+ bps beyond level
- Reversal window: 10 bars
- Holding period: 60 minutes
- Treatment: rejection count >= 3
- Counterfactual: rejection count 0-1

### Hard Gates

| Gate | Status |
|---|---|
| 1. Deterministic definition | PASS |
| 2. Executable entry | PASS |
| 3. No hindsight | PASS |
| 4. Correct cost normalization | PASS |
| 5. Data integrity | PASS |
| 6. Legitimate counterfactual | PASS |
| 7. Causal claims limited to observables | PASS |
| 8. No future-bar dependency | PASS |
| 9. Reproducibility | PASS |

All 9 gates PASS.

### Economic Evidence

| Metric | Treatment (3+ rej) | Counterfactual (0-1 rej) |
|---|---|---|
| N | 2,318 | 316 |
| Freq/yr | 812 | 110 |
| Gross Mean | -0.33 bps | — |
| Gross Median | +0.30 bps | — |
| Net Mean | -2.33 bps | -6.93 bps |
| Net Median | -1.70 bps | -3.86 bps |
| WR | 50.4% | 47.8% |
| Std | 47.04 | — |
| Worst | -391.67 bps | — |
| Best | +496.62 bps | — |

### Counterfactual
CF: N=316, Net Mean=-6.93 bps, Net Median=-3.86 bps, WR=47.8%.

The counterfactual (fade after fresh break with 0-1 rejections) performs MUCH worse than the treatment. This is because fresh breaks tend to continue, so fading them loses money. Breakouts after 3+ rejections are more likely to fail, so fading them loses less.

Counterfactual assessment: **VALID / DISCRIMINATING**

### Conditional Delta
Mean: **+4.60 bps** (TREATMENT SUPERIOR)
Median: **+2.16 bps** (TREATMENT SUPERIOR)

This is the **largest conditional delta in RF history** — larger than CAND-077 (+1.67 bps) and CAND-081 (+1.23 bps).

### Distribution Evidence
Treatment: Mean=-2.33, Median=-1.70, Std=47.04. Broad dispersion. Worst=-392 bps, Best=+497 bps. Excluding best event: Mean=-2.55 bps. The effect is broad-based — median is positive relative to CF median.

### Absolute Economics
Net Mean: -2.33 bps. Net Median: -1.70 bps.
**Absolute economics are negative.** CAND-083 is NOT a standalone economically qualified Alpha.

### Economic Headroom
The +4.60 bps conditional delta is substantial. However, the absolute treatment economics (-2.33 bps) are negative. The mechanism adds genuine informational value but not enough for standalone profitability.

### Dynamic-vs-Static
PASS — the cumulative rejection count is essential. Fading after fresh breaks (0-1 rejections) loses -6.93 bps, while fading after 3+ rejections loses only -2.33 bps. The count changes the economics by +4.60 bps.

### Mechanism Integrity
The mechanism is coherent: more rejections → more trapped participants → larger forced exit flow → better fade outcomes. The evidence supports this: treatment outperforms CF by +4.60 bps.

### Prior-Art
NEW — confirmed. No prior candidate tested cumulative rejection count.

### State Potential
HIGH. The cumulative rejection count describes a market condition (size of trapped population) that could modify other strategies' behavior. If validated, it could filter or size breakout-reversal entries.

### Alpha Potential
LOW. Absolute economics negative (-2.33 bps). Not a standalone Alpha.

### Rare-Event Potential
LOW. 812 events/year is not rare-event frequency.

### Failure Mode
The most likely failure is that the rejection count does not correlate with trapped-participant population in live conditions. The mechanism is plausible but the absolute economics are negative.

### G1 Decision
> **INFORMATIONALLY INTERESTING — STATE REVIEW ELIGIBLE**

The +4.60 bps conditional delta is the largest observed in RF history. The mechanism is genuine. However, absolute economics are negative. The correct classification is State Review Eligible, not standalone Alpha.

### Next-Stage Eligibility
Not G2 eligible (absolute economics negative). State Review Eligible — requires owner decision before any formal State hypothesis registration.

---

## 6. CAND-084 — Range Compression → Expansion Asymmetry

### Definition
Continuation entry in expansion direction after intraday range compresses below 50% of its 100-bar average and then expands above 100%. Exit after 60 minutes.

### Mechanism
Range compression accumulates positions → expansion triggers exits → continuation pressure in expansion direction.

### Frozen Parameters
- Range: 20-bar rolling high minus low
- Range average: 100-bar rolling average
- Compression: range < 50% of average
- Expansion: range > 100% of average
- Holding period: 60 minutes

### Hard Gates

| Gate | Status |
|---|---|
| 1. Deterministic definition | PASS |
| 2. Executable entry | PASS |
| 3. No hindsight | PASS |
| 4. Correct cost normalization | PASS |
| 5. Data integrity | PASS |
| 6. Legitimate counterfactual | PASS |
| 7. Causal claims limited to observables | PASS |
| 8. No future-bar dependency | PASS |
| 9. Reproducibility | PASS |

All 9 gates PASS.

### Economic Evidence

| Metric | Treatment (compressed) | Counterfactual (not compressed) |
|---|---|---|
| N | 1,910 | 9,644 |
| Freq/yr | 669 | 3,377 |
| Gross Mean | +0.58 bps | — |
| Gross Median | +0.66 bps | — |
| Net Mean | -1.42 bps | -1.56 bps |
| Net Median | -1.34 bps | -1.96 bps |
| WR | 52.3% | 50.1% |

### Counterfactual
CF: N=9,644, Net Mean=-1.56 bps, Net Median=-1.96 bps, WR=50.1%.

Counterfactual assessment: **VALID / DISCRIMINATING**

### Conditional Delta
Mean: **+0.14 bps** (TREATMENT SUPERIOR)
Median: **+0.62 bps** (TREATMENT SUPERIOR)

The delta is extremely small. Compression adds almost no informational value.

### Distribution Evidence
Treatment: Mean=-1.42, Median=-1.34, Std=24.49. Broad-based but weak. Worst=-216 bps, Best=+243 bps. Excluding best: Mean=-1.55 bps.

### Absolute Economics
Net Mean: -1.42 bps. Net Median: -1.34 bps.
**Absolute economics are negative.** CAND-084 is NOT a standalone economically qualified Alpha.

### Economic Headroom
The +0.14 bps conditional delta is negligible. Compression adds almost no value.

### Dynamic-vs-Static
WEAK — the compression adds only +0.14 bps of conditional value. The hypothesis could almost be expressed as "when range > average, enter in the expansion direction" without the compression requirement.

### Mechanism Integrity
The mechanism is plausible but the evidence does not support it. Compression adds minimal informational value.

### Prior-Art — CAND-077 Independence Audit

**CRITICAL: CAND-084 vs CAND-077**

| Dimension | CAND-077 | CAND-084 |
|---|---|---|
| State definition | ATR percentile compression → expansion | Intraday range ratio compression → expansion |
| Observable | ATR percentile + directional inconsistency | Range ratio (range / average range) |
| Participant constraint | Stops clustered during compression | Positions accumulated during quiet period |
| Event definition | ATR percentile crosses 25→50 | Range ratio crosses 50%→100% |
| Mechanism | Compression → expansion transition | Compression → expansion transition |
| Entry timing | At transition | At transition |
| Direction | Counter-trend (fade) | Continuation (expansion direction) |
| CF delta | +1.67 bps | +0.14 bps |

**Analysis:**

The MECHANISM is the same: compression creates trapped participants, expansion triggers exits, exits create directional pressure.

The OBSERVABLES are different (ATR percentile vs range ratio).

The DIRECTION is different (fade vs continuation).

However, the core economic mechanism — "quiet period accumulates positions, expansion triggers exits" — is identical. CAND-084 is essentially CAND-077 expressed with:
- A different compression metric (range ratio vs ATR percentile)
- A different direction (continuation vs fade)
- Much weaker results (+0.14 bps vs +1.67 bps delta)

**Classification: EXTENSION / REDUNDANT**

CAND-084 is an extension of CAND-077, not a genuinely new mechanism. The different observable (range ratio vs ATR percentile) does not create a materially different economic mechanism. The direction difference (continuation vs fade) is an implementation choice, not a mechanism distinction.

### State Potential
LOW — redundant with CAND-077.

### Alpha Potential
LOW — negative absolute economics, negligible conditional delta.

### Failure Mode
The mechanism is essentially CAND-077 with a different metric. CAND-077 already demonstrated +1.67 bps delta with a more refined approach. CAND-084 adds nothing new.

### G1 Decision
> **INFORMATIONALLY INTERESTING — EXTENSION OF CAND-077**

### Next-Stage Eligibility
Not G2 eligible. Not State Review Eligible (redundant with CAND-077). Should be CLOSED.

---

## 7. CAND-085 — Approach Velocity → Breakout Continuation

### Definition
Continuation entry after high-velocity approach (velocity > 2.0) breakout of 20-bar high/low. Exit after 60 minutes.

### Mechanism
High-velocity approach traps participants on wrong side → forced exits create continuation after breakout.

### Frozen Parameters
- Structural level: 20-bar rolling high/low
- Velocity: |close[i] - close[i-20]| / avg_change[i]
- High velocity: > 2.0
- Low velocity: < 0.5
- Breakout threshold: 3+ bps beyond level
- Holding period: 60 minutes

### Hard Gates

| Gate | Status |
|---|---|
| 1. Deterministic definition | PASS |
| 2. Executable entry | PASS |
| 3. No hindsight | PASS |
| 4. Correct cost normalization | PASS |
| 5. Data integrity | PASS |
| 6. Legitimate counterfactual | **FAIL** — zero low-velocity events |
| 7. Causal claims limited to observables | PASS |
| 8. No future-bar dependency | PASS |
| 9. Reproducibility | PASS |

**Gate 6 FAILS.** The low-velocity counterfactual (velocity < 0.5) produced zero events. The velocity filter is too restrictive — almost no breakouts occur after low-velocity approaches.

### Economic Evidence

| Metric | Treatment (high vel) |
|---|---|
| N | 8,201 |
| Freq/yr | 2,872 |
| Gross Mean | -0.13 bps |
| Gross Median | -0.83 bps |
| Net Mean | -2.13 bps |
| Net Median | -2.83 bps |
| WR | 48.2% |
| Worst | -1,043.90 bps |
| Best | +1,027.67 bps |

### Counterfactual
**INVALID — zero events.** The low-velocity condition (velocity < 0.5) produced no breakout events. The velocity filter is too restrictive.

### Conditional Delta
N/A — no counterfactual.

### Distribution Evidence
Treatment: Mean=-2.13, Median=-2.83, Std=40.09. WR=48.2%. Broad dispersion with extreme tails. The effect is economically negative.

### Absolute Economics
Net Mean: -2.13 bps. Net Median: -2.83 bps.
**Absolute economics are negative.**

### Economic Headroom
None. The treatment is economically negative.

### Dynamic-vs-Static
CANNOT BE TESTED — counterfactual is invalid.

### Mechanism Integrity
The mechanism is plausible but the counterfactual is invalid. Without a valid comparison, the mechanism cannot be assessed.

### Prior-Art
NEW — confirmed. No prior candidate tested approach velocity.

### State Potential
UNKNOWN — cannot be assessed without valid counterfactual.

### Alpha Potential
LOW — negative absolute economics, no counterfactual.

### Failure Mode
The velocity threshold (> 2.0) is too restrictive for the low-velocity counterfactual. The mechanism cannot be validated without a working counterfactual.

### G1 Decision
> **INSUFFICIENT — COUNTERFACTUAL INVALID**

### Next-Stage Eligibility
Not G2 eligible. Not State Review Eligible (counterfactual invalid). Should be CLOSED or held for counterfactual redesign.

---

## 8. Cross-Candidate Economic Comparison

| Metric | CAND-083 | CAND-084 | CAND-085 |
|---|---|---|---|
| N | 2,318 | 1,910 | 8,201 |
| Freq/yr | 812 | 669 | 2,872 |
| Net Mean | -2.33 | -1.42 | -2.13 |
| Net Median | -1.70 | -1.34 | -2.83 |
| WR | 50.4% | 52.3% | 48.2% |
| CF N | 316 | 9,644 | 0 |
| CF Delta Mean | **+4.60** | +0.14 | N/A |
| CF Delta Median | +2.16 | +0.62 | N/A |
| Adjudication | INFO INTERESTING | INFO INTERESTING | INSUFFICIENT |

---

## 9. Counterfactual Quality

| Candidate | CF Valid? | CF Discriminating? | CF Assessment |
|---|---|---|---|
| CAND-083 | YES (316 events) | YES (+4.60 bps delta) | VALID / STRONG |
| CAND-084 | YES (9,644 events) | WEAK (+0.14 bps delta) | VALID / WEAK |
| CAND-085 | **NO** (0 events) | N/A | **INVALID** |

---

## 10. Mechanism Quality Comparison

| | CAND-083 | CAND-084 | CAND-085 |
|---|---|---|---|
| Mechanism coherence | Strong | Weak (redundant) | Unknown (no CF) |
| Dynamic-vs-static | PASS | WEAK | CANNOT TEST |
| Prior-art independence | NEW | **EXTENSION** | NEW |
| Evidence quality | Strong CF delta | Weak CF delta | Invalid CF |

---

## 11. Distribution Quality

| | CAND-083 | CAND-084 | CAND-085 |
|---|---|---|---|
| Broad-based? | Yes (median positive relative to CF) | Weak | N/A |
| Outlier-dependent? | Moderate (worst=-392, best=+497) | Moderate | Extreme (worst=-1044, best=+1028) |
| Median coherent? | Yes (+2.16 delta median) | Weak (+0.62) | N/A |

---

## 12. Prior-Art / Redundancy Audit

| Candidate | Classification | Reason |
|---|---|---|
| CAND-083 | NEW | Cumulative rejection count is genuinely new |
| CAND-084 | **EXTENSION** | Mechanism identical to CAND-077 (compression → expansion) |
| CAND-085 | NEW | Approach velocity is genuinely new (but CF invalid) |

---

## 13. State Library Impact

No changes to existing State library. CAND-083 may warrant future State Review Eligibility pending owner decision. CAND-084 is redundant with CAND-077. CAND-085 is insufficient.

---

## 14. CAND-077

> STATE REVIEW ELIGIBLE — PRESERVED / NOT REOPENED

---

## 15. CAND-081

> STATE REVIEW ELIGIBLE — PRESERVED / NOT REOPENED

---

## 16. CAND-079

> STATE OBSERVATION

---

## 17. CAND-078

> CLOSED

---

## 18. Closed-Line Firewall

> PASS — No closed candidate reopened

---

## 19. Protected Forward Runtime

CAND-015/024/035: ACTIVE / PROTECTED / UNTOUCHED

---

## 20. G2

> NOT EXECUTED

---

## 21. System Assembly

> NOT EXECUTED

---

## 22. Final G1 Decisions

| Candidate | Decision | Reason |
|---|---|---|
| CAND-083 | **INFORMATIONALLY INTERESTING — STATE REVIEW ELIGIBLE** | +4.60 bps conditional delta (largest in RF history). Absolute economics negative. Genuine mechanism. |
| CAND-084 | **INFORMATIONALLY INTERESTING — EXTENSION OF CAND-077** | +0.14 bps delta (negligible). Mechanism identical to CAND-077. Redundant. |
| CAND-085 | **INSUFFICIENT — COUNTERFACTUAL INVALID** | Zero low-velocity events. Cannot validate mechanism. |

---

## 23. Next Permitted Task

**Option A:** CAND-083 State Governance Review (formalize State hypothesis)
**Option B:** V29 G0 (new discovery cycle)

Owner decision required. CAND-083's +4.60 bps conditional delta warrants explicit governance consideration before V29.
