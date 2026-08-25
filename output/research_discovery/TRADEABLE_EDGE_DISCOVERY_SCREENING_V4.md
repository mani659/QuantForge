# QuantForge — G0 Candidate Generation + Screening
# TRADEABLE EDGE DISCOVERY SCREENING V4

## 1. Research Factory V2 Context

Following the adoption of the `QUANTFORGE_RESEARCH_FACTORY_V2.md` doctrine, QuantForge operates as an Economic-First / Cost-Aware Research Funnel. The pipeline progresses strictly through G0 (Candidate Generation) → G1 (Economic Plausibility) → G2 (Cheap Empirical Pilot) before any expensive scientific or production infrastructure is engaged.

This document represents the execution of the G0 milestone.

## 2. G0 Objective

The objective of this screening is to identify a small number (3–5) of genuinely promising, economically plausible, and structurally distinct trading mechanisms. The goal is to evaluate whether these mechanisms possess the fundamental characteristics—observable market behavior, executable entry, and post-entry movement—that justify advancing to the G1 Economic Plausibility Screen.

## 3. Candidate Generation Method

Candidates were synthesized by reviewing cross-market structural dynamics, liquidity absorption models, multi-timescale equilibria, and auction mechanics. Strict adherence to the closed-line firewall was maintained. We explicitly prohibit any mechanism that re-specifies or attempts to rescue the closed Mean Reversion (DISC-021), fixed 12/1 TSMOM (DISC-022), H01 Equity (DISC-023), Session Range Expansion (DISC-024), Liquidity Sweep (DISC-025), or ORD (DISC-026) research lines.

## 4. Candidate Cards

### CAND-G0-001
**Name:** Cross-Asset Volatility Spillover
**Mechanism Family:** cross-market / relative-value
**Market Mechanism:** Volatility shocks propagate sequentially from central liquidity hubs (US Equities) to peripheral assets (Crypto/Precious Metals) due to arbitrage latency and information absorption delays.
**Scientific Object:** The lagged conditional volatility of asset B given a volatility shock in asset A.
**Observable Definition:** Trailing 60-minute realized volatility in USATECHIDXUSD exceeding the 95th percentile.
**Executable Entry:** Market order straddle or momentum-breakout entry on BTCUSD or XAGUSD exactly at the close of the USATECHIDXUSD shock bar.
**Expected Post-Entry Response:** The realized volatility and directional momentum of the target asset expands over the subsequent 2-4 hours.
**Expected Holding Period:** 2-4 hours.
**Expected Frequency:** 2-3 times per month.
**Economic Headroom:** UNKNOWN.
**Cross-Market Scope:** USATECHIDXUSD -> BTCUSD, XAUUSD, XAGUSD.
**Cheapest Data Needed:** Hourly / M1.
**G1 Screen:** Compute the median 4-hour forward directional excursion of BTCUSD/XAUUSD conditioned on a USATECHIDXUSD volatility shock to see if it exceeds realistic spread.
**G2 Pilot:** Straddle or breakout backtest on M1 data.
**Falsifiability:** Volatility does not expand sequentially, or the expansion occurs simultaneously with no exploitable lag.
**Closed-Line Independence:** NEW.
**G0 Verdict:** PROMOTE TO G1.

---

### CAND-G0-002
**Name:** Session-Transition Imbalance Continuation
**Mechanism Family:** auction/session dynamics
**Market Mechanism:** Consistent, low-volatility directional drift during the Asian session indicates institutional order flow accumulation. When London liquidity enters, this imbalance is aggressively materialized, driving price further in the drift direction.
**Scientific Object:** The correlation between Asian-session directional drift quality and London-session return.
**Observable Definition:** Asian session (00:00-07:00 UTC) price drift with a linear R-squared > 0.85, followed by a breakout of the Asian range in the first hour of London (08:00-09:00 UTC).
**Executable Entry:** Market entry upon the breakout of the Asian range during the 08:00-09:00 UTC window.
**Expected Post-Entry Response:** Price continues in the breakout direction as London participants provide liquidity for the established imbalance.
**Expected Holding Period:** 4-6 hours (exit at London close / NY open).
**Expected Frequency:** 2-4 times a week per asset.
**Economic Headroom:** CLEAR.
**Cross-Market Scope:** EURUSD, GBPUSD, XAUUSD.
**Cheapest Data Needed:** M1.
**G1 Screen:** Measure the median London-session return following a high R-squared Asian drift and a London open breakout, comparing against spread costs.
**G2 Pilot:** M1 backtest of the entry/exit logic on EURUSD.
**Falsifiability:** London session reliably reverses the Asian drift, or the breakout fails to exceed the spread.
**Closed-Line Independence:** NEW.
**G0 Verdict:** PROMOTE TO G1.

