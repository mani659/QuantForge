# FEASIBILITY CHECK — Free Market-Data Sources for QuantForge

**Date:** 2026-10-07 (all URLs retrieved this date). **Scope:** feasibility only — no acquisition, no recommendations, no strategy/statistics output. **Method:** official endpoints / pre-installed libs only; ≤1 sample (≤2 months, one instrument) per source to scratch (`%TEMP%\opencode\feasibility_sample`), verified, then deleted (§3). No credentials; no package installs.

## 1. Per-source findings

### 1.1 Dukascopy (tick + M1: FX, index/commodity CFDs, BTC)

- **Official URLs:** `https://datafeed.dukascopy.com/datafeed/{SYMBOL}/{YYYY}/{MM-1}/{DD}/{HH}h_ticks.bi5` and `.../BID_candles_min_1.bi5` (month 0-indexed, day zero-padded; `ASK_candles_min_1.bi5` also 200; `LAST_candles_min_1.bi5` 404); docs `https://www.dukascopy.com/wiki/en/development/data-export/`; official instrument list JSONP `https://freeserv.dukascopy.com/2.0/?path=common/instruments` (needs `Referer`; 1604 instruments with `historical_filename` + `history_start_tick/60sec/60min/day`).
- **Terms verbatim — `https://www.dukascopy.com/swiss/english/legal-pages/terms-of-use/`, retrieved 2026-10-07:** "…you agree to use the WEBSITE solely for your own non-commercial use and benefit, and not for resale or other transfer or disposition to, or use by or for the benefit of, any other person or entity." · "Such download is licensed to you by DUKASCOPY ONLY for your own personal, non-commercial use in accordance with the TCU and does not transfer any other rights to you." · "You shall not use or attempt to use any 'scraper,' 'robot,' 'bot,' 'spider,' 'data mining,' 'computer code,' or any other automate device, program, tool, algorithm, process or methodology to access, acquire, copy, or monitor any portion of the WEBSITE, any data or content found on or accessed through the WEBSITE, or any other WEBSITE information without the prior express written consent of DUKASCOPY."
- **Personal research / local copy:** downloads licensed for personal non-commercial use; no separate data-redistribution license found.
- **Account:** not required (all endpoints fetched anonymously). **Rate limits:** no numeric policy published; observed 503 bursts after sustained requests (long cooldown) → throttling needed.
- **Format:** LZMA `.bi5` (auto/FORMAT_ALONE/FORMAT_RAW LZMA1). **M1 = 24 B BE:** `u32 sec-of-day, i32 open, i32 close, i32 low, i32 high, f32 volume` (validated fields 3/4=low/high over 7,200 bars). **Tick = 20 B BE:** `u32 ms-in-hour, i32 ask, i32 bid, f32 askVol, f32 bidVol` (598 ticks: ask>bid 100%, monotonic ts). Prices integer subunits, scale per instrument: EURUSD/GBPUSD/USDCHF/USDCAD/AUDUSD ×1e-5; USDJPY, XAU/XAG, WTI/Brent, index CFDs, UST-bond ×1e-3; BTCUSD ×1e-1 (all checked vs known market levels; instrument list carries scale metadata).
- **Timezone / daily cutoff:** GMT/UTC (folder = GMT day; M1 00:00→23:59 GMT verified; tick ms UTC). Daily candles not probed → daily = **built** by GMT-day aggregation (FX 24×5; index/CFD M1 only during exchange sessions → partial GMT days).
- **Price type:** bid (sampled `BID_`); `ASK_` exists; ticks carry both sides.
- **Gaps:** pre-history folders return **stub files** (HTTP 200, constant o=c=l=h, vol 0) — verified XAUUSD 2000-06-15 & 2003-01-15 flat 1250, XAGUSD 1999-06-15 flat 375 → content validation mandatory; official metadata can differ from datafeed (EURUSD ticks real 2003-05-05 vs `history_start_tick` 2007-01-01; XAGUSD M1 real ≤2003-12-15 vs metadata tick 2014-07-25; DEUIDXEUR M1 real ≤2013-11-15 vs metadata 2012-06-14); throttling; per-instrument dates §2.

