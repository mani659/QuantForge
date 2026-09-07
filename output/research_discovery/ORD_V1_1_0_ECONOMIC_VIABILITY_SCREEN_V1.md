# QUANTFORGE — ORD V1.1.0
# ECONOMIC TRANSLATION / VIABILITY SCREEN V1

## 1. Executive Verdict
**ECONOMICALLY NON-VIABLE**

The registered scientific behavioral movement—entering at the 5-minute close of an opening range breakout and holding for a 120-minute horizon—fails to overcome the basic minimum friction of financial markets. While the event exhibits a scientifically robust edge over the control, its absolute gross response (mean +1.12 to +2.01 basis points) is completely consumed by even ultra-conservative observed round-trip spreads and slippage.

## 2. Frozen Scientific Evidence
* **Status:** SCIENTIFICALLY SUPPORTED
* **Adjudicated Protocol:** ORD V1.1.0 (SHA: `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06`)
* **Execution:** `EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532`
* **Result:** XAUUSD, XAGUSD, and USATECHIDXUSD verified as statistically robust structural events (`DeltaM > 0`, `p_holm < 0.05`).

## 3. Economic Translation
The strict executable translation of the scientific phenomenon is:
* **Entry:** At the exact closing price of the 5-minute candle that breaks the opening range (`entry_close`).
* **Exit:** At the exact closing price 120 minutes later (`horizon_close`).
* **Metric:** Response in basis points (bps): `(horizon_close - entry_close) / entry_close * 1e4` (multiplied by direction).

## 4. Execution / Fill Assumptions
* **Pricing Series:** The translation assumes executions occur exactly at the mid-price series (`entry_close` and `horizon_close`). 
* **Friction:** Real-world execution requires crossing the bid-ask spread at entry and exit, plus accounting for slippage on market orders at a momentum-driven breakout.

## 5. Cost Model
Given the absolute values involved, exact sub-pip quote matching is unnecessary to establish non-viability. We evaluate fixed conservative cost bands representing total round-trip execution cost (spread + slippage):
* **0 bps:** Perfect frictionless mid-price fill.
* **5 bps:** Highly liquid major asset (e.g., US Tech index) conservative friction.
* **10 bps:** Typical metal (e.g., Gold) average friction.
* **20 bps:** Higher friction/volatility metal (e.g., Silver) friction.

## 6. Market-Level Economics
| Market | Scientific Status | Treatment N | Gross Response (Mean) | Gross Response (Median) | Estimated Round-Trip Cost | Net Response (Mean) | Break-Even Cost | Economic Classification |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **XAUUSD** | SUPPORT | 2184 | +1.26 bps | -0.13 bps | ~ 5 - 10 bps | **Negative** | 1.26 bps | NON-VIABLE |
| **XAGUSD** | SUPPORT | 2177 | +1.12 bps | -1.75 bps | ~ 15 - 30 bps | **Negative** | 1.12 bps | NON-VIABLE |
| **USATECHIDXUSD**| SUPPORT | 839 | +2.01 bps | +1.24 bps | ~ 2 - 5 bps | **Negative** | 2.01 bps | NON-VIABLE |
| **BTCUSD** | HALTED | - | - | - | - | - | - | HALTED / NOT EVALUABLE / NO ECONOMIC ADJUDICATION |

## 7. Break-Even Cost
The absolute maximum round-trip cost the strategy can tolerate before expected value turns negative (mean basis):
* **XAUUSD:** 1.26 bps (~$0.30 per ounce round-trip)
* **XAGUSD:** 1.12 bps (~$0.003 per ounce round-trip)
* **USATECHIDXUSD:** 2.01 bps (~4 index points round-trip)

## 8. Cost Sensitivity (Win% and Net Mean)
**XAUUSD:**
* **0 bps:** Net Mean = +1.26 bps, Win% = 49.8%
* **5 bps:** Net Mean = -3.74 bps, Win% = 40.4%
* **10 bps:** Net Mean = -8.74 bps, Win% = 31.5%

**XAGUSD:**
* **0 bps:** Net Mean = +1.12 bps, Win% = 48.4%
* **5 bps:** Net Mean = -3.88 bps, Win% = 43.1%
* **10 bps:** Net Mean = -8.88 bps, Win% = 38.3%

**USATECHIDXUSD:**
* **0 bps:** Net Mean = +2.01 bps, Win% = 51.6%
* **5 bps:** Net Mean = -2.99 bps, Win% = 46.0%
* **10 bps:** Net Mean = -7.99 bps, Win% = 41.0%

## 9. Execution Realism
The required break-even costs are lower than the structural minimum bid-ask spreads for these instruments during New York opening hours. It is physically impossible to execute the breakout entries and time-based exits at costs equal to or lower than the break-even threshold. The edge is entirely theoretical/mid-market.

## 10. Cross-Market Economic Evidence
The failure mode is identical across all three scientifically supported markets: the behavioral phenomenon (`DeltaM`) is driven by the extreme negativity of the control (failed penetrations) rather than absolute profitability of the treatment. The treatment's absolute gross return is statistically bounded near zero.

## 11. Economic Classification
> **ECONOMICALLY NON-VIABLE**
> 
> Costs erase the behavioral movement before costs. The edge is gross-negative or practically zero, leaving no surplus to fund transaction costs.

## 12. Limitations
This analysis utilizes conservative fixed bands rather than full order-book simulations. However, since the break-even thresholds are 1-2 basis points, more precise quote matching is strictly unnecessary; the system fails the first-order spread screen. No alternative entry/exit mechanisms or optimized parameters were tested, strictly adhering to governance.

## 13. Next Governance Decision
The governed recommendation is to **CLOSE** the ORD V1.1.0 candidate line as a TRANSLATION FAILURE, identical to Mean Reversion and Liquidity Sweep/Reversal, and return to TRADEABLE EDGE DISCOVERY SCREENING.

## 14. Integrity
- read-only;
- no ORD scientific rerun;
- no protocol change;
- no Definition Lock change;
- no parameter tuning;
- no market selection from economic results;
- no BOE detector;
- no EA;
- no PnL backtest;
- no live/demo execution.
