# QUANTFORGE — ORD V1.1.0 EXECUTION IMPLEMENTATION

# INDEPENDENT CLEARANCE AUDIT V1

*Strictly read-only. No execution; no rerun; no scientific result calculation; no PnL; no cost analysis; no protocol modification; no Definition Lock modification; no closed-line reopening.*

---

## 1. Executive Verdict

**CONDITIONAL PASS — DETERMINISTIC CORRECTIONS REQUIRED**

The execution implementation (`scripts/run_ord_v1.py`) contains **two deterministic defects** that must be corrected before V1.1.0 execution:

1. **Detection boundary (line 170):** The script requires `max(et_min) >= 1020` (a bar at or after 17:00 ET), which is stricter than the frozen V1.1.0 protocol. The protocol defines 17:00 ET as an upper boundary, not a required observation.
2. **Invalid-day denominator (lines 139-144, 276-278):** The script uses the V1.0.0 denominator (all calendar dates with ≥1 M1 observation) instead of the V1.1.0 denominator (dates with ≥1 observation in the detection window).

Both corrections are uniquely dictated by the frozen V1.1.0 protocol text and require no new scientific or statistical decision. All other implementation elements are faithful to the frozen protocol.

---

## 2. Frozen Protocol Identity

| Item | Value |
|---|---|
| Protocol version | V1.1.0 |
| SHA-256 | `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06` |
| Amendment | AMEND-DENOM-1 (§20 denominator) |
| Owner approved | YES |

---

## 3. Implementation Identity

| Item | Value |
|---|---|
| Script | `scripts/run_ord_v1.py` |
| Protocol reference (line 39) | V1.0.0 (`cc01b23c…`) — **needs update to V1.1.0** |
| Protocol path (line 39) | `ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1.md` — **needs update to V1_AMENDED** |
| Seed | 20260818 |
| B | 10,000 |
| Markets | XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD |
| EURUSD | Excluded |

---

## 4. Detection Boundary Audit

### 4.1 Protocol Requirement (V1.1.0 §5, §20)

> Detection runs through `17:00:00 ET inclusive` as an upper timestamp boundary.

> A 17:00 bar does NOT need to exist.

### 4.2 Implementation (line 170)

```python
if len(det_pos) == 0 or emin[det_pos].max() < DETECT_END:
    continue  # no detection possible -> zero events this day
```

Where `DETECT_END = 17 * 60 = 1020`.

**Defect:** This requires `max(et_min) >= 1020` (a bar at or after 17:00:00 ET). If the last detection-window bar is at 16:59 ET (et_min = 1019), the day is skipped — even though 16:59 is within the detection window.

**Correct behavior per V1.1.0:** The check should be `len(det_pos) == 0` only. If any bars exist in the detection window (et_min > win_end and et_min <= 1020), the day is eligible for event detection.

**Severity:** CRITICAL — This is the same defect identified by the V1.0.0 stop adjudication.

### 4.3 Required Correction

Replace line 170:
```python
if len(det_pos) == 0 or emin[det_pos].max() < DETECT_END:
```
with:
```python
if len(det_pos) == 0:
```

This is a deterministic correction uniquely dictated by the frozen V1.1.0 protocol.

---

## 5. V1.1 Denominator Audit

### 5.1 Protocol Requirement (V1.1.0 §20)

> the denominator consists of calendar dates containing >= 1 M1 observation whose timestamp falls within the market post-opening-range detection window (after the 30-minute opening window closes through 17:00:00 ET inclusive)

### 5.2 Implementation (lines 139-144, 276-278)

```python
# In build_events:
g = df.groupby("date", sort=True)
for date, grp in g:
    n_total_dates += 1
    ...
    if not win_ok:
        n_invalid_days += 1
        continue

# In main:
diag = {
    "total_dates": n_total_dates,
    "invalid_days": n_invalid_days,
    "invalid_fraction": (n_invalid_days / n_total_dates) if n_total_dates else 0.0,
}
```

**Defect:** `n_total_dates` counts ALL calendar dates with any M1 observation (including weekends with stray data outside the detection window). The V1.1.0 denominator should only count dates with at least one observation in the detection window.

**Correct behavior per V1.1.0:** The denominator should be constructed by checking whether each date has ≥1 M1 observation with `et_min > win_end` (after the opening window). Dates with observations only outside the detection window (e.g., Sunday evening timestamps) should not enter the denominator.

