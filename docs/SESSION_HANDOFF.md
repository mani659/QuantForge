# QUANTFORGE — SESSION HANDOFF (AUTHORITATIVE)

**Purpose:** Authoritative restart point for the next QuantForge session. Do not reconstruct project history from conversational memory; start from this document and the referenced artifacts.

**Last consolidated:** 2026-09-01 (V33 G1 complete + G0 process refinement introduced)

**Today's commits (2026-08-31 — session summary):**
1. `615552a` — V26 G0 dynamic state transition discovery
2. `2faa099` — V26 G1 economic plausibility screen
3. `9323bb8` — V26 closure and dynamic-state knowledge
4. `d57bd1c` — CAND-077 state governance review
5. `7a8ee5f` — V27 G0 dynamic transition discovery
6. `a9c9625` — V27 G1 economic plausibility screen
7. `aa43691` — CAND-077 + CAND-081 state governance review
8. `8e87a01` — V28 G0 new discovery
9. `818d6d5` — V28 G1 economic plausibility screen
10. `9306767` — CAND-083 state governance review
11. `a705c32` — V29 G0 new discovery
12. `02f312e` — V29 G1 economic plausibility screen
13. `74933bb` — Relational research governance framework
14. `2ea4884` — Unified research knowledge ledger v1
15. `d372f11` — SEED-002 relational discovery
16. `52bd4a4` — Cross-research knowledge ledger integration
17. `5e15fd3` — Unified research history csv ledger
18. `502baed` — V30 G0 new discovery
19. `755f7d7` — V30 G0 integrity audit
20. `09ce762` — V30 G1 economic plausibility screen
21. `25cee70` — V30 G1 integrity audit
22. `923b822` — V31 G0 new discovery
23. `3b268de` — V31 G0 integrity audit
24. `75a3576` — V31 G1 economic plausibility screen
25. `7ce4049` — V31 G1 adjudication integrity audit
26. `bb3b940` — V32 G0 knowledge-gap discovery
27. `a4756c7` — V32 G0 integrity audit
28. `4a2cdce` — V32 G1 economic plausibility screen
29. `1a06b93` — session-close documentation reconciliation
30. `a77384d` — V33 G0 knowledge-gap discovery
31. `b7edfca` — V33 G0 integrity audit
32. `0a34f32` — V33 G1 economic plausibility screen
33. `3a53f40` — V33 G1 economic plausibility screen (final)
34. `pending` — G0 process refinement (Mechanism-Observable Challenge)

---

## 0. START HERE NEXT SESSION

> **READ THIS DOCUMENT. THEN READ ONLY THE REFERENCED ARTIFACTS NECESSARY FOR YOUR SPECIFIC TASK.**
>
> **DO NOT ASK THE OWNER TO REPEAT PROJECT HISTORY.**
>
> **DO NOT RECONSTRUCT STATE FROM CONVERSATIONAL MEMORY.**

### Required next-session reading

