# QUANTFORGE — GIT/GITHUB PRIVATE-DATA REMEDIATION PLAN V1

*Read-only planning artifact. NO history rewrite, NO force-push, NO commit, NO push, NO file deletion, NO credential rotation performed. All sensitive values masked as `<REDACTED_MT5_ACCOUNT_ID>`.*

---

## 1. Confirmed Findings

Reproduced from `GIT_GITHUB_SECRET_EXPOSURE_AUDIT_V1.md` and re-verified during this precheck:

| # | Finding | Severity | Location | Reachability |
|---|---|---|---|---|
| F1 | MT5 account login ID (9-digit, masked) + broker name (masked) + local terminal path | MEDIUM (account identifier; not an auth secret) | `broker/mt5_connection.py` (`DEFAULT_TERMINAL_PATH`, `EXPECTED_ACCOUNT`) | Current tree + **all 10 commits, incl. pushed `origin/main` (`9dc2619`)** |
| F2 | Same account ID in test fixtures/assertions | LOW | `tests/test_mt5_connection.py` | Current tree + all 10 commits |
| F3 | Freebuff conversation/session DB tracked | INFO (privacy) | `.freebuff/desktop-v2.db`, `-db-shm`, `-db-wal` | Pushed (`9dc2619`) + local (`b67a3cc`, `8990dfe`); scanned credential-clean |
| F4 | Visual Studio / Copilot state DBs tracked | INFO (privacy) | `.vs/` (7 files: `slnx.sqlite`, `CodeChunks.db`, `SemanticSymbols.db`, `.vsidx`, `.wsuo`, `DocumentLayout.json`, `VSWorkspaceState.json`) | Pushed + local; scanned credential-clean |
| F5 | Generated test outputs tracked | INFO (hygiene) | `test_outputs/` (110 files) | Pushed + local |
| F6 | Scratch tooling tracked | INFO (hygiene) | `scratch/audit.py` (1 file) | Pushed + local |

**Confirmed clean:** no passwords, API keys, tokens, private keys, JWTs, or the Norgate credential anywhere. `data/` (raw vendor data) is untracked and gitignored. `boe/execution/mt5_transport.py` contains no account ID, no broker path, and no credentials (terminal path comes from a config object).

---

## 2. Files Requiring Source Remediation

### 2.1 `broker/mt5_connection.py`

Current hardcoded values:

- `DEFAULT_TERMINAL_PATH = Path(r"<REDACTED_LOCAL_TERMINAL_PATH>")` (broker-local path, redacted)
- `EXPECTED_ACCOUNT = <REDACTED_MT5_ACCOUNT_ID>` (redacted)

**Planned change (not yet applied):** source both from environment variables with **no real-value defaults**:

- `QF_MT5_TERMINAL_PATH` → `terminal_path` (default `None`)
- `QF_MT5_EXPECTED_ACCOUNT` → `expected_account` (default `None`)

Behavior contract preserved:

- `MT5Connection(terminal_path=None, expected_account=None, ...)` still accepts explicit constructor arguments (backward-compatible for any caller passing values).
- At `connect()` time: if `terminal_path` is `None`, raise `MT5ConnectionError` with a clear "set QF_MT5_TERMINAL_PATH" message (the tool `tools/check_mt5_connection.py` currently relies on the default; it will require the env var — acceptable and documented).
- If `expected_account` is `None`, skip the login-mismatch verification (documented; verification is opt-in via env var).
- No real account ID, broker name, or personal path remains in source.

The codebase has **no existing env/config-loading mechanism** (verified: no `os.environ`/`getenv`/dotenv in non-test code); this introduces the minimal standard-library `os.getenv` pattern — no new dependency.

### 2.2 `tests/test_mt5_connection.py`

- Replace `FakeMT5.__init__(account: int = <REDACTED_MT5_ACCOUNT_ID>)` default with a **synthetic** fixture ID (e.g., `10000001`).
- Replace `assertEqual(status.account, <REDACTED_MT5_ACCOUNT_ID>)` and the `ConnectionStatus(account=<REDACTED_MT5_ACCOUNT_ID>, ...)` construction with the synthetic ID.
- Keep the mismatch test as-is (it already uses a different fake ID).

