# QUANTFORGE — H01 EQUITY DATA SOURCE AUDIT V1

**Track:** A — Multi-market equity replication of the classic volatility-response asymmetry
**Type:** Data discovery / acquisition / validation ONLY. Not a protocol, not a definition lock, not an experiment, not a backtest, not a statistical analysis.
**Date:** 2026-08-16
**Status:** **B — PROMISING SOURCE, ADDITIONAL DUE DILIGENCE REQUIRED**
**Read-only on repository:** the only file created is this artifact. Bounded verification samples were downloaded to an external temporary directory (outside the repository); no raw data was placed in the QuantForge repository.

---

## 1. Purpose

Identify and validate a legitimate multi-market equity/index price dataset suitable for a future H01 equity replication (Track A). The scientific question the data must eventually support is:

> Does classic negative-shock volatility-response asymmetry generalize across a broader multi-market equity universe?

The minimum registered governance constraint is **≥2 evaluable equity markets per layer**, with daily prices, enough history for more than one regime, consistent timestamps, reproducible provenance and transformations, and no outcome-dependent market selection. This document records the existing-data gap, every source investigated, the bounded-sample verification performed, the candidate ranking (pre-declared criteria only), the decision gates, and the governance outcome. It deliberately does NOT select markets, horizons, matching, bootstrap parameters, thresholds, or methods, and it does NOT compute any H01 statistic.

---

## 2. Existing Equity Data Gap (confirmed from the frozen artifacts)

### Historical (HPD universe — frozen validation artifacts)

| Root | Instrument | Asset class | Region | Resolution | Coverage | Rolls | Quality flags |
|---|---|---|---|---|---|---|---|
| sp | S&P 500 | Equity index | US | **CORE VALID** | 1982-04-21 → 2002-10-01 | 82 | continuity_ok=True; 5,163 front rows |
| aor | All Ords (AUS) | ? (unresolved) | non-US | quarantined RESOLVED-NONUS | 1991-09-25 → 2001-09-28 | 35 | 8,890 zero-vol rows flagged; identity "?" |
| cac | CAC 40 (FRA) | ? (unresolved) | non-US | quarantined RESOLVED-NONUS | 1999-01-04 → 2002-10-01 | 15 | identity "?"; ~3.7y only |

- **`sp` is the only validated US equity index** (S&P 500 *futures*, front-month ratio back-adjusted). `aor` and `cac` are quarantined under the frozen H01 provenance rule (RESOLVED-NONUS, identity unresolved, "never re-admitted by outcome" — re-admission requires a separate provenance governance decision, not a data audit).
- **Historical gap:** exactly **1** legitimate equity market. ≥2 per historical layer is NOT achievable from the current validated universe.

### Contemporary (M1 universe — verified daily series)

- The M1 universe contains five daily series: XAUUSD, XAGUSD, EURUSD, BTCUSD, **USATECHIDXUSD** (2023-09-01 → 2026-07-10, 871 days). The only equity index is **USATECHIDXUSD**.
- No other equity price data exists locally (the TSMOM paper file is monthly factor returns only — insufficient frequency).
- **Contemporary gap:** exactly **1** equity market. ≥2 per contemporary layer requires new data.

**Net position (matches the screening):** a scientifically valid multi-market definition cannot be written from the current validated universes. External acquisition is required. This audit determines whether a legitimate source exists to fill the gap.

---

## 3. Sources Investigated

| # | Source | Category | Investigated how | Result |
|---|---|---|---|---|
| 1 | **FRED** (Federal Reserve Bank of St. Louis) | Free public (platform) / third-party-copyrighted series | Bounded download + full validation of 4 series | **EMPIRICALLY VALIDATED** — best candidate |
| 2 | **Yahoo Finance** | Free, undocumented reverse-engineered API | Bounded chart-API probes (8 symbols, full-history) | Depth verified; **license RESTRICTED** |
| 3 | **Stooq** | Free, personal-use license | Direct CSV endpoint + static bulk endpoint probes | **Access BLOCKED** (anti-bot); **license RESTRICTED** |
| 4 | Exchange/public index data (Euronext, Cboe, CME, LSE) | Registration-gated public | Documented; not downloaded | Registration-gated; limited free history; not verified this session |
| 5 | Academic/public datasets (Shiller; Kenneth French) | Public research data | Documented; not downloaded | **Insufficient frequency** (monthly) for the daily object |
| 6 | Paid vendors (Norgate, CSI, exchange data, marketdata.app, Polygon, Tiingo, Alpha Vantage) | Commercial | Documented as alternatives; nothing purchased | Clean licensing at cost; requires separate procurement decision |

