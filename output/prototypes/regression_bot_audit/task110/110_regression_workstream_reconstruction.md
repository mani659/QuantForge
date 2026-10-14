# TASK110 — Regression-Bot Workstream Reconstruction (Tasks95–110)

**Status:** read-only reconstruction from working-tree records. No ruling,
admission, or evaluation. The true starting point, restored.

## 1. Original concepts (Task100; Task96 context)

Two price-regression hypotheses, never tested in the proposed form:
- **R1 / RG-TREND-001** — fit a regression line to price; trade its
  slope/projection (trend continuation).
- **R2 / RG-REVERT-001** — fit a regression line to price; trade deviation
  from it as a baseline (mean reversion).
Task100: both `RELATED EVIDENCE ONLY` and `INSUFFICIENTLY SPECIFIED` — no
source for any design parameter. Task96: no prior QuantForge study,
candidate, or prototype uses a regression line fitted to price as either
signal (only in-repo least-squares usage is CAND-089's range slope — a
different object).

## 2. Exact scope of the R1/R2 exclusions (Task101 §7 → Task102 §3, owner)

- **R1: Option C — excluded at admission.** Mechanism-identity ruling: the
  evidence did not establish a distinct economic mechanism from the
  protected trend-momentum line. Explicitly unauthorized: specification
  drafting, evaluation authorization, backtest/replay/paper execution,
  estimator rescue. Not an empirical failure; never backtested.
- **R2: Option A — excluded at the mechanism gate** under NEG-065
  (mean-reversion family: permanent closure, can_be_reopened = NO).
  The exact regression-residual implementation was never empirically
  tested. Explicitly unauthorized: baseline/estimator rescue, re-expression
  of the closed mechanism. Not an empirical failure.
- Supporting rulings: Q1=A (§99.1 binds Lane B admission as a mandatory
  owner-ruled general rule); Q2=general rule; Q5=EXT-054 kept rejected on
  Task99 terms (admission-level redundancy, never evaluated).

## 3. Relation to closed mechanisms (no reopening implied)

R1 was excluded for *failing to establish* distinctness from protected
trend-momentum (DISC-022 family); R2 was excluded *into* the NEG-065
family closure. Related closed lines, untouched: DISC-021/DISC-022,
NEG-065/NEG-066, BASE-001/002, R1/R2 HTF→LTF §99.1 lines (label collision
noted; RG- identifiers disambiguate), EXT-054, PROTO-TREND-001 (closed
ECONOMICALLY INSUFFICIENT), Batch 1 (GEM/VM/TOM closed), EMA-GRAB
(closed/preserved). Task96's precedent conflict and Task98's scope question
were closed by Q1=A; Task99's B4-non-transferability stands (acceptances
are prototype-specific owner acts).

## 4. Evaluated vs discussed vs never tested

- **Evaluated and closed:** TASK57-MDP-001 (Maximum Diversification; discovery
  INCONCLUSIVE/BOUNDARY_EFFECT → M1 NO_REGION → selection NONE → task74
  CLOSED / NOT PROMOTABLE, rescue_authorized:false, frozen); Batch 1
  (3/3 consumed); PROTO-TREND-001 (1/1); EMA-GRAB (preserved).
- **Discussed, never evaluated:** R1, R2 (admission/mechanism exclusions);
  EXT-054 (admission rejection); EXT-051…053/055…062 library entries
  (sourcing characterizations only); RS/S1/S2/ToQ/Darvas/Propulsion items
  (various blocked/deferred states per task95 §5.2).
- **Never empirically tested in proposed form:** R1, R2 (exact residual),
  EXT-054 — their exclusions are mechanism-identity rulings and must not be
  described as empirical disproof.

## 5. Executable implementation belonging to the regression-bot objective

- R1/R2: none exists (INSUFFICIENTLY SPECIFIED; drafting barred).
- TASK57 `mdp_engine.py`: a complete evaluated implementation of the MDP
  concept — but it belongs to a CLOSED line (rescue false); reuse for any
  evaluation = rescue. Available as provenance/knowledge only.
- TASK108 draft spec: unadmitted proposal on a falsified premise; historical
  only.
- **Net: no available executable implementation or admissible specification
  exists today.** "Preserved" (task95 Tier-1 language) means artifacts kept,
  use conditional on owner authorization — not availability.

## 6. Why work moved to EXT-062 and why that direction was invalidated

TASK107, missing the task57/task95 records, framed EXT-062 as a preserved,
unadjudicated, DISTINCT library item and recommended a spec track; TASK108
drafted on that premise. TASK109 established: EXT-062 was CONSUMED by
TASK57-MDP-001 (explicit lineage, task57 §3), evaluated, and closed with
rescue barred; B1–B6 unresolvable from sources and untransplantable from
task57. TASK110 (closure reconciliation) corrected the handoff continuity
record; the correction stands in §99.6.

## 7. Remaining material constraints

HOLD/NONE (governance); Q1=A gate before any specification-freeze; no
admissible concept (all regression concepts excluded or closed); data-reuse
authorization unsettled for any evaluation touching existing files;
closure permanence + rescue bars; §3B fresh budgets required for any
evaluation; no candidate registration; forward runtime protected and not
an operative evidence path.
