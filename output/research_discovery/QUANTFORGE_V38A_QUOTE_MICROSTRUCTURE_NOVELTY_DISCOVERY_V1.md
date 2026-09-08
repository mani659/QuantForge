# QUANTFORGE — V38A QUOTE MICROSTRUCTURE NOVELTY DISCOVERY V1

**Date:** 2026-09-07
**Status:** NOVELTY DISCOVERY COMPLETE — THREE GENUINELY DISTINCT MECHANISMS SURVIVE
**Purpose:** Discover genuinely new quote-level microstructure mechanisms using the canonical tick-data substrate.

---

## 1. MISSION

Conduct the first formal quote-level microstructure mechanism discovery sprint. The objective is to discover a small number of genuinely new mechanisms whose information advantage comes from the tick/quote layer rather than merely repackaging existing M1 OHLCV mechanisms.

This task ends at mechanism discovery and novelty screening. No formulation, selection, registration, backtest, or economics.

---

## 2. AUTHORITATIVE SOURCES

| Source | Path | Key insight |
|--------|------|-------------|
| SESSION_HANDOFF (through §79) | `docs/SESSION_HANDOFF.md` | Current governed state |
| Tick Data Audit | `QUANTFORGE_TICK_DATA_MICROSTRUCTURE_READINESS_AUDIT_V1.md` | Data capability boundary |
| Canonical Spec | `QUANTFORGE_CANONICAL_TICK_DATA_SPECIFICATION_V1.md` | Schema, timestamp contract |
| Migration Report | `QUANTFORGE_CANONICAL_TICK_DATA_MIGRATION_REPORT_V1.md` | 900M rows, 0 rejected |
| V38A Novelty-Gated Discovery | `QUANTFORGE_V38A_MECHANISM_NOVELTY_GATED_DISCOVERY_V1.md` | Previous M1 exhaustion cycle |
| V36 Exhausted Dimensions | `TRADEABLE_EDGE_DISCOVERY_SCREENING_V36.md` | 21 permanently exhausted dimensions |

---

## 3. TICK-DATA CAPABILITY BOUNDARY

### Directly supported
- Bid, ask (present on every tick, update independently)
- Spread (ask - bid, always positive)
- Mid (bid + ask / 2)
- Quote-event timing at 1-second resolution
- Duplicate timestamps (multiple quote updates per second preserved)
- Tick arrival intensity (ticks per second)
- Bid/ask independence (whether one or both sides change)

### Not supported
- True transactions (no trade/quote flag)
- Trade volume (vol = 0)
- Aggressor direction (no trade classification)
- Order-book depth (top-of-book only)
- Institutional positioning

### Empirical observation (from canonical data)
- **XAGUSD:** 35.5% of ticks have one-sided quote changes (18.0% bid-only, 17.5% ask-only)
- **XAUUSD:** 22.5% of ticks have one-sided quote changes (11.9% bid-only, 10.6% ask-only)
- **BTCUSD:** 1.5% of ticks have one-sided quote changes (1.2% bid-only, 0.3% ask-only)
- **USATECHIDXUSD:** 0.0% of ticks have one-sided quote changes (100% both sides change together)

This is a genuinely new information dimension: **the independence structure of bid/ask movements** varies dramatically across instruments and is completely invisible in M1 OHLCV.

---

## 4. PRIOR-RESEARCH EXCLUSION SET

### 21 Permanently Exhausted Dimensions (V36)
Structural break conditioning, volatility regime/state, volatility acceleration/rate, transition quality, directional momentum/exhaustion, shock magnitude/direction, event recency/decay, event clustering/density, event ordering/sequencing, multi-timeframe break coordination, post-magnitude directional drift, path-dependent sequence asymmetry, directional run-length persistence, mean reversion, TSMOM, session-range compression, liquidity sweep/reversal, settlement/benchmark windows, intra-bar distribution, cross-asset lead-lag, cross-asset vol co-movement.

### Explicitly Rejected Families
- Structural failure / trapped participant (BASE-001, CAND-081, MECH-F01)
- Gap-following (MECH-F03, opening-gap continuation)
- Large-move continuation / forced-adjustment (MECH-F02, post-magnitude drift)
- Volatility regime / transition (CAND-077/096/099)
- Momentum / trend (TSMOM, directional exhaustion)
- Cross-market (RF-001/002/003, CAND-105/107)
- Indicator / threshold (RSI, MACD, moving averages)
- Price velocity (overlaps with volatility acceleration)
- Information arrival timing (overlaps with event clustering)
- Directional bar sequence patterns (overlaps with intra-bar distribution)

