# PROTO-TREND-001 Code Freeze v2 (Phase-1B)

v1 is superseded because its main() was incomplete (it raised SystemExit
before any pipeline ran); v1 pure functions are carried over unchanged
where correct (see change list in GATE_REPORT_1B.md).

Self-test: `test_evaluate_v2.py` run 2026-10-08 (repo .venv, synthetic data
only) — **41 v1 checks kept green + 25 new v2 checks pass, 0 failures**:
closure-label branches incl. all six single-criterion failures; end-to-end
main() on synthetic real-format files (PASS / PASS+FINANCING WARNING /
ECONOMICALLY INSUFFICIENT / NEGATIVE / N<8 stop / determinism /
REPORT markers); cutoff truncation; F-SNAP missing-date error.

Frozen code (read-only from this point; any change invalidates these hashes):

- `evaluate_v2.py` — 29643 bytes — sha256 `c7bb98faa235bb882a9ff5b7b14166eb588b393e17b51717ed517ec280526ad8`
- `test_evaluate_v2.py` — 12924 bytes — sha256 `ef10212f73af072d1d975012c7e30132be3eb7e4e588ff5d92334f4c6867c654`
- `universe.json` — 2160 bytes — sha256 `60a55578623ff31906b7f40fc11b68287972bbaa59bf99fd2d7680fb30583005` (unchanged since Phase 1)

Phase 2 must verify these hashes still match before running (S7).

## Attestation — every computation on real market data performed so far

The ONLY computations on real market data performed in Phase 1 and Phase-1B,
listed exhaustively (each verified against its authorizing clause):

1. S3 acquisition reads: per-series row counts and first/last dates for
   MANIFEST.csv (authorized: S3 manifest fields).
2. S4 integrity gate: monotonicity, duplicate counts, NaN row counts,
   missing-weekday runs, and row-to-row Close returns ONLY for the
   threshold-flag lists (A11 gate; authorized: S4).
3. X1 cross-check (owner-approved): for 8 flagged dates, one broker M1
   21:00-UTC close pair + return + ratio each (authorized: X1 rule text).
4. B3 structure-check: per real file rows, first/last dates, dtype status,
   rows-after-cutoff counts (authorized: B3; computes no returns/signals).
5. sha256/file-size reads for manifests, freezes and this file (authorized:
   S2/S6/B4/B6 bookkeeping).

Nothing else was computed from real market data. No signals, no positions,
no portfolio, no Sharpe, no strategy return, no bootstrap, no drawdown, no
control, no cost-grid evaluation, no confirmation. The evaluator ran ONLY on
synthetic data (test suite); main() was never executed against data_raw/.
