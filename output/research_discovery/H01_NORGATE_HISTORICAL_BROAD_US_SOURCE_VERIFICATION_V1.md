# QUANTFORGE — NORGATE HISTORICAL BROAD-US EQUITY SOURCE VERIFICATION V1

## 1. Executive Verdict
**B — SOURCE PROMISING BUT MORE DUE DILIGENCE REQUIRED**

The provider (Norgate Data) offers the correct structural exposures (Russell 2000 and NYSE Composite) with appropriate frequency (daily OHLC) and delivery mechanisms (Python API). However, data integrity and cross-source validation gates cannot be cleared until the operator explicitly authorizes a subscription purchase to obtain the necessary sample data. Archival rights remain PENDING explicit written clarification. No H01 statistics were computed, and no market was added.

## 2. Product / Package Verification
**SOURCE-DERIVED FACT:**
- **Exact subscription/package required:** Norgate Data US Stocks **Diamond** package (which provides history back to 1950, necessary to cover the 1982–2002 H01 era; the Platinum package only covers back to 1990).
- **Russell 2000 index data:** Included in the US indices offering.
- **NYSE Composite index data:** Included in the US indices offering.
- **Format:** Both series are available as daily end-of-day data (OHLC format).
- **Historical Depth:** The Diamond package supports history back to 1950.
- **Continuity:** Historical data is continuous and versioned via the Norgate Data Updater.

## 3. Russell 2000 Verification
**MODEL INFERENCE / GOVERNANCE DECISION:**
- **Identity:** Genuine US small-cap equity index tracking the 2,000 smallest stocks in the Russell 3000 index.
- **Distinctness:** Structurally distinct from the S&P 500 (`sp`). The S&P 500 covers large-cap US equities, whereas the Russell 2000 covers small-cap US equities. This represents a distinct segment of the broad US equity market and should be considered a second exposure under the existing exposure-accounting rules (G2 distinctness passed).

## 4. NYSE Composite Verification
**MODEL INFERENCE / GOVERNANCE DECISION:**
- **Identity:** Genuine broad-US exchange equity index covering all common stock listed on the New York Stock Exchange.
- **Distinctness:** Structurally distinct from the S&P 500. The S&P 500 is a cap-weighted index of 500 selected large companies. The NYSE Composite covers thousands of stocks simply by virtue of exchange listing. It represents a different methodology and constituent scope, qualifying it as a structurally distinct second exposure.

## 5. Historical Coverage
**SOURCE-DERIVED FACT / GOVERNANCE DECISION:**
- The required H01 historical era is 1982–2002.
- The US Stocks Diamond package provides coverage back to 1950.
- While the Diamond package goes to 1950, the exact first usable dates for the specific indices depend on their respective inceptions (e.g., Russell 2000 inception in 1984; NYSE Composite inception in 1966).
- **Overlap:** The overlap for Russell 2000 would cover 1984–2002, capturing the 1987 crash, the 1990s bull market, and the 2000–02 bear market. The overlap for NYSE Composite would cover the entire 1982–2002 era. 

## 6. Exposure Distinctness
**GOVERNANCE DECISION:**
Both the Russell 2000 and the NYSE Composite pass the exposure distinctness requirement compared to the existing `sp` (S&P 500 futures) market. Neither is merely another representation of the same large-cap exposure.

## 7. Data Object / Methodology
**SOURCE-DERIVED FACT:**
- **Price vs. Total-Return:** Norgate provides price-type index values (daily close is the official published index level).
- **Format:** Daily OHLC is natively provided.
- **Adjustments:** No ratio-back-adjustment is applied to the index-level daily close. It is the canonical published value.

## 8. Data Integrity
**GOVERNANCE DECISION:**
- **Status:** **UNVERIFIED.**
- **Reason:** The operator has not yet authorized the purchase of a subscription. No sample data has been obtained. Checks for duplicate timestamps, missing dates, weekend rows, non-positive values, and malformed records must be performed on the actual data post-procurement.

