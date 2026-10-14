# TASK120 — CAND-025 Re-Measurement Results (single bounded run)

**Status:** MEASUREMENT COMPLETED. No auto-promotion in any outcome (none
granted here). Raw outputs: `events.csv` (158 rows, `6171e9a3…`),
`summary.json` (`92f071f7…`), `phase1_count.json` (`69c9575c…`).

## Sample

158 rule-satisfying events, 2023-09-01 → 2026-07-02, zero skips
(no_atr/incomplete/zero_dir all 0). Full verified panel; no date invention.

## Outcomes vs adopted bars

- **T1 sign stability: PASS (structural).** Halves means +0.023 / +2.281 —
  both positive. (First-half margin thin, stated plainly.)
- **T2 stressed nets:** mean net2 (2-pt) +1.152 — consistent with G1's
  +1.25 within noise; mean net3 (3-pt) +0.152.
- **T3 bootstrap/Holm: FAIL.** 95% CIs: net2 [−6.565, +8.843], net3
  [−7.615, +7.951] — lower bounds below zero (SD-dominated, as G1 warned);
  Holm-adjusted p = 0.7772 both (α=0.05). Neither condition met.
- **T4 falsification flag: RAISED.** 84/158 events (53.2%) continued
  post-entry — strict majority continuation, the V9 preregistered
  falsification direction.
- **Go/no-go (ALL of T1 + T3@2.0 + T3@3.0): NO-GO.** T3 fails; T4 flag
  corroborates fragility.

## Reading (reported, not promoted)

The frozen object behaves as G1 recorded (mean net2 +1.15 ≈ +1.25) with
the warned-about variance (CI spanning ±7–8 points). Sign agreement holds
structurally but the economic edge is statistically indistinguishable from
zero under the adopted inferential procedure, and the mechanism's own
falsification direction is present. Task-65 frontier comparison: N=158 knife-edge cell remains below reliable detection, as anticipated.
