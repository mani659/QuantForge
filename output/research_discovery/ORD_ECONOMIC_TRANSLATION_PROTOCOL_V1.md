# QUANTFORGE — ORD ECONOMIC / STRATEGY TRANSLATION PROTOCOL V1

FROZEN BEFORE COMPUTATION. This document registers the single baseline economic
translation of the scientifically supported ORD V1.1.0 behavioral result. No
economic value is computed here; no alternative is tested; nothing is tuned.

## 0. Identity and Scope

- **Stage:** post-adjudication economic / strategy translation of the ORD
  V1.1.0 behavioral result.
- **Authorizing adjudication:** `output/research_discovery/ORD_SCIENTIFIC_RESULTS_ADJUDICATION_V1.md`
  — **A — SCIENTIFICALLY SUPPORTED** (XAUUSD, XAGUSD, USATECHIDXUSD SUPPORT;
  BTCUSD scientifically HALTED; EURUSD NOT REGISTERED / DATA-LIMITED).
- **Frozen scientific protocol:** `output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md`
  (V1.1.0, SHA-256 `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06`).
  No scientific object is modified. No parameter is changed.
- **Frozen definition lock:** `output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md`.
- **Scientific execution (authoritative source of events):**
  `output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/`
  (state COMPLETED; manifests `missing_artifacts=[]`, `unexpected_artifacts=[]`).
- **Governance reference:** DISC-025 (Liquidity Sweep / Reversal) — including
  its mandatory lesson that the response must be entry-anchored and its
  observed-cost methodology, and DISC-023/024 (unrelated, not reused).
- **Baseline registration:** the single baseline below is registered BEFORE any
  computation. One baseline implementation only. No alternative entry/exit/stop
  is tested. No parameter search, no ML, no EA, no demo/live.
- **Protocol identity:** this document. Its SHA-256 is computed and persisted by
  the economic-run metadata at execution start (standard quantification practice
  established by the Liquidity-Sweep pre-economic audits).

---

## 1. Executive Verdict

**NOT DECIDED — this protocol is frozen before computation.** This section
exists to register, before any result, that this stage determines whether the
validated ORD behavior can be converted into ONE mechanically executable
baseline trade that survives observed market friction. The possible final
classifications are registered in §13. No verdict is implied here.

---

## 2. Scientific Object Being Translated

Translated object (unchanged from the adjudication): **opening range →
close-break → entry at the breakout-close → structural invalidation →
post-entry directional movement.**

- **Scientific response anchored at the entry:** the registered behavioral
  response is the unconditional 120-minute directional return from the actual
  breakout-candle close. This is the DISC-025 lesson already satisfied by the
  scientific object (Definition Lock §15: Economic Capture Requirement PASS) —
  the economics are measured from the same conceptual origin as the response.
- **What is translated:** only the treatment (breakout) events from the
  persisted scientific event table. Controls are NOT traded (they are the
  registered counterfactual and produce no executable trade).
- **What is NOT translated:** no inversion, no rescue, no filters, no
  confluence, no alternative horizon, no alternative widening.

---

## 3. Baseline Entry

Frozen exactly as the scientific definition:

- **Entry event:** first qualifying close-break per direction per trading day
  (treatment rows in the persisted event table):
  - LONG: first M1 close `> OpeningRange_High` (strict).
  - SHORT: first M1 close `< OpeningRange_Low` (strict).
- **Entry price (scientific):** the breakout candle close (`entry_close` in the
  persisted event table).
- **Direction:** LONG breakout → BUY; SHORT breakout → SELL. Direction is fixed
  at the event and never changed by later price action.
- **No** next-bar entry, limit entry, pullback entry, or confirmation delay.

The executable fill is defined in §4.

---

## 4. Execution Bridge

The scientific event is an M1 candle close; the economic stage must attach an
executable quote. Frozen deterministic bridge (registered before computation):

**Entry fill rule.** The entry minute = the minute of the breakout candle
(`anchor_ts`, UTC, truncated to the minute). Execution:

1. **Long entry:** fill at the FIRST available observed ASK quote at or
   immediately after the breakout-close timestamp.
2. **Short entry:** fill at the FIRST available observed BID quote at or
   immediately after the breakout-close timestamp.
3. Per-minute quote aggregation (validated Liquidity-Sweep methodology):
   observed tick file rows in the entry minute are aggregated to a median bid
   and median ask; the fill uses the median ask (long) / median bid (short) for
   that minute.

**Bid/ask selection:** for a LONG entry the ask is used (the price a buyer pays);
for a SHORT entry the bid is used (the price a seller receives). This embeds the
observed half-spread in the fill and is the executable-quote origin of the round
trip (DISC-025 requirement).

