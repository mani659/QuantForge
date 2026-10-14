# EXT-062 — Maximum Diversification Portfolio: Proposed Specification (DRAFT)

**Status:** PROPOSED DRAFT — NOT admitted, NOT frozen, NOT bound to any
evaluation, NOT validated, NOT profitable, NOT approved for trading.
**Library ID:** EXT-062 (preserved, unadjudicated).
**Prototype ID:** UNASSIGNED — to be assigned by the owner at a freeze decision, if any.
**Scope of this document:** source-faithful transcription of the concept plus
explicitly marked blockers. No value was invented to make it appear complete.

## 1. Identity and provenance (documented facts)

- **Concept:** Maximum Diversification Portfolio (MDP), risk-based portfolio
  construction — a weighting rule, NOT a directional price rule.
- **Primary source:** Choueifaty, Y. & Coignard, Y. (2008), "Toward Maximum
  Diversification," *Journal of Portfolio Management* 35(1), 40–51,
  doi:10.3905/JPM.2008.35.1.40. Long-only constraint form attributed to
  Choueifaty, Froidure & Reynier (2013). (Task51 records a CRAN "34(4)"
  citation conflict against JPM/publisher/working-paper 35(1) — discrepancy
  carried, not resolved.)
- **Recorded evidence:** none empirical in this repository. Task51 normalized
  spec (§6), classification DISTINCT, data PARTIALLY, rating Strong on
  objective/closed form (`task51/51_external_classical_strategy_sourcing.md`
  §§6, 10–13, 15). Original source claim (higher long-run return at lower
  volatility vs cap-weighting, in-sample) is a SOURCE CLAIM — UNVERIFIED.

## 2. Causal rationale and failure conditions (from the concept, not new claims)

- **Rationale:** maximizing the diversification ratio harvests asset risk
  premia more efficiently than capitalization weighting by allocating toward
  the volatility/correlation structure rather than market size.
- **Conditions under which the rationale should fail:** covariance estimation
  error dominates the signal; correlations spike toward 1 in stress
  (diversification evaporates); the cross-section is too thin for a stable
  Σ⁻¹σ; turnover/financing (unaddressed by source) exceeds the harvested
  premium. These are the concept's own fragilities, listed for future test
  design — not predictions.

## 3. Market and instrument scope

- **Source statement:** "multi-asset cross-section (stocks, or any asset
  panel)."
- **BLOCKER B4 — universe UNSPECIFIED.** No universe is selected here.
  Background only (not a selection): Task51 §11 rates compatibility
  PARTIALLY via the `_t37` 11-symbol cache or the 4-ETF set, both thin.
  Selecting either would be a design decision requiring separate
  authorization plus a data-scope decision (existing-file reuse is
  unauthorized). This field must be frozen with an explicit universe before
  any implementation decision.

## 4. Timeframe and required inputs

- **Rebalance cadence: BLOCKER B3 — UNSPECIFIED by source.**
- **Required input type:** cross-section of asset returns sufficient to
  estimate Σ (N×N covariance) and per-asset volatilities σ. No files named,
  no data touched. Return/dividend convention for estimation: **BLOCKER B6.**

## 5. Signal calculation and entry conditions

- There is no market-timing signal. The "signal" is the weight vector solving,
  at each rebalance date:
  `maximize DR(w) = wᵀσ / √(wᵀΣw)`.
- **Unconstrained form (source-specified):** closed form `w ∝ Σ⁻¹σ`,
  normalized to sum 1.
- **Long-only form (2013, source-specified):** maximize DR subject to `w ≥ 0`,
  `Σw = 1`; no closed form — numerically optimized (equivalently
  `min yᵀΣy s.t. σᵀy = 1, y ≥ 0`, then normalize).
- **BLOCKER B5 — variant UNSPECIFIED** (unconstrained closed form vs
  long-only numerical). A documented variant choice; selecting one without a
  source basis would be invention.
- **Entry:** apply the computed weights to the portfolio at the rebalance
  date. No per-trade trigger exists by design.
- **Estimation windows: BLOCKER B1 (covariance window), BLOCKER B2
  (volatility window, usually same as Σ — unstated).**

## 6. Exit conditions and position lifecycle

- No exits as trades exist by design. Lifecycle = hold weights until the next
  rebalance date (cadence: BLOCKER B3). Drift handling between rebalances is
  unspecified by source — carried as part of B3, not filled.

## 7. Risk limits and position sizing

- Sizing IS the weight vector (fully invested, weights sum to 1 —
  source-specified normalization). Leverage is unspecified by source; no
  leverage is assumed and none is authorized (default is 1.0× fully
  invested; any other value would require explicit authorization).
- No stops/targets exist in the source (buy-hold-rebalance weighting) —
  recorded as source-faithful absence, not a gap to fill by invention.

## 8. Execution assumptions, costs, missing data

- **Transaction-cost fields: BLOCKER** — source specifies none. Required at
  freeze: per-side spread/slippage/commission schedule and turnover
  accounting. Not invented here.
- **Missing/invalid data handling: BLOCKER** — source specifies none.
  Required at freeze: staleness, corporate-action, and short-history rules.
- Assumed execution: portfolio-level rebalance at closes (granularity,
  lot-size, and fill conventions unspecified — part of the cost-field
  blocker).

## 9. Deterministic example (hand arithmetic illustration, NOT a test)

Inputs (illustrative 2-asset case): Σ = [[0.04, 0.01],[0.01, 0.09]],
σ = [0.20, 0.30].
- det(Σ) = 0.04×0.09 − 0.01×0.01 = 0.0035.
- Σ⁻¹ = (1/0.0035)[[0.09, −0.01],[−0.01, 0.04]].
- Σ⁻¹σ = [4.28571, 2.85714]; sum = 7.14286 → w = [0.60, 0.40].
- wᵀσ = 0.24; wᵀΣw = 0.0336; DR(w) = 0.24/√0.0336 = 1.30931.
- Check: equal-weight DR = 1.29099 < 1.30931, consistent with maximization.
No code was run; no test was executed. This example is acceptance material
for a future implementation review.

**Acceptance criteria for later implementation (unexecuted):** (a) closed-form
weights reproduce §9 values to 1e-9; (b) DR(w*) ≥ DR(1/N) on any admissible
input; (c) weights sum to 1; (d) long-only variant respects w ≥ 0;
(e) singular/non-PD Σ produces a defined failure (raise, no silent
fallback); (f) any BLOCKER field still open fails the freeze review.

## 10. Ambiguities, prohibited assumptions

BLOCKERS B1–B6 as above. Prohibited: inventing windows/cadence/universe/
variant/conventions; selecting a data substrate; treating Task51's
compatibility notes as authorizations; treating DISTINCT as profitable,
admitted, or validated; reusing existing market-data files (unauthorized).

## 11. Required future evidence, validation stages, stop criteria

- Owner §99.1 ruling on EXT-062 (outstanding — see task report §4).
- Blocker resolution exclusively by further source access, never invention
  (Task51 §16 rule).
- Frozen universe + data-scope decision (new acquisition and/or named-file
  reuse authorization) before any implementation decision.
- Implementation, then a separately authorized bounded evaluation with
  frozen prototype-count/complexity budgets (§3B) — none authorized here.
- Stop criteria: negative §99.1 ruling → close; any blocker unresolvable
  from sources → close with record; budget exhausted → stop for new decision.
