# TASK122 — Portfolio Mutation Record (authorized append-only changes)

**Authority:** TASK122 owner direction authorizing exactly the TASK121
append-only package for ledger row 8 and INV-007 (no unrelated edits, no
promotion, no research execution). Package text verified byte-for-byte
against TASK121 §2 before application (annotation string matched exactly,
including the em-dash and task121 path reference).

## Mutation 1 — research ledger row 8 (STUDY-CAND-025)

- File: `output/prototypes/research_ledger/task62/62_quantforge_complete_research_ledger.csv`
- Before: 61131 B, sha256 `5424e9ed0666e766…` (144 rows × 34 cols, LF).
- Target verified pre-mutation: single CAND-025 row (STUDY-CAND-025,
  XAUUSDm M1, failure_class STATISTICALLY_UNSUPPORTED, dates/costs/N
  UNKNOWN, validation/confirmation none) — matches TASK114-quoted fields.
- Change: trailing column `reopening_notes` added (no annotation column
  existed; schema extension per the authorized package); exact TASK121
  annotation text on row 8 only; empty elsewhere.
- After: 61659 B, sha256 `1fdee0a48b31dc16af4ca97af895d0023be0405c230fc54a30800746a94ca07b`.
- Verified post-mutation by re-parse: row count, all 34 original columns
  per-cell identical, annotation on target row only. (Ledger `grade`
  VERIFIED flag vs evidence grade E distinction preserved untouched.)

## Mutation 2 — inventory INV-007 (CAND-025)

- File: `output/prototypes/portfolio_reconciliation/task66/66_canonical_candidate_inventory.csv`
- Before: 45253 B, sha256 `d424faddc5cb476b…` (184 rows × 14 cols, CRLF,
  line-ending style preserved on write).
- Target verified pre-mutation: single INV-007 row (CAND-025, XAUUSDm M1,
  original_verdict STATISTICALLY_UNSUPPORTED (grade E), research_status
  PRESERVED_CONDITIONAL) — matches quoted fields.
- Change: trailing column `reopening_notes` added; identical annotation
  text on INV-007 only; empty elsewhere.
- After: 45823 B, sha256 `190018bb5c1f366b2806eb6c8f02046bce29af516fa738fdfc6f4a928a925795`.
- Verified post-mutation identically: counts, all 14 original columns
  per-cell identical, single annotated row.

## Scope confirmation

No other row, column value, file, candidate, closure, ledger entry,
strategy artifact, or governing document touched. Historical negative
evidence preserved byte-for-byte (all original cells identical in both
files). If either target had drifted, the mutation would have stopped —
neither had.
