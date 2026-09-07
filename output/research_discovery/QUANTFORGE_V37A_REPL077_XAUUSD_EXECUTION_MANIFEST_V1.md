# QUANTFORGE — V37A EXECUTION MANIFEST

# REGISTRATION: V37A-REPL-077-XAUUSD-M1
# STATUS: FROZEN / NOT EXECUTED
# MANIFEST VERSION: 1.0
# DATE: 2026-09-03

---

## 1. Experiment

| Field | Value |
|---|---|
| Registration | V37A-REPL-077-XAUUSD-M1 |
| Experiment | CAND-077 frozen volatility compression→expansion replication on XAUUSD M1 |
| Status | FROZEN / NOT EXECUTED |
| Normative source | `output/research_discovery/QUANTFORGE_V37A_REPL077_XAUUSD_REGISTRATION_V1.md` (methodologically authoritative; this manifest is the provenance/control document) |
| Owner authorization | PENDING (execution requires explicit owner authorization in the execution task) |

---

## 2. Repository Provenance (at freeze time)

| Field | Value |
|---|---|
| Repository HEAD | `bbb1c267550e7a1b983abcbc74dab5dd9696a3ec` |
| Branch | `main` |
| Registration artifact SHA-256 | `a8cf84fbce18bda56713a59347a8f900ab3e95e38c21b0c0cb3550febac729c6` |
| Historical implementation SHA-256 | `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b` |
| Archival implementation SHA-256 | `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b` |
| XAUUSD M1 data SHA-256 | `54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c` |
| XAUUSD M1 data bytes | 104,298,565 |
| Execution manifest SHA-256 | Recorded externally after final content (see freeze report / commit message); not self-referential |

---

## 3. Frozen Inputs (exact paths and hashes)

| Input | Path | SHA-256 |
|---|---|---|
| Historical implementation (untracked source) | `research/v26_g1_screen.py` | `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b` |
| Immutable archival copy | `research/archive/v26/CAND-077/v26_g1_screen.py` | `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b` |
| Registration artifact | `output/research_discovery/QUANTFORGE_V37A_REPL077_XAUUSD_REGISTRATION_V1.md` | `a8cf84fbce18bda56713a59347a8f900ab3e95e38c21b0c0cb3550febac729c6` |
| XAUUSD M1 source data | `data/m1/XAUUSD_M1.csv` | `54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c` |

The archival copy is byte-for-byte identical to the historical source (same 12,310 bytes; same SHA-256). The historical source remains unmodified and untracked, as historically. The data file is unmodified.

---

## 4. Execution Environment Freeze

| Field | Value |
|---|---|
| Operating environment | Windows-10-10.0.19045-SP0 (local checkout) |
| Python | 3.11.9 |
| pandas | 3.0.2 |
| numpy | 2.4.4 |
| Script/module path (frozen operational definition) | `research/v26_g1_screen.py` (CAND-077 `run_077` + helpers `compute_atr` / `atr_pct` / `load` / `v3_evidence`) |
| Data path | `data/m1/XAUUSD_M1.csv` |
| Timezone convention | +4h UTC shift applied in `load()` (identical to original V26 handling) |
| Branch | `main` |
| Repository HEAD | `bbb1c267550e7a1b983abcbc74dab5dd9696a3ec` |

No new dependencies are introduced. No environment configuration is altered. Execution must re-verify the historical/archival hashes before Phase A.

---

## 5. Frozen Experiment Summary (not redefinition — registration remains normative)

| Field | Frozen value |
|---|---|
| Original instrument | USATECHIDXUSD |
| Replication instrument | XAUUSD |
| Timeframe | M1 |
| Primary window (entries) | 2023-09-01 → 2026-04-10 |
| Outcome horizon | 30 M1 bars (bar-index based) |
| Direction | long-only |
| Treatment | exact V26 CAND-077 implementation |
| Control | exact V26 CAND-077 implementation |
| Friction | 2.0 bps round-trip (constant shift at aggregation, both arms) |
| Primary metric | conditional net mean delta (treatment net mean − control net mean) |
| Secondary metrics | frozen registration list (N T/CF, gross/net means and medians, mean/median delta, WR delta, std, worst/best, exclude-best mean) |
| Tick data | prohibited |
| Volume | unused |
| Secondary full-window check | 2021-04-12 → 2026-04-10 (consistency evidence only) |

---

## 6. Phase-A Entry Conditions

Phase A may begin only when ALL of the following hold:

1. V37A registration artifact exists and its hash matches `a8cf84fbce18bda56713a59347a8f900ab3e95e38c21b0c0cb3550febac729c6`.
2. Historical implementation hash matches `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b`.
3. Archival copy hash matches the historical hash.
4. This execution manifest exists.
5. XAUUSD file identity matches `54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c`.
6. Repository freeze commit (this commit) exists with only the intended V37A artifacts.
7. Owner has explicitly authorized execution in the execution task.

The execution task must independently re-check every hash. This manifest grants no execution authorization.

---

## 7. Phase A / Phase B and Rerun Rules (frozen reference)

- Phase A: load full XAUUSD file, verify frozen schema, compute signal state, identify treatment/control events, report counts, verify data integrity. No returns, no economics.
- Governance checkpoint between phases; no parameter modification permitted.
- Phase B: only after Phase-A authorization; frozen 30-bar outcomes, gross, 2.0 bps, net, frozen metrics.
- Rerun prohibited unless a method-independent, pre-existing implementation defect is proven, documented, independently justified, versioned, and governance-authorized.
- No numeric replication gate exists. Adjudication is holistic under G1 V3 doctrine.

---

*Execution manifest complete. Freeze commit pending per repository convention. Owner authorization PENDING. NOT EXECUTED.*