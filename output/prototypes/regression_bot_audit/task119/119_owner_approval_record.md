# TASK119 — CAND025-RM-01 Owner Approval Record (RECORDED DECISION)

**Status:** recorded owner approval. This file records a decision; it does
not execute anything.

## 1. Provenance (proposal vs approval, distinguished)

- Proposal: TASK118 `118_owner_decision.md` (sha256 `5d1661c9…`, 1906 B) —
  proposed text, explicitly unapproved at filing.
- Approval: owner instruction TASK119 (2026-10-13), verbatim operative
  language: "The owner has approved the bundled CAND025-RM-01 ruling,
  proposed numeric/inferential provisions, and bounded scope presented in
  TASK118." No earlier approval existed or is claimed; nothing is
  backdated.

## 2. Scope approved (exactly the TASK118 bundle, no more)

(1) Identity (i): tested instrument WAS USATECHIDXUSD M1 (XAUUSDm ledger
label to be corrected as a documentation fix at execution time, not a
content change); XAUUSD excluded (new G0 if pursued). (2) §99.1
confirmation for CAND-025 re-measurement adopted with the DISC-025
comparison rationale on record (TASK114 §3). (3) Preregistration as
finalized in `119_frozen_preregistration.md`, INCLUDING the adopted
numeric bars and inferential parameters (T1 structural; T2 zero-bars; T3
95% bootstrap lower bounds + Holm α=0.05, B=10000, seed 20261013; T4
majority falsification flag; T7 count contingency). (4) Gated chain:
freeze verification → filed preregistration (this package) → review →
implementation review + synthetic self-test → execution gate (freeze/SHA
re-verified) → ONE bounded execution → bounded report. Activity bounds
(one of each; zero sweeps/reruns/variants). Data: named USATECHIDXUSD M1
file only, SHA-verified pre-use against `39f25619…`; tick excluded; no new
collection; no holdout; no recorders. Stops and non-effects per §3 below.

## 3. Non-effects (unchanged by this approval)

HOLD otherwise unchanged (bounded exception for this chain only; no branch
activation); registration unchanged; no promotion, Phase IV, other
reopening, or governance/ledger change. Approval of the chain is not
permission to skip any in-chain gate (§4 of the frozen preregistration).

## 4. Record integrity

Prior TASK118 artifacts unmodified (hashes re-verified this session).
V9 freeze triple untouched. This record creates no candidate and grants no
standing authorization beyond the single gated chain above.
