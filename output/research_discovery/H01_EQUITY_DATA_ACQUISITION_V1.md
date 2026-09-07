# QUANTFORGE — H01 EQUITY DATA ACQUISITION & LICENSING RESOLUTION V1

**Track:** A — Multi-market equity replication of the classic volatility-response asymmetry
**Type:** Data acquisition / source verification / licensing resolution ONLY. Not a definition lock, not a protocol, not an experiment, not a statistical analysis of H01 quantities.
**Date:** 2026-08-16
**Status:** **A — EQUITY DATASET READY FOR DEFINITION LOCK (US-anchored scope)**, with an explicit scope qualification (see §14).
**Repository read-only except this artifact:** bounded verification samples were downloaded to the external temporary directory; no raw data was placed in the repository.

---

## 1. Executive Verdict

**A — EQUITY DATASET READY FOR DEFINITION LOCK**, for a **US-anchored, two-exposure** replication.

The scope decision's open item — a historical layer reduced to a single Nasdaq factor — is resolved by assembling a **composite universe from already-validated sources**: the in-repository HPD `sp` (S&P 500 *futures*, 1982-2002, CORE VALID) supplies the **broad-US historical exposure** that FRED alone cannot, and FRED's NASDAQ100/NASDAQCOM supply the US-tech exposure. The historical layer is therefore **two distinct exposures**, not one factor. The contemporary layer is four validated FRED markets spanning the same two exposures. All components are reproducible, and the licensing path is **resolved as PENDING** for every component (written-permission requirements documented; requests prepared but NOT sent), consistent with the repository's established HPD license-PENDING precedent.

**Scope qualification (GOVERNANCE DECISION, not a fact):** the international-breadth variant of the claim is **NOT achievable from free, archiveable sources** — this session re-verified that Yahoo and Stooq remain license-restricted/blocked, CME is access-gated (403), Euronext is login-gated, and FRED's non-US daily index coverage is absent. The US-anchored universe is ready now; the international variant requires a separately authorized paid acquisition path (Norgate/CSI/Databento) or an explicit scope revision. The definition lock's first act must be the operator's confirmation of the US-anchored scope (or authorization of the paid path).

**Two new verification findings (SOURCE-DERIVED FACT):**
1. **Nasdaq official API early history is unreliable.** For Nasdaq-100, the provider's own API (api.nasdaq.com) deviates from FRED **and** Yahoo by up to 15.5% on 1996-2003 dates (129 dates >1% in 1996 alone), with FRED and Yahoo agreeing essentially exactly (median |Δret| = 0.0003 bp over 1996-2004). FRED's NASDAQ100 is the authoritative source; the Nasdaq API is usable only for *contemporary* provider-direct OHLC, not as the historical source.
2. **HPD `sp` (futures) vs cash S&P 500 are return-comparable but not return-identical.** Daily-return corr 0.946, median |Δ| = 16.4 bp, with concentrated dislocations in the 1987 crisis (Dec-87 futures closed at 201.50 vs cash 224.84 on 1987-10-19 — a genuine documented futures/cash divergence, not an HPD data error) and isolated roll/basis days. `sp` is confirmed as a faithful S&P 500 exposure, but mixing futures and cash series in one layer requires the **registered futures/cash comparability rule** — a definition-lock item, now with evidence.

---

## 2. Scientific Requirement

**Claim (from the scope decision):** the classic negative-shock volatility-response asymmetry, already ESTABLISHED for US equities, generalizes across multiple **independent** equity exposures (US-anchored; international where available).

- Daily or higher-frequency market-level price data; meaningful historical depth; multiple regimes; deterministic timestamps; reproducible provenance and transformations; defensible licensing.
- The registered ≥2-evaluable-market rule is a **minimum evaluability floor**, not the definition of adequate generalization; the binding constraint is **factor independence per era** (exposure diversity), not ticker count.
- No new numerical market-count requirement is invented here; the numeric breadth target remains an unresolved definition-lock question (recorded per the scope decision §6).

---

## 3. Existing Data Gap

(Confirmed from frozen artifacts; SOURCE-DERIVED FACT.)
- Historical: `sp` (S&P 500 futures, CORE VALID, 1982-04-21 → 2002-10-01, 82 rolls) is the only validated equity market; `aor`/`cac` remain quarantined RESOLVED-NONUS (identity unresolved), excluded by the frozen provenance rule.
- Contemporary: `USATECHIDXUSD` (M1, 2023-09-01 → 2026-07-10) is the only equity market.
- Gap per the scope decision: at least one **additional distinct historical equity exposure** beyond the Nasdaq pair, plus a resolved archival-licensing path.

