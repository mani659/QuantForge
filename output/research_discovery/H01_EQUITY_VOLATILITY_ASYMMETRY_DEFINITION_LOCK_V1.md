# QUANTFORGE — H01 EQUITY VOLATILITY-ASYMMETRY SCIENTIFIC DEFINITION LOCK V1

**Track:** A — Multi-market equity replication of the classic volatility-response asymmetry
**Type:** Outcome-blind scientific definition lock ONLY. Not a protocol, not an experiment, not a pre-registration, not a statistical analysis.
**Date:** 2026-08-16 (amended 2026-08-23)
**Version:** 1.0.0 → 1.1.0 (NYA source exception amendment)
**Status:** **LEVEL 2 — DEFINITION READY FOR PRE-REGISTRATION** (all central scientific choices fixed outcome-blind)
**Repository read-only except this artifact.**

---

## 1. Purpose and Basis

Freeze the scientific meaning of the US-anchored equity replication — the claim, the prior, the scope, the market universe, the instrument-comparability rule, and the object-identity choices — outcome-blind, before any pre-registration or execution. Grounded in: `H01_EQUITY_REPLICATION_SCREENING_V1.md`, `H01_EQUITY_SCOPE_DECISION_V1.md`, `H01_EQUITY_DATA_SOURCE_AUDIT_V1.md`, `H01_EQUITY_DATA_ACQUISITION_V1.md`, the frozen H01 v1.2 protocol, the H01 definition lock, the H01 v1.2 adjudication, the Track-A governance decision, and the frozen HPD validation artifacts.

This document fixes ONLY the scientific definition. Matching mechanics, bootstrap, strata counts, thresholds, and classification algorithms belong to pre-registration and are deliberately not resolved here.

---

## 2. Final Scientific Statement

> **H01-EQUITY (definition-locked):** *For equity/index markets, the forward change in realized variance following a negative daily return shock differs from that following a positive daily return shock of equal absolute magnitude, after conditioning on the pre-shock realized-variance state.*

- **Preserved meaning (identical to the frozen H01 object):** return → volatility **association**; exposure = daily close-to-close log return; negative vs positive shocks of **equal absolute magnitude**; **forward** volatility response; conditioning on **pre-shock RV state**; asset-class-specific claim (equity only).
- **Explicitly NOT:** a causal leverage mechanism, return prediction, volatility timing, a short-volatility strategy, a trading signal, or a market-regime detector.
- **Generalization framing:** this is an asset-class-specific replication question — does the frozen H01 phenomenon reproduce across multiple distinct US equity exposures? It is not a claim about equity markets generally, and it is not an international claim.

---

## 3. Equity Prior

**Frozen: CLASSIC EQUITY ASYMMETRY, direction `D > 0`, where**

`D = ΔlnRV(negative shock) − ΔlnRV(positive shock)`

Positive D = a larger subsequent volatility response following negative shocks.

- **SOURCE-DERIVED FACT (from the H01 definition lock, external literature):** Black (1976); Christie (1982); Nelson (1991, EGARCH); GJR (1993); Engle–Ng (1993); Bekaert–Wu (2000); Aït-Sahalia–Fan–Li (2013) — status **ESTABLISHED** for equities, prior direction external-literature-sourced, not QuantForge-derived.
- **MODEL INFERENCE:** the prior is not in doubt for the equity object; the replication's purpose is cross-sectional generalization, not re-establishment of the direction. No new literature is added to justify an implementation choice.

---

## 4. Geographic / Asset-Class Scope

**Frozen: US-anchored, two distinct exposures.**

- **US equity/index markets with genuinely distinct exposures** — broad US large-cap and US technology (Nasdaq family).
- **International expansion is NOT part of this definition.** Historical international breadth was found not achievable from free, archiveable sources (acquisition report §4, §8); it requires a separately authorized paid acquisition or an explicit scope revision. This is recorded as a boundary, not a deficiency of the current question.
- The claim this definition can support is **US-universe replication across two distinct exposures**, explicitly distinguished from "equity markets generally" (§15).

