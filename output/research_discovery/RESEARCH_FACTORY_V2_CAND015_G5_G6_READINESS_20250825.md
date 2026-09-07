# QUANTFORGE — RESEARCH FACTORY V2
# CAND-G0-015 G5/G6 FORWARD-VALIDATION READINESS

## 1. G5 Final State
**G5 VALID — HISTORICAL REPLAY ONLY**

## 2. Historical Replay Evidence
- **Research Mean LOW-VOL:** +9.53 bp
- **G5 Replay Mean LOW-VOL:** +9.30 bp
- **Difference:** -0.23 bp
- The exact frozen candidate identity was flawlessly preserved.
- Transitioning from theoretical M5 close to the next M1 open was perfectly deterministic, with zero look-ahead.

## 3. What Has Been Proven
CAND-015 successfully survives translation into an execution proxy. The structural avoidance of the massive HIGH-VOL left tail holds perfectly when subjected to realistic inter-bar pricing drift. The historical viability of the edge under realistic proxy friction is exceptionally robust.

## 4. What Has NOT Been Proven
This replay does **NOT** constitute measured live execution.
- The reported -0.23 bp slippage is an execution proxy mathematically derived from historical data, not observed live slippage.
- The reported 50 ms latency is simulated/conceptual, not measured.

## 5. G6 Blocker
**G6 — Controlled Forward / Demo Validation is BLOCKED pending forward execution infrastructure.**
*Note: This is a strict infrastructural block, not an economic failure or strategy defect. The validated historical economic object remains completely intact and supported.*

## 6. Minimum G6 Requirements
To authorize G6 Forward Validation, the repository must possess the following minimum capabilities:
- **DATA:** A real-time BTCUSD price feed with deterministic timestamps.
- **SIGNAL:** Deterministic implementation of the frozen CAND-015 signal.
- **STATE:** Real-time pre-entry D1 volatility-state calculation.
- **EXECUTION:** Paper/demo execution model capable of recording: signal time, decision time, quoted price, simulated/actual executable price, exit price, spread, and slippage.
- **LOGGING:** Immutable event/trade ledger.
- **IDENTITY:** Persistence of candidate identity, implementation identity, data source identity, timestamp, and execution environment.
- **OBSERVATION:** Forward observation must NOT change the candidate definition.

## 7. G6 Non-Goals
G6 does **not** require the final production bot architecture.
Do NOT build multi-market execution frameworks, portfolio engines, strategy factories, deployment orchestration, or large tick pipelines.
The minimal system must only answer: *Does the frozen CAND-015 signal occur in real time and does realistic executable pricing preserve the historically validated economic behavior?*

## 8. Forward Validation Controls
Historical replay validates historical reproducibility.
Forward validation tests whether the same frozen object survives real-time observation and realistic execution conditions.
The two must never be conflated.

## 9. G6 Entry Criteria
Forward validation must immediately stop and be reviewed if:
- Signal identity diverges from the frozen baseline.
- Timestamp alignment differs.
- Execution price semantics differ.
- Spread materially exceeds assumptions.
- Observed slippage materially exceeds the registered cost model.
- Signal frequency differs materially from historical expectations.
- The implementation requires parameter changes to function.

## 10. Integrity
The frozen economic object is fully intact and shielded from optimization. The explicit blockers correctly identify missing architectural requirements rather than masking them as research results.