### 2.3 Confirmed scope boundary

`git grep` across HEAD confirms the account ID and the broker name appear **only** in these two files — no other tracked source, docs, or config contains them.

---

## 3. Gitignore Remediation

Add to `.gitignore` (no file changed yet):

```text
# Tool / IDE state (privacy)
.freebuff/
.vs/

# Databases & binary caches
*.db
*.db-wal
*.db-shm
*.npy

# Generated research outputs
test_outputs/
.build_cache/

# Raw / large vendor data
data/

# Scratch tooling (keep tracked exception for scratch/audit.py)
scratch/*
!scratch/audit.py
```

Precedence note:

- `scratch/` becomes ignored **except** `scratch/audit.py` (currently the only tracked file under `scratch/`; it is a legitimate script that should remain tracked — verified it is code, not tool-state).
- `*.db` etc. are safe to ignore globally: the audit's tracked-file extension histogram shows the only tracked `*.db`/`*.sqlite`/`*.db-wal`/`*.db-shm` files are the `.freebuff` and `.vs` tool-state files scheduled for untracking; no legitimate tracked database exists.
- Do **not** add patterns like `output/` or `*.json`/`*.md` — they would hide legitimate research artifacts.

---

## 4. Tool-State Files to Untrack

`git rm --cached` (index-only; files stay on disk) for:

- `.freebuff/desktop-v2.db`, `.freebuff/desktop-v2.db-shm`, `.freebuff/desktop-v2.db-wal`
- all 7 tracked `.vs/` files
- all 110 tracked `test_outputs/` files (all verified generated outputs: `auth_*.json`, `research/experiments/*/deployment_outcome.json`, `manifest.json` — none are input fixtures)
- `scratch/` remains tracked only for `scratch/audit.py` (per §3 exception)

Resulting tracked count: 465 → ≈345 files. No source code, research artifact, or governance record is untracked.

---

## 5. History Exposure

- **MT5 account ID:** present in all 10 commits — `e9b793f`, `330889a`, `613e6e0`, `9dc2619` (**pushed = origin/main**), `30b5e75`, `89f56ba`, `c39d085`, `320b680`, `b67a3cc`, `8990dfe` (HEAD).
- **`.freebuff/` + `.vs/`:** present in pushed `9dc2619` and local `b67a3cc`/`8990dfe` (`.vs` additionally since `e9b793f`).
- **Divergence:** `origin/main...main` = 0 ahead / **6 behind** — local main is 6 commits ahead of the last push; nothing exists on the remote that is not local.
- **Today's ORD/governance work is entirely untracked** (verified: `TRADEABLE_EDGE_DISCOVERY_SCREENING_V3.md`, `ORD_OPENING_RANGE_*`, governance edits are working-tree changes only) — a history rewrite would **not** touch or lose it.
- **No tags exist**, and the history is linear (10 commits) — the rewrite surface is small and low-risk for a solo repository.

---

## 6. Option A — Future-Only Cleanup

Apply §2–§4 (source fix + gitignore + untrack) and commit forward. History keeps the account ID and tool-state DBs.

- **Pros:** zero history risk; no force-push; no clone disruption; fastest path back to the ORD audit.
- **Cons:** the account ID and `.freebuff`/`.vs` blobs remain in pushed history. Anyone with remote access (now or if the repo later becomes public) can retrieve the account ID and prior conversation-DB snapshots. This is acceptable **only if** the remote is and will remain private and the account is treated as disclosed.
- **Post-condition if chosen:** treat the MT5 account as disclosed; optionally rotate by opening a new MT5 account/ID with the broker (not performed here).

---

## 7. Option B — Full History Rewrite

Rewrite all 10 commits to (a) purge the MT5 account ID and broker/path from `broker/mt5_connection.py` and `tests/test_mt5_connection.py` blobs, and (b) drop `.freebuff/`, `.vs/`, and `test_outputs/` from every commit.

