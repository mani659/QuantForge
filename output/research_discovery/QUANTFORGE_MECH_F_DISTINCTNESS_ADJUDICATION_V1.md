# QUANTFORGE — MECH-F DISTINCTNESS ADJUDICATION V1

**Date:** 2026-09-07
**Status:** DISTINCTNESS AUDIT COMPLETE — ONE OR MORE CANDIDATES REQUIRE EXCLUSION/REFORMULATION
**Purpose:** Independent, read-only semantic distinctness adjudication of MECH-F01/F02/F03 against all prior QuantForge research.
**Parent doctrine:** V38 (D13 closed-line firewall), V38A (BV1–BV13), BS1–BS13 (BS3 closed-line firewall)

---

## 1. SCOPE

This document records an independent, read-only semantic distinctness adjudication of three mechanisms discovered in the latest V38A research cycle:

- MECH-F01 — Failed Breakout Inventory Reversal
- MECH-F02 — Shock-Induced Position Adjustment Cascade
- MECH-F03 — Overnight Gap Inventory Rebalancing

The audit determines whether each mechanism is genuinely distinct from prior QuantForge research at the **mechanism level**, not merely at the implementation level. Changing instrument, threshold, bar count, timing, direction, or holding period does NOT establish mechanism distinctness.

**Hard boundary respected:** No mechanism selected, no Base formulated, no parameters chosen, no economics calculated, no backtests run, no code modified, no runner touched.

---

## 2. AUTHORITATIVE SOURCES CONSULTED

| Source | Artifact | Role in audit |
|--------|----------|---------------|
| Fresh Discovery | `QUANTFORGE_V38A_FRESH_INDEPENDENT_MECHANISM_DISCOVERY_V1.md` | Candidate definitions |
| CAND-081 Governance Review | `QUANTFORGE_CAND077_CAND081_STATE_GOVERNANCE_REVIEW_V1.md` | CAND-081 mechanism definition |
| CAND-083 Independence Audit | `QUANTFORGE_CAND083_STATE_GOVERNANCE_REVIEW_V1.md` | CAND-081 independence confirmation |
| SEED-002 Registration | `QUANTFORGE_RELATIONAL_RESEARCH_V1_SEED002_REGISTRATION.md` | CAND-081 definition in relational context |
| SEED-002 Results | `QUANTFORGE_RELATIONAL_SEED002_DISCOVERY_RESULTS_V1.md` | CAND-081 negative result |
| BASE-001 Registration | `QUANTFORGE_MECH_N01_V38A_BASE_REGISTRATION_V1.md` | BASE-001 frozen definition |
| BASE-001 Formulation | `QUANTFORGE_MECH_N01_OUTCOME_BLIND_FORMULATION_V1.md` | MECH-N01 mechanism statement |
| BASE-001 Stage 3 | `QUANTFORGE_BASE001_V38A_STAGE3_ECONOMIC_VALIDATION_V1.md` | LONG vs SHORT economics |
| BASE-001 Adjudication | `QUANTFORGE_BASE001_OWNER_ECONOMIC_ADJUDICATION_V1.md` | Closure rationale |
| V38A New Discovery | `QUANTFORGE_V38A_NEW_BASE_MECHANISM_DISCOVERY_V1.md` | MECH-N01/N02/N03, rejected mechanisms |
| Relational Discovery | `QUANTFORGE_RELATIONAL_MECHANISM_DISCOVERY_V1.md` | REL-M03 / RF-003 |
| Relational Formulations | `QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md` | RF-003 formulation |
| Liquidity Sweep Closure | `LIQUIDITY_SWEEP_RESEARCH_LINE_CLOSURE_GOVERNANCE_RECORD_V1.md` | DISC-025 closure |
| Liquidity Sweep Adjudication | `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_SCIENTIFIC_ADJUDICATION_V1.md` | Sweep behavioral discovery |
| V36 Strategic Assessment | `TRADEABLE_EDGE_DISCOVERY_SCREENING_V36.md` | 21 exhausted dimensions |
| SESSION_HANDOFF | `docs/SESSION_HANDOFF.md` | Current governed state |

---

## 3. CANDIDATE DEFINITIONS (from Fresh Discovery)

### MECH-F01 — Failed Breakout Inventory Reversal

**Trigger:** Breakout of structural level (close beyond N-bar high/low), followed by failure (price reverses back through level within F bars).

