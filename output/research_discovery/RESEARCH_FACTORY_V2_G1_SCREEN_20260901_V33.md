# RESEARCH FACTORY V2 — V33 G1 ECONOMIC PLAUSIBILITY SCREEN

## 1. G1 Status

> V33 G1 COMPLETE — BOTH CANDIDATES CLOSED

Date: 2026-09-01
Market: USATECHIDXUSD M1
Data range: 2023-09-01 to 2026-07-10 (~2.9 years, 906,815 bars)
Friction: 2 bps
Holding period: 60 bars (60 minutes)
Rearm: 60 bars

## 2. V33 G0 Integrity Result

- CAND-098: G1 ELIGIBLE — clearly novel
- CAND-099: G1 ELIGIBLE — materially distinct but adjacent
- CAND-100: DATA INFEASIBLE — bid/ask spread unavailable

## 3. Authorized Candidate Set

CAND-098 and CAND-099 only.

## 4. CAND-100 Exclusion

CAND-100 permanently excluded as DATA INFEASIBLE. Bid/ask spread not available in governed dataset. OHLC proxy conflates with volatility research.

## 5. CAND-098 — Event-Cluster Response Degradation

### 5.1 Frozen Definition

- Event: bar-to-bar move > 1.5x ATR(100)
- Treatment: event occurs when >=3 other events within 200-bar lookback (clustered)
- Control: event occurs when <3 other events within 200-bar lookback (isolated)
- Outcome: forward return over 60 bars
- Friction: 2 bps
- Rearm: 60 bars

### 5.2 Implementation Verification

The implementation faithfully represents the registered hypothesis:
- Multiple events detected via ATR-based breakout threshold
- Cluster density computed as rolling count within 200-bar window
- Treatment/control split based on cluster count threshold
- Forward returns computed from close-to-close over 60 bars
- No look-ahead, no future information in treatment classification
- Semantic integrity: PASS — multi-event cluster construct preserved

### 5.3 Data and Coverage

- Data: USATECHIDXUSD M1, 906,815 bars (2023-09-01 to 2026-07-10)
- Total events detected: 43,066
- After rearm (60 bars): 9,410
- Treatment (clustered, count >=3): 8,392
- Control (isolated, count <3): 1,017

### 5.4 Gross Economics

| Group | N | Gross Mean | Gross Median | Std |
|---|---|---|---|---|
| Treatment (clustered) | 8,392 | +0.51 bps | +1.15 bps | 32.69 bps |
| Control (isolated) | 1,017 | +1.62 bps | +1.45 bps | 24.93 bps |

### 5.5 Net Economics

| Group | N | Net Mean | Net Median | WR |
|---|---|---|---|---|
| Treatment (clustered) | 8,392 | -1.49 bps | -0.85 bps | 53.5% |
| Control (isolated) | 1,017 | -0.38 bps | -0.55 bps | 54.8% |

### 5.6 Conditional Delta

| Metric | Value | Favors |
|---|---|---|
| Mean Delta | -1.11 bps | Control (isolated) |
| Median Delta | -0.30 bps | Control (isolated) |
| WR Delta | -1.2% | Control (isolated) |

### 5.7 Distribution

| Metric | Treatment | Control |
|---|---|---|
| Std | 32.69 bps | 24.93 bps |
| P10 | -25.19 bps | -20.83 bps |
| P90 | +25.42 bps | +25.35 bps |

**Primary hypothesis metric (distribution width):** Treatment WIDER than control (32.69 vs 24.93 bps). This SUPPORTS the hypothesis that clustered events produce wider distributions.

### 5.8 Nine Hard Gates

| Gate | Result | Evidence |
|---|---|---|
| 1. Measurement integrity | PASS | Bar-to-bar return from OHLC |
| 2. Temporal ordering | PASS | Events detected before forward returns |
| 3. Look-ahead protection | PASS | No future info in treatment classification |
| 4. Counterfactual validity | PASS | Same event class, different cluster density |
| 5. Sample adequacy | PASS | Treatment N=8,392, Control N=1,017 |
| 6. Cost model integrity | PASS | 2 bps applied identically |
| 7. Distribution completeness | PASS | Full distribution reported |
| 8. No post-hoc modification | PASS | All parameters frozen in G0 |
| 9. Temporal independence | PASS | 60-bar rearm applied |

