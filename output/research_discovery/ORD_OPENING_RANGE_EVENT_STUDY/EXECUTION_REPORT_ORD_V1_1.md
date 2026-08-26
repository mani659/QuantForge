# QUANTFORGE — ORD V1.1.0 EXECUTION REPORT

## 1. Execution Status

> **PASS**

The frozen ORD V1.1.0 protocol was executed once, exactly as registered. Three markets passed the anomaly gate and produced scientific results. One market (BTCUSD) was halted per §20 (>10% invalid-day fraction).

## 2. Protocol Identity

| Field | Value |
|---|---|
| Version | V1.1.0 |
| File | `ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md` |
| SHA-256 | `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06` |
| Amendment | AMEND-DENOM-1 (§20 denominator) |

## 3. Execution Identity

| Field | Value |
|---|---|
| Repository HEAD | `a6c62edf9666f59eb8a044da2d0497f9a366e0a0` |
| Seed | 20260818 |
| B | 10,000 |
| L | 10 (p=0.1 terminate / 0.9 continue) |
| α | 0.05 |
| HORIZON | 120 minutes |
| MIN_TREATMENT | 100 |
| HALT_FRACTION | 0.10 |
| Execution start | 2026-08-18T12:16:56 UTC |
| Execution end | 2026-08-18T12:18:05 UTC |
| Duration | 69.9 seconds |
| Python | 3.11 |
| Platform | Windows |

## 4. Universe

| Market | Status | Total Dates | Invalid Days | Invalid % | Events | Treatment | Control |
|---|---|---|---|---|---|---|---|
| XAUUSD | PASS | 1,288 | 4 | 0.31% | 2,256 | 2,184 | 62 |
| XAGUSD | PASS | 1,282 | 11 | 0.86% | 2,251 | 2,177 | 56 |
| BTCUSD | HALTED | 1,825 | 218 | 11.95% | — | — | — |
| USATECHIDXUSD | PASS | 706 | 27 | 3.82% | 927 | 839 | 25 |

EURUSD: EXCLUDED (DATA-LIMITED)

## 5. Data Integrity

| Input | Expected SHA-256 | Actual SHA-256 | Status |
|---|---|---|---|
| XAUUSD_M1.csv | `54cf61559673adc7…` | `54cf61559673adc7…` | ✅ |
| XAGUSD_M1.csv | `69444be954a869eb…` | `69444be954a869eb…` | ✅ |
| USATECHIDXUSD_M1.csv | `39f25619bd26d72f…` | `39f25619bd26d72f…` | ✅ |
| BTCUSD_M1.csv | `97b853854d8f650d…` | `97b853854d8f650d…` | ✅ |

Protocol SHA verified: ✅
Definition Lock exists: ✅
Pre-registration audit PASS: ✅

## 6. Anomaly Gate Results

| Market | Invalid Fraction | Threshold | Result |
|---|---|---|---|
| XAUUSD | 0.31% | 10% | PASS |
| XAGUSD | 0.86% | 10% | PASS |
| BTCUSD | 11.95% | 10% | HALTED |
| USATECHIDXUSD | 3.82% | 10% | PASS |

BTCUSD halt is consistent with the V1.0.0 execution and reflects the genuine data characteristics of a 24/7 market where many dates have observations only outside the ORD detection window.

## 7. Scientific Results (Non-Adjudicated)

> **NOT ADJUDICATED — deferred to independent adjudication.**

### Evaluable Markets

| Market | N_days | Treatment | Control | ΔM_obs | p_raw | p_holm | B_valid | Classification |
|---|---|---|---|---|---|---|---|---|
| XAUUSD | 1,284 | 2,184 | 62 | 30.90 | 1.0e-04 | 3.0e-04 | 10,000 | SUPPORT |
| XAGUSD | 1,267 | 2,177 | 56 | 71.04 | 1.0e-04 | 3.0e-04 | 10,000 | SUPPORT |
| USATECHIDXUSD | 660 | 839 | 25 | 49.52 | 5.0e-04 | 5.0e-04 | 10,000 | SUPPORT |

### Halted Markets

| Market | Reason | Events | Treatment | Control |
|---|---|---|---|---|
| BTCUSD | Invalid-day fraction 11.95% > 10% | — | — | — |

### Holm Step-Down

Three evaluable markets. Raw p-values sorted: [1.0e-04, 1.0e-04, 5.0e-04]. Holm adjustment applied at α = 0.05.

## 8. Artifact Inventory

| Artifact | SHA-256 (first 16) | Size |
|---|---|---|
| event_table_all_markets.csv | `ac92a58579f5ed12…` | 1,420,520 bytes |
| statistics.json | `9c86718a922e58d0…` | 3,612 bytes |
| metadata.json | `92d1d9a71683bab4…` | 6,771 bytes |
| bootstrap_XAUUSD.npy | `e425941a4e3ca4e9…` | 80,128 bytes |
| bootstrap_XAGUSD.npy | `293aa004c8684cf6…` | 80,128 bytes |
| bootstrap_USATECHIDXUSD.npy | `c29537b7c1f47431…` | 80,128 bytes |
| null_XAUUSD.npy | `193dd80e785f2e7a…` | 80,128 bytes |
| null_XAGUSD.npy | `d06c22fe5caf5a53…` | 80,128 bytes |
| null_USATECHIDXUSD.npy | `3ae1637a4b892ac8…` | 80,128 bytes |

All artifact hashes are recorded in `metadata.json`.

## 9. Execution Discipline

- ✅ Executed once
- ✅ No smoke test
- ✅ No reduced B
- ✅ No rerun
- ✅ No parameter modification
- ✅ No market selection
- ✅ No methodology alteration
- ✅ Protocol unchanged
- ✅ Definition Lock unchanged
- ✅ All bootstrap/null draws persisted
- ✅ All event data persisted
- ✅ Deterministic (fixed seed, stable operations)

## 10. Historical V1.0.0 Preservation

The V1.0.0 protocol and its stopped execution artifacts remain preserved:

- `ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1.md` — V1.0.0 protocol
- `ORD_OPENING_RANGE_EVENT_STUDY/EXECUTION_REPORT_ORD_V1.md` — V1.0.0 stopped execution report
- `ORD_OPENING_RANGE_EVENT_STUDY/statistics.json` — V1.0.0 halted statistics
- `ORD_OPENING_RANGE_EVENT_STUDY/metadata.json` — V1.0.0 execution metadata

The V1.0.0 STOP remains a permanent historical record.

## 11. Scientific Adjudication

> **NOT PERFORMED — DEFERRED TO INDEPENDENT ADJUDICATION.**

## 12. Governance State

> **ORD V1.1.0 — EXECUTED ONCE, AWAITING INDEPENDENT ADJUDICATION**

## 13. Required Next Task

> **ORD V1.1.0 INDEPENDENT EXECUTION / RESULTS ADJUDICATION**
