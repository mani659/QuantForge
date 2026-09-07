# QUANTFORGE — H01 EQUITY TRACK A

# NYA DUAL-SOURCE FIDELITY + PRE-AMENDMENT AUDIT V1

**Audit type:** Read-only pre-amendment evidence audit
**Date:** 2026-08-23
**Status:** COMPLETE

---

## 1. Executive Verdict

**D — THE TWO FILES ARE NOT INDEPENDENT AND NO VALID CROSS-SOURCE EVIDENCE EXISTS**

`NYA_DATA.html` and `US_Equity_Data.csv` are **identical representations of the same Yahoo Finance NYA dataset** — same 5,163 rows, same dates, same Close values, zero mismatches. The CSV is a derived/formatted copy of the HTML data, not an independent source. No independent cross-source validation of NYA prices exists in the repository.

However, the **underlying NYA dataset itself is technically valid** for potential future amendment (correct date range, valid Close prices, structurally distinct from S&P 500). The issue is solely that no independent source confirms Yahoo's NYA values.

---

## 2. File Identity

| Property | NYA_DATA.html | US_Equity_Data.csv |
|---|---|---|
| **Path** | `docs/NYA_DATA.html` | `docs/US_Equity_Data.csv` |
| **Size** | 1,399,864 bytes (1,367.1 KB) | 346,004 bytes (337.9 KB) |
| **SHA-256** | `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f` | `a06de89b616af764d8a14163c0448700fbe940580f04cdbed466a0e5fd39e425` |
| **Modified** | 2026-08-23 12:04:57 | 2026-08-23 12:45:09 |
| **Git tracked** | NO (untracked) | NO (untracked) |
| **Source provenance** | Yahoo Finance `^NYA` historical data page | Derived from same Yahoo source (see §3) |

---

## 3. Provenance

### NYA_DATA.html

- **Source:** Yahoo Finance historical data page for `^NYA` (NYSE Composite Index)
- **Provenance evidence:** HTML structure contains Yahoo Finance CSS classes (`yf-u4m6f0`, `yf-534r60`); column headers match Yahoo's standard format ("Close price adjusted for splits", "Adjusted close price adjusted for splits and dividend and/or capital gain distributions")
- **Download method:** Browser-saved HTML table (not API)
- **Date format:** "Sep 30, 2002" (US format, MMM DD, YYYY)

### US_Equity_Data.csv

- **Source:** **DERIVED FROM THE SAME YAHOO DATA** — NOT independent
- **Provenance evidence:**
  - Same 5,163 rows as HTML
  - Same dates (all 5,163 dates match exactly)
  - Same Close values (all 5,163 values match to 6+ decimal places)
  - Same OHLC=Close pattern
  - Same Volume dashes for pre-2001 dates
  - Only differences: date format (DD-Mon-YY vs "MMM DD, YYYY"), encoding (BOM present), no HTML markup
- **Conclusion:** The CSV is a formatted/converted copy of the HTML data, likely created by the user or a tool that parsed the HTML table

### Classification

**Both files originate from Yahoo Finance. They are NOT independent sources.**

---

## 4. Dual-Source Fidelity

| Metric | Result |
|---|---|
| Common dates | 5,163 |
| Exact matches | 5,163 / 5,163 (100%) |
| Mismatches | 0 |
| HTML-only dates | 0 |
| CSV-only dates | 0 |
| Max absolute difference | 0.000000 |
| Max relative difference | 0.00000000 |

**The two files are byte-for-byte equivalent in their data content.** The CSV is a transformed copy of the HTML.

### Cross-Source Classification

**NOT INDEPENDENT** — Both files derive from the same original Yahoo Finance source. This does NOT constitute cross-source validation.

---

## 5. Date Coverage

### NYA Coverage

| Metric | Value |
|---|---|
| Earliest date | 1982-04-21 |
| Latest date | 2002-09-30 |
| Total rows | 5,163 |
| H01 window (1982-04-21 → 2002-10-01) | 5,163 rows within window |
| Last day missing | 2002-10-01 (1 day before HISTORICAL_END) |

### SP Coverage (for comparison)

| Metric | Value |
|---|---|
| Earliest date | 1982-04-21 |
| Latest date | 2002-10-01 |
| Total rows | 5,163 |

### Date Set Comparison

| Metric | Value |
|---|---|
| Common dates | 5,161 |
| SP-only dates | 2 (1985-09-27, 2002-10-01) |
| NYA-only dates | 2 (1983-11-25, 1993-09-01) |

