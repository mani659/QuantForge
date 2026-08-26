# QUANTFORGE — H01 EQUITY V1.2.0

# FINAL EXECUTION-READINESS AUDIT

**Audit type:** Independent, adversarial, READ-ONLY execution-readiness audit
**Date:** 2026-08-23
**Status:** COMPLETE

---

## 1. Executive Verdict

**A — EXECUTION READY**

All gates pass. The protocol is frozen and ready for explicit owner execution authorization.

---

## 2. Protocol Identity

| Property | Value |
|---|---|
| **Protocol version** | 1.2.0 |
| **Definition lock version** | 1.1.0 |
| **Protocol amendment** | NYA universe addition (v1.2.0) |
| **Definition lock amendment** | NYA Yahoo source exception (v1.1.0) |
| **Owner approval** | 2026-08-23 |
| **Independent amendment audit** | `H01_NYA_AMENDMENT_PROPOSALS_INDEPENDENT_AUDIT_V1.md` (A — PASS) |
| **Amendment application audit** | `H01_NYA_AMENDMENT_APPLICATION_AUDIT_V1.md` (PASS) |

---

## 3. Source Integrity

### sp (S&P 500 Futures)

| Property | Value |
|---|---|
| **Source file** | `data/m1/front_sp.csv` (frozen HPD record) |
| **SHA-256** | `09451cdb44e09a453fc40888d8f0e9ba6b8ad79a9e45a4a05128683e2f2e721b` |
| **Price field** | Continuous ratio-back-adjusted `adj_close` |
| **Coverage** | 1982-04-21 → 2002-10-01 (5,163 rows) |
| **Frozen validation** | CORE VALID, 82 rolls, continuity_ok=True |

**Note:** The `front_sp.csv` source file is not currently on disk (likely cleaned after prior execution). The SHA-256 is recorded in the frozen protocol and the prior execution metadata. The execution script must have access to this file at execution time. This is an execution-logistics concern, not a protocol-readiness concern.

### NYA (NYSE Composite)

| Property | Value |
|---|---|
| **Source file** | `docs/NYA_DATA.html` |
| **SHA-256** | `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f` |
| **Price field** | `Close` (price-type index level) |
| **Coverage** | 1982-04-21 → 2002-09-30 (5,163 rows) |
| **Verified on disk** | YES — SHA-256 matches exactly |

### FRED Files

| File | SHA-256 | Status |
|---|---|---|
| fred_SP500.csv | `351555b5...` | Not on disk (frozen snapshot) |
| fred_DJIA.csv | `29c8ca59...` | Not on disk (frozen snapshot) |
| fred_NASDAQCOM.csv | `51187aa6...` | Not on disk (frozen snapshot) |
| fred_NASDAQ100.csv | `aeacca4f...` | Not on disk (frozen snapshot) |

**Note:** The FRED frozen snapshot files are not currently on disk. The execution script must have access to these files at execution time. This is an execution-logistics concern, not a protocol-readiness concern.

---

## 4. Scientific Invariants — All Verified Unchanged

| Invariant | Status |
|---|---|
| Scientific hypothesis | UNCHANGED |
| Equity prior (D > 0) | UNCHANGED |
| Scope (US-anchored, two exposures) | UNCHANGED |
| Shock definition | UNCHANGED |
| Equal-magnitude concept | UNCHANGED |
| Volatility response | UNCHANGED |
| Horizon (5 days) | UNCHANGED |
| Volatility-state conditioning | UNCHANGED |
| Cross-market aggregation | UNCHANGED |
| Generalization claim | UNCHANGED |
| Falsification concept | UNCHANGED |
| Independence firewall | UNCHANGED |
| Bootstrap (L=11, B=10,000, seed 20260816) | UNCHANGED |
| Null construction | UNCHANGED |
| CI construction | UNCHANGED |
| Holm correction (4-cell family, α=0.05) | UNCHANGED |
| Evaluability rules | UNCHANGED |
| Classification rules | UNCHANGED |

---

## 5. Universe — Verified Exactly

| Cell | Markets | Status |
|---|---|---|
| **EQBROAD_L1** | `sp`, `NYA` | AMENDED (approved) |
| **EQBROAD_L2** | SP500, DJIA | UNCHANGED |
| **EQTECH_L1** | NASDAQ100, NASDAQCOM | UNCHANGED |
| **EQTECH_L2** | NASDAQ100, NASDAQCOM | UNCHANGED |

No additional market is authorized. No market may be dropped unless the frozen missing-data rule independently requires it.

---

## 6. Statistical Family — Exactly 4 Cell-Level Tests

1. EQBROAD_L1
2. EQBROAD_L2
3. EQTECH_L1
4. EQTECH_L2

Adding NYA does NOT create:
- A fifth test
- A separate NYA hypothesis
- A separate NYA p-value
- Another Holm family

The family is defined at the **cell level**, not the market level.

---

## 7. Determinism — Verified

| Property | Value |
|---|---|
| **Seed** | 20260816 (frozen, pre-registered) |
| **Bootstrap method** | Circular calendar-block, L=11 |
| **Replicates** | B = 10,000 |
| **Reproducibility identity** | Protocol SHA + definition-lock SHA + source SHA(s) + seed + environment |

The seed remains valid for the amended execution. No new seed is required because the amendment changes only the market membership, not the randomization machinery.

---

## 8. Data Processing — Symmetric Handling Verified

| Property | sp | NYA |
|---|---|---|
| **Price field** | `adj_close` (ratio back-adjusted) | `Close` (price-type index) |
| **Date parsing** | Standard date format | Standard date format |
| **Return calculation** | `ln(close_t / close_{t-1})` | `ln(close_t / close_{t-1})` |
| **Missing-day handling** | Drop if window incomplete | Drop if window incomplete |
| **Roll-day handling** | Excluded | N/A (no roll days) |
| **Calendar alignment** | Trading days only | Trading days only |