### 1.2 Yahoo Finance (Batch-1 route)

- **Official URL:** `https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}` via Batch-1 `yfinance` (`yf.download(t, period="max", auto_adjust=True)`), `output/prototypes/lane_b_batch1/fetch_data.py`.
- **Terms verbatim:** YDN Guidelines `https://legal.yahoo.com/us/en/yahoo/guidelines/ydn/index.html` — "Some of our APIs and Web Services are made available only for non-commercial use. For such APIs and Web Services, it's NOT PERMITTED to: Use these services in high traffic, established commercial-oriented or business web sites or applications; Incorporate these services into applications or websites monetized indirectly (by advertising, affiliate links) or directly…" · "We typically do not grant additional queries for these non-commercial use only services." · Yahoo API TOU `https://legal.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.html` — "PLEASE NOTE that Yahoo's APIs may be subject to rate limits at Yahoo's absolute and sole discretion." (both retrieved 2026-10-07)
- **Personal research / local copy:** non-commercial use permitted; no redistribution/archival grant found. **Account:** not required (chart JSON keyless). **Rate limits:** discretionary, no numeric value published.
- **Format:** JSON chart → OHLCV; pandas `auto_adjust=True` → adjusted Close (sample cols `Close,High,Low,Open,Volume`).
- **Timezone / daily cutoff:** per-symbol `exchangeTimezoneName` (FX Europe/London; US index/futures America/New_York; ^N225 Asia/Tokyo; BTC-USD UTC); daily bar = exchange-timezone calendar day (sample: 00:00 Europe/London rows). Daily **direct**.
- **Price type:** single adjusted OHLC (no bid/ask). **Gaps:** `XAUUSD=X`, `XAGUSD=X`, `FGBL=F` 404; futures symbols are continuous (roll not investigated); first-trade dates §2 (24 symbols probed).

### 1.3 FRED (St. Louis Fed)

- **Official URL:** `https://fred.stlouisfed.org/graph/fredgraph.csv?id={ID}` (CSV `observation_date,{ID}`, business-day rows).
- **Terms verbatim — `https://fred.stlouisfed.org/legal/terms`, retrieved 2026-10-07:** "FRED provides data and data services to the public for non-commercial, educational, and personal uses subject to a few prohibitions. Furthermore, other uses (e.g., commercial) are subject to additional restrictions." · "You may NOT… Suggest the Federal Reserve Bank of St. Louis or FRED endorses your product, service, opinion, arguments, or conclusions. Take all the data on FRED or related services and claim it is a unique product or service…" · "(g) Use scripts, spiders, scrapers, bots, or any manual or automatic technology, tool, software, process, or device to access or collect information from the FRED® Services in any manner that is excessive, disruptive, or adversely impacts the stability, performance, or availability of the FRED® Services" · "…FRED® Content in connection with the development or training of any software program or system or machine learning, including, but not limited to, large language models, deep learning, generative artificial intelligence…"
- **Personal research / local copy:** CSV downloads verified accountless; keep data-owner copyright notices (page: permission must come from data owner, not St. Louis Fed).
- **Account:** not required (optional). **Rate limits:** none published; browser-like User-Agent → HTTP 000 (blocked), default curl UA works; sporadic 503/000.
- **Format:** CSV, date-only, business days (holidays omitted/empty). **Timezone:** none (dates only); publication lags per series not audited. Daily **direct**. **Price type:** single reference value (spot/yield).
- **Gaps (`fred_meta.json` dcterms ranges):** DCOILWTICO 1986-01-02→2026-09-29; DCOILBRENTEU 1987-05-20→2026-09-29; DEXUSEU 1999-01-04→2026-10-02; DEXUSUK/DEXJPUS/DEXUSAL/DEXCAUS/DEXSZUS 1971-01-04→2026-10-02; DGS2 1976-06-01, DGS10 1962-01-02, DGS30 1977-02-15 (→2026-10-05); SP500 & DJIA 2016-10-07, NASDAQCOM 1971-02-05, NIKKEI225 1949-05-16 (→2026-10-06); DTB3 1954-01-04; TB3MS 1934-01-01. **Absent:** `GOLDAMGBD228NLBM`/`SLVPRUSD` → "IBA Data To Be Removed From FRED"; no DAX/FTSE/Bund/BTC/NDX (NASDAQCOM ≠ NDX); `DEXJPY` invalid → use `DEXJPUS`.