**Participant hypothesis:** Breakout traders enter at the breakout. When the breakout fails, they are trapped. Stop-losses and margin rules force liquidation. Forced liquidation creates directional pressure in the reversal direction.

**Causal chain:** breakout → failure → trapped participants → forced liquidation → reversal.

**Direction:** Fade the original breakout (failed upside → SHORT, failed downside → LONG).

### MECH-F02 — Shock-Induced Position Adjustment Cascade

**Trigger:** Large intraday move exceeding a structural threshold S (relative to recent volatility).

**Participant hypothesis:** Large move triggers stop-losses, margin calls, risk-limit adjustments, and volatility-targeting reductions. These forced adjustments create additional directional flow in the same direction as the original move.

**Causal chain:** large move → stop-outs → margin calls → risk-limit reductions → vol-targeting reductions → self-reinforcing cascade → exhaustion.

**Direction:** Follow the original large move (same direction).

### MECH-F03 — Overnight Gap Inventory Rebalancing

**Trigger:** Overnight gap (US market open minus previous session close).

**Participant hypothesis:** Overnight holders face positioning imbalance at the open. Some rebalance (creating directional flow). Gap traders enter (adding to flow). Market makers adjust inventory (adding to flow).

**Causal chain:** overnight information → gap → positioning imbalance → rebalancing flow → opening session direction.

**Direction:** Follow the gap direction (gap up → LONG, gap down → SHORT).

---

## 4. PRIOR-RESEARCH EXCLUSION SET

### 4.1 CAND-081 (Structural Level Failure Trap) — CRITICAL COMPARISON

**Mechanism (verbatim):** "When price breaks a structural level (20-bar high/low) by 3+ bps but reverses back through the level within 5 bars, trapped breakout participants create directional pressure against the breakout direction."

**Participant hypothesis:** "Breakout participants enter expecting continuation. When the breakout fails within 5 bars, these participants face losses. Their stops are placed beyond the breakout level. As price reverses through the level, stops are triggered, creating forced exit flow that accelerates the reversal."

**Observable:** Price breaks level by 3+ bps, reverses within 5 bars.

**Event:** Break → fail within 5 bars → trapped participants.

**Directional consequence:** Fade the breakout (counter-breakout direction).

**Governance status:** STATE REVIEW ELIGIBLE — PRESERVED. Not a Base, not Alpha, not closed, not promoted.

### 4.2 BASE-001 (Structural Level Validation Flow)

**Mechanism:** Validated breakout → participant behavior change → directional continuation.

**Direction:** Follow validated break (LONG bullish, SHORT bearish).

**Governance status:** CLOSED / NOT BASE-ELIGIBLE.

### 4.3 MECH-N01/N02/N03

MECH-N01: Structural Level Validation Flow (same as BASE-001).
MECH-N02: Cross-Asset Hedging Cascade (cross-market).
MECH-N03: Session-Sequential Trend Quality (trend path quality).

### 4.4 RF-001/002/003

RF-001: Cross-Market Confirmation Failure (cross-market, fade).
RF-002: Synchrony Regime (cross-market).
RF-003: Cross-Market Shock Absorption Asymmetry (cross-market, asymmetric absorption).

### 4.5 Exhausted Dimensions (21 from V36)

Structural break conditioning, volatility regime/state, volatility acceleration/rate, transition quality, directional momentum/exhaustion, shock magnitude/direction, event recency/decay, event clustering/density, event ordering/sequencing, multi-timeframe break coordination, post-magnitude directional drift, path-dependent sequence asymmetry, directional run-length persistence, mean reversion, TSMOM, session-range compression, liquidity sweep/reversal, settlement/benchmark windows, intra-bar distribution, cross-asset lead-lag, cross-asset vol co-movement.

### 4.6 Liquidity Sweep Research (DISC-025)

Behavioral discovery supported; economic translation failed. Sweep → rejection → confirmation → directional excursion. Closed with preserved discovery.

---

## 5. MECH-F01 DEEP AUDIT

### 5.1 Mechanism-Level Comparison: MECH-F01 vs CAND-081

