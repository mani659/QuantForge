# ORD Economic Staged Execution — Implementation Manifest (V1)

Scope: implementation ONLY of the approved V2.0.1 staged-execution
infrastructure (Stages 0–3).  No production run, no economic dataset was
processed, no PnL/economics computed on real data, no rule or protocol change,
no commit/push (this work is committed/Judged only when the user explicitly
asks).  All frozen protocol texts are byte-identical to their recorded SHA-256
(verified at the end of the milestone).

## 1. Protocol inputs (unchanged, verified byte-exact)

| Document | SHA-256 (verified) |
|---|---|
| ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_1_AMENDED.md | `1d3ee7a6a9fd747cb57a716b43c5eb80bb7d6016011d2c4df9f0814cc196968d` |
| ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md | `8f45d7f82c80b7131c958c158f448520fef6927d49f9eb844fbbd55e35395663` |
| ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md | `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06` |
| ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md | `b58105404d277560eec31a8b08c5b1997b86a03904fc4a804e87beaac448ab30` |
| ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1.md | prefix `50a08aaf…` |
| ORD_ECONOMIC_TRANSLATION_PROTOCOL_V2_AMENDED.md | prefix `85d4e1d1…` |

Pre-existing (unchanged, reused): `research/orchestration/event_study_recorder.py`,
`scripts/reconcile_execution.py`, and all aggregation helpers in
`scripts/run_ord_econ_v1.py` (LEDGER_COLUMNS, simulate_event, MarketMetrics,
profit_factor, split_dev_oos, year_concentration, classify, PeakSampler,
commission/slippage bands).  No helper was re-implemented in the staged package.

## 2. New implementation surface (all test-backed)

### Package `research/staged_execution/` (new)
- `__init__.py` — staged-pipeline entry points.
- `_identity.py` — canonical W4 identity: nine-field byte-stable manifest
  (`market`, `schema.version.stage1`, `protocol.economic.sha256`,
  `protocol.scientific.sha256`, `source.m1.sha256`, `source.tick.sha256`,
  `implementation.preparation.sha256`, `parameters.stage1.manifest`,
  `code.schema.prep`); `prep_identity() -> PREP_<market>_<64 upper hex>`;
  `preparation_implementation_sha256()` (field-7 source set incl.
  `scripts/ord_econ_stage1_prepare.py`); fixed-width `<QddI` 28-byte minute
  index with chunked exact external median/percentile (bounded RAM, matches
  numpy semantics), plus `sha256_file`/`sha256_bytes`.
- `_failure.py` — W3 failure classification: 9 registered
  `INFRASTRUCTURE_FAILURE_CATEGORIES`, 4 registered `ECONOMIC_EXCLUSION_CODES`
  (disjoint), `ExecutionInfrastructureFailure`, guard
  `assert_no_infrastructure_in_economic_channel`.
- `_stage_recorder.py` — StageRunRecorder (STAGE0/1/3, is_complete lifecycle,
  INVALIDATED on component-failure/mutation, YAML+JSON journals), reconcilable
  by the approved `scripts/reconcile_execution.py`.
- `stage0.py` — `run_stage0_preflight`: streamed hash, headerless 6-field
  schema, timestamp format, quote validity, malformed/out-of-order stats,
  RAM/disk/RSS probe, fresh `PREFLIGHT_<market>_<runid>` identity per run;
  FALSE verdicts are findings (never raises); component failure raises
  `ExecutionInfrastructureFailure`.  No economic result is ever persisted.
- `stage1.py` — `run_stage1_prepare`: frozen `PREP_<market>_<hash>` per market;
  single bounded streaming pass over ticks (MinuteAggregates flushed at
  rollover/EOF), M1-derived OR skeleton + range checks + horizon completeness +
  structural-stop watches (V1.1.0 §5 fill semantics: trigger-side first
  qualifying tick at/after trigger-bar start, gap-through at actual quote,
  capped at horizon), exact->fallback->market-median quote resolution,
  artifacts `{prep_manifest, minute_quotes.csv.gz, event_inputs.csv,
  event_paths.csv, minute_index.bin, execution_journal.json}`; reuse gate
  (`is_valid_prep`: journal COMPLETED + identity byte-exact + artifact hashes);
  mutation/failure → `PREPARATION_INTEGRITY_FAILURE` until `force_rebuild`
  archives `…_RECONCILED_…` (never overwrites); no economic field in manifest.
