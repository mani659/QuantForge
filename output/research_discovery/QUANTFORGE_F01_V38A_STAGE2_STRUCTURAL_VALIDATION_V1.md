# QUANTFORGE — F-01 V38A STAGE 2 STRUCTURAL VALIDATION V1

**Milestone:** F-01 V38A Stage 2 Structural Validation (first execution milestone)
**Status:** **STRUCTURALLY VALID — DATA ACCRUAL PENDING** — economic outcomes remain sealed; no Base status created
**Parent governance:** V38 (RATIFIED); V38A (RATIFIED, BV1–BV13); BS1–BS13 (RATIFIED); BF1–BF13 (RATIFIED); Formulation Cycle V1 (SHA `655473e2a863`); Selection Final V1 (SHA `3097b776cb00`); Registration Design V1 (SHA `6af00afd3189`); Registration Freeze V1 (SHA `41883aaeab6a`)
**Frozen object state:** **F-01 — V38A REGISTERED FOR STAGE 2 EXECUTION** (unchanged by this milestone)
**SESSION_HANDOFF intentionally NOT modified** (execution milestone; handoff updates remain attached to governance-ratification milestones per recent repository pattern).

Label conventions: GOVERNANCE FACT / STRUCTURAL RESULT / AUDIT / NOT PERMITTED.

---

## 1. EXECUTIVE STAGE 2 VERDICT

**STRUCTURALLY VALID — DATA ACCRUAL PENDING.**

Stage 2 proves the registered F-01 decision process can be executed exactly, deterministically, and without leakage — it says nothing about whether F-01 makes money (no economic value exists in this report). All thirteen structural gates S2-1–S2-13 pass. The complete integrity and pipeline tests passed on the sealed baseline archive: 906,815 bars with zero structural defects, session construction and opportunity-population logic deterministic (two identical runs) and reproducible (two independent implementations identical), calendar logic verified (17/17 checks), and the frozen hashes (registration, calendar, data) all match.

The registered study is **forward-only** from the freeze date 2026-09-03; no post-freeze observations have accrued yet. The validation-eligible opportunity population is therefore **currently empty by design** — recorded as DATA ACCRUAL PENDING, explicitly NOT a structural failure. Stage 3 must NOT begin until the frozen registration contains sufficient admissible observations under the registered scope.

## 2. GOVERNANCE STATE

(GOVERNANCE FACT) Verified before and during execution:

- V38 = RATIFIED; V38A = RATIFIED; BS1–BS13 = RATIFIED; BF1–BF13 = RATIFIED.
- F-01 = SELECTED BASE HYPOTHESIS; registration = FROZEN (`…_REGISTRATION_FREEZE_V1.md`, SHA `41883aaeab6a`); Stage 2 = AUTHORIZED by the freeze record.
- Base Registry = **EMPTY**; no Base exists; no Stage 3 execution; no Stage 4 adjudication.
- HEAD `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`; branch `main`.
- Registration artifact SHA `41883aaeab6a`; calendar artifact SHA `39e5b3cfa25c8ae13d0debddff2b5f480b836aa29785b42b94f4484048a81696`; data artifact `data/m1/USATECHIDXUSD_M1.csv` SHA `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`.
- Working tree: pre-existing dirty/untracked files unchanged by this milestone (see §22).

## 3. FROZEN REGISTRATION IDENTITY

(GOVERNANCE FACT) Consumed exactly as frozen:

- **Instrument:** logical `USATECHIDXUSD`; executable feed `USTECm` (Exness MT5, Exness-MT5Trial15); mapping `USATECHIDXUSD->EXNESS:USTECM:1.0`.
- **Session:** America/New_York; open 09:30 ET; close 16:00 ET; early close 13:00 ET; DST via the registered UTC translation.
- **Position:** one long overnight leg (session close → next eligible session open), flat intraday; no short, pyramiding, stop, target, intraday management, signal filter, regime filter, or Conditional.
- **Population:** eligible leg requires valid session close at t and valid next-session open at t+1 under the registered calendar; every exclusion gets a deterministic NO-TRADE reason.
- **Boundary:** validation-eligible evidence begins at the freeze date 2026-09-03; pre-freeze data excluded from validation.

## 4. DATA SNAPSHOT USED

(STRUCTURAL RESULT)

