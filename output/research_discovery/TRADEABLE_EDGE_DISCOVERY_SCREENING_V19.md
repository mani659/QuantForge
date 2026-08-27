# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V19
# DATE: 2026-08-27

## 1. Research Factory Context
Following the formalization of the Dual-Path Strategy and System Governance doctrine, the Research Factory recognizes two legitimate outcomes: finding a single standalone killer strategy (Path A) or discovering independently valid mechanisms that can be assembled into a robust system (Path B). A candidate that fails as a standalone strategy may still qualify as a component, provided its underlying mechanism is scientifically/economically valid and not merely a statistical accident or inferior to its counterfactual.

## 2. V19 Objective
Discover 3–5 genuinely independent mechanism candidates where the explicitly observable condition changes the post-entry return distribution for a clear economic reason. The goal is to find the intersection of: Counterfactual Superiority, Positive Net Expectancy, Meaningful Economic Headroom, Adequate Observability, and Sufficient Opportunity Frequency.

## 3. Lessons from V10–V18
- **Problem 1 (CAND-055):** A profitable event failed because the specific condition degraded the counterfactual.
- **Problem 2 (CAND-052):** A condition successfully added information (Treatment > Counterfactual) but absolute expectancy was flat (+0.01 bps).
- **Problem 3 (CAND-051):** A mechanism was logically sound but yielded practically zero frequency (N=1).
- **Problem 4 (CAND-050):** A causal story sounded convincing (retail stop runs) but the actual mechanism wasn't observable and failed the counterfactual gate.

## 4. Dual-Path Implication
Candidates in V19 must be evaluated on both Standalone Potential (can this run the bot alone?) and Component Potential (can this contribute unique expectancy to a modular system?). We do not deliberately weaken standalone candidates to make them combinable.

## 5. SMC Structural-State Translation
V19 deliberately translates Smart Money Concepts (SMC) principles into observable price state transitions rather than unobservable causal narratives (like "institutional sponsorship"). We evaluate structural phenomena—Sweep, Structural Shift, Retest, Freshness—as purely objective mathematical states.

## 6. Mechanism Families
- **FAMILY A:** Structural State Transitions (Sweep → Shift → Retest)
- **FAMILY B:** Economic Reference / Anchor (Friday Close / Weekly Open)
- **FAMILY D:** Sequential Information Arrival (Expansion → Pullback Trap)

## 7. Candidates Considered

### CAND-G0-056
**Name:** Post-Sweep Structural Shift Confirmation
**Mechanism Family:** A — Structural State Transitions
**Observable Mechanism Variable:** A confirmed sweep of the prior session's extreme (High/Low) followed immediately by a structural break (closing past the most recent local 5-minute swing pivot in the opposite direction).
**Economic Constraint:** A sweep of a liquidity reference traps breakout traders. However, a sweep alone is just a momentary extreme. The subsequent structural shift explicitly confirms that the opposing flow possesses sufficient aggression to break the local trend regime.
**Mechanistic Explanation:** Breakout traders buy the high. When price reverses and immediately breaks a local structural low, the breakout capital is trapped, and the opposing flow has established control. The resulting retest of the broken structure provides a highly asymmetric entry.
**Repeatable Event:** Price pierces the Prior Day High (PDH), reverses, and within 30 minutes closes below the most recent 5-minute swing low that preceded the high. Price then returns to retest the broken swing low.
**Information State:** A liquidity pool was swept AND structural momentum has verifiably reversed.
**Predicted Post-Entry Behavior:** Immediate, energetic continuation away from the swept level.
**Executable Entry:** Limit order at the broken swing low upon first retest.
**Deterministic Exit:** 16:00 ET or End of Session.
**Opportunity Integrity:** First occurrence per day.
**Positive-Expectancy Thesis:** The structural shift confirms the reversal is genuine, protecting against trending days where the PDH is just a momentary pause.
**Economic Headroom:** Structural reversals from session extremes often yield 50-150 bps intraday.
**Adverse-Risk Structure:** A massive trend could ignore the local structural break.
**Primary Counterfactual:** Price sweeps the PDH and reverses to the entry point, but WITHOUT having broken the local swing low first (no structural shift confirmation).
**Expected Treatment Superiority:** A sweep with a structural shift has confirmed regime change. A sweep without it is fighting an intact trend.
**Falsification Condition:** Reversals with a structural shift perform identically to or worse than reversals without the structural shift.
**Expected Frequency:** Moderate (~40-60 opps/year).
**Data Required:** M1 USATECHIDXUSD.
**Intended Standalone Role:** CORE.
**Intended Component Role:** CORE COMPONENT / REGIME SPECIALIST.
**Closed-Line Independence:** This improves upon CAND-050 (PDH Sweep) by adding the strict SMC requirement of a Structural Shift confirmation.
**G0 Decision:** PROMOTE