### 1.4 U.S. Treasury — Daily Par Yield Curve (rates, 1990→)

- **Official URL:** `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{YEAR}/all?type=daily_treasury_yield_curve&field_tdr_date_value={YEAR}&page&_format=csv` (yearly; monthly variant `&month={YYYYMM}`).
- **Terms verbatim — `https://www.treasurydirect.gov/terms.htm`, retrieved 2026-10-07 (HTTP 505 to plain curl; content fetched):** "These Terms and Conditions govern the access and use of our website … as they may from time to time be modified by TreasuryDirect.gov, fiscal.treasury.gov, and all other websites operated by the Bureau of the Fiscal Service ('Fiscal Service')." · "Government works generally cannot be copyrighted, though we request that we be given appropriate credit." · "You may view, download and print material on this site for non-commercial personal use only."
- **Methodology verbatim — `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView`:** "…the daily yield curve rates… are closing market bid prices…" · "…indicative, bid-side market price quotations (not actual transactions)… at or near 3:30 PM each trading day."
- **Personal research / local copy:** view/download/print for non-commercial personal use; government works not copyrightable (credit requested). Note: CSVs live on home.treasury.gov while the T&C names Fiscal Service sites; home.treasury.gov site-policies has **no data-specific license** (checked).
- **Account:** not required. **Rate limits:** none published/observed. **Format:** CSV `Date,"1 Mo"…"30 Yr"`; current files add `1.5 Month` (15 cols); 1990 file 9 tenors (10 cols); MM/DD/YYYY descending. **Timezone / cutoff:** U.S. trading days, ~15:30 ET quote time. Daily **direct**. **Price type:** bid only. **Coverage:** **1990-01-02→present** (1990 = 250 rows; 1989 file 200-but-0-bytes → nothing earlier); holidays absent. **Gaps:** tenor set changed over time; rates only, no prices of §2 instruments.

### 1.5 Binance Vision (BTC kline archives)

- **Official URLs:** `https://data.binance.vision/data/spot/monthly/klines/{PAIR}/{interval}/{PAIR}-{interval}-{YYYY}-{MM}.zip`, `/data/spot/daily/...`; README at `https://data.binance.vision/`.
- **Terms verbatim — `https://data.binance.vision/terms-of-use.html` (PDF, extracted with PyPDF2): "BINANCE VISION DATASET TERMS" v1.0, Last Updated August 26, 2026:** §3.1 "Datasets are provided to You under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License ('CC BY-NC-SA 4.0'), incorporated herein by reference, except where specifically designated otherwise." · §4.1 "Permitted non-commercial uses are limited to academic research, non-monetized open educational projects, algorithmic historical backtesting for purely personal non-production research, and non-commercial open-source data science evaluations." · §4.2 "You shall not use the Datasets for live proprietary trading execution, automated commercial order generation, or signal distribution to third parties for direct or indirect compensation." · §7.1 "You agree to strictly abide by all posted rate limits, automated script guidelines, and download protocols established on the Binance Vision repository and API base endpoints."
- **Personal research / local copy:** backtesting for personal non-production research explicitly permitted; caching under CC BY-NC-SA 4.0. **Account:** not required. **Rate limits:** §7.1 references posted limits; numeric values not enumerated in fetched README.
- **Format:** ZIP → headerless 12-col CSV (open time μs-UTC, OHLC, volume, close time, quote volume, trades, taker fields, ignore). **Timezone / cutoff:** UTC day, bars open 00:00 UTC. Daily **direct**. **Price type:** last-trade OHLC (klines; depth not sampled). **Coverage:** BTCUSDT monthly from 2017-08 (2017-07 404), daily from 2017-08-17 (2017-08-16 404); BTCEUR/BTCBUSD 2023-01 archives present. **Gaps:** spot crypto only; delisted pairs remain archived; no header; §5.3 lets Binance discontinue datasets without notice.

