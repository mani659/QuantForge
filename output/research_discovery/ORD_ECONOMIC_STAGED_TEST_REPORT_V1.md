# ORD Economic Staged Execution — Test Report (V1)

Final consolidated run (this report's figures):
`python -m pytest tests\test_ord_staged_*.py tests\test_crash_reconciliation.py tests\test_execution_infrastructure.py tests\test_artifact_contract_correction.py -q`
→ **104 passed, 0 failed** in 21.1 s.  `python -m compileall` clean on the
staged package + the four CLI scripts.

## New staged-execution suite — 75 tests

| File | Tests | Focus |
|---|---|---|
| test_ord_staged_identity.py | 21 | canonical 9-field manifest byte-stability, field order, lowercase/uppercase hex rules, BOM rejection, `STAGE1_PARAMETER_KEYS`/parameter manifest, external median/percentile vs numpy (incl. 200k values), even-average semantics, repeated values, empty raises, minute-index write/lookup/median/corruption, record size `<QddI`=28, sha vectors, field-7 impl-hash determinism + missing-file |
| test_ord_staged_failure.py | 13 | exact label, 9 registered categories, 4 economic codes, class disjointness, classify mapping (OOM/disk/parser/hash/default), roundtrip, unregistered reject, channel guard reject+accept |
| test_ord_staged_stage0.py | 7 | pristine PASS, repeatable fresh identity, missing files → FAIL verdict, bad schema/bad quote/expected-hash mismatch → FAIL, component failure → infra raise |
| test_ord_staged_stage1.py | 13 | immutable prep artifacts, manifest facts (medians, minutes, events, 1 stop fill, NO economic fields), exit-reason counts 1/1/1/1/1, horizon fields (entry exact 07:31, exit minute 12855451), stop fields (level 202.0, fill bid 200.5/ask 200.6 @07:32), reuse when matching, mutation invalidates + blocks until force, force archives `…_RECONCILED_…` (never overwrites) + journal CRASHED, bounded-memory evidence (max_minute_ticks_resident ≤ 1, minutes_flushed 123, tick_rows_streamed 123), gzip stream row0 `12855331,`, deterministic rebuild identity, exact `EVENT_INPUT_COLUMNS`, missing source → infra |
| test_ord_staged_stage2.py | 8 | exactly-once fresh identity, base+per-market artifact contract, ledger math (`(120.0-120.1)/120.1*1e4`, `(200.5-203.1)/203.1*1e4`), holding durations 120/1, prep mutation fail-closed (no new execution dir), missing source fail-closed, helper identity (`market_metrics is v1.market_metrics`), statistics excluded counts, dev-OOS split (4 event days, dev 2/2, oos 0) |
| test_ord_staged_stage3.py | 6 | pristine chain → PASS + `VERIFICATION_<exec-id>/` layout + journal COMPLETED + read-only proof (ledger hash unchanged), non-restartable without force, tampered ledger → FAIL (net_reproduced), missing artifact → FAIL, missing market ledger → FAIL, non-COMPLETED journal → FAIL |
| test_ord_staged_recorder.py | 7 | five infra artifacts written, execution_id == dir name, existing-dir rejection, mutation guard → INVALIDATED, reconciler reconciles a stale/CRASHED dir (`STALE:` + `SUCCESS:`), terminal-state pass-through, interrupt → INTERRUPTED |

## Regression coverage — 29 tests (unchanged suites, all green)

- `test_crash_reconciliation.py` — approved reconciler behavior unchanged.
- `test_execution_infrastructure.py` — EventStudyRecorder artifact/journal
  contract (pre-existing, reused by Stage 2).
- `test_artifact_contract_correction.py` — artifact-completeness correction
  contract (pre-existing).

## Fixture integrity

`tests/synth_ord_fixtures.py` is deterministic, test-only, and writes only to
`pytest` tmp dirs.  It generates frozen-format M1 / headerless tick /
event-table inputs for XAUUSD (London OR): 4 trading days, 5 events
(1 HORIZON, 1 STRUCTURAL_INVALIDATION, EXCLUDED_RANGE_MISMATCH,
EXCLUDED_RANGE_RECONSTRUCTION, EXCLUDED_HORIZON_INCOMPLETE), 123 observed
minutes, market medians 120.0/120.1.  No real economic data touched.

## Notes on bugs found and fixed during test execution

1. External quantile quickselect overwrote the file it was reading (recursion
   shared partition file names) → per-call work dirs; matches numpy exactly.
2. `flush_minute` closure lacked `nonlocal cur_key` → UnboundLocalError.
3. Horizon-completeness key aligned to the actual exit minute `hz` (09:31),
   not `anchor+120min`; M1 fixture extended to a 09:31 bar.
4. Prep manifest keys reconciled with `PrepIdentity.fields()` keys
   (`implementation_sha256`, `parameter_manifest`).
5. Stage 1 wraps unreadable sources into `ExecutionInfrastructureFailure`.
6. Stage 2 normalizes the V2.0.1 protocol SHA to lower-case for the recorder's
   case-sensitive comparison.
7. Stage 3 reproduces gross/net from the frozen `event_inputs.csv` (the V1.1.0
   ledger intentionally does not persist `exit_bid`/`exit_ask`), and its global
   RUNNING-scan excludes its own live `VERIFICATION_` identity.

No production execution was performed; no economic result was computed on any
real dataset.  HARD STOP after this report.