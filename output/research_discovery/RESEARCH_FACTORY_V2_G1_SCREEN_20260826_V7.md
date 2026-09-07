# QuantForge — Research Factory V2
# G1 ECONOMIC PLAUSIBILITY SCREEN — V7 CANDIDATES

## 1. G1 Objective
Execute a cheap economic plausibility screen for candidates CAND-G0-018, CAND-G0-019, and CAND-G0-020. The objective is to objectively determine whether each candidate exhibits enough post-entry magnitude and sufficient opportunity frequency to overcome realistic execution friction and justify the computational cost of a G2 empirical pilot.

## 2. Static Integrity Checks
Before execution, a static assertion check was performed on the implementations to prevent the contamination errors of previous cycles:
- **Entry Valid:** YES (Explicitly executable, occurs after event completion).
- **Post-Entry Measurement Valid:** YES (Measured exclusively from executable entry).
- **Exit Deterministic:** YES (Fixed time horizons and session boundaries).
- **No MFE (Maximum Favorable Excursion):** YES.
- **No Hidden Parameters:** YES.
- **No Proxy Substitution:** YES (Exact definitions followed).
- **No Downsampling:** YES.
- **Duplicate Suppression Valid:** YES (Strict lockouts per event logic).
- **No Future Leakage:** YES (KPIs and conditions measured prior to entry).

## 3. CAND-018 Results (Pre-Auction Liquidity Vacuum Reversal)
- **Instrument:** USATECHIDXUSD (M1/M5/D1)
- **Events:** 176
- **Opportunities/Year:** 61.63
- **Mean Gross:** -8.75 points
- **Median Gross:** +9.55 points
- **Win Rate:** 52.84%
- **Max Winner:** 343.80 points
- **Max Loser:** -396.43 points
- **Friction:** 2.0 index points (conservative estimate for NQ CFD round-trip)
- **Median Net:** +7.55 points
- **G1 Verdict:** PASS — MARGINAL. While the median net response is robustly positive (+7.55 points), the negative mean indicates severe left-tail dependency (large losers outweigh winners). A G2 pilot is justified explicitly to test whether strict risk controls (stop losses) can cleanly truncate the negative tail while preserving the positive median expectation.

## 4. CAND-019 Results (Fixed-Income to FX Yield-Shock Transmission Lag)
- **Instrument Required:** US 2Y Treasury Note Futures (or proxy like SHY ETF) & USDJPY
- **Data Availability:** Missing required Fixed-Income benchmark data (US 2Y/SHY) in local M1 repository.
- **Substitution:** PROHIBITED. No silent proxy substitution allowed.
- **G1 Verdict:** BLOCKED — DATA AVAILABILITY.

## 5. CAND-020 Results (Friday Afternoon Positional De-Risking)
- **Instrument:** XAUUSD (M1/H1/D1)
- **Events:** 79
- **Opportunities/Year:** 15.82
- **Mean Gross:** -$1.27
- **Median Gross:** -$0.59
- **Win Rate:** 44.30%
- **Max Winner:** +$52.15
- **Max Loser:** -$63.03
- **Friction:** $0.30 (conservative XAUUSD CFD round-trip)
- **Median Net:** -$0.89
- **G1 Verdict:** INSUFFICIENT. The opportunity frequency is exceedingly low (~16 times per year). Furthermore, both the mean and median gross responses are negative, yielding an economically unviable profile regardless of the friction assumed. The theorized Friday liquidation flow does not predictably manifest as an executable mechanical edge under the strict registered parameters.

## 6. Friction Model
- **USATECHIDXUSD (CAND-018):** Assumed 2.0 index points round-trip. This is a conservative estimate given typical 1.0 - 1.5 pt tight institutional spreads on Nasdaq CFDs. The dataset contains OHLC only; bid/ask was not extracted.
- **XAUUSD (CAND-020):** Assumed $0.30 (30 cents) round-trip. This is conservative relative to standard institutional gold spreads (10-20 cents). Dataset contains OHLC only.

## 7. Opportunity Frequency
- **CAND-018:** ~61 opps/year (Adequate for targeted intraday strategy).
- **CAND-019:** Unknown (Blocked).
- **CAND-020:** ~16 opps/year (Too infrequent for statistical significance over a short period; acts as a disqualifying factor combined with the negative return profile).

## 8. Executable-Capture Verification
- **CAND-018:** Executable entry explicitly taken at the 09:30:00 US/Eastern open print, after the 08:30-09:30 drift condition was fully realized and verified.
- **CAND-020:** Executable entry explicitly taken at the Friday 12:00 NY time open print, measured linearly to the 16:55 NY time close.

## 9. Hidden Parameter Check
Confirmed: NO hidden parameters. Evaluated exact registered horizons and ATR boundaries without post-hoc optimization or threshold scanning.

## 10. G1 Classification
- **CAND-018:** PASS — MARGINAL
- **CAND-019:** BLOCKED
- **CAND-020:** INSUFFICIENT

## 11. G2 Promotions
- **CAND-018 (Pre-Auction Liquidity Vacuum Reversal)**

## 12. G1 Kill/Block List
- **Killed:** CAND-020 (Insufficient post-entry drift and low frequency)
- **Blocked:** CAND-019 (Missing local required data for Fixed Income benchmark)

## 13. Resource Use
- Data: Existing M1 files (`USATECHIDXUSD_M1.csv`, `XAUUSD_M1.csv`).
- Infrastructure: Lightweight Python (`pandas`, `numpy`).
- Execution Time: ~5 seconds per candidate.
- NO Parquet, NO Tick Data, NO Stage 1/2 infrastructure utilized.

## 14. Integrity
The evaluations were executed strictly according to the pre-registered event definitions. No parameters were fitted, no thresholds were altered to rescue a candidate, and no maximum favorable excursions (MFE) were utilized to fake economic headroom. CAND-015 running logs were explicitly firewalled and not accessed.