| Field | Value |
|---|---|
| Artifact | `data/m1/USATECHIDXUSD_M1.csv` (sealed baseline) |
| SHA-256 (recomputed 2026-09-03) | `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6` — **matches frozen** |
| Rows | 906,815 bars |
| Schema | `timestamp,open,high,low,close,volume` |
| Range | 2023-09-01 00:00:00 → 2026-07-10 20:14:00 |
| Role in Stage 2 | structural pipeline test ONLY (schema/timestamps/session derivation/determinism); **zero observations enter the validation population** |
| Study-eligible snapshot | **empty at execution time** — no post-freeze (≥ 2026-09-03) bars exist in any admissible source; the 2026-07-11 → 2026-09-02 window exists only in protected forward artifacts and was NOT read, hashed, materialized, or referenced |

(AUDIT) No economics were computed from the snapshot; prices were inspected only for structural validity (positivity, OHLC ordering) and bar-existence checks; no price values are reported in this document.

## 5. CALENDAR INTEGRITY

(STRUCTURAL RESULT) Consumed exactly: `output/research_discovery/QUANTFORGE_F01_V38A_CALENDAR_V1.json` (SHA `39e5b3cfa25c…`, matches frozen).

- JSON validity: PASS; 18 top-level keys; 20 full closures; 4 early closes; no duplicate closure dates (verified); no contradictory session definitions.
- Timezone: America/New_York with the registered UTC-translation rule (standard US DST rule implemented deterministically, no tz-database dependency — documented in the implementation).
- 17/17 calendar-logic checks passed, including: Labor Day 2026-09-07, Thanksgiving 2026-11-26, Christmas 2026-12-25, New Year's Day 2027-01-01 excluded; weekends excluded; next-eligible-session mapping skips the Labor Day holiday weekend (Fri 09-04 → Tue 09-08); early-close boundaries 13:00 ET for 2026-11-27 and 2026-12-24; regular close 16:00 ET; DST offsets correct at both 2026 transitions (Mar 7/8: −5/−4; Oct 31/Nov 1: −4/−5) and 2027 spring transition (Mar 14: −4); early-close days are trading sessions.
- **Reconciliation flag 2027-12-23:** the registered study horizon (primary days 1–63 ends 2026-12-02; confirmation days 64–126 ends 2027-03-05) places 2027-12-23 **OUTSIDE the study horizon** — verified `False` for membership in horizon days 1–126. Per the freeze record, it remains a documented calendar-integrity observation only; **the frozen calendar artifact was NOT edited.**

## 6. SESSION CONSTRUCTION

(STRUCTURAL RESULT) Sessions are constructed from the frozen calendar + data per the registered rule (first bar ≥ 09:30 ET for open; last bar ≤ 16:00/13:00 ET for close, after UTC→ET translation; duplicates: earliest qualifying for open, latest for close — no duplicate timestamps exist in the archive, verified).

- Study horizon (≥ 2026-09-03, through 2027-12-31 as calendar infrastructure): 334 eligible sessions.
- Pipeline test range (2026-01-02 → 2026-07-10, the intersection of the frozen 2026 calendar with the sealed archive): 130 eligible sessions — all 130 had a valid session-open bar and a valid session-close bar (structural existence checks only; no returns computed).
- No synthetic sessions, no weekend/holiday sessions, no partial-session creation.

## 7. OPPORTUNITY POPULATION

(STRUCTURAL RESULT)

- **Study-horizon population (validation-eligible): 0 eligible legs.** Reason: the registered forward-only boundary admits only bars with session-open ≥ 2026-09-03; none exist at execution time. Recorded as **structurally valid but currently empty** — explicitly NOT a structural failure.
- **Pipeline-test population (sealed baseline, structural test only):** 130/130 sessions with both boundary bars present → 130 potential legs exercised for construction logic; every session produced exactly one potential overnight leg; no duplicates, no overlaps, no intraday entries, no overnight stacking, no pyramiding (structural checks).

## 8. EXCLUSION REASONS

(STRUCTURAL RESULT) The registered deterministic NO-TRADE statuses were implemented and exercised:

| Status | Behavior verified |
|---|---|
| NO-TRADE — MISSING CLOSE | session has no valid bar ≤ close boundary → leg not formed (0 occurrences in pipeline test; applicable to empty study horizon) |
| NO-TRADE — MISSING NEXT OPEN | session t+1 has no valid bar ≥ open boundary → leg not formed (0 occurrences in pipeline test) |
| NO-TRADE — NO NEXT SESSION | t+1 is holiday/weekend per calendar → leg not formed (calendar logic verified: e.g., Fri 09-04 → Tue 09-08) |
| NO-TRADE — INVALID TIMESTAMP / DATA CORRUPTION | 0 malformed rows, 0 invalid timestamps, 0 out-of-order rows in the archive (§4) |
| Early close | close boundary = 13:00 ET; one leg preserved (calendar logic verified) |

