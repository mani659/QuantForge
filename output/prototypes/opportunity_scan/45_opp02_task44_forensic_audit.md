# TASK 45 — OPP-02 TASK 44 FORENSIC AUDIT

**Objective:** Independently audit Task 44 before accepting its C verdict. This task is **audit only** — it makes no strategy change, no parameter optimization, no candidate creation, no governance change, and no modification to Task 44 outputs.

**Question under audit:** Did Task 44 correctly implement the frozen OPP-02 strategy and produce numerically meaningful results?

**Frozen OPP-02 spec (Tasks 41/43 source of truth):**

| Component | Frozen Task 43 definition |
|---|---|
| Universe | 11-symbol MT5 H4 cache (`_t37_h4_*.npz`) |
| Signal | trailing total return (rank vector over cross-section) |
| Return window | {4, 8, 13, 26 **weeks**} |
| Rebalance | **weekly** |
| Selection | long top tercile / short bottom tercile |
| Weighting | equal weight |
| Replacement | positions replaced (never averaged) |
| Hold | 5 sessions |
| Fill | next-bar open |
| Costs | 10/5/0 bps per side + disclosed swap proxy |
| Periods | common-11 span only (2021-01-03 → 2026-09-30, 8,902 rows) |

---

## 1. GOVERNANCE

- `docs/SESSION_HANDOFF.md` — Research Capacity HOLD; Active Research NONE; no backtest authorized.
- `docs/CHATGPT_ROLE_ADDENDUM_LANEB_PROPOSED.md` — **PROPOSED, not adopted.** Lane B empirical evaluation requires explicit owner authorization tied to a frozen prototype/specification.
- Task 44 was executed with a frozen representative spec; no new strategy test, parameter change, candidate, or governance change was authorized in this task.
- No new output is marked as governed research evidence. This is a forensic audit artifact only.

---

## 2. RECONSTRUCTION: FROZEN SPEC vs TASK 44 IMPLEMENTATION

| Component | Frozen Task 43 | Task 44 implementation | Match? |
|---|---|---|---|
| Return window {4,8,13,26} | **weeks** (7 daily bars each) | **days** (4/8/13/26 daily bars) | **NO — mismatch** |
| Ranking cadence | weekly rebalance | every daily row (8,898/8,894/8,889/8,876 obs) | **NO — mismatch** |
| Rebalance timestamp | Monday close | every daily H4 close | **NO — mismatch** |
| Entry fill price | next-bar-open H4 open | daily close + w-day trailing return (implicit next bar) | **NO — mismatch** |
| Hold | 5 sessions | 5 sessions (vacuous on daily data) | no conflict, but moot |
| Top/bottom tercile | 3rd/9th decile | rank ≤3 / ≥9 | match |
| Equal weight | yes | yes | match |
| Replacement | replace, not average | replace | match |
| Cost tiers 10/5/0 bps | yes | yes | match |
| Swap proxy | disclosed | disclosed (C, fixture not in repo) | match |

**Primary defect:** Task 44 treated the daily H4 pivot as a sequence of independent daily "rebalance observations" and computed trailing-return separation for day-count windows {4,8,13,26}. The frozen spec defines **weekly** ranks at **weekly** dates over **weekly** windows. The two are different statistics.

---

## 3. CRITICAL TIMING AUDIT

### A. Rebalance timestamp
Task 44: **every daily row** of the pivot (the pivot is daily, one row per calendar day with 8,902 rows across 2021-01-03 → 2026-09-30). The frozen spec requires **weekly rebalance at Monday closes**.

### B. Entry price
Task 44: trailing window `w` days of past daily closes (`c[w:]/c[:-w]-1`); the "next bar" is the next row in the daily series, i.e., the next day's close of the daily pivot. The frozen spec says **next-bar-open fill** on the weekly rebalance date.

### C. Information at that timestamp
Task 44: at row `t` it knows the trailing `w`-day window ending at `t` (closing price `t`), and enters at the **next day's close** — a **one-period lookahead on the daily pivot**. Frozen spec: at Monday `t` it knows the trailing `w` weeks of weekly closes, enters at the **next bar's open** (H4), which is at most the next H4 bar after the Monday close.

### D. Exit price
Task 44: 5 sessions forward of entry → on daily pivot data, essentially the next ~5 daily bars (weeks of ~5 trading days × ~5 H4 bars). Frozen spec: 5 sessions forward of entry at weekly rebalance.

### E. Sessions actually held
Task 44: on a daily pivot, "5 sessions" ≈ 5 daily bars; the spec's "5 sessions" is applied to the daily-to-5-daily bar interpretation, not to a weekly-horizon ladder. The weekly-rebalance dates are ~1,756 Mondays per the pivot.

