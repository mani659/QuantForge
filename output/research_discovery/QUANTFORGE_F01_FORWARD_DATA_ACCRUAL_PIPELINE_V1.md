# QUANTFORGE — F-01 FORWARD-DATA ACCRUAL PIPELINE V1

**Milestone:** F-01 governed forward-data accrual infrastructure (design + implementation)
**Status:** **F-01 FORWARD-DATA ACCRUAL PIPELINE OPERATIONAL — NO CURRENT OBSERVATIONS**
**Parent governance:** V38 (RATIFIED); V38A (RATIFIED, BV1–BV13); BS1–BS13 (RATIFIED); BF1–BF13 (RATIFIED); F-01 Registration Freeze V1 (SHA `41883aaeab6a`); Stage 2 V1 (SHA `8d8177c2df49`); Stage 3 gate V1 (SHA `558d8e9b8b4b`)
**This is INFRASTRUCTURE ONLY.** It provides the provenance-preserving mechanism for future admissible `USTECm` observations; it validates nothing, computes no economics, changes no registration, and does not make F-01 Stage-3 ready.
**SESSION_HANDOFF intentionally NOT modified** (infrastructure milestone; default per mandate §28).

Label conventions: GOVERNANCE FACT / INFRASTRUCTURE / STRUCTURAL TEST / AUDIT / NOT PERMITTED.

---

## 1. EXECUTIVE INFRASTRUCTURE VERDICT

**F-01 FORWARD-DATA ACCRUAL PIPELINE OPERATIONAL — NO CURRENT OBSERVATIONS.**

A governed, append-only forward-data accrual mechanism is established for the frozen F-01 study. It is fully implemented and structurally tested (17/17 pipeline tests P1–P12 pass), and it is initialized with an empty study archive consistent with the registered accrual state (0 eligible observations — the correct state, not a defect). The pipeline can now receive future admissible USTECm M1 exports from the authorized acquisition mechanism, preserve them append-only with full chain-of-custody hashing, and report only structural accrual state. It cannot compute economics, cannot access protected material, and cannot launch Stage 3.

No economic computation, no registration change, and no scope change occurred. F-01 remains REGISTERED; Stage 3 remains DATA ACCRUAL PENDING until the frozen boundary reaches 63/126 eligible sessions.

## 2. GOVERNANCE STATE

(GOVERNANCE FACT) Verified at authoring:

- V38/V38A/BS1–BS13/BF1–BF13 all RATIFIED; F-01 = REGISTERED; Stage 2 = STRUCTURALLY VALID; Stage 3 = DATA ACCRUAL PENDING (gate report SHA `558d8e9b8b4b`); Base Registry = **EMPTY**; Base = NONE; no Stage 4.
- HEAD `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`; branch `main`.
- Registration SHA `41883aaeab6a`; calendar SHA `39e5b3cfa25c8ae13d0debddff2b5f480b836aa29785b42b94f4484048a81696`; sealed baseline `data/m1/USATECHIDXUSD_M1.csv` SHA `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`; Stage-2 implementation SHA `65189960e4150f31284fcd456cacf7c661b8555e4f0d5f919bae9be4bae08e8d`.

## 3. REGISTERED DATA BOUNDARY

(GOVERNANCE FACT) The pipeline enforces the frozen boundary automatically:

- Validation-eligible evidence begins at the session-open boundary of the freeze date: **2026-09-03 09:30 America/New_York = 2026-09-03 13:30 UTC** (DST, computed via the registered US DST rule — not a hard-coded offset).
- `timestamp < boundary` ⇒ **REJECT / NON-STUDY** (recorded in the ingest report; never admitted, never backfilled).
- `timestamp >= boundary` ⇒ candidate for registered accrual.
- The sealed baseline archive (`data/m1/…`, through 2026-07-10) is never read or modified by the pipeline; the protected forward window (2026-07-11 → 2026-09-02) is never referenced.

## 4. AUTHORIZED SOURCE

(GOVERNANCE FACT / INFRASTRUCTURE) The authorized acquisition mechanism is the repository's existing MT5 infrastructure, not a new external feed:

- **Connector:** `broker/mt5_connection.py` (broker-layer terminal verification; environment-configured via `QF_MT5_TERMINAL_PATH` / `QF_MT5_EXPECTED_ACCOUNT`; credential-free by design).
- **Export pattern:** the established MT5 CSV-export mechanism that produced `data/m1/*.csv` (schema `timestamp,open,high,low,close,volume`), for symbol `USTECm` (logical `USATECHIDXUSD`) on Exness-MT5Trial15.
- **Operation:** the operator exports fresh USTECm M1 bars from the authorized terminal and invokes `python research/f01_v38a_accrual_pipeline.py --ingest <export.csv>`. The pipeline validates, appends, and hashes.
- No live MT5 connection is run by this milestone (no terminal/credentials in this environment; the security boundary forbids embedding secrets — §16). No credentials, tokens, or connection secrets are stored in code, artifacts, or logs.
- (NOT PERMITTED) The pipeline never sources from protected forward artifacts; if the only available data were protected, the correct state would be ACCRUAL PIPELINE BLOCKED — not circumvention.

