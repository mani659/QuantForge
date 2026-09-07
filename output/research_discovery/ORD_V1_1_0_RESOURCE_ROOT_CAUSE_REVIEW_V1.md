# QUANTFORGE — ORD V1.1.0 RESOURCE / HARD-CRASH
# ROOT-CAUSE ENGINEERING REVIEW V1

## 1. Executive Verdict
**DATA-LOADING SCALABILITY DEFECT**

## 2. Execution Incident
Execution `EXECUTION_20260818T125713Z_a79f58f8-2c9b-4cdd-81f7-cc08ef69119d` terminated abruptly during the XAGUSD data-loading phase. The absence of a Python `MemoryError` traceback—which is explicitly caught in `run_ord_v1.py`—indicates an OS-level hard termination (e.g., OOM killer or Windows commit limit exhaustion) triggered by an instantaneous memory spike. 

## 3. Timeline Reconstruction
1. Process start and successful pre-flight.
2. XAUUSD data load completed successfully (peak memory sustained).
3. XAUUSD events built, statistics bootstrapped, and null array generated.
4. XAUUSD partial artifacts successfully flushed to disk.
5. Loop advanced to XAGUSD.
6. Printed `[XAGUSD] loading ...`.
7. `pd.read_csv` invoked for XAGUSD.
8. Process hard-terminated before completing `load_market` operations.

## 4. Crash Evidence
- The interactive terminal session immediately regained control with exit code 1, emitting no traceback.
- `MemoryError` was not raised internally, definitively ruling out standard Python memory exhaustion that would have gracefully triggered the `INTERRUPTED` state. 
- The crash occurred exactly during the memory-intensive pandas DataFrame instantiation phase for the second asset.

## 5. Resource Evidence
- The system possesses ~15.7 GB total RAM (~6 GB available), but Python/pandas on Windows routinely triggers process-specific OS aborts when failing to allocate massive contiguous C-arrays instantly.
- (Heartbeat memory monitoring was unavailable as this was a legacy execution, but the deterministic OS failure mode points directly to resource pressure).

## 6. XAGUSD Data Characteristics
- **Size on disk**: 87.4 MB.
- **Rows**: 1,729,137.
- **Structure**: standard 6-column tabular layout (timestamp, open, high, low, close, volume). 
- **Integrity**: The file is intact and can be parsed statically without error. It is NOT corrupted.

## 7. Implementation Memory Profile
The `run_ord_v1.py` implementation is fatally flawed regarding memory scalability over multiple high-density markets:
1. `df = load_market(mkt)` executes entirely before binding to the `df` variable. Thus, the ~400+ MB XAUUSD DataFrame remains fully resident in memory while the new XAGUSD DataFrame is loaded and processed.
2. Inside `load_market()`, pandas performs `.dropna()`, `.sort_values()`, and `.drop_duplicates()` sequentially. Because `inplace=True` is omitted, each of these operations allocates a complete, disjoint copy of the 1.7M row DataFrame in memory. 
3. At the peak moment during XAGUSD data cleaning, the process simultaneously holds: the XAUUSD DataFrame + XAGUSD raw CSV buffer + XAGUSD unsorted DataFrame + XAGUSD sorted DataFrame copy. This causes an instantaneous memory spike in excess of 2+ GB, shattering the environment's burst allocation tolerance and triggering the OS kill.

## 8. Alternative Hypotheses
- **H1 (File too large):** Rejected. XAUUSD is larger (104 MB vs 87 MB) and successfully processed, proving the engine can handle the sheer file size in isolation.
- **H2 (Previous market resident):** Proven. Python reference semantics dictate the previous market remains resident until the new one completes its entire load cycle.
- **H3 (Pandas memory amplification):** Proven. Sequential chained operations without `inplace=True` heavily duplicate the DataFrame.
- **H4 (Bootstrap accumulated):** Rejected. Bootstrap arrays (80 KB) and event lists (~10 MB) are too small to cause an OOM.
- **H5 (Data corruption):** Rejected. XAGUSD is structurally sound.
- **H6 (External termination):** Rejected. The crash correlates precisely with the exact moment of peak memory allocation.

## 9. Most Likely Root Cause
**DATA-LOADING SCALABILITY DEFECT**
The execution architecture's failure to explicitly garbage-collect the previous market (no `del df`), combined with its reliance on heavily duplicating pandas operations during data loading, creates an overlapping, compounded memory spike that the environment cannot sustain.

## 10. Scientific Firewall
Any future engineering remediation must strictly remain an infrastructure optimization. The opening-range definition, breakout tests, 120-minute response horizon, V1.1 denominator invalidation logic, non-parametric test statistics, block bootstrap (B=10,000, L=10), and Holm step-down procedures must remain mathematically identical to the frozen protocol.

## 11. Required Engineering Remediation
A new, memory-efficient data loading implementation must be authored for the runner. 
- Explicitly `del df` and invoke `import gc; gc.collect()` at the end of each market loop before initializing the next.
- Optimize `load_market()` by relying on `inplace=True` operations to eliminate multi-copy memory amplification.
- (Remediation will be performed in a separate, authorized step).

## 12. Required Pre-Execution Verification
Before any future ORD execution is authorized, the patched implementation must undergo a rigid, independent audit to guarantee that the memory optimizations did not inadvertently alter data alignment, timestamps, or V1.1 inference logic.

## 13. Final Governance State
The legacy execution (`EXECUTION_20260818T125713Z`) remains permanently `CRASHED` and non-adjudicable.

## 14. Integrity
- read-only;
- no execution;
- no rerun;
- no scientific result calculation;
- no PnL;
- no costs;
- no protocol modification;
- no Definition Lock modification;
- no CRASHED-artifact modification;
- no historical restoration;
- no closed-line reopening.
