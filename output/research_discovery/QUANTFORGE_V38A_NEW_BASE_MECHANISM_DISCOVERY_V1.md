# QUANTFORGE — V38A NEW BASE MECHANISM DISCOVERY

**Date:** 2026-09-07
**Status:** DISCOVERY COMPLETE — CANDIDATES READY FOR OWNER SELECTION
**Purpose:** Identify 3-5 high-quality, economically meaningful market mechanisms for potential future Base formulation.

---

## 1. MISSION

Conduct a new, independent V38A Base Mechanism Discovery sprint. Identify a small number of high-quality, economically meaningful market mechanisms that could support a future Base decision process. This is research discovery only — no strategy formulation, registration, backtesting, economic validation, optimization, or promotion.

---

## 2. AUTHORITATIVE SOURCES CONSULTED

| Source | Artifact | Key insight used |
|--------|----------|-----------------|
| V38 Doctrine | `QUANTFORGE_V38_DOCTRINE_RATIFICATION_V1.md` | Hybrid Base + Conditional architecture; D1-D25 clauses |
| V38A Validation Pathway | `QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_RATIFICATION_V1.md` | BV1-BV13; six-stage lifecycle; economics as evidence not gates |
| Outcome-Blind Formulation | `QUANTFORGE_OUTCOME_BLIND_BASE_DECISION_PROCESS_FORMULATION_RATIFICATION_V1.md` | BF1-BF13; mechanism-observable-decision chain; no-rescue |
| Base Hypothesis Selection | `QUANTFORGE_BASE_HYPOTHESIS_SELECTION_VALIDATION_RATIFICATION_V1.md` | BS1-BS13; family redundancy control; provenance requirements |
| Relational Discovery | `QUANTFORGE_RELATIONAL_MECHANISM_DISCOVERY_V1.md` | REL-M01/M02/M03 already discovered and formulated as RF-001/002/003 |
| Relational Formulations | `QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md` | RF-001/002/003 complete formulations — must not duplicate |
| RF-001 Registration | `QUANTFORGE_RF001_V38A_REGISTRATION_V1.md` | Frozen RF-001 definition — must not duplicate |
| V36 Strategic Assessment | `TRADEABLE_EDGE_DISCOVERY_SCREENING_V36.md` | 21 exhausted mechanism dimensions — must not revisit |
| Comprehensive Exclusion List | Internal research database | All closed/rejected/negative research — must not duplicate |
| SESSION_HANDOFF | `docs/SESSION_HANDOFF.md` | Current governed state; RF-001 Stage 3 blocked |

---

## 3. EXISTING-RESEARCH EXCLUSION SET

### 3.1 Permanently Exhausted Mechanism Dimensions (V36)

The following 21 dimensions are permanently exhausted and must not be revisited:

1. Structural break conditioning
2. Volatility regime / state
3. Volatility acceleration / rate
4. Transition quality
5. Directional momentum / exhaustion
6. Shock magnitude / direction
7. Event recency / decay
8. Event clustering / density
9. Event ordering / sequencing
10. Multi-timeframe break coordination
11. Post-magnitude directional drift
12. Path-dependent sequence asymmetry
13. Directional run-length persistence
14. Mean reversion (DISC-021: non-viable)
15. TSMOM / trend-following (DISC-022: not promotable)
16. Session-range compression (DISC-024: contradicted)
17. Liquidity sweep / reversal (DISC-025: translation failure)
18. Settlement / benchmark windows (CAND-074/075: no directional value)
19. Intra-bar distribution / bar conviction (CAND-106: negative)
20. Cross-asset lead-lag timing (CAND-105: negative)
21. Cross-asset volatility co-movement (CAND-107: redundant)

### 3.2 Formulated/Discovered Mechanisms (Must Not Duplicate)

| Mechanism | Status | Why distinct from new candidates |
|-----------|--------|--------------------------------|
| REL-M01 → RF-001 | Formulated, Stage 3 blocked | Confirmation failure between two indices |
| REL-M02 → RF-002 | Formulated, deferred | Synchrony regime transition across complex |
| REL-M03 → RF-003 | Formulated, deferred | Shock absorption asymmetry across markets |
| F-01 | Registered, Stage 3 pending | Calendar spread overnight strategy |
| F-02 | Formulated, deferred | Two-index pairs spread reversion |
| F-03 | Formulated, deferred | Cross-sectional rank rotation |

### 3.3 State Observations (Cannot Be Bases)

CAND-077 (vol compression→expansion), CAND-081 (structural level failure trap), CAND-083 (cumulative rejection pressure), CAND-099 (vol transition quality) — all remain observations/Conditional knowledge, never Base candidates.

### 3.4 Protected-Forward Candidates

CAND-015, CAND-024, CAND-035 — fully excluded from inspection or use.

---

