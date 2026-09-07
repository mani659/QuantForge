# QUANTFORGE — TICK-DATA CAPABILITY & MICROSTRUCTURE READINESS AUDIT V1

**Date:** 2026-09-07
**Status:** AUDIT COMPLETE — PARTIALLY READY — PREREQUISITE DATA/INFRASTRUCTURE WORK REQUIRED
**Purpose:** Independent, READ-ONLY audit of QuantForge's tick-data sources and infrastructure to determine readiness for microstructure mechanism discovery.

---

## 1. MISSION

Perform a strict, independent, READ-ONLY audit of QuantForge's currently available tick-data sources and infrastructure to determine whether the project has sufficient data fidelity to begin a new microstructure/tick-level mechanism-discovery program.

The purpose is NOT to discover a strategy. The purpose is to answer:

> **What information does QuantForge's actual tick data contain, how reliable is it, and which genuinely new observables can be derived without assuming information that does not exist?**

---

## 2. AUTHORITATIVE SOURCES CONSULTED

| Source | Path | Key insight |
|--------|------|-------------|
| SESSION_HANDOFF (through §77) | `docs/SESSION_HANDOFF.md` | Current governed state |
| Tick Validator | `validator/tick_validator.py` | Expected schema: date, time, bid, ask, last, volume |
| Tick-to-M1 Converter | `converter/tick_to_m1.py` | Expected schema: date, time, bid, ask, last, volume |
| Tick Parquet Converter | `research/staged_execution/tick_parquet_converter.py` | Parquet schema: source_row_ordinal, date, time, bid, ask, last, vol |
| RF-001 Recorder | `scripts/forward/rf001_observation_recorder.py` | M1 OHLCV from MT5, not tick data |
| F-01 Recorder | `scripts/forward/f01_recorder.py` (implied) | M1 OHLCV from MT5, not tick data |
| Validation Reports | `reports/*_mt5_ticks_validation.txt` | Pre-computed quality metrics for 5 symbols |
| Test Fixture Parquet | `tests/output_test_b/XAGUSD/202101.parquet` | Canonical tick parquet schema |
| M1 Derived Data | `data/m1/*.csv` | M1 OHLCV converted from ticks |

---

## 3. ACTUAL DATA SOURCES

### 3.1 Tick Data (on-disk, not git-tracked)

| Symbol | File | Size (GB) | Rows | Date Range | Days |
|--------|------|-----------|------|------------|------|
| USATECHIDXUSD | `data/tick/USATECHIDXUSD_mt5_ticks.csv` | 8.4 | 173,457,022 | 2023-09-01 to 2026-07-10 | 1,043 |
| XAUUSD | `data/tick/XAUUSD_mt5_ticks.csv` | 12.9 | 281,514,283 | 2021-04-12 to 2026-04-10 | 1,824 |
| XAGUSD | `data/tick/XAGUSD_mt5_ticks.csv` | 5.8 | 146,389,821 | 2021-07-13 to 2026-07-12 | 1,825 |
| BTCUSD | `data/tick/BTCUSD_mt5_ticks.csv` | 12.8 | 299,204,931 | 2021-05-23 to 2026-05-22 | 1,825 |
| EURUSD | `data/tick/EURUSD_mt5_ticks.csv` | 0.1 | 28,931,551 | 2025-01-01 to 2026-04-01 | 454 |

**Total tick data on disk:** ~40 GB, ~930M rows across 5 symbols.

### 3.2 Derived M1 Data (on-disk, not git-tracked)

| Symbol | File | Size (MB) |
|--------|------|-----------|
| BTCUSD | `data/m1/BTCUSD_M1.csv` | 141 |
| EURUSD | `data/m1/EURUSD_M1.csv` | 114 |
| USATECHIDXUSD | `data/m1/USATECHIDXUSD_M1.csv` | 57 |
| XAGUSD | `data/m1/XAGUSD_M1.csv` | 87 |
| XAUUSD | `data/m1/XAUUSD_M1.csv` | 104 |

### 3.3 Live Prospective Data (git-tracked, active)

| Dataset | File | Source | Status |
|---------|------|--------|--------|
| RF-001 two-market M1 | `data/rf001/raw/rf001_two_market_m1_raw.csv` | MT5 M1 bars (USTECm + US500m) | Active, accruing |
| F-01 M1 | `data/f01/raw/ustechidxusd_m1_raw.csv` | MT5 M1 bars (USTECm) | Active |

