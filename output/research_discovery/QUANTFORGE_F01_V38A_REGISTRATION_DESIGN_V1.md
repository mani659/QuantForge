# QUANTFORGE — F-01 V38A REGISTRATION DESIGN V1

**Milestone:** F-01 Base Hypothesis Freeze / V38A Registration Design (Stage-1 preparation)
**Status:** REGISTRATION DESIGN COMPLETE — **F-01 V38A REGISTRATION READY FOR FREEZE**
**Parent governance:** V38 (RATIFIED); V38A (RATIFIED, BV1–BV13); BS1–BS13 (RATIFIED); BF1–BF13 (RATIFIED); Formulation Cycle V1 (SHA `655473e2a863`); Selection Final V1 (SHA `3097b776cb00`)
**This document converts the selected hypothesis F-01 into a deterministic, immutable, prospective Stage-1 registration specification. It validates nothing, computes no economics, and creates no Base status.**
**SESSION_HANDOFF intentionally NOT modified** (registration-design milestone; §32 of milestone mandate).

Label conventions: GOVERNANCE FACT / REGISTRATION DESIGN (FROZEN) / REGISTRATION DESIGN (TO BE FROZEN AT EXECUTION) / AUDIT / NOT PERMITTED.

---

## 1. EXECUTIVE REGISTRATION VERDICT

**F-01 V38A REGISTRATION READY FOR FREEZE.**

F-01 — Session-Partition Reference Process (Overnight Exposure Leg) — has been converted into a complete, deterministic, prospective V38A Stage-1 registration package. Every material operational semantic is frozen in this document: instrument identity, session definition, position semantics, opportunity population, outcome definition, cost model, execution model, validation scope, and reporting plan. No tunable parameter exists (F-01 has zero), and no operational definition was chosen by inspecting any historical outcome.

Two items are classified as **execution-time mechanical completions** (not design defects): the concrete data-snapshot hash and the concrete calendar artifact are produced when the Stage-2 pipeline runs (§23). All ten registration-integrity gates R1–R10 pass on the specification (§22). The next milestone is **F-01 V38A REGISTRATION FREEZE / EXECUTION AUTHORIZATION**; nothing in this document executes Stage 2 or later.

The registered object remains a **hypothesis**. It is not Base status, not validated, not Registry-eligible, not Qualified Alpha.

## 2. GOVERNANCE STATE

(GOVERNANCE FACT) Verified at authoring:

- V38 = RATIFIED (`c42c3c3`); V38A = RATIFIED (`4da500b`, BV1–BV13, six-stage pathway); BS1–BS13 = RATIFIED (`9a2492f`); BF1–BF13 = RATIFIED (`4edbfdb`).
- F-01 = **SELECTED BASE HYPOTHESIS** (Selection Final V1, SHA `3097b776cb00`); F-02 / F-03 = DEFERRED for the first slot.
- BH-01 = WITHDRAWN; H01 = CLOSED; ORD = CLOSED; TRADEABLE_EDGE exhausted; CAND-077/081/083/099 remain observations; CAND-015/024/035 protected-forward and excluded.
- Base Registry = **EMPTY**; no Base exists; no V38A validation has executed.
- HEAD `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`, branch `main`.

## 3. SELECTED HYPOTHESIS IDENTITY

(GOVERNANCE FACT) The selected hypothesis, immutable per §4 of the milestone mandate:

> **F-01 — Session-Partition Reference Process (Overnight Exposure Leg):** on every eligible trading day, hold one liquid US equity index from the defined session close to the next defined session open (long); flat from the open to the close; exactly one decision opportunity per eligible trading day.

Immutable elements (NOT subject to redesign): overnight architecture; long/flat structure; session-partition concept; one-opportunity-per-day structure. This milestone resolves operational ambiguity only (§5 of the mandate).

## 4. PROVENANCE AND HISTORICAL-KNOWLEDGE BOUNDARY

(GOVERNANCE FACT / AUDIT)

