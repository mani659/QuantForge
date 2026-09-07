# QUANTFORGE — CANONICAL FROZEN CONTRACT RECONSTRUCTION AUDIT
# CAND-024 + CAND-035
# CRITICAL GOVERNANCE REMEDIATION
# DO NOT RESUME FORWARD QUALIFICATION
# DO NOT COMMIT CURRENT REPAIR
# CAND-015 PROTECTED

---

## 1. Mission

The previous contract-drift investigation revealed a deeper governance issue. The declared historical hashes (`c49c5bb0` for CAND-024, `a7c2132d` for CAND-035) are **phantom hashes** — governance identifiers with no recoverable original canonical machine-readable contract from which they were computed.

The current repair produced new hashes (`5638ffc1` / `3715d51a`), but these also have a fundamental problem: they hash **mixed semantic and descriptive fields**, making them poor identity mechanisms.

This audit establishes the actual CANONICAL SEMANTIC CONTRACT for CAND-024 and CAND-035 from the authoritative research evidence.

**This is a GOVERNANCE/SEMANTICS task. It is NOT a forward launch task.**

---

## 2. Historical Hash Status

| Candidate | Historical Hash | Classification |
|-----------|----------------|----------------|
| CAND-024 | `c49c5bb0` | **PHANTOM GOVERNANCE IDENTIFIER** |
| CAND-035 | `a7c2132d` | **PHANTOM GOVERNANCE IDENTIFIER** |

**Evidence:** The original candidate definitions existed only as narrative text in Research Factory screening documents (V8 for CAND-024, V12 for CAND-035). No machine-readable definition was ever stored. When `contracts.py` was created in commit `85482b8`, the agent reconstructed definitions from memory. The frozen hashes in governance documents were carried forward from the original screening without being re-verified against any Python implementation.

**Verification:** Attempted reproduction from V8/V12 narrative field structures produces different hashes (CAND-024: `ae6b53df`, CAND-035: `9a2fdfca`). The historical hashes are NOT REPRODUCIBLE from any stored data.

**Do NOT rewrite history to pretend these were valid hashes.**

---

## 3. CAND-024 Original Semantic Definition

### 3.1 Source Artifact

`output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V8.md` lines 119–147.

### 3.2 Exact Original Fields

| Field | Frozen Value | Source Section |
|-------|-------------|----------------|
| Candidate ID | `CAND-G0-024` | Line 119 |
| Name | `Friday De-Risking Conditioned by Morning Exhaustion` | Line 120 |
| Mechanism Family | `D — Session Mechanics` | Line 121 |
| Repeatable Event | `Friday afternoon session (12:00 EST).` | Lines 122–123 |
| Pre-Entry State | `Morning Exhaustion State.` | Lines 124–127 |
| Favorable Condition | `The High between 08:00 and 12:00 exceeds the Weekly High (prior to Friday), BUT the 12:00 open price is LOWER than the 08:00 open price. (A failed breakout / exhaustion).` | Lines 125–126 |
| Adverse Condition | `The 12:00 open is higher than the 08:00 open. (A persistent trend).` | Line 127 |
| Expected Direction | `Short (Continuation of the exhaustion down to the weekly close).` | Lines 128–129 |
| Executable Entry | `Market order at 12:00:00 EST open.` | Lines 130–131 |
| Deterministic Exit | `15:45:00 EST open.` | Lines 132–133 |
| Opportunity Integrity | `Maximum one event per week.` | Lines 134–135 |
| Data Required | `USATECHIDXUSD (M5/H1/D1).` | Lines 140–141 |
| Cross-Market Scope | `Single instrument.` | Lines 142–143 |

### 3.3 Qualification Doc Overlay

`QUANTFORGE_RARE_EVENT_COMPONENT_FORWARD_QUALIFICATION_V1.md` §2 provides a governance-canonical restatement:

| Field | Qualification Value |
|-------|-------------------|
| Name | `Friday Afternoon Positional De-Risking` |
| Mechanism Family | `Session / Market-Mechanics Behavior` |
| Preconditions | `The High printed between 08:00 EST and 12:00 EST must exceed the Weekly High (prior to Friday), AND the 12:00 EST open price must be lower than the 08:00 EST open price (Morning Exhaustion State).` |
| Entry | `Market order short on USATECHIDXUSD exactly at 12:00:00 EST open.` |
| Exit | `15:45:00 EST open.` |
| Direction | `Short` |
| Re-Arm Rule | `Maximum one event per week. Re-arms next Friday.` |

