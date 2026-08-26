# QUANTFORGE — CROSS-MARKET LIQUIDITY SWEEP / REVERSAL
# EVENT-STUDY PRE-REGISTRATION V1.2.0

## 0. Version History
- **v1.0.0**: Initial outcome-blind protocol.
- **v1.1.0**: Precision clarification applied after independent audit V1. Exactly three deterministic corrections applied:
  1. Control-event absence window explicit through 17:00:00 ET; MFE anchor explicit at rejection candle close.
  2. Bootstrap mapping explicitly defined as flattening all events contained within resampled day-clusters into 1D median arrays per replicate.
  3. P-value construction explicitly formulated as a null-imposing recentered distribution testing $H_0: \Delta M = 0$.
- **v1.2.0**: Precision amendment applied after the final independent clearance audit (CONDITIONAL PASS). Exactly five deterministic clarifications applied; no scientific object changed:
  1. Exact stationary-bootstrap mechanics registered (termination probability p = 0.1 / continuation probability 0.9, uniform block starts, circular wrapping, fixed replicate length N with final truncation).
  2. MFE horizon semantics registered: literal wall-clock 120-minute window continuing across the 17:00:00 ET boundary into 24/5 data; complete-horizon eligibility rule; no partial or truncated windows.
  3. Sweep-candle confirmation reference resolved: the first qualifying sweep-and-rejection candle opens the pending state and its opposite extreme is frozen; later sweep candles do not reset it.
  4. Data-quality / stopping gates made fully explicit (duplicates, invalid prices, missing bars, required session coverage, invalid-day denominator, gate timing, three-way day/event distinction).
  5. Market-level classification rule and median convention registered (SUPPORT / CONTRADICTED / INCONCLUSIVE mapping; even-n median = arithmetic mean of the two central ordered observations).


## 1. Scientific Question
Does a deterministic sweep of a prior Asian-session extreme, followed by rejection and micro-structural reversal confirmation, produce a statistically larger subsequent directional price excursion than the pre-registered control events?

## 2. Discovery vs Validation Scope
**Discovery Instrument**: `XAUUSD` (Where the structural candidate originated).
**Validation Scope**: The protocol strictly prohibits isolated single-market hacking. The candidate represents a fundamental behavioral claim about auction mechanics. Therefore, the hypothesis must be subjected to a multi-market validation universe to determine whether the behavior is asset-specific, asset-class-specific, or broadly robust across independent auction mechanisms.

## 3. Market Universe
The eligible universe is defined from locally available high-quality M1 data:
- `XAUUSD`
- `XAGUSD`
- `EURUSD`
- `USATECHIDXUSD`
- `BTCUSD`

Eligibility is determined strictly by data availability, timestamp integrity, and sufficient minimum event count, not historical performance. Markets lacking sufficient M1 depth or event frequency will be explicitly tagged as EVIDENCE-LIMITED.

## 4. Session Definitions
All timezone logic strictly utilizes `America/New_York` to deterministically handle Exchange time and DST transitions.
- **Asian Session (Reference Formation)**: `18:00:00 ET` (prior day) to `02:59:00 ET` inclusive.
- **London Session (Overlap/Expansion)**: `03:00:00 ET` to `07:59:00 ET` inclusive.
- **New York Session (Primary Volume)**: `08:00:00 ET` to `17:00:00 ET` inclusive.

## 5. Asian Reference Level
Calculated exclusively from the Asian session boundary. Fixed before any London/NY data is evaluated.
- **Asian High**: `max(high)` of M1 bars within the Asian session.
- **Asian Low**: `min(low)` of M1 bars within the Asian session.

## 6. Sweep Definition
Evaluated only during the London or NY session windows:
- **Upper Sweep**: `High_t > AsianHigh` (strict inequality).
- **Lower Sweep**: `Low_t < AsianLow` (strict inequality).
*No arbitrary minimum excursion, tick threshold, or ATR filter is applied.*

## 7. Rejection Definition
A structural wick-rejection requires the breaching M1 candle to fail to hold the breakout:
- **Upper Sweep Rejection**: `High_t > AsianHigh` AND `Close_t <= AsianHigh`.
- **Lower Sweep Rejection**: `Low_t < AsianLow` AND `Close_t >= AsianLow`.

