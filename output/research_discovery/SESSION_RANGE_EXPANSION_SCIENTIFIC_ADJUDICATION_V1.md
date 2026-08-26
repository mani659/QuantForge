# QUANTFORGE — SESSION-ANCHORED RANGE EXPANSION
# SCIENTIFIC RESULTS ADJUDICATION V1

## 1. Executive Verdict
**CANDIDATE CONTRADICTED — CLOSE**

## 2. Result Integrity
The execution artifacts conclusively establish adherence to the frozen protocol:
- Protocol Version: v1.1.3
- Execution Architecture: Single-process/serial execution
- Bootstrap Configuration: B = 10,000, L = 10, p_terminate = 0.1, exact N truncation
- Random Seed: 20260817
- Data Quality: 85 invalid days out of 873 calendar days containing at least one M1 bar. The 9.74% invalid proportion successfully cleared the >10% stopping threshold.
- No PnL, expectancy, or secondary optimization logic was introduced to the primary statistic calculation.

## 3. Registered Hypothesis
The frozen registered hypothesis tested was:
> Does extreme pre-session range compression reliably precede a statistically significant increase in subsequent cash-session range expansion magnitude, compared to sessions that follow normal or expanded pre-session states?

## 4. Primary Result
Based on the exact registered methodology:
- **Observed Difference in Medians ($\Delta M$)**: `-0.004367`
- **Two-Sided 95% Percentile Confidence Interval**: `[-0.005533, -0.002754]`

The 95% Confidence Interval is strictly negative (upper bound $< 0$).

## 5. Scientific Interpretation
The registered behavioral hypothesis is formally and unequivocally **contradicted** in the tested `USATECHIDXUSD` sample under the frozen definition. 

### Established
- Extreme pre-session compression (defined as $\le$ the trailing 63-day 25th percentile) was associated with significantly **LOWER** subsequent normalized cash-session range than the uncompressed control group.
- The hypothesized positive state-transition behavior is falsified for this asset and timeframe under this classifier.

### Not Established
- That compression is a universally predictive low-volatility regime.
- That the inverse relationship (compression preceding further suppression) is economically exploitable or tradable after costs.
- That the result generalizes to other instruments, horizons, markets, or clustering methodologies.
- That the result justifies selectively swapping the state classifier.

## 6. Secondary Firewall
The secondary descriptive results support the integrity of the primary finding without altering it:
- The chronological half splits ($\Delta M_1$: -0.003675, $\Delta M_2$: -0.005193) are highly stable and both negative, demonstrating the contradiction is persistent across the time sample.
- Directional persistence metrics (~50.7% vs ~52.5%) are purely descriptive and offer no capacity to "rescue" the failed primary response magnitude.

## 7. Economic Firewall
A statistically significant behavioral result (positive or negative) is NOT a trading edge by itself. This study provides **behavioral evidence only**. There is absolutely no conclusion regarding expectancy, PnL, spread, slippage, risk/reward, or live profitability. Therefore, this finding must NOT be translated into a strategy.

## 8. Generalization Boundary
This conclusion applies strictly to:
- `USATECHIDXUSD` / M1 timeframe
- `America/New_York` timezone
- Pre-session: 18:00:00–09:29:00 inclusive
- Cash session: 09:30:00–16:00:00 inclusive
- Deterministic 63-day rolling linear percentile threshold ($q=0.25$)
- Close-normalized range response

No cross-market or universal generalizations are authorized by this data.

## 9. Hypothesis Disposition
**RECORD AND CLOSE**
The registered behavioral hypothesis has been contradicted, and no independent reason exists to continue this exact hypothesis. 

## 10. ML / K-Means Firewall
The negative outcome of this deterministic rolling-percentile classifier does not legitimize retrospective rescue via K-means or other Machine Learning clustering. It is impermissible to claim "K-means would probably work better" based on this result. While a different state-definition method could constitute an entirely separate future research question, no such research is initiated or authorized here. K-means remains a separate candidate methodology, not a rescue mechanism for a failed study.

## 11. QuantForge End-Goal Relevance
The actual QuantForge objective is to discover a defensible trading edge capable of surviving economic friction over months of forward observation. This candidate failed the fundamental behavioral hurdle. A contradicted hypothesis must not be forced into strategy translation. 

The correct research outcome has been achieved: **Candidate rejected; proceed to another independently screened behavioral edge.**

## 12. Research-Line Governance Decision
**CLOSED**

## 13. Exact Next Legitimate Task
Update the central **governance record** and then return to the broader **Tradeable Edge Discovery** process to screen the next independent behavioral candidate.

## 14. Prohibited Follow-Up
- Do NOT invert the hypothesis (e.g., trying to trade the suppression) based on this outcome.
- Do NOT test another percentile threshold (e.g., 10% or 15%).
- Do NOT rerun with an ML classifier to reverse the verdict.
- Do NOT change the lookback window or normalization method.

## 15. Integrity
No code was executed. No reruns occurred. No secondary parameters were modified. This adjudication rests solely upon the mathematically frozen outputs of the single pre-registered script run.
