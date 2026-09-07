# QUANTFORGE — LIQUIDITY SWEEP / REVERSAL
# STRATEGY & ECONOMIC TRANSLATION V1

## 0. Identity and Method

- **Stage:** post-adjudication economic/strategy translation of the XAUUSD Liquidity Sweep / Reversal V1.2.0 behavioral result.
- **Authorizing adjudication:** `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_SCIENTIFIC_ADJUDICATION_V1.md` — **A — ADVANCE TO ECONOMIC / STRATEGY TRANSLATION** (scoped to XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD; EURUSD excluded by the unresolved data-quality gate).
- **Frozen behavioral protocol:** `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_EVENT_STUDY_PROTOCOL_V1.md` (v1.2.0). No behavioral element was modified.
- **Baseline registration:** the single baseline translation (rules below) was **registered before any computation**; nothing was tuned, searched, or selected by outcome. One baseline implementation only, per the stage firewall.
- **Data:** frozen v1.2.0 event CSVs (persisted); `data/m1/*_M1.csv` (verified input hashes); **observed** MT5 tick bid/ask `data/tick/*_mt5_ticks.csv` (XAUUSD/BTCUSD/USATECHIDXUSD streamed for this stage; XAGUSD via the pre-existing per-minute aggregate `output/xagusd_cost_viability_v1/xagusd_minute_aggregates.csv`).
- **Analysis scripts (scratch, read-only, not repository artifacts):** `scratch/lsweep_econ_v1/extract_spreads.py`, `scratch/lsweep_econ_v1/simulate.py`, results `scratch/lsweep_econ_v1/results_v1.json`.

---

## 1. Executive Verdict

**ECONOMICALLY NON-VIABLE — for the registered minimal executable translation, in all four validated markets, gross (before any cost).**

The minimal translation of the validated behavior — **entry at the confirmation close, direction short/long by sweep side, structural stop at the frozen sweep-candle extreme, exit at the close of the 120-minute behavioral horizon** — has a **negative median gross PnL in every market** (XAUUSD −5.3 bp, XAGUSD −11.6 bp, USATECHIDXUSD −5.0 bp, BTCUSD −11.8 bp per trade), win rates of 19–26%, stop-out rates of 70–80%, and negative economics in **every year and in both chronological halves** of every market. Observed transaction costs are **not** the binding constraint: the translation is already gross-negative before spread, commission, or slippage.

**The behavioral discovery stands** (the excursion phenomenon is statistically validated and unaffected by this stage). **The candidate does not become a bot** under this translation: no demo/live path is authorized from this baseline. Structurally different translation concepts (entry/exit alternatives) are identified in §16 as future, separately pre-registered studies — they were deliberately NOT tested here (that would constitute exit/entry mining, which this stage prohibits).

---

## 2. Behavioral Evidence Being Translated

Adjudicated behavioral object (unchanged): a strict breach of the prior Asian-session extreme → wick rejection (close-failure) → deterministic micro-structural confirmation (first later close beyond the frozen sweep-candle extreme) → larger 120-minute directional excursion than control, significant after Holm in all four evaluable markets.

**What the behavior measures — and what it does not:** the primary response is **MFE anchored at the swept Asian level** (`AsianHigh − min(low)` / `max(high) − AsianLow` over 120 min) — a maximum excursion from the *Asian extreme*, not a captureable entry-to-exit PnL. Median treatment MFE from the Asian level (this stage, bp): XAUUSD 23.0, XAGUSD 48.2, USATECHIDXUSD 24.2, BTCUSD 55.8. This is the ceiling the economics must translate.

---

## 3. Market Scope

| Market | Status | Treatment events | Event window | Trades simulated |
|---|---|---|---|---|
| XAUUSD | EVALUABLE | 1527 | 2021-04-13 → 2026-04-10 | 1517 |
| XAGUSD | EVALUABLE | 1517 | 2021-07-13 → 2026-07-10 | 1507 |
| USATECHIDXUSD | EVALUABLE | 984 | 2023-09-01 → 2026-07-10 | 972 |
| BTCUSD | EVALUABLE | 1960 | 2021-05-24 → 2026-05-22 | 1941 |
| EURUSD | EXCLUDED (data gate) | — | — | — |

Events excluded from simulation only for a missing 120-minute exit bar in the M1 record (10–19 per market, 0.6–1.0%): the same completeness rule as the behavioral protocol's §10.

---

## 4. Baseline Entry

