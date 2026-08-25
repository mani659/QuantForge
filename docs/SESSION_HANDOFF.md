# QuantForge — Session Handoff (Authoritative)

**Purpose:** authoritative snapshot for the next session. Originally established at the point **Strategy Assembly V1 was declared FROZEN** (2026-08-12); updated 2026-08-13 after TSMOM V2 execution/adjudication and closure; **updated 2026-08-16 after the H01 volatility-response program and the H01 Equity V1 execution + independent adjudication**. Do not reconstruct project state from conversational memory; start from this document and the referenced records.

---

## 0. Start Here Next Session

> **START HERE NEXT SESSION**
>
> ## Required next-session reading
> 1. `docs/SESSION_HANDOFF.md`
> 2. `output/research_discovery/QUANTFORGE_RESEARCH_FACTORY_V2.md`
> 3. `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V3.md`
> 4. `output/research_discovery/RESEARCH_FACTORY_V2_SCREEN_G0_G1_G2_20260824.md`
>
> ## Explicit prohibitions
> Next session must NOT:
> * rescue CAND-001;
> * rescue CAND-002;
> * rescue CAND-003;
> * reopen DISC-021–DISC-026;
> * jump directly to G3;
> * jump directly to production tick infrastructure.
>
> ## Current Milestone
> **TRADEABLE EDGE DISCOVERY SCREENING**
>
> ## Operating Doctrine
> **Economic-First Discovery + Conditional Market Behavior**
>
> ## Last Screening
> 2026-08-24 G0→G1→G2 screening:
> 3 candidates screened, 0 promoted.
>
> ## Next Action
> **G0 CANDIDATE GENERATION**
>
> Future candidates should focus on repeatable market events/states and the conditional directional response following executable entry, including investigation of the market-state/KPI conditions that influence that response.
>
> The first 2026-08-25 G1 attempt was invalidated due to executable-capture, deterministic-exit, proxy-substitution, and undocumented-downsampling defects. No G2 execution occurred. The G1 contract has now been hardened to require executable entry, deterministic exit, post-entry-only measurement, exact candidate-definition adherence, and explicit prohibition of MFE/proxy/down-sampling substitutions. Do NOT automatically rerun the four invalid candidates.
>
> ### HISTORICAL / CLOSED
>
> - DISC-021
> - DISC-022
> - DISC-023
> - DISC-024
> - DISC-025
> - DISC-026 XAGUSD economic translation — CLOSED
>
> ### ACTIVE
>
> - None

---

## 1. Repository State

- **HEAD / freeze commit:** `b67a3cc` — `feat: implement strategy packaging, admission controller, and deployment updates`
- **Branch:** `main` (linear history, no tags)
- **Freeze date:** 2026-08-12 (unchanged — no new freeze commit since)
- **Worktree (uncommitted additions since freeze):**
  - Modified (pre-existing, agent state): `.freebuff/desktop-v2.db{-shm,-wal}`
  - Modified (governance/docs, uncommitted): `docs/CHANGELOG.md`, `docs/PHASE7_FREEZE_APPROVED.md`, `docs/ARCHITECTURE.md`, `docs/CONSTITUTION_v1.0.md`, `docs/ROADMAP.md`, `README.md`, `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md`, `research/knowledge/RESEARCH_TIMELINE.md`
  - Created (uncommitted): `docs/CONSTITUTIONAL_AMENDMENT_AMEND-1.md`, `docs/SESSION_HANDOFF.md`, `output/` (all research artifacts: `event_study_v1..v3/`, `xagusd_cost_viability_v1/`, `tsmom_v1/` — see §13)
  - No source code, tests, or contracts modified by any research task since the freeze.

## 2. Milestone Frozen

**STRATEGY ASSEMBLY V1 — FROZEN** (2026-08-12).

Frozen boundaries of this milestone:
- Admission boundary (`assembly/admission/AdmissionController`)
- Package-consumption boundary (`ValidatedStrategyPackage` consumption)
- Research-semantics firewall
- Fail-closed dependency boundary (`DependencyFactory` → `DependencyAdmissionError`)
- Deployment-artifact construction boundary
- AMEND-1 governance incorporated