### 3.4 Test Fixture Parquet

| File | Rows | Schema |
|------|------|--------|
| `tests/output_test_b/XAGUSD/202101.parquet` | 1 | source_row_ordinal, date, time, bid, ask, last, vol |

---

## 4. FIELD SEMANTICS — ACTUAL RECORDS

### 4.1 USATECHIDXUSD, XAUUSD, XAGUSD, BTCUSD (True Tick Data)

**Observed format:** 6-column CSV, comma-separated, no header.

| Column | Index | Datatype | Semantic | Observed behavior |
|--------|-------|----------|----------|-------------------|
| date | 0 | string (YYYYMMDD) | Trade/quote date | Valid, no invalid timestamps |
| time | 1 | string (HH:MM:SS) | Trade/quote time | Second resolution, multiple ticks per second |
| bid | 2 | float64 | Best bid price | Always present, always > 0 |
| ask | 3 | float64 | Best ask price | Always present, always > bid |
| last | 4 | float64 | Last traded price | **For USATECHIDXUSD: always equals bid (100%).** For XAUUSD/XAGUSD: equals bid. For BTCUSD: equals bid. |
| volume | 5 | float64 | Tick volume | **For USATECHIDXUSD/XAUUSD/XAGUSD: always 0.** For BTCUSD: always 0. This is NOT real trade volume. |

**Critical semantic findings:**

- **`last` field is semantically equivalent to `bid` for all symbols.** The MT5 tick model reports the last traded price, but for CFDs on this broker, the execution price always equals the bid. This means `last` provides NO independent information beyond `bid`.
- **`volume` field is zero for all ticks across all symbols.** This is tick volume (count of ticks), not real trade volume. The MT5 broker does not provide real transaction volume for these instruments.
- **Both `bid` and `ask` are present and update independently.** Spread can be reliably calculated.
- **No trade/quote event-type flag exists.** Every row is a quote update (bid/ask change). The `last` field does not indicate a separate trade event — it mirrors the bid.

### 4.2 EURUSD (MISLABELLED — NOT TICK DATA)

**Observed format:** 7-column CSV, comma-separated, no header.

| Column | Index | Datatype | Semantic | Observed behavior |
|--------|-------|----------|----------|-------------------|
| date | 0 | string (YYYY.MM.DD) | Bar date | Different date format from other symbols (dots vs. no separators) |
| time | 1 | string (HH:MM) | Bar time | **Minute resolution, not second resolution** |
| col2 | 2 | float64 | Open price | OHLCV open |
| col3 | 3 | float64 | High price | OHLCV high |
| col4 | 4 | float64 | Low price | OHLCV low |
| col5 | 5 | float64 | Close price | OHLCV close |
| vol | 6 | float64 | Tick count | Real tick count per minute (non-zero, mean ~84) |

**Critical finding: `EURUSD_mt5_ticks.csv` is actually M1 OHLCV data, not tick data.** Evidence:
- 7 columns vs. 6 for true tick data
- Time resolution is minutes (HH:MM), not seconds (HH:MM:SS)
- Column structure is OHLCV (open, high, low, close, volume)
- `open==low` only 14.4% of the time (would be ~100% for tick data where each row is a single price)
- Date format uses dots (YYYY.MM.DD) vs. YYYYMMDD for true tick data
- Volume is tick count per minute (mean 84), not zero

**The tick validator and tick-to-M1 converter assume 6-column format.** EURUSD cannot be processed by these tools without modification.

---

## 5. TIMESTAMP AUDIT

### 5.1 Resolution

| Symbol | Resolution | Evidence |
|--------|------------|----------|
| USATECHIDXUSD | 1 second | Multiple ticks per second (mean 3.9 ticks/sec, max 20/sec). Time format HH:MM:SS. |
| XAUUSD | 1 second | Multiple ticks per second (mean 3.8 ticks/sec, max 29/sec). Time format HH:MM:SS. |
| XAGUSD | 1 second | Multiple ticks per second (mean 3.0 ticks/sec, max 20/sec). Time format HH:MM:SS. |
| BTCUSD | 1 second | Multiple ticks per second (mean 2.9 ticks/sec, max 94/sec). Time format HH:MM:SS. |
| EURUSD | 1 minute | Time format HH:MM (no seconds). M1 bar data. |

