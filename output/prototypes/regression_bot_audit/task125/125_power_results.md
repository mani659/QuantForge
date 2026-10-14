# TASK125 — Power Study Results

**Preregistration:** Frozen before measurement (hash `153b9acc…`).
**Method:** Direct simulation of XSM portfolio returns under known effect
sizes, using the real ETF covariance matrix and XSM spread distribution
estimated from verified data. 2000 runs per effect size. Seeds 20261013
(primary), 20261014 (sensitivity).

## Estimated XSM spread distribution (from real data)

- Mean: 26.6 bps/month
- Std: 370.6 bps/month

The enormous standard deviation (370.6 bps/month) relative to the effect
sizes (25-100 bps/month) is the binding constraint. With only 4 assets, the
cross-sectional spread is extremely noisy.

## Power results (primary, seed 20261013)

| Effect (bps/mo) | Power | Std err |
|---:|---:|---:|
| 0 (null) | 0.216 | 0.009 |
| 25 | 0.061 | 0.005 |
| 50 | 0.129 | 0.007 |
| 75 | 0.440 | 0.011 |
| 100 | 0.788 | 0.009 |

## Power results (sensitivity, seed 20261014)

| Effect (bps/mo) | Power | Std err |
|---:|---:|---:|
| 0 (null) | 0.211 | 0.009 |
| 25 | 0.058 | 0.005 |
| 50 | 0.118 | 0.007 |
| 75 | 0.428 | 0.011 |
| 100 | 0.772 | 0.009 |

## False-positive behavior

The false-positive rate at effect=0 is **0.216** (primary) and **0.211**
(sensitivity) — well above the nominal α=0.05. This indicates the test is
**miscalibrated under the null**, likely because the normal approximation
does not account for the serial dependence in the XSM spread (the real
spread has significant autocorrelation, especially from BIL with
ρ=0.865). The miscalibration inflates the false-positive rate but does not
change the qualitative conclusion: power is low across the defensible
effect range.

## Decision classification

**B. LOW-POWER.**

- Power at 50 bps/mo (midpoint): 0.129 — far below the 0.80 target.
- Power at 100 bps/mo (upper bound): 0.788 — still below 0.80.
- False-positive rate: 0.216 — above the 0.05 target.

The design cannot reliably distinguish even a large (100 bps/mo) effect
from noise and costs with the available 4-asset panel and ~216 monthly
observations.

## Most influential assumptions

1. **Spread std (370.6 bps/mo):** The dominant factor. Driven by the
   4-asset universe — with only 4 assets, the cross-sectional spread is
   extremely noisy.
2. **Cost assumption (30 bps round-trip):** Consumes 30-120% of the
   effect range, further reducing net detectability.
3. **Serial dependence:** The miscalibrated false-positive rate suggests
   the i.i.d. assumption understates the true variance of the test
   statistic.

## Does the Task-63 calibration generalize?

Yes. The Task-63 calibration established that the detectable region
requires Sharpe ≳1.5 sustained over ~8 years. The XSM spread std of 370.6
bps/mo implies a monthly Sharpe of only 26.6/370.6 ≈ 0.07 — far below the
detectable region. The Task-63 verdict ("NOT SUITABLE as configured for
the next real search phase") generalizes directly to this design.