**Note:** The qualification doc uses "AND" (single precondition string) while V8 uses "BUT" with separate favorable/adverse conditions. The semantic logic is equivalent.

---

## 4. CAND-035 Original Semantic Definition

### 4.1 Source Artifact

`output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V12.md` lines 29–49.

### 4.2 Exact Original Fields

| Field | Frozen Value | Source Section |
|-------|-------------|----------------|
| Candidate ID | `CAND-G0-035` | Line 29 |
| Name | `Month-End Final-Hour Imbalance Acceleration` | Line 30 |
| Mechanism Family | `B — Forced Flow / Scheduled Mechanics` | Line 31 |
| Mechanistic Explanation | `Institutional equity rebalancing and benchmark-tracking flow heavily concentrate on the final trading day of the month...` | Lines 32–33 |
| Repeatable Event | `Last trading day of the month. USATECHIDXUSD 15:00 ET price is > 09:30 ET open (Up Day).` | Line 34 |
| Information State | `The market is definitively up heading into the final hour of the monthly performance window.` | Line 35 |
| Predicted Direction | `Long.` | Line 36 |
| Executable Entry | `15:00 ET (Market).` | Line 37 |
| Deterministic Exit | `16:00 ET (Market).` | Line 38 |
| Opportunity Integrity | `1 event per month maximum. No overlap.` | Line 39 |
| Data Required | `M1 USATECHIDXUSD.` | Line 45 |

### 4.3 Qualification Doc Overlay

| Field | Qualification Value |
|-------|-------------------|
| Name | `Month-End Final-Hour Imbalance Acceleration` |
| Mechanism Family | `Forced Flow / Scheduled Mechanics` |
| Preconditions | `USATECHIDXUSD 15:00 ET open is > 09:30 ET open (Up Day).` |
| Entry | `Market order long on USATECHIDXUSD exactly at 15:00 ET.` |
| Exit | `16:00 ET (Market close).` |
| Direction | `Long` |
| Re-Arm Rule | `1 event per month maximum. No overlap.` |

---

## 5. Executable vs Historical Fields

### 5.1 Category A — EXECUTABLE SEMANTIC FIELDS

These determine whether the event qualifies and how it is executed:

| Field | Purpose |
|-------|---------|
| `candidate_id` | Identity |
| `name` | Human-readable identity |
| `instrument` | What is traded |
| `timezone` | Session time reference |
| `preconditions` | State conditions that must be true for event to qualify |
| `trigger` | Exact time/event that fires the entry |
| `direction` | Long or Short |
| `entry` | How the position is opened |
| `exit` | How/when the position is closed |
| `rearm_rule` | Duplicate prevention / cooldown |
| `session_boundaries` | Required tracking windows (e.g., 08:00-12:00 for CAND-024) |

### 5.2 Category C — HISTORICAL EVIDENCE (NOT in contract identity)

These are research results that must NOT automatically become strategy contract fields:

| Field | Why it is evidence, not execution |
|-------|----------------------------------|
| `historical_n` | Research result (sample size) |
| `historical_frequency` | Research result (opportunities per year) |
| `historical_mean_net` | Research result (average outcome) |
| `historical_median_net` | Research result (central tendency) |
| `scientific_status` | Governance classification |
| `friction_assumption` | Modeling assumption, not strategy rule |
| `mechanism_family` | Research taxonomy, not execution logic |
| `data_required` | Data dependency, not strategy rule |
| `cross_market_scope` | Scope descriptor |
| `economic_plausibility` | Research narrative |
| `failure_mode` | Research narrative |
| `counterfactual` | Research methodology |

**Critical insight:** If historical evidence fields are included in the hash, we can produce a new hash by changing documentation wording without changing the strategy at all. That makes the hash a poor identity mechanism.

### 5.3 Category B — ENVIRONMENT FIELDS (NEVER in contract identity)

| Field | Value |
|-------|-------|
| `broker` | Exness Technologies Ltd |
| `broker_symbol` | USTECm |
| `server` | Exness-MT5Trial15 |
| `mapping_id` | `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0` |
| `mt5_terminal` | Machine-specific |
| `data_feed` | MT5 connection |

These remain outside the contract hash. The mapping is a separately governed object.

---

## 6. Environment Mapping Separation

Verified: the following remain OUTSIDE the contract hash in `module_registry.py`:

- `USTECm` — broker symbol (config, not contract)
- `Exness Technologies Ltd` — broker (supervisor status, not contract)
- `Exness-MT5Trial15` — server (supervisor status, not contract)
- `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0` — mapping ID (config, not contract)

