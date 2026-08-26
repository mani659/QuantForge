# QUANTFORGE — ORD ECONOMIC EXECUTION
# CRASH / RESOURCE AUDIT + STAGED EXECUTION DESIGN V1

Status: INFRASTRUCTURE / EXECUTION-DESIGN ONLY (read-only audit + design).
No economic simulation, no PnL/trade-stat/viability computation, no protocol
amendment, no runner/recorder modification, no EA, no commit, no push.

---

## 1. Executive Verdict

**DECISION: B — STAGED EXECUTION REQUIRED.**

The monolithic economic execution architecture

`raw tick CSV → load massive dataset → derive quotes → simulate trades →
calculate metrics → next market`

is **resource-unsafe on the current host** and was the direct cause of two
failed controlled executions. Both failures occurred during the **XAUUSD**
per-minute tick-materialization phase in memory — the first as a pandas C-parser
`out of memory` exception, the second under a rising ~3.9 GB RSS workload that
was externally terminated. The runner violates the frozen machine-safety intent
(§17.2 of the amended protocol: *"never load a full tick file or a full minutes
table into memory"*): even the line-streaming version accumulates the **entire
per-market needed-minute tick bucket** in RAM before simulating any event.

A deterministic, bounded-memory, **three-stage pipeline**
(`preflight → freeze economic inputs → one controlled economic execution →
verification → economic adjudication`) must replace the monolithic runner's
dataflow. Staging changes **dataflow only**; it alters no opening range,
breakout, entry, stop, horizon, cost model, gate, OOS split, market universe, or
machine-safety rule. The frozen scientific and economic objects remain
byte-identical and are preserved (§13).

The two prior execution identities are terminal: `…2d5555f0` = **CRASHED /
NOT_ADJUDICABLE** (reconciled), `…cff4a63e` = **RUNNING (stale) / NOT YET
RECONCILED** (process dead, reconciliation mandatory before any new run). They
are never resumed, reused, or treated as evidence.

---

## 2. Failure Forensics

Facts below were recovered from `execution_journal.json`,
`execution_heartbeat.json`, `implementation_manifest.json`,
`process_identity.json`, the crashed directories, and the captured console
traceback. Where something is not provable, it is stated as UNKNOWN.

### 2.1 Execution `EXECUTION_20260820T074818Z_2d5555f0-a436-4ef7-829a-9bdf24f33d5e`

| Field | Evidence |
|---|---|
| PID | 18348 |
| Start (UTC) | 2026-08-20T07:48:18.87 |
| Runner SHA | `b33eee492210a008ff30c544f7490d3823c4517bcacbecdc6dd6e82f2b6b6aca` |
| Last heartbeat | 07:50:11 UTC — RSS **1,130,074,112 B (1.05 GiB)** |
| Last phase | XAUUSD `stream_buckets` (pandas chunked `read_csv`, `chunksize=1_000_000`, `low_memory=False`) |
| Market at failure | **XAUUSD** (12.58 GB tick file) |
| Python caught | **YES** — traceback printed: `pandas.errors.ParserError: Error tokenizing data. C error: out of memory` in `pandas._libs.parsers.TextReader._tokenize_rows` |
| OS killed | No (process exited via uncaught exception path) |
| Recorder state | `RUNNING` at death; reconciled to **CRASHED** `07:52:30` via `reconcile_execution.py` (reason `EXTERNAL_PROCESS_DEATH_RECONCILED`) |
| Artifacts | infrastructure 5 only; no ledgers/stats/report |
| Classification | **APPLICATION FAILURE / RESOURCE EXHAUSTION** — pandas C parser could not obtain a large contiguous allocation while tokenizing the 12.58 GB file, on a 16 GiB host with ~6 GiB free |

Root cause note: `low_memory=False` instructs the C engine to bypass the
on-the-fly chunk heuristic; combined with a 12.58 GB single file this drove the
tokenizer allocation past what the OS would grant → C-level OOM surfaced as a
Python `ParserError`.

### 2.2 Execution `EXECUTION_20260820T082217Z_cff4a63e-f6ea-450d-a102-87a40fba5a09`

| Field | Evidence |
|---|---|
| PID | 14792 |
| Start (UTC) | 2026-08-20T08:22:17.29 |
| Runner SHA | `b2cdfdd833eb9f7d3186a95c26f06c5218dbfabd1626a303e1e9cafe60565220` (line-streaming variant) |
| Last heartbeat | 08:24:48 UTC — RSS **3,903,938,560 B (3.64 GiB)** and climbing |
| Last phase | XAUUSD line-by-line tick streaming into in-memory per-minute `bucket` |
| Market at failure | **XAUUSD** |
| Python caught | No (no traceback; console log empty) |
| OS / IDE / tool | **UNKNOWN which killer** — the run was externally interrupted during the streaming phase; process observed **DEAD** afterwards |
| Recorder state | **`RUNNING` (stale)** — **NOT YET RECONCILED**; reconciliation is mandatory before any subsequent execution |
| Artifacts | infrastructure 4 (no heartbeat-final manifest); no ledgers/stats |
| Classification | **RESOURCE EXHAUSTION PRESSURE + EXTERNAL TERMINATION** — RSS 3.64 GiB at +2.5 min with the per-market bucket still growing toward XAUUSD peak; terminated outside the Python lifecycle |

Root cause note: the line-streaming fix removed the pandas OOM, but the per-event
needed-minute set for all 8,335 events is materialized as in-memory lists of
every bid/ask/time inside the trigger, entry, exit, and MFE/MAE path minutes.
For XAUUSD alone (2,256 events × ~126 needed minutes/event) this accumulates to
multiple GiB before simulation begins. It is exactly the "full minutes table in
memory" that §17.2 prohibits.

### 2.3 Non-crash pre-flight defect (not an execution)

The first ever invocation failed `preflight` with
`Protocol SHA mismatch. Expected: 8F45…, Actual: 8f45…`. This was a
case-sensitivity mismatch between the recorder's byte-exact SHA comparison and
the constant's upper-case form. It occurred in `PRE_FLIGHT`, before `start()`,
so no execution identity/directory was created. Resolved by lower-casing the
constant before the controlled runs. Recorded for completeness only; it is not a
failed execution.

---

## 3. Resource Analysis

Measured on-host facts (all values read-only):

| Asset | File size | Est. rows* | In-memory danger |
|---|---|---|---|
| XAUUSD tick | 12.58 GB | ~282 M | whole-file load impossible; full per-minute bucket ~GiB-scale |
| BTCUSD tick | 12.46 GB | ~260 M | same |
| USATECHIDXUSD tick | 8.20 GB | ~171 M | same |
| XAGUSD tick | 5.69 GB | ~119 M | same |
| EURUSD tick | 0.10 GB | ~2.1 M | not in MARKETS |
| M1 (all markets) | 54–134 MB each | — | safe per-market load (precedent: scientific run) |
| Event table | 8,335 rows | — | safe |

*Est. rows = size ÷ 48.0 bytes/line (sampled mean over 200 random reads).

Host budget (live measurement, post-crash):
- Total RAM: **15.79 GiB**; available at scan: **6.57 GiB**; 8 logical CPUs.
- Free disk: **216.76 GiB** (sufficient for all stage outputs).

### Why the monolithic pipeline cannot be made safe by code tweaks alone

1. **Aggregates-are-the-bucket**: the runner streams fine, but then **retains**
   the complete per-market `bucket` (every needed minute × every tick) plus the
   derived `med` dictionary until the market finishes. This is a "full minutes
   table", expressly prohibited by §17.2, and scales with market size, not with
   event count.
2. **Pandas amplification**: `read_csv` with string dtype + `low_memory=False`
   on a 12.58 GB file creates large transient C tokenizer buffers (proven by the
   ParserError OOM of Exec 2.1).
3. **No stage boundary**: hashing (pre-flight), quote extraction (prep), and
   simulation (evaluation) share one process lifetime; there is no checkpoint at
   which raw ticks can be discarded and replaced by compact, frozen aggregates.
4. **No explicit release discipline**: loop variables (`m1df`, `bucket`, `med`)
   are rebound but never `del`'d; CPython reference-counting eventually frees
   them, but pandas retains internal caches/arenas between iterations, so peak
   working set is not guaranteed monotone-clean (same class of defect the
   scientific `ORD_V1_1_0_MEMORY_REMEDIATION_V1.md` removed for M1 data).

**Consequence:** the monolithic design **cannot safely process the four markets
sequentially** on a 16 GiB host. Stage boundaries that persist compact frozen
inputs to disk are required.

---

## 4. Current Monolithic Architecture

```
hashes (M1+tick)                    # pre-flight, streamed, OK
  → EventStudyRecorder.start()      # identity 1/host, heartbeat every 5 s
  → per market (XAUUSD→BTCUSD):
       load M1 (per market)         # OK, ~100 MB
       build_needed_minutes(all events)   # in-memory set
       stream_buckets(market)       # ⚠ builds FULL per-minute tick bucket in RAM
       compute_medians(bucket)      # ⚠ second resident structure
       simulate every event         # reads bucket + med
       aggregate ledger/stats/year/OOS/bands
  → write 13 artifacts
  → recorder.complete_execution()
```

Safety verdict: **UNSAFE** (two independent empirical failures, §2.1 and §2.2).
The architecture is *conceptually* correct (protocol-conformant economics) but
*memory-scalable* only if the quote materialization and the evaluation are
separated by a frozen, hashed, on-disk intermediate.

---

## 5. Stage 0 Design — Resource / Data Preflight

**Purpose.** Prove each tick file is storable, hashed, parseable, time-consistent,
quote-valid, and streamable within a fixed memory budget — **before any event
input is derived**. Stage 0 computes **no economic results**.

**Repeatability.** Stage 0 is fully repeatable; every run targets a fresh
`PREFLIGHT_<market>` directory; no run depends on a previous run.

**Per market, output (`output/research_discovery/ORD_ECONOMIC/V1.1.0/PREFLIGHT_<market>/`):**

| Check | Deterministic output |
|---|---|
| File existence | present / missing (missing ⇒ abort, no execution) |
| Hash | SHA-256, streamed 1 MiB chunks |
| Schema | headerless `date,time,bid,ask,last,vol`; 6 fields on row 0; no header row |
| Row count | exact count via a single line-buffered pass (no pandas) |
| Timestamp format | `%Y%m%d`,`%H:%M:%S`; zero failures on random sample + full-pass error counter |
| Timezone | documented convention: naive UTC (matches M1 `timestamp` = UTC bars); inconsistency counter |
| Bid/ask validity | counters for non-finite / ≤0 / bid>ask rows via the same single pass |
| Memory-safe streaming probe | stream a fixed slice (e.g., 10 M rows) measuring peak RSS; assert << budget |
| Expected output size | estimated compact Stage-1 intermediate size (rows × ~40 B) vs free disk |

Stage 0 artifacts: `preflight.json` (all checks + counters + hashes + peak RSS),
`stage0_manifest.json`, `execution_journal.json` (state `COMPLETED` via a
lightweight stage recorder, or `CRASHED` via reconciliation). A single combined
`PREFLIGHT_ALL_MARKETS.json` may be emitted for convenience but never replaces
the per-market records.

**Stage-identity/crash rule:** unique identity + isolated dir + heartbeat +
process identity + fail-closed finalization + crash reconciliation, identical to
the recorder pattern. A crashed Stage 0 makes no claim of any kind; it can simply
be re-run.

---

## 6. Stage 1 Design — Economic Input Preparation (frozen)

**Purpose.** Convert, **one market at a time**, the raw tick file into a
compact, immutable, hashable intermediate containing **only** the deterministic
information the economic simulation requires. Stage 1 performs **no** PnL, no
viability, no profit factor, no economic classification, no optimization metric.

**Memory model — bounded by construction:**
- A single line-buffered pass over the tick file.
- Per-minute transient buffer: ticks of the **current minute only** are held;
  on minute-rollover the minute is reduced to its aggregates and **discarded**.
- No per-market `bucket`/`med` tables are ever resident. Peak RSS is O(ticks in
  one minute) ≈ KB–MB, independent of file size and event count.
- The per-event needed-minute set is precomputed from the **event table + M1**
  (no tick data), then served as a lookup during the single pass.

**Stage 1 output (frozen per market), `PREP_<market>_<stage1hash>/`:**

`prep_manifest.json` (reproducibility, §12):
- source M1 SHA-256; source tick SHA-256; scientific event-table SHA-256;
  economic protocol SHA-256; preparation implementation SHA-256;
- generation timestamp (UTC); market; string schema version (`stage1.v1`);
  stage-1 intermediate SHA-256; row counts; peak RSS.

`minute_quotes.parquet` (or `.csv.gz`): per needed minute
`minute_key (UTC), bid_median, ask_median, nticks` — the only per-minute values
the simulation will ever read.

`event_inputs.csv` — per event, exactly the fields §6 of the mission mandates:
- event ID (market + trading_day + direction + anchor_ts);
- market; trading day; direction;
- breakout timestamp; scientific entry close (from the persisted event table);
- `T_B` (= anchor + 60 s);
- structural OR levels `High_OR`/`Low_OR` **and** the `range_width` cross-check
  result (tolerance `max(1e-4, 1e-6·|range_width|)`) → passes / `EXCLUDED_RANGE_*`;
- eligible entry quote-minute selection result (exact / fallback+1..5 /
  market-median / no coverage);
- executable entry quote (median ASK for LONG, median BID for SHORT) + entry
  spread (bp);
- horizon timestamp (T_B+120) + horizon-completeness flag (M1 bar at
  anchor+120 exists);
- structural-stop trigger metadata: trigger bar index/minute (from M1 closes)
  and, when the trigger minute is encountered during the single pass, the
  **first trigger-side executable tick** (bid≤High_OR for LONG / ask≥Low_OR for
  SHORT at/after trigger-bar start; gap-through fills use the actual quote);
- exit-lookup metadata (needed-minute keys for exit exact ±5 and MFE/MAE path).

Every value is deterministic given the frozen source files and the stage-1
program. The intermediate is immutable (written once, no in-place edits, final
SHA persisted in `prep_manifest.json`).

**Stage-identity/crash rule:** fresh unique identity + isolated dir + heartbeat
+ process identity + manifest + fail-closed finalization + reconciliation.
A **complete and hash-verified** Stage-1 directory is a *restartable artifact*
(§10): it may be reused verbatim by Stage 2. A partial/crashed Stage-1 directory
is simply re-run and never mistaken for preparation evidence.

---

## 7. Stage 2 Design — Economic Evaluation (the one controlled execution)

**Purpose.** The **actual ORD V1.1.0 baseline economic execution**, registered
beforehand, running **exactly once**, consuming **only**:
1. the frozen Stage-1 `prep_manifest.json` + `minute_quotes` + `event_inputs`
   for each market, and
2. the deterministic M1 data (already SHA-fingerprinted) required for the
   remaining exit / MFE / MAE lookups and the OR cross-check.

**Stage 2 computes** — strictly from those frozen inputs — and **nothing else**:
- trade ledger (entry/exit resolution, structural-invalidation vs horizon exits,
  gap-through fills, exclusions retained);
- gross return per trade; observed entry+exit spread; Model A cost
  `RT(A)=(s_entry+s_exit)/2`, `Net_A=Gross−RT(A)`;
- Model B descriptive `Net_B=Gross−(s_entry+s_exit)` + additive
  commission `{0,2,5,10}` bp × slippage `{0,2,5}` bp sensitivity bands;
- MFE / MAE (from the per-minute quote path T_B..hit_minute);
- cumulative net (chronological Model-A sum), PF (with `+∞`/`0`/`NaN` boundary
  semantics), max drawdown;
- development/OOS (chronological first `⌊N/2⌋` event days = DEV, rest = OOS);
- per-year results; year-concentration `max|yearly|/|cumulative|`;
- the five registered viability gates and final classifications
  (ECONOMICALLY PROMISING / ECONOMICALLY NON-VIABLE / INSUFFICIENT DATA;
  BTCUSD NO-SCIENTIFIC-VERDICT caveat; EURUSD NOT SIMULATED).

**Memory model:** no raw tick file is read in Stage 2 at all — the compact
`minute_quotes`/`event_inputs` (KBs–MBs) and per-market M1 (~100 MB) are loaded
per market; markets remain fully independent and are processed sequentially with
explicit `del`/`gc` boundaries between markets. Peak Stage-2 RSS is bounded and
far below the host budget.

**Exactly-once (§9):** Stage 2 is a full `EventStudyRecorder` execution —
unique execution identity `EXECUTION_<timestamp>_<UUID>`, isolated directory,
5 s heartbeat with PID/RSS, process identity, mutation guard, fail-closed
artifact gate, and the **same 13 required artifacts** registered in
`run_ord_econ_v1.py` (ledgers per market, statistics, market/yearly/dev-OOS
summaries, cost outputs, metadata, peak resource, report). It records the
Stage-1 hashes. **A failed or interrupted Stage 2 is CRASHED / NOT_ADJUDICABLE,
never resumed from partial calculations; a new Stage-2 identity is created only
after governance authorizes another controlled attempt.**

---

## 8. Stage 3 Design — Final Verification

**Purpose.** Read-only, post-execution verification. No scientific or economic
redefinition.

Checks, output `output/research_discovery/ORD_ECONOMIC/V1.1.0/VERIFICATION_<execution-id>/`:
- every source hash (M1, tick) matches the persisted scientific manifest and the
  Stage-1 hashes;
- every Stage-1 hash matches `prep_manifest.json`;
- trade count = expected traded + excluded rows = event count per market;
- ledger integrity (no partial rows; columns present; EXCLUDE rows preserved);
- formula consistency (Model-A identity `Net=Gross−RT(A)` reproduced from
  ledger fields; cumulative = chronological sum; PF boundary semantics);
- OOS split (first `⌊N/2⌋` event days) reproduced;
- year concentration reproduced;
- viability gates reproduced from ledger;
- artifact completeness vs the Stage-2 required list; journal state COMPLETED;
- reconciliation status of any crashed identities (must be CRASHED, not running).

Stage 3 creates **no** economic evidence — it only certifies what Stage 2
produced and that the frozen inputs were byte-exact. Outputs:
`verification_report.json`, `verification_summary.md`, stage journal.

---

## 9. Exactly-Once Semantics

Mapping to the mission's §7 rule:

| Stage | Role | Repeatable? | Economic evidence? | Resume rules |
|---|---|---|---|---|
| Stage 0 Preflight | health/schema/hash check | **Yes**, freely | No | restartable |
| Stage 1 Preparation | freeze quote inputs to disk | Yes (idempotent) | No | restartable; **reusable if complete+hash-verified** |
| Stage 2 Evaluation | **the** controlled economic execution | **One controlled attempt** | **Yes** | **never resumed**; new identity only after governance |
| Stage 3 Verification | read-only certification | Yes | No (certifies only) | restartable |

Staging is an **execution-engineering mechanism**, not multiple strategy trials.
The final economic experiment remains **ONE CONTROLLED BASELINE ECONOMIC
EXECUTION**. A failed Stage 2 must not be resumed from an incomplete economic
result; a new Stage-2 identity is required only after governance authorizes
another controlled attempt.

---

## 10. Crash Reconciliation

- **Every stage** carries identity + isolated dir + heartbeat + process identity
  + artifact manifest + fail-closed finalization, and is reconciled through
  `scripts/reconcile_execution.py` semantics (process-death detection via
  PID + create-time + boot-time; terminal CRASHED state; preserved partial
  artifacts with hashes; `scientific_validity=false`,
  `scientific_adjudication=NOT_ADJUDICABLE`).
- A **crashed Stage 1** is never mistaken for completed economic evidence.
- A **crashed Stage 2** is NON-ADJUDICABLE.
- **Immediate mandatory action:** reconcile the stale
  `EXECUTION_20260820T082217Z_cff4a63e…` directory (process 14792 confirmed
  DEAD) to CRASHED **before** any subsequent execution, so that no `RUNNING`
  journal stands un-reconciled next to a future identity. `…2d5555f0` is already
  CRASHED.

---

## 11. Memory Safety

Evaluated against the mission's §11 criteria (no arbitrary chunk sizes
prescribed unless evidence-supported):

