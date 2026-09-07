# QUANTFORGE — ORD V1.1.0 PROTOCOL AMENDMENT

# INDEPENDENT AUDIT V1

*Strictly read-only. No execution; no rerun; no scientific result calculation; no PnL; no cost analysis; no protocol modification; no Definition Lock modification; no closed-line reopening.*

---

## 1. Executive Verdict

**PASS — AMENDMENT APPROVED FOR OWNER REVIEW**

The proposed V1.1.0 amendment is scientifically legitimate, governance-compliant, deterministic, outcome-blind, and genuinely surgical. It changes only the invalid-day anomaly denominator population — narrowing it from "all calendar dates with ≥1 M1 observation" to "dates with ≥1 M1 observation during the market-session detection window." No scientific object, statistical estimator, inference machinery, or classification rule is altered. The Definition Lock, original V1.0.0 protocol, and all execution artifacts remain untouched.

---

## 2. Current Governance State

| Item | Status |
|---|---|
| ORD V1.0.0 | Frozen (SHA `cc01b23c…` verified) |
| Definition Lock V1 | Unchanged (SHA `b5810540…`) |
| Pre-registration audit | PASS — APPROVED FOR EXECUTION |
| V1.0.0 execution | STOPPED (denominator > 10% for all markets) |
| Stop adjudication | CONDITIONAL (17:00 bar = implementation error; denominator = valid) |
| Denominator governance | DETERMINATE — WEEKENDS INCLUDED |
| V1.1.0 amendment proposal | Prepared (SHA `85263b84…` verified) |
| V1.1.0 amendment audit | THIS DOCUMENT |
| Owner approval | PENDING |

---

## 3. Amendment Necessity

The amendment is necessary and correctly characterized:

- **V1.0.0 was not "wrong."** The frozen denominator faithfully implemented its registered definition ("all calendar dates containing ≥ 1 M1 observation"). Weekends with stray data were correctly included.
- **V1.0.0 stopped legitimately.** The >10% fraction was genuine under the frozen rule.
- **V1.1.0 is a deliberate new data-quality population rule.** It narrows the denominator to dates that can participate in the ORD market-session population — dates with observations during the detection window.
- The amendment is **not** a coding-bug fix. The only coding bug (17:00 bar requirement) was separately identified and resolved by the stop adjudication.

---

## 4. Exact Change Audit

### 4.1 Structural Comparison

| Metric | V1.0.0 | V1.1.0 |
|---|---|---|
| Total lines | 216 | 217 |
| Lines added | — | 1 (version history entry) |
| Lines modified | — | 2 (version line, denominator) |
| Sections changed | — | §0, §2, §20 |

### 4.2 Substantive Changes (verified line-by-line)

| Line | V1.0.0 | V1.1.0 | Nature |
|---|---|---|---|
| §0 (line 6) | `Protocol version: V1.0.0` | `Protocol version: V1.1.0` | Version metadata |
| §2 (line 21) | — | `V1.1.0: Denominator amendment (AMEND-DENOM-1)` | Version history addition |
| §20 (line 160) | `all calendar dates containing ≥ 1 M1 observation...` | `dates with ≥ 1 M1 observation within the detection window...` | Denominator definition |

### 4.3 No Other Changes

All other 213+ lines are byte-identical between V1.0.0 and V1.1.0 (accounting for the +1 line shift from the version history addition). Verified by checking that every non-modified line in V1.0.0 appears in V1.1.0.

---

## 5. Scientific Object Preservation

The amended protocol preserves the frozen scientific object exactly:

> Opening range → close-break → entry at breakout close → structural invalidation → post-entry directional movement.

| Element | Changed? | Evidence |
|---|---|---|
| Opening-range definition (§4) | NO | Unchanged text |
| Breakout detection (§5) | NO | Unchanged text |
| Entry price (§6) | NO | Unchanged text |
| Invalidation (§7) | NO | Unchanged text |
| Control event (§10) | NO | Unchanged text |
| Control sign (§10) | NO | Unchanged text |
| Primary response (§8) | NO | Unchanged text |
| Horizon (§9) | NO | Unchanged text |
| ΔM statistic (§12) | NO | Unchanged text |
| Evaluability (§13) | NO | Unchanged text |
| Bootstrap (§14) | NO | Unchanged text |
| Null construction (§15) | NO | Unchanged text |
| p-value formula (§15) | NO | Unchanged text |
| CI construction (§16) | NO | Unchanged text |
| Holm family (§17) | NO | Unchanged text |
| Classification (§18) | NO | Unchanged text |
| Market universe (§3) | NO | XAU/XAG/USATECH/BTC unchanged |
| Definition Lock | NO | Untouched |

---

## 6. Detection Boundary

The amended protocol preserves the V1.0.0 detection-window language:

- §5: "through **17:00:00 ET inclusive**" — boundary, not requirement
- §20: "breakout/penetration detection requires data through 17:00:00 ET (bars may be missing inside the window without automatic failure)"

