# QUANTFORGE — POST-CLEANUP GIT TRACKING AND `.gitignore` VERIFICATION AUDIT V1

**Date:** 2026-09-07
**Auditor:** Independent Read-Only Audit
**Scope:** Repository state after Git oversized-file cleanup (commit `081539a`)
**Status:** COMPLETE — FINDINGS REQUIRING ATTENTION

---

## 1. SCOPE

This audit verifies whether the Git cleanup that:
- Removed 3 oversized push-blocking files from Git history
- Added `*.jsonl`, `*.csv.gz`, `output/` to `.gitignore`
- Untracked 482 files
- Pushed successfully at commit `081539a`

has accidentally excluded any canonical QuantForge governance, research, registration, contract, specification, audit, or milestone artifacts from version control.

**Audit type:** READ-ONLY. No modifications made.

---

## 2. CURRENT GIT STATE

| Property | Value |
|----------|-------|
| HEAD | `081539a` |
| Branch | `main` |
| Up to date with origin | YES |
| Total tracked files | 452 |
| Files in `output/` tracked | **0** |
| Files on disk in `output/` | 833 |
| Untracked working-tree files | 8 (runtime/, research scripts, stop output) |

**Git log (last 10):**
```
081539a docs: add §65 Git oversized-file audit to session handoff
4fec092 chore(git): untrack oversized generated files, prevent future growth
c951bd9 feat: RF-001 two-market raw capture extension
afa86cd feat: US500 forward feed extension for RF-001 observation
269dad1 docs: RF-001 V38A Stage 2 structural validation
33cf204 docs: RF-001 V38A Stage 1 registration
f004460 docs: RF-001 owner selection and prospective freeze
d5b47c7 docs: mandatory relational owner decision matrix
6692043 docs: relational final selection comparison
0ab381f docs: relational owner decision packet
```

---

## 3. `.gitignore` ANALYSIS

### Rules affecting research/governance artifacts

| Rule | Line | Scope | Risk |
|------|------|-------|------|
| `*.csv` | 47 | All CSV files anywhere | LOW — data files |
| `*.csv.gz` | 48 | All gzipped CSV | LOW — data files |
| `*.jsonl` | 56 | All JSONL files | **MEDIUM** — `scripts/rare_events/event_ledger.jsonl` and others are tracked (added before rule) |
| `output/` | 76 | **Entire output directory tree** | **CRITICAL** — catches all canonical governance docs in `output/research_discovery/` |
| `data/` | 81 | Entire data directory | LOW — raw market data |
| `*.json` | NOT present | N/A | NOTE: `.json` files are NOT globally ignored |

### Critical finding: `output/` is overly broad

The `output/` rule on line 76 ignores the **entire** `output/` directory tree. This was intended to catch generated runtime data, but it also catches:

- **319 canonical governance `.md` files** in `output/research_discovery/`
- **Registration documents** (RF-001, FB-001, F-01)
- **Validation reports** (Stage 2 structural, Stage 3 economic)
- **Owner selection freeze artifacts**
- **Adjudication records**
- **Research factory screen results**
- **Discovery reports**

These files are NOT generated runtime data. They are **authored governance documents** that happen to be stored in `output/`.

---

## 4. 482-FILE CLASSIFICATION SUMMARY

### Category A: Runtime/Generated Data (APPROPRIATELY IGNORED)

| Type | Count | Examples |
|------|-------|---------|
| Heartbeat logs | ~15 | `G6_CAND015_FORWARD_*/heartbeat.jsonl` |
| Connection event logs | ~10 | `G6_CAND015_FORWARD_*/connection_events.jsonl` |
| Session manifests | ~10 | `G6_CAND015_FORWARD_*/session_manifest.json` |
| Process identity | ~10 | `G6_CAND015_FORWARD_*/process_identity.json` |
| Execution heartbeats | ~15 | `ORD_*/execution_heartbeat.json` |
| Execution journals | ~15 | `ORD_*/execution_journal.json` |
| Execution manifests | ~15 | `ORD_*/execution_manifest.json` |
| Process identity (ORD) | ~15 | `ORD_*/process_identity.json` |
| Statistics (ORD) | ~10 | `ORD_*/statistics.json` |
| Build caches | ~20 | `tsmom_v*/.build_cache/*.json` |
| CSV data files | ~30 | `*.csv` in various dirs |
| NPY binary files | ~5 | `*.npy` |
| Python scripts (generated) | ~10 | `run_*.py`, `g1_screen*.py` |
| TXT output | ~5 | `*.txt` |
| HTML reports | ~3 | `*.html` |
| **Subtotal** | **~190** | |

