# QUANTFORGE — GIT / GITHUB SECRET & PRIVATE-DATA EXPOSURE AUDIT V1

*Strictly read-only audit. No file modified; no history rewritten; no push; no credential rotation; no provider contact. All credential/account values redacted from this report.*

---

## 1. Executive Verdict

**EXPOSURE FOUND — LOW severity (account-identifier level; no authentication secrets).**

One confirmed piece of private account information exists in the current tree **and in the full reachable Git history, including the pushed history on GitHub**:

- a hardcoded **MT5 broker account login ID** (with broker name and local terminal path) in `broker/mt5_connection.py`, present in **every commit since the initial commit** (`e9b793f`), hence reachable from `origin/main` (`9dc2619`).

No passwords, API keys, tokens, private keys, JWTs, or other authentication secrets were found anywhere in the current tree or in any reachable Git blob.

**The previously pasted Norgate credential was NOT found** in the current tree or in any reachable Git history (see §5).

All other findings are privacy-hygiene issues (tracked tool-state databases) or non-sensitive research/test artifacts.

---

## 2. Repository Identity

| Item | Value |
|---|---|
| Repository path | `C:\Users\User10\Documents\MRV\yuvi\QuantForge` |
| Current branch | `main` |
| HEAD | `8990dfeef635f175ed39d26a3b525193c9af47ae` |
| Remote | `origin → https://github.com/mani659/QuantForge.git` (fetch/push) |
| Local refs | `main` (HEAD), `origin/main` = `9dc2619` (local main is **6 commits ahead**; last push 2026-08-11) |
| Tags | none |
| Total commits (all refs) | 10 (linear history) |
| Tracked-file count | 465 |
| Working-tree state | DIRTY: modified governance docs (README, docs/*, research/knowledge/*) and many untracked new research artifacts (today's ORD/governance work), `data/` fully untracked |

---

## 3. Current-Tree Findings

| Severity | Finding Type | Path | Status | Notes |
|---|---|---|---|---|
| **MEDIUM** | MT5 broker account login ID (9-digit) + broker name (masked) + local terminal path | `broker/mt5_connection.py` (`DEFAULT_TERMINAL_PATH`, `EXPECTED_ACCOUNT`) | TRACKED | Account identifier, not a password. Identifies the operator's live trading account and broker. |
| **LOW** | Same account ID in test fixture | `tests/test_mt5_connection.py` | TRACKED | Test scaffolding; same value as above. |
| **INFO (privacy)** | Freebuff conversation/session database (SQLite, 92 messages, 2026-08-10→08-15, 1 thread) | `.freebuff/desktop-v2.db`, `-wal`, `-shm` | TRACKED | Tool-state DB with conversation content should not be in Git. Scanned: **0** "norgate" hits; "password"/"secret"/"token" hits are a 1Password CLI ad and research-instruction prose — not credentials. |
| **INFO (privacy)** | Visual Studio Copilot index + solution state DBs | `.vs/QuantForge/CopilotIndices/.../CodeChunks.db`, `SemanticSymbols.db`, `.vs/slnx.sqlite` | TRACKED | Code-indexing caches; **0** credential-term rows. Tool-state files should not be in Git. |
| **INFO** | Authorization test scaffolding | `test_outputs/auth_*.json` (10 files) | TRACKED | `operator_identity: admin_user`, `deployment_identity: paper_run`; synthetic, no real credentials. |
| **INFO** | Paper-session simulated balances | `test_outputs/research/experiments/run_*/deployment_outcome.json`, `reports/*.json` | TRACKED | Simulated `account_balance` values only; no account IDs, no credentials. |
| **INFO** | Bootstrap draw caches (binary float arrays) | `output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/.build_cache/*.npy` | UNTRACKED | 31 regex pattern hits were binary false positives; not in Git. |
| **INFO** | Norgate scratch scripts & research docs | `scratch_norgate_*.py`, `output/research_discovery/H01_NORGATE_*.md` | UNTRACKED | Contain local paths and trial-status discussion only; **no credentials**. |

---

## 4. Git-History Findings

| Severity | Finding Type | Commit | Path | Reachability | Status |
|---|---|---|---|---|---|
| **MEDIUM** | MT5 account login ID + broker + terminal path | `e9b793f` (initial) → present in **all 10 commits** | `broker/mt5_connection.py`, `tests/test_mt5_connection.py` | **Reachable from `main` AND from pushed `origin/main` (`9dc2619`)** | CONFIRMED |
| **INFO** | Freebuff conversation DB | `9dc2619` (pushed), `b67a3cc`, `8990dfe` | `.freebuff/desktop-v2.db*` | Reachable from both refs | Credential-term scans: 0 "norgate" in every blob version; benign ad/prose matches only |
| **INFO** | VS Copilot index DBs | pushed `9dc2619` | `.vs/...` | Reachable from both refs | Clean |
| — | Norgate word | `8990dfe` only | `output/research_discovery/H01_HISTORICAL_BROAD_US_DATA_ACQUISITION_V1.md` | Reachable from `main` only (not pushed) | Research artifact; contains no credential |

Full-history greps (`git grep` across all 10 commits): **0** occurrences of any password/API-key/token/private-key assignment; **0** credential-bearing URLs; no `.env`, PEM, JWT, AWS, Slack, or GitHub-token patterns.

---

## 5. Norgate Credential Check

- **Current-tree presence:** NOT PRESENT — no "norgate" in any tracked blob; untracked Norgate artifacts (3 scratch scripts, 4 research docs) contain only local paths and trial-status narrative, no username/password.
- **Git-history presence:** NOT FOUND — "norgate" appears in exactly one blob (`H01_HISTORICAL_BROAD_US_DATA_ACQUISITION_V1.md` @ HEAD), a research artifact with no credential content. All committed `.freebuff` DB/WAL/SHM blobs (both pushed and local) contain 0 "norgate" hits.
- **Reachability:** n/a (not found).
- **Caveat (honest limit):** the tracked Freebuff DB's stored conversation window is 2026-08-10→08-15; the Norgate trial work occurred 2026-08-17, outside that window, and **no commit has been made since 2026-08-16**. The credential was pasted into a conversation that was never committed to Git, and no evidence of it exists in any reachable blob. This cannot be proven absolutely (a deleted-then-garbage-collected blob could in principle exist), but no evidence of exposure was found.
- **Recommended action:** none required for Git; for hygiene, never paste the Norgate credential into chats or repo files, and do not store it in any tracked location. If in doubt, rotate the Norgate password with the provider (not performed here).

---

## 6. Private-Data Findings

| Category | Finding | Classification |
|---|---|---|
| Credentials (passwords/tokens/keys) | **None found** in tree or history | — |
| Account information | MT5 account login ID + broker name (masked) + local terminal path in `broker/mt5_connection.py` (tracked, pushed) | Genuine private account info — MEDIUM |
| Personal data | None (no emails-with-secrets, IPs, SSH hosts, payment data, cookies) | — |
| Raw vendor data | `data/` (tick/M1 extracts) is **untracked**; `*.csv/parquet/pkl/bin/fxt/hst/zip` are gitignored; tracked `reports/*.json` are validation summaries only | No raw vendor data committed |
| Harmless research artifacts | Protocols, adjudications, screening docs, DB hashes, market names | INFO — normal project material |

---

## 7. Latest Commit Review

HEAD `8990dfe` (2026-08-16, "H01 Equity Track A: adjudication and historical broad-US data-source audit") contains:

- H01 Equity adjudication + data-source audit artifacts (intended research content);
- the Freebuff DB version with only benign matches (see §3);
- the MT5 account ID (inherited unchanged from the initial commit);
- **no** credentials, no private account data beyond the MT5 ID, no raw private datasets.

Today's (uncommitted) working tree adds only research/governance artifacts plus untracked `data/`, scratch scripts, and build caches — none credential-bearing.

---

## 8. GitHub Publication Status

**REMOTE PUBLICATION STATUS NOT VERIFIED FROM LOCAL EVIDENCE.**

The remote URL is `https://github.com/mani659/QuantForge.git`; repository visibility (public/private) cannot be established locally without authenticating, which this audit must not do. Independently of visibility: the pushed history (`9dc2619` and ancestors) **contains the MT5 account ID**, so anyone with access to the remote (public viewers, or collaborators on a private repo) can see it.

---

## 9. Risk Assessment

- **Overall: LOW.** No authentication secret (password/token/key) exists anywhere. The single confirmed exposure is a broker **account identifier** (with broker name and local path), which is private account information but cannot by itself authorize access to the account (MT5 connection also requires the terminal-held password and, typically, 2FA/device binding).
- **Secondary risk: privacy hygiene.** Tracked tool-state databases (`.freebuff/*`, `.vs/*`) embed conversation/index content into history; this is the class of file that can silently capture secrets pasted into chats. The current content is clean, but the risk class is real.

---

## 10. Required Remediation (recommendations only — NOT performed)

1. **MT5 account ID:** replace the hardcoded `EXPECTED_ACCOUNT` (and terminal path) with environment/local-config sourcing; remove the ID from `broker/mt5_connection.py` and `tests/test_mt5_connection.py`. If the repository is or may become public, a **separate, authorized** history-rewrite task should scrub the ID from all 10 commits (and force-push only with explicit approval), and the account should be treated as disclosed.
2. **`.gitignore` hardening:** add `.freebuff/`, `.vs/`, `test_outputs/`, `scratch/`, `*.db`, `*.db-wal`, `*.db-shm`, `*.npy`, `data/` to prevent tool-state and build-cache commits.
3. **Remove tool-state DBs from history** (separate authorized task): `.freebuff/desktop-v2.db*`, `.vs/` index DBs.
4. **Norgate credential:** no action required from this audit; do not commit or paste it. Rotation is optional prudence.
5. **Guardrail:** verify `git status` before any future commit so untracked scratch/data/build-cache files are never staged with `git add -A`.

---

## 11. Exact Next Task

> Credential rotation is **not** required (no authentication secret found). The MT5 account ID exposure and the tool-state-DB hygiene issues should be remediated in a separate, explicitly authorized task (code change + `.gitignore` + optional history rewrite). None of this blocks the planned **ORD pre-registration audit** workflow, which involves no publication of the affected files.

---

## 12. Integrity

- Strictly read-only: the only file created is this audit artifact; no existing file was modified.
- No credentials reproduced anywhere in this report; the MT5 account ID, broker details beyond the name, local path details, and any candidate secret values are masked/redacted.
- No Git history rewritten; no push; no provider contact; no credential rotation; no security tooling installed; no GitHub inspection performed.
- Working tree left exactly as found.
