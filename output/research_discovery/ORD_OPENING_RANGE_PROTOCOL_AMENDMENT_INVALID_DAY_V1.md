# QUANTFORGE — ORD INVALID-DAY DENOMINATOR PROTOCOL AMENDMENT

*Prepared 2026-08-18. Outcome-blind. No execution authorized.*

---

## 1. Executive Decision

**AMENDMENT PROPOSAL PREPARED — AWAITING INDEPENDENT AUDIT AND APPROVAL**

The frozen ORD V1.0.0 invalid-day denominator ("all calendar dates containing ≥ 1 M1 observation") includes weekend dates with stray M1 observations, causing the >10% anomaly gate to halt execution for data-contamination reasons unrelated to the market-session population being studied. This amendment narrows the denominator to dates containing at least one M1 observation during each market's defined post-opening-range detection window, thereby excluding weekends and holidays without active-market data.

---

## 2. Current Frozen State

| Item | Value |
|---|---|
| Protocol | ORD V1.0.0 |
| Protocol SHA-256 | `cc01b23cf213abc906750d7ec1d238089047baa3b6fb9bf0beb733bf1b0649a7` |
| Definition Lock | V1 (unchanged) |
| Pre-registration audit | PASS — APPROVED FOR ORD MULTI-MARKET EXECUTION |
| Execution result | STOPPED (denominator > 10% for all four markets) |
| Stop adjudication | CONDITIONAL (denominator valid; detection-window implementation error) |
| Denominator governance | DETERMINATE — WEEKENDS INCLUDED (frozen protocol includes weekends with stray data) |

---

## 3. Problem Requiring Amendment

The frozen V1.0.0 denominator counts every calendar date containing ≥ 1 M1 observation. For XAUUSD/XAGUSD, 256 Sunday dates contain residual M1 observations (adjacent Friday close / Sunday evening open timestamps). These Sundays fail the opening-window gate and are counted as invalid days, inflating the invalid-day fraction from ~1% (weekday-only) to ~17% (including Sundays). The >10% anomaly gate halts execution.

The denominator is functioning as designed — but its design captures data-contamination dates (weekends with stray records) that are outside the ORD market-session population. The amendment narrows the denominator to the intended population.

---

## 4. Scientific Scope of the Amendment

**Scope:** Invalid-day anomaly denominator only (protocol §20).

**Changes to:**
- The definition of which dates enter the denominator.
- The definition of which dates are counted as invalid days.

**Does NOT change:**
- Opening-range definition, timestamps, or duration.
- Breakout detection rules or the "through 17:00:00 ET" boundary.
- Entry price or invalidation semantics.
- Control definition or control sign.
- Primary response (120-minute horizon, bp return from entry).
- ΔM statistic or median convention.
- Bootstrap mechanics (day-cluster stationary, B=10,000, seed 20260818).
- Null construction or p-value formula.
- Confidence interval construction.
- Holm family or α.
- Evaluability threshold (≥100 treatment events).
- Market universe (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD; EURUSD excluded).
- Classification rules.
- Secondary analyses.
- Event uniqueness or day-cluster coupling.

---

## 5. Exact Current Rule

Protocol §20 (V1.0.0):

> "**Invalid-day denominator (explicit, not silently borrowed):** all calendar dates containing ≥ 1 M1 observation after timestamp normalization and duplicate removal; weekends/holidays with no data are not counted. An **invalid day** = a date with ≥ 1 observation that fails the opening-window completeness gate (missing/zero-width/§20-invalid window). The **invalid-day fraction** is computed BEFORE primary inference; **if it exceeds 10%, execution HALTS for an anomaly audit**."

---

## 6. Exact Proposed Rule

Protocol §20 (V1.1.0 — amended):

> "**Invalid-day denominator (explicit, not silently borrowed):** the denominator consists of calendar dates containing ≥ 1 M1 observation whose timestamp falls within the market's defined post-opening-range detection window (after the 30-minute opening window closes through 17:00:00 ET inclusive) on that date, after timestamp normalization (UTC → America/New_York) and duplicate removal. A date with M1 observations only outside the detection window (e.g., weekends, holidays, or pre-window hours) does not enter the denominator. An **invalid day** = a denominator date that fails the opening-window completeness gate (missing/zero-width/§20-invalid 30-bar window with valid OHLC and W > 0). The **invalid-day fraction** is computed BEFORE primary inference; **if it exceeds 10%, execution HALTS for an anomaly audit** (the 10% threshold is inherited from the project's data-gate convention; the invalid-day definition is registered here explicitly, correcting the ambiguity recorded in DISC-025 and resolved by the denominator governance decision)."