**Exact-timestamp rule:** if no tick exists at the exact entry minute
(`anchor_ts` truncated), fallback in this deterministic order:
1. **±5-minute window:** the nearest available minute with an observed
   aggregation; ties resolve to the earlier minute; window fixed at ±5 minutes
   (same window as the validated sweep cost lookup — a registered coverage rule,
   not a tuning parameter).
2. **Market-median fallback:** if still unavailable, use the market median
   bid/ask across ALL observed minutes of that market, and flag the trade
   `QUOTE_FALLBACK=market-median`.
3. **No acceptable quote:** if even the market-median is undefined (no usable
   tick coverage for the market), the trade is EXCLUDED under the pre-registered
   data-quality rule (§11), recorded as `EXCLUDED_NO_QUOTE_COVERAGE`, and
   reported — never silently substituted.

**Entry-close vs executable entry:** the scientific `entry_close` and the
executable fill (ask/bid) differ by the observed half-spread; BOTH are recorded
per trade (§9). The return origin used by §8 is the executable fill, so gross
and net economics are anchored at the actual executable quote — the DISC-025
lesson.

---

## 5. Structural Invalidation

Frozen direct translation of ORD invalidation. The structural levels
(`OpeningRange_High` / `OpeningRange_Low`) are not persisted in the scientific
event table, so they are reconstructed deterministically from the validated M1
record using the FROZEN window definitions (protocol V1.1.0 §4):

- XAUUSD, XAGUSD, BTCUSD: 30 bars `03:00:00–03:29:59 ET` inclusive
  (London opening anchor); `High_OR = max(high)`, `Low_OR = min(low)`.
- USATECHIDXUSD: 30 bars `09:30:00–09:59:59 ET` inclusive (US cash open);
  `High_OR = max(high)`, `Low_OR = min(low)`.
- Timezone: deterministic UTC→America/New_York (zoneinfo), identical to the
  scientific pipeline; day is the event's `trading_day`.
- **Integrity cross-check:** reconstructed `High_OR − Low_OR` must equal the
  persisted event-table `range_width`; any mismatch flags and excludes the trade
  under §11 (`EXCLUDED_RANGE_MISMATCH`) — never silently accepted.

**Stop rule (registered treatment — the structural level itself):**
- LONG: exit when price closes back at or below `OpeningRange_High` (a
  subsequent M1 close `≤ High_OR`).
- SHORT: exit when price closes back at or above `OpeningRange_Low` (a
  subsequent M1 close `≥ Low_OR`).

**Executable stop fill:** the invalidation is close-based; the executable stop
is a resting order AT the structural level:
- LONG stop → SELL, fill at `OpeningRange_High`.
- SHORT stop → BUY, fill at `OpeningRange_Low`.
- The stop trigger is evaluated bar-by-bar from the bar AFTER the entry bar; the
  fill price is the structural level itself (a resting-stop fill). This is the
  smallest deterministic execution assumption and does not introduce any buffer,
  ATR, candle-high/low, volatility, or trailing logic.

**Fill ordering (frozen, no ambiguity):**
1. If the structural-invalidation close and the horizon exit close occur on the
   SAME bar/minute, the STOP is evaluated FIRST (conservative; inherited from
   protocol V1.1.0 §7 "invalidation is evaluated first").
2. If a stop condition is satisfied by an M1 close but the executable quote
   resolves at a later tick, the fill is at the structural level at the stop bar
   timestamp (a resting-stop price does not depend on the arrival of a later
   tick); the spread at the stop minute is the observed spread (§7).

---

## 6. Horizon Exit

- **Horizon:** 120 minutes wall-clock from the entry bar (`entry + 120 min`), the
  registered behavioral window.
- **Horizon exit rule:** unless the structural invalidation fires first, exit at
  the first executable quote available at the 120-minute horizon:
  - LONG exit → SELL at the median BID of the horizon minute.
  - SHORT exit → BUY at the median ASK of the horizon minute.
- **Quote availability:** same bridge as §4 (exact minute → ±5-minute fallback →
  market-median → pre-registered exclusion `EXCLUDED_NO_QUOTE_COVERAGE`).
- **Horizon completeness:** if the M1 bar at `entry + 120 min` does not exist
  (incomplete horizon), the trade is excluded before inference under the
  pre-registered rule (§11) and reported — the same completeness rule as the
  scientific protocol §9.
- **Ordering with stop:** stop-first on any co-occurring timestamp (§5).

---

## 7. Cost Model

Use OBSERVED MT5 bid/ask tick data. No assumed spread.

