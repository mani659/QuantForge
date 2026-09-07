# QUANTFORGE — BASE HYPOTHESIS SELECTION / VALIDATION DESIGN V1

**Milestone:** Base Hypothesis Selection / Validation Design (research-design milestone, NOT ratification)
**Status:** DESIGN PROPOSAL — NOT RATIFIED
**Parent governance:** V38 doctrine (RATIFIED, `c42c3c3`); V38A Base Validation Pathway (RATIFIED, `4da500b`)
**Authorized next milestone after ratification of this design:** actual Base-hypothesis selection
**Design artifact:** this document (untracked, created per milestone authorization)
**No Base was created, selected, or hypothesized. The Base Registry remains EMPTY.**

Label conventions used throughout:
- GOVERNANCE FACT — binding ratified doctrine (V38 / V38A / G1 V3)
- DESIGN PROPOSAL — this milestone's proposal, not yet ratified
- UNRESOLVED — genuinely requires a later owner/governance decision
- NOT PERMITTED — prohibited by ratified doctrine or this design
- FUTURE MILESTONE — an explicitly deferred step

---

## 1. EXECUTIVE DESIGN VERDICT

**BASE SELECTION PATHWAY READY FOR RATIFICATION.**

The design resolves the governing question the ratified V38A pathway deliberately left open: *how does QuantForge move from "there may be legitimate decision-process concepts" to "one specific Base hypothesis is frozen and ready for V38A registration," without ranking on historical outcomes, resurrecting closed lines, or constructing a rescue vehicle?*

The answer has one load-bearing spine: **selection is a governance act performed on decision-process architecture, not a measurement act performed on results.** The protocol therefore (a) gates on object type before any economics are considered (§5), (b) separates *eligibility blockers* from *priority evidence* from *validation evidence* so that the same numbers can never serve both priority and gate roles (§8, §11), (c) freezes the hypothesis before V38A registration so no later result can alter it (§14), and (d) routes the final choice through owner authorization with the explicit status that a selected hypothesis is not a Base (§21, §23).

No Base is selected by this document. No hypothesis is declared. The Base Registry remains EMPTY.

---

## 2. GOVERNANCE CONTEXT

(GOVERNANCE FACT) Confirmed repository state at authoring:

- V38 Assembled-Decision / Relational Qualification Doctrine — **RATIFIED** (commit `c42c3c3`): HYBRID BASE + CONDITIONAL; Base Registry begins EMPTY; No-Rescue; conditional components may have zero/negative standalone expectancy; incremental-over-Base qualification; no universal numeric gates; D1–D25 binding.
- V38A Base Validation Pathway — **RATIFIED** (commit `4da500b`): BV1–BV13 binding; six-stage lifecycle (Stage 0 hypothesis → Stage 5 registry entry); BASE-ELIGIBLE / INCONCLUSIVE / NOT BASE-ELIGIBLE categories with **no sign-or-magnitude economic gate**; Motivation ≠ Validation; frozen opportunity population; one coherent frozen cost model; structural No-Rescue.
- **Base Registry = EMPTY. No Base exists. No Base hypothesis is currently authorized. No Base validation is underway.**
- G1 V3 remains authoritative: VALIDITY = HARD GATES; ECONOMIC METRICS = EVIDENCE; QUALIFICATION = HOLISTIC ADJUDICATION.
- System Assembly Candidate Register remains untouched; closed lines (H01, ORD, TRADEABLE_EDGE families) remain closed; CAND-077/081/083/099 remain observations; CAND-015/024/035 remain protected-forward and fully excluded.

(DESIGN PROPOSAL) This milestone sits between V38A Stage 0 (hypothesis formulation) and Stage 1 (prospective registration). It governs *which* hypothesis may be formulated for registration and *how that choice is made defensibly*.

---

## 3. BASE SELECTION PROBLEM

(DESIGN PROPOSAL) The problem is not "find a good strategy." It is: **choose one decision-process concept to spend V38A validation capital on, under rules that make the choice immune to the documented failure modes of the archive** — retrospective winner selection, favorable-era selection, closed-line resurrection, family overfitting, and Base-as-rescue.

The selection decision is uniquely dangerous because it is the last governance step where historical results are visible before the V38A validation window seals. Every control in this design exists to ensure that visibility cannot become selection authority.

