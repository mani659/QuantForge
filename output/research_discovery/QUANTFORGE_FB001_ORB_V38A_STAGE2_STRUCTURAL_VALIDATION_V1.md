# FB-001 ORB — V38A STAGE 2 STRUCTURAL VALIDATION

**Date:** 2026-09-06
**Status:** STRUCTURALLY VALID — STAGE 3 AUTHORIZED

---

## 1. GOVERNING REGISTRATION

```text
Registration:     FB-001-ORB-V38A-REG-V1-r1
Registration SHA: 04e9f804cca93d64ea18396abf5d25d2b968df974ee505f2b0866104e1af8086
Repository HEAD:  45fc4cb (freeze commit)
Predecessor:      FB-001-ORB-V38A-REG-V1 (superseded)
Artifact:         output/research_discovery/QUANTFORGE_FB001_ORB_V38A_REGISTRATION_V1-r1.md
```

---

## 2. IMPLEMENTATION PROVENANCE

```text
Primary implementation:   research/fb001_orb_structural.py
Independent implementation: research/fb001_orb_independent.py
Test suite:               research/fb001_orb_structural_tests.py
Reproducibility test:     research/fb001_orb_reproducibility.py
No existing FB-001 implementation was found in the repository.
Both implementations were created for Stage 2 structural validation.
No production code was modified.
```

---

## 3. DATA USED FOR STRUCTURAL VALIDATION

```text
Data source: Synthetic test data (deterministic, reproducible)
Data purpose: Structural validation only — no economic evidence
Real broker data: NOT used for structural validation
Pre-freeze data: NOT used for economic validation
Post-freeze data: NOT available at time of Stage 2 execution
```

---

## 4. DETERMINISTIC PROCESS RECONSTRUCTION

### 4.1 Session

```text
Regular session: [09:30:00 ET, 16:00:00 ET)
DST: America/New_York (local Eastern Time)
Early close: eligible if after 10:00; full OR still required
Holiday: no session, no opportunity
```

### 4.2 Canonical Bar Semantics

```text
Bar: [bar_open_time, bar_close_time)
bar_close_time = bar_open_time + 1 minute
Completed at bar_close_time
Included if bar_open_time in window
```

### 4.3 Opening Range

```text
Interval: [09:30:00, 10:00:00) — exactly 30 bars
OR_high = max(high), OR_low = min(low)
< 30 bars → NO ORB OPPORTUNITY
Zero-width range (OR_high == OR_low): valid, breakout possible
```

### 4.4 Signal

```text
Signal bar: first completed bar with bar_open_time >= 10:00
Long: close > OR_high
Short: close < OR_low
Equality: NO SIGNAL
No breakout threshold
One signal per session
```

### 4.5 Entry

```text
Market order at signal bar completion
Executed at next bar open (bar with bar_open_time >= signal bar close time)
No stop orders, no pending orders
```

### 4.6 Position State

```text
FLAT → LONG/SHORT → FLAT
Maximum one position per session
No further signals after first entry
```

### 4.7 Exit

```text
Retrace: subsequent bar close <= OR_high (LONG) or >= OR_low (SHORT)
  Executed at retrace bar open
  "Subsequent" = bar_open_time > entry bar close time
Session close: open of final session bar
  Regular: [15:59, 16:00) open
  Early close: bar ending at early_close_time open
Conflict: session close governs
```

### 4.8 Cost Model

```text
Round-trip: 2 bps
Applied mechanically to gross return
No economic metrics reported
```

---

## 5. DETERMINISM EVIDENCE

```text
Test: Run identical synthetic data through primary implementation twice
Result: IDENTICAL structural hash (65c5ddea88eeb66b)
Verdict: DETERMINISM — PASS
```

---

## 6. TEMPORAL / LEAKAGE AUDIT

| Check | Result |
|---|---|
| Pre-09:30 bars excluded from OR | PASS |
| Signal evaluated only after OR completion | PASS |
| Retrace checked only on subsequent bars | PASS |
| No future session info affects earlier session | PASS |

```text
No leakage identified. All decisions use only completed bars available
at the time of the decision. No future information enters any decision.
Verdict: LEAKAGE AUDIT — PASS
```

---

## 7. OPPORTUNITY POPULATION VALIDATION

| Check | Result |
|---|---|
| No-signal sessions → 0 opportunities | PASS |
| One opportunity per qualifying session | PASS |
| Incomplete OR (29 bars) → 0 opportunities | PASS |
| Retraced position counts as 1 opportunity | PASS |
| No post-hoc subset selection | PASS |

```text
Opportunity population constructed exactly per frozen registration.
Verdict: OPPORTUNITY POPULATION — PASS
```