- **Rule (registered a priori):** enter at the **close of the confirmation bar** (the first M1 close satisfying the registered reversal confirmation) — a market order at that close. No additional confirmation, no confluence, no filter.
- **Direction:** upper sweep → SHORT; lower sweep → LONG.
- **Effective timing:** entry sits **beyond** the swept Asian level by (median): XAUUSD 5.2 bp, XAGUSD 11.3 bp, USATECHIDXUSD 4.7 bp, BTCUSD 13.2 bp. The confirmed reversal has already moved from the Asian extreme to the confirmation close before any trade exists.
- **Residual excursion available from entry** (median MFE-from-Asian − entry offset): XAUUSD ≈ 17.8 bp, XAGUSD ≈ 36.9 bp, USATECHIDXUSD ≈ 19.5 bp, BTCUSD ≈ 42.7 bp — i.e., the market does on average move substantially farther in the reversal direction *at some point* inside the 120-minute window.

## 5. Baseline Invalidation (Stop)

- **Rule (registered a priori):** structural invalidation = the **frozen sweep-candle extreme** — for upper sweeps, the rejection (sweep) candle's High; for lower sweeps, its Low. Stop evaluated from the bar after entry; fill at the stop level; stop-first on the bar where stop and exit coincide. No tick/pip optimization beyond the structural point.
- **Effect:** the stop sits beyond the Asian level in the *adverse* direction, so its distance from entry is the sweep-wick distance plus the entry offset. **Stop-out rate: 70–80% across markets** (XAUUSD 76.5%, XAGUSD 75.5%, USATECHIDXUSD 79.5%, BTCUSD 70.3%). Median holding time 18–31 minutes. The typical trade has an early favorable excursion (the validated behavior) and then **reverts through the entry and the stop within the 120-minute window**; the stop converts the reversion into a full sweep-distance loss.

## 6. Baseline Exit

- **Primary exit (registered a priori):** close of the M1 bar exactly **120 minutes after entry** — the direct translation of the validated measurement window, selected on market mechanics (it is the window over which the effect was established), not on historical profitability.
- **Consequence:** the realized exit is the 120-minute *close*, not the MFE extreme. The validated excursion peaks intra-window and is not captured by a fixed-horizon close.
- **Registered alternatives (NOT tested, NOT optimized — see §16):** exit at the Asian opposite boundary; structural trailing exit; partial/time-based exits.

## 7. Cost Model (observed)

- **Observed spreads:** per-minute median bid/ask spread from the MT5 tick files at the entry and exit minutes. Lookup quality: **exact-minute matches 98.3–99.4%** of lookups; ±5-min fallback 0.0–0.9%; market-median fallback 0.2–1.5% (flagged). The cost model is therefore based on observed quotes, not assumptions, for all four markets.
- **Round-trip cost conventions (as the XAGUSD precedent):** Model A (standard) RT = (s_entry + s_exit)/2; Model B (conservative) RT = s_entry + s_exit, where s is the full spread in bp.
- **Observed round-trip cost, Model A (median / P90), bp:** XAUUSD 1.73 / 2.09; XAGUSD 12.30 / 14.30; USATECHIDXUSD 1.05 / 1.91; BTCUSD 16.77 / 34.87.
- **Unobserved components (commission, slippage):** no broker schedule exists in the repository (same finding as the XAGUSD study). Bands applied: commission 0/2/5/10 bp RT; slippage 0/2/5 bp RT.

## 8. Risk Model

- Fixed notional of 1 unit per trade; no compounding; no sizing optimization; per-trade metrics in bp (instrument-agnostic). Equity-curve drawdown reported per unit notional (bp).

## 9. Trade Frequency

| Market | Trades/year | Trades/month | % events traded |
|---|---|---|---|
| XAUUSD | ≈ 304 | ≈ 25 | 99.4% |
| XAGUSD | ≈ 302 | ≈ 25 | 99.3% |
| USATECHIDXUSD | ≈ 340 | ≈ 28 | 98.8% |
| BTCUSD | ≈ 389 | ≈ 32 | 99.0% |

Frequency is **not** the constraint — 25–32 trades/month per market is ample. Same-day upper+lower pairs are both traded independently (per-event economics; overlap of concurrent windows is minor: 4–7% of events have another event inside their window).

## 10. Economic Metrics (per trade, bp; verified single baseline run)

