# QUANTFORGE — H01 EQUITY V1

# DEFINITION-LOCK AMENDMENT PROPOSAL: NYA SOURCE GOVERNANCE

**Amendment type:** Source-governance exception for Yahoo Finance NYA
**Date:** 2026-08-23
**Status:** PROPOSAL — NOT YET APPROVED
**Governing artifact:** `H01_EQUITY_VOLATILITY_ASYMMETRY_DEFINITION_LOCK_V1.md`

---

## 1. Purpose

This amendment proposes a narrowly scoped exception to the existing Yahoo Finance source exclusion (definition lock §18) to permit the existing Yahoo `^NYA` (NYSE Composite Index) daily Close dataset as a primary research source for the H01 Equity V1 experiment.

The amendment does NOT:
- Remove the general Yahoo exclusion
- Permit Yahoo as a primary source for any other market
- Change the scientific hypothesis
- Change any statistical method
- Change any market-selection rule

---

## 2. Existing Rule

Definition lock §18 currently states:

> | Nasdaq API, Yahoo, Stooq | NOT in the primary universe; Yahoo/Nasdaq-API used only for validation; nothing archived from them |

This excludes Yahoo as a primary source for any market in the H01 universe.

---

## 3. Proposed Exception

Add the following exception to §18:

> **Exception — NYSE Composite (`NYA`):** The existing Yahoo Finance `^NYA` daily Close dataset is approved as a primary source for NYA, subject to the following conditions:
>
> 1. The source artifact is the immutable local file `docs/NYA_DATA.html` (SHA-256: `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f`)
> 2. Only the `Close` field is used (price-type index level)
> 3. The dataset has been independently validated against FRED quarterly NYSE Composite observations (80 quarter-end dates; 76 exact matches; maximum discrepancy 0.51%)
> 4. This exception applies only to NYA and does not extend to any other Yahoo-sourced market

---

## 4. NYA Identity

| Property | Value |
|---|---|
| **Index name** | NYSE Composite Index |
| **Ticker** | `^NYA` (Yahoo) / `$NYA` (Norgate) |
| **Index provider** | ICE Data Services (formerly NYSE) |
| **Constituents** | All common stocks listed on NYSE (~2,000 names) |
| **Construction** | Market-cap-weighted |
| **Price type** | Price-type index level (not total-return) |
| **Base date** | December 31, 1965 = 50.00 |
| **Historical availability** | November 30, 1984 (official NYSE); 1982-04-21 (Yahoo reconstructed) |

---

## 5. Yahoo Source

| Property | Value |
|---|---|
| **Source** | Yahoo Finance historical data page |
| **Ticker** | `^NYA` |
| **File path** | `docs/NYA_DATA.html` |
| **File size** | 1,399,864 bytes (1,367.1 KB) |
| **SHA-256** | `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f` |
| **Git tracked** | NO (untracked) |
| **Row count** | 5,163 |
| **Date range** | 1982-04-21 → 2002-09-30 |
| **Fields** | Date, Open, High, Low, Close, Adj Close, Volume |
| **Close = Adj Close** | Yes (100% identical) |
| **OHLC = Close** | Yes (100% — known Yahoo limitation for index data) |

---

## 6. Close Field

The `Close` field is the correct candidate field:
- Price-type index level (not total-return)
- Split-adjusted (consistent with H01 price-type requirement)
- No dividend adjustments (unlike `Adj Close`)
- H01 requires daily close-to-close log returns; `Close` provides exactly this

---

## 7. Historical Coverage

| Metric | Value |
|---|---|
| **Earliest date** | 1982-04-21 |
| **Latest date** | 2002-09-30 |
| **H01 historical window** | 1982-04-21 → 2002-10-01 |
| **Coverage** | Full H01 window except final day (2002-10-01) |
| **1-day gap** | 2002-09-30 → 2002-10-01 (handled by missing-day policy) |

---

## 8. SHA/Provenance Requirements

The following provenance controls are required:

1. **Immutable artifact:** `docs/NYA_DATA.html` must remain unchanged
2. **SHA-256 fingerprint:** `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f`
3. **Raw source preservation:** The HTML file must be preserved as downloaded
4. **Provenance record:** This amendment document serves as the provenance record
5. **Field selection:** Only `Close` is used; `Adj Close`, `Open`, `High`, `Low`, `Volume` are ignored

