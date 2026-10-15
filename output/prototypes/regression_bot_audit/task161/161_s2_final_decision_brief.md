# TASK161 — S2 Final Decision Brief (consolidation; no selections made)

**Status:** decision brief only. All five items remain owner-reserved and
unselected. No experiment, implementation, or authorization follows from
this file. HEAD `666c1a9`; HOLD/NONE (re-verified post-write; see hash).

## 1. Five-decision table (options reproduced faithfully from source)

| Decision (source) | Permitted choices | Technical recommendation + rationale | Consequence of alternatives | SCR adjacency | Selection status |
|---|---|---|---|---|---|
| Window convention (S2 audit §1: "or a count the owner fixes pre-data"; §5) | (a) first-5 NYSE sessions; (b) first calendar week (Mon–Fri) | (a): exchange-governed, deterministic across Jan-1 weekday shifts | (b) varies in composition year to year; changes the tested span | Direct: sessions 1–2 sit inside Hirsch's SCR window under either counting; the choice shifts how much SCR-overlapping exposure is included — see §2 | Unresolved owner-reserved |
| Concept identity (audit §2: two different strategies) | (a) unconditional week exposure; (b) Hirsch barometer-conditional timing (needs own source-quality + DISC-022-adjacency track) | (a): smaller falsifiable unit; (b) is a separate unadjudicated hypothesis, not a variant | (b) re-opens sourcing/adjudication from zero | (b)'s conditional logic is independent of the SCR-overlap question; (a) carries the overlap as stated in §2 | Unresolved owner-reserved |
| Control/comparison (audit §6; S4-degeneracy record) | (a) TOM-convention: unconditional long, cumulative-net; (b) alternatives except S4-degenerate paired form (prohibited) | (a): repository's honest pattern; avoids documented degeneracy | (b): any paired same-window form is structurally uninformative | N/A (control choice is orthogonal to the window's SCR content) | Unresolved owner-reserved (binding a spec is an owner act) |
| Budget adequacy (RS-302 precedent) | Proceed / decline for ~34 events | None offered (resource commitment is owner prerogative) | Proceed spends a full chain on thin evidence; decline closes the route cleanly | N/A | Unresolved owner-reserved |
| Holiday handling (audit table + §6) | NYSE rule governs (determinable) + ADHOC_CLOSURES list adoption | NYSE rule as stated; list adoption as listed | Without the list, short sessions are unspecified | N/A | Unresolved owner-reserved |

## 2. SCR adjacency analysis (sessions 1–2)

Per the audit §2 source anatomy, January sessions 1–2 fall inside
Hirsch's canonical SCR window — the RS-302 phenomenon family — while
sessions 3–5 have no source claim anywhere. RS-302 closed on
data-integrity (venue/feed), NOT economic falsification. Therefore the
overlap is an adjacency question for the identity/window decisions (Q1-A
pattern), not a bar and not a permission: it neither proves S2 will fail
(economics were never tested) nor proves it will succeed (no source
defines the S2 rule). A sessions-3–5-only variant is NOT offered (unsourced
invention, prohibited). The owner decides knowing this; the record must
show the decision was made with eyes open, which this table provides.

## 3. Minimum valid freeze (all five recorded with signature/date)

Required: the five selections above, each explicit. Already established
(no re-decision): instrument (SPY-class ETF daily), direction (long-only),
entry/exit mechanics (executable-close ask/bid pattern), friction family
(10/5/0), disjoint annual windows, no-outcome-contamination finding.
Validation after recording: freeze review of the assembled spec against
§1–§8 sources + hash. Genuinely separate items: none — the five close the
set (budget decision gates whether the freeze is worth filing at all).

## 4. Immediate transition (conditional implementation task)

On recorded selections: bounded implementation at
`output/prototypes/s2_newyear_week/` (new dir, created only then) —
pure-function engine mirroring the frozen rule; synthetic self-test
(planted January weeks, hand-computed outcomes, determinism, no-look-ahead
proof); reuse map (SPY file SHA `483919f8`, Batch-1 calendar machinery as
pattern, pointintime checks, TASK120/146 review pattern); exclusions (no
tuning, no rescue, no holdout, no profitability claims, no deployment);
stops (missing data beyond rule, contract incompatibility, failed tests);
acceptance = tests green + review pass. Prerequisites: recorded selections
+ frozen spec + bounded implementation authorization (three distinct acts,
none present).

## 5. Actions not performed

No backtest, simulation, inference, data use, holdout, runtime,
candidate, governance, commit, or push activity. Prior records untouched.
Source paths/sections: S2 audit §§1–9 (`lane_b_s2_independence_audit.md`);
task95 §5.2/§7; TASK153/154/155/156/160 files (hashes re-verified);
handoff HOLD block; role contract.

## 6. Final verdict

**`S2_DECISION_BRIEF_READY`** — the brief is complete and the five
decisions are presentable in one pass; implementation readiness remains
strictly conditional on recorded selections. STOP; TASK162 not begun.
