# QUANTFORGE — ORD V1.1.0 EXECUTION IMPLEMENTATION

# FRESH INDEPENDENT RE-AUDIT V1

## 1. Executive Verdict

> **PASS — EXECUTION AUTHORIZED**

The corrected implementation faithfully implements the frozen ORD V1.1.0 protocol. All prior defects have been resolved. No new scientific, statistical, or data-quality ambiguity remains. Two independent researchers using this implementation would obtain materially identical scientific results.

## 2. Frozen Protocol Identity

| Field | Value |
|---|---|
| Version | V1.1.0 |
| File | `ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md` |
| SHA-256 | `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06` |

## 3. Implementation Identity

| Field | Value |
|---|---|
| File | `scripts/run_ord_v1.py` |
| Protocol path | `output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md` |
| Protocol SHA | `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06` |
| Correction record | `ORD_OPENING_RANGE_IMPLEMENTATION_CORRECTIONS_V1_1.md` |

## 4. Detection Boundary

**Frozen rule (§5):** "through 17:00:00 ET inclusive" — upper boundary, not required observation.

**Frozen rule (§20):** "bars may be missing inside the window without automatic failure — no hidden gapless-session requirement."

**Implementation trace:**

```python
DETECT_END = 17 * 60  # 17:00:00 ET inclusive
det_mask = (emin > win_end) & (emin <= DETECT_END)
det_pos = np.nonzero(det_mask)[0]
if len(det_pos) == 0:
    continue  # no detection-window bars -> zero events this day
```

**Independent verification:**

- `emin <= DETECT_END` correctly includes 17:00 (et_min=1020 ≤ 1020) ✅
- `emin > win_end` correctly starts after the opening window ✅
- `len(det_pos) == 0` correctly requires only that at least one detection-window bar exists ✅
- No `max(et_min) >= 1020` or equivalent remains ✅
- A day with bars through 16:59 ET (et_min=1019) has `1019 ≤ 1020` → included in detection window ✅
- A day with no detection-window bars is skipped (zero events, not invalid) ✅

**Verdict: CORRECT** ✅

## 5. V1.1 Denominator

**Frozen rule (§20):** "the denominator consists of calendar dates containing >= 1 M1 observation whose timestamp falls within the market post-opening-range detection window (after the 30-minute opening window closes through 17:00:00 ET inclusive)"

**Implementation trace:**

```python
det_window_mask = (et_min > win_end) & (et_min <= DETECT_END)
dates_with_det_obs = set(df.loc[det_window_mask, "date"].unique())
n_total_dates = len(dates_with_det_obs)
```

**Independent verification:**

- `et_min > win_end` selects bars after the opening window ✅
- `et_min <= DETECT_END` selects bars through 17:00 ET inclusive ✅
- `df.loc[det_window_mask, "date"].unique()` extracts unique dates with detection-window observations ✅
- `n_total_dates = len(dates_with_det_obs)` sets denominator = detection-window dates only ✅
- Opening-range-only observations do NOT qualify a date for the denominator ✅
- Weekends with stray observations outside the detection window are excluded ✅
- No weekday filter introduced ✅
- No holiday calendar introduced ✅
- No exchange calendar introduced ✅

**Anomaly denominator ≠ event population:**

- A date enters the denominator if it has ≥1 detection-window observation
- A date produces zero events if it fails the opening-window gate or has no qualifying break/penetration
- These populations are correctly distinct in the code ✅

**Verdict: CORRECT** ✅

## 6. Invalid-Day Gate

**Frozen rule (§20):** "An invalid day = a denominator date that fails the opening-window completeness gate"

**Implementation trace:**

```python
if not win_ok:
    if date in dates_with_det_obs:
        n_invalid_days += 1
    continue
```

**Independent verification:**

- `n_invalid_days` increments only when `date in dates_with_det_obs` (denominator date) ✅
- `n_invalid_days` increments only when `not win_ok` (opening-window gate failure) ✅
- Dates outside the denominator are not counted as invalid ✅
- The fraction `n_invalid_days / n_total_dates` is computed correctly ✅
- The 10% halt threshold is applied per market before inference ✅

**Verdict: CORRECT** ✅

## 7. Protocol Identity

| Field | Script | Required |
|---|---|---|
| PROTOCOL_PATH | `...V1_AMENDED.md` | `...V1_AMENDED.md` ✅ |
| PROTOCOL_SHA | `85263b84...` | `85263b84...` ✅ |
| Docstring version | V1.1.0 | V1.1.0 ✅ |

No accidental V1.0.0 execution path exists.

**Verdict: CORRECT** ✅

## 8. Scientific Object

Protocol §1: "Opening range → close-break → entry at breakout close → structural invalidation → post-entry directional continuation."

**Implementation trace:**

