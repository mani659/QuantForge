# QUANTFORGE — INDEPENDENT PROGRAM-LEVEL RESEARCH + ARCHITECTURE AUDIT V1

**Date:** 2026-08-24
**Auditor role:** Senior Research Architect / Systems Architect / Senior Software Engineer
**Mode:** READ-ONLY — no modifications, no experiments, no implementations
**Authoritative commit:** `2007e07` — `docs: close ORD XAGUSD economic translation`

---

## 1. Executive Verdict

**QuantForge is an excellent scientific research laboratory that has not yet become an efficient machine for discovering profitable strategies.**

The project has built world-class governance, provenance, reproducibility, and closure discipline. These are genuine, rare strengths. However, after ~15 days of intensive work (2026-08-09 through 2026-08-24), six research lines, and hundreds of thousands of words of governance documentation, the program has produced:

- **Zero positive economic results**
- **Zero tradeable strategies**
- **Zero validated edges**
- **Zero bot-ready outputs**

Every research line that reached economic testing failed. Several produced strong *scientific* results — but scientific support and economic viability are fundamentally different things, and QuantForge has been treating the first as a reliable precursor to the second. It is not.

The program remains credible, but only if the research factory is restructured to prioritize early economic screening before committing heavy engineering resources.

---

## 2. Current Authoritative State

| Dimension | Status |
|---|---|
| HEAD commit | `2007e07` — `docs: close ORD XAGUSD economic translation` |
| Branch | `main` (linear, 24 commits including duplicates across what appear to be two remotes) |
| Current milestone | TRADEABLE EDGE DISCOVERY SCREENING |
| Active research lines | None |
| Closed lines | DISC-021 through DISC-026 (6 lines closed) |
| BOE runtime | Contracts frozen, no detector implemented |
| Strategy Assembly | FROZEN (AMEND-1 ratified) |
| Test baseline | 614 tests passed at freeze point (2026-08-12) |
| Data inventory | 5 M1 CSV markets (~500 MB), 5 MT5 tick CSV markets (~42 GB) |
| Research artifacts | 125 governance markdown documents (~1.5 MB), 118 files in `output/research_discovery/` |

---

## 3. Research History Reconstruction

### Matrix: All Six Research Lines

| Line | Hypothesis | Scientific Result | Economic Result | Opened | Closed | Closure Justified? | Engineering Cost | Information Gained |
|---|---|---|---|---|---|---|---|---|
| **DISC-021** Mean Reversion | Extreme displacement → recoil → persistence creates deployable edge | Narrow XAGUSD DOWN asymmetry statistically observable | NON-VIABLE (observed spreads consume gross effect; break-even ~10.9 bp vs median RT ~9.1 bp) | 2026-08-10 | 2026-08-12 | **YES** — rigorous, cost data was definitive | MEDIUM (V1-V3 event studies + cost viability) | HIGH — established cost-awareness discipline |
| **DISC-022** TSMOM 12/1 | Fixed trend signal adds incremental value above drift | PARTIALLY REPRODUCED (historical +0.67%/mo incremental, contemporary −1.10%/mo) | NOT CONFIRMED (Condition 8 cross-era consistency FAILS) | 2026-08-12 | 2026-08-13 | **YES** — clean design, definitive cross-era failure | HIGH (V1 + V2 with full 28-market HPD panel) | MEDIUM — drift-control methodology is reusable |
| **DISC-023** H01 Equity Track A | Classic volatility-response asymmetry is tradeable | STRONGLY SUPPORTED (US-tech cross-era replication TRUE) | ECONOMIC FAILURE (dual-era gate failed: historical negative, contemporary positive) | 2026-08-13 | 2026-08-23 | **YES** — but enormous engineering cost for predictable economic outcome | **VERY HIGH** (screening, scope decision, data-source audit, data acquisition, Norgate investigation, NYA verification, definition lock, multiple protocol audits, v1.1→v1.2→v1.3 implementation iterations, 4 economic executions, source identity amendments) | LOW relative to cost — the leverage effect is one of the most documented stylized facts in finance; converting it to a daily-frequency trade was always extremely unlikely to work |
| **DISC-024** Session Range Expansion | Pre-session compression precedes expansion | CONTRADICTED (compression → *smaller* range) | N/A (scientific failure) | 2026-08-17 | 2026-08-17 | **YES** — quick, efficient falsification | LOW | HIGH per unit cost — fast kill is the ideal model |
| **DISC-025** Liquidity Sweep / Reversal | Asian sweep + rejection → directional excursion | BEHAVIORALLY SUPPORTED (4 markets, Holm-corrected) | NON-VIABLE (gross-negative before costs; translation failure) | 2026-08-17 | 2026-08-17 | **YES** — but revealed a structural flaw in translation design | MEDIUM | HIGH — established the "entry must be the event" principle |
| **DISC-026** ORD | Opening-range breakout → continuation is tradeable | SCIENTIFICALLY SUPPORTED (3/3 markets Holm-adjusted) | NON-VIABLE (XAGUSD: median net −12.4 bp, PF 0.356, Win 9.1%) | 2026-08-17 | 2026-08-24 | **YES** — definitive failure | **EXTREMELY HIGH** (definition lock, protocol v1 → v1 amended → v2 → v2.1 → v2.1 amended, 2 protocol audits, scientific execution with crashes/memory remediation/reconciliation, invalidation governance review, Parquet specification v2, converter implementation + audit, production Parquet conversion, Stage-1 adapter + audit, Stage-1 production execution, Stage-1 output audit, Stage-2 execution, independent adjudication, closure) | LOW relative to cost — the gross response (1-2 bp mean) was visible in the earlier viability screen before all staged infrastructure was built |