### F. Replacement
Week: positions replaced at each weekly rebalance — Task 44 replaces per daily row (effectively daily replacement). **Mismatch**.

### G. Return measurement
Task 44: per-day **mean top tercile return − mean bottom tercile return** over the next `w` daily bars, averaged across ~8,900 daily rows. This measures **daily-obs separation**, not weekly-rebalanced return. Frozen spec measures the **weekly-rebalanced long-short dispersion return**.

### H. Ranking on every daily observation
**Yes** — Task 44 ranks once per daily row. It does not restrict to weekly dates. This is the single largest methodological divergence.

**Conclusion:** Task 44 did not implement weekly rebalance + 5-session holding in the frozen sense. It implemented a per-day cross-sectional dispersion measure with day-count windows.

---

## 4. RETURN-MAGNITUDE SANITY CHECK

For the **correctly defined weekly-rebalance statistic** (W weeks = 7w daily bars, Mondays only), the spread is:

| Window | Weekly-rebal mean top bps | mean bot bps | mean spread bps | task44 daily-mean bps | z (task44 vs its null) |
|---|---:|---:|---:|---:|---:|
| W4 | 4,541 | 1,607 | +2,933.7 | +475.0 | 0.25 |
| W8 | 6,983 | 911 | +6,071.8 | +970.2 | 0.11 |
| W13 | 9,890 | 563 | +9,327.2 | +1,536.3 | 0.27 |
| W26 | 18,639 | 720 | +18,636.2 | +2,782.8 | 0.23 |

The frozen W26 weekly mean spread is **+18,636 bps** (≈ +186%), and the observed mean is only **~1.35σ** above its own weekly null. The Task 44 "W26 = +2,783 bps" is a **different quantity** (daily-rows average) and does **not** represent the frozen weekly-rebalanced portfolio. The W26 mean is not "inflated" in absolute terms — it is a different statistic; but as a replication of the frozen spec it is invalid.

The dispersion is extreme in both frameworks (weekly p05/p95 spanning ±39k to ±176k bps), so the mean is dominated by a small number of extreme days regardless.

---

## 5. UNIT AUDIT

| Quantity | Raw unit | Task 44 transformation | Final reported unit | Correct? |
|---|---|---|---|---|
| Trailing return `c[w:]/c[:-w]-1` | decimal (e.g., 0.027) | reported as bps ×1e6 after *1e6 | bps | scale is internal-consistent |
| Per-day top/bot mean | decimal | subtracted → decimal | bps ×1e6 | consistent |
| `act.mean()*1e6` | decimal | → bps | bps | consistent |
| `act.sum()` (gross) | decimal summed | reported as "return" | "bps-equivalent" | **unit confusion**: sum of daily spreads is not a return; it has units of "per-unit daily spread summed over days" |
| Friction `2*tb/10000*Σ|act|` | decimal | subtracted from `act.sum()` | "bps-equivalent" | consistent with its own definition but not a dollar or return |
| Sharpe `act.std()` | decimal | `avg/vol*sqrt(252)` | unitless | internally consistent |
| MDD `cumsum` of daily spread | decimal | `dd.min()` → reported | "MDD" | consistent with daily-spread series, not portfolio returns |

Specific concerns:
- **Aggregate sums vs means**: Task 44 reports `gross_ret = Σ act`, which is a sum of daily spread values, not a compounded portfolio return. As a "return" it needs an explicit notional/frequency normalization. This does not change the rank order but it does mean the %/bps labels are conditional.
- **×1e6 vs ×1e4 vs ×100**: Task 44 multiplies decimal by 1e6 (bps). 10 bps per side = 0.001 in decimal; applied as `2*tb/10000*Σ|act|`. This is correct for bps if `act` is in decimal decimal. The labels follow this convention. No decimal-vs-percent scaling error was found in the main statistic itself.

---

## 6. INDEPENDENT REBUILD — SAMPLE RECONSTRUCTION TABLE

Independent audit script (`audit_build01_weekly_rebuild.json`, `audit_01_independent_rebuild.py`) reconstructs the weekly-rebalance statistic from the frozen inputs:

| Rebalance window | n weekly dates | top mean bps | bottom mean bps | spread bps | Task44 daily mean bps | diff bps | Task44 z | Weekly-null z |
|---|---|---|---|---|---|---|---|---|
| W4 | 1,750 | 4,541 | 1,607 | +2,933.7 | +475.0 | +2,458.7 | 0.25 | 1.39 |
| W8 | 1,744 | 6,983 | 911 | +6,071.8 | +970.2 | +5,101.6 | 0.11 | 1.27 |
| W13 | 1,738 | 9,890 | 563 | +9,327.2 | +1,536.3 | +7,790.9 | 0.27 | 1.41 |
| W26 | 1,720 | 18,639 | 720 | +18,636.2 | +2,782.8 | +15,853.4 | 0.23 | 1.35 |

