# QUANTFORGE — TRADEABLE EDGE DISCOVERY & REGIME/STATE SCREENING V1

## 1. Executive Verdict
**B — PROMISING BUT NOT YET DEFINABLE**

The project has successfully pivoted from abstract anomaly hunting to the rigorous search for an economically viable, deployable trading edge. Existing research lines (Mean Reversion, 12/1 TSMOM) have been properly closed after failing economic or cross-era stability gates. By auditing the repository's existing high-resolution M1 and tick data, we have identified **Session-Anchored Intraday Range Expansion (Volatility Breakout)** on the US Tech Index (USATECHIDXUSD) as the highest-priority behavioral candidate. However, before it enters the formal definition-lock phase, it requires a dedicated scoping step to explicitly define the state variable (range compression) and the proposed execution horizon.

## 2. Current QuantForge Research Position
**SOURCE-DERIVED FACT:**
- **QuantForge Engine:** Core execution, temporal, and strategy assembly boundaries are COMPLETE and FROZEN (AMEND-1 ratified).
- **Mean Reversion:** CLOSED (DISC-021). The extreme-displacement hypothesis was statistically observable but economically non-viable under observed tick-level bid/ask spreads.
- **12/1 TSMOM:** CLOSED (DISC-022). Failed to demonstrate a stable incremental edge above unconditional drift across historical and contemporary eras.
- **H01 Equity (Track A):** OPEN. A pure scientific finding (classic volatility-response asymmetry established in US-tech). It is not a trading strategy, and no BOE runtime semantics have been created.
- **Detector Implementation:** DESIGN BLOCKED. The system requires a scientifically validated behavioral hypothesis before a runtime detector can be built.

## 3. Ultimate Trading Objective
**GOVERNANCE DECISION:**
The objective is to discover a **defensible, economically viable trading edge**. This means identifying a simple, robust market behavior with a credible economic rationale that survives realistic transaction costs, remains stable across market regimes, and can be continuously monitored (statistically) in live forward observation. We are explicitly separating Layer A (Market Behavior) from Layer B (Tradeability) and Layer C (Strategy).

## 4. Existing Data / Infrastructure Capability
**SOURCE-DERIVED FACT:**
- **Data Availability:** M1 (1-minute) historical data is available for `USATECHIDXUSD`, `EURUSD`, `XAUUSD`, `BTCUSD`, and `XAGUSD`. Tick-level data with observed spreads is available for `XAGUSD`. A 28-market historical daily panel exists for 1987–2002.
- **Infrastructure:** The `boe/execution`, `research/lifecycle`, and `boe/observation` machinery are fully built and frozen.
- **Cost Data:** We possess the capability to model exact MT5 execution costs (as demonstrated in the XAGUSD cost-viability study).

## 5. Closed Research Lines
**GOVERNANCE DECISION:**
- **Mean Reversion (DISC-021):** Will NOT be reopened by adding regime filters, volatility filters, or ML clustering. The fundamental cost barrier remains.
- **12/1 TSMOM (DISC-022):** Will NOT be reopened through alternative ML classification, trend-state filtering, or parameter tuning.

## 6. Candidate Behavioral Hypotheses
**MODEL INFERENCE:**
Using existing M1 data, the following broad behaviors are testable:
1. **Intraday Volatility Breakout (Range Expansion):** Unidirectional session persistence following a tight pre-session consolidation.
2. **Session-Transition Mean Reversion:** Liquidity-driven reversals at the London/NY overlap. (High risk of failing the spread-cost gate).
3. **Volatility Clustering Directional Bias:** Asymmetric forward drift conditioned on the prior day's ATR state (borrowing insight from H01, but mapped to intraday holds).
4. **Intraday Momentum Reversal After Extreme Moves:** Exhaustion fading. (Similar to the closed MR line, likely to fail economic gates).

## 7. Candidate Scoring Matrix
**MODEL INFERENCE:**

| Candidate | A. Economic Rationale | B. Measurement Clarity | C. Data Exists | E. Independence | G. Cost Survivable | H. Temporal Robustness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Session Range Expansion** | High (Institutional flow) | High | Yes (M1) | Yes | High (1 trade/day, large move) | High |
| **2. Session Transition MR** | Medium (Liquidity gaps) | Medium | Yes (M1) | Yes | Low (Spread sensitive) | Medium |
| **3. Volatility Directional Bias** | High (Risk premia) | High | Yes (M1) | No (Overlaps H01) | Medium | High |
| **4. Exhaustion Fading** | Medium (Panic/Reflux) | High | Yes (M1) | No (Overlaps MR) | Low (Spread sensitive) | Medium |

