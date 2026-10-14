# TASK135 — Gap 3 Decision: Forward-Data Granularity and Implementation

## Finding

- **Minimum bar frequency: DAILY bars suffice.** The frozen rule needs
  monthly closes (r12), prior-month daily closes (volatility), and
  next-session opens (execution). All are definable from daily bars by
  construction. M1/tick data are explicitly NOT required and must not be
  introduced (scope expansion + data-scope violation).
- **Execution timing:** next available row date after month-end T
  (the series itself defines sessions; no NYSE calendar file needed).
- **Source capability verified by construction** (no empirical
  computation): 10,602 daily rows span 1986–2026; monthly resampling,
  prior-month std, and next-row lookup are deterministic transforms of
  daily closes. Admissibility of the source for these transforms follows
  from its verified identity (TASK129), not from any new inspection.
- **Implementation:** none exists on record → minimal exact-to-spec build
  gated by review + synthetic self-test before any market-data contact
  (PROTO-TREND-001 IA-12 pattern, cited as pattern).

## Carried limitations (unchanged, still unresolved)

Costs (assumption + grid, no broker facts), dividends (omitted, disclosed),
financing (stress-only), tradability granularity (forward-demo matter).
No download, collection, or empirical computation performed or needed for
any finding above.
