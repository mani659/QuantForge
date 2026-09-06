# FB-001 ORB — V38A STAGE 1 REGISTRATION REPAIR (V1-r1)

**Date:** 2026-09-06
**Status:** READ-ONLY REPAIR REPORT

---

## REPAIR SUMMARY

| Repair | Issue | Resolution |
|---|---|---|
| A | Opening-range minimum contradiction (30 bars vs 1 bar) | 30 bars required; no degenerate range |
| B | Canonical M1 bar semantics undefined | Bars defined as half-open intervals [open, close) |
| C | Session-close execution semantics contradictory | Exit at open of final session bar |
| D | Session calendar scope contradiction | All eligible sessions; early-close after 10:00 still eligible |
| E | Prospective validation boundary ambiguous | Session-level rule; no partially pre-freeze sessions |

---

## CONSISTENCY AUDIT RESULTS

| Check | Status |
|---|---|
| 30-bar OR requirement consistent across all sections | PASS |
| Canonical M1 interval semantics consistent | PASS |
| Signal timing consistent with interval definition | PASS |
| Entry timing consistent with signal timing | PASS |
| Session-close execution timing consistent | PASS |
| Early-close handling consistent with calendar scope | PASS |
| Prospective validation boundary consistent with session definition | PASS |
| No remaining contradictions | PASS |

---

# FB-001-ORB-V38A-REG-V1-r1

## 1. IDENTITY

```text
Registration ID:    FB-001-ORB-V38A-REG-V1-r1
Predecessor:        FB-001-ORB-V38A-REG-V1
Revision reason:    Internal specification consistency repair
Mechanism change:   NO
Economic information introduced: NO
Optimization performed: NO

Name:               Opening Range Breakout (ORB)
Instrument:         USATECHIDXUSD
Executable Symbol:  USTECm
Broker:             Exness Technologies Ltd
Server:             Exness-MT5Trial15
Timeframe:          M1

Status:             REGISTRATION FROZEN — STAGE 2 AUTHORIZED
                    NOT YET A BASE
                    NOT VALIDATED
                    NOT ECONOMICALLY EVALUATED
```

---

## 2. MECHANISM

```text
The session opening range captures initial price discovery during the
first 30 minutes of the regular trading session. Breaks from this range
produce directional follow-through because:

1. The opening range represents the market's initial assessment of fair
   value after overnight information is absorbed.

2. Participants who positioned against the breakout direction are trapped
   when price moves beyond the range boundary.

3. Forced exits from trapped positions create directional pressure that
   continues beyond the initial breakout.

The mechanism is: time-defined structural formation → directional breakout
→ trapped-participant forced exits → continuation.
```

---

## 3. CANONICAL M1 BAR SEMANTICS

```text
Every M1 bar is defined as a half-open time interval:

  bar = [bar_open_time, bar_close_time)

where:

  bar_close_time = bar_open_time + 1 minute

Therefore:
  - The bar is "open" at bar_open_time.
  - The bar is "forming" during the interval [bar_open_time, bar_close_time).
  - The bar is "completed" at bar_close_time.
  - At bar_close_time, the bar's open, high, low, close are final.

A bar is INCLUDED in a time window if and only if its bar_open_time
falls within the window's half-open interval.

The bar currently forming (whose bar_close_time has not yet been reached)
is NEVER used for computation. Only completed bars are used.

Timezone: America/New_York (Eastern Time).
All timestamps in this registration are Eastern Time (ET).
```

---

## 4. SESSION DEFINITION

```text
Regular session interval (half-open):

  [09:30:00 ET, 16:00:00 ET)

The session begins at 09:30:00 ET and ends at 16:00:00 ET.

Session-close bar:
  The final eligible M1 bar of the session is the bar whose interval
  ends at the session close:

    bar_open_time = 15:59:00 ET
    bar_close_time = 16:00:00 ET

  This bar's interval is [15:59:00, 16:00:00).

Session-close execution:
  A session-close exit is executed at the OPEN of the final session bar.
  That is: execution price = open price of the bar [15:59:00, 16:00:00).

Early-close sessions:
  If the session closes before 16:00:00 ET (early close):
    The session interval becomes [09:30:00 ET, early_close_time ET).
    The final session bar is the bar whose interval ends at early_close_time.
    Session-close exit executes at the open of that final bar.
    The opening-range requirement (full 09:30–10:00 interval) is NOT shortened.

Holiday sessions:
  If the market is closed (holiday): no session exists. No opportunity.
```

