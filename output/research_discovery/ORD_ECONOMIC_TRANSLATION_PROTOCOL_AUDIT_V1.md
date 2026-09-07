# QUANTFORGE — ORD ECONOMIC / STRATEGY TRANSLATION
# INDEPENDENT PRE-EXECUTION ECONOMIC AUDIT V1

## 1. Executive Verdict

**B — CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED.**

The frozen economic protocol (`ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1.md`) is
deterministic and executable in its scientific object, market scoping, cost
model, gates, and accounting structure, with **no new scientific or economic
hypothesis needed**. However, the two-researcher test (identical results with no
further decision) is NOT yet satisfied because the document contains internal
ambiguities that must be uniquely pinned by deterministic wording/mechanics
edits. Every item listed in §21 is resolvable without introducing a new
parameter, alternative translation, or hypothesis — hence CONDITIONAL PASS, not
FAIL, and not PASS as written.

## 2. Protocol Integrity

- Control set read: frozen economic protocol; ORD scientific protocols
  (V1.1.0 amended + definition lock); V3 implementation audit; Tradeable Edge
  Discovery Screening V3; DISC-025 economic translation + governance record;
  `event_study_recorder.py`; live M1 and MT5 tick data schemas; the scientific
  adjudication.
- The economic protocol is internally consistent with the scientific object:
  it translates ONLY the treatment (breakout) events from the persisted event
  table; controls are explicitly NOT traded; BTCUSD economics are simmered only
  with an explicit NO-SCIENTIFIC-VERDICT caveat; EURUSD is NOT simulated.
- No scientific artifact, protocol, runner, or execution infrastructure was
  modified by this audit. No PnL or trade statistics were computed; no
  historical economic outcome was inspected; no tick aggregation was built.

## 3. Entry Execution Bridge

Direction / quote side (LONG→ASK, SHORT→BID) is correct and consistent with the
buy-ask / sell-bid convention. Requirements verified:

- **Direction/quote side:** correct.
- **Breakout minute identified deterministically:** the entry minute is defined
  as `anchor_ts` (UTC, truncated to the minute) — but see §21-F1.
- **No future quote:** the fallback chain (±5 min → market median → exclusion)
  is bounded forward from the entry minute; no future-minute selection.
- **First qualifying quote clearly defined:** NO — see §21-F1 (conflict between
  "first observed ASK/BID" and "median-per-minute").
- **Minute aggregation semantics:** partially unambiguous — median-bid / median-ask
  per UTC minute from valid ticks (§10.2) is specified; but the selection between
  "first tick" and "minute-median" is not.
- **Median-per-minute fully specified:** aggregation rule and validity filter are
  specified; tick-side selection vs median rule is not (F1).
- **Fallback ±5 deterministic:** stated (nearest available minute, tie → earlier).
- **Market-median fallback deterministic:** stated.
- **Exclusion deterministic:** stated (`EXCLUDED_NO_QUOTE_COVERAGE`).

**CRITICAL QUESTION (flagged, not silently resolved):** the phrase "fill at the
FIRST available observed ASK/BID quote at or immediately after the breakout-close
timestamp" (protocol §4 items 1–2) conflicts with the separate "per-minute
median" rule (protocol §4 item 3) that the fill uses the minute's median. These
are two different entry-price layers. The exact sequence
`tick stream → per-minute median → entry price selection` is NOT pinned, and
while the protocol's own "no look-ahead" requirement and the DISC-025
entry-anchoring constraint force the resolution (fill can only occur at/after
the close is observable), the text currently permits two readings. See §21-F1.

## 4. Structural Stop

- Levels: LONG `OpeningRange_High`, SHORT `OpeningRange_Low` — exact geometry of
  the scientific invalidation, no ATR/buffer/optimization. PASS.
- **Level source + determinism:** OR High/Low are not persisted in the event
  table, so they are reconstructed from validated M1 using the FROZEN per-market
  opening windows (03:00–03:29 ET metals/crypto; 09:30–09:59 ET US tech index),
  with integrity cross-check against persisted event-table `range_width`
  (`EXCLUDED_RANGE_MISMATCH`). Deterministic and falsifiable. PASS.
- **Stop-first rule:** uniquely defined (stop evaluated before horizon on any
  co-occurring bar/minute; inherited from scientific protocol §7). PASS.
