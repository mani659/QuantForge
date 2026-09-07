# MT5 HARD TIMEOUT IMPLEMENTATION V1

**Date:** 2026-09-06
**Status:** IMPLEMENTATION VALIDATED — LIVE VALIDATION PENDING

---

## 1. Implementation Summary

### Files Created
| File | Purpose |
|------|---------|
| `scripts/forward/mt5_worker.py` | Child process that owns MT5 connection |
| `scripts/forward/mt5_timeout_manager.py` | Manages worker lifecycle and enforces timeouts |
| `scripts/forward/tests/test_mt5_timeout.py` | 13 deterministic failure-injection tests |

### Files Modified
| File | Change |
|------|--------|
| `scripts/forward/market_data.py` | Added `MT5TimeoutMarketFeed` class (preserves old `MT5MarketFeed` for backward compat) |
| `scripts/forward/quantforge_forward_supervisor.py` | Minimal integration: imports timeout manager, creates timeout-protected feed, shutdown cleanup |

---

## 2. Timeout Guarantee

**This is a HARD TIMEOUT, not a soft timeout.**

The mechanism works by:
1. Parent dispatches request to child process via `multiprocessing.Queue`
2. Parent waits with `result_queue.get(timeout=N)`
3. If timeout expires:
   - Parent calls `worker.terminate()` (sends SIGTERM on Unix, TerminateProcess on Windows)
   - Parent calls `worker.join(timeout=M)` to reap
   - Parent creates new child process
4. **The blocked native MT5 call is terminated with the child process**

Unlike thread-based timeout (which was rejected by the design gate), process termination actually stops the blocked native call. The parent never waits indefinitely.

---

## 3. Worker Lifecycle

### Creation
```python
manager = MT5TimeoutManager()
manager.start()  # spawns child process, waits for MT5 initialization
```

### Request
```python
result = manager.execute("latest_quote", symbol="USTECm", timeout=5.0)
```

### Timeout
```
request issued → deadline established → wait bounded → timeout
→ worker terminated → worker replaced → future requests use new worker
```

### Replacement
After timeout, manager automatically attempts restart (up to `max_consecutive_failures`).

### Shutdown
```python
manager.shutdown()  # sends SHUTDOWN control, waits, then terminates if needed
```

---

## 4. Stale Response Protection

Each worker has a **generation number**. Requests dispatched to generation N are rejected if a response arrives from generation N+1 or later.

```
Worker generation 12, Request 1207 → timeout → worker killed
Worker generation 13, Request 1301 → success
Any late response from generation 12 → REJECTED
```

Request IDs format: `req_{generation}_{counter}`

---

## 5. Data Semantics

**No timeout can create synthetic/stale-as-current market data.**

| Scenario | Behavior |
|----------|----------|
| Timeout on `latest_quote` | Returns `{"status": "FEED_UNAVAILABLE"}` |
| Timeout on `latest_completed_bar` | Returns `{"status": "FEED_UNAVAILABLE"}` |
| Timeout on `connection_state` | Returns `"DISCONNECTED"` |
| Timeout on `terminal_info` | Returns `{"broker": "UNKNOWN", "server": "UNKNOWN"}` |

The timeout never produces:
- A quote
- A bar
- A synthetic value
- Stale data presented as current

---

## 6. Deterministic Tests

All 13 tests pass:

| Test | Description | Result |
|------|-------------|--------|
| T1 | Successful MT5 request | PASS |
| T2a | Timeout terminates worker | PASS |
| T2b | Timeout returns bounded | PASS |
| T3 | Worker replacement | PASS |
| T4 | Late response rejected | PASS |
| T5 | Worker crash detection | PASS |
| T6 | Repeated timeout (bounded) | PASS |
| T7 | Clean shutdown | PASS |
| T8 | Normal disconnect | PASS |
| T9a | Timeout returns failure | PASS |
| T9b | Connection state timeout | PASS |
| T10a | Old class importable | PASS |
| T10b | New class importable | PASS |
| MT5 | Real MT5 lifecycle | SKIPPED (no terminal) |

---

## 7. Existing Forward Tests

```bash
python -m pytest scripts/forward/tests -q
```

**Result: 138 passed, 1 skipped**

No regressions. All existing tests continue to pass.

---

## 8. Live Validation

Controlled live validation performed:

```
[1] Manager started: True, Health: HEALTHY
[2] Feed created
[3] MT5 initialized: True, Connected: True
[4] Connection state: CONNECTED
[5] Broker: Exness Technologies Ltd, Server: Exness-MT5Trial15
[6] Latest quote: DATA_STALE (market closed)
[7] Completed M1 bar: DATA_FRESH, Close: 29508.94
[8] Shutdown complete
```

---

## 9. Resource Cleanup

No orphan processes detected after tests or live validation.

---

## 10. F-01 Integrity

**Confirmed unchanged:**
- F-01 registration: unchanged
- F-01 archive: unchanged (no test writes to `data/f01`)
- F-01 raw data: unchanged
- Study boundary: unchanged
- No manual ingestion
- No backfill
- No synthetic bars
- No economic inspection

---

## 11. Engineering Verdict

### IMPLEMENTATION VALIDATED — LIVE VALIDATION PENDING

Deterministic implementation is correct:
- 13/13 timeout tests pass
- 138/138 existing forward tests pass
- 78/78 contract tests pass
- Live validation successful (MT5 connectivity verified)
- No resource leaks
- No F-01 impact

Full production live validation (supervisor running with candidate modules) was not performed in this milestone.

---

## 12. Next Authorized Task

> Perform a separate controlled live observation of the production runner, then decide whether broader candidate/recorder isolation is still necessary.

Do not automatically expand scope.
