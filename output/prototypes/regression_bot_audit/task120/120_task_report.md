# TASK120 — Execution Gate Completion and Conditional Measurement: Task Report

| Field | Value |
|---|---|
| Task ID (inferred) | `TASK120` — next after `task119`; no task-ID registry exists |
| Directory | `output/prototypes/regression_bot_audit/task120/` |
| Mode | Single approved bounded chain executed once. No other run. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-13 |

## 1. Command and configuration (single invocation)

`.venv\Scripts\python.exe output/prototypes/regression_bot_audit/task120/run_measurement.py`
(run script `ddd69624…`, config `run_config.md` `11e09ee3…` frozen
pre-outcome; engine `d8b2d45c…`, self-test `25cc463a…` 7/7 PASS with one
pre-data bug found+fixed). One pre-run loader crash (missing "timestamp"
alias, exit 1, zero artifacts) preceded the single bounded run — not a
rerun. No second mapping, sweep, variant, or retry under any outcome.

## 2. Gate outcomes

G1 approval recorded; G2 prereg frozen/complete; G3 V9 byte-identical;
G4 implementation reviewed + synthetic self-test + determinism; G5 SHA
exact match + span/bars/identity + single-principle tz mapping; G6 scope
(single run, named file only, no tick/holdout/recorders/adaptive); G7
prereg lock + explicit params + frozen config. Count gate: 158 ≥ 157 →
proceed per predeclared contingency (full-set primary; subclause
disclosed unexecutable). Full evidence in the gate file.

## 3. Measurement outcome (reported, not promoted)

n=158 (2023-09-01→2026-07-02, zero skips). T1 PASS (+0.023/+2.281 halves);
mean net2 +1.152 (≈ G1 +1.25), net3 +0.152; T3 FAIL (CIs [−6.56,+8.84] /
[−7.62,+7.95], Holm p 0.78); T4 flag RAISED (84/158 continuation).
Go/no-go: NO-GO. Decision file: no confirmation, no promotion, no
continuation, no rescue; re-measurement budget consumed.

## 4. Boundary confirmations

No strategy modification, parameter search, discovery, alternate
instrument, unauthorized collection, sample expansion, threshold/method
change, registration, promotion, deployment, runtime alteration, commit,
or push. No omission: null/adverse mechanics (wide CIs, T4 flag, thin
first half, contingency subclause) all reported. Adverse results preserved
in full (events.csv, summary.json, phase1_count.json). HOLD / Active
Research NONE unchanged (re-verified post-write). TASK119 artifacts and
governing documents unedited.

## 5. Manifest (verified after all edits)

| File | Purpose | Size / SHA-256 |
|---|---|---|
| `cand025_engine.py` | Reviewed minimal implementation (G4) | 8468 B / `d8b2d45c353be3dc5514086f822d3ec78cb9236f20aee3bfb154a11d42855376` |
| `test_engine_synthetic.py` | Synthetic self-test, 7/7 (G4) | 6357 B / `25cc463a222192cf9fa4c766ebb3123203f5a42150417a417a404fe153b3e5c1` |
| `run_config.md` | Frozen pre-outcome config | 2123 B / `11e09ee3bf0b6d2dec2a9d7a86f9a396c81c66487c6a613ec11c527cf3491755` |
| `run_measurement.py` | Single-run gated runner | 3000 B / `ddd6962483c9c89371f5f33733a7e772c492dcceaddbffcc6436ad3320003337` |
| `phase1_count.json` | Outcome-blind count record | 318 B / `69c9575c82d79c82f5e6ae40e52f2e5b0b143077b404e45b1c1bdbd3ac494cd5cb57f258e25ff42206` |
| `events.csv` | Raw per-event outputs (158 rows) | 14567 B / `6171e9a3876b11dff42494eba53fa31b8592951dc5974c9d5e3620d08fd1d868` |
| `summary.json` | Result aggregates | 990 B / `92f071f772ddb755fc7462ac497b6f67637fabe2ae76459e4c999dc3b165dab0` |
| `120_execution_gate_evidence.md` | G1–G7 + count-gate evidence | 3576 B / `230d36b033c2cd0dfec77b3a070f9f4d656345fe84298e674e415a37f87732c4` |
| `120_measurement_results.md` | Outcomes vs adopted bars | 1666 B / `bcf344e4d7ddda2119482aff16c85bae00c9c0913b28b6cc284c953114a867ee` |
| `120_decision_and_limitations.md` | NO-GO decision + binding limits | 1606 B / `e44922a402a562e5259b66daa50196fd460df192a5f00dde076b1de9801d7167` |
| `120_task_report.md` | Verification and final status (this file) | digest computed post-write; recorded in the TASK120 completion message |

## 6. Final status

**`MEASUREMENT_COMPLETED_REVIEW_REQUIRED`** — single bounded measurement
complete with full adverse-inclusive reporting; review of this package (not
a rerun) is the only lawful next step, under a separate decision if any.