- **Close-based scientific invalidation vs economic stop — explicitly translated,
  not assumed:** the protocol registers the translation decision: the trigger is
  the first M1 bar AFTER entry whose CLOSE satisfies the invalidation (close-based,
  faithful to the scientific object), and the executable assumption is a resting
  fill AT the structural level at that stop bar's minute. Because the trigger
  bar's low already trades through the level (close beyond the level), a level
  fill is economically achievable; intra-bar touch-and-reject before a confirming
  close is NOT treated as a stop (an explicit, registered translation decision
  that avoids contradicting the scientific close-based object). This is now
  completely specified. PASS.
- One residual wording requirement: state explicitly that the fill occurs at the
  level in the presence of a gap-through on the trigger bar (fill assumed at the
  level, not at a worse gap price). Include in the §21 correction list (F4).

## 5. Horizon Exit

- **120-min anchor:** entry minute + 120 minutes (wall-clock), minute resolution.
- **Exit quote side:** LONG→BID, SHORT→ASK at the horizon minute (correct).
- **Stop/horizon coincidence:** stop-first (uniquely defined). PASS.
- **Horizon basis:** tick-executable (median bid/ask of the horizon minute), not
  M1-close; documented as such.
- **No tick at horizon timestamp:** deterministic bridge identical to entry
  (exact → ±5 → market median → exclusion). PASS.
- **Incomplete horizon:** excluded with report (`EXCLUDED_INCOMPLETE_HORIZON`
  implied by §6 + §9 exclusion tags). PASS.
- **Session boundary handling:** horizon is literal wall-clock and may cross the
  17:00 ET boundary into 24/5 data, matching the scientific protocol §9. Should
  be stated in one sentence (§21,F5).
- Bridge is identical across all markets. PASS.

## 6. Cost Model

- **Model A:** `RT(A) = (s_entry + s_exit) / 2`, one half-spread per side,
  inherited from the validated Liquidity-Sweep economic stage. PASS.
- **Spread unit:** bp of the per-minute mid (`s[m] = (ask−bid)/mid × 10^4`).
  Conversion methodology is specified. PASS.
- **Entry/exit spreads:** from the entry minute and exit minute lookups via the
  §4/§6 bridge. PASS.
- **Buy/sell direction consistency:** fills at ask/bid; gross is defined
  mid-to-mid; net = gross − RT(A). The two views (mid-to-mid gross − RT(A) vs
  executable ask/bid fill round trip) are algebraically the same — no double
  counting — but see §21-F3 (the `1e-6` cross-check tolerance is stricter than
  second-order spread effects allow and must be re-expressed as an explicit
  relative/algebraic identity).
- **Model B:** `RT(B) = s_entry + s_exit` (conservative); commission band
  0/2/5/10 bp RT and slippage band 0/2/5 bp RT — DESCRIPTIVE ONLY, never used to
  select/tune and never used in the viability gates (gates are Model-A-only,
  §13). Confirmed NOT an implicit optimization grid. PASS.
- No commission is invented; the unobserved-components statement is honest. PASS.

## 7. Tick Data

Verified against live files (schema inspection only — no economics):

- **Schema:** all four registered files are 6-column `date,time,bid,ask,last,vol`:
  XAUUSD `20210412,11:00:00,1740.548,1740.835,1740.548,0`; XAGUSD
  `20210713,00:00:03,26.248,26.278,26.248,0`; USATECHIDXUSD
  `20230901,00:00:00,15504.339,15507.403,15504.339,0`; BTCUSD
  `20210523,00:00:00,37431.7,37522.8,37431.7,0`. The EURUSD file is the only
  7-column/dotted-date variant — EURUSD is excluded, so no schema conflict. PASS.
- **Timestamp resolution:** seconds (`HH:MM:SS`); minute key = UTC
  `YYYYMMDD,HH:MM` — consistent with the validated sweep extraction. The protocol
  must state the tick timezone is UTC (aligned with M1 UTC) explicitly — §21-F2.
- **bid ≤ ask, positive prices:** registered data gate (§10.2) with invalid-tick
  counting. PASS.
- **Duplicate behavior:** keep-first / chronological-sort inherited from the
  scientific pipeline (§10.3); duplicates within a minute are handled by
  aggregation. Only the F2 timezone statement must be added.