### 5.2 Timezone

- All tick timestamps appear to be in **broker server timezone** (Exness-MT5Trial15).
- No explicit timezone field exists in the data.
- UTC conversion requires knowledge of the broker's server timezone offset, which is not recorded in the data.
- The tick validator and converter do not perform timezone conversion — they treat timestamps as-is.

### 5.3 Event Ordering

| Check | USATECHIDXUSD | XAUUSD | XAGUSD | BTCUSD |
|-------|--------------|--------|--------|--------|
| Backward timestamps | 0 | 0 | 0 | 0 |
| Timestamps in order | YES | YES | YES | YES |
| Duplicate timestamps | 124,468 | 12,113,435 | 20,774,568 | 15,700,361 |
| Duplicate rate | 0.07% | 4.3% | 14.2% | 5.2% |

**Duplicate timestamps are frequent.** Multiple ticks share the same second. Within a single second, event ordering is NOT recoverable from the timestamp alone. The data does not contain sub-second resolution (milliseconds, microseconds, nanoseconds) or sequence numbers.

### 5.4 Missing Intervals

| Symbol | Largest Gap (sec) | Missing Trading Days |
|--------|-------------------|---------------------|
| USATECHIDXUSD | 344,701 (~4 days) | 16 days (holidays) |
| XAUUSD | 262,896 (~3 days) | 6 days (holidays) |
| XAGUSD | 324,301 (~3.7 days) | 12 days (holidays) |
| BTCUSD | 140,401 (~1.6 days) | 1 day |
| EURUSD | 176,404 (~2 days) | None reported |

Gaps correspond to known market holidays. Weekend gaps are present and expected. No unexplained gaps detected within trading days.

---

## 6. EVENT-TYPE AUDIT

### 6.1 What Each Record Represents

For USATECHIDXUSD, XAUUSD, XAGUSD, BTCUSD:

**Each row is a quote update.** The row contains the current best bid and best ask at the time of the update. The `last` field reflects the last traded price, but as documented in §4.1, it equals `bid` for all observations — providing no independent trade-event information.

### 6.2 Trade/Quote Separation

**NOT DIRECTLY OBSERVABLE.** The data does not contain a flag distinguishing:
- Quote update (bid/ask change)
- Transaction (trade execution)
- Spread update (bid or ask changed)

All rows have the same structure. A price change in `bid` or `ask` could indicate either a quote update or a trade execution. Without an event-type flag, these cannot be separated.

### 6.3 Aggressor Classification

**NOT DIRECTLY OBSERVABLE.** The data cannot distinguish:
- Buyer-initiated transactions (aggressive buy)
- Seller-initiated transactions (aggressive sell)

The `last` price equals `bid` for all observations, which could suggest execution at the bid (seller-initiated), but this is the broker's default behavior for CFD ticks, not evidence of aggression. Lee-Ready-style classification is NOT justified because:
- The `last` field does not vary independently from `bid`
- There is no bid/ask tick direction indicator
- The data lacks the granularity needed for classification

### 6.4 Order-Book Depth

**NOT AVAILABLE.** The data contains only best bid and best ask (top-of-book). It does not contain:
- Bid depth (number of lots at best bid)
- Ask depth (number of lots at best ask)
- Resting liquidity at multiple price levels
- Order-book imbalance
- Cancelations
- Depth-of-market information

---

## 7. DATA COMPLETENESS

### 7.1 Validation Status

| Symbol | Backward TS | Invalid TS | Invalid Numeric | Ask < Bid | Negative Prices | Zero Prices | Status |
|--------|------------|------------|-----------------|-----------|----------------|-------------|--------|
| USATECHIDXUSD | 0 | 0 | 0 | 0 | 0 | 0 | **PASS** |
| XAUUSD | 0 | 0 | 0 | 0 | 0 | 0 | **PASS** |
| XAGUSD | 0 | 0 | 0 | 0 | 0 | 0 | **PASS** |
| BTCUSD | 0 | 0 | 0 | 0 | 0 | 0 | **PASS** |
| EURUSD | 0 | 0 | 0 | 0 | 0 | 0 | **PASS** (but M1, not tick) |

### 7.2 Spread Statistics

