# QUANTFORGE — GIT/GITHUB PRIVATE-DATA REMEDIATION REPORT V1

*Authorized Option B remediation: full Git history rewrite + force-push. All sensitive values masked; the real MT5 account ID never appears in this report.*

---

## 1. Authorization

Explicit authorization received for **OPTION B — FULL GIT HISTORY REMEDIATION** per the reviewed plan `GIT_GITHUB_PRIVATE_DATA_REMEDIATION_PLAN_V1.md`: remove the confirmed MT5 account identifier / broker-local environment information and tracked IDE/tool-state databases from the complete reachable repository history, then force-push the cleaned `main` to `origin/main`, preserving legitimate source, research, governance, and current ORD work.

---

## 2. Original Repository State

| Item | Value |
|---|---|
| Branch | `main` |
| Original HEAD | `8990dfeef635f175ed39d26a3b525193c9af47ae` |
| Local `origin/main` tracking | `9dc2619b434b9a1dd3381aacef20a3b57d4d7fef` |
| **Actual remote `main` (discovered)** | `5a94978fb912192e32891da3ea70d21f51d6c5de` — "Add README.md…" by `mani659`, pushed 2026-08-11, parent `9dc2619`; present on GitHub but absent locally (the push gate correctly refused the first attempt) |
| Commits (local) | 10 |
| Commits (remote incl. README) | 11 |
| Tracked files | 465 |
| Backup | `git clone --mirror` → `QuantForge_pre_remediation_backup.git` (sibling dir, verified: HEAD `8990dfe`, 10 commits, contains pre-state) + local tag `remediation-backup-pre-v1` @ `8990dfe` (never pushed) |

---

## 3. Source Remediation

- `broker/mt5_connection.py` — refactored to environment configuration:
  - `QF_MT5_TERMINAL_PATH` → terminal path (no default; `MT5ConnectionError` if unset at connect);
  - `QF_MT5_EXPECTED_ACCOUNT` → expected account login (no default; verification skipped when unset);
  - explicit constructor arguments preserved and take precedence; no account ID, broker name, or local path hardcoded.
- `tests/test_mt5_connection.py` — synthetic fixture account `10000001` (clearly non-real); mismatch test passes `expected_account` explicitly; added `test_missing_configuration_is_rejected` and `test_environment_configuration_is_honored`.
- Verified: `python -m py_compile` OK; **6/6 unit tests pass** (`python -m unittest tests.test_mt5_connection -v`).
- Scope check: `boe/execution/mt5_transport.py` untouched (confirmed clean — no account ID, no broker path, no credentials).

---

## 4. Tracked Tool-State Removal

Removed from the rewritten history (all commits) via the rewrite filter:

- `.freebuff/desktop-v2.db`, `-db-shm`, `-db-wal`
- `.vs/` (7 files: `slnx.sqlite`, `CodeChunks.db`, `SemanticSymbols.db`, `.vsidx`, `.wsuo`, `DocumentLayout.json`, `VSWorkspaceState.json`)
- `test_outputs/` (110 generated files)

Files remain on disk (untracked) and are now gitignored. `.gitignore` hardened with: `.freebuff/`, `.vs/`, `*.db`, `*.db-wal`, `*.db-shm`, `*.npy`, `test_outputs/`, `.build_cache/`, `data/`, `scratch/*` with keep-exception for the legitimate tracked `scratch/audit.py`. Tracked count: **465 → 345** (no source or research artifact removed).

---

## 5. History Rewrite

`git filter-branch --tree-filter` on `main` only (origin tracking ref left untouched for the lease):

- removed `.freebuff`, `.vs`, `test_outputs` from every commit;
- replaced the real MT5 account ID in `broker/mt5_connection.py` / `tests/test_mt5_connection.py` with the synthetic `10000001`;
- removed the broker-local terminal path and broker name.

Pre-state protected: `git stash push` → rewrite → `git stash pop`; all 10 pre-existing modified working-tree files (README, docs, governance) restored byte-identical; the Freebuff DB files restored (sizes verified: 9,428,992 / 5,491,992 bytes, matching pre-rewrite). filter-branch backup ref `refs/original/refs/heads/main` deleted; `git reflog expire --expire=now --all`; `git gc --prune=now --aggressive` (695 objects, 1 pack).

