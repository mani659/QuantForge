# QUANTFORGE — RELATIONAL OWNER DECISION PACKET
# GOVERNANCE DECISION PACKET FOR RF-001, RF-002, RF-003

**Date:** 2026-09-07
**Status:** OWNER DECISION PACKET COMPLETE — OWNER SELECTION PENDING
**Purpose:** Make governance-selectable parameters transparent and governable

---

## 1. GOVERNING SOURCES

- `QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md` (formulation specifications)
- `QUANTFORGE_RELATIONAL_PARAMETER_ADJUDICATION_V1.md` (parameter classification)
- `QUANTFORGE_RELATIONAL_MECHANISM_DISCOVERY_V1.md` (discovery artifact)
- Outcome-Blind Base Formulation Pathway (BF1–BF13)
- Base Hypothesis Selection Framework (BS1–BS13)
- V38A Base Validation Pathway (BV1–BV13)
- SESSION_HANDOFF §55, §56

---

## 2. FORMULATION SUMMARIES

### RF-001: Cross-Market Confirmation Failure Process

- **Source mechanism:** REL-M01
- **Behavioral hypothesis:** When a structurally significant price event occurs in one US equity index, correlated indices typically confirm the move. When confirmation explicitly fails, the failure represents a distinct market-state transition.
- **Markets:** USATECHIDXUSD (primary) + one confirmation index
- **Observable:** Primary market N-bar breakout; confirmation market observed for M bars
- **Event:** Confirmation failure — M bars elapse without confirmation
- **Decision:** Fade the non-confirming index's relative direction
- **Execution:** Entry at open of bar M+2; exit at session close
- **Opportunity population:** One per structural event; one position at a time
- **Scope:** US regular session, M1 bars, forward-only
- **Cost model:** 2 bps round-trip
- **Standalone:** YES — confirmation failure is self-triggering
- **Distinctness:** Not F-02, F-03, mean reversion, TSMOM, CAND-083, CAND-105
- **Falsification:** Non-confirming market performance is statistically identical regardless of confirmation status

### RF-002: Cross-Market Synchrony Regime Process

- **Source mechanism:** REL-M02
- **Behavioral hypothesis:** US equity indices normally move with high synchrony. When synchrony breaks down, the desynchronized state is a distinct market regime.
- **Markets:** USATECHIDXUSD + additional US equity index(es)
- **Observable:** Directional agreement fraction over W-bar window; regime transition when below T
- **Event:** Synchrony regime transition — measure falls below T
- **Decision:** Fade the divergent index's most recent direction
- **Execution:** Entry at open of next bar; exit at session close
- **Opportunity population:** One per regime transition; oscillation control within W bars
- **Scope:** US regular session, M1 bars, forward-only
- **Cost model:** 2 bps round-trip
- **Standalone:** YES — synchrony transition is self-triggering
- **Distinctness:** Not F-02, F-03, CAND-107, vol regime
- **Falsification:** Divergent index performance is statistically identical regardless of synchrony regime

### RF-003: Cross-Market Shock Absorption Asymmetry Process

- **Source mechanism:** REL-M03
- **Behavioral hypothesis:** When an external shock affects multiple indices, they absorb it differently. Asymmetry in absorption reflects structural differences in participant composition.
- **Markets:** USATECHIDXUSD + additional US equity index(es)
- **Observable:** Complex-wide return exceeds S (shock); absorption measured over K bars; asymmetry exceeds A
- **Event:** Shock absorption asymmetry event — K bars after shock, asymmetry > A
- **Decision:** Fade the slow-absorbing index's post-shock direction
- **Execution:** Entry at open of bar K+1; exit at session close
- **Opportunity population:** One per shock; minimum K-bar separation
- **Scope:** US regular session, M1 bars, forward-only
- **Cost model:** 2 bps round-trip
- **Standalone:** YES — shock detection and absorption measurement are self-contained
- **Distinctness:** Not mean reversion, CAND-105, vol regime, CAND-107
- **Falsification:** Slow-absorbing index performance is statistically identical to fast-absorbing index

---

## 3. GOVERNANCE-SELECTABLE CHOICES

