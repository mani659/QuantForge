# QUANTFORGE — ORD V1.1.0 IMPLEMENTATION CORRECTIONS

## 1. Correction Status

> **DETERMINISTIC CORRECTIONS APPLIED — EXECUTION NOT PERFORMED**

Date: 2026-08-18

## 2. Source Audit

Independent implementation audit:

`output/research_discovery/ORD_OPENING_RANGE_EXECUTION_IMPLEMENTATION_AUDIT_V1_1.md`

Verdict: **CONDITIONAL PASS — DETERMINISTIC CORRECTIONS REQUIRED**

## 3. Frozen Protocol

`output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md`

Version: **V1.1.0**

SHA-256: `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06`

## 4. Corrections Applied

### Correction 1 — Detection-Window Coverage

| Field | Value |
|---|---|
| Audit finding | Line 170 used `max(et_min) < DETECT_END` — requires physical 17:00 bar |
| Frozen rule | 17:00 ET is upper boundary; bar NOT required |
| Change | Replaced with `len(det_pos) == 0` — any detection-window bar suffices |
| Lines affected | ~170 |
| Semantic change | Detection window no longer requires 17:00 observation |

### Correction 2 — V1.1.0 Invalid-Day Denominator

| Field | Value |
|---|---|
| Audit finding | Denominator used all calendar dates with ≥1 raw M1 observation (V1.0.0 rule) |
| Frozen rule | V1.1.0: dates with ≥1 M1 observation in the market-session detection window |
| Change | Computed `dates_with_det_obs` from detection-window mask; denominator = this set |
| Lines affected | ~139-146 |
| Semantic change | Weekends/holidays with stray observations outside detection window excluded |

### Correction 3 — Protocol Identity

| Field | Value |
|---|---|
| Audit finding | Script referenced V1.0.0 protocol path and SHA |
| Frozen rule | V1.1.0 is the current frozen protocol |
| Change | Updated `PROTOCOL_PATH`, `PROTOCOL_SHA`, docstring to V1.1.0 |
| Lines affected | ~39-44, docstring |
| Semantic change | None (metadata only) |

## 5. Verification of Unchanged Elements

All of the following were verified UNCHANGED after corrections:

- ✅ MARKETS (XAUUSD, XAGUSD, BTCUSD, USATECHIDXUSD)
- ✅ Opening-range windows (03:00-03:29 for XAU/XAG/BTC; 09:30-09:59 for USATECH)
- ✅ 30-bar completeness gate
- ✅ Breakout: `dc > hi_or` / `dc < lo_or` (strict inequality)
- ✅ Entry = breakout-candle close
- ✅ Invalidation: `Close <= High_OR` / `Close >= Low_OR`
- ✅ Control: penetration without qualifying close-break
- ✅ Primary response: 10000 × bp directional return at 120-min horizon
- ✅ Bootstrap: day-cluster stationary, B=10000, seed=20260818, p_terminate=0.1
- ✅ Null: DeltaM*_null = DeltaM* - DeltaM_obs
- ✅ p-value: (1+count)/(1+B_valid), inclusive >=
- ✅ CI: 2.5th/97.5th percentiles
- ✅ Holm step-down, α=0.05
- ✅ Classification: SUPPORT/CONTRADICTED/INCONCLUSIVE/EVIDENCE-LIMITED
- ✅ MIN_TREATMENT = 100
- ✅ HALT_FRACTION = 0.10
- ✅ Event uniqueness: first long/short per day
- ✅ Secondary outputs: MFE, range-normalized, invalidation rate, halves, year-by-year
- ✅ Closed-line independence
- ✅ Determinism: fixed seed, sorted inputs, stable grouping
- ✅ Artifact persistence: bootstrap/null draws, event table, statistics, metadata

## 6. No Other Semantic Changes

The three corrections are the ONLY semantic changes applied.

- No new scientific/statistical decisions introduced
- No new data-quality rules added
- No new market filters introduced
- No statistical machinery altered
- No secondary definitions changed
- No closed-line records modified

## 7. Denominator Logic Detail

The corrected denominator logic:

```python
# V1.1.0 denominator: dates with >= 1 observation in the detection window
# (after opening window through 17:00 ET inclusive)
det_window_mask = (et_min > win_end) & (et_min <= DETECT_END)
dates_with_det_obs = set(df.loc[det_window_mask, "date"].unique())
n_total_dates = len(dates_with_det_obs)
```

Invalid-day counting:

```python
if not win_ok:
    if date in dates_with_det_obs:
        n_invalid_days += 1  # denominator date that fails opening-window gate
    continue  # ineligible day -> no events
```

This ensures:
- Only detection-window dates enter the denominator
- Invalid days are denominator dates that fail the opening-window gate
- Dates with no detection-window observations are excluded entirely
- No external holiday calendar or weekday filter is introduced

## 8. Detection Coverage Logic Detail

The corrected detection-coverage check:

```python
det_mask = (emin > win_end) & (emin <= DETECT_END)
det_pos = np.nonzero(det_mask)[0]
det_rows = rows[det_pos]
if len(det_pos) == 0:
    continue  # no detection-window bars -> zero events this day
```

This ensures:
- Any detection-window bar (through 16:59:59 or at 17:00:00 ET) is sufficient
- A physical 17:00 bar is NOT required
- Days with detection-window observations can produce events

## 9. Execution

> **NOT PERFORMED**

No scientific results were generated during this correction task.

## 10. Next Required Task

> **FRESH INDEPENDENT ORD V1.1.0 EXECUTION IMPLEMENTATION RE-AUDIT**

The corrected implementation must be independently verified before execution is authorized.

## 11. Integrity

- Read-only: no execution, no rerun
- No scientific result calculation
- No PnL or cost analysis
- No protocol modification
- No Definition Lock modification
- No closed-line reopening
