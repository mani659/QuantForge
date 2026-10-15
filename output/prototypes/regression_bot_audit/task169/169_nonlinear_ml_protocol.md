# TASK169 — Nonlinear ML Comparison Protocol (locked before any model fitting)

## 1. Scope source

Owner request recorded in the TASK169 instruction (bounded comparison of
Random Forest and RBF SVM on the existing `_t39` data, following the
technical-owner recommendation). Recorded as the task-specific scope
source; no signature fabricated. Exactly two predeclared models; no
discovery sweep.

## 2. Verified inputs (Phase A, from source artifacts — metadata only)

- Data: `output/prototypes/fx_h4inv_adx_prep/_t39_baskets_forensics.jsonl`
  — 1,933,160 B, SHA-256
  `e2fa81737f9264798baf0c4964084ccb73c7230751f58e43c1975e34f888dc97`,
  **1031 rows** (matches TASK152).
- Target: `outcome`, 1 = recover / 0 = fail — **1 (651) / 0 (380)**,
  matches TASK152; consistently defined across all rows.
- Predictors (the exact TASK152 four): `adx_base`, `atr_base`,
  `spread_base_pips` (continuous), `dir` (±1 as stored, values {−1, 1},
  no encoding choice). **Zero missingness** in all four (verified).
  Pre-entry status: TASK152's frozen audit states all four are "measured
  at or before base entry"; field semantics corroborate (base-entry-time
  measurements; all `*_addon*`, `adverse_pre_*`, `time_to_addon_h`,
  `vwap_dist_*`, `t_*_s`, `*_touched`, `max/min_post_pnl`,
  `killed_before_recovery`, `cap_*`, `hour`, `sym`, `fx` excluded as
  post-entry/irrelevant — NOT used here either).
- Split (chronological, exactly as TASK152): train `year ∈ [2021, 2024]`
  → **700 rows / 241 fails**; test `year ∈ [2025, 2026]` →
  **331 rows / 139 fails**. Verified identical to TASK152 — no
  discrepancy, no reconciliation needed. `basket_id` unique (row
  identifier available).
- Prior logistic reference (TASK152, historical only): test AUC 0.5278,
  bootstrap 95% CI [0.466, 0.594], permutation p = 0.204, verdict FAIL.
  No saved TASK152 predictions exist (task152 dir contains only the
  report) → **no formal paired test vs logistic is admissible**;
  logistic appears as descriptive reference only.
- Environment: sklearn 1.9.1, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1
  already installed. No packages to be installed.

## 3. Closure-rule check (required stop-condition analysis, recorded before fitting)

- **§99.1 protected families:** predictive-model/logistic diagnostics are
  NOT among the listed families → no family re-research bar triggered.
- **No formal closure record** exists for this branch (no
  `rescue_authorized: false`, no `can_be_reopened: NO` marker — contrast
  MDP-001, CAND-025, RS-404, PROTO-TREND-001, which carry explicit
  closure records). TASK152 verdict = FAIL with recommendation: any
  further work must be "a new, separately authorized question — not a
  re-cut of this one." This task is that separately owner-requested
  question (estimator-class adequacy), and is not a re-cut: logistic is
  NOT refit; features, target, split, and inclusion rules are unchanged.
- **Textual tension, disclosed:** TASK152's frozen protocol decision
  rules end with "Test partition never reused." That line sits inside
  TASK152's own decision loop alongside "No refit, threshold change,
  feature change, or split change after seeing results" — i.e., it bars a
  second bite **within that diagnostic**. The ratifying owner has now
  explicitly directed this follow-up on that same split (TASK169 scope:
  "the existing chronological 700/331 split, once verified") with the
  prior examination disclosed and results mandated **exploratory and
  non-confirmatory regardless of score** (§5 of the task). Recorded here
  rather than silently reinterpreted: reuse of an already-examined test
  partition is exactly why confirmatory force is stripped by task
  mandate, no model may be selected on score, and the branch closes
  below if the predeclared pattern rule is not met. The comparison is
  structurally incapable of manufacturing a "win" that rescues the
  closed-fail logistic result.
