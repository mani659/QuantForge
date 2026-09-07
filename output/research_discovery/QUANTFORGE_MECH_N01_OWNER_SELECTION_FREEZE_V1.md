# QUANTFORGE — MECH-N01 OWNER SELECTION FREEZE

**Date:** 2026-09-07
**Status:** OWNER SELECTION COMPLETE — MECH-N01 SELECTED FOR FORMULATION
**Milestone:** Owner authorization of MECH-N01 for progression to Outcome-Blind Base Formulation Cycle (BF1–BF13)
**Parent doctrine:** V38A (BV1–BV13), BS1–BS13 (selection clauses), BF1–BF13 (formulation clauses)

---

## 1. SELECTION SCOPE

This document records the owner's authorization of MECH-N01 (Structural Level Validation Flow) for progression to the Outcome-Blind Base Formulation Cycle under BF1–BF13. This is a SELECTION FREEZE, not a formulation. No decision process is specified. No parameters are assigned. No economics are computed. No registration is created.

**Selection authority:** Owner, per BS11.

---

## 2. AUTHORITATIVE SOURCES CONSULTED

| Source | Artifact | Role in selection |
|--------|----------|------------------|
| V38 Doctrine | `QUANTFORGE_V38_DOCTRINE_RATIFICATION_V1.md` | Hybrid Base + Conditional architecture; D1–D25 clauses |
| V38A Validation Pathway | `QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_RATIFICATION_V1.md` | BV1–BV13; six-stage lifecycle; economics as evidence not gates |
| Base Hypothesis Selection | `QUANTFORGE_BASE_HYPOTHESIS_SELECTION_VALIDATION_RATIFICATION_V1.md` | BS1–BS13; selection clauses; object-type gate; anti-rescue |
| Outcome-Blind Formulation | `QUANTFORGE_OUTCOME_BLIND_BASE_DECISION_PROCESS_FORMULATION_RATIFICATION_V1.md` | BF1–BF13; formulation clauses; outcome-blind boundary |
| V38A New Base Mechanism Discovery | `QUANTFORGE_V38A_NEW_BASE_MECHANISM_DISCOVERY_V1.md` | Discovery artifact containing MECH-N01/N02/N03 |
| SESSION_HANDOFF | `docs/SESSION_HANDOFF.md` | Current governed state; RF-001 Stage 3 blocked |

---

## 3. SELECTED MECHANISM

| Field | Value |
|-------|-------|
| Mechanism ID | MECH-N01 |
| Mechanism name | Structural Level Validation Flow |
| Unit of analysis | Single market (e.g., USATECHIDXUSD) |
| Market process | When price breaks a structurally significant level and holds for K bars, participant behavior changes: stop-hunters cover, new entrants enter, market makers adjust. The validation event creates a self-reinforcing directional impulse. |
| Observable | Bar E closes above/below breakout level; bars E+1 through E+K hold; bar E+K completes validation |
| State/event transition | "Breakout uncertain" → "Breakout validated" (discrete event at bar E+K) |
| Directional consequence | Bullish validation → LONG; Bearish validation → SHORT |
| Falsification | Validated breakouts show no directional edge vs. invalidated breakouts |

---

## 4. MECHANISM DEFINITION (FROM DISCOVERY)

**Market process:**
When price breaks above a structurally significant high (or below a structurally significant low), the breakout initially creates uncertainty. Market participants who sold the breakout (stop-hunters, short-term contrarians) are underwater. Participants who bought the breakout (momentum followers) are profitable but uncertain. If price holds above the breakout level for a sustained period, the level transitions from "just broken" to "validated as new support/resistance." This transition changes participant behavior: stop-hunters are forced to cover (creating buying pressure), new buyers enter (validating the breakout), and market makers adjust quotes upward (reflecting the changed structural state). The validation itself creates a self-reinforcing directional impulse.

**Participant interpretation:**
- Stop-hunters / short-term contrarians: Sold the breakout expecting a fake-out. When the breakout holds, they are forced to cover, creating buying pressure.
- Momentum followers: Bought the breakout but are uncertain. When the level holds, they add to positions, reinforcing the move.
- Market makers: Adjust inventory and quotes to reflect the new structural level. The level changing character forces hedging adjustments.
- Structural traders: Only enter after the level is validated, adding additional directional flow.

**Key insight:** The VALIDATION EVENT (level holds for K bars) is a distinct participant-behavior transition, not merely "momentum continued."

---

## 5. OWNER-SELECTION RATIONALE

The owner selects MECH-N01 for the following reasons, all grounded in discovery artifact evidence and BS1–BS13 compliance:

### 5.1 Object-type qualification (BS1)
MECH-N01 is a mechanism, not a complete decision process. It requires formulation under BF1–BF13 before it can become a BASE HYPOTHESIS. This selection authorizes the formulation step, not registration or validation.

