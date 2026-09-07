# V37A PHASE B REPORT — OUTCOME MEASUREMENT

# REGISTRATION: V37A-REPL-077-XAUUSD-M1
# PHASE: B (frozen 30-bar outcome measurement — single run)
# DATE: 2026-09-03
# STATUS: EXECUTED / RESULTS PRESERVED — NO ADJUDICATION

---

## 1. Execution Identity / Hash Verification

All frozen hashes re-verified at Phase-B start and matched (FACT): historical `b320c42d…`, archival `b320c42d…`, registration `a8cf84fb…`, manifest `4e76610f…`, XAUUSD data `54cf6155…`. Repository HEAD `f192f3d283779164d79a84fed212e2bc13ca9f0a` (matches freeze commit). Environment: Windows-10-10.0.19045 · Python 3.11.9 · pandas 3.0.2 · numpy 2.4.4. Driver: `phase_b_driver.py`.

## 2. Population Reconciliation (FACT)

Primary-window treatment population recomputed with identical verbatim detection and **exactly matched the locked Phase-A count (2,309)** before any outcome was computed (guard in driver). Matched-control observations = 559, equal to Phase A's matched count. No population discrepancy.

## 3. Outcome Definition (frozen)

entry=close[i]; exit=close[i+30]; gross=((close[i+30]−close[i])/close[i])×10⁴; net=gross−2.0 bps per event (identical to the frozen constant-shift convention for mean/median aggregates). Bar-index based; no clock-time conversion; no bid/ask; no alternate costs. All events satisfy exit_index=entry_index+30 by the frozen n−30 detection boundary; zero events excluded by any other rule.

## 4. Primary-Window Results (2023-09-01 → 2026-04-10) — MEASUREMENT ONLY

| Metric | Treatment | Control | Delta |
|---|--:|--:|--:|
| N | 2,309 | 559 (matched) | — |
| Gross mean (bps) | +1.81 | +1.14 | +0.67 |
| Net mean (bps) | −0.19 | −0.86 | **+0.67** |
| Net median (bps) | −1.43 | −0.06 | −1.37 |
| Gross median (bps) | +0.57 | +1.94 | −1.37 |
| Win rate (gross > 0) | 52.2% | 55.1% | −2.9% |

**PRIMARY METRIC (net mean delta): Treatment net mean − Control net mean = +0.67 bps.**

Distribution (treatment / control): std (gross) 22.17 / 21.76; worst −87.01 / −169.52; best +329.98 / +66.54; exclude-best net mean −0.33 / −1.22.

## 5. Secondary Full-History Consistency Check (2021-04-12 → 2026-04-10; pre-registered, separate)

| Metric | Treatment | Control | Delta |
|---|--:|--:|--:|
| N | 4,402 | 934 (matched) | — |
| Gross mean (bps) | +0.56 | +0.50 | +0.06 |
| Net mean (bps) | −1.44 | −1.50 | +0.06 |
| Net median (bps) | −2.21 | −2.51 | +0.30 |
| Win rate | 49.3% | 48.5% | +0.8% |

Secondary result is reported separately and does not replace the primary verdict.

## 6. Match-Reuse / Dependence Accounting (FACT)

Primary window: 559 matched control observations derive from **226 unique control events**; **153 unique controls are referenced by ≥2 treatments** (333 duplicate references in the matched sample); 73 unique controls referenced exactly once; 1,750 treatments unmatched (remain in treatment statistics per the frozen method, mirroring the original). Reuse structure is preserved in the event-level artifact for later adjudication; no independence is claimed for the matched-control sample.

## 7. Completeness Check (FACT)

Phase-A treatment count 2,309 → Phase-B treatment outcomes 2,309 (100%, zero unexplained discrepancy). Phase-A matched-control count 559 → Phase-B control outcomes 559 (100%). Every outcome valid with exit_index=entry_index+30.

## 8. Method-Integrity / No-Rerun Statement

Single run. No post-hoc subsetting, no session/day/time filtering, no outlier removal, no additional robustness filters beyond the frozen exclude-best diagnostic, no result-based rerun, no methodology change. Sole robustness diagnostic: exclude-best net mean (frozen).

## 9. Artifacts (isolated V37A directory, all untracked)

- `phase_b_driver.py`
- `phase_b_event_level_primary.csv` (2,868 rows: 2,309 treatment + 559 matched-control observations; experiment_id, phase, market, timestamp, bar_index, classification, treatment/control event ids, matched-control bar/timestamp, reuse indicator, entry/exit price, gross/net bps, window indicator)
- `phase_b_event_level_secondary.csv` (5,336 rows)
- `phase_b_report.json` (aggregates)
- `phase_b_report.md` (this report)

No frozen artifact overwritten; registration and manifest untouched.

---

*Phase B complete. Measurements preserved without interpretation. Adjudication is a separate governed step. NO Alpha / State / replication conclusion is expressed here.*