### Category B: Canonical Governance/Research Artifacts (SHOULD BE TRACKED)

| Type | Count | Examples |
|------|-------|---------|
| RF-001 governance | 5 | `QUANTFORGE_RF001_V38A_REGISTRATION_V1.md`, `QUANTFORGE_RF001_TWO_MARKET_RAW_CAPTURE_V1.md` |
| FB-001 governance | 3 | `QUANTFORGE_FB001_ORB_V38A_REGISTRATION_V1-r1.md`, `QUANTFORGE_FB001_ORB_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` |
| F-01 governance | 3 | `QUANTFORGE_F01_V38A_REGISTRATION_FREEZE_V1.md`, `QUANTFORGE_F01_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` |
| Relational research | 7 | `QUANTFORGE_RELATIONAL_MECHANISM_DISCOVERY_V1.md`, `QUANTFORGE_RELATIONAL_PARAMETER_ADJUDICATION_V1.md` |
| V38/V38A doctrine | 4 | `QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_RATIFICATION_V1.md`, `QUANTFORGE_V38_DOCTRINE_RATIFICATION_V1.md` |
| Base formulation | 5 | `QUANTFORGE_OUTCOME_BLIND_BASE_DECISION_PROCESS_FORMULATION_RATIFICATION_V1.md` |
| Research factory screens | ~50 | `RESEARCH_FACTORY_V2_G1_SCREEN_*.md`, `RESEARCH_FACTORY_V2_G*_CAND*.md` |
| G0/G1 integrity audits | ~15 | `QUANTFORGE_V3*_G0_INTEGRITY_AUDIT_V1.md` |
| G1 economic screens | ~5 | `QUANTFORGE_V3*_G1_ECONOMIC_SCREEN_V1.md` |
| ORD research | ~30 | `ORD_OPENING_RANGE_*.md`, `ORD_ECONOMIC_*.md`, `ORD_V1_1_0_*.md` |
| H01 research | ~20 | `H01_EQUITY_*.md`, `H01_NYA_*.md`, `H01_VOLATILITY_*.md` |
| US500/forward feed | 2 | `QUANTFORGE_US500_FORWARD_FEED_EXTENSION_V1.md` |
| Session reports | 3 | `QUANTFORGE_SESSION_REPORT_20260824.md` |
| Project cleanup | 3 | `QUANTFORGE_PROJECT_CLEANUP_*.md` |
| Architecture/governance | 10 | `QUANTFORGE_CANONICAL_*.md`, `QUANTFORGE_PROGRAM_LEVEL_*.md` |
| XAUUSD research | 7 | `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_*.md` |
| SESSION_RANGE_EXPANSION | 7 | `SESSION_RANGE_EXPANSION_*.md` |
| TRADEABLE_EDGE screenings | 36 | `TRADEABLE_EDGE_DISCOVERY_SCREENING_V*.md` |
| Rare events | 3 | `QUANTFORGE_RARE_EVENT_*.md` |
| Git oversized audit | 1 | `QUANTFORGE_GIT_OVERSIZED_FILE_AUDIT_V1.md` |
| **Subtotal** | **~225** | |

### Category C: Source/Test/Configuration (CORRECTLY TRACKED)

All source code, tests, and configuration files remain tracked:
- `scripts/forward/` — 19 files tracked
- `research/` — 91 files tracked
- `tests/` — 89 files tracked
- `boe/` — 127 files tracked
- `docs/` — 23 files tracked
- `config/` — 3 files tracked

### Category D: Other