---

### CAND-G0-003
**Name:** Nested Volatility Compression Breakout
**Mechanism Family:** multi-timescale structure
**Market Mechanism:** Simultaneous volatility compression across multiple timescales (daily, 4-hour, 1-hour) signifies an extreme equilibrium. Breaking this equilibrium forces a cascade of structural re-pricing and stop-loss triggering, producing a low-recoil trend.
**Scientific Object:** The intersection of historical volatility percentiles across D1, H4, and H1 timescales.
**Observable Definition:** Realized volatility over 1-day, 4-hour, and 1-hour windows simultaneously falling below their respective 10th percentiles.
**Executable Entry:** Stop-entry order triggered when price breaks the established H4 range during the compression state.
**Expected Post-Entry Response:** A sustained, low-recoil directional move as the market discovers a new value area.
**Expected Holding Period:** 1-3 days.
**Expected Frequency:** 1-2 times a month per asset.
**Economic Headroom:** CLEAR.
**Cross-Market Scope:** Universal.
**Cheapest Data Needed:** Hourly / M1.
**G1 Screen:** Measure the maximum favorable excursion (MFE) vs maximum adverse excursion (MAE) over 3 days following a nested volatility compression breakout.
**G2 Pilot:** H1/M1 breakout backtest on XAUUSD and EURUSD.
**Falsifiability:** Breakouts from nested compression are dominated by false breakouts (immediate reversion) rather than sustained trends.
**Closed-Line Independence:** NEW.
**G0 Verdict:** PROMOTE TO G1.

---

### CAND-G0-004
**Name:** Transient Volume-Impact Reversal
**Mechanism Family:** liquidity / order-flow
**Market Mechanism:** Extremely high volume spikes in a short period (e.g. 5 min) without a macro news catalyst represent transient liquidity absorption. This pushes price away from equilibrium temporarily, which reverts as liquidity replenishes.
**Scientific Object:** The 60-minute price return associated with a >99th percentile M1 volume spike.
**Observable Definition:** 5-minute volume > 99th percentile of a 30-day rolling window for that time-of-day, accompanied by a directional move of > 2 standard deviations.
**Executable Entry:** Market order immediately at the close of the 5-minute anomaly bar, fading the direction of the spike.
**Expected Post-Entry Response:** Price reverts partially toward the pre-spike level as the transient order flow imbalance subsides.
**Expected Holding Period:** 15 to 60 minutes.
**Expected Frequency:** 2-4 times a month per asset.
**Economic Headroom:** MARGINAL.
**Cross-Market Scope:** XAUUSD, XAGUSD, BTCUSD, USATECHIDXUSD.
**Cheapest Data Needed:** M1 (must include volume).
**G1 Screen:** Compute the median 60-min return following 99th percentile M1 volume spikes, minus the entry spread.
**G2 Pilot:** Run on EURUSD and BTCUSD M1 to see if post-entry excursion exceeds 3 bps.
**Falsifiability:** Price continues in the direction of the volume spike (momentum), or fails to revert more than the bid-ask spread.
**Closed-Line Independence:** ADJACENT.
**G0 Verdict:** PROMOTE TO G1.

---

## 5. Closed-Line Independence Review

