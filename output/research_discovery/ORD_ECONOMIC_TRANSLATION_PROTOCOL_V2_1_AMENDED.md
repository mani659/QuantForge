# QUANTFORGE — ORD ECONOMIC / STRATEGY TRANSLATION PROTOCOL V2.0.1 (AMENDED — STAGED EXECUTION DATAFLOW, PRECISION RESOLUTIONS W1–W4)

FROZEN BEFORE COMPUTATION. This document amends
`ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_AMENDED.md` (V2.0.0) **for execution
dataflow, provenance, and precision ONLY**. No scientific or economic decision
is changed. The economic experiment remains exactly ONE baseline experiment,
executed exactly once.

**V2.0.1 is a precision-only amendment of V2.0.0.** It applies exactly the four
precision findings returned by the independent audit of V2.0.0
(**B — CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED**):

- **W2** — market-median fallback universe not explicitly frozen;
- **W4** — preparation identity hash inputs/order/algorithm not uniquely
  defined;
- **W1** — "at most one minute of tick observations resident" wording not
  formally measurable;
- **W3** — Stage 0 / Stage 1 infrastructure failures must not be confused with
  economic `EXCLUDED_*` outcomes.

It does NOT restate, modify, or re-derive any V1.1.0 economic rule. **Every
entry, entry-bridge, stop, horizon, MFE/MAE, cost-model, Model A / Model B,
primary economic metric, viability gate, OOS split, market-universe, BTCUSD
caveat, and EURUSD-exclusion rule of V1.1.0 is preserved unchanged.** The V2.0.0
document is retained unmodified and is not overwritten; the V1.1.0 document is
retained unmodified and is not overwritten.

---

## 0. Identity and Scope

- **Stage:** post-adjudication economic / strategy translation of the ORD
  V1.1.0 behavioral result — executed through a staged, bounded-memory,
  crash-safe dataflow.
- **Version:** V2.0.1 (precision-only amendment of V2.0.0, resolving W1–W4;
  staged-execution dataflow/provenance amendment of V1.1.0).
- **Amendment source:** the independent audit of V2.0.0
  (verdict **B — CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED**; findings
  W1–W4) and the staging architecture
  `output/research_discovery/ORD_ECONOMIC_EXECUTION_STAGING_DESIGN_V1.md`
  (**B — STAGED EXECUTION REQUIRED**).
- **Immediate frozen base protocol (this document supersedes its text):**
  `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_AMENDED.md`
  (V2.0.0, SHA-256
  `85D4E1D1BD6AFB35B51FEEEC92DAE8EF98782AC95C3C6BD6126F28ED0E0B021C`),
  retained unmodified.
- **Frozen economic base protocol (incorporated unchanged, NOT restated):**
  `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md`
  (V1.1.0, SHA-256
  `8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663`).
  Its §§1–18 (Executive Verdict; Scientific Object; Baseline Entry; Execution
  Bridge; Structural Invalidation; Horizon Exit; Cost Model; Position/Notional;
  Trade Accounting; Data Gates; Dev/OOS Split; Primary Metric; Viability Gates;
  Cross-Market Reporting; Year/Half Stability; Reproducibility; Machine-Safety
  Controls; Economic Firewall) remain fully in force and unchanged. V1.1.0 §4
  (Execution Bridge, incl. the market-median fallback) and V1.1.0 §17
  (Machine-Safety Controls) are the references binding §§4.3 and §4.5 below.
- **Original frozen protocol (superseded in text, preserved unmodified):**
  `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1.md`
  (V1.0.0, SHA-256
  `50A08AAF4744A793CF5F0793E7AD104BB6EB5D04EA7EB82FE56DB30587FF74F2`).
- **Authorizing adjudication (unchanged):**
  `output/research_discovery/ORD_SCIENTIFIC_RESULTS_ADJUDICATION_V1.md` —
  **A — SCIENTIFICALLY SUPPORTED** (XAUUSD, XAGUSD, USATECHIDXUSD SUPPORT;
  BTCUSD scientifically HALTED; EURUSD NOT REGISTERED / DATA-LIMITED).
