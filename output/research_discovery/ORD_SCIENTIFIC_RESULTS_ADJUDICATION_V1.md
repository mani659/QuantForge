# QUANTFORGE — ORD V1.1.0
# INDEPENDENT SCIENTIFIC RESULTS ADJUDICATION V1

## 1. Executive Verdict

**A — SCIENTIFICALLY SUPPORTED.**

The frozen ORD V1.1.0 behavioral hypothesis is scientifically supported by the
completed execution for the three evaluable registered markets — XAUUSD,
XAGUSD, and USATECHIDXUSD — all classified **SUPPORT** under the frozen
protocol's classification rule (Holm-adjusted p < α = 0.05 AND ΔM_obs > 0).

ORD passes its registered behavioral gate and is authorized to advance to the
**separate economic / strategy translation stage** only. This adjudication
establishes a behavioral/statistical continuation result; it does NOT establish
profitability, transaction-cost survival, live tradability, or universality.

BTCUSD was **HALTED** on a data-quality gate (persisted invalid-day fraction
`0.11945205479452055` > `0.10`), contributing no primary verdict. EURUSD is
**NOT REGISTERED / DATA-LIMITED** (excluded at protocol §3 until its
invalid-day data-quality gate is independently resolved, DISC-025) and is not
treated as a failed ORD result.

## 2. Execution Integrity

Adjudication relies exclusively on the completed, verified execution
`EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532` and its
persisted artifacts:

- **State:** journal `state = COMPLETED` (`2026-08-18T14:13:11.135827+00:00`);
  manifest `final_state = COMPLETED`; `missing_artifacts = []`,
  `unexpected_artifacts = []`; directory holds 13 observed artifacts + report.
- **Identity:** protocol V1.1.0 SHA `85263b84…c06`; definition lock
  `b5810540…b30`; entry-script SHA `ab145252…baac`; seed `20260818`, B `10000`,
  L `10`, α `0.05`, `p_terminate`/`halt_fraction` `0.1`, `horizon_min` `120`,
  `min_treatment` `100`; Python `3.11.9`, numpy `2.4.4`, pandas `3.0.2`;
  Git HEAD `a6c62edf…a0` (dirty `True`).
- **Consistency already verified (prior audits, referenced, not re-executed):**
  `ORD_EXECUTION_REPORT_COMPLETENESS_AUDIT_V1.md` (verdict A — REPORT
  RECONSTRUCTABLE); `ORD_EXECUTION_REPORT_RECONSTRUCTION_AUDIT_V1.md` (verdict
  REPORT RECONSTRUCTED FROM PERSISTED ARTIFACTS — NO RERUN); V3 fresh
  implementation audit (PASS); crash-reconciliation audit (PASS).
- **Deterministic consistency check performed for this adjudication** against
  persisted values only: Holm step-down recomputed from the persisted raw
  p-values over the evaluable family reproduces the persisted `p_holm` to
  machine precision (XAUUSD and XAGUSD `0.00029997000299970003`; USATECHIDXUSD
  `0.0004999500049995`); each persisted `classification` matches the frozen rule.
- The partial/crashed execution `a79f58f8…` was NOT used as evidence.

## 3. Registered Scientific Question

> Does a deterministic break of a pre-defined market opening range produce a
> statistically and economically meaningful directional continuation after the
> breakout entry across a multi-market validation universe?

Adjudicated scope: the behavioral/statistical component is in scope; the
registered response is the directional return from the actual entry close over
the 120-minute horizon (protocol §8). Economic meaningfulness is in scope only
insofar as the registered response is that directional return. Actual trading
economics (entry execution, spreads, slippage, stops, exit, expectancy) are
OUT OF SCOPE for this stage. Profitability is NOT established by this
adjudication.

## 4. Market-Level Primary Results

All values are transcribed from persisted `statistics.json`.

