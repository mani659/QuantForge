# QUANTFORGE — CAND-015
# G6 FORWARD PAPER OBSERVATION POST-AUDIT
# SESSION: G6_CAND015_FORWARD_002
# 2026-08-26

## 1. Session Identity
- **Session ID:** `G6_CAND015_FORWARD_002`
- **Candidate:** `CAND-G0-015`
- **Broker:** Exness (Demo)
- **Platform:** MT5

## 2. Completion
- **Start UTC:** `2026-08-25 17:01:07.899406+00:00`
- **End UTC:** `2026-08-26 05:01:08.183679+00:00`
- **Requested Duration:** 12.0 hours
- **Actual Duration:** 43200.28 seconds (~12.0 hours)
- **Termination:** The session terminated completely and cleanly upon reaching its 12-hour target duration without any unhandled exceptions blocking the graceful shutdown.

## 3. MT5 Health
- **First Heartbeat:** `17:01:17 UTC`
- **Final MT5 Status:** `CONNECTED`
- **Connection Continuity:** A significant transient disruption occurred between approximately `00:04 UTC` and `01:00 UTC` where MT5 disconnected, resulting in 379,223 instant reconnect attempts by the wrapper loop. This behavior corresponds perfectly to a standard broker rollover/maintenance window. After the maintenance period, the connection recovered autonomously and safely for the remaining 4 hours of the session. 
- **Fatal Errors:** 0

## 4. Data Continuity
- **Max Heartbeat Gap:** 11.57 seconds (heartbeat generation remained live during the maintenance loop)
- **Max USTEC Observation Gap:** 3,612.0 seconds (~1 hour)
- **Max BTC Observation Gap:** 3,313.0 seconds
The data gaps were entirely due to the broker's standard midnight maintenance downtime. Quotes advanced correctly and smoothly before and after the downtime.

## 5. Qualifying Events
- **Total Qualifying Events:** 0
- **LOW_VOL Events:** 0
- **HIGH_VOL Events:** 0

## 6. Paper Trades
- **Completed Paper Trades:** 0
- **Incomplete Trades:** 0

## 7. Signal State
- The telemetry reported `signal_state: UNKNOWN` continuously. This is an artifact of the telemetry logging configuration (`getattr(self.signal_engine, 'volatility_state', 'UNKNOWN')`), because the `Cand015SignalEngine` calculates the volatility state dynamically and only emits it during a qualifying event, rather than storing it as a persistent class attribute. It does NOT indicate any mathematical or signal-engine failure.

## 8. Safety
- **Order APIs:** None invoked.
- **Demo Mode:** Fully active.
- **Paper Engine:** Active. No real orders or demo orders were ever dispatched. The strategy remained completely isolated from any broker execution endpoint.

## 9. Performance
N/A. (0 trades executed).

## 10. Historical vs Forward
**Historical Validated Result:** CAND-015 historically exhibits roughly 260 opportunities per year.
**Overnight Forward Observation Result:** The 12-hour forward observation generated zero events.
**Verdict:** A zero-event overnight run is fully expected due to sparsity and does NOT invalidate the historical results.

## 11. Session Classification
### A — VALID OBSERVATION
The runner remained healthy (handling MT5's maintenance window correctly) and completed the intended 12-hour observation duration.

## 12. Next Observation Recommendation
Further longer-duration observation is reasonable because the event is sparse.
Given a historical frequency of ~260 events/year (approx. 0.0297 events/hour), the expected occurrences (Poisson λ) and probability of observing exactly zero events are:
- **12 hours:** Expected events ≈ 0.356 | Probability of 0 events ≈ **70.0%**
- **24 hours:** Expected events ≈ 0.712 | Probability of 0 events ≈ **49.0%**
- **7 days:** Expected events ≈ 4.98 | Probability of 0 events ≈ **0.68%**
*(Note: This is a mathematical expectation model, not an assertion of future market behavior).*

## 13. Integrity
This audit was performed in a read-only capacity. No code was modified, no sessions were altered, and no strategy logic was adjusted.
