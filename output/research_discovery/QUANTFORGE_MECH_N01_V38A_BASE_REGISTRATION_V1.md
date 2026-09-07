# QUANTFORGE — MECH-N01 V38A BASE REGISTRATION V1

**Date:** 2026-09-07
**Status:** V38A BASE REGISTRATION COMPLETE — MECH-N01 REGISTERED — STAGE 2 AUTHORIZED
**Milestone:** V38A Base Registration and Parameter Freeze for MECH-N01 (Structural Level Validation Flow)
**Parent doctrine:** V38A (BV1–BV13), BS1–BS13, BF1–BF13
**Selection artifact:** `QUANTFORGE_MECH_N01_OWNER_SELECTION_FREEZE_V1.md` (SHA `1bab8a0c`)
**Formulation artifact:** `QUANTFORGE_MECH_N01_OUTCOME_BLIND_FORMULATION_V1.md` (SHA `0a82d181`)

---

## 1. REGISTRATION SCOPE

This document registers MECH-N01 (Structural Level Validation Flow) as a formal V38A Base Registration. It freezes all governance-selectable parameters, resolves all remaining ambiguities, and creates the canonical Base definition. This is a governance and registration task. It does NOT execute Stage 2, Stage 3, economic validation, backtesting, optimization, or any performance assessment.

---

## 2. AUTHORITATIVE SOURCES

| Source | Artifact | Role |
|--------|----------|------|
| V38 Doctrine | `QUANTFORGE_V38_DOCTRINE_RATIFICATION_V1.md` | Hybrid Base + Conditional; D1–D25 |
| V38A Validation Pathway | `QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_RATIFICATION_V1.md` | BV1–BV13; six-stage lifecycle |
| Base Hypothesis Selection | `QUANTFORGE_BASE_HYPOTHESIS_SELECTION_VALIDATION_RATIFICATION_V1.md` | BS1–BS13; selection clauses |
| Outcome-Blind Formulation | `QUANTFORGE_OUTCOME_BLIND_BASE_DECISION_PROCESS_FORMULATION_RATIFICATION_V1.md` | BF1–BF13; formulation clauses |
| MECH-N01 Owner Selection Freeze | `QUANTFORGE_MECH_N01_OWNER_SELECTION_FREEZE_V1.md` | Owner selection |
| MECH-N01 Outcome-Blind Formulation | `QUANTFORGE_MECH_N01_OUTCOME_BLIND_FORMULATION_V1.md` | Formulation architecture |
| SESSION_HANDOFF | `docs/SESSION_HANDOFF.md` | Current governed state |

---

## 3. OWNER-SELECTED MECHANISM

| Field | Value |
|-------|-------|
| Mechanism ID | MECH-N01 |
| Mechanism name | Structural Level Validation Flow |
| Mechanism hypothesis | A structural price break becomes economically informative when subsequent price behavior demonstrates that the break is accepted/validated rather than immediately rejected; this validation reflects a change in participant behavior and may produce directional flow. |
| Unit of analysis | Single market (USATECHIDXUSD) |
| Selected by | Owner, per BS11 |
| Selection date | 2026-09-07 |

---

## 4. FINAL DECISION ARCHITECTURE

The registered architecture is **Architecture A — Minimal**, the simplest formulation that preserves the MECH-N01 mechanism with maximum determinism and minimum parameter burden.

Core process:
1. Compute rolling N-bar highest high and lowest low
2. Detect breakout (close beyond level)
3. Freeze breakout reference level
4. Observe K consecutive closes beyond frozen level (validation)
5. Enter at open of bar after validation
6. Exit at session close (23:59 UTC daily)
7. Direction: follow validated break (LONG bullish, SHORT bearish)
8. Rejection during K-bar window: no trade

---

## 5. FROZEN N — STRUCTURAL LOOKBACK

**Frozen value:** `N = 60 completed M1 bars`

### Governance assessment