| Type | Count | Notes |
|------|-------|-------|
| TSMOM results | 6 | Scientific reports + results JSON — arguably canonical |
| V37A phase reports | 6 | Execution reports — arguably canonical |
| XAGUSD cost viability | 8 | Protocol + reports — arguably canonical |
| Stage0 preflight | 8 | Execution manifests — generated but reproducibility-critical |
| Ord economic translation | 15 | Protocol documents — canonical |
| **Subtotal** | **~43** | |

---

## 5. CRITICAL `output/` CANONICAL ARTIFACT AUDIT

### RF-001 Artifacts

| Artifact | Path | On Disk | Tracked | Ignored | Canonical? |
|----------|------|---------|---------|---------|------------|
| Owner Selection Freeze | `QUANTFORGE_RF001_OWNER_SELECTION_FREEZE_V1.md` | YES | NO | YES | **YES** |
| V38A Registration | `QUANTFORGE_RF001_V38A_REGISTRATION_V1.md` | YES | NO | YES | **YES** |
| Stage 2 Structural Validation | `QUANTFORGE_RF001_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` | YES | NO | YES | **YES** |
| Two-Market Raw Capture | `QUANTFORGE_RF001_TWO_MARKET_RAW_CAPTURE_V1.md` | YES | NO | YES | **YES** |
| US500 Feed Extension | `QUANTFORGE_US500_FORWARD_FEED_EXTENSION_V1.md` | YES | NO | YES | **YES** |

### FB-001 Artifacts

| Artifact | Path | On Disk | Tracked | Ignored | Canonical? |
|----------|------|---------|---------|---------|------------|
| ORB Registration V1-r1 | `QUANTFORGE_FB001_ORB_V38A_REGISTRATION_V1-r1.md` | YES | NO | YES | **YES** |
| Stage 2 Structural | `QUANTFORGE_FB001_ORB_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` | YES | NO | YES | **YES** |
| Live Integration | `QUANTFORGE_FB001_ORB_LIVE_INTEGRATION_V1.md` | YES | NO | YES | **YES** |

### F-01 Artifacts

| Artifact | Path | On Disk | Tracked | Ignored | Canonical? |
|----------|------|---------|---------|---------|------------|
| Registration Freeze | `QUANTFORGE_F01_V38A_REGISTRATION_FREEZE_V1.md` | YES | NO | YES | **YES** |
| Stage 2 Structural | `QUANTFORGE_F01_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` | YES | NO | YES | **YES** |
| Stage 3 Economic | `QUANTFORGE_F01_V38A_STAGE3_ECONOMIC_VALIDATION_V1.md` | YES | NO | YES | **YES** |

### Relational Research Artifacts

| Artifact | Path | On Disk | Tracked | Ignored | Canonical? |
|----------|------|---------|---------|---------|------------|
| Mechanism Discovery | `QUANTFORGE_RELATIONAL_MECHANISM_DISCOVERY_V1.md` | YES | NO | YES | **YES** |
| Outcome-Blind Formulations | `QUANTFORGE_RELATIONAL_OUTCOME_BLIND_FORMULATIONS_V1.md` | YES | NO | YES | **YES** |
| Parameter Adjudication | `QUANTFORGE_RELATIONAL_PARAMETER_ADJUDICATION_V1.md` | YES | NO | YES | **YES** |
| Owner Decision Packet | `QUANTFORGE_RELATIONAL_OWNER_DECISION_PACKET_V1.md` | YES | NO | YES | **YES** |
| Final Selection Comparison | `QUANTFORGE_RELATIONAL_FINAL_SELECTION_COMPARISON_V1.md` | YES | NO | YES | **YES** |
| Mandatory Decision Matrix | `QUANTFORGE_RELATIONAL_MANDATORY_OWNER_DECISION_MATRIX_V1.md` | YES | NO | YES | **YES** |

### V38/V38A Doctrine Artifacts

| Artifact | Path | On Disk | Tracked | Ignored | Canonical? |
|----------|------|---------|---------|---------|------------|
| V38A Base Validation Pathway | `QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_RATIFICATION_V1.md` | YES | NO | YES | **YES** |
| V38 Doctrine Ratification | `QUANTFORGE_V38_DOCTRINE_RATIFICATION_V1.md` | YES | NO | YES | **YES** |
| Base Formulation Ratification | `QUANTFORGE_OUTCOME_BLIND_BASE_DECISION_PROCESS_FORMULATION_RATIFICATION_V1.md` | YES | NO | YES | **YES** |

