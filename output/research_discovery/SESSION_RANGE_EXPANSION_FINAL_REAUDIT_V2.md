# QUANTFORGE — SESSION-ANCHORED RANGE EXPANSION FINAL RE-AUDIT V2

## 1. Executive Verdict

**CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED**

The v1.1.2 protocol is scientifically sound, outcome-blind, and fully deterministic in its scientific core: session boundaries, normalization, rolling-percentile classifier, control group, primary response, median convention, stationary-bootstrap mechanics, inference, falsification, and all firewalls are correctly and completely specified. The v1.1.1 sequence-length termination and the v1.1.2 continuation-probability and primary-response timestamp wording are correctly implemented.

However, under the strict adversarial standard ("another researcher must implement this from the protocol alone without asking what was meant"), **four precision items remain non-unique in the current text**, two of which are explicitly called out by the audit mandate:

1. **Session completeness (§4/§16):** the word "continuous" is internally inconsistent with the only operational gate (fewer-than-200-bars), and the §4 parenthetical's arithmetic for its own example (13:00 ET early close) is wrong.
2. **Rolling-percentile position convention (§7):** "standard linear interpolation (e.g., `i + (j - i) * fraction`)" does not pin how (i, j, fraction) are derived from q and n; two common libraries produce different 25th-percentile thresholds from the same 63 values.
3. **Secondary directional tie case (§11):** the exact-0 direction case (`Close_16:00 == Open_09:30`) is unspecified.
4. **Chronological half split (§14):** "mechanically split into chronological halves" does not state observation-count split vs. date midpoint.

All four are deterministic and uniquely resolvable wording items — none requires a new scientific or statistical decision. Per the governing rule, **no execution is authorized from this verdict.** Execution may be authorized only after the corrections below are applied and pass a final re-audit.

## 2. Scientific Object

**PASS.** The primary question is exactly:

> Does extreme pre-session range compression reliably precede larger cash-session range expansion than the non-compressed control group?

The protocol (§2, §17–§21) confirms: behavioral hypothesis of volatility-state transition; not a trading strategy; zero PnL/expectancy/spread/slippage/Sharpe; not return prediction; distinct from mean reversion, 12/1 TSMOM, H01 leverage/asymmetry, K-means, and ML (§11 of the definition lock). The clean later path is preserved: behavior validation → strategy research → economic validation → demo → forward statistical monitoring → live consideration (§15 of the definition lock; §18/§20/§21 of the protocol).

## 3. Session Boundary Verification

**PASS** (all arithmetic verified independently):

- **Pre-session:** 18:00:00 ET (prior day) through 09:29:00 ET (current day) **inclusive** = 18:00–23:59 (360 bars) + 00:00–09:29 (570 bars) = **930 M1 timestamps**. Correct.
- **Cash session:** 09:30:00 ET through 16:00:00 ET **inclusive** = 09:30–09:59 (30) + 10:00–15:59 (360) + 16:00 (1) = **391 M1 timestamps**. Correct.
- **Zero overlap:** pre-session terminal timestamp is 09:29:00; cash first timestamp is 09:30:00. Zero overlap. Correct.
- **DST:** mapped via `America/New_York` standard timezone conversion, automatic DST (§3). Correct.
- **Prior-day crossing:** the window crosses midnight by construction; the rule "prior-day 18:00 → current-day 09:29" is unambiguous for any event day.
- **Monday handling:** for a Monday event day, the literal "prior day" is Sunday; the pre-session window therefore spans Sunday 18:00 ET → Monday 09:29 ET. If the dataset contains no Sunday bars, the window degenerates deterministically to Monday 00:00–09:29. The protocol requires no minimum pre-session bar count, so execution is deterministic under either data condition. **Clarification note only — no new decision required.**
- **16:00 dual role:** 16:00 is both the terminal response timestamp and the mandatory denominator close (§9). The cash high/low explicitly includes all timestamps from 09:30:00 through 16:00:00 inclusive (§9, fixed in v1.1.2). No "strictly between" language remains in the protocol.

