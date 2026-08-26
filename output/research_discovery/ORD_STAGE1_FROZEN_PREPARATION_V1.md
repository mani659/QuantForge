# QUANTFORGE — STAGE-1 FROZEN PREPARATION (V1)
**Date:** 2026-08-24
**Purpose:** Freeze the deterministic Stage-1 preparation package to strictly bind all identities, inputs, components, and semantic constraints prior to any authorization of economic execution.

## 1. IDENTITIES

### Market
* **Market:** `XAGUSD`

### Economic Protocol
* **Protocol file:** `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_1_AMENDED.md`
* **Protocol version:** `V2.1.1 / V2.1 AMENDED`
* **SHA:** `1d3ee7a6a9fd747cb57a716b43c5eb80bb7d6016011d2c4df9f0814cc196968d`

### Input Identity
* **Source Type:** Parquet representation (from M-ORD-ECO-04-CONV-02)
* **Parquet Specification SHA:** `b71ca7689acb06f949b5457cfcb9ed4a20ebaaa80662e9c62138df02fcb4b630`
* **Converter SHA:** `c808069bccdf64be98022a311d058fb9b7e2d00518ffb6d09224884d69159470`
* **Source CSV SHA:** `edccad88ed5b74caf16a14203f3cf743306c65f2ebc5004cf566ed61deeb6e17`
* **Dataset Row Count:** `146,389,821`
* **Parquet Partitions:** 61 partitions (chronological sequence `202107` to `202607`)

### Implementation Identity
* **Stage-1 Executable Path:** `research/staged_execution/stage1.py`
* **Stage-1 Implementation SHA:** `8c6f7aad288414c68d4017fe5c7f60101b297459f81abc67d43390517d1786c6` (Post M-ORD-ECO-05A Adapter update)

## 2. PARQUET ADAPTER / MAPPING
* **Adapter Architecture:** `TickSource` interface (specifically `ParquetTickSource`).
* **Field Mapping:**
    * Parquet `date` (string) → Stage 1 `date_s` (string)
    * Parquet `time` (string) → Stage 1 `hh`, `mm`, `ss` (integers)
    * Parquet `bid` (float64) → Stage 1 `bid` (float)
    * Parquet `ask` (float64) → Stage 1 `ask` (float)
    * Parquet `last` (float64) / `vol` (float64) → Ignored
* **`source_row_ordinal`**: This column is structurally preserved in the Parquet artifact but implicitly consumed in Stage 1 via strict deterministic sequence order iteration. PyArrow `to_batches` chunking over alphabetically sorted partition files yields a chronologically monotonic stream that is byte-for-byte aligned with the original CSV ordinal order.

## 3. STAGE-1 READ PATH
The input boundary (`_stream_minutes`) dynamically binds the input string as a chronological PyArrow dataset stream:
1. Lexicographical glob of `*.parquet`.
2. PyArrow `read_table` bounded stream `to_batches(max_chunksize=100000)`.
3. Extraction of string tuples and validation.
4. Downstream chronological dispatch to invariant structural-stop detection.

## 4. FAILURE CONDITIONS
* **Out of Order Partitions:** Fails closed if partition globbing violates chronological sequence constraints.
* **Malformed Tuples:** Invalid time structures (e.g. failing to resolve 3 splits in `time` strings) yield `is_valid=False`, cleanly discarding corrupt rows akin to the legacy CSV behavior.
* **Missing `manifest.json`:** `stage1.py` fails to bind `tick_sha` transparently if the dataset identity manifest has been stripped, halting execution payload generation.

## 5. EXECUTION FIREWALL
> Stage 1 remains NOT EXECUTED.
> Stage 2 remains NOT EXECUTED.
> Economic adjudication remains NOT PERFORMED.
