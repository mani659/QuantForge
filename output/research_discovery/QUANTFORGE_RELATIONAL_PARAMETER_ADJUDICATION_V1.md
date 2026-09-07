# QUANTFORGE — RELATIONAL PARAMETER ADJUDICATION
# STRICT READ-ONLY ADJUDICATION OF UNRESOLVED STRUCTURAL PARAMETERS

**Date:** 2026-09-07
**Status:** ADJUDICATION COMPLETE — OWNER DECISION MAY BE REQUIRED
**Source artifact:** `QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md`

---

## 1. GOVERNING SOURCES

- `QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md` (source formulations)
- `QUANTFORGE_RELATIONAL_MECHANISM_DISCOVERY_V1.md` (discovery artifact)
- Outcome-Blind Base Formulation Pathway (BF1–BF13)
- Base Hypothesis Selection Framework (BS1–BS13)
- V38A Base Validation Pathway (BV1–BV13)
- SESSION_HANDOFF §55

No economic results from FB-001, F-01, protected-forward candidates, or closed relational research are used in this adjudication.

---

## 2. FORMULATION INVENTORY

| Formulation | Source mechanism | Core mechanism | Unresolved parameters |
|-------------|-----------------|----------------|----------------------|
| RF-001 | REL-M01 | Cross-market confirmation failure | N, M, confirmation market |
| RF-002 | REL-M02 | Synchrony regime transition | W, T, index complex |
| RF-003 | REL-M03 | Shock absorption asymmetry | S, K, A, index complex |

---

## 3. UNRESOLVED-PARAMETER TABLE

### RF-001

| Parameter | Why unresolved | Class | Can be objectively derived? | Governance consequence |
|-----------|---------------|-------|---------------------------|----------------------|
| N (lookback horizon) | Defines what constitutes a "structurally significant" breakout in the primary market | **B — GOVERNANCE-SELECTABLE** | No — changing N changes which events qualify; the mechanism implies a finite horizon but not a unique value | Owner must select N prospectively |
| M (confirmation window) | Defines how long to wait for confirmation before declaring failure | **B — GOVERNANCE-SELECTABLE** | No — changing M changes what counts as confirmation failure; the mechanism implies a finite window but not a unique value | Owner must select M prospectively |
| Confirmation market identity | Which second index serves as the confirmation market | **B — GOVERNANCE-SELECTABLE** | No — the mechanism requires a second index but not a specific one | Owner must select the confirmation index prospectively |
| Session boundary (09:30–16:00 ET) | US regular session hours | **A — MECHANISM-DERIVED** | Yes — defined by external market structure | No governance choice needed |
| Entry timing (open of bar M+2) | Follows from temporal causality after M-bar window | **A — MECHANISM-DERIVED** | Yes — the mechanism defines the decision point; entry must follow | No governance choice needed |
| Exit timing (close of session) | Single-session position | **A — MECHANISM-DERIVED** | Yes — the mechanism defines a single-session horizon | No governance choice needed |
| Invalidation (primary reverses before entry) | Mechanism-defined cancellation | **A — MECHANISM-DERIVED** | Yes — if the primary event reverses, the confirmation failure is void | No governance choice needed |
| Cost model (2 bps) | Standard convention | **A — MECHANISM-DERIVED** | Yes — follows from existing ratified cost convention | No governance choice needed |

### RF-002

| Parameter | Why unresolved | Class | Can be objectively derived? | Governance consequence |
|-----------|---------------|-------|---------------------------|----------------------|
| W (window length) | Defines the observation horizon for the synchrony measure | **B — GOVERNANCE-SELECTABLE** | No — changing W changes the frequency and character of regime transitions | Owner must select W prospectively |
| T (synchrony threshold) | Defines the boundary between synchronized and desynchronized regimes | **B — GOVERNANCE-SELECTABLE** | No — changing T changes what qualifies as a regime transition | Owner must select T prospectively |
| Index complex composition | Which indices participate in the synchrony measure | **B — GOVERNANCE-SELECTABLE** | No — the mechanism requires multiple indices but not specific ones | Owner must select the index complex prospectively |
| Session boundary (09:30–16:00 ET) | US regular session hours | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |
| Entry timing (open of next bar) | Temporal causality | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |
| Exit timing (close of session) | Single-session position | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |
| Invalidation (synchrony returns above T) | Mechanism-defined cancellation | **A — MECHANISM-DERIVED** | Yes — if synchrony returns above T, the regime transition was transient | No governance choice needed |
| Oscillation control (within W bars) | Prevents re-triggering within same observation window | **A — MECHANISM-DERIVED** | Yes — natural consequence of W-bar window | No governance choice needed |
| Cost model (2 bps) | Standard convention | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |

### RF-003

| Parameter | Why unresolved | Class | Can be objectively derived? | Governance consequence |
|-----------|---------------|-------|---------------------------|----------------------|
| S (shock threshold) | Defines what constitutes an "external-looking" shock | **B — GOVERNANCE-SELECTABLE** | No — changing S changes which events qualify as shocks | Owner must select S prospectively |
| K (absorption window) | Defines how long to measure absorption after a shock | **B — GOVERNANCE-SELECTABLE** | No — changing K changes what counts as "slow" vs "fast" absorption | Owner must select K prospectively |
| A (asymmetry threshold) | Defines when absorption asymmetry is "significant" | **B — GOVERNANCE-SELECTABLE** | No — changing A changes what qualifies as an asymmetry event | Owner must select A prospectively |
| Index complex composition | Which indices participate | **B — GOVERNANCE-SELECTABLE** | No | Owner must select the index complex prospectively |
| Session boundary (09:30–16:00 ET) | US regular session hours | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |
| Entry timing (open of next bar) | Temporal causality | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |
| Exit timing (close of session) | Single-session position | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |
| Invalidation (asymmetry < A before entry) | Mechanism-defined cancellation | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |
| Minimum shock separation (K bars) | Natural consequence of K-bar absorption window | **A — MECHANISM-DERIVED** | Yes — two shocks within K bars interfere with measurement | No governance choice needed |
| Cost model (2 bps) | Standard convention | **A — MECHANISM-DERIVED** | Yes | No governance choice needed |

---

## 4. CLASSIFICATION SUMMARY

| Class | Count | Parameters |
|-------|-------|-----------|
| A — MECHANISM-DERIVED | 22 | Session boundaries, entry/exit timing, invalidation rules, cost models, oscillation control, minimum shock separation |
| B — GOVERNANCE-SELECTABLE | 9 | N, M, confirmation market (RF-001); W, T, index complex (RF-002); S, K, A, index complex (RF-003) |
| C — EMPIRICALLY TUNABLE | 0 | None |
| D — FORMULATION-LEVEL AMBIGUITY | 0 | None |

---

## 5. MECHANISM-DERIVABILITY ANALYSIS

### Parameters that ARE mechanism-derived (Class A)

All Class A parameters are either:
- Defined by external market structure (session boundaries, cost model)
- Logically implied by the mechanism's temporal structure (entry/exit timing, invalidation rules)
- Natural consequences of the mechanism's own definitions (oscillation control, minimum shock separation)

None of these require a research choice. They are outcome-independent.

### Parameters that are NOT mechanism-derived (Class B)

**N (RF-001):** The mechanism implies a finite lookback horizon (a "structurally significant" breakout requires looking back at some number of bars), but the mechanism does not imply a unique value. Different values of N produce different event populations. This is a genuine governance choice.

**M (RF-001):** The mechanism implies a finite confirmation window (confirmation must be assessed within some bounded period), but the mechanism does not imply a unique value. Different values of M produce different confirmation-failure populations. This is a genuine governance choice.

**Confirmation market (RF-001):** The mechanism requires a second index, but any correlated US equity index could serve. Different indices produce different confirmation-failure dynamics. This is a genuine governance choice.

**W (RF-002):** The mechanism implies a finite observation window (synchrony must be measured over some period), but the mechanism does not imply a unique value. Different values of W produce different regime-transition frequencies. This is a genuine governance choice.

**T (RF-002):** The mechanism implies a threshold between synchronized and desynchronized, but the mechanism does not imply a unique value. Different values of T produce different regime-transition populations. This is a genuine governance choice.

**Index complex (RF-002, RF-003):** The mechanism requires multiple indices, but the specific composition is not implied. Different compositions produce different synchrony/absorption dynamics. This is a genuine governance choice.

**S (RF-003):** The mechanism implies a shock threshold (a "large move" affecting the complex), but the mechanism does not imply a unique value. Different values of S produce different shock-event populations. This is a genuine governance choice.

**K (RF-003):** The mechanism implies a finite absorption measurement period, but the mechanism does not imply a unique value. Different values of K produce different absorption-asymmetry populations. This is a genuine governance choice.