## 4. Continuity / Completeness Verification

**REAL FINDING — REQUIRED CORRECTION (item 1).**

The protocol contains two non-equivalent statements:

- §4: "A valid event day must contain a **continuous** cash session from 09:30 ET to 16:00 ET. Standard market early-close days (e.g., day after Thanksgiving closing at 13:00 ET) **which produce fewer than 200 M1 bars** are explicitly dropped."
- §16: "If **fewer than 200 M1 bars** exist in the 391-timestamp cash session window, the day is flagged as a potential half-day/holiday and explicitly dropped."

Only one executable test exists (the <200-bar gate); no internal-gap detection test is specified anywhere. The audit mandate explicitly forbids silently choosing between (A) minimum-coverage and (B) true continuity:

- Under (A), a day with 300 bars and a 90-minute internal gap **passes** and enters the sample.
- Under (B), that day **fails** — but implementing (B) requires a gap-detection rule (expected timestamp set / max-gap / duplicate treatment) that the protocol does not state, i.e., a new implementation decision.

**Arithmetic error in §4:** a 13:00 ET early-close day contains 09:30:00–13:00:00 inclusive = 30 + 180 + 1 = **211 bars**, which is **greater than 200**. The §4 parenthetical's claim ("which produce fewer than 200 M1 bars") is therefore false for its own example, and the <200-bar gate does **not** drop 13:00 closes. Such days are nevertheless excluded deterministically by the independent §16 rule (missing `Close_16:00` → invalid day). The operational outcome is correct, but the stated rationale is not; the same arithmetic error appears in PROTOCOL_AUDIT_V1 §14 and FINAL_REAUDIT_V1 §4 ("flawlessly rejects early closes").

**Unique resolution (deterministic, no new science):** pin §4 to state that the <200-bar minimum-coverage rule is the **sole** session-completeness gate; "continuous" is descriptive; internal gaps do not invalidate a day that has ≥200 bars in the window and valid terminal closes; and correct the early-close example (early-close days are dropped by the missing-16:00-close rule, not by the bar-count gate).

## 5. Normalization

**PASS.**

- **Pre-session:** `Normalized_R_pre = R_pre / Close_09:29`; numerator = High−Low over 18:00:00–09:29:00 inclusive; denominator = close of the final pre-session bar (09:29:00). Denominator ≤ 0 or missing → day invalid, dropped from state calculation (§6).
- **Response:** `Normalized_R_cash = (High_cash − Low_cash) / Close_16:00` with identical rigor; denominator ≤ 0 or missing → day invalid, dropped from the primary response (§9, §16). The v1.1.0 correction (explicit `Close_16:00` zero/missing rule) is present.
- **No look-ahead:** the state uses only bars through 09:29:00; the denominator for the state is the 09:29:00 close; no response-window bar enters the state. Correct.
- **Invalid denominator source:** any bar with price ≤ 0 invalidates the day (§16), so the denominator cannot come from an invalid bar. Duplicate timestamps: first retained, duplicates dropped (§16). Correct.

## 6. Rolling Percentile Mathematics

**REAL FINDING — REQUIRED CORRECTION (item 2).**