| Question | Answer |
|----------|--------|
| What does N control? | The number of completed M1 bars used to compute the highest high (bullish level) or lowest low (bearish level) |
| Why is a value required? | The mechanism requires "a lookback period" to define what constitutes a structural level |
| Is the value implied by the mechanism? | No. The mechanism requires "a lookback period" but does not specify the exact value |
| Could another value represent the same mechanism? | Yes. N=30, N=90, N=120 would all represent the same mechanism with different structural granularity |
| Would selecting among alternatives normally require empirical performance evidence? | Yes. Normally you would test different N values to see which produces better outcomes |
| Can the owner legitimately freeze the value prospectively? | **YES** — N=60 is justified by design reasoning: 60 M1 bars = 1 hour of market data. This is a clean, round number representing one complete hour of price history. It is long enough to capture a meaningful structural range and short enough to reflect recent price action. The value is mechanism-consistent (the mechanism requires "a lookback period"; one hour is a defensible structural period for intraday breakouts). |

**Decision:** N = 60 is frozen as a governance-selectable parameter justified by mechanism-consistent design reasoning.

---

## 6. FROZEN K — VALIDATION PERSISTENCE

**Frozen value:** `K = 5 completed M1 closes`

### Governance assessment

| Question | Answer |
|----------|--------|
| What does K control? | The number of consecutive M1 bar closes that must remain beyond the structural level after a breakout for validation to occur |
| Why is a value required? | The mechanism requires "a hold period" to distinguish acceptance from noise |
| Is the value implied by the mechanism? | No. The mechanism requires "a hold period" but does not specify the exact value |
| Could another value represent the same mechanism? | Yes. K=3, K=10, K=15 would all represent the same mechanism with different validation strictness |
| Would selecting among alternatives normally require empirical performance evidence? | Yes. Normally you would test different K values to see which produces better outcomes |
| Can the owner legitimately freeze the value prospectively? | **YES** — K=5 is justified by design reasoning: 5 M1 bars = 5 minutes of post-break persistence. This is long enough to distinguish genuine acceptance from noise (a single bar closing beyond the level could be random) and short enough to be tradeable (the validation completes within minutes, allowing same-session entry and exit). The value is mechanism-consistent (the mechanism requires "a hold period"; 5 minutes is a defensible minimum for participant-behavior transition). |

**Decision:** K = 5 is frozen as a governance-selectable parameter justified by mechanism-consistent design reasoning.

---

## 7. SESSION SCOPE

**Frozen value:** `All eligible trading sessions — no session filter`

### Governance assessment

| Question | Answer |
|----------|--------|
| What does session scope control? | Whether structural levels, breakouts, validation, entry, and exit are restricted to specific trading hours |
| Does the mechanism require a specific session? | No. The mechanism operates whenever structural levels exist and breakouts occur |
| Is a session filter mechanism-consistent? | Not inherently. The participant-behavior transition can occur at any time structural levels are broken and validated |
| Would adding a session filter require empirical evidence? | Yes. Selecting a specific session (e.g., US regular hours) based on historical performance would be outcome-driven |
| Can the owner freeze "no filter" prospectively? | **YES** — "No session filter" is the mechanism-consistent choice. The mechanism does not specify session restrictions. Adding restrictions would add complexity without mechanism necessity. |

**Decision:** All eligible trading sessions are included. No session filter is applied.

---

## 8. ENTRY DELAY DECISION

**Frozen value:** `No max entry delay — immediate entry at next bar open`

### Governance assessment

| Question | Answer |
|----------|--------|
| What does max entry delay control? | The maximum number of bars after validation before entry is abandoned |
| Is it necessary to the mechanism? | **No.** The formulation specifies entry at "open of bar E+K+1," which defines a unique immediate entry point |
| Does adding a delay introduce unnecessary degrees of freedom? | **Yes.** A 3-bar delay window creates a second execution pathway (enter at E+K+1, E+K+2, or E+K+3) that is inconsistent with the minimal architecture |
| Can the owner remove it prospectively? | **YES** — The mechanism requires entry after validation. The simplest deterministic entry is "next bar open." No delay is needed. |

**Decision:** Max entry delay is REMOVED from the Base. Entry occurs at the open of bar E+K+1. If that bar's open is unavailable, entry is skipped (the opportunity is abandoned). This preserves the minimal architecture.

---

## 9. SESSION EXIT DEFINITION

The formulation identified "session definition for exit timing" as the remaining ambiguity. This is resolved below.

**Frozen session definition:**

