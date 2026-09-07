# QUANTFORGE — MECH-N01 OUTCOME-BLIND BASE FORMULATION V1

**Date:** 2026-09-07
**Status:** BF1–BF13 FORMULATION COMPLETE — PROVISIONALLY SELECTED ARCHITECTURE READY FOR OWNER ADJUDICATION
**Milestone:** Outcome-Blind Base Formulation Cycle for MECH-N01 (Structural Level Validation Flow)
**Parent doctrine:** V38A (BV1–BV13), BS1–BS13 (selection clauses), BF1–BF13 (formulation clauses)
**Selection artifact:** `output/research_discovery/QUANTFORGE_MECH_N01_OWNER_SELECTION_FREEZE_V1.md` (SHA `1bab8a0c`)

---

## 1. MISSION

Conduct the formal V38A Outcome-Blind Base Formulation Cycle BF1–BF13 for the owner-selected mechanism MECH-N01 (Structural Level Validation Flow). Transform the frozen mechanism hypothesis into a complete, deterministic, prospective Base decision architecture suitable for later registration and structural validation.

This task is formulation only. It does NOT register, validate, economically test, backtest, optimize, or promote the Base.

---

## 2. AUTHORITATIVE SOURCES

| Source | Artifact | Role |
|--------|----------|------|
| V38 Doctrine | `QUANTFORGE_V38_DOCTRINE_RATIFICATION_V1.md` | Hybrid Base + Conditional; D1–D25 |
| V38A Validation Pathway | `QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_RATIFICATION_V1.md` | BV1–BV13; six-stage lifecycle |
| Base Hypothesis Selection | `QUANTFORGE_BASE_HYPOTHESIS_SELECTION_VALIDATION_RATIFICATION_V1.md` | BS1–BS13; selection clauses |
| Outcome-Blind Formulation | `QUANTFORGE_OUTCOME_BLIND_BASE_DECISION_PROCESS_FORMULATION_RATIFICATION_V1.md` | BF1–BF13; formulation clauses |
| V38A New Base Mechanism Discovery | `QUANTFORGE_V38A_NEW_BASE_MECHANISM_DISCOVERY_V1.md` | Discovery artifact (MECH-N01/N02/N03) |
| MECH-N01 Owner Selection Freeze | `QUANTFORGE_MECH_N01_OWNER_SELECTION_FREEZE_V1.md` | Owner selection of MECH-N01 |
| SESSION_HANDOFF | `docs/SESSION_HANDOFF.md` | Current governed state |

---

## 3. FROZEN MECHANISM

The mechanism preserved throughout this formulation:

**Structural Level Validation Flow**

Core hypothesis:

> A structural price break becomes economically informative when subsequent price behavior demonstrates that the break is accepted/validated rather than immediately rejected; this validation reflects a change in participant behavior and may produce directional flow.

This is still a **MECHANISM HYPOTHESIS**. It is not a proven edge. Language has not been strengthened beyond the evidence.

---

## 4. BF1 — MECHANISM PRESERVATION

### 4.1 Structural phenomenon detected

The Base detects when price breaks above the highest high (or below the lowest low) of a defined lookback window of completed M1 bars. The structural level represents a price point where market participants have previously found resistance (highest high) or support (lowest low).

### 4.2 Participant behavior hypothesized

When the breakout occurs:
- Stop-hunters / short-term contrarians who sold the breakout are underwater and may be forced to cover
- Momentum followers who bought the breakout are profitable but uncertain
- Market makers must adjust inventory and quotes to reflect the changed structural state

When the breakout is validated (holds for K bars):
- Stop-hunters are forced to cover, creating directional pressure
- New entrants enter in the validated direction, reinforcing the move
- Market makers complete their hedging adjustments

### 4.3 Observable evidence of validation

Validation occurs when price closes remain on the breakout side of the structural level for K completed M1 bars after the breakout bar. The validation is deterministic: compare each bar's close to the breakout level.

### 4.4 What constitutes failure/rejection

The breakout is rejected if price closes return through the structural level before K completed bars. At that point, the breakout has failed and the mechanism's hypothesized participant-behavior transition does not occur.

### 4.5 Why available prospectively

The structural level is computed from completed M1 bars (past data only). The breakout is detected on a completed bar. The K-bar hold period is observed on completed bars. No future information is required at any decision point.

---

## 5. BF2 — OBSERVABLE DEFINITION