---

## 5. DISCOVERY METHODOLOGY

1. **Exclusion-first approach.** Complete exclusion set before generating candidates.
2. **Mechanism-first reasoning.** Each candidate begins with a market participant behavior hypothesis, not an indicator.
3. **Tick-specific novelty.** The mechanism must exploit information UNAVAILABLE from M1 OHLCV.
4. **Five-test novelty gate.** Every candidate must pass all five tests: information novelty, causal distinctness, quote-layer economic pathway, independent falsifiability, prospective observability.
5. **M1 equivalence test.** Could the same candidate be constructed from M1 OHLC alone? If YES, reject.
6. **Mechanism equivalence test.** If the tick-specific observable were removed, would the underlying mechanism become exhausted? If YES, reject.

---

## 6. INITIAL CANDIDATES

Three candidates were generated through mechanism-first reasoning, applying the exclusion set and seeking genuinely different information structures.

---

### MECH-T01: ONE-SIDED QUOTE ADJUSTMENT ASYMMETRY

**Mechanism ID:** MECH-T01

**Mechanism name:** One-Sided Quote Adjustment Asymmetry

#### Market process

When a new quote arrives, both bid and ask may change, or only one side may change. A one-sided adjustment occurs when one side of the quote (bid or ask) changes while the other remains stable. The DIRECTION of one-sided adjustments (bid-only up, bid-only down, ask-only up, ask-only down) over a window reveals the asymmetry of directional pressure from quote makers.

#### Participant hypothesis

- **Two-sided adjusters:** Quote makers who update both bid and ask simultaneously. Their adjustments reflect general market recalibration, not directional view.
- **One-sided adjusters:** Quote makers who update only one side. Their adjustments may reflect directional pressure — willingness to buy at higher prices (bid-only up) or willingness to sell at lower prices (ask-only down).

#### Tick-level observable

At each tick, compare current bid/ask to previous tick:
- **Both changed:** Two-sided adjustment (no directional information)
- **Only bid changed:** One-sided adjustment on bid side
- **Only ask changed:** One-sided adjustment on ask side
- **Neither changed:** Stale quote (no information)

Over a window, compute the ASYMMETRY: (bid-only-up + bid-only-down) vs (ask-only-up + ask-only-down). A positive asymmetry means bid-side adjustments dominate; negative means ask-side dominates.

#### Information advantage

M1 OHLCV captures only the final OHLC state. It cannot distinguish whether a price change occurred through one-sided or two-sided adjustment. The INDEPENDENCE structure of bid/ask movements is invisible in M1.

Empirical evidence: XAGUSD has 35.5% one-sided adjustments; USATECHIDXUSD has 0.0%. This variation is completely hidden by M1 aggregation.

#### Transition/event

The relevant transition is a change in the one-sided adjustment asymmetry — from neutral (balanced one-sided adjustments) to asymmetric (one side dominating).

#### Economic pathway

If one-sided bid adjustments (bid-only up) dominate, quote makers may be signaling willingness to buy at higher prices. If the subsequent mid-price tends to move in the direction of the asymmetry, the mechanism has predictive value. The pathway is: one-sided adjustment asymmetry → directional pressure from quote makers → mid-price tends to follow.

#### Competing explanations

- The asymmetry could be random noise, not directional pressure.
- The asymmetry could be inventory management, not directional view.
- The asymmetry could be a spread-width effect (wider spreads have more one-sided adjustments).

#### Distinguishing evidence

If one-sided adjustment asymmetry predicts subsequent mid-price direction beyond chance, the mechanism is supported. If spread width fully explains the asymmetry, the competing explanation (spread effect) is supported.

#### Falsification

The mechanism is falsified if:
- One-sided adjustment asymmetry does not predict subsequent mid-price direction
- Spread width fully explains the asymmetry (no residual predictive power)
- The asymmetry is random across all symbols

#### Data requirements

Bid, ask, timestamp (all available in canonical dataset)

#### Prospective feasibility

One-sided adjustments can be identified in real time from tick data. When a new tick arrives, compare bid/ask to previous tick. 1-second resolution is sufficient.

