# VS-TSMOM-01 Report (single bounded evaluation under v5)

## Decision rules (frozen v5; Holm α=0.05 across {D1, D2}; ratio bar CONFIRMED ACTIVE at 2.0)

- D1 lower bound > 0 (Holm-adj) AND ratio ≥ 2 → PASS
- D1 upper bound < 0 → FAIL
- Else → INCONCLUSIVE

## Primary outcome with bootstrap interval (D1, paired scaled−fixed)

mean net differential −0.005500/mo (−55.0 bps); 95% interval
[−0.008809, −0.002236]; Holm-adjusted p = 1.0; n = 474 months
(1987-02→2026-07); seed 20261014.

## Secondary (D2, paired scaled−passive)

mean −0.008064/mo (−80.6 bps); 95% interval [−0.012539, −0.003034];
Holm-adjusted p = 1.0. Gates nothing; reported.

## Benefit-to-friction ratio

benefit −0.005500 / friction 0.000306 = −17.96 (bar: ≥ 2). Not met.

## Closure label

FAIL — D1 upper bound (−0.002236) < 0. No promotion, no continuation, no
rescue. Budget consumed.

## Diagnostics (descriptive, non-inferential)

- Skips: no_anchor 12 (1986 warmup), no_entry 1 (final month), no_vol 0.
- Turnover (mean |w|, scaled leg): 0.5558. Total scaled-leg costs: disclosed
  in monthly_series.csv (friction 3.06 bps/mo mean).
- Vol tracking: realized annualized scaled-portfolio vol 0.1141 vs 0.10
  target — the scaling mechanism operated near target; economics failed anyway.
- Cost grid (mean D1 / mean D2): ×0.5 −54.4/−79.1 bps; ×1 −55.0/−80.6;
  ×2 −56.3/−83.7; ×4 −58.8/−89.7. Negative at every multiplier.
- Financing stress (scaled-leg mean net): 0% +52.3 bps; 2% +43.0; 4% +33.7.
- Yearly D1/D2 breakdowns: 40 years in monthly_series.csv/summary.json.
- Mechanism note: fixed leg (≈+107 bps/mo) and passive (≈+133 bps/mo)
  both exceeded the scaled leg (≈+52 bps/mo) — volatility scaling
  underweighted high-volatility advances; the drag is structural to the
  scaling rule on this panel, not an implementation artifact.

## Limitations (mandatory tradability caveat)

Close-to-close NASDAQ-100 price-index test ONLY — not next-open execution
and not evidence of tradable net profitability. Price index excludes
~1%/yr distributions; no historical financing series exists (generic
stress only); Batch-1 costs are declared assumptions, not broker facts;
index-CFD lot granularity unaddressed. No statement here supports live,
paper, or deployment use.

## Power statement

About 474 monthly paired observations; the interval excludes zero on the
negative side — this is evidence against incremental value at the tested
scale, not proof of universal absence.