---

## 4. DISCOVERY vs SELECTION vs VALIDATION vs QUALIFICATION

(DESIGN PROPOSAL) Four distinct governance states, each with its own legal inputs and outputs:

| State | Question | Inputs | Output | Evidence allowed |
|---|---|---|---|---|
| DISCOVERY | What decision-process *concepts* might legitimately exist? | archive lessons, architecture reasoning, market structure | candidate concepts (unenumerated) | any historical record, for motivation only |
| SELECTION (this milestone) | Which ONE concept gets V38A validation capital? | object-type-qualified concepts, governance review, research-priority rationale | SELECTED BASE HYPOTHESIS (frozen) | eligibility blockers + priority evidence; **never an outcome ranking gate** |
| VALIDATION (V38A) | Does the frozen hypothesis earn BASE-ELIGIBLE status? | the frozen registration, sealed validation evidence | BASE-ELIGIBLE / INCONCLUSIVE / NOT BASE-ELIGIBLE | only V38A six-stage evidence |
| QUALIFICATION (V38) | Does a Conditional improve the validated Base? | validated Base + predeclared Conditional + one cost model | incremental-value adjudication | assembled-test evidence only |

(NOT PERMITTED) Results from VALIDATION may not feed back into SELECTION of a different concept (that is post-hoc winner selection). Results from QUALIFICATION may not alter the Base (that is post-hoc Base editing, prohibited by V38A §15-ratified versioning rules).

---

## 5. OBJECT-TYPE GATE

(DESIGN PROPOSAL) Before any economics, provenance, or historical record is considered, every concept must pass the object-type gate:

> Is this actually a decision process — something that deterministically determines actual trade participation/execution under a declared scope, data source, outcome definition, execution model, and cost model?

A Base-candidate concept must be expressible as all of:

- decision conditions;
- actual trade participation semantics (when a trade is taken);
- entry semantics;
- exit semantics;
- execution semantics;
- declared scope (instrument(s), timeframe(s), session treatment);
- data source;
- outcome definition;
- cost model.

(GOVERNANCE FACT / NOT PERMITTED) Rejected at Stage 0 — before any further review — anything that is merely: an observation; a state; an event; an indicator; a threshold; a descriptive statistic; a market condition; a Conditional component; a historical subset; an abstract mechanism; a hypothetical P&L.

(GOVERNANCE FACT) Explicit confirmation carried from ratified doctrine: **CAND-077, CAND-081, CAND-083, and CAND-099 remain non-Base objects.** They are state/event observations, not decision processes; this pathway does not reinterpret them. A *complete decision process built around the information one of them carries* could, in principle, be a *newly formulated* concept under §9 — but the observation itself can never be the candidate.

---

## 6. CLOSED-LINE FIREWALL

(GOVERNANCE FACT, from V38 D13 / V38A BV-rules) Closure prohibits silently treating the old artifact as an approved Base candidate.

(DESIGN PROPOSAL) A closed line MAY provide: motivation; architectural lessons; evidence about what failed; evidence about market context; inspiration for a genuinely new hypothesis.

A closed line MAY NOT provide: retroactive Base status; direct Base entry; automatic validation scope; automatic parameter selection; automatic favorable-era selection.

If a future Base hypothesis is motivated by a closed artifact, the hypothesis must be **explicitly declared, independently justified, prospectively registered, and validated under V38A** — the closed artifact is cited as provenance, never as evidence of the new hypothesis.

---

## 7. HISTORICAL ARTIFACT REUSE

(DESIGN PROPOSAL) Distinguish two reuse forms:

**LEGITIMATE REUSE (conceptual):** A prior study demonstrates that a *decision concept* is worth asking a new question about, and the new Base hypothesis is independently specified — its own decision rules, its own declared scope, its own registration.

**PROHIBITED REUSE (result-driven construction):** Taking the prior study's best parameter / period / instrument / regime / cell / threshold / subset and relabeling that result as a Base hypothesis.

The distinguishing test is architectural: does the new hypothesis stand as a complete, deterministic decision process specifiable *before* its own measurement — or does its specification require copying the old result? Only the former is a Base hypothesis.

---

## 8. ECONOMICS-AT-SELECTION RULES

