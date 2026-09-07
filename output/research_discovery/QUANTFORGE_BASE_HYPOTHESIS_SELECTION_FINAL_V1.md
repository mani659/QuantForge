# QUANTFORGE — BASE HYPOTHESIS SELECTION FINAL V1

**Milestone:** Base Hypothesis Selection — F-01 / F-02 / F-03 governed review under ratified BS1–BS13
**Status:** SELECTION COMPLETE — **ONE HYPOTHESIS SELECTED (F-01)** — state is **SELECTED BASE HYPOTHESIS — V38A REGISTRATION REQUIRED**; NOT a Base, NOT validated, NOT Registry-eligible
**Parent governance:** V38 (RATIFIED); V38A (RATIFIED, BV1–BV13); BS1–BS13 (RATIFIED); BF1–BF13 (RATIFIED); Outcome-Blind Formulation Cycle V1 (COMPLETE, SHA `655473e2a863`)
**SESSION_HANDOFF intentionally NOT modified** (selection milestone).

Label conventions: GOVERNANCE FACT / SELECTION REVIEW / SELECTED BASE HYPOTHESIS — V38A REGISTRATION REQUIRED / DEFERRED / REJECTED / NOT PERMITTED / AUDIT.

---

## 1. EXECUTIVE SELECTION VERDICT

**ONE HYPOTHESIS SELECTED: F-01 — Session-Partition Reference Process (Overnight Exposure Leg).**

F-01 is the most defensible first Base hypothesis for QuantForge to enter V38A registration: it is the cleanest legitimate reference decision process among the three formulated candidates — zero free parameters, single declared instrument class, one decision per trading day, transparent single-leg execution, and a decision architecture (session partition) never before tested in this repository.

F-02 and F-03 are **DEFERRED for the first slot** — legitimate, complete, outcome-blind formulations with no affirmative blocker, but carrying unresolved scope/execution surfaces (pair identity underdetermination; daily full-turnover cost structure) that make them less defensible as the *first* reference. They remain SELECTABLE in a later review once those surfaces are resolved.

The selection rationale is architectural, not economic: **no historical outcome was consulted, no economics were computed, no performance ranking occurred.** The state of F-01 is **SELECTED BASE HYPOTHESIS** — it is not a Base, it is not V38A-validated, and it is not Registry-eligible. **OWNER AUTHORIZATION IS REQUIRED to enter V38A registration.** The Base Registry remains EMPTY.

## 2. GOVERNANCE STATE

(GOVERNANCE FACT) Verified at selection:

- V38 = RATIFIED (`c42c3c3`); V38A = RATIFIED (`4da500b`); BS1–BS13 = RATIFIED (`9a2492f`); BF1–BF13 = RATIFIED (`4edbfdb`).
- Formulation cycle = COMPLETE (`QUANTFORGE_OUTCOME_BLIND_BASE_FORMULATION_CYCLE_V1.md`, SHA `655473e2a863`): F-01 / F-02 / F-03 exist as FORMULATED HYPOTHESES — NOT SELECTED.
- BH-01 = WITHDRAWN; H01 = CLOSED; ORD = CLOSED; TRADEABLE_EDGE family exhausted; CAND-077/081/083/099 remain observations; CAND-015/024/035 protected-forward and excluded.
- Base Registry = **EMPTY**; no Base exists; no hypothesis was selected prior to this review.
- HEAD `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`, branch `main`.

## 3. AUTHORITATIVE SOURCES

1. `docs/SESSION_HANDOFF.md`
2. V38 ratification; V38A design + ratification (BV1–BV13)
3. Base Hypothesis Selection / Validation Design + ratification (BS1–BS13)
4. Outcome-Blind Formulation Design + ratification (BF1–BF13)
5. `QUANTFORGE_OUTCOME_BLIND_BASE_FORMULATION_CYCLE_V1.md` (F-01/F-02/F-03 full packages)
6. `QUANTFORGE_BASE_HYPOTHESIS_SELECTION_RECOMMENDATION_V1.md` (V1-r2, BH-01 withdrawal — the governing precedent)
7. G1 V3 ratification; V34 Mechanism–Observable Challenge
8. V27–V37 closure/adjudication records; H01 records (`H01_ECONOMIC_TRANSLATION_INPUT_MANIFEST_V1.md` six-series archive); ORD records; TRADEABLE_EDGE records; CAND-075 record
9. V38 doctrine proposal D16 (liquidity-pool hypothesis — conceptual source only, not operationalized)
10. Execution/data governance records (forward runtime protections; Norgate archival licensing decision; FRED series status)

## 4. CANDIDATE SET

(GOVERNANCE FACT) Exactly three candidates from the completed cycle; no artificial candidates added:

| ID | Name | Decision class | Parameters | Cycle status | Selection status (this review) |
|---|---|---|---|---|---|
| F-01 | Session-Partition Reference Process (Overnight Exposure Leg) | Calendar/session | 0 | FORMULATED — NOT SELECTED | **SELECTED (hypothesis only)** |
| F-02 | Two-Index Relative-Value Process (Spread Reversion) | Pairs / relative value | 4 declared constants | FORMULATED — NOT SELECTED | **DEFERRED for first slot** |
| F-03 | Cross-Sectional Relative-Strength Rotation Process | Rank allocation | 1 declared constant | FORMULATED — NOT SELECTED | **DEFERRED for first slot** |

## 5. BS1 OBJECT-TYPE REVIEW

(SELECTION REVIEW) Each candidate verified against the eleven-question completeness standard (participation, direction, entry, exit, risk/invalidation, execution, scope, outcome, cost model, opportunity population, deterministic semantics):

- **F-01: PASS.** Complete: participation = every trading day (overnight leg); direction = long (mechanism-predicted); entry = prior close (MOC); exit = next open (MOO); invalidation = deterministic data-gap skip; execution = MOC/MOO single leg; scope declared (one liquid US equity index); outcome = per-leg net log return; cost model declared (1 bps/5 bps convention); population = all trading days, one decision each. Zero free parameters; no undefined terminology.
- **F-02: PASS.** Complete: participation daily; direction = sign of rolling z-score; entry = ±1.0σ crossing at close; exit = zero-crossing or 3σ invalidation with cooling rule; execution = daily two-leg MOC, equal notional; scope declared (two liquid US equity indices); outcome = book net log return; cost model declared; population = all trading days in defined states. Four design constants fully declared.
- **F-03: PASS.** Complete: participation daily; direction = rank-determined top/bottom; entry/exit = daily rebalance; invalidation = deterministic missing-data guard; execution = daily two-leg MOC, full turnover; scope declared (four-index universe); outcome = book net log return; cost model declared; population = all trading days. One design constant declared.

No economics were used to compensate for any semantic gap; none was needed. All three PASS BS1. (SELECTION REVIEW — a pass here is necessary, not sufficient.)

## 6. PROVENANCE / HISTORICAL-PERFORMANCE REVIEW

(SELECTION REVIEW — BS2/BS3/BS4/BS5 applied)

**Origin and motivation (per cycle artifact, committed pre-outcome):**
- F-01: first-principles session-structure reasoning (risk-bearing across the overnight interval). Prior repository knowledge used as constraint only: intraday cost failures (ORD), M1 event-family exhaustion (V27–V36), vol-state conditioning (CAND-077/107), the BH-01 withdrawal (no outcome-descended trigger). No closed artifact's parameters, eras, markets, cells, or subsets imported. No repository outcome cited as a reason the process exists.
- F-02: first-principles relative-pricing reasoning (substitute arbitrage). Constraints used: single-asset reversion closures (DISC-021/CAND-097), cross-market directional closures (CAND-076/079), intraday cost failures. Constants (20-day lookback; ±1.0σ entry; 0.0 exit; 3.0σ invalidation) declared as conventional statistical architecture in the cycle artifact — no outcome consulted. Pair identity (S&P 500 × Nasdaq-100) declared prospectively at formulation, not after inspection.
- F-03: first-principles cross-sectional demand reasoning. Constraints used: TSMOM closure (DISC-022), reversion closures, intraday failures. Constant (20-day lookback) declared conventionally. Universe = all four contemporaneous broad-US liquid index series available in the archive — the full set, not a chosen subset.

**Hidden-use audit (per milestone §6):** no element of any formulation was chosen because it performed well historically, because another value performed worse, or because one period/market/parameter/regime was favorable. The formulation-cycle artifact is the pre-outcome record; its provenance-firewall sections (per-package) are verified consistent with the packages. No contamination found. Similarity to prior research (e.g., F-02's statistical skeleton vs the reversion family; F-03's ranking vs TSMOM) is architectural adjacency, not outcome selection — addressed in §16.

## 7. F-01 ADJUDICATION

(SELECTION REVIEW — milestone §9 questions answered)

