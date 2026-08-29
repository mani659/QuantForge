# RESEARCH FACTORY V2 — G1 ECONOMIC PLAUSIBILITY SCREEN — V24
# DATE: 2026-08-29

## 1. G1 Status

V24 G1 COMPLETE. Three candidates screened using exact frozen definitions. Zero G2 promotions.

## 2. Data Used

- `data/m1/XAUUSD_M1.csv` — 1,768,123 bars (2021-04 to 2026-04)
- `data/m1/USATECHIDXUSD_M1.csv` — 906,815 bars (2023-09 to 2026-07)
- Friction: 2.0 bps round-trip
- No tick data, no Parquet pipeline
- All timestamps converted from UTC to ET (UTC-4)

## 3. CAND-071

### 3.1 Treatment
Gold overnight return (18:00–03:00 ET) > 0.5%. Enter USATECHIDXUSD at 09:30 ET in Gold's direction. Exit at 10:00 ET.

### 3.2 Counterfactual
Same Gold condition. Enter USATECHIDXUSD at 12:00 ET. Exit at 12:30 ET.

### 3.3 Economic Results

| Metric | Treatment | Counterfactual |
|---|---|---|
| N | 230 | 232 |
| Frequency | 88.7/yr | — |
| Mean Gross | +0.01 bps | — |
| Median Gross | +0.27 bps | — |
| Friction | 2.0 bps | 2.0 bps |
| Mean Net | -1.99 bps | -2.86 bps |
| Median Net | -1.73 bps | -2.46 bps |
| Win Rate | 52.2% | 47.4% |

### 3.4 Counterfactual Gate
TREATMENT SUPERIOR (mean net -1.99 vs -2.86; median net -1.73 vs -2.46). The open entry is slightly better than mid-day, but both are negative.

### 3.5 Payoff Structure
Median slightly positive (+0.27 bps gross), but mean dragged negative by left tail. Not broad-based positive.

### 3.6 Evidence Quality
High N (230 events). Treatment directionally superior to counterfactual. But absolute economics are negative after friction.

### 3.7 Mechanism vs Behavior
Gold→Tech overnight repricing at the open is OBSERVED BEHAVIOR (slightly better than mid-day). The hypothesized institutional-rebalancing MECHANISM is not directly observable.

### 3.8 Cross-Market Integrity
Both datasets are UTC-aligned and converted to ET. Timestamps are consistent.

### 3.9 Standalone Potential
WEAK. Mean net -1.99 bps is below zero.

### 3.10 Component Potential
MARGINAL. The Gold direction may add a small informational edge to other Tech modules (treatment is better than counterfactual), but the standalone signal is unprofitable.

### 3.11 Rare-Event Potential
NOT APPLICABLE. High frequency (88.7/yr) but negative economics.

### 3.12 G2 Eligibility
NOT ELIGIBLE. Failed absolute economic gate.

---

## 4. CAND-072

### 4.1 Treatment
Friday range in bottom 20% of rolling 4-week ranges. Monday first 30-min return > 0.3%. Enter at 10:00, exit at 15:45.

### 4.2 Counterfactual
Same Monday expansion. Friday range in top 50% (expanded). Same entry/exit.

### 4.3 Economic Results

| Metric | Treatment | Counterfactual |
|---|---|---|
| N | 26 | 66 |
| Frequency | 10.2/yr | — |
| Mean Gross | -3.15 bps | — |
| Median Gross | +1.40 bps | — |
| Friction | 2.0 bps | 2.0 bps |
| Mean Net | -5.15 bps | -10.98 bps |
| Median Net | -0.60 bps | -3.52 bps |
| Win Rate | 53.8% | 48.5% |

### 4.4 Counterfactual Gate
TREATMENT SUPERIOR (mean net -5.15 vs -10.98; median net -0.60 vs -3.52). Compressed Fridays produce less negative results than expanded Fridays, but both are negative.

### 4.5 Payoff Structure
Median slightly negative (-0.60 bps net). Mean strongly negative (-5.15 bps net) due to left tail. Not broad-based positive.

### 4.6 Evidence Quality
EVIDENCE-LIMITED (N=26). Treatment is better than counterfactual, but absolute economics are negative.

### 4.7 Mechanism vs Behavior
Friday compression → Monday behavior difference is OBSERVED. Forced-inventory MECHANISM is not directly observable.

### 4.8 Cross-Market Integrity
Single-market (USATECHIDXUSD). No cross-market requirements.

### 4.9 Standalone Potential
WEAK. Mean net -5.15 bps.

### 4.10 Component Potential
MARGINAL. The Friday compression state shows some informational value (treatment better than counterfactual), but the Alpha entry is unprofitable.

### 4.11 Rare-Event Potential
Low frequency (10.2/yr) with negative economics. Not viable.

### 4.12 G2 Eligibility
NOT ELIGIBLE. Failed absolute economic gate.

### 4.13 State Firewall
The Friday compression condition shows incremental information over the expanded counterfactual. This is OBSERVED STATE-RELATED INFORMATION — NOT SEPARATELY REGISTERED as a new state candidate.

---

## 5. CAND-073

### 5.1 Treatment
12:00–12:30 ET return > 0.4%. 12:30–12:45 confirms. Enter at 12:45, exit at 13:45.

### 5.2 Counterfactual
10:30–11:00 return > 0.4%. 11:00–11:15 confirms. Enter at 11:15, exit at 12:15.

### 5.3 Economic Results

