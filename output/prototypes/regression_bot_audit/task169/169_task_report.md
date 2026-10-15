# TASK169 — Task Report

| Field | Value |
|---|---|
| Task | `TASK169` — fixed-config nonlinear ML diagnostic (RF vs RBF SVM) |
| Directory | `output/prototypes/regression_bot_audit/task169/` (new) |
| HEAD / branch | `9bac975` / `main` (unchanged; no commit, no push) |
| Scope source | owner-requested bounded comparison (recorded in protocol §1; no signature fabricated) |
| Date | 2026-10-15 |

## Execution summary

- **Phase A:** verified `_t39_baskets_forensics.jsonl` against TASK152
  source: SHA `e2fa8173…`, 1031 rows, outcome 651/380, four predictors
  zero-missing and pre-entry, split 700/241 and 331/139 reproduced
  exactly (no discrepancy → no reconciliation stop). Governing-rule
  check: §99.1 families don't cover this branch, no formal closure/
  rescue-bar record exists, TASK152's "Test partition never reused"
  tension recorded with resolution pre-fit (protocol §3).
- **Protocol locked pre-fit:** `169_nonlinear_ml_protocol.md`
  7907 B / `159b84f19d609dbbf29c6474a5461c8ae66f5a05fb121b33944840d44aa72b05`.
- **Phase B/C:** one run of `run_task169_ml_comparison.py` (hash-gated;
  two predeclared fits; frozen configs; no installs — sklearn 1.9.1
  already present). Integrity gates passed; both models fit on the same
  700 rows, scored the same 331 rows once.

## Commands actually run

1. Source/hash/count verification (read-only, metadata).
2. `.venv\Scripts\python.exe .../task169/run_task169_ml_comparison.py`
   → executed **exactly once** (log: `169_execution_log.txt`).

## Results (single run)

RF test AUC **0.4865** CI [0.4240, 0.5478], permutation p 0.659,
AP 0.5945 (baseline 0.5801), Brier 0.2513. SVM test AUC **0.4802**
CI [0.4177, 0.5426], p 0.732, AP 0.5753. Logistic reference (TASK152):
0.5278 [0.466, 0.594], p 0.204. Neither model met the predeclared
pattern rule (credible + materially different); both AUCs below chance
are noise, not invertible signal. **Predictive-model branch closes: no
further estimators.**

## Manifest (verified after all edits)

| Deliverable | Size / SHA-256 |
|---|---|
| `169_nonlinear_ml_protocol.md` | 7907 B / `159b84f19d609dbbf29c6474a5461c8ae66f5a05fb121b33944840d44aa72b05` |
| `run_task169_ml_comparison.py` | 7519 B / `3249593add91a0fc4ec6107047760d474c5a5fd20ab1e02bbc7871636d76099c` |
| `169_model_results.json` | 2553 B / `170866db6223d3c1d32f5840ce17ea0486ddfe6beba0d6c5f6447ca52c4430b5` |
| `169_test_predictions.csv` | 22,764 B / `adc6a2fa1c8223d1dbfa4e1a038d45bf7c480c41d474a4ae51d4ab0d70c22a38` |
| `169_ml_comparison_report.md` | 4240 B / `88291f45a6ac2a30427815809cec6fb2b6d4531d2ead64f128601dd3c42e2a8f` |
| `169_execution_log.txt` | 984 B / `5f689c5d2f19e06c921967be6fc401985beb9bef62239c14effdfe395a91d6c6` |
| `169_task_report.md` (this file) | digest in the TASK169 completion message |

## Final verdict

**`NO_NONLINEAR_ADVANTAGE_OBSERVED`** — both models ran; metrics as
above; no materially different pattern vs logistic; branch closed.

## Actions NOT performed

No tuning/grid/random search, ensembles, threshold optimization, or
third estimator; no feature/label/split/inclusion changes; no package
installation; no new data collection or downloads; no holdout beyond
the TASK152 test partition; no formal significance test vs logistic
(no saved predictions existed); no strategy backtest, S2 modification
(its INCONCLUSIVE closure stands), deployment, or trading; no
governance edits — Research Capacity **HOLD** and Active Research
**NONE verified unchanged**; no commit, no push. TASK170 not begun.
