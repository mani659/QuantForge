# QUANTFORGE — RESEARCH FACTORY V2
# TRADEABLE EDGE DISCOVERY SCREENING — V24
# DATE: 2026-08-29

## 1. G0 Status

V24 G0 — CANDIDATE GENERATION ONLY. No G1, G2, or experiment execution.

## 2. Research Objective

Discover 3–5 genuinely independent mechanism candidates from materially different economic families. V24 must NOT be another collection of small variations of sweep/freshness/acceptance/session-anchor patterns. The dual-path architecture (standalone Alpha vs. modular system) influences selection: candidates may be standalone Alphas, State/Condition artifacts, Event Opportunists, or regime specialists.

---

## 3. Candidates

---

### CAND-G0-071

### Candidate ID
CAND-071

### Name
Cross-Market Overnight Information Transmission — Gold Lead to Tech Repricing

### Artifact Type
ALPHA/EVENT

### Mechanism Family
Cross-Market Transmission / Information Arrival

### Hypothesis
A large directional move in Gold (XAUUSD) during the Asian session (18:00–03:00 ET) transmits to the US Technology Index (USATECHIDXUSD) during the New York open, creating a directional repricing edge. The causal mechanism is shared macro exposure: Gold and Tech are both sensitive to real-rate expectations and risk sentiment. When Gold reprices overnight while US equity markets are closed, the information must be incorporated into Tech when US participants arrive. The first 30 minutes of NY trading contain the repricing.

### Economic Constraint
Gold and Tech share macro-factor exposure (real rates, USD strength, risk sentiment). A >0.5% overnight Gold move represents significant repricing that US participants have not yet absorbed. The forced repricing at the NY open creates a directional opportunity before the information is fully priced.

### Market Participant Constraint
Institutional macro desks, CTAs, and risk-parity allocators rebalance across both Gold and Tech simultaneously. When Gold moves overnight, these participants must adjust Tech exposure at the open. This forced flow creates directional pressure.

### Observable Variables
- XAUUSD 18:00–03:00 ET session return (absolute)
- XAUUSD session direction (up/down)
- USATECHIDXUSD first 30-minute return (09:30–10:00 ET)
- Direction of Tech repricing relative to Gold direction

### Exact Setup
1. XAUUSD 18:00–03:00 ET session absolute return > 0.5%
2. Direction: bullish (positive return) or bearish (negative return)

### Exact Confirmation
The Gold session return is fully known at 03:00 ET (session close). No real-time data needed after 03:00.

### Exact Entry
Market order on USATECHIDXUSD at 09:30:00 ET (NY open), in the same direction as the Gold overnight move.

### Exact Exit
Market order closing the position at 10:00:00 ET (30-minute holding window).

### Direction
Same direction as XAUUSD overnight move (Gold up → Long Tech; Gold down → Short Tech).

### Re-arm Rule
Maximum one event per calendar day. Re-arms at next 18:00 ET.

### Expected Frequency Class
Low to Moderate (~20–40 qualifying events per year, based on ~0.5% Gold overnight moves occurring roughly 1–2x per week).

### Rare-Event Suitability
Moderate. If per-event economics exceed 10 bps, the frequency is sufficient for standalone viability.

### Economic Headroom Rationale
A 0.5% Gold move represents a meaningful macro repricing. The forced institutional rebalancing at the NY open should produce at least 10–30 bps of directional Tech movement before the information is fully absorbed. This comfortably exceeds the 2 bps friction threshold.

### Counterfactual
The identical >0.5% Gold overnight move, but USATECHIDXUSD entry at 12:00 ET (mid-day, when the repricing has already occurred).

### Why Counterfactual Is Discriminating
The counterfactual isolates the timing of the information arrival. If the edge exists at the open but disappears by mid-day, it confirms that the opportunity is specifically the forced repricing window. If mid-day entries work equally well, the hypothesis fails.

### Data Availability
XAUUSD M1 and USATECHIDXUSD M1 are both available in the repository. No external data required.

### Causal Observability
Fully observable. Gold overnight return is known by 03:00 ET. Tech entry at 09:30 is deterministic. Exit at 10:00 is deterministic.

### Prior-Art Classification
NEW. Cross-market lead-lag between Gold and Tech has not been tested in any prior V1–V23 cycle. Prior work has been exclusively single-market.

### Closed-Line Check
No overlap with any closed line (DISC-021 through DISC-026, or closed V-candidates). No disguised rescue.

### Standalone Potential
MODERATE to STRONG. If per-event economics exceed 10 bps, the frequency is viable for a standalone specialist module.

### Component Potential
STRONG. Even if standalone expectancy is marginal, the cross-market signal could serve as a directional filter for other Tech-based modules.

### State-Artifact Potential
LOW. This is an Alpha/Event, not a state.