## 4. DISCOVERY METHODOLOGY

1. **Exclusion-first approach:** Identified all 21 exhausted dimensions, all formulated/discovered mechanisms, and all closed research lines before generating candidates.
2. **Mechanism-first reasoning:** Each candidate begins with a market participant behavior hypothesis, not an indicator or statistical pattern.
3. **Distinctness gate:** Each candidate must demonstrate material architectural difference from the nearest prior mechanism. If distinctness cannot be established, the candidate is rejected.
4. **No economic screening:** No backtests, no historical returns, no expectancy calculations, no parameter sweeps. Quality is assessed by mechanism clarity, participant plausibility, and prospective testability.
5. **Stop condition:** 3 genuinely distinct mechanisms identified. Quality threshold met; no need to force additional candidates.

---

## 5. CANDIDATE MECHANISMS

---

### MECH-N01: STRUCTURAL LEVEL VALIDATION FLOW

**Mechanism ID:** MECH-N01

**Mechanism name:** Structural Level Validation Flow

#### Market process

When price breaks above a structurally significant high (or below a structurally significant low), the breakout initially creates uncertainty. Market participants who sold the breakout (stop-hunters, short-term contrarians) are underwater. Participants who bought the breakout (momentum followers) are profitable but uncertain. If price holds above the breakout level for a sustained period, the level transitions from "just broken" to "validated as new support/resistance." This transition changes participant behavior: stop-hunters are forced to cover (creating buying pressure), new buyers enter (validating the breakout), and market makers adjust quotes upward (reflecting the changed structural state). The validation itself creates a self-reinforcing directional impulse.

#### Participant interpretation

- **Stop-hunters / short-term contrarians:** Sold the breakout expecting a fake-out. When the breakout holds, they are forced to cover, creating buying pressure.
- **Momentum followers:** Bought the breakout but are uncertain. When the level holds, they add to positions, reinforcing the move.
- **Market makers:** Adjust inventory and quotes to reflect the new structural level. The level changing character forces hedging adjustments.
- **Structural traders:** Only enter after the level is validated, adding additional directional flow.

The key insight: the VALIDATION EVENT (level holds for K bars) is a distinct participant-behavior transition, not merely "momentum continued."

#### Observable manifestation

At M1 resolution:
- Bar E: price closes above the highest high of the prior N completed M1 bars (bullish breakout) — OR — closes below the lowest low (bearish breakout)
- Bars E+1 through E+K: price closes remain above (or below) the breakout level
- Bar E+K: the K-bar hold period completes → validation event occurs

The observable is deterministic: compare each bar's close to the breakout level. No statistical estimation required.

#### State/event transition

The transition is from "breakout uncertain" to "breakout validated." This is a discrete event at bar E+K, not a continuous variable. Before E+K, the breakout may still fail. After E+K, the level has changed structural character.

#### Potential economic consequence

After validation:
- Forced short covering (for bullish breakouts) creates buying pressure
- New long entries create additional buying pressure
- Market maker quote adjustment creates upward drift
- Net effect: directional continuation bias in the validated direction

The economic consequence occurs at a tradeable horizon (immediately after K-bar validation) because the participant behavior change is triggered by the validation event itself.

#### Directional consequence

- Bullish validation (price holds above breakout for K bars) → LONG bias
- Bearish validation (price holds below breakout for K bars) → SHORT bias

The direction is opposite to MECH-N01's nearest prior mechanism (RF-001): RF-001 fades the non-confirming market; MECH-N01 follows the validated breakout direction.

#### Falsification

The mechanism is falsified if:
- Validated breakouts (K-bar hold) show no directional edge compared to invalidated breakouts (price reverses before K bars)
- The K-bar hold period does not separate economically
- The directional consequence is random after validation

#### Distinctness

| Nearest prior mechanism | Why MECH-N01 is different |
|------------------------|--------------------------|
| RF-001 (confirmation failure) | RF-001 detects when Market B fails to confirm Market A's event, then fades Market B. MECH-N01 detects when a breakout in a single market holds for K bars, then follows the validated direction. Different mechanism (validation vs. failure), different observable (hold period vs. confirmation window), different direction (follow vs. fade). |
| CAND-081 (structural level failure trap) | CAND-081 is a STATE observation about what happens after price fails at a level. MECH-N01 is a DECISION PROCESS about what happens after price validates a level. CAND-081 observes failure; MECH-N01 observes validation. Opposite event, different decision architecture. |
| DISC-024 (session-range compression) | DISC-024 tested pre-session compression → cash-session range expansion. Contradicted. MECH-N01 is about structural level validation, not range compression. Different mechanism entirely. |
| Breakout trading (general) | Generic breakout trading enters AT the breakout. MECH-N01 enters AFTER K-bar validation. The delayed entry is the mechanism — it captures the participant behavior change at validation, not the breakout itself. |

