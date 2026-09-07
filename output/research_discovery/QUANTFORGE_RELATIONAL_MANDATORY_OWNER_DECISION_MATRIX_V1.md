# QUANTFORGE — MANDATORY RELATIONAL OWNER DECISION MATRIX
# CONTENT EXTRACTION AND DECISION-READINESS AUDIT

**Date:** 2026-09-07
**Status:** DECISION-READINESS AUDIT COMPLETE — OWNER SELECTION PENDING
**Purpose:** Expose the actual substantive formulation differences and governance choices

---

## PHASE 1 — THE THREE FORMULATIONS

---

### RF-001: CROSS-MARKET CONFIRMATION FAILURE PROCESS

- **Exact title:** Cross-Market Confirmation Failure Process
- **Source mechanism:** REL-M01
- **Behavioral hypothesis:** When a structurally significant price event occurs in one liquid US equity index, correlated indices typically confirm the move within a structurally defined window. The confirmation reflects shared participant flow, information propagation, and cross-market hedging behavior. When confirmation explicitly fails — the correlated index does not produce the expected confirming event within the expected window — the failure represents a distinct market-state transition. The non-confirming market has absorbed or rejected the information that drove the confirming market, suggesting a structural divergence in participant positioning, information processing, or liquidity conditions.
- **Markets:** USATECHIDXUSD (primary) + one confirmation index (e.g., US500, US30)
- **Relational observable:** Primary market produces an N-bar breakout (close exceeds highest high of prior N completed M1 bars, or falls below lowest low). Confirmation market is observed for M bars. If confirmation market does NOT produce a confirming event within M bars, a confirmation failure has occurred.
- **State/event:** Confirmation failure — M bars elapse since the primary market's structural event without the confirmation market producing a confirming event.
- **Decision:** Fade the confirmation market's relative direction. If primary event bullish + confirmation failed → short the confirmation market. If primary event bearish + confirmation failed → long the confirmation market.
- **Entry:** Open of bar M+2 after the primary event (temporal causality preserved — all information known before execution).
- **Exit/invalidation:** Exit at session close (16:00 ET). Invalidation: if primary market reverses its structural event (close returns within N-bar range) before entry, opportunity is cancelled.
- **Opportunity population:** One per structural event; maximum one position at a time; structural events in last M bars of session excluded; duplicate same-direction breakouts without intervening reversal treated as continuation.
- **Scope:** M1 bars, US regular session (09:30–16:00 ET), forward-only prospective data.
- **Execution model:** Market order at open; market order at session close. 2 bps round-trip.
- **Standalone-Base rationale:** The confirmation failure event is self-contained and self-triggering. No external strategy needed for activation.
- **Distinctness rationale:** Not F-02 (pairs spread), not F-03 (rank rotation), not mean reversion (displacement fading), not TSMOM (own-history), not CAND-083 (single-market), not CAND-105 (lead-lag timing). The trigger is a discrete confirmation failure event.
- **Falsification route:** If the non-confirming market's subsequent session performance is statistically identical regardless of whether confirmation occurred — the mechanism is falsified.

---

### RF-002: CROSS-MARKET SYNCHRONY REGIME PROCESS

