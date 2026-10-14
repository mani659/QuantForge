# TASK152 — Leakage-Safe Logistic Diagnostic on _t39 Closed-Trade Records

| Field | Value |
|---|---|
| Task ID (inferred) | TASK152 |
| Directory | output/prototypes/regression_bot_audit/task152/ |
| Mode | Single bounded diagnostic under the cited owner instruction. No execution beyond it. |
| HEAD / branch | 666c1a9 / main (unchanged) |
| Date UTC | 2026-10-14 |

## 1. Feasibility findings
Full detail in the frozen protocol below; key facts verified pre-freeze: 1031 baskets, 2021-2026, outcome 1=recover (651) / 0=fail (380); zero missingness in all candidate pre-entry fields; prior _t39 logit mixed post-entry fields (leakage) while _t24 logit was already clean (hence _t39 selected); chronological split train 2021-2024 (700 rows / 241 fails) vs test 2025-2026 (331 rows / 139 fails); sklearn 1.9.1 specified because statsmodels is absent and installs are prohibited.

## 2. Frozen protocol (locked before any model fitting; hash below)

--- protocol text verbatim ---
# TASK152 — Frozen Diagnostic Protocol (locked before any model fitting)

## Target
`outcome` from `_t39_baskets_forensics.jsonl`: 1 = recover, 0 = fail.
Consistently defined across all 1031 rows.

## Predictors (frozen; all measured at or before base entry)
- `adx_base` (continuous), `atr_base` (continuous),
  `spread_base_pips` (continuous) — standardized with TRAINING means/stds.
- `dir` (±1 as stored) — used as-is, no encoding choice.
Excluded with reason: sym (9 levels → 8 dummies, unnecessary); hour
(24 levels, unnecessary); fx (collinear with sym groups); every
`*_addon*`, `time_to_addon_h`, `adverse_pre_*`, `overshoot`,
`vwap_dist_*`, `max/min_post_pnl`, `t_*_s`, `*_touched`,
`killed_before_recovery`, `cap_*` field (measured at/after addon or exit —
post-entry leakage).

## Split (chronological, frozen)
- Train: year in 2021–2024 (700 rows, 241 fails).
- Test: year in 2025–2026 (331 rows, 139 fails).
- Minimums: test fails ≥ 50 (have 139); train fails ≥ 100 (have 241).

## Model (frozen; available dependency only)
sklearn LogisticRegression(C=1.0, penalty='l2', solver='lbfgs',
max_iter=1000). statsmodels is NOT installed and may not be installed
(task prohibition); sklearn 1.9.1 is installed. Fit on train only.
Non-convergence → run invalid → INCONCLUSIVE with cause recorded.

## Baseline (no model predictions)
Intercept-only: test majority-class rate (accuracy baseline) and AUC 0.5
(constant score) as the chance reference.

## Metric, uncertainty, null (frozen)
- Primary: test-set AUC (roc_auc_score).
- Uncertainty: bootstrap 95% CI over test rows, 2000 resamples, seed
  20261014.
- Null: permutation test, 1000 shuffles of test labels, seed 20261015;
  p = fraction with AUC ≥ observed.

## Decision rules (frozen)
- CONTINUE iff lower 95% CI bound > 0.5 AND permutation p < 0.05.
- FAIL iff valid run completes and criteria not met.
- No refit, threshold change, feature change, or split change after
  seeing results. Test partition never reused.
--- end protocol text ---

Protocol SHA-256 (computed before fitting): 89eb6eedee6ec582d397948511a8dd8f02e221febdcd77b3515533001ed35c3c (2011 bytes). Unaltered after this hash. One environment note, not a deviation: sklearn 1.9.1 emits a FutureWarning that penalty=l2 is deprecated; the specified L2 regularization with C=1.0 was applied as preregistered.

## 3. Execution status and results (single run, per protocol)
Converged: yes (lbfgs, 7 iterations). No refit, no changes. Test AUC = 0.5278; bootstrap 95 percent CI [0.466, 0.594] (2000 resamples, seed 20261014); permutation p = 0.204 (1000 shuffles, seed 20261015). Majority-class rate = 0.5801. Fitted coefficients (train-standardized): adx_base -0.0893, atr_base 0.3120, spread_base_pips -0.4181, dir 0.0084, intercept 0.6485 (reported, not interpreted as strategy inputs). Decision: lower CI bound (0.466) is NOT greater than 0.5; permutation p (0.204) is NOT less than 0.05. Criteria not met.

## 4. Limitations
Within-month basket correlation exists (about 14 baskets/month); the bootstrap CI resamples rows, so precision may be overstated — stated, not corrected post hoc. Classification is not profitability: a positive AUC would not imply net edge after costs, and this null result does not falsify any mechanism. The 2025-2026 test window may differ in regime from training; the chronological split measures exactly that transportability, including its failure. The _t24 records were not modeled (prior clean analysis stands).

## 5. Verdict: FAIL
Valid test, converged, adequate counts, leakage-safe pre-entry predictors, chronological split — and pre-entry information shows no measurable predictive value for basket recovery beyond chance (AUC 0.53, CI straddles 0.5, permutation p = 0.20).

## 6. Recommendation for the next action
None required by this result. The diagnostic answers its question negatively within its preregistered bounds; existing postures (S2, RS-404, CAND-025, HOLD/NONE) are unchanged; no follow-on measurement is proposed. If the owner wants anything further here, the only honest next step would be a new, separately authorized question — not a re-cut of this one.

`	ext
TASK152 COMPLETE — STOP. TASK153 not begun.
`