| Symbol | Avg Spread | Median Spread | P95 | P99 | Max |
|--------|-----------|---------------|-----|-----|-----|
| USATECHIDXUSD | 1.91 pts | 1.44 pts | 3.51 | 3.55 | 35.67 |
| XAUUSD | 0.49 pts | 0.40 pts | 0.88 | 1.52 | 15.00 |
| XAGUSD | 0.041 pts | 0.030 pts | 0.085 | 0.167 | 2.00 |
| BTCUSD | 78.58 pts | 75.70 pts | 123.50 | 130.20 | 1032.20 |
| EURUSD | 4.7e-5 | 4.0e-5 | 9.0e-5 | 1.8e-4 | 0.003 |

All spreads are positive (ask > bid). No inverted spreads detected.

### 7.3 Tick Density

| Symbol | Avg Ticks/Min | Median Ticks/Min | Min | Max | P95 | Avg Ticks/Sec | Max Ticks/Sec |
|--------|--------------|-----------------|-----|-----|-----|--------------|--------------|
| USATECHIDXUSD | 191 | 164 | 1 | 861 | 434 | 3.9 | 20 |
| XAUUSD | 159 | 125 | 1 | 933 | 419 | 3.8 | 29 |
| XAGUSD | 85 | 51 | 1 | 893 | 288 | 3.0 | 20 |
| BTCUSD | 118 | 97 | 1 | 789 | 295 | 2.9 | 94 |
| EURUSD | 63 | 46 | 1 | 786 | 172 | 2.5 | 20 |

Sufficient tick density for microstructure research. USATECHIDXUSD and XAUUSD have the highest density (~3-4 ticks/sec average).

### 7.4 Completeness Assessment

| Capability | Assessment |
|------------|------------|
| A. Tick-level event sequencing | **PARTIAL** — Events are ordered by timestamp, but duplicate timestamps prevent sub-second ordering. |
| B. Quote-state reconstruction | **YES** — Bid and ask are present on every tick. Quote state can be reconstructed tick-by-tick. |
| C. Spread analysis | **YES** — Spread = ask - bid is reliably calculable on every tick. |
| D. Intrabar transaction-intensity research | **YES** — Tick count per second/minute is derivable. Volume is zero for most symbols (tick volume not available). |
| E. Microstructure-state research | **PARTIAL** — Spread and quote dynamics are observable. Order-book state is not. |

---

## 8. RECONSTRUCTION CAPABILITY

| Observable | Classification | Evidence |
|------------|---------------|----------|
| Best bid | **DIRECTLY OBSERVABLE** | Present on every tick |
| Best ask | **DIRECTLY OBSERVABLE** | Present on every tick |
| Spread | **DIRECTLY OBSERVABLE** | ask - bid, always positive |
| Mid-price | **DERIVABLE RELIABLY** | (bid + ask) / 2, deterministic |
| Quote changes | **DERIVABLE RELIABLY** | Diff of bid/ask across consecutive ticks |
| Event arrival rate | **DERIVABLE RELIABLY** | Count of ticks per time interval |
| Short-horizon volatility | **DERIVABLE RELIABLY** | Variance of returns over short windows |
| Trade-price path | **DERIVABLE WITH MATERIAL ASSUMPTIONS** | `last` equals `bid` for all observations. Assuming execution at bid, trade path = bid path. But this is broker-specific behavior, not independent trade evidence. |
| Quote/trade sequence | **NOT RELIABLY DERIVABLE** | No event-type flag. Cannot distinguish quote updates from trades. |
| Price-impact proxy | **DERIVABLE WITH MATERIAL ASSUMPTIONS** | Can measure price change per tick, but without trade/quote separation, impact attribution is ambiguous. |

---

## 9. STORAGE / INFRASTRUCTURE AUDIT

### 9.1 Tick CSV Format

- **Format:** CSV, comma-separated, no header
- **Schema:** date, time, bid, ask, last, volume (6 columns for true tick data)
- **Encoding:** UTF-8
- **Compression:** None (raw CSV)
- **Partitioning:** None (single file per symbol)
- **Provenance:** MT5 tick data export, validated by `tick_validator.py`

### 9.2 Tick Parquet Converter

