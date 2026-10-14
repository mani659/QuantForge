# VS-TSMOM-01 Repaired Preregistration v3 (COMPLETE, NOT AUTHORIZED FOR EXECUTION)

**Status:** repaired draft incorporating filed COMP-01 (task137,
`1d76fc1c…`) to resolve the TASK136 estimand mismatch. Supersedes v2 as
working paper (v2 preserved as history). NOT filed as approved. NOT
permission to execute. B4 record: task133 (`d1e1a823…`); DISC-022 closed
and untouched except the benchmark-only use expressly permitted by COMP-01.

## Changes from v2 (each with reason)

1. **Primary estimand is now the paired scaled−fixed differential**
   (reason: v2's scaled−passive primary could not answer the B4-approved
   incremental-value question; TASK136 Decision 1). Buy-and-hold demoted
   to secondary inferential comparison D2.
2. **Fixed leg specified as benchmark-only comparator** (reason: COMP-01
   approval): direction = sign(r12) on the IDENTICAL r12 series, constant
   unit size |w|=1, ties flat, same next-open monthly timing, same costs,
   same window, same missing-data rules. Definitional counterpart to the
   scaled leg (constant size vs vol-scaled size, shared 1.0 cap) — not an
   empirical choice. Reported ONLY inside the bounded report; never
   registered, promoted, standalone-evaluated, or reused. DISC-022 closure
   otherwise intact.
3. **Holm across both comparisons added** (reason: required by COMP-01).
   No conflict: v2 set no multiplicity rule (single comparison), so
   nothing is contradicted. Alpha unchanged at 0.05.
4. **Economic bar transferred to the new primary** (reason: same
   convention, new estimand): benefit-to-friction ratio ≥ 2, where benefit
   = mean paired net differential (scaled−fixed) and friction = realized
   monthly cost drag of the scaled leg. Still PROPOSED/owner-confirmable
   (TASK135 Gap-1 status preserved, not upgraded).
5. **No other changes.** Signal, vol estimator, target 10%, timing, ties,
   bounds, fail-closed data rules, cost grid + financing stress, block
   bootstrap (block 12, B=10000, seed 20261014 — carried unchanged),
   single window, index-level claim with tradability caveat, stops,
   non-effects — all carried.

## Frozen decision rules (complete)

- Family D1 (primary, paired scaled−fixed) + D2 (secondary, paired
  scaled−passive), each with one-sided 95% bootstrap lower bound; Holm
  α=0.05 across {D1, D2}.
- PASS: D1 lower bound > 0 (Holm-adjusted) AND benefit-to-friction ≥ 2.
- FAIL: D1 upper bound < 0.
- INCONCLUSIVE: D1 interval includes zero (or ratio bar waived with
  positive point estimate — reported as written).
- D2 reported with Holm-adjusted inference; gates nothing.
- Diagnostics (descriptive, non-inferential): vol-tracking, yearly D1/D2
  breakdowns, turnover, cost grid, financing stress.
- Stops: identity/freeze/SHA mismatch, >5% yearly missingness, budget
  exhaustion, integrity failure, completion → bounded report, no
  continuation, no rescue. Non-effects: no promotion/registration/Phase
  IV/governance/other-reopening effects in any outcome.

## Review gates before any execution

Approval → filed preregistration (THIS version) → review →
implementation review + synthetic self-test → execution gate (freeze/SHA
re-verified) → ONE bounded execution → bounded report. Each gate
independent; approval skips none.