- **Formulation provenance:** first-principles session-structure reasoning committed pre-outcome in the governed formulation cycle (Formulation Cycle V1 §7); no repository outcome consulted; no closed-artifact element imported.
- **Selection provenance:** Selection Final V1 §7 — selected as the cleanest legitimate reference decision process (zero parameters, cleanest population, untested decision class); explicitly NOT selected for any historical result.
- **Documented tension (carried forward, not concealed):** the long-overnight direction is mechanism-predicted and coincides with a widely documented external empirical regularity. Governance response: motivation ≠ validation (V38A §7); the entire motivating knowledge base — including the repository archive and the external prior — is motivation only and can never become validation evidence (§13).
- **Historical-knowledge boundary for this document:** no historical economics were read or used to make any decision in this document. Facts used are governance and data-infrastructure facts only (symbol mapping, normalization decision, timezone convention, V38A stage semantics).

## 5. EXACT DECISION RULE

(REGISTRATION DESIGN — FROZEN)

For each eligible trading day t in the declared validation window:

1. At the defined session close of day t (16:00 ET; 13:00 ET on early-close days), enter a long position in the registered instrument at the registered execution price, full declared notional.
2. Hold the position through the overnight interval.
3. At the defined session open of day t+1 (09:30 ET), exit the position at the registered execution price.
4. Remain flat from the session open to the session close of day t+1.
5. One position per eligible session; no pyramiding; no intraday management; no stop, target, or discretionary intervention.

If day t has no valid session close, or day t+1 has no valid session open, the leg is a recorded no-trade decision in the population (§10). No other conditioning exists: no signal filter, regime filter, volatility gate, drawdown rule, trend filter, or Conditional content (§17).

## 6. INSTRUMENT IDENTITY

(REGISTRATION DESIGN — FROZEN)

**Instrument: `USATECHIDXUSD` (logical symbol), executed as the Exness MT5 symbol `USTECm` — a Nasdaq-100 index CFD.**

- **Index/underlying:** Nasdaq-100 (liquid US equity index product).
- **Data identifier:** `USATECHIDXUSD` (logical) / `USTECm` (broker symbol); mapping `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0` per the frozen symbol-mapping decision.
- **Venue/market convention:** Exness Technologies Ltd, Exness-MT5Trial15 server, read-only MT5 connection.
- **Currency:** USD.
- **Series type:** CFD on the Nasdaq-100 index (executable instrument); the daily session-bar research series is derived from the CFD's M1 bars (§7, §15).
- **Execution semantics support:** YES — the CFD trades through the overnight interval, so close-to-open holding is genuinely executable (no gap-fill fiction).

**Resolution rationale (no performance consulted — AUDIT):** (1) F-01 requires a *tradable* liquid US equity index with real open AND close observations; the FRED close-only daily series (SP500, DJIA, NASDAQ100, NASDAQCOM) are research/reference series with **no open price** and cannot support close-to-open semantics at all — excluded on feasibility. (2) Among executable options with repository-grounded governance, `USATECHIDXUSD/USTECm` is the only one with an established data feed, normalization decision, frozen symbol mapping, and forward accrual pipeline. (3) Class membership: a Nasdaq-100 index CFD is within the formulation's declared class ("one liquid US equity index"; "S&P 500" was an example, not a commitment — the selection artifact listed instrument identity as a registration decision). (4) Governance cleanliness: reuse of the established logical symbol avoids new data-acquisition governance. **No historical performance of any candidate instrument was inspected; identity is resolved by execution realism, data availability, and governance cleanliness only.**

## 7. EXECUTION INSTRUMENT / RESEARCH SERIES RELATIONSHIP

(REGISTRATION DESIGN — FROZEN)

- **Directly executable instrument:** the `USTECm` CFD on the Exness MT5 connection.
- **Research/reference series:** daily session bars derived from `USATECHIDXUSD/USTECm` M1 bars (§15), representing the executable instrument's own prices — **the measured series IS the executable instrument's price**, so no unmeasured mapping gap exists.
- **Documented limitations (recorded, not hidden):** (1) the CFD price is not identical to the underlying Nasdaq-100 index level (CFD carries broker spread/markup; the frozen cost model covers the CFD execution context — §12); (2) the CFD's continuous trading means the "overnight interval" is a defined measurement interval, not a market-closed interval; (3) broker/server timezone conventions are translated to `America/New_York` per the established normalization rule.
- **Execution claim:** the registration measures and claims "hold the USTECm CFD from underlying-session close to next underlying-session open." No claim is made about the index level itself.