1. **Completeness of the overnight decision process:** COMPLETE. The decision variable is session-partition exposure (hold the overnight leg / flat intraday); one decision per trading day; all eleven questions answered in the cycle package.
2. **"Every trading day" operational determinism:** DETERMINISTIC. Participation = every trading day in the declared window; the calendar and session clock define the population; data-gap days are defined no-trade decisions (recorded in the population), not exceptions.
3. **Instrument/session boundaries:** Session boundaries are defined by the regular US equity session (09:30–16:00 ET auction-bounded). Instrument identity is a single declared index class (one liquid US equity index); the specific identity is a V38A registration freeze (§21), not an unresolved ambiguity.
4. **Execution without hypothetical fills:** REPRESENTABLE. MOC/MOO at the session boundary are real, standard executions at index level (cash index or governed index-CFD feed); no hypothetical intraday fills, no partial-fill modeling required. Cost convention declared (1 bps each way base / 5 bps stress), to be frozen at registration.
5. **Opportunity population coherence:** COHERENT. All trading days in the frozen window, each exactly one decision; fixed and enumerable in advance — the cleanest population among the three candidates.
6. **Distinctiveness from CAND-075 / session / event work:** DISTINCT AT ARCHITECTURE LEVEL. CAND-075 (V25) measured closing-auction *event* displacement in M1 gold-CFD data — an event-occurrence study. F-01 is a daily close-to-open *decision process* on a daily equity index with no event conditioning — different decision object (session leg vs auction event), different information dimension (calendar partition vs auction print), different horizon and instrument class. Not a re-expression.
7. **Mechanism independence:** INDEPENDENTLY MOTIVATED. The risk-bearing-compensation chain (continuous session passes risk; overnight holders bear unreactable information; compensation accrues to the overnight leg) was committed in the cycle artifact before any measurement, with the sign claim explicitly assigned to future validation.
8. **Hidden historical selection in scope:** NONE FOUND. The modern daily US equity context is forward-justified (current execution environment, market structure, data availability, future tradability); no era, market, or parameter was chosen for historical favorability (§11).
9. **Execution/data blockers:** NONE. Daily open AND close observations are required (FRED close-only series are insufficient for the open leg); the intended source is a governed daily OHLC feed (e.g., MT5 index-CFD M1-derived daily bars). Feasibility verified at formulation; source governance is a registration-time item — a governance item, not a blocker.

**Documented tension (recorded, not concealed):** F-01's direction — long the overnight leg — is mechanism-predicted (risk-bearing compensation accrues to holders), and it coincides with the most extensively documented empirical regularity in equity research (the overnight/intraday return asymmetry). That regularity is **external prior knowledge**, a lawful hypothesis *source* under the ratified design (design §6D: scientific/mechanistic reasoning), not repository outcome evidence. The governance response is structural: (a) the formulation was committed pre-outcome with a full mechanism chain and falsification conditions; (b) no repository measurement informed the rule; (c) the entire motivating knowledge base is motivation, never validation (Motivation ≠ Validation, V38A); (d) validation will rest on fresh forward data with the repository archive sealed. If the mechanism is false, the process fails validation — that is exactly what validation is for. This is the same discipline BH-01 demanded, applied prospectively rather than retrospectively: **BH-01's defect was that its trigger existed only because of the repository's H01 arc and measured outcomes; F-01's rule exists because of a pre-outcome mechanism chain in a governed cycle artifact.**

**ADJUDICATION: SELECTABLE — and the strongest candidate for the first slot.**

## 8. F-02 ADJUDICATION

(SELECTION REVIEW — milestone §10 questions answered)

1. **Pair relationship determinism:** DETERMINISTIC given the pair freeze. The rolling z-score of the log-price ratio over the trailing 20-day window is fully specified; entry/exit/invalidation events are deterministic functions of price history.
2. **Index identity justification:** The mechanism requires two near-substitute indices sharing a common factor. The declared pair (S&P 500 × Nasdaq-100) satisfies this structurally; the archive offers four contemporaneous series (SP500, DJIA, NASDAQ100, NASDAQCOM), and the mechanism holds for any liquid pair among them. The pair is **underdetermined by mechanism** — any pair would satisfy the premise — so the specific identity is a declared scope surface that must be frozen at registration, not an ambiguity.
3. **Rolling z-score completeness:** COMPLETE. Window, normalization, entry/exit/invalidation bounds, and cooling rule all specified in the cycle package.
4. **Entry/exit executability:** EXECUTABLE. Daily two-leg MOC, equal notional, deterministic event rules.
5. **Structural-break invalidation determinism:** DETERMINISTIC. |z| > 3.0 closes the position; no re-entry until z crosses zero.
6. **Pair-selection hidden market shopping:** NOT FOUND at formulation — the pair was declared prospectively in the cycle artifact. **BUT the surface is real and must be governed:** the pair choice is a scope decision with degrees of freedom (4 candidate series → 6 possible pairs), and nothing in the mechanism selects one pair over another. Because the selection review cannot verify post hoc that no pair was favored for its historical relationship, F-02's pair identity must be frozen with an explicit pre-registration statement of why the declared pair is the architectural choice — or the pair list (all 6 pairs as one declared family) must be frozen. This is a governance-completeness item, not an affirmative blocker: the pair was declared before any measurement in this milestone, and no economics were computed.
7. **Distinctiveness from mean-reversion and cross-market research:** DISTINCT AT ARCHITECTURE LEVEL. vs DISC-021/CAND-097 (closed single-asset reversion): different decision object (two-leg relative book vs outright), different information dimension (cross-sectional ratio vs absolute displacement), different economic mechanism (substitute-arbitrage convergence vs single-asset overreaction). vs CAND-076/079 (closed cross-market directional): different decision object (convergence book vs directional exposure). The statistical skeleton (z-score entry / zero-crossing exit) is adjacent to the closed reversion family — recorded as adjacency, judged architectural rather than cosmetic, with the final adjudication resting with V38A structural validation.
8. **Opportunity population suitability:** SUITABLE. All trading days in defined states; entry/exit events deterministic; clean daily population for Base-vs-Conditional attribution.
9. **Execution/cost realism:** REALISTIC with a registration item. Two-leg equal-notional daily MOC book on liquid indices; short-leg feasibility (borrow/CFD availability) is a registration-time realism check. Cost convention declared (1 bps/leg/side base; 4 bps round trip; 5 bps stress).

