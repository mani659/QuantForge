# QUANTFORGE — CAND-077 + CAND-081 STATE GOVERNANCE REVIEW V1
# DATE: 2026-08-30
# STATUS: GOVERNANCE REVIEW COMPLETE
# NO EXPERIMENT / NO G2 / NO V28 / NO OPTIMIZATION

---

## 1. Purpose

Perform a formal State Governance Review of:
- CAND-077 — Volatility Character Transition
- CAND-081 — Structural Level Failure Trap

following completion of V27 G1.

This determines:
1. What each candidate actually represents
2. Whether each deserves formal State Review status
3. Whether the two States are genuinely distinct
4. What evidence supports each
5. What remains unproven
6. What future qualification path is permissible
7. What must be permanently protected from reinterpretation
8. Whether V28 G0 can begin from a clean State library

---

## 2. Authoritative Current State

- HEAD: `a9c9625` — `docs: complete V27 G1 economic plausibility screen`
- V27 G1: COMPLETE
- V28 G0: NOT STARTED
- Forward runtime: ACTIVE / PROTECTED / UNTOUCHED

---

## 3. V27 G1 Context

V27 G1 evaluated three candidates:
- CAND-080: INSUFFICIENT (counterfactual failed — zero events) → CLOSED
- CAND-081: INFORMATIONALLY INTERESTING (+1.23 bps conditional delta) → STATE REVIEW ELIGIBLE
- CAND-082: INFORMATIONALLY INTERESTING (outlier-dependent, State hypothesis contradicted) → CLOSED

No G2 promotions. One new State Review Eligible object (CAND-081) added to the library alongside the existing CAND-077.

---

## 4. CAND-077 — Independent Governance Review

### 4.1 Original Mechanism

**Frozen hypothesis (V26):** Compression → Expansion volatility transition produces economically useful downstream behavior.

**State interpretation:** A transition in volatility *character* — from compressed/low-activity to expanded/high-activity — may alter the economics of subsequent events.

### 4.2 Original Evidence

| Metric | Value |
|---|---|
| N | 2,084 |
| Frequency | ~700/year |
| Gross Mean | +1.15 bps |
| Gross Median | +0.86 bps |
| Net Mean | -0.85 bps |
| Net Median | -1.14 bps |
| Counterfactual N | 387 |
| Counterfactual Mean | -2.52 bps |
| Counterfactual Median | -1.90 bps |
| Conditional Delta | **+1.67 bps** (TREATMENT SUPERIOR) |
| Hard Validity Gates | ALL 9 PASS |

### 4.3 Post-Closure Exploratory Evidence

| Filter | N | WR | Gross Mean | Gross Median |
|---|---|---|---|---|
| Baseline | 2,084 | 54.5% | +1.15 | +0.86 |
| Breakout > 15 bps | 219 | 64.8% | +8.41 | +6.97 |
| Breakout > 20 bps | 133 | 64.7% | +8.45 | +10.14 |

**Classification:** EXPLORATORY EVIDENCE ONLY — NOT VALIDATED

### 4.4 What Is Established

**CONFIRMED HISTORICAL OBSERVATION:**
- The compression-to-expansion transition is objectively definable using ATR percentile
- N=2,084 observations across ~3 years of USATECHIDXUSD M1 data
- Treatment (fade the breakout direction after transition) outperforms counterfactual by +1.67 bps (mean) — largest conditional delta in RF history
- All 9 hard validity gates pass
- The transition is genuinely dynamic (not a static threshold)
- The counterfactual (same breakout in already-expanded state) is valid and discriminating

### 4.5 What Is Exploratory

**EXPLORATORY OBSERVATION:**
- Breakout magnitude relationship (larger breakout → higher WR/mean)
- >15 bps threshold: N=219, WR=64.8%, +8.41 bps mean
- Time-of-day effects (Hours 15/17/18/20)
- Day-of-week effects (Tuesday strongest)
- Monotonic relationship between breakout size and economics

These are POST-CLOSURE observations subject to selection bias. They may inform hypothesis generation but must NOT be treated as confirmatory evidence.

### 4.6 What Is Hypothesized

**FUTURE HYPOTHESIS:**
- Expansion magnitude after compression contains incremental information about downstream outcome distribution
- The transition from compressed to expanded volatility creates a specific market condition that could modify other strategies' economics
- The monotonic breakout-magnitude relationship may reflect a genuine information content gradient

