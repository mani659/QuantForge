# PROTO-TREND-001 — Frozen Specification (DRAFT) and Evaluation Authorization Record (UNSIGNED)

**Status:** DRAFT for owner review. Nothing in this file authorizes data acquisition, evaluation, backtest or trading until the owner signs Part B. After signing, Part A is hashed and frozen; no edit afterwards.
**Drafted:** 2026-10-07. **Drafted by:** lead architect (AI), at owner request.
**Classification:** Lane B development artifact. NOT a QuantForge candidate, NOT research evidence, NOT a trade authorization, NOT a reopening of any closed line.

---

# PART A — FROZEN SPECIFICATION

## A0. Identifier and purpose
- **Identifier:** PROTO-TREND-001 (to be confirmed by the owner freeze instruction).
- **Question it answers (one):** does a fixed, literature-defined, volatility-scaled time-series momentum portfolio over a diversified set of liquid markets earn a net-of-cost return that is distinguishable from zero in the post-publication period 2010-01 to 2026-09, using only free daily data?
- **What a pass means:** eligibility for a pre-registered forward demo test. Nothing else. A fail closes this prototype. Neither outcome validates or refutes trend-following in general.

## A1. Source (primary; citations to be verified by the agent before freeze, correct citation text only, never the rule)
- Moskowitz, T., Ooi, Y. H., Pedersen, L. H. (2012), "Time series momentum," *Journal of Financial Economics* 104(2), 228–250. Rule parameters taken from this paper: 12-month look-back, 1-month holding period, ex-ante volatility from an exponentially weighted estimate with a 60-day centre of mass. The paper's per-instrument volatility target is 40%; this prototype uses 10% (scale only; Sharpe-invariant).
- Secondary corroboration only: Hurst, B., Ooi, Y. H., Pedersen, L. H. (2017), "A Century of Evidence on Trend-Following Investing," *Journal of Portfolio Management* 44(1), 15–29. Never substituted for the primary.

## A2. Universe (frozen before data access)
Candidate list, 15 markets. Free-data vendor and symbol are frozen per market; no vendor or symbol substitution after performance is computed.

| Class | Market | Vendor / symbol | Expected start |
|---|---|---|---|
| Equity index | S&P 500 | Yahoo `^GSPC` | 1927 |
| Equity index | Nasdaq-100 | Yahoo `^NDX` | 1985 |
| Equity index | DAX | Yahoo `^GDAXI` | 1987 |
| Equity index | FTSE 100 | Yahoo `^FTSE` | 1984 |
| Equity index | Nikkei 225 | Yahoo `^N225` | 1965 |
| FX | EURUSD | Yahoo `EURUSD=X` | 2003-12 |
| FX | GBPUSD | Yahoo `GBPUSD=X` | 2003-12 |
| FX | USDJPY | Yahoo `USDJPY=X` | 1996 |
| FX | AUDUSD | Yahoo `AUDUSD=X` | 2006-05 |
| FX | USDCAD | Yahoo `USDCAD=X` | 2003-09 |
| FX | USDCHF | Yahoo `USDCHF=X` | 2003-09 |
| Metal | Gold | Yahoo `GC=F` (continuous futures) | 2000-08 |
| Metal | Silver | Yahoo `SI=F` (continuous futures) | 2000-08 |
| Energy | Brent | FRED `DCOILBRENTEU` (spot) | 1987-05 |
| Crypto | Bitcoin | Yahoo `BTC-USD` | 2014-09 |