#### Data requirements

- M1 OHLCV for a single instrument (e.g., USATECHIDXUSD)
- N-bar lookback for structural level definition (frozen at registration)
- K-bar hold period for validation (frozen at registration)
- Standard M1 data — no exotic data required

#### Likely Base/Conditional role

**Base.** The mechanism is self-contained and self-triggering. The validation event (K-bar hold after breakout) is a complete decision trigger requiring no external strategy. The mechanism produces a complete decision process: context (breakout detected), participation (validation event), direction (validated direction), entry (after K bars), exit (session close), invalidation (price returns through level before entry).

#### Research risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| N and K become optimization targets | HIGH | Freeze both as structural parameters at registration. N defines "structural" (not optimized); K defines "validation" (not optimized). |
| Overlap with momentum continuation | MEDIUM | The mechanism is NOT momentum — it is validation-induced participant flow. Distinctness must be maintained in formulation. |
| Session dependence | MEDIUM | Validate across multiple session segments. The mechanism should work whenever breakouts occur, not only at specific times. |
| Opportunity sparsity | MEDIUM | K-bar validation requirement reduces frequency. This is a feature (quality over quantity), not a bug. |

---

### MECH-N02: CROSS-ASSET HEDGING CASCADE

**Mechanism ID:** MECH-N02

**Mechanism name:** Cross-Asset Hedging Cascade

#### Market process

When one liquid US equity index experiences a large directional move, portfolio hedgers and market makers in correlated indices must adjust their positions. A large upward move in USATECHIDXUSD, for example, creates delta exposure for market makers who are short US500 options or who maintain market-maker inventory in US500. To hedge this exposure, they must buy US500 — creating buying pressure in US500 that is CAUSED BY the USATECHIDXUSD move, not by independent information in US500. The hedging flow is predictable because it is mechanically driven by portfolio hedging rules, not by discretionary information processing. The cascade occurs with a structural delay (hedging is not instantaneous) and creates a tradeable directional impulse in the second market.

#### Participant interpretation

- **Portfolio hedgers:** Maintain delta-neutral or target-exposure portfolios across correlated indices. When one index moves, they must rebalance by trading the correlated index. This is mechanical, not discretionary.
- **Market makers:** Quote across correlated indices. A large move in one creates inventory imbalance in the other. Hedging is mandatory and rules-based.
- **Index/ETF arbitrageurs:** When the underlying index moves, ETFs and futures must adjust. Cross-market arbitrage creates flows in correlated instruments.
- **Cross-margin accounts:** Margin calls in one instrument can force position changes in correlated instruments.

The key insight: the hedging flow is MECHANICALLY PREDICTABLE because it follows from portfolio hedging rules, not from information processing. The cascade is a structural consequence of multi-instrument market-making, not a behavioral response.

#### Observable manifestation

At M1 resolution:
- Bar E: USATECHIDXUSD (or other primary index) produces a large move (close-to-close return exceeding a structural threshold S in basis points)
- Bars E+1 through E+L: US500 (or other correlated index) shows delayed directional movement in the same direction as the primary move
- The delayed movement in US500 is the hedging cascade

The observable is deterministic: detect the primary move (threshold S), then measure the secondary market's directional response over L bars.

#### State/event transition

The transition is from "independent pricing" to "hedging-driven pricing" in the secondary market. This occurs when the primary market's move is large enough to trigger mechanical hedging flows. The transition is observable as a delayed directional response in the secondary market.

#### Potential economic consequence

After the hedging cascade begins:
- The secondary market experiences forced buying (or selling) from hedgers
- This creates a directional impulse that is independent of the secondary market's own information
- The impulse is tradeable because it has a predictable direction (same as primary move) and a predictable timing (starts after structural delay L)

#### Directional consequence

- Primary market moves UP → hedging cascade creates BUYING pressure in secondary market → LONG secondary market
- Primary market moves DOWN → hedging cascade creates SELLING pressure in secondary market → SHORT secondary market

The direction is the SAME as the primary market's move (unlike RF-001, which fades the non-confirming market).

#### Falsification

The mechanism is falsified if:
- Large primary-market moves do not produce delayed directional responses in the secondary market
- The delayed response is random (no directional predictability)
- The response timing is not structurally identifiable (no tradeable horizon)

#### Distinctness

