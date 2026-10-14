# TASK135 — Gap 1 Decision: Economic Decision Threshold

## Finding

No authoritative record fixes an economic-magnitude bar for a paired
vol-scaled-vs-passive differential. Task-65 landmarks (detectability
benchmarks, not decision bars) cannot be transplanted; PROTO-TREND-001's
0.30 Sharpe bar governs a different estimand (absolute net Sharpe, not a
paired differential). Any numeric magnitude bar therefore encodes an
owner risk/return preference — correctly identified, not fabricated.

## Decision (structure grounded; value proposed)

- **Statistical evidence (predeclared, sufficient for PASS/FAIL):**
  one-sided 95% bootstrap lower bound of mean paired net differential > 0
  (PASS); upper bound < 0 (FAIL); otherwise INCONCLUSIVE. This alone
  decides the preregistered outcome — economics enters via the next line.
- **Economic materiality (proposed default, owner-adoptable):**
  benefit-to-friction ratio ≥ 2, where benefit = mean paired net
  differential per month and friction = realized monthly cost drag of the
  strategy leg. Rationale independent of outcomes: a dynamic rule must
  earn a multiple of its own friction to justify complexity over passive
  holding; 2:1 is a conventional complexity premium, labeled as
  convention, not evidence. Reported jointly with the statistical verdict:
  PASS requires BOTH the statistical bar AND ratio ≥ 2.
- **Owner dependency (exact):** the 2:1 value and the decision to impose
  any magnitude bar at all. The owner may replace 2:1 with another value
  or waive the magnitude bar (statistical trichotomy alone) at approval —
  either choice recorded, neither invented here.

## What this resolves and does not

Resolves: how economic materiality will be judged without inventing a
threshold. Does not resolve: the owner's risk preference (reserved above).
Statistical evidence and economic materiality stay separate by construction.
