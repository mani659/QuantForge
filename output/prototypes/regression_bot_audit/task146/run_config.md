# TASK146 run configuration — fixed pre-outcome (any deviation voids the run)

- data_file: data/fred/fred_NASDAQ100.csv
- data_sha256: 1196c3f2dca171c1b56b4bbe2cc1fcd51ec7ea1f30bb74d7c3cfc2a313ffe52f (recomputed this session; EXACT match to H01 manifest row)
- data_meta: 10602 rows, 1986-01-02 to 2026-08-21, monotonic, unique, tz-naive-as-UTC (timestamps only, no values read for this check)
- frozen spec: VS-TSMOM-01 v5 (task144, 1974fe6d…); B4 (d1e1a823…); COMP-01 (1d76fc1c…); ratio bar CONFIRMED ACTIVE at 2.0 (owner verdict, this turn)
- rule: r12 = P(T)/P(T-12m)-1, T = last non-missing daily close of month; direction = sign (zero -> flat)
- vol: prior calendar month daily simple returns std, ddof=1 (pandas default + VM-001 n-1 precedent), xsqrt(252); non-finite/non-positive -> skip month (counted); no other minimum exists on record, none set
- positions: scaled w = sign*min(1, 0.10/sigma); fixed f = sign*1.0 (definitional constant-size counterpart, shared 1.0 cap); passive p = 1.0; first month builds from zero (flat -> target IS a target change)
- entry E(m) = first daily close strictly after T(m) (CLOSE-01 next-close rule); holding return R(m) = E(m+1)/E(m) - 1; same-close fills prohibited
- missing months (no T, no anchor, insufficient vol, no entry/exit): excluded from ALL series, counted
- costs: Batch-1 family 10/5/0 bps per side on |Delta w|; grid x0.5/1/2/4; financing stress 0/2/4% per year on gross notional |w| (stress-only)
- inference: circular block bootstrap block 12, B=10000, seed 20261014; one-sided 95% lower bound (5th pct); upper bound = 95th pct (matching end of the stated interval); one-sided bootstrap p; Holm alpha 0.05 across {D1, D2}
- verdict: PASS iff D1 lower>0 AND D1 Holm p<0.05 AND ratio>=2 (ratio = mean D1 net / mean scaled-leg cost drag; friction==0 -> bar unmet); FAIL iff D1 upper<0; else INCONCLUSIVE
- execution: single run, this config only; engine vs_tsmom_engine.py as reviewed (G4: 12/12 synthetic self-tests, determinism verified, one alignment bug + one spec-conformance correction pre-data)