## 8. Reversal Confirmation
Deterministic micro-structure confirmation (MSS/BOS surrogate):
- **Upper Sweep Confirmation**: Occurs at the exact first subsequent M1 candle that achieves `Close < Low_of_sweep_candle`.
- **Lower Sweep Confirmation**: Occurs at the exact first subsequent M1 candle that achieves `Close > High_of_sweep_candle`.

**Sweep-Candle Reference (frozen)**: The first qualifying sweep-and-rejection candle for a directional event opens that event's pending confirmation state. Its opposite candle extreme is frozen as the confirmation reference:
- Upper sweep: freeze that first candle's `Low`; confirmation requires the first later close strictly below that frozen `Low`.
- Lower sweep: freeze that first candle's `High`; confirmation requires the first later close strictly above that frozen `High`.
Later sweep candles do NOT reset or replace the pending event's confirmation reference.

## 9. Event Uniqueness
To prevent overlapping dependency leakage within the same trading session:
- Only the **first** confirmed upper sweep and the **first** confirmed lower sweep per market, per calendar trading day, are retained.
- If both occur on the same day, they are retained as separate directional events but must be processed within the same daily resampling block to preserve dependence.

## 10. Primary Response
Maximum Favorable Excursion (MFE) measured over a strictly fixed forward horizon of **120 minutes** after reversal confirmation.
- **Upper Reversal MFE**: `SweepLevel - minimum(low)` over the next 120 minutes.
- **Lower Reversal MFE**: `maximum(high) - SweepLevel` over the next 120 minutes.
*Note: The reference price for MFE is exactly the swept Asian level, anchoring the measurement structurally rather than to optimized entry points.*

**MFE Horizon Semantics (frozen)**: The 120-minute forward MFE window is a literal wall-clock interval beginning at the event anchor timestamp and may continue across the 17:00:00 ET NY-session boundary into subsequent 24/5 market data. No truncation of the MFE horizon at session boundaries; no imputation; no partial-window MFE. An event is eligible for primary inference only if a complete 120-minute MFE observation window is available; events occurring too close to the end of available data, such that the full 120-minute horizon cannot be evaluated, are excluded before primary inference. This rule applies identically to treatment and control events, using their respective registered anchor timestamps.

## 11. Control Group
**Rejected-Sweep Counterparts**.
The control group isolates the predictive value of the micro-structural confirmation against failed breakout attempts. It is defined deterministically as:
- **Control Event**: An eligible rejected sweep that has no qualifying reversal confirmation from the end of the sweep-rejection candle through `17:00:00 ET`.
- **Control MFE Anchor**: The timestamp of the close of the rejection/sweep candle.
- **Control MFE Horizon**: The next 120 minutes after that anchor.

The MFE horizon semantics of §10 (literal wall-clock 120-minute window, complete-horizon eligibility, no partial or truncated windows) apply identically to control events, anchored at the control MFE anchor defined above.

## 12. Primary Statistic
**Difference in medians of event-level MFE ($\Delta M$)**.
$\Delta M_{market} = \text{Median(MFE)}_{confirmed\_sweep} - \text{Median(MFE)}_{control}$

- **Sign Convention**: $\Delta M > 0$ strictly means that confirmed sweep/reversals produce larger directional excursions than the unconfirmed control group.

**Median Convention (frozen)**: For even sample sizes, the median is the arithmetic mean of the two central ordered observations; for odd sample sizes it is the middle ordered observation. This convention is applied identically to the observed statistic and to every bootstrap replicate statistic.

## 13. Market-Level Inference
Within each market, events are highly time-dependent. We utilize a **Stationary Block Bootstrap** to preserve intra-day and serial dependence structures.
- **B**: 10,000 iterations.
- **Block Expected Length (L)**: 10 days.
- **Seed**: 20260817.
- **CI**: Two-sided 95% Percentile Confidence Interval.

**Observed Statistic**: The primary observed statistic $\Delta M_{obs}$ is calculated from the complete original event set using the same treatment/control aggregation rule below, before bootstrap resampling.

