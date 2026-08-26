# QUANTFORGE — H01 EQUITY V1

# INDEPENDENT READ-ONLY AUDIT: NYA AMENDMENT PROPOSALS

**Audit type:** Independent, adversarial, read-only governance and scientific-scope audit
**Date:** 2026-08-23
**Status:** COMPLETE

---

## 1. Executive Verdict

**A — PASS**

Both proposals are minimal, evidence-supported, internally consistent, and safe to present for owner approval. No scientific, statistical, provenance, or governance defects were found.

---

## 2. Amendment A Verdict

**PASS**

The definition-lock amendment correctly proposes a narrowly scoped exception for Yahoo Finance `^NYA` as a primary source, subject to provenance, SHA-256, immutable-artifact, and independent FRED validation controls. The exception does not authorize Yahoo generally, does not create a general source authorization, and does not change any scientific or statistical element.

---

## 3. Amendment B Verdict

**PASS**

The protocol amendment correctly proposes adding `NYA` to `EQBROAD_L1` as the second primary-evaluable market, upgrading that cell from EVIDENCE-LIMITED/DESCRIPTIVE to primary-eligible. The amendment does not change any statistical parameter, inference method, multiple-comparison family, or scientific object.

---

## 4. Required Findings Table

| Audit Area | Verdict | Severity | Finding |
|---|---|---|---|
| Source exclusion | PASS | — | Existing §18 Yahoo exclusion correctly cited |
| Yahoo exception scope | PASS | — | Exception is narrowly scoped to NYA only |
| NYA identity | PASS | — | Correctly identified as NYSE Composite |
| Provenance | PASS | — | SHA-256, immutable artifact, field selection documented |
| FRED validation | PASS | — | Bounded validation correctly described |
| Licensing | PASS | — | PENDING status correctly preserved |
| Structural distinctness | PASS | — | NYA vs S&P 500 distinctness verified |
| Historical coverage | PASS | — | 1982-04-21 → 2002-09-30 satisfies H01 |
| Terminal-date handling | PASS | — | 1-day gap handled by existing §9 missing-day policy |
| Scientific object | PASS | — | Classic volatility-response asymmetry unchanged |
| Statistical invariants | PASS | — | All parameters unchanged |
| Multiple testing | PASS | — | Family is 4 cells (§19); adding markets within a cell does not change family |
| Sample eligibility | PASS | — | ≥30 pairs/stratum gate unchanged |
| Outcome neutrality | PASS | — | No outcome-dependent language found |
| Governance sequence | PASS | — | Correct proposal → audit → approval → implementation → execution |
| Scope creep | PASS | — | No hidden authorization found |

---

## 5. Amendment A Detailed Audit

### 5a. Existing Rule

**Location:** `H01_EQUITY_VOLATILITY_ASYMMETRY_DEFINITION_LOCK_V1.md`, §18
**Exact text:** "Nasdaq API, Yahoo, Stooq | NOT in the primary universe; Yahoo/Nasdaq-API used only for validation; nothing archived from them"
**Governance meaning:** Yahoo is excluded as a primary source for any market in the H01 universe.

### 5b. Proposed Exception

The amendment proposes a single exception:

> **Exception — NYSE Composite (`NYA`):** The existing Yahoo Finance `^NYA` daily Close dataset is approved as a primary source for NYA, subject to the following conditions:
> 1. Immutable local file with SHA-256
> 2. Only `Close` field used
> 3. Independent FRED validation
> 4. Applies only to NYA

**Audit finding:** The exception is narrowly scoped. It does NOT:
- Remove the general Yahoo exclusion
- Authorize Yahoo for other symbols
- Create a general source authorization
- Permit future unregistered Yahoo datasets

### 5c. Source Identity

| Property | Value | Verified |
|---|---|---|
| Ticker | `^NYA` | ✅ |
| Index | NYSE Composite | ✅ |
| Field | `Close` | ✅ |
| Date range | 1982-04-21 → 2002-09-30 | ✅ |

### 5d. Provenance Controls