### 4.7 Economic Mechanism

**OBSERVED:**
- Compression-to-expansion transition creates directional breakout
- Fade-the-trend entry after the transition outperforms fade in already-expanded state
- The transition itself contains +1.67 bps of informational value

**HYPOTHESIZED:**
- During compression, participants accumulate positions with tight stops
- The expansion event triggers stop cascades on the breakout side
- The trapped-participant exit flow creates directional pressure against the breakout
- This pressure is specific to the transition, not to the expanded state

**UNPROVEN:**
- Actual participant positioning or stop placement
- Whether the mechanism is stop-cascade-driven or information-driven
- Whether the effect will persist in future data

### 4.8 Participant Mechanism

The participant constraint is: positions accumulated during compression have stops clustered near the compression range. The expansion breaks through these stops, creating forced exit flow. The transition from compressed to expanded creates a specific population of trapped participants who did not exist during the compressed phase.

### 4.9 Dynamic-vs-Static Test

The transition is essential:
- CAND-077 tests the compression→expansion transition, not "compressed volatility" as a static state
- The counterfactual (same breakout in already-expanded state) shows the transition adds +1.67 bps of value
- A static "high volatility" filter would not capture the same information

**RESULT: PASS** — the transition is causally meaningful.

### 4.10 Prior-Art

CAND-077 is NEW. No prior QuantForge candidate tested the compression→expansion volatility transition as a directional signal.

Historical check:
- CAND-040: volatility expansion (tested expansion itself, not the compression→expansion transition)
- CAND-077 is distinct because it specifically requires the transition FROM compressed TO expanded

### 4.11 State Classification

> **STATE REVIEW ELIGIBLE**

**State concept:** A transition in volatility character from compressed/smooth to expanded/active creates a specific market condition that may modify the economics of downstream events.

The State is the *transition itself*, not the static compressed or expanded state. The transition creates a temporary market condition with specific participant dynamics.

### 4.12 Future Qualification Path

```
CAND-077 historical observation (+1.67 bps conditional delta)
        ↓
Formal State hypothesis registration (NEW, independently governed)
        ↓
Hypothesis must define:
  - exact state concept (volatility character transition)
  - exact pre-entry observable (ATR percentile transition)
  - exact threshold (frozen BEFORE testing — NOT 15 bps)
  - exact treatment
  - exact counterfactual
  - qualified downstream Alpha target
        ↓
Interaction study (separately authorized)
        ↓
State qualification
```

**Critical:** The formal State hypothesis must be independently governed. It must NOT:
- Simply select "breakout >15 bps" because it had the best historical result
- Use the same data without a holdout
- Be treated as a continuation of CAND-077

---

## 5. CAND-081 — Independent Governance Review

### 5.1 Original Mechanism

**Frozen hypothesis (V27 G0):** When price breaks a structural level (20-bar high/low) by 3+ bps but reverses back through the level within 5 bars, trapped breakout participants create directional pressure against the breakout direction.

**State interpretation:** The presence of a trapped participant population following a failed structural break creates a specific market condition.

### 5.2 G1 Evidence

| Metric | Value |
|---|---|
| N | 3,887 |
| Frequency | ~1,361/year |
| Gross Mean | +1.22 bps |
| Gross Median | +1.70 bps |
| Net Mean | -0.78 bps |
| Net Median | -0.30 bps |
| Win Rate | 53.0% |
| Worst | -398.47 bps |
| Best | +1,077.12 bps |
| Excluding Best | -1.06 bps |

### 5.3 Counterfactual

| Metric | Treatment | Counterfactual |
|---|---|---|
| N | 3,887 | 3,364 |
| Net Mean | -0.78 bps | -2.01 bps |
| Net Median | -0.30 bps | -2.62 bps |
| WR | 53.0% | 48.3% |

Counterfactual: Successful breakouts (price breaks level and stays above for 5+ bars, no failure). Same fade entry applied after confirmation.

**Counterfactual assessment:** VALID / DISCRIMINATING

### 5.4 Conditional Evidence

Delta Mean: **+1.23 bps** (TREATMENT SUPERIOR)
Delta Median: **+2.33 bps** (TREATMENT SUPERIOR)

