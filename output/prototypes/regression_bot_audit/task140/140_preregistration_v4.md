# VS-TSMOM-01 Repaired Preregistration v4 (COMPLETE, NOT AUTHORIZED FOR EXECUTION)

**Status:** amended draft incorporating the TASK139 Gate-4 completeness
fix via recorded amendment (`140_amendment_record.md`, same package).
Supersedes v3 as working paper (v3 preserved as history). NOT filed as
approved. NOT permission to execute. B4 record: task133 (`d1e1a823…`);
COMP-01 record: task137 (`1d76fc1c…`); DISC-022 closed and untouched
except the benchmark-only use expressly permitted by COMP-01.

## Changes from v3 (each with reason)

1. **Trichotomy completed** (reason: TASK139 Gate-4 FAIL — the lower>0 +
   ratio<2 case with ratio active matched no branch): added "Lower bound
   > 0 with ratio < 2 while the ratio bar is active → INCONCLUSIVE
   (statistically positive, economically immaterial per the bar)."
2. **No other changes.** Primary paired scaled−fixed estimand;
   benchmark-only fixed leg (constant unit size, identical conventions,
   reported only inside the bounded report); buy-and-hold secondary D2;
   Holm α=0.05 across {D1, D2}; benefit-to-friction ≥ 2 PROPOSED/
   owner-confirmable; signal, vol estimator, target 10%, timing, ties,
   bounds, fail-closed data rules, cost grid + financing stress, block
   bootstrap (block 12, B=10000, seed 20261014), single window,
   index-level claim with tradability caveat, stops, non-effects — all
   carried byte-for-byte in substance from v3.

## Frozen decision rules (complete and now exhaustive)

- Family D1 (primary, paired scaled−fixed) + D2 (secondary, paired
  scaled−passive), each with one-sided 95% bootstrap lower bound; Holm
  α=0.05 across {D1, D2}.
- PASS: D1 lower bound > 0 (Holm-adjusted) AND benefit-to-friction ≥ 2.
- FAIL: D1 upper bound < 0.
- INCONCLUSIVE: D1 interval includes zero; OR lower bound > 0 with ratio
  < 2 while the ratio bar is active (statistically positive, economically
  immaterial per the bar); OR ratio bar waived with positive point
  estimate (reported as written).
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
