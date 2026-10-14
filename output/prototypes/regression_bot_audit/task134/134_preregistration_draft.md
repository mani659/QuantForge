# VS-TSMOM-01 Preregistration Draft (DESIGN ONLY — NOT AUTHORIZED FOR EXECUTION)

**Status:** draft prepared under TASK134 design authority within the B4
admitted track. NOT filed as approved. NOT permission to execute. B4
decision record: task133 file (`d1e1a823…`). DISC-022 closed and untouched.

## 1. Estimand (required item 1)

**Primary estimand:** mean paired monthly net differential
D(m) = R_volscaled(m) − R_buyhold(m), in decimal per month (reported also
in bps). Gross signal effects reported separately from net economic value:
gross differential, cost drag (turnover × frozen schedule), financing
stress, net differential. The economic question answered is "does the
vol-scaled rule beat passive holding after costs" — NOT "does scaling beat
fixed" (the fixed comparator is prohibited; see §8).

## 2. Data (required item 2; no substitution)

FRED `NASDAQ100` price index, `data/fred/fred_NASDAQ100.csv` (identity per
TASK129: 10,602 rows, 1986-01-02→2026-08-21, 3.41% missing, no year >5%).
Price-only: ~1%/yr distributions omitted — longs underperform true total
return; disclosed, directionally conservative for a net-long-tilted rule,
NOT corrected (no total-return series spans 1986 in-repo). Yahoo ^NDX
(total-return, from 1985) exists but substituting it would change the
admitted object — requires a separate owner decision, not made here.
Financing: no historical swap series exists — generic stress only (§4).
Tradability: index CFD assumed available; minimum-lot granularity
unaddressed (forward-demo matter, not this test).

## 3. Frozen strategy specification (required item 3)

- Signal: r12 = P(T)/P(T−12 calendar months) − 1, T = last trading day of
  month; direction = sign(r12), zero → flat.
- Volatility: prior calendar month realized volatility, annualized
  (std of daily simple returns × √252) — VM-001 monthly-variance pattern,
  documented as pattern choice.
- Position: w = sign(r12) × min(1, 0.10/σ); target_vol 10% carried from
  TASK128 draft, arbitrariness disclosed (no source basis; predeclared).
- Rebalance monthly; execution next session open (GEM Month-End/Next-Day
  pattern); trade only on target change.
- Bounds [-1,+1] (no leverage, stated risk bound).
- Missing data: >5% missing in any span-year → STOP; timestamp duplicates
  fail closed (RS-404 amendment-5 pattern); no fill, no interpolation.
- Lagging: every input bar has timestamp ≤ its use point (signal uses
  closes ≤ T; vol uses strictly prior month).

## 4. Cost model (required item 4; declared, not broker-factual)

Primary at Batch-1 family (spread 10 / slippage 5 / commission 0 bps per
side), declared as research assumption per PROTO-TREND-001 B3 precedent —
NOT a broker fact. Sensitivity grid ×0.5/×1/×2/×4 (IA-8 pattern).
Financing stress 0%/2%/4% per year on gross notional (IA-10 pattern),
labeled stress-only. Turnover reported. No invented broker schedule.

## 5. Inference (required item 5)

Circular block bootstrap on the paired differentials: block 12 months,
B=10000, seed 20261014 (arbitrary-but-fixed, labeled). Addresses serial
dependence (monthly differentials autocorrelate) and heteroskedasticity
(percentile method) without parametric assumptions. Single primary
comparison → no multiplicity correction (stated; any added comparison
creates a new preregistration). Researcher DFs: none — one outcome, one
test, predeclared.

## 6. Chronology (required item 6; single window)

Single evaluation window: first evaluable month (~1987-02, after 12m
signal + 1m vol warmup) → 2026-08. NO development/validation/final split:
this deliberately departs from the TASK128 draft to cure its Defect 6
(development-informed thresholds = post-outcome parameters). All bars
frozen here, before any outcome access. No holdout exists; protection is
procedural (freeze-then-run), stated plainly.

## 7. Thresholds (required item 7; no invented magnitude bar)

- PASS: one-sided 95% bootstrap lower bound of mean paired net
  differential > 0 (pattern precedent; α=0.05 convention).
- FAIL: upper bound < 0.
- INCONCLUSIVE: interval includes zero.
Economic magnitude (annualized net Sharpe, mean bps) reported
descriptively; no magnitude bar invented. Owner may impose one — flagged
as owner-optional, not set here.

## 8. Comparator audit (required item 8)

Fixed-TSMOM appears NOWHERE: no leg, no benchmark, no diagnostic computed
from it. Benchmark is buy-and-hold NASDAQ100 (lawful passive-control
precedent: GEM unconditional-SPY control; PROTO-TREND-001 all-+1 control).
The vol-scaled leg's r12 content is the B4-admitted overlap — distinguished
from a comparator (admitted object vs prohibited benchmark).

## 9. Power limitations (required item 9)

TASK125/126 XSM findings do NOT transfer (different design, universe,
estimand — stated, not generalized). This design: ~470 monthly paired
differentials, single predeclared test, no interim looks. No power claim
is made (a power study would be a simulation — prohibited in this task);
the CI width will speak. Underpowered-relative-to-what is unanswerable
without the owner's magnitude bar (§7).

## 10. Execution-authorization request (required item 10; UNAPPROVED)

Separate file in this package. Requests: SHA verification → freeze check →
synthetic self-test → ONE bounded execution → bounded report; named FRED
file only; no sweeps/reruns/variants; stops as in §5 of the limitations
register. This request grants nothing.