The minimum deterministic observables required:

### 5.1 Structural level reference

- **Bullish structural level:** The highest high among the most recent N completed M1 bars (exclusive of the current bar)
- **Bearish structural level:** The lowest low among the most recent N completed M1 bars (exclusive of the current bar)

### 5.2 Breakout condition

- **Bullish breakout:** The current bar's close exceeds the bullish structural level
- **Bearish breakout:** The current bar's close is below the bearish structural level

### 5.3 Post-break price location

- **Above breakout:** Current bar's close > bullish structural level
- **Below breakout:** Current bar's close < bearish structural level

### 5.4 Persistence / acceptance

- Each completed bar after the breakout bar is evaluated: does the close remain on the breakout side of the structural level?
- **Acceptance:** Close remains on breakout side
- **Rejection:** Close returns through the structural level

### 5.5 Bar sequencing

- The breakout bar is designated bar E
- Subsequent bars are E+1, E+2, ..., E+K
- Validation is confirmed at the close of bar E+K

### 5.6 Close/open relationships

Not used in this formulation. Only close-to-level relationships are evaluated.

All observables are objectively measurable, available at decision time, independent of future information, and reproducible across implementations.

---

## 6. BF3 — STRUCTURAL LEVEL DEFINITION

### 6.1 Where does the level come from?

The structural level is derived from the price history of the instrument itself. For bullish levels, it is the highest high in the N-bar lookback. For bearish levels, it is the lowest low.

### 6.2 How is it constructed?

At each completed M1 bar, compute:
- `bullish_level = highest(high[i]) for i in [1..N]` (most recent N completed bars, excluding current)
- `bearish_level = lowest(low[i]) for i in [1..N]` (most recent N completed bars, excluding current)

### 6.3 What historical information is allowed?

Only the high and low of each completed M1 bar within the N-bar lookback window. No volume, no indicators, no external data.

### 6.4 When does the level become fixed?

The level is recomputed at the close of every completed M1 bar. It is a rolling value. However, once a breakout is detected (bar E), the breakout level is frozen as the structural level that was active at bar E's close. The frozen level is used for all subsequent validation evaluation (bars E+1 through E+K).

### 6.5 Can the level move after formation?

The rolling structural level continues to update as new bars complete. However, once a breakout event is triggered, the breakout reference level is frozen. The rolling level may change, but the validation evaluation uses the frozen breakout reference level.

### 6.6 How are overlapping levels handled?

If multiple structural levels exist (e.g., the N-bar high and the N-bar high from a different lookback), each is treated independently. A breakout of one level does not disqualify a breakout of another. See Section 11 (BF7) for opportunity-population rules on overlapping signals.

### 6.7 When is a level no longer relevant?

A structural level is no longer relevant when:
- A new breakout is detected from a more recent structural level (the new breakout supersedes)
- The breakout fails (price closes through the level before K bars)

---

## 7. BF4 — STRUCTURAL BREAK DEFINITION

### 7.1 Required price relationship

- **Bullish break:** Bar E close > bullish structural level (highest high of prior N completed bars)
- **Bearish break:** Bar E close < bearish structural level (lowest low of prior N completed bars)

### 7.2 Reference level

The structural level defined in BF3.

### 7.3 Whether wick penetration counts

No. Only the close is evaluated. Intra-bar wicks that exceed the level but where the close does not are NOT breakouts. The mechanism requires acceptance at the close, not merely intra-bar exploration.

### 7.4 Whether close confirmation is required

Yes. The breakout is confirmed only when the bar closes beyond the structural level. This is the close-confirmation requirement.

### 7.5 Exact decision timestamp

The breakout decision is made at the completion (close) of bar E. At that moment, the breakout is either confirmed (close beyond level) or not.

### 7.6 Whether intra-bar information may be used

No. Only completed-bar information is used. The breakout is evaluated on the bar's close.

### 7.7 Whether the event is evaluated on completed bars only

Yes. All evaluation occurs on completed M1 bars. No intra-bar evaluation is performed.

---

## 8. BF5 — VALIDATION / ACCEPTANCE DEFINITION

This is the central formulation problem.

### 8.1 What subsequent behavior constitutes acceptance?

After the breakout bar (E), each subsequent completed bar (E+1, E+2, ..., E+K) is evaluated:
- **Acceptance:** The bar's close remains on the breakout side of the frozen structural level
- If all K bars show acceptance, the breakout is validated at the close of bar E+K

