# QUANTFORGE — H01 HISTORICAL BROAD-US EQUITY DATA ACQUISITION & SOURCE VERIFICATION V1

**Mission:** determine whether the H01 Equity Track A evidence gap — a second *structurally distinct* historical (≈1982–2002) broad-US equity exposure — can be legitimately acquired and validated from free/archiveable sources.
**Mode:** outcome-blind source discovery + identity/depth/integrity/licensing verification. **No H01 statistic was computed** (no D, d_m, p, CI, shock, RV, or volatility-response asymmetry); prices were inspected for SOURCE/IDENTITY/INTEGRITY/PROVENANCE only.
**Governing position (SOURCE-DERIVED FACT, from DISC-023 / adjudication / handoff):** EQBROAD_L1 is EVIDENCE-LIMITED because only `sp` exists historically; the next legitimate task is this acquisition/source-verification task; no universe amendment is authorized by this task.

---

## 1. Scientific Evidence Gap (GOVERNANCE DECISION / SOURCE-DERIVED FACT)

- Historical broad-US exposure currently = **only `sp`** (HPD S&P 500 futures, CORE VALID, 1982-04-21 → 2002-10-01) → EQBROAD_L1 is EVIDENCE-LIMITED under the frozen ≥2-evaluable-market rule.
- Contemporary broad-US = SP500 + DJIA (FRED) → SUPPORT; but the historical leg has no second market.
- The gap is **historical broad-US multi-market replication**. The desired object is `sp` + **at least one structurally distinct** broad-US equity exposure — NOT another technology index, NOT a near-duplicate representation of the same large-cap exposure (definition-lock accounting: SP500 + DJIA = one broad-US exposure; market count ≠ exposure count).

## 2. Source Landscape (SOURCE-DERIVED FACT, verified this session)

### HPD (in-repository archive) — EXHAUSTED
- Full archive = 32 roots; **exactly one** US equity root (`sp`). `aor` (AllOrds) and `cac` (CAC 40) are quarantined RESOLVED-NONUS; `lj`/`ll` (Gilt/UK) quarantined RESOLVED-NONUS; `cr` (CRB) is an INDEX_COMMODITY; no `nd` (Nasdaq 100) or `md` (S&P MidCap) roots exist. (Verified against `FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv`, `HPD_MANIFEST.csv`.)

### FRED — NO DEEP HISTORICAL BROAD-US SERIES REMAINS
- SP500 and DJIA: daily, but **2016-08-15 onward only** (verified this session: 2,610 rows each; no pre-2016 history).
- NASDAQCOM (1971+) / NASDAQ100 (1986+): deep but **US-technology exposure**, not broad-US.
- **Wilshire family (WILL5000PR/WILL5000IND etc.): REMOVED from FRED on June 3, 2024** (SOURCE-DERIVED FACT, St. Louis Fed announcement, April 9, 2024: removed from the database, Excel add-in, mobile apps, APIs, and all FRED services; contact `index.access@wilshire.com` for Wilshire index data). The only deep-historical total-market US series FRED once hosted is therefore **unavailable** (verified this session: the series pages return "Error — St. Louis Fed").
- No other deep-historical broad-US daily price series exists on FRED (no Russell daily, no S&P MidCap, no NYSE Composite).

### Yahoo Finance — depth-capable, license-RESTRICTED
- ^GSPC (S&P 500 cash, 1970+), ^DJI (Dow), ^RUT (Russell 2000, **1987+ full depth**, verified this session: 9,806 rows from 1987-09-10), ^W5000 (Wilshire).
- **License RESTRICTED** (SOURCE-DERIVED FACT, prior data-source audit): official Yahoo API terminated 2017 for ToS abuse; the chart endpoint is undocumented/reverse-engineered; ToS prohibit redistribution. Read-only validation use only — **not archiveable**.
- Access limitation observed this session: the chart API serves ≈34 years of daily bars (^DJI from 1982 requested → returned 1992-01-02 onward; the 1982–1991 window is not retrievable via this endpoint).

### Stooq — license-RESTRICTED and endpoint-blocked
- ^SPX/^DJI/^RUT etc. exist; direct CSV endpoint and static bulk blocked (JS proof-of-work challenge / HTTP 401, verified in the prior data-source audit); terms limit use to personal use. Not archiveable.

