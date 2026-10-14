# TASK123 — Failure Classification (tested vs untested vs administrative)

**Method:** 143 ledger rows classified by evidence type. Definitions:
- **economic_failure**: direct empirical result showing non-viability
  (ECONOMICALLY_NONVIABLE, COST_FAILURE, STATISTICALLY_UNSUPPORTED,
  SAMPLE_INSUFFICIENT).
- **contradiction**: mechanism contradicted by test (MECHANISM_CONTRADICTED).
- **inconclusive**: data/measurement prevented evaluation (DATA_FAILURE,
  DATA_ALIGNMENT_FAILURE, VALIDATION_FAILURE).
- **administrative_exclusion**: closed on governance/process grounds
  without economic test (ROBUSTNESS_FAILURE topology variants).
- **duplicate**: ruled redundant (DUPLICATE_MECHANISM).
- **mixed_or_other**: composite rows.
- **not_tested**: NOT_EVALUATED / UNKNOWN.

## Counts (reconcile to 123_failure_population.csv)

| Evidence type | Count | % |
|---|---:|---:|
| economic_failure | 66 | 46.2% |
| not_tested | 36 | 25.2% |
| contradiction | 12 | 8.4% |
| inconclusive | 10 | 7.0% |
| duplicate | 4 | 2.8% |
| administrative_exclusion | 4 | 2.8% |
| mixed_or_other | 11 | 7.7% |

**Tested (exact implementation empirically evaluated): 107 rows (74.8%).**
**Not tested (NOT_EVALUATED/UNKNOWN): 36 rows (25.2%).**

## Critical sub-counts

- **Single-shot (n_configs=1, no neighborhood): 93 of 107 evaluated rows.**
- **Costs UNKNOWN: 85 of 107 evaluated rows (79.4%).**
- **Sample N UNKNOWN: 58 of 107 evaluated rows (54.2%).**
- **Validation/confirmation present: 0 of 107 evaluated rows** (all "none").

## Lane B tested rows (the only ones with realistic cost treatment)

PROTO-GEM-001 (dual momentum, N=220, COST_FAILURE); PROTO-VM-001 (vol
targeting, N=283, COST_FAILURE); PROTO-TOM-001 (turn-of-month, N=403,
COST_FAILURE); PROTO-RS204/RS302/RS401/RS404/RS405 (calendar/event,
COST/DATA failures); PROTO-OPEX-001 (OPEX, N=404, COST_FAILURE);
PROTO-EMA-GRAB (trend pullback, N=393, COST_FAILURE); TASK57-MDP-001
(bounded discovery, ROBUSTNESS_FAILURE topology); TASK60-REBAL-001,
TASK61-CORR-001 (allocation variants, ROBUSTNESS_FAILURE +
STATISTICALLY_UNSUPPORTED). **All failed.** The Lane B track has never
produced a promotable prototype.

## Distinguishing CAND-025 from the regression concepts

CAND-025 (Macro Shock Liquidity Void Reversal) is a **range-spike reversal**
on USATECHIDXUSD M1 — a post-shock liquidity-void refill mechanism. It is
**NOT** a regression concept. R1 (RG-TREND-001) and R2 (RG-REVERT-001) are
**regression-line hypotheses** (fit a line to price; trade slope/residual).
They share the word "reversal" but are mechanistically distinct: CAND-025
uses a volatility-shock trigger with a fixed-session exit; R1/R2 use
least-squares estimation of a price trend/baseline. **CAND-025 never tested
either regression concept; its NO-GO does not inform the R1/R2 exclusions.**

## Limitations

- Ledger `grade` VERIFIED/PARTIALLY_VERIFIED flags indicate verification
  of the record's existence, not of the underlying economic claims.
- 12 rows are PARTIALLY_VERIFIED (incl. the composite CAND-015/019/020 row).
- Several rows have MIXED failure classes with per-item grades in notes;
  classified here by the dominant/most severe class.
- "economic_failure" includes STATISTICALLY_UNSUPPORTED (39 rows) — these
  are **single-shot tests without inferential statistics**, not true
  economic falsifications. Treating them as falsifications would overstate
  the evidence base.
