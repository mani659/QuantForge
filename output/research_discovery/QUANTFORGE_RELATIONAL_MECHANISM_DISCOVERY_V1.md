# QUANTFORGE — RELATIONAL MECHANISM DISCOVERY
# OUTCOME-BLIND MECHANISM DISCOVERY — PRE-FORMULATION

**Date:** 2026-09-07
**Status:** DISCOVERY COMPLETE — FORMULATION CYCLE NOT YET STARTED
**Track:** Relational Research

---

## 1. RESEARCH MISSION

Investigate whether a relationship between distinct markets can provide information about a market-state transition, timing asymmetry, directional response, or structural dependency that is sufficiently deterministic and economically interpretable to become a standalone decision process under the QuantForge Outcome-Blind Formulation Framework.

This is pre-formulation discovery only. No strategies are registered. No economic testing is performed. No parameters are selected.

---

## 2. GOVERNING DOCTRINE

This research track operates under:

- V38 Doctrine (Hybrid Base + Conditional)
- Outcome-Blind Base Formulation Pathway (BF1–BF13)
- Base Hypothesis Selection Framework (BS1–BS13)
- V38A Base Validation Pathway (BV1–BV13)
- Relational Research Framework V1 (admission/exclusion rules inherited into V38)

**Constraints:**
- Base Registry remains EMPTY
- No historical economic performance is used to rank or select mechanisms
- No FB-001 economics inspected
- No F-01 economics inspected
- No protected-forward economics inspected
- No parameters are chosen
- No backtesting is performed
- No optimization is performed
- Closed research lines are not reopened

---

## 3. RELATIONAL PRIOR-KNOWLEDGE MAP

| Item | Mechanism | Status | Why it matters now |
|------|-----------|--------|-------------------|
| F-02 | Two-index relative-value pairs (spread reversion) | FORMULATED — DEFERRED | Cross-market by design. Deferred due to pair-identity underdetermination. Represents the relative-pricing family. |
| F-03 | Cross-sectional relative-strength rotation (4-index rank) | FORMULATED — DEFERRED | Cross-market by design. Deferred due to daily full-turnover cost dominance. Represents the ranking family. |
| SEED-002 | CAND-083 precondition × CAND-081 trapped-participant relational test | CLOSED — NEGATIVE | The only executed relational experiment. Result: CAND-083 precondition makes CAND-081 worse. Established the no-rescue doctrine (Clause D8). |
| CAND-083 | Cumulative rejection pressure at structural levels | STATE REVIEW ELIGIBLE | Single-market (USATECHIDXUSD). Input A for SEED-002. Not itself cross-market. |
| CAND-105 | Cross-asset lead-lag asymmetry (Gold/Tech M1) | CLOSED — NEGATIVE | Mean delta +0.35 bps, not significant. Gold-lead and tech-lead regimes produce identical downstream tech economics. Genuine negative finding for M1 lead-lag. |
| CAND-107 | Cross-asset volatility co-movement regime | CLOSED — REDUNDANT | Collapsed into existing vol regime family (CAND-077/096/099). Cross-asset vol correlation already covered. |
| DISC-021 | Mean reversion (5 markets) | CLOSED — NON-VIABLE | Transaction costs consume entire gross effect. Established cost-boundary discipline. |
| DISC-022 | TSMOM 12/1 (28+5 markets) | CLOSED — NOT PROMOTABLE | Cross-era directional consistency failure. Contemporary replication contradicts historical. |
| DISC-013 | Cross-market universality claim | PARTIALLY IMPLEMENTED | Historical cross-market validation foundation. Operational line closed. |
| Relational Framework V1 | Governance architecture for relational testing | ESTABLISHED — INHERITED INTO V38 | Defines admission/exclusion rules, incremental information framework, counterfactual requirements. |
| V38 Doctrine | Hybrid Base + Conditional architecture | RATIFIED | Highest-level doctrine. Hosts HTF→LTF relational stacks. No relational experiment before Base registry entry. |

**Key insight:** F-02 and F-03 are the only formulated hypotheses that are inherently cross-market. All prior cross-market tests (DISC-013, DISC-021, DISC-022, CAND-105) were retrospective findings, not decision processes. The relational research track must produce mechanisms that are decision-process-ready, not merely observational.