| Dimension | MECH-F01 | CAND-081 | Assessment |
|-----------|----------|----------|------------|
| **Trigger** | Structural level break + failure within F bars | Structural level break + failure within 5 bars | SAME — both require the same structural event (break and fail at a level) |
| **Participant behavior** | Breakout traders trapped → forced liquidation → reversal | Breakout traders trapped → forced exit flow → reversal | SAME — identical participant class, identical behavior, identical consequence |
| **Information mechanism** | Forced liquidation after failure creates directional pressure | Trapped participants create directional pressure against breakout | SAME — forced liquidation IS the trapped-participant flow |
| **Market-state transition** | Breakout in progress → breakout failed | Free participant state → trapped participant state | SAME — both describe the transition from "breakout uncertain" to "breakout failed" |
| **Directional consequence** | Fade the breakout (opposite direction) | Fade the breakout (counter-breakout direction) | SAME — both fade the original breakout direction |
| **Economic transmission** | Forced liquidation → selling/buying pressure → reversal | Forced exit flow → directional pressure → reversal | SAME — forced liquidation IS forced exit flow |
| **Failure mode** | Forced liquidation may not occur (participants hold) | Trap may not produce directional pressure | SAME — both depend on forced participant behavior |
| **Opportunity population** | One per failed breakout | One per failed structural break | SAME — both triggered by the same event |

**Assessment: IDENTICAL MECHANISM.** The causal chain is:
- MECH-F01: breakout → failure → trapped participants → forced liquidation → reversal
- CAND-081: break → fail → trapped participants → forced exit flow → reversal

" Forced liquidation" and "forced exit flow" are synonymous descriptions of the same participant behavior. The mechanism is identical.

### 5.2 Same Event?

**YES.** Both require: (a) price breaks a structural level, (b) price reverses back through the level within a defined window. The only implementation difference is that CAND-081 specifies N=20, threshold=3 bps, window=5 bars, while MECH-F01 leaves N, threshold, and F as governance-selectable parameters. Parameter generalization does not create mechanism distinctness.

### 5.3 Same Participant Hypothesis?

**YES.** Both hypothesize:
- Breakout traders enter at the breakout
- Breakout fails → traders are trapped
- Forced exit flow (stops, margin rules) creates directional pressure
- Directional pressure pushes price in the reversal direction

The participant classes are identical (breakout traders). The behavior is identical (trapped → forced liquidation). The consequence is identical (reversal).

### 5.4 Same Causal Chain?

**YES.** The causal chains are structurally identical:

| Step | MECH-F01 | CAND-081 |
|------|----------|----------|
| 1 | Breakout occurs | Structural level broken |
| 2 | Breakout fails (price reverses through level) | Price reverses through level (within window) |
| 3 | Breakout traders trapped | Trapped participant population created |
| 4 | Forced liquidation creates directional pressure | Forced exit flow creates directional pressure |
| 5 | Price reverses | Directional pressure against breakout |

### 5.5 Same Economic Consequence?

**YES.** Both hypothesize that the forced liquidation after failure creates a directional edge in the reversal direction. The hypothesized edge is fundamentally the same: fade the failed breakout.

### 5.6 Different Observable Only?

**YES — this is the core finding.** The difference between MECH-F01 and CAND-081 is primarily:

1. **Governance classification:** CAND-081 is a STATE OBSERVATION. MECH-F01 is a DECISION PROCESS.
2. **Parameter specificity:** CAND-081 uses N=20, 3 bps, 5 bars. MECH-F01 leaves these as governance-selectable.
3. **Entry/exit rules:** CAND-081 has no entry/exit rules (it is an observation). MECH-F01 specifies entry after failure confirmation and exit at session close.
4. **Completeness:** CAND-081 is incomplete as a Base (no participation, entry, exit). MECH-F01 is a complete decision process.

**These are governance-level differences, not mechanism-level differences.** The underlying market mechanism — structural level break, failure, trapped participants, forced liquidation, reversal — is identical.

### 5.7 BASE-001 Closure Protection

> "Would failed breakout → fade merely be another formulation of the failed/rejected-break portion of the structural-level research already explored?"

**YES.** CAND-081 specifically tested the failed-breakout portion of structural-level research. The counterfactual in CAND-081's governance review compared:
- Failed breakouts (trap formed): -0.78 bps net mean, 53% win rate
- Successful breakouts (no trap): -2.01 bps net mean, 48.3% win rate

The failed-breakout → fade direction was specifically tested in CAND-081. MECH-F01 is proposing to trade this exact same phenomenon as a Base. This is a duplication risk.

### 5.8 CAND-081 Protection

CAND-081 is STATE REVIEW ELIGIBLE — PRESERVED. It must not be reopened. However, its mechanism definition is preserved as negative knowledge. The mechanism-level comparison above uses only CAND-081's mechanism definition and governance history, not any performance metrics.

### 5.9 MECH-F01 Verdict

