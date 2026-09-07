# QUANTFORGE — V38A BASE VALIDATION PATHWAY DESIGN

**Status:** DESIGN — PENDING OWNER RATIFICATION AS PATHWAY
**Date:** 2026-09-03
**Revision:** V1-r2 (in-place revision, 2026-09-03) — corrective revision following independent review. Prior version SHA-256: `4c4e4780bbaeabe7790e6a614ae37782dbcf8bf2596bfae0ab3cb5b7ada3f52e`. This revision (a) removes implicit economic-gate language from the viability classification, (b) adds the explicit anti-"Alpha-lite" statement, (c) redefines "robustness evidence" as reproducibility-and-interpretability evidence, (d) corrects the validation-stage count to six stages with hypothesis/registration distinguished, (e) resolves the load-bearing open design questions at design level, and (f) revises BV clauses BV5/BV6/BV8/BV13 to preclude any hidden profitability gate.
**Parent doctrine:** V38 Assembled-Decision / Relational Qualification Doctrine (RATIFIED 2026-09-03, commit `c42c3c3`; ratification SHA `1d6810b8…`) — **UNCHANGED by this revision**.
**Nature:** Read-only research-design deliverable. **No Base was created. No Base is selected. No Base hypothesis is authorized. No registry exists. No experiment was executed.**

---

## 1. MISSION

(GOVERNANCE FACT + DESIGN PROPOSAL) Define exactly what a legitimate QuantForge BASE is, how Base viability is established, what evidence permits registry entry, and how the pathway avoids both extremes: (Extreme A) "any decision process can become a Base" — which creates a rescue target; and (Extreme B) "a Base must already be a fully qualified Alpha" — which recreates the measured-dead standalone gate and prevents ever testing whether conditional information creates incremental value. The revision adds a third, load-bearing requirement: **economic metrics remain mandatory evidence but never become a hidden universal economic gate** — no sign, magnitude, or threshold of net expectancy independently determines Base eligibility.

## 2. EVIDENCE BASIS

(GOVERNANCE FACT) V38 clauses D1–D25 bind the design: empty Base Registry (D9); entry only via prospective Clause-D2 validation (D2, D9); no retroactive Base from any closed artifact (D2, D9, D13, D18); No-Rescue rule (D8); negative-standalone conditional components permitted with increment-only qualification (D3, D6); one execution/cost model (D7); depth and permutation controls (D11, D12); firewalls (D13, D14); G1 V3 pillars preserved, no universal numeric gates (D20), qualification holistic.
(GOVERNANCE FACT) The record motivating the design tension: three independent standalone-first economic failures (ORD, TRADEABLE_EDGE V27–V36, H01) show the old gate is inapplicable; SEED-002 shows rescue framing is invalid; H01 era-dependence shows decision context carries economics.
(INFERENCE — now stated as DESIGN PROPOSAL) The load-bearing question this design resolves: how a decision process can be a legitimate increment reference without a standalone-profit requirement and without becoming a rescue target — answered structurally and holistically, never by a numeric rule.

## 3. BASE DEFINITION

(GOVERNANCE FACT) A BASE is a registered, deterministic decision process that determines actual trade participation/execution under a declared scope, data source, outcome definition, execution model, and cost model (V38 D1).

(DESIGN PROPOSAL — sharpening retained from review) A Base is **necessarily a decision process, never an observation**. Direct consequence: CAND-077/081/083 and CAND-099 are state/event observations — not decision processes — and **cannot be Base hypotheses by construction**; their role under V38 is conditional-component characterization. Objects that were complete decision processes (ORD, H01, the TRADEABLE_EDGE candidates) can motivate future Base hypotheses.

Explicit distinctions:

```text
BASE (registered, validated decision process; reference for increments)
≠ QUALIFIED ALPHA (standalone economic value sufficient to trade alone; G1 V3)
≠ CONDITIONAL COMPONENT (information layer admitted to modify a Base)
≠ OBSERVATION (characterized market structure; no decision process)
≠ HYPOTHESIS (unvalidated claim about any of the above)
```

(DESIGN PROPOSAL — anti-"Alpha-lite") **Base status is not awarded because a process is "slightly profitable," "better than zero," or "economically promising." Base status is not a weaker form of Qualified Alpha.** The economic question for Base status is whether the process provides a legitimate, interpretable, non-pathological reference decision context. Alpha qualification remains separate and governed by G1 V3. A Base may therefore carry positive, approximately neutral, or negative decision economics **without the sign alone determining Base status** — while arbitrary or deeply pathological losing processes remain unable to qualify simply because a Conditional might later improve them (anti-rescue is structural and holistic, not threshold-based; see Sections 5 and BV13).

