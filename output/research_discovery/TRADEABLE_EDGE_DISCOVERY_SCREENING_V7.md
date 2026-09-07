# QuantForge — G0 Candidate Generation
# TRADEABLE EDGE DISCOVERY SCREENING V7

## 1. Research Factory V2 Context
Under the Research Factory V2 doctrine, QuantForge operates as an Economic-First / Cost-Aware Research Funnel. The objective is to discover genuine conditional market behavior that can be translated into an executable economic edge. This document represents the execution of the G0 milestone for the V7 cycle, incorporating the Opportunity Integrity rules and the formal Economic Plausibility criteria.

## 2. Parallel-Track Boundary
This G0 Candidate Generation explicitly operates on TRACK B (Active Research Discovery). 
TRACK A (CAND-015 Forward Validation) remains ACTIVE / PROTECTED. No forward observation data from CAND-015 has been inspected, and CAND-015's mechanisms were not duplicated or relied upon for this cycle. The tracks remain strictly isolated.

## 3. G0 Candidate Generation Method
Candidates were generated through logical deduction of distinct market mechanics, focusing on observable state transitions and structural liquidity imbalances. No historical data was mined, no backtests were executed, and no parameter optimization occurred. The candidates adhere to the strict G0 Formalization and Economic-Capture firewalls.

## 4. Mechanism Families Considered
To maintain mechanism diversity, the following families were targeted:
- **Family C (Liquidity / Auction Behavior):** Structural liquidity imbalances around scheduled market events.
- **Family A (Cross-Market Information Transmission):** Asynchronous pricing of macro shocks across different asset classes.
- **Family E (Session / Market-Mechanics Behavior):** Time-driven positional de-risking and liquidation flows.

## 5. Candidates Considered

### Candidate ID: CAND-G0-018
### Name: Pre-Auction Liquidity Vacuum Reversal
### Mechanism Family: Family C (Liquidity / Auction Behavior)
### Repeatable Event:
Price drifts > 1.5 ATR(14) on M5 in a single direction during the 60 minutes strictly prior to the US Equity Cash Open (08:30 - 09:30 EST).
### Scientific Object:
Prior to a major scheduled liquidity event, liquidity providers widen spreads or pull quotes, causing price to drift against the prevailing trend due to minor order imbalance. Once the auction opens and deep liquidity returns, price sharply reverses this vacuum drift to realign with the true higher-timeframe equilibrium.
### Conditional KPI:
D1 Trend State (e.g., SMA(20) vs SMA(50) alignment). Drift that occurs *against* the daily trend should have a stronger reversal expectancy.
### Expected Post-Event Direction:
Reversal of the 08:30-09:30 EST pre-open drift.
### Executable Entry:
Market order at exactly 09:30:00 EST open.
### Deterministic Exit:
Fixed 60-minute horizon (10:30:00 EST).
### Opportunity Integrity:
- **Onset:** M5 cumulative drift > 1.5 ATR at 09:25 close.
- **Completion:** 09:30:00 EST open.
- **Duplicate Suppression:** Hard 1-per-day limit.
- **Re-arm:** Next trading day.
- **Overlap Handling:** N/A (exact time-bound event).
### Economic Plausibility:
Entry is at a high-liquidity time (cash open) where spreads tighten rapidly. The structural return of liquidity can drive a directional move substantially larger than the open spread.
### Frequency Expectation:
Moderate (1-2 times a week per equity index).
### Data Required:
M5 USATECHIDXUSD (or similar US equity index CFD).
### Cross-Market Scope:
Primarily US Equity Indices.
### Closed-Line Independence:
Distinct from DISC-024 (Session Range Expansion) and DISC-026 (Opening Range Breakout). This does not measure range expansion or breakout of an opening range; it measures a specific directional reversal of pre-open thin-liquidity drift precisely AT the open.
### G0 Decision:
PROMOTE TO G1

---