- **Exact title:** Cross-Market Synchrony Regime Process
- **Source mechanism:** REL-M02
- **Behavioral hypothesis:** Multiple liquid US equity indices normally move with high intraday synchrony — they advance and decline together because they share common participants, information, and macroeconomic exposure. When synchrony breaks down — one index moves materially while others do not, or indices move in opposite directions — the desynchronized state reflects a genuine difference in participant flow, information processing, or positioning between the indices. The synchrony breakdown is a state transition, not a continuous variable. The transition from synchronized to desynchronized represents a distinct market regime that may predict subsequent structural behavior in the desynchronized index.
- **Markets:** USATECHIDXUSD + at least one additional US equity index (e.g., US500)
- **Relational observable:** A synchrony measure computed over a rolling window of W completed M1 bars. The synchrony measure is the fraction of bars in the window where all indices in the complex move in the same direction (all positive or all negative returns). Directional agreement measure, not a correlation coefficient.
- **State/event:** Synchrony regime transition — the first bar where the synchrony measure falls below threshold T after having been above T (synchronized → desynchronized).
- **Decision:** Identify the divergent index (whose return direction differs from the majority of the complex in the most recent bar). Fade the divergent index's most recent direction. If divergent index moved up while complex moved down → short the divergent index. If divergent index moved down while complex moved up → long the divergent index.
- **Entry:** Open of the next bar after regime transition is detected.
- **Exit/invalidation:** Exit at session close (16:00 ET). Invalidation: if synchrony measure returns above T before entry, opportunity is cancelled (regime transition was transient).
- **Opportunity population:** One per regime transition; oscillation control within W bars (subsequent transitions within W bars not new opportunities); only synchronized→desynchronized transitions eligible; maximum one position at a time.
- **Scope:** M1 bars, US regular session (09:30–16:00 ET), forward-only prospective data.
- **Execution model:** Market order at open; market order at session close. 2 bps round-trip.
- **Standalone-Base rationale:** The synchrony regime transition is self-contained and self-triggering. No external strategy needed.
- **Distinctness rationale:** Not F-02 (pairs spread), not F-03 (rank rotation), not CAND-107 (vol co-movement), not vol regime trading. The mechanism is directional synchrony regime transitions.
- **Falsification route:** If the divergent index's subsequent session performance is statistically identical regardless of whether a synchrony breakdown occurred — the mechanism is falsified.

---

### RF-003: CROSS-MARKET SHOCK ABSORPTION ASYMMETRY PROCESS

- **Exact title:** Cross-Market Shock Absorption Asymmetry Process
- **Source mechanism:** REL-M03
- **Behavioral hypothesis:** When an external-looking event affects multiple correlated markets simultaneously — such as a sudden large price move, a news-driven gap, or a volatility spike — the markets absorb the shock differently. One market may absorb the shock quickly (price stabilizes, returns to pre-shock levels), while another may absorb it slowly (price continues moving, overshoots, takes longer to stabilize). The asymmetry in absorption reflects a structural difference in participant composition, liquidity depth, or information processing between the markets. The absorption characteristics are observable and may predict the subsequent trajectory of the slow-absorbing market.
- **Markets:** USATECHIDXUSD + at least one additional US equity index
- **Relational observable:** Shock detected when absolute return of complex-wide average (mean return across all indices) over a single M1 bar exceeds threshold S (bps). After shock, absorption characteristic of each index measured over K subsequent bars: sum of absolute signed returns over K bars (lower sum = faster absorption). Absorption asymmetry = difference between slowest-absorbing and fastest-absorbing index. If asymmetry exceeds A, a shock absorption asymmetry event has occurred.
- **State/event:** Shock absorption asymmetry event — K bars after shock, asymmetry exceeds A.
- **Decision:** The slow-absorbing index is in a structurally different state. Fade the slow-absorbing index's post-shock direction. If slow-absorbing index moved up after the shock → short. If it moved down → long.
- **Entry:** Open of bar K+1 after the shock.
- **Exit/invalidation:** Exit at session close (16:00 ET). Invalidation: if absorption asymmetry falls below A before entry, opportunity is cancelled.
- **Opportunity population:** One per shock event; maximum one position at a time; shocks in last K bars of session excluded; multiple shocks separated by ≥ K bars are independent.
- **Scope:** M1 bars, US regular session (09:30–16:00 ET), forward-only prospective data.
- **Execution model:** Market order at open; market order at session close. 2 bps round-trip.
- **Standalone-Base rationale:** The shock detection and absorption measurement are self-contained. No external strategy needed.
- **Distinctness rationale:** Not mean reversion (displacement fading), not CAND-105 (lead-lag timing), not vol regime (volatility level), not CAND-107 (vol co-movement). The mechanism is asymmetric absorption of the same shock across markets.
- **Falsification route:** If the slow-absorbing index's subsequent performance is statistically identical to the fast-absorbing index's performance — the mechanism is falsified.

---

