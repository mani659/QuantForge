# TASK136 — Technical Decision: VS-TSMOM-01 Identifiability and Path

**Role:** independent technical lead. This decision challenges prior work
in this chain, including the TASK134/135 design it partially overturns.
No experiment authorized or performed.

## Research question and estimand

B4-approved question: does volatility scaling add incremental economic
value to the r12 momentum signal? Estimand: Performance(scaled) −
Performance(fixed), same signal, period, and costs. That difference IS
the incremental contribution — by definition, not by convention.

## Comparator finding (Decision 1)

The incremental contribution is mathematically identifiable ONLY via a
vol-scaled vs fixed-TSMOM paired comparison. The approved design compares
scaled vs buy-and-hold instead — which answers "does vol-scaled momentum
beat passive," a different estimand: beating passive could come entirely
from the r12 signal itself (telling zero about scaling), and trailing
passive could mask a positive scaling contribution. Scaled-vs-zero has
the same defect. These comparisons are NOT interchangeable, and no
statistical sophistication repairs the mismatch. **Conclusion: the current
design cannot answer its stated question without changing the approved
scope.** It CAN validly answer the narrower passive-comparison question —
but that is a different experiment requiring honest re-scoping, not a
reading of the current one.

## Best-use assessment (Decision 2)

Against preserved alternatives (RS-404 closed; S2 needs full decisions +
build; CAND-025 consumed; CORR-001 conditional; EXT intake long; pause):
the VS-TSMOM-01 track — frozen spec, verified data, complete prereg —
remains closest to executable evidence. Every alternative needs more
decisions and more build for less-ready questions. The track is worth
saving if the comparator gap can be closed with one narrow permission.

## Recommendation: C — narrow authorization change (Decision 3)

Request permission for a **benchmark-only fixed-TSMOM leg**: computed with
identical costs/timing, reported solely as the paired baseline for the
incremental estimand, never registered/promoted, DISC-022 closure intact,
Holm extended across both comparisons (predeclared). This is the minimal
change that makes the approved question answerable. Not A (estimand
unidentifiable as approved — proceeding would launder a passive
comparison into an incremental-value claim). Not B as primary (a
passive-only test is valid but answers a different question; offered
below as fallback, honestly relabeled). Not D (nothing else is closer;
switching wastes the completed design).

## Strongest argument against this recommendation

Re-running closed DISC-022 logic even as a benchmark erodes the
firewall's bright line and creates a citable precedent for executing
closed strategies "for comparison"; the owner excluded this comparator
weeks ago in the B4 record, so this request revisits settled scope; and
a null incremental result would spend an evaluation confirming what the
closure implied. If the owner judges the bright line worth more than the
incremental question, B (honestly relabeled passive-only test) or pause
is correct instead.

## Minimum next action (owner decision required)

```text
DECISION VS-TSMOM-01-COMP-01 (benchmark-only fixed leg):
Permit computing the fixed-TSMOM rule SOLELY as a paired baseline for the
incremental estimand, under identical frozen costs/timing, reported only
inside the bounded VS-TSMOM-01 report, with Holm across both comparisons
predeclared. No candidate status, no promotion, no standalone use, DISC-022
closure intact, all other B4 non-effects unchanged.
Owner answer: APPROVE / REJECT / DEFER.
```

## Files inspected / created

Inspected: handoff (HOLD/NONE verified), role contract, B4 record
(`d1e1a823…`), TASK134 prereg draft + report, TASK135 v2 + exec request,
TASK129 design gate. Created: this report only (`task136/`). No data
opened, no execution, no registration, no governance change, no commit.
HOLD / Active Research NONE unchanged.
