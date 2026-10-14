# TASK126 — Calibration Correction Preregistration (FROZEN before evaluation)

**Status:** FROZEN before any corrected-effect measurement. Hash recorded in
`126_manifest.sha256`.

## 1. Correction being applied

The smallest demonstrated calibration defect in TASK125 (method audit §2):
the simulation generated net returns with mean = effect - cost instead of
mean = effect. At effect=0, the true mean was -30 bps (not 0), making the
null hypothesis false in the simulation and inflating the rejection rate to
21.6%.

**Corrected simulation:**
```python
def simulate_xsm_returns(rng, spread_std, effect_bps, n_months):
    effect_decimal = effect_bps / 10000.0
    return rng.normal(effect_decimal, spread_std, n_months)
```

At effect=0: mean = 0 (correct null). At effect>0: mean = effect (correct
alternative — net return equals the effect, cost already netted).

## 2. Preserved from TASK125 (no changes)

- Effect grid: {0, 25, 50, 75, 100} bps/mo
- Cost assumption: 30 bps round-trip (Batch-1 frozen)
- Spread std: estimated from real data (370.6 bps/mo)
- Seeds: 20261013 (primary), 20261014 (sensitivity)
- Run count: 2000 per effect size
- Test: one-sample t-test, normal approximation, α=0.05
- Sample: 216 months

## 3. Decision rules (frozen)

- **A — CALIBRATED, LOW-POWER:** corrected Type-I error ≤ 10% AND power
  at 50 bps/mo < 80%
- **B — CALIBRATED, TESTABLE:** corrected Type-I error ≤ 10% AND power
  at 50 bps/mo ≥ 80%
- **C — UNRESOLVED:** corrected Type-I error > 10% OR power cannot be
  estimated

## 4. Validation sequence (frozen)

1. Run corrected null (effect=0), 2000 runs, seed 20261013
2. Check Type-I error rate: must be ≤ 10% (allowing for normal-approximation
   error at df=215)
3. If Type-I error > 10%: stop, classify C
4. If Type-I error ≤ 10%: run corrected power grid {25, 50, 75, 100}
5. Classify A or B based on power at 50 bps/mo

No post-outcome amendments. Any change creates a new preregistration.
