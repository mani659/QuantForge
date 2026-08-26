# QuantForge — XAGUSD Real Transaction Cost & Economic Viability Study — Protocol V1 (Pre-Registered)

**Status:** PRE-REGISTERED (all cost models, matching rules, and decision criteria defined before any confirmatory gross-to-net computation)
**Date:** 2026-08-12
**Version:** V1.0.0
**Area:** `output/xagusd_cost_viability_v1/` (research artifact; not production code)
**Purpose:** determine whether the V3 XAGUSD directional mean-reversion lead survives **observed** XAGUSD transaction costs, using the tick-level bid/ask data present in the repository.

---

## 1. Frozen reference signal (V3, unchanged)

The V3 XAGUSD event definition is used **verbatim** (from `output/event_study_v3/event_dataset_V3.csv`; protocol V3.0.0):

- **N1** rolling price z-score `(close − SMA₁₂₀)/σ₁₂₀(close)`; primary threshold ±3.0; S=240 separation; H=120 outcome horizon.
- Direction-adjusted return `dir_adj_return_h120` (DOWN `+ret`, UP `−ret`), measured over bars `t+1..t+120`.
- **Primary economic reference cell (frozen from V3):** XAGUSD **N1 DOWN VALIDATION**, gross mean **+10.86 bp** over 2 h → **break-even round-trip cost = 10.86 bp** (V3 cost_sensitivity.csv; N1 DOWN TEST gross +10.07 bp).
- Secondary cells reported but not decision-bearing: N1 UP, N2 DOWN, N2 UP (V3 found UP null and N2 weaker; N2 DOWN gross VAL 4.41 bp, TEST 1.53 bp).

No signal, threshold, window, or event is altered. The research question is **cost only**.

## 2. Cost data (observed)

- **Source:** `data/tick/XAGUSD_mt5_ticks.csv` — MT5-style tick export, columns `date(YYYYMMDD), time(HH:MM:SS), bid, ask, last, volume`, no header. Volume column is all zeros (unusable); `last == bid` in this feed; `ask > bid` on every row checked.
- **Coverage (archaeology, pre-protocol):** 2021-07-13 00:00 → 2026-07-12 23:59; ~146M rows; tick mids track M1 XAGUSD closes (validated at 2025-02, 2026-01, 2026-07 samples). Covers the full V3 event population.
- **Interpretation:** executable bid/ask quotes (indicative vs executable cannot be distinguished from the file alone; treated as observed quotes — see limitation §8).
- SHA-256 fingerprint recorded in metadata.

## 3. Unit conversion

- `mid = (bid + ask)/2`
- `spread_bp = (ask − bid)/mid × 10⁴`
- All costs expressed in **basis points of XAGUSD price** to match the V3 return basis (bp over 2 h). No pip/point/percent mixing.

## 4. Cost matching rule (event → observed cost)

- Per-minute spread = **median** of tick-level spreads in that UTC minute (only minutes containing ≥1 tick).
- **Entry cost:** spread in the minute containing event timestamp `t`. If the minute is empty, nearest minute with ticks within ±5 min.
- **Exit cost:** spread in the minute containing `t + 120 min`. Same fallback.
- If no ticks within ±5 min of either point → event cost marked **UNOBSERVED** and counted (expected only in market-closure gaps).
- Entry and exit costs are matched per-event; no future information is used (both points ≤ t+120).

## 5. Round-trip cost models (all pre-registered; both reported)

| Model | Formula | Basis | Use |
|---|---|---|---|
| A — standard (half-spread per side) | `RT_A = (entry_spread_bp + exit_spread_bp)/2` | mid-referenced returns; taker crosses half-spread each side | PRIMARY |
| B — conservative (full spread per side) | `RT_B = entry_spread_bp + exit_spread_bp` | taker pays full quoted spread each side | ROBUSTNESS |

- **Commission:** UNOBSERVED. Sensitivity band `{0, 2, 5, 10} bp` round trip, labelled assumption (retail MT5 silver ECN commission is broker-specific; no commission schedule exists in the repository).
- **Slippage:** UNOBSERVED. Sensitivity band `{0, 2, 5} bp` round trip, labelled assumption (no execution logs exist).
- Total cost = spread model + commission band + slippage band (additive, worst-case aligned).

