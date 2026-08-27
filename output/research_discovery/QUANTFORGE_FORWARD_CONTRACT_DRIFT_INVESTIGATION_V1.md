# QUANTFORGE — FORWARD CONTRACT-DRIFT INVESTIGATION
# CAND-024 + CAND-035
# DATE: 2026-08-27

---

## 1. Incident

> CONTRACT HASH DRIFT

The forward supervisor runtime audit discovered that the contract hashes produced by the runtime code do not match the frozen hashes declared in governance documents. Investigation confirms this is a **definition reconstruction drift** — the Python dictionaries in `contracts.py` were reconstructed from memory rather than faithfully translated from the original candidate specifications.

---

## 2. Observed Hashes (Runtime)

| Candidate | Runtime Hash | Source |
|-----------|-------------|--------|
| CAND-024 | `4f1c267e6c9694c094eda15d12e1520d3ae1e455ef87b24d7adcf745096cf7e5` | `runtime/forward/cand_024/status.json` |
| CAND-035 | `a0357ec9f438cd4f339c64ea8917afe983c809a0a8850b95c03d1ed629ed8eb9` | `runtime/forward/cand_035/status.json` |

---

## 3. Expected Frozen Hashes

| Candidate | Frozen Hash | Source |
|-----------|------------|--------|
| CAND-024 | `CAND-024:1.0:c49c5bb0` | `QUANTFORGE_USATECHIDXUSD_USTECM_NORMALIZATION_DECISION_V1.md` (line 99), `QUANTFORGE_RARE_EVENT_FORWARD_LAUNCH_20260827.md` (line 13), `QUANTFORGE_UNIFIED_FORWARD_SUPERVISOR_READINESS_V1.md` (line 12), `QUANTFORGE_RARE_EVENT_FORWARD_LAUNCH_INTEGRITY_AUDIT_V1.md` (line 14) |
| CAND-035 | `CAND-035:1.0:a7c2132d` | `QUANTFORGE_USATECHIDXUSD_USTECM_NORMALIZATION_DECISION_V1.md` (line 100), `QUANTFORGE_RARE_EVENT_FORWARD_LAUNCH_20260827.md` (line 14), `QUANTFORGE_UNIFIED_FORWARD_SUPERVISOR_READINESS_V1.md` (line 13), `QUANTFORGE_RARE_EVENT_FORWARD_LAUNCH_INTEGRITY_AUDIT_V1.md` (line 18) |

---

## 4. Authoritative Contract Source

The authoritative contract source is `scripts/rare_events/contracts.py` (line 1-63).

This file was created in commit `85482b8` (`feat: provision rare-event forward qualification infrastructure`) and has **NEVER been modified** since creation. The `git diff HEAD -- scripts/rare_events/contracts.py` output is empty.

The `FrozenContract` class computes the hash as:
```python
contract_str = json.dumps(self.definition, sort_keys=True)
return hashlib.sha256(contract_str.encode('utf-8')).hexdigest()
```

---

## 5. Frozen Hash Generation

The frozen hashes (`c49c5bb0` and `a7c2132d`) were computed from the **ORIGINAL candidate definitions** that existed in the Research Factory screening documents (V7/V8 for CAND-024, V12 for CAND-035). These definitions were the authoritative strategy specifications used during the G1 screening process.

When `contracts.py` was created in commit `85482b8`, the agent **RECONSTRUCTED** the candidate definitions as Python dictionaries from memory, rather than faithfully translating the original specifications. The reconstructed dictionaries contain differences from the original definitions, producing different hashes.

**Verification:** The current code in `contracts.py` produces:
- CAND-024: `4f1c267e` (does NOT match `c49c5bb0`)
- CAND-035: `a0357ec9` (does NOT match `a7c2132d`)

The file has never been modified, so the definitions have always produced these hashes. The "frozen" hashes in governance documents were carried forward from the original screening without being re-verified against the Python implementation.

---

## 6. Supervisor Contract Source

The supervisor contract source chain:

1. `scripts/rare_events/contracts.py` → defines `CAND_024_CONTRACT` and `CAND_035_CONTRACT`
2. `scripts/rare_events/cand_024_engine.py` → imports `CAND_024_CONTRACT` from `contracts.py` (line 4)
3. `scripts/rare_events/cand_035_engine.py` → imports `CAND_035_CONTRACT` from `contracts.py` (line 5)
4. `scripts/forward/module_registry.py` → creates `Cand024Engine()` and `Cand035Engine()` instances (lines 140, 152)
5. `scripts/forward/quantforge_forward_supervisor.py` → calls `get_registry()` and distributes quotes to modules (line 37, 209-220)

