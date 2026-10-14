# TASK127 — Dataset Inventory (read-only, manifests/metadata only)

**Method:** Existing manifests, metadata, file listings, and provenance
records. No raw file scanning or copying. No data content accessed.

## Repository state

HEAD `666c1a9` / branch `main` / 235 worktree lines. HOLD / Active Research
NONE confirmed. TASK125–126 conclusions verified via hashes in prior
completion messages.

## Top-level data inventory

| Location | Contents | Asset count | Frequency | Notes |
|---|---|---:|---|---|
| `data/m1/` | 5 CSVs (BTCUSD, EURUSD, USATECHIDXUSD, XAGUSD, XAUUSD) | 5 | M1 | FX/metals/crypto; 2021-01→2026-10 |
| `data/fred/` | 4 CSVs (SP500, DJIA, NASDAQ100, NASDAQCOM) | 4 | Daily | Market indices, not individual assets |
| `data/tick/` | 5 tick CSVs | 5 | Tick | 13-14 GB total; not scanned |
| `data/tick_canonical/` | 4 symbol dirs (XAUUSD, XAGUSD, BTCUSD, USATECHIDXUSD) | 4 | Monthly parquet | 62 monthly files each |
| `data/f01/` | accrual state + snapshot + 1 study CSV | 1 | M1 | USATECHIDXUSD only |
| `data/fb001_orb/` | observer events + sessions | — | Event | Forward recorder data |
| `data/rf001/` | raw dir | — | — | RF-001 research data |
| `_t37 cache` | 11 NPZ files (M1 + H4 + ADX) | 11 | M1/H4 | FX/metals/crypto; 2021-01→2026-10 |
| `lane_b_batch1/data/` | 4 ETF CSVs + TB3MS | 4 + 1 RF | Daily/monthly | SPY/VEU/AGG/BIL; verified hashes |
| `lane_b_trend001/data_raw/` | 15 vendor CSVs | 15 | Daily | Yahoo/FRED; 14 used in PROTO-TREND-001 |
| `event_study_v1/` | 1 CSV (cross-market) | — | Event | 4 rows; not a return series |
| `event_study_v2/` | 1 CSV (cross-market) | — | Event | 60 rows; not a return series |

## Cross-sectional universe assessment

**Feasibility screen: ≥50 assets with compatible overlapping history and
credible cost inputs.**

| Candidate universe | Assets | Compatible overlap? | Costs? | Verdict |
|---|---|---|---|---|
| _t37 cache (FX) | 11 | Yes (same 2021-01→2026-10) | No (no cost inputs) | Too few; no costs |
| lane_b_batch1 (ETFs) | 4 | Yes (same panel) | Yes (Batch-1 frozen) | Too few |
| data/m1 (FX/metals) | 5 | Yes | No | Too few; no costs |
| lane_b_trend001 (mixed) | 15 | Partial (different vendors) | No | Too few; incompatible |
| FRED indices | 4 | Yes | No | Indices, not assets; too few |
| Cross-market event study | — | — | — | Not a return series |

**No candidate universe meets the 50-asset feasibility screen.**

## What is NOT present

- No CRSP-like equity cross-section
- No multi-stock return panel
- No point-in-time universe membership records
- No survivorship-bias-free asset universe
- No dataset with ≥50 individual assets having compatible overlapping
  daily/monthly returns and credible transaction-cost inputs
