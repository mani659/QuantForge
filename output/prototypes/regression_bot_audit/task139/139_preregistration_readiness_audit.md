# TASK139 — Independent Preregistration Readiness Audit (v3)

**Role:** independent audit of TASK138, not a redesign. No execution, no
data access, no modifications to TASK138 artifacts (all hashes re-verified
intact this session).

## Gate 1 — Paired estimand: PASS

Scaled and fixed legs share the r12 series, timing, panel, window, costs,
and missing-data rules per the v3 text; the pairing is by month with the
differential as the unit of analysis. Months where scaled |w|<1 vs fixed
±1 are predeclared design behavior, not a mismatch. The estimand answers
the B4-approved incremental-value question as framed.

## Gate 2 — Sizing semantics: PASS

Constant |w|=1 is definitional of "fixed" as opposed to "scaled" (shared
1.0 cap; no second signal; no sizing-policy change beyond the constant).
DISC-022's original sizing is not on record, so no conflict is
establishable — and none is claimed: the baseline is defined as the paired
counterpart, not as a replication of DISC-022. Documented in v3, no
empirical content.

## Gate 3 — Multiplicity: PASS

D1 (primary, scaled−fixed) and D2 (secondary, scaled−passive) precisely
defined; Holm α=0.05 across {D1, D2}; alpha unchanged from v2's one-sided
95% (v2 had no multiplicity rule, so nothing contradicted). Diagnostics
labeled descriptive/non-inferential — family not expanded.

## Gate 4 — Economic criterion: FAIL (one incomplete branch)

Benefit (mean paired net differential) and friction (realized monthly cost
drag, scaled leg) are computable without discretion, and PROPOSED status
stays explicit. BUT the trichotomy is not exhaustive: the case **lower
bound > 0 with ratio < 2 while the ratio bar is active** matches NONE of
PASS (needs ratio ≥ 2), FAIL (needs upper bound < 0), or INCONCLUSIVE
(as written: interval-includes-zero, or the waived-ratio case). Honest
executors could diverge here (FAIL vs INCONCLUSIVE) — post-outcome
discretion exactly where preregistration must eliminate it.
**Smallest correction (one sentence, via recorded amendment, not silent
edit):** "Lower bound > 0 with ratio < 2 while the ratio bar is active →
INCONCLUSIVE (statistically positive, economically immaterial per the
bar)." No redesign; no threshold change; the bar itself untouched.

## Gate 5 — Dataset and costs: PASS

Index-level claim with mandatory tradability caveat; costs declared as
assumption with grid; financing stress-only; no tradable-net, executable,
or profitability claims found (re-swept at audit time).

## Gate 6 — Reproducibility: PASS (one non-blocking note)

Seeds, fail-closed missing-data rules, single-window chronology, metrics,
stops, and required report contents all present. Note (non-blocking):
warmup start "~1987-02" is approximate in prose but deterministic given
the panel (12m signal + 1m vol from 1986-01-02); an implementer derives
it exactly. No action required.

## Audit verdict

5 of 6 gates PASS; Gate 4 FAILS on trichotomy completeness. **No
execution-authorization recommendation is made.** Per the decision rule,
work stops here with the single-sentence correction above — not a broad
redesign, not a new governance review.