- **Streaming:** Stage 0, 1 hold one file line at a time (evidence: streamed
  hashing and the line-streaming fix already removed the pandas OOM).
- **Chunking:** the non-prescriptive alternative to line streaming is a fixed
  byte-chunk scan with row-boundary restoration; **not required** when
  line-buffered iteration over a single minute keeps O(1 minute) resident.
- **Bounded in-memory state:** Stage 1 discards every minute after reduction
  (proven bound: peak RSS ≈ largest single minute, not full file/table). Stage 2
  reads only compact frozen aggregates. Nominal Stage-1/2 peak budget:
  **≤ 4 GiB ceiling**; observed Exec-2 working set of 3.64 GiB was the
  unbounded monolithic bucket — eliminated by design.
- **Per-market isolation:** stages iterate XAUUSD→XAGUSD→USATECHIDXUSD→BTCUSD
  sequentially; Stage 2 adds explicit `del m1df; gc.collect()` between markets.
- **Explicit object release:** stated in Stage-1 pass and Stage-2 per-market
  boundary (§6, §7).
- **Resource monitoring:** psutil sampling at fixed intervals recorded to each
  stage's heartbeat + `peak_resource.json`-style output.

No chunk size is prescribed here because the bound comes from the data model
(one-minute reduction), not from tuning.

