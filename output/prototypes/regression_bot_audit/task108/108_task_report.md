# TASK108 — EXT-062 Bounded Lane B Specification and Admission Assessment

| Field | Value |
|---|---|
| Task ID (inferred) | `TASK108` — next after `task107`; no task-ID registry exists |
| Directory | `output/prototypes/regression_bot_audit/task108/` |
| Subject | EXT-062 ONLY (owner-selected). No substitution performed. |
| Track | Lane B, specification-only. No evaluation authorized, none performed. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-13 |

---

## 1. Governing-state verification (permit-check passed)

- HOLD / Active Research NONE / New Candidate NONE / Backtest NONE / Economic Validation NONE / Phase IV NOT AUTHORIZED — handoff CURRENT PROJECT STATE block + §99.6, unchanged.
- §99.6 continuity entry intact (stopping point explicit); Task107 decision package read (`task107/107_owner_decision_package.md`).
- Permit: role §§3A permits executable specification drafting, overlap checking, structural classification, and documentation without evaluation authorization. This owner task order authorizes the bounded spec-only track for EXT-062. No evaluation authorization exists or is inferred.
- Constraint: Q1=A — §99.1 check mandatory and owner-ruled before specification-freeze. No owner §99.1 ruling on EXT-062 exists in any record. Consequence applied: the check below is performed and recorded; the ruling is carried as PENDING; the specification is issued PROPOSED (not admitted, not frozen).

## 2. EXT-062 identity, provenance, evidence (facts vs interpretations vs unknowns)

- **Facts (task51 §6):** Maximum Diversification Portfolio, Choueifaty–Coignard (2008, JPM 35(1)) + long-only form (2013); risk-based weighting rule, not a directional price rule; objective DR(w) fixed; unconstrained closed form w ∝ Σ⁻¹σ fixed; long-only form numerical, fixed. Task51 status: DISTINCT, data PARTIALLY, six ambiguities recorded (window, vol window, cadence, universe, variant, return convention).
- **Interpretations (labeled):** task51's DISTINCT rating and TOP-3 placement are preparer assessments, not rulings; the CRAN citation conflict is carried unresolved; the 2-asset arithmetic in the spec (§9) is illustrative hand computation, not evidence.
- **Unknowns:** all six BLOCKERS B1–B6; whether the owner will rule on §99.1; whether a data scope will ever be authorized; whether the in-sample source claim replicates (UNVERIFIED, untested here).

## 3. Proposed causal claim and mechanism distinction

- **Claim (from the concept):** maximizing the diversification ratio harvests asset risk premia more efficiently than cap-weighting.
- **Distinction:** EXT-062 contains no market-timing signal of any kind — no trend/momentum lookback, no mean-reversion trigger, no breakout level, no session/calendar/carry logic, no regression fit to price, no primary/confirmation event structure, no lot-multiplier/recovery mechanics. Protected mechanisms are all directional-timing or martingale-recovery families; a weighting-plus-rebalance rule shares mechanism-identity with none of them.

## 4. §99.1 admission gate — check performed, ruling pending

Family-by-family check against the §99.1 list (handoff §99.1, read from disk)
plus closed lines and ledger search:

| Protected item | Overlap with EXT-062 | Result |
|---|---|---|
| Mean reversion DISC-021 / NEG-065 | no reversion trigger, no deviation rule, no oscillator | none |
| Fixed TSMOM 12/1 DISC-022 / NEG-066 | no momentum signal or lookback sign | none |
| Session range expansion DISC-024 | no session logic | none |
| Liquidity sweep/reversal DISC-025 | none | none |
| Structural breakout BASE-001/MECH-N01 | no breakout levels | none |
| Session-sequential quality BASE-002/MECH-N03 | none | none |
| HTF→LTF R1/R2 (§99.1 lines) | no multi-timeframe relational structure | none |
| Grid/basket/recovery DISC-015/016/018 | no lot multiplier, averaging-down, or recovery logic; shared word "basket" is superficial (portfolio weighting vs martingale basket) | none |
| ATR breakout (Phase 2 C) | no volatility-breakout trigger | none |
| Zone Recovery (Phase 2 E) | none | none |
| Quote-level Q01–Q06 | no microstructure content | none |
| RF-001 confirmation-failure protocol | no breakout events, no primary/confirmation structure (RF-001: USATECHIDXUSD structural breakouts vs US500 confirmation, 0 evaluable opportunities) | none |
| R1/R2 regression-bot, EXT-054, PROTO-TREND-001, Batch 1 (GEM/VM/TOM) | no regression fit, no RSI trigger, no TSMOM signal, no calendar/volatility-target content | none |
| Negative ledger (diversification / risk-parity / mean-variance / weighting search) | no entry found touching portfolio weight-optimization | none |

**Gate outcome: check complete — no protected overlap found. Owner §99.1
ruling: PENDING (no existing ruling; none recorded here).** "Distinct" was
not treated as profitable, admitted, or validated. Nothing was reopened.

## 5. Specification outcome

- `108_ext062_specification.md` issued as PROPOSED DRAFT: source-faithful
  objective + both solution forms + hand-worked deterministic example with
  unexecuted acceptance criteria; six BLOCKERS (B1–B6) plus cost-field,
  missing-data, universe, identifier, and benchmark blockers explicitly
  marked; no value invented.
- The concept **cannot yet proceed to a frozen specification**: blockers B1–B6
  are resolvable only by further source access (never invention), and
  freezing additionally requires the pending owner §99.1 ruling plus a
  data-scope decision. This is outcome (1)-deferred, not outcome (2)-failed:
  admission did not fail (no criterion failed), so no
  `108_admission_blockers.md` failure record was created — and no
  speculative completion was fabricated to fill the slot.

## 6. Changes made (only the deliverables)

- Created: `output/prototypes/regression_bot_audit/task108/108_ext062_specification.md` (this task's §4 deliverable).
- Created: `output/prototypes/regression_bot_audit/task108/108_task_report.md` (this file).
- Modified: nothing. No prior report rewritten; history left byte-identical.

## 7. Manifest

| Deliverable | Purpose | SHA-256 |
|---|---|---|
| `108_ext062_specification.md` | Proposed draft spec for EXT-062 with marked blockers (task §4) | `bb3e41cfd751b27de405d794d4b135590af9f7401beef2e912440278e12f900d` (7260 B) |
| `108_task_report.md` | Source-grounded findings, gate outcome, verification, stopping point (task §6.1) | digest computed post-write; recorded in the TASK108 completion message |

`108_admission_blockers.md` intentionally absent: admission did not fail (see §4).

## 8. Completion-gate confirmations

- Every cited source/path verified against working-tree files this session
  (§99.1 list, role §§3A–3D, task107 package, task51 §§6/10–13/15–16,
  task99 record, task101 §7–8, task102 §3–4, handoff §99.6, closure record).
- Scope held to EXT-062 + existing records; no other concept touched.
- No code, test, backtest, simulation, parameter search, power study, or
  economic validation run or written. No market-data file opened for
  evaluation (data compatibility cited from task51 text only).
- No runtime contact (no status read, no process touched), no MT5 contact,
  no candidate registration, no governance/ruling/ledger change, no
  commit/push.
- HOLD / Active Research NONE unchanged (re-verified post-write).
- Unrelated working-tree changes preserved (this task added only the two
  files above inside the audit-trail namespace).

## 9. Genuinely unresolved authorization blockers (not technical details)

1. Owner §99.1 ruling on EXT-062 (required before any freeze).
2. Blocker resolution (B1–B6) by further source access — a future bounded
   task, not authorized here.
3. Data scope (new acquisition and/or named-file reuse) — required before
   any implementation/evaluation decision (carried from TASK107 §6).

```text
TASK108 COMPLETE — STOP FOR REVIEW. TASK109 not started.
```
