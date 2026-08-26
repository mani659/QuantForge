# QUANTFORGE — ORD ECONOMIC / STRATEGY TRANSLATION PROTOCOL V2.0.0 (AMENDED — STAGED EXECUTION DATAFLOW)

FROZEN BEFORE COMPUTATION. This document amends
`ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md` **for execution dataflow and
provenance ONLY**. No scientific or economic decision is changed. The economic
experiment remains exactly ONE baseline experiment, executed exactly once.

**V2.0.0 is a dataflow/provenance-only amendment of the frozen V1.1.0
protocol.** It registers the staged-execution architecture mandated by
`output/research_discovery/ORD_ECONOMIC_EXECUTION_STAGING_DESIGN_V1.md`
(verdict **B — STAGED EXECUTION REQUIRED**), which was itself grounded in two
failed controlled monolithic executions
(`EXECUTION_20260820T074818Z_2d5555f0…`, `EXECUTION_20260820T082217Z_cff4a63e…`,
both **CRASHED / NOT_ADJUDICABLE**). **Every entry, entry-bridge, stop, horizon,
MFE/MAE, cost-model, Model A / Model B, primary economic metric, viability gate,
OOS split, market-universe, BTCUSD-caveat, and EURUSD-exclusion rule of V1.1.0 is
preserved unchanged.** This document supersedes the V1.1.0 text only in the
mechanics of *how the computer safely prepares and executes* the frozen
baseline; the V1.1.0 document is retained unmodified and is not overwritten.

---

## 0. Identity and Scope

- **Stage:** post-adjudication economic / strategy translation of the ORD
  V1.1.0 behavioral result — now executed through a staged, bounded-memory,
  crash-safe dataflow.
- **Version:** V2.0.0 (staged-execution dataflow/provenance amendment of
  V1.1.0).
- **Amendment source:** `output/research_discovery/ORD_ECONOMIC_EXECUTION_STAGING_DESIGN_V1.md`
  — **B — STAGED EXECUTION REQUIRED** (crash/resource audit §2, resource
  analysis §3, monolithic unsafety proof §4–§5, staged design §6–§13).
- **Frozen base protocol (incorporated unchanged, NOT restated):**
  `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md`
  (V1.1.0, SHA-256 `8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663`).
  Its §§1–18 (Executive Verdict; Scientific Object; Baseline Entry; Execution
  Bridge; Structural Invalidation; Horizon Exit; Cost Model; Position/Notional;
  Trade Accounting; Data Gates; Dev/OOS Split; Primary Metric; Viability Gates;
  Cross-Market Reporting; Year/Half Stability; Reproducibility; Machine-Safety
  Controls; Economic Firewall) remain fully in force and unchanged.
- **Original frozen protocol (superseded in text, preserved unmodified):**
  `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1.md`
  (V1.0.0, SHA-256 `50A08AAF4744A793CF5F0793E7AD104BB6EB5D04EA7EB82FE56DB30587FF74F2`).
- **Authorizing adjudication (unchanged):**
  `output/research_discovery/ORD_SCIENTIFIC_RESULTS_ADJUDICATION_V1.md` —
  **A — SCIENTIFICALLY SUPPORTED** (XAUUSD, XAGUSD, USATECHIDXUSD SUPPORT;
  BTCUSD scientifically HALTED; EURUSD NOT REGISTERED / DATA-LIMITED).
- **Frozen scientific protocol (unchanged):**
  `output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md`
  (V1.1.0, SHA-256 `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06`).
- **Frozen definition lock (unchanged):**
  `output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md`.
- **Scientific execution (authoritative source of events, unchanged):**
  `output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/`
  (state COMPLETED; manifests `missing_artifacts=[]`, `unexpected_artifacts=[]`).
- **Baseline registration:** unchanged — one baseline implementation only. No
  alternative entry/exit/stop is tested. No parameter search, no ML, no EA, no
  demo/live. Staging is an execution-engineering mechanism, NOT multiple
  strategy trials (§9).
- **Protocol identity:** this document. Its SHA-256 is computed and persisted by
  the V2 amendment report and re-verified by every subsequent stage.
- **Version history:**
  - **V1.0.0** — frozen baseline economic translation (original text).
  - **V1.1.0** — precision-only amendment resolving execution-quote
    look-ahead, tick timezone, floating-point validation, gap-through stop
    fills, horizon boundary behavior, MFE/MAE source semantics, cumulative-net
    definition, profit-factor boundary cases, and exactly-once execution
    inheritance. No scientific or economic object changed.
  - **V2.0.0** — staged-execution dataflow/provenance amendment: Stage 0
    preflight; Stage 1 frozen economic-input preparation with bounded quote
    aggregation residency; immutable hashed preparation artifacts; Stage 2 as
    the sole controlled economic execution (exactly once, non-resumable); Stage
    3 read-only verification; restart/reuse rules; non-resumability; historical
    preservation; and hardened provenance. **No scientific or economic decision
    changed.**

