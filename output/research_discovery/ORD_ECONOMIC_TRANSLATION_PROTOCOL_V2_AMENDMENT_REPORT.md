# QUANTFORGE — ORD ECONOMIC TRANSLATION PROTOCOL V2 AMENDMENT REPORT

Status: AMENDMENT REPORT — DATAFLOW AND PROVENANCE ONLY.
No economic execution; no PnL / trade-stat / viability computation; no protocol
modification beyond the registered V2 staged-execution dataflow; no runner or
EventStudyRecorder modification; no commit; no push.

---

## 1. Amendment Verdict

**PASS — V2.0.0 staged-execution dataflow/provenance amendment registered.**

The amendment introduces a bounded-memory, crash-safe, exactly-once staged
execution architecture (Stage 0 → Stage 1 → Stage 2 → Stage 3) that is dataflow
and provenance only. **No scientific or economic decision changed.** The frozen
V1.1.0 economic registry (entry, bridge, stop, horizon, MFE/MAE, cost model,
Model A/B, primary metric, viability gates, OOS split, market universe, BTCUSD
caveat, EURUSD exclusion) is incorporated unchanged and remains authoritative.

---

## 2. Stale-Run Reconciliation

**Target: `output/research_discovery/ORD_ECONOMIC/V1.1.0/EXECUTION_20260820T082217Z_cff4a63e-f6ea-450d-a102-87a40fba5a09`**

- PID 14792 confirmed **DEAD** (psutil `NoSuchProcess`) before any action.
- Heartbeat stale: last `execution_heartbeat.json` at 2026-08-20T08:24:48 UTC
  (RSS 3,903,938,560 B, rising) — prior to reconciliation at 10:17:48 UTC.
- Execution identity matched the target directory exactly in journal,
  heartbeat, process identity, and implementation manifest.
- Partial artifacts (4 infrastructure files) belong to this execution; no
  ledger/statistics/report/economic artifact exists.
- Reconciled via the approved mechanism:
  `scripts/reconcile_execution.py` → **SUCCESS: formally reconciled as CRASHED**.
- Result: journal state **CRASHED**, reason `EXTERNAL_PROCESS_DEATH_RECONCILED`;
  `scientific_validity = false`;
  `scientific_adjudication = NOT_ADJUDICABLE`; all partial artifacts preserved
  with hashes in `execution_manifest.json`; **not resumable, not reusable**.

The previously CRASHED `EXECUTION_20260820T074818Z_2d5555f0-a436-4ef7-829a-9bdf24f33d5e`
remains CRASHED / NOT_ADJUDICABLE (unchanged; no execution may reuse either
identity).

---

## 3. Original Protocol SHA

- **V1.0.0** — `ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1.md`:
  SHA-256 `50A08AAF4744A793CF5F0793E7AD104BB6EB5D04EA7EB82FE56DB30587FF74F2`
  (retained unmodified, superseded in text).
- **V1.1.0** — `ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md`:
  SHA-256 `8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663`
  (frozen base; incorporated unchanged by V2.0.0, retained unmodified).

---

## 4. V2 Protocol SHA

**`ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_AMENDED.md`** (V2.0.0):

- SHA-256: `85D4E1D1BD6AFB35B51FEEEC92DAE8EF98782AC95C3C6BD6126F28ED0E0B021C`
- Computed over the full file bytes at amendment-finalization time. This hash
  is the identity used by every downstream stage.

---

## 5. Dataflow Changes

The monolithic pipeline

`raw tick CSV → load massive dataset → derive quotes → simulate trades →
calculate metrics → next market`

is replaced by a staged, bounded-residency pipeline:

`raw data → Stage 0 preflight → Stage 1 frozen preparation → Stage 2 one
economic execution → Stage 3 read-only verification → independent adjudication`.

Rationale (unchanged from the staging design): two controlled executions failed
monolithically on the same host — `…2d5555f0` via pandas C-parser `out of
memory` on the 12.58 GB XAUUSD tick file (RSS 1.05 GiB at last heartbeat),
`…cff4a63e` via a rising ~3.9 GB RSS during XAUUSD per-minute in-memory bucket
materialization that was externally terminated. The staged model enforces at
most one minute of quote aggregation residency in Stage 1 and removes raw tick
files entirely from Stage 2's memory.

---

## 6. Stage 0 Rules

- **Repeatable, non-scientific** preflight per market (XAUUSD, XAGUSD,
  USATECHIDXUSD, BTCUSD).
- Checks: file existence; source SHA-256 (streamed); schema; exact row count;
  timestamp format and quote sanity counters; environment/resource capability
  (RAM, free disk, peak-RSS streaming probe).
- Output: `PREFLIGHT_<market>/` — no economic result; may be repeated; fresh
  identity each run; does not enter the economic lineage.

---

## 7. Stage 1 Rules

- **One market at a time**; never retains a full tick file or a full minutes
  table.
- **Bounded residency design target: at most one minute of tick observations
  resident for quote aggregation**, except small deterministic event-join state
  per market.
- Produces deterministic, immutable, hashed on-disk inputs registering: market;
  source tick hash; source M1 hash; economic protocol hash; preparation
  implementation hash; event ID; trading day; direction; breakout timestamp;
  `T_B`; entry quote/metadata; entry spread; structural stop; horizon timestamp;
  exit-lookup metadata; preparation schema version; per-minute quote aggregation
  metadata.
- Does **NOT** calculate viability, PnL, profit factor, classification, or any
  optimization metric.
- **Restart/reuse:** a completed Stage-1 preparation is reusable ONLY when its
  persisted metadata and hashes match the current protocol, source data, prep
  implementation, and schema version exactly; otherwise it must be regenerated.
  A Stage-1 artifact is a frozen input to Stage 2, not scientific/economic
  evidence.