## 9. Cross-Source Validation
**GOVERNANCE DECISION:**
- **Status:** **UNVERIFIED.**
- **Reason:** Pending sample data access.

## 10. Licensing
**SOURCE-DERIVED FACT:**
- **Personal Use:** Allowed ("The Licensee may use the Content for a personal purpose such as investment or trading.").
- **Redistribution:** Prohibited ("The Licensee will not: (i) redistribute the Content in any way or form except where express permission has been sought...").
- **Commercial Use:** Prohibited.
- **Machine Access / Export:** Permitted locally via Python API / Norgate Data Updater.

**GOVERNANCE DECISION:**
- **Classification:** **PENDING.**
- **Rationale:** The license permits private research use, but explicit written permission for permanent repository archival (fingerprinting and storage in the frozen H01 artifacts) requires formal clarification, consistent with the precedent set for HPD and FRED data. No formal inquiry has been sent to Norgate yet.

## 11. Reproducibility
**SOURCE-DERIVED FACT:**
- **Mechanism:** Data is accessed locally via the Norgate Data Updater and extracted using the official `norgatedata` Python package (available on PyPI).
- **Determinism:** The data updates are versioned. An exact extraction script can be written to pull the historical index series to a CSV file.
- **Fingerprinting:** The resulting CSV file can be deterministically hashed (SHA-256) and stored as a frozen artifact. Another researcher with a Norgate subscription running the same script on the same database vintage will successfully reproduce the extraction.

## 12. Procurement Status
**SOURCE-DERIVED FACT / GOVERNANCE DECISION:**
- **Subscription Required:** Norgate Data US Stocks
- **Package Name:** Diamond (required for pre-1990 history)
- **Current Price:** ~$787.50 / year
- **Sample Access Status:** Not accessed. No subscription exists in the environment.
- **Remaining Uncertainty:** Actual data integrity (missing days, gaps) and exact first-available date for the specific indices in Norgate's database.

## 13. Decision Gates
**GOVERNANCE DECISION:**
- **G1 — Product availability:** **PASS** (Confirmed via Norgate documentation).
- **G2 — Broad-US identity:** **PASS** (Both candidates are genuine broad-US).
- **G3 — Exposure distinctness:** **PASS** (Structurally distinct from S&P 500).
- **G4 — Historical overlap:** **PASS** (Sufficient overlap with 1982-2002 era).
- **G5 — Data integrity:** **PENDING** (Requires sample data access).
- **G6 — Reproducibility:** **PASS** (Python API and updater support deterministic extraction).
- **G7 — Licensing:** **PENDING** (Requires explicit archival permission).
- **G8 — Extraction/fingerprinting feasibility:** **PASS** (Can extract to CSV and SHA-256 hash).

## 14. Governance Decision
**B — SOURCE PROMISING BUT MORE DUE DILIGENCE REQUIRED**

The Norgate US Stocks Diamond package is structurally and operationally capable of solving the historical broad-US evidence gap. However, the requirement to verify data integrity and cross-source fidelity cannot be bypassed. The process is paused at the procurement gate.

## 15. Exact Next Legitimate Task
> **AUTHORIZE NORGATE US STOCKS DIAMOND PROCUREMENT OR CLARIFY ARCHIVAL RIGHTS**

The operator must authorize the ~$787.50 annual subscription to proceed to the data integrity and cross-source validation gates (G5, G9). Alternatively, the operator may authorize a formal written inquiry to Norgate regarding permanent research repository archival rights before committing funds.

## 16. Prohibited Follow-Up
- Purchasing the subscription without operator authorization.
- Extracting full histories for non-target markets.
- Computing any H01 statistics on the candidate data once procured.
- Adding any market to the frozen H01 universe.

## 17. Integrity
- **Outcome-blind:** No H01 statistics or results were calculated.
- **Read-only:** No files in the repository were altered during this verification task except for the creation of this report.
- **No external communication:** Norgate was not contacted. Information was retrieved solely from public documentation.
- **No unauthorized procurement:** No purchase was attempted or authorized.
