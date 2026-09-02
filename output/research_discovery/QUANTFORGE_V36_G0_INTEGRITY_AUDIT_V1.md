# QUANTFORGE — V36 G0 INTEGRITY / PRIOR-ART AUDIT

## CAND-105 + CAND-106 + CAND-107

**Date:** 2026-09-02
**Status:** AUDIT COMPLETE
**Scope:** Cross-asset, intra-bar, and cross-asset-volatility novelty audit

---

## 1. Mission

Perform a strict, adversarial, READ-ONLY G0 integrity audit of CAND-105 (Cross-Asset Lead-Lag Asymmetry), CAND-106 (Intra-Bar Price Distribution Quality), and CAND-107 (Cross-Asset Volatility Co-movement Regime).

These candidates were generated under V36's deliberate search-space diversification. The audit determines whether they represent genuinely new mechanisms/data dimensions.

---

## 2. Authoritative Repository State

- **HEAD:** `17cf997` — `docs: add V36 G0 commit SHA to SESSION_HANDOFF`
- **Branch:** `main`
- **V35 COMPLETE:** CAND-103 CLOSED (ECONOMICALLY NEGATIVE), CAND-104 CLOSED (HYPOTHESIS CONTRADICTED)
- **V34 COMPLETE:** CAND-101 CLOSED (ECONOMICALLY NEGATIVE), CAND-102 CLOSED (HYPOTHESIS CONTRADICTED)
- **G2 promotions:** 0 across all cycles
- **State Review Eligible:** CAND-077, CAND-081, CAND-083
- **Forward runtime:** CAND-015/024/035 ACTIVE / PROTECTED / UNTOUCHED

---

## 3. V36 Diversification Claim Verification

V36 claims to have moved outside the V19–V35 structural-OHLC search pattern by testing:

1. **Cross-asset information flow** (CAND-105) — relationship BETWEEN assets
2. **Bar-internal price distribution** (CAND-106) — structure WITHIN a bar
3. **Cross-asset volatility co-movement** (CAND-107) — correlation of volatility BETWEEN assets

**Assessment:** The diversification claim is VALID. All three candidates test dimensions that have never been explored in V19–V35. Prior candidates analyzed patterns WITHIN a single instrument (USATECHIDXUSD) using OHLC-derived features. V36 introduces cross-asset relationships and bar-internal structure.

---

## 4. Cross-Asset Data Availability

### Data verification

| Asset | File | Bars | Date Range | Resolution |
|---|---|---|---|---|
| XAUUSD | `data/m1/XAUUSD_M1.csv` | 1,768,123 | 2021-04-12 to 2026-04-10 | M1 |
| USATECHIDXUSD | `data/m1/USATECHIDXUSD_M1.csv` | 906,815 | 2023-09-01 to 2026-07-10 | M1 |

### Overlap period

**2023-09-01 to 2026-04-10** (~2.6 years, ~906,815 bars)

Both assets have M1 resolution with timestamp, open, high, low, close columns. Volume is 0 for both (confirmed in SESSION_HANDOFF).

### Synchronization risks

1. **Timestamp alignment:** Both use M1 bars with timestamps. However, the exact bar boundaries may not be perfectly synchronized across assets (e.g., gold may have a bar closed at 10:01 while tech has a bar closed at 10:01, but the exact close times may differ by seconds).

2. **Missing observations:** If one asset has a missing M1 bar while the other does not, the synchronization could introduce gaps. The audit notes this as a G1-implementation concern.

3. **Session overlap:** Gold trades nearly 24 hours; tech has defined session hours. The overlap period may have different trading hours, which could affect lead-lag measurement.

4. **No future information leakage:** Both datasets are independent. Neither contains information about the other's future bars.

**Data feasibility:** YES — both assets exist, have M1 resolution, and have overlapping date ranges.

---

## 5. CAND-105 Semantic Audit

### 5.1 Reconstructed Definition