- Trailing window: exactly 63 **prior valid** days; current day excluded; threshold recomputed day by day from history only; invalid days cannot enter history; first 63 valid days are initialization-only and cannot generate events; fewer than 63 valid history days → day dropped (§7). All PASS.
- Classifier: COMPRESSED iff `Normalized_R_pre ≤` trailing 25th-percentile threshold (§7). PASS.
- **Interpolation:** §7 states "Standard **linear interpolation** is used (e.g., `i + (j - i) * fraction`)." This formula pins the interpolation step only; it does **not** pin how (i, j, fraction) are derived from q and n. The audit mandate requires: "If two common libraries can produce different 25th-percentile thresholds from the same 63 values under the protocol wording, classify this as a correction requirement."

  Verified divergence for n = 63, q = 0.25:
  - numpy `percentile(x, 25, method='linear')` (default; R type 7; Excel PERCENTILE.INC): one-based position 1 + q·(n−1) = 16.5 → interpolate between the 16th and 17th order statistics.
  - Python `statistics.quantiles(x, n=4)` (default method 'exclusive'; R type 6; Excel PERCENTILE.EXC): position q·(n+1) = 16 → the 16th order statistic exactly.
  
  These differ materially for a boundary day. The repository's own convention is numpy-default (`np.percentile` throughout `output/tsmom_*`, `event_study_*`, `xagusd_cost_viability_v1`), and PROTOCOL_AUDIT_V1 §5 originally specified "`linear` as per numpy default" — but the v1.1.x protocol text dropped the "numpy default" qualifier, leaving the position convention unpinned.

  **Unique resolution (deterministic, no new science):** pin the convention explicitly, e.g., "numpy `method='linear'` (equivalently R type 7 / Excel PERCENTILE.INC): one-based position 1 + q·(n−1); i = floor(position), j = ceil(position), fraction = position − floor(position); for n = 63 and q = 0.25, position = 16.5, i.e., the average of the 16th and 17th order statistics of the 63 sorted values; duplicate values handled naturally by the sorted order."

## 7. Control Group

**PASS.** CONTROL = every otherwise-valid day with `Normalized_R_pre >` the rolling 25th-percentile threshold (§8). Mutually exclusive with COMPRESSED; collectively exhaustive over valid classified days; no second threshold; no response-based exclusion; no volatility-based post-classification filtering. Correct.

## 8. Primary Response

**PASS.** `Normalized_R_cash = (High_cash − Low_cash) / Close_16:00`; high/low computed from all M1 observations with timestamps 09:30:00 through 16:00:00 inclusive (§9, v1.1.2 wording); terminal close mandatory; zero/negative/missing denominator → day invalid; complete-day requirement via §16 gates; state and response do not overlap (state ends 09:29:00, response begins 09:30:00). Correct.

## 9. Primary Statistic

**PASS.** ΔM = median(COMPRESSED response) − median(CONTROL response) (§10). Median convention explicitly registered: arithmetic mean of the two central ordered observations for an even-sized sample — unique for any sample size an executor might encounter. NaN/invalid observations cannot enter (invalid days dropped). State labels attached to days from chronological construction; no response-dependent reclassification. ΔM computed inside each bootstrap iteration with fixed labels (§10, §12). Correct.

## 10. Stationary Bootstrap Mathematics

**PASS** — the highest-priority section verifies cleanly:

- Geometric block lengths with p = 1/L = 0.1; **expected block length = 1/p = 10**. The mechanics (emit observation; then terminate with probability p = 0.1; continue with probability 1 − p = 0.9; on termination start a new block at a uniformly selected observation; continuation advances chronologically and wraps circularly at the end) imply exactly Geometric(p) block lengths with mean 10 — consistent with the prose, the parameter table, and the v1.1.2 version note. No contradiction between prose, parameter table, version history, and mechanics.
- Exact algorithm verified for every replicate: (1) first block start uniform; (2) emit current observation; (3) draw termination decision; (4) if terminate, choose new start uniformly; (5) else advance chronologically, wrapping at the end of the valid sequence; (6) continue until length ≥ N; (7) truncate the final sequence to exactly N (v1.1.1).
- N = the original number of valid day-level observations; N fixed across replicates, never recomputed inside a replicate; no selective pre-truncation removal; no imputation; state labels remain attached to sampled tuples.
- The 63-day rolling classifier is **not** rerun on bootstrap samples; COMPRESSED/CONTROL labels are never recomputed from resampled data (§10, §12).
- Sampling unit = day-level tuples `[Normalized_R_cash, State_Label]`, not raw M1 bars (§12). Correct.