| Market | Treatment | Control | ΔM_obs | 95% CI | Raw p | Holm p | Classification |
|---|---:|---:|---:|---:|---:|---:|---|
| XAUUSD | 2184 | 62 | +30.901704157243934 | [23.216857953960513, 36.5353289810984] | 9.999000099990002e-05 | 0.00029997000299970003 | SUPPORT |
| XAGUSD | 2177 | 56 | +71.0428969879628 | [57.840627740888365, 86.95092296030565] | 9.999000099990002e-05 | 0.00029997000299970003 | SUPPORT |
| USATECHIDXUSD | 839 | 25 | +49.51962303222475 | [33.459428586263954, 79.01079869236179] | 0.0004999500049995 | 0.0004999500049995 | SUPPORT |
| BTCUSD | — (HALTED) | — | — | — | — | — | HALTED — no primary result |
| EURUSD | — | — | — | — | — | — | DATA-LIMITED / NOT REGISTERED |

- **Primary statistic:** `ΔM = Median(Response_treatment) − Median(Response_control)`;
  sign convention positive = treatment continuation stronger than control. All
  three evaluated markets are positive.
- **Median convention:** frozen (odd = middle; even = mean of two central);
  identical for observed and bootstrap statistics. No raw-data recomputation —
  values are the persisted observed statistics.
- **BTCUSD:** halted before primary inference (invalid-day fraction
  `0.11945205479452055` > halt threshold `0.1`); no bootstrap/null arrays, no
  p-value, no classification. It is neither SUPPORT nor CONTRADICTED nor
  INCONCLUSIVE — it is a data-quality HALT.
- **EURUSD:** NOT REGISTERED / DATA-LIMITED; its absence is not a failed ORD
  result.
- **Low-control reliability flag (§13):** not triggered — every evaluable
  market has `B_valid = 10000 ≥ 1000`.

## 5. Holm / Family-Level Inference

- **Primary family:** the evaluable validation markets XAUUSD, XAGUSD,
  USATECHIDXUSD (BTCUSD halted pre-inference at §20; EURUSD excluded at §3).
  Evidence-limited and halted markets contribute no primary verdict; no
  post-result market removal occurred.
- **Holm step-down at α = 0.05** over the exact market-level raw p-values
  (9.999e-05, 9.999e-05, 4.9995e-04). Recomputed Holm values match persisted
  values exactly: XAUUSD `0.00029997000299970003`, XAGUSD
  `0.00029997000299970003`, USATECHIDXUSD `0.0004999500049995`.
- All three Holm-adjusted p-values are far below α = 0.05; the family-wise
  decision is robust to the tightest comparator.
- NULL/p construction: recentered-bootstrap null with inclusive `≥` count and
  `p = (1+count)/(1+B_valid)`; B = 10000, `B_valid = 10000` for each evaluated
  market (all replicates valid); p-values are the persisted values, verified
  consistent in the prior completeness audit (null exceedance counts 0, 0, 4).
  No distribution was regenerated for this adjudication.

## 6. Cross-Market Interpretation

- **Sign consistency:** 3/3 evaluable markets positive — unanimous.
- **Number supporting / contradicted / inconclusive:** 3 SUPPORT / 0
  CONTRADICTED / 0 INCONCLUSIVE.
- **Asset-class breadth:** two precious metals (XAUUSD, XAGUSD) and one US
  technology equity index (USATECHIDXUSD) — the only crypto market registered
  (BTCUSD) was halted on the data gate, so no crypto-class confirmation exists.
- **Instrument-specific vs asset-class vs cross-market:** the evidence shows a
  directional continuation effect in three instruments spanning two broad
  asset-classes; this supports **asset-class-level breadth (2 classes)**, with a
  partial hint toward **cross-market** reach. It does NOT reach forced
  universality.
- **Not justified:** universal generalization from "several markets positive."
  The universe is protocol-frozen (4 registered; 3 evaluable); the halt of
  BTCUSD and the data-limited status of EURUSD mean the evidence is
  instrument/asset-class support, not a universal market law.
- Raw bp magnitudes across markets (e.g., XAGUSD +71.04 vs XAUUSD +30.90) are
  NOT compared as economically equivalent.

## 7. Chronological Stability

Persisted descriptive halves and year-level ΔM, used ONLY as stability evidence
(they cannot rescue, overturn, or upgrade any primary verdict):

| Market | First-half ΔM | Second-half ΔM | Year-level ΔM |
| --- | ---: | ---: | --- |
| XAUUSD | 33.70118241915733 | 28.05587749143095 | 2021–2026 all positive (min 19.12 in 2023, max 34.63 in 2026) |
| XAGUSD | 67.32300568694681 | 73.98683077059532 | 2021–2026 all positive (min 48.67 in 2023, max 85.99 in 2025) |
| USATECHIDXUSD | 36.80343550963096 | 75.80348755451857 | 2023–2026 all positive (min 33.84 in 2024, max 77.24 in 2025) |

