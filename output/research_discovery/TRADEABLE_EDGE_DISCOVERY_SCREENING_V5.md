# QuantForge — G0 Candidate Generation
# TRADEABLE EDGE DISCOVERY SCREENING V5

## 1. Research Factory V2 Context

Following the adoption of the `QUANTFORGE_RESEARCH_FACTORY_V2.md` doctrine, and the 2026-08-25 refinement around Conditional Market Behavior and Opportunity Integrity, QuantForge operates as an Economic-First / Cost-Aware Research Funnel. 

This document represents the execution of the G0 milestone for the V5 candidate generation cycle.

## 2. G0 Objective

The objective of this screening is to identify candidates focused on repeatable market events/states and the conditional directional response following an executable entry. This cycle explicitly investigates the market-state/KPI conditions that influence that response, rather than searching for unconditional patterns.

## 3. Mandatory Governance Rules (New)

1. **Closed-Line Anti-Rescue Rule:** A previously failed candidate cannot be revived by adding a conditioning variable, filter, regime label, or timeframe alignment unless the new mechanism is demonstrably a different scientific object rather than a post-hoc refinement.
2. **Mechanistic Justification:** Does the conditioning variable have an independently justified causal/mechanistic reason to alter the conditional response? Conditional KPIs must not be found via data-mined filtering of a pattern.

## 4. Rejected Candidates

### CAND-G0-014 (HTF-Aligned Momentum Divergence)
**G0 Disposition:** **KILL — closed-line rescue/variant.**
**Reasoning:** This candidate proposed adding a higher-timeframe trend filter to the exact Double Top + RSI Divergence mechanism that failed the G1 economic screen as CAND-G0-011. Under the new Anti-Rescue Rule, adding a timeframe alignment to a closed candidate is considered a post-failure filter applied to rescue a closed line. It is not a genuinely new object. 

---

## 5. Candidate Cards (Promoted)

### CAND-G0-012
**Name:** Trend-Pullback Re-Acceleration
**Mechanism Family:** Trend Continuation / Conditional Market Behavior
**Market Mechanism:** A strong macro trend pulls back to a short-term dynamic mean. The probability of trend resumption (momentum re-acceleration) with positive expectancy is hypothesized to be conditioned by the volatility state of the pullback itself.
**Scientific Object:** The forward return distribution of a pullback touch, conditioned on localized volatility.
**Conditioning KPI:** Pullbacks occurring under low localized volatility yield higher expectancy than high-volatility (panic) pullbacks.
**Deterministic Frozen Definitions:**
- **Strong Macro Trend:** D1 ADX(14) > 25 and directional alignment (D1 +DI > -DI for uptrend, -DI > +DI for downtrend).
- **Short-Term Dynamic Mean:** H1 20-period Exponential Moving Average (EMA).
- **Low Localized Volatility:** H1 ATR(14) is strictly less than its own 20-period Simple Moving Average.
- **Event Onset (First Touch):** The High (in downtrend) or Low (in uptrend) of the current H1 bar crosses the H1 20-EMA for the first time since the Re-Arm Condition was met. (Prevents ambiguous wicks from generating multiple events).
- **Executable Entry:** Market order on the close of the H1 bar that completes the Event Onset.
- **Event Completion / Deterministic Exit:** Fixed 8-hour forward measurement window.
- **Re-Arm Condition (New Swing):** Price must exceed the most recent 5-bar local maximum (in uptrend) or minimum (in downtrend) in the trend direction, OR cross the opposing 50-period EMA, before a new pullback touch can be considered an event.
- **Duplicate Suppression:** Hard suppression of any touches that occur before the Re-Arm condition is met.
**Expected Frequency:** Moderate.
**Economic Headroom:** UNKNOWN.
**Cross-Market Scope:** Universal (FX, Crypto, Metals, Indices).
**Cheapest Data Needed:** Hourly.
**G1 Screen:** Compute the median 8-hour forward directional excursion, conditioned on the H1 ATR state, against a 3.0 bps friction barrier.
**Closed-Line Independence:** NEW.
**G0 Verdict:** PROMOTE TO G1 (Definitions frozen).

---

### CAND-G0-013
**Name:** Macro-Shock Volatility Reset Continuation
**Mechanism Family:** Event-driven / Volatility Regime / Conditional Market Behavior
**Market Mechanism:** An extreme volatility event normalizes into a period of declining volatility. The hypothesis asks whether the original directional impulse persists after the normalization phase.
**Scientific Object:** The post-reset directional drift, conditioned by the liquidity/session state.
**Conditioning KPI:** The continuation probability and expectancy differ by liquidity/session state (e.g., Asian session transition vs. London session transition).
**Deterministic Frozen Definitions:**
- **Hypothesis Parameter 1 (Extreme Volatility Shock):** H1 ATR(14) spikes > 3 standard deviations above its 30-day rolling mean.
- **Hypothesis Parameter 2 (Normalization Phase):** 4 consecutive hours of strictly declining ATR immediately following the shock bar.
- **Event Onset:** The close of the 4th consecutive hour of declining ATR.
- **Executable Entry:** Market order on the close of the 4th normalization hour, in the direction of the initial macro-shock bar's return.
- **Event Completion / Deterministic Exit:** Fixed 12-hour forward measurement window.
- **Re-Arm Condition / Duplicate Suppression:** Hard 24-hour lockout after an event onset. Only one opportunity can be generated per 24-hour cycle to prevent overlapping opportunities from the same macro event.
**Expected Frequency:** Low (macro events only).
**Economic Headroom:** UNKNOWN.
**Cross-Market Scope:** FX, Metals.
**Cheapest Data Needed:** Hourly.
**G1 Screen:** Measure the median 12-hour return following the reset, separated by the session in which the entry occurs, tested against realistic spread.
**Closed-Line Independence:** NEW (Diverges from mean reversion by hypothesizing continuation after shock).
**G0 Verdict:** PROMOTE TO G1 (Definitions frozen).