## PHASE 2 — THE NINE GOVERNANCE-SELECTABLE PARAMETERS

| # | Formulation | Parameter / Decision | Exact unresolved choice | Why it matters mechanistically | Coupled with |
|---|-------------|---------------------|------------------------|-------------------------------|--------------|
| G1 | RF-001 | N — lookback horizon | What value of N defines a "structurally significant breakout"? The mechanism implies a finite horizon but not a unique value. | Smaller N = more frequent, smaller events; larger N = fewer, larger events. Different N produces different event populations. | G2 (weakly) |
| G2 | RF-001 | M — confirmation window | What value of M defines the confirmation deadline? The mechanism implies a finite window but not a unique value. | Shorter M = more failures detected; longer M = fewer failures. Different M produces different confirmation-failure populations. | G1 (weakly) |
| G3 | RF-001 | Confirmation market identity | Which second index (US500, US30, or other) serves as the confirmation reference? The mechanism requires a second index but not a specific one. | Different indices have different correlation structures with USATECHIDXUSD. The confirmation-failure dynamics change. | Independent |
| G4 | RF-002 | W — synchrony window | What value of W defines the observation horizon for directional agreement? The mechanism implies a finite window but not a unique value. | Shorter W = noisier measure, more transitions; longer W = smoother measure, fewer transitions. | G5 (moderately) |
| G5 | RF-002 | T — synchrony threshold | What value of T defines the boundary between synchronized and desynchronized? The mechanism implies a threshold but not a unique value. | Higher T = more transitions; lower T = fewer, more extreme transitions. | G4 (moderately) |
| G6 | RF-002 | Index complex composition | Which indices participate in the synchrony measure? The mechanism requires multiple indices but not specific ones. | Different compositions produce different synchrony dynamics. | Independent |
| G7 | RF-003 | S — shock threshold (bps) | What value of S defines an "external-looking" shock? The mechanism implies a threshold but not a unique value. | Lower S = more shocks; higher S = fewer, larger shocks. | G8, G9 (moderately) |
| G8 | RF-003 | K — absorption window | What value of K defines the absorption measurement period? The mechanism implies a finite period but not a unique value. | Shorter K = captures fast absorption; longer K = captures slow absorption. | G7, G9 (moderately) |
| G9 | RF-003 | A — asymmetry threshold | What value of A defines when absorption asymmetry is "significant"? The mechanism implies a threshold but not a unique value. | Lower A = more asymmetry events; higher A = fewer, more extreme events. | G7, G8 (moderately) |

---

## PHASE 3 — REDUCTION TO INDEPENDENT DECISIONS

| Independent Decision | Constituent parameters | Formulations affected | Decision meaning |
|----------------------|----------------------|----------------------|------------------|
| Decision 1: RF-001 temporal structure | G1 (N) + G2 (M) | RF-001 only | How to define the structural event lookback and confirmation deadline — jointly determines the event population |
| Decision 2: RF-001 structural scope | G3 (confirmation market) | RF-001 only | Which second index serves as the confirmation reference |
| Decision 3: RF-002 temporal/threshold structure | G4 (W) + G5 (T) | RF-002 only | How to measure synchrony and define the regime boundary — jointly determines the transition population |
| Decision 4: RF-002 structural scope | G6 (index complex) | RF-002 only | Which indices participate in the synchrony measure |
| Decision 5: RF-003 event/threshold structure | G7 (S) + G8 (K) + G9 (A) | RF-003 only | How to define the shock, measure absorption, and set the asymmetry threshold — jointly determines the asymmetry-event population |
| Decision 6: RF-003 structural scope | G6 (index complex) | RF-003 only | Which indices participate in the shock absorption analysis |

**Exact reduction:** 9 nominal parameters → **6 independent decisions**. The coupling analysis confirmed:
- G1+G2: weak temporal coupling (N and M interact but are not strictly dependent)
- G4+G5: moderate measurement coupling (W and T interact as a system)
- G7+G8+G9: moderate absorption coupling (S, K, and A interact as a system)
- G3 and G6 are structurally independent choices

