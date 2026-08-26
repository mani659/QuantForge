# ORD TICK PARQUET CONVERSION SPECIFICATION V2

## 1. Objective and Authority
This specification defines a lossless, deterministic, reproducible physical representation of the registered raw MT5 tick source as Parquet. This representation safely feeds the frozen Stage-1 preparation without changing the economic object.
**Authority:** The Raw MT5 tick CSV remains the immutable source-of-record. The Parquet files are derived artifacts only.

## 2. Numeric Representation
- **Original CSV Representation:** Base-10 string literals (e.g., "1954.23").
- **Current Stage-1 Parsing Semantics:** Python's built-in `float(val)` function, which casts string literals into IEEE 754 64-bit floating point numbers (float64).
- **Selected Parquet Representation:** `DOUBLE` (float64).
- **Equivalence Justification:** Parquet `DOUBLE` exactly matches the memory representation and precision of Python's `float64`. This guarantees zero divergence in economic calculation compared to Stage-1 parsing directly from CSV text. Integer scaling or `DECIMAL` types could introduce subtle floating-point rounding differences against the existing baseline implementation.
- **Verification Rule:** A unit test must assert that reading the Parquet `DOUBLE` field into a Python float equals `float(csv_string)` exactly for all edge cases (i.e. `parquet_val == float(csv_val)`).

## 3. Row Identity
- **Freeze `source_row_ordinal`:** The exact 0-indexed row position of the tick in the original CSV must be preserved as a physical column in the Parquet file.
- Duplicate timestamps must be perfectly preserved.
- The deterministic source ordering from the CSV must be exactly maintained.
- **Source-Order Invariant:** The registered raw MT5 tick source is expected to be globally nondecreasing in `(date,time)` and conversion MUST fail closed if this invariant is violated. This is a property of the REGISTERED SOURCE, not a sorting operation performed by the converter. The converter must NOT sort the input.
- **NO deduplication** of ticks is permitted under any circumstances.

## 4. Timestamp
- **Timezone:** Timestamps must remain in UTC. No timezone conversion is permitted.
- **Precision:** No precision loss is permitted. 
- **Exact representation:** The original `date` and `time` string fields will be preserved as `STRING` to guarantee zero precision loss or timezone ambiguity during parsing.

## 5. Schema
Freeze exact names, physical types, and nullability:
- `source_row_ordinal`: `INT64`, non-null
- `date`: `STRING`, non-null (Format: YYYYMMDD)
- `time`: `STRING`, non-null (Format: HH:MM:SS or HH:MM:SS.mmm)
- `bid`: `DOUBLE`, non-null
- `ask`: `DOUBLE`, non-null
- `last`: `DOUBLE`, nullable
- `vol`: `DOUBLE`, non-null

## 6. Partitioning
Freeze deterministic directory structure:
- **Structure:** `output/parquet_ticks/<market>/<YYYYMM>.parquet`
- No random filenames (e.g., no UUIDs).
- No outcome-dependent partitions (e.g., partitioning by winning/losing days).
- Partitions must be purely temporal (e.g., by month) based on the `date` string.

## 7. Conversion Memory
The converter implementation must be:
- **Streaming:** Processing the CSV row-by-row or in fixed chunks.
- **Bounded-memory:** O(1) memory complexity with respect to the total file size.
- **No full-file DataFrame:** It must not load the entire CSV into memory.
- **No unbounded accumulation:** It must write to Parquet partitions progressively.

## 8. Market-Median Compatibility
Parquet conversion must preserve ALL eligible observed minutes.
The converter MUST NOT:
- event-filter;
- pre-aggregate;
- discard non-event minutes;
- convert ticks into M1 during physical conversion.
M1 remains the authoritative event-structure source.

## 9. Provenance
The conversion process must output a manifest JSON containing:
- Source CSV SHA-256.
- Converter implementation SHA-256.
- Specification SHA-256 (this document).
- Schema version string (e.g., "V2").

## 10. Content Integrity and Reproducibility
- **Integrity evidence:** Total row count, deterministic partition inventory, and column-level hashes (e.g., hashing the uncompressed byte arrays of the columns).
- **Reproducibility definition:** "Equivalent canonical content" means two independent conversions of the same raw CSV must yield exactly identical row ordering, identical parsed values, and identical column hashes, even if the final Parquet physical file bytes differ due to writer-specific metadata or compression non-determinism.

## 11. Failure Handling
- **Classification:** Any conversion failure (e.g., out-of-memory, disk full, parse error) must be classified exclusively as an `EXECUTION-INFRASTRUCTURE FAILURE`.
- **Exclusion:** It must never be classified as an economic exclusion.
- **Behavior:** The converter must fail-closed and never silently continue with incomplete data.