## 11. RNG / Replicate Mechanics

**PASS.** Fixed seed 20260817; fixed B = 10,000; fixed algorithm; no hidden random initialization. Byte-identical PRNG across languages is not required (and the protocol does not claim it); the bootstrap algorithm itself is unambiguous (given the item-2 correction above, which does not touch RNG).

## 12. Confidence Interval / Decision Rules

**PASS.** Two-sided 95% percentile CI of the bootstrap ΔM distribution: lower = 2.5th percentile, upper = 97.5th percentile (unique for a two-sided 95% percentile interval). CI computed from bootstrap ΔM values; no null transformation; no studentization; no correction needed because the confirmatory family size is exactly 1 (§13). SUPPORT if lower CI > 0; CONTRADICTED if upper CI < 0; INCONCLUSIVE if CI includes 0 (§17). α = 0.05 (frozen table). No wording implies a practical trading threshold — a tiny positive ΔM may support the behavioral hypothesis even if economically unusable later, which is intentional.

## 13. Chronological Stability

**REAL FINDING — REQUIRED CORRECTION (item 4).**

- Full sample = sole confirmatory analysis; chronological halves = descriptive only; halves cannot change the primary classification; no post-result deletion (§14, §15). PASS.
- **Split rule unspecified:** §14 says only "mechanically split into chronological halves." Two implementations differ: observation-count split (first floor(N/2) chronological observations, remainder second) vs. date midpoint. Descriptive-only, so not verdict-affecting, but under the strict standard the rule must be pinned.

  **Unique resolution:** "split the N day-level observations in chronological order: the first floor(N/2) observations form the first half; the remaining N − floor(N/2) form the second half."

## 14. Secondary Firewall

**REAL FINDING — REQUIRED CORRECTION (item 3).**

- Direction strictly defined as sign of (`Close_16:00 − Open_09:30`): UP if > 0, DOWN if < 0 (§11). PASS.
- Persistence: UP requires `Close_16:00 ≥ Low_cash + 0.75 × Range_cash`; DOWN requires `Close_16:00 ≤ High_cash − 0.75 × Range_cash`; `Range_cash = High − Low`. PASS.
- Zero range → diagnostic NaN, excluded from the secondary denominator. PASS.
- **Exact-0 direction case unspecified:** if `Close_16:00 == Open_09:30`, the session is neither UP nor DOWN; the protocol does not state the treatment. Descriptive-only.

  **Unique resolution:** "if `Close_16:00 == Open_09:30`, the session is directionless; the diagnostic is NaN and excluded from the secondary denominator (same treatment as zero range)."

- Firewall: purely descriptive; cannot rescue a failed primary nor change the verdict (§11). No hidden strategy test. PASS.

## 15. Data Quality / Stopping

**PASS** (with the item-1 correction incorporated for the completeness gate).

- Duplicates: first retained, rest dropped. Invalid prices (≤ 0): day invalid. Missing 09:29:00 or 16:00:00 close: day invalid. Incomplete sessions / early closes: dropped (via missing terminal close; bar-count gate for low-coverage days). Weekends filtered. Holidays: handled by the completeness/close rules. DST: automatic via timezone conversion. Zero-range days: not invalid — valid days with Range_cash = 0 enter the primary response normally (zero-range only affects the secondary diagnostic). Internal gaps: allowed under the <200 minimum-coverage reading (item 1).
- Stopping rule (§22): denominator = "total calendar days containing at least one M1 bar," explicit; numerator = days flagged invalid by the data-quality gates; duplicates deduplicated so each calendar day counts once; initialization-only days are valid (not flagged), so they count in the denominator but not the numerator; stopping is assessed **before** primary inference ("execution must STOP and trigger an anomaly audit before inference is computed"). Correct.

## 16. Economic Firewall

