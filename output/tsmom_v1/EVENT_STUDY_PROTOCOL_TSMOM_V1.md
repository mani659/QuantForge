# QUANTFORGE — EVENT STUDY PROTOCOL — TSMOM V1 (TIME-SERIES MOMENTUM)

**Protocol version:** 1.0.3 (amended per execution-stop economic-layer remediation)
**Status:** FROZEN — corrected pre-registration, still before any outcome inspection.
**Date of freeze (v1.0.0):** 2026-08-12
**Date of amendment (v1.0.1):** 2026-08-12
**Date of amendment (v1.0.2):** 2026-08-12
**Date of amendment (v1.0.3):** 2026-08-12
**Project state:** QuantForge Engine COMPLETE/FROZEN; Strategy Assembly V1 FROZEN; Mean-Reversion line CLOSED (DISC-021); TSMOM selected as next research candidate (External Behavioral Hypothesis Discovery & Screening V1).
**Experiment output root:** `output/tsmom_v1/`
**Integrity rule:** This protocol is the only artifact at pre-registration/amendment time. No outcome data, event dataset, result table, or analysis script may exist until this protocol has passed independent final re-audit.

---

## 0. Amendment Record

### v1.0.1 (prior)
- **Findings addressed:** F-1 (EURUSD cost data misclassified), F-2 (artificial volatility cap removed from primary), F-3 (primary inference switched to multivariate calendar block bootstrap), F-4 (sample table index labels corrected), F-5 (PANIC percentile window defined), F-6 (explicit scientific interpretation categories), F-7 (first-month turnover convention), F-8 (TEST power clarified). F-9 required no change.
- **Statement:** No scientific outcome was inspected during that amendment.

### v1.0.2 (prior)
- **Findings addressed:**
  - **R-1 (F2/TEST inference made executable):** the multivariate calendar block bootstrap (L = 12) is infeasible on the TEST window (T_TEST ≈ 8 calendar months < L). F2 now has a fully pre-registered, deterministic, computable inference: pooled point estimate + directional sign + an **exact one-sided sign-flip (Rademacher) permutation test** by exhaustive enumeration (2^T_TEST assignments). `L_F2 = min(12, T_TEST)` is explicitly rejected with justification (see Section 11). The Holm family remains {F1, F2} and is mathematically executable.
  - **R-2 (block bootstrap mechanics):** the F1 calendar-block bootstrap draw/truncation mechanics and the ragged per-market F1-window representation are now specified exactly (see Section 11).
  - **R-3 (NC1):** NC1 (run-shuffle) is demoted to an exploratory run-structure diagnostic; it does not preserve contemporaneous cross-market dependence and cannot be the primary statistical null. NC2 (time shift) remains the formal negative control. The confirmatory family is not expanded.
- **Statement:** No scientific outcome was inspected during this amendment. Only protocol text, the re-audit findings, and arithmetic on pre-registered sample sizes were used.
- **Statement:** The TSMOM hypothesis and the confirmatory scientific question are unchanged: sign of the past 12-month return (skipping the most recent month) predicts the sign of the future one-month return. The primary confirmatory test (F1), the uncapped MOP-faithful weighting, the five-market universe, the chronological partitions, the economic cost gate, and the observed/assumed/unobserved cost distinction are all unchanged.
- **Status:** This remains a corrected pre-registration. No experiment has been executed; no engineering is authorized by this amendment.

### v1.0.3 (current)
- **Execution-stop remediation (Option A — dimensionally consistent economic accounting):** TSMOM V1.0.2 execution was correctly STOPPED before any outcome computation because the registered cost construction (`TO_m × h̄`, turnover normalized by gross exposure) is dimensionally inconsistent with the registered pooled statistic `π_m = mean_i(p·R)` (a mean of leverage-weighted returns), understating costs by approximately the average position leverage (≈ N/Σ|p| ≈ 0.37; costs ~2.7× understated) and inflating break-even by the same factor. This amendment adopts **Option A**: the primary return statistic `π_m = mean_i(p_{i,m}·R_{i,m})` is preserved unchanged, and the monthly net series is redefined as `π_m^net = mean_i( r_{i,m} − C_{i,m} )` with per-market traded-unit cost `C_{i,m} = |Δp_{i,m}|·h_{i,m}` (plus the final-close term), which is dimensionally identical to `r_{i,m}` (see Section 10). The old turnover-based drag and its break-even formula are retired; turnover remains a reported diagnostic only. This supersedes the provisional G-3 reading of the net series.
- **Statement:** The scientific hypothesis and the confirmatory statistical machinery (F1 block bootstrap, F2 sign-flip, controls, sensitivities, partitions, TEST protection) are unchanged. Only the economic accounting is corrected.
- **Statement:** No scientific outcome was inspected during this amendment. Execution stopped before any return, signal, weight, cost, or bootstrap value was computed.
- **Status:** This remains a corrected pre-registration. No experiment has been executed; no engineering is authorized by this amendment.