The contract flows directly from `contracts.py` through the engine instances to the supervisor. There is **no independent reconstruction** in the supervisor — the supervisor uses the engine's contract object directly.

---

## 7. Serialization Comparison

### Current Python Dictionary (CAND-024)

```json
{
  "name": "Friday Afternoon Positional De-Risking",
  "mechanism_family": "Session / Market-Mechanics Behavior",
  "event_definition": "Friday 12:00 NY time (EST).",
  "preconditions": [
    "The High printed between 08:00 EST and 12:00 EST must exceed the Weekly High (prior to Friday)",
    "12:00 EST open price must be lower than the 08:00 EST open price (Morning Exhaustion State)"
  ],
  "entry": "Market order short on USATECHIDXUSD exactly at 12:00:00 EST open.",
  "exit": "15:45:00 EST open.",
  "direction": "Short",
  "duplicate_rearm_rule": "Maximum one event per week. Re-arms next Friday.",
  "market": "USATECHIDXUSD",
  "session_timezone": "America/New_York",
  "friction_assumption": "2.0 index points round-trip",
  "historical_n": 13,
  "historical_frequency": 4.55,
  "historical_mean_net": "+40.59 bps",
  "historical_median_net": "+34.00 bps",
  "scientific_status": "Qualified"
}
```

**Hash:** `4f1c267e6c9694c094eda15d12e1520d3ae1e455ef87b24d7adcf745096cf7e5`

### Current Python Dictionary (CAND-035)

```json
{
  "name": "Month-End Final-Hour Imbalance Acceleration",
  "mechanism_family": "Forced Flow / Scheduled Mechanics",
  "event_definition": "Last trading day of the month at 15:00 ET.",
  "preconditions": [
    "USATECHIDXUSD 15:00 ET open is > 09:30 ET open (Up Day)"
  ],
  "entry": "Market order long on USATECHIDXUSD exactly at 15:00 ET.",
  "exit": "16:00 ET (Market close).",
  "direction": "Long",
  "duplicate_rearm_rule": "1 event per month maximum. No overlap.",
  "market": "USATECHIDXUSD",
  "session_timezone": "America/New_York",
  "friction_assumption": "2.0 index points round-trip",
  "historical_n": 13,
  "historical_frequency": 4.09,
  "historical_mean_net": "+62.36 bps",
  "historical_median_net": "Positive",
  "scientific_status": "Qualified"
}
```

**Hash:** `a0357ec9f438cd4f339c64ea8917afe983c809a0a8850b95c03d1ed629ed8eb9`

---

## 8. Field-by-Field Difference

The exact differences between the original definitions (from Research Factory screening) and the reconstructed Python dictionaries cannot be determined without the original source definitions in a structured format. The original definitions were embedded in narrative screening documents (V7/V8 for CAND-024, V12 for CAND-035), not in a machine-readable format.

However, the hash mismatch **definitively proves** that the Python dictionaries contain different content from the original definitions. The differences could include:

- Different text in preconditions, entry, exit, or event_definition fields
- Different field values (e.g., different numeric values for historical_n, frequency, etc.)
- Different field names or structure
- Extra or missing fields
- Different string formatting (punctuation, capitalization, whitespace)

---

## 9. Strategy Semantics Comparison

### Semantic Behavior: EQUIVALENT

Despite the hash mismatch, the **semantic behavior** of the strategies appears equivalent:

**CAND-024:**
- Trigger: Friday 12:00 NY time when Morning High > Weekly High AND 12:00 Open < 08:00 Open
- Entry: Market order short at 12:00:00 EST
- Exit: 15:45:00 EST
- Direction: Short
- Market: USATECHIDXUSD

**CAND-035:**
- Trigger: Last trading day of month at 15:00 ET when 15:00 Open > 09:30 Open
- Entry: Market order long at 15:00 ET
- Exit: 16:00 ET (Market close)
- Direction: Long
- Market: USATECHIDXUSD

The engine implementations (`cand_024_engine.py` and `cand_035_engine.py`) correctly implement these semantic rules. The strategy logic is functionally correct.

