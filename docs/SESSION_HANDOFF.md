
# QUANTFORGE — SESSION HANDOFF

**Last session:** 2026-09-22
**Task completed:** External Information MVC Phase III — implementation, independent audit, and formal freeze bookkeeping.
**Status:** All infrastructure frozen. Research capacity on hold. Nothing authorized for next step.

---

## CURRENT PROJECT STATE (read this first)

```text
P0-Lite:                    FROZEN
P0-F1:                      FROZEN
P0-F2:                      FROZEN

EXTERNAL INFORMATION MVC:
  Phase I —                 FROZEN (§102)
  Phase II —                FROZEN (§103)
  Phase III —               FROZEN (§105)   ← just completed

RESEARCH CAPACITY:          HOLD (§99)
ACTIVE RESEARCH:            NONE
NEW CANDIDATE:              NONE
EXTERNAL DATA:              NONE ACQUIRED
BACKTEST:                   NONE
ECONOMIC VALIDATION:        NONE
BOE:                        UNCHANGED
GOVERNANCE:                 UNCHANGED
PHASE IV:                   NOT AUTHORIZED
```

## WHAT JUST HAPPENED (this session)

1. Phase III scope-definition audit confirmed §104 Classification B (owner authorization required).
2. Owner authorized Phase III implementation.
3. Phase III implemented: `artifact_store.py` (content-addressed local persistence), `grouping.py` (record batch semantics), updated `__init__.py`, 49 targeted tests.
4. Full test suite: 1141/0 (was 1092). Zero regressions.
5. Independent adversarial audit: 27 checks, all passed, zero blocking findings.
6. Formal freeze bookkeeping appended as §105.

## ROLE-CONTRACT UPDATE (2026-09-24) — REASONING UPDATE ONLY, NO STATE CHANGE

Owner-authorized adoption of the Lane B role addendum into `docs/CHATGPT_ROLE_AND_RESEARCH_CONTINUITY.md` (§31, status ADOPTED 2026-09-24). This is a **ROLE-CONTRACT / REASONING UPDATE ONLY**:

* Research Capacity HOLD remains unchanged;
* Active Research remains NONE;
* New Candidate remains NONE;
* External Data remains NONE ACQUIRED;
* Backtest remains NONE;
* Economic Validation remains NONE;
* Phase IV remains NOT DEFINED / NOT AUTHORIZED;
* BOE remains unchanged;
* existing prospective processes (supervisor, CAND-015/024/035, F-01/FB-001/RF-001 observers) remain protected;
* no Lane B empirical evaluation was authorized by adoption itself (evaluation requires separate explicit owner authorization tied to a frozen prototype/specification with prototype-count and complexity budgets).

## WHAT IS NOT AUTHORIZED

- No external-data acquisition (HTTP/API/scraper/download)
- No research activation
- No candidate creation
- No backtesting
- No economic validation
- No Phase IV
- No reopening closed research (RF-001, Idea 1, Idea 2, Idea 3)
- No new mechanism-discovery cycles
- No rescue of closed mechanisms
- No variant creation from closed lines

## KEY CONSTRAINTS (unchanged)

- §99: RESEARCH CAPACITY HOLD — OUTCOME C — NO BRANCH CURRENTLY JUSTIFIED
- §98: Liquidity-pool hypothesis = UNVALIDATED FUTURE HYPOTHESIS (negative-knowledge firewall active)
- §94: RF-001 CLOSED — ECONOMICALLY NOT SUPPORTED
- FB-001 freeze boundary: 2026-09-06 08:00 ET
- Dataset hash: 9fce00a4d04ae99c

## KEY FILE LOCATIONS

- `docs/SESSION_HANDOFF.md` — this file, authoritative project state (§65–§105)
- `docs/CHATGPT_ROLE_AND_RESEARCH_CONTINUITY.md` — permanent reasoning/role contract
- `research/external_information/` — External Information MVC (Phase I/II/III)
- `tests/test_external_information_phase3.py` — Phase III tests (49 tests)
- `data/rf001/` — RF-001 research data
- `data/tick_canonical/XAUUSD/` — 61 monthly parquet files, 281.5M rows

## GOVERNING RULES

- Read `docs/CHATGPT_ROLE_AND_RESEARCH_CONTINUITY.md` before any work
- Read `docs/SESSION_HANDOFF.md` (this file) for current state
- No Git commits/pushes unless explicitly authorized
- No strategy optimization, no parameter mining, no experiments
- Every file change must be traceable to an explicit owner request

---

## 65. GIT OVERSIZED FILE AUDIT & HISTORY REWRITE (2026-09-07)

**Status:** COMPLETE

**Completed work:**

1. Full audit of all tracked files and reachable Git history blobs against GitHub 100 MB limit.
2. Three push-blocking files identified:
   - `G6_CAND015_FORWARD_002/heartbeat.jsonl` � 168 MB (crash-loop noise, zero research value)
   - `G6_CAND015_FORWARD_002/connection_events.jsonl` � 168 MB (same crash-loop pattern)
   - `ORD_STAGE1_XAGUSD_EXEC_01/.../minute_quotes.csv.gz` � 17 MB (one-time prep data)
3. Root cause: files committed before `.gitignore` covered `.jsonl` and `.csv.gz` extensions. Once tracked, `.gitignore` cannot retroactively untrack.
4. Fix implemented:
   - Added `*.jsonl`, `*.csv.gz`, `output/` to `.gitignore`
   - Untracked all 482 files in `output/` directory via `git rm --cached`
   - Ran `git filter-repo --force --invert-paths` to remove the three oversized files from entire Git history
   - Re-added `origin` remote, pushed successfully
5. Backup branch `backup-before-history-rewrite` and tag created before destructive operation.
6. Audit report produced (`QUANTFORGE_GIT_OVERSIZED_FILE_AUDIT_V1.md`).

**Verification:**

- `git push` � SUCCESS (commit `4fec092` pushed)
- No tracked file exceeds 10 MB post-cleanup
- Historical blob `.freebuff/desktop-v2.db-wal` (5.5 MB) persists in history but is under GitHub limit
- All `output/` files remain on disk (untracked, not deleted)

**Governed states confirmed:**

- RF-001: RUNNER RESTARTED � TWO-MARKET RECORDER v2.0.0 ACTIVE � DATA ACCRUAL IN PROGRESS
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Next authorized task:** RF-001 V38A Stage 3 Economic Validation (requires =1 eligible post-freeze MATCHED observation).

---

## 66. GITIGNORE CANONICAL ARTIFACT RESTORATION (2026-09-07)

**Status:** COMPLETE

**Completed work:**

1. Post-cleanup audit (§65) identified FAIL: blanket `output/` gitignore rule excluded 382 canonical `.md`, `.json`, `.py`, `.txt` governance documents from Git tracking.
2. Root cause: `output/` added to `.gitignore` to prevent `heartbeat.jsonl` (168MB) from being re-tracked was too broad.
3. `.gitignore` corrected: replaced `output/` with 22 specific runtime/session directory ignore rules.
4. All 382 canonical artifacts verified and staged for commit.
5. Pre-commit verification: PASS (no runtime data, no `.csv`/`.npy`/`.jsonl`/`.parquet` staged, largest file 2.88MB).
6. Committed as `ea05034`, pushed successfully.
7. Restoration report produced (`QUANTFORGE_GITIGNORE_CANONICAL_ARTIFACT_RESTORATION_V1.md`).

**Verification:**

- `git push` — SUCCESS (commit `ea05034` pushed)
- Remote tracking: `main` ahead of `origin/main` by 0 commits
- 383 files tracked under `output/` (352 `.md`, 18 `.json`, 10 `.py`, 2 `.txt`)
- No runtime data, heartbeats, connection logs, or generated JSONL tracked
- Fresh clone will now include complete governance trail

**Governed states confirmed:**

- RF-001: RUNNER RESTARTED → TWO-MARKET RECORDER v2.0.0 ACTIVE → DATA ACCRUAL IN PROGRESS
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Next authorized task:** RF-001 V38A Stage 3 Economic Validation (requires ≥1 eligible post-freeze MATCHED observation).

---

## 67. RF-001 V38A STAGE 3 ECONOMIC VALIDATION — BLOCKED (2026-09-07)

**Status:** STAGE 3 BLOCKED — NO ELIGIBLE POST-FREEZE RF-001 OPPORTUNITY

**Completed work:**

1. Read all authoritative documents: registration artifact, owner selection freeze, two-market capture spec, V38A pathway design/ratification, F-01 Stage 3 precedent, Stage 2 report, session handoff.
2. Inspected canonical RF-001 two-market raw dataset (`data/rf001/raw/rf001_two_market_m1_raw.csv`).
3. Verified recorder code (line 243: `datetime.utcfromtimestamp(ts)`) confirms CSV timestamps are UTC.
4. Evaluated eligibility gate before any economic computation.

**Eligibility gate results:**

| Metric | Value |
|--------|-------|
| Total post-freeze synchronized rows | 94 |
| MATCHED rows | 94 |
| PRIMARY_ONLY events (logged) | 41 |
| CONFIRMATION_ONLY events (logged) | 3 |
| MISALIGNED events | 0 |
| CSV timestamp range (UTC) | 09:15–10:49 UTC |
| CSV timestamp range (ET) | 05:15–06:49 ET |
| Rows within US regular session (09:30–16:00 ET) | **0** |
| Eligible primary structural events | **0** |
| Eligible RF-001 opportunities | **0** |

**Root cause:** All 94 MATCHED observations are pre-market (05:15–06:49 ET). The frozen RF-001 session is US regular session (09:30–16:00 ET). Zero observations exist within the eligible session window.

**What was NOT done:** No economic statistics, no gross/net returns, no cost application, no distributional diagnostics, no profit factor, no backfill, no freeze relaxation, no parameter changes, no event manufacture.

**Governed states confirmed:**

- RF-001: STAGE 3 BLOCKED — DATA ACCRUAL CONTINUES (pre-market only so far)
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Next authorized task:** RF-001 V38A Stage 3 re-evaluation (requires ≥1 eligible post-freeze MATCHED observation within US regular session 09:30–16:00 ET). Accrual continues.

---

## 68. V38A NEW BASE MECHANISM DISCOVERY (2026-09-07)

**Status:** DISCOVERY COMPLETE — CANDIDATES READY FOR OWNER SELECTION

**Completed work:**

1. Read all authoritative V38/V38A doctrine (BF1-BF13, BS1-BS13, BV1-BV13).
2. Compiled comprehensive exclusion set: 21 exhausted mechanism dimensions (V36), all closed/rejected research, all formulated/discovered mechanisms (REL-M01/M02/M03, RF-001/002/003, F-01/F-02/F-03), all state observations (CAND-077/081/083/099).
3. Discovered 3 genuinely distinct mechanisms through mechanism-first reasoning:
   - **MECH-N01:** Structural Level Validation Flow (single-market, breakout validation → participant behavior change → directional flow)
   - **MECH-N02:** Cross-Asset Hedging Cascade (cross-market, large primary move → mechanical hedging flow → directional response)
   - **MECH-N03:** Session-Sequential Trend Quality (single-market, trend path quality → participant composition → follow/fade decision)
4. Verified distinctness: all 3 survive audit against all 21 exhausted dimensions, all RF-001/002/003, and all closed research.
5. No economic testing, no parameter optimization, no threshold mining performed.

**Exclusions/negative knowledge used:**
- 21 exhausted mechanism dimensions from V36 strategic assessment
- DISC-021 (mean reversion: non-viable), DISC-022 (TSMOM: not promotable), DISC-024 (session range: contradicted), DISC-025 (liquidity sweep: translation failure), DISC-026 (ORB: non-viable)
- CAND-105 (lead-lag: negative), CAND-107 (vol co-movement: redundant)
- SEED-002 (no-rescue doctrine)
- H01 (economic translation failure)
- 7 rejected mechanism concepts during discovery

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Artifact:** `output/research_discovery/QUANTFORGE_V38A_NEW_BASE_MECHANISM_DISCOVERY_V1.md`

**Next governed step:** Owner review of discovery artifact to determine whether any mechanism warrants progression to the Outcome-Blind Base Formulation Cycle (BF1–BF13).

---

## 69. MECH-N01 OWNER SELECTION FREEZE (2026-09-07)

**Status:** OWNER SELECTION COMPLETE — MECH-N01 SELECTED FOR FORMULATION

**Completed work:**

1. Read all authoritative V38/V38A doctrine (BS1–BS13, BF1–BF13, BV1–BV13).
2. Reviewed V38A New Base Mechanism Discovery artifact (MECH-N01/N02/N03).
3. Verified distinctness: MECH-N01 survives audit against all 21 exhausted dimensions, all RF-001/002/003, all state observations (CAND-077/081/083/099), and all closed research.
4. Owner selected MECH-N01 (Structural Level Validation Flow) for progression to Outcome-Blind Base Formulation Cycle (BF1–BF13).
5. Selection frozen: mechanism identity locked, no formulation performed, no parameters assigned, no economics computed, no registration created.

**Selection rationale:**
- Highest mechanism clarity, participant plausibility, observable determinism, execution realism among all candidates
- Single-market architecture (no cross-market complexity)
- Deterministic observable (K-bar hold is binary)
- Clearest falsification path (validated vs. invalidated breakouts)
- Lowest threshold-mining risk (N and K frozen structurally)
- Materially distinct from all exhausted dimensions, all RF-001/002/003, and all closed research

**Deferred mechanisms:**
- MECH-N02 (Cross-Asset Hedging Cascade): higher threshold-mining risk, less deterministic observable, may be better suited as Conditional
- MECH-N03 (Session-Sequential Trend Quality): dual-direction logic more complex, path quality → resilience link inferential

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Artifact:** `output/research_discovery/QUANTFORGE_MECH_N01_OWNER_SELECTION_FREEZE_V1.md`
**Selection record SHA256:** `1bab8a0c37d03c85552f39a68886f136835fbf19a85026f8a2e06143ab68262e`

**Next governed step:** Outcome-Blind Base Formulation Cycle for MECH-N01 under BF1–BF13.

---

## 70. MECH-N01 OUTCOME-BLIND BASE FORMULATION BF1–BF13 (2026-09-07)

**Status:** BF1–BF13 FORMULATION COMPLETE — PROVISIONALLY SELECTED ARCHITECTURE READY FOR OWNER ADJUDICATION

**Completed work:**

1. Read all authoritative V38/V38A doctrine (BS1–BS13, BF1–BF13, BV1–BF13).
2. Read MECH-N01 owner selection freeze artifact.
3. Completed BF1–BF13 formulation sections:
   - BF1: Mechanism preservation (structural level validation → participant behavior change → directional flow)
   - BF2: Observable definition (N-bar high/low, close-based breakout, K-bar hold)
   - BF3: Structural level (rolling N-bar high/low, frozen at breakout)
   - BF4: Structural break (close beyond level, no wick penetration, close confirmation required)
   - BF5: Validation/acceptance (K consecutive closes beyond level, all-or-nothing)
   - BF6: Direction (validated bullish → LONG, validated bearish → SHORT, no fade)
   - BF7: Opportunity population (single instrument, M1, no session filter, independent events)
   - BF8: Entry (open of bar E+K+1, max 3-bar delay)
   - BF9: Invalidation (rejection during K-bar window = no trade)
   - BF10: Exit (session close)
   - BF11: Execution model (M1 OHLCV, CFD on US equity index)
   - BF12: Outcome definition (entry-to-exit price difference, cost-adjusted)
   - BF13: Completeness audit (2 ambiguities identified, both delegated to governance)
4. Classified parameters:
   - N (lookback): GOVERNANCE-SELECTABLE (default: 60)
   - K (hold period): GOVERNANCE-SELECTABLE (default: 5)
   - Session scope: GOVERNANCE-SELECTABLE (default: no filter)
   - Max entry delay: GOVERNANCE-SELECTABLE (default: 3 bars)
   - No empirically tunable parameters
5. Explored 4 formulation architectures:
   - Architecture A (Minimal): SELECTED — highest mechanism fidelity, maximum determinism, minimum parameter burden
   - Architecture B (Session-Filtered): REJECTED — adds complexity without mechanism necessity
   - Architecture C (Retest Entry): REJECTED — inconsistent with mechanism, adds ambiguity
   - Architecture D (Multi-Level Confluence): REJECTED — different mechanism entirely
6. Identified remaining ambiguities:
   - Session definition for exit timing (delegated to governance)
   - Overlapping validation windows (resolved: concurrent trades permitted)
   - Structural level persistence after breakout (resolved: frozen at breakout)

**Governance compliance:** All BF1–BF13 clauses satisfied. All governance checks PASS.

**Parameter summary:**
- N (lookback period): GOVERNANCE-SELECTABLE, default 60
- K (validation hold period): GOVERNANCE-SELECTABLE, default 5
- Session scope: GOVERNANCE-SELECTABLE, default no filter
- Max entry delay: GOVERNANCE-SELECTABLE, default 3 bars
- No empirically tunable parameters