**PASS.** The protocol contains zero entry/exit rules, direction trading rules, stop-loss, take-profit, position sizing, spread, slippage, PnL, Sharpe, or expectancy calculations (§18, §20). A positive result leads to a separate strategy-translation stage (§14 of the definition lock; §20). Correct.

## 17. K-Means / ML Firewall

**PASS.** K-means is excluded from the primary; the deterministic rolling-percentile classifier is the only primary classifier; no clustering parameter can be inserted post-outcome (§19). The exclusion of K-means from this specific test is not a rejection of ML as a broader research direction (definition lock §7 rejects K-means for this specific 1-D classification, not ML generally); future K-means/ML research remains possible as a separately registered study. Correct.

## 18. Outcome-Blindness

**PASS.** Full text scan of the protocol: zero effect values, zero p-values from results, zero PnL, zero expectancy, zero favorable dates, zero strategy results, zero K-means outputs, zero performance-derived parameter choices. §24 states the outcome-blind self-audit declaratively, which is permitted. Parameters (63, 25%, 09:30) are standard quarter/quartile choices frozen before any data inspection (definition lock §20).

## 19. Executor Checklist

| Item | Fully specified? | Material ambiguity? | Unique resolution? |
| :--- | :--- | :--- | :--- |
| Timezone conversion (`America/New_York`, auto DST) | Yes | No | N/A |
| Pre-session boundaries (18:00:00 prior → 09:29:00 inclusive) | Yes | No | N/A |
| Cash-session boundaries (09:30:00 → 16:00:00 inclusive) | Yes | No | N/A |
| Timestamp counts (930 pre / 391 cash) | Yes | No | N/A |
| Session completeness ("continuous" vs <200 gate) | No | **Yes** | **Yes (item 1: <200 gate is sole test; internal gaps allowed; fix early-close arithmetic)** |
| Internal gap handling | No | **Yes** | **Yes (item 1: no gap test; gaps do not invalidate)** |
| Normalization (both R_pre and R_cash) | Yes | No | N/A |
| 63-day history (prior valid days only, init-only) | Yes | No | N/A |
| Percentile position formula | No | **Yes** | **Yes (item 2: numpy method='linear' / R7, position 1 + q·(n−1))** |
| Linear interpolation | Partial | **Yes** | **Yes (item 2)** |
| Compression threshold (≤ 25th percentile) | Yes | No | N/A |
| Control group (all non-compressed valid days) | Yes | No | N/A |
| Primary response (09:30–16:00 inclusive, Close_16:00) | Yes | No | N/A |
| Median convention (even-sample arithmetic mean) | Yes | No | N/A |
| Bootstrap sampling unit (day tuples) | Yes | No | N/A |
| p = 0.1 termination probability | Yes | No | N/A |
| 0.9 continuation probability | Yes | No | N/A |
| Block start selection (uniform) | Yes | No | N/A |
| Circular continuation (wrap at end) | Yes | No | N/A |
| Replicate length N (original valid count) | Yes | No | N/A |
| Final truncation to exactly N | Yes | No | N/A |
| State-label behavior (fixed, not recomputed) | Yes | No | N/A |
| RNG (seed 20260817, B = 10,000) | Yes | No | N/A |
| CI (two-sided 95% percentile, 2.5/97.5) | Yes | No | N/A |
| Chronological halves (count vs date split) | No | **Yes** | **Yes (item 4: first floor(N/2) by chronological order)** |
| Secondary directional metric (zero-direction case) | No | **Yes** | **Yes (item 3: directionless → NaN, excluded)** |
| Stopping denominator (days with ≥1 M1 bar) | Yes | No | N/A |

## 20. Findings