- **Tooling:** `git filter-repo` (preferred; must be installed separately — not installed here) or `git filter-branch` (available with Git for Windows; slower, no install needed). Alternative minimal variant: `git filter-branch --index-filter` to delete `.freebuff/`/`.vs/`/`test_outputs/`, plus a content filter or `--tree-filter` sed for the account ID.
- **Required actions (NOT performed, require explicit authorization):**
  1. Run the rewrite on a fresh clone/backup of the repo;
  2. verify rewritten history: 0 occurrences of the account ID, 0 `.freebuff`/`.vs`/`test_outputs` paths, research artifacts intact, `git fsck` clean;
  3. `git push --force origin main` (or force-with-lease);
  4. locally re-clone / re-fetch; invalidate old clones;
  5. re-run the full `GIT_GITHUB_SECRET_EXPOSURE_AUDIT_V1` scan on the rewritten repo.
- **Consequences:** all commit hashes change (10 commits); `origin/main` history diverges from any clone made before the rewrite; the Freebuff DB and VS state will be re-created locally by the tools (now gitignored, so they stay out of Git).
- **Suitability:** appropriate here — solo repo, linear 10-commit history, no tags, local main already 6 commits ahead of the remote, and the alternative (Option A) leaves confirmed private account information permanently in pushed history.

---

## 8. Risks

| Risk | Option A | Option B | Mitigation |
|---|---|---|---|
| Account ID remains in pushed history | **Accepted** | Eliminated | Option B preferred if repo is public/may become public |
| History divergence / broken clones | None | Real | Rewrite on backup first; force-push with `--force-with-lease`; re-clone after |
| Losing research content | None | Low | Verify all 465 tracked paths minus the 120 tool-state paths survive; ORD work is untracked and unaffected |
| Tool-state DBs re-created locally | Re-ignored | Re-ignored | `.gitignore` rules from §3 make recurrence impossible |
| Breaking `tools/check_mt5_connection.py` / runtime | Requires env vars after §2 | Same | Document `QF_MT5_TERMINAL_PATH` / `QF_MT5_EXPECTED_ACCOUNT` in the tool docstring and `docs/` |
| Untested behavior change | Low | Low | Run `tests/test_mt5_connection.py` (updated) + `python -m py_compile` after §2 |

---

## 9. Recommended Path

**Option B (full history rewrite), preceded by a remote-visibility check.**

Rationale:

1. A confirmed private account identifier + broker + personal machine path is in **pushed** history — the exact category the audit flagged as needing removal "before we continue committing work."
2. The repository is a solo, linear 10-commit history with no tags and local main 6 commits ahead of `origin/main` — the cheapest possible rewrite profile.
3. The `.freebuff` conversation DB and `.vs` state DBs should not exist in version control under any scenario.

Sequence (each step a separate authorized task):

1. **Check remote visibility** (read-only probe of `github.com/mani659/QuantForge`) to set urgency: public → Option B required; private → Option B still recommended for the account ID.
2. **Apply source remediation (§2)** + update tests; run `tests/test_mt5_connection.py` and a compile check.
3. **Apply gitignore + untrack (§3–§4)**; verify with `git status --short`.
4. **Rewrite history (§7)** on a backup clone; verify purge; force-push only with explicit approval.
5. **Re-run the full secret-exposure audit** on the rewritten repo.
6. Return to the **ORD pre-registration audit** (unaffected; no ORD artifact is touched by any step).

If the user chooses Option A instead: steps 2–3 only, treat the MT5 account as disclosed, and record that decision in this plan's follow-up.

---

## 10. Explicit Authorization Required

The following are **NOT authorized by this plan** and each requires a separate explicit instruction:

- [ ] Running `git filter-repo` / `git filter-branch` (history rewrite)
- [ ] `git push --force` / `--force-with-lease` to `origin`
- [ ] Creating any commit (including the remediation commit itself)
- [ ] `git rm --cached` execution (the untrack step)
- [ ] Editing `broker/mt5_connection.py`, `tests/test_mt5_connection.py`, `.gitignore` (the source-remediation edits)
- [ ] Any credential rotation or provider contact

---

## 11. Integrity

- This task performed **zero** repository mutations: no files edited, no index changes, no commits, no pushes, no history operations, no deletions, no credential rotation.
- The only new artifact is this plan; the audit artifact and all research/governance files are untouched.
- Working tree and refs are exactly as found at task start.
- All private values masked; no account ID, password, token, or personal path reproduced.