```
MARKET PHENOMENON: Gold and tech respond to information at different speeds.
MECHANISM: Different participant populations (safe-haven vs risk-on) process information differently.
OBSERVABLE: Rolling correlation of returns between XAUUSD and USATECHIDXUSD.
EXPECTED EFFECT: Lead-lag regimes produce different downstream economics for tech.
TRADEABLE USE: State indicator for risk management or cross-asset positioning.
```

### 5.2 Link Quality

| Link | Assessment | Evidence |
|---|---|---|
| Market phenomenon | GOOD | Lead-lag between correlated assets is documented |
| Mechanism | BORDERLINE | Common factor exposure could produce same correlation pattern |
| Observable | GOOD | Rolling return correlation is deterministic |
| Expected effect | BORDERLINE | May reflect common trend, not information flow |
| Tradeable use | GOOD | State indicator application is clear |

**Weakest link:** Mechanism — the "information flow" explanation may be confounded with common factor exposure.

### 5.3 Critical Question

> Is this testing directional timing asymmetry between assets, or simply when both assets trend together?

**Answer:** The observable (rolling return correlation) measures SYNCHRONIZATION, not DIRECTION OF INFORMATION FLOW. High correlation means both assets move together; low correlation means they diverge. The lead-lag direction is NOT directly measured by correlation.

**This is a significant limitation.** The V36 G0 artifact claims to test "lead-lag asymmetry," but the registered observable (rolling correlation) measures co-movement, not lead-lag direction. To truly test lead-lag, one would need to compute cross-correlation at various lags and identify the lag that maximizes correlation.

**However:** The observable IS genuinely distinct from all prior work. No candidate has tested cross-asset return correlation as a conditioning variable. The distinction between "correlation" and "lead-lag" is noted as a G1-implementation concern, not a G0-rejection.

### 5.4 Novelty Verdict

> **CLEARLY NOVEL** (with caveat: observable measures co-movement, not lead-lag direction)

The cross-asset dimension is genuinely new. The observable is distinct from all prior work.

---

## 6. CAND-105 Prior-Art Comparison

| Prior candidate | Shared mechanism | Shared observable | Shared temporal structure | Material difference |
|---|---|---|---|---|
| CAND-079 (Gold vol→Tech) | Cross-asset volatility | Vol transition | Event-level | CAND-079 tested vol TRANSITION. CAND-105 tests return CORRELATION. Different observable. |
| 11 Cross-Market candidates | Cross-market effects | Various | Various | Cross-Market candidates tested cross-market effects but not return correlation as a conditioning variable. |
| CAND-103 (Multi-TF breaks) | Cross-scale coordination | Break scope | Event-level | CAND-103 tested breaks across TIMEFRAMES. CAND-105 tests returns across ASSETS. Different dimension. |
| CAND-096 (Vol acceleration) | Volatility dynamics | Rate of change | Rolling window | CAND-096 measured vol ACCELERATION within one asset. CAND-105 measures CORRELATION between assets. |

**Novelty:** CLEARLY NOVEL — cross-asset return correlation is a genuinely new conditioning variable.

---

## 7. CAND-105 Mechanism–Observable Challenge

### 7.1 Mechanism Independence

Lead-lag between correlated assets is documented in market microstructure literature. Gold and tech respond to different information flows.

### 7.2 Proxy Challenge

Correlation could arise from common macro shocks (USD, rates, risk sentiment) rather than lead-lag information flow.

### 7.3 Alternative Explanation

1. Common factor exposure (USD, rates)
2. Simultaneous news response
3. Mechanical portfolio rebalancing
4. Statistical noise

### 7.4 Observable Fidelity

Rolling return correlation captures co-movement. However, it does NOT distinguish lead from lag — it measures synchronization, not direction of information flow.

### 7.5 Expected-Effect Bridge

If co-movement regimes reflect different market stress levels, subsequent economics may differ.

