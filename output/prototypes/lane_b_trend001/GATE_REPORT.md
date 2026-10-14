# GATE_REPORT — PROTO-TREND-001 freeze / acquire / integrity (Phase 1)

## 1. Precondition: PASS

Signed Part B supplied by owner (Salman, 2026-10-08): B3 **Decision: CONFIRMED** (table values byte-equal to draft proposal: FX 0.5/0.5/0, gold 0.5/1.0/0, silver 6.0/1.0/0, equity 1.0/1.0/0, Brent 3.0/1.0/0, bitcoin 6.0/1.0/0); B4 **Owner decision: ACCEPT**; B5 **Owner approval: YES**; Authorization **Salman / 2026-10-08**; **Signature: Salman**. No bracket placeholders remain in B1–B5/authorization/signature. Single Part A source: Downloads draft (sha256 ae573661…; LF text); frozen Part A sliced byte-identical from it.

## 2. S1 citation check: PASS, no text change, no STOP

- Moskowitz, Ooi, Pedersen (2012), "Time series momentum," J. Financial Economics 104(2), 228–250 — confirmed (CBS portal; ScienceDirect DOI 10.1016/j.jfineco.2011.11.003; EconPapers; RePEc). Text correct.
- Hurst, Ooi, Pedersen (2017), "A Century of Evidence on Trend-Following Investing," J. Portfolio Management 44(1), 15–29 — confirmed (CBS portal; JPM site; DOI 10.3905/jpm.2017.44.1.015). Text correct.
- Rule params vs paper (§2.4/eq.5): 12-month formation return r(t−12,t) ✓; 1-month hold r(t,t+1) ✓; EW variance with "center of mass δ/(1−δ) = 60 days" ✓ verbatim ("centre of mass 60 trading days" matches); 40% vol target, position = 40%/σ ✓ ("The paper's target is 40%; prototype uses 10% (scale only)" is accurate, a disclosed adaptation, not a discrepancy).

## 3. S2 freeze

Part A = file lines 10–109 (everything between the PART A and PART B headings). sha256 `4b44615dcf1646bd752dbaf6604f3c3a8c513840d2686228ec818eecddcbf35f`, first16 `4b44615dcf1646bd` → written into B1. B2: HEAD 666c1a9af38a05cde9fb2931d80a4f4c53846b1c / branch main / pre-start tree 76 modified + 126 untracked (pre-existing, untouched); no MT5/config calls, no commit/push. Frozen file `docs/lane_b_trend001/PROTO-TREND-001_spec_and_authorization.md` (17722 B, sha256 58137021…8d08d2e59). Annex `IMPLEMENTATION_ANNEX.md` = prompt minus the two RUN FLAG lines (10611 B, sha256 fd544bd3…40b81e8). Both read-only. Notes: DRAFT/UNSIGNED labels retained verbatim from the draft template (superseded by the filled signature block; "nothing more" rule); owner's B3 replaces draft B3 (the draft's cutoff sentence is superseded; cutoff retained in A5/A7); env provisioned per owner instruction (repo .venv now pandas 3.0.6 / numpy 2.4.6 / yfinance 1.7.0 / requests 2.34.2).

## 4. S3 manifest (15/15 acquired, 0 failures, 0 retries needed; ≥1.2 s pacing; Yahoo Batch-1 route period=max auto_adjust=True, yfinance 1.7.0, endpoint query2/v8/finance/chart; Brent via FRED CSV default UA, 1 request)

series | rows | first → last | sha256 (first 12)
^GSPC | 24809 | 1927-12-30 → 2026-10-07 | d70a7fe62044
^NDX | 10334 | 1985-10-01 → 2026-10-07 | 3dee6850d64f
^GDAXI | 9806 | 1987-12-30 → 2026-10-08 | 11ca43e44252
^FTSE | 10804 | 1984-01-03 → 2026-10-08 | 2848f7f9bd9a
^N225 | 15182 | 1965-01-05 → 2026-10-08 | 68aeedb6c371
EURUSD=X | 5930 | 2003-12-01 → 2026-10-08 | 9c419f0dc491
GBPUSD=X | 5942 | 2003-12-01 → 2026-10-08 | 165d50e790d4
USDJPY=X | 7764 | 1996-10-30 → 2026-10-08 | 7eb2cf9c0031
AUDUSD=X | 5306 | 2006-05-16 → 2026-10-08 | 990198aa2765
USDCAD=X | 5997 | 2003-09-17 → 2026-10-07 | 54b0f150d71b
USDCHF=X | 5995 | 2003-09-17 → 2026-10-07 | 568f8bb0d1b8
GC=F | 6552 | 2000-08-30 → 2026-10-08 | 5a7d5fa33249
SI=F | 6553 | 2000-08-30 → 2026-10-08 | 50ceb118b906
BTC-USD | 4405 | 2014-09-17 → 2026-10-08 | af897bafeacc
DCOILBRENTEU | 10275 | 1987-05-20 → 2026-10-06 | ed1eaa6fd4a9
Full hashes + per-series retrieval timestamps (2026-10-08T11:38–11:39Z) in data_raw/MANIFEST.csv. Vendor terms URLs + dates in data_raw/vendor_terms.txt (Yahoo API TOU; FRED legal/terms; both retrieved 2026-10-08). Raw files stored unmodified (Batch-1 CSV layout; FRED bytes verbatim). Starts match A2 expectations (1927/1985/1987/1984/1965/2003-12/2003-12/1996/2006-05/2003-09/2003-09/2000-08/2000-08/1987-05/2014-09).

