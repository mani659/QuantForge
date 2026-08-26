# QUANTFORGE — ORD ECONOMIC / STRATEGY TRANSLATION
# FINAL INDEPENDENT PRE-EXECUTION AUDIT V2

FINAL governance gate before the one controlled ORD economic translation
execution. Read-only. Nothing executed; no PnL; no trade statistics; no
historical economic outcome inspected; no protocol, runner, recorder, cost
model, gate, alternative, or parameter modified.

## 1. Executive Verdict

**A — PASS — APPROVED FOR ONE CONTROLLED ECONOMIC EXECUTION.**

The V1.1.0 amended protocol (`ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md`,
SHA-256 `8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663`)
resolves every finding F1–F9 of the V1 audit, is internally deterministic, is
consistent with the frozen scientific protocol, the recorders' fail-closed
lifecycle, the persisted event/data artifacts, and the Liquidity-Sweep
precedents it inherits. Two independent researchers can implement the amended
protocol and obtain materially identical baseline economics without asking
another economic question, subject to the four non-blocking implementation
notes recorded in §18. The prior verdict (B — CONDITIONAL PASS) is upgraded.

## 2. Protocol Identity

| Item | Requirement | Verified |
|---|---|---|
| Version | V1.1.0 | PASS — header and §0 register V1.1.0 (precision-only amendment). |
| SHA-256 | `8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663` | PASS — computed on the persisted file, exact match. |
| V1.0.0 separated | original `ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1.md` unmodified | PASS — hash unchanged `50A08AAF...74F2`; not overwritten. |
| Scientific/economic gate change | none | PASS — §0/§20 explicitly register "No scientific or economic object changed"; §13 gate thresholds and structure preserved (only deterministic PF boundary-state evaluation added, claiming no threshold change). |
| Stands on its own | amended text is authoritative and complete | PASS — full document containing all operative rules inline; provenance references only, no required external reading for operation. |

## 3. Entry / No-Look-Ahead (F1)

Verified against §4 of the amended protocol and the persisted event table:

- `anchor_ts` in `event_table_all_markets.csv` is the breakout **bar start**,
  minute-aligned (e.g. `2021-05-23T07:34:00`), consistent with the M1
  convention that bar timestamps label bar starts. Confirmed from file.
- `T_B = anchor_ts + 60 s` is the instant the breakout candle close is
  observable (next minute boundary). Fully deterministic from the persisted
  table; no look-ahead.
- Entry minute = first eligible M1 tick minute whose interval begins at or
  after `T_B`, which by alignment is the minute immediately after the breakout
  bar. LONG = median ASK; SHORT = median BID. No tick before `T_B` contributes;
  ticks of the breakout bar's own minute never qualify.

**Critical question (answer):** If the breakout candle close is at `09:47:00`
(bar labeled `09:47`, close observable at `09:48:00`), then `T_B = 09:48:00`
and the **entire 09:48 minute is eligible** — its interval begins exactly at
`T_B` and every tick in it is strictly `≥ T_B`. This is the protocol's explicit
per-minute-median model and is exactly the "next fillable minute with a valid
per-minute median" rule recommended by the V1 audit's F1. It is deliberately
**not** identical to "first available tick after breakout close" (single tick),
but the difference is explicitly registered (median of the first eligible
minute), so it is not a silent divergence and cannot yield different
implementations.

Fallback chain is deterministic and forward-only: first eligible minute → ±5
minute (minutes at/after `T_B` only, ties to earlier) → market median
(`QUOTE_FALLBACK=market-median`) → exclusion
(`EXCLUDED_NO_QUOTE_COVERAGE`). No future-looking quote selection (§4 item 7).
**No look-ahead remains.**

Verdict: **PASS**.

## 4. Stop / Gap-Through (F4)

Verified against §5:

- Reconstructed levels from validated M1 with the registered OR windows
  (London 03:00–03:29:59 ET for XAUUSD/XAGUSD/BTCUSD; US cash 09:30–09:59:59 ET
  for USATECHIDXUSD), cross-checked to persisted `range_width`
  (`EXCLUDED_RANGE_MISMATCH` on mismatch).