| Element | Value |
|---------|-------|
| Session timezone | UTC |
| Session opening | 00:00 UTC (start of trading day) |
| Session closing | 23:59 UTC (end of trading day) |
| Authoritative calendar | The instrument's own trading schedule (USATECHIDXUSD trades nearly 24 hours; the session is defined as the full UTC trading day) |
| Exit timing | Close of the final completed M1 bar before 23:59 UTC |
| Holiday treatment | If the instrument does not trade on a calendar day, no session exists and no trades are taken |
| Early close treatment | If the instrument closes early (e.g., holiday early close), exit occurs at the final completed M1 bar before actual market close |
| Daylight-saving treatment | Not applicable — UTC has no daylight-saving transitions |
| Missing final bars | If the final bar of the session is missing from data, exit uses the last available bar's close |

### Rationale

USATECHIDXUSD trades nearly 24 hours on Exness. The most deterministic, reproducible session definition is the UTC trading day (00:00–23:59 UTC). This avoids broker-specific session times, exchange-hours dependencies, and daylight-saving complexity. The exit occurs at the close of the final completed M1 bar of the UTC day, which is a deterministic, reproducible timestamp.

---

## 10. STRUCTURAL LEVEL SEMANTICS

All semantics frozen below are deterministic and reproducible without hindsight.

| Semantic | Frozen value |
|----------|-------------|
| Current forming bar excluded from lookback | **YES** — only completed bars are used |
| Exact lookback bars | N=60 completed M1 bars immediately preceding the current bar |
| Highest high definition | `max(high[i]) for i in [1..N]` where i=1 is the most recent completed bar |
| Lowest low definition | `min(low[i]) for i in [1..N]` where i=1 is the most recent completed bar |
| Equality handling (breakout) | **Strict inequality required.** Close must be strictly above (bullish) or strictly below (bearish) the level. Close exactly at the level = no breakout. |
| Multiple simultaneous levels | At each bar, one bullish level (N-bar high) and one bearish level (N-bar low) exist. Only one can be broken at a time (price cannot be both above highest high and below lowest low). |
| Level immutability once event begins | **FROZEN at breakout.** Once bar E closes beyond the level, the breakout reference level is frozen. The rolling level may continue to update, but validation uses the frozen level. |
| New level generation after prior event | After a breakout (whether validated or rejected), the rolling N-bar high/low continues to update. A new structural level forms naturally as the lookback window rolls forward. |
| Event retriggering | A new breakout of the same frozen level (after price returns and breaks again) is a new independent event. |
| Overlapping breakout handling | Each breakout is independent. If two breakouts occur from different structural levels, both are tracked separately through their own K-bar validation windows. |

---

## 11. BREAKOUT SEMANTICS

| Semantic | Frozen value |
|----------|-------------|
| Breakout bar identification | Bar E is the first completed bar whose close is strictly beyond the structural level |
| Close confirmation required | **YES** — only the close is evaluated; wicks beyond the level do not count |
| Intra-bar information used | **NO** — only completed-bar information |
| Decision timestamp | Close of bar E |
| Breakout equality | Close must be strictly beyond the level. Close exactly at the level = no breakout. |

---

## 12. VALIDATION SEMANTICS

| Semantic | Frozen value |
|----------|-------------|
| Breakout bar counts as validation close #1 | **NO** — bar E is the breakout bar. Validation closes are E+1 through E+K. |
| K consecutive closes meaning | Each of the K bars (E+1 through E+K) must have a close strictly beyond the frozen structural level |
| Strict beyond requirement | **YES** — close must be strictly above (bullish) or strictly below (bearish) the frozen level |
| Level movement during validation | The frozen level does NOT move. Validation uses the level frozen at bar E. |
| Rejection during K-bar window | If any bar among E+1 through E+K has a close that returns through (or exactly to) the frozen level, validation fails. The breakout is rejected. No trade. |
| Validation restart after failure | **NO** — a rejected breakout does not restart. A new breakout requires a new bar closing beyond the level. |
| New structural event during validation | A new breakout of a different structural level can begin during an existing validation window. The two events are independent. |
| Overlapping validation sequences | **PERMITTED.** Two independent breakouts from different structural levels may have overlapping validation windows. Each is tracked independently. |

---

## 13. DIRECTION SEMANTICS

