# QUANTFORGE — RARE-EVENT FORWARD INFRASTRUCTURE READINESS
# CAND-024 / CAND-035
# DATE: 2026-08-27

## 1. Mission
The mission of this task was to provision the dedicated, isolated forward-observation infrastructure for CAND-024 and CAND-035 in preparation for the Rare-Event Forward Qualification track, without altering the frozen research definitions or launching the actual observation.

## 2. Frozen Contract Verification
Both candidate definitions were strictly verified against their original historical artifacts (V7/V8 for CAND-024, V12 for CAND-035). The infrastructure implements the exact rules established in those documents. No "fixes", optimizations, or regime filters (like CAND-059) were applied.

## 3. CAND-024 Frozen Contract
- **ID:** CAND-024
- **Event:** Friday Afternoon Positional De-Risking
- **Preconditions:** Friday Morning High > Weekly High AND Friday 12:00 EST Open < 08:00 EST Open (Morning Exhaustion).
- **Entry:** Market order short at exactly 12:00:00 EST on USATECHIDXUSD.
- **Exit:** 15:45:00 EST.
- **Direction:** Short.
- **Economics:** ~+40.59 bps historical net.
- **Frequency:** ~4.55/year.

## 4. CAND-035 Frozen Contract
- **ID:** CAND-035
- **Event:** Month-End Final-Hour Imbalance Acceleration
- **Preconditions:** Last trading day of month AND 15:00 ET open > 09:30 ET open (Up day).
- **Entry:** Market order long at exactly 15:00 ET on USATECHIDXUSD.
- **Exit:** 16:00 ET.
- **Direction:** Long.
- **Economics:** ~+62.36 bps historical net.
- **Frequency:** ~4.09/year.

## 5. Contract Identity / Hash
To prevent semantic drift, the engine enforces immutable hashed contracts.
- **CAND-024:** Version 1.0 (Hash: Deterministic SHA-256)
- **CAND-035:** Version 1.0 (Hash: Deterministic SHA-256)

## 6. Architecture
The architecture consists of a central orchestrator (`rare_event_runner.py`) that feeds a standard Market Data Interface to two entirely independent event engines (`cand_024_engine.py` and `cand_035_engine.py`). If an engine triggers, a theoretical entry is simulated by the `paper_execution.py` firewall.

## 7. Directory Isolation
All infrastructure is strictly isolated in `scripts/rare_events/`. CAND-015's runner and logs remain entirely untouched and walled off.

## 8. Market Data Interface
The engine relies on a standardized, abstracted `quote` dictionary injected by the runner (`{"utc_timestamp", "symbol", "bid", "ask"}`). It has no direct broker dependencies, ensuring determinism.

## 9. Event Identity
Each event generates a deterministic, restart-safe ID composed of the candidate ID, the session date, and a sequence (e.g., `CAND-024-20260827-01`).

## 10. Event Ledger
An append-only `event_ledger.jsonl` securely records qualification state transitions (e.g., `EVENT_DETECTED`, `PAPER_IN_POSITION`, `INVALIDATED`). It operates completely upstream of outcome data.

## 11. Outcome Ledger
An append-only `outcome_ledger.jsonl` securely records post-trade execution data (gross, friction, net).

## 12. Paper Execution Firewall
A strict firewall ensures no real order APIs or credentials are accessible. The paper engine computes a modeled entry strictly incorporating the standard 2.0 pt USATECHIDXUSD friction.

## 13. Fail-Closed Rules
Any uncertainty regarding price, session, symbol, or timezone results in the engine defaulting to `INVALIDATED` or `WATCHING`, preventing synthetic trade fabrication.

## 14. Calendar / Timezone Integrity
All internal session logic strictly utilizes the `America/New_York` timezone for EST/EDT and DST boundary safety. The system does not rely on static UTC offsets for local session gates.

## 15. Heartbeat
Low-noise heartbeat logging writes to `health.jsonl` periodically, tracking uptime, connection state, and current candidate state.

## 16. Reconnect
Bounded exponential backoff is implemented (1s → 30s max) to ensure graceful degradation during data outages, avoiding rapid-fire unthrottled reconnect loops.

## 17. Crash / Restart Reconciliation
The runner uses a deterministic date/session mechanism so that a crash during the week/month does not result in duplicate events firing upon restart.

## 18. Event-Count Tracking
- **Minimum:** 3 qualifying events.
- **Target:** 5 qualifying events.

## 19. Module Independence
CAND-024 and CAND-035 do not share state, do not suppress one another, and are not aggregated into a portfolio equity curve.

## 20. Future Information Preservation
The runner's architecture permits time-stamped preservation for future overlap analysis (System Assembly) without contaminating the current qualification run.

## 21. Testing
A suite of pytest unit tests ensures contract stability, state initiation, duplicate prevention, and reconnect logic operate as intended. 

## 22. Smoke Test
A local synthetic smoke test successfully booted the runner, verified state reconciliation, and demonstrated a clean shutdown (SIGINT) without submitting live orders.

## 23. Launch Readiness
**INFRASTRUCTURE READY — OBSERVATION NOT LAUNCHED**

## 24. Known Limitations
The exact holiday/early-close calendar integration relies on standard datetime heuristics; external calendar feed injection is required for the final production runner.

## 25. Integrity
No original research files were modified. No filters were optimized. The historical integrity is perfectly maintained.