### 1.6 Stooq (daily CSV)

- **Official URL:** `https://stooq.com/q/d/l/?s={sym}[&d1=…&d2=…]&i=d`; bulk `https://stooq.com/db/h/`.
- **Terms verbatim — `https://stooq.com/terms.html`, retrieved 2026-10-07:** §5.3 "Redistribution of data found on the website is not allowed without the consent of Stooq." · §6.1 "The Index data may be used only for your own personal, non-commercial purposes."
- **Personal research / local copy:** redistribution restricted; commercial limits apply (licensed-index clauses). **Account:** not required, but **JS-gated**: all 25 CSV probes returned HTTP 200 with an identical 796-byte JavaScript proof-of-work challenge ("This site requires JavaScript to verify your browser") instead of CSV; `db/h/` likewise; PoW POST attempts to `/stooq.com/__verify` produced no CSV. **Rate limits:** n/a (gated first). **Format / timezone / price / coverage:** unverified (no CSV) → §8.

## 2. Coverage table — 18 instruments

Legend: T=tick, M1=1-min, D=daily; cell = `{symbol} {res} {earliest}`; **—** = absent (footnotes). Dukascopy earliest = first **content-verified real** file (stubs excluded); (…) = official platform metadata where different. Latest dates per source: Dukascopy ≥2026-09-15 (probed 200); Yahoo daily 2026-09-29+; FRED FX 2026-10-02, yields 2026-10-05, indices 2026-10-06, WTI/Brent 2026-09-29; Treasury 2026-07-31 (sample; current yearly file); Binance monthly 2026-08-31 (sample); Stooq n/a.

