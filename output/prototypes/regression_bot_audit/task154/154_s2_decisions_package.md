# TASK154 — S2 Decisions Package: Four Choices Adjudicated, Spec Blocked on Owner Selection

**Delegation note:** this task asserts delegation of routine technical
decisions. No standing record of such delegation was found (TASK130
verification); it is recorded here as asserted-in-prompt. Crucially, the
authoritative S2 audit itself reserves THESE four choices to the owner
("must not be made by the agent"; "OWNER DECISION REQUIRED"; "owner
judgment explicitly reserved"). Specific record-level reservations
override a general prompt-level delegation claim. What follows gives
options + technical recommendations + downsides, and records all four
selections as outstanding. Nothing below selects on the owner's behalf.

## Choice 1 — Evaluation window

- Options on record: (a) first 5 NYSE sessions of January; (b) first
  calendar week (Mon–Fri).
- Technical recommendation: (a) — exchange-governed, deterministic
  regardless of Jan-1 weekday shifts; (b) varies in composition year to year.
- Downside: none evidentiary (purely definitional) — but reserved
  regardless. **Owner selection required.**

## Choice 2 — Strategy identity and exact mechanism

- Options on record: (a) unconditional week exposure; (b) Hirsch
  barometer-conditional timing. Per the audit these are DIFFERENT
  strategies; (b) additionally needs its own source-quality and
  DISC-022-adjacency adjudication.
- Technical recommendation: (a) — the smaller falsifiable unit; (b) is a
  separate, unadjudicated hypothesis, not a variant.
- Downside: (a) may dilute a conditional effect if one exists; choosing
  (b) chooses a different research object. **Owner selection required**
  (selecting the hypothesis itself is substantive, never routine).

## Choice 3 — Control strategy and comparison design

- Options: (a) TOM convention — unconditional long over the identical
  span with cumulative-net comparison (repository's honest pattern);
  (b) paired same-window exposure (S4-degenerate per PROTO-OPEX-001's
  record — structurally uninformative).
- Technical recommendation: (a) — avoids a documented degeneracy.
  Downside: none technical. **Owner binding required** (specification act).

## Choice 4 — Resource and execution budget

- Question (RS-302 precedent): does ~34 events of evidence value justify
  a full spec→build→evaluate slot, given calendar headwinds and weak
  power even on success?
- No technical recommendation for or against spending is offered —
  resource commitment is an owner prerogative, explicitly reserved.
  **Owner judgment required.**

## Conditional spec skeleton (NOT frozen — slots await the four choices)

Hypothesis: first-week-January SPY-class exposure earns positive net
return [SLOT 1: window] under [SLOT 2: unconditional | barometer rule];
instrument SPY-class ETF daily (Batch-1 convention); direction long 1.0×;
entry/exit per executable-close convention; control per [SLOT 3];
costs Batch-1 family; sample ~34 events [SLOT 4: adequacy ruling];
primary = cumulative-net differential with predeclared CI; stops: data
integrity failure, budget exhaustion, completion → report, no rescue.
Every bracketed slot is an owner fill. Nothing here is executable.

## Verdict: S2_BLOCKED_BY_SPECIFIC_MISSING_DECISION

Minimum missing information (single act, no new audit):

```text
DECISION S2-SPEC-01 (S2 specification choices):
(1) Window: (a) first-5-NYSE-sessions / (b) first-calendar-week.
(2) Identity: (a) unconditional week exposure / (b) barometer-conditional
    (admitting (b) opens its own source-quality + DISC-022-adjacency track).
(3) Control: (a) TOM-convention unconditional-long cumulative-net /
    alternative with stated reason (S4-degenerate paired form prohibited).
(4) Budget: proceed / decline for ~34 events (if proceed, capped single
    spec→build→evaluate chain, no variants).
Owner answer: APPROVE-AS-FILLED / REJECT / DEFER.
```

No experiments, measurements, data use, candidate changes, governance
edits, commits, or pushes performed. HOLD/NONE re-verified post-write
(see hash line). Prior records untouched.