- **DISC-021 (Mean Reversion):** CAND-G0-004 relies on volume/liquidity exhaustion rather than pure price z-score displacement, rendering it adjacent but distinct. All other candidates are completely unrelated.
- **DISC-022 (TSMOM):** No trend-following variants or 12/1 re-specifications were proposed.
- **DISC-023 (H01 Equity):** No candidate leverages asymmetric volatility response to negative shocks.
- **DISC-024 (Session Range Expansion):** CAND-G0-003 is multi-timescale and agnostic of sessions, explicitly avoiding the pre-session compression to cash-session expansion dynamic.
- **DISC-025 (Liquidity Sweep):** CAND-G0-002 focuses on *continuation* of a high-quality Asian drift into London, actively contrasting with the Asian extreme *reversal* tested in DISC-025.
- **DISC-026 (ORD):** CAND-G0-002 utilizes London open, not US open, and is predicated on pre-existing Asian drift quality rather than a pure opening range breakout.

**Conclusion:** All promoted candidates respect the closed-line firewall.

## 6. Economic Headroom Assessment

1. **CAND-G0-002 (Session Imbalance):** CLEAR. London session continuations yield substantial gross excursions capable of absorbing 1-3 bp frictions.
2. **CAND-G0-003 (Nested Compression):** CLEAR. Multi-day breakouts provide massive headroom relative to entry frictions.
3. **CAND-G0-004 (Volume-Impact Reversal):** MARGINAL. Structural mispricing must consistently outsize round-trip spreads and slippage on the immediate fade.
4. **CAND-G0-001 (Volatility Spillover):** UNKNOWN. Dependent on whether cross-asset volatility manifests as a tradable directional trend or requires complex options structures.

## 7. Candidate Ranking

1. **CAND-G0-002 (Session-Transition Imbalance Continuation):** High plausibility, extremely clear executable entry, cheap to falsify.
2. **CAND-G0-003 (Nested Volatility Compression Breakout):** Highest economic headroom, cross-market universal scope.
3. **CAND-G0-004 (Transient Volume-Impact Reversal):** Strong micro-structural basis, but marginal headroom constraints.
4. **CAND-G0-001 (Cross-Asset Volatility Spillover):** Interesting theoretical mechanism, but lowest executable clarity and unknown headroom.

## 8. G0 Decisions

- CAND-G0-001: PROMOTE TO G1
- CAND-G0-002: PROMOTE TO G1
- CAND-G0-003: PROMOTE TO G1
- CAND-G0-004: PROMOTE TO G1

## 9. Proposed G1 Screens

- **CAND-G0-001:** Compute the median 4-hour forward directional excursion of BTCUSD/XAUUSD conditioned on a USATECHIDXUSD volatility shock.
- **CAND-G0-002:** Measure the median London-session return following a high R-squared Asian drift and a London open breakout.
- **CAND-G0-003:** Measure the maximum favorable excursion (MFE) vs maximum adverse excursion (MAE) over 3 days following a nested volatility compression breakout.
- **CAND-G0-004:** Compute the median 60-min return following 99th percentile M1 volume spikes, minus the entry spread.

## 10. Resource Requirements

- All proposed G1 screens can be executed using the existing M1 dataset inventory (`data/m1/`).
- No Parquet conversion, tick processing, or Stage 1/2 infrastructure is required or authorized.

## 11. Rejected Candidates

### CAND-G0-005
**Name:** 12-Month Momentum with Regime Filter
**Mechanism Family:** regime-conditioned behavior
**Reason for Rejection:** Explicit rescue attempt of DISC-022. Fails the closed-line firewall.
**G0 Verdict:** KILL AT G0.

## 12. Governance Decision

**G0 COMPLETE — CANDIDATE(S) PROMOTED TO G1**
**G1 EXECUTION NOT AUTHORIZED BY THIS TASK.**

## 13. Exact Next Milestone

G1 — ECONOMIC PLAUSIBILITY SCREEN FOR PROMOTED CANDIDATE(S)

## 14. Integrity

- No backtests were run.
- No PnL was calculated.
- No parameter sweeps or threshold optimizations occurred.
- Read-only repository inspection was maintained.
- All decisions were made based on mechanistic reasoning and structural constraints in accordance with Research Factory V2.

## 15. G1 Executable-Capture Contract (Hardened)

