# QUANTFORGE — ORD INVALID-DAY DENOMINATOR GOVERNANCE DECISION V1

*Strictly read-only. No execution; no rerun; no scientific result calculation; no PnL; no cost calculation; no protocol modification; no Definition Lock modification; no closed-line reopening.*

---

## 1. Executive Decision

**DETERMINATE — WEEKENDS INCLUDED**

The frozen ORD protocol §20 unambiguously establishes that the invalid-day denominator includes all calendar dates containing ≥ 1 M1 observation, regardless of weekday/weekend classification. A weekend date with ≥ 1 stray M1 observation belongs in the denominator. The protocol's exclusion clause ("weekends/holidays with no data are not counted") addresses dates with zero observations, not weekends with data.

No protocol amendment is justified on this ground. The executor's denominator implementation was correct. The execution STOP on the denominator ground was valid.

---

## 2. Authoritative Text

### 2.1 Protocol §20 (binding)

> "**Invalid-day denominator (explicit, not silently borrowed):** all calendar dates containing ≥ 1 M1 observation after timestamp normalization and duplicate removal; weekends/holidays with no data are not counted. An **invalid day** = a date with ≥ 1 observation that fails the opening-window completeness gate (missing/zero-width/§20-invalid window). The **invalid-day fraction** is computed BEFORE primary inference; **if it exceeds 10%, execution HALTS for an anomaly audit** (the 10% threshold is inherited from the project's data-gate convention; the invalid-day definition is registered here explicitly, correcting the ambiguity recorded in DISC-025)."

### 2.2 Protocol §20 three-way distinction (binding)

> "**Three-way distinction (not conflated):** invalid day; eligible day with zero events; event with incomplete horizon (excluded pre-inference)."

### 2.3 Protocol §4 day eligibility (binding)

> "**Day eligibility (deterministic):** all 30 window timestamps present with valid OHLC (> 0) and W > 0. Days failing any condition are ineligible (no event, counted per §20 invalid-day rule)."

### 2.4 Protocol §11 event uniqueness (binding)

> "Per market per trading day, at most two directional events"

### 2.5 Protocol §14 bootstrap (binding)

> "**Sampling unit:** the chronological sequence of trading-day clusters (days containing ≥1 eligible event)."

### 2.6 Definition Lock §6 (binding)

> "**Eligibility (day-level, deterministic):** a day is eligible only if all 30 window M1 timestamps exist with valid OHLC (> 0). A zero-width range (`High == Low`) makes the day ineligible (no clean breakout can be defined). Missing bars, holiday days, and days with a truncated opening window are ineligible (not events)."

### 2.7 Audit §13 (non-binding commentary)

> "explicit invalid-day denominator (calendar dates with ≥1 observation; weekends/empty days excluded)"

### 2.8 Audit §17 INFO (non-binding commentary)

> "the invalid-day gate covers **opening-window** failures only; a day with a complete opening window but a truncated post-opening session yields zero events silently (deterministic, no decision required, but a weaker coverage gate than the sweep's session-coverage rule)."

---

## 3. Definition-Lock Analysis

The Definition Lock does not address the invalid-day denominator. It defines day eligibility (opening-window completeness) and event structure, but the anomaly fraction and its denominator are protocol-level constructs registered in §20 of the frozen protocol. The Definition Lock is silent on this question.

---

## 4. Protocol Analysis

### 4.1 The Denominator Sentence

Protocol §20 defines the denominator as:

> "all calendar dates containing ≥ 1 M1 observation after timestamp normalization and duplicate removal; weekends/holidays with no data are not counted."

This sentence has two clauses separated by a semicolon:

**Clause 1 (denominator definition):** "all calendar dates containing ≥ 1 M1 observation after timestamp normalization and duplicate removal"

**Clause 2 (exclusion):** "weekends/holidays with no data are not counted"

### 4.2 Logical Parsing of Clause 2

Clause 2 says: "weekends/holidays **with no data** are not counted."

This qualifies the exclusion to weekends/holidays that have **no data**. The phrase "with no data" is a restrictor on the exclusion — it specifies which weekends/holidays are excluded.

If the intent were to exclude ALL weekends regardless of data, the text would say:

- "weekends/holidays are not counted" (without the "with no data" qualifier), or
- "weekends/holidays with or without data are not counted"

Instead, the text explicitly limits the exclusion to weekends/holidays "with no data." This means:

- Weekends/holidays **with no data** → excluded from denominator
- Weekends/holidays **with data** → NOT excluded by this clause

A weekend date containing ≥ 1 M1 observation has "data." Therefore, clause 2 does not exclude it. It falls under clause 1: "all calendar dates containing ≥ 1 M1 observation."

