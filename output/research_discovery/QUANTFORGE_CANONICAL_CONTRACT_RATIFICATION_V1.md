# QUANTFORGE — CANONICAL CONTRACT RATIFICATION + CONTRACT-BOUNDARY REPAIR
# CAND-024 + CAND-035
# DATE: 2026-08-27

---

## 1. Mission

Ratify the canonical semantic contracts for CAND-024 and CAND-035, implement them in machine-readable form, compute deterministic canonical hashes, separate strategy identity from historical evidence and environment metadata, verify engine consistency, strengthen contract tests, and prepare the supervisor for later resumption.

**DO NOT resume forward qualification in this task.**

---

## 2. Historical Phantom Identifiers

| Candidate | Historical Hash | Status |
|-----------|----------------|--------|
| CAND-024 | `c49c5bb0` | **PHANTOM GOVERNANCE IDENTIFIER** |
| CAND-035 | `a7c2132d` | **PHANTOM GOVERNANCE IDENTIFIER** |

These hashes were governance declarations with no recoverable canonical machine-readable contract. They are retained historically as phantom identifiers. They are NOT the canonical contract hashes.

---

## 3. CAND-024 Canonical Semantics

Source: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V8.md` lines 119–146.

| Field | Canonical Value |
|-------|----------------|
| candidate_id | `CAND-024` |
| name | `Friday De-Risking Conditioned by Morning Exhaustion` |
| instrument | `USATECHIDXUSD` |
| timezone | `America/New_York` |
| preconditions | `("The High between 08:00 and 12:00 exceeds the Weekly High (prior to Friday)", "The 12:00 open price is LOWER than the 08:00 open price (Morning Exhaustion State)")` |
| trigger | `Friday 12:00:00 EST open` |
| direction | `Short` |
| entry | `Market order at 12:00:00 EST open` |
| exit | `15:45:00 EST open` |
| rearm_rule | `Maximum one event per week` |
| session_boundaries | `{morning_tracking_start: "08:00:00 EST", morning_tracking_end: "12:00:00 EST", trigger_time: "12:00:00 EST", exit_time: "15:45:00 EST"}` |

---

## 4. CAND-035 Canonical Semantics

Source: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V12.md` lines 29–48.

| Field | Canonical Value |
|-------|----------------|
| candidate_id | `CAND-035` |
| name | `Month-End Final-Hour Imbalance Acceleration` |
| instrument | `USATECHIDXUSD` |
| timezone | `America/New_York` |
| preconditions | `("Last trading day of the month", "USATECHIDXUSD 15:00 ET price is > 09:30 ET open (Up Day)")` |
| trigger | `Last trading day of month at 15:00 ET` |
| direction | `Long` |
| entry | `15:00 ET (Market)` |
| exit | `16:00 ET (Market close)` |
| rearm_rule | `1 event per month maximum. No overlap.` |
| session_boundaries | `{reference_open: "09:30 ET", trigger_time: "15:00 ET", exit_time: "16:00 ET"}` |

---

## 5. Executable Fields

Category A — determines what the machine does:

- `candidate_id`, `name`, `instrument`, `timezone`
- `preconditions` (state conditions for event qualification)
- `trigger` (exact time/event that fires entry)
- `direction` (Long or Short)
- `entry` (how the position is opened)
- `exit` (how/when the position is closed)
- `rearm_rule` (duplicate prevention / cooldown)
- `session_boundaries` (required tracking windows)

**Only these fields are hashed.**

---

## 6. Historical Evidence Separation

Category C — research results, NOT in strategy identity:

- `historical_n`, `historical_frequency`, `historical_mean_net`, `historical_median_net`
- `scientific_status`, `friction_assumption`, `mechanism_family`, `data_required`
- `counterfactual`, `economic_plausibility`, `failure_mode`
- Any p-value, confidence interval, drawdown, win rate

These are modeled as a separate `HistoricalEvidence` dataclass. Changing evidence NEVER changes the canonical contract hash.

**PASS** — Evidence is fully separated.

---

## 7. Environment Separation

Category B — broker/runtime, NOT in strategy identity:

- `broker`, `broker_symbol`, `server`, `mapping_id`
- MT5 terminal, feed source, runtime PID, machine, latency

These are modeled as a separate `EnvironmentMapping` dataclass. The current governed mapping:

`MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`

**PASS** — Environment is fully separated.

---

## 8. Canonical Serialization

```
executable fields (Category A only)
    ↓
canonical JSON: json.dumps(data, sort_keys=True, separators=(',', ':'))
    ↓
UTF-8 encode
    ↓
SHA-256
    ↓
full hex digest (64 chars)
    ↓
first 8 chars (display hash)
```

Properties:
- Deterministic (same input → same hash)
- Order-stable (sort_keys)
- Whitespace-stable (separators eliminate extra spaces)
- Environment-independent
- Evidence-independent

---

## 9. Hash Algorithm

- **Algorithm:** SHA-256
- **Full hash:** 64 hex characters
- **Display hash:** First 8 hex characters
- **Truncation:** Explicit, documented, display-only

---

## 10. New Canonical Contract IDs

| Candidate | Canonical Identity | Full Hash |
|-----------|-------------------|-----------|
| CAND-024 | `CAND-024:CANONICAL:925495a8` | `925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e` |
| CAND-035 | `CAND-035:CANONICAL:ddc5d0e9` | `ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5` |

Historical phantom identifiers `c49c5bb0` and `a7c2132d` are retained as historical records only.

---

## 11. CAND-024 Engine Verification

Source: `scripts/rare_events/cand_024_engine.py`

| Executable Rule | V8 Original | Engine | Verdict |
|----------------|-------------|--------|---------|
| Instrument | USATECHIDXUSD | `quote['symbol'] != "USATECHIDXUSD"` | EXACT MATCH |
| Timezone | America/New_York | `pytz.timezone('America/New_York')` | EXACT MATCH |
| Session tracking | 08:00-12:00 | Lines 48-53 | EXACT MATCH |
| Weekly high | Prior to Friday | Lines 39-41 | EXACT MATCH |
| Preconditions | High > Weekly AND 12:00 < 08:00 | Line 60 | EXACT MATCH |
| Trigger | Friday 12:00:00 | Line 56 | EXACT MATCH |
| Direction | Short | Line 66 | EXACT MATCH |
| Entry | Market at 12:00:00 | Line 68 | EXACT MATCH |
| Exit | 15:45:00 | Line 76 | EXACT MATCH |
| Re-arm | Weekly | Lines 22-30 | EXACT MATCH |

**PASS**

---

## 12. CAND-035 Engine Verification

Source: `scripts/rare_events/cand_035_engine.py`

| Executable Rule | V12 Original | Engine | Verdict |
|----------------|-------------|--------|---------|
| Instrument | USATECHIDXUSD | `quote['symbol'] != "USATECHIDXUSD"` | EXACT MATCH |
| Timezone | America/New_York | `pytz.timezone('America/New_York')` | EXACT MATCH |
| Last trading day | Last weekday | Lines 16-23 | EXACT MATCH |
| Reference open | 09:30 ET | Line 45 | EXACT MATCH |
| Preconditions | 15:00 > 09:30 open | Line 50 | EXACT MATCH |
| Trigger | Last day 15:00 | Line 48 | EXACT MATCH |
| Direction | Long | Line 56 | EXACT MATCH |
| Entry | 15:00 Market | Line 58 | EXACT MATCH |
| Exit | 16:00 Market close | Line 65 | EXACT MATCH |
| Re-arm | Monthly | Lines 30-35 | EXACT MATCH |

**PASS**

---

## 13. Contract Tests

78 tests across 10 categories:

| Category | Tests | Status |
|----------|-------|--------|
| Identity (exact hash, determinism, format) | 12 | ALL PASS |
| Mutation (executable field changes → hash changes) | 9 | ALL PASS |
| Evidence exclusion (evidence changes → hash unchanged) | 4 | ALL PASS |
| Environment exclusion (env changes → hash unchanged) | 4 | ALL PASS |
| Field completeness | 4 | ALL PASS |
| Serialization stability | 4 | ALL PASS |
| Engine consistency | 8 | ALL PASS |
| Negative tests (missing/malformed fields) | 11 | ALL PASS |
| Phantom hash separation | 3 | ALL PASS |
| Contract content (V8/V12 verification) | 19 | ALL PASS |

**78/78 PASS**

---

## 14. Negative Tests