---

## 8. EXECUTION MAPPING VALIDATION

| Case | Description | Result |
|---|---|---|
| A | Long breakout → LONG, entry at next bar open | PASS |
| B | Short breakout → SHORT, entry at next bar open | PASS |
| C | Signal close == OR_high or OR_low → NO SIGNAL | PASS |
| D | Long breakout then retrace → exit at retrace bar open | PASS |
| D | Short breakout then retrace → exit at retrace bar open | PASS |
| E | Entry execution bar not counted as retrace | PASS |
| F | Final session bar identified, exit at its open | PASS |
| G | Session close / retrace conflict → session close governs | PASS |
| H | Price within range → NO OPPORTUNITY | PASS |
| I | Fewer than 30 OR bars → NO OPPORTUNITY | PASS |
| J | Early close after 10:00 → full OR, early final bar | PASS |
| K | Early close before 10:00 → NO OPENING RANGE | PASS |
| L | DST transition → session remains 09:30–16:00 ET | PASS |

```text
All 13 execution mapping cases pass.
Verdict: EXECUTION MAPPING — PASS
```

---

## 9. DATA-QUALITY VALIDATION

| Check | Result |
|---|---|
| Missing bars → deterministic skip, no fabrication | PASS |
| Malformed bars → excluded from calculation | PASS |
| Duplicate timestamps → first occurrence wins | PASS |
| Conflicting duplicates → first occurrence, auditable | PASS |
| Out-of-order bars → reordered by bar_close_time | PASS |

```text
Data quality rules implemented exactly per V1-r1 §15.
Verdict: DATA-QUALITY HANDLING — PASS
```

---

## 10. REPRODUCIBILITY EVIDENCE

```text
Primary implementation: fb001_orb_structural.py (class-based, dataclass outcomes)
Independent implementation: fb001_orb_independent.py (functional, dict outcomes)

Test cases compared:
  1. Long breakout, session close      — PASS
  2. Short breakout, session close     — PASS
  3. Long breakout, retrace            — PASS
  4. Short breakout, retrace           — PASS
  5. No breakout                       — PASS
  6. Incomplete OR                     — PASS

All structural fields match exactly between implementations.
Verdict: INDEPENDENT REPRODUCIBILITY — PASS
```

---

## 11. COST-MODEL CONSISTENCY

```text
Round-trip cost: 2 bps (1 bps entry + 1 bps exit)
Applied uniformly to all trades
Mechanically subtracted from gross return
No economic metrics computed or reported
Verdict: COST-MODEL CONSISTENCY — PASS
```

---

## 12. DEVIATIONS / ISSUES

```text
Finding 1: Malformed final session bar
  The V1-r1 registration does not explicitly specify behavior when the
  canonical final session bar (e.g., [15:59, 16:00)) is malformed and
  excluded from valid bars. The implementation uses the last valid bar
  at or before the canonical final bar time as the session-close bar.

  Classification: Implementation-level decision, not a registration defect.
  Impact: Does not affect determinism, reproducibility, or correctness.
  The registration could be clarified in a future revision if needed.
```

---

## 13. STAGE 2 VERDICT

**STRUCTURALLY VALID**

All eight structural criteria are satisfied:

| Criterion | Result |
|---|---|
| Deterministic implementation | PASS |
| Reproducibility | PASS |
| Absence of forward-information leakage | PASS |
| Correct opportunity-population construction | PASS |
| Correct state transitions | PASS |
| Correct temporal ordering | PASS |
| Correct execution-price mapping | PASS |
| Cost-model consistency | PASS |

---

## 14. ECONOMIC QUALIFICATION

```text
No economic qualification was performed during Stage 2.

No P&L computed.
No expectancy computed.
No win rate computed.
No Sharpe ratio computed.
No drawdown computed.
No profit factor computed.
No cumulative return computed.
No benchmark comparison performed.

Economic validation is authorized only after Stage 2 structural sign-off.
Stage 3 Economic Validation is now AUTHORIZED.
```

---

## 15. GOVERNANCE STATUS

```text
FB-001-ORB-V38A-REG-V1-r1

V38A Stage: 1 (Registration)    — COMPLETE
V38A Stage: 2 (Structural)      — COMPLETE — STRUCTURALLY VALID
V38A Stage: 3 (Economic)        — AUTHORIZED — NOT YET EXECUTED
V38A Stage: 4 (Adjudication)    — NOT YET EXECUTED

Base Registry: EMPTY
F-01: UNCHANGED
```

---

**END OF FB-001 ORB V38A STAGE 2 STRUCTURAL VALIDATION**