(GOVERNANCE FACT, from V38A) No sign, magnitude, or threshold of net expectancy — or any economic statistic — determines Base eligibility. Economic metrics are mandatory evidence only inside holistic viability adjudication (V38A Stage 4).

(DESIGN PROPOSAL) Before registration, historical economics are usable in exactly three separated roles:

1. **ELIGIBILITY BLOCKER** — evidence of structural invalidity, impossibility, leakage, pathology, rescue construction, or other disqualifying condition. Blocker evidence *excludes*; it never *selects*.
2. **PRIORITY EVIDENCE** — evidence influencing which otherwise-legitimate candidate deserves scarce validation capital (§12).
3. **VALIDATION EVIDENCE** — evidence intentionally designated for the future V38A study; it is *sealed* at selection (§15) and may not be inspected for selection purposes.

(NOT PERMITTED) Prohibited selection mechanisms — each would make historical performance the selection mechanism:
- "choose the highest return / least negative / highest win rate candidate";
- "choose the best modern-era cell";
- "choose the strongest backtest / best Sharpe";
- "choose the candidate that survived the most tests";
- "choose the candidate whose result most resembles the desired Base."

The rule stated plainly: **historical performance may be evidence *about* an artifact; an outcome-ranked comparison of artifacts cannot be the selection mechanism.** Priority evidence ranks research-worthiness; eligibility blockers filter validity; only governance review and owner authorization select.

---

## 9. RESEARCH-PRIORITY FRAMEWORK

(DESIGN PROPOSAL) Where multiple object-type-qualified concepts exist, a transparent priority mechanism allocates validation capital. The mechanism MAY weigh:

- architectural relevance (answers an unresolved system question);
- execution readiness (can actually be executed in the declared environment);
- data availability and data-freshness prospects;
- novelty relative to exhausted families;
- ability to produce a fixed, attributable opportunity population;
- research-capital cost;
- relevance to current strategic objectives;
- prior negative knowledge (learned failure modes);
- forward-justified modern relevance (§13).

(NOT PERMITTED) The mechanism must NOT rank primarily on P&L, expectancy, win rate, Sharpe, return, or best historical period. Any quantitative prioritization is labeled **research prioritization, not Base eligibility**, and is recorded as such in the selection record so it cannot later be read as a gate.

---

## 10. CANDIDATE-FAMILY / REDUNDANCY CONTROL

(DESIGN PROPOSAL) Base selection must not become a redundant strategy-generation engine. Controls:

- Prefer distinct decision-process architecture over cosmetic parameter variation; two concepts differing only in thresholds/parameters are one family, not two candidates.
- A candidate that is architecturally a re-expression of a closed failed family carries the family's negative knowledge as an eligibility-relevant fact (§8 blocker role), and requires an explicit *new-mechanism* justification to be advanced.
- No arbitrary similarity metric is created; redundancy review is qualitative, documented, and part of the selection record.

---

## 11. PROSPECTIVE SELECTION FREEZE

(DESIGN PROPOSAL) The frozen-point sequence:

```
Research concept
  → candidate screening (object-type + governance)
  → research-priority decision
  → BASE HYPOTHESIS DECLARATION
  → BASE HYPOTHESIS FREEZE  ← selection ends here
  → V38A Stage 1 prospective registration
  → Stage 2 structural validation
  → Stage 3 economic validation
  → Stage 4 viability adjudication
  → Stage 5 registry entry / lifecycle initiation
```

After the freeze:

- no historical result may alter the hypothesis;
- no parameter selection may occur;
- no scope selection may occur;
- no favorable subset may be substituted;
- no Conditional result may influence the Base.

The freeze is what makes V38A's Motivation ≠ Validation enforceable: the motivating record is fixed *before* the validation window opens.

---

## 12. SELECTION DATA BOUNDARY

(DESIGN PROPOSAL) The protocol does not default to "blind everything." It partitions visibility by role:

**May be inspected for research governance (selection rationale):** provenance records; registration history; known failure modes; family membership; closure verdicts; mechanism rationale; data availability. Where the V38A validation will need an independent confirmation segment or genuinely new observations, the selection team may inspect what exists to *design the scope* — without using it as evidence for the hypothesis.