**Day-Level to Event-Level Bootstrap Mapping**:
1. Each eligible event retains its market, trading-day identifier, direction, event type, anchor timestamp, and MFE.
2. All eligible events on the same trading day are stored together as one day-level cluster.
3. Bootstrap resampling occurs at the day-cluster level.
4. When a day cluster is selected multiple times in a replicate, ALL of that day's events are copied each time in their entirety. No event is independently resampled, duplicated, or dropped except as a direct consequence of day-cluster resampling.
5. After the bootstrap day sequence is formed, treatment events are flattened into one treatment event array and control events into one control event array.
6. The replicate statistic is: $\Delta M^* = \text{Median(MFE}^*_{treatment}) - \text{Median(MFE}^*_{control})$.
7. A replicate must contain at least one finite treatment and one finite control MFE; otherwise the replicate is marked invalid according to the protocol's deterministic missing-replicate rule.

**Stationary Bootstrap Mechanics (frozen)**:
- Sampling unit: the chronological sequence of trading-day clusters (days containing at least one eligible event).
- The number of day clusters in the original eligible sequence, $N$, is fixed once before bootstrap resampling and is identical for every replicate; it is never recomputed inside a replicate.
- For each replicate:
  1. Choose the first block start index uniformly over the $N$ day-cluster positions.
  2. Emit the day cluster at the current position, with its full event array attached.
  3. Draw a block-termination decision: with termination probability $p = 0.1$ end the current block; with continuation probability $0.9$ continue the block. Block lengths are therefore geometric with expected length $1/p = 10 = L$.
  4. On termination, choose the next block start index uniformly over the $N$ positions.
  5. On continuation, advance chronologically by one day-cluster position; if the end of the sequence is reached, wrap circularly to the beginning.
  6. Continue emitting day clusters until the sequence length reaches or exceeds $N$, then truncate the final block to exactly $N$ day clusters.
- Each sampled day carries its full event array; a day selected multiple times contributes its events once per selection (all events duplicated in their entirety). No event is independently resampled.
- The replicate statistic is then computed from the flattened treatment and control arrays as defined in steps 5–7 above.

## 14. Cross-Market Inference
Each market is processed as an independent scientific unit. The outcome must definitively report:
- **XAUUSD**: [Support / Contradicted / Inconclusive]
- **XAGUSD**: [Support / Contradicted / Inconclusive]
- **EURUSD**: [Support / Contradicted / Inconclusive]
- **USATECHIDXUSD**: [Support / Contradicted / Inconclusive]
- **BTCUSD**: [Support / Contradicted / Inconclusive]

**Market-Level Classification (frozen)**: For each evaluable market (at least 100 eligible confirmed treatment events, per §17):
- **SUPPORT**: Holm-adjusted p-value $< 0.05$ AND observed $\Delta M_{obs} > 0$.
- **CONTRADICTED**: Holm-adjusted p-value $< 0.05$ AND observed $\Delta M_{obs} < 0$.
- **INCONCLUSIVE**: otherwise.
A market with fewer than 100 eligible confirmed treatment events is tagged EVIDENCE-LIMITED and receives no primary classification. No equivalence margin is used. The cross-market research interpretation (asset-specific / asset-class-specific / cross-market / universal) is a report-stage matter and remains separate from the per-market classification.

## 15. Dependence / Bootstrap
The bootstrap resamples daily units. If a single day contains both an upper sweep and a lower sweep event, they move together in the resampled block. This explicitly controls for daily volatility clustering and ensures high-frequency event days do not silently inflate statistical significance. The exact stationary-bootstrap mechanics (termination probability $p = 0.1$, continuation probability $0.9$, uniform block starts, circular wrapping, fixed replicate length $N$ with final truncation) are registered in §13.

## 16. Inference and Multiple Comparisons
**Null-Inference and P-Value Definition**:
The protocol tests the null hypothesis $H_0: \Delta M = 0$. Because the difference in medians is location-equivariant, we use a null-imposing recentered bootstrap construction.
- **Null Distribution**: $\Delta M_{null}^* = \Delta M^* - \Delta M_{obs}$
- **Exact P-Value Formula**: $p = \frac{1 + \sum_{b=1}^{B_{valid}} I(|\Delta M_{null}^{*b}| \ge |\Delta M_{obs}|)}{1 + B_{valid}}$
where $I$ is the inclusive indicator function, and $B_{valid}$ is the count of finite valid replicates.