### Critical Observation

**DISC-024 is the model for what efficient research should look like.** It was screened, defined, executed, adjudicated, and closed within a single session. Total artifact count: ~6 documents.

**DISC-026 (ORD) produced 64+ governance documents**, a custom Parquet specification, a full tick-to-Parquet converter, a multi-stage execution framework (4 stages), crash reconciliation infrastructure, memory remediation code, and ~150 KB of protocol amendments — all to discover that the gross signal is 1-2 basis points, which was already estimated by the earlier `ORD_V1_1_0_ECONOMIC_VIABILITY_SCREEN_V1.md` before the heavy infrastructure was built.

---

## 4. Scientific Record

### SCIENTIFICALLY SUPPORTED
- DISC-021 (narrow XAGUSD displacement asymmetry — real but too small)
- DISC-025 (liquidity sweep behavior — real across 4 markets)
- DISC-026 (opening-range breakout — real across 3 markets)
- H01 Equity V1 (volatility-response asymmetry — strongly replicated in US-tech)

### SCIENTIFICALLY INCONCLUSIVE
- DISC-022 / TSMOM V1 (F1 CI includes zero)

### SCIENTIFICALLY PARTIALLY REPRODUCED
- DISC-022 / TSMOM V2 (historical positive, contemporary contradictory)

### SCIENTIFICALLY CONTRADICTED
- DISC-024 (session range expansion — effect goes in wrong direction)

### Summary
The research program has produced **genuine scientific findings**. Multiple behavioral phenomena have been rigorously validated with pre-registered protocols, dependence-aware inference, and clean negative controls. The scientific methodology is strong.

**However: zero of these scientific findings have been economically viable.** This is the central problem.

---

## 5. Economic Record

### ECONOMICALLY SUPPORTED
**None.**

### ECONOMICALLY FAILED (all tested candidates)
- DISC-021: observed costs consume gross effect
- DISC-022: cross-era inconsistency (not primarily a cost failure)
- DISC-023: dual-era stability gate failed
- DISC-025: gross-negative before costs (translation failure)
- DISC-026: gross response ~1-2 bp (structurally too small)

### Summary
**Every single candidate that reached economic testing has failed.** This is a 0/5 record. While individual closures are justified, the pattern demands explanation. The most likely explanations:

1. **The candidate mechanisms are too small.** Mean-reversion asymmetries, opening-range continuations, and leverage-effect translations produce single-digit basis-point gross signals — not enough to survive any realistic friction.

2. **The candidate generation is concentrated in a narrow mechanism family.** All tested candidates are effectively "detect a structural price-pattern event → trade in the event's direction → exit at a fixed horizon." This is one strategy template applied to different event definitions.

3. **Economic plausibility is checked too late.** The ORD viability screen showed 1-2 bp gross response *before* the full staged infrastructure was built, yet the project proceeded through 9 M-ORD-ECO milestones.

---

## 6. Research Factory Assessment

### Most Important Question: How plausible is it that QuantForge will eventually discover a genuinely tradeable edge?

**Assessment: MODERATE — but only if the research factory is restructured.**

**Evidence for MODERATE (not LOW):**
- The data inventory (5 markets, M1 + tick, bid/ask quotes) is genuine and valuable
- The scientific methodology is rigorous and trustworthy
- The governance discipline prevents overfitting and rescue bias
- Multiple behavioral phenomena *are* real — the research is not finding noise
- The infrastructure for reproducible execution exists and works
- The owner is willing to accept negative results (critical for integrity)

