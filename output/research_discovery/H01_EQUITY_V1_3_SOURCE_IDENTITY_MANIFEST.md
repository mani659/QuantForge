# QUANTFORGE — H01 EQUITY TRACK A
# V1.3 SOURCE IDENTITY MANIFEST

## Identity Core
* **Protocol Version:** V1.3.0
* **Definition-Lock Version:** V1.2.0 (Unchanged)
* **Seed:** 20260816 (Unchanged)

## Implementation
* **Implementation Artifact:** `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/run_h01_equity_v1.py`
* **Implementation SHA-256:** `25bd4bcc3316d882ad28a8252b59f4c1331e0ee54fdb0d1fb6de63cd623404b2`
* **Changes:** Minimal deterministic header allowance for `sp_historical.csv` (line 180 updated to accept 6-column header). FREDDIR updated to permanent governed path. Corrected runtime identity: HPD path updated, FINGERPRINTS updated with V1.3 SHAs, hardcoded `front_sp.csv` filename changed to `sp_historical.csv`. Gate-6 explicitly bound to governed `data/PER_MARKET_VALIDATION.csv`.

## Registered Source Artifacts
* **SP (Historical Equivalent):** `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/daily_series/sp_historical.csv`
  * **SHA-256:** `DD35661826279D786C3ACEC08446E7F0C99137B6A349AD367461851B61148BD8`
* **NYA (Existing):** `docs/NYA_DATA.html`
  * **SHA-256:** `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f`
* **FRED SP500:** `data/fred/fred_SP500.csv`
  * **SHA-256:** `4b6c37f3477a4f3454009e500eb1b4d7844b38b0aaad10097b5fe6a5f8ae0db7`
* **FRED DJIA:** `data/fred/fred_DJIA.csv`
  * **SHA-256:** `6a274816b3ed64956346c10dc8decb5eb585155ac16af410cd2306048d290ee2`
* **FRED NASDAQCOM:** `data/fred/fred_NASDAQCOM.csv`
  * **SHA-256:** `377af7dec4b1a01486cc9e2db48fbe0538e024d58ed258eedbd01e98494358d6`
* **FRED NASDAQ100:** `data/fred/fred_NASDAQ100.csv`
  * **SHA-256:** `1196c3f2dca171c1b56b4bbe2cc1fcd51ec7ea1f30bb74d7c3cfc2a313ffe52f`

## Acquisition Metadata (FRED)
* **Acquisition Timestamp:** 2026-08-23T15:24:00+03:00
* **Source:** Official FRED platform (https://fred.stlouisfed.org)
* **Raw Artifacts:** Saved locally without manual truncation or modification.
