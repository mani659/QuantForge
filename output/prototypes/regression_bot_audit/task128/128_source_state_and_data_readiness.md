# TASK128 — Source State and Data Readiness

| Field | Value |
|---|---|
| Task ID (inferred) | `TASK128` — next after `task127`; no task-ID registry exists |
| Directory | `output/prototypes/regression_bot_audit/task128/` |
| Mode | Read-only analysis. No execution. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-13 |

## State verification

HOLD / Active Research NONE confirmed. TASK123–127 hashes verified. The
4-asset XSM design is structurally underpowered (TASK125/126: A —
CALIBRATED, LOW-POWER). No broader cross-sectional universe exists (TASK127:
B — DATA GAP). The regression concepts (R1/R2) are excluded without testing.
EXT-054/MDP/PROTO-TREND-001 are closed. CAND-025 is NO-GO. RS-404 is
closed-invalid.

## Available single-instrument data (verified, authorized for research use)

| Instrument | Source | Coverage | Observations | Verification |
|---|---|---|---:|---|
| NASDAQ100 | FRED | 1986-01→2026-08 | 10,602 daily | Verified; research use |
| NASDAQCOM | FRED | 1971-02→2026-08 | 14,491 daily | Verified; research use |
| SP500 | FRED | 2016-08→2026-08 | 2,610 daily | Verified; research use |
| DJIA | FRED | 2016-08→2026-08 | 2,610 daily | Verified; research use |
| USATECHIDXUSD | MT5 M1 | 2023-09→2026-07 | 906,815 M1 | SHA `39f25619…`; consumed by CAND-025-RM-01 |
| XAUUSD/XAGUSD | Tick canonical | 62 monthly files each | — | Verified; research use |

## Authorization boundaries

- No evaluation authorization exists for any non-Batch-1 dataset.
- Reuse of USATECHIDXUSD for a new evaluation requires a new explicit
  authorization (CAND-025-RM-01 consumed its budget).
- FRED data is authorized for research use but not for evaluation.
- No data collection, downloading, or purchasing is authorized.
- No holdout access. No runtime contact. No candidate creation.