- **Malformed-row handling:** registered (reject invalid; count and report). PASS.
- **Coverage + exact/fallback rules:** registered (§7 reporting + §4/§6 bridge). PASS.

## 8. Market Coverage

- **XAUUSD, XAGUSD, USATECHIDXUSD:** Eligible — simulated and economically
  evaluated exactly as the registered SUPPORT markets. PASS.
- **BTCUSD:** simulated ONLY with the explicit NO-SCIENTIFIC-VERDICT caveat; the
  protocol states that its economic classification cannot authorize promotion
  until the scientific data-quality halt is resolved. This does NOT create a new
  scientific market classification — the scientific HALT status is untouched.
  PASS.
- **EURUSD:** NOT simulated (NOT REGISTERED / DATA-LIMITED). PASS.
- No post-result market admission or removal exists in the protocol. PASS.

## 9. Position / Notional Convention

- Fixed 1 normalized unit per trade; returns in bp of entry price; unit-free
  cross-market comparison; no risk-percent optimization; no leverage assumption;
  no compounding; no Kelly; no adaptive sizing. PASS.
- Currency conversion: none — bp-based, broker contract values explicitly
  declared UNKNOWN where unknown. The economic output is comparable in a
  well-defined normalized unit. PASS.

## 10. Trade Accounting

- Ledger columns cover every required field: market, trading_day, direction,
  or_high, or_low, breakout_ts, breakout_close, executable_entry_quote,
  entry_spread_bp, structural_invalidation_level, exit_reason, exit_ts,
  executable_exit_quote, exit_spread_bp, gross_bp, cost_bp, net_bp, net_bp_B,
  MFE, MAE, holding duration, quote_lookup, data_quality_flag. PASS.
- No silent deletion: `EXCLUDED_*` rows are retained with reason and excluded
  from metrics only; losing trades are never deleted. PASS.
- **Required pinning (F6):** the MFE/MAE data source for each economic trade is
  not uniquely defined (scientific event-table MFE over the full horizon vs
  MFE/MAE over the actual holding window; MAE is not present in the persisted
  scientific event table and must be recomputed deterministically). Must be
  pinned before execution.

## 11. Development / OOS

- Split: first 50% of event days chronological = DEVELOPMENT, last 50% = OOS;
  deterministic; same convention as the validated sweep economic stage. No date
  midpoint; no performance-derived split. PASS.
- **CRITICAL QUESTION (resolved by the protocol itself):** the development half
  exists solely as a stability/reporting partition. Protocol §11 states
  "nothing is fitted, tuned, or selected on the development half. There are no
  fitted parameters in this one-baseline design." No contradiction; there is no
  tuning stage. PASS.

## 12. Primary Economic Metric

- Primary = **median net return per trade (bp), Model A** (observed spread only).
  Formula: per-trade net_bp = gross_bp(mid-to-mid) − RT(A); median across
  per-trade net_bp per market. PASS.
- Spread cost included exactly once (mid-to-mid gross excludes spread; RT(A)
  adds it once). Model B commission/slippage excluded from Model A and from all
  gates. Gross/net distinction explicit. Per-market medians computed
  independently. PASS.

## 13. Viability Gates

1. **median net return per trade > 0** (Model A) — deterministic. PASS.
2. **cumulative net result > 0** — not yet written as "chronological cumulative
   SUM of per-trade net_bp"; pin the SUM wording (F7). Functional intent clear.
3. **profit factor > 1.0 on net (Model A)** — §12 defines PF with the same
   wins/|losses| structure as the sweep precedent, but the group input
   (sums vs counts) and the no-loss / no-win boundary must be pinned (F8).
4. **≤60% calendar-year concentration** — formula
   `max_y |yearly net sum| ≤ 0.60 × |total cumulative net|` with `total ≠ 0`
   guard; since gate 2 forces cumulative > 0 for any passing market, the
   zero/negative denominator branch is moot — state this explicitly (F7).
   Deterministic as registered. PASS.
5. **OOS half independently positive** — BOTH median net > 0 AND cumulative
   net > 0 on the OOS half. Uniquely defined. PASS.

No Sharpe/arbitrary thresholds; no gate editing after results. PASS as frozen
with F7/F8 wording pins.