**Evidence against HIGH:**
- 0/5 economic successes after 15 days of intensive work
- Candidate mechanisms have been narrowly concentrated (price-pattern events with fixed-horizon exits)
- The gross signals found are consistently in the 1-10 bp range — below minimum friction for retail/CFD execution
- No cross-sectional, carry, microstructure, or multi-timescale mechanisms have been explored
- The program has not yet tested whether *any* mechanism in its data inventory can produce >20 bp gross per trade — the approximate minimum for retail viability

### Are we building an excellent scientific research laboratory, or an efficient machine for discovering profitable strategies?

**We are building an excellent scientific research laboratory.**

The laboratory produces trustworthy negative results. It does not yet efficiently discover positive economic results. The distinction is critical:

- A good research lab asks: "Is this phenomenon real?" → Answer: frequently yes
- An efficient discovery machine asks: "Can this phenomenon make money after costs?" → Answer: consistently no

The research factory needs to ask the economic question **first**, not after months of infrastructure building.

---

## 7. Architecture Assessment

### Strengths (Genuine, Worth Retaining)

1. **Source identity / provenance:** SHA-256 hashing of all inputs, frozen protocol hashes, byte-exact verification — production-grade
2. **Pre-registered protocols:** Scientific protocols frozen before execution — eliminates post-hoc rationalization
3. **Closure discipline:** Lines are closed definitively with explicit firewalls — prevents rescue bias
4. **Scientific/economic separation:** Clear distinction between "behavior is real" and "behavior is tradeable"
5. **EventStudyRecorder:** Fail-closed execution recording with artifact gates — well-designed
6. **Test baseline:** 614 tests passing with deterministic behavior — solid foundation
7. **Frozen contract boundaries:** BOE contracts are stable, well-documented, type-safe

### Weaknesses

1. **Duplicated sources of truth:** `sha256_file()` is implemented in at least 3 places (`_identity.py`, `event_study_recorder.py`, `run_ord_econ_v1.py`). The identity system should be a single importable module.

2. **Hardcoded paths and SHAs in execution scripts:** `run_ord_econ_v1.py` contains hardcoded `PROTOCOL_PATH`, `PROTOCOL_SHA`, `SCIENTIFIC_MANIFEST`, and `EVENT_TABLE` paths. These should be injected or derived from a manifest.

3. **Stage 2 hardcodes expected market-specific artifacts:** `REQUIRED_STAGE2_ARTIFACTS` in `stage2.py` lists `trade_ledger_XAUUSD.csv`, `trade_ledger_XAGUSD.csv`, etc. — tightly coupling the implementation to the current market set.

4. **Protocol version proliferation:** ORD went through V1 → V1 amended → V2 → V2.1 → V2.1 amended → V2.1 final re-audit. This is not architecture discipline; it's specification instability that burned engineering cycles.

5. **Research code vs. production code contamination:** The `strategy/` directory contains `signal_generator.py` with hardcoded `"recoil"` strategy class and mean-reversion-specific logic (z-score, body size, wick ratios). This code is from the original mean-reversion research and has never been connected to any validated strategy. It is dead code masquerading as architecture.

6. **BOE runtime is DESIGN BLOCKED:** The `BehaviorDetectorContract` is an abstract class with zero implementations. The entire BOE pipeline (`DeploymentOrchestrator`, observers, risk engine, position sizer) exists as infrastructure waiting for a detector that has never been built because no research line has produced a viable signal. **The BOE runtime is premature architecture.**

7. **Two parallel execution systems:** The `research/engine/run_engine.py` (ResearchRunEngine) and the `research/staged_execution/` system serve overlapping purposes with different abstractions. The staged system was built specifically for ORD and may not generalize cleanly.

---

## 8. Software Engineering Assessment

### Research Prototype Quality: FAIR to STRONG

| Dimension | Rating | Notes |
|---|---|---|
| Code architecture | FAIR | Clean module boundaries in BOE; research scripts are monolithic |
| Test coverage | STRONG | 614 tests, 86+ test files, covers contracts/observers/deployment/evidence |
| Deterministic behavior | STRONG | Seeds frozen, SHA verification, replay-capable |
| Reproducibility | STRONG | Input identity, protocol freezing, exactly-once execution |
| Maintainability | FAIR | Research scripts are 800-900 line monoliths; staged execution is better factored |
| Dependency management | FAIR | Standard Python scientific stack; `.venv` present |
| Error handling | FAIR | Fail-closed in staged system; less disciplined in research scripts |
| Performance | POOR to FAIR | Memory issues required remediation (ORD crash); tick file streaming is sequential |
| Data access | FAIR | CSV-based with Parquet conversion built for ORD; not generalized |
| Module boundaries | STRONG for BOE contracts; WEAK for research scripts | Research execution scripts are self-contained but not composable |