| Metric | XAUUSD | XAGUSD | USATECHIDXUSD | BTCUSD |
|---|---|---|---|---|
| n trades | 1517 | 1507 | 972 | 1941 |
| **Gross median** | **−5.34** | **−11.63** | **−5.04** | **−11.82** |
| Gross mean | −0.45 | −0.35 | −0.94 | +1.91 |
| Win rate (gross) | 21.9% | 23.0% | 19.2% | 26.5% |
| Avg win / avg loss | +18.0 / −5.9 | +34.9 / −12.5 | +15.9 / −6.1 | +44.4 / −17.8 |
| Profit factor (gross) | 0.93 | 0.97 | 0.86 | 1.11 |
| Stop-out rate | 76.5% | 75.5% | 79.5% | 70.3% |
| Median holding (min) | 20 | 20 | 18 | 31 |
| RT(A) median | 1.73 | 12.30 | 1.05 | 16.77 |
| RT(A) P90 | 2.09 | 14.30 | 1.91 | 34.87 |
| **Net median, A + 0** | **−7.16** | **−23.43** | **−6.14** | **−27.48** |
| **Net median, A + 2c + 2s** | **−11.16** | **−27.43** | **−10.14** | **−31.48** |
| Net median, A + 5c + 5s | −17.16 | −33.43 | −16.14 | −37.48 |
| Net median, B + 2c + 2s | −12.94 | −39.22 | −11.47 | −45.28 |
| Cumulative net (A+4), bp | −9,442 | −24,015 | −5,929 | −39,553 |
| Max drawdown (A+4), bp | 9,533 | 24,146 | 6,016 | 39,692 |

Outcome distribution (XAUUSD example): p05 −19, p25 −9, p50 −5.3, p75 −2.2, p95 +41.6 bp — most trades lose the stop distance; a right tail of large wins is insufficient.

### Excursion-to-cost

| Market | Median residual excursion from entry (bp) | RT(A) median (bp) | RT(A) as % of residual |
|---|---|---|---|
| XAUUSD | 17.8 | 1.73 | ≈ 10% |
| XAGUSD | 36.9 | 12.30 | ≈ 33% |
| USATECHIDXUSD | 19.5 | 1.05 | ≈ 5% |
| BTCUSD | 42.7 | 16.77 | ≈ 39% |

The excursion-to-cost margin is *superficially* large, but it is **economically moot**: the registered exit/stop mechanics do not capture the residual excursion — the median realized gross is negative in every market. Costs are not the binding constraint.

## 11. Market-by-Market Economics

- **XAUUSD — NON-VIABLE (baseline).** Cheapest to trade (RT 1.7 bp) and the discovery market, yet gross median −5.3 bp; 76.5% stop-outs; negative in every year (−9.6 to −17.8 bp net A+4) and both halves.
- **XAGUSD — NON-VIABLE (baseline).** Observed costs (12.3 bp RT) are the heaviest of the metals pair, but the gross translation is negative (−11.6 bp) even before them; negative in every year.
- **USATECHIDXUSD — NON-VIABLE (baseline).** Cheapest costs (1.05 bp RT), tightest gross (−5.0 bp); 79.5% stop-outs; negative in every year and both halves.
- **BTCUSD — NON-VIABLE (baseline).** The only positive gross *mean* (+1.9 bp, right-skewed tail) but median −11.8 bp and the largest costs (16.8 bp RT; P90 34.9 bp); negative in every year (−20.8 to −53.2 bp net A+4) and both halves.
- **EURUSD — not evaluated** (data-quality gate unresolved).

## 12. Chronological Validation

Per-year median net (Model A + 2c + 2s), bp: **uniformly negative in every market and every year**:

- XAUUSD: 2021 −11.5 · 2022 −11.8 · 2023 −9.6 · 2024 −10.3 · 2025 −12.3 · 2026 −17.8
- XAGUSD: 2021 −26.5 · 2022 −31.3 · 2023 −27.9 · 2024 −27.1 · 2025 −22.9 · 2026 −33.0
- USATECHIDXUSD: 2023 −10.3 · 2024 −9.9 · 2025 −10.0 · 2026 −11.2
- BTCUSD: 2021 −41.3 · 2022 −53.2 · 2023 −38.0 · 2024 −27.5 · 2025 −20.8 · 2026 −26.7

Development / out-of-sample halves (registered split: first 50% of event days vs last 50%): median net (A+4) **negative in both halves for every market** (XAUUSD −11.3 / −10.9; XAGUSD −29.1 / −25.1; USATECHIDXUSD −10.0 / −10.3; BTCUSD −43.8 / −24.7). No single anomalous period drives the result; the economics are uniformly adverse. No parameter was fitted on the development half (there are no fitted parameters).

## 13. Cross-Market Robustness

The result is **mechanically uniform across three distinct market mechanisms** — precious metals, equity-index CFD, crypto — and across ~3–5 years each, with identical event definitions and identical registered translation rules. There is no market in which the minimal translation is gross-positive, no year that is positive, and no half that is positive. This is a robustly negative economic result for this translation, not a data artifact: the simulation mechanics were manually validated trade-by-trade (entry at confirmation close; stop at the frozen sweep extreme; stop-first fill; exit at the 120-min close), and the observed spread model is exact-minute in ≥98% of lookups.