### 8.2 What subsequent behavior constitutes rejection?

- **Rejection:** Any bar among E+1 through E+K has a close that returns through the frozen structural level to the opposite side
- If rejection occurs at any point during the K-bar window, the breakout has failed
- The failed breakout produces NO trade

### 8.3 How long is the validation observation conceptually?

K completed M1 bars after the breakout bar. The validation window spans bars E+1 through E+K.

### 8.4 What price relationships matter?

Only the close-to-level relationship. Whether each bar's close is above (for bullish) or below (for bearish) the frozen structural level.

### 8.5 When does validation become known?

At the completion (close) of bar E+K, if all K bars maintained acceptance. This is the validation timestamp.

### 8.6 Can validation occur intra-bar or only on completed bars?

Only on completed bars. Each bar in the validation window must complete before its acceptance/rejection is determined.

### 8.7 What happens if acceptance and rejection evidence conflict?

Within the K-bar window, a single rejection bar terminates the breakout. There is no partial validation. The K-bar hold is an all-or-nothing condition: all K bars must show acceptance for validation to occur.

### 8.8 Parameter K

K is a formulation parameter requiring later governance selection. K is NOT selected by historical testing. K represents the minimum hold period that the owner considers sufficient for the participant-behavior transition to occur. K is designated as **GOVERNANCE-SELECTABLE** (see Section 18).

---

## 9. BF6 — DECISION DIRECTION

### 9.1 Directional participation

- **Bullish validation** (price holds above breakout for K bars) → **LONG**
- **Bearish validation** (price holds below breakout for K bars) → **SHORT**

### 9.2 Justification by mechanism

The mechanism hypothesizes that validation creates participant-behavior changes (covering, new entries, market-maker adjustment) that produce directional flow. The flow is in the validated direction. Therefore, the trade follows the validated direction.

### 9.3 Whether the Base ever fades a validated break

No. The mechanism does not hypothesize that validated breaks reverse. The Base follows validated breaks only.

### 9.4 Whether rejected breaks produce no trade or an opposite trade

No trade. A rejected breakout (failure before K bars) means the participant-behavior transition did not occur. There is no mechanism rationale for an opposite trade.

### 9.5 Whether ambiguity produces no trade

If the validation state is ambiguous (e.g., a bar close is exactly at the structural level), the bar is treated as rejection. The close must be strictly beyond the level to count as acceptance. Exact equality = rejection = no trade.

---

## 10. BF7 — OPPORTUNITY POPULATION

### 10.1 Instrument scope

Single instrument. Default: USATECHIDXUSD (USTECm on Exness). The mechanism is single-market by design.

### 10.2 Timeframe

M1 (one-minute bars). The mechanism operates at M1 resolution.

### 10.3 Session scope

The mechanism operates whenever the instrument is trading and structural levels can be defined. No session filter is applied in the minimal formulation. Structural levels are computed continuously from the rolling N-bar lookback. Breakouts can occur at any time.

Note: A session filter (e.g., US regular hours 09:30–16:00 ET) is a potential governance-selectable refinement but is NOT included in the minimal formulation to avoid outcome-driven scope selection. See Section 19 (Alternative Formulations) for a session-filtered variant.

### 10.4 Structural-level eligibility

Any rolling N-bar high or low is eligible to produce a breakout. No minimum distance, no minimum age, no minimum significance threshold beyond the N-bar lookback.

### 10.5 Event uniqueness

Each breakout event is unique to:
- The instrument
- The breakout bar (E)
- The frozen structural level active at bar E

### 10.6 Overlapping events

If two structural levels produce breakouts on the same bar, both are independent events. Each is tracked separately through its own K-bar validation window.

### 10.7 Simultaneous levels

Not applicable. The rolling N-bar high/low produces one bullish level and one bearish level at each bar. Only one can be broken at a time (price cannot be above the highest high and below the lowest low simultaneously).

### 10.8 Repeated breaks

If price breaks the same structural level multiple times (e.g., breaks above, returns below, breaks above again), each break is a separate event with its own validation window. The level remains the same until a new structural level is defined.

### 10.9 Cooldown logic

No cooldown is applied in the minimal formulation. Each break is an independent event.

### 10.10 Whether multiple trades may arise from the same structural level