---

## 7. Scientific Rationale

The ORD experiment studies opening-range breakout behavior during active market sessions. The anomaly-quality denominator should measure data integrity within the population of dates that can participate in the ORD event structure — dates where the market was active during the detection window (03:30–17:00 ET for XAUUSD/XAGUSD/BTCUSD; 10:00–17:00 ET for USATECHIDXUSD).

Weekend dates with stray M1 observations (e.g., Sunday evening open timestamps for gold/silver) contain no active-market data during the detection window. These dates cannot produce ORD events; they are outside the scientific population. Including them in the denominator measures data-file contamination rather than market-session data quality.

The amended denominator aligns the anomaly gate with the actual population being studied: dates on which the market was active during ORD-relevant hours.

---

## 8. Governance Rationale

The amendment follows the governance chain:

1. **V1.0.0 execution STOP** — denominator > 10% for all markets.
2. **Stop adjudication** — denominator STOP was valid (executor correctly included weekends per frozen protocol).
3. **Denominator governance decision** — DETERMINATE: weekends ARE included under V1.0.0 wording.
4. **This amendment** — changes the denominator to exclude dates outside the market-session detection window.

The amendment is not justified by performance outcomes. It is justified by the scientific validity of the anomaly-quality population.

---

## 9. Holiday / Weekend Treatment

**Weekends:** Dates with M1 observations only during weekend hours (e.g., Sunday evening timestamps) have no observations during the post-opening-range detection window (03:30–17:00 ET for XAU/XAG/BTC; 10:00–17:00 ET for USATECH). These dates are excluded from the denominator.

**Holidays:** A holiday where the market is fully closed has no M1 observations during the detection window. It is excluded from the denominator (no observation → not a denominator date). A holiday where the market opens late but still trades during the detection window IS included in the denominator (has observations in the detection window).

**No explicit holiday calendar is introduced.** The rule is deterministic and observation-driven: a date enters the denominator if and only if it has ≥ 1 M1 observation within the detection window. This avoids the need for exchange-specific holiday lists.

**Zero-observation dates:** A date with no M1 observations at all does not enter the denominator (consistent with V1.0.0).

---

## 10. Unchanged ORD Semantics

All of the following are **explicitly unchanged**:

- Definition Lock V1 (unchanged, not modified)
- Opening range: 30-minute window, 03:00–03:29 ET (XAU/XAG/BTC) or 09:30–09:59 ET (USATECH)
- Breakout: first close strictly beyond the OR edge through 17:00:00 ET inclusive
- Entry: breakout-candle close
- Invalidation: close back through the broken edge
- Control: penetration without qualifying close-break; sign = attempt direction
- Primary response: bp directional return from entry close to 120-minute horizon close
- Horizon: 120 minutes wall-clock, complete horizon required
- ΔM: median(treatment) − median(control)
- Bootstrap: day-cluster stationary, geometric blocks p=0.1, circular wrap, truncate to N, B=10,000, seed=20260818
- Null: ΔM*_null = ΔM* − ΔM_obs
- p-value: (1 + count)/(1 + B_valid), inclusive ≥
- CI: percentile 2.5/97.5 of ΔM* distribution
- Holm: evaluable-market family, α=0.05
- Evaluability: ≥100 treatment events, finite treatment+control
- Classification: SUPPORT/CONTRADICTED/INCONCLUSIVE/EVIDENCE-LIMITED
- Market universe: XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD (EURUSD excluded)
- Event uniqueness: ≤2 events per market per day, first per direction
- Day-cluster coupling
- Secondary analyses (MFE, range-normalized return, invalidation rate, halves, year-by-year)
- Cross-market interpretation firewall
- Closed-line independence

---

## 11. Historical V1 Preservation

ORD V1.0.0 remains the original frozen protocol. Its STOPPED execution remains part of the permanent research record. The V1.0.0 protocol file (`ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1.md`) is not modified. The V1.0.0 execution report, statistics, event table, and metadata are not modified. The V1.0.0 denominator governance decision is not modified.

The amended protocol is a new version (V1.1.0) that supersedes V1.0.0 for future execution only.

---

## 12. Outcome-Blindness

This amendment is prepared without reference to:

- Any ORD event count
- Any ORD ΔM value
- Any ORD p-value or confidence interval
- Any ORD market classification
- Any market's specific invalid-day fraction
- Any market's performance characteristics
- Any expected statistical outcome

