# QUANTFORGE — RF-001 V38A STAGE 1 REGISTRATION

**Date:** 2026-09-07
**Status:** STAGE 1 REGISTRATION FROZEN — STAGE 2 AUTHORIZED
**Purpose:** Complete deterministic prospective V38A registration for RF-001

---

## 1. OWNER SELECTION RECORD

**Selected formulation:** RF-001 — Cross-Market Confirmation Failure Process

**Source mechanism:** REL-M01

**Source formulation artifact:** `QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md`

**Owner selection artifact:** `QUANTFORGE_RF001_OWNER_SELECTION_FREEZE_V1.md`

**Owner selection artifact SHA256:** `7f34240191a3bd3812c40650ae0067cc2b38ba43f00553e7c16ffd6ec076d175`

**Owner selection commit:** `6644487`

**Selection type:** Owner-directed prospective governance choice

**Historical economic results used:** NO

**FB-001 economics used:** NO

**F-01 economics used:** NO

**Protected-forward economics used:** NO

**Optimization performed:** NO

**Parameter tuning performed:** NO

**Closed research reopened:** NO

---

## 2. REGISTRATION IDENTITY

| Field | Value |
|-------|-------|
| Registration ID | `RF-001-V38A-REG-V1` |
| Title | Cross-Market Confirmation Failure Process |
| Primary market | USATECHIDXUSD (USTECm) |
| Confirmation market | US500 |
| Timeframe | M1 |
| Session | US regular session (09:30–16:00 ET) |
| Status at freeze | SELECTED FOR V38A REGISTRATION — NOT YET A BASE |
| Base Registry | EMPTY |

---

## 3. MECHANISM

A structurally significant directional event in the primary USATECHIDXUSD market is expected to receive directional confirmation from US500 within a finite confirmation window. Failure of US500 to produce the corresponding confirming event within that window is hypothesized to represent a distinct cross-market information/positioning state and becomes the decision event.

The registered process is NOT:

- Correlation divergence
- Lead/lag
- Spread mean reversion
- Synchrony regime
- Ordinary momentum
- Breakout continuation

The specific event is:

`PRIMARY STRUCTURAL EVENT → CONFIRMATION WINDOW → CONFIRMATION FAILURE`

---

## 4. PRIMARY STRUCTURAL EVENT

**Lookback horizon:** N = 30 completed M1 bars

### Bullish structural event

The close of a completed USATECHIDXUSD M1 bar is strictly greater than the highest high of the prior 30 completed USATECHIDXUSD M1 bars.

### Bearish structural event

The close of a completed USATECHIDXUSD M1 bar is strictly less than the lowest low of the prior 30 completed USATECHIDXUSD M1 bars.

### Equality

If close equals the highest high or lowest low — NO EVENT.

### Bar model

Completed bars only: `[bar_open_time, bar_close_time)` with `bar_close_time = bar_open_time + 1 minute`.

No forming bar may affect event detection.

---

## 5. CONFIRMATION EVENT

The confirmation event uses the identical N-bar breakout construction applied to US500's own data.

**Source formulation (verbatim):** *"Confirmation is defined as: the close of any M1 bar in the confirmation market exceeds (for bullish) or falls below (for bearish) the confirmation market's own N-bar high/low within the M-bar window."*

### Bullish confirmation event

The close of any completed US500 M1 bar within the confirmation window is strictly greater than the highest high of the prior 30 completed US500 M1 bars at that point in time.

### Bearish confirmation event

The close of any completed US500 M1 bar within the confirmation window is strictly less than the lowest low of the prior 30 completed US500 M1 bars at that point in time.

### Confirmation clock

The confirmation clock begins on the bar immediately after the primary structural event bar.

If the primary event completes at bar E (the event bar is bar E):

- Confirmation bar 1 = bar E+1
- Confirmation bar 2 = bar E+2
- ...
- Confirmation bar 15 = bar E+15

The event bar itself (bar E) does NOT count toward the M=15 confirmation window. The following bar (E+1) is confirmation bar 1. Confirmation bar 15 (bar E+15) is the final eligible confirmation observation.

---

## 6. CONFIRMATION FAILURE