**Unresolved ambiguities:**
- Session definition for exit timing (delegated to governance at registration)

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Artifact:** `output/research_discovery/QUANTFORGE_MECH_N01_OUTCOME_BLIND_FORMULATION_V1.md`
**Formulation record SHA256:** `0a82d181219a7bf49c0f9e64a7d0240c666e06db9ad6d41089f7b5af96a5226c`

**Next governed step:** Owner adjudication of this formulation, followed (if approved) by BS1–BS13 selection and V38A registration.

---

## 71. MECH-N01 V38A BASE REGISTRATION (2026-09-07)

**Status:** V38A BASE REGISTRATION COMPLETE — MECH-N01 REGISTERED — STAGE 2 AUTHORIZED

**Completed work:**

1. Read all authoritative V38/V38A doctrine and MECH-N01 formulation/selection artifacts.
2. Resolved all governance-selectable parameters with mechanism-consistent design reasoning:
   - N = 60 M1 bars (1 hour lookback — structural granularity)
   - K = 5 M1 bars (5 minutes validation — persistence threshold)
   - Session scope: all eligible trading sessions (no filter — mechanism does not require restrictions)
   - Session exit: 23:59 UTC daily (deterministic, no daylight-saving complexity)
   - Max entry delay: REMOVED (inconsistent with minimal architecture; immediate entry at next bar open)
   - Stop-loss: NOT INCLUDED (mechanism does not hypothesize post-entry invalidation)
3. Froze all structural level semantics (rolling N-bar high/low, strict inequality, frozen at breakout).
4. Froze all validation semantics (K consecutive closes strictly beyond frozen level, all-or-nothing, breakout bar not counted).
5. Froze all direction semantics (follow validated break, no fade, no reversal without new event).
6. Froze all opportunity population rules (single instrument M1, independent events, concurrent trades permitted).
7. Froze all entry semantics (open of bar E+K+1, no delay, abandon if unavailable).
8. Froze all exit semantics (session close at 23:59 UTC, no target, no stop, no trailing).
9. Froze all risk/invalidation semantics (pre-entry rejection only; no post-entry stop).
10. Froze execution model (M1 OHLCV, deterministic bar-completion semantics, missing/duplicate data handling).
11. Froze outcome definition (entry-to-exit price difference, cost-adjusted).
12. Performed independent determinism audit — PASS: two researchers would produce identical implementations.
13. Confirmed Base Registry was EMPTY before registration.
14. Assigned Base ID: **BASE-001**.
15. Registered BASE-001 in the Base Registry.

**Frozen parameters:**
- N = 60 M1 bars
- K = 5 M1 bars
- Session scope: all sessions (no filter)
- Session exit: 23:59 UTC daily
- Entry: open of bar E+K+1 (no delay)
- Exit: session close (no stop, no target)

**Parameter governance notes:**
- Max entry delay was REMOVED (inconsistent with minimal architecture)
- Stop-loss was NOT INCLUDED (mechanism does not hypothesize post-entry invalidation)
- No empirically tunable parameters exist

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: **BASE-001 registered** (previously EMPTY)

**Artifact:** `output/research_discovery/QUANTFORGE_MECH_N01_V38A_BASE_REGISTRATION_V1.md`
**Registration record SHA256:** `6318e215296cac235f872135eb2997f2a10e1cb9d3334130fa979c0ccae6bbe2`

**Next governed step:** V38A Stage 2 — Structural Validation for BASE-001.

---

## 72. BASE-001 V38A STAGE 2 STRUCTURAL VALIDATION (2026-09-07)

**Status:** STAGE 2 STRUCTURAL VALIDATION PASS — BASE-001 STRUCTURALLY VALID — STAGE 3 AUTHORIZED

**Completed work:**

1. Read all authoritative V38/V38A doctrine and BASE-001 registration/formulation artifacts.
2. Performed structural-level audit: rolling 60-bar level, strict inequality, frozen at breakout — all PASS.
3. Performed breakout audit: first close beyond level, no intra-bar hindsight, deterministic event sequence — all PASS.
4. Performed validation audit: K=5 consecutive closes beyond frozen level, all-or-nothing, breakout bar not counted — all PASS.
5. Performed direction audit: upside → LONG, downside → SHORT, simultaneous impossible, no reversal — all PASS.
6. Performed entry audit: open of bar E+K+1, no delay, missing bar = abandon — all PASS.
7. Performed exit/session audit: 23:59 UTC daily, deterministic, no daylight-saving complexity — all PASS.
8. Performed opportunity-population audit: single instrument M1, all sessions, independent events — all PASS.
9. Performed missing-data audit: conservative treatment defined for all scenarios — PASS.
10. Performed lookahead/leakage audit: no temporal leakage detected — PASS.
11. Performed determinism/reproducibility audit: two researchers would produce identical implementations — PASS.
12. Constructed 18 synthetic edge-case scenarios: all produce expected deterministic outcomes — PASS.
13. Identified 4 non-blocking observations (out-of-order timestamps, malformed bars, incomplete bars, impossible OHLC — all implementation-level data-quality concerns).

**Audit summary:**
- All hard gates PASS
- All structural criteria PASS
- 18/18 synthetic edge cases PASS
- 0 material findings
- 4 non-blocking observations (data-quality concerns)

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 registered

**Artifact:** `output/research_discovery/QUANTFORGE_BASE001_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md`
**Validation record SHA256:** `191a7a256fd67d2b625a485b009bf7c1c3936cdb5629a608ec0190cccbb0e1e6`

**Next governed step:** V38A Stage 3 — Economic Validation for BASE-001.

---

## 73. BASE-001 V38A STAGE 3 ECONOMIC VALIDATION (2026-09-07)

**Status:** STAGE 3 EXECUTED — BASE-001 ECONOMIC EVIDENCE INSUFFICIENT FOR QUALIFICATION

**Completed work:**

1. Read all authoritative V38/V38A doctrine and BASE-001 registration/Stage 2 artifacts.
2. Audited USATECHIDXUSD M1 data: 906,815 bars, 2023-09-01 to 2026-07-10, zero data-quality exclusions.
3. Constructed complete BASE-001 opportunity population from frozen definition: 838 opportunities.
4. Calculated gross economics: 52.0% win rate, 0.0221% mean return, 1.06 profit factor.
5. Applied 2 bps round-trip cost: net mean 0.0021%, net profit factor 1.01.
6. Performed distribution analysis: extreme concentration (top 10% contribute 912% of return), max drawdown -40.91%.
7. Performed temporal robustness: 7 of 12 quarters negative, 2025 negative overall.
8. Performed directional analysis: LONG positive (0.0874% gross mean, 59% win rate), SHORT negative (-0.0566% gross mean, 43.7% win rate).
9. Performed session/time analysis: 51.7% of trades at hour 00 UTC (near-zero economics).
10. Performed statistical inference: p=0.957, not significantly different from zero, 95% CI [-0.076%, +0.080%].
11. Issued holistic economic adjudication: evidence does not support qualification.

**Key economic findings:**
- 838 opportunities over 1043 days (0.80 trades/day)
- Gross mean: 0.0221%, Net mean: 0.0021% (cost eliminates edge)
- Win rate: 52.0% gross, 49.9% net
- Max drawdown: -40.91%
- Statistical significance: p=0.957 (NOT significant)
- LONG side: positive (0.0874% gross, 59% win rate)
- SHORT side: negative (-0.0566% gross, 43.7% win rate)
- Return distribution: extreme concentration on少数 large winners

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 registered (not economically qualified)

**Artifacts:**
- `output/research_discovery/QUANTFORGE_BASE001_V38A_STAGE3_ECONOMIC_VALIDATION_V1.md` (SHA `c6cc9a53`)
- `output/base001_opportunity_table.csv` (838 opportunities)
- `scripts/forward/base001_stage3_validation.py` (validation script)

**Next governed step:** Owner adjudication of Stage 3 findings. The Base remains registered but is not economically qualified. Any governance action must follow the separate governance process.

---

## 74. BASE-001 OWNER ECONOMIC ADJUDICATION (2026-09-07)

**Status:** BASE-001 OWNER ADJUDICATION COMPLETE — BASE-001 NOT BASE-ELIGIBLE AND CLOSED

**Owner decision:** NOT BASE-ELIGIBLE — CLOSE BASE-001

**Primary evidence supporting decision:**
- Net mean return: +0.0021% (statistically indistinguishable from zero, p=0.957)
- 2 bps round-trip cost eliminates virtually all gross edge (0.0221% → 0.0021%)
- Maximum drawdown: -40.91%
- Return distribution pathological: top 10% of trades contribute 912% of total return
- Temporal instability: 7 of 12 quarters negative
- SHORT side destroys value: -0.0566% gross mean, 43.7% win rate
- Any repair would constitute rescue (prohibited)

**Lifecycle consequence:** BASE-001 transitions from REGISTERED to CLOSED / NOT BASE-ELIGIBLE.

**Negative knowledge preserved:**
- Mechanism was structurally valid (Stage 2 PASS)
- Gross edge was marginal (0.0221%)
- Cost eliminated edge
- Mechanism not symmetrically valid (LONG positive, SHORT negative)
- Return distribution fragile (concentration on tail events)
- Mechanism not temporally stable
- Risk profile severe (-40.91% drawdown)

**Future research observations (UNVALIDATED):**
- LONG-only structural validation may merit independent investigation (requires fresh discovery/formulation/selection/registration)
- Cost sensitivity suggests future mechanisms should be larger-magnitude
- Session/time concentration suggests potential for session-filtered variants

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE

**Artifact:** `output/research_discovery/QUANTFORGE_BASE001_OWNER_ECONOMIC_ADJUDICATION_V1.md`
**Adjudication record SHA256:** `c98f1255e223f0278cfad25fc6672cc12e2776a974050408be16601493cfabc8`

**Next governed step:** Base research pipeline continues. BASE-001 is closed. Future mechanism research may investigate the recorded research observations through fresh outcome-blind governance cycles.

---

## 75. FRESH V38A INDEPENDENT BASE MECHANISM DISCOVERY (2026-09-07)

**Status:** FRESH V38A MECHANISM DISCOVERY COMPLETE — CANDIDATES READY FOR OWNER SELECTION

**Completed work:**

1. Read all authoritative materials: SESSION_HANDOFF (through §74), V38/V38A doctrine, BASE-001 registration/Stage 2/Stage 3/adjudication, previous discovery (MECH-N01/N02/N03), relational discovery (REL-M01/M02/M03), V36 strategic assessment (21 exhausted dimensions), outcome-blind formulation doctrine (BF1–BF13), base hypothesis selection doctrine (BS1–BS13).
2. Compiled comprehensive exclusion set: 21 exhausted mechanism dimensions (V36), BASE-001 and all variants (structural level validation, K-bar hold, Architecture A/B/C/D), all formulated/discovered mechanisms (MECH-N01/N02/N03, REL-M01/M02/M03, RF-001/002/003, F-01/02/03), all closed research lines (H01, ORD, SEED-002, all TRADEABLE_EDGE families), protected-forward candidates (CAND-015/024/035), all state observations (CAND-077/081/083/099).
3. Discovered 3 genuinely distinct mechanisms through mechanism-first reasoning:
   - **MECH-F01:** Failed Breakout Inventory Reversal (single-market, failed breakout → trapped participants → forced liquidation → reversal)
   - **MECH-F02:** Shock-Induced Position Adjustment Cascade (single-market, large move → forced adjustments → self-reinforcing cascade → continuation)
   - **MECH-F03:** Overnight Gap Inventory Rebalancing (single-market, overnight gap → inventory rebalancing → opening session flow → continuation)
4. Verified distinctness: all 3 survive audit against all 21 exhausted dimensions, all RF-001/002/003, all MECH-N01/N02/N03, and all closed research.
5. Different failure modes: F01 fades (reversal), F02 follows (forced adjustments), F03 follows (inventory rebalancing).
6. All 3 are Base-potential: self-contained, self-triggering, no Conditional dependence required.
7. No economic testing, no parameter optimization, no threshold mining performed.

**Exclusions/negative knowledge used:**
- 21 exhausted mechanism dimensions from V36 strategic assessment
- BASE-001 closed/not-base-eligible (adjudication artifact)
- DISC-021 (mean reversion: non-viable), DISC-022 (TSMOM: not promotable), DISC-024 (session range: contradicted), DISC-025 (liquidity sweep: translation failure)
- CAND-105 (lead-lag: negative), CAND-106 (intra-bar: negative), CAND-107 (vol co-movement: redundant)
- CAND-074/075 (settlement/benchmark: no directional value)
- SEED-002 (no-rescue doctrine)
- 12 rejected mechanism concepts during discovery

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE

**Artifact:** `output/research_discovery/QUANTFORGE_V38A_FRESH_INDEPENDENT_MECHANISM_DISCOVERY_V1.md`

**Next governed step:** Owner review of discovery artifact to determine whether any mechanism warrants progression to the Outcome-Blind Base Formulation Cycle (BF1–BF13).

---

## 76. MECH-F DISTINCTNESS ADJUDICATION (2026-09-07)

**Status:** DISTINCTNESS AUDIT COMPLETE — ONE OR MORE CANDIDATES REQUIRE EXCLUSION/REFORMULATION

**Completed work:**

1. Read all authoritative materials: SESSION_HANDOFF (through §75), fresh discovery artifact, CAND-081 governance review/independence audit/SEED-002 registration/results, BASE-001 formulation/registration/Stage 3/adjudication, MECH-N01 formulation, RF-003 formulation, liquidity sweep closure/adjudication, V36 strategic assessment.
2. Deep audit of MECH-F01 vs CAND-081: Identical mechanism (breakout → failure → trapped participants → forced liquidation → reversal). Governance-level difference only (decision process vs. observation). Mechanism-level distinctness: NOT ACHIEVED.
3. Audit of MECH-F02 vs prior shock/vol research: Forced-adjustment mechanism is plausible but not independently observable from M1 OHLCV. Trigger ("exceeds threshold") is empirical, not mechanistic. Overlaps with post-magnitude directional drift (exhausted). Mechanism-level distinctness: PARTIAL.
4. Audit of MECH-F03 vs prior gap/opening research: Decision rule is functionally identical to gap-following momentum. Inventory-rebalancing mechanism is interpretive overlay, not independently observable. Overlaps with settlement/benchmark windows (exhausted). Mechanism-level distinctness: PARTIAL.
5. Mechanism-level comparison: 8/8 dimensions same for F01 vs CAND-081. F02 vs post-magnitude drift: 1/8 same, 5/8 partial, 2/8 distinct. F03 vs gap momentum: 2/8 same, 5/8 partial, 0/8 distinct.
6. All three candidates classified as PARTIALLY DISTINCT. No candidate achieves mechanism-level DISTINCT.

**Critical findings:**

- **MECH-F01 is the same mechanism as CAND-081.** The causal chain is identical. The difference is governance classification (decision process vs. observation), not mechanism.
- **MECH-F02's mechanism is not independently observable.** Forced adjustments cannot be distinguished from normal trading using M1 OHLCV data.
- **MECH-F03's decision rule is gap-following momentum.** The inventory-rebalancing story does not change the observable, timing, or direction.

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE

**Artifact:** `output/research_discovery/QUANTFORGE_MECH_F_DISTINCTNESS_ADJUDICATION_V1.md`

**Next governed step:** Owner review of distinctness findings. Owner selection is authorized for all three candidates with full disclosure of overlap findings. No candidate is excluded, but the owner must understand the mechanism-level overlaps before selecting any candidate for formulation.

---

## 77. V38A MECHANISM NOVELTY-GATED FRESH DISCOVERY (2026-09-07)

**Status:** NOVELTY-GATED DISCOVERY COMPLETE — NO MECHANISM PASSED THE NOVELTY GATE

**Completed work:**

1. Read all authoritative materials: SESSION_HANDOFF (through §76), V38/V38A doctrine, BASE-001 discovery through closure, MECH-N01/N02/N03, MECH-F01/F02/F03, distinctness adjudication, CAND-077/081/083/099 governance, V36 strategic assessment (21 exhausted dimensions), relational discovery/formulations, liquidity sweep closure.
2. Built comprehensive exclusion set: 21 exhausted dimensions, 6 explicit rejection families (structural failure/trapped participant, gap-following, large-move continuation, volatility regime, momentum/trend, cross-market), 8 indicator/threshold patterns.
3. Discovered 4 initial candidates through mechanism-first reasoning:
   - MECH-X01 (Breakout Velocity Conviction): FAIL — same mechanism family as BASE-001
   - MECH-X02 (Post-Extreme Directional Absorption): FAIL — same mechanism family as CAND-081
   - MECH-X03 (Directional Conviction Decay): FAIL — same mechanism family as MECH-N03
   - MECH-X04 (Information Absorption Asymmetry): FAIL — same mechanism family as MECH-F02
4. Applied five-test novelty gate (causal distinctness, observable distinctness, economic-transmission distinctness, failure-mode distinctness, independent falsifiability). All four candidates FAIL.
5. Rejected 8 additional candidates before five-test gate (data infeasibility or overlap with exhausted dimensions).
6. Zero survivors. Owner-selection eligibility set is EMPTY.

**Critical findings:**