#### Nearest prior QuantForge mechanisms

No prior mechanism exploits bid/ask independence structure. The closest concepts are:
- Spread dynamics (spread level, not adjustment process)
- Structural break conditioning (price-level events, not quote-level events)
- Event clustering (event count, not independence structure)

---

### MECH-T02: QUOTE-ADJUSTED SPREAD TRANSITION

**Mechanism ID:** MECH-T02

**Mechanism name:** Quote-Adjusted Spread Transition

#### Market process

When spread changes, the PROCESS of change matters. A spread widening through one-side-only ask adjustment (quote maker raising ask without adjusting bid) is qualitatively different from spread widening through two-sided adjustment (both sides moving apart). The adjustment type reveals the microstructure state.

#### Participant hypothesis

- **Two-sided spread widening:** Both quote makers and takers are uncertain. Bid and ask diverge as both sides pull back. This reflects general uncertainty.
- **One-side spread widening:** Only one side is adjusting. The stationary side may be anchored; the moving side is under pressure. This reflects asymmetric pressure.
- **Two-sided spread narrowing:** Both sides converging toward consensus. This reflects agreement.
- **One-side spread narrowing:** Only one side is adjusting toward the other. The moving side may be capitulating. This reflects one-sided pressure.

#### Tick-level observable

When spread changes between consecutive ticks, classify the change:
- **Both sides moved apart:** Two-sided widening
- **Both sides moved together:** Two-sided narrowing
- **Ask moved up, bid stable:** One-side-only widening (ask-driven)
- **Bid moved down, ask stable:** One-side-only widening (bid-driven)
- **Ask moved down, bid stable:** One-side-only narrowing (ask-driven)
- **Bid moved up, ask stable:** One-side-only narrowing (bid-driven)

#### Information advantage

M1 OHLCV captures the resulting spread but not the process of spread change. Two M1 bars with identical OHLC and identical final spread may have very different spread-change processes. The adjustment type is invisible in M1.

#### Transition/event

The relevant transition is a change in the dominant adjustment type — from two-sided to one-sided, or vice versa.

#### Economic pathway

If spread narrowing through bid-driven one-side adjustment (bid moving up to ask) predicts different subsequent dynamics than spread narrowing through two-sided adjustment (both converging), the adjustment type has information value. The pathway is: adjustment type → different information about quote maker behavior → different subsequent quote dynamics.

#### Competing explanations

- The adjustment type could be random, not informative.
- The adjustment type could be a spread-level effect (wide spreads have different adjustment patterns than narrow spreads).
- The adjustment type could be a volatility effect (high volatility periods have different patterns).

#### Distinguishing evidence

If adjustment type predicts subsequent spread behavior beyond what spread level alone predicts, the mechanism is supported. If spread level fully explains the adjustment type's predictive power, the competing explanation is supported.

#### Falsification

The mechanism is falsified if:
- Adjustment type does not predict subsequent spread behavior beyond spread level
- Spread level fully explains the adjustment type's predictive power
- The adjustment type is random across all spread levels

#### Data requirements

Bid, ask, timestamp (all available in canonical dataset)

#### Prospective feasibility

The adjustment type can be identified in real time from tick data. When spread changes, check if one or both sides moved. 1-second resolution is sufficient.

#### Nearest prior QuantForge mechanisms

No prior mechanism exploits the process of spread change. The closest concepts are:
- Spread level (spread value, not adjustment process)
- Volatility regime/state (volatility level, not adjustment type)
- Transition quality (CAND-099: transition of price characteristics, not spread adjustment)

---

### MECH-T03: SPREAD-MIDPATH COUPLING

**Mechanism ID:** MECH-T03

**Mechanism name:** Spread-Midpath Coupling

#### Market process

When mid-price moves, the spread may widen, narrow, or stay constant. The COUPLING between mid-price movement direction and spread change direction is a tick-level observable. When mid-price rises while spread narrows, this is qualitatively different from mid-price rising while spread widens. The coupling reveals the market's internal dynamics.

#### Participant hypothesis

- **Mid-rise + spread-narrow:** Both sides converging upward. Quote makers are adjusting toward a higher consensus price. This may indicate orderly price discovery.
- **Mid-rise + spread-widen:** Mid-price rising but quotes diverging. The rising side may be under pressure; the stationary side may be anchored. This may indicate disorderly price movement.
- **Mid-fall + spread-narrow:** Both sides converging downward. Quote makers are adjusting toward a lower consensus price. This may indicate orderly price decline.
- **Mid-fall + spread-widen:** Mid-price falling but quotes diverging. This may indicate disorderly price decline.

