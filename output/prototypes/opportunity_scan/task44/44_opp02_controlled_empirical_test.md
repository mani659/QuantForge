# OPP-02 Controlled Empirical Test — Narrative Artifact

**Task:** 44 — Controlled empirical test of OPP-02 (cross-sectional relative-strength rank basket)
**Universe:** 11-symbol MT5 H4 cache (`_t37_h4_*.npz`); common-11 span 2021-01-03 → 2026-09-30 (8,902 rows)
**Frozen spec:** weekly rebalance · trailing-return rank · long top / short bottom tercile · equal weight · positions replaced · 5-session hold · next-bar-open fill · cost 10/5/0 bps per side + swap proxy · primary control = same basket without rank filter
**Run:** `run01_measure.py` (frozen-protocol implementation, vectorized NumPy); `run01_results.json` (raw); `run02_results.json` (canonical)
**Random seed:** 20261004 · **Permutation null:** 300 trials/window, outcome-blind (random top-3/bottom-3 of available symbols per day)

---

## 1. Setup and data audit

- 11 symbols: XAUUSDm, XAGUSDm, USTECm, EURUSDm, GBPUSDm, USDJPYm, EURGBPm, AUDNZDm, BTCUSDm, ETHUSDm, USOILm.
- Full pivot: 12,585 daily rows; 3,683 rows (29%) have fewer than 11 symbols and are excluded from the primary per-day rank analysis; 8,902 common-11 rows retained (2021-01-03 → 2026-09-30).
- Per-day tercile masks are computed over that row's available symbols only; the primary analysis is restricted to the common-11 rows. This is the single most defensible span and is the basis of every figure below.
- No parameter optimization, no post-result rule change.

## 2. Cross-sectional separation (act_mean bps / null 2.5–97.5%)

| Window | act_mean bps | null mean bps | null p25 | null p75 | Verdict |
|---|---:|---:|---:|---:|---|
| 4 | +475.0 | −12.0 | −776.5 | −703.1 | INSIDE null |
| 8 | +970.2 | +7.5 | −1696.7 | −1366.6 | INSIDE null |
| 13 | +1536.3 | +34.3 | −2555.5 | −2203.4 | OUTSIDE null (>10× std) |
| 26 | +2782.8 | −53.5 | −4065.1 | −3904.1 | OUTSIDE null (>10× std) |

- W4/W8 observed means sit inside the outcome-blind null bands: no separation signal there.
- W13/W26 observed means sit far outside the null bands; the separation is not explained by random ranking. The effect is large but highly dispersed (act_std ≈ 23k–33k bps), driven by a small number of extreme days (act p05/p95 ≈ −100k to −130k bps).

## 3. Portfolio treatment (aggregate daily top-minus-bottom, with and without friction)

Aggregate figures are sums over rebal days (unit-notional basket, no per-position compounding); per-rebal-day mean is act_mean_bps above.

| Window | cost10 gross | cost10 net | cost0 gross | Sharpe cost10 | MDD | PF |
|---|---:|---:|---:|---:|---:|---:|
| 4 | +4.2269 | +4.0601 | +4.2269 | 0.579 | −2.31 | 1.11 |
| 8 | +8.6285 | +8.3874 | +8.6285 | 0.840 | −4.50 | 1.15 |
| 13 | +13.6563 | +13.3459 | +13.6563 | 1.053 | −7.26 | 1.19 |
| 26 | +24.7004 | +24.2553 | +24.7004 | 1.348 | −14.90 | 1.25 |

- Friction (10 vs 0 bps) trims gross by ~1.8–1.9% in every window; net remains positive across all tiers, so the 10-bps tier passes, but the margins are thin relative to the dispersion.
- The cost tier changes are immaterial to the verdict: the result is a rank-separation statistic, not a cost-sensitive edge.

## 4. Temporal eras (common-11)

- Every window is negative in 2022 (the energetic, tightening year: W26 net −11.41, Sharpe −3.07).
- Positive in 2023 and 2024; 2025 weaker; 2026 mixed but with W26 +5.65 (Sharpe 2.00) the strongest single slice.
- The aggregate credit concentrates in a single ~13-month regime (2024.9 → 2026.10). The result is not persistent across the full common-11 span.

## 5. Symbol cross-section

Per-rebal-day aggregate contributions (W26; same sign pattern in W4/8/13):

| Symbol | W26 contribution |
|---|---:|
| XAUUSDm | −22.13 (negative) |
| XAGUSDm | +31.03 (dominant long) |
| BTCUSDm | +46.49 (dominant long) |
| USDJPYm | −0.75 (negative) |
| Others | small positive/zero |

- BTCUSDm + XAGUSDm carry the result; XAUUSDm (the largest economical instrument by notional) is negative.
- 2026 single-symbol concentration is extreme: BTCUSDm > 50% of gross in W13/W26. This is a hard concentration FAIL.

## 6. Primary verdict

**C — NO CLEAR MECHANISM (under the frozen test), with a strong proviso.**

- Mechanism present: true. W13/W26 means fall outside the outcome-blind null by >10× null std.
- Mechanism short horizon: W4/W8 are inside the null — not stable across horizons.
- Persistence: FAIL (2022 negative; 2025–26 weak/mixed; result concentrated in one regime).
- Concentration: FAIL (BTCUSDm/XAGUSDm dominant; XAUUSDm negative).
- Friction: PASS marginally (net positive at 10 bps, thin margins).
- Executability: PASS (deterministic weekly rank/order/replace protocol on H4 caches).

The controlled test therefore does **not** validate OPP-02 as a repeatable strategy. It does show that a cross-sectional rank signal can produce a large, statistically unusual long-horizon separation — which is precisely why the 2022 negative, regime concentration, and symbol concentration must be resolved before any empirical decision to act is taken.

## 7. Reproducibility record

- Inputs: `output/prototypes/fx_h4inv_adx_prep/_t37_h4_{sym}.npz` (11 symbols).
- Software: Python 3.11, pandas 3.0.2, NumPy 2.4.4.
- Seed: 20261004 · null trials: 300 · common-11 rows: 8,902.
- Files created:
  - `output/prototypes/opportunity_scan/task44/run01_measure.py`
  - `output/prototypes/opportunity_scan/task44/run01_results.json`
  - `output/prototypes/opportunity_scan/task44/run02_results.json`
  - `output/prototypes/opportunity_scan/task44/44_opp02_controlled_empirical_test.md`

## 8. Open items

- Swap proxy is disclosed but the feeder swap history is not available in this repository (cost tier 10/5/0 bps assumes the proxy; C on swap execution risk until the fixture is supplied).
- The controlled test is frozen: no tuning, no post-hoc rule changes, no cherry-picking of windows.
