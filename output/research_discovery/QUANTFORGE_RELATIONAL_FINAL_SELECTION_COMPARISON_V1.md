# QUANTFORGE — RELATIONAL FINAL SELECTION COMPARISON
# CONCISE OWNER-SELECTION COMPARISON

**Date:** 2026-09-07
**Status:** FORMULATIONS READY FOR OWNER SELECTION
**Purpose:** Decision-support artifact for owner selection

---

## 1. COMPARISON MATRIX

| Dimension | RF-001 | RF-002 | RF-003 |
|-----------|--------|--------|--------|
| Source mechanism | REL-M01 | REL-M02 | REL-M03 |
| Behavioral hypothesis | Confirmation failure in correlated indices | Synchrony regime breakdown | Asymmetric shock absorption across indices |
| Markets involved | USATECHIDXUSD + one confirmation index | USATECHIDXUSD + index complex | USATECHIDXUSD + index complex |
| Relational observable | N-bar breakout in primary; no confirmation in secondary within M bars | Directional agreement fraction below T over W-bar window | Complex return exceeds S; absorption asymmetry exceeds A over K bars |
| Event/state transition | Confirmation failure — M bars elapse without confirmation | Synchrony regime transition — measure crosses below T | Shock absorption asymmetry — K bars after shock, asymmetry > A |
| Decision | Fade non-confirming index's relative direction | Fade divergent index's most recent direction | Fade slow-absorbing index's post-shock direction |
| Entry structure | Open of bar M+2 after primary event | Open of next bar after regime transition | Open of bar K+1 after shock |
| Exit/invalidation | Session close; cancelled if primary reverses before entry | Session close; cancelled if synchrony returns above T | Session close; cancelled if asymmetry falls below A |
| Opportunity population | One per structural event; one position at a time; last M bars excluded | One per regime transition; oscillation control within W bars; synchronized→desynchronized only | One per shock; K-bar separation; last K bars excluded |
| Standalone Base potential | YES — self-triggering | YES — self-triggering | YES — self-triggering |
| Distinctness from F-02/F-03 | DISTINCT — failure detection, not spread trading or ranking | DISTINCT — synchrony regime, not pair spread or strength ranking | DISTINCT — absorption asymmetry, not spread or ranking |
| Distinctness from TSMOM | DISTINCT — cross-market event, not own-history trend | DISTINCT — cross-market synchrony, not own-trend | DISTINCT — cross-market absorption, not own-trend |
| Distinctness from breakout/ORB | DISTINCT — failure detection is the trigger, not the breakout itself | DISTINCT — regime transition is the trigger, not a breakout | DISTINCT — shock absorption is the trigger, not a breakout |
| Main falsification route | Non-confirming index performance identical regardless of confirmation status | Divergent index performance identical regardless of synchrony regime | Slow-absorbing index performance identical to fast-absorbing index |
| Main specification risk | N and M must be frozen; temptation to tune | W and T must be frozen; temptation to tune | S, K, A must be frozen; temptation to tune |
| Main data risk | Requires two aligned M1 series | Requires multiple aligned M1 series | Requires multiple aligned M1 series |
| Main execution risk | Late-session events excluded; position time varies with M | Position time varies with regime transition timing | Position time varies with shock timing and K |

---

## 2. GOVERNANCE DECISIONS (COUPLED)

### Original 9 parameters → ~6 independent decisions

| Original parameter | Coupling | Independent decision |
|-------------------|----------|---------------------|
| G1: N (RF-001 lookback) | Coupled with G2 | **Decision 1: RF-001 temporal structure (N + M)** |
| G2: M (RF-001 confirmation window) | Coupled with G1 | (included above) |
| G3: Confirmation market | Independent | **Decision 2: RF-001 structural scope (confirmation index)** |
| G4: W (RF-002 window) | Coupled with G5 | **Decision 3: RF-002 temporal/threshold structure (W + T)** |
| G5: T (RF-002 threshold) | Coupled with G4 | (included above) |
| G6: Index complex (RF-002) | Independent | **Decision 4: RF-002 structural scope (index complex)** |
| G7: S (RF-003 shock) | Coupled with G8, G9 | **Decision 5: RF-003 event/threshold structure (S + K + A)** |
| G8: K (RF-003 absorption) | Coupled with G7, G9 | (included above) |
| G9: A (RF-003 asymmetry) | Coupled with G7, G8 | (included above) |
| G6: Index complex (RF-003) | Independent | **Decision 6: RF-003 structural scope (index complex)** |

### Decision-by-formulation matrix

| Decision | RF-001 | RF-002 | RF-003 |
|----------|--------|--------|--------|
| 1: Temporal structure | N + M (lookback + confirmation window) | — | — |
| 2: Structural scope | Confirmation market identity | — | — |
| 3: Temporal/threshold structure | — | W + T (window + threshold) | — |
| 4: Structural scope | — | Index complex composition | — |
| 5: Event/threshold structure | — | — | S + K + A (shock + absorption + asymmetry) |
| 6: Structural scope | — | — | Index complex composition |

---

## 3. MECHANISM-LEVEL COMPARISON

### 3.1 What is the core relational mechanism?

| Formulation | Core mechanism |
|-------------|---------------|
| RF-001 | When Index A produces a structural event and Index B fails to confirm, the failure itself is a distinct market-state signal |
| RF-002 | When the index complex transitions from synchronized to desynchronized, the divergent index is in a distinct state |
| RF-003 | When an external shock affects the complex and indices absorb it differently, the asymmetry in absorption is a distinct signal |

### 3.2 What participant behavior is hypothesized?

