# TASK164 — NASDAQ Execution Definitions: Decision Record

## 0. Verification baseline (all re-checked this session)

TASK163 intact (`ad618c03…`); HEAD `9bac975`; HOLD / Active Research NONE;
tick canonical spec read in full (222 lines); M1 timestamp metadata
recomputed (no values analyzed). Prior B-blockers (unaltered files) all
reconfirmed.

## 1. Timestamp and timezone

- Video broker convention: CLOSED as unestablishable (broker unnamed;
  no record states its offset; not revisited).
- Dataset-clock convention (file stamps as-read, zero conversion):
  RECOMMENDED as the only fully record-verifiable, deterministic option —
  WITH mandatory honest relabeling (a file-clock test, neither an
  Exness-clock test nor an exact video replication). UTC reading noted as
  reasoning only, not authority.
- Verified Exness-clock mapping: UNAVAILABLE (no record states the
  offset; task78/85 input gate + binding owner-item requirement stand).
- **Authority: adoption of any convention is owner-reserved** (standing
  input gate). Recommendation ≠ selection.

## 2. Broker cost basis (tick semantics now VERIFIED)

Canonical tick spec V1 establishes the 6-column no-header format
(date, time, bid, ask, last=bid always, vol=0 always); the USATECH tick
header line matches it exactly, so historical bid/ask (hence spread) are
measurable under future authorized processing — no content was processed
in this task beyond the single header line. Still missing (owner-bound):
commission schedule (none on record), slippage assumption (none),
contract point value (for currency-denominated P&L; bps-on-notional needs
it not). Batch-1 10/5/0 family remains available only as a declared
assumption with disclosed ETF mismatch — not recommended over measured
spreads. No values invented; current quotes never substituted for history.

## 3. Missing sessions (precise denominator, timestamps only)

871 distinct dates; span 1044 calendar days (746 weekdays, 16 fully
absent). Execution bars on the file clock: BOTH present 521 days
(59.8%); EXACTLY ONE present 333 days (38.2%); NEITHER 17 days (2.0%).
Recommended: skip-and-count (no interpolation, no shifting), coverage
reported as these three fractions + missing-date list, data-rejection bar
at >5% yearly missingness (pattern transplant from FRED preregs,
owner-confirmable). Structural caveat recorded: missingness clusters
off-hours and is likely non-random — a future test must carry this as a
selection-bias limitation, not average over it. Bar adoption is
owner-reserved.

## 4. Verdict: OWNER_SELECTIONS_REQUIRED

Definitions are now fully specified and evidence-backed; every remaining
item is an explicit owner act: (a) timestamp-convention adoption,
(b) slippage/commission values (+ tick-job authorization for spread
measurement), (c) missing-session bar confirmation. No owner-reserved
choice was made here; no execution, collection, registration, governance,
commit, or push activity occurred. HOLD/NONE unchanged.