---

## 5. Market Universe

Frozen by identity/provenance, never by outcome. All markets are **daily-close price-type series** (no total-return series; no ETFs; no CFDs in the primary universe).

### Historical Era (1982-04-21 → 2002-10-01; the validated HPD era)

| Market | Source | Instrument | Exposure | Coverage (in-era) |
|---|---|---|---|---|
| `sp` | HPD (frozen, in-repo) | S&P 500 **futures**, front-month, ratio back-adjusted | **Broad US large-cap** | 1982-04-21 → 2002-10-01 (5,163 rows) |
| `NYA` | Yahoo Finance `^NYA` (exception §18a) | NYSE Composite **cash index**, daily close | **Broad US large-cap** | 1982-04-21 → 2002-09-30 (5,163 rows) |
| NASDAQ100 | FRED (fredgraph.csv) | Nasdaq-100 **cash index**, daily close | **US technology** | 1986-01-02 → 2002-10-01 |
| NASDAQCOM | FRED (fredgraph.csv) | Nasdaq Composite **cash index**, daily close | **US technology** | 1971-02-05 → 2002-10-01 |

### Contemporary Era (2016-08-15 → present; defined by FRED SP500/DJIA availability)

| Market | Source | Instrument | Exposure | Coverage |
|---|---|---|---|---|
| SP500 | FRED | S&P 500 **cash index** | **Broad US large-cap** | 2016-08-15 → present |
| DJIA | FRED | Dow Jones Industrial Average **cash index** | **Broad US large-cap** | 2016-08-15 → present |
| NASDAQ100 | FRED | Nasdaq-100 **cash index** | **US technology** | 2016-08-15 → present |
| NASDAQCOM | FRED | Nasdaq Composite **cash index** | **US technology** | 2016-08-15 → present |

### Structural candidate evaluation (identity/provenance basis)

- **NDX ⊂ NCOMP (nested constituents, same exchange, same era, same sector tilt):** both are the **US-technology exposure**, not two independent exposures. Both are retained as markets *within* that exposure — the Composite's 1971+ history extends era coverage and the pair provides within-exposure corroboration; exclusion of either has no structural basis. Registered explicitly: **market count (2) ≠ independent exposure count (1).**
- **SP500 vs DJIA (distinct index families — 500 cap-weighted vs 30 price-weighted — same broad-US large-cap exposure):** one exposure, two markets. Registered as near-duplicates within the broad-US exposure.
- **`sp` (futures) vs FRED SP500 (cash):** different instrument types and non-overlapping eras — distinct roles (historical vs contemporary broad-US legs). Governed by the futures/cash comparability rule (§6).
- **`USATECHIDXUSD` (M1/MT5): EXCLUDED from the primary universe** (§8) on structural grounds.
- **Explicitly NOT removed by outcome:** no candidate is included or excluded because of H01 v1.2 performance; `USATECHIDXUSD`'s strong v1.2 result played no role in its exclusion (the reason is structural), and no candidate is dropped for weak performance.

### Era structure

- **Historical Era:** 1982-04-21 → 2002-10-01 (HPD-era; `sp` full history; NDX/NCOMP within it). Common historical exposure window **1986 → 2002** (multi-regime: 1987 crash, 1990s bull, 2000-02 bear).
- **Contemporary Era:** 2016-08-15 → present (FRED SP500/DJIA availability; multi-regime: 2018 Q4, COVID 2020, 2022 bear, 2024-26).
- **Era-gap 2002-10 → 2016-08 is structurally excluded from both eras** (no broad-US cash series exists there from validated sources; provenance boundary, not an outcome choice). Pre-registration fixes the exact window endpoints from these era definitions.

---

## 6. Futures vs Cash Comparability