### 5.2 Discovery priority ranking
MECH-N01 ranked #1 in the discovery artifact's qualitative prioritization across 10 dimensions:
- Mechanism clarity: HIGH
- Participant plausibility: HIGH
- Observable determinism: HIGH
- Prospective testability: HIGH
- Economic pathway: HIGH
- Execution realism: HIGH
- Falsifiability: HIGH
- Independence: HIGH
- Opportunity clarity: HIGH
- Threshold mining risk: MEDIUM (lowest among candidates)

### 5.3 Architectural simplicity
MECH-N01 is a single-market mechanism. It does not require cross-market data synchronization, hedging-flow detection, or multi-instrument coordination. This reduces execution complexity and data-dependency risk.

### 5.4 Deterministic observable
The K-bar hold is binary and deterministic. No statistical estimation, no regime detection, no probabilistic classification. The observable is directly comparable across forward observations.

### 5.5 Clear falsification path
The mechanism has a clean falsification test: compare validated breakouts (K-bar hold) vs. invalidated breakouts (reversal before K bars). If no directional difference exists, the mechanism is falsified. This is the clearest falsification path among the three candidates.

### 5.6 Independence from all exhausted work
MECH-N01 is materially distinct from all 21 exhausted mechanism dimensions, all RF-001/002/003, all formulated hypotheses (F-01/F-02/F-03), and all closed research lines. The distinctness assessment in the discovery artifact (§6) confirms this.

---

## 6. ALTERNATIVE MECHANISMS (NOT SELECTED)

| Mechanism | Status | Why not selected |
|-----------|--------|-----------------|
| MECH-N02 (Cross-Asset Hedging Cascade) | Discovered, deferred | Higher threshold-mining risk (S and L parameters); hedging response is less deterministic than N01 observables; may be better suited as Conditional than Base |
| MECH-N03 (Session-Sequential Trend Quality) | Discovered, deferred | Dual-direction logic is more complex than N01; path quality → participant composition → resilience link is inferential; good standalone Base candidate but N01 is architecturally simpler |

MECH-N02 and MECH-N03 remain in the research repository as discovered mechanisms. They are not rejected — they are deferred pending future owner consideration.

---

## 7. DISTINCTNESS ASSESSMENT

### 7.1 Distinctness from all exhausted dimensions
MECH-N01 survives audit against all 21 permanently exhausted mechanism dimensions (V36). The mechanism is about structural level VALIDATION, not about volatility, momentum, mean reversion, lead-lag, or any other exhausted concept. Full cross-tabulation available in discovery artifact §6.2.

### 7.2 Distinctness from RF-001/002/003
| RF mechanism | Why MECH-N01 is different |
|-------------|--------------------------|
| RF-001 (confirmation failure) | RF-01 detects when Market B fails to confirm Market A's event, then fades Market B. MECH-N01 detects when a breakout in a single market holds for K bars, then follows the validated direction. Different mechanism, different observable, different direction. |
| RF-002 (synchrony regime) | RF-02 measures joint directional synchrony across the complex. MECH-N01 is single-market. Different unit of analysis. |
| RF-003 (shock absorption) | RF-03 measures shock absorption asymmetry across markets. MECH-N01 is about level validation. Different mechanism. |

### 7.3 Distinctness from state observations
CAND-077, CAND-081, CAND-083, CAND-099 remain observations, not Base candidates. MECH-N01 is not a state observation — it is a mechanism that produces a deterministic observable (K-bar hold) and requires formulation under BF1–BF13.

### 7.4 Distinctness from closed research
MECH-N01 does not import parameters, scope, or results from any closed research line (H01, ORD, TRADEABLE_EDGE, or any DISC/CAND closure). The mechanism was discovered independently through the V38A discovery sprint.

---

## 8. NEGATIVE-KNOWLEDGE CONSTRAINTS

The following negative-knowledge constraints are binding on the future formulation of MECH-N01:

| Constraint | Source | Binding on formulation |
|-----------|--------|----------------------|
| N and K must be frozen, not optimized | Discovery §10.2 | Formulation must specify N and K as structural parameters, not as optimized values |
| Overlap with "momentum continuation" must be avoided | Discovery §10.2 | Formulation must preserve the validation-induced-flow distinctness — MECH-N01 is not momentum |
| Session dependence must be documented, not tuned | Discovery §10.1 | If the mechanism is session-dependent, this is a structural limitation, not a parameter |
| DISC-026 (ORB: non-viable) does not apply | Discovery §3 | MECH-N01 is not an opening-range breakout strategy — it is a structural level validation mechanism |
| 21 exhausted dimensions are permanently excluded | V36 strategic assessment | Formulation must not produce a decision process that实质上 revisits any exhausted dimension |

---

## 9. EXPLICIT NON-USE OF HISTORICAL PERFORMANCE

Per BF2/BF3 and BS4/BS5:

- MECH-N01 was selected based on mechanism clarity, participant plausibility, observable determinism, and architectural independence — NOT on any historical performance metric.
- No backtests were run. No returns were computed. No expectancy was calculated. No Sharpe ratio was assessed. No win rate was measured.
- The selection record contains no numeric ranking derived from historical outcomes.
- Historical knowledge was used ONLY for negative-knowledge constraints (Section 8) and distinctness verification (Section 7).

