# VS-TSMOM-01 Execution-Authorization Request v3 (UNAPPROVED — grants nothing)

**Status:** request referencing repaired preregistration v3 (fingerprint
sha256 `41c8f1a28b7db551850c3584a9531c2e3ec544cc984f3a3846c2ad94418d0faa`,
3289 bytes). Supersedes the v2 request as working paper. Approval requires
a separate explicit owner act. This file is not that act.

## Requested computation (single gated run)

SHA verification of `data/fred/fred_NASDAQ100.csv` → freeze check (B4 +
COMP-01 + v3 hashes) → synthetic self-test of a minimal exact-to-spec
implementation (both legs + passive benchmark) → ONE bounded execution of
v3 → bounded report with mandatory tradability-caveat section. No sweeps,
reruns, variants, follow-ons, data collection, or holdout contact.

## Inputs / outputs / boundaries / safeguards

- Inputs: named FRED file only (SHA + span/bars re-verified pre-use);
  frozen v3; B4 + COMP-01 records.
- Outputs: bounded report (primary D1 verdict incl. ratio bar, D2 with
  Holm inference, estimates with CIs, sensitivities, integrity log,
  conformance attestation).
- Boundaries: one verification, one review, one execution, one report;
  zero parameter search, simulation beyond the test, or data expansion.
- Safeguards: pre-use gates; fail-closed stops; HOLD otherwise unchanged;
  no candidate, Phase IV, runtime, or deployment effects.
- What approval would/would not grant: the single run above only; never
  threshold changes, universe/data substitution, fixed-leg standalone
  use, follow-on testing, or inference beyond v3's outcomes.