**A (RF-003):** The mechanism implies a threshold for "significant" asymmetry, but the mechanism does not imply a unique value. Different values of A produce different asymmetry-event populations. This is a genuine governance choice.

---

## 6. OUTCOME-INDEPENDENCE ANALYSIS

For each proposed resolution, the question is: would we choose this rule/value if we knew nothing about historical economic results?

| Parameter | Outcome-independent? | Reasoning |
|-----------|---------------------|-----------|
| Session boundaries | YES — externally defined | US regular session is a market fact |
| Entry/exit timing | YES — logically implied | Temporal causality requires these rules |
| Invalidation rules | YES — logically implied | If the event reverses, the mechanism is void |
| Cost model | YES — convention | Standard 2 bps round-trip |
| N | REQUIRES GOVERNANCE CHOICE | No value is implied by the mechanism alone |
| M | REQUIRES GOVERNANCE CHOICE | No value is implied by the mechanism alone |
| Confirmation market | REQUIRES GOVERNANCE CHOICE | No index is implied by the mechanism alone |
| W | REQUIRES GOVERNANCE CHOICE | No value is implied by the mechanism alone |
| T | REQUIRES GOVERNANCE CHOICE | No value is implied by the mechanism alone |
| Index complex | REQUIRES GOVERNANCE CHOICE | No composition is implied by the mechanism alone |
| S | REQUIRES GOVERNANCE CHOICE | No value is implied by the mechanism alone |
| K | REQUIRES GOVERNANCE CHOICE | No value is implied by the mechanism alone |
| A | REQUIRES GOVERNANCE CHOICE | No value is implied by the mechanism alone |

---

## 7. PARAMETER-COLLAPSE ANALYSIS

Can any governance-selectable parameter be eliminated?

| Parameter | Can it be collapsed? | Analysis |
|-----------|---------------------|----------|
| N | NO | The mechanism requires a definition of "structurally significant breakout." Without N, there is no event to detect. |
| M | NO | The mechanism requires a bounded confirmation window. Without M, there is no deadline for confirmation failure. |
| Confirmation market | NO | The mechanism requires a second index. Without it, there is no cross-market relationship. |
| W | NO | The mechanism requires an observation window for synchrony. Without W, there is no synchrony measure. |
| T | NO | The mechanism requires a regime boundary. Without T, there is no transition to detect. |
| Index complex | NO | The mechanism requires multiple indices. Without a complex, there is no synchrony or absorption to measure. |
| S | NO | The mechanism requires a shock definition. Without S, there is no event to detect. |
| K | NO | The mechanism requires an absorption measurement period. Without K, there is no absorption measure. |
| A | NO | The mechanism requires an asymmetry threshold. Without A, there is no asymmetry event. |

**No parameter can be eliminated.** All nine governance-selectable parameters are structurally necessary. The mechanism cannot be reformulated to avoid them without changing the mechanism itself.

---

## 8. MECHANISM-PRESERVATION AUDIT

For every proposed parameter resolution, does the resolution change the mechanism?

| Resolution | Mechanism change? | Assessment |
|-----------|------------------|------------|
| Freeze N, M, confirmation market at registration | NO | These parameters define the event population, not the mechanism. The mechanism (confirmation failure) is preserved. |
| Freeze W, T, index complex at registration | NO | These parameters define the regime-transition population, not the mechanism. The mechanism (synchrony regime transition) is preserved. |
| Freeze S, K, A, index complex at registration | NO | These parameters define the asymmetry-event population, not the mechanism. The mechanism (shock absorption asymmetry) is preserved. |

**All resolutions preserve the mechanism.** No parameter resolution transforms a relational mechanism into momentum, breakout, or mean reversion.

---

## 9. DISTINCTNESS RECHECK

After parameter adjudication, does any formulation collapse into prior work?

| Formulation | Still distinct from F-02? | Still distinct from F-03? | Still distinct from mean reversion? | Still distinct from TSMOM? | Still distinct from CAND-083? | Still distinct from breakout/ORB? |
|-------------|--------------------------|--------------------------|-------------------------------------|--------------------------|------------------------------|----------------------------------|
| RF-001 | YES — confirmation failure, not spread trading | YES — event detection, not ranking | YES — cross-market failure, not single-asset mean reversion | YES — cross-market, not own-history | YES — cross-market, not single-market | YES — failure detection, not breakout trading |
| RF-002 | YES — synchrony regime, not pair spread | YES — directional agreement, not strength ranking | YES — regime transition, not displacement fading | YES — cross-market synchrony, not own-trend | YES — cross-market, not single-market | YES — regime detection, not breakout trading |
| RF-003 | YES — absorption asymmetry, not spread trading | YES — shock processing, not strength ranking | YES — absorption characteristics, not displacement fading | YES — cross-market absorption, not own-trend | YES — cross-market, not single-market | YES — shock absorption, not breakout trading |