Before any G1 execution, the implementation must adhere to the following strict requirements established in `QUANTFORGE_RESEARCH_FACTORY_V2.md`:
1. **Trigger:** Explicitly defined.
2. **Executable Entry:** Earliest realistic entry without assuming unobservable/future prices.
3. **Post-Entry Window:** Only movement after entry may be measured.
4. **Deterministic Exit:** No Maximum Favorable Excursion (MFE) allowed. Must use fixed horizon, stop, target, or session boundary.
5. **Gross Opportunity:** Measured from executable entry to deterministic exit.
6. **Friction:** Explicitly stated and applied.
7. **Frequency:** Expected trades and overlaps recorded.
8. **No Free Breakout Capture:** Must pay the breakout confirmation threshold.

Additionally, the **G1 Definition-Lock Rule** explicitly prohibits proxy substitution (e.g., swapping R-squared for Efficiency Ratio) and undocumented event downsampling. All screens must pass the pre-run static assertion checklist.

## 16. G0 Candidate Generation Cycle V5 (2026-08-25)

This cycle operates under the hardened Research Factory V2 contract, strictly avoiding any MFE endpoints, pre-entry assumptions, or undocumented proxies.

### 16.1. Candidate Cards

#### CAND-G0-006
**Name:** Crypto-to-Equity Risk-On Impulse Lead
**Mechanism Family:** Multi-timescale lead/lag (Family B)
**Market Mechanism:** Bitcoin trades 24/7 and absorbs overnight/weekend liquidity shocks and macroeconomic risk repricing before traditional markets open. An extreme, directional impulse in BTCUSD immediately prior to the US equity open reliably predicts the opening momentum and subsequent cash-session trend of US technology equities.
**Scientific Object:** The directional correlation between pre-market (07:30–09:30 ET) BTCUSD extreme return and the USATECHIDXUSD cash-session return.
**Trigger:** BTCUSD directional return in the 2 hours preceding 09:30 ET > 3x its 14-day ATR.
**Executable Entry:** Market order on USATECHIDXUSD exactly at the close of the 09:30 ET M1 bar, in the direction of the BTCUSD impulse. Entry is fully observable and executable immediately after the trigger.
**Deterministic Exit:** Fixed horizon exit at the 16:00 ET cash session close.
**Expected Post-Entry Response:** USATECHIDXUSD trends in the direction of the BTC overnight impulse throughout the cash session.
**Expected Frequency:** 15-25 times per year.
**Economic Headroom:** CLEAR. A full cash-session trend typically dwarfs a single entry spread.
**Friction Relationship:** Single entry, multi-hour hold, massive expected movement vs spread.
**Cheapest Data Needed:** M1 USATECHIDXUSD and M1 BTCUSD.
**Cheap G1 Screen:** Filter days with > 3 ATR BTC pre-market move. Compute USATECHIDXUSD return from 09:31 open to 16:00 close. Compare median return to expected spread.
**Cheap G2 Pilot:** Script across 10 years of M1 data for this specific time window.
**Falsification Condition:** Gross return of the USATECH session is negative or zero net of drift.
**Cross-Market Scope:** Specific cross-asset pair (Crypto to Equity Index).
**Closed-Line Independence:** NEW.
**G0 Verdict:** PROMOTE TO G1.

---

#### CAND-G0-007
**Name:** Weekend Gap Regime Continuation
**Mechanism Family:** Regime transition / state persistence (Family F)
**Market Mechanism:** Weekend gaps represent discontinuous price discovery. When a gap fails to mean-revert (fill) during the initial liquidity influx of the Monday session, it indicates a structural regime shift rather than transient imbalance, leading to a multi-day continuation trend.
**Scientific Object:** The conditional probability of a Friday-to-Friday directional trend given an unfilled Monday open gap.
**Trigger:** Market opens Sunday/Monday with a gap > 1.5x the 14-day ATR. At the end of the first 2 hours of trading, the price has NOT crossed the Friday closing price.
**Executable Entry:** Market order in the direction of the gap exactly at the open of the M1 bar immediately following the 2-hour confirmation window.
**Deterministic Exit:** Fixed horizon exit at the Friday session close.
**Expected Post-Entry Response:** Multi-day drift/trend in the direction of the gap.
**Expected Frequency:** 5-10 times per year per market.
**Economic Headroom:** CLEAR.
**Friction Relationship:** Very low turnover, massive holding period (nearly 5 days), easily outscaling spread.
**Cheapest Data Needed:** Hourly / M1.
**Cheap G1 Screen:** Identify > 1.5 ATR gaps. Filter for non-filled after 2 hours. Compute return from hour 2 to Friday close.
**Cheap G2 Pilot:** Script over 15 years of hourly data.
**Falsification Condition:** Post-gap drift is zero or immediately mean-reverts after the 2-hour mark.
**Cross-Market Scope:** EURUSD, XAUUSD, XAGUSD.
**Closed-Line Independence:** NEW.
**G0 Verdict:** PROMOTE TO G1.