### Candidate ID: CAND-G0-019
### Name: Fixed-Income to FX Yield-Shock Transmission Lag
### Mechanism Family: Family A (Cross-Market Information Transmission)
### Repeatable Event:
US 2Y Treasury Note Futures (or a proxy like SHY ETF) experiences an M15 return > 2.5 standard deviations of its 30-day rolling M15 distribution.
### Scientific Object:
Major macro shocks are instantly priced into centralized fixed-income futures, but decentralized spot FX order books take a short time (latency) to fully adjust to the new yield differential equilibrium.
### Conditional KPI:
Pre-event 24-hour trend state of the target FX pair (Aligned vs. Counter to the shock).
### Expected Post-Event Direction:
In the fundamental direction implied by the yield shock (e.g., US yield up -> USDJPY up).
### Executable Entry:
Market order on USDJPY at the exact close of the M15 fixed-income shock bar.
### Deterministic Exit:
Fixed 4-hour horizon.
### Opportunity Integrity:
- **Onset:** FI M15 return > 2.5 SD.
- **Completion:** M15 bar close.
- **Duplicate Suppression:** Hard 4-hour lockout on USDJPY entries.
- **Re-arm:** 4 hours must pass without another FI shock.
- **Overlap Handling:** Any subsequent shocks during the lockout are ignored.
### Economic Plausibility:
M15 to H4 drift on yield repricing represents fundamental macro capital flows, which historically produce directional excursions easily exceeding tight USDJPY spreads.
### Frequency Expectation:
Low to Moderate (News and macro-driven).
### Data Required:
Synchronized M15 data for US 2Y Futures (or SHY) and USDJPY.
### Cross-Market Scope:
Fixed Income (Leader) -> USDJPY (Lagging).
### Closed-Line Independence:
Entirely new cross-asset pair (FI to FX) and fundamental driver. Does not rely on mean reversion (DISC-021) or momentum (DISC-022).
### G0 Decision:
PROMOTE TO G1

---

### Candidate ID: CAND-G0-020
### Name: Friday Afternoon Positional De-Risking
### Mechanism Family: Family E (Session / Market-Mechanics Behavior)
### Repeatable Event:
It is Friday at 12:00 NY time, and the price of XAUUSD is > 1.5 ATR(D1) away from the Monday open price.
### Scientific Object:
Ahead of the weekend, institutional participants liquidate profitable intra-week trend positions to avoid weekend gap risk. If a strong trend existed from Monday to Thursday, Friday afternoon will systematically exhibit counter-trend drift as positions are closed.
### Conditional KPI:
Weekly Excursion Magnitude (Distance from Monday open in ATR terms). The larger the intra-week move, the larger the expected liquidation flow.
### Expected Post-Event Direction:
Counter to the Monday-Thursday trend (Mean reversion towards the weekly mean/open).
### Executable Entry:
Market order on XAUUSD on Friday at exactly 12:00 NY time.
### Deterministic Exit:
Friday session close (e.g., 16:55 NY time).
### Opportunity Integrity:
- **Onset:** Friday 12:00 NY time condition check.
- **Completion:** Friday 12:00 NY time.
- **Duplicate Suppression:** Exactly one evaluation per week.
- **Re-arm:** Next Friday.
- **Overlap Handling:** N/A (exact time-bound event).
### Economic Plausibility:
Weekend de-risking flows in commodities can be substantial and unidirectional, creating a predictable 5-hour directional imbalance that exceeds the XAUUSD spread.
### Frequency Expectation:
Low (Maximum once per week, practically ~10-15 times a year when the threshold is met).
### Data Required:
H1 XAUUSD.
### Cross-Market Scope:
XAUUSD, potentially other commodities.
### Closed-Line Independence:
Distinct from DISC-021 (Mean Reversion). This does not rely on an arbitrary z-score extreme; it is purely driven by time-and-week structural liquidation mechanics.
### G0 Decision:
PROMOTE TO G1

---

## 6. G0 Screening Results
Three candidates were generated, thoroughly evaluated against the G0 constraints, and found to be formally definable, economically plausible in concept, and independent of closed research lines.

## 7. Promoted Candidates
- CAND-G0-018
- CAND-G0-019
- CAND-G0-020

## 8. Killed Candidates
None. (Generation was strictly limited to high-quality, pre-screened conceptual models).

## 9. Blocked Candidates
None.

## 10. Mechanism Diversity
The three promoted candidates span exactly three distinct mechanism families:
- Family C (Liquidity / Auction Behavior)
- Family A (Cross-Market Information Transmission)
- Family E (Session / Market-Mechanics Behavior)
No two candidates rely on the same causal driver.

## 11. Ranked Candidates
1. **CAND-G0-018 (Pre-Auction Liquidity Vacuum Reversal):** Extremely clear causality, highly deterministic execution, easy to falsify.
2. **CAND-G0-019 (Fixed-Income to FX Yield-Shock Transmission Lag):** Strong fundamental logic, though cross-market synchronization adds minor data complexity.
3. **CAND-G0-020 (Friday Afternoon Positional De-Risking):** Classic market mechanic, highly testable, but lowest frequency of the group.

## 12. Exact Next Milestone
**G1 — ECONOMIC PLAUSIBILITY SCREEN FOR V7 PROMOTED CANDIDATE(S)**

## 13. Integrity
No historical data was scanned. No backtests were run. No PnL was calculated. No parameter searching occurred. No ML/mining tools were used. The protected CAND-015 forward observation logs were not accessed.