| Dimension | Assessment |
|-----------|------------|
| Mechanism distinctness from CAND-081 | **NOT DISTINCT** — identical mechanism |
| Distinctness from BASE-001 | DISTINCT — BASE-001 follows validated breaks; F01 fades failed breaks. Different direction, different event. |
| Governance classification difference | **YES** — F01 is a decision process; CAND-081 is an observation |
| Mechanism-level difference | **NO** — same causal chain, same participant behavior, same economic consequence |
| Repackaging risk | **HIGH** — F01 is CAND-081's observation repackaged as a decision process |

**Verdict: PARTIALLY DISTINCT.** The governance classification is different (decision process vs. observation), but the underlying mechanism is identical. The distinctness is at the governance level, not the mechanism level. Owner selection should be PERMITTED WITH CAVEATS: the owner must understand that MECH-F01 is the same mechanism as CAND-081, reformulated as a complete decision process.

---

## 6. MECH-F02 AUDIT

### 6.1 What "Shock" Actually Means Mechanistically

MECH-F02 defines "shock" as: "an unusually large price move (significantly larger than recent normal activity)." The threshold S is defined relative to recent volatility (e.g., "move exceeding N times recent ATR").

**The problem:** "Large move" is a statistical description, not a mechanism. The mechanism is supposed to be "forced position adjustments" (stop-outs, margin calls, risk-limit reductions). But the trigger is defined by magnitude, not by the mechanism itself.

This means the trigger is empirically identifiable (any large move) but the mechanism (forced adjustments) is not separately observable. You cannot distinguish a "large move that triggered forced adjustments" from a "large move that was purely informational" using only M1 OHLCV data.

### 6.2 Is Forced Adjustment Different from Volatility Transition?

**CAND-077** (volatility character transition): Market transitions from smooth to choppy or vice versa. Mechanism: regime change in volatility character.

**MECH-F02** (shock-induced cascade): Large move triggers forced adjustments. Mechanism: forced participant repositioning.

**Comparison:**
- CAND-077: regime-level transition (hours/days), triggered by ATR percentile change
- MECH-F02: event-level process (minutes), triggered by single large move

The triggers are different (rolling regime vs. single event). The mechanisms are different (volatility character vs. forced repositioning). **PARTIALLY DISTINCT** — different trigger, different mechanism, but the observable (continued directional movement after a large move) is similar.

### 6.3 Does MECH-F02 Duplicate RF-003?

**RF-003** (Cross-Market Shock Absorption Asymmetry):
- Two markets absorb the same shock differently
- Slow-absorbing market is shorted
- Cross-market comparison

**MECH-F02** (Shock-Induced Position Adjustment Cascade):
- Single market, large move triggers forced adjustments
- Follow the forced-adjustment flow
- Single-market

**Comparison:**
- RF-003 is cross-market (relational). MECH-F02 is single-market. Different unit of analysis.
- RF-003 measures absorption asymmetry. MECH-F02 measures forced-adjustment cascade.
- RF-003 fades the slow absorber. MECH-F02 follows the large move.

**DISTINCT** — different mechanism, different unit of analysis, different direction.

### 6.4 Is "Exceeds Threshold" Merely an Empirical Trigger?

**YES.** The threshold S is defined relative to recent volatility, but the mechanism (forced adjustments) is not separately observable. The threshold identifies "large moves," but the mechanism (forced adjustments) is inferred, not observed.

This creates a problem: the mechanism is unfalsifiable in its current form. You cannot test whether forced adjustments occurred — you can only test whether large moves were followed by continued directional movement. The forced-adjustment story is an interpretive overlay on an observable that is also consistent with other explanations (e.g., momentum continuation, information flow, liquidity withdrawal).

### 6.5 Does a Genuinely Distinct Causal Pathway Exist?

**PARTIALLY.** The causal pathway (large move → forced adjustments → cascade) is distinct from:
- Volatility regime (different trigger, different mechanism)
- Momentum continuation (different mechanism — forced adjustments vs. trend following)
- Mean reversion (different direction)

But the pathway is NOT distinct from:
- Post-magnitude directional drift (exhausted) — both describe continued movement after large moves
- Directional momentum (exhausted) — both describe directional continuation

The forced-adjustment mechanism is a plausible explanation for post-large-move continuation, but it is not independently observable. The same observable (continued movement after large moves) is consistent with multiple mechanisms.

### 6.6 MECH-F02 Verdict

