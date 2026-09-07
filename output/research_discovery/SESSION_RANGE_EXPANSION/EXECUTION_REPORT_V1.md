# QUANTFORGE — SESSION-ANCHORED RANGE EXPANSION V1 CONTROLLED EXECUTION REPORT

## 1. Execution identity
- Protocol Version: v1.1.3
- Date: 2026-08-17 12:11:03
- Seed: 20260817

## 2. Protocol integrity
- Protocol SHA-256: ef66f35cb9ebfefe6af91f71845b9c286a410f5d09c45b3deb633c3e8d0519f6

## 3. Dataset integrity
- Dataset SHA-256: 39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6
- Path: `USATECHIDXUSD_M1.csv`

## 4. Data-quality gates
- Total calendar days with $\ge 1$ bar: 873
- Invalid days dropped: 85
- Invalid proportion: 9.74% (Passes <10% stopping rule)

## 5. Sample counts
- Initialization days (dropped): 63
- Total primary-valid test days ($N$): 582
- COMPRESSED count: 144
- CONTROL count: 438

## 6. Observed Delta M
- **Observed $\Delta M$**: -0.004367

## 7. Bootstrap configuration
- B: 10000
- Block Expected Length ($L$): 10
- Terminate $p$: 0.1
- Truncation exactly to $N$: Yes
- Sample Unit: Day-level tuples with fixed state labels.

## 8. 95% CI
- **Two-sided 95% Percentile CI**: [-0.005533, -0.002754]

## 9. Primary verdict
**CONTRADICTED**

## 10. Chronological descriptive results
- Half 1 $\Delta M$: -0.003675
- Half 2 $\Delta M$: -0.005193

## 11. Directional secondary diagnostic
- COMPRESSED Persistence Rate: 0.5069
- CONTROL Persistence Rate: 0.5251
- Excluded exact zero-range/directionless days.

## 12. Runtime / CPU / memory profile
- Elapsed Time: 10.98 seconds
- Peak Process RSS: 204.8 MB

## 13. Reproducibility verification
- Execution completed using serial one-process architecture.
- Random state correctly seeded.
- Exact mathematics aligned with v1.1.3 specification.

## 14. Scientific interpretation
The behavioral hypothesis that pre-session range compression precedes greater cash-session range expansion magnitude is **CONTRADICTED**.
This isolates a volatility state-transition mechanic. It does **NOT** establish a profitable trading strategy, as no entry/exit spread logic was executed.

## 15. Economic firewall
- ZERO PnL
- ZERO Sharpe
- ZERO trading logic

## 16. Exact next governed task
> INDEPENDENT READ-ONLY SCIENTIFIC RESULTS ADJUDICATION

## 17. Integrity
- No ML used.
- No strategy files created.
- No tuning applied.
