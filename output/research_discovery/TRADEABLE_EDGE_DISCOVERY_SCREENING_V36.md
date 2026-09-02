# TRADEABLE EDGE DISCOVERY SCREENING — V36

## 1. G0 Status

> V36 G0 — SEARCH-SPACE DIVERSIFICATION / NEW MECHANISM DISCOVERY

Date: 2026-09-02
Market: USATECHIDXUSD M1 + XAUUSD M1 (cross-asset)
Data range: 2023-09-01 to 2026-07-10 (~2.9 years)

**V36 deliberately breaks the V19–V35 structural-OHLC search pattern.**

---

## 2. V36 Starting State

### V35 results

- CAND-103 CLOSED — ECONOMICALLY NEGATIVE (multi-timeframe breaks produce no separation)
- CAND-104 CLOSED — HYPOTHESIS CONTRADICTED (large moves followed by mean reversion)
- V35 permanently closed. 0 G2 promotions.

### Strategic conclusion from V19–V35

95+ candidates tested. 0 G2 promotions. The dominant search pattern — M1 OHLC-derived structural/volatility/directional mechanisms — has been exhaustively explored with diminishing returns. V36 must move to genuinely different information dimensions.

---

## 3. V19–V35 Mechanism Coverage

| Dimension | Candidates Tested | Status |
|---|---|---|
| Structural breaks / levels | CAND-077/081/083/086/087/088/089/091/092/093/095/098/101/102/103/104 | Exhausted — diminishing returns |
| Volatility dynamics | CAND-077/079/080/096/099 | Exhausted — CAND-077 State-eligible, others negative/contradicted |
| Direction / momentum | CAND-091/092/095/102/104 | Exhausted — all negative/contradicted |
| Event sequencing / clustering | CAND-098/101 | Exhausted — negative |
| Shock / magnitude | CAND-095/099/104 | Exhausted — negative/contradicted |
| Cross-market | CAND-079 + 11 Cross-Market candidates | Mostly blocked/negative |
| Settlement / benchmark | DISC-022/023 + 3 Settlement candidates | All economically negative |
| Mean reversion | DISC-021 | CLOSED |
| Execution stress | CAND-100 | DATA INFEASIBLE |

---

## 4. Search-Space Gap Matrix

| Dimension | Already Tested? | Evidence | Remaining Gap |
|---|---|---|---|
| Price path / structural events | YES (16+ candidates) | Exhausted | None — do not reuse |
| Volatility level / regime | YES (7+ candidates) | CAND-077 State-eligible | Do not add more volatility scalars |
| Volatility acceleration / rate | YES (CAND-096) | CONTRADICTED | Closed |
| Transition quality | YES (CAND-099) | CONTRADICTED | Closed |
| Direction / momentum | YES (5+ candidates) | All negative/contradicted | Closed |
| Event recency / decay | YES (CAND-092) | NEGATIVE | Closed |
| Event clustering | YES (CAND-098) | NEGATIVE | Closed |
| Event ordering | YES (CAND-101) | NEGATIVE | Closed |
| Directional persistence | YES (CAND-102) | CONTRADICTED | Closed |
| Shock magnitude | YES (CAND-095/104) | NEGATIVE/CONTRADICTED | Closed |
| Multi-timeframe breaks | YES (CAND-103) | NEGATIVE | Closed |
| Cross-asset lead-lag | **NO** | Never tested | **OPEN — genuinely new** |
| Intra-bar distribution | **NO** | Never tested | **OPEN — genuinely new** |
| Return distribution shape | **NO** | Never tested | **OPEN — genuinely new** |
| Cross-asset volatility co-movement | **NO** | Never tested | **OPEN — genuinely new** |

---

## 5. Exhausted Dimensions

The following are permanently exhausted for V36+ candidate generation:

- Structural break conditioning
- Volatility regime / state
- Volatility acceleration
- Transition quality
- Directional momentum / exhaustion
- Shock magnitude / direction
- Event recency / decay
- Event clustering / density
- Event ordering / sequencing
- Multi-timeframe break coordination
- Post-magnitude directional drift
- Path-dependent sequence asymmetry
- Directional run-length persistence