---

## 1. Amendment Scope (what changes and what does not)

### 1.1 NOT changed (frozen, incorporated from V1.1.0)

The following are registered as byte-frozen and **identical** to V1.1.0:

1. Scientific object being translated (V1.1.0 §2).
2. Baseline entry definition and breakout-close semantics (V1.1.0 §3).
3. Execution bridge: `T_B = anchor_ts + 60 s`; first eligible tick minute at/after
   `T_B`; median ASK for LONG / median BID for SHORT; exact → ±5 fallback →
   market-median → `EXCLUDED_NO_QUOTE_COVERAGE` (V1.1.0 §4).
4. Structural invalidation windows (London 03:00–03:29 ET for XAUUSD/XAGUSD/
   BTCUSD; US 09:30–09:59 ET for USATECHIDXUSD), `High_OR`/`Low_OR`
   reconstruction, `range_width` cross-check, close-triggered stop, trigger-side
   executable fill, gap-through at actual quote, no backfill/buffer (V1.1.0 §5).
5. 120-minute literal wall-clock horizon, horizon exit (median BID / ASK),
   fallback chain, horizon-completeness exclusion (V1.1.0 §6).
6. Observed-spread cost model: median bid/ask per minute; spread in bp; Model A
   `RT(A) = (s_entry + s_exit)/2`; Model B descriptive `RT(B) = s_entry + s_exit`;
   commission/slippage bands descriptive only (V1.1.0 §7, §12).
7. Position / notional convention; basis-point returns; gross/net definitions
   (V1.1.0 §8).
8. Trade accounting, ledger columns, algebraic identity cross-check
   `tol_rel = 1e-6`, MFE/MAE source semantics (`mfe ≥ 0`, `mae ≤ 0`), retention
   of `EXCLUDED_*` rows (V1.1.0 §9).
9. Data gates, exclusions reported never silent (V1.1.0 §10).
10. Development/OOS split: chronological first 50% of event days = DEV, last 50%
    = OOS (V1.1.0 §11).
11. Primary economic metric (median net bp, Model A), cumulative net (chronological
    sum), profit factor with `+∞`/`0`/`NaN` boundaries (V1.1.0 §12).
12. Economic viability gates 1–5 and classifications, BTCUSD NO-SCIENTIFIC-VERDICT
    caveat, EURUSD NOT SIMULATED, overall disposition, cross-market structure
    (V1.1.0 §13, §14).
13. Year/half stability reporting (V1.1.0 §15).
14. Economic firewall: nothing outside the registered baseline is tested (V1.1.0
    §18).

### 1.2 Changed (this amendment)

1. **Reproducibility (§16 of V1.1.0) is implemented through staged artifact
   directories** (Stage 0 `PREFLIGHT_*`, Stage 1 `PREP_<market>_<hash>`, Stage 2
   `EXECUTION_<timestamp>_<UUID>`, Stage 3 `VERIFICATION_*`) while preserving the
   same persisted content: identities, protocol/runner/data hashes, cost-model
   identity, ledgers, summaries, dev/OOS, yearly results, metadata, report.
2. **Machine-safety controls (§17 of V1.1.0) are strengthened into a bounded
   residency model** — details in §§2–8 below. The prohibition set is widened
   from "never load a full tick file or a full minutes table" to: **at most one
   minute of tick observations resident for quote aggregation** in Stage 1
   (§6.1), with per-market event-join state explicitly bounded.
3. **Exactly-once semantics are explicitly attributed to Stage 2** (the sole
   economic execution); Stages 0/1/3 are repeatable/restartable/read-only as
   registered (§9, §10).

---

## 2. Staged Dataflow Model (registered)

```
raw data
  → Stage 0  PRE-FLIGHT            (repeatable, non-scientific health check)
  → Stage 1  FROZEN INPUT PREP     (bounded residency; immutable hashed inputs)
  → Stage 2  THE ONE ECONOMIC EXECUTION   (exactly once, non-resumable)
  → Stage 3  READ-ONLY VERIFICATION (repeatable certification)
  → INDEPENDENT ECONOMIC RESULTS ADJUDICATION (next governance task, unchanged)
```

No stage writes into another stage's directory. No stage may overwrite any
historical execution or preparation.

---

## 3. Stage 0 — PRE-FLIGHT (repeatable, non-scientific)

Registered per market (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD) and non-scientific:

- source file existence;
- source SHA-256 (streamed, 1 MiB chunks);
- schema check (`date,time,bid,ask,last,vol`, headerless);
- row count (exact, single line-buffered pass);
- timestamp format (`YYYYMMDD,HH:MM:SS`) and quote sanity (non-finite / ≤0 /
  `bid>ask` counters);