| ID | Formulation | Governance choice | Why it matters | What changes if chosen differently |
|----|-------------|------------------|----------------|-----------------------------------|
| G1 | RF-001 | N — lookback horizon for structural event | Defines what constitutes a "structurally significant" breakout | Smaller N = more frequent, smaller events; larger N = fewer, larger events |
| G2 | RF-001 | M — confirmation window length | Defines how long to wait for confirmation before declaring failure | Shorter M = more failures detected; longer M = fewer failures, more confirmations |
| G3 | RF-001 | Confirmation market identity | Which second index serves as the confirmation reference | Different indices have different correlation structures with USATECHIDXUSD |
| G4 | RF-002 | W — synchrony observation window | Defines the horizon over which directional agreement is measured | Shorter W = noisier measure; longer W = smoother but slower regime detection |
| G5 | RF-002 | T — synchrony threshold | Defines the boundary between synchronized and desynchronized | Higher T = more transitions; lower T = fewer, more extreme transitions |
| G6 | RF-002 | Index complex composition | Which indices participate in the synchrony measure | Different compositions produce different synchrony dynamics |
| G7 | RF-003 | S — shock threshold (bps) | Defines what constitutes an "external-looking" shock | Lower S = more shocks; higher S = fewer, larger shocks |
| G8 | RF-003 | K — absorption measurement window | Defines how long to measure absorption after a shock | Shorter K = captures fast absorption; longer K captures slow absorption |
| G9 | RF-003 | A — asymmetry threshold | Defines when absorption asymmetry is "significant" | Lower A = more asymmetry events; higher A = fewer, more extreme events |

---

## 4. CHOICE CLASSIFICATION

| ID | Classification | Description |
|----|---------------|-------------|
| G1 | B. TEMPORAL STRUCTURE | Defines the observation horizon for detecting the structural event |
| G2 | B. TEMPORAL STRUCTURE | Defines the response horizon for confirmation assessment |
| G3 | A. STRUCTURAL SCOPE | Defines which markets participate in the relationship |
| G4 | B. TEMPORAL STRUCTURE | Defines the observation horizon for synchrony measurement |
| G5 | C. EVENT DEFINITION | Defines the regime boundary for synchrony transitions |
| G6 | A. STRUCTURAL SCOPE | Defines which markets participate in the relationship |
| G7 | C. EVENT DEFINITION | Defines what constitutes a shock event |
| G8 | B. TEMPORAL STRUCTURE | Defines the absorption measurement horizon |
| G9 | C. EVENT DEFINITION | Defines the asymmetry threshold for event detection |

---

## 5. OUTCOME-BLIND OPTIONS

### G1: N (RF-001 lookback horizon)

The mechanism requires a finite lookback to define "structurally significant breakout." The following alternatives are implied by the mechanism:

**Option 1: Short horizon (e.g., 15–30 M1 bars)**
- Exact rule: Close exceeds highest high (or lowest low) of prior 15–30 completed M1 bars
- Mechanism interpretation: "Structurally significant" means a breakout relative to recent price action (15–30 minutes)
- Determinism: Fully deterministic
- Temporal implications: Events are frequent; confirmation window is the binding constraint
- Data requirements: Standard M1 data
- Principal tradeoff: More events, more noise, more opportunities to test the mechanism
- Distinctness implications: Remains distinct — breakout detection is not the mechanism; confirmation failure is

**Option 2: Medium horizon (e.g., 30–60 M1 bars)**
- Exact rule: Close exceeds highest high (or lowest low) of prior 30–60 completed M1 bars
- Mechanism interpretation: "Structurally significant" means a breakout relative to the prior 30–60 minutes
- Determinism: Fully deterministic
- Temporal implications: Events are moderately frequent
- Data requirements: Standard M1 data
- Principal tradeoff: Balanced event frequency
- Distinctness implications: Remains distinct

**Option 3: Long horizon (e.g., 60–120 M1 bars)**
- Exact rule: Close exceeds highest high (or lowest low) of prior 60–120 completed M1 bars
- Mechanism interpretation: "Structurally significant" means a breakout relative to the prior 1–2 hours
- Determinism: Fully deterministic
- Temporal implications: Events are infrequent; each event is more significant
- Data requirements: Standard M1 data
- Principal tradeoff: Fewer events, each more significant, but fewer opportunities to validate
- Distinctness implications: Remains distinct — but approaches the character of longer-term breakout; must ensure M is chosen to preserve the confirmation-failure mechanism