### Official / exchange / academic — not viable for this gap
- S&P Dow Jones Indices: no free machine-readable daily history (Excel-based, limited depth).
- Nasdaq official API: NDX/NCOMP only (technology exposure; early history 1996-2003 unreliable, documented in the acquisition report).
- Academic (Shiller, Kenneth French): **monthly** frequency — insufficient for the daily H01 object (SOURCE-DERIVED FACT, prior audit).

### Paid providers (Tier 3, future alternatives ONLY — nothing purchased, no authorization)
- Norgate Data (S&P 500 cash 1950+, DJIA 1915+, NYSE Composite, Wilshire, Russell variants; clean licensing at cost), CSI, Databento. These are the only currently-known route to a second structurally distinct historical broad-US series **with archival rights**.

## 3. Exposure Distinctness (the binding constraint; GOVERNANCE DECISION / SOURCE-DERIVED FACT)

- Under the frozen definition-lock accounting (SP500 + DJIA = **one** broad-US large-cap exposure; NDX ⊂ NCOMP = one tech exposure), the required second historical object must be a **different segment or breadth** of the US equity market, not another large-cap index:
  - **^DJI / ^GSPC (Dow / S&P 500 cash): FAIL G2** — same broad-US large-cap exposure as `sp`; would add market count, not exposure count.
  - **^RUT (Russell 2000, small-cap): PASSES G1+G2** — genuinely distinct US equity segment (small-cap), 1987+ depth (≈15 years of the 20-year `sp` era) — but **license-RESTRICTED** (G6 FAIL).
  - **Wilshire 5000 (total market): G1/G2 defensible** (total-market breadth vs large-cap) — but **removed from FRED**; retrievable only via license inquiry or paid vendors.
  - **NASDAQ family: FAIL G1** — technology exposure, excluded by the scientific purpose ("structurally distinct broad-US," explicitly not another tech index).

## 4. Data Integrity of the Depth-Capable Free Candidates (SOURCE-DERIVED FACT, bounded checks this session)

- **Cross-source fidelity — Dow (Yahoo ^DJI vs frozen FRED DJIA snapshot, 2016-08-15 → 2026-08-14):** 2,514 common dates; median |relative level diff| = **0.0000%**, p99 = 0.0000%, max = 0.0422% (rounding); daily-return agreement median **0.00 bp**, p99 0.00 bp. The two providers' Dow series are identical to machine precision — establishing both that the Yahoo Dow data is faithful AND that the frozen FRED DJIA snapshot is authentic (corroboration of the already-validated input).
- **^RUT:** 9,806 daily rows, 1987-09-10 → 2026-08-14, no structural anomalies in the bounded probe; inception value ≈ 168.97 consistent with the Russell 2000's 1978 base (135) scaled through 1987.
- **^DJI anchor:** 2000-01-14 close 11,722.98 — matches the documented Dow dot-com peak exactly.
- These checks are **source-integrity only**; no H01 response statistic was computed.

## 5. Licensing / Archival Status (SOURCE-DERIVED FACT; no claim of permission)

| Candidate | License | Archiveable | Path to clearance |
|---|---|---|---|
| HPD `sp` | PENDING (frozen record) | in-repo | existing standing record |
| FRED SP500/DJIA/Nasdaq | platform CLEAR; underlying © PENDING | via frozen snapshot | permission requests PREPARED/NOT SENT |
| FRED Wilshire | **REMOVED** (unavailable) | n/a | direct inquiry `index.access@wilshire.com` (license path only, not authorized here) |
| Yahoo ^DJI/^GSPC/^RUT | **RESTRICTED** | **NO** | no free archival route |
| Stooq | **RESTRICTED** (personal use) | **NO** | no free archival route |
| Paid (Norgate/CSI/Databento) | commercial, clean archival at cost | YES (at cost) | separate procurement authorization required |

## 6. Decision Gates (evaluated on identity + structural exposure + depth + integrity + reproducibility + licensing — NEVER on H01 performance)

