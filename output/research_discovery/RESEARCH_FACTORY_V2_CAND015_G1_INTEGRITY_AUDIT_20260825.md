# QUANTFORGE — RESEARCH FACTORY V2
# CAND-G0-015 G1 INTEGRITY AUDIT

## 1. Executive Verdict
**VALID G1**
The G1 implementation for CAND-G0-015 strictly adheres to the frozen G0 definition. All critical economic, executable, and deterministic invariants are satisfied. The conditional asymmetry observed in the low-volatility state is a genuine outcome of the predefined mechanism and not an implementation artifact. 

## 2. Candidate Identity
**CAND-G0-015** — Nasdaq-Crypto Information Absorption Lag

## 3. Event Definition Trace
- **Shock Definition:** The script calculates the M5 ATR(14) and its 30-day (8,640 bar) rolling average strictly using past data. A shock is correctly flagged when the M5 return exceeds 3x this moving average.
- **Completion:** The event completes at the close of the M5 anomaly bar.

## 4. Entry/Exit Trace
- **Entry:** Executed at `btc_close[i]`, representing the exact close time of the USATECHIDXUSD anomaly bar. No look-ahead bias or pre-entry return is included in BTC's return.
- **Direction:** Mapped deterministically from the close-open difference of the anomaly bar.
- **Exit:** Executed at `btc_close[i+12]`, which exactly represents the 60-minute deterministic horizon. It is identical across all states.

## 5. Conditional-State Trace
- **Conditioning KPI:** D1 equity volatility regime. 
- **Integrity:** The D1 ATR and its 30-day SMA are calculated on daily resampled data. Critically, the script applies a `shift(1)` to the daily values before joining them to the M5 timeline. This guarantees that the volatility state for any M5 bar is based strictly on the D1 values that closed the day *before* the trade. There is zero look-ahead bias and no outcome-dependent selection. 

## 6. Opportunity Integrity
- **Lockout Enforcement:** A 60-minute (12-bar) lockout is enforced using `if i < last_event_idx + 12: continue`.
- **Duplicate Suppression:** Overlapping shocks inside the lockout window are correctly incremented to the `lockout_supp` variable and ignored.
- **Result:** The 1,039 valid opportunities represent genuinely independent macro shocks.

## 7. Return Calculation
- Returns are strictly calculated as the deterministic `exit_price` minus `executable entry`.
- No Maximum Favorable Excursion (MFE) is used. No future extrema are involved. 

## 8. Friction
- A static 3.0 bps round-trip friction is applied universally across all states to calculate the Net Return.

## 9. Hidden Parameters
- None. There are no undocumented filters, no event thinning beyond the registered lockout, and no state-specific exclusions.

## 10. Data Integrity
- Data is drawn from local `data/m1/` files and properly resampled to synchronized 5-minute bars via an `inner` join. 

## 11. Economic Result Admissibility
The reported split:
- +9.53 bp mean net in LOW volatility
- -5.63 bp mean net in HIGH volatility
...is a valid consequence of the pre-registered state variable modifying the exact same underlying event object.

## 12. G2 Recommendation
**G2 READY**

## 13. Integrity
The G1 implementation faithfully executes the G0 contract. Opportunity Integrity is preserved. Executable capture is preserved. The result is admissible.
