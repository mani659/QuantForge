# TASK115 — CAND025-RM-01 Final Decision (READY FOR OWNER; NOT APPROVED)

**Status:** decision-ready text. Nothing herein is approved, recorded as
approved, or executed. Technical recommendation and owner decision are
separate (§6).

## 1. Recommended basis (owner guidance carried, not a ruling)

Per the tasking guidance, identity is pre-filled as **USATECHIDXUSD** for
same-object reopening; XAUUSDm is excluded (an XAUUSD run = new G0 under
its own gate). The §99.1 ruling itself remains an owner act (§5, block 2).

## 2. Fields resolved from authoritative records

- **Freeze (byte-verified this session):** V9 G0 `b1ac7853…019df3`
  (156 lines); V9 screen `05405eaa…5f8b1f2` (99 lines); G1 adjudication
  `79dd4c2a…947d4a` (73 lines). Rule: 08:30–08:35 TR > 3.0×ATR(14) →
  08:35 reversal entry → 09:30 exit; 1/day; no stops/filters (G2 identity
  rule: any addition = new G0).
- **Identity evidence:** G0 data line + screen lines 59/91 (USATECHIDXUSD,
  Local USATECH M1 CSV, no tick/parquet) vs ledger-only XAUUSDm label with
  no test artifact (plausible origin: V9 cross-market-scope note).
- **Data reference:** `data/m1/USATECHIDXUSD_M1.csv`, reference SHA-256
  `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`
  (multi-record: H01 protocol, ORD protocol + amended, F01 freeze).
  Caveat stated: the hash attests the repo's canonical panel, not proven
  byte-identity with G1's 2026-08 input; executor cross-checks span
  2023-09-01→2026-07-10 / ~906.8k bars / SHA pre-use, aborts on mismatch.
  Tick file excluded. No new collection; no holdout; no recorders (forward
  accumulation therefore out of scope — larger-N design restricted to
  split-sample variants on the existing panel, disclosed as weakening).
- **Design (from task67/task95):** larger-N rule, 2.0/3.0-pt cost stress,
  sign-stability test, Task-65 frontier benchmark; numeric go/no-go bars
  frozen IN the preregistration (owner-visible), not set here.
- **Implementation:** none on record → minimal exact-to-spec build gated
  by review + synthetic self-test before any market-data contact
  (PROTO-TREND-001 IA-12 pattern, cited as pattern).
- **Stops:** identity/freeze/SHA mismatch, budget exhaustion, integrity
  failure, completion → report, no continuation, no rescue.
- **Non-effects:** HOLD otherwise unchanged; registration unchanged; no
  promotion, Phase IV, other reopening, or governance change.

## 3. Owner-only blockers (no record can fill these)

**B-OWNER-1 — §99.1 ruling adoption** (CAND-025 vs DISC-025 comparison in
TASK114 §3; negative terminates). **B-OWNER-2 — budget confirmation**
(activity bounds in §4 govern by default: one verification, one
preregistration, one implementation review, one bounded execution, one
report, zero sweeps/reruns; any additional numeric bound is owner-optional).
**B-OWNER-3 — verdict** below. Without all three, nothing is authorized.

## 4. Technical recommendation (not a decision)

Approve with identity (i), for the stated reason that Tier-1 adjudication
plus a met upward trigger plus a frozen spec makes this the shortest
audited path to an answer on a preserved conditional — with the adverse
record (knife-edge economics, single-shot history, slow confirmation)
fully disclosed in TASK114 §5. REJECT is correct if the owner judges the
economics disqualifying. This recommendation neither approves nor executes.

## 5. Exact decision text

```text
DECISION CAND025-RM-01 (bounded CAND-025 re-measurement):
(1) Identity: (i) tested instrument WAS USATECHIDXUSD M1 (correct the
    XAUUSDm ledger label) → re-measure that instrument. XAUUSD excluded
    (new G0 if pursued). Unresolvable → STOP.
(2) §99.1 confirmation for CAND-025 re-measurement, with operative reason
    on the DISC-025 comparison. Negative → terminate.
(3) Authorize: freeze verification → preregistration filing (larger-N
    rule, 2.0/3.0-pt stress, sign-stability, Task-65 benchmark, go/no-go
    bars frozen therein) → minimal exact-to-spec implementation gated by
    review + synthetic self-test → ONE bounded re-measurement execution →
    bounded report. Budget: activity bounds above [owner may add numeric
    bound]. Data: named USATECHIDXUSD M1 file only, SHA-verified pre-use
    against 39f25619…; tick excluded; no new collection; no holdout; no
    recorders. Stops per §2. Non-effects per §2.
Owner answer: APPROVE (blocks B-OWNER-1–3 complete) / REJECT / DEFER.
```