- The M1 OHLCV mechanism space has been exhaustively explored through 95+ candidates (V19–V36), plus MECH-N/F discovery cycles.
- Remaining candidate concepts either duplicate existing mechanisms with different measurements/levels/interpretations, or require data not available in the governed dataset.
- A zero-survivor cycle is scientifically acceptable and preferable to false novelty.

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE

**Artifact:** `output/research_discovery/QUANTFORGE_V38A_MECHANISM_NOVELTY_GATED_DISCOVERY_V1.md`

**Next governed step:** The novelty-gated discovery cycle is complete with zero survivors. The M1 OHLCV single-market mechanism space appears exhaustively explored. Future mechanism discovery may require: (a) different data (order flow, tick data, cross-asset), (b) different timeframes, or (c) genuinely different market microstructure hypotheses that are independently observable.

---

## 78. TICK-DATA CAPABILITY & MICROSTRUCTURE READINESS AUDIT (2026-09-07)

**Status:** AUDIT COMPLETE — PARTIALLY READY — PREREQUISITE DATA/INFRASTRUCTURE WORK REQUIRED

**Completed work:**

1. Read all authoritative sources: SESSION_HANDOFF (through §77), tick validator, tick-to-M1 converter, tick parquet converter, RF-001 recorder, F-01 recorder, validation reports for 5 symbols, test fixture parquet, M1 derived data.
2. Inspected actual tick data files on disk (5 CSV files, ~40 GB total, ~930M rows).
3. Verified field semantics from actual records (not from field names).
4. Audited timestamp fidelity, event ordering, completeness.
5. Assessed reconstruction capability and research readiness.

**Critical findings:**

- **4 symbols have true tick data** (USATECHIDXUSD, XAUUSD, XAGUSD, BTCUSD): 6 columns (date, time, bid, ask, last, volume), second resolution, 1,043–1,825 days coverage, validation PASS.
- **EURUSD "tick" data is mislabelled.** File contains M1 OHLCV (7 columns, OHLCV structure, minute resolution), not tick data.
- **`last` field equals `bid` for all observations.** No independent trade-price evidence. Trade/quote separation NOT possible.
- **`volume` field is zero for all tick data.** Real trade volume NOT available. Tick count IS available.
- **No order-book depth.** Top-of-book only (best bid/ask).
- **No trade/quote event-type flag.** Cannot distinguish quote updates from trades.
- **No prospective tick capture.** Live recorder captures M1 bars, not ticks.
- **Parquet infrastructure exists but has not been executed** on full datasets.

**Newly observable research classes (with current data):**
- Spread dynamics and spread-state transitions
- Event intensity transitions (ticks per second)
- Quote update frequency and churn
- Microstructure volatility transitions
- Intraday spread-return dynamics
- Bid/ask independence dynamics

**NOT observable with current data:**
- True order flow (aggressor classification)
- Real trade volume
- Order-book depth and liquidity replenishment
- Trade events (separate from quote updates)
- Institutional positioning

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE

**Artifact:** `output/research_discovery/QUANTFORGE_TICK_DATA_MICROSTRUCTURE_READINESS_AUDIT_V1.md`

**Next governed step:** Tick-level mechanism discovery is PARTIALLY AUTHORIZED. The data supports research in spread dynamics, event intensity, and quote-level microstructure. Trade-flow, volume-based, and depth-based research remain blocked. Prospective tick capture would require building a new recorder using MT5's `copy_ticks_from()` API.

---

## 79. CANONICAL TICK DATA INFRASTRUCTURE — READY FOR QUOTE-LEVEL MICROSTRUCTURE DISCOVERY (2026-09-07)

**Status:** CANONICAL TICK DATA SUBSTRATE COMPLETE — READY FOR QUOTE-LEVEL MICROSTRUCTURE DISCOVERY

**Completed work:**

1. Built canonical tick data canonicalizer (`scripts/data/tick_canonicalizer.py`). Streaming, bounded-memory, chunked processing. 9-column schema (source_row_ordinal, date, time, bid, ask, last, vol, mid, spread).
2. Wrote 16 validation tests (`tests/test_tick_canonicalizer.py`). All 16 PASS.
3. Canonicalized all 4 validated tick datasets:
   - XAGUSD: 146,389,821 rows → 61 partitions, 0 rejected
   - USATECHIDXUSD: 173,457,022 rows → 35 partitions, 0 rejected
   - XAUUSD: 281,514,283 rows → 61 partitions, 0 rejected
   - BTCUSD: 299,204,931 rows → 61 partitions, 0 rejected
   - **Total: 900,566,057 rows canonicalized, 0 rejected.**
4. Generated provenance manifests for all 4 symbols (SHA-256 checksums, column hashes, partition inventories, quality statistics).
5. Wrote canonical tick data specification (`QUANTFORGE_CANONICAL_TICK_DATA_SPECIFICATION_V1.md`).
6. Wrote migration report (`QUANTFORGE_CANONICAL_TICK_DATA_MIGRATION_REPORT_V1.md`).

**Critical findings:**
- Zero rejected rows across 900M+ rows — raw source data is structurally clean.
- 70.1% of rows have duplicate timestamps (multiple quote updates per second). All preserved.
- Canonical Parquet: 14.8 GB total (63% compression from ~40 GB raw CSV).
- 218 monthly partitions across 4 symbols.

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE

**Artifacts:**
- Specification: `output/research_discovery/QUANTFORGE_CANONICAL_TICK_DATA_SPECIFICATION_V1.md`
- Migration report: `output/research_discovery/QUANTFORGE_CANONICAL_TICK_DATA_MIGRATION_REPORT_V1.md`
- Canonicalization code: `scripts/data/tick_canonicalizer.py`
- Validation tests: `tests/test_tick_canonicalizer.py`
- Canonical data: `data/tick_canonical/<SYMBOL>/<YYYYMM>.parquet`
- Manifests: `data/tick_canonical/<SYMBOL>/manifest.json`

**Next governed step:** Quote-level microstructure mechanism discovery is AUTHORIZED for the 7 supported research domains (spread dynamics, event intensity, quote churn, micro-volatility, spread-return dynamics, bid/ask independence, intrabar path). Trade-flow, volume-based, and depth-based research remain blocked. Prospective tick capture would require a new recorder using MT5's `copy_ticks_from()` API.

---

## 80. QUOTE MICROSTRUCTURE NOVELTY DISCOVERY — THREE MECHANISMS SURVIVE (2026-09-07)

**Status:** QUOTE-MICROSTRUCTURE NOVELTY DISCOVERY COMPLETE — THREE GENUINELY DISTINCT MECHANISMS READY FOR OWNER SELECTION

**Completed work:**

1. Read all authoritative materials: SESSION_HANDOFF (through §79), tick data audit, canonical spec, migration report, V36 exhausted dimensions, V38A novelty-gated discovery, prior mechanism definitions.
2. Built comprehensive exclusion set: 21 exhausted dimensions, 7 explicit rejection families, 7 rejected tick-level concepts.
3. Discovered 3 initial candidates through mechanism-first reasoning:
   - MECH-T01 (One-Sided Quote Adjustment Asymmetry): PASS — 5/5 novelty tests
   - MECH-T02 (Quote-Adjusted Spread Transition): PASS — 5/5 novelty tests
   - MECH-T03 (Spread-Midpath Coupling): PASS — 5/5 novelty tests
4. Applied five-test novelty gate (information novelty, causal distinctness, quote-layer economic pathway, independent falsifiability, prospective observability). All 3 candidates PASS all 5 tests.
5. Applied M1 equivalence test and mechanism equivalence test. All 3 PASS.
6. Rejected 7 candidates before five-test gate (overlap with exhausted dimensions).
7. Zero rejected after five-test gate.

**Critical findings:**

- **3 candidates survive the novelty gate** — first tick-level discovery cycle produces survivors (previous M1 cycle produced zero).
- **Bid/ask independence is a genuinely new information dimension.** XAGUSD has 35.5% one-sided quote adjustments; USATECHIDXUSD has 0.0%. This variation is completely hidden by M1 aggregation.
- **The tick/quote layer provides genuinely new mechanisms** not available from M1 OHLCV.
- Owner-selection eligibility set contains 3 candidates.

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE

**Artifact:** `output/research_discovery/QUANTFORGE_V38A_QUOTE_MICROSTRUCTURE_NOVELTY_DISCOVERY_V1.md`

**Next governed step:** Owner may select any of the 3 surviving candidates for outcome-blind formulation (BF1–BF13). No candidate is formulated or registered in this task.

---

## 81. QUOTE MICROSTRUCTURE RECONCILIATION — §80 OVERTURNED (2026-09-08)

**Status:** §80 VERDICT OVERTURNED — NO OWNER-SELECTION ELIGIBLE MECHANISM

**Purpose:** Controlled reconciliation of §80 following independent read-only scientific and governance audit.

### Prior verdict (§80 — SUPERSEDED)

§80 claimed three genuinely distinct mechanisms (MECH-T01, MECH-T02, MECH-T03) ready for owner selection, all passing 5/5 novelty tests.

### Independent audit result

An independent audit found:

1. **All four headline empirical statistics were incorrect.** XAGUSD claimed 35.5% → actual 13.5%. XAUUSD claimed 22.5% → actual 48.2%. BTCUSD claimed 1.5% → actual 49.6%. USATECHIDXUSD claimed 0.0% → actual 0.7%. Corrected via canonical Parquet verification (all partitions, `source_row_ordinal`-ordered tick-to-tick comparison).
2. **T01 has genuine information novelty** (bid/ask independence is real and unavailable from M1) **but mechanism novelty is unestablished** ("directional pressure from quote makers" is a participant hypothesis, not an observed mechanism).
3. **T02 is mechanism-equivalent to T01** — same underlying bid/ask adjustment events, different target variable. Does not establish a different market-generating process.
4. **T03 maps to exhausted dimensions** — removing the tick-specific component (spread-change) leaves an M1-available variable (mid-direction) combined with concepts covered by exhausted volatility/momentum research.
5. **Causal-language overreach identified** — the discovery artifact attributes "signaling," "anchoring," "pressure," and "capitulation" to quote updates that cannot support such inferences. Quote data does not contain participant intent.
6. **Five-test gate was applied conceptually, not empirically** — the artifact states PASS without verifying the supporting empirical claims.

### Corrected candidate status

| Candidate | Classification | Owner-selection eligible? |
|-----------|---------------|--------------------------|
| MECH-T01 (One-Sided Quote Adjustment Asymmetry) | INFORMATION-NOVEL / MECHANISM NOVELTY UNESTABLISHED | **NO** |
| MECH-T02 (Quote-Adjusted Spread Transition) | MECHANISM-EQUIVALENT TO T01 / NOT DISTINCT | **NO** |
| MECH-T03 (Spread-Midpath Coupling) | NOT GENUINELY DISTINCT / EXHAUSTED-DIMENSION INTERACTION | **NO** |

### Owner selection

**NONE**

### Preserved positive knowledge

Bid/ask independence is a genuinely new quote-level information dimension relative to M1 OHLCV. Cross-symbol variation is real: USATECHIDXUSD 0.7%, XAGUSD 13.5%, XAUUSD 48.2%, BTCUSD 49.6%. This information dimension remains available for future investigation.

### Preserved negative knowledge

1. Feature novelty does not imply mechanism novelty.
2. A quote-level observable can be genuinely new without constituting a new market mechanism.
3. Different target variables over the same quote events do not automatically create different mechanisms.
4. Tick-derived interaction terms can collapse to exhausted M1 mechanisms when the tick-specific component is removed.
5. Quote updates cannot be interpreted as trade aggression without transaction/order-flow evidence.
6. Participant narratives must have observable discriminators.
7. Incorrect descriptive statistics invalidate supporting evidence even when the conceptual research direction is legitimate.

### Economics

**No economic testing was performed or authorized.** No profitability, expectancy, cost, tradeability, or robustness assessment was conducted.

### Protected systems

- BASE-001: UNCHANGED — remains CLOSED / NOT BASE-ELIGIBLE
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: UNCHANGED — DEFERRED
- RF-003: UNCHANGED — DEFERRED
- F-01: UNCHANGED
- F-02: UNCHANGED
- F-03: UNCHANGED
- FB-001: UNCHANGED
- Protected-forward states: UNCHANGED
- Live runner: UNINTERRUPTED
- Canonical tick data: UNCHANGED
- Canonical tick specification: UNCHANGED

### Next authorized task

Fresh quote-level mechanism discovery may be considered under the existing governance framework, using the newly established bid/ask independence information dimension as research substrate, but without assuming a mechanism or economic edge. The next discovery must be genuinely mechanism-oriented and independently screened.

### Forbidden next task

No formulation of T01/T02/T03. No owner selection. No Base registration. No Stage 2. No Stage 3. No economics. No optimization. No rescue of failed mechanisms. No threshold selection. No spread threshold mining. No event threshold mining. No holding-period search. No return testing. No profitability testing.

### Artifact

`output/research_discovery/QUANTFORGE_V38A_QUOTE_MICROSTRUCTURE_NOVELTY_DISCOVERY_V1.md` — updated with POST-AUDIT RECONCILIATION section (§19).

---

## 82. FRESH QUOTE-LEVEL MECHANISM DISCOVERY — ZERO SURVIVORS (2026-09-08)

**Status:** FRESH QUOTE-LEVEL MECHANISM DISCOVERY COMPLETE — ZERO SURVIVORS

**Purpose:** Fresh, independent, mechanism-first quote-level discovery sprint following the §81 reconciliation.

### Discovery scope

- 6 initial candidates generated through mechanism-first reasoning
- All 6 rejected at prior-art separation gate
- 0 candidates reached formal five-test novelty gate
- 0 survivors

### Candidate summary

| Candidate | Name | Rejection reason |
|-----------|------|-----------------|
| Q01 | Quote-Update Burstiness Regime | Collapses to exhausted event clustering (CAND-098) |
| Q02 | Quote-Update Persistence Regime | Collapses to exhausted volatility regime + event clustering |
| Q03 | Quote-Side Sequential Dominance | Mechanism-equivalent to T01 |
| Q04 | Spread-Adjustment Consistency | Mechanism-equivalent to T01/T02 |
| Q05 | Spread-Path Directional Coupling | Mechanism-equivalent to T03 |
| Q06 | Quote-Activity State Transition | Composite of exhausted dimensions + T01 |

### Exhaustion pattern

- Quote-activity temporal patterns (Q01, Q02) → exhausted event clustering / volatility regime
- Quote-side counting patterns (Q03, Q04) → T01/T02 (information-novel, mechanism novelty unestablished)
- Quote-price interaction patterns (Q05) → T03 (not genuinely distinct)
- Composite patterns (Q06) → exhausted dimensions + T01

### Negative knowledge

1. The canonical tick substrate provides genuinely new information (bid/ask independence, quote-update timing, spread dynamics at tick resolution).
2. Across the executed quote-level discovery cycles, no mechanism-level survivor was identified within the specifically searched and governed quote-level information space and exclusion set.
3. Feature novelty remains established. Mechanism novelty remains unestablished across two discovery cycles.
4. A zero-survivor result is scientifically preferable to a feature disguised as a mechanism.

### Preserved states

- T01: INFORMATION-NOVEL / MECHANISM NOVELTY UNESTABLISHED (unchanged)
- T02: MECHANISM-EQUIVALENT TO T01 (unchanged)
- T03: NOT GENUINELY DISTINCT (unchanged)
- Bid/ask independence: valid information-level research dimension (unchanged)

### Economics

**No economic testing was performed or authorized.**

### Protected systems

- BASE-001: UNCHANGED — CLOSED / NOT BASE-ELIGIBLE
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: UNCHANGED — DEFERRED
- RF-003: UNCHANGED — DEFERRED
- F-01: UNCHANGED
- F-02: UNCHANGED
- F-03: UNCHANGED
- FB-001: UNCHANGED
- Protected-forward states: UNCHANGED
- Live runner: UNINTERRUPTED
- Canonical tick data: UNCHANGED
- Canonical tick specification: UNCHANGED

### Artifact

`output/research_discovery/QUANTFORGE_V38A_QUOTE_MICROSTRUCTURE_FRESH_MECHANISM_DISCOVERY_V1.md`

### Next authorized governed step

The quote-level mechanism space has been explored across two discovery cycles (T01/T02/T03 and Q01–Q06). Both cycles produced zero mechanism-level survivors. The bid/ask independence dimension remains valid information-level knowledge but has not yielded a distinct market-generating mechanism.

Future research may consider:
- Whether the exhausted mechanism families should be revisited with tick-level observables as alternative measurements (rather than new mechanisms), subject to the normal reopening and research-registration requirements
- Whether prospective tick data capture would enable mechanism discovery at a different resolution, if separately authorized
- Whether the exclusion set should be refined based on the two-cycle exhaustion pattern

These are opportunities, not authorizations. Any future research direction requires the normal governance and registration process.

### Forbidden next steps

No formulation. No owner selection. No Base registration. No Stage 2/3. No economics. No optimization. No rescue of rejected mechanisms. No threshold selection. No closed line reopening.

---

## 83. RF-001 V38A STAGE 3 ECONOMIC VALIDATION (2026-09-08)