**Severity:** CRITICAL — This is the defect that motivated the V1.1.0 amendment.

### 5.3 Required Correction

The denominator construction must be changed to:
1. For each date, check if any observation falls within `(win_end, DETECT_END]` (the detection window).
2. Only dates with ≥1 detection-window observation enter the denominator.
3. An invalid day is a denominator date that fails the opening-window gate.

This is a deterministic correction uniquely dictated by the frozen V1.1.0 protocol.

---

## 6. Scientific Object

### 6.1 Protocol Requirement

> Opening range → close-break → entry at breakout close → structural invalidation → post-entry directional movement.

### 6.2 Implementation Verification

| Element | Implemented? | Correct? |
|---|---|---|
| Opening range (30-min, §4) | YES | Correct (lines 148-165) |
| Breakout (strict close beyond edge, §5) | YES | Correct (lines 175-189) |
| Entry (breakout-candle close, §6) | YES | Correct (line 200) |
| Invalidation (close back through edge, §7) | YES | Correct (lines 235-244) |
| Control (penetration without close-break, §10) | YES | Correct (lines 175-189) |
| Control sign (attempt direction, §10) | YES | Correct (continuation-direction) |
| Primary response (bp from entry, §8) | YES | Correct (lines 218-222) |
| Horizon (120 min, complete required, §9) | YES | Correct (lines 210-215) |

**Verdict:** PASS — Scientific object faithfully implemented.

---

## 7. Event Construction

| Check | Result |
|---|---|
| First long per day | YES (line 177: `long_break_rows[0]`) |
| First short per day | YES (line 186: `short_break_rows[0]`) |
| Max 2 events/day | YES (long + short, independently) |
| Failed break doesn't reset | YES (first-per-direction, not first-per-attempt) |
| Same-day coupling | YES (both events on same `date`) |
| Strict inequality (close > High_OR) | YES (line 175: `dc > hi_or`) |
| Touching excluded | YES (strict >, not >=) |
| No ATR/tick filter | YES (none in code) |
| No confirmation delay | YES (event = entry) |

**Verdict:** PASS — Event construction faithful.

---

## 8. Control / Response

| Check | Result |
|---|---|
| Control = penetration without close-break | YES |
| First penetration bar used | YES |
| Control anchor = penetration close | YES |
| Same 120-min horizon for control | YES |
| Continuation-direction sign | YES |
| Primary response unconditional | YES (response not truncated by invalidation) |
| MFE not substituted | YES (MFE computed but not used for primary) |
| Entry = breakout close (not next-bar) | YES (line 200) |

**Verdict:** PASS — Control and response faithful.

---

## 9. Statistical Machinery

### 9.1 Bootstrap

| Check | Result |
|---|---|
| Day-cluster sampling | YES (line 353: `day_order`, `day_idx`) |
| Fixed N | YES (line 354: `N = len(day_order)`) |
| Geometric block length p=0.1 | YES (line 310: `rng.geometric(0.1, ...)`) |
| Uniform block start | YES (line 311: `rng.integers(0, N, ...)`) |
| Chronological continuation | YES (line 320: `(sl[:, None] + off) % N`) |
| Circular wrap | YES (modulo N) |
| Truncate to N | YES (line 322: `[:N]`) |
| Events duplicated with day | YES (whole-day resampling) |
| Treatment/control flatten after resampling | YES (lines 323-324) |
| Invalid-replicate rule (≥1 finite T + ≥1 finite C) | YES (lines 325-328) |
| B = 10,000 | YES (line 310: `B * blocks_est`) |
| Seed = 20260818 | YES (line 432: `SEED`) |

### 9.2 Null

| Check | Result |
|---|---|
| ΔM*_null = ΔM* − ΔM_obs | YES (line 411: `null_draws = valid_draws - dm_obs`) |
| count = #{b : \|ΔM*_null\| ≥ \|ΔM_obs\|} | YES (line 412: `np.abs(null_draws) >= abs(dm_obs)`) |
| p = (1+count)/(1+B_valid) | YES (line 413) |
| Inclusive ≥ | YES (>= in line 412) |
| No zero p-values | YES (formula prevents it) |

### 9.3 CI