**Resolution (MODEL INFERENCE from validated data):** the required additional distinct historical exposure already exists in-repository — HPD `sp` is the broad-US (S&P 500) historical exposure. Assembled with FRED's Nasdaq series, the historical layer is two exposures. No new historical ticker needs to be *acquired* for the US-anchored claim; what was required was **validation and licensing resolution**, which this task performed (§9-§11).

---

## 4. Sources Investigated

| # | Source | Category | This session | Result |
|---|---|---|---|---|
| 1 | **FRED** (St. Louis Fed) | Free public platform / third-party series | Prior audit validated 4 series; NDX now corroborated by Yahoo (§10) | **VALIDATED — part of the composite** |
| 2 | **Nasdaq official API** (api.nasdaq.com) | Provider-direct free | NEW: NDX full-history probe (7,775 rows, 1996-06-06+) + fidelity test vs FRED/Yahoo | **Early data (1996-2003) UNRELIABLE**; usable for contemporary OHLC only |
| 3 | **HPD `sp`** (in-repository) | Existing validated dataset | NEW: futures-vs-cash comparability vs ^GSPC (§10) | **VALIDATED — broad-US historical exposure** |
| 4 | **Yahoo Finance** (chart API) | Free, undocumented, RESTRICTED | Used ONLY for one-off read-only validation comparisons (not archived) | Depth re-verified; license RESTRICTED |
| 5 | **Stooq** | Free, personal-use | (Prior audit: blocked) | Access BLOCKED + RESTRICTED |
| 6 | **CME** (settlement data) | Exchange, free/gated | NEW: settlements endpoint 403 Forbidden | **Access-gated** — not usable this session |
| 7 | **Euronext** (CAC 40) | Exchange, registration-gated | NEW: public page login-gated | **Registration-gated** — not usable automated |
| 8 | Academic datasets (Shiller, K. French) | Public | (Prior audit) | Monthly only — insufficient frequency |
| 9 | Paid vendors (Norgate, CSI, Databento) | Commercial | Compared on paper (§11); nothing purchased | CLEAR licenses at cost; procurement authorization required |

---

## 5. Candidate Comparison Matrix

Pre-declared criteria only; ranking never informed by H01 v1.2 performance.

| Criterion | FRED | Nasdaq API | HPD `sp` (in-repo) | Yahoo | Stooq | CME | Euronext | Paid vendors |
|---|---|---|---|---|---|---|---|---|
| Markets (equity) | 4 US indices | NDX (+others, US) | S&P 500 futures | International breadth | International | ES futures | CAC 40 | Broad |
| Historical depth | N100 1986+; NCOM 1971+; SPX/DJI 2016+ | NDX 1996+ (early data unreliable) | 1982-2002 | GSPC/N225 1970+; FTSE 1984+; etc. | unknown | unknown (gated) | unknown (gated) | vendor-dependent |
| Daily frequency | ✓ (close) | ✓ (OHLC) | ✓ (OHLC, adj) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Integrity | PASS (spot-checks + Yahoo corroboration) | FAIL for 1996-2003; OK recent | PASS (CORE VALID; vs-cash documented) | PARTIAL (anchors authentic) | n/a | n/a | n/a | vendor-dependent |
| Futures vs cash | cash | cash | **futures** | cash | cash | futures | cash | vendor-dependent |
| Licensing (platform) | CLEAR | PENDING (provider terms) | PENDING (HPD record) | RESTRICTED | RESTRICTED | gated | gated | CLEAR (contract) |
| Licensing (archival) | PENDING (3rd-party ©) | PENDING | PENDING | RESTRICTED | RESTRICTED | gated | gated | CLEAR |
| Reproducibility | HIGH | MEDIUM (early data defect; API stability) | HIGH (in-repo) | LOW | FAIL | gated | gated | HIGH |
| **Role in composite** | **historical Nasdaq + contemporary US** | **contemporary cross-val only** | **historical broad-US** | **validation reference only** | — | — | — | **international alternative** |

---

## 6. Best Candidate Deep Review — the Composite

The leading acquisition candidate is not a single provider but the **composite** {HPD `sp` + FRED}, because no single free source satisfies both the breadth requirement and the licensing/archival requirement (§5).