## 8. SESSION DEFINITION

(REGISTRATION DESIGN — FROZEN)

- **Timezone:** all session boundaries are defined in `America/New_York` (EST/EDT). Bar timestamps from the feed are translated to `America/New_York` before boundary comparison, per the established normalization decision (dynamic translation via UTC handles DST shifts).
- **Regular session open:** 09:30 ET.
- **Regular session close:** 16:00 ET.
- **Early-close sessions:** 13:00 ET close, per the declared calendar source.
- **Holidays/weekends:** non-trading days per the declared calendar source; no session, no decision, no population entry.
- **Special sessions:** none recognized beyond the declared calendar; any unexpected feed bar outside the declared calendar does not create a session.
- **Daylight-saving transitions:** boundaries are wall-clock in America/New_York; the UTC translation handles the transition; a 23-hour or 25-hour overnight interval is measured as actually observed (no adjustment).
- **Missing session observations:** a session with no valid bar at/after the open boundary, or no valid bar at/before the close boundary, is a missing session — handled in §10.
- **Deterministic reproducibility:** two independent implementations using the same calendar source, timestamp translation rule, and bar-selection rule must produce identical sessions.

(REGISTRATION DESIGN — TO BE FROZEN AT EXECUTION) The concrete calendar artifact (machine-readable NYSE/Nasdaq trading calendar, including early-close dates) is produced and hashed at Stage-2 pipeline construction (§23 item 2).

## 9. POSITION SEMANTICS

(REGISTRATION DESIGN — FROZEN)

- Entry at the defined session close of day t (16:00 ET / 13:00 ET early close).
- Exit at the defined session open of day t+1 (09:30 ET).
- Flat outside the overnight interval.
- Exactly one position per eligible session; no pyramiding; no intraday management; no stop/target; no discretionary intervention.
- Full declared notional on each leg; position size constant across legs (no sizing rule — sizing is a registration parameter set to 1.0 notional unit).
- No short exposure at any point (long/flat only — §10 of the milestone mandate).

## 10. OPPORTUNITY POPULATION

(REGISTRATION DESIGN — FROZEN)

**Definition:** the set of overnight legs L_t for every session t in the declared validation window such that:

- session t has a valid session-close bar (last valid M1 bar at/before the close boundary), AND
- session t+1 has a valid session-open bar (first valid M1 bar at/after the open boundary).

Each such leg is exactly one decision (participate). Every other case is a **recorded no-trade decision** with a defined status:

| Case | Status |
|---|---|
| t missing close (no valid bar ≤ close boundary) | NO-TRADE — MISSING CLOSE |
| t+1 missing open (no valid bar ≥ open boundary) | NO-TRADE — MISSING NEXT OPEN |
| t+1 is a holiday/weekend (no session) | NO-TRADE — NO NEXT SESSION |
| duplicate timestamps at a boundary | bar-selection rule resolves deterministically (§15); no population ambiguity |
| early close | close boundary = 13:00 ET per calendar; normal leg |
| partial session (valid close, no next open; or valid open, prior close missing) | recorded no-trade with the applicable status |

- The population is **enumerable before any outcome is measured** (given the calendar and the frozen data, the eligibility computation is deterministic).
- The population definition is part of the registration and becomes **immutable at registry entry** (V38A §10 population clause).
- The population ledger records every session in the window with its decision and status — nothing is silently dropped.

## 11. OUTCOME DEFINITION

(REGISTRATION DESIGN — FROZEN)

- **Raw result:** per-leg log return r_t = ln(open_{t+1} / close_t), where open_{t+1} and close_t are the registered bar prices of the leg.
- **Direction:** long only.
- **Gross result:** r_t (no costs).
- **Net result:** r_t − (c_entry + c_exit), where c_entry and c_exit are the frozen one-way costs in log-return units (§12).
- **Return unit:** log return per overnight leg, reported in basis points (1 bp = 0.0001) and dimensionless ratio where stated.
- **Aggregation:** population mean and median of net (and gross) per-leg returns over the primary and confirmation segments separately and combined; population count and legs-per-trading-day frequency.
- **Exceptional sessions:** no-trade legs contribute no outcome observation; they are reported in the population ledger, not excluded silently.
- **Predeclared secondary diagnostics (only these):** standard deviation and P10/P90 of the per-leg net distribution; per-calendar-month leg counts; gross-minus-net cost burden per leg. No additional metrics may be introduced after measurement and labeled primary (V38A §11: metrics predeclared, interpreted holistically).

