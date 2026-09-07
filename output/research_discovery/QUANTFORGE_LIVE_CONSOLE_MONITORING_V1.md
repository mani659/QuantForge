# QUANTFORGE LIVE CONSOLE MONITORING V1

Date: 2026-08-29
Status: COMPLETE
Classification: Operator Visibility Enhancement

---

## 1. Objective

Make the visible Command Prompt a simple live observation screen for the operator. Normal state is quiet but visibly alive. Major events are clearly printed. Detailed evidence remains in independent ledgers.

---

## 2. Live Display

Every ~10 seconds, the supervisor prints a compact live status block:

```
============================================================
 QUANTFORGE FORWARD RUNNER — LIVE
============================================================

MT5:
CONNECTED

Broker Symbol:
USTECm

------------------------------------------------------------
 CANDIDATE MONITOR
------------------------------------------------------------

CAND-015:
ACTIVE / PROTECTED

CAND-024:
ACTIVE
Contract: 925495a8
Events: 0 / 3 / 5
State: WATCHING

CAND-035:
ACTIVE
Contract: ddc5d0e9
Events: 0 / 3 / 5
State: WATCHING

------------------------------------------------------------
 SCANNER
------------------------------------------------------------

Feed: OK
Last Scan: 14:32:15 UTC
Runner: LIVE
============================================================

System is LIVE — scanning for authorized candidate events.
STOP: stop_quantforge_forward.bat
STATUS: status_quantforge_forward.bat
```

---

## 3. Refresh Strategy

- Live status refreshes every ~10 seconds
- Does NOT print every tick or every loop iteration
- Uses `_live_display_interval` (10s) to throttle refreshes
- Event banners interrupt the live display, then it resumes

---

## 4. CAND-015

Shows: `ACTIVE / PROTECTED`
No performance metrics. No internal strategy details.

---

## 5. CAND-024

Shows: ACTIVE, canonical hash (8-char), event count, engine state.
Contract: `925495a8`

---

## 6. CAND-035

Shows: ACTIVE, canonical hash (8-char), event count, engine state.
Contract: `ddc5d0e9`

---

## 7. Feed Status

- `Feed: OK` when connected
- `Feed: DISCONNECTED` when connection is lost
- Feed status is derived from actual `feed.connection_state()`, not fabricated

---

## 8. Event Notifications

When a candidate undergoes a genuine state transition:

```
============================================================
 !!! QUANTFORGE EVENT DETECTED !!!
============================================================

Candidate:
CAND-024

Canonical:
925495a8

Event ID:
<event-id>

State:
DETECTED

Event Time UTC:
<timestamp>

Logical Market:
USATECHIDXUSD

Broker Symbol:
USTECm

============================================================
```

---

## 9. Event Deduplication

Uses `(event_id, event_state)` as dedup key. Same combination prints only once. Sequence: DETECTED → CAPTURED → COMPLETED (each once).

---

## 10. Normal Console Behavior

No tick spam. No M1 bar spam. No NO_EVENT spam. No heartbeat spam. Normal operation is quiet except for the periodic live status refresh.

---

## 11. Operator Controls

Footer shown during startup/live display:
- `STOP: stop_quantforge_forward.bat`
- `STATUS: status_quantforge_forward.bat`

---

## 12. Status Integration

Console is presentation only. Runtime state (`save_status()`) remains authoritative. Ledgers remain evidence. No duplicate state models.

---

## 13. Failure Display

- Feed disconnection: shows `Feed: DISCONNECTED` in live status
- Module error: individual module shows error state without suppressing others
- No fake NO_EVENT or fabricated events

---

## 14. Tests

125/125 tests passing including:
- Live display prints active modules
- Live display shows feed OK
- Live display shows feed disconnected
- Live display shows runner LIVE
- Live display shows last scan timestamp
- Live display shows operator controls
- Event banner prints once (dedup)
- Event banner shows enhanced format
- Module error isolation

---

## 15. Manual Verification

Start `run_quantforge_forward.bat` → confirm:
- Visible CMD window
- Live status appears with all 3 candidates
- MT5 connected
- Runner remains active
- Periodic refresh visible

---

## 16. Contract Preservation

No modification to:
- CAND-024: `925495a8`
- CAND-035: `ddc5d0e9`

---

## 17. Qualification Timeline

Preserved:
- Original: `2026-08-27T09:44:58Z`
- Valid canonical: `2026-08-27T12:05:15Z`

---

## 18. Integrity

- No live/demo/real orders
- No signal combination
- No portfolio logic
- Independent candidates
- Presentation-only change
- No strategy semantics modified