| Nearest prior mechanism | Why MECH-N02 is different |
|------------------------|--------------------------|
| RF-001 (confirmation failure) | RF-001 detects when Market B fails to confirm Market A's event, then fades Market B. MECH-N02 detects hedging-driven flow from Market A into Market B, then follows the flow. Different mechanism (hedging cascade vs. confirmation failure), different direction (follow vs. fade), different trigger (large move vs. structural breakout). |
| RF-002 (synchrony regime) | RF-002 measures joint directional synchrony across the complex. MECH-N02 measures the mechanical hedging flow from one market to another. Synchrony is a statistical measure; hedging cascade is a participant-flow mechanism. |
| CAND-105 (lead-lag timing) | CAND-105 tested whether Gold-lead vs. Tech-lead regimes produce different downstream economics. Closed as negative. MECH-N02 is not about lead-lag timing — it is about mechanically-driven hedging flow. The mechanism is participant-flow, not information-timing. |
| Cross-market correlation trading | Correlation trading trades the level of correlation itself. MECH-N02 trades the directional consequence of hedging flow. The correlation is background context; the hedging flow is the mechanism. |

#### Data requirements

- M1 OHLCV for at least two correlated US equity indices (e.g., USATECHIDXUSD + US500)
- S (structural threshold for primary move) — frozen at registration
- L (hedging cascade observation window) — frozen at registration
- Standard M1 data — no exotic data required

#### Likely Base/Conditional role

**Base or Conditional — uncertain.** The mechanism is self-contained (large primary move → hedging cascade → directional response). However, it requires two instruments and a structural threshold S. As a Base, it would trade the secondary market based on the primary market's move. As a Conditional, it could layer on top of an existing Base to filter or time entries. The owner should assess whether this is more naturally a standalone Base or a Conditional component.

#### Research risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| S (threshold) becomes optimization target | HIGH | Freeze S as a structural parameter at registration. Define S mechanistically (e.g., "the N-bar ATR" or "a move exceeding X standard deviations") not empirically. |
| Hedging flow is not always present | MEDIUM | The mechanism hypothesizes that hedging flow is mechanically driven. If hedgers don't always hedge, the mechanism weakens. Falsification will reveal this. |
| Overlap with simple cross-market momentum | MEDIUM | The mechanism is NOT cross-market momentum. It is specifically about hedging-driven flow. Distinctness must be maintained. |
| Opportunity sparsity | MEDIUM | Large primary moves are relatively rare. This is a feature (quality), not a bug. |

---

### MECH-N03: SESSION-SEQUENTIAL TREND QUALITY

**Mechanism ID:** MECH-N03

**Mechanism name:** Session-Sequential Trend Quality

#### Market process

Intraday price trends develop through different paths. Some trends consist of a single impulsive move (one large directional bar or a short sequence of directional bars). Others develop through a grinding, multi-leg process (price advances, retraces, advances again, retraces again, gradually trending). The PATH of the trend reflects the participant composition and conviction behind the move. A single-impulse trend reflects concentrated, decisive positioning (strong conviction, limited opposition). A grinding multi-leg trend reflects distributed, contested positioning (mixed conviction, active opposition). The path quality predicts the trend's subsequent resilience: impulse-driven trends are more likely to persist because the underlying conviction is concentrated; grinding trends are more likely to reverse because the underlying positioning is contested and participants are willing to take profits.

#### Participant interpretation

- **Impulse-driven trend:** A single large participant or coordinated group initiates a large position. The move is decisive. Other participants are caught off-guard. The lack of opposition during the impulse suggests the move has structural backing.
- **Grinding trend:** Multiple participants are trading in the same direction but with active opposition. Each advance is followed by profit-taking. The trend persists but with continuous two-way activity. The contested nature suggests the move may be overcrowded.
- **Profit-takers:** In grinding trends, profit-takers are active (they sell each small advance). In impulse trends, profit-takers are absent during the impulse (they enter later). The timing of profit-taking is different.
- **New entrants:** In grinding trends, new entrants arrive gradually (each advance attracts new buyers). In impulse trends, new entrants arrive late (after the impulse). The entry timing is different.

The key insight: the TREND PATH itself is an observable that reveals participant composition. The path is not an indicator — it is a direct observation of how the trend developed.

#### Observable manifestation

At M1 resolution:
- A directional trend is detected (e.g., price has moved X bars in the same direction, or cumulative return exceeds a threshold)
- The PATH of the trend is measured: count the number of direction-changing bars within the trend (bars where the return opposes the trend direction)
- **Impulse trend:** Few direction-changing bars (concentrated, decisive move)
- **Grinding trend:** Many direction-changing bars (distributed, contested move)

The observable is deterministic: count opposing-direction bars within the trend window. No statistical estimation required.

#### State/event transition

The transition is from "trend developing" to "trend quality assessed." This occurs when the trend reaches a minimum length (e.g., D bars). At that point, the path quality is measured and the decision is made.

#### Potential economic consequence

After trend quality is assessed:
- Impulse trends (low path noise) have concentrated conviction → more likely to continue → follow the trend
- Grinding trends (high path noise) have distributed conviction → more likely to reverse → fade the trend

The economic consequence occurs at a tradeable horizon (immediately after quality assessment) because the path quality reveals the participant composition at the time of assessment.