Every exclusion has a deterministic reason; the population ledger records every session with its decision and status; nothing is silently dropped.

## 9. EXECUTION-SEMANTICS VERIFICATION

(STRUCTURAL RESULT) The implementation conforms to the frozen execution model: entry reference = last M1 bar close at/before the session-close boundary (MOC); exit reference = first M1 bar open at/after the next session-open boundary (MOO); boundary selection verified for all 130 pipeline-test sessions (both references exist); no favorable fill interpolation, no intrabar improvement, no spread-based synthetic fill, no hidden VWAP, no slippage optimization — the bar-selection code contains no such paths. No execution profitability was computed.

## 10. LEAKAGE AUDIT

(AUDIT — PASS) Eligibility and construction use only: (1) the frozen calendar (public, known at freeze time — documented calendar structure, not look-ahead); (2) bar timestamps within the session's own boundaries (open selection uses bars ≥ the open boundary; close selection uses bars ≤ the close boundary); (3) the calendar-based next-session mapping (dates only — the next session's market prices are never consulted for current eligibility). No future return, future regime, future volatility, future Conditional, or future economic result is used anywhere. The implementation contains no reference to any price after the close boundary of the session being constructed.

## 11. DETERMINISM TEST

(STRUCTURAL RESULT) Implementation A run twice against the identical snapshot: session classification, eligible-session set, opportunity population, exclusion reasons, and entry/exit boundary existence **identical** (130/130 sessions, `True`). No economic output.

## 12. REPRODUCIBILITY TEST

