# TASK120 — Execution Gate Evidence (G1–G7 + count gate)

**Authority:** TASK119 approval (recorded) + frozen preregistration
(`67432f71…`, re-verified byte-identical pre-run). V9 triple unchanged.
HOLD/NONE throughout. Single measurement invocation; one pre-run loader
crash (missing "timestamp" alias, exit 1, zero artifacts) followed by the
single bounded run — not a rerun (no measurement had occurred).

## G1 — Approval recorded
TASK119 approval record (`f07f13ab…`), scope = bundled CAND025-RM-01.
Verified pre-run.

## G2 — Preregistration frozen complete
`119_frozen_preregistration.md` hash-matched pre-run; adopted T1–T7 rules
explicit; run_config.md frozen pre-outcome (this task's config record).

## G3 — V9 freeze byte-identical
V9 triple re-verified pre-run (hashes per approval record §2). G2 identity
rule honored: zero rule/threshold/window changes.

## G4 — Implementation and review (PASS)

- Engine `cand025_engine.py` (`d8b2d45c…`, 8468 B): reads only the
  caller-supplied CSV; fixed SPEC dict + fixed seed 20261013; no network,
  MT5, tick, holdout, recorder, or adaptive logic (code-reviewed).
- No-look-ahead review: ATR/TR use bars ≤ signal point only (signal bar
  excluded from its own ATR window); entry/exit at bar opens (executable);
  costs subtracted post-trade; complete-bars-only with fail-closed counted
  skips; resample drops the incomplete trailing bar.
- One engine bug found and fixed pre-data (DataFrame index-alignment →
  all-NaN) via the synthetic self-test — exactly what G4 exists for.
- Synthetic self-test `test_engine_synthetic.py` (`25cc463a…`): 7/7 PASS —
  planted event exact (direction/entry/costs), quiet days silent,
  zero-direction skipped+counted, missing-09:30 skipped+counted,
  determinism byte-identical, analyze/T4 smoke. No market data involved.

## G5 — Data identity and integrity (PASS)

- File `data/m1/USATECHIDXUSD_M1.csv`: SHA-256 recomputed from actual bytes
  = `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`
  — EXACT match (56,818,845 bytes).
- Metadata (timestamp column only; no prices read for this check):
  906,815 rows, 2023-09-01T00:00Z→2026-07-10T20:14Z, monotonic, unique,
  0 Saturday bars — matches ema_grab/H01/F01 records.
- Instrument identity USATECHIDXUSD per filename + V9 records (not XAUUSDm).
- tz mapping (single attempt, principled, pre-outcome): naive timestamps
  read as UTC — no invented offset/DST; consistent with bare-timestamp
  quoting across H01/ORD/F01 records. NO second mapping under any outcome.

## G6 — Scope and execution controls (PASS)

Activity = this single run + reports (within approved bounds; zero
sweeps/reruns/variants). Code reads only the named file. No tick, holdout,
new collection, recorders, parameter search, candidate/runtime contact, or
adaptive behavior. Command recorded in the task report.

## G7 — Preregistration and decision-rule lock (PASS)

Frozen prereg unchanged; T1–T4 rules, Holm α=0.05, B=10000, seed, costs,
stops, and reporting all explicit pre-outcome; run_config.md frozen before
the run; no post-outcome amendment (none made).

## Count gate (outcome-blind, pre-returns): PASS via contingency

Enumerated 158 rule-satisfying events (skips all zero) BEFORE any return
was computed. Predeclared rule: ≥157 proceeds. 158 > 157 → full-set
primary per the T7 contingency; verification-subset subclause recorded
UNEXECUTABLE (no G1 event list exists on any record) — disclosed, not
worked around. <157 would have stopped with MEASUREMENT_INVALIDATED.