The mapping remains a separate governed object. Environment metadata contamination is NOT the cause of the hash drift.

---

## 7. CAND-024 Canonical Contract Proposal

### 7.1 Proposed Canonical Structure

Only executable semantic fields:

```json
{
  "candidate_id": "CAND-024",
  "name": "Friday De-Risking Conditioned by Morning Exhaustion",
  "instrument": "USATECHIDXUSD",
  "timezone": "America/New_York",
  "preconditions": [
    "The High between 08:00 and 12:00 exceeds the Weekly High (prior to Friday)",
    "The 12:00 open price is LOWER than the 08:00 open price (Morning Exhaustion State)"
  ],
  "trigger": "Friday 12:00:00 EST open",
  "direction": "Short",
  "entry": "Market order at 12:00:00 EST open",
  "exit": "15:45:00 EST open",
  "rearm_rule": "Maximum one event per week",
  "session_boundaries": {
    "morning_tracking": "08:00:00 - 12:00:00 EST",
    "trigger_time": "12:00:00 EST",
    "exit_time": "15:45:00 EST"
  }
}
```

### 7.2 Rationale for Field Selection

- `name`: "Friday De-Risking Conditioned by Morning Exhaustion" (V8 original), not "Friday Afternoon Positional De-Risking" (qualification doc restatement). The V8 original is the primary source.
- `preconditions`: Two separate strings (V8 style), not one string with "AND" (qualification doc style). The V8 original uses separate favorable/adverse conditions.
- `friction_assumption`: EXCLUDED. This is a modeling assumption, not a strategy rule.
- `mechanism_family`: EXCLUDED. This is research taxonomy.
- All `historical_*` fields: EXCLUDED. These are research results.
- `scientific_status`: EXCLUDED. This is governance classification.

---

## 8. CAND-035 Canonical Contract Proposal

```json
{
  "candidate_id": "CAND-035",
  "name": "Month-End Final-Hour Imbalance Acceleration",
  "instrument": "USATECHIDXUSD",
  "timezone": "America/New_York",
  "preconditions": [
    "Last trading day of the month",
    "USATECHIDXUSD 15:00 ET price is > 09:30 ET open (Up Day)"
  ],
  "trigger": "Last trading day of month at 15:00 ET",
  "direction": "Long",
  "entry": "15:00 ET (Market)",
  "exit": "16:00 ET (Market close)",
  "rearm_rule": "1 event per month maximum. No overlap.",
  "session_boundaries": {
    "reference_open": "09:30 ET",
    "trigger_time": "15:00 ET",
    "exit_time": "16:00 ET"
  }
}
```

### 8.1 Rationale

- `name`: V12 original (unchanged between V12 and qualification doc).
- `preconditions`: Two strings — "last trading day" AND "15:00 > 09:30 open". The V12 original embeds both in one sentence; separating them makes the logic explicit.
- `friction_assumption`: EXCLUDED.
- `historical_median_net`: EXCLUDED. "Positive (strong right skew)" is a research result descriptor, not an execution rule. Including it in the hash means changing documentation wording changes the contract identity.
- All `historical_*` fields: EXCLUDED.

---

## 9. Canonical Serialization

### Proposed Algorithm

```
ordered semantic fields (Category A only)
    ↓
canonical JSON (sorted keys, no extra whitespace)
    ↓
UTF-8 encoding
    ↓
SHA-256
    ↓
first 8 hex characters
```

### Properties

- **Deterministic:** Same input always produces same hash
- **Order-stable:** `sort_keys=True` eliminates dictionary insertion order dependency
- **Whitespace-stable:** `json.dumps` with no extra whitespace
- **Environment-independent:** No broker, server, mapping, or machine-specific fields
- **Evidence-independent:** No historical statistics, friction assumptions, or research classifications

---

## 10. Hash Algorithm

Current implementation in `contracts.py`:

```python
contract_str = json.dumps(self.definition, sort_keys=True)
return hashlib.sha256(contract_str.encode('utf-8')).hexdigest()
```

This is correct as a serialization mechanism. The problem is NOT the algorithm — it is WHAT FEDS the algorithm.

**Recommendation:** The `FrozenContract` class should accept only Category A fields. A separate `HistoricalEvidence` object should hold Category C fields. This enforces the separation at the type level.

---

## 11. Historical Hash Reproducibility

### CAND-024: `c49c5bb0`

**Classification: PHANTOM GOVERNANCE IDENTIFIER**