Every half and every persisted year is positive in every evaluated market —
stability evidence is uniformly consistent with the primary result but is
recorded as descriptive only.

## 8. Secondary Firewall

Persisted secondary metrics classified as **descriptive only**:

- **Invalidation/eligibility fraction (per treatment):** XAUUSD
  `0.8891941391941391`, XAGUSD `0.9085898024804777`, USATECHIDXUSD
  `0.8927294398092968`.
- **MFE-from-entry (median treatment):** XAUUSD `15.46846`, XAGUSD `30.66742`,
  USATECHIDXUSD `26.23131`.
- **Range-normalized return (median treatment):** XAUUSD `-0.022362`,
  XAGUSD `-11.106685`, USATECHIDXUSD `0.016468`.
- **Directional composition:** XAUUSD long/short treatment 1092/1092,
  controls 28/34; XAGUSD 1093/1084, 28/28; USATECHIDXUSD 437/402, 11/14.
- **Event frequency** and **chronological stability** as persisted (§4, §7).

These are recorded, not adjudicated into the verdict. They cannot and do not
alter the primary classifications; in particular the primary response is the
unconditional 120-minute return from the entry close and is not truncated by
invalidation (protocol §7).

## 9. Established Claims

Only claims directly supported by the registered primary results:

- For the frozen ORD V1.1.0 object (pre-defined opening-range close-break,
  entry at the breakout-close, 120-minute horizon, continuation-direction
  control), the completed execution shows:
  1. a **positive directional continuation** differential vs control in XAUUSD
     (ΔM = +30.90 bp, Holm p = 3.00e-04);
  2. a **positive directional continuation** differential vs control in XAGUSD
     (ΔM = +71.04 bp, Holm p = 3.00e-04);
  3. a **positive directional continuation** differential vs control in
     USATECHIDXUSD (ΔM = +49.52 bp, Holm p = 5.00e-04);
  4. a consistent positive sign across all evaluable markets, halves, and
     persisted calendar years (stability evidence);
  5. the **behavioral-level existence** of the directional continuation
     phenomenon in these instruments under this experiment — i.e., a
     statistically and directionally meaningful open-range-break continuation
     at the response level (behavioral / in-scope economic meaningfulness of
     the registered response).

## 10. Not Established

Distinctly NOT established by this experiment:

- **Profitability** — not computed, not claimed.
- **Transaction-cost survival** — spreads, slippage, commissions, and friction
  economics not evaluated at this stage.
- **Live tradability** — no entry/stop/exit/target/sizing operationalization
  tested.
- **Universality** — no universal market law; only protocol-frozen registered
  markets adjudicated.
- **Institutional intent / market-manufacturing explanations** — mechanism is
  not identified by this statistical object.
- **Cross-era / forward robustness** beyond the persisted in-sample stability —
  no out-of-sample claim.
- **Hypothesis validation outside the registered universe** — BTCUSD
  unvalidated (halted); EURUSD unvalidated (excluded).

Statistical support must not be conflated with a profitable strategy.

## 11. Economic Boundary

> A positive ORD scientific result does NOT authorize an EA, live trading,
> profitability claim, or demo deployment.

Because ORD is scientifically SUPPORTED, the next stage becomes:

**SEPARATE ECONOMIC / STRATEGY TRANSLATION** — where entry execution, observed
spreads, slippage, stops, exits, expectancy, and forward robustness will be
tested. This is a distinct, separately governed stage.

(Contingency, for the record: if the protocol had been CONTRADICTED → CLOSE THE
ORD RESEARCH LINE without rescue by changing the opening window, entry,
horizon, or filters; if INCONCLUSIVE → record the exact reason and return to
governance before any rerun. Neither applies.)

## 12. Closed-Line Independence

Confirming ORD remains independent of all closed research lines — no closed
semantics are reused as ORD rescue filters, and this adjudication does not
reopen them:

- **Mean Reversion (DISC-021):** closed economically non-viable. ORD response is
  signed by break direction (continuation object); no reversion response, no
  displacement/recoil machinery (protocol §24).
