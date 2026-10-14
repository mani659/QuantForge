# VS-TSMOM-01 Execution-Authorization Request v2 (UNAPPROVED — grants nothing)

**Status:** request referencing final preregistration v2 (this package).
Supersedes the TASK134 request as working paper. Approval requires a
separate explicit owner act. This file is not that act.

## Requested computation (single gated run)

SHA verification of `data/fred/fred_NASDAQ100.csv` → freeze check (B4
record + preregistration v2 hashes) → synthetic self-test of a minimal
exact-to-spec implementation → ONE bounded execution of v2 → bounded
report with mandatory tradability-caveat section. No sweeps, reruns,
variants, follow-ons, fixed-TSMOM computation, data collection, or
holdout contact.

## Inputs / outputs / boundaries / safeguards

- Inputs: named FRED file only (SHA + span/bars re-verified pre-use);
  frozen v2; B4 record.
- Outputs: bounded report (primary verdict incl. ratio bar, estimates
  with CIs, sensitivities, integrity log, conformance attestation).
- Boundaries: one verification, one review, one execution, one report;
  zero parameter search, simulation beyond the test, or data expansion.
- Safeguards: pre-use gates; fail-closed stops; HOLD otherwise unchanged;
  no candidate, Phase IV, runtime, or deployment effects.
- What approval would/would not grant: the single run above only; never
  threshold changes, universe/data substitution, follow-on testing, or
  inference beyond v2's outcome.
