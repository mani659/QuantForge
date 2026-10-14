# TASK124 — Experiment Selection Decision

**Decision: C. Defer experiment selection.**

## Rationale

The TASK123 proposal (pure cross-sectional momentum on SPY/VEU/AGG/BIL) is
**genuinely distinct** from every closed candidate (overlap matrix:
materially overlapping with GEM's relative leg but distinct testable
prediction; genuinely distinct from MDP-001/VM/TOM/REBAL/CORR). The
distinction is mechanistic, not nominal.

However, the proposal fails the informativeness test for a decisive reason:

**The 4-asset cross-sectional universe is orders of magnitude thinner than
what cross-sectional momentum requires, and the Task-63 calibration report
establishes that the pipeline's detection gates demand hedge-fund-outlier
effects (Sharpe ≳1.5 sustained) with power ≈ 0 across the plausible range
for normal mechanisms.**

Spending a bounded empirical research cycle on a 4-asset XSM would likely
produce an inconclusive result regardless of whether a true effect exists —
the design is structurally underpowered for the detection gates, not
merely underpowered in sample size.

## The specific missing fact

The minimum detectable effect (MDE) for a 4-asset cross-sectional momentum
strategy at frozen cost assumptions, given:
- Serial dependence in monthly ETF returns
- The tiny 4-asset cross-section (2-vs-2 comparison)
- The Task-63 detection gates (topology binds first; interior rate ≤10%)
- Realistic turnover and multiple-testing exposure

This MDE **cannot be determined from existing records** — no power study
exists for this design, and running one is prohibited by this task's
restrictions. The Task-63 calibration report provides strong circumstantial
evidence that the MDE exceeds any plausible 4-asset cross-sectional
momentum effect, but circumstantial evidence is not a verified power claim.

## Why not A (retain)?

Retaining the 4-asset XSM would commit a bounded research cycle to a design
that the existing calibration evidence suggests is structurally
underpowered. The distinction from GEM is real but does not overcome the
power deficit. An inconclusive result would waste the cycle and produce no
decisive information.

## Why not B (replace)?

No better-supported, genuinely distinct hypothesis using verified available
resources was identified in the records:
- M1 FX cross-sectional momentum: thinner universe (7 assets), shorter
  history (~5 years), different economics
- Volatility forecasting: related to VM (closed) but the distinction is
  subtle and the power question is equally unresolved
- Any regression concept: barred (R1/R2 excluded, MDP closed)
- Any allocation variant: MDP/REBAL/CORR all closed on the same panel

The evidence is insufficient to identify a replacement that is clearly
more informative than the 4-asset XSM.

## Largest unresolved risk

The 4-asset XSM might actually be detectable if the cross-sectional
momentum effect in US equities is strong enough to overcome the tiny
universe. The Task-63 calibration was run on a different family (MDP
allocation), not on cross-sectional momentum specifically. The
extrapolation to XSM is conceptual, not verified. If the effect is strong,
the proposal would be informative; if modest, it would be wasted.

## Exact authorization needed before any empirical work

1. **Power study authorization** (to establish the MDE for the 4-asset
   XSM before committing a bounded cycle), OR
2. **Broader data universe** (a verified multi-stock cross-sectional panel
   with compatible return construction and realistic cost treatment), OR
3. **Owner decision to proceed despite the power concern** (accepting the
   risk of an inconclusive result).

None of these is available under the current records. TASK124 authorizes
none of them.