**Multiple Comparisons**:
The statistical family is defined as the set of eligible validation markets. We pre-register the **Holm-Bonferroni step-down procedure** over the exact market-level p-values at a family-wise $\alpha = 0.05$. A positive finding on XAUUSD cannot be claimed as statistically robust unless it clears the Holm-corrected threshold.

## 17. Data Gates
Execution MUST STOP if quality gates are breached:
- Missing terminal data or corrupted timestamps.
- Invalid prices ($\le 0$): any required OHLC value $\le 0$ invalidates the affected observation/bar.

**Deterministic Data Handling (frozen)**:
- **Duplicate timestamps**: sort chronologically and retain the FIRST observation for each duplicate timestamp; construct sessions and events only after this deduplication.
- **Invalid prices**: any required OHLC value $\le 0$ is invalid.
- **Missing bars**: missing M1 timestamps inside a session are NOT automatically fatal unless they cause another explicit gate to fail. The protocol requires sufficient session observations, valid required terminal/reference data, and deterministic event construction; no hidden gapless-session requirement is implied.
- **Required session coverage**: a session/day lacking the minimum required data for its role is ineligible:
  - *Asian reference formation*: the Asian session must contain at least one valid bar, otherwise no Asian High/Low can be formed and the day cannot participate in event construction;
  - *London/NY event detection*: the London/NY windows must contain at least one valid bar for sweep evaluation;
  - *120-minute post-event MFE*: the full 120-minute MFE window must be available per §10, otherwise the event is excluded before primary inference.

**Minimum Event Count**: A market must generate at least $N \ge 100$ confirmed events over the dataset to be evaluable. If $N < 100$, it is tagged EVIDENCE-LIMITED and dropped from primary inference (no primary classification per §14).

**Invalid-Day Fraction**: The denominator is all calendar trading dates containing at least one M1 observation for the instrument after timestamp normalization and duplicate removal. Weekends are not counted as invalid days merely because the market has no data. The invalid-day fraction is evaluated BEFORE primary inference. If the invalid-day fraction exceeds 10%, execution halts for an anomaly audit.

**Three-way distinction (not to be conflated)**:
- *invalid day* — fails the required-session-coverage gate above;
- *eligible day with zero qualifying events* — a valid day on which no sweep/rejection event is generated;
- *event with incomplete MFE horizon* — an event whose full 120-minute MFE window is unavailable; such events are excluded before primary inference (per §10).

## 18. Falsification
The behavioral hypothesis is formally falsified if:
- Reversal MFE is reliably smaller than or indistinguishable from the control group ($\Delta M \le 0$).
- Continuation strictly dominates post-sweep (i.e., true breakout instead of stop-run reversal).
- The effect fails family-level multiple comparison inference.

## 19. Economic Firewall
The protocol measures MFE behavior only. It explicitly prohibits calculations of PnL, expectancy, static targets, stop-losses, slippage arrays, or risk-reward distributions. These are deferred entirely to the subsequent strategy-translation phase, provided the behavioral edge is mathematically supported.

## 20. SMC / ML Firewall
Allowed: Objective session highs/lows, exact price penetrations, wicks (closes vs extremes), deterministic candle-fractal breaks.
Prohibited: Subjective order block drawing, manual FVGs, "smart money" narratives, retrospective HMM/K-means regime clustering to save failed outcomes.

## 21. Strategy Translation Firewall
Entry rules (e.g., entering at confirmation close), stops (e.g., 1 tick above wick), targets, and sizing mechanics are strictly excluded from this behavioral validation protocol. 

## 22. Readiness
**LEVEL 2 — READY FOR INDEPENDENT AUDIT**

## 23. Exact Next Task
The precise next legitimate task is the **Independent Read-Only Execution Audit** of this v1.2.0 pre-registration protocol, to verify that it is fully deterministic and capable of being executed without requiring any new scientific decisions.

## 24. Integrity
The protocol is fully registered outcome-blind. No parameters were optimized. No historical results were inspected to selectively cull or add markets. No execution scripts were run. No secondary models were attached.
