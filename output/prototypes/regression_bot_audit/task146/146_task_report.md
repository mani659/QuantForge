# TASK146 — Bounded Execution Task Report

| Field | Value |
|---|---|
| Authorization | Owner verdict AUTHORIZE, Salman Ismail, 2026-10-14; v5 `1974fe6d…`; ratio bar CONFIRMED ACTIVE at 2.0 (filed: `146_execution_authorization.md`) |
| Directory | `output/prototypes/regression_bot_audit/task146/` |
| Mode | Single approved bounded chain executed once. No other run. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-14 (authorization date) |

## 1. Command and configuration (single invocation)

`.venv\Scripts\python.exe output/prototypes/regression_bot_audit/task146/run_measurement.py`
(run_config.md frozen pre-outcome; engine reviewed + 12/12 synthetic
self-tests + determinism verified pre-data, including one alignment-bug
fix and one spec-conformance correction removing a foreign t1 concept).
No rerun, sweep, variant, or retry under any outcome.

## 2. Gates (all passed pre-measurement)

G4 implementation review + synthetic self-test; G5 SHA exact match
(`1196c3f2…` vs H01 manifest row) + span/bars/identity + single-principle
tz mapping; G6 scope (named file only, no tick/holdout/recorders/adaptive
logic); G7 prereg lock + explicit params + frozen config. HOLD/NONE throughout.

## 3. Measurement outcome (reported, not promoted)

n=474 (1987-02→2026-07, skips 12/1/0). D1 mean −55.0 bps, CI
[−88.1,−22.4] bps, Holm p=1.0; D2 mean −80.6 bps; ratio −17.96.
**FAIL** (upper bound < 0). No promotion, no continuation, no rescue;
budget consumed.

## 4. Boundary confirmations

No sweep/rerun/variant, threshold/method change, registration, promotion,
deployment, runtime alteration, commit, or push. No omission: CIs, Holm p,
ratio, skips, contingency absence (N/A — no count anchor in this design),
and adverse mechanics fully reported. TASK133/144 artifacts and governing
documents unedited.

## 5. Manifest (verified after all edits)

| File | Purpose | Size / SHA-256 |
|---|---|---|
| `146_execution_authorization.md` | Filed owner approval | recorded below |
| `vs_tsmom_engine.py` | Reviewed minimal implementation (G4) | recorded below |
| `test_engine_synthetic.py` | Synthetic self-test, 12/12 (G4) | recorded below |
| `run_config.md` | Frozen pre-outcome config | recorded below |
| `run_measurement.py` | Single-run gated runner | recorded below |
| `monthly_series.csv` | Raw per-month outputs (474 rows) | recorded below |
| `results.json` | Result aggregates | recorded below |
| `REPORT.md` | Bounded evaluation report | recorded below |
| `146_task_report.md` | Verification and final status (this file) | digest in completion message |

## 6. Final status

**`MEASUREMENT_COMPLETED_REVIEW_REQUIRED`** — single bounded measurement
complete with full adverse-inclusive reporting; review of this package (not
a rerun) is the only lawful next step, under a separate decision if any.
