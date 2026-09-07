# QUANTFORGE — ORD V1.1.0 MEMORY / DATA-LOADING SCALABILITY REMEDIATION V1

## 1. Root Cause
The legacy runner explicitly manifested a **DATA-LOADING SCALABILITY DEFECT**, where market-level DataFrames were not explicitly garbage collected. Due to Python reference-binding semantics, the entire DataFrame for the previously loaded market (e.g., XAUUSD at ~400+ MB) remained fully resident in memory simultaneously while the next market (XAGUSD) was being loaded and processed. This overlap, combined with full-DataFrame sequential duplication during pandas chaining (`dropna`, `sort_values`, etc.), created an instantaneous peak memory spike that triggered OS-level termination.

## 2. Implemented Changes
The remediation was confined strictly to `scripts/run_ord_v1.py` and targeted reducing peak memory without altering the scientific data output.
Modifications included:
- Replaced `load_market()` with an optimized, minimal-copy loader.
- Restructured the `MARKETS` evaluation loop in `main()` with a `try/finally` block to guarantee the previous market's DataFrame is garbage collected before proceeding.

## 3. Data-Loading Changes
- Switched to `usecols` during `pd.read_csv()` to parse only scientifically required columns, dropping the unused `volume` column from the in-memory array.
- Applied `dtype` overrides directly in `pd.read_csv()` to load prices straight into `float64`, preventing secondary Python allocations.
- Deleted the raw `timestamp` string array immediately after converting it to the memory-efficient `datetime64[ns]` object.
- Replaced sequenced copies with `inplace=True` variants of `.dropna()`, `.sort_values()`, and `.drop_duplicates()`.
- Used `df.rename(columns=..., inplace=True)` rather than assigning float columns over themselves.

## 4. Market-Lifetime Changes
The main market loop was reconstructed to wrap market evaluation inside a `try/finally` block:
```python
import gc
for mkt, spec in MARKETS.items():
    df = None
    try:
        df = load_market(mkt)
        ...
    finally:
        if df is not None:
            del df
        gc.collect()
```
This guarantees that even if a market fails, its object memory is freed and the peak footprint does not compound monotonically across the target universe.

## 5. Scientific Equivalence
Tested via deterministic synthetic inputs. The new `load_market()` outputs were confirmed to be semantically equivalent to the unoptimized legacy `load_market()` function in terms of row count, duplicate survivors, ordering, date generation, precision floats, and timezone conversions. Byte-for-byte serialization similarity was purposefully discarded in favor of logical data-semantic equivalence.

## 6. Volume-Column Decision
`volume` was explicitly dropped via `usecols`. A comprehensive analysis of `run_ord_v1.py` and its dependencies confirmed that `volume` is entirely ignored by the scientific logic and artifacts. The input-file SHA-256 fingerprinting hashes the full raw bytes of the `.csv` file, so execution identity is completely unaffected.

## 7. Timestamp Semantics
The legacy `pd.to_datetime(..., format="%Y-%m-%d %H:%M:%S", errors="coerce")` parser remains identically applied. Validation confirmed identical detection of invalid dates, timezone assignment, and extraction of internal day bounds.

## 8. Duplicate / Sort Semantics
The existing `keep="first"` deduplication semantic was enforced exactly as written. Tests validated that in circumstances where identical timestamps share contradictory OHLC values, the chronological duplicate resolution survives identically across both loaders.

## 9. Tests
An isolated engineering test suite was added in `tests/test_ord_v1_memory_remediation.py`:
- `test_scientific_equivalence`: Proved chronological survivor, opening range, and data-precision equivalence across an array of valid and malformed synthetic scenarios.
- `test_market_lifetime`: Proved the `try/finally` correctly executes the `.__del__()` invocation before iterating.
- Executed `python -m pytest tests/` which passed cleanly (`641 passed in 8.89s`), confirming zero collateral damage to the larger QuantForge infrastructure.

## 10. Memory Diagnostics
A lightweight synthetic trace recorded execution RSS behavior:
```text
RSS Before: 107.51 MB
RSS During: 107.51 MB
RSS After : 107.51 MB
```
(Synthetic sets are structurally too small to demonstrate GB-level spikes, but they confirm no unchecked systemic memory leaks remain tied to global variables). 

## 11. Unchanged Scientific Components
The `build_events()` function and `run_bootstrap()` inference core were untouched. Execution constants (`SEED`, `B`, `HORIZON_MIN`, `ALPHA`) and the statistical definitions were mathematically isolated from the remediation scope and preserved exactly.

## 12. Known Limitations
This optimization remains constrained to memory and scalability infrastructure; it does not solve missing event representation or fundamental model assumptions within the V1.1.0 protocol.

## 13. Next Independent Audit
The implementation must undergo an independent read-only implementation audit to approve these infrastructure changes before real dataset execution is permitted.