**Sealed to preserve validation independence (validation outcome construction):** the specific economics of the confirmation segment or any new observation designated as the V38A validation window. Once the freeze occurs, the sealed boundary is closed and any further inspection of those numbers before Stage 4 adjudication is a governance violation.

The goal is not artificial blindness; it is **separation between the selection rationale (which may cite history) and the validation outcome (which must be measured independently)**.

---

## 13. MODERN-REGIME SELECTION

(DESIGN PROPOSAL, using H01 as the architectural example only — NOT reopened) Era dependence is documented knowledge. Two distinct justifications must never be conflated:

- **FORWARD-JUSTIFIED MODERN SCOPE (legitimate priority reason):** "QuantForge can only trade the future; a modern-era scope matches current execution environment, data regime, market structure, and cost environment." This is a priority reason and may legitimately shape the *declared scope* of a new hypothesis — recorded *before* the new study's outcomes are examined.
- **RETROSPECTIVE WINNING-ERA SELECTION (prohibited):** "This period worked best historically, therefore validate that period." This is result-driven construction.

The test: would the same scope be chosen if the motivating historical cell had shown the opposite sign? Forward-justified scoping survives that test; era-picking does not.

---

## 14. CONDITIONAL FIREWALL

(GOVERNANCE FACT, V38A) A Base must be independent of Conditional-component results.

(DESIGN PROPOSAL) A Base hypothesis must be completely specifiable without:
- knowing which Conditional will later be used;
- selecting a Conditional to make the Base work;
- filtering Base opportunities according to Conditional success;
- adapting Base parameters based on Conditional results.

Any selection rationale that references a future Conditional ("this weak process would be fine once conditioned") is a **rescue framing** and is an eligibility blocker (§25).

---

## 15. PARALLEL-CANDIDATE GOVERNANCE

(DESIGN PROPOSAL) Multiple concepts may be researched as design concepts (discovery and screening are parallel-friendly). But:

- V38A validation results may never be used to choose the "winning Base" after the fact. A candidate whose V38A validation has begun owns its independent outcome and adjudication; starting more than one validation "to see which passes" would convert validation into a selection tournament — prohibited.
- Selection occurs **before** any candidate's outcome exposure. Freeze (§11) precedes registration (§V38A Stage 1) precedes measurement (Stage 3).
- No arbitrary numeric cap on parallel *concepts* is set; governance reviews the active validation queue for redundancy (§10) and capital efficiency (§26).

---

## 16. SELECTION OUTCOME STATES

(DESIGN PROPOSAL) Selection outcomes are governance states, NOT validation results:

- **SELECTED FOR BASE REGISTRATION** — candidate is sufficiently specified, object-type-qualified, family-reviewed, and owner-authorized to enter V38A Stage 1 registration. This authorizes *validation only*; it confers no Base status.
- **DEFERRED** — conceptually legitimate but should not consume validation capital yet.
- **REJECTED** — fails object-type, governance, independence, execution, redundancy, or anti-rescue requirements.
- **DATA / DESIGN INSUFFICIENT** — insufficient information to make a responsible selection decision (recorded; may be revisited with new information under a fresh selection review, never by reopening the same validation).

---

## 17. OWNER AUTHORIZATION

(DESIGN PROPOSAL) Ownership follows ratified doctrine's existing governance terminology (the project owner / owner-authorized governance acts):

- research design and screening recommendations are made independently;
- **final Base-hypothesis selection requires owner authorization**;
- owner approval does NOT make the candidate a Base;
- owner approval authorizes entry into V38A registration/validation only.

Recorded distinction: **SELECTED HYPOTHESIS ≠ VALIDATED BASE.**

---

## 18. BASE-HYPOTHESIS REGISTRATION CONTENT

(DESIGN PROPOSAL) Minimum candidate package required before V38A Stage 1 registration:

1. unique hypothesis identifier;
2. decision-process description (complete, deterministic);
3. object-type justification;
4. motivation / provenance (historical-artifact dependencies, if any);
5. declaration of whether prior results motivated selection — and in what role (priority only);
6. declared instrument(s);
7. declared timeframe / timeframe hierarchy;
8. data source;
9. decision rules (entry, exit, participation);
10. execution semantics;
11. outcome definition;
12. cost model (one coherent, frozen, realistic);
13. opportunity-population definition (fixed, attributable);
14. proposed validation scope, including any independent confirmation segment or genuinely new observations;
15. rationale for research priority;
16. explicit no-rescue declaration;
17. explicit Conditional-independence declaration;
18. family / redundancy review;
19. owner selection authorization.

