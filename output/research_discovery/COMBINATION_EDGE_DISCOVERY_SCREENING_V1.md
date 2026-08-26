# QUANTFORGE — COMBINATION EDGE DISCOVERY
# GOVERNANCE / SCIENTIFIC SCREENING V1

## 0. Identity and Mode

- **Task:** READ-ONLY governance and scientific screening of whether previously established research objects can legitimately form a NEW combination edge.
- **Control set:** `docs/SESSION_HANDOFF.md` (updated 2026-08-17); `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-001…025); `research/knowledge/RESEARCH_TIMELINE.md` (§1–18); finalized adjudication artifacts and protocols for H01 Equity (DISC-023), Liquidity Sweep / Reversal (DISC-025), Session-Anchored Range Expansion (DISC-024), Mean Reversion (DISC-021), TSMOM (DISC-022).
- **Mode:** no execution, no backtest, no protocol, no code, no new experiment. Only repository-established facts are used; nothing is assumed from historical existence alone.

---

## 1. Executive Verdict

**B — COMBINATION RESEARCH IS NOT YET JUSTIFIED.**

No candidate combination survives the governance screen. The repository contains only two potentially reusable *behavioral* components — the H01 Equity volatility-response object and the Liquidity-Sweep reversal event — and the only serious pairing of them (directional liquidity event + pre-existing volatility context) **fails the special review**: H01's validated object is a post-event volatility *response*, not a validated pre-entry state variable; its universe (daily US equity) does not overlap the M1 event markets; transplanting a "volatility-tercile state" would be a **new unvalidated variable**, not a combination of established objects; and the natural motivation is rescue of the failed sweep translation. Every other pairing involves a closed or contradicted component (MR, TSMOM, Session Range) and is rejected. **Return to Tradeable Edge Discovery Screening** — the combination route is not justified before a new independent candidate exists.

---

## 2. Current Validated Research Inventory

| Object | DISC | Scientific object | Validated in | Freq/Universe | Timing of its observable | Economic status | Line status |
|---|---|---|---|---|---|---|---|
| **H01 Equity** | 023 | Classic negative-shock volatility-response asymmetry: magnitude-matched negative vs positive daily shocks → forward ΔlnRV response, stratified by pre-shock volatility tercile | EQTECH_L1/L2 SUPPORT (NASDAQ-family, two eras); EQBROAD_L2 SUPPORT (SP500+DJIA); EQBROAD_L1 EVIDENCE-LIMITED (`sp` only) | Daily; US equity (HPD `sp`, FRED NASDAQ100/NASDAQCOM/SP500/DJIA) | Shock & pre-shock tercile known at shock-day close; the validated claim is about the **forward 5-day vol response** (post-event) | Behavioral support; no economic translation | **OPEN** (narrowed US-equity program) |
| **Liquidity Sweep / Reversal** | 025 | Sweep of prior Asian extreme → wick rejection → micro-structural confirmation → larger 120-min directional excursion than control | XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD SUPPORT; EURUSD DATA-LIMITED | M1; metals/index-CFD/crypto | Event (confirmation) known at its M1 close; Asian reference known before London/NY | Minimal translation ECONOMICALLY NON-VIABLE (gross-negative, all 4 markets) | **CLOSED** (trading line); behavioral information preserved |
| **Session Range Expansion** | 024 | Pre-session compression → cash-session range expansion | **CONTRADICTED** on USATECHIDXUSD | M1 | Pre-session state known pre-cash | n/a | **CLOSED** — contradicted |
| **Mean Reversion** | 021 | Displacement → recoil → persistence | Narrow XAGUSD asymmetry statistically real; economically non-viable under observed costs | M1/tick | n/a | NON-VIABLE | **CLOSED** |
| **TSMOM 12/1** | 022 | Fixed 12/1 trend signal incremental over drift | Historical incremental positive; **contemporary contradicted**; NOT PROMOTABLE | Daily/monthly; 28-market HPD + 5-market contemporary | Signal known at month end | Contemporary NOT CONFIRMED | **CLOSED** — not promotable |

**Only repository-established facts used.** In particular, TSMOM is recorded as *not validated as a contemporary predictor* (its contemporary incremental sign was opposite the historical) and therefore cannot serve as a favorable regime filter; Session Range is contradicted; Mean Reversion is closed as economically non-viable.

## 3. Combination Eligibility Rules

A combination is eligible only if: (1) each component measures a genuinely different dimension; (2) each is known at or before the decision time; (3) the interaction rationale predates the observed economic outcomes; (4) no favorable-market selection from results; (5) no threshold tuning from a failed strategy; (6) no restatement of one component in other words; (7) a genuinely new scientific/economic question results. A combination is a **NEW research object** with its own question → definition → pre-registration → audit → execution → adjudication; it is never "Sweep V2", "H01 rescue", or a patch.

## 4. Orthogonality Analysis

Dimension classification of established objects:

- **H01 Equity** → volatility state / volatility-response dimension (daily, response-based).
- **Liquidity Sweep** → directional liquidity / auction-structure dimension (M1, event-based, directional).
- **Session Range** → volatility-state dimension (pre-session compression) — same family as H01, and contradicted.
- **Mean Reversion** → mean-reversion dimension — closed.
- **TSMOM** → trend/momentum dimension — closed, contemporary unvalidated.

Only H01 (volatility) and Sweep (directional liquidity) are on *different* dimensions and both carry established positive behavioral content. Any other pairing is either same-dimension (H01 + Session Range = volatility + volatility), or contains a closed/contradicted component (Sweep+TSMOM, Sweep+MR, H01+TSMOM, H01+MR, Sweep+Session Range). **No correlation or outcome statistics were computed** — this is a conceptual screen, as required.

## 5. Time-Availability Analysis

- **Sweep event:** known at the confirmation M1 close; Asian reference known before London/NY. Clean pre-decision timing. ✓
- **H01 pre-shock volatility tercile:** known before the shock day's outcome (constructed from prior RV) — *in principle* a pre-decision variable. **However**, the *validated* H01 claim is the post-event response asymmetry; the tercile itself was never validated as a predictor of anything beyond that response. ✓ timing, ✗ validated-predictor status (see §11).
- **Session Range state:** known pre-cash, but contradicted as a predictor → unusable as a favorable filter.
- **TSMOM signal:** known at month end, but contemporary direction contradicted → unusable as a validated state.
- **Prohibited timing patterns confirmed absent from every serious candidate considered:** no component depends on eventual MFE, full-session future statistics, post-entry responses, or win/loss knowledge.

## 6. Economic Complementarity

The only conceptually legitimate economic role found: **directional liquidity trigger (sweep) + volatility context (prior vol state)** — "structural event + volatility regime," a recognized combination class. But complementarity *in the abstract* is not sufficient: the volatility-context component must be an *established, pre-decision, transferable* object. H01's established object is not transferable as a live state variable (daily US-equity response object; no M1 derivation exists in the repository), so the concrete pair lacks an established second component. Every other pairing fails at the component level (closed/contradicted). No combination is selected "merely because one failed standalone strategy could be filtered by another."

## 7. Closed-Line Rescue Audit

Explicitly tested and rejected rescue patterns:

- **"Sweep failed because stops were too frequent, so add H01/volatility context."** — Outcome-driven rescue unless an independently justified pre-existing hypothesis exists. The generic "liquidity events differ across vol regimes" rationale is real but was never registered before the sweep's economic failure; its natural motivation here is removing the losing trades. **Rejected as stated; see §11 for the special review.**
- **"Session expansion failed, so use sweep direction as the filter."** — Both lines closed/contradicted; combining two non-validated-trading objects does not create validity. **Rejected.**
- **"Mean reversion failed, so use TSMOM to avoid bad regimes."** — Both closed; TSMOM contemporary contradicted. **Rejected.**
- **"TSMOM historical was positive, so use it as a regime filter."** — Contemporary contradiction recorded (DISC-022); the historical panel is not a validated contemporary filter. **Rejected.**

Rule applied: a closed line contributes to a NEW combination only if the combination is justified independently of its failed economic result. No candidate meets this bar.

## 8. Candidate Combination 1 — "Volatility-Contextualized Liquidity Reversal"

- **Components:** (A) confirmed sweep-reversal event (directional liquidity, M1); (B) prior volatility state (H01-family tercile).
- **Independent rationale:** liquidity events plausibly behave differently across volatility regimes (different dimensions: auction structure vs volatility state).
- **Information timing:** (A) at confirmation close; (B) before the event (prior RV). Both pre-decision in principle.
- **Market scope:** nominally the four sweep markets; but (B)'s established object lives in daily US equity — no overlap beyond USATECHIDXUSD, and (B) would have to be re-derived on M1 metals/crypto as a **new variable**.
- **Economic rationale:** the failed translation's losses concentrated in stop-outs; volatility conditioning *might* separate regimes. This is precisely the rescue pattern unless the interaction rationale predates the failure — it does not.
- **Rescue risk:** HIGH — the natural construction is "filter the failed sweep."
- **New scientific question:** would exist, but it would test a *new* volatility-state variable, not H01's validated response object.
- **Verdict:** **REJECTED** (see §11 special review; fails component-establishment and rescue-audit tests).

## 9. Candidate Combination 2 — "Trend-Regime-Conditioned Liquidity Reversal"

- **Components:** (A) confirmed sweep-reversal event; (B) TSMOM-style trend state.
- **Independent rationale:** trend regime could in principle modulate reversal success — a different dimension (trend vs liquidity).
- **Information timing:** (B) known at month end; (A) intraday — both pre-decision, but at very different frequencies.
- **Market scope:** the contemporary TSMOM panel and the sweep panel share markets (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD), but TSMOM's contemporary incremental result was **negative** — the component is not validated in the era that would matter.
- **Economic rationale:** none independent — the only motivation is conditioning the failed sweep.
- **Rescue risk:** HIGH — closed-line component (DISC-022), contemporary contradicted.
- **New scientific question:** would rest on an unvalidated component.
- **Verdict:** **REJECTED** — component (B) is not established as a favorable filter; using it is closed-line rescue.

## 10. Candidate Combination 3 — "Volatility-State Cross-Validation"

- **Components:** (A) H01 volatility-response state; (B) Session-Range compression state.
- **Independent rationale:** none beyond both being volatility-family measures.
- **Information timing:** both pre-decision in principle.
- **Market scope:** unclear — H01 is daily US equity; Session Range is M1 USATECHIDXUSD.
- **Economic rationale:** none; (B) is **contradicted** and cannot act as a favorable filter.
- **Rescue risk:** HIGH — reviving a contradicted object through combination.
- **New scientific question:** redundant — both components measure volatility state (orthogonality rule 6: restatement in different words).
- **Verdict:** **REJECTED** — same-dimension redundancy and a contradicted component.

## 11. H01 + Liquidity-Structure Special Review

The most interesting potential combination — **directional liquidity event + pre-existing volatility context** — is examined cleanly, per the mandate not to assume suitability:

- **Timing:** H01's *pre-shock volatility tercile* is in principle a pre-entry state (constructed from prior RV, known at shock-day close). ✓
- **Market overlap:** H01 Equity's validated universe is **daily US equity** (HPD `sp`; FRED NASDAQ100/NASDAQCOM/SP500/DJIA). The sweep's validated universe is **M1 metals/index-CFD/crypto**. Overlap is essentially limited to USATECHIDXUSD (one market) — insufficient for a multi-market combination study.
- **Directionality:** H01's validated object is a volatility *response asymmetry* (forward ΔlnRV), which carries **no price-direction claim**; the sweep event is directional. The two objects measure different things, but H01's object is not a directional state usable to steer the sweep trade.
- **Definitional suitability as a live state variable:** **NO.** H01's established claim is the post-event response; the tercile state was never validated as a standalone predictor, and no M1-frequency derivation of it exists anywhere in the repository. Using it on the sweep markets would require constructing a *new* variable and *new* validation — that is a new hypothesis, not a combination of established objects (eligibility rules 1 and 3 fail).
- **Rescue risk:** the combination is the obvious post-hoc response to the sweep's economic failure ("volatility context removes the losing trades") — prohibited unless independently justified pre-outcome; it is not on record anywhere before the failure.
- **Conclusion:** **H01 is NOT suitable as a pre-entry state variable for a new economic hypothesis at this time.** The combination is rejected cleanly. (This does not foreclose a *future* hypothesis that conditions a new independent candidate on volatility state — but that would be a fresh definition, not a combination of H01 + Sweep.)

## 12. ML Position

No ML is used to discover or fit any combination in this task. Because no combination survives the screen, there is currently **no authorized role for ML as a regime classifier** attached to a combination hypothesis. ML remains a possible future *methodology* (e.g., regime classification) only after a deterministic combination or candidate hypothesis is established through the normal definition → pre-registration → audit chain; it is not itself the edge and not a rescue path for any closed line.

## 13. Overall Governance Decision

**B — COMBINATION RESEARCH IS NOT YET JUSTIFIED.**

- Only two established behavioral components (H01 Equity, Sweep) sit on different dimensions with positive content; their pairing fails the special review (no validated pre-entry state variable, no market overlap, rescue risk).
- All other pairings contain a closed or contradicted component.
- No candidate satisfies the seven eligibility rules; no candidate clears the closed-line rescue audit.
- Per the final principle, the output is deliberately **small**: no combination earns a new economic research stage now.

## 14. Exact Next Legitimate Task

> **TRADEABLE EDGE DISCOVERY SCREENING** — return to screening a new, independent candidate with an explicit path from behavior → economics → trading implementation. Combination research is not justified until the repository contains at least two *established, pre-decision, transferable* behavioral components on different dimensions — which today it does not.

If and only if a future candidate emerges and a genuinely independent second component later becomes established, a fresh combination screen may be re-run at that time.

## 15. Prohibited Follow-Up

- Any economic test of the three rejected combinations (or variants of them).
- Any "Sweep V2 / H01 rescue / Session Range rescue / combination-as-patch" framing.
- Any retesting of the failed sweep translation's alternatives.
- Any use of TSMOM, Mean Reversion, or Session Range as a favorable filter.
- Any ML fitting of a combination, now or until a deterministic hypothesis exists.
- Any reopening of closed lines (DISC-021/022/024/025) or of H01-broad.
- Any market selection, threshold tuning, or outcome-derived rationale.

## 16. Integrity

Strictly read-only. The only new repository artifact is this screening. No protocol, no code, no experiment, no governance-file modification, no data change, no candidate selected. All facts are repository-established (DISC-001…025, handoff, timeline); no correlation or outcome statistic was computed; conceptual judgments are flagged as governance-stage reasoning.
