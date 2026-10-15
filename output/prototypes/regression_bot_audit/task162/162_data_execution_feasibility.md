# TASK162 — Data and Execution Feasibility (Phase B; metadata only, no outcomes)

**File:** `data/m1/USATECHIDXUSD_M1.csv` — SHA-256 recomputed from actual
bytes matches H01/ORD records (`39f25619…`, 56,818,845 bytes). Columns
timestamp/open/high/low/close/volume (OHLC-only). 906,815 rows,
2023-09-01→2026-07-10, monotonic, unique, tz-naive. No holdout bars this
reuse (handoff silent on universal holdouts; CAND025-RM-01 precedent ran
an owner-authorized M1 evaluation on this file).

## Findings (each independently blocking)

1. **Broker-time mapping: UNESTABLISHABLE.** File stamps are naive MT5
   server time (event_study protocols). The video's broker is unnamed;
   the feed's UTC offset is undocumented (repo's own audit: "GMT+2/+3
   inferred, undocumented"). Task78/85 gate: timestamp/timezone rule per
   instrument is OWNER_INPUT_REQUIRED and blocks execution authorization;
   ema_grab binding: formal timezone declaration is an owner item.
   Implementing 01:05/23:50 on the file's own clock without a mapping
   would test an unknown (possibly timeshifted) session — not the stated
   hypothesis. No conversion performed or assumed.
2. **Realistic costs: ABSENT.** OHLC-only bars (audit: "no bid/ask;
   execution costs would need a bound spread model"). No commission/
   slippage schedule for USATECH CFD on record; Batch-1 10/5/0 family is
   ETF-based. Tick-derived spreads would manufacture inputs under the
   same timezone taint. Using fixed 10/5/0 here = inventing costs
   (prohibited: no realistic net economics from invented costs).
3. **Execution-bar coverage: INADEQUATE.** Only ~79% of the 871 days have
   a 01:05 bar and ~79% a 23:50 bar on the file's own clock (~1 in 5 days
   missing one or both) — consistent with a daily feed break spanning
   midnight server time. The rule as stated (trade every eligible day)
   is unexecutable on ~21% of days; skipping them changes the rule and
   would need preregistration, which cannot precede resolved mapping.

**Phase B conclusion:** file integrity PASSES; every executability
requirement FAILS. No authorization record created (nothing meets the bar
for one). No engine built: with three independent blockers, implementation
machinery is premature and appears in no deliverable list.
