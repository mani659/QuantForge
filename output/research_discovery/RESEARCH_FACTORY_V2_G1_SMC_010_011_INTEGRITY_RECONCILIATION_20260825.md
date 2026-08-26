# QuantForge — RESEARCH FACTORY V2
# G1 INTEGRITY RECONCILIATION: CAND-010 & CAND-011

## 1. Verdict

**CAND-010:** INVALID G1 (Material implementation divergence, severe event-count anomaly, and hidden parameters).
**CAND-011:** CONDITIONAL (Implementation mostly accurate, but contains a hidden confirmation-window parameter).

## 2. CAND-010 Definition Trace

- **HTF POI:** Defined as `df.resample('D').agg({'high':'max', 'low':'min'}).shift(1)`. Matches frozen definition (Previous day's high or low).
- **FVG/OB Requirement:** None specified in frozen G0 definition; none implemented. Matches.
- **Liquidity Sweep:** Defined as `df_m5['high'] > df_m5['prev_high']`. Matches.
- **CHOCH:** Defined as `row['close'] < row['known_swing_low']` within 24 bars of the sweep. Swings are defined as a 7-bar rolling window centered (3 bars before and after). Matches swing definition, but the 24-bar constraint is an undocumented hidden parameter.
- **Entry:** `entry_price = df_m5_reset.iloc[i+1]['open']`. Earliest observable entry after the CHOCH bar closes. Matches.
- **Exit:** `exit_price = df_m5_reset.iloc[i+24]['close']`. Fixed 2-hour horizon (24 M5 bars). Matches.

## 3. CAND-010 Event-Count Anomaly

The reported 20,726 events is a severe anomaly caused by a state-machine implementation error.
- The `sweep_high` condition evaluates to `True` for *every single M5 bar* whose high remains above the previous daily high, rather than just the initial crossing event.
- Consequently, the `recent_sweep_high_idx` is continuously updated.
- When a CHOCH is found (`close < known_swing_low`), the state is reset, an event is logged, and an entry is generated.
- However, on the very next bar, if the price is still above `prev_high`, `sweep_high` becomes `True` again. If the price also remains below `known_swing_low`, another CHOCH event is instantly triggered.
- This creates massive overlapping cascades of events for a single price move, treating every bar in the post-CHOCH sequence as a new, independent trading event.

## 4. CAND-011 Definition Trace

- **Double Top/Bottom Definition:** 20-bar rolling extrema separated by 20 to 100 bars. Matches.
- **Swing Construction:** `rolling(21, center=True).max()`. Matches.
- **Similarity Tolerance:** `price_diff_pct <= 0.001` (0.1%). Matches.
- **RSI Definition:** Manually computed 14-period RSI. Matches.
- **Divergence Definition:** `rsi_diff >= 5`. Matches.
- **Confirmation / Entry:** Close crosses the 10-period SMA (`close < sma10`). However, the implementation restricts this search to `for j in range(i, i+20)`, enforcing a hidden 20-bar window for the SMA cross to occur.
- **Deterministic Exit:** 4-hour horizon (48 M5 bars). Matches.
- **Mean-Reversion Firewall:** The implementation strictly requires the dual-swing geometric matching and specific divergence. It cannot trigger on pure z-score displacement. It successfully remains a structural divergence object, not generic mean reversion.

## 5. Executable-Capture Check

- **No MFE:** Both candidates correctly compute returns using the deterministic fixed-horizon exit price. No Maximum Favorable Excursion was captured.
- **No Future Extrema:** Swing detection is correctly delayed (shifted by 3 bars for 010, evaluated 10 bars later for 011) to prevent hindsight bias.
- **No Pre-Entry Capture:** Returns are measured exactly from the open/close of the bar following the confirmation signal.

## 6. Parameter Integrity

- **Hidden Parameters Found:**
  - CAND-010: A 24-bar (2-hour) maximum time limit between the HTF sweep and the CHOCH.
  - CAND-011: A 20-bar maximum time limit between the second swing confirmation and the SMA crossing.
- Neither of these time limits were present in the frozen G0 candidate definitions.

## 7. Candidate Verdicts

- **CAND-010:** INVALID G1. The event-count cascade completely invalidates the economic measurement.
- **CAND-011:** CONDITIONAL. The hidden 20-bar confirmation window is a minor discrepancy. The core geometric and momentum logic is intact, and the event count (4,026) is realistic for 5 years of M5 data.

## 8. Economic Result Admissibility

- **CAND-010:** Non-adjudicable. The results are corrupted by overlapping identical events.
- **CAND-011:** Economically insufficient. Even with the minor hidden parameter, the structural double-top + RSI divergence pattern yields a median gross edge of only +0.16 bps, which cannot overcome the 3.0 bps friction barrier. The hypothesis is falsified.

## 9. Next Milestone

> G1 NON-ADJUDICABLE FOR AFFECTED CANDIDATE

## 10. Integrity

- The audit was purely read-only.
- No scripts were repaired or rerun.
- No definitions were modified.
- No G2 pilot was executed.