Yes. If the same structural level is broken, validated, and then broken again after price returns, the second break is a new independent event.

---

## 11. BF8 — ENTRY / PARTICIPATION

### 11.1 When the decision becomes actionable

At the completion (close) of bar E+K, when validation is confirmed.

### 11.2 Earliest possible entry

At the open of bar E+K+1 (the bar immediately following validation completion).

### 11.3 Exact bar/timestamp semantics

- Validation confirmed at close of bar E+K
- Entry at open of bar E+K+1
- If bar E+K+1's open is available, entry occurs at that price
- If bar E+K+1's open is not available (data gap, market closure), entry is delayed to the next available bar's open

### 11.4 What happens if the entry cannot be executed

If the entry cannot be executed at the open of bar E+K+1 (e.g., market is closed, data is missing), the process attempts entry at the next available bar's open. If more than a defined maximum number of bars elapse without execution, the opportunity is abandoned.

### 11.5 Whether the process is allowed to miss the trade

Yes. The process is allowed to miss trades due to data gaps, market closure, or execution failure. Missing a trade is preferred over entering at an undetermined price.

---

## 12. BF9 — INVALIDATION / RISK

### 12.1 Mechanism invalidation

The mechanism is invalidated (the breakout has failed) if price closes return through the structural level BEFORE validation is complete (before bar E+K). At that point, the hypothesized participant-behavior transition did not occur.

### 12.2 Distinguishing mechanism invalidation from ordinary adverse price movement

- **Mechanism invalidation:** Price closes through the structural level during the K-bar validation window. This means the breakout has failed and no trade should be entered.
- **Ordinary adverse price movement:** Price moves adversely AFTER entry (after validation is complete). This is normal trade risk, not mechanism invalidation.

### 12.3 Structural invalidation (post-entry)

After entry, the trade remains active until an exit condition is met (see BF10). There is no structural invalidation mechanism post-entry in the minimal formulation. The trade runs until exit.

### 12.4 Timing invalidation

Not used in the minimal formulation. No time-based stop.

### 12.5 Level failure (post-entry)

Not used in the minimal formulation. The structural level is used for breakout detection and validation only, not for post-entry risk management.

### 12.6 Maximum-risk boundary

Not specified in the minimal formulation. No stop-loss is defined. The trade exits at session close (BF10). The maximum risk is the full adverse move from entry to session close.

Note: A stop-loss is a potential governance-selectable refinement but is NOT included in the minimal formulation. See Section 19 (Alternative Formulations).

---

## 13. BF10 — EXIT

### 13.1 Thesis exit

The thesis is that validated breakouts produce directional continuation. The thesis does not specify a profit target or a continuation threshold. The trade is held until a structural or time-based exit occurs.

### 13.2 Risk exit

Not defined in the minimal formulation. No stop-loss. See BF9.

### 13.3 Operational / session exit

The trade is exited at the session close. The session is defined as the set of bars during which the instrument is actively trading.

Note: The session close exit is mechanism-consistent because the participant-behavior transition hypothesized by the mechanism is an intraday phenomenon. The directional flow from validation is expected to manifest within the session.

### 13.4 Exit semantics

- Exit occurs at the close of the last bar before session end
- If session end is not precisely defined, exit occurs at a governance-selected time
- The exit is deterministic: at the designated time, the position is closed at the next available price

---

## 14. BF11 — EXECUTION MODEL

### 14.1 Market / asset type

CFD on US equity index (USATECHIDXUSD / USTECm on Exness).

### 14.2 Price source

M1 OHLCV bars from the MT5 terminal.

### 14.3 Bar completion semantics

Each M1 bar is considered complete at its close timestamp. All evaluation occurs on completed bars.

### 14.4 Executable timing

- Entry: open of bar E+K+1
- Exit: close of last bar before session end

### 14.5 Spread / cost treatment conceptually

Spread and transaction costs are acknowledged but not modeled in the formulation. The eventual V38A validation will use a frozen cost model. The formulation assumes a single round-trip cost per trade (entry spread + exit spread + commissions).

### 14.6 Handling of missing observations

If a bar is missing from the data sequence:
- During validation window: treat the missing bar as rejection (conservative)
- At entry: skip to next available bar's open
- At exit: skip to next available bar's close

### 14.7 Duplicate observations

If duplicate bars are detected (same timestamp, same OHLCV), duplicates are removed. The first occurrence is used.

