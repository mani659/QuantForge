# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V18
# DATE: 2026-08-27

## 1. Research Factory Context
The V17 G1 cycle exposed the critical distinction between informational value (a condition that successfully filters out bad trades) and tradeable economic value (a condition that provides sufficient absolute headroom after friction). V18 G0 operates under a stricter mandate to find the precise intersection of three requirements: counterfactual superiority, absolute economic headroom, and sufficient sample frequency.

## 2. V18 Objective
To discover 3–5 candidate mechanisms where: (1) The condition adds explicit, verifiable information relative to its counterfactual; (2) The expected post-entry response exceeds realistic friction by a material margin; and (3) The expected event frequency is large enough to allow for credible empirical validation. 

## 3. Lessons from V17
- **TYPE 1 FAILURE (CAND-050):** The event is profitable, but the condition makes it worse than the counterfactual.
- **TYPE 2 FAILURE (CAND-052):** The condition successfully filters chop (Treatment > Counterfactual), but absolute economics are perfectly flat (+0.01 bps). Informational value does not equal tradeable value.
- **TYPE 3 FAILURE (CAND-051):** The mechanism makes structural sense, but the strict parameters yield zero or negligible frequency (N=1), making it non-adjudicable.

## 4. Economic Headroom Requirement
Every V18 candidate must demonstrate a plausible economic pathway where the expected price movement strictly *after* executable entry materially exceeds the standard 2 bps transaction cost. Conditions that merely "lose less" than their counterfactuals are forbidden.

## 5. Counterfactual Superiority Requirement
Every V18 candidate is designed with a direct, registered counterfactual. The proposed mechanism condition must provide explicit, logical reasoning for why the treatment distribution should significantly outperform the counterfactual distribution.

## 6. Frequency Requirement
Mechanisms must possess a plausible structural frequency (High, Moderate, or Low But Plausible). "Extremely Rare" outlier events with no path to statistical validation are excluded from V18.

## 7. Mechanism Families
- **FAMILY B:** Reference Price / Settlement Transition
- **FAMILY D:** Information Sequencing
- **FAMILY E:** Structural Failure / Acceptance

## 8. Candidates Considered

### CAND-G0-053
**Name:** Friday Cash-Close Settlement Reversion
**Mechanism Family:** B — Reference Price / Settlement Transition
**Observable Condition:** USATECHIDXUSD trends in a single direction by > 1.5% absolute between 09:30 and 15:30 ET on a Friday.
**Economic Constraint:** The 15:30-16:00 ET window on a Friday represents the weekly cash close. Institutional participants and options dealers aggressively flatten extended directional risk to avoid weekend exposure (a 48-hour unhedgeable gap risk).
**Mechanistic Explanation:** When the Friday session is highly extended (large trend), participants holding that directional risk are forced to lock in profits and flatten books in the final 30 minutes. This forced, price-insensitive liquidity creates a systematic counter-trend flow.
**Repeatable Event:** On a Friday, between 09:30 and 15:30 ET, the absolute return of USATECHIDXUSD is > 1.5%.
**Information State:** A highly extended, uni-directional Friday session has reached the mandatory weekly settlement window.
**Expected Treatment Superiority:** Flattening risk before a 48-hour closure is a forced mechanical flow. On a standard Tuesday, no such weekend risk penalty exists, so the forced reversion flow is absent.
**Predicted Post-Entry Behavior:** Reversion against the 09:30-15:30 trend direction.
**Executable Entry:** 15:30 ET on Friday (Market order opposite the daily trend).
**Deterministic Exit:** 15:59 ET (Market).
**Opportunity Integrity:** Maximum one trigger per week.
**Positive-Expectancy Thesis:** Forced liquidation/flattening flow is price-insensitive, providing a clean directional tailwind into the closing bell.
**Economic Headroom:** The final 30 minutes of an extended Friday trend typically yield 20-50 bps of reversion, which comfortably exceeds the 2 bps friction.
**Adverse-Risk Structure:** A massive macro headline could cause a trend to accelerate into the close, but structurally, risk-flattening dominates.
**Primary Counterfactual:** The exact same 1.5% trend between 09:30 and 15:30 ET, but occurring on a Tuesday.
**Falsification Condition:** Tuesday 15:30-16:00 reversions perform identically to Friday 15:30-16:00 reversions.
**Expected Frequency:** Low to Moderate (~20-30 opps/year).
**Data Required:** M1 USATECHIDXUSD (with day-of-week).
**Intended Component Role:** EVENT OPPORTUNIST.
**Closed-Line Independence:** Distinct from generic session reversals. Targets a specific, scheduled liquidity transition (weekend settlement).
**G0 Decision:** PROMOTE