## 4. WHY BASE STATUS IS NECESSARY

(DESIGN PROPOSAL) V38 requires a validated Base before assembled qualification because: (1) a real decision population is the only legitimate measurement substrate — phantom P&L has no population; (2) an actual execution path and one coherent cost model make "increment" economically meaningful rather than arithmetic on hypothetical fills; (3) without a reference decision, State × State layering degenerates into the rescue framing SEED-002 disproved; (4) incremental value is only measurable as a difference against a fixed reference decision. None of this requires the Base to be highly profitable — it requires the Base to be **real and interpretable as a reference**.

## 5. BASE VIABILITY — THE KEY DESIGN PROBLEM

(DESIGN PROPOSAL) Base viability is the holistic determination that a candidate decision process is sufficiently credible, coherent, interpretable, and non-pathological to serve as the reference decision for assembled incremental testing — without Alpha-level qualification and **without any numeric or sign-based gate**.

**No sign, magnitude, or threshold of net expectancy independently determines Base eligibility.** Economic metrics are mandatory evidence; their interpretation is holistic.

### Mandatory viability dimensions (all must be addressed; none is a numeric rule)

| Dimension | Requirement |
|---|---|
| Structural validity | Deterministic, reproducible, leakage-free, prospectively defined decision logic |
| Coherent decision economics | Decision economics are interpretable in light of the declared decision process — the measured behavior is consistent with the declared mechanism and reference meaning; economics are not incoherent with or contradictory to the declared logic |
| Non-pathological behavior | No structural defect such as perverse selection logic, sign instability between gross and net that contradicts declared semantics, or tail/loss behavior that makes the process's reference meaning pathological |
| Reproducibility and interpretability | An independent re-implementation reproduces the registered population and behavior; the process is interpretable as a reference decision context within its frozen scope (Section 11) |
| Execution realism | Entry/exit/cost assumptions are executable in the declared context; no hypothetical fills |
| Stable declared scope | Scope frozen at registration; no dependence of scope on outcome inspection |
| Credible opportunity population | The frozen opportunity population is well-defined and adequate to support an incremental comparison (Section 12); adequacy is adjudicated, not a minimum-N rule |
| No post-hoc construction | No favorable-period, favorable-subset, or outcome-driven selection in defining the process or its population |
| Independence from Conditional components | The Base is defined and validated without reference to any Conditional component's results |
| Not a rescue vehicle | No evidence the process was proposed or retained in order to be "fixed" by Conditional research |

(DESIGN PROPOSAL) Classification is by total evidence, not by economics sign:

**BASE-ELIGIBLE** — the total evidence establishes that the process is structurally valid; deterministic and reproducible; prospectively defined; economically coherent; non-pathological in its gain/loss behavior; realistic under its declared execution/cost context; supported by a credible frozen opportunity population; sufficiently interpretable to function as a legitimate reference decision context; independent of future Conditional-component results; and not constructed or retained as a rescue vehicle.

**INCONCLUSIVE** — evidence is insufficient to establish legitimate reference status, including (not exhaustively): inadequate independent validation evidence; unresolved reproducibility; unresolved execution realism; unstable or poorly understood decision economics; unresolved data sufficiency; insufficiently established opportunity population; unresolved scope integrity. Borderline cases (including processes whose net economics are near zero or ambiguous) are **not** resolved by a numerical boundary; the adjudicator documents, against the complete dimensions and evidence quality, why the process is sufficiently interpretable to serve as a Base, insufficiently established, or affirmatively invalid.

**NOT BASE-ELIGIBLE** — affirmative evidence of structural or conceptual invalidity, including (not exhaustively): leakage; non-deterministic or irreproducible decision logic; pathological loss behavior; demonstrably incoherent decision economics (behavior contradicting the declared decision process such that no reference meaning exists); post-hoc population construction; post-hoc selection; rescue construction; implausible execution assumptions; dependency on Conditional-component outcomes; or other evidence that the process cannot defensibly serve as an independent reference context.

(FUTURE MILESTONE) The final wording of the viability dimensions is settled at V38A pathway ratification; no numeric threshold is created here or there.

## 6. BASE VALIDATION VS ALPHA QUALIFICATION

(DESIGN PROPOSAL) The separation prevents Base status from becoming a hidden "Alpha-lite" badge:

| | BASE VALIDATED | QUALIFIED ALPHA |
|---|---|---|
| Claim | "Legitimate reference decision context; assembled increment tests may reference it" | "Standalone economic value sufficient to trade alone" |
| Evidence | Registered decision process; structural validity; decision economics as evidence; reproducibility-and-interpretability evidence; holistic viability adjudication | G1 V3 standalone qualification standard (existing, unchanged) |
| Economic sign requirement | NONE (sign is evidence within holistic adjudication; never a rule) | Per G1 V3 (existing) |
| Consequence | Conditional research may reference it; no standalone tradeability claim | Standalone/production claims permitted |

Base validation confers **no standalone tradeability claim** and **no profitability claim**. A validated Base is a legitimate decision process whose economics can be measured and incremented — nothing more.

## 7. PROSPECTIVE SCOPE AND DATA FRESHNESS

(DESIGN PROPOSAL) Prospective means: registration freezes — before any outcome evaluation — instrument, date scope, economic convention, decision rule, outcome, execution assumptions, and validation procedure. Scope changes after measurement invalidate the study.

**MOTIVATION ≠ VALIDATION** (retained and strengthened). Motivating observations may inspire a Base hypothesis but may not simultaneously serve as its confirmatory evidence where that would contaminate prospective integrity. Rules:
- Hypothesis motivated by no prior QuantForge result: validation on the full predeclared scope.
- Hypothesis motivated by a prior result (e.g., ORD's or H01's structure): validation must use (a) a genuinely independent confirmation segment not part of the motivating evidence, and/or (b) genuinely new observations postdating the motivating program. Sufficiency is adjudicated per declared hypothesis scope, data availability, and evidence independence — **no universal duration or sample-size threshold**. If neither independent evidence source exists, the study is DATA-INSUFFICIENT (recorded, not entered).

(FUTURE MILESTONE) The H01 contemporary-window data-freshness fact is a registration-time determination for any future modern-era study; not resolvable by this design.

(DESIGN PROPOSAL) Forward/demo evidence: NOT required for registry entry. Historical validation with prospective integrity is the entry standard. Staged forward observation may attach as a standing owner condition when a Base supports extended assembled research; no universal duration invented.

## 8. LEGITIMATE NEW SCOPE VS RETROSPECTIVE RESCUE

(GOVERNANCE FACT + DESIGN PROPOSAL) A new modern-era scope is legitimate when justified **before examining the new study's outcomes**, on forward-looking grounds independent of any historical result's sign: future tradability; current execution environment; relevant data regime; current market structure; current cost environment. LEGITIMATE NEW SCOPE: forward-justified, recorded pre-measurement, full-scope. RETROSPECTIVE RESCUE: scope chosen because a historical segment won; scope narrowed post-measurement; motivating observations reused as validation. H01's contemporary cell is **not** selected as a Base by this document; it remains preserved evidence that could motivate a future, separately justified, fresh-scope study under Section 7.

## 9. BASE VALIDATION LIFECYCLE — SIX STAGES

(DESIGN PROPOSAL — corrected) The pathway comprises **six stages** (Stage 0 and Stage 1 are distinct: hypothesis formulation precedes prospective registration):

```text
Stage 0  Hypothesis formulation   — object-type check (decision process, not observation); decision logic stated; motivation recorded (including prior-result citation, if any); NOT yet a registration
Stage 1  Prospective registration — full freeze (Section 10 fields); scope; forward justification if any; validation procedure; recorded pre-measurement
Stage 2  Structural validation    — implementation, reproducibility, leakage audit, population construction; NO economic outcomes exposed
Stage 3  Economic validation      — registered decision economics measured: gross and net under the frozen cost model, distributional diagnostics, trade frequency; economics are EVIDENCE
Stage 4  Viability adjudication   — BASE-ELIGIBLE / INCONCLUSIVE / NOT BASE-ELIGIBLE by total evidence (Section 5); independent adjudication review → owner decision
Stage 5  Registry entry and lifecycle initiation — entry record; modification/versioning/closure rules (Section 16)
```

Stop conditions: Stage 0 object-type failure → not a Base hypothesis; Stage 1 incomplete freeze → no measurement; Stage 2 structural failure (leakage, non-reproducibility, invalid population) → NOT BASE-ELIGIBLE; Stage 3 incoherent or pathological economics → NOT BASE-ELIGIBLE (by evidence dimension, not by sign); Stage 4 insufficient evidence → INCONCLUSIVE; Stage 4 affirmative invalidity → NOT BASE-ELIGIBLE.

## 10. BASE REGISTRATION — REQUIRED FREEZE FIELDS

