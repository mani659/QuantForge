# QUANTFORGE — H01 EQUITY REPLICATION — RESEARCH DISCOVERY & SCREENING V1

**Track:** A — Multi-market equity replication of the classic volatility-response asymmetry
**Type:** Discovery / screening ONLY. Not a pre-registration, not a protocol, not an experiment, not a backtest.
**Date:** 2026-08-16
**Status:** **LEVEL 1 — PROMISING BUT NOT YET DEFINABLE** · Governance: **B — EXTERNAL DATA ACQUISITION REQUIRED FIRST**
**Read-only:** no file in the control set was modified; no statistic was computed beyond reading frozen validation artifacts; nothing was downloaded.

---

## 1. Purpose

Determine whether a scientifically legitimate multi-market equity replication of the classic volatility-response asymmetry can be defined from available evidence, and what evidence/data would be required. This document records the candidate question, the evidence basis, the equity-universe feasibility analysis (historical and contemporary), the data-sufficiency requirements, the literature/prior status, independence checks, and the governance decision. It deliberately does NOT select markets, horizons, matching, bootstrap parameters, thresholds, or methods.

## 2. Candidate Scientific Question

> Does the classic negative-shock volatility-response asymmetry observed in the H01 equity observations generalize across a broader multi-market equity universe?

Preserved scientific meaning (identical to the H01 object):
- return → volatility **association** (exposure = return; response = forward change in realized variance);
- negative versus positive daily shocks of **equal absolute magnitude** (magnitude-matched comparison);
- **forward** volatility response;
- conditioning on **pre-shock realized-variance state**;
- asset-class-specific claim (equity only).

Explicitly NOT: return prediction, volatility timing, short-volatility strategy, market regime filter, trading signal, or leverage-effect trading strategy.

## 3. Why This Track Earned Screening (evidence basis — NOT confirmation)

From the frozen, stream-verified H01 v1.2 result set:

- Historical equity (`sp`, HPD): D = +0.150, CI95 [0.080, 0.193] (excludes zero), p_raw = 0.0001, p_Holm = 0.0011, classic direction.
- Contemporary equity (`USATECHIDXUSD`, M1): D = +0.422, CI95 [0.269, 0.577] (excludes zero), p_raw = 0.0001, p_Holm = 0.0011, classic direction.
- Both family-level significant under the corrected null-imposing inference (B = 10,000, seed 20260813, verified against the registered stream).
- Both formally EVIDENCE-LIMITED/DESCRIPTIVE because each layer has exactly one evaluable market (registered ≥2-market rule).
- Classic direction agrees with the strongest external equity volatility literature (Black 1976; GJR 1993; Engle–Ng 1993 — "ESTABLISHED" prior in the H01 definition lock).

**Explicit status:** the purpose of Track A is to test generalization beyond the two single-market observations, not to confirm a result already considered established. The two observations are candidate evidence for a definition process only.

## 4. Historical Equity Data Feasibility (validated HPD universe — outcome-blind inventory)

Source artifacts: `FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv`, `HPD_MANIFEST.csv`, `front_<root>.csv` (all frozen, 2026-08-13 acquisition validation). The HPD archive contains 32 front-month series.

| Root | Instrument | Asset class | Region | Validation | Coverage | Rolls | continuity_ok |
|---|---|---|---|---|---|---|---|
| sp | S&P 500 | Equity index | US | CORE, VALID | 1982-04-21 → 2002-10-01 | 82 | True |
| aor | All Ords (AUS) | ? (unresolved) | non-US | RESOLVED-NONUS (quarantined) | 1991-09-25 → 2001-09-28 | 35 | True |
| cac | CAC 40 (FRA) | ? (unresolved) | non-US | RESOLVED-NONUS (quarantined) | 1999-01-04 → 2002-10-01 | 15 | True |
| cr | CRB Index | Index (commodity basket) | US | RESOLVED-CORE | 1986-06-12 → 2002-08-30 | 91 | True |

Findings:

1. **`sp` (S&P 500) is the only validated US equity index** in the historical universe. There are no NASDAQ, Dow Jones, Russell, S&P MidCap, or other US equity index futures in the archive.
2. **`aor` and `cac` are the only other equity candidates, and both are excluded by the frozen H01 provenance rule** (quarantined RESOLVED-NONUS roots: aor, cac, lj, ll). Per the H01 protocol §4, these exclusions "predate H01, come from the frozen HPD acquisition/validation pipeline, are not H01 outcome-derived, are not altered by H01, and are **never re-admitted by outcome** (§17 gate 11)." Re-admission for a new research line would require a separate provenance/acquisition governance decision, independent of H01 outcomes — not something a screening can grant.
3. Even ignoring provenance: `cac` covers only 1999–2002 (~3.7 years) — insufficient for a meaningful historical replication; `aor` covers 1991–2001 (~10.3 years) and carries a flagged zero-volume anomaly (8,890 zero-vol rows reported in the manifest; "RussiaAnomaly" note) and an unresolved identity field (asset_class "?").
4. `cr` (CRB Index) is a commodity-basket index, not an equity index — it is already registered in H01 as the INDEX_COMMODITY class and is not an equity replication candidate.

