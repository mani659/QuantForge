# TASK125 — Preregistration: XSM Detectability and Power Study

**Status:** FROZEN before any measurement. Hash recorded below. No
post-outcome amendments permitted.

## 1. Study purpose

Determine whether a four-asset, monthly-rebalanced cross-sectional momentum
(XSM) design can distinguish a genuinely economically meaningful
relative-strength effect from noise and realistic transaction costs with the
available SPY/VEU/AGG/BIL panel. This is a **testability assessment**, not a
strategy validation or profitability demonstration.

## 2. Design under study

- **Universe:** SPY, VEU, AGG, BIL (4 US ETFs)
- **Ranking variable:** trailing 12-month total return
- **Formation period:** 12 months
- **Rebalance:** monthly
- **Portfolio construction:** equal-weight long top-quartile (2 assets),
  short bottom-quartile (2 assets); fully invested long/short
- **Execution timing:** next trading session open (signal at month-end
  close)
- **Tie handling:** if r12 values are equal, rank by ticker alphabetical
  order (deterministic, predeclared)
- **Cost model:** Batch-1 frozen family: spread 10 bps/side, slippage 5
  bps/side, commission 0 bps/side; round-trip = 30 bps on traded notional
- **Sample window:** 2008-05 to 2026-09 (~216 months, matching GEM/VM
  evaluation span)

## 3. Estimand and effect range

**Estimand:** mean net monthly return of the XSM portfolio, in bps/month.

**Economically meaningful effect:** No single threshold is justified from
existing evidence for a 4-asset cross-sectional momentum design. The study
uses a **sensitivity analysis** over a defensible range: δ ∈ {0, 25, 50, 75,
100} bps/month. The range is justified as:
- Lower bound (25 bps/mo): approximately the monthly cross-sectional spread
  documented in broad equity momentum literature, scaled down for the
  4-asset universe
- Upper bound (100 bps/mo): approximately the monthly cross-sectional spread
  documented in broad equity momentum literature without scaling
- The range brackets the plausible effect; no single value is privileged

## 4. Simulation method

**Parametric bootstrap** using real ETF return moments:
- Load SPY/VEU/AGG/BIL daily total-return closes from verified Batch-1 data
- Compute monthly simple returns per asset
- Estimate 4×4 covariance matrix Σ and AR(1) autocorrelation ρ per asset
- Simulate 2000 paths of 216 months × 4 assets:
  - Draw from multivariate normal with covariance Σ
  - Apply AR(1) autocorrelation ρ per asset
  - Inject cross-sectional momentum effect: add δ/2 to the top-2 ranked
    assets' mean returns and subtract δ/2 from the bottom-2 ranked assets'
    mean returns (the injection is applied to the simulation parameters,
    not to the realized returns)
- For each path, apply the XSM ranking rule and compute net monthly returns
  after costs

**Random seeds:** 20261013 (primary), 20261014 (sensitivity). Fixed before
any results are examined.

**Run counts:** 2000 paths per effect size. 5 effect sizes. Total: 10,000
simulated paths.

## 5. Test procedure

For each simulated path:
1. Compute the 216 monthly net returns of the XSM portfolio
2. Compute the one-sample t-statistic: t = mean / (std/√n)
3. Compute the two-sided p-value
4. Apply Holm α=0.05 across the decision family {primary outcome} (single
  comparison, so Holm = Bonferroni = α)

**Power:** fraction of paths with p < 0.05 at each effect size.
**False-positive rate:** power at δ=0.

## 6. Power targets and decision rules

- **Power target:** 80% at the preregistered economically meaningful effect
- **Decision criteria:**
  - **A. TESTABLE:** power ≥ 80% at δ=50 bps/mo (midpoint of the
    defensible range) AND false-positive rate ≤ 5%
  - **B. LOW-POWER:** power < 80% at δ=100 bps/mo (upper bound of the
    defensible range) OR false-positive rate > 5%
  - **C. INDETERMINATE:** neither A nor B is met (power is between 80% at
    δ=50 and 80% at δ=100, or false-positive rate is between 5% and 10%)

## 7. Reproducibility

- Python 3.11.9, numpy 2.4.6, pandas 3.0.6 (repo .venv)
- All random seeds fixed before execution
- All parameters frozen in this document
- No post-outcome amendments

## 8. Prohibited activities

No strategy performance backtest. No parameter optimization. No candidate
creation. No holdout access. No strategy execution. No paper trading. No
deployment. No governance or candidate status changes. No commit or push.

## 9. Hash

sha256 of this file at freeze time: recorded in `125_manifest.sha256`.
