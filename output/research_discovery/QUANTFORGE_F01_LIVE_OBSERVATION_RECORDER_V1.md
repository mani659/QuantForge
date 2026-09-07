# QUANTFORGE — F-01 LIVE OBSERVATION RECORDER (V1)

**Milestone:** F-01 Live Market-Observation Recorder — integration with the existing Unified Runner / MT5 paper-trading infrastructure.
**Date:** 2026-09-03
**Status:** INFRASTRUCTURE REPORT

---

## 1. Executive Infrastructure Verdict

**F-01 LIVE OBSERVATION RECORDER OPERATIONAL — NO CURRENT OBSERVATIONS.**

The recorder is implemented, attached to the Unified Runner's shared MT5 feed, exception-safe, and verified end-to-end — including a genuine live capture from the running Exness terminal and a governed handoff whose boundary decision (reject pre-freeze) was applied correctly by the accrual pipeline.

The honest caveat behind "NO CURRENT OBSERVATIONS": the terminal's **USTECm M1 bar series has not advanced since 2026-08-27T12:55Z** (the live tick stream is fresh, but `copy_rates_from_pos(M1)` returns no newer closed bar). The infrastructure therefore cannot yet accrue post-freeze M1 evidence — not an infrastructure failure, a terminal data-availability dependency, documented in §19.

**Stage 3 readiness is NOT claimed. No Stage 3, no economics, no Base status. Base Registry remains EMPTY.**

---

## 2. Governance State

Verified before implementation:

| Item | State |
|---|---|
| V38 / V38A / BS1–BS13 / BF1–BF13 | RATIFIED |
| F-01 | SELECTED BASE HYPOTHESIS, REGISTERED / FROZEN |
| Stage 2 | STRUCTURALLY VALID |
| Forward-data accrual pipeline | OPERATIONAL (v1.0.0) |
| Stage 3 | DATA ACCRUAL PENDING |
| Base Registry | EMPTY — no Base exists |

Repository baseline: HEAD `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5`, branch `main`; pre-existing dirty/untracked files untouched.

---

## 3. Existing Unified Runner Architecture

- **Launcher:** `run_quantforge_forward.bat` → `python -u scripts/forward/quantforge_forward_supervisor.py --mode forward` (foreground, env `QF_MT5_TERMINAL_PATH` set; `status_quantforge_forward.bat` / `stop_quantforge_forward.bat` companion scripts).
- **Supervisor:** `scripts/forward/quantforge_forward_supervisor.py` — singleton lock (`msvcrt`, stale-lock recovery), MT5 startup gate (server must equal `Exness-MT5Trial15`, `USTECm` select + quote check), 1-second loop: `latest_quote("USTECm")` → distribute quote to modules → 60s heartbeat (`supervisor_health.jsonl`) → 10s live status.
- **Module lifecycle:** modules are **in-process wrappers** registered by `scripts/forward/module_registry.py` — CAND-015 (protected adapter), CAND-024, CAND-035 (`ForwardModuleWrapper`). Restart = re-run the BAT (stale lock/session recovery handled).
- **Logging/supervision:** status.json, supervisor.lock, shutdown.req, health ledger under `runtime/forward/supervisor/` (protected data area — not read or modified by this work).

## 4. Existing MT5 Data Interface

- `scripts/forward/market_data.py` — `MT5MarketFeed`: `initialize()` (env-config terminal path), `connection_state()`, `terminal_info()`, `latest_quote(symbol)` (tick via `symbol_info_tick`), `latest_completed_bar(symbol, timeframe)` (M1–H1 via `copy_rates_from_pos(…, 1, 1)`), `shutdown()`.
- `broker/mt5_connection.py` — credential-free env-configured connection verifier (not a bar source).
- Live verification this session: `initialize: True`, `connection: CONNECTED`, broker `Exness Technologies Ltd`, server `Exness-MT5Trial15`, MetaTrader5 package 5.0.5735.

## 5. Existing Three-Module Integration Boundary

The three trading modules were **not modified**. The recorder is a fourth, additive component of the supervisor loop, invoked *after* module quote distribution:

```text
for module in self.modules: module.process_quote(...)   # unchanged
self.f01_recorder.on_tick(quote_res)                    # added
```

The recorder shares the supervisor's single `MT5MarketFeed` instance (one connection, no second broker system) and holds no mutable strategy state. Its `on_tick` is exception-safe by contract (tested T13), so a recorder fault cannot alter module behavior or crash the loop.

## 6. Recorder Architecture

**Implementation:** `scripts/forward/f01_observation_recorder.py` (v1.0.0, new file).

