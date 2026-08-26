# QuantForge — Canonical Mean-Reversion Event Study Protocol V1 (Pre-Registered)

**Status:** PRE-REGISTERED (defined before any outcome inspection)
**Date:** 2026-08-12
**Version:** V1.0.0
**Area:** `output/event_study_v1/` (research artifact; not production code)

## 1. Purpose

To determine whether the behavioral phenomenon described by the QuantForge research corpus — extreme short-term displacement, adverse/panic momentum, recoil/recovery, and persistence — can be converted into a **reproducible, population-level, out-of-sample, cross-market, versionable scientific specification** from the raw M1 data present in the repository.

This is a research experiment. It does not define a production detector. Its outcome is evidence (or its absence).

## 2. Governing rules (pre-registered)

1. **No outcome inspection before this protocol is frozen.** Event definitions, measures, windows, horizons, thresholds grid, partitions, and statistical procedures below are fixed in advance.
2. **No look-ahead.** All detection inputs use data up to and including the event bar's close (`close[t]`). All outcomes use bars `t+1 … t+H` only.
3. **No selected-trade bias.** The event dataset contains the **whole eligible population** per the rules below — never only "winning" events.
4. **No threshold mining.** A single primary threshold is pre-registered; the threshold grid is reported as a TRAIN-only stability study. No value is selected by PnL.
5. **No post-hoc redefinition.** If the event definition must change, that is a new protocol version (V2), not an edit of V1.
6. **No leakage between partitions.** TRAIN defines the panic-momentum quantile and hosts the exploratory threshold grid. VALIDATION evaluates the pre-registered primary definition once. TEST is used once, at the end, as a confirmatory hold-out (pre-authorized here).
7. **Negative results are valid results.** "NO ROBUST THRESHOLD ESTABLISHED" is an acceptable conclusion.

## 3. Data

- Sources: `data/m1/{XAUUSD,EURUSD,BTCUSD,XAGUSD,USATECHIDXUSD}_M1.csv`.
- Format: `timestamp,open,high,low,close,volume`; M1 bars; timestamps naive (MT5 server time); no timezone correction applied (ordering only).
- Data-quality manifest produced first: row counts, date ranges, duplicate timestamps, gaps, missing OHLCV, volume coverage, per market.
- Dataset fingerprint: SHA-256 of each source file recorded.
- Usable period per market: bars with sufficient warm-up (`W + m` bars of history) **and** sufficient forward horizon (`H` bars ahead within the same partition). No event is detected in the first `W + m` bars or the last `H` bars of a partition.

## 4. Displacement measure (pre-registered)

- **Primary:** rolling standardized displacement (z-score) of close:
  `z_t = (close_t − SMA(close, W)) / stdev(close, W)`, with `W = 120` bars (≈ 2 h on M1).
  `stdev` = rolling population standard deviation over the same window.
- **Sensitivity windows (reported, not primary):** `W ∈ {60, 240}`.
- Units: standard deviations. Assumptions: rolling normality is NOT assumed; z is only a normalization. Look-ahead: none (window ends at `t`). Warm-up: first `W` bars excluded.
- Note: z-score is adopted because it is the standard volatility-normalized displacement measure and the corpus documents z-scale observations; its use here is a **pre-registered methodology choice**, and no specific threshold is assumed.

## 5. Momentum / panic measure (pre-registered)

- `mom_t = (close_t / close_{t−m}) − 1`, `m = 30` bars (≈ 30 min), in percent.
- Panic-momentum classification (for DOWN events): `mom_t ≤ P25(mom)` where P25 is the 25th percentile of `mom` computed **on TRAIN only**, per market. For UP events: `mom_t ≥ P75(mom)` (mirror). This is a pre-registered fixed quantile, not tuned to outcomes.
- Candidate classes: **D** = displacement-only; **D+P** = displacement + panic momentum.
- Whether momentum adds information beyond displacement is assessed by comparing D vs D+P outcome distributions (not by selection).

## 6. Candidate / event definition (pre-registered)

