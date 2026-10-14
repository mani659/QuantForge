# TASK147 — Branch Closure, First ML Direction, and Roadmap (single report)

## 1. Branch-closure verification

VS-TSMOM-01: single bounded run completed under recorded approval
(TASK146: n=474, FAIL — D1 mean −55 bps, CI entirely negative, Holm p=1.0,
ratio −17.96; no promotion/continuation/rescue). Artifacts re-verified
intact this session (task146 report `f8047ad9…`, REPORT `19d70c14…`,
results `08332de4…`, monthly 474 rows `1f97224c…`). HOLD / Active Research
NONE confirmed. **VS-TSMOM-01 is CLOSED as tested** (failed confirmation,
not universal falsification). No rerun, rescue, retune, or reopening.

## 2. ML-relevant evidence on record (no new research performed)

- **Modeling precedent:** almost none as prediction — only statsmodels
  Logit used *diagnostically* on trade outcomes (`_t24_run_analysis.py`,
  `_t39_stats.py`). No sklearn/RF/SVM/KMeans strategy model exists.
- **Infrastructure reusable:** `research/pointintime/` (leakage property
  checks), `research/p0` (ledger/fills), `p1` (search control), `p2`
  (validation), `research/g6_forward` (forward/paper harness),
  `research/analytics` (evaluator/metrics/verdict).
- **Data substrate:** `_t37` 11-symbol M1+H4+spread cache (2021→2026,
  ~2–3M M1 bars/symbol) — the only multi-symbol panel with spread data
  (costs directly measurable); M1 panels (5 symbols); tick canonical
  (4 symbols); FRED indices; Batch-1 ETFs (evaluation budgets consumed).
- **Labels without look-ahead:** unsupervised methods need none by
  construction; supervised targets must be point-in-time functions of
  already-printed bars (pointintime checks reusable).
- **Closed-signal fence (binding):** trend/momentum, mean reversion,
  breakout, session, calendar, sweep, grid, vol-targeting economics, and
  price-regression trend models (R1) may not reappear inside ML features,
  targets, or regimes. Any regime or model that re-expresses them is out.

## 3. Comparison (no fabricated scores; evidence cited per row)

| Approach | Hypothesis fit | Data/infra fit | Label safety | OOS | Interpretability | Overfit burden | Cost feasibility | Beyond baseline? | Standing |
|---|---|---|---|---|---|---|---|---|---|
| K-means regimes (vol-risk use) | Volatility clustering is real; regime-conditioned sizing is risk management, not a directional edge | _t37 panel + spread; pointintime checks | Unsupervised: none needed | Chronological split feasible | Centroids inspectable | k/scaling/window must be frozen (medium) | Switch turnover measurable from spread | Must beat static allocation (testable) | **RECOMMENDED first** |
| Linear regression (forward return) | Collides with R1 (price-regression trend, excluded at admission) on any price/trend feature set | Same panels | Labels point-in-time-able | Feasible | High | Low params, but gate is legal not statistical | Modelable | Untestable without an owner distinctness ruling first | NOT first (reopening risk) |
| Logistic (predictive) | Needs a base event to classify — none exists without a strategy | Same | Same label machinery as above | Feasible | High | Low | Modelable | Depends on the event definition | NOT first (second-stage tool) |
| Random forest | Same hypothesis problem as linear, plus opacity | Same; slower | Same | Feasible but CV-tricky | Low | HIGH (depth/trees/features/samples) | Learnable-noise risk | Only after an interpretable baseline shows signal | NOT first |
| SVM | Same as RF with worse calibration/scaling | Same; slowest | Same | Feasible | Lowest | HIGH (kernel/C/gamma) + poor probabilities for cost-aware sizing | Same | Same precondition | LAST |