## 5. RAW DATA PRESERVATION

(INFRASTRUCTURE) Raw export values are preserved exactly as provided: original timestamps, original OHLC values, source identity (export path recorded in the snapshot ledger), acquisition timestamp, and snapshot identity. The separation is explicit:

- **RAW ACCRUAL:** what the authorized source provided (the export file; validated, not transformed).
- **STUDY NORMALIZATION:** none required beyond the registered representation (the study archive stores the same schema with `volume=0`, matching the registered baseline convention) — deterministic, documented, versioned.
- No economic transformation exists anywhere in the pipeline.

## 6. TIMESTAMP GOVERNANCE

(INFRASTRUCTURE) Source timestamps are preserved exactly as provided (naive UTC, Exness server convention per the frozen symbol-mapping/normalization decisions). The pipeline documents: source representation = `YYYY-MM-DD HH:MM:SS` UTC; exchange-local = America/New_York via the registered US DST rule (second Sunday March 02:00 → first Sunday November 02:00); no single hard-coded UTC offset (verified: DST tests for March/November 2026 in the self-test suite). Boundary conversion is computed per date.

## 7. CALENDAR INTEGRATION

(INFRASTRUCTURE) The pipeline consumes exactly the frozen calendar artifact `output/research_discovery/QUANTFORGE_F01_V38A_CALENDAR_V1.json` with **hash verification on every run** (mismatch ⇒ abort). It uses the calendar to identify eligible sessions, session opens/closes, early closes (13:00 ET), and next-session mapping. The calendar is never modified by the pipeline; calendar changes belong to a separate governance process.

## 8. APPEND-ONLY ACCRUAL

(INFRASTRUCTURE) The study archive (`data/f01/ustechidxusd_m1_study.csv`) is written strictly append-only:

- Existing rows are never modified, deleted, reordered, or overwritten (verified by test: a conflicting re-ingest is quarantined and the archive hash is unchanged).
- Newly admitted bars are appended in timestamp order.
- A correction to an upstream observation produces a new governed snapshot/version (a new ledger entry and new hash) rather than mutating prior evidence.
- State-file updates use atomic replace (temp file + `os.replace`); no partial writes.

## 9. SNAPSHOT / HASH CHAIN

(INFRASTRUCTURE) Chain of custody is maintained in `data/f01/snapshot_ledger.jsonl`:

```text
SOURCE (authorized export)
  ↓  validation
RAW SNAPSHOT
  ↓  append + hash
STUDY SNAPSHOT (archive SHA-256)
  ↓  ledger entry
CHAIN: SNAP-0000 (GENESIS) → SNAP-0001 → …
```

Each ledger entry records: snapshot ID, predecessor hash, source, acquisition timestamp, first/last timestamp, row count, SHA-256, registration reference, pipeline version. Existing hash records are never rewritten (append-only ledger). Current genesis state: SNAP-0000, 0 rows, archive hash `effa52d7ab38…` (hash of the empty header-only archive).

## 10. DATA-QUALITY CONTROLS

(INFRASTRUCTURE) Every ingest run checks: schema identity; malformed rows; duplicate timestamps (exact vs conflicting); out-of-order timestamps (rows sorted before processing; conflicts reported); missing required price fields; non-positive prices; invalid OHLC relationships; price-scale plausibility for USTECm (structural source-identity check: 100 < price < 1,000,000); unexpected timestamp gaps (vs the frozen calendar). Structural failures are **rejected/quarantined according to the deterministic policy** (§11) — never silently repaired. A run with fatal errors exits non-zero and writes no partial archive changes.

## 11. DUPLICATE / GAP HANDLING

(INFRASTRUCTURE)

- **Exact duplicate** (same timestamp, same values): collapsed with explicit provenance — the collapse is counted in the ingest report and the resulting study snapshot is reconstruction-equivalent (unique-by-timestamp rows); provenance is preserved in the report.
- **Conflicting duplicate** (same timestamp, different values): **never silently chosen** — quarantined (counted, reason recorded) and escalated in the ingest report; the archive is not modified by that row.
- **Expected market closures** (weekends, holidays, registered calendar closures): not gaps — no alarm, no action.
- **Unexpected data gaps** (a calendar-eligible session with no bars): recorded as a gap observation in the ingest report; never filled, interpolated, forward-filled, or auto-substituted from another source.