**All three formulations remain structurally distinct.** No formulation collapses into prior closed work.

---

## 10. FORMULATION-BY-FORMULATION REGISTRATION-READINESS

### RF-001: Cross-Market Confirmation Failure Process

**Classification:** NOT REGISTRATION-READY — GOVERNANCE CHOICE REQUIRED

**Remaining choices:**
1. N (lookback horizon) — owner must select prospectively
2. M (confirmation window) — owner must select prospectively
3. Confirmation market identity — owner must select prospectively

**Blocked by empirical calibration?** NO. All three choices are governance decisions, not empirical tuning. The owner can select values without inspecting economic results.

**Mechanism complete?** YES. The mechanism (confirmation failure) is fully specified. The unresolved parameters define the event population, not the mechanism.

### RF-002: Cross-Market Synchrony Regime Process

**Classification:** NOT REGISTRATION-READY — GOVERNANCE CHOICE REQUIRED

**Remaining choices:**
1. W (window length) — owner must select prospectively
2. T (synchrony threshold) — owner must select prospectively
3. Index complex composition — owner must select prospectively

**Blocked by empirical calibration?** NO. All three choices are governance decisions.

**Mechanism complete?** YES. The mechanism (synchrony regime transition) is fully specified.

### RF-003: Cross-Market Shock Absorption Asymmetry Process

**Classification:** NOT REGISTRATION-READY — GOVERNANCE CHOICE REQUIRED

**Remaining choices:**
1. S (shock threshold) — owner must select prospectively
2. K (absorption window) — owner must select prospectively
3. A (asymmetry threshold) — owner must select prospectively
4. Index complex composition — owner must select prospectively

**Blocked by empirical calibration?** NO. All four choices are governance decisions.

**Mechanism complete?** YES. The mechanism (shock absorption asymmetry) is fully specified.

---

## 11. GOVERNANCE CHOICES STILL REQUIRED

| Formulation | Choice | Type | Owner must authorize? |
|-------------|--------|------|----------------------|
| RF-001 | N (lookback horizon) | Structural parameter | YES |
| RF-001 | M (confirmation window) | Structural parameter | YES |
| RF-001 | Confirmation market identity | Instrument selection | YES |
| RF-002 | W (window length) | Structural parameter | YES |
| RF-002 | T (synchrony threshold) | Structural parameter | YES |
| RF-002 | Index complex composition | Instrument selection | YES |
| RF-003 | S (shock threshold) | Structural parameter | YES |
| RF-003 | K (absorption window) | Structural parameter | YES |
| RF-003 | A (asymmetry threshold) | Structural parameter | YES |
| RF-003 | Index complex composition | Instrument selection | YES |

**Total governance choices required: 10**

---

## 12. EMPIRICAL-CALIBRATION BLOCKERS

**None.**

All unresolved parameters are governance-selectable (Class B). No parameter requires empirical calibration (Class C). No parameter is a formulation-level ambiguity (Class D).

The formulations are not blocked by empirical calibration. They are blocked only by the requirement for prospective owner authorization of structural parameters.

---

## 13. OWNER-SELECTION BOUNDARY

This artifact does NOT:

- Select a winning formulation
- Select parameter values
- Rank formulations by expected performance
- Authorize V38A registration
- Perform economic testing
- Compare candidate economics

The purpose of this adjudication is to establish that:

1. All unresolved parameters are governance-selectable (Class B)
2. No parameter requires empirical tuning (Class C)
3. No parameter is a formulation defect (Class D)
4. All formulations are mechanism-complete
5. All formulations remain distinct from prior work
6. The remaining choices are owner-level governance decisions

The owner may now:
- Select parameter values for one or more formulations
- Authorize V38A registration with frozen parameters
- Defer for further consideration
- Reject formulations that do not meet quality standards

---

## 14. EXPLICIT NO-ECONOMIC-TESTING STATEMENT

**No economic testing was performed in this adjudication.**

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

The adjudication is purely structural and governance-based.

---

**END OF ADJUDICATION ARTIFACT**
