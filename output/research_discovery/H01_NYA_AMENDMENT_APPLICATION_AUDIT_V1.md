# QUANTFORGE — H01 EQUITY V1

# NYA AMENDMENT APPLICATION — IMPLEMENTATION AUDIT

**Audit type:** Independent implementation audit of applied amendments
**Date:** 2026-08-23
**Status:** COMPLETE

---

## 1. Owner Authorization

**APPROVED AND APPLIED**

The owner authorized the two audited NYA amendments on 2026-08-23. Both amendments have been applied to the frozen governance artifacts.

---

## 2. Amendment A — Definition Lock

**Status: APPLIED**

### What Changed

Definition lock `H01_EQUITY_VOLATILITY_ASYMMETRY_DEFINITION_LOCK_V1.md`:

| Section | Change | Status |
|---|---|---|
| Header | Version 1.0.0 → 1.1.0; date amended 2026-08-23 | APPROVED |
| §5 (Historical Era table) | Added `NYA` row: Yahoo Finance `^NYA`, NYSE Composite cash index, 1982-04-21 → 2002-09-30 | APPROVED |
| §18 (Licensing) | Added NYA exception (§18a): Yahoo `^NYA` daily Close approved as primary source with provenance/SHA-256/FRED-validation controls | APPROVED |

### What Did NOT Change

- §2 (Scientific Statement) — UNCHANGED
- §3 (Equity Prior) — UNCHANGED
- §4 (Scope) — UNCHANGED
- §6 (Futures vs Cash) — UNCHANGED
- §7 (Nasdaq Family) — UNCHANGED
- §8 (USATECHIDXUSD) — UNCHANGED
- §9 (Shock Definition) — UNCHANGED
- §10 (Equal-Magnitude) — UNCHANGED
- §11 (Volatility Response) — UNCHANGED
- §12 (Horizon) — UNCHANGED
- §13 (Conditioning) — UNCHANGED
- §14 (Aggregation) — UNCHANGED
- §15 (Generalization) — UNCHANGED
- §16 (Falsification) — UNCHANGED
- §17 (Independence Firewall) — UNCHANGED
- General Yahoo exclusion for other markets — PRESERVED

---

## 3. Amendment B — Protocol / Universe

**Status: APPLIED**

### What Changed

Protocol `H01_EQUITY_VOLATILITY_ASYMMETRY_PROTOCOL_V1.md`:

| Section | Change | Status |
|---|---|---|
| Header | Version 1.1.0 → 1.2.0; version history updated | APPROVED |
| §5 (Universe table) | EQBROAD_L1 markets: `sp` → `sp`, `NYA`; instruments/sources updated | APPROVED |
| §5 (Market identity) | Added `NYA` identity: NYSE Composite cash index, Yahoo `^NYA`, FRED-validated, §18a exception | APPROVED |
| §7 (Data Inputs) | Added NYA: `docs/NYA_DATA.html`, SHA-256 `367b103...`, Close field, coverage 1982-04-21 → 2002-09-30, FRED validation | APPROVED |
| §8 (Preprocessing) | Added NYA era truncation: full validated history, 1-day terminal gap handled by §9 | APPROVED |
| §9 (Roll-Day Rules) | Updated: "FRED cash indices and NYA have no roll days" | APPROVED |
| §16 (Evaluability) | Updated: EQBROAD_L1 now has 2 markets → primary-eligible | APPROVED |
| §24 (Licensing) | Added NYA row: EXCEPTION GRANTED (§18a), archival rights PENDING | APPROVED |

### What Did NOT Change

- §1 (Purpose) — UNCHANGED
- §2 (Scientific Question) — UNCHANGED
- §3 (Equity Prior) — UNCHANGED
- §4 (Scope) — UNCHANGED
- §6 (Source-Type Rule) — UNCHANGED
- §10 (Shock Definition) — UNCHANGED
- §11 (Volatility Response) — UNCHANGED
- §12 (Horizon) — UNCHANGED
- §13 (Volatility-State Conditioning) — UNCHANGED
- §14 (Matching) — UNCHANGED
- §15 (Statistics) — UNCHANGED
- §17 (Dependence-Aware Inference) — UNCHANGED
- §18 (Null-Inference) — UNCHANGED
- §19 (Multiple Comparisons) — UNCHANGED
- §20 (Cross-Era Design) — UNCHANGED
- §21 (Secondary Analyses) — UNCHANGED
- §22 (Data-Quality Gates) — UNCHANGED
- §23 (Scientific Decision Rules) — UNCHANGED
- §25 (Outcome-Blind Self-Audit) — UNCHANGED
- §26 (Authorized Next Action) — UNCHANGED
- §27 (Integrity Statement) — UNCHANGED
- EQBROAD_L2, EQTECH_L1, EQTECH_L2 — UNCHANGED

