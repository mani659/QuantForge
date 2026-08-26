# QUANTFORGE — H01 EQUITY TRACK A
# V1.3 SOURCE-IDENTITY AMENDMENT PROPOSAL

## 1. Purpose
The purpose of this amendment proposal is to authorize the creation of a new **V1.3.0 execution identity** for the H01 Equity experiment. This amendment officially replaces the permanently unavailable V1.2.0 source snapshots with scientifically equivalent free/repository-derived snapshots without altering the underlying scientific object, methodology, or hypothesis.

## 2. Reason V1.3 Is Required
The H01 Equity V1.2.0 experiment is currently **FROZEN / EXECUTION BLOCKED**. Five exact frozen input snapshots (`front_sp.csv`, `fred_SP500.csv`, `fred_DJIA.csv`, `fred_NASDAQCOM.csv`, `fred_NASDAQ100.csv`) are permanently unavailable from the repository, and their exact original cryptographic hashes cannot be recovered. H01 execution cannot proceed without perfectly matching the fingerprint gate. Therefore, a new execution identity (V1.3) must be explicitly governed to bind new, scientifically equivalent source snapshots.

## 3. V1.2.0 Historical Identity
**V1.2.0 remains historically frozen and unchanged.** This amendment does not overwrite the historical record or invalidate V1.2.0. V1.3 is strictly a successor execution identity created solely to bypass the irretrievable loss of the original V1.2.0 source artifacts.

## 4. V1.3 Source Identity
V1.3 is classified strictly as a **SOURCE-IDENTITY / INPUT-SNAPSHOT AMENDMENT**. It is not a scientific redesign. The V1.3 execution identity will mandate a strict cryptographic fingerprinting gate against the new explicitly registered hashes.

## 5. SP Replacement
- **Proposed source identity:** `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/daily_series/sp_historical.csv`
- **SHA-256:** `DD35661826279D786C3ACEC08446E7F0C99137B6A349AD367461851B61148BD8`
- **File size:** 341,705 bytes
- **Row count:** 5,163 (1982-04-21 to 2002-10-01)
- **Columns:** `date`, `sym`, `close`, `adj_close`, `is_roll_day`, `log_return`
- **Provenance:** Derived scientific representation of the now-unrecoverable `front_sp.csv`. Generated deterministically by the original H01 execution pipeline (`run_h01_equity_v1.py`). This is a repository-derived equivalent, NOT the original source file.

## 6. NYA Existing Source
- **Frozen source:** `docs/NYA_DATA.html`
- **SHA-256:** `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f`
- No new replacement is proposed. The exact existing artifact and hash remain active.

## 7. FRED Replacement Snapshots
Fresh snapshots for the following FRED series will be acquired **only after amendment approval**:
- `SP500` (SHA-256: `V1.3_SHA256_PENDING_ACQUISITION`)
- `DJIA` (SHA-256: `V1.3_SHA256_PENDING_ACQUISITION`)
- `NASDAQCOM` (SHA-256: `V1.3_SHA256_PENDING_ACQUISITION`)
- `NASDAQ100` (SHA-256: `V1.3_SHA256_PENDING_ACQUISITION`)

## 8. Scientific Equivalence Requirements
V1.3 requires pre-execution verification of scientific equivalence:
- **SP**: Must confirm the same instrument, same ratio-back-adjustment method, same daily series, same 1982-2002 date coverage, same `adj_close` scientific field, and same roll semantics.
- **FRED**: Must confirm the same series IDs, same index definitions, same daily observations over the required H01 windows, same price-type meaning, and no substituted series.
- **NYA**: Must confirm the unchanged existing frozen source, same `Close` field, and same date coverage.
If any equivalence test fails, V1.3 execution is automatically blocked.

## 9. Provenance and Fingerprinting
- `sp_historical.csv` is not the original `front_sp.csv`. It contains the exact scientific S&P series used by H01, derived via a documented and deterministic transformation. Its exact SHA becomes the V1.3 source identity.
- The derivation chain must be preserved, and no further transformations are permitted before execution.
- The exact FRED snapshots, once downloaded, must immediately receive a SHA-256 hash. The raw downloaded artifacts must be preserved.

## 10. Source-Freeze Requirements
- **No live vendor query during experiment execution.** All vendor data must be explicitly frozen locally before execution.
- Execution consumes only the frozen local snapshots bound by SHA-256. A later FRED revision must NOT silently alter a running or future execution.
- The protocol's existing date/window rules solely determine which observations are analytically used; the raw snapshot itself must not be silently truncated before fingerprinting.

## 11. Statistical Invariants
All statistical and methodological components are explicitly frozen and remain identical to V1.2.0:
- Scientific hypothesis
- Four-cell family
- Market membership
- Historical/validation/forward partitions
- Event definition
- Response definition
- Daily return construction
- Primary statistic
- Null construction
- Bootstrap method and block length
- Replicate count (B=10,000)
- Random seed policy (V1.3 must preserve the frozen execution seed unless the protocol explicitly requires otherwise)
- Confidence interval construction
- P-value calculation
- Holm correction and Alpha (0.05)
- Minimum matched-pair requirements, evaluability, and falsification rules.

## 12. Multiple-Testing Family
V1.3 **does not introduce a new hypothesis test**. The family remains exactly four cells:
1. EQBROAD_L1
2. EQBROAD_L2
3. EQTECH_L1
4. EQTECH_L2
The FRED source replacement does not create additional cells. The SP replacement does not create an additional market. NYA remains the exact same approved second EQBROAD_L1 market.

## 13. No Outcome-Dependent Replacement
V1.3 strictly prohibits:
- Replacing any FRED series, SP, or dropping NYA after seeing results.
- Changing sources based on performance.
- Changing historical windows, market composition, or statistical parameters.
Any future source replacement strictly requires a new governance amendment.

## 14. Failure Handling
- **Source acquisition failure:** Treated as an infrastructure/data-acquisition failure, NOT scientific evidence.
- **Hash mismatch:** Execution blocked.
- **Missing required series:** Execution blocked.
- **Scientific-equivalence failure:** Governance review required.
- **Experiment runtime failure:** Execution failure, not a scientific result. Reinterpretation of infrastructure problems as H01 findings is prohibited.

## 15. Budget Constraint
**No paid data acquisition is authorized or required.**
Expected sources are the existing `sp_historical.csv`, existing `NYA_DATA.html`, and freely obtainable FRED snapshots. No Norgate, DataBento, Bloomberg, CRSP, or other paid replacement is authorized.

## 16. Governance Sequence
1. **V1.3 Proposal:** Prepared and submitted (current step; does NOT authorize execution).
2. **Owner approval:** Required before any sources may be acquired/frozen.
3. **Acquisition:** Free FRED snapshots downloaded and fingerprinted.
4. **Source-identity audit:** Verifies all exact hashes.
5. **Final execution-readiness audit:** Verifies the complete V1.3 identity.
6. **Owner execution authorization:** Explicitly required for the single execution.

## 17. Owner Approval Requirement
Owner explicitly must approve this V1.3 amendment proposal before any new data acquisition occurs.

## 18. Explicit Non-Authorization of Execution
This proposal **DOES NOT AUTHORIZE EXECUTION**. It only authorizes the data-acquisition and source-identity re-fingerprinting process upon owner approval.
