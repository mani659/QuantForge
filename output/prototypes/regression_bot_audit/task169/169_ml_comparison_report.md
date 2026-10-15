# TASK169 — Nonlinear ML Comparison Report (RF vs RBF SVM on `_t39`)

**Final verdict: `NO_NONLINEAR_ADVANTAGE_OBSERVED`** — both models ran
exactly once under the pre-fit-locked protocol
(`169_nonlinear_ml_protocol.md`, SHA-256 `159b84f19d…44aa72b05`).

## 1. Results (test partition 2025–2026, n = 331, 139 fails)

| Model | Test ROC-AUC | 95% bootstrap CI¹ | Permutation p² | Avg precision³ | Brier |
|---|---|---|---|---|---|
| Random Forest (frozen config) | **0.4865** | [0.4240, 0.5478] | 0.659 (bonf. 1.0) | 0.5945 | 0.2513 |
| RBF SVM (decision function) | **0.4802** | [0.4177, 0.5426] | 0.732 (bonf. 1.0) | 0.5753 | omitted⁴ |
| Logistic, TASK152 (historical ref.) | 0.5278 | [0.466, 0.594] | 0.204 | — | — |

¹ 2000 row-bootstrap resamples, seed 20261014 (0 discarded redraws).
² 1000 test-label shuffles, seed 20261015; multiplicity: two
predeclared comparisons, Bonferroni criterion p < 0.025.
³ AP positive class = recover (1); test recover prevalence 192/331 =
0.5801 = no-skill baseline. ⁴ Decision scores are not probabilities
(pre-declared omission; calibrating would be an unauthorized fit).

## 2. Sample accounting and integrity

1031 baskets verified against source hash `e2fa8173…`; outcome
1 = 651 / 0 = 380; four predictors (`adx_base`, `atr_base`,
`spread_base_pips`, `dir`) with zero missingness, all pre-entry
(TASK152 audit); chronological split reproduced exactly: train
2021–2024 = 700 rows / 241 fails, test 2025–2026 = 331 / 139; **0
excluded rows**; both models fit on the identical 700 rows and scored
the identical 331 rows once. Environment sklearn 1.9.1 / numpy 2.4.6
(pre-existing; nothing installed). Failure prevalence test = 41.99%.

## 3. Interpretation (predeclared rule, applied as written)

Pattern requires BOTH [credible: CI lower > 0.5 AND Bonferroni p < 0.025]
AND [materially different: |AUC − 0.5278| ≥ 0.05]:

- RF: not credible (CI straddles 0.5, p = 0.659); not materially
  different (Δ = 0.041). SVM: not credible (p = 0.732); not materially
  different (Δ = 0.048).
- Both AUCs sit slightly *below* chance — **noise, not invertible
  signal**: both CIs include 0.5, permutation tests far from
  significant, and inverting scores after seeing results would be
  exactly the post-hoc mining the protocol forbids. No threshold
  statistics are reported (none was ever frozen).
- Conclusion: neither fixed nonlinear estimator recovered predictive
  ranking information that the logistic model missed — if anything both
  ranked marginally worse, within noise. **The predictive-model branch
  closes here: no further estimators, no additional probes**
  (protocol §5; task §6 rule 1).

## 4. Limitations (binding on interpretation)

- **Exploratory and non-confirmatory regardless of score** (task
  mandate): the 2025–2026 partition was already examined for logistic —
  it is not an untouched holdout. Even a high score here could not
  validate an edge; the scores are in fact null.
- The TASK152 test-partition reuse tension was disclosed pre-fit in the
  protocol (§3); confirmatory force was stripped by construction (no
  model selection on score, branch-closure rule, fixed configs).
- Within-month basket dependence (~14/month): row-level bootstrap CIs
  may overstate precision — restated from TASK152, not corrected post
  hoc.
- No formal difference test vs the logistic reference (no saved TASK152
  predictions exist → none admissible).
- Predictive discrimination ≠ decision usefulness ≠ net trading
  economics; nothing here supports any strategy claim. RF Brier 0.2513
  vs prevalence-based reference 0.2460 (p(1−p) at 0.5801) shows no
  probabilistic skill either.

## 5. Non-effects confirmation

No tuning/grid search/ensembles/threshold optimization; no feature,
label, inclusion, or split changes; no new data or downloads; no
holdout beyond the TASK152 test partition; no strategy backtest,
paper/live trading, or deployment; **S2 untouched** (its preregistered
INCONCLUSIVE verdict stands, line closed); no governance edits;
Research Capacity **HOLD** and Active Research **NONE unchanged**; no
commit, no push. No model selected for further work (neither qualifies,
and score-ranking selection is barred).