---

## 1. Scientific Hypothesis (primary)

> The sign of a sufficiently long-horizon past return predicts the sign of the future return in the same direction (continuation), at monthly frequency.

Operational form for this experiment:

> For instrument *i* and assessment month-end *m−1*: if the cumulative return of instrument *i* over the twelve months *m−12 … m−2* (skipping the most recent month *m−1*) is positive, hold a long position over month *m*; if negative, hold a short position over month *m*. The direction-adjusted forward monthly return is positive on average across the universe, and remains positive after observed transaction costs.

This is the **opposite** scientific claim to the closed Mean-Reversion line (reversion vs. continuation). Mean-Reversion methodology is not reused or repurposed anywhere in this protocol.

## 2. Architectural Decision: Design Type

**Decision: Type B — time-series predictive-return experiment, with an event-population wrapper for pipeline compatibility.**

- The scientific observation unit is the **monthly signal assessment per instrument**, not a tick-triggered behavioral event.
- The old Mean-Reversion event model (displacement → recoil → persistence, separation windows, intraday forward horizons) is **not forced** onto TSMOM. Monthly assessments are naturally non-overlapping; no overlap-suppression machinery is required or applied.
- The frozen QuantForge research machinery **is** used for: reproducibility, chronological partitioning, experiment identity, OOS discipline, statistical inference discipline, and economic viability. Those are pipeline properties, not signal semantics.
- Consequence: the "event population" of this experiment = the set of all assessment month-ends (one per market per month, from warm-up to data end). This population is defined before outcomes.

## 3. External Primary Source

**Anchor (primary):** Moskowitz, Ooi, Pedersen (2012), *Time Series Momentum*, Journal of Financial Economics 104(2), 228–250.

