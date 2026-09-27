# GOLD BANK — Forensic Mechanism Audit Record

**Date:** 2026-09-27
**Status:** Completed forensic / read-only audit. No research activation.
**Artifact type:** Governance audit record (conclusions preserved, not a Pine implementation).

---

## 1. Source provenance and identity

* The audited Pine Script source was **owner-supplied in the ChatGPT conversation** (attachment transport unavailable) and is **not currently stored as a repository source file**. No repository path is fabricated for it; no Pine source file was created from memory.
* Source identity as supplied:
  * Pine Script `@version=5`
  * Indicator: `Price Action Concepts [GOLD BANK INDICATOR]`
  * Short title: `GOLD BANKINDICATOR-V1 - Price Action GOLD BANKINDICATOR [1.2.2]`
  * `indicator()` object, not `strategy()`.
* This artifact records conclusions **about** the owner-supplied source. It is not a source-of-truth Pine implementation and must not be treated as one.

---

## 2. Executive verdict

GOLD BANK is a complex descriptive market-structure indicator, not a demonstrated trading strategy or genuinely distinct research mechanism. Its BOS/CHoCH/CHoCH+ constructs are pivot-break and structural-state calculations overlapping existing structural, continuation, reversal, and SMC research families. Order blocks are drawn downstream of that same structure and therefore do not establish an independent mechanism by being displayed as separate zones. Premium/equilibrium/discount are range-location constructions; candlestick patterns are conventional price-geometry descriptions; MTF structure is a filtering/representation layer. "Volumetric order block" terminology materially overstates the data semantics: the source uses TradingView `volume` plus bar-state counters, with no bid/ask volume, aggressor direction, order-book depth, or resting-liquidity data. Two causal-timing problems are material: explicit HTF `request.security(..., lookahead = barmerge.lookahead_on)` for D/W/M/12M high-low references, and future-confirmed pivots whose drawings anchor at the historical pivot location (historical visual-information timing mismatch). A dynamic internal-lookback block is misordered (the `vv >= 1.5` branch captures all later thresholds, so the intended adaptive 10→5 mapping does not operate as written) and its persistent `iLen` makes the behavior path-dependent. Bearish `"Precise"` order-block and weak-low volume-label paths contain suspicious inconsistencies; several advertised modules (FVG inputs, accumulation/distribution inputs, EQH/EQL display, plot-candle/bar-color controls, parts of alert scaffolding) are incomplete or effectively inert. Pattern state can persist up to 50 bars, so displayed state is not an immediate signal. No complete executable strategy is defined (no unique entry, execution price, stop, target, horizon, sizing, costs, overlap policy, control, or outcome). The dominant failure mode is **confluence illusion**: multiple descriptive representations of the same evolving price path presenting as independent confirmations, with substantial discretionary visual-selection/hindsight risk (formal statistical overfitting not claimed as proven).

---

## 3. Component inventory (summary)

| Component | Actual computation | Economic claim | Mechanism class |
|---|---|---|---|
| Swing structure / pivots | Pivot highs/lows requiring future-bar confirmation | Structural turning points | Structural state (descriptive + event) |
| Internal structure | Lower-order pivot-break calculations | Finer structural state | Structural state |
| BOS | Close beyond prior swing extreme | Continuation / buyers overwhelmed sellers (implied) | Breakout / trend continuation |
| CHoCH / CHoCH+ | Break against prevailing structural direction (+refinement layer) | Reversal / shift of control (implied) | Reversal / structural state transition |
| Dynamic/manual lookbacks | Pivot lookback length incl. misordered `vv`-threshold block (10→5 intended, first branch dominates) + persistent `iLen` | Adaptive sensitivity (implied) | Execution/filter construct (defective) |
| MTF structure | Higher-timeframe structural evaluation | Cross-timeframe confirmation (implied) | Cross-timeframe alignment (filter/representation) |
| HTF D/W/M/12M levels | `request.security(..., lookahead_on)` high-low references | Reference levels | Price-location (causal-timing risk) |
| Order blocks (incl. "Precise" bearish branch) | Zones derived downstream of BOS/CHoCH structure | Institutional supply/demand (implied) | Descriptive zone construct; branch inconsistency noted |
| Volumetric order blocks | TradingView `volume` + bar-state counters | Buy/sell activity, accumulation/distribution (implied) | Activity-conditioned display; data semantics overstated |
| Premium / equilibrium / discount | Position of price within a range | Favorable/unfavorable location (implied) | Price-location construct |
| FVG logic | Gap/imbalance detection (inputs present; feature incomplete per audit) | Unfilled-liquidity attraction (implied) | Gap/imbalance (inert as implemented) |
| Candle patterns | Conventional OHLC pattern geometry | Reversal/continuation signal (implied) | Price-geometry description |
| Pivots display, EQH/EQL input, candle/bar-color controls | Display scaffolding (partially inert) | None established | Descriptive |
| Alerts / state machines | Signal/state propagation incl. up-to-50-bar pattern persistence | Timely signals (implied) | Execution/filter construct |
| Accumulation/distribution inputs | Configured inputs, effectively inert in supplied source | Institutional activity (implied) | Inert; no mechanism established |

---

## 4. Causal / repainting findings

**Confirmed material risks:**