## 12. COST MODEL

(REGISTRATION DESIGN — FROZEN)

- **Convention:** per-leg entry + exit costs applied symmetrically; one coherent model; no spread/slippage/commission decomposition required.
- **Base case:** c_entry = 1 bp (0.0001); c_exit = 1 bp (0.0001) → 2 bps per overnight leg.
- **Stress case:** c_entry = 5 bps; c_exit = 5 bps → 10 bps per overnight leg.
- **One-way vs round-trip:** costs are declared per leg (entry + exit), matching the formulation (§7 of Formulation Cycle V1: "1 bps entry + 1 bps exit base (2 bps per overnight leg), 5 bps stress").
- **Context justification:** liquid index-CFD execution on the registered broker; the CFD trades through the interval so both boundary fills are ordinary market orders.
- **Frozen prospectively:** no cost value may be altered after outcome exposure; no cost search is permitted; the cost model is **not a profitability gate** (V38A: one coherent frozen cost model; economics are evidence, not thresholds).

## 13. VALIDATION SCOPE

(REGISTRATION DESIGN — FROZEN)

**Validation scope = forward-only, unseen data accruing after the registration freeze.**

- **Validation-eligible evidence:** daily session observations with session-open timestamps **on or after the registration-freeze date (2026-09-03)**, accruing forward.
- **Sealed evidence (motivation/provenance only, never validating):** all pre-freeze data — the repository's USATECHIDXUSD/XAUUSD M1 archives, the FRED daily close series, the H01-era windows, and any other pre-freeze observation. The external prior on the overnight direction is likewise motivation only.
- **Reasoning (per milestone §14 — not automatically forward-only, decided on the merits):** F-01's directional content is influenced by external prior knowledge; the strongest prospective posture consistent with V38A's motivation≠validation clause (V38A design: "genuinely new observations postdating the motivating program") is to validate exclusively on observations postdating the registration freeze. The repository archive is not merely inconvenient history — it overlaps the project's own research arc, and reusing it would weaken the prospective integrity this registration exists to establish. Forward-only is therefore selected deliberately, not by default.
- **No historical segment** is included; the validation window is defined by the freeze date and the predeclared segments (§14), not by any historical boundary.

## 14. PRIMARY / CONFIRMATION SEGMENTS

(REGISTRATION DESIGN — FROZEN, declared before any results exist)

- **Primary segment:** trading days with session-open timestamps from the freeze date through the freeze date + 62 trading days (63 trading days ≈ one quarter of accrual).
- **Confirmation segment:** trading days 64 through 126 after the freeze date (a second, independent 63-trading-day tranche).
- **Ordering and purpose:** primary first (initial adjudication evidence); confirmation second (independent repeat evidence). Neither segment is chosen for historical performance — no performance of either segment can exist at this writing.
- **Independence:** segments are contiguous but separately declared, recorded, and reported; the confirmation segment's evidence is independent of the primary's in time.
- **Adjudication posture:** Stage-4 viability adjudication proceeds on total evidence; thin accrual at any adjudication point may lawfully produce INCONCLUSIVE / DATA-INSUFFICIENT (recorded, not entered) — a governed outcome, not a defect (V38A: no universal duration or sample threshold; sufficiency adjudicated per declared scope).

## 15. DATA SOURCE AND DATA INTEGRITY

(REGISTRATION DESIGN — FROZEN, with execution-time completions)

- **Daily bar source:** M1 bars for `USATECHIDXUSD`/`USTECm` from the Exness MT5 read-only connection, aggregated into daily session bars:
  - **Session open:** open price of the first M1 bar with timestamp ≥ the session-open boundary (09:30 ET) after timestamp translation to America/New_York.
  - **Session close:** close price of the last M1 bar with timestamp ≤ the session-close boundary (16:00 ET; 13:00 ET early close).
  - **Duplicate timestamps:** after sorting by timestamp, the earliest qualifying bar selects the open; the latest qualifying bar selects the close.