(STRUCTURAL RESULT) Independent implementation B (bisect-based search on sorted timestamps — a different code path from A's linear scan) reproduced implementation A exactly: 130/130 sessions, identical open/close validity statuses (`True`). Both implementations share only the frozen inputs and the registered rule. The independent implementation is part of the same governed module (`f01_v38a_stage2_structural.py`, functions `build_population_a` / `build_population_b`) — documented, not manufactured.

## 13. POPULATION RECONCILIATION

(STRUCTURAL RESULT) Structural funnel (pipeline test on sealed baseline, 2026-01-02 → 2026-07-10):

```text
source observations (906,815 bars)
        ↓  0 malformed, 0 invalid timestamps, 0 out-of-order
valid timestamps (906,815)
        ↓  frozen 2026 calendar
calendar-eligible sessions in test range (130)
        ↓  all have valid open + close boundary bars
sessions with required prices (130 / 130)
        ↓  calendar-based next-session mapping (all within range)
eligible overnight legs (130 potential; structural test only)
```

Study-horizon funnel: source observations ≥ freeze boundary = **0** → calendar-eligible sessions in horizon (334 through 2027-12-31; 126 within the registered segments) → sessions with required prices = **0** → eligible legs = **0**. The two funnels reconcile exactly; the counts agree across implementations A and B. **STRUCTURALLY VALID BUT CURRENTLY EMPTY** — no backfill, no protected-window substitution, no scope alteration.

## 14. DST / HOLIDAY / EARLY-CLOSE VERIFICATION

(STRUCTURAL RESULT) All verified structurally (no economics):

- **DST:** the registered America/New_York semantics are implemented via the standard US DST rule; boundary translation verified at both 2026 transitions (spring 2026-03-08: −4h; pre-transition 03-07: −5h; fall 2026-11-01: −5h; pre-transition 10-31: −4h) and the 2027 spring transition (03-14: −4h). No hard-coded single UTC offset; a 23/25-hour overnight interval is measured as actually observed (structural fact).
- **Holidays:** all frozen closures excluded (sample-verified: 2026-09-07, 2026-11-26, 2026-12-25, 2027-01-01; full sets loaded and validated — no duplicate dates).
- **Early closes:** 13:00 ET boundary applied for the registered early-close dates; one overnight leg preserved; no assessment of early-close leg performance (prohibited).
- **Weekends:** no synthetic sessions; no weekend/holiday-gap economic calculation (none computed).

## 15. MISSING-DATA HANDLING

(STRUCTURAL RESULT) The registered policy is implemented: no price synthesis, no interpolation, no forward-fill, no proxy data; missing boundary bars produce the deterministic NO-TRADE status (§8). In the pipeline test all 130 sessions had both boundary bars (0 missing), demonstrating the full path; in the study horizon, missing-data handling applies to the empty accrual state (every future session is classified against the same deterministic rules). Structural counts recorded; no prices reported.

## 16. S2-1–S2-13 GATE RESULTS

(AUDIT — every gate with evidence)

| Gate | Check | Result |
|---|---|---|
| S2-1 | Registration identity matches execution (instrument, session, rule, boundary per freeze) | **PASS** (§3) |
| S2-2 | Data source identity matches registration (`data/m1/USATECHIDXUSD_M1.csv`, SHA matches frozen) | **PASS** (§4) |
| S2-3 | Calendar identity matches registration (SHA `39e5b3cfa25c…`, JSON valid, no duplicates) | **PASS** (§5) |
| S2-4 | Timestamp semantics valid (parse, ordering, duplicates, timezone translation) | **PASS** (§4, §5, §14) |
| S2-5 | Session construction deterministic (two identical runs) | **PASS** (§6, §11) |
| S2-6 | Opportunity population deterministic (identical across runs) | **PASS** (§7, §11) |
| S2-7 | Exclusion reasons deterministic (statuses specified and exercised) | **PASS** (§8) |
| S2-8 | Execution semantics conform (MOC/MOO boundary selection, no fill improvement) | **PASS** (§9) |
| S2-9 | No look-ahead / leakage | **PASS** (§10) |
| S2-10 | Independent/repeated reproduction conforms (A vs B identical) | **PASS** (§12) |
| S2-11 | No Conditional embedded (rule is the calendar partition alone) | **PASS** (§3, §17 below) |
| S2-12 | No protected forward evidence accessed (runtime/, G6 dirs, forward ledgers not read) | **PASS** (§4, §22) |
| S2-13 | Economic outcomes remain sealed (no return/P&L computed or exposed) | **PASS** (§17) |

## 17. ECONOMIC FIREWALL VERIFICATION

(AUDIT — PASS) The Stage-2 implementation contains no return, P&L, expectancy, win rate, Sharpe, drawdown, performance-ranking, or economic-comparison computation of any kind (verified by inspection of the governed module `research/f01_v38a_stage2_structural.py`; the module's only price handling is positivity/OHLC-ordering checks and boundary-bar existence). This report contains structural counts only. No economic calculation was silently performed and withheld — none exists.

## 18. DATA-ACCRUAL STATUS

(STRUCTURAL RESULT) **NO CURRENT VALIDATION-ELIGIBLE OBSERVATIONS.** The frozen registration admits only bars with session-open ≥ 2026-09-03; none have accrued at execution time. The sealed baseline archive ends 2026-07-10 (SHA verified unchanged since freeze). The 2026-07-11 → 2026-09-02 window is excluded entirely (protected forward artifacts, never read). Accrual requirements: the registered append-only pipeline (new bars appended to the archive with append-only enforcement and SHA-256 checkpoints at Stage-2 start — recorded — and at each segment boundary) is the only admissible source of future observations. **No backfill; no protected-window substitution; no scope modification.** Stage 3 must not begin merely to satisfy a schedule.

## 19. STRUCTURAL EXCEPTIONS / BLOCKERS

(STRUCTURAL RESULT) **None.** No registration defect, data defect, calendar defect, implementation defect, or governance blocker was found. The only note is the recorded reconciliation observation for 2027-12-23 (§5), which is outside the study horizon and required no change. F-01, the calendar, the data, the instrument, and the validation scope were **not modified** (§27 of the mandate honored).

## 20. FINAL STAGE 2 VERDICT

### Final Independent Audit (Q1–Q13, per mandate §33)

- **Q1** Was any protected forward artifact inspected? **NO.** `runtime/`, G6 forward dirs, forward ledgers, and health/event logs were never read, hashed, or referenced (§4, §22).
- **Q2** Was any pre-freeze observation used as validation evidence? **NO.** The sealed baseline archive was consumed for structural pipeline testing only (schema/timestamps/session derivation/determinism); zero observations from it enter the validation population (§4, §7, §18).
- **Q3** Was F-01 modified? **NO.** The registered rule, session semantics, and position semantics are untouched (§3, §19).
- **Q4** Was the calendar modified? **NO.** The frozen calendar artifact is byte-identical to its registered hash; the 2027-12-23 flag was verified outside the study horizon and left as a documented observation (§5).
- **Q5** Was the instrument changed? **NO.** `USATECHIDXUSD`/`USTECm` identity verified against the registration (§3).
- **Q6** Was any parameter optimized? **NO.** Zero tunable parameters; only the registered operational constants were implemented (§3, §6).
- **Q7** Were economic outcomes calculated or exposed? **NO.** No return, P&L, expectancy, win rate, Sharpe, drawdown, distribution, or ranking exists in the implementation or this report (§17, §22).
- **Q8** Is the opportunity population deterministic? **YES if structurally valid.** Identical across repeated runs (§7, §11).
- **Q9** Can repeated runs reproduce it? **YES if structurally valid.** Two independent implementations identical (§12).
- **Q10** Is leakage absent? **YES if structurally valid.** Calendar-and-boundary-only construction; no future information (§10).
- **Q11** Is Conditional content absent? **YES.** The rule is the calendar partition alone (§3, gate S2-11).
- **Q12** Is the registered data boundary respected? **YES.** Forward-only from 2026-09-03; pre-freeze and protected-window data excluded (§4, §18).
- **Q13** Does Stage 2 remain purely structural? **YES.** All outputs are structural counts and integrity results (§17, §22).

**STRUCTURALLY VALID — DATA ACCRUAL PENDING.**

The registered F-01 decision process is fully implementable exactly as frozen: deterministic, reproducible, leakage-free, calendar- and data-integrity-clean, execution-conformant, Conditional-free, and with economic outcomes sealed. The validation-eligible population is currently empty because the forward-only boundary (2026-09-03) has accrued no observations yet — a governed state, not a defect. This verdict says nothing about whether F-01 makes money.

## 21. NEXT-MILESTONE BOUNDARY

The next milestone may be **F-01 V38A STAGE 3 ECONOMIC VALIDATION** — but ONLY once the frozen registration contains sufficient admissible post-freeze observations under the registered scope (primary segment days 1–63 and confirmation days 64–126, currently scheduled to complete 2026-12-02 and 2027-03-05 respectively). Until then the status is **DATA ACCRUAL PENDING**; Stage 3 must not begin early, and the protected interval and pre-freeze data remain permanently excluded.

## 22. REPOSITORY / GIT INTEGRITY

(GOVERNANCE FACT) Recorded at completion:

- HEAD before and after: `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`; branch `main`.
- Changes (exactly two new untracked files): `research/f01_v38a_stage2_structural.py` (the governed Stage-2 structural implementation, frozen at Stage-2 start per the freeze's implementation-reference rule; SHA `65189960e4150f31284fcd456cacf7c661b8555e4f0d5f919bae9be4bae08e8d`, 306 lines) and `output/research_discovery/QUANTFORGE_F01_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` (this report).
- No commit, no staging (execution milestone; no repository convention requires a commit).
- `SESSION_HANDOFF.md` intentionally NOT modified (execution milestones in this arc are recorded at the next governance-ratification point; no economic result exists to record).
- No source/configuration change; no Base Registry record; no validation result beyond this structural report; no new economic measurement; no protected-forward inspection; the sealed baseline data file is byte-identical to its frozen hash.
- `git diff --check` verified clean.
- Pre-existing dirty/untracked files (forward runtime data, G6 dirs, health/event ledgers, screening scripts, V37A phase-A, selection/cycle/design/freeze artifacts, superseded proposal) remain untouched.

## 23. HARD STOP

Stage 2 complete. **STRUCTURALLY VALID — DATA ACCRUAL PENDING.** Economic outcomes remain sealed; F-01 remains REGISTERED FOR STAGE 2 EXECUTION — not a Base, not validated, not eligible; **Base Registry EMPTY**.

STOP. No Stage 3; no performance inspection; no Stage 4 adjudication; no Registry entry; no Conditional components; no assembled testing; no registration alteration; no protected forward data; no scope expansion. H01/ORD/TRADEABLE_EDGE remain CLOSED; CAND-077/081/083/099 unchanged; CAND-015/024/035 protected-forward and excluded.

Next milestone (when the frozen registration contains sufficient admissible observations): **F-01 V38A STAGE 3 ECONOMIC VALIDATION** under the registered protocol. Nothing in this document authorizes that milestone or any research beyond it.