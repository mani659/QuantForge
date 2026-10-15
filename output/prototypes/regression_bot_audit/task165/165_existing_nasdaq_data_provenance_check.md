# TASK165 — Existing NASDAQ Data Provenance and Execution-Readiness Check

## 0. Verified starting state

HEAD `9bac975` / `main`; HOLD / Active Research NONE (re-verified);
TASK164 intact (`6c756533…`). Original video strategy: NOT reproducible
(broker and clock mapping unestablishable — TASK163/164 findings stand,
not re-litigated). QuantForge adaptation (Exness-clock fixed window):
conditionally eligible per TASK162 (mechanism cleared), blocked on the
inputs below.

## 1. Shortlisted sources and provenance (read-only inspection only)

| # | Path | Symbol | Provenance (evidenced) | Type / span | Hash (established this session unless noted) |
|---|---|---|---|---|---|
| C1 | `data/m1/USATECHIDXUSD_M1.csv` | USATECHIDXUSD (label; broker binding unverified beyond feed family) | Exness-MT5Trial15 feed family (readiness audit); H01/ORD manifest row | M1 OHLC, 2023-09→2026-07, 906,815 rows | `39f25619…468050` (H01 match, re-verified) |
| C2 | `data/tick/USATECHIDXUSD_mt5_ticks.csv` | USATECHIDXUSD (label) | Same feed family; 6-col no-header format matches canonical spec V1 (bid=col2, ask=col3 — header line only, values unexamined) | Tick bid/ask, from 2023-09, 8,801,376,883 bytes | `56105bda…78141ba` (new baseline) |
| C3 | `.../fx_h4inv_adx_prep/_t37_m1_USTECm.npz` | USTECm (label) | MT5-derived per task51 §11; OHLC+spread keys verified | M1 + spread, 1,970,042 rows, 2021→2026 per record | `9375c86e…cc31d` (new baseline) |
| C4 | `data/tick_canonical/USATECHIDXUSD/` | USATECHIDXUSD (label) | Canonical spec (broker server tz, preserved as-is); 36 monthly parquets from 2023-09 (directory listing only) | Tick parquet | Not hashed (directory-level only; per-file hashes deferred to authorized use) |
| C5 | `data/fred/fred_NASDAQ100.csv` | NASDAQ100 index | FRED; price-only | Daily closes, 1986→2026, 10,602 rows | `1196c3f2…51ec7e` (H01 match) |

No other candidate sources were found; the search stopped at five per
scope. Provenance gaps are marked, not inferred.

## 2. Execution-readiness screen (strongest candidate first)

Best case C1+C2 combined (M1 bars + tick spreads, same feed family):

1. Observations at 01:05/23:50 — PARTIALLY: M1 bars exist at both stamps
   on ~60% of days (TASK164); tick coverage at those stamps unmeasured.
2. Clock mapping — NOT ESTABLISHED: naive stamps throughout; feed offset
   undocumented; task78/85 input gate + binding owner-item stand.
3. Bid/ask fields — PARTIALLY: tick columns verified, values unexamined;
   M1 files have none. Commission/slippage/contract specs: NOT
   ESTABLISHED anywhere.
4. Session calendar — NOT ESTABLISHED: no calendar on record; weekday
   inference only; ~40% day-loss under skip-and-count with likely
   non-random missingness.
5. Contract/commission/costs — NOT ESTABLISHED (see §3).
6. Holdout-free range — VERIFIED: no universal holdout on record;
   CAND025-RM-01 precedent ran an authorized M1 evaluation on this file.

C3/C4 inherit the same clock/cost/calendar gaps with thinner records.
C5 FAILS outright: daily granularity cannot support 01:05/23:50 execution.

## 3. Route decision: B — EXISTING_DATA_INSUFFICIENT

No inspected source demonstrates a credible route: every candidate fails
at least the clock mapping, and all fail costs and calendar. This is NOT
a provenance failure (sources are identified and hashed) — it is a
capability failure, so B, not C. Park the candidate unless ALL of the
following arrive together: (a) owner timestamp/timezone declaration,
(b) slippage + commission values (plus tick-processing authorization for
spread measurement), (c) missing-session bar confirmation. No acquisition
campaign is proposed — the gap list above is already minimal, and tick
data already on disk covers the only measurable remainder.

## 4. Next action, if any (all owner acts; none taken here)

Single combined owner act supplying (a)–(c); then preregistration; then
separate execution authorization. Absent that, no further work is
authorized or useful on this candidate — stop spending here.

## 5. Actions not performed; unresolved owner decisions

No values analyzed for performance; no spreads computed; no download,
collection, holdout, runtime, registration, governance, commit, or push
activity. Unresolved (unchanged): timestamp convention, cost values,
missing-session bar, and any evaluation authorization. HOLD/NONE intact.