- **Timestamp semantics:** feed timestamps translated to America/New_York via the established UTC-translation rule (normalization decision); DST handled dynamically.
- **OHLC fields required:** open, close (high/low not used by the rule but retained in the frozen archive for integrity checking).
- **Corporate-action treatment:** CFD prices are raw as delivered by the broker; no adjustment is applied; index divisor/corporate events are reflected in the delivered price series. Documented as unadjusted raw CFD prices.
- **Holiday calendar:** the declared NYSE/Nasdaq calendar (execution-time artifact, hashed).
- **Data-quality checks (predeclared, Stage-2):** monotonic timestamps; price > 0; no zero-return artifacts from feed duplicates (a zero tick does not create a bar); boundary-bar existence per session; reconciliation of derived session bars against the raw M1 archive hash.
- **Protected artifacts:** the derivation uses the market feed only. No protected forward ledger (CAND-015/024/035 event/health ledgers, forward runner state) is read, modified, or referenced. Protected-forward performance remains uninspected (NOT PERMITTED).
- **Volume:** not required by the rule; M1 volume remains irrelevant to F-01 (milestone §17).
- (REGISTRATION DESIGN — TO BE FROZEN AT EXECUTION) The concrete data snapshot (M1 archive range, file hash) is produced and hashed at Stage-2 pipeline construction (§23 item 1).

## 16. EXECUTION MODEL

(REGISTRATION DESIGN — FROZEN)

- **Representation:** market-on-close at the session-close boundary (entry) and market-on-open at the next session-open boundary (exit), using the derived bar prices as the fill reference, with the frozen per-leg costs applied (§12).
- **Rationale:** the CFD trades through the interval, so both fills are ordinary executable market orders; no VWAP, official settlement, or improved-fill convention is used.
- **Consistency:** the identical execution representation is used in Stage 3 economic validation; no alternative execution convention may be substituted later (V38A: execution realism, one coherent treatment).
- **No hypothetical improvement:** fill = the frozen bar price; no partial fills, no queue position, no slippage modeling beyond the frozen cost convention.

## 17. CONDITIONAL INDEPENDENCE

(AUDIT — milestone §19)

F-01 as registered contains **no Conditional content**: no regime filter, volatility filter, momentum filter, event filter, liquidity filter, confirmation condition, macro filter, or external signal. The decision rule is the calendar partition alone (§5). Any future information layer would be a separate V38 relational component qualified by increment over this Base — never part of the Base. (AUDIT result: NO hidden Conditional logic; Gate R9 PASS.)

## 18. DETERMINISM / REPRODUCIBILITY

(AUDIT — milestone §20)

Two independent implementations must produce identical: eligible sessions; positions; entry timestamps; exit timestamps; opportunity population; outcome observations. Edge cases specified to achieve this: timestamp translation (UTC→America/New_York), boundary comparisons (≥ open / ≤ close), duplicate-timestamp rule (§15), early-close calendar, missing-close/missing-open/no-next-session statuses (§10), DST 23/25-hour days (§8), feed gaps (missing sessions recorded, not dropped), and the no-trade ledger. The rule, calendar, cost model, execution model, population algorithm, and outcome algorithm are each specified in this document (§5, §8, §10, §11, §12, §15, §16). No implementation is executed by this document (specification review only).

## 19. LEAKAGE REVIEW

(AUDIT — milestone §21)

- No future prices, future returns, future regime labels, future Conditional information, or hindsight-derived scope are used anywhere in the rule.
- Calendar knowledge (the declared NYSE/Nasdaq schedule, including holidays and early closes) is public and known at freeze time — documented as calendar structure, not look-ahead.
- The derivation uses only bars within their own session boundaries; no bar after the session-close boundary contributes to the close selection, and no bar before the session-open boundary contributes to the open selection.
- Validation-eligible evidence begins at the freeze date; all pre-freeze data is sealed (§13).
- Protected forward ledgers are never read (§15).
- (AUDIT result: no leakage; Gate R8/R9 consistent.)

## 20. V38A STAGE MAPPING

(GOVERNANCE FACT — milestone §24)