No data was purchased. No full dataset was acquired. Bounded verification samples only (see §8 and §16).

---

## 4. Candidate Comparison Matrix

Criteria are the task's pre-declared list (scientific suitability, breadth, historical depth, reproducibility, provenance, licensing, data quality, acquisition stability, cost). Ranking is **never** informed by H01 v1.2 performance.

| Criterion | FRED | Yahoo (chart API) | Stooq | Paid vendors |
|---|---|---|---|---|
| Provider | Federal Reserve Bank of St. Louis | Yahoo Finance (undocumented endpoint) | Stooq (Poland) | e.g., Norgate / CSI / exchanges |
| Asset coverage | Equity **indices** (cash levels), US-centric | Equity indices, **international breadth** | Equity indices, international (^ symbols) | Broad (indices, futures) |
| Markets verified (equity) | 4 (SP500, DJIA, NASDAQCOM, NASDAQ100) | 8 probed (GSPC, NDX, DJI, FTSE, GDAXI, N225, HSI, STOXX50E) | 0 (all requests blocked) | n/a |
| Historical depth | NASDAQCOM 1971+; NASDAQ100 1986+; **SP500/DJIA only 2016+** | Deep: GSPC/N225 1970+; FTSE 1984+; GDAXI/HSI/NDX 1985-87+; DJI 1992+ | Unknown (blocked) | Vendor-dependent |
| Frequency | Daily (close only) | Daily | Daily | Daily |
| Raw price availability | Index levels (close), no OHLC/volume | Index levels + OHLC | OHLC | Vendor-dependent |
| Adjusted/unadjusted | Unadjusted index points (no dividend adj.) | Unadjusted index points | Unadjusted | Vendor-dependent |
| Corporate-action treatment | Handled by index provider (divisor); none needed at series level | Same | Same | Vendor-dependent |
| Futures vs index | **Cash index — no rolls required** | **Cash index — no rolls required** | Cash index | Often futures (roll logic needed) |
| Licensing (platform) | CLEAR — free, attribution notice required | RESTRICTED — ToS prohibit redistribution/automation | RESTRICTED — "personal use only; commercial use prohibited" | CLEAR (paid license) |
| Licensing (series archival) | **PENDING** — series third-party copyrighted (S&P DJI, Nasdaq); permission required for non-personal use | RESTRICTED — no written permission | RESTRICTED | CLEAR under contract |
| Reproducibility | HIGH — stable deterministic endpoint | LOW — undocumented, subsamples `range=max`, may break | FAIL — automated access blocked | HIGH (licensed feed) |
| Acquisition stability | Stable; pace requests (rate-limited under burst) | Unstable/undocumented; ToS risk | Blocked | Contractual |
| Cost | Free | Free (ToS-restricted) | Free (license-restricted) | Paid (no local precedent) |
| **Rank** | **1** | 2 (scientific breadth ideal, license-blocked) | 3 (blocked) | 4 (cost + procurement) |

---

## 5. Best Candidate Deep Review — FRED

### 5.1 Verified series (bounded full-history samples, 2026-08-16)

| Series ID | Market | Rows | Coverage | Notes |
|---|---|---|---|---|
| SP500 | S&P 500 index level | 2,610 | 2016-08-15 → 2026-08-14 | Daily series begins 2016-08-15 (documented 2016 reset of this series under the S&P DJI agreement); no pre-2016 history in FRED |
| DJIA | Dow Jones Industrial Average | 2,610 | 2016-08-15 → 2026-08-14 | Same 2016 reset |
| NASDAQCOM | Nasdaq Composite | 14,486 | 1971-02-05 → 2026-08-14 | Full history; index base 100.0 on 1971-02-05 (verified) |
| NASDAQ100 | Nasdaq-100 | 10,597 | 1986-01-02 → 2026-08-14 | Full history |