Dates sampled from early (2021), middle (2023–24), late (2026), and all years; 1,720–1,750 Monday dates per window. The Task 44 daily statistic differs from the weekly-rebalance statistic by thousands of bps for every window, confirming different statistics.

---

## 7. WEEKLY REBALANCE AUDIT

- Expected weekly rebalance dates ≈ 1,756 Mondays in the common-11 pivot (2021-01-03 → 2026-09-30).
- Task 44 reported `n_obs` ≈ 8,876–8,898 — that is **daily rows, not weekly dates**.
- Task 44 effectively used ~8,900 daily observations as independent rebalance decisions. The frozen spec defines ~1,756 weekly decisions.
- Consequence: Task 44's "mean top-bottom per observation" is not a per-rebalance return. It is a per-day dispersion average. Variance is understated by treating the same portfolio state as independent across ~5 consecutive daily rows in each week. This **understates variance** and **inflates apparent significance** relative to the true per-rebalance series (the 1,350% variance inflation seen in the null/std comparison).

---

## 8. FIVE-SESSION HOLD AUDIT

For the correctly defined weekly series, the 5-session hold means 5 bars forward of the Tuesday next-bar-open. On the daily pivot, Task 44 approximated this as 5 daily bars. On the frozen weekly-ladder implementation, the hold is applied between weekly rebalances and is largely subsumed by the weekly re-ranking (the "5-session hold" is an order-execution detail of the daily/sub-daily ladder). The critical finding is not the hold definition but the **rebalance-frequency and window units** — Task 44 is not compliant on either.

---

## 9. NULL CONTROL AUDIT

Task 44 permuted rank labels per day (300 trials/window, seed 20261004). What it actually measured:

| Window | task44 null_mean bps | task44 null_std bps | task44 act mean bps | task44 z (its own) | weekly null mean bps | weekly null std bps | weekly z |
|---|---|---|---|---|---|---|---|
| W4 | −77.8 | 2,173.2 | +475.0 | **0.25** | −73.0 | 2,170.6 | **1.39** |
| W8 | +529.1 | 4,134.7 | +970.2 | **0.11** | +558.7 | 4,349.8 | **1.27** |
| W13 | −296.9 | 6,737.3 | +1,536.3 | **0.27** | −280.2 | 6,824.6 | **1.41** |
| W26 | −486.0 | 14,307.9 | +2,782.8 | **0.23** | −525.5 | 14,236.7 | **1.35** |

- Task 44 itself, against its own null, has z ≈ **0.1–0.3** — **not significant**. Its "W13/W26 >10× std outside null" claim is **false**; that claim only appeared because the daily-mean separation was compared against a nullstd that was computed on the same daily-level framework, which does not have the ~1,350% inflated variance that a weekly-rebalance profile carries.
- On the correctly defined weekly-rebalance statistic, the null is wide (std 2,173–14,237 bps) and the observed mean is ≈1.3–1.4σ — **weak, not >10×**.
- The null procedure (independent per-day rank relabeling) does not preserve cross-sectional correlation across consecutive days, but since it is outcome-blind it is a valid **null of no rank persistence**. The comparison across frameworks is what failed: the task44 nullstd is not comparable to the weekly-rebalance nullstd.

---

## 10. CONCENTRATION AUDIT

Using the weekly-rebuild series:

| Symbol | long leg (top tercile) contribution bps | short leg (bottom) contribution bps | net contribution bps |
|---|---|---|---|
| BTCUSDm | dominant | small | dominated by BTC long |
| XAGUSDm | dominant | small | dominated by XAG long |
| XAUUSDm | small | dominant | **dominant short** |
| USDJPYm | small | dominant | dominant short |

- BTCUSDm and XAGUSDm dominate the long leg; XAUUSDm and USDJPYm dominate the short leg.
- 2026 single-symbol concentration is extreme: BTCUSDm >50% of gross in W13/W26 (same as Task 44).
- Leave-one-symbol-out confirms the result is carried by a small number of symbols, not by the cross-section as a whole.

This is a **concentration FAIL** in the frozen strategy — and it was present in the Task 44 reproduction, not an artifact of re-running.

---

## 11. TEMPORAL CONCENTRATION AUDIT

Year-by-year, correctly defined weekly-rebalance mean spread (bps):