Confirmation failure occurs only when ALL of the following are true:

1. A qualifying primary structural event has occurred.
2. The corresponding US500 confirmation event has NOT occurred within the full 15-bar confirmation window (bars E+1 through E+15).
3. The primary event has not been invalidated under the frozen formulation.

Failure is known only once the registered confirmation window has expired — i.e., at the close of confirmation bar 15 (bar E+15).

Do NOT generate a failure event early merely because confirmation has not yet happened within the first K < 15 bars.

---

## 7. M-BAR TIMING

| Bar | Event | Information known |
|-----|-------|-------------------|
| E | Primary structural event | USATECHIDXUSD close exceeds 30-bar high/low |
| E+1 | Confirmation bar 1 | US500 bar 1 checked against its own 30-bar range |
| E+2 | Confirmation bar 2 | US500 bar 2 checked against its own 30-bar range |
| ... | ... | ... |
| E+15 | Confirmation bar 15 (final) | US500 bar 15 checked — confirmation either occurred or failed |
| E+16 | Decision bar | Confirmation failure confirmed; decision made at close of this bar |
| E+17 | Entry bar | Position entered at open of this bar |

**M-bar counting convention:** Event bar E is bar 0. The following bar (E+1) is confirmation bar 1. Confirmation bar 15 (bar E+15) is the final eligible confirmation observation. Decision is made at close of bar E+16. Entry is at open of bar E+17.

This convention is deterministic and deterministic only in this form.

---

## 8. DECISION MAPPING

### Bullish primary event + failed US500 bullish confirmation

`SHORT US500`

### Bearish primary event + failed US500 bearish confirmation

`LONG US500`

The direction mapping is explicit and deterministic:

```
PRIMARY_EVENT DIRECTION → US500 POSITION
BULLISH PRIMARY + FAILED CONFIRMATION → SHORT US500
BEARISH PRIMARY + FAILED CONFIRMATION → LONG US500
```

No discretionary direction selection. No relative-direction ambiguity. The position is always in US500, always opposite to the primary event direction.

---

## 9. ENTRY

Entry at the open of bar E+17 (the bar after the decision bar E+16).

All information used for the decision is known before execution. Temporal causality preserved.

No modified entry. No limit orders. No improvement logic.

---

## 10. INVALIDATION

If USATECHIDXUSD closes back within its N-bar range before the position is entered, the opportunity is cancelled.

**"Reverses its structural event" defined exactly:**

For a bullish primary event at bar E: USATECHIDXUSD closes at or below the highest high of the 30-bar lookback (the same high that the event exceeded) at any point before entry at bar E+17 open.

For a bearish primary event at bar E: USATECHIDXUSD closes at or above the lowest low of the 30-bar lookback (the same low that the event fell below) at any point before entry at bar E+17 open.

If invalidation occurs: no position is taken. The opportunity is cancelled.

No stop-losses. No take-profits. No additional invalidation rules.

---

## 11. POSITION

States: `FLAT` | `LONG` | `SHORT`

Position is in: `US500`

Maximum one position at a time.

If a new opportunity arises while a position is open, the existing position is held to session close. No new position is opened.

---

## 12. EXIT

Exit at the close of the session (16:00 ET).

Single-session position. No overnight holding.

Market order at session close.

---

## 13. OPPORTUNITY POPULATION

**One opportunity = one valid primary structural event that survives the registered invalidation rules and reaches a confirmation-failure decision.**

### Eligible primary events

- USATECHIDXUSD close exceeds highest high of prior 30 completed M1 bars (bullish)
- USATECHIDXUSD close falls below lowest low of prior 30 completed M1 bars (bearish)
- Event occurs in US regular session (09:30–16:00 ET)
- Sufficient session time remains for confirmation window (M=15 bars) + decision bar + entry bar
- No position is currently open

### Excluded events

- Events in the last 17 bars of the session (insufficient time for 15-bar confirmation window + decision bar E+16 + entry at E+17 open)
- Equality (close equals the 30-bar high or low): no event

### Invalidated events

- Primary market reverses (close returns within 30-bar range) before entry

### Successfully confirmed events

- US500 produces the corresponding directional breakout within the 15-bar window