- environment and resource capability (RAM, free disk, peak-RSS streaming probe).

Output directory: `output/research_discovery/ORD_ECONOMIC/V1.1.0/PREFLIGHT_<market>/`
(`preflight.json`, `stage0_manifest.json`, stage journal).

- Stage 0 computes **no economic result** and may be repeated freely.
- A failed Stage 0 is reconciled; a re-run creates a new `PREFLIGHT_*` identity.
- Stage 0 does not register an execution identity in the economic lineage.

---

## 4. Stage 1 — FROZEN ECONOMIC INPUT PREPARATION

Registered: process **ONE market at a time**. Stage 1 converts the raw tick file
into a compact, immutable, hashable intermediate containing only the
deterministic inputs the economic simulation needs:

- market; source tick SHA-256; source M1 SHA-256; economic protocol SHA-256
  (V1.1.0); preparation implementation SHA-256;
- event ID; trading day; direction; breakout timestamp; `T_B`;
- eligible entry quote-minute, executable entry quote, entry spread;
- structural stop (trigger-bar metadata and, where deterministically derivable
  in the single pass, the first trigger-side executable quote);
- horizon timestamp; exit-lookup metadata; preparation schema version;
- per-minute quote aggregation metadata (minute key, median bid, median ask,
  `nticks`).

Stage 1 **does NOT** calculate: economic viability, PnL, profit factor, economic
classification, or any optimization metric.

### 4.1 Bounded quote aggregation residency (hard requirement)

> The implementation must maintain bounded residency, with the design target:
> **at most one minute of tick observations resident for quote aggregation,
> except for the small deterministic event-join state required for that
> market.**

- Tick files are read line-buffered, one line at a time; the current minute's
  ticks are reduced to per-minute medians on minute-rollover and then discarded.
- No full tick file, no per-market "minutes table", and no per-market
  accumulated minute-bucket may be resident at any time.
- No prescriptive chunk size is mandated; the bound derives from the data model
  (one-minute reduction), not from tuning.
- Stage 1 records peak RSS in its manifest and fails-closed on a resource
  incident without modifying any scientific/economic rule (V1.1.0 §17.6
  preserved).

### 4.2 Stage-1 output identity

- Deterministic preparation identity: **`PREP_<market>_<hash>`**, where `<hash>`
  binds the frozen preparation inputs.
- Output directory:
  `output/research_discovery/ORD_ECONOMIC/V1.1.0/PREP_<market>_<hash>/`
  containing: preparation manifest; source hashes; protocol hash;
  implementation hash; schema version; frozen event/input table; quote
  aggregation metadata; artifact hashes.
- **No preparation directory may overwrite an existing preparation** (`exist_ok
  = False` semantics).

---

## 5. Stage-1 Restartability / Reuse Rule

> A completed Stage-1 preparation may be reused ONLY when its persisted
> metadata and hashes match the current frozen economic protocol, source data,
> preparation implementation, and schema version **exactly**.

- If any identity differs (protocol SHA, source M1/tick SHA, implementation
  SHA, schema version): **Stage 1 must be regenerated**.
- A Stage-1 artifact is **not scientific/economic evidence by itself**; it is a
  frozen input to Stage 2.
- A partial/crashed Stage-1 directory is never reused; it is re-run and
  reconciled, and is never mistaken for a completed preparation.

---

## 6. Stage 2 — THE ONE CONTROLLED ECONOMIC EXECUTION

> **Stage 2 is the sole controlled economic execution.**

- Stage 2 consumes **ONLY**:
  - frozen Stage-1 inputs (`PREP_<market>_<hash>` metadata and tables);
  - the frozen economic protocol (V1.1.0 incorporated unchanged, §0/§1);
  - approved execution infrastructure (isolation, heartbeat, journal,
    mutation guard, artifact gate).
- Stage 2 calculates: trade ledger; gross/net; Model A; Model B descriptive
  sensitivity; MFE/MAE; cumulative net; PF; OOS; yearly results; viability
  gates — all exactly as registered in V1.1.0 §§9–13 and the ledger column
  contract (§9).
- Stage 2 is **exactly once / non-resumable**.
- If Stage 2 crashes: **CRASHED / NOT_ADJUDICABLE**. It must **never** resume
  from partial economic calculations, and its identity must never be reused.

### 6.1 Stage-2 identity persistence

Stage 2 must persist:
- execution UUID (`EXECUTION_<timestamp>_<UUID>`);
- Stage-1 preparation hashes (consumed `PREP_<market>_<hash>`);
- economic protocol hash (V1.1.0 + this V2.0.0 document);
- implementation hash; Git HEAD; environment; process identity; heartbeat.

A mismatch of any required identity **invalidates the execution before any
economic calculation** (fail-closed; V1.1.0 §17 and EventStudyRecorder mutation
guard preserved).

