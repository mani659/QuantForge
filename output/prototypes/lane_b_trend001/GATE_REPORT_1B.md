# GATE_REPORT_1B — PROTO-TREND-001 Phase-1B (PHASE_2_GO: NO)

## 1. Precondition: PASS

Part A sha256 still `4b44615dcf1646bd…` (full match); frozen spec + annex
byte-identical; Phase-1 code hashes match CODE_FREEZE.md (evaluate.py
d2dc2eb9…, test_evaluate.py 6777e88e…, universe.json 60a55578…).

## 2. X1 metals cross-check: 1 PASS / 3 PASS / 4 FAIL / 6 UNVERIFIABLE

Rule: signs agree AND 0.6 ≤ broker/vendor ≤ 1.6, else FAIL → removal.
Broker return = M1 21:00-UTC close flagged-date ÷ previous-weekday 21:00
close − 1 (XAUUSD 2021-04-12→2026-04-10; XAGUSD 2021-07-13→2026-07-12).

GC=F 2026-01-30: vendor −0.107796, broker −0.104492, ratio 0.9694 → PASS.
SI=F 2025-12-31: −0.093571 / −0.066704 / 0.7129 → PASS.
SI=F 2026-02-03: +0.081586 / +0.060786 / 0.7451 → PASS.
SI=F 2026-02-12: −0.098001 / −0.113446 / 1.1576 → PASS.
SI=F 2025-12-30: +0.107621 / +0.046084 / 0.4282 → FAIL.
SI=F 2026-01-26: +0.140253 / +0.059872 / 0.4269 → FAIL.
SI=F 2026-01-27: −0.083047 / +0.029607 / −0.3565 → FAIL (sign flip).
SI=F 2026-02-05: −0.090727 / −0.158282 / 1.7446 → FAIL.
UNVERIFIABLE (no exact-21:00 bar in broker feed; no substitution made):
2022-10-03, 2025-04-04, 2025-12-29 (prev missing), 2026-01-30, 2026-03-19,
2026-05-15 (all SI=F). Pre-2021 flags outside broker span: not applicable.
CONSEQUENCE: SI=F is EXCLUDED by the removal rule. universe.json is frozen
read-only, so the listing is an OWNER ACTION before Phase 2 (record in
universe.json as "removed"; no vendor substitution). Nothing else computed
from broker files.

## 3. v1 → v2 change list

Kept byte-identical in behavior: month_table, signal_at, sigma_at,
holding_return, check_no_lookahead, sharpe, bootstrap_lower,
max_drawdown_rescaled, financing tables/constants, load_market_csv,
CutoffRefusal/LookaheadError. Changed per annex: load_universe (IA-16:
vendor mapping, NaN drop, sort/dedup, truncate-at-cutoff with logged drops,
max-date assert; panel refuses later frames); row entry = earliest e across
active + per-market own entries (IA-17); F-SNAP own-entry price +
FsnapError (IA-18); N<8 → DataIntegrityStop + STOP_REPORT.md, nothing else
(IA-19); full main() incl. criteria/closure/grid/stress/control/ex-bitcoin/
diagnostics/REPORT (IA-20); vectorized bootstrap (identical distribution);
positional panel internals (identical values; no-look-ahead call documented
as tautological, real protection = direct unit test per ERRATA_1B.md).

## 4. Tests: 41 kept + 25 new, all green

test_evaluate_v2.py (synthetic only; never loads data_raw): 41 v1 checks
green; closure branches incl. all six single-criterion failures; e2e main()
on real-format synthetic CSVs (PASS / PASS+FINANCING WARNING /
ECONOMICALLY INSUFFICIENT / NEGATIVE / N<8 stop / determinism byte-identical
/ REPORT markers); cutoff truncation; F-SNAP missing-date error. 66/66 PASS.

## 5. v2 hashes (CODE_FREEZE_v2.md; files read-only)

evaluate_v2.py 29643 B sha256 c7bb98fa…280526ad8; test_evaluate_v2.py 12924 B
sha256 ef10212f…46867c654; universe.json 2160 B sha256 60a55578…0830fb
(unchanged since Phase 1). Attestation of every real-data computation is in
CODE_FREEZE_v2.md (gate flags, X1, structure counts, hashes — nothing else).

## 6. Errata: ERRATA_1B.md (annex header vs B4; tautological check; v1 test f)

PHASE_2_GO: NO — run ends here. No evaluation performed.