**Status:** STAGE 3 EXECUTED — NO STRUCTURALLY QUALIFYING OPPORTUNITIES IN CURRENT ACCRUAL WINDOW

**Purpose:** Execute frozen RF-001 V38A Stage 3 Economic Validation on naturally accrued eligible data.

### Authorization basis

A read-only current-state audit (2026-09-08) established that the previously blocking RF-001 eligibility condition has been naturally satisfied through continued forward data accrual. The canonical dataset contains 1,302 MATCHED observations, of which 210 fall within the frozen US regular session (09:30–16:00 ET) on 2026-09-07. The sole Stage 3 blocking condition — ≥1 eligible post-freeze MATCHED observation within the frozen session window — is cleared.

### Frozen contracts applied

- Primary: USATECHIDXUSD (USTECm), N=30
- Confirmation: US500 (US500m), M=15
- Session: US regular (09:30–16:00 ET)
- Entry: open of bar E+17; Exit: session close (16:00 ET)
- Cost: 2 bps round-trip
- Direction: Bullish primary + failed confirmation → SHORT US500; Bearish primary + failed confirmation → LONG US500

### Data integrity

| Check | Result |
|-------|--------|
| Total rows | 1,302 (all MATCHED, all post-freeze) |
| Timestamp ordering | PASS |
| Duplicate timestamps | 0 |
| Zero-price rows | 0 |
| Malformed bars | 0 |
| Session-eligible rows | 210 (2026-09-07 09:30–12:59 ET) |

Data quality: CLEAN. No exclusions.

### Eligibility funnel

| Stage | Count |
|-------|------:|
| Raw post-freeze observations | 1,302 |
| MATCHED observations | 1,302 |
| Session-eligible observations | 210 |
| Primary structural events (N=30 breakout) | 14 |
| Events excluded (insufficient session time) | 0 |
| Eligible primary events | 14 |
| Confirmed by US500 (no opportunity) | 5 |
| Invalidated (primary reversed before entry) | 9 |
| Confirmation failures (potential opportunities) | 0 |
| **Eligible RF-001 opportunities** | **0** |

### Event outcomes

- 5 of 14 events (35.7%) confirmed by US500 within 15-bar window
- 9 of 14 events (64.3%) invalidated — primary market reversed before entry
- 7 of 9 invalidations occurred within 1–3 bars (rapid reversal characteristic)
- 0 confirmation failures with sustained primary

### Economic results

**No opportunities exist.** Gross and net economic computation is not applicable.

### Statistical evidence

**Not applicable.** No sample exists for testing.

### Governance adjudication

**STAGE 3 EXECUTED — NO STRUCTURALLY QUALIFYING RF-001 OPPORTUNITIES IN THE CURRENT ELIGIBLE ACCRUAL WINDOW. ECONOMIC EVIDENCE NOT YET AVAILABLE.**

This is distinct from the former eligibility block. The authorization gate is satisfied while the resulting structural opportunity population is zero. The mechanism has not been validated or invalidated economically.

### Negative knowledge

1. Primary structural events occur frequently (14 in 3.5 hours)
2. US500 confirmation is common (35.7% of events)
3. Invalidation is the dominant outcome (64.3%)
4. Rapid invalidation is characteristic (7 of 9 within 1–3 bars)
5. No opportunities produced in this accrual window

### Limitations

- Single session day (2026-09-07 only)
- Partial session coverage (09:30–12:59 ET, not full session)
- Insufficient data for economic conclusions

### Protected systems

- RF-001 recorder: UNINTERRUPTED — still accruing
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- BASE-001: CLOSED / NOT BASE-ELIGIBLE
- T01: INFORMATION-NOVEL / MECHANISM NOVELTY UNESTABLISHED
- T02: MECHANISM-EQUIVALENT TO T01
- T03: NOT GENUINELY DISTINCT
- Q01–Q06: ZERO SURVIVORS
- Canonical tick data: UNCHANGED
- Live runner: UNINTERRUPTED

### Artifact

`output/research_discovery/QUANTFORGE_RF001_V38A_STAGE3_ECONOMIC_VALIDATION_V1.md`

### Next authorized task

Continue RF-001 V38A natural data accrual. Re-evaluate Stage 3 only when sufficient additional eligible observations have accrued to produce a meaningful structural opportunity population.

### Forbidden next tasks

No parameter changes. No optimization. No threshold mining. No variant testing. No session expansion. No backfill. No event manufacture. No RF-001 recorder interruption. No research substitution. No alternative mechanism discovery. No closed line reopening.

---

## 84. MECH-N03 V38A BASE REGISTRATION (2026-09-08)

**Status:** V38A BASE REGISTRATION COMPLETE — MECH-N03 REGISTERED — EXECUTION NOT AUTHORIZED

**Completed work:**

1. Read all authoritative V38/V38A doctrine and MECH-N03 formulation/selection artifacts.
2. Resolved all governance-selectable parameters with mechanism-consistent design reasoning:
   - D = 10 M1 bars (10 minutes — trend quality assessment window)
   - Impulse threshold: noise < 0.30
   - Grinding threshold: noise ≥ 0.50
   - Intermediate: 0.30 ≤ noise < 0.50 → EXCLUDED
   - Session: US regular 09:30–16:00 ET
   - Consecutive sessions required
   - Entry: open of first M1 bar in Session B (09:30 ET)
   - Exit: close of last M1 bar in Session B (16:00 ET)
   - Cost: 2 bps round-trip
   - Minimum sample: 100/100/200/50 (impulse/grinding/historical/forward)
   - Economic gate: Mean net decision return > 0
3. Froze all observable semantics (path noise count, trend direction, classification thresholds).
4. Froze all session semantics (US regular, consecutive, timezone handling).
5. Froze all decision semantics (impulse follow, grind fade, intermediate no-trade).
6. Froze all outcome semantics (Session B return, net of 2 bps).
7. Froze all statistical semantics (bootstrap 95% CI, H₁/H₂ separate adjudication).
8. Froze all robustness semantics (D sensitivity {5,10,15,20} exploratory, threshold sensitivity exploratory).
9. Performed independent determinism audit — PASS: two researchers would produce identical implementations.
10. Verified Base Registry state: BASE-001 CLOSED / NOT BASE-ELIGIBLE.
11. Assigned Base ID: **BASE-002**.
12. Registered BASE-002 in the Base Registry.

**Frozen parameters:**
- D = 10 M1 bars (trend window length)
- Impulse: noise < 0.30
- Grinding: noise ≥ 0.50
- Session: US regular 09:30–16:00 ET
- Consecutive sessions required
- Entry: open of first M1 bar in Session B
- Exit: close of last M1 bar in Session B
- Cost: 2 bps round-trip
- Minimum sample: 100/100/200/50
- Economic gate: Mean net decision return > 0

**Parameter governance notes:**
- D resolved at registration following MECH-N01/BASE-001 precedent (N, K resolved at registration with mechanism-consistent design reasoning)
- Minimum sample resolved at registration as governance decision
- Economic gate resolved at registration as governance decision
- D sensitivity {5,10,15,20} is EXPLORATORY only, not confirmatory
- No empirically tunable parameters exist

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE, **BASE-002 registered** (MECH-N03)

**Artifact:** `output/research_discovery/QUANTFORGE_MECH_N03_V38A_BASE_REGISTRATION_V1.md`
**Registration record SHA256:** `5aa978d007ada2de4d7f15667d9c2c699c6fc173b7854c985b37f3a3d7a0e877`

**Next governed step:** V38A Stage 2 — Structural Validation for BASE-002 (requires separate execution-authorization decision). Registration does NOT authorize Stage 2 or Stage 3 execution.

---

## 85. BASE-002 ECONOMIC GATE RECONCILIATION & REGISTRATION AMENDMENT (2026-09-08)

**Status:** RECONCILIATION COMPLETE — BASE-002 AMENDED — AWAITING FINAL FREEZE AUDIT

**Purpose:** Governed reconciliation of BASE-002 registration following the freeze audit (CONDITIONAL PASS). One material blocker and two non-blocking issues resolved.

**Completed work:**

1. Read all authoritative V38/V38A doctrine and BASE-002 registration/freeze audit artifacts.
2. Applied owner decision: Primary economic gate = INCREMENTAL ECONOMIC VALUE (Δ net return > 0 vs. unconditional directional counterfactual).
3. Amended §14 (Primary Economic Gate): Changed from "Mean net decision return > 0" (absolute) to "Δ net return > 0 vs. counterfactual" (incremental).
4. Amended §13 (Minimum Sample): Resolved 100/100/200/50 ambiguity — 100 = impulse minimum, 100 = grinding minimum, 200 = derived (100+100), 50+50 = forward minimum.
5. Amended §15 (Statistical Plan): Updated primary statistic to Δ net return; defined H₁/H₂ mixed-result rule (SUPPORTED / PARTIALLY SUPPORTED / CONTRADICTED / INCONCLUSIVE).
6. Amended §16 (Counterfactual): Aligned with amended §14; primary gate = Δ > 0.
7. Amended §29 (Economic Translation Audit): Updated to reflect incremental gate.
8. Amended §35 (Final Verdict): Updated to reflect amended registration.
9. Added Amendment Record to registration artifact.
10. Computed amended registration SHA256: `eb41bfcd22cb7c7bfd439884d9e2e9cffa2dbb25ba4cb48257b6cf6c5e0102b6`

**Amended frozen parameters:**
- D = 10 M1 bars (UNCHANGED)
- Impulse: noise < 0.30 (UNCHANGED)
- Grinding: noise ≥ 0.50 (UNCHANGED)
- Session: US regular 09:30–16:00 ET (UNCHANGED)
- Consecutive sessions required (UNCHANGED)
- Entry: open of first M1 bar in Session B (UNCHANGED)
- Exit: close of last M1 bar in Session B (UNCHANGED)
- Cost: 2 bps round-trip (UNCHANGED)
- Minimum sample: 100/100/200/50 (CLARIFIED — 200 derived from 100+100)
- **Economic gate: Δ net return > 0 vs. unconditional directional counterfactual (AMENDED)**
- H₁/H₂: Both required for full promotion; partial support does not constitute full MECH-N03 promotion (DEFINED)

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE, **BASE-002 registered (AMENDED)** (MECH-N03)

**Artifact:** `output/research_discovery/QUANTFORGE_MECH_N03_V38A_BASE_REGISTRATION_V1.md`
**Original registration SHA256:** `5aa978d007ada2de4d7f15667d9c2c699c6fc173b7854c985b37f3a3d7a0e877`
**Amended registration SHA256:** `eb41bfcd22cb7c7bfd439884d9e2e9cffa2dbb25ba4cb48257b6cf6c5e0102b6`

**Next governed step:** FINAL BASE-002 REGISTRATION FREEZE AUDIT (confirms amended registration is internally consistent and execution-ready). Registration does NOT authorize Stage 2 or Stage 3 execution.

---

## 86. BASE-002 FINAL REGISTRATION FREEZE AUDIT (2026-09-08)

**Status:** FINAL FREEZE PASS — BASE-002 REGISTERED / AMENDED / FROZEN — STAGE 2 AUTHORIZATION ELIGIBLE

**Purpose:** Final independent freeze audit of amended BASE-002 registration following economic gate reconciliation (§85).

**Audit result:** ALL 15 freeze criteria PASS.

**Key findings:**

1. **Economic gate:** Internally consistent. §14 defines Δ net return > 0 vs. counterfactual. §16 uses identical counterfactual. Same opportunity universe, identical cost treatment. Absolute profitability retained as secondary, non-decisional statistic. Prior blocker (§14/§16 mismatch) FULLY RESOLVED.
2. **Counterfactual:** Explicit and executable. Unconditional directional exposure: enter at Session B open in Session A trend direction, exit at Session B close, regardless of path quality. Identical cost (2 bps) and opportunity universe for candidate and comparator.
3. **Minimum sample:** Unambiguous. 100 = impulse minimum, 100 = grinding minimum, 200 = derived (100+100), 50+50 = forward minimum. No hidden sample requirements.
4. **H₁/H₂ adjudication:** Deterministic. SUPPORTED (both succeed), PARTIALLY SUPPORTED (one succeeds, one fails — NOT promotable), CONTRADICTED (both fail), INCONCLUSIVE (insufficient evidence). Component rescue explicitly prohibited.
5. **Core MECH-N03:** Unchanged. D=10, thresholds 0.30/0.50, session US regular 09:30–16:00 ET, entry Session B open, exit Session B close, cost 2 bps.
6. **Hidden degrees of freedom:** NONE. All 18 material decisions frozen and classified.
7. **Registration drift:** ZERO unauthorized changes. Only §13, §14, §15, §16, §29, §35 amended per authorized reconciliation.
8. **SHA256 verified:** `eb41bfcd22cb7c7bfd439884d9e2e9cffa2dbb25ba4cb48257b6cf6c5e0102b6`
9. **Stage 2 execution:** NOT PERFORMED. No source, test, config, data, or runtime changes.

**Minor documentation carry-forward:** §17 (Cross-Era / Robustness) confirmatory table still references "mean net return > 0" instead of "Δ net return > 0 vs. counterfactual". This is a documentation inconsistency, not a material governance defect — §14 is the authoritative primary economic gate. Carry forward to Stage 3 planning.

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE, **BASE-002 registered (AMENDED / FROZEN)** (MECH-N03)

**Artifact:** `output/research_discovery/QUANTFORGE_MECH_N03_V38A_BASE_REGISTRATION_V1.md`
**Amended registration SHA256:** `eb41bfcd22cb7c7bfd439884d9e2e9cffa2dbb25ba4cb48257b6cf6c5e0102b6`

**Next governed step:** BASE-002 Stage 2 Structural Validation Authorization Review (requires separate governed task). Registration does NOT authorize Stage 2 or Stage 3 execution.

---

## 87. BASE-002 STAGE 2 STRUCTURAL VALIDATION AUTHORIZATION (2026-09-08)

**Status:** STAGE 2 AUTHORIZED — BASE-002 READY FOR STRUCTURAL VALIDATION EXECUTION

**Authorization checks — ALL PASS:**

1. **Freeze status:** Final Registration Freeze Audit = FINAL FREEZE PASS. BASE-002 remains frozen. Registration artifact SHA256 verified.
2. **No intervening drift:** No source, test, config, data, runtime, or registration changes since final freeze audit.
3. **Stage 2 boundary:** Structural Validation only. No parameter modification, optimization, or variant creation permitted.
4. **Frozen protocol:** Stage 2 will execute exactly the registered BASE-002 specification. No rescue rules, threshold mining, session mining, holding-period mining, post-hoc exclusions, opportunity selection, closed-line reopening, or mechanism modification.
5. **Authorization boundary:** Frozen registration is AUTHORIZED FOR STAGE 2 EXECUTION.

**Governed states confirmed:**
- RF-001: UNCHANGED — Stage 3 blocked, accrual continues
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-001 CLOSED / NOT BASE-ELIGIBLE, **BASE-002 STAGE 2 AUTHORIZED** (MECH-N03)

**Next permitted task:** Execute BASE-002 V38A Stage 2 Structural Validation.

**Explicit prohibition:** Do NOT modify the frozen BASE-002 registration during Stage 2 execution. No parameter changes, no threshold changes, no session changes, no cost changes, no mechanism changes.

---

## 88. BASE-002 V38A STAGE 2 STRUCTURAL VALIDATION (2026-09-08)

**Status:** STAGE 2 COMPLETE — STRUCTURAL EVIDENCE INCONCLUSIVE

**Execution result:**

| Component | N | Delta mean (bps) | 95% CI | Result |
|-----------|---|------------------|--------|--------|
| H₁ (impulse follow) | 125 | 0.0000 | [0.0000, 0.0000] | NOT SUPPORTED |
| H₂ (grinding fade) | 155 | 0.1197 | [-0.1599, 0.3812] | NOT SUPPORTED |
| Combined | 280 | 0.0662 | [-0.0863, 0.2162] | FAIL |

**Sample gates:** ALL PASS (impulse 125 >= 100, grinding 155 >= 100, combined 280 >= 200).

**Adjudication:** CONTRADICTED — Neither H₁ nor H₂ confirmed at the registered significance level.

**Material structural finding:** H₁ delta is mechanically zero by construction. For impulse observations, MECH-N03 decision direction equals the unconditional counterfactual direction, producing delta = 0.0000 bps regardless of data. This is a registered-protocol structural issue, not an execution error.

**Governed states confirmed:**
- RF-001: UNCHANGED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-002 STAGE 2 COMPLETE (MECH-N03)

**Artifact:** `scripts/forward/base002_stage2_structural_validation.py`
**Report:** Stage 2 execution report produced in conversation.

**Next governed step:** BASE-002 Stage 2 Result Adjudication / Owner Governance Decision required. The structural finding (H₁ mechanically zero) requires owner adjudication before any Stage 3 consideration.

---

## 89. BASE-002 PROTOCOL DEFECT & IDENTIFIABILITY RE-EXAMINATION (2026-09-08)

**Status:** RE-EXAMINATION COMPLETE — PARTIAL DEFECT IDENTIFIED