## 14. Economic Classification

**Registered gates (pre-registered before computation):** PROMISING requires median net (A+2c+2s) > 0, median gross ≥ 1.5 × median RT(A), ≥ 30 trades/yr, and net positive in both halves; NON-VIABLE if median net (A+0) ≤ 0, or P90 RT(A) ≥ median gross, or < 30 trades/yr.

| Market | Net A+0 > 0 | Margin ≥ 1.5 | Freq ≥ 30/yr | P90 RT < gross | Classification |
|---|---|---|---|---|---|
| XAUUSD | NO (−7.2) | NO (gross < 0) | YES (304) | NO | **NON-VIABLE** |
| XAGUSD | NO (−23.4) | NO | YES (302) | NO | **NON-VIABLE** |
| USATECHIDXUSD | NO (−6.1) | NO | YES (340) | NO | **NON-VIABLE** |
| BTCUSD | NO (−27.5) | NO | YES (389) | NO | **NON-VIABLE** |

**Overall: ECONOMICALLY NON-VIABLE for the registered minimal executable translation.** The candidate does not become a bot under this translation; no demo/live path is authorized from this baseline.

## 15. Demo / Forward-Test Path

**Not authorized.** The baseline is non-viable before costs; there is nothing to forward-test. A demo stage would be warranted only if a future, separately pre-registered translation demonstrates positive net economics (see §16).

## 16. Production Architecture Requirements

Not evaluated in depth (architecture is deferred until economic viability is demonstrated, per the stage firewall). The architecture sketched in the mission — signal engine (sweep → rejection → confirmation), execution engine (order/fill/spread protection), risk engine (fixed-risk sizing, daily/drawdown protection), monitoring — remains the reference design if and only if a future translation clears the economic gates.

**Identified future alternatives (registered as untested options, explicitly NOT optimized or evaluated here):**
1. **Entry at the next bar's open** after confirmation (removes the same-close fill assumption).
2. **Limit entry at/near the swept Asian level** (captures the validated excursion *from the level* rather than the post-move confirmation close — the single most structurally promising alternative, because the behavioral MFE is anchored at the level, and the confirmation-close entry consumes the early move).
3. **Exit at the Asian opposite boundary** (structural target based on the Asian range, not on the 120-min close).
4. **Structural trailing exit** (e.g., trail from the extreme) to capture the MFE-type excursion instead of the window close.
5. **Per-market admission discipline** (e.g., exclude XAGUSD/BTCUSD until their wide-spread regimes narrow, if costs ever become the binding margin).

Any of these requires a **new, outcome-blind, pre-registered economic protocol** with its own cost model and classification gates. Testing them by selecting whichever looks best here would constitute exactly the exit/entry mining this stage prohibits.

## 17. Exact Next Legitimate Task

> A **governance decision** on the disposition of the liquidity-sweep/reversal line: register this economic outcome (behavioral effect validated; minimal executable translation economically non-viable in all four markets), and decide whether to (a) close the line with the negative economic result recorded, or (b) authorize ONE of the §16 alternatives as a separately pre-registered economic protocol — with the explicit rule that no alternative may be selected because of this stage's numbers (that would violate outcome-blindness), and no demo/live work is authorized by any of this.

The discovery value is preserved regardless: a statistically supported behavioral phenomenon whose minimal executable translation does not survive the economics of trading it is a legitimate, complete scientific result.

## 18. Prohibited Follow-Up

- Any exit/entry/parameter search on this stage's data.
- Any re-selection of markets, horizons, or definitions based on this stage's PnL.
- Any EURUSD inclusion until its data-quality operationalization is resolved.
- Any demo/forward/live deployment from this baseline.
- Any ML/K-means/HMM rescue, confluence indicators, or strategy variants.
- Any reopening of closed lines (Mean Reversion DISC-021, TSMOM DISC-022, H01/H01 Equity DISC-023, Session-Anchored Range Expansion DISC-024) or merging results with them.
- Reinterpreting this stage as a behavioral falsification (it is not — the behavioral adjudication stands).

## 19. Integrity

Strictly read-only with respect to scientific objects: the behavioral protocol, event CSVs, adjudication, governance records, and BOE/Assembly/Deployment are untouched. The only new repository artifact is this report. Analysis was performed in `scratch/lsweep_econ_v1/` (scripts + intermediate JSON, outside the repository's research layer). The baseline rules were registered before computation; the simulation was manually validated trade-by-trade; cost data are observed MT5 quotes (exact-minute ≥ 98.3%); all classifications follow the pre-registered gates; results are reported per market, per year, per half, and per cost model without selection.