* **HTF lookahead:** explicit `request.security(..., lookahead = barmerge.lookahead_on)` for D/W/M/12M references exposes historical values to future information — material historical causal-timing risk.
* **Pivot timing mismatch:** pivots require future-bar confirmation while drawings anchor at the historical pivot location — a signal knowable only later appears at the earlier location (historical visual-information timing mismatch).
* **Persistent state:** pattern state persisting up to 50 bars means displayed state ≠ real-time signal timing.

**Plausible risks (not confirmed as defects):** MTF aggregation timing ambiguity where confirmation bars are not pinned down; alert/historical information-set mismatch where alerts fire on state defined with confirmation lag.

---

## 5. Data-semantics findings

TradingView `volume` (venue-aggregated, non-aggressor-signed) plus bar-state counters are the only activity inputs. No bid/ask volume, no aggressor direction, no order-book depth, no resting-liquidity data exists in the construction. Terms such as "volumetric," "buy/sell activity," "accumulation/distribution," and "liquidity" are therefore economic stories assigned to activity proxies, not measured variables. Institutional/order-block language is not supported by the data as an observable fact.

---

## 6. Implementation defects (material only)

1. **Dynamic lookback ordering** (`vv >= 1.5 ...` through `vv >= 2.0` chain): first branch captures all later thresholds; adaptive 10→5 mapping inoperative as written. Severity: high for the feature (feature dead), mechanism-neutral.
2. **Persistent `iLen`:** path-dependent behavior rather than instantaneous mapping. Severity: moderate (reproducibility/interpretation impact).
3. **Bearish `"Precise"` order-block branch + weak-low volume labels:** suspicious/inconsistent implementation paths. Severity: moderate; discrepancies, not mechanism evidence.
4. **Inert advertised modules:** FVG inputs, accumulation/distribution inputs, EQH/EQL display input, candle/bar-color controls, alert scaffolding portions. Severity: low–moderate (expectation vs behavior mismatch).

No code was modified to fix any defect.

---

## 7. QuantForge overlap / distinctness map

* **DISC-021 Mean Reversion:** no new standalone mechanism; premium/discount or return-to-zone readings do not create one. (B-adjacent; no reopening.)
* **DISC-022 TSMOM:** BOS continuation belongs to the same broader continuation/momentum/breakout family though not identical to the frozen specification. No reopening.
* **DISC-025 Liquidity Sweep/Reversal + SMC/liquidity-sweep family:** CHoCH/reversal/order-block/SMC interpretations overlap the protected family. No distinct mechanism. No reopening.
* **SMC Institutional POI / Idea 2:** strong conceptual overlap, no mechanism-level novelty.
* **Overall:** no A-class (genuinely distinct) mechanism. Components classify as B (same mechanism/extension: BOS/CHoCH/structure), C (combination of known ingredients without new mechanism: the confluence stack), D (information construct without demonstrated mechanism: volumetric labeling), or E (descriptive: premium/discount bands, candle patterns, MTF display, inert modules).

---

## 8. Root-cause failure analysis

*Root causes:* (1) **Confluence illusion** — BOS, CHoCH, OB, FVG, premium/discount, MTF, and candle labels re-describe one evolving price path, so independent-looking confirmations are correlated measurements; live, only the first trigger exists and the rest arrive late or not at all. (2) **No executable strategy defined** — without entry/execution/stop/target/horizon/costs, historical appearance cannot convert into a tradable claim. (3) **Causal-timing defects** (HTF lookahead, pivot anchoring, persistent state) make historical charts show information earlier than any live process could know it.
*Secondary causes:* overstated volume semantics (activity proxies, no aggressor/depth data); dead adaptive-lookback and inert modules (advertised behavior ≠ actual behavior); implementation inconsistencies.
*Amplifiers:* dozens of simultaneous labels, timeframes, optional filters, and parameters enabling discretionary visual selection and hindsight assembly.
*Non-causes:* indicator count as such; Pine as a language; TradingView volume availability (useful descriptively, just not order flow).

---

## 9. Governance disposition

* Research Capacity HOLD — unchanged.
* Active Research NONE; New Candidate NONE; Backtest NONE; Economic Validation NONE; External Research Data NONE; Phase IV NOT AUTHORIZED.
* No candidate created; no experiment executed or authorized; no external-data acquisition; no code modified.
* No closed line reopened (DISC-021/022/025, SMC/POI/Idea 2 all unchanged).
* No Lane B prototype authorized.
* GOLD BANK preserved as an audited descriptive indicator artifact. Conclusion scoped to the supplied indicator as audited — not a claim about every possible use of any component.
* Future sessions must not restart the GOLD BANK investigation via re-labeling, re-parameterization, combination, or visual selection of BOS/CHoCH/OB/FVG/premium-discount/candlestick/MTF variants unless a separately governed and demonstrably distinct mechanism is established and authorized.
* Observation / interpretation / mechanism / opportunity / authorization / state remain distinct.

---

## 10. Preserved follow-up material

None promoted. No component survived as a genuinely distinct mechanism; several items remain *unresolved-but-insufficient* (precise-branch behavior, inert-module intent) and are preserved here as documentation, not as research leads. No IDs assigned. No experiment proposed. No activation.
