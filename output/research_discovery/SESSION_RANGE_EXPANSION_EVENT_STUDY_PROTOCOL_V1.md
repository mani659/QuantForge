# QUANTFORGE — SESSION-ANCHORED RANGE EXPANSION EVENT-STUDY PROTOCOL

## Version History
- **v1.0.0**: Initial outcome-blind protocol.
- **v1.1.0**: Precision corrections (session timestamp boundaries, percentile linear interpolation, median convention, stationary bootstrap geometric mechanics, secondary directional clarity).
- **v1.1.1**: Bootstrap precision correction (explicit termination rule truncating each resampled sequence to exactly N observations).
- **v1.1.2**: Final deterministic wording corrections (stationary-bootstrap continuation probability, exact primary-response timestamp wording).
- **v1.1.3**: Final precision corrections for session completeness semantics, percentile position convention, zero-direction secondary handling, and chronological half-split convention.

## 1. Executive Verdict
**A — LEVEL 2 / READY FOR EXECUTION AUDIT**

This protocol translates the frozen definition lock into a complete, deterministic, and outcome-blind statistical event study. All methodological, inferential, and data-quality decisions have been pre-registered without any reference to historical profitability or data inspection. It is ready for an independent, read-only audit before data is touched.

## 2. Scientific Question
**GOVERNANCE DECISION:**
> Does a state of extreme pre-session range compression reliably precede a statistically significant increase in subsequent cash-session range expansion magnitude, compared to sessions that follow normal or expanded pre-session states?

This protocol tests a behavioral hypothesis concerning volatility state transitions, not a trading edge.

## 3. Market / Data Scope
**GOVERNANCE DECISION:**
- **Instrument:** `USATECHIDXUSD`
- **Timeframe:** M1 (1-minute)
- **Timezone:** `America/New_York` (ET)
- **Pre-session window:** 18:00:00 ET (prior day) through 09:29:00 ET (current day) inclusive.
- **Cash-session response:** 09:30:00 ET through 16:00:00 ET (current day) inclusive.
- **Timestamp Authority:** The internal UTC timestamp mapped strictly to ET using standard timezone conversion (accounting automatically for DST).

## 4. Session Construction
**GOVERNANCE DECISION:**
- **Pre-session Bounds:** 18:00:00 ET through 09:29:00 ET inclusive contains exactly **930** M1 timestamps.
- **Cash-session Bounds:** 09:30:00 ET through 16:00:00 ET inclusive contains exactly **391** M1 timestamps. There is zero overlap with the pre-session window.
- **Completeness:** The operational session-completeness gate is the minimum-coverage rule: a day passes the bar-count gate when at least 200 M1 observations exist in the 09:30:00–16:00:00 inclusive cash-session window. This is a minimum-coverage gate, NOT a requirement for gapless minute-by-minute continuity. Internal M1 gaps do not independently invalidate a day when the minimum coverage and terminal-close rules pass. The actual data-quality rules are exactly the protocol's stated gates; no hidden continuity test is required. A 13:00 ET early close produces 211 inclusive minute timestamps, so such a day is excluded because the mandatory 16:00 close is missing, not because it falls below the 200-bar minimum.

## 5. Pre-Session Range
**GOVERNANCE DECISION:**
- **Pre-session High:** Maximum M1 `high` price between 18:00:00 ET and 09:29:00 ET inclusive.
- **Pre-session Low:** Minimum M1 `low` price between 18:00:00 ET and 09:29:00 ET inclusive.
- **Raw Range ($R_{pre}$):** High - Low.

## 6. Normalization
**GOVERNANCE DECISION:**
- **Formula:** $Normalized\_R_{pre} = \frac{R_{pre}}{Close_{09:29:00}}$
- **Numerator:** $R_{pre}$ as defined above.
- **Denominator:** The `close` price of the final M1 bar of the pre-session window (09:29:00 ET).
- **Zero/Missing:** If the close price is $\leq 0$ or missing, the day is marked invalid and dropped from state calculation.

## 7. Compression State
**GOVERNANCE DECISION:**
- **Trailing Window:** The most recent 63 valid trading days, excluding the current day.
- **Threshold:** The 25th percentile of the trailing 63-day $Normalized\_R_{pre}$ distribution.
- **Interpolation Convention:** The rolling 25th percentile uses NumPy/PERCENTILE.INC (R type 7) linear interpolation, with zero-based equivalent position `h = q(N-1)` or one-based order-statistic position `1 + q(N-1)`. For $N = 63$ and $q = 0.25$, the position is 16.5 in one-based indexing. The threshold is the arithmetic interpolation halfway between the 16th and 17th ordered observations. This convention is binding and implementation-independent.
- **Classifier:** The current day is classified as **COMPRESSED** if its $Normalized\_R_{pre} \leq$ the trailing 25th percentile threshold.
- **Data Requirement:** The first 63 days of the dataset are consumed purely for initialization and cannot generate a testable event. If fewer than 63 valid history days exist, the day is dropped. Duplicate values are handled naturally by the linear interpolation.

