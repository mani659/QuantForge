
## 65. GIT OVERSIZED FILE AUDIT & HISTORY REWRITE (2026-09-07)

**Status:** COMPLETE

**Completed work:**

1. Full audit of all tracked files and reachable Git history blobs against GitHub 100 MB limit.
2. Three push-blocking files identified:
   - `G6_CAND015_FORWARD_002/heartbeat.jsonl` � 168 MB (crash-loop noise, zero research value)
   - `G6_CAND015_FORWARD_002/connection_events.jsonl` � 168 MB (same crash-loop pattern)
   - `ORD_STAGE1_XAGUSD_EXEC_01/.../minute_quotes.csv.gz` � 17 MB (one-time prep data)
3. Root cause: files committed before `.gitignore` covered `.jsonl` and `.csv.gz` extensions. Once tracked, `.gitignore` cannot retroactively untrack.
4. Fix implemented:
   - Added `*.jsonl`, `*.csv.gz`, `output/` to `.gitignore`
   - Untracked all 482 files in `output/` directory via `git rm --cached`
   - Ran `git filter-repo --force --invert-paths` to remove the three oversized files from entire Git history
   - Re-added `origin` remote, pushed successfully
5. Backup branch `backup-before-history-rewrite` and tag created before destructive operation.
6. Audit report produced (`QUANTFORGE_GIT_OVERSIZED_FILE_AUDIT_V1.md`).

**Verification:**

- `git push` � SUCCESS (commit `4fec092` pushed)
- No tracked file exceeds 10 MB post-cleanup
- Historical blob `.freebuff/desktop-v2.db-wal` (5.5 MB) persists in history but is under GitHub limit
- All `output/` files remain on disk (untracked, not deleted)

**Governed states confirmed:**

- RF-001: RUNNER RESTARTED � TWO-MARKET RECORDER v2.0.0 ACTIVE � DATA ACCRUAL IN PROGRESS
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Next authorized task:** RF-001 V38A Stage 3 Economic Validation (requires =1 eligible post-freeze MATCHED observation).

---

## 66. GITIGNORE CANONICAL ARTIFACT RESTORATION (2026-09-07)

**Status:** COMPLETE

**Completed work:**

1. Post-cleanup audit (§65) identified FAIL: blanket `output/` gitignore rule excluded 382 canonical `.md`, `.json`, `.py`, `.txt` governance documents from Git tracking.
2. Root cause: `output/` added to `.gitignore` to prevent `heartbeat.jsonl` (168MB) from being re-tracked was too broad.
3. `.gitignore` corrected: replaced `output/` with 22 specific runtime/session directory ignore rules.
4. All 382 canonical artifacts verified and staged for commit.
5. Pre-commit verification: PASS (no runtime data, no `.csv`/`.npy`/`.jsonl`/`.parquet` staged, largest file 2.88MB).
6. Committed as `ea05034`, pushed successfully.
7. Restoration report produced (`QUANTFORGE_GITIGNORE_CANONICAL_ARTIFACT_RESTORATION_V1.md`).

**Verification:**

- `git push` — SUCCESS (commit `ea05034` pushed)
- Remote tracking: `main` ahead of `origin/main` by 0 commits
- 383 files tracked under `output/` (352 `.md`, 18 `.json`, 10 `.py`, 2 `.txt`)
- No runtime data, heartbeats, connection logs, or generated JSONL tracked
- Fresh clone will now include complete governance trail

**Governed states confirmed:**

- RF-001: RUNNER RESTARTED → TWO-MARKET RECORDER v2.0.0 ACTIVE → DATA ACCRUAL IN PROGRESS
- RF-002: DEFERRED
- RF-003: DEFERRED
- FB-001: UNCHANGED
- F-01: UNCHANGED
- Base Registry: EMPTY

**Next authorized task:** RF-001 V38A Stage 3 Economic Validation (requires ≥1 eligible post-freeze MATCHED observation).