---

## PHASE 4 — EXACT OWNER OPTIONS

### Decision 1: RF-001 temporal structure (N + M)

**Choice A:** Short horizon + short window (N = 15–30 M1 bars, M = 5–15 M1 bars)
- Exact rule: Close exceeds highest high (or lowest low) of prior 15–30 completed M1 bars; confirm within 5–15 bars of primary event
- Character: Frequent, small events; early failure detection; more opportunities to test mechanism; more noise

**Choice B:** Medium horizon + medium window (N = 30–60 M1 bars, M = 15–30 M1 bars)
- Exact rule: Close exceeds highest high of prior 30–60 completed M1 bars; confirm within 15–30 bars
- Character: Moderately frequent events; balanced detection; moderate position time remaining

**Choice C:** Long horizon + long window (N = 60–120 M1 bars, M = 30–60 M1 bars)
- Exact rule: Close exceeds highest high of prior 60–120 completed M1 bars; confirm within 30–60 bars
- Character: Infrequent, large events; late failure detection; fewer opportunities; less session time remaining

**Mechanism preserved by all listed choices:** YES — N defines the event population, M defines the confirmation window; the mechanism (confirmation failure) is identical across all options.

**Outside-formulation options excluded:** Very short N (<15 bars) approaches noise; very long N (>120 bars) approaches trend-following; very short M (<5 bars) may not allow a meaningful confirmation assessment; very long M (>60 bars) may extend past session boundaries.

---

### Decision 2: RF-001 structural scope (confirmation market)

**Choice A:** US500 (S&P 500 proxy)
- Exact rule: US500 is the confirmation market for USATECHIDXUSD events
- Character: Broadest US equity proxy; high correlation with USATECHIDXUSD; confirmation failures likely rare but significant

**Choice B:** US30 (Dow Jones proxy)
- Exact rule: US30 is the confirmation market
- Character: Different sector composition; may produce different confirmation-failure dynamics

**Mechanism preserved by all listed choices:** YES — confirmation market identity defines the pair, not the mechanism.

**Outside-formulation options excluded:** Non-US equity indices (different session hours); indices without M1 data availability.

---

### Decision 3: RF-002 temporal/threshold structure (W + T)

**Choice A:** Short window + strict threshold (W = 10–20 M1 bars, T = 0.70–0.80)
- Exact rule: Directional agreement over 10–20 bars; synchronized when >70–80% show agreement
- Character: Frequent transitions; noisy measure; each transition more extreme; more opportunities but more false signals

**Choice B:** Medium window + moderate threshold (W = 20–40 M1 bars, T = 0.55–0.65)
- Exact rule: Directional agreement over 20–40 bars; synchronized when >55–65% show agreement
- Character: Balanced noise/frequency; moderate detection speed

**Choice C:** Long window + lenient threshold (W = 40–80 M1 bars, T = 0.45–0.55)
- Exact rule: Directional agreement over 40–80 bars; synchronized when >45–55% show agreement
- Character: Smooth measure; rare transitions; each transition more significant; fewer opportunities

**Mechanism preserved by all listed choices:** YES — W defines synchrony measurement, T defines regime boundary; the mechanism (synchrony regime transition) is identical across all options.

**Outside-formulation options excluded:** Very short W (<10 bars) too noisy; very long W (>80 bars) approaches session-level aggregation; very low T (<0.45) produces too many transitions; very high T (>0.80) rarely transitions.

---

### Decision 4: RF-002 structural scope (index complex)

**Choice A:** Two-index complex (USATECHIDXUSD + US500)
- Exact rule: Synchrony measured across two indices
- Character: Simplest complex; clear directional agreement; limited to one relationship

**Choice B:** Three-index complex (USATECHIDXUSD + US500 + US30)
- Exact rule: Synchrony measured across three indices; majority direction (≥2 of 3)
- Character: Richer synchrony signal; majority may be ambiguous with three indices

**Mechanism preserved by all listed choices:** YES — complex composition defines participating markets, not the mechanism.

**Outside-formulation options excluded:** Complexes with indices trading different sessions; indices without M1 data availability.

