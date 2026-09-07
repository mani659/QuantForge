# QUANTFORGE — H01 EQUITY REPLICATION SCOPE DECISION V1

**Track:** A — Multi-market equity replication of the classic volatility-response asymmetry
**Type:** Governance / scientific-scope decision ONLY. Not a definition lock, not a protocol, not an experiment, not a statistical analysis.
**Date:** 2026-08-16
**Status:** **B — BROADER DATA REQUIRED BEFORE DEFINITION LOCK**
**Read-only on repository:** the only file created is this artifact. No dataset was acquired; no statistic was computed; no protocol or definition lock was written.

---

## 1. Purpose

Decide the scientific scope for Track A before any further data collection: what claim must the equity replication support, what breadth does that claim require, and can the currently validated, archiveable free sources (principally FRED) deliver it? This document fixes the claim and the required breadth; it does NOT select markets, horizons, matching, bootstrap, thresholds, or methods, and it does NOT write the definition lock.

---

## 2. Scientific Question (unchanged, from the screening)

> Does the classic negative-shock volatility-response asymmetry generalize beyond the two single-market equity observations already seen in H01 v1.2 (`sp`, historical S&P 500, D = +0.150, p_Holm = 0.0011; `USATECHIDXUSD`, contemporary, D = +0.422, p_Holm = 0.0011)?

The operative question is NOT "can we find any two equity series." It is: can we construct a **cross-sectional equity universe whose breadth and provenance are sufficient to justify a generalization claim** — the exact thing the H01 ≥2-market rule exists to withhold on single (or near-single-factor) evidence?

The registered scientific object is fully reusable: shock = daily log return; equal-magnitude matching; pre-shock RV-state conditioning; forward 5-day ΔlnRV response; equity prior = **ESTABLISHED classic leverage** (definition lock: Black 1976; Christie 1982; Nelson 1991; GJR 1993; Engle–Ng 1993; Bekaert–Wu 2000; Aït-Sahalia–Fan–Li 2013 — external-literature sourced, not QuantForge data).

---

## 3. FRED US-Only Option

Candidate (from the data-source audit): historical = {NASDAQCOM, NASDAQ100}; contemporary = {SP500, DJIA, NASDAQCOM, NASDAQ100} (± the existing `USATECHIDXUSD`, subject to a future source-comparability rule).

### Assessment

**Historical cross-sectional independence: LOW.** NASDAQ100's constituents are the largest ~100 non-financial Nasdaq-listed names — structurally a subset of the ~3,000+ name Nasdaq Composite — listed on the same exchange, in the same era (1986-2002), with the same heavy technology/sector tilt. The pair is a **near-duplicate exposure**, not an independent market pair. Empirically their daily returns are near-perfectly correlated by construction (high constituent overlap + cap weighting); this is a structural fact, not a claim needing a computed correlation.

**Effectively a single equity factor historically: YES.** A 1986-2002 historical layer built from these two series is one observation of "the classic asymmetry in US technology-listed equities," not a cross-sectional claim about equity markets.

**Does it satisfy the scientific purpose? NO.** The track exists to convert two single-market observations into a cross-sectional generalization. A historical layer of two near-duplicate Nasdaq indices re-creates the H01 single-observation problem at the *factor* level — the exact defect the ≥2-market rule was registered to prevent (protocol §11, §18: a primary verdict requires ≥2 evaluable markets; for exactly 2, both must agree; the rule is never vacuous). Two near-duplicates satisfy the letter of the rule and violate its purpose.

**Additional structural defect: the S&P 500 is absent from the historical layer.** The motivating historical observation (`sp`) is S&P 500 — a *broad US large-cap* index, the flagship of the ESTABLISHED prior. FRED's SP500/DJIA begin 2016-08-15, so a FRED-only historical layer cannot include the broad-US exposure at all. The replication universe would exclude the exact index family whose evidence started the track, and would test "does the asymmetry hold in US tech indices" — a different object from "does the S&P-500-type asymmetry generalize."

**Cross-era comparability: FAILS.** The contemporary FRED set spans ~2 distinct US exposures (broad large-cap via SP500/DJIA; US tech via NASDAQCOM/NDX), while the historical set spans 1 (US tech). The claim would differ across eras by construction — an internal design inconsistency.

**Correlation caveat (stated explicitly, per the task):** correlation alone is not scientific invalidity, and markets are not excluded here because they are correlated. The rejection is narrower and structural: the historical layer provides **one factor's worth of independent evidence**, which is insufficient for the generalization claim regardless of correlation level, and it cannot include the broad-US exposure that anchors both the motivating evidence and the literature prior.

---

## 4. International-Breadth Option

Broader geographic coverage **materially strengthens** the claim. The two candidate statements are different scientific objects:

- "the classic asymmetry **reproduces in a small set of US equity indices**" — a weak replication statement, partially redundant with the already-established US literature; and
- "the classic asymmetry **generalizes across equity markets**" — a cross-sectional claim requiring independent markets (different economies, regimes, market microstructures, and index-construction conventions).

