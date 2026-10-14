# PROTO-TREND-001 — Outcome Interpretation and Closure Record

**Date:** 2026-10-08. **Mode:** read-only interpretation of frozen artifacts. No
experiments, reruns, simulations or data acquisition were performed for this
record. Classification unchanged: Lane B prototype evaluation artifact; NOT
research evidence; NOT a candidate; NOT a trade authorization.

## 1. Sources reviewed (all read-only)

| Source | sha256 (or first 16) |
|---|---|
| Frozen spec file `docs/lane_b_trend001/PROTO-TREND-001_spec_and_authorization.md` | `5813702185ccd1f1fa2c890a37c29b028c95758d10712b8b7f52fff8d08d2e59` |
| Part A (exact text between headings) | `4b44615dcf1646bd752dbaf6604f3c3a8c513840d2686228ec818eecddcbf35f` |
| Part B section | `58bc6c817b9592605fe419e382733bcf127eb383dec4635a0652bc113045dddc` |
| Annex `docs/lane_b_trend001/IMPLEMENTATION_ANNEX.md` | `fd544bd39881c478405052c5bf4f8651744d55ca00f36e0c45b7bec2440b81e8` |
| `evaluate_v2.py` (frozen) | `c7bb98faa235bb882a9ff5b7b14166eb588b393e17b51717ed517ec280526ad8` |
| `universe.json` (14 series, post owner-approved SI=F removal) | `0f1cb786899c414d2957d93bac51130e04c0d8995e28b08c0398cbe57c5bf2ab` |
| `results.json` | `bbcef6dccb24974ddc07456453711d3967eede17251f0d97acb95730f8cb45f6` (17967 B) |
| `monthly_series.csv` | `ac53b366746624511b1198589f42dbe7d2bec668002ff3f6eca8fd758fec241b` (52158 B) |
| `REPORT.md` | `34622c4145ff478c80c708e4540f3a889723782325c5745421e26ba9ef599a03` (14200 B) |

Authorization context: Part B signed `Salman, 2026-10-08`; B3 economic inputs
CONFIRMED; B4 ACCEPT (DISC-022 not reopened); B5 YES (Yahoo/FRED, research
use); B6 budget: 1 prototype, 1 evaluation. The single evaluation was executed
once on 2026-10-08 (exit 0); this record consumes no further evaluation.

## 2. IA-10 decision path to ECONOMICALLY INSUFFICIENT

IA-10 (annex) / A7 (Part A) fixed six criteria on the net monthly series at
×1 costs, verdict window entry-date ≥ 2010-01-01 (n = 200 months):

| # | Criterion | Value | Result |
|---|---|---|---|
| 1 | Net Sharpe ≥ 0.30 | 0.500483 | PASS |
| 2 | Bootstrap 5th pct of mean > 0 (B=10000, block 12, seed 20261007) | +0.000453 | PASS |
| 3 | Net Sharpe > 0 in 2010–2019 and 2020–2026 | (0.432373, 0.601180) | PASS |
| 4 | Net Sharpe > 0 at L = 63/126/252 | (0.259139, 0.181695, 0.500483) | PASS |
| 5 | Rescaled max drawdown ≤ 25% | 0.252022 | **FAIL** |
| 6 | Net Sharpe > 0 after 4%/yr financing stress on gross notional | −0.271654 | **FAIL** |