### Regime-Specialist Potential
MODERATE. The mechanism may be stronger during high-volatility macro regimes (FOMC, NFP eves) and weaker during quiet periods.

### Information-Sharing Potential
Could share Gold-momentum state with Tech-reversal modules. If Gold is trending strongly overnight, Tech modules should be biased in the same direction.

### Expected Failure Mode
The Gold→Tech transmission may be too fast (priced in before 09:30) or too noisy (Gold and Tech decorrelated during certain regimes). The counterfactual (mid-day entry) is designed to detect both failure modes.

### G1 Test Design
G1 will measure the 30-minute post-open return on USATECHIDXUSD when XAUUSD overnight return exceeds 0.5%, compared to the mid-day counterfactual. The executable capture contract: entry at 09:30 open, exit at 10:00 open, direction aligned with Gold.

---

### CAND-G0-072

### Candidate ID
CAND-072

### Name
Weekly Range Compression Monday Breakout

### Artifact Type
ALPHA/EVENT

### Mechanism Family
Calendar / Weekly Structure Mechanics

### Hypothesis
When Friday's trading range (High − Low) is in the bottom 20% of the rolling 4-week Friday ranges, Monday's first directional expansion (>0.3% from Monday open) produces a high-probability continuation trade. The mechanism is inventory-driven: compressed Friday ranges indicate participants deferred positioning decisions to the weekend. The resulting inventory imbalance creates forced Monday execution.

### Economic Constraint
Friday range compression means participants did NOT establish full weekend positioning. When new information arrives over the weekend (or participants simply resume normal activity), the forced Monday rebalancing creates a directional surge. The compression stores "kinetic energy" that releases on Monday.

### Market Participant Constraint
Portfolio managers and risk controllers who failed to rebalance on Friday must execute on Monday morning. This forced flow creates directional pressure proportional to the degree of Friday compression.

### Observable Variables
- Friday USATECHIDXUSD range (High − Low)
- Rolling 4-week Friday range percentile
- Monday open price
- First directional expansion magnitude

### Exact Setup
1. Friday USATECHIDXUSD range (High − Low) is in the bottom 20% of rolling 4-week Friday ranges
2. Monday opens and the first 30-minute bar (09:30–10:00) produces a directional return > 0.3% from the Monday open

### Exact Confirmation
Friday range is known at Friday 16:00 ET close. Monday open is known at 09:30 ET. The first 30-minute return is known at 10:00 ET.

### Exact Entry
Market order on USATECHIDXUSD at 10:00:00 ET, in the direction of the first 30-minute Monday expansion.

### Exact Exit
Market order closing the position at 15:45:00 ET (before MOC flows).

### Direction
Same direction as the first 30-minute Monday expansion.

### Re-arm Rule
Maximum one event per week. Re-arms on next Friday.

### Expected Frequency Class
Low (~15–25 qualifying events per year, based on ~20% of Fridays being compressed and ~50% of those producing a >0.3% Monday expansion).

### Rare-Event Suitability
Moderate. If per-event economics exceed 15 bps, the weekly frequency is viable for a standalone specialist.

### Economic Headroom Rationale
Compressed ranges create genuine inventory imbalances. The forced Monday rebalancing should produce 15–50 bps of directional movement. This significantly exceeds friction.

### Counterfactual
The identical Monday first-30-minute >0.3% expansion, but when Friday's range was in the top 50% of rolling 4-week ranges (expanded Friday, normal inventory).

### Why Counterfactual Is Discriminating
The counterfactual isolates the inventory-imbalance mechanism. If compressed Fridays produce larger Monday moves than expanded Fridays, the inventory hypothesis is supported. If they perform identically, the compression adds no information.

### Data Availability
USATECHIDXUSD M1 data is available. Friday ranges and Monday opens are fully derivable.

### Causal Observability
Fully observable. Friday range is known at close. Monday entry is deterministic.

### Prior-Art Classification
NEW. Weekly range compression has not been tested as a Monday breakout trigger in any prior V1–V23 cycle. CAND-063 tested Asian session compression as a state filter for breakouts, but this is a distinct mechanism (weekly calendar structure vs. intraday volatility state).

### Closed-Line Check
No overlap with CAND-063 (Asian compression is a volatility state; this is a calendar inventory mechanism). No closed-line rescue.

### Standalone Potential
MODERATE. Low frequency but potentially high per-event economics.

### Component Potential
STRONG. Could serve as a weekly regime signal for other modules (e.g., "compressed Friday = prepare for Monday breakout").

### State-Artifact Potential
MODERATE. The Friday compression state itself could be a valuable module filter, even if the Alpha entry is marginal.

### Regime-Specialist Potential
STRONG. Specifically designed for the Monday open regime.

### Information-Sharing Potential
Friday compression state could be shared with trend-following modules to adjust Monday position sizing.