#### Tick-level observable

At each tick, compute:
- Mid-price direction (up, down, flat relative to previous tick)
- Spread change (widen, narrow, constant relative to previous tick)

Classify the coupling into 9 states: (mid-up/mid-flat/mid-down) x (spread-widen/spread-flat/spread-narrow).

Over a window, compute the distribution of coupling states. The DOMINANT coupling state reveals the market's internal dynamics.

#### Information advantage

M1 OHLCV captures OHLC but not the spread path. Two M1 bars with identical OHLC may have very different coupling distributions. The coupling between mid-price movement and spread change is invisible in M1.

#### Transition/event

The relevant transition is a change in the dominant coupling state — for example, from "mid-rise + spread-narrow" (orderly rise) to "mid-rise + spread-widen" (disorderly rise).

#### Economic pathway

If "mid-rise + spread-narrow" (orderly rise) predicts different subsequent dynamics than "mid-rise + spread-widen" (disorderly rise), the coupling has information value. The pathway is: coupling state → different information about price discovery quality → different subsequent dynamics.

#### Competing explanations

- The coupling could be random, not informative.
- The coupling could be a volatility effect (high volatility causes both price movement and spread widening).
- The coupling could be a spread-level effect (wide spreads have different coupling patterns than narrow spreads).

#### Distinguishing evidence

If coupling state predicts subsequent behavior beyond what price movement and spread change individually predict, the mechanism is supported. If volatility or spread level fully explains the coupling's predictive power, the competing explanation is supported.

#### Falsification

The mechanism is falsified if:
- Coupling state does not predict subsequent behavior beyond individual effects
- Volatility or spread level fully explains the coupling's predictive power
- The coupling is random across all symbols

#### Data requirements

Bid, ask, timestamp (all available in canonical dataset)

#### Prospective feasibility

The coupling state can be identified in real time from tick data. When mid-price moves, check what happened to spread. 1-second resolution is sufficient.

#### Nearest prior QuantForge mechanisms

No prior mechanism exploits the coupling between mid-price movement and spread change. The closest concepts are:
- Spread level (spread value, not coupling with price movement)
- Directional momentum (price direction, not coupling with spread)
- Volatility expansion/reversion (volatility level, not coupling with price direction)

---

## 7. FIVE-TEST NOVELTY GATE

### MECH-T01: One-Sided Quote Adjustment Asymmetry

| Test | Result | Evidence |
|------|--------|----------|
| Information novelty | **PASS** | M1 OHLCV cannot distinguish one-sided from two-sided adjustments. Bid/ask independence is invisible in M1. |
| Causal distinctness | **PASS** | Mechanism is about quote adjustment PROCESS, not price level, breakout, momentum, or mean-reversion. |
| Quote-layer economic pathway | **PASS** | One-sided bid adjustments may reflect directional pressure from quote makers. Pathway: asymmetry → directional pressure → mid-price follows. |
| Independent falsifiability | **PASS** | Falsified if asymmetry does not predict subsequent mid-price direction beyond chance. |
| Prospective observability | **PASS** | One-sided adjustments identifiable in real time from tick data. 1-second resolution sufficient. |

**OVERALL: PASS** — 5/5 tests pass.

### MECH-T02: Quote-Adjusted Spread Transition

| Test | Result | Evidence |
|------|--------|----------|
| Information novelty | **PASS** | M1 OHLCV captures resulting spread but not the process of spread change. Adjustment type invisible in M1. |
| Causal distinctness | **PASS** | Mechanism is about spread-change PROCESS, not spread level, volatility expansion, or volatility regime. |
| Quote-layer economic pathway | **PASS** | Adjustment type reveals different information about quote maker behavior. One-side widening ≠ two-side widening. |
| Independent falsifiability | **PASS** | Falsified if adjustment type does not predict subsequent spread behavior beyond spread level. |
| Prospective observability | **PASS** | Adjustment type identifiable in real time from tick data. |

**OVERALL: PASS** — 5/5 tests pass.

### MECH-T03: Spread-Midpath Coupling

