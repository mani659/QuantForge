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
