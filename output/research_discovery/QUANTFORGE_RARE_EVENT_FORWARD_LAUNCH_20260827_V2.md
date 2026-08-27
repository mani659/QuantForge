# QUANTFORGE — RARE-EVENT FORWARD LAUNCH (ACTUAL)
# CAND-024 + CAND-035
# DATE: 2026-08-27

## 1. Launch Timestamp
`2026-08-27T09:44:58Z`

## 2. Research Target
- CAND-024 (Friday De-Risking)
- CAND-035 (Month-End Imbalance)

## 3. Frozen Contracts
- CAND-024: `CAND-024:1.0:c49c5bb0`
- CAND-035: `CAND-035:1.0:a7c2132d`

## 4. Logical Symbol
`USATECHIDXUSD`

## 5. Forward Representation (Broker Symbol)
`EXNESS:USTECm`

## 6. Mapping
`MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`

## 7. Market Input
> CURRENT MT5 MARKET DATA (Read-Only)

## 8. Execution Mode
> PAPER ONLY
(No real order API, no demo order submission, no live order submission).

## 9. Qualification Bounds
- **Minimum**: 3 qualifying events (per candidate)
- **Target**: 5 qualifying events (per candidate)
- **Maximum Calendar Boundary**: 18 months

## 10. Firewalls
- **CAND-015 Isolation**: CAND-015 is explicitly protected, untouched, and its state is not shared.
- **System Assembly Exclusion**: System Assembly is NOT executed and remains prohibited pending independent forward validation of both components.

## 11. Event Ledger
`scripts/rare_events/event_ledger.jsonl` (Append-Only)

## 12. Outcome Ledger
`scripts/rare_events/outcome_ledger.jsonl` (Append-Only)

## 13. Heartbeat Ledger
`scripts/rare_events/health.jsonl` (Append-Only)

## 14. Status
The qualification clock for CAND-024 and CAND-035 has officially started. The background runner daemon is actively observing current MT5 `USTECm` data, mapped into the logical `USATECHIDXUSD` namespace for processing.
