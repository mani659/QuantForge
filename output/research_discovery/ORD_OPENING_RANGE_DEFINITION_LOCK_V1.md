# QUANTFORGE — OPENING-RANGE DIRECTIONAL BREAK (ORD)
# SCIENTIFIC DEFINITION LOCK V1

## 0. Identity and Mode

- **Candidate:** ORD — Opening-Range Directional Break, the primary candidate from `TRADEABLE_EDGE_DISCOVERY_SCREENING_V3.md`.
- **Task:** DEFINITION TASK ONLY — freeze one deterministic, cross-market scientific object. No backtest, no PnL, no historical inspection, no parameter optimization, no ML, no EA, no protocol.
- **Control set:** V3 screening; `docs/SESSION_HANDOFF.md`; `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-001…025); `research/knowledge/RESEARCH_TIMELINE.md`; closed-line adjudications (DISC-021/022/024/025); M1 data inventory; tick bid/ask infrastructure record.
- **Binding design constraint (DISC-025 lesson):** the primary response measures movement **from the actual executable entry**, never from a prior reference level that existed before entry.

---

## 1. Executive Verdict

**DEFINITION LOCKED — LEVEL 2 (READY FOR PRE-REGISTRATION).** One opening-range definition, one breakout definition, one entry, one invalidation, one primary response, one horizon, one control, one event-uniqueness rule, one cross-market mapping, and a mandatory economic-capture tie to the entry are all frozen from market mechanics (not from historical performance). The object is the simplest possible statement: **opening range → close-break → executable entry at the break close → structural invalidation (back through the broken edge) → post-entry directional movement over a fixed horizon**, identical across the validation universe.

## 2. Scientific Question

> Does a deterministic break of a pre-defined market opening range produce a statistically and economically meaningful **directional continuation after the breakout entry** across a multi-market validation universe?

The object is the behavior surrounding an opening-range close-break. It is NOT: institutional manipulation, smart money behavior, a guaranteed breakout, a trading strategy, or a profitability claim.

## 3. Discovery vs Validation

- **Discovery origin:** ORD identified in V3 screening as the primary V3 candidate (weighted score 89; economic-capture-first design).
- **Validation universe:** XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD. EURUSD remains **DATA-LIMITED / EXCLUDED** until its separate data-quality gate is resolved. No market is added because of historical performance; the universe is fixed before any outcome is known.

## 4. Market Universe (frozen)

| Market | Class | Opening anchor (America/New_York) | Rationale |
|---|---|---|---|
| XAUUSD | Precious metal | London open — 03:00:00 ET | Primary pricing session for gold/silver; first major liquidity event of the 24/5 day |
| XAGUSD | Precious metal | London open — 03:00:00 ET | Same class mechanism |
| USATECHIDXUSD | US equity index CFD | US cash open — 09:30:00 ET | Instrument anchored to the US cash session; the structural "opening" of its primary market |
| BTCUSD | Crypto | London reference — 03:00:00 ET | 24/7 market; the opening-range concept maps to the chosen reference clock (the canonical 03:00:00 ET reference), per the one-object rule |

The anchors are **structural instrument mechanics**, fixed a priori; no per-market optimization. This is one scientific object with one canonical timezone (`America/New_York`, DST via `zoneinfo`), not separately tuned opening times.

## 5. Timezone / Market Clock

- Canonical timezone: **America/New_York** (all markets; DST handled deterministically via `zoneinfo`).
- M1 timestamps are UTC; conversion UTC → ET is deterministic.
- Crypto (BTCUSD) uses the same reference clock with the 03:00:00 ET mapping (no session concept; clock-window mapping is structural).
- One object; the only cross-market differences are the structural opening anchors above.

## 6. Opening Range (frozen)

- **Opening window:** the first **30 minutes** of the opening anchor — London window **03:00:00–03:29:59 ET inclusive** (XAUUSD, XAGUSD, BTCUSD); US cash window **09:30:00–09:59:59 ET inclusive** (USATECHIDXUSD). Exactly **30 M1 timestamps** per window.
- **Mechanical justification (independent of any historical outcome):** the opening range is the classic opening-range-breakout liquidity-formation window — the period during which the market establishes the day's reference levels from initial order-flow imbalance after the quiet/overnight phase. The 30-minute window is the standard structural convention for this object (opening-range breakout); it is a market-structure choice, not a performance-derived parameter.
- **Range:** `OpeningRange_High = max(high)` and `OpeningRange_Low = min(low)` over the 30 window bars; range width = High − Low (descriptive/eligibility only).
- **OHLC fields:** high/low for the range; close for breakout, invalidation, and response.
- **Boundaries:** inclusive on both ends of the window; strict inequalities for the breakout (below).
- **Eligibility (day-level, deterministic):** a day is eligible only if all 30 window M1 timestamps exist with valid OHLC (> 0). A zero-width range (`High == Low`) makes the day ineligible (no clean breakout can be defined). Missing bars, holiday days, and days with a truncated opening window are ineligible (not events).
- **Fixity:** the range is **fixed at the window close** and never includes evaluation-phase bars (no look-ahead).

## 7. Breakout Event (frozen)

- **Long (upside) breakout:** the **first M1 bar after the opening window** whose **close > OpeningRange_High** (strict; close strictly beyond the upper edge).
- **Short (downside) breakout:** the **first M1 bar after the opening window** whose **close < OpeningRange_Low** (strict).
- **Close-based, not penetration-based:** the close is the first price at which the break is verifiable and executable; high/low penetration alone (wick) does not qualify.
- **Touching** the boundary (`close == edge`) does NOT qualify (strict inequality).
- **Evaluation window:** the breakout is evaluated over the bars from window end through **17:00:00 ET inclusive** of the same NY calendar day (mirroring the validated sweep session-window design; after 17:00 the day's active-session theme is over).
- **Multiple attempts:** only the **first** qualifying close per direction per day counts; later attempts (including a failed break that closes back inside and re-attempts) do not create new events. Both directions are evaluated independently.
- **Simultaneous upper/lower:** impossible on one bar (High > Low by construction); both directions may occur on the same day (see §13).

## 8. Entry Timing (frozen)

- **Entry:** at the **close of the breakout candle** — the candle whose close first exceeds the broken edge. The event IS the entry; there is no confirmation lag beyond the qualifying bar itself.
- **Rationale (execution realism + mechanism):** the close of the qualifying bar is the first price at which the breakout condition is known; a market order at that close is the minimal execution-realistic translation. No next-bar-open (adds lag), no tick-level entry (unnecessary for the object).
- **This is the economic-capture anchor:** every response is measured from this price.

## 9. Invalidation (frozen)

- **Structural invalidation:** a subsequent M1 close **at or beyond the broken edge on the losing side** — long: any later close **≤ OpeningRange_High**; short: any later close **≥ OpeningRange_Low**. Equivalently: price has returned to the opening range.
- **Why this represents failure of the behavior:** the hypothesis is directional continuation beyond the opening range; a close back at the broken edge means the break is not holding — the registered behavior is absent on that day.
- **No optimized distance; the invalidation is exactly the geometry** (the broken range edge). The invalidation is evaluated bar-by-bar after entry; if both invalidation and the horizon exit occur on the same bar, invalidation is evaluated first (conservative).

## 10. Primary Behavioral Response (frozen)

- **Primary response (per event):** the **directional return from the entry close to the horizon close, in basis points of the entry price** —
  - long: `(Close[entry + H] − Close[entry]) / Close[entry] × 10⁴`
  - short: `(Close[entry] − Close[entry + H]) / Close[entry] × 10⁴`
- **Why bp from the entry:** directly executable and economically interpretable; the DISC-025 mandatory rule — the response is anchored at the actual entry price, never at the range edge or any pre-entry reference.
- **Secondary (descriptive only, non-rescuing):** MFE from entry over [entry, entry+H]; range-width-normalized continuation (in opening-range units). These cannot alter the primary verdict.

## 11. Horizon (frozen)

- **H = 120 minutes**, literal wall-clock from the entry close.
- **Mechanical rationale:** the post-break continuation window during which opening-session order-flow imbalance plays out is on the 1–2 hour scale; 120 minutes is the project's registered intraday behavioral-horizon convention (validated sweep protocol §10). Fixed; no horizon grid, no 15/30/60/120 search.
- **Semantics:** the 120-minute window is a literal wall-clock interval beginning at the entry close and may cross the 17:00:00 ET boundary into subsequent 24/5 data. No truncation at session boundaries; no imputation; no partial windows. An event is eligible only if a complete 120-minute window is available (events near data end are excluded before inference). Identical for treatment and control.

## 12. Control Group (frozen)

- **Control event (per direction per day):** a **penetration without a qualifying close-break** — at least one M1 bar in the evaluation window with `high > OpeningRange_High` (upper attempt) or `low < OpeningRange_Low` (lower attempt), but **no qualifying close beyond the edge in that direction through 17:00:00 ET**.
- **Control anchor:** the close of the **first penetration bar** in that direction.
- **Control response:** the same directional 120-minute horizon return from the control anchor close, signed by the attempt direction (upper attempt → hypothetical long). Same completeness rule as treatment.
- **Justification (independent, a priori):** the control conditions on "the level was touched" (comparable market condition) minus the registered qualifying event (close-break); it answers "what happens after the opening range is tested but the close-break never registers" — the direct counterfactual to the treatment. Mechanically defined; **no post-result matching, no control tuning**.
- **Partition (deterministic, per direction per day):** qualifying close-break exists → treatment (first one); no qualifying close-break but ≥1 penetration → control (first penetration); neither → no event. A day can carry up to two events per direction-type combination (see §13).

## 13. Event Uniqueness (frozen)

- **First qualifying close-break per direction per day** (treatment); **first penetration per direction per day** when no close-break occurs in that direction (control).
- A day may contain: upper treatment + lower treatment; upper treatment + lower control; upper control + lower treatment; upper control + lower control; or a single-sided event. All events remain attached to their calendar day.
- **No second event in the same direction on the same day** (a failed break does not reset the first-per-direction rule).
- **Dependence design:** the hierarchy is market → calendar day → events (≤ 2) → day-cluster bootstrap (dependence-preserving), identical in structure to the validated sweep design. Events on the same day move together in resampling.

## 14. Cross-Market Definition (frozen)

- ONE object across XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD; the only differences are the structural opening anchors of §4 (instrument-class mechanics: London open for metals/crypto reference, US cash open for the index CFD). No market-specific breakout, response, horizon, or control definitions.
- The same event structure, response, invalidation, control, and uniqueness rules apply verbatim to every market; the experiment will discover where the behavior holds rather than assume it.

## 15. Economic Capture Requirement (mandatory — PASS)

- **Is the primary response directly tied to the actual entry?** YES — the response is the bp return from the entry close (the breakout candle close) to the horizon close. There is no measurement from a prior reference level; no confirmation-lag disconnect; no "MFE from the opening edge" as the primary.
- **Anti-sweep check:** the sweep failed because its statistic (excursion from the Asian level) was not capturable at the confirmation entry. ORD's primary statistic is the post-entry move by construction. Any future protocol must preserve this property.

## 16. Falsification (frozen, definition-level)

- **SUPPORTED:** positive registered effect (treatment response exceeds control under the future inference rule).
- **CONTRADICTED:** reliable opposite-direction effect (e.g., treatment continuation reliably smaller than control, or negative).
- **INCONCLUSIVE:** neither.
- Numerical significance machinery (bootstrap, Holm, p-values) is deferred to pre-registration; the definition fixes the objects those rules will consume.

## 17. Independence From Closed Lines (frozen)

- **vs Mean Reversion (DISC-021):** ORD is a directional continuation object — the response is signed by the break direction; a null/negative result means "no continuation," not reversion. No reversion response, no displacement/recoil/persistence machinery.
- **vs TSMOM (DISC-022):** TSMOM was a monthly-frequency, rolling-window momentum signal tested against a drift benchmark; ORD is an intraday, event-driven, session-structure object with no lookback window, no rolling signal, no drift benchmark, and a single fixed-horizon post-entry move.
- **vs Session Range Expansion (DISC-024):** SRE tested whether pre-session compression precedes larger cash-session **range size** (a volatility-state object), and was contradicted; ORD tests whether an opening-range **close-break** precedes **directional continuation** (a direction object). Different input (break vs compression percentile), different output (direction vs range size), different object class (event vs state).
- **vs Liquidity Sweep / Reversal (DISC-025):** the sweep used a breach of the **prior Asian extreme**, a rejection, and a confirmation lag, measuring excursion from the Asian level (reversal object); ORD uses the **current session's own opening range**, a close-break, **no rejection and no confirmation lag**, measuring continuation from the entry (trend object). Different reference (current-session range vs prior-session extreme), different logic (continuation vs reversal), different response anchor (entry close vs Asian level).
- **Explicit non-similarities:** ORD is NOT another volatility-range experiment (it is directional), NOT another momentum/TSMOM experiment (no rolling momentum), NOT a modified sweep (no prior-extreme reference, no rejection, no confirmation lag, response from entry). The distinction is in the scientific object, not the naming.

## 18. ML Position (frozen)

- ML is not part of the definition. Future ML may serve as a regime classifier **only if independently justified after the deterministic ORD object is established** — never to discover the pattern, never to rescue a null/contradicted result.

## 19. Definition-Level Readiness

**LEVEL 2 — READY FOR PRE-REGISTRATION.** All required single definitions are frozen: opening range (30-min, session-anchored), breakout (first close beyond the edge), entry (breakout-candle close), invalidation (close back through the broken edge), primary response (bp directional return from entry to horizon), horizon (120-min wall-clock), control (penetration-without-close-break), event uniqueness (first per direction per day, ≤2/day, day-cluster coupling), cross-market mapping (structural anchors only), and economic capture (response tied to entry). No definitional piece requires a new scientific decision.

## 20. Exact Next Task

> **Outcome-blind PRE-REGISTRATION of the ORD definition** (protocol): universe (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD; EURUSD excluded pending data gate), day-eligibility and coverage gates, event construction, primary statistic (e.g., ΔM = median treatment response − median control response per market), dependence-preserving inference (day-cluster stationary bootstrap), B/L/seed, Holm family, null construction, secondary analyses, and the full reproducibility record — followed by independent audit, one controlled multi-market execution, scientific adjudication, then economic translation with observed MT5 costs.

## 21. Prohibited Follow-Up

- Any backtest, PnL, or historical inspection before pre-registration.
- Any change to the opening window, anchor, horizon, response, invalidation, or control from historical results (including any horizon/range grid).
- Selecting markets by performance; adding markets; using EURUSD before its data gate resolves.
- Framing ORD as any closed-line repair; using H01 as a state variable; reviving the combination screen; using ML to discover the pattern; building an EA; touching BOE/Assembly/Deployment; modifying any closed protocol.

## 22. Integrity

Strictly read-only and outcome-blind. The only new repository artifact is this definition lock. No code, no experiment, no PnL, no optimization, no governance-file modification, no market selected for historical performance. Every frozen definition carries a market-mechanics rationale documented independently of any historical outcome; the economic-capture requirement of DISC-025 is applied as a mandatory design constraint.