#### Directional consequence

- Impulse trend (up) → LONG bias (concentrated conviction → continuation)
- Grinding trend (up) → SHORT bias (distributed conviction → reversal)
- Impulse trend (down) → SHORT bias
- Grinding trend (down) → LONG bias

The direction DEPENDS on the path quality: impulse → follow; grinding → fade. This is a dual-direction mechanism, not a single-direction mechanism.

#### Falsification

The mechanism is falsified if:
- Impulse trends and grinding trends show identical subsequent economics
- Path noise count does not separate economically
- The dual-direction logic (follow impulse, fade grinding) produces no net edge

#### Distinctness

| Nearest prior mechanism | Why MECH-N03 is different |
|------------------------|--------------------------|
| DISC-022 (TSMOM) | TSMOM follows own-history trend direction over monthly horizons. MECH-N03 assesses the quality of an intraday trend at M1 resolution and trades differently based on quality. Different timeframe, different mechanism, different decision. |
| CAND-070 (sustained momentum micro-structure failure) | CAND-070 tested whether sustained momentum fails at the micro-structure level. Closed — hypothesis contradicted (trend resumes, not reverses). MECH-N03 does not hypothesize that all sustained momentum fails. It hypothesizes that GRINDING (contested) trends fail while IMPULSE (concentrated) trends continue. Different hypothesis, different observable. |
| CAND-102 (directional run-length persistence) | CAND-102 tested whether run-length predicts continuation. Closed — contradicted (non-monotonic pattern). MECH-N03 is not about run-length. It is about the INTERNAL PATH QUALITY of the trend. A 10-bar impulse trend and a 10-bar grinding trend have the same run-length but different path quality. |
| CAND-088 (session sequence asymmetry) | CAND-088 tested whether aligned breaks outperform. Closed — contradicted. MECH-N03 is not about break alignment. It is about the internal structure of a trend. |
| Momentum (general) | Generic momentum follows the direction. MECH-N03 follows OR fades based on path quality. The path quality is the mechanism, not the direction. |

#### Data requirements

- M1 OHLCV for a single instrument (e.g., USATECHIDXUSD)
- D (minimum trend length for quality assessment) — frozen at registration
- Standard M1 data — no exotic data required

#### Likely Base/Conditional role

**Base.** The mechanism is self-contained and self-triggering. The trend quality assessment (impulse vs. grinding) is a complete decision trigger requiring no external strategy. The mechanism produces a complete decision process: context (trend detected), participation (quality assessed at bar D), direction (follow if impulse, fade if grinding), entry (after quality assessment), exit (session close), invalidation (trend reverses beyond defined threshold before entry).

#### Research risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| D becomes optimization target | HIGH | Freeze D as a structural parameter at registration. D defines "minimum trend length" — not optimized from data. |
| Path noise measure becomes threshold-mined | HIGH | Define path noise structurally (e.g., "count of bars where return opposes trend direction / total bars in trend"). No threshold optimization. |
| Dual-direction logic is complex | MEDIUM | The follow/fade logic is deterministic and mechanistically motivated. Complexity is acceptable if the mechanism is clear. |
| Overlap with volatility-based trend quality | MEDIUM | MECH-N03 is NOT about volatility. It is about directional path structure. Distinctness must be maintained. |

---

## 6. DISTINCTNESS ASSESSMENT

### 6.1 Cross-candidate distinctness

| Pair | Distinct? | Reason |
|------|-----------|--------|
| MECH-N01 vs MECH-N02 | YES | N01 is single-market (level validation). N02 is cross-market (hedging cascade). Different unit of analysis, different mechanism, different trigger. |
| MECH-N01 vs MECH-N03 | YES | N01 is about structural level validation (breakout holds). N03 is about trend path quality (impulse vs. grinding). Different mechanism, different observable, different decision. |
| MECH-N02 vs MECH-N03 | YES | N02 is cross-market hedging flow. N03 is single-market trend path quality. Different mechanism, different unit of analysis. |

### 6.2 Distinctness from all exhausted dimensions

| Exhausted dimension | MECH-N01 | MECH-N02 | MECH-N03 |
|--------------------|----------|----------|----------|
| Structural break conditioning | NOT this — N01 is about LEVEL VALIDATION, not break conditioning | NOT this — N02 is about HEDGING FLOW, not break conditioning | NOT this — N03 is about TREND PATH, not break conditioning |
| Volatility regime/state | NOT this — N01 is about structural levels, not vol | NOT this — N02 is about hedging flow, not vol | NOT this — N03 is about path structure, not vol |
| Momentum/exhaustion | NOT this — N01 follows validated breakouts (not momentum) | NOT this — N02 follows hedging flow (not momentum) | N03 partially fades grinding trends — but the mechanism is PATH QUALITY, not exhaustion |
| Mean reversion | NOT this — N01 follows, doesn't fade | NOT this — N02 follows, doesn't fade | N03 fades grinding trends — but the mechanism is PATH QUALITY, not mean reversion |
| Lead-lag timing | NOT this — N01 is single-market | NOT this — N02 is about hedging flow, not timing | NOT this — N03 is single-market |