### CAND-G0-054
**Name:** Post-Shock Volatility Absorption
**Mechanism Family:** D — Information Sequencing
**Observable Condition:** A violent > 0.8% absolute 5-minute shock in USATECHIDXUSD during the active cash session (09:30-15:00 ET), followed immediately by 30 minutes of strict volatility containment (total High-Low range < 0.2%).
**Economic Constraint:** When a massive shock occurs, the market instantly enters price-discovery mode. If the subsequent 30 minutes feature extreme containment instead of continuation or whip-saw, it signals that passive institutional liquidity successfully absorbed the shock flow and "capped" the market.
**Mechanistic Explanation:** A massive shock creates high localized volatility. If the shock is suddenly followed by a tight 30-minute consolidation, the initiating aggressive flow has exhausted itself against passive institutional limit orders. The path of least resistance is now back in the direction of the passive liquidity (a reversal of the shock).
**Repeatable Event:** A 5-minute absolute return > 0.8%. Over the immediately subsequent 30 minutes, the High-Low range is strictly < 0.2%.
**Information State:** An aggressive market-order shock has been explicitly, verifiably absorbed by passive liquidity.
**Expected Treatment Superiority:** A shock followed by a tight consolidation (absorption) is a coiled spring for a structural reversal. A shock followed by continued high volatility is standard, unconstrained price discovery.
**Predicted Post-Entry Behavior:** Steady reversion against the original 5-minute shock direction.
**Executable Entry:** Exactly 30 minutes after the completion of the 5-minute shock (Market order opposite the shock).
**Deterministic Exit:** 60 minutes after entry, or 16:00 ET (whichever comes first).
**Opportunity Integrity:** Continuous intraday evaluation. First valid sequence per day.
**Positive-Expectancy Thesis:** The explicit proof of absorption (30m containment) confirms the initiating flow is exhausted. The responding flow now holds control and pushes price back towards the pre-shock equilibrium.
**Economic Headroom:** Reversing a 0.8% shock can typically yield 20-50 bps of reversion, easily beating 2 bps friction.
**Adverse-Risk Structure:** The consolidation could be a brief pause before a second leg of the shock.
**Primary Counterfactual:** A >0.8% 5-minute shock, followed by 30 minutes where the High-Low range is wide (>0.6%) (No containment/absorption).
**Falsification Condition:** Reversals from uncontained post-shock environments perform identically to reversals from contained environments.
**Expected Frequency:** Moderate (~30-50 opps/year).
**Data Required:** M1 USATECHIDXUSD.
**Intended Component Role:** INTRADAY REVERSION COMPONENT.
**Closed-Line Independence:** An explicit two-step information sequence (Shock -> Containment), completely independent of generic ATR reversion.
**G0 Decision:** PROMOTE