## 6. Statistical analysis

- Cost distribution percentiles **P50 / P75 / P90 / P95 / P99 / max** for: tick-level spread (bp), per-minute median spread (bp), and per-event round-trip cost (bp, both models).
- **Net effect** per event: `net_i = dir_adj_return_h120_i − RT_cost_i`.
- Cluster bootstrap for net mean CI (B=2000, seed 20260814): clusters = connected components of the overlap graph `|t_i − t_j| < 120` over **all XAGUSD events** in the analysis window (identical rule to V3), statistics pooled over direction-selected events within resampled clusters. Null-centered p for net ≠ 0.
- Net success rate = share of events with `net_i > 0`.
- **Break-even:** gross mean of the cell (frozen). **Margin** = break-even − observed median round-trip cost.

## 7. Session / regime cost analysis

- Spread bp by **UTC hour** (24 bins) over the full tick record — determines whether the effect's event hours coincide with high-cost hours.
- Spread bp by **calendar year** and by **chronological third** (matching V3 partition thirds) — determines cost drift over the research period (relevant because V3's effect strengthens over time while price levels rose).
- Spread bp by **pre-event volatility tercile** (realized vol = std of 1-min close-to-close returns over the 120 bars before `t`, computed from M1; event-time terciles within XAGUSD events) — determines whether the effect occurs disproportionately in high-cost conditions.

## 8. Decision rule (pre-registered; no post-hoc margin selection)

Verdict computed on the **primary cell (N1 DOWN, VALIDATION, Model A at observed median round-trip cost)**:

- **VIABLE** iff ALL of:
  1. observed median AND P75 RT_A cost < break-even (10.86 bp);
  2. net mean > 0 with bootstrap CI excluding 0 at median observed cost;
  3. margin (break-even − median cost) ≥ 3 bp after the **zero unobserved-cost** assumption is relaxed to the {2 bp commission, 2 bp slippage} mid-band (i.e., still positive at median + 4 bp unobserved);
  4. tail check: P90 RT_A cost < break-even OR net at P90 cost still > 0.
- **NON-VIABLE** iff any of: median or P75 RT_A ≥ break-even; net mean ≤ 0 at median cost; net CI includes 0 at median cost; or tail cost (P90) erodes net to ≤ 0 while P90 is within the observed distribution.
- **UNRESOLVED** iff cost data cannot be matched to a material share of the primary event population (>5% UNOBSERVED), or the observed spread data is inconsistent with the M1 basis.

If the verdict is NON-VIABLE under Model A, Model B and the unobserved bands are reported but do not change the verdict (they only strengthen it).

## 9. Holdout / OOS caveat

This is an **economic feasibility analysis of the existing V3 lead** — NOT a fresh out-of-sample validation. TEST results are secondary. The V3 signal and partitions are fixed and reused; nothing here re-validates the signal.

## 10. What this study may and may not conclude

- MAY conclude: VIABLE (justifying a Scientific Specification Readiness Review), NON-VIABLE (closing the Mean-Reversion research line), or UNRESOLVED.
- MUST NOT conclude: detector readiness, strategy validation, production approval, threshold freezing, or any BOE implementation authorization — even if VIABLE.

## 11. Reproducibility

Recorded in `experiment_metadata_V1.json`: source fingerprints (tick file, M1, V3 event dataset), pandas/numpy versions, seed, matching rule, model formulas, cost bands, output artifact SHA-256s. No hidden manual filtering; every exclusion counted and reported.

## 12. Outputs (all under `output/xagusd_cost_viability_v1/`)

`COST_VIABILITY_PROTOCOL_V1.md` (this file), `cost_data_inventory.csv`, `cost_distribution.csv`, `cost_by_session.csv`, `cost_by_regime.csv`, `gross_to_net_analysis.csv`, `cost_sensitivity.csv`, `experiment_metadata_V1.json`, `final_cost_viability_report.md`. V1/V2/V3 artifacts untouched.

---

*Pre-registered 2026-08-12 before any confirmatory gross-to-net computation. Cost models, matching rules, and the decision rule were fixed before inspecting matched event costs.*