**Mechanism preservation:** ALL OPTIONS PRESERVED. N defines the event population, not the mechanism. The mechanism (confirmation failure) is identical across all options.

**Distinctness:** ALL OPTIONS DISTINCT from F-02, F-03, mean reversion, TSMOM, CAND-083, breakout/ORB.

---

### G2: M (RF-001 confirmation window)

The mechanism requires a bounded window for confirmation assessment.

**Option 1: Short window (e.g., 5–15 M1 bars)**
- Exact rule: Confirm within 5–15 bars of the primary event
- Mechanism interpretation: Confirmation must occur quickly; failure is detected early
- Determinism: Fully deterministic
- Temporal implications: Decision is made early in the session; position has more time to run
- Data requirements: Standard M1 data
- Principal tradeoff: More failures detected (shorter window = less time to confirm); but may miss slow confirmations
- Distinctness implications: Remains distinct — short window makes the mechanism more event-driven

**Option 2: Medium window (e.g., 15–30 M1 bars)**
- Exact rule: Confirm within 15–30 bars of the primary event
- Mechanism interpretation: Confirmation has a moderate window
- Determinism: Fully deterministic
- Temporal implications: Decision is made mid-session
- Data requirements: Standard M1 data
- Principal tradeoff: Balanced detection
- Distinctness implications: Remains distinct

**Option 3: Long window (e.g., 30–60 M1 bars)**
- Exact rule: Confirm within 30–60 bars of the primary event
- Mechanism interpretation: Confirmation has a generous window; only clear failures are detected
- Determinism: Fully deterministic
- Temporal implications: Decision is made late in the session; less position time remaining
- Data requirements: Standard M1 data
- Principal tradeoff: Fewer failures detected (longer window = more time to confirm); each failure is more significant
- Distinctness implications: Remains distinct — but long window may reduce the event-driven character

**Mechanism preservation:** ALL OPTIONS PRESERVED. M defines the confirmation-failure population, not the mechanism.

**Distinctness:** ALL OPTIONS DISTINCT.

---

### G3: Confirmation market identity (RF-001)

The mechanism requires a second index.

**Option 1: US500 (S&P 500 proxy)**
- Exact rule: US500 is the confirmation market for USATECHIDXUSD events
- Mechanism interpretation: Confirmation reflects whether the broader market confirms tech-specific moves
- Determinism: Fully deterministic
- Temporal implications: None — same session, same timestamps
- Data requirements: US500 M1 data (available in forward pipeline)
- Principal tradeoff: US500 is the broadest US equity proxy; high correlation with USATECHIDXUSD; confirmation failures are likely rare but significant
- Distinctness implications: Remains distinct — pair identity does not change the mechanism

**Option 2: US30 (Dow Jones proxy)**
- Exact rule: US30 is the confirmation market
- Mechanism interpretation: Confirmation reflects whether blue-chip stocks confirm tech moves
- Determinism: Fully deterministic
- Temporal implications: None
- Data requirements: US30 M1 data
- Principal tradeoff: US30 has different sector composition than USATECHIDXUSD; may produce different confirmation-failure dynamics
- Distinctness implications: Remains distinct

**Option 3: Other US equity index**
- Exact rule: A different US equity index is the confirmation market
- Mechanism interpretation: Depends on the specific index chosen
- Determinism: Fully deterministic
- Temporal implications: None
- Data requirements: M1 data for the chosen index
- Principal tradeoff: Different indices have different correlation structures
- Distinctness implications: Remains distinct

**Mechanism preservation:** ALL OPTIONS PRESERVED. Confirmation market identity defines the pair, not the mechanism.

**Distinctness:** ALL OPTIONS DISTINCT.

---

### G4: W (RF-002 synchrony window)

The mechanism requires an observation window for directional agreement.

**Option 1: Short window (e.g., 10–20 M1 bars)**
- Exact rule: Compute directional agreement over the most recent 10–20 completed M1 bars
- Mechanism interpretation: Synchrony is measured over a short horizon; regime transitions are frequent
- Determinism: Fully deterministic
- Temporal implications: Regime transitions detected quickly
- Data requirements: Standard M1 data
- Principal tradeoff: Noisy measure; frequent transitions; more opportunities but more false signals
- Distinctness implications: Remains distinct — short window makes regime detection responsive