## 8. Control Group
**GOVERNANCE DECISION:**
- **Control Group:** All valid trading days where the pre-session state is NOT compressed (i.e., $Normalized\_R_{pre} >$ the trailing 25th percentile threshold).
- **Rationale:** This is the most natural, structurally complete comparison group.

## 9. Primary Response
**GOVERNANCE DECISION:**
- **Metric:** Cash-Session Normalized Range ($Normalized\_R_{cash}$)
- **Formula:** $\frac{High_{cash} - Low_{cash}}{Close_{16:00:00}}$
- **Window:** **The cash-session high and low are computed from all M1 observations with timestamps from 09:30:00 ET through 16:00:00 ET inclusive.**
- **Zero/Missing:** If the `Close_{16:00:00}` price is $\leq 0$ or missing, the day is marked invalid and dropped from the primary response calculation.

## 10. Primary Statistic
**GOVERNANCE DECISION:**
- **Statistic:** Difference in Medians ($\Delta M$)
- **Formula:** $Median(Normalized\_R_{cash} \ | \ COMPRESSED) - Median(Normalized\_R_{cash} \ | \ CONTROL)$
- **Median Convention:** Arithmetic average of the two central ordered observations for an even-sized sample.
- **Rule:** The $\Delta M$ is calculated inside each bootstrap iteration. The group labels (COMPRESSED/CONTROL) are held fixed and remain attached to their respective days during resampling.

## 11. Secondary Directional Response
**GOVERNANCE DECISION:**
- **Diagnostic:** Directional Persistence Rate.
- **Direction:** Session direction is determined strictly by the sign of $(Close_{16:00:00} - Open_{09:30:00})$.
- **Persistence:** If the session is UP ($> 0$), persistence requires $Close_{16:00:00} \geq Low_{cash} + 0.75 \times Range_{cash}$. If DOWN ($< 0$), persistence requires $Close_{16:00:00} \leq High_{cash} - 0.75 \times Range_{cash}$.
- **Tie/Zero:** If $Close_{16:00:00} == Open_{09:30:00}$, the cash session is directionless. In this case, or if $Range_{cash} = 0$, the directional-persistence diagnostic is NaN and excluded from the secondary denominator.
- **Firewall:** This is purely a descriptive diagnostic. It cannot rescue a failed primary response, nor change the scientific verdict.

## 12. Dependence / Inference
**GOVERNANCE DECISION:**
- **Method:** Stationary Block Bootstrap (Politis & Romano, 1994).
- **Sampling Unit:** Resample the day-level aggregated observation tuples: `[Normalized_R_cash, State_Label]`, not raw M1 bars.
- **Block Generation:** Block lengths are drawn from a Geometric distribution with parameter $p = \frac{1}{L} = 0.1$ (expected block length $L=10$ days).
- **Selection Mechanics:** The stationary bootstrap mechanics are defined exactly as follows:
  1. At the start of each block, choose the block's starting observation uniformly from the valid chronological day sequence.
  2. After each sampled observation, with probability $p = 1/L = 0.1$, **TERMINATE** the current block and start a NEW block at a uniformly selected observation.
  3. With probability $1 - p = 0.9$, **CONTINUE** the current block at the next chronological observation.
  4. Continuation beyond the chronological end wraps circularly to the beginning.
- **Termination / Sequence Length:** For each bootstrap replicate, blocks are sampled and appended until the resampled sequence reaches or exceeds the original number $N$ of valid day-level observations. If the final appended block causes the sequence length to exceed $N$, truncate the resampled sequence to exactly $N$ observations. Every replicate therefore contains exactly $N$ day-level observations. $N$ is not recomputed inside a replicate, truncation occurs only at the end of the sampled sequence, no observation is imputed, no observation is dropped selectively prior to truncation, and the state label remains attached to each sampled day tuple.
- **Replicates ($B$):** 10,000.
- **Inference:** Two-sided 95% percentile confidence interval of the bootstrap $\Delta M$ distribution.
- **Seed:** 20260817.

## 13. Multiple Comparisons
**GOVERNANCE DECISION:**
- **Family:** Exactly ONE primary confirmatory test (Difference in Medians of $Normalized\_R_{cash}$). 
- **Control:** No multiple hypothesis correction is required because the confirmatory family size is 1.