Neither supervised direction is presumed better than regime detection, and
K-means is not presumed superior — it wins on: smallest falsifiable unit
(do stable vol regimes exist out-of-sample? — answerable with zero
trading), zero label-leakage surface, direct spread-based costing, and no
dependence on any closed directional signal *provided the feature set is
fenced to volatility/spread/volume-rate inputs* (trend, reversal,
breakout, session, and calendar features explicitly excluded).

## 4. Recommended first branch (+ fallback)

**RECOMMENDED — K-means volatility-regime characterization on the _t37
panel, descriptive only (no trading):**
- Hypothesis: realized-volatility regimes in FX/metals are stable,
  out-of-sample-persistent partitions (not: tradeable edge — that is a
  later, separately authorized question).
- Market/timeframe: _t37 11 symbols, H4 bars 2021→2026 (M1 reserved for
  future granularity work, not this step).
- Features (frozen pre-outcome): rolling realized-volatility levels and
  vol-of-vol + spread percentiles only. Fenced OUT: returns, slopes,
  moving-average positions, breakout/session/calendar constructs.
- Baseline: single-regime (static) allocation — regimes must beat it on
  stability (adjusted Rand across chronological folds), not returns.
- Structure: chronological train/validation/test; k frozen (k=3 proposed:
  low/medium/high vol — owner-visible, not tuned); no look-ahead (features
  use strictly past bars; pointintime checks applied).
- Costs: switch-count × spread (descriptive turnover accounting, not a
  strategy P&L).
- Metrics: regime persistence, OOS stability, turnover rate. No Sharpe, no
  returns-based claim.
- Continue iff: OOS stability exceeds the prefrozen bar with no
  reselection. Fail conditions: instability, k-sensitivity flips, any
  directional-signal creep → stop, record, no rescue.
- Reuse: _t37 cache, pointintime leakage checks, P0 fills/analytics
  read-paths, TASK120/146 review patterns.

**FALLBACK — logistic diagnostic on existing closed-trade records**
(proven `_t24/_t39` pattern): characterize WHEN closed strategies failed
(regime-conditional failure analysis on Batch-1 monthly CSVs, CAND-025
events.csv, VS-TSMOM-01 monthly_series.csv). Zero new data use, zero new
predictions, purely informational — directly improves negative-knowledge
quality at negligible cost.

**Ranked lower:** linear (R1-reopening risk), RF/SVM (overfit burden +
opacity before any baseline exists).

## 5. Three-task roadmap (each gated; later tasks need their own approvals)

1. **File the bounded regime-study preregistration + data-use
   authorization request** (frozen features/k/stability metric/OOS split/
   stops; _t37 descriptive use only). Smallest useful step; documentation
   only.
2. **(Conditional on approval) Execute the one bounded stability
   measurement + report** (stability verdict only; no trading, no P&L).
3. **(Conditional on stable regimes) Design — not execute — the
   regime-conditioned sizing rule** with its own preregistration and
   authorization request.

## 6. Authorizations, blockers, resources (estimates labeled)

- Required owner acts: (i) _t37 descriptive-use authorization for Task 1's
  study (no evaluation); (ii) execution approval for Task 2; (iii) any
  trading-use design needs a fresh act. Exact texts belong in those tasks,
  not here. No signatures inferred or manufactured.
- Blockers: none for Task 1 (writable now); Tasks 2–3 blocked on (i)–(iii).
- Resource estimates: Task 1 documentation-only (~1 task); Task 2 single
  bounded measurement on 11-symbol H4 cache (minutes of compute, one run,
  no sweeps); Task 3 design-only. No data purchase, no new infrastructure.

## 7. Final decision: RECOMMEND_BRANCH

K-means volatility-regime characterization (fenced, descriptive-only) as
the first ML branch; logistic diagnostic on existing records as fallback.
HOLD/NONE unchanged; Lane A/B separation preserved (no candidates, no
registrations); preregistration, outcome-blindness, and negative
knowledge preserved; existing validated infrastructure reused, none
duplicated. No commits, pushes, deployments, or governance changes.