No further Assembly expansion without a new architectural decision.

## 3. Governance — Constitutional Amendment AMEND-1

- **Status:** APPROVED — RATIFIED (owner approval, 2026-08-12), per Constitution v1.0 §8.
- **Record:** `docs/CONSTITUTIONAL_AMENDMENT_AMEND-1.md`.
- **Scope (exactly two items):**
  - **A — DeploymentOrchestrator:** may retain coordination references to, and lifecycle decisions for, Behavioural-Reality-owned observation windows across calls.
  - **B — DeploymentDependencies:** `observation_policy: ObservationPolicyContract` authorized as a required injected dependency, threaded through `DeploymentBootstrap`, consumed only at the observation-window boundary.
- **Procedural irregularity (preserved):** implementation in `b67a3cc` preceded approval; AMEND-1 regularizes prospectively.

## 4. Amended Deployment Boundary

> **Behavioural Reality owns behavioural history.** Deployment may coordinate the lifecycle of Behavioural-Reality-owned observation state across multiple snapshots. Deployment does not become the owner of behavioural history and does not define behavioural science.

Still prohibited: Deployment owning behavioural history; accumulating `BehaviorFrame`s; detector science; recoil/persistence semantics; inventing thresholds; reconstructing research semantics; arbitrary mutable deployment state unrelated to coordination; modification of any other frozen contract without a constitutional amendment.

## 5. Frozen Architectural Boundaries

`boe/execution/**`, `boe/deployment/**` (as amended by AMEND-1), `boe/temporal/**`, `boe/evidence/**`, `boe/observation/**` contracts, `boe/behavior_detector_contract.py`, `boe/behavior_observation.py`, `boe/observation_environment.py`, `research/lifecycle/**`, `research/engine/run_engine.py`, `research/experiment_recorder.py`, `research/dataset/**`, `research/analytics/**`, `research/packaging/**`. Verified untouched by the `b67a3cc` milestone, by the freeze task, and by all subsequent research tasks (TSMOM V1 included).

## 6. Test Baseline (last known verified baseline)

- `python -m pytest tests/ -q` → **614 passed** (verified at freeze point)
- `python -m pytest tests/ -q -W error` → **614 passed** (verified at freeze point)
- Admission/assembly/packager subset → **29 passed** (verified at freeze point)

No test suite was run or modified by the TSMOM V1 execution; the freeze-point baseline remains the last known regression state. Do not claim additional test results from TSMOM execution unless explicitly recorded in the experiment artifacts.

## 7. Research-Semantics Firewall

PASS. No z-score, momentum, recoil, persistence, ATR, threshold, detector-scoring, or signal-definition semantics exist in `assembly/**` or `boe/deployment/**`. `config/recoil_rules.json` is not referenced by the runtime path. `behavior_strength` remains the categorical token defined by the frozen `BehaviorFrame` contract. TSMOM V1 and V2 produced research evidence only; nothing crossed into runtime.

## 8. TSMOM V1 — Executed Result (historical record)

**Time-Series Momentum / Trend-Following V1: EXECUTED — Scientific INCONCLUSIVE / Economic NOT CONFIRMED.**

- Protocol: `output/tsmom_v1/EVENT_STUDY_PROTOCOL_TSMOM_V1.md` **v1.0.3** (frozen, unchanged during execution; SHA-256 `2d60cb71…292c5`).
- Execution authorized by the final v1.0.2 pre-execution audit (PASS) and the v1.0.3 economic accounting audit (PASS).
- **Adjudicated by V2 (see §10a).** The continuation question is now RESOLVED: the line is CLOSED (DISC-022).

### Primary F1 (TRAIN+VALIDATION, T = 50, 39 blocks, B = 10,000, L = 12)
- Gross mean ≈ **+1.51% / month**; 95% CI ≈ **[−2.53%, +4.54%]**; one-sided p ≈ **0.2375** — CI includes zero.
- Net mean ≈ +1.48% / month; 95% CI ≈ [−2.58%, +4.52%]; p ≈ 0.2436.