**Purpose:** Independent forensic audit of whether the H₁ identifiability defect was a pre-existing protocol/design defect or an execution error, and whether the Stage 2 result can legitimately be adjudicated as a scientific contradiction.

**Key findings:**

1. **H₁ is structurally non-identifiable.** The impulse-follow treatment (§10: "Follow the trend direction") and the unconditional directional counterfactual (§16: "enter at Session B open in the direction of the Session A trend") are mathematically identical for every eligible observation. ΔH₁ ≡ 0 by construction. This is a mathematical identity, not an empirical finding.
2. **Pre-existing defect.** The identity was derivable from the frozen registration alone (§10 + §16) before any Stage 2 execution. This is a pre-existing protocol/design defect, not a post-execution discovery.
3. **H₂ is independently identifiable.** The grinding-fade treatment direction (-trend_direction) differs from the counterfactual direction (+trend_direction). The +0.1197 bps observed result is a genuine empirical comparison. CI crosses zero → NOT SUPPORTED.
4. **Combined gate is structurally dilated.** The combined statistic (+0.0662 bps) equals (155/280) × 0.1197 — a diluted H₂, not a test of the combined mechanism. It cannot legitimately serve as evidence for or against MECH-N03.
5. **Stage 2 classification partially invalid.** H₁ classified as "NOT SUPPORTED" is invalid — H₁ was not testable. The correct classification is NON-IDENTIFIABLE. The §15 framework does not define this state (governance gap).
6. **No amendment authorized.** Any future correction would constitute a prospective protocol amendment with post-result rescue risk. Not authorized by this re-examination.

**Governed states confirmed:**
- RF-001: UNCHANGED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: BASE-002 STAGE 2 COMPLETE — RE-EXAMINED (MECH-N03)

**Artifact:** Protocol Defect & Identifiability Re-Examination report produced in conversation.

---

## 90. BASE-002 POST-STAGE-2 GOVERNANCE ADJUDICATION (2026-09-08)

**Status:** ADJUDICATION COMPLETE — CLOSE AS NON-ADJUDICABLE

**Disposition:** `CLOSE AS NON-ADJUDICABLE`

**Rationale:**

1. H₁ is structurally non-identifiable — the registered comparison was incapable of testing the impulse-follow hypothesis. ΔH₁ ≡ 0 by construction.
2. H₂ is validly testable but does not demonstrate positive incremental evidence (CI crosses zero).
3. The combined gate is structurally dilated and not scientifically interpretable.
4. The §15 adjudication framework does not cover non-identifiable comparisons (governance gap).
5. Closing as CONTRADICTED would conflate a protocol defect with a scientific finding.
6. The only scientifically defensible closure is NON-ADJUDICABLE.

**Knowledge accounting:**

| Category | Finding |
|----------|---------|
| Established | H₂ does not demonstrate positive incremental value (valid test, CI crosses zero) |
| Established | The registered H₁ counterfactual is degenerate (mathematical identity) |
| Established | The combined gate cannot test MECH-N03 as a whole (structural dilution) |
| Not established | Whether impulse trends continue (H₁ was not testable) |
| Not established | Whether MECH-N03 adds incremental economic value (combined gate invalid) |
| Negative knowledge | H₁ identifiability requires a counterfactual directionally distinct from the treatment |
| Negative knowledge | The combined gate is invalid when one component is degenerate |
| Negative knowledge | The §15 framework does not cover non-identifiable comparisons (governance gap) |

**H₁:** Classified as NON-IDENTIFIABLE. The 0.0000 bps result is a mathematical identity, not an empirical contradiction.

**H₂:** Classified as NOT SUPPORTED (valid empirical result). Preserved as genuine negative evidence.

**Combined:** Classified as NOT SCIENTIFICALLY INTERPRETABLE. Preserved as a structural artifact.

**Future correction:** May be legitimate in principle if it preserves the original scientific question (do clean trends continue?) using a counterfactual directionally distinct from the impulse-follow treatment. Would constitute NEW RESEARCH, not an amendment. Not authorized by this adjudication.

**Governed states confirmed:**
- RF-001: UNCHANGED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: **BASE-001 CLOSED / NOT BASE-ELIGIBLE, BASE-002 CLOSED AS NON-ADJUDICABLE** (MECH-N03)

**Next permitted task:** No further BASE-002 work. Preserve negative knowledge. Future MECH-N03 research, if any, requires a new governed formulation/registration task — NOT AUTHORIZED.

**Forbidden actions:**
- No amendment to BASE-002
- No rerun of Stage 2
- No replacement counterfactual
- No threshold/D/session/entry/exit changes
- No optimization, parameter mining, or rescue
- No closed-line reopening
- No silent displacement of active research lines (RF-001, FB-001, F-01, CAND-015/024/035)

## 91. R1/R2 STAGE 2 EXECUTION — FROZEN PROTOCOL (2026-09-09)

**Status:** EXECUTION COMPLETE — BOTH HYPOTHESES NOT SUPPORTED

**Disposition:** `R1 NOT SUPPORTED`, `R2 NOT SUPPORTED`

### Protocol Summary

**R1 — HTF Structural Context → LTF Breakout:**
- HTF = D1, 20-day rolling high/low
- ATR = EMA-based ATR(14), alpha=1/14
- Proximity = 0.5 × ATR(14)
- Entry = Open of bar E+1
- Exit = 16:00 ET
- Session = US regular (09:30–16:00 ET)
- Cost = 2 bps round-trip

**R2 — HTF Structural Event → LTF Confirmation:**
- HTF = D1, 20-day rolling high/low
- K = 5 consecutive M1 closes beyond same level
- Entry = Open of bar after 5th confirmation
- Exit = 16:00 ET
- Late-session = exclude if < K+2 = 7 bars remain
- Session = US regular (09:30–16:00 ET)
- Cost = 2 bps round-trip

### Execution Results

| Metric | R1 | R2 |
|--------|----|----|
| Eligible observations (N) | 1,662 | 35,586 |
| Treatment mean (net) | -9.92 bps | 1.71 bps |
| Counterfactual mean | 1.18 bps | 1.18 bps |
| Incremental Δ | -11.10 bps | 0.54 bps |
| 95% CI | [-18.58, -3.81] bps | [-6.18, 7.43] bps |
| CI excludes zero | YES (negative) | NO |
| Economic gate | FAIL | FAIL |
| Disposition | NOT SUPPORTED | NOT SUPPORTED |

### R1 Interpretation

R1 breakouts near daily structural levels produced significantly worse returns than unconditional session returns. The treatment mean was -9.92 bps versus a counterfactual of 1.18 bps, yielding a negative incremental Δ of -11.10 bps. The 95% bootstrap CI was [-18.58, -3.81] bps, entirely below zero. The registered economic gate (Δ > 0 AND CI excludes zero) was NOT satisfied.

**Scientific interpretation:** Breakouts near daily structural levels do not carry positive incremental information relative to unconditional session returns. The proximity condition may capture noise or mean-reversion dynamics rather than persistence.

### R2 Interpretation

R2 confirmed events (daily close beyond 20-day level + 5 consecutive M1 closes) produced returns of 1.71 bps versus a counterfactual of 1.18 bps, yielding a small positive Δ of 0.54 bps. However, the 95% bootstrap CI was [-6.18, 7.43] bps, which includes zero. The registered economic gate was NOT satisfied.

**Scientific interpretation:** The combination of HTF event and LTF confirmation does not demonstrate statistically significant incremental value over unconditional session returns. The evidence is inconclusive — the point estimate is positive but not statistically distinguishable from zero.

### Execution Integrity

- No protocol modification occurred during execution
- Frozen parameters were used exactly as registered
- Counterfactuals were distinguishable from treatment (no BASE-002 defect)
- Bootstrap methodology was preregistered (10,000 resamples, seed=42)
- Data: 906,815 M1 bars (2023-09-01 to 2026-07-10), USATECHIDXUSD

### Governed States Confirmed

- RF-001: UNCHANGED — remains sole strategic priority
- FB-001: UNCHANGED
- F-01: UNCHANGED
- CAND-015/024/035: UNCHANGED
- Base Registry: BASE-001 CLOSED, BASE-002 CLOSED AS NON-ADJUDICABLE

### Knowledge Accounting

| Category | Finding |
|----------|---------|
| Established | R1 breakouts near daily levels produce significantly negative incremental returns |
| Established | R2 confirmed events produce small positive but statistically insignificant incremental returns |
| Negative knowledge | Daily structural proximity does not carry positive breakout persistence information |
| Negative knowledge | HTF event + LTF confirmation (K=5) does not demonstrate incremental value |

### Next Permitted Task

No further R1/R2 work. Preserve negative knowledge. Future research on HTF→LTF relational mechanisms requires a new governed formulation/registration task — NOT AUTHORIZED.

**Forbidden actions:**
- No amendment to R1 or R2
- No rerun of Stage 2
- No parameter modification (K, proximity, ATR, session, entry, exit)
- No rescue, optimization, or parameter mining
- No closed-line reopening
- No new discovery cycle

---

## 92. SESSION CLOSURE CHECKPOINT (2026-09-13)

**Status:** SESSION UPDATE / HANDOFF ONLY — NO NEW RESEARCH AUTHORIZED

### A. R1 Closure (Confirmed)

```
R1 = CLOSED / NOT SUPPORTED
N = 1,662
Δ = -11.10 bps
95% CI = [-18.58, -3.81] bps
```

R1 and R2 were independently adjudicated. Neither rescued the other. Both are closed. No follow-up variant was authorized. Evidence recorded at §91.

### B. R2 Closure (Confirmed)

```
R2 = CLOSED / NOT SUPPORTED
N = 35,586
Δ = +0.54 bps
95% CI = [-6.18, +7.43] bps
```

Point estimate positive but statistically inconclusive. Economic gate failed. Evidence recorded at §91.

### C. FCR Reconnaissance (Recorded)

The externally supplied First Candle Rule (FCR) strategy was subjected to a single raw historical reconnaissance run. This was NON-GOVERNED / NON-REGISTERED / NON-AUTHORIZED.

```
Market: USATECHIDXUSD
Data: M1 (906,815 bars, 2023-09-01 to 2026-07-10)
M5 derived: 181,104 bars
Session days: 687

Funnel:
  Breakouts (momentum >= 0.6): 74,062
  + FVG within 3 bars:         435 (0.59%)
  + FVG retest:                 34 (7.8%)
  + Engulfing:                   1 (2.9%)

Trades: 1 (short, 2026-07-03)
Wins: 0
Net: -8.81 bps
```

**Primary observation:** The executed interpretation produced an extremely sparse strategy funnel, with the principal bottleneck at the breakout-to-FVG stage (0.59%).

**Scientific limitation:** This result does NOT establish that the underlying FCR concept is contradicted. The source description contains material ambiguities and the implementation necessarily selected deterministic interpretations for those ambiguities. The assumption ledger documents all 13 ambiguity items.

**Classification:** CLEARLY UNPROMISING UNDER THIS IMPLEMENTATION. Not CONTRADICTED, not ECONOMICALLY NON-VIABLE, not SCIENTIFICALLY DISPROVEN.

### D. FCR Current Disposition

```
FCR = DEFERRED / NOT FORMALLY AUDITED
```

Reason: Raw reconnaissance clearly unpromising; source specification materially under-defined; reconnaissance insufficient for scientific adjudication; no formal FCR audit authorized; no FCR registration; no FCR candidate ID.

### E. RF-001 Protection

> **SUPERSEDED 2026-09-16:** RF-001 was subsequently CLOSED — ECONOMICALLY NOT SUPPORTED (§94, corrected final). The text below is preserved verbatim for chronology.

```
RF-001 = UNCHANGED
RF-001 remains the current strategic research priority
```

[Historical, pre-§94] FCR reconnaissance does not replace, displace, or alter RF-001 in any way. RF-001 status, accrual state, protocol, governance, and strategic priority are all preserved.

### F. Research-State Checkpoint

| Category | Lines |
|----------|-------|
| Active research | RF-001 (sole strategic priority, V38A, forward accrual) |
| Closed research | R1 (NOT SUPPORTED), R2 (NOT SUPPORTED), BASE-001 (NOT BASE-ELIGIBLE), BASE-002 (NON-ADJUDICABLE) |
| Deferred | FCR (DEFERRED / NOT FORMALLY AUDITED), RF-002, RF-003 |
| Unchanged | FB-001, F-01, CAND-015/024/035 |
| Most recent completed branch | R1/R2 relational research → both closed/not supported |
| Most recent exploratory work | FCR raw reconnaissance → clearly unpromising under one implementation |
| Next governed decision point | Fresh research-capacity / branch-selection assessment (NOT to be performed here) |

> **SUPERSEDED 2026-09-16:** the "Active research" row above predates the §94 RF-001 closure and the Phase 3 freeze. The authoritative current state is §94 (RF-001 CLOSED), §96 (Phase 2: ATR=C, Zone=E), §97 (Outcome C), and §99 (RESEARCH CAPACITY HOLD). No active research line exists as of 2026-09-16.

### G. Next-Session Restart Point

```
AUTHORITATIVE START: docs/SESSION_HANDOFF.md

MOST RECENT COMPLETED BRANCH: R1/R2 relational research → both closed/not supported (§91)

MOST RECENT EXPLORATORY WORK: FCR raw reconnaissance → clearly unpromising under one implementation (§92)

ACTIVE STRATEGIC LINE: RF-001 (V38A, forward accrual, sole priority)

NEXT GOVERNED TASK: Fresh research-capacity / branch-selection assessment
```

> **SUPERSEDED 2026-09-16:** the ACTIVE STRATEGIC LINE and NEXT GOVERNED TASK lines above predate §94 and the Phase 3 freeze. Current authoritative start point: §94 (RF-001 CLOSED) → §96–§100 (Phase 2/3 complete, OUTCOME C, RESEARCH CAPACITY HOLD, next start point in §99.5).

### H. Files for Next Session

