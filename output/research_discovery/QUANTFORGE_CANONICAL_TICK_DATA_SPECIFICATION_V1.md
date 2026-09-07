# QUANTFORGE — CANONICAL TICK DATA SPECIFICATION V1

**Date:** 2026-09-07
**Status:** FROZEN — Ready for quote-level microstructure discovery
**Purpose:** Define the canonical, reproducible, provenance-preserving Parquet representation of QuantForge's validated MT5 tick data.

---

## 1. PURPOSE

This specification defines a lossless, deterministic, reproducible canonical representation of QuantForge's validated MT5 tick CSV data as Parquet. It establishes the research substrate for quote-level microstructure mechanism discovery.

**Authority:** The raw MT5 tick CSVs remain the immutable source-of-record. Canonical Parquet files are derived artifacts only.

---

## 2. SCOPE

This specification covers the four validated TRUE tick datasets:

| Symbol | Source file | Rows | Coverage |
|--------|-----------|------|----------|
| XAGUSD | `data/tick/XAGUSD_mt5_ticks.csv` | 146,389,821 | 2021-07-13 to 2026-07-12 |
| USATECHIDXUSD | `data/tick/USATECHIDXUSD_mt5_ticks.csv` | 173,457,022 | 2023-09-01 to 2026-07-10 |
| XAUUSD | `data/tick/XAUUSD_mt5_ticks.csv` | 281,514,283 | 2021-04-12 to 2026-04-10 |
| BTCUSD | `data/tick/BTCUSD_mt5_ticks.csv` | 299,204,931 | 2021-05-23 to 2026-05-22 |

**Excluded:** `EURUSD_mt5_ticks.csv` (contains M1 OHLCV, not tick data).

---

## 3. SUPPORTED SYMBOLS

| Symbol | Category | Typical spread | Avg ticks/sec |
|--------|----------|---------------|--------------|
| XAGUSD | Precious metals CFD | 0.04 pts | 3.0 |
| USATECHIDXUSD | Index CFD | 1.91 pts | 3.9 |
| XAUUSD | Precious metals CFD | 0.49 pts | 3.8 |
| BTCUSD | Crypto CFD | 78.58 pts | 2.9 |

---

## 4. RAW SOURCE SEMANTICS

Each raw source CSV contains 6 columns, comma-separated, no header:

| Column | Index | Datatype | Semantic |
|--------|-------|----------|----------|
| date | 0 | string (YYYYMMDD) | Trade/quote date |
| time | 1 | string (HH:MM:SS) | Trade/quote time (second resolution) |
| bid | 2 | float64 | Best bid price |
| ask | 3 | float64 | Best ask price |
| last | 4 | float64 | Last traded price (nullable, always equals bid for all symbols) |
| vol | 5 | float64 | Tick volume (always 0 for all symbols) |

**Critical semantics:**
- `last` equals `bid` for 100% of observations. It provides no independent trade-price information.
- `vol` is 0 for all observations. It is tick volume, not real trade volume.
- Both `bid` and `ask` are present and update independently. Spread is reliably calculable.

---

## 5. CANONICAL SCHEMA

Freeze exact names, physical types, and nullability:

| Field | Parquet Type | Nullable | Source |
|-------|-------------|----------|--------|
| source_row_ordinal | INT64 | NO | Derived (0-indexed row position in source CSV) |
| date | STRING | NO | Source column 0 |
| time | STRING | NO | Source column 1 |
| bid | DOUBLE | NO | Source column 2 |
| ask | DOUBLE | NO | Source column 3 |
| last | DOUBLE | YES | Source column 4 (preserved for provenance) |
| vol | DOUBLE | NO | Source column 5 (preserved for provenance) |
| mid | DOUBLE | NO | Derived: (bid + ask) / 2 |
| spread | DOUBLE | NO | Derived: ask - bid |

**Schema version:** V1

---

## 6. TIMESTAMP CONTRACT

- **Resolution:** 1 second (source resolution).
- **Timezone:** Broker server timezone (not converted to UTC). Preserved as-is from source.
- **Precision:** No precision loss. Original `date` and `time` strings preserved exactly.
- **Sub-second ordering:** NOT recoverable. Multiple ticks share the same second. Within-second ordering is not defensible.
- **Canonical interpretation:** Events sharing the same timestamp are contemporaneous at the resolution supported by the source and have no defensible within-timestamp ordering.

---

## 7. DUPLICATE SEMANTICS