**Conclusion:** from the current validated historical universe, **≥2 evaluable equity markets per historical layer is NOT achievable**. Options: (a) new US equity index data acquisition, or (b) a provenance governance decision on the quarantined non-US roots (aor/cac) with their documented quality caveats. Both are future decision-stage questions; neither is settled here.

## 5. Contemporary Equity Data Feasibility (M1 universe)

The contemporary M1 universe (`data/m1/`) contains exactly five daily series: XAUUSD, XAGUSD, EURUSD, BTCUSD, USATECHIDXUSD (plus their tick counterparts in `data/tick/`, MT5-sourced). The only equity index is **`USATECHIDXUSD`** (2023-09-01 → 2026-07-10, 871 days, single tech-sector index).

Findings:

1. **Exactly one contemporary equity market exists.** No SPX, NDX, DJI, or international index series are present locally.
2. No other legitimate equity price data exists in the repository: the `Time Series Momentum Original Paper Data.xlsx` contains only monthly TSMOM *factor* returns (359 rows, 2 sheets) — not daily price series, and therefore unusable for the daily-return / ΔlnRV object.
3. ≥2 contemporary equity markets **requires new M1 (or daily) data acquisition**.

## 6. Data Sufficiency Requirements (conceptual minimum)

To answer the candidate question honestly, a future definition would require (conceptually; no thresholds invented here beyond project-registered precedents):