- **Location:** `research/staged_execution/tick_parquet_converter.py`
- **Schema:** source_row_ordinal (int64), date (string), time (string), bid (float64), ask (float64), last (float64), vol (float64)
- **Partitioning:** By YYYYMM (monthly partitions)
- **Compression:** Snappy (default)
- **Provenance:** SHA-256 hashing of all fields, source CSV, converter implementation, and specification
- **Production mode:** Only XAGUSD registered for production conversion. Firewall prevents unauthorized conversion.
- **Status:** Infrastructure exists but has NOT been run on the full tick datasets. Only the test fixture (1 row) exists as parquet.

### 9.3 M1 Derived Data

- **Format:** CSV with header (timestamp, open, high, low, close, volume)
- **Source:** Converted from tick data using `converter/tick_to_m1.py`
- **Price source:** Configurable (bid, ask, last, mid). Default is bid.
- **Volume:** Sum of tick volume per minute. For USATECHIDXUSD/XAUUSD/XAGUSD/BTCUSD, this is always 0 (tick volume is 0).

### 9.4 RF-001 / F-01 Prospective Data

- **Format:** CSV with header
- **Source:** Live MT5 M1 bar polling via `MT5TimeoutMarketFeed`
- **Not tick data.** These record M1 OHLCV bars, not individual ticks.

### 9.5 Storage Weaknesses

1. **No partitioning for tick CSVs.** Single 8-13 GB files per symbol. Reading specific date ranges requires full-file scans.
2. **No compression.** Raw CSV is ~3x larger than necessary.
3. **No deduplication.** Duplicate rows exist (0.07%–14.2% depending on symbol).
4. **No checksums.** No integrity verification for tick CSVs.
5. **No schema versioning.** No way to track schema changes over time.
6. **EURUSD mislabelled.** File named `*_mt5_ticks.csv` but contains M1 OHLCV data.
7. **Parquet conversion not executed.** Infrastructure exists but has not been applied to full datasets.

---

## 10. HISTORICAL VS PROSPECTIVE DATA

### 10.1 Historical Tick Data

| Symbol | Resolution | Fields | Coverage | Quality | Provenance |
|--------|-----------|--------|----------|---------|------------|
| USATECHIDXUSD | 1 sec | bid, ask, last (=bid), vol (=0) | 2023-09 to 2026-07 (1,043 days) | HIGH (validated PASS) | MT5 tick export |
| XAUUSD | 1 sec | bid, ask, last (=bid), vol (=0) | 2021-04 to 2026-04 (1,824 days) | HIGH (validated PASS) | MT5 tick export |
| XAGUSD | 1 sec | bid, ask, last (=bid), vol (=0) | 2021-07 to 2026-07 (1,825 days) | HIGH (validated PASS) | MT5 tick export |
| BTCUSD | 1 sec | bid, ask, last (=bid), vol (=0) | 2021-05 to 2026-05 (1,825 days) | HIGH (validated PASS) | MT5 tick export |
| EURUSD | **1 min** | **OHLCV (not tick)** | 2025-01 to 2026-04 (454 days) | M1, not tick | MT5 M1 export (mislabelled) |

### 10.2 Prospective Tick Data

**No prospective tick data is currently being captured.** The live recorder (RF-001) captures M1 OHLCV bars, not individual ticks. To capture prospective tick data, a new recorder would need to be built using MT5's `copy_ticks()` or `copy_ticks_from()` API.

---

## 11. MICROSTRUCTURE RESEARCH READINESS MATRIX

| Capability | Available? | Reliability | Direct/Derived | Research use |
|------------|-----------|-------------|----------------|--------------|
| Bid | YES | HIGH | DIRECTLY OBSERVABLE | Quote dynamics, spread analysis |
| Ask | YES | HIGH | DIRECTLY OBSERVABLE | Quote dynamics, spread analysis |
| Last/trade | PARTIAL | LOW | DERIVABLE WITH ASSUMPTIONS | `last` = `bid` always. No independent trade evidence. |
| Spread | YES | HIGH | DIRECTLY OBSERVABLE | Spread-state transitions, cost analysis |
| Quote updates | YES | HIGH | DERIVABLE RELIABLY | Event intensity, quote dynamics |
| Trade events | **NO** | N/A | NOT OBSERVABLE | Cannot distinguish trades from quotes |
| Tick arrival rate | YES | HIGH | DERIVABLE RELIABLY | Event-intensity transitions |
| Event ordering | PARTIAL | MEDIUM | DERIVABLE WITH LIMITATIONS | 1-sec resolution, duplicates prevent sub-second ordering |
| Aggressor direction | **NO** | N/A | NOT OBSERVABLE | No trade classification possible |
| Trade volume | **NO** | N/A | NOT OBSERVABLE | `vol` = 0 for all ticks |
| Tick volume | YES | HIGH | DERIVABLE RELIABLY | Count of ticks per interval |
| Order-book depth | **NO** | N/A | NOT AVAILABLE | Top-of-book only |
| Liquidity replenishment | **NO** | N/A | NOT OBSERVABLE | No depth data |
| Quote/trade sequence | **NO** | N/A | NOT OBSERVABLE | No event-type flag |
| Price impact proxy | PARTIAL | LOW | DERIVABLE WITH ASSUMPTIONS | Price change per tick, but ambiguous without trade/quote separation |