| Semantic | Frozen value |
|----------|-------------|
| Upside | Validated upside break → **LONG** |
| Downside | Validated downside break → **SHORT** |
| Simultaneous upside/downside breaks | **IMPOSSIBLE.** Price cannot be above the N-bar highest high and below the N-bar lowest low simultaneously. |
| Tie behavior | Close exactly at level = rejection = no trade |
| Ambiguous cases | Close exactly at level = rejection = no trade. No ambiguity exists: the close is either strictly beyond the level (acceptance) or not (rejection). |
| Direction reversal without separate event | **NOT PERMITTED.** The Base does not reverse direction. An active trade exits at session close. A new trade requires a new structural event. |

---

## 14. OPPORTUNITY POPULATION

The frozen Base opportunity universe:

| Element | Frozen value |
|---------|-------------|
| Instruments | USATECHIDXUSD (USTECm on Exness) — single instrument |
| Timeframe | M1 (one-minute bars) |
| Market calendar | The instrument's own trading schedule |
| Sessions | All eligible trading sessions (no filter) |
| Structural level eligibility | Any rolling N-bar high or low. No minimum distance, no minimum age, no significance threshold beyond the N-bar lookback. |
| Overlapping levels | Each level tracked independently. A breakout of one level does not disqualify a breakout of another. |
| Repeated break behavior | Each break is an independent event. If price breaks, validates, returns, and breaks again, the second break is a new event. |
| First validated break only | **NO.** Multiple validated breaks from the same level are permitted as independent events. |
| New level overlapping active opportunity | **PERMITTED.** A new structural level can form during an active validation window or active trade. The new level is relevant only for future breakouts. |
| Multiple simultaneous positions | **PERMITTED.** Independent breakouts may produce concurrent trades. |
| Same structural level producing multiple trades | **YES.** Each break of the same level is an independent event. |

---

## 15. ENTRY SEMANTICS

| Semantic | Frozen value |
|----------|-------------|
| Validation completion timestamp | Close of bar E+K |
| Exact entry bar | Open of bar E+K+1 |
| Exact entry price convention | The open price of bar E+K+1 |
| Order type concept | Market order at next bar open |
| Gap treatment | If bar E+K+1 gaps significantly, entry still occurs at the open. No gap filter. |
| Missing bar treatment | If bar E+K+1 is missing, entry is skipped. The opportunity is abandoned. |
| Execution failure treatment | If entry cannot be executed, the opportunity is abandoned. |
| Max entry delay | **NONE.** Entry must occur at the open of bar E+K+1. If unavailable, the opportunity is abandoned. |

---

## 16. EXIT / SESSION SEMANTICS

| Semantic | Frozen value |
|----------|-------------|
| Exit type | Session close (time-based) |
| Exit timing | Close of the final completed M1 bar before 23:59 UTC |
| Exit price | The close of the final M1 bar of the UTC trading day |
| Profit target | **NONE** |
| Trailing stop | **NONE** |
| Profit-taking | **NONE** |
| Discretionary exit | **NONE** |
| Alternative holding period | **NONE** |
| Early close treatment | Exit at the final completed M1 bar before actual market close |
| Holiday treatment | No session = no trades |

---

## 17. RISK / INVALIDATION SEMANTICS

| Semantic | Frozen value |
|----------|-------------|
| Pre-entry invalidation | Breakout rejected during K-bar window = no trade |
| Post-entry stop-loss | **NONE** — the trade exits at session close |
| Structural invalidation post-entry | **NONE** — the structural level is used for breakout detection and validation only |
| Timing invalidation | **NONE** — no time-based stop within the session |
| Maximum-risk boundary | The full adverse move from entry to session close. No predefined stop. |
| Rationale | The minimal formulation does not define an arbitrary stop. The mechanism does not hypothesize a specific invalidation point after entry. The session-close exit is the complete exit architecture. |

---

## 18. EXECUTION MODEL

| Element | Frozen value |
|---------|-------------|
| Market / asset type | CFD on US equity index (USATECHIDXUSD / USTECm on Exness) |
| Price source | M1 OHLCV bars from the MT5 terminal |
| Bar completion semantics | Each M1 bar is complete at its close timestamp. All evaluation occurs on completed bars. |
| Entry timing | Open of bar E+K+1 |
| Exit timing | Close of final M1 bar before 23:59 UTC |
| Spread / cost treatment | Acknowledged but not modeled. A frozen cost model will be applied during V38A Stage 3. |
| Missing observations during validation | Treated as rejection (conservative) |
| Missing observations at entry | Skip to next available bar's open; if unavailable, abandon |
| Missing observations at exit | Use last available bar's close |
| Duplicate observations | Remove duplicates; use first occurrence |
| Market closure during validation | Validation paused; resumes when market reopens |
| Market closure during active trade | Exit at last available price before closure |
| Execution failure | Abandon (entry) or mark at last available price (exit) |