### Expected Failure Mode
The mechanism may be too rare (insufficient N for G1), or the Monday expansion may not reliably follow from Friday compression. The counterfactual directly tests this.

### G1 Test Design
G1 will measure the post-entry return of Monday breakout trades when Friday range was compressed vs. expanded. Entry at 10:00, exit at 15:45, direction from first 30-minute expansion.

---

### CAND-G0-073

### Candidate ID
CAND-073

### Name
Mid-Day Reversal Continuation

### Artifact Type
ALPHA/EVENT

### Mechanism Family
Session Microstructure / Participant Transition

### Hypothesis
A sharp directional reversal (>0.4%) occurring strictly between 12:00 ET and 12:30 ET (the lunch-session transition), followed by a 15-minute continuation in the reversal direction, produces a high-probability continuation trade for the next 60 minutes. The mechanism is participant-driven: the 12:00–12:30 window marks the transition from morning institutional flow to afternoon execution. Reversals during this window represent genuine position reorientation by large participants, not noise.

### Economic Constraint
The lunch session is when institutional traders reassess morning positions and prepare afternoon execution. A sharp reversal during this window signals a genuine change in institutional conviction. The 15-minute continuation confirms that the reorientation is sustained, not a momentary blip.

### Market Participant Constraint
Institutional portfolio managers and execution desks reposition during the lull. A sharp reversal signals that a significant participant is actively rotating. The 15-minute confirmation ensures the repositioning is genuine.

### Observable Variables
- 12:00–12:30 ET directional return (absolute)
- 12:30–12:45 ET continuation (confirming the reversal direction)
- Post-12:45 continuation for 60 minutes

### Exact Setup
1. USATECHIDXUSD 12:00–12:30 ET return > 0.4% in one direction (the reversal)
2. 12:30–12:45 ET continues in the same direction (confirmation)

### Exact Confirmation
The reversal is known at 12:30 ET. The 15-minute confirmation is known at 12:45 ET.

### Exact Entry
Market order on USATECHIDXUSD at 12:45:00 ET, in the direction of the reversal.

### Exact Exit
Market order closing the position at 13:45:00 ET (60-minute holding window).

### Direction
Same direction as the 12:00–12:30 reversal.

### Re-arm Rule
Maximum one event per day. Re-arms next trading day.

### Expected Frequency Class
Moderate (~30–50 qualifying events per year, based on ~0.4% reversals occurring in the lunch window on roughly 15–20% of trading days, with ~60% producing 15-minute confirmation).

### Rare-Event Suitability
Not a rare event. Moderate frequency suitable for standalone or module use.

### Economic Headroom Rationale
Institutional repositioning during the lunch transition should produce 15–40 bps of sustained directional movement. The 15-minute confirmation filter removes noise reversals. This comfortably exceeds friction.

### Counterfactual
The identical >0.4% directional move occurring between 10:30 ET and 11:00 ET (mid-morning), with 15-minute continuation, entered at 11:15 ET and exited at 12:15 ET.

### Why Counterfactual Is Discriminating
The counterfactual isolates the session-transition mechanism. If lunch reversals produce larger/sustained moves than mid-morning reversals, the participant-transition hypothesis is supported. If they perform identically, the time-of-day adds no information.

### Data Availability
USATECHIDXUSD M1 data is available. All timestamps are fully derivable.

### Causal Observability
Fully observable. Entry at 12:45 is deterministic. Exit at 13:45 is deterministic.

### Prior-Art Classification
EXTENSION of session-microstructure research, but with a genuinely new mechanism. Prior work (CAND-062, CAND-069) tested specific time anchors (15:15 fade, 11:30 anchor). This tests the 12:00–12:30 reversal as an explicit participant-transition event with a continuation (not reversal) trade. The economic mechanism (institutional repositioning) is distinct from the prior exhaustion/anchor mechanisms.

### Closed-Line Check
CAND-062 tested late-session exhaustion fades (reversal at 15:15). CAND-069 tested mid-session anchor sweeps. This candidate tests lunch-session reversal continuation — a different time window, different direction (continuation not fade), and different economic mechanism (repositioning not exhaustion).

### Standalone Potential
STRONG. Moderate frequency, clean mechanism, executable entry/exit.

### Component Potential
STRONG. Could serve as a session-specific continuation module.

### State-Artifact Potential
LOW. This is an Alpha/Event.

### Regime-Specialist Potential
STRONG. Specifically operates during the lunch-session transition regime.

### Information-Sharing Potential
Could share session-transition state with other modules (e.g., "lunch reversal confirmed = bias afternoon direction").

### Expected Failure Mode
The 15-minute confirmation may not be sufficient to filter noise, or the 60-minute holding window may be too long (capturing afternoon reversals). The counterfactual directly tests the session-transition value.