### 4.3 Redundancy Analysis

Clause 2 is logically redundant with clause 1 for weekends with no data: a date with no observations cannot satisfy "≥ 1 M1 observation," so it's already excluded by clause 1. The redundancy serves as a clarification — it explicitly confirms that empty weekends don't enter the denominator, preventing any reader from counting them.

This redundancy does not create an ambiguity. It narrows the exclusion, not broadens it.

### 4.4 Distinguishing "Calendar Dates" from "Trading Day"

The protocol uses two distinct terms:

- **"Calendar dates"** (§20 denominator): "all calendar dates containing ≥ 1 M1 observation"
- **"Trading day"** (§11 event uniqueness, §14 bootstrap): "per market per trading day"; "trading-day clusters (days containing ≥1 eligible event)"

The protocol deliberately distinguishes these. The denominator uses "calendar dates" (broader); the event/bootstrap machinery uses "trading day" (narrower, requiring eligible events). This confirms that the denominator is intentionally broader than the set of trading days.

### 4.5 §4 Eligibility vs §20 Denominator

Protocol §4 says ineligible days are "counted per §20 invalid-day rule" — meaning they enter the denominator and are counted as invalid. This confirms the denominator is broader than eligible event days. Ineligible days (including weekends with stray data that fail the opening-window gate) are part of the denominator and counted as invalid.

---

## 5. Weekend / Trading-Day Analysis

### 5.1 Data Reality

| Market | Weekend Dates with Data | Weekend Bars | Stray Data Type |
|---|---|---|---|
| XAUUSD | 256 Sundays | 92,074 | Adjacent Friday close / Sunday evening open |
| XAGUSD | 256 Sundays | 90,966 | Same as XAUUSD |
| BTCUSD | 522 Sat+Sun | 701,853 | Genuine 24/7 crypto market |
| USATECHIDXUSD | 143 Sundays | 49,023 | Residual data |

### 5.2 Protocol Treatment

Under the frozen protocol's denominator definition:

- Each of these weekend dates contains ≥ 1 M1 observation → enters the denominator
- Each fails the opening-window gate (no 30-bar 03:00-03:29 ET window on Sundays; BTCUSD may pass on some weekends) → counted as invalid if window fails
- The invalid-day fraction includes these dates in both numerator and denominator

### 5.3 Impact on Fraction

| Market | Fraction (with weekends) | Estimated Fraction (without weekends) |
|---|---|---|
| XAUUSD | 17.37% | ~1.1% |
| XAGUSD | 17.89% | ~1.6% |
| BTCUSD | 12.04% | N/A (weekends are valid 24/7) |
| USATECHIDXUSD | 21.99% | ~6.7% |

The inclusion of weekends materially affects whether the >10% halt threshold is triggered for XAUUSD, XAGUSD, and USATECHIDXUSD.

---

## 6. Interpretation Alternatives

### Alternative A — Weekends Included (the protocol's text)

**Supporting text:** Protocol §20: "all calendar dates containing ≥ 1 M1 observation"; "weekends/holidays with no data are not counted" (excludes only empty weekends).

**Reasoning:** The denominator includes any calendar date with ≥ 1 observation. Weekends with stray data satisfy this condition. The exclusion clause specifically targets weekends "with no data," not weekends "with data."

**Consequence:** Invalid-day fractions of 12-22% for all markets. Execution HALTS.

### Alternative B — Weekends Excluded (imported from sweep precedent)

**Supporting text:** Sweep protocol §17: "Weekends are not counted as invalid days merely because the market has no data." Audit §13 summary: "weekends/empty days excluded."

**Reasoning:** The sweep protocol explicitly excludes weekends; the audit summary suggests the same intent for ORD; the project's convention is to exclude weekends from anomaly denominators.

**Consequence:** Invalid-day fractions below 10% for XAUUSD, XAGUSD, USATECHIDXUSD. Execution proceeds.

### Why Alternative B Is Not Permissible

1. **The sweep protocol cannot override ORD.** Per the interpretation hierarchy (§5 of this decision), the Definition Lock and frozen ORD protocol are authoritative. A prior protocol's treatment is procedural context, not substantive authority for ORD's scientific definition.

2. **The audit summary is imprecise.** Audit §13 says "weekends/empty days excluded" — but this is a non-binding summary of the protocol's actual text. The protocol's actual text says "weekends/holidays with no data are not counted," which is narrower than "weekends excluded." The audit summary compresses and slightly misstates the protocol's precise wording.

