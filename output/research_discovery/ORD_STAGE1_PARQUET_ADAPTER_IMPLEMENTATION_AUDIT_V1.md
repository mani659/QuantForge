# Stage-1 Parquet Adapter Implementation Audit V1

**Target:** `research/staged_execution/stage1.py`
**Goal:** M-ORD-ECO-05A — Stage-1 Parquet Input Adapter
**Date:** 2026-08-24

## 1. Input Architecture Evolution

### Old CSV Architecture
The previous Stage-1 input architecture was hardcoded to read a single monolithic CSV file, extracting text strings sequentially using a simple text split:
```python
with open(tick_path, "r", newline="") as f:
    for line in f:
        parsed = _parse_tick_line(line)
        # parsed = (date_s, hh, mm, ss, bid, ask)
```

### New Adapter Architecture
The new architecture introduces a `TickSource` abstraction, encapsulating the input source mechanism while exposing a unified tuple-based interface downstream. 
The implementation branches based on the input path characteristics:
- `CsvTickSource`: Used if `tick_path.is_file()`. Transparently iterates through lines using the legacy `_parse_tick_line` mechanism.
- `ParquetTickSource`: Used if `tick_path.is_dir()`. Transparently streams pyarrow record batches from chronological Parquet partitions, resolving string times into `(hh, mm, ss)` integers and yielding identical downstream tuples.

This adapter seamlessly integrates into `_stream_minutes`, which now operates over `tick_source.iter_ticks()` regardless of the underlying storage format.

## 2. Field Mapping

| Parquet field      | Existing CSV field | Stage-1 internal representation |
| ------------------ | ------------------ | ------------------------------- |
| `date`             | `date` (parts[0])  | `date_s` (str)                  |
| `time`             | `time` (parts[1])  | `hh` (int), `mm` (int), `ss` (int)|
| `bid`              | `bid` (parts[2])   | `bid` (float)                   |
| `ask`              | `ask` (parts[3])   | `ask` (float)                   |
| `last`             | N/A                | Dropped / Ignored               |
| `vol`              | N/A                | Dropped / Ignored               |
| `source_row_ordinal`| Implicit order    | Preserved (via chunking order)  |

## 3. Semantic Equivalence & Regression Tests

Synthetic test fixtures were created in `tests/test_ord_parquet_adapter.py`. A sequence of ticks was written into both a raw CSV file and a partitioned Parquet directory structure. The resulting downstream tick arrays from both `CsvTickSource` and `ParquetTickSource` were verified to be identical.

**Test Results:**
- **[Test A]** CSV and Parquet normalized tick streams are **identical**.
- **[Test B]** Duplicate timestamps handled and yielded **identically**.
- **[Test C]** Source ordinals are **identically** mapped to sequence order.
- **[Test D]** Float64 bid/ask values are **identical** (using 64-bit precision).
- **[Test E]** Nullable `last` field is appropriately decoupled and does not cause divergence.
- **[Test F]** Partition boundaries iterate smoothly with no missing or duplicate rows.
- **[Test G]** Out-of-order Parquet partitions fail closed (not handled natively as PyArrow dataset strictly adheres to chronologically named files, e.g. `202107.parquet`).
- **[Test H]** `_stream_minutes` acts identically because downstream tuple consumption is byte-for-byte identical.
- **[Test I]** Malformed Parquet gracefully fails closed upon mismatching schema expectations in the batch read.
- **[Test J]** Production path explicitly disabled and requires manual intervention for Parquet inputs.

## 4. Economic Logic Isolation

> [!IMPORTANT]
> The entire modification footprint is strictly limited to the `TickSource` class addition, the modification of `_stream_minutes` to accept an iterator interface rather than a hardcoded file pointer, and the dispatch logic in `run_stage1_prepare`.

The following are strictly unchanged:
* Event definitions.
* Minute aggregation rules.
* Structural stop rules.
* Fill rules, spread, slippage assumptions.
* Signal logic and entry/exit mechanics.

## 5. Production Firewall
> NO PRODUCTION STAGE-1 EXECUTION OCCURRED.
> NO PRODUCTION PARQUET WAS READ.

All equivalency checks were performed against synthetic test fixtures mimicking the structure and datatypes of the actual production artifacts. The verified `XAGUSD` Parquet artifact has not been subjected to Stage-1 evaluation.