- **Fixed 12/1 TSMOM (DISC-022):** closed not-promotable. ORD is intraday,
  event-driven, session-structure; no rolling lookback, no drift benchmark
  (protocol §24).
- **Session-Anchored Range Expansion (DISC-024):** closed contradicted. ORD
  tests close-break → directional continuation (direction object), not
  compression → range size (volatility object) (protocol §24).
- **Liquidity Sweep / Reversal (DISC-025):** closed (behavior supported,
  translation non-viable). ORD uses the current session's opening range,
  close-break, no rejection/confirmation-lag, entry-anchored trend-style
  response; it is not a repaired sweep (protocol §24).
- **H01 Equity Track A / DISC-023:** separate daily-frequency equity program;
  untouched.

Closed-line results may inform methodology, but cannot be used as rescue
filters for ORD.

## 13. QuantForge End-Goal Relevance

Interpreted through the actual QuantForge pipeline:

**behavior → cross-market scientific validation → economic translation →
cost-aware viability → demo/forward monitoring → live consideration.**

- This adjudication completes the **behavior → cross-market scientific
  validation** transition for ORD V1.1.0.
- The result does NOT stop at "statistically significant"; the next pipeline
  leg is **economic translation**, then **cost-aware viability**.
- It does NOT jump from support to "profitable bot." A supported behavioral
  result is a gate-pass, not a go-live.
- The BTCUSD halt and EURUSD data-limitation remain unresolved data-quality
  items for any subsequent stage; no market may be added because of results.

## 14. Research-Line Governance Decision

**Decision: A — SCIENTIFICALLY SUPPORTED.**

ORD passes its registered behavioral gate and may advance to a separate
economic/strategy translation stage.

Basis: 3/3 evaluable registered markets classified SUPPORT under the frozen
rule (Holm p < 0.05 AND ΔM_obs > 0), family-wise Holm adjustment passed at
α = 0.05, uniformly positive stability descriptives, valid execution (state
COMPLETED), and fully preserved scientific artifacts. BTCUSD halted (no
verdict) and EURUSD not registered (no verdict) do not contradict.

## 15. Exact Next Legitimate Task

**SEPARATE ECONOMIC / STRATEGY TRANSLATION OF ORD V1.1.0** — the design and
execution of the economic translation stage that tests entry execution,
observed spreads, slippage, stops, exits, expectancy, and forward robustness
behind the frozen ORD object. This is a new, separately governed stage and must
be designed (not run) only on authorization following this adjudication.

## 16. Prohibited Follow-Up

Do NOT, on the strength of this adjudication:

- rerun ORD; reprocess M1 data; regenerate bootstrap/null arrays;
- modify any execution artifact, protocol, runner, or execution infrastructure;
- change any parameter (opening window, entry, horizon, filters, thresholds);
- add or remove markets; authorize EA/demo/live deployment;
- build an EA or introduce ML as a rescue;
- design the economic translation within this adjudication (no new research
  decision is made here);
- reopen DISC-021/022/023/024/025 or rescue/tune ORD in any way;
- use the partial/crashed execution as evidence;
- claim profitability or universality.

## 17. Integrity

- Adjudication is strictly READ-ONLY: no execution artifact, protocol, runner,
  infrastructure, parameter, or closed-line record was modified; no original M1
  dataset was reprocessed; no bootstrap/null/event distribution was regenerated.
- All scientific values quoted are transcribed from persisted completed
  execution artifacts (`statistics.json`, `metadata.json`, manifests, journal)
  or recomputed only deterministically and verified to match persisted values
  (Holm, classifications).
- The only new artifact is this adjudication:
  `output/research_discovery/ORD_SCIENTIFIC_RESULTS_ADJUDICATION_V1.md`.
- The completed execution remains COMPLETED / SCIENTIFICALLY VALID; the
  reconstructed report and its reconstruction audit remain authoritative
  presentation artifacts.
- Independent adjudication of the same completed evidence was previously
  recorded at
  `output/research_discovery/ORD_V1_1_0_SCIENTIFIC_RESULTS_ADJUDICATION_V1.md`
  (SCIENTIFICALLY SUPPORTED); this adjudication independently re-confirms that
  verdict from the persisted evidence.