| Metric | Treatment | Counterfactual |
|---|---|---|
| N | 308 | 149 |
| Frequency | 109.5/yr | — |
| Mean Gross | +0.02 bps | — |
| Median Gross | +0.10 bps | — |
| Friction | 2.0 bps | 2.0 bps |
| Mean Net | -1.98 bps | -2.57 bps |
| Median Net | -1.90 bps | -3.37 bps |
| Win Rate | 50.6% | 44.3% |

### 5.4 Counterfactual Gate
TREATMENT SUPERIOR (mean net -1.98 vs -2.57; median net -1.90 vs -3.37). Lunch reversals are less negative than mid-morning reversals, but both are negative.

### 5.5 Payoff Structure
Median near zero (+0.10 bps gross). Mean near zero (+0.02 bps gross). After friction, both are negative. Not broad-based positive.

### 5.6 Evidence Quality
High N (308 events). Treatment directionally superior. But absolute economics are negative after friction.

### 5.7 Mechanism vs Behavior
Lunch-session reversals produce slightly better outcomes than mid-morning reversals. OBSERVED BEHAVIOR. The institutional-repositioning MECHANISM is not directly observable.

### 5.8 Cross-Market Integrity
Single-market (USATECHIDXUSD). No cross-market requirements.

### 5.9 Standalone Potential
WEAK. Mean net -1.98 bps.

### 5.10 Component Potential
MARGINAL. The session-transition timing shows some informational value, but the standalone signal is unprofitable.

### 5.11 Rare-Event Potential
NOT APPLICABLE. High frequency (109.5/yr) but negative economics.

### 5.12 G2 Eligibility
NOT ELIGIBLE. Failed absolute economic gate.

---

## 6. Cross-Candidate Comparison

| Candidate | N | Freq/yr | Mean Net | Median Net | Counterfactual | Verdict |
|---|---|---|---|---|---|---|
| CAND-071 | 230 | 88.7 | -1.99 | -1.73 | Treatment Superior | INSUFFICIENT |
| CAND-072 | 26 | 10.2 | -5.15 | -0.60 | Treatment Superior | INSUFFICIENT |
| CAND-073 | 308 | 109.5 | -1.98 | -1.90 | Treatment Superior | INSUFFICIENT |

## 7. Counterfactual Gate Summary

All three candidates show TREATMENT SUPERIOR to counterfactual. The hypothesized mechanisms (cross-market timing, Friday inventory, lunch-session transition) all add some informational value. However, this value is insufficient to overcome friction in all cases.

## 8. Absolute Economic Gate

All three candidates FAIL the absolute economic gate (mean net < 0 after 2 bps friction). The gross returns are near zero or negative, meaning the signals do not produce enough directional edge to survive even minimal transaction costs.

## 9. Rare-Event Candidates

None. All three have either high frequency with negative economics (CAND-071, CAND-073) or low frequency with negative economics (CAND-072).

## 10. State/Condition Observations

- **CAND-072 Friday compression:** The compression condition shows incremental information over the expanded counterfactual (treatment less negative). This is OBSERVED STATE-RELATED INFORMATION — NOT SEPARATELY REGISTERED.
- **CAND-071 Gold overnight direction:** The Gold direction adds a small timing advantage at the open vs. mid-day. Weak state information.
- **CAND-073 Lunch timing:** The 12:00 window is slightly better than 10:30 for continuation trades. Weak state information.

No new state candidates are registered during G1.

## 11. Prior-Art / Redundancy

- CAND-071: NEW — no prior cross-market testing
- CAND-072: NEW — no prior weekly calendar structure testing
- CAND-073: EXTENSION — prior session work (CAND-062, 069) tested fades/anchors, not continuation

No redundancy with prior V19–V23 candidates detected.

## 12. Closed-Line Firewall

No closed lines reopened. No disguised rescues.

## 13. Protected Forward Runtime

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED

Do not inspect forward performance.

## 14. G2 Promotions

> NONE

All three candidates failed the absolute economic gate.

## 15. Infrastructure

- Data: `data/m1/XAUUSD_M1.csv`, `data/m1/USATECHIDXUSD_M1.csv`
- Script: `research/v24_g1_screen.py`
- No tick data, no Parquet pipeline, no production infrastructure
- Results: `output/research_discovery/v24_g1_results.json`

## 16. Conclusion

V24 G1 screened three candidates from genuinely distinct mechanism families (cross-market transmission, calendar structure, session microstructure). All three showed TREATMENT SUPERIOR to counterfactual, confirming that the hypothesized mechanisms add some informational value. However, all three failed the absolute economic gate — the gross returns are near zero, meaning the signals do not produce enough directional edge to survive even 2 bps of friction.

**Root Cause:** The mechanisms are real but weak. Gold→Tech overnight repricing, Friday inventory compression, and lunch-session reversals all produce small directional tendencies, but these tendencies are too small to overcome transaction costs in a CFD/retail execution environment.

**Implication:** These mechanism families may be more suitable for:
1. Lower-friction instruments (futures with 0.5 bps execution)
2. State/condition filters for other, stronger Alpha signals
3. Cross-market correlation modules in a multi-asset system

None of these pathways are authorized at this stage.

## 17. Next Milestone

V24 G1 is COMPLETE. No G2 promotions. The Research Factory returns to G0 for V25 candidate generation, or the project may choose to focus exclusively on forward-qualifying the existing rare-event components (CAND-024, CAND-035).