### 5.2 Integrity validation (bounded sample)

For every series: **0 duplicate dates, 0 weekend rows, 0 non-positive values, 0 calendar gaps > 5 days**. Missing-value rows (96 / 96 / 487 / 362) are **US exchange holidays** (Labor Day, Thanksgiving, Christmas, MLK, Good Friday, Memorial Day, July 4, etc.) listed with a "." placeholder — trivially dropped by the pipeline's existing missing-data rules; not data errors.

**Independent known-value spot checks (all PASS):**
- NASDAQCOM 2000-03-10 = **5,048.62** — exactly the documented Nasdaq Composite dot-com closing peak.
- NASDAQ100 1999-2001 max = **4,704.73** on 2000-03-27 — exactly the documented Nasdaq-100 closing peak (NDX peaked later than the Composite).
- NASDAQCOM 1987-10-19 = **360.21** — exactly the documented Black-Monday Nasdaq Composite close.
- NASDAQCOM 1971-02-05 = **100.00** — the index base date.
- SP500 2020-02-19 = **3,386.15** — the documented pre-COVID S&P 500 peak close.

### 5.3 Structure / scientific compatibility

- **Close-only daily cash index levels.** This is fully compatible with the H01 object: shocks are daily close-to-close log returns; realized variance is computed from daily log returns over the registered 5-day windows (identical construction to the existing HPD and M1 daily series in the pipeline, which are also close-based). No OHLC or intraday data is required by the object.
- **Cash index, not futures — no roll construction, no back-adjustment, no roll-jump artifacts.** This is a simplification relative to the HPD pipeline (which needed front-month ratio back-adjustment for `sp`), and it removes an entire class of construction risk.
- **Corporate-action treatment:** index providers recompute the index divisor for constituent changes; the published daily close is the standard object. No per-series adjustment step is needed (unlike single-stock series).
- **Comparability (G4): PASS.** The identical scientific object can be applied across all four markets without a definition change.

### 5.4 Licensing / provenance

- **Platform:** FRED is free to use; the FRED API Terms of Use require attribution ("This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis") and prohibit abuse (rate, replication of the site, etc.). The `fredgraph.csv` download path worked without an API key.
- **Series-level:** the FRED terms are explicit that data series may be **owned by third parties and subject to copyright restrictions**, and that **"before using data series owned by third parties for anything other than your own personal use, you must contact the data owner to obtain permission."** SP500/DJIA are © S&P Dow Jones Indices; NASDAQCOM/NASDAQ100 are © Nasdaq.
- **Status for this workspace:** personal/private research use is within the terms; **repository archival/redistribution is PENDING** (no written permission obtained). This is consistent with the repository's own established precedent: the HPD acquisition recorded its data license as **PENDING** and continues to use the data locally for research. Recording the license as PENDING (with attribution) is the honest status; it does not block a research definition lock, but it must be recorded in the ingestion provenance exactly as the HPD license was.
- **Access:** the `fredgraph.csv` endpoint was stable in the first pass; a burst of rapid probes triggered transient timeouts (rate-limiting posture). Paced, sequential requests are required — reproducible, not fragile.

### 5.5 Coverage limitations (the core finding)

- **US-only.** The four verified series are all US markets.
- **Historical S&P 500 / Dow are absent.** SP500 and DJIA begin 2016-08-15, so a historical layer (matching the HPD-era window 1982-2002) **cannot include S&P 500 or the Dow** from FRED. The historical layer from FRED is limited to the **two Nasdaq-family indices** (NASDAQ100 1986+, NASDAQCOM 1971+, common window 1986 → 2002, ≈16 years covering the 1987 crash, the 1990s bull, and the 2000-02 bear — genuinely multi-regime).
- **Independence caveat (historical):** NASDAQ100 and Nasdaq Composite are both Nasdaq US indices, heavily correlated (near-single-factor). Two near-duplicate markets are materially weaker than two independent markets for a *generalization* claim — the exact limitation the H01 ≥2-market rule exists to prevent. Whether a two-market Nasdaq-family historical layer is scientifically acceptable is a **definition-stage decision**, not one this audit may pre-empt.
- **Contemporary:** SP500, DJIA, NASDAQCOM, NASDAQ100 all run to 2026-08-14 → easily **≥2 (in fact 4) contemporary US markets**, complementing the M1 `USATECHIDXUSD`. The 2016-2026 contemporary window includes the 2018 Q4 selloff, the 2020 COVID crash, the 2022 bear market, and the 2024-26 cycle — multiple regimes.

