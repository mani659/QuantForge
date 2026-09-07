# QUANTFORGE — RF-001 OWNER SELECTION & PROSPECTIVE FREEZE

**Date:** 2026-09-07
**Status:** OWNER SELECTION FROZEN — SELECTED FOR V38A REGISTRATION
**Purpose:** Record and freeze the owner's selection of RF-001 for eventual V38A Base registration

---

## 1. OWNER SELECTION RECORD

**Selected formulation:** RF-001 — Cross-Market Confirmation Failure Process

**Source mechanism:** REL-M01

**Selection date:** 2026-09-07

**Selection type:** Owner-directed prospective governance choice

**Selection author:** Owner

**Historical economic results used:** NO

**Live FB-001 economics used:** NO

**F-01 economics used:** NO

**Protected-forward economics used:** NO

**Optimization performed:** NO

**Parameter tournament performed:** NO

**Selection was owner-directed:** YES

---

## 2. FROZEN GOVERNANCE CHOICES

| Parameter | Frozen Value | Governing Notation | Source |
|-----------|-------------|-------------------|--------|
| N (lookback horizon) | 30 completed M1 bars | `N = 30` | G1 owner selection |
| M (confirmation window) | 15 completed M1 bars | `M = 15` | G2 owner selection |
| Confirmation market | US500 (S&P 500 proxy) | `confirmation_market = US500` | G3 owner selection |

**Scope frozen:**

| Parameter | Frozen Value |
|-----------|-------------|
| Primary market | USATECHIDXUSD |
| Confirmation market | US500 |
| Timeframe | M1 |
| Session | US regular session (09:30–16:00 ET) |
| N | 30 |
| M | 15 |
| Cost model | 2 bps round-trip |
| Data domain | Forward-only prospective from 2026-09-06 08:00 ET |

**Scope exclusions:**

- US30 substitution: NOT PERMITTED
- Dynamic confirmation-market selection: NOT PERMITTED
- Multi-index confirmation: NOT PERMITTED
- Basket confirmation: NOT PERMITTED
- Cross-session confirmation: NOT PERMITTED

---

## 3. COMPLETE RESULTING DECISION PROCESS

### Context

US equity regular session (09:30–16:00 ET). M1 bars.

### Primary market

`USATECHIDXUSD`

### Confirmation market

`US500`

### Structural event (primary market)

**BULLISH EVENT:** Primary market close exceeds highest high of the prior 30 completed M1 bars.

**BEARISH EVENT:** Primary market close falls below lowest low of the prior 30 completed M1 bars.

Completed bars only. No partial bars.

### Confirmation window

Exactly: `15 completed M1 bars` following the primary event.

### Confirmation

A confirming event is the corresponding directional structural event in US500 within the 15-bar window:

- Bullish primary event → US500 close exceeds highest high of its own prior 30 completed M1 bars within 15 bars.
- Bearish primary event → US500 close falls below lowest low of its own prior 30 completed M1 bars within 15 bars.

### Failure

No confirming event occurs within the registered 15-bar window.

### Decision

**Bullish primary event + failed bullish confirmation:**

`SHORT US500`

**Bearish primary event + failed bearish confirmation:**

`LONG US500`

This mapping is deterministic and explicit:

```
PRIMARY_EVENT DIRECTION → OPPOSITE US500 POSITION
BULLISH PRIMARY + FAILED CONFIRMATION → SHORT US500
BEARISH PRIMARY + FAILED CONFIRMATION → LONG US500
```

### Entry

Entry at the open of bar M+2 after the primary event (bar 17 after event detection).

Temporal causality preserved: all information used for the decision is known before execution.

### Invalidation

If the primary market reverses its structural event — USATECHIDXUSD close returns within the 30-bar range — before the position is entered, the opportunity is cancelled. No position is taken.

No stop-losses. No take-profits. No additional invalidation rules.

### Exit

Exit at the close of the session (16:00 ET). Single-session position.

### Opportunity population

One opportunity per qualifying structural event. Maximum one position at a time. Structural events in the last M=15 bars of the session are excluded (insufficient time for confirmation window and entry). Duplicate structural events (same direction, same session, no intervening reversal) do not create new opportunities — treated as continuation.

### Cost model

2 bps round-trip (1 bps entry + 1 bps exit). Applied mechanically to gross return. No cost optimization.