```text
STAGE 0   F-01 hypothesis formulation + BS1–BS13 selection          COMPLETE (Formulation Cycle V1; Selection Final V1)
    ↓
STAGE 1   Prospective registration freeze                           THIS MILESTONE (design); final freeze = next milestone
    ↓
STAGE 2   Structural validation (implementation, reproducibility,
          leakage audit, population construction; NO economic
          outcomes exposed before structural sign-off)              NOT EXECUTED
    ↓
STAGE 3   Economic validation (registered decision economics,
          gross/net under the frozen cost model, predeclared
          diagnostics; economics are EVIDENCE)                      NOT EXECUTED
    ↓
STAGE 4   Holistic viability adjudication (BASE-ELIGIBLE /
          INCONCLUSIVE / NOT BASE-ELIGIBLE by total evidence;
          independent review → owner decision; no sign/magnitude
          gate)                                                     NOT EXECUTED
    ↓
STAGE 5   Registry entry only if eligible                           NOT EXECUTED — Base Registry EMPTY
```

This milestone prepares Stage 1 only; it does not execute Stages 2–5.

## 21. REPORTING PLAN

(REGISTRATION DESIGN — FROZEN)

- **Primary outcome:** net per-leg mean and median log return over the primary segment, the confirmation segment, and combined (in bps), with population counts and leg frequency.
- **Primary comparison / adjudication evidence:** the ten V38A viability attributes (structural validity; determinism and reproducibility; prospective definition; economic coherence; non-pathology; execution realism; credible frozen opportunity population; interpretability as a reference decision context; independence from Conditional results; non-rescue) — adjudicated on total evidence at Stage 4, with gross and net economics and the predeclared distributional diagnostics as evidence.
- **Secondary diagnostics (predeclared only):** per §11 — standard deviation, P10/P90, per-month leg counts, cost burden. No exploratory metric may be added after measurement and reported as primary.
- **No universal threshold:** no sign, magnitude, or threshold of net expectancy, win rate, Sharpe, drawdown, sample count, or p-value determines classification (V38A: metrics are evidence; no hidden gate).
- **Reporting artifacts (future):** validation protocol, validation result, adjudication record per V38A design §"future pathway" — none created by this document.

## 22. REGISTRATION INTEGRITY GATES R1–R10

(AUDIT — milestone §27; these are registration-integrity gates, NOT economic qualification gates)

| Gate | Question | Result |
|---|---|---|
| R1 — Object identity | F-01 remains the selected decision process (session-partition, long overnight / flat intraday, one decision/day) | **PASS** (§3, §5) |
| R2 — Rule completeness | All decision semantics frozen (entry/exit/flat, no conditioning, no-trade statuses) | **PASS** (§5, §9) |
| R3 — Scope completeness | Instrument, sessions, calendar, and data frozen | **PASS** (§6, §8, §13, §15) |
| R4 — Population completeness | Opportunity universe deterministic and enumerable pre-measurement | **PASS** (§10) |
| R5 — Outcome completeness | Outcome and reporting frozen with predeclared diagnostics | **PASS** (§11, §21) |
| R6 — Cost completeness | Cost model frozen (1/1 base, 5/5 stress, per-leg convention) | **PASS** (§12) |
| R7 — Execution completeness | Execution semantics frozen (MOC/MOO, bar-price fills, no hypothetical improvement) | **PASS** (§16) |
| R8 — Prospective integrity | No outcome was used to modify the registration | **PASS** (§4, §6, §13; AUDIT Q1–Q5) |
| R9 — Conditional independence | No Conditional embedded | **PASS** (§17) |
| R10 — Reproducibility | Independent implementation reproduces the registration | **PASS** (§18; edge cases enumerated) |

### Final Independent Audit (Q1–Q10, per milestone §34)

