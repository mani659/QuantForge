# PROTO-S2-001 — Frozen Specification (FROZEN; NOT AUTHORIZED FOR EXECUTION)

**Identifier:** PROTO-S2-001 (Lane B prototype namespace per §3D — confers
no candidate status; CANDIDATE registration explicitly not granted).
**Status:** FROZEN 2026-10-13 on recorded owner selections (decisions file,
same package). NOT filed as approved for execution. NOT permission to
execute. Selections: window FIRST_5_SESSIONS, identity UNCONDITIONAL_S2,
control TOM_CONTROL, budget PROCEED-bounded (design/implementation/
synthetic-test only; evaluation budget reserved), holiday NYSE +
fail-closed skips.

## 1. Hypothesis and mechanism

January week-1 SPY-class exposure earns positive net return (unconditional
New-Year repositioning premium). Falsifier: non-positive net economics
under the frozen costs over the evaluated span. No barometer conditioning;
no regime filter; no variant.

## 2. Instrument, universe, timeframe

SPY-class ETF daily closes, `lane_b_batch1/data/SPY.csv` (SHA `483919f8`,
8472 rows 1993-01-29→2026-09-25, verified). No other instrument. No M1/CFD
translation (out of scope; would be a new object).

## 3. Entry, exit, position management

- Entry: executable close (ask construction: Dec close × 1.0010) of the
  last December row-date; exit: executable close (bid: Jan-5th-session
  close, no adjustment) — wait, cost accounting unified below; rule:
  ENTER at Dec-close, EXIT at 5th-January-session close, LONG 1.0× only.
- Window: first 5 January row-dates (J1..J5); need not be contiguous
  calendar days (holidays skipped by date order, not by invention).
- Position: 1.0× long during window; flat otherwise. No sizing/scaling/
  leverage/pyramiding/partials. No stops/targets/filters.
- Missing endpoints: any missing entry/exit date → that year SKIPPED
  fail-closed and counted (covers holidays, short sessions, data gaps
  uniformly; no imputation, no substitution).

## 4. Control and comparison

TOM-convention: unconditional buy-and-hold SPY over the identical span
(first entry date → last exit date), same cost schedule (entry/exit legs
once). Comparison: cumulative net (strategy) vs cumulative net (control),
DESCRIPTIVE only. Primary inference is on the strategy leg alone
(no paired test against control — S4 degeneracy avoided by construction).

## 5. Evaluation window and chronology

First evaluable January: 1994 (needs December 1993; SPY starts
1993-01-29). Last: January 2026. Expected N ≈ 33 annual events
(determined mechanically at execution; predeclared counting, not a claim).
Single window; no development/validation split (avoids post-outcome
parameters). No holdout exists; protection is procedural (freeze-then-run).

## 6. Data and provenance

Panel above only (hash-verified pre-use or stop). Timestamp duplicates
fail closed. >5% yearly missingness → STOP (pattern precedent; short-session
years count normally — only truly absent rows count as missing).

## 7. Costs (declared assumption, not broker fact)

Batch-1 family: spread 10 / slippage 5 / commission 0 bps per side.
Entry leg: Dec_close × 1.0015 (+10 spread +5 slippage); exit leg:
Jan5_close × 0.9985 (−10 spread −5 slippage); commission 0. Total 30 bps
round-trip (matches frozen "30 RT" annotation). Control legs identical
schedule (entry/exit once each). No financing leg (cash-settled
assumption disclosed; a financed implementation would differ — out of
scope, stated).

## 8. Primary metric, uncertainty, decision rules

- Primary: mean annual net return, with 95% bootstrap CI (i.i.d. over
  annual non-overlapping events; B=10000; seed 20261015 arbitrary-but-
  fixed, labeled).
- PASS: lower 95% bound > 0. FAIL: upper bound < 0. INCONCLUSIVE:
  interval includes zero. No magnitude bar invented (owner may impose one
  at evaluation authorization; flagged, not set).
- Minimum evidence to continue: PASS as defined. Anything else ends the
  line with a record (no rescue, no variant).

## 9. Resource ceiling and stops

Single bounded analysis + report; zero sweeps/reruns/variants. Stops: data
mismatch, budget exhaustion, integrity failure, completion → report, no
continuation. Evaluation itself NOT authorized here (needs a separate act
with its own budget decision).

## 10. Non-effects

No candidate registration/promotion, no Phase IV, no governance change,
no other reopening, no deployment-technology claims. HOLD/NONE unchanged
by this freeze.