---

## 6. RF-001-SPECIFIC AUDIT

### What IS tracked (source code and tests):

| File | Status |
|------|--------|
| `scripts/forward/rf001_observation_recorder.py` | TRACKED |
| `scripts/forward/us500_live_smoke_test.py` | TRACKED |
| `research/rf001_v38a_stage2_structural.py` | TRACKED |
| `research/rf001_v38a_stage2_independent.py` | TRACKED |
| `docs/SESSION_HANDOFF.md` (contains RF-001 state) | TRACKED |

### What is NOT tracked (governance documents):

| File | Status |
|------|--------|
| `QUANTFORGE_RF001_OWNER_SELECTION_FREEZE_V1.md` | **UNTRACKED** |
| `QUANTFORGE_RF001_V38A_REGISTRATION_V1.md` | **UNTRACKED** |
| `QUANTFORGE_RF001_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` | **UNTRACKED** |
| `QUANTFORGE_RF001_TWO_MARKET_RAW_CAPTURE_V1.md` | **UNTRACKED** |
| `QUANTFORGE_US500_FORWARD_FEED_EXTENSION_V1.md` | **UNTRACKED** |

### Impact assessment:

**RF-001 source code** is fully preserved and tracked. A researcher can:
- Read the recorder implementation (`rf001_observation_recorder.py`)
- Run the Stage 2 validation scripts
- Read the session handoff for current state

**RF-001 governance** is partially lost from Git:
- The frozen registration document (`QUANTFORGE_RF001_V38A_REGISTRATION_V1.md`) is NOT in Git
- The owner selection freeze rationale is NOT in Git
- The Stage 2 validation report is NOT in Git
- The two-market capture specification is NOT in Git

**No data loss** — all files exist on disk. But a fresh clone would NOT include these governance artifacts.

---

## 7. SOURCE/TEST/CONFIG TRACKING AUDIT

| Directory | Tracked Files | Status |
|-----------|---------------|--------|
| `scripts/forward/` | 19 | ALL TRACKED |
| `research/` | 91 | ALL TRACKED |
| `tests/` | 89 | ALL TRACKED |
| `boe/` | 127 | ALL TRACKED |
| `docs/` | 23 | ALL TRACKED |
| `config/` | 3 | ALL TRACKED |

**No source, test, or configuration files were accidentally untracked.**

The broad `output/` rule did NOT affect:
- `scripts/` (separate directory)
- `research/` (separate directory)
- `tests/` (separate directory)
- `boe/` (separate directory)
- `docs/` (separate directory)

---

## 8. REPRODUCIBILITY ASSESSMENT

**Question:** If the repository were freshly cloned at `081539a`, would a future QuantForge researcher be able to determine what RF-001 is, why it was selected, what was frozen, and how its Stage 3 validation is supposed to operate?

**Answer: PARTIAL — with significant gaps.**

### What a fresh clone WOULD provide:

1. **RF-001 source code** — `scripts/forward/rf001_observation_recorder.py` (the implementation)
2. **RF-001 test scripts** — `research/rf001_v38a_stage2_structural.py`, `research/rf001_v38a_stage2_independent.py`
3. **RF-001 current state** — `docs/SESSION_HANDOFF.md` (§61-§65 describe RF-001 registration, validation, and infrastructure)
4. **RF-001 context** — References in `docs/SESSION_HANDOFF.md` to frozen parameters, decision semantics, and validation stages

### What a fresh clone would NOT provide:

1. **RF-001 frozen registration document** — The exact parameters, SHA256 hash, and freeze rationale
2. **RF-001 owner selection freeze** — Why RF-001 was selected over RF-002/RF-003
3. **RF-001 Stage 2 validation report** — The 14-test, 7-leakage-check, 5-determinism results
4. **RF-001 two-market capture specification** — The synchronization states and missing-data firewall design
5. **RF-001 US500 feed extension report** — How US500m was discovered and wired

