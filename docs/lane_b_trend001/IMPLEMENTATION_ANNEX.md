# TASK70 — EXECUTE APPROVED REOPENING (IMPLEMENTATION ANNEX RECORD)

Task: proto-trend-001-full-run
Repo: QuantForge (private research repo). Authorized scope: the signed
PART B of PROTO-TREND-001_spec_and_authorization.md (owner: Salman,
2026-10-08). Nothing outside that scope is authorized.

RUN FLAGS (the owner edits these two lines only)

HARD RULES
- Work only inside: output/prototypes/lane_b_trend001/ and
  docs/lane_b_trend001/ (create both). No edit to any existing file,
  engine, partition, governance doc, ledger or config. Do not register
  anything in any ledger. No commit, no push, no package install, no
  network access except the two vendors in S3. NEVER print credentials.
- Use the repo's own Python interpreter and already-installed pandas,
  numpy, yfinance, requests. If something is missing, stop and report.
- Do not run the QuantForge engine. This prototype uses its own
  stand-alone script (the repo's Lane B precedent).
- No decision may be taken by looking at real-data results. Where this
  prompt and the spec are silent or conflict, STOP and ask; never choose
  after seeing numbers.
- Hard stop after Phase 1 unless PHASE_2_GO: YES. Hard stop after one
  bounded report in Phase 2. No rerun, no variant, no tuning, ever.

PRECONDITION (check first)
Part B must contain a confirmed B3, B4 = ACCEPT, B5 = YES, and a signature
line with a name and date. If any [bracket] remains, or Part A text differs
from the version the owner reviewed, STOP and report. Do nothing else.

==================== PHASE 1 ====================

S1 Citation check (text only)
 Verify the two citations in A1 from public sources. If a citation TEXT is
 wrong, correct only the text. If the paper's rule parameters differ from
 A3 (12-month look-back, 1-month hold, EWMA volatility with 60-day centre
 of mass), do NOT change the rule: stop and report the discrepancy.

S2 Freeze
 Save the signed spec under docs/lane_b_trend001/. sha256 of Part A is the
 exact text between the "PART A" and "PART B" headings; write its first 16
 hex characters into B1, and HEAD, branch and working-tree status into B2.
 Also save THIS prompt (without the flags) as IMPLEMENTATION_ANNEX.md and
 record its sha256. Make the frozen files read-only.

S3 Acquisition (once)
 Exactly the 15 series in A2.
  Yahoo (yfinance, period="max", auto_adjust=True): ^GSPC ^NDX ^GDAXI ^FTSE
  ^N225 EURUSD=X GBPUSD=X USDJPY=X AUDUSD=X USDCAD=X USDCHF=X GC=F SI=F
  BTC-USD.
  FRED CSV (default user agent): https://fred.stlouisfed.org/graph/
  fredgraph.csv?id=DCOILBRENTEU  (Brent spot).
 At most 1 request per second, at most 2 retries per series, no other
 vendor, no substitution, no Dukascopy, Binance or Stooq.
 Store raw files unmodified in data_raw/ with MANIFEST.csv: series, vendor
 URL, retrieval time UTC, rows, first date, last date, sha256. Save the
 vendor terms URLs and retrieval dates beside it.

S4 Integrity gate (A11 only)
 Per series: monotonic dates; duplicates; gaps over 5 consecutive business
 days inside the active span; days with |daily simple return| > 25%
 (> 8% for GC=F and SI=F), listed with date and value; count of NaN rows.
 Compute NOTHING else. Do not fix, fill or remove any series. If any
 series fails, report it and still complete S5 and S6.
 Write universe.json: the 15 series, each marked PASS or REVIEW from the
 gate (the owner may remove a market before Phase 2; the evaluator reads
 universe.json and applies no other filter).

S5 Write the evaluator (evaluate.py) per the IMPLEMENTATION ANNEX below.
 Write unit tests and the synthetic self-test (IA-12). All run on synthetic
 data only; no real series is loaded in S5.

S6 Freeze the code
 Run the self-test; it must pass. Compute sha256 of evaluate.py, its test
 file and universe.json; record them in CODE_FREEZE.md. After this point
 the code is read-only. Write GATE_REPORT.md (max ~15 KB): precondition
 result, S1 findings, the Part A hash, the manifest table, the S4 table,
 every series needing review, self-test results, code hashes.
 STOP. Print file sizes and sha256s only; do not paste report contents.
 If PHASE_2_GO is NO, the run ends here.

==================== PHASE 2 (only if PHASE_2_GO: YES) ====================

S7 Run once
 Verify the code hashes still match CODE_FREEZE.md; if not, STOP.
 Run evaluate.py once on the real data and universe.json. Write
 results.json, monthly_series.csv and REPORT.md. Run it a second time into
 a scratch folder and confirm results.json is byte-identical (determinism
 check); then delete the scratch run. STOP. Do not run anything else.

==================== IMPLEMENTATION ANNEX ====================
These clarifications resolve ambiguity only; they do not change Part A.

IA-1 Prices: use the vendor 'Close' column (auto_adjusted for Yahoo).
  Brent: the FRED value column. Drop NaN rows. No forward-fill, no
  interpolation, no volume use. A "trading day" is one observation of the
  market's own series (this makes bitcoin's 252 observations about 8.3
  months; disclosed, and covered by the ex-bitcoin diagnostic).