---

## 4. Changed Sections Summary

| File | Section | Change Type | Approved? |
|---|---|---|---|
| Definition Lock | Header | Version/amendment date | ✅ YES |
| Definition Lock | §5 | NYA added to historical era table | ✅ YES |
| Definition Lock | §18 | NYA Yahoo source exception | ✅ YES |
| Protocol | Header | Version/amendment history | ✅ YES |
| Protocol | §5 | EQBROAD_L1 = sp + NYA | ✅ YES |
| Protocol | §5 | NYA market identity | ✅ YES |
| Protocol | §7 | NYA data input + SHA-256 | ✅ YES |
| Protocol | §8 | NYA era truncation | ✅ YES |
| Protocol | §9 | NYA roll-day note | ✅ YES |
| Protocol | §16 | EQBROAD_L1 evaluability | ✅ YES |
| Protocol | §24 | NYA licensing entry | ✅ YES |

**Total: 11 sections changed across 2 files. All APPROVED. No unapproved changes.**

---

## 5. Scientific Invariants — Verified Unchanged

| Invariant | Definition Lock Section | Protocol Section | Changed? |
|---|---|---|---|
| Scientific hypothesis | §2 | §2 | NO |
| Equity prior (D > 0) | §3 | §3 | NO |
| Scope (US-anchored, two exposures) | §4 | §4 | NO |
| Shock definition | §9 | §10 | NO |
| Equal-magnitude concept | §10 | §14 | NO |
| Volatility response | §11 | §11 | NO |
| Horizon (5 days) | §12 | §12 | NO |
| Volatility-state conditioning | §13 | §13 | NO |
| Cross-market aggregation | §14 | §15 | NO |
| Generalization claim | §15 | §20 | NO |
| Falsification concept | §16 | §23 | NO |
| Independence firewall | §17 | §21 | NO |

**ALL SCIENTIFIC INVARIANTS VERIFIED UNCHANGED.**

---

## 6. Multiple-Testing Family — Verified Unchanged

Protocol §19 states:

> **Primary family:** the **4 cells** of §5 — EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2.

| Property | Before Amendment | After Amendment | Changed? |
|---|---|---|---|
| Family size | 4 cells | 4 cells | NO |
| Family composition | EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2 | EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2 | NO |
| Holm correction | 4-member family, α = 0.05 | 4-member family, α = 0.05 | NO |
| Market-level changes | EQBROAD_L1 = 1 market | EQBROAD_L1 = 2 markets | YES (data scope only) |

**The family is defined at the cell level, not the market level. Adding NYA to EQBROAD_L1 changes the observations within that cell, not the number of hypothesis-test cells.**

---

## 7. NYA Source Artifact Binding

| Property | Value | Verified? |
|---|---|---|
| Source file | `docs/NYA_DATA.html` | ✅ |
| SHA-256 | `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f` | ✅ |
| Field | `Close` (price-type index level) | ✅ |
| Date range | 1982-04-21 → 2002-09-30 | ✅ |
| Row count | 5,163 | ✅ |
| Provenance | Yahoo Finance `^NYA` historical data page | ✅ |
| Independent validation | FRED quarterly (80 obs, 76 exact matches) | ✅ |
| Derived copy | `US_Equity_Data.csv` identified as same source | ✅ |

**NYA source artifact properly bound in both definition lock (§18a) and protocol (§7).**

---

## 8. Implementation Audit Verdict

**PASS**

Every changed section is approved. No unapproved changes were found. All scientific invariants, multiple-comparison family, and inference machinery remain unchanged.

---

## 9. Final Governance State

**H01 EQUITY V1 — AMENDED WITH NYA — FROZEN / READY FOR FINAL EXECUTION-READINESS AUDIT**

| Property | Status |
|---|---|
| Definition lock | v1.1.0 (NYA exception applied) |
| Protocol | v1.2.0 (NYA universe applied) |
| Scientific object | UNCHANGED |
| NYA included | YES (EQBROAD_L1 = sp + NYA) |
| Execution authorized | NO |
| Next task | Independent final execution-readiness audit |

---

## 10. Execution Authorization

> **NO H01 EXECUTION OCCURRED.**

> **NO H01 EXECUTION IS AUTHORIZED BY THIS TASK.**

---

## 11. Required Next Task

**Independent final execution-readiness audit of the amended H01 protocol**

The amended protocol must pass a fresh independent implementation audit before execution is authorized.

---

## 12. Integrity

- Owner authorization: YES (2026-08-23)
- Amendments applied: YES (both A and B)
- Implementation audit: PASS
- No execution: YES
- No data download: YES
- No statistics computed: YES
- No new DISC: YES
- No session handoff updated: YES
- No commit: YES