**Remote-commit reconciliation:** the remote's extra commit `5a94978` (README, owner-authored) was folded into the rewritten history by cherry-picking onto the clean rewritten base with attribution preserved (`a6c62ed`, author `mani659`), then `refs/heads/main` updated. The rewritten history therefore contains **11 commits** — the full local + remote reachable history, all clean. Temp worktree used for the cherry-pick (main working tree untouched); worktree removed after.

---

## 6. Security Verification Before Push

Verified on the full 11-commit rewritten `main` and the current tree:

- real MT5 account ID: **0 matches** in any rewritten commit and the working tree;
- broker name / local path: **0 matches**;
- password / API-key / private-key patterns: **0 matches**;
- `.freebuff` / `.vs` / `test_outputs` paths in rewritten history: **0**;
- working-tree status: 13 modified tracked files (`.gitignore`, README, docs, governance, the two remediated source files) + untracked research artifacts — all intended, none tool-state;
- Norgate: no occurrences beyond the pre-existing research artifact (no credential content).

---

## 7. ORD Preservation Check

- `ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md` — present, untracked, untouched.
- `ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1.md` — present, untracked, untouched; SHA-256 **`cc01b23c…`** verified before and after (and re-verified: `cc01b23cf213…`).
- `TRADEABLE_EDGE_DISCOVERY_SCREENING_V3.md` — present, untracked, untouched.
- All uncommitted ORD/governance work remained intact throughout (stash/pop + update-ref preserved it).

---

## 8. Force-Push Result

```
+ 5a94978...a6c62ed main -> main (forced update)
```

First attempt was correctly **rejected by `--force-with-lease` (stale info)** because the remote held `5a94978` (unknown locally). After read-only investigation and folding the README commit into the rewritten history, the push succeeded with `--force-with-lease` against the verified remote state `5a94978`. No unconditional `--force` was ever used.

---

## 9. Remote Verification

- `git ls-remote origin refs/heads/main` → `a6c62edf9666f59eb8a044da2d0497f9a366e0a0` = local `main` (**SYNCED**).
- Backup tag `remediation-backup-pre-v1` confirmed **absent from the remote** (0 refs).
- The remote's prior history (`5a94978` and its ancestors, containing the account ID and tool-state DBs) is no longer reachable on GitHub after the forced update.

---

## 10. Final Repository State

| Item | Value |
|---|---|
| Branch / HEAD | `main` @ `a6c62edf9666f59eb8a044da2d0497f9a366e0a0` |
| Remote | `origin` = `https://github.com/mani659/QuantForge.git`, main SYNCED |
| Commits | 11 (all rewritten, messages/order/attribution preserved) |
| Tracked files | 345 |
| Real account ID | absent from tree and all 11 commits |
| Tool-state DBs | absent from history; present on disk, gitignored |
| Working tree | 13 intended modified files + untracked research artifacts (incl. ORD work) — nothing committed by this task |
| Backups | `QuantForge_pre_remediation_backup.git` (mirror) + local tag `remediation-backup-pre-v1` (local only) |

---

## 11. Remaining Risks

1. **Local backup artifacts retain the pre-state:** the mirror clone and the local tag `remediation-backup-pre-v1` still contain the old history (account ID + tool-state DBs). They are local-only and were never pushed; delete them once the remediation is confirmed stable. Until then, treat them as sensitive.
2. **Any other clones/caches** of the old history (other machines, IDE caches, GitHub forks) still hold the old commits; force-push does not purge them. Known scope: none identified locally.
3. **Account disclosure stands:** the account ID was in pushed history for ~6 days (Aug 11–17). If the repository is or was public, consider the account disclosed and optionally rotate it with the broker. Repository visibility was not verified (no authenticated GitHub inspection performed).
4. **Working-tree changes are uncommitted** (remediation + ORD governance work). They should be committed in a deliberate, separate commit after review — this task intentionally committed nothing.

---

## 12. Integrity

- Only the explicitly authorized mutations occurred: two source files refactored, `.gitignore` hardened, history rewritten (11 commits), remote force-pushed with lease after verification.
- No other file modified; no research/governance/dataset content changed; no credentials rotated; no provider contacted; no repository-visibility change.
- No real account ID, password, token, private key, or personal path appears in this report or any tracked file.
- Next task per the mission: **return to the ORD independent pre-registration audit**.