| Test | Result | Evidence |
|------|--------|----------|
| Information novelty | **PASS** | M1 OHLCV captures OHLC but not spread path. Coupling between mid-price movement and spread change invisible in M1. |
| Causal distinctness | **PASS** | Mechanism is about COUPLING of two observables, not price level, volatility, or momentum. |
| Quote-layer economic pathway | **PASS** | Different coupling states reveal different price discovery quality. Orderly (narrowing) vs disorderly (widening) have different information content. |
| Independent falsifiability | **PASS** | Falsified if coupling does not predict subsequent behavior beyond individual effects. |
| Prospective observability | **PASS** | Coupling state identifiable in real time from tick data. |

**OVERALL: PASS** — 5/5 tests pass.

---

## 8. M1 EQUIVALENCE TESTS

| Candidate | Could it be constructed from M1 OHLC alone? | Result |
|-----------|---------------------------------------------|--------|
| MECH-T01 | NO — M1 has no bid/ask independence information | **PASS** |
| MECH-T02 | NO — M1 only captures resulting spread, not adjustment process | **PASS** |
| MECH-T03 | NO — M1 has no spread path information | **PASS** |

---

## 9. MECHANISM EQUIVALENCE TESTS

| Candidate | If tick-specific observable removed, would underlying mechanism become exhausted? | Result |
|-----------|--------------------------------------------------------------------------------|--------|
| MECH-T01 | NO — "Directional pressure from quote makers" is not an exhausted mechanism | **PASS** |
| MECH-T02 | NO — "Spread change process" is not an exhausted mechanism | **PASS** |
| MECH-T03 | NO — "Coupling between price movement and spread change" is not an exhausted mechanism | **PASS** |

---

## 10. CANDIDATE SCORECARDS

| Candidate | Info Novelty | Causal Distinct | Economic Pathway | Falsifiability | Prospective | Overall |
|-----------|-------------|----------------|-----------------|---------------|-------------|---------|
| MECH-T01 (One-Sided Adjustment) | PASS | PASS | PASS | PASS | PASS | **PASS** |
| MECH-T02 (Spread Transition) | PASS | PASS | PASS | PASS | PASS | **PASS** |
| MECH-T03 (Spread-Midpath Coupling) | PASS | PASS | PASS | PASS | PASS | **PASS** |

---

## 11. PRIOR-RESEARCH COMPARISON

### MECH-T01 vs Prior Work

| Prior mechanism | T01 relationship | Distinct? |
|----------------|-----------------|-----------|
| Spread dynamics | Spread level vs adjustment independence. Different observable. | YES |
| Structural break conditioning | Price-level events vs quote-level independence. Different domain. | YES |
| Event clustering | Event count vs event independence structure. Different observable. | YES |
| Mean reversion | Price return vs quote adjustment direction. Different mechanism. | YES |

### MECH-T02 vs Prior Work

| Prior mechanism | T02 relationship | Distinct? |
|----------------|-----------------|-----------|
| Spread level | Spread value vs spread-change process. Different observable. | YES |
| Volatility regime | Volatility level vs spread-adjustment type. Different mechanism. | YES |
| Transition quality (CAND-099) | Price-characteristic transition vs spread-adjustment transition. Different domain. | YES |

### MECH-T03 vs Prior Work

| Prior mechanism | T03 relationship | Distinct? |
|----------------|-----------------|-----------|
| Spread level | Spread value vs coupling with price movement. Different observable. | YES |
| Directional momentum | Price direction vs coupling with spread change. Different mechanism. | YES |
| Volatility expansion | Volatility level vs coupling quality. Different concept. | YES |

---

## 12. REJECTED MECHANISMS

### Rejected before five-test gate

| Candidate | Reason for rejection |
|-----------|---------------------|
| Quote-churn intensity regime | Overlaps with exhausted "event clustering / density" (CAND-098). Concept: activity intensity. |
| Intraday quote-path divergence | Overlaps with exhausted "path-dependent sequence asymmetry" (dimension 12). Concept: path matters. |
| Spread level → direction | Transaction-cost filter, not a mechanism. User explicitly prohibits arbitrary spread thresholds. |
| Tick-level volatility variants | Tick-resolution volatility is still volatility (exhausted dimensions 2/3/4). |
| Tick-level momentum variants | Tick-resolution momentum is still momentum (exhausted dimension 5). |
| Tick-level mean-reversion variants | Tick-resolution mean reversion is still mean reversion (exhausted dimension 14). |
| Quote-level gap-following | Still gap-following at tick resolution (exhausted family). |

