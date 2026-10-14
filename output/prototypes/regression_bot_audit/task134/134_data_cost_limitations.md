# TASK134 — Data and Cost Limitations Register

**Purpose:** every data/cost limitation affecting the design, with
consequence and state. Nothing hidden, nothing patched.

## Data limitations

1. **Price-only index (no dividends).** ~1%/yr distributions omitted.
   Consequence: long exposure understated vs true total return;
   directionally conservative for net-long tilts, asymmetric across
   long/short months. Use permitted (ranking/signal largely unaffected).
   Unresolved: no in-repo total-return NASDAQ series spans 1986; ^NDX
   substitution needs a separate owner decision.
2. **3.41% missing observations** (362/10,602; no year >5% per TASK129).
   Stop rule (>5%/yr) predeclared. Executor re-verifies pre-use.
3. **Methodology drift** across 40 years embedded in the published index —
   disclosed, part of the tradeable object, not adjustable.
4. **No holdout exists.** Final evaluation has no sealed partition;
   protection is freeze-then-run procedure only.
5. **Single-file dependence.** Entire test rests on
   `data/fred/fred_NASDAQ100.csv`; SHA + span re-verified pre-use or stop.

## Cost limitations

6. **Batch-1 family is an assumption**, not a broker fact (vehicle
   mismatch: ETF precedent vs index CFD). Sensitivity grid bounds the
   uncertainty; it does not resolve it.
7. **No historical financing series.** Generic stress only; true CFD
   financing unmeasurable from records.
8. **Minimum-lot granularity** unaddressed (capital-agnostic evaluation,
   per PROTO-TREND-001 A13 precedent) — forward-demo matter.
9. **Turnover unknown pre-outcome.** Realized turnover reported; if it
   exceeds the grid's informative range, the result is reported as-is
   (no grid extension post-outcome).

## Stops tied to limitations

Any of: SHA/span mismatch, >5% yearly missingness, unverifiable costs
beyond the grid's coverage, or panel unavailability → STOP with a record,
no substitution, no repair.
