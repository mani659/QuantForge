# QuantForge — Research Factory V2
# TRADEABLE EDGE DISCOVERY SCREENING — V9
# G0 CANDIDATE GENERATION
# 2026-08-26

## 1. Research Factory V2 Context
This G0 cycle executes under the strict Economic-First Research Factory V2 methodology. CAND-018 and CAND-021 demonstrated that attempting to rescue an underlying event (pre-auction liquidity vacuum) with retrospective indicator filters or condition states often results in scientifically contradicted economic artifacts. V9 mandates that the candidate's core event itself must mechanistically explain the expected directional edge.

## 2. V9 Research Thesis
**Can we find a market mechanism where the event itself represents information, liquidity, auction imbalance, or price-discovery change, rather than relying on an indicator filter to make an existing event look better?**
The pipeline explicitly targets structural market mechanics: observable events that mechanically necessitate a probabilistic post-entry response due to liquidity routing, inventory mandates, or information digestion.

## 3. Candidate Generation Method
Candidates were designed by mapping known market-microstructure realities to strictly objective, mathematical representations without discretionary components or layered technical indicators.

## 4. Mechanism Families
- **Family A — Information Arrival / Price Discovery:** Scheduled or sudden information shocks that create liquidity voids or structural repricing.
- **Family C — Price-Discovery State Transition:** Failed price discovery forcing asymmetric unwinding of trapped positions.
- **Family D — Session / Market Microstructure:** Time-bound liquidity mandates, such as forced inventory liquidation at session boundaries.

## 5. Candidates Considered