## 14. Cross-Market Reporting

- Markets adjudicated strictly independently; no requirement that all four pass;
  no removal of failing markets; no aggregate that hides failures. PASS.
- Classification grammar (instrument-specific / asset-class / cross-market /
  economically non-viable) is registered and uses the same structure as the
  DISC-025 precedent. PASS.

## 15. Stability / Year Analysis

- Every calendar year reported; no year removed; no parameter selected from
  year performance; dev/OOS reported separately; stability is not an
  optimization process (chapter §11 and operations are explicit). PASS.

## 16. DISC-025 Capture Lesson

- The economic origin IS the executable quote: fills at observed ask/bid of the
  entry/exit minute; gross is anchored at the executable entry reference;
  scientific `entry_close` is recorded for verification but is not the PnL
  origin. The opening-range edge is not used as a fill; MFE is never substituted
  for the primary; no pre-entry reference. The lesson is satisfied — PROVIDED
  the F1 entry rule is pinned so the executable fill cannot read pre-close ticks
  of the breakout minute (the entry-anchoring and no-look-ahead constraint).
  This is part of §21-F1.

## 17. Economic Firewall

- No alternative entry/stop/target; no trailing/break-even/partial exit; no
  ATR/trend/volatility filter; no confluence; no ML/HMM/K-means; no parameter
  optimization — all explicitly excluded in the protocol's §18 firewall, and no
  hidden test tool exists in the document. Only ONE baseline translation is
  registered. PASS.

## 18. Reproducibility

- The protocol mandates persistence of: execution identity; protocol SHA-256;
  runner SHA-256; M1 hashes (scientific manifest) + tick-file SHA-256; cost-model
  identity; trade-ledger CSVs; market summaries; dev/OOS results; yearly results;
  peak memory; execution metadata; final economic report. This corrects the
  DISC-025 persistence gap. PASS.
- Only additions: timezone statement (F2) and trade-accounting source pins (F6).
  No economic execution may be claimed complete without these persisted. PASS
  subject to F2/F6.

## 19. Machine Safety

- Sequential market processing; tick files (6–13 GB) streamed, never loaded
  whole; per-market M1/event reads only; psutil memory monitoring with peak RSS;
  isolated execution directory; EventStudyRecorder heartbeat + journal;
  resource failure = recorded incident, safe stop, preserved state, no rule
  modification under pressure; deterministic/no randomness. PASS.

## 20. Execution Integrity

- The economic run inherits the crash-safe recorder pattern (preflight → start →
  heartbeat/journal → complete/interrupt/invalidate) and the reconciliation
  machinery used for scientific runs. Fail-closed behavior (UNKNOWN → no
  mutation), no-resume discipline (a partial run requires reconciliation, not
  resume), and exactly-once are consistent with the recorder contract reviewed.
  The protocol should state in one line that the economic run reuses this
  pattern including the no-resume rule (F9).

## 21. Findings Table

