# TASK114 — CAND025-RM-01 Owner Decision Package (PROPOSED, NOT APPROVED)

**Status:** decision package only. No re-measurement executed, no
preregistration filed, no data content accessed. CAND025-RM-01 remains
proposed and unapproved (as in TASK113).

## 1. Freeze verification (verified from disk, not summaries)

The V9 frozen object exists, is identifiable, and is unchanged:

| Artifact | Path | SHA-256 |
|---|---|---|
| V9 G0 (mechanism, rule, PROMOTE) | `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V9.md` (156 lines) | `b1ac785321a829c73c980b0f94b4f4cfd60612209cc8945b446eb0bf0d019df3` |
| V9 G1 screen (PASS-MARGINAL, instrument + data lines) | `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260826_V9.md` (99 lines) | `05405eaa2870bb65847626188cb4288687d6652b182a42270bb8185445f8b1f2` |
| G1 final adjudication (HOLD + G2 identity rule §10) | `output/research_discovery/RESEARCH_FACTORY_V2_G1_CAND025_FINAL_ADJUDICATION_20260826.md` (73 lines) | `79dd4c2a8e8c72c0e32bf906f30dad59d42c46d90c2c37ef98b516c087947d4a` |

Frozen rule: 08:30–08:35 EST M5 True Range > 3.0× M5 ATR(14) → reversal
entry at 08:35 open → deterministic exit at 09:30 open; max 1/day; 157
events; no stops/filters. G2 identity rule (adjudication §10, verbatim in
substance): on any revisit the exact frozen object must be kept — adding a
stop-loss or filter constitutes a new G0 candidate. Upward trigger
verified: task67 preservation named T57-allocation completion as the upward
condition; T57 completed (task74 closed) → trigger met.

## 2. Identity fork (from source records; no silent selection)

- **USATECHIDXUSD:** V9 G0 "Data Required: USATECHIDX M1 (resampled to
  M5)"; screen line 59 "Instrument: USATECHIDXUSD", line 91 "Data: Local
  USATECH M1 CSV. No tick data or Parquet used." All 157 events measured on
  it; plausibility stated in USATECHIDX points.
- **XAUUSDm:** unified ledger row 8 + inventory INV-007 label
  `instruments = XAUUSDm M1`. No XAUUSD test artifact exists anywhere
  (task67 §2.1). Plausible origin: V9's "Cross-Market Scope" note naming
  XAUUSD/GBPUSD as generalizable — a note, not a test.
- **Consequences:** same-object reopening MUST use USATECHIDXUSD; an XAUUSD
  run is a new candidate requiring its own G0 gate (task67 §2.1). Costs
  were point-denominated (2.0 assumed) on USATECHIDX scale — not portable.
  If records cannot settle which file was tested, no defensible comparison
  exists and execution is blocked (stated as a stop below).

## 3. §99.1 confirmation basis (for the owner ruling)

CAND-025 (Family A Information Arrival/Price Discovery): scheduled macro
shock → TR-based void detection → fixed-session reversal exit. DISC-025
(closed): Asian-extreme breach → rejection → confirmation-gated reversal;
behavioral discovery supported, executable translation non-viable, line
closed. To confront: both are post-event reversals ("reversal" in both
names). To distinguish: volatility-shock trigger vs level-breach trigger;
macro-release context vs Asian-session context; fixed session exit vs
rejection-plus-confirmation. Task67's matrix asserts distinctness — a
preparer assessment, not a ruling. The owner must rule material distinction
vs superficial renaming; a negative ruling terminates this package.

## 4. Binding, scope, budgets, data, stops

- **Binding:** the three freeze files above, byte-identical; any deviation
  (stop, filter, threshold, window, exit, universe) = new G0, out of scope.
- **Permitted next-stage activity (only if approved):** verify freeze +
  file a preregistration (larger-N rule, 2.0/3.0-pt cost stress,
  sign-stability test, Task-65 frontier benchmark, numeric go/no-go bars
  frozen therein, no-invention attestation). No implementation, no
  evaluation, no data execution beyond preregistration checks.
- **Budget [BLOCKER — owner fills]:** no re-measurement budget exists on
  record. Proposed frame: single bounded analysis + report; zero new data
  collection. Amount/scope fields must be completed in the decision.
- **Data permissions [PARTIAL BLOCKER]:** filename `data/m1/USATECHIDXUSD_M1.csv`
  confirmed present by name only (contents never opened this session);
  tick file explicitly excluded per screen line 91. Executor must
  SHA-verify the file and confirm it is the tested panel before any use;
  unverifiable → STOP. No new collection, no holdout, no other files.
- **Evaluation boundary:** no evaluation authorized here; any evaluation
  needs the stage gates in TASK113 §4 plus fresh budgets/data scope.
- **Stopping conditions:** identity unresolvable → stop; freeze mismatch →
  stop; budget exhausted → stop; integrity failure → stop; completion →
  preregistration filed, no continuation.

## 5. Adverse evidence — and why re-measurement is still defensible

+1.25 mean net vs 2.0-pt friction (3.0 pts "instantly obliterates"); SD
~50; N=157 single-shot, no tests/CIs/Sharpe; dates/costs UNKNOWN; no
validation/confirmation/holdout/topology/sealed sample; forward ~55/yr
slow; FP MEDIUM; Task-65 poor detectability at high turnover. Defensibility:
Tier-1 second-priority adjudication; exact frozen spec exists; the precise
gap is sign stability under larger N — answerable only by bounded
re-measurement; T57 trigger met; design pre-sketched in records. If the
owner judges the knife-edge economics disqualifying, REJECT is the correct
answer — stated plainly.

## 6. Exact decision wording (APPROVE / REJECT / DEFER)

```text
DECISION CAND025-RM-01 (bounded CAND-025 re-measurement):
(1) Identity (pick one): (i) tested instrument WAS USATECHIDXUSD M1
    (correct the XAUUSDm ledger label) → re-measure that instrument; or
    (ii) XAUUSD M1 → declared a NEW G0 requiring its own gate (not this
    reopening). Unresolvable → STOP (instrument shopping prohibited).
(2) §99.1 confirmation for CAND-025 re-measurement, with operative reason
    addressing the DISC-025 comparison in §3. Negative → terminate.
(3) Authorize freeze verification + preregistration filing ONLY, per §4
    (larger-N rule, 2.0/3.0-pt stress, sign-stability test, Task-65
    benchmark, go/no-go bars frozen therein). Budget: [owner fills].
    Data: named USATECHIDXUSD M1 file only, SHA-verified pre-use; tick
    data excluded; no new collection; no holdout.
(4) Non-effects: HOLD otherwise unchanged; registration unchanged; no
    implementation, evaluation, promotion, Phase IV, other reopening, or
    governance change.
Owner answer: APPROVE (fields 1–4 complete) / REJECT / DEFER.
```

No preregistration draft prepared (per §4 of the task: nothing filed as
though approved). Conditions blocking execution: unapproved decision; any
unfilled BLOCKER field; failed freeze/SHA verification.