### 14.8 Market closure

If the market closes during the validation window:
- The validation window is paused
- Validation resumes when the market reopens
- If the market closes during an active trade, the position is exited at the last available price before closure

### 14.9 Execution failure

If an entry or exit cannot be executed:
- The opportunity is abandoned (for entry)
- The position is marked at the last available price (for exit)

---

## 15. BF12 — OUTCOME DEFINITION

### 15.1 Event / trade outcome

Each trade outcome is defined as:
- `outcome = exit_price - entry_price` (for LONG)
- `outcome = entry_price - exit_price` (for SHORT)

### 15.2 Measurement horizon

From entry (open of bar E+K+1) to exit (close of last bar before session end).

### 15.3 Gross outcome

The raw price difference without cost adjustment.

### 15.4 Cost-adjusted outcome

`cost_adjusted_outcome = gross_outcome - round_trip_cost`

Where `round_trip_cost` is the frozen cost model applied during V38A validation.

### 15.5 Opportunity accounting

Each validated breakout produces at most one trade. Rejected breakouts produce zero trades. The opportunity population is the set of all breakouts (validated + rejected). The trade population is the subset of validated breakouts.

### 15.6 Missing-data treatment

If data is missing during the measurement horizon:
- If missing at entry: opportunity is not counted as a trade
- If missing during the trade: outcome is interpolated from available bars
- If missing at exit: outcome uses the last available price

### 15.7 Event independence

Each trade is treated as independent. Overlapping validation windows (from different structural levels) may produce concurrent trades, which are treated as independent events.

---

## 16. BF13 — COMPLETENESS / DETERMINISM AUDIT

### 16.1 Could two competent researchers implement the same Base from this document?

**Yes**, with the following noted ambiguities (Section 21):

### 16.2 Audit checklist

| Item | Status | Notes |
|------|--------|-------|
| Ambiguity | MOSTLY RESOLVED | Session definition has one ambiguity (Section 21) |
| Hidden hindsight | NONE DETECTED | All decisions use completed-bar information only |
| Hidden parameters | NONE | N and K are explicitly designated as governance-selectable |
| Undefined tie cases | RESOLVED | Close exactly at level = rejection |
| Overlapping levels | RESOLVED | Each level tracked independently |
| Repeated signals | RESOLVED | Each break is independent |
| Session boundaries | AMBIGUOUS | See Section 21 |
| Exact timing | RESOLVED | Entry at open of E+K+1, exit at session close |
| Missing data | RESOLVED | Conservative treatment defined |
| Execution assumptions | RESOLVED | Entry/exit timing specified |
| State transitions | RESOLVED | Break → validation window → validated → entry → exit |
| Invalidation | RESOLVED | Rejection during K-bar window |
| Exit semantics | RESOLVED | Session close |

---

## 17. PARAMETER GOVERNANCE

### 17.1 Parameters classified

| Parameter | Classification | Rationale |
|-----------|---------------|-----------|
| N (lookback period for structural level) | GOVERNANCE-SELECTABLE | The mechanism requires "a lookback period" but the exact value is a design choice. N=60 is the default recommendation (1 hour of M1 data) but must be explicitly frozen by the owner before registration. |
| K (validation hold period) | GOVERNANCE-SELECTABLE | The mechanism requires "a hold period" but the exact value is a design choice. K=5 is the default recommendation (5 minutes of post-break persistence) but must be explicitly frozen by the owner before registration. |
| Session scope | GOVERNANCE-SELECTABLE | The mechanism operates whenever structural levels exist, but a session filter may be applied. Default: no session filter (24-hour). |
| Maximum entry delay | GOVERNANCE-SELECTABLE | Maximum number of bars after validation before entry is abandoned. Default: 3 bars. |
| Cost model | FROZEN AT V38A REGISTRATION | Not a formulation parameter; frozen during V38A registration. |

### 17.2 Empirically tunable parameters

**None.** No parameter in this formulation is classified as empirically tunable. All parameters are either frozen by mechanism (none in this formulation), governance-selectable, or frozen at registration.

### 17.3 Default values

Default values are provided for completeness. They are NOT selected by historical testing. They are the simplest mechanism-consistent values:

- N = 60 (1 hour of M1 data — a structural lookback that captures recent price history without being arbitrarily long or short)
- K = 5 (5 minutes — a validation period that is long enough to distinguish acceptance from noise but short enough to be tradeable)
- Session scope = no filter (the mechanism operates whenever structural levels exist)
- Maximum entry delay = 3 bars