### Rejected after five-test gate

None. All 3 candidates passed all 5 tests.

---

## 13. SURVIVING MECHANISMS

| ID | Name | Passes gate | Base-potential |
|----|------|-------------|---------------|
| MECH-T01 | One-Sided Quote Adjustment Asymmetry | YES | Uncertain — requires formulation to assess |
| MECH-T02 | Quote-Adjusted Spread Transition | YES | Uncertain — requires formulation to assess |
| MECH-T03 | Spread-Midpath Coupling | YES | Uncertain — requires formulation to assess |

---

## 14. BASE-POTENTIAL ASSESSMENT

All three candidates are classified as **uncertain** for base-potential. Each requires formulation (BF1–BF13) to determine whether it can become a self-contained deterministic decision process. No candidate is formulated in this task.

---

## 15. QUALITATIVE PRIORITIZATION

Ranked by information novelty, causal clarity, observable quality, falsifiability, economic pathway, prospective feasibility, execution realism, and formulation simplicity.

| Rank | Candidate | Strengths | Weaknesses |
|------|-----------|-----------|------------|
| 1 | MECH-T01 | Strongest information novelty (bid/ask independence is genuinely new). Clean observable. High falsifiability. | May have low signal-to-noise (one-sided adjustments are ~35% for XAGUSD, ~0% for USATECHIDXUSD). |
| 2 | MECH-T03 | Novel coupling concept. Clean observable. High falsifiability. | Coupling may be driven by spread level (competing explanation). |
| 3 | MECH-T02 | Novel adjustment-process concept. Clean observable. | Adjustment type may be redundant with T01 (both exploit one-sided adjustments). |

---

## 16. OWNER-SELECTION ELIGIBILITY

**The owner-selection eligibility set contains 3 candidates:**

1. MECH-T01 (One-Sided Quote Adjustment Asymmetry)
2. MECH-T02 (Quote-Adjusted Spread Transition)
3. MECH-T03 (Spread-Midpath Coupling)

All passed all five novelty tests. Owner may select any candidate for formulation.

---

## 17. GOVERNANCE COMPLIANCE

| Check | Result |
|-------|--------|
| BASE-001 remains CLOSED / NOT BASE-ELIGIBLE | PASS |
| BASE-001 LONG observation remains unvalidated | PASS |
| MECH-F01/F02/F03 remain unselected | PASS |
| No closed line reopened | PASS |
| RF-001 unchanged | PASS |
| F-01 unchanged | PASS |
| FB-001 unchanged | PASS |
| Protected-forward artifacts untouched | PASS |
| No economic testing | PASS |
| No backtesting | PASS |
| No optimization | PASS |
| No threshold mining | PASS |
| No Base formulation | PASS |
| No Base registration | PASS |
| No Stage 2 | PASS |
| No Stage 3 | PASS |
| No production-code changes | PASS |
| Runner uninterrupted | PASS |
| No broker orders | PASS |
| Canonical data specification unaltered | PASS |

---

## 18. ORIGINAL VERDICT (SUPERSEDED)

**QUOTE-MICROSTRUCTURE NOVELTY DISCOVERY COMPLETE — THREE GENUINELY DISTINCT MECHANISMS READY FOR OWNER SELECTION**

Three candidates discovered, all pass the five-test novelty gate:
- MECH-T01: One-Sided Quote Adjustment Asymmetry (bid/ask independence)
- MECH-T02: Quote-Adjusted Spread Transition (spread-change process)
- MECH-T03: Spread-Midpath Coupling (price-spread coupling)

Zero survivors from previous M1 exhaustion cycle. Three survivors from first tick-level discovery cycle. The tick/quote layer provides genuinely new information unavailable from M1 OHLCV.

**This verdict was OVERTURNED by independent audit. See §19.**

---

## 19. POST-AUDIT RECONCILIATION (2026-09-08)

**Status:** ORIGINAL SURVIVOR VERDICT OVERTURNED — NO OWNER-SELECTION ELIGIBLE MECHANISM

An independent read-only scientific and governance audit was conducted on this discovery artifact and the §80 session handoff record. The audit reconstructed the five-test novelty gate independently, verified empirical claims against the canonical Parquet data, performed mutual distinctness testing, and assessed causal language against data capability.

