# QUANTFORGE — TRADEABLE EDGE DISCOVERY SCREENING V2

## 1. Executive Objective
Return QuantForge to its primary objective: discovering a defensible trading edge that can survive statistical validation, economic/PnL validation, demo/forward testing, and live-market conditions. This screening strictly prioritizes candidates with robust behavioral mechanisms and excursions large enough to overcome spread and slippage. Academic curiosity and methodological complexity are secondary to economic tradability.

## 2. Current Project Position
The project has returned to **TRADEABLE EDGE DISCOVERY SCREENING**. 
The H01 Equity Track A is open but currently awaiting historical broad-US equity data acquisition. We now require a completely new, independent candidate to enter the pipeline at the screening stage.

## 3. Closed Research Lines
We explicitly avoid the following families of hypotheses, as their variations have been tested and closed:
1. **Mean Reversion (DISC-021)**: Arbitrary z-score/displacement mean-reversion. Closed due to economic non-viability (spread consumed the signal, especially in XAGUSD).
2. **TSMOM 12/1 (DISC-022)**: Fixed time-series momentum. Closed due to lack of stable cross-era incremental signal.
3. **Session-Anchored Range Expansion (DISC-024)**: Pre-session compression preceding cash-session expansion magnitude. Contradicted (compression preceded lower expansion).

## 4. Available Data Inventory
The local `data/m1/` directory contains high-quality M1 data for five primary assets:
- `BTCUSD_M1.csv` (~140MB)
- `EURUSD_M1.csv` (~114MB)
- `USATECHIDXUSD_M1.csv` (~56MB)
- `XAGUSD_M1.csv` (~87MB)
- `XAUUSD_M1.csv` (~104MB)

All datasets support M1 analysis. EURUSD and XAGUSD have historically struggled with economic viability against spread constraints in previous studies. BTCUSD, XAUUSD, and USATECHIDXUSD remain strong candidates due to inherently larger absolute excursion properties.

## 5. Candidate Families
We evaluate five structurally independent behavioral families:
- **A. Liquidity Sweep / Stop-Run**: Penetration of anchored structural extremes (e.g., session highs/lows) to accumulate liquidity before a reversal.
- **B. Volatility Shock Continuation**: Forced liquidation cascades following an acute volatility spike, creating momentum persistence rather than reversion.
- **C. Microstructure TWAP Footprint**: Detecting algorithmic slicing of parent orders via consecutive directional bar sequences.
- **D. Opening Gap Repair**: Market maker inventory neutralization driving price back toward the prior cash close.
- **E. Cross-Market Confirmation**: Leading/lagging relationships between equity indices and FX or metals.

## 6. Candidate Comparison Matrix

| Candidate | Mechanism | Tradability | Frequency | Data Fit | Robustness | Overfit Risk | Live Path | Overall |
|---|---|---|---|---|---|---|---|---|
| **A. Session Sweep & Reversal (XAUUSD)** | HIGH | HIGH | HIGH | HIGH | HIGH | LOW | HIGH | **HIGH** |
| **B. Shock Continuation (BTCUSD)** | HIGH | HIGH | MED | HIGH | MED | MED | HIGH | **HIGH** |
| **C. TWAP Sequence (EURUSD)** | HIGH | LOW | HIGH | HIGH | HIGH | MED | HIGH | **LOW** |
| **D. Opening Gap Repair (USATECH)** | MED | MED | MED | HIGH | MED | LOW | HIGH | **MED** |
| **E. Cross-Market Confirm (USATECH/EUR)** | MED | MED | MED | HIGH | LOW | HIGH | MED | **LOW** |

## 7. Economic Filter
Candidate C (TWAP on EURUSD) is downgraded heavily. While the behavioral footprint of execution algos is real, EURUSD's low baseline volatility means the captured move is highly likely to be consumed by standard retail spreads and commissions (as observed in DISC-021). Candidate E requires multi-symbol execution sync, risking slippage mismatch. Candidates A (XAUUSD) and B (BTCUSD) are favored because gold and bitcoin structurally produce massive, violent excursions that comfortably absorb 2–3 tick/pip spreads.