- **Policy:** Duplicates are PRESERVED, not deduplicated.
- **Rationale:** Multiple quote updates can legitimately occur within the same second. Each update is an independent observable event.
- **Duplicate rates observed:** 0.07% (USATECHIDXUSD) to 14.2% (XAGUSD).
- **No synthetic ordering:** Within same-timestamp records, no sequence is assigned. Original CSV row order is preserved via `source_row_ordinal`.

---

## 8. ORDERING SEMANTICS

- **Canonical order:** Chronological by `(date, time)` as strings, then by `source_row_ordinal`.
- **Source-order invariant:** The source CSV is globally non-decreasing in `(date, time)`. The converter validates this and fails-closed if violated.
- **No sorting:** The converter does NOT sort the input. Original CSV row order is preserved.
- **Out-of-order rejection:** Records with timestamps earlier than the previous record are rejected.

---

## 9. QUALITY RULES

Structural data-integrity rules (not outcome-driven filters):

| Rule | Action |
|------|--------|
| Missing bid or ask | Reject row |
| bid < 0 or ask < 0 | Reject row |
| bid == 0 or ask == 0 | Reject row |
| ask < bid | Reject row |
| Non-numeric bid/ask/last/vol | Reject row |
| Timestamp earlier than previous | Reject row |
| Null last | Preserve (nullable field) |

All rejected rows are counted and recorded in the manifest. No silent discards.

---

## 10. DERIVED VARIABLES

### Mid

- **Formula:** `mid = (bid + ask) / 2`
- **Units:** Price (same as source)
- **Precision:** float64 (IEEE 754)
- **Missing-data behavior:** Never missing (bid and ask are always present)
- **Provenance:** Mathematically derived from bid and ask

### Spread

- **Formula:** `spread = ask - bid`
- **Units:** Price (same as source)
- **Precision:** float64 (IEEE 754)
- **Missing-data behavior:** Never missing
- **Provenance:** Mathematically derived from bid and ask

---

## 11. UNSUPPORTED INFORMATION

The canonical dataset explicitly does NOT contain:

- Trade events (no event-type flag)
- Aggressor direction (no trade classification)
- Real trade volume (vol = 0)
- Order-book depth (top-of-book only)
- Trade/quote sequence separation
- Institutional positioning

**Do NOT claim these are observable from the canonical dataset.**

---

## 12. PARTITION STRATEGY

- **Structure:** `data/tick_canonical/<SYMBOL>/<YYYYMM>.parquet`
- **Partitioning:** Monthly, by `date[:6]` (YYYYMM string prefix).
- **Rationale:** Monthly partitions are large enough to avoid millions of tiny files (avg ~3M rows/partition), yet small enough for practical date-range access.
- **No random filenames.** No UUIDs. No outcome-dependent partitions.
- **Compression:** Snappy (default). Partitioned by month for practical research access.

---

## 13. PROVENANCE

Each canonical dataset includes a `manifest.json` containing:

| Field | Description |
|-------|-------------|
| symbol | Symbol name |
| schema_version | Schema version string ("V1") |
| source_file | Source CSV filename |
| source_sha256 | SHA-256 hash of entire source CSV |
| specification_sha256 | SHA-256 hash of this specification document |
| implementation_sha256 | SHA-256 hash of canonicalizer script |
| total_rows | Total rows processed |
| rejected_rows | Total rows rejected |
| duplicate_timestamp_rows | Rows with duplicate timestamps |
| bid_ask_inverted_rows | Rows rejected for ask < bid |
| negative_price_rows | Rows rejected for negative prices |
| zero_price_rows | Rows rejected for zero prices |
| null_last_rows | Rows where last is null |
| first_timestamp | First timestamp in canonical output |
| last_timestamp | Last timestamp in canonical output |
| partitions | List of partition filenames |
| partition_row_counts | Row count per partition |
| column_hashes | SHA-256 hashes of each source column's uncompressed byte arrays |
| compression | Parquet compression codec |
| elapsed_seconds | Wall-clock time for conversion |

---

## 14. REPRODUCIBILITY

- **Definition:** Two independent conversions of the same source CSV produce identical row ordering, identical parsed values, and identical column hashes.
- **Logical-level reproducibility:** Parquet physical bytes may differ due to writer metadata or compression non-determinism. Logical content is identical.
- **Verification:** Column hashes must match across runs with different compression settings.

---

## 15. VERSIONING

| Version | Date | Changes |
|---------|------|---------|
| V1 | 2026-09-07 | Initial canonical specification. 9-column schema (source_row_ordinal, date, time, bid, ask, last, vol, mid, spread). Monthly partitions. Snappy compression. |

Future schema changes require a new specification version and re-conversion from source.

---

**END OF CANONICAL TICK DATA SPECIFICATION V1**
