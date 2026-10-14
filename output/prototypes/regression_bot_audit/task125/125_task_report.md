# TASK125 — Task Report

| Field | Value |
|---|---|
| Task ID (inferred) | `TASK125` — next after `task124`; no task-ID registry exists |
| Directory | `output/prototypes/regression_bot_audit/task125/` |
| Mode | Bounded statistical-power study (owner-authorized). Synthetic simulations only. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-13 |

## Verification

Preregistration frozen before measurement (hash `153b9acc…`). Data files
verified via provenance.json hashes (SPY `483919f8…`, VEU `eeb120f4…`, AGG
`dd9483ce…`, BIL `61c4b653…`). Study used synthetic simulations only —
no strategy backtest, no parameter optimization, no candidate creation, no
holdout access, no runtime contact. HOLD / Active Research NONE unchanged.
All 5 deliverables written with hashes verified in `125_manifest.sha256`.

## Results summary

Classification: **B. LOW-POWER.** The 4-asset XSM design is structurally
underpowered: power 12.9% at 50 bps/mo, 78.8% at 100 bps/mo (target 80%),
false-positive rate 21.6% (target ≤5%). The limiting factor is the
four-asset universe (spread std 370.6 bps/mo), not sample length or
inferential method.

## Stop conditions checked

No stop conditions triggered: data permissions verified, estimand and
effect range defined pre-outcome, statistical method valid for power
assessment, all required inputs present.

## Final status

TASK125 COMPLETE — STOP. No strategy backtest or candidate promotion
authorized. Any empirical test requires separate explicit owner
authorization.