**A researcher could reconstruct RF-001 from source code and session handoff, but would lack the formal governance trail that justifies the frozen parameters and validation results.**

---

## 9. HISTORICAL EVIDENCE ASSESSMENT

### What was intentionally removed from Git history:

| File | Size | Classification | Appropriate? |
|------|------|----------------|--------------|
| `G6_CAND015_FORWARD_002/heartbeat.jsonl` | 168 MB | Crash-loop noise | YES |
| `G6_CAND015_FORWARD_002/connection_events.jsonl` | 168 MB | Crash-loop noise | YES |
| `ORD_STAGE1_XAGUSD_EXEC_01/.../minute_quotes.csv.gz` | 17 MB | One-time prep data | YES |

### What was untracked but remains on disk:

| Category | Count | Recoverable? |
|----------|-------|--------------|
| Canonical governance docs | ~225 | YES — exist on disk |
| Generated runtime data | ~190 | YES — exist on disk |
| Research results | ~43 | YES — exist on disk |
| **Total** | ~458 | ALL recoverable |

**No permanent data loss.** All files exist on disk. The issue is that a fresh Git clone would not include the canonical governance documents.

---

## 10. REQUIRED CORRECTIVE ACTIONS

### CRITICAL: `output/` rule needs refinement

The `output/` rule on line 76 of `.gitignore` is too broad. It should be refined to:

```
# Generated research outputs (keep canonical governance docs tracked)
output/**/heartbeat.jsonl
output/**/connection_events.jsonl
output/**/session_manifest.json
output/**/process_identity.json
output/**/execution_heartbeat.json
output/**/execution_journal.json
output/**/execution_manifest.json
output/**/implementation_manifest.json
output/**/statistics.json
output/**/metadata.json
output/**/peak_resource.json
output/**/execution_metadata.json
output/**/cost_model_outputs.json
output/**/.build_cache/
output/**/*.csv
output/**/*.csv.gz
output/**/*.jsonl
output/**/*.npy
output/**/*.db
output/**/*.db-wal
output/**/*.db-shm
output/**/*.log
output/**/*.txt
output/**/*.html
output/**/*.zip
output/**/*.rar
```

**OR** more practically:

```
# Generated research outputs (keep canonical governance docs tracked)
output/**/G6_CAND015_FORWARD_*/
output/**/CAND015_G6_FORWARD_*/
output/**/ORD_*/execution_*
output/**/ORD_*/process_*
output/**/ORD_*/statistics.*
output/**/ORD_*/metadata.*
output/**/ORD_*/peak_*
output/**/ORD_*/cost_model_*
output/**/ORD_*/implementation_*
output/**/ORD_ECONOMIC_*/execution_*
output/**/ORD_ECONOMIC_*/process_*
output/**/ORD_STAGE1_*/PREP_*/
output/**/ORD_STAGE2_*/ORD_ECONOMIC_*/
output/**/stage0_preflight*/
output/**/stage0_preflight_xau*/
output/**/tsmom_v*/.build_cache/
output/**/tsmom_v*/*.csv
output/**/xagusd_cost_viability_v1/*.csv
output/**/xagusd_cost_viability_v1/*.npy
output/**/SESSION_RANGE_EXPANSION/day_level_events.csv
output/**/XAUUSD_LIQUIDITY_SWEEP_REVERSAL/*_event_*.csv
output/**/V37A_REPL077_XAUUSD_PHASEA/phase_a_report.json
output/**/V37A_REPL077_XAUUSD_PHASEA/phase_b_report.json
output/**/V37A_REPL077_XAUUSD_PHASEA/phase_b_event_level*.csv
output/**/*.html
output/**/*.txt
output/**/seed002_output.txt
output/**/run_h01_economic_translation_v1.py
output/**/g1_screen.py
output/**/g1_screen_2.py
output/**/v24_g1_results.json
output/**/v25_g1_results.json
output/**/v26_cand079_results.json
output/**/V26_G1_SUMMARY.html
```

**AND** re-track all canonical governance documents:

```bash
git add -f output/research_discovery/QUANTFORGE_*.md
git add -f output/research_discovery/RESEARCH_FACTORY_*.md
git add -f output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_*.md
git add -f output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY/EXECUTION_REPORT_*.md
git add -f output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY/metadata.json
git add -f output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY/statistics.json
# ... etc for all canonical files
```

### PRIORITY: Re-track RF-001 governance documents immediately

The following files should be force-added to Git:

```bash
git add -f output/research_discovery/QUANTFORGE_RF001_OWNER_SELECTION_FREEZE_V1.md
git add -f output/research_discovery/QUANTFORGE_RF001_V38A_REGISTRATION_V1.md
git add -f output/research_discovery/QUANTFORGE_RF001_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md
git add -f output/research_discovery/QUANTFORGE_RF001_TWO_MARKET_RAW_CAPTURE_V1.md
git add -f output/research_discovery/QUANTFORGE_US500_FORWARD_FEED_EXTENSION_V1.md
```

---

## 11. GOVERNANCE INTEGRITY CHECKS

| Check | Result |
|-------|--------|
| RF-001 definition unchanged | CONFIRMED — source code tracked |
| RF-001 registration unchanged | CONFIRMED — exists on disk (untracked) |
| No candidate reopened | CONFIRMED |
| No research line reopened | CONFIRMED |
| No economic validation performed | CONFIRMED |
| No Stage 2 performed | CONFIRMED |
| No Stage 3 performed | CONFIRMED |
| No optimization | CONFIRMED |
| No forward performance inspected | CONFIRMED |
| No live trading changes | CONFIRMED |
| Runner not restarted/stopped by this task | CONFIRMED |
| No source modifications | CONFIRMED |
| No test modifications | CONFIRMED |
| No Git history modifications | CONFIRMED |
| No additional files untracked by this task | CONFIRMED |

---

## 12. REQUIRED CLASSIFICATION TABLE

| Artifact / Pattern | Current state | Artifact type | Canonical? | Should Git track it? | Risk | Recommendation |
| ------------------ | ------------- | ------------- | ---------- | -------------------- | ---- | -------------- |
| `output/research_discovery/QUANTFORGE_RF001_*.md` | IGNORED | Governance | YES | YES | **CRITICAL** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/QUANTFORGE_FB001_*.md` | IGNORED | Governance | YES | YES | **CRITICAL** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/QUANTFORGE_F01_V38A_*.md` | IGNORED | Governance | YES | YES | **CRITICAL** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/QUANTFORGE_RELATIONAL_*.md` | IGNORED | Governance | YES | YES | **CRITICAL** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/QUANTFORGE_V38*.md` | IGNORED | Governance | YES | YES | **CRITICAL** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/RESEARCH_FACTORY_*.md` | IGNORED | Research record | YES | YES | **HIGH** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/ORD_OPENING_RANGE_*.md` | IGNORED | Research record | YES | YES | **HIGH** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/H01_*.md` | IGNORED | Research record | YES | YES | **MEDIUM** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/QUANTFORGE_V3*_G*.md` | IGNORED | Audit record | YES | YES | **MEDIUM** | NEEDS FUTURE RE-TRACKING |
| `output/research_discovery/G6_CAND015_FORWARD_*/heartbeat.jsonl` | IGNORED | Runtime log | NO | NO | NONE | CORRECTLY IGNORED |
| `output/research_discovery/G6_CAND015_FORWARD_*/connection_events.jsonl` | IGNORED | Runtime log | NO | NO | NONE | CORRECTLY IGNORED |
| `output/research_discovery/G6_CAND015_FORWARD_*/session_manifest.json` | IGNORED | Runtime log | NO | NO | NONE | CORRECTLY IGNORED |
| `output/research_discovery/G6_CAND015_FORWARD_*/process_identity.json` | IGNORED | Runtime log | NO | NO | NONE | CORRECTLY IGNORED |
| `output/tsmom_v1/results_TSMOM_V1.json` | IGNORED | Results | Arguable | MAYBE | LOW | INVESTIGATE FURTHER |
| `output/tsmom_v2/results_TSMOM_V2.json` | IGNORED | Results | Arguable | MAYBE | LOW | INVESTIGATE FURTHER |
| `output/tsmom_v1/SCIENTIFIC_REPORT_TSMOM_V1.md` | IGNORED | Report | YES | YES | **MEDIUM** | NEEDS FUTURE RE-TRACKING |
| `output/tsmom_v2/SCIENTIFIC_REPORT_TSMOM_V2.md` | IGNORED | Report | YES | YES | **MEDIUM** | NEEDS FUTURE RE-TRACKING |
| `output/xagusd_cost_viability_v1/final_cost_viability_report.md` | IGNORED | Report | YES | YES | **MEDIUM** | NEEDS FUTURE RE-TRACKING |
| `scripts/forward/rf001_observation_recorder.py` | TRACKED | Source | YES | YES | NONE | KEEP TRACKED |
| `research/rf001_v38a_stage2_structural.py` | TRACKED | Source | YES | YES | NONE | KEEP TRACKED |
| `docs/SESSION_HANDOFF.md` | TRACKED | Governance | YES | YES | NONE | KEEP TRACKED |
| `runtime/` | UNTRACKED | Runtime data | NO | NO | NONE | CORRECTLY UNTRACKED |
| `data/` | IGNORED | Raw data | NO | NO | NONE | CORRECTLY IGNORED |
| `*.jsonl` (global) | IGNORED | Data format | NO | NO | LOW | CORRECTLY IGNORED |
| `*.csv.gz` (global) | IGNORED | Data format | NO | NO | LOW | CORRECTLY IGNORED |
| `output/` (entire dir) | IGNORED | Mixed | MIXED | **PARTIAL** | **CRITICAL** | NEEDS FUTURE `.gitignore` REFINEMENT |