No outcome result is required to "earn" selection. Absence of any mandatory field → the package is not ready and selection is DEFERRED or DATA/DESIGN INSUFFICIENT.

---

## 19. BASE HYPOTHESIS → V38A REGISTRATION TRANSITION

(DESIGN PROPOSAL) The transition is a handoff, not a promotion:

- The frozen hypothesis (§11) becomes the V38A Stage 1 registration object.
- The selection record (this milestone's rationale) is attached as provenance; it is NOT validation evidence.
- The V38A six-stage lifecycle then runs under its own rules (BV1–BV13). Selection controls end at the freeze; validation controls begin at registration.
- No selection-time economic figure is carried forward into Stage 3 measurement. Stage 3 measures the registered decision economics over the complete declared scope.

---

## 20. ANTI-RESCUE ANALYSIS

(DESIGN PROPOSAL) Two audit questions, answered by the controls:

**Q1: Could someone identify a losing historical strategy, select it specifically because a Conditional might rescue it, and pass it through this pathway?**

**NO.** Four independent controls block it: (a) §14 — any selection rationale referencing a future Conditional is a rescue framing and an eligibility blocker; (b) §5 — the object must be a complete standalone decision process, not a carve-out; (c) §8 — historical loss cannot make something *more* selectable (blockers exclude, priority never selects on poor economics); (d) §16/§20 of V38A ratified doctrine — NOT BASE-ELIGIBLE includes rescue construction, and a rescue object can never clear Stage 4.

**Q2: Could a legitimate decision-process concept with no Qualified-Alpha standing nevertheless be selected for prospective Base validation?**

**YES.** Selection criteria are architectural (§10 of the mandate's non-economic list in this design's §5/§10/§18): completeness, execution realism, scope clarity, reproducibility, attribution suitability, Conditional independence, no-rescue motivation, research-value rationale. None of these is an Alpha test. V38A then decides BASE-ELIGIBLE or not holistically, with no profitability gate.

The two answers are produced by the same structure: selection filters on *what the process is and why it is worth asking about*, never on *how much it earned*.

---

## 21. HIDDEN ECONOMIC-GATE AUDIT

(DESIGN PROPOSAL) Sweep of this protocol against universal-eligibility language:

- profitability / expectancy / win rate / Sharpe / drawdown / frequency / sample count / cost-adjusted return / return stability / historical-era performance / best market / best parameter / best regime: **none appears as an eligibility condition anywhere in this design.** Each appears only in §8's three-role separation (blocker/priority/sealed-validation) or in §12's prohibited-mechanisms list. Numerical evidence may inform research priority where governed and recorded; it never takes the form "must exceed X to be selected as a Base."
- The word "viability" in this design always refers to V38A Stage-4 holistic adjudication (BV6), never to a numeric selection bar.

---

## 22. RESEARCH-CAPITAL EFFICIENCY

(DESIGN PROPOSAL) The project's objective is eventual tradeability of a *system*, not research volume. Selection therefore prefers candidates that answer meaningful unresolved architecture questions without combinatorial search:

- interpretable decision processes;
- clear execution and attribution;
- strong governance provenance;
- strategic relevance;
- capacity to support later Conditional research (a real fixed opportunity population);
- forward-justified modern executability.

Deliberately NOT favored: historically profitable candidates, "survivor" candidates, or candidates whose appeal rests on a favorable cell. Scarce validation capital goes to the question worth answering, not the number that looked best.

---

## 23. REQUIRED FUTURE ARTIFACTS

(DESIGN PROPOSAL — FUTURE MILESTONE) Minimum artifacts implied by this design, none created now:

- **Selection / validation design ratification record** (when this design is ratified);
- **Base-hypothesis selection record** (the governed selection decision with rationale, priority evidence, and owner authorization);
- **Base-hypothesis registration** (V38A Stage 1 package, per §18);
- downstream V38A artifacts (validation protocol, results, adjudication, registry entry) per the ratified V38A artifact architecture.

Registry implementation remains a separate later milestone (V38A ratified boundary). This design creates no registry, no records, no candidates.

---

## 24. OPEN DESIGN QUESTIONS

(DESIGN PROPOSAL — genuinely governance-deferred only; nothing resolvable here is left open)

1. **Owner calibration of the priority framework** — the relative weight the owner wants architectural-relevance vs execution-readiness vs data-freshness to carry when the queue is contested. The framework (§9) is complete without a fixed weighting; the owner may set weights at ratification or leave them qualitative.
2. **Whether the first validated hypothesis will be one motivated by a closed artifact (e.g., a modern-scope re-ask of a closed decision-process line) or a de-novo decision-process concept** — a research-strategy choice for the owner at actual selection time, deliberately not prejudged here.
3. **Standing forward-observation policy** — whether the owner wants V38A's optional forward/demo observation to become a standing expectation for Base Registry entry at some later governance revision (V38A left this optional; unchanged here).
4. **Registry implementation detail** — deferred to the separate registry-implementation milestone by V38A ratified boundary; not a selection-design question.

---

## 25. PROPOSED FORMAL BS CLAUSES

(DESIGN PROPOSAL — NOT RATIFIED) Each clause states Requirement / Prohibition / Rationale / Governance consequence. No clause creates a numeric eligibility gate.

**BS1 — Base Object-Type Requirement.**
Requirement: A Base candidate is a complete, deterministic decision process (decision conditions, participation, entry, exit, execution, scope, data source, outcome, cost model). Prohibition: observations, states, events, indicators, thresholds, subsets, Conditional components, and hypothetical P&L cannot be candidates. Rationale: only a decision process yields the frozen opportunity population and single cost model V38A needs for attribution. Consequence: failure → REJECTED at screening, before economics are reviewed.

**BS2 — Selection Provenance.**
Requirement: every candidate carries a provenance record: origin, motivation, prior-artifact dependencies (if any), and the role prior results played. Prohibition: no candidate may enter selection without provenance. Rationale: provenance is what lets governance separate conceptual reuse from result-driven construction. Consequence: missing provenance → DATA / DESIGN INSUFFICIENT.

**BS3 — Closed-Line Firewall.**
Requirement: closed artifacts may motivate a *new*, independently specified hypothesis. Prohibition: no closed artifact, its parameters, its winning era/cell/subset, or its verdict may be imported as the candidate itself or as the candidate's evidence. Rationale: V38 D13 / V38A ratified rules forbid silent recycling. Consequence: violation → REJECTED; any advanced hypothesis citing a closed line must show independent specification.

**BS4 — Historical-Result Separation.**
Requirement: historical economics are sorted into three roles at selection — eligibility blocker, priority evidence, sealed validation evidence. Prohibition: the same figure may not act as both priority evidence and eligibility evidence; blocked candidates may not be re-ranked by outcome. Rationale: role separation is what prevents outcome ranking from becoming selection. Consequence: misclassification → selection record defective; selection re-run under correct roles.

**BS5 — Research-Priority vs Eligibility Separation.**
Requirement: prioritization criteria (architecture, execution readiness, data, novelty, attribution, cost, strategy relevance, negative knowledge) are recorded as *research prioritization*. Prohibition: P&L/expectancy/win-rate/Sharpe/return/best-period ranking may not appear among prioritization criteria. Rationale: priority allocates capital; it must not masquerade as a gate. Consequence: any numeric ranking in a selection record must be labeled priority-only or the record is invalid.

**BS6 — Prospective Selection Freeze.**
Requirement: selection ends at a documented freeze of the hypothesis (identity, scope, rules, cost model, population definition). Prohibition: after freeze, no historical result, parameter, scope, subset, or Conditional result may alter the hypothesis. Rationale: the freeze makes Motivation ≠ Validation (V38A) enforceable. Consequence: post-freeze alteration voids the selection; the change is a new hypothesis requiring a new selection.

**BS7 — Selection Data Boundary.**
Requirement: the selection team defines, in writing before selection, what is inspectable (provenance, governance, failure modes, data availability) and what is sealed (the designated validation window's economics). Prohibition: sealed figures may not be inspected before V38A Stage 4 adjudication. Rationale: separation of selection rationale from validation outcome construction. Consequence: breach → the validation's independence is compromised; adjudication must be re-staged or the hypothesis re-selected with a clean window.

**BS8 — Family Redundancy Control.**
Requirement: candidates are reviewed for architectural family membership; distinct architecture is preferred over parameter variation. Prohibition: near-duplicate re-expressions of one family may not be advanced as multiple candidates, and a closed failed family's re-expression requires a new-mechanism justification. Rationale: prevents redundant generation and family overfitting. Consequence: redundancy finding → DEFERRED or REJECTED with documented reason.

**BS9 — Conditional Independence.**
Requirement: the candidate is fully specifiable with no reference to any future Conditional. Prohibition: selecting a Conditional to make the Base work, filtering opportunities by Conditional success, or adapting the Base to a Conditional. Rationale: V38A requires the Base to exist independently (BV-ratified Conditional independence). Consequence: any such rationale → REJECTED as rescue framing.

**BS10 — Parallel-Candidate Protection.**
Requirement: multiple concepts may be screened; selection of the one advanced to V38A occurs before any candidate's outcome exposure. Prohibition: running multiple V38A validations to pick a passing Base; using validation results as a selection tournament. Rationale: validation is adjudication, not selection. Consequence: violation → affected validations void; fresh selection required.

**BS11 — Owner Selection Authority.**
Requirement: final Base-hypothesis selection requires owner authorization, recorded in the selection record. Prohibition: no research-side recommendation alone may enter a candidate into V38A Stage 1. Rationale: selection is a governance act; ownership resides with the project owner per ratified doctrine. Consequence: unauthorized entry → registration invalid; owner decision recorded and preserved.

**BS12 — Base-Hypothesis / Base Separation.**
Requirement: the protocol labels a selected candidate a BASE HYPOTHESIS, never a Base. Prohibition: selection may not be described as, or treated as, Base creation or validation. Rationale: Base exists only after V38A adjudication and Registry entry. Consequence: mislabeling → corrected in the record; Registry integrity unaffected (Registry remains EMPTY).

**BS13 — Anti-Rescue Selection Protection.**
Requirement: the selection rationale must stand without any assumption that a Conditional will improve the process. Prohibition: selecting a weak or losing process because Conditional research might fix it; rescue-framed registrations. Rationale: V38 D8 / BV13 (No-Rescue) extends backward into selection; SEED-002 remains the governing lesson. Consequence: rescue framing → REJECTED at any point; never a candidate.

---

## 26. FINAL RECOMMENDATION

(DESIGN PROPOSAL) **BASE SELECTION PATHWAY READY FOR RATIFICATION.**

- The pathway is complete: object-type gate → provenance → role-separated economics → family control → priority framework → freeze → data boundary → owner authorization → registration package → V38A handoff.
- The two central success conditions hold by construction, not by aspiration: selection cannot be outcome ranking (§8, §21), and rescue selection is structurally impossible (§14, §20, BS13).
- The pathway creates no Base, no registry, and no candidate; it only defines how a future selection may lawfully occur.
- Ratification of this design authorizes *selection as a governed act*, not selection itself — and never validation.

---

## 27. GIT / REPOSITORY INTEGRITY

Recorded at authoring:

- HEAD before: `4da500b8c365e84062c6bf145af3a0e158ecaa6c` (V38A ratification); branch `main`.
- Change: exactly ONE new untracked design artifact — `output/research_discovery/QUANTFORGE_BASE_HYPOTHESIS_SELECTION_VALIDATION_DESIGN_V1.md`.
- No commit, no staging (design-only milestone).
- `SESSION_HANDOFF.md` intentionally NOT modified (design-only milestone; next milestone depends on this design's verdict).
- No source, test, configuration, governance, ledger, discovery-DB, candidate, or registry change.
- No Base selected or created; Base Registry remains EMPTY; no validation executed; no hypothesis declared.

(GOVERNANCE FACT — carry-forward) The next permissible milestone, if and only if this design is ratified, is **BASE HYPOTHESIS SELECTION / VALIDATION DESIGN RATIFICATION**; only after that may an actual Base-hypothesis selection occur.

**HARD STOP.** Design complete. No selection, no hypothesis, no validation, no registry, no experiment.
