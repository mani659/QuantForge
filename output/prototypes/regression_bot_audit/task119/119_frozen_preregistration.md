# CAND025-RM-01 Frozen Preregistration (FROZEN; execution needs all §4 gates)

**Status:** FROZEN preregistration under recorded approval (see approval
record). Frozen ≠ executed. No post-outcome amendment or threshold tuning
permitted — any change creates a new preregistration version; this result
stands or falls as frozen.

## 1. Frozen binding

V9 G0 `b1ac7853…019df3`; V9 screen `05405eaa…5f8b1f2`; G1 adjudication
`79dd4c2a…947d4a` (all byte-verified, unmodified). Rule: 08:30–08:35 EST
M5 True Range > 3.0× M5 ATR(14) → reversal entry 08:35 open → exit 09:30
open; max 1/day; no stops/filters (G2 identity rule). Identity:
USATECHIDXUSD only; XAUUSD excluded (ledger-label correction documented
as fix, not content change).

## 2. Data and pre-use integrity (executor-side)

File `data/m1/USATECHIDXUSD_M1.csv` (presence + 56,818,845-byte size
confirmed by metadata 2026-10-13; contents never opened in preparation).
Reference SHA-256 `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`
(triple-record). Pre-use: recompute SHA + confirm span ≈2023-09-01→2026-07-10
/ ~906.8k bars; abort on any mismatch. Tick excluded; no new collection;
no holdout; no recorders.

## 3. Sample, design, costs

Bars M1→M5; sample = all bars in the verified panel (date range UNDECLARED
in all ledgers — no invented range). Events: all rule-satisfying events;
original N=157 kept identified as verification subset; count contingency
(count >157 → full set primary). Split: chronological halves at median
event date (odd extra to second half). Missing bars: incidence reported,
no fill. Costs: 2.0-pt basis + 3.0-pt stress; Task-65 frontier comparison
reported (no force).

## 4. Primary outcome and adopted decision rules (explicit pre-outcome)

- T1: sign agreement — both halves positive mean net (structural).
- T2: mean net > 0 under 2.0-pt AND 3.0-pt stress (zero intrinsic).
- T3 (ADOPTED): 95% bootstrap CI lower bound > 0 under both stresses
  (B=10000, i.i.d. over events, seed 20261013) with Holm α=0.05 across
  {T1, T3@2.0, T3@3.0}.
- T4 (ADOPTED): strict-majority 5-min continuation → falsification flag
  recorded regardless of T1–T3.
- Go/no-go: ALL of T1 + T3@2.0 + T3@3.0 must pass; T4 flag recorded as
  mechanism concern in all cases.

## 5. Limits, stops, gates, non-effects, reporting

One verification, one review, ONE execution, one report; zero
sweeps/reruns/variants. Implementation (none on record): minimal
exact-to-spec build gated by review + synthetic self-test before any
market-data contact. Stops: identity/freeze/SHA mismatch, budget
exhaustion, integrity failure, completion → bounded report, no
continuation, no rescue. Gates: approval (RECORDED) → filed preregistration
(THIS file) → review → implementation review + synthetic self-test →
execution gate (freeze/SHA re-verified) → execution → report. Each gate
independent; approval skips none. Non-effects: no promotion/registration/
Phase IV/governance/other-reopening effects in any outcome. Report format:
primary verdict, estimates with CIs, frontier comparison, integrity log,
conformance attestation.
