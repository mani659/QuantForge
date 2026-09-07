# QUANTFORGE — Gitignore Canonical Artifact Restoration Report (V1)

Date: 2026-09-07  
Author: opencode  
Status: COMPLETE  

---

## Summary

The prior `output/` gitignore rule was too broad, accidentally excluding ~382 canonical `.md`, `.json`, `.py`, and `.txt` governance documents from Git tracking. No permanent data loss occurred (all files remained on disk), but a fresh clone would have lacked the project's complete governance trail. The `.gitignore` has been corrected with specific directory-level ignore rules, and all canonical artifacts have been restored to Git.

---

## Background

### Prior State
The `.gitignore` contained a blanket `output/` rule that caused `git ls-files --others --ignored --exclude-standard output/` to match all files under `output/`. This excluded 382 canonical governance/research documents from version control.

### Root Cause
When the oversized-file audit (§65) added `output/` to `.gitignore` to prevent `heartbeat.jsonl` (168MB) and `connection_events.jsonl` (168MB) from being re-tracked, the rule was too broad. It caught everything under `output/`, including canonical `.md` governance reports, `.json` experiment metadata, and `.py` driver scripts.

### Impact Assessment
- **Data loss:** None. All 382 files remained on disk throughout.
- **Fresh clone impact:** A clone of the repository would have lacked all governance artifacts under `output/`.
- **Git history impact:** None. The files were never committed after the blanket rule was added, so no history was lost.

---

## What Changed

### `.gitignore` Correction

**Before:**
```gitignore
# Generated research outputs
output/
```

**After:**
```gitignore
# Generated research outputs — runtime/session directories only
# Canonical governance/research artifacts under output/research_discovery/ remain trackable
output/event_study_v1/
output/event_study_v2/
output/event_study_v3/
output/M-ORD-ECO-04-CONV-02/
output/stage0_preflight/
output/stage0_preflight_xau/
output/tsmom_v1/.build_cache/
output/tsmom_v2/.build_cache/
output/xagusd_cost_viability_v1/
output/research_discovery/CAND015_G6_FORWARD_*/
output/research_discovery/G6_CAND015_FORWARD_*/
output/research_discovery/ORD/V1.1.0/EXECUTION_*/
output/research_discovery/ORD_ECONOMIC/V1.1.0/EXECUTION_*/
output/research_discovery/ORD_STAGE1_*/
output/research_discovery/ORD_STAGE2_*/
output/research_discovery/H01_ECONOMIC_TRANSLATION_V1_TEST_*/
output/research_discovery/H01_ECONOMIC_V1_EXEC_*/
output/research_discovery/H01_EQUITY_V1_3_0_EXECUTION/
output/research_discovery/H01_EQUITY_V1_3_EXEC_*/
output/research_discovery/H01_EQ_V1_3_EXEC_*/
output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/.build_cache/
output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/daily_series/
output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/daily_series/
output/research_discovery/H01_EQ_V1_3_EXEC_*/daily_series/
output/research_discovery/V37A_REPL077_XAUUSD_PHASEA/phase_b_event_level_*/
test_outputs/
.build_cache/
```

### Files Restored to Tracking

| Category | Count | Examples |
|----------|-------|---------|
| `.md` governance docs | 352 | RF-001 registration, FB-001 Stage 2, F-01 calendar, V38A doctrine |
| `.json` experiment metadata | 18 | TSMOM results, ORD event study statistics, F-01 calendar |
| `.py` driver scripts | 10 | H01 runners, TSMOM runners, g1_screen scripts |
| `.txt` output | 2 | seed002_output.txt, V37A run log |
| **Total** | **383** | Including `.gitignore` itself |

### Pre-Commit Verification

- **Runtime data check:** PASS — No heartbeat files, connection event logs, or generated JSONL staged.
- **Large file check:** PASS — Largest staged file is `results_TSMOM_V2.json` at 2.88MB (well under GitHub 100MB limit).
- **Canonical classification:** PASS — All 382 restored files are governance documents, experiment metadata, or driver scripts.
- **Global ignore rules:** PASS — No `.csv`, `.npy`, `.jsonl`, `.parquet`, or `.h5` files staged (all blocked by global ignores).

### RF-001 Artifacts Verified
- `QUANTFORGE_RF001_V38A_REGISTRATION_V1.md`
- `QUANTFORGE_RF001_OWNER_SELECTION_FREEZE_V1.md`
- `QUANTFORGE_RF001_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md`
- `QUANTFORGE_RF001_TWO_MARKET_RAW_CAPTURE_V1.md`

### FB-001 Artifacts Verified
- `QUANTFORGE_FB001_ORB_V38A_REGISTRATION_V1-r1.md`
- `QUANTFORGE_FB001_ORB_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md`
- `QUANTFORGE_FB001_ORB_LIVE_INTEGRATION_V1.md`

### F-01 Artifacts Verified
- `QUANTFORGE_F01_V38A_REGISTRATION_FREEZE_V1.md`
- `QUANTFORGE_F01_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md`
- `QUANTFORGE_F01_V38A_STAGE3_ECONOMIC_VALIDATION_V1.md`
- `QUANTFORGE_F01_V38A_CALENDAR_V1.json`

---

## Git History

| Commit | Hash | Description |
|--------|------|-------------|
| 1 | `4fec092` | `chore(git): untrack oversized generated files, prevent future growth` |
| 2 | `081539a` | `docs: add §65 Git oversized-file audit to session handoff` |
| 3 | `ea05034` | `fix: preserve canonical research artifacts while narrowing gitignore` |

Backup branch `backup-before-history-rewrite` preserved at `4fec092`.

---

## Remaining Untracked Files

These are intentionally excluded (runtime/session data, scripts, temporary outputs):

| File | Classification | Exclusion Method |
|------|----------------|------------------|
| `runtime/` | Active runtime state | `.gitignore` |
| `scripts/f01_pre_recovery_state.py` | Diagnostic script | Not governance |
| `scripts/forward/restore_mt5_window.ps1` | Operational utility | Not governance |
| `research/v26_*.py` - `v29_*.py` | Draft exploration scripts | Not governance |
| `stop_quantforge_out.txt` | Temporary output | Not governance |

---

## Appendix: Global Ignore Rules (Still in Effect)

These rules prevent large/binary files from being staged regardless of directory:

```
*.csv
*.npy
*.jsonl
*.parquet
*.h5
*.sqlite
*.db
*.db-shm
```

These rules are independent of the `output/` gitignore rules and remain correct.

---

## Conclusion

**POST-CLEANUP AUDIT FAIL has been RESOLVED.** The `.gitignore` now correctly excludes only runtime/session directories while preserving all canonical governance/research artifacts under `output/`. A fresh clone of the repository will include the complete governance trail.