| Dimension | Assessment |
|-----------|------------|
| Mechanism distinctness from CAND-077 | PARTIALLY DISTINCT — different trigger, different mechanism, but similar observable |
| Mechanism distinctness from RF-003 | DISTINCT — cross-market vs. single-market, different mechanism |
| Mechanism distinctness from post-magnitude drift | NOT DISTINCT — same observable (continued movement after large moves), different interpretive layer |
| Mechanism distinctness from directional momentum | NOT DISTINCT — same directional consequence, different interpretive layer |
| Observable separability | LOW — forced adjustments not separately observable from M1 OHLCV |
| Falsifiability | LOW — mechanism is unfalsifiable (forced adjustments cannot be directly tested) |
| Trigger mechanism gap | HIGH — "exceeds threshold" is empirical, not mechanistic |

**Verdict: PARTIALLY DISTINCT.** The forced-adjustment mechanism is a plausible and distinct interpretation, but it is not independently observable and cannot be distinguished from momentum continuation using available data. The trigger ("exceeds threshold") is empirical, not mechanistic. Owner selection should be PERMITTED WITH CAVEATS: the owner must understand that the mechanism is interpretive and not independently falsifiable.

---

## 7. MECH-F03 AUDIT

### 7.1 Is the Mechanism Actually Inventory Rebalancing?

MECH-F03 claims the mechanism is "inventory rebalancing at the open" — overnight holders rebalancing positions, gap traders entering, market makers adjusting inventory.

**The problem:** The decision rule is: enter in the gap direction at the open. This is functionally identical to gap-following momentum. The inventory-rebalancing story is an interpretive overlay on a simple momentum trade.

### 7.2 Is It Merely Gap-Following Momentum?

**YES — functionally.** The decision rule:
- Gap up → LONG at open
- Gap down → SHORT at open
- Exit at session close or after N bars

This is the definition of gap-following momentum. The inventory-rebalancing story explains WHY the gap might continue, but the decision rule is identical to simple gap-following.

### 7.3 Does It Duplicate Existing Opening-Gap Research?

The V38A discovery artifact rejected "opening auction → regular session transition" because it "overlaps with exhausted 'settlement / benchmark windows' (CAND-074/075)."

MECH-F03 is positioned as distinct from settlement windows because it is about "overnight information accumulation" rather than "settlement mechanics." But:

- Settlement windows: price behavior around benchmark fixing times
- MECH-F03: price behavior at the session open after an overnight gap

The session open IS a settlement-adjacent time. The gap IS created by overnight information that cannot be traded until the open. The participant dynamics (positioning adjustments, rebalancing) are structurally similar to settlement-window dynamics.

**PARTIALLY OVERLAPS** with the exhausted settlement/benchmark family.

### 7.4 Does the Mechanism Depend on Market-Opening Microstructure?

**YES.** The mechanism specifically depends on:
- US market open time (09:30 ET)
- Overnight information accumulation
- Opening-session participant dynamics

This ties the mechanism to market-opening microstructure, which overlaps with the exhausted settlement/benchmark windows family.

### 7.5 Is the Participant Hypothesis Coherent?

**PARTIALLY.** The participant classes are plausible:
- Overnight holders rebalancing: plausible
- Gap traders entering: plausible
- Market makers adjusting inventory: plausible

But the causal chain is weak:
- Gap → positioning imbalance → rebalancing flow → continuation

The link between "positioning imbalance" and "continuation" is inferential. If the gap reflects genuine information, continuation is expected regardless of inventory rebalancing. If the gap reflects positioning only, the rebalancing might actually REVERSE the gap (if overnight holders sell into the open to reduce exposure).

### 7.6 Is the Gap Merely an Observable or Part of the Mechanism?

**The gap is the observable, not the mechanism.** The mechanism is supposed to be "inventory rebalancing." But the decision rule only uses the gap direction, not any measure of inventory or rebalancing. The gap is the trigger; the rebalancing is the (unobservable) mechanism.

### 7.7 Can It Become a Mechanism-Driven Base?

**PROBLEMATIC.** For a Base to be mechanism-driven, the mechanism must produce a distinctly different observable or timing from a simple indicator. MECH-F03's decision rule (enter in gap direction at open) is functionally identical to a gap indicator. The inventory-rebalancing mechanism does not produce a different observable, different timing, or different direction than simple gap-following.

A mechanism-driven Base would need to answer: "What does inventory rebalancing tell us that gap direction alone does not?" The current formulation cannot answer this question.

### 7.8 MECH-F03 Verdict