The amendment is justified solely by the scientific validity of the anomaly-quality denominator population.

---

## 13. Versioning

**Proposed version:** V1.1.0

**Rationale:** Following the H01 precedent (v1.0.0 → v1.1.0 for specification amendments), this is a minor-level amendment that changes a deterministic definition (the denominator population) without altering the scientific object, statistical machinery, or inference rules. A patch-level number (V1.0.1) would be insufficient for a change that materially alters which dates participate in the anomaly gate. The amendment is substantive enough to warrant a minor version increment.

---

## 14. Proposed Protocol Identity

| Item | Value |
|---|---|
| Inherited protocol | ORD V1.0.0 |
| Inherited SHA-256 | `cc01b23cf213abc906750d7ec1d238089047baa3b6fb9bf0beb733bf1b0649a7` |
| Amendment identifier | AMEND-DENOM-1 (invalid-day denominator population) |
| New version | V1.1.0 |
| Sections modified | §20 (Data Gates — invalid-day denominator definition) |
| Sections unchanged | All other sections (§1–§19, §21–§29) |
| Definition Lock | Unchanged |
| Proposed SHA-256 | `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06` (raw bytes on disk; CRLF line endings) |

---

## 15. Amendment Risk Audit

| Risk Factor | Changed by Amendment? | Evidence |
|---|---|---|
| Treatment/control event detection | NO | §5 unchanged; detection logic independent of denominator |
| Event-day eligibility (opening-window gate) | NO | §4 unchanged; eligibility check is before denominator |
| Primary response (120-min bp) | NO | §8 unchanged |
| Control definition and sign | NO | §10 unchanged |
| ΔM statistic | NO | §12 unchanged; median of treatment/control responses |
| Bootstrap sampling unit | NO | §14 unchanged; day-cluster stationary bootstrap |
| Null construction | NO | §15 unchanged; recentered bootstrap |
| p-value formula | NO | §15 unchanged |
| Confidence interval | NO | §16 unchanged |
| Holm family | NO | §17 unchanged; evaluable-market family |
| Classification rules | NO | §18 unchanged |
| Market universe | NO | §3 unchanged; XAU/XAG/USATECH/BTC |
| Evaluability threshold | NO | §13 unchanged; ≥100 treatment events |
| Definition Lock | NO | Not modified |
| **Invalid-day denominator** | **YES** | §20 changed: narrowed to detection-window dates |
| **Invalid-day fraction** | **YES** | Fraction will change because denominator shrinks |
| **>10% halt gate** | **YES** | May no longer trigger for some markets |

**Conclusion:** The amendment is surgical. Only the denominator definition changes. No scientific object, statistical estimator, inference machinery, or classification rule is affected. The amendment cannot change which treatment/control events exist, what their responses are, or how the bootstrap/null/Holm machinery operates.

## 16. Required Independent Audit

Before execution, the amended protocol requires:

1. **Independent amendment audit** — verify that:
   - Only §20 is modified.
   - No scientific object, statistical, or inference change was introduced.
   - The amended denominator is deterministic and outcome-blind.
   - The Definition Lock is unchanged.
   - The amendment is compatible with the frozen ORD object.

2. **Pre-execution integrity check** — verify:
   - Amended protocol SHA-256 matches the frozen file.
   - All input data fingerprints match.
   - Universe unchanged.

---

## 17. Execution Authorization

**NO EXECUTION AUTHORIZATION**

The sequence after this task:

1. ✅ Amendment proposal (this document)
2. ⬜ Independent amendment audit
3. ⬜ Owner/governance approval
4. ⬜ Frozen amended protocol (V1.1.0)
5. ⬜ Corrected execution script (fix detection-coverage check per stop adjudication; implement amended denominator)
6. ⬜ Single compliant execution
7. ⬜ Independent adjudication

No step may be skipped.

---

## 18. Integrity

- Read-only: YES — no files modified during this preparation
- No execution: CONFIRMED
- No rerun: CONFIRMED
- No scientific result calculation: CONFIRMED
- No PnL: CONFIRMED
- No cost calculation: CONFIRMED
- No protocol modification (V1.0.0 preserved): CONFIRMED
- No Definition Lock modification: CONFIRMED
- No closed-line reopening: CONFIRMED
- Outcome-blind: CONFIRMED

---

*This amendment proposal was prepared as a read-only governance task. The amended protocol is not yet frozen and no execution is authorized.*
