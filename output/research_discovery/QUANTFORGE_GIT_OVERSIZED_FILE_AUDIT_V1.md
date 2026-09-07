# QUANTFORGE GIT OVERSIZED FILE AUDIT V1

**Date:** 2026-09-07  
**Auditor:** OpenCode  
**Scope:** All tracked files in working tree and reachable blobs in Git history  
**Threshold:** GitHub file size limit = 100 MB  

---

## EXECUTIVE SUMMARY

**Push status:** BLOCKED. Three tracked files exceed GitHub's 100 MB limit.

| File | Size | Status | Classification |
|------|------|--------|----------------|
| `G6_CAND015_FORWARD_002/heartbeat.jsonl` | 168 MB | **PUSH BLOCKER** | Class A |
| `G6_CAND015_FORWARD_002/connection_events.jsonl` | 168 MB | **PUSH BLOCKER** | Class A |
| `ORD_STAGE1_XAGUSD_EXEC_01/.../minute_quotes.csv.gz` | 17 MB | **PUSH BLOCKER** | Class B |

**Root cause:** These files were committed before `.gitignore` covered their extensions (`.jsonl`, `.csv.gz`). Once tracked, `.gitignore` has no effect.

---

## COMPLETE INVENTORY

### A. Files exceeding GitHub 100 MB limit (push blockers)

| # | Path | Size | Introduced by | Content |
|---|------|------|---------------|---------|
| 1 | `output/research_discovery/G6_CAND015_FORWARD_002/heartbeat.jsonl` | 168,397,311 B (160.6 MB) | `f6a4bb4` | Repeated crash-loop logs: START → ERROR → FATAL cycle every ~10ms for 7 hours. Pure diagnostic noise, zero research value. |
| 2 | `output/research_discovery/G6_CAND015_FORWARD_002/connection_events.jsonl` | 168,375,223 B (160.6 MB) | `f6a4bb4` | Same crash-loop pattern as heartbeat. Redundant with heartbeat.jsonl. |
| 3 | `output/research_discovery/ORD_STAGE1_XAGUSD_EXEC_01/PREP_XAGUSD_07BACB1E396BBA517E0F46F461C3CB48B94E5E9ABB2F30D67A025B810A67C736/minute_quotes.csv.gz` | 17,217,243 B (16.4 MB) | `f6a4bb4` | Compressed historical XAGUSD minute quotes used for one-time prep. No ongoing research value. |

### B. Large tracked files under 100 MB (not blocking push, but notable)

| # | Path | Size | Risk |
|---|------|------|------|
| 4 | `output/tsmom_v2/results_TSMOM_V2.json` | 3,023,796 B (2.9 MB) | Low — results artifact, may grow |
| 5 | `output/research_discovery/G6_CAND015_FORWARD_004/heartbeat.jsonl` | 2,849,859 B (2.7 MB) | Low — same crash-loop pattern as #1, smaller volume |
| 6 | `output/tsmom_v1/results_TSMOM_V1.json` | 908,245 B (0.9 MB) | Low — results artifact |
| 7 | `output/research_discovery/CAND015_G6_FORWARD_002/heartbeat.jsonl` | 230,299 B (225 KB) | Low — crash-loop, smaller |
| 8 | `output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/results_H01_V1.2.json` | 143,956 B (141 KB) | Low |
| 9 | `output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/results_H01_V1.json` | 137,586 B (134 KB) | Low |

### C. Historical blobs in Git history (no longer in worktree)

| # | Blob SHA | Size | Notes |
|---|----------|------|-------|
| 10 | `.freebuff/desktop-v2.db-wal` | 5,491,992 B (5.2 MB) | Removed from tracking. `.freebuff/` now in `.gitignore`. Blob persists in history. |

---

## ROOT CAUSE ANALYSIS

The `.gitignore` file covers:
- `*.csv` — matches `.csv` but NOT `.csv.gz`
- `*.zip` — matches `.zip` but NOT `.jsonl`
- `data/` — excludes raw data directory

**Missing patterns:**
- `*.jsonl` — JSONL format logs (heartbeat, connection_events)
- `*.csv.gz` — gzipped CSV (minute_quotes)
- `output/` — entire output directory (research artifacts, results)

The three push-blocker files were committed in `f6a4bb4` ("formally distinguish research artifacts from strategy systems") before these patterns existed. Once a file is tracked, `.gitignore` cannot retroactively untrack it.

---

## CLASSIFICATION

| Class | Definition | Files |
|-------|------------|-------|
| **A** | Must untrack immediately. Exceeds GitHub limit. Zero research value. Pure noise. | #1, #2 (heartbeat.jsonl, connection_events.jsonl) |
| **B** | Must untrack. Exceeds GitHub limit. One-time prep data, no ongoing value. | #3 (minute_quotes.csv.gz) |
| **C** | Should untrack proactively. Under 100 MB now but may grow. No ongoing value. | #5 (G6_CAND015_FORWARD_004/heartbeat.jsonl), #7 (CAND015_G6_FORWARD_002/heartbeat.jsonl) |
| **D** | Monitor. Under 100 MB, legitimate research results. May need size management if they grow. | #4, #6, #8, #9 (TSMOM results, H01 results) |

---

## RECOMMENDED TREATMENT

### Immediate (unblocks push)

1. **Untrack Class A + B files** via `git rm --cached`
2. **Add missing patterns to `.gitignore`:**
   - `*.jsonl`
   - `*.csv.gz`
   - `output/` (entire directory, since all content is generated artifacts)

### Follow-up (prevent recurrence)

3. **Audit `output/` contents** — decide which subdirectories need tracked reports vs. generated data
4. **Consider Git LFS** if any `output/` files genuinely need version control (currently none do)
5. **Leave historical blobs** — rewriting history to remove #10 is not worth the risk

---

## MINIMUM SAFE NEXT IMPLEMENTATION

```
Step 1: Add to .gitignore
  *.jsonl
  *.csv.gz
  output/

Step 2: Untrack oversized files
  git rm --cached output/research_discovery/G6_CAND015_FORWARD_002/heartbeat.jsonl
  git rm --cached output/research_discovery/G6_CAND015_FORWARD_002/connection_events.jsonl
  git rm --cached output/research_discovery/ORD_STAGE1_XAGUSD_EXEC_01/.../minute_quotes.csv.gz
  git rm --cached output/research_discovery/G6_CAND015_FORWARD_004/heartbeat.jsonl
  git rm --cached output/research_discovery/CAND015_G6_FORWARD_002/heartbeat.jsonl

Step 3: Commit the cleanup
  git add .gitignore
  git commit -m "chore(git): untrack oversized generated files, prevent future growth"

Step 4: Verify push succeeds
  git push
```

**Note:** Files remain on disk after `git rm --cached`. No data loss. They are simply no longer tracked by Git.

---

## VERIFICATION

After implementation, run:
- `git push --dry-run` — should show clean push
- `git ls-files | ForEach-Object { ... }` — verify no tracked file exceeds 10 MB
- `git status` — verify untracked files appear as untracked (not staged for deletion)

---

*End of audit.*
