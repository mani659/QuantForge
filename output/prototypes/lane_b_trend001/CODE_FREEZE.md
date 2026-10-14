# PROTO-TREND-001 Code Freeze (S6)

Self-test: `test_evaluate.py` run 2026-10-08 (repo .venv, synthetic data only) — **41/41 checks PASS** (IA-12a date logic + cutoff; units; IA-12b no-look-ahead incl. planted-leak FAIL; IA-12c planted effect net>0 and bootstrap lower>0; IA-12d null 100 reps false-positive fraction within 10%; IA-12e cost arithmetic incl. hand-computed toy; IA-12f cutoff refusal).

Frozen code (read-only from this point; any change invalidates these hashes):

- `evaluate.py` — 12543 bytes — sha256 `d2dc2eb90dd2cfa43760a1409d7c8416a67a50be21b75f28828d087cecbfcf03`
- `test_evaluate.py` — 9050 bytes — sha256 `6777e88e2b85eaa040a8706e604aa416724dd7c747dfed931ebd4898dfb2671e`
- `universe.json` — 2160 bytes — sha256 `60a55578623ff31906b7f40fc11b68287972bbaa59bf99fd2d7680fb30583005`

Phase 2 must verify these hashes still match before running (S7). PHASE_2_GO: NO — run ends here.