1. **§4/§16 session completeness (material, wording).** "Continuous" vs. the <200-bar gate are non-equivalent; only the gate is operational; a 300-bar day with a 90-minute gap is included under the gate. Additionally, the §4 parenthetical is arithmetically wrong (13:00 close = 211 bars, not <200); early closes are actually dropped by the missing-16:00-close rule. Same arithmetic error in PROTOCOL_AUDIT_V1 §14 and FINAL_REAUDIT_V1 §4.
2. **§7 percentile position convention (material, wording).** The interpolation formula alone does not pin the position convention; numpy 'linear' (R7) and statistics.quantiles 'exclusive' (R6) yield different 25th-percentile thresholds for n = 63. The audit mandate classifies this as a correction requirement.
3. **§11 secondary exact-0 direction (minor, wording).** `Close_16:00 == Open_09:30` case unspecified; descriptive-only.
4. **§14 chronological half split (minor, wording).** Observation-count vs. date-midpoint split unspecified; descriptive-only.
5. **Definition-lock residual wording (non-blocking consistency note).** Definition lock §5 states R_pre "strictly between 18:00 ET and 09:30 ET" and §4 ends the pre-session at "09:30 ET," which are endpoint-inconsistent with the protocol's inclusive 18:00:00–09:29:00 (the lock would exclude the 18:00 bar and nominally touch the cash start). The protocol v1.1.2 is authoritative and internally consistent; recommend aligning the lock's wording so the two documents agree exactly.
6. **Monday pre-session (clarification note).** Literal "prior day" = Sunday; the window deterministically spans Sunday 18:00 ET → Monday 09:29 ET, degenerating to Monday 00:00–09:29 if no Sunday bars exist. No minimum pre-session bar count is required; no new decision needed.

No scientific or statistical decision is unresolved. All findings are deterministic, uniquely resolvable wording items.

## 21. Required Corrections

The execution spec must adopt the following four binding wording corrections (no scientific or statistical change):

1. **§4 — Session completeness:** State that the fewer-than-200-bars rule is the **sole** session-completeness gate (minimum coverage, not true contiguity); internal gaps do not invalidate a day with ≥200 bars in the 391-timestamp window and valid terminal closes; correct the early-close example (13:00 ET close = 211 bars; such days are dropped by the missing-16:00-close rule, not the bar-count gate).
2. **§7 — Percentile convention:** Pin the exact quantile method — numpy `method='linear'` (R type 7 / Excel PERCENTILE.INC): one-based position 1 + q·(n−1), i = floor(position), j = ceil(position), fraction = position − floor(position); for n = 63, q = 0.25 → position 16.5 (average of the 16th and 17th order statistics); duplicate values handled by sorted order.
3. **§11 — Secondary exact-0 direction:** If `Close_16:00 == Open_09:30`, the session is directionless; the diagnostic is NaN and excluded from the secondary denominator (same treatment as zero range).
4. **§14 — Chronological half split:** Split the N day-level observations in chronological order — first floor(N/2) observations = first half; the remainder = second half.

Non-blocking consistency note: align the definition-lock wording (§4 "to 09:30 ET," §5 "strictly between 18:00 ET and 09:30 ET") with the protocol's inclusive 18:00:00–09:29:00 bounds.

## 22. Final Execution Recommendation

**CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED.** The four corrections above are deterministic and uniquely resolvable; none requires a new scientific, statistical, mathematical, or implementation decision. Per the governing rule, **no execution is authorized by this verdict.** After the corrections are applied, a final re-audit is required before execution is authorized.

## 23. Integrity

- Strictly read-only: no file modified; no script written; no data processed beyond schema-level inspection (column order, timestamp convention, row count, coverage window of `data/m1/USATECHIDXUSD_M1.csv`).
- No ΔM, percentile, CI, bootstrap, PnL, expectancy, or Sharpe computed.
- No outcome inspection; no parameter tuning; no market/session/threshold change; no hypothesis change.
- The only new artifact is this audit report.
- Facts are labeled by document reference; all arithmetic (930, 391, 211, 1 + q·(n−1), expected block length 10) was verified independently.
