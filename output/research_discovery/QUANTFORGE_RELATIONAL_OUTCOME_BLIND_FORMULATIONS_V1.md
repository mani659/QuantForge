# QUANTFORGE — RELATIONAL OUTCOME-BLIND FORMULATIONS
# OUTCOME-BLIND FORMULATION CYCLE — RELATIONAL MECHANISMS

**Date:** 2026-09-07
**Status:** FORMULATION COMPLETE — OWNER SELECTION NOT YET PERFORMED
**Track:** Relational Research
**Source artifact:** `QUANTFORGE_RELATIONAL_MECHANISM_DISCOVERY_V1.md`

---

## 1. GOVERNING DOCTRINE

This formulation cycle operates under:

- V38 Doctrine (Hybrid Base + Conditional)
- Outcome-Blind Base Formulation Pathway (BF1–BF13)
- V38A Base Validation Pathway (BV1–BV13)
- Relational Research Framework V1 (inherited into V38)

**Hard constraints:**
- Base Registry remains EMPTY
- No historical economic performance is used to select, rank, or prioritize formulations
- No parameters are chosen from historical data
- No FB-001 economics inspected
- No F-01 economics inspected
- No protected-forward economics inspected
- No backtesting performed
- No optimization performed
- No closed research lines reopened
- No Conditional rescue layers introduced

---

## 2. PRIOR RELATIONAL KNOWLEDGE BOUNDARY

The following prior work defines the redundancy boundary:

| Prior work | Status | Redundancy boundary |
|------------|--------|-------------------|
| F-02 (two-index pairs) | FORMULATED — DEFERRED | Spread-reversion relative book. New formulations must not collapse into pair-spread trading. |
| F-03 (rank rotation) | FORMULATED — DEFERRED | Cross-sectional ranking allocation. New formulations must not collapse into relative-strength ranking. |
| SEED-002 | CLOSED — NEGATIVE | CAND-083 × CAND-081 relational test. No-rescue doctrine established. New formulations must not depend on CAND-083 as a precondition. |
| CAND-105 (lead-lag) | CLOSED — NEGATIVE | Gold/Tech M1 lead-lag. No significant timing asymmetry found. New formulations must not be simple lead-lag timing. |
| CAND-107 (vol co-movement) | CLOSED — REDUNDANT | Cross-asset vol correlation collapsed into vol regime family. New formulations must not be volatility correlation. |
| DISC-021 (mean reversion) | CLOSED — NON-VIABLE | Costs consume gross effect. New formulations must not be single-asset mean reversion. |
| DISC-022 (TSMOM) | CLOSED — NOT PROMOTABLE | Cross-era consistency failure. New formulations must not be time-series momentum. |

---

## 3. MECHANISM-TO-FORMULATION MAP

| Discovery mechanism | Formulation | Decision |
|--------------------|-------------|----------|
| REL-M01 (Confirmation Failure) | RF-001 | Formulated as standalone Base |
| REL-M02 (Synchrony Regime) | RF-002 | Formulated as standalone Base |
| REL-M03 (Shock Absorption) | RF-003 | Formulated as standalone Base |

All three discovery mechanisms survive initial screening. Each requires a genuinely different decision architecture.

---

## 4. DISTINCTNESS AUDIT

### RF-001 vs prior work

| Prior work | Structural difference |
|------------|----------------------|
| F-02 | F-02 trades the spread between two indices. RF-001 detects when one index fails to confirm another's structural event. The trigger is a discrete confirmation failure, not a continuous spread level. |
| F-03 | F-03 ranks indices by relative strength. RF-001 detects a specific event (confirmation failure) in a specific pair. No ranking occurs. |
| Mean Reversion | Mean reversion fades displacement toward a mean. RF-001 does not fade displacement — it detects when one market fails to confirm another's event. The trigger is the failure itself, not the level of prices. |
| TSMOM | TSMOM follows own-history trend. RF-001 is cross-market. The trigger is the relationship between two markets, not one market's history. |
| CAND-083 | CAND-083 is single-market cumulative rejection. RF-001 is cross-market confirmation failure. Different unit of analysis. |
| CAND-105 | CAND-105 tested whether lead-lag timing produces different downstream economics (a timing question). RF-001 detects when confirmation fails (an event question). Different mechanism. |