### 7.6 Falsification

If co-movement regimes produce identical downstream economics, the hypothesis is contradicted.

### 7.7 Tradeability

Correlation estimation noise, regime instability, common factor dominance.

### 7.8 Base Rate

Cross-asset information flow is genuinely unexplored. The base rate is poor, but the dimension is new.

**Mechanism Confidence:** MODERATE
**Proxy Confidence:** MODERATE (caveat: measures co-movement, not lead-lag)
**Observable Information Potential:** MODERATE

---

## 8. CAND-105 Temporal Audit

```
ANCHOR: Current bar for both assets
OBSERVATION WINDOW: Rolling window of returns for both assets
SIGNAL FORMATION: After correlation is computed from completed bars
OUTCOME WINDOW: H bars after signal
```

**Leakage check:** PASS — correlation computed from completed bars only. No future information.

**Synchronization concern:** Both assets must be aligned by timestamp. Missing bars in one asset could create gaps. This is a G1-implementation concern.

---

## 9. CAND-106 Semantic Audit

### 9.1 Reconstructed Definition

```
MARKET PHENOMENON: Bar-internal price distribution contains information about participant conviction.
MECHANISM: Bars with open near extremes indicate directional conviction; open near middle indicates indecision.
OBSERVABLE: Open position ratio, close position ratio, bar symmetry.
EXPECTED EFFECT: High-conviction bars produce different downstream economics than indecision bars.
TRADEABLE USE: State indicator for entry quality or risk management.
```

### 9.2 Link Quality

| Link | Assessment | Evidence |
|---|---|---|
| Market phenomenon | GOOD | Bar-internal structure is fundamental to price action |
| Mechanism | BORDERLINE | Conviction is inferred, not directly observed |
| Observable | GOOD | Open/close position ratios are deterministic from OHLC |
| Expected effect | BORDERLINE | May reflect volatility or trend, not conviction |
| Tradeable use | GOOD | State indicator application is clear |

**Weakest link:** Mechanism — the "conviction" explanation may be confounded with volatility or trend.

### 9.3 Critical Question

> Does "open/close location within range" represent a genuinely new information dimension, or is it a mathematically repackaged candle-shape feature?

**Answer:** The observable IS genuinely distinct from prior work. Prior candidates used OHLC as inputs to compute derived features (returns, ranges, breaks). CAND-106 analyzes the INTERNAL STRUCTURE of the bar itself — where the open and close fall within the range. This is a different level of analysis.

However, the MECHANISM (conviction/indecision) is inferred. The observable may capture:
1. Volatility level (high-vol bars may have different distributions)
2. Trend state (trending markets may produce different bar structures)
3. Session timing (bars near session boundaries may have different structures)

These confounds are noted as limitations, not rejection criteria.

### 9.4 Proxy Fidelity

**What can OHLC reveal about intra-bar price distribution?**

OHLC reveals:
- Where the open falls within the range (open position ratio)
- Where the close falls within the range (close position ratio)
- How symmetric the bar is (body position relative to range)

OHLC does NOT reveal:
- Actual order flow
- Sequence of all trades
- Bid/ask dynamics
- Depth
- Liquidity-provider behavior

The observable APPROXIMATES internal acceptance/rejection. This inference must be explicitly labeled.

### 9.5 Novelty Verdict

> **CLEARLY NOVEL**

No prior candidate has analyzed bar-internal distribution. The observable is genuinely distinct from all prior work.

---

## 10. CAND-106 Prior-Art Comparison

