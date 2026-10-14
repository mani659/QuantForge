# TASK134 — Task Report

| Field | Value |
|---|---|
| Task ID (inferred) | `TASK134` — next after `task133`; no task-ID registry exists |
| Directory | `output/prototypes/regression_bot_audit/task134/` |
| Mode | Design only. No execution authorized or performed. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-13 |

## Requirement-by-requirement compliance (§Required design work 1–10)

1. Estimand: mean paired monthly net differential (strategy − buy-hold),
   gross/net separated — COMPLIANT (prereg §1).
2. Data limitation: price-only consequences documented; ^NDX substitution
   noted as needing separate decision, not made — COMPLIANT (prereg §2,
   limitations file).
3. Frozen spec: r12, prior-month vol (VM pattern), 10% target (disclosed
   arbitrary), next-open monthly, ties flat, [-1,+1], fail-closed missing
   data — COMPLIANT (prereg §3).
4. Cost model: Batch-1 family as declared assumption + ×0.5–×4 grid +
   0/2/4% financing stress (labeled) — COMPLIANT, no broker facts invented.
5. Inference: block bootstrap (block 12, B=10000, seed 20261014),
   heteroskedasticity accommodated, single comparison — COMPLIANT.
6. Chronology: single window (~1987-02→2026-08), no development splits
   (cures TASK129 Defect 6 by removing post-outcome parameters) — COMPLIANT.
7. Thresholds: PASS lower bound >0 / FAIL upper <0 / INCONCLUSIVE covers
   zero; no magnitude bar invented (owner-optional flagged) — COMPLIANT.
8. Comparator audit: fixed-TSMOM absent everywhere; buy-and-hold benchmark
   with control precedent — COMPLIANT.
9. Power: TASK125/126 explicitly not transferred; no power claimed; CI
   speaks — COMPLIANT.
10. Exec-auth request: separate, unapproved, exact computation/inputs/
    outputs/scope/safeguards — COMPLIANT.

## Design decisions / unresolved issues

- Single-window chronology chosen over TASK128 splits (reason recorded).
- Magnitude bar left to owner option (no source for one).
- ^NDX substitution, forward-demo granularity, and any evaluation itself
  remain future decisions, not made here.
- If any listed choice lacks grounding on review, the exact item is named
  above — no silent assumption exists in the package.

## Boundary observance

No backtest, simulation, download, parameter search, holdout, runtime, or
paper-trading operation. DISC-022 untouched; fixed-TSMOM nowhere used. No
candidate created/promoted. HOLD / Active Research NONE re-verified
post-write. No commit/push/unrelated edits. V9/task133/governance files
untouched.

## Manifest (verified after all edits)

| Deliverable | Size / SHA-256 |
|---|---|
| `134_preregistration_draft.md` | 5480 B / `21d6c96c62d1dcc3a763fee51bb115e23fe0a0684462a957f390a0e5fa55e909` |
| `134_data_cost_limitations.md` | 1935 B / `af93495f5690eb1ac3dfdf89e905d8f7ea3ab7aa5cb1a29b885c1c8d978ce30a` |
| `134_inference_power_note.md` | 1808 B / `fe165a7ec05ef15504d6a21c1da163a52ba1d21fec4b0f27898effcca8993c67` |
| `134_execution_authorization_request.md` | 1566 B / `7c27faaa75cb804f804093bac3a4b1735d726c0ff98b7afb8fb83b91e27cae58` |
| `134_task_report.md` (this file) | digest computed post-write; recorded in the TASK134 completion message |

## Final state

Design prepared and audited; execution authorization still pending; no
execution performed; DISC-022 closed; Research Capacity HOLD; Active
Research NONE.