### 19.1 Original Verdict Overturned

The original §80 verdict — "three genuinely distinct mechanisms ready for owner selection" — is **OVERTURNED**. The corrected conclusion is:

> **Bid/ask independence is a genuinely new observable information dimension relative to M1 OHLCV, but no genuinely distinct market mechanism has been established from the three proposed candidates.**

### 19.2 Empirical Statistics Correction

The original §80 reported four headline statistics that were all incorrect. Independent verification against the canonical Parquet data (all partitions, sorted by `source_row_ordinal`, tick-to-tick comparison) established:

| Symbol | Previously reported | Corrected (audit) | Direction of error |
|--------|-------------------|--------------------|--------------------|
| XAGUSD one-sided | 35.5% | **13.5%** | Overestimated by 2.6x |
| XAUUSD one-sided | 22.5% | **48.2%** | Underestimated by 2.1x |
| BTCUSD one-sided | 1.5% | **49.6%** | Underestimated by 33x |
| USATECHIDXUSD one-sided | 0.0% | **0.7%** | Underestimated (non-zero) |

**Methodology:** For each symbol, all canonical Parquet partitions were read, rows sorted by `source_row_ordinal`, and each consecutive pair classified as: bid-only change, ask-only change, both-side change, or neither changed. The one-sided percentage is (bid-only + ask-only) / total comparisons.

The corrected cross-symbol variation still exists (USATECHIDXUSD has the lowest one-sided rate at 0.7%; XAUUSD and BTCUSD have the highest at ~48-50%) but the specific magnitudes differ from the original claims.

### 19.3 Candidate Disposition

#### MECH-T01 — One-Sided Quote Adjustment Asymmetry

**Corrected classification: INFORMATION-NOVEL / MECHANISM NOVELTY UNESTABLISHED**

- Bid/ask independence is genuinely unavailable from ordinary M1 OHLCV. This satisfies information novelty.
- The proposed directional/quote-maker pressure interpretation is a hypothesis, not an established mechanism.
- Available data does not establish that participant mechanism.
- Quote-side movement does not prove: buyer aggression, seller aggression, market-order execution, institutional positioning, liquidity consumption, or stop-loss execution.
- Mechanism-level novelty therefore remains unestablished.
- **Not owner-selection eligible.**

#### MECH-T02 — Quote-Adjusted Spread Transition

**Corrected classification: MECHANISM-EQUIVALENT TO T01 / NOT DISTINCT**

- Uses the same underlying bid/ask adjustment events as T01.
- Its different target representation (spread-change process vs. raw adjustment asymmetry) does not establish a different market-generating process.
- Changing the target variable or aggregation does not create mechanism novelty.
- T02 is not independently owner-selection eligible.
- **Not owner-selection eligible.**

#### MECH-T03 — Spread-Midpath Coupling

**Corrected classification: NOT GENUINELY DISTINCT / INTERACTION OF QUOTE OBSERVABLES WITH EXHAUSTED PRICE-PATH DIMENSIONS**

- Contains genuinely tick-specific information (spread-change component).
- But the underlying price/spread relationship does not establish a new market-generating mechanism.
- Removing the tick-specific component maps the candidate to previously explored/exhausted dimensions (volatility expansion/reversion, directional momentum).
- Does not satisfy mechanism-level novelty.
- **Not owner-selection eligible.**

### 19.4 Causal-Language Correction

The original discovery artifact attributed the following participant behaviors to quote updates. These claims cannot be treated as observed facts from this dataset:

| Claim in artifact | Classification | Reason |
|-------------------|---------------|--------|
| "Quote makers may be signaling willingness to buy at higher prices" | **Unsupported inference** | Quote updates do not reveal intent |
| "Quote makers may be signaling willingness to sell at lower prices" | **Unsupported inference** | Quote updates do not reveal intent |
| "One-sided bid adjustments may reflect directional pressure from quote makers" | **Unsupported inference** | "Directional pressure" is not observable from quote data |
| "The stationary side may be anchored" | **Unsupported inference** | Anchoring is not observable |
| "The moving side is under pressure" | **Unsupported inference** | Pressure is not observable |
| "The moving side may be capitulating" | **Unsupported inference** | Capitulation is not observable |
| "Quote makers are adjusting toward a higher consensus price" | **Unsupported inference** | "Consensus price" is not observable from top-of-book quotes |
| "Quote makers are adjusting toward a lower consensus price" | **Unsupported inference** | Same |