### G1 Test Design
G1 will measure the 60-minute post-entry return of lunch-session reversal continuations vs. mid-morning reversal continuations. Entry at confirmation close, exit 60 minutes later, direction from the reversal.

---

## 4. STRONGEST CANDIDATES

**Ranked:**

1. **CAND-073 (Mid-Day Reversal Continuation)** — Highest standalone potential. Moderate frequency, clean mechanism, executable entry/exit. Directly tests a specific participant-transition hypothesis with a rigorous counterfactual.

2. **CAND-071 (Cross-Market Gold→Tech)** — Genuinely novel mechanism family (cross-market transmission) not explored in any prior cycle. If validated, provides a completely independent signal source.

3. **CAND-072 (Weekly Range Compression Monday Breakout)** — Strongest component/module potential. The Friday compression state itself may be valuable even if the Alpha entry is marginal.

## 5. MECHANISM DIVERSITY

V24 differs from V19–V23 by exploring three entirely new mechanism families:

| V24 Candidate | Mechanism Family | Prior Coverage |
|---|---|---|
| CAND-071 | Cross-Market Transmission | ZERO — never tested |
| CAND-072 | Calendar / Weekly Structure | ZERO — CAND-063 tested intraday volatility compression, not weekly calendar inventory |
| CAND-073 | Session Microstructure (Reversal Continuation) | MINIMAL — prior session work tested fades and anchors, not continuation after lunch reversals |

V19–V23 heavily explored: sweep geometry, freshness, acceptance, session anchors, MOC flow, momentum exhaustion, shock absorption, structural breaks. V24 avoids all of these.

## 6. COUNTERFACTUAL QUALITY

- **CAND-071:** Tests Gold overnight → Tech open repricing vs. mid-day Tech entry. Isolates the timing of information arrival.
- **CAND-072:** Tests compressed-Friday Monday breakouts vs. expanded-Friday Monday breakouts. Isolates the inventory-imbalance mechanism.
- **CAND-073:** Tests lunch-session reversal continuations vs. mid-morning reversal continuations. Isolates the participant-transition mechanism.

All counterfactuals directly measure the incremental value of the proposed mechanism.

## 7. ECONOMIC HEADROOM

- **CAND-071:** Gold overnight moves >0.5% represent genuine macro repricing. Forced institutional rebalancing at the NY open should produce 10–30 bps. Exceeds 2 bps friction.
- **CAND-072:** Friday compression creates inventory imbalances. Forced Monday rebalancing should produce 15–50 bps. Exceeds 2 bps friction.
- **CAND-073:** Lunch-session institutional repositioning should produce 15–40 bps of sustained movement. Exceeds 2 bps friction.

## 8. DUAL-PATH CLASSIFICATION

| Candidate | Type | Standalone | Component | State | Regime | Rare-Event |
|---|---|---|---|---|---|---|
| CAND-071 | Alpha/Event | Moderate-Strong | Strong | Low | Moderate | No |
| CAND-072 | Alpha/Event | Moderate | Strong | Moderate | Strong | Moderate |
| CAND-073 | Alpha/Event | Strong | Strong | Low | Strong | No |

## 9. CROSS-MARKET APPLICABILITY

- **CAND-071:** Cross-market validation is INHERENT to the hypothesis (Gold→Tech). If G1 passes, G2 should test on additional cross-market pairs (e.g., XAGUSD→BTCUSD).
- **CAND-072:** Single-market (USATECHIDXUSD). Cross-market testing not required at this stage.
- **CAND-073:** Single-market (USATECHIDXUSD). Cross-market testing not required at this stage.

## 10. DATA FEASIBILITY

All three candidates use only XAUUSD M1 and USATECHIDXUSD M1 data, both available in the repository. No external data, no unavailable causal data, no proxy substitution.

## 11. PRIOR-ART FIREWALL

- **CAND-071:** NEW. No prior cross-market lead-lag testing.
- **CAND-072:** NEW. No prior weekly calendar structure testing. CAND-063 tested intraday Asian compression (different mechanism).
- **CAND-073:** EXTENSION. Prior session work (CAND-062, 069) tested fades and anchors. This tests continuation after lunch reversals — different direction, different time window, different economic mechanism.

## 12. CLOSED-LINE FIREWALL

No closed lines (DISC-021 through DISC-026) are reopened. No disguised rescues of V19–V23 failures. No overlap with CAND-056 through CAND-070.

## 13. CURRENT FORWARD OBSERVATION

### CAND-015
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-024
> ACTIVE / PROTECTED / UNTOUCHED

### CAND-035
> ACTIVE / PROTECTED / UNTOUCHED

Do not inspect their performance.

## 14. G1

> NOT EXECUTED

## 15. SYSTEM ASSEMBLY

> NOT EXECUTED

## 16. NEXT MILESTONE

> G1 — ECONOMIC PLAUSIBILITY SCREEN (CAND-071, CAND-072, CAND-073)