---

## 12. Reproducibility

**Stage-1 inputs** persist, per market: source M1 hash; source tick hash;
scientific event-table hash; economic protocol hash; preparation implementation
hash; generation timestamp; market; schema version. **Stage-2 execution**
persists: Stage-1 hashes; economic protocol hash; runner hash; execution ID;
cost-model identity (Model A / Model B descriptive). **Stage-0** persists all
source hashes. Every fingerprint is a SHA-256 over full bytes; every directory
is content-addressed by its own stamp; history is never overwritten.

---

## 13. Scientific Object Preservation

Staging alters **dataflow only**. It does NOT change:
- opening-range windows (London 03:00–03:29 ET for XAU/XAG/BTC, US
  09:30–09:59 ET for USATECH);
- breakout definition (close-based); entry concept (median quote at/after T_B);
- structural invalidation (close-triggered, first trigger-side executable tick at
  or after trigger bar start, gap-through at actual quote, capped at horizon);
- 120-minute horizon; cost model(s); viability gates (all five); OOS split
  (first ⌊N/2⌋ event days); market universe (XAUUSD, XAGUSD, USATECHIDXUSD,
  BTCUSD; EURUSD NOT SIMULATED);
- M1/tick/event objects — every source file remains untouched and is hashed at
  each stage.