- LONG stop = resting SELL at `High_OR`; trigger quote side = **BID**; exit at
  the BID of the first eligible stop-fill tick. SHORT stop = resting BUY at
  `Low_OR`; trigger side = **ASK**; exit at the ASK of the first eligible
  stop-fill tick. Deterministic for both directions.
- Close-based bar-by-bar evaluation from the bar after the entry bar
  (scientific invalidation preserved: `≤ High_OR` long, `≥ Low_OR` short).
- **Gap-through:** if the first executable quote at/after the stop-trigger
  moment is already beyond the level, the fill is that actual quote. **No
  favorable price improvement; no backfill to the theoretical level; no stop
  buffer.** Fill uses the tick's actual quote (event-driven), embedding observed
  spread — conservative executable reality.
- Stop-first on co-occurring structural-invalidation/horizon same-bar event
  (inherited scientific precedence).

Deterministic reading note (non-blocking): "stop-trigger bar timestamp" uses
the M1 bar-start convention (bar timestamp = minute start), so the first
qualifying trigger-side tick is taken at/after the trigger bar's start minute.
When the trigger bar is the same minute as the entry-fill minute (entry fill in
minute `anchor_ts+1`; first stop-check bar is `anchor_ts+1`), a same-minute
entry-then-stop is possible; this is a deterministic consequence that identical
for all implementers and is faithfully recorded by the ledger ordering
§18-M3.

Verdict: **PASS**.

## 5. Horizon (F5)

Verified against §6:

- Horizon = **120 literal wall-clock minutes from the executable entry
  timestamp** (`T_B = anchor_ts + 60 s`). Duration is the registered behavioral
  window and is not modified.
- Explicitly may cross the session boundary, NY cash close, 17:00–18:00
  rollover hour, and the next applicable session; no artificial truncation.
- Horizon exit: LONG → median BID of the horizon minute; SHORT → median ASK;
  same quote bridge as entry (exact minute → ±5 → market median → exclusion).
- Incomplete horizon (no M1 bar at `entry + 120 min`) → excluded under
  `EXCLUDED_NO_QUOTE_COVERAGE`/completeness rule, reported.
- Control horizon note: controls are NOT traded in this economic translation
  (protocol §2 — controls are the registered counterfactual and produce no
  executable trade). There is therefore no treatment/control horizon divergence
  possible; the horizon rule is uniform across the treatment-only universe.

Verdict: **PASS**.

## 6. MFE / MAE (F6)

Verified against §9:

- Source data = MT5 bid/ask ticks normalized to UTC minute keys (same data as
  the fills).
- LONG path uses the **BID** (exit side): `MFE = max_t(bid_t)`,
  `MAE = min_t(bid_t)`, excursions from the executable entry ask.
- SHORT path uses the **ASK** (exit side): `MFE = min_t(ask_t)`,
  `MAE = max_t(ask_t)`, excursions from the executable entry bid.
- Observation window explicitly defined: per eligible tick minute, sampled from
  the first eligible entry minute **through and including the actual exit
  minute** (stop fill moment or horizon exit).
- Unit = bp from the executable entry quote; formulas given.
- Explicitly **descriptive only**; cannot affect viability classification (§9
  and §12); the primary metric remains median net (Model A).

Note (non-blocking): the phrase "signed so `mfe ≥ 0` and `mae ≤ 0`" is loose
for a trade whose price never moves favorably (max excursion can be negative);
the governing formulas are deterministic max/min of the defined series, so
implementations agree (§18-M2).

Verdict: **PASS**.

## 7. Cost Model (F3, F2)

Verified against §4, §7, §9:

- **F2 (timezone):** tick timestamps explicitly UTC; normalized to the same UTC
  minute key as validated M1 before any quote lookup; M1 breakout timestamp
  matched in UTC; no local-time interpretation; DST cannot shift the fill
  lookup because all matching is on UTC minute keys. Confirmed against actual
  files: tick rows `YYYYMMDD,HH:MM:SS,bid,ask,last,vol` and M1 rows
  `timestamp,open,high,low,close,volume` are aligned to the same UTC minute.