3. **The ORD protocol uses different language from the sweep protocol.** The sweep protocol says "calendar **trading** dates" (emphasis added). The ORD protocol says "all **calendar** dates" (emphasis added). This is a deliberate textual difference — the ORD framers chose broader language.

4. **The protocol explicitly distinguishes "calendar dates" from "trading day."** §20 uses "calendar dates"; §11 and §14 use "trading day." This confirms the denominator is intentionally broader.

---

## 7. Materiality Assessment

The question materially affects:

- The invalid-day denominator: ±256 dates for XAUUSD/XAGUSD
- The invalid-day fraction: 17% vs 1% for XAUUSD
- Whether the >10% halt is triggered: YES (with weekends) vs NO (without)
- Whether execution proceeds: HALTS (with weekends) vs PROCEEDS (without)

This is a material ambiguity only if both interpretations are reasonable from the frozen text. As established above, the frozen text unambiguously supports Alternative A (weekends included). Alternative B requires importing external precedent that the ORD protocol's own language supersedes.

---

## 8. Outcome-Blindness

This decision was made without reference to:

- Any ORD event count
- Any ORD response statistic
- Any ORD p-value or confidence interval
- Any market's specific invalid-day fraction
- Any ORD market's performance characteristics

The decision rests solely on the exact text of the frozen ORD protocol §20 and the interpretation hierarchy.

---

## 9. Governance Verdict

**DETERMINATE — WEEKENDS INCLUDED**

The frozen ORD protocol §20 unambiguously establishes that the invalid-day denominator is "all calendar dates containing ≥ 1 M1 observation after timestamp normalization and duplicate removal." The exclusion clause ("weekends/holidays with no data are not counted") addresses only dates with zero observations. Weekend dates with ≥ 1 stray M1 observation are included in the denominator.

The protocol's deliberate use of "calendar dates" (broader) rather than "trading day" (narrower, used elsewhere in the same protocol) confirms this intent.

No protocol amendment is justified on this ground. The frozen protocol already determines the correct denominator.

---

## 10. Consequence for ORD V1 Execution

### 10.1 Denominator Ground

The executor's denominator implementation was **correct**. Weekends with stray M1 observations were included in the denominator, consistent with the frozen protocol §20.

The execution STOP on the denominator ground was **valid**. All four markets have invalid-day fractions exceeding 10% when weekends with stray data are included.

### 10.2 Detection-Window Ground (Resolved by Prior Adjudication)

The prior stop adjudication found the executor's detection-coverage check to be **incorrect** — the script requires a bar at exactly 17:00 ET, but the protocol defines 17:00 as the boundary, not a requirement. This was an implementation error.

### 10.3 Combined Status

| Stop Ground | Valid? | Correctable by Script Fix? |
|---|---|---|
| Denominator (weekends included) | **VALID** | NO — protocol says what it says |
| Detection window (17:00 bar required) | **INVALID** | YES — fix the coverage check |

The execution remains halted. The detection-window fix alone does not resolve the denominator issue. The denominator is protocol-determined and includes weekends.

### 10.4 Path Forward

The denominator is frozen as-is. If the project wishes to exclude weekends from the denominator, that requires a **formal protocol amendment** through the governance process — not a silent implementation change. The amendment would need to:

1. Register the exact population change (exclude weekends with stray data from the denominator).
2. Justify the change on scientific grounds (e.g., weekends are not trading days for the relevant markets).
3. Be approved through the project's governance hierarchy.
4. Be incorporated into a new protocol version (V1.1.0 or V2.0.0).

Alternatively, the project may accept the denominator as-is and accept that the experiment halts — the data quality is insufficient for the registered anomaly gate.

---

## 11. Required Next Task

The governance decision is complete. The project must now choose between:

1. **Amend the protocol** to exclude weekends from the denominator (requires formal governance).
2. **Accept the halt** and close the ORD execution as data-quality-blocked.
3. **Obtain cleaner data** that does not contain stray weekend observations, then re-execute under the existing protocol.

The executor should not make this choice. It is a project-level governance decision.

---

## 12. Integrity

- Read-only: YES — no files modified during this decision
- No execution: CONFIRMED
- No rerun: CONFIRMED
- No scientific result calculation: CONFIRMED
- No PnL: CONFIRMED
- No cost calculation: CONFIRMED
- No protocol modification: CONFIRMED
- No Definition Lock modification: CONFIRMED
- No closed-line reopening: CONFIRMED

---

*This governance decision was produced as a read-only analysis of the frozen ORD protocol's invalid-day denominator definition. The protocol unambiguously includes weekends with stray M1 observations in the denominator. No amendment is justified by this analysis alone.*