- Opening range: 30-bar window → High_OR, Low_OR ✅
- Breakout: `dc > hi_or` (long), `dc < lo_or` (short) — strict inequality ✅
- Entry: `entry_close = float(c[ev_row])` — breakout candle close ✅
- Invalidation: subsequent close ≤ High_OR (long) or ≥ Low_OR (short) ✅
- Response: bp directional return at 120-min horizon ✅

**Verdict: CORRECT** ✅

## 9. Event Construction

### Opening Range

- XAUUSD/XAGUSD/BTCUSD: start=180 (03:00), end=209 (03:29) ✅
- USATECHIDXUSD: start=570 (09:30), end=599 (09:59) ✅
- 30-bar completeness: `len(wrows) == 30` ✅
- Valid OHLC: `np.all(wo > 0) and np.all(wh > 0) and np.all(wl > 0) and np.all(wc > 0)` ✅
- Nonzero range: `hi_or > lo_or` ✅

### Breakout

- Long: `dc > hi_or` ✅
- Short: `dc < lo_or` ✅
- First per direction: `long_break_rows[0]` / `short_break_rows[0]` ✅
- No ATR/tick filter ✅

### Entry

- `entry_close = float(c[ev_row])` ✅
- No next-bar substitution ✅

### Invalidation

- Long: `win_closes <= inval_edge` where `inval_edge = hi_or` ✅
- Short: `win_closes >= inval_edge` where `inval_edge = lo_or` ✅
- No buffer ✅

### Event Uniqueness

- First long/day and first short/day ✅
- Max two events/day ✅
- No duplicate event creation ✅

**Verdict: CORRECT** ✅

## 10. Control / Response

### Control

- Long control: `dh > hi_or` (high penetration) AND no `dc > hi_or` (no qualifying close-break) ✅
- Short control: `dl < lo_or` (low penetration) AND no `dc < lo_or` (no qualifying close-break) ✅
- Control anchor: penetration candle close ✅
- Continuation-direction sign: long control → positive response sign, short control → negative ✅

### Primary Response

- Long: `(horizon_close - entry_close) / entry_close * 1e4` ✅
- Short: `(entry_close - horizon_close) / entry_close * 1e4` ✅
- Horizon: `target = entry_ts + np.timedelta64(120, "m")` ✅
- Complete horizon required: `horizon_complete = i < len(ts_arr) and ts_arr[i] == target and c[i] > 0` ✅
- Incomplete horizon excluded before inference ✅

**Verdict: CORRECT** ✅

## 11. Statistical Machinery

### Bootstrap

- Day-cluster stationary: `days_treat` / `days_control` dictionaries keyed by day index ✅
- Geometric blocks: `rng.geometric(0.1, size=B * blocks_est)` ✅
- Circular wrap: `walk = (sl[:, None] + off) % N` ✅
- Truncate to N: `seq = walk[mask][:N]` ✅
- B = 10,000 ✅
- Seed = 20260818 ✅
- Replicate validity: skips if NaN median ✅

### Null

- `null_draws = valid_draws - dm_obs` (DeltaM* - DeltaM_obs) ✅
- Count: `np.sum(np.abs(null_draws) >= abs(dm_obs))` — inclusive >= ✅
- p-value: `(1 + count) / (1 + B_valid)` ✅
- No zero p-values possible ✅

### CI

- `np.percentile(valid_draws, 2.5)` and `np.percentile(valid_draws, 97.5)` ✅
- From ordinary sampling distribution, not null ✅

### Holm

- Eligible-market family only ✅
- Step-down: `adj = np.minimum(1.0, (m_count - np.arange(m_count)) * ps[order])` ✅
- α = 0.05 ✅
- Monotone: `adj = np.maximum.accumulate(adj)` ✅

### Classification

- SUPPORT: Holm p < 0.05 AND dm > 0 ✅
- CONTRADICTED: Holm p < 0.05 AND dm < 0 ✅
- INCONCLUSIVE: otherwise ✅
- EVIDENCE-LIMITED: <100 treatment events ✅

**Verdict: CORRECT** ✅

## 12. Data Gates

| Gate | Implementation | Protocol § |
|---|---|---|
| UTC input | `pd.to_datetime(..., format="%Y-%m-%d %H:%M:%S")` | §20 |
| ET conversion | `.dt.tz_localize("UTC").dt.tz_convert(ET)` | §4 |
| Duplicates | `.drop_duplicates(subset="ts", keep="first")` | §20 |
| Invalid OHLC | `np.all(wo > 0) and ...` | §20 |
| OR completeness | `len(wrows) == 30` | §4 |
| Detection window | `(et_min > win_end) & (et_min <= DETECT_END)` | §5, §20 |
| Anomaly denominator | `dates_with_det_obs` | §20 (amended) |
| >10% halt | `if diag["invalid_fraction"] > HALT_FRACTION` | §20 |
| 120-min horizon | `target = entry_ts + np.timedelta64(120, "m")` | §9 |
| Incomplete horizon | Excluded before inference | §9 |
| Zero-event dates | Not in eligible set | §13 |