---

### Decision 5: RF-003 event/threshold structure (S + K + A)

**Choice A:** Moderate shock + short window + low threshold (S = 10–20 bps, K = 5–10 bars, A = 5–10 bps cumulative)
- Exact rule: Shock when complex return >10–20 bps; measure over 5–10 bars; asymmetry >5–10 bps
- Character: Frequent shocks; fast absorption assessment; many asymmetry events; each may be less extreme

**Choice B:** Large shock + medium window + moderate threshold (S = 20–40 bps, K = 10–20 bars, A = 10–20 bps cumulative)
- Exact rule: Shock when complex return >20–40 bps; measure over 10–20 bars; asymmetry >10–20 bps
- Character: Infrequent shocks; balanced capture; moderate event frequency

**Choice C:** Extreme shock + long window + high threshold (S = 40+ bps, K = 20–40 bars, A = 20+ bps cumulative)
- Exact rule: Shock when complex return >40 bps; measure over 20–40 bars; asymmetry >20 bps
- Character: Very rare shocks; slow absorption capture; very few events; each highly significant

**Mechanism preserved by all listed choices:** YES — S defines shock population, K defines absorption measurement, A defines asymmetry threshold; the mechanism (shock absorption asymmetry) is identical across all options.

**Outside-formulation options excluded:** Very low S (<10 bps) treats every small move as a shock; very high S (>50 bps) produces too few events; very short K (<5 bars) may not capture absorption; very long K (>40 bars) extends past session boundaries; very low A (<5 bps) treats every difference as asymmetry; very high A (>30 bps) produces too few events.

---

### Decision 6: RF-003 structural scope (index complex)

**Choice A:** Two-index complex (USATECHIDXUSD + US500)
- Exact rule: Absorption measured across two indices
- Character: Simplest complex; clear asymmetry; limited to one relationship

**Choice B:** Three-index complex (USATECHIDXUSD + US500 + US30)
- Exact rule: Absorption measured across three indices; slowest vs fastest absorption
- Character: Richer signal; comparison across three indices may be less clean

**Mechanism preserved by all listed choices:** YES — complex composition defines participating markets, not the mechanism.

**Outside-formulation options excluded:** Complexes with indices trading different sessions; indices without M1 data availability.

---

## PHASE 5 — FORMULATION COMPARISON

| Dimension | RF-001 | RF-002 | RF-003 |
|-----------|--------|--------|--------|
| Core mechanism | One market fails to confirm another's structural event | Index complex transitions from synchronized to desynchronized | Markets absorb the same shock at different speeds |
| Why relationship is informative | Confirmation failure reveals structural divergence in participant positioning or information processing | Synchrony breakdown reveals genuine differences in flow, positioning, or information between indices | Absorption asymmetry reveals structural differences in market depth and participant composition |
| Observable | N-bar breakout in primary; M-bar confirmation window in secondary | W-bar directional agreement fraction; threshold T | Complex-wide return > S; K-bar absorption measure; asymmetry > A |
| Event/state transition | Confirmation failure (M bars without confirmation) | Synchrony regime transition (measure crosses below T) | Shock absorption asymmetry (K bars after shock, asymmetry > A) |
| Trading decision | Fade non-confirming index's relative direction | Fade divergent index's most recent direction | Fade slow-absorbing index's post-shock direction |
| Temporal structure | N-bar lookback → M-bar window → entry bar M+2 → exit session close | W-bar rolling window → transition detection → entry next bar → exit session close | Shock detection → K-bar measurement → entry bar K+1 → exit session close |
| Opportunity population | One per structural event; one position at a time; last M bars excluded | One per regime transition; oscillation control within W bars | One per shock; K-bar separation; last K bars excluded |
| Execution complexity | LOW — single entry/exit per event | LOW — single entry/exit per transition | LOW — single entry/exit per shock |
| Data complexity | LOW — two M1 series, aligned timestamps | MODERATE — multiple M1 series, majority direction computation | MODERATE — multiple M1 series, absorption measure computation |
| Standalone Base potential | YES — self-triggering | YES — self-triggering | YES — self-triggering |
| Distinctness risk | LOW — clearly distinct from all prior work | LOW — clearly distinct from all prior work | LOW — clearly distinct from all prior work |
| Specification risk | MODERATE — N and M could be reinterpreted; temptation to tune | MODERATE — W and T could be reinterpreted; temptation to tune | MODERATE — S, K, A could be reinterpreted; temptation to tune; 3 coupled parameters |
| Falsification clarity | HIGH — clear null: performance identical regardless of confirmation status | HIGH — clear null: performance identical regardless of synchrony regime | HIGH — clear null: slow-absorbing performance identical to fast-absorbing |

