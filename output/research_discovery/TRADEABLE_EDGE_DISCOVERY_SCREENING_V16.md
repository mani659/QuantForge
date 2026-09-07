# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V16
# DATE: 2026-08-27

## 1. Research Factory Context
The Command Alignment and Research Track Reconciliation V1 confirmed that V15 is closed and the factory is authorized to resume G0 Candidate Generation. The CAND-015 protected forward-validation track remains active. The V16 cycle adheres strictly to the V15 Counterfactual Superiority Doctrine: a mechanism is only valid if it actively adds value relative to its exact counterfactual.

## 2. V16 Objective
To discover a small number of genuinely distinct research artifacts driven by objective economic constraints. The focus is on behaviors where the presence of the constraint predictably changes the economic distribution, yielding positive expectancy that cannot be explained by a generic unconstrained event.

## 3. Lessons Applied
- **Counterfactual Superiority:** A profitable treatment is not a valid mechanism if its counterfactual is superior. All candidates must have a clearly defined, testable counterfactual.
- **Economic Constraints:** generic price patterns are rejected in favor of mechanisms anchored in structural market realities (e.g., fixing windows, macro data releases, cross-market information diffusion).

## 4. Discovery Principles
- The constraint must be observable prior to entry.
- The entry must be fully executable.
- The exit must be deterministic.
- The data required must be currently feasible (M1).

## 5. Mechanism Families
- **FAMILY A:** Settlement / Reference Price Constraints (Fixing-Window Liquidity Transfer)
- **FAMILY G:** Information Arrival / Sequential Repricing (Sequential Macro-Release Dislocation)
- **FAMILY D:** Cross-Market Constraints (Cross-Market Lead-Lag Asymmetry)

## 6. Candidates Considered

### CAND-G0-047
**Name:** Fixing-Window Liquidity Transfer
**Mechanism Family:** A — Settlement / Reference Price Constraints
**Economic Constraint:** Institutional necessity to flatten intraday risk and execute massive notional volume into the official fixing/closing window.
**Mechanistic Explanation:** Institutional dealers often warehouse risk during a strong intraday trend but must aggressively flatten their books as the end-of-day fixing window approaches to avoid overnight exposure. If a massive trend exhausts just prior to the final hour, the subsequent reversal is driven by price-insensitive dealer liquidation targeting the official close.
**Repeatable Event:** At exactly 14:45 ET, the price trend from the 09:30 open is > +1.0% (a large directional imbalance). At 15:00 ET (the start of the final hour), the price reverses sharply, dropping > 0.3% within 15 minutes.
**Information State:** The dominant trend has exhausted just prior to a major settlement window, and dealers are unloading accumulated inventory.
**Predicted Post-Entry Behavior:** Continuation of the reversal into the close (Short).
**Executable Entry:** 15:15 ET (Market).
**Deterministic Exit:** 16:00 ET (Market, official close).
**Opportunity Integrity:** Evaluated once daily at 15:15 ET. Single trigger per day.
**Positive-Expectancy Thesis:** Dealers flattening their books before the close are price-insensitive. Unwinding a massive day's trend inventory creates a structural liquidation wave that persists exactly until the closing bell.
**Adverse-Risk Structure:** If the initial 15-minute drop is just noise, the original trend will resume. Requiring a large morning imbalance ensures there is massive inventory to unwind.
**Primary Counterfactual:** At 14:45 ET, the price trend from 09:30 is tight (between -0.3% and +0.3%). At 15:00 ET, price drops > 0.3% within 15 minutes.
**Expected Counterfactual Difference:** Without a massive prior imbalance, dealers have no large inventory to unwind into the close. The drop into the fixing window is just noise and will likely mean-revert.
**Falsification Condition:** The 15:15-16:00 trend is identical regardless of the size of the 09:30-14:45 imbalance.
**Expected Frequency:** Moderate (~20-40 opps/year).
**Intended Component Role:** SESSION COMPONENT.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Focuses on institutional dealer flattening into the close (a fixing constraint) rather than generic afternoon momentum or European close (CAND-043).
**G0 Decision:** PROMOTE

