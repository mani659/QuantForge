# QUANTFORGE — F-01 V38A REGISTRATION FREEZE V1

**Milestone:** F-01 V38A Registration Freeze / Execution Authorization (final governance gate before Stage 2)
**Status:** **F-01 V38A REGISTRATION FROZEN — STAGE 2 STRUCTURAL VALIDATION AUTHORIZED** (authorization granted; Stage 2 is NOT executed here)
**Parent governance:** V38 (RATIFIED); V38A (RATIFIED, BV1–BV13); BS1–BS13 (RATIFIED); BF1–BF13 (RATIFIED); Formulation Cycle V1 (SHA `655473e2a863`); Selection Final V1 (SHA `3097b776cb00`); Registration Design V1 (SHA `6af00afd3189`)
**Frozen object state:** **F-01 — V38A REGISTERED FOR STAGE 2 EXECUTION** — NOT a Validated Base, NOT a Base, NOT Base-eligible, NOT Qualified Alpha.
**SESSION_HANDOFF intentionally NOT modified** (registration-freeze milestone).

Label conventions: GOVERNANCE FACT / FROZEN / MECHANICAL COMPLETION / AUDIT / NOT PERMITTED.

---

## 1. FREEZE DECLARATION

**IMMUTABLE REGISTRATION FREEZE EFFECTIVE 2026-09-03.**

The F-01 registration is now the boundary between design and execution. Both mechanical completions are resolved (§4–§5), all registration-integrity gates R1–R13 pass (§17), and the final audit Q1–Q13 passes (§22).

**Post-freeze immutability rule:** NO RULE, SCOPE, DATA, CALENDAR, EXECUTION, COST, OR OUTCOME DEFINITION MAY CHANGE UNTIL STAGE 2 IS COMPLETE. Any proposed post-freeze change is one of: (a) a registration violation; (b) a new governed registration; or (c) a formally documented implementation bug whose correction is outcome-independent and separately governed. Silent patching of the frozen study is prohibited. Any change to the registered hypothesis after this freeze requires a new governed registration.

## 2. SELECTED HYPOTHESIS IDENTITY

(GOVERNANCE FACT / FROZEN) **F-01 — Session-Partition Reference Process (Overnight Exposure Leg):** on every eligible trading day, hold one liquid US equity index from the defined session close to the next defined session open (long); flat from the open to the close; exactly one decision opportunity per eligible trading day. Immutable: overnight architecture; long/flat structure; session-partition concept; one-opportunity-per-day structure.

## 3. EXACT DECISION RULE

(FROZEN) For each eligible trading day t: enter long at the defined session close of day t (16:00 ET; 13:00 ET early close); hold through the overnight interval; exit at the defined session open of day t+1 (09:30 ET); flat open→close; one position per eligible session; no pyramiding; no intraday management; no stop/target; no discretionary intervention. Missing close(t) or missing open(t+1) ⇒ recorded no-trade decision (§9). No other conditioning exists.

## 4. MECHANICAL COMPLETION #1 — DATA SNAPSHOT (RESOLVED)

(MECHANICAL COMPLETION / FROZEN) The registered data snapshot facts:

| Field | Value |
|---|---|
| Source | Exness MT5 read-only connection, symbol `USTECm`, logical `USATECHIDXUSD` |
| Data identifier | `data/m1/USATECHIDXUSD_M1.csv` |
| Schema | `timestamp,open,high,low,close,volume` (volume = 0 throughout; not used by the rule) |
| Baseline start timestamp | 2023-09-01 00:00:00 |
| Baseline end timestamp | 2026-07-10 20:14:00 |
| Baseline bar count | 906,815 (906,816 lines incl. header) |
| Retrieval / version date | 2026-09-03 (hash computed 2026-09-03) |
| Baseline SHA-256 | `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6` |