### RF-002 vs prior work

| Prior work | Structural difference |
|------------|----------------------|
| F-02 | F-02 trades a specific pair's spread. RF-002 measures joint directional synchrony across the index complex. Different unit of analysis. |
| F-03 | F-03 ranks by relative strength. RF-002 measures directional agreement. Strength and synchrony are different concepts. |
| CAND-107 | CAND-107 tested vol co-movement. RF-002 is not about volatility — it is about directional synchrony. Different measure. |
| Vol regime | Vol regime trades volatility level. RF-002 uses synchrony as a regime indicator. Different concept. |

### RF-003 vs prior work

| Prior work | Structural difference |
|------------|----------------------|
| Mean Reversion | Mean reversion fades displacement. RF-003 measures asymmetry in how different markets absorb the same shock. Different mechanism. |
| CAND-105 | CAND-105 tested timing. RF-003 tests absorption characteristics. Different concept. |
| Vol regime | Vol regime trades volatility level. RF-003 trades absorption asymmetry across markets. Different concept. |

**Distinctness verdict:** All three formulations survive the distinctness audit. No formulation collapses into prior closed work.

---

## 5. FORMULATION SPECIFICATIONS

---

### RF-001: CROSS-MARKET CONFIRMATION FAILURE

**Source mechanism:** REL-M01

**Title:** Cross-Market Confirmation Failure Process

**Behavioral mechanism (MECHANISTIC HYPOTHESIS):**
When a structurally significant price event occurs in one liquid US equity index, correlated indices typically confirm the move within a structurally defined window. The confirmation reflects shared participant flow, information propagation, and cross-market hedging behavior. When confirmation explicitly fails — the correlated index does not produce the expected confirming event within the expected window — the failure represents a distinct market-state transition. The non-confirming market has absorbed or rejected the information that drove the confirming market, suggesting a structural divergence in participant positioning, information processing, or liquidity conditions.

**Relational structure:**
- Primary market: USATECHIDXUSD (USTECm)
- Confirmation market: A second US equity index from the same complex (e.g., US500, US30, or another tech-heavy index)
- Relationship: Cross-market confirmation of structural price events
- Timeframe: M1 bars
- Session: US regular session (09:30–16:00 ET)

**Observable:**
The primary market produces a **structural event** defined as: the close of an M1 bar exceeds the highest high of the prior N completed M1 bars (for a bullish event) or falls below the lowest low of the prior N completed M1 bars (for a bearish event). N is a structural parameter defining the lookback horizon for "significant" — it is not optimized from data but rather defines what constitutes a structurally meaningful breakout.

The confirmation market is observed for the next M completed M1 bars. Confirmation is defined as: the close of any M1 bar in the confirmation market exceeds (for bullish) or falls below (for bearish) the confirmation market's own N-bar high/low within the M-bar window.

If the confirmation market does NOT produce the confirming event within M bars, a **confirmation failure** has occurred.

**Event:**
The confirmation failure event is the moment when M bars have elapsed since the primary market's structural event without the confirmation market producing a confirming event.

**Decision:**
When a confirmation failure is detected:
- If the primary market's event was bullish and the confirmation market failed to confirm: the confirmation market is in a structurally different state than the primary market. The decision is to fade the confirmation market's relative underperformance — i.e., take a short position in the confirmation market relative to the primary market.
- If the primary market's event was bearish and the confirmation market failed to confirm: the confirmation market is in a structurally different state. The decision is to fade the confirmation market's relative outperformance — i.e., take a long position in the confirmation market relative to the primary market.