## 8. Regime / State Research Opportunities
**MODEL INFERENCE:**
The probability of a successful intraday breakout is heavily dependent on the market's pre-existing state.
- **State Variable:** *Pre-Session Range Compression*. 
- **Rationale:** Breakouts from wide, highly volatile ranges tend to fail (whipsaw). Breakouts from tight, compressed ranges tend to trend as accumulated order flow is violently resolved.
- **Independence:** This state variable explains the *condition* under which the behavior occurs, rather than being selected blindly to maximize backtest PnL.

## 9. K-Means / ML Position
**GOVERNANCE DECISION:**
K-Means and other clustering algorithms are **METHODS**, not hypotheses. We will not "run K-means to find profitable clusters."
However, K-means is a valid method to objectively classify our proposed state variable (*Pre-Session Range Compression*) into two distinct regimes (e.g., "Compressed" vs "Expanded") using 1D clustering. This removes human subjectivity from setting arbitrary threshold parameters (e.g., "range < 50 pips"). 

## 10. Highest-Priority Candidate
**GOVERNANCE DECISION:**
**Session-Anchored Intraday Range Expansion on USATECHIDXUSD.**
*Hypothesis:* Intraday directional persistence (momentum) in the US Tech index is significantly stronger and more likely to follow through to the end of the US cash session when the breakout originates from a state of measurable pre-session range compression (low volatility).

## 11. Why It Is Independent
**MODEL INFERENCE:**
- Distinct from 12/1 TSMOM: It operates on an intraday horizon (M1 data) rather than monthly data, exploiting microstructure/session flow rather than macro-economic trends.
- Distinct from Mean Reversion: It trades *with* the breakout momentum (trend continuation), not against panic displacement.
- Distinct from H01: It seeks a tradeable session edge based on range expansion, rather than measuring multi-day inter-close volatility asymmetry.

## 12. Why Current Data Can Test It
**SOURCE-DERIVED FACT:**
QuantForge currently possesses the `USATECHIDXUSD_M1.csv` dataset. M1 resolution is perfectly suited to construct precise pre-session (e.g., Asian/European hours) high/low ranges and evaluate exact US cash-session breakout prices and closing exits.

## 13. What Would Falsify It
**MODEL INFERENCE:**
The hypothesis is falsified if:
1. The post-breakout drift to the session close is zero or random.
2. The gross effect exists but is entirely consumed by the median bid/ask spread (failing the economic gate like MR).
3. The behavior only exists in one specific chronological year and fails in walk-forward.

## 14. Eventual Strategy Translation
**MODEL INFERENCE:**
If the behavioral layer (Layer A) survives, translation to a strategy (Layer C) is highly feasible. The entry is a simple stop-order at the pre-session boundary. The exit is a time-based exit at the session close. This creates a highly favorable cost profile: one entry, one exit, capturing a macro intraday move, paying the spread only once, and holding zero overnight gap risk.

## 15. Future Forward / Demo / Live Monitoring
**MODEL INFERENCE:**
This candidate is perfectly suited for sequential forward monitoring. QuantForge can easily track:
- Daily state classification (Compressed vs Expanded).
- Breakout trigger rate.
- Gross excursion (MAE/MFE) within the session.
- Realized spread and slippage on the breakout trigger.
- Hit rate and expectancy over rolling 30-day windows.

## 16. Prohibited Follow-Up
- Writing a backtest or EA for this candidate immediately.
- Optimizing session start/end times to maximize historical PnL.
- Adding arbitrary moving averages or RSI filters to "improve" the win rate.

## 17. Exact Next Legitimate Task
> **SCOPING AND DEFINITION LOCK FOR SESSION RANGE EXPANSION**

Before testing, a formal protocol must be written to define exactly how the pre-session range is measured, how K-means will be rigidly applied to classify the state, and how the intraday holding period is strictly bounded.

## 18. Integrity
- No code was written.
- No backtests or K-means clustering were executed.
- No historical PnL optimization occurred.
- The selection relied strictly on existing repository data and economic rationale.
- The closed TSMOM and Mean Reversion lines were completely respected and not revived.
