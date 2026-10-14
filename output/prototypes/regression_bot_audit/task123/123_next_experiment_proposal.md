# TASK123 — Next Experiment Proposal

**Status:** PROPOSED, not authorized. No experiment started. No data
accessed. Distinction from closed candidates explicitly justified below.

## The single recommended direction: cross-sectional momentum on the ETF panel

### Why this direction (not a list)

This is the only direction that simultaneously (a) has a plausible economic
mechanism, (b) has never been isolated and tested on verified available
data, (c) uses a sample size adequate for statistical power, and (d) is
genuinely distinct from every closed candidate in the ledger.

### Economic mechanism

Cross-sectional momentum (relative strength): assets with higher trailing
returns tend to continue outperforming over the intermediate horizon,
reflecting gradual information diffusion and behavioral under-reaction.
This is one of the most robust anomalies in the empirical asset-pricing
literature and is distinct from time-series momentum (single-asset trend
following) — the cross-sectional effect is about relative performance
persistence, not absolute trend persistence.

### Distinction from closed candidates (explicitly justified)

| Closed candidate | What it tested | Why this is different |
|---|---|---|
| PROTO-GEM-001 (dual momentum, NEGATIVE) | Absolute TSMOM + relative cross-sectional + defensive AGG overlay | GEM conflated cross-sectional with TSMOM and a defensive overlay; the pure cross-sectional signal was never isolated |
| DISC-022 / TSMOM-V1/V2 (fixed 12/1 TSMOM) | Single-asset time-series momentum on 28 futures | Time-series momentum is absolute trend; cross-sectional is relative ranking |
| PROTO-VM-001 (vol targeting) | Volatility-scaled position sizing | Sizing rule, not signal generation |
| TASK57-MDP-001 (max diversification) | Risk-based allocation | Allocation rule, not signal generation |
| TASK60-REBAL-001 / TASK61-CORR-001 | Fixed-mix / correlation-regime allocation | Allocation rules, not signal generation |

The proposed direction is **pure cross-sectional momentum** (rank ETFs by
trailing 12-month return; long top-quartile, short bottom-quartile,
rebalanced monthly) with no TSMOM filter, no defensive overlay, and no
allocation overlay. This specific implementation has never been tested.

### Falsifiable prediction

**H1:** Top-quartile ETFs by trailing 12-month return outperform
bottom-quartile ETFs by a mean net differential > 0 bps/month over the
evaluation window, net of transaction costs.

**Falsifier:** The bootstrap lower bound of the mean net differential ≤ 0
at the frozen cost assumptions.

### Required data and verification

- **Data:** SPY/VEU/AGG/BIL total-return daily closes (already verified in
  the repository; `data/provenance.json` hashes on record). No new data
  collection.
- **Integrity check:** SHA-256 recompute of each file against its reference
  hash before any use. Fail-closed on mismatch.
- **Sample:** Monthly rebalancing, ~216 months (2008-06 to 2026-09,
  matching the GEM/VM evaluation span for comparability).

### Preregistration requirements (frozen before any outcome access)

1. **Primary outcome:** mean net monthly differential (top-quartile
   minus bottom-quartile), net of transaction costs.
2. **Cost assumptions:** Owner-frozen per-side spread/slippage/commission
   (the Batch-1 family: spread 10 / slippage 5 / commission 0 bps/side).
3. **Statistical procedure:** 95% bootstrap CI (B=10000, i.i.d. over
   months, seed fixed); Holm α=0.05 across the decision family.
4. **MDE (minimum detectable effect):** Preregistered based on the
   expected cross-sectional spread and the frozen costs; must be set before
   outcome access.
5. **Stop criteria:** bootstrap lower bound ≤ 0 → stop; budget exhaustion
   → stop; any preregistered bar not met → stop.
6. **Multiplicity control:** Holm across {primary, stress2, stress4}.
7. **No post-outcome changes:** any change creates a new preregistration.

### Evidence requirements before execution

1. Data SHA-256 verification (all four ETF files).
2. Synthetic self-test of the implementation (planted cross-sectional
   signal; verify exact rule semantics, no look-ahead, determinism).
3. Preregistration filed and reviewed.
4. Independent implementation review (conformance to frozen spec).

### Why this provides more information than idea generation

- Tests a specific, well-documented anomaly (not a broad search).
- Uses verified, already-hashed data (no acquisition risk).
- Sample size (~216 months) provides adequate power for a monthly
  rebalanced design (unlike the single-shot intraday studies that dominate
  the failure population).
- Directly tests a component that was conflated in GEM's dual-momentum
  design — informative even if negative.
- Distinct from every closed candidate by explicit mechanism (relative
  ranking vs absolute trend following).

### Missing fact that would prevent selection

None. The direction is implementable with verified available resources.
The only missing inputs are the owner's preregistration of the MDE and
cost assumptions, which are routine owner acts, not blockers.

### Principal risk

The cross-sectional momentum effect may be weaker in a 4-asset ETF panel
than in broad equity cross-sections (the effect is typically estimated on
hundreds of stocks). The 4-asset panel may be too thin to produce a
reliable signal. The cheapest decisive test: the Stage 1 screening test
(above) with a predeclared MDE; if the screening CI excludes zero, the
question is resolved cheaply.