- **F3 (identity, Model A):** `net_A = gross − RT(A)`, `RT(A) =
  (s_entry + s_exit)/2` (one half-spread per side). The verification is the
  algebraic identity `|(gross − RT(A)) − executable_quote_round_trip| ≤
  tol_rel × max(1, |gross|, |RT(A)|, |executable_quote_round_trip|)` with
  `tol_rel = 1e-6` (bp units). Pure floating-point guard; creates no economic
  threshold; is not a gate. No double-counting: fills already embed the observed
  half-spreads; the identity is a consistency check on listed views.
- Model B: `RT(B) = s_entry + s_exit` (full spread each side); commission
  (0/2/5/10 bp RT) and slippage (0/2/5 bp RT) bands are **additive on top for
  sensitivity only**, reported DESCRIPTIVELY ONLY, never used to select, tune,
  or classify. Model A is the primary and classification basis.
- Basis-point convention internally consistent: spreads in bp of mid;
  returns in bp of entry price.

Note (non-blocking): the ledger's `net_bp_B` column formula is not written out
in one line in §9; the derived unique reading from §7 (net_B = gross − RT(B),
spread-only; bands only in the descriptive sensitivity table) is recommended to
be pinned in the executing runner's ledger schema so identical columns result
(§18-M1). This cannot affect the primary metric or the gates.

Verdict: **PASS**.

## 8. Primary Economic Metric

Verified: **median net return per trade (bp), Model A (observed spread only)**
(§12). The metric is frozen and the gates use it directly (gate 1). No
substitution by mean, Sharpe, MFE, expectancy, or PF anywhere in the gates.
MFE/MAE are explicitly descriptive. All diagnostic metrics are reported for all
markets/halves/years — no selective reporting.

Verdict: **PASS**.

## 9. Viability Gates (F7, F8, year-concentration, OOS)

Verified against §13 and §12:

1. median net > 0 — pinned (median of per-trade `net_bp`, Model A).
2. cumulative net > 0 — **F7:** cumulative net = chronological sum of per-trade
   normalized net return in bp, in execution order; no compounding,
   reinvestment, weighting, annualization. Ordering is deterministic
   (chronological, by event/entry timestamp).
3. profit factor > 1.0 on net — **F8:** `PF = Σ(net_bp>0) / |Σ(net_bp<0)|`;
   no losses → `+∞` (passes), no wins → `0` (fails), no trades → `NaN /
   NOT EVALUABLE` (fails). Boundary handling deterministic at the gate.
4. year concentration: numerator = maximum over calendar years of |yearly net
   sum|; denominator = |total cumulative net| = |final chronological cumulative
   sum| (positive because gate 2 precedes gate 4). Rule: numerator/denominator
   ≤ 60% when total cumulative net ≠ 0. The natural single-scalar reading of
   "total |cumulative net|" (the final cumulative sum) is unique given F7; the
   `≠ 0` branch is handled by gate-ordering. Deterministic.
5. OOS half independently positive — pinned as **both** OOS median net > 0 AND
   OOS cumulative net > 0 (explicit conjunction; a positive dev / non-positive
   OOS always fails).

No gate editing after results; no arbitrary Sharpe thresholds. Final
classifications (ECONOMICALLY PROMISING — REQUIRES FORWARD VALIDATION /
BEHAVIORALLY VALIDATED / ECONOMICALLY NON-VIABLE; BTCUSD
NO-SCIENTIFIC-VERDICT caveat; EURUSD NOT SIMULATED) and overall disposition
rules preserved.

Verdict: **PASS** (these two critical definitions are uniquely pinned).

## 10. OOS / Development

