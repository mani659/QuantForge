# QUANTFORGE CAND-015 ADAPTER INTERFACE REPAIR V1

## 1. Incident

Supervisor started successfully, initialized all 3 modules, then crashed
with `AttributeError: 'Cand015ModuleWrapper' object has no attribute 'config'`.

## 2. Exact Error

```
File "...quantforge_forward_supervisor.py", line 233, in run
    "symbol": module.config['logical_symbol'],
              ^^^^^^^^^^^^^
AttributeError: 'Cand015ModuleWrapper' object has no attribute 'config'
```

Second error after first fix:

```
File "...quantforge_forward_supervisor.py", line 251, in run
    "modules": {m.candidate_id: m.engine.state for m in self.modules}
                                ^^^^^^^^
AttributeError: 'Cand015ModuleWrapper' object has no attribute 'engine'
```

## 3. Supervisor Interface

The supervisor accesses these attributes on each module:

- `module.config['logical_symbol']` — logical market name
- `module.config['mapping_id']` — symbol mapping
- `module.config['broker_symbol']` — broker symbol (in quote reconstruction)
- `module.candidate_id` — module identifier
- `module.process_quote(quote, instance_id)` — process a quote
- `module.engine.state` — current engine state (for heartbeat)
- `module.module_dir` — module runtime directory

## 4. CAND-015 Wrapper Interface (Before Fix)

`Cand015ModuleWrapper` provided:

- `candidate_id` ✓
- `adapter` ✓ (but supervisor expected `engine`)
- `module_dir` ✓
- `event_ledger` ✓
- `outcome_ledger` ✓
- `paper` ✓
- `status_file` ✓
- `stats` ✓
- `process_quote()` ✓

Missing:

- `config` ✗
- `engine` ✗ (had `adapter` instead)

## 5. Missing Attribute/Method

1. `config` — dict with `logical_symbol`, `mapping_id`, `broker_symbol`, `minimum`, `target`
2. `engine` — reference to adapter (supervisor accesses `engine.state`)

## 6. Root Cause

`Cand015ModuleWrapper` was written with a different interface than
`ForwardModuleWrapper`. The supervisor assumed all modules share the same
interface (config, engine, process_quote).

## 7. Minimal Repair

### module_registry.py

Added to `Cand015ModuleWrapper.__init__()`:

```python
self.config = {
    "logical_symbol": "USATECHIDXUSD",
    "broker_symbol": "USTECm",
    "mapping_id": "MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0",
    "minimum": 3,
    "target": 5
}
self.engine = adapter
```

### cand015_adapter.py

Added `state` property to `Cand015Adapter`:

```python
@property
def state(self):
    return self._state

@state.setter
def state(self, value):
    self._state = value
```

## 8. CAND-015 Semantic Preservation

No changes to CAND-015 signal engine, thresholds, timing, entry, exit,
ATR calculation, or M5/D1 logic. Only adapter metadata exposed.

## 9. Shared Feed

USTECm data shared across all modules. CAND-015 adapter fetches M1 bars
from the same MT5 connection. BTCUSD not required for current signal
evaluation.

## 10. BTCUSD Handling

BTCUSD is buffered by CAND-015 engine but not used in current signal
evaluation. Not fetched from MT5 in current implementation.

## 11. Regression Tests

2 new tests added:

1. `test_cand015_wrapper_has_config_attribute` — verifies Cand015ModuleWrapper
   exposes config with correct keys
2. `test_all_modules_satisfy_supervisor_interface` — verifies all modules
   in registry satisfy the supervisor's required interface

## 12. Smoke Test

Not required — real forward test succeeded.

## 13. Real Forward Test

PASS. Supervisor started, initialized all 3 modules, ran main loop for
10+ seconds without crash. MT5 connected. All modules active.

## 14. BAT Test

BAT correctly shows:
- MT5 terminal status
- Singleton check
- Launches supervisor in foreground
- Command window stays visible

## 15. Singleton

Verified. Lock file prevents duplicate processes.

## 16. Status

Verified. Shows supervisor PID, MT5 connection, all 3 modules active.

## 17. CAND-024

> ACTIVE — 0 / 3 / 5

Canonical: `925495a8`

## 18. CAND-035

> ACTIVE — 0 / 3 / 5

Canonical: `ddc5d0e9`

## 19. Qualification Timeline

Preserved: `2026-08-27T09:44:58Z` / `2026-08-27T12:05:15Z`

## 20. CAND-015

> ACTIVE / PROTECTED / ADAPTER-INTEGRATED

## 21. System Assembly

> NOT EXECUTED

## 22. Integrity

- No contract changes
- No strategy logic changes
- No research executed
- No signal combination
- No portfolio logic
- 132/132 tests pass
- All 3 modules running under unified observer