**Frozen decision: Option A — the historical broad-US exposure is the S&P 500 futures complex; futures-vs-cash is a registered source-type difference, not a defect.**

- **SOURCE-DERIVED FACT (acquisition report §6, §9-§10):** HPD `sp` vs cash S&P 500 (Yahoo ^GSPC validation, 5,162 obs, 1982-2002): daily-return corr 0.946; median |Δret| 16.4 bp; 115 dates (2.2%) >1%; the largest deviations are genuine documented futures/cash divergences (Dec-87 futures closed 201.50 vs cash 224.84 on 1987-10-19) and isolated roll/basis days — no evidence of HPD corruption.
- **Scientific measurement logic (MODEL INFERENCE):**
  1. The H01 object is a **within-market** statistic — shocks, magnitude matching, and ΔlnRV responses are computed entirely within each market's own series. Source type (futures vs cash) is therefore a recorded market attribute, not a pooled confound.
  2. The motivating historical broad-US observation (H01 v1.2 `sp`) was **itself futures-based** — a futures-based historical leg is instrument-consistent with the motivating evidence, not a mismatch.
  3. Option B (require cash historical, no mixing) is not a defensible scientific choice: no validated cash S&P 500 exists before 2016 from free, archiveable sources, and removing `sp` would collapse the historical layer back to the single Nasdaq factor the scope decision rejected. Option C (both futures and cash under a formal framework) is unavailable — the cash pre-2016 series does not exist in validated sources.
- **Registered comparability rule (conceptual):** (i) each market is its own scientific unit; (ii) source type (futures/cash) is recorded in the market-identity table; (iii) the object is applied identically to every series; (iv) futures/cash return divergence (documented above) is a registered interpretation caveat; a cross-source consistency check (futures vs cash, contemporary-era where comparable instruments exist) may be declared as a **secondary, non-rescuing** analysis at pre-registration.

---

## 7. Nasdaq Family Exposure

**Frozen: the Nasdaq family is ONE scientific exposure — US technology — carried by two markets (NASDAQ100, NASDAQCOM).**

- Structural basis (not performance): NDX constituents are a cap-weighted subset of the Composite; same exchange, same era, same sector tilt → the pair is one exposure with two markets.
- Both retained (era coverage 1971+ via Composite; within-exposure corroboration); registered explicitly that the two do **not** count as two independent exposures toward the generalization claim.
- The generalization claim rests on the **exposure count (2: broad-US, US-tech)**, not the market count (3 historical / 4 contemporary).
- No Nasdaq-series market is added or removed by H01 v1.2 performance.

---

## 8. Contemporary USATECHIDXUSD

**Frozen: EXCLUDED from the primary market universe on structural grounds.**

- **Identity:** a US-technology index delivered on the M1/MT5 feed — a **CFD-style instrument**, not a cash index or futures contract.
- **Exposure:** US technology — the **same factor** as NASDAQ100/NASDAQCOM; including it would add market count, not exposure count.
- **Provenance:** MT5 feed, a different lineage from the validated FRED/HPD sources; inclusion would require the source-mixing comparability rule that the governance chain has repeatedly deferred ("Do NOT mix FRED + HPD + MT5 without a future registered comparability rule") — a rule this definition declines to invent.
- **Outcome-blindness:** the exclusion is by identity/source-type/exposure-duplication. It would be identical if USATECHIDXUSD's v1.2 result had been null or negative. It is NOT removed because it was favorable or unfavorable.
- **Recorded role:** available only as a **secondary, non-rescuing** cross-provider consistency reference (e.g., does the contemporary tech exposure behave similarly in an independent MT5-delivered series?) to be declared at pre-registration — never as a primary market.

---

## 9. Shock Definition

**Frozen: primary shock = daily close-to-close log return `r_t`, signed scalar, within-market comparison; zero-return days excluded.**

- Reuses the frozen H01 shock construction (protocol §2, §12) — the replication tests the same exposure variable.
- No standardized/residual shock as the primary; secondary alternatives may be declared later at pre-registration but cannot alter the primary.
- Construction applies within each market's own series (futures: back-adjusted close; cash: index close).