Verified: per market, treatment events sorted by `trading_day`; **first 50% of
event days = DEVELOPMENT, last 50% = OUT-OF-SAMPLE**, chronological, fixed,
deterministic, and explicitly "identical convention to the Liquidity-Sweep
economic stage." The Liquidity-Sweep precedent implementation pins the tie rule
for odd day counts as `dev = first ⌊N_days/2⌋ days`, `oos = remainder`
(`scratch/lsweep_econ_v1/simulate.py:223-226`), which the ORD protocol inherits
by reference — so there is no date-midpoint ambiguity under the registered
convention. Nothing is fitted or tuned on development; no fitted parameters
exist; development cannot select a different baseline (single baseline).

Verdict: **PASS**.

## 11. Market Coverage

Verified: economic markets = XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD reported
strictly independently. BTCUSD is simulated and reported with the registered
**NO-SCIENTIFIC-VERDICT** caveat (scientifically HALTED; economic
classification, if any, does not authorize promotion without resolving the
scientific halt). EURUSD NOT SIMULATED (NOT REGISTERED / DATA-LIMITED). No
market may be removed or added after observing economics. Cross-market
classification structure preserved (§14).

Verdict: **PASS**.

## 12. Data Gates

Verified against §5, §10, §6:

- Tick schema (6-column `YYYYMMDD,HH:MM:SS,bid,ask,last,vol`) confirmed against
  actual files for all four registered markets.
- UTC timestamps; chronological within file; minute key aligned to M1 UTC.
- Duplicates: keep-first / chronological-sort convention identical to the
  scientific pipeline.
- Malformed rows: negative/non-positive prices and `bid > ask` rejected,
  invalid counts recorded per tick.
- Missing entry quote: §4 fallback chain (exact → ±5 → market median →
  exclusion) with flags.
- Missing/fallback exit quote: same bridge (§6).
- Incomplete horizon: excluded under completeness rule (§6).
- M1 reconstruction consistency: M1 input hashes must match the persisted
  implementation manifest; opening-range levels reconstructed from validated M1
  and cross-checked against persisted `range_width` (`EXCLUDED_RANGE_MISMATCH`).
- No hidden data-quality rules; all exclusions recorded with deterministic
  reason tags and never silently substituted.

Verdict: **PASS**.

## 13. Trade Ledger

Verified against §9: ledger CSV per market includes `market, trading_day,
direction, or_high, or_low, breakout_ts (anchor_ts), breakout_close
(entry_close), executable_entry_quote, entry_spread_bp,
structural_invalidation_level, exit_reason, exit_ts, executable_exit_quote,
exit_spread_bp, gross_bp (mid-to-mid), cost_bp (RT(A)), net_bp (Model A),
net_bp_B, mfe_from_entry_bp, mae_from_entry_bp, holding_duration_min,
quote_lookup, data_quality_flag` — all mission-required fields present. No trade
is deleted for being unfavorable; all rows including `EXCLUDED_*` (reason, no
economics) are reported. Same-day independent upper/lower simulation and
concurrent-window recording preserved. Cross-check identity per §9-F3.

Verdict: **PASS**.

## 14. Crash / Execution Lifecycle (F9)

Verified against protocol §17 and `research/orchestration/event_study_recorder.py`
(source read in full):

- Unique execution ID: `EXECUTION_<UTC ts>_<uuid>` generated at construction;
  immutable; persisted in manifest, journal, heartbeat, process identity.
- Isolated execution directory:
  `base/project/version/<execution_id>`; `mkdir(exist_ok=False)` — directory
  reuse is structurally impossible.
- Exactly-once: `complete_execution()` only from RUNNING; mutation guard
  (entry-script / helper / protocol SHA) verified before completion; artifact
  integrity gate (missing/unexpected) fail-closed → INVALIDATED + exception.
- Heartbeat: 5 s thread writing `execution_heartbeat.json` with pid,
  process_start_time, RSS, execution_id.
- Process identity: pid, process create time, platform, boot time captured at
  preflight (fail-closed if not capturable).
- No resume: no resume path exists in the recorder; a crashed run remains
  RUNNING/INTERRUPTED/INVALIDATED and is reconciled externally, never resumed;
  the next execution gets a new identity and a new directory. The V1.1.0 §17
  statement registers exactly this inheritance, including mandatory crash
  reconciliation before any subsequent execution.
