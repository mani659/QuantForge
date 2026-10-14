# GATE_REPORT_1C — PROTO-TREND-001 Phase-1C (PHASE_2_GO: NO)

## 1. Precondition: PASS

Part A sha256 `4b44615dcf1646bd…` (full match); `evaluate_v2.py`,
`test_evaluate_v2.py`, `universe.json` matched CODE_FREEZE_v2 before any
change. Flag note: OWNER_APPROVES_REMOVAL_SI arrived as "Yes", read as the
affirmative (case-insensitive).

## 2. C1 code scan: no v3 needed on these grounds

- No hardcoded universe size: no `15`/`N=15`/`len==15` literal anywhere
  (sole "15" nearby is the "IA-15" item label in a docstring).
- No SI=F requirement: `SI=F` occurs only in the CLASS_OF map (line 56)
  and SWAP map (line 67) — passive lookup tables, never required keys.
- Table indexing (all iterate listed symbols only): costs
  `evaluate_v2.py:514` + `:594` (`COST_BY_CLASS[CLASS_OF[s]]`; KeyError only
  for symbols NOT in CLASS_OF, guarded `:510-512`/`:590-592`); SWAP `:347`
  iterates evaluated rows' weights; exposure loop `:464-465` iterates
  evaluated symbols; `ex_bitcoin` filter `:631` is BTC-specific. Absent SI=F
  is never looked up and cannot raise. Reads: `:109-110` (loader),
  `:508-509` (main), `:588-589` (run_full) take all of `uni["series"]`
  with no status filter. Conclusion: deleting the SI=F entry takes effect
  with zero code change.

## 3. C2 scratch test (temp folder, synthetic real-format CSVs): PASS

Run1 (15 series) and run2 (same minus SI=F) both rc=0. N(m) lower by exactly
1 in every month (SI=F active throughout). Zero `SI=F` references in run2
results.json/monthly_series.csv/REPORT.md. Closure label recomputed via
`decide_closure` matches in both runs. Determinism: repeated run2 →
byte-identical results.json.

## 4. C3 removal applied (flag YES)

`universe.json` → `universe_phase1.json` (byte copy, hash verified
`60a55578…`, read-only). Edited copy: SI=F entry deleted from `series`,
top-level `removed_log` added verbatim (rule A11 via X1; the 4 FAIL dates;
vendor_substitution none); nothing else changed (verified: 14 series in
original order, all other keys byte-identical). Loader code path returns 14
symbols, SI=F absent (no data loading performed for the check). New sha256
`0f1cb786…5bf2ab`.

## 5. C4 freeze: CODE_FREEZE_v2_ADDENDUM.md (old/new hashes, reason + date
2026-10-08, owner Salman flag 2026-10-08, evaluator/test files unchanged,
Phase-2 verification list). universe.json, universe_phase1.json and the
addendum are read-only.

PHASE_2_GO: NO — run ends here. No evaluation performed.