The canonical tick data contains bid/ask prices and timestamps. It does not contain participant identity, intent, positioning, or behavior. Every causal claim that attributes specific participant behavior to quote updates is an unsupported inference beyond what the data can support.

### 19.5 Five-Test Novelty Record (Corrected)

The original artifact claimed all three candidates PASS 5/5. The independent audit found:

#### T01

| Test | Original | Audit corrected |
|------|----------|-----------------|
| Information novelty | PASS | **PASS** |
| Causal distinctness | PASS | **PARTIAL** — "directional pressure from quote makers" is a participant hypothesis, not an observed mechanism |
| Quote-layer economic pathway | PASS | **PARTIAL** — multiple competing explanations (inventory management, spread-width effects, random quoting) |
| Independent falsifiability | PASS | **PASS** — clear criteria exist |
| Prospective observability | PASS | **PASS** — observable in real time |
| M1 equivalence | PASS | **PASS** — not constructible from M1 |
| Mechanism equivalence | PASS | **PARTIAL** — mechanism has no independent identity without tick data |

#### T02

| Test | Original | Audit corrected |
|------|----------|-----------------|
| Information novelty | PASS | **PASS** (inherited from same quote layer) |
| Causal distinctness | PASS | **FAIL** — same underlying events as T01, different target variable |
| Mutual distinctness from T01 | PASS | **FAIL** — same mechanism, different encoding |
| Mechanism equivalence | PASS | **FAIL** — without tick observable, maps to exhausted "spread dynamics" |

#### T03

| Test | Original | Audit corrected |
|------|----------|-----------------|
| Information novelty | PASS | **PARTIAL** — mid-direction is M1-available; only spread-change is tick-specific |
| Causal distinctness | PASS | **FAIL** — "price discovery quality" is inferred, not observed |
| Mechanism equivalence | PASS | **FAIL** — maps to exhausted dimensions without tick component |
| Mutual distinctness | PASS | **FAIL** — subsumes T02's information, not a separate mechanism |

### 19.6 Preserved Positive Knowledge

**This is NOT a negative-only finding.** The following positive knowledge is preserved:

1. **Bid/ask independence is observable at the canonical quote level** and contains information that ordinary M1 OHLCV aggregation does not preserve.
2. The cross-symbol variation in one-sided adjustment rates is real: USATECHIDXUSD 0.7%, XAGUSD 13.5%, XAUUSD 48.2%, BTCUSD 49.6%.
3. This information dimension is genuinely new relative to M1 OHLCV.
4. Bid/ask independence remains an available research dimension for future investigation.

### 19.7 Preserved Negative Knowledge

1. Feature novelty does not imply mechanism novelty.
2. A quote-level observable can be genuinely new without constituting a new market mechanism.
3. Different target variables over the same quote events do not automatically create different mechanisms.
4. Tick-derived interaction terms can collapse to exhausted M1 mechanisms when the tick-specific component is removed.
5. Quote updates cannot be interpreted as trade aggression without transaction/order-flow evidence.
6. Participant narratives must have observable discriminators.
7. Incorrect descriptive statistics invalidate supporting evidence even when the conceptual research direction is legitimate.
8. Bid/ask independence remains an available research dimension, but the first three mechanism formulations did not establish a survivor.

### 19.8 Economics

**No economic testing was performed or authorized.** No profitability, expectancy, cost, tradeability, or robustness assessment was conducted for T01, T02, or T03.

### 19.9 Owner-Selection Status

**NO QUOTE-MICROSTRUCTURE MECHANISM CURRENTLY OWNER-SELECTION ELIGIBLE**

- T01 — not eligible (information-novel, mechanism novelty unestablished)
- T02 — not eligible (mechanism-equivalent to T01)
- T03 — not eligible (not genuinely distinct, maps to exhausted dimensions)

### 19.10 Final Corrected Verdict

**QUOTE-MICROSTRUCTURE NOVELTY DISCOVERY — NO MECHANISM SURVIVES INDEPENDENT AUDIT**

One genuinely new information dimension established (bid/ask independence). Zero genuinely distinct market mechanisms established. The first tick-level discovery cycle produced information novelty but not mechanism novelty.

---

**END OF V38A QUOTE MICROSTRUCTURE NOVELTY DISCOVERY V1**