---

## 19. OUTCOME DEFINITION

| Element | Frozen value |
|---------|-------------|
| Trade outcome (LONG) | `exit_price - entry_price` |
| Trade outcome (SHORT) | `entry_price - exit_price` |
| Measurement horizon | From entry (open of bar E+K+1) to exit (close of final M1 bar before 23:59 UTC) |
| Gross outcome | Raw price difference without cost adjustment |
| Cost-adjusted outcome | `gross_outcome - round_trip_cost` (frozen cost model applied during V38A Stage 3) |
| Opportunity accounting | Each validated breakout = at most one trade. Rejected breakouts = zero trades. |
| Missing data at entry | Opportunity not counted as a trade |
| Missing data during trade | Outcome interpolated from available bars |
| Missing data at exit | Outcome uses last available price |
| Event independence | Each trade is independent. Concurrent trades from independent breakouts are treated as independent events. |

---

## 20. PARAMETER CLASSIFICATION

| Parameter | Classification | Frozen value | Justification |
|-----------|---------------|-------------|---------------|
| N (lookback period) | GOVERNANCE-SELECTABLE — FROZEN | 60 M1 bars | Mechanism-consistent design reasoning: 1 hour of price history |
| K (validation hold period) | GOVERNANCE-SELECTABLE — FROZEN | 5 M1 bars | Mechanism-consistent design reasoning: 5 minutes of post-break persistence |
| Session scope | GOVERNANCE-SELECTABLE — FROZEN | All sessions (no filter) | Mechanism does not require session restrictions |
| Session exit time | GOVERNANCE-SELECTABLE — FROZEN | 23:59 UTC daily | Deterministic, reproducible, no daylight-saving complexity |
| Max entry delay | REMOVED | None | Inconsistent with minimal architecture; immediate entry at next bar open |
| Stop-loss | NOT INCLUDED | None | Mechanism does not hypothesize post-entry invalidation; session-close exit is complete |
| Cost model | FROZEN AT V38A STAGE 3 | TBD | Not a formulation parameter; frozen during economic validation |

**Empirically tunable parameters: NONE.**

---

## 21. DETERMINISM AUDIT

### 21.1 Can two independent competent researchers implement this Base from this registration artifact and produce the same opportunity population and decisions?

**YES.** The registration artifact specifies every decision point with complete determinism. No parameter requires empirical selection. No ambiguity requires historical data to resolve.

### 21.2 Audit checklist

| Item | Status | Resolution |
|------|--------|-----------|
| Hidden parameters | NONE | All parameters explicitly classified and frozen |
| Hidden defaults | NONE | All values explicitly stated |
| Ambiguous timestamps | RESOLVED | Entry at open of E+K+1, exit at close of final bar before 23:59 UTC |
| Timezone ambiguity | RESOLVED | UTC throughout |
| Session ambiguity | RESOLVED | Full UTC trading day (00:00–23:59) |
| Level ambiguity | RESOLVED | Rolling N-bar high/low, strict inequality |
| Equality ambiguity | RESOLVED | Close exactly at level = rejection = no breakout = no trade |
| Validation ambiguity | RESOLVED | K consecutive closes strictly beyond frozen level; all-or-nothing |
| Overlapping events | RESOLVED | Each breakout independent; concurrent trades permitted |
| Repeated signals | RESOLVED | Each break of same level is independent event |
| Execution ambiguity | RESOLVED | Entry at next bar open; exit at session close |
| Missing-data ambiguity | RESOLVED | Conservative treatment defined for all scenarios |
| Daylight-saving ambiguity | RESOLVED | UTC has no daylight-saving transitions |
| Holiday/early-close ambiguity | RESOLVED | No session = no trades; early close = exit at last available bar |

---

## 22. REGISTRATION ELIGIBILITY

