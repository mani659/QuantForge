# VS-TSMOM-01 Final Preregistration v2 (COMPLETE, NOT AUTHORIZED FOR EXECUTION)

**Status:** complete draft incorporating TASK135 gap adjudications.
Supersedes the TASK134 draft as working paper (that file preserved as
history). NOT filed as approved. NOT permission to execute. B4 record:
task133 (`d1e1a823…`); DISC-022 closed and untouched.

## Changes from v1 (each with reason)

1. **Primary outcome narrowed to index-level** (Gap 2): mean paired monthly
   net differential computed on FRED price closes under declared costs;
   tradability claims explicitly out of scope with mandatory caveat
   section. Reason: price-only series cannot support executable-P&L
   claims; narrowing restricts rather than expands.
2. **Economic bar added as PROPOSED** (Gap 1): PASS additionally requires
   benefit-to-friction ratio ≥ 2 (conventional complexity premium,
   labeled; owner may replace or waive at approval).
3. **No other changes.** Signal, vol estimator, target 10%, monthly
   next-open, ties flat, [-1,+1], fail-closed missing data, cost grid +
   financing stress, block bootstrap (block 12, B=10000, seed 20261014),
   single window (~1987-02→2026-08), buy-and-hold benchmark, fixed-TSMOM
   absent everywhere — all carried byte-for-byte in substance from v1.

## Frozen decision rules (complete)

- PASS: one-sided 95% bootstrap lower bound of mean paired index-level
  net differential > 0 AND benefit-to-friction ratio ≥ 2 (latter
  owner-confirmable at approval).
- FAIL: upper bound < 0.
- INCONCLUSIVE: interval includes zero (or ratio bar waived and bound
  straddles with positive point estimate — reported as written).
- Secondary (diagnostic, non-inferential): realized-vol tracking of the
  10% target; yearly differentials; turnover; cost-grid sensitivity;
  financing-stress sensitivity.
- Stops: identity/freeze/SHA mismatch, >5% yearly missingness, budget
  exhaustion, integrity failure, completion → bounded report, no
  continuation, no rescue. Non-effects: no promotion/registration/Phase
  IV/governance/other-reopening effects in any outcome.

## Review gates before any execution

Approval → filed preregistration (THIS version) → review →
implementation review + synthetic self-test → execution gate (freeze/SHA
re-verified) → ONE bounded execution → bounded report. Each gate
independent; approval skips none.