---

#### CAND-G0-008
**Name:** Safe-Haven Metal Divergence
**Mechanism Family:** Relative-value / cross-market state discrepancy (Family A)
**Market Mechanism:** Gold (safe-haven/monetary) and Silver (industrial) normally move together. A sharp divergence (Gold up, Silver down) flags an acute macro risk-off regime (flight to safety + industrial collapse). This state persists structurally as institutions rebalance over several days.
**Scientific Object:** The forward 5-day return of the XAU/XAG relative value portfolio following an acute 1-day divergence.
**Trigger:** Daily return of XAUUSD > +1.5% AND daily return of XAGUSD < -1.0%.
**Executable Entry:** Buy XAUUSD and Sell XAGUSD exactly at the daily close (or next day open) where the trigger is met.
**Deterministic Exit:** Fixed horizon exit exactly 5 trading days later at the daily close.
**Expected Post-Entry Response:** Divergence expands further as the risk-off regime persists.
**Expected Frequency:** 1-3 times per year.
**Economic Headroom:** MARGINAL (rare event, requires two spreads, but structural move is large).
**Friction Relationship:** 5-day holding period provides substantial time for divergence to exceed the combined XAU and XAG spreads.
**Cheapest Data Needed:** Daily.
**Cheap G1 Screen:** Find days meeting trigger. Compute 5-day forward return of long XAU / short XAG.
**Cheap G2 Pilot:** Simple script over 20 years of daily close data.
**Falsification Condition:** Divergence immediately reverts to historical mean correlation.
**Cross-Market Scope:** XAU/XAG specific.
**Closed-Line Independence:** NEW.
**G0 Verdict:** PROMOTE TO G1.

---

#### CAND-G0-009
**Name:** Extreme Displacement ML Rescue
**Mechanism Family:** Mean Reversion (Family F)
**Market Mechanism:** Same as DISC-021 (extreme short-term displacement reversing), but applying a K-means volatility regime filter to avoid trend-continuation days.
**Scientific Object:** Short-term mean reversion conditioned on low volatility regime.
**Trigger:** Price drops > 4 ATR in 2 hours AND K-means regime = "Low Volatility".
**Executable Entry:** Entry on the next M1 bar open.
**Deterministic Exit:** 4-hour fixed horizon.
**Expected Post-Entry Response:** Asymmetric mean-reversion recovery.
**Expected Frequency:** 50 times per year.
**Economic Headroom:** INSUFFICIENT.
**Friction Relationship:** Marginal moves consumed by spread (already established in DISC-021).
**Cheapest Data Needed:** M1.
**Cheap G1 Screen:** N/A.
**Cheap G2 Pilot:** N/A.
**Falsification Condition:** Same as DISC-021.
**Cross-Market Scope:** Universal.
**Closed-Line Independence:** RESCUE (Attempting to revive DISC-021 using a different filter threshold).
**G0 Verdict:** KILL AT G0.

### 16.2. Closed-Line Firewall Review

- **DISC-021 (Mean Reversion):** CAND-G0-009 directly attempted to rescue this mechanism via K-means filtering and was rightfully killed. CAND-G0-006, 007, and 008 use entirely different mechanics (lead/lag, continuation, divergence).
- **DISC-022 (TSMOM):** No trend-following/momentum candidates proposed.
- **DISC-023 (H01 Equity):** No volatility-asymmetry candidates proposed.
- **DISC-024 (Session Range Expansion):** No session compression/expansion mechanics.
- **DISC-025 (Liquidity Sweep):** No Asian extreme reversals.
- **DISC-026 (ORD):** No opening range breakouts.