| # | Severity | Location | Finding | Required deterministic pin (no new hypothesis) |
|---|---|---|---|---|
| F1 | MATERIAL | §4 (3.1 in mission terms) | "First observed ASK/BID" (items 1–2) conflicts with "median-per-minute" fill (item 3); the intended `tick stream → per-minute median → entry price selection` sequence is not pinned; the median of the ENTIRE breakout minute would include pre-close ticks, violating the protocol's own no-look-ahead and the DISC-025 entry-anchoring. | Rewrite §4 to a single rule: entry minute = the first minute at/after the breakout-CLOSE timestamp (breakout close = end of the breakout bar, i.e., next fillable minute) that has a valid per-minute median; fill price = that minute's median ask (LONG) / median bid (SHORT); never use ticks from the breakout bar's own minute before the close registers. |
| F2 | MODERATE | §7 / §10 | Tick timezone not stated. | Add: tick timestamps are UTC, second resolution, minute key = UTC `YYYYMMDD,HH:MM`, aligned with M1 UTC. |
| F3 | MODERATE | §9 | Cross-check `gross_bp − RT(A) = fill round trip within 1e-6` is stricter than second-order spread effects (denominator mismatch between entry/exit mids) allow. | Re-express as: net_bp computed on the actual ask/bid fill path; the "agreement" between views stated as an algebraic identity with an explicit relative tolerance (e.g., ≤ 1e-6 relative, or ≤ 1e-3 bp) rather than an absolute bp bound; or pin net_bp = the executable-fill round trip directly and set gross_bp = net_bp + RT(A) as the verifier. |
| F4 | MINOR | §5 | Gap-through on the trigger bar not explicitly addressed. | Add one line: even if the trigger bar opens through the level (gap), the fill is assumed at the structural level (registered conservative assumption). |
| F5 | MINOR | §6 | Session-boundary crossing not stated in one sentence. | Add: horizon is literal wall-clock from the entry minute and may cross the 17:00 ET boundary into subsequent 24/5 data; completeness via the +120-min M1 bar. |
| F6 | MODERATE | §9 | MFE/MAE sources not uniquely defined for economic trades; MAE is not persisted in the scientific event table. | Pin: MFE and MAE are computed deterministically over the ACTUAL holding window (entry fill to exit fill) from the validated M1 bars (high/low), in bp of the executable entry price; or explicitly reuse the scientific event-table MFE over the full horizon AND define MAE. One option must be chosen and frozen. |
| F7 | MINOR | §13 gates 2/4 | "Cumulative net" not written as an explicit chronological SUM; zero/negative total branch of gate 4 handled implicitly via gate-2 ordering. | Add: cumulative net (Model A) = chronological sum of per-trade net_bp; because only markets with cumulative net > 0 reach gate 4, the gate-4 denominator is always positive (state this). |
| F8 | MINOR | §12/§13 gate 3 | PF boundary cases (no losses → division by zero; no wins → PF=0) and group input (sums vs counts) not pinned. | Pin: PF_net = Σ(net_bp | net_bp>0) / |Σ(net_bp | net_bp<0)|; no positive net → PF = 0; no negative net → PF = ∞ (passes gate 3). |
| F9 | MINOR | §17/§19 | Reuse of the no-resume/fail-closed reconciliation pattern not stated in one line. | Add: the economic run reuses the EventStudyRecorder + reconciliation semantics (exactly-once; a partial/crashed run is reconciled, never resumed; UNKNOWN → no mutation). |

## 22. Final Governance Decision

**B — CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED.**

Rationale: The economic object, market scoping, execution architecture, cost
model, viability gates, and firewall are deterministic and consistent with the
frozen scientific protocol and the DISC-025 lessons. No genuine new scientific
or economic decision is required to make the protocol executable; the
outstanding items (F1–F9) are all deterministic wording/mechanics pins. F1 is
the only MATERIAL item: it must be frozen before the two-researcher test can
pass, because the entry fill price is the single most consequential value in the
translation. F6 materially affects the required ledger fields. All others are
moderate/minor clarifications.

**Condition for promotion to A:** apply the §21 pins to a V1.1 revision of the
economic protocol (preserving every scientific object, metric, and gate; no
parameter or alternative introduced), recompute the protocol SHA-256, and
re-confirm this audit outcome against the revised text. No execution may occur
on the current V1 text.

## 23. Exact Next Task

> Freeze the required deterministic corrections into **`ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1.1`
> (amend-only revision of V1; no scientific/economic object, metric, gate, or
> baseline change)** incorporating §21-F1..F9; record the new protocol SHA-256;
> then re-run this pre-execution audit against V1.1 (read-only). Only upon an
> upgraded A verdict is ONE controlled economic execution authorized, followed
> by the economic adjudication, and — only if a market is classified ECONOMICALLY
> PROMISING — the forward/demo validation stage.

## 24. Integrity

- Strictly READ-ONLY: no economic simulation, no PnL, no trade statistics, no
  tick aggregation, no historical economic outcome inspection, no M1 reprocessing
  beyond schema/first-line inspection, no parameter optimization, no modification
  of the economic protocol, scientific protocol, runner, recorder, or any
  execution artifact.
- Tick schema facts verified directly from file headers (4 registered markets).
  Recorder semantics verified from source interfaces (preflight/start/heartbeat/
  journal/complete/interrupt/invalidate; fail-closed reconciliation pattern
  established by the crash-reconciliation work).
- The only new repository artifact is this audit:
  `output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_AUDIT_V1.md`.
- No trading, demo, or deployment is authorized by anything in this audit.