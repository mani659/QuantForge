# QUANTFORGE — NORGATE TRIAL TECHNICAL EXTRACTION & SOURCE VALIDATION V2

## 1. Executive Verdict
**B — TECHNICALLY VERIFIED BUT LICENSING STILL PENDING**

The Norgate Data Updater and Python API were successfully verified using the US Stocks Platinum 3-week free trial. The required object (NYSE Composite daily OHLC) is correctly delivered, mathematically sound, and exhibits strong cross-source fidelity. However, the trial is software-limited to two years of history, and explicit written permission for permanent research-repository archival remains pending. No H01 scientific statistic was computed and no market was added to the frozen protocol.

## 2. NDU & API Verification
**SOURCE-DERIVED FACT:**
- **NDU Installation:** Norgate Data Updater is installed and running locally with an active Platinum trial.
- **Python API Version:** `norgatedata` v1.0.77.
- **Connection:** The Python API successfully connected to the local NDU service.

## 3. NYSE Composite Verification
**SOURCE-DERIVED FACT:**
- **Exact Symbol:** `$NYA`
- **Asset Name:** NYSE Composite Index
- **Base Type:** Stock Market
- **Format:** Daily OHLC (Price-type cash index).
- **Trial Availability:** 2024-08-19 to 2026-08-14.

## 4. Russell 2000 Verification
**SOURCE-DERIVED FACT:**
- **Exact Symbol:** `$RUT`
- **Asset Name:** Russell 2000 Index
- **Base Type:** Stock Market
- **Format:** Daily OHLC (Price-type cash index).
- **Trial Availability:** 2024-08-19 to 2026-08-14.

## 5. Trial-History Limits & Diamond Depth
**SOURCE-DERIVED FACT / GOVERNANCE DECISION:**
- **Trial Limits:** The Platinum trial is strictly software-limited. The earliest date returned by the API is 2024-08-19. Deep history is inaccessible via the trial.
- **Diamond Depth Verification:** As established in V1 via authoritative Norgate documentation, the paid Diamond package provides NYSE Composite history starting December 31, 1965 (sufficient for the 1982-2002 era), but Russell 2000 history only starts December 24, 1996 (insufficient). **The Russell 2000 is formally rejected for closing the deep historical gap.**

## 6. Trial Data Integrity
**SOURCE-DERIVED FACT:**
Data extracted for `$NYA` from 2024-08-19 to 2026-08-14:
- **Row count:** 499
- **Columns:** Open, High, Low, Close, Volume, Turnover
- **Duplicate timestamps:** 0
- **Weekend rows:** 0
- **Missing dates:** 21 (Consistent with ~10 US market holidays per year over a 2-year period).
- **Non-positive values:** 0
- **Malformed rows:** 0
- **Integrity:** HIGH. The data is clean, continuous business days.

## 7. Cross-Source Validation
**SOURCE-DERIVED FACT:**
Bounded comparison of `$NYA` against Yahoo Finance (`^NYA`) for the exact trial window:
- **First Date (2024-08-19):** Norgate Close: 18882.04 | Yahoo Close: 18882.04
- **Last Date (2026-08-14):** Norgate Close: 24821.68 | Yahoo Close: 24821.68
- **Fidelity:** Exact matches on the anchor dates. Across all 499 overlapping dates, the mean absolute close difference is 0.0438. This marginal discrepancy is expected due to minor provider index revisions or timestamp reporting conventions, demonstrating extremely strong source-level agreement.

## 8. Licensing
**GOVERNANCE DECISION:**
- **Personal/Local Research Use:** CLEAR.
- **API Use / CSV Export:** CLEAR.
- **Permanent Archival:** **PENDING**. While the trial operates correctly and extraction is permitted, the EULA is silent on permanent repository storage (like the frozen H01 artifacts). Explicit written permission must be secured before committing Diamond data to the permanent archive.

## 9. Reproducibility
**SOURCE-DERIVED FACT:**
- **Method:** `norgatedata.price_timeseries()` function returning a pandas DataFrame, which is natively exported to CSV.
- **Determinism:** High. The extraction can be repeated deterministically.
- **Fingerprinting:** The trial CSV was exported and successfully SHA-256 hashed (`aeb80bef27d5ab00dce9267abbad549ab4d8f1a50c648a0e80f06d39189134ba`).

## 10. Decision Gates
**GOVERNANCE DECISION:**
- **G1 (Product availability):** PASS.
- **G2 (Broad-US identity):** PASS (NYSE Composite).
- **G3 (Exposure distinctness):** PASS (NYSE Composite vs S&P 500).
- **G4 (Historical overlap):** PASS for NYSE Composite (1965+ via Diamond).
- **G5 (Trial Data Integrity):** PASS.
- **G6 (Reproducibility):** PASS.
- **G7 (Licensing):** PENDING (Permanent archival).
- **G8 (Extraction feasibility):** PASS.

## 11. Governance Decision
**B — TECHNICALLY VERIFIED BUT LICENSING/DEPTH STILL PENDING**
(The workflow, integrity, and cross-source fidelity are technically verified. Diamond depth is verified via documentation. Formal archival licensing is pending.)

## 12. Exact Next Legitimate Task
> **PROCURE NORGATE US STOCKS DIAMOND AND OBTAIN ARCHIVAL CLARIFICATION**

The operator is authorized to procure the full Diamond package and formally clarify archival rights to complete the source acquisition.

## 13. Integrity
- No H01 scientific statistic was computed and no market was added to the frozen protocol.
- Extraction was bounded strictly to the trial window.
- Yahoo data was used solely for diagnostic source-fidelity checking and was not stored.
- All temporary CSV extractions were saved to a scratch directory outside the repository core.