### Production-System Quality: NOT APPLICABLE

There is no production system. The BOE runtime pipeline exists as contracts and tests but has never been connected to a real strategy, a real detector, or real market data. The broker adapter (`mt5_adapter.py`, `mt5_connection.py`) exists but has never been exercised in a research context. The gap between current state and production is **very large** — this is expected at the research stage, but the project should be honest about it.

---

## 9. Data Architecture Assessment

### Current State
- **M1 OHLCV:** 5 CSV files, ~500 MB total, adequate for research
- **Tick bid/ask:** 5 CSV files, ~42 GB total, essential for cost modeling
- **Parquet:** Built for ORD via `tick_parquet_converter.py` — single-use, not generalized
- **HPD panel:** 28-market historical daily data used for TSMOM V2 — validated, fingerprinted

### Assessment

| Question | Answer |
|---|---|
| Can we add new datasets without repeating the identity saga? | PARTIALLY — if CSV, the identity infrastructure works; if a new format, significant work |
| Can multiple markets be represented cleanly? | YES for M1; the Parquet specification is XAGUSD-specific and would need generalization |
| Can new research lines reuse the infrastructure? | PARTIALLY — EventStudyRecorder is reusable; staged execution system is ORD-specific |
| Can we avoid rebuilding minute/tick representations repeatedly? | NO — each new mechanism may need different aggregation; current infrastructure is bespoke |
| Is provenance strong enough for future live validation? | YES — SHA identity is genuine and transferable |
| Is the architecture scalable beyond XAGUSD? | PARTIALLY — the M1 data is multi-market; the tick/Parquet pipeline needs generalization |

### Key Gap
The data architecture is adequate for M1-based research. The tick-level pipeline was over-specialized for ORD and would need to be rebuilt or generalized for a different mechanism. **This is a significant lesson: do not build bespoke data pipelines until the economic case is established.**

---

## 10. Economic Realism Assessment

### What Has Been Tested
| Dimension | Status |
|---|---|
| Transaction costs (bid/ask spreads) | **STRONG** — observed MT5 tick-level spreads, exact-minute matching, ≥98% coverage |
| Commission/slippage sensitivity | FAIR — fixed bands (0, 2, 5, 10, 20, 50 bp) rather than empirical |
| Execution timing | FAIR — entry at bar-close (realistic for M1 bars); no sub-bar execution modeling |
| Market impact | NOT TESTED — fixed notional assumed; no sizing/liquidity interaction |
| Signal latency | NOT TESTED — assumed instantaneous signal-to-order |
| Regime changes | PARTIALLY — chronological Dev/OOS splits; no regime-conditional testing |
| Forward testing | NOT PERFORMED — all testing is historical |
| Overfitting control | **STRONG** — pre-registered protocols, Holm correction, frozen specifications |
| Train/Dev/OOS design | **STRONG** — chronological splits, exactly-once TEST consumption |

### Critical Gap: Statistical Behavior vs. Actual Tradeability

QuantForge is currently proving **statistical behavior**, not **actual tradeability**. The distinction:

- **Statistical behavior:** "This event is followed by a directional move that is statistically distinguishable from the control group" (YES — multiple candidates)
- **Actual tradeability:** "A trader who enters at the observable event and exits at a predetermined point will make money after all realistic costs" (NO — zero candidates)

The gap is explained by a consistent pattern: **the gross signal sizes found (1-10 bp) are at or below the friction floor for retail/CFD execution.**

This raises a structural question: **Can the data inventory (MT5 CFD M1/tick data for 5 markets) support discovery of edges large enough to survive retail friction?** The answer is not yet determined, but five consecutive failures at the same friction boundary is evidence that deserves attention.

---

## 11. Research Bias Assessment

### Bias Controls (Strong)
- Pre-registered protocols before execution ✓
- Holm family-wise correction ✓
- Frozen specifications (no post-hoc tuning) ✓
- Exactly-once TEST consumption ✓
- Explicit closure without rescue ✓
- Independence checks against closed lines ✓

### Remaining Risks

