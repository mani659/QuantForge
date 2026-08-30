# RESEARCH FACTORY V2 — G1 ECONOMIC PLAUSIBILITY SCREEN — V27
# DATE: 2026-08-30
# STATUS: V27 G1 COMPLETE
# NO G2 / NO OPTIMIZATION / NO RESCUE

---

## 1. G1 Status

> V27 G1 COMPLETE — 3 CANDIDATES EVALUATED

All three candidates passed validity gate evaluation. None achieved ECONOMICALLY PROMISING or QUALIFICATION-WORTHY status. All three are classified as INFORMATIONALLY INTERESTING or INSUFFICIENT.

---

## 2. V27 G0 Input

Three candidates from V27 G0:
- CAND-080: Vol Regime Quality Transition (smooth → choppy, fade entry)
- CAND-081: Structural Level Failure Trap (break-and-fail, counter-breakout fade)
- CAND-082: Post-Expansion Retracement Quality State (quality retracement → continuation)

All definitions frozen at G0. No modifications during G1.

---

## 3. G1 V3 Framework Applied

Two-layer architecture:
- Layer 1: 9 binary hard validity gates (measurement integrity)
- Layer 2: Economic evidence adjudication (holistic, not scorecard)

Friction: 2.0 bps round-trip.
Instrument: USATECHIDXUSD M1 (906,815 bars, 2023-09-01 to 2026-07-11).

---

## 4. Hard Validity Gate Method

Each candidate evaluated against 9 binary gates:
1. Deterministic definition
2. Executable entry
3. No hindsight
4. Correct cost normalization
5. Data integrity
6. Legitimate counterfactual
7. Causal claims limited to observables
8. No future-bar dependency
9. Reproducibility

All three candidates use deterministic, rule-based definitions with no hindsight contamination. Cost normalization is consistent (2 bps round-trip in bps). Data is USATECHIDXUSD M1. Counterfactuals are defined for CAND-081 and CAND-082; CAND-080's counterfactual failed to produce events.

---

## 5. CAND-080 — Vol Regime Quality Transition

### 5.1 Frozen Hypothesis

When market transitions from smooth directional movement to choppy movement (at roughly same ATR level), the regime quality change creates trapped trend participants whose forced exits produce measurable directional pressure.

### 5.2 Artifact Classification

Alpha / Event (provisional) — also State/Condition potential.

### 5.3 Mechanism

Smooth trending phase → directional inconsistency increases → choppy regime. Trapped trend participants exit, creating forced flow.

### 5.4 Observability

- ATR (20-bar): computable
- Directional inconsistency (20-bar rolling): computable
- Smooth-to-choppy transition: computable (incon crosses from <0.35 to >0.50)
- ATR constraint: computable (ATR within 80-120% of 20-bar average)

### 5.5 Treatment Definition

At close of first bar where directional inconsistency > 0.50 after being < 0.35 (within 10-bar window), enter SHORT (fade prior smooth trend). Exit after 60 minutes.

### 5.6 Counterfactual

Counterfactual: already-choppy market (incon > 0.40 for all of last 50 bars), same fade entry.

### 5.7 Counterfactual Discrimination

**FAILED.** The "already-choppy" condition produced ZERO events. The market is almost never independently choppy without having recently been smooth. The counterfactual cannot be evaluated.

### 5.8 Economic Consequence

Treatment: N=3,893, Freq=1,363/yr, Net Mean=-1.75 bps, Median=-1.77 bps, WR=50.8%.

### 5.9 Distribution Evidence

Mean=-1.75 bps, Median=-1.77 bps, Std=26.81 bps. Distribution is nearly symmetric around zero minus friction. Worst=-231 bps, Best=+321 bps. Excluding best event: Mean=-1.83 bps. No outlier dependence.

### 5.10 Economic Headroom

Negative after friction. No headroom.

### 5.11 Execution / Cost Considerations

2 bps round-trip friction fully consumes the small gross mean (+0.25 bps). No economic headroom.

### 5.12 Nine Hard Gates

| Gate | Status |
|---|---|
| 1. Deterministic definition | PASS |
| 2. Executable entry | PASS |
| 3. No hindsight | PASS |
| 4. Correct cost normalization | PASS |
| 5. Data integrity | PASS |
| 6. Legitimate counterfactual | **FAIL** — zero counterfactual events |
| 7. Causal claims limited to observables | PASS |
| 8. No future-bar dependency | PASS |
| 9. Reproducibility | PASS |

### 5.13 Economic Evidence Adjudication

> **INSUFFICIENT — NO COUNTERFACTUAL**

The treatment events are defined and executable. However, the counterfactual condition (independently choppy market) produced zero events. Without a valid counterfactual, the conditional value of the transition cannot be assessed.