**Constants classification (milestone §12):** 20-day lookback — conventional one-month architecture choice (option 1). ±1.0σ entry / 0.0 exit / 3.0σ invalidation — conventional statistical bounds (option 1). Pair identity — declared prospectively with an explicit pre-outcome design rationale (option 2), but underdetermined by mechanism (documented surface). No constant was chosen because it is expected to work (option 3).

**ADJUDICATION: SELECTABLE — DEFERRED for the first slot.** No affirmative blocker; the pair-identity freeze and the reversion-family adjacency documentation make F-02 a legitimate candidate for a later slot rather than the cleanest first reference.

## 9. F-03 ADJUDICATION

(SELECTION REVIEW — milestone §11 questions answered)

1. **Universe justification:** The declared universe (S&P 500, DJIA, Nasdaq-100, Nasdaq Composite) is **the complete set of contemporaneous broad-US liquid index series available in the repository archive** (per the H01 economic-translation input manifest; `sp` and `NYA` are historical-era or composite-adjacent series with limited contemporary coverage). Inclusion of the full available set is the opposite of subset shopping: no series was excluded to improve any property, and no series was added beyond availability.
2. **Inclusion by design rather than outcome selection:** BY DESIGN. Universe = availability ∩ broad-US liquid index class; no historical relationship was consulted.
3. **Ranking rule determinism:** DETERMINISTIC. Trailing 20-day log returns ranked descending; top rank long, bottom rank short.
4. **Tie determinism:** The cycle package must specify tie-breaking at registration (e.g., lexicographic order by declared series identity). This is a **registration-time completion item** — the rule as formulated is deterministic except under exact ties, which are possible; the tie-break is a mechanical completion, not a design change, and does not alter the architecture.
5. **Holding/turnover mechanics:** COMPLETE. Daily rebalance at close; positions held one day; full turnover.
6. **Short-leg semantics:** DEFINED. Equal notional short of the bottom-ranked index via index-level instruments; short-leg availability is a registration-time realism check (as for F-02).
7. **Execution cost realism:** The declared convention (1 bps/leg/side; 4 bps full daily turnover; 5 bps stress) is coherent and declared prospectively. **Governance concern (not a blocker):** daily full turnover at 4 bps/day round trip implies a structural cost burden (~800+ bps/year of turnover cost at base convention, before any relative-spread advantage) that makes the process's cost realism the binding constraint. This is arithmetic on the declared convention — no hypothesis economics were computed — and it is precisely the kind of realism a first reference should not have as its dominant question.
8. **Distinctiveness from equal-weight basket usage:** DISTINCT. The H01 arc used the six markets only as an equal-weight composite of conditional deltas; F-03 ranks them cross-sectionally into a long/short book — different decision object and information dimension. vs DISC-022 TSMOM: cross-sectional ranking vs own-history trend — architectural distinction, recorded.
9. **Turnover governance issue:** The daily full-turnover structure is executable, but its cost structure makes execution governance the central question for F-03, weakening it as the *first* reference (attribution would be dominated by turnover-cost arithmetic rather than decision quality).

**Constants classification (milestone §12):** 20-day lookback — conventional one-month architecture choice (option 1). Universe composition — full available set, explicit pre-outcome rationale (option 2). Top-1/bottom-1 — minimal expression of the ranking claim (option 1). Daily rebalance — the natural frequency of a daily-decision process, declared with cost realism (option 1). No constant chosen because it is expected to work (option 3).

**ADJUDICATION: SELECTABLE — DEFERRED for the first slot.** No affirmative blocker; the full-turnover cost structure (governance concern) and the tie-break completion item make F-03 a legitimate later candidate rather than the cleanest first reference.

