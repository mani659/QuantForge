# TASK168 — S2 Preflight Report (pre-outcome; PASS)

Run before any strategy-return calculation. Authorization record
(`168_s2_evaluation_authorization.md`) was written first.

## 1. Fingerprints verified (SHA-256, all MATCH)

| Artifact | SHA-256 | Status |
|---|---|---|
| Frozen spec `166_s2_frozen_spec.md` (PROTO-S2-001) | `5a318e7e47263c67dc308adf9e326122e56b285e5eaaf585274867525a47eb94` | MATCH |
| Selections `166_s2_owner_decisions.md` | `12448126490fd1bbc4b926ac470a53b24a44c81b37fde1e2b7573e57b6ddce7c` | MATCH |
| Implementation `s2_engine.py` | `2892c8b5f3f9c13fe1dd3317d45f5f33725437be1f3936501943699dcff97f7b` | MATCH |
| Synthetic suite `test_s2_engine_synthetic.py` | `508c4e485e05f96150b0af979966692551a34bc1c5c4bb703e8743cd042cdb83` | MATCH |
| Data `lane_b_batch1/data/SPY.csv` | `483919f897326b261a669bc595a37112b4de5222c4ad0ed84da08060f4b71231` | MATCH |
| TASK167 package | `22b8eb46554f7c1437d17b0cf71a54aff3947b3f2b971c8dc398832816278b6e` | MATCH |

## 2. Synthetic preflight (no market data)

Command: `.venv\Scripts\python.exe output/prototypes/s2_newyear_week/test_s2_engine_synthetic.py`
Result: **12/12 PASS** (planted week, cost arithmetic, both skip paths,
both integrity stops + clean pass, determinism, control arithmetic,
cost-drag year, trichotomy).

## 3. Frozen-contract checks

- **Costs:** entry Dec_close ×1.0015 / exit Jan5_close ×0.9985 =
  (10 spread + 5 slippage) per side, commission 0 → 30 bps RT; control
  bears the schedule once each. Matches spec §7 and TASK167
  reconciliation; no amendment.
- **Windows/holidays:** FIRST_5_SESSIONS = first five January row-dates
  by date order (holidays skipped by construction, never imputed);
  missing endpoints → fail-closed skip + count. Deterministic from
  timestamps alone; TASK167 dates-only screen: 33 eligible Januaries
  1994-01→2026-01 (exact N set mechanically at execution).
- **TOM_CONTROL:** fully defined in spec §4 (identical span, same cost
  schedule once, cumulative-net descriptive, no paired test).
- **Primary endpoint:** mean annual net + 95% bootstrap CI, B=10000,
  seed 20261015 (spec's only resampling); PASS/FAIL/INCONCLUSIVE
  thresholds frozen in spec §8; no magnitude bar imposed.
- **Data readiness:** span 1993-01-29→2026-09-25, monotonic unique
  timestamps, 0 total NaN, no yearly >5% (TASK167 screen); close column
  present; execution-close convention supported.
- **Scope:** single panel, no holdout, no new data, no substitution.

## 4. Gate decision

All preflight conditions PASS → authorized single execution proceeds
under `168_s2_evaluation_authorization.md`. HOLD/NONE unchanged.