## 5. S4 integrity (A11 only; row-to-row Close returns; business days = Mon–Fri)

series | monotonic | dups | NaN rows | missing weekdays | gap>5b | flags
^GSPC | Y | 0 | 0 | 960 | 1 | 0
^NDX | Y | 0 | 0 | 368 | 0 | 0
^GDAXI | Y | 0 | 0 | 311 | 0 | 0
^FTSE | Y | 0 | 0 | 354 | 0 | 0
^N225 | Y | 0 | 0 | 931 | 1 | 0
EURUSD=X | Y | 0 | 0 | 34 | 1 | 0
GBPUSD=X | Y | 0 | 0 | 22 | 0 | 0
USDJPY=X | Y | 0 | 0 | 48 | 1 | 0
AUDUSD=X | Y | 0 | 0 | 17 | 0 | 0
USDCAD=X | Y | 0 | 0 | 19 | 0 | 0
USDCHF=X | Y | 0 | 0 | 21 | 0 | 0
GC=F | Y | 0 | 0 | 260 | 0 | 3
SI=F | Y | 0 | 0 | 259 | 0 | 45
BTC-USD | Y | 0 | 0 | 0 | 0 | 2
DCOILBRENTEU | Y | 0 | 1173 | 0 | 0 | 4
Gaps: ^GSPC 1933-03-06..14 (US bank holiday, pre-verdict); ^N225 2019-04-29..05-06 (Golden Week/imperial transition); EURUSD=X + USDJPY=X 2008-08-11..25 (11 weekdays, vendor hole, pre-verdict). Brent NaN = holiday non-observations (dropped per IA-1).
Flags (>25%; >8% GC/SI): GC=F: 2008-09-17 +0.090277; 2013-04-15 -0.093538; 2026-01-30 -0.107796. BTC-USD: 2017-12-07 +0.252472; 2020-03-12 -0.371695. Brent: 1991-01-17 -0.30317; 2020-04-02 +0.352037; 2020-04-21 -0.474654; 2020-04-22 +0.509868. SI=F (45): 2004-04-21 -0.111671; 2004-12-08 -0.093901; 2006-04-20 -0.137182; 2006-04-24 -0.092017; 2006-04-28 +0.0834; 2006-06-13 -0.130494; 2006-09-11 -0.086738; 2007-08-16 -0.084119; 2008-03-20 -0.086437; 2008-08-15 -0.099409; 2008-09-17 +0.110686; 2008-09-18 +0.088468; 2008-10-02 -0.13011; 2008-10-10 -0.107868; 2008-10-29 +0.115472; 2008-11-24 +0.0923; 2008-12-01 -0.081983; 2009-03-19 +0.129707; 2011-05-05 -0.080035; 2011-09-22 -0.096042; 2011-09-23 -0.177541; 2013-04-15 -0.112719; 2013-06-20 -0.083249; 2013-09-19 +0.08032; 2016-11-14 -0.098258; 2020-03-13 -0.094292; 2020-03-16 -0.116491; 2020-08-11 -0.109816; 2020-09-21 -0.100969; 2021-01-08 -0.09625; 2021-02-01 +0.092862; 2021-02-02 -0.102524; 2022-10-03 +0.082226; 2025-04-04 -0.085668; 2025-12-29 -0.086682; 2025-12-30 +0.107621; 2025-12-31 -0.093571; 2026-01-26 +0.140253; 2026-01-27 -0.083047; 2026-01-30 -0.313468; 2026-02-03 +0.081586; 2026-02-05 -0.090727; 2026-02-12 -0.098001; 2026-03-19 -0.082032; 2026-05-15 -0.091283.

## 6. Series needing review (REVIEW in universe.json)

^GSPC, ^N225, EURUSD=X, USDJPY=X (gaps above); GC=F, SI=F, BTC-USD, DCOILBRENTEU (flags above; SI 45 flags suggest possible roll artifacts per A9 — individual review required before any use). PASS: ^NDX, ^GDAXI, ^FTSE, GBPUSD=X, AUDUSD=X, USDCAD=X, USDCHF=X. Nothing removed or fixed (S4 report-only). No series fails outright (all monotonic, no duplicates; gaps/flags documented for review).

## 7. Self-test + code freeze

test_evaluate.py (synthetic only; never loads data_raw): 41/41 PASS — IA-12a date logic + cutoff; units; IA-12b truncated-equals + planted-leak FAILS; IA-12c planted 15-market momentum net>0 and bootstrap lower>0; IA-12d 100 null reps within 10%; IA-12e zero-change/flip/hand-toy costs + grid scaling; IA-12f cutoff refusal. CODE_FREEZE.md: evaluate.py 12543 B sha256 d2dc2eb9…fcf03; test_evaluate.py 9050 B sha256 6777e88e…71e; universe.json 2160 B sha256 60a55578…0830fb; all read-only.

PHASE_2_GO: NO — run ends here. No evaluation performed.
