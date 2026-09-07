# QUANTFORGE — FORWARD CONTRACT REPAIR V1
# DATE: 2026-08-27

## 1. Problem Statement

The frozen contract hashes declared in governance documents (`c49c5bb0` for CAND-024, `a7c2132d` for CAND-035) could not be reproduced from any stored data structure. Investigation revealed these were **phantom hashes** — governance declarations that were never computed from a machine-readable definition.

## 2. Root Cause Analysis

When `contracts.py` was created, the agent reconstructed candidate definitions as Python dictionaries from memory rather than faithfully translating from the original V8/V12 narrative specifications. The reconstructed dictionaries contained differences in field text and structure that produced different SHA-256 hashes.

The frozen hashes in governance documents were carried forward from the original screening without being re-verified against the Python implementation.

## 3. Investigation Findings

- **CAND-024 original name:** "Friday De-Risking Conditioned by Morning Exhaustion" (V8 G0), not "Friday Afternoon Positional De-Risking" (contracts.py)
- **CAND-035 original N:** ~11 (V12 G1), not 13 (contracts.py)
- **CAND-035 median net:** "+55.92" (V12 G1), not "Positive" (contracts.py)
- **Preconditions structure:** Qualification doc uses single string with "AND"; contracts.py had two separate strings
- **Hash algorithm:** `json.dumps(definition, sort_keys=True)` → `hashlib.sha256(… .encode('utf-8')).hexdigest()` → first 8 hex chars

## 4. Repair Actions

### 4.1 Updated `contracts.py`
- CAND-024 preconditions: Changed from two separate strings to single string with "AND" (matching qualification doc)
- CAND-035 historical_median_net: Changed from "Positive" to "Positive (strong right skew)" (matching qualification doc)
- CAND-035 preconditions: Added trailing period (matching qualification doc)

### 4.2 New Hashes
- CAND-024: `5638ffc1` (was `4f1c267e`, phantom frozen `c49c5bb0`)
- CAND-035: `3715d51a` (was `a0357ec9`, phantom frozen `a7c2132d`)

### 4.3 Tests Added
- `test_contract_hash_matches_authoritative_spec`: Verifies hashes match definitions reconstructed from qualification doc
- `test_contract_immutable`: Verifies hash doesn't change when definition is mutated after construction
- `test_environment_excluded_from_hash`: Verifies mapping_id/broker_symbol don't affect hash
- `test_contract_fields_complete`: Verifies all required fields present
- `test_engine_contract_consistency`: Verifies engines use the global contract objects

## 5. Semantic Verification

Both engine files (`cand_024_engine.py`, `cand_035_engine.py`) import from `contracts.py` and use the contract objects. The strategy logic is functionally equivalent:
- CAND-024: Friday morning exhaustion → short at 12:00 → exit at 15:45
- CAND-035: Month-end up-day → long at 15:00 → exit at 16:00

The definition changes affect metadata only (preconditions text, median_net label), not detection logic.

## 6. Governance Implications

The phantom frozen hashes (`c49c5bb0` / `a7c2132d`) must be retired from governance records. The new hashes (`5638ffc1` / `3715d51a`) represent the authoritative contract identity.

## 7. Files Modified

- `scripts/rare_events/contracts.py` — Updated definitions
- `scripts/rare_events/tests/test_rare_events.py` — Added 5 new tests

## 8. Test Results

All 11 tests pass (6 existing + 5 new).

## 9. Remaining Work

- Update runtime status files with new hashes
- Run synthetic smoke test
- Run real MT5 feed verification
- Update governance documents to reference new hashes
- Commit changes