1. **Candidate selection bias:** The screening process (NEW_HYPOTHESIS_SCREENING_V1, TRADEABLE_EDGE_DISCOVERY_SCREENING V1-V3) generates candidates from a narrow mechanism family — intraday price-pattern events. This is not post-result bias, but it is a *systematic limitation* in the candidate generation process.

2. **Sequential candidate testing:** Six candidates tested sequentially means the screening of later candidates is informed by the failures of earlier ones. This is methodologically appropriate (learning from negative results is good science), but it can create a "this time it will work" optimism bias. The ORD viability screen showed 1-2 bp gross *before* the full pipeline, yet the pipeline was built anyway.

3. **Data-source narrowing:** All research uses 5 MT5 CFD markets with a single broker's data. Broker-specific effects (spread patterns, tick data quality, session coverage) may not generalize. This is not bias per se, but it limits the universe of discoverable effects.

4. **No hidden degrees of freedom detected.** The governance system is genuinely effective at preventing post-hoc tuning, rescue attempts, and parameter shopping. This is a major strength.

---

## 12. What QuantForge Does Well

### Governance practices that should NEVER be weakened:
1. **Pre-registration before results.** Every protocol is frozen before execution. This is the gold standard.
2. **Closure without rescue.** When a line fails, it is closed. Period. No "what if we tried different parameters." This discipline is rare and invaluable.
3. **Scientific/economic separation.** The project correctly maintains that "scientifically supported" ≠ "tradeable." This distinction must be preserved.
4. **Provenance and identity.** SHA-256 verification of inputs, protocols, and implementations creates genuine reproducibility.

### Engineering infrastructure worth retaining:
1. **EventStudyRecorder** — well-designed, reusable execution recording
2. **SHA identity system** — genuine, battle-tested
3. **614-test baseline** — covers core contract boundaries
4. **M1 + tick data inventory** — real asset, already validated

### Research discipline producing trustworthy negative results:
- Every closure is justified by evidence, not opinion
- The closure firewalls prevent zombie research lines
- The historical record is honest about what was found and what wasn't

### Historical findings that remain useful:
- DISC-025's "entry must be the event" principle
- DISC-021's observed cost floor for XAGUSD (~9 bp RT)
- DISC-022's drift-control methodology
- The general lesson that 1-10 bp gross signals do not survive retail friction

---

## 13. What QuantForge Does Poorly

### CRITICAL

**1. Economic plausibility is checked too late.**

The ORD viability screen (`ORD_V1_1_0_ECONOMIC_VIABILITY_SCREEN_V1.md`) showed gross responses of 1.12-2.01 bp — obviously below any realistic friction floor — *before* the M-ORD-ECO staged infrastructure was built. The project then built a Parquet specification, a converter, a Stage-1 adapter, a Stage-1 executor, a Stage-2 executor, a Stage-3 verifier, a crash reconciliation system, and memory remediation code to confirm what the viability screen already showed.

**This is the single most expensive mistake in the program's history.** The staged infrastructure (9 milestones, ~64 governance documents, ~150 KB of code across `research/staged_execution/`) was unnecessary because the economic case was already dead.

**2. Candidate generation is too narrow.**

All six candidates are variations of: "detect a price-pattern event → trade in the event's direction → exit at fixed horizon." This is one strategy template. The program has not meaningfully explored:
- Cross-sectional effects (relative value between markets)
- Carry / term structure (not applicable to CFDs without modification)
- Multi-timescale interactions
- Volume-conditioned effects (volume data is reportedly unreliable)
- Calendar / seasonal patterns beyond session structure
- Volatility state transitions (as *trading signals*, not just scientific findings)
- Order flow / queue position effects

### HIGH

**3. Governance documentation overhead is disproportionate.**

The ORD line produced 64+ governance documents for a mechanism whose gross signal is 1-2 bp. The H01 Equity Track A produced 46+ documents including Norgate verification, NYA amendment proposals, source identity manifests, and multiple execution attempts. This documentation discipline is individually defensible but collectively excessive when applied to candidates that could have been killed earlier.

**4. Ping-pong audit/fix/re-audit cycles waste time.**

The ORD scientific execution went through: implementation audit V1.1 → corrections V1.1 → re-audit V1.1 → execution → crash → hard crash audit → memory remediation → memory remediation audit → resource root-cause review → legacy crash governance exception → execution invalidation governance review → fresh implementation audit V2 → fresh implementation audit V3 → final execution clearance → execution. This is ~15 documents and multiple code iterations for a single execution.