The event count (3,893) is extremely high (~1,363/yr), suggesting the directional inconsistency thresholds may be too permissive, but this is a G0 definitional issue, not a G1 finding.

### 5.14 Failure Modes

1. **Counterfactual invalidation:** The "already-choppy" state is inseparable from the smooth-to-choppy transition — the market cannot be independently choppy without recently being smooth.
2. **Excessive event frequency:** ~1,363 events/year suggests the transition detection is too broad.
3. **No economic displacement:** Gross mean +0.25 bps is far below friction.

### 5.15 G1 Decision

> REJECT — Insufficient evidence due to counterfactual failure

### 5.16 Next-Stage Eligibility

Not eligible for G2. Not eligible for State review. The counterfactual must be redesigned before any future evaluation. The "already-choppy" condition is conceptually incompatible with the smooth-to-choppy transition — a different counterfactual formulation is needed.

---

## 6. CAND-081 — Structural Level Failure Trap

### 6.1 Frozen Hypothesis

When price breaks a structural level (20-bar high/low) by 3+ bps but reverses back through the level within 5 bars, trapped breakout participants create directional pressure against the breakout direction.

### 6.2 Artifact Classification

Alpha / Event (provisional) — also State/Condition potential.

### 6.3 Mechanism

Breakout → failure within 5 bars → trapped participants exit → directional pressure against breakout.

### 6.4 Observability

- 20-bar high/low: computable
- Breakout detection (3+ bps above level): computable
- Failure detection (close back through level within 5 bars): computable
- Subsequent 60-bar return: computable

### 6.5 Treatment Definition

At close of first bar that closes below 20-bar high after confirmed upside breakout (within 5-bar window), enter SHORT. Mirror for downside failures. Exit after 60 minutes.

### 6.6 Counterfactual

Successful breakouts: price breaks the level and stays above for 5+ bars (no failure). Same fade entry applied after confirmation.

### 6.7 Counterfactual Discrimination

The counterfactual is discriminating. It compares failed breakouts (trap formed) to successful breakouts (no trap). If the fade works better after failures than after successes, the trap mechanism is supported.

### 6.8 Economic Consequence

Treatment: N=3,887, Freq=1,361/yr, Net Mean=-0.78 bps, Median=-0.30 bps, WR=53.0%.
Counterfactual: N=3,364, Net Mean=-2.01 bps, Median=-2.62 bps, WR=48.3%.
Delta: Mean=+1.23 bps, Median=+2.33 bps — TREATMENT SUPERIOR.

### 6.9 Distribution Evidence

Treatment: Mean=-0.78 bps, Median=-0.30 bps, Std=43.97 bps. The median is close to zero after friction, suggesting the effect is broad-based. Worst=-398 bps, Best=+1,077 bps. Excluding best event: Mean=-1.06 bps.

The large best event (+1,077 bps) is a tail event. Excluding it reduces the mean slightly but does not change the qualitative conclusion.

### 6.10 Economic Headroom

Treatment net mean=-0.78 bps (negative). No standalone economic headroom. However, the conditional delta (+1.23 bps) is meaningful — the trap mechanism adds genuine informational value.

### 6.11 Execution / Cost Considerations

2 bps round-trip friction consumes most of the gross mean (+1.22 bps). The median (+1.70 bps gross, -0.30 bps net) suggests most events are near break-even after friction.

### 6.12 Nine Hard Gates

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

### 6.13 Economic Evidence Adjudication

> **INFORMATIONALLY INTERESTING**