---

## 12. UNSUPPORTED-CLAIM REGISTER

The following claims CANNOT be supported by the available data:

| Claim | Why unsupported |
|-------|----------------|
| True order flow (buyer vs. seller initiated) | No trade classification flag. `last` = `bid` is broker behavior, not aggression evidence. |
| Institutional orders | No order-size data, no depth data, no participant identification. |
| Dealer inventory | No position data, no dealer identification. |
| Resting liquidity | No order-book depth data. |
| Order-book imbalance | No depth data. |
| Buyer/seller aggression | No trade classification. Lee-Ready not justified. |
| Real trade volume | `vol` = 0 for all tick data. Tick count is available but is not volume. |
| Trade events | No event-type flag. Cannot separate trades from quotes. |

---

## 13. NEWLY OBSERVABLE RESEARCH CLASSES

The following classes of mechanisms COULD become observable with the available tick data, subject to the limitations documented above.

### 13.1 Event-Intensity Transitions

- **Description:** Changes in the rate of quote updates per unit time. High-intensity periods may indicate active price discovery; low-intensity periods may indicate information vacuum.
- **Required fields:** Timestamp (available), bid/ask (available)
- **Whether fields exist:** YES
- **Whether directly testable:** YES — tick arrival rate per second/minute is derivable
- **Major limitations:** Cannot distinguish quote updates from trades. Intensity reflects quote churn, which may include both informational and non-informational events.

### 13.2 Spread-State Transitions

- **Description:** Changes in spread width over time. Spread widening may indicate uncertainty or reduced liquidity; spread tightening may indicate consensus or increased liquidity.
- **Required fields:** Bid, ask (available)
- **Whether fields exist:** YES
- **Whether directly testable:** YES — spread = ask - bid on every tick
- **Major limitations:** Spread is a top-of-book measure. Does not reflect depth or resilience.

### 13.3 Microstructure Volatility Transitions

- **Description:** Changes in the variance of quote returns at tick resolution. High micro-volatility may indicate active price discovery; low micro-volatility may indicate stale quotes.
- **Required fields:** Bid or ask (available), timestamp (available)
- **Whether fields exist:** YES
- **Whether directly testable:** YES — returns = diff(log(bid)) or diff(log(ask))
- **Major limitations:** Quote returns include both trade-induced and non-trade-induced changes. Cannot separate informational volatility from noise.

### 13.4 Quote Replenishment/Withdrawal Proxies

- **Description:** Patterns in bid/ask changes that suggest liquidity provision or withdrawal. Rapid bid changes at a price level may indicate liquidity provision; rapid ask changes may indicate withdrawal.
- **Required fields:** Bid, ask, timestamp (available)
- **Whether fields exist:** YES
- **Whether directly testable:** PARTIALLY — can measure quote change frequency and direction, but cannot observe the underlying order flow
- **Major limitations:** Quote changes are observed, but the intent (provision vs. withdrawal vs. adjustment) is not. Without depth data, replenishment/withdrawal is inferred, not observed.

### 13.5 Intraday Spread-Return Dynamics

- **Description:** The relationship between spread level and subsequent price returns at tick resolution. Wide spreads may predict larger returns (compensation for illiquidity); narrow spreads may predict smaller returns.
- **Required fields:** Bid, ask, timestamp (available)
- **Whether fields exist:** YES
- **Whether directly testable:** YES — spread and returns are both derivable
- **Major limitations:** Correlation is not causation. Spread-lead relationships may reflect shared drivers rather than causal effects.

