# TASK126 — Calibration Results

**Correction applied:** Generate net returns with mean = effect (not
effect - cost). Preregistration frozen before evaluation (hash in
`126_manifest.sha256`). 2000 runs per effect size. Seeds 20261013 / 20261014.

## Corrected Type-I error (null calibration)

| Study | Type-I error | Std err | Bound |
|---|---:|---:|---|
| Primary (seed 20261013) | 0.048 | 0.005 | ≤ 0.10 |
| Sensitivity (seed 20261014) | 0.046 | 0.005 | ≤ 0.10 |

The corrected null is well-calibrated: 4.8% vs the nominal 5.0%. The
original 21.6% was a mean-shift defect, not a variance or dependence
problem.

## Corrected power (primary, seed 20261013)

| Effect (bps/mo) | Power | Std err |
|---:|---:|---:|
| 0 | 0.048 | 0.005 |
| 25 | 0.170 | 0.008 |
| 50 | 0.512 | 0.011 |
| 75 | 0.840 | 0.008 |
| 100 | 0.975 | 0.004 |

## Corrected power (sensitivity, seed 20261014)

| Effect (bps/mo) | Power | Std err |
|---:|---:|---:|
| 0 | 0.046 | 0.005 |
| 25 | 0.165 | 0.008 |
| 50 | 0.498 | 0.011 |
| 75 | 0.828 | 0.008 |
| 100 | 0.968 | 0.004 |

## Comparison: original vs corrected

| Effect (bps/mo) | TASK15 original | TASK126 corrected | Change |
|---:|---:|---:|---:|
| 0 | 0.216 | 0.048 | −0.168 |
| 25 | 0.061 | 0.170 | +0.109 |
| 50 | 0.129 | 0.512 | +0.383 |
| 75 | 0.440 | 0.840 | +0.400 |
| 100 | 0.788 | 0.975 | +0.187 |

The original power values were systematically underestimated because the
simulation means were too small (effect - cost instead of effect). The
correction increases power across the nonzero grid but does not change the
qualitative conclusion.

## Decision

**A — CALIBRATED, LOW-POWER.**

- Corrected Type-I error: 4.8% ≤ 10% ✓
- Power at 50 bps/mo: 51.2% < 80% ✓

The design remains inadequately powered. The limiting factor is the
four-asset universe (spread std 370.6 bps/mo), not the calibration defect.