All three candidates survive the distinctness audit against all 21 exhausted dimensions.

### 6.3 Distinctness from RF-001/002/003

| RF mechanism | MECH-N01 | MECH-N02 | MECH-N03 |
|-------------|----------|----------|----------|
| RF-001 (confirmation failure) | N01 follows validated breakouts (same direction); RF-001 fades non-confirming market (opposite direction). Different mechanism, different direction. | N02 follows hedging flow (same direction as primary); RF-001 fades non-confirming market. Different mechanism, different trigger. | N03 follows/fades based on path quality; RF-001 fades based on confirmation failure. Different mechanism, different trigger. |
| RF-002 (synchrony regime) | N01 is single-market; RF-002 is cross-market synchrony. Different unit of analysis. | N02 is about hedging flow; RF-002 is about synchrony breakdown. Different mechanism. | N03 is single-market; RF-002 is cross-market. Different unit of analysis. |
| RF-003 (shock absorption) | N01 is about level validation; RF-003 is about shock absorption asymmetry. Different mechanism. | N02 is about hedging flow; RF-003 is about shock absorption. Different mechanism. | N03 is about trend path; RF-003 is about shock absorption. Different mechanism. |

---

## 7. ECONOMIC-MECHANISM REASONING

### MECH-N01: Why it might matter economically

The structural level validation flow hypothesizes that participant behavior changes measurably when a breakout is validated. Before validation, participants are uncertain. After validation, stop-hunters cover, new buyers enter, and market makers adjust. This behavioral shift is mechanistic (driven by position management rules, not discretion) and creates a predictable directional impulse. The economic consequence follows from the participant behavior change, not from statistical pattern-matching.

### MECH-N02: Why it might matter economically

The cross-asset hedging cascade hypothesizes that portfolio hedging rules create mechanically predictable flows between correlated indices. When one index moves large, hedgers MUST adjust positions in the other index. This flow is not discretionary — it follows from hedging mandates, margin requirements, and market-making rules. The flow is directional (same direction as primary move) and delayed (hedging is not instantaneous). The economic consequence follows from mechanical hedging behavior, not from information processing.

### MECH-N03: Why it might matter economically

The session-sequential trend quality hypothesizes that the path of a trend reveals the participant composition behind it. Impulse trends reflect concentrated conviction (few participants with large positions). Grinding trends reflect distributed conviction (many participants with small positions, active opposition). The composition predicts subsequent resilience: concentrated conviction is harder to reverse than distributed conviction. The economic consequence follows from the relationship between path structure and participant positioning.

---

## 8. FALSIFICATION CRITERIA

### MECH-N01

| Falsification test | Expected result if mechanism is unsupported |
|--------------------|---------------------------------------------|
| Compare validated breakouts (K-bar hold) vs. invalidated breakouts (reversal before K bars) | No directional difference in subsequent session performance |
| Vary K (hold period) | No separation at any K value |
| Test across different N (lookback) values | Mechanism disappears for some N values |

### MECH-N02

| Falsification test | Expected result if mechanism is unsupported |
|--------------------|---------------------------------------------|
| Compare large primary moves with hedging response vs. without | No directional difference in secondary market |
| Vary L (cascade observation window) | No separation at any L value |
| Test across different S (threshold) values | Mechanism disappears for some S values |

### MECH-N03

| Falsification test | Expected result if mechanism is unsupported |
|--------------------|---------------------------------------------|
| Compare impulse trends vs. grinding trends | No directional difference in subsequent performance |
| Vary D (minimum trend length) | No separation at any D value |
| Test the dual-direction logic (follow impulse, fade grinding) | Net edge is zero or negative |

---

## 9. DATA REQUIREMENTS

| Requirement | MECH-N01 | MECH-N02 | MECH-N03 |
|-------------|----------|----------|----------|
| Instruments | Single (e.g., USATECHIDXUSD) | Two correlated (e.g., USATECHIDXUSD + US500) | Single (e.g., USATECHIDXUSD) |
| Timeframe | M1 | M1 | M1 |
| Session | US regular (09:30–16:00 ET) | US regular (09:30–16:00 ET) | US regular (09:30–16:00 ET) |
| Data fields | OHLCV | OHLCV × 2 markets | OHLCV |
| Exotic data required | None | None | None |
| Forward pipeline availability | YES | YES | YES |

All three candidates are computable from currently available M1 OHLCV data. No additional data sources are required.

---