---

## 6. Historical Coverage

| Source | Markets with deep history | Common multi-market window | Regime coverage |
|---|---|---|---|
| FRED | NASDAQ100 (1986+), NASDAQCOM (1971+) | 1986-01 → 2002 (≈16y), 2 markets | 1987 crash; 1990s bull; 2000-02 bear |
| FRED (SP500/DJIA) | — (2016+ only) | n/a for HPD-era window | n/a |
| Yahoo (restricted) | GSPC/N225 1970+; FTSE 1984+; GDAXI 1987+; HSI 1986+; NDX 1985+; DJI 1992+ | 1984 → 2002 with 4-7 markets | Multiple regimes incl. 1987, 1990-92, 1997-98, 2000-02 |
| Stooq (blocked) | Unknown (not retrievable) | n/a | n/a |

The only *free, clean-license* path to a historical multi-market layer is FRED's two Nasdaq-family indices. International historical breadth is only available via license-restricted access (Yahoo) or paid vendors.

---

## 7. Contemporary Coverage

| Source | Contemporary equity markets (verified) | Notes |
|---|---|---|
| FRED | SP500, DJIA, NASDAQCOM, NASDAQ100 (all → 2026-08-14) | 4 markets; multi-regime 2016-2026 |
| Existing M1 | USATECHIDXUSD (2023-09 → 2026-07) | MT5-sourced tech index; separate universe |

FRED satisfies the contemporary requirement outright (4 markets vs ≥2). A definition-stage decision is whether the contemporary layer is formed from FRED series alone, from M1 alone, or from a consistent mixed universe — that is a scientific-scope decision, not made here. No proxy (ETF/CFD) is needed to reach two contemporary markets, and none is proposed.

---

## 8. Data Integrity (bounded-sample verification results)

### FRED (full details in §5.2)
No duplicates, no weekend rows, no non-positive values, no >5-day calendar gaps; missing rows are US holidays; five independent known-value spot checks all matched documented values exactly. **Integrity: PASS.**

### Yahoo (chart API)
Full-history probes returned authentic anchor values (FTSE 100 = 1,000.0 on 1984-01-03, its documented base date; DAX ≈ 1,005 in Dec 1987, its documented base era; GSPC 93.0 in Jan 1970; N225 2,402.85 in Jan 1970; HSI 2,568.3 in Dec 1986). **But** the endpoint is undocumented: `range=max` silently returns subsampled/truncated windows (168-416 rows for 40-year ranges), and only explicit `period1/period2` requests return full daily history. This instability, combined with ToS prohibition, makes Yahoo unsuitable as the *archival* source even though its data is scientifically ideal.

### Stooq
Direct CSV endpoint returns a JavaScript proof-of-work anti-bot challenge page (796-byte HTML, no data) for every symbol; the static bulk endpoint returns HTTP 401. No data could be obtained for validation. Consistent with Stooq's documented Dec-2020 policy of no longer providing data for automatic downloading.

### Exchange/gated sources
Not downloaded (registration/login gating); recorded with unknown long-history availability — not forced into the design.

---

## 9. Licensing / Provenance

| Source | License status (workspace) | Basis |
|---|---|---|
| FRED platform | **CLEAR** | Free; attribution notice required; abuse/rate prohibitions (FRED API Terms of Use) |
| FRED series archival | **PENDING** | Series © S&P DJI (SP500/DJIA) and © Nasdaq (NASDAQCOM/NASDAQ100); written permission required for non-personal use — mirrors the HPD "license PENDING" precedent |
| Yahoo | **RESTRICTED** | Official Finance API terminated 2017 for ToS abuse; chart endpoint is reverse-engineered; ToS prohibit redistribution and third-party-accessible repositories; no written permission |
| Stooq | **RESTRICTED** | "This data is intended solely for personal use. Any commercial use is prohibited." (stooq.com/db/, /db/h/); automated download blocked |
| Paid vendors | CLEAR (under contract) | Requires a separate procurement decision; no local precedent |