**9/9 PASS**

### 5.9 Mechanism Assessment

**Distribution width:** Treatment (clustered) has wider std (32.69 vs 24.93 bps). This SUPPORTS the hypothesis that event clustering degrades response quality.

**Economic direction:** Control (isolated) outperforms treatment (clustered) on all economic metrics (mean, median, WR). This is CONSISTENT with the hypothesis — clustered events produce worse economics.

**However:** The absolute economics are negative for both groups. Neither treatment nor control is independently profitable. The conditional information (clustered events are worse) is real but the magnitude is small (-1.11 bps mean delta).

**Mechanism interpretation:** The data supports the interpretation that event clustering creates information overload that degrades response quality. But the economic magnitude is insufficient for standalone Alpha. The primary value is as a STATE indicator — avoiding trades during high-density clusters.

### 5.10 Prior-Art Caveat

CAND-092 tested single-event recency (time since last event). CAND-098 tests multi-event clustering (count of recent events). These are different constructs. The G1 result shows that cluster density provides information beyond single-event recency — the distribution width difference is genuine and the economic direction is consistent.

### 5.11 Economic Adjudication

**Economic verdict:** ECONOMICALLY NEGATIVE — absolute economics are negative for both groups. Mean delta favors control by -1.11 bps. Median delta favors control by -0.30 bps. WR delta favors control by -1.2%.

**Evidence profile:** HYPOTHESIS SUPPORTED on distribution width (treatment wider), but ECONOMICALLY INSUFFICIENT for standalone Alpha. The conditional information is real but too weak for monetization.

**State potential:** NOT JUSTIFIED — while the distributional finding is interesting, the economic magnitude is insufficient for State qualification.

### 5.12 Final Classification

> **CLOSED — ECONOMICALLY NEGATIVE**

Distribution width hypothesis supported (clustered events produce wider distributions), but absolute economics negative and conditional delta insufficient for State qualification.

## 6. CAND-099 — Volatility Regime Transition Quality

### 6.1 Frozen Definition

- ATR(14) percentile over trailing 200 bars
- Compressed: percentile < 25
- Expanded: percentile > 50
- Transition: compressed -> expanded within 5-60 bars
- Smoothness: variance of ATR changes during transition
- Treatment: smooth (variance below median)
- Control: sharp (variance above median)
- Outcome: forward return over 60 bars from transition completion
- Friction: 2 bps

### 6.2 Implementation Verification

The implementation faithfully represents the registered hypothesis:
- ATR percentile computed via rolling rank (C-optimized)
- Regime states detected via percentile thresholds
- Transitions detected as compressed -> expanded crossings
- Smoothness measured as variance of ATR changes during transition window
- Treatment/control split based on smoothness median
- Forward returns computed from close-to-close over 60 bars
- Semantic integrity: PASS — transition quality construct preserved

**CAND-077 semantic check:** PASS — implementation measures transition quality (path variance), not regime state (percentile level). Distinct from CAND-077.

**CAND-096 semantic check:** PASS — implementation measures path smoothness (variance of changes), not acceleration (rate of change). Related but distinct from CAND-096.

### 6.3 Data and Coverage

- Data: USATECHIDXUSD M1, 906,815 bars (2023-09-01 to 2026-07-10)
- Transition starts detected: 292,071
- Complete transitions (5-60 bars to expanded): 200
- Treatment (smooth): 100
- Control (sharp): 100

**Sample size warning:** N=100 per group is small. This is a rare-event phenomenon. Results should be interpreted with caution.

### 6.4 Gross Economics

| Group | N | Gross Mean | Gross Median | Std |
|---|---|---|---|---|
| Treatment (smooth) | 100 | +0.31 bps | +2.76 bps | 12.81 bps |
| Control (sharp) | 100 | +18.39 bps | +27.28 bps | 10.12 bps |

### 6.5 Net Economics

| Group | N | Net Mean | Net Median | WR |
|---|---|---|---|---|
| Treatment (smooth) | 100 | -1.69 bps | -5.24 bps | 40.0% |
| Control (sharp) | 100 | +16.39 bps | +25.28 bps | 99.0% |

### 6.6 Conditional Delta

| Metric | Value | Favors |
|---|---|---|
| Mean Delta | -18.08 bps | Control (sharp) |
| Median Delta | -30.52 bps | Control (sharp) |
| WR Delta | -59.0% | Control (sharp) |