---

## 10. Equal-Magnitude Concept

**Frozen: negative and positive shocks of equal absolute magnitude are compared; the equal-magnitude condition is not loosened.**

- The concept is magnitude-matched comparison (caliper matching on |r_t| within market and stratum is the H01-registered implementation, inherited as object identity; the exact algorithm/caliper belongs to pre-registration).
- Rank-only or unconditioned matching would change the scientific meaning and is not an option.

---

## 11. Volatility Response Concept

**Frozen: primary response = `ΔlnRV = ln(RV_forward) − ln(RV_backward)`, where realized variance is the sum of squared daily log returns over the window.**

- Conceptual identity with the frozen H01 response (protocol §3, §12): forward window vs pre-shock window, shock day excluded from both.
- Implementation details (window arithmetic, missing-data handling) belong to pre-registration.

---

## 12. Horizon Decision

**Frozen: `h = 5 trading days` — inherited as OBJECT-IDENTITY, not by inertia and not by outcome.**

- The replication's purpose is to test whether the **frozen H01 object** generalizes across markets. The 5-day window is part of that object, registered in H01 v1.1 (before any outcome existed), with the literature anchor Aït-Sahalia–Fan–Li (2013) documenting the effect at 5-day and 21-day horizons (protocol §11). Changing the horizon would change the object and would make the exercise a new experiment rather than a replication.
- This choice is outcome-blind: 5 days was fixed pre-outcome in H01 v1.1; the equity-specific result did not and cannot influence it.
- 1-day and 21-day horizons are **secondary-only, non-rescuing** (may be declared at pre-registration, cannot alter the primary verdict) — mirroring the frozen v1.2 secondary treatment.

---

## 13. Volatility-State Conditioning

**Frozen: condition on the pre-shock realized-variance state (within-market); the concept is retained unchanged.**

- The scientific requirement is pre-shock RV conditioning — intrinsic to the question (the asymmetry is conditional on the vol state).
- The stratum count (3 terciles on within-market ln(RV_back)) and bounds are inherited object details from the frozen H01 object (protocol FROZEN_PARAMS); their exact implementation belongs to pre-registration. No new state model (regime/HMM/GARCH-state) is introduced.

---

## 14. Cross-Market Aggregation

**Frozen (conceptual):**
- Each market is an **independent scientific unit**; market-level evidence is primary.
- No single market can dominate the conclusion — equal-weight conceptual treatment (market-level equal weighting is the registered H01 aggregation concept, inherited).
- Cross-market aggregation is secondary to market-level evidence; the exact estimator belongs to pre-registration.

---

## 15. Generalization Claim

**Frozen boundary:**
- **Within-market evidence:** a single market's asymmetry (however significant) is descriptive of that market.
- **Cross-market replication:** consistent direction across multiple distinct **exposures** within an era is replication evidence.
- **US-universe generalization:** consistent direction across the two distinct US exposures in both eras supports the US-anchored claim — explicitly NOT "equity markets generally."
- **No international generalization** is claimed by this definition.

---

## 16. Falsification Concept

At a high level (no thresholds — those belong to pre-registration), the candidate is weakened or falsified by:
- a **reliable opposite-direction effect** across multiple distinct equity exposures;
- **failure to reproduce the classic direction** across the validated universe (the two exposures, both eras);
- **instability across legitimate eras** (historical vs contemporary direction inconsistency).

---

## 17. Independence Firewall

**Frozen: independent of** Mean Reversion (closed), 12/1 TSMOM (closed), trading-strategy construction, and volatility-based trade filters. A future use of this research as a trading filter requires a separate scientific and strategy research process. The association object is a research hypothesis, not a signal.

---

## 18. Licensing / Provenance

Recorded honestly (governance constraint, not a scientific result):