The Stage-2 report's scientific boundary text (§15) is retained verbatim: the
economic execution performs no adjudication and states no verdict on whether any
strategy works, fails, or is profitable.

---

## 14. Protocol Amendment Requirement

**Determination: an amendment is warranted, but it is narrow and deterministic —
and it is NOT performed here.**

The amended protocol already mandates streaming and bounded-memory aggregates
(§17.2) and exactly-once identity (its §17 quotation of F9). Staging is therefore
*consistent with* the protocol's intent and changes **no economic/scientific
semantic**. Two protocol surfaces, however, are not yet "precisely registrable"
for a staged dataflow:

1. **§16 / §17 distinction between preparation and execution.** The protocol's
   required-artifact list (§16) and its "ONE controlled economic execution"
   wording (§17, §19) must be clarified so that:
   - PRELIGHT/PREP directories are **infrastructure artifacts**, not executions;
   - only the Stage-2 directory is THE economic execution identity;
   - Stage-1 frozen inputs are registered inputs to Stage 2 (and therefore the
     Stage-2 `input_manifest_hash` includes the Stage-1 hashes);
   - a reused, hash-verified Stage-1 artifact is explicitly a *restartable
     preparation unit*, not a partial economic result.
2. **Machine-safety section wording alignment.** §17.2 says "never load a full
   tick file or a full minutes table into memory"; the amendment should make
   explicit that the *aggregate* (per-minute medians) intermediate is the only
   resident tick-derived state and that raw per-minute tick lists must never be
   accumulated market-wide (which is precisely the defect staged execution
   removes).