## 10. CROSS-CANDIDATE RESEARCH-PRIORITY REVIEW

(SELECTION REVIEW — qualitative only; NO numerical score; no expected-profit dimension)

| Dimension | F-01 | F-02 | F-03 |
|---|---|---|---|
| A. Architectural distinctiveness | HIGH (new decision class) | HIGH (new decision class) | HIGH (new decision class) |
| B. Decision completeness | HIGHEST (0 parameters, 1 decision/day) | HIGH (4 declared constants) | HIGH (1 constant + tie-break item) |
| C. Execution feasibility | HIGHEST (single leg MOC/MOO) | MEDIUM (two legs, short leg) | MEDIUM (two legs, daily turnover) |
| D. Attribution quality | HIGHEST (cleanest fixed population) | HIGH | HIGH |
| E. Data feasibility | HIGH (one daily OHLC series; feed verified) | HIGH (two daily close series; archive READY) | HIGH (four daily close series; archive READY) |
| F. Strategic relevance | HIGH (session structure untested) | HIGH (relative value untested) | HIGH (cross-section untested) |
| G. Research-capital efficiency | HIGHEST (single instrument, no search) | MEDIUM-HIGH | MEDIUM-HIGH |
| H. Governance cleanliness | HIGHEST (no hidden surfaces; direction documented) | MEDIUM-HIGH (pair surface; family adjacency) | MEDIUM-HIGH (turnover governance concern) |
| I. Base-first validity | YES | YES | YES |

The qualitative ordering (F-01 leading on B/C/D/G/H) reflects governance and attribution architecture only — explicitly NOT expected profitability. No dimension was scored numerically; no gate was created.

## 11. MODERN-SCOPE / SIGN-INVERSION REVIEW

(SELECTION REVIEW — BS6 applied)

**Scope-level test — "Would this instrument/scope/market universe still be the intended research context if all motivating historical results had been negative?"**

- F-01: **PASS.** The modern daily US-equity *context* is forward-justified (only the future is tradeable; current execution environment, cost structure, market structure, data availability, future tradability). The rule-level direction (long overnight) is mechanism-predicted; if the mechanism's premise were false, the process fails validation on fresh data — that is the validation design, not a selection defect. No era, market, or parameter was selected because it historically won. The repository archive (including any H01-era window) is sealed and can never be validation evidence (Motivation ≠ Validation).
- F-02: **PASS at scope level.** Two liquid US equity indices with contemporaneous daily data; forward-contiguous validation context. The pair identity is declared, not outcome-selected — with the documented underdetermination surface (§8.6) to be frozen at registration.
- F-03: **PASS at scope level.** The full available contemporaneous index universe; forward-contiguous validation context. No subset, era, or regime selected for favorability.

No formulation selected a scope because it historically worked best. The BH-01 precedent is honored: the failed element there was the outcome-descended *trigger*; all three candidates here carry mechanism/architecture-descended rules committed pre-outcome, and none rests on any repository cell.

## 12. CLOSED-LINE FIREWALL REVIEW

(SELECTION REVIEW — BS3)

| Closed artifact | F-01 | F-02 | F-03 |
|---|---|---|---|
| H01 (daily vol-conditioned long/flat) | Not reused: different decision object (session partition vs state-conditioned full-day exposure); no trigger imported | Not reused | Not reused (equal-weight basket vs ranked book) |
| ORD (intraday breakout) | Not reused (daily horizon, no breakout) | Not reused | Not reused |
| TRADEABLE_EDGE V27–V36 (M1 events) | Not reused (daily, non-event) | Not reused | Not reused |
| CAND-077/081/083/099 (observations) | Not used (no state in any formulation) | Not used | Not used |
| DISC-021/CAND-097 (single-asset reversion) | n/a | Architectural adjacency only — different object/mechanism, documented (§8.7) | n/a |
| DISC-022 (TSMOM) | n/a | n/a | Architectural adjacency only — cross-sectional vs own-history (§9.8) |

No closed line is reopened, promoted, parameter-imported, or disguised. Each candidate is a genuinely new governed object created by the formulation cycle.

## 13. ANTI-RESCUE REVIEW

(SELECTION REVIEW — BS13)

- F-01: **YES** — coherent and worthy of independent evaluation with no Conditional ever created: complete session-partition process; economics measured on its own overnight legs. A future Conditional (e.g., state-conditioned overnight legs) would be an increment over the reference, never a requirement.
- F-02: **YES** — complete pairs process; convergence measured on its own book.
- F-03: **YES** — complete rank process; persistence measured on its own book.

No candidate's rationale depends on future confirmation, liquidity filters, regime filters, event filters, Conditional improvement, or "repair." No weak-process-for-increment framing exists in any package.

## 14. ATTRIBUTION REVIEW

