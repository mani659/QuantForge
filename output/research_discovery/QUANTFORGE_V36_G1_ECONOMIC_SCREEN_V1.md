# QUANTFORGE — V36 G1 ECONOMIC PLAUSIBILITY SCREEN

## CAND-105 + CAND-106

**Date:** 2026-09-02
**Status:** COMPLETE — BOTH CANDIDATES CLOSED
**Market:** USATECHIDXUSD M1 (outcome); XAUUSD M1 + USATECHIDXUSD M1 (CAND-105 state inputs)
**Data range:** 2023-09-01 to 2026-04-10 (aligned overlap)
**Cost assumption:** 2 bps round-trip friction

---

## 1. Mission

Execute the authorized V36 G1 Economic Plausibility Screen for CAND-105 (Cross-Asset Lead-Lag Asymmetry) and CAND-106 (Intra-Bar Price Distribution Quality). V36 is the first QuantForge research cycle deliberately outside the V19–V35 single-asset structural-OHLC search pattern. This screen determines whether the two new information dimensions contain economically meaningful conditional information.

---

## 2. Authoritative Inputs

- V36 G0: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V36.md`
- V36 G0 Integrity Audit: `output/research_discovery/QUANTFORGE_V36_G0_INTEGRITY_AUDIT_V1.md`
- G1 V3 Framework: `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md`
- G0 Process Refinement: `output/research_discovery/QUANTFORGE_G0_MECHANISM_OBSERVABLE_CHALLENGE_V1.md`
- Candidate ledger: `research/knowledge/unified_ledger/QUANTFORGE_RESEARCH_CANDIDATE_LEDGER_V1.csv`

**Scope note:** V36 G0 produced three candidates (CAND-105/106/107). Per the V36 G0 integrity audit disposition recorded in SESSION_HANDOFF Section 44, CAND-107 is REDUNDANT with existing volatility-regime research and is NOT tested in this screen. Only CAND-105 and CAND-106 are authorized.

---

## 3. Frozen Candidate Definitions

### CAND-105 — Cross-Asset Lead-Lag Asymmetry

- **Expression class:** STATE / CONDITION
- **Mechanism family:** Cross-Asset Information Flow
- **Research question:** Does the direction of cross-asset information flow (which asset's return precedes the other's) condition subsequent economics of USATECHIDXUSD?
- **Registered observable (G0):** Rolling correlation of returns between XAUUSD and USATECHIDXUSD over a defined window, including the DIRECTION of lead (which asset's returns precede the other).
- **Audit caveat (G0 integrity audit):** The G0 audit explicitly flagged that a plain rolling correlation measures co-movement, not directional lead/lag, and required G1 to implement temporal lead/lag structure. G1 implements a genuine directional lead measure (below) rather than same-bar correlation.
- **Frozen parameters:** lag = 1 aligned minute; trailing window = 240 aligned minutes; regime split = terciles of lead_asym (top tercile = gold-lead, bottom tercile = tech-lead, middle excluded); outcome horizon = 60 tech M1 bars; rearm = 60 bars; friction = 2 bps.
- **Treatment:** GOLD-LEAD regime — gold's prior-minute return is more strongly associated with tech's subsequent-minute return than the reverse.
- **Control:** TECH-LEAD regime — tech's prior-minute return is more strongly associated with gold's subsequent-minute return than the reverse.

### CAND-106 — Intra-Bar Price Distribution Quality

- **Expression class:** STATE / CONDITION
- **Mechanism family:** Bar-Internal Structure
- **Research question:** Does the internal structure of a completed M1 bar — where open and close fall within the bar's high-low range — condition subsequent economics of USATECHIDXUSD?
- **Registered observable (G0):** Open/close position ratios within the completed high-low range; bar symmetry. G1 freezes the bar-symmetry scalar: **body fraction = |close − open| / (high − low) ∈ [0,1]**.
  - Body fraction near 1 ⇒ open near one extreme and close near the other (full-range directional body = conviction).
  - Body fraction near 0 ⇒ close near open (indecision / doji character).
- **Frozen parameters (fixed structural thresholds, predeclared):** treatment = body fraction ≥ 0.70 (high conviction); control = body fraction ≤ 0.30 (indecision); middle band excluded; outcome horizon = 60 tech M1 bars; rearm = 60 bars; friction = 2 bps.
- **OHLC limit:** the observable is an OHLC-derived PROXY for within-bar distribution. It does not observe order flow, bid/ask sequence, depth, aggressor side, or the exact intra-bar path.

---

## 4. Dataset Identity

- **Outcome instrument:** USATECHIDXUSD M1 — 906,815 bars, 2023-09-01 to 2026-07-10.
- **State input instrument (CAND-105):** XAUUSD M1 — 1,768,123 bars, 2021-04-12 to 2026-04-10.
- **Aligned overlap (CAND-105):** exact-timestamp inner join of completed 1-minute returns — **827,517 aligned bars**, 2023-09-01 to 2026-04-10 20:14. Contiguous 1-minute-aligned runs: **899**.
- **Data files:** `data/m1/USATECHIDXUSD_M1.csv`, `data/m1/XAUUSD_M1.csv`.
- **Volume:** 0 / unavailable for both instruments. No volume-based claim is made.
- **Script:** `research/v36_g1_experiment.py`
- **Environment:** Python 3.11, pandas, numpy.

---

## 5. Nine Hard Validity Gates

### CAND-105

| Gate | PASS/FAIL | Evidence |
|---|---|---|
| 1. Deterministic definition | PASS | lead_asym = rolling(240) corr difference at frozen lag 1, fully deterministic from OHLC + timestamps |
| 2. Executable entry | PASS | Signal forms at the close of the aligned signal bar; all inputs ≤ signal-bar close |
| 3. No hindsight contamination | PASS | No post-entry signal definition; outcome window begins after signal is knowable |
| 4. Correct cost normalization | PASS | 2 bps friction applied uniformly in bps on the outcome instrument |
| 5. Data integrity | PASS | Both instruments present, exact-timestamp aligned, 1-minute-return construction verified (827,517 aligned bars) |
| 6. Legitimate counterfactual | PASS | Treatment (gold-lead) vs control (tech-lead) isolate DIRECTION of the same lead-lag observable — not random bars |
| 7. Causal claims limited to observables | PASS | Claims stated in observable price/timing terms; mechanism treated as hypothesis |
| 8. No future-bar dependency | PASS | Pairs (gold[s], tech[s+1]) with s+1 ≤ signal bar; outcome begins after signal close |
| 9. Reproducible | PASS | Deterministic from the two OHLC files and frozen parameters |

### CAND-106

| Gate | PASS/FAIL | Evidence |
|---|---|---|
| 1. Deterministic definition | PASS | body fraction = \|C−O\|/(H−L), deterministic from OHLC |
| 2. Executable entry | PASS | Body fraction known only at bar close; outcome begins after |
| 3. No hindsight contamination | PASS | No post-entry signal definition |
| 4. Correct cost normalization | PASS | 2 bps applied uniformly in bps |
| 5. Data integrity | PASS | M1 OHLC sufficient; zero-range bars excluded deterministically |
| 6. Legitimate counterfactual | PASS | High-conviction (body ≥ 0.7) vs indecision (body ≤ 0.3) bars isolate intra-bar distribution structure |
| 7. Causal claims limited to observables | PASS | "Conviction" explicitly labeled an OHLC-derived proxy, not observed behaviour |
| 8. No future-bar dependency | PASS | Uses only the completed signal bar |
| 9. Reproducible | PASS | Deterministic from OHLC + fixed thresholds |

**All 9 hard gates PASS for both candidates.** No validity failure; any shortfall is economic, not measurement.

---

## 6. CAND-105 Semantic Verification

### Registered vs Implemented

| Element | G0 definition | G1 implementation | Match |
|---|---|---|---|
| Cross-asset observable | Rolling correlation of returns, XAUUSD + USATECHIDXUSD | Rolling directional cross-lag correlation of 1-min returns | YES |
| Direction of lead | Which asset's returns precede the other | lead_asym = corr(gold[s], tech[s+1]) − corr(tech[s], gold[s+1]) over trailing window | YES |
| Temporal information flow | A moves first → B responds later | Frozen lag 1 aligned minute: gold move at s vs tech move at s+1 (and reverse) | YES |
| Co-movement vs lead | MUST NOT silently become same-bar correlation | lead_asym is a DIFFERENCE of one-minute-offset correlations; lag-0 corr reported only as reference | PASS |

**Semantic integrity: PASS.** The implementation measures directional temporal lead asymmetry in M1 returns, NOT contemporaneous co-movement, NOT simple direction agreement, NOT a common risk state.

---

## 7. CAND-105 Synchronization / Timing Verification

### Synchronization methodology (documented exactly)

1. Each asset's close-to-close log return is computed ONLY between consecutive bars of that asset exactly 1 minute apart; all other returns are set NaN (daily/weekend maintenance gaps never become pseudo-returns).
2. The two return series are inner-joined on exact timestamps (deterministic; duplicated timestamps impossible after sort; missing bars drop the row).
3. Rows are grouped into **contiguous aligned runs** where consecutive timestamps differ by exactly 1 minute, guaranteeing that lag-1 alignment means the same economic clock offset throughout the window.
4. lead_asym at signal bar t uses only pairs (gold[s], tech[s+1]) with s+1 ≤ t — no future bar enters the state.
5. Outcome is measured on the TECH series positionally (60 tech M1 bars after the signal-bar close), not on the merged subset, so outcome horizon is exactly 60 tech minutes.

**Verification results:** aligned bars = 827,517 (vs the audit's reported 569,378 overlapping bars; the audit figure appears to have used a stricter filter — this screen verifies 827,517 exact-timestamp-aligned 1-min-return bars independently). Contiguous runs = 899. lead_asym percentiles: P10 −0.129, P50 −0.003, P90 +0.130 — a centred, roughly symmetric state distribution.

**Residual timing caveat (documented, not corrected):** identical broker minute stamps do not prove identical economic timing within the minute. Lag 1 minute is the finest alignment the data supports and is the only frozen lag tested. No lag is selected from outcomes.

---

## 8. CAND-105 Sample Construction

- Aligned M1 bars (both assets, completed 1-min returns): 827,517
- Bars with fully computable lead_asym AND forward window: **643,416**
- Tercile boundaries (predeclared 1/3–2/3 split of the lead_asym distribution): lo = −0.0455, hi = +0.0415
- Raw treatment (gold-lead, top tercile): 214,472
- Raw control (tech-lead, bottom tercile): 214,472
- After rearm (60-bar minimum separation): **treatment N = 5,236; control N = 5,263**

**Independence:** rearm spacing equals the outcome horizon, so sampled outcome windows do not overlap. Regime labels derive from 240-minute windows; consecutive labels are autocorrelated, but rearmed sampling prevents pseudo-replication of outcomes.

---

## 9. CAND-105 Counterfactual

- **Treatment:** signal bars in the gold-lead regime (lead_asym > 41.5th-percentile boundary).
- **Control:** signal bars in the tech-lead regime (lead_asym < −45.5th-percentile boundary).
- The two groups are the two ends of the SAME directional-lead observable, so the comparison isolates the direction of temporal information flow.
- **Major alternative explanations (interpretation limitations, no post-hoc filters introduced):** common macro/dollar shocks; session overlap; one asset's greater volatility; simultaneous news reaction; beta/correlation state; estimation noise in 240-minute correlations.

---

## 10. CAND-105 Economic Results

| Metric | Treatment (Gold-Lead) | Control (Tech-Lead) | Delta |
|---|---:|---:|---:|
| N (after rearm) | 5,236 | 5,263 | — |
| Gross Mean | +0.33 bps | −0.01 bps | +0.35 bps |
| Gross Median | +0.89 bps | +0.53 bps | +0.35 bps |
| Net Mean | −1.67 bps | −2.01 bps | +0.35 bps |
| Net Median | −1.11 bps | −1.47 bps | +0.35 bps |
| Win Rate (gross > 0) | 52.8% | 51.8% | +1.1% |
| Win Rate (net > 0) | 46.5% | 46.0% | +0.5% |
| Std Dev | 29.32 bps | 28.92 bps | +0.40 bps |
| P10 / P90 | −25.4 / +25.4 bps | −25.5 / +25.5 bps | ≈ 0 |
| Contemporaneous (lag-0) corr reference | 0.118 | 0.123 | −0.004 |

Welch t-statistic (descriptive): **0.61** — not statistically distinguishable from zero.

**Interpretation:**
- Mean delta is +0.35 bps — far below any economically meaningful conditional separation and below every conditional delta that previously reached STATE REVIEW ELIGIBLE status (CAND-077 +1.67, CAND-081 +1.23, CAND-083 +4.60 bps).
- Median delta +0.35 bps and WR delta +1.1% are small and directionally consistent but statistically indistinguishable from zero (t = 0.61).
- The lag-0 co-movement level is nearly identical across regimes (0.118 vs 0.123), confirming the lead regime is not simply a proxy for contemporaneous correlation.
- Both groups' net means are clearly negative (−1.67 / −2.01 bps), i.e. even if the small directional delta were real, it does not survive friction as standalone economics.

---

## 11. CAND-105 Mechanism Interpretation

**What the experiment actually demonstrated:** Over the tested conditions, gold-lead and tech-lead M1 regimes of USATECHIDXUSD/XAUUSD produce essentially indistinguishable downstream economics for tech. The +0.35 bps delta is small, statistically insignificant (t = 0.61), and far below the scale of conditional information previously retained for State review.

**What the result implies about the mechanism:** The hypothesis that directional cross-asset lead structure carries economically meaningful conditional information is NOT supported by the measured M1 lead/lag asymmetry at 1-minute lag / 240-minute window. This does NOT prove lead-lag relationships do not exist in markets generally; it establishes that the registered observable, as implemented, produced no useful economic separation under the tested conditions.

**Alternative explanations not excluded (limitations, not post-hoc fixes):** common factor exposure and estimation noise may dominate any true lead signal at M1; identical broker clocks do not guarantee identical economic timing within the minute.

---

## 12. CAND-105 Adjudication

### Evidence Profile

- Mean delta: +0.35 bps (small)
- Median delta: +0.35 bps (small)
- WR delta: +1.1% (small)
- t-statistic: 0.61 (not significant)
- Net means: both groups negative (−1.67 / −2.01 bps)
- Co-movement level across regimes: near-identical (0.118 / 0.123)
- Comparison against State-review precedents: +0.35 bps is ~5x smaller than CAND-077 (+1.67) and ~13x smaller than CAND-083 (+4.60)

### Classification

> **CLOSED — ECONOMICALLY NEGATIVE**

**Rationale:** No economically meaningful conditional separation demonstrated. All deltas are small and statistically insignificant. No State potential is justified. No qualification path is opened.

---

## 13. CAND-106 Semantic Verification

### Registered vs Implemented

| Element | G0 definition | G1 implementation | Match |
|---|---|---|---|
| Observable | Open/close position ratios; bar symmetry within completed range | body fraction = \|close−open\|/(high−low) — the bar-symmetry scalar of the registered set | YES |
| Intra-bar level | WITHIN-bar distribution, not candle colour / range / ATR | body fraction is range-normalised (volatility-level independent) | YES |
| Treatment | Extreme open/close positions (conviction) | body fraction ≥ 0.70 (full-range directional body) | YES |
| Control | Middle/indecision bars | body fraction ≤ 0.30 (doji / close-near-open) | YES |
| Direction | Intra-bar structure ≠ bar direction | body fraction uses |close−open| (sign-free) | YES |

**Semantic integrity: PASS.** The implementation tests the registered intra-bar distribution observable, not candle colour, return magnitude, ATR, or a composite pattern classifier.

---

## 14. CAND-106 OHLC-Information Limitations

Completed OHLC does NOT reveal:
- the actual sequence of transactions inside the bar,
- order flow, bid/ask sequence, depth, or aggressor side,
- the exact intra-bar path.

Therefore "conviction" is an **OHLC-derived proxy** for within-bar distribution quality (open at one extreme + close at the other vs close near open). All mechanism language is conditioned on this proxy limitation. No claim of direct observation of participant behaviour is made.

---

## 15. CAND-106 Sample Construction

- Total M1 bars: 906,815
- Bars with computable body fraction AND forward window: 906,687
- body_frac percentiles: P10 = 0.106, P50 = 0.489, P90 = 0.852
- Raw treatment (body ≥ 0.70): 233,854
- Raw control (body ≤ 0.30): 265,144
- After rearm (60-bar separation): **treatment N = 14,412; control N = 14,529**

Zero-range bars (high == low) excluded deterministically (body fraction undefined). Rearm spacing equals outcome horizon, preventing overlapping outcome windows (no pseudo-replication).

---

## 16. CAND-106 Counterfactual

- **Treatment:** completed M1 bars with body fraction ≥ 0.70 (high conviction).
- **Control:** completed M1 bars with body fraction ≤ 0.30 (indecision).
- Both groups are ordinary completed M1 bars of the SAME instrument differing only in intra-bar body/range structure; outcome convention (long drift over 60 bars, net of 2 bps) is identical for both.
- Alternative explanations (volatility level, session timing, trend state, direction) are interpretation limitations. Direction decomposition is reported below as a diagnostic; no post-hoc filters were introduced.

---

## 17. CAND-106 Economic Results

| Metric | Treatment (Conviction ≥ 0.70) | Control (Indecision ≤ 0.30) | Delta |
|---|---:|---:|---:|
| N (after rearm) | 14,412 | 14,529 | — |
| Gross Mean | +0.49 bps | +0.49 bps | −0.01 bps |
| Gross Median | +0.91 bps | +0.84 bps | +0.07 bps |
| Net Mean | −1.51 bps | −1.51 bps | −0.01 bps |
| Net Median | −1.09 bps | −1.16 bps | +0.07 bps |
| Win Rate (gross > 0) | 53.2% | 53.0% | +0.2% |
| Win Rate (net > 0) | 45.9% | 46.2% | −0.3% |
| Std Dev | 28.78 bps | 28.78 bps | 0.00 bps |
| P10 / P90 | −23.0 / +23.9 bps | −23.3 / +23.8 bps | ≈ 0 |

Welch t-statistic (descriptive): **−0.02** — economically and statistically zero.

### Direction Decomposition (diagnostic only)

| Group | UP bars | DOWN bars |
|---|---|---|
| Treatment | N=7,397, mean +0.55 bps | N=7,015, mean +0.41 bps |
| Control | N=7,289, mean +0.47 bps | N=7,240, mean +0.51 bps |

No meaningful direction asymmetry inside either group; the near-zero delta is not masking a direction effect.

**Interpretation:** High-conviction and indecision bars are followed by **identical** downstream economics (mean delta −0.01 bps, t = −0.02). The intra-bar conviction observable carries no incremental economic information under the tested conditions. The result is also NOT explained by ordinary bar direction (direction decomposition shows flat UP/DOWN differences in both groups).

---

## 18. CAND-106 Mechanism Interpretation

**What the experiment actually demonstrated:** Within-bar body/range structure (conviction vs indecision) has no detectable association with subsequent 60-minute economics of USATECHIDXUSD. Mean delta is −0.01 bps with t = −0.02; outcome distributions are effectively identical (std 28.78 both groups).

**What the result implies about the mechanism:** The OHLC-proxy "conviction" construct — as registered and implemented — does not carry useful forward information. The result is consistent with two readings: (a) intra-bar structure genuinely lacks incremental information at M1 in this instrument, or (b) the OHLC proxy (body fraction) is too coarse to capture any real within-bar distribution signal. Both readings lead to the same economic conclusion: no exploitable conditional information was demonstrated.

**Relationship to bar direction / range:** Not confounded — the observable is range-normalised and sign-free, and direction decomposition confirms the flat result is not hiding direction effects.

---

## 19. CAND-106 Adjudication

### Evidence Profile

- Mean delta: −0.01 bps (essentially zero)
- Median delta: +0.07 bps (trivially positive)
- WR delta: +0.2% (negligible)
- t-statistic: −0.02 (not significant)
- Net means: identical (−1.51 / −1.51 bps)
- Direction decomposition: flat in both groups

### Classification

> **CLOSED — ECONOMICALLY NEGATIVE**

**Rationale:** High-conviction and indecision bars produce identical downstream economics. No conditional information, no State potential, no qualification path.

---

## 20. Cross-Candidate Interpretation

Both V36 candidates — the two surviving genuinely-new information dimensions from the first cross-asset / bar-internal research cycle — produced essentially zero economic separation:

- **CAND-105 (cross-asset lead-lag):** mean delta +0.35 bps, t = 0.61.
- **CAND-106 (intra-bar distribution):** mean delta −0.01 bps, t = −0.02.

V36 was methodologically successful as the first cycle outside the V19–V35 single-asset structural-OHLC search pattern: both candidates were genuinely novel, data-feasible, measurement-valid (9/9 gates), and produced clean null/negative economic evidence. The economic outcome is consistent with the factory base rate: **new information dimensions can be genuinely novel and still carry no exploitable conditional information.**

---

## 21. Limitations

1. **CAND-105:** 1-minute lag is the finest alignment supported; identical broker minute stamps do not guarantee identical economic timing within the minute. Common macro factor exposure may dominate any true lead signal. Only one (frozen, predeclared) lag/window combination was tested.
2. **CAND-105:** The audit figure of 569,378 overlapping bars differs from this screen's independently verified 827,517 exact-timestamp-aligned 1-min-return bars (filter definitions differ); conclusions are unaffected because both groups are drawn from the same aligned sample.
3. **CAND-106:** OHLC cannot observe true intra-bar transaction sequence; body fraction is a proxy. If real within-bar information exists, it may be unobservable at M1 OHLC granularity.
4. **CAND-106:** Fixed structural thresholds (0.70/0.30) were predeclared; alternative thresholds were not swept (by design).
5. **Single outcome instrument:** All outcomes measured on USATECHIDXUSD M1; results specific to this instrument/timeframe.
6. **Both candidates:** Economic conclusions are negative; neither absence of any market phenomenon nor absence of all possible variants is claimed.

---

## 22. Governance Disposition

| Candidate | N (T/C) | Hard Gates | Net Mean | Net Median | WR (gross) | Mean Delta | Final Classification |
|---|---|---|---|---|---|---|---|
| CAND-105 | 5,236 / 5,263 | 9/9 PASS | −1.67 / −2.01 bps | −1.11 / −1.47 bps | 52.8% / 51.8% | +0.35 bps | **CLOSED — ECONOMICALLY NEGATIVE** |
| CAND-106 | 14,412 / 14,529 | 9/9 PASS | −1.51 / −1.51 bps | −1.09 / −1.16 bps | 53.2% / 53.0% | −0.01 bps | **CLOSED — ECONOMICALLY NEGATIVE** |

### Governance Verification

- ✅ No optimization
- ✅ No post-hoc thresholding
- ✅ No lag sweeping (lag frozen at 1 minute before execution)
- ✅ No threshold mining (CAND-106 thresholds frozen at 0.70/0.30)
- ✅ No protected-runtime inspection
- ✅ No relational testing
- ✅ No APEX execution
- ✅ No closed candidate reopened (incl. CAND-107 remains REDUNDANT)
- ✅ No CAND-099 reuse
- ✅ No G2 execution
- ✅ Forward runtime untouched
- ✅ State library unchanged

### State Library

UNCHANGED: CAND-077/081/083 STATE REVIEW ELIGIBLE (preserved). No new State potential from V36.

---

## 23. Reproducibility

- **Outcome dataset:** USATECHIDXUSD M1 (`data/m1/USATECHIDXUSD_M1.csv`), 906,815 bars, 2023-09-01 to 2026-07-10
- **State dataset (CAND-105):** XAUUSD M1 (`data/m1/XAUUSD_M1.csv`), aligned overlap 827,517 bars (2023-09-01 to 2026-04-10)
- **Frozen parameters (CAND-105):** lag = 1 aligned min; window = 240 aligned min; tercile regime split; horizon = 60 tech bars; rearm = 60; friction = 2 bps
- **Frozen parameters (CAND-106):** body fraction thresholds ≥ 0.70 / ≤ 0.30; horizon = 60 bars; rearm = 60; friction = 2 bps
- **Synchronization (CAND-105):** exact-timestamp inner join of 1-minute-adjacent returns; contiguous aligned runs; outcome measured on the TECH series positionally
- **Cost model:** 2 bps round-trip, applied identically to treatment and control
- **Event definitions:** CAND-105 — lead regime of signal bar; CAND-106 — body fraction class of completed bar
- **Script:** `research/v36_g1_experiment.py`
- **Exclusions:** bars without completed 1-minute returns on both assets (CAND-105); zero-range bars and bars without forward window (CAND-106); boundary bars lacking full windows
- **Environment:** Python 3.11, pandas, numpy

---

*V36 G1 complete. Both candidates closed as ECONOMICALLY NEGATIVE. 0 G2 promotions. V36 permanently closed. CAND-107 remains REDUNDANT. State library unchanged. Forward runtime protected.*
