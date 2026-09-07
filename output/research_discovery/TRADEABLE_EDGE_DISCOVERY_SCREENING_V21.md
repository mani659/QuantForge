# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V21
# DATE: 2026-08-27

## 1. Research Factory Context
V21 initiates the formal distinction between ALPHA/EVENT ARTIFACTS (standalone executable strategies) and STATE/CONDITION ARTIFACTS (predictive information that alters a downstream distribution). The Dual-Path doctrine now acknowledges that a condition may be enormously valuable as a filter or module state even if it is not profitable to trade in isolation.

## 2. V21 Objective
Search for new Alpha/Event Artifacts and, separately, high-value State Artifacts—without mixing their roles. State candidates must be designed with a specific future target-event concept to prove that they materially alter a downstream distribution.

## 3. V20 Lessons
V20's CAND-059 proved that a condition (Freshness vs Mitigated) can possess massive informational value (a 4.5 bps performance gap over 24,000 events) while the underlying absolute strategy remains negative. Condemning the information because the baseline strategy failed is a severe analytical error.

## 4. Alpha/Event vs State/Condition Doctrine
- **ALPHA/EVENT ARTIFACT:** Must demonstrate absolute positive executable expectancy after friction.
- **STATE/CONDITION ARTIFACT:** Must demonstrate that it materially changes the distribution of an objectively defined downstream event, relative to a strict counterfactual state. It does not need to be independently profitable.

## 5. SMC Structural-State Translation
SMC principles (like Freshness, Sweep vs Acceptance) will continue to be modeled as isolated, measurable STATE transitions rather than bundled institutional causation narratives.

## 6. Mechanism Families
- **FAMILY F:** Session / Participant Transition
- **FAMILY B:** Regime State
- **FAMILY A:** Structural State

## 7. Candidates Considered

### Candidate ID: CAND-G0-062
**Name:** Late-Session Trend Exhaustion Fade
**Artifact Type:** ALPHA/EVENT
**Mechanism Family:** F — Session / Participant Transition
**Observable Variable:** A continuous 60-minute directional move > 0.5% (with no counter-trend close) immediately preceding the 15:00 ET timestamp, followed by a failure to make a new extreme in the 15:00-15:15 window.
**Economic Constraint:** Discretionary participants locking in afternoon trend profits ahead of the final 16:00 close MOC window, causing a localized liquidity vacuum.
**Mechanistic Explanation:** The trend exhausts as capital rotates out before the closing bell obligations.
**Repeatable Event:** 14:00-15:00 directional return > 0.5%. 15:00-15:15 extreme < 15:00 extreme.
**Target Event:** N/A (Alpha/Event).
**Information Available Before Entry:** Yes, completely known at 15:15.
**Predicted Effect:** Reversion in the final hour as positions are closed.
**Executable Entry:** Market order fade at 15:15:00.
**Deterministic Exit:** 15:45:00 (before the 15:50 MOC window begins).
**Counterfactual:** Similar continuous move ending at 13:00, failing to break high by 13:15, faded at 13:15.
**Expected Treatment Difference:** The 15:15 fade taps into mandated end-of-day profit-taking, whereas mid-day pauses can easily resolve into trend continuation.
**Falsification:** Mid-day fades perform equally well or better.
**Economic Headroom:** Must yield >5 bps net to clear friction reliably.
**Expected Frequency:** Low to Moderate.
**Standalone Potential:** MODERATE
**Component Potential:** STRONG
**Future Module Role:** Event Opportunist Module (Late Session Reversion).
**Data Required:** M1 USATECHIDXUSD.
**SMC Structural Mapping:** N/A.
**Closed-Line Independence:** Uses a different session window and mechanic than prior end-of-day candidates.
**G0 Decision:** PROMOTE

---

### Candidate ID: CAND-G0-063
**Name:** Asian Session Volatility Compression State
**Artifact Type:** STATE/CONDITION
**Mechanism Family:** B — Regime State
**Observable Variable:** The absolute range (High - Low) of the entire 18:00 - 03:00 ET session is in the bottom 10% of rolling 30-day Asian ranges.
**Economic Constraint:** Severe compression implies market-maker inventory has dwindled or participants are flat waiting for a macro catalyst, meaning the next directional move will face virtually no immediate absorption/friction.
**Mechanistic Explanation:** Stored kinetic energy. Breakouts from extreme compression lack resting liquidity to fade them.
**Repeatable State:** 18:00-03:00 (H-L) < 10th percentile of rolling 30 days.
**Target Event:** An opening range breakout (ORD) or 60-minute expansion event during the London or NY session.
**Information Available Before Entry:** Yes, state is permanently locked at 03:00 ET.
**Predicted Effect:** Target breakouts occurring after the Compression State will demonstrate significantly fatter right-tail distributions (larger continuous runs) and lower immediate mean-reversion tendencies.
**Executable Entry:** N/A (State Artifact).
**Deterministic Exit:** N/A.
**Counterfactual:** The exact same target breakout event occurring when the Asian session range is in the top 50% (Expansion state).
**Expected Treatment Difference:** Breakouts from compression travel further before exhausting compared to breakouts from already-expanded volatility states.
**Falsification:** Target breakouts perform identically regardless of the preceding Asian volatility state.
**Economic Headroom:** Must demonstrate a statistically significant shift in the target event's distribution (e.g., +15 bps improvement in the right tail).
**Expected Frequency:** Moderate (10% of sessions).
**Standalone Potential:** N/A (State Artifact).
**Component Potential:** STRONG
**Future Module Role:** Volatility filter for Trend/Breakout Modules.
**Data Required:** M1 USATECHIDXUSD.
**SMC Structural Mapping:** N/A.
**Closed-Line Independence:** A pure volatility regime definition, unlinked to specific price geometry.
**G0 Decision:** PROMOTE