International indices (European, Asian, other developed markets) are the natural carriers of that independence. No international markets are chosen here — the point is that the *claim* of generalization, honestly stated, requires breadth beyond one factor per era and, ideally, more than one geography. That breadth is currently available only through license-restricted sources (Yahoo, Stooq — depth verified in the data audit, archival permission not granted) or paid vendors (clean licensing at cost, no procurement authorization).

---

## 5. Hypothesis Scope

The eventual claim should be **Scope C — "generalizes across equity indices broadly, requiring a breadth target"** — stated concretely as:

> The classic negative-shock volatility-response asymmetry, already ESTABLISHED for US equities, reproduces across multiple **independent** equity markets (US and, where available, international), i.e., the phenomenon is a property of equity markets, not of a single index or factor.

Rationale:
- **Scope A alone ("generalizes across US equity indices") is too weak** to constitute a generalization claim: the phenomenon is already US-established in the external literature, and a US-only replication (even multi-market) mainly re-measures a correlated US factor. It is a replication statement, not the generalization the track exists to test.
- **Scope B alone ("international")** needlessly discards the US anchor of the motivating evidence and the literature prior.
- **Scope C** (broad, with a breadth target) is the honest target; the breadth target is a definition-lock question and is explicitly NOT fixed here. The claim is US-anchored but generalization-framed: multiple independent exposures per era, ideally spanning ≥2 geographies.

The choice is evidence-driven, not source-driven: the two motivating observations are US, so the claim must be US-anchored; the *generalization* content requires independent exposures, which neither the current data nor FRED can supply historically.

---

## 6. Minimum Scientific Breadth

The registered ≥2-evaluable-market rule (protocol §11, §18) is a **minimum technical evaluability requirement** — its purpose is "no primary verdict rests on one market." It is NOT an adequacy criterion for a generalization claim.

- **Minimum evaluability:** ≥2 markets per layer, both agreeing in sign for the ≥2/3 consistency rule to be non-vacuous. Already registered; reused, not invented.
- **Adequate evidence for generalization:** multiple **independent exposures** per era — independence judged on exposure (economy, sector, microstructure, era), not on ticker count. Two near-duplicate markets are one observation of the phenomenon.
- Whether a specific numeric breadth target (e.g., a minimum number of markets or minimum number of distinct factors per layer) is necessary **cannot be justified yet** — the binding constraint is factor independence, not count, and the defensible numeric target depends on the universe that acquisition can actually deliver. Recorded as an **unresolved definition-lock question**.

---

## 7. Market Dependence / Near-Duplicates

Structural analysis of the candidate set {NASDAQCOM, NASDAQ100, SP500, DJIA, USATECHIDXUSD}:

| Group | Members | Relationship | Distinct exposures |
|---|---|---|---|
| Nasdaq family | NASDAQCOM, NASDAQ100, (USATECHIDXUSD) | NDX constituents ⊂ Composite; same exchange; same era; tech-heavy cap-weighted | 1 (US tech) |
| Broad US large-cap | SP500, DJIA | Distinct index families (500 cap-weighted vs 30 price-weighted) but same broad US large-cap exposure, near-perfectly correlated | 1 (US broad) |

- The whole candidate set spans **≈2 distinct exposures**, both US: broad US large-cap and US tech.
- The **historical** subset spans **1** exposure (US tech).
- No market is excluded merely for correlation; the finding is that the *set's factor diversity* is insufficient for the claim — a universe-construction problem for the acquisition path, not a market-removal decision.
- The near-duplicate structure is a matter of record (constituent overlap, same exchange, same sector tilt), not of computed statistics; empirical correlation estimation belongs to the ingestion-stage validation, not to this governance decision.

---

## 8. Licensing / Reproducibility

Two questions, deliberately kept separate:

### Scientific suitability
Can the source answer the scientific question? FRED **can** structurally answer a US-only question (validated close-only daily cash-index levels, fully compatible with the H01 object, no roll construction). It **cannot** supply the historical breadth required by the claim (§3). Yahoo/Stooq **can** supply breadth (depth verified) but are not archiveable.

### Governance / licensing suitability
Can the data legally and reproducibly be archived and used in this workspace?
- FRED platform: CLEAR (free; attribution required; abuse/rate prohibitions). FRED series: **PENDING** for archival — third-party copyright (© S&P DJI for SP500/DJIA; © Nasdaq for the Nasdaq series); the FRED terms require contacting the data owner for permission for anything beyond personal use. Mirrors the HPD license-PENDING precedent.
- Yahoo: RESTRICTED (no archival permission; official API terminated 2017 for ToS abuse). Stooq: RESTRICTED ("personal use only") and access-blocked. Paid vendors: CLEAR under contract, cost + procurement.

**Conclusion:** a defensible universe must satisfy BOTH dimensions. No currently validated source does so for the historical layer of any scope: FRED fails breadth, and the breadth-capable sources fail archival licensing.