## 8. ML / Methodology Position
Machine learning methods (K-means, HMM, XGBoost) remain valid tools but are **not** hypotheses. A strong behavioral edge should be detectable with simple, deterministic rules. If a simple rule proves the mechanism, ML might later optimize the state boundaries. We will not start with ML simply because it is sophisticated; the primary candidate must rely on a deterministic, interpretable classifier.

## 9. Primary Candidate
**PRIMARY NEXT CANDIDATE: London/NY Session Sweep and Reversal (XAUUSD)**

- **Behavioral Hypothesis**: Institutional participants require massive liquidity to fill block orders. This liquidity resides as stop-losses directly above/below the established Asian session extremes (e.g., 00:00–07:00 UTC). A penetration of this extreme during the high-volume London/NY overlap, followed immediately by a structural close back inside the range, reliably precedes a directional excursion toward the opposite side of the range.
- **Economic Plausibility**: It is structurally necessary for large market participants to seek liquidity pools. 
- **Tradable Move**: XAUUSD reversals off major liquidity sweeps often yield dozens of dollars in price movement, dwarfing standard broker spreads.
- **Data Support**: `XAUUSD_M1.csv` is locally available, deep, and perfectly suited for defining session boundaries and trigger thresholds.
- **Distinct from Closed Lines**: Mean Reversion tested arbitrary unanchored z-score displacement. This tests specifically anchored structural liquidity pools (session boundaries).
- **Strategy Translation Path**: Straightforward. Signal = sweep + reversal close. Entry = next open. Risk = just beyond the sweep wick. Reward = opposite session bound. 

## 10. Backup Candidate
**SECOND-BEST CANDIDATE: Post-Shock Liquidation Continuation (BTCUSD)**

- **Behavioral Hypothesis**: An acute, localized volatility shock (e.g., a 15-minute range exceeding the trailing 99th percentile) reliably precedes directional continuation over the subsequent 1-4 hours due to fragmented liquidity and forced cascading liquidations, rather than mean reversion.
- **Why not chosen first**: The crypto market's structural mechanisms change rapidly. Gold's liquidity dynamics are historically more robust and stable across macro regimes. We retain BTCUSD as a backup to avoid premature lock-in.

## 11. Why Primary Was Selected
The XAUUSD Session Sweep & Reversal aligns perfectly with QuantForge's ultimate goal. It offers a highly plausible institutional behavioral mechanism, is extremely simple to define deterministically (no ML required), occurs frequently enough to generate statistical power, and most importantly, produces excursions in gold that are structurally large enough to survive real-world economic friction. 

## 12. What Would Falsify It
The hypothesis will be formally falsified if:
1. The median directional excursion following a sweep-and-reversal is indistinguishable from the unconditional median excursion.
2. The price reliably continues in the direction of the sweep (proving it was a true breakout rather than a stop-run).

## 13. Strategy Translation Path
If mathematically supported:
1. Candidate behavior establishes the presence of the directional drift.
2. Economic translation applies explicit XAUUSD spread assumptions and static risk/reward ratios.
3. If PnL > 0, deploy a lightweight MT5 EA to forward-test fill quality on demo.

## 14. Next Legitimate Task
The exact next legitimate task is: **Scientific Definition Lock and Outcome-Blind Pre-Registration** for the XAUUSD Session Sweep and Reversal candidate.

## 15. Prohibited Follow-Up
- Do NOT backtest the XAUUSD candidate in an exploratory script.
- Do NOT run K-means to find the "best" sweep parameters.
- Do NOT evaluate historical PnL before finalizing the definition lock.
- Do NOT return to the Session Range Expansion candidate.

## 16. Integrity
No code was written. No data was processed. No ML was invoked. The candidate was selected purely on behavioral rationale, economic viability against known friction, and structural distinctness from closed lines.