## 14. Chronological Design
**GOVERNANCE DECISION:**
- **Primary Inference:** Full-sample (maximizing statistical power to detect the structural effect).
- **Chronological Split:** After chronological ordering of all primary-valid event days, the first `floor(N/2)` observations form the first descriptive half and the remaining observations form the second descriptive half (where $N$ is the number of primary-valid event days). No date-based midpoint is used. The halves are descriptive only, and neither half can alter the full-sample primary verdict.

## 15. Stability / Robustness
**GOVERNANCE DECISION:**
- **Check 1:** Chronological halves (defined above).
- **Rule:** These are descriptive checks only. No data will be deleted post-result based on these splits.

## 16. Data Quality Gates
**GOVERNANCE DECISION:**
- **Missing Data:** If the 09:29:00 ET close or 16:00:00 ET close is missing, the day is invalid.
- **Duplicate Timestamps:** First observation retained, duplicates dropped.
- **Invalid Prices:** Any price $\leq 0$ invalidates the day.
- **Session Completeness:** If fewer than 200 M1 bars exist in the 391-timestamp cash session window, the day is flagged as a potential half-day/holiday and explicitly dropped.

## 17. Falsification
**GOVERNANCE DECISION:**
- **SUPPORTED:** The 95% CI for the Difference in Medians ($\Delta M$) is strictly positive (lower bound $> 0$).
- **INCONCLUSIVE:** The 95% CI includes zero.
- **CONTRADICTED:** The 95% CI is strictly negative (upper bound $< 0$), indicating compression suppresses subsequent expansion.

## 18. Economic Firewall
**GOVERNANCE DECISION:**
- **Rule:** This protocol executes exactly ZERO PnL, expectancy, spread, slippage, or Sharpe ratio calculations. Economic viability is explicitly relegated to a future research phase.

## 19. K-Means Firewall
**GOVERNANCE DECISION:**
- **Rule:** K-means is NOT part of this experiment. The classifier is 100% deterministic (rolling percentile).

## 20. Strategy Translation Firewall
**GOVERNANCE DECISION:**
- **Rule:** No trading rules, entry triggers, stop-losses, or position sizing algorithms may be tested during this protocol execution.

## 21. Forward Monitoring
**GOVERNANCE DECISION:**
- **Concept:** If deployed, the system will track the daily state (COMPRESSED vs NORMAL) and record the realized expansion and directional persistence. 
- **Rule:** This data is for statistical monitoring of edge decay only. It authorizes no silent parameter adaptation.

## 22. Stopping Rules
**GOVERNANCE DECISION:**
- **Rule:** If the data-quality gates flag more than 10% of the total calendar days containing at least one M1 bar as invalid, execution must STOP and trigger an anomaly audit before inference is computed.

## 23. Frozen Parameter Table
| Parameter | Frozen Value |
| :--- | :--- |
| Instrument | `USATECHIDXUSD` |
| Timezone | `America/New_York` |
| Pre-session Window | 18:00:00 ET (prior) to 09:29:00 ET inclusive |
| Cash-session Window | 09:30:00 ET to 16:00:00 ET inclusive |
| Trailing Window | 63 valid trading days |
| Compression Threshold | 25th percentile (linear interpolation) |
| Primary Statistic | Difference in Medians ($\Delta M$, arithmetic mean for even samples) |
| Inference Method | Stationary Block Bootstrap (Geometric $p=0.1$, circular) |
| Block Length ($L$) | 10 days |
| Replicates ($B$) | 10,000 |
| Random Seed | 20260817 |
| Significance ($\alpha$) | 0.05 (Two-sided 95% CI) |

## 24. Outcome-Blind Self-Audit
**GOVERNANCE DECISION:**
- Zero historical effect values are present.
- Zero PnL or trade frequency has been calculated.
- No parameters (63, 25%, 09:30) were derived from optimizing results.
- No strategy rules are embedded.
- The protocol is fully deterministic.

## 25. Governance Decision
**A — LEVEL 2 / READY FOR EXECUTION AUDIT**

## 26. Exact Next Task
> **FINAL INDEPENDENT READ-ONLY RE-AUDIT OF THE CORRECTED SESSION RANGE EXPANSION PROTOCOL**

The corrected protocol must now be reviewed by an independent agent/operator. Upon passing the read-only re-audit, execution may be authorized.

## 27. Integrity
- No code was written or executed.
- No data was peeked at.
- All decisions strictly resolve ambiguities identified by the audit.