- DOWN event at bar `t` iff `z_t ≤ −Z_primary`. UP event at bar `t` iff `z_t ≥ +Z_primary`.
- **Primary threshold:** `Z_primary = 3.0` (pre-registered; central value of the corpus-documented −2.8…−3.8 range).
- **Threshold stability grid (TRAIN-only, exploratory):** `Z ∈ {2.0, 2.5, 3.0, 3.5, 4.0}`.
- **Overlap suppression:** minimum separation `S = 240` bars between events of the **same direction** per market (keep the first qualifying bar; suppress subsequent same-direction bars until `S` bars elapsed). Cross-direction overlap is allowed and its frequency is reported as a dependence caveat.
- **Direction:** DOWN and UP populations are analyzed **separately** and pooled direction-adjusted. Direction is research metadata; it does not modify any frozen contract.

## 7. Outcome measures (pre-registered)

Primary horizon `H = 120` bars; sensitivity `H ∈ {60, 240}`. All outcomes use bars `t+1…t+H`.

For DOWN events (long-reversion hypothesis):
- `event_return_H = close[t+H] / close[t] − 1`
- `adverse_excursion = (close[t] − min(low[t+1..t+H])) / close[t]`  (≥ 0)
- `favorable_excursion = (max(high[t+1..t+H]) − close[t]) / close[t]`  (≥ 0)
- `recovery_ratio = favorable_excursion / (favorable_excursion + adverse_excursion)`  (0…1; recovery proportion of total excursion)
- `recovery_time =` index of the first bar `i ∈ [1..H]` with `close[t+i] > close[t]`; `H+1` if never
- `retention = mean( close[t+i] > close[t] for i ∈ 1..H )`  (fraction of horizon above event close)
- **MAE** = `adverse_excursion`; **MFE** = `favorable_excursion` (definitions recorded; this experiment's MAE/MFE are close-referenced, high/low-based — resolving, for this experiment, the definitional mismatch flagged in RESEARCH_GAPS #5)

For UP events: mirror definitions; `direction_adjusted_return = −(close[t+H]/close[t] − 1)`.

## 8. Partitions (pre-registered, per market, chronological)

- TRAIN = [start, 70%) — panic-quantile definition + exploratory threshold grid.
- VALIDATION = [70%, 85%) — single confirmatory evaluation of the pre-registered primary definition (Z=3.0).
- TEST = [85%, end) — single confirmatory hold-out pass (pre-authorized; used exactly once).
- Events within `H` bars of a partition boundary are excluded from that partition's outcome statistics (retained in the dataset, flagged).

## 9. Statistical procedures (pre-registered)

- Statistics per (market, direction, partition, Z, H): event count, mean/median of each outcome, dispersion, **bootstrap 95% CI** (B = 2000 resamples, seeded, `seed=20260812`).
- **Chance comparison:** mean `event_return_H` vs (a) the unconditional mean of H-bar forward returns over the same partition, and (b) a random non-event sample of equal size (seeded). "Distinguishable from chance" requires the bootstrap CI of the event-mean to exclude zero **and** the difference-vs-baseline CI to exclude 0.
- Threshold stability: per Z in the grid (TRAIN), event count, mean return, CI — reported as a region, not a pick.
- Cross-market: same statistics per market; portability assessed by sign and CI overlap of the primary measure, not by any single number.
- Regime/time-of-day: exploratory TRAIN-only dimension (volatility terciles by rolling std; hour-of-day buckets), reported with explicit small-sample caveats.
- Limitations to state: event clustering/overlap dependence, no transaction costs, heavy tails, multiple comparisons across the TRAIN grid (grid is exploratory only), and cross-market multiplicity.

## 10. Reproducibility

Recorded with the outputs: source dataset SHA-256 fingerprints, pandas/numpy versions, protocol version V1.0.0, script version, seeds, partitions, event dataset identity (SHA-256 of the CSV), and this document.

## 11. Promotion gate (post-analysis)

**GATE 1 — SPECIFICATION READY** requires, at minimum: reproducible event definition; reproducible recoil and persistence measures; directionality; event boundaries; MAE/MFE definitions; a stable threshold **region** (not a single fitted number); out-of-sample (VALIDATION) and cross-market evidence; and normalization treatment. Anything less is **GATE 1 PARTIALLY READY** or **GATE 1 FAILED** — engineering must not proceed either way without a later, separate specification-readiness review.

*Pre-registered 2026-08-12 before any outcome analysis. No threshold, window, or definition in this document was chosen after inspecting outcomes.*