**Option 2: Medium window (e.g., 20–40 M1 bars)**
- Exact rule: Compute directional agreement over 20–40 completed M1 bars
- Mechanism interpretation: Synchrony measured over moderate horizon
- Determinism: Fully deterministic
- Temporal implications: Balanced detection speed
- Data requirements: Standard M1 data
- Principal tradeoff: Balanced noise/frequency
- Distinctness implications: Remains distinct

**Option 3: Long window (e.g., 40–80 M1 bars)**
- Exact rule: Compute directional agreement over 40–80 completed M1 bars
- Mechanism interpretation: Synchrony measured over long horizon; regime transitions are rare but significant
- Determinism: Fully deterministic
- Temporal implications: Slow detection; fewer transitions
- Data requirements: Standard M1 data
- Principal tradeoff: Smooth measure; rare transitions; each transition more significant
- Distinctness implications: Remains distinct — but long window may approach session-level aggregation

**Mechanism preservation:** ALL OPTIONS PRESERVED. W defines the synchrony-measurement population, not the mechanism.

**Distinctness:** ALL OPTIONS DISTINCT.

---

### G5: T (RF-002 synchrony threshold)

The mechanism requires a regime boundary.

**Option 1: Strict threshold (e.g., T = 0.70–0.80)**
- Exact rule: Synchronized when >70–80% of bars show directional agreement
- Mechanism interpretation: Only highly synchronous periods are "synchronized"; most periods are desynchronized
- Determinism: Fully deterministic
- Temporal implications: Fewer transitions (most of the time the measure is below T)
- Data requirements: None beyond M1 data
- Principal tradeoff: Fewer regime transitions; each transition is more extreme
- Distinctness implications: Remains distinct

**Option 2: Moderate threshold (e.g., T = 0.55–0.65)**
- Exact rule: Synchronized when >55–65% of bars show directional agreement
- Mechanism interpretation: Moderate synchrony is the baseline; breakdowns are detectable
- Determinism: Fully deterministic
- Temporal implications: Moderate transition frequency
- Data requirements: None beyond M1 data
- Principal tradeoff: Balanced transition frequency
- Distinctness implications: Remains distinct

**Option 3: Lenient threshold (e.g., T = 0.45–0.55)**
- Exact rule: Synchronized when >45–55% of bars show directional agreement
- Mechanism interpretation: Even modest agreement is "synchronized"; only clear disagreements are desynchronized
- Determinism: Fully deterministic
- Temporal implications: Many transitions (frequent regime changes)
- Data requirements: None beyond M1 data
- Principal tradeoff: Many transitions; each may be less significant
- Distinctness implications: Remains distinct — but very low T may produce too many transitions

**Mechanism preservation:** ALL OPTIONS PRESERVED. T defines the regime-transition population, not the mechanism.

**Distinctness:** ALL OPTIONS DISTINCT.

---

### G6: Index complex composition (RF-002)

The mechanism requires multiple indices.

**Option 1: Two-index complex (USATECHIDXUSD + US500)**
- Exact rule: Synchrony measured across USATECHIDXUSD and US500
- Mechanism interpretation: Synchrony between tech and broad market
- Determinism: Fully deterministic
- Temporal implications: None
- Data requirements: USATECHIDXUSD + US500 M1 data
- Principal tradeoff: Simplest complex; clear directional agreement; but limited to one relationship
- Distinctness implications: Remains distinct

**Option 2: Three-index complex (USATECHIDXUSD + US500 + US30)**
- Exact rule: Synchrony measured across three indices
- Mechanism interpretation: Synchrony across the US equity complex
- Determinism: Fully deterministic
- Temporal implications: None
- Data requirements: Three M1 data series
- Principal tradeoff: Richer synchrony signal; but "majority" direction may be ambiguous with three indices
- Distinctness implications: Remains distinct — but must define majority clearly (≥2 of 3)

**Mechanism preservation:** BOTH OPTIONS PRESERVED. Complex composition defines the participating markets, not the mechanism.

**Distinctness:** BOTH OPTIONS DISTINCT.

---

### G7: S (RF-003 shock threshold)

The mechanism requires a shock definition.