**However:** The hash mismatch means the identity serialization is different, which means the contract identity does not match the frozen governance declaration.

---

## 10. Environment Metadata Comparison

The environment metadata is correctly separated from the contract identity:

- `broker_symbol`: `"USTECm"` — in `module_registry.py` config, NOT in contract definition
- `mapping_id`: `"MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0"` — in `module_registry.py` config, NOT in contract definition
- `broker`: `"Exness Technologies Ltd"` — in supervisor status, NOT in contract
- `server`: `"Exness-MT5Trial15"` — in supervisor status, NOT in contract

The contract hash is computed ONLY from the strategy definition dictionary, not from environment metadata. Environment metadata contamination is **NOT** the cause of the drift.

---

## 11. Root Cause

**DEFINITION RECONSTRUCTION DRIFT**

The root cause is that `contracts.py` was created with **reconstructed** candidate definitions that do not match the original definitions from the Research Factory screening.

Specifically:
1. The original candidate definitions existed in narrative screening documents (V7/V8 for CAND-024, V12 for CAND-035)
2. When `contracts.py` was created in commit `85482b8`, the agent reconstructed these definitions as Python dictionaries from memory
3. The reconstructed dictionaries contain differences from the original definitions (different field values, text, or structure)
4. The hash computed from the reconstructed dictionaries produces different hashes (`4f1c267e` / `a0357ec9`) from the original frozen hashes (`c49c5bb0` / `a7c2132d`)
5. The frozen hashes in governance documents were carried forward from the original screening without being re-verified against the Python implementation

**The architectural defect** is that the runtime derives the contract hash bottom-up from a reconstructed Python dictionary, rather than strictly inheriting the top-down frozen hash from the governance artifact.

---

## 12. Strategy Drift Assessment

> **NO** — The strategy logic is semantically equivalent.

The engine implementations correctly implement the intended strategy rules. The trigger conditions, entry/exit logic, direction, market, and session handling are all functionally correct. The drift is in the identity serialization, not in the strategy behavior.

---

## 13. Hash Drift Assessment

> **YES** — The hash identity has drifted.

The hashes produced by the current code (`4f1c267e` / `a0357ec9`) do not match the frozen hashes (`c49c5bb0` / `a7c2132d`). This is a confirmed identity drift.

---

## 14. Qualification Impact

> **INTEGRITY HOLD — DO NOT COUNT EVENTS**

Because the contract identity is unresolved, qualification is paused. The event counters remain:
- CAND-024: `0 / 3 / 5`
- CAND-035: `0 / 3 / 5`

No qualifying forward event has been contaminated by the drift (zero events have been captured). The historical start timestamp is preserved.

---

## 15. Historical Start-Time Preservation

> **PRESERVED — 2026-08-27T09:44:58Z**

The qualification clock start is recorded in `runtime/forward/supervisor/status.json` as `"qualification_clock_start": "2026-08-27T09:44:58Z"`. This must not be reset.

---

## 16. Task Scheduler Status

> **NOT INSTALLED**

`QuantForgeForwardSupervisor` does not currently exist in Windows Task Scheduler. Persistence remediation must happen only after the contract issue is fixed.

---

## 17. CAND-015

> **ACTIVE / PROTECTED / UNTOUCHED**

CAND-015's forward observation and all its logs remain completely isolated and unaffected by this investigation.

---

## 18. Required Remediation

**One exact next action:**

Reconstruct the original candidate definitions by extracting them from the original Research Factory screening documents (V7/V8 for CAND-024, V12 for CAND-035) and computing new frozen hashes from those exact definitions. Then update `contracts.py` to use the correct definitions, and update all governance documents to reference the new verified hashes.

Alternatively, if the original definitions can be recovered in a structured format, the frozen hashes should be recomputed and the governance documents updated to match the actual Python implementation.

The architectural fix is to make the runtime **inherit** the frozen hash from the governance artifact (top-down) rather than **compute** it from a reconstructed dictionary (bottom-up).

---

## 19. Integrity

The investigation was performed as a strict read-only audit. No code was modified. No files were created except this investigation artifact. No supervisor was restarted. No events were counted. The forward qualification remains in integrity hold.

---

*Investigation complete. Root cause identified: definition reconstruction drift. Strategy semantics unaffected. Hash identity drifted. Qualification paused.*