| Component | Status |
|---|---|
| HPD `sp` | **PENDING** (standing frozen HPD record; local research use per repo precedent) |
| FRED SP500, DJIA | platform access CLEAR (attribution required); underlying index series (© S&P Dow Jones Indices) archival rights **PENDING** |
| FRED NASDAQ100, NASDAQCOM | platform access CLEAR; underlying series (© Nasdaq) archival rights **PENDING** |
| Permission requests | **PREPARED, NOT SENT** (acquisition report §11; operator dispatch required) |
| Nasdaq API, Stooq | NOT in the primary universe; used only for validation; nothing archived from them |
| Yahoo Finance `^NYA` | **EXCEPTION GRANTED** (§18a below) |

**Exception — NYSE Composite (`NYA`) — owner-approved 2026-08-23:**

The existing Yahoo Finance `^NYA` daily Close dataset is approved as a primary source for NYA, subject to the following conditions:

1. The source artifact is the immutable local file `docs/NYA_DATA.html` (SHA-256: `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f`)
2. Only the `Close` field is used (price-type index level)
3. The dataset has been independently validated against FRED quarterly NYSE Composite observations (80 quarter-end dates; 76 exact matches; maximum discrepancy 0.51%) — bounded independent validation, not full daily-series validation
4. This exception applies only to NYA and does not extend to any other Yahoo-sourced market
5. Yahoo Finance archival rights remain **PENDING** (requires owner acceptance for archival persistence)

**Amendment provenance:**
- Amendment type: Source-governance exception for Yahoo Finance NYA
- Proposal: `H01_NYA_DEFINITION_LOCK_AMENDMENT_PROPOSAL_V1.md`
- Independent audit: `H01_NYA_AMENDMENT_PROPOSALS_INDEPENDENT_AUDIT_V1.md` (verdict: A — PASS)
- Owner approval: 2026-08-23
- Applied: 2026-08-23

No source is represented as CLEAR without evidence; licensing PENDING is a governance constraint recorded at definition stage, resolved at acquisition/ingestion.

---

## 19. Definition-Level Readiness

**LEVEL 2 — DEFINITION READY FOR PRE-REGISTRATION.**

Every central scientific choice is fixed outcome-blind: claim (§2), prior direction (§3), scope (§4), universe with structural exclusions (§5, §8), futures/cash rule (§6), Nasdaq exposure accounting (§7), shock (§9), equal-magnitude (§10), response (§11), horizon (§12), conditioning (§13), aggregation (§14), generalization boundary (§15), falsification concept (§16), firewall (§17), licensing record (§18). No choice required outcome knowledge to be made; none was inspected.

Deferred to pre-registration by design (not unresolved): matching algorithm/caliper/tie-break, strata implementation, bootstrap construction (L, B, seed), p-value convention, Holm family, evaluability thresholds (≥30 pairs/stratum, ≥2 markets), classification rules, and secondary analyses (horizons, cross-source consistency, cross-provider reference). Deferred items are inherited from the frozen H01 object or are registration decisions; none changes the scientific definition.

---

## 20. Exact Next Task

**PRE-REGISTRATION — H01 EQUITY PROTOCOL V1 (pre-registration draft)**, registering the frozen definition (§2-§18) with the statistical design (matching, strata, bootstrap, family, thresholds, classification) — followed by independent audit, then execution. No protocol is written by this definition lock; nothing is executed.

---

## 21. Integrity

- The repository was modified in exactly one way: the required artifact `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY_DEFINITION_LOCK_V1.md`.
- No H01 statistic was computed; no matching, bootstrap, or model was run; no data was inspected for market selection; no market, horizon, parameter, or threshold was chosen from any outcome; no prior or class was altered.
- The frozen H01 v1.2 protocol and artifacts, the HPD validation records, BOE/Assembly/Deployment, and all governance records are untouched. Universe and design choices are justified by identity, provenance, source type, and the documented object — never by v1.2 performance.