1. `docs/SESSION_HANDOFF.md` (this document)
2. `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md` (G1 V3 framework)
3. `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (candidate register)
4. `research/knowledge/RESEARCH_TIMELINE.md` (research timeline)

### Explicit prohibitions

Next session must NOT:

- Rescue CAND-086, CAND-087, CAND-088, CAND-089, CAND-090, CAND-091, CAND-092, CAND-093, CAND-094, CAND-095, CAND-096, CAND-097, or any closed V19–V32 candidate;
- Rescue CAND-084 (EXTENSION / REDUNDANT);
- Rescue CAND-085 (INSUFFICIENT);
- Generate V32 replacement for CAND-097 without owner authorization;
- Reopen V30, V31, or V32;
- Rerun G1 screens;
- Optimize CAND-077 filters;
- Inspect CAND-015/024/035 forward performance;
- Modify forward runner;
- Perform System Assembly;
- Treat exploratory filter observations as validated strategies;
- Execute relational testing without governance authorization;
- Execute APEX RB001–RB004 without authorization.

### Current milestone

> **V32: CLOSED / VERIFIED**
> **V31: CLOSED / VERIFIED**
> **V30: CLOSED / VERIFIED**
> **CAND-095: CLOSED — ECONOMICALLY NEGATIVE**
> **CAND-096: CLOSED — HYPOTHESIS CONTRADICTED (INFORMATIONALLY INTERESTING, STATE REVIEW ELIGIBLE — opposite direction)**
> **CAND-097: CLOSED — REDUNDANT WITH DISC-021**
> **3 STATE REVIEW ELIGIBLE objects: CAND-077, CAND-081, CAND-083 (PRESERVED)**
> **SEED-002: TESTED NEGATIVE — NO INCREMENTAL INFORMATION**
> **V32: 0 G2 promotions. 2 candidates tested, 2 closed. CAND-096 shows genuine conditional information in opposite direction.**
> **V33 G0: 3 NEW CANDIDATES — CAND-098 (Event-Cluster Response Degradation), CAND-099 (Volatility Regime Transition Quality), CAND-100 (Spread-Conditioned Execution Stress)**
> **V33 G0 INTEGRITY AUDIT: CAND-098 G1 ELIGIBLE, CAND-099 G1 ELIGIBLE, CAND-100 DATA INFEASIBLE (bid-ask spread unavailable)**
> **V33 G1: CAND-098 CLOSED — ECONOMICALLY NEGATIVE (hypothesis supported on distribution width but economically insufficient). CAND-099 CLOSED — HYPOTHESIS CONTRADICTED / INFORMATIONALLY INTERESTING (sharp transitions massively outperform smooth, opposite of hypothesized direction).**
> **G0 PROCESS REFINEMENT: Mechanism-Observable Challenge introduced (8 adversarial questions + proxy confidence). NOT a hard gate. Effective V34 G0 onward.**

Today's session (2026-09-01) completed: V33 G0 (3 candidates), V33 G0 integrity audit (CAND-100 DATA INFEASIBLE, 2 eligible), V33 G1 (CAND-098 ECONOMICALLY NEGATIVE, CAND-099 HYPOTHESIS CONTRADICTED / INFORMATIONALLY INTERESTING). V29–V33 Research Factory Meta-Audit completed. G0 process refinement introduced: Mechanism-Observable Challenge. V33 permanently closed.

---

## 1. PROJECT MISSION

QuantForge's overriding goal:

> Build a robust, defensible trading system capable of surviving live/demo conditions over months/years.

Research is valuable only when it has a governed path toward:

> TRADEABLE EDGE → VALIDATION → QUALIFICATION → FORWARD EVIDENCE → SYSTEM VALUE

The system may ultimately consist of one exceptional strategy or multiple independent specialized modules. Rare high-expectancy events remain legitimate.

---

## 2. CURRENT REPOSITORY STATE

- **HEAD:** `1a06b93` — `docs: close 2026-08-31 research session`
- **V32 G1 commit:** `4a2cdce` — `research: complete V32 G1 economic plausibility screen`
- **Branch:** `main` (linear history)
- **Uncommitted:** runtime/forward data (CAND-015 health, event ledgers), research scripts, scratch files — correctly excluded from governance commits
- **No source code, tests, or contracts modified by research tasks**

---

## 3. CURRENT GOVERNANCE

### G1 V3 Framework — RATIFIED

Effective: FUTURE RESEARCH ONLY (V25+)

Architecture:
- **Layer 1:** 9 binary hard validity gates (measurement integrity)
- **Layer 2:** Economic evidence adjudication (holistic, not scorecard)

Four artifact classes:
1. Standalone Alpha
2. Rare-Event Alpha
3. State/Condition
4. Regime/Specialist

Numeric thresholds are REFERENCE POINTS, not universal laws:
- 5 bps → reference
- 20 bps → reference
- 2 bps State delta → removed as universal rule
- N=3 → evidence-quality marker
- N=10 → evidence-quality marker

Economic adjudication classes:
1. ECONOMICALLY NEGATIVE
2. INFORMATIONALLY INTERESTING
3. ECONOMICALLY PROMISING
4. QUALIFICATION-WORTHY
5. RARE-EVENT QUALIFICATION-WORTHY

### Ratification artifacts

- `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md`
- `output/research_discovery/QUANTFORGE_G1_HARD_GATES_VS_EVIDENCE_ADJUDICATION_V1.md`
- `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_PROPOSAL.md`
- `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_CRITERIA_AUDIT_V1.md`

---

## 4. HISTORICAL RECLASSIFICATION AUDIT

68 historical candidates audited:
- 63 V3-compatible closures (93%)
- 3 potential State/Condition classification mismatches

State review pool (OWNER REVIEW REQUIRED — no interaction testing authorized):
- CAND-059: First Touch > Subsequent Touch — STATE-ARTIFACT
- CAND-065: Deep Sweep > Shallow Sweep — STATE OBSERVATION
- CAND-069: Mid-session > Morning — STATE OBSERVATION

Artifact: `output/research_discovery/QUANTFORGE_HISTORICAL_CANDIDATE_V3_RECLASSIFICATION_AUDIT_V1.md`

---

## 5. RESEARCH FACTORY HISTORY V19–V26

### V19–V24

18 candidates. 0 G2 promotions. Dominant pattern: conditionally informative but economically flat. Meta-review identified possible conditional-value bias and recommended greater emphasis on direct economic displacement.

Artifact: `output/research_discovery/QUANTFORGE_V24_CLOSURE_AND_FACTORY_META_REVIEW_V1.md`

### V25

Candidates: CAND-074 (London Gold Fix), CAND-075 (Closing Auction), CAND-076 (Gold→Tech Overnight)
Result: 0 G2 promotions. All three economically negative. Settlement/benchmark and simple cross-market directional formulations failed.

Lesson: Even theoretically compelling settlement/benchmark mechanisms did not produce measurable directional displacement in M1 data.

### V26

Candidates: CAND-077 (Vol Compression→Expansion), CAND-078 (Trend Exhaustion), CAND-079 (Gold Vol Transition→Tech)
Result: 0 G2 promotions. Two of three showed positive conditional deltas — first time in RF history.

Lesson: Dynamic state transitions produce more conditional information than static conditions. CAND-077 showed +1.67 bps delta (largest in RF history).

V26 closure: `output/research_discovery/QUANTFORGE_V26_CLOSURE_DYNAMIC_STATE_KNOWLEDGE_V1.md`

### V27

Candidates: CAND-080 (Vol Regime Quality Transition), CAND-081 (Structural Level Failure Trap), CAND-082 (Post-Expansion Retracement Quality State)
Result: 0 G2 promotions. CAND-081 shows +1.23 bps conditional delta (second-strongest in RF history).

- CAND-080: INSUFFICIENT (counterfactual failed — zero events)
- CAND-081: INFORMATIONALLY INTERESTING — STATE REVIEW ELIGIBLE (+1.23 bps delta)
- CAND-082: INFORMATIONALLY INTERESTING (outlier-dependent, State hypothesis contradicted)

V27 G0: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V27.md`
V27 G1: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V27.md`

---

## 6. CURRENT CANDIDATE REGISTER

### Active Forward (PROTECTED)

| Candidate | Status | Canonical |
|---|---|---|
| CAND-015 | ACTIVE / PROTECTED / EXTERNAL | adapter-based |
| CAND-024 | RARE-EVENT QUALIFICATION ACTIVE | `CAND-024:CANONICAL:925495a8` |
| CAND-035 | RARE-EVENT QUALIFICATION ACTIVE | `CAND-035:CANONICAL:ddc5d0e9` |

### State Library

| Candidate | Mechanism | Classification |
|---|---|---|
| CAND-059 | First Touch > Subsequent Touch | STATE-ARTIFACT |
| CAND-065 | Deep Sweep > Shallow Sweep | STATE OBSERVATION |
| CAND-069 | Mid-session > Morning | STATE OBSERVATION |
| **CAND-077** | **Vol compression → expansion** | **STATE REVIEW ELIGIBLE — OWNER REVIEW REQUIRED** |
| **CAND-081** | **Structural level failure trap** | **STATE REVIEW ELIGIBLE** |
| **CAND-083** | **Cumulative rejection pressure at structural level** | **STATE REVIEW ELIGIBLE — GOVERNANCE COMPLETE** |
| CAND-079 | Gold vol transition → Tech | STATE OBSERVATION |

### Registered Components

| Candidate | Status |
|---|---|
| CAND-042 | COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED |

---

## 7. CAND-077 — DETAILED STATUS

### Original V26 Frozen Hypothesis

> Compressed volatility → expanding volatility transition produces economically useful downstream behavior.

### G1 V3 Result

| Metric | Value |
|---|---|
| N | 2,084 |
| Frequency | ~700/year |
| Gross Mean | +1.15 bps |
| Gross Median | +0.86 bps |
| Net Mean | -0.85 bps |
| Net Median | -1.14 bps |
| Win Rate | 54.5% |
| Counterfactual N | 387 |
| Counterfactual Mean | -2.52 bps |
| Counterfactual Median | -1.90 bps |
| Conditional Delta | **+1.67 bps** (TREATMENT SUPERIOR) |
| Hard Validity Gates | ALL 9 PASS |
| Transition Integrity | PASS |

### Classification

> INFORMATIONALLY INTERESTING — STATE REVIEW ELIGIBLE — OWNER REVIEW REQUIRED

### Post-Closure Filter Observation (EXPLORATORY / NOT VALIDATED)

After V26 closure, an exploratory analysis examined whether selectivity filters could improve win rate. Results:

| Filter | N | Win Rate | Gross Mean | Gross Median |
|---|---|---|---|---|
| Baseline | 2,084 | 54.5% | +1.15 | +0.86 |
| Breakout > 2 bps | 1,454 | 54.7% | +1.42 | +1.07 |
| Breakout > 5 bps | 846 | 55.0% | +1.48 | +1.50 |
| Breakout > 10 bps | 415 | 57.8% | +2.74 | +3.30 |
| **Breakout > 15 bps** | **219** | **64.8%** | **+8.41** | **+6.97** |
| Breakout > 20 bps | 133 | 64.7% | +8.45 | +10.14 |

Estimated frequency at >15 bps: ~77 events/year.

**These are NOT validated filters.** Filter selected AFTER observing baseline outcome = selection bias.

### Time-of-Day Observations (EXPLORATORY)

- Hour 17: 69.8% WR, +10.93 bps (N=63)
- Hour 18: 70.6% WR, +14.19 bps (N=17, small sample)
- Hour 20: 72.0% WR, +7.16 bps (N=25)
- Hour 15: 64.9% WR, +3.11 bps (N=205)

### Day-of-Week Observations (EXPLORATORY)

- Tuesday: 62.2% WR, +3.96 bps (N=410)
- Monday: 57.7% WR, +2.24 bps (N=444)

### Critical Filter Governance

> FILTER DISCOVERY ≠ VALIDATED STRATEGY

The observed breakout-size relationship must not be treated as validation. If pursued, requires a separately governed future hypothesis with:
- Pre-registered threshold (BEFORE confirmatory test)
- Exact treatment definition
- Exact counterfactual
- No post-outcome selection
- Proper holdout/prospective testing

---

## 8. CAND-079 — DETAILED STATUS

### G1 V3 Result

| Metric | Value |
|---|---|
| N | 35,920 |
| Frequency | ~13,781/year |
| Net Mean | -1.79 bps |
| Net Median | -1.98 bps |
| Conditional Delta | +0.78 bps (TREATMENT SUPERIOR) |
| Validity | ALL 9 GATES PASS |
| Cross-Market Integrity | PASS |

### Classification

> STATE OBSERVATION (weak conditional delta)

### Post-Closure Filter (EXPLORATORY)

Gold UP + move >20 bps: 52.8% WR, +1.32 bps. Weak exploratory improvement. Not a qualified filter.

---

## 9. CAND-078

> CLOSED — ECONOMICALLY NEGATIVE / COUNTERFACTUAL INFERIORITY

Delta: -0.25 bps (counterfactual superior). No inverse hypothesis authorized.

---

## 10. EXTERNAL STATISTICAL RESEARCH PRIORS

A custom-bot statistical analysis (Aug 7–29, 2026) covering 40+ log files across three bots.

Classification: **PROVISIONAL EXTERNAL RESEARCH INPUT — NOT VALIDATED QUANTFORGE EVIDENCE**

Key observations retained as research priors:
1. Static regime labels may fail to reflect intraday behavior
2. Dynamic regime drift may be more informative
3. Volatility development may differ from already-expanded volatility
4. ADX appears potentially non-monotonic (extreme = possible exhaustion)
5. R-velocity after entry may provide trade-health information
6. Volume/spread/rollover conditions may define execution-quality states
7. Session × regime interactions may matter

No thresholds or bot rules were imported. All V26 definitions are independent.

---

## 11. FORWARD RUNTIME ARCHITECTURE

One unified manual launcher: `run_quantforge_forward.bat`
One Python runner: `quantforge_forward_supervisor.py`
One shared MT5 read-only connection
Independent observers: CAND-015, CAND-024, CAND-035

Forward environment:
- Logical: `USATECHIDXUSD`
- Broker: `Exness Technologies Ltd`
- Server: `Exness-MT5Trial15`
- Symbol: `USTECm`
- Mapping: `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`

Forward runtime: **ACTIVE / PROTECTED**

Do NOT:
- Inspect performance
- Stop/restart runner
- Change runner/launcher/contracts
- Inspect ledgers

---

## 12. CAND-015

> ACTIVE / PROTECTED / EXTERNAL

Adapter-based integration via `cand015_adapter.py`. External engine preserved (dictionary-based identity, pandas/ATR, process_tick). BTCUSD data buffered but not used in current signal evaluation. Cold start: accumulates M1 bars over time (30-day ATR warmup).

**Deferred UI note:** When next forward candidate is added, update CAND-015 status presentation to show State: WATCHING / Results: PROTECTED. Do NOT add false counter unless CAND-015's own protocol supports it.

---

## 13. CAND-024

> RARE-EVENT QUALIFICATION ACTIVE / PROTECTED

Canonical: `CAND-024:CANONICAL:925495a8`
Historical: ~+40.59 bps net/event, ~4.55/year
Current target: 5 events, minimum 3

---

## 14. CAND-035

> RARE-EVENT QUALIFICATION ACTIVE / PROTECTED

Canonical: `CAND-035:CANONICAL:ddc5d0e9`
Historical: ~+62.36 bps net/event, ~4.09/year
Current target: 5 events, minimum 3

---

## 15. CLOSED RESEARCH LINES

All permanently closed:
- V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, V29, V30, V31, V32
- CAND-071 through CAND-079 (except CAND-077 STATE REVIEW ELIGIBLE)
- CAND-087 through CAND-097 (all closed — various reasons)
- DISC-021 through DISC-028
- Mean Reversion line (DISC-021)
- TSMOM 12/1 line (DISC-022)
- H01 Equity Track A (DISC-023)

No automatic reopening permitted.

---

## 16. RESCUE FIREWALL

> NEW FRAMEWORK ≠ RETROACTIVE RESCUE
> FILTER OBSERVATION ≠ VALIDATED CANDIDATE
> CONDITIONAL INFORMATION ≠ QUALIFIED STATE
> POSITIVE WIN RATE ≠ PROFITABLE STRATEGY
> POSITIVE MEAN ≠ ROBUST ECONOMIC EDGE
> LARGE N ≠ ECONOMIC VALUE
> SMALL N + LARGE RETURN ≠ PROOF

---

## 17. SYSTEM ASSEMBLY

> NOT EXECUTED

No system assembly may occur merely because several useful artifacts exist.

---

## 18. STATE GOVERNANCE REVIEWS (COMPLETE)

### CAND-077 + CAND-081 Review Result

> BOTH STATE REVIEW ELIGIBLE — PRESERVED
> V28 G0 READY

### CAND-083 Review Result

> STATE REVIEW ELIGIBLE — PRESERVED
> V29 G0 READY

### CAND-077

> STATE REVIEW ELIGIBLE — PRESERVED

**State concept:** A transition in volatility character from compressed/smooth to expanded/active creates a specific market condition that may modify the economics of downstream events.

**Evidence:** N=2,084, +1.67 bps conditional delta (largest in RF history), all 9 validity gates pass.

**Exploratory findings:** Breakout magnitude relationship (>15 bps = 64.8% WR, +8.41 bps) remains EXPLORATORY EVIDENCE ONLY. No numerical threshold ratified.

**Future path:** Formal State hypothesis registration → qualified downstream Alpha → interaction study → State qualification.

### CAND-081

> STATE REVIEW ELIGIBLE — PRESERVED

**State concept:** The presence of a trapped participant population following a failed structural break creates a specific market condition that may modify the economics of subsequent events.

**Evidence:** N=3,887, +1.23 bps conditional delta (second-strongest in RF history), all 9 validity gates pass, counterfactual valid and discriminating (3,364 events).

**Absolute economics:** Net mean=-0.78 bps. NOT a standalone Alpha.

**Future path:** Formal State hypothesis registration → qualified downstream Alpha → interaction study → State qualification.

### Independence

The two mechanisms are genuinely independent:
- Different observables (ATR percentile vs price level)
- Different participant populations (trend followers vs breakout traders)
- Different timeframes (regime-level vs event-level)
- Can coexist in the same market

### Critical Governance Rules

> NO NUMERICAL FILTER THRESHOLD IS RATIFIED.
> CAND-077 and CAND-081 are NOT standalone Alphas.
> Both require formally frozen State hypotheses before qualification.
> CAND-024/CAND-035 must NOT be retroactively designated as downstream Alphas.

### Artifact

`output/research_discovery/QUANTFORGE_CAND077_CAND081_STATE_GOVERNANCE_REVIEW_V1.md`

---

### CAND-083 Governance Review Result

> STATE REVIEW ELIGIBLE — PRESERVED
> DISTINCT STATE CONCEPT FROM CAND-077 AND CAND-081
> V29 G0 READY

**State concept:** Repeated unsuccessful attempts to establish price acceptance at a structural area may progressively increase the population of participants whose positions become vulnerable to forced exit, creating a distinct market condition when the structure ultimately fails.

**G1 Evidence:** N=2,318, +4.60 bps conditional delta (largest in RF history), all 9 validity gates pass, counterfactual valid and discriminating (N=316).

**Absolute economics:** Net mean=-2.33 bps. NOT a standalone Alpha.

**Independence from CAND-077:** INDEPENDENT. Different observables (rejection count vs ATR percentile). Different participant populations (rejected breakout participants vs trend followers in compressed state).

**Independence from CAND-081:** INDEPENDENT BUT POTENTIALLY RELATED. CAND-083 captures pre-failure accumulation; CAND-081 captures post-failure trapped state. Different temporal phases of structural failure.

**Threshold governance:** NO NUMERICAL REJECTION-COUNT THRESHOLD IS RATIFIED.

**Future path:** Formal State hypothesis registration → qualified downstream Alpha → interaction study → State qualification.

**Artifact:** `output/research_discovery/QUANTFORGE_CAND083_STATE_GOVERNANCE_REVIEW_V1.md`

---

## 19. PERMITTED NEXT TASKS

- **V34 G0 — NEW DISCOVERY under refined G0 process (if owner authorizes)**
- Formal State hypothesis registration for CAND-077 (if owner authorizes)
- Formal State hypothesis registration for CAND-081 (if owner authorizes)
- Formal State hypothesis registration for CAND-083 (if owner authorizes)
- Formal State hypothesis registration for CAND-077 (if owner authorizes)
- Formal State hypothesis registration for CAND-081 (if owner authorizes)
- Formal State hypothesis registration for CAND-083 (if owner authorizes)
- Relational research governance question resolution (if owner authorizes)
- CAND-024/CAND-035 forward observation (continue, do not inspect)
- CAND-015 forward observation (continue, do not inspect)

---

## 20. FORBIDDEN NEXT TASKS

- Rescue CAND-086, CAND-087, CAND-088, CAND-089, CAND-090, CAND-091, CAND-092, CAND-093, CAND-094, CAND-095, CAND-096, CAND-097, or any closed V19–V32 candidate
- Rescue CAND-084 (EXTENSION / REDUNDANT)
- Rescue CAND-085 (INSUFFICIENT)
- Generate V32 replacement for CAND-097 without owner authorization
- Optimize CAND-077 filters
- Automatically promote CAND-077, CAND-081, or CAND-083 to STATE-ARTIFACT
- Create new Alpha from CAND-077
- Select >15 bps as the threshold for any future hypothesis
- Select any rejection-count threshold for CAND-083
- Modify forward runner
- Inspect CAND-015/024/035 performance
- Perform System Assembly
- Rescue closed candidates
- Treat exploratory filter observations as validated
- Rescue SEED-002 (negative relational finding)
- Test CAND-092/CAND-093/CAND-094 combinations
- Reopen CAND-077, CAND-078, or CAND-079
- Retroactively designate CAND-024/CAND-035 as downstream Alphas for CAND-077/CAND-081/CAND-083
- Create variants of CAND-077, CAND-081, or CAND-083
- Skip the Mechanism-Observable Challenge in V34+ G0 discovery
- Treat Proxy Confidence as an automatic rejection criterion
- Use the Mechanism-Observable Challenge to retroactively score V19–V33 candidates

---

## 21. RESEARCH DOCTRINE

> Frequency is not value.
> Win rate is not expectancy.
> R is a measurement unit, not a target.
> bps is a measurement unit, not a universal qualification law.
> Information is not automatically monetizable.
> A state is not a strategy.
> A counterfactual advantage is not automatically absolute Alpha.
> A plausible mechanism is not a proven mechanism.
> A promising sample is not validated evidence.

---

## 22. DATA LIMITATION

Volume data unavailable / zero for both USATECHIDXUSD and XAUUSD M1 data. Do not claim volume confirmation where no actual volume exists.

---

## 23. RESTART INSTRUCTIONS

1. Read this document completely
2. Read the G1 V3 ratification artifact
3. Read the V26 closure artifact
4. Read the candidate register (RESEARCH_DISCOVERY_DATABASE.md)
5. Determine which task the owner wants
6. Execute only the authorized task
7. Do NOT reconstruct project history from conversation

---

## 24. AUTHORITATIVE ARTIFACT INDEX

| Artifact | Path |
|---|---|
| G1 V3 Ratification | `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md` |
| G1 Hard Gates vs Evidence | `output/research_discovery/QUANTFORGE_G1_HARD_GATES_VS_EVIDENCE_ADJUDICATION_V1.md` |
| G1 V3 Proposal | `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_PROPOSAL.md` |
| G1 Criteria Audit | `output/research_discovery/QUANTFORGE_G1_ECONOMIC_QUALIFICATION_CRITERIA_AUDIT_V1.md` |
| Historical Reclassification Audit | `output/research_discovery/QUANTFORGE_HISTORICAL_CANDIDATE_V3_RECLASSIFICATION_AUDIT_V1.md` |
| V24 Closure + Meta-Review | `output/research_discovery/QUANTFORGE_V24_CLOSURE_AND_FACTORY_META_REVIEW_V1.md` |
| V25 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V25.md` |
| V25 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260829_V25.md` |
| V26 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V26.md` |
| V26 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V26.md` |
| V26 Closure + Knowledge | `output/research_discovery/QUANTFORGE_V26_CLOSURE_DYNAMIC_STATE_KNOWLEDGE_V1.md` |
| Candidate Register | `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` |
| Research Timeline | `research/knowledge/RESEARCH_TIMELINE.md` |
| V26 G1 Summary (HTML) | `output/research_discovery/V26_G1_SUMMARY.html` |
| Operator Runtime Correction | `output/research_discovery/QUANTFORGE_OPERATOR_RUNTIME_CORRECTION_V1.md` |
| V27 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V27.md` |
| V27 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V27.md` |
| CAND-077+081 State Governance | `output/research_discovery/QUANTFORGE_CAND077_CAND081_STATE_GOVERNANCE_REVIEW_V1.md` |
| V28 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V28.md` |
| V28 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V28.md` |
| CAND-083 State Governance | `output/research_discovery/QUANTFORGE_CAND083_STATE_GOVERNANCE_REVIEW_V1.md` |
| V29 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V29.md` |
| V29 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V29.md` |
| Relational Research Framework | `output/research_discovery/QUANTFORGE_RELATIONAL_RESEARCH_FRAMEWORK_GOVERNANCE_V1.md` |
| Unified Knowledge Ledger V1 | `output/research_discovery/QUANTFORGE_UNIFIED_RESEARCH_KNOWLEDGE_LEDGER_V1.md` |
| Unified Research History CSV Ledger V1 | `research/knowledge/unified_ledger/` (7 CSV files + data dictionary + reconciliation exceptions) |
| CSV Ledger Milestone Report | `output/research_discovery/QUANTFORGE_UNIFIED_RESEARCH_HISTORY_CSV_LEDGER_V1.md` |
| Cross-Research Object Ledger V1 | `research/knowledge/unified_ledger/QUANTFORGE_CROSS_RESEARCH_OBJECT_LEDGER_V1.csv` (64 objects: QF + APEX + SMC + Bot + Watchlist) |
| Cross-Research Integration Report | `output/research_discovery/QUANTFORGE_CROSS_RESEARCH_KNOWLEDGE_INTEGRATION_V1.md` |
| V30 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V30.md` |
| V30 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V30.md` |
| V30 G1 Integrity Audit | `output/research_discovery/QUANTFORGE_V30_G1_INTEGRITY_AUDIT_V1.md` |
| V31 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V31.md` |
| V31 G0 Integrity Audit | `output/research_discovery/QUANTFORGE_V31_G0_INTEGRITY_AUDIT_V1.md` |
| V31 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V31.md` |
| V31 G1 Adjudication Audit | `output/research_discovery/QUANTFORGE_V31_G1_ADJUDICATION_INTEGRITY_AUDIT_V1.md` |
| V32 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V32.md` |
| V32 G0 Integrity Audit | `output/research_discovery/QUANTFORGE_V32_G0_INTEGRITY_AUDIT_V1.md` |
| V32 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V32.md` |
| V33 G0 Screening | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V33.md` |
| V33 G0 Integrity Audit | `output/research_discovery/QUANTFORGE_V33_G0_INTEGRITY_AUDIT_V1.md` |
| V33 G1 Screen | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260901_V33.md` |
| G0 Process Refinement | `output/research_discovery/QUANTFORGE_G0_MECHANISM_OBSERVABLE_CHALLENGE_V1.md` |

---

## 25. UNIFIED RESEARCH HISTORY CSV LEDGER V1

**Status:** ESTABLISHED — RECONCILED

**Scope:** Full QuantForge research history (Pre-Research Factory through V29)

**Location:** `research/knowledge/unified_ledger/`

**Contents:**
- 73 candidates reconstructed (CAND-010 through CAND-088 + G1 Invalid batch)
- 12 behavioural knowledge records
- 21 structured evidence measurements
- 7 State objects with full provenance
- 5 exploratory observations
- 69 negative knowledge records
- 10 conceptual relationships (ALL UNTESTED)
- 8 reconciliation exceptions documented

**Key files:**
- `QUANTFORGE_RESEARCH_CANDIDATE_LEDGER_V1.csv` — master candidate register
- `QUANTFORGE_BEHAVIOURAL_KNOWLEDGE_LEDGER_V1.csv` — knowledge findings
- `QUANTFORGE_RESEARCH_EVIDENCE_LEDGER_V1.csv` — structured measurements
- `QUANTFORGE_STATE_LIBRARY_LEDGER_V1.csv` — State objects
- `QUANTFORGE_EXPLORATORY_OBSERVATIONS_LEDGER_V1.csv` — exploratory findings
- `QUANTFORGE_NEGATIVE_KNOWLEDGE_LEDGER_V1.csv` — closure/negative knowledge
- `QUANTFORGE_RESEARCH_RELATIONSHIP_LEDGER_V1.csv` — conceptual relationships
- `QUANTFORGE_UNIFIED_LEDGER_DATA_DICTIONARY_V1.md` — column definitions
- `QUANTFORGE_UNIFIED_LEDGER_RECONCILIATION_EXCEPTIONS_V1.md` — discrepancies

**Nature:** Knowledge infrastructure — NOT an experiment, NOT a relational test, NOT a promotion mechanism.

**Future maintenance:** Every milestone closeout should update relevant ledger rows.

---

## 26. CROSS-RESEARCH INTEGRATION V1

**Status:** COMPLETE — RECONCILED

**Streams integrated:**
- QuantForge RF (V19–V29 + pre-V19): 20 objects
- APEX_CORE (RC012–RC015, M17–M52): 29 objects
- SMC_STREAM (R1–R11): 12 objects
- CUSTOM_BOT_OBSERVED: 1 object (provisional)
- APEX_WATCHLIST: 2 objects (untested)
- **Total: 64 cross-research objects**

**Key finding:** APEX has 6 validated scientific primitives (HIGH_VOL distribution/persistence/predictability, session-transition LNO distribution/scale, BTC transferability) but ZERO validated economic modules (M3=0, M4=0). SMC has validated event extraction but both BOS+OB (M4 FAILED) and CHOCH (M3 FAILED) failed economics.

**State library:** UNCHANGED (CAND-077/081/083 STATE REVIEW ELIGIBLE)
**Forward runtime:** UNTOUCHED
**Relational experiments:** NOT EXECUTED
**V30:** NOT EXECUTED

---## 27. RELATIONAL RESEARCH V1 — SEED-002 DISCOVERY

**Status:** GOVERNANCE COMPLETE — SEED-002 REGISTERED AND TESTED

**Governance questions resolved:**
1. Minimum sample: Evidence-quality-dependent (no universal N ratified)
2. Confirmation: Temporal separation required
3. Incremental info: A+B vs max(A-alone, B-alone) comparison structure
4. Counterfactual: CAND-081 WITH CAND-083 vs CAND-081 WITHOUT CAND-083
5. Multiple testing: Sufficient with registration + limited relationships
6. Rare events: Governed by evidence-quality framework
7. Temporal: A → structural failure → B → downstream
8. Causal language: CONDITIONAL ASSOCIATION — NOT CAUSAL PROOF

**SEED-002:** REGISTERED AND TESTED
- Input A: CAND-083 (STATE REVIEW ELIGIBLE, +4.60 bps conditional delta)
- Input B: CAND-081 (STATE REVIEW ELIGIBLE, +1.23 bps conditional delta)
- Hypothesis: Does structural failure preceded by CAND-083 accumulated rejection produce different downstream economics when CAND-081 trapped-participant state occurs?
- Counterfactual: CAND-081 events WITHOUT CAND-083 precondition

**Discovery result:** NO INCREMENTAL INFORMATION — CONTROL SUPERIOR
- Treatment (CAND-081 WITH CAND-083): N=4,917, Net Mean=-1.96 bps, Median=-1.61 bps, WR=46.1%
- Control (CAND-081 WITHOUT CAND-083): N=1,784, Net Mean=-0.19 bps, Median=-0.90 bps, WR=48.7%
- Delta Mean: -1.78 bps, Delta Median: -0.72 bps
- Classification: CONTROL SUPERIOR — CAND-083 precondition makes CAND-081 worse

**Artifact:** `output/research_discovery/QUANTFORGE_RELATIONAL_SEED002_DISCOVERY_RESULTS_V1.md`
**Script:** `research/seed002_relational_experiment.py`

**Confirmation:** NOT EXECUTED (not warranted — result is negative)
**G2:** NOT EXECUTED
**V30:** NOT EXECUTED
**System Assembly:** NOT EXECUTED

**State library:** UNCHANGED (CAND-077/081/083 STATE REVIEW ELIGIBLE)
**Forward runtime:** UNTOUCHED
**CAND-088:** EXPLORATORY / PROVISIONAL — NEW G0 REQUIRED

---

## 28. V30 G0 — FRESH MECHANISM DISCOVERY + INTEGRITY AUDIT

**Status:** G0 COMPLETE — AUDIT COMPLETE — 1 CANDIDATE REDUNDANT

**Candidates (original V30 G0):**

| ID | Name | Artifact Type | Mechanism Family | Prior-Art | Audit Result |
|---|---|---|---|---|---|
| CAND-089 | Acceptance Velocity Decay | STANDALONE ALPHA / STATE | Information Processing Dynamics | NEW | **ELIGIBLE** |
| CAND-090 | Recovery Quality Differential | STANDALONE ALPHA / STATE | Response Quality Dynamics | **REDUNDANT (same as CAND-087)** | **REJECTED** |
| CAND-091 | Cumulative Directional Exhaustion | STATE / CONDITION | Directional Exhaustion Dynamics | NEW | **ELIGIBLE** |

**CAND-090 rejection reason:** Identical economic hypothesis to V29 CAND-087 (Recovery Quality Differential). Same research question, same mechanism, same observable concept, same counterfactual structure, same economic prediction. Parameter differences (10 vs 30 bars, 20 vs 60 holding) are implementation choices, not mechanism distinctions.

**V30 eligible candidates for G1:** CAND-089, CAND-091 (2 of 3)

**SEED-002 lesson applied:** Not all conceptually plausible combinations produce positive information. V30 focuses on mechanism-quality rather than condition-quantity.

**Cross-research ledger:** Used as knowledge map only. No relational testing.

**State library:** UNCHANGED (CAND-077/081/083 STATE REVIEW ELIGIBLE)
**Forward runtime:** UNTOUCHED
**CAND-088:** EXPLORATORY / PROVISIONAL — NEW G0 REQUIRED
**SEED-002:** TESTED NEGATIVE — NO INCREMENTAL INFORMATION

**Artifacts:**
- V30 G0: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V30.md`
- Integrity Audit: `output/research_discovery/QUANTFORGE_V30_G0_INTEGRITY_AUDIT_V1.md`

