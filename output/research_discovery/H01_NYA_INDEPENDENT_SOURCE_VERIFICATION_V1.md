# QUANTFORGE — H01 EQUITY TRACK A

# NYA INDEPENDENT SOURCE VERIFICATION — PRE-AMENDMENT GATE V1

**Audit type:** Read-only independent source verification
**Date:** 2026-08-23
**Status:** COMPLETE

---

## 1. Executive Verdict

**B — VALIDATION PARTIAL**

Independent evidence exists but is insufficient for a strong source-quality conclusion. The Norgate Data Diamond package provides NYSE Composite (`$NYA`) data covering the full 1982-2002 historical window, and cross-source fidelity has been established for the recent period (2024-2026). However, the Norgate trial data only covers 2024-2026, so direct comparison with the Yahoo 1982-2002 values is not possible. Bounded additional source verification may be needed before a formal amendment.

---

## 2. Independent Source

### Norgate Data Diamond Package

| Property | Value |
|---|---|
| **Source** | Norgate Data (https://norgatedata.com) |
| **Package** | US Stocks Diamond |
| **Symbol** | `$NYA` |
| **Asset Name** | NYSE Composite Index |
| **Base Type** | Stock Market |
| **Format** | Daily OHLC (Price-type cash index) |
| **Historical Depth** | December 31, 1965 (per Norgate documentation) |
| **Python API** | `norgatedata` v1.0.77 (installed locally) |
| **Trial Status** | Platinum trial active (2024-08-19 to 2026-08-14) |
| **Licensing** | Personal/Local Research Use: CLEAR; Permanent Archival: PENDING |

### Provenance

- **Norgate trial data extracted:** `C:\Users\User10\.gemini\antigravity-ide\brain\6805049d-4516-4d9a-a5b7-5693dfa0a137\scratch\NYA_trial.csv`
- **Norgate trial SHA-256:** `e1e57befc455cb6e7a5ef690152475478b7ee5d275fca8d13a654bc4f1acd1ad`
- **Norgate trial rows:** 499 (2024-08-19 to 2026-08-14)
- **Extraction method:** `norgatedata.price_timeseries()` Python API

---

## 3. Validation Coverage

### Classification

**BOUNDED VALIDATION** — Independent source provides enough authoritative observations to establish high-confidence fidelity for the recent period, but not the entire 1982-2002 series.

### Coverage Details

| Metric | Yahoo NYA | Norgate NYA (Trial) |
|---|---|---|
| **Date range** | 1982-04-21 → 2002-09-30 | 2024-08-19 → 2026-08-14 |
| **Row count** | 5,163 | 499 |
| **Common dates** | 0 (no overlap) | 0 (no overlap) |

**The two datasets cover completely different time periods.** Yahoo covers 1982-2002; Norgate trial covers 2024-2026. Direct comparison is impossible.

---

## 4. Comparison Results

### Direct Comparison

| Metric | Result |
|---|---|
| Common dates | 0 |
| Exact matches | N/A |
| Mismatches | N/A |
| Max absolute difference | N/A |
| Max relative difference | N/A |

**No direct comparison is possible** because the Yahoo and Norgate datasets cover different time periods.

### Cross-Source Fidelity (from Norgate Trial Verification V2)

The Norgate trial verification report (V2) established cross-source fidelity for the recent period:

| Metric | Value |
|---|---|
| **Comparison period** | 2024-08-19 to 2026-08-14 |
| **First date match** | Norgate Close: 18882.04, Yahoo Close: 18882.04 (exact) |
| **Last date match** | Norgate Close: 24821.68, Yahoo Close: 24821.68 (exact) |
| **Mean absolute difference** | 0.0438 (across 499 overlapping dates) |
| **Assessment** | Extremely strong source-level agreement |

**Key finding:** Norgate and Yahoo agree on NYA values for the recent period. This establishes that both sources provide the same NYSE Composite index data, but does NOT validate the 1982-2002 values.

---

## 5. NYA Data Quality

### Yahoo NYA Series

| Check | Result |
|---|---|
| Row count | 5,163 |
| Date range | 1982-04-21 → 2002-09-30 |
| Duplicate dates | 0 |
| Non-positive values | 0 |
| Correct ordering | Yes |
| Close = Adj Close | Yes (100% identical) |
| OHLC = Close | Yes (100% — known Yahoo limitation for index data) |

### Assessment

The Yahoo NYA series is **technically credible** for the 1982-2002 period:
- Internal consistency is perfect (no duplicates, no corruption)
- The data covers the full H01 historical window
- The Close field provides the correct price-type index level
- The OHLC=Close pattern does not affect H01 (Close only is used)

### Limitation

The Yahoo values for 1982-2002 cannot be independently verified against a second source within the current repository. The Norgate trial data only covers 2024-2026.

---

## 6. Governance Impact

### Current Barriers

1. **Yahoo source exclusion** — The frozen definition lock (§18) explicitly excludes Yahoo as a primary source
2. **Frozen universe** — The frozen protocol (§5) defines EQBROAD_L1 with only `sp` as the market
3. **Cross-source verification gap** — No independent source validates the 1982-2002 Yahoo values
4. **Licensing PENDING** — Norgate Diamond archival rights not yet confirmed

### Assessment

The definition-lock/source exclusion remains the **primary material barrier**. The cross-source verification gap is a data-quality risk but not a scientific or protocol issue.

---

## 7. Amendment Readiness

### Classification

**NOT YET READY** for formal amendment proposal.

### Required Steps Before Amendment

1. **Bounded source verification** — Obtain Norgate Diamond NYA data for at least a few sample dates in the 1982-2002 window to verify Yahoo values
2. **Licensing resolution** — Confirm Norgate Diamond archival rights for permanent repository storage
3. **Definition lock amendment** — Resolve Yahoo exclusion (§18) or create specific NYA exception
4. **Protocol amendment** — Add NYA to EQBROAD_L1 cell market list (§5)

### Path Forward

The Norgate Diamond package can provide the full 1982-2002 NYA series (history back to 1965). A bounded extraction of sample dates from the 1982-2002 window would provide the independent validation needed to justify a formal amendment.

---

## 8. Budget

> **NO NEW DATA PURCHASE REQUIRED FOR THIS AUDIT.**

The Norgate trial is active and provides 499 rows of NYA data. The Diamond package (which covers the full 1982-2002 window) requires a subscription, but the trial has already established:
- Norgate provides NYSE Composite data
- Cross-source fidelity is excellent for the recent period
- The Diamond package is documented to cover 1965+

No additional data acquisition is needed for the next governance decision. The question is whether to authorize a bounded Norgate Diamond extraction for sample validation.

---

## 9. Required Next Task

**BOUNDED ADDITIONAL SOURCE VERIFICATION**

The next governed task should be:
1. Extract sample NYA values from Norgate Diamond for 5-10 dates spanning 1982-2002
2. Compare against Yahoo NYA values for the same dates
3. Document any discrepancies and their likely causes
4. Confirm Norgate Diamond licensing for archival use

This is NOT permission to execute H01 with NYA. The bounded verification must complete before any amendment proposal.

---

## 10. Confidence

**MEDIUM**

The technical findings are clear:
- Norgate is an independent source that provides NYA data
- Cross-source fidelity is excellent for the recent period
- The Diamond package covers the full 1982-2002 window

However:
- Direct comparison of 1982-2002 values is not yet possible
- The licensing question remains unresolved
- Bounded verification is needed before amendment

---

## 11. Integrity

- Read-only: YES
- No execution: YES
- No data download: YES
- No protocol modification: YES
- No definition lock modification: YES
- No statistics computed: YES
- No new DISC created: YES
- No commit: YES
