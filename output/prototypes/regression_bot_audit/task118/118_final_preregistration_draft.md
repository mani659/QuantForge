# CAND-025 Re-Measurement Preregistration — FINAL DRAFT, NOT AUTHORIZED FOR EXECUTION

**Status:** complete draft pending approval + adoption of PROPOSED items
(see threshold matrix). NOT filed as approved. NOT permission to execute.
Supersedes the TASK116 draft in completeness; TASK116 file preserved as history.

## 1. Frozen hypothesis, identity, logic

CAND-025 Macro Shock Liquidity Void Reversal (V9 G0 `b1ac7853…`,
screen `05405eaa…`, adjudication `79dd4c2a…`, all byte-verified):
08:30–08:35 EST M5 True Range > 3.0× M5 ATR(14) → reversal entry at 08:35
open → deterministic exit 09:30 open; max 1/day; no stops/filters
(G2 identity rule: any addition = new G0). Identity USATECHIDXUSD only;
XAUUSD excluded. Causal claim: macro-shock liquidity voids refill within
the hour (source claim, unverified); preregistered falsifier: V9
continuation direction (T4).

## 2. Data identity checks (executor-side, post-approval)

File `data/m1/USATECHIDXUSD_M1.csv`; reference SHA-256
`39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`;
confirm span ≈2023-09-01→2026-07-10 / ~906.8k bars pre-use; abort on any
mismatch. Tick file excluded. No new collection; no holdout; no recorders.
(Filename/SHA ≠ proof — verification happens before use, never here.)

## 3. Inclusion/exclusion, sample, splits, costs

- Bars M1→M5; date range UNDECLARED (all ledgers) — sample = all bars in
  the verified panel, no invented range.
- Events: all rule-satisfying events; original N=157 kept identified as
  verification subset; count contingency per matrix T7.
- Split: chronological halves at median event date (odd extra to second
  half). Missing bars: incidence reported, no fill.
- Costs: 2.0-pt basis + 3.0-pt stress (records). Frontier comparison
  reported (T5, no force).

## 4. Primary outcome, procedure, bars

- Primary: sign-stability verdict (T1, structural) with stressed-net
  estimates (T2, structural) and 95% bootstrap lower bounds under both
  stresses with Holm α=0.05 across {T1, T3@2.0, T3@3.0} (T3/T6 PROPOSED:
  B=10000 i.i.d. over events, seed 20261013).
- Secondary: V9 falsification flag (T4 majority form PROPOSED).
- Go/no-go: ALL decision bars must pass (T1 + T3 both stresses); T4 flag
  recorded as mechanism concern regardless. PROPOSED bars adopted only by
  approval (matrix §decision statement).

## 5. Stops, review gates, non-effects, reporting

Stops: identity/freeze/SHA mismatch, budget exhaustion, integrity failure,
completion → bounded report, no continuation, no rescue. Gates: approval →
filed preregistration → review → implementation review + synthetic
self-test → execution gate (freeze/SHA re-verified) → ONE execution →
report. Non-effects: no promotion/registration/Phase IV/governance/other
reopening regardless of outcome. Limits: one verification, one review, one
execution, one report; zero sweeps/reruns/variants.

## 6. Unsupported items (explicit)

Numeric bars, α/B/seed/block choices, halves edge rules beyond §3, and any
larger-N design beyond the T7 contingency are PROPOSED or BLOCKED as marked
— none presented as grounded. No implementation exists on record; minimal
exact-to-spec build gated as above.
