# VS-TSMOM-01 Preregistration v5 (COMPLETE, NOT AUTHORIZED FOR EXECUTION)

**Status:** amended version incorporating approved CLOSE-01 (APPROVE,
Salman Ismail, 2026-10-14). Supersedes v4 as working paper (v4 preserved
as history). NOT filed as approved for execution. NOT permission to
execute. B4 record: task133 (`d1e1a823…`); COMP-01 record: task137
(`1d76fc1c…`); CLOSE-01 approval: this package. DISC-022 closed and
untouched except the benchmark-only use expressly permitted by COMP-01.

## Changes from v4 (each with reason)

1. **Execution timing: next session open → first close strictly after
   month-end T** (reason: CLOSE-01 approval; the bound file has closes
   only). Entry = first daily close strictly after T; exit = first daily
   close strictly after the next signal month-end; holding interval is
   close-to-close. Same-close execution remains prohibited (a T-close
   fill would assume closing-auction access the spec never establishes).
2. **Execution-lag change disclosed** (reason: CLOSE-01 requires it):
   signal-to-execution lag grows by ~1 session vs the v4 next-open rule;
   overnight-gap capture moves from entry-open into the holding return.
   The rule stays a monthly momentum rule; it is not the same executable
   object — hence this new version, never a silent reinterpretation.
3. **No other changes.** Paired scaled−fixed estimand; benchmark-only
   fixed leg (constant unit size, identical conventions including the new
   timing, reported only inside the bounded report); buy-and-hold
   secondary D2; Holm α=0.05 across {D1, D2}; benefit-to-friction ≥ 2
   PROPOSED/owner-confirmable; r12 signal; prior-month vol; target 10%;
   ties flat; bounds [-1,+1]; fail-closed missing data (>5% yearly stop,
   duplicates fail closed, no fill); cost grid + financing stress; block
   bootstrap (block 12, B=10000, seed 20261014); single window
   (~1987-02→2026-08); index-level claim with tradability caveat
   (close-to-close price-index test only — strengthened, not weakened);
   stops; non-effects — all carried.

## Frozen decision rules (complete)

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
independent; approval skips none. Schema check (no observation access):
date-ordered daily closes support next-close lookup definitionally; no
opens needed anywhere in this version.
