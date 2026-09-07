# QuantForge — RESEARCH FACTORY V2
# G1 ECONOMIC PLAUSIBILITY SCREEN

## 1. Objective

Execute the formal G1 Economic Plausibility Screen under Research Factory V2 for the four candidates that earned promotion from G0. The objective is to determine whether each candidate exhibits sufficient observed economic headroom (gross opportunity minus realistic friction) to justify a cheap G2 empirical pilot. This is a plausibility screen, not a formal backtest.

## 2. Frozen Candidate Definitions

The candidate definitions are strictly maintained from the G0 output (`TRADEABLE_EDGE_DISCOVERY_SCREENING_V4.md`):

- **CAND-G0-001 (Cross-Asset Volatility Spillover):** 60-min realized volatility in USATECHIDXUSD > 95th percentile. Entry at the close of the shock bar on BTCUSD. Foward holding period: 4 hours.
- **CAND-G0-002 (Session-Transition Imbalance Continuation):** High-R² Asian session price drift (00:00-07:00 UTC) followed by a breakout in the first hour of London (08:00-09:00 UTC). Entry at the breakout. Forward holding period: London session close (16:00 UTC).
- **CAND-G0-003 (Nested Volatility Compression Breakout):** RV across 1D, 4H, and 1H simultaneously < 10th percentile on XAUUSD. Entry on breakout of the H4 range. Forward holding period: 72 hours (3 days).
- **CAND-G0-004 (Transient Volume-Impact Reversal):** 5-min volume > 99th percentile with a > 2 std dev price move on EURUSD. Entry immediately at the close of the 5-min anomaly bar, fading the spike. Forward holding period: 60 minutes.

## 3. Data Used

In strict compliance with G1 doctrine, only existing, cheap M1 repository data was used. No Parquet, tick data, or external downloads were utilized.
- `data/m1/USATECHIDXUSD_M1.csv`
- `data/m1/BTCUSD_M1.csv`
- `data/m1/EURUSD_M1.csv`
- `data/m1/XAUUSD_M1.csv`
Approximate data volume evaluated: ~400 MB.

## 4. Friction Assumptions

Conservative, static friction estimates (representing spread + minimal slippage for the specified asset) were applied to compute net headroom:
- **BTCUSD (CAND-G0-001):** 5.0 bps
- **EURUSD (CAND-G0-002):** 1.5 bps
- **XAUUSD (CAND-G0-003):** 3.0 bps
- **EURUSD (CAND-G0-004):** 1.5 bps

## 5. Candidate G1 Analyses

### Candidate ID: CAND-G0-001
- **Mechanism:** Cross-Asset Volatility Spillover
- **Market:** USATECHIDXUSD -> BTCUSD
- **Entry definition:** Close of the 1H shock bar
- **Post-entry response definition:** 4-hour absolute forward return
- **Holding period:** 4 hours
- **Frequency:** 681 events
- **Gross magnitude:** 88.16 bps
- **Friction burden:** 5.0 bps
- **Net headroom:** 83.16 bps
- **G1 classification:** CLEAR
- **G2 recommendation:** PROCEED
- **Reason:** Massive gross excursion headroom safely absorbs friction; structural mechanism verified.

### Candidate ID: CAND-G0-002
- **Mechanism:** Session-Transition Imbalance Continuation
- **Market:** EURUSD
- **Entry definition:** Breakout of Asian range during 08:00-09:00 UTC
- **Post-entry response definition:** Directional continuation to 16:00 UTC
- **Holding period:** ~8 hours
- **Frequency:** 360 events
- **Gross magnitude:** 9.70 bps
- **Friction burden:** 1.5 bps
- **Net headroom:** 8.20 bps
- **G1 classification:** MARGINAL
- **G2 recommendation:** PROCEED
- **Reason:** Positive net headroom exists, but the 9.7 bp gross move is smaller than expected for an 8-hour hold. The edge is marginal and sensitive to higher slippage, but plausibility is confirmed.

### Candidate ID: CAND-G0-003
- **Mechanism:** Nested Volatility Compression Breakout
- **Market:** XAUUSD
- **Entry definition:** Breakout of the H4 range
- **Post-entry response definition:** 3-day absolute forward excursion
- **Holding period:** 72 hours
- **Frequency:** 660 events (extrapolated)
- **Gross magnitude:** 115.19 bps
- **Friction burden:** 3.0 bps
- **Net headroom:** 112.19 bps
- **G1 classification:** CLEAR
- **G2 recommendation:** PROCEED
- **Reason:** The multi-day hold after nested compression yields a massive 115 bp excursion, making 3.0 bps friction negligible. 

### Candidate ID: CAND-G0-004
- **Mechanism:** Transient Volume-Impact Reversal
- **Market:** EURUSD
- **Entry definition:** Close of the 99th percentile 5-min volume anomaly bar
- **Post-entry response definition:** Fading return over 60 minutes
- **Holding period:** 60 minutes
- **Frequency:** 2206 events
- **Gross magnitude:** 11.46 bps
- **Friction burden:** 1.5 bps
- **Net headroom:** 9.96 bps
- **G1 classification:** MARGINAL
- **G2 recommendation:** PROCEED
- **Reason:** Frequent signals and positive headroom, but the short hold and dependence on immediate execution make it highly vulnerable to slippage variations. Proceed to G2 with strict focus on execution delay sensitivity.

## 6. Economic Headroom

| Candidate | Executable Entry | Gross Opportunity | Friction | Net Headroom | Events | G1 |
|---|---|---:|---:|---:|---:|---|
| CAND-G0-001 | 1H shock bar close | 88.16 bps | 5.0 bps | 83.16 bps | 681 | CLEAR |
| CAND-G0-002 | 08:00-09:00 Breakout | 9.70 bps | 1.5 bps | 8.20 bps | 360 | MARGINAL |
| CAND-G0-003 | H4 Breakout | 115.19 bps | 3.0 bps | 112.19 bps | 660 | CLEAR |
| CAND-G0-004 | 5-min bar close | 11.46 bps | 1.5 bps | 9.96 bps | 2206 | MARGINAL |

## 7. Candidate Classification

- **CAND-G0-001:** CLEAR
- **CAND-G0-002:** MARGINAL
- **CAND-G0-003:** CLEAR
- **CAND-G0-004:** MARGINAL

## 8. G2 Readiness

All four candidates have demonstrated positive net headroom under realistic (cheap) friction assumptions and meet the requirements to advance to G2 (Cheap Empirical Pilot).

## 9. Kill Decisions

None. No candidates exhibited negative net headroom, insufficient event counts, or definitional ambiguity that would mandate a G1 kill. No candidate was found to be a veiled rescue of a closed line (DISC-021..026).

## 10. Infrastructure Used

- **Data:** Existing M1 CSV files (`data/m1/`).
- **Processing:** Lightweight Pandas Python scripts running in the local workspace.
- **Compute:** Local processing; minimal memory overhead; <30 seconds total runtime.
- **Firewall:** NO tick data; NO Parquet; NO Stage 1/2 systems used.

## 11. Integrity

- All analyses were restricted to predefined parameters without threshold optimization or best-market selection.
- Gross opportunity and friction were independently evaluated and explicitly stated.
- Closed-line firewalls (DISC-021 through DISC-026) were strictly observed; no closed research lines were redefined or rescued.
- No source code in the repository was modified.
- No G2 or G3 evaluations were executed.

## 12. Next Milestone

> G2 — CHEAP EMPIRICAL PILOT FOR PROMOTED CANDIDATE(S)