### CAND-G0-048
**Name:** Sequential Macro-Release Dislocation
**Mechanism Family:** G — Information Arrival / Sequential Repricing
**Economic Constraint:** Multi-stage information processing where a macro data release anchors the market in one direction, but the subsequent cash open completely rejects that anchor.
**Mechanistic Explanation:** A major macro data release (e.g., 08:30 ET) causes a massive pre-market move. If the 09:30 ET Cash Open fails to sustain the move and completely retraces to the pre-release level, the initial macro reaction was fundamentally "wrong" or trapped weak liquidity. Cash market participants (with true institutional size) are repricing the information in the opposite direction.
**Repeatable Event:** Between 08:30 ET and 09:30 ET, price moves > +1.0%. Between 09:30 ET and 11:30 ET, price fully retraces to touch the exact 08:30 ET pre-release level.
**Information State:** The initial macro-shock consensus has been completely invalidated by cash-session institutional flow.
**Predicted Post-Entry Behavior:** Continuation of the retracement (Short).
**Executable Entry:** The exact minute the 08:30 ET level is touched (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated continuously between 09:30 and 11:30 ET. Single trigger per day.
**Positive-Expectancy Thesis:** The complete rejection of a 1% macro move by cash participants means the true institutional consensus opposes the initial reaction. The breakdown below the pre-release level triggers stop-losses from those who bought the macro headline, causing asymmetrical continuation.
**Adverse-Risk Structure:** Retracing a macro move requires massive volume. By the time it fully retraces, the opposing momentum is undeniable.
**Primary Counterfactual:** Between 08:30 ET and 09:30 ET, price moves < 0.2% (no macro shock). Between 09:30 ET and 11:30 ET, price drops 1.0% to touch the 08:30 ET level.
**Expected Counterfactual Difference:** Without a macro shock to trap participants, crossing the 08:30 level has no structural meaning and likely results in mean-reversion.
**Falsification Condition:** The post-cross continuation is identical regardless of whether a massive macro shock occurred at 08:30 ET.
**Expected Frequency:** Low (~10-20 opps/year).
**Intended Component Role:** EVENT OPPORTUNIST.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Focuses specifically on the 08:30 macro release window and cash-open rejection, distinct from generic intraday reversals or opening print crosses (CAND-046).
**G0 Decision:** PROMOTE

### CAND-G0-049
**Name:** Cross-Market Lead-Lag Asymmetry
**Mechanism Family:** D — Cross-Market Constraints
**Economic Constraint:** Information diffusion delay between highly correlated but structurally different assets.
**Mechanistic Explanation:** Gold (XAU) is the primary macroeconomic safe haven. Silver (XAG) is a secondary hybrid. During a massive macro shock, Gold moves first and absorbs primary institutional flow. Silver should theoretically follow. If Gold experiences a massive directional shock but Silver remains completely flat over the same window, an information arbitrage exists. Silver must eventually "catch up" to restore the structural ratio, or Gold must revert.
**Repeatable Event:** Between 09:30 ET and 10:30 ET, XAUUSD moves > +1.0%. Over the exact same window, XAGUSD moves between -0.2% and +0.2% (flat).
**Information State:** A massive pricing dislocation exists between primary and secondary correlated assets.
**Predicted Post-Entry Behavior:** XAGUSD breaks out to catch up to XAUUSD (Long XAGUSD).
**Executable Entry:** 10:30 ET (Market Long XAGUSD).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 10:30 ET.
**Positive-Expectancy Thesis:** Arbitrageurs and secondary flow will eventually force Silver to re-price to match the new macro regime established by Gold. The delayed reaction provides a low-risk entry before the catch-up momentum begins.
**Adverse-Risk Structure:** Silver's flat response might indicate a genuine divergence (e.g., industrial weakness vs monetary fear). However, extreme 1% gold shocks usually overwhelm industrial micro-factors.
**Primary Counterfactual:** Between 09:30 ET and 10:30 ET, XAUUSD moves < 0.3% (no shock). Over the same window, XAGUSD remains flat.
**Expected Counterfactual Difference:** Without a Gold shock, Silver remaining flat is just normal market noise, and taking a position has zero expectancy. With a Gold shock, Silver is mispriced.
**Falsification Condition:** Silver's 10:30-16:00 return distribution is identical whether Gold shocked > 1% or remained flat.
**Expected Frequency:** Low (~10-25 opps/year).
**Intended Component Role:** CROSS-MARKET COMPONENT / EVENT OPPORTUNIST.
**Data Required:** M1 XAUUSD, M1 XAGUSD.
**Cross-Market Scope:** Dual asset.
**Closed-Line Independence:** Relies on lead-lag correlation delay (information diffusion) rather than concurrent liquidity breakdowns (CAND-042).
**G0 Decision:** PROMOTE

## 7. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 8. Promoted Candidates
- **CAND-047:** Fixing-Window Liquidity Transfer
- **CAND-048:** Sequential Macro-Release Dislocation
- **CAND-049:** Cross-Market Lead-Lag Asymmetry

## 9. Killed Candidates
None.

## 10. Blocked Candidates
None.

## 11. Counterfactual Quality
All three candidates possess highly specific, structurally constrained counterfactuals:
- **CAND-047:** 15:00 drop with vs. without massive accumulated morning imbalance.
- **CAND-048:** 08:30 level cross with vs. without massive 08:30 macro shock.
- **CAND-049:** Silver flat with vs. without a concurrent massive Gold shock.

## 12. Mechanism Diversity
The candidates cover Settlement/Reference Price Constraints (A), Information Arrival/Sequential Repricing (G), and Cross-Market Constraints (D).

## 13. Component Potential
All three are specifically designed as specialized component artifacts. CAND-047 targets specific intraday structural handoffs (Session Component). CAND-048 and CAND-049 target rare structural dislocations (Event Opportunist / Cross-Market).

## 14. Ranked Candidates
1. **CAND-049 (Cross-Market Lead-Lag Asymmetry):** The most objectively constrained mechanism, relying on proven cross-asset fundamentals and information diffusion delay.
2. **CAND-048 (Sequential Macro-Release Dislocation):** Powerful behavioral trap mechanism anchored to objective scheduled macro data releases.
3. **CAND-047 (Fixing-Window Liquidity Transfer):** Structurally sound end-of-day mechanics, though reliant on fixing-window dealer behavior which can be noisy.

## 15. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-047, CAND-048, CAND-049)

## 16. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. All proposed constraints utilize currently available, verifiable M1 data. System Assembly was not performed.