Invalid contracts correctly rejected:
- Missing candidate_id → TypeError
- Empty name → ValueError
- Empty instrument → ValueError
- Empty preconditions → ValueError
- Empty trigger → ValueError
- Empty direction → ValueError
- Empty entry → ValueError
- Empty exit → ValueError
- Empty rearm_rule → ValueError
- Whitespace-only name → ValueError
- Frozen contract attribute assignment → AttributeError

---

## 15. Supervisor Contract Firewall

The supervisor loads contracts through:

```
quantforge_forward_supervisor.py
  → module_registry.py (get_registry)
    → cand_024_engine.py / cand_035_engine.py
      → contracts.py (CAND_024_CONTRACT / CAND_035_CONTRACT)
```

- Single source of truth: `contracts.py`
- No dictionary reconstruction in supervisor
- Contract hash written to status.json and event ledgers
- Engine inherits canonical contract, does not recompute

**PASS** — Supervisor uses canonical contract top-down, not bottom-up reconstruction.

---

## 16. Forward Integrity Hold

| Item | Status |
|------|--------|
| Forward qualification | **INTEGRITY HOLD** |
| CAND-024 events | 0 / 3 / 5 |
| CAND-035 events | 0 / 3 / 5 |
| Supervisor | STOPPED |
| Task Scheduler | NOT INSTALLED |

---

## 17. Timeline Preservation

| Event | Timestamp |
|-------|-----------|
| Original intended launch | `2026-08-27T09:44:58Z` PRESERVED |
| Contract integrity hold start | `2026-08-27` (phantom hash discovery) |
| Canonical contract ratified | `2026-08-27` (this artifact) |
| Integrity gap | Duration between hold start and ratification |

The integrity gap is an acknowledged period where forward observation was on hold. No events were recorded during this period.

---

## 18. CAND-015

> **ACTIVE / PROTECTED / UNTOUCHED**

CAND-015's forward observation and all its logs remain completely isolated and unaffected.

---

## 19. System Assembly

> **NOT EXECUTED**

---

## 20. Ratification Status

> **CANONICAL CONTRACTS RATIFIED**

The canonical semantic contracts for CAND-024 and CAND-035 have been:
- Extracted from authoritative V8/V12 research artifacts
- Implemented as immutable `FrozenStrategyContract` dataclasses
- Separated from `HistoricalEvidence` and `EnvironmentMapping`
- Hash-verified with 78 passing tests
- Engine-consistent with both `cand_024_engine.py` and `cand_035_engine.py`
- Supervisor-compatible through single-source import chain

---

## 21. Required Next Action

> **SUPERVISOR RESUME + PERSISTENCE VALIDATION**

A separate task must:
1. Start the supervisor
2. Verify MT5 connection
3. Verify canonical hashes in runtime status
4. Validate event detection with synthetic or live data
5. Confirm forward qualification resumes correctly

---

## 22. Integrity

This task modified:
- `scripts/rare_events/contracts.py` — Rewritten with canonical architecture
- `scripts/rare_events/tests/test_rare_events.py` — 78 comprehensive tests
- `runtime/forward/cand_024/status.json` — Updated contract_hash
- `runtime/forward/cand_035/status.json` — Updated contract_hash
- `output/research_discovery/QUANTFORGE_CANONICAL_CONTRACT_RATIFICATION_V1.md` — This artifact

No CAND-015 files were modified. No events were counted. No supervisor was started. Forward qualification remains on integrity hold.

---

## 23. Files Modified

| File | Change |
|------|--------|
| `scripts/rare_events/contracts.py` | Rewritten: FrozenStrategyContract + HistoricalEvidence + EnvironmentMapping |
| `scripts/rare_events/tests/test_rare_events.py` | Rewritten: 78 canonical contract tests |
| `runtime/forward/cand_024/status.json` | Updated contract_hash to canonical |
| `runtime/forward/cand_035/status.json` | Updated contract_hash to canonical |
| `output/research_discovery/QUANTFORGE_CANONICAL_CONTRACT_RATIFICATION_V1.md` | Created |

---

*Ratification complete. Canonical contracts: CAND-024:CANONICAL:925495a8, CAND-035:CANONICAL:ddc5d0e9. Tests: 78/78 PASS. Engines: PASS. Supervisor firewall: PASS. Qualification: INTEGRITY HOLD.*