The denominator amendment does NOT alter the detection-window rule. The denominator uses "the market post-opening-range detection window (after the 30-minute opening window closes through 17:00:00 ET inclusive)" — this references the same boundary that already exists in §5 and §20.

**No hidden 17:00-bar requirement is introduced.** The denominator asks whether observations exist within the window, not whether a bar at exactly 17:00:00 exists. A date with observations through 16:59 ET (within the window) qualifies.

---

## 7. Invalid-Day Denominator

### 7.1 Amended Rule (§20)

> the denominator consists of calendar dates containing >= 1 M1 observation whose timestamp falls within the market post-opening-range detection window (after the 30-minute opening window closes through 17:00:00 ET inclusive) on that date, after timestamp normalization (UTC to America/New_York) and duplicate removal.

### 7.2 Semantic Analysis

| Question | Answer |
|---|---|
| What is the earliest qualifying timestamp? | Opening window close + 1 minute (e.g., 03:30:00 ET for XAU/XAG/BTC) |
| Is the opening-range window itself included? | NO — "after the 30-minute opening window closes" |
| Is the breakout-detection interval inclusive of endpoints? | YES — "through 17:00:00 ET inclusive" |
| Is 17:00 an upper bound only? | YES — consistent with §5 and §20 detection rule |
| Are dates with no detection-window observations excluded? | YES — "does not enter the denominator" |
| Are weekends with stray observations outside the detection window excluded? | YES — observations outside the window don't qualify |
| Are weekends with observations inside the detection window included? | YES — they have qualifying observations |
| Are holidays treated the same as any other date? | YES — observation-driven, no calendar |
| Is a separate exchange holiday calendar introduced? | NO — deterministic, observation-driven |
| Is the rule deterministic across markets? | YES — same rule, different window anchors per §4 |

### 7.3 Denominator Membership Test

A date enters the denominator iff:
1. It has ≥ 1 M1 observation after timestamp normalization and dedup; AND
2. At least one observation's timestamp falls within (opening window close, 17:00:00 ET] on that date.

This is deterministic, outcome-blind, and requires no external data or calendar.

---

## 8. Weekend / Holiday Handling

### 8.1 Weekends

- **Weekends with stray observations outside the detection window** (e.g., Sunday evening open timestamps): excluded from denominator (no observation in detection window).
- **Weekends with observations inside the detection window** (e.g., BTCUSD Saturday trading): included in denominator (has qualifying observations).

This is correct: BTCUSD trades 24/7 and has legitimate detection-window observations on weekends. Gold/silver do not.

### 8.2 Holidays

- **Holidays with no market activity**: no observations in detection window → excluded.
- **Holidays with partial market activity** (e.g., early close): observations in detection window → included.

No exchange holiday calendar is introduced. The rule is purely observation-driven.

### 8.3 Consistency Check

The amended protocol mentions "weekends, holidays, or pre-window hours" only in the denominator context (§20), explaining what "outside the detection window" means. No other section references weekend/holiday handling. The three-way distinction (§20) and event construction (§5, §11) are unchanged.

---

## 9. Statistical Machinery Preservation

| Element | Changed? |
|---|---|
| Bootstrap sampling unit (day clusters) | NO |
| Bootstrap parameters (B=10,000, seed=20260818) | NO |
| Null construction (ΔM*_null = ΔM* − ΔM_obs) | NO |
| p-value formula ((1+count)/(1+B_valid)) | NO |
| CI construction (percentile 2.5/97.5) | NO |
| Holm step-down (α=0.05) | NO |
| Classification rules | NO |
| Evaluability threshold (≥100) | NO |
| Median convention | NO |

The denominator change affects only the anomaly gate. It does not alter which events exist, what their responses are, or how the bootstrap/null/Holm machinery operates.

---

## 10. Outcome-Blindness

### 10.1 Amendment Record Audit

| Outcome Term | Found? | Context |
|---|---|---|
| ΔM values | NO | Not mentioned |
| p-values | YES | §10 list of "unchanged" elements only |
| Confidence intervals | YES | §10 list of "unchanged" elements only |
| Holm values | YES | §10 list of "unchanged" elements only |
| Classification results | YES | §10 list of "unchanged" elements only |
| Event counts | YES | §12 list of "not used" terms only |
| Favorable/unfavorable | NO | Not mentioned |
| Market rankings | NO | Not mentioned |
| Performance | YES | Explicitly stated: "not justified by performance outcomes" |
| V1 execution stop | YES | Referenced as governance history (allowed) |

### 10.2 Verdict

No performance outcome information was used to justify the amendment. The amendment is justified solely by the data-quality population definition. All outcome-related terms appear only in the "unchanged/not used" context.

---

## 11. Historical V1 Preservation

| Check | Result |
|---|---|
| V1.0.0 file untouched | PASS (SHA verified) |
| V1.0.0 SHA recorded | PASS (`cc01b23c…`) |
| V1.0.0 STOP preserved | PASS (execution report, statistics, event table unchanged) |
| V1.0.0 not retroactively labeled invalid | PASS (amendment record states "V1 was not wrong") |
| V1.1.0 clearly successor | PASS (explicit version history, amendment identifier) |