### 13.6 Tick-Cluster Dynamics

- **Description:** Patterns in the clustering of multiple ticks within the same second. High clustering may indicate active trading; low clustering may indicate information vacuum.
- **Required fields:** Timestamp (available)
- **Whether fields exist:** YES
- **Whether directly testable:** YES — ticks per second is derivable
- **Major limitations:** Tick clustering reflects quote update frequency, not necessarily trade frequency.

---

## 14. M1 OHLCV FRONTIER — WHAT TICK DATA ADDS

### 14.1 Information Gained at Tick Resolution

| Information | M1 OHLCV | Tick Data | Gain |
|-------------|----------|-----------|------|
| Price path within minute | Hidden (only OHLC known) | Observable (tick-by-tick) | **GENUINE** — intrabar path reveals ordering of events |
| Spread evolution | Hidden (only snapshot) | Observable (tick-by-tick) | **GENUINE** — spread dynamics are invisible in M1 |
| Event intensity | Hidden (only volume) | Observable (ticks per second) | **GENUINE** — event rate is a new dimension |
| Quote update frequency | Not available | Derivable | **GENUINE** — quote churn is a new observable |
| Sub-minute volatility | Hidden (only range) | Derivable | **GENUINE** — micro-volatility is a new dimension |
| Bid/ask independence | Not available | Observable | **GENUINE** — bid and ask can move independently |
| Spread-return dynamics | Not available | Derivable | **GENUINE** — new research domain |

### 14.2 Information NOT Gained at Tick Resolution

| Information | M1 OHLCV | Tick Data | Gain |
|-------------|----------|-----------|------|
| Real trade volume | Not available (vol=0) | Not available (vol=0) | **NONE** — volume remains unavailable |
| Aggressor direction | Not available | Not available | **NONE** — trade classification not possible |
| Order-book depth | Not available | Not available | **NONE** — depth remains unavailable |
| Trade events | Not available | Not available | **NONE** — event-type separation not possible |
| Institutional flow | Not available | Not available | **NONE** — no participant data |

### 14.3 Summary

Tick data provides **genuine new information** in 7 dimensions: intrabar price path, spread evolution, event intensity, quote update frequency, sub-minute volatility, bid/ask independence, and spread-return dynamics. These are invisible in M1 OHLCV and represent a real expansion of the research space.

Tick data does **NOT** provide information in 5 critical microstructure dimensions: real volume, aggressor direction, order-book depth, trade events, and institutional flow. These remain unavailable regardless of data resolution.

---

## 15. RESEARCH-READINESS DETERMINATION

### **TICK-DATA AUDIT COMPLETE — PARTIALLY READY — PREREQUISITE DATA/INFRASTRUCTURE WORK REQUIRED**

### 15.1 What IS Ready

1. **Historical tick data exists** for 4 symbols (USATECHIDXUSD, XAUUSD, XAGUSD, BTCUSD) with 1,043–1,825 days of coverage, second-resolution, bid/ask present, spread calculable.
2. **Tick density is sufficient** (3–4 ticks/sec average, up to 94/sec for BTCUSD).
3. **Data quality is high** (validation PASS for all 4 symbols, no backward timestamps, no invalid numerics, no inverted spreads).
4. **Tick infrastructure exists** (validator, M1 converter, parquet converter) though parquet conversion has not been executed on full datasets.
5. **New research domains are genuinely accessible** at tick resolution: spread dynamics, event intensity, quote churn, micro-volatility, intrabar path.

### 15.2 What is NOT Ready

1. **EURUSD "tick" data is mislabelled.** The file contains M1 OHLCV, not tick data. Cannot be used for tick-level research without re-export from MT5.
2. **No prospective tick capture.** The live recorder captures M1 bars, not ticks. A new tick recorder would need to be built.
3. **`last` field provides no independent information.** It equals `bid` for all observations. Trade-price analysis is not possible.
4. **`volume` field is zero.** Real trade volume is unavailable. Volume-based research is not possible.
5. **No trade/quote separation.** Event-type flags are absent. Cannot distinguish informational events from noise.
6. **No order-book depth.** Top-of-book only. Depth-based research is not possible.
7. **Sub-second ordering not recoverable.** Duplicate timestamps (up to 14.2% for XAGUSD) prevent within-second event ordering.
8. **Timezone not recorded.** Broker server timezone is unknown. UTC conversion requires external knowledge.