- Fail-closed finalization on any integrity failure. Protocol does not
  interfere with or alter this infrastructure.

Verdict: **PASS**.

## 15. Reproducibility

Verified against §16/§17 and recorder: protocol SHA-256 (computed at start from
the pinned protocol file), runner SHA-256 (`entry_script_sha256`), M1 hashes
(`input_manifest_hash`, must match the scientific implementation manifest),
tick file SHA-256 computed at execution, execution ID, trade ledger CSVs, market
summaries JSON, development/OOS results, yearly results, cost-model identity
(Model A / Model B structure, bands), execution metadata with resource telemetry
(peak RSS capturable via the 5 s heartbeat RSS series plus runner-recorded
peak), artifact manifest (missing/unexpected/hashes), and the final economic
report. No critical economic evidence is unprescribed; intermediate artifacts
are written to disk (explicit DISC-025 persistence correction).

Verdict: **PASS**.

## 16. DISC-025 Capture Lesson

Verified: the economic measurement origin is the **actual executable entry
price** — the executable fill (ask for LONG, bid for SHORT) is the return origin
(§4 "The return origin used by §8 is the executable fill", §8 return
definitions use `P_entry`/`P_exit` as the ask/bid executable fills). It cannot
revert to the opening-range edge, a theoretical breakout price, a pre-entry
reference, or the behavioral MFE reference. The scientific response was already
entry-anchored (scientific protocol §5/§8 and adjudication), and the economic
stage preserves the same conceptual origin at the executable quote.

Verdict: **PASS**.

## 17. Economic Firewall

Verified (§18): no alternate entries, exits, stops, ATR/candle-high/low/
volatility buffers, partial exits, trailings, break-evens, filters,
confluence, ML/HMM/K-means, or parameter optimization. The registered baseline
succeeds or fails on its own. No economic result, whether positive or negative,
auto-authorizes any alternative translation or optimization.

Verdict: **PASS**.

## 18. Findings Table

| Area | Verdict | Severity | Finding |
|---|---|---|---|
| Protocol identity | PASS | — | V1.1.0; SHA exact; V1.0.0 separate/unchanged; no gate change. |
| Entry bridge | PASS | — | T_B = anchor_ts+60 s; first eligible minute median ASK/BID; fallbacks registered; DISC-025 origin preserved. |
| No-look-ahead | PASS | — | No tick before T_B; whole next minute is explicitly the model; pinned; no future-looking selection. Two implementations cannot diverge. |
| Tick timezone | PASS | — | UTC stated and applied to UTC minute keys; DST cannot shift lookup; confirmed against file layouts. |
| Stop | PASS | — | Resting orders at OR edges; trigger side BID/ASK per direction; close-based bar-by-bar trigger; stop-first. |
| Gap-through fill | PASS | — | Fill at actual first executable quote beyond level; no backfill; no improvement; no buffer. |
| Horizon | PASS | — | 120 literal wall-clock from entry; crosses all boundaries; deterministic bridge + completeness exclusion. |
| MFE/MAE | PASS | — | Executable path, correct quote sides, window through actual exit, bp, descriptive only, cannot gate. |
| Cost accounting | PASS | — | net_A = gross − RT(A) identity with 1e-6 relative FP tolerance; Model B full-spread + additive descriptive bands; no double count; no new threshold. |
| Cumulative net | PASS | — | Chronological sum in execution order; no compounding/reinvestment/weighting/annualization. |
| Profit factor | PASS | — | Defined with +∞ / 0 / NaN boundaries; handled deterministically at gate 3. |
| OOS split | PASS | — | 50/50 by event days, chronological; odd-count tie rule pinned by the referenced Liquidity-Sweep convention (dev = first ⌊N/2⌋ days); reporting-only; nothing fitted. |
| Viability gates | PASS | — | All five pinned; year-concentration numerator/denominator and OOS "positive" (median AND cumulative) uniquely defined. |
| Market coverage | PASS | — | 4 markets independent; BTCUSD NO-SCIENTIFIC-VERDICT caveat; EURUSD excluded; no post-hoc removal. |
| Data gates | PASS | — | Schema/UTC/duplicates/malformed/quote-final-fallback/incomplete-horizon/range cross-check all deterministic and reported. |
| Trade ledger | PASS | — | All mission columns present; no deletion of unfavorable trades; EXCLUDED_* rows reported. |
| Resource safety | PASS | — | Streamed ticks, sequential markets, no multi-market tick loading, heartbeat RSS, isolated dir, fail-closed. |
| Crash lifecycle | PASS | — | Unique ID, isolated dir, exactly-once, no resume, no dir reuse, heartbeat, process identity, reconciliation, fail-closed. |
| Reproducibility | PASS | — | All required evidence persisted; tick hashes, runner/protocol/M1 hashes, ledger, stats, halves, years, telemetry, manifest, report. |
| Economic firewall | PASS | — | No alternatives, buffers, filters, ML, or optimization authorized; baseline stands alone. |
| Executability | **PASS** | — | Two independent researchers implementing the amended protocol obtain materially identical baseline economics without asking another economic question. |