| Dimension | Assessment |
|-----------|------------|
| Mechanism distinctness from gap momentum | NOT DISTINCT — decision rule is functionally identical |
| Mechanism distinctness from settlement windows | PARTIALLY DISTINCT — different timing (open vs. close), but similar participant dynamics |
| Participant hypothesis coherence | PARTIAL — plausible but causal chain is weak |
| Observable separability | LOW — inventory rebalancing not separately observable |
| Falsifiability | LOW — mechanism is unfalsifiable (rebalancing cannot be directly tested) |
| Mechanism-driven Base potential | LOW — decision rule is gap-following, not mechanism-driven |

**Verdict: PARTIALLY DISTINCT.** The mechanism (inventory rebalancing) is different from gap-following in interpretation, but the decision rule is functionally identical. The mechanism is not independently observable and does not produce a different observable than simple gap-following. Owner selection should be PERMITTED WITH CAVEATS: the owner must understand that the decision rule is gap-following momentum with an interpretive overlay.

---

## 8. MECHANISM-LEVEL COMPARISON

### 8.1 MECH-F01 vs Closest Prior (CAND-081)

| Dimension | MECH-F01 | CAND-081 | Same / Partial / Distinct | Reason |
|-----------|----------|----------|--------------------------|--------|
| Trigger | Structural level break + failure within F bars | Structural level break + failure within 5 bars | **SAME** | Both require break and fail at structural level |
| Participant behavior | Breakout traders trapped → forced liquidation | Breakout traders trapped → forced exit flow | **SAME** | Identical participant class and behavior |
| Information mechanism | Forced liquidation creates directional pressure | Forced exit flow creates directional pressure | **SAME** | "Forced liquidation" = "forced exit flow" |
| Market-state transition | Breakout uncertain → breakout failed | Free state → trapped state | **SAME** | Both describe the same transition |
| Directional consequence | Fade the breakout | Fade the breakout | **SAME** | Both fade in the same direction |
| Economic transmission | Forced liquidation → reversal pressure | Forced exit flow → reversal pressure | **SAME** | Same transmission mechanism |
| Failure mode | Forced liquidation may not occur | Trap may not produce pressure | **SAME** | Same failure condition |
| Opportunity population | One per failed breakout | One per failed structural break | **SAME** | Same event triggers both |

**Overall: SAME MECHANISM.** 8/8 dimensions same. The governance classification differs (decision process vs. observation), but the mechanism is identical.

### 8.2 MECH-F02 vs Closest Prior (Post-Magnitude Drift / CAND-077)

| Dimension | MECH-F02 | Post-Magnitude Drift | Same / Partial / Distinct | Reason |
|-----------|----------|---------------------|--------------------------|--------|
| Trigger | Large move exceeding threshold S | Large move (no specific threshold) | **PARTIAL** | Both triggered by large moves; F02 adds threshold |
| Participant behavior | Forced adjustments (stops, margin calls) | Not specified (drift) | **PARTIAL** | F02 specifies mechanism; drift does not |
| Information mechanism | Forced adjustment cascade | Not specified | **DISTINCT** | F02 has a mechanism; drift is purely observational |
| Market-state transition | Normal → forced-adjustment cascade | Not specified | **DISTINCT** | F02 has a transition; drift does not |
| Directional consequence | Follow the large move | Follow the large move | **SAME** | Both follow the same direction |
| Economic transmission | Forced adjustments → continuation | Not specified | **PARTIAL** | F02 specifies transmission; drift does not |
| Failure mode | Cascade may not occur | Not specified | **PARTIAL** | F02 specifies failure; drift does not |
| Opportunity population | One per large move | One per large move | **SAME** | Same event triggers both |

**Overall: PARTIALLY DISTINCT.** 1/8 same, 5/8 partial, 2/8 distinct. The forced-adjustment mechanism is a genuine addition to the observational "drift" concept, but the observable and directional consequence are the same.

### 8.3 MECH-F03 vs Closest Prior (Gap Momentum / Settlement Windows)

