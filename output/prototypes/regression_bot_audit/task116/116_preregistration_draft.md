# CAND-025 Re-Measurement Preregistration — DRAFT, NOT AUTHORIZED FOR EXECUTION

**Status:** draft prepared under TASK116 delegated authority. NOT approved,
NOT filed as approved, NOT permission to execute. Execution requires
CAND025-RM-01 APPROVAL plus every in-chain gate below.

## 1. Frozen binding (byte-verified)

V9 G0 `b1ac7853…019df3` (156 lines); V9 screen `05405eaa…5f8b1f2`
(99 lines); G1 adjudication `79dd4c2a…947d4a` (73 lines). Rule:
08:30–08:35 EST M5 True Range > 3.0× M5 ATR(14) → reversal entry 08:35
open → exit 09:30 open; max 1/day; no stops/filters (G2 identity rule: any
addition = new G0, out of scope). Identity: USATECHIDXUSD only; XAUUSD
excluded.

## 2. Reference data and pre-use verification (executor-side, post-approval)

File: `data/m1/USATECHIDXUSD_M1.csv` (filename confirmed; contents never
opened in preparation). Reference SHA-256:
`39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`
(multi-record). Pre-use: compute SHA + confirm span ≈2023-09-01→2026-07-10
/ ~906.8k bars; abort on any mismatch. Tick file excluded. No new
collection; no holdout; no recorders. (Filename/SHA ≠ proof of pre-use
integrity — verification happens before use, not here.)

## 3. Sample, bars, splits, costs (records only)

- Bars: M1 resampled to M5 (screen line 91). Date range: UNDECLARED in all
  ledgers — sample defined as all bars in the verified panel, no invented range.
- Events: all rule-satisfying events in the panel; original N=157 kept as
  the identified verification subset. Larger-N contingency: if count >157,
  full set is primary (predeclared, no assumption made now).
- Split (sign-stability): chronological halves by event date; structural
  criterion = sign agreement + net>0 under both cost stresses; exact
  numeric go/no-go bars BLOCKED — frozen at preregistration finalization
  with owner visibility, never inferred here.
- Costs: 2.0-pt assumed basis + 3.0-pt stress (records); Task-65 frontier
  comparison reported. Missing bars: incidence reported, no fill
  (fill = new rule, prohibited).

## 4. Outcomes, non-effects, statistics

- Primary outcome: sign-stability verdict on the frozen rule.
- Reported: stressed-net estimates, frontier comparison, freeze-conformance
  attestation, integrity log.
- Non-effects (regardless of outcome): no promotion, registration, Phase IV,
  governance, or other-reopening effects.
- Inferential machinery (CI method, seeds, multiplicity handling):
  BLOCKED — frozen at preregistration finalization post-approval.

## 5. Limits, runs, stops, reporting

One freeze verification, one implementation review, ONE bounded execution,
one report; zero sweeps/reruns/variants. Stops: identity/freeze/SHA
mismatch, budget exhaustion, integrity failure, completion → report, no
continuation, no rescue. Implementation (none on record): minimal
exact-to-spec build gated by review + synthetic self-test before any
market-data contact.

## 6. Gates before later stages (separation explicit)

Draft → (CAND025-RM-01 APPROVAL) → filed preregistration → review gate →
implementation review + synthetic self-test → execution gate (freeze/SHA
re-verified) → execution → bounded report. Approval of the decision is not
permission to skip any gate. Confirmation/validation and any paper/live
step need separate future decisions.

## 7. Unresolved mandatory fields (blockers, not assumptions)

Numeric go/no-go bars; inferential machinery specs; larger-N primary design
if panel yields only N=157 (fallback: verification + split-half on 157,
disclosed as weakening). All frozen at finalization post-approval — never
filled here.
