# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V23
# DATE: 2026-08-27

## 1. Research Factory Context
V23 operates under a strict reset directive: ALPHA EVENT FIRST. Recent cycles have successfully isolated profound state information (CAND-059 Freshness, CAND-064 Acceptance vs Sweep, CAND-066 Conditional Freshness), but state artifacts cannot survive without independently profitable Alphas to condition. 

## 2. V23 Objective
Return emphasis to NEW ALPHA/EVENT DISCOVERY. Search for intrinsically profitable, independently observable events that possess positive executable expectancy on their own, before any specialized state filters are applied.

## 3. V22 Lessons
V22 demonstrated that State Information is not universally monotonic. Freshness is a powerful positive filter for retests (CAND-059), but a negative filter for fading sweeps (CAND-066). State artifacts cannot be declared "good filters" in isolation; their interaction with specific Alphas must be rigorously and independently proven.

## 4. Alpha-vs-State Dependency
State research must not become an endless search for filters. The target is: ALPHA EVENT FIRST -> STATE INFORMATION SECOND -> MODULE COMBINATION LATER.

## 5. SMC Structural-State Translation
SMC concepts (sweep, rejection, structural failure) will be utilized as measurable objects to construct direct Alpha events, avoiding unproven chained sequences.

## 6. Alpha Mechanism Families
- **FAMILY C:** Sequential Information Event
- **FAMILY F:** Session Microstructure
- **FAMILY A:** Structural Price Event

## 7. Optional State Mechanism
None included. 100% focus on Alpha discovery.

## 8. Candidates Considered

### Candidate ID: CAND-G0-068
**Name:** Post-Shock Absorption Reversal
**Artifact Type:** ALPHA/EVENT
**Mechanism Family:** C — Sequential Information Event
**Observable Mechanism Variable:** A single M1 candle with a range (High - Low) > 5x the rolling 60-period average M1 range (The Shock), followed *immediately* by exactly 3 consecutive M1 inside bars (The Absorption).
**Economic Constraint:** A massive, isolated expansion (macro release/shock) that fails to generate any follow-through directional volume within 3 minutes signifies that the event was entirely priced in and liquidity has instantly restabilized. The market will aggressively revert the initial shock.
**Repeatable Event:** The shock + 3 consecutive inside bars sequence.
**Information Available Before Entry:** Yes, strictly observable upon the close of the 3rd inside bar.
**Predicted Post-Entry Behavior:** Immediate mean-reversion against the shock candle.
**Executable Entry:** Market order in the direction opposite to the shock candle's direction, executed upon completion of the 3rd inside bar.
**Deterministic Exit:** Time-based exit 15 minutes post-entry.
**Opportunity Integrity:** Identifies shocks structurally without requiring an external news-feed dependency.
**Positive-Expectancy Thesis:** Fully absorbed shocks trap late-arriving liquidity, creating a high-probability vacuum in the opposite direction.
**Economic Headroom:** Must yield > 5 bps expected net return after friction.
**Adverse-Risk Structure:** The inside bars provide a tight structural invalidation point.
**Primary Counterfactual:** Fading a similar shock candle that does *not* produce 3 consecutive inside bars (e.g., fading immediately after the shock candle closes).
**Expected Treatment Superiority:** Fading immediately is stepping in front of a freight train; fading after the 3 inside bars confirms that the train has stopped.
**Falsification Condition:** Shock fades perform identically regardless of the immediate post-shock absorption sequence.
**Expected Frequency:** Low but plausible (major shocks only).
**Standalone Potential:** STRONG
**Component Potential:** MODERATE
**Future Module Role:** Event Opportunist (Macro Fade).
**Data Required:** M1 USATECHIDXUSD.
**SMC Structural Mapping:** N/A
**Closed-Line Independence:** Entirely novel sequential structure.
**G0 Decision:** PROMOTE

---

### Candidate ID: CAND-G0-069
**Name:** NY Mid-Session Reversal Anchor
**Artifact Type:** ALPHA/EVENT
**Mechanism Family:** F — Session Microstructure
**Observable Mechanism Variable:** The highest high (or lowest low) established strictly between 11:30 ET and 12:30 ET is subsequently breached between 13:00 ET and 14:00 ET, but rejected (closes back inside) within exactly 3 minutes.
**Economic Constraint:** The 11:30-12:30 period represents the transition from morning institutional flow into the mid-day lull. Extremes established here often serve as vulnerable liquidity pools for the afternoon re-engagement. A swift rejection of this anchor traps early afternoon breakout traders.
**Repeatable Event:** 11:30-12:30 extreme is breached and rejected in <3 mins between 13:00-14:00.
**Information Available Before Entry:** Yes.
**Predicted Post-Entry Behavior:** Sharp reversal back into the core daily range as breakout traders liquidate.
**Executable Entry:** Market order upon M1 closing back inside the 11:30-12:30 anchor.
**Deterministic Exit:** 15:45 ET (before MOC flows).
**Opportunity Integrity:** Avoids the highly optimized open/close windows.
**Positive-Expectancy Thesis:** Mid-day false breakouts generate sustained afternoon reversals.
**Economic Headroom:** Must yield > 5 bps expected net return after friction.
**Adverse-Risk Structure:** Time-bound to prevent overnight holding.
**Primary Counterfactual:** The identical breach/rejection sequence occurring on the 09:30-10:30 anchor.
**Expected Treatment Superiority:** Mid-day anchors are inherently weaker and more prone to engineered sweeps than morning establishing anchors.
**Falsification Condition:** Reversals off mid-day anchors are no more profitable than reversals off morning anchors.
**Expected Frequency:** Moderate.
**Standalone Potential:** STRONG
**Component Potential:** STRONG
**Future Module Role:** Reversal Module (Session Specific).
**Data Required:** M1 USATECHIDXUSD.
**SMC Structural Mapping:** Session Liquidity Sweep.
**Closed-Line Independence:** Tests a previously unresearched temporal anchor (the mid-day lull).
**G0 Decision:** PROMOTE