---

## 4. MECHANISM-PRESERVATION CHECK

| Check | Result |
|-------|--------|
| Original mechanism: Primary USATECHIDXUSD structural event → US500 confirmation window → explicit confirmation failure → decision based on failure | VERIFIED |
| Frozen result preserves this exact mechanism | YES |
| Does N=30 change the mechanism? | NO — N defines the event population, not the mechanism |
| Does M=15 change the mechanism? | NO — M defines the confirmation window, not the mechanism |
| Does US500 change the mechanism? | NO — market identity defines the pair, not the mechanism |
| Is the result still generic lead/lag? | NO — trigger is a discrete confirmation failure event |
| Is the result still generic correlation divergence? | NO — trigger is event detection, not continuous correlation |
| Is the result still pair spread mean reversion? | NO — trigger is failure detection, not spread level |
| Is the result still breakout continuation? | NO — trigger is failure detection, not breakout trading |
| Is the result still momentum? | NO — trigger is cross-market event, not own-history trend |
| Is the result still synchrony regime trading? | NO — trigger is event failure, not regime transition |

**MECHANISM PRESERVED: YES**

---

## 5. DISTINCTNESS CHECK

| Prior work | Distinct? | Reason |
|------------|-----------|--------|
| F-02 (pairs spread) | YES | Confirmation failure, not spread trading |
| F-03 (rank rotation) | YES | Event detection, not ranking |
| Mean reversion | YES | Cross-market failure, not single-asset displacement fading |
| TSMOM | YES | Cross-market, not own-history trend |
| CAND-083 | YES | Cross-market, not single-market rejection accumulation |
| CAND-105 | YES | Failure detection, not lead-lag timing |
| CAND-107 | YES | Event failure, not vol co-movement |
| ORB / Breakout | YES | Failure detection, not breakout trading |
| RF-002 | YES | Confirmation failure, not synchrony regime |
| RF-003 | YES | Confirmation failure, not shock absorption |

**DISTINCTNESS PRESERVED: YES**

---

## 6. OUTCOME-BLIND CERTIFICATION

| Check | Result |
|-------|--------|
| Historical economic results used | NO |
| Live FB-001 economics used | NO |
| F-01 economics used | NO |
| Protected-forward economics used | NO |
| Optimization performed | NO |
| Parameter tournament performed | NO |
| Selection was owner-directed | YES |
| N=30 chosen from historical performance | NO |
| M=15 chosen from historical performance | NO |
| US500 chosen from historical performance | NO |
| Any formulation ranked by expected profitability | NO |

**OUTCOME-BLIND: CERTIFIED**

---

## 7. DEFERRED FORMULATIONS

| Formulation | Status | Action |
|-------------|--------|--------|
| RF-002 — Cross-Market Synchrony Regime Process | DEFERRED | No further work in this task |
| RF-003 — Cross-Market Shock Absorption Asymmetry Process | DEFERRED | No further work in this task |

RF-002 and RF-003 are NOT rejected. They remain available for future owner selection.

---

## 8. V38A BOUNDARY

The result of this task is:

`SELECTED FOR V38A REGISTRATION`

It is NOT:

- `BASE`
- `VALIDATED`
- `BASE-ELIGIBLE`
- `QUALIFIED`

Base Registry: **UNCHANGED — EMPTY**

The next authorized task is: **V38A Stage 1 Registration for RF-001**

---

## 9. PROSPECTIVE FREEZE STATEMENT

This formulation is frozen as of 2026-09-07.

Any future correction requires a new governed revision.

The frozen formulation consists of:

1. RF-001 Cross-Market Confirmation Failure Process (source mechanism REL-M01)
2. N = 30 completed M1 bars
3. M = 15 completed M1 bars
4. Confirmation market = US500
5. Decision: bullish primary + failed confirmation → SHORT US500; bearish primary + failed confirmation → LONG US500
6. Entry: open of bar M+2 (bar 17)
7. Exit: session close (16:00 ET)
8. Invalidation: primary reverses before entry
9. Cost: 2 bps round-trip
10. Session: US regular session (09:30–16:00 ET)

No parameter may be changed without a new governed revision.

No additional filters, regimes, conditions, or Conditional layers may be introduced without a new governed decision.

---

**END OF OWNER SELECTION FREEZE**