Root cause: **F — Multiple interacting causes.** The IDE agent generates code that frequently fails initial audit, requiring correction cycles. Protocol specifications are sometimes ambiguous, causing implementation divergence. And the governance process requires formal documentation of every intermediate state, multiplying the cost of each iteration.

### MEDIUM

**5. BOE runtime architecture is premature.**

The BOE core (`boe/` directory — 16 subdirectories, contracts, observers, evidence framework, deployment, risk, profile engine) was built before any research line produced a viable signal. It represents significant engineering investment in infrastructure that has never been used and may never be used if no tradeable edge is found. The `strategy/` directory contains dead code from the original mean-reversion conception.

---

## 14. Biggest Strategic Risk

> **QuantForge spends months building increasingly sophisticated validation and governance infrastructure while generating candidates from the same narrow mechanism family (intraday price-pattern events with fixed-horizon exits), all of which produce gross signals in the 1-10 bp range — below the friction floor of the available execution environment (retail MT5 CFDs).**

This is the scenario where the laboratory becomes self-justifying: each negative result is rigorously documented, the governance process works perfectly, the closures are all defensible, the infrastructure improves with each cycle — but no tradeable edge is found because the *candidate generation process* is looking in the wrong place.

The friction floor for retail CFD execution is approximately:
- XAUUSD: ~5-10 bp round-trip
- USATECHIDXUSD: ~2-5 bp round-trip
- XAGUSD: ~10-30 bp round-trip
- BTCUSD: ~10-20 bp round-trip

Any mechanism that produces <10 bp gross per trade is structurally unviable on this execution platform. Five consecutive candidates have produced signals in this range. The question is whether the data inventory *can* support discovery of larger effects, or whether the program needs different data, different markets, or different strategy templates.

---

## 15. Biggest Strategic Opportunity

**The research infrastructure and governance discipline are genuine assets that would be extremely valuable *if* applied to candidates with larger gross signals.**

Specifically:
1. The data inventory (42 GB of tick bid/ask data across 5 markets) has not been exploited for mechanisms beyond event-study-style patterns. Microstructure, volatility clustering, cross-market relationships, and multi-timescale effects remain unexplored.
2. The observed cost data is a real competitive advantage — it enables immediate economic plausibility screening for any new candidate, before building infrastructure.
3. The research methodology (pre-registered, Holm-corrected, exactly-once) is transferable to any candidate type.
4. The fast-kill model demonstrated by DISC-024 shows the research factory *can* be efficient when it doesn't over-engineer.

The opportunity is to combine the existing governance discipline with a **diversified candidate generation process** and a **hard economic plausibility gate before heavy infrastructure**.

---

## 16. Serious Chance of Eventual Tradeable Edge

**Assessment: MODERATE** — conditional on restructuring.

**Reasoning:**
- The data inventory is real and contains genuine market behavior
- Some of the scientific findings (sweep, ORD, H01 asymmetry) demonstrate real phenomena
- The governance system prevents false positives, which means a positive result, if ever found, would be trustworthy
- The program has demonstrated the ability to kill bad ideas — this is necessary for eventual success
- However, the 0/5 economic record after a focused search is a serious warning
- The mechanism space explored so far has been narrow
- Whether the friction floor of the execution platform is compatible with discoverable effects remains an open question

---

## 17. Required Research Factory Changes

**MINOR RESTRUCTURING — with one critical addition.**

### Change 1: Mandatory Economic Plausibility Gate (CRITICAL)

Before any candidate enters scientific definition lock, it must pass a **cheap economic plausibility check**:

> "Given observed friction for the target markets, what minimum gross signal size would make this candidate viable? Is there any reason to believe the mechanism can produce signals of that magnitude?"

For retail MT5 CFDs:
- Minimum viable gross per trade: ~15-20 bp (conservative)
- If the mechanism's expected gross is <15 bp based on prior evidence or structural reasoning, it is killed before scientific definition lock

This gate would have prevented the ORD staged infrastructure (gross ~1-2 bp was known early) and likely the H01 economic translation (daily-frequency volatility asymmetry → Q1/11-day trade is structurally unlikely to produce >15 bp per event).

### Change 2: Candidate Diversity Requirement (HIGH)

The next screening round must include candidates from at least 2 different strategy template families. The current template — "detect event → trade direction → exit at horizon" — has been tested 5 times and failed 5 times. Alternatives:

- **Mean-reverting within sessions** (not the closed DISC-021 z-score displacement, but e.g., statistical arbitrage between correlated pairs from the 5-market universe)
- **Volatility trading** (selling/buying realized volatility vs. a reference, using the tick data to construct realized vol estimators)
- **Multi-timescale** (daily signal → intraday execution, using both M1 and tick data)
- **Cross-market conditional** (one market's behavior conditions entry in another)

### Change 3: Infrastructure Budget Proportionality (HIGH)

Set an explicit governance rule:

> "No bespoke data pipeline, format conversion, or multi-stage execution system may be built for a candidate until: (a) the economic plausibility gate is passed with a gross signal estimate ≥2× the observed friction floor, AND (b) a cheap M1-only scientific screen shows a directionally positive result."

This prevents another ORD-scale infrastructure investment before economic viability is plausible.

---

## 18. Proposed Next Research Phase

```
Stage A — Candidate Generation (diverse)
    Generate ≥5 candidates from ≥3 different mechanism families
    Include at least one non-event-study template
    
    ↓

Stage B — Economic Plausibility Gate (HARD, CHEAP, FAST)
    For each candidate:
      What is the minimum gross signal for viability? (use observed friction data)
      Is there structural reason to expect that signal magnitude?
    Kill candidates below 15 bp expected gross immediately
    
    ↓

Stage C — Cheap Scientific Screen (M1 only, no infrastructure)
    Run a lightweight, M1-only, single-script pilot for surviving candidates
    No Parquet conversion, no staged execution, no multi-market tick streaming
    Question: "Is there a directionally positive signal AT ALL?"
    Kill candidates with no signal
    Budget: 1 session per candidate maximum
    
    ↓

Stage D — Scientific Definition Lock + Validation (existing governance)
    Full pre-registration for survivors
    Protocol audit → execution → adjudication
    Use existing EventStudyRecorder infrastructure
    
    ↓

Stage E — Economic Validation (only if scientific SUPPORT + gross ≥ 15 bp)
    Tick-level cost matching
    Dev/OOS splits
    Yearly evidence
    Full economic protocol — but ONLY for candidates that survived all prior gates
    
    ↓

Stage F — Strategy Construction
    Entry/exit/sizing rules from the validated economic result
    Paper-trading simulation
    
    ↓

Stage G — Bot Validation
    Connect to broker adapter
    Demo/paper execution
    Forward performance tracking
```

The key difference from current practice: **Stages B and C are explicitly designed to kill candidates cheaply.** The expensive infrastructure (Stages D-E) is reserved for candidates that have already demonstrated economic plausibility.

---

## 19. Bot Readiness Assessment

| Dimension | Status | Distance from Ready |
|---|---|---|
| **Research readiness** | Active — no viable edge found yet | FAR — 0/6 economic successes |
| **Strategy readiness** | Not started — no validated strategy exists | FAR — requires a positive economic result first |
| **Execution-engine readiness** | Contracts exist, no implementation | MODERATE — BOE pipeline is designed but needs a detector |
| **Bot-engineering readiness** | MT5 adapter exists, untested in research context | FAR — broker integration is skeletal |
| **Production readiness** | Not applicable | VERY FAR — no monitoring, no risk management, no failover |

**Honest assessment: The bot is not close.** The project is at Phase 1 of a multi-phase journey, and Phase 1 (finding a viable edge) has not yet produced a positive result. The BOE runtime architecture, while well-designed, is premature — it was built for a research program that hasn't yet found what to detect.

---

## 20. Program Scorecard

| Dimension | Rating | Explanation |
|---|---|---|
| **Program Scientific Quality** | **Strong** | Pre-registered protocols, dependence-aware inference, Holm correction, clean negative controls, honest reporting of negatives. The scientific methodology would pass academic peer review. |
| **Program Engineering Quality** | **Fair** | Good contract design and test coverage; excessive research script monoliths; premature runtime architecture; bespoke infrastructure that doesn't generalize; memory/crash issues during execution. |
| **Research Efficiency** | **Poor** | 6 lines, 0 economic successes, hundreds of governance documents, massive infrastructure for candidates with <10 bp gross signals. DISC-024 shows it CAN be efficient; the overall record shows it usually isn't. |
| **Economic Realism** | **Fair to Strong** | Observed cost data is genuine; cost sensitivity analysis is thorough; the economic testing *when applied* is rigorous. The weakness is applying it too late — after heavy infrastructure is already built. |
| **Probability of Eventual Tradeable Edge** | **Moderate** | Conditional on restructuring the research factory. With the current approach (narrow candidate generation + late economic gate), the probability is lower. With diversified candidates and early economic screening, it is credibly moderate. Cannot responsibly estimate higher given the 0/5 record. |

---

## 21. Owner-Level Recommendation

### "Should I continue investing serious time and resources into QuantForge?"

**YES — but with three immediate changes.**

### 1. Does QuantForge currently have a credible path to a tradeable strategy?

**Yes, but the current path is inefficient.** The scientific methodology and governance are strong foundations. The data inventory is genuine. The ability to kill bad ideas prevents wasted investment in false positives. However, the candidate generation and economic screening processes need restructuring to avoid spending months on candidates with <10 bp gross signals.

### 2. Does the research factory need restructuring?

**MINOR RESTRUCTURING — not fundamental redesign.** The core governance (pre-registration, closure discipline, provenance) must be retained. The changes needed are:
- Add a mandatory cheap economic plausibility gate before scientific definition lock
- Diversify candidate generation beyond the current event-study-with-fixed-horizon template
- Set infrastructure budget proportionality rules

### 3. The three most important changes

1. **INSTALL AN ECONOMIC PLAUSIBILITY GATE BEFORE DEFINITION LOCK.** Any candidate with expected gross <15 bp on the target markets is killed immediately, before any infrastructure is built. Use the existing observed cost data to set this threshold. This single change would have prevented the ORD staged infrastructure (~7 days of work).

2. **DIVERSIFY CANDIDATE GENERATION.** The next screening must include candidates from at least 3 different mechanism families. The "event → direction → fixed horizon" template has been tested 5 times and failed 5 times. Explore multi-timescale, cross-market, volatility-state, and structural-relationship mechanisms.

3. **SET A "CHEAP PILOT" REQUIREMENT BEFORE HEAVY INFRASTRUCTURE.** Before building any bespoke data pipeline, format conversion, or staged execution system, a candidate must show a directionally positive signal in a single-script, M1-only, no-infrastructure pilot. This takes one session, not seven.

### 4. What must NOT be changed

- **Pre-registration before execution.** Never compromise this.
- **Closure without rescue.** Never weaken the firewalls.
- **Scientific/economic separation.** Never blur these categories.
- **SHA identity and provenance.** This is genuine infrastructure.
- **Honest reporting of negative results.** This is the program's intellectual integrity.

### 5. What the next research phase should accomplish

The next phase should **screen 5+ diverse candidates**, apply the economic plausibility gate to each, run cheap pilots on survivors, and enter full governance only for candidates that show both directional signal AND economic plausibility. The goal is to kill 80% of candidates in <1 session each and invest heavily only in the 20% that have a genuine chance.

### 6. What evidence would cause me to conclude that QuantForge should be abandoned or fundamentally redesigned

- **3 more diverse candidates fail at the economic plausibility gate** (i.e., even candidates from different mechanism families cannot produce >15 bp gross signals in this data). This would suggest the friction floor of the MT5 CFD execution platform is incompatible with the effects discoverable in the available data.
- **The data inventory is exhausted** (all reasonable mechanisms have been tested on all 5 markets with no positive result). This would require either new data sources or a fundamental rethinking of the approach.
- **The governance overhead becomes self-defeating** (each candidate requires >50 governance documents regardless of merit). This would suggest the process needs simplification, not the science.

---

## 22. Hard Conclusions

1. **QuantForge has built a world-class scientific research laboratory.** The provenance, reproducibility, pre-registration, and closure discipline are genuine strengths that would survive external scrutiny.

2. **QuantForge has not yet built an efficient machine for discovering profitable strategies.** The 0/5 economic record, narrow candidate generation, and late economic screening demonstrate this clearly.

3. **The biggest mistake was building the ORD staged infrastructure after the viability screen showed 1-2 bp gross.** This was ~7 days of engineering for a predictable negative outcome.

4. **The biggest opportunity is to apply the existing governance discipline to a diversified candidate set with early economic gates.** The infrastructure and methodology are ready; the candidate generation process is the bottleneck.

5. **The bot is not close.** No viable edge has been found. The BOE runtime is premature but well-designed. The path to a bot requires finding a positive economic result first — everything else follows from that.

6. **The program should continue — but it must stop treating scientific support as a reliable predictor of economic viability.** These are different questions, and the research factory must answer the economic question early and cheaply before investing in heavy infrastructure.

7. **The single most important change: install an economic plausibility gate that kills candidates with <15 bp expected gross before any infrastructure is built.** This is the highest-leverage intervention available.

---

*Audit complete. No files modified. No experiments run. No candidates selected. No governance documents changed. No code committed.*