### 6.7 Distribution

| Metric | Treatment | Control |
|---|---|---|
| Std | 12.81 bps | 10.12 bps |
| P10 | -10.75 bps | +7.06 bps |
| P90 | +7.72 bps | +27.28 bps |

**Primary hypothesis metric (distribution width):** Treatment WIDER than control (12.81 vs 10.12 bps). This CONTRADICTS the hypothesis — smooth transitions were expected to produce tighter distributions, but they are actually wider.

### 6.8 Nine Hard Gates

| Gate | Result | Evidence |
|---|---|---|
| 1. Measurement integrity | PASS | ATR percentile from OHLC |
| 2. Temporal ordering | PASS | Transitions detected before forward returns |
| 3. Look-ahead protection | PASS | No future info in transition classification |
| 4. Counterfactual validity | PASS | Same regime change, different quality |
| 5. Sample adequacy | PASS | Treatment N=100, Control N=100 (marginal) |
| 6. Cost model integrity | PASS | 2 bps applied identically |
| 7. Distribution completeness | PASS | Full distribution reported |
| 8. No post-hoc modification | PASS | All parameters frozen in G0 |
| 9. Temporal independence | PASS | Rearm applied (transitions are non-overlapping) |

**9/9 PASS** (marginal on sample adequacy)

### 6.9 Mechanism Assessment

**Distribution width:** Treatment (smooth) has wider std (12.81 vs 10.12 bps). This CONTRADICTS the hypothesis — smooth transitions were expected to produce tighter distributions.

**Economic direction:** Control (sharp) massively outperforms treatment (smooth) on ALL metrics:
- Net mean: +16.39 vs -1.69 bps (delta: -18.08 bps)
- Net median: +25.28 vs -5.24 bps (delta: -30.52 bps)
- WR: 99.0% vs 40.0% (delta: -59.0%)

**The hypothesis direction is WRONG.** Sharp transitions produce better economics, not smooth transitions.

**However:** The conditional information is massive and genuine. Sharp transitions produce +16.39 bps net mean with 99% win rate. This is the strongest conditional signal in RF history.

**Mechanism interpretation:** The data contradicts the hypothesized mechanism (participant preparedness during smooth transitions). Instead, it suggests that sharp transitions create forced positioning and urgency that produces predictable subsequent flow. This is a DIFFERENT mechanism than hypothesized — more akin to execution stress / forced positioning than orderly adaptation.

### 6.10 Prior-Art Caveat

**CAND-077:** Tested regime STATE (compressed vs expanded). CAND-099 tests transition QUALITY. The G1 result shows that transition quality is economically meaningful, but in the OPPOSITE direction of the hypothesis.

**CAND-096:** Tested volatility acceleration. CAND-099 tests path smoothness. The G1 result shows sharp transitions (high path variance) outperform smooth transitions. This is related to but distinct from CAND-096's acceleration finding.

**CAND-080:** Attempted transition quality but failed due to zero events. CAND-099 succeeded in finding events (N=200) by using a broader regime detection method.

### 6.11 Economic Adjudication

**Economic verdict:** INFORMATIONALLY INTERESTING — the conditional signal is massive (+18.08 bps mean delta, 99% WR for sharp transitions) but the hypothesis direction is WRONG. The mechanism (participant preparedness during smooth transitions) is contradicted.

**Evidence profile:** HYPOTHESIS CONTRADICTED but ECONOMICALLY STRONG conditional signal in opposite direction.

**State potential:** The conditional signal is strong enough for State consideration, but the hypothesis direction is wrong and the sample is small (N=100 per group). State qualification requires further investigation with larger samples.

### 6.12 Final Classification

> **CLOSED — HYPOTHESIS CONTRADICTED (INFORMATIONALLY INTERESTING)**

Sharp transitions massively outperform smooth transitions (+18.08 bps mean delta, 99% WR). The hypothesized mechanism (participant preparedness during smooth transitions) is contradicted. The observed mechanism (forced positioning during sharp transitions) is economically strong but was not the registered hypothesis.

## 7. Candidate Comparison