### 15.3 Prerequisites for Tick-Level Mechanism Discovery

| Prerequisite | Status | Blocking? |
|-------------|--------|-----------|
| Historical tick data with bid/ask | AVAILABLE | No |
| Sufficient tick density | AVAILABLE | No |
| Trade/quote separation | NOT AVAILABLE | **YES** — limits observable mechanisms |
| Real trade volume | NOT AVAILABLE | **YES** — limits volume-based research |
| Order-book depth | NOT AVAILABLE | **YES** — limits depth-based research |
| EURUSD tick data (correct format) | NOT AVAILABLE | Minor — other symbols sufficient |
| Prospective tick recorder | NOT BUILT | **YES** — limits prospective validation |
| Sub-second timestamps | NOT AVAILABLE | Minor — 1-sec resolution sufficient for many research classes |
| Parquet conversion of full datasets | NOT EXECUTED | Minor — CSV is functional |

---

## 16. GOVERNANCE COMPLIANCE

| Check | Result |
|-------|--------|
| BASE-001 remains CLOSED / NOT BASE-ELIGIBLE | PASS |
| MECH-F01/F02/F03 remain unselected | PASS |
| No new mechanism selected | PASS |
| No Base formulation | PASS |
| No Base registration | PASS |
| No Stage 2 | PASS |
| No Stage 3 | PASS |
| No economic testing | PASS |
| No optimization | PASS |
| No threshold mining | PASS |
| Protected-forward artifacts untouched | PASS |
| RF-001 unchanged | PASS |
| F-01 unchanged | PASS |
| FB-001 unchanged | PASS |
| Runner uninterrupted | PASS |
| No broker orders | PASS |
| No production-code changes | PASS |
| No test changes | PASS |

---

## 17. RECOMMENDED PREREQUISITE ACTIONS

The following actions would close the identified gaps. These are recommendations only — implementation requires owner authorization.

### High Priority

1. **Build a prospective tick recorder.** Use MT5's `copy_ticks_from()` API to capture live ticks for USATECHIDXUSD (and optionally XAUUSD, XAGUSD). This would enable prospective tick-level validation.
2. **Re-export EURUSD tick data.** The current file is M1 OHLCV, not tick data. Re-export from MT5 with 6-column tick format (date, time, bid, ask, last, volume).
3. **Execute parquet conversion.** Run `tick_parquet_converter.py` on the 4 validated tick datasets to create partitioned, compressed, checksummed parquet files.

### Medium Priority

4. **Document broker timezone.** Determine the Exness-MT5Trial15 server timezone and record it for UTC conversion.
5. **Deduplicate tick data.** Remove duplicate rows (especially XAGUSD at 14.2%).
6. **Investigate `last` field semantics.** Confirm whether `last` = `bid` is a broker-specific behavior or a CFD-specific behavior. This determines whether trade-price analysis is possible on other brokers.

### Low Priority

7. **Add sub-second timestamps.** If MT5 provides millisecond timestamps, capture them. This would enable within-second event ordering.
8. **Add checksums to tick CSVs.** Enable integrity verification.

---

## 18. FINAL VERDICT

**TICK-DATA AUDIT COMPLETE — PARTIALLY READY — PREREQUISITE DATA/INFRASTRUCTURE WORK REQUIRED**

QuantForge has substantial historical tick data (4 symbols, 1,043–1,825 days, second-resolution, bid/ask present, high quality). This data enables genuine new research classes: spread dynamics, event intensity, quote churn, micro-volatility, intrabar path analysis, and spread-return dynamics.

However, critical limitations prevent full microstructure research:
- No trade/quote separation (event-type flags absent)
- No real trade volume (volume = 0)
- No order-book depth (top-of-book only)
- `last` field provides no independent information (= bid)
- EURUSD "tick" data is actually M1 OHLCV (mislabelled)
- No prospective tick capture (live recorder captures M1 bars)
- Sub-second event ordering not recoverable

**The data is sufficient to begin tick-level mechanism discovery in the domains of spread dynamics, event intensity, and quote-level microstructure. It is NOT sufficient for trade-flow, volume-based, or depth-based microstructure research.**

---

**END OF TICK-DATA CAPABILITY & MICROSTRUCTURE READINESS AUDIT V1**
