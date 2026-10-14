# TASK128 — Owner Decision Proposal

## Decision: A — EXPERIMENT PROPOSAL READY

One direction is sufficiently justified and its proposed test is
implementable with verified existing data, **conditional on a §99.1
ruling** confirming that volatility-scaled TSMOM is distinct from fixed
TSMOM (DISC-022).

## Recommended direction

**Volatility-scaled time-series momentum on NASDAQ100.**

- **Mechanism:** signal = sign(r12) × (target_vol / realized_vol)
- **Instrument:** NASDAQ100 index (FRED daily, 1986→2026, 10,602 obs)
- **Data readiness:** verified, authorized for research use, 40 years
- **Distinctness:** regime-conditional sizing vs fixed sizing (mechanistic
  distinction, pending §99.1 ruling)
- **Costs:** Batch-1 frozen family as starting point
- **Testability:** ~480 monthly observations, adequate power
- **Preregistrability:** design fully specified above

## Why it outranks alternatives

- **vs fixed TSMOM:** barred by DISC-022 (same mechanism)
- **vs mean reversion:** barred by DISC-021/NEG-065 (permanent closure)
- **vs turn-of-month:** same mechanism class as PROTO-TOM-001 (failed)
- **vs FOMC drift:** low power (46 events), same family as RS-401 (failed)
- **vs intraday session:** many closed, data too short
- **vs cross-sectional:** structurally underpowered (TASK125/126)
- **vs vol regime switching:** promising but less developed than
  vol-scaled TSMOM; could be a follow-up

## Precise experiment that should follow

1. Owner rules on §99.1 distinction (vol-scaled vs fixed TSMOM)
2. If distinct: freeze preregistration (design above) + cost model
3. Run development-period analysis (1986→2005)
4. If development is promising: run validation (2006→2015)
5. If validation confirms: run final evaluation (2016→2026)

## Additional owner authorization required

1. **§99.1 ruling** on vol-scaled TSMOM vs fixed TSMOM
2. **Evaluation authorization** for NASDAQ100 (no current authorization
   exists for non-Batch-1 datasets)
3. **Cost model freeze** (NASDAQ100-specific or Batch-1 family)

## What evidence would cause abandonment

- §99.1 ruling bars the direction (variant of fixed TSMOM)
- Development-period results show no improvement over fixed momentum
- Cost model cannot be established at a defensible level
- Data integrity issues (missing data > 5% in any year)

## Is new data purchase necessary?

**No.** NASDAQ100 FRED data is verified, authorized for research use, and
provides 40 years of daily observations. No new data purchase is required.
The only prerequisite is the §9.1 ruling and evaluation authorization.

## TASK128 authorization boundary

TASK128 authorized this analysis only. It does not authorize the
§99.1 ruling, the evaluation authorization, or any execution of the
proposed experiment.