**Option 1: Moderate shock (e.g., S = 10–20 bps per bar)**
- Exact rule: Shock when complex-wide absolute return exceeds 10–20 bps in a single M1 bar
- Mechanism interpretation: Moderate-sized moves affecting the complex simultaneously
- Determinism: Fully deterministic
- Temporal implications: Moderate shock frequency
- Data requirements: Standard M1 data
- Principal tradeoff: Frequent shocks; each may be less extreme
- Distinctness implications: Remains distinct

**Option 2: Large shock (e.g., S = 20–40 bps per bar)**
- Exact rule: Shock when complex-wide absolute return exceeds 20–40 bps
- Mechanism interpretation: Large moves affecting the complex simultaneously
- Determinism: Fully deterministic
- Temporal implications: Infrequent shocks
- Data requirements: Standard M1 data
- Principal tradeoff: Rare shocks; each is more significant; fewer opportunities
- Distinctness implications: Remains distinct

**Option 3: Extreme shock (e.g., S = 40+ bps per bar)**
- Exact rule: Shock when complex-wide absolute return exceeds 40 bps
- Mechanism Interpretation: Only extreme moves qualify as shocks
- Determinism: Fully deterministic
- Temporal implications: Very rare shocks
- Data requirements: Standard M1 data
- Principal tradeoff: Very few opportunities; each is highly significant
- Distinctness implications: Remains distinct — but may produce too few events

**Mechanism preservation:** ALL OPTIONS PRESERVED. S defines the shock-event population, not the mechanism.

**Distinctness:** ALL OPTIONS DISTINCT.

---

### G8: K (RF-003 absorption window)

The mechanism requires an absorption measurement period.

**Option 1: Short window (e.g., K = 5–10 M1 bars)**
- Exact rule: Measure absorption over 5–10 bars after the shock
- Mechanism interpretation: Absorption is assessed quickly; captures immediate post-shock behavior
- Determinism: Fully deterministic
- Temporal implications: Decision is made quickly after the shock
- Data requirements: Standard M1 data
- Principal tradeoff: Captures fast absorption; may miss slow absorption
- Distinctness implications: Remains distinct

**Option 2: Medium window (e.g., K = 10–20 M1 bars)**
- Exact rule: Measure absorption over 10–20 bars after the shock
- Mechanism interpretation: Absorption assessed over moderate horizon
- Determinism: Fully deterministic
- Temporal implications: Decision is made mid-aftermath
- Data requirements: Standard M1 data
- Principal tradeoff: Balanced capture of absorption characteristics
- Distinctness implications: Remains distinct

**Option 3: Long window (e.g., K = 20–40 M1 bars)**
- Exact rule: Measure absorption over 20–40 bars after the shock
- Mechanism interpretation: Absorption assessed over long horizon; captures slow absorption
- Determinism: Fully deterministic
- Temporal implications: Decision is made late after the shock; less session time remaining
- Data requirements: Standard M1 data
- Principal tradeoff: Captures slow absorption; but late decision reduces position time
- Distinctness implications: Remains distinct

**Mechanism preservation:** ALL OPTIONS PRESERVED. K defines the absorption-measurement population, not the mechanism.

**Distinctness:** ALL OPTIONS DISTINCT.

---

### G9: A (RF-003 asymmetry threshold)

The mechanism requires an asymmetry threshold.

**Option 1: Low threshold (e.g., A = 5–10 bps cumulative)**
- Exact rule: Asymmetry event when slow-absorbing index exceeds fast-absorbing by 5–10 bps cumulative over K bars
- Mechanism interpretation: Even modest asymmetry qualifies
- Determinism: Fully deterministic
- Temporal implications: More asymmetry events
- Data requirements: Standard M1 data
- Principal tradeoff: Many events; each may be less extreme
- Distinctness implications: Remains distinct

**Option 2: Moderate threshold (e.g., A = 10–20 bps cumulative)**
- Exact rule: Asymmetry event when difference exceeds 10–20 bps
- Mechanism interpretation: Moderate asymmetry is significant
- Determinism: Fully deterministic
- Temporal implications: Moderate event frequency
- Data requirements: Standard M1 data
- Principal tradeoff: Balanced event frequency
- Distinctness implications: Remains distinct

**Option 3: High threshold (e.g., A = 20+ bps cumulative)**
- Exact rule: Asymmetry event when difference exceeds 20 bps
- Mechanism interpretation: Only extreme asymmetry qualifies
- Determinism: Fully deterministic
- Temporal implications: Rare events
- Data requirements: Standard M1 data
- Principal tradeoff: Few events; each is highly significant
- Distinctness implications: Remains distinct