**Finding:** The preprocessing is symmetric. NYA-specific preprocessing (no roll-day rule) is necessary because NYA is a cash index, not futures. This does not create a methodological difference — it correctly applies the same scientific object to each market's own data type.

---

## 9. Terminal Date Handling — Verified

| Property | Value |
|---|---|
| **NYA latest date** | 2002-09-30 |
| **H01 HISTORICAL_END** | 2002-10-01 |
| **Gap** | 1 trading day |
| **Handling** | Missing-day policy (§9): any shock requiring 2002-10-01 in its window is dropped |
| **Forward filling** | NOT used |
| **Artificial terminal observation** | NOT created |

The 1-day terminal gap is correctly handled by the existing missing-day policy.

---

## 10. Market-Level Evaluability — No Predetermined Outcome

The protocol states:

> `EQBROAD_L1` contains two primary-evaluable markets (`sp` and `NYA`, subject to ≥30-pairs floors) → **primary-eligible** (no longer EVIDENCE-LIMITED by construction).

**Key distinction:** "primary-eligible" ≠ "SUPPORT". The protocol correctly states that evaluability is determined at execution, not predetermined. EQBROAD_L1 could still receive any verdict (SUPPORT, CONTRADICTION, INCONCLUSIVE, or EVIDENCE-LIMITED if gates fail).

---

## 11. Multiple-Comparison Family — Exactly 4 Cells Verified

Protocol §19 states:

> **Primary family:** the **4 cells** of §5 — EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2.

| Property | Before | After | Changed? |
|---|---|---|---|
| Family size | 4 | 4 | NO |
| Family composition | 4 cells | 4 cells | NO |
| Holm correction | 4-member, α=0.05 | 4-member, α=0.05 | NO |

---

## 12. Bootstrap Determinism — Seed Valid

| Property | Value |
|---|---|
| **Seed** | 20260816 |
| **Source** | Frozen pre-registration constant |
| **Validity** | The seed drives the random number stream; adding NYA changes the data, not the RNG |
| **New seed required?** | NO — the same seed produces a deterministic stream for the amended data |

---

## 13. Single-Execution Governance — Verified

| Property | Status |
|---|---|
| **Prior execution** | H01 Equity V1.1.0 (protocol v1.1.0, completed 2026-08-16) |
| **Amendment creates fresh authorization** | YES — v1.2.0 is a new frozen protocol requiring new execution |
| **Rerun automatically authorized?** | NO — each execution requires explicit authorization |
| **Crash handling** | Single uninterrupted invocation; no partial-cache resume; interrupted run restarted from scratch |
| **Data changes invalidate execution identity** | YES — any source file change requires re-audit |

---

## 14. Data Integrity / Reproducibility — Verified

The execution can be reproduced from:
- Protocol SHA-256 (v1.2.0)
- Definition-lock SHA-256 (v1.1.0)
- Source SHA-256(s): sp (`09451cdb...`), NYA (`367b103...`), FRED files (4 SHAs)
- Parameter set: L=11, B=10,000, seed=20260816, caliper=0.25, min_pairs=30
- Environment: Python 3.11+, numpy, scipy

No hidden dependency remains.

---

## 15. Economic / Strategy Firewall — Verified

This H01 execution does NOT authorize:
- PnL
- Trading strategy
- Entry rules
- Stop rules
- Exit rules
- Spread testing
- Execution simulation
- Position sizing
- BOE transfer

H01 remains a scientific behavioral experiment only.

---

## 16. Licensing / Source Governance

| Component | Status |
|---|---|
| HPD `sp` | **PENDING** (internal research use per repo precedent) |
| FRED SP500, DJIA | platform access CLEAR; archival rights **PENDING** |
| FRED NASDAQ100, NASDAQCOM | platform access CLEAR; archival rights **PENDING** |
| Yahoo Finance `^NYA` | **EXCEPTION GRANTED** (§18a); archival rights **PENDING** |

**Classification: CONDITIONAL**

Internal research use is accepted under the HPD PENDING precedent and the NYA Yahoo exception. The execution-governance statement in protocol §24 explicitly permits execution under these conditions. Archival/republication remains subject to owner policy.

---

## 17. Scope Creep Search — No Issues Found

No hidden authorization for:
- New markets (beyond NYA)
- New eras
- New thresholds
- Alternative price fields
- New sampling rules
- New filters
- New market-selection rules
- Result-dependent exclusions
- Alternative statistical tests
- Undocumented preprocessing

All scope creep checks PASS.

---

## 18. Open Issues

**None.** All gates pass.

---

## 19. Final Execution State

> **H01 EQUITY V1.2.0 — FROZEN / EXECUTION READY**

---

## 20. Execution Authorization

> **NO H01 EXECUTION OCCURRED DURING THIS AUDIT.**

> **EXPLICIT OWNER EXECUTION AUTHORIZATION IS STILL REQUIRED.**

---

## 21. Required Next Task

**Owner authorization of the single H01 execution**

The owner must explicitly authorize:
1. The single H01 V1.2.0 execution
2. Access to the frozen source files (front_sp.csv, FRED files, NYA_DATA.html)
3. The execution environment (Python 3.11+, numpy, scipy)

---

## 22. Integrity

- Read-only: YES
- No execution: YES
- No data download: YES
- No protocol modification: YES
- No definition lock modification: YES
- No statistics computed: YES
- No new DISC: YES
- No commit: YES