IA-2 Per market i and calendar month m (signal month):
  s(i,m) = last observation date in month m.
  e(i,m) = first observation date strictly after s(i,m)  (entry).
  Holding return R(i,m) = P(e(i,m+1)) / P(e(i,m)) - 1.
  Each market uses its own calendar; there is no master calendar.
IA-3 Signal: sign( P(s) / P(s - L observations) - 1 ), L = 252 (primary);
  63 and 126 for the neighbourhood diagnostic. Zero return -> flat (0).
  Uses data with date <= s only.
IA-4 Volatility: daily simple returns r_t = P_t / P_{t-1} - 1;
  sigma_hat = r.ewm(com=60, adjust=False, min_periods=60).std() * sqrt(252),
  taken at s. Same sqrt(252) for all markets.
IA-5 Position p(i,m) = signal * 0.10 / sigma_hat. A market is ACTIVE in month
  m iff it has L observations of history, a valid sigma_hat > 0, and a
  holding return computable with e(i,m+1) <= 2026-09-30.
IA-6 N(m) = number of active markets. Target weight w(i,m) = p(i,m) / N(m).
  Gross return G(m) = sum_i w(i,m) * R(i,m).
IA-7 Month window: verdict months are those whose entry date e(i,m) is on
  or after 2010-01-01. Excluded-but-reported: entry dates 2004-01-01 to
  2009-12-31. Last month included: the last month with e(i,m+1) <= cutoff
  (expected: signal month 2026-07). Sub-periods by entry-date year:
  2010-2019 and 2020-2026. Record N(m) for every month; if N(m) < 8 in the
  first verdict month, STOP with DATA-INTEGRITY STOP.
IA-8 Costs. c(i) per side in decimal, from B3 by class: FX majors 0.0001;
  gold 0.00015; silver 0.0007; equity indices 0.0002; Brent 0.0004;
  bitcoin 0.0007. Cost(m) = sum_i c(i) * |w(i,m) - w(i,m-1)| with w = 0 for
  a market not held in the prior month (first month builds from zero; a sign
  flip is charged on the full change). Net N(m) = G(m) - Cost(m).
  Cost grid: multiply c by 0.5, 1, 2, 4 (diagnostic; verdict at x1).