### F2 TEST (2025-09..2026-07, T = 11, single pre-authorized use)
- Gross ≈ **+6.70% / month**, positive sign; exact sign-flip one-sided p ≈ **0.1274**; Holm-adjusted p ≈ **0.2549**.
- Net ≈ +6.68% / month, p ≈ 0.1274. TEST is corroborative only.

### Economic layer
- Economic classification: **NOT CONFIRMED** (registered gate: F1 gross CI includes 0).
- Pooled break-even one-way cost ≈ **140 bp**; observed pooled median one-way half-spread ≈ **3.24 bp** (bid/ask cost-match coverage 100%, 166/166 legs).
- **Cost is therefore NOT the limiting factor** — this is the opposite failure mode from the Mean-Reversion closure.

### Scientific classification
**INCONCLUSIVE** — F1 confirmatory CI includes zero; F2 not significant after Holm; effective independent signal count is low (per-market signal runs 1–7; pooled flips 21); the formal NC2 control produced a stronger significant association (see §9). No UNRESOLVED trigger fires (flips 21 ≥ 15, coverage 100%, pooled N 219 ≥ 30).

## 9. NC2 Critical Finding (V1 — resolved by V2)

The **NC2 formal negative control** (6-month time-shifted signal) produced:

- mean ≈ **+3.93% / month**
- 95% CI ≈ **[+0.69%, +7.45%]** (excludes zero)
- one-sided p ≈ **0.0079**

**This was stronger than the V1 primary confirmatory result**, so V1 could not cleanly attribute its positive point estimates to the registered "12-month signal → next-month continuation" mechanism. The leading alternative — **persistent market drift / long-biased regime composition** — motivated the V2 drift-controlled design. **Resolution:** V2 replaced the contaminated NC2 with the same-universe all-long drift benchmark and three clean negative controls (NC1 paired direction rotation, NC3 24-month lag, NC4 calendar-block null); see §10a.

## 10. Market Composition Finding

- XAUUSD strongly positive (mean ≈ +6.1%/month, Sharpe ≈ 1.17, 40 long / 8 short).
- USATECHIDXUSD = **22/22 long-biased observations** (Sharpe ≈ 1.40).
- EURUSD negative (mean ≈ −2.0%/month, Sharpe ≈ −0.57).
- Positive pooled performance is **heterogeneous**; the sample may contain strong persistent upward market regimes (gold, tech index).

> This is a scientific interpretation question for the next audit, not a conclusion that the strategy is invalid.

No market may be removed, reweighted, or selectively excluded.

## 10a. TSMOM V2 — Executed Result (drift-controlled; adjudicated)

**TSMOM V2: EXECUTED — Scientific PARTIALLY REPRODUCED / NOT PROMOTABLE / line CLOSED (DISC-022).**

- Protocol: `output/tsmom_v2/EVENT_STUDY_PROTOCOL_TSMOM_V2_DRIFT_CONTROL.md` **v2.0.0** (frozen, unchanged during execution; SHA-256 `e9aa9465…c493d`).
- Question: does the fixed 12/1 TSMOM signal add incremental value **above a same-universe, same-weight all-long drift benchmark**?
- Scientific object: `ΔΠ(m) = Π_tsmom(m) − Π_long(m)` — NOT absolute TSMOM return.

### Historical Layer A (28-market HPD panel, common window 1987-01-13 → 2002-08-30, 175 position months, 4,900 market-months, 552 pooled flips)
- **F1** (TRAIN+VALIDATION, T = 148, L = 12, B = 10,000, seed 20260813): incremental `ΔΠ` mean ≈ **+0.67% / month**; 95% CI ≈ **[+0.03%, +1.54%]** (lower bound positive); one-sided p ≈ **0.019**; **Holm-adjusted p ≈ 0.038** (family {F1, Layer-B}, α = 0.05) — passes.
  - Π_tsmom ≈ +1.39%/month; Π_long (drift benchmark) ≈ +0.71%/month; long exposure ≈ 53%.