**Data sources (all four registered markets have compact 6-column tick files
`YYYYMMDD,HH:MM:SS,bid,ask,last,vol`):**
- `data/tick/XAUUSD_mt5_ticks.csv`
- `data/tick/XAGUSD_mt5_ticks.csv`
- `data/tick/USATECHIDXUSD_mt5_ticks.csv`
- `data/tick/BTCUSD_mt5_ticks.csv`
- (XAGUSD additionally inherits the validated per-minute aggregate precedent
  `output/xagusd_cost_viability_v1/xagusd_minute_aggregates.csv` as a
  deterministic cross-check; the raw tick file is the primary source.)

**Per-minute aggregation:** valid ticks (positive bid, positive ask, `bid ≤ ask`)
in each minute → median bid, median ask, tick count `nticks`. Invalid ticks are
counted and rejected in the data gates (§11).

**Spread metric:** `s[m] = (ask_med − bid_med) / mid_med × 10^4` in bp at minute m,
`mid_med = (bid_med + ask_med)/2`.

**Round-trip cost conventions (inherited from the Liquidity-Sweep V1 economic
stage and the XAGUSD precedent):**
- **Model A (standard, PRIMARY):** `RT(A) = (s_entry + s_exit) / 2` (one
  half-spread each side).
- **Model B (conservative):** `RT(B) = s_entry + s_exit` (full spread each side).

**Unobserved components:** no broker commission schedule exists in the
repository — no commission is invented. A clearly labeled conservative
transaction-cost sensitivity is reported DESCRIPTIVELY ONLY and is never used to
select or tune the baseline: commission band `0 / 2 / 5 / 10` bp RT and slippage
band `0 / 2 / 5` bp RT (identical bands to the validated sweep economic stage).

**Charge structure (Database lineage: the net return is computed on the observed
spread; explicit cost bands are additive on top for sensitivity only):**
- Net return (primary, Model A, observed-spread-only) = gross (mid-to-mid,
  §8) − RT(A).
- Since fills use ask/bid directly (§4, §6), the executable-quote round trip
  equals mid-to-mid gross − RT(A) by construction; both views are reported and
  must agree.

**Reporting per market (`cost_identity` must record):** exact quote coverage
(% of event-entry/exit minutes with any tick aggregation), exact-minute match
rate, fallback rate (by fallback tier), market-median fallback rate, exclusion
counts, observed spread distribution (median / mean / p25 / p75 / p90). Any
market whose tick coverage is inadequate (i.e., exact+bridged quote availability
< 90% of required minutes) is flagged `INADEQUATE_TICK_COVERAGE` and reported
prominently; exclusions still follow §11.

---

## 8. Position / Notional Convention

- **Fixed notional:** 1 normalized unit per trade (instrument-agnostic).
- **No** compounding, no Kelly, no risk-percent optimization, no position
  sizing search.
- Per-trade returns are expressed in **basis points** of the executable entry
  price, so markets are compared unit-free without pretending raw price/dollar
  magnitudes are equivalent.
- **Cross-market equivalence note:** raw bp magnitudes are compared only
  structurally (sign and ranking structure), never as interpolated currency
  economics. Actual broker contract specifications (contract size, margin) are
  recorded as KNOWN/UNKNOWN in the market summaries: what is known (per-trade
  bp economics, observed spreads) is reported; what remains unknown (dollar
  notional per lot per broker) is declared UNKNOWN and is not assumed.

**Return definitions (per trade, signed by direction):**
- LONG: `R = (P_exit − P_entry) / P_entry × 10^4`
- SHORT: `R = (P_entry − P_exit) / P_entry × 10^4`
where `P_entry` / `P_exit` are the mid-to-mid executable references for GROSS
and the ask/bid executable fills (buy price for long in, sell price for long
out; sell price for short in, buy price for short out) which already embed the
observed spread.

---

## 9. Trade Accounting

Persist one trade-ledger CSV per market with EXACTLY these columns (from §18
mission requirements):

`market, trading_day, direction, or_high, or_low, breakout_ts (anchor_ts),
breakout_close (entry_close), executable_entry_quote, entry_spread_bp,
structural_invalidation_level, exit_reason {STRUCTURAL_INVALIDATION | HORIZON |
EXCLUDED_*}, exit_ts, executable_exit_quote, exit_spread_bp, gross_bp
(mid-to-mid), cost_bp (RT(A) observed spread), net_bp (primary, Model A),
net_bp_B, mfe_from_entry_bp, mae_from_entry_bp, holding_duration_min,
quote_lookup {exact | fallback±k | market-median}, data_quality_flag`