- **Frozen scientific protocol (unchanged):**
  `output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md`
  (V1.1.0, SHA-256
  `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06`).
- **Frozen definition lock (unchanged):**
  `output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md`.
- **Scientific execution (authoritative source of events, unchanged):**
  `output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/`
  (state COMPLETED; manifests `missing_artifacts=[]`, `unexpected_artifacts=[]`).
- **Baseline registration:** unchanged — one baseline implementation only. No
  alternative entry/exit/stop is tested. No parameter search, no ML, no EA, no
  demo/live. Staging is an execution-engineering mechanism, NOT multiple
  strategy trials (§9).
- **Protocol identity:** this document. Its full SHA-256 is computed at
  finalization, recorded unabbreviated in the V2.0.1 amendment report, and
  re-verified by every subsequent stage.
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
  - **V2.0.1** — precision-only amendment resolving (1) the complete
    market-minute universe for market-median quote fallback; (2) deterministic
    SHA-256 preparation identity construction; (3) bounded-memory residency
    semantics; (4) explicit separation of execution-infrastructure failures
    from economic trade exclusions. **No scientific or economic decision
    changed.**
  - **V2.0.1-r1** — materialization correction: inserted the previously
    referenced §4.5 `EXECUTION-INFRASTRUCTURE FAILURE CLASSIFICATION` into the
    protocol body. No scientific, economic, staging, or provenance rule
    changed.

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

### 1.2 Changed by V2.0.0 (retained in force)

1. **Reproducibility (§16 of V1.1.0) is implemented through staged artifact
   directories** (Stage 0 `PREFLIGHT_*`, Stage 1 `PREP_<market>_<hash>`, Stage 2
   `EXECUTION_<timestamp>_<UUID>`, Stage 3 `VERIFICATION_*`) while preserving the
   same persisted content: identities, protocol/runner/data hashes, cost-model
   identity, ledgers, summaries, dev/OOS, yearly results, metadata, report.
2. **Machine-safety controls (§17 of V1.1.0) are strengthened into a bounded
   residency model** — details in §§2–8 below.
3. **Exactly-once semantics are explicitly attributed to Stage 2** (the sole
   economic execution); Stages 0/1/3 are repeatable/restartable/read-only as
   registered (§9, §10).

### 1.3 Changed by V2.0.1 (this amendment — precision ONLY)

1. **W1 — Bounded-memory residency semantics** are reworded as a formally
   measurable bounded streaming constraint on Stage 1 (§4.1). This is an
   infrastructure safety constraint, not an economic parameter.
2. **W2 — Market-median fallback universe** is explicitly frozen to the complete
   set of eligible per-minute quote aggregates for ALL observed minutes of the
   same market (§4.3). This is a provenance clarification only.
3. **W3 — Infrastructure-failure classification** explicitly separates
   execution-infrastructure failures (`EXECUTION-INFRASTRUCTURE FAILURE`) from
   registered economic `EXCLUDED_*` outcomes (§4.5).
4. **W4 — Preparation identity hash** is uniquely defined: SHA-256 over a
   canonical, byte-stable manifest with a frozen field set and order; the
   preparation identity uses the full 64-character hash (§4.4).

No V1.1.0 economic rule is touched by any of the four resolutions.

---

## 2. Staged Dataflow Model (registered)