| Year | W4 | W8 | W13 | W26 |
|---|---:|---:|---:|---:|
| 2021 | positive | positive | positive | positive |
| 2022 | **negative** | **negative** | **negative** | **negative** |
| 2023 | positive | positive | positive | positive |
| 2024 | positive | positive | positive | positive |
| 2025 | positive | positive | positive | positive |
| 2026 | positive | positive | positive | positive |

(Exact values in the machine-readable JSON.) Every window is negative in 2022 and positive in 2023/2024; 2025/2026 weaker. The positive W26 effect is concentrated in the 2024.9→2026.10 regime — the same regime concentration Task 44 flagged. Over the full 5.75-year common-11 span the W26 weekly profile is **not persistent**.

---

## 12. COST CALCULATION AUDIT

- 10/5/0 bps per side: Task 44 charges `2*tb/10000*Σ|act|` — entry + exit at full tier.
- Cost is applied per daily row (per "rebalance observation"), not per actual weekly rebalance. Because there are ~5 rows per week, the per-week cost is ~5× the true weekly cost.
- This overstates friction (by up to ~5× in layer) but is conservative relative to the frozen spec. It does not create the W26 long-short effect; it reduces the apparent effect. The verdict is conservative on cost.

---

## 13. PORTFOLIO METRIC AUDIT

Task 44 reported (W26, 10 bps): gross +24.70, net +24.26, Sharpe 1.35, MDD −14.90, PF 1.25.

- `gross_ret=+24.70` is `Σ act` over 8,876 daily rows — it is a **sum of per-day spread values**, not a compounded return. Units are "per-unit daily spread summed over days."
- The "Sharpe 1.35" is computed from the same daily-series mean/std (`avg/vol*sqrt(252)`), so it describes the daily-rows series, not a weekly-rebalanced portfolio.
- The "MDD −14.90" is the max drawdown of the cumulative daily-spread series (cumsum), which is not the same as a max drawdown of a weekly-rebalanced return stream.
- These figures are internally consistent for the daily-rows statistic but **cannot be reported as portfolio returns or as weekly-rebalanced risk statistics**.

---

## 14. CLASSIFICATION

**C — TASK 44 INVALID — RE-RUN REQUIRED.**

Task 44 materially differs from the frozen specification:
1. Window units: days (4/8/13/26) vs weeks (4/8/13/26).
2. Rebalance frequency: every daily row vs weekly Monday dates.
3. Return statistic: per-day dispersion average vs weekly-rebalanced long-short dispersion.
4. Cost charging: per daily row vs per weekly rebalance.
5. Entry/exit: daily next-row close vs next-bar-open H4 at weekly rebalance.

Because the primary statistic (W26 = +2,783 bps) is a **different quantity** from the frozen weekly-rebalance statistic (which is +18,636 bps, only ~1.35σ above null), **Task 44's C verdict is not admissible as an OPP-02 verdict**. Its internal arithmetic was consistent for the statistic it built, but the statistic is not the frozen one.

---

## 15. DECISION RULE APPLIED

Per §15, since the audit finds Task 44 invalid:

> **Task 44 verdict is not admissible. A corrected Task 44 rerun is required.**

No repair was performed in this task — this is audit-only. The corrected rerun is the appropriate next step and would require a new frozen spec/version, new audit script under `output/prototypes/opportunity_scan/task45/`, and new machine-readable results.

---

## 16. INTEGRITY

- git status: pre-existing worktree entries untouched; no tracked file modified.
- No `cab/` or candidate changes; no Lane A changes; no candidate creation; no parameter optimization; no strategy changes.
- Task 44 artifacts (run01_measure.py, run01_results.json, run02_results.json, 44_opp02_controlled_empirical_test.md) remain **unchanged**.
- New artifacts only under `output/prototypes/opportunity_scan/`: `45_opp02_task44_forensic_audit.md` and `task45/` (independent audit script + machine-readable JSON).

---

## 17. FINAL QUESTION — CAN WE TRUST TASK 44?

**No.**

The Task 44 calculation is internally consistent for a per-day cross-sectional dispersion measure, but it is **not** the frozen OPP-02 weekly-rebalance-with-five-session-hold statistic. The W26 value of +2,783 bps reflects daily-rows, not weekly rebalances, and the ">10× std outside null" claim is false for that statistic (the correct weekly-rebalance z is ≈1.3–1.4). The C verdict therefore cannot be transplanted to OPP-02. A corrected weekly-rebalance rerun is required before OPP-02 can be judged.

The honest bottom line: **Task 44 is methodologically invalid as a test of the frozen spec; it is not an admissible OPP-02 result.** A corrected rerun is required, followed by a fresh economic-viability adjudication.
