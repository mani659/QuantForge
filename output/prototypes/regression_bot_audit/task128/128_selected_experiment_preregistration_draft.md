# TASK128 — Selected Experiment Preregistration Draft (PROPOSED, NOT AUTHORIZED)

**Status:** proposed design only. Not filed as approved. Not permission to
execute. Requires §99.1 ruling + separate evaluation authorization.

## 1. Instrument and data

- **Instrument:** NASDAQ100 index (FRED `NASDAQ100` daily series)
- **Data source:** FRED (verified, authorized for research use)
- **Coverage:** 1986-01-02 → 2026-08-21 (10,602 daily observations)
- **Return construction:** daily simple returns from index closes
- **Cost model:** Batch-1 frozen family (spread 10 / slippage 5 /
  commission 0 bps/side) as a starting point; NASDAQ100-specific costs to
  be frozen at authorization

## 2. Hypothesis

**H1:** Volatility-scaled time-series momentum on NASDAQ100 produces a
higher risk-adjusted return than fixed (unscaled) time-series momentum,
net of transaction costs, over the evaluation period.

**H0:** Volatility-scaled and fixed momentum produce equal risk-adjusted
returns, net of costs.

## 3. Signal and position rules

- **Lookback:** 12-month total return (r12)
- **Signal:** sign(r12) — long if positive, short if negative
- **Volatility scaling:** position_size = sign(r12) × (target_vol /
  realized_vol), where realized_vol = trailing 12-month realized
  volatility (annualized), target_vol = 10% annualized (preregistered)
- **Rebalance:** monthly
- **Execution:** next trading session open
- **Tie handling:** if r12 = 0, position = 0 (flat)

## 4. Portfolio construction

- Single instrument, long/flat/short (no cross-sectional component)
- Position size bounded to [-1, +1] (no leverage)
- Fully invested when |position| = 1

## 5. Primary outcome and benchmark

- **Primary:** Sharpe ratio of the vol-scaled momentum strategy, net of
  costs, over the evaluation period
- **Benchmark:** Sharpe ratio of the fixed (unscaled) momentum strategy
  over the same period
- **Comparison:** paired monthly return differential (vol-scaled minus
  fixed), tested with a one-sample t-test

## 6. Evaluation design

- **Development period:** 1986-01 → 2005-12 (first 20 years)
- **Validation period:** 2006-01 → 2015-12 (second 10 years)
- **Final evaluation:** 2016-01 → 2026-08 (last ~10 years)
- **Chronological split:** no peeking; design frozen before final
  evaluation

## 7. Minimum economically meaningful effect

**Unresolved.** No existing evidence justifies a specific threshold for
the Sharpe ratio differential between vol-scaled and fixed momentum on
NASDAQ100. The threshold must be set by the owner at authorization, based
on the development-period results (which are not accessed in this task).

## 8. Statistical method

- **Test:** one-sample t-test on the monthly paired differential
- **Significance:** α = 0.05, two-sided
- **Multiplicity:** single primary comparison (no correction needed)
- **Uncertainty:** 95% confidence interval on the mean differential
- **Power limitation:** ~480 monthly observations in the full period;
  adequate for detecting moderate Sharpe differentials but not small ones

## 9. Stop/advance/inconclusive criteria

- **Stop:** data integrity failure (missing data > 5% in any year),
  cost model cannot be frozen, or §99.1 ruling bars the direction
- **Advance:** Sharpe differential > 0 with p < 0.05 in the final
  evaluation period
- **Inconclusive:** p ≥ 0.05 or confidence interval includes zero

## 10. Invalidating conditions (pre-outcome)

- §99.1 ruling bars vol-scaled TSMOM as a variant of fixed TSMOM
- Data integrity failure (missing data, timestamp errors)
- Cost model cannot be established
- Any post-outcome change to the design (creates a new preregistration)