- **§99.3/§99.4 (HOLD/NONE):** stand unchanged; this is a narrowly
  scoped, owner-requested diagnostic of the same class as TASK151/152
  (which fitted under task-specific authorization). Not research
  reactivation; no candidate, no registration, no backtest.

**Gate: no authoritative rule explicitly prohibits this comparison →
execution permitted.** (The tension in §3 is reported, not bypassed.)

## 4. Fixed models (no search, no tuning — exactly two fits)

**Model A — Random Forest**
`RandomForestClassifier(n_estimators=500, max_depth=4,
min_samples_leaf=25, max_features="sqrt", class_weight=None,
random_state=20261015, n_jobs=1)`. Input: the 4 raw predictors (trees
need no scaling; no other preprocessing). Config per task; not varied.

**Model B — RBF SVM**
`Pipeline([StandardScaler(), SVC(kernel="rbf", C=1.0,
gamma="scale", class_weight=None)])`; scaler fit on TRAIN only; ranking
from `decision_function`. Implementation note: `probability=False`
(default) — no Platt scaling (would be an extra fitting step, not
authorized); therefore SVM outputs are decision scores, not
probabilities (see metric rules).

Both fit once on the same 700 train rows; each evaluated exactly once
on the same 331 test rows. No refit on test, no CV, no second split,
no threshold optimization (no classification statistics reported).

## 5. Evaluation rules (fixed before fitting)

- **Primary:** test ROC-AUC per model (ranking metric).
- **Secondary (descriptive):** average precision (PR-AUC) per model;
  test prevalence (failure rate) for context.
- **Brier score:** reported for Random Forest only (its `predict_proba`
  is a valid model output for a proper scoring rule). OMITTED for SVM by
  pre-declaration: decision scores are not probabilities; calibrating
  would add an unauthorized fitting step. No log-loss for SVM either.
- **Uncertainty (TASK152 method, comparable metric):** bootstrap 95% CI
  over test rows, 2000 resamples, seed 20261014; resamples lacking both
  classes are redrawn (count recorded).
- **Null (TASK152 method):** permutation of test labels against fixed
  scores, 1000 shuffles, seed 20261015; p = fraction with AUC ≥ observed.
- **Multiplicity (two predeclared comparisons):** raw p reported per
  model plus Bonferroni-adjusted criterion p < 0.025. Results remain
  non-confirmatory regardless (task mandate).
- **Known dependence limitation (restated from TASK152, not corrected
  post hoc):** ~14 baskets/month are within-month correlated; row-level
  bootstrap precision may be overstated.
- **Historical reference:** logistic AUC 0.5278 [0.466, 0.594], p 0.204
  — descriptive only; no formal difference test (no saved predictions).
- **Interpretation rule (fixed before fitting):** a model shows a
  "credible and materially different predictive pattern" iff
  (1) bootstrap CI lower bound > 0.5 AND multiplicity-adjusted
  permutation p < 0.025 [credible], AND (2) test AUC differs from the
  logistic reference 0.5278 by ≥ 0.05 [materially different]. Else the
  predictive-model branch closes with no further estimators. This is a
  predeclared descriptive classification aid — not an economic threshold
  and not a promotion criterion. No model may be selected for further
  work solely for the higher score of the two.
- **Prediction outputs:** CSV of scored test rows with `row_index`
  (0-based jsonl line), `basket_id`, `year`, `outcome`, `rf_prob`,
  `svm_decision` for audit.

## 6. Stop conditions (in force)

Stop before fitting if: data hash ≠ `e2fa8173…`; row/split/outcome
counts ≠ TASK152; any of the four predictors missing/unverifiable as
pre-entry; a closure rule conflict; package install or data acquisition
required. During execution: fix only ordinary implementation defects
within the frozen configuration — no hyperparameter, feature, label, or
split changes; a failure that cannot be fixed within config → report as
execution failure, no rerun shopping.