See Section 93 (this session's file manifest) for the exact list of files to share with the next ChatGPT session.

---

## 93. NEXT-SESSION FILE MANIFEST (2026-09-13)

### REQUIRED (share with next session)

| Path | Why Needed | Contains |
|------|-----------|----------|
| `docs/SESSION_HANDOFF.md` | Authoritative project control tower | All governance state, R1/R2 results at §91, FCR record at §92, research-line status, forbidden actions |
| `docs/ARCHITECTURE.md` | Four-layer BOE architecture reference | Frozen architectural boundaries, information flow rules |
| `docs/CHATGPT_ROLE_AND_RESEARCH_CONTINUITY.md` | Permanent reasoning/role contract | ChatGPT role definition, reasoning principles |
| `output/r1_r2_stage2_results.json` | R1/R2 execution evidence | Exact N, treatment/counterfactual means, CIs, gate outcomes |
| `output/fcr_recon_results.json` | FCR reconnaissance evidence | Exact funnel, trade list, dates, P&L |

### STRONGLY RECOMMENDED (materially improves assessment)

| Path | Why Useful | Supports |
|------|-----------|----------|
| `first_candle_rule_strategy.pdf` | Source document for FCR | Any future FCR formal audit; contains the original strategy description |
| `output/research_discovery/QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md` | RF-001/002/003 formulations | Understanding relational research framework conventions |
| `output/research_discovery/QUANTFORGE_RELATIONAL_RESEARCH_FRAMEWORK_GOVERNANCE_V1.md` | Relational research governance | Understanding governance conventions for future research |
| `output/research_discovery/QUANTFORGE_V38_DOCTRINE_RATIFICATION_V1.md` | V38 Doctrine | Understanding V38A frozen parameters and constraints |
| `dna/market_dna.py` | Canonical ATR implementation | Reference for ATR convention (EMA-based, alpha=1/14) |

### OPTIONAL / REFERENCE

| Path | Purpose |
|------|---------|
| `scripts/forward/fcr_recon_v2.py` | FCR execution script (reproducibility) |
| `scripts/forward/r1r2_final.py` | R1/R2 execution script (reproducibility) |
| `scripts/forward/rf001_stage3_validation.py` | RF-001 validation reference (is_late_in_session, session conventions) |
| `data/rf001/raw/recorder_status.json` | RF-001 live accrual status |
| `data/rf001/raw/rf001_two_market_m1_raw.csv` | RF-001 prospective data (~2,802 rows) |

### DO NOT SHARE INITIALLY

| Path | Reason to Exclude |
|------|-------------------|
| `data/m1/USATECHIDXUSD_M1.csv` | 54 MB raw data; results already summarized in JSON artifacts |
| `data/m1/BTCUSD_M1.csv` | 140 MB; not relevant to current research lines |
| `data/m1/EURUSD_M1.csv` | 114 MB; not relevant to current research lines |
| `data/m1/XAGUSD_M1.csv` | 87 MB; not relevant to current research lines |
| `data/m1/XAUUSD_M1.csv` | 104 MB; not relevant to current research lines |
| `data/tick/` | Massive tick data; not needed for governance restart |
| `data/tick_canonical/` | Parquet tick archives; not needed for governance restart |
| `output/research_discovery/*.md` (other than the 3 listed) | Historical discovery documents; not needed for restart |
| `output/QUANTFORGE_GIT_*.md` | Git audit reports; operational, not research-critical |
| `scripts/forward/r1_r2_stage2_execution.py` | Superseded by r1r2_final.py |
| `scripts/forward/r1r2_exec.py` | Superseded by r1r2_final.py |
| `scripts/forward/fcr_debug.py` | Debug script, not needed |
| `scripts/forward/fcr_debug2.py` | Debug script, not needed |

### MISSING / NOT VERIFIED

| Expected Purpose | Referenced From | Why It Matters |
|------------------|----------------|----------------|
| (none) | — | All critical artifacts verified present |

---

## 94. RF-001 OWNER ECONOMIC ADJUDICATION & CLOSURE (2026-09-13)

### §94.1 Authorization

Stage 3 economic validation independently reconstructed using the frozen RF-001 V38A protocol. Two critical corrections applied:

1. **Invalidation logic corrected:** Original implementation checked wrong levels (rh30 for bearish, rl30 for bullish). Corrected: bullish invalidated when primary drops below rh30; bearish invalidated when primary rises above rl30.

2. **Duplicate suppression applied:** Frozen protocol rule — "Duplicate structural events (same direction, same session, no intervening reversal) do not create new opportunities" (Formulation §Opportunity population, line 145).

### §94.2 Corrected Eligibility Funnel

| Population Stage | Count |
|------------------|------:|
| Raw post-freeze observations | 2,841 |
| MATCHED observations | 2,841 |
| Session-eligible (09:30–16:00 ET) | 670 |
| Primary structural events (N=30 breakout) | 66 |
| Last M bars excluded (15:46–16:00 ET) | 1 |
| Duplicate suppressed (same dir, no reversal) | 55 |
| **Non-duplicate primary events** | **10** |
| Confirmed by US500 (no opportunity) | 0 |
| Invalidated (primary reverses before entry) | **10** |
| Confirmation failures (potential opportunities) | 0 |
| **Economically evaluable opportunities** | **0** |

### §94.3 Invalidation Pattern

All 10 non-duplicate events invalidated within 1–3 bars:

| Event | Direction | Invalidation Bar |
|-------|-----------|-----------------|
| Sep 7 13:30 | bullish | E+2 |
| Sep 7 14:59 | bearish | E+1 |
| Sep 7 16:03 | bullish | E+1 |
| Sep 8 13:32 | bearish | E+2 |
| Sep 8 14:50 | bullish | E+1 |
| Sep 8 16:09 | bearish | E+3 |
| Sep 8 17:01 | bullish | E+1 |
| Sep 8 17:41 | bearish | E+1 |
| Sep 9 13:30 | bullish | E+1 |
| Sep 9 14:21 | bearish | E+2 |

**Meaning:** USATECHIDXUSD structural breakouts are overwhelmingly transient — the primary market reverses within minutes, eliminating the opportunity before entry.

### §94.4 Superseded Results

**34-opportunity result = SUPERSEDED / INVALID FOR ADJUDICATION**
- Reason: Frozen duplicate structural-event suppression was not applied.
- The 34-opportunity economic result must NOT be used as evidence for RF-001's final economic verdict.

**1-opportunity result = SUPERSEDED / INVALID FOR ADJUDICATION**
- Reason: Invalidation logic was backwards (checked rh30 for bearish, rl30 for bullish instead of the reverse).
- The single LONG US500 trade at -20.97 bps is NOT a valid RF-001 output.

**Corrected result: 0 eligible opportunities.** The previous Stage 3 finding (§83, 0 opportunities with 1,302 observations on Sep 7 only) is confirmed by the corrected analysis with 2,841 observations across 3 days.

### §94.5 Owner Adjudication

**RF-001 — ECONOMICALLY NOT SUPPORTED — CLOSED**

The frozen RF-001 V38A protocol was tested as designed. With corrected invalidation logic and frozen duplicate suppression applied, the protocol produced ZERO economically evaluable opportunities across 2,841 MATCHED observations covering 3 trading days.

The mechanism is not economically supported because:
1. Confirmation failures do not survive the invalidation check — the primary market reverses before entry in every case.
2. No economically evaluable opportunities exist from which to compute returns.
3. N=0 (zero evaluable trades) provides no statistical power.

### §94.6 Falsification Route

The registered falsification route states: "If confirmation failures are random — i.e., the non-confirming market's subsequent session performance is statistically identical regardless of whether confirmation occurred — the mechanism is falsified."

With 0 eligible opportunities, this route cannot be fully tested. However, the structural finding — that USATECHIDXUSD breakouts universally reverse before entry — is itself evidence that the mechanism does not produce actionable opportunities under its registered protocol.

### §94.7 Lifecycle Consequence

RF-001 moves to **CLOSED**. This frozen RF-001 experiment is economically not supported under its registered protocol. It does NOT mean the broad market hypothesis has been universally disproven — only that this specific protocol does not produce evaluable opportunities.

### §94.8 No-Rescue Boundary

The following are PROHIBITED:
- Removing or weakening duplicate suppression
- Changing confirmation logic
- Changing N, M, session, entry timing, exit timing, direction, or cost
- Creating LONG-only or SHORT-only variants
- Backfilling or data manufacture
- Reopening RF-001
- Searching for a more favorable implementation

Any such changes constitute a NEW research question and require governed discovery.

### §94.9 Research-State Update

| Research Line | Status |
|---------------|--------|
| RF-001 | **CLOSED** — ECONOMICALLY NOT SUPPORTED |
| R1 | CLOSED — NOT SUPPORTED (§91) |
| R2 | CLOSED — NOT SUPPORTED (§91) |
| BASE-001 | CLOSED — NOT BASE-ELIGIBLE (§74) |
| BASE-002 | CLOSED — NON-ADJUDICABLE (§90) |
| FCR | DEFERRED — NOT FORMALLY AUDITED (§92) |
| RF-002 | DEFERRED |
| RF-003 | DEFERRED |
| ATR Breakout | FUTURE TODO — not authorized |
| Zone Recovery | FUTURE TODO — not authorized |

### §94.10 Next Governed Decision Point

RF-001 CLOSED. NO AUTOMATIC NEW BRANCH AUTHORIZED.

The next research decision must be made separately under QuantForge governance.

---

## 95. NEXT-SESSION FILE MANIFEST (UPDATE — 2026-09-13)

### REQUIRED (share with next session)

| Path | Why Needed | Contains |
|------|-----------|----------|
| `docs/SESSION_HANDOFF.md` | Authoritative project control tower | All governance state including §94 RF-001 closure |
| `docs/ARCHITECTURE.md` | Four-layer BOE architecture reference | Frozen architectural boundaries |
| `docs/CHATGPT_ROLE_AND_RESEARCH_CONTINUITY.md` | Permanent reasoning/role contract | ChatGPT role definition, reasoning principles |

### STRONGLY RECOMMENDED

| Path | Why Useful |
|------|-----------|
| `output/research_discovery/QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md` | RF-001/002/003 formulations |
| `output/research_discovery/QUANTFORGE_RELATIONAL_RESEARCH_FRAMEWORK_GOVERNANCE_V1.md` | Relational research governance |

### RF-001 CLOSURE ARTIFACTS

| Path | Content |
|------|---------|
| `data/rf001/raw/rf001_two_market_m1_raw.csv` | RF-001 prospective data (2,841 MATCHED rows) |
| `data/rf001/raw/recorder_status.json` | RF-001 recorder status |
| `output/research_discovery/QUANTFORGE_RF001_V38A_STAGE3_ECONOMIC_VALIDATION_V1.md` | Previous Stage 3 validation (superseded by §94) |

---

## 96. PHASE 2 — INDEPENDENT MECHANISM & PRIOR-ART AUDIT: ATR BREAKOUT / ZONE RECOVERY (2026-09-16)

**Status:** COMPLETE — READ-ONLY MECHANISM AUDIT — NEITHER DIRECTION SURVIVED AS A NEW RESEARCH BRANCH

**Mission context:** Following the Phase 1 authoritative-state recovery and the §94 RF-001 closure, the owner requested an independent mechanism/distinctness audit of two named future directions before any branch-selection decision. No repository state was modified.

### §96.1 ATR Breakout

**Classification: C — SAME MECHANISM / VARIATION.**

- Residual market mechanism after stripping ATR stop/target/sizing/session/friction: `breakout → directional continuation`.
- Materially overlaps existing QuantForge breakout/trend/momentum families, including closed work: DISC-022 (TSMOM — closed/not promotable), BASE-001 / MECH-N01 (structural level validation → follow — closed/not Base-eligible), R1 (HTF structural context → LTF breakout — closed/not supported), R2 (HTF structural event → LTF confirmation — closed/not supported), and the project's standing breakout/threshold-trigger dependence rejection.
- ATR stop/target, volatility-proportional sizing, session window, news/rollover/spread filters, and universe choice are implementation / risk / execution layers, not a new market mechanism.
- External prior art treats Donchian/ATR breakout as a well-established implementation family; no external evidence of a genuinely unusual mechanism was found.

**Disposition: NOT AN ACTIVE RESEARCH BRANCH.** This is not a "deferred candidate" — it failed the current distinctness/mechanism gate. Re-opening it would require a genuinely new causal claim, not new parameters.

### §96.2 Zone Recovery

**Classification: E — NOT A MARKET MECHANISM.**

- The proposal's distinctive content is recovery/basket/position-sizing architecture: initial directional trade, counter-position at the opposite zone boundary, progressive/geometric counter-position sizing, basket-level profitability condition, simultaneous basket closure, maximum recovery-cycle limit, no conventional per-position stop.
- No independently specified market hypothesis survives once the lot multiplier and basket accounting are removed.
- Direct overlap with prior QuantForge negative knowledge: DISC-015 (grid/basket mechanics introduce concentrated tail risk — 7,525 clusters, median cluster profitable but minimum −5,234.54, maximum lot 10.24 vs median 0.08), DISC-016 (extreme lot-size tails), DISC-018 (basket/grid forensics).
- Structural risk analysis: directional breakout through the recovery structure produces escalating exposure; cycle limit contains leg count but not realized loss; margin/stop-out can precede basket recovery; multi-leg cost accumulation and execution sequencing can dominate basket arithmetic.
- External prior art treats zone recovery as a popular retail hedging/recovery family (martingale-like, basket TP); vendor promotional claims are not evidence of edge.

**Disposition: NOT AN ACTIVE RESEARCH BRANCH.** It failed the mechanism gate, not merely the economics gate.

### §96.3 Governance effect

- Neither direction was activated, formulated, registered, backtested, or optimized.
- Neither may be treated as an available active branch in any subsequent session without a genuinely new mechanism claim.

---

## 97. PHASE 3 — RESEARCH-CAPACITY & BRANCH-SELECTION AUDIT (2026-09-16)

**Status:** COMPLETE — READ-ONLY GOVERNED AUDIT — OUTCOME C

**Outcome:**

```text
OUTCOME C — NO BRANCH CURRENTLY JUSTIFIED
```

**Current research state:**

```text
RESEARCH CAPACITY HOLD
```

**Basis (from the Phase 3 audit, preserving Phase 1 and Phase 2 as distinct inputs):**

1. **Phase 1 (authoritative state recovery):** the current working tree is authoritative; HEAD is stale relative to it; RF-001 corrected closure is authoritative; no active Base economic-validation line exists; the project sits at a branch-selection point.
2. **Phase 2 (mechanism archaeology):** ATR Breakout = C (same mechanism/variation); Zone Recovery = E (not a market mechanism). Neither is an available branch.
3. **Phase 3 (capacity audit):** the remaining future/deferred portfolio was audited mechanism-first against distinctness, observability, falsifiability, prior-art burden, and governance readiness. No direction satisfied the research-capital requirements.

**Key finding:** the preserved future/deferred portfolio contains no sufficiently mature, distinct, observable, falsifiable market mechanism that has earned the next active research allocation.

**Explicit non-claim:** this is NOT a statement that no future research ideas exist. The future hypothesis library remains preserved (§98). It is also NOT a claim that the entire market mechanism space is exhausted — only that no surviving candidate was identified within the specifically searched and governed future-direction set at this time.

**Next governed decision point (carried forward):** a fresh mechanism-distinctness / branch-selection decision may be initiated only when a genuinely distinct market mechanism has been identified and is sufficiently defined for the formulation gate (see §99.5).

---

## 98. PRESERVED FUTURE-DIRECTION LIBRARY — FUTURE CONCEPTS, NOT ACTIVE BRANCHES (2026-09-16)

**Standing distinction (reinforced for all future sessions):**

```text
FUTURE TODO ≠ ACTIVE RESEARCH
HYPOTHESIS ≠ CANDIDATE
METHODOLOGY ≠ MARKET MECHANISM
INFORMATION NOVELTY ≠ MECHANISM NOVELTY
```

No item below is authorized, registered, formulated, or executable. Each must pass the normal mechanism → distinctness → observability → falsifiability → formulation → registration → structural-validation → economic-validation gates if ever pursued.

| Direction | Status | Non-active constraints |
|-----------|--------|------------------------|
| Outcome-blind relational structural-library research (encode structural characteristics of completed studies; identify non-redundant structural relationships and logical/temporal orderings; potentially generate future hypotheses) | **FUTURE METHODOLOGY — NOT ACTIVE** | Historical economic performance MUST NOT be used as the selecting input. No ranking by profitability, no reverse-engineering of profitable combinations, no mining historical expectancy, no using prior winners as labels, no reconstructing closed strategies. This methodology does not itself constitute a validated market mechanism and must not bypass any gate. |
| SMC Institutional POI Validation Framework (POI models + refinement pillars) | **FUTURE CONCEPT / PATTERN-VALIDATION FRAMEWORK — NOT ACTIVE** | Currently understood as a pattern taxonomy / validation framework, not an established QuantForge market mechanism. No individual POI model is promoted. Converting any POI concept into research would require a specific outcome-blind falsifiable market hypothesis with counterfactual. |
| Liquidity-Pool Movement Hypothesis (markets may move toward identifiable liquidity locations/pools) | **UNVALIDATED FUTURE HYPOTHESIS — NOT ACTIVE** | Requires precise ex-ante definition of "liquidity pool." Versions depending on actual order-book depth, resting liquidity, or aggressor flow are observability-blocked under current data (no true volume, no aggressor side, no depth). Must not collapse into ordinary level/attraction behavior already explored. |
| Dynamic Regime / ADX Transition (static M15 regime labels may miss intraday state change; ADX percentile drift/transition as candidate observable) | **UNVALIDATED FUTURE HYPOTHESIS — NOT ACTIVE** | ADX is an observable/proxy, not an established mechanism. The ±15 ADX-percentile-per-H4-bar observation is an untested example — it is NOT a frozen parameter and must not be backtested or promoted. Risks becoming a regime filter for existing families rather than an independent hypothesis. |
| Quote-Level Microstructure (bid/ask independence, spread dynamics, quote churn domains) | **INFORMATION-NOVEL ONLY — MECHANISM NOVELTY UNESTABLISHED** | §80–§82 established: T01/T02/T03 not owner-selection eligible; Q01–Q06 fresh cycle produced ZERO mechanism survivors. Quote-level information availability ≠ mechanism novelty. Two discovery cycles produced no distinct market-generating mechanism. |
| Prospective tick capture (new recorder via MT5 `copy_ticks_from()`) | **INFRASTRUCTURE OPPORTUNITY — NOT AUTHORIZED** | Would require separate authorization; does not by itself create a mechanism. |
| ORD / DISC-026 follow-on economics | **CLOSED — NOT REOPENED** | Scientific support stands; registered XAGUSD economic translation closed/non-viable; no revival authorized. |
| F-01 / FB-001 | **UNCHANGED / PROSPECTIVE ONLY** | F-01: registration frozen, NOT economically validated, not an active economic research line. FB-001: prospective accrual only, not active Base economic validation. |

---

## 99. NEGATIVE-KNOWLEDGE FIREWALL & RESEARCH-CAPACITY HOLD (2026-09-16)

### §99.1 Protected closed/rejected families

The following families must not be re-researched via superficial renaming, timeframe change, indicator change, market change, session change, threshold change, stop/target change, sizing change, or execution change. Any genuinely new entry requires a new causal claim that survives the mechanism-distinctness gate from the frozen negative-knowledge state:

- **Mean reversion** (DISC-021 — economically non-viable under observed costs);
- **Fixed TSMOM / 12-1 trend continuation** (DISC-022 — not promotable; contemporary contradicted);
- **Session range expansion** (DISC-024 — contradicted, wrong direction);
- **Liquidity sweep/reversal minimal translation** (DISC-025 — economically non-viable, gross-negative);
- **Structural breakout/follow** (BASE-001 / MECH-N01 — not Base-eligible);
- **Session-sequential trend quality** (BASE-002 / MECH-N03 — non-adjudicable; H₁ non-identifiable defect stands);
- **HTF→LTF relational structures** (R1/R2 — not supported);
- **Grid/basket/recovery architectures** (DISC-015/016/018 tail-risk knowledge; Phase 2 Zone Recovery = E);
- **ATR breakout as presently defined** (Phase 2 = C — same mechanism/variation);
- **Zone Recovery as presently defined** (Phase 2 = E — not a market mechanism);
- **Prior quote-level Q01–Q06 mechanism-search space** (zero mechanism survivors across two cycles);
- **RF-001 cross-market confirmation-failure protocol as registered** (§94 — economically not supported; no-rescue boundary in §94.8 stands).

### §99.2 Control-tower statement

```text
Current Research Capacity State:
HOLD

No active research branch is authorized at this point.

The portfolio has reached a governed research-capacity hold because
the currently preserved future directions have not established a
sufficiently distinct, observable, falsifiable market mechanism that
justifies consuming the next research allocation.

This is not a claim that no future mechanisms exist.

Future hypotheses and methodologies remain preserved (§98).

No future hypothesis, TODO, methodology, implementation concept, or
research observation constitutes authorization for active research.
```

### §99.3 Governance rules in force (retained, unchanged)

- Single-active-line rule.
- Separate formulation / registration / structural-validation / economic-validation gates.
- No unauthorized code/config/test/data changes.
- No rescue of closed research; no parameter/threshold/session mining; no event manufacture; no hindsight optimization.
- No historical economic selection for outcome-blind relational research.
- FUTURE TODO ≠ authorization; HYPOTHESIS ≠ candidate; METHODOLOGY ≠ market mechanism; INFORMATION NOVELTY ≠ mechanism novelty.
- Independent audit before owner adjudication where required.
- `docs/SESSION_HANDOFF.md` is the authoritative control-tower document.

### §99.4 Standing prohibitions for the hold period

No new mechanism discovery cycle, candidate formulation, candidate registration, economic validation, backtesting, parameter testing, data collection, or recorder deployment is authorized by this freeze. If a genuinely new research idea is identified, it must be recorded as an out-of-scope observation and brought to governance separately — not converted into a candidate.

### §99.5 Next start point (restart condition)

The next research session must NOT begin with "pick one of ATR Breakout, Zone Recovery, SMC POI, liquidity pools, or ADX."

```text
Next Start Point:
A future governed mechanism-distinctness / branch-selection decision
may be initiated only when a genuinely distinct market mechanism has
been identified and is sufficiently defined for the formulation gate.
```

If governance later authorizes a new mechanism-discovery exercise, it must begin from the current frozen negative-knowledge state (§99.1) and the §98 future library, treating both as non-authorization constraints.

---

## 100. PHASE 1 → PHASE 2 → PHASE 3 LINEAGE SUMMARY (2026-09-16)

```text
Phase 1:
Authoritative state recovered (working tree authoritative; HEAD stale;
RF-001 corrected closure authoritative; no active Base economic line)

Phase 2:
ATR Breakout  = C — SAME MECHANISM / VARIATION  (not a branch)
Zone Recovery = E — NOT A MARKET MECHANISM      (not a branch)

Phase 3:
OUTCOME C — NO BRANCH CURRENTLY JUSTIFIED
RESEARCH CAPACITY HOLD
```

These three stages are distinct governed events and must not be collapsed into a generic "research completed" statement.

---

## 101. P0 INFRASTRUCTURE MILESTONES — P0-LITE / P0-F1 / P0-F2 FROZEN (2026-09-20)

**Status:** COMPLETE — INFRASTRUCTURE BOOKKEEPING ONLY — RESEARCH STATE UNCHANGED

This section records governed infrastructure milestones completed under the §99 research-capacity hold. It changes no research conclusion, no governance rule, no architecture decision, and no research priority. The §99.2 hold state stands unchanged.

### §101.1 What was built (factual inventory)

- **P0-Lite — point-in-time / provenance foundation** (`research/pointintime/`, 9 modules): `PointInTimeInput`, `ProvenanceStatus` (VERIFIED / EQUIVALENT_BY_CONSTRUCTION / UNVERIFIED), `Modality`, `RevisionState`, `KnowledgeBasisRule`/`KnowledgeBasisRegistry` (PRICE_BAR_CLOSED_V1, PRICE_TICK_OBSERVED_V1, DOCUMENT_PUBLICATION_V1, MACRO_ACTUAL_RELEASE_V1, POSITIONING_PUBLICATION_V1), `RevisionPolicy`, `AdmissionReason`/`AdmissionResult`, `ADMIT_INPUTS`, leakage property checks. Knowledge time is re-derived from named evidence; retrieval time is excluded from admission; identity is content-deterministic.
- **P0-F1 — governed Parquet tick reader** (`research/staged_execution/tick_reader.py`): streaming `iter_batches`, duplicate-timestamp preservation, `source_row_ordinal` enforcement, `[start, end)` bounds, declared-timezone handling, opt-in SHA-256 integrity (fail-closed), quote-data-only semantics; minimal streaming change in `stage1.py`.
- **Maintenance:** the pre-existing `run_stage1_prepare` function-local `import json` shadowing defect (`UnboundLocalError` on the force-rebuild archival path) was repaired by deleting the one shadowing line (suite 901/1 → 902/0).
- **P0-F2 — minimal additive Dataset Foundation extension:** `PartitionName.PARTITIONED` + additive `partition_key` (keyed monthly partitions), additive `schema_id` with a closed registry (`research/dataset/schemas.py`), `ParquetPartitionReader` as a thin adapter over the frozen P0-F1 reader (`research/dataset/parquet_reader.py`), `DatasetManifest.fingerprint` semantics untouched.

### §101.2 Independent audit lineage

- **P0-Lite + P0-F1 freeze audit: PASS WITH MINOR FINDINGS — FREEZE MAY PROCEED** (adversarial reconstruction from code: boundary, scale, retrieval-time isolation, revision policy, hash opt-in, scope all verified).
- **P0-F2 first freeze audit: BLOCKED** — B-1 (partition read scope = directory+window, not the declared `source_uri` file) + M-1 (schema registry lacked the canonical 9-column substrate fields `mid`/`spread`). Both reproduced at runtime.
- **Remediation (scoped to B-1 + M-1 only):** partition-file isolation enforced inside F2 via exact `TickObservation.partition` provenance comparison — fail-closed, non-filtering, invariant under `verify_hashes=False/True`, without modifying F1; `mid`/`spread` added as raw optional quote fields; P0 artifacts 18/18 byte-identical through the remediation.
- **P0-F2 re-audit: PASS WITH MINOR FINDINGS — P0-F2 MAY PROCEED TO FREEZE.** B-1 verified provenance-exact, fail-closed, partial-stream-safe (sibling, undeclared, and late-stream contamination all fail closed under both hash modes; clean directories unaffected). M-1 verified against the real canonical substrate at metadata level (construction succeeds; schema closure retained; undeclared fields such as `trade_size` still rejected). Fingerprint preservation re-proven from actual values against an independent 4 KiB-chunk reference. BOE boundary: zero `boe → research` imports.

### §101.3 Verification state at freeze

```text
Full suite:                936 passed / 0 failures  (Python 3.11.9, verified 2026-09-20)
P0-Lite frozen:            YES (independent audit passed)
P0-F1 frozen:              YES (independent audit passed)
P0-F2 frozen:              YES (remediation independently verified; re-audit PASS WITH MINOR FINDINGS)
P0/F1 frozen artifacts:    18/18 byte-identical
Fingerprint semantics:     PRESERVED (actual-value proof, legacy == independent reference)
BOE boundary:              PRESERVED (0 boe→research imports; boe/ diff empty)
Dataset Foundation:        additive only; existing CSV path and canonical fingerprint untouched
Retained minors:           (1) mutable module-level schema registries; (2) raw IsADirectoryError
                           for directory-valued source_uri — non-blocking, not scheduled
Dataset/migration impact:  NONE — no dataset rewritten, no manifest rewritten, no fingerprints
                           regenerated, no verdicts or strategy packages regenerated
```

### §101.4 Governance effect

```text
RESEARCH CAPACITY HOLD:      UNCHANGED (§99.2)
NO ACTIVE RESEARCH BRANCH:   UNCHANGED
NO CANDIDATE ACTIVATED:      UNCHANGED
CLOSED LINES (§99.1):        NOT REOPENED
§98 FUTURE LIBRARY:          UNCHANGED — no item promoted or demoted
BOE:                         UNCHANGED
```

P0 is an infrastructure milestone only. Capability existence does not constitute research authorization; the §98/§99 constraints apply to any future use of the new infrastructure. The §99.5 restart condition stands: a governed branch-selection decision requires a genuinely distinct, sufficiently defined mechanism first.

---

## 102. EXTERNAL INFORMATION MVC PHASE I — FROZEN (2026-09-21)

**Status:** COMPLETE — INFRASTRUCTURE FREEZE — RESEARCH STATE UNCHANGED

This section records the formal freeze of External Information MVC Phase I (pure domain contracts) following its independent remediation re-audit (final result: PASS — PHASE I MAY PROCEED TO FREEZE). It is factual bookkeeping only. It changes no research conclusion, no governance rule, no architecture decision, and no research priority. The §99 research-capacity hold stands unchanged.

### §102.1 Scope (factual inventory)

Phase I implemented exactly five domain-contract modules plus their contract tests (tests/test_external_information_phase1.py):

- `research/external_information/__init__.py` — package exports; zero logic.
- `research/external_information/source_registry.py` — `SourceIdentity` + `SourceRegistry`: immutable source identities, closed source classes (RESEARCH / MACRO / POSITIONING), versioned registry snapshots, duplicate registration fails.
- `research/external_information/artifact_reference.py` — `ArtifactReference` + byte-verification primitive: SHA-256 content identity via the frozen `research/staged_execution/_identity.py` implementation; reference contract only.
- `research/external_information/evidence.py` — `EvidenceKind` (closed four-kind vocabulary) + `PublicationEvidence`: modality-specific publication-forensics evidence.
- `research/external_information/instrument_mapping.py` — `InstrumentMapping` + versioned per-source mapping tables with the explicit `UNRESOLVED` state.

Explicitly NOT part of Phase I (verified absent at freeze): no Phase II record construction; no `PointInTimeInput` construction; no `ADMIT_INPUTS` integration; no external-data acquisition; no artifact storage implementation; no network/API/scraper code; no grouping (Phase III); no BOE integration.

### §102.2 Independent verification lineage

Phase I implementation → independent freeze audit (PASS WITH MINOR FINDINGS: N-1 extras keyspace, N-2 nested `awareness_proxy`, N-3 record-level reserved keys) → targeted remediation of N-1/N-2/N-3 (suite 993 → 1022) → independent remediation re-audit (BLOCKED — M-9: `extras` stored by reference; a retained caller mapping could forge the governed basis value and inject prohibited keys after construction) → M-9 targeted remediation (owned deep-frozen `extras` snapshot; recursive sequence traversal; serialization precedence; suite 1022 → 1034) → independent M-9 freeze re-audit V2: **PASS — PHASE I MAY PROCEED TO FREEZE** (no blocker, no major finding). The prior O-10 sequence-traversal observation was closed by the M-9 remediation (runtime-verified prohibition across mapping/list/tuple/mixed container shapes).

### §102.3 Verification state at freeze

```text
Full suite:                 1034 passed / 0 failures  (Python 3.11.9, verified 2026-09-21)
Phase-I targeted suite:     98 passed / 0 failures
Deprecation-warning runs:   clean (-W error::DeprecationWarning, two consecutive runs)
P0-Lite:                    unchanged / frozen (anchor hashes re-verified)
P0-F1:                      unchanged / frozen
P0-F2:                      unchanged / frozen
BOE:                        unchanged (boe/ diff empty)
EnvironmentSnapshot:        unchanged (hash 1666bac504ddd2a1)
boe → research imports:     0
Dataset Foundation:         untouched; no dataset or fingerprint change
```

### §102.4 Contract-specific freeze facts

- **Source identity:** immutable identities; closed source classes; versioned registry snapshots; historical versions remain representable; no source-quality, reliability, predictive, sentiment, or importance semantics.
- **Artifact reference:** SHA-256 content identity (64-character lowercase hex, single frozen hashing implementation); immutable reference contract; integrity primitive performs no I/O; no storage implementation.
- **Evidence:** live reuse of the frozen P0 knowledge-basis registry (no duplicated basis constants; DOCUMENT / POSITIONING → `publication_timestamp`, MACRO_RELEASE → `actual_release_timestamp`, verified against the live registry); fail-closed reserved-key protection ordered governed-shadow guard → specific prohibited-key guard → namespace validation → ownership freeze; namespaced extras (`evidence_` / `access_` / `x_`); recursive prohibited-key protection including mappings inside sequences; alias-free deep-frozen `extras` snapshot (caller mutation cannot alter governed evidence or inject prohibited keys); governed fields applied after extras in serialization (governed basis value appears exactly once); `collection_latency` derived-only; no `awareness_proxy` semantic field anywhere.
- **Instrument mapping:** immutable, versioned, per-source mappings; explicit `UNRESOLVED`; duplicate source-native mapping detection; no universal instrument ontology.

### §102.5 Retained non-blocking observations (not remediated, not elevated)

```text
BLOCKER:  none
MAJOR:    none

O-4  registry version is an explicit label
O-5  registered_at is optional
O-6  M007 accepted
O-7  literal "UNRESOLVED" ambiguity
O-8  negative collection latency
O-12 transient non-reproducible warning artifact
O-13 naive datetime permitted as ordinary extras payload
O-14 nested collection_latency may exist as ordinary auxiliary payload
O-15 access fields remain observational free text
```

These observations remain open, non-blocking, and are not scheduled; they do not affect the frozen contract guarantees above.

### §102.6 Governance effect

This freeze is an infrastructure milestone only.

It does not:

- activate research;
- create a candidate;
- authorize external-data acquisition;
- authorize Phase II;
- modify the research-capacity hold;
- reopen any closed research line;
- modify BOE governance;
- modify architecture governance.

The authoritative project state remains RESEARCH CAPACITY HOLD (§99). Capability existence does not constitute research authorization; the §98/§99 constraints apply to any future use of the External Information MVC infrastructure.

### §102.7 Phase II / Phase III firewall

```text
Phase II:      NOT STARTED
Phase III:     NOT STARTED

No implementation authorization is granted by this freeze record.
```

---

## 103. EXTERNAL INFORMATION MVC PHASE II — FROZEN (2026-09-21)

**Status:** COMPLETE — INFRASTRUCTURE FREEZE — RESEARCH STATE UNCHANGED

This section records the formal freeze of External Information MVC Phase II (record construction) following its independent B-1 remediation re-audit (final result: PASS WITH MINOR FINDINGS — PHASE II MAY PROCEED TO FREEZE). It is factual bookkeeping only. It changes no research conclusion, no governance rule, no architecture decision, and no research priority. The §99 research-capacity hold stands unchanged.

### §103.1 Scope (factual inventory)

Phase II implemented exactly one new module plus its contract tests (tests/test_external_information_phase2.py):

- `research/external_information/record.py` — `ExternalInformationRecord` + `ExternalInformationRecordError`: the minimal immutable provenance wrapper containing exactly five fields — `input` (frozen P0 `PointInTimeInput`), `artifact` (frozen Phase-I `ArtifactReference`), `source_identity` (frozen Phase-I `SourceIdentity`), `mapping_version`, `source_native_id`.

Explicitly NOT part of Phase II (verified absent at freeze): no external-data acquisition; no artifact storage; no network/API/scraper code; no grouping; no BOE integration; no Phase III implementation; no second modality/basis/revision taxonomy; no second record-identity algorithm.

Phase II constructs frozen `PointInTimeInput` objects from validated Phase-I domain objects; `ADMIT_INPUTS` remains deferred to the future consumer (Design A — construction is separate from decision-boundary admission).

### §103.2 Independent verification lineage

Phase II implementation (suite 1034 → 1077) → independent freeze audit V1 (BLOCKED — B-1: direct dataclass construction bypassed record-level provenance invariants: snapshot laundering, source-class/modality falsification, source-identity mismatch, arbitrary lineage metadata) → targeted `__post_init__` remediation moving all record-level invariants into the type itself (suite 1077 → 1092) → independent B-1 re-audit V2: **PASS WITH MINOR FINDINGS — PHASE II MAY PROCEED TO FREEZE** (no blocker, no major finding; the direct-construction boundary is closed and adversarially re-proven on both construction paths).

### §103.3 Verification state at freeze

```text
Full suite:                 1092 passed / 0 failures  (verified 2026-09-21)
Phase-II targeted suite:    58 passed / 0 failures
Deprecation-warning runs:   clean (-W error::DeprecationWarning, two consecutive runs)
P0-Lite:                    unchanged / frozen
P0-F1:                      unchanged / frozen
P0-F2:                      unchanged / frozen
Phase I:                    unchanged / frozen (frozen hashes re-verified)
BOE:                        unchanged (boe/ diff empty)
boe → research imports:     0
pointintime/dataset/staged_execution → external_information imports: 0
```

### §103.4 Contract guarantees (independently verified)

- The record contains only the approved five fields (pinned by test); no duplicated P0 facts; no redundant `source_registry_version` (registry lineage is carried by `source_identity.registry_version`).
- P0 construction uses explicit named arguments only; the evidence mapping is never splatted into the constructor.
- Knowledge time remains P0-derived/verified: a `knowledge_timestamp` differing from the basis-derived value fails construction; Phase II derives no timestamp of its own.
- External modality is enforced: only DOCUMENT / MACRO_RELEASE / POSITIONING; price modalities cannot be wrapped into a record.
- Snapshot references are forbidden: `input.snapshot_ref is None` on every valid record; enforced by the type on every construction path.
- Source identity must match the P0 `source_id`; re-attribution by wrapping fails closed.
- Source class/modality consistency is enforced (RESEARCH↔DOCUMENT, POSITIONING↔POSITIONING, MACRO↔MACRO_RELEASE) via the frozen Phase-I mapping.
- Basis/status consistency is enforced against the live frozen P0 knowledge-basis registry; provenance status is never caller-assertable.
- Evidence reserved-key protection is enforced at the record boundary: record-level fields masquerading as evidence cannot enter through any construction path (P0 itself accepts arbitrary evidence keys; the record type owns this invariant).
- Revision/version semantics remain owned by P0 (version 1 = ORIGINAL; version > 1 ≠ ORIGINAL; invalid combinations fail on both construction paths).
- `ADMIT_INPUTS` remains deferred to the future consumer: zero executable admission calls in record.py; a valid record's `input` flows unchanged into the frozen batch admission gate.
- Record and component immutability are preserved (frozen dataclass; components own their immutability; no duplicated deep-freeze logic).
- No storage, network, acquisition, or research semantics were added.

### §103.5 Retained non-blocking observations (not remediated, not elevated)

```text
BLOCKER:  none
MAJOR:    none
MINOR:    none

O-16  Direct construction can accept nested/sequence-wrapped reserved keys
      in a hand-built P0 evidence payload. This shape is unreachable through
      the sanctioned create() path because frozen Phase I blocks it at the
      source; the record type's restatement is a flat top-level check.
O-17  Direct construction aliases an input source_native_id tuple. The tuple
      is immutable, so there is no mutation/integrity risk.
```

The independent re-audit classified both as non-blocking observations. They remain open and are not scheduled; they do not affect the frozen contract guarantees above.

### §103.6 Governance effect

This freeze is an infrastructure milestone only.

It does not:

- activate external-information research;
- create a candidate;
- authorize external-data acquisition;
- authorize Phase III;
- modify the Research Capacity Hold;
- reopen closed research;
- modify BOE governance;
- modify architecture governance.

The authoritative project state remains RESEARCH CAPACITY HOLD (§99).

### §103.7 Phase III firewall

```text
PHASE III:                  NOT STARTED
EXTERNAL DATA ACQUISITION:  NOT AUTHORIZED
RESEARCH AUTHORIZATION:     UNCHANGED

This record grants no Phase III implementation authorization.
```

---

## 104. EXTERNAL INFORMATION MVC PHASE III — SCOPE-DEFINITION AUDIT RECORDED (2026-09-21)

**Status:** AUDIT RECORD — BOUNDARY DEFINED, NOT AUTHORIZED — RESEARCH STATE UNCHANGED

This section records the factual result of a read-only Phase III scope-definition / authorization-boundary audit performed on 2026-09-21 (baseline: HEAD bcdfbb7; suite 1092 passed / 0 failures; handoff ending at §103; zero Phase III implementation files; zero acquisition code in the frozen packages). It is factual bookkeeping only. It changes no research conclusion, no governance rule, no architecture decision, and no research priority. The §99 research-capacity hold stands unchanged.

### §104.1 Audit result

The audit's final classification was:

```text
B — PHASE III CAN BE DEFINED; OWNER AUTHORIZATION REQUIRED
```

Justification (as derived by the audit): both frozen MVC records name exactly what was deferred (§102.1 / §103.1: "no grouping (Phase III)", "no artifact storage"), and the remaining gap — governed artifact storage plus record grouping/batch semantics feeding the already-frozen P0 admission gate — is genuinely distinct from Phases I/II, constructional rather than acquiritional, fully synthetic-testable, and free of research semantics. Defining Phase III consumed no research authorization. The audit also verified: no hidden Phase III implementation exists under another name; the `data/fred` CSV directory is pre-existing, gitignored, ungoverned historical data with no connection to any frozen contract, and is not Phase III evidence; no closed negative-knowledge line (§99.1) is reopened or supported by the defined boundary.

### §104.2 Minimum defensible boundary as defined (NOT implemented, NOT authorized)

1. **Governed external-artifact store** — local, content-addressed persistence for bytes matching an existing frozen `ArtifactReference`; hash/size/media-type verified on ingest; reference-in/reference-out; zero network operations; fail closed on any mismatch or duplicate conflicting ingest.
2. **Record grouping / batch semantics** — immutable, versioned grouping of already-constructed Phase-II `ExternalInformationRecord`s: revision chains linked by P0 `record_id`, provenance-preserving admission batches for handoff to the frozen `ADMIT_INPUTS` by a future consumer, and completeness assertions over a group. P0 `compute_record_id` remains the sole identity algorithm; no new identity, basis, modality, or revision taxonomy.

Candidate modules only (would require authorization): `research/external_information/artifact_store.py`, `research/external_information/grouping.py`, plus contract tests. The boundary is fully validable with synthetic bytes, synthetic artifacts, and synthetic record fixtures — no real external data is required at any point.

### §104.3 Explicit exclusions and firewalls (unchanged)

The defined boundary excludes: any acquisition of external data (HTTP/API/scraper/download); source adapters, polling, or calendars; consensus/vintage/event-window semantics; dataset publication into the Dataset Foundation; research-consumer code; new admission reason codes; any BOE dependency in either direction; any `EnvironmentSnapshot` change; any weakening of the frozen modality separation (QUOTE_ACTIVITY_PROFILE ≠ TRADE_VOLUME_PROFILE ≠ TIME_AT_PRICE ≠ TRADE_DIRECTION_PROFILE ≠ ORDER_FLOW_PROFILE ≠ ORDER_BOOK_PROFILE). Information novelty is not mechanism novelty (§98); capability existence is not research authorization (§99). Real external-data acquisition and any research consumer each require separate, explicit owner authorization decisions.

### §104.4 Authorization state (as of this record)

```text
PHASE III:                  DEFINABLE (CLASSIFICATION B) — OWNER AUTHORIZATION REQUIRED
PHASE III IMPLEMENTATION:   NOT AUTHORIZED
EXTERNAL DATA ACQUISITION:  NOT AUTHORIZED
RESEARCH ACTIVATION:        NOT AUTHORIZED
NEW CANDIDATE:              NONE
ECONOMIC VALIDATION:        NONE
BOE:                        UNCHANGED
GOVERNANCE:                 UNCHANGED
RESEARCH CAPACITY:          HOLD
```

---

## 105. EXTERNAL INFORMATION MVC PHASE III — FROZEN (2026-09-22)

**Status:** COMPLETE — INFRASTRUCTURE FREEZE — RESEARCH STATE UNCHANGED

This section records the formal freeze of External Information MVC Phase III (governed artifact store + record grouping / batch semantics) following its independent implementation audit (final result: PASS — NO BLOCKING FINDINGS). It is factual bookkeeping only. It changes no research conclusion, no governance rule, no architecture decision, and no research priority. The §99 research-capacity hold stands unchanged.

### §105.1 Scope (factual inventory)

Phase III implemented exactly two new modules plus their contract tests and the package export update:

- `research/external_information/artifact_store.py` — `ArtifactStore` + `ArtifactStoreEntry` + `ArtifactStoreError`: governed, local, content-addressed artifact persistence. Content hash (SHA-256 via the frozen Phase I `ArtifactReference`) is the sole identity. `storage_location` is recorded as provenance metadata only and is never used as a filesystem path. Ingest verifies hash and byte size before writing; retrieval verifies before returning; fail closed on any mismatch, missing artifact, or conflicting content. Idempotent on same-content duplicate. Zero network operations.

- `research/external_information/grouping.py` — `RecordBatch` + `RecordBatchError`: immutable, versioned, governed record grouping / batch semantics for already-valid frozen Phase-II `ExternalInformationRecord` objects. Batch identity is deterministic (derived from sorted member `record_id:version` pairs via SHA-256). Membership is deduplicated by identity. Ordering is deterministic (sorted by frozen P0 `sort_key()`). Cross-modality batches are permitted. The batch encodes no research meaning — no same-event, same-market, same-signal, same-outcome, or same-strategy implication.

- `research/external_information/__init__.py` — updated docstring and exports to include Phase III modules (`ArtifactStore`, `ArtifactStoreEntry`, `ArtifactStoreError`, `RecordBatch`, `RecordBatchError`).

- `tests/test_external_information_phase3.py` — 49 targeted tests across 14 test classes covering artifact store (happy path, integrity, missing, duplicate, remove, path security, immutability, metadata, boundary) and record batch (happy path, empty, deduplication, ordering, cross-modality, immutability, serialization, invalid, boundary).

Explicitly NOT part of Phase III (verified absent at freeze): no external-data acquisition; no HTTP/API client code; no web scraping; no source polling; no macro-release acquisition; no consensus acquisition; no positioning acquisition; no document discovery; no research datasets; no event-study infrastructure; no signal generation; no strategy logic; no candidate creation; no economic validation; no backtesting; no BOE changes; no P0 changes; no Phase I changes; no Phase II changes.

### §105.2 Independent verification lineage

Phase III implementation (suite 1092 → 1141) → independent read-only adversarial audit (27 adversarial checks: path traversal defense, content-hash identity, idempotent store, integrity verification, tampered-content rejection, wrong-payload rejection, missing-artifact fail-closed, conflicting-content rejection, remove correctness, has()-integrity, partial-write detection, no-acquisition-code, batch-identity determinism, different-batch-IDs, empty-batch, deduplication, version-preservation, immutability, batch_id-read-only, P0-sort-key ordering, cross-modality, as_dict-deterministic, no-research-semantics, no-knowledge-time-semantics, no-BOE-dependency, no-acquisition-code-in-grouping, non-record-rejection, invalid-batch-version-rejection, naive-created_at-rejection) → **PASS — NO BLOCKING FINDINGS** (no frozen-contract violation, no research-semantic leakage, no acquisition infrastructure, no BOE dependency, repository unchanged by audit).

### §105.3 Verification state at freeze

```text
Phase III targeted suite:    49 passed / 0 failures   (verified 2026-09-22)
Full suite:                 1141 passed / 0 failures  (verified 2026-09-22)
Independent adversarial checks: 27 passed / 0 failures
Blocking findings:          0
Major findings:             0
```

### §105.4 Contract guarantees (independently verified)

Artifact Store:

- `content_hash` remains the governing artifact identity (frozen Phase I `ArtifactReference`).
- `storage_location` is recorded as metadata only; it is never treated as a filesystem path authority.
- Stored content is integrity-checked against the reference on both ingest and retrieval.
- Tampered content is rejected on retrieval.
- Wrong payload is rejected on ingest.
- Missing artifact fails closed (raises `ArtifactStoreError`).
- Conflicting content under the same hash is rejected.
- Idempotent same-content storage is deterministic.
- No acquisition code exists in the module.

Record Batch:

- Membership consists exclusively of valid frozen Phase-II `ExternalInformationRecord` objects.
- Batch identity is deterministic (order-independent, derived from sorted member identities).
- Ordering is deterministic (sorted by frozen P0 `sort_key()`).
- Deduplication by `record_id:version` is explicit.
- Different record versions remain distinct members.
- Batch state is immutable (frozen dataclass).
- Serialization (`as_dict()`) is deterministic and JSON-serializable.
- No research meaning is encoded by grouping.

Architectural:

- No P0 construction by Phase III modules.
- No mutation of frozen P0 / Phase I / Phase II objects.
- No knowledge-time mutation.
- No BOE dependency.
- No `EnvironmentSnapshot` changes.
- Modality separation remains intact (DOCUMENT / MACRO_RELEASE / POSITIONING).

### §105.5 Retained non-blocking observations (not remediated, not elevated)

```text
BLOCKER:  none
MAJOR:    none
MINOR:    none

O-Phase3-01  has() verifies artifact integrity by reading the entire artifact.
              This is potentially I/O-heavy at scale but is not a
              correctness or security defect.

O-Phase3-02  remove() uses rmdir(), so unexpected residual files may
              prevent directory removal. This is consistent with
              fail-closed behavior and is not a correctness defect.

O-Phase3-03  Batch identifiers use the first 16 hexadecimal characters of
              SHA-256, giving a 64-bit identifier. Sufficient for expected
              batch volume; non-security-critical.
```

All three are retained as observations only. None blocks the freeze. None is elevated into remediation. None changes the Phase III boundary.

### §105.6 Governance effect

This freeze is an infrastructure milestone only.

It does NOT:

- activate research;
- create a candidate;
- authorize external-data acquisition;
- authorize Phase IV;
- reopen closed research;
- modify the Research Capacity Hold;
- modify BOE governance;
- modify P0 governance;
- modify Phase I;
- modify Phase II.

The authoritative project state remains RESEARCH CAPACITY HOLD (§99). The existence of the frozen artifact store and batch infrastructure does not constitute permission to populate it with live external data.

```text
PHASE III:                  FROZEN
RESEARCH CAPACITY:          HOLD
ACTIVE RESEARCH:            NONE
NEW CANDIDATE:              NONE
EXTERNAL DATA:              NONE ACQUIRED
BACKTEST:                   NONE
ECONOMIC VALIDATION:        NONE
BOE:                        UNCHANGED
GOVERNANCE:                 UNCHANGED
```

### §105.7 Phase IV / future-work firewall

```text
PHASE III:                  FROZEN
PHASE IV:                   NOT DEFINED / NOT AUTHORIZED
```

Any future extension requires a separate scope-definition and authorization process. In particular:

- external-data acquisition remains separately governed;
- research consumption remains separately governed;
- research semantics remain separately governed.

The existence of the frozen artifact store and batch infrastructure must not be treated as permission to populate it with live external data, conduct research, create candidates, run backtests, or begin Phase IV.

---

## 106. GOLD BANK FORENSIC AUDIT — READ-ONLY GOVERNANCE RECORD (2026-09-27)

**Status:** Completed forensic / read-only audit. No research activation. No state change.

**Source:** Owner-supplied Pine Script (`Price Action Concepts [GOLD BANK INDICATOR]`, short title `GOLD BANKINDICATOR-V1`, `@version=5`, `indicator()` object) provided in conversation; attachment transport unavailable. No repository Pine source exists for it; none was fabricated or stored. Full record: `docs/audits/GOLD_BANK_FORENSIC_AUDIT_2026-09-27.md`.

**Research authorization:** none. **Candidate created:** none. **Experiment executed:** none.

### §106.1 Principal technical findings (preserved)

* Explicit HTF `request.security(..., lookahead = barmerge.lookahead_on)` for D/W/M/12M high-low references — material historical causal-timing risk.
* Future-confirmed pivots with drawings anchored at the historical pivot location — historical visual-information timing mismatch.
* Dynamic internal-lookback block misordered (`vv >= 1.5` branch captures all later thresholds; intended adaptive 10→5 mapping inoperative), with persistent `iLen` making behavior path-dependent.
* "Volumetric order block" terminology overstates data semantics: TradingView `volume` plus bar-state counters only; no bid/ask volume, aggressor direction, order-book depth, or resting-liquidity data.
* Order blocks are downstream of BOS/CHoCH structure — no independent mechanism established by displaying them as separate zones.
* Advertised modules incomplete or effectively inert as supplied (FVG inputs, accumulation/distribution inputs, EQH/EQL display, candle/bar-color controls, alert scaffolding portions); implementation inconsistencies in the bearish `"Precise"` order-block branch and weak-low volume labels.
* No complete executable strategy defined: no unique entry, execution price, stop, target, horizon, sizing, costs, overlap policy, control, or outcome.

### §106.2 Disposition

> GOLD BANK is preserved as an audited descriptive indicator artifact. No genuinely distinct mechanism survived the forensic distinctness review. No candidate, backtest, external-data acquisition, economic validation, or Phase IV activity is authorized or implied. Existing closed/preserved QuantForge lines remain unchanged.

Overlap preserved without reopening: DISC-021 (no new standalone mechanism), DISC-022 (same broader continuation family), DISC-025 + SMC/liquidity-sweep family (overlap, no distinct mechanism), SMC Institutional POI / Idea 2 (conceptual overlap only).

> Future sessions must not restart the GOLD BANK investigation merely by re-labeling, re-parameterizing, combining, or visually selecting BOS/CHoCH/OB/FVG/premium-discount/candlestick/MTF variants unless a separately governed and demonstrably distinct mechanism is established and authorized.

Observation / interpretation / mechanism / opportunity / authorization / state remain distinct. The conclusion is scoped to the supplied indicator as audited — not proof about every possible use of any component.

### §106.3 Governance effect

None. This section is a read-only record:

```text
RESEARCH CAPACITY:          HOLD
ACTIVE RESEARCH:            NONE
NEW CANDIDATE:              NONE
BACKTEST:                   NONE
ECONOMIC VALIDATION:        NONE
EXTERNAL RESEARCH DATA:     NONE
PHASE IV:                   NOT AUTHORIZED
BOE:                        UNCHANGED
GOVERNANCE:                 UNCHANGED
```