IA-9 Statistics (monthly net series, verdict window).
  Sharpe = mean / std(ddof=1) * sqrt(12), no risk-free subtraction.
  Bootstrap: circular block bootstrap, block 12 months, B = 10000,
  seed 20261007; lower bound = 5th percentile of the bootstrap mean.
  Drawdown: rescale the net series by 0.10 / (std * sqrt(12)), compound
  monthly, report the maximum peak-to-trough drawdown.
  IA-10 Criteria exactly as A7: (1) net Sharpe >= 0.30; (2) bootstrap lower
  bound of mean > 0; (3) net Sharpe > 0 in both sub-periods; (4) net Sharpe
  > 0 for L = 63, 126 and 252; (5) rescaled max drawdown <= 25%; (6) net
  Sharpe > 0 after subtracting (0.04/12) * sum_i |w(i,m)| each month.
  Closure label: all six pass -> PASS-TO-FORWARD; if F-SNAP (below) net
  Sharpe <= 0 add " (FINANCING WARNING)". Any failure -> ECONOMICALLY
  INSUFFICIENT if the GROSS series has Sharpe >= 0.30 and bootstrap lower
  bound > 0, otherwise NEGATIVE.
IA-11 F-SNAP (diagnostic, not a criterion). Annual rate for a held side:
  max(0, -swap_points) * point * 365 / price. Per-month charge =
  sum_i |w(i,m)| * rate(i, side) / 12, side by the sign of p. Swap points
  (G0, 2026-10-07; symbol: swap_long / swap_short / point):
   US500m -164.9/0.0/0.01 (S&P 500 ^GSPC)  USTECm -696.4/0.0/0.01 (^NDX)
   DE30m -42.8/0.0/0.1 (^GDAXI)  UK100m -168.6/0.0/0.01 (^FTSE)
   JP225m 0.0/0.0/0.1 (^N225)  EURUSDm -5.7/0.0/1e-5  GBPUSDm -2.2/-0.5/1e-5
   USDJPYm 0.0/-13.9/0.001  AUDUSDm 0.0/-2.0/1e-5  USDCADm 0.0/-8.9/1e-5
   USDCHFm 0.0/-10.3/1e-5  XAUUSDm -536.7/0.0/0.001 (GC=F)
   XAGUSDm -7.9/0.0/0.001 (SI=F)  BTCUSDm -1886.4/0.0/0.01
   Brent (UKOILm): EXCLUDED from F-SNAP (anomalous value).
  price = the vendor series price at e(i,m).
IA-12 Self-test (synthetic data only, before any real run). Required:
  (a) date logic on a toy calendar: s, e, holding windows and the last
      month are exactly as IA-2/IA-7;
  (b) no look-ahead: for every month, recompute the signal and sigma_hat
      from the series truncated at s(i,m) and assert they equal the full-run
      values; plant a deliberate one-bar leak in a copy and assert the
      check FAILS;
  (c) planted effect: 15 synthetic markets with time-series momentum built
      in; the evaluator must return net mean > 0 and bootstrap lower
      bound > 0 (seeded);
  (d) null: i.i.d. noise markets; over 100 seeded replications (B = 2000
      for the test only) the fraction with lower bound > 0 must be <= 10%;
  (e) cost arithmetic: with zero signal change the cost is zero; a full
      sign flip is charged 2x|w|; a hand-computed 3-month toy matches;
  (f) the evaluator refuses to load any date after 2026-09-30.
  All must pass, otherwise STOP and report.
IA-13 Diagnostics to report (A8, no others): per-market gross contribution
  and turnover; gross vs net; cost decomposition; leverage distribution
  (max, mean of sum |w|); exposure by class; realised volatility; skewness;
  yearly net returns; ex-bitcoin portfolio; cost grid; financing stress at
  0, 2, 4, 6 percent; the 2004-2009 reported-only window; sub-periods;
  neighbourhood L = 63/126/252; the control (all signs +1, same costs);
  correlation of net with the control; worst 10 months; N(m) over time.
IA-14 REPORT.md layout: the A7 criteria table with PASS/FAIL and values; the
  primary outcome with the bootstrap interval; the closure label; the
  diagnostics; the A9 limitations; and the A12 power statement ("about 200
  monthly observations; a fail is not strong evidence of no edge"). No
  recommendations, no interpretation beyond the pre-declared label.
IA-15 Bounded output: no figures required; CSV for the monthly series.
  Finish by printing file sizes and sha256s and any item NOT FOUND or STOPPED.
