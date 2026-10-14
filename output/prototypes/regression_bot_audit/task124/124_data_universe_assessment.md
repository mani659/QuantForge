# TASK124 — Data Universe Assessment (verified available resources)

**Method:** Existing manifests and data inventory records only. No data
content accessed. No new collection.

## Verified available datasets

| Dataset | Source | Coverage | Verification | Authorization |
|---|---|---|---|---|
| SPY/VEU/AGG/BIL daily TR | Yahoo (yfinance auto_adjust) | SPY 1993→, AGG 2003→, VEU 2007→, BIL 2007→, all to 2026-09-25 | SHA-256 in `lane_b_batch1/data/provenance.json` | Batch-1 evaluation (consumed); reuse requires new authorization |
| TB3MS monthly | FRED | 1934→2026-08 | Recorded in Batch-1 provenance | Same as above |
| M1 FX (7 symbols) | MT5-derived | 2021-01→2026-10 | `data/m1/` inventory | Research use; no evaluation authorization |
| USATECHIDXUSD M1 | MT5-derived | 2023-09-01→2026-07-10 | SHA `39f25619…` triple-record | CAND-025-RM-01 (consumed) |
| Tick (4 symbols) | MT5 | Various | `data/tick/` inventory | Research use; no evaluation authorization |
| FRED indices (4) | FRED | Various | Recorded in task51 §11 | Research use |

## Is the 4-ETF universe an unavoidable constraint?

**Yes, for cross-sectional equity momentum.** The verified datasets contain
no broad equity cross-section (no CRSP-like panel, no multi-stock universe).
The only multi-asset equity panel is the 4-ETF set (SPY/VEU/AGG/BIL), which
was constructed for the Batch-1 allocation prototypes.

**Could a broader cross-sectional universe be constructed from available
data?** No. The M1 FX data covers 7 currency pairs — a cross-sectional FX
study is possible but (a) FX momentum is a different economic mechanism
with different cost structure, (b) the M1 data starts 2021-01 (only ~5
years), and (c) cross-sectional FX momentum has not been tested but the
universe is even thinner (7 assets) and shorter.

**Could the 4-ETF universe be combined with other instruments?** No
defensible economic rationale exists for combining ETFs with FX pairs or
FRED indices in a single cross-sectional ranking — different asset classes
have different return constructions, cost structures, and economic
mechanisms. Combining them would be an invented universe, not a verified
one.

## Power assessment (conceptual only — no calculations performed)

**The binding constraint is not sample size but cross-sectional thickness.**

The Task-63 calibration report (read this session) established:
- The detectable region requires **Sharpe ≳1.5 sustained over ~8 years**
- At 3Y samples, **nothing survives at any tested level**
- The topology gate is the binding constraint (interior rate ≤10% even at
  Sharpe ≥1)
- **FPR ≈ 0 is purchased with power ≈ 0 across the plausible effect range**
- Verdict: **NOT SUITABLE as configured for the next real search phase**

**Application to the 4-asset XSM proposal:**
- ~216 monthly observations (2008-05→2026-09) — exceeds the 3Y minimum
- But the cross-sectional spread in a 4-asset universe is a 2-vs-2
  comparison — the effective number of independent cross-sectional
  observations is extremely small
- Cross-sectional momentum is typically estimated on hundreds of stocks;
  the 4-asset panel is orders of magnitude thinner
- The Task-63 verdict implies that even if a true cross-sectional momentum
  effect exists in 4 ETFs, the pipeline's detection gates would likely
  refuse it (topology gate binds first; interior rate ≤10%)

**Conclusion:** The power/informativeness question **cannot be established
from existing evidence.** The Task-63 calibration suggests the 4-asset XSM
is likely too thin to produce a detectable signal, but this is a conceptual
inference from the calibration report, not a verified power calculation.
No power study exists for this specific design, and none can be run under
this task's restrictions.

**Missing fact that prevents resolution:** The minimum detectable effect
(MDE) for a 4-asset cross-sectional momentum strategy at the frozen cost
assumptions, given the serial dependence and tiny cross-section. This
cannot be determined from existing records.
