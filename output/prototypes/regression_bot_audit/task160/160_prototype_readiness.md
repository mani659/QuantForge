# TASK160 — S2 Prototype Readiness Plan (conditional; nothing authorized)

**Status:** plan only, executable ONLY after the §1 owner selections are
recorded with signature/date. No implementation exists or is built here.

## 1. Location and interfaces (proposed, not created)

- Proposed: `output/prototypes/s2_newyear_week/s2_engine.py` (new
  directory; created only under a future implementation authorization).
- Interfaces: `load_panel(path) -> daily closes`; `signals(dates, rule)`;
  `evaluate(panel, rule, costs) -> monthly-equivalent event rows`;
  `analyze(rows) -> verdict inputs`. Pure functions; no I/O inside logic;
  no MT5/runtime imports.

## 2. Minimum executable behavior

Exactly the frozen rule once selections exist: December-close entry →
January-window exit per the selected convention; long 1.0×; costs on
traded notional per the frozen schedule; fail-closed missing-data and
duplicate handling; deterministic outputs (sorted events, fixed seeds).

## 3. Reuse (verified available, gated by conformance review at build)

- `lane_b_batch1/data/SPY.csv` (SHA `483919f8`, verified) — panel.
- Batch-1 calendar-window evaluation machinery as PATTERN (not code
  transplant without review); P0 ledger/fills read-paths; pointintime
  timestamp checks; TASK120/146 synthetic-self-test + determinism pattern.

## 4. Tests required before any market-data contact

Synthetic self-test (planted January weeks with hand-computed outcomes):
rule fires on planted window; skips planted gaps; ties/edge dates handled;
cost arithmetic exact; determinism byte-identical; no-look-ahead
(positions use bars ≤ signal date only). Market-data run only after all
green + review sign-off under a future authorization.

## 5. Identity/leakage preservation and correctness evidence

Frozen-rule mirror (code reviewed line-by-line against the frozen spec);
synthetic vectors above; determinism proof (two runs, identical bytes);
conformance checklist signed at review. Correctness = tests green +
review pass — never "looks profitable."

## 6. Exclusions and stop conditions

No tuning, no candidate rescue (RS-302 adjacency noted, not exploited),
no holdout, no profitability claims from implementation tests, no
deployment. Stop: missing data beyond the frozen rule, contract
incompatibility (e.g., considers M1/CFD translation — out of scope),
failed tests, budget exhaustion. Any stop → record, no retry without a
new act.

## 7. Authorization boundary

This plan authorizes NOTHING. Implementation needs (i) recorded owner
selections, (ii) frozen spec, (iii) bounded implementation authorization,
(iv) separate evaluation authorization — none present. HOLD/NONE unchanged.
