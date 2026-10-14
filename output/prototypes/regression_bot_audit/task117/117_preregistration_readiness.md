# TASK117 — CAND-025 Preregistration Readiness (blocker matrix)

**Status:** readiness audit. Draft exists (TASK116); filing and execution
require the pending approval. Determination at §3.

## 1. Blocker-by-blocker matrix

### (a) Numeric go/no-go thresholds — OWNER DECISION REQUIRED

No numeric promotion/validation bar for CAND-025 re-measurement exists in
any record. Task-65 gives calibration landmarks (≥10% measurable at Sharpe
~1.5/8Y; ≥50% reliable nowhere; detectable region outside the intraday
3–5Y universe per Q8) — benchmarks for comparison, not transplantable bars
(transplanting a number across designs = invention). Structural criteria
are predeclared (sign agreement, net>0 under 2.0/3.0-pt stress); exact bars
must be set by the owner at preregistration-finalization review. Minimum
action: owner sets bars in the finalization review (one act, no menu).

### (b) Inferential method + multiplicity — RESOLVED FROM EXISTING AUTHORITY (pattern; parameters at filing)

Repo precedent determines the pattern, so the owner need not choose it:
family-wise error control across the small comparison family (Holm, per
task57 preregistration precedent) with resampling-based intervals for
time-ordered events (block bootstrap, per PROTO-TREND-001 precedent).
Exact parameters (α, B, block length, seeds) are frozen in the filed
preregistration with owner visibility at the review gate — standard
predeclaration practice, not post-outcome selection, not invention. No
separate owner act required beyond the verdict.

### (c) N=157 sufficiency / larger-N permissibility — RESOLVED (finding adverse; conditional design permitted)

Existing authority answers sufficiency negatively: Task-65 Q7/Q8/Q10 as
applied in the task67 matrix place CAND-025's cell (N=157, knife-edge
economics, high turnover) below the calibrated reliable-detection region
(UNDETERMINED/BORDERLINE, poor detectability) — a finding, not a blocker
to be filled. Larger-N sources: forward accumulation needs recorders
(prohibited); new collection prohibited; split-sample weakens (disclosed).
Permitted within activity limits: the predeclared panel contingency —
enumerate rule-satisfying events at execution; if count >157 the full set
is primary with the original 157 as verification subset (no assumption
made now). Unconditional larger-N is BLOCKED BY MISSING EVIDENCE (no
lawful source of more events).

### (d) Identity + canonical-data integrity checks — RESOLVED FROM EXISTING AUTHORITY

V9 lines 59/91 + G0 data line (USATECHIDXUSD) vs ledger-only XAUUSDm label
with no test artifact; reference SHA `39f25619…` (triple-record);
executor pre-use SHA + span/bars cross-check with abort on mismatch; tick
excluded. Checks fully specified; only their execution awaits approval.

### (e) Stops, non-effects, review gates — RESOLVED FROM EXISTING AUTHORITY

TASK115 §2/§4 as grounded in §3B multiplicity logic and freeze rules
(identity/freeze/SHA mismatch, budget exhaustion, integrity failure,
completion → report, no continuation/rescue; HOLD/registration/Phase IV
non-effects; draft → approval → filed preregistration → review →
implementation review + synthetic self-test → execution gate → execution →
report).

## 2. READY / NOT READY determination for future execution

**NOT READY — approval absent (OWNER_APPROVAL_PENDING governs).**
Preregistration draft COMPLETE and approvable: items (b), (d), (e) resolved;
(a) needs the owner's bars at finalization review; (c) resolved adversely
with a permitted conditional design. No item requires another audit cycle —
the only missing inputs are the owner's verdict/ruling/bars, deliverable in
the single CAND025-RM-01 act.