---

### Candidate ID: CAND-G0-070
**Name:** Sustained Momentum Micro-Structure Failure
**Artifact Type:** ALPHA/EVENT
**Mechanism Family:** A — Structural Price Event
**Observable Mechanism Variable:** A sustained 60-minute directional move (absolute return > 0.5%) that makes strictly higher M5 highs (or lower M5 lows for downtrend). The first M5 candle to close completely below the prior M5 candle's low triggers the event.
**Economic Constraint:** In a high-momentum directional regime without pullbacks, the very first micro-structure failure traps late-arriving retail momentum chasers, triggering a sharp but brief cascade of stop-losses.
**Repeatable Event:** 60-min trend > 0.5% with uninterrupted M5 HH/HLs, followed immediately by the first M5 LH/LL close.
**Information Available Before Entry:** Yes.
**Predicted Post-Entry Behavior:** An immediate, sharp counter-trend liquidation cascade.
**Executable Entry:** Market order short (if uptrend) immediately upon the M5 structure break close.
**Deterministic Exit:** 15 minutes post-entry.
**Opportunity Integrity:** Completely agnostic to time-of-day.
**Positive-Expectancy Thesis:** The first structural failure in an overheated trend always triggers a localized stop-run.
**Economic Headroom:** Must yield > 5 bps expected net return.
**Adverse-Risk Structure:** Brief time-in-market (15 mins) avoids getting caught in the macro trend resumption.
**Primary Counterfactual:** Fading the exact same M5 structure break when the preceding 60-minute return was < 0.2% (chop).
**Expected Treatment Superiority:** Structural failures in chop are meaningless noise; structural failures in overheated trends trigger forced liquidations.
**Falsification Condition:** Momentum failures revert no harder than chop failures.
**Expected Frequency:** High.
**Standalone Potential:** STRONG
**Component Potential:** STRONG
**Future Module Role:** Trend Exhaustion Reversal.
**Data Required:** M1 USATECHIDXUSD (resampled to M5 for structure detection).
**SMC Structural Mapping:** Micro Market Structure Shift (MSS).
**Closed-Line Independence:** A pure momentum-exhaustion test untethered from static support/resistance levels.
**G0 Decision:** PROMOTE

## 9. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 10. Alpha/Event Candidates
- **CAND-G0-068:** Post-Shock Absorption Reversal
- **CAND-G0-069:** NY Mid-Session Reversal Anchor
- **CAND-G0-070:** Sustained Momentum Micro-Structure Failure

## 11. State/Condition Candidates
None.

## 12. Killed Candidates
None.

## 13. Blocked Candidates
None.

## 14. Counterfactual Quality
- **CAND-068:** Tests the structural absorption (inside bars) against immediate fading.
- **CAND-069:** Tests the mid-day temporal anchor against the morning anchor.
- **CAND-070:** Tests overheated momentum failures against chop failures.

## 15. Economic Headroom
All three Alpha candidates must prove standalone absolute net expectancy > 5 bps to clear friction.

## 16. Evidence Feasibility
All candidates rely strictly on observable M1/M5 price geometry without external dependencies.

## 17. State Information Potential
N/A (All Alphas).

## 18. SMC Opportunities
- **CAND-069:** Session Liquidity Sweep.
- **CAND-070:** Market Structure Shift (MSS).

## 19. Standalone vs Component Potential
- **CAND-068:** STANDALONE: Strong. COMPONENT: Moderate.
- **CAND-069:** STANDALONE: Strong. COMPONENT: Strong.
- **CAND-070:** STANDALONE: Strong. COMPONENT: Strong.

## 20. Module / Regime Potential
- **CAND-068:** Event Opportunist.
- **CAND-069:** Reversal Module.
- **CAND-070:** Reversal Module.

## 21. Ranked Candidates
1. **CAND-070:** Tests a foundational microstructure premise (the first LH/LL in a runaway trend).
2. **CAND-068:** Clever structural proxy for identifying and fading macro shocks without a news feed.
3. **CAND-069:** Clean temporal liquidity anchor.

## 22. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-068, CAND-069, CAND-070)

## 23. Integrity
No historical data was queried, scanned, or executed. All candidates are explicitly designed as standalone Alphas with executable entries and deterministic exits. No State candidates were generated.