### 16.3. Candidate Ranking

1. **CAND-G0-006 (Crypto-to-Equity Risk-On Impulse Lead):** Highest executable clarity, highly observable trigger, completely uncorrelated to prior closed mechanisms.
2. **CAND-G0-007 (Weekend Gap Regime Continuation):** Extremely simple, massive holding period guarantees friction overhead is negligible, universal across non-24/7 markets.
3. **CAND-G0-008 (Safe-Haven Metal Divergence):** Novel cross-market regime state, but low frequency and double-spread friction pushes it lower.

### 16.4. Proposed G1 Screens (Hardened Contract Aware)

- **CAND-G0-006:** Filter days where BTC moved > 3 ATR pre-market (07:30-09:30 ET). Enter USATECH at 09:30 close. Exit 16:00 close. Calculate gross return vs 1x spread.
- **CAND-G0-007:** Identify > 1.5 ATR weekend gaps. Check if filled by hour 2. If not, enter at hour 2 close, exit Friday close. Calculate gross return vs 1x spread.
- **CAND-G0-008:** Find days with XAU > +1.5% and XAG < -1.0%. Enter XAU long / XAG short at close. Exit 5 days later. Calculate gross return vs 2x spread.

*All proposed G1 screens strictly respect executable entry (no pre-entry capture) and deterministic exits (no MFE).*

### 16.5. G0 Decisions

- CAND-G0-006: PROMOTE TO G1
- CAND-G0-007: PROMOTE TO G1
- CAND-G0-008: PROMOTE TO G1
- CAND-G0-009: KILL AT G0

### 16.6. Exact Next Milestone

**G1 — ECONOMIC PLAUSIBILITY SCREEN** (For CAND-G0-006, 007, 008)

*G1 AUTHORIZATION REQUIRED IN A SEPARATE TASK. DO NOT EXECUTE NOW.*

---

## 17. OWNER-SUPPLIED SMC HYPOTHESIS SOURCE