- **Breadth:** 21/28 markets positive by mean incremental; all leave-one-market-out values positive; all leave-one-class-out values positive (only Rates and Equity index negative by class mean).
- **Negative controls (all clean):** NC1 (paired direction rotation) fraction-null-≥-observed ≈ 0.0001; NC3 (24-month lag shift) effect negative, no persistence beyond construction horizon; NC4 (calendar-block null) ≈ 0.037.
- **F2** (historical TEST, T = 27, single authorized use, seed = F1 seed): `ΔΠ` ≈ +0.34%/month, positive direction, CI includes zero, p ≈ 0.120 — corroborative only.

### Contemporary Layer B (5 markets, 2021–2026, T = 54, 219 assessments, seed 20260814)
- Incremental `ΔΠ` mean ≈ **−1.10% / month** (net of observed MT5 costs ≈ −1.11%); 95% CI ≈ [−5.70%, +0.09%]; one-sided p ≈ 0.971.
- All-long benchmark ≈ **+3.02%/month** (CI excluding zero, p ≈ 0.001) — the drift book dominates; TSMOM underperforms the all-long book.
- **Direction is OPPOSITE the historical Layer A.**

### Promotion gate (frozen §19, all 8 conditions)
- Conditions 1–7 **PASS** (F1 mean ΔΠ > 0; F1 CI LB > 0; Holm p < 0.05; positive vs all-long; not single-market; not single-class; survives controls).
- **Condition 8 — contemporary directional consistency — FAILS** (historical +0.67% vs contemporary −1.10%).
- **Final: NOT PROMOTABLE / TSMOM REMAINS UNRESOLVED; scientific classification = PARTIALLY REPRODUCED.**

### Economics
- Historical HPD cost: **UNOBSERVED** (no fabricated spreads; sensitivity bands {0,5,10,20,50} bp labelled ASSUMPTION; net stays positive at 50 bp). Historical economics **UNRESOLVED by design**.
- Contemporary: observed MT5 half-spreads (Option-A accounting); net CI LB < 0 → **NOT CONFIRMED**.
- Economics are NOT the primary closure reason — the decisive problem is **no stable incremental signal across eras**.