| # | Instrument | Dukascopy | Yahoo | FRED | Binance | Stooq |
|---|---|---|---|---|---|---|
| 1 | XAUUSD gold | XAUUSD T+M1 2003-05-05 (stubs 1999–2003-01) | GC=F D 2000-08-30 futures; XAUUSD=X 404 | — IBA gold removed | — | — |
| 2 | XAGUSD silver | XAGUSD M1 ≤2003-12-15 (>2003-05-05 stub); T meta 2014-07-25 | SI=F D 2000-08-30 futures; XAGUSD=X 404 | — IBA silver removed | — | — |
| 3 | EURUSD | EURUSD T+M1 2003-05-04 | EURUSD=X D 2003-12-01 | DEXUSEU D 1999-01-04 | — | — |
| 4 | GBPUSD | GBPUSD M1 2003-05-05 (T meta 2012-02-09) | GBPUSD=X D 2003-12-01 | DEXUSUK D 1971-01-04 | — | — |
| 5 | USDJPY | USDJPY M1 2003-05-05 (T meta 2007-03-27) | USDJPY=X D 1996-10-30 | DEXJPUS D 1971-01-04 | — | — |
| 6 | AUDUSD | AUDUSD T+M1 2003-08-04 | AUDUSD=X D 2006-05-15 | DEXUSAL D 1971-01-04 | — | — |
| 7 | USDCAD | USDCAD M1 2003-08-04 (T meta 2012-02-09) | USDCAD=X D 2003-09-16 | DEXCAUS D 1971-01-04 | — | — |
| 8 | USDCHF | USDCHF M1 2003-05-05 (T meta 2012-02-09) | USDCHF=X D 2003-09-16 | DEXSZUS D 1971-01-04 | — | — |
| 9 | S&P 500 | USA500IDXUSD T+M1 2012-06-15 (meta 2012-01-16) | ^GSPC D 1927-12-30 | SP500 D 2016-10-07 | — | — |
| 10 | Nasdaq-100 | USATECHIDXUSD T+M1 2012-06-15 | ^NDX D 1985-10-01 | — (NASDAQCOM ≠ NDX) | — | — |
| 11 | DAX | DEUIDXEUR M1 2013-11-15 (2013-09-16 absent; T meta 2012-06-14) | ^GDAXI D 1987-12-30 | — | — | — |
| 12 | FTSE 100 | GBRIDXGBP T+M1 2012-06-15 | ^FTSE D 1984-01-03 | — | — | — |
| 13 | Nikkei 225 | JPNIDXJPY T+M1 2012-06-15 | ^N225 D 1965-01-05 | NIKKEI225 D 1949-05-16 | — | — |
| 14 | WTI | LIGHTCMDUSD T+M1 2012-06-15 (60s meta 2011-12-20) | CL=F D 2000-08-23 futures | DCOILWTICO D 1986-01-02 | — | — |
| 15 | Brent | BRENTCMDUSD T+M1 2011-06-15 (meta 2010-12-02) | BZ=F D 2007-07-30 futures | DCOILBRENTEU D 1987-05-20 | — | — |
| 16 | US T-Bond | USTBONDTRUSD T+M1 2018-06-15 (meta 2018-12-18) | ZB=F D 2000-09-21 (also ZN=F) | DGS30 D 1977-02-15 (yield, not price) | — | — |
| 17 | Bund | BUNDTREUR T+M1 2016-06-15 (meta 2016-05-02) | — (FGBL=F 404) | — | — | — |
| 18 | BTCUSD | BTCUSD T+M1 2017-05-08 (meta 2017-05-07; 2016-06 absent) | BTC-USD D 2014-09-17 | — | BTCUSDT D 2017-08-17 (spot) | — |

**Daily direct vs built:** Dukascopy **built** (GMT calendar day from M1; index/CFD days = session GMT days); Yahoo **direct** (exchange-TZ day, bar ts 00:00 exchange TZ); FRED **direct** (business date, no time); Treasury **direct** (U.S. trading day, ~15:30 ET); Binance **direct** (UTC day, 00:00 UTC); Stooq unverified.

**Treasury note (rates, not one of the 18):** daily par yield curve all tenors 1 Mo–30 Yr, **1990-01-02→present** (§1.4); FRED also serves DGS2/DGS10/DGS30/DTB3/TB3MS daily yields.

## 3. Samples verified (≤1/source; all deleted after recording)

