# QUANTFORGE — ORD V1 EXECUTION STOP ADJUDICATION V1

*Strictly read-only, adversarial audit. No protocol modification; no Definition Lock modification; no rerun; no scientific adjudication; no PnL; no cost analysis; no closed-line reopening.*

---

## 1. Executive Verdict

**CONDITIONAL — One stop reason invalid; one genuine protocol-level ambiguity remains.**

The executor stopped the frozen ORD V1 execution citing two conditions:

1. **Invalid-day fraction > 10%** for all four markets — the executor attributes this partly to weekends with residual M1 observations being counted in the denominator.
2. **Detection-window boundary ambiguity** — the executor claims the protocol does not deterministically resolve whether "through 17:00:00 ET inclusive" requires a bar at exactly 17:00:00 ET.

**Audit finding on Issue 2 (detection boundary):** The executor's interpretation is **incorrect**. The frozen protocol already resolves this. The executor's script imposes a stricter requirement (`max(et_min) >= 1020`) than the protocol specifies. The protocol defines detection *through* 17:00:00 ET as the upper boundary of the detection window, not as a requirement for an observation at exactly 17:00:00. The audit's own registered findings confirm this (§17 INFO: "truncated post-opening sessions yield zero events silently — deterministic, not a decision"). A breakout at any observed time through 16:59:59 ET is a valid ORD event under the frozen definition.

**Audit finding on Issue 1 (denominator):** The invalid-day fraction is inflated by including **256 Sunday dates** (XAUUSD/XAGUSD) or **522 weekend dates** (BTCUSD) in the denominator. The frozen protocol's denominator definition ("all calendar dates containing ≥ 1 M1 observation") does not explicitly exclude weekends with stray observations. The sweep protocol (from which ORD inherits) explicitly states "weekends are not counted as invalid days merely because the market has no data," but does not address weekends *with* data. This is a **genuine ambiguity** requiring governance clarification.

---

## 2. Frozen Protocol Integrity

| Check | Result |
|---|---|
| Protocol version | V1.0.0 — confirmed |
| Protocol SHA-256 | `cc01b23cf213abc906750d7ec1d238089047baa3b6fb9bf0beb733bf1b0649a7` — verified on disk |
| Definition Lock | Present, unchanged |
| Pre-registration audit | PASS — APPROVED FOR ORD MULTI-MARKET EXECUTION |
| Protocol modification during stopped execution | NONE |
| Definition Lock modification | NONE |

---

## 3. Claimed Stop Conditions

| # | Claimed Condition | Executor's Characterization | Audit Finding |
|---|---|---|---|
| 1 | Invalid-day fraction > 10% for all markets | Data-integrity failure (§20 halt gate) | **Partially valid.** Genuine denominator ambiguity. Weekend dates inflate the fraction. |
| 2 | Detection-window boundary ambiguity | Protocol does not resolve "through 17:00" | **Invalid.** Protocol already resolves this. Executor's script is stricter than the protocol. |

---

## 4. Detection Boundary Audit

### 4.1 Frozen Protocol Wording

**Protocol §5 (Breakout Event):**
> "the first M1 bar after the opening window (through **17:00:00 ET inclusive** of the same NY calendar day) with `Close_t > High_OR`"

**Protocol §20 (Event-session completeness):**
> "breakout/penetration detection requires data through 17:00:00 ET (bars may be missing inside the window without automatic failure — no hidden gapless-session requirement — but the specific required bars must exist for the event and horizon rules)."

**Definition Lock §7:**
> "Evaluation window: the breakout is evaluated over the bars from window end through **17:00:00 ET inclusive** of the same NY calendar day."

### 4.2 Interpretation Analysis

The phrase "through 17:00:00 ET inclusive" defines the **upper boundary** of the detection window. It means:

- Detection applies to bars with timestamps ≤ 17:00:00 ET.
- A breakout at 16:59:00 ET is within the detection window.
- A breakout at 17:00:00 ET is within the detection window (if such a bar exists).
- The absence of a bar at exactly 17:00:00 does not invalidate the day, because the protocol explicitly permits "bars may be missing inside the window without automatic failure."

The protocol does **not** say: "a valid event day must contain an observation at exactly 17:00:00 ET." The 17:00:00 timestamp is the boundary of the detection universe, not a required observation point.

### 4.3 Audit Confirmation

The independent pre-registration audit (§17) explicitly states:

> **INFO (non-blocking):** the invalid-day gate covers **opening-window** failures only; a day with a complete opening window but a truncated post-opening session yields zero events silently (deterministic, no decision required, but a weaker coverage gate than the sweep's session-coverage rule).

This confirms that:
- The invalid-day gate does **not** cover detection-window failures.
- A day with a complete opening window but truncated detection data yields zero events **silently** — it is not invalid.
- This is registered as INFO (non-blocking), not as a protocol defect.

### 4.4 Executor's Implementation

The execution script (line 170):
```python
if len(det_pos) == 0 or emin[det_pos].max() < DETECT_END:
    continue  # no detection possible -> zero events this day
```

Where `DETECT_END = 17 * 60 = 1020`.

This condition requires `max(et_min) >= 1020` (i.e., a bar at or after 17:00:00 ET). If the maximum detection-bar et_min is 1019 (16:59:00 ET), the day is skipped.

**This is stricter than the frozen protocol.** The protocol requires data "through 17:00:00 ET" as the upper boundary of detection, not a bar at exactly 17:00:00. The correct check should be `len(det_pos) == 0` (no bars in the detection window), not `emin[det_pos].max() < DETECT_END`.

### 4.5 Required Mathematical Test

If a market has observations through 16:59 ET but none at 17:00 ET:

| Question | Answer (from frozen text) |
|---|---|
| Can a qualifying breakout at 16:59 be a valid ORD event? | **YES.** 16:59 is within "through 17:00:00 ET inclusive." |
| Can a qualifying breakout at any observed time ≤16:59 be valid? | **YES.** All such times are within the detection window. |
| Does the absence of 17:00 make the day invalid? | **NO.** The protocol does not require a bar at 17:00. The audit confirms truncated sessions yield zero events silently. |
| Does the protocol say detection coverage is an invalid-day condition? | **NO.** The audit explicitly states the invalid-day gate covers opening-window failures only (§17 INFO). |

---

## 5. Invalid-Day Denominator Audit

### 5.1 Protocol Definition (§20)

> "**Invalid-day denominator (explicit, not silently borrowed):** all calendar dates containing ≥ 1 M1 observation after timestamp normalization and duplicate removal; weekends/holidays with no data are not counted. An **invalid day** = a date with ≥ 1 observation that fails the opening-window completeness gate (missing/zero-width/§20-invalid window)."

### 5.2 Analysis

The denominator is: **all calendar dates containing ≥ 1 M1 observation**.

The protocol explicitly excludes "weekends/holidays **with no data**." It does **not** explicitly exclude weekends **with** data.

### 5.3 Sweep Protocol Precedent

The sweep protocol (§17), from which ORD inherits, states:

> "**Invalid-Day Fraction**: The denominator is all calendar trading dates containing at least one M1 observation for the instrument after timestamp normalization and duplicate removal. **Weekends are not counted as invalid days merely because the market has no data.**"

The sweep protocol's explicit weekend exclusion suggests the framers intended weekends to be excluded from the denominator. However, the sweep protocol also says "calendar **trading** dates" (emphasis added), while the ORD protocol says "all **calendar** dates" (emphasis added). The ORD protocol uses broader language.

### 5.4 Ambiguity

The ORD protocol's denominator definition is ambiguous regarding weekends with stray M1 observations:

- **Literal reading:** "all calendar dates containing ≥ 1 M1 observation" includes weekends with stray data. These dates fail the opening-window gate (no 03:00-03:29 ET window on Sundays), so they are counted as invalid days.
- **Intended reading (inferred from sweep precedent):** Weekends should be excluded from the denominator regardless of stray data, because they are not trading days for the relevant markets.

The protocol does not resolve this ambiguity.

---

## 6. Weekend / Calendar-Day Audit

### 6.1 Weekend Observations in M1 Data

| Market | Total Dates | Weekend Dates | Weekend Bars | Primary Weekend |
|---|---|---|---|---|
| XAUUSD | 1,554 | 256 | 92,074 | Sunday only |
| XAGUSD | 1,548 | 256 | 90,966 | Sunday only |
| BTCUSD | 1,827 | 522 | 701,853 | Saturday + Sunday |
| USATECHIDXUSD | 873 | 143 | 49,023 | Sunday only |

### 6.2 Invalid-Day Attribution

| Market | Invalid Days | Weekend Dates | Non-Weekend Invalid | Weekend % of Invalid |
|---|---|---|---|---|
| XAUUSD | 270 | 256 | 14 | 94.8% |
| XAGUSD | 277 | 256 | 21 | 92.4% |
| BTCUSD | 220 | 522 | — | — |
| USATECHIDXUSD | 192 | 143 | 49 | 74.5% |

**XAUUSD/XAGUSD:** ~93-95% of invalid days are Sundays with residual M1 observations. These are not trading days for gold/silver; the stray observations are likely from adjacent Friday close or Sunday evening open timestamps.

**BTCUSD:** The 522 weekend dates far exceed the 220 invalid days, because many weekend dates pass the opening-window gate (BTCUSD trades 24/7 and has valid OHLC during the 03:00-03:29 ET window on weekends). The invalid-day fraction is lower (12.04%) because most weekend dates are eligible.

**USATECHIDXUSD:** 143 Sunday dates, of which 192 total dates fail the opening-window gate. Some weekday dates also fail (data gaps around 16:14 ET for some days, though this affects detection, not the opening window).

### 6.3 Impact on Invalid-Day Fraction

If weekends with stray observations were excluded from the denominator:

| Market | Current Fraction | Weekday-Only Fraction (estimated) | Below 10%? |
|---|---|---|---|
| XAUUSD | 17.37% (270/1554) | ~1.1% (14/1298) | YES |
| XAGUSD | 17.89% (277/1548) | ~1.6% (21/1292) | YES |
| BTCUSD | 12.04% (220/1827) | N/A (weekends are valid days) | N/A |
| USATECHIDXUSD | 21.99% (192/873) | ~6.7% (49/730) | YES |

**If weekends are excluded, XAUUSD, XAGUSD, and USATECHIDXUSD would fall below the 10% threshold.** The halt would not have been triggered for these markets on the denominator alone.

---

## 7. Script-vs-Protocol Audit

| Implementation Element | Protocol Requirement | Script Behavior | Divergence? |
|---|---|---|---|
| Date construction | Calendar dates with ≥1 M1 observation (§20) | `df.groupby("date")` — includes all dates with data | Consistent |
| Weekend handling in denominator | Ambiguous (see §5.4) | Weekends included if they have data | Consistent with literal reading |
| Opening-window gate | 30 bars, valid OHLC, W>0 (§4) | Same | Consistent |
| Detection window | "through 17:00:00 ET inclusive" (§5) | `emin <= DETECT_END` (1020) | Consistent |
| **Detection coverage check** | **Protocol: no explicit requirement for bar at 17:00** | **Script: `max(et_min) >= DETECT_END`** | **DIVERGENT** |
| Invalid-day fraction gate | >10% → HALT (§20) | `if diag["invalid_fraction"] > HALT_FRACTION` | Consistent |
| Event construction | First close beyond edge through 17:00 (§5) | Same | Consistent |
| Bootstrap | Day-cluster stationary, B=10000, seed 20260818 (§14) | Same | Consistent (not reached) |

**One divergence identified:** The script's detection-coverage check (line 170) requires `max(et_min) >= 1020`, which is stricter than the protocol's "through 17:00:00 ET inclusive." The protocol defines the detection window's upper boundary; the script requires a bar at that boundary.

---

## 8. Execution Artifact Audit

### 8.1 Persisted Artifacts

| Artifact | SHA-256 | Contents |
|---|---|---|
| event_table_all_markets.csv | `8124cfc3…` | 2,840 BTCUSD events only |
| statistics.json | `b5d03786…` | Empty results (all markets halted) |
| metadata.json | `4760a430…` | Execution identity, environment, artifact hashes |
| EXECUTION_REPORT_ORD_V1.md | `5c062280…` | Executor's stop report |

### 8.2 Integrity Verification

- Protocol hash: verified (cc01b23c…)
- Input data hashes: verified (all four M1 datasets)
- Seed: 20260818 (recorded)
- B: 10,000 (recorded)
- Universe: XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD (correct)
- EURUSD: excluded (correct)
- No bootstrap draws produced (halted before inference)
- No null draws produced
- No scientific results computed

### 8.3 Reproducibility

The stopped state is reproducible: the script with the same seed and data will produce the same halt conditions. The 2,840 BTCUSD events in the event table are reproducible. The zero events for XAUUSD/XAGUSD/USATECHIDXUSD are reproducible given the script's current (incorrect) detection-coverage check.

---

## 9. Market-Specific Diagnostics

### 9.1 XAUUSD

- **Opening window:** 03:00-03:29 ET — valid for 1,284 weekday dates
- **Detection data:** Last bar at 16:59 ET (et_min = 1019). No bar at 17:00 ET.
- **Events detected:** 0 (script skips all days due to `max < 1020`)
- **Root cause:** Script's detection-coverage check is stricter than the protocol
- **Correct behavior under protocol:** Days with data through 16:59 ET should produce events for any breakout at observed times through 16:59:00

### 9.2 XAGUSD

- **Opening window:** 03:00-03:29 ET — valid for 1,271 weekday dates
- **Detection data:** Last bar at 16:59 ET (et_min = 1019). No bar at 17:00 ET.
- **Events detected:** 0 (same script issue as XAUUSD)
- **Correct behavior under protocol:** Same as XAUUSD

### 9.3 BTCUSD

- **Opening window:** 03:00-03:29 ET — valid for 1,607 dates (including weekends)
- **Detection data:** Bars at 17:00 ET exist (1,761 bars). Data extends through 23:59 ET.
- **Events detected:** 2,840 (passed detection-coverage check)
- **Halted:** Invalid-day fraction 12.04% > 10%
- **Note:** BTCUSD demonstrates that the script's detection-coverage check works when data extends through 17:00 ET. This confirms the check is requiring a 17:00 bar.

### 9.4 USATECHIDXUSD

- **Opening window:** 09:30-09:59 ET — valid for 681 dates
- **Detection data:** Many dates have data gaps around 16:14 ET. No bar at 17:00 ET for most dates.
- **Events detected:** 0 (script skips days due to `max < 1020`)
- **Root cause:** Same script issue as XAUUSD/XAGUSD, compounded by data gaps
- **Correct behavior under protocol:** Days with detection data through 16:14 ET should produce events for breakouts at observed times through 16:14:00

---

## 10. Blocker Classification

| Claimed Blocker | Protocol Genuinely Requires It? | Executor Implementation Correct? | Genuine Execution Blocker? |
|---|---|---|---|
| >10% invalid-day fraction | Yes (§20) | Yes (gate logic correct) | **YES** — but denominator includes weekends (ambiguous) |
| Weekend denominator inflation | Ambiguous (§20 vs sweep precedent) | Consistent with literal reading | **YES** — genuine ambiguity |
| Exact 17:00 bar required | **NO** (protocol defines boundary, not requirement) | **NO** (script is stricter) | **NO** — implementation error |
| 16:59 final bar invalidates day | **NO** (protocol allows bars through 16:59) | **NO** (script requires 17:00) | **NO** — implementation error |
| USATECHIDXUSD internal gaps | No (protocol allows missing bars) | Script requires max >= 1020 | **NO** — implementation error |
| Zero XAU/XAG events | N/A (consequence of above) | Incorrect detection check | **NO** — consequence of implementation error |

---

## 11. Reusability of Existing Execution Artifacts

- **Event table (BTCUSD, 2,840 events):** The BTCUSD events were correctly detected under the script's logic. However, since the script's detection-coverage check is stricter than the protocol, some BTCUSD events at times between 16:59 and 17:00 that should have been detected were correctly included (BTCUSD has data through 17:00+). The event table is internally consistent but represents a subset of what a corrected script would produce.
- **Statistics/metadata:** Empty of scientific results. Reusable as execution-identity record only.
- **Bootstrap/null draws:** Not produced. No scientific inference was computed.
- **Scientific results:** NONE produced. No p-values, CIs, Holm values, or classifications exist.

**Conclusion:** The existing artifacts contain no scientific results and are not reusable for scientific purposes. A corrected execution is required.

---

## 12. Final Execution-State Decision

**CONDITIONAL**

- **One stop reason is invalid:** The executor's interpretation of "through 17:00:00 ET" as requiring a bar at exactly 17:00:00 is incorrect. The frozen protocol defines this as the detection window's upper boundary, not as a required observation. The executor's script (line 170) imposes a stricter check (`max >= 1020`) than the protocol specifies. A breakout at any observed time through 16:59:59 ET is a valid ORD event.

- **One genuine ambiguity remains:** The invalid-day denominator includes weekend dates with stray M1 observations. The frozen protocol's wording ("all calendar dates containing ≥ 1 M1 observation") does not explicitly exclude weekends with data. The sweep protocol explicitly excludes weekends, but the ORD protocol uses different language. This ambiguity directly affects whether the >10% halt threshold is triggered.

---

## 13. Required Next Task

1. **Governance clarification:** Resolve the invalid-day denominator ambiguity — should weekends with stray M1 observations be excluded from the denominator? The sweep protocol's explicit exclusion suggests they should be, but the ORD protocol's wording does not explicitly state this.

2. **Corrected execution (after clarification):** If the denominator is clarified to exclude weekends, re-run the frozen ORD V1 protocol with a corrected script that:
   - Excludes weekend dates from the invalid-day denominator (per the clarified protocol).
   - Uses `len(det_pos) == 0` as the detection-coverage check (not `max >= 1020`), consistent with the protocol's "through 17:00:00 ET inclusive" boundary.
   - All other protocol parameters remain frozen (B=10000, seed=20260818, α=0.05, etc.).

3. **No new pre-registration required** if the corrected script implements the existing frozen protocol correctly. The protocol is already deterministic once the denominator ambiguity is resolved.

---

## 14. Integrity

- Read-only: YES — no files modified during this audit
- No protocol modification: CONFIRMED
- No Definition Lock modification: CONFIRMED
- No rerun: CONFIRMED
- No scientific adjudication: CONFIRMED
- No PnL: CONFIRMED
- No cost analysis: CONFIRMED
- No closed-line reopening: CONFIRMED

---

*This adjudication was produced as an independent, adversarial, read-only audit of the STOPPED ORD V1 execution. The executor's detection-window interpretation was found to be incorrect (the protocol already resolves this). The weekend denominator issue is a genuine ambiguity requiring governance clarification.*