```
raw data
  → Stage 0  PRE-FLIGHT            (repeatable, non-scientific health check)
  → Stage 1  FROZEN INPUT PREP     (bounded streaming; immutable hashed inputs)
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
- Stage 0 failure classification follows §4.5: an infrastructure failure is
  `EXECUTION-INFRASTRUCTURE FAILURE`, never an economic outcome.

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
  `nticks`) **for ALL observed minutes of that market** (see §4.3 for the
  binding market-median fallback universe).

Stage 1 **does NOT** calculate: economic viability, PnL, profit factor, economic
classification, or any optimization metric.

### 4.1 Bounded-memory residency — formally measurable (W1 resolution)

> Stage 1 MUST process tick data as a bounded streaming aggregation. At no
> point may it retain the complete market-wide per-minute quote table or an
> equivalent structure whose size grows O(number_of_minutes). Tick-derived
> aggregation state MUST remain O(size_of_current_minute), plus the bounded
> deterministic event-join state required for the registered market/event
> population.

Clarified and binding:

- Stage 1 may maintain the current minute's tick observations;
- it may retain small fixed-size event-join structures (the bounded
  deterministic event-join state required for the registered market/event
  population);
- it may emit finalized per-minute aggregates immediately to disk on
  minute-rollover, then discard the current minute's observations;
- it MUST NOT accumulate an entire market's minute aggregates in RAM.

This is an infrastructure safety constraint, not an economic parameter. No
arbitrary RAM number is prescribed. Tick files are read line-buffered, one line
at a time; no full tick file, no per-market "minutes table", and no per-market
accumulated minute-bucket may be resident at any time. No prescriptive chunk
size is mandated; the bound derives from the data model (one-minute reduction),
not from tuning. Stage 1 records peak RSS in its manifest and fails-closed on a
resource incident without modifying any scientific/economic rule (V1.1.0 §17.6
preserved).

### 4.2 Stage-1 output identity

- Deterministic preparation identity: **`PREP_<market>_<hash>`**, where `<hash>`
  is the full 64-character SHA-256 defined in §4.4.
- Output directory:
  `output/research_discovery/ORD_ECONOMIC/V1.1.0/PREP_<market>_<hash>/`
  containing: preparation manifest; source hashes; protocol hash;
  implementation hash; schema version; frozen event/input table; quote
  aggregation metadata; artifact hashes.
- **No preparation directory may overwrite an existing preparation** (`exist_ok
  = False` semantics).

### 4.3 Market-median fallback universe — frozen (W2 resolution)

The V1.1.0 execution-bridge fallback chain (exact → ±5 min → market-median) is
unchanged. Its final fallback is hereby bound precisely:

> The market-median fallback is computed from the complete set of eligible
> per-minute quote aggregates for ALL observed minutes of the same market in the
> registered tick dataset, after the protocol's deterministic tick-quality
> rules have been applied. The fallback universe is not restricted to event
> minutes, entry/exit windows, successful lookups, or Stage-1 event-related
> minutes.

Frozen semantics:

- exact population = all eligible observed minutes for that market;
- same quote-side semantics as V1.1.0 (median ASK for LONG / median BID for
  SHORT at the fallback reference);
- same tick-quality filtering as V1.1.0 (the deterministic tick-quality rules of
  the execution bridge);
- the market median is fixed for the source dataset/preparation — it is a
  deterministic function of the frozen inputs, not of any event subset;
- no performance-based filtering: no minutes are excluded because of economic
  relevance, trade outcome, or lookup success.

This is a provenance clarification only. It makes two independent
implementations compute the identical market-median value.

### 4.4 Preparation identity hash — uniquely defined (W4 resolution)

The preparation identity `PREP_<market>_<hash>` MUST be reproducible by any
independent implementation. The `<hash>` is defined as follows.

#### 4.4.1 Hash algorithm

**SHA-256** (FIPS 180-4), computed over the canonical manifest serialization of
§4.4.3. The result is the full 64-character uppercase-hex digest.

#### 4.4.2 Canonical input manifest

The preparation hash MUST be computed over a canonical, byte-stable manifest
containing **exactly** these nine fields, in this fixed order:

1. market identifier;
2. Stage-1 schema version;
3. economic protocol SHA-256;
4. scientific protocol SHA-256;
5. source M1 SHA-256;
6. source tick SHA-256;
7. preparation implementation SHA-256;
8. canonical Stage-1 parameter manifest;
9. preparation code/schema version.

The exact bytes hashed must therefore be uniquely reconstructable from the
production inputs alone.

#### 4.4.3 Canonical serialization (byte-stable)

The canonical manifest is serialized deterministically as follows, using only
the values above and no environment-dependent content:

- encoding: UTF-8 (no BOM);
- one field per line;
- fixed field ordering (the order of §4.4.2);
- field names included, `key=value\n` per line, no trailing blank line beyond a
  single trailing newline after the last field;
- lexical/canonical normalization of each value;
- **no** timestamps;
- **no** machine-specific paths;
- **no** usernames;
- **no** environment-dependent values.

Freezing the exact field order and serialization above makes the digest
identical across independent implementations.

#### 4.4.4 Identity construction

- The preparation identity uses the **full 64-character SHA-256**:
  `PREP_<market>_<sha256-hex>` (uppercase hex, e.g. `PREP_XAUUSD_<64 hex>`).
- The full hash is recorded unabbreviated in the preparation manifest.
- The exact bytes hashed are uniquely reconstructable from the production inputs
  alone (per §4.4.2–§4.4.3).
- No truncation of the digest in any directory name, manifest, or Stage-2
  provenance record.

### 4.5 Execution-infrastructure failure classification (W3 resolution)

The protocol distinguishes two disjoint classes of failure outcomes.

#### 4.5.1 Economic exclusions

Economic exclusions are **ONLY** the registered V1.1.0/V2 economic trade
outcomes, such as:

- `EXCLUDED_NO_QUOTE_COVERAGE`;
- `EXCLUDED_HORIZON_INCOMPLETE`;
- and other explicitly registered economic exclusion states.

These remain governed by the frozen economic rules (V1.1.0 §10 data gates,
exclusions reported, never silent).

#### 4.5.2 Execution-infrastructure failures

Stage 0 and Stage 1 infrastructure failures, including:

- out-of-memory / resource exhaustion;
- disk / filesystem failure;
- parser / process failure;
- protocol / source / implementation hash mismatch;
- corrupted preparation artifact;
- process crash;
- stale heartbeat;
- infrastructure exception;
- preparation integrity failure.

These MUST be classified uniformly as **`EXECUTION-INFRASTRUCTURE FAILURE`**
and MUST NOT be encoded as economic exclusions.

#### 4.5.3 Five consequences (binding)

An execution-infrastructure failure:

1. does not create an economic result;
2. does not become a losing trade;
3. does not reduce the economic sample;
4. does not trigger economic classification;
5. does not modify the frozen economic dataset.

> This classification applies uniformly to Stage 0 and Stage 1 infrastructure
> failures. Stage 2 failures remain governed by the exactly-once execution and
> crash-reconciliation rules.

No new economic decision is added by this classification.

---

## 5. Stage-1 Restartability / Reuse Rule

> A completed Stage-1 preparation may be reused ONLY when its persisted
> metadata and hashes match the current frozen economic protocol, source data,
> preparation implementation, and schema version **exactly**.

- If any identity differs (protocol SHA, source M1/tick SHA, implementation
  SHA, schema version): **Stage 1 must be regenerated**.
- The preparation `<hash>` itself (per §4.4) is part of the match: two
  preparations with different `<hash>` values are different identities and may
  not substitute for each other.
- A Stage-1 artifact is **not scientific/economic evidence by itself**; it is a
  frozen input to Stage 2.
- A partial/crashed Stage-1 directory is never reused; it is re-run and
  reconciled, and is never mistaken for a completed preparation. A crashed or
  corrupted Stage-1 directory is classified per §4.5.

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
- Stage 2 reads the full `PREP_<market>_<hash>` SHA-256 (§4.4) and re-verifies
  it before any economic calculation (fail-closed).

### 6.1 Stage-2 identity persistence

Stage 2 must persist:
- execution UUID (`EXECUTION_<timestamp>_<UUID>`);
- Stage-1 preparation hashes (consumed `PREP_<market>_<hash>`, unabbreviated);
- economic protocol hash (V1.1.0 + this V2.0.1 document);
- implementation hash; Git HEAD; environment; process identity; heartbeat.

A mismatch of any required identity **invalidates the execution before any
economic calculation** (fail-closed; V1.1.0 §17 and EventStudyRecorder mutation
guard preserved).

---

## 7. Stage 3 — READ-ONLY VERIFICATION

- Stage 3 verifies: Stage-1 hashes (incl. the full preparation `<hash>` per
  §4.4); Stage-2 ledger; formulas; market completeness; OOS; year summaries;
  viability gates; artifacts.
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

### 11.1 Zero-economic-change verification

V2.0.1 changes **NO**:

- market universe (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD simulated; EURUSD NOT
  SIMULATED);
- entry;
- `T_B`;
- quote bridge;
- fallback logic;
- stop;
- gap-through behavior;
- horizon;
- MFE/MAE;
- Model A;
- Model B;
- primary median-net metric;
- cumulative net;
- profit factor;
- year concentration;
- OOS gate;
- the five economic viability gates;
- BTCUSD NO-SCIENTIFIC-VERDICT caveat;
- EURUSD exclusion;
- trade accounting.

### 11.2 Scope of change

V2.0.1 changes **ONLY** the four precision items W1–W4 (§1.3), i.e. the formal
definition of bounded-memory residency (§4.1), the frozen market-median fallback
universe (§4.3), the unique preparation-hash construction (§4.4), and the
explicit separation of infrastructure failures from economic exclusions (§4.5).
All V2.0.0 staged-execution semantics (Stage 0/1/2/3, exactly once,
non-resumable Stage 2, no overwrite, no reuse of failed Stage-2 identity,
historical preservation) are preserved unchanged.

> **No scientific or economic decision changed.**

---

## 12. Outcome-Blindness

- No value, parameter, threshold, gate, or classification in V2.0.1 was informed
  by any economic backtest, PnL observation, market ranking, or historical trade
  outcome on ORD events.
- V2.0.1 resolves four precision findings produced by an independent,
  read-only audit of V2.0.0 — not by any performance-derived preparation design.
- No viability threshold changed; no economic result exists yet.
- The economic experiment remains exactly one baseline, allowed to succeed or
  fail on its own.

---

## 13. Integrity

- Strictly READ-ONLY with respect to all scientific objects and all frozen
  economic rules: ORD scientific protocol, definition lock, execution artifacts,
  event table, statistics, manifests, adjudication, governance records, and the
  V1.0.0 / V1.1.0 / V2.0.0 protocol texts are untouched.
- No M1 reprocessing into scientific objects; no bootstrap/null/event
  regeneration; no PnL computed here.
- The only new repository artifacts from this amendment are this V2.0.1 document
  and its amendment report.
- V2.0.1 is a precision-only amendment: it changes no scientific or economic
  object, market, opening-range definition, breakout definition, entry concept,
  structural invalidation, 120-minute horizon, observed-spread cost model,
  primary economic metric, viability gates, development/OOS split,
  year-concentration gate, Model B sensitivity, or baseline strategy. It only
  makes the already-approved staged execution architecture uniquely
  reproducible.
- All economic rules, fills, costs, gates, and classifications remain as
  registered in V1.1.0 — BEFORE computation; no value, parameter, or threshold
  was or is informed by any economic backtest on ORD events.
- This protocol does not authorize trading, demo, or deployment of any kind.

---

## 14. Exact Next Task

> After this document is frozen and its full SHA-256 recorded unabbreviated in
> its amendment report: an **INDEPENDENT READ-ONLY RE-AUDIT OF ORD ECONOMIC
> TRANSLATION V2.0.1** (verification that W1–W4 are resolved precisely, that all
> V2.0.0 staged-execution semantics are preserved, and that no
> scientific/economic object changed). ONLY after that audit returns PASS may
> staged execution infrastructure be implemented and audited. No execution, no
> Stage-0 run, no Stage-1 generation, no Stage-2 run, no audit, and no economic
> judgment may be claimed from this document alone.

---

*FROZEN BEFORE COMPUTATION. No economic simulation, PnL, trade statistics,
viability, optimization, or outcome inspection was performed at any point. The
research object remains frozen.*