---

## 29. V30 G1 — ECONOMIC PLAUSIBILITY SCREEN

**Status:** COMPLETE — BOTH CANDIDATES CLOSED
| Candidate | Decision | Rationale |
|---|---|---|
| CAND-089 (Acceptance Velocity Decay) | **CLOSED — NO INCREMENTAL INFORMATION** | Mean delta +0.26 bps, median delta -0.22 bps, WR delta -1.2%. No meaningful distributional separation. Mechanism ambiguous. |
| CAND-091 (Cumulative Directional Exhaustion) | **CLOSED — HYPOTHESIS CONTRADICTED** | Mean delta -0.67 bps (control superior), median delta -0.39 bps. Exhaustion adds dispersion (49.79 vs 29.78 bps std) without return. Worst tail much worse (-45 vs -31 bps P10). |

**Key evidence:**
- CAND-089: N=4,152 (treatment) / 4,269 (control). Net Mean: -2.20 / -2.46 bps. Near-zero conditional delta.
- CAND-091: N=3,886 (treatment) / 4,535 (control). Net Mean: -2.69 / -2.02 bps. Treatment WORSE than control.
- Both candidates pass all 9 hard validity gates. Failures are in economic evidence, not measurement.
- Mechanism quality: CAND-089 ambiguous, CAND-091 contradicted.
- State potential: NOT JUSTIFIED for either.