Reference:
[`output/research_discovery/SMC_HYPOTHESIS_REGISTER_V1.md`](file:///c:/Users/User10/Documents/MRV/yuvi/QuantForge/output/research_discovery/SMC_HYPOTHESIS_REGISTER_V1.md)

Six owner-supplied Smart Money Concepts (SMC) hypotheses have been ingested for formalization assessment. Only hypotheses judged genuinely formalizable and economically coherent (e.g., H2, H5, H6) may be considered for future G0 candidate selection. Discretionary mechanisms (H3, H4) remain permanently blocked.

## 18. SMC-DERIVED G0 CANDIDATE SELECTION

The following hypotheses from the SMC register (H2, H5, H6) have been evaluated for translation into deterministic G0 candidates.

### H2 Disposition: PROMOTE TO G0 (CAND-G0-010)

**Name:** HTF POI + M1/M5 CHOCH Reversal
**Mechanism Family:** Structural Reversals at Liquidity Extremes (Family 1)
**Closed-Line Independence:** Distinct from DISC-025 (Liquidity Sweep). DISC-025 relied purely on a localized wick-sweep and rejection close. CAND-G0-010 strictly requires a multi-bar structural break (CHOCH), demanding a sustained shift in order flow rather than a transient stop-run.
**POI Definition:** Previous day's high or low.
**Trigger:** 
1. Price crosses the POI.
2. An M5 structural swing is formed (a fractal extreme where the central bar is higher/lower than 3 bars before and after).
3. The M5 close breaks (closes beyond) the immediately preceding M5 opposing swing.
**Executable Entry:** Market order on the open of the M5 bar immediately following the CHOCH confirming close.
**Deterministic Exit:** Fixed 2-hour horizon.
**Expected Frequency:** 30-50 times per year per market.
**Friction Relationship:** Moderate. The M5 entry ensures tight proximity to the extreme, but the 2-hour hold must produce enough excursion to clear the round-trip spread.
**Cheap G1 Screen Concept:** Scan EURUSD M5 data for previous daily high/low sweeps followed by a 3-bar swing break. Measure the median 2-hour gross excursion.
**Cheap G2 Pilot Concept:** Backtest on M5 EURUSD over 5 years.
**Explicit Falsification Condition:** The M5 CHOCH is a lagging artifact of the sweep rather than a leading indicator of reversal, yielding zero net drift after entry.

### H5 Disposition: HOLD FOR DEFINITION / DATA

**Name:** Two-Bar Reversal + Low Volume
**Reason for Hold:** A formal audit of the `data/m1/` repository confirms that the M1 CSV files (e.g., BTCUSD, USATECHIDXUSD) contain NO volume data (`volume = 0` for all records). Furthermore, tick volume in decentralized FX/CFD markets is fundamentally unreliable for proving institutional participation ("low volume"). This hypothesis is mathematically formalizable but practically blocked until high-quality, centralized exchange volume data (e.g., CME Futures or direct equity feeds) is ingested and validated.
**Status:** HOLD.

### H6 Disposition: PROMOTE TO G0 (CAND-G0-011)

**Name:** Double Top/Bottom + RSI Divergence
**Mechanism Family:** Structural Reversals at Liquidity Extremes (Family 1)
**Closed-Line Independence:** Distinct from DISC-021 (Mean Reversion). DISC-021 traded extreme standard-deviation displacements (z-score shocks) aiming for immediate elastic snapback. CAND-G0-011 requires a complex, dual-swing spatial structure (double top/bottom) over an extended timeframe, explicitly confirmed by a momentum failure (RSI divergence).
**Trigger:**
1. Two 20-bar rolling extrema (Swing 1 and Swing 2) occur separated by 20 to 100 bars.
2. The price of Swing 2 is within 0.1% of Swing 1 (or penetrates it).
3. The 14-period RSI at Swing 2 is at least 5 points less extreme than the RSI at Swing 1 (Divergence).
4. Confirmation occurs when price crosses the 10-period moving average.
**Executable Entry:** Market order on the close of the confirming bar.
**Deterministic Exit:** Fixed 4-hour horizon.
**Expected Frequency:** 10-20 times per year per market.
**Friction Relationship:** Highly favorable. A confirmed double-top reversal held for 4 hours typically yields excursions well beyond 1-3 bps spreads.
**Cheap G1 Screen Concept:** Scan EURUSD and XAUUSD M1/M5 for the dual-swing structural matching and RSI difference. Measure the 4-hour gross excursion.
**Cheap G2 Pilot Concept:** Simple parameterized backtest on XAUUSD.
**Explicit Falsification Condition:** Double tops with RSI divergence are indistinguishable from normal ranging price action, and the 4-hour drift is essentially zero.

### Formal G0 Candidates Promoted:
- **CAND-G0-010** (Derived from H2)
- **CAND-G0-011** (Derived from H6)

---

## 19. CONDITIONAL BEHAVIOR & OPPORTUNITY INTEGRITY

**Conditional Behavior / Mathematical Expectancy Research Principle:**
Future G0 candidates must prioritize investigating conditional post-event behaviors rather than searching for 100% win-rate patterns. A candidate must define an event, an executable entry, a forward measurement window, and explicitly hypothesize which observable market KPIs (e.g., volatility, session, trend) condition the return distribution to achieve positive mathematical expectancy. 

**Opportunity Integrity:**
All future event-based candidates must explicitly define event onset, event completion, duplicate suppression, and re-arm conditions to prevent single market episodes from creating overlapping duplicate opportunities in the state machine.

### Recent Candidate Dispositions
- **CAND-G0-010 (HTF POI + CHOCH):** INVALID / NON-ADJUDICABLE. The G1 implementation suffered a severe event-count anomaly due to a state-machine duplication error, violating Opportunity Integrity. Closed for this cycle without an economic conclusion.
- **CAND-G0-011 (Double Top + RSI Div):** ECONOMICALLY INSUFFICIENT. The G1 implementation successfully isolated valid structures, but the median gross edge (+0.16 bps) was entirely consumed by realistic friction (3.0 bps). Closed for this cycle.
