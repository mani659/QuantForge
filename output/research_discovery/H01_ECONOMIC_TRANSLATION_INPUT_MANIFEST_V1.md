# QUANTFORGE — H01 EQUITY TRACK A
# ECONOMIC TRANSLATION INPUT MANIFEST V1

## 1. Protocol Identity
- **Economic Protocol Version**: V1
- **Economic Protocol SHA**: `1bb9fc1f56a2d49839609344b9dcb8bc4a7424987367b3b629b48814503befa7`

## 2. Six-Market Input Sources
All inputs are identically inherited from the scientifically supported H01 V1.3.0 universe.

| Market | Source | SHA-256 | Field | Historical | Contemporary | Status |
|---|---|---|---|---|---|---|
| `sp` | `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/daily_series/sp_historical.csv` | `dd35661826279d786c3acec08446e7f0c99137b6a349ad367461851b61148bd8` | `adj_close` | Y | N | READY |
| `NYA` | `docs/NYA_DATA.html` | `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f` | `<td[4]>` (Close) | Y | N | READY |
| `SP500` | `data/fred/fred_SP500.csv` | `4b6c37f3477a4f3454009e500eb1b4d7844b38b0aaad10097b5fe6a5f8ae0db7` | `SP500` | N | Y | READY |
| `DJIA` | `data/fred/fred_DJIA.csv` | `6a274816b3ed64956346c10dc8decb5eb585155ac16af410cd2306048d290ee2` | `DJIA` | N | Y | READY |
| `NASDAQ100` | `data/fred/fred_NASDAQ100.csv` | `1196c3f2dca171c1b56b4bbe2cc1fcd51ec7ea1f30bb74d7c3cfc2a313ffe52f` | `NASDAQ100` | Y | Y | READY |
| `NASDAQCOM` | `data/fred/fred_NASDAQCOM.csv` | `377af7dec4b1a01486cc9e2db48fbe0538e024d58ed258eedbd01e98494358d6` | `NASDAQCOM` | Y | Y | READY |

## 3. Date Alignment and Structural Viability
- **Chronology**: All data sets strictly chronological.
- **Date Matching**: Historical (1982-04-21 to 2002-10-01) and Contemporary (2016-08-15 to 2026-08-14) eras are fully supported by the respective files. `NASDAQ100` Historical coverage begins 1986-01-02 natively (allowed).
- **Missing Data Handling**: Handled deterministically per H01 invariants; missing strings ("-", ".") are trapped, zero returns filtered based on the protocol.

## 4. Signal Construction Feasibility
- **Lookback**: Continuous daily series fully support computing the trailing 11-day distribution ($L=11$).
- **Forward Horizon**: Sufficient consecutive days exist to map the prior-day state to the 1-day forward outcome ($r_t$) without structural look-ahead.

## 5. Cost Model Support
The required cost model strictly relies on the frozen assumptions (2 bps base, 5 bps stress). No market-specific bid/ask or spread data is required, so the existing close-only daily series are sufficient.

## 6. Equal-Market Weight Feasibility
All six market series are independent and capable of separately calculating the per-market conditional incremental return ($\Delta_m$) prior to cross-market equal weighting. 

## 7. Era Separation Feasibility
Historical and contemporary inputs correspond perfectly to separate source blocks. They can be naturally evaluated as independent economic endpoints as dictated by the dual-era primary gate.

## 8. Bootstrap Input Feasibility
The chronological density and volume (thousands of observations per era) easily support the $11$-day block market-clustered bootstrap with $B=10,000$ replicates.

## 9. Preparation Status
> **ALL INPUTS READY AND FROZEN**
No explicit data transformations outside of the already-approved dynamic loading logic (e.g. `load_nya`) are required. Original files are untouched.