(SELECTION REVIEW) All three produce a fixed opportunity population, deterministic participation, deterministic execution, one declared coherent cost model, a stable outcome definition, and clean baseline attribution — satisfying the BASE vs BASE+PREDECLARED CONDITIONAL comparison structure of V38:

- F-01: one decision per trading day; per-leg net log return; zero-parameter population — the cleanest baseline (a future Conditional would add a predeclared condition over the same daily population).
- F-02: daily defined states; deterministic z-events; book net log return.
- F-03: daily rank events; book net log return.

No candidate has ambiguous population construction; F-01's is the most transparent (§17).

## 15. EXECUTION-REALISM REVIEW

(SELECTION REVIEW — no costs tested; no economics computed)

| Candidate | Classification | Notes |
|---|---|---|
| F-01 | **CLEAR** | MOC/MOO at real session boundaries; single liquid index leg; daily OHLC data source verified feasible (MT5 index-CFD M1-derived bars or governed daily feed); no hypothetical fills, no undefined shorting, no unbounded turnover |
| F-02 | **CLEAR (one governance item)** | Two-leg daily MOC book; short-leg availability (borrow/CFD) is a registration-time realism check; no unbounded turnover (event-driven entries) |
| F-03 | **GOVERNANCE CONCERN** | Daily full turnover is bounded and executable, but the declared cost structure (~4 bps/day round trip at base) makes cost realism the binding question for a first reference; no blocker found, but the concern is recorded and is a reason for deferral |

No unavailable prices, ambiguous session boundaries (F-01 boundaries are auction-defined), impossible fills, or unrealistic price-formation assumptions were found in any candidate.

## 16. DISTINCTIVENESS REVIEW

(SELECTION REVIEW — decision-architecture level, not feature level)

- **F-01 vs session/event work (CAND-075 et al.):** NOT merely another session-event formulation. CAND-075 measured closing-auction event displacement; F-01 is a full session-partition decision process with daily population semantics and no event conditioning — different decision object, information dimension, horizon, and instrument class (§7.6).
- **F-02 vs mean reversion (DISC-021/CAND-097):** NOT merely another mean-reversion variant. The tradable object is a two-leg relative spread; the mechanism is substitute-arbitrage convergence; the information dimension is cross-sectional relative price. The z-score skeleton is adjacent but the architecture differs (§8.7).
- **F-03 vs cross-market directional (CAND-076/079) and TSMOM (DISC-022):** NOT merely another cross-market directional artifact. F-03 is a market-neutral-by-construction rank book over the full index complex; the economic claim is cross-sectional demand persistence, distinct from both directional spillover and own-history trend (§9.8).
- **Cross-candidate:** pairwise distinct on decision object, information dimension, economic claim, and execution structure (cycle artifact §11) — verified again at selection; no candidate is a variant of another.

## 17. FIRST-BASE QUALITY REVIEW

(SELECTION REVIEW) Because this is the first Base slot — the reference against which the entire V38 assembled architecture will later be tested:

| First-base criterion | F-01 | F-02 | F-03 |
|---|---|---|---|
| Clean semantics | HIGHEST (0 parameters) | HIGH | HIGH |
| Low ambiguity | HIGHEST (1 decision/day, calendar-defined) | MEDIUM (pair freeze required) | MEDIUM (tie-break item; turnover governance) |
| Transparent opportunity population | HIGHEST | HIGH | HIGH |
| Transparent execution | HIGHEST (single leg) | MEDIUM | MEDIUM |
| Strong attribution | HIGHEST | HIGH | HIGH |
| Broad research usefulness | HIGH (any Conditional can condition the daily population) | HIGH | MEDIUM-HIGH |
| Limited hidden degrees of freedom | HIGHEST | MEDIUM (pair surface) | MEDIUM-HIGH |

By these criteria — deliberately excluding expected profitability — **F-01 is the clearest and most defensible reference decision context** if it later passes V38A. Its one documented tension (externally-known favorable direction) is governed by the motivation≠validation boundary and fresh-data validation design (§7), not resolved by denial.

## 18. FINAL SELECTION DECISION

**A. ONE HYPOTHESIS SELECTED: F-01 — Session-Partition Reference Process (Overnight Exposure Leg).**

F-01 clearly survives BS1–BS13 and is the most defensible first Base hypothesis:
- BS1 object type: PASS (§5)
- BS2/BS3 provenance: clean, pre-outcome, no import (§6)
- BS4/BS5 historical-result separation: no outcome consulted; no hidden gate (§6, §11)
- BS6 sign-inversion: scope PASS; rule mechanism-predicted and fresh-data-validated (§11)
- BS8 family redundancy: distinct at architecture level (§16)
- BS9 Conditional independence / BS10 base-first / BS13 anti-rescue: PASS (§13)
- BS11 owner authority: required, not assumed (§20)
- BS12 hypothesis ≠ Base: maintained (§19)