---

## 4. TAXONOMY OF RELATIONAL MECHANISMS

### What counts as "relational"

A relational mechanism involves two or more distinct markets where the relationship itself is the source of decision-relevant information. The taxonomy distinguishes:

**Level 1 — Relational Observation:**
> Two markets tend to move together.

Not decision-relevant. Descriptive only.

**Level 2 — Relational State:**
> A normally synchronous relationship has entered an unusual asynchronous state.

Potentially informative but not yet a decision.

**Level 3 — Relational Event:**
> Market A makes a defined transition while Market B fails to respond within a defined structural sequence.

Potentially decision-relevant. The event itself is the trigger.

**Level 4 — Relational Decision Process:**
> When a predefined relationship event occurs under predefined context, take action X under predefined execution rules.

This is the level required for Base formulation.

### Mechanism categories considered

| Category | Description | Example |
|----------|-------------|---------|
| Lead/lag | One market undergoes an event; a related market has not yet responded | Index A breaks structure; Index B has not yet responded |
| Synchrony breakdown | Two normally related markets transition from synchronous to asynchronous state | Correlation regime shift between two indices |
| Cross-market state handoff | Market A enters a new state; Market B subsequently transitions in a repeatable manner | Volatility shock in one market propagates with structural delay to another |
| Relative shock absorption | One market experiences a shock; another absorbs it differently | External event hits both; one absorbs, one rejects |
| Confirmation failure | Market A produces a structural event; Market B explicitly fails to confirm | Breakout in Index A; Index B fails to confirm the breakout |
| Conditional dependency | The behavior of Market B depends on the state of Market A | Trend in Market B is only valid when Market A is in a specific regime |

### Categories rejected

| Category | Reason for rejection |
|----------|---------------------|
| Simple correlation | collapses into observation (Level 1), not decision (Level 4) |
| Pairs mean reversion | already covered by F-02 (deferred, not new) |
| Cross-sectional ranking | already covered by F-03 (deferred, not new) |
| Volatility correlation | already covered by CAND-077/096/099 (closed, redundant per CAND-107) |

---

## 5. MECHANISM QUALITY CRITERIA

Every proposed mechanism must pass:

### A. Distinctness
Why is this not merely mean reversion, momentum, breakout, correlation trading, cross-sectional ranking, a rebranded F-02, a rebranded F-03, or an already-tested CAND-083 mechanism?

### B. Causal/behavioral interpretation
What participant or market-structure behavior could create the relationship? Labeled as MECHANISTIC HYPOTHESIS, not established fact.

### C. Observable manifestation
What exact market observation would reveal the mechanism? Must be measurable from available data.

### D. Decision relevance
How could the observable eventually become a deterministic decision? No "use as confirmation" — define what action could conceptually follow.

### E. Falsifiability
What observation would make the mechanism unsupported?

---

## 6. CANDIDATE MECHANISMS

### REL-M01: Cross-Market Confirmation Failure

**Behavioral hypothesis:** When a structurally significant price event occurs in one liquid US equity index (e.g., a breakout above a defined high, a break below a defined low, or a session-range expansion), correlated indices typically confirm the move within a structurally defined window. When confirmation explicitly fails — the correlated index does not produce the expected confirming event within the expected window — the failure itself represents a distinct market-state transition. The non-confirming market has absorbed or rejected the information that drove the confirming market, suggesting a structural divergence in participant positioning or information.

**Relationship structure:** US equity index complex (USATECHIDXUSD, US500, US30, US2000, or subsets). The relationship is between the "leading" index (the one that produces the structural event) and the "lagging" index (the one expected to confirm).

**Observable:** Index A produces a defined structural event (e.g., new session high, range expansion, break of a defined level). Index B does not produce a corresponding confirming event within a defined structural window (e.g., N bars, rest of session, next session open).

**Event/state transition:** Confirmation failure — the moment when the expected confirmation window closes without Index B confirming Index A's event.

**Candidate decision concept:** When confirmation failure is detected, the non-confirming index may be in a structurally different state than the confirming index. A deterministic decision could involve: (a) fading the non-confirming index's direction if the failure suggests absorption, or (b) avoiding directional exposure in the non-confirming index if the failure suggests structural weakness.

