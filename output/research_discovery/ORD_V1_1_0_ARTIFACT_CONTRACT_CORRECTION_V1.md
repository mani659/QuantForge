# QUANTFORGE — ORD V1.1.0
# HALT-AWARE ARTIFACT CONTRACT / FINALIZATION CORRECTION

## 1. Defect
The `EventStudyRecorder` previously used a completely static expected artifact list that failed to account for legitimately halted markets, treating their correctly omitted artifacts as failures. Furthermore, the recorder did not automatically whitelist its own internal infrastructure artifacts (`execution_heartbeat.json`, `process_identity.json`), flagging them as unexpected.

## 2. Why BTCUSD Halt Is Legitimate
BTCUSD encountered 218 invalid days (an invalid fraction of 0.1195), triggering the pre-registered >10% anomaly threshold defined in the V1.1.0 protocol. The protocol explicitly requires execution to HALT inference for the offending market. Consequently, generating statistical bootstrap and empirical null arrays for BTCUSD is scientifically and mechanically prohibited by the protocol itself. The absence of these arrays is exactly what the protocol expects.

## 3. Scientific vs Infrastructure Artifacts
To resolve the contradiction between strict finalization and legitimate omission, the artifact contract has been explicitly separated into two models:
- **Scientific Expected Artifacts**: Files whose expected presence is governed by the actual completion status of each market.
- **Infrastructure Expected Artifacts**: Internal lifecycle files generated and owned unconditionally by the `EventStudyRecorder`.

## 4. Finalization Contract
The finalization contract is now dynamic but remains fully deterministic and strict:
- **Successful Market**: Bootstrap and empirical null arrays are strictly required. Missing them results in `INVALIDATED`.
- **Legitimately Halted Market**: Bootstrap and empirical null arrays are correctly omitted. The omission is accepted (`COMPLETED`).
- **Unexpected Foreign File**: Any unrecognized file from any source triggers `INVALIDATED`.
- **Recorder Infrastructure**: Properly whitelisted, satisfying the `COMPLETED` strictness.

## 5. Recorder-Owned Files
The following files are now deterministically claimed by the `EventStudyRecorder` as infrastructure artifacts:
- `execution_journal.json`
- `implementation_manifest.json`
- `execution_manifest.json`
- `execution_heartbeat.json`
- `process_identity.json`

## 6. Halt-Aware Market States
`run_ord_v1.py` now resolves the final expected scientific artifacts dynamically at the conclusion of the execution but strictly before finalization. The `market_status` map (declaring each market as `COMPLETED` or `HALTED`) dictates whether the statistical arrays are demanded by the recorder. This `market_status` mapping is explicitly recorded in `execution_manifest.json`.

## 7. Tests
A focused test suite (`tests/test_artifact_contract_correction.py`) was created and executed alongside the full repository test suite.
Command: `python -m pytest tests/ -q`
Result: `648 passed in 10.27s`

The 7 focused infrastructure tests specifically proved that the strictness bounds are preserved: foreign files crash the runner, failed market masquerades crash the runner, while legitimately halted markets pass peacefully.

## 8. Scientific Firewall
The frozen ORD protocol, definition lock, event logic, statistical bootstrap, empirical null logic, confidence intervals, Holm adjustments, and classification mechanics remain absolutely untouched. No scientific behavior was modified.

## 9. Current Invalidated Execution
The current execution `EXECUTION_20260818T134028Z_e6d8fd0c-a3ab-48c9-b356-027686f4d895` has NOT been modified or reclassified by this correction task. It remains preserved exactly as it was, with its terminal state set to `INVALIDATED`.

## 10. Next Independent Audit
The exact next task is the **ORD V1.1.0 ARTIFACT CONTRACT CORRECTION INDEPENDENT AUDIT**.
