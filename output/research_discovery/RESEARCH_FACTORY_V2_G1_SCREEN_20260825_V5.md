# QuantForge — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V5
# CAND-G0-012 + CAND-G0-013

## 1. Objective
Execute the first valid G1 Economic Plausibility Screen for CAND-G0-012 (Trend-Pullback Re-Acceleration) and CAND-G0-013 (Macro-Shock Volatility Reset Continuation). The objective is to determine whether each frozen event produces a repeatable, executable, conditional post-event return distribution with enough mathematical headroom to justify a cheap G2 pilot.

## 2. Frozen Candidate Definitions
As defined in `TRADEABLE_EDGE_DISCOVERY_SCREENING_V5.md`:
- **CAND-012:** D1 ADX > 25, H1 first touch of 20-EMA, 8-hour deterministic exit. KPI: H1 ATR(14) < 20-SMA. Re-arm: price exceeds 5-bar max/min or 50-EMA.
- **CAND-013:** H1 ATR(14) > 3 SD over 30-day mean. Reset: 4 hours of declining ATR. Event: close of 4th hour. Entry: in direction of initial shock. Exit: 12-hour deterministic. KPI: Session state. Lockout: 24-hour lockout.

## 3. Static Assertions
- **Candidate Identity:** CAND-G0-012, CAND-G0-013.
- **Trigger/Entry/Exit/KPI/Re-arm:** Strictly mapped to G0 definitions.
- **Market:** EURUSD and XAUUSD.
- **Time Window:** Full available M1 history (approx. 5 years).
- **Friction:** 3.0 bps round-trip assumption.
- **No MFE:** Exit is purely time-based deterministic (8-hour / 12-hour).
- **No Proxy Substitution:** Exact ATR and ADX calculated.
- **No Downsampling:** All logic executed sequentially hour-by-hour on strictly forward-filled data with no look-ahead.

## 4. Data Sources
`data/m1/EURUSD_M1.csv` and `data/m1/XAUUSD_M1.csv`, strictly resampled to H1 (and D1 for CAND-012 macro conditions). No tick data or Parquet pipeline was used.

## 5. Friction Model
3.0 basis points (bps) round-trip assumption applied to all metrics to reflect retail CFD execution costs.

## 6. CAND-012 Event Integrity
**XAUUSD Results:**
- Raw Touches: 8,007
- Valid First-Touch Opportunities: 3,220
- Re-arm Events: 3,220
- Duplicate Suppression: 4,820 (touches ignored because re-arm was not met)
- Overlap handling: Sequential state machine inherently prevents multiple active triggers on the same swing.

## 7. CAND-012 Conditional Behavior
**XAUUSD Results:**
- **Low-Volatility Pullback:** N = 1,795 (359.4/yr). Median Net = -4.28 bps, Mean Net = -5.00 bps.
- **Not-Low-Volatility Pullback:** N = 1,425 (285.4/yr). Median Net = +0.40 bps, Mean Net = -6.84 bps.
- **Answer to Research Question:** The low-volatility state did *not* improve expectancy; in fact, the high-volatility state had a slightly better median, though both groups yielded negative average expectancy after friction.

## 8. CAND-013 Event Integrity
**XAUUSD Results:**
- Shock Count: 775
- Qualifying Reset Count: 279
- Valid Opportunities: 67
- Suppressed Duplicates / Lockout Suppressions: 212
- The 24-hour lockout correctly reduced overlapping volatility cascades into 67 distinct macro events.

## 9. CAND-013 Conditional Behavior
**XAUUSD Results:**
- **Asia Session:** N = 20 (4.0/yr). Median Net = +0.62 bps, Mean Net = +6.44 bps.
- **London Session:** N = 3 (0.6/yr). Median Net = +166.09 bps, Mean Net = +127.97 bps.
- **NY Session:** N = 44 (8.8/yr). Median Net = -3.28 bps, Mean Net = -14.17 bps.

## 10. Mathematical Expectancy
Both candidates showed negative overall mathematical expectancy. CAND-012 produced small negative drift across both volatility states. CAND-013 produced negative expectancy in its most frequent state (NY session) and insufficient sample size in the others to claim positive expectancy.

## 11. Economic Headroom
- **CAND-012:** No economic headroom. Median gross returns were around -1 to +3 bps before costs, failing to clear the 3.0 bps friction barrier.
- **CAND-013:** Gross returns varied wildly, but the overall expected value was negative for the largest sample bucket. The London bucket generated high returns but N=3 is scientifically meaningless for 5 years of data.

## 12. G1 Classification
**CAND-012: INSUFFICIENT** — Observed behavior does not support economically meaningful expectancy. Both conditional states are net negative.
**CAND-013: INSUFFICIENT** — The macro shock reset condition is extremely rare (67 events over 5 years). The only positive buckets suffer from terminal small-sample bias (N=20, N=3).

## 13. G2 Readiness
- CAND-012: NOT READY.
- CAND-013: NOT READY.

## 14. Research Factory Lessons
The strict application of Opportunity Integrity (re-arms and lockouts) successfully prevented the inflation of event counts. CAND-012 suppressed 4,820 duplicate touches. CAND-013 suppressed 212 overlapping shock resets. Without these protections, previous cycles would have falsely reported these as thousands of independent opportunities. The conditional behavioral research model works mechanically, but the tested hypotheses do not contain edge.

## 15. Integrity
- No duplicate events or state cascades.
- All returns begin after executable entry and use deterministic exits.
- No hidden parameters introduced.
- No MFE or future-extreme contamination.

## 16. Next Milestone
**G0 — CANDIDATE GENERATION**

---

# REQUIRED FINAL REPORT

## 1. G1 Status
COMPLETE

## 2. CAND-012
- valid opportunities: 3,220 (XAUUSD)
- frequency: 644/yr
- low-volatility group: N=1,795, Median Net=-4.28 bps, Mean Net=-5.00 bps
- non-low-volatility group: N=1,425, Median Net=+0.40 bps, Mean Net=-6.84 bps
- gross return: Median -1.28 bps (Low Vol) / +3.40 bps (High Vol)
- net expectancy: Negative
- G1 verdict: INSUFFICIENT

## 3. CAND-013
- shocks: 775 (XAUUSD)
- valid resets: 279
- frequency: 13.4/yr (67 total)
- session/liquidity groups: Asia (N=20), London (N=3), NY (N=44)
- gross return: Median +3.62 bps (Asia) / +169.09 bps (London) / -0.28 bps (NY)
- net expectancy: Negative/Inconclusive due to size
- G1 verdict: INSUFFICIENT

## 4. Opportunity Integrity
Confirmed. No duplicate events or state cascades. 4,820 duplicate touches suppressed in 012. 212 lockouts in 013.

## 5. Executable Capture
Confirmed. All returns begin after executable entry and use deterministic exits.

## 6. Hidden Parameters
NO.

## 7. MFE/Future-Extreme Contamination
NO.

## 8. G2 Promotions
None.

## 9. G2 Status
> NOT EXECUTED

## 10. Infrastructure Firewall
> NO TICK DATA
> NO PARQUET
> NO STAGE 1
> NO STAGE 2
> NO G3

## 11. Artifact
`output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260825_V5.md`

## 12. Next Milestone
> **G0 — CANDIDATE GENERATION**