(DESIGN PROPOSAL) A Base registration freezes, before measurement:

| Field | Status |
|---|---|
| Decision rule (deterministic, executable specification) | REQUIRED |
| Opportunity population (definition and construction rule) | REQUIRED |
| Instrument(s) | REQUIRED |
| Timeframe(s) | REQUIRED |
| Data source (file identity/hash where applicable) | REQUIRED |
| Signal timing / entry rule | REQUIRED |
| Exit rule / outcome horizon | REQUIRED |
| Direction and position logic | REQUIRED |
| Execution assumptions | REQUIRED |
| Cost model (declared, consistent, realistic for the declared context) | REQUIRED |
| Risk handling (position sizing convention, exposure limits) | REQUIRED |
| Trading calendar / session treatment | REQUIRED |
| Missing-data policy | REQUIRED |
| Look-ahead controls (declared information timing) | REQUIRED |
| Date scope (primary + any predeclared confirmation segment) | REQUIRED |
| Validation procedure (stages, adjudication path) | REQUIRED |
| Motivation (prior-result citation, if any) | REQUIRED |
| Predeclared secondary diagnostics | OPTIONAL |
| Tick-level cost integration | OPTIONAL (only where the declared execution context requires it) |
| Post-hoc scope or parameter changes | NOT ALLOWED |

## 11. EVIDENCE REQUIREMENTS — REPRODUCIBILITY AND INTERPRETABILITY

(DESIGN PROPOSAL — "robustness evidence" redefined) Registry entry does not depend on an undefined "robustness" bar. The required evidence is **evidence sufficient to establish reproducibility and interpretability within the frozen declared scope**, meaning:
- reproducibility of the frozen decision rule (an independent re-implementation reproduces the registered population and behavior);
- stable construction of the opportunity population;
- independent confirmation where appropriate (Section 7);
- consistent execution semantics across the declared scope;
- absence of obvious leakage;
- consistency of the measured behavior with the declared decision process (interpretability).

No universal statistical threshold, mandatory sample size, Sharpe ratio, win-rate threshold, expectancy threshold, p-value, or minimum-market-count requirement is created (none such exists in higher-level authoritative governance for this purpose). Evidence classes required before entry: (1) **Structural** — determinism, reproducibility, no leakage, valid population (Stage 2); (2) **Economic** — decision economics as evidence, gross and net, distributional diagnostics, trade frequency (Stage 3); (3) **Reproducibility-and-interpretability evidence** as defined above; (4) **Prospective integrity** — registration predates measurement; motivation ≠ validation (Section 7). Forward/live evidence: not required for entry.

## 12. OPPORTUNITY POPULATION — FREEZE AND ATTRIBUTION DISTINCTION

(DESIGN PROPOSAL) Two concepts are explicitly distinguished:

**Base population definition** — the complete set of decisions the registered rule produces over the declared scope, constructed at Stage 2 under the frozen rule, with a documented policy for filtered opportunities, excluded trades, delayed entries, missed trades, unavailable data, repeated events, and overlapping decisions. **Frozen at registry entry.**

**Assembled decision eligibility** — the subset question asked later by the Conditional layer: which Base opportunities may be acted upon, with altered entry/confirmation/execution behavior only per the predeclared assembly design. A Conditional component may modify whether a Base opportunity is acted upon and how it is executed under the predeclared design; it **may not redefine the Base opportunity universe and may not retroactively remove unfavorable Base opportunities from the Base population**. The frozen Base population is the exclusive measurement substrate; component-driven exclusions are measured decision consequences, never definitional edits. Adequacy of the population to support an incremental comparison is adjudicated (credible-opportunity dimension), not set by a minimum-N rule.

## 13. COST / EXECUTION INTEGRITY

(DESIGN PROPOSAL — retained) One coherent cost model per Base context; costs frozen at Base registration; realistic for the declared execution context (spread, slippage, commission, execution delay, missed fills, market-specific costs, using existing cost doctrine — the 2.0 bps round-trip convention where the declared context matches the M1-CFD family, context-specific models where justified); no opportunistic cost adjustment; assembled tests inherit the Base execution/cost context unless a future governance revision explicitly permits otherwise. **The cost model measures execution realism; it does not create a universal profitability gate** — costs are evidence within holistic adjudication, never a sign/magnitude rule on net economics.

## 14. BASE REGISTRY ENTRY CRITERIA