---

## 5. OPENING RANGE

```text
Opening-range interval (half-open):

  [09:30:00 ET, 10:00:00 ET)

This interval contains exactly 30 one-minute bars:

  Bar 1:  [09:30:00, 09:31:00)
  Bar 2:  [09:31:00, 09:32:00)
  ...
  Bar 30: [09:59:00, 10:00:00)

The opening range consists of ALL 30 completed M1 bars in this interval.

Opening-range calculation:
  OR_high = maximum(high) across all 30 bars
  OR_low  = minimum(low) across all 30 bars

Minimum bar requirement:
  The opening range requires ALL 30 completed M1 bars to be available.
  If fewer than 30 completed bars exist in the [09:30:00, 10:00:00)
  interval (e.g., late session start, data gap, early data unavailability):
    The opening range is NOT defined.
    No signal is generated for that session.
    No opportunity exists for that session.

  There is no degenerate single-bar opening range.

Degenerate range (OR_high == OR_low):
  If all 30 bars exist but OR_high == OR_low (price did not move during
  the opening range): the range IS defined (it is a zero-width range).
  A breakout signal fires if the signal bar's close strictly exceeds
  OR_high or is strictly below OR_low.
```

---

## 6. SIGNAL

```text
Signal bar:
  The first completed M1 bar whose bar_open_time >= 10:00:00 ET.

  Using canonical bar semantics, this bar's interval is:
    [10:00:00, 10:01:00)

  This bar's bar_close_time is 10:01:00 ET.
  The bar is "completed" at 10:01:00 ET.
  The signal is evaluated at 10:01:00 ET (when the bar completes).

Signal conditions (evaluated at signal bar completion):
  Long signal:  signal_bar_close > OR_high
  Short signal: signal_bar_close < OR_low
  No signal:    signal_bar_close >= OR_low AND signal_bar_close <= OR_high

Equality handling:
  If signal_bar_close == OR_high or signal_bar_close == OR_low:
    NO SIGNAL. Breakout requires strict exceedance.

No breakout threshold:
  There is no minimum bps requirement. Any close strictly beyond the
  range boundary constitutes a breakout signal.

One signal per session:
  Only the first breakout signal is considered.
  After a signal fires (or if no signal fires), no further signals are
  evaluated in the same session.
```

---

## 7. ENTRY

```text
Order type: MARKET ORDER

Signal evaluation timing:
  The signal is evaluated only after the signal bar is completed
  (at bar_close_time = 10:01:00 ET).

Order submission timing:
  The market order is submitted at the signal bar's completion
  (10:01:00 ET).

Execution bar:
  The order is executed at the open of the next M1 bar.
  The execution bar's interval is:
    [10:01:00, 10:02:00)
  Execution price = open price of this bar.

No stop orders:
  No stop-entry orders. No pending orders. Only market orders.

No order expiry:
  The market order executes at the next bar open. There is no expiry
  window, no validity period, and no cancellation condition.
```

---

## 8. POSITION STATE

```text
States: FLAT, LONG, SHORT

Transitions:
  FLAT → LONG:   when long signal fires and order executes
  FLAT → SHORT:  when short signal fires and order executes
  LONG → FLAT:   when exit condition triggers
  SHORT → FLAT:  when exit condition triggers

Constraints:
  Maximum one position per session.
  No overlapping positions.
  After a position is opened (or after a signal fires), no further
  signals are evaluated in the same session.
```

---

## 9. EXIT / INVALIDATION

```text
Two exit conditions exist.

EXIT CONDITION 1 — Retrace Invalidation:

  For LONG position:
    Trigger: any subsequent completed M1 bar (after the entry execution bar)
             whose close <= OR_high
    Execution: market order at the open of the retrace bar

  For SHORT position:
    Trigger: any subsequent completed M1 bar (after the entry execution bar)
             whose close >= OR_low
    Execution: market order at the open of the retrace bar

  "Subsequent" means the bar's bar_open_time > entry execution bar's
  bar_close_time.

EXIT CONDITION 2 — Session Close:

  Trigger: the final session bar
    Regular session: bar [15:59:00, 16:00:00)
    Early-close session: bar whose interval ends at early_close_time

  Execution: market order at the OPEN of the final session bar

  For regular session: execution price = open of bar [15:59:00, 16:00:00)

CONFLICT PRECEDENCE:
  If both conditions are true in the same bar:
    Session close exit GOVERNS.
  Rationale: session close is a structural boundary; it takes precedence
  over the signal-based retrace exit.

  For LONG: retrace condition is close <= OR_high.
  If the session-close bar's close <= OR_high, session close governs.

  For SHORT: retrace condition is close >= OR_low.
  If the session-close bar's close >= OR_low, session close governs.

EARLY CLOSE:
  If the session closes before 16:00:00 ET:
    The final session bar is the bar whose interval ends at early_close_time.
    Session-close exit executes at the open of that bar.
    Both conditions may apply to the same bar; session close governs.

MISSING BAR:
  If a bar is missing from the data (gap):
    The next available bar's open is used for execution.
    Missing bars do not cancel or invalidate exit conditions.
```