**Mechanism preservation:** ALL OPTIONS PRESERVED. A defines the asymmetry-event population, not the mechanism.

**Distinctness:** ALL OPTIONS DISTINCT.

---

## 6. MECHANISM-PRESERVATION AUDIT

| Choice | All options preserve mechanism? | Any option changes the discovered mechanism? |
|--------|-------------------------------|---------------------------------------------|
| G1 (N) | YES | NO — N defines event population, not confirmation-failure mechanism |
| G2 (M) | YES | NO — M defines confirmation window, not the failure mechanism |
| G3 (confirmation market) | YES | NO — market identity defines the pair, not the failure mechanism |
| G4 (W) | YES | NO — W defines synchrony measurement, not the regime-transition mechanism |
| G5 (T) | YES | NO — T defines regime boundary, not the transition mechanism |
| G6 (index complex) | YES | NO — complex defines participating markets, not the synchrony mechanism |
| G7 (S) | YES | NO — S defines shock population, not the absorption mechanism |
| G8 (K) | YES | NO — K defines absorption measurement, not the asymmetry mechanism |
| G9 (A) | YES | NO — A defines asymmetry threshold, not the absorption-asymmetry mechanism |

**No option for any governance choice changes the discovered mechanism.**

---

## 7. DISTINCTNESS AUDIT

| Choice | All options distinct from F-02? | From F-03? | From mean reversion? | From TSMOM? | From CAND-083? | From breakout/ORB? |
|--------|--------------------------------|------------|---------------------|-------------|---------------|-------------------|
| G1 | YES | YES | YES | YES | YES | YES |
| G2 | YES | YES | YES | YES | YES | YES |
| G3 | YES | YES | YES | YES | YES | YES |
| G4 | YES | YES | YES | YES | YES | YES |
| G5 | YES | YES | YES | YES | YES | YES |
| G6 | YES | YES | YES | YES | YES | YES |
| G7 | YES | YES | YES | YES | YES | YES |
| G8 | YES | YES | YES | YES | YES | YES |
| G9 | YES | YES | YES | YES | YES | YES |

**All options for all governance choices remain structurally distinct from all prior closed work.**

---

## 8. PARAMETER COUPLING ANALYSIS

### Coupled pairs

| Pair | Coupling type | Dependency |
|------|--------------|------------|
| G1 (N) + G2 (M) | TEMPORAL COUPLING | N defines the event; M defines the confirmation window. If N is very large (infrequent events), M must be large enough to allow a response. If N is very small (frequent events), M can be shorter. However, they are not strictly dependent — any N can pair with any M. The coupling is weak. |
| G4 (W) + G5 (T) | MEASUREMENT COUPLING | W defines the window; T defines the threshold. A short W with a high T may produce very few transitions. A long W with a low T may produce many. They are not strictly dependent but interact. The coupling is moderate. |
| G7 (S) + G8 (K) + G9 (A) | ABSORPTION COUPLING | S defines the shock; K defines the measurement; A defines the threshold. A large S with a short K may not capture enough absorption. A small S with a long K may produce too many events. They interact as a system. The coupling is moderate. |
| G3 + G6 | INDEPENDENT | Confirmation market (G3) and index complex (G6) are independent choices for different formulations. |

### Conclusion

The nine nominal parameters represent approximately **6 independent governance decisions**:

1. **RF-001 structural scope:** Confirmation market (G3)
2. **RF-001 temporal structure:** N and M (G1+G2, weakly coupled)
3. **RF-002 structural scope:** Index complex (G6)
4. **RF-002 temporal/threshold structure:** W and T (G4+G5, moderately coupled)
5. **RF-003 structural scope:** Index complex (G6, shared with RF-002)
6. **RF-003 event/threshold structure:** S, K, and A (G7+G8+G9, moderately coupled)

---

## 9. DECISION ORDER

The recommended decision order prevents downstream choices from implicitly influencing upstream formulation selection:

```
STEP 1: FORMULATION SELECTION
  Owner selects which formulation(s) to pursue
        ↓
STEP 2: STRUCTURAL SCOPE (if formulation selected)
  Owner selects instrument/complex identity
        ↓
STEP 3: TEMPORAL / EVENT DEFINITION
  Owner selects observation horizons and thresholds
        ↓
STEP 4: REGISTRATION
  V38A registration with all parameters frozen
```

**Important:** Step 1 (formulation selection) must precede all parameter choices. Parameters should not be explored across all three formulations simultaneously — that would constitute implicit parameter-mining across formulations.

---

## 10. OWNER DECISION MATRIX

| Formulation | Core mechanism | Distinctness | Deterministic potential | Governance choices | Empirical tuning required | Registration potential |
|-------------|---------------|-------------|------------------------|-------------------:|--------------------------|----------------------|
| RF-001 | Confirmation failure | DISTINCT | FULLY DETERMINISTIC | 3 (N, M, market) | NONE | READY AFTER GOVERNANCE CHOICES |
| RF-002 | Synchrony regime | DISTINCT | FULLY DETERMINISTIC | 3 (W, T, complex) | NONE | READY AFTER GOVERNANCE CHOICES |
| RF-003 | Shock absorption | DISTINCT | FULLY DETERMINISTIC | 4 (S, K, A, complex) | NONE | READY AFTER GOVERNANCE CHOICES |

All three formulations are fully deterministic once governance choices are made. No empirical tuning is required.

---

## 11. GOVERNANCE-RISK ASSESSMENT

### RF-001

| Risk | Level | Mitigation |
|------|-------|-----------|
| Specification drift | MODERATE — N and M could be reinterpreted | Freeze N and M at registration; no post-registration modification |
| Parameter mining | LOW — only 3 parameters; distinct mechanism | V38A registration freeze prevents post-hoc tuning |
| Data dependence | LOW — standard M1 data for two indices | Forward-only data; no historical dependency |
| Redundancy | LOW — confirmation failure is distinct from all prior work | Distinctness audit documented |
| Execution ambiguity | LOW — entry/exit timing is mechanism-derived | Temporal causality preserved |

### RF-002

| Risk | Level | Mitigation |
|------|-------|-----------|
| Specification drift | MODERATE — W and T could be reinterpreted | Freeze W and T at registration |
| Parameter mining | LOW — only 3 parameters; distinct mechanism | V38A registration freeze |
| Data dependence | LOW — standard M1 data for multiple indices | Forward-only |
| Redundancy | LOW — synchrony regime is distinct from vol regime, pairs, ranking | Distinctness audit documented |
| Execution ambiguity | LOW — entry/exit timing is mechanism-derived | Temporal causality preserved |

### RF-003

| Risk | Level | Mitigation |
|------|-------|-----------|
| Specification drift | MODERATE — S, K, A could be reinterpreted | Freeze all three at registration |
| Parameter mining | LOW — but 3 threshold parameters; interaction risk | V38A registration freeze; coupled parameters treated as a system |
| Data dependence | LOW — standard M1 data | Forward-only |
| Redundancy | LOW — shock absorption asymmetry is distinct from all prior work | Distinctness audit documented |
| Execution ambiguity | LOW — entry/exit timing is mechanism-derived | Temporal causality preserved |

---

## 12. OWNER-SELECTION BOUNDARY

This artifact does NOT:

- Select a winning formulation
- Choose parameter values
- Perform economic testing
- Inspect historical performance
- Register a V38A Base
- Introduce a Conditional
- Generate new formulations

The purpose is to present the owner with:

1. Three mechanism-complete, distinct formulations
2. Nine governance-selectable parameters (approximately 6 independent decisions)
3. Outcome-blind alternatives for each parameter
4. Mechanism-preservation confirmation for all options
5. Distinctness confirmation for all options
6. Parameter-coupling analysis
7. Recommended decision order
8. Governance-risk assessment

The owner must make the prospective governance decisions separately.

---

## 13. EXPLICIT NO-ECONOMIC-TESTING STATEMENT

**No economic testing was performed in this decision packet.**

- No backtesting
- No historical return calculation
- No P&L computation
- No expectancy calculation
- No win rate calculation
- No FB-001 economics inspected
- No F-01 economics inspected
- No protected-forward economics inspected
- No parameter optimization
- No favorable-period selection
- No favorable-instrument selection

The owner must be able to evaluate these formulations without being shown performance results.

---

**END OF DECISION PACKET**