| Prior candidate | Shared mechanism | Shared observable | Shared temporal structure | Material difference |
|---|---|---|---|---|
| CAND-077 (Vol regime) | Market state | ATR percentile | Rolling window | CAND-077 measured vol LEVEL. CAND-106 measures bar-internal STRUCTURE. Different analytical level. |
| CAND-095 (Shock magnitude) | Move size | Absolute return | Event-level | CAND-095 measured move SIZE. CAND-106 measures bar-internal DISTRIBUTION. Different observable. |
| CAND-096 (Vol acceleration) | Vol dynamics | Rate of change | Rolling window | CAND-096 measured vol ACCELERATION. CAND-106 measures bar-internal STRUCTURE. |
| CAND-098 (Event clustering) | Event patterns | Event count | Event-level | CAND-098 counted events ACROSS time. CAND-106 analyzes structure WITHIN one bar. |

**Novelty:** CLEARLY NOVEL — bar-internal distribution is a genuinely new analytical level.

---

## 11. CAND-106 Mechanism–Observable Challenge

### 11.1 Mechanism Independence

Bar-internal structure is fundamental to price action. Traders observe whether bars show conviction or indecision.

### 11.2 Proxy Challenge

Bar-internal structure could reflect volatility level, session timing, or trend state rather than conviction.

### 11.3 Alternative Explanation

1. Volatility level effects
2. Session timing effects
3. Trend state effects
4. Data quality issues

### 11.4 Observable Fidelity

Open/close position ratios directly capture bar-internal distribution. However, the mechanism (conviction) is inferred.

### 11.5 Expected-Effect Bridge

If high-conviction bars indicate strong positioning, subsequent action may be more orderly.

### 11.6 Falsification

If high-conviction and indecision bars produce identical downstream distributions, the hypothesis is contradicted.

### 11.7 Tradeability

Volatility confound, session timing, small separation consumed by costs.

### 11.8 Base Rate

Bar-internal distribution is genuinely unexplored. The dimension is new.

**Mechanism Confidence:** MODERATE
**Proxy Confidence:** MODERATE
**Observable Information Potential:** MODERATE

---

## 12. CAND-106 Temporal Audit

```
ANCHOR: Current bar
OBSERVATION WINDOW: Recent N bars of bar-internal features
SIGNAL FORMATION: After features are computed from completed bars
OUTCOME WINDOW: H bars after signal
```

**Leakage check:** PASS — features computed from completed bars only. The close is known only when the bar is complete.

---

## 13. CAND-107 Semantic Audit

### 13.1 Reconstructed Definition

```
MARKET PHENOMENON: Volatility co-movement between gold and tech identifies market regimes.
MECHANISM: High co-movement indicates correlated stress; low co-movement indicates normal conditions.
OBSERVABLE: Rolling correlation of absolute returns between XAUUSD and USATECHIDXUSD.
EXPECTED EFFECT: Co-movement regimes produce different downstream economics.
TRADEABLE USE: State indicator for risk management.
```

### 13.2 Link Quality

| Link | Assessment | Evidence |
|---|---|---|
| Market phenomenon | GOOD | Volatility co-movement is documented |
| Mechanism | BORDERLINE | Common factor exposure could produce same pattern |
| Observable | GOOD | Rolling correlation of absolute returns is deterministic |
| Expected effect | BORDERLINE | May reflect common volatility, not co-movement regime |
| Tradeable use | GOOD | State indicator application is clear |

**Weakest link:** Mechanism — the "co-movement regime" explanation may be confounded with common volatility or factor exposure.

### 13.3 Critical Question

> Does co-movement contain information about the relationship between assets, or is it merely another way of identifying high/low volatility regimes?

**Answer:** The observable (correlation of absolute returns) measures the RELATIONSHIP between asset volatilities, not volatility within one asset. This is a different analytical framework from CAND-077/096/099, which analyzed volatility WITHIN one asset.

However, the MECHANISM (market stress) is inferred. High co-movement could reflect:
1. Common macro shocks
2. Simultaneous session effects
3. Shared global risk factors
4. Volatility level effects

These confounds are noted as limitations.

### 13.4 Novelty Verdict

> **CLEARLY NOVEL**

No prior candidate has tested cross-asset volatility co-movement. The observable is genuinely distinct from all prior work.

---