**Distinctness argument:** This is NOT F-02 (which trades spread convergence between two indices). This is NOT F-03 (which ranks indices by relative strength). This is NOT mean reversion (which fades displacement toward a mean). This is NOT CAND-105 (which tested whether Gold-lead vs Tech-lead regimes produce different downstream economics — a lead-lag timing question, not a confirmation-failure question). This is NOT CAND-083 (which is single-market cumulative rejection pressure). The mechanism is specifically about the failure of one market to confirm another market's structural event — the failure itself is the signal, not the relative pricing or timing.

**Data feasibility:** Available. USATECHIDXUSD and other US equity index M1 data exists in the forward pipeline. Timestamp alignment is feasible at M1 resolution. Market hours overlap is perfect (all US equity indices trade the same sessions).

**Main falsification route:** If confirmation failures are随机 and do not predict any structural state difference in the non-confirming index, the mechanism is unsupported. If the non-confirming index's subsequent behavior is statistically identical regardless of whether confirmation occurred, the mechanism is falsified.

**Main governance risk:** Specification drift in defining "structural event" and "confirmation window." The mechanism must be formulated with frozen definitions before any economic testing.

---

### REL-M02: Synchrony Regime Transition

**Behavioral hypothesis:** Two or more liquid US equity indices normally move with high intraday synchrony (similar direction, similar magnitude). When synchrony breaks down — one index moves materially while others do not, or indices move in opposite directions — the desynchronized state represents a distinct market regime. The mechanism is that synchrony breakdown reflects a genuine difference in participant flow, information processing, or positioning between the indices, not random noise. The breakdown is observable and potentially predictive of a structural transition in the desynchronized index.

**Relationship structure:** US equity index complex. The relationship is the joint movement pattern across indices, not the relative pricing of any pair.

**Observable:** A synchrony measure (e.g., correlation of returns over a rolling window, or a directional agreement measure across the index complex) transitions from a "synchronized" regime to a "desynchronized" regime. The transition is defined by a structural threshold, not a statistical parameter.

**Event/state transition:** The moment when the synchrony measure crosses from synchronized to desynchronized. This is a regime transition, not a continuous variable.

**Candidate decision concept:** When the index complex enters a desynchronized regime, the individual indices may be in structurally different states. A deterministic decision could involve: (a) reducing exposure to the index that is diverging from the complex (if divergence suggests vulnerability), or (b) increasing exposure to the index that is leading the complex (if leadership is persistent).

