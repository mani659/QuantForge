# TASK140 — Amendment Record: trichotomy completeness (outcome-blind)

**Declared:** 2026-10-13, BEFORE any VS-TSMOM-01 outcome access.
Outcome-blindness evidence: no VS-TSMOM-01 results, events, summary, or
output file of any kind exists anywhere in the repository (verified by
full-tree filename search this session); no bounded execution has ever
run. No outcome has been computed, viewed, or guessed.

## 1. Defect (TASK139 Gate 4)

V3 decision rules as written: PASS requires lower bound > 0 AND ratio ≥ 2;
FAIL requires upper bound < 0; INCONCLUSIVE covers interval-includes-zero
(plus the waived-ratio case). The case **lower bound > 0 with ratio < 2
while the ratio bar is active** matches no branch — honest executors could
diverge (FAIL vs INCONCLUSIVE), i.e., post-outcome discretion where
preregistration must eliminate it.

## 2. Correction (one sentence, no threshold change)

Added to the decision rules: "Lower bound > 0 with ratio < 2 while the
ratio bar is active → INCONCLUSIVE (statistically positive, economically
immaterial per the bar)." Rationale: the statistical evidence favors the
strategy but the predeclared economic bar is unmet — neither a pass nor a
failure. Threshold 2, alpha 0.05, Holm family, estimand, dataset, costs,
and comparator restrictions all unchanged.

## 3. Mechanism (established repo convention)

New-version amendment per §3B ("genuine changes create a new
specification/version") and the task42 amendment-file pattern (declared
amendment + defect + outcome-blind timing + preserved originals): v3 file
untouched; v4 issued as a complete new file in `task140/`. No silent edit.
