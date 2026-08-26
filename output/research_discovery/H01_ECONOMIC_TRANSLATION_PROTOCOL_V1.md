# QUANTFORGE — H01 EQUITY TRACK A
# ECONOMIC TRANSLATION PROTOCOL V1

## 1. Purpose
The purpose of this protocol is to translate the scientifically supported H01 behavioral volatility-asymmetry finding into a formal, deterministic economic test. This protocol isolates the economic usefulness of the signal without relying on outcome-dependent tuning, strategy optimization, or arbitrary aggregation choices, preserving a strict firewall between behavioral science and economic viability.

## 2. Scientific Basis
H01 Equity V1.3.0 established scientific SUPPORT for classic volatility-response asymmetry across broad-US and US-tech equity exposures in both historical and contemporary evaluation windows. The scientific hypothesis successfully demonstrated that prior downside shocks (measured against an 11-day local block) significantly alter the subsequent one-day return distribution.

## 3. Economic Question
Does the H01-supported volatility-response asymmetry provide economically actionable predictive information after predefined execution costs, without relying on outcome-dependent tuning?

## 4. Economic Hypothesis
- **Null ($H_0$)**: The H01 behavioral signal does not produce economically meaningful incremental forward return after registered execution costs in both evaluated eras.
- **Alternative ($H_1$)**: The H01 behavioral signal produces a positive, statistically significant incremental forward return after registered execution costs in both historical and contemporary eras.
- **Significance Threshold**: $\alpha = 0.05$ (evaluated per era).

## 5. Economic Object and Position
The economic position is defined as:
- **ACTIVE Exposure**: Long (1.0 weight) in the underlying market.
- **INACTIVE Exposure**: Flat (0.0 weight) in the underlying market.
Market returns are measured as un-normalized logarithmic returns. Every market is independently held and evaluated simultaneously.

## 6. Signal Definition
The signal strictly inherits the behavioral object from H01 V1.3.0. 
- **ACTIVE**: The logarithmic return at $T-1$ falls within the lowest tercile ($Q1$) of the trailing $L=11$ block distribution.
- **INACTIVE**: All other evaluable states.
This definition uses zero post-registration free parameters.

## 7. Timing / Look-Ahead Control
The timing structure explicitly prevents look-ahead bias:
1. $T-1$ Close: Prior day's return is realized.
2. Signal computation: Evaluated against the $T-1$ trailing block.
3. Exposure transition: Entered or maintained at the $T-1$ Close.
4. $T$ Close: Realize the 1-day logarithmic forward return ($r_t$).

## 8. Market Universe
The evaluation universe strictly mirrors the H01 V1.3.0 registered families:
- **Historical Era**: sp, NYA, NASDAQ100, NASDAQCOM (1982-04-21 to 2002-10-01)
- **Contemporary Era**: SP500, DJIA, NASDAQ100, NASDAQCOM (2016-08-15 to 2026-08-14)
Data requirements strictly demand provenance matching the six H01 V1.3.0 source fingerprints. No market selection or exclusion is permitted.

## 9. Forward Outcome
The forward outcome is the daily logarithmic return from $T-1$ Close to $T$ Close ($r_t$).

## 10. Execution Cost Model
Costs are defined as PRE-REGISTERED ASSUMPTIONS because the protocol spans indices without uniform liquid futures.
The transition costs are applied exactly as follows:
- **INACTIVE → ACTIVE**: 1 bps entry cost deducted from $r_t$.
- **ACTIVE → INACTIVE**: 1 bps exit cost deducted from $r_t$.
- **ACTIVE → ACTIVE**: 0 bps additional cost.
- **INACTIVE → INACTIVE**: 0 bps additional cost.
This yields a **Base Case** assumption of 2 bps per round-trip trade.
A **Cost Stress** scenario of 5 bps round-trip (2.5 bps entry/exit) is also pre-registered.

## 11. Primary Economic Endpoint and Market Weighting
The primary economic endpoint is the Equal-Market-Weighted Daily Incremental Return, calculated independently for each era.
1. For each market $m$, calculate the daily incremental mean:
   $\Delta_m = \text{mean}(\text{after-cost } r_t \mid \text{ACTIVE}) - \text{mean}(\text{after-cost } r_t \mid \text{INACTIVE})$