- **Q1** Was F-01 changed to improve expected outcomes? **NO.** The selected architecture is untouched (§3, §5); only operational ambiguity was resolved, none by outcome inspection.
- **Q2** Was any parameter optimized? **NO.** F-01 has zero tunable parameters; the operational definitions (§5 of the mandate) are deterministic implementation decisions, not tuning values — each resolved by execution realism, data availability, or governance cleanliness, never by outcomes.
- **Q3** Was the validation window selected based on historical performance? **NO.** The window is forward-only accrual from the freeze date (2026-09-03), chosen for prospective integrity (§13–§14); no historical boundary or era was selected.
- **Q4** Was the instrument selected based on performance? **NO.** `USATECHIDXUSD/USTECm` was resolved by execution realism, open-price availability, existing governed feed, and class membership (§6); no performance of any candidate instrument was inspected.
- **Q5** Was any new economic result calculated? **NO.** No returns, costs-as-results, expectancies, or comparisons were computed; the cost values are frozen conventions (§12), not measurements.
- **Q6** Is the complete opportunity population deterministic? **YES** if ready — the population algorithm and all edge-case statuses are specified (§10) and enumerable pre-measurement; gate R4 PASS.
- **Q7** Can two independent implementations reproduce the same decisions? **YES** if ready — rule, calendar, timestamp translation, bar selection, population, and outcome algorithms are specified with edge cases (§18); gate R10 PASS.
- **Q8** Is the cost model frozen? **YES** if ready — 1/1 bps base and 5/5 bps stress, per-leg convention, no post-exposure alteration (§12); gate R6 PASS.
- **Q9** Is any Conditional embedded in F-01? **NO.** Zero Conditional content; the audit is explicit (§17); gate R9 PASS.
- **Q10** Does the specification preserve F-01 as a hypothesis rather than Base status? **YES.** The registered object is a hypothesis; Stage 4 adjudication and Stage 5 entry alone create Base status; the Base Registry remains EMPTY (§1, §20).

## 23. UNRESOLVED ITEMS

(REGISTRATION DESIGN — classified, none blocking)

1. **Data-snapshot hash/version** — the concrete M1 archive range and file hash are produced at Stage-2 pipeline construction (cannot exist before the pipeline runs). Class: FIXABLE SPECIFICATION COMPLETION — outcome-independent, mechanical.
2. **Concrete calendar artifact** — the machine-readable NYSE/Nasdaq trading calendar (holidays + early closes) is produced and hashed at Stage-2 construction. Class: FIXABLE SPECIFICATION COMPLETION — outcome-independent, mechanical.
3. **Broker symbol liquidity/availability check at execution** — the registered broker symbol's continued availability is verified at execution authorization (a registration-time realism check, not an economics check). Class: EXECUTION-TIME VERIFICATION.
4. **No other unresolved item exists.** No parameter, threshold, scope element, or cost value is open.

## 24. FINAL REGISTRATION VERDICT

**F-01 V38A REGISTRATION READY FOR FREEZE.**

The specification is complete, deterministic, prospective, and governance-clean: all material semantics frozen; gates R1–R10 pass; audits clean; the only open items are execution-time mechanical completions. This verdict is a specification verdict only — it is NOT "Base validated," NOT "Base eligible," NOT "economically viable," NOT "profitable," NOT "production-ready." No economics were computed, and none are implied.

## 25. REPOSITORY / GIT INTEGRITY

(GOVERNANCE FACT) Recorded at authoring:

- HEAD before and after: `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`; branch `main`.
- Change: exactly ONE new untracked artifact — `output/research_discovery/QUANTFORGE_F01_V38A_REGISTRATION_DESIGN_V1.md`.
- No commit, no staging (registration-design milestone; default no-commit).
- `SESSION_HANDOFF.md` intentionally NOT modified.
- No source/test/configuration change; no Base Registry record; no validation; no experiment; no new economic measurement; no protected-forward inspection; no forward-runner modification.
- `git diff --check` verified clean.
- Pre-existing dirty/untracked files (forward runtime data, G6 dirs, health/event ledgers, screening scripts, V37A phase-A, selection/cycle artifacts, superseded proposal) remain untouched and are not part of this milestone.

## 26. HARD STOP

Registration design complete. **F-01 V38A REGISTRATION READY FOR FREEZE** — hypothesis only; Base Registry EMPTY.

STOP. No V38A Stage 2 execution; no economic validation; no fresh-outcome inspection; no backtest; no Registry entry; no viability adjudication; no Conditional component; no modification of F-01 based on any outcome (none exists); H01/ORD/TRADEABLE_EDGE remain CLOSED; CAND-077/081/083/099 unchanged; protected-forward excluded.

Next milestone, if and only if the owner authorizes: **F-01 V38A REGISTRATION FREEZE / EXECUTION AUTHORIZATION** — final freeze of this specification (including the §23 execution-time completions) and authorization of Stage-2 structural validation. Nothing in this document authorizes that milestone or any research beyond it.