### Confirmation failures

- No US500 confirmation within 15 bars AND primary has not reversed → decision triggered

### Duplicate/continuation events

- Same-direction primary breakouts without an intervening reversal in the same session are treated as continuation, not new independent opportunities
- No new opportunity generated

---

## 14. DATA REQUIREMENTS

### Per synchronized M1 bar

**Primary USATECHIDXUSD:**

| Field | Description |
|-------|-------------|
| Timestamp | Bar open time (UTC or ET-normalized) |
| Open | Open price |
| High | High price |
| Low | Low price |
| Close | Close price |

**Confirmation US500:**

| Field | Description |
|-------|-------------|
| Timestamp | Bar open time (UTC or ET-normalized) |
| Open | Open price |
| High | High price |
| Low | Low price |
| Close | Close price |

### Synchronization

Both markets must be aligned using the same canonical temporal basis. A bar is "aligned" if both USATECHIDXUSD and US500 have a completed bar with the same open timestamp.

### Missing-bar handling

If a bar is missing for either market at a given timestamp: skip that timestamp. Do not interpolate. Do not impute. Do not forward-fill.

### Duplicate handling

If a timestamp appears more than once for either market: use the first occurrence. Discard duplicates.

### Malformed-bar handling

If a bar has any of: open = 0, high = 0, low = 0, close = 0, high < low, close < low, close > high — skip that bar.

### Out-of-order handling

Bars must be processed in timestamp order. If bars are received out of order, sort by timestamp before processing.

### Data insufficiency

If required data is unavailable: `BLOCKED / INCOMPLETE`. Do not create proxy data.

---

## 15. TEMPORAL / LEAKAGE DEFINITION

| Stage | Information known | What cannot be used |
|-------|-------------------|---------------------|
| Primary event detection (bar E close) | USATECHIDXUSD close exceeds 30-bar high/low | US500 bar E data; any future bars |
| Confirmation bar 1 (bar E+1 close) | US500 bar E+1 close vs its own 30-bar range | US500 bars E+2 through E+15; USATECHIDXUSD bars E+1 onward for confirmation |
| Confirmation bar 2 (bar E+2 close) | US500 bar E+2 close vs its own 30-bar range | Future confirmation bars |
| ... | ... | ... |
| Confirmation bar 15 (bar E+15 close) | US500 bar E+15 close vs its own 30-bar range | Nothing later needed for confirmation decision |
| Decision bar (bar E+16 close) | Confirmation failure confirmed | No new information needed |
| Entry (bar E+17 open) | Position taken | Must not use post-entry information |

At each stage, only information from completed bars at or before the current bar is available. No future information from either market influences any decision.

---

## 16. PROSPECTIVE VALIDATION DESIGN

**Registration freeze timestamp:** 2026-09-07 (this artifact)

**Data domain:** Forward-only prospective data from 2026-09-06 08:00 ET onward

**Economic validation population:** Only eligible complete observations generated after registration freeze.

**Pre-freeze data:** May be used only for Stage 2 structural validation. Not used for economic validation.

**Backfill:** Not permitted. No historical outcomes admitted into economic validation.

---

## 17. COST MODEL

**Entry:** 1 bps (market order at open)

**Exit:** 1 bps (market order at session close)

**Total round-trip:** 2 bps

Applied mechanically to gross return.

No spread modeling. No variable slippage. No financing. No market impact.

The cost model is evidence/measurement infrastructure, not a qualification gate.

---

## 18. REPRODUCIBILITY AUDIT

| Component | Deterministic? | Resolution |
|-----------|---------------|------------|
| Primary event | YES | Close > highest high of prior 30 completed M1 bars (bullish) or close < lowest low (bearish). Equality = no event. |
| Confirmation event | YES | US500 close > its own 30-bar highest high (bullish) or < its own 30-bar lowest low (bearish). Identical N-bar construction applied to US500. |
| M-bar timing | YES | Event bar = E. Confirmation bars = E+1 through E+15. Decision bar = E+16. Entry bar = E+17. Event bar does not count toward M. |
| Confirmation failure | YES | No US500 confirmation event in bars E+1 through E+15. |
| Invalidation | YES | USATECHIDXUSD close returns within 30-bar range before entry at E+17 open. |
| Decision direction | YES | Bullish primary + failed confirmation → SHORT US500. Bearish primary + failed confirmation → LONG US500. |
| Entry bar | YES | Open of bar E+17. |
| Exit | YES | Session close (16:00 ET). |
| Opportunity population | YES | One per qualifying event; deduplication by same-direction continuation; exclusion of events too late in session. |
| Synchronization | YES | Both markets aligned by bar open timestamp. Missing/malformed bars skipped. |
| Cost | YES | 2 bps round-trip applied mechanically. |