| Check | Result |
|---|---|
| Percentile 2.5/97.5 | YES (line 414) |
| Of ΔM* distribution (not null) | YES (`valid_draws`, not `null_draws`) |
| No studentization | YES |

### 9.4 Holm

| Check | Result |
|---|---|
| Eligible-market family | YES (line 448: `fam = [m for m, r in market_results.items() if not r.get("halted") and r.get("evaluable")]`) |
| Step-down | YES (lines 451-454) |
| α = 0.05 | YES (line 456: `ph < ALPHA`) |
| Evidence-limited no Holm verdict | YES (line 462: `r["classification"] = "EVIDENCE-LIMITED"`) |

### 9.5 Classification

| Check | Result |
|---|---|
| SUPPORT: Holm p < 0.05 AND ΔM > 0 | YES (line 457) |
| CONTRADICTED: Holm p < 0.05 AND ΔM < 0 | YES (line 459) |
| INCONCLUSIVE: otherwise | YES (line 461) |
| EVIDENCE-LIMITED: <100 treatment | YES (line 462) |

**Verdict:** PASS — Statistical machinery faithful.

---

## 10. Data Gates

| Gate | Implemented? | Correct per V1.1.0? |
|---|---|---|
| UTC → ET conversion | YES (line 119) | YES |
| Duplicate removal (keep-first) | YES (line 120) | YES |
| Invalid OHLC (≤0) | YES (line 158) | YES |
| Opening-window completeness (30 bars) | YES (line 151) | YES |
| Detection-window coverage | YES (line 170) | **NO — requires 17:00 bar** |
| Horizon completeness (120 min) | YES (line 213) | YES |
| Anomaly denominator (>10% halt) | YES (line 382) | **NO — uses V1.0.0 denominator** |
| Three-way distinction | YES | YES |

**Verdict:** CONDITIONAL — Two data-gate implementations need deterministic correction.

---

## 11. Reproducibility

| Requirement | Implemented? |
|---|---|
| Protocol SHA | YES (line 41, but references V1.0.0) |
| Input hashes | YES (lines 46-51) |
| Environment info | YES (lines 357-367) |
| Parameter manifest | YES (in env_info) |
| Event tables (CSV) | YES (lines 467-476) |
| Bootstrap draws | YES (line 438: `np.save`) |
| Null draws | YES (lines 440-442: `np.save`) |
| Observed statistics | YES (in statistics.json) |
| p-values, CIs, Holm | YES (in statistics.json) |
| Classifications | YES (in statistics.json) |
| Metadata JSON | YES (lines 479-494) |
| Execution report | NOT in script (produced separately) |

**Verdict:** PASS — Reproducibility infrastructure is complete. Protocol reference needs update to V1.1.0.

---

## 12. Determinism

| Check | Result |
|---|---|
| Fixed seed (20260818) | YES |
| No wall-clock in scientific calc | YES (wall clock only in metadata timestamps) |
| Sorted chronological inputs | YES (line 120: `sort_values("ts")`) |
| Stable grouping | YES (`groupby("date", sort=True)`) |
| np.median convention | YES (matches frozen definition) |
| np.searchsorted for horizon | YES (deterministic) |
| UTC→ET via zoneinfo | YES (deterministic, DST-aware) |

**Verdict:** PASS — Implementation is deterministic.

---

## 13. Closed-Line Independence

| Check | Result |
|---|---|
| No Mean Reversion imports | YES (none) |
| No TSMOM imports | YES (none) |
| No Session Range Expansion imports | YES (none) |
| No Liquidity Sweep imports | YES (none) |
| No detector semantics | YES (none) |
| Independent event construction | YES |

**Verdict:** PASS — ORD remains independent.

---

## 14. Findings Table

