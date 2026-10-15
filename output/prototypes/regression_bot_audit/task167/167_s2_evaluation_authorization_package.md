# TASK167 — S2 Single-Evaluation Authorization Package (PROPOSED, NOT APPROVED)

**Status:** authorization proposal only. No approval recorded, nothing
authorized, nothing executed. Approval requires a separate explicit owner
act; this file is not that act.

## 1. Frozen spec binding

`PROTO-S2-001` frozen spec (`task166/166_s2_frozen_spec.md`, sha256
`5a318e7e47263c67dc308adf9e326122e56b285e5eaaf585274867525a47eb94`,
4414 bytes). Verified byte-identical this session. Selections on record:
window FIRST_5_SESSIONS, identity UNCONDITIONAL_S2, control TOM_CONTROL,
budget PROCEED-bounded (design/implementation/synthetic-test; evaluation
budget reserved), holiday NYSE + fail-closed skips (owner message
2026-10-15; no signature fabricated).

## 2. Cost consistency (verified, no conflict)

Source annotation: friction 10/5/0 with 30 RT total. Frozen arithmetic:
entry Dec_close × 1.0015 (+10 spread, +5 slippage), exit Jan5_close ×
0.9985 (−10, −5), commission 0 → 15 bps per leg × 2 legs = 30 bps round
trip. Exact match, no amendment needed. Costs declared as research
assumption (Batch-1 B3 precedent), not broker fact. Control legs bear the
identical schedule once each.

## 3. Data scope (verified by metadata only, no outcomes)

- File: `output/prototypes/lane_b_batch1/data/SPY.csv` (794,286 bytes,
  sha256 `483919f897326b261a669bc595a37112b4de5222c4ad0ed84da08060f4b71231`).
- Span 1993-01-29→2026-09-25, monotonic, unique; NaN total 0 (no yearly
  >5% stop triggered).
- Eligible January windows (≥5 rows + December prior, dates only): 33,
  1994-01→2026-01 — matches the audit's ~34-event figure.
- Timestamp duplicates: none found in metadata scan (executor re-verifies).
- **Permission gap:** no existing authorization covers S2's evaluation
  use of this file (Batch-1 budgets consumed 3/3; reuse requires explicit
  permission — TASK107 blocker pattern). Listed here so the owner act
  covers it; not assumed.

## 4. Design elements carried unchanged

TOM control complete (buy-and-hold, identical span, same schedule once
each, cumulative-net descriptive, no paired test — S4 degeneracy avoided
by construction). Inference: mean annual net + 95% bootstrap CI
(B=10000, seed 20261015, i.i.d. over non-overlapping annual events);
PASS lower>0 / FAIL upper<0 / INCONCLUSIVE covers zero; no magnitude bar
invented (owner may impose at approval). Single window, no splits, no
holdout (procedural protection stated).

## 5. Proposed authorized chain (single bounded evaluation)

SHA verification → freeze check → synthetic self-test of a minimal
exact-to-spec implementation → ONE bounded execution → bounded report
(primary verdict, estimates with CIs, control comparison, integrity log,
conformance attestation). Activity bounds: one verification, one review,
one execution, one report; zero sweeps/reruns/variants. Stops: identity/
freeze/SHA mismatch, budget exhaustion, integrity failure, completion →
report, no continuation, no rescue. Non-effects: no promotion/
registration/Phase IV/governance/other-reopening effects in any outcome.

## 6. Recommendation

The package is complete and internally consistent; cost arithmetic
matches the frozen annotation exactly; data verified adequate (33
windows, zero NaN, lawful control). Information gain: first empirical
test of an audited-clean, fully preregistered calendar-seasonal rule —
decisive PASS/FAIL/INCONCLUSIVE either way, ending a long-open question.
**Recommend owner approval** of this bounded single evaluation (with data
permission for the named file + activity bounds above). Approval grants
only this run; anything further needs a new act.