- **cross-check fields:** gross_bp vs executable-quote round trip
  (gross − RT(A) must equal the ask/bid fill round trip within 1e-6).
- **Do not delete** losing or invalid trades after observation; all rows are
  reported, including `EXCLUDED_*` rows (which carry a reason, no economics).
- **Overlap note:** same-day upper/lower events are simulated independently
  (identical to the sweep validation); concurrent windows are recorded.

---

## 10. Data Gates (pre-registered; exclusions are reported, never silent)

1. **Input hashes:** M1 SHA-256 must match the persisted
   `implementation_manifest.json` `input_manifest_hash` for XAUUSD, XAGUSD,
   USATECHIDXUSD, BTCUSD (already verified byte-exact in prior audits).
2. **Tick integrity:** validate schema of each tick file; timestamps
   chronological within file; reject negative/non-positive prices and
   `bid > ask`; record per-tick invalid counts.
3. **No duplicate-handling drift:** identical keep-first / chronological-sort
   convention as the scientific pipeline.
4. **M1 coverage:** sufficient bars for the entry window, the stop scan, and the
   +120-minute horizon; completeness per §11.
5. **Quote coverage around entry/exit:** exact minute → ±5 → market median →
   exclusion (§4, §6, §7).
6. **Range-level integrity:** reconstructed `High_OR − Low_OR` vs persisted
   `range_width` (§5).
7. Exclusions are recorded with a deterministic reason tag and summarized in the
   market summary; excluded trades never enter the economic metrics.

---

## 11. Development / OOS Split

- **Split (frozen before computation):** per market, treatment events sorted by
  `trading_day`; **first 50% of event days = DEVELOPMENT**, **last 50% of event
  days = OUT-OF-SAMPLE**. Chronological, fixed, deterministic (identical
  convention to the Liquidity-Sweep economic stage).
- The split is for **temporal reporting only**: nothing is fitted, tuned, or
  selected on the development half. There are no fitted parameters in this
  one-baseline design.
- Reporting: full / development / OOS for every market, plus per-calendar-year.

---

## 12. Primary Economic Metric

**Primary: median net return per trade (bp), Model A (observed spread only).**

Core economic diagnostics, all reported per market (full / dev / OOS / year):

- total trades; trades / month; win rate; median win; median loss;
- profit factor (gross wins / |gross losses|, and same on net, Model A);
- gross median; net median; cumulative net bp (Model A);
- maximum drawdown in cumulative bp (Model A);
- stop / invalidation rate; horizon-exit rate;
- per-trade spread distribution; quote-lookup breakdown; exclusion counts.

**No single metric is reported selectively.** All are reported for all markets,
halves, and years.

---

## 13. Economic Viability Gates

Registered BEFORE computation. A market passes the baseline economic stage only
if ALL of the following hold (Model A, observed spread only):

1. **median net return per trade > 0**;
2. **cumulative net result > 0**;
3. **profit factor > 1.0** on net (Model A);
4. **no severe calendar-year concentration:** the maximum |yearly net sum|
   ≤ 60% of total |cumulative net| when total cumulative net ≠ 0 (deterministic
   concentration rule; a single dominant year alone may not carry the result);
5. **OOS half not materially inconsistent:** OOS median net > 0 AND OOS
   cumulative net > 0 (the OOS half is independently positive; a positive
   development half with a non-positive OOS half always fails this gate).

**No** additional/arbitrary Sharpe thresholds; no gate editing after results.

Final classifications (registered):

- All gates pass on a market → **ECONOMICALLY PROMISING — REQUIRES FORWARD
  VALIDATION** (does NOT authorize live/demo trading).
- The market's scientific verdict was SUPPORT but any economic gate fails →
  **BEHAVIORALLY VALIDATED / ECONOMICALLY NON-VIABLE**.
- Scientific status notes: BTCUSD is economically simulated and reported (it is
  in the registered universe and tick files exist) BUT it carries NO scientific
  verdict (HALTED, scientific stage) — its economic classification, if any, is
  recorded with an explicit
  **NO-SCIENTIFIC-VERDICT** caveat and does not authorize promotion without
  first resolving the scientific data-quality halt. EURUSD is NOT SIMULATED
  (NOT REGISTERED / DATA-LIMITED).

**Overall disposition (registered):** if all simulated markets with a scientific
verdict fail economically → ORD overall = BEHAVIORALLY VALIDATED / ECONOMICALLY
NON-VIABLE for the registered baseline. If ≥1 such market passes all gates →
overall = ECONOMICALLY PROMISING IN N INDEPENDENTLY REPORTED MARKET(S) —
REQUIRES FORWARD VALIDATION. Cross-market structure (instrument-specific /
asset-class / cross-market) is reported per §14.