Canonical specification as published (confirmed against the paper and Quantpedia's implementation summary):

| Element | Published value |
|---|---|
| Universe | 58 futures: 24 commodity, 12 FX pairs, 9 equity index, 13 government bond |
| Lookback | Past 12-month excess return |
| Skip period | Most recent month (to avoid short-term reversal contamination) |
| Holding horizon | 1 month |
| Signal | Sign of the past 12-month (skipped) excess return → long if +, short if − |
| Position sizing | Inversely proportional to ex-ante volatility (GARCH in source paper; Quantpedia notes historical volatility is acceptable) |
| Rebalancing | Monthly |
| Sample | 1965–2009 |
| Reported performance | Alpha ≈ 20.7% p.a. (Fama-French), monthly return ≈ 1.26% (Table 3 Panel A), vol ≈ 15.7%, Sharpe ≈ 1.31, max drawdown ≈ −33.9% |

**Secondary anchor (robustness context):** Hurst, Ooi, Pedersen (2017), *A Century of Evidence on Trend-Following Investing*, Journal of Portfolio Management 44(1), 15–29 — 67 markets, 1880–2016, positive average returns in every decade; per-market Sharpe ≈ 0.4; diversified gross Sharpe ≈ 0.7–0.8 with positive net-of-cost Sharpe in every decade.

**Core hypothesis preserved verbatim:** the past 12-month return positively predicts the future return.

## 4. QuantForge Translation

- Universe: 5 spot markets (XAUUSD, EURUSD, BTCUSD, XAGUSD, USATECHIDXUSD). Spot, not futures → no roll; carry not included (documented deviation D5/D6).
- Prices: M1 OHLC close series, aggregated deterministically to daily and monthly closes (Section 6).
- Assessment cadence: monthly (calendar month-end).
- Signal: sign of the cumulative return over the 12 months *m−12 … m−2* (skip month *m−1*), computed at the month-end *m−1* close.
- Position over month *m*: direction = sign; size = vol-scaled (Section 5).
- Outcome: direction-adjusted monthly return over month *m*.

## 5. Primary Confirmatory Specification (exact)

For market *i*, calendar month *m*, with month-end close `C_{i,m}` (last populated UTC trading day of month *m*):

1. **Monthly return:** `R_{i,m} = C_{i,m} / C_{i,m-1} − 1`. Defined only when both boundary closes exist.
2. **Lookback cumulative return (signal input):** `L_{i,m} = Π_{k=m-12}^{m-2} (1 + R_{i,k}) − 1` (12 months, skipping month *m−1*).
3. **Signal:** `S_{i,m} = +1` if `L_{i,m} > 0`, else `−1`. (Zero treated as `−1`; zero probability in continuous prices; rule fixed for determinism.)
4. **Ex-ante volatility:** `σ_ann_{i,m}` = annualized standard deviation of the daily returns of market *i* over the 21 populated trading days ending at the assessment month-end *m−1*: `std(daily returns) × sqrt(252)`. If fewer than 5 daily returns exist in the window, market *i* has **no assessment** for month *m* (excluded, counted).
5. **Position weight (PRIMARY — MOP-faithful, uncapped):** `w_{i,m} = 0.40 / σ_ann_{i,m}`. No cap is applied. (0.40 = MOP annualized vol target per position, F-9: retained and attributed to the published methodology. The constant is scale-neutral across markets; relative weights depend only on `1/σ_ann`.)
6. **Position:** `p_{i,m} = w_{i,m} · S_{i,m}`.
7. **Direction-adjusted monthly return:** `r_{i,m} = p_{i,m} · R_{i,m}`.
8. **Portfolio return for month *m*:** `π_m = mean_i ( r_{i,m} )` over markets with an assessment for month *m*.
9. **Pooled confirmatory statistic:** mean of `π_m` over the pre-registered window (Section 8), annualized, with the F1 multivariate calendar block bootstrap CI (Section 11) and the F2 exact sign-flip test (Section 11), computed on the gross series and on the corrected net series `π_m^net` (Section 10).

**Primary confirmatory definition (one, not a grid):** the MOP 12-month-lookback / 1-month-hold / uncapped inverse-vol-scaled specification above, exactly. The capped variant `min(0.40/σ_ann, 2.0)` is an EXPLORATORY SENSITIVITY only (E9) and can never select or redefine the primary result.

## 6. Data Aggregation Rules (deterministic, no discretionary sessions)

Source: `data/m1/{MARKET}_M1.csv`, columns `timestamp,open,high,low,close,volume`, UTC timestamps, verified 0 duplicate timestamps and no missing OHLC in prior research (re-verified at execution via SHA-256).

1. **Trading-day bucket:** UTC calendar date (00:00:00–23:59:59.999 UTC). No per-market session windows. This is the single global, deterministic definition.
2. **Daily close** `d_t`: close of the last M1 bar with that UTC date. Days with zero bars are **skipped** (never fabricated).
3. **Daily return:** `close_t / close_{t-1} − 1` over consecutive populated trading days (a weekend/holiday gap yields one return spanning the gap — deterministic and kept).
4. **Month-end:** the last populated UTC trading day of each UTC calendar month.
5. **Monthly return:** per formula in Section 5 (needs both boundary month-end closes).
6. **Warm-up:** a market enters the assessment population at the first month-end *m−1* for which all twelve lookback months *m−12 … m−2* have complete monthly returns (equivalently: ≥13 full months of month-end closes before the first position month).
7. **Missing months:** a market with no data in a calendar month simply has no assessment that month; the portfolio mean is over markets with assessments (counts reported).
8. **Duplicate timestamps / missing bars / gaps:** counted and reported; no filtering.

## 7. Market Universe and Expected Sample (approximate; exact counts computed at execution)

Indexing convention (verified in audit F-4; formulas unchanged): the **assessment month-end** is the end of month *m−1* (signal computed there); the **position month** is month *m* (outcome over it). A market's first usable observation is its first assessment month-end.

| Market | M1 start | M1 end (approx) | First assessment month-end | First position month | Usable assessment months (approx) |
|---|---|---|---|---|---|
| XAUUSD | 2021-04 | 2026-04 | end 2022-04 | 2022-05 | ≈ 48 |
| EURUSD | 2021-01 | 2026-06 | end 2022-01 | 2022-02 | ≈ 53 |
| BTCUSD | 2021-05 | 2026-05 | end 2022-05 | 2022-06 | ≈ 48 |
| XAGUSD | 2021-07 | 2026-07 | end 2022-07 | 2022-08 | ≈ 48 |
| USATECHIDXUSD | 2023-09 | 2026-07 | end 2024-09 | 2024-10 | ≈ 22 |
| **Pooled** | | | | | **≈ 219** |

- **USATECHIDXUSD limitation (documented, not silently modified):** ~22 usable assessments; its results are reported separately and its exclusion from the pooled portfolio is reported as an explicit sensitivity (E7), never silently dropped.
- No markets are added during the experiment.
- Effective independence: monthly signals are serially dependent (sign runs). Report per market: number of assessments, number of sign transitions (flips), mean run length. **The pooled ~219 observations are NOT 219 independent events** — inference respects time dependence (Section 11).

## 8. TRAIN / VALIDATION / TEST

Per market, on that market's ordered list of usable assessment months (length `N_i`):

- Split points: `A_i = floor(0.70 · N_i)`, `B_i = floor(0.85 · N_i)`.
- **TRAIN:** assessment months 1 … `A_i`.
- **VALIDATION:** months `A_i+1` … `B_i`.
- **TEST:** months `B_i+1` … `N_i` (final 15%, the pre-authorized single-use holdout).

Because **no parameter is estimated from QuantForge data** (the specification is fixed by the published literature), every period is out-of-sample with respect to the methodology. The partitions serve (a) pre-registered discipline and (b) temporal-stability reporting:

- **F1 (primary, statistical power):** pooled `π_m` over TRAIN + VALIDATION (first 85%).
- **F2 (fresh holdout corroboration):** pooled `π_m` over TEST (final 15%) — used exactly once.

Rules: VALIDATION is never inspected-and-retuned; TEST is never revisited after the pre-registered verdict; no cell selection across lookback/horizon/market occurs anywhere.

**TEST power and protection (F-8 + R-1, explicit):** TEST is a protected holdout, not a substitute for the full scientific assessment. USATECHIDXUSD has very few TEST observations (~3–4); pooled TEST power is limited. TEST is **corroborative**: a non-significant TEST does NOT automatically mean the hypothesis is contradicted — the interpretation categories (Section 16) govern. F2's p-value is computed by the **pre-registered exact sign-flip permutation test fixed at protocol v1.0.2** (Section 11); no alternative F2 inference may be selected after seeing TEST results, and F2 cannot select any lookback, horizon, cap, volatility definition, or cost treatment. A positive F2 alone cannot confirm general TSMOM; F2 remains subordinate to the full scientific + economic promotion gate.

## 9. Primary Outcome and Report Measures

Primary outcome: direction-adjusted monthly portfolio return `π_m`. Report per window (full, TRAIN, VALIDATION, TEST) and per market:

- mean, median, hit rate (% positive months), standard deviation;
- annualized mean and annualized Sharpe of the pooled portfolio;
- F1: 95% percentile multivariate-calendar-block-bootstrap CI + one-sided bootstrap p-value (Section 11);
- F2: point estimate, directional sign, exact sign-flip one-sided p-value (Section 11);
- effect size (mean/σ), not raw PnL, as the primary magnitude measure.

## 10. Economic Viability Layer

**Principle (DISC-021):** statistical significance is insufficient; the effect must survive observed transaction costs. The literature's "net of cost" claim does not automatically transfer to these instruments — it is measured here.

1. **Cost source — genuine bid/ask markets (4 of 5):** observed MT5 bid/ask tick files `data/tick/{MARKET}_mt5_ticks.csv` (`date,time,bid,ask,last,volume`) for **BTCUSD, XAGUSD, XAUUSD, USATECHIDXUSD** — the same data class already characterized for XAGUSD. Observed spread evidence remains mandatory for these markets.
2. **EURUSD — observed spread UNOBSERVED (F-1, explicit):** `data/tick/EURUSD_mt5_ticks.csv` is an **M1 OHLCV minute-bar export** (`date,time,open,high,low,close,volume`), NOT a bid/ask tick stream. It MUST NEVER be treated as bid/ask evidence, and **no synthetic spread may be derived from OHLC data**. The EURUSD economic analysis therefore uses a pre-registered assumption: one-way spread = **0.1 bp per side (ASSUMPTION, not observed)**, with an explicit assumption band {0.1, 0.5, 1.0, 2.0} bp per side reported as a sensitivity table (E10). No broker cost is invented and presented as observed.
3. **Matching (bid/ask markets):** entry timestamp = last M1 bar of month *m−1*; exit timestamp = last M1 bar of month *m*. For each, take the nearest tick quote within ±60 s; if none, widen to ±600 s; if still none, that leg is **UNOBSERVED** (counted, coverage % reported).
4. **Cost per trade (bid/ask markets):** half-spread `(ask − bid)/2 / mid`, in basis points, at the matched quote. Round trip = entry + exit half-spreads (≈ full spread).
5. **Position-change accounting (F-7, corrected for Option A):** `Δp_{i,m} = p_{i,m} − p_{i,m−1}`, with `p_{i,0} = 0` (initial entry measured from zero exposure). Holding an unchanged position ⇒ `Δp = 0` ⇒ zero transaction cost. Increasing/decreasing exposure charges only the traded increment `|Δp|`. Full reversal `+p → −p` ⇒ `|Δp| = 2p`, charging exactly the economically correct traded exposure (sell p units at one half-spread + buy p units at one half-spread); **no extra factor is applied** — the result follows directly from the position-change definition.
6. **Actual per-market cost contribution (Option A — the ONLY cost entering the net series):** `C_{i,m} = |Δp_{i,m}| · h_{i,m}`, where `h_{i,m}` is the one-way half-spread (bp) sampled at the rebalance timestamp at the end of month *m−1* (entry into `p_{i,m}`); for the final position month *N*, an additional closing cost `|p_{i,N}| · h_{i,N+1}` is charged, where `h_{i,N+1}` is the half-spread sampled at the end of month *N* (exit). **Dimensional check:** `|Δp|` is dimensionless notional units and `h` is a per-unit fraction, so `C_{i,m}` is in the same return units as `r_{i,m} = p_{i,m}·R_{i,m}` — both sides of `π_m^net` are dimensionally identical. `h_{i,m}` for EURUSD = registered 0.1 bp/side ASSUMPTION (Section 10.2, band E10); for the four bid/ask markets = observed matched half-spread (item 4). Commission/slippage sensitivity (item 10) adds `|Δp|·c` per traded unit.
7. **Monthly net series (corrected):** `π_m^net = mean_i ( r_{i,m} − C_{i,m} )` over markets with an assessment for month *m*. The F1/F2 net statistics, net CIs (Section 11 inference applied to the net series), and net point estimates are computed on `π_m^net`.
8. **Turnover (REPORTED DIAGNOSTIC ONLY — not the cost input):** `TO_m = Σ_i |Δp_{i,m}| / Σ_i |p_{i,m}|` (mean over months = monthly turnover; annualized = 12 × mean). First-month convention: `p_{i,0} = 0` ⇒ `TO_1 = 1.0`. `TO_m` is a normalized diagnostic (fraction of gross exposure traded) reported alongside the actual cost contributions; it is **never used as a substitute for `C_{i,m}`** in `π_m^net` (the pre-1.0.3 dimensionally inconsistent drag is retired).
9. **Break-even one-way cost (corrected, derived from `net expectancy = 0`):** pooled `h* = Σ_m Σ_i r_{i,m} / V` and per-market `h*_i = Σ_m r_{i,m} / V_i`, where `V_i = Σ_{m=1..N} |Δp_{i,m}| + |p_{i,N}|` (total traded volume including the final close) and `V = Σ_i V_i`. Units: leverage-weighted return per unit traded — identical to the units of the observed/assumed half-spread (bp). Behavior checks: unchanged position ⇒ no trading ⇒ `h*` undefined (reported as such; not relevant); full reversal ⇒ `|Δp| = 2p` per unit of return; zero final exposure ⇒ no closing cost. The gate compares `h*` against the pooled observed median one-way half-spread.
10. **Commission / slippage:** **UNOBSERVED.** Pre-registered assumption band: {0, 0.5, 1, 2} bp per side, added to `C_{i,m}` as `|Δp|·c` per traded unit, reported as a net-sensitivity table. The primary verdict uses 0 bp commission + observed spread (and the EURUSD 0.1 bp/side assumption); every other cell is labelled an assumption.
11. **Per-market spread distributions at rebalance timestamps:** P50/P75/P90/P95/P99 — computed at execution-time for the **four bid/ask markets only** (same machinery as `output/xagusd_cost_viability_v1/`). EURUSD is excluded from spread-distribution reporting (spread UNOBSERVED).

## 11. Statistical Inference

- **Dependence structure:** monthly TSMOM assessments are serially dependent (12-month overlapping lookbacks and persistent sign runs) and **contemporaneously dependent across markets** (shared macro episodes). Both must be preserved by inference.
- **PRIMARY F1 inference — multivariate calendar block bootstrap (exact mechanics, v1.0.2/R-2):**
  1. **Panel:** the F1 union calendar panel = the ordered set of calendar months in which at least one market has an eligible F1-window assessment (ragged representation, below). Let `T_F1` = number of such months (≈ 46; per-market F1 lengths ≈ 41–45).
  2. **Ragged representation:** F1 = the first 85% of each market's own usable assessment series (months 1 … `B_i` with `B_i = floor(0.85·N_i)`). The union panel contains every calendar month in which ≥1 market has an F1 observation. For each calendar month, only markets that actually have an eligible F1 observation in that month contribute to `π_m` (Section 5.8). **No synthetic observations are created**; months with no contributing market do not enter the union panel.
  3. **Blocks:** all overlapping contiguous 12-month blocks of the ordered union panel: block `s` = months `s … s+11`, for `s = 1 … (T_F1 − 11)`. Number of blocks = `T_F1 − 11`.
  4. **Draw:** sample blocks **with replacement**, uniformly, in draw order, until the concatenated sequence has length ≥ `T_F1`. The draw sequence is fully determined by the fixed seed (20260812).
  5. **Truncation:** keep the first `T_F1` months of the concatenated sequence (the resampled panel has exactly `T_F1` months).
  6. **Multivariate preservation:** each resampled calendar month carries ALL markets' observations belonging to that original calendar month (a month-vector); markets without an eligible observation in that month contribute nothing. Contemporaneous cross-market dependence is therefore preserved within every resampled month.
  7. **Statistic:** for each resampled month, compute `π_m` over its contributing markets (Section 5.8); pooled statistic = mean of `π_m` over the truncated resampled panel.
  8. **Replicates:** B = 10,000. Report the 95% percentile interval of the replicate distribution and the **one-sided p-value** (hypothesized positive direction) = fraction of replicates with pooled mean ≤ 0.
- **F2 inference (v1.0.2/R-1 — executable, deterministic, pre-registered):** the multivariate calendar block bootstrap is **infeasible** on the TEST window: `T_TEST` ≈ 8 calendar months < L = 12. `L_F2 = min(12, T_TEST)` is **explicitly rejected**: with T_TEST ≈ 8, the only 8-month block reproduces the observed panel in every replicate (zero bootstrap variation → degenerate CI), and a shorter block would destroy the 12-month signal-construction dependence that L = 12 is designed to preserve while requiring an un-pre-registered block-length choice. F2 therefore uses an exact finite-sample procedure:
  1. **Pooled TEST point estimate:** mean of `π_m` over the TEST union calendar months (`T_TEST` ≈ 8; ragged representation as above, restricted to each market's TEST window).
  2. **Directional sign:** sign of that point estimate.
  3. **Exact one-sided sign-flip (Rademacher) permutation test:** enumerate **all** `2^T_TEST` assignments of ±1 to the `T_TEST` observed `π` values (T_TEST ≈ 8 → 256 assignments; exhaustive, deterministic, no RNG); under each assignment compute the mean; **F2 one-sided p-value** = (number of assignments with mean ≥ the observed mean) / `2^T_TEST`. Exact conditional on the observed magnitudes under the null that each `π_m` is symmetrically distributed around zero.
  4. **Assumption caveat (explicit):** serial dependence in the monthly `π` series makes the sign-flip test approximate; F2 is therefore corroborative only and can never confirm the hypothesis alone. The confirmatory load is on F1.
  5. No block-bootstrap CI is reported for F2.
- **Secondary (robustness only):** the run-cluster bootstrap (resampling contiguous same-sign signal runs within each market) is retained as a robustness analysis **only**. It is NOT the primary confirmatory inference because per-market run resampling breaks cross-market panel alignment; if it is reported, it is reported as robustness and cannot replace or override the primary CI.
- **Market dependence:** report the pairwise correlation matrix of direction-adjusted returns across the five markets; no independence is assumed.
- **Effective sample:** report pooled flips count and mean run length; interpret the effective independent signal count explicitly, and state the effective-sample limitation in the conclusions.
- **Multiplicity (confirmatory family, Holm α = 0.05, family size = 2 — mathematically executable):**
  - **F1:** pooled `π_m` over TRAIN+VALIDATION (gross and net); one-sided p-value from the block bootstrap (fraction of replicates ≤ 0).
  - **F2:** pooled `π_m` over TEST (gross and net); one-sided p-value from the exact sign-flip enumeration.
  - Both p-values are one-sided in the hypothesized positive direction; Holm-adjusted p-values reported for both. No other test enters the confirmatory family.
- **Negative controls (pre-registered, not decorative):**
  - **NC1 — run-shuffle (EXPLORATORY DIAGNOSTIC ONLY, R-3):** shuffle the order of signal runs within each market (preserving run lengths and returns, breaking the signal→return link). **NC1 does not preserve contemporaneous cross-market dependence** (per-market run shuffling breaks calendar alignment across markets) and therefore **cannot be used as the primary statistical null** for the pooled confirmatory result. It is reported as a run-structure diagnostic only.
  - **NC2 — time-shifted signal (FORMAL NEGATIVE CONTROL, R-3):** apply the month *m−1* signal to the outcome month *m+6* (truncated at data end); expected null; report point estimate and CI. NC2 preserves calendar alignment and the signal's autocorrelation structure while breaking the signal→outcome link, and is the formal dependence-aware null.
- **Falsification statement (the strongest test):** the hypothesis is NOT confirmed if the pooled direction-adjusted forward return is indistinguishable from zero on the pre-registered OOS layers (F1 CI includes 0), or if the net-of-cost pooled effect is ≤ 0 after observed transaction costs. Success is never "best among variants."

## 12. Walk-Forward / Temporal Stability (descriptive only)

- 4 fixed folds over each market's usable assessment months (quartiles) + a chronological-thirds view (consistent with V1–V3 reporting).
- Per fold: pooled mean, 95% CI, sign; portfolio equity curve and **max drawdown** (gross and net).
- No signal parameter is re-estimated or tuned per fold.

## 13. Momentum-Crash Diagnostics (no crash-avoidance strategy)

Pre-registered state definitions, information available at assessment time only (no look-ahead):

- **BEAR:** trailing 12-month return of market *i* at the assessment month-end ≤ −20%.
- **PANIC (F-5, explicit):** `σ_ann_{i,m}` above the 90th percentile of the **expanding** historical distribution of that market's own `σ_ann` values, where the percentile is computed only on `σ_ann` observations dated **before the assessment month-end** (no look-ahead). PANIC is **undefined** until at least **24 prior assessment-time `σ_ann` observations** exist for that market; before that minimum history, the state is classified as NOT-PANIC (and the count of undefined months is reported). The window is expanding (all history up to the assessment), never rolling-forward of future data.

Report (descriptive): mean direction-adjusted return and count in each state {BEAR∩PANIC, BEAR only, PANIC only, neither}, pooled and per market. If crash-state returns are strongly negative while non-crash returns are strongly positive, that is reported as a finding for a **separate future conditioning experiment** — never used here to filter trades. PANIC remains diagnostic only and is never a strategy filter.

## 14. Negative Controls (as in Section 11)

- **NC1** is a **run-structure diagnostic only** and cannot serve as the primary statistical null for the pooled confirmatory result (it does not preserve contemporaneous cross-market dependence).
- **NC2** remains the **formal time-shift negative control**.
- The confirmatory family is not expanded by either control.

## 15. Sensitivity Analyses (all EXPLORATORY SENSITIVITY — excluded from the confirmatory family and verdict)

- E1: lookback 6 months (12/1 spec otherwise unchanged).
- E2: lookback 24 months.
- E3: horizon 3 months (non-overlapping quarterly outcomes).
- E4: no volatility scaling (`w = 1`).
- E5: per-market cells (each market individually). **A positive result from a single market does NOT confirm general TSMOM (F-6).**
- E6: excess-return hurdle 0.25%/month subtracted from the lookback return (raw-return deviation check).
- E7: pooled portfolio excluding USATECHIDXUSD (its ~22-observation limitation).
- E8: cost-commission band {0, 0.5, 1, 2} bp/side (net sensitivity).
- E9 (F-2): capped volatility variant `min(0.40/σ_ann, 2.0)` — EXPLORATORY ONLY; it can never select or redefine the primary result, which remains the uncapped MOP-faithful rule.
- E10 (F-1): EURUSD one-way spread assumption band {0.1, 0.5, 1.0, 2.0} bp/side (net sensitivity).

All sensitivities: raw p-values, no Holm, no verdict; every one labelled EXPLORATORY.

## 16. Economic Success Criterion and Scientific Interpretation

### 16a. Economic gate (pre-registered, based on F1/F2 with observed costs)

| Class | Condition |
|---|---|
| **ECONOMICALLY VIABLE** | F1 net (corrected Option-A `π_m^net`: observed matched half-spreads where available, EURUSD 0.1 bp/side assumption, 0 bp commission) 95% CI lower bound > 0 AND F2 net point estimate > 0 AND pooled corrected break-even `h*` > pooled observed median one-way cost AND net remains > 0 at 1 bp/side commission |
| **ECONOMICALLY INSUFFICIENT** | F1 gross CI excludes 0 but corrected net CI includes 0 (observed costs consume the effect with no defensible margin) |
| **NOT CONFIRMED** | F1 gross 95% CI includes 0, or F2 sign is negative/opposed |
| **UNRESOLVED** | pooled flips < 15, or bid/ask cost-match coverage < 80% (excluding EURUSD, which uses the assumption), or pooled usable assessments < 30 → descriptive reporting only, no verdict |

No arbitrary profitability threshold is used; the margin test is the CI-lower-bound > 0 condition after observed costs plus the break-even comparison — both derived from observed evidence, not invented. F2's Holm p-value (sign-flip) is reported for completeness; the F2 gate uses the point estimate and net positivity, per Section 8.

### 16b. Scientific interpretation categories (F-6, explicit)

The scientific claim and the promotion question are reported separately:

- **REPRODUCED** — the primary pooled effect is positive and the protected holdout direction agrees, satisfying the pre-registered statistical and economic gates (F1 net CI lower bound > 0, F2 direction positive).
- **PARTIALLY REPRODUCED** — some continuation evidence exists (e.g., F1 gross CI excludes 0) but full confirmation is incomplete (economic gate not fully met, or holdout direction weak/negative).
- **CONTRADICTED** — evidence consistently opposes the continuation hypothesis (F1 gross CI ≤ 0 with consistent negative signs across periods).
- **INCONCLUSIVE** — evidence is insufficient to discriminate from noise (UNRESOLVED triggers).

**Explicit rule:** a positive result from a single market (E5) does NOT confirm general TSMOM. Per-market findings remain distinct from pooled/general conclusions and are never promoted as evidence of the general hypothesis.

## 17. Deviations Register (all labelled)

| ID | Deviation from MOP 2012 | Classification | Rationale |
|---|---|---|---|
| D1 | Raw return instead of excess return (no risk-free series for spot CFDs) | DATA-DRIVEN ADAPTATION | No T-bill series in repo; sign impact negligible (hurdle sensitivity E6) |
| D2 | 21-day historical vol instead of GARCH | DATA-DRIVEN ADAPTATION | Quantpedia explicitly permits historical vol; deterministic |
| D3 | 40% vol target retained; **no cap in the primary** (uncapped `0.40/σ_ann`, MOP-faithful); capped variant is exploratory only (E9) | DATA-DRIVEN ADAPTATION (target) + EXPLORATORY SENSITIVITY (cap) | F-2: the artificial 2.0 cap is removed from the primary; no additional cap is introduced |
| D4 | UTC calendar-day/month bucketing | DATA-DRIVEN ADAPTATION | Deterministic; avoids discretionary session definitions |
| D5 | 5 spot markets instead of 58 futures | DATA-DRIVEN ADAPTATION | Universe limitation, documented, not silent |
| D6 | No futures roll / carry | DATA-DRIVEN ADAPTATION | Spot instruments; removes roll noise |
| D7 | EURUSD spread UNOBSERVED; 0.1 bp/side assumption + band E10 | DATA-DRIVEN ADAPTATION | F-1: EURUSD tick file is an M1 OHLCV export, not bid/ask; assumption never presented as observed |
| D8 | F2 inference = exact sign-flip permutation test (block bootstrap infeasible on T_TEST ≈ 8 < L = 12) | DATA-DRIVEN ADAPTATION (inference only) | R-1: deterministic, pre-registered, executable; does not change the statistic or the gate; L_F2 = min(12, T_TEST) rejected with justification (Section 11) |
| E1–E10 | Lookback/horizon/scaling/universe/cost/cap cells | EXPLORATORY SENSITIVITY | Never part of the confirmatory family |

No deviation replaces the primary confirmatory definition.

## 18. Reproducibility Requirements (execution-time)

- Re-record SHA-256 fingerprints of all five `data/m1/*_M1.csv` and five `data/tick/*_mt5_ticks.csv` inputs.
- Record python, pandas, numpy, scipy versions; fixed seed 20260812; B = 10,000; block length L = 12; F2 exact sign-flip enumeration (2^T_TEST, T_TEST ≈ 8); net-series construction (Option A, Section 10): `π_m^net = mean_i(p·R − |Δp|·h)` with matched half-spreads and the final-close convention.
- Artifacts under `output/tsmom_v1/`: `experiment_metadata_TSMOM_V1.json`, `daily_series_TSMOM_V1.csv`, `assessment_events_TSMOM_V1.csv`, `cost_match_TSMOM_V1.csv`, `bootstrap_TSMOM_V1.csv`, `results_TSMOM_V1.json`, `SCIENTIFIC_REPORT_TSMOM_V1.md` (+ spread-distribution and net-sensitivity tables).
- No hidden manual filtering; every exclusion (warm-up, missing months, unmatched cost legs, USATECHIDXUSD cells, EURUSD assumption usage) counted and reported.
- The experiment must be replayable from this protocol alone, without conversational context.

## 19. Explicit Non-Goals

- No detector implementation; no BOE/Assembly/Deployment changes; no production thresholds; no runtime semantics; no crash-avoidance strategy; no optimization grid; no best-cell selection; no addition of markets; no reuse of Mean-Reversion event machinery.
- No outcome artifacts exist or may be generated by this amendment.
- The capped vol variant (E9) can never select or redefine the primary result.
- The EURUSD tick file is never treated as bid/ask evidence; no synthetic spread is derived from OHLC.
- F2 cannot select any lookback, horizon, cap, volatility definition, or cost treatment; no alternative F2 inference may be selected after seeing TEST results.
- The net series uses per-market traded-unit costs (`|Δp|·h`); the turnover ratio is a reported diagnostic and is never substituted for the cost input in the net series.
- The output of this experiment is scientific evidence only.

## 20. Stopping Rules

- STOP if any confirmatory precondition fails (universe/history/cost coverage per Section 16 UNRESOLVED) — report descriptively, no verdict.
- STOP before any verdict if TEST has been inspected more than the single pre-authorized use.
- STOP if any protocol change is needed after outcome inspection — any change requires a new protocol version (2.0.0) and is prohibited within V1.
- STOP if the multivariate calendar block bootstrap's fixed block length (L = 12) is altered after results are seen — no post-result tuning.
- STOP if the F2 inference method (exact sign-flip enumeration, fixed at v1.0.2) is altered after TEST results are seen — the method is fixed now.

---

*Frozen at 2026-08-12 (v1.0.0); amended v1.0.1 (F-1…F-8), v1.0.2 (R-1…R-3), and v1.0.3 (execution-stop economic-layer remediation, Option A), all prior to any outcome inspection. No analysis script, event dataset, or result artifact exists at amendment time.*
