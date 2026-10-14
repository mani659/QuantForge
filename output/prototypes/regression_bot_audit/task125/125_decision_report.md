# TASK125 — Decision Report

## Classification: B. LOW-POWER

The 4-asset XSM design cannot reliably distinguish even a large (100
bps/month) cross-sectional momentum effect from noise and realistic
transaction costs with the available SPY/VEU/AGG/BIL panel and ~216 monthly
observations.

## Evidence summary

- Power at 50 bps/mo: 12.9% (target: 80%)
- Power at 100 bps/mo: 78.8% (target: 80%)
- False-positive rate: 21.6% (target: ≤5%)
- XSM spread std: 370.6 bps/mo — the binding constraint

## Limiting factor

**The four-asset universe.** The cross-sectional spread in a 4-asset panel
has a standard deviation of 370.6 bps/month — an order of magnitude larger
than the economically meaningful effect range (25-100 bps/month). No
inferential method, sample extension, or cost reduction within the current
data universe can overcome this. The Task-63 calibration's verdict (the
detect region requires Sharpe ≳1.5 sustained; this design offers ≈0.07)
generalizes directly.

The sample length (~216 months) and cost assumptions (30 bps round-trip)
are secondary: even with zero costs and infinite sample size, the 4-asset
cross-sectional spread is too noisy to detect modest effects. The limiting
factor is structural, not statistical.

## Single recommended next action

**Do not spend a bounded empirical research cycle on the 4-asset XSM
design.** The power study demonstrates it is structurally underpowered.
The recommended next action is to either:

1. **Acquire a broader cross-sectional data universe** (a verified
   multi-stock panel with ≥50 assets, compatible return construction, and
   realistic cost treatment) and re-run this power study, OR
2. **Select a different hypothesis-testing direction** that does not
   require a broad cross-sectional universe.

This recommendation is a detectability verdict, not a profitability
claim. The XSM mechanism may or may not be real; this study shows it cannot
be tested with the current data.

## Is an empirical strategy test justified?

**No.** The power study shows the design is structurally underpowered.
Committing a bounded research cycle would produce an inconclusive result
regardless of whether a true effect exists. The cycle would be wasted.

## TASK125 authorization boundary

TASK125 authorized this power study only. It does not authorize any
subsequent strategy backtest, candidate creation, parameter optimization,
or governance change. Any empirical test of the XSM design — or any
replacement direction — requires a separate explicit owner authorization.
