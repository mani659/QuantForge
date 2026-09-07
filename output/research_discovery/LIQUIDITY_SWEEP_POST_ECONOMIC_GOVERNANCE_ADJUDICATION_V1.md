# QUANTFORGE — LIQUIDITY SWEEP / REVERSAL
# POST-ECONOMIC TRANSLATION GOVERNANCE ADJUDICATION V1

## 0. Identity

- **Audit object:** `LIQUIDITY_SWEEP_STRATEGY_ECONOMIC_TRANSLATION_V1.md` (first economic translation of the adjudicated sweep/reversal behavior).
- **Control set:** economic translation artifact; `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_SCIENTIFIC_ADJUDICATION_V1.md`; `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_EVENT_STUDY_PROTOCOL_V1.md` (v1.2.0); `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_FINAL_CLEARANCE_AUDIT_V2.md` (PASS); `docs/SESSION_HANDOFF.md`; `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-021…024); `research/knowledge/RESEARCH_TIMELINE.md`.
- **Mode:** STRICT, READ-ONLY governance adjudication. No recomputation, no new backtest, no alternative testing, no EA, no demo/live.

---

## 1. Executive Verdict

**BEHAVIORALLY SUPPORTED / ECONOMICALLY NON-VIABLE (registered minimal translation) — RESEARCH LINE CLOSED.**

The behavioral discovery is preserved and real: the sweep → rejection → confirmation phenomenon is statistically supported in all four evaluable markets (adjudication unchanged). The first minimal executable translation — confirmation-close entry, structural sweep-extreme stop, 120-minute-horizon-close exit, fixed notional — is **gross-negative before costs in every market, every year, and both chronological halves**; no market, no year, no half is positive. The failure mechanism is a **TRANSLATION FAILURE (B)**: the validated excursion is anchored at the Asian level and the registered mapping cannot capture it, with costs secondary. Under the strict alternative-selection rule (§8), **no alternative translation has a justification that predates the economic result and derives from the frozen behavioral object alone** — therefore **no new economic protocol is authorized**, and the candidate line is **CLOSED** with the discovery preserved in the record. The next legitimate task is a return to **Tradeable Edge Discovery Screening** for a new, independent candidate.

---

## 2. Behavioral Evidence (preserved)

Established by the frozen v1.2.0 experiment and its independent adjudication (unchanged by this stage):

- XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD — SUPPORT (Holm-adjusted p = 3.9996e-04 < 0.05; ΔM_obs > 0; CIs far from zero).
- The behavior: a strict breach of the prior Asian-session extreme → wick rejection → deterministic micro-structural confirmation → statistically larger 120-minute directional excursion (MFE) from the swept Asian level than the rejected-sweep control group.
- Cross-mechanism breadth: precious metals (2), equity-index CFD (1), crypto (1) — preliminary Level 3; FX untested (EURUSD data-limited).

This stage did not touch the behavioral protocol, event definitions, or adjudication.

## 3. Economic Translation Result (verified from the artifact)

| Market | Trades | Gross median (bp) | Win rate | PF | Stop-out | Net A+0 med (bp) | Every year negative | Both halves negative |
|---|---|---|---|---|---|---|---|---|
| XAUUSD | 1517 | −5.34 | 21.9% | 0.93 | 76.5% | −7.16 | YES | YES |
| XAGUSD | 1507 | −11.63 | 23.0% | 0.97 | 75.5% | −23.43 | YES | YES |
| USATECHIDXUSD | 972 | −5.04 | 19.2% | 0.86 | 79.5% | −6.14 | YES | YES |
| BTCUSD | 1941 | −11.82 | 26.5% | 1.11* | 70.3% | −27.48 | YES | YES |

\* BTCUSD gross *mean* +1.9 bp and PF 1.11 (right-skewed tail), but the *median* is −11.8 bp and every year/half is negative — not evidence of viability.

Baseline integrity confirmed: registered before computation; entry = confirmation close; direction = reversal side; stop = frozen sweep-candle extreme (no tick/pip buffer); exit = 120-min horizon close; fixed notional; observed MT5 per-minute median bid/ask spreads (exact-minute ≥ 98.3% of lookups); dev/OOS split by first/last 50% of event days; no optimization, no parameter search, no selection.

## 4. Failure Mechanism

**B — TRANSLATION FAILURE** (stated strictly from the report's evidence):

- **Not A (cost failure):** the gross median is negative **before any cost** in all four markets (XAUUSD −5.3, XAGUSD −11.6, USATECHIDXUSD −5.0, BTCUSD −11.8 bp). Observed round-trip costs (Model A: 1.05–16.77 bp) worsen the result but are not the binding constraint. Cost failure is rejected.
- **B (translation failure):** the underlying excursion is present — median MFE from the Asian level is 23.0–55.8 bp and the median residual from the confirmation close is 17.8–42.7 bp — but the mapping converts it into losses: the confirmation-close entry sits 4.7–13.2 bp beyond the Asian level; the structural sweep-extreme stop is hit in 70–80% of trades (the excursion peaks then reverts through the stop); and the 120-minute *close* exit captures the close, not the extreme. The failure is fully explained by the entry/stop/exit mapping, with costs secondary.
- **C (behavioral failure) not established:** the evidence shows the *mapping* fails, not that the phenomenon cannot be exploited by any directional execution. Whether a level-anchored capture could work remains **unknown** (untested) — and, per §8, that unknown does not authorize a rescue.

## 5. Cross-Market Disposition

The same economic failure occurs across **all four** economically evaluated markets with the same signature: negative gross median sign, PF ≈ 0.86–0.97 gross (1.11 BTCUSD with negative median), stop-out 70–80%, temporal stability of the failure (every year, both halves), and cost sensitivity that is real but not decisive. This is a **structurally weak implementation across markets**, not a weakness confined to one instrument. Raw bp magnitudes were not compared as economically equivalent; the verdict rests on sign, PF, stop-out behavior, temporal stability, and cost non-bindingness — all uniform.

## 6. EURUSD Disposition

Preserved exactly: **DATA-LIMITED / NOT ADJUDICATED** (16.96% invalid-day fraction > 10% gate → halt before inference). It is not an economic failure, not a hypothesis result, and it remains excluded from all economic work until its data-quality operationalization is separately resolved.

## 7. Behavioral vs Economic Boundary

- **Not contradictory:** a real behavioral phenomenon can exist while a chosen execution mapping is bad. The negative economic translation does not retroactively change the behavioral protocol or adjudication.
- **Established:** (1) the behavioral phenomenon is statistically supported (Holm-corrected, 4 markets, 3 mechanisms); (2) the registered minimal translation is economically non-viable (gross-negative, all markets/years/halves, confirmed by observed spreads).
- **Rejected:** the hypothesis that *this specific minimal mapping* is an economically viable trading implementation.
- **Unknown:** (1) whether any other executable mapping could capture the validated excursion after realistic costs; (2) whether the behavior is exploitable in FX (EURUSD untested); (3) universality — never claimed, still not claimed.

## 8. Research-Line Decision

**CLOSED** (candidate trading line), with the behavioral discovery preserved and recorded.

Rationale against the three options:

- **C — ONE NEW ECONOMIC PROTOCOL:** NOT authorized. Per the strict selection rule (§9 of the mission), an alternative may be authorized only if its scientific/market-mechanics justification existed **before** the economic result and derives from the frozen behavioral object. Examination of each candidate: **next-bar-open entry** — a generic fill-realistic refinement, not derivable from the object, and would not address the mechanism (entry too late relative to the level); **limit entry at the Asian level** — a different trading concept that requires entering at the level during any sweep (treatment or control) and was never part of the frozen event structure or its direction logic; **Asian opposite-boundary target** — a hypothesis about *where* the reversal ends, not registered in the frozen protocol, generated in response to the close-exit failure; **structural trailing exit** — a generic exit-management technique, not derived from the object. **None** was registered, justified, or derivable before the failure; each would be selected because of the observed PnL pattern. No alternative is authorized.
- **A — CLOSE vs B — OPEN/UNRESOLVED:** the strict rule and the mission's final principle ("if no [pre-existing alternative], close the line and move to the next candidate") govern. The minimal-translation failure, uniform across markets/years/halves and structurally explained, is sufficient evidence that this behavior, under the project's intended trading model and governance, has no currently authorized executable path. Keeping the line OPEN with no authorized question (B) would leave a permanently unresolvable state; the honest disposition is a formal close with the discovery archived — the same treatment as the project's other adjudicated closed lines (DISC-021, DISC-024), where negative/contradictory evidence is preserved as a permanent discovery, not discarded.

## 9. Alternative-Selection Governance

- **Prohibited, explicitly:** changing the confirmation definition; ATR/percentage/buffer-adjusted stops; changing the horizon; selecting a better-performing target; selecting XAUUSD because it is the discovery market; selecting only higher-PF markets; optimizing costs or execution timing; merging alternatives. Any such change requires a new, outcome-blind, separately pre-registered economic protocol — and none is authorized by this adjudication.
- **Recovery of the behavioral discovery:** the finding "sweep → rejection → confirmation precedes larger directional excursions" is a legitimate, complete scientific result and is preserved as such; it does not license any trading translation by virtue of being real.

## 10. Prohibited Rescue

No parameter rescue, no post-hoc alternative, no demo/live, no EA, no ML/K-means/HMM, no confluence, no merging with or revival of closed lines (Mean Reversion DISC-021, TSMOM DISC-022, H01/H01 Equity DISC-023, Session-Anchored Range Expansion DISC-024). The economic failure of the baseline does not reopen the behavioral protocol; the behavioral support does not reopen the economic line.

## 11. Exact Next Legitimate Task

> **CLOSED → Return to TRADEABLE EDGE DISCOVERY SCREENING** and screen a new, independent candidate, with this line's record complete: behavioral SUPPORT ×4 (EURUSD data-limited) and economic NON-VIABLE baseline (translation failure, gross-negative before costs in all four markets), closure adjudicated under the strict alternative-selection rule.

Before new screening, the discovery database should register this line's permanent record (behavioral discovery + economic non-viability + closure), consistent with DISC-021/024 treatment. No demo, live, or alternative-translation work is authorized by anything in this adjudication.

## 12. Integrity

Strictly read-only. The only new repository artifact is this adjudication. No recomputation, no backtest, no alternative test, no EA, no governance-file modification. The economic translation artifact, behavioral protocol, adjudication, clearance audits, and closed-line records are untouched. The pipeline principle is preserved: behavioral discovery → cross-market validation → economic translation → cost-aware validation → demo → monitoring → live; the sweep/reversal line exits this pipeline at the economic-translation stage with a negative result, as a complete and honest research outcome.
