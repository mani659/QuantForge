# V37A PHASE A REPORT — FEASIBILITY / EVENT CONSTRUCTION

# REGISTRATION: V37A-REPL-077-XAUUSD-M1
# PHASE: A (signal-state detection and population accounting ONLY)
# DATE: 2026-09-03
# STATUS: PHASE A — FEASIBLE (population feasibility only; NO economic adjudication)

---

## 1. Execution Identity

| Field | Value |
|---|---|
| Registration | V37A-REPL-077-XAUUSD-M1 |
| Phase | A |
| Repository HEAD | `f192f3d283779164d79a84fed212e2bc13ca9f0a` |
| Branch | main |
| Driver | `output/research_discovery/V37A_REPL077_XAUUSD_PHASEA/phase_a_driver.py` |
| Machine-readable output | `output/research_discovery/V37A_REPL077_XAUUSD_PHASEA/phase_a_report.json` |

## 2. Hash Verification (all re-verified at execution start)

| Input | SHA-256 | Match |
|---|---|---|
| Historical implementation | `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b` | YES |
| Archival implementation | `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b` | YES |
| Registration artifact | `a8cf84fbce18bda56713a59347a8f900ab3e95e38c21b0c0cb3550febac729c6` | YES |
| Execution manifest | `4e76610f8a5f6a498eb1418460f143dca0d24ea6c490a70ce4395e25b23d77af` | YES |
| XAUUSD M1 data | `54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c` | YES |

## 3. Environment

Windows-10-10.0.19045-SP0 · Python 3.11.9 · pandas 3.0.2 · numpy 2.4.4 · branch main · HEAD f192f3d. Frozen helpers imported from the archival copy (SHA above) with a path-resolution fix only (module DIR pointed to the registered `data/m1`); function semantics unchanged.

## 4. XAUUSD Data Verification (FACT)

Full file: 1,768,123 bars, 2021-04-12 → 2026-04-10 (raw; shifted +4h per frozen `load()`). Monotonic timestamps: YES. Duplicate timestamps: 0. OHLC violations: 0 (no high<low, high<max(o,c), low>min(o,c), no non-positive prices). Volume all zero (unused). NaN in ATR percentile: exactly 200 at series head — the frozen implementation's intrinsic 200-bar warm-up (expected, not corruption). No tick/bid-ask data used.

## 5. Frozen Signal Pipeline Executed (EXECUTION RESULT)

Full-file load → +4h UTC shift (frozen `load()` semantics) → ATR(14, rolling mean) → ATR percentile (200-bar trailing, strict rank) → compression/comp_high detection → transition/breakout detection → treatment flags → control flags → primary-window entry-date filter (raw timestamps 2023-09-01 → 2026-04-10, applied AFTER state computation) → index-only matching accounting. All detection loops copied verbatim from frozen `run_077`. No forward indexing, no returns, no economics computed.

## 6. Populations (primary window, EXECUTION RESULT — counts only)

| Population | Count |
|---|---|
| Treatment events (window) | **2,309** (full file: 4,402) |
| Control events (window) | **25,034** (full file: 49,119) |
| Matched-control entries produced for window treatments (frozen earliest-in-±50 rule) | 559 |
| Unique control events used in matched sample | 226 |
| Duplicate control reuse in matched sample | 333 |
| Unmatched window treatments | 1,750 |
| Window treatment first/last entry | 2023-09-01 00:00 / 2026-04-09 22:04 |
| Window control first/last entry | 2023-09-01 00:59 / 2026-04-10 14:25 |

Comparison context (FACT, not economics): original CAND-077 on USATECHIDXUSD reported treatment N=2,084 and matched CF N=387 over its full history; the XAUUSD window yields treatment 2,309 and matched 559 — the same order of magnitude, and the same matching profile (frozen earliest-in-±50 rule reuses nearby control bars; unmatched treatments remain in treatment statistics, as in the original).

## 7. Feasibility Classifications (feasibility only, no economic meaning)

| Question | Classification |
|---|---|
| Control population exists under frozen definition? | CLEARLY FEASIBLE (25,034 window candidates; matched sample produced) |
| Treatment population instantiable under frozen definition? | CLEARLY FEASIBLE (2,309 window events) |
| Frozen matching executable? | YES (559 matched entries; rule reproduced mechanically) |

## 8. Data-Integrity Findings

No corruption. Scheduled market closures present (expected for XAUUSD retail M1) and handled identically to the original via the frozen bar-index convention. Warm-up sufficiency: full history precedes the window; all events ≥250 bars from series start; 30-bar outcome margin enforced by the frozen n−30 loop bound.

## 9. Phase-B Boundary Statement (FACT)

No close[i+30], gross return, net return, mean, median, delta, win rate, or any economic value was computed, stored, or printed by Phase A. The phase boundary is demonstrable from the driver source (detection and index-only accounting only).

---

*Phase A complete. Feasibility established. Governance checkpoint reached. Phase B requires separate authorization. NO economic interpretation is expressed in this report.*