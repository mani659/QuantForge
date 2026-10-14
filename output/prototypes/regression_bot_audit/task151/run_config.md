# TASK151 run configuration — fixed pre-outcome (any deviation voids the run)

- data: eleven `_t37_m1_{SYM}.npz` (OHLC+spread+epoch-ns timestamps);
  row counts must match prereg §2 table exactly or STOP
- integrity: per-file SHA computed + recorded (baseline establishment —
  no reference exists); keys must include time/open/high/low/close/spread;
  timestamps parsed epoch-ns → UTC; ordering + duplicates checked
  (duplicates → STOP); adxcache files never touched
- sklearn: KMeans import verified (1.9.1); kmeans++ init; k ∈ {2,3};
  n_init=1 × seeds 0–9 (10 restarts); lowest inertia wins, first wins ties
- features: EXACTLY log-RV, log-Parkinson, 20-day vol-of-vol, 20-day
  spread percentile; zero-bar days excluded + counted; zero-variance days
  excluded + counted; 19-day warmup dropped + counted; no fill
- normalization: per-symbol z-score with TRAINING means/stds only
- segments (by timestamp): TRAIN 2021-01→2023-12; VALIDATION 2024;
  TEST 2025→panel end
- baselines: pooled-vol (log_rv) tertile split from TRAIN cut points
  (deterministic); shuffled null (permute TRAIN rows, seed 0; expect ARI≈0)
- stability: Hungarian-matched centroid ARI (own-fit vs mapped) on val
  and test; dwell = mean run length (descriptive); prevalence = TEST shares
- aggregation rule (predeclared): per-k verdicts under §8 bars; overall
  CONTINUE iff some k meets all bars incl. null<0.2; overall FAIL iff no k
  meets bars and every k hits a FAIL trigger; else INCONCLUSIVE
- verdict bars (PROPOSED, per prereg §8): CONTINUE needs ARI≥0.5 (val AND
  test) + all regimes ≥10% TEST + null<0.2; FAIL on ARI<0.3 anywhere or any
  regime<5%; else INCONCLUSIVE
- budget: 2 k-configs + tertile + null = 5 fits max, single run; no
  reseeding, no refit, no rescue
- environment: repo .venv (Python 3.11.9, numpy 2.4.6 UNCHANGED, pandas
  3.0.6 UNCHANGED, sklearn 1.9.1 + scipy/joblib/threadpoolctl/narwhals/
  cloudpickle as required deps, installed under TASK151 owner authorization)
