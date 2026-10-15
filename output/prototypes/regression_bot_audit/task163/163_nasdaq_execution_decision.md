# TASK163 — NASDAQ Execution Definitions: Decision Report

## 0. Verification baseline (all re-checked this session)

TASK162 files intact (`61e0ab03…`, `a17e0eed…`); HEAD `9bac975`; HOLD /
Active Research NONE; tick-file header line read as metadata only
(`date,time,bid?,ask?,last?,vol?` pattern — 6 fields, no header row;
column semantics UNVERIFIED, see §3). No values analyzed, nothing
executed, nothing downloaded.

## 1. Identity: exact replication CLOSED, adaptation conditionally open

The video names no broker and establishes no clock mapping — exact
reproduction is impossible on current record (no inference can supply
the video broker's UTC offset). The QuantForge adaptation (Exness MT5
NASDAQ, i.e. the `USATECHIDXUSD` file whose feed the readiness audit
identifies as Exness-MT5Trial15) is a DIFFERENT test object, honestly
labeled as such — not a replication. It is separable from S2's reserved
identity decision (daily holding rule vs annual seasonal; TASK162 finding
stands, nothing new disturbs it) and collides with no closed family
beyond what TASK162 cleared.

## 2. Three-item decision table

| Item | Source-defined alternatives | Recommended decision + rationale | Authority status |
|---|---|---|---|
| A. Timestamp/timezone | (i) file stamps as-read, no conversion (fully reproducible, deterministic); (ii) my CAND-025 UTC-reading principle (reasoning, not a rule); (iii) owner-declared Exness server convention (task78/85 gate + ema_grab binding require owner input) | (i) as the only option verifiable entirely from records — WITH the explicit caveat that equivalence to any broker wall clock is unverified | Technically recommended; ADOPTION is owner-reserved (standing input gate) |
| B. Broker cost basis | (i) Batch-1 10/5/0 family as declared assumption (precedent: B3 assumptions; mismatch disclosed — ETF-based); (ii) tick-derived historical spreads (measured, not manufactured) + owner-frozen slippage/commission; (iii) owner-supplied schedule (none exists) | (ii): historical spreads from the tick file's bid/ask columns IF column semantics verify, plus frozen slippage/commission values. Minimum missing inputs: column verification, slippage + commission numbers, contract point value | Technical recommendation only; VALUES + processing job are owner acts |
| C. Missing sessions | (i) skip-and-count fail-closed (repo pattern: CAND-025/VS-TSMOM skips; no interpolation, no shifting); (ii) trade partial sessions (invents fills — rejected); (iii) interpolate (prohibited everywhere) | (i) + coverage reporting (fraction traded, missing-date list) + data-rejection bar (>5% yearly missingness → STOP; pattern transplant from FRED preregs, owner-confirmable) | (i) follows established pattern; the BAR transplant needs owner confirmation |

## 3. Route verdict: CLOSE_EXACT_REPLICATION_PROPOSE_ADAPTATION

Exact video replication is closed (unreconstructible broker/clock — a
data verdict on this candidate, not a strategy verdict). The Exness-clock
adaptation remains defensible CONDITIONALLY: Exness feed identity
verified, mechanism cleared, blockers reducible to three owner inputs
above. Not STOP_CANDIDATE: every blocker is obtainable in principle
(declaration, authorized processing, existing rule), and no record answers
the underlying intraday-drift question.

## 4. Smallest next action (all owner acts; single combined act possible)

(a) timestamp/timezone declaration for the feed clock; (b) slippage +
commission values (+ tick-column confirmation or supplied schedule);
(c) confirm the missing-session bar. Then: preregistration + separate
execution authorization (each its own act). No data collected, no
evaluation ran, no candidate created, no governance changed in this task.
HOLD/NONE unchanged.