### Artifacts
All under `output/tsmom_v2/`: protocol, `run_tsmom_v2.py`, `experiment_metadata_TSMOM_V2.json`, `assessment_events_TSMOM_V2.csv`, `incremental_monthly_TSMOM_V2.csv`, `bootstrap_TSMOM_V2.csv`, `negative_controls_TSMOM_V2.csv`, `cost_analysis_TSMOM_V2.csv`, `results_TSMOM_V2.json` (+ `.build_cache/`). `SCIENTIFIC_REPORT_TSMOM_V2.md` was not produced at execution (terminal print crash after artifacts were written); the audit confirmed computation state complete and reporting state incomplete, and the closure documentation preserves the result. During the final TSMOM closure task the V2 scientific report was reconstructed from persisted artifacts only (no recomputation, no new inference; see the report's reconstruction notice). TEST consumed exactly once; no rerun; no methodology changed after results.

## 11. Current Research Status

**Research Factory: ACTIVE — ORD ECONOMIC TRANSLATION.**

- Mean Reversion: **CLOSED — ECONOMICALLY NON-VIABLE** (DISC-021).
- Fixed 12/1 TSMOM candidate: **CLOSED — NOT PROMOTABLE** (DISC-022).
- H01 broad universal formulation: **NOT ESTABLISHED / closed in that form** (v1.1 invalid inference; v1.2 corrected + adjudicated; universal claim not supported). H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / UNADJUDICATED.
- **H01 Equity Track A (DISC-023): CLOSED — ECONOMIC FAILURE.**
- **Session-Anchored Range Expansion (DISC-024): CLOSED — CONTRADICTED.**
- **Liquidity Sweep / Reversal (DISC-025): CLOSED — ECONOMIC TRANSLATION NON-VIABLE.**
- **Opening Range Breakout (ORD / DISC-026):** SCIENTIFICALLY SUPPORTED — ECONOMIC TRANSLATION CLOSED AS NON-VIABLE FOR REGISTERED XAGUSD OBJECT.
  - ORD economic stage: CLOSED FOR XAGUSD.
- The next task is **TRADEABLE EDGE DISCOVERY SCREENING**. A new candidate may be screened under the Research Factory governance.

## 12. Current Blockers

### BOE / Detector
Still **DESIGN BLOCKED** — no runtime detector implementation is authorized. The scientific specification for the previously considered Mean-Reversion detector was never established, and that research line is closed. Do NOT revive Mean Reversion through another experiment.

### TSMOM
**CLOSED** — not a runtime candidate. No TSMOM detector, runtime configuration, or V3 continuation may be created. The line is preserved as a negative/boundary result (DISC-022).

## 13. TSMOM Artifacts

### V1 — all under `output/tsmom_v1/` (do not delete or alter)

- `EVENT_STUDY_PROTOCOL_TSMOM_V1.md` — approved protocol **v1.0.3**, byte-for-byte unchanged during execution
- `run_tsmom_v1.py` — deterministic execution script (replayable)
- `experiment_metadata_TSMOM_V1.json` — fingerprints, versions, seeds, row counts
- `daily_series_TSMOM_V1.csv` — M1 → daily aggregation
- `assessment_events_TSMOM_V1.csv` — 219 monthly assessments, signals, weights, costs, partitions
- `cost_match_TSMOM_V1.csv` — quote matches (166/166 legs, 100% coverage)
- `bootstrap_TSMOM_V1.csv` — 20,000 F1 replicate means (gross + net)
- `spread_distributions_TSMOM_V1.csv` — rebalance-timestamp half-spread percentiles (4 bid/ask markets)
- `net_sensitivity_TSMOM_V1.csv` — E8/E10 cost bands
- `results_TSMOM_V1.json` — full machine-readable results
- `SCIENTIFIC_REPORT_TSMOM_V1.md` — the experiment report
- `.build_cache/` — intermediate deterministic caches

### V2 — all under `output/tsmom_v2/` (do not delete or alter)

- `EVENT_STUDY_PROTOCOL_TSMOM_V2_DRIFT_CONTROL.md` — frozen protocol **v2.0.0**, unchanged
- `run_tsmom_v2.py` — deterministic execution script (replayable)
- `experiment_metadata_TSMOM_V2.json` — fingerprints, versions, seeds, hashes
- `assessment_events_TSMOM_V2.csv` — 5,119 events (Layer A 4,900 + Layer B 219)
- `incremental_monthly_TSMOM_V2.csv` — monthly Π_tsmom / Π_long / ΔΠ (229 rows)
- `bootstrap_TSMOM_V2.csv` — 60,000 replicate means (F1/F2/Layer-B gross + Layer-B net)
- `negative_controls_TSMOM_V2.csv` — NC1/NC3/NC4 results
- `cost_analysis_TSMOM_V2.csv` — historical assumption bands + contemporary EURUSD sensitivity
- `results_TSMOM_V2.json` — full machine-readable results
- `SCIENTIFIC_REPORT_TSMOM_V2.md` — V2 scientific report (reconstructed during the final TSMOM closure task from persisted artifacts only; no recomputation)
- `.build_cache/` — execution cache

Recorded: V2 computation completed and wrote all result artifacts before the terminal print crash (reporting state incomplete); the read-only adjudication audit verified protocol integrity, source/inverse fingerprints, internal consistency, TEST consumed exactly once, and no methodology change after results. The scientific report was reconstructed after the audit from persisted numbers only.

## 13a. H01 Volatility-Response Line → H01 Equity V1 (executed & adjudicated)

### Broad H01 formulation — NOT ESTABLISHED / closed in that form

- H01 v1.1 registered inference was invalid (D_obs-centered bootstrap p ≈ 1 by construction); H01 v1.2 corrected the null construction (null-imposing recentered bootstrap, protocol v1.2.0) and was executed + independently adjudicated: the universal cross-asset claim was **not supported**; COMMODITIES_OTHER produced a formal contradiction of its registered inverse prior; equity observations (`sp`, `USATECHIDXUSD`) were classic-direction but **EVIDENCE-LIMITED** (one evaluable market per layer).
- **H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / SCIENTIFIC RESULT UNADJUDICATED.** No v1.1 p-value is used anywhere; no v1.2 result is merged with the Equity V1 result.

### H01 Equity V1 — EXECUTED and ADJUDICATED (Scientific + Economic)

- **Scientific Result:** Strongly SUPPORTED in the tested US-tech exposure. Replicates across two eras (strong cross-era replication = TRUE). 
- **Economic Translation (Q1 / 11-day):** Executed exactly once (`H01_ECONOMIC_V1_EXEC_04`). The translation failed the mandatory dual-era stability gate. It produced negative returns across all market segments in the Historical era (FAIL: Δ = -0.00143921) and uniformly positive returns in the Contemporary era (PASS: Δ = +0.00077702). Overall: **ECONOMIC FAILURE**.
- **Track A status: CLOSED — ECONOMIC FAILURE (2026-08-23).** The historical/contemporary divergence must be preserved exactly as evidence. The failure of the economic translation does not invalidate the H01 scientific finding. 
- **Strongest surviving claim:** classic volatility-response asymmetry is strongly supported in the tested US-tech exposure and replicates across two eras.
- **Economic conclusion:** The registered Q1/11-day translation is not a stable cross-era economic edge.
- **Governance firewall:** no reopening of H01 Equity Track A; no reinterpretation of the scientific SUPPORT results; no rescue translation; no contemporary-only strategy; no threshold search; no horizon search; no trading strategy from H01; no BOE semantics; no reopening of any closed line.
- **Key artifacts:** `output/research_discovery/H01_EQUITY_V1_SCIENTIFIC_ADJUDICATION.md`, `output/research_discovery/H01_ECONOMIC_V1_EXEC_04`, scientific artifacts under `H01_EQUITY_VOLATILITY_ASYMMETRY/`, the Track-A chain; DISC-023.

## 14. Governance / Architecture Position

- AMEND-1 ratified 2026-08-12.
- Strategy Assembly V1 frozen.
- Deployment boundary as amended by AMEND-1.
- **No constitutional amendment is pending from TSMOM research.** Both TSMOM lines closed as research findings only; nothing crossed into runtime.
- Research remains separated from runtime.

## 15. Current Project Position

- **COMPLETED / FROZEN:** BOE Core Phases 1–6; Phase 7 Deployment Layer (incl. AMEND-1-ratified temporal orchestration); Phase 8 Research Industrialization; Phase 9 Operational Governance; Experiment Orchestration V1; Research Execution Context V1; Dataset Foundation V1; Scientific Hypothesis Evaluator V1; Validated Strategy Packaging V1; **Strategy Assembly V1**.
- **QuantForge engine:** COMPLETE / FROZEN.
- **Strategy Assembly V1:** FROZEN (AMEND-1 ratified 2026-08-12); must not be expanded without a new architectural decision.
- **Mean-Reversion research line:** CLOSED — ECONOMICALLY NON-VIABLE (DISC-021). No detector promoted; no BOE runtime semantics created.
- **Fixed 12/1 TSMOM research line:** CLOSED — NOT PROMOTABLE (DISC-022). V1 = Scientific INCONCLUSIVE / Economic NOT CONFIRMED; V2 historical = positive incremental (F1 ΔΠ ≈ +0.67%/mo, Holm p ≈ 0.038); V2 contemporary = negative incremental (ΔΠ ≈ −1.10%/mo); final classification = PARTIALLY REPRODUCED; promotion = FAILED (7/8, Condition 8 cross-era consistency failed); candidate CLOSED. No detector promoted; no runtime semantics created; TEST consumed once.
- **H01 broad universal formulation:** NOT ESTABLISHED / closed in that form (v1.1 invalid inference; v1.2 corrected and adjudicated; universal claim not supported). H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / UNADJUDICATED.
- **H01 Equity Track A (DISC-023):** CLOSED — ECONOMIC FAILURE.
- **Session-Anchored Range Expansion (DISC-024):** CLOSED — CONTRADICTED.
- **Liquidity Sweep / Reversal (DISC-025):** CLOSED — ECONOMIC TRANSLATION NON-VIABLE.
- **Opening Range Breakout (ORD / DISC-026):** SCIENTIFICALLY SUPPORTED — ECONOMIC TRANSLATION CLOSED AS NON-VIABLE FOR REGISTERED XAGUSD OBJECT.
- **CURRENT MILESTONE:** TRADEABLE EDGE DISCOVERY SCREENING.
- **CRITICAL PATH / BLOCKER:** None.
- **NEXT LEGITIMATE TASK:** **RETURN TO G0 CANDIDATE GENERATION**. The first 2026-08-25 G1 attempt was invalidated due to executable-capture, deterministic-exit, proxy-substitution, and undocumented-downsampling defects. No G2 execution occurred. G1 contract has now been hardened to require executable entry, deterministic exit, post-entry-only measurement, exact candidate-definition adherence, and explicit prohibition of MFE/proxy/down-sampling substitutions. Do NOT automatically rerun the four invalid candidates.

## 16. Explicitly Forbidden Work

TSMOM (permanently, line closed):

- TSMOM V3 or any further 12/1 variant;
- changing lookback, horizon, volatility rules, weighting, or market universe for 12/1;
- parameter tuning / lookback search on the closed candidate;
- market selection or regime filtering on the closed candidate;
- using the consumed TEST again;
- creating a BOE TSMOM detector;
- claiming the closed candidate is promotable.

Also still forbidden (from the freeze): detector implementation; observer implementation; recoil/persistence/z-score/momentum/ATR threshold invention; modification of detector/observation/evidence/temporal/lifecycle contracts; observer registry expansion; fingerprint expansion; serialization; broker/live integration; portfolio logic; Research Factory automation; reopening frozen milestones; speculative refactoring; any Strategy Assembly expansion; reopening Mean Reversion.

H01 Equity Track A (permanently, line closed — ECONOMIC FAILURE):

- reopening H01 Equity Track A;
- modifying H01 methodology to rescue the translation;
- parameter tuning, threshold searching, or post-hoc market selection;
- creating a trading strategy from H01 results;
- creating BOE semantics from H01;
- merging H01 with other research lines.

## 17. Read-Only / Integrity Statement

- TSMOM V1 and V2 executions were research-output-only: all changes are additions under `output/tsmom_v1/` and `output/tsmom_v2/`; both frozen protocols were never modified; TEST was consumed exactly once (V2) with no rerun and no post-result method change; no source, test, contract, configuration, or governance file was changed by any research task.
- The V2 result was adjudicated by a strict read-only audit and is recorded here and as DISC-022; historical records (DISC-001..021, V1 report, both protocols) were not rewritten. Historical documents retain their original claims; V1's NC2 anomaly is recorded as historically true and resolved by V2's drift-controlled design.
- The missing V2 scientific report was reconstructed during the final TSMOM closure task from persisted artifacts only (no recomputation, no new inference), and is recorded with an explicit reconstruction notice; this is a documentation completion, not a protocol change.
- This handoff update is a state snapshot reflecting the closure of both research lines, not a replacement for historical records.

---

*Authoritative for the next session. Headers: Start Here · Repository State · Milestone Frozen · Governance · Boundary · Frozen Boundaries · Test Baseline · Firewall · TSMOM V1 Result · NC2 Finding · Market Composition · TSMOM V2 Result · Research Status · Blockers · TSMOM Artifacts · H01 Equity V1 · Governance Position · Project Position · Forbidden · Integrity.*
