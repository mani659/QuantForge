# VS-TSMOM-01 Execution-Authorization Request (UNAPPROVED — grants nothing)

**Status:** request prepared under TASK134 design authority within the B4
admitted track. Approval requires a separate explicit owner act. This file
is not that act.

## Requested computation (single gated run)

SHA verification of `data/fred/fred_NASDAQ100.csv` → freeze check (V9
n/a; preregistration + B4 record hashes) → synthetic self-test of a
minimal exact-to-spec implementation → ONE bounded execution of the frozen
preregistration → bounded report. No sweeps, reruns, variants, or
follow-ons.

## Inputs / outputs / scope / safeguards

- Inputs: named FRED file only (SHA + span/bars re-verified pre-use);
  frozen preregistration (`134_preregistration_draft.md` as approved).
- Outputs: bounded evaluation report (primary verdict, estimates with
  CIs, cost-grid sensitivity, integrity log, conformance attestation).
- Resource scope: one verification, one review, one execution, one
  report; zero parameter search, simulation beyond the test, or data
  collection.
- Safeguards: pre-use gates (identity/freeze/SHA); fail-closed stops
  (mismatch, budget exhaustion, integrity failure, completion → report,
  no continuation, no rescue); HOLD otherwise unchanged; no candidate,
  Phase IV, runtime, or deployment effects.

## What approval would and would not grant

Would grant: the single run above. Would NOT grant: fixed-TSMOM
comparator work, threshold changes, universe/data substitution,
follow-on testing, or any inference beyond the preregistered outcome.