---

## 6. Candidate Proposals

### Candidate 1: CAND-105 — Cross-Asset Lead-Lag Asymmetry

**Expression Class:** STATE / CONDITION
**Mechanism Family:** Cross-Asset Information Flow
**New Dimension:** Cross-sectional information (multiple instruments)

**Market phenomenon:** Gold (XAUUSD) and tech (USATECHIDXUSD) are driven by different participant populations with different information processing speeds. Gold responds to safe-haven flows; tech responds to risk-on/growth flows. The lead-lag relationship between these assets may vary across market conditions, creating exploitable information.

**Mechanism:** When gold leads tech, it may indicate safe-haven anticipation of risk events. When tech leads gold, it may indicate risk-on momentum. The lead-lag structure reflects which participant group is reacting first to new information.

**Observable:** Rolling correlation of returns between XAUUSD and USATECHIDXUSD over a defined window. Direction of lead (which asset's returns precede the other).

**Expected economic effect:** Periods where gold leads tech may produce different downstream economics for tech than periods where tech leads gold. The lead-lag structure may serve as a State indicator.

**Why this is genuinely distinct:**
- No prior candidate has tested cross-asset information flow
- CAND-079 tested gold→tech vol transition, not lead-lag return dynamics
- 11 Cross-Market candidates tested cross-market effects but not lead-lag structure
- This uses a genuinely different data dimension: relationship BETWEEN assets, not within one asset

---

### Candidate 2: CAND-106 — Intra-Bar Price Distribution Quality

**Expression Class:** STATE / CONDITION
**Mechanism Family:** Bar-Internal Structure
**New Dimension:** Bar-internal price distribution (beyond simple OHLC)

**Market phenomenon:** The internal structure of a price bar — where the open falls within the bar's range, how symmetric the bar is, whether the close is near the high or low — contains information about participant conviction and market microstructure that is not captured by simple returns or volatility.

**Mechanism:** Bars with open near the high and close near the low (or vice versa) indicate strong directional conviction. Bars with open near the middle indicate indecision or balanced two-way flow. The distribution of bar-internal features across recent history may predict subsequent market behavior.

**Observable:** Open position ratio (open - low) / (high - low), close position ratio (close - low) / (high - low), bar symmetry measure.

**Expected economic effect:** Bars with extreme open/close positions (high conviction) may produce different downstream economics than bars with middle open/close positions (indecision). The conviction distribution may serve as a State indicator.

**Why this is genuinely distinct:**
- No prior candidate has analyzed bar-internal distribution
- CAND-077/096/099 analyzed volatility LEVELS and TRANSITIONS, not bar-internal structure
- CAND-095/104 analyzed move MAGNITUDE, not bar-internal distribution
- This measures the QUALITY of price movement within a bar, not the SIZE or DIRECTION

---

### Candidate 3: CAND-107 — Cross-Asset Volatility Co-movement Regime

**Expression Class:** STATE / CONDITION
**Mechanism Family:** Cross-Asset Volatility Dynamics
**New Dimension:** Cross-asset volatility correlation regime

**Market phenomenon:** The correlation of volatility between gold and tech may shift between regimes: high co-movement (both volatile together, indicating market stress) and low co-movement (independent volatility, indicating normal conditions). These regimes may have different economic properties.

**Mechanism:** High volatility co-movement indicates correlated stress across asset classes — participants are repositioning simultaneously across markets. Low co-movement indicates independent market dynamics. The regime shift may predict changes in market behavior.

**Observable:** Rolling correlation of absolute returns (volatility proxy) between XAUUSD and USATECHIDXUSD.

**Expected economic effect:** High co-movement regimes may produce wider distributions and different directional dynamics than low co-movement regimes. The regime may serve as a State indicator for risk management.

**Why this is genuinely distinct:**
- No prior candidate has tested cross-asset volatility co-movement
- CAND-077 tested volatility STATE within one asset
- CAND-096 tested volatility ACCELERATION within one asset
- CAND-079 tested gold→tech VOL TRANSITION, not co-movement regime
- This measures the RELATIONSHIP between asset volatilities, not volatility within one asset

---

## 7. New-Dimension Justification

### CAND-105

**New dimension:** Cross-sectional information flow between instruments.

All prior V19–V35 candidates analyzed patterns WITHIN a single instrument (USATECHIDXUSD). CAND-105 analyzes the INFORMATIONAL RELATIONSHIP between two instruments (XAUUSD and USATECHIDXUSD). This is a fundamentally different data dimension.

### CAND-106

**New dimension:** Bar-internal price distribution structure.

All prior candidates used OHLC as inputs to compute derived features (returns, ranges, breaks). CAND-106 analyzes the INTERNAL STRUCTURE of the bar itself — where the open and close fall within the range. This is a different level of analysis.

### CAND-107

**New dimension:** Cross-asset volatility correlation regime.

Prior volatility research (CAND-077/096/099) analyzed volatility WITHIN one asset. CAND-107 analyzes the CORRELATION of volatility BETWEEN two assets. This is a different analytical framework.

---

## 8. Mechanism–Observable Challenge

### CAND-105: Cross-Asset Lead-Lag Asymmetry

#### 8.1 Mechanism Independence

**What phenomenon exists independently?**

Lead-lag relationships between correlated assets are a documented market phenomenon. Gold and tech respond to different information flows at different speeds. This exists independently of any specific formula.

#### 8.2 Proxy Challenge

**How can the observable arise without the mechanism?**

Return correlation could reflect simultaneous response to common factors (e.g., USD strength, interest rates) rather than lead-lag information flow. The correlation may be spurious.

#### 8.3 Alternative Explanation

**What competing process could produce it?**

1. Common factor exposure (USD, rates)
2. Simultaneous news response
3. Mechanical portfolio rebalancing
4. Statistical noise in correlation estimation

#### 8.4 Observable Fidelity

**Why does the observable reasonably measure the mechanism?**

Rolling return correlation directly captures the co-movement relationship. However, correlation does not distinguish lead from lag — it measures synchronization, not direction of information flow.

#### 8.5 Expected-Effect Bridge

**Why should it alter subsequent outcomes?**

If gold leads tech during risk-off periods, the lead-lag structure may predict tech's subsequent behavior. The informational advantage of knowing which asset is leading could inform risk management.

#### 8.6 Falsification

**What would clearly contradict the hypothesis?**

If lead-lag regimes produce identical downstream economics for tech, the hypothesis is contradicted.

#### 8.7 Tradeability

**What could destroy the information?**

1. Correlation estimation noise
2. Regime instability
3. Transaction costs consuming small effects
4. Common factor dominance

#### 8.8 Base Rate

**Why should G1 resources be spent?**

Cross-asset information flow is a genuinely unexplored dimension. No prior candidate has tested lead-lag dynamics. The base rate is poor, but the mechanism is economically plausible and uses a genuinely new data dimension.

**Mechanism Confidence:** MODERATE
**Proxy Confidence:** MODERATE
**Observable Information Potential:** MODERATE

---

### CAND-106: Intra-Bar Price Distribution Quality

#### 8.1 Mechanism Independence

**What phenomenon exists independently?**

Bar-internal structure (where open/close fall within range) is a fundamental property of price action. Traders observe whether bars show conviction (close near extreme) or indecision (close near middle). This exists independently.

#### 8.2 Proxy Challenge

**How can the observable arise without the mechanism?**

Bar-internal structure could simply reflect volatility level — high-vol bars may have different open/close distributions than low-vol bars. The observable may conflate conviction with volatility.

#### 8.3 Alternative Explanation

**What competing process could produce it?**

1. Volatility level effects
2. Session timing effects (open/close near session boundaries)
3. Mechanical price dynamics (trending vs ranging markets)
4. Data quality issues (M1 bar construction)

#### 8.4 Observable Fidelity

**Why does the observable reasonably measure the mechanism?**

Open/close position ratios directly capture the bar-internal distribution. However, the mechanism (conviction/indecision) is inferred.

#### 8.5 Expected-Effect Bridge

**Why should it alter subsequent outcomes?**

If high-conviction bars indicate strong directional positioning, subsequent price action may be more orderly. If indecision bars indicate balanced flow, subsequent action may be more uncertain.

#### 8.6 Falsification

**What would clearly contradict the hypothesis?**

If high-conviction and indecision bars produce identical downstream distributions, the hypothesis is contradicted.

#### 8.7 Tradeability

**What could destroy the information?**

1. Volatility confound
2. Session timing effects
3. Small separation consumed by costs
4. Parameter sensitivity

#### 8.8 Base Rate

**Why should G1 resources be spent?**

Bar-internal distribution is a genuinely unexplored dimension. No prior candidate has analyzed where open/close fall within the bar range. The mechanism is plausible and the observable is clean.

**Mechanism Confidence:** MODERATE
**Proxy Confidence:** MODERATE
**Observable Information Potential:** MODERATE

---

### CAND-107: Cross-Asset Volatility Co-movement Regime

#### 8.1 Mechanism Independence

**What phenomenon exists independently?**

Volatility co-movement between correlated assets is a documented phenomenon. High co-movement indicates correlated stress; low co-movement indicates independent dynamics. This exists independently.

#### 8.2 Proxy Challenge

**How can the observable arise without the mechanism?**

Co-movement could reflect common factor exposure (USD, rates) rather than genuine market stress. The regime may be driven by external factors, not internal market dynamics.

#### 8.3 Alternative Explanation

**What competing process could produce it?**

1. Common factor exposure
2. Mechanical portfolio rebalancing
3. Statistical noise in correlation estimation
4. Calendar effects

#### 8.4 Observable Fidelity

**Why does the observable reasonably measure the mechanism?**

Rolling correlation of absolute returns directly captures co-movement. However, the mechanism (market stress) is inferred.

#### 8.5 Expected-Effect Bridge

**Why should it alter subsequent outcomes?**

If high co-movement indicates correlated stress, subsequent price action may be wider and more uncertain. If low co-movement indicates normal conditions, subsequent action may be more predictable.

#### 8.6 Falsification

**What would clearly contradict the hypothesis?**

If co-movement regimes produce identical downstream economics, the hypothesis is contradicted.

#### 8.7 Tradeability

**What could destroy the information?**

1. Correlation estimation noise
2. Regime instability
3. Common factor dominance
4. Costs consuming small effects

#### 8.8 Base Rate

**Why should G1 resources be spent?**

Cross-asset volatility co-movement is a genuinely unexplored dimension. No prior candidate has tested this. The mechanism is plausible and uses a genuinely new analytical framework.

**Mechanism Confidence:** MODERATE
**Proxy Confidence:** MODERATE
**Observable Information Potential:** MODERATE

---

## 9. Prior-Art / Novelty Audit

### CAND-105

| Dimension | Closest Prior | CAND-105 | Distinction |
|---|---|---|---|
| Mechanism | CAND-079 (gold→tech vol transition) | Cross-asset return lead-lag | CAND-079 tested vol TRANSITION. CAND-105 tests return LEAD-LAG. Different observable. |
| Observable | 11 Cross-Market candidates | Rolling return correlation | Cross-Market candidates tested cross-market effects but not lead-lag dynamics. |
| Temporal structure | CAND-092 (event recency) | Rolling window correlation | CAND-092 measured time since ONE event. CAND-105 measures ongoing correlation. |
| Economic question | CAND-095 (shock direction) | Which asset leads? | CAND-095 tested direction of shock. CAND-105 tests direction of information flow between assets. |

**Novelty:** CLEARLY NOVEL — cross-asset information flow is a genuinely new dimension.

### CAND-106

| Dimension | Closest Prior | CAND-106 | Distinction |
|---|---|---|---|
| Mechanism | CAND-077 (vol regime) | Bar-internal distribution | CAND-077 measured volatility LEVEL. CAND-106 measures bar-internal STRUCTURE. Different analytical level. |
| Observable | CAND-095 (shock magnitude) | Open/close position ratios | CAND-095 measured move SIZE. CAND-106 measures bar-internal DISTRIBUTION. Different observable. |
| Temporal structure | CAND-098 (event clustering) | Single-bar internal structure | CAND-098 counted events across time. CAND-106 analyzes structure within one bar. |
| Economic question | CAND-096 (vol acceleration) | Bar conviction quality | CAND-096 measured rate of vol change. CAND-106 measures quality of price movement within a bar. |

**Novelty:** CLEARLY NOVEL — bar-internal distribution is a genuinely new analytical level.

### CAND-107

| Dimension | Closest Prior | CAND-107 | Distinction |
|---|---|---|---|
| Mechanism | CAND-077 (vol regime) | Cross-asset vol co-movement | CAND-077 measured vol WITHIN one asset. CAND-107 measures vol CORRELATION BETWEEN assets. Different framework. |
| Observable | CAND-079 (gold→tech vol transition) | Rolling correlation of absolute returns | CAND-079 tested vol TRANSITION. CAND-107 tests vol CO-MOVEMENT REGIME. Different observable. |
| Temporal structure | CAND-096 (vol acceleration) | Rolling correlation window | CAND-096 measured rate of vol change. CAND-107 measures co-movement regime. |
| Economic question | CAND-099 (transition quality) | Co-movement regime economics | CAND-099 tested transition SMOOTHNESS. CAND-107 tests co-movement REGIME. |

**Novelty:** CLEARLY NOVEL — cross-asset volatility co-movement is a genuinely new dimension.

---

## 10. Data Feasibility

### CAND-105

**Required data:**
- USATECHIDXUSD M1: YES (`data/m1/USATECHIDXUSD_M1.csv`)
- XAUUSD M1: YES (`data/m1/XAUUSD_M1.csv`)
- Return computation: YES
- Correlation computation: YES

**Data feasibility:** YES

### CAND-106

**Required data:**
- USATECHIDXUSD M1: YES
- OHLC: YES
- Open/close position ratios: YES (deterministic from OHLC)

**Data feasibility:** YES

### CAND-107

**Required data:**
- USATECHIDXUSD M1: YES
- XAUUSD M1: YES
- Absolute returns: YES
- Correlation computation: YES

**Data feasibility:** YES

---

## 11. Temporal Integrity

### CAND-105

```
ANCHOR: Current bar
OBSERVATION WINDOW: Rolling window of returns for both assets
SIGNAL FORMATION: After correlation is computed from completed bars
OUTCOME WINDOW: H bars after signal
```

**Leakage check:** PASS — correlation computed from completed bars only.

### CAND-106

```
ANCHOR: Current bar
OBSERVATION WINDOW: Recent N bars of bar-internal features
SIGNAL FORMATION: After features are computed
OUTCOME WINDOW: H bars after signal
```

**Leakage check:** PASS — features computed from completed bars only.

### CAND-107

```
ANCHOR: Current bar
OBSERVATION WINDOW: Rolling window of absolute returns for both assets
SIGNAL FORMATION: After correlation is computed from completed bars
OUTCOME WINDOW: H bars after signal
```

**Leakage check:** PASS — correlation computed from completed bars only.

---

## 12. Parameter Governance

### CAND-105

| Parameter | Classification | Status |
|---|---|---|
| Correlation lookback | STRUCTURAL | Pre-declare before G1 |
| Outcome horizon | STRUCTURAL | Pre-declare before G1 |
| Lead-lag detection method | STRUCTURAL | Pre-declare before G1 |

### CAND-106

| Parameter | Classification | Status |
|---|---|---|
| Feature lookback | STRUCTURAL | Pre-declare before G1 |
| Outcome horizon | STRUCTURAL | Pre-declare before G1 |
| Conviction thresholds | STRUCTURAL | Pre-declare before G1 |

### CAND-107

| Parameter | Classification | Status |
|---|---|---|
| Correlation lookback | STRUCTURAL | Pre-declare before G1 |
| Co-movement regime thresholds | STRUCTURAL | Pre-declare before G1 |
| Outcome horizon | STRUCTURAL | Pre-declare before G1 |

All parameters are STRUCTURAL and can be frozen before G1.

---

## 13. State vs Alpha Classification

### CAND-105: STATE / CONDITION

**Why:** The lead-lag regime is a market condition that could modify the economics of downstream events. It is not a standalone Alpha.

**What future decision could this state inform?**
- Risk management: adjust exposure based on which asset is leading
- Cross-asset positioning: favor long/short depending on lead-lag regime

### CAND-106: STATE / CONDITION

**Why:** The bar-internal distribution is a market condition that could modify the economics of downstream events. It is not a standalone Alpha.

**What future decision could this state inform?**
- Entry quality: prefer entries during high-conviction bars
- Risk management: reduce exposure during indecision bars

### CAND-107: STATE / CONDITION

**Why:** The co-movement regime is a market condition that could modify the economics of downstream events. It is not a standalone Alpha.

**What future decision could this state inform?**
- Risk management: reduce exposure during high co-movement (stress) regimes
- Position sizing: adjust based on co-movement regime

---

## 14. Tradeability Challenge

### CAND-105

**What must be true?**
1. Lead-lag regimes must produce ≥2 bps separation
2. Regimes must be identifiable in real-time
3. The effect must survive 2 bps costs

**What could destroy it?**
- Correlation estimation noise
- Regime instability
- Common factor dominance

### CAND-106

**What must be true?**
1. Bar-internal features must produce ≥2 bps separation
2. Features must be computable in real-time
3. The effect must survive 2 bps costs

**What could destroy it?**
- Volatility confound
- Session timing effects
- Small separation consumed by costs

### CAND-107

**What must be true?**
1. Co-movement regimes must produce ≥2 bps separation
2. Regimes must be identifiable in real-time
3. The effect must survive 2 bps costs

**What could destroy it?**
- Correlation estimation noise
- Regime instability
- Common factor dominance

---

## 15. Base-Rate Challenge

The historical base rate is 0 G2 promotions across 95+ candidates. However, V36 deliberately moves to genuinely new information dimensions (cross-asset, bar-internal, co-movement regime) that have never been tested. The base rate applies to the OLD search pattern; V36 is testing NEW dimensions.

---

## 16. G1 Eligibility

### CAND-105: Cross-Asset Lead-Lag Asymmetry

> **NEW — G1 ELIGIBLE**

Rationale: Genuinely new dimension (cross-asset information flow), clean observable, not a variant of prior candidates.

### CAND-106: Intra-Bar Price Distribution Quality

> **NEW — G1 ELIGIBLE**

Rationale: Genuinely new dimension (bar-internal distribution), clean observable, not a variant of prior candidates.

### CAND-107: Cross-Asset Volatility Co-movement Regime

> **NEW — G1 ELIGIBLE**

Rationale: Genuinely new dimension (cross-asset vol co-movement), clean observable, not a variant of prior candidates.

---

## 17. Governance Conclusion

V36 G0 discovery complete. Three candidates generated:

| ID | Title | New Dimension | Type | Mechanism Confidence | Proxy Confidence | Observable Information Potential | G1 Status |
|---|---|---|---|---|---|---|---|
| CAND-105 | Cross-Asset Lead-Lag Asymmetry | Cross-sectional info flow | STATE / CONDITION | MODERATE | MODERATE | MODERATE | G1 ELIGIBLE |
| CAND-106 | Intra-Bar Price Distribution Quality | Bar-internal structure | STATE / CONDITION | MODERATE | MODERATE | MODERATE | G1 ELIGIBLE |
| CAND-107 | Cross-Asset Volatility Co-movement Regime | Cross-asset vol correlation | STATE / CONDITION | MODERATE | MODERATE | MODERATE | G1 ELIGIBLE |

**Key finding:** V36 successfully moved outside the dominant V19–V35 structural-OHLC search pattern. All three candidates test genuinely new information dimensions using cross-asset data and bar-internal structure that have never been explored.

**V36 G0 is COMPLETE.** Awaiting integrity/prior-art audit before G1.
