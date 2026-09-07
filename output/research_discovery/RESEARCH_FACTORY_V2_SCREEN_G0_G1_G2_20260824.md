# QUANTFORGE — RESEARCH FACTORY V2 SCREENING
**Date:** 2026-08-24
**Scope:** G0 → G1 → G2

## 1. Screening Objective
The objective of this screening cycle is not to immediately discover a profitable strategy, but to formally validate the new Economic-First Discovery Pipeline (Research Factory V2) by routing a diverse set of candidates through the cheap early-stage gates (G0 → G1 → G2) and strictly preventing any candidate from entering G3 (Scientific Validation) without earning the right.

## 2. Candidates
**CAND-001**
- **Mechanism family:** Cross-market / relative-value (Statistical Arbitrage)
- **Market / instrument:** XAUUSD and XAGUSD
- **Intended timeframe:** Intraday (M1 data, 15-minute signal, 60-minute holding)
- **Behavioral mechanism:** Liquidity absorption and correlation limits arbitrage gaps between precious metals.
- **Falsifiable hypothesis:** An extreme divergence (>3 standard deviations) between rolling 15-minute returns of XAU and XAG will mean-revert over the subsequent 60 minutes.
- **Proposed trade expression:** Sell the outperformer, buy the underperformer when the z-score of the spread return exceeds 3.0.
- **Expected holding period:** 60 minutes.
- **Expected signal frequency:** High (intraday scanning).
- **Why the mechanism could survive costs:** Precious metal divergence events are highly volatile; the standard deviation of the spread could theoretically produce a 30+ bps reversion gap.
- **Known failure modes:** Prolonged trending divergence; structural decoupling.
- **Relation to closed lines:** NOVEL (genuinely new mechanism family).

**CAND-002**
- **Mechanism family:** Session / auction behavior
- **Market / instrument:** USATECHIDXUSD
- **Intended timeframe:** Intraday (M1 data, 15:30-16:00 NY time)
- **Behavioral mechanism:** Market-on-Close (MOC) anticipatory flows and dealer covering.
- **Falsifiable hypothesis:** The directional return from 15:30 to 15:45 NY time predicts the directional return from 15:45 to the 16:00 cash close.
- **Proposed trade expression:** Enter in the direction of the 15:30-15:45 move at 15:45; exit at 16:00.
- **Expected holding period:** 15 minutes.
- **Expected signal frequency:** 1 per session.
- **Why the mechanism could survive costs:** NDX moves 20-50 bps in the final 30 minutes; USATECHIDXUSD friction is exceptionally low (~1.1 bp).
- **Known failure modes:** Reversion instead of continuation; noise dominating the MOC window.
- **Relation to closed lines:** NOVEL (genuinely new mechanism family).

**CAND-003**
- **Mechanism family:** Volatility-state transitions
- **Market / instrument:** XAUUSD
- **Intended timeframe:** Hourly / M1
- **Behavioral mechanism:** Volatility clustering and liquidity replenishment cycles.
- **Falsifiable hypothesis:** A strong hourly volatility expansion (TR > 2x ATR) followed immediately by a sharp 15-minute compression (TR < 0.5x ATR) leads to a directional breakout aligned with the prior expansion.
- **Proposed trade expression:** Enter at the close of the compressed 15-minute bar in the direction of the prior hourly expansion; exit 45 minutes later.
- **Expected holding period:** 45 minutes.
- **Expected signal frequency:** 1-5 per week.
- **Why the mechanism could survive costs:** Volatility expansions often exceed 30 bps, easily clearing the 1.7 bp friction of XAUUSD.
- **Known failure modes:** False breakouts from compression; structural regime shifts.
- **Relation to closed lines:** NOVEL (genuinely new mechanism family).

## 3. G0 Results
- **CAND-001:** NOVEL (Cross-market RV) → **PASS**
- **CAND-002:** NOVEL (Session auction) → **PASS**
- **CAND-003:** NOVEL (Volatility state) → **PASS**

## 4. G1 Economic Plausibility
- **CAND-001:** Spread trades require paying the spread on two instruments (XAU ~1.7 bp + XAG ~12.3 bp = ~14 bp total friction). The expected gross divergence target was estimated at >20 bps. **G1-PROMISING.**
- **CAND-002:** USATECHIDXUSD friction is ~1.1 bp. The EOD drift could realistically be 15-20 bps. **G1-PROMISING.**
- **CAND-003:** XAUUSD friction is ~1.7 bp. The breakout of a volatility coil usually exceeds 10 bps. **G1-MARGINAL** (borderline, but allowed to proceed to a cheap G2).

## 5. G2 Pilot Design
- **Dataset:** Existing local M1 CSV datasets (`XAUUSD_M1.csv`, `XAGUSD_M1.csv`, `USATECHIDXUSD_M1.csv`). No Parquet conversion or tick parsing was executed.
- **CAND-001 Design:** Calculated 15-minute returns for XAU and XAG. Computed rolling 1-day z-score of the difference. Filtered for z-score > 3.0 or < -3.0. Measured the 60-minute forward return of the spread.
- **CAND-002 Design:** Filtered for USATECHIDXUSD 15:30-15:45 NY time returns. Measured correlation with the immediate 15:45-16:00 forward return.
- **CAND-003 Design:** Constructed hourly ATRs. Screened for Hour 1 Expansion (TR > 2x ATR) + Hour 2 first 15m Compression (TR < 0.5x ATR). Measured the next 45-minute return.

## 6. G2 Results
- **CAND-001:** 26,425 events found. Mean Gross Return = 1.43 bps (Median = 3.11 bps). Win Rate = 53.34%. *Assessment:* The gross signal is an order of magnitude smaller than the combined ~14 bp friction.
- **CAND-002:** 1,044 events found. Mean Gross Return = 0.31 bps. Win Rate = 30.84%. *Assessment:* No directional edge exists. The return is indistinguishable from noise and below friction.
- **CAND-003:** 0 events found. *Assessment:* The rigid interaction between hourly expansion and immediate 15-minute compression produced zero trigger events in the sample, indicating the structural formulation is flawed or too restrictive.

## 7. Candidate Decisions
- **CAND-001:** **KILL** (Insufficient economic headroom. The 1.43 bp signal is crushed by 14 bp friction).
- **CAND-002:** **KILL** (Weak empirical evidence and no signal).
- **CAND-003:** **KILL** (Mechanism failure / 0 events).

## 8. Mechanism-Family Coverage
- Families explored: 3 (Relative Value, Session Auction, Volatility Transition)
- Candidates generated: 3
- Families killed: 3
- Families promoted: 0

## 9. Resource Allocation Decision
No candidate earned the right to proceed to G3 Scientific Validation. Production tick pipelines and Parquet conversions remain unallocated.

## 10. Closed-Line Firewall
No closed lines were reopened. The candidates were genuinely novel and distinct from the DISC-021 through DISC-026 families.

## 11. Promotion Recommendations
None.

## 12. Research-Factory Lessons
The G0 → G1 → G2 funnel operated flawlessly. In a single fast session, three distinct mechanism families were proposed, economically assessed, empirically tested using cheap M1 data, and cleanly killed. 

Under the legacy doctrine, CAND-001's 26,000 events and >50% win rate might have prompted a multi-day scientific investigation and staging pipeline, only to fail at the end due to the 14 bp friction floor. The Economic-First Pipeline correctly prevented this waste by demanding G1/G2 economic checks before G3 infrastructure.