| Dimension | MECH-F03 | Gap Momentum | Same / Partial / Distinct | Reason |
|-----------|----------|-------------|--------------------------|--------|
| Trigger | Overnight gap | Overnight gap | **SAME** | Both triggered by the same event |
| Participant behavior | Inventory rebalancing, gap traders, market makers | Not specified (gap direction) | **PARTIAL** | F03 specifies participants; gap momentum does not |
| Information mechanism | Positioning imbalance → rebalancing flow | Not specified | **PARTIAL** | F03 has a mechanism; gap momentum does not |
| Market-state transition | Overnight accumulation → opening rebalancing | Not specified | **PARTIAL** | F03 has a transition; gap momentum does not |
| Directional consequence | Follow the gap direction | Follow the gap direction | **SAME** | Both follow the same direction |
| Economic transmission | Rebalancing flow → continuation | Not specified | **PARTIAL** | F03 specifies transmission; gap momentum does not |
| Failure mode | Rebalancing may not occur | Not specified | **PARTIAL** | F03 specifies failure; gap momentum does not |
| Opportunity population | One per trading day | One per trading day | **SAME** | Same event triggers both |

**Overall: PARTIALLY DISTINCT.** 2/8 same, 5/8 partial, 0/8 distinct. The inventory-rebalancing mechanism is a genuine addition to simple gap-following, but the decision rule is functionally identical and the mechanism is not independently observable.

---

## 9. DUPLICATE ANALYSIS

### 9.1 MECH-F01

**Classification: PARTIALLY DISTINCT** (leaning toward DUPLICATE/REJECT)

The mechanism is identical to CAND-081. The difference is governance classification (decision process vs. observation). The distinctness is at the governance level, not the mechanism level. Under the strict mechanism-level standard, MECH-F01 is a repackaging of CAND-081 as a decision process.

However, the governance framework explicitly permits "a complete decision process built around the information one of them carries" as a "newly formulated concept" (BS1–BS13). The question is whether "newly formulated" requires mechanism-level novelty or merely governance-level novelty.

**Assessment:** The mechanism is not novel. The formulation is novel. Owner selection should understand this distinction.

### 9.2 MECH-F02

**Classification: PARTIALLY DISTINCT**

The forced-adjustment mechanism is a plausible interpretation that adds specificity to the observational "post-magnitude drift" concept. But the mechanism is not independently observable and cannot be distinguished from momentum continuation using available data. The trigger ("exceeds threshold") is empirical, not mechanistic.

### 9.3 MECH-F03

**Classification: PARTIALLY DISTINCT** (leaning toward DUPLICATE/REJECT)

The inventory-rebalancing mechanism is a plausible interpretation, but the decision rule is functionally identical to gap-following momentum. The mechanism does not produce a different observable, timing, or direction than simple gap-following. A mechanism-driven Base would need to demonstrate that the mechanism produces a distinct edge that gap-following alone does not.

---

## 10. BASE-001 CLOSURE PROTECTION

BASE-001 is CLOSED / NOT BASE-ELIGIBLE. Its Stage 3 LONG result must not be used to justify MECH-F01.

**Audit finding:** MECH-F01's "failed breakout → fade" is the EXACT SAME phenomenon that CAND-081 tested as a STATE OBSERVATION. CAND-081's governance review included a counterfactual comparing failed breakouts (trap formed) vs. successful breakouts (no trap). The failed-breakout → fade direction was specifically tested and found to have +1.23 bps conditional delta (better than successful breakouts).

MECH-F01 would be converting this CAND-081 observation into a Base. This is not a new mechanism — it is the same mechanism promoted from observation to decision process.

**Closure protection status:** The distinctness is at the governance level, not the mechanism level. The BASE-001 closure does not technically prohibit this (BASE-001 was about VALIDATED breakouts, not FAILED breakouts). But the CAND-081 observation is the same mechanism.

---

## 11. CAND-081 PROTECTION

CAND-081 is STATE REVIEW ELIGIBLE — PRESERVED. It must not be reopened.

**Audit finding:** MECH-F01 is the same mechanism as CAND-081, repackaged as a decision process. The mechanism definition, participant hypothesis, causal chain, and directional consequence are all identical.

**Does MECH-F01 reopen CAND-081?** Technically, no — MECH-F01 is a "newly formulated concept" under BS1–BS13, not a reopening of CAND-081. But the mechanism is the same. The governance framework permits this, but the distinctness audit must record the overlap.

**CAND-081 protection status:** Not technically violated. But the mechanism overlap is material and must be disclosed to the owner.

---

## 12. CANDIDATE VERDICTS

### MECH-F01 — Failed Breakout Inventory Reversal

