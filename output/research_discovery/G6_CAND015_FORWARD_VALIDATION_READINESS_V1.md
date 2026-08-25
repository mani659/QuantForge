# QUANTFORGE — RESEARCH FACTORY V2
# CAND-G0-015 G6 FORWARD VALIDATION READINESS V1

## 1. Objective
The objective of this artifact is to declare the structural readiness of the minimum G6 forward observation harness for `CAND-G0-015`. The harness is designed to observe market events strictly according to the frozen economic object and log deterministically without adaptation, optimization, or live money exposure.

## 2. Frozen Identity
**Exact Binding:**
- `candidate_id`: CAND-G0-015 (Nasdaq-Crypto Information Absorption Lag)
- `shock_definition`: USATECHIDXUSD, M5, > 3 * atr_30d
- `volatility_state`: USATECHIDXUSD, D1, d1_atr < d1_atr_30d (evaluated pre-entry)
- `lockout`: 60 minutes
- `entry`: Next available quote after event completion
- `exit`: Time-based 60 minutes after decision
- `friction_bps`: 3.0 bps

The system is hard-bound to `research/g6_forward/cand015_identity.py`. Startup fails automatically if this definition is modified.

## 3. Data Feed
**Real-time/Demo Feed used:** NONE.
The `FORWARD_PAPER` mode explicitly raises `NotImplementedError` and blocks startup because no real-time data source is currently available.
The `REPLAY_TEST` mode uses local M1 CSV historical replay to validate the harness logic, but explicitly marks execution prices and latency as synthetic.

## 4. Signal Engine
**Semantics:** EXACT FROZEN CAND-015.
The `Cand015SignalEngine` aggregates ticks into M5 and D1 bars, evaluates the M5 shock exactly at bar completion, evaluates the D1 volatility state using pre-entry boundaries, and enforces the 60-minute lockout.

## 5. Event State Machine
Implemented rigidly with states: `IDLE`, `EVENT_DETECTED`, `ENTRY_PENDING`, `OBSERVED_ENTRY`, `IN_POSITION`, `EXIT_PENDING`, `OBSERVED_EXIT`, `CLOSED`. Duplicate signal events are structurally rejected.

## 6. Paper Execution
**Real Orders:** NOT POSSIBLE.
The adapter simulates entries and exits based on the next available stream quote. No broker credentials, API endpoints, or order routing paths exist.

## 7. Immutable Ledger
An append-only `EventLedger` logs every lifecycle completion to CSV. The ledger enforces strict marking of `mode`, `price_source`, `execution_price_type`, `slippage_status`, and `latency_status` to prevent conflating replay with reality.

## 8. Latency Measurement
**Status:** UNAVAILABLE (LIVE).
In `REPLAY_TEST` mode, latency is measured locally as `HARNESS PROCESSING LATENCY`. Live market latency cannot be measured until a real-time feed is connected.

## 9. Historical Parity Check
**Verdict:** PASS.
The harness has been tested against synthetic replay segments; the state transitions, lockout blocks, and execution delays mirror the G5 historical output structurally.

## 10. Safety Controls
- Default mode is restricted paper logic.
- Engine verifies frozen identity strictly on startup.
- `FORWARD_PAPER` blocks by exception.
- No `execute_real_order` capabilities exist in the source tree.

## 11. Known Limitations
1. No real-time data integration is implemented, permanently blocking `FORWARD_PAPER` mode.
2. In `REPLAY_TEST`, execution quotes default to the OHLC open and label bid/ask/spread as `unavailable`, preventing true live slippage calculation.

## 12. G6 Readiness Verdict
- **Harness Readiness:** READY
- **Forward Readiness:** BLOCKED — NO REAL-TIME/DEMO DATA SOURCE

---

# REQUIRED FINAL REPORT

### 1. G6 Status
CAND-015 REPLAY HARNESS READY
TRUE G6 FORWARD VALIDATION BLOCKED — REAL-TIME DATA SOURCE REQUIRED

### 2. Frozen Identity
Exact Binding Verified (CAND-G0-015, Version 1.0.0).

### 3. Data Feed
`FORWARD_PAPER` = None. `REPLAY_TEST` = Historical CSV.

### 4. Signal Engine
Confirm exact frozen CAND-015 semantics.

### 5. Paper Execution
Confirm no real orders are possible.

### 6. Event Ledger
Confirm immutable event/trade logging explicitly classifying `UNMEASURED_REPLAY` slippage.

### 7. Latency
Unavailable (Only Harness Processing Latency measured).

### 8. Historical Parity
PASS

### 9. Tests
- **Test A:** PASS
- **Test B:** PASS
- **Test C:** PASS
- **Test D:** PASS
- **Test E:** PASS
- **Test F:** PASS
- **Test G:** PASS
- **Test H:** PASS
- **Test I:** PASS
- **Test J:** PASS

### 10. Known Limitations
No real-time feed exists; bid/ask arrays are unavailable in M1 CSVs.

### 11. G6 Readiness
CAND-015 REPLAY HARNESS READY / TRUE G6 FORWARD VALIDATION BLOCKED

### 12. Next Milestone
**RESOLVE REAL-TIME DATA CAPABILITY**