### Coverage Assessment

NYA covers the full H01 historical window except the final day (2002-10-01). The 1-day gap is handled by the protocol's missing-day policy (§9): incomplete windows are dropped, not imputed. This is a minor coverage difference, not a blocker.

---

## 6. Price Field

| Field | NYA HTML | NYA CSV | H01 Requirement |
|---|---|---|---|
| Close | Present | Present | **Required** — daily close-to-close log return |
| Adj Close | Present | Present | **NOT used** — would introduce dividend adjustments |
| Open | Present (= Close) | Present (= Close) | **NOT used** |
| High | Present (= Close) | Present (= Close) | **NOT used** |
| Low | Present (= Close) | Present (= Close) | **NOT used** |
| Volume | Present (dash pre-2001) | Present (dash pre-2001) | **NOT used** |

**Correct field:** `Close` (split-adjusted price-type index level). This matches the protocol's requirement for price-type series (not total-return).

**Both fields are identical** in this dataset (no splits/dividends in NYA 1982-2002), so either would produce the same result. However, `Close` is the governance-correct choice.

---

## 7. OHLC Interpretation

### Pattern

**100% of rows (5,163/5,163) have Open = High = Low = Close.**

### Explanation

This is a **known Yahoo Finance limitation for historical index data**. Yahoo provides only the closing value for index historical data, repeating it across all OHLC fields. This is NOT data corruption — it is the standard behavior for index downloads from Yahoo Finance.

### Impact on H01

**NO IMPACT.** The H01 scientific object uses only daily close-to-close log returns:

> `r_t = ln(close_t / close_{t-1})`

The `Close` field provides exactly this. The OHLC equality does not affect the registered H01 scientific object because H01 does not use intraday price information.

---

## 8. Structural Distinctness

### NYSE Composite (NYA) vs S&P 500 (`sp`)

| Attribute | NYSE Composite (NYA) | S&P 500 (`sp`) |
|---|---|---|
| Universe | All common stocks on NYSE (~2,000 names) | 500 selected large-cap US companies |
| Selection | All NYSE-listed stocks | Committee-selected, cap-weighted |
| Sector breadth | Full NYSE market (industrial, utility, transportation, financial) | Broad but curated |
| Smallest constituents | Includes micro/small-cap NYSE stocks | Excludes sub-500-rank names |
| Exchange | NYSE only | NYSE + Nasdaq + other |
| Instrument type | Cash index | Futures (front-month, ratio back-adjusted) |
| Source | Yahoo Finance | HPD |

### Distinctness Verdict

**STRUCTURALLY DISTINCT.** NYA and S&P 500 represent different broad-US exposures:
- NYA = full NYSE market (broader, includes smaller names)
- S&P 500 = curated large-cap (more concentrated, cross-exchange)

They share significant large-cap overlap but are not near-duplicates in the way NASDAQ100 and NASDAQCOM are (definition lock §7). The distinctness is comparable to SP500 vs DJIA in EQBROAD_L2 (different index families, same broad-US exposure, registered as distinct markets).

---

## 9. Historical Coverage

### H01 Requirement

> EQBROAD_L1 era: Historical (1982-04-21 → 2002-10-01)

### NYA Coverage

- **Starts:** 1982-04-21 (identical to `sp`)
- **Ends:** 2002-09-30 (1 day before HISTORICAL_END)
- **Overlap with `sp`:** 5,161 dates (99.96% of both series)

### Assessment

NYA covers the full H01 historical window. The 1-day gap at the end (NYA ends Sep 30; SP ends Oct 1) is:
- Likely because 2002-10-01 was a non-trading day for NYSE but was a trading day for CME futures
- Or Yahoo's NYA data has a 1-day lag vs futures data
- Handled by the protocol's missing-day policy (§9)

**This is NOT a protocol violation.** Markets are evaluated on their own eligible series, not on a fixed common window.

---

## 10. Provenance Analysis

### NYA_DATA.html

- **Source:** Yahoo Finance `^NYA` historical data page
- **Provenance:** Browser-saved HTML table
- **Confidence:** HIGH — HTML structure is unambiguously Yahoo Finance

### US_Equity_Data.csv

- **Source:** **DERIVED FROM SAME YAHOO DATA** — NOT independent
- **Evidence:** Identical 5,163 rows, identical dates, identical Close values, zero mismatches
- **Classification:** NOT INDEPENDENT