| Source | Sample | Window | Rows | First → last | Columns | Bytes | sha256 | Parse |
|---|---|---|---|---|---|---|---|---|
| Dukascopy M1 | EURUSD 5 daily `BID_candles_min_1.bi5` | 2024-04-01..05 GMT | 1,440×5=7,200 | 04-01T00:00 → 04-05T23:59 GMT | ts,o,c,l,h,vol bin | 10,427–11,392 | per file (first d5edc4dc296067138a05e60b585179467227446e02a34d17a59eec01141f5d5a) | **ok** |
| Dukascopy tick | EURUSD `22h_ticks.bi5` | 2024-04-01 22h GMT | 598 | 22:00:00.161 → 22:59:53.882 | ask,bid,askVol,bidVol | 3,096 | 92203979396cb6f2e2d8e105a202ff71b925601d0ddda2855860fddf193eb6c2 | **ok**, ask>bid 100% |
| Yahoo | yfinance EURUSD=X daily | 2026-08-03..09-29 | 42 | 2026-08-03 → 2026-09-29 | Close,High,Low,Open,Volume | 3,837 | 13f47aee270139a278e4343c294a6a8403d78ba8cf171380224fe1b3523725a5 | **ok** |
| FRED | fredgraph.csv DCOILWTICO | 2026-07-01..08-31 | 44 | 69.74 → 87.03 | observation_date,DCOILWTICO | 771 | d428f05a03eb4281302434d05c9b4309cf4a72e6b9247d1b0250b51fb46e369c | **ok** |
| Treasury | monthly 202606 / 202607 | 2026-06 / 2026-07 | 21 / 22 | 06-30→06-01 / 07-31→07-01 (desc) | Date + 14 tenors (incl 1.5 Month) | 1,811 / 1,892 | 57764f0d…a19a41 / 58205642…0b82364 | **ok** |
| Treasury probe | yearly 1990 | 1990-01-02..12-31 | 250 | 12-31 → 01-02 (desc) | Date + 9 tenors | 14,069 | d8d5e4bb7ae2f13ccf03a7f50537723a4a5a37e2ebe85da3e32f53328c411d18 | **ok** (1989 empty) |
| Binance | BTCUSDT-1d-2026-08.zip | 2026-08 UTC | 31 | 62,887.88 → 77,682.00 | 12 headerless | 2,185 | fd8374a811ac7d3f4144d9c857c4f10796402c178316a25ed0c2f0ca6e16a8c1 | **ok** |
| Stooq | none obtained | — | — | — | — | — | — | challenge page 796 B |

Scope compliance: each source ≤1 instrument; ≤2 months except Treasury availability probe (single year file, deleted). Probe JSONs + terms documents retained in scratch only; all data samples deleted.

## 4. (a) Backward extension of the five QuantForge M1 instruments (`data/m1`)

Existing spans (MT5 broker UTC stamps): BTCUSD 2021-05-23→2026-05-22, EURUSD 2021-01-04→2026-06-30, USATECHIDXUSD 2023-09-01→2026-07-10, XAGUSD 2021-07-13→2026-07-12, XAUUSD 2021-04-12→2026-04-10.

| Instrument | Dukascopy earliest real M1 (verified) | Earliest tick | Extension vs existing | Pitfalls |
|---|---|---|---|---|
| EURUSD | **2003-05-04** (132-bar Sunday day verified) | **2003-05-05** (metadata 2007-01-01 is wrong/older) | ≈17.7 yr | ×1e-5; bid vs broker series; GMT vs MT5 day edges |
| XAUUSD | **2003-05-05** (stubs flat 2000-06-15, 2003-01-15) | meta 2003-05-05 | ≈17.9 yr | filter pre-2003 stubs by constant price; ×1e-3 |
| XAGUSD | **(2003-05-05, 2003-09-15]** (stub then real) | meta 2014-07-25 only | ≈17.5 yr | stubs pre-start; boundary not pinned (§8); ×1e-3 |
| BTCUSD | **2017-05-08** (meta 2017-05-07) | meta 2017-05-07 | ≈4.0 yr | CFD vs spot/Binance; ×1e-1; early-BTC gaps |
| USATECHIDXUSD | **2012-06-15** | meta 2012-06-14 | ≈11.2 yr | CFD not index; session-only M1; ×1e-3; ^NDX daily cross-check from 1985 |

Overlap periods exist for all five (validation possible later); none performed here (bulk download out of scope).

## 5. (b) Bid / ask / mid by source

| Source | Fields | Bid/ask? | Mid buildable? |
|---|---|---|---|
| Dukascopy tick | ask + bid + per-side volumes (verified) | **both** | yes, per tick |
| Dukascopy M1 | `BID_` and `ASK_` series (both 200; `LAST_` 404) | **both (two series)** | yes, aligned series (sample = BID) |
| Yahoo | adjusted single OHLCV | no (convention unpublished) | n/a |
| FRED | one reference value/date | no | n/a |
| Treasury | bid only ("closing market bid prices", verbatim) | bid | no (no ask) |
| Binance klines | last-trade OHLC (depth endpoint not sampled) | no in klines | n/a |
| Stooq | unverified | unknown | unknown |