- `stage2.py` — `run_stage2_execute`: EXACTLY-ONCE non-resumable; re-derives
  and byte-verifies every prep from CURRENT source M1/tick hashes before any
  calculation (missing sources fail closed `PREPARATION_INTEGRITY_FAILURE`);
  uses the EventStudyRecorder under output `ORD_ECONOMIC/V1.1.0/EXECUTION_…`;
  ledger per V1.1.0 `LEDGER_COLUMNS` (32), statistics/yearly/dev-OOS/cost/
  metadata; market-adaptive artifact contract
  (`expected_artifacts_for(markets)` = base + `trade_ledger_<m>.csv`);
  helpers imported from `scripts.run_ord_econ_v1` only; crash → CRASHED /
  NOT_ADJUDICABLE via approved reconciler.
- `stage3.py` — `run_stage3_verify` (READ-ONLY, V2.0.1 §7): source hashes vs
  execution metadata + scientific manifest; prep identity reproduced valid +
  matches execution; ledger columns faithful; excluded rows preserved; trade
  count == event rows; gross/net reproduced from the FROZEN event inputs
  (Model-A `cost=(s_entry+s_exit)/2`, long/short formulas); PF boundary
  semantics incl. +inf/0/NaN; year concentration; dev/OOS split
  (first floor(N/2) event days); five viability gates; artifact completeness;
  no un-reconciled RUNNING staged identities (its own live `VERIFICATION_` is
  excluded); output `VERIFICATION_<execution-id>/`, restartable with
  `force_rerun` (prior dir archived `…_RECONCILED_…`); verdict only PASS/FAIL.

### CLI scripts (new)
- `scripts/ord_econ_stage0_preflight.py`
- `scripts/ord_econ_stage1_prepare.py` (registered in field-7 hash set)
- `scripts/ord_econ_stage2_execute.py` (exit 1 on infra failure)
- `scripts/ord_econ_stage3_verify.py` (exit 1 on FAIL)

## 3. Test suite (new, all passing)

`python -m pytest tests\test_ord_staged_{identity,failure,stage0,stage1,stage2,stage3,recorder}.py`
→ **75 passed** (15 s).  Synthetic deterministic XAUUSD fixture
(`tests/synth_ord_fixtures.py`): 4 trading days, 5 events
(1 HORIZON, 1 STRUCTURAL_INVALIDATION, 3 exclusions), 123 observed minutes,
market medians 120.0/120.1.  Existing related suites stay green: 29 passed
(`test_crash_reconciliation`, `test_execution_infrastructure`,
`test_artifact_contract_correction`).  `compileall` clean.

Coverage highlights: manifest byte-stability + BOM rejection; external
median/percentile vs numpy incl. 200k values; minute-index corruption; failure
classification incl. channel guard; stage0 PASS/FAIL/component-failure;
stage1 immutability/reuse/mutation-invalidates/force-archive/bounded-memory
evidence (max minute ticks resident ≤ 1; 123 minutes flushed); stage2
exactly-once, artifact contract, fail-closed on prep mutation and missing
sources, dev-OOS split; stage3 pristine PASS, tampered-ledger FAIL, missing
artifact/market-ledger/non-COMPLETED journal FAIL, read-only proof (ledger
hash unchanged across re-verification), non-restartable without force;
recorder infra-artifacts, mutation guard, reconciler CRASHED + STALE.

## 4. Post-implementation integrity + hard stop

Re-verified immediately before closing this milestone: all six protocol files
and the two pre-existing crashed execution dirs
(`EXECUTION_20260820T074818Z_2d5555f0-…` and
`EXECUTION_20260820T082217Z_cff4a63e-…`, both `CRASHED /
EXTERNAL_PROCESS_DEATH_RECONCILED`) are byte-identical / journal-state
unchanged.  No production Stage 0/1/2 run, no commit/push — HARD STOP.