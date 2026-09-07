# QUANTFORGE — XAUUSD LIQUIDITY SWEEP / SESSION REVERSAL
# SCIENTIFIC DEFINITION SCREENING V1

## 1. Executive Verdict
**LEVEL 2 — SCIENTIFICALLY DEFINABLE AND READY FOR PRE-REGISTRATION**
The candidate relies entirely on objective market-structure geometry (price and time boundaries). It can be perfectly quantified without subjective chart-reading or ML, making it ready to be drafted into a deterministic event-study protocol.

## 2. Candidate Concept
The candidate tests the core SMC (Smart Money Concepts) / ICT behavioral premise: **London/NY Session Sweep and Reversal on XAUUSD**.
Specifically, the hypothesis posits that when price breaches a major structural liquidity level established in a prior session, fails to sustain the breakout, and sharply rejects, it initiates a high-probability, high-magnitude reversal excursion.

## 3. Existing Closed Lines
This candidate is structurally distinct from all closed lines:
- **Mean Reversion (DISC-021)** tested arbitrary, unanchored rolling z-score displacement. This candidate tests fixed, timezone-anchored structural levels.
- **Session Range Expansion (DISC-024)** tested whether a compressed state predicts future magnitude expansion. This candidate tests whether a specific localized geometric event (a sweep/false-break) predicts *directional* reversal.
- **TSMOM (DISC-022)** and **H01** are macro-trend and volatility-response hypotheses, wholly unrelated to intraday microstructure liquidity sweeps.

## 4. Session Structure
To avoid broker-time shifts and daylight saving errors, we anchor to standard Exchange/New York time (`America/New_York`), already utilized reliably in QuantForge.
- **Asian Session (Consolidation)**: `18:00:00 ET` (prior day open) to `02:59:00 ET`.
- **London Session (Overlap/Expansion)**: `03:00:00 ET` to `07:59:00 ET`.
- **New York Session (Primary Volume)**: `08:00:00 ET` to `17:00:00 ET`.

## 5. Reference Liquidity Level
**Asian Session High and Low**.
*Market-mechanics justification*: The Asian session in XAUUSD is historically a low-volume consolidation phase that builds distinct upper and lower boundaries. When London and NY participants enter the market with institutional volume, they require liquidity to execute block orders. The stops residing just above the Asian High and below the Asian Low provide this liquidity. This makes the Asian extremes the most mechanically defensible target for a stop-run.

## 6. Sweep Definition
A sweep occurs when an M1 candle's **High** is strictly greater than the Asian Session High, or its **Low** is strictly less than the Asian Session Low, during the London or NY session windows. 
- *Minimum excursion*: $> 0$ ticks. Any strict penetration of the exact price extreme qualifies. Arbitrary tick-size minimums or ATR multiples introduce optimization risk and are excluded.

## 7. Rejection Definition
A rejection occurs when the M1 candle that penetrated the reference level **fails to close beyond it**.
- *Upper Sweep*: M1 High > Asian High, BUT M1 Close $\le$ Asian High. (A wick penetration).
- *Lower Sweep*: M1 Low < Asian Low, BUT M1 Close $\ge$ Asian Low.

## 8. Reversal Confirmation
To prevent subjective "market structure shift" drawing, the reversal confirmation must be instant and deterministic. 
- **Definition**: A structural break of the sweep candle itself. 
- If an upper sweep occurs, the reversal is confirmed the moment a subsequent M1 candle closes **below the Low of the specific M1 sweep candle**. 
- This represents the smallest, most objective fractal confirmation that buyers have been trapped and momentum has shifted.

## 9. Primary Behavioral Hypothesis
> When the Asian Session extreme is swept during the London or NY session and immediately rejected (leaving a wick), followed by a micro-structural confirmation close in the opposite direction, the subsequent directional price excursion away from the swept level is statistically larger than the excursion following a standard non-sweep/breakout continuation.

## 10. Primary Response
**Maximum Favorable Excursion (MFE) within a fixed 120-minute horizon**.
*Justification*: MFE measures the absolute magnitude of the move made available by the behavior. A fixed horizon prevents unbounded lookaheads. If the sweep initiates a true reversal, the 2-hour MFE should be significantly larger (and more directional) than random entry or standard breakout continuation.

## 11. Data Feasibility
- `XAUUSD_M1.csv` is locally available (~104MB). 
- It contains deep historical OHLC timestamps.
- M1 data perfectly supports exact Asian session extrema calculation, intrabar wick penetration (High/Low vs Close), and subsequent M1 close confirmation.
- Bid/Ask spreads can be reliably modeled via standard institutional XAUUSD assumptions (e.g., ~15-30 cents) during economic viability testing.

## 12. Economic / Trading Path
This candidate possesses a highly credible path to live execution:
- **Behavior**: M1 data mathematically detects the sweep, rejection, and confirmation.
- **Entry**: Market order immediately on the confirming M1 close.
- **Risk Management**: Static stop-loss placed 1 tick beyond the wick extreme of the sweep candle.
- **Target**: The opposite Asian session extreme, or a trailing mechanism.
- **Cost Model**: XAUUSD volatility routinely produces $5 to $15 intraday swings, easily dwarfing standard $0.15-$0.30 spreads. 
- **Validation**: If statistically supported, translated directly to a lightweight MT5 EA for demo forward-testing of fill quality.

## 13. SMC Quantification Rules
**Allowed (Deterministic)**
- Time-bound session highs/lows.
- Mathematical level crossing (High/Low vs Level).
- Wick definition (Close vs Level).
- Micro-structural break (Close vs Sweep Candle Low/High).

**Not Allowed (Subjective)**
- Drawing order blocks based on "momentum".
- Discretionary trendline liquidity.
- Subjectively identifying "smart money accumulation".
- Imbalance/FVG visual interpretations without strict numerical boundaries.

## 14. Complexity Assessment
Complexity is extraordinarily low. The logic requires only:
1. Max/Min of a fixed time window.
2. A simple `<` or `>` logical check on the M1 High/Low.
3. A subsequent `<` or `>` check on the M1 Close.
No indicators, moving averages, rolling distributions, or complex parameters are required. 

## 15. ML Position
Machine Learning (including K-means or HMM) is strictly prohibited at this stage. The hypothesis relies on a deterministic structural mechanism. ML is not required to define a high or a low. If the simple behavioral baseline proves robust, ML could theoretically be used in the future to classify macro-regimes where sweeps are more effective, but it will not be used to define the sweep itself.

## 16. Falsification
The candidate will be scientifically falsified if:
- The median MFE following a confirmed sweep/reversal is statistically indistinguishable from zero or the baseline control distribution.
- Price reliably continues in the direction of the sweep (falsifying the "trap/reversal" mechanism and proving it was merely a strong breakout).

## 17. Definition-Level Readiness
**LEVEL 2**. The concept is completely untangled from subjective chart-reading and reduced to pure price/time geometry. It is ready for strict pre-registration.

## 18. Exact Next Legitimate Task
The exact next legitimate task is drafting the **Outcome-Blind Pre-Registration Protocol (Event Study V1)** for the XAUUSD Liquidity Sweep / Session Reversal candidate.

## 19. Prohibited Follow-Up
- Do NOT build an exploratory backtest to check if the Asian session is the "best" session.
- Do NOT test ATR multiples to filter the sweep.
- Do NOT evaluate historical PnL.
- Do NOT execute the study until an independent audit passes the protocol.

## 20. Integrity
No code was written. No data was processed. No historical outcomes were analyzed to arrive at these definitions. The candidate was scientifically specified using deductive market-structure reasoning.
