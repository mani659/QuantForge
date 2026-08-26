# QuantForge — RESEARCH FACTORY V2
# G1 RESULT INTEGRITY AUDIT

## 1. Executive Verdict

**OVERALL G1 INTEGRITY: INVALID**

The G1 Economic Plausibility Screen (`RESEARCH_FACTORY_V2_G1_SCREEN_20260825.md`) contains a severe, systemic methodological failure across all four candidates. The reported "gross opportunities" do not represent executable trade paths. In every candidate, the implementation script (`g1_screen.py` and `g1_screen_2.py`) calculated the **Maximum Favorable Excursion (MFE)** over the holding period, assuming perfect foresight to exit at the absolute peak price. Furthermore, for breakout candidates, the script assumed entry at the pre-breakout close price, thereby falsely claiming the breakout threshold distance as captured profit. 

All four candidates must be rejected from G2 promotion under this specific evidence. 

## 2. G1 Report Identity

- **Source Report:** `output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260825.md`
- **Execution Scripts:** `g1_screen.py` and `g1_screen_2.py`
- **Audit Type:** Read-Only Independent Integrity Audit

## 3. Script Trace

The audit traced the exact Pandas operations applied in the Python scripts to generate the reported 88.16, 9.70, 115.19, and 11.46 bp figures.

- **CAND-G0-001:** `exc = (p_future / p0 - 1).abs().max() * 10000`
- **CAND-G0-002:** `exc = (l['max'] / l['first'] - 1) * 10000`
- **CAND-G0-003:** `max_exc = (p_future / p0 - 1).abs().max() * 10000`
- **CAND-G0-004:** `excursions.append(exc.max())`

In every case, the script computes the `.max()` of the forward window. This calculates MFE, not executable return.

## 4. Candidate Entry Audit

### CAND-G0-001 (Volatility Spillover)
- **Defined Entry:** Straddle or breakout entry.
- **Implemented Entry:** Close of the 1H shock bar (`p0`).
- **Entry Problem:** The script enters at `p0` and takes the absolute maximum excursion (`abs().max()`) of the next 4 hours. This entirely ignores the required price movement needed to trigger a breakout or straddle, capturing the "breakout distance" for free.
- **Exit Problem:** Exits at the perfect absolute peak within 4 hours.
- **Pre-Entry Excursion Included?** YES.

### CAND-G0-002 (Session-Transition Imbalance)
- **Defined Entry:** Breakout of Asian range.
- **Implemented Entry:** Close of the first London hour (`l['first']`).
- **Entry Problem:** Entry is delayed to the close of the 08:00 hour, which correctly excludes pre-entry movement, but...
- **Exit Problem:** Measures from `l['first']` to `l['max']` (the highest/lowest point of the entire London session) rather than the London close (`l['last']`) as defined in G0. 
- **Pre-Entry Excursion Included?** NO. But exit is impossible.

### CAND-G0-003 (Nested Volatility Compression)
- **Defined Entry:** Stop-entry on H4 range breakout.
- **Implemented Entry:** Close of the H1 compression bar (`p0`).
- **Entry Problem:** Fails to require price to actually break the H4 range. Enters at the immediate H1 close and magically captures the absolute maximum move in whichever direction goes furthest (`abs().max()`). 
- **Exit Problem:** Perfect exit at the 3-day peak.
- **Pre-Entry Excursion Included?** YES.

### CAND-G0-004 (Volume-Impact Reversal)
- **Defined Entry:** Close of the 5-min anomaly bar.
- **Implemented Entry:** Correctly implemented at the close (`p0`).
- **Exit Problem:** Computes `exc.max()` over the 60-minute window, assuming perfect exit at the peak of the reversion, not at the end of the 60-minute holding period.
- **Pre-Entry Excursion Included?** NO. But exit is impossible.

## 5. Gross Opportunity Reconstruction

None of the reported gross opportunity figures (88.16, 9.70, 115.19, 11.46 bps) are valid. They are maximum excursions, which routinely overstate true executable returns by 3x to 10x. Realizable gross returns based on the defined end-of-horizon exits would be substantially lower and potentially negative net of friction.

## 6. Friction Audit

- **BTCUSD (5.0 bps):** PLAUSIBLE.
- **EURUSD (1.5 bps):** PLAUSIBLE.
- **XAUUSD (3.0 bps):** PLAUSIBLE.
- **Verdict:** The friction assumptions themselves were reasonable and appropriately conservative for a G1 screen. The failure is entirely in the gross opportunity numerator.

## 7. Frequency/Turnover Audit

- **CAND-G0-003 Sampling Error:** The script arbitrarily down-sampled events for speed (`events = events[::10]`) and then multiplied the resulting event count by 10 (`len(events)*10`). While explicit, this is an improper sampling technique for measuring low-frequency nested compressions.

## 8. Data Integrity

- The script correctly constrained itself to the `data/m1/` directory. No Parquet or tick data was used. Data integrity rules were followed.

## 9. Parameter Integrity

- **Hidden Parameter in CAND-G0-002:** The G0 definition required "linear R-squared > 0.85". The G1 script substituted this with an "Efficiency Ratio > 0.6" (`er = net / ret`). This is an unapproved parameter substitution.

## 10. Candidate Verdicts

- **CAND-G0-001:** INVALID G1.
- **CAND-G0-002:** INVALID G1.
- **CAND-G0-003:** INVALID G1.
- **CAND-G0-004:** INVALID G1.

## 11. G2 Readiness

- **CAND-G0-001:** G2-KILL (Based on this screen).
- **CAND-G0-002:** G2-KILL.
- **CAND-G0-003:** G2-KILL.
- **CAND-G0-004:** G2-KILL.

*(Note: The candidates themselves might still be theoretically interesting, but their advancement to G2 is halted until a valid G1 screen proves they possess actual executable headroom, not MFE.)*

## 12. Research Factory Lesson

This audit highlights the most common illusion in quantitative screening: **The MFE Trap**. Measuring the `.max()` of a forward window assumes the trader possesses a time machine. Furthermore, measuring absolute return (`abs().max()`) assumes the trader also possesses a directional oracle. A valid screen must measure from a realistic entry trigger to a deterministic, rule-based exit (e.g., end of holding period or trailing stop logic).

## 13. Integrity

- No G2 empirical pilot was executed.
- No source code, tick datasets, or Parquet files were touched.
- No parameters were tuned.
- The results of the previous G1 screen were invalidated based strictly on read-only methodological trace.
