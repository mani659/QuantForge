# Implementation Plan: M-ORD-ECO-02 Tick-to-Parquet Converter

## Goal Description
Implement the tick-to-Parquet converter according to `ORD_TICK_PARQUET_CONVERSION_SPECIFICATION_V2.md`, strictly on synthetic fixtures. 

## Proposed Changes

### `research/staged_execution/tick_parquet_converter.py`
1. `TickParquetConverter`: A streaming class that reads headerless CSV row-by-row.
2. It parses numerics explicitly using `float(val)` to match Stage-1 semantics.
3. **Memory Bound & Writer Lifecycle**: 
   - Processing is row-streaming in fixed chunk sizes (e.g. 100,000 rows).
   - Only **ONE** `ParquetWriter` is open at a time.
   - The converter assumes chronological ordering. When the partition `<YYYYMM>` changes, the current writer is closed, and a new one is opened. 
   - If a row arrives for an older, already closed partition, it raises an `EXECUTION-INFRASTRUCTURE FAILURE` (fail closed to guarantee single-pass bounded memory).
4. **Canonical Column Hashes**:
   - Computes **per-column sequential hashes** using 7 separate SHA-256 hashers.
   - Exact Canonical Byte Serialization:
     - `source_row_ordinal`: Little-endian signed INT64 (`struct.pack('<q', val)`)
     - `date`: UTF-8 with 4-byte unsigned little-endian length prefix (`struct.pack('<I', len(val)) + val.encode('utf-8')`)
     - `time`: UTF-8 with 4-byte unsigned little-endian length prefix
     - `bid`, `ask`, `vol`: IEEE-754 binary64 little-endian (`struct.pack('<d', val)`)
     - `last`: 1 byte tag `b'\x00'` if NULL. If VALUE, `b'\x01'` followed by `struct.pack('<d', val)`.
5. Outputs a deterministic manifest containing source hashes, column hashes, and partition lists.

### `tests/test_tick_parquet_converter.py`
- **Test A**: Basic valid tick conversion.
- **Test B**: Duplicate timestamps preserved correctly.
- **Test C**: `source_row_ordinal` starts at 0 and is contiguous.
- **Test D**: Numeric equivalence (`parquet == float(csv_string)`) using edge-case decimal strings.
- **Test E**: Nullable `last` field testing (both valid floats and empty string nulls).
- **Test F**: Verification of correct partitioning (`<market>/<YYYYMM>.parquet`).
- **Test G**: Canonical reproducibility (identical canonical hashes across two runs).
- **Test H**: Physical byte independence (run with different pyarrow compression `SNAPPY` vs `NONE`, expect different file physical SHAs but identical canonical hashes).
- **Test I**: Malformed inputs raise `RuntimeError` labeled as infrastructure failure.
- **Test J**: Memory behavior. Create a synthetic CSV with 500,000 rows. Use `tracemalloc` to measure peak memory usage during conversion. Verify that peak memory is bounded (e.g., < 20MB) and does not scale proportionally with the 500,000 rows.
- **Firewall**: Ensure the converter throws an error if asked to read from the production tick directory.

### `output/research_discovery/ORD_TICK_PARQUET_CONVERTER_IMPLEMENTATION_AUDIT_V1.md`
The final required report mapping the implementation back to the V2 specification.