---

## 9. Data Acquisition Alternatives

- **A — Proceed US-only with FRED: REJECTED.** The historical layer is a single Nasdaq factor and cannot include the broad-US exposure that anchors the claim; the letter of the ≥2-market rule would be met while its scientific purpose is violated. This is precisely the "two highly related Nasdaq series satisfying a numerical minimum" outcome the task prohibits.
- **B — Acquire broader equity data first: SELECTED.** The research question is sound, but the narrow US/Nasdaq-heavy dataset cannot support the intended claim. What is missing: (i) at least one additional **distinct** historical equity exposure (a broad-US historical index such as S&P 500/Dow pre-2016, or international indices) beyond the Nasdaq pair, and (ii) an **archival-legal licensing path** for the chosen broader universe (written permission from data owners, or a paid-vendor procurement decision).
- **C — Keep both paths open until the definition lock: REJECTED** as a deferral. The task's governing principle is that the claim must be fixed before more data is collected ("scientific claim → required breadth → defensible universe → data acquisition → definition lock"). One of the two "paths" (US-only FRED) is already known to be scientifically insufficient for the claim, so keeping both open is not an honest option — the acquisition must be targeted at the breadth the claim requires.

No acquisition begins in this task.

---

## 10. Research Minimalism

The smallest scientifically defensible universe is the target — but **smaller ≠ sufficient**. The binding constraint is ≥2 **independent exposures** per era, not a raw market count. A 5-ticker US set spanning 2 correlated factors is *not* smaller-but-sufficient; it is insufficient at any size. Minimalism operates within the breadth requirement: once the acquisition path delivers a defensible multi-exposure universe, the definition lock should use the fewest markets that satisfy it — no "more is better," no redundant additions.

---

## 11. Governance Decision

**B — BROADER DATA REQUIRED BEFORE DEFINITION LOCK.**

- The claim (equity-market generalization of the classic asymmetry, US-anchored, requiring independent exposures per era, ideally international) is sound and remains the track's target.
- The currently validated, archiveable free sources cannot support a defensible historical multi-market equity layer of **any** scope: FRED's historical layer is one Nasdaq factor with no broad-US index before 2016; the breadth-capable sources (Yahoo, Stooq) are license-restricted for archival.
- Therefore the narrow US/Nasdaq-heavy dataset would not support the intended claim, and the definition lock cannot be written outcome-blind on a universe that is known to be near-single-factor. Broader data acquisition — with the licensing path resolved — must precede the definition lock.

---

## 12. Exact Next Legitimate Task

**EQUITY DATA ACQUISITION / LICENSING-RESOLUTION TASK** (high level only):

1. Resolve the archival-licensing path for a broader universe: written permission requests to the relevant data owners (S&P DJI, Nasdaq, Yahoo, Stooq) for archival use, and/or a separately authorized paid-vendor procurement decision (e.g., Norgate/CSI/exchange data) — nothing purchased without authorization.
2. Acquire and validate at least one additional **distinct** historical equity exposure beyond the Nasdaq pair — a broad-US historical index (S&P 500 / Dow pre-2016) and/or international equity indices — following the repository's established ingestion pattern (provenance, integrity fingerprints, gap/continuity gates, license record PENDING where applicable).
3. Only then: **H01-EQUITY SCIENTIFIC DEFINITION LOCK** — which fixes the breadth target, the market list (outcome-blind, never from H01 v1.2 performance), and the remaining design parameters.

No protocol and no definition lock is written now.

---

## 13. Prohibited Follow-Up

Explicitly prohibited: selecting markets because H01 v1.2 favored them; discarding NASDAQCOM/NDX because they are inconvenient; adding SP500/DJIA only to increase sample size; using ETFs as substitutes without a separate scientific justification; treating CFD data as equivalent to cash/futures index history automatically; mixing FRED, HPD, and MT5 data without a future registered source-comparability rule; claiming international (or even multi-market US) generalization from two Nasdaq-family series; accepting a near-single-factor historical layer on the strength of the numerical ≥2-market minimum; writing the definition lock or any protocol before the breadth and licensing questions are resolved; re-opening commodities; reviving the universal H01 formulation.

---

## 14. Integrity

- This decision modified the repository in exactly one way: the required artifact `output/research_discovery/H01_EQUITY_SCOPE_DECISION_V1.md`.
- No dataset was acquired; no H01 statistic was computed; no shock/ΔlnRV/asymmetry quantity was calculated; no market, horizon, matching parameter, bootstrap parameter, or threshold was selected; no prior or class was altered; no definition lock or protocol was written.
- The near-duplicate and factor-dependence judgments rest on structural/provenance facts (constituent overlap, same exchange, same era, sector tilt) and on the frozen validation artifacts, not on computed statistics; empirical correlation estimation is deferred to the ingestion-stage validation.
- The frozen H01 v1.2 protocol and artifacts, BOE/Assembly/Deployment, and all governance records are untouched.