| Area | Verdict | Severity | Finding |
|---|---|---|---|
| Protocol identity | CONDITIONAL | MODERATE | Script references V1.0.0 SHA/path; needs update to V1.1.0 |
| Script identity | PASS | — | `run_ord_v1.py` identified correctly |
| Detection boundary | **FAIL** | **CRITICAL** | Line 170 requires `max(et_min) >= 1020` (17:00 bar); V1.1.0 says 17:00 is upper boundary only |
| V1.1 denominator | **FAIL** | **CRITICAL** | Lines 139-144 count all calendar dates; V1.1.0 requires detection-window-gated dates |
| Weekend handling | **FAIL** | **CRITICAL** | Consequence of denominator defect: weekends with stray data incorrectly included |
| Holiday handling | PASS | — | Observation-driven (no calendar), but denominator gate needed |
| Scientific object | PASS | — | Opening range → close-break → entry → invalidation → response: correct |
| Universe | PASS | — | XAU/XAG/USATECH/BTC; EURUSD excluded |
| Opening range | PASS | — | 30-min windows, correct anchors, 30-bar check |
| Breakout | PASS | — | Strict close-beyond-edge, first per direction per day |
| Entry | PASS | — | Breakout-candle close |
| Invalidation | PASS | — | Close back through edge, response unconditional |
| Control | PASS | — | Penetration without close-break, continuation-direction sign |
| Primary response | PASS | — | bp from entry close, 120-min horizon, complete required |
| Event uniqueness | PASS | — | ≤2/day, first per direction, day coupling |
| Evaluability | PASS | — | ≥100 treatment, finite T+C |
| Bootstrap | PASS | — | Day-cluster stationary, geometric, circular, truncate to N, B=10000 |
| Null | PASS | — | ΔM*_null = ΔM* − ΔM_obs, inclusive ≥ |
| P-value | PASS | — | (1+count)/(1+B_valid) |
| CI | PASS | — | Percentile 2.5/97.5 of ΔM* |
| Holm | PASS | — | Eligible-market family, step-down, α=0.05 |
| Classification | PASS | — | SUPPORT/CONTRADICTED/INCONCLUSIVE/EVIDENCE-LIMITED |
| Data gates | CONDITIONAL | CRITICAL | Detection boundary and denominator need correction |
| Secondaries | PASS | — | MFE, range-normalized, invalidation rate, halves, year-by-year |
| Reproducibility | PASS | — | All artifacts persisted; protocol reference needs update |
| Determinism | PASS | — | Fixed seed, no wall-clock in science |
| Closed-line firewall | PASS | — | No imports from closed lines |
| Scope discipline | PASS | — | Only detection boundary and denominator need change |

---

## 15. Final Execution Recommendation

**CONDITIONAL PASS — DETERMINISTIC CORRECTIONS REQUIRED**

Two implementation corrections are required before V1.1.0 execution. Both are uniquely dictated by the frozen V1.1.0 protocol and require no new scientific or statistical decision:

### Correction 1: Detection Boundary (line 170)

**Current:**
```python
if len(det_pos) == 0 or emin[det_pos].max() < DETECT_END:
```

**Required:**
```python
if len(det_pos) == 0:
```

**Justification:** V1.1.0 §5/§20 define 17:00 ET as the upper boundary of the detection window, not as a required observation. The protocol explicitly states "bars may be missing inside the window without automatic failure." A day with detection-window bars through 16:59 ET is eligible.

### Correction 2: Invalid-Day Denominator (lines 139-144, 276-278)

**Current:** `n_total_dates` counts all calendar dates with ≥1 M1 observation.

**Required:** The denominator should count only dates with ≥1 M1 observation in the detection window (after opening window through 17:00 ET).

**Justification:** V1.1.0 §20 explicitly narrows the denominator to "calendar dates containing >= 1 M1 observation whose timestamp falls within the market post-opening-range detection window."

### Correction 3: Protocol References (lines 39-44)

**Current:** References V1.0.0 protocol SHA and path.

**Required:** Update to V1.1.0 SHA (`85263b84…`) and path (`ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md`).

**Justification:** The script should validate against the currently frozen protocol.

### Path Forward

After these three deterministic corrections:

1. Fresh independent implementation verification
2. Single compliant execution
3. Independent adjudication

---

## 16. Integrity

- Read-only: YES — no files modified during this audit
- No execution: CONFIRMED
- No rerun: CONFIRMED
- No scientific result calculation: CONFIRMED
- No PnL: CONFIRMED
- No cost analysis: CONFIRMED
- No protocol modification: CONFIRMED
- No Definition Lock modification: CONFIRMED
- No closed-line reopening: CONFIRMED

---

*This audit was produced as an independent, adversarial, read-only review of the ORD V1.1.0 execution implementation. Two deterministic corrections are required before execution authorization.*