---

## 18. ALTERNATIVE FORMULATIONS

### Architecture A: Minimal (PROVISIONALLY SELECTED)

The simplest formulation that preserves the mechanism:
- Rolling N-bar high/low defines structural level
- Breakout = close beyond level
- Validation = K consecutive closes beyond level
- Entry at open of bar after validation
- Exit at session close
- No session filter, no stop-loss, no cooldown

**Assessment:**
- Mechanism fidelity: HIGH — directly implements the mechanism
- Determinism: HIGH — all decisions are binary
- Falsifiability: HIGH — validated vs. invalidated breakouts are directly comparable
- Execution realism: HIGH — simple entry/exit
- Simplicity: HIGH — minimum parameters (N, K)
- Parameter burden: LOW — only N and K

### Architecture B: Session-Filtered

Same as Architecture A, but restricted to US regular session (09:30–16:00 ET):
- Structural levels computed from bars within the session only
- Breakouts and validation evaluated within the session
- Entry and exit within the session

**Assessment:**
- Mechanism fidelity: MEDIUM — the mechanism does not inherently require session filtering, but the participant-behavior transition is more likely during active trading hours
- Determinism: HIGH
- Falsifiability: HIGH
- Execution realism: MEDIUM — requires session-time awareness
- Simplicity: MEDIUM — adds session-definition complexity
- Parameter burden: MEDIUM — session boundaries are governance-selectable

**Rejection rationale:** Session filtering is a legitimate design choice but adds a governance decision without mechanism necessity. The minimal formulation is preferred for its lower parameter burden and mechanism fidelity. Session filtering may be added as a future refinement.

### Architecture C: Retest Entry

Same as Architecture A, but entry occurs only after a retest of the breakout level:
- After K-bar validation, wait for price to return to the structural level
- Enter only if price bounces off the level (retest confirmation)

**Assessment:**
- Mechanism fidelity: LOW — the mechanism hypothesizes that validation itself triggers participant behavior change, not that a retest is required
- Determinism: MEDIUM — retest detection introduces ambiguity (how close must price get to the level?)
- Falsifiability: MEDIUM
- Execution realism: LOW — retests may not occur, missing many validated breakouts
- Simplicity: LOW — adds retest-definition complexity
- Parameter burden: HIGH — retest proximity threshold is a new parameter

**Rejection rationale:** The retest variant is inconsistent with the mechanism. The mechanism hypothesizes that the validation event itself (K-bar hold) triggers the participant-behavior transition. Requiring a retest adds a condition not present in the mechanism and introduces additional parameters and ambiguity.

### Architecture D: Multi-Level Confluence

Same as Architecture A, but requires breakouts of multiple structural levels (e.g., N1-bar high AND N2-bar high) to confirm:

**Assessment:**
- Mechanism fidelity: LOW — the mechanism is about single-level validation, not multi-level confluence
- Determinism: MEDIUM
- Falsifiability: MEDIUM
- Execution realism: LOW
- Simplicity: LOW
- Parameter burden: HIGH — multiple N values

**Rejection rationale:** Multi-level confluence is a different mechanism entirely. The MECH-N01 mechanism is about the validation of a single structural level. Adding confluence requirements changes the mechanism.

---

## 19. REJECTED FORMULATIONS

| Architecture | Reason for rejection | Category |
|-------------|---------------------|----------|
| Architecture B (Session-Filtered) | Adds session-definition complexity without mechanism necessity | Parameter burden |
| Architecture C (Retest Entry) | Inconsistent with mechanism (retest not hypothesized); adds ambiguity and parameters | Mechanism inconsistency, parameter burden |
| Architecture D (Multi-Level Confluence) | Different mechanism entirely (single-level validation vs. multi-level confluence) | Mechanism inconsistency |

---

## 20. PROVISIONALLY SELECTED FORMULATION

**Architecture A: Minimal** is the provisionally selected formulation.

Selection basis:
- Highest mechanism fidelity — directly implements the MECH-N01 mechanism
- Maximum determinism — all decisions are binary
- Maximum falsifiability — validated vs. invalidated breakouts are directly comparable
- Minimum parameter burden — only N and K (both governance-selectable)
- No outcome-driven design choices
- No hidden parameters, no hidden hindsight, no rescue framing