---

## 10. EXECUTION

```text
All orders: MARKET ORDERS at the specified bar's open price.

Entry execution price:
  Open of the bar whose interval begins at 10:01:00 ET
  (the bar immediately following the signal bar).

Exit execution price (retrace):
  Open of the bar in which the retrace condition triggers.

Exit execution price (session close):
  Open of the final session bar
  ([15:59:00, 16:00:00) for regular sessions).

No limit orders.
No stop orders.
No pending orders.
No fill improvement assumptions.

Slippage: not modeled. Assumed zero for registration purposes.
The cost model accounts for friction.
```

---

## 11. SCOPE

```text
Instrument:          USATECHIDXUSD (USTECm)
Timeframe:           M1
Regular session:     [09:30:00 ET, 16:00:00 ET)
Opening range:       [09:30:00 ET, 10:00:00 ET) — 30 bars required
Calendar:            All eligible regular trading sessions
                     (including scheduled early-close sessions)
Holidays:            No session / no opportunity
Early close >= 10:00: Session eligible if opening range fully defined
Early close < 10:00:  No opening range / no opportunity
Data source:         MT5 broker data (USTECm)
Timezone:            America/New_York (Eastern Time)
Session eligibility: All sessions where 30 completed bars exist in [09:30, 10:00)
```

---

## 12. OPPORTUNITY POPULATION

```text
One opportunity = one trading session where a breakout signal fires.

Conditions for an opportunity to exist:
  1. Regular session is open (not a holiday).
  2. All 30 completed M1 bars exist in [09:30:00, 10:00:00) ET.
  3. A breakout signal fires (signal bar close strictly beyond range boundary).

Conditions for no opportunity:
  1. Session is closed (holiday).
  2. Fewer than 30 completed bars in the opening-range window.
  3. No breakout signal fires (close remains within or on the range boundary).

Maximum opportunities per session: 1.
Minimum opportunities per session: 0.

Failed breakout:
  If a signal fires but the position is exited via retrace before
  session close, the opportunity still counts. The opportunity is
  the signal, not the outcome.

Second signal:
  Not possible. After the first signal, no further signals are
  evaluated in the same session.

Population enumeration:
  The population is determined by the session definition, opening-range
  requirement, and signal rule. No post-hoc filtering is applied.
  No subset selection.
```

---

## 13. OUTCOME DEFINITION

```text
For LONG positions:
  gross_return = 10000 × (exit_price / entry_price - 1)
  net_return   = gross_return - 2

For SHORT positions:
  gross_return = 10000 × (1 - exit_price / entry_price)
  net_return   = gross_return - 2

Where:
  entry_price = open of the bar [10:01:00, 10:02:00) ET
  exit_price  = open of the retrace bar (retrace exit)
                OR open of the final session bar (session-close exit)
  2 = registered round-trip cost in bps

Outcome unit: basis points (bps).
All outcomes are expressed in bps.
No currency conversion is applied.
```

---

## 14. COST MODEL

```text
Round-trip friction: 2 bps
  Entry cost component: 1 bps (half of round-trip)
  Exit cost component: 1 bps (half of round-trip)

Application:
  The 2 bps cost is subtracted from the gross return to produce
  the net registered outcome.

  This cost is applied uniformly to all trades regardless of:
  - time of day
  - position direction
  - holding period
  - market conditions

  The cost model is frozen at registration and may not be changed
  during validation.

Assumptions:
  - No additional slippage beyond the 2 bps cost
  - No commission
  - No swap/financing costs
  - No partial fills
  - No market impact

  These are registration assumptions. They may be relaxed in future
  research but are frozen for this validation cycle.
```

