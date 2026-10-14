# TASK126 — Task Report

| Field | Value |
|---|---|
| Task ID (inferred) | `TASK126` — next after `task125`; no task-ID registry exists |
| Directory | `output/prototypes/regression_bot_audit/task126/` |
| Mode | Bounded statistical-method audit (owner-authorized). Synthetic simulations only. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-13 |

## Verification

TASK15 artifacts immutable (hashes verified). Correction preregistration
frozen before evaluation. Corrected study used synthetic simulations only —
no strategy backtest, no parameter optimization, no candidate creation, no
holdout access, no runtime contact. HOLD / Active Research NONE unchanged.
All 5 deliverables written with hashes verified in `126_manifest.sha256`.

## Results summary

The 21.6% null rejection rate was traced to a mean-shift defect (simulation
mean = effect - cost instead of effect). After correction: Type-I error
4.8% (well-controlled), power at 50 bps/mo 51.2% (below 80% target).
Classification: **A — CALIBRATED, LOW-POWER**. The 4-asset XSM design is
structurally underpowered; no calibration fix can overcome the tiny
cross-sectional universe.

## Stop conditions checked

No stop conditions triggered. All inputs present, method valid, calibration
achieved.

## Final status

TASK126 COMPLETE — STOP. No strategy test or broader-universe search
authorized. Any empirical work requires separate explicit owner
authorization.
