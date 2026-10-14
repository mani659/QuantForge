# TASK128 — Task Report

| Field | Value |
|---|---|
| Task ID (inferred) | `TASK128` — next after `task127`; no task-ID registry exists |
| Directory | `output/prototypes/regression_bot_audit/task128/` |
| Mode | Read-only analysis. No execution. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-13 |

## Verification

State verified (HEAD, HOLD/NONE, TASK123–127 hashes). FRED data verified
(NASDAQ100: 10,602 daily obs, 1986→2026). No data content accessed for
performance analysis. No holdout access. No runtime contact. HOLD / Active
Research NONE unchanged.

## Decision

**A — EXPERIMENT PROPOSAL READY** (conditional on §99.1 ruling).

Selected direction: volatility-scaled time-series momentum on NASDAQ100.
Uses verified FRED data (40 years daily). Distinct from fixed TSMOM by
mechanism (regime-conditional sizing vs fixed sizing), pending §9.1
ruling. No new data purchase necessary.

## Deliverables

All 7 files written. Hashes verified in `128_manifest.sha256`. Working-tree
diff contains only the seven new TASK128 files.

## Final status

TASK128 COMPLETE — STOP. The proposed experiment is not authorized. Any
execution requires a §9.1 ruling and separate evaluation authorization.