**No permission is claimed where none exists.** No raw external data was placed in the repository. The bounded samples live only in an external temporary directory, fingerprinted (SHA-256) for provenance:

- `fred_SP500.csv` `351555b5556f3437…`, `fred_DJIA.csv` `29c8ca59469de81b…`, `fred_NASDAQCOM.csv` `51187aa6f103f27d…`, `fred_NASDAQ100.csv` `aeacca4f6472dd56…` (verification samples; re-acquired and re-verified at the approved ingestion stage).
- The seven `stooq_*.csv` files are the anti-bot challenge pages (fingerprints document the block, not data).

---

## 10. Scientific Suitability

- **The H01 object is fully compatible with close-only daily cash-index levels** (shock = close-to-close log return; RV = 5-day windows of daily log returns; identical to the existing pipeline construction). Close-only is not a deficiency for this object.
- **FRED supports a US-only multi-market design:** 2 deep historical (Nasdaq family) + 4 contemporary US markets. Scientifically defensible as *one leg* (US cross-sectional replication), with two caveats that are definition-stage questions, not this audit's to resolve: (i) the historical pair's near-single-factor correlation, and (ii) the absence of S&P 500 / Dow from the historical window — meaning the historical replication universe excludes the exact index family (`sp`, S&P 500) behind one of the two motivating observations.
- **International breadth is only available through license-restricted access or paid acquisition.** A "broader multi-market" reading that requires international markets cannot be met by any free, clean-license source verified here.
- **No proxy substitution is proposed.** ETFs, CFDs, or synthetic broker instruments would be required only to manufacture breadth that the genuine index sources already provide (FRED) or that are license-blocked (Yahoo/Stooq). No proxy is needed and none is recommended.

---

## 11. Reproducibility

- **FRED: HIGH.** The `fredgraph.csv` endpoint is deterministic and stable; another researcher can re-acquire identical data and reproduce the fingerprints; paced requests avoid rate-limiting. The transformation pipeline (drop holiday placeholder rows → daily log returns → H01 object) is standard and scriptable.
- **Yahoo: LOW.** Undocumented endpoint; `range=max` truncates; endpoint may change or throttle; re-acquisition is possible with the documented `period1/period2` recipe but is fragile.
- **Stooq: FAIL (access).** Automated re-acquisition currently impossible without a browser; the repo's Stooq precedent (`raja-grewal/stooq-commodities`, Codeberg, MIT) is **commodities-only** (gold, silver, copper, WTI, etc.) and does not extend to equity indices.

---

## 12. Decision Gates

| Gate | FRED | Yahoo | Stooq |
|---|---|---|---|
| **G1 Market breadth** (≥2 legit equity markets/layer) | **PASS** with caveat — historical pair is Nasdaq-family (near-single-factor); contemporary 4 markets; S&P 500 historical absent | PASS (7+ deep markets) | NOT ASSESSABLE (blocked) |
| **G2 Historical depth** (multi-regime) | **PASS** for Nasdaq pair (1986-2002, 16y, 3+ regimes); FAIL for SP500/DJIA (2016+) | PASS (deep, international) | NOT ASSESSABLE |
| **G3 Price integrity** (independently validated) | **PASS** — 5/5 known-value spot checks exact; zero integrity defects | PARTIAL — anchors authentic; API unstable | NOT ASSESSABLE |
| **G4 Comparability** (same H01 object) | **PASS** — cash index closes, no rolls, close-only compatible | PASS | PASS (in principle) |
| **G5 Licensing** (legitimate in workspace) | **PASS (platform) / PENDING (series archival)** — mirrors HPD precedent | **FAIL** — RESTRICTED | **FAIL** — RESTRICTED + blocked |
| **G6 Reproducibility** (re-acquire/fingerprint) | **PASS** | PARTIAL | FAIL |

**Gate summary:** FRED is the only source that passes all six gates (with G1's independence caveat and G5's PENDING archival status explicitly recorded). No source passes on all criteria without caveats.

---

## 13. Governance Decision

**B — PROMISING SOURCE, ADDITIONAL DUE DILIGENCE REQUIRED.**