**Verdict: CORRECT** ✅

## 13. Reproducibility

| Artifact | Persisted | Protocol § |
|---|---|---|
| Protocol SHA | metadata.json | §26 |
| Input hashes | metadata.json (pre-execution gate) | §26 |
| Environment | metadata.json | §26 |
| Parameter manifest | metadata.json | §26 |
| Event tables | event_table_all_markets.csv | §26 |
| Bootstrap draws | bootstrap_{market}.npy | §26 |
| Null draws | null_{market}.npy | §26 |
| Statistics | statistics.json | §26 |
| Metadata | metadata.json | §26 |

**Verdict: CORRECT** ✅

## 14. Determinism

| Check | Implementation |
|---|---|
| Fixed seed | `SEED = 20260818` ✅ |
| No wall-clock random | No `time.time()` in scientific calcs ✅ |
| Chronological sort | `df.sort_values("ts")` ✅ |
| Deterministic grouping | `df.groupby("date", sort=True)` ✅ |
| Deterministic timezone | `ZoneInfo("America/New_York")` ✅ |
| Stable median | `np.median` ✅ |
| Stable percentile | `np.percentile` ✅ |
| Stable searchsorted | `np.searchsorted` ✅ |

**Verdict: CORRECT** ✅

## 15. Implementation Diff

### Authorized corrections applied:

| # | Correction | Old | New | Semantic? |
|---|---|---|---|---|
| 1 | Detection boundary | `max(et_min) < DETECT_END` | `len(det_pos) == 0` | Yes |
| 2 | V1.1 denominator | All calendar dates | Detection-window dates | Yes |
| 3 | Protocol identity | V1.0.0 path/SHA | V1.1.0 path/SHA | No |

### No unauthorized changes detected:

All other code paths, constants, logic, and data handling are unchanged from the pre-correction state as documented by the correction record.

**Verdict: CORRECT** ✅

## 16. Closed-Line Independence

- No Mean Reversion semantics (DISC-021) ✅
- No TSMOM semantics (DISC-022) ✅
- No Session Range Expansion semantics (DISC-024) ✅
- No Liquidity Sweep/Reversal semantics (DISC-025) ✅
- No detector/BOE logic ✅

**Verdict: CORRECT** ✅

## 17. Findings Table

| Area | Verdict | Severity | Finding |
|---|---|---|---|
| Protocol identity | ✅ PASS | — | V1.1.0 path and SHA correctly referenced |
| Detection boundary | ✅ PASS | — | `len(det_pos) == 0`; no 17:00 bar required |
| V1.1 denominator | ✅ PASS | — | Detection-window dates only |
| Invalid-day count | ✅ PASS | — | Denominator dates failing OR gate |
| Weekend/holiday handling | ✅ PASS | — | Observation-driven; no calendar |
| Opening range | ✅ PASS | — | 30 bars, valid OHLC, nonzero range |
| Breakout | ✅ PASS | — | Strict inequality, first per direction |
| Entry | ✅ PASS | — | Breakout candle close |
| Invalidation | ✅ PASS | — | Subsequent close through edge |
| Control | ✅ PASS | — | Penetration without close-break |
| Primary response | ✅ PASS | — | 120-min bp from entry close |
| Event uniqueness | ✅ PASS | — | First long/short per day |
| Evaluability | ✅ PASS | — | ≥100 treatment events |
| Bootstrap | ✅ PASS | — | Day-cluster stationary, B=10000, seed=20260818 |
| Null | ✅ PASS | — | DeltaM* - DeltaM_obs, inclusive >= |
| P-value | ✅ PASS | — | (1+count)/(1+B_valid) |
| CI | ✅ PASS | — | 2.5th/97.5th percentiles |
| Holm | ✅ PASS | — | Step-down, α=0.05 |
| Classification | ✅ PASS | — | SUPPORT/CONTRADICTED/INCONCLUSIVE/EVIDENCE-LIMITED |
| Data gates | ✅ PASS | — | All gates per §20 |
| Reproducibility | ✅ PASS | — | All artifacts persisted |
| Determinism | ✅ PASS | — | Fixed seed, stable operations |
| Diff scope | ✅ PASS | — | Only 3 authorized corrections |
| Closed-line firewall | ✅ PASS | — | Independent of all closed lines |

## 18. Final Execution Recommendation

> **ORD V1.1.0 execution implementation is approved for one single compliant execution.**

All prior defects (detection boundary, V1.1 denominator, protocol identity) have been resolved. The implementation now faithfully represents the frozen V1.1.0 protocol. No new scientific, statistical, or data-quality decision is required.

The next task is:

> **ORD V1.1.0 SINGLE CONTROLLED EXECUTION**

## 19. Integrity

- Read-only: no execution performed during this re-audit
- No rerun of V1.0.0
- No scientific results generated
- No PnL or cost analysis
- No protocol modification
- No Definition Lock modification
- No closed-line reopening