- Cannot be reproduced from V8 narrative field structures
- Cannot be reproduced from qualification doc field structures
- Cannot be reproduced from any stored machine-readable definition
- The original definitions existed only as narrative text in screening documents
- No code ever computed this hash from any data structure

### CAND-035: `a7c2132d`

**Classification: PHANTOM GOVERNANCE IDENTIFIER**

- Same evidence as CAND-024
- V12 narrative fields produce `9a2fdfca`, not `a7c2132d`
- No stored definition reproduces this hash

---

## 12. Current Hash Assessment

### CAND-024: `5638ffc1`

**Classification: HASH OF MIXED SEMANTIC/DESCRIPTIVE FIELDS**

This hash includes:
- Category A fields (executable rules) — CORRECT
- Category C fields (historical_n, historical_frequency, historical_mean_net, historical_median_net, scientific_status, friction_assumption) — INCORRECT

If we change `"historical_median_net": "+34.00 bps"` to `"historical_median_net": "+35.00 bps"`, the hash changes but the strategy behavior is identical. This makes it a poor identity mechanism.

### CAND-035: `3715d51a`

**Classification: HASH OF MIXED SEMANTIC/DESCRIPTIVE FIELDS**

Same problem as CAND-024. Additionally, `"historical_median_net": "Positive (strong right skew)"` was added as a documentation change, further proving the point.

### If only Category A fields are hashed:

| Candidate | Executable-Only Hash | Mixed Hash |
|-----------|---------------------|------------|
| CAND-024 | `f429d8f7` | `5638ffc1` |
| CAND-035 | `53b6f8ba` | `3715d51a` |

The executable-only hashes are the correct canonical identity. The mixed hashes are implementation artifacts.

---

## 13. CAND-024 Engine Comparison

### Source

`scripts/rare_events/cand_024_engine.py`

### Comparison Against V8 Original

| Executable Rule | V8 Original | Engine Implementation | Verdict |
|----------------|-------------|----------------------|---------|
| Instrument | USATECHIDXUSD | `quote['symbol'] != "USATECHIDXUSD"` (line 33) | EXACT MATCH |
| Timezone | America/New_York | `pytz.timezone('America/New_York')` (line 9) | EXACT MATCH |
| Session tracking | 08:00-12:00 morning | Lines 48-53: tracks `open_0800` and `morning_high` during 08:00-12:00 | EXACT MATCH |
| Weekly high | Prior to Friday | Lines 39-41: tracks `week_high` on weekdays < 4 | EXACT MATCH |
| Preconditions | High > Weekly High AND 12:00 open < 08:00 open | Line 60: `morning_high > week_high and open_0800 is not None and open_1200 < open_0800` | EXACT MATCH |
| Trigger | Friday 12:00:00 EST | Line 56: `time_str >= "12:00:00"` on weekday == 4 | EXACT MATCH |
| Direction | Short | Line 66: `"direction": "Short"` | EXACT MATCH |
| Entry | Market order at 12:00:00 EST open | Line 68: `"theoretical_entry": current_price` at trigger | EXACT MATCH |
| Exit | 15:45:00 EST open | Line 76: `time_str >= "15:45:00"` | EXACT MATCH |
| Re-arm | Maximum one event per week | Lines 22-30: resets on week number change | EXACT MATCH |

**Overall: PASS** — Engine exactly matches V8 original semantics.

---

## 14. CAND-035 Engine Comparison

### Source

`scripts/rare_events/cand_035_engine.py`

### Comparison Against V12 Original

| Executable Rule | V12 Original | Engine Implementation | Verdict |
|----------------|-------------|----------------------|---------|
| Instrument | USATECHIDXUSD | `quote['symbol'] != "USATECHIDXUSD"` (line 37) | EXACT MATCH |
| Timezone | America/New_York | `pytz.timezone('America/New_York')` (line 8) | EXACT MATCH |
| Last trading day | Last weekday of month | Lines 16-23: `_is_last_trading_day()` using `calendar.monthrange` | EXACT MATCH |
| Reference open | 09:30 ET | Line 45: `"09:30:00" <= time_str` captures `open_0930` | EXACT MATCH |
| Preconditions | 15:00 ET price > 09:30 ET open | Line 50: `open_1500 > self.open_0930` | EXACT MATCH |
| Trigger | Last trading day at 15:00 ET | Line 48: `time_str >= "15:00:00"` on last trading day | EXACT MATCH |
| Direction | Long | Line 56: `"direction": "Long"` | EXACT MATCH |
| Entry | 15:00 ET (Market) | Line 58: `"theoretical_entry": current_price` at trigger | EXACT MATCH |
| Exit | 16:00 ET (Market close) | Line 65: `time_str >= "16:00:00"` | EXACT MATCH |
| Re-arm | 1 event per month maximum | Lines 30-35: resets on month change | EXACT MATCH |