### CAND-G0-057
**Name:** Weekly Opening Gap Fade Exhaustion
**Mechanism Family:** B — Economic Reference / Anchor
**Observable Mechanism Variable:** The market opens on Sunday/Monday with a >0.2% gap. Price attempts to close the gap, touches the exact Friday Close reference (within 0.05%), and immediately reverses to break the Monday Open price.
**Economic Constraint:** The Friday Close is the ultimate weekly reference anchor. A gap open traps weekend flow. The attempt to close the gap represents the exhaustion of weekend rebalancing. The exact touch of the Friday Close "seals" the gap, and the subsequent break of the Monday Open confirms the new week's structural direction has begun.
**Mechanistic Explanation:** When the gap is sealed, mean-reversion algorithms exit their gap-fade trades, withdrawing liquidity. The break of the Monday Open triggers directional momentum capital.
**Repeatable Event:** Monday Open gap > 0.2%. Price touches within 0.05% of Friday Close. Price reverses and crosses the Monday Open price.
**Information State:** Weekend gap closed; mean-reversion flow exhausted; new directional regime initiated.
**Predicted Post-Entry Behavior:** Trend continuation in the direction of the initial Monday Open break.
**Executable Entry:** Market order on the close of the 1-minute bar that crosses the Monday Open (after the gap is sealed).
**Deterministic Exit:** End of Monday session.
**Opportunity Integrity:** One trigger per week maximum.
**Positive-Expectancy Thesis:** The sequence explicitly traps gap-fade traders and triggers momentum capital precisely at the exhaustion point of the pullback.
**Economic Headroom:** Monday trends after gap closures frequently exceed 40-80 bps.
**Adverse-Risk Structure:** The market could just chop around the open.
**Primary Counterfactual:** The market opens with a >0.2% gap, pulls back arbitrarily (does NOT reach within 0.05% of Friday close), and breaks the Monday open.
**Expected Treatment Superiority:** Touching the exact Friday Close exhausts the structural gap-fade flow. An arbitrary pullback leaves the gap "unsealed", leaving structural gravity below.
**Falsification Condition:** Unsealed gap trends perform identically to or better than sealed gap trends.
**Expected Frequency:** Low to Moderate (~15-25 opps/year).
**Data Required:** M1 USATECHIDXUSD.
**Intended Standalone Role:** SPECIALIST.
**Intended Component Role:** EVENT OPPORTUNIST.
**Closed-Line Independence:** Entirely new weekly transition anchor, untouched by V10-V18 intraday work.
**G0 Decision:** PROMOTE

