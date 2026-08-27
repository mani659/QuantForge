# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V15
# COUNTERFACTUAL-DISCRIMINATING ECONOMIC MECHANISMS
# DATE: 2026-08-26

## 1. Research Factory V2 Context
V14 screening proved that relying on standalone profitability is dangerous if the counterfactual condition is also highly profitable (e.g., CAND-042). A profitable treatment event does not validate a causal mechanism if the control event behaves identically. V15 pivots the pipeline to strictly demand **discriminating counterfactuals**—mechanisms where the presence of a specific economic constraint causes a testable market response, and the explicit absence of that constraint yields a materially different outcome.

## 2. V15 Objective
To discover tradeable artifacts governed by mechanisms with genuine discriminatory power. V15 rejects candidates that merely ask "Does event X predict a move?" and instead requires:
> "MECHANISM PRESENT → RESPONSE A" versus "MECHANISM ABSENT → RESPONSE B"

## 3. Lessons Applied
- **V14 Counterfactual Lesson:** A massive edge in the treatment group is scientifically invalid if the counterfactual group shares the exact same edge. V15 counterfactuals are explicitly designed to capture the exact same price action *without* the underlying structural constraint.
- **V14 Component Governance Lesson:** Candidates with strong per-event economics but untestable causal narratives are relegated to Component-Candidates rather than Qualified System Components. V15 focuses on mechanisms observable strictly through price and cross-asset relationships.

## 4. Mechanism Families
- **FAMILY E:** Event Failure / Confirmation (Trapped institutional flow)
- **FAMILY C:** Cross-Market Confirmation (Macro risk-off sponsorship)
- **FAMILY F:** Reference / Anchor Repricing (Cost-basis capitulation)

---

## 5. Candidates Considered

