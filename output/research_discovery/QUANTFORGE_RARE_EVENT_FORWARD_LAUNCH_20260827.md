# QUANTFORGE — RARE-EVENT FORWARD LAUNCH
# CAND-024 / CAND-035
# DATE: 2026-08-27

## 1. Launch Authorization
The Rare-Event Component Forward Qualification track for CAND-024 and CAND-035 has been explicitly authorized and launched on prospective paper trading infrastructure. System Assembly, optimization, and combined testing remain strictly forbidden.

## 2. Frozen Contracts
- **CAND-024:** Friday Afternoon Positional De-Risking
- **CAND-035:** Month-End Final-Hour Imbalance Acceleration

## 3. Contract Hashes
- **CAND-024:** `CAND-024:1.0:c49c5bb0`
- **CAND-035:** `CAND-035:1.0:a7c2132d`

## 4. CAND-024 Track
- **Status:** FORWARD OBSERVATION ACTIVE
- **Target Event Count:** 3 minimum / 5 preferred

## 5. CAND-035 Track
- **Status:** FORWARD OBSERVATION ACTIVE
- **Target Event Count:** 3 minimum / 5 preferred

## 6. Paper Execution Safety
A strict firewall ensures:
- NO REAL ORDER API
- NO DEMO ORDER SUBMISSION
- NO LIVE ORDER SUBMISSION
All execution is mocked entirely locally, simulating fixed spread and friction assumptions (2.0 points for USATECHIDXUSD).

## 7. Event-Count Requirements
The primary qualification threshold is event count, not calendar time.
- **Minimum:** 3 qualifying events per candidate.
- **Target:** 5 qualifying events per candidate.

## 8. Event Identity
Events are logged with an immutable deterministic ID derived from the date and sequence, mapped directly to the frozen contract hash. Duplicate triggers are structurally prohibited by engine rules.

## 9. Detection Protocol
The `event_ledger.jsonl` tracks states transparently (WATCHING, EVENT_DETECTED, PAPER_IN_POSITION, MISSED, INVALIDATED, COMPLETED).

## 10. Outcome Protocol
The `outcome_ledger.jsonl` tracks strictly post-execution results (gross, net, friction) and operates strictly downstream of event detection logic.

## 11. Fail-Closed Behavior
Any data ambiguity or session parsing failure defaults immediately to INVALIDATED or NO EVENT. The runner will not hallucinate events or fill in gaps.

## 12. Session / DST Integrity
The system employs precise `America/New_York` timezone calculations for market hours and handles all DST/EST/EDT offsets deterministically without hardcoded UTC offsets.

## 13. Restart / Reconciliation
The runner restores state from the durable JSONL ledgers upon boot. Reconnects follow an exponential backoff curve (1s → 30s) to gracefully weather temporary feed outages.

## 14. Module Independence
CAND-024 and CAND-035 do not communicate. They run in isolated event engines orchestrated by the same host.

## 15. CAND-015 Independence
The CAND-015 runner and its active 7-day forward observation are completely protected, unmodified, and isolated from this launch.

## 16. System Assembly Exclusion
System Assembly has NOT been executed. These components are being validated as standalone rare events.

## 17. Launch Timestamp
2026-08-27T12:17:28+03:00

## 18. Current Event Counts
- **CAND-024:** 0 / 3 min / 5 target
- **CAND-035:** 0 / 3 min / 5 target

## 19. Current Operational Health
Observation is ACTIVE. Background daemon launched successfully. Heartbeat is logging correctly to `health.jsonl`.

## 20. Integrity
The observation has been launched on exact frozen heuristics without any adjustments for frequency or profitability optimization.