### CAND-G0-058
**Name:** Large-Range Expansion First Pullback Trap
**Mechanism Family:** D — Sequential Information Arrival
**Observable Mechanism Variable:** A rapid 60-minute expansion > 1.0% with no 5-minute bar closing against the trend. The first 5-minute bar to close against the trend is immediately engulfed (the very next bar closes beyond the pullback bar's extreme).
**Economic Constraint:** Extreme directional momentum forces participants to chase. The first pullback bar invites aggressive mean-reversion flow attempting to catch the top/bottom. When that pullback is immediately engulfed, those mean-reversion participants are instantly trapped offside.
**Mechanistic Explanation:** The immediate engulfing of the first pullback proves that institutional momentum flow is completely overwhelming the available counter-trend liquidity. Trapped counter-trend flow provides a forced tailwind.
**Repeatable Event:** A rolling 60-minute return > 1.0%. The first 5-minute bar to close against the trend (pullback) is immediately followed by a 5-minute bar that closes beyond the extreme of the pullback bar.
**Information State:** First structural attempt at mean-reversion explicitly failed and trapped participants.
**Predicted Post-Entry Behavior:** Violent trend continuation.
**Executable Entry:** Market order at the close of the engulfing 5-minute bar.
**Deterministic Exit:** 60 minutes after entry.
**Opportunity Integrity:** First occurrence per expansion event.
**Positive-Expectancy Thesis:** Trapped counter-trend liquidity in a high-momentum environment creates forced liquidations (squeezes).
**Economic Headroom:** These continuation legs regularly yield 30-70 bps quickly.
**Adverse-Risk Structure:** Entering late in a 1.0% trend carries climax risk. The strict 60m exit caps duration exposure.
**Primary Counterfactual:** The exact same 1.0% expansion, followed by a pullback bar, but the next bar does NOT immediately engulf it (it takes 3+ bars to resume, or it chops).
**Expected Treatment Superiority:** The immediate (1-bar) engulfing signifies absolute structural dominance and instantly trapped capital. A slow resumption allows counter-trend capital to manage risk.
**Falsification Condition:** Slow resumptions perform identically to immediate engulfing resumptions.
**Expected Frequency:** Moderate (~30-50 opps/year).
**Data Required:** M1 USATECHIDXUSD.
**Intended Standalone Role:** SPECIALIST.
**Intended Component Role:** REGIME SPECIALIST (High Momentum).
**Closed-Line Independence:** A strict sequence-based information trap, completely distinct from static indicator momentum or arbitrary range breakouts.
**G0 Decision:** PROMOTE

## 8. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 9. Promoted Candidates
- **CAND-G0-056:** Post-Sweep Structural Shift Confirmation
- **CAND-G0-057:** Weekly Opening Gap Fade Exhaustion
- **CAND-G0-058:** Large-Range Expansion First Pullback Trap

## 10. Killed Candidates
None.

## 11. Blocked Candidates
None.

## 12. Counterfactual Quality
- **CAND-056:** Tests the exact SMC requirement of a Structural Shift vs a Sweep without a shift.
- **CAND-057:** Tests the exact anchor touch (Gap Sealed) vs an arbitrary pullback (Unsealed).
- **CAND-058:** Tests the immediate trapped capital sequence (1-bar engulf) vs a slow, un-trapped trend resumption.
All counterfactuals directly measure the incremental value of the specific condition.

## 13. Economic Headroom Quality
All candidates are structurally capable of yielding 30-150 bps of post-entry movement, comfortably clearing the 2 bps friction requirement and avoiding the CAND-052 flat-expectancy trap.

## 14. Frequency Quality
- **CAND-056:** Moderate (~40-60/year). Plausible for a Core Component.
- **CAND-057:** Low/Moderate (~15-25/year). Plausible for an Event Opportunist.
- **CAND-058:** Moderate (~30-50/year). Plausible for a Regime Specialist.

## 15. Mechanism Observability
All mechanisms (local swing pivots, Friday closing price, sequential 5-minute bar closes) are 100% strictly observable in standard M1 OHLCV data. None require invisible institutional positioning data.

## 16. SMC Structural-State Opportunities
CAND-056 directly translates the SMC "Sweep → Market Structure Shift (MSS) → Return to Order Block / Retest" sequence into a strictly observable, falsifiable artifact.

## 17. Standalone vs Component Potential
- **CAND-056:** STANDALONE POTENTIAL: Strong (Frequent, structural). COMPONENT POTENTIAL: High (Core anchor).
- **CAND-057:** STANDALONE POTENTIAL: Weak (Too rare). COMPONENT POTENTIAL: High (Highly uncorrelated weekly event).
- **CAND-058:** STANDALONE POTENTIAL: Weak (Requires specific extreme momentum regime). COMPONENT POTENTIAL: High (Extracts value specifically when mean-reversion components would fail).

## 18. Ranked Candidates
1. **CAND-056 (Post-Sweep Structural Shift):** Directly tests a foundational SMC concept against a rigorous counterfactual.
2. **CAND-058 (First Pullback Trap):** High probability of strong independent component value during trending regimes.
3. **CAND-057 (Weekly Gap Fade Exhaustion):** Very clean, independent anchor, though frequency is lower.

## 19. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-056, CAND-057, CAND-058)

## 20. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. All proposed constraints utilize currently available, verifiable M1 data. System Assembly was not performed.