---

## 10. LIFECYCLE BOUNDARY

This selection freeze establishes the following boundary:

| What this document does | What this document does NOT do |
|------------------------|-------------------------------|
| Records owner authorization of MECH-N01 for formulation | Does not create a BASE HYPOTHESIS |
| Freezes the mechanism identity for formulation | Does not specify decision conditions, entry, exit, scope, cost model |
| Authorizes progression to BF1–BF13 formulation cycle | Does not register the hypothesis in V38A |
| Records selection rationale under BS1–BS13 | Does not validate, test, or execute anything |
| Freezes the discovery artifact as the canonical source | Does not alter RF-001, RF-002, RF-003, F-01, FB-001, or any governed state |

**SELECTED HYPOTHESIS ≠ VALIDATED BASE** (BS12). Base status exists only after V38A structural + economic validation, holistic viability adjudication, and owner-approved Registry entry.

---

## 11. AUTHORIZATION FOR NEXT STAGE

**Next governed step:** Owner-authorized Outcome-Blind Base Formulation Cycle under BF1–BF13 for MECH-N01 (Structural Level Validation Flow).

The formulation cycle must:
1. Produce a complete, deterministic decision process (BF1)
2. Be outcome-blind (BF2) with no historical-performance-driven parameters (BF3)
3. Carry the full mechanism–observable–decision traceability chain (BF4)
4. Specify complete decision semantics: participation, direction, entry, exit, risk/invalidation, execution, scope, outcome, cost model, opportunity population (BF6)
5. Be coherent with no future Conditional (BF7)
6. Carry the architectural-distinctness statement (BF8)
7. Respect negative-knowledge constraints (BF9)
8. Answer "would this be worthy of independent evaluation with no Conditional ever created?" with YES (BF10)
9. End as FORMULATED HYPOTHESIS — NOT SELECTED (BF12), subject to BS1–BS13 selection before V38A registration (BF13)

---

## 12. GOVERNANCE CHECKLIST

| Check | Result |
|-------|--------|
| BS1 — Object-type requirement | PASS — MECH-N01 is a mechanism requiring formulation, not a complete decision process |
| BS2 — Selection provenance | PASS — provenance recorded (discovery artifact, §2) |
| BS3 — Closed-line firewall | PASS — no closed artifact imported; mechanism discovered independently |
| BS4 — Historical-result separation | PASS — no historical results used as selection criteria |
| BS5 — Research-priority vs. eligibility separation | PASS — selection based on priority criteria only; no P&L ranking |
| BS6 — Prospective selection freeze | PASS — mechanism identity frozen in this document |
| BS7 — Selection data boundary | PASS — no sealed validation-window figures inspected |
| BS8 — Family redundancy control | PASS — MECH-N01 is architecturally distinct from all prior mechanisms |
| BS9 — Conditional independence | PASS — MECH-N01 is self-contained; no future Conditional required |
| BS10 — Parallel-candidate protection | PASS — MECH-N01 selected; MECH-N02/N03 deferred (not run as validation tournament) |
| BS11 — Owner selection authority | PASS — owner authorization recorded in this document |
| BS12 — Base-hypothesis / Base separation | PASS — labeled BASE HYPOTHESIS, never Base |
| BS13 — Anti-rescue selection protection | PASS — no rescue framing; MECH-N01 selected on mechanism merit alone |
| BF1 — Decision-process object requirement | PENDING — formulation under BF1–BF13 not yet performed |
| BF2 — Outcome-blind formulation | PENDING — formulation under BF1–BF13 not yet performed |
| BF3 — Historical-performance firewall | PENDING — formulation under BF1–BF13 not yet performed |
| No economic testing | PASS — no backtests, no returns, no expectancy, no Sharpe, no win rate |
| No parameter optimization | PASS — N and K identified conceptually, not from data |
| No threshold mining | PASS — no numerical thresholds selected from historical performance |
| No registration | PASS — no V38A registration created |
| No production-code change | PASS |
| No runner interruption | PASS |
| No broker orders | PASS |
| No governance reinterpretation | PASS |

---

## 13. FINAL VERDICT

**MECH-N01 (Structural Level Validation Flow) SELECTED by owner for progression to Outcome-Blind Base Formulation Cycle (BF1–BF13).**

Selection frozen. Mechanism identity locked. Formulation authorized. No formulation performed. No registration created. No validation executed. Base Registry remains EMPTY.

---

**Selection record SHA256:** `1bab8a0c37d03c85552f39a68886f136835fbf19a85026f8a2e06143ab68262e`

**Owner authorization:** Documented in this artifact per BS11.

**Next governed step:** Outcome-Blind Base Formulation Cycle for MECH-N01 under BF1–BF13.

---

**END OF MECH-N01 OWNER SELECTION FREEZE**
