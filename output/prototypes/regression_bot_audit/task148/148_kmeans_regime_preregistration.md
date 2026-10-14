# TASK148 — K-Means Volatility-Regime Study: Preregistration (DESIGN ONLY)

**Status:** bounded preregistration, NOT AUTHORIZED FOR EXECUTION. No
measurement performed. B4/COMP-01 untouched (descriptive study, no
strategy, no comparator). HOLD/NONE unchanged by this document.

## 1. Research question

Are volatility regimes identifiable and sufficiently stable across time
and symbols (11-symbol FX/metals/crypto panel) to justify further
research? A stability verdict only — never a trading signal.

## 2. Data contract (metadata-verified, values untouched)

- Panel: 11 files `_t37_m1_{SYM}.npz`, M1 OHLC+spread, row counts
  verified this session (executor re-verifies exactly, mismatch → STOP):
  AUDNZDm 2132968; BTCUSDm 3017792; ETHUSDm 3017787; EURGBPm 2120964;
  EURUSDm 2120306; GBPUSDm 2125500; USDJPYm 2126055; USOILm 1994318;
  USTECm 1970042; XAGUSDm 2009865; XAUUSDm 2029174. H4 files
  (`_t37_h4_{SYM}.npz`, ~9049–12582 rows) NOT used (daily grid derives
  from M1). adxcache files NOT used (see exclusion below).
- Fields used: time/open/high/low/close/spread (all present; verified by
  key listing). NO volume column exists in any file — volume-rate
  features are EXCLUDED as unavailable (evidence, not choice).
- adxcache files (closed_adx/forming_adx/atr_*) EXCLUDED entirely (ADX =
  trend indicator; ATR bundled with closed-breakout context).
- Coverage per task51 §11 record: 2021-01→2026-10; executor verifies and
  reports actual span pre-use (timestamps are epoch-ns ints; UTC
  interpretation predeclared; parse failure → STOP). No reference SHA
  exists on record — executor computes and records SHA pre-use (baseline
  establishment, not match-verification).
- Missing: days with zero M1 bars excluded + counted; no fill. No holdout
  exists for this panel; none claimed.

## 3. Features (frozen set; OHLC+spread only)

Daily grid from M1 bars. Per day per symbol: (1) realized variance = sum
of squared M1 log returns, log-scaled; (2) Parkinson range estimator
from daily high/low/close; (3) vol-of-vol = 20-day rolling std of log
realized variance; (4) spread level = daily mean spread, as 20-day
rolling percentile rank. Normalization: per-symbol z-score using
TRAINING-segment mean/std ONLY (fitted pre-validation, frozen).
FENCED OUT: returns/slopes/MA positions/breakouts/session or calendar
dummies/ADX/ATR-triggers/any closed-signal construct.

## 4. Leakage prevention

All scaling parameters (z-score means/stds, percentile windows are
rolling-causal by construction) fitted on TRAIN ONLY. Centroids fitted on
TRAIN ONLY; validation/test points assigned to frozen centroids (no
refit). Chronological segments: TRAIN 2021-01→2023-12, VALIDATION
2024-01→2024-12, TEST 2025-01→panel end. Future observations never
influence past assignments (pointintime leakage checks applied).

## 5. K-means configuration (bounded, no search)

k ∈ {2, 3} only (2 = calm/stressed minimal; 3 = low/medium/high).
scikit-learn KMeans, kmeans++ init, n_init=10, seeds 0–9, deterministic
(first lowest-inertia wins); executor verifies sklearn import pre-run
else STOP. Pooled panel (all symbols' daily vectors). No other k, no
other algorithm, no reseeding on failure.

## 6. Stability evaluation (mechanism, not returns)

(a) Centroid-mapping ARI: fit on VALIDATION separately → Hungarian-match
to TRAIN centroids → ARI(validation own-fit labels, validation mapped
labels); same TRAIN→TEST. (b) Persistence: mean dwell time in days per
regime (descriptive). (c) Prevalence: each regime's share of TEST
assignments. (d) Null reference: time-permuted labels → ARI expected ≈ 0
(proves the metric is not vacuous). Genuine stability (persistent,
prevalent, cross-window agreement) distinguished from merely obtaining
clusters (any k-means returns labels — the bars below decide).

## 7. Baselines

(1) Non-clustering volatility-binning reference: pooled-vol tertile split
(deterministic, no fitting) evaluated on the same stability metrics.
(2) Shuffled/null reference per §6(d). Clusters must beat BOTH to matter.

## 8. Decision rules (thresholds PROPOSED with rationale, not evidence)

- CONTINUE: ARI(train→validation) ≥ 0.5 AND ARI(train→test) ≥ 0.5 AND
  every regime ≥ 10% of TEST assignments AND null ARI < 0.2. Rationale:
  0.5 = conventional moderate-agreement boundary; 10% guards degenerate
  single-cluster solutions; null check validates the metric.
- FAIL: ARI < 0.3 on either mapping OR any regime < 5% (degenerate).
- INCONCLUSIVE: anything between. No rescue, no re-fit, no k change.

## 9. Resource limits

Max configurations: 2 (k=2,3) + 2 baselines + 1 null = 5 fits, single
measurement run, minutes of compute on 11 H4/daily-scale frames. Stops:
hash/count/parse mismatch, budget exhaustion, integrity failure,
completion → bounded report, no continuation. No sweeps, reruns, variants.

## 10. Interpretation boundary

No strategy selection, trading-rule design, candidate registration,
execution, deployment, or profitability claim — in ANY outcome, including
CONTINUE (which recommends only a follow-on sizing-rule DESIGN task with
its own authorization). Regimes are market descriptions, not signals.

## 11. Gates before any execution

Approval → filed preregistration (THIS version) → review → synthetic
self-test of the pipeline (synthetic OHLC only) → execution gate (hashes/
counts/parse re-verified, sklearn import verified) → ONE bounded run →
bounded report. Each gate independent; approval skips none.