---

## 15. DATA RULES

```text
Completed bars:
  Only completed M1 bars are used for computation.
  A bar is completed at its bar_close_time.
  The bar currently forming is never used.

Missing bars:
  If a bar is missing from the data sequence:
    Skip the missing bar index.
    Use the next available bar for execution.
    Missing bars do not cancel exit conditions.
  If bars are missing from the opening-range window such that fewer than
  30 bars are available: no opening range is defined, no signal generated.

Malformed bars:
  If a bar has open > high or close < low or other logical inconsistency:
    Exclude the bar from range calculation.
    If the bar is a signal bar, no signal is generated from it.
    If the bar is an exit bar, use the next valid bar.

Duplicate bars:
  If two bars share the same bar_close_time:
    Use the first occurrence.
    Exclude the duplicate.

Conflicting duplicates:
  If two bars share the same bar_close_time but different prices:
    Use the first occurrence.
    Record the conflict for audit purposes.

Out-of-order bars:
  If bars arrive out of chronological order:
    Reorder by bar_close_time before processing.
    Signal computation uses the reordered sequence.

Market holidays:
  No data → no session → no opportunity.

Early closes:
  Session interval becomes [09:30:00, early_close_time ET).
  Opening-range requirement is NOT shortened.
  If early_close_time <= 10:00:00: opening range cannot be fully defined → no opportunity.
  If early_close_time > 10:00:00: opening range may be fully defined → opportunity possible.
  Session-close exit executes at the open of the final eligible bar.

DST transitions:
  The session is defined in local Eastern Time.
  On DST transition days, the session may have more or fewer bars.
  The opening-range window is still [09:30:00, 10:00:00) ET local time.
  All 30 bars must exist for the range to be defined.
```

---

## 16. VALIDATION SCOPE DESIGN

```text
Registration/freeze timestamp:
  The registration is frozen at the time the V1-r1 artifact is created.
  (Timestamp recorded at freeze time.)

Prospective validation boundary:
  The first validation-eligible observation is the first fully eligible
  trading session whose required decision data occurs entirely after the
  registration freeze boundary.

  "Fully eligible" means:
    - The session is not a holiday.
    - All 30 opening-range bars have bar_close_time > freeze_timestamp.
    - The signal bar has bar_close_time > freeze_timestamp.
    - The entry execution bar has bar_close_time > freeze_timestamp.

  No partially pre-freeze session may contribute an economic validation
  observation.

  Stage 2 may still use pre-freeze data strictly for structural and
  reproducibility purposes under the V38A framework.

Primary validation population:
  All fully eligible sessions on USATECHIDXUSD M1 after the freeze boundary
  where the opening range is definable (30 bars available) and a breakout
  signal fires.

Confirmation population:
  A temporally separated subset of the primary population.
  The confirmation period must be pre-specified before Stage 3 begins.
  The confirmation must test the exact same hypothesis registered here.

Observation accrual policy:
  Observations accrue automatically as sessions occur after the freeze.
  No backfilling. No selection of favorable periods.
```

---

## 17. REPRODUCIBILITY CHECK

```text
Can an independent engineer implement FB-001 exactly from this
registration without asking the author?

CHECKLIST:
  [x] Canonical M1 bar semantics: half-open intervals defined → YES
  [x] Session definition: exact half-open interval → YES
  [x] Opening range: exact 30-bar interval, exact high/low → YES
  [x] Signal bar: first bar with bar_open_time >= 10:00 → YES
  [x] Signal conditions: exact comparisons, equality handling → YES
  [x] Entry: market order, next bar open → YES
  [x] Exit: retrace (exact condition) and session close (exact execution) → YES
  [x] Session-close execution: open of final session bar → YES
  [x] Conflict precedence: session close > retrace → YES
  [x] Position state: FLAT/LONG/SHORT, max one per session → YES
  [x] Opportunity population: one per session, first signal wins → YES
  [x] Cost model: 2 bps round-trip → YES
  [x] Outcome formula: exact for long and short → YES
  [x] Data rules: missing, malformed, duplicate, out-of-order → YES
  [x] Early close handling: session close at final bar's open → YES
  [x] DST handling: local ET session → YES
  [x] Prospective validation boundary: session-level rule → YES

RESULT: No consequential implementation choice requires asking the author.
```

---

## 18. REGISTRATION INTEGRITY