---

## 7. Stage 3 — READ-ONLY VERIFICATION

- Stage 3 verifies: Stage-1 hashes; Stage-2 ledger; formulas; market
  completeness; OOS; year summaries; viability gates; artifacts.
- Stage 3 **cannot modify** scientific or economic results; it certifies them.
- Output: `VERIFICATION_<execution-id>/` (verification report + manifest).
- Stage 3 creates no economic evidence and no new trade/statistic.

---

## 8. Historical Preservation

- All prior executions remain immutable; prior CRASHED executions remain
  forensic (`…2d5555f0` CRASHED; `…cff4a63e` CRASHED — reconciled via
  `reconcile_execution.py`, NOT_ADJUDICABLE).
- Stage-1 preparation artifacts are immutable once finalized.
- A new run always receives a new identity.
- **No shared destructive output directory.**

---

## 9. Exactly-Once Governance (registered)

| Stage | Repeatable? | Economic evidence? | Resume/reuse |
|---|---|---|---|
| Stage 0 Preflight | **Yes** | No | restartable; fresh identity each run |
| Stage 1 Preparation | **Yes** (idempotent) | No | restartable; **reusable ONLY when hashes match exactly** |
| Stage 2 Evaluation | **Single controlled run** | **Yes** | **NON-RESUMABLE**; new identity only after governance authorizes another controlled attempt |
| Stage 3 Verification | **Yes** | No (certifies) | restartable read-only |

- No stage may overwrite another execution.
- No failed Stage-2 execution may become a successful execution through partial
  resumption.
- Staging is an execution-engineering mechanism, not multiple strategy trials:
  the final experiment is **ONE CONTROLLED BASELINE ECONOMIC EXECUTION**.

---

## 10. Crash Reconciliation (unchanged mechanism, applied to stages)

- Every stage carries identity + isolated directory + heartbeat + process
  identity + artifact manifest + fail-closed finalization.
- Reconciliation uses the approved mechanism
  (`scripts/reconcile_execution.py` semantics): process-death detection via PID +
  create-time + boot-time; terminal `CRASHED` state; preserved partial artifacts
  with hashes; `scientific_validity=false`;
  `scientific_adjudication=NOT_ADJUDICABLE`.
- A crashed Stage 1 is never mistaken for completed economic evidence.
- A crashed Stage 2 is NON-ADJUDICABLE.

---

## 11. Self-Audit (amendment scope verification)

V2.0.0 changes **NO**:
- entry; entry bridge; stop; horizon; MFE/MAE; cost model; Model A; Model B;
  primary economic metric; viability gates; OOS split; market scope (XAUUSD,
  XAGUSD, USATECHIDXUSD, BTCUSD simulated; EURUSD NOT SIMULATED); BTCUSD
  NO-SCIENTIFIC-VERDICT caveat; baseline strategy; any scientific object or
  decision.

V2.0.0 changes **ONLY**:
- execution architecture (staged dataflow) and provenance (hashing, identities,
  restart/reuse rules, non-resumability, historical preservation, bounded quote
  aggregation residency).

> **No scientific or economic decision changed.**

---

## 12. Exact Next Task

> After this document is frozen and its SHA-256 recorded: an **INDEPENDENT
> READ-ONLY AUDIT OF THE V2 STAGED ECONOMIC PROTOCOL** (verification that the
> staged dataflow is consistent with the frozen V1.1.0 economic registry, that
> the bounded-residency model is registrable, and that no scientific/economic
> object changed). ONLY after that audit passes may staged execution
> infrastructure be implemented and audited. No execution, no Stage-1
> generation, no Stage-2 run, no audit, and no economic judgment may be claimed
> from this document alone.

---

## 13. Integrity

- Strictly READ-ONLY with respect to all scientific objects and all frozen
  economic rules: ORD scientific protocol, definition lock, execution artifacts,
  event table, statistics, manifests, adjudication, governance records, and the
  V1.0.0 / V1.1.0 economic protocol texts are untouched.
- No M1 reprocessing into scientific objects; no bootstrap/null/event
  regeneration; no PnL computed here.
- The only new repository artifacts from this amendment are this V2.0.0
  document and its amendment report.
- V2.0.0 is a dataflow/provenance-only amendment: it changes no scientific or
  economic object, market, opening-range definition, breakout definition, entry
  concept, structural invalidation, 120-minute horizon, observed-spread cost
  model, primary economic metric, viability gates, development/OOS split,
  year-concentration gate, Model B sensitivity, or baseline strategy. It only
  changes how the computer safely prepares and executes the frozen baseline.
- All economic rules, fills, costs, gates, and classifications remain as
  registered in V1.1.0 — BEFORE computation; no value, parameter, or threshold
  was or is informed by any economic backtest on ORD events.
- This protocol does not authorize trading, demo, or deployment of any kind.