FRED is empirically validated, clean-licensed at the platform level, reproducible, and satisfies the letter of the ≥2-market minimum (2 deep US historical markets; 4 contemporary US markets). It is the clear best candidate. However, three genuine items remain unresolved, and the task's final principle forbids lowering the standard to force a source into the design:

1. **Scientific scope (unresolved):** is a US-only universe — with a historical layer restricted to two near-duplicate Nasdaq-family indices, and **no S&P 500/Dow before 2016** — sufficient to test "generalization across a broader multi-market equity universe"? This is a scientific question for the outcome-blind definition stage, and it determines whether FRED alone can carry the track or whether international breadth is required.
2. **Licensing path (unresolved):** if international breadth is required, the only options are (a) written permission from the relevant data owners (Stooq/Yahoo terms make this unlikely for redistribution), or (b) a separately authorized paid vendor (Norgate/CSI/exchange data). If the US-only scope is accepted, FRED's series-archival status is recorded **PENDING** exactly as the HPD license was recorded.
3. **Acquisition-stage validation (pending by design):** full-history ingestion, gap/roll/continuity gates, and second-source cross-validation on a sample window follow the repository's established ingestion pattern at the approved ingestion stage — not in this audit.

**C is explicitly rejected** (a suitable free source does exist — FRED). **A is premature** because the scope and licensing questions above must be resolved before a definition lock can be written with confidence; deciding them here would either silently narrow the scientific claim (US-only) or silently authorize a licensing/procurement path — both are outside a data audit.

---

## 14. Exact Next Legitimate Task

**H01-EQUITY SCIENTIFIC DEFINITION LOCK**, conditional on the scope it itself must settle outcome-blind:

- If the definition-stage scope decision accepts a **US-only universe** → the definition lock proceeds with **FRED as the validated source** (NASDAQ100 + NASDAQCOM historical; SP500 + DJIA + Nasdaq pair contemporary), license recorded **PENDING** with attribution (HPD precedent), and full-history ingestion following the repository's standard validation pattern.
- If the scope decision requires **international breadth** → a separate **EQUITY DATA LICENSING / PROCUREMENT TASK** precedes the definition lock (written permission requests to data owners, or a paid-vendor procurement decision).

No protocol, no market list, no horizon, and no method is written now. The definition lock — when authorized — makes those decisions outcome-blind from the validated universe, never from H01 v1.2 performance.

---

## 15. Prohibited Follow-Up

Explicitly prohibited: selecting equity markets based on H01 v1.2 performance; dropping weak markets; choosing market counts to maximize significance; changing horizons because another horizon looked better; importing GJR/EGARCH as the primary test; introducing K-means/HMM/ML; using the equity result as a trading signal; merging Track A with TSMOM; re-opening the commodity branch; re-admitting quarantined HPD non-US roots (aor/cac) without a separate provenance governance decision; downloading full external datasets into the repository before the approved ingestion stage; substituting proxies (ETFs/CFDs/synthetic instruments) to reach two markets; treating FRED's US-only set as a substitute for international breadth without an explicit scope decision; claiming written permission for archival where none exists; reviving the universal H01 claim.

---

## 16. Integrity

- This audit modified the repository in exactly one way: the required artifact `output/research_discovery/H01_EQUITY_DATA_SOURCE_AUDIT_V1.md`. Everything else was read-only.
- Bounded verification samples (11 CSVs: 4 FRED series + 7 blocked Stooq responses) were downloaded to the external temporary directory `C:/Users/User10/AppData/Local/Temp/quantforge_eqsrc_audit/` — **outside** the repository — with SHA-256 fingerprints recorded (§9). No raw external data was placed in the repository; the samples are verification-only and will be re-acquired and re-verified at the approved ingestion stage.
- No H01 statistic was computed; no shock/ΔlnRV/asymmetry quantity was calculated; no GARCH/GJR/EGARCH was fitted; no market, horizon, matching parameter, bootstrap parameter, or threshold was selected; no prior or class was altered; no protocol or experiment script was created.
- Ranking used only the pre-declared data criteria (suitability, breadth, depth, reproducibility, provenance, licensing, quality, stability, cost). H01 v1.2 performance was never used to rank, include, or exclude any source or market.
- The frozen H01 protocol (v1.2.0), its artifacts, BOE/Assembly/Deployment, and all governance records are untouched.