The decision is made at the close of bar M+1 after the primary event (i.e., after the confirmation window closes).

**Entry execution:**
Entry at the open of bar M+2 (the bar after the decision bar). This ensures the decision is temporally causal — all information used for the decision is known before execution.

**Exit / invalidation:**
- Exit at the close of the session (16:00 ET) — this is a single-session position.
- Invalidation: if the primary market reverses its structural event (i.e., the primary market's close returns within the N-bar range before the position is entered), the opportunity is cancelled. No position is taken.

**Opportunity population:**
- One opportunity per structural event in the primary market.
- Maximum one position at a time.
- If multiple structural events occur in the same session, each is evaluated independently, but only one position may be open at any time.
- Structural events that occur in the last M bars of the session are excluded (insufficient time for confirmation window and entry).
- Duplicate structural events (same direction, same session, no intervening reversal) do not create new opportunities.

**Scope:**
- Instrument pair: USATECHIDXUSD + one confirmation index
- Timeframe: M1
- Session: US regular session (09:30–16:00 ET)
- Data domain: Forward-only prospective data from 2026-09-06 08:00 ET onward
- Calendar: Trading days only, no holiday adjustment needed (MT5 handles)

**Cost model:**
- Entry: 1 bps (market order at open)
- Exit: 1 bps (market order at session close)
- Total round-trip: 2 bps
- Applied mechanically to gross return

**Independence:**
This is a standalone Base process. It does not require another strategy for activation. The confirmation failure event is self-contained and self-triggering.

**Distinctness:**
Not F-02 (pairs spread), not F-03 (rank rotation), not mean reversion, not TSMOM, not CAND-083 (single-market), not CAND-105 (lead-lag timing). The mechanism is specifically about the failure of one market to confirm another market's structural event.

**Falsification route:**
If confirmation failures are random — i.e., the non-confirming market's subsequent session performance is statistically identical regardless of whether confirmation occurred — the mechanism is falsified.

**Specification risks:**
- N (lookback horizon) must be frozen at registration. Structural, not optimized.
- M (confirmation window) must be frozen at registration. Structural, not optimized.
- Confirmation market identity must be frozen at registration.
- The "structural event" definition (N-bar breakout) must not be changed after registration.

**Parameter risks:**
- Future researchers may be tempted to tune N and M to improve economics. These must be frozen as structural parameters at registration, not optimized.
- The confirmation market selection must not be changed to find a "better" pair.

**Data risks:**
- Requires M1 data for two indices with aligned timestamps. Available in forward pipeline.
- Market hours mismatch: both indices must trade the same session. US equity indices satisfy this.

**Redundancy risks:**
- If N is very small, the mechanism approaches noise. If N is very large, it approaches trend-following. The structural definition of N determines the mechanism's character.
- The confirmation window M must be large enough to allow a response but small enough to detect failure. Structural definition required.

**Registration readiness:**
`FORMULATION-COMPLETE BUT NOT REGISTRATION-READY`
N and M require structural specification before registration. The formulation is conceptually complete but the exact values must be frozen at registration time, not derived from data.

---

### RF-002: SYNCHRONY REGIME TRANSITION

**Source mechanism:** REL-M02

**Title:** Cross-Market Synchrony Regime Process

**Behavioral mechanism (MECHANISTIC HYPOTHESIS):**
Multiple liquid US equity indices normally move with high intraday synchrony — they advance and decline together because they share common participants, information, and macroeconomic exposure. When synchrony breaks down — one index moves materially while others do not, or indices move in opposite directions — the desynchronized state reflects a genuine difference in participant flow, information processing, or positioning between the indices. The synchrony breakdown is a state transition, not a continuous variable. The transition from synchronized to desynchronized represents a distinct market regime that may predict subsequent structural behavior in the desynchronized index.

**Relational structure:**
- Index complex: USATECHIDXUSD + at least one additional US equity index (e.g., US500)
- Relationship: Joint directional synchrony across the complex
- Timeframe: M1 bars
- Session: US regular session (09:30–16:00 ET)

**Observable:**
A **synchrony measure** is computed over a rolling window of W completed M1 bars. The synchrony measure is defined as the fraction of bars in the window where all indices in the complex move in the same direction (all positive returns or all negative returns). This is a directional agreement measure, not a correlation coefficient.

A **synchrony regime** is defined:
- **Synchronized:** the synchrony measure exceeds a threshold T (e.g., more than T% of bars show directional agreement)
- **Desynchronized:** the synchrony measure falls below the threshold T

The regime transition is the moment when the synchrony measure crosses from above T to below T.

**Event:**
The synchrony regime transition event is the first bar where the synchrony measure falls below T after having been above T.

**Decision:**
When a synchrony regime transition is detected:
- Identify which index in the complex is the **divergent** index — the index whose return direction differs from the majority of the complex in the most recent bar.
- The divergent index is in a structurally different state than the complex.
- The decision is to take a position against the divergent index's most recent direction — i.e., fade the divergence. If the divergent index moved up while the complex moved down, take a short position in the divergent index. If the divergent index moved down while the complex moved up, take a long position in the divergent index.

The decision is made at the close of the bar where the regime transition is detected.

**Entry execution:**
Entry at the open of the next bar. This ensures temporal causality.

**Exit / invalidation:**
- Exit at the close of the session (16:00 ET) — single-session position.
- Invalidation: if the synchrony measure returns above T before entry, the opportunity is cancelled. The regime transition was transient.

**Opportunity population:**
- One opportunity per synchrony regime transition.
- Maximum one position at a time.
- If the synchrony measure oscillates around T (multiple transitions in rapid succession), only the first transition creates an opportunity. Subsequent transitions within W bars are not new opportunities.
- Only transitions from synchronized to desynchronized are eligible. Transitions from desynchronized to synchronized are not opportunities (they represent regime normalization, not a trading signal).

**Scope:**
- Instrument complex: USATECHIDXUSD + one additional US equity index
- Timeframe: M1
- Session: US regular session (09:30–16:00 ET)
- Data domain: Forward-only prospective data from 2026-09-06 08:00 ET onward

**Cost model:**
- Entry: 1 bps
- Exit: 1 bps
- Total round-trip: 2 bps

**Independence:**
Standalone Base process. The synchrony regime transition is self-contained and self-triggering. No external strategy is needed.

**Distinctness:**
Not F-02 (pairs spread), not F-03 (rank rotation), not CAND-107 (vol co-movement), not vol regime trading. The mechanism is specifically about directional synchrony regime transitions in the index complex.

**Falsification route:**
If synchrony regime transitions are random — i.e., the divergent index's subsequent session performance is statistically identical regardless of whether a synchrony breakdown occurred — the mechanism is falsified.

**Specification risks:**
- W (window length) must be frozen at registration. Structural.
- T (synchrony threshold) must be frozen at registration. Structural.
- Index complex composition must be frozen at registration.
- The directional agreement measure must not be changed to a correlation coefficient or other statistical measure.

**Parameter risks:**
- W and T may be tempting to optimize. They must be frozen as structural parameters.
- The index complex composition must not be changed to find a "better" combination.

**Data risks:**
- Requires M1 data for multiple indices with aligned timestamps. Available.
- Both indices must trade the same session. US equity indices satisfy this.

**Redundancy risks:**
- If W is very short, the measure is noisy. If W is very long, regime transitions are rare. Structural definition required.
- The threshold T must distinguish genuine regime transitions from noise.

**Registration readiness:**
`FORMULATION-COMPLETE BUT NOT REGISTRATION-READY`
W and T require structural specification before registration. The formulation is conceptually complete.

---

### RF-003: CROSS-MARKET SHOCK ABSORPTION ASYMMETRY

**Source mechanism:** REL-M03

**Title:** Cross-Market Shock Absorption Asymmetry Process

**Behavioral mechanism (MECHANISTIC HYPOTHESIS):**
When an external-looking event affects multiple correlated markets simultaneously — such as a sudden large price move, a news-driven gap, or a volatility spike — the markets absorb the shock differently. One market may absorb the shock quickly (price stabilizes, returns to pre-shock levels), while another may absorb it slowly (price continues moving, overshoots, takes longer to stabilize). The asymmetry in absorption reflects a structural difference in participant composition, liquidity depth, or information processing between the markets. The absorption characteristics are observable and may predict the subsequent trajectory of the slow-absorbing market.

**Relational structure:**
- Index complex: USATECHIDXUSD + at least one additional US equity index
- Relationship: Asymmetric shock absorption across the complex
- Timeframe: M1 bars
- Session: US regular session (09:30–16:00 ET)

**Observable:**
A **shock** is detected when: the absolute return of the complex-wide average (mean return across all indices) over a single M1 bar exceeds a structural threshold S (in basis points). S defines what constitutes an "external-looking" shock — a large move affecting the entire complex simultaneously.

After a shock is detected, the **absorption characteristic** of each index is measured over the subsequent K bars. The absorption measure for each index is defined as: the sum of absolute signed returns over the K bars following the shock. A lower sum indicates faster absorption (the index stabilized quickly). A higher sum indicates slower absorption (the index continued moving).

The **absorption asymmetry** is the difference between the absorption measure of the slowest-absorbing index and the fastest-absorbing index.

If the absorption asymmetry exceeds a structural threshold A, a **shock absorption asymmetry event** has occurred.

**Event:**
The shock absorption asymmetry event is the moment when K bars have elapsed since the shock and the absorption asymmetry exceeds A.

**Decision:**
When a shock absorption asymmetry event is detected:
- The slow-absorbing index is in a structurally different state than the fast-absorbing index.
- The decision is to reduce exposure to the slow-absorbing index — i.e., take a position against the slow-absorbing index's post-shock direction. If the slow-absorbing index moved up after the shock (slow absorption of an upward shock), take a short position. If it moved down, take a long position.

The decision is made at the close of bar K after the shock.

**Entry execution:**
Entry at the open of the next bar. Temporal causality preserved.

**Exit / invalidation:**
- Exit at the close of the session (16:00 ET) — single-session position.
- Invalidation: if the absorption asymmetry falls below A before entry, the opportunity is cancelled.

**Opportunity population:**
- One opportunity per shock event.
- Maximum one position at a time.
- Shocks occurring in the last K bars of the session are excluded.
- Multiple shocks in the same session are independent if separated by at least K bars.

**Scope:**
- Instrument complex: USATECHIDXUSD + one additional US equity index
- Timeframe: M1
- Session: US regular session (09:30–16:00 ET)
- Data domain: Forward-only prospective data from 2026-09-06 08:00 ET onward

**Cost model:**
- Entry: 1 bps
- Exit: 1 bps
- Total round-trip: 2 bps

**Independence:**
Standalone Base process. The shock detection and absorption measurement are self-contained.

**Distinctness:**
Not mean reversion (which fades displacement), not CAND-105 (lead-lag timing), not vol regime (volatility level), not CAND-107 (vol co-movement). The mechanism is specifically about asymmetric absorption of the same shock across markets.

**Falsification route:**
If absorption asymmetry is random — i.e., the slow-absorbing index's subsequent performance is statistically identical to the fast-absorbing index's performance — the mechanism is falsified.

**Specification risks:**
- S (shock threshold) must be frozen at registration. Structural.
- K (absorption window) must be frozen at registration. Structural.
- A (asymmetry threshold) must be frozen at registration. Structural.
- Index complex composition must be frozen.

**Parameter risks:**
- S, K, and A may be tempting to optimize. They must be frozen as structural parameters.

**Data risks:**
- Requires M1 data for multiple indices. Available.
- Shock detection depends on S being set appropriately — too low generates too many shocks, too high generates too few.

**Redundancy risks:**
- If S is very low, every small move is a "shock." If S is very high, shocks are rare. Structural definition required.
- The absorption measure must not be confused with volatility — it is about the path of returns after a shock, not the level of volatility.

**Registration readiness:**
`FORMULATION-COMPLETE BUT NOT REGISTRATION-READY`
S, K, and A require structural specification before registration. The formulation is conceptually complete.

---

## 6. TEMPORAL INTEGRITY

### RF-001

| Step | Information known | When |
|------|------------------|------|
| Primary event detection | N-bar high/low exceeded | At close of event bar |
| Confirmation window | M bars observed | Bars M+1 through M after event |
| Decision | Confirmation failure confirmed | At close of bar M+1 |
| Entry | Position taken | At open of bar M+2 |
| Exit | Position closed | At close of session |

All information used for the decision is known before execution. No future information influences the decision.

### RF-002

| Step | Information known | When |
|------|------------------|------|
| Synchrony measure | W-bar directional agreement | At close of each bar |
| Regime transition | Synchrony falls below T | At close of transition bar |
| Decision | Divergent index identified | At close of transition bar |
| Entry | Position taken | At open of next bar |
| Exit | Position closed | At close of session |

All information used for the decision is known before execution.

### RF-003

| Step | Information known | When |
|------|------------------|------|
| Shock detection | Complex return exceeds S | At close of shock bar |
| Absorption measurement | K bars observed | Bars 1 through K after shock |
| Decision | Asymmetry exceeds A | At close of bar K |
| Entry | Position taken | At open of bar K+1 |
| Exit | Position closed | At close of session |

All information used for the decision is known before execution.

---

## 7. OPPORTUNITY POPULATION

### RF-001

| Criterion | Definition |
|-----------|-----------|
| Opportunity exists when | Primary market produces N-bar breakout AND confirmation window closes without confirmation AND session has sufficient remaining time for entry |
| No opportunity when | No N-bar breakout occurs, OR confirmation occurs within M bars, OR breakout occurs in last M bars of session, OR position is already open |
| Maximum per session | One position at a time. Multiple breakouts evaluated independently but only one position open. |
| After first decision | Decision is made. If opportunity cancelled (primary reverses), no position taken. |
| Recurrence | Same-direction breakouts without intervening reversal do not create new opportunities. |
| Duplicates | Treated as continuation of existing opportunity, not new. |

### RF-002

| Criterion | Definition |
|-----------|-----------|
| Opportunity exists when | Synchrony measure falls below T (transition from synchronized to desynchronized) AND session has sufficient remaining time |
| No opportunity when | Synchrony is already below T, OR transition occurs in last bar of session, OR position is already open from prior transition |
| Maximum per session | One position at a time. |
| After first decision | Decision is made. |
| Recurrence | Transitions within W bars of prior transition are not new opportunities (oscillation control). |
| Duplicates | Treated as continuation, not new. |

### RF-003

| Criterion | Definition |
|-----------|-----------|
| Opportunity exists when | Shock detected (complex return > S) AND K bars later asymmetry > A AND session has sufficient remaining time |
| No opportunity when | No shock, OR asymmetry < A after K bars, OR shock in last K bars of session, OR position already open |
| Maximum per session | One position at a time. |
| After first decision | Decision is made. |
| Recurrence | Multiple shocks separated by ≥ K bars are independent. |
| Duplicates | Treated independently if separated by ≥ K bars. |

---

## 8. EXECUTION MODEL

All three formulations share the same execution model:

- **Order concept:** Market order at open of execution bar
- **Signal timing:** At close of decision bar (all information known)
- **Execution timing:** At open of next bar (temporal causality preserved)
- **Position state:** Flat or one position (no pyramiding)
- **Overlap rules:** One position at a time. If a new opportunity arises while a position is open, the existing position is held to session close. No new position is opened.
- **Exit execution:** Market order at close of session (16:00 ET)

---

## 9. COST MODEL

All three formulations share the same cost model:

- Entry: 1 bps (market order slippage + commission)
- Exit: 1 bps (market order slippage + commission)
- Total round-trip: 2 bps
- Applied mechanically to gross return
- No cost optimization
- No cost tuning

---

## 10. STANDALONE-BASE ASSESSMENT

| Formulation | Standalone? | Conditional dependence? |
|-------------|------------|------------------------|
| RF-001 | YES | NO — confirmation failure is self-triggering |
| RF-002 | YES | NO — synchrony regime transition is self-triggering |
| RF-003 | YES | NO — shock absorption asymmetry is self-triggering |

All three formulations are capable of standing independently as Base processes.

---

## 11. FALSIFICATION ROUTES

| Formulation | Primary falsification |
|-------------|----------------------|
| RF-001 | Non-confirming market's session performance is statistically identical regardless of confirmation status |
| RF-002 | Divergent index's session performance is statistically identical regardless of synchrony regime |
| RF-003 | Slow-absorbing index's session performance is statistically identical to fast-absorbing index's performance |

---

## 12. SPECIFICATION-RISK AUDIT

| Formulation | Specification risks | Mitigation |
|-------------|-------------------|------------|
| RF-001 | N, M, confirmation market identity | Frozen at registration. No post-registration modification. |
| RF-002 | W, T, index complex composition | Frozen at registration. No post-registration modification. |
| RF-003 | S, K, A, index complex composition | Frozen at registration. No post-registration modification. |

All formulations have the same structural risk: parameters must be frozen at registration, not optimized from data. The V38A registration freeze mechanism (Section 10 of BV1) provides the governance protection.

---

## 13. REGISTRATION-READINESS ASSESSMENT

| Formulation | Status | Reason |
|-------------|--------|--------|
| RF-001 | FORMULATION-COMPLETE BUT NOT REGISTRATION-READY | N, M, and confirmation market require structural specification at registration time |
| RF-002 | FORMULATION-COMPLETE BUT NOT REGISTRATION-READY | W, T, and index complex require structural specification at registration time |
| RF-003 | FORMULATION-COMPLETE BUT NOT REGISTRATION-READY | S, K, A, and index complex require structural specification at registration time |

None of the formulations are registration-ready. All require structural parameter specification before V38A registration can proceed. This is by design — the formulation cycle defines the mechanism and architecture; the registration cycle freezes the exact parameters.

---

## 14. OWNER-SELECTION BOUNDARY

This artifact does NOT:

- Select a winner
- Declare any formulation "SELECTED FOR V38A"
- Rank formulations by expected performance
- Authorize V38A registration
- Perform economic testing
- Compare candidate economics

The final deliverable is a set of three formulations that can be presented to the owner for a separate governed selection decision under BS1–BS13.

The owner may:
- Authorize one or more formulations for V38A registration
- Defer all formulations for further refinement
- Reject formulations that do not meet the owner's quality standard
- Request a different selection review

---

## 15. EXPLICIT NO-ECONOMIC-TESTING STATEMENT

**No economic testing was performed in this formulation cycle.**

- No backtesting
- No historical return calculation
- No P&L computation
- No expectancy calculation
- No win rate calculation
- No Sharpe ratio calculation
- No drawdown calculation
- No profit factor calculation
- No cumulative return calculation
- No benchmark comparison
- No FB-001 economics inspected
- No F-01 economics inspected
- No protected-forward economics inspected
- No parameter optimization
- No favorable-period selection
- No favorable-instrument selection

The owner must be able to evaluate these formulations without being shown performance results.

---

**END OF FORMULATION ARTIFACT**
