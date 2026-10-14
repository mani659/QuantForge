# TASK151 — Task Report

| Field | Value |
|---|---|
| Authorization | Owner APPROVE (Salman Ismail, 2026-10-14) of exactly the TASK148 request; filed |
| Directory | `output/prototypes/regression_bot_audit/task151/` |
| Mode | Single approved bounded chain executed once. No other run. |
| HEAD / branch | `666c1a9` / `main` (unchanged) |
| Date UTC | 2026-10-14 (authorization date) |

## 1. Authority chain (all hashes re-verified)

Preregistration `d28967b4…`, approval record (this package), gate report
from the stopped attempt (prior session, same chain). B4/COMP-01 untouched
and uninvolved (descriptive study, no strategy/comparator).

## 2. Environment remediation (authorized)

scikit-learn 1.9.1 + hard deps (scipy 1.17.1, joblib, threadpoolctl,
narwhals, cloudpickle) installed into the repo .venv; numpy 2.4.6 and
pandas 3.0.6 byte-identical before/after (no unrelated upgrades; pip
itself not upgraded). No manifest/lockfile exists in repo → none changed.
KMeans import + instantiation verified.

## 3. Gates (all passed pre-measurement)

Prereg/TASK148-request hashes; 11 files present with prereg-table row
counts; per-file SHA established + recorded; schema incl. spread;
timestamp parse (epoch-seconds → UTC); ordering/duplicates clean;
OHLC+spread constructible; volume confirmed absent; adxcache untouched;
sklearn config matches frozen spec; synthetic self-test 12/12 green with
determinism (one timestamp-unit bug found+fixed pre-data); budget
enforceable (5 fits).

## 4. Measurement outcome (reported, not promoted)

n=train 10374/val 3550/test 6192; k=2 ARI 0.745/0.853 prev 53.5/46.5
dwell 7.3; k=3 ARI 0.853/0.402 prev 49.3/25.4/25.3 dwell 5.6; tertile
balanced/dwell 3.8; null ARI 0.852 → override → **INCONCLUSIVE**.
No trading, sizing, candidate, profitability, or follow-on implication.

## 5. Boundary confirmations

No sweep/rerun/variant, threshold/method change, registration, promotion,
deployment, runtime alteration, commit, or push. No omission: null
override, degeneracy risks, documentation defect, and adverse mechanics
fully reported. HOLD / Active Research NONE unchanged (re-verified
post-write).

## 6. Manifest (verified after all edits)

| File | Purpose | Size / SHA-256 |
|---|---|---|
| `150_data_use_approval_record.md` (task150) | Filed owner approval | 1115 B / `6f81998d…968b0` |
| `regime_pipeline.py` | Reviewed pipeline incl. one pre-data timestamp-unit fix | 6926 B / `93d4d857…59f18d7` |
| `test_pipeline_synthetic.py` | Synthetic self-test, 12/12 (G4) | 3775 B / `da118f19…0aa26d9` |
| `run_config.md` | Frozen pre-outcome config | 2007 B / `686f7e95…56264fa0` |
| `run_measurement.py` | Single-run gated runner | 5675 B / `cf8e1c6f…0121575` |
| `assignments.csv` | TEST assignments, 6192 rows | 240429 B / `81ca2afe…9b88cc0` |
| `metrics.json` | Metrics, gates, verdict | 89611 B / `e384594f…f54e9f4a` |
| `REPORT.md` | Bounded stability report | 2490 B / `5bffc54d…d24dd79f9` |
| `151_task_report.md` | Verification and final status (this file) | digest in completion message |