- Attaches to the supervisor feed; polls the latest **completed** M1 bar once per loop tick.
- Persists to an isolated raw recorder archive — never into the study archive.
- Handoff to the governed accrual pipeline through its existing interface (`--handoff`); the pipeline remains the sole authority for admission, boundary, snapshot, ledger, and state.
- CLI: `--smoke-test` (isolated T1–T15), `--verify` (live non-economic smoke + genuine capture), `--handoff` (governed accrual ingest), `--status` (operational).

## 7. Data Source / Symbol Identity

- Logical identity `USATECHIDXUSD` ↔ executable feed `USTECm` (registered mapping `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`, same as the three modules).
- Symbol identity enforced at capture: non-`USTECm` bars are rejected and logged (`SYMBOL_MISMATCH_REJECTED`); no silent remapping.
- Timeframe locked to M1.

## 8. Timestamp / Timezone Handling

- Source MT5 epoch preserved exactly; rendered to deterministic ISO UTC (`%Y-%m-%d %H:%M:%S`).
- Local clock recorded only as acquisition metadata; never substitutes the source bar time.
- Live clock measurement: `quote_source_epoch == local_utc_epoch` → **observed offset 0 s** today; the existing runner's "MT5 epoch as UTC" convention holds for this terminal. DST/seasonal drift remains a monitored risk (§19).

## 9. Raw Capture Format

Append-only CSV, `data/f01/raw/ustechidxusd_m1_raw.csv` (gitignored data area), schema `timestamp,open,high,low,close,volume` — identical to the accrual pipeline's ingest schema; `tick_volume` now preserved via an additive `volume` key in `MT5MarketFeed.latest_completed_bar` (numpy-safe; existing feed tests unaffected — full suite 125/125).

## 10. Append-Only / Duplicate / Quarantine Policy

- **Exact duplicate** (same timestamp + values): idempotent skip, counted.
- **Conflicting duplicate** (same timestamp, different values): quarantined — never overwrites; logged (`CONFLICTING_DUPLICATE_QUARANTINED`); archive hash unchanged (tested).
- **Stale bar** (older than last captured): skipped, logged.
- **Malformed / OHLC-invalid / non-positive / non-M1-aligned bars:** rejected, logged, counted.
- Archive rows are never rewritten, truncated, or backfilled.

## 11. F-01 Accrual Handoff

- `--handoff` invokes `research/f01_v38a_accrual_pipeline.py` `ingest()` with the raw archive as source and the real governed study paths.
- No accrual-governance logic is duplicated in the recorder; the pipeline applies the frozen boundary, admission/quarantine, snapshot hashing, ledger append, and state update.
- Recorder operational status (`--status`, status file, events log) exposes capture/connection state only — never eligible-session or study state (pipeline authoritative, per §20 of the mandate).

## 12. Data Path / Chain of Custody

```text
MT5 (USTECm M1)
      ↓
RAW RECORDER ARCHIVE  data/f01/raw/ustechidxusd_m1_raw.csv
      ↓  (operator --handoff)
F-01 ACCRUAL PIPELINE (frozen boundary, ledger, snapshot, state)
      ↓
F-01 STUDY ARCHIVE    data/f01/ustechidxusd_m1_study.csv
```

Raw recorder archive and study archive are distinct; the recorder never writes the study archive directly.

## 13. Restart / Reconnect

- Persisted status (last bar, cumulative counters) reloaded at start; tail-row cross-check when status is absent.
- Older bars skipped after restart (no duplicate admission); newer bars appended (tested T8).
- Feed unavailability / synthetic feed failure tolerated without raising; capture resumes on recovery (tested T9/T13).
- Missed intervals are not backfilled by the recorder; recovery of genuinely admissible bars remains the governed pipeline's normal ingest path with preserved provenance.

## 14. Security / Credentials

- No credentials, tokens, or connection secrets in code, config, logs, or CLI. Reuses the existing env-configured MT5 connection (`QF_MT5_TERMINAL_PATH`), matching the runner's convention.

## 15. Operational Monitoring

- `--status`: version, symbol/timeframe, raw archive path, cumulative counts (captured, exact dups, conflicts, quarantined, malformed, symbol mismatch, feed-unavailable, errors), last bar, last error.
- Events log (`recorder_events.jsonl`) for quarantine/alert events.
- Supervisor banner and live status now include `F-01 Recorder: ACTIVE (RAW CAPTURE)`.
- No P&L, returns, or economic quantities anywhere.

## 16. Structural Tests T1–T15

Isolated synthetic fixtures, temp data root: **16/16 PASS** (`--smoke-test`).

