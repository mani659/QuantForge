# QUANTFORGE — H01 EQUITY V1

# PROTOCOL AMENDMENT PROPOSAL: NYA UNIVERSE ADDITION

**Amendment type:** Universe addition — NYA to EQBROAD_L1
**Date:** 2026-08-23
**Status:** PROPOSAL — NOT YET APPROVED
**Governing artifact:** `H01_EQUITY_VOLATILITY_ASYMMETRY_PROTOCOL_V1.md` (v1.1.0)

---

## 1. Purpose

This amendment proposes adding NYSE Composite (`NYA`) as the second primary-evaluable market in the `EQBROAD_L1` cell, upgrading that cell from EVIDENCE-LIMITED/DESCRIPTIVE to primary-eligible.

The amendment does NOT:
- Change the scientific hypothesis
- Change any statistical method
- Change any market-selection rule
- Change any eligibility criterion
- Change any threshold
- Change any inference procedure
- Add any market to other cells
- Modify EQBROAD_L2, EQTECH_L1, or EQTECH_L2

---

## 2. Existing EQBROAD_L1 Membership

Protocol §5 currently defines:

| Cell | Exposure | Era | Markets (identity) | Instrument | Source |
|---|---|---|---|---|---|
| **EQBROAD_L1** | Broad US large-cap | Historical (1982-04-21 → 2002-10-01) | `sp` | S&P 500 **futures**, front-month, ratio back-adjusted | HPD (frozen, in-repo) |

**Current status:** EQBROAD_L1 contains a single market (`sp`) → **EVIDENCE-LIMITED by construction** (protocol §16: "a cell supports a primary verdict iff it has ≥ 2 primary-evaluable markets").

---

## 3. Proposed Membership

| Cell | Exposure | Era | Markets (identity) | Instrument | Source |
|---|---|---|---|---|---|
| **EQBROAD_L1** | Broad US large-cap | Historical (1982-04-21 → 2002-10-01) | `sp`, `NYA` | S&P 500 **futures** (front-month, ratio back-adjusted) + NYSE Composite **cash index** (daily close) | HPD (frozen, in-repo) + Yahoo Finance (validated, in-repo) |

**Proposed status:** EQBROAD_L1 would contain two primary-evaluable markets → **primary-eligible** (subject to ≥30-pairs-per-stratum evaluability gate).

---

## 4. NYA Eligibility Evidence

### Data Integrity

| Check | Result |
|---|---|
| Row count | 5,163 |
| Date range | 1982-04-21 → 2002-09-30 |
| Duplicate dates | 0 |
| Non-positive values | 0 |
| Correct ordering | Yes |
| Close = Adj Close | Yes (100%) |
| Price type | Price-type index level (daily close) |

### Evaluability Prediction

With 5,163 daily observations spanning 20+ years across multiple market regimes (1987 crash, 1990s bull, 2000-02 bear), NYA is expected to produce ≥30 matched pairs per stratum for all 3 volatility-state terciles. Final evaluability is determined at execution.

### Independent Validation

FRED quarterly NYSE Composite observations independently validate the Yahoo NYA Close series:
- 80 quarter-end dates compared
- 76 exact matches (95.0%)
- 4 minor discrepancies (all <0.6%)
- No material contradictions

---

## 5. Historical Coverage

| Property | NYA | Requirement |
|---|---|---|
| Start date | 1982-04-21 | ≥ 1982-04-21 |
| End date | 2002-09-30 | ≤ 2002-10-01 |
| Coverage | Full H01 window except final day | Sufficient |
| 1-day gap | 2002-09-30 → 2002-10-01 | Handled by missing-day policy (§9) |

### Coverage Assessment

NYA covers the full H01 historical window. The protocol does not require every market to observe the literal `HISTORICAL_END` date; the missing-day policy (§9) handles incomplete windows by dropping them, not imputing.

---

## 6. Structural Distinctness

### NYA vs S&P 500 (`sp`)

| Attribute | NYSE Composite (NYA) | S&P 500 (`sp`) |
|---|---|---|
| **Universe** | All common stocks on NYSE (~2,000 names) | 500 selected large-cap US companies |
| **Selection** | All NYSE-listed stocks | Committee-selected, cap-weighted |
| **Sector breadth** | Full NYSE market (industrial, utility, transportation, financial) | Broad but curated |
| **Smallest constituents** | Includes micro/small-cap NYSE stocks | Excludes sub-500-rank names |
| **Exchange** | NYSE only | NYSE + Nasdaq + other |
| **Instrument type** | Cash index | Futures (front-month, ratio back-adjusted) |
| **Source** | Yahoo Finance | HPD |

### Distinctness Verdict

**STRUCTURALLY DISTINCT.** NYA and S&P 500 represent different broad-US exposures:
- NYA = full NYSE market (broader, includes smaller names)
- S&P 500 = curated large-cap (more concentrated, cross-exchange)

They share significant large-cap overlap but are not near-duplicates in the way NASDAQ100 and NASDAQCOM are (definition lock §7). The distinctness is comparable to SP500 vs DJIA in EQBROAD_L2 (different index families, same broad-US exposure, registered as distinct markets).

---

## 7. Exact Unchanged Protocol Parameters

The following parameters remain **completely unchanged**:

| Parameter | Value | Protocol Section |
|---|---|---|
| Scientific question | Classic volatility-response asymmetry | §2 |
| Equity prior | D > 0 (classic direction) | §3 |
| Scope | US-anchored, two distinct exposures | §4 |
| Era windows | HISTORICAL_END = 2002-10-01; CONTEMPORARY_START = 2016-08-15; CONTEMPORARY_END = 2026-08-14 | §5 |
| Shock definition | Daily close-to-close log return | §10 |
| Volatility response | ΔlnRV = ln(RV_forward) − ln(RV_backward) | §11 |
| Horizon | h = 5 trading days | §12 |
| Strata | 3 terciles of ln(RV_back) | §13 |
| Matching | Caliper c = 0.25 × SD(|r|), greedy one-to-one | §14 |
| Statistics | Per-market d_m = mean over 3 strata | §15 |
| Evaluability | ≥30 matched pairs per stratum | §16 |
| Bootstrap | L = 11, B = 10,000, seed 20260816 | §17 |
| Null inference | Null-imposing construction | §18 |
| Multiple comparisons | Holm, family of 4 cells, α = 0.05 | §19 |
| Cross-era design | No pooled estimator; descriptive consistency only | §20 |
| Secondary analyses | 10 pre-declared analyses | §21 |
| Data-quality gates | 10 frozen gates | §22 |
| Scientific decision rules | SUPPORT/CONTRADICTION/INCONCLUSIVE/EVIDENCE-LIMITED | §23 |

---

## 8. Exact Unchanged Inference Machinery

The following machinery remains **completely unchanged**:

- Bootstrap construction (circular calendar-block, L=11)
- Null construction (shock-response-level null transformation)
- p-value convention (Monte-Carlo, inclusive ≥)
- CI construction (percentile, 2.5%/97.5%)
- Holm correction (4-cell family, α=0.05)
- Empty-stratum rule
- Replicate aggregation rule
- NaN handling
- Evaluability gate (≥30 pairs/stratum, ≥2 markets per cell)
- Classification rules (SUPPORT/CONTRADICTION/INCONCLUSIVE/EVIDENCE-LIMITED)

---

## 9. No New Hypothesis

This amendment does NOT introduce:

- A new scientific question
- A new prior direction
- A new exposure
- A new era
- A new market-selection rule
- A new eligibility criterion
- A new statistical test
- A new inference method
- A new decision threshold
- A new data source type (cash index is already used in EQBROAD_L2 and EQTECH)

---

## 10. No New Market-Selection Rule

This amendment does NOT create:

- A rule for selecting markets based on expected results
- A rule for adding markets after seeing outcomes
- A rule for removing markets based on performance
- A rule for changing the universe post-execution

NYA is added because:
1. It is structurally distinct from S&P 500
2. It covers the required historical period
3. It has been independently validated
4. It completes the pre-existing EQBROAD_L1 evidence design

Any future universe change requires another formal amendment.

---

## 11. Execution Authorization Requirement

> **NO H01 EXECUTION IS AUTHORIZED BY THIS PROPOSAL.**

This proposal prepares the governance documentation only. Execution requires:

1. **Definition lock amendment approval** (Amendment A)
2. **Protocol amendment approval** (this document)
3. **Fresh independent implementation audit** of the amended protocol
4. **Explicit execution authorization** from the owner

---

## 12. Independent Audit Requirement

Before execution, the amended protocol must pass:

1. **Source-provenance audit** — verify NYA data integrity and FRED validation
2. **Implementation audit** — verify the execution script correctly handles NYA
3. **Gate audit** — verify all 10 data-quality gates pass for NYA
4. **Reproducibility audit** — verify NYA results are fully reproducible

---

## 13. Owner Approval Requirement

The owner must explicitly approve:

1. The definition lock amendment (Amendment A)
2. The protocol amendment (Amendment B)
3. The execution authorization (separate from amendment approval)

---

## 14. Research-Sequence Protection

The required sequence is:

> **Amendment proposal → independent audit → owner approval → frozen amended protocol → single authorized execution → independent adjudication**

No step may be skipped. No execution occurs merely because the proposal exists.

---

## 15. Outcome-Dependent Design Prohibition

Explicitly prohibited:

- Removing NYA if results are weak
- Adding another market if NYA fails
- Choosing a different market after seeing NYA results
- Changing the historical window
- Changing the price field after execution
- Changing definitions based on results

Any future universe change requires another amendment.

---

## 16. Amendment Record

| Property | Value |
|---|---|
| **Amendment type** | Universe addition |
| **Target cell** | EQBROAD_L1 |
| **Market added** | `NYA` (NYSE Composite Index) |
| **Source** | Yahoo Finance `^NYA` (validated by FRED) |
| **Definition lock change** | §18 Yahoo exclusion exception for NYA |
| **Protocol change** | §5 EQBROAD_L1 market list; §7 NYA data input; §8 NYA preprocessing; §24 NYA licensing |
| **Scientific invariants preserved** | All (hypothesis, statistic, inference, thresholds) |
| **Execution authorized** | NO |
| **Owner approval required** | YES |

---

## 17. Integrity

- This is a governance amendment proposal only
- No H01 statistic has been computed
- No experiment has been run
- No data has been acquired
- No protocol has been modified
- No definition lock has been modified
- No session handoff has been updated
- No commit has been made
