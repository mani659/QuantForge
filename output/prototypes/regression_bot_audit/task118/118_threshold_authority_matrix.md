# TASK118 — Threshold Authority Matrix (numeric acceptance criteria)

**Status:** audit record. GROUNDED items derive from cited records; PROPOSED
items require owner adoption (118_owner_decision.md). Nothing here approves
or executes anything.

## Method

Each candidate criterion: source sought in authoritative pre-existing
records → classified GROUNDED (directly applicable), PATTERN-ONLY (similar
precedent, not transferable as numbers), or PROPOSED (specified here,
adoption required). Transplanting another strategy's numbers is prohibited;
it was not done.

## Matrix

| # | Criterion | Source / rationale | Exact proposed rule | Standing |
|---|---|---|---|---|
| T1 | Sign stability | Structural; task67 "sign-stability test" requirement; G1 82+/75− shows why it matters. Binary — no number needed. | Both chronological halves (split at median event date; odd extra event to second half) show positive mean net. | GROUNDED (structural) |
| T2 | Stressed net positive | Zero is intrinsic break-even, not a transplant; costs 2.0/3.0-pt from G1/task67 records. | Point-estimate mean net > 0 under 2.0-pt AND 3.0-pt stress. | GROUNDED (structural) |
| T3 | Lower confidence bound > 0 | PATTERN precedent only: PROTO-TREND-001 criterion 2 (one-sided 95% lower bound > 0) and task57 Holm α=0.05 are spec-specific — similar, NOT directly applicable. | 95% bootstrap CI (B=10000, i.i.d. over events, seed 20261013, arbitrary-but-fixed) lower bound > 0 under 2.0-pt stress; Holm α=0.05 across decision family {T1, T3@2.0pt, T3@3.0pt}. | PROPOSED — owner adoption required |
| T4 | V9 falsification direction | Source-grounded directionally (V9: consistent 5-min shock continuation falsifies); unquantified in source. | Secondary rejection flag: strict majority of events show 5-min post-entry continuation → mechanism concern recorded (does not alone override T1–T3; predeclared weight). | Direction GROUNDED; majority form PROPOSED — adoption required |
| T5 | Task-65 frontier | Benchmark for comparison ONLY (Q7/Q8 landmarks are calibration-specific). Transplanting Sharpe ~1.5 as a bar = invention — refused. | Report position vs frontier; no go/no-go force. | GROUNDED as reporting-only |
| T6 | Seeds / resampling details | No CAND-025 record fixes them. | B=10000, i.i.d. over events, seed 20261013; halves per T1 rule; no fill, report-only missing-bar incidence. | PROPOSED — adoption required |
| T7 | Count contingency | Conditional design, no assumption (TASK116). | If panel yields >157 events: full set primary + original-157 verification subset. | GROUNDED (conditional) |

## Smallest decision statement

Adopt PROPOSED items T3/T4-quantified-form/T6 (single act: approve
CAND025-RM-01 with the preregistration as drafted in
118_final_preregistration_draft.md) or reject/defer. No menu of α values,
no menu of seeds — one bundled adoption. GROUNDED items need no decision.