| Gate | ^RUT (Yahoo) | Wilshire 5000 | ^DJI (Yahoo) | FRED SP500/DJIA |
|---|---|---|---|---|
| G1 Broad-US identity | PASS (small-cap US) | PASS (total market US) | PASS (large-cap US) | PASS |
| G2 Structurally distinct from `sp` | **PASS** (small-cap segment) | **PASS-ish** (total-market breadth; definition-stage judgment) | **FAIL** (same large-cap exposure) | **FAIL** (same exposure) |
| G3 Historical depth vs 1982–2002 | PARTIAL (1987–2002 ≈ 15y) | PASS (1971+) — if retrievable | PARTIAL (API ≈1992+) | FAIL (2016+) |
| G4 Data integrity | PASS (bounded probe clean) | (removed from FRED) | PASS (0.00 bp vs FRED) | PASS (frozen, validated) |
| G5 Reproducibility | FAIL (undocumented API, ToS) | n/a on FRED | FAIL | PASS (fredgraph) |
| G6 Licensing / archival | **FAIL (RESTRICTED)** | PENDING via direct inquiry / paid | **FAIL (RESTRICTED)** | FAIL for depth (none exists) |
| G7 Cross-source fidelity | (no independent free daily) | (removed) | PASS (0.00 bp) | PASS (already validated) |

## 7. Governance Outcome (GOVERNANCE DECISION)

**C — NO SUITABLE ADDITIONAL HISTORICAL BROAD-US SOURCE FOUND** (free/archiveable sources, as of 2026-08-16).

- Every free source with historical depth is **license-RESTRICTED** (Yahoo, Stooq) or **no longer available** (FRED Wilshire, removed June 3, 2024), and every archiveable free source lacks the required depth (FRED SP500/DJIA 2016+) or the required distinctness (Nasdaq = tech). HPD is exhausted (`sp` only).
- The **evidence gap remains**: EQBROAD_L1 stays single-market; no universe amendment is authorized by this outcome.
- Recorded future alternatives (require separate operator authorization — NOT authorized here): (i) **paid provider** (Norgate/CSI/Databento — clean archival licensing at cost; e.g., DJIA cash 1915+, NYSE Composite, Wilshire, Russell, S&P 500 cash 1950+); (ii) a **Wilshire direct licensing inquiry** to `index.access@wilshire.com` (the contact named in FRED's removal notice) for the Wilshire 5000 total-market series.

## 8. Exact Next Legitimate Task

- **A — if the operator authorizes a paid acquisition path:** a procurement + source-verification task for one validated second historical broad-US series (e.g., a small-cap or total-market index with archival rights), then the standard chain: `source validation → governance decision → definition/universe amendment → new pre-registration → independent audit → execution`.
- **B — if the operator prefers a licensing inquiry first:** an operator-dispatched (NOT-sent-by-research) inquiry to Wilshire (`index.access@wilshire.com`) and/or the chosen paid vendor, with the response recorded before any acquisition.
- Neither path may skip the amendment chain; neither path may select a market by expected H01 performance; **no H01 Equity V1 modification occurs at any point in this task or its immediate successors.**

## 9. Prohibited Follow-Up

Adding any market to the frozen Equity V1 universe without the amendment chain; purchasing data without operator authorization; using Yahoo/Stooq data as anything other than read-only validation; selecting a market because it is likely to strengthen the prior result; computing any H01 statistic on candidates; re-opening commodities/TSMOM/Mean Reversion; international expansion; any protocol or definition-lock change.

## 10. Integrity

Strictly outcome-blind and read-only with respect to all scientific/protocol artifacts. The only repository change is this report. Bounded probes (FRED error responses for the removed Wilshire series; Yahoo ^DJI/^RUT in-memory only; the FRED DJIA snapshot read from the frozen external temp sample) were downloaded to the external temp directory only — nothing placed in the repository, no new dataset, no H01 statistic, no shock/RV/asymmetry/p-value computation, no market selected by outcome, no source chosen. The frozen H01 Equity V1 artifacts, the definition lock, and all governance/BOE/Assembly/Deployment records are untouched. Labeling: factual claims are SOURCE-DERIVED; exposure-distinctness judgments are GOVERNANCE/DEFINITION-STAGE DECISIONS flagged for the amendment chain; no MODEL INFERENCE was performed (no statistical modeling anywhere in this task).