| Formulation | Hypothesized behavior |
|-------------|----------------------|
| RF-001 | Cross-market information propagation and hedging flows normally produce confirmation. Failure to confirm reflects structural divergence in participant positioning or information processing. (MECHANISTIC HYPOTHESIS) |
| RF-002 | Shared participants and information normally produce synchronous movement. Breakdown reflects genuine differences in flow, positioning, or information between indices. (MECHANISTIC HYPOTHESIS) |
| RF-003 | Different participant compositions and liquidity structures cause indices to process the same shock at different speeds. Asymmetry reflects structural differences in market depth and participant behavior. (MECHANISTIC HYPOTHESIS) |

### 3.3 Why is the relationship itself informative?

| Formulation | Why the relationship matters |
|-------------|----------------------------|
| RF-001 | The failure of one market to confirm another's event reveals that the two markets are in structurally different states — the relationship itself carries information about state divergence |
| RF-002 | The breakdown of normally synchronous movement reveals that the complex has entered a different regime — the relationship itself is the regime indicator |
| RF-003 | The asymmetry in how markets absorb the same shock reveals structural differences in market composition — the relationship itself carries information about relative vulnerability |

### 3.4 What would make the mechanism falsifiable?

| Formulation | Falsification route |
|-------------|-------------------|
| RF-001 | Non-confirming index's subsequent session performance is statistically identical regardless of confirmation status |
| RF-002 | Divergent index's subsequent session performance is statistically identical regardless of synchrony regime |
| RF-003 | Slow-absorbing index's subsequent session performance is statistically identical to fast-absorbing index |

### 3.5 What prevents collapse into simpler mechanisms?

| Formulation | Why not mean reversion | Why not momentum | Why not breakout | Why not correlation | Why not F-02 | Why not F-03 | Why not CAND-083 |
|-------------|----------------------|-----------------|-----------------|--------------------|-------------|-------------|--------------------|
| RF-001 | Trigger is confirmation failure, not displacement fading | Trigger is cross-market event, not own-history trend | Trigger is failure detection, not breakout trading | Trigger is discrete event, not continuous co-movement | Trigger is event failure, not spread convergence | Trigger is event detection, not relative ranking | Trigger is cross-market, not single-market |
| RF-002 | Trigger is regime transition, not displacement fading | Trigger is cross-market synchrony, not own-trend | Trigger is regime detection, not breakout trading | Trigger is regime transition, not continuous correlation | Trigger is synchrony regime, not pair spread | Trigger is directional agreement, not strength ranking | Trigger is cross-market, not single-market |
| RF-003 | Trigger is absorption asymmetry, not displacement fading | Trigger is cross-market absorption, not own-trend | Trigger is shock processing, not breakout trading | Trigger is absorption characteristics, not correlation level | Trigger is absorption asymmetry, not spread | Trigger is shock processing, not ranking | Trigger is cross-market, not single-market |

---

## 4. OWNER DECISION CRITERIA (QUALITATIVE)

| Criterion | RF-001 | RF-002 | RF-003 |
|-----------|--------|--------|--------|
| Mechanism clarity | HIGH — confirmation failure is a discrete, intuitive event | MEDIUM — synchrony regime is clear but requires defining "majority" direction | MEDIUM — shock absorption is intuitive but requires defining "shock" |
| Distinctiveness | HIGH — clearly distinct from all prior work | HIGH — clearly distinct from all prior work | HIGH — clearly distinct from all prior work |
| Deterministic specification potential | HIGH — fully deterministic once N, M, market frozen | HIGH — fully deterministic once W, T, complex frozen | HIGH — fully deterministic once S, K, A, complex frozen |
| Observability | HIGH — confirmation failure is directly observable | HIGH — synchrony is directly measurable | HIGH — shock and absorption are directly measurable |
| Data feasibility | HIGH — two M1 series needed; available | HIGH — multiple M1 series needed; available | HIGH — multiple M1 series needed; available |
| Standalone Base potential | YES — self-triggering | YES — self-triggering | YES — self-triggering |
| Specification simplicity | HIGH — 2 temporal parameters + 1 market | MEDIUM — 2 parameters (coupled) + complex | MEDIUM — 3 parameters (coupled) + complex |
| Falsifiability | HIGH — clear null hypothesis | HIGH — clear null hypothesis | HIGH — clear null hypothesis |
| Governance risk | LOW-MODERATE — N and M are coupled but independent decisions are clear | LOW-MODERATE — W and T are coupled; regime definition must be frozen | MODERATE — S, K, A are coupled as a system; more interaction risk |

---

## 5. OWNER DECISION INPUT

### Independent governance decisions (blank fields)

`Decision 1 (RF-001 temporal structure): ______`

`Decision 2 (RF-001 structural scope): ______`

`Decision 3 (RF-002 temporal/threshold structure): ______`

`Decision 4 (RF-002 structural scope): ______`

`Decision 5 (RF-003 event/threshold structure): ______`

`Decision 6 (RF-003 structural scope): ______`

### Recommended owner decision sequence

```
STEP 1: Select which formulation(s) to pursue
        ↓
STEP 2: Select structural scope (instrument/complex identity)
        ↓
STEP 3: Select temporal/event definition parameters
        ↓
STEP 4: Proceed to V38A registration with all parameters frozen
```

---

## 6. EXPLICIT NO-ECONOMIC-TESTING STATEMENT

`Economic testing performed: NO`

`Historical economic results inspected: NO`

`FB-001 economics inspected: NO`

`F-01 economics inspected: NO`

`Protected-forward economics inspected: NO`

`Optimization performed: NO`

---

**END OF COMPARISON ARTIFACT**
