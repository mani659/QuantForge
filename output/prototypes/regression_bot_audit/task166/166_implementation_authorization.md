# TASK166 — Scoped Implementation Authorization (bounded; task order only)

**Authority:** TASK166 task order ("proceed directly to implementation
under this task's bounded engineering scope"). This note records scope,
not a governance change. No owner signature is claimed beyond the
selections record (separate file).

## Authorized (this task only)

- Minimal exact-to-spec engine at
  `output/prototypes/s2_newyear_week/s2_engine.py` (new directory).
- Colocated synthetic-only self-test
  (`test_s2_engine_synthetic.py`) — placed beside the engine (not in
  `tests/`) to avoid entangling the frozen platform suite; precedent:
  TASK120/146/151 colocated self-tests. Rationale recorded here.
- Running the synthetic tests ONLY (constructed fixtures; zero market
  data; zero outcomes).

## Explicitly not authorized

Historical backtest, any market-data execution, parameter search, model
fitting, holdout access, data collection, candidate registration/status
change, paper/live trading, deployment, governance edits, commits, pushes.
Implementation review + synthetic green lights NOTHING beyond themselves;
evaluation needs a separate explicit act.

## Boundaries enforced and verified post-write

HOLD / Active Research NONE unchanged. No prior artifact modified. Work
stops at tested code + this report.
