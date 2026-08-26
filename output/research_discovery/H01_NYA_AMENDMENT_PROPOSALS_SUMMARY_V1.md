# QUANTFORGE — H01 EQUITY V1

# NYA FORMAL GOVERNANCE AMENDMENT PROPOSALS — SUMMARY

**Status:** TWO PROPOSALS PREPARED — EXECUTION NOT AUTHORIZED
**Date:** 2026-08-23

---

## 1. Amendment Status

**TWO PROPOSALS PREPARED — EXECUTION NOT AUTHORIZED**

Two narrowly scoped amendment proposals have been prepared to add NYSE Composite (`NYA`) as the second primary-evaluable market in `EQBROAD_L1`. These are governance proposals only; no execution is authorized.

---

## 2. Definition-Lock Change (Amendment A)

**File:** `output/research_discovery/H01_NYA_DEFINITION_LOCK_AMENDMENT_PROPOSAL_V1.md`

### What Changes

A single exception is added to definition lock §18:

> **Exception — NYSE Composite (`NYA`):** The existing Yahoo Finance `^NYA` daily Close dataset is approved as a primary source for NYA, subject to immutable artifact, SHA-256 fingerprint, provenance record, and independent FRED validation controls.

### What Does NOT Change

- The general Yahoo exclusion for other markets
- Any scientific hypothesis, prior, or scope
- Any market-selection rule
- Any eligibility criterion
- Any statistical method
- Any threshold or inference procedure

---

## 3. Protocol Change (Amendment B)

**File:** `output/research_discovery/H01_NYA_PROTOCOL_UNIVERSE_AMENDMENT_PROPOSAL_V1.md`

### What Changes

EQBROAD_L1 market membership:

| Before | After |
|---|---|
| `sp` (S&P 500 futures) | `sp` (S&P 500 futures) + `NYA` (NYSE Composite cash index) |

### What Does NOT Change

- EQBROAD_L2, EQTECH_L1, EQTECH_L2
- Any statistical parameter (bootstrap, null, CI, Holm, alpha)
- Any inference method
- Any evaluability rule
- Any data-quality gate
- Any secondary analysis

---

## 4. Scientific Invariants

Everything intentionally unchanged:

| Invariant | Status |
|---|---|
| Scientific hypothesis | UNCHANGED |
| Equity prior (D > 0) | UNCHANGED |
| Scope (US-anchored, two exposures) | UNCHANGED |
| Shock definition | UNCHANGED |
| Volatility response | UNCHANGED |
| Horizon (5 days) | UNCHANGED |
| Strata (3 terciles) | UNCHANGED |
| Matching (caliper, greedy) | UNCHANGED |
| Bootstrap (L=11, B=10,000, seed 20260816) | UNCHANGED |
| Null construction | UNCHANGED |
| CI construction | UNCHANGED |
| Holm correction (4-cell family, α=0.05) | UNCHANGED |
| Evaluability (≥30 pairs/stratum, ≥2 markets) | UNCHANGED |
| Classification rules | UNCHANGED |
| Era windows | UNCHANGED |
| Data-quality gates | UNCHANGED |

---

## 5. NYA Evidence Summary

| Property | Value |
|---|---|
| **Date range** | 1982-04-21 → 2002-09-30 |
| **Row count** | 5,163 |
| **Provenance** | Yahoo Finance `^NYA` historical data page |
| **SHA-256** | `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f` |
| **FRED validation** | 76/80 quarter-end dates exact match (95.0%) |
| **Structural distinctness** | NYSE Composite (~2,000 NYSE stocks) vs S&P 500 (curated 500) — STRUCTURALLY DISTINCT |
| **Price field** | Close (price-type index level) |
| **OHLC pattern** | O=H=L=C (100% — known Yahoo limitation; no H01 impact) |

---

## 6. Licensing

| Component | Status |
|---|---|
| Yahoo Finance data access | CLEAR (freely accessible) |
| Yahoo Finance archival rights | **PENDING** (requires owner acceptance) |
| FRED validation source | CLEAR (public Federal Reserve data) |

**Owner requirement:** Must explicitly accept the Yahoo-sourced NYA dataset for internal research use, acknowledging Yahoo Terms of Service govern data use.

---

## 7. Execution Gate

> **NO H01 EXECUTION IS AUTHORIZED BY THESE PROPOSALS.**

Execution requires:

1. Independent audit of both proposals
2. Owner approval of definition lock amendment
3. Owner approval of protocol amendment
4. Fresh independent implementation audit
5. Explicit execution authorization

---

## 8. Required Next Task

**Independent read-only audit of both NYA amendment proposals**

The two proposals must pass an independent, adversarial, read-only audit before owner approval is requested. The audit should verify:

- Amendment A correctly scopes the Yahoo exception
- Amendment B correctly adds NYA to EQBROAD_L1
- No scientific invariants are violated
- No unintended changes are introduced
- All provenance controls are adequate
- The governance sequence is preserved

---

## 9. Files Created

| File | Purpose |
|---|---|
| `output/research_discovery/H01_NYA_DEFINITION_LOCK_AMENDMENT_PROPOSAL_V1.md` | Amendment A: Source-governance exception |
| `output/research_discovery/H01_NYA_PROTOCOL_UNIVERSE_AMENDMENT_PROPOSAL_V1.md` | Amendment B: Universe addition |
| `output/research_discovery/H01_NYA_AMENDMENT_PROPOSALS_SUMMARY_V1.md` | This summary document |

---

## 10. Governance Firewall

This task has:
- ✅ NOT modified any protocol or definition lock
- ✅ NOT added NYA to the universe
- ✅ NOT executed H01
- ✅ NOT calculated new statistics
- ✅ NOT purchased data
- ✅ NOT consumed DataBento credits
- ✅ NOT created a new DISC
- ✅ NOT updated SESSION_HANDOFF.md
- ✅ NOT committed changes