**Exact amendment scope (if approved by governance):** a section inserted into
`ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md` (designated e.g. §17A, "Staged
Execution Dataflow") defining the four stage identities/directories, the
restartable-preparation rule, the Stage-2-is-the-execution rule, the Stage-1
hash registration in Stage-2's input manifest, and the memory-residency bound.
No economic rule, threshold, gate, split, cost model, market, or scientific
object changes. Consistent with §20's "precision-only amendment" boundary and
the V1.1.0 amendment/amendment-report/audit governance chain.

Per instruction, **this document does not amend the protocol**. The amendment
(if any) requires a separate frozen-amendment + amendment-report + independent
audit cycle.

---

## 15. Governance Decision

**Requirement decision (mission §15):**

> **B — STAGED EXECUTION REQUIRED.**

Rationale: two independent empirical resource failures of the monolithic pipeline
(§2.1 pandas C-parser OOM during XAUUSD tokenization on a 16 GiB host; §2.2
~3.9 GiB rising RSS during XAUUSD bucket materialization, externally terminated),
plus an architectural proof that the monolithic `bucket`/`med` residency is a
"full minutes table" that scales with market size (§3, §4). Forensic evidence is
sufficient; further evidence is not required.

**Governance ordering for resuming the frozen economic experiment:**
1. Reconcile stale `…cff4a63e` → CRASHED (mandatory, already-supported utility).
2. Freeze the staged-dataflow amendment (§14) + amendment report + independent
   read-only audit (mirrors the V1.1.0 governance chain).
3. Run Stage 0 (repeatable) for the four markets.
4. Run Stage 1 (repeatable, frozen inputs) per market; verify hashes.
5. Run the **one controlled Stage-2 economic execution** with its own
   EventStudyRecorder identity.
6. Run Stage 3 verification.
7. **INDEPENDENT ECONOMIC RESULTS ADJUDICATION** — which was and remains the
   exact next governance task registered in §19/§16 of the protocol.

No alternative translation, no tuning, no rescue of failed identities, no EA,
no commit, no push.

---

## 16. Exact Next Task

> **FREEZE THE STAGED-EXECUTION AMENDMENT (protocol §17A-equivalent) + AMENDMENT
> REPORT + INDEPENDENT READ-ONLY AUDIT**, and reconcile the stale
> `…cff4a63e` execution to CRASHED — then, and only after those governance gates
> pass, execute Stage 0 → Stage 1 → the single controlled Stage-2 economic
> execution → Stage 3 → **INDEPENDENT ECONOMIC RESULTS ADJUDICATION**.

---

## 17. Integrity

- Strictly READ-ONLY with respect to all scientific and economic objects:
  ORD scientific protocol, definition lock, event study artifacts, event table,
  M1 files, tick files, economic protocol, and all executed/legacy execution
  directories are untouched by this task.
- No economic simulation, PnL, trade statistics, viability, optimization,
  or outcome inspection was performed.
- The only new repository artifact is this design document.
- No code was written, modified, or executed against the frozen objects during
  this design task (the earlier memory-diagnostic probes in this session were
  read-only file reads/measurements; no simulation was run).

---

*End of document — ORD ECONOMIC EXECUTION STAGING DESIGN V1.*