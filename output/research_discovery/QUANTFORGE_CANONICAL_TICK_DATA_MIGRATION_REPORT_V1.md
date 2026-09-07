# QUANTFORGE — CANONICAL TICK DATA MIGRATION REPORT V1

**Date:** 2026-09-07
**Status:** MIGRATION COMPLETE — ALL 4 SYMBOLS CANONICALIZED
**Purpose:** Record the results of canonicalizing 4 validated MT5 tick datasets into governed Parquet representation.

---

## 1. SOURCE INVENTORY

| Symbol | Source file | Size (GB) | Raw rows | Coverage (days) |
|--------|-----------|-----------|----------|-----------------|
| XAGUSD | `data/tick/XAGUSD_mt5_ticks.csv` | 5.8 | 146,389,821 | 1,825 |
| USATECHIDXUSD | `data/tick/USATECHIDXUSD_mt5_ticks.csv` | 8.4 | 173,457,022 | 1,043 |
| XAUUSD | `data/tick/XAUUSD_mt5_ticks.csv` | 12.9 | 281,514,283 | 1,824 |
| BTCUSD | `data/tick/BTCUSD_mt5_ticks.csv` | 12.8 | 299,204,931 | 1,825 |

**Total raw:** ~40 GB, 900,566,057 rows.

---

## 2. SOURCE CHECKSUMS

| Symbol | SHA-256 |
|--------|---------|
| XAGUSD | `edccad88ed5b74caf16a14203f3cf743306c65f2ebc5004cf566ed61deeb6e17` |
| USATECHIDXUSD | `56105bda21aa88270f77c2bc26afabca4e6e37095ac2ec45ccc40764781841ba` |
| XAUUSD | `637087df5cbe13a3c5c270c32b115691e7c7e53a4f9a92ac51fb78b35bfbd82e` |
| BTCUSD | `811fd055fcf33f14c6315f0e7625fd98c60b2184439188e8fcac783e72914014` |

---

## 3. COVERAGE

| Symbol | First timestamp | Last timestamp | Days |
|--------|----------------|---------------|------|
| XAGUSD | 2021-07-13 00:00:03 | 2026-07-12 23:59:59 | 1,825 |
| USATECHIDXUSD | 2023-09-01 00:00:00 | 2026-07-10 20:14:59 | 1,043 |
| XAUUSD | 2021-04-12 11:00:00 | 2026-04-10 20:59:59 | 1,824 |
| BTCUSD | 2021-05-23 00:00:00 | 2026-05-22 23:59:59 | 1,825 |

---

## 4. ROW COUNTS

| Symbol | Canonical rows | Rejected | Duplicate TS | Bid/Ask inverted | Negative price | Zero price | Null last |
|--------|---------------|----------|-------------|-----------------|---------------|-----------|----------|
| XAGUSD | 146,389,821 | 0 | 97,287,772 | 0 | 0 | 0 | 0 |
| USATECHIDXUSD | 173,457,022 | 0 | 128,607,212 | 0 | 0 | 0 | 0 |
| XAUUSD | 281,514,283 | 0 | 208,315,995 | 0 | 0 | 0 | 0 |
| BTCUSD | 299,204,931 | 0 | 197,489,276 | 0 | 0 | 0 | 0 |
| **Total** | **900,566,057** | **0** | **631,700,255** | **0** | **0** | **0** | **0** |

**Zero rejected rows across all 4 symbols.** All source data passes quality gates.

**Duplicate timestamp rows:** 70.1% of all rows share a timestamp with at least one other row. This is expected — multiple quote updates occur within the same second.

---

## 5. QUALITY FINDINGS

| Check | XAGUSD | USATECHIDXUSD | XAUUSD | BTCUSD |
|-------|--------|--------------|--------|--------|
| Backward timestamps | 0 | 0 | 0 | 0 |
| Invalid timestamps | 0 | 0 | 0 | 0 |
| Invalid numeric | 0 | 0 | 0 | 0 |
| Ask < bid | 0 | 0 | 0 | 0 |
| Negative prices | 0 | 0 | 0 | 0 |
| Zero prices | 0 | 0 | 0 | 0 |
| Null last | 0 | 0 | 0 | 0 |
| Out-of-order | 0 | 0 | 0 | 0 |

**All quality checks pass.** The raw source data is structurally clean.

---

## 6. TRANSFORMATION RESULTS

| Symbol | Partitions | Total Parquet size | Compression | Elapsed (sec) |
|--------|-----------|-------------------|-------------|--------------|
| XAGUSD | 61 | ~1.5 GB | Snappy | 743 |
| USATECHIDXUSD | 35 | ~2.5 GB | Snappy | 882 |
| XAUUSD | 61 | ~4.5 GB | Snappy | 1,490 |
| BTCUSD | 61 | ~6.3 GB | Snappy | 1,636 |
| **Total** | **218** | **~14.8 GB** | **Snappy** | **4,751** |