---

## 13. FINAL VERDICT

**POST-CLEANUP AUDIT FAIL — CANONICAL ARTIFACT(S) ACCIDENTALLY EXCLUDED**

### Summary:

- **Latest HEAD:** `081539a`
- **Current branch:** `main`
- **Canonical governance/research artifacts remain tracked:** **PARTIAL** — Source code and `docs/SESSION_HANDOFF.md` are tracked, but ~225 canonical governance documents in `output/research_discovery/` are now ignored
- **`output/` is too broadly ignored:** **YES** — The `output/` rule catches both generated runtime data AND canonical governance documents
- **Corrective implementation required:** **YES** — The `.gitignore` needs refinement and canonical documents need to be force-added back to Git
- **This audit made NO repository or runtime modifications:** **CONFIRMED**

### Specific findings:

1. **RF-001 governance documents** (5 files) are untracked — registration, owner selection freeze, Stage 2 report, two-market capture spec, US500 feed extension report
2. **FB-001 governance documents** (3 files) are untracked — registration, Stage 2 report, live integration report
3. **F-01 governance documents** (3 files) are untracked — registration freeze, Stage 2 report, Stage 3 report
4. **Relational research documents** (7 files) are untracked — mechanism discovery, formulations, adjudication, decision packets
5. **V38/V38A doctrine documents** (4 files) are untracked — base validation pathway, doctrine ratification, formulation ratification
6. **Research factory screens** (~50 files) are untracked — G1/G2/G3/G4/G5 screens and closures
7. **All 319 `.md` files** in `output/research_discovery/` are untracked

### Impact:

- **No permanent data loss** — all files exist on disk
- **Fresh clone would lack governance trail** — a researcher could reconstruct RF-001 from source code but would lack formal frozen registration, validation reports, and owner selection rationale
- **SESSION_HANDOFF.md provides partial recovery** — it references the governance artifacts but does not contain their full content

### Recommended immediate action:

1. Refine `output/` `.gitignore` rule to exclude only generated runtime data
2. Force-add all canonical governance documents back to Git
3. Commit the corrected tracking state
4. Verify push succeeds

---

*End of audit. Report written to `output/research_discovery/QUANTFORGE_POST_GIT_CLEANUP_TRACKING_AUDIT_V1.md` (note: this report itself is in the ignored `output/` directory and would need to be force-added to be tracked).*