## 12. PROTECTED-DATA FIREWALL

(AUDIT — PASS) The pipeline never inspects, parses, copies, merges, summarizes, compares, hashes, or derives anything from protected forward material (the forward runtime's ledgers, event logs, and health state; G6 forward artifacts). Its only file operations are: the operator-supplied export (allowlisted via the `--ingest` argument), the frozen calendar (hash-verified), and the study directory `data/f01/` (study archive, snapshot ledger, state file). The self-test suite verifies the module contains no protected-root path references (test P10, constructed-token check). Protected markers do not appear in the module text.

## 13. STUDY ELIGIBILITY BOUNDARY

(INFRASTRUCTURE) The pipeline identifies timestamp eligibility (≥ 13:30 UTC 2026-09-03), session eligibility (frozen calendar), and data completeness — structural facts only. It determines whether required session-open/close observations exist. It does **not** compute overnight return, net return, P&L, expectancy, win rate, Sharpe, or drawdown — the module contains no economic computation (tests P11; source inspection).

## 14. STAGE 3 TRIGGER INTERFACE

(INFRASTRUCTURE) The pipeline exposes only structural trigger information:

```text
eligible_sessions_with_data
primary_complete (>= 63 eligible sessions)
confirmation_complete (>= 126 eligible sessions)
data_snapshot_hash
calendar_hash
registration_hash
```

Current values: `0 / False / False` + the genesis hashes — exactly matching the registered DATA ACCRUAL PENDING state. No performance is exposed. The decision "is the frozen registered sample sufficient for Stage 3?" remains a separate governed evaluation.

## 15. FAILURE HANDLING

(INFRASTRUCTURE) Deterministic failure modes: source unavailable (export file missing ⇒ report error, non-zero exit, no archive change); schema mismatch (abort); calendar hash mismatch (abort); malformed rows (counted, rejected); duplicate timestamps (collapse-with-provenance or quarantine per §11); feed identity suspect (price-scale violation ⇒ abort with `PRICE SCALE OUT OF REGISTERED RANGE`); clock/timezone errors (timestamps must parse; boundary computed per-date); stale data (pre-boundary rows rejected as NON-STUDY); unexpected gaps (recorded, never filled); calendar mismatch (calendar is fixed). Every failure produces **ACCRUAL FAILURE / QUARANTINED** semantics — never silent progression.

## 16. SECURITY BOUNDARY

(GOVERNANCE FACT) No credentials, passwords, tokens, or connection secrets are placed in Git, research artifacts, logs, or commit messages. The acquisition path uses the repository's existing environment-configured connector (`QF_MT5_TERMINAL_PATH` / `QF_MT5_EXPECTED_ACCOUNT`); the pipeline itself contains no secret material and no connection code.

## 17. PIPELINE STRUCTURAL TESTS

(STRUCTURAL TEST — 17/17 PASS, run 2026-09-03)

| Test | Check | Result |
|---|---|---|
| P1 | Source identity (schema) — wrong schema rejected | **PASS** |
| P2 | Freeze-boundary enforcement — pre-freeze bars rejected | **PASS** |
| P3 | Append-only — post-freeze admitted; conflicting re-ingest quarantined with archive hash unchanged | **PASS** |
| P4 | Duplicate detection — exact duplicate collapsed with provenance | **PASS** |
| P5 | Gap detection — expected closures not gaps; unexpected gaps recorded, never filled | **PASS** |
| P6 | Timezone/DST correctness — Mar/Nov 2026 offsets; boundary = 13:30 UTC | **PASS** |
| P7 | Calendar integration — Labor Day excluded; early close 13:00 ET | **PASS** |
| P8 | Snapshot hashing — identical ingest ⇒ identical archive hash | **PASS** |
| P9 | Reproducible reconstruction — fresh dir, same inputs ⇒ identical archive hash | **PASS** |
| P10 | Protected-data firewall — no protected-root references in module | **PASS** |
| P11 | No-economic-output firewall — no return/P&L computation in module | **PASS** |
| P12 | No-automatic-Stage-3 firewall — no launch path in module | **PASS** |

Test fixtures are synthetic timestamp/price structures (no economic results); the suite runs in an isolated temporary directory and never touches the operational study archive.

### Final Independent Audit (Q1–Q12, per mandate §30)

- **Q1** Did the pipeline access protected forward data? **NO.** Protected forward material (the forward runtime's ledgers, event logs, and health state) is never referenced or opened (§12; test P10).
- **Q2** Did it backfill pre-freeze data into the study? **NO.** Pre-boundary bars are rejected as NON-STUDY on every run (§3; test P2); the sealed baseline is never read.
- **Q3** Did it modify F-01 registration? **NO.** The registration is consumed by hash reference only; nothing writes to any registration artifact.
- **Q4** Did it alter the calendar? **NO.** The frozen calendar is consumed hash-verified and never written (§7).
- **Q5** Did it introduce another instrument? **NO.** Only `USATECHIDXUSD`/`USTECm` schema and price-scale checks are implemented (§4).
- **Q6** Did it calculate economics? **NO.** The module contains no return/P&L/expectancy computation (§13; test P11).
- **Q7** Did it optimize anything? **NO.** No parameters, thresholds, costs, or filters are tuned or searched.
- **Q8** Can the pipeline reproduce the same snapshots from the same source? **YES if operational.** Identical inputs produce identical archive hashes (tests P8–P9).
- **Q9** Is the study boundary enforced automatically? **YES if operational.** Every run rejects pre-boundary rows by construction (test P2); the boundary is computed per-date via the registered DST rule (§6).
- **Q10** Does the pipeline automatically execute Stage 3? **NO.** No launch path exists (test P12); it reports structural trigger state only (§14).
- **Q11** Can data continue to accrue without changing the registration? **YES.** Append-only accrual is registration-agnostic beyond the frozen boundary (§8); the registration never changes.
- **Q12** Are post-study observations prevented from silently entering the registered Stage 3 sample? **YES.** The pipeline preserves admissible observations append-only in the archive but the registered Stage-3 sample is bounded by the frozen 126-session window — enforced at Stage-3 population construction (frozen Stage-2 logic), and the pipeline never labels or aggregates observations beyond the frozen boundary as Stage-3 evidence (§18 of mandate honored).

## 18. CURRENT ACCRUAL STATE

(INFRASTRUCTURE) Initialized 2026-09-03, 16:06 UTC:

- Study archive `data/f01/ustechidxusd_m1_study.csv`: header only, 0 rows, SHA `effa52d7ab3829ade581e048acc8643a04db5f3f5b528dc5ee321768671ada07`.
- Snapshot ledger `data/f01/snapshot_ledger.jsonl`: GENESIS entry (SNAP-0000, predecessor GENESIS, registration reference, sealed-baseline reference).
- State `data/f01/accrual_state.json`: `archive_row_count 0`, `eligible_sessions_with_data 0`, `primary_complete False`, `confirmation_complete False`, `last_snapshot_id SNAP-0000`.
- Status: **ACCRUAL PIPELINE OPERATIONAL — NO CURRENT OBSERVATIONS** (absence of new market observations is NOT an infrastructure failure).
- `data/f01/` is gitignored per the repository's data convention; the pipeline implementation lives at `research/f01_v38a_accrual_pipeline.py` (SHA `3f3a90b2b0a4dbeb802de971d502b4f260b1cfee650ba787bd978bf28945f58d`).

## 19. REPOSITORY / GIT INTEGRITY

(GOVERNANCE FACT) Recorded at completion:

- HEAD before and after: `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`; branch `main`.
- New files: `research/f01_v38a_accrual_pipeline.py` (implementation, SHA `3f3a90b2b0a4…`) and the gitignored data directory `data/f01/` (study archive, snapshot ledger, accrual state — data, per repository convention).
- No commit, no staging (infrastructure milestone; no convention requires a commit).
- `SESSION_HANDOFF.md` intentionally NOT modified.
- No source/configuration change; no registration change; no calendar change; no Base Registry record; no economic result; no protected-forward access; the sealed baseline and Stage-2 implementation are byte-identical to their frozen hashes.
- `git diff --check` verified clean.

## 20. HARD STOP

Infrastructure complete. **ACCRUAL PIPELINE OPERATIONAL — NO CURRENT OBSERVATIONS.** F-01 remains REGISTERED; Stage 3 remains DATA ACCRUAL PENDING; Base Registry EMPTY.

STOP. No Stage 3; no return/P&L calculation; no performance inspection; no registration modification; no scope extension; no protected forward material; no Base Registry entry; no Stage 4; no Conditional components. H01/ORD/TRADEABLE_EDGE remain CLOSED; CAND-077/081/083/099 unchanged; CAND-015/024/035 protected-forward and excluded.

Next research execution remains **F-01 V38A STAGE 3 ECONOMIC VALIDATION** — only when the frozen registered boundary reaches its declared sufficiency (primary ≥ 63 eligible sessions; full scope ≥ 126), evaluated as a separate governed milestone. The pipeline's governing principle is fixed: it exists to preserve future evidence, never to manufacture, select, repair, or optimize it.