# QUANTFORGE PROJECT CLEANUP AUDIT V1

## 1. Cleanup Objective

Reduce unnecessary clutter while preserving maximum research provenance.
Remove obsolete engineering, scratch files, stale logs, empty directories,
and __pycache__ caches. Preserve all authoritative research, active forward
observation, governance, and reproducibility evidence.

## 2. Repository Inventory

- **Repository root:** C:\Users\User10\Documents\MRV\yuvi\QuantForge
- **Source size (excl .git/.venv/.vs):** 41.88 GB (bulk: data/ ~40.4 GB)
- **Source code size (excl data/):** ~2.5 GB (mostly output/ ~2.4 GB)
- **Git directory:** 33.55 MB
- **Total tracked files:** ~3,327

## 3. Authoritative Files (PRESERVE)

### Core Documentation (docs/)
- SESSION_HANDOFF.md, ARCHITECTURE.md, CONSTITUTION_v1.0.md, CONTEXT.md,
  CHANGELOG.md, CORE_FREEZE.md, INTERFACES.md, TRACEABILITY.md,
  CODING_STANDARD.md, CONSTITUTIONAL_AMENDMENT_AMEND-1.md
- RESEARCH_ENGINE_DESIGN.md, RESEARCH_FACTORY_PIPELINE.md,
  RESEARCH_INDEX.md, STRATEGY_RESEARCH_PROTOCOL.md,
  EXPERIMENT_ORCHESTRATION_V1_ADR.md, ROADMAP.md
- PHASE7_FREEZE_APPROVED.md, PHASE8_PERMANENT_FREEZE.md,
  SPRINT9_1_PERMANENT_FREEZE.md, MISSION_FREEZE.md
- docs/Research_Journal/ (3 .docx files)

### Research Knowledge
- research/knowledge/RESEARCH_DISCOVERY_DATABASE.md
- research/knowledge/RESEARCH_GAPS.md
- research/knowledge/RESEARCH_TIMELINE.md

### Research Infrastructure
- research/analytics/ (7 files)
- research/engine/ (7 files)
- research/lifecycle/ (10 files)
- research/orchestration/ (5 files)
- research/packaging/ (4 files)
- research/dataset/ (7 files)
- research/staged_execution/ (10 files)
- research/g6_forward/ (15 files - includes CAND-015 engine)

### Output Research Artifacts (ALL PRESERVED)
- output/research_discovery/ (271 entries) - ALL historical research
- output/event_study_v1/, v2/, v3/
- output/tsmom_v1/, v2/
- output/xagusd_cost_viability_v1/

## 4. Active Runtime (PRESERVE)

### Forward System
- run_quantforge_forward.bat (A)
- status_quantforge_forward.bat (A)
- stop_quantforge_forward.bat (A)
- scripts/forward/quantforge_forward_supervisor.py (A)
- scripts/forward/status.py (A)
- scripts/forward/supervisor_health.py (A)
- scripts/forward/market_data.py (B)
- scripts/forward/module_registry.py (B)
- scripts/forward/cand015_adapter.py (B)
- scripts/forward/tests/ (2 test files)

### Rare Events
- scripts/rare_events/cand_024_engine.py (B)
- scripts/rare_events/cand_035_engine.py (B)
- scripts/rare_events/contracts.py (B)
- scripts/rare_events/event_ledger.py (B)
- scripts/rare_events/outcome_ledger.py (B)
- scripts/rare_events/health.py (B)
- scripts/rare_events/paper_execution.py (B)
- scripts/rare_events/mt5_market_feed.py (B)
- scripts/rare_events/tests/test_rare_events.py (B)

### Runtime State
- runtime/forward/supervisor/ (status.json, health, lock)
- runtime/forward/cand_024/ (status, ledgers)
- runtime/forward/cand_035/ (status, ledgers)
- runtime/forward/history/ (migration records)

## 5. Superseded Infrastructure (CATEGORY D - ARCHIVE/REMOVE)

| File | Reason |
|------|--------|
| `run_cand015_forward.bat` | Superseded by unified runner |
| `install_quantforge_forward_task.bat` | Task Scheduler no longer required |
| `scripts/rare_events/rare_event_runner.py` | Superseded by unified supervisor |
| `research/g6_forward/run_long_observation.py` | Superseded by adapter integration |

## 6. Task Scheduler Engineering

- **Task name:** QuantForgeForwardSupervisor
- **Status:** Ready (not running)
- **Last Run:** 11/30/1999 (never ran successfully or very old)
- **Enabled:** Yes
- **Action:** Remove from Windows Task Scheduler
- **Risk:** LOW - supervisor is manually started, task never ran

## 7. Scratch/Temporary Files (SAFE TO REMOVE)

### Root-level scratch .py
| File | Size | Reason |
|------|------|--------|
| `append_errors.py` | ~400 bytes | One-off code patcher |
| `debug_test_c.py` | ~2 KB | One-off debug script |
| `fix_terminology.py` | ~800 bytes | One-off text fixer |
| `main.py.py` | 0 bytes | Empty, double extension |

### Root-level .txt
| File | Size | Reason |
|------|------|--------|
| `phase78_content.txt` | ~45 KB | Old phase content dump |
| `phase9_content.txt` | ~32 KB | Old phase content dump |
| `Structure.txt` | ~466 bytes | Old structural notes |

### Diagnostic scripts
| File | Reason |
|------|--------|
| `scripts/rare_events/alias_diagnostic.py` | One-off MT5 diagnostic |
| `scripts/rare_events/diagnostic.py` | One-off MT5 diagnostic |