---

## 14. Cross-Market Reporting

Markets reported strictly independently: XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD.
No requirement that every market passes; no removal of a failing market to
improve any aggregate.

- **instrument-specific** ← 1 market passes;
- **asset-class-specific** ← >1 related-mechanism market passes (e.g., the
  metals pair);
- **cross-market** ← ≥1 market in ≥2 distinct mechanisms (metals / equity-index
  CFD / crypto) passes;
- **economically non-viable** ← no market with a scientific verdict passes.

EURUSD: not simulated (DATA-LIMITED). BTCUSD: simulated and reported with its
no-scientific-verdict caveat (§13).

---

## 15. Year / Half Stability

- Report baseline economics by calendar year and by development/OOS halves for
  every market.
- **No tuning, no removal of bad years, no parameter changes.**
- If economics are positive only in one historical period, this is stated
  explicitly and the market does NOT pass gate 4/5 as applicable.

---

## 16. Reproducibility

Persist (isolated execution directory):

- economic execution identity (id + UTC timestamp);
- protocol SHA-256 (this document, computed at execution start);
- runner SHA-256 (the economic translation runner script);
- data hashes (M1 from the scientific manifest; tick file SHA-256 computed at
  execution);
- cost-model identity (Model A = `(s_entry+s_exit)/2`, observed MT5 median
  bid/ask; Model B descriptive; commission/slippage bands descriptive);
- trade ledger CSVs (one per market);
- market summaries JSON;
- development / OOS results;
- yearly results;
- execution metadata (environment, seed-free determinism, resource telemetry);
- final economic report.

This explicitly corrects the DISC-025 persistence gap: every intermediate
economic artifact is written to disk.

---

## 17. Machine-Safety Controls

The scientific ORD execution demonstrated that large M1 Pandas pipelines can
exhaust machine memory; the tick files are 6–13 GB each and MUST NOT be loaded
whole. Frozen controls:

1. Process markets sequentially (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD).
2. **Stream tick files** (line-buffered binary read, per-line filter) into
   bounded per-minute aggregates; never load a full tick file or a full
   minutes table into memory.
3. Event table and M1 OHLC read into memory per market only (the M1 record is
   the same size as the scientific run, which the executed run handled with the
   memory remediation of the V3 implementation audit).
4. Monitor process memory (psutil or equivalent) at a fixed interval; record
   peak RSS.
5. Isolated execution directory + EventStudyRecorder heartbeat/journal
   (crash-safe recorder pattern from the reconciliation implementation).
6. On resource failure: stop safely, record the incident in the journal, write
   all persisted state, and DO NOT modify any scientific/economic rule because
   of resource pressure. A resource failure is treated as an execution incident,
   not as a result.
7. Deterministic throughout: no randomness; reproducible per market run.

---

## 18. Economic Firewall

The following are explicitly NOT tested in this protocol (each is a separate
future hypothesis with its own pre-registration, not a baseline modification):

- different opening windows; different breakout thresholds;
- next-bar entry; pullback entry; limit entry;
- alternative stops (ATR, candle-close, volatility, buffers);
- targets; trailing exits; break-even; partial exits;
- time-stop alternatives; horizon grids;
- risk optimization; filters; confluence; ML / HMM / K-means;
- inverting / rescuing a non-viable baseline.

The registered baseline is allowed to succeed or fail on its own.

---

## 19. Exact Next Task

> After this protocol is frozen and its SHA-256 recorded: an **INDEPENDENT
> PRE-EXECUTION ECONOMIC PROTOCOL AUDIT** (read-only verification that this
> protocol, the event-source identities, the tick/M1 data gates, the bridge
> rules, the cost model, the gates, and the machine-safety controls are all
> precisely registrable and free of ambiguity), THEN ONE controlled economic
> execution of this baseline against the persisted events and observed quotes,
> THEN the economic adjudication, and — only if a market is classified
> ECONOMICALLY PROMISING — the forward/demo validation stage. No execution, no
> audit, and no economic judgment may be claimed from this document alone.

---

## 20. Integrity

- Strictly READ-ONLY with respect to all scientific objects: the ORD scientific
  protocol, definition lock, execution artifacts, event table, statistics,
  manifests, adjudication, and governance records are untouched.
- No M1 reprocessing into scientific objects; no bootstrap/null/event
  regeneration; no PnL computed here.
- The only new repository artifact is this frozen protocol.
- All economic rules, fills, costs, gates, and classifications are registered
  BEFORE computation; no value, parameter, or threshold in this document was
  informed by any economic backtest on ORD events.
- This protocol does not authorize trading, demo, or deployment of any kind.