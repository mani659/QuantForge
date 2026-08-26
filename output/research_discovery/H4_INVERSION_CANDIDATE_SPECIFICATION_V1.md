# QUANTFORGE — H4 INVERSION × ADX REGIME
# CANDIDATE SPECIFICATION / SEMANTIC ARCHAEOLOGY V1

## 1. Executive Summary

An independent, read-only semantic archaeology of the existing H4 Inversion bot was conducted. The audit reveals a **critical discrepancy** between the structural hypothesis provided in the mission brief (3 specific ADX regimes, grid scaling, trap pending orders, SMC confluence) and the **actual implementation in the source files**. 

The existing implementation (`CAB Master` and `CAB Watcher`) does **not** contain the 3 fixed ADX thresholds, grid logic, or pending-order trap mechanisms. Instead, it relies on a strict open/close H4 inversion model and dynamic percentile-based M1 market regimes (Exhaustion vs. Trending). This document establishes the factual, implementation-grounded specification found in the source code.

## 2. Source Files / Provenance

The archaeology was performed on the existing `CAB` (Omni-Pair) bot implementation:
- `c:\Users\User10\Documents\MRV\CAB\Multi Pair\For multi pairs\cab_master.py` (H4 Inversion entry and execution engine)
- `c:\Users\User10\Documents\MRV\CAB\Multi Pair\For multi pairs\config.py` (Pair-specific risk, ATR, and management configurations)
- `c:\Users\User10\Documents\MRV\CAB\Multi Pair\For gold only\cab_watcher.py` (Advanced position management and M1 regime logic)
- `c:\Users\User10\Documents\MRV\CAB\Multi Pair\For multi pairs\CAB_Global_Sentinel.mq5` (Failover heartbeat system)

*Note: Extensive full-text searches were conducted for `get_adx_directional()`, `check_exhaustion_filter()`, and `check_smc_confluence()`. These functions do **not** exist in the repository.*

## 3. H4 Inversion Event Definition

The function `check_h4_inversion()` is implemented in `cab_master.py`.
- **Bars Used**: H4 timeframe. It calls `mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 0, 3)`
  - Bar 0 (index -1 in rates): Current open/incomplete bar.
  - Bar 1 (index -2 in rates): Previous closed bar.
  - Bar 2 (index -3 in rates): Prior closed bar.
- **Bullish Condition**: `Bar1 Close > Bar1 Open` AND `Bar2 Close < Bar2 Open` AND `Bar1 Close > Bar2 Open`.
- **Bearish Condition**: `Bar1 Close < Bar1 Open` AND `Bar2 Close > Bar2 Open` AND `Bar1 Close < Bar2 Open`.
- **Nuances**:
  - Only open and close prices are used. Highs/lows (wicks) are completely ignored.
  - Strict inequalities (`>`, `<`); equality handling is absent.
  - There are NO embedded ATR, ADX, or session constraints inside this function.

## 4. Signal Timing

- **Bar 2**: Represents the directional thrust that is being inverted (e.g., a bearish closed candle).
- **Bar 1**: Represents the confirming inversion candle that closes beyond Bar 2's open.
- **Bar 0**: The signal is known exactly at the **open timestamp** of Bar 0.
- **Execution Timing**: The bot deduplicates using the H4 candle timestamp (`last_h4_bars`). It executes at the **current ask (for buys)** or **current bid (for sells)** on the very first M15/M1 tick that registers the new H4 candle.

## 5. ADX Regime Definition

**NOT FOUND IN SOURCE AS DESCRIBED.**
The strict thresholds (`ADX < 30`, `30 ≤ ADX ≤ 60`, `ADX > 60`) are absent from the implementation.

Instead, regime definition (`get_market_regime` in `cab_watcher.py`) uses an M1 timeframe over a 170-bar lookback:
- Calculates Wilder's ADX (14-period), ATR (14-period vs 50-period ratio), and Body-to-Range Ratio (BR).
- It calculates the **Percentile Rank** of the current value against the 170-bar window.
- **EXHAUSTION**: `atr_rank >= 75 AND br_rank <= 35`
- **TRENDING**: `adx_rank >= 65 AND br_rank > 35`
- **STABLE**: Default fallback.

## 6. Regime A — Grid

**NOT FOUND IN SOURCE CODE.**
There is no grid execution, no 1.5× scaling, no layer calculation, and no VWAP basket target logic anywhere in the bot's execution source.

## 7. Regime B — Continuation

**NOT FOUND IN SOURCE CODE.**
There is no DI alignment logic, no trap pending-orders, and no pending-order expiration logic. All trades are executed as immediate market deals (`mt5.TRADE_ACTION_DEAL`).

## 8. Regime C — Inversion

The actual implemented entry logic (`execute_entries` in `cab_master.py`) consists of:
- **H4 Inversion**: Exact open/close cross logic.
- **Spread Gate**: Checks if current spread exceeds `config.PAIRS["MAX_SPREAD"]`.
- **Dynamic 1% Risk**: Calculates lot size based on `RISK_PERCENT` (e.g., 1.0% or 0.5%).
- **ATR-Based Stop**: SL is strictly placed at `M15 ATR (14 period) × ATR_MULT_SL` away from the execution price.
- **Missing Elements**: Exhaustion checks and SMC context are absent from the entry loop.

## 9. Position Management

Position management is aggressively decoupled across two files.

**From `cab_watcher.py` (M1 Loop - Fluid Logic):**
- **Reaper**: If `Regime == TRENDING` and `R-Ratio <= -0.5`, exit immediately at market. (Acts dynamically on the current bar).
- **Protector**: If `R-Ratio >= 1.2`, modify SL to `Entry +/- (M15 ATR * 0.1)`.
- **Harvester**: If `Regime == EXHAUSTION` and `R-Ratio >= 2.0`, exit immediately at market.