Existing `data/m1`: broker single OHLCV, no bid/ask.

## 6. (c) Restrictions bearing on automated-trading use

- **Dukascopy:** non-commercial-only ("solely for your own non-commercial use") + express ban on "scraper/robot/bot/spider… to access, acquire, copy, or monitor… without the prior express written consent" (verbatim §1.1) → automated bulk download faces the TCU on its face; no research exemption found on retrieved pages.
- **Yahoo:** several APIs "made available only for non-commercial use"; NOT PERMITTED in high-traffic/commercial-oriented applications; extra queries "typically" not granted; rate limits sole-discretion; attribution required (§1.2). No scraping/chart-JSON blessing found.
- **FRED:** personal/non-commercial use allowed; scripts/bots prohibited only when "excessive, disruptive, or adversely impacts" stability (verbatim) — moderate collection not categorically banned; AI/ML-training use prohibited; endorsement/product-claim bans apply.
- **Treasury:** "view, download and print … for non-commercial personal use only" (verbatim); automated collection neither named nor prohibited in T&C; no separate CSV/API policy found.
- **Binance Vision:** "algorithmic historical backtesting for purely personal non-production research" permitted; "live proprietary trading execution", "automated commercial order generation", commercial bot platforms forbidden (§4.2/4.4); posted rate limits/protocols binding (§7.1); CC BY-NC-SA 4.0 for local copies/derivatives.
- **Stooq:** redistribution ban (verbatim §5.3) + bot-gated access.
- Cross-cutting: every personal-use permission comes with redistribution/publication limits; most restrict commercial deployment; none of the retrieved terms bans a private local backtest over personally stored copies.

## 7. Dependencies (nothing installed)

Python 3.11.9 · stdlib (`lzma`, `struct`, `csv`, `json`, `hashlib`, `re`, `subprocess`) · yfinance 1.6.0 · requests 2.34.2 · pandas 3.0.2 · PyPDF2 3.0.1 · Windows built-in `curl.exe`. Zero installs performed.

## 8. NOT FOUND / not verified

1. **Stooq CSV sample:** JS PoW challenge on every CSV/bulk probe from this network; only terms.html retrieved; symbol coverage/format/timezone unverified; data-page "personal use only" quote only in search snippet, not retrieved directly.
2. **FRED:** no gold/silver (IBA removal), no DAX/FTSE/Bund/BTC/NDX series; no numeric rate limit on fetched pages; per-series publication lags not audited.
3. **Yahoo:** `XAUUSD=X`/`XAGUSD=X`/`FGBL=F` 404; no numeric rate limits; futures roll mechanics and intraday coverage not audited.
4. **Dukascopy:** `LAST_candles` 404 (no native mid/last M1); D1 files unprobed (M1/tick only); numeric rate-limit policy unpublished; 503 cooldown unquantified; XAGUSD start bracketed to (2003-05-05, 2003-09-15] and DEUIDXEUR to (2013-09-16, 2013-11-15] — not pinned to the day; BUNDTREUR price level not cross-validated vs independent quote (real-vs-stub done, scale/contract semantics open); tick eras for XAGUSD/indices unprobed beyond metadata; `history_start_*` metadata conflicts with datafeed (§1.1).
5. **Treasury:** no data-specific license on home.treasury.gov (site-policies checked); nothing ≤1989 (1989 file empty); tenor set varies by era.
6. **Binance:** no FX/indices/metals; numeric rate limits not enumerated in fetched README; kline bid/ask absent.
7. No account-registration paths tested anywhere (all access claims verified anonymously).
8. Not performed (out of scope): bulk downloads, `data/m1`↔source continuity/timezone-alignment checks, statistics backtests.


---

**Report metadata (finish):** file size = 23872 bytes (including this line); sha256 of all preceding content (file without this final line) = `0e93d5de12541a7dee5240924073e8b4e44f939328ba324e8bca1c44ecce579e`.