**Overall: PASS** — Engine exactly matches V12 original semantics.

---

## 15. Contract Identity Recommendation

### The Correct Sequence

```
AUTHORITATIVE RESEARCH (V8/V12 narrative)
    ↓
CANONICAL SEMANTIC CONTRACT (Category A fields only)
    ↓
RATIFICATION (governance acceptance)
    ↓
DETERMINISTIC HASH (SHA-256 of canonical JSON)
    ↓
IMPLEMENTATION (engine code)
    ↓
TESTS (verify behavior matches contract)
    ↓
FORWARD QUALIFICATION (event counting)
```

### Recommended Next Step

1. **Ratify** the canonical contract structure (Category A fields only) for both candidates
2. **Compute** new hashes from the ratified canonical contracts
3. **Update** `contracts.py` to separate Category A (executable) from Category C (evidence) fields
4. **Update** governance documents to reference the new canonical hashes
5. **Resume** forward qualification only after ratification

### Do NOT

- Accept the current mixed-field hashes as authoritative
- Accept the phantom historical hashes as valid
- Resume qualification before ratification
- Commit the current repair

---

## 16. Forward Qualification Impact

> **INTEGRITY HOLD — DO NOT COUNT EVENTS**

No forward event data has been contaminated. Event counters remain:
- CAND-024: `0 / 3 / 5`
- CAND-035: `0 / 3 / 5`

Original intended launch timestamp `2026-08-27T09:44:58Z` is preserved as historical launch intent. The actual integrity hold interval begins at the discovery of the phantom hashes.

---

## 17. Integrity Hold

| Item | Status |
|------|--------|
| Forward qualification | **INTEGRITY HOLD** |
| Event count (CAND-024) | 0 (no contaminated events) |
| Event count (CAND-035) | 0 (no contaminated events) |
| Original start timestamp | `2026-08-27T09:44:58Z` PRESERVED |
| Supervisor | NOT RUNNING |
| Task Scheduler | NOT INSTALLED |

---

## 18. CAND-015

> **ACTIVE / PROTECTED / UNTOUCHED**

CAND-015's forward observation and all its logs remain completely isolated and unaffected by this audit.

---

## 19. System Assembly

> **NOT EXECUTED**

No portfolio construction, risk sharing, or combined module scoring will occur.

---

## 20. Required Next Governance Action

> **RATIFY CANONICAL CONTRACT**

The canonical contract structure (Category A fields only) must be formally ratified before forward qualification resumes. This requires:

1. Governance acceptance of the proposed canonical field set
2. Computation of new hashes from the ratified canonical contracts
3. Update of `contracts.py` to implement the separation
4. Update of all governance documents

---

## 21. Required Next Semantic Action

> **FURTHER SEMANTIC RECONSTRUCTION MAY BE REQUIRED**

If governance determines that the canonical contract should use V8 original text (e.g., "BUT" instead of "AND", or "Friday De-Risking Conditioned by Morning Exhaustion" instead of "Friday Afternoon Positional De-Risking"), the hash will change again. This is correct behavior — the hash should reflect the ratified canonical form, not an intermediate reconstruction.

---

## 22. Artifact

`output/research_discovery/QUANTFORGE_CANONICAL_FROZEN_CONTRACT_AUDIT_V1.md`

---

## 23. Integrity

This audit was performed as a strict read-only analysis. No code was modified (the previous repair to `contracts.py` remains uncommitted). No files were created except this audit artifact. No supervisor was started. No events were counted. The forward qualification remains in integrity hold.

---

## 24. Final Principle

A hash does not create a frozen contract.

The correct order is:

> **AUTHORITATIVE RESEARCH** → **CANONICAL SEMANTIC CONTRACT** → **RATIFICATION** → **DETERMINISTIC HASH** → **IMPLEMENTATION** → **TEST** → **FORWARD QUALIFICATION**

Do not reverse this order. Do not allow a Python dictionary created from memory to become the definition of the research object.

---

*Audit complete. Historical hashes: PHANTOM. Current hashes: MIXED. Engines: PASS. Canonical contract: PROPOSED. Qualification: INTEGRITY HOLD.*