The formulation is PROVISIONALLY SELECTED for owner adjudication. It is NOT a validated Base.

---

## 21. REMAINING AMBIGUITIES

### 21.1 Session definition for exit timing

**Ambiguity:** The exit is defined as "session close," but USATECHIDXUSD trades nearly 24 hours. What constitutes "session close"?

**Options:**
1. Use the last bar of the US regular session (16:00 ET)
2. Use the last bar before the daily reset (if any)
3. Use a fixed time (e.g., 17:00 ET)
4. Let the owner define session boundaries at registration

**Recommendation:** Let the owner define session boundaries at registration. This is a governance-selectable decision, not a formulation ambiguity. The formulation specifies "session close" and leaves the exact definition to governance.

### 21.2 Overlapping validation windows

**Ambiguity:** If two structural levels produce breakouts on different bars but their validation windows overlap, the Base may have two concurrent trades. Is this intended?

**Resolution:** Yes. Each breakout is independent. Concurrent trades from independent breakouts are permitted. The mechanism does not restrict concurrent positions.

### 21.3 Structural level persistence after breakout

**Ambiguity:** After a breakout, the rolling N-bar high/low continues to update. If a new structural level forms during the validation window, does it affect the current breakout?

**Resolution:** No. Once a breakout is triggered (bar E), the breakout reference level is frozen. The rolling level may change, but validation uses the frozen level. The new structural level is relevant only for future breakouts.

---

## 22. GOVERNANCE COMPLIANCE

| Check | Result |
|-------|--------|
| MECH-N01 selection unchanged | PASS — formulation preserves the frozen mechanism |
| No historical performance used | PASS — no backtests, no returns, no expectancy, no Sharpe, no win rate |
| No protected-forward inspection | PASS — CAND-015/024/035 not inspected |
| No backtesting | PASS |
| No economics | PASS |
| No optimization | PASS — N and K are governance-selectable, not optimized |
| No threshold mining | PASS — no numerical thresholds selected from performance |
| No Base registration | PASS — Base Registry remains EMPTY |
| RF-001 unchanged | PASS |
| F-01 unchanged | PASS |
| FB-001 unchanged | PASS |
| No production-code changes | PASS |
| No test changes | PASS |
| No runner interruption | PASS |
| No broker orders | PASS |
| No closed research reopened | PASS |
| BF1 — Decision-process object | PASS — complete deterministic decision process |
| BF2 — Outcome-blind formulation | PASS — no outcome-driven design choices |
| BF3 — Historical-performance firewall | PASS — no historical results used |
| BF4 — Mechanism–observable–decision traceability | PASS — full chain specified |
| BF5 — State/decision separation | PASS — not a state promotion |
| BF6 — Complete decision semantics | PASS — all 11 questions answered |
| BF7 — Conditional independence | PASS — no future Conditional required |
| BF8 — Distinctiveness / redundancy control | PASS — distinct from all exhausted dimensions |
| BF9 — Negative-knowledge constraint | PASS — constraints respected |
| BF10 — No-rescue formulation | PASS — independently worthy of evaluation |
| BF11 — Research-capital control | PASS — single formulation, no budget breach |
| BF12 — Formulation/selection separation | PASS — labeled FORMULATED, not SELECTED |
| BF13 — Prospective freeze transition | PASS — formulation ready for BS1–BS13 selection |

---

## 23. FINAL VERDICT

**BF1–BF13 FORMULATION COMPLETE — PROVISIONALLY SELECTED ARCHITECTURE READY FOR OWNER ADJUDICATION**

The minimal formulation (Architecture A) is the provisionally selected architecture. It directly implements the MECH-N01 mechanism with maximum determinism and minimum parameter burden. Two governance-selectable parameters (N, K) require owner specification before registration. One remaining ambiguity (session definition for exit timing) is delegated to governance.

The Base Registry remains EMPTY. This formulation is NOT a validated Base. It is a formulation proposal subject to BS1–BS13 selection before V38A registration.

---

**Formulation record SHA256:** `0a82d181219a7bf49c0f9e64a7d0240c666e06db9ad6d41089f7b5af96a5226c`

**Next governed step:** Owner adjudication of this formulation, followed (if approved) by BS1–BS13 selection and V38A registration.

---

**END OF MECH-N01 OUTCOME-BLIND BASE FORMULATION V1**