### Candidate ID: CAND-G0-025
### Name: Macro Shock Liquidity Void Reversal
### Mechanism Family: Family A — Information Arrival / Price Discovery
### Mechanistic Explanation: 
Scheduled macroeconomic data releases (e.g., 08:30 EST US CPI/NFP) cause instantaneous, violent repricing. When the initial shock is exceptionally severe, liquidity providers withdraw, causing the price to mechanically overshoot equilibrium into a "liquidity void." As spreads normalize and liquidity returns in the subsequent hour, the market must organically mean-revert to fill the overextended void.
### Repeatable Event: 
The 08:30:00–08:35:00 EST M5 candle's True Range exceeds 3.0 × M5 ATR(14) (where ATR is calculated prior to 08:30).
### Information State: 
Equilibrium overshoot is confirmed; the initial panic is priced in and liquidity providers will revert the price as they re-enter the order book.
### Predicted Direction: 
Reversal (counter to the 08:30–08:35 M5 candle's closing direction).
### Executable Entry: 
08:35:00 EST open.
### Deterministic Exit: 
09:30:00 EST open (regular session open).
### Opportunity Integrity: 
- **Onset:** 08:30 EST.
- **Completion:** 08:35 EST.
- **Duplicate Suppression:** Maximum 1 event per day.
- **Overlap:** Impossible due to fixed session exit.
### Economic Plausibility: 
Extreme macro shocks routinely create 50–150 point voids in USATECHIDX; capturing even a 10% structural retracement provides massive gross headroom against 2.0-point friction.
### Failure Mode: 
If the initial 5-minute shock direction consistently continues as a trend during the pre-market instead of mean-reverting, the overshoot mechanism is falsified.
### Data Required: 
USATECHIDX M1 (resampled to M5).
### Cross-Market Scope: 
Highly generalizable to rate-sensitive assets (XAUUSD, GBPUSD) affected by the 08:30 EST US data window.
### Closed-Line Independence: 
Completely independent. Does not use pre-auction drift or volatility state conditioning.
### G0 Decision: 
**PROMOTE**

---

### Candidate ID: CAND-G0-026
### Name: US Open Initial Balance Trap
### Mechanism Family: Family C — Price-Discovery State Transition
### Mechanistic Explanation: 
The first 30 minutes of the US session (09:30–10:00 EST) establish the Initial Balance (IB), representing early price discovery. A breakout of the IB that immediately fails indicates that directional liquidity is exhausted and breakout momentum traders are trapped. The structural unwinding of these trapped positions forces price rapidly to the opposite side of the IB.
### Repeatable Event: 
Between 10:00 and 11:00 EST, an M5 candle high exceeds the 09:30–10:00 EST highest high, but the same M5 candle closes below the 09:30–10:00 EST highest high. (Mirror for low).
### Information State: 
Breakout participants are trapped; directional price discovery has failed and must unwind.
### Predicted Direction: 
Reversal (short if the high failed, long if the low failed).
### Executable Entry: 
Open of the M5 candle immediately following the failed breakout candle.
### Deterministic Exit: 
12:00:00 EST open (midday session boundary).
### Opportunity Integrity: 
- **Onset:** 10:00 EST.
- **Completion:** The close of the first failing M5 candle before 11:00 EST.
- **Duplicate Suppression:** Only the *first* IB failure per day triggers an entry.
- **Overlap:** Impossible.
### Economic Plausibility: 
Unwinding a false IB break often traverses the entire daily range established up to that point, offering substantial point capture.
### Failure Mode: 
If trapped breakouts routinely consolidate or successfully re-breakout instead of causing a structural unwind, the trap hypothesis fails.
### Data Required: 
USATECHIDX M1 (resampled to M5).
### Cross-Market Scope: 
Applicable to any market with a defined, high-volume session open (e.g., DAX at 03:00 EST).
### Closed-Line Independence: 
Independent. Relies on intraday price action state-transitions, completely disconnected from prior candidate lines.
### G0 Decision: 
**PROMOTE**

---

### Candidate ID: CAND-G0-027
### Name: Intraday Trend Inventory Unwind
### Mechanism Family: Family D — Session / Market Microstructure
### Mechanistic Explanation: 
Intraday market makers and proprietary trading desks accumulate significant directional inventory during severe, one-sided trend days. Risk mandates routinely require flattening these books before the overnight session gap risk. The forced liquidation of this inventory in the final hour creates a mechanical counter-trend drift.
### Repeatable Event: 
The absolute return from 09:30:00 EST open to 15:00:00 EST open exceeds 1.5 × D1 ATR(14) (ATR calculated from the previous completed day).
### Information State: 
Intraday participants hold extreme, unbalanced directional inventory that must be mathematically flattened prior to the close.
### Predicted Direction: 
Reversal (Counter to the 09:30–15:00 trend direction).
### Executable Entry: 
15:00:00 EST open.
### Deterministic Exit: 
15:55:00 EST open (prior to the closing auction volatility).
### Opportunity Integrity: 
- **Onset:** 09:30 EST.
- **Completion:** 15:00 EST.
- **Duplicate Suppression:** Max 1 event per day.
- **Overlap:** Impossible.
### Economic Plausibility: 
A 1.5 ATR trend day represents massive, extended movement. A 5–10% unwind in the final hour provides sufficient point capture.
### Failure Mode: 
If trend days persistently accelerate into the close ("power hour" continuation) rather than unwinding, the mechanical liquidation hypothesis is falsified.
### Data Required: 
USATECHIDX M1 (resampled to D1 for ATR).
### Cross-Market Scope: 
Generalizable to all equity indices with strict session closures.
### Closed-Line Independence: 
Independent. Tests end-of-day mechanics rather than pre-market mechanics.
### G0 Decision: 
**PROMOTE**

## 6. G0 Results
- Total generated: 3
- Promoted: 3
- Killed: 0
- Blocked: 0

## 7. Promoted Candidates
- **CAND-G0-025:** Macro Shock Liquidity Void Reversal
- **CAND-G0-026:** US Open Initial Balance Trap
- **CAND-G0-027:** Intraday Trend Inventory Unwind

## 8. Killed Candidates
None.

## 9. Blocked Candidates
None.

## 10. Mechanism Diversity
The promoted candidates represent three distinct mechanism families (Information Arrival, State Transition, Session Microstructure), ensuring that if one mechanism is scientifically contradicted, the others test entirely independent structural hypotheses.

## 11. Ranked Candidates
1. **CAND-G0-026 (Initial Balance Trap):** Exceptional mechanism clarity and high expected frequency without relying on macro data releases.
2. **CAND-G0-025 (Macro Shock):** Deeply rooted in known liquidity provider behavior (widening spreads during shocks), highly falsifiable.
3. **CAND-G0-027 (Inventory Unwind):** Solid economic logic, though frequency may be lower due to the strict 1.5 ATR threshold requirement.

## 12. Exact Next Milestone
**G1 — ECONOMIC PLAUSIBILITY SCREEN**

## 13. Integrity
V9 G0 was completed descriptively and theoretically. No historical data was scanned. No parameters were searched. No incomplete forward results from CAND-015 were inspected.