---

## PHASE 6 — DISTINCTNESS AUDIT

### F-02 (two-index pairs)

**RF-001:** DISTINCT — F-02 trades the spread between two indices. RF-001 detects when one index fails to confirm another's structural event. The trigger is a discrete confirmation failure, not a continuous spread level.

**RF-002:** DISTINCT — F-02 trades a specific pair's spread. RF-002 measures joint directional synchrony across the index complex. Different unit of analysis.

**RF-003:** DISTINCT — F-02 trades spread convergence/divergence. RF-003 measures asymmetry in how different markets absorb the same shock. Different mechanism.

### F-03 (rank rotation)

**RF-001:** DISTINCT — F-03 ranks indices by relative strength. RF-001 detects a specific event (confirmation failure) in a specific pair. No ranking occurs.

**RF-002:** DISTINCT — F-03 ranks by relative strength. RF-002 measures directional agreement. Strength and synchrony are different concepts.

**RF-003:** DISTINCT — F-03 ranks indices. RF-003 measures absorption characteristics. Different concept.

### CAND-083 (cumulative rejection pressure)

**RF-001:** DISTINCT — CAND-083 is single-market cumulative rejection. RF-001 is cross-market confirmation failure. Different unit of analysis.

**RF-002:** DISTINCT — CAND-083 is single-market. RF-002 is cross-market synchrony. Different unit of analysis.

**RF-003:** DISTINCT — CAND-083 is single-market rejection accumulation. RF-003 is cross-market shock absorption. Different unit of analysis.

### Mean reversion

**RF-001:** DISTINCT — Mean reversion fades displacement toward a mean. RF-001 detects when one market fails to confirm another's event. The trigger is the failure itself, not the level of prices.

**RF-002:** DISTINCT — Mean reversion fades displacement. RF-002 uses synchrony as a regime indicator. Different mechanism.

**RF-003:** DISTINCT — Mean reversion fades displacement. RF-003 measures asymmetry in shock absorption. Different mechanism.

### TSMOM

**RF-001:** DISTINCT — TSMOM follows own-history trend. RF-001 is cross-market. The trigger is the relationship between two markets, not one market's history.

**RF-002:** DISTINCT — TSMOM is own-trend. RF-002 is cross-market synchrony. Different concept.

**RF-003:** DISTINCT — TSMOM is own-trend. RF-003 is cross-market absorption. Different concept.

### ORB / Breakout

**RF-001:** DISTINCT — Breakout/ORB trades the breakout itself. RF-001 detects when one market fails to confirm another's breakout. The trigger is the failure detection, not the breakout.

**RF-002:** DISTINCT — Breakout/ORB trades breakouts. RF-002 detects regime transitions. Different trigger.

**RF-003:** DISTINCT — Breakout/ORB trades breakouts. RF-003 detects shock absorption asymmetry. Different trigger.

---

## PHASE 7 — OWNER DECISION QUALITY

### RF-001

- **Mechanism clarity:** HIGH — confirmation failure is a discrete, intuitive event with clear temporal structure
- **Determinism:** HIGH — fully deterministic once N, M, confirmation market frozen
- **Data feasibility:** HIGH — two M1 series needed; available in forward pipeline
- **Standalone Base potential:** HIGH — self-triggering; no conditional dependence
- **Specification simplicity:** HIGH — 2 temporal parameters + 1 market identity; 3 total governance choices
- **Falsifiability:** HIGH — clear null hypothesis (performance identical regardless of confirmation status)
- **Governance risk:** LOW-MODERATE — N and M are coupled but independent decisions are clear; specification drift risk mitigated by V38A freeze

