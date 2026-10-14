# TASK109 — EXT-062 Source Resolution (B1–B6 and citation conflict)

**Status:** record of a read-only search over existing authoritative records.
No value invented, no parameter estimated, no data file opened for evaluation.
**Scope:** the six TASK108 blockers plus the carried citation discrepancy.

## Method

For each field: (1) definition fixed by the original concept, (2) definition
recoverable from an authoritative existing specification, (3) design decision
not fixed by existing evidence. Category-3 values are not filled. Market-data
files were not used to estimate, optimize, or compare anything. Searched:
task51 sourcing record; task57 discovery report/preregistration/results/engine
header (read-only); task66/68/74/75/77 chain records; task95 library-state
table; handoff §99/§107; role §§3A–3D. No external source access exists in
this repository.

## B1 — Covariance estimation window

- Missing: the lookback length for estimating Σ.
- (1) Original concept: not fixed (task51 §6: PARAMETER UNSPECIFIED).
- (2) Existing spec: TASK57-MDP-001 searched {63, 126, 252} days as
  "mechanism convention," baseline 126 (task57 §§11, 16; results JSON
  `est_window_days`). These are task57's frozen choices, not source-fixed.
- (3) Unfixed for any new specification.
- **Classification: UNRESOLVED.** Task57's values are documented-as-used but
  legally unusable (see §8: reuse = rescue of a closed line).

## B2 — Volatility window

- Missing: the lookback for σ (usually same as Σ — unstated).
- (1) Not fixed. (2) Task57 estimated within the same windows (engine uses
  one estimation frame; no separate vol window in the searched space).
- **Classification: UNRESOLVED** (same reuse bar as B1).

## B3 — Rebalance cadence

- Missing: portfolio rebalance frequency.
- (1) Not fixed ("periodically rebalanced"). (2) Task57 searched {21, 63}
  days (monthly/quarterly convention), 93/31 rebalances over the span.
- **Classification: UNRESOLVED** (same reuse bar).

## B4 — Universe

- Missing: the asset panel.
- (1) Not fixed ("multi-asset cross-section"). (2) Task57 fixed
  {SPY, VEU, AGG, BIL} pre-discovery with SHA-verified Batch-1 files.
- **Classification: UNRESOLVED** (same reuse bar; naming these files now
  would additionally be unauthorized evaluation-data reuse).

## B5 — Unconstrained vs long-only variant

- Missing: which solution form.
- (1) Both forms source-specified (2008 closed form; 2013 long-only
  numerical); the CHOICE is unspecified. (2) Task57 used long-only
  (min_weight ∈ {0.0, 0.05}, SLSQP).
- **Classification: UNRESOLVED** (option set source-resolved; choice open
  and barred from task57 transplant).

## B6 — Return/dividend convention

- Missing: return definition for estimation.
- (1) Not fixed. (2) Task57 used Yahoo auto_adjust total-return closes
  (task57 §6).
- **Classification: UNRESOLVED** (same reuse bar).

## Citation conflict (CRAN "34(4)" vs JPM 35(1), DOI 10.3905/JPM.2008.35.1.40)

- No repository record resolves publisher citations; no external access
  permitted. **Classification: UNRESOLVED, immaterial** (does not affect the
  objective, which is identically stated everywhere).

## §8. Why category-(2) values cannot be used

TASK57-MDP-001 was evaluated and closed: discovery verdict INCONCLUSIVE /
BOUNDARY_EFFECT (task57 §31) → M1 stratified gate NO_REGION → selection NONE
→ task74 conclusion CLOSED / NOT PROMOTABLE ("no selectable region
demonstrated"), rescue_authorized: false, conclusion frozen
(`task77/77_mdp001_status.json`). Library rule: evaluated items are hard
exclusions (task95 §5.2). Transplanting task57's frozen parameters into a
new MDP specification would be rescue/re-run of a closed line without
authorization — prohibited (see ruling package §5). The parameters therefore
exist as historical facts and are unavailable as design inputs.
