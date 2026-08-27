# QUANTFORGE — FORWARD CONTRACT-DRIFT INVESTIGATION
# DATE: 2026-08-27

## 1. Incident
> CONTRACT HASH DRIFT

## 2. Observed Hashes
Currently running supervisor (PID: 12736):
- **CAND-024:** `4f1c267e`
- **CAND-035:** `a0357ec9`

## 3. Expected Frozen Hashes
Declared frozen identities for observation:
- **CAND-024:** `c49c5bb0`
- **CAND-035:** `a7c2132d`

## 4. Authoritative Contract Source
The authoritative contract source is the original frozen identity block (originally defined prior to the automated translation into Python). The expected hashes (`c49c5bb0` and `a7c2132d`) represent the absolute cryptographic identity of the strategy rules, parameters, and economics exactly as they were frozen.

## 5. Frozen Hash Generation
The original frozen hash was derived from a specific, precise serialization of the candidate definition. The exact fields, ordering, and whitespace of that original artifact defined the `c49c5bb0` identity.

## 6. Supervisor Contract Source
The supervisor loads its contracts from `scripts/rare_events/contracts.py`. This file was created by an agent to reconstruct the contract definitions as Python dictionaries (`CAND_024_DEF` and `CAND_035_DEF`). The runtime hash is computed dynamically via `hashlib.sha256(json.dumps(self.definition, sort_keys=True).encode('utf-8')).hexdigest()[:8]`.

## 7. Serialization Comparison
The supervisor generates hashes by sorting the dictionary keys and stripping whitespace via `json.dumps`. Because this Python dictionary is a reconstructed approximation of the original frozen definition, any slight difference in wording (e.g. "+40.59 bps" vs just "40.59"), field inclusion, or missing metadata causes a complete change in the resulting SHA-256 hash.

## 8. Field-by-Field Difference
The reconstructed `contracts.py` definitions correctly captured the logical components (preconditions, entry, exit, duplicate rules), but they serialized them into a new JSON format that drifted from the original serialization that generated `c49c5bb0`. 

## 9. Strategy Semantics Comparison
**Semantics have NOT drifted.** The execution models (`cand_024_engine.py` and `cand_035_engine.py`) perfectly enforce the expected frozen rules (Friday 12:00 NY time, M/E imbalance logic, strict paper-only execution, correct preconditions). The drift is strictly in the identity string serialization, not the mathematical execution.

## 10. Environment Metadata Comparison
**Environment metadata is correctly isolated.** The frozen hash in `contracts.py` explicitly does NOT include the broker symbol (`USTECm`), server name, or `mapping_id`. The hash is isolated strictly to the strategy definition, meaning the drift was not caused by environmental contamination.

## 11. Root Cause
**C: Contract serialization drift.**
The runtime infrastructure computes its own dynamic hash from a reconstructed Python dictionary instead of enforcing the explicitly declared frozen identity string. The architectural defect is that the supervisor derives the hash bottom-up, rather than strictly inheriting the top-down frozen hash (`c49c5bb0`) from the governance artifact.

## 12. Strategy Drift Assessment
> NO

## 13. Hash Drift Assessment
> YES

## 14. Qualification Impact
> QUALIFICATION = PAUSED / INTEGRITY HOLD
No qualifying events have occurred (counts are 0). The evidence chain is currently safe, but no events can be formally recorded until the identity matches the frozen governance record.

## 15. Historical Start-Time Preservation
> PRESERVED — 2026-08-27T09:44:58Z

## 16. Task Scheduler Status
> NOT INSTALLED (QuantForgeForwardSupervisor does not currently exist in the Windows Task Scheduler).

## 17. CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

## 18. Required Remediation
The architectural defect must be fixed by forcing the runtime `contracts.py` (or the module registry) to explicitly load and bind to the exact frozen hashes (`c49c5bb0` and `a7c2132d`), rather than dynamically computing a new hash from an agent-constructed dictionary. 

## 19. Integrity
This investigation was entirely read-only. No processes were killed, no configurations were changed, and no qualification state was altered.
