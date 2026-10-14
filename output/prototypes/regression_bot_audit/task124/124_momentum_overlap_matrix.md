# TASK124 — Momentum Overlap Matrix (component-by-component)

**Proposed hypothesis (TASK123):** Pure cross-sectional momentum (XSM) on
SPY/VEU/AGG/BIL — rank 4 ETFs by trailing 12-month total return; long
top-quartile (2 assets), short bottom-quartile (2 assets); equal-weight
long/short; monthly rebalance; no TSMOM gate, no defensive state, no
single-asset concentration.

## Prior exact specifications on the same ETF panel

| Prototype | Signal | Construction | Rebalance | Result |
|---|---|---|---|---|
| PROTO-GEM-001 | Absolute TSMOM gate (SPY vs BIL r12) → if pass, relative leg (SPY vs VEU r12); tie → SPY | 100% single asset (SPY, VEU, or AGG defensive) | Monthly, next-open | NEGATIVE (−30.61 bps/mo vs control) |
| PROTO-VM-001 | Volatility targeting (Moreira-Muir): w = c/Var(m) | Vol-scaled SPY + TB3MS | Monthly | COST_FAILURE |
| PROTO-TOM-001 | Turn-of-month 4-day window | SPY only | 4-day window | COST_FAILURE |
| TASK57-MDP-001 | Max diversification: max DR(w) = wᵀσ/√(wᵀΣw) | Long-only, sum(w)=1, SLSQP | Every 21/63 days | ROBUSTNESS_FAILURE topology → CLOSED |
| TASK60-REBAL-001 | Fixed-mix rebalancing | Long-only, fixed weights | Periodic | ROBUSTNESS_FAILURE + STATISTICALLY_UNSUPPORTED |
| TASK61-CORR-001 | Correlation-regime allocation | Long-only, regime-gated | Periodic | ROBUSTNESS_FAILURE + STATISTICALLY_UNSUPPORTED |

## Component-by-component comparison: XSM vs GEM (the closest prior)

| Component | GEM (exact) | XSM (proposed) | Overlap classification |
|---|---|---|---|
| Ranking variable | r12(SPY) vs r12(BIL) [absolute gate]; r12(SPY) vs r12(VEU) [relative leg] | r12 of all 4 ETFs, ranked | **Materially overlapping mechanism, distinct testable prediction** — GEM uses r12 for a sequential 2-asset comparison; XSM uses r12 for a simultaneous 4-asset ranking |
| Formation period | 12 months | 12 months | Same |
| Rebalance | Monthly, next-open | Monthly | Same |
| Portfolio construction | 100% single asset (concentrated) | Equal-weight long/short across cross-section (diversified) | **Genuinely distinct mechanism** — concentration vs diversification |
| Defensive state | 100% AGG on gate failure | None (always long/short) | **Genuinely distinct mechanism** |
| Gate structure | Sequential: absolute gate → relative leg | Simultaneous: rank all 4 | **Genuinely distinct mechanism** |
| Cross-sectional scope | Binary (SPY vs VEU, 2 assets) | Full ranking (4 assets) | **Materially overlapping mechanism, distinct testable prediction** |
| Tie handling | US equity (SPY) | Not specified (must be frozen) | Unresolved — must be specified at preregistration |
| Cash/negative signals | Never in cash (AGG defensive) | Short leg provides negative exposure | **Genuinely distinct mechanism** |
| Execution timing | Next session open | Not specified (must be frozen) | Unresolved |
| Cost model | 10/5/0 bps/side (Batch-1 frozen) | Not specified (must be frozen) | Unresolved |

## XSM vs MDP-001 (the allocation-rule prior)

| Component | MDP-001 | XSM | Classification |
|---|---|---|---|
| Signal | None (allocation rule) | r12 ranking | **Genuinely distinct mechanism** |
| Construction | Long-only, sum(w)=1, max DR | Long/short, equal-weight | **Genuinely distinct mechanism** |
| Economic question | Does risk-based allocation outperform? | Does relative-strength ranking predict returns? | **Genuinely distinct mechanism** |

**Does MDP-001 answer the XSM economic question?** No. MDP-001 tests
whether a specific allocation rule (maximize diversification ratio) produces
positive risk-adjusted returns. XSM tests whether trailing relative
performance predicts future relative performance. These are different
economic questions. MDP-001's closure does not constrain XSM.

## XSM vs VM-001 and TOM-001

| Component | VM-001 | TOM-001 | XSM | Classification |
|---|---|---|---|---|
| Signal | Volatility (not return) | Calendar (not return) | Return ranking | **Genuinely distinct mechanism** |
| Construction | Vol-scaled long | Long only | Long/short | **Genuinely distinct mechanism** |

## Summary classification

| Prior | Overlap with XSM |
|---|---|
| PROTO-GEM-001 | **Materially overlapping mechanism, distinct testable prediction** — GEM's relative leg is a binary cross-sectional comparison embedded in a sequential gate with a defensive state and single-asset concentration; XSM is a pure simultaneous 4-asset ranking with no gate, no defensive state, and long/short construction |
| PROTO-VM-001 | **Genuinely distinct mechanism** |
| PROTO-TOM-001 | **Genuinely distinct mechanism** |
| TASK57-MDP-001 | **Genuinely distinct mechanism** |
| TASK60-REBAL-001 | **Genuinely distinct mechanism** |
| TASK61-CORR-001 | **Genuinely distinct mechanism** |

**Key distinction from GEM:** GEM's cross-sectional component was never
isolated — it was always combined with the absolute TSMOM gate and the
defensive AGG state in a 100%-single-asset construction. The pure XSM
signal (simultaneous 4-asset ranking, long/short, no gate, no defensive
state) has never been tested. A different name or omission of an overlay
is not by itself proof of independence — but here the distinction is
mechanistic (simultaneous vs sequential, diversified vs concentrated,
long/short vs single-asset), not merely nominal.

**Unresolved items (must be frozen at preregistration):** tie handling,
execution timing, cost model, position sizing (equal-weight vs
vol-scaled), rebalance drift handling.