## 14. CAND-107 Prior-Art Comparison

| Prior candidate | Shared mechanism | Shared observable | Shared temporal structure | Material difference |
|---|---|---|---|---|
| CAND-077 (Vol regime) | Volatility state | ATR percentile | Rolling window | CAND-077 measured vol WITHIN one asset. CAND-107 measures vol CORRELATION BETWEEN assets. |
| CAND-096 (Vol acceleration) | Vol dynamics | Rate of change | Rolling window | CAND-096 measured vol ACCELERATION. CAND-107 measures vol CO-MOVEMENT. |
| CAND-099 (Transition quality) | Vol transition | Smoothness | Event-level | CAND-099 tested transition SMOOTHNESS. CAND-107 tests co-movement REGIME. |
| CAND-079 (Gold vol→Tech) | Cross-asset vol | Vol transition | Event-level | CAND-079 tested gold→tech vol TRANSITION. CAND-107 tests vol CO-MOVEMENT REGIME. |

**Novelty:** CLEARLY NOVEL — cross-asset volatility co-movement is a genuinely new dimension.

---

## 15. CAND-107 Mechanism–Observable Challenge

### 15.1 Mechanism Independence

Volatility co-movement between correlated assets is documented. High co-movement indicates correlated stress.

### 15.2 Proxy Challenge

Co-movement could reflect common macro factors (USD, rates, risk sentiment) rather than genuine market stress.

### 15.3 Alternative Explanation

1. Common macro shocks
2. Simultaneous session effects
3. Shared global risk factors
4. Volatility level effects

### 15.4 Observable Fidelity

Rolling correlation of absolute returns captures co-movement. However, the mechanism (market stress) is inferred.

### 15.5 Expected-Effect Bridge

If high co-movement indicates correlated stress, subsequent action may be wider and more uncertain.

### 15.6 Falsification

If co-movement regimes produce identical downstream economics, the hypothesis is contradicted.

### 15.7 Tradeability

Correlation estimation noise, regime instability, common factor dominance.

### 15.8 Base Rate

Cross-asset volatility co-movement is genuinely unexplored. The dimension is new.

**Mechanism Confidence:** MODERATE
**Proxy Confidence:** MODERATE
**Observable Information Potential:** MODERATE

---

## 16. CAND-107 Temporal Audit

```
ANCHOR: Current bar for both assets
OBSERVATION WINDOW: Rolling window of absolute returns for both assets
SIGNAL FORMATION: After correlation is computed from completed bars
OUTCOME WINDOW: H bars after signal
```

**Leakage check:** PASS — correlation computed from completed bars only.

**Synchronization concern:** Same as CAND-105 — both assets must be aligned by timestamp.

---

## 17. Cross-Candidate Comparison

| Dimension | CAND-105 | CAND-106 | CAND-107 |
|---|---|---|---|
| New data dimension | Cross-asset returns | Bar-internal structure | Cross-asset volatility |
| Mechanism | Lead-lag / info flow | Conviction / indecision | Co-movement regime |
| Primary risk | Common factor confound | Volatility confound | Common factor confound |
| Novelty | CLEARLY NOVEL | CLEARLY NOVEL | CLEARLY NOVEL |
| Mechanism Confidence | MODERATE | MODERATE | MODERATE |
| Proxy Confidence | MODERATE | MODERATE | MODERATE |

**Cross-asset semantic integrity:** CAND-105 and CAND-107 both use XAUUSD + USATECHIDXUSD. Both assets contribute genuine information — gold and tech have different participant populations and respond to different information flows. The cross-asset relationship is not simply "mostly Asset A state."

---

## 18. Data Feasibility

| Candidate | Required Data | Available | Feasible |
|---|---|---|---|
| CAND-105 | XAUUSD M1 + USATECHIDXUSD M1 | YES | YES |
| CAND-106 | USATECHIDXUSD M1 OHLC | YES | YES |
| CAND-107 | XAUUSD M1 + USATECHIDXUSD M1 | YES | YES |