F-02 and F-03: **DEFERRED for the first slot** (no affirmative blocker; pair-identity freeze and turnover-governance concern respectively — resolvable in a later review). **REJECTED:** none. **BLOCKED:** no governance defect found.

## 19. SELECTED HYPOTHESIS PACKAGE

> **SELECTED BASE HYPOTHESIS — V38A REGISTRATION REQUIRED**

- **Hypothesis ID:** F-01 (formulation-class identifier; NOT a Base ID; NOT a candidate-ledger entry)
- **Exact formulation reference:** `output/research_discovery/QUANTFORGE_OUTCOME_BLIND_BASE_FORMULATION_CYCLE_V1.md`, §7 (SHA `655473e2a863`, 464 lines)
- **Name:** Session-Partition Reference Process (Overnight Exposure Leg)
- **Decision-process statement:** on every trading day of the declared window, hold long exposure in one liquid US equity index from the prior regular-session close to the next regular-session open; flat from open to close; one decision per day.
- **Provenance:** first-principles session-structure reasoning; committed pre-outcome in the governed formulation cycle; no repository outcome consulted; no closed-artifact element imported (§6, §7).
- **Selection rationale (architectural):** cleanest legitimate reference decision process for the first slot — zero free parameters; single declared instrument class; one decision per day; transparent MOC/MOO single-leg execution; complete fixed opportunity population; session-partition decision class never before tested in QuantForge; research-capital efficiency highest of the three. **Not selected for any historical result.**
- **BS1–BS13 findings:** object-type PASS; provenance clean; firewall clean; sign-inversion PASS at scope with mechanism-predicted rule; anti-rescue YES; attribution HIGHEST; execution CLEAR; distinctiveness HIGH; first-base quality HIGHEST (§5–§17).
- **Historical-performance firewall result:** CLEAN — no element chosen for historical favorability; the archive is sealed as motivation-only (§6, §11).
- **Sign-inversion result:** PASS at scope level; rule direction mechanism-predicted with the documented external-prior tension governed by fresh-data validation (§7, §11).
- **Anti-rescue result:** PASS — coherent with no Conditional ever created (§13).
- **Attribution result:** cleanest daily population among the three; supports BASE vs BASE+PREDECLARED CONDITIONAL (§14).
- **Execution review:** CLEAR — MOC/MOO at real session boundaries; no hypothetical fills (§15).
- **Distinctiveness review:** distinct at architecture level from CAND-075/session work, H01, ORD, V27–V36 (§16).
- **Unresolved registration items (deferred to V38A registration design, NOT resolved here):** instrument identity; session-boundary calendar definition; data source governance; validation window; cost-model freeze; tie-free semantics not applicable (no ranking); short-leg not applicable (single long leg); statistical/economic reporting plan; structural validation protocol.
- **Owner authorization:** **OWNER AUTHORIZATION REQUIRED TO ENTER V38A REGISTRATION** (§20).

The selected object is a **hypothesis**. It is NOT Base status, NOT V38A-validated, NOT Registry-eligible.

## 20. OWNER AUTHORIZATION BOUNDARY

**OWNER AUTHORIZATION REQUIRED TO ENTER V38A REGISTRATION.**

(GOVERNANCE FACT) The agent's selection recommendation is independent; only the owner may authorize F-01 to proceed to the next milestone (**BASE HYPOTHESIS FREEZE / V38A REGISTRATION DESIGN**). Owner authorization:

- creates permission to begin the registration-design milestone — nothing more;
- does NOT create Base status;
- does NOT validate the hypothesis;
- does NOT imply profitability;
- does NOT authorize Registry entry;
- cannot waive any BS1–BS13 protection (ratified doctrine: an override would require a separate governance amendment, which no task has authorized).

Owner options: **AUTHORIZE F-01 TO ENTER V38A REGISTRATION** / **DEFER** / **REJECT** / **REQUEST A DIFFERENT SELECTION REVIEW** (a new review must still satisfy BS1–BS13).

## 21. V38A HANDOFF REQUIREMENTS

If owner-authorized, the next milestone (**BASE HYPOTHESIS FREEZE / V38A REGISTRATION DESIGN**) must freeze, under V38A BV1–BV13, exactly these items for F-01:

1. **Instrument identity** — the single liquid US equity index (declared class at formulation; specific identity frozen at registration).
2. **Complete scope** — declared instrument, session calendar (09:30–16:00 ET auction-bounded), exclusion/skip semantics.
3. **Data source** — governed daily OHLC feed (e.g., MT5 index-CFD M1-derived daily bars; FRED close-only series are insufficient for the open leg); data-source governance resolved (including the recorded Norgate archival items if any historical series are used — expected: forward-contiguous feed only).
4. **Validation window** — forward-contiguous fresh data accruing after selection; the repository archive (including any H01-era window) is sealed and cannot serve as validation evidence (Motivation ≠ Validation).
5. **Confirmation segment** — if required by the validation design (V38A stage definition), specified at registration.
6. **Deterministic rule implementation** — the calendar rule (close(t) → open(t+1) long; flat open → close), zero free parameters, gap-skip semantics.
7. **Execution semantics** — MOC at close / MOO at open, full declared notional, single leg.
8. **Cost model** — one coherent frozen convention: 1 bps entry + 1 bps exit base, 5 bps stress; no other cost treatment may be introduced later.
9. **Outcome definition** — per-leg net log return close(t) → open(t+1) net of declared transition costs.
10. **Opportunity population** — all trading days in the frozen window, one decision each; frozen before any measurement.
11. **Statistical/economic reporting plan** — V38A stage-3/4 evidence plan (per BV clauses); no sign/magnitude gate; economics are evidence in holistic adjudication only.
12. **Structural validation protocol** — V38A stages 1–2 (determinism, execution integrity, contamination controls) before any economic exposure.
13. **Contamination controls** — no re-optimization, no scope narrowing after outcome exposure, no Conditional influence, no fresh-data inspection before the frozen window opens.

Nothing in §19–§21 freezes these items today; they are the handoff list for the registration-design milestone.

## 22. FINAL GOVERNANCE AUDIT

(AUDIT — milestone §27)

- **Q1** Was any candidate selected because it historically made the most money? **NO.** No economics were consulted; selection rationale is architectural (§7, §18).
- **Q2** Was any favorable historical period selected? **NO.** All scopes forward-justified; archive sealed (§11).
- **Q3** Was any historical parameter optimized? **NO.** F-01 has zero parameters; F-02/F-03 constants are conventional, declared pre-outcome, unmodified (§6, §8–§9).
- **Q4** Was any new economic measurement performed? **NO.** No backtest, return, expectancy, Sharpe, win rate, drawdown, correlation, sensitivity, or Monte Carlo computation occurred (§15, §23).
- **Q5** Was a future Conditional required to justify the candidate? **NO.** Base-first YES for all three (§13).
- **Q6** Did any observation become a Base? **NO.** No CAND/SRE/state object was promoted; F-01 is a new governed object (§12).
- **Q7** Did any closed line get reopened? **NO.** H01/ORD/TRADEABLE_EDGE remain CLOSED; no parameter/era/cell imported (§6, §12).
- **Q8** Does the selected hypothesis remain a hypothesis rather than a Base? **YES.** State = SELECTED BASE HYPOTHESIS — V38A REGISTRATION REQUIRED (§19).
- **Q9** Is V38A validation still required? **YES.** Full six-stage pathway; nothing in this milestone shortcuts it (§21).
- **Q10** Does the Base Registry remain EMPTY? **YES.** No registry entry created or authorized (§2, §20).

## 23. REPOSITORY / GIT INTEGRITY

(GOVERNANCE FACT) Recorded at selection:

- HEAD before and after: `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`; branch `main`.
- Change: exactly ONE new untracked artifact — `output/research_discovery/QUANTFORGE_BASE_HYPOTHESIS_SELECTION_FINAL_V1.md`.
- No commit, no staging (selection milestone; default no-commit).
- `SESSION_HANDOFF.md` intentionally NOT modified.
- No source/test/configuration change; no Base Registry record; no candidate-ledger mutation; no validation; no experiment; no new economic measurement; no protected-forward inspection.
- `git diff --check` verified clean.
- Pre-existing dirty/untracked files (forward runtime data, G6 dirs, health/event ledgers, screening scripts, V37A phase-A, V1-r2 selection recommendation, cycle artifact, superseded proposal) remain untouched and are not part of this milestone.

## 24. HARD STOP

Selection complete. **F-01 is SELECTED as a hypothesis only — V38A registration required.** F-02 and F-03 remain FORMULATED HYPOTHESES — NOT SELECTED (deferred for the first slot).

STOP. No freeze of V38A registration; no missing parameter or scope defined; no structural or economic validation; no backtest; no forward-data testing; no Registry entry; no Conditional component; no assembled research; H01/ORD/TRADEABLE_EDGE remain CLOSED; CAND-077/081/083/099 unchanged; protected-forward excluded; **Base Registry EMPTY**.

Next milestone, if and only if the owner authorizes F-01: **BASE HYPOTHESIS FREEZE / V38A REGISTRATION DESIGN** — conversion of F-01 into the fully frozen V38A registration package (§21), after which a registration-integrity gate precedes any V38A execution. Nothing in this artifact authorizes that milestone or any research beyond it.