### HPD `sp` (S&P 500 futures, in-repository)
- SOURCE-DERIVED FACT: front_month series, 5,163 rows, 1982-04-21 → 2002-10-01, 82 contract rolls, ratio back-adjusted (`adj_close`), continuity_ok=True, CORE VALID (frozen HPD validation).
- NEW (this session): vs cash S&P 500 (Yahoo ^GSPC), common window 1982-04-21 → 2002-10-01 (5,162 obs): **daily-return corr 0.946039; median |Δret| 16.45 bp; max |Δret| 1,080 bp on 1987-10-19; 115 dates (2.2%) with |Δret| > 1%**.
- Anomaly attribution (SOURCE-DERIVED FACT): 1987-10-19 HPD close 201.50 = the documented Dec-87 futures close vs cash 224.84 (the famous Black-Monday futures/cash divergence); 1982-09-22 is a genuine futures/cash daily divergence (not a roll day — same contract); 2000-12-11 and 1987-12-18 similar basis/roll-day effects. **No evidence of an HPD data error; the differences are real futures-vs-cash behavior.**
- MODEL INFERENCE: `sp` is a faithful broad-US equity exposure and is directly comparable at the *object* level (each market's own shocks and forward-ΔlnRV responses are internally consistent), but futures and cash daily returns are not identical (median 16 bp, crisis dislocations) — the registered comparability rule must address this before a mixed futures/cash layer is locked.

### FRED (US indices)
- SOURCE-DERIVED FACT (prior audit + this session): NASDAQ100 (10,597 rows, 1986-01-02+), NASDAQCOM (14,486 rows, 1971-02-05+), SP500/DJIA (2,610 rows, 2016-08-15+). Zero duplicates/weekends/non-positives; holiday rows are NaN placeholders; five known-value spot checks exact.
- NEW (this session): NASDAQ100 **corroborated by Yahoo** over 1996-2004 (median |Δret| 0.0003 bp; exact agreement on the disputed 1996 dates where the Nasdaq API deviates).

### Nasdaq official API (NDX)
- SOURCE-DERIVED FACT: 7,775 rows, 1996-06-06 → 2026-08-14, OHLC. **Early history unreliable**: vs FRED+Yahoo, level deviations up to 15.51% concentrated in 1996 (129 dates >1%), scattered 1997-2003, essentially exact after ~2004.
- MODEL INFERENCE: use the Nasdaq API only as a *contemporary* provider-direct cross-reference (OHLC for the recent era); **do not use it as the historical NDX source** — FRED is the corroborated source.

---

## 7. Historical Coverage

| Exposure | Series | Coverage | Window in the composite |
|---|---|---|---|
| Broad US (futures) | HPD `sp` | 1982-04-21 → 2002-10-01 | 1986 → 2002 |
| US tech (cash) | FRED NASDAQ100 | 1986-01-02 → present | 1986 → 2002 |
| US broad (cash, composite) | FRED NASDAQCOM | 1971-02-05 → present | 1986 → 2002 |

- Common historical window **1986-01 → 2002-10 (~16 years)**, spanning the 1987 crash, the 1990s bull, and the 2000-02 bear — multiple regimes (SOURCE-DERIVED FACT from coverage ranges).
- International historical coverage: **not available from any free, archiveable source** (re-verified this session). Only Yahoo (RESTRICTED) or paid vendors provide it.

---

## 8. Cross-Sectional Breadth

- **Historical: two distinct exposures** — broad US large-cap (`sp`) and US tech (NASDAQ100, NASDAQCOM). This resolves the scope decision's near-single-factor defect for the historical layer.
- **Contemporary: two distinct exposures** — broad US (SP500, DJIA) and US tech (NASDAQCOM, NASDAQ100), each pair near-duplicate within itself but distinct across the pair; `USATECHIDXUSD` (M1) adds a third-era tech observation subject to a source-comparability rule.
- MODEL INFERENCE: the composite converts the H01 two-single-market evidence into a 2-exposure × 2-era design. It does **not** constitute international breadth; the "generalizes across equity markets" claim is supportable in its US-anchored form only. International breadth is a paid/authorized option, not a free one.
- No market is included or excluded by H01 v1.2 performance; selection is by identity (flagship US index; major US index families) — the universe-construction rule for the definition lock.

---

## 9. Data Integrity / Validation

| Check | Result |
|---|---|
| FRED: dups / weekends / non-positives / >5-day gaps | 0 / 0 / 0 / 0 (4 series; prior audit) |
| FRED known-value spot checks | 5/5 exact (Composite 5048.62 on 2000-03-10; NDX max 4704.73 on 2000-03-27; Composite 360.21 on 1987-10-19; 1971 base 100.0; SP500 3386.15 on 2020-02-19) |
| FRED holiday rows | NaN placeholders (US exchange holidays) — dropped by existing missing-data rules |
| FRED NASDAQ100 vs Yahoo ^NDX (1996-2004, 1,914 common obs) | corr 0.991971; median |Δret| 0.0003 bp — **essentially identical** |
| Nasdaq API NDX vs FRED (7,597 common obs) | corr 0.973247; median |Δret| 0.0 bp but max |Δret| 638 bp; **129 dates >1% in 1996**; early data unreliable |
| HPD `sp` vs cash ^GSPC (5,162 obs, 1982-2002) | corr 0.946039; median |Δret| 16.45 bp; crisis dislocations explained (futures/cash basis) — `sp` faithful, futures ≠ cash at return level |
| Nasdaq API NDX schema | OHLC + close, `MM/DD/YYYY`, strings with commas — parse transform required (documented for ingestion) |

---

## 10. Cross-Source Verification

Per task §8, the leading candidate was cross-validated against independent sources (read-only, bounded; the comparison sources are not part of the dataset):

1. **FRED NASDAQ100 vs Yahoo ^NDX** (same cash index): agreement essentially exact (median |Δret| 0.0003 bp over 1996-2004; exact values on the 1996-07/10/12 disputed dates: 606.89 / 775.08 / 844.63 — FRED matches Yahoo; the Nasdaq API does not). → **FRED NDX verified.**
2. **FRED NASDAQ100 vs Nasdaq official API NDX**: deviations concentrated in the API's early history (up to 15.5%, 1996-2003). → **Nasdaq API early data flagged; use FRED.**
3. **HPD `sp` vs cash ^GSPC** (futures vs cash, different instruments — comparability check, not fidelity): documented in §6/§9; confirms `sp` is genuine S&P 500 exposure with expected futures/cash differences.

Discrepancies are explainable by methodology (futures basis/rolls; provider vintage) — no unexplained data corruption found.

---

## 11. Licensing / Archival Rights

Statuses use the task's scale: CLEAR / PENDING / RESTRICTED / UNKNOWN / DENIED. **Nothing is classified CLEAR without evidence; no permission is claimed as received.**

| Component | Provider / series | Platform | Archival status | Permission requirement |
|---|---|---|---|---|
| HPD `sp` | TurtleTrader-sourced S&P futures (frozen HPD record) | n/a | **PENDING** (standing HPD record) | Already documented at HPD acquisition; local research use per repo precedent |
| FRED SP500, DJIA | © S&P Dow Jones Indices via FRED | CLEAR (free; attribution) | **PENDING** | Written permission from S&P DJI for archival/redistribution beyond personal research use |
| FRED NASDAQCOM, NASDAQ100 | © Nasdaq via FRED | CLEAR (free; attribution) | **PENDING** | Written permission from Nasdaq for archival/redistribution beyond personal research use |
| Nasdaq API NDX | Nasdaq (provider-direct) | PENDING (site terms) | **PENDING** | Permission from Nasdaq for archival; contemporaneous use only |
| Yahoo (validation only) | Yahoo Finance | RESTRICTED | **RESTRICTED** | ToS prohibit redistribution/automated archival; used only for one-off read-only validation |
| Stooq | Stooq | RESTRICTED | **RESTRICTED** | "personal use only; commercial use prohibited"; access blocked |
| CME / Euronext | Exchange | gated | gated | Registration/login; not assessed further this session |
| Norgate / CSI / Databento | Commercial | CLEAR (under contract) | CLEAR (contractual) | Procurement authorization required; nothing purchased |

**Prepared permission requests (required; NOT sent — operator dispatch required):**
- **To S&P Dow Jones Indices** (index_services@spdji.com): request a non-commercial research archival/redistribution license for daily S&P 500 and Dow Jones Industrial Average index levels, describing use (daily closes for registered volatility-response research, in-repository archival, no redistribution, no commercial use, attribution preserved).
- **To Nasdaq Global Indexes / Nasdaq data licensing** (via nasdaq.com contact/licensing): request a non-commercial research archival license for Nasdaq-100 and Nasdaq Composite daily index levels, same use description.
- Each request must state the research program (QuantForge H01 equity replication), the exact series and date ranges, the local-only archival intent, and the attribution commitment. Until responses are received, all components remain **PENDING** — the repository's established posture for the HPD data itself.

**GOVERNANCE DECISION:** the licensing path is *resolved* as PENDING-with-documented-requirements (consistent with the HPD precedent that the repository already operates under). If the operator requires CLEAR status before the definition lock, the paid-vendor path (Norgate — strongest fit for daily index history with research licenses; CSI; Databento) is the alternative and requires a separate procurement authorization.

---

## 12. Reproducibility

Retrieval date: 2026-08-16. Samples reside in the external temporary directory (outside the repository); fingerprints recorded for provenance. No raw data was placed in the repository.

| Source | URL / recipe | Files (external temp) | SHA-256 (first 16) | Rows | Range |
|---|---|---|---|---|---|
| FRED SP500 | fredgraph.csv?id=SP500 | fred_SP500.csv | 351555b5556f3437 | 2,610 | 2016-08-15 → 2026-08-14 |
| FRED DJIA | fredgraph.csv?id=DJIA | fred_DJIA.csv | 29c8ca59469de81b | 2,610 | 2016-08-15 → 2026-08-14 |
| FRED NASDAQCOM | fredgraph.csv?id=NASDAQCOM | fred_NASDAQCOM.csv | 51187aa6f103f27d | 14,486 | 1971-02-05 → 2026-08-14 |
| FRED NASDAQ100 | fredgraph.csv?id=NASDAQ100 | fred_NASDAQ100.csv | aeacca4f6472dd56 | 10,597 | 1986-01-02 → 2026-08-14 |
| Nasdaq API NDX | api.nasdaq.com/api/quote/NDX/historical?assetclass=index&fromdate=1996-01-01&todate=2026-08-14&limit=99999 | nasdaq_ndx_full.json | 6f2a9cf7586389bd | 7,775 | 1996-06-06 → 2026-08-14 |
| Nasdaq API NDX (window) | same with fromdate=2024-01-01 | nasdaq_ndx_hist.json | db77ab8707a27fc1 | 657 | 2024 → 2026-08-14 |
| Yahoo ^GSPC (validation) | chart API period1=epoch(1982-04-20)&period2=epoch(2002-10-03) | in-memory | — | 5,167 | 1982-04-19 → 2002-10-02 |
| Yahoo ^NDX (validation) | chart API period1=epoch(1995-12-01)&period2=epoch(2004-01-15) | in-memory | — | 2,045 | 1995-11-30 → 2004-01-14 |
| HPD `sp` (in-repo) | frozen `front_sp.csv` | in-repo (frozen) | per HPD manifest | 5,163 | 1982-04-21 → 2002-10-01 |

Transformation notes: FRED holiday rows are NaN placeholders (drop); Nasdaq API values are comma-formatted strings (parse); Yahoo daily timestamps carry session time (normalize to date); HPD `sp` uses `adj_close` (ratio back-adjusted front-month). Reacquisition is deterministic for FRED; the Nasdaq API and Yahoo endpoints are undocumented and may change.

---

## 13. Decision Gates

| Gate | Composite {HPD `sp` + FRED} | Notes |
|---|---|---|
| **G1 Breadth** | **PASS (US scope)** | 2 distinct exposures per era; international = FAIL (no free archiveable source) |
| **G2 Historical depth** | **PASS** | sp 1982-2002; N100/NCOM 1986/1971+; common 1986-2002, multi-regime |
| **G3 Price integrity** | **PASS** | FRED spot-checked + Yahoo-corroborated; `sp` CORE VALID, futures-vs-cash behavior documented; Nasdaq API early data excluded from the historical role |
| **G4 Comparability** | **CONDITIONAL PASS** | Object applies identically to every series; futures/cash return differences documented (corr 0.946, median 16 bp, crisis dislocations) → the registered futures/cash comparability rule is a definition-lock item, now evidence-based |
| **G5 Licensing** | **PASS (as PENDING)** | All components PENDING with documented permission requirements; requests prepared (unsent); consistent with HPD precedent; CLEAR alternative = paid path |
| **G6 Reproducibility** | **PASS** | HPD in-repo (frozen); FRED deterministic; reacquisition recipes recorded |
| **G7 Cross-source verification** | **PASS** | FRED NDX vs Yahoo exact; Nasdaq API early-data defect identified; `sp` vs cash documented |

**Gate summary:** the composite passes all seven gates — G1 for the US scope, G4 conditional on the definition-lock comparability rule, G5 as PENDING (not CLEAR). The only gate that fails absolutely is **international breadth** (G1 international reading), which is out of scope for free sources.

---

## 14. Governance Decision

**A — EQUITY DATASET READY FOR DEFINITION LOCK** (US-anchored scope).

**GOVERNANCE DECISION, stated precisely:**
1. The assembled universe — historical {`sp`, NASDAQ100, NASDAQCOM}, contemporary {SP500, DJIA, NASDAQCOM, NASDAQ100} (± `USATECHIDXUSD` under a source-comparability rule) — is scientifically defensible for the US-anchored two-exposure claim, reproducible, and licensing-documented (PENDING per repo precedent). It is **ready to enter the definition-lock process**.
2. **The international variant is NOT covered by this decision.** No free, archiveable source provides international breadth (re-verified this session). Achieving it requires either a **separately authorized paid acquisition** (Norgate/CSI/Databento) or an explicit scope revision. This is recorded, not assumed.
3. The near-single-factor defect that motivated the scope decision's "broader data required" is resolved for the US-anchored claim by the composite (2 distinct exposures historically). If the operator instead confirms the international claim is mandatory, the paid path must be authorized before the definition lock.

---

## 15. Exact Next Legitimate Task

**H01-EQUITY SCIENTIFIC DEFINITION LOCK**, whose first acts must be:

1. **Scope confirmation (governance):** the operator accepts the US-anchored two-exposure universe as assembled — or authorizes the paid international path first. (Neither is assumed here.)
2. **Register the futures/cash comparability rule**, using the evidence recorded in §6/§9 (HPD `sp` futures vs FRED cash: corr 0.946, median 16 bp daily, crisis dislocations) — deciding, outcome-blind, whether a mixed futures/cash layer is permitted and under what construction.
3. **Fix the breadth target and the market list** outcome-blind (markets by identity, never by H01 v1.2 performance), consistent with the ≥2-market evaluability floor and the 2-exposure-per-era requirement.
4. **Record the licensing posture** — PENDING for all components with attribution, permission requests dispatched by the operator (or the paid path authorized).

No protocol and no definition lock is written now.

---

## 16. Prohibited Follow-Up

Selecting markets from H01 v1.2 performance; dropping weak markets; market-count tuning; horizon changes; GJR/EGARCH as primary; K-means/ML; trading-signal use; Track-A/TSMOM merge; re-opening commodities; re-admitting quarantined HPD roots (aor/cac) without a separate provenance governance decision; using the Nasdaq API's early history (1996-2003) as a historical source; mixing FRED + HPD + MT5 without the registered comparability rule; claiming international generalization from the US-anchored composite; claiming CLEAR licensing where PENDING; claiming permission received where none was sent; placing raw external data in the repository before the approved ingestion stage; writing the definition lock or any protocol now.

---

## 17. Integrity

- The repository was modified in exactly one way: the required artifact `output/research_discovery/H01_EQUITY_DATA_ACQUISITION_V1.md`.
- Bounded verification samples (FRED ×4, Nasdaq API ×2, Yahoo in-memory only) were downloaded to the external temporary directory `C:/Users/User10/AppData/Local/Temp/quantforge_eqsrc_audit/` — outside the repository — with SHA-256 fingerprints recorded (§12). No raw data was placed in the repository; the samples are verification-only and will be re-acquired/re-verified at the approved ingestion stage.
- **No H01 statistic was computed.** All this-session computations were source-fidelity and comparability validations explicitly requested by this task's §8: same-index return agreement (FRED vs Yahoo vs Nasdaq API for NDX) and futures-vs-cash comparability (HPD `sp` vs ^GSPC). No shock, RV, matching, asymmetry, bootstrap, or p-value was calculated; no market, horizon, parameter, or threshold was selected; no prior or class was altered.
- Yahoo was used only for one-off read-only validation (the repository's established cross-validation pattern — HPD used stooq the same way); it is not part of the dataset and nothing from it is archived.
- The frozen H01 v1.2 protocol and artifacts, BOE/Assembly/Deployment, and all governance records are untouched.