- **≥2 evaluable equity markets per layer** (the ≥2-market evaluability rule is an existing registered H01 threshold, reused, not invented);
- enough time history and **enough independent shock observations** per market (H01's ≥30 matched pairs per stratum precedent; the historical common window 1987–2002 and the shorter contemporary window are the existing precedents — not decided here);
- **more than one regime** where possible;
- consistent daily-return construction (front-month, ratio back-adjustment — same as the HPD pipeline);
- comparable realized-variance construction (same 5-day forward/backward RV object);
- consistent source provenance and validation (gaps/rolls/continuity gates);
- **no outcome-driven market selection** (markets chosen from the universe definition, never from v1.2 performance).

Genuinely unresolved decisions (to be fixed only at definition stage, outcome-blind): exact market list, horizons, matching calipers, bootstrap parameters, evaluability thresholds, and the prior statement. This document does not resolve any of them.

## 7. Literature / Prior Support

SOURCE-DERIVED FACTS (from the H01 definition lock and readiness audit):
- The classic negative-shock volatility asymmetry for equities is an established, heavily replicated finding in the volatility literature (Black 1976; GJR 1993; Engle–Ng 1993), and is the basis of the definition-lock "ESTABLISHED" prior status for equity.
- The H01 primary object (correlation between a return and the change in its volatility, measured via realized-variance change) matches the formulation in Aït-Sahalia, Fan & Li (2013), as recorded in the definition lock.
- The external literature contains known limitations relevant to a multi-market replication: most classic-leverage evidence is US-equity-based; results can differ across international indices, index-future vs cash instruments, and sample eras; roll construction affects index-future series.

MODEL INFERENCE (this screening's judgment, labeled as such):
- The classic asymmetry is sufficiently established as the prior direction for an equity-specific track — the prior is not in doubt for the equity object.
- Multi-market replication across independent index markets has genuine scientific value: it converts two single-market observations into a cross-sectional claim, which the H01 single-market rule explicitly withholds.
- The candidate is a strengthening test, not a novelty claim: it expects the classic direction and asks whether it generalizes.

## 8. Scientific Object Stability

The H01 object — daily log-return shock, equal-magnitude matching, pre-shock volatility-state conditioning, forward 5-day ΔlnRV response — is defined at the market level and contains no asset-class-specific machinery. It is conceptually reusable for any equity index market without changing what the hypothesis means:

- shock = daily log return (identical construction);
- magnitude = |r| (identical);
- conditioning = pre-shock RV terciles (identical);
- response = forward ΔlnRV (identical);
- matching = caliper nearest-neighbour on |r| within (market, stratum) (identical);
- class statistic = equal-weighted market mean (identical).

**Yes — the same scientific object can plausibly be applied to multiple equity markets without a definition change.** No blocker at the object level.

## 9. Independence / Firewall

- **vs Mean Reversion (closed):** independent — a return→volatility association, not a return-autocorrelation claim.
- **vs 12/1 TSMOM (closed):** independent — no return prediction, no trend signal, no factor construction.
- **vs broad H01 (narrowed):** an asset-class-specific narrowing; the universal cross-class claim remains closed and is not revived.
- **vs trading strategy construction:** independent — a scientific association object; no strategy layer, no signal, no threshold.
- **Forbidden dependency:** this track must NOT become "use equity volatility asymmetry as a regime/filter for TSMOM" or any other strategy input. That combination is explicitly prohibited.

## 10. Data Acquisition Options (ranked; NO selection, NO download)

Ranked by the task criteria (scientific suitability, breadth, history, reproducibility, licensing, cost):

1. **Stooq (free index data).** Already referenced in the project's frozen acquisition validation as the independent external cross-validation source (`raja-grewal/stooq-commodities`, Codeberg, MIT) — an established provenance precedent in this repo. Broad index coverage (SPX, NDX, DJI, international indices), long history, reproducible daily downloads, free. Licensing must be re-verified for index data terms (HPD's own license was recorded PENDING in the acquisition report — the same caution applies to any new source).
2. **FRED (Federal Reserve data, free).** Clean licensing, reproducible, but narrow — limited to a handful of US index series; weak for a multi-market cross-sectional design.
3. **Quarantined HPD non-US roots (aor, cac).** History exists locally but is blocked by the frozen RESOLVED-NONUS exclusion rule (needs a separate provenance governance decision), has short/sectional coverage (cac ~3.7y) and documented quality flags (aor zero-vol anomaly) — poor scientific suitability.
4. **Commercial vendors (e.g., exchange data, Norgate/CSI-type services).** Clean licensing and breadth at cost; would need a procurement decision; no local precedent.

This ranking is informational for the future acquisition task. No source is selected, and nothing is downloaded.

## 11. Research Minimalism / Budget

Track A is a single narrow question — does the classic equity asymmetry generalize across multiple equity markets — and can remain one:

- same scientific object, same machinery (matching, strata, synchronized block bootstrap, Holm family — all re-usable unchanged);
- no ML, no clustering, no GARCH model comparison, no options, no volatility trading, no macro predictors, no regime classifiers, no dozens of horizons;
- the only genuinely new component is the expanded equity market universe and its validation.

Evidence-to-complexity ratio is high; the binding constraint is data, not methodology.

## 12. Readiness Level

**LEVEL 1 — PROMISING BUT NOT YET DEFINABLE.**

The hypothesis and evidence structure are clear (Level-2 characteristics: a single object, established prior, re-usable machinery), but the central data-feasibility question — whether ≥2 evaluable equity markets per layer can be assembled — remains **open and unresolved** with the current validated universes (1 historical market, 1 contemporary market). A formal definition lock cannot be written outcome-blind until the universe question is answered. Level 3 (pre-registration) is far off and not considered.

## 13. Governance Decision

**B — TRACK A REQUIRES EXTERNAL DATA ACQUISITION FIRST.**

The question is scientifically worthwhile and the evidence profile justifies the next research cycle, but current validated data cannot support a scientifically valid multi-market definition. Proceeding to a definition lock now would either manufacture a single-market class again (defeating the purpose) or silently re-admit quarantined non-US markets (a provenance decision that must be made explicitly and independently). Data acquisition must come first.

## 14. Exact Next Legitimate Task (high level only)

**EQUITY DATA ACQUISITION / SOURCE VERIFICATION TASK** — an outcome-blind acquisition and validation of a candidate multi-market equity index universe (historical and/or contemporary), following the repository's established ingestion-validation pattern (provenance, integrity fingerprints, gap/roll/continuity gates, licensing record), with the explicit requirement that markets are selected from universe definition — never from H01 v1.2 performance. Only after the acquired universe is validated does the question return to a **H01-EQUITY SCIENTIFIC DEFINITION LOCK**.

Neither artifact is written now.

## 15. Prohibited Follow-Up

Explicitly prohibited: selecting equity markets based on H01 v1.2 performance; dropping weak equity markets; choosing market counts to maximize significance; changing the 5-day horizon because another horizon looked better; importing GJR/EGARCH as the primary test; introducing K-means/HMM/ML; using the equity result as a trading signal; merging Track A with TSMOM; re-opening the commodity branch; re-admitting quarantined non-US roots without a separate provenance governance decision; reviving the universal H01 claim.

## 16. Integrity

This screening was strictly read-only: no file in the control set was modified; no H01 statistic was recomputed (all cited v1.2 values are the already-verified frozen artifacts); no market, horizon, parameter, threshold, or method was selected; no data was downloaded; no protocol or experiment script was created; BOE/Assembly/Deployment and the frozen H01 protocol are untouched. Feasibility statements are based on the frozen validation artifacts (`FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv`, `HPD_MANIFEST.csv`, `front_*.csv`) and the local M1/paper-data inventory, read only. The v1.2 equity result is treated strictly as candidate evidence for a definition process, not as an established finding.