### RF-002

- **Mechanism clarity:** MEDIUM — synchrony regime is clear but requires defining "majority" direction and the regime boundary
- **Determinism:** HIGH — fully deterministic once W, T, index complex frozen
- **Data feasibility:** HIGH — multiple M1 series needed; available
- **Standalone Base potential:** HIGH — self-triggering
- **Specification simplicity:** MEDIUM — 2 parameters (coupled) + complex composition; majority direction must be defined
- **Falsifiability:** HIGH — clear null hypothesis (performance identical regardless of synchrony regime)
- **Governance risk:** LOW-MODERATE — W and T interact as a system; regime definition must be frozen

### RF-003

- **Mechanism clarity:** MEDIUM — shock absorption is intuitive but requires defining "shock," "absorption," and "asymmetry" precisely
- **Determinism:** HIGH — fully deterministic once S, K, A, index complex frozen
- **Data feasibility:** HIGH — multiple M1 series needed; available
- **Standalone Base potential:** HIGH — self-triggering
- **Specification simplicity:** MEDIUM — 3 parameters (coupled as a system) + complex; more interaction risk
- **Falsifiability:** HIGH — clear null hypothesis (slow-absorbing performance identical to fast-absorbing)
- **Governance risk:** MODERATE — S, K, A interact as a system; more coupling risk than RF-001 or RF-002

---

## PHASE 8 — CRITICAL DECISION QUESTION

### RF-001

**What would we be committing ourselves to learn if we selected this formulation?**

We would be testing whether the failure of one US equity index to confirm another's structurally significant price event contains independent directional information about the non-confirming index's subsequent session performance. Specifically, we would be learning whether cross-market information propagation and hedging flows produce predictable patterns when confirmation explicitly fails.

### RF-002

**What would we be committing ourselves to learn if we selected this formulation?**

We would be testing whether the breakdown of normally synchronous directional movement across the US equity complex contains independent directional information about the divergent index's subsequent session performance. Specifically, we would be learning whether synchrony regime transitions reflect genuine structural differences in participant flow, positioning, or information processing that manifest in subsequent price behavior.

### RF-003

**What would we be committing ourselves to learn if we selected this formulation?**

We would be testing whether asymmetric absorption of the same external shock across correlated US equity indices contains independent directional information about the slow-absorbing index's subsequent session performance. Specifically, we would be learning whether structural differences in participant composition and liquidity depth between indices produce predictable differential trajectories after simultaneous shocks.

---

## PHASE 9 — OWNER DECISION READINESS

**RF-001:** OWNER-DECISION READY
- Mechanism complete: YES
- All parameters classified: YES (3 governance-selectable)
- No empirical calibration blockers: YES
- Distinctness verified: YES
- All governance alternatives documented: YES

**RF-002:** OWNER-DECISION READY
- Mechanism complete: YES
- All parameters classified: YES (3 governance-selectable)
- No empirical calibration blockers: YES
- Distinctness verified: YES
- All governance alternatives documented: YES

**RF-003:** OWNER-DECISION READY
- Mechanism complete: YES
- All parameters classified: YES (4 governance-selectable)
- No empirical calibration blockers: YES
- Distinctness verified: YES
- All governance alternatives documented: YES

---

## PHASE 10 — NO ECONOMICS

- **Economic testing:** NO
- **Historical economic results:** NOT INSPECTED
- **FB-001 economics:** NOT INSPECTED
- **F-01 economics:** NOT INSPECTED
- **Protected-forward economics:** NOT INSPECTED
- **Optimization:** NO

---

## PHASE 11 — NO NEW DISCOVERY

No new relational mechanisms generated. No RF-004 created. No modifications to RF-001/002/003. This task only exposes the existing owner decision for transparency.

---

**END OF MANDATORY OWNER DECISION MATRIX**
