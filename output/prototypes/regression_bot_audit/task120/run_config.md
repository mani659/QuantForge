# TASK120 run configuration — fixed pre-outcome (any deviation voids the run)

- data_file: data/m1/USATECHIDXUSD_M1.csv
- data_sha256: 39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6 (recomputed this session, exact match)
- data_meta: 906815 rows, 2023-09-01T00:00Z to 2026-07-10T20:14Z, monotonic, unique, tz-naive-as-UTC
- rule: V9 CAND-G0-025 (frozen triple hashes in approval record §2)
- signal: 08:30 America/New_York wall-time M5 bar TR > 3.0 x Wilder ATR(14); ATR over 14 M5 bars with close_time <= 08:30:00 ET, signal bar excluded; TR prevclose = 08:30:00 close
- tz mapping (single attempt, principled): naive timestamps read as UTC (no invented offset/DST; consistent with bare-timestamp quoting across H01/ORD/F01 records); NO second mapping attempt under any outcome (that would be a parameter search)
- resample: left-labeled 5-min bins, complete bars only (5/5 M1), last incomplete bar dropped
- entry: reversal at 08:35 open, dir = -sign(sig_close - sig_open); zero direction skips (counted)
- exit: 09:30 open; gross_pts = dir * (exit - entry); net = gross - 2.0 / gross - 3.0
- completeness: signal bar complete, 14 ATR bars present, 08:35/09:30 opens exist; else skip + count
- count rule (outcome-blind, pre-returns): count >= 157 proceeds (==157 record-consistent; >157 full-set primary + verification-subset subclause recorded UNEXECUTABLE: no G1 event list on any record); count < 157 STOPS with MEASUREMENT_INVALIDATED (no returns computed)
- statistics: T1 halves at median event date (odd extra to second half); means; 95% bootstrap CI B=10000 i.i.d. over events seed 20261013; Holm alpha 0.05 over {T3@2.0, T3@3.0}; T3 passes iff both lower bounds > 0 AND both Holm-adjusted p < 0.05; T4 majority-continuation flag over events with complete 08:35-08:40 bar (denominator reported)
- go/no-go: ALL of T1 + T3@2.0 + T3@3.0 (per frozen prereg §4); T4 recorded regardless; no auto-promotion in any outcome
- execution: single run, this config only; engine cand025_engine.py as reviewed (G4: 7/7 synthetic self-tests, determinism verified, one alignment bug found+fixed pre-data)