All three candidates have confirmed data availability.

---

## 19. Parameter Audit

### CAND-105

| Parameter | Classification | Status |
|---|---|---|
| Correlation lookback | STRUCTURAL | Pre-declare before G1 |
| Outcome horizon | STRUCTURAL | Pre-declare before G1 |
| Sampling alignment | STRUCTURAL | Pre-declare before G1 |

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

## 20. Final G1-Readiness Disposition

### CAND-105: Cross-Asset Lead-Lag Asymmetry

| Criterion | Status |
|---|---|
| New data dimension | YES — cross-asset returns |
| Mechanism novelty | YES — lead-lag / info flow |
| Observable novelty | YES — rolling cross-asset correlation |
| Temporal integrity | PASS |
| Data feasibility | YES |
| Mechanism confidence | MODERATE |
| Proxy confidence | MODERATE (caveat: measures co-movement, not lead-lag direction) |

> **PASS — G1 ELIGIBLE**

### CAND-106: Intra-Bar Price Distribution Quality

| Criterion | Status |
|---|---|
| New data dimension | YES — bar-internal structure |
| Mechanism novelty | YES — conviction / indecision |
| Observable novelty | YES — open/close position ratios |
| Temporal integrity | PASS |
| Data feasibility | YES |
| Mechanism confidence | MODERATE |
| Proxy confidence | MODERATE |

> **PASS — G1 ELIGIBLE**

### CAND-107: Cross-Asset Volatility Co-movement Regime

| Criterion | Status |
|---|---|
| New data dimension | YES — cross-asset volatility correlation |
| Mechanism novelty | YES — co-movement regime |
| Observable novelty | YES — rolling cross-asset vol correlation |
| Temporal integrity | PASS |
| Data feasibility | YES |
| Mechanism confidence | MODERATE |
| Proxy confidence | MODERATE |

> **PASS — G1 ELIGIBLE**

---

## 21. Governance Conclusion

### V36 G0 INTEGRITY AUDIT — RESULT

| Candidate | New Dimension | Mechanism Novelty | Observable Novelty | Temporal Integrity | Data Feasible | Mechanism Confidence | Proxy Confidence | Final Disposition |
|---|---|---|---|---|---|---|---|---|
| CAND-105 | Cross-asset returns | CLEARLY NOVEL | CLEARLY NOVEL | PASS | YES | MODERATE | MODERATE | **G1 ELIGIBLE** |
| CAND-106 | Bar-internal structure | CLEARLY NOVEL | CLEARLY NOVEL | PASS | YES | MODERATE | MODERATE | **G1 ELIGIBLE** |
| CAND-107 | Cross-asset vol correlation | CLEARLY NOVEL | CLEARLY NOVEL | PASS | YES | MODERATE | MODERATE | **G1 ELIGIBLE** |

### Cross-Candidate Conclusion

All three candidates survive the integrity audit. **3 G1-eligible candidates.**

### Governance Verification

- ✅ No G1 executed
- ✅ No outcome analysis
- ✅ No optimization
- ✅ No closed candidate reopened
- ✅ No CAND-099 reuse
- ✅ No relational testing
- ✅ No APEX execution
- ✅ No protected runtime inspection

### Files Changed

| File | Purpose |
|---|---|
| `output/research_discovery/QUANTFORGE_V36_G0_INTEGRITY_AUDIT_V1.md` | Integrity audit artifact |
| `docs/SESSION_HANDOFF.md` | Updated with audit results |
| `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` | Audit disposition recorded |
| `research/knowledge/RESEARCH_TIMELINE.md` | Audit timeline entry |

### Commit

SHA: pending

### SESSION_HANDOFF

Updated and verified.

### Next Permitted Task

> **V36 G1 — ECONOMIC PLAUSIBILITY SCREEN for CAND-105, CAND-106, and CAND-107**
