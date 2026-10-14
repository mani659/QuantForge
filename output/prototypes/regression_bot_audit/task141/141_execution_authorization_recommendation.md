# TASK141 — Execution-Authorization Recommendation (PROPOSED, NOT GRANTED)

**Status:** technical recommendation to the project owner. Grants nothing.
Execution requires a separate explicit owner act; this file is not that act.

## Recommended authorization (single bounded VS-TSMOM-01 execution)

- **Under:** frozen preregistration v4 (sha256
  `1974fe6df80161579ab89245a0cf690082571924cd806ad2e12f8849b8ef4db7`,
  2739 bytes — cited directly, superseding the v3 request).
- **Scope:** SHA verification of `data/fred/fred_NASDAQ100.csv` → freeze
  check (B4 + COMP-01 + v4 hashes) → synthetic self-test of a minimal
  exact-to-spec implementation (scaled leg, fixed baseline leg, passive
  benchmark) → ONE bounded execution → bounded report with mandatory
  tradability-caveat section. No sweeps, reruns, variants, follow-ons,
  data collection, or holdout contact.
- **Ratio-bar declaration required in the act:** CONFIRM benefit-to-friction
  ≥ 2 as a gating bar OR WAIVE it (v4 decides either branch; silence
  would leave the verdict ambiguous — the one owner input beyond verdict).
- **Outputs:** bounded report (primary D1 verdict, D2 with Holm inference,
  estimates with CIs, sensitivities, integrity log, conformance
  attestation).
- **Stopping conditions:** identity/freeze/SHA mismatch, >5% yearly
  missingness, budget exhaustion, integrity failure, completion → report,
  no continuation, no rescue.
- **Exclusions:** fixed leg reported only inside the bounded report (no
  standalone use); no threshold/data/universe changes; no candidate,
  Phase IV, runtime, or deployment effects; HOLD otherwise unchanged.
- **Non-authorization clause:** recommending is not granting; no
  execution, threshold-setting, or follow-on is permitted by this file.

## Why this is the productive next step

All six readiness gates pass; the design answers the B4-approved
incremental-value question with the only lawful comparator set; the
remaining uncertainty (outcome itself) is exactly what a bounded,
preregistered execution resolves. Further documentation without execution
has diminishing returns from here.
