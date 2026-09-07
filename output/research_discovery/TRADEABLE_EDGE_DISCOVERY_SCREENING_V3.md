# QUANTFORGE — TRADEABLE EDGE DISCOVERY SCREENING V3

> **GOVERNANCE AMENDMENT (2026-08-24): ECONOMIC-FIRST PIPELINE INTEGRATION**
> Following the Program-Level Research Audit, all future candidate discovery and screening processes must adhere to the `QUANTFORGE_RESEARCH_FACTORY_V2.md` operating doctrine. 
> 
> Specifically:
> 1. Candidate generation must systematically diversify across mechanism families (no more exclusive focus on `event -> direction -> fixed horizon`).
> 2. Every candidate must pass **G1 (Economic Plausibility Gate)** before any expensive scientific infrastructure or definition lock is authorized. A structural argument for sufficient economic headroom (e.g., >15 bps expected gross) must be made using observed friction.
> 3. Surviving candidates must undergo **G2 (Cheap Empirical Pilot)** before full scientific validation.
> 
> This document (V3) selected ORD, which subsequently failed economic viability. Future screenings will apply the G1/G2 gates to prevent escalation of sub-friction signals.

## 0. Identity and Mode

- **Task:** fresh, READ-ONLY, outcome-blind discovery screening for the next QuantForge trading-edge candidate. No backtest, no PnL, no optimization, no ML, no protocol, no EA.
- **Control set:** `docs/SESSION_HANDOFF.md` (2026-08-17); `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-001…025); `research/knowledge/RESEARCH_TIMELINE.md`; `output/research_discovery/COMBINATION_EDGE_DISCOVERY_SCREENING_V1.md` (result: B — combination research not yet justified); finalized adjudication artifacts for DISC-021…025; local market/data inventory (5 M1 markets + 5 MT5 tick bid/ask files).
- **Universe:** validated local M1 markets — XAUUSD, XAGUSD, EURUSD, BTCUSD, USATECHIDXUSD. **EURUSD is excluded from initial consideration until its invalid-day data-quality gate is separately resolved** (recorded in DISC-025). No market is selected for historical attractiveness; candidates are screened against the whole validated set.
- **Data facts (repository-established):** M1 OHLCV for all five markets (UTC timestamps; `volume` column unreliable — all zeros per the XAGUSD cost-viability record); full MT5 bid/ask tick files for all five (XAUUSD/BTCUSD/USATECHIDXUSD/XAGUSD used for observed cost modeling; EURUSD tick file present but market data-gated); sessions via `America/New_York`.

---

## 1. Executive Verdict

**PRIMARY CANDIDATE: Opening-Range Directional Break (ORD).** **BACKUP CANDIDATE: Volatility-Coil Directional Breakout (VCD).** Only the primary is authorized for the next stage (Scientific Definition Screening / Definition Lock); the backup is held as a documented alternative. Three further candidates are rejected or require justification. The screen applies the central lesson of DISC-025: **economic capture must be structurally plausible before any experiment** — every approved candidate's measured object is the post-entry move, its entry is the event itself, its invalidation is structural, and its expected excursion is assessed against observed friction (XAUUSD ≈ 1.7 bp RT, USATECHIDXUSD ≈ 1.1 bp RT, XAGUSD ≈ 12.3 bp, BTCUSD ≈ 16.8 bp, per the sweep economic translation).

---

## 2. Current Research Position

Closed lines (must not be revived, tuned, inverted, or used as filters): Mean Reversion (DISC-021), fixed 12/1 TSMOM (DISC-022), H01 broad universal formulation (closed in that form), Session-Anchored Range Expansion (DISC-024, contradicted), Liquidity Sweep / Reversal (DISC-025, behavior supported / translation non-viable). Open: H01 Equity Track A (narrowed US-equity program; separate daily-frequency line, not an intraday candidate source). Combination research: not justified (combination screen = B). Active objective: this screening.

## 3. Lessons From Prior Candidates

- **Session Range Expansion:** the behavioral hypothesis itself was contradicted — compression did not precede larger range. Lesson: some behavioral hypotheses are simply false; the screen must tolerate falsification quickly.
- **Liquidity Sweep / Reversal:** the behavior was strongly supported across four markets, yet the minimal translation failed **gross, before costs** — because the validated response (MFE measured from a prior Asian reference level) was fundamentally disconnected from the executable entry (confirmation close, which fires after most of the move). **Statistical significance alone is insufficient; the measured object must be the post-entry move.** This is the binding design constraint of V3.
- **General rule adopted:** a candidate is rejected NOW if its research statistic would naturally measure a move from a historical reference while the trade enters after that move. Every surviving candidate defines its response over the window beginning at the entry.

## 4. Candidate 1 — Opening-Range Directional Break (ORD)

- **Candidate name:** ORD — Opening-Range Directional Break.
- **Market mechanism:** at the start of an active session, the market establishes a small opening range as liquidity forms; a directional break of that range with a close beyond it reflects order-flow imbalance; intraday continuation is the auction hypothesis (the opening-range break is a widely observed intraday event with follow-through in directional sessions).
- **Deterministic definition idea:** opening window = first N minutes of the London session (or a fixed clock-time window for markets without session structure); OpeningRange High/Low = max(high)/min(low) over that window; event = first subsequent M1 bar whose close is strictly beyond the opening range (upper break: close > OpeningRange High; lower break: close < OpeningRange Low) within the session.
- **Decision-time information:** opening range (known at window end) and the breaking bar's OHLC (known at its close) — all pre-decision; no future information.
- **Simplest executable translation:** market order at the close of the breaking bar; direction = break direction (upper → long, lower → short). The event IS the entry — no confirmation lag beyond one bar.
- **Natural invalidation:** structural — price returns inside the opening range (close back through the broken edge). Loss is bounded by the break distance.
- **Natural exit:** structurally defined alternatives registered later (fixed behavioral horizon close; opposite opening-range edge); one primary exit chosen in the definition lock on mechanics, not profitability.
- **Economic capture argument:** the measured response is the continuation **after** the break close (entry → exit), not a move from a prior reference. Expected continuation on directional sessions is tens of bp; observed friction on XAUUSD ≈ 1.7 bp and USATECHIDXUSD ≈ 1.1 bp RT is small relative to that. The structural invalidation bounds the adverse case.
- **Cross-market applicability:** high — any market with defined sessions (metals, index CFD); crypto needs a fixed clock-time "opening window" (24/7), a definitional adaptation; EURUSD pending data gate.
- **Data requirements:** M1 OHLC only (available). No volume, no tick data required.
- **Expected frequency:** high — one opening window per session per market; break events plausibly on a large fraction of directional days (order of magnitude: tens per month per market).
- **Complexity:** LOW — session window + range + break + invalidation; deterministic geometry only.
- **Main scientific risk:** opening-range breaks may not continue more often than chance on many days (range-bound days → frequent small invalidation losses); the definition lock must specify the response as post-entry continuation to avoid the anti-sweep trap.
- **Main economic risk:** if the break distance is small and the invalidation tight, the win rate may be too low for the loss sizes; mitigated by structural asymmetry (bounded invalidation loss vs open continuation).
- **Rescue/overfitting risk:** low-to-moderate — the opening-window length N is the one structural parameter; it must be frozen in the definition lock from mechanics (e.g., liquidity-formation time), not chosen by outcomes, and evaluated across markets without per-market tuning.
- **Overall screening verdict:** **PROMISING.**

## 5. Candidate 2 — Volatility-Coil Directional Breakout (VCD)

- **Candidate name:** VCD — Volatility-Coil Directional Breakout.
- **Market mechanism:** after a period of realized-volatility contraction (a "coil"), the market accumulates; a directional break of the coil with a close beyond it releases the pent-up move; continuation is the hypothesis.
- **Deterministic definition idea:** coil = the price range over the trailing K sessions with realized-volatility contraction (deterministic measure, e.g., K-day high/low range narrowing relative to its own trailing distribution); event = first M1/daily bar whose close is strictly beyond the coil edge.
- **Decision-time information:** coil edges and the breaking bar — all pre-decision.
- **Simplest executable translation:** market order at the breaking bar close; direction = break direction.
- **Natural invalidation:** structural — close back inside the coil.
- **Natural exit:** structurally defined (horizon close / structural opposite point); chosen in the definition lock.
- **Economic capture argument:** the response is the post-break continuation; compression-break expansions are often large relative to friction; observed friction favorable on XAUUSD/USATECHIDXUSD.
- **Cross-market applicability:** high — coil/consolidation is universal across metals/index/crypto; EURUSD pending data gate.
- **Data requirements:** M1 OHLC only.
- **Expected frequency:** moderate — a few coils per month per market (K-session contraction is rarer than an opening-range break).
- **Complexity:** LOW-MEDIUM — the coil/contraction definition needs a deterministic volatility measure.
- **Main scientific risk:** false breaks of the coil are common; the definition must not be a re-statement of the contradicted Session-Range object — the response here is **directional continuation**, not range size. Independence must be explicit in the definition lock.
- **Main economic risk:** entry at the break close may be late relative to the coil's initial burst; the measured object (post-entry continuation) must be the statistic.
- **Rescue/overfitting risk:** moderate — the coil-contraction threshold is a structural parameter to be frozen, not tuned; must not be framed as "Session Range done right."
- **Overall screening verdict:** **PROMISING (backup).**

## 6. Candidate 3 — Structural-Level Break-and-Hold (BLH)

- **Candidate name:** BLH — Structural-Level Break-and-Hold (continuation through a prior-session extreme).
- **Market mechanism:** a close beyond a prior session's extreme with hold (no immediate rejection) indicates true breakout continuation rather than stop-run reversal.
- **Deterministic definition idea:** reference = prior session High/Low; event = first close strictly beyond the reference that holds for a fixed follow-through window.
- **Decision-time information:** prior session extreme and the breaking bar — pre-decision.
- **Simplest executable translation:** market order at the breaking bar close; direction = break direction.
- **Natural invalidation:** close back through the prior-session extreme.
- **Natural exit:** structurally defined.
- **Economic capture argument:** the response is the post-break continuation; but the reference is a **prior-session level**, and the entry at the break close occurs after the level-to-close move — a partial anti-sweep exposure. Capture is honest only if the statistic is the post-entry move.
- **Cross-market applicability:** high.
- **Data requirements:** M1 OHLC only.
- **Expected frequency:** moderate.
- **Complexity:** LOW.
- **Main scientific risk:** conceptual adjacency to the sweep's falsification condition ("true breakout dominates"); must be framed as an independent continuation hypothesis, not sweep repair — otherwise it fails the closed-line firewall.
- **Main economic risk:** same entry-lag concern as the sweep, partially mitigated by requiring the response to be post-entry.
- **Rescue/overfitting risk:** moderate-high — proximity to the closed sweep line makes rescue framing a live governance hazard.
- **Overall screening verdict:** **NEEDS MORE JUSTIFICATION** — only eligible if the definition lock establishes independence from the sweep line and the response is strictly post-entry; not selected as primary or backup.

## 7. Candidate 4 — Session-Overlap Persistence (SOP)

- **Candidate name:** SOP — Session-Overlap Directional Persistence.
- **Market mechanism:** directional order-flow during the London/NY overlap persists into the remainder of the NY session.
- **Deterministic definition idea:** overlap window = 08:00–11:00 ET; event = net directional move over the overlap window exceeding a deterministic threshold; trade in that direction.
- **Decision-time information:** overlap close — pre-decision at the signal.
- **Simplest executable translation:** market order at the overlap close.
- **Natural invalidation:** reversal of the overlap move by a fixed structural amount.
- **Natural exit:** structurally defined.
- **Economic capture argument:** entry is **after** the overlap move — the captured object is persistence, which is a momentum-family claim.
- **Cross-market applicability:** moderate (FX/metals/index; crypto weaker without overlap structure).
- **Data requirements:** M1 OHLC only.
- **Expected frequency:** high (daily).
- **Complexity:** LOW.
- **Main scientific risk:** momentum-family hypothesis; the closed TSMOM line adjudicated a momentum object as NOT PROMOTABLE (cross-era inconsistency). An intraday persistence claim is a different frequency but the same dimension — the definition lock would need an independent rationale, and the governance cost is high.
- **Main economic risk:** entry-after-move; persistence may be weak after the overlap.
- **Rescue/overfitting risk:** high — proximity to the closed TSMOM/momentum dimension.
- **Overall screening verdict:** **NEEDS MORE JUSTIFICATION / REJECTED as a priority** — momentum-family proximity to a closed line; not selected.

## 8. Candidate 5 — Tick Spread-Structure Trigger (TSS)

- **Candidate name:** TSS — Quote-Spread Structure Trigger.
- **Market mechanism:** deterministic bid/ask spread behavior (e.g., spread contraction or widening-exhaustion at structural moments) as a timing signal.
- **Deterministic definition idea:** per-minute median spread from tick data relative to its trailing distribution at fixed clock/session moments.
- **Decision-time information:** spread state — pre-decision.
- **Simplest executable translation:** market order at the trigger; direction from a second structural component.
- **Natural invalidation / exit:** structural, but the expected excursion is small — the signal operates at microstructure scale.
- **Economic capture argument:** weak — observed round-trip friction is 1–17 bp across markets (XAGUSD ≈ 12 bp, BTCUSD ≈ 17 bp); a spread-structure trigger's expected excursion is typically the same order as or smaller than friction; latency sensitivity is extreme; the XAGUSD cost-viability precedent (gross ≈ 10.9 bp consumed by ≈ 9.1 bp costs) demonstrates the class-level danger.
- **Cross-market applicability:** moderate (requires tick data; EURUSD gated).
- **Data requirements:** tick bid/ask (available but heavy; ~0.75 billion lines processed this cycle).
- **Expected frequency:** high.
- **Complexity:** HIGH (streaming tick infrastructure, latency modeling).
- **Main scientific risk:** the signal's excursion is fundamentally friction-adjacent.
- **Main economic risk:** very high — microstructure strategies die at the spread.
- **Rescue/overfitting risk:** high — easily overfit at tick granularity.
- **Overall screening verdict:** **REJECTED** — friction-dominated, latency-sensitive, low economic-capture plausibility.

## 9. Economic Capture Comparison

| Candidate | Entry = event? | Measured object | Invalidation | Friction vs expected excursion | Capture class |
|---|---|---|---|---|---|
| ORD | YES (break close) | post-entry continuation | opening-range re-entry (tight, structural) | XAUUSD 1.7 bp RT vs tens-of-bp sessions | STRONG |
| VCD | YES (break close) | post-entry continuation | coil re-entry (structural) | small RT vs large expansion days | STRONG-MODERATE |
| BLH | YES (break close) | post-entry continuation | prior-extreme re-entry | moderate | MODERATE |
| SOP | LATE (after overlap) | persistence | structural | moderate | WEAK-MODERATE |
| TSS | trigger-time | microstructure-scale | structural | excursion ≈ friction | WEAK |

## 10. Cross-Market Comparison

All five candidates are multi-market by construction. ORD/VCD/BLH require only session/clock structure (crypto needs a clock-window adaptation); SOP requires overlap structure (crypto weak); TSS requires tick depth (all present, EURUSD gated). No candidate assumes a specific market; the eventual scope (XAU-specific / metals / multi-asset) is left to discovery.

## 11. Data Feasibility

ORD, VCD, BLH, SOP: M1 OHLC only — fully available (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD; EURUSD pending data gate). TSS: tick bid/ask — available but heavier and friction-dominated. No candidate requires unavailable data; no procurement task is warranted.

## 12. Complexity Comparison

LOW: ORD, BLH, SOP. LOW-MEDIUM: VCD (coil/contraction definition). HIGH: TSS (tick streaming, latency). Preference rule (high economic plausibility + low complexity) favors ORD then VCD.

## 13. Ranked Candidate Matrix

| Dimension (weight) | ORD | VCD | BLH | SOP | TSS |
|---|---|---|---|---|---|
| Economic capture (30%) | 24 | 24 | 19 | 14 | 8 |
| Cross-market (20%) | 18 | 18 | 17 | 15 | 12 |
| Objective definition (15%) | 14 | 13 | 12 | 12 | 9 |
| Data availability (15%) | 15 | 15 | 15 | 15 | 13 |
| Expected frequency (10%) | 9 | 7 | 7 | 8 | 6 |
| Implementation simplicity (10%) | 9 | 8 | 9 | 8 | 4 |
| **Weighted total** | **89** | **85** | **79** | **72** | **52** |

Ranking uses pre-result reasoning and available infrastructure only; no historical PnL or significance enters.

## 14. Primary Candidate

**ORD — Opening-Range Directional Break.** Highest weighted score (89); strongest economic-capture class; highest frequency; lowest complexity; cleanest independence from all closed lines (no prior-extreme reference, no rejection logic, no compression→range claim, no momentum-family frame). The opening-range concept has no closed-line precedent in this repository.

## 15. Backup Candidate

**VCD — Volatility-Coil Directional Breakout.** Second (85); larger expected excursion but lower frequency and moderate definitional complexity; requires explicit independence framing from the contradicted Session-Range object (directional continuation vs range size). Held as backup; NOT authorized for the next stage unless the primary is rejected at definition lock.

## 16. Why Primary Was Selected

ORD satisfies the special-priority profile best: the behavioral event (opening-range break) **is** the executable entry; the natural invalidation (range re-entry) is structural and tight; the natural exit is structurally definable; the expected continuation is substantially larger than observed friction on the best-cost markets (XAUUSD 1.7 bp, USATECHIDXUSD 1.1 bp RT); the same mechanism occurs in every session-structured market; and it is the least exposed to closed-line rescue framing. It also directly embodies the anti-sweep lesson: the response will be defined as the post-entry move, never a move from a prior reference level.

## 17. Prohibited Follow-Up

- Any backtest, PnL calculation, parameter search, or optimization before the definition lock.
- Selecting the opening window N, coil thresholds, or exits from historical outcomes.
- Framing ORD or VCD as any closed-line repair (no "sweep done right," "session range done right," "TSMOM alternative").
- Using H01 as a state variable; reviving the combination screen; using ML to discover the pattern; building an EA; touching BOE/Assembly/Deployment; modifying any protocol; reopening DISC-021/022/024/025 or H01-broad.
- Including EURUSD before its data-quality gate is resolved.
- Volume-based definitions (volume column unusable).

## 18. Exact Next Legitimate Task

> **SCIENTIFIC DEFINITION SCREENING / DEFINITION LOCK for ORD** — freeze: scientific question, object, universe (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD; EURUSD pending), opening-window definition (frozen from mechanics), event/signal definition, decision-time timing, response (post-entry continuation only), structural invalidation, primary exit, falsification, cross-market scope, and the explicit independence statement from all closed lines. Then: definition → pre-registration → independent audit → execution → adjudication → economic translation.

VCD remains the documented backup; no backup experiment is authorized by this screen.

## 19. Integrity

Strictly READ-ONLY and outcome-blind. The only new repository artifact is this screening. No code, no experiment, no backtest, no PnL, no optimization, no governance-file modification, no market selected for historical performance. All data facts are repository-established; all candidate ratings are pre-result reasoning; the economic-capture principle from DISC-025 is applied as the binding design constraint.