The proposal requires:
- ✅ Immutable source artifact (`docs/NYA_DATA.html`)
- ✅ SHA-256 fingerprint
- ✅ Exact source identity (`^NYA`)
- ✅ Exact field (`Close`)
- ✅ Acquisition provenance (Yahoo Finance historical data page)
- ✅ Preserved raw artifact (HTML file)
- ✅ Independent validation evidence (FRED quarterly)

### 5e. FRED Validation Wording

The proposal states:

> Independent validation is **bounded, not full daily-series validation**. FRED provides quarterly observations, not daily. The 76/80 exact match rate establishes high-confidence fidelity for the NYA series across the 1982-2002 historical window, but does not independently verify every daily observation.

**Audit finding:** The proposal correctly describes bounded validation. It does NOT falsely claim full daily-series validation.

### 5f. Licensing Wording

The proposal states:

> Yahoo Finance archival rights: **PENDING** (Terms of Service permit personal/non-commercial use; archival persistence in repository requires owner acceptance)

**Audit finding:** Licensing remains correctly classified as PENDING. It is not silently declared acceptable.

### 5g. Scientific Firewall

Amendment A introduces no:
- ✅ Hypothesis change
- ✅ Signal change
- ✅ Return definition change
- ✅ Statistical change
- ✅ Inference change
- ✅ Market-selection logic

---

## 6. Amendment B Detailed Audit

### 6a. Existing Membership

Protocol §5 currently defines:

| Cell | Markets |
|---|---|
| EQBROAD_L1 | `sp` |
| EQBROAD_L2 | SP500, DJIA |
| EQTECH_L1 | NASDAQ100, NASDAQCOM |
| EQTECH_L2 | NASDAQ100, NASDAQCOM |

### 6b. Proposed Membership

| Cell | Markets |
|---|---|
| EQBROAD_L1 | `sp`, `NYA` |

**Audit finding:** Only NYA is added. No other market is added or removed. EQBROAD_L2, EQTECH_L1, EQTECH_L2 are unchanged.

### 6c. NYA Eligibility

| Requirement | NYA | Status |
|---|---|---|
| Broad-US exposure | NYSE Composite (~2,000 NYSE stocks) | ✅ |
| Structurally distinct from `sp` | Different universe, construction, exchange | ✅ |
| Price-type daily close | Close field (price-type index level) | ✅ |
| Historical coverage | 1982-04-21 → 2002-09-30 | ✅ |
| ≥30 pairs per stratum | 5,163 observations (expected) | ✅ (determined at execution) |

### 6d. Structural Distinctness

| Attribute | NYA | S&P 500 |
|---|---|---|
| Universe | All NYSE stocks (~2,000) | 500 selected large-cap |
| Selection | All NYSE-listed | Committee-selected |
| Exchange | NYSE only | NYSE + Nasdaq + other |
| Instrument | Cash index | Futures |

**Audit finding:** NYA is structurally distinct from S&P 500. The distinctness is comparable to SP500 vs DJIA in EQBROAD_L2.

---

## 7. Critical Date-Range Audit

### Terminal Date

| Item | Value |
|---|---|
| NYA latest date | 2002-09-30 |
| H01 HISTORICAL_END | 2002-10-01 |
| Gap | 1 trading day |

### Protocol Handling

Protocol §9 states:

> Missing-day policy: a shock day `t` is excluded unless **all 5 days** of each window are present in the market's daily series (incomplete windows dropped, not imputed).

**Audit finding:** The 1-day gap is handled by the existing missing-day policy. NYA observations on 2002-09-30 and earlier dates are valid; the missing 2002-10-01 observation is simply not available, and any shock requiring that date in its window will be dropped. No protocol amendment is needed for the terminal date.

---

## 8. Statistical Invariants Audit

The following are verified unchanged:

| Parameter | Value | Changed? |
|---|---|---|
| Shock definition | Daily close-to-close log return | NO |
| Volatility response | ΔlnRV = ln(RV_forward) − ln(RV_backward) | NO |
| Horizon | h = 5 trading days | NO |
| Strata | 3 terciles of ln(RV_back) | NO |
| Matching | Caliper c = 0.25 × SD(|r|) | NO |
| Bootstrap | L = 11, B = 10,000, seed 20260816 | NO |
| Null construction | Null-imposing construction | NO |
| CI | Percentile, 2.5%/97.5% | NO |
| Holm | 4-cell family, α = 0.05 | NO |
| Evaluability | ≥30 pairs/stratum, ≥2 markets per cell | NO |
| Classification | SUPPORT/CONTRADICTION/INCONCLUSIVE/EVIDENCE-LIMITED | NO |

**Audit finding:** Adding one eligible market changes the number of observations within EQBROAD_L1, but this is **data/universe scope**, not a methodological redesign. All statistical parameters remain frozen.

---

## 9. Multiple-Comparison Audit

### Family Definition

Protocol §19 states:

> **Primary family:** the **4 cells** of §5 — EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2.

### Impact of Adding NYA

- Family size: 4 cells → 4 cells (**unchanged**)
- Family composition: EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2 (**unchanged**)
- Holm correction: applied to 4 cell-level statistics (**unchanged**)
- α = 0.05 (**unchanged**)

**Audit finding:** The primary family is defined at the **cell level**, not the market level. Adding a market within a cell does not change the number of family members. The multiple-comparison framework is completely unchanged.

---

## 10. Outcome Neutrality Audit

The proposal states:

> NYA is added because:
> 1. It is structurally distinct from S&P 500
> 2. It covers the required historical period
> 3. It has been independently validated
> 4. It completes the pre-existing EQBROAD_L1 evidence design

**Audit finding:** The justification is identity/provenance-based, not outcome-based. No language presupposes a specific H01 result. The proposal correctly states that evaluability is determined at execution.

---

## 11. Source-Conflict Handling Audit

### Source Hierarchy

| Role | Source | Description |
|---|---|---|
| Primary source | Yahoo `^NYA` | Daily Close data for H01 execution |
| Independent validation | FRED quarterly | 80 quarter-end observations (bounded) |
| Supporting corroboration | Norgate trial | Recent-period (2024-2026) agreement |

**Audit finding:** The proposal correctly distinguishes:
- Primary source (Yahoo)
- Independent validation (FRED)
- Supporting corroboration (Norgate)

The proposal does NOT describe Norgate recent-period agreement as historical 1982-2002 validation.

---

## 12. Governance Sequencing Audit

The proposal states:

> **Amendment proposal → independent audit → owner approval → frozen amended protocol → single authorized execution → independent adjudication**

**Audit finding:** The sequence is correct. No execution occurs before approval. No amendment is silently applied.

---

## 13. Scope-Creep Audit

The proposal does NOT authorize:
- ✅ H01 strategy construction
- ✅ PnL calculation
- ✅ Execution modeling
- ✅ Spread testing
- ✅ Live trading
- ✅ BOE semantics
- ✅ Detector creation
- ✅ Portfolio construction
- ✅ Another market (beyond NYA)
- ✅ Another era
- ✅ Another hypothesis
- ✅ Future Yahoo data
- ✅ Dynamic market replacement
- ✅ Result-dependent exclusions
- ✅ Parameter tuning

**Audit finding:** No scope creep detected. The proposals are exactly as narrow as claimed.

---

## 14. Owner-Approval Readiness

**READY FOR OWNER APPROVAL**

Both proposals have passed independent audit. The next step is owner review and approval of:
1. Definition lock amendment (Amendment A)
2. Protocol amendment (Amendment B)

---

## 15. Execution Authorization

> **H01 EXECUTION IS NOT AUTHORIZED BY THIS AUDIT.**

This audit establishes that the proposals are safe to present for owner approval. Execution requires:
1. Owner approval of both amendments
2. Implementation of approved amendments
3. Fresh independent implementation audit
4. Explicit execution authorization

---

## 16. Next Task

**Owner review and approval of the two NYA amendment proposals**

---

## 17. Integrity

- Read-only: YES
- No execution: YES
- No data download: YES
- No protocol modification: YES
- No definition lock modification: YES
- No statistics computed: YES
- No new DISC created: YES
- No commit: YES