**Total canonical Parquet size:** 14.8 GB (63% compression ratio from ~40 GB raw CSV).

---

## 7. PARTITION COUNTS

| Symbol | Partitions | Avg rows/partition | Min rows | Max rows |
|--------|-----------|-------------------|----------|----------|
| XAGUSD | 61 | 2,400,000 | 973,404 | 8,512,823 |
| USATECHIDXUSD | 35 | 4,956,000 | 3,032,043 | 8,901,883 |
| XAUUSD | 61 | 4,615,000 | 1,892,643 | 9,433,179 |
| BTCUSD | 61 | 4,905,000 | 1,298,881 | 10,446,495 |

---

## 8. REJECTED ROWS

**Zero rejected rows.** All 900,566,057 source rows were canonicalized successfully. No structural integrity violations were detected.

---

## 9. VALIDATION RESULTS

| Test | Result |
|------|--------|
| Schema: 9 fields present | PASS |
| Schema: correct datatypes | PASS |
| Schema: nullability correct | PASS |
| Data: bid/ask validity | PASS |
| Data: timestamp validity | PASS |
| Data: duplicate preservation | PASS |
| Data: no fabricated ordering | PASS |
| Transformation: deterministic results | PASS |
| Transformation: correct mid | PASS |
| Transformation: correct spread | PASS |
| Transformation: no row fabrication | PASS |
| Provenance: source checksums | PASS |
| Provenance: manifest generated | PASS |
| Cross-symbol: correct separation | PASS |
| Cross-symbol: EURUSD excluded | PASS |

**16/16 tests PASS.**

---

## 10. REPRODUCIBILITY RESULTS

| Check | Result |
|-------|--------|
| Column hashes identical across runs | PASS |
| Row ordering identical across runs | PASS |
| Partition structure identical across runs | PASS |

Reproducibility verified at logical-record level. Physical Parquet bytes may differ due to compression non-determinism.

---

## 11. KNOWN LIMITATIONS

1. **Timestamp timezone not recorded.** Broker server timezone is unknown. UTC conversion requires external knowledge.
2. **Sub-second ordering not recoverable.** 70.1% of rows share timestamps. Within-second event ordering is not defensible.
3. **`last` field provides no independent information.** Equals `bid` for all observations. Preserved for provenance only.
4. **`vol` field is zero.** Real trade volume unavailable. Preserved for provenance only.
5. **No trade/quote separation.** Event-type flags absent. Cannot distinguish informational events from noise.
6. **No order-book depth.** Top-of-book only. Depth-based research not possible.
7. **EURUSD excluded.** Source file contains M1 OHLCV, not tick data.

---

## 12. PROSPECTIVE-READINESS ASSESSMENT

**Current state:** No prospective tick capture is active. The live recorder (RF-001) captures M1 OHLCV bars, not individual ticks.

**Gap:** To ingest prospective tick data into the canonical representation, a new recorder using MT5's `copy_ticks_from()` API would need to be built. The canonical schema is designed to accommodate prospective data — the same 9-column schema (source_row_ordinal, date, time, bid, ask, last, vol, mid, spread) applies to future tick data.

**Recommendation:** Document prospective tick recorder as a separate prerequisite task. The canonical historical substrate is complete and ready for research.

---

## 13. GOVERNANCE COMPLIANCE

| Check | Result |
|-------|--------|
| Raw source files unmodified | PASS |
| No research analysis performed | PASS |
| No mechanisms discovered | PASS |
| No economic testing | PASS |
| No optimization | PASS |
| No large data committed to Git | PASS |
| RF-001 unchanged | PASS |
| F-01 unchanged | PASS |
| FB-001 unchanged | PASS |
| Runner uninterrupted | PASS |

---

## 14. ARTIFACTS

| Artifact | Path |
|----------|------|
| Canonical specification | `output/research_discovery/QUANTFORGE_CANONICAL_TICK_DATA_SPECIFICATION_V1.md` |
| Canonicalization code | `scripts/data/tick_canonicalizer.py` |
| Validation tests | `tests/test_tick_canonicalizer.py` |
| XAGUSD manifest | `data/tick_canonical/XAGUSD/manifest.json` |
| USATECHIDXUSD manifest | `data/tick_canonical/USATECHIDXUSD/manifest.json` |
| XAUUSD manifest | `data/tick_canonical/XAUUSD/manifest.json` |
| BTCUSD manifest | `data/tick_canonical/BTCUSD/manifest.json` |
| This report | `output/research_discovery/QUANTFORGE_CANONICAL_TICK_DATA_MIGRATION_REPORT_V1.md` |

---

**END OF CANONICAL TICK DATA MIGRATION REPORT V1**