Non-blocking implementation notes (no severity, do not affect verdict; to be
followed by the executing runner so the ledger is written identically):

- **M1 (ledger schema):** write `net_bp_B = gross_bp − RT(B)_bp` (spread-only,
  full spread each side); commission/slippage bands appear only in the separate
  descriptive sensitivity table. Pinning this one line removes any residual
  doubt about the `net_bp_B` column.
- **M2 (MFE/MAE sign phrase):** rely on the formulas, not the "mfe ≥ 0 / mae
  ≤ 0" phrase, for a trade whose price never moves favorably (max excursion can
  be negative); both implementers compute the defined max/min series.
- **M3 (same-minute entry/stop):** when the first stop-check bar is the
  entry-fill minute, entry (minute median) and stop (first qualifying tick) can
  occur in the same minute; record ledger rows in chronological tick order with
  the entry median established at the minute's close for ordering purposes.
- **M4 (split tie rule):** register `DEVELOPMENT = first ⌊N_days/2⌋ days`,
  `OOS = remainder`, matching the referenced Liquidity-Sweep convention.

## 19. Final Governance Decision

**A — PASS — APPROVED FOR ONE CONTROLLED ECONOMIC EXECUTION.**

The amended V1.1.0 protocol stands on its own. Every material ambiguity raised
by the V1 audit (F1–F9) is resolved deterministically, and the requested
critical definitions (year-concentration numerator/denominator, OOS
"positive," split tie rule, entry fill timing) are uniquely pinned by the
amended text and its registered references. No blocker remains.

## 20. Exact Next Task

Proceed to **ONE controlled economic execution** of the amended V1.1.0 protocol
against the persisted scientific treatment events and observed MT5 quotes,
using the EventStudyRecorder lifecycle (exactly-once; isolated execution
directory; heartbeat; fail-closed artifact gate), with markets processed
sequentially and tick files streamed. This is a single registered baseline run
(Model A primary; Model B descriptive; no alternatives). After completion and
artifact-integrity verification, the result proceeds to the **economic
adjudication**; only if a market is classified ECONOMICALLY PROMISING does the
separately-governed forward/demo validation stage follow. No optimization
follows automatically from any result; no alternative translation is authorized
automatically.

## 21. Integrity

- Strictly read-only execution of this audit: no economic simulation, no PnL,
  no trade statistics, no historical economic outcome inspection, no ORD
  rerun, no protocol/runner/recorder/reconciliation modification, no cost-model
  or gate change, no alternative testing, no parameter optimization, no
  EA/demo/live, no commit, no push.
- The only new repository artifact is this document:
  `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_AUDIT_V2.md`.
- Facts verified from persisted sources: hashes of both protocol files; event
  table header/sample rows (`anchor_ts` convention, `range_width`, `entry_close`);
  scientific protocol entry/invalidation/horizon sections; adjudication market
  verdicts; tick and M1 file layouts; the EventStudyRecorder source in full;
  the Liquidity-Sweep economic precedent and its split implementation.
- The amended protocol itself was not modified during this audit.