Decision path (pre-declared, no discretion): all-six-pass is required for
PASS-TO-FORWARD; it did not occur, so the failure branch applies. IA-10 then
routes by the **gross** series: if gross Sharpe ≥ 0.30 and gross bootstrap
lower bound > 0 → ECONOMICALLY INSUFFICIENT; otherwise NEGATIVE. Both gross
gates passed (gross Sharpe 0.511123 ≥ 0.30; gross bootstrap lower bound > 0),
so the frozen label is **ECONOMICALLY INSUFFICIENT** ("gross passes, net
fails", A11 taxonomy). The stored label, the label recomputed from the frozen
criteria via `decide_closure`, and the REPORT.md label all agree. The F-SNAP
"(FINANCING WARNING)" suffix branch is unreachable here because it only
applies when all six criteria pass.

## 3. Pre-declared diagnostics (IA-13 set only; protocol facts)

Faithful summary of the frozen outputs. These are **diagnostics, not outcomes**
and confer no pass, promotion or evidence status.

- **Gross vs net:** gross mean 0.0019148/mo vs net 0.0018747/mo; total
  cumulative cost 0.0080271 over 200 months (~0.000040/mo). Trading costs are
  small relative to the mean.
- **Cost grid (Sharpe at ×0.5/×1/×2/×4):** 0.5058 / 0.5005 / 0.4898 / 0.4685.
  Mild monotone decay; the ×1 verdict is not a cost-threshold artifact.
- **Financing stress (Sharpe at 0/2/4/6 % on gross notional):**
  0.5005 / 0.1151 / −0.2717 / −0.6592. With mean gross leverage
  Σ|w| ≈ 0.867, a 4%/yr charge (~0.0029/mo) exceeds the net mean (~0.0019/mo);
  criterion 6 fails because the charge is larger than the edge, not because
  of trading costs.
- **F-SNAP diagnostic (broker-swap upper bound, not a criterion):** net Sharpe
  with F-SNAP charges −1.092288. Per A7 this applies today's (2026-10-07)
  static swaps to the whole window and is an upper-bound stress.
- **Control (all signs +1, same panel, same costs):** Sharpe 0.814343, mean
  0.0029179, drawdown 0.196778; correlation with the strategy net 0.307310.
  Diagnostic comparison only (A6): the long-only panel out-Sharped the signed
  signal in this window; the modest correlation indicates the TSVM timing
  produced a return stream only partly shared with static long exposure.
- **Leverage:** max Σ|w| 1.416559; mean 0.866627.
- **Exposure by class (mean |w|):** fx 0.0921, gold 0.0483, equity 0.0462,
  brent 0.0249, bitcoin 0.0102.
- **Realised volatility** 0.044948; **skewness** −0.325113.
- **Ex-bitcoin:** Sharpe 0.338493, bootstrap lower bound −0.000064 (slightly
  negative), drawdown 0.266076 — bitcoin contributes materially to the
  primary result.
- **2004–2009 reported-only window (excluded from verdict):** Sharpe 0.629461
  (n=72).
- **Neighbourhood detail:** L=63 and L=126 bootstrap lower bounds are negative
  (−0.000424, −0.000785) although their Sharpes are positive; criterion 4
  required only positive Sharpe, which held.
- **2010–2019 sub-period bootstrap lower bound** is also negative
  (−0.000322) although its Sharpe passed criterion 3.
- **Worst months:** 2026-02 −3.75%, 2018-01 −3.37%, 2022-10 −3.29%,
  2011-08 −3.29%, 2010-04 −2.91% (full list in REPORT.md).
- **N(m):** 13–14 active markets across the verdict window (14-symbol
  universe after the owner-approved SI=F removal).
- **Yearly net:** positive 2010, 2012–2015, 2017, 2021–2026; negative 2011,
  2016, 2018, 2019; 2020 ≈ 0.

## 4. A9 limitations and A12 power statement (from the frozen REPORT.md)

A9 limitations, as recorded in REPORT.md:
- Continuous futures may contain roll gaps (gate flags reviewed).
- Spot FX/oil omit carry and roll yield; stress is a coarse proxy.
- Index series are price indices (no dividends).
- Cross-asset closes are asynchronous; one-day lag limits the effect.
- Bitcoin volatile; equal-risk scaling bounds weight; ex-bitcoin reported.
- Vendors may revise series; provenance hashes taken at acquisition.
- Rule on panel only; no general trend-following claim.

A12 power statement, verbatim: "About 200 monthly observations; a fail is not
strong evidence of no edge."

## 5. Protocol conclusions vs independent interpretation

**Protocol-defined (fixed before data access; the only binding conclusions):**
the closure label ECONOMICALLY INSUFFICIENT; criteria 1–4 PASS and 5–6 FAIL
with the values above; the closure is permanent for this specification
(A11: "no rescue, variant, rerun, parameter change or combination"); a fail
closes this prototype (A0); neither outcome validates or refutes
trend-following in general (A0, A10).

**Independent interpretation (non-binding, creates no obligations, no
follow-on is authorized):** both failures concern tail/financing robustness
rather than the central estimate — the rescaled drawdown exceeded the 25%
threshold by 0.002, and the 4%/yr gross-notional charge exceeds the observed
mean return while trading costs do not. The F-SNAP upper bound (−1.09) and
the control comparison (long-only Sharpe 0.81 vs signed 0.50) are consistent
with a panel where long-side exposure, not signed timing, dominated this
window. Criterion 2's margin is thin (+0.000453) and the 2010–2019 and
short-L bootstrap lower bounds are negative; per A12 the sample cannot
distinguish a modest true edge from zero. None of this changes the frozen
label or authorizes any action.

## 6. Disposition

- The single authorized evaluation (Part B: 1; B6 budget: 1) was consumed on
  2026-10-08. The evaluation budget is exhausted.
- **PROTO-TREND-001 is CLOSED as ECONOMICALLY INSUFFICIENT.**
- Not promotable: no forward demo, no candidate registration, no Phase IV,
  no Lane A evidence reuse, per A0/A7/A11 and B8.
- DISC-022 remains closed and unopened by this record (A10/B4).
- This closure record is the final artifact of the prototype's lifecycle.

## 7. Unresolved questions (not answerable from the frozen artifacts; no new
tests were run to answer them)

1. **Per-market gross contribution** was requested by IA-13 alongside
   turnover, but the frozen diagnostics persist only turnover per market;
   the contribution series cannot be recovered from the artifacts without a
   rerun (prohibited).
2. **Cutoff truncation logs** (rows dropped per series at 2026-09-30, IA-16)
   were computed during the run but are not persisted in results.json or
   REPORT.md; they cannot be inspected post hoc without a rerun.
3. **Drawdown episode geometry** (start/end months of the rescaled peak-to-
   trough path) is not recorded in the frozen outputs; deriving it would be
   new analysis outside this read-only record.
4. **Counterfactual with SI=F present** is unknowable: the universe was
   frozen at 14 series before execution; any comparison would be a second
   evaluation (prohibited by B6/B8).
5. **True historical financing cost** over 2010–2026: F-SNAP is an
   upper-bound static-swap stress by pre-declaration; actual broker swap
   history is not in the artifacts.
6. **Whether a modest true edge exists:** criterion 2's thin margin and the
   A12 power statement leave this statistically open; resolving it would
   require data or tests beyond the frozen budget.

## 8. Integrity confirmation

All frozen specification, authorization, code, universe, data and evaluation
artifacts were verified byte-identical (sha256) before this record was
written and were not modified by it. No evaluator was executed for this
record; no new experiment, rerun, determinism run, backtest, simulation,
parameter search, optimization or data acquisition occurred. No commits or
pushes. Forward runtime, supervisor, MT5 connection and recorders untouched.