### CAND-G0-044
**Name:** Initial Balance Trap Liquidation
**Mechanism Family:** E — Event Failure / Confirmation
**Economic Constraint:** Trapped directional institutional flow and forced liquidation.
**Mechanistic Explanation:** The First Hour (09:30-10:30 ET) establishes the "Initial Balance" where institutional flow commits to a daily direction. If the first hour creates a massive directional trend, trend-following capital commits heavily. If the market then violently reverses and breaks the absolute extreme (high/low) of that first hour, the original institutional premise has structurally failed. The trapped participants are forced to liquidate, accelerating the reversal.
**Repeatable Event:** Between 09:30 and 10:30 ET, the price trend is > +1.0% (or < -1.0%). Between 10:30 and 15:00, the price breaks the 09:30-10:30 Low (for an uptrend) or High (for a downtrend).
**Information State:** A dominant morning trend has structurally failed, trapping momentum capital.
**Predicted Direction:** Continuation of the reversal (e.g., Short if morning was up).
**Executable Entry:** The exact minute the Initial Balance extreme is broken (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated continuously intraday; single trigger per day.
**Positive-Expectancy Thesis:** The breakdown is driven by forced selling (stop losses of trapped longs). Forced selling is price-insensitive, creating rapid, asymmetrical continuation in the direction of the failure.
**Adverse-Risk Structure:** A false breakdown is possible, but the massive preceding trend ensures a large pool of liquidity exists to be triggered.
**Primary Counterfactual:** The 09:30-10:30 ET range is tight (return between -0.2% and +0.2%). The price later breaks the morning extreme.
**Expected Counterfactual Difference:** Breaking a massive 1% range traps massive capital, causing violent continuation. Breaking a tight 0.2% range traps nobody, resulting in noise and chop.
**Falsification Condition:** Reversal continuation is identical regardless of the size of the morning trend.
**Expected Frequency:** Low to Moderate (~15-30 opps/year).
**Intended Component Role:** EVENT OPPORTUNIST / REGIME SPECIALIST.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Replaces simple trend continuations (CAND-043) with trend *failures*.
**G0 Decision:** PROMOTE

### CAND-G0-045
**Name:** Safe-Haven Confirmed Risk-Off
**Mechanism Family:** C — Cross-Market Confirmation
**Economic Constraint:** Structural macro capital flight.
**Mechanistic Explanation:** A genuine, systemic risk-off panic requires capital to flee equities and seek safety in Gold (or Treasuries). If Equities crash violently but Gold does NOT rally, the equity selloff lacks structural macro sponsorship (it may be a liquidity shock, tech-specific sector rotation, or dollar strength). A confirmed flight-to-safety indicates persistent institutional selling that is unlikely to mean-revert intraday.
**Repeatable Event:** At 11:30 ET, USATECHIDXUSD is DOWN > -1.0% from the 09:30 Open, AND XAUUSD is UP > +0.5% from the 09:30 Open.
**Information State:** A structural, cross-asset risk-off panic is confirmed in progress.
**Predicted Direction:** Continuation (Short USATECHIDXUSD).
**Executable Entry:** 11:30 ET (Market Short).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated once daily at 11:30 ET.
**Positive-Expectancy Thesis:** Macro panic selling is institutional and persistent. Value-buyers step away when safe-havens confirm the panic, allowing the selloff to grind continuously into the close without major mean-reverting resistance.
**Adverse-Risk Structure:** Shorting after a 1% drop is dangerous if the drop is localized. By requiring Gold confirmation, we filter out localized drops that are highly prone to afternoon mean-reversion.
**Primary Counterfactual:** At 11:30 ET, USATECH is DOWN > -1.0%, but XAUUSD is DOWN or FLAT (<= 0.0%).
**Expected Counterfactual Difference:** Confirmed panics (Gold up) trend relentlessly lower. Unconfirmed panics (Gold down/flat) suffer violent afternoon mean-reversion as value-buyers step in.
**Falsification Condition:** Unconfirmed equity crashes trend downward just as persistently as confirmed crashes.
**Expected Frequency:** Low (~10-20 opps/year).
**Intended Component Role:** REGIME SPECIALIST.
**Data Required:** M1 USATECHIDXUSD, M1 XAUUSD.
**Cross-Market Scope:** Dual asset.
**Closed-Line Independence:** Entirely independent. Contrasts with CAND-042 (which traded the unconfirmed/correlated crash).
**G0 Decision:** PROMOTE

### CAND-G0-046
**Name:** Opening Print Capitulation Pivot
**Mechanism Family:** F — Reference / Anchor Repricing
**Economic Constraint:** Institutional cost-basis anchoring.
**Mechanistic Explanation:** The 09:30 ET Opening Print handles the largest volume of the day, acting as the ultimate anchor for daily institutional cost basis. When price extends far from the open, it builds inventory in that direction. If price later completely retraces to touch the exact 09:30 Opening Print, the entire morning inventory is now underwater or scratched. This critical reference level acts as a structural pivot, triggering mass capitulation.
**Repeatable Event:** Between 09:30 and 11:30, price extends > +1.0% (or < -1.0%) away from the 09:30 Open price. Then, between 11:30 and 15:00, price completely retraces to touch the exact 09:30 Open price.
**Information State:** The entire morning trend inventory has just been pushed to breakeven/loss at the highest-volume anchor point of the day.
**Predicted Direction:** Continuation of the retracement (e.g., Short if morning was up).
**Executable Entry:** The exact minute the 09:30 Open price is touched (Market).
**Deterministic Exit:** 16:00 ET (Market).
**Opportunity Integrity:** Evaluated continuously intraday; single trigger per day.
**Positive-Expectancy Thesis:** The Opening Print is a highly visible technical and structural pivot. Crossing it after a massive excursion triggers stop-loss cascades from morning participants, causing price to slice through the Open with momentum.
**Adverse-Risk Structure:** A false cross is possible, but institutional algorithms are highly sensitive to daily VWAP/Open crosses, providing immediate directional pressure.
**Primary Counterfactual:** The morning excursion (09:30-11:30) never exceeds 0.3% from the Open. Price then crosses the Open during the afternoon.
**Expected Counterfactual Difference:** Crossing the Open after a 1% excursion triggers capitulation and momentum. Crossing the Open after a 0.3% chop triggers nothing, resulting in mean-reversion around the Open.
**Falsification Condition:** The post-cross behavior is identical regardless of the size of the preceding excursion.
**Expected Frequency:** Low to Moderate (~15-25 opps/year).
**Intended Component Role:** SESSION COMPONENT / EVENT OPPORTUNIST.
**Data Required:** M1 USATECHIDXUSD.
**Cross-Market Scope:** Single asset.
**Closed-Line Independence:** Independent focus on the Opening Print reference level and inventory capitulation.
**G0 Decision:** PROMOTE

---

## 6. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 7. Promoted Candidates
- **CAND-G0-044:** Initial Balance Trap Liquidation
- **CAND-G0-045:** Safe-Haven Confirmed Risk-Off
- **CAND-G0-046:** Opening Print Capitulation Pivot

## 8. Killed Candidates
None.

## 9. Blocked Candidates
None.

## 10. Counterfactual Quality
All three candidates explicitly possess counterfactuals that isolate the mechanism constraint:
- **CAND-044:** Range breaks with vs. without massive trapped institutional flow.
- **CAND-045:** Equity selloffs with vs. without structural safe-haven confirmation.
- **CAND-046:** Opening print crosses with vs. without massive accumulated underwater inventory.

## 11. Mechanism Diversity
The candidates cover Event Failure Constraints (E), Cross-Market Confirmation (C), and Anchor/Reference Repricing (F).

## 12. Component Potential
These artifacts specifically target regime shifts and capitulation events, making them highly suited for Event Opportunist or Regime Specialist roles within a diversified system.

## 13. Ranked Candidates
1. **CAND-045:** Cross-market confirmation provides the most objective, untamperable evidence of structural macro involvement.
2. **CAND-044:** Trapped institutional flow is a core, highly robust market microstructure mechanism.
3. **CAND-046:** Cost-basis anchoring at the Opening Print is structurally sound, though vulnerable to exact-tick noise.

## 14. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-044, CAND-045, CAND-046)

## 15. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. All proposed constraints utilize currently available, verifiable M1 data.