| Dimension | Assessment |
|-----------|------------|
| Distinctness verdict | **PARTIALLY DISTINCT** — same mechanism as CAND-081, different governance classification |
| Nearest prior mechanism | CAND-081 (Structural Level Failure Trap) |
| Primary overlap | Identical causal chain: breakout → failure → trapped participants → forced liquidation → reversal |
| Primary distinction | MECH-F01 is a complete decision process; CAND-081 is a state observation. Governance-level difference, not mechanism-level difference. |
| Owner selection permitted? | **YES, WITH CAVEATS** — owner must understand the CAND-081 overlap |

### MECH-F02 — Shock-Induced Position Adjustment Cascade

| Dimension | Assessment |
|-----------|------------|
| Distinctness verdict | **PARTIALLY DISTINCT** — forced-adjustment mechanism is plausible but not independently observable |
| Nearest prior mechanism | Post-magnitude directional drift (exhausted) / CAND-077 (vol regime) |
| Primary overlap | Same observable (continued movement after large moves) as post-magnitude drift |
| Primary distinction | Forced-adjustment cascade is a specific mechanism, not just observational drift. But mechanism is not separately testable. |
| Owner selection permitted? | **YES, WITH CAVEATS** — owner must understand the mechanism is interpretive and not independently falsifiable |

### MECH-F03 — Overnight Gap Inventory Rebalancing

| Dimension | Assessment |
|-----------|------------|
| Distinctness verdict | **PARTIALLY DISTINCT** — mechanism is plausible but decision rule is gap-following momentum |
| Nearest prior mechanism | Gap-following momentum / Settlement windows (CAND-074/075) |
| Primary overlap | Decision rule (enter in gap direction at open) is functionally identical to gap-following momentum |
| Primary distinction | Inventory-rebalancing mechanism adds interpretation but does not change the observable or decision rule |
| Owner selection permitted? | **YES, WITH CAVEATS** — owner must understand the decision rule is gap-following with an interpretive overlay |

---

## 13. OVERALL OWNER-SELECTION RECOMMENDATION

**DISTINCTNESS AUDIT COMPLETE — ONE OR MORE CANDIDATES REQUIRE EXCLUSION/REFORMULATION**

**Detailed assessment:**

- **MECH-F01:** PARTIALLY DISTINCT. Same mechanism as CAND-081. Governance-level novelty only. Owner selection PERMITTED WITH CAVEATS.
- **MECH-F02:** PARTIALLY DISTINCT. Plausible mechanism but not independently observable. Owner selection PERMITTED WITH CAVEATS.
- **MECH-F03:** PARTIALLY DISTINCT. Decision rule is gap-following momentum. Owner selection PERMITTED WITH CAVEATS.

**No candidate is DISTINCT at the mechanism level.** All three are PARTIALLY DISTINCT, meaning some genuine mechanism difference exists but substantial overlap remains with prior research.

**The critical finding is MECH-F01:** Its mechanism is identical to CAND-081. The governance framework permits formulating a decision process around an existing observation, but the distinctness audit must record that the mechanism is not novel.

**Owner selection is authorized** for all three candidates, but the owner must be informed of:
1. MECH-F01's identity with CAND-081 at the mechanism level
2. MECH-F02's interpretive (not falsifiable) mechanism
3. MECH-F03's gap-following decision rule

---

## 14. GOVERNANCE COMPLIANCE

| Check | Result |
|-------|--------|
| No mechanism selected | PASS |
| No Base formulated | PASS |
| No parameters chosen | PASS |
| No economics calculated | PASS |
| No backtests run | PASS |
| No optimization performed | PASS |
| No thresholds mined | PASS |
| No protected-forward inspection | PASS |
| No BASE-001 reopened | PASS |
| No closed research reopened | PASS |
| No code modified | PASS |
| No runner touched | PASS |
| CAND-081 performance metrics not used | PASS — only mechanism definition used |
| BASE-001 Stage 3 LONG result not used to justify F01 | PASS |

---

## 15. FINAL VERDICT

**DISTINCTNESS AUDIT COMPLETE — ONE OR MORE CANDIDATES REQUIRE EXCLUSION/REFORMULATION**

Three candidates audited:
- MECH-F01: PARTIALLY DISTINCT (same mechanism as CAND-081)
- MECH-F02: PARTIALLY DISTINCT (interpretive mechanism, not independently observable)
- MECH-F03: PARTIALLY DISTINCT (decision rule is gap-following momentum)

No candidate achieves mechanism-level DISTINCT. All three are PARTIALLY DISTINCT with material overlaps to prior research. Owner selection is authorized with full disclosure of the overlap findings.

---

**END OF MECH-F DISTINCTNESS ADJUDICATION V1**
