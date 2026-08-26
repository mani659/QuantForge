# QuantForge — XAGUSD Real Transaction Cost & Economic Viability Study V1 — Final Report

**Protocol:** V1.0.0 (pre-registered, `COST_VIABILITY_PROTOCOL_V1.md`) · **Date:** 2026-08-12 · **Area:** `output/xagusd_cost_viability_v1/`
**Design posture:** cost-only feasibility analysis of the frozen V3 XAGUSD lead. The signal is untouched; the question is whether observed XAGUSD execution costs leave enough of the gross effect to continue the promotion process.

---

## 1. Executive Verdict

**NON-VIABLE.**

The decisive fact that was missing from V3 is now observed directly: the repository contains a full XAGUSD **tick-level bid/ask record (146.4M ticks, 2021-07-13 → 2026-07-12)** — the exact research period — so the V3 assumption "no spread/bid-ask data exists in the repository" is **falsified**, and the cost question can be answered from observed quotes rather than assumptions.

The answer is unambiguous: **observed round-trip spread costs consume the gross effect.** For the primary cell (N1 DOWN, VALIDATION):

- Gross effect: **+10.66 bp** over 2 h (matched subset; full population +10.86 bp, identical to V3's F1).
- Observed mean round-trip spread cost (half-spread per side, Model A): **9.89 bp**; median **9.09 bp**; P75 **9.94 bp**; P90 **11.42 bp**; P99 **36.15 bp**.
- Net effect: **+0.77 bp**, cluster-bootstrap 95% CI **[−3.78, +5.40]** — indistinguishable from zero.
- Net success rate: **52.6%**.
- Margin at median cost: **+1.56 bp** — already below the pre-registered 3 bp margin, and **below any realistic allowance for the unobserved components** (commission, slippage): with a minimal 2+2 bp unobserved band, median-case net = **−2.44 bp**; with 5+5 bp, **−8.44 bp**.
- Tail check: **P90 cost (11.42 bp) already exceeds break-even (10.86 bp)** → net at P90 = **−0.76 bp**. Under the conservative Model B (full spread per side, mean 19.78 bp) net = **−9.1 bp**.

Every pre-registered NON-VIABLE trigger fires: net CI includes zero at median cost; tail (P90) cost erodes net to ≤ 0; margin is below any defensible threshold. The most favorable legitimate interpretation (the effect is not concentrated in high-cost minutes, and event-time costs are below the global average because the events cluster in the recent high-price period) still leaves a net that is statistically indistinguishable from zero. **The XAGUSD mean-reversion research line is closed as economically non-viable.**

## 2. V3 Signal Definition Used (frozen, unchanged)

`output/event_study_v3/event_dataset_V3.csv` (SHA-256 `e80bd1d700c9…`), XAGUSD rows only, carried forward verbatim:

- **N1** `(close − SMA₁₂₀)/σ₁₂₀(close)`; primary threshold ±3.0; S=240 same-direction separation; H=120 outcome horizon; direction-adjusted returns with fixed hypothesized signs (DOWN → positive, UP → negative).
- Primary economic reference: **N1 DOWN VALIDATION**, gross +10.86 bp (full population, matches V3 F1 exactly); break-even round-trip cost 10.86 bp.
- No threshold, window, event, or normalization was altered. Nothing was re-optimized.

## 3. Transaction-Cost Sources

| Source | Type | Observed? | Period | Coverage of V3 |
|---|---|---|---|---|
| `data/tick/XAGUSD_mt5_ticks.csv` | MT5-style tick export: `date,time,bid,ask,last,vol` (no header) | **Observed bid/ask** | 2021-07-13 00:00 → 2026-07-12 23:59 | Full |
| `data/m1/XAGUSD_M1.csv` | M1 OHLCV (SHA-256 matches V3 fingerprint `69444be9…`) | for vol-regime context only | 2021-07-13 → 2026-07-12 | Full |
| Commission schedules | — | **UNOBSERVED** | — | n/a |
| Broker execution logs / order records / account statements / spread snapshots | — | **ABSENT** (repository-wide search: 0 matches) | — | n/a |
| Slippage records | — | **UNOBSERVED** | — | n/a |

The MT5 tick file is genuine executable-format bid/ask data over the whole research period: 146,389,821 rows, monotonic timestamps (0 out-of-order chunks), `ask > bid` on 100% of sampled rows, `last == bid` (feed convention), volume column all zeros (unusable). Tick mids track M1 XAGUSD closes (validated at 2025-02, 2026-01, 2026-07 samples). No commission schedule, execution log, or slippage record exists anywhere in the repository.

## 4. Cost Data Quality

- **Sample:** 146.4M ticks; 1.729M minutes with ≥1 tick; ticks/min P50=51, P90=203, max=893.
- **Coverage:** 2021-07-13 → 2026-07-12, 24/5. 1,324 minute-gaps >10 min; max gap 5,406 min (weekend/holiday pattern identical to M1). A feed quirk: hours 21–22 UTC have materially fewer minutes (~23k/48k vs ~75k) — systematic daily feed pause, not event-driven.
- **Duplicate timestamps:** multiple ticks per second are normal for a tick stream (feed standard); no out-of-order chunks.
- **Missing values:** none in bid/ask.
- **Spread structure:** near-fixed absolute spread of 3 cents (0.030), with frequent 4–9-cent values and a long tail of spikes (max observed 1.997 = 386 bp at tick level; 379.7 bp at minute level). Zero spread never occurs.
- **Indicative vs executable:** not distinguishable from the file; treated as observed quotes (the most favorable assumption).

## 5. Cost Distribution

| Level | P50 | P75 | P90 | P95 | P99 | Max |
|---|---|---|---|---|---|---|
| Tick-level spread (bp) | 9.86 | 12.66 | 13.95 | 15.52 | 23.77 | 386.2 |
| Minute-median spread (bp) | 12.15 | 13.18 | 14.42 | 15.66 | 23.40 | 379.7 |
| **Per-event RT cost, Model A (bp)** — N1 DOWN VALIDATION | **9.09** | **9.94** | **11.42** | **13.04** | **36.15** | — |

Because the spread is a near-fixed *absolute* 3 cents, **bp cost falls as price rises**: year-median minute spread bp = 12.7 (2021), 13.9 (2022), 12.8 (2023), 10.4 (2024), 8.7 (2025), 6.8 (2026). Tick-level P50 (9.9 bp) is below minute-level P50 (12.2 bp) because high-price recent years contribute more ticks per minute.

## 6. Session / Regime Cost Analysis

- **Session (UTC):** spread bp is nearly flat across hours (hourly median 12.0–12.6 bp); tails are modestly worse at hours 22–23 (P99 56–59 bp) and hour 0 (P99 46 bp). The V3 event hours do not coincide with systematically higher costs.
- **Chronological:** costs fall over time with the price rise (see §5). V3's effect strengthens over time (chrono thirds) — i.e., the effect's recent-period concentration coincides with the *lowest* cost regime, the most favorable combination, which still fails.
- **Pre-event volatility regime (XAGUSD events):** entry spread P50 ≈ 12.3–12.4 bp in low/mid vol terciles, 11.1 bp in high vol (mean 12.5 bp — tail-driven). The effect does not occur disproportionately in high-cost conditions.
- **Direct test (§12's critical question):** splitting the primary cell at median cost, **high-cost events have HIGHER gross** (+12.19 bp, mean cost 11.58 bp → net +0.61 bp) than low-cost events (+9.12 bp, mean cost 8.20 bp → net +0.92 bp); corr(return, cost) = +0.149. The effect is not a product of cheap execution windows — and even in the cheapest windows it nets < 1 bp.

## 7. Round-Trip Cost Construction

- Entry cost = per-minute median spread (bp) at minute of event `t`; exit cost = same at `t+120`; fallback nearest minute ±5 (pre-registered).
- **Model A (primary, standard):** `RT_A = (entry + exit)/2` — mid-referenced returns, taker crosses half-spread each side.
- **Model B (robustness, conservative):** `RT_B = entry + exit` — full quoted spread each side.
- **Commission:** UNOBSERVED — assumption band {0, 2, 5, 10} bp round trip.
- **Slippage:** UNOBSERVED — assumption band {0, 2, 5} bp round trip.
- Matching completeness: entry matched 15,565/15,565 (100%); exit matched 14,758/15,565 (94.8%; the 5–8% failures are exits falling in weekend/feed gaps — no executable quote exists, excluded and counted, pre-specified).

## 8. Gross vs Net Results (Model A, cluster-bootstrap CIs)

| Cell | n | Gross bp | Mean RT cost bp | Net bp | Net CI 95% | Success |
|---|---|---|---|---|---|---|
| **N1 DOWN VALIDATION (primary)** | 430 | **+10.66** | 9.89 | **+0.77** | **[−3.78, +5.40]** | 52.6% |
| N1 DOWN TEST | 443 | +9.49 | 12.05 | −2.56 | [−16.62, +10.84] | 50.8% |
| N1 DOWN TRAIN | 1810 | +3.92 | 12.80 | −8.89 | [−11.75, −6.03] | 42.4% |
| N2 DOWN VALIDATION | 707 | +4.26 | 9.61 | −5.35 | [−8.69, −2.05] | 48.5% |
| N2 DOWN TEST | 704 | −0.72 | 10.34 | −11.06 | [−20.99, −0.85] | 46.3% |
| N1/N2 UP (all) | — | ≤ 0 gross | ~9.4–12.7 | ≤ −10 | negative CIs | 37–44% |

Full-population gross (unmatched included): N1 DOWN VAL 10.86 bp, TEST 10.08 bp — identical to V3. Net results are computed on the matched subsets (94.3% / 91.5% of the frozen populations). **The only positive net estimate anywhere is the primary cell at +0.77 bp with CI spanning zero; every other cell is negative or null.**

## 9. Break-Even Cost

- **Primary cell break-even round-trip cost = 10.86 bp** (gross effect, frozen from V3).
- Observed median RT cost (Model A): **9.09 bp** → margin **+1.56 bp**.
- Observed mean RT cost (Model A): **9.89 bp** → margin **+0.77 bp**.
- Model B (full spread per side): median ≈ 18 bp → break-even exceeded by ~7 bp.

## 10. Cost Sensitivity

| Statistic | RT cost (Model A) | Net at that cost |
|---|---|---|
| P50 | 9.09 bp | +1.56 bp |
| P75 | 9.94 bp | +0.71 bp |
| **P90** | **11.42 bp** | **−0.76 bp** |
| P95 | 13.04 bp | −2.39 bp |
| P99 | 36.15 bp | −25.49 bp |

TEST shows the same shape with worse tails (P90 22.4 bp → net −12.9 bp; P99 102.4 bp → net −92.9 bp). **Median is below break-even but the entire upper half of the observed cost distribution is not; P90 alone destroys the effect.** Claiming viability from the median would ignore that tail behavior — exactly what the protocol precludes.

## 11. Slippage / Unobserved Cost Assessment

- **Slippage: unobserved.** Zero is assumed only as the best case; bounded sensitivity: {2, 5} bp.
- **Commission: unobserved.** No schedule exists in the repository; MT5 retail silver ECN/raw-spread structures typically charge commissions, and this feed's 3-cent spread is already a marked-up retail spread. Bounded sensitivity: {2, 5, 10} bp.
- At median cost, adding the minimal plausible 2+2 bp unobserved band gives net **−2.44 bp**; 5+5 bp gives **−8.44 bp**. There is **no margin for unobserved costs** — the observed spread alone nearly consumes the edge.

## 12. Economic Viability

**NON-VIABLE** — determined by the pre-registered decision rule, not by post-hoc judgment:

| VIABLE condition (all required) | Result |
|---|---|
| Median AND P75 RT cost < break-even (10.86 bp) | 9.09, 9.94 < 10.86 — pass |
| Net mean > 0 with bootstrap CI excluding 0 at median cost | +0.77, CI [−3.78, +5.40] — **FAIL** |
| Margin ≥ 3 bp at median after mid unobserved band (median + 4 bp) | 1.56 bp; 9.09+4 = 13.09 > 10.86 — **FAIL** |
| P90 cost < break-even OR net at P90 > 0 | 11.42 > 10.86; net −0.76 — **FAIL** |

NON-VIABLE triggers confirmed: (1) net CI includes zero at median cost; (2) P90 tail cost erodes net to ≤ 0; (3) margin below any defensible allowance, with zero unobserved-cost headroom. Model B and the unobserved bands only strengthen the verdict.

## 13. Scientific Limitations

1. **Quotes vs fills:** bid/ask are feed quotes; indicative vs executable indistinguishable; treated as executable (favorable assumption). Actual fills could be worse.
2. **No fresh holdout:** TEST was reused with the V3 caveat; this is an economic feasibility analysis, not new OOS validation.
3. **Matched subset:** 5–8% of events (weekend/feed-gap exits) excluded from net; gross differs from V3 by ≤ 0.6 bp on the subsets.
4. **M1 close price basis** (bid vs mid) is ambiguous; the half-spread-per-side model is the standard mid-referenced assumption, and Model B brackets the alternative.
5. **Single feed:** the repository's only cost evidence is this one MT5 feed; other brokers' schedules may differ, but the effect's margin (−1.6 bp at median, negative at P90) is far too thin for broker variation to rescue.
6. **Unobserved components** (commission, slippage) are assumption bands; the verdict does not depend on them (spread alone fails).
7. **Intraday path costs** beyond entry/exit spreads (e.g., quoting through the 2-h hold) are not modeled; holding-period risk is already reflected in the return CI.

## 14. Final Research-Line Decision

**Close the Mean-Reversion implementation path as economically non-viable.**

Per the pre-registered decision branch (NON-VIABLE): stop the Mean-Reversion research line; do not run a V4 event study; do not implement a detector; no Scientific Specification Readiness Review is warranted. The V3 lead — statistically real as a directional asymmetry but economically insufficient — is now shown, with **observed** execution-cost evidence, to be **non-viable even before the unobserved cost components**. The V3 holdout claim (break-even ≈ 10 bp) is superseded: observed median round-trip cost at event times is 9.1 bp and the distribution's upper half exceeds break-even.

The formal negative/conditional finding should be recorded in `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-style entry) as a **governance/research-layer action outside this task's write scope** (this task's firewall restricts writes to `output/xagusd_cost_viability_v1/`).

## 15. Exact Next Step

1. **Record the negative finding** in the research discovery database (DISC-style entry: XAGUSD directional asymmetry confirmed statistically in V1–V3 but economically non-viable under observed tick-level spread costs; break-even 10.9 bp vs observed median RT 9.1 bp / P90 11.4 bp; no margin for commission/slippage).
2. **Reclassify** the project's detector blocker note (research-gap #1 "live/broker costs") as *partially resolved by observed historical spread data — with a negative outcome for this hypothesis*.
3. **Decide the next research hypothesis** — the Mean-Reversion line is closed; the architecture remains DESIGN BLOCKED for any detector until a different, cost-surviving scientific specification exists.

---

*Research artifact. V1/V2/V3 outputs untouched. Reproducibility: protocol V1.0.0; tick SHA-256 `edccad88…`, M1 SHA-256 `69444be9…` (= V3 fingerprint), events SHA-256 `e80bd1d7…` (= V3 fingerprint); pandas 3.0.2 / numpy 2.4.4; seed 20260814; matching rule and model formulas in protocol §4–§5; all CSVs + `event_cost_matched.csv` + `xagusd_minute_aggregates.csv` cached in this area.*
