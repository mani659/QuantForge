# ERRATA_1B — Phase-1 record corrections (no frozen file edited)

1. **Annex header wording ("EXECUTE APPROVED REOPENING") contradicts B4
   (DISC-022 is not reopened).** The IMPLEMENTATION_ANNEX.md title carried
   over a stale "REOPENING" header from a template. B4 (owner-signed
   ACCEPT) governs: DISC-022 is not reopened; a PASS changes no closed
   line. The header wording is superseded by B4 and must be read as
   "approved bounded evaluation" scope. Frozen files stay byte-identical;
   this erratum is the correction vehicle.
2. **The in-loop look-ahead check is tautological and test (b) is the real
   protection.** v1's `check_no_lookahead` call inside `evaluate_panel`
   always passes (inputs are sliced to dates ≤ s by construction). The
   genuine protection is the direct unit test: recomputation from truncated
   inputs plus the planted-leak case asserting the check FAILS (kept green
   in both suites). v2 documents this in-code and does not re-add the call.
3. **v1 test (f) covered a function main() did not call.** `load_market_csv`
   (strict single-file refusal) was tested, but v1's main() stub never
   loaded anything. In v2, `load_universe` is the loading path used by
   main(); `load_market_csv` is retained unchanged for tested compatibility,
   and truncation/assertion behavior is covered by dedicated v2 tests.