---

## 9. FRED Bounded Validation

### Independent Validation Source

| Property | Value |
|---|---|
| **Source** | FRED (Federal Reserve Economic Data) |
| **Series** | BOGZ1FL073164003Q — NYSE Composite Index, Level |
| **Provider** | Board of Governors of the Federal Reserve System |
| **Frequency** | Quarterly, End of Period |
| **Coverage** | 1945-10-01 to 2026-01-01 |

### Validation Results

| Metric | Value |
|---|---|
| **Quarter-end dates compared** | 80 |
| **Exact matches** | 76 (95.0%) |
| **Minor discrepancies** | 4 (5.0%) |
| **Maximum discrepancy** | 0.51% (1984-12-31) |
| **Average discrepancy (mismatches)** | 0.31% |
| **Material contradictions** | 0 |

### Validation Scope

> Independent validation is **bounded, not full daily-series validation**. FRED provides quarterly observations, not daily. The 76/80 exact match rate establishes high-confidence fidelity for the NYA series across the 1982-2002 historical window, but does not independently verify every daily observation.

---

## 10. Licensing Status

| Component | Status |
|---|---|
| **Yahoo Finance data access** | CLEAR (freely accessible historical data page) |
| **Yahoo Finance archival rights** | **PENDING** (Terms of Service permit personal/non-commercial use; archival persistence in repository requires owner acceptance) |
| **FRED validation source** | CLEAR (public Federal Reserve data; attribution required) |

**Licensing requirement:** Owner must explicitly accept the Yahoo-sourced NYA dataset for internal research use, acknowledging that:
- Yahoo Terms of Service govern data use
- The dataset is used for internal research only
- No republication or commercial distribution is authorized
- The FRED validation source is public and unconditionally usable

---

## 11. Reproducibility Requirements

The NYA dataset must be reproducible via:

1. **Frozen artifact:** `docs/NYA_DATA.html` with recorded SHA-256
2. **Source verification:** Yahoo Finance `^NYA` historical data page (URL may change)
3. **Independent validation:** FRED quarterly observations (publicly accessible)
4. **Extraction method:** HTML table parsing (deterministic)

---

## 12. Scientific Invariants

This amendment does NOT change:

- The scientific hypothesis (§2)
- The equity prior (§3)
- The geographic/asset-class scope (§4)
- The structural candidate evaluation criteria (§5)
- The futures/cash comparability rule (§6)
- The Nasdaq family exposure accounting (§7)
- The USATECHIDXUSD exclusion (§8)
- The shock definition (§9)
- The equal-magnitude concept (§10)
- The volatility response concept (§11)
- The horizon decision (§12)
- The volatility-state conditioning (§13)
- The cross-market aggregation (§14)
- The generalization claim (§15)
- The falsification concept (§16)
- The independence firewall (§17)

---

## 13. Explicit Non-Changes

This amendment does NOT:

- Remove the general Yahoo exclusion for other markets
- Permit Yahoo as a primary source for any market other than NYA
- Change any market-selection rule
- Change any eligibility criterion
- Change any statistical method
- Change any threshold
- Change any inference procedure
- Create a new research line
- Authorize execution

---

## 14. Governance Approval Required

This amendment requires:

1. **Independent audit** of the proposal
2. **Owner approval** of the source exception
3. **Definition lock update** (if approved)
4. **Protocol amendment** (Amendment B)
5. **Protocol audit** (after Amendment B)
6. **Owner approval** of the amended protocol
7. **Execution authorization** (separate from amendment approval)

---

## 15. Execution Remains Prohibited

> **NO H01 EXECUTION IS AUTHORIZED BY THIS PROPOSAL.**

This proposal prepares the governance documentation only. Execution requires:
- Approved definition lock amendment
- Approved protocol amendment
- Fresh independent implementation audit
- Explicit execution authorization

---

## 16. Integrity

- This is a governance amendment proposal only
- No H01 statistic has been computed
- No experiment has been run
- No data has been acquired
- No protocol has been modified
- No definition lock has been modified
- No session handoff has been updated
- No commit has been made