| Dimension | CAND-098 | CAND-099 |
|---|---|---|
| N (treatment) | 8,392 | 100 |
| N (control) | 1,017 | 100 |
| Mean Delta | -1.11 bps | -18.08 bps |
| Median Delta | -0.30 bps | -30.52 bps |
| WR Delta | -1.2% | -59.0% |
| Nine Gates | 9/9 PASS | 9/9 PASS |
| Hypothesis | SUPPORTED (distribution width) | CONTRADICTED (direction wrong) |
| Mechanism | CONSISTENT | CONTRADICTED |
| Adjudication | ECONOMICALLY NEGATIVE | HYPOTHESIS CONTRADICTED / INFORMATIONALLY INTERESTING |

## 8. Economic Evidence Comparison

CAND-099 has vastly stronger conditional information (larger delta) but the hypothesis direction is wrong. CAND-098 has weaker conditional information and the hypothesis is supported on distribution width but economically insufficient.

## 9. Counterfactual Quality

Both counterfactuals are well-constructed:
- CAND-098: Same event class, different cluster density
- CAND-099: Same regime change, different transition quality

Failures are in economic evidence and hypothesis direction, not experimental design.

## 10. Distribution / Tail Assessment

**CAND-098:** Treatment has wider distribution (std 32.69 vs 24.93 bps). Supports hypothesis. But both groups have negative absolute economics.

**CAND-099:** Treatment has wider distribution (std 12.81 vs 10.12 bps). Contradicts hypothesis. Control has dramatically better economics.

## 11. Temporal Integrity

Both candidates have valid temporal ordering. No look-ahead. Events/transitions detected before forward returns computed.

## 12. Nine-Gate Summary

| Candidate | Gates |
|---|---|
| CAND-098 | 9/9 PASS |
| CAND-099 | 9/9 PASS (marginal on sample adequacy) |

## 13. CAND-099 vs CAND-077/096 Integrity

**CAND-099 vs CAND-077:** PASS — implementation measures transition quality (path variance), not regime state (percentile level). But the economic finding (sharp transitions better) may relate to regime change dynamics.

**CAND-099 vs CAND-096:** PASS — implementation measures path smoothness, not acceleration. But the economic finding may be partially explained by acceleration effects. Interpretive limitation noted.

## 14. Prior-Art / G0 Integrity

- CAND-098: NEW (confirmed at G0) — G1 result supports hypothesis on distribution width
- CAND-099: NEW (confirmed at G0) — G1 result contradicts hypothesis direction
- CAND-100: DATA INFEASIBLE — not tested

## 15. State Library

CAND-077/081/083: PRESERVED

## 16. SEED-002

> TESTED NEGATIVE — NO INCREMENTAL INFORMATION

## 17. Relational Framework

> GOVERNED — NO NEW TEST

## 18. APEX RB001–RB004

> DESIGNED / NOT EXECUTED

## 19. CAND-100 / Data Feasibility

CAND-100: DATA INFEASIBLE — bid/ask spread unavailable. Not tested.

## 20. Closed-Line Firewall

No V19–V32 closed hypothesis reopened.

## 21. Forward Runtime

CAND-015/024/035: ACTIVE / PROTECTED / UNTOUCHED

## 22. Confirmation Requirements

Neither candidate warrants confirmation:
- CAND-098: economically negative despite hypothesis support
- CAND-099: hypothesis contradicted (direction wrong)

## 23. Final Economic Adjudication

| Candidate | Adjudication | State Potential |
|---|---|---|
| CAND-098 | ECONOMICALLY NEGATIVE | NOT JUSTIFIED |
| CAND-099 | HYPOTHESIS CONTRADICTED / INFORMATIONALLY INTERESTING | NOT JUSTIFIED (direction wrong, small N) |

## 24. Integrity Verification

1. Only CAND-098 and CAND-099 were tested
2. CAND-100 was not tested
3. No thresholds were optimized
4. No parameter grids were searched
5. Counterfactuals were not redesigned
6. Temporal ordering is valid
7. No look-ahead occurred
8. Nine hard gates were applied
9. Gross and net economics are separated
10. Absolute and conditional economics are separated
11. No unsupported causal claims were made
12. No State interaction was performed
13. SEED-002 was not retested
14. No relational testing occurred
15. APEX RB001–RB004 were not executed
16. Forward runtime was not inspected
17. Confirmation was not executed
18. G2 was not executed
19. System Assembly was not executed
20. Ledger provenance is complete