| Requirement | Status |
|-------------|--------|
| BS1 — Object-type requirement | PASS — complete deterministic decision process |
| BS2 — Selection provenance | PASS — provenance recorded in selection artifact |
| BS3 — Closed-line firewall | PASS — no closed artifact imported |
| BS4 — Historical-result separation | PASS — no historical results used |
| BS5 — Research-priority vs. eligibility separation | PASS — selection based on priority criteria only |
| BS6 — Prospective selection freeze | PASS — mechanism identity frozen |
| BS7 — Selection data boundary | PASS — no sealed figures inspected |
| BS8 — Family redundancy control | PASS — architecturally distinct from all prior mechanisms |
| BS9 — Conditional independence | PASS — no future Conditional required |
| BS10 — Parallel-candidate protection | PASS — MECH-N01 selected; MECH-N02/N03 deferred |
| BS11 — Owner selection authority | PASS — owner authorization recorded |
| BS12 — Base-hypothesis / Base separation | PASS — labeled BASE HYPOTHESIS until Registry entry |
| BS13 — Anti-rescue selection protection | PASS — no rescue framing |
| BF1–BF13 compliance | PASS — all formulation clauses satisfied |
| BV1–BV13 compliance | PASS — registration satisfies Base Validation requirements |
| Complete decision process | PASS — all 11 questions answered deterministically |
| No empirically tunable parameters | PASS — zero empirical parameters |
| Determinism audit | PASS — two researchers would produce identical implementations |

---

## 23. BASE ID

**Base ID:** `BASE-001`

The current Base Registry is confirmed EMPTY before this registration. No existing Base IDs conflict.

---

## 24. REGISTRY STATUS

**Before registration:** Base Registry is EMPTY.

**After registration:** Base Registry contains BASE-001 (MECH-N01 — Structural Level Validation Flow).

The Base is **REGISTERED**, not validated. Registration creates a governed object in the Registry. It does not confer Base status in the sense of "validated" or "profitable." Base status in that sense exists only after V38A Stage 4 adjudication and owner-approved Registry entry confirming BASE-ELIGIBLE.

Note: The current V38A lifecycle defines registration as the creation of a governed object with frozen parameters. The term "Base" in the Registry refers to a registered deterministic decision process, not a validated trading system.

---

## 25. NEXT AUTHORIZED STAGE

Successful registration authorizes the next governed lifecycle stage:

**V38A Stage 2 — Structural Validation**

Stage 2 must occur as a separate task. It will verify that the registered decision process is structurally complete, deterministic, and free of leakage. Stage 2 does NOT perform economic validation.

---

## 26. GOVERNANCE CHECKLIST

| Check | Result |
|-------|--------|
| MECH-N01 owner selection unchanged | PASS |
| Outcome-blind formulation preserved | PASS |
| No historical performance used | PASS — no backtests, no returns, no expectancy, no Sharpe, no win rate |
| No parameter optimization | PASS — N and K frozen by governance reasoning, not optimization |
| No parameter sweep | PASS |
| No economic validation | PASS |
| No Stage 2 | PASS — Stage 2 is a separate task |
| No Stage 3 | PASS |
| No protected-forward inspection | PASS — CAND-015/024/035 not inspected |
| No closed-line reopening | PASS |
| RF-001 unchanged | PASS |
| F-01 unchanged | PASS |
| FB-001 unchanged | PASS |
| Runner uninterrupted | PASS |
| No broker orders | PASS |
| No unrelated source/test changes | PASS |
| No production-code changes | PASS |
| Base Registry was EMPTY before registration | PASS |

---

## 27. FINAL VERDICT

**V38A BASE REGISTRATION COMPLETE — MECH-N01 REGISTERED — STAGE 2 AUTHORIZED**

BASE-001 (Structural Level Validation Flow) is registered with frozen parameters:
- N = 60 M1 bars (structural lookback)
- K = 5 M1 bars (validation hold period)
- Session: all eligible trading sessions (no filter)
- Session exit: 23:59 UTC daily
- Entry: open of bar after validation (no delay)
- Exit: session close (no stop, no target)
- Direction: follow validated break

Base Registry now contains BASE-001. The Base is registered, not validated. Stage 2 (Structural Validation) is authorized as the next governed step.

---

**Registration record SHA256:** `6318e215296cac235f872135eb2997f2a10e1cb9d3334130fa979c0ccae6bbe2`

---

**END OF MECH-N01 V38A BASE REGISTRATION V1**
