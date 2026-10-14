# TASK126 — Decision Report

## Result: A — CALIBRATED, LOW-POWER

The corrected test controls false positives (Type-I error 4.8%), and the
4-asset XSM design remains inadequately powered (51.2% at 50 bps/mo vs the
80% target).

## Separate conclusions

### Validity of the TASK125 power estimates

**Invalid as confirmatory evidence.** The 21.6% null rejection rate was
caused by a mean-shift defect: the simulation generated net returns with
mean = effect - cost instead of mean = effect. At effect=0, the true mean
was -30 bps (not 0), making the null false in the simulation. The
original power values were systematically underestimated. The corrected
procedure (this task) is the valid basis for any conclusion.

### Detectability under the four-asset design and stated costs

**Inadequately powered.** Even after correction:
- Power at 50 bps/mo: 51.2% (target 80%)
- Power at 100 bps/mo: 97.5% (the upper bound of the defensible range)
- The design can detect very large effects (≥75 bps/mo) but not moderate
  ones (≤50 bps/mo)

The binding constraint is the four-asset universe: spread std = 370.6
bps/mo. With only 4 assets, the cross-sectional spread is an order of
magnitude noisier than the economically meaningful effect range.

### Whether a broader universe is needed

**Yes, for this design.** The 4-asset panel cannot support a testable
cross-sectional momentum study. A broader universe (≥50 assets, verified,
compatible return construction, realistic costs) is required. The
existing verified datasets contain no broad equity cross-section.

### Whether evidence says anything about the strategy's actual
profitability

**Nothing.** This is a detectability assessment, not a profitability
assessment. The LOW-POWER result means the design cannot distinguish a
true effect from noise — it does not mean the effect is absent. The XSM
mechanism may or may not be real; this study cannot answer that question.

## What the correction changes and does not change

**Changes:** The original power table is superseded. The corrected power
values (this task) are the valid estimates.

**Does not change:** The qualitative conclusion (LOW-POWER). The 4-asset
universe is structurally too noisy for this design. No calibration fix,
sample extension, or cost reduction within the current data universe can
overcome this.

## Recommended next action

Do not spend a bounded empirical research cycle on the 4-asset XSM design.
The detectability question is resolved: the design is testable only for
very large effects (≥75 bps/mo) that are implausible for a 4-asset
cross-sectional momentum strategy. Either acquire a broader cross-sectional
universe or select a different hypothesis direction.

TASK126 authorized this calibration audit only. It does not authorize any
subsequent strategy test, broader-universe search, or TASK127.