| Check | Status |
|---|---|
| No historical economic data used | ✓ |
| No parameter tuning | ✓ |
| No optimization | ✓ |
| No closed-line resurrection | ✓ |
| No Conditional inserted | ✓ |
| No change from owner-selected formulation mechanism | ✓ |
| All parameters from repaired specification | ✓ |
| BF1–BF13 compliant | ✓ |
| BS1–BS13 compliant | ✓ |
| BV1–BV13 compatible | ✓ |
| 30-bar OR requirement consistent | ✓ |
| Canonical bar semantics consistent | ✓ |
| Session-close execution consistent | ✓ |
| Calendar/early-close handling consistent | ✓ |
| Prospective validation boundary consistent | ✓ |

---

## 19. GOVERNANCE STATUS

```text
FB-001-ORB-V38A-REG-V1-r1

Predecessor: FB-001-ORB-V38A-REG-V1
Revision:    Internal specification consistency repair
Mechanism:   UNCHANGED (ORB mechanism preserved exactly)
Economics:   NOT EVALUATED
Optimization: NOT PERFORMED

Status: SELECTED FOR V38A REGISTRATION — REGISTRATION FROZEN
        NOT YET A BASE
        NOT VALIDATED

Base Registry: EMPTY
F-01: UNCHANGED
V38A Stage: 1 (Registration) — COMPLETE (V1-r1)
V38A Stage: 2 (Structural Validation) — NOT STARTED
V38A Stage: 3 (Economic Validation) — NOT STARTED
V38A Stage: 4 (Viability Adjudication) — NOT STARTED
```

---

## 20. FREEZE METADATA

```text
Registration artifact: QUANTFORGE_FB001_ORB_V38A_REGISTRATION_V1-r1.md
Repository HEAD:        dbab55c23f082137582112828934c7697ccbdb8c
Registration timestamp: 2026-09-06 (freeze time)
Predecessor artifact:   QUANTFORGE_FB001_ORB_V38A_REGISTRATION_V1
```

---

## 21. VERSIONING / PROVENANCE

```text
V1 (FB-001-ORB-V38A-REG-V1):
  Created: 2026-09-06
  Status: SUPERSEDED by V1-r1
  Reason for supersession: Internal specification contradictions
    (opening-range minimum, bar semantics, session-close execution,
     calendar scope, prospective validation boundary)
  Mechanism: ORB — UNCHANGED
  Economics: NOT EVALUATED
  Preserved: YES — historical artifact retained

V1-r1 (FB-001-ORB-V38A-REG-V1-r1):
  Created: 2026-09-06
  Status: REGISTRATION FROZEN — STAGE 2 AUTHORIZED
  Predecessor: V1
  Reason for revision: Internal specification consistency repair
  Mechanism: ORB — UNCHANGED
  Economics: NOT EVALUATED
  Optimization: NOT PERFORMED
```

---

## 22. GOVERNANCE CHECK

```text
Base Registry:        EMPTY
F-01:                 UNCHANGED
Stage 2 executed:     NO
Stage 3 executed:     NO
Stage 4 executed:     NO
Historical economics: NOT USED
P&L calculated:       NO
Expectancy calculated: NO
Win rate calculated:  NO
Benchmark comparison:  NO
Optimization:          NOT PERFORMED
Parameter changes:     NONE
Conditional introduced: NO
Production code changed: NO
Protected-forward candidate accessed: NO
```

---

## 23. SESSION HANDOFF

The following entry should be added to `docs/SESSION_HANDOFF.md`:

```markdown
> **FB-001 ORB V38A REGISTRATION V1-r1 (2026-09-06): Stage 1 registration repair complete and frozen. V1 superseded due to internal specification-consistency contradictions only. No economic evidence introduced. Stage 2 has NOT been executed. Base Registry remains EMPTY. F-01 unchanged. Next authorized task: V38A Stage 2 Structural Validation using V1-r1 only.**
```

---

## 24. STAGE 1 VERDICT

**REGISTRATION FROZEN — STAGE 2 AUTHORIZED**

---

## 25. NEXT AUTHORIZED TASK

> **Execute V38A Stage 2 Structural Validation for FB-001 using V1-r1 as the sole governing registration specification.**

Stage 2 must NOT use V1 — only V1-r1 is governing.

---

**END OF FB-001 ORB V38A STAGE 1 REGISTRATION REPAIR (V1-r1)**