**Study-snapshot protocol (FROZEN):** validation-eligible observations are bars whose session-open timestamp is ≥ the freeze date (2026-09-03), accrued forward into the same append-only archive by the registered accrual pipeline. The archive identity is maintained by (1) append-only convention (no rewriting, no deletion, no reordering of existing rows) and (2) SHA-256 checkpoints recorded at Stage-2 start and at each segment boundary. At freeze time the study-eligible portion is **empty** (the baseline archive's last bar is 2026-07-10; no post-freeze bars exist yet). The baseline archive through 2026-07-10 is the **sealed pre-freeze baseline** — motivation/provenance only, never validation evidence. The 2026-07-11 → 2026-09-02 window exists only in protected forward artifacts and is **excluded entirely** (not read, not referenced).

(AUDIT) No economics were inspected while defining the snapshot; no observation was excluded for cleanliness; no subset was selected; the data is not modified after hashing; a regenerated file would change identity and require a new registration.

## 5. MECHANICAL COMPLETION #2 — EXCHANGE CALENDAR ARTIFACT (RESOLVED)

(MECHANICAL COMPLETION / FROZEN) The calendar artifact is created and frozen:

| Field | Value |
|---|---|
| Artifact | `output/research_discovery/QUANTFORGE_F01_V38A_CALENDAR_V1.json` |
| Content | timezone America/New_York; regular open 09:30 ET; regular close 16:00 ET; early close 13:00 ET; DST rule; weekends; 20 full closures (2026–2027); 4 early closes; extraordinary-closure policy; notes |
| Source | Official NYSE/Nasdaq published trading calendar (public record) |
| Version / frozen | V1 / 2026-09-03 |
| SHA-256 | `39e5b3cfa25c8ae13d0debddff2b5f480b836aa29785b42b94f4484048a81696` |

(AUDIT) The calendar is infrastructure, not a tuning variable: no calendar version was selected to favor any observation set. One reconciliation flag is recorded (2027-12-23 early close, outside the study horizon): the Stage-2 calendar-integrity check reconciles the artifact against the official published schedule; any outcome-independent discrepancy is corrected, re-hashed, and recorded as a mechanical completion before Stage-2 execution.

## 6. INSTRUMENT / FEED IDENTITY — VERIFIED

(GOVERNANCE FACT / FROZEN) Verified independently at freeze:

- Logical identity = `USATECHIDXUSD`; executable feed identity = `USTECm`; mapping `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`.
- The Stage-2 feed is the same feed described by the registration (Exness MT5 read-only connection, Exness-MT5Trial15 server).
- No hidden mapping to another instrument; no replacement with a historical index proxy; the measured price is the registered execution/reference price (the CFD's own M1-derived session bars).
- No historical profitability comparison across alternate instruments was made; no instrument was selected for expected results. The feasibility rationale (execution realism, open-price availability, existing governed feed, class membership) remains the basis of identity (Registration Design V1 §6).

## 7. SESSION SEMANTICS — FINAL FREEZE

(FROZEN) Timezone `America/New_York`; regular session open 09:30 ET; regular session close 16:00 ET; declared early close 13:00 ET; DST handled through the registered UTC translation; holidays/weekends per the frozen calendar artifact (§5); missing sessions recorded, never silently dropped; special sessions: none beyond the calendar. Data timestamps map into these semantics via the registered bar-derivation rule: session open = open of the first M1 bar with timestamp ≥ the open boundary; session close = close of the last M1 bar with timestamp ≤ the close boundary (duplicates: earliest qualifying for open, latest qualifying for close), after timestamp translation to America/New_York.

## 8. POSITION RULE — FINAL FREEZE

(FROZEN) One long overnight position from the defined session close to the next eligible session open, flat intraday; one opportunity per eligible session; no pyramiding; no intraday management; no stop; no target; no discretionary adjustment; no short side; no filter; no regime condition; no Conditional. No parameter optimization. (AUDIT: zero tunable parameters; operational definitions are the registered constants above.)

## 9. OPPORTUNITY POPULATION — FINAL FREEZE

(FROZEN) Population = every eligible overnight leg L_t for which session-close data at t and next-session-open data at t+1 are both valid under the registered data/calendar rules. Deterministic statuses:

| Case | Status |
|---|---|
| Missing close(t) | NO-TRADE — MISSING CLOSE |
| Missing next open(t+1) | NO-TRADE — MISSING NEXT OPEN |
| t+1 holiday/weekend (no session) | NO-TRADE — NO NEXT SESSION |
| Duplicate timestamps at a boundary | resolved by the registered bar-selection rule (§7); no population ambiguity |
| Invalid timestamps | recorded NO-TRADE — INVALID TIMESTAMP (Stage-2 data-integrity check catches) |
| Early close | close boundary = 13:00 ET per calendar; normal leg |
| Unexpected closure | no session; recorded with documented reason (calendar policy) |
| Incomplete session | recorded no-trade with the applicable status |
| Data corruption | recorded NO-TRADE — DATA CORRUPTION; flagged by Stage-2 integrity checks |

Every excluded observation has a deterministic reason; the population ledger records every session in the window with its decision and status. The population is constructible without knowing outcomes and becomes immutable at registry entry.

## 10. OUTCOME — FINAL FREEZE

(FROZEN) Entry price = registered session-close bar price of day t; exit price = registered session-open bar price of day t+1. Per-leg raw return r_t = ln(open_{t+1}/close_t); log-return representation in basis points (1 bp = 0.0001). Net = r_t − (c_entry + c_exit) with frozen costs (§11). Gross/net terminology per Registration Design V1 §11. Aggregation: mean and median per segment and combined; population counts and leg frequency; predeclared secondary diagnostics only (standard deviation, P10/P90, per-month leg counts, cost burden). No diagnostics beyond those declared may be generated later.

## 11. COST MODEL — FINAL FREEZE

(FROZEN) Base case: 1 bps entry + 1 bps exit (2 bps per overnight leg). Stress case: 5 bps entry + 5 bps exit (10 bps per leg). Costs are per leg; no hidden spread adjustment; no hidden slippage adjustment; no commission added; no post-result cost adjustment. The stress case is evidence only — it is NOT a Base-eligibility threshold (V38A: economics are evidence; no sign/magnitude gate).

## 12. VALIDATION SCOPE — FINAL FREEZE

(FROZEN) Validation-eligible evidence begins at the formal freeze timestamp (2026-09-03, session-open boundary). All evidence before the freeze — the sealed baseline archive (through 2026-07-10), the protected forward window (2026-07-11 → 2026-09-02, excluded entirely), FRED daily closes, H01-era windows, and the external prior — is motivation/provenance only where required by the registered prospective boundary. Segments: **primary = first 63 eligible trading days** (sessions with open ≥ freeze date, days 1–63); **confirmation = days 64–126**. Neither segment may be shortened, extended, or moved after Stage-2 results exist. If post-freeze evidence is insufficient at any adjudication point, the lawful downstream result is DATA-INSUFFICIENT / INCONCLUSIVE — recorded, not a reason to alter the registration.

## 13. CONFIRMATION-SEGMENT INDEPENDENCE — VERIFIED

(GOVERNANCE FACT / FROZEN) Primary and confirmation segments are distinct (days 1–63 vs 64–126); segment ordering is fixed; neither segment can be redefined after observation; there is no historical segment substitution; both are declared in this freeze before any study-eligible observation exists. No economic outcome was inspected before this freeze.

## 14. IMPLEMENTATION REFERENCE

(FROZEN) No implementation exists at freeze time; Stage 2 will implement the frozen specification. Implementation-freeze rule: the Stage-2 implementation (module/file identity, version, environment) is recorded and frozen at Stage-2 start, before any structural output is generated; if implementation changes are required solely to make the frozen semantics executable, they are documented as outcome-independent mechanical completions and the resulting implementation is frozen before Stage-2 proceeds. No implementation change may improve expected outcomes.

## 15. STRUCTURAL VALIDATION PLAN (STAGE 2) — FROZEN

(FROZEN) Stage 2 verifies, with no economic outcomes exposed:

1. **Determinism** — repeated execution generates the same opportunity population.
2. **Reproducibility** — an independent implementation reproduces the same session set and positions.
3. **Calendar integrity** — session classification follows the registered calendar artifact (§5); reconciliation against the official published schedule.
4. **Data integrity** — timestamps valid, ordered, free of prohibited duplicates/corruption; bar-derivation rule verified; baseline archive hash reconciliation (`39f25619…`); accrual append-only invariant.
5. **Population integrity** — all eligible overnight legs included; all exclusions have deterministic causes (§9).
6. **Leakage** — no future market data used to construct the current opportunity; boundary comparisons verified.
7. **Execution semantics** — entry/exit mapping matches the registered model (§7, §10).
8. **Cost semantics** — the frozen cost model is structurally represented correctly (§11); no economic execution occurs.

## 16. STAGE 2 ECONOMIC FIREWALL — FROZEN

(FROZEN) Stage 2 MUST NOT expose P&L, expectancy, win rate, Sharpe, drawdown, return distributions, or performance ranking. Stage 2 MAY determine session counts, opportunity counts, missing-data counts, structural integrity, timestamps, and decision-state records. Prices may be inspected only insofar as structural integrity requires (e.g., positivity, ordering); no price inspection may reveal outcome performance (no return computation, no cross-bar comparison).

## 17. REGISTRATION IMMUTABILITY CHECK — R1–R13

(AUDIT — all must PASS)

| Gate | Check | Result |
|---|---|---|
| R1 | Selected hypothesis identity unchanged | **PASS** (§2) |
| R2 | Decision rule unchanged | **PASS** (§3) |
| R3 | Instrument unchanged | **PASS** (§6) |
| R4 | Session semantics fixed | **PASS** (§7) |
| R5 | Opportunity population fixed | **PASS** (§9) |
| R6 | Outcome fixed | **PASS** (§10) |
| R7 | Costs fixed | **PASS** (§11) |
| R8 | Primary/confirmation scope fixed | **PASS** (§12–§13) |
| R9 | Data snapshot fixed | **PASS** (§4; baseline SHA-256 recorded) |
| R10 | Calendar fixed | **PASS** (§5; artifact SHA-256 recorded) |
| R11 | Execution model fixed | **PASS** (§7, §15) |
| R12 | No Conditional embedded | **PASS** (§8; Conditional-independence declaration below) |
| R13 | No outcome information used to make any freeze decision | **PASS** (audit Q1–Q5, Q12) |

All 13 PASS ⇒ **F-01 REGISTRATION READY FOR EXECUTION** (Stage 2 only).

## 18. CONDITIONAL-INDEPENDENCE DECLARATION

(FROZEN) F-01 as registered contains zero Conditional content: no regime, volatility, momentum, event, liquidity, confirmation, macro, or external-signal logic anywhere in the rule (§3, §8). Any future information layer is a separate V38 relational component qualified by increment over this Base — never part of the Base, and no such component is registered or anticipated by this freeze.

## 19. PROSPECTIVE-INTEGRITY DECLARATION

(FROZEN) This registration predates all validation-eligible observation. The freeze timestamp (2026-09-03) is the prospective boundary: study-eligible evidence begins there; all pre-freeze information is excluded from validation (§12). No outcome of any kind was used to make any freeze decision (R13; audit Q1–Q5). Motivation ≠ Validation holds: the motivating knowledge base is motivation only.

## 20. EXECUTION AUTHORIZATION BOUNDARY

**STAGE 2 STRUCTURAL VALIDATION IS NOW AUTHORIZED.**

Authorization covers ONLY V38A Stage 2 structural validation (the eight frozen checks of §15) under the economic firewall of §16. **Stage 2 is NOT executed by this milestone.** The boundary is explicit:

```text
FREEZE / AUTHORIZATION MILESTONE  (this document)
        ↓
STOP
        ↓
NEXT MILESTONE
F-01 V38A STAGE 2 STRUCTURAL VALIDATION
```

This authorization does NOT authorize Stage 3, Stage 4, Registry entry, Conditional research, assembled testing, or any economic measurement. It does NOT confer Base status, Base-eligibility, or Qualified Alpha status.

## 21. FINAL REGISTRATION ARTIFACT CONTENTS — VERIFIED

(AUDIT) This document contains all 22 required elements: freeze declaration (§1); selected hypothesis identity (§2); exact decision rule (§3); instrument/feed identity (§6); execution/reference-series relationship (Registration Design V1 §7, incorporated and unchanged); session/calendar specification (§5, §7); data snapshot identity/hash (§4); position semantics (§8); opportunity population (§9); outcome definition (§10); cost model (§11); validation scope (§12); primary/confirmation segments (§12–§13); implementation reference (§14); Stage-2 structural validation plan (§15); registration-integrity gates R1–R13 (§17); prospective-integrity declaration (§19); Conditional-independence declaration (§18); post-freeze immutability rule (§1); execution authorization boundary (§20); final verdict (§25); repository integrity (§24).

## 22. FINAL AUDIT (Q1–Q13)

(AUDIT)

- **Q1** Was F-01 changed to improve expected outcomes? **NO.** Architecture and rule untouched from selection (§2–§3); only the two outcome-independent mechanical completions were resolved (§4–§5).
- **Q2** Was any parameter optimized? **NO.** Zero tunable parameters; all operational definitions are the registered constants, each resolved by execution realism, data availability, or governance cleanliness.
- **Q3** Was the validation scope selected because of performance? **NO.** Forward-only scope from the freeze timestamp for prospective integrity (§12); no historical boundary chosen.
- **Q4** Was the instrument selected because of performance? **NO.** Identity resolved by feasibility/governance (§6); no performance comparison made.
- **Q5** Was any new economic result computed? **NO.** No returns, costs-as-results, expectancies, or comparisons were computed; only structural metadata (schema, timestamps, counts, hashes) was read.
- **Q6** Is the data snapshot immutable and hashed? **YES if ready.** Baseline archive hashed (`39f25619…`, §4); study-snapshot append-only protocol with SHA-256 checkpoints at Stage-2 start and segment boundaries frozen.
- **Q7** Is the calendar artifact immutable and identified? **YES if ready.** `QUANTFORGE_F01_V38A_CALENDAR_V1.json` hashed (`39e5b3cf…`, §5); Stage-2 reconciliation rule recorded.
- **Q8** Is the opportunity population deterministic? **YES if ready.** Algorithm and all edge-case statuses frozen (§9).
- **Q9** Can independent implementations reproduce the decisions? **YES if ready.** Rule, calendar, timestamp translation, bar selection, population, and outcome algorithms specified (Registration Design V1 §18; this freeze §7, §9, §10); determinism/reproducibility are Stage-2 checks (§15).
- **Q10** Is the cost model frozen? **YES if ready.** 1/1 bps base, 5/5 bps stress, per-leg (§11).
- **Q11** Is any Conditional embedded? **NO.** Zero Conditional content (§8, §18).
- **Q12** Is all pre-freeze information excluded from validation where required by the registered prospective boundary? **YES.** Freeze timestamp boundary; sealed baseline and protected window excluded (§4, §12, §19).
- **Q13** Does registration authorize only Stage 2? **YES.** Authorization boundary explicit (§20); Stages 3–5 not authorized.

## 23. REPOSITORY / GIT INTEGRITY

(GOVERNANCE FACT) Recorded at freeze:

- HEAD before and after: `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`; branch `main`.
- Changes: exactly TWO new untracked artifacts — `output/research_discovery/QUANTFORGE_F01_V38A_REGISTRATION_FREEZE_V1.md` (this record) and `output/research_discovery/QUANTFORGE_F01_V38A_CALENDAR_V1.json` (the calendar artifact it hashes).
- No commit, no staging (registration-freeze milestone; default no-commit).
- `SESSION_HANDOFF.md` intentionally NOT modified.
- No source/test/configuration change; no Base Registry record; no validation; no experiment; no new economic measurement; no protected-forward inspection; no forward-runner modification; no data-file modification (the sealed baseline `data/m1/USATECHIDXUSD_M1.csv` is untouched, hash recorded pre-freeze).
- `git diff --check` verified clean.
- Pre-existing dirty/untracked files (forward runtime data, G6 dirs, health/event ledgers, screening scripts, V37A phase-A, selection/cycle/design artifacts, superseded proposal) remain untouched and are not part of this milestone.

## 24. FINAL VERDICT

**F-01 V38A REGISTRATION FROZEN — STAGE 2 STRUCTURAL VALIDATION AUTHORIZED.**

The frozen object is **F-01 — V38A REGISTERED FOR STAGE 2 EXECUTION**. It is NOT a Validated Base, NOT a Base, NOT Base-eligible, NOT Qualified Alpha, NOT production-ready. Registration authorizes only Stage 2 structural execution under the frozen semantics and the §16 economic firewall.

## 25. HARD STOP

Freeze complete. **STOP.**

Do NOT: execute Stage 2 (authorized but not executed here); inspect fresh economic outcomes; calculate P&L or expectancy; perform Stage 3; adjudicate Stage 4; create a Base Registry entry; add Conditional components; perform assembled testing; modify F-01 based on any outcome (none exists). H01/ORD/TRADEABLE_EDGE remain CLOSED; CAND-077/081/083/099 unchanged; protected-forward excluded; **Base Registry EMPTY**.

Next permissible milestone: **F-01 V38A STAGE 2 STRUCTURAL VALIDATION** — consumes the frozen registration, the hashed calendar artifact, and the sealed baseline data exactly as frozen here. Any change to the registered hypothesis after this freeze requires a new governed registration.