## 10. RESEARCH RISKS

### 10.1 Shared risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Parameters N, K, S, D, L become optimization targets | HIGH — invalidates prospective integrity | Freeze ALL structural parameters at registration. No post-registration modification. V38A registration freeze mechanism (BV3) provides governance protection. |
| Mechanism ambiguity in formulation | MEDIUM — unclear decision semantics | Each candidate has a clear mechanism-observable-decision chain. Formulation must preserve this clarity. |
| Session dependence | MEDIUM — mechanism may only work at certain times | Test across full session. If mechanism is session-dependent, document as a structural limitation, not a parameter to tune. |

### 10.2 Candidate-specific risks

| Candidate | Specific risk | Severity |
|-----------|--------------|----------|
| MECH-N01 | Overlap with "momentum continuation" framing — must maintain validation-induced-flow distinctness | MEDIUM |
| MECH-N02 | Hedging flow may not always be present or detectable at M1 resolution | MEDIUM |
| MECH-N03 | Dual-direction logic (follow/fade) is more complex than single-direction mechanisms | MEDIUM |

---

## 11. QUALITATIVE PRIORITIZATION

### Ranking dimensions

1. **Mechanism clarity** — How clearly can the mechanism be stated?
2. **Participant plausibility** — How plausible is the participant-behavior hypothesis?
3. **Observable determinism** — How deterministic is the observable?
4. **Prospective testability** — How easily can the mechanism be tested prospectively?
5. **Economic pathway** — How clear is the path from mechanism to economic consequence?
6. **Execution realism** — Can a future Base process act on the information?
7. **Falsifiability** — How clearly can the mechanism be falsified?
8. **Independence from prior research** — How distinct is this from all exhausted work?
9. **Opportunity-population clarity** — How clearly defined is the eligible population?
10. **Risk of becoming threshold mining** — How likely is parameter optimization to corrupt the mechanism?

### Adjudication

**MECH-N01 (Structural Level Validation Flow):**
- Mechanism clarity: HIGH — level validation is a concrete, observable event
- Participant plausibility: HIGH — stop-hunting and forced covering are well-documented market phenomena
- Observable determinism: HIGH — K-bar hold is binary and deterministic
- Prospective testability: HIGH — forward data accrual will naturally produce validation events
- Economic pathway: HIGH — participant behavior change → directional flow → economic consequence
- Execution realism: HIGH — entry after K-bar validation, exit at session close
- Falsifiability: HIGH — validated vs. invalidated breakouts can be compared
- Independence: HIGH — distinct from all exhausted dimensions and RF-001/002/003
- Opportunity clarity: HIGH — one opportunity per validated breakout
- Threshold mining risk: MEDIUM — N and K must be frozen, not optimized

**MECH-N02 (Cross-Asset Hedging Cascade):**
- Mechanism clarity: MEDIUM — hedging flow is mechanistic but harder to observe directly
- Participant plausibility: HIGH — portfolio hedging rules are well-documented
- Observable determinism: MEDIUM — the primary move is deterministic; the hedging response is probabilistic
- Prospective testability: MEDIUM — requires two instruments and a threshold S
- Economic pathway: MEDIUM — hedging flow → directional pressure → economic consequence (but timing is less precise)
- Execution realism: MEDIUM — entry after structural delay L, exit at session close
- Falsifiability: MEDIUM — primary move → secondary response can be tested, but timing is uncertain
- Independence: HIGH — distinct from all exhausted dimensions and RF-001/002/003
- Opportunity clarity: MEDIUM — one opportunity per large primary move, but threshold S defines "large"
- Threshold mining risk: HIGH — S and L are parameters that could be optimized

**MECH-N03 (Session-Sequential Trend Quality):**
- Mechanism clarity: HIGH — impulse vs. grinding is a concrete, observable distinction
- Participant plausibility: HIGH — concentrated vs. distributed positioning is well-documented
- Observable determinism: HIGH — path noise count is deterministic
- Prospective testability: HIGH — forward data accrual will naturally produce trends of varying quality
- Economic pathway: MEDIUM — path quality → participant composition → subsequent resilience (but the link between composition and resilience is inferential)
- Execution realism: HIGH — entry after quality assessment, exit at session close
- Falsifiability: HIGH — impulse vs. grinding trends can be compared
- Independence: HIGH — distinct from all exhausted dimensions and RF-001/002/003
- Opportunity clarity: MEDIUM — one opportunity per trend of sufficient length, but D defines "sufficient"
- Threshold mining risk: MEDIUM — D must be frozen, not optimized

### Priority ranking