This is the **second-strongest conditional delta** in RF history (after CAND-077's +1.67 bps).

The delta is consistent across both mean and median — the trap mechanism adds genuine informational value.

### 5.5 Absolute Economics

Net Mean: -0.78 bps
Net Median: -0.30 bps

**Absolute economics are negative.** CAND-081 is NOT a standalone economically qualified Alpha. The +1.23 bps conditional delta is informational evidence, not standalone profitability.

### 5.6 Economic Mechanism

**OBSERVED:**
- Failed breakouts (trap formed) produce better fade outcomes than successful breakouts (no trap)
- Treatment outperforms counterfactual by +1.23 bps (mean) and +2.33 bps (median)
- The trap mechanism adds genuine informational value

**HYPOTHESIZED:**
- Breakout participants enter with stops beyond the structural level
- When the breakout fails, these participants face losses
- As price reverses through the level, stops are triggered
- Forced exit flow accelerates the reversal
- The trap creates a specific population of trapped participants who did not exist before the breakout attempt

**UNPROVEN:**
- Actual participant positioning or stop placement
- Whether the mechanism is stop-cascade-driven or information-driven
- Whether the effect will persist in future data

### 5.7 Participant Mechanism

The participant constraint is: breakout participants enter expecting continuation. When the breakout fails within 5 bars, these participants face losses. Their stops are placed beyond the breakout level. As price reverses through the level, stops are triggered, creating forced exit flow that accelerates the reversal.

The trap creates a specific, time-bounded market condition with identifiable participant dynamics.

### 5.8 Dynamic-vs-Static Test

The break-and-fail is essential:
- "Price below the 20-bar high" alone is not the signal
- The BREAK and FAIL creates a specific trapped-participant population
- The forced-exit flow is specific to the trap, not to the static position below the level
- The timing of the reversal is linked to the trap formation, not to the static level

**RESULT: PASS** — the transition is causally meaningful.

### 5.9 Prior-Art

CAND-081 is NEW. No prior QuantForge candidate tested the "structural level break and failure trap" as a directional signal.

Historical check:
- CAND-059: first touch > subsequent touch (different — no break-and-fail required)
- CAND-065: deep sweep > shallow sweep (different — no failure requirement)
- CAND-070: momentum micro-structure failure (different — tested fading first structure break in trend, falsified)
- CAND-055: IB false breakout (similar concept but different mechanism — IB is time-based, not structural price level)

### 5.10 State Classification

> **STATE REVIEW ELIGIBLE**

**State concept:** The presence of a trapped participant population following a failed structural break creates a specific market condition that may modify the economics of subsequent events.

The State is the *trap condition itself* — the combination of a structural level break, failure, and resulting trapped participants.

### 5.11 Future Qualification Path

```
CAND-081 historical observation (+1.23 bps conditional delta)
        ↓
Formal State hypothesis registration (NEW, independently governed)
        ↓
Hypothesis must define:
  - exact state concept (trapped participant population after failed break)
  - exact structural level definition
  - exact failure window
  - exact treatment
  - exact counterfactual
  - qualified downstream Alpha target
        ↓
Interaction study (separately authorized)
        ↓
State qualification
```

---

## 6. CAND-077 vs CAND-081

### 6.1 Mechanism Difference

| | CAND-077 | CAND-081 |
|---|---|---|
| Mechanism | Volatility character transition | Structural level failure trap |
| What changes | Market regime (smooth → choppy) | Participant state (free → trapped) |
| Trigger | ATR percentile transition | Price breaks and fails at structural level |
| Timeframe | Regime-level (hours/days) | Event-level (minutes) |

### 6.2 Observable Difference

| | CAND-077 | CAND-081 |
|---|---|---|
| Primary observable | ATR percentile + directional inconsistency | Price vs structural level |
| Transition detection | Incon crosses 0.35 → 0.50 | Price breaks level by 3+ bps, reverses within 5 bars |
| ATR constraint | ATR within 80-120% of average | None |

### 6.3 Participant Difference

| | CAND-077 | CAND-081 |
|---|---|---|
| Trapped participants | Trend followers with tight stops | Breakout traders with stops beyond level |
| Forced flow source | Choppy regime triggers stops on both sides | Level failure triggers stops on breakout side |
| Directionality | Counter-trend (fade) | Counter-breakout (fade) |

### 6.4 Economic Difference

| | CAND-077 | CAND-081 |
|---|---|---|
| Conditional delta | +1.67 bps (mean) | +1.23 bps (mean) |
| Median delta | Not reported separately | +2.33 bps |
| Absolute economics | -0.85 bps | -0.78 bps |
| Counterfactual | Valid (387 events) | Valid (3,364 events) |

### 6.5 Independence Assessment

**The two mechanisms are genuinely independent.**

- They use different observables (ATR percentile vs price level)
- They detect different transitions (regime change vs event failure)
- They trap different participant populations (trend followers vs breakout traders)
- They operate on different timeframes (regime-level vs event-level)
- They could theoretically coexist (a choppy regime could contain structural level failures)

### 6.6 Can They Coexist?

**Yes.** The two States are conceptually compatible:
- CAND-077 describes a regime-level condition (market character)
- CAND-081 describes an event-level condition (trap after failed break)
- A market could be in a choppy regime (CAND-077) AND contain structural level failures (CAND-081)
- They are not mutually exclusive

---

## 7. State Library Review

| Candidate | Mechanism | Classification | Change |
|---|---|---|---|
| CAND-059 | First Touch > Subsequent Touch | STATE-ARTIFACT | PRESERVED |
| CAND-065 | Deep Sweep > Shallow Sweep | STATE OBSERVATION | PRESERVED |
| CAND-069 | Mid-session > Morning | STATE OBSERVATION | PRESERVED |
| CAND-077 | Vol compression → expansion | STATE REVIEW ELIGIBLE | PRESERVED |
| CAND-079 | Gold vol transition → Tech | STATE OBSERVATION | PRESERVED |
| **CAND-081** | **Structural level failure trap** | **STATE REVIEW ELIGIBLE** | **PRESERVED** |

**EXISTING STATE CLASSIFICATIONS PRESERVED EXCEPT WHERE THIS REVIEW EXPLICITLY AUTHORIZES AN UPDATE.**

No changes to existing classifications. CAND-081 was added to the library after V27 G1. This review confirms both CAND-077 and CAND-081 remain STATE REVIEW ELIGIBLE.

---

## 8. Evidence Classification

### CAND-077

| Observation | Classification |
|---|---|
| Compression→expansion transition is objectively definable | CONFIRMED HISTORICAL OBSERVATION |
| N=2,084, +1.67 bps conditional delta | CONFIRMED HISTORICAL OBSERVATION |
| All 9 validity gates pass | CONFIRMED HISTORICAL OBSERVATION |
| Breakout magnitude relationship (monotonic) | EXPLORATORY OBSERVATION |
| >15 bps = 64.8% WR, +8.41 bps | EXPLORATORY OBSERVATION |
| Time-of-day effects | EXPLORATORY OBSERVATION |
| "Expansion magnitude contains information" | FUTURE HYPOTHESIS |
| Stop-cascade mechanism explains the effect | HYPOTHESIS (UNPROVEN) |
| Effect will persist in future data | UNRESOLVED QUESTION |

### CAND-081

| Observation | Classification |
|---|---|
| Structural level break-and-fail is objectively definable | CONFIRMED HISTORICAL OBSERVATION |
| N=3,887, +1.23 bps conditional delta | CONFIRMED HISTORICAL OBSERVATION |
| All 9 validity gates pass | CONFIRMED HISTORICAL OBSERVATION |
| Counterfactual valid and discriminating | CONFIRMED HISTORICAL OBSERVATION |
| Median delta +2.33 bps (broad-based) | CONFIRMED HISTORICAL OBSERVATION |
| Absolute economics negative (-0.78 bps) | CONFIRMED HISTORICAL OBSERVATION |
| Trapped participant mechanism explains the effect | HYPOTHESIS (UNPROVEN) |
| Effect will persist in future data | UNRESOLVED QUESTION |

---

## 9. Selection / Hindsight Risks

### CAND-077

- **Post-closure filter selection:** The breakout-magnitude filters were tested AFTER observing the baseline outcome. This is selection bias.
- **Multiple thresholds tested:** Six threshold levels were examined. The >15 bps result may be sample-specific.
- **Same-sample validation:** All filter results use the same historical data as the baseline G1 screen.

### CAND-081

- **No selection bias in the primary result:** The G0 definition was frozen before G1 execution. The +1.23 bps delta is from the frozen definition.
- **High event frequency:** ~1,361 events/year suggests the 20-bar structural level may be too loose, but this is a G0 definitional observation, not a G1 optimization finding.

---

## 10. Numerical Threshold Governance

> **NO NUMERICAL FILTER THRESHOLD IS RATIFIED.**

For CAND-077:
- The >15 bps breakout observation remains EXPLORATORY EVIDENCE ONLY
- No threshold is approved for any future hypothesis
- Any future threshold must be frozen BEFORE confirmatory testing

For CAND-081:
- The 20-bar structural level and 3 bps breakout threshold are the frozen G0 definitions
- These are not "optimized" thresholds — they are the original hypothesis
- Future formalization may refine these, but only through governed hypothesis registration

---

## 11. State vs Alpha Classification

| Candidate | State Decision | Alpha Decision | Absolute Economics | Conditional Evidence | Future Path |
|---|---|---|---|---|---|
| CAND-077 | STATE REVIEW ELIGIBLE | NOT ALPHA (negative standalone) | -0.85 bps | +1.67 bps delta | State qualification path |
| CAND-081 | STATE REVIEW ELIGIBLE | NOT ALPHA (negative standalone) | -0.78 bps | +1.23 bps delta | State qualification path |

Both candidates are classified as STATE REVIEW ELIGIBLE, not as standalone Alphas. Their conditional deltas are informational evidence, not standalone profitability.

---

## 12. Future State Qualification Framework

For each State Review Eligible object, the future path is:

```
Historical observation
        ↓
Formal State definition (NEW hypothesis, independently governed)
        ↓
Definition frozen BEFORE outcome testing
        ↓
Independently qualified downstream event / Alpha identified
        ↓
Prospective State × Alpha interaction test
        ↓
State qualification
```

**Requirements:**
- The State definition must be frozen BEFORE testing
- A legitimate downstream Alpha must be independently identified
- The interaction test must be separately authorized
- CAND-024/CAND-035 must NOT be retroactively designated as downstream Alphas

---

## 13. Closed-Line Firewall

All closed research lines preserved:
- V19–V27 closed candidates: NOT REOPENED
- CAND-071 through CAND-076: CLOSED
- CAND-078: CLOSED
- CAND-080: CLOSED (V27 G1)
- CAND-082: CLOSED (V27 G1)
- No inverse hypotheses authorized
- No rescues performed

---

## 14. CAND-079

> STATE OBSERVATION — PRESERVED

Delta: +0.78 bps (weak). Not elevated to STATE REVIEW ELIGIBLE. Not reopened.

---

## 15. CAND-080

> CLOSED — INSUFFICIENT (counterfactual failed)

No rescue. No redesign.

---

## 16. Protected Forward Runtime

CAND-015:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-024:
> ACTIVE / PROTECTED / UNTOUCHED

CAND-035:
> ACTIVE / PROTECTED / UNTOUCHED

---

## 17. V28 Readiness

> **V28 G0 READY**

The State library is sufficiently governed for V28 G0 to begin:
- CAND-077: STATE REVIEW ELIGIBLE (preserved, not reopened)
- CAND-081: STATE REVIEW ELIGIBLE (preserved, not reopened)
- Both are clearly classified and fenced off
- V28 may proceed with fresh discovery, independent of both State objects

---

## 18. Governance Decision

**CAND-077:** STATE REVIEW ELIGIBLE — PRESERVED
**CAND-081:** STATE REVIEW ELIGIBLE — PRESERVED
**Both:** Independent State qualification paths defined
**V28:** READY
**Numerical thresholds:** NOT RATIFIED
**Interaction studies:** NOT AUTHORIZED
**Rescue:** NOT PERFORMED

---

## 19. Integrity / Consistency Check

| Check | Status |
|---|---|
| A. CAND-077 exploratory threshold NOT ratified | PASS |
| B. CAND-077 NOT optimized | PASS |
| C. CAND-081 NOT promoted to standalone Alpha | PASS |
| D. CAND-077 and CAND-081 remain conceptually distinct | PASS |
| E. No closed candidate reopened | PASS |
| F. No forward runtime inspected or modified | PASS |
| G. No new experiment executed | PASS |
| H. No V28 candidate generated | PASS |
| I. No G2 executed | PASS |
| J. SESSION_HANDOFF sufficient for new session | PASS |