### Stale logs
| File | Size | Reason |
|------|------|--------|
| `scripts/rare_events/forward_runner.log` | 244 bytes | Stale log |
| `scripts/rare_events/runner_output.log` | 0 bytes | Empty stale log |

### research/scratch/ (11 files)
All one-off G1-G5 screen experiment scripts. No reproducibility value.

### Empty directories
- `logs/`
- `research/cache/`
- `research/matrix/`
- `research/experiments/`

### __pycache__ (50 dirs, ~4 MB)
All project __pycache__ directories. Git-ignored, safe to remove.

### .pytest_cache
Test cache directories. Safe to remove.

## 8. Historical Research (PRESERVE)

ALL historical research artifacts are preserved:
- V1-V23 screening iterations
- G0/G1/G2/G3 closure records
- H01 equity volatility experiments
- ORD economic translation experiments
- XAUUSD liquidity sweep experiments
- Session range expansion experiments
- CAND-015 forward run sessions (001-004)
- All QUANTFORGE_*.md governance records
- All RESEARCH_FACTORY_*.md records
- All TRADEABLE_EDGE_*.md records

## 9. Duplicate/Redundant Files

No exact duplicates found in output/research_discovery/.
All versioned files (V1-V23) represent iterative research progression.

## 10. Runtime Files

- runtime/forward/history/ contains migration checkpoints and pre-canonical
  records. These are D (superseded but reproducibility-value). PRESERVE.
- runtime/forward/supervisor/, cand_024/, cand_035/ are ACTIVE. PRESERVE.

## 11. Data Files

- data/tick/ (5 CSV files, ~40 GB) - Active research datasets. PRESERVE.
- data/m1/ (5 CSV files) - Active research datasets. PRESERVE.
- data/fred/ (4 CSV files) - Active research datasets. PRESERVE.
- data/PER_MARKET_VALIDATION.csv - Active. PRESERVE.
- data/Time Series Momentum Original Paper Data.xlsx - Historical. PRESERVE.

## 12. Dead Code

| File | Status |
|------|--------|
| `scripts/rare_events/rare_event_runner.py` | Superseded by unified supervisor |
| `research/g6_forward/run_long_observation.py` | Superseded by adapter |
| `install_quantforge_forward_task.bat` | Task Scheduler abandoned |
| `run_cand015_forward.bat` | Superseded by unified runner |

## 13. Safe-to-Remove List

1. `append_errors.py` (root)
2. `debug_test_c.py` (root)
3. `fix_terminology.py` (root)
4. `main.py.py` (root)
5. `phase78_content.txt` (root)
6. `phase9_content.txt` (root)
7. `Structure.txt` (root)
8. `scripts/rare_events/alias_diagnostic.py`
9. `scripts/rare_events/diagnostic.py`
10. `scripts/rare_events/forward_runner.log`
11. `scripts/rare_events/runner_output.log`
12. `research/scratch/` (entire directory, 11 files)
13. `logs/` (empty directory)
14. `research/cache/` (empty directory)
15. `research/matrix/` (empty directory)
16. `research/experiments/` (empty directory)
17. All `__pycache__/` directories (50 dirs)
18. All `.pytest_cache/` directories
19. `run_cand015_forward.bat` (superseded launcher)
20. `install_quantforge_forward_task.bat` (obsolete Task Scheduler)
21. `scripts/rare_events/rare_event_runner.py` (superseded runner)
22. `research/g6_forward/run_long_observation.py` (superseded runner)

## 14. Archive List

No archiving needed. All historical research remains in output/research_discovery/.
Superseded files are simple enough to delete (not archive).

## 15. Preserve List

- All docs/ documentation
- All research/ infrastructure
- All output/ research artifacts
- All runtime/ active state
- All data/ datasets
- All scripts/forward/ active code
- All scripts/rare_events/ active engines
- All config/ files
- All boe/ core engine code
- All tests/ test suite
- All assembly/, broker/, converter/, dna/, execution/, ledger/,
  operational_governance/, strategy/, tools/, validator/ code

## 16. Disk-Space Opportunities

| Category | Size | Action |
|----------|------|--------|
| scratch/ | ~23 MB | Already gitignored, not tracked |
| __pycache__ (50 dirs) | ~4 MB | Remove |
| Root .txt files | ~78 KB | Remove |
| Root .py scratch | ~3 KB | Remove |
| Stale logs | ~244 bytes | Remove |
| research/scratch/ | ~50 KB | Remove |
| **Total removable (tracked)** | **~5 MB** | Small but reduces clutter |

Note: The 40 GB data/ directory is gitignored and not tracked.
The 23 MB scratch/ directory is gitignored and not tracked.
Primary value is clutter reduction, not disk space.

## 17. Risks

| Risk | Mitigation |
|------|------------|
| Deleting active runtime files | NONE - no active files in remove list |
| Deleting research artifacts | NONE - all research preserved |
| Breaking forward supervisor | NONE - supervisor not restarted |
| Losing reproducibility | LOW - removed files are one-off scratch |
| Task Scheduler removal | LOW - task never ran, supervisor is manual |
| Contract identity change | NONE - contracts not touched |

## 18. Cleanup Execution Plan

1. Remove root-level scratch .py and .txt files
2. Remove diagnostic scripts
3. Remove stale logs
4. Remove research/scratch/ directory
5. Remove empty directories
6. Remove __pycache__ directories
7. Remove .pytest_cache directories
8. Remove superseded launchers (run_cand015_forward.bat, install_quantforge_forward_task.bat)
9. Remove superseded runner (rare_event_runner.py, run_long_observation.py)
10. Remove Task Scheduler task
11. Verify forward system still works
12. Run tests
13. Git commit
14. Update governance