- **Identity:** deterministic `PREP_<market>_<hash>`; directory contains prep
  manifest, source hashes, protocol hash, implementation hash, schema version,
  frozen event/input table, quote aggregation metadata, artifact hashes. No
  overwrite of an existing preparation.

---

## 8. Stage 2 Rules

- **Stage 2 is the sole controlled economic execution.**
- Consumes only: frozen Stage-1 inputs; the frozen economic protocol (V1.1.0
  incorporated unchanged; V2.0.0 dataflow registry); approved execution
  infrastructure.
- Calculates: trade ledger; gross/net; Model A; Model B descriptive sensitivity;
  MFE/MAE; cumulative net; PF; OOS; yearly results; viability gates — exactly as
  registered in V1.1.0 §§9–13.
- **Exactly once / non-resumable.** If Stage 2 crashes → **CRASHED /
  NOT_ADJUDICABLE**; never resumed from partial economic calculations.
- **Identity:** execution UUID `EXECUTION_<timestamp>_<UUID>`; persists Stage-1
  prep hashes, protocol hash, implementation hash, Git HEAD, environment,
  process identity, heartbeat. Mismatch invalidates the execution **before** any
  economic calculation (fail-closed).

---

## 9. Stage 3 Rules

- Read-only verification: Stage-1 hashes; Stage-2 ledger; formulas; market
  completeness; OOS; year summaries; viability gates; artifacts.
- Cannot modify scientific/economic results.
- Output: `VERIFICATION_<execution-id>/`. Repeatable; certifies only.

---

## 10. Exactly-Once Semantics

| Stage | Repeatable | Economic evidence | Resume/reuse |
|---|---|---|---|
| Stage 0 Preflight | Yes | No | restartable |
| Stage 1 Preparation | Yes (idempotent) | No | restartable; reusable only when hashes match exactly |
| Stage 2 Evaluation | **Single controlled run** | **Yes** | **NON-RESUMABLE** |
| Stage 3 Verification | Yes | No | restartable read-only |

- No stage may overwrite another execution.
- No failed Stage-2 execution may become a successful execution through partial
  resumption.
- The final experiment is **ONE CONTROLLED BASELINE ECONOMIC EXECUTION**.

---

## 11. Hash / Provenance Rules

- Every source object (M1, tick, event table, protocols) is SHA-256 hashed at
  each stage; no fingerprint is derived from any economic outcome.
- Stage 1 embeds all source/protocol/implementation/schema hashes in its
  manifest; its own identity is content-addressed (`PREP_<market>_<hash>`).
- Stage 2 embeds Stage-1 hashes + protocol hashes + implementation/Git/env/
  process identity + heartbeat; a mismatch invalidates before economic
  calculation.
- All prior executions remain immutable and forensic; CRASHED identities are
  never reused; a new run always receives a new identity; no shared destructive
  output directory.

---

## 12. Scientific/Economic Object Preservation

No change to: scientific object being translated; baseline entry; execution
bridge; structural invalidation; horizon; MFE/MAE; cost model; Model A; Model B;
primary economic metric; cumulative-net definition; profit-factor boundary
handling; viability gates (1–5); dev/OOS split; year-concentration gate; market
universe (XAUUSD/XAGUSD/USATECHIDXUSD/BTCUSD simulated, EURUSD NOT SIMULATED);
BTCUSD NO-SCIENTIFIC-VERDICT caveat; baseline strategy. All V1.1.0 economic text
is incorporated unchanged and authoritative.

---

## 13. Outcome-Blindness

- No value, parameter, threshold, gate, or classification in V2.0.0 was informed
  by any economic backtest on ORD events.
- Staging decisions were driven exclusively by execution forensics (two CRASHED
  identities, presented in the staging design) and the frozen V1.1.0 registry —
  not by any PnL or trade-outcome observation.
- The economic experiment remains exactly one baseline, allowed to succeed or
  fail on its own.

---

## 14. Self-Audit

Verified by construction of the V2 document and by the unchanged-first
sections of this report: V2 changes execution architecture/provenance only
(Stage 0/1/2/3, bounded quote aggregation residency, preparation hashes,
single controlled Stage-2 execution, Stage-3 verification, restart/reuse rules,
non-resumability, historical preservation, provenance). V2 changes **NO** entry,
stop, horizon, cost, metric, gate, OOS, market scope, or baseline strategy. **No
scientific or economic decision changed.**

---

## 15. Exact Next Task

> **INDEPENDENT READ-ONLY AUDIT OF THE V2 STAGED ECONOMIC PROTOCOL** — verify
> that the V2.0.0 staged dataflow is consistent with the frozen V1.1.0 economic
> registry, that the bounded-residency model and exactly-once/non-resumable
> Stage-2 semantics are precisely registrable and free of ambiguity, and that no
> scientific/economic object changed. Only after that audit passes may staged
> execution infrastructure be implemented and audited. No Stage-1 generation, no
> Stage-2 run, and no economic judgment may be claimed from this report.

---

## 16. Integrity

- Strictly READ-ONLY with respect to all scientific objects, all frozen
  economic rules, and the V1.0.0 / V1.1.0 protocol texts (all retained
  unmodified).
- No economic simulation, PnL, trade statistics, viability, optimization, or
  outcome inspection was performed at any point.
- The only new repository artifacts of this amendment are:
  `ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_AMENDED.md` and this report.
- A stale execution (`…cff4a63e`) was formally reconciled as CRASHED via the
  approved tool; its partial artifacts are preserved; nothing was deleted.
- No code was written or executed against the frozen objects; no commit; no
  push.

---

*End of report — ORD ECONOMIC TRANSLATION PROTOCOL V2 AMENDMENT REPORT.*