# TASK151 — Regime Stability Measurement Report (single bounded run)

## Preregistered verdict: INCONCLUSIVE

k=2 met the numeric CONTINUE bars (ARI val 0.745 / test 0.853,
prevalence 53.5/46.5%, dwell 7.3d) but the NULL reference agreed at ARI
0.852 (≥ 0.2 threshold) → predeclared null override applies. k=3:
INCONCLUSIVE on its own bars (test ARI 0.402). Tertile baseline:
balanced prevalence (37.6/29.5/32.9%), dwell 3.8d.

## What the null result means (reported, not promoted)

Time-permuted training data reproduces validation's own partition at
ARI 0.85: the pooled clusters reflect the MARGINAL distribution's shape
(calm vs stressed days pool-wide), not temporal regime dynamics. The
preregistration's own safeguard caught exactly the vacuous-regime case
it was designed for. No trading, sizing, candidate, or profitability
claim follows — in ANY direction. The question "do stable temporal vol
regimes exist here" is answered: not demonstrated.

## Sample and integrity

Matrix 20,116 daily rows (train 10374 / val 3550 / test 6192);
drops: 209 warmup/zero-var days (counted, no fill). Test window
2025-01-01→2026-10-01. 11 files present with row counts matching the
prereg table; per-file SHA established and recorded in metrics.json;
timestamps parsed epoch-seconds → UTC; ordering/duplicates verified
(no duplicates); sklearn 1.9.1 KMeans per frozen config (kmeans++,
n_init=1 × seeds 0–9, lowest-inertia-first-wins). Budget: 2 k-configs +
tertile + null = 5 fits, single run, no reseed/refit/rescue.

## Deviations and limitations (all disclosed)

1. **Prereg documentation defect (no computational effect):** prereg §2
   labels timestamps "epoch-ns ints"; actual values are epoch SECONDS.
   Executor parsed as seconds → correct calendar segmentation (verified
   by test window landing 2025-01→2026-10). A nanosecond reading would
   have collapsed all data to 1970 and failed loudly, not silently.
2. **Engine timestamp-unit fix** (one-line, pre-measurement): same cause
   as above; found because row counts came back degenerate, fixed,
   self-test re-greened, then the single run.
3. k=3 third cluster does not persist into test (ARI 0.402) — recorded,
   not tuned.
4. metrics.json embeds test label arrays (redundant with
   assignments.csv) — harmless duplication, left as written (no rerun
   for cosmetics).
5. Realized-volatility levels, costs, returns, and trade outcomes were
   never computed — stability only, per the frozen scope.