**Independent implementability:** PASS — an independent engineer can construct the complete timeline and implementation without asking any clarifying questions.

---

## 19. MECHANISM PRESERVATION

| Check | Result |
|-------|--------|
| Mechanism: Primary structural event → US500 confirmation window → confirmation failure → fade US500 | VERIFIED |
| Still distinct from correlation divergence? | YES — trigger is discrete event, not continuous correlation |
| Still distinct from lead/lag? | YES — trigger is event failure, not timing asymmetry |
| Still distinct from spread mean reversion? | YES — trigger is failure detection, not spread level |
| Still distinct from momentum? | YES — trigger is cross-market event, not own-history |
| Still distinct from breakout/ORB? | YES — trigger is failure detection, not breakout itself |
| Still distinct from synchrony regime? | YES — trigger is event failure, not regime transition |
| Still distinct from shock absorption? | YES — trigger is confirmation failure, not shock processing |

**MECHANISM PRESERVED: YES**

---

## 20. DISTINCTNESS PRESERVED

All prior work distinctly different from this registration. No formulation collapses into closed research.

---

## 21. OUTCOME-BLIND INTEGRITY

| Check | Result |
|-------|--------|
| Historical economics used | NO |
| FB-001 economics used | NO |
| F-01 economics used | NO |
| Protected-forward economics used | NO |
| Optimization performed | NO |
| Parameter tuning performed | NO |
| Closed research reopened | NO |
| N=30 chosen from historical performance | NO |
| M=15 chosen from historical performance | NO |
| US500 chosen from historical performance | NO |

**OUTCOME-BLIND: CERTIFIED**

---

## 22. DEFERRED FORMULATIONS

| Formulation | Status |
|-------------|--------|
| RF-002 — Cross-Market Synchrony Regime Process | DEFERRED |
| RF-003 — Cross-Market Shock Absorption Asymmetry Process | DEFERRED |

---

## 23. GOVERNANCE STATUS

| Item | Status |
|------|--------|
| RF-001 | SELECTED FOR V38A REGISTRATION — STAGE 1 FROZEN |
| RF-002 | DEFERRED |
| RF-003 | DEFERRED |
| FB-001 | UNCHANGED |
| F-01 | UNCHANGED |
| Base Registry | EMPTY (unchanged) |
| V38A Stage 2 | NOT YET EXECUTED — AUTHORIZED AFTER THIS REGISTRATION |
| V38A Stage 3 | NOT AUTHORIZED |

---

## 24. FREEZE STATEMENT

This registration is frozen as of 2026-09-07.

The frozen registration consists of:

1. Registration ID: RF-001-V38A-REG-V1
2. Primary market: USATECHIDXUSD
3. Confirmation market: US500
4. N = 30 completed M1 bars
5. M = 15 completed M1 bars
6. Structural event: 30-bar breakout (close > highest high or close < lowest low)
7. Confirmation event: US500's own 30-bar breakout within 15-bar window
8. Failure: no US500 confirmation in 15 bars
9. Decision: bullish primary + failed confirmation → SHORT US500; bearish primary + failed confirmation → LONG US500
10. Entry: open of bar E+17 (after decision bar E+16)
11. Exit: session close (16:00 ET)
12. Invalidation: primary reverses before entry
13. Cost: 2 bps round-trip
14. Session: US regular session (09:30–16:00 ET)

Any future correction requires a new governed revision.

No parameter may be changed without a new governed revision.

No additional filters, regimes, conditions, or Conditional layers may be introduced without a new governed decision.

---

**END OF V38A STAGE 1 REGISTRATION**