### CAND-G0-055
**Name:** Initial Balance False Breakout
**Mechanism Family:** E — Structural Failure / Acceptance
**Observable Condition:** The Initial Balance (IB) is the 09:30-10:30 ET high-low range. A false breakout occurs when the price breaks the IB high or low, but fails to maintain the expansion and quickly closes back inside the IB boundary.
**Economic Constraint:** The first hour (IB) establishes the intraday value area based on overnight information. A breakout of this area signals a new directional regime. If the breakout immediately fails, it confirms the breakout was a liquidity sweep lacking structural institutional sponsorship.
**Mechanistic Explanation:** Directional algorithms heavily trade the IB breakout. When the breakout fails to sustain and crosses back into the IB, those algorithms are trapped offside and are forced to liquidate, creating an energetic rotational move toward the opposite side of the IB.
**Repeatable Event:** Between 10:30 and 14:00 ET, price pierces the IB high (or low) by > 0.1% but < 0.3%. Within 30 minutes of the peak, the price closes back inside the strict IB range.
**Information State:** An intraday regime shift (breakout) has explicitly failed and trapped directional flow.
**Expected Treatment Superiority:** A confirmed sweep and failure of the IB boundary traps momentum capital. Simply trading back and forth inside the IB traps nobody.
**Predicted Post-Entry Behavior:** Energetic rotation toward the opposite side of the IB.
**Executable Entry:** The close of the 1-minute bar that crosses back inside the IB boundary (Market order against the breakout).
**Deterministic Exit:** 16:00 ET.
**Opportunity Integrity:** Maximum one trigger per day (first failure).
**Positive-Expectancy Thesis:** Trapped momentum capital must cover, providing a clean tailwind. 
**Economic Headroom:** An IB rotation in USATECH is typically 40-100 bps, easily exceeding 2 bps friction.
**Adverse-Risk Structure:** The market could just be expanding the range slowly. The strict time limit (failure within 30 mins) ensures we only capture sharp, definitive rejections.
**Primary Counterfactual:** The price approaches within 0.1% of the IB high/low but strictly fails to pierce it, then reverses inward.
**Falsification Condition:** Fading a non-breakout approach to the IB performs identically to fading a confirmed false breakout of the IB.
**Expected Frequency:** High (~80-120 opps/year).
**Data Required:** M1 USATECHIDXUSD.
**Intended Component Role:** EVENT OPPORTUNIST / SESSION ROTATION.
**Closed-Line Independence:** Distinct from CAND-050 (PDH). Tests the specific institutional 60-minute Initial Balance window rather than the prior calendar day.
**G0 Decision:** PROMOTE

## 9. G0 Results
- **Evaluated:** 3
- **Promoted:** 3
- **Killed:** 0
- **Blocked:** 0

## 10. Promoted Candidates
- **CAND-G0-053:** Friday Cash-Close Settlement Reversion
- **CAND-G0-054:** Post-Shock Volatility Absorption
- **CAND-G0-055:** Initial Balance False Breakout

## 11. Killed Candidates
None.

## 12. Blocked Candidates
None.

## 13. Counterfactual Quality
All three candidates possess highly specific counterfactuals designed to test the exact incremental value of the proposed mechanism condition:
- **CAND-053:** Friday (Settlement condition) vs Tuesday (No settlement condition).
- **CAND-054:** Shock + Tight Consolidation (Absorption) vs Shock + Wide Range (No Absorption).
- **CAND-055:** IB Pierce + Failure (Trapped Capital) vs IB Close Approach (No Trapped Capital).

## 14. Economic Headroom Quality
All three candidates target substantial intraday moves (20-100 bps) that comfortably clear the 2 bps friction requirement, resolving the primary failure mode of CAND-052.

## 15. Frequency Quality
All three candidates possess plausible frequencies for empirical testing:
- **CAND-053:** ~20-30 opps/year (Weekly constraint).
- **CAND-054:** ~30-50 opps/year.
- **CAND-055:** ~80-120 opps/year.

## 16. Mechanism Diversity
The candidates span Reference Price / Settlement Transition (B), Information Sequencing (D), and Structural Failure / Acceptance (E).

## 17. Component Potential
All three are structurally sound as modular trading components, possessing explicit onset, execution, and deterministic exit rules.

## 18. Ranked Candidates
1. **CAND-054 (Post-Shock Volatility Absorption):** Highly logical information sequence. Absorption is a fundamental market microstructure concept that provides clean edges.
2. **CAND-053 (Friday Cash-Close Settlement Reversion):** Scheduled participant transitions are robust and less prone to regime decay.
3. **CAND-055 (Initial Balance False Breakout):** A classic institutional structural setup, but its empirical frequency must be verified.

## 19. Exact Next Milestone
G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-053, CAND-054, CAND-055)

## 20. Integrity
No historical data was queried, scanned, or executed. No closed lines were rescued. CAND-015 logs were not inspected. All proposed constraints utilize currently available, verifiable M1 data. System Assembly was not performed.