**Distinctness argument:** This is NOT correlation trading (which trades convergence of correlation itself). This is NOT F-02 (which trades a specific pair's spread). This is NOT F-03 (which ranks by relative strength — a different measure than synchrony). This is NOT CAND-107 (which tested cross-asset vol co-movement and was closed as redundant with vol regime research). The mechanism is specifically about the transition between synchrony regimes in the joint behavior of the index complex, not about the level of correlation or the relative pricing of any pair.

**Data feasibility:** Available. Multiple US equity index M1 data series exist. Synchrony can be measured from overlapping session data. No exotic data required.

**Main falsification route:** If synchrony breakdowns are random and do not predict any structural difference in subsequent index behavior, the mechanism is unsupported. If the desynchronized regime has identical subsequent economics to the synchronized regime, the mechanism is falsified.

**Main governance risk:** Parameter drift in defining the synchrony measure and the regime threshold. The synchrony measure must be structurally defined (e.g., directional agreement across N indices) rather than statistically estimated (e.g., rolling correlation with a lookback).

---

### REL-M03: Cross-Market Shock Absorption Asymmetry

**Behavioral hypothesis:** When an external-looking event (e.g., a sudden price move, a news-driven gap, or a volatility spike) affects multiple correlated markets simultaneously, the markets absorb the shock differently. One market may absorb the shock quickly (price stabilizes, volatility returns to normal), while another may absorb it slowly (price continues moving, volatility remains elevated). The asymmetry in absorption reflects a structural difference in participant composition, liquidity, or information processing between the markets. The absorption characteristics are observable and may predict the subsequent trajectory of the slow-absorbing market.

**Relationship structure:** US equity index complex. The relationship is between the shock-absorption characteristics of different indices, not their relative pricing.

**Observable:** An external-looking shock is detected (e.g., a sudden large move across multiple indices). The absorption characteristic of each index is measured (e.g., time to stabilize, magnitude of overshoot, volatility persistence). The asymmetry between indices is the observable.

**Event/state transition:** The moment when the absorption asymmetry exceeds a defined structural threshold — one index has clearly absorbed the shock while the other has not.

**Candidate decision concept:** When absorption asymmetry is detected, the slow-absorbing index may be in a structurally different state than the fast-absorbing index. A deterministic decision could involve: (a) reducing exposure to the slow-absorbing index (if slow absorption suggests structural vulnerability), or (b) waiting for the slow-absorbing index to complete absorption before taking directional exposure.

**Distinctness argument:** This is NOT mean reversion (which fades displacement toward a mean — absorption asymmetry is about the process of stabilization, not the direction of movement). This is NOT CAND-105 (which tested lead-lag timing, not absorption characteristics). This is NOT CAND-107 (which tested vol co-movement, not absorption asymmetry). This is NOT volatility regime trading (which trades the level of volatility, not the asymmetry in absorption across markets). The mechanism is specifically about how different markets absorb the same shock, not about the shock itself or the subsequent volatility level.

**Data feasibility:** Available. Multiple US equity index M1 data series exist. Shock detection and absorption measurement can be computed from M1 data. No exotic data required.

**Main falsification route:** If absorption asymmetry is random and does not predict any structural difference in subsequent index behavior, the mechanism is unsupported. If the slow-absorbing index's subsequent trajectory is statistically identical to the fast-absorbing index's trajectory, the mechanism is falsified.

**Main governance risk:** Definition drift in "external-looking shock" and "absorption characteristic." The shock must be structurally defined (e.g., a move exceeding N standard deviations across multiple indices simultaneously), not identified retrospectively.

---

## 7. DISTINCTNESS AUDITS

### REL-M01 vs prior work

| Prior work | Why REL-M01 is not redundant |
|------------|------------------------------|
| F-02 (pairs spread) | F-02 trades the spread between two indices. REL-M01 trades the failure of one index to confirm another's event. Different mechanism, different observable, different decision. |
| F-03 (rank rotation) | F-03 ranks indices by relative strength. REL-M01 detects confirmation failure. Ranking is continuous; confirmation failure is a discrete event. |
| CAND-105 (lead-lag) | CAND-105 tested whether Gold-lead vs Tech-lead regimes produce different downstream economics. REL-M01 tests whether confirmation failure in equity indices produces a structural state difference. Different instruments, different mechanism, different question. |
| CAND-083 (rejection pressure) | CAND-083 is single-market. REL-M01 is inherently cross-market. |
| Mean reversion | Mean reversion fades displacement toward a mean. REL-M01 detects the failure of one market to confirm another's event. Different mechanism. |

### REL-M02 vs prior work

| Prior work | Why REL-M02 is not redundant |
|------------|------------------------------|
| F-02 (pairs spread) | F-02 trades a specific pair's spread. REL-M02 measures joint synchrony across the complex. Different unit of analysis. |
| F-03 (rank rotation) | F-03 ranks by relative strength. REL-M02 measures directional agreement. Strength and synchrony are different concepts. |
| CAND-107 (vol co-movement) | CAND-107 tested vol correlation and was closed as redundant with vol regime research. REL-M02 is not about volatility correlation — it is about directional synchrony in the index complex. Different measure, different mechanism. |
| CAND-077/096/099 (vol regime) | These are single-market volatility regimes. REL-M02 is a cross-market synchrony regime. Different concept. |
| Correlation trading | Correlation trading trades the level of correlation itself. REL-M02 uses synchrony as a regime indicator, not as the traded variable. |

### REL-M03 vs prior work

| Prior work | Why REL-M03 is not redundant |
|------------|------------------------------|
| Mean reversion | Mean reversion fades displacement toward a mean. REL-M03 measures the asymmetry in how different markets absorb the same shock. Different mechanism. |
| CAND-105 (lead-lag) | CAND-105 tested timing of information flow. REL-M03 tests absorption characteristics. Timing and absorption are different concepts. |
| Volatility regime | Vol regime trades the level of volatility. REL-M03 trades the asymmetry in absorption across markets. Different concept. |
| CAND-107 (vol co-movement) | Closed as redundant. REL-M03 is not about volatility co-movement — it is about how different markets process the same shock differently. |

---

## 8. DATA FEASIBILITY

| Requirement | Available? | Notes |
|-------------|-----------|-------|
| US equity index M1 data | YES | USATECHIDXUSD, others in forward pipeline |
| Timestamp alignment | YES | M1 resolution, same trading hours |
| Multiple index series | YES | At minimum USATECHIDXUSD is available; others may need feed configuration |
| Market hours overlap | YES | All US equity indices trade the same sessions |
| Historical data for formulation | YES | Forward pipeline provides prospective data |
| No exotic data required | YES | All mechanisms computable from standard M1 OHLCV |

**Feasibility assessment:** All three mechanisms are observable from currently available data. No additional data sources are required.

---

## 9. STANDALONE BASE ASSESSMENT

| Mechanism | Can it become a Base? | Conditional dependence? | Assessment |
|-----------|----------------------|------------------------|------------|
| REL-M01 | YES | NO — the mechanism is self-contained. The confirmation failure event in Index A/B is the decision trigger. No external strategy is needed to define when the relationship is "active." | STANDALONE-CAPABLE |
| REL-M02 | YES | NO — the synchrony regime transition is the decision trigger. The mechanism is self-contained. No external strategy is needed to define when synchrony breakdown occurs. | STANDALONE-CAPABLE |
| REL-M03 | YES | NO — the shock absorption asymmetry is the decision trigger. The mechanism is self-contained. No external strategy is needed to define when a shock occurs or when absorption is asymmetric. | STANDALONE-CAPABLE |

All three mechanisms pass the standalone Base test. None requires another strategy to define when the relationship is active.

---

## 10. FALSIFICATION ROUTES

| Mechanism | Primary falsification route |
|-----------|---------------------------|
| REL-M01 | Confirmation failures are random; non-confirming index subsequent behavior is statistically identical regardless of confirmation status |
| REL-M02 | Synchrony breakdowns are random; desynchronized regime has identical subsequent economics to synchronized regime |
| REL-M03 | Absorption asymmetry is random; slow-absorbing index subsequent trajectory is statistically identical to fast-absorbing index trajectory |

---

## 11. PRIORITY CLASSIFICATION

| Mechanism | Priority | Reason |
|-----------|----------|--------|
| REL-M01 | HIGH PRIORITY FOR FORMULATION | Most mechanistically clear. Confirmation failure is a discrete, observable event with a natural decision trigger. Strong distinctness from all prior work. Low specification-risk if "structural event" and "confirmation window" are frozen at registration. |
| REL-M02 | MEDIUM PRIORITY FOR FORMULATION | Mechanistically clear but synchrony measurement introduces more degrees of freedom than REL-M01. The regime transition must be structurally defined to avoid parameter drift. |
| REL-M03 | MEDIUM PRIORITY FOR FORMULATION | Mechanistically interesting but "external-looking shock" and "absorption characteristic" are harder to define structurally without introducing parameters. Higher governance risk than REL-M01. |

---

## 12. EXPLICIT STATEMENTS

- **Economic testing performed:** NO
- **Historical economic results used:** NO
- **FB-001 economics inspected:** NO
- **F-01 economics inspected:** NO
- **Protected-forward economics inspected:** NO
- **Parameter optimization performed:** NO
- **Closed lines reopened:** NO
- **Production code changed:** NO
- **Owner selection performed:** NO
- **V38A registration performed:** NO

---

## 13. NEXT AUTHORIZED TASK

The next step is NOT formulation of these mechanisms into strategies. The next step is owner review of this discovery artifact to determine whether any mechanism warrants progression to the Outcome-Blind Base Formulation Cycle (BF1–BF13).

If the owner authorizes progression, the formulation cycle must:
- Produce a complete deterministic decision process
- Answer all eleven governance questions
- Not consult historical economic performance
- Not select parameters from data
- Not use FB-001 or F-01 economics as selection evidence

---

**END OF DISCOVERY ARTIFACT**