The trap mechanism shows genuine conditional value: treatment outperforms counterfactual by +1.23 bps (mean) and +2.33 bps (median). This is the second-strongest conditional delta observed in QuantForge history (after CAND-077's +1.67 bps).

However, absolute economics remain negative (-0.78 bps mean, -0.30 bps median). The trap mechanism adds information but not enough to survive friction as a standalone Alpha.

### 6.14 Failure Modes

1. **Excessive event frequency:** ~1,361 events/year suggests the 20-bar structural level is too loose. A tighter level definition might produce fewer, higher-quality events.
2. **Negative absolute economics:** The trap adds informational value but not enough to overcome friction.
3. **Tail risk:** Worst event=-398 bps. The structural level provides a natural stop, but the stop may not always hold.

### 6.15 G1 Decision

> INFORMATIONALLY INTERESTING — Not economically sufficient for G2

### 6.16 Next-Stage Eligibility

Not eligible for G2 (absolute economics negative). Eligible for State/Condition review if a legitimate downstream Alpha is identified. The trap mechanism is genuine and may serve as a component filter.

---

## 7. CAND-082 — Post-Expansion Retracement Quality State

### 7.1 Frozen Hypothesis

After a volatility expansion, quality retracements (30-60% pullback, low volatility during retracement) are associated with better continuation outcomes than poor retracements (>60% pullback or high volatility during retracement).

### 7.2 Artifact Classification

State / Condition (primary) — also Alpha potential.

### 7.3 Mechanism

Expansion event → retracement assessment → quality/poor classification → continuation probability differs.

### 7.4 Observability

- ATR percentile (100-bar window): computable
- Expansion detection (ATR percentile <25 → >50): computable
- Retracement depth (fraction of expansion range): computable
- Retracement volatility (ATR during retracement vs expansion ATR): computable

### 7.5 Treatment Definition

After expansion detected, wait for 30% retracement. If retracement is quality (30-60% depth, retracement ATR < 70% of expansion ATR), enter in expansion direction. Exit after 60 minutes.

### 7.6 Counterfactual

Poor retracements: >60% depth OR retracement ATR > 100% of expansion ATR. Same continuation entry.

### 7.7 Counterfactual Discrimination

The counterfactual compares quality retracements to poor retracements after the same expansion event. This isolates the retracement quality state.

### 7.8 Economic Consequence

Treatment (quality): N=97, Freq=34/yr, Net Mean=-0.33 bps, Median=-3.70 bps, WR=47.4%.
Counterfactual (poor): N=3,324, Net Mean=-1.29 bps, Median=-2.07 bps, WR=49.8%.
Delta: Mean=+0.96 bps, Median=-1.63 bps — MIXED.

### 7.9 Distribution Evidence

Treatment: Mean=-0.33 bps, Median=-3.70 bps. The large gap between mean and median (3.37 bps) indicates the positive mean is driven by right-tail events, not broad-based economics. The median is deeply negative.

Best event=+212 bps, Worst=-63 bps. Excluding best event: Mean=-2.52 bps. The effect is outlier-dependent.

### 7.10 Economic Headroom

Treatment median=-3.70 bps is far below friction. No economic headroom for standalone Alpha. The positive mean is driven by a few large winners.

### 7.11 Execution / Cost Considerations

2 bps friction fully consumes the small gross mean (+1.67 bps). The negative median indicates most quality retracement continuation entries lose money after friction.

### 7.12 Nine Hard Gates

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

### 7.13 Economic Evidence Adjudication

> **INFORMATIONALLY INTERESTING**

The delta is MIXED: positive mean (+0.96 bps) but negative median (-1.63 bps). The positive mean is outlier-dependent (best event=+212 bps). The median indicates that quality retracement continuations do NOT produce better outcomes than poor retracement continuations.

The State hypothesis is contradicted: quality retracements do not lead to materially better continuation than poor retracements. The median is actually WORSE for quality (-3.70 bps) than for poor (-2.07 bps).

### 7.14 Failure Modes

1. **State hypothesis contradicted:** Quality retracements produce worse median outcomes than poor retracements. The retracement quality distinction does not contain meaningful State information.
2. **Outlier dependence:** The positive mean is driven by a single large winner (+212 bps), not broad-based economics.
3. **Low sample:** N=97 is adequate but not large. The quality retracement criteria may be too restrictive.
4. **Asymmetric sample sizes:** Treatment N=97 vs CF N=3,324. The quality criteria are much more restrictive than the poor criteria.

### 7.15 G1 Decision

> INFORMATIONALLY INTERESTING — State hypothesis not supported

### 7.16 Next-Stage Eligibility

Not eligible for G2. Not eligible for State review. The retracement quality distinction does not contain meaningful State information — quality retracements perform WORSE than poor retracements on median.

---

## 8. Cross-Candidate Comparison

| Metric | CAND-080 | CAND-081 | CAND-082 |
|---|---|---|---|
| N | 3,893 | 3,887 | 97 |
| Freq/yr | 1,363 | 1,361 | 34 |
| Gross Mean | +0.25 | +1.22 | +1.67 |
| Gross Median | +0.23 | +1.70 | -1.70 |
| Net Mean | -1.75 | -0.78 | -0.33 |
| Net Median | -1.77 | -0.30 | -3.70 |
| WR | 50.8% | 53.0% | 47.4% |
| CF N | 0 | 3,364 | 3,324 |
| CF Mean Net | N/A | -2.01 | -1.29 |
| Delta Mean | N/A | +1.23 | +0.96 |
| Delta Median | N/A | +2.33 | -1.63 |
| Adjudication | INSUFFICIENT | INFO INTERESTING | INFO INTERESTING |

---

## 9. Counterfactual Quality Comparison

| | CAND-080 | CAND-081 | CAND-082 |
|---|---|---|---|
| CF defined? | Yes | Yes | Yes |
| CF events? | **0** | 3,364 | 3,324 |
| CF valid? | **NO** | YES | YES |
| CF discriminating? | **N/A** | YES | YES |

CAND-080's counterfactual is invalid (zero events). CAND-081 and CAND-082 have valid, discriminating counterfactuals.

---

## 10. Economic Evidence Comparison

| | CAND-080 | CAND-081 | CAND-082 |
|---|---|---|---|
| Absolute economics | Negative | Negative | Negative |
| Conditional value | Unknown (no CF) | +1.23 bps (strong) | +0.96 bps (mixed) |
| Distribution | Symmetric | Broad-based median | Outlier-dependent |
| Economic headroom | None | None | None |

All three have negative absolute economics. CAND-081 has the strongest conditional value. CAND-082's conditional value is outlier-dependent.

---

## 11. Mechanism Quality Comparison

| | CAND-080 | CAND-081 | CAND-081 | CAND-082 |
|---|---|---|---|---|
| Mechanism test | Weak (no CF) | Strong (CF valid) | Strong | Weak (contradicted) |
| Dynamic-vs-static | Unclear | Clear (trap vs no-trap) | Clear | Unclear |
| Participant constraint | Hypothesized | Hypothesized | Hypothesized | Hypothesized |
| Economic displacement | None observed | Informational | Informational | Outlier-dependent |

---

## 12. G1 Adjudication Matrix

| Candidate | 9 Gates | Economic Evidence | Counterfactual | Mechanism | G1 Adjudication | Next Status |
|---|---|---|---|---|---|---|
| CAND-080 | 8/9 PASS (CF gate FAIL) | Negative, no CF | INVALID (0 events) | Weak (no CF) | INSUFFICIENT | CLOSED |
| CAND-081 | 9/9 PASS | Negative absolute, strong conditional | VALID (3,364 events) | Strong | INFORMATIONALLY INTERESTING | STATE REVIEW ELIGIBLE |
| CAND-082 | 9/9 PASS | Negative absolute, mixed conditional | VALID (3,324 events) | Contradicted | INFORMATIONALLY INTERESTING | CLOSED |

---

## 13. CAND-077 Firewall

> STATE REVIEW ELIGIBLE — PRESERVED — NOT REOPENED

CAND-077's post-closure filter observation (breakout >15 bps = 64.8% WR, +8.41 bps) remains EXPLORATORY EVIDENCE ONLY. It was not used as a V27 threshold, benchmark, or confirmation.

---

## 14. CAND-078

> CLOSED — ECONOMICALLY NEGATIVE / COUNTERFACTUAL INFERIORITY

No change.

---

## 15. CAND-079

> STATE OBSERVATION

No change.

---

## 16. Current State Library

| Candidate | Classification | Change |
|---|---|---|
| CAND-059 | STATE-ARTIFACT | No change |
| CAND-065 | STATE OBSERVATION | No change |
| CAND-069 | STATE OBSERVATION | No change |
| CAND-077 | STATE REVIEW ELIGIBLE | No change |
| CAND-079 | STATE OBSERVATION | No change |
| **CAND-081** | **STATE REVIEW ELIGIBLE** | **NEW** |

CAND-081's trap mechanism shows genuine conditional value (+1.23 bps delta). If a legitimate downstream Alpha is identified, CAND-081 could serve as a State/Condition that identifies trap states.

---

## 17. Protected Forward Runtime

CAND-015:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-024:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-035:
> ACTIVE / PROTECTED / UNTOUCHED

---

## 18. G2 Status

> NOT EXECUTED

No candidate achieved ECONOMICALLY PROMISING or QUALIFICATION-WORTHY status. G2 is not authorized for any V27 candidate.

---

## 19. System Assembly

> NOT EXECUTED

---

## 20. Governance Integrity

- No candidate was rescued
- No historical results were modified
- No forward runtime was touched
- No interaction study was performed
- No new candidates were generated during G1
- No thresholds were optimized
- CAND-077 was not reopened
- All nine validity gates were applied independently
- Economic adjudication is based on total evidence, not single metrics

---

## 21. Next Authorized Action

V27 G1 is complete. The next authorized actions are:

1. **CAND-081 State review:** If the owner authorizes, CAND-081's trap mechanism could be registered as a formal State hypothesis for future interaction testing.
2. **V28 G0:** A new discovery cycle may proceed independently.
3. **CAND-077 State review:** If the owner authorizes, CAND-077's State hypothesis could be registered.

No action is mandatory. All three paths are optional.

---

## 22. Forbidden Actions

- Run G2 for any V27 candidate
- Optimize CAND-080, CAND-081, or CAND-082
- Rescue CAND-080 (INSUFFICIENT)
- Use CAND-077's >15 bps threshold
- Modify forward runner
- Inspect CAND-015/024/035 performance
- Perform System Assembly
- Perform State interaction (requires separate authorization)
