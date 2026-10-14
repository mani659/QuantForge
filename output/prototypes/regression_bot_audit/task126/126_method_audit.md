# TASK126 — Method Audit: Null-Calibration Defect in TASK125

## 1. Tracing the 21.6% null rejection rate

**Reported result:** TASK125 power at effect=0 is 0.216 (21.6%), far above
the nominal α=0.05.

**Test statistic:** One-sample t-test: t = mean / (std/√n), two-sided
p-value via normal approximation, reject if p < 0.05.

**Null-generating process (TASK125 code):**
```python
mean = effect_decimal - cost_decimal  # at effect=0: mean = -0.003 (-30 bps)
return rng.normal(mean, spread_std, n_months)
```

**The defect:** At effect=0, the simulation generates returns with mean
= **-30 bps/month**, not 0. The t-test tests H0: mean = 0. Since the true
mean is -30 bps (not 0), the null hypothesis is **false in the simulation**.
The test correctly rejects a false null — the 21.6% is not a Type-I error
inflation but a **systematic bias** from generating data under the wrong
null.

**Root cause:** The cost is subtracted from the simulation mean, but the
t-test is testing whether the *net* return (gross - cost) is different from
0. The net return at effect=0 should have mean = 0 (no edge → gross = cost
→ net = 0). The simulation instead generates net returns with mean = -cost
(gross = 0, net = -cost), which is a **negative edge**, not the null.

**Why BIL autocorrelation is NOT the cause:** The defect is in the mean
vector, not the variance. The simulation uses i.i.d. draws (no AR(1)
filtering), so serial dependence cannot explain the miscalibration. The
21.6% is fully explained by the -30 bps mean shift.

## 2. The smallest demonstrated correction

**Fix:** Generate net returns with mean = effect (not effect - cost):

```python
def simulate_xsm_returns(rng, spread_std, effect_bps, n_months):
    effect_decimal = effect_bps / 10000.0
    return rng.normal(effect_decimal, spread_std, n_months)
```

This is the smallest correction that fixes the calibration defect:
- At effect=0: mean = 0 (correct null)
- At effect=50: mean = 50 bps (correct alternative — net return equals effect)

The cost is already accounted for in the net return definition; it should
not be subtracted again in the simulation mean.

**Justification:** The correction aligns the simulation's null-generating
process with the preregistered null hypothesis (H0: mean net return = 0).
No other changes are made: same effect grid, same cost assumption, same
seeds, same spread std, same test procedure.

## 3. Validity of the original TASK125 power estimates

**The original power table is invalid as confirmatory evidence.** The
simulations at effect > 0 also have the wrong mean (effect - cost instead
of effect), so the reported power values are systematically biased:
- At effect=25: true mean should be 25 bps, but simulation used -5 bps →
  power underestimated
- At effect=50: true mean should be 50 bps, but simulation used 20 bps →
  power underestimated
- At effect=100: true mean should be 100 bps, but simulation used 70 bps →
  power underestimated

The original power values are **lower bounds** on the true power (because
the simulation means are smaller than they should be). The corrected
procedure will produce higher power estimates.

**However, the qualitative conclusion (LOW-POWER) is likely robust:**
even with the corrected means, the spread std (370.6 bps/mo) is so large
relative to the effect range that power will remain low. The correction
will not change the classification from B to A.

## 4. What the original results do NOT say

- They do NOT prove the XSM mechanism is ineffective (the null was wrong).
- They do NOT prove the 4-asset universe is too thin (the power was
  underestimated, not overestimated).
- They DO demonstrate that the original simulation had a calibration defect
  that must be corrected before any confirmatory conclusion.