---

### Candidate ID: CAND-G0-064
**Name:** Structural Acceptance Time-State
**Artifact Type:** STATE/CONDITION
**Mechanism Family:** A — Structural State
**Observable Variable:** Price breaks a 60-minute extreme and sustains at least 15 consecutive 1-minute closes beyond that extreme without crossing back into the old range.
**Economic Constraint:** Sustained time (15 mins) beyond a broken level forces longer-timeframe participants and VWAP execution algorithms to accept the new value area, shifting the consensus of fair value and preventing immediate mean reversion.
**Mechanistic Explanation:** Time builds structural acceptance. A brief breach is a sweep; a sustained breach is acceptance.
**Repeatable State:** 60-min extreme broken. Next 15 M1 bars all close beyond the extreme.
**Target Event:** A pullback to the broken extreme (a retest) occurring after the 15-minute acceptance.
**Information Available Before Entry:** Yes, state is confirmed on the 15th close.
**Predicted Effect:** Retests occurring after the Acceptance State will demonstrate a higher probability of trend continuation (bouncing off the level).
**Executable Entry:** N/A (State Artifact).
**Deterministic Exit:** N/A.
**Counterfactual:** A pullback to a broken extreme where price spent only 1 to 5 minutes beyond the extreme before pulling back (Sweep state).
**Expected Treatment Difference:** Acceptance-state retests bounce; Sweep-state retests fail and revert.
**Falsification:** The amount of time spent beyond a level before a retest has no impact on the retest's success rate.
**Economic Headroom:** Must demonstrate a measurable improvement in the win rate and median net of the target retest event.
**Expected Frequency:** High.
**Standalone Potential:** N/A (State Artifact).
**Component Potential:** STRONG
**Future Module Role:** Structural filter for Retest/Continuation Modules.
**Data Required:** M1 USATECHIDXUSD.
**SMC Structural Mapping:** Structural Acceptance vs Liquidity Sweep.
**Closed-Line Independence:** Directly isolates the time-component of structural behavior.
**G0 Decision:** PROMOTE

## 8. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 9. Alpha/Event Candidates
- **CAND-G0-062:** Late-Session Trend Exhaustion Fade

## 10. State/Condition Candidates
- **CAND-G0-063:** Asian Session Volatility Compression State
- **CAND-G0-064:** Structural Acceptance Time-State

## 11. Killed Candidates
None.

## 12. Blocked Candidates
None.

## 13. Counterfactual Quality
- **CAND-062 (Alpha):** Tests the end-of-day participant constraint directly against a mid-day void.
- **CAND-063 (State):** Tests severe compression directly against an expansion state on the identical target event.
- **CAND-064 (State):** Tests a 15-minute sustained breach directly against a 1-5 minute breach (Sweep).
All counterfactuals isolate the exact proposed mechanism.

## 14. Economic Headroom
- **CAND-062:** Requires standalone absolute positive expectancy (>5 bps net).
- **CAND-063:** Requires a demonstrable shift in the downstream right-tail payout of target events.
- **CAND-064:** Requires a demonstrable shift in the win rate/median net of target events.

## 15. State-Information Potential
- **CAND-063** could serve as a core gating filter for any breakout or trend-continuation system.
- **CAND-064** could serve as a core gating filter to distinguish between fake-outs (sweeps) and genuine structural shifts (acceptance).

## 16. SMC Opportunities
- **CAND-064** explicitly tests the SMC narrative of "Acceptance vs Sweep" using a strictly quantifiable time-based observable metric rather than subjective tape reading.

## 17. Standalone vs Component Potential
- **CAND-062:** STANDALONE: Moderate. COMPONENT: Strong.
- **CAND-063:** STANDALONE: N/A. COMPONENT: Strong.
- **CAND-064:** STANDALONE: N/A. COMPONENT: Strong.

## 18. Module / Regime Potential
- **CAND-062:** Event Opportunist.
- **CAND-063:** Volatility / Trend.
- **CAND-064:** Trend Continuation.

## 19. Ranked Candidates
### Alpha/Event
1. **CAND-062:** Clean session transition logic.

### State/Condition
1. **CAND-063:** The Asian compression concept is a classic, robust regime filter.
2. **CAND-064:** The Acceptance vs Sweep time-based mechanic is highly intriguing and perfectly bounds a core SMC concept.

## 20. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-062, CAND-063, CAND-064)

## 21. Integrity
No historical data was queried, scanned, or executed. State artifacts and Alpha artifacts have been explicitly separated. System Assembly was not performed.
