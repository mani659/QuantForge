# TASK134 — Statistical-Inference and Power-Limitations Note

## Inference justification

- **Block bootstrap (block 12, B=10000):** monthly paired differentials
  exhibit serial dependence (momentum states persist across months);
  i.i.d. tests would understate uncertainty. Blocks of 12 preserve
  annual autocorrelation structure without parametric assumptions.
- **Percentile interval:** accommodates heteroskedasticity (vol regimes
  change residual variance) without a variance model.
- **One-sided 95% lower bound:** the claim under test is directional
  (vol-scaled beats passive); α=0.05 convention, predeclared.
- **Single comparison:** no multiplicity adjustment needed; any added
  outcome (subperiods, diagnostics beyond the cost grid) is descriptive
  only and labeled non-inferential.
- **Seed 20261014:** arbitrary-but-fixed; recorded so reruns (if ever
  authorized) reproduce exactly.

## Power limitations (honest bounds)

- No power study run (simulation prohibited in this task); no power
  claimed. N≈470 paired differentials is the total information available —
  adequate in principle for moderate effects, inadequate in principle for
  small ones, with the boundary between them owner-definable via a
  magnitude bar (not set here).
- TASK125/126 (4-asset XSM, spread-std-bound) do not transfer: different
  estimand (paired differential vs cross-sectional spread), different
  universe (single index vs 4-ETF panel), different test.
- Serial dependence + heteroskedasticity widen the realized interval
  beyond i.i.d. approximations — the bootstrap accounts for this; naive
  t-tests would not (cf. TASK129 Defect 2, cured here).
- If the interval includes zero, the result is INCONCLUSIVE — not evidence
  of no effect (A12-style power humility applied to this design).