T1 symbol identity · T2 M1-only · T3 closed-bar · T4 duplicate idempotency · T5 conflicting-duplicate quarantine (archive unchanged) · T6 malformed rejection · T7 append-only · T8 restart recovery · T9 reconnect survival · T10 source-timestamp preservation · T11 pre-freeze cannot enter study · T12 protected data never referenced · T13 recorder failure does not alter module behavior · T14 fresh observations reach accrual interface · T15 no economic/trading tokens in source.

**End-to-end exercise (§30):** synthetic MT5-like source → recorder → raw archive → governed accrual → study admission — **7/7 PASS** in an isolated temp root; real `data/f01/` chain byte-untouched (verified: genesis SNAP-0000, 0 rows).

## 17. Live Smoke Test (§31)

Run against the actual running MT5 environment (`--verify`):

- Connection: CONNECTED — Exness Technologies Ltd / Exness-MT5Trial15.
- Fresh tick: DATA_FRESH; server-vs-UTC clock offset **0 s**.
- Latest completed M1 bar: `time 2026-08-27T12:55:00Z`, O 29486.84 / H 29488.09 / L 29482.34 / C 29483.34, volume 419 — captured to the raw recorder archive (genuine observation preserved raw, per §8).
- **Governed handoff of the genuine bar:** `rows_seen 1, admitted 0, rejected_prefreeze 1` — the frozen boundary (2026-09-03T13:30Z) was enforced by the pipeline on real data; ledger records `SNAP-0002` (predecessor = genesis hash, sha = unchanged archive hash, source = raw archive). Study archive remains **empty**.

## 18. Current Accrual State

From the governed accrual pipeline (`--state`): `eligible_sessions_with_data 0` · `primary_complete False` · `confirmation_complete False` · archive row count 0 · freeze boundary `2026-09-03T13:30:00` · last snapshot SNAP-0002 (chain consistent). Stage 3 remains DATA ACCRUAL PENDING.

## 19. Limitations / Remaining Dependencies

1. **USTECm M1 series stale in the terminal** — the last closed M1 bar dates 2026-08-27T12:55Z (the tick stream is fresh). Until the terminal advances its USTECm M1 history, no new M1 bars exist for the recorder to capture. This is the binding dependency for accrual, not an infrastructure defect.
2. **Server-time convention** — "MT5 epoch as UTC" measured exact (offset 0 s) at smoke time; seasonal/DST drift of the broker server clock would shift session alignment and must be monitored; any confirmed drift requires a governed registration decision, not a recorder fix.
3. **M1 granularity** — tick-level data is intentionally not archived (registered study needs M1).
4. **Known cosmetic ledger quirk** — post-genesis snapshot IDs start at SNAP-0002 (SNAP-0001 label unused); chain integrity is hash-linked and verified; recorded previously, unchanged (frozen infrastructure).

## 20. Final Infrastructure Verdict

**F-01 LIVE OBSERVATION RECORDER OPERATIONAL — NO CURRENT OBSERVATIONS.**

Operational means: the infrastructure can preserve future observations safely — proven on isolated synthetic fixtures and on one genuine live bar whose admission decision was correctly made by the governed pipeline. No Stage 3 readiness, no Stage 3 completion, no Base validation, no Base-eligibility, no profitability claims of any kind.

## 21. Repository / Git Integrity

- HEAD `4edbfdb0f9930060cf66db60e484adb1d6e7b3d5` (unchanged); branch `main`; no commit (infrastructure milestone; no commit by default).
- New file: `scripts/forward/f01_observation_recorder.py`.
- Additive modifications: `scripts/forward/market_data.py` (`volume` key in `latest_completed_bar`); `scripts/forward/quantforge_forward_supervisor.py` (recorder import, instance, loop hook, banner/live-status line).
- Existing forward test suite: **125/125 PASS** after the changes.
- `git diff --check`: clean. Data artifacts under `data/f01/` are gitignored (raw recorder archive, events log, status file).
- Pre-existing dirty/untracked files untouched; no protected data read, modified, or referenced.

## 22. Hard Stop

STOP. No Stage 3 execution, no economics, no F-01 performance inspection, no registration/cost/scope alteration, no protected data use, no Base Registry entry, no Stage 4. The recorder's job is complete: genuine observations can now flow safely from the running MT5 environment into the governed accrual chain. The next research execution remains **F-01 V38A STAGE 3 ECONOMIC VALIDATION**, gated on the frozen registered boundary reaching 63/126 eligible sessions — which additionally now depends on the terminal's USTECm M1 series advancing.