**Artifacts:**
- V30 G1 Screen: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V30.md`
- Script: `research/v30_g1_experiment.py`

---

## 30. V30 G1 INTEGRITY AUDIT

**Status:** COMPLETE — VERIFIED WITH DOCUMENTATION CORRECTIONS

**Verdict:** VERIFIED WITH DOCUMENTATION CORRECTIONS

**Key findings:**
- CAND-089 rewrite traced: changed from per-test velocity to per-break velocity (SEMANTIC DRIFT). Negative result is robust to this difference.
- CAND-091: fully verified, implementation matches G0 hypothesis.
- Distribution wording corrected: "indistinguishable" → "no meaningful distributional separation demonstrated."
- All 9 hard gates verified for both candidates.
- No look-ahead, no treatment contamination, valid counterfactuals.
- V30 closure: VALID.

**Corrections applied:**
1. Distribution wording in G1 artifact (Section 5.7)
2. Velocity measurement note added to G1 artifact (Section 5.1)

**Artifact:** `output/research_discovery/QUANTFORGE_V30_G1_INTEGRITY_AUDIT_V1.md`

---

## 31. V31 G1 — ECONOMIC PLAUSIBILITY SCREEN

**Status:** COMPLETE — BOTH CANDIDATES CLOSED
| Candidate | Decision | Rationale |
|---|---|---|
| CAND-092 (Event-Information Decay) | **CLOSED — ECONOMICALLY NEGATIVE** | Evidence profile: MIXED / METRIC DISCORDANCE. Mean delta -2.11 bps (control superior). Median delta +0.21 bps (trivially positive). WR delta +3.3%. Negative central tendency dominates. |
| CAND-093 (Price-Discovery Friction) | **CLOSED — ECONOMICALLY NEGATIVE** | Evidence profile: MIXED / METRIC DISCORDANCE. Mean delta -1.00 bps (control superior). Median delta +0.77 bps (treatment better). WR delta +0.6%. Negative central tendency dominates. |

**Key evidence:**
- CAND-092: N=3,195 (treatment) / 3,324 (control). Net Mean: -3.42 / -1.31 bps. ECONOMICALLY NEGATIVE. Evidence profile: MIXED / METRIC DISCORDANCE.
- CAND-093: N=5,601 (treatment) / 2,820 (control). Net Mean: -2.67 / -1.66 bps. ECONOMICALLY NEGATIVE. Evidence profile: MIXED / METRIC DISCORDANCE.
- Both candidates pass all 9 hard validity gates. Failures are in economic evidence, not measurement.
- State potential: NOT JUSTIFIED for either.

**Artifacts:**
- V31 G1 Screen: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V31.md`
- V31 G1 Adjudication Audit: `output/research_discovery/QUANTFORGE_V31_G1_ADJUDICATION_INTEGRITY_AUDIT_V1.md`
- Script: `research/v31_g1_experiment.py`

---

## 32. V32 G0 — KNOWLEDGE-GAP / ECONOMIC-MECHANISM DISCOVERY

**Status:** G0 COMPLETE — INTEGRITY AUDIT COMPLETE — 1 CANDIDATE REDUNDANT
**Candidates (after integrity audit):**

| ID | Name | Expression Class | Mechanism Family | Prior-Art | Audit Result |
|---|---|---|---|---|---|
| CAND-095 | Shock-Magnitude Asymmetry | STATE / CONDITION | Directional Response Asymmetry | NEW | **ELIGIBLE** |
| CAND-096 | Volatility Acceleration Gradient | STATE / CONDITION | Volatility Dynamics | NEW | **ELIGIBLE** |
| CAND-097 | Post-Shock Overshoot Reversion | STANDALONE ALPHA / STATE | Mean-Reversion Dynamics | **REDUNDANT (same as DISC-021)** | **REJECTED** |
**CAND-097 rejection reason:** Identical economic hypothesis to DISC-021 Mean Reversion line. Both test: price moves too far → reverts. DISC-021 used z-score displacement; CAND-097 uses ATR-based shock magnitude. The economic mechanism (mean reversion after extreme movement) is the same. DISC-021 established this mechanism is statistically observable but economically non-viable (costs consume the effect).
**V32 eligible candidates for G1:** CAND-095, CAND-096 (2 of 3)

**V32 G1 result:** COMPLETE — Both candidates closed. CAND-095 ECONOMICALLY NEGATIVE. CAND-096 HYPOTHESIS CONTRADICTED / INFORMATIONALLY INTERESTING. V32 permanently closed. See section 33.
**V30/V31 lessons applied:**
- No velocity/exhaustion/recovery variants
- No time-since-event as primary variable
- No approach-smoothness as primary variable
- No condition accumulation
**Cross-research ledger:** Used as knowledge map only. 5 heavily explored families avoided. 5 under-explored gaps identified.
**State library:** UNCHANGED (CAND-077/081/083 STATE REVIEW ELIGIBLE)
**Forward runtime:** UNTOUCHED
**SEED-002:** TESTED NEGATIVE — NO INCREMENTAL INFORMATION
**APEX RB001–RB004:** DESIGNED / NOT EXECUTED**Artifacts:**
- V32 G0: `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V32.md`
- Integrity Audit: `output/research_discovery/QUANTFORGE_V32_G0_INTEGRITY_AUDIT_V1.md`

---

## 33. V32 G1 — ECONOMIC PLAUSIBILITY SCREEN

**Status:** COMPLETE — BOTH CANDIDATES CLOSED — V32 CLOSED / VERIFIED

| Candidate | Decision | Rationale |
|---|---|---|
| CAND-095 (Shock-Magnitude Asymmetry) | **CLOSED — ECONOMICALLY NEGATIVE** | Mean delta -0.28 bps (control superior), median delta -0.58 bps (control superior), WR delta -2.2% (control superior). All metrics favor control. Mechanism ambiguous. |
| CAND-096 (Volatility Acceleration Gradient) | **CLOSED — HYPOTHESIS CONTRADICTED** | Mean delta -1.62 bps (control superior), median delta -1.48 bps (control superior), WR delta -3.1% (control superior). Decelerating volatility significantly outperforms accelerating. Information is real but hypothesis direction is wrong. Economic adjudication: INFORMATIONALLY INTERESTING. STATE REVIEW ELIGIBLE (opposite direction). |

**Key evidence:**
- CAND-095: N=7,325 (treatment) / 7,524 (control). Net Mean: -1.42 / -1.14 bps. All metrics favor control. ECONOMICALLY NEGATIVE.
- CAND-096: N=5,622 (treatment) / 897 (control). Net Mean: -1.23 / +0.40 bps. Decelerating volatility is superior. HYPOTHESIS CONTRADICTED but INFORMATIONALLY INTERESTING.
- Both candidates pass all 9 hard validity gates. Failures are in economic evidence, not measurement.
- CAND-096 semantic check against CAND-077: PASS — implementation genuinely measures acceleration (second derivative), not regime transition.
- CAND-095: State potential NOT JUSTIFIED.
- CAND-096: State potential — INFORMATIONALLY INTERESTING in opposite direction. Hypothesis direction contradicted but conditional information real.

**Artifacts:**
- V32 G1 Screen: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260831_V32.md`
- Script: `research/v32_g1_experiment.py`

---

## 34. V33 G1 — ECONOMIC PLAUSIBILITY SCREEN

**Status:** V33 G1 COMPLETE — BOTH CANDIDATES CLOSED

| Candidate | Decision | Rationale |
|---|---|---|
| CAND-098 (Event-Cluster Response Degradation) | **CLOSED — ECONOMICALLY NEGATIVE** | Hypothesis supported on distribution width (clustered events produce wider distributions), but absolute economics negative and conditional delta insufficient for State qualification. Mean delta=-1.11 bps, Median delta=-0.30 bps, WR delta=-1.2%. |
| CAND-099 (Volatility Regime Transition Quality) | **CLOSED — HYPOTHESIS CONTRADICTED / INFORMATIONALLY INTERESTING** | Sharp transitions massively outperform smooth transitions. Mean delta=-18.08 bps (control superior), Median delta=-30.52 bps, WR delta=-59.0% (99% vs 40%). Hypothesis direction WRONG. N=100 per group (marginal). |

**Key evidence:**
- CAND-098: Treatment N=8,392, Control N=1,017. Clustered events produce wider distributions (std 32.69 vs 24.93 bps) but worse economics. 9/9 hard gates PASS.
- CAND-099: Treatment N=100, Control N=100. Sharp transitions produce +16.39 bps net mean with 99% WR. Smooth transitions produce -1.69 bps net mean with 40% WR. 9/9 hard gates PASS (marginal on sample adequacy).
- CAND-099 semantic check against CAND-077/096 PASS — implementation measures transition quality, not regime state or acceleration.
- State potential: NOT JUSTIFIED for either candidate.

**Artifacts:**
- V33 G1 Screen: `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260901_V33.md`
- Script: `research/v33_g1_experiment.py`

---

## 35. V33 G0 INTEGRITY / PRIOR-ART AUDIT

**Status:** AUDIT COMPLETE — 2 G1-ELIGIBLE, 1 DATA-INFEASIBLE

| Candidate | Disposition | Rationale |
|---|---|---|
| CAND-098 | **G1 ELIGIBLE** | Clearly novel — multi-event cumulative load vs single-event temporal decay |
| CAND-099 | **G1 ELIGIBLE** | Materially distinct from CAND-077/096 — transition quality vs regime state vs acceleration |
| CAND-100 | **DATA INFEASIBLE** | Core observable (bid-ask spread) unavailable. OHLC proxy conflates with volatility research. |

**CAND-100 closure reason:** Bid-ask spread data is not available in the governed dataset (confirmed in data_feed.py: `"spread": "unavailable"`). The proposed OHLC proxy (high-low range) is a volatility measure, not a spread measure, and would collapse the hypothesis into existing CAND-077/CAND-096 research. The mechanism (forced positioning, liquidity stress) requires actual spread information.

**V33 G1 authorized for:** CAND-098, CAND-099 only.
**Candidate count:** 2 G1-eligible (within 2-4 target range). No replacement generated.

**Artifact:** `output/research_discovery/QUANTFORGE_V33_G0_INTEGRITY_AUDIT_V1.md`

---

## 35. V33 G0 — KNOWLEDGE-GAP / ECONOMIC-MECHANISM DISCOVERY

**Status:** G0 COMPLETE — 3 NEW CANDIDATES FROM KNOWLEDGE-GAP ANALYSIS

**Candidates:**

| ID | Name | Expression Class | Mechanism Family | Prior-Art |
|---|---|---|---|---|
| CAND-098 | Event-Cluster Response Degradation | STATE / CONDITION | Event-Cluster Dynamics | NEW |
| CAND-099 | Volatility Regime Transition Quality | STATE / CONDITION | Volatility Dynamics | NEW |
| CAND-100 | Spread-Conditioned Execution Stress | STATE / CONDITION | Market Microstructure | NEW |

**Knowledge gaps addressed:**
1. Event-cluster response decay (CAND-098)
2. Volatility regime transition quality (CAND-099)
3. Execution stress and spread dynamics (CAND-100)
**Cross-research ledger:** Used as knowledge map only. 5 heavily explored families avoided. 5 under-explored gaps identified, 3 addressed.

**V32 lessons applied:**
- No velocity/exhaustion/recovery variants
- No time-since-event as primary variable
- No condition accumulation
- No mean-reversion variants

**State library:** UNCHANGED (CAND-077/081/083 STATE REVIEW ELIGIBLE)
**Forward runtime:** UNTOUCHED
**SEED-002:** TESTED NEGATIVE — NO INCREMENTAL INFORMATION
**APEX RB001–RB004:** DESIGNED / NOT EXECUTED

**Artifact:** `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V33.md`

---

## 35. V32 CLOSURE

**Status:** V32 CLOSED / VERIFIED

V32 complete: 0 G2 promotions. 3 original candidates discovered, 1 rejected at G0 (CAND-097 = REDUNDANT WITH DISC-021), 2 tested at G1, 2 closed.

- CAND-095: CLOSED / ECONOMICALLY NEGATIVE
- CAND-096: CLOSED / HYPOTHESIS CONTRADICTED (INFORMATIONALLY INTERESTING, STATE REVIEW ELIGIBLE — opposite direction)
- CAND-097: CLOSED / REDUNDANT WITH DISC-021

Key negative knowledge:
- Shock-magnitude asymmetry does not produce directional downstream advantage (DOWN slightly better than UP, contradicting hypothesis).
- Volatility deceleration produces better economics than acceleration — the opposite of the hypothesized mechanism. This is genuine conditional information but in the wrong direction.
- CAND-096 implementation genuinely measures acceleration, not regime transition — confirms CAND-077 distinctness.

---

## 36. G0 PROCESS REFINEMENT — MECHANISM-OBSERVABLE CHALLENGE

**Status:** RATIFIED — PROSPECTIVE GOVERNANCE REFINEMENT

**Effective:** V34 G0 onward

**Basis:** V29–V33 Research Factory Meta-Audit (completed 2026-09-01)

### What Changed

Beginning with V34 G0, every candidate must answer eight mandatory Mechanism-Observable Challenge questions:

A. **Mechanism Independence** — What market phenomenon exists independently of the proposed feature?
B. **Proxy Challenge** — How could the observable be generated without the claimed mechanism?
C. **Alternative Explanation** — What competing market state could create the same observable?
D. **Observable Fidelity** — Why is the observable a reasonable measurement of the claimed mechanism?
E. **Expected-Effect Bridge** — Why should this observable alter the outcome distribution?
F. **Falsification** — What result would clearly contradict the mechanism?
G. **Tradeability Challenge** — What would make the effect disappear after realistic costs?
H. **Base-Rate Challenge** — Why does this candidate deserve G1 testing given the historical base rate?

Each candidate receives a **Proxy Confidence** assessment: STRONG / MODERATE / WEAK.

The G0 artifact must separately record **Mechanism Confidence** and **Observable Information Potential**.

### What Did NOT Change

- No hard mechanism-quality gate introduced
- No automatic rejection system
- No numeric scoring
- G1 V3 framework unchanged
- G0 integrity audit unchanged
- Prior-art process unchanged
- State library unchanged
- Closed-line firewalls unchanged
- Relational governance unchanged
- Forward runtime unchanged

### Why NOT a Hard Gate

CAND-099 demonstrated that mechanism falsification does not imply observable invalidity. A hard gate might have rejected CAND-099 before G1, losing the genuinely informative transition-quality finding. The challenge surfaces weaknesses; it does not automatically reject.
### Historical State

No V19–V33 candidate is retroactively scored against this framework.

### Artifact

`output/research_discovery/QUANTFORGE_G0_MECHANISM_OBSERVABLE_CHALLENGE_V1.md`

---

*Authoritative for next session. Updated 2026-09-01 (V33 G1 + G0 process refinement). V33 G1 complete: CAND-098 ECONOMICALLY NEGATIVE, CAND-099 HYPOTHESIS CONTRADICTED / INFORMATIONALLY INTERESTING. V33 CLOSED. V32 CLOSED / VERIFIED. V31 CLOSED / VERIFIED. V30 CLOSED / VERIFIED. State objects preserved (CAND-077/081/083 STATE REVIEW ELIGIBLE). SEED-002 negative. Forward runtime protected. G0 process refinement introduced: Mechanism-Observable Challenge effective V34 G0 onward. No hard mechanism gate. Next authorized: V34 G0 — NEW DISCOVERY under refined G0 process (if owner authorizes).*
