# QUANTFORGE — RARE-EVENT CANONICAL RESUME
# CAND-024 + CAND-035
# CANONICAL CONTRACTS RATIFIED
# PAPER ONLY
# PRESERVE ORIGINAL TIMELINE
# CAND-015 PROTECTED

## 1. Mission

Resume the protected Rare-Event Forward Qualification track after successful
canonical contract ratification.

## 2. Canonical Contracts

### CAND-024

Display hash: `925495a8`

Full hash: `925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e`

Canonical identity: `CAND-024:CANONICAL:925495a8`

### CAND-035

Display hash: `ddc5d0e9`

Full hash: `ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5`

Canonical identity: `CAND-035:CANONICAL:ddc5d0e9`

## 3. Historical Phantom Identifiers

The following hashes were previously used as contract identities but are NOT
reproducible from any stored machine-readable definition:

- `c49c5bb0` — PHANTOM (CAND-024)
- `a7c2132d` — PHANTOM (CAND-035)
- `4f1c267e` — PHANTOM (CAND-024)
- `a0357ec9` — PHANTOM (CAND-035)
- `5638ffc1` — MIXED-FIELD (CAND-024)
- `3715d51a` — MIXED-FIELD (CAND-035)

These remain historical/invalid identifiers. They are NOT current canonical
identities.

## 4. Environment Mapping

Research identity: `USATECHIDXUSD`

Broker: `Exness Technologies Ltd`

Server: `Exness-MT5Trial15`

Broker symbol: `USTECm`

Mapping: `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`

Note: Environment mapping is NOT part of the canonical contract hash.
It is a separate governed object.

## 5. Pre-Ratification Runtime

The pre-ratification period ran from `2026-08-27T09:44:58Z` to the canonical
contract ratification. During this period:

- 51 health records were captured (old runner)
- 12 supervisor health records were captured (PID 12736)
- 0 events were captured
- Both modules remained in WATCHING state throughout
- No qualifying events were accepted

Pre-ratification health data has been archived to:
`runtime/forward/history/pre_canonical_supervisor_health.jsonl`
`runtime/forward/history/pre_supervisor_health.jsonl`

## 6. Integrity Gap

Gap start: `2026-08-27T09:44:58Z`

Gap end: `2026-08-27T10:10:08Z` (canonical contract ratification)

Reason: Phantom hash discovery and canonical contract ratification

Invalidated runtime architecture: Old runner used phantom/mixed-field contract
hashes that were not reproducible from stored definitions.

Qualifying events accepted during gap: ZERO

Both modules remained in WATCHING state throughout the gap period.

## 7. Runtime Evidence Preservation

Pre-ratification event ledgers: EMPTY (0 bytes)

Pre-ratification outcome ledgers: EMPTY (0 bytes)

Pre-ratification health data: ARCHIVED

No event data was lost because no events were captured during the pre-ratification
period.

## 8. Valid Qualification Resume

Original intended start: `2026-08-27T09:44:58Z`

Valid canonical qualification resume: `2026-08-27T12:05:15Z`

The valid resume timestamp is when the supervisor was restarted with canonical
contracts and confirmed running with MT5 connection.

The original timestamp remains historical continuity metadata.

## 9. Supervisor

PID: 6924

Mode: forward

State: RUNNING

MT5: CONNECTED

Broker: Exness Technologies Ltd

Server: Exness-MT5Trial15

Modules loaded: 2

Version: 1.0.0-unified

## 10. Task Scheduler

Task: `QuantForgeForwardSupervisor`

Status: NOT INSTALLED (requires Administrator privileges)

The scheduled task must be installed by running `install_quantforge_forward_task.bat`
as Administrator. The bat script is correct and ready.

## 11. CAND-024

Contract hash: `925495a86b35e6266b3dd04e27474dc94f19e86f0c0649cb0b976443f71cb13e`

Canonical identity: `CAND-024:CANONICAL:925495a8`

State: WATCHING

Event count: 0 / 3 / 5

Mapping: MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0

## 12. CAND-035

Contract hash: `ddc5d0e9bed41a7ccae30e69b2b8b38914e2a90693282ecd2823e10948d48cc5`

Canonical identity: `CAND-035:CANONICAL:ddc5d0e9`

State: WATCHING

Event count: 0 / 3 / 5

Mapping: MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0

## 13. Ledgers

CAND-024 event ledger: APPEND-ONLY / SEPARATE / EMPTY (0 bytes)

CAND-024 outcome ledger: APPEND-ONLY / SEPARATE / EMPTY (0 bytes)

CAND-035 event ledger: APPEND-ONLY / SEPARATE / EMPTY (0 bytes)

CAND-035 outcome ledger: APPEND-ONLY / SEPARATE / EMPTY (0 bytes)

Pre-ratification health: ARCHIVED (51 + 12 records)

## 14. Paper Execution

Mode: SYNTHETIC PAPER EXECUTION ONLY

No live order submission. No demo order submission. No real order submission.

PaperExecutionFirewall with friction=2.0 index points round-trip.

## 15. Feed

MT5 connection: CONNECTED

Broker symbol: USTECm

Latest bid: 29518.34

Latest ask: 29519.46

Feed age: ~1.3 seconds

No historical fallback. No synthetic feed.

## 16. Event Counters

CAND-024: 0 / 3 / 5 (current / minimum / target)

CAND-035: 0 / 3 / 5 (current / minimum / target)

Pre-ratification events: ZERO

Valid qualification starts from: 2026-08-27T12:05:15Z

## 17. CAND-015

Status: ACTIVE / PROTECTED / EXTERNAL / UNTOUCHED

Not inspected. Not migrated. Not modified.

## 18. System Assembly

Status: NOT EXECUTED

## 19. Research Discovery

Status: MAY RESUME SEPARATELY

The forward qualification is now running in the background. A future G0 cycle
is independent from the protected CAND-024/CAND-035 runtime.

## 20. Final Resume Status

> CANONICAL RARE-EVENT QUALIFICATION RESUMED — PROTECTED

The supervisor is running with canonical contracts. Both modules are active.
MT5 is connected. Event ledgers are empty and ready for valid qualification.
The qualification timeline is explicitly partitioned.

## 21. Integrity

78/78 contract tests PASS.

Engine consistency: CAND-024 PASS, CAND-035 PASS.

Supervisor contract firewall: PASS.

Paper execution firewall: PASS.

Event ledger separation: PASS.

Module independence: PASS.

Singleton lock: PASS.

CAND-015 firewall: PASS.

System Assembly: NOT EXECUTED.

Canonical contract hashes: VERIFIED IN RUNTIME.

---

Resume artifact created: 2026-08-27T12:05:15Z