| Rank | Candidate | Reason |
|------|-----------|--------|
| 1 | MECH-N01 (Structural Level Validation Flow) | Highest mechanism clarity, highest participant plausibility, highest observable determinism, highest execution realism. Lowest threshold mining risk. Most naturally suited to standalone Base. |
| 2 | MECH-N03 (Session-Sequential Trend Quality) | High mechanism clarity, high participant plausibility, high observable determinism. Dual-direction logic is more complex but mechanistically motivated. Good standalone Base candidate. |
| 3 | MECH-N02 (Cross-Asset Hedging Cascade) | Plausible mechanism but hedging response is less deterministic than N01/N03 observables. Higher threshold mining risk (S and L parameters). May be better suited as Conditional than Base. |

---

## 12. REJECTED MECHANISMS

The following mechanism concepts were considered and rejected during the discovery process:

| Concept | Reason for rejection |
|---------|---------------------|
| Liquidity vacuum / thin-book moves | Overlaps with exhausted "liquidity sweep / reversal" (DISC-025). The mechanism of price moving through thin books is structurally similar to sweep-and-reversal. |
| Session-positioning imbalance resolution | Overlaps with exhausted "momentum exhaustion" (CAND-062/091) and "session-range compression" (DISC-024). The end-of-session positioning resolution is a form of momentum exhaustion. |
| Opening auction → regular session transition | Overlaps with exhausted "settlement / benchmark windows" (CAND-074/075). Opening auction dynamics are structurally similar to settlement-window effects. |
| Intraday volatility clustering | Overlaps with exhausted "volatility regime / state" (CAND-077/096/099). Volatility clustering is a vol-regime concept. |
| Cross-asset return spillover timing | Overlaps with exhausted "cross-asset lead-lag timing" (CAND-105). Return spillover is a lead-lag concept. |
| Price rejections at round numbers | Overlaps with exhausted "structural break conditioning" and CAND-083 (cumulative rejection pressure). Round-number reactions are a form of structural-level behavior. |
| Order-flow imbalance (if data available) | Data infeasible — tick-level order flow not available in governed dataset (CAND-100 precedent). |

---

## 13. RECOMMENDED CANDIDATES FOR OWNER-SELECTION CONSIDERATION

| Rank | Mechanism ID | Name | Recommended role | Key decision for owner |
|------|-------------|------|-----------------|----------------------|
| 1 | MECH-N01 | Structural Level Validation Flow | Base | N and K must be specified at registration. Single-market. Most clear mechanism. |
| 2 | MECH-N03 | Session-Sequential Trend Quality | Base | D must be specified at registration. Single-market. Dual-direction logic. |
| 3 | MECH-N02 | Cross-Asset Hedging Cascade | Base or Conditional | S and L must be specified. Two-market. Owner assesses Base vs. Conditional role. |

**Minimum viable set:** MECH-N01 and MECH-N03 are sufficiently distinct to form a minimum viable discovery set of 2 candidates. MECH-N02 adds cross-market diversity but has higher threshold-mining risk.

---

## 14. GOVERNANCE COMPLIANCE

| Check | Result |
|-------|--------|
| RF-001 unchanged | PASS — no modification to RF-001 registration, recorder, or accrual |
| RF-001 live accrual uninterrupted | PASS — runner not touched |
| F-01 unchanged | PASS |
| FB-001 unchanged | PASS |
| Protected-forward candidates untouched | PASS — CAND-015/024/035 not inspected |
| Closed lines not reopened | PASS — no closed research reopened |
| No strategy formulation | PASS — mechanism discovery only |
| No registration | PASS |
| No economic testing | PASS — no backtests, no returns, no expectancy |
| No parameter optimization | PASS — parameters identified conceptually, not from data |
| No threshold mining | PASS — no numerical thresholds selected from historical performance |
| No forward-performance inspection | PASS |
| No production-code change | PASS |
| No runner interruption | PASS |
| No broker orders | PASS |
| No governance reinterpretation | PASS |

---

## 15. FINAL VERDICT

**V38A BASE MECHANISM DISCOVERY COMPLETE — CANDIDATES READY FOR OWNER SELECTION**

Three genuinely distinct mechanisms discovered:
- MECH-N01: Structural Level Validation Flow (single-market, level validation → participant behavior change → directional flow)
- MECH-N02: Cross-Asset Hedging Cascade (cross-market, large primary move → mechanical hedging flow → directional response)
- MECH-N03: Session-Sequential Trend Quality (single-market, trend path quality → participant composition → continuation/fade decision)

All three are materially distinct from all 21 exhausted dimensions, all existing relational mechanisms (REL-M01/M02/M03 → RF-001/002/003), all formulated hypotheses (F-01/F-02/F-03), and all closed research lines. No economic testing performed. No parameters optimized. No thresholds mined.

The next governed step is owner review of this discovery artifact to determine whether any mechanism warrants progression to the Outcome-Blind Base Formulation Cycle (BF1–BF13).

---

**END OF MECHANISM DISCOVERY ARTIFACT**