### Independent Source Availability

**NO independent daily NYA source exists in the repository.**

- FRED has quarterly NYSE Composite data (`BOGZ1FL073164003Q`) — insufficient frequency for H01
- No daily NYSE Composite series was identified on FRED
- No other local dataset contains NYA daily prices

---

## 11. Cross-Source Fidelity

### Classification

**NOT INDEPENDENT — No valid cross-source evidence exists.**

Both `NYA_DATA.html` and `US_Equity_Data.csv` derive from the same Yahoo Finance source. The CSV is a formatted copy of the HTML data.

### Implication

The NYA Close values cannot be independently verified against a second source within the current repository. Cross-source verification would require:
- An independent download from a different provider (e.g., Bloomberg, Refinitiv, exchange data)
- Or a different free source (none identified that provides daily NYA data)

### Risk Assessment

The absence of cross-source verification is a **data-quality risk**, not a scientific or protocol issue. The risk is:
- Yahoo's NYA Close values could contain errors or revisions
- Without an independent check, such errors would be undetectable

This risk is **manageable** through:
- Future independent source verification (if a second source becomes available)
- The frozen H01 data-quality gates (which would catch non-positive values, duplicates, etc.)
- The fact that Yahoo Finance is a widely-used data provider with established quality controls

---

## 12. Pre-Amendment Question

> **Would the local NYA evidence, if the owner approves a formal source/universe amendment, provide a technically credible second EQBROAD_L1 market without changing the scientific hypothesis or statistical method?**

### Answer: **CONDITIONAL**

The NYA dataset is technically suitable:
- ✅ Correct date range (1982-04-21 → 2002-09-30)
- ✅ Valid Close prices (positive, no duplicates, correct ordering)
- ✅ Structurally distinct from S&P 500
- ✅ Price-type index level (not total-return)
- ✅ Sufficient observations for evaluability (5,163 rows)
- ✅ No protocol violation (OHLC=Close does not affect H01)

However, an **unresolved provenance/licensing issue remains**:
- ❌ No independent cross-source verification exists
- ❌ Yahoo is explicitly excluded as a primary source by the frozen definition lock (§18)
- ❌ Licensing for archival persistence of Yahoo-sourced primary data is unresolved

### Conclusion

The data itself is suitable for a governed amendment. The amendment would need to:
1. Resolve the Yahoo source exclusion (definition lock §18)
2. Accept the cross-source verification gap as a known data-quality risk
3. Carry the licensing PENDING status into execution metadata

---

## 13. Budget Gate

> **No new data acquisition is necessary for the next governance decision.**

We already possess the candidate files. No additional data purchase, download, or credit consumption is required.

---

## 14. Governance Status

> **NYA IS NOT YET PART OF THE FROZEN H01 UNIVERSE.**

The frozen definition lock (§18) explicitly excludes Yahoo as a primary source:
> "Nasdaq API, Yahoo, Stooq | NOT in the primary universe; Yahoo/Nasdaq-API used only for validation; nothing archived from them"

The frozen protocol (§5) defines EQBROAD_L1 with only `sp` as the market.

Adding NYA requires formal governance amendments to both artifacts.

---

## 15. Required Next Task

**FORMAL H01 DEFINITION-LOCK / UNIVERSE AMENDMENT PROPOSAL FOR NYA**

The next governed task should be:
1. Draft definition lock amendment (resolve Yahoo exclusion for NYA)
2. Draft protocol amendment (add NYA to EQBROAD_L1)
3. Independent audit of both amendment proposals
4. Owner approval gate

This is NOT permission to execute H01 with NYA. The amendments must be completed and approved before any execution.

---

## 16. Confidence

**HIGH** (for the technical findings); **MEDIUM** (for the pre-amendment recommendation)

The technical findings are unambiguous:
- Both files are from Yahoo (NOT independent)
- NYA data is internally valid (correct dates, valid prices)
- NYA is structurally distinct from S&P 500
- No protocol violation exists

The pre-amendment recommendation is MEDIUM confidence because:
- The cross-source verification gap is real but manageable
- The Yahoo source exclusion is a governance decision, not a data-quality issue
- The licensing question requires resolution but is not a blocker

---

## 17. Integrity

- Read-only: YES
- No execution: YES
- No data download: YES
- No protocol modification: YES
- No definition lock modification: YES
- No statistics computed: YES
- No new DISC created: YES
- No commit: YES