---

## 12. Versioning / Hash Integrity

| Item | SHA-256 | Verified? |
|---|---|---|
| V1.0.0 on-disk | `cc01b23cf213abc906750d7ec1d238089047baa3b6fb9bf0beb733bf1b0649a7` | PASS — matches registered |
| V1.1.0 on-disk | `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06` | PASS — matches recorded |
| Definition Lock | `b58105404d277560eec31a8b08c5b1997b86a03904fc4a804e87beaac448ab30` | PASS — unchanged |
| Original audit | `ebeae5f44dcd0fcaf0512c9dff274008182e39f894f68bdcc5487d1195f1e416` | PASS — unchanged |

Versioning follows H01 precedent (v1.0.0 → v1.1.0 for specification amendments). The amendment identifier (AMEND-DENOM-1) is recorded. No accidental overwrite occurred.

---

## 13. Implementation Determinism

The amended protocol can be implemented deterministically with two changes to the execution script:

1. **Detection-coverage check:** Replace `max(et_min) >= DETECT_END` with `len(det_pos) == 0` (per the stop adjudication's established interpretation).
2. **Denominator construction:** Include only dates with ≥1 M1 observation in the detection window (post-opening through 17:00 ET).

Both changes are deterministic. No new scientific decision is required. No external holiday calendar is needed.

**No other implementation ambiguity remains.** The protocol text fully determines the denominator, the detection window, and the anomaly gate.

---

## 14. Findings Table

| Area | Verdict | Severity | Finding |
|---|---|---|---|
| Amendment necessity | PASS | — | Correctly characterized: deliberate population rule, not a bug fix |
| Versioning | PASS | — | V1.1.0 follows H01 precedent; AMEND-DENOM-1 recorded |
| Exact changes | PASS | — | 3 lines changed (§0, §2, §20); 1 line added; no other changes |
| Scientific object | PASS | — | Opening range → close-break → entry → invalidation → response: unchanged |
| Opening range | PASS | — | §4 unchanged |
| Breakout | PASS | — | §5 unchanged; 17:00 boundary preserved |
| Entry | PASS | — | §6 unchanged |
| Invalidation | PASS | — | §7 unchanged |
| Control | PASS | — | §10 unchanged; sign preserved |
| Primary response | PASS | — | §8 unchanged |
| Detection boundary | PASS | — | 17:00 remains upper bound; no bar-at-17:00 requirement introduced |
| Denominator | PASS | — | Deterministic: observation-driven, detection-window-gated |
| Holiday handling | PASS | — | Observation-driven; no holiday calendar introduced |
| Evaluability | PASS | — | §13 unchanged |
| Bootstrap | PASS | — | §14 unchanged |
| Null | PASS | — | §15 unchanged |
| P-value | PASS | — | §15 unchanged |
| CI | PASS | — | §16 unchanged |
| Holm | PASS | — | §17 unchanged |
| Classification | PASS | — | §18 unchanged |
| Outcome-blindness | PASS | — | No performance outcomes used; amendment justified by population semantics |
| Historical V1 preservation | PASS | — | V1.0.0 untouched; STOP preserved; V1.1.0 is successor |
| Hash integrity | PASS | — | All SHA-256 hashes verified on-disk |
| Implementation determinism | PASS | — | Two script changes needed; both deterministic; no new decisions |
| Scope discipline | PASS | — | Only anomaly denominator changed; no scientific/statistical/inference alteration |

---

## 15. Final Recommendation

**PASS — AMENDMENT APPROVED FOR OWNER REVIEW**

The V1.1.0 amendment is:
- **Scientifically legitimate:** narrows the anomaly denominator to the ORD market-session population
- **Surgical:** only §20 denominator changed; no other section altered
- **Outcome-blind:** no performance outcomes used in justification
- **Deterministic:** observation-driven; no external calendar required
- **Governance-compliant:** follows established amendment chain (stop → adjudication → governance decision → amendment → audit)
- **Compatible with frozen ORD object:** scientific question, events, responses, inference all unchanged
- **Versioned correctly:** V1.1.0 per H01 precedent; AMEND-DENOM-1 identifier recorded

### Required Next Action

> **OWNER / GOVERNANCE APPROVAL OF ORD V1.1.0**

After approval:
1. Freeze V1.1.0 (hash verification)
2. Corrected execution implementation audit (fix detection-coverage check + implement amended denominator)
3. Single compliant execution
4. Independent adjudication

---

## 16. Integrity

- Read-only: YES — no files modified during this audit
- No execution: CONFIRMED
- No rerun: CONFIRMED
- No scientific result calculation: CONFIRMED
- No PnL: CONFIRMED
- No cost analysis: CONFIRMED
- No protocol modification: CONFIRMED (V1.0.0 and V1.1.0 both untouched)
- No Definition Lock modification: CONFIRMED
- No closed-line reopening: CONFIRMED

---

*This audit was produced as an independent, adversarial, read-only review of the proposed ORD V1.1.0 protocol amendment. The amendment is approved for owner review.*