**From `cab_master.py` (H4 Loop - Master Management):**
- **Opposite Signal Kill**: If an active buy position exists and `check_h4_inversion` returns BEARISH (or vice versa), the trade is immediately killed.
- **Break-Even (BE_LOCK)**: SL moved to exact open price when R-Ratio reaches `BE_GATE_R` (e.g., 0.8R).
- **Profit Lock**: SL moved to +0.5R when R-Ratio reaches `LOCK_GATE_R` (e.g., 1.0R).
- **Partial (HARVEST_50)**: Closes 50% of the volume when R-Ratio reaches `PARTIAL_R` (e.g., 1.5R).

## 10. Hidden Assumptions

- **Deduplication**: The bot prevents duplicate entries entirely on the same H4 candle using the candle timestamp, but has no cooldowns between consecutive H4 signals.
- **Timeframes**: Entry uses H4. ATR for SL uses M15 (period 14). Regime intelligence uses M1 (170 bars).
- **Filling Modes**: A custom `_get_filling_mode()` abstracts FOK vs IOC broker restrictions, defaulting to RETURN.
- **Engineering Overhead**: The bot uses a file-based heartbeat (`cab_heartbeat.txt`) written by Python and read by an MT5 Expert Advisor (`CAB_Global_Sentinel.mq5`). If Python dies, the MQ5 EA acts as a failover and applies an emergency trailing stop (`InpFailoverATRMult`).

## 11. Data Requirements

Required to reproduce the ACTUAL implemented signal and management:
- **Signal Reconstruction**: H4 OHLC (specifically open and close).
- **Economic Translation (Entry)**: M15 OHLC (for 14-period ATR SL distance calculation), tick data for spread filtering and execution.
- **Trade Management (Regimes)**: M1 OHLC (at least 170 bars) for percentile-based Regime detection (ADX, ATR, Body-Ratio).

## 12. Behavioral vs Economic vs Engineering Classification

| Component | Exact Existing Semantics | Timeframe | Threshold / Rule | Candidate Classification | Uncertainty |
|---|---|---|---|---|---|
| H4 inversion | `c1_c > c1_o`, `c2_c < c2_o`, `c1_c > c2_o` | H4 | Strict inequality, no wicks | A - Behavioral | None |
| ADX / Regimes | Percentile rank of Wilder ADX & ATR & Body-Ratio | M1 | ADX rank > 65; ATR rank > 75 | A - Behavioral | None (differs from prompt) |
| DI alignment | **Not Found** | N/A | N/A | Unresolved | Not in source |
| Grid base/add/kill| **Not Found** | N/A | N/A | C - Engineering | Not in source |
| Continuation session| **Not Found** | N/A | N/A | Unresolved | Not in source |
| Continuation entry| **Not Found** | N/A | N/A | Unresolved | Not in source |
| Trap pending order| **Not Found** | N/A | N/A | Unresolved | Not in source |
| Inversion entry | Market execution immediately on H4 close | Tick | Spread < MAX_SPREAD | C - Engineering | None |
| Initial SL | M15 ATR(14) × Multiplier (e.g. 2.5) | M15 | ATR Multiplier | B - Translation | None |
| Reaper | Exit if losing in trending regime | M1 | R-Ratio <= -0.5R | B - Translation | None |
| Protector | Move SL to Entry + 0.1 ATR | M1 | R-Ratio >= 1.2R | B - Translation | None |
| Trailing | **Not Found** | N/A | N/A | C - Engineering | Not in source |
| Harvester | Exit if winning in exhausted regime | M1 | R-Ratio >= 2.0R | B - Translation | None |
| Structural invalidation| Exit if opposing H4 inversion occurs | H4 | Opposing Signal | A - Behavioral | None |

## 13. Candidate Abstraction

> **H4 Inversion × Percentile Market State Conditional Behavior**

Based on factual code archaeology, the core behavioral candidate is an **H4 Engulfing/Inversion (Open/Close only) constrained or managed by micro-structural (M1) regime states**. The regimes are NOT static ADX thresholds, but rather dynamic percentile-ranked states (Exhaustion vs Trending) acting primarily as exit/management modifiers, not entry filters.

## 14. Unresolved Questions

- **Where did Regime A (Grid) and Regime B (Continuation/DI Alignment / Pending Orders) originate?** They are completely absent from the audited source files. Were they part of a deprecated version, an MT4 EA, or purely a theoretical design?
- **Missing Functions**: `check_smc_confluence()`, `get_adx_directional()`, and `check_exhaustion_filter()` do not exist in this repository.

## 15. Governance Recommendation

**Do NOT proceed to experiment design using the 3 static ADX regimes or Grid logic.**
The factual archaeology proves that the existing bot operates on a completely different set of semantics (M1 percentile regimes and aggressive R-ratio management). Before authorizing an experiment, QuantForge must decide whether to test the *actual* implemented semantics or explicitly treat the 3 ADX regimes as a *new*, unverified theoretical candidate.

## 16. Integrity

- **READ-ONLY**: Verified.
- **NO EXECUTION**: Verified.
- **NO BACKTEST**: Verified.
- **NO PNL / COST CALCULATION**: Verified.
- **NO CODE CHANGES**: Verified.
- **NO PROTOCOL CHANGES**: Verified.
- **NO PARAMETER TUNING**: Verified.
- **NO CLOSED-LINE REOPENING**: Verified.
- **NO BOE DETECTOR IMPLEMENTATION**: Verified.