2. Calculate the cross-market primary endpoint ($\Delta$) via equal weighting to prevent high-volatility or high-frequency markets from dominating:
   $\Delta = \frac{1}{M} \sum_{m=1}^{M} \Delta_m$
   *(where M is the number of primary-evaluable markets in the era).*

For presentation, the secondary annualized endpoint is defined strictly as: $\Delta_{\text{annual}} = \Delta \times 252$.

## 12. Statistical Method and Confidence Interval
To account for serial dependence, repeated observations, and cross-market correlation, the 95% Confidence Interval is constructed using a **market-clustered block bootstrap**:
- **Resampling Unit**: Market-specific daily return series.
- **Block Length**: $L=11$ (strictly inherited from the H01 dependence horizon).
- **Replicates**: $B=10,000$.
- **Seed**: `20260816` (inherited from H01 V1.3.0).
- **Procedure**: For each replicate, resample each market's daily sequence using independent blocks. Calculate each market's $\Delta_m$, equal-weight them into the pooled $\Delta$, and store. The 95% CI is the standard percentile interval of the 10,000 pooled estimates. Incomplete terminal blocks are truncated.

## 13. Historical / Contemporary Era Treatment
Eras are strictly separated for the primary gate to prevent masking regime decay.
- **Primary Gate**: The primary cross-market endpoint ($\Delta$) must be positive, and its 95% CI lower bound must be strictly $> 0$, in **BOTH** the Historical and Contemporary eras independently.
- **Secondary**: A pooled all-era result.

## 14. Parameter Freeze
There are **ZERO** post-registration free parameters. Lookbacks ($L=11$), quantiles ($Q1$), block lengths ($11$), weighting schemes (Equal), and cost assumptions (2 bps / 5 bps) are explicitly frozen prior to execution. No tuning is permitted.

## 15. Economic Success Criteria
**ECONOMIC SUPPORT** requires:
1. The lower bound of the 95% CI for the Primary Endpoint > 0 in the Historical Era.
2. The lower bound of the 95% CI for the Primary Endpoint > 0 in the Contemporary Era.
This must hold under the Base Case cost assumption (2 bps).

## 16. Economic Failure / Translation-Failure Criteria
- **ECONOMIC FAILURE**: The 95% CI lower bound $\le 0$ in either the Historical or Contemporary era under the Base Case cost assumption.
- **TRANSLATION FAILURE**: Data limitations or infrastructure failures prevent accurate calculation.

## 17. Robustness / Cost Stress
The protocol relies on three rigid scenarios evaluated against the primary endpoints:
1. Zero-cost baseline.
2. 2 bps round-trip Base Case assumption.
3. 5 bps round-trip Cost Stress assumption.
If the signal survives the Base Case but fails the Cost Stress, the economic conclusion must explicitly state the effect is highly sensitive to friction.

## 18. Multiple-Testing Control
Because the protocol relies on exactly ONE primary economic endpoint evaluated sequentially as a strict dual-era gate, no multiple-testing correction is required.

## 19. Reproducibility & Failure Handling
- **Provenance**: Cryptographic verification of the six H01 V1.3.0 source files.
- **Reproducibility**: Deterministic script yielding a single execution ID.
- **Failure**: Any infrastructure failure or mismatch blocks execution (non-adjudicable).

## 20. Scientific/Economic Firewall
H01 scientific SUPPORT is not itself economic evidence. A failed economic translation does NOT invalidate the scientific H01 result. Positive economic results do not retroactively change the H01 scientific classification.

## 21. Governance Sequence
Draft → independent protocol audit → owner approval → source/data preparation → source audit → frozen economic inputs → execution-readiness audit → single economic execution → independent adjudication.

## 22. Explicit Non-Authorization of Execution
This protocol draft **DOES NOT AUTHORIZE EXECUTION**. Economic execution remains explicitly blocked pending final owner authorization.
