# CODE_FREEZE_v2 ADDENDUM — SI=F removal (Phase-1C)

- Old `universe.json` sha256: `60a55578623ff31906b7f40fc11b68287972bbaa59bf99fd2d7680fb30583005` (15 series; preserved byte-identical as `universe_phase1.json`, read-only).
- New `universe.json` sha256: `0f1cb786899c414d2957d93bac51130e04c0d8995e28b08c0398cbe57c5bf2ab` (14 series).
- Removal reason: X1 cross-check FAIL on 4 silver dates (2025-12-30 ratio 0.43; 2026-01-26 ratio 0.43; 2026-01-27 sign flip; 2026-02-05 ratio 1.74) → A11 removal rule; no vendor substitution. Date: 2026-10-08.
- Owner approval: owner Salman approved SI=F removal (flag OWNER_APPROVES_REMOVAL_SI: Yes, dated 2026-10-08). Flag spelling "Yes" read case-insensitively as the affirmative; noted here.
- `evaluate_v2.py` and `test_evaluate_v2.py` are UNCHANGED (hashes below match CODE_FREEZE_v2.md); the loader returns 14 symbols for the new file via its frozen code path (verified, no data loading).

## Phase 2 verification list

- `evaluate_v2.py` sha256 `c7bb98faa235bb882a9ff5b7b14166eb588b393e17b51717ed517ec280526ad8`
- `test_evaluate_v2.py` sha256 `ef10212f73af072d1d975012c7e30132be3eb7e4e588ff5d92334f4c6867c654`
- `universe.json` (new) sha256 `0f1cb786899c414d2957d93bac51130e04c0d8995e28b08c0398cbe57c5bf2ab`
- This addendum sha256 (see GATE_REPORT_1C.md sizes table)
- Part A sha256 `4b44615dcf1646bd752dbaf6604f3c3a8c513840d2686228ec818eecddcbf35f` (first16 `4b44615dcf1646bd`)