**Deliberate exclusions, recorded now:** WTI (spot and futures printed a negative price on 2020-04-20, which breaks return arithmetic; excluded rather than patched); government bonds (not confirmed tradable at the owner's broker); any instrument not found in the broker symbol inventory (gate G0 below).
**Tradability gate G0 (pre-data, read-only):** every market must have a tradable symbol on the owner's broker (MT5 symbol list). A market without one is removed from the universe BEFORE data acquisition. No other change is permitted by G0.
**G0 outcome (2026-10-07, read-only MT5 query):** all 15 markets are listed and report full trade mode. Universe unchanged. Broker symbols: US500m, USTECm, DE30m (DAX), UK100m, JP225m, EURUSDm, GBPUSDm, USDJPYm, AUDUSDm, USDCADm, USDCHFm, XAUUSDm, XAGUSDm, UKOILm (Brent), BTCUSDm. Bonds were not queried and none appear in the index, metal or energy lists. Static contract data (contract size, minimum volume, swap) are as returned; several tick-value fields came back as 0 or null and are not used.
**Unbalanced panel:** a market enters the panel on the first month with 12 months of valid history. N_t = markets active at month t.

## A3. Signal, sizing, portfolio (all frozen)
1. **Signal:** s_i,t = sign of the past 252-trading-day total return of market i, computed at the close of the last trading day of month t. Zero return → flat.
2. **Volatility estimate:** σ̂_i,t = annualised exponentially weighted standard deviation of daily simple returns, centre of mass 60 trading days, as of the same close.
3. **Position:** p_i,t = s_i,t × (0.10 / σ̂_i,t), fixed for the whole holding month. No leverage cap (reported as a diagnostic).
4. **Portfolio:** equal risk across active markets: R_P,m = (1/N_t) Σ_i p_i,t × r_i,m (return from the entry close to the next month's entry close).
5. **Rebalance:** monthly. Positions change only at monthly rebalance dates.
6. **Execution timing (no look-ahead):** signal uses data up to and including the close of the last trading day of month t; the trade is executed at the NEXT trading day's close. The holding return runs from that close to the corresponding close one month later.
7. **Vehicle:** price series as downloaded (spot or continuous front-month). No financing, swap, carry or dividend is imported into the primary result (disclosed limitation, see A9).

## A4. Costs (owner economic inputs; frozen in Part B §B3)
- Charged per side on traded notional |Δp_i| at each rebalance, with a per-class half-spread plus slippage in basis points. Proposed values are in Part B §B3. Observed Exness spreads informed them; they are assumptions, not broker facts (the same status as prior Lane B inputs).
- **Pre-declared cost grid (diagnostic only):** ×0.5, ×1 (primary), ×2, ×4. The verdict is taken at ×1 and nowhere else. The grid exists so that "unknown cost sensitivity" cannot recur as an open question.

## A5. Span and partitions
- **Verdict window:** 2010-01-01 to 2026-09-30 (post-publication; the primary paper's sample ends in 2009).
- **Reported but excluded from the verdict:** 2004-01 to 2009-12 (inside the published sample; shown to check that the rule behaves as the paper reports).
- **Diagnostic sub-periods inside the verdict window:** 2010–2019 and 2020–2026-09.
- **No sealed partition inside the data.** The rule is fixed from the literature, not fitted. The protection against selection is (a) one rule, (b) the pre-declared neighbourhood below and (c) a forward demo after any pass. The drafter (an AI) knows the history of this strategy family; this is disclosed as a limit on the evidence and is why a forward test is required.

## A6. Control (exactly one)
Equal-risk long-only portfolio of the same markets: same volatility scaling, same monthly rebalance, same costs, all signs fixed at +1. Used for comparison diagnostics only (relative Sharpe, drawdown), not for the verdict.

## A7. Primary outcome and pass criteria (all fixed before data access)
**Primary outcome (one):** mean net monthly return of R_P over the verdict window, with a 95% circular block-bootstrap interval (block length 12 months, B = 10,000, seed 20261007).
**PASS-TO-FORWARD requires ALL of:**
1. Net annualised Sharpe at primary cost ≥ 0.30.
2. One-sided 95% lower bound of mean net monthly return > 0.
3. Net Sharpe > 0 in BOTH 2010–2019 and 2020–2026-09.
4. Neighbourhood plateau: net Sharpe > 0 for look-backs of 3, 6 and 12 months (3 and 6 are diagnostics, not variants; they change nothing else).
5. Drawdown: maximum drawdown of the series rescaled to 10% annualised volatility ≤ 25%.
6. Financing stress: net Sharpe > 0 after a charge of 4% per year on gross notional.
**Any single failure → CLOSED (NEGATIVE or ECONOMICALLY INSUFFICIENT per A11).** No threshold may be changed after data access.

**Mandatory broker-swap diagnostic F-SNAP (reported for every outcome; not a pass criterion):** G0 shows retail CFD financing well above the generic 4% stress for some markets. For each market and side, annual financing rate = max(0, −swap_points) × point × 365 ÷ price, using the G0 swap values (held constant over the whole window) and the market's price at each rebalance; positive swaps (credits) are treated as zero. Charged on notional held per day. Approximate long-side rates from the G0 snapshot: gold 4.7%, silver 4.7%, Bitcoin 8.2%, EURUSD 1.8%, S&P 500 about 9% and Nasdaq-100 about 10% (the last two assume index levels the drafter could not see). Because 2010–2021 rates were far lower than today's, applying today's swaps to the whole window is an UPPER-BOUND stress, and the swap table itself moves from day to day. **Interpretation rule (pre-declared):** if all six criteria pass but F-SNAP net Sharpe ≤ 0, the closure label is **PASS-TO-FORWARD (FINANCING WARNING)**. The forward demo is then required to measure real swap charges on the broker before any further step.

## A8. Pre-declared diagnostic set (no other analysis permitted)
Per-market contribution and turnover; gross vs net; cost decomposition; leverage distribution (max, mean); exposure by class; realised volatility; skewness; yearly returns; ex-Bitcoin portfolio; cost grid; financing stress at 0/2/4/6%; sub-period split; look-back neighbourhood (3/6/12); correlation of R_P with the control; worst 10 months; number of active markets over time.

## A9. Mechanism and data risks (disclosed now)
- Continuous futures series (`GC=F`, `SI=F`) may contain roll gaps; the data gate flags any |daily return| > 8% for review and fails closed if unexplained.
- Spot FX and spot oil returns omit carry and roll yield; real CFD holding costs include swap. The financing stress (criterion 6) is a coarse proxy, not a model.
- Index series are price indices (no dividends).
- Cross-asset closes are asynchronous; the one-day execution lag limits, but does not eliminate, the effect.
- Bitcoin enters from 2014-09 and is highly volatile; equal-risk scaling bounds its weight, and an ex-Bitcoin result is reported.
- Free data vendors may revise or withdraw series; provenance hashes are taken at acquisition.
- The result concerns this rule on this panel only.

## A10. Distinctness (honesty item, as in the Batch-2 intake audit)
This prototype is **not distinct in mechanism** from DISC-022 (fixed 12/1 time-series momentum). It differs in universe (15 markets vs the 28-future panel and the 5-market M1 panel), era (2010–2026 post-publication vs 1987–2002 and 2022–2026), vehicle (price proxies of broker-tradable markets), cost treatment and report set. DISC-022's closure is untouched and is not reopened. The Lane B precedent is GEM and VM (momentum and sizing relatives admitted as Lane B prototypes). The owner decision is recorded in Part B §B4.

## A11. Data-integrity gate and closure taxonomy
**Fail-closed data gate (before any return is computed):** monotonic timestamps; no duplicate dates; no gap > 5 consecutive business days inside a market's active span; |daily return| > 25% (8% for `GC=F`/`SI=F`) flagged and individually reviewed; provenance hash per series; vendor terms retained. A market that fails is reported and handled ONLY by the removal rule: remove it BEFORE performance is computed, never substitute a vendor. If the remaining universe has fewer than 8 markets in 2010 → DATA-INTEGRITY STOP.
**Closure taxonomy:** PASS-TO-FORWARD; NEGATIVE; ECONOMICALLY INSUFFICIENT (gross passes, net fails); DATA-INTEGRITY STOP. Closure is permanent for this specification: no rescue, variant, rerun, parameter change or combination.

## A12. Evidence budget
About 200 monthly observations in the verdict window. Statistical power is modest: a true net Sharpe near 0.4 gives roughly a coin-flip chance of meeting criterion 2. A fail at this sample size is not strong evidence of no edge; the report must say so.

## A13. Implementation notes (outside the verdict; recorded now so they cannot be argued post-hoc)
- **Capital granularity.** The evaluation is capital-agnostic. A real book is not: at G0 minimum lots, one gold lot step is about 1 oz (about $4,200 of notional) and one silver step is 50 oz (about $3,100). On a small account those minimums would dominate the risk. Any forward demo must therefore run on a balance large enough that minimum lots are not binding (a demo balance of tens of thousands, or a funded account), and the portfolio must be sized by the rule, not rounded up.
- **Brent swap anomaly.** The G0 value for UKOILm (swap_short −125.3 points) implies an implausibly large nightly charge and is likely a roll-related artifact. It is excluded from F-SNAP; Brent's financing is covered by the generic stress only. The drafter did not see a basis to correct it.
- **Live data source.** A future live or forward system takes prices from the broker feed, not from the research vendors. Vendor data in this prototype is used for personal research only (B5).

---

# PART B — EVALUATION AUTHORIZATION RECORD (UNSIGNED)

**Classification:** Lane B Prototype Evaluation; NOT research evidence, NOT a candidate, NOT validation, NOT Phase IV, NOT a trade authorization.
**Authorization:** `Salman, 2026-10-08` — 1 frozen prototype, max 1 evaluation. **Recorded:** `2026-10-08`, BEFORE data acquisition and performance calculation; inputs fixed at authorization and immutable.
**Owner:** Salman

**Date:** 2026-10-08

**Authorization statement:**

> I authorize execution of the single bounded Lane B evaluation of PROTO-TREND-001 exactly as specified in Part A and Part B of the frozen specification. I authorize one data acquisition and one evaluation only. No optimization, variant search, rescue, parameter change, vendor substitution, universe substitution, or post-result rule change is authorized.

## B1. Authorized prototype and frozen-specification binding
| Prototype | Frozen specification | sha256 (first 16) | Evaluations authorized |
|---|---|---|---|
| PROTO-TREND-001 | Part A of this file, as signed | `4b44615dcf1646bd` | 1 |

## B2. Repository state captured before starting
HEAD / branch: `HEAD 666c1a9af38a05cde9fb2931d80a4f4c53846b1c / branch main. Working tree pre-start: 76 modified files, 126 untracked paths (porcelain counts; pre-existing workspace state, untouched by this task). No MT5 order or configuration call. No commit or push by the agent`. Working tree untouched areas: governance, architecture, recorder, engine. No MT5 order or configuration call. No commit or push by the agent.

## B3. Owner economic inputs

**Decision:** CONFIRMED.

I confirm the proposed B3 economic inputs exactly as specified:

| Class          | Spread (bps/side) | Slippage (bps/side) | Commission | Total per side |
| -------------- | ----------------: | ------------------: | ---------: | -------------: |
| FX majors      |               0.5 |                 0.5 |          0 |            1.0 |
| Gold           |               0.5 |                 1.0 |          0 |            1.5 |
| Silver         |               6.0 |                 1.0 |          0 |            7.0 |
| Equity indices |               1.0 |                 1.0 |          0 |            2.0 |
| Brent          |               3.0 |                 1.0 |          0 |            4.0 |
| Bitcoin        |               6.0 |                 1.0 |          0 |            7.0 |

These are owner-declared research assumptions, not broker guarantees. The pre-declared Ã—0.5 / Ã—1 / Ã—2 / Ã—4 cost grid remains diagnostic only, and Ã—1 remains the sole primary verdict cost.
## B4. Prototype-specific clarification

**Owner decision: ACCEPT.**

PROTO-TREND-001 is accepted as a bounded Lane B prototype despite its mechanism overlap with DISC-022.

This acceptance:

* does NOT reopen DISC-022;
* does NOT alter the closure of DISC-022;
* does NOT constitute evidence for or against TSMOM generally;
* authorizes only the single evaluation explicitly defined by this frozen specification.
## B5. Data-source authorization

**Owner approval: YES.**

I authorize the use of Yahoo Finance via the specified Batch 1 route and FRED for Brent solely for this personal, non-commercial research evaluation.

This authorization is restricted to:

* the exact series listed in Part A Â§A2;
* one acquisition;
* the frozen PROTO-TREND-001 evaluation;
* local research use only.

It does NOT authorize commercial deployment, automated commercial order generation, redistribution, production use of vendor data, or substitution of vendors.
## B6. Multiplicity and complexity budget (frozen)
Prototypes: 1. Evaluations: 1. Variants: 0. Parameter searches: 0. Filters: 0. Alternate universes, look-backs (other than the pre-declared diagnostic 3/6/12), windows, vehicles, holding periods, costs (other than the pre-declared grid), calibration windows: 0. Stops, targets, overlays, combinations: 0. Controls: 1 (A6). Primary outcome: 1 (A7).

## B7. No-look-ahead enforcement (mechanically applied)
Signal timing, data use and execution lag as in A3.6. The evaluation script must contain an automated check that no return after the signal date enters the signal or volatility estimate, and a unit test with planted data showing that the evaluation function can return a non-zero result when an effect is planted (the self-test that would have caught the OPEX "0.00 by construction" defect). The self-test runs on synthetic data only.

## B8. Prohibitions restated
No optimization, rerun, rescue, variants, combination, promotion, candidate registration or discovery. No post-result change of any threshold, cost or universe. No commit or push by the agent. Hard stop after one bounded report.

**Signature:** `Salman` — `2026-10-08` — "Execute the single authorized Lane B evaluation of PROTO-TREND-001."