(DESIGN PROPOSAL — no implicit profitability gate) A decision process enters the (still-empty, not-yet-existing) Base Registry when the holistic adjudication finds: **Structural validity + reproducibility-and-interpretability evidence (Section 11) + economically coherent and non-pathological decision economics (as evidence) + execution realism + prospective integrity**, under **owner approval on independent adjudication-review recommendation**. No single mathematical cutoff exists; no sign or magnitude of net expectancy is a rule. Entry is recorded with: decision-rule reference, scope, cost model, population definition, validation-study reference, and entry date.

## 15. BASE REGISTRY PROTECTIONS

(DESIGN PROPOSAL — retained) The registry and entry process prevent: retroactive insertion; favorable-period insertion; post-hoc scope changes; parameter modifications after outcome exposure; historical-subset carving; **conditional-component contamination** (a Base may not be defined or adjusted using observations produced by a Conditional component's results); result-driven construction; and **parallel-winner selection** (competing Bases for the same decision context may not be evaluated keeping only the best outcome; each registration is independent and adjudicated on its own merits; comparative post-hoc selection across registrations is not an entry mechanism).

## 16. VERSIONING / MODIFICATION / CLOSURE

(DESIGN PROPOSAL — retained) Default rule: **a material decision-rule change creates a new Base hypothesis and a new validation study, never an edit to existing Base status.** Distinctions: (a) *implementation bug fix* — defect demonstrable independent of outcomes, corrected with documented provenance, re-verified against the same registration (a patch, not a redesign); (b) *methodological modification* — any change to decision rule, scope, population, cost model, or outcome = new Base version requiring re-validation under a new registration; (c) *Base redesign* — new hypothesis, new study; the prior Base may be retired. Governance: patches recorded against the Base record; modifications open a new registration; retirement/closure requires an owner decision with recorded reason. A closed Base returns only through a new hypothesis satisfying prospective integrity. Registry versioning artifacts are design-level; not implemented.

## 17. BASE LIFECYCLE

(DESIGN PROPOSAL — retained) Using existing lifecycle vocabulary where applicable:

```text
HYPOTHESIS → REGISTERED → VALIDATED → BASE-ELIGIBLE → BASE REGISTERED → CONDITIONAL RESEARCH AVAILABLE → RETIRED / CLOSED
```

Adjudication: Stage 2–3 outputs reviewed by an independent adjudication review; BASE-ELIGIBLE / INCONCLUSIVE / NOT BASE-ELIGIBLE determinations and registry entry are owner decisions on that review's recommendation. Closure evidence: structural invalidity, non-reproducibility, incoherent or pathological economics, unstable scope, unresolvable cost ambiguity, post-hoc dependence, or repeated failure under prospective validation. A closed Base returns only via a new governed hypothesis; a new scope on the same underlying decision logic = a new Base hypothesis.

## 18. EXISTING ARTIFACT DISPOSITION

(GOVERNANCE FACT + DESIGN PROPOSAL — unchanged by this revision)

| Object | Classification |
|---|---|
| CAND-077 / CAND-081 / CAND-083 / CAND-099 | **CANNOT BE BASE** — state/event observations, not decision processes; conditional-component characterization only |
| H01 contemporary observation | **CAN MOTIVATE FUTURE BASE HYPOTHESIS** (never a Base itself); fresh-scope prospective validation required (Sections 7–8); H01 stays CLOSED |
| ORD | **CAN MOTIVATE FUTURE BASE HYPOTHESIS**; fresh validation required; ORD stays CLOSED |
| TRADEABLE_EDGE candidates | **CAN MOTIVATE FUTURE BASE HYPOTHESIS** (individually); subject to family redundancy rules and prospective integrity |

No object is reopened; no object is a Base; no prior result becomes a Base by reinterpretation; motivation confers no status. No Base candidate is created.

## 19. HTF / LTF COMPATIBILITY

(DESIGN PROPOSAL — retained) A future Base may be a complete hierarchical decision process — HTF context → structural condition → LTF trigger/confirmation → execution — provided the entire stack is a single deterministic decision rule **frozen together at registration** and validated as one Base. **Frozen-inside architecture** (layers part of the registered decision rule; evaluated as the Base; not conditional components) is distinguished from **post-registration conditional augmentation** (anything added after registry entry to modify decisions = a Conditional component). This preserves V38 D15 without confusing internal architecture with external conditionals.

## 20. FUTURE LIQUIDITY RESEARCH COMPATIBILITY

(DESIGN PROPOSAL — retained) A future liquidity-oriented decision process could theoretically be validated as a Base hypothesis through this pathway — via a fresh prospective hypothesis and full relational admission (V38 D16) before operationalization. Liquidity remains an unvalidated future hypothesis. NOT PERMITTED here: liquidity definitions, thresholds, zones, entry rules, candidates, or experiments.

## 21. CONDITIONAL-RESEARCH DEPENDENCY

(GOVERNANCE FACT — explicit)

```text
NO VALIDATED BASE  →  NO ASSEMBLED ECONOMIC TEST  →  NO CONDITIONAL QUALIFICATION
NO VALIDATED BASE  →  conditional observations may still be characterized and preserved
                       (no assembled economic qualification)
```

Characterization knowledge continues regardless of Base existence; assembled economic qualification does not begin until the Base Registry holds an entry. No dead knowledge is created by the Base requirement.

## 22. HYPOTHESIS / BASE / CONDITIONAL STATE TRANSITIONS

(DESIGN PROPOSAL — retained) Legality of each status:

| Status | Legal when |
|---|---|
| OBSERVATION | any characterized market structure with provenance |
| HYPOTHESIS | recorded claim with mechanism; no measurement claims |
| BASE HYPOTHESIS | object is a decision process; motivation recorded; NOT a retroactive subset (Stage 0) |
| BASE REGISTERED | Stage 1 prospective registration frozen (Section 10) |
| BASE VALIDATED / BASE-ELIGIBLE | Stage 4 viability adjudication + owner approval (Section 5) |
| BASE REGISTERED (registry entry) | entry record fixed (Section 14) |
| CONDITIONAL COMPONENT | admitted via research-stage path (V38 D10) for a specific relational purpose; never needs standalone expectancy |
| RELATIONAL HYPOTHESIS | predeclared Base × Component pairing registered (V38 D4/D12) |
| ASSEMBLED DECISION | one execution/cost model over the frozen Base population (V38 D5/D7) |
| QUALIFICATION | increment-over-Base established, holistic adjudication (V38 D6); system qualification later |

## 23. REQUIRED GOVERNANCE ARTIFACTS

(DESIGN PROPOSAL — minimum, none created) Five artifacts for the future pathway: Base hypothesis registration (Stage 0/1); Base validation protocol; Base validation result; Base adjudication record; Base registry entry record. Registration and protocol frozen pre-measurement; result and adjudication follow measurement; entry record is the single authoritative registry mutation. Registry implementation is a separate later milestone (V38 D24).

---

## 24. PROPOSED BV CLAUSES — COMPLETE REVISED BV1–BV13

(DESIGN PROPOSAL — NOT RATIFIED.) Each clause: Requirement (R), Prohibition (P), Rationale (W), Governance consequence (G).

**BV1 — Base definition.**
R: A Base is a registered, deterministic decision process determining actual trade participation/execution under a declared scope, data source, outcome definition, execution model, and cost model. P: No observation, state, event, indicator, historical subset, hypothetical P&L, or post-hoc combination may be a Base. W: Only real decision processes can be increment references. G: Object-type check at hypothesis formulation; non-decision-process objects are ineligible by construction.

**BV2 — Base legitimacy.**
R: A Base hypothesis records its decision logic, motivation (including any prior-result citation), and proposed scope before any measurement. P: Retrospective subset creation; favorable-period scoping; motivation ≠ validation violations. W: Legitimacy is established by prospective record, not outcome. G: Unregistered measurement is void.

**BV3 — Prospective registration.**
R: Registration freezes all Section 10 REQUIRED fields pre-measurement; any post-measurement field change invalidates the study. P: Scope, parameter, or population changes after outcome exposure. W: The freeze is the anti-retrospection mechanism. G: Deviations close the study as NOT BASE-ELIGIBLE.

**BV4 — Structural validation.**
R: Stage 2 establishes determinism, reproducibility, leakage-freedom, and valid population construction; no economic outcomes are exposed. P: Economic exposure before structural sign-off. W: Structure must precede economics. G: Structural failure closes the study as NOT BASE-ELIGIBLE.

**BV5 — Economic validation (economics as evidence, not gates).**
R: Stage 3 measures the registered decision economics — gross and net under the frozen cost model, distributional diagnostics, trade frequency — over the full predeclared scope. Economic metrics are **required evidence for holistic viability adjudication; they are not universal qualification thresholds**. No sign, magnitude, or threshold of net or gross expectancy, win rate, drawdown, volatility, Sharpe, sample count, or p-value is a Base-eligibility rule. P: Subset reporting as primary evidence; post-hoc metric selection; treating any single economic statistic as an automatic pass/fail. W: Economics are evidence; interpretability and structure adjudicate. G: Metrics are predeclared in the registration and interpreted holistically.

**BV6 — Viability adjudication (holistic).**
R: Stage 4 classifies BASE-ELIGIBLE, INCONCLUSIVE, or NOT BASE-ELIGIBLE by **total evidence** against the viability dimensions of Section 5. BASE-ELIGIBLE requires the ten attributes of Section 5 (structural validity; determinism and reproducibility; prospective definition; economic coherence; non-pathology; execution realism; credible frozen opportunity population; interpretability as a reference decision context; independence from Conditional-component results; not a rescue vehicle). INCONCLUSIVE covers insufficient evidence on any dimension. NOT BASE-ELIGIBLE requires affirmative evidence of structural or conceptual invalidity (leakage; irreproducibility; pathology; incoherent decision economics; post-hoc construction; rescue construction; implausible execution; Conditional dependence). **No sign, magnitude, or threshold of net expectancy independently determines the classification.** Borderline cases are adjudicated on the complete dimensions, with the adjudicator documenting why the process is sufficiently interpretable as a Base, insufficiently established, or affirmatively invalid. P: Automatic status rules keyed to positive/zero/negative economics; entry on weak evidence; deliberate selection of an arbitrary or deeply pathological losing process as a research anchor. W: The tension between Extreme A and Extreme B is resolved by dimensional coherence and interpretability, not by a profit bar or a loss bar. G: Classification is an independent adjudication-review recommendation; the owner decides entry.

**BV7 — Motivation–validation separation and data freshness.**
R: Motivating observations may not serve as validating observations; motivated hypotheses require a genuinely independent confirmation segment and/or genuinely new observations not part of the motivating evidence; if neither exists, the study is DATA-INSUFFICIENT. Sufficiency is adjudicated per declared scope, data availability, and evidence independence — no universal duration or sample threshold. P: Reusing motivating results as validation. W: Prospective integrity requires validation independent of discovery. G: DATA-INSUFFICIENT studies are recorded, not entered.

**BV8 — Base registry entry (no implicit profitability gate).**
R: Entry requires structural validity + reproducibility-and-interpretability evidence + economically coherent and non-pathological decision economics (as evidence) + execution realism + prospective integrity, adjudicated holistically and approved by the owner; the entry record fixes the decision rule, scope, cost model, population, and validation reference. The entry chain encodes **no implicit profitability gate**. P: Entry on a single economic statistic; entry by comparative post-hoc selection among parallel candidates; entry of rescue vehicles or arbitrary/pathological processes. W: Entry is a governed mutation establishing a reference context, not a profitability certification. G: Registry entry authorizes assembled research referencing the Base; it confers no standalone tradeability claim.

**BV9 — Registry protections.**
R: The entry process prevents retroactive insertion, favorable-period insertion, post-hoc scope/parameter change, subset carving, conditional-component contamination of Base definition, and parallel-winner selection. P: Any of the foregoing. W: Protections keep the reference decision clean. G: Violations void the affected Base record.

**BV10 — Versioning, modification, closure.**
R: Implementation bug fixes are patched against the registration with outcome-independent provenance; methodological modifications open a new Base version/study; redesign opens a new hypothesis; closure is an owner decision with recorded reason; a closed Base returns only via a new prospective hypothesis. P: Editing historical Base status to reflect new results. W: Material change = new evidence, not new history. G: Records are append-only.

**BV11 — Opportunity-population freeze.**
R: The Base's opportunity population is constructed at Stage 2 under the frozen rule and fixed at registry entry as the exclusive substrate for assembled comparisons; the Base population definition and assembled-decision eligibility are distinct concepts (Section 12); components may condition decisions but never redefine the universe or retroactively remove Base opportunities. P: Component-driven population redefinition or retroactive removal. W: Attribution requires a stable reference universe. G: Population definition is part of the entry record.

**BV12 — Conditional eligibility dependency.**
R: No assembled economic test and no conditional qualification occurs without a Base registry entry; conditional observations may be characterized and preserved regardless. P: Assembled testing against unvalidated references or processes disqualified at adjudication. W: The Base requirement is the anti-phantom and anti-rescue structure (V38 D8). G: Experiments without a registry entry are void.

**BV13 — Anti-rescue protection (structural, not threshold-based).**
R: Base status may never be used as a rescue mechanism: a process proposed or retained for the purpose of being "fixed" by Conditional research is NOT BASE-ELIGIBLE, and arbitrary or deeply pathological losing processes cannot qualify simply because a Conditional might later improve them. Disqualification operates through the structural dimensions — rescue construction, pathology, incoherent decision economics, irreproducibility, implausible execution — not through a sign or magnitude rule. The primary question of any assembled test remains whether a predeclared Conditional improves a legitimate reference decision; SEED-002 is the recorded lesson. P: Rescue framing in any registration or test; proposing a Base because it is deeply negative. W: Anti-rescue must be structural so that no gate can be gamed and no sign rule can exclude a legitimate reference. G: Rescue-framed registrations are rejected at admission; rescue-framed tests are void.

---

## 25. INTERNAL DESIGN AUDIT — RESCUE LOOP AND HIDDEN GATES

(Result of the dedicated internal audit required by review, reported for the record.)

**Rescue-loop check.** Q: Could a researcher deliberately select a structurally weak or economically poor process, label it Base, and use Conditional research to rescue it? A: **NO** — the entry chain requires structural validity, reproducibility, economic coherence, non-pathology, execution realism, prospective integrity, interpretability as a reference, and independence from Conditional results, each adjudicated against affirmative evidence; rescue construction and pathology are NOT BASE-ELIGIBLE categories; and no sign rule exists that a "weak" process could satisfy by being merely negative. Q: Could a legitimate but non-Alpha decision process qualify when the complete evidence establishes coherent, interpretable, non-pathological reference behavior? A: **YES** — no Alpha-level or positive-expectancy requirement exists; the gate is reference-legitimacy, not profitability.

**Hidden-gate sweep.** The revised text was swept for language that would make a universal eligibility threshold of: net/gross expectancy, cost floor, win rate, drawdown, Sharpe, volatility, sample count, trade count, p-values, confidence intervals, frequency, minimum/maximum return, minimum edge, or minimum improvement. Findings: no such universal rule remains. Numerical metrics appear only as predeclared evidence within holistic adjudication (BV5/BV6/BV8), and the classification language is exclusively dimension- and evidence-based. The cost floor appears only as a realism description (Section 13), not as an eligibility comparator.

---

## 26. EXECUTIVE DESIGN VERDICT

The revised pathway is **genuinely ready for ratification** as the V38A Base Validation Pathway. It establishes the required balance precisely: a Base does NOT need to be Qualified Alpha (no standalone-profit or sign requirement exists); a Base cannot be an arbitrarily weak or pathological process kept alive because Conditional research might rescue it (exclusion is structural — rescue construction, pathology, incoherence, irreproducibility — adjudicated on total evidence); and economic metrics remain mandatory evidence for holistic viability adjudication rather than a hidden universal economic gate (BV5/BV6/BV8). No Base was created, selected, or hypothesized; the Base Registry remains EMPTY; no experiment was executed.

## 27. REMAINING OPEN QUESTIONS

(Only questions truly requiring a later governance decision remain. Previously load-bearing questions — borderline practice, risk-metric substitution, second-opinion universality, confirmation-segment sufficiency — are resolved at design level above and are NOT listed here.)

1. Final wording of the Section 5 viability dimensions for adoption at V38A pathway ratification (structure settled; wording ratified).
2. Whether a standing-condition forward-observation requirement attaches to Bases later supporting extended assembled research (recommended optional; owner decision at ratification or pathway operation).
3. Registration-time empirical facts for any specific future Base hypothesis (e.g., H01 contemporary-window data freshness; ORD-family data adequacy) — determined at each hypothesis's Stage 0/1, not by this design.
4. Registry artifact architecture and versioning records — implementation-milestone detail (V38 D24), not design.

## 28. RATIFICATION BOUNDARY

(GOVERNANCE FACT) V38 remains **ratified and unchanged** by this revision. V38A remains **unratified** until a separate ratification milestone. The Base Registry remains **EMPTY**. **No Base exists. No Base validation has occurred.** This document is a design proposal; its BV clauses are not ratified.

## 29. REPOSITORY / GIT INTEGRITY

HEAD before revision: `c42c3c389c61b07d57ff6c6e01b31537a73d1e5d`. HEAD after revision: identical (no commit made). Changed file: only `output/research_discovery/QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_DESIGN_V1.md` (in-place revision; prior SHA-256 `4c4e4780…` recorded in the header). `docs/SESSION_HANDOFF.md`: **unchanged** (design-only milestone). No source, test, or configuration file changed. `git diff --check`: clean. No staging; no commit; no unrelated modification.

---

**HARD STOP.** No ratification, no Base hypothesis selection, no Base validation, no registry implementation, no assembled or conditional testing. The only next permissible milestone is **V38A BASE VALIDATION PATHWAY RATIFICATION**, provided the revised design satisfies the governance requirements.
