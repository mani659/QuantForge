# QUANTFORGE — CAND-015 G6 HARNESS
# AUDIT RESOLUTION V1

## 1. Original Findings
The independent read-only audit of the G6 Harness (`output/research_discovery/G6_CAND015_HARNESS_INDEPENDENT_AUDIT_V1.md`) identified the following weaknesses:
- **Test C:** Checked identity dictionary values rather than actual pre-entry D1 state behavior.
- **Test D:** Placeholder test without behavioral verification of the complete M5 boundary.
- **Test F:** Placeholder test without behavioral verification of the deterministic exit horizon.
- **Test H:** Historical Parity test merely instantiated the harness rather than evaluating an actual frozen signal sequence.
- **Test J:** Weak heartbeat output test.

Original Verdict: **B — CONDITIONAL**

## 2. Corrections
No modifications were made to `CAND-G0-015`, its frozen identity, or the harness architecture. Modifications were strictly limited to rewriting the `pytest` suite in `research/g6_forward/tests_g6.py` to assert the required structural and behavioral invariants of the observation harness. 

## 3. Test Improvements
- **Test C (Pre-entry volatility state):** Validates that appending massive future-volatility M1 ticks within the current day does not alter the D1 state, strictly enforcing the `pre_entry` requirement.
- **Test D (Complete M5 boundary):** Verifies that an incomplete M5 bar containing a shock does not trigger a signal until the precise completion boundary of that M5 timeframe is reached.
- **Test F (Deterministic exit):** Verifies that the state machine explicitly ignores intermediate prices and forces exit execution entirely based on the 60-minute deterministic horizon.
- **Test J (Heartbeat):** Dynamically alters the state machine and verifies that standard stdout heartbeat logs accurately reflect the live state.

## 4. Historical Parity
- **Fixture Identity:** Synthetic deterministic sequence containing exactly 1 embedded Nasdaq shock.
- **Reference Identity:** CAND-G0-015 (1.0.0).
- **Result:** SIGNAL PARITY = PASS. 
- **Details:** The event count was correctly measured as exactly 1. Event ordering, lockouts, and timestamps perfectly reproduced the logic without dropping into infinite loops or looking ahead. The harness matched the signal sequence deterministically. 

## 5. Regression Results
Running `pytest research/g6_forward/tests_g6.py -v`:
- Total Tests: 10
- Passed: 10
- Failed: 0
All tests A–J successfully passed.

## 6. Remaining Limitations
The `FORWARD_PAPER` mode remains strictly blocked with a `NotImplementedError` due to the lack of a real-time or demo market data feed. True forward observation cannot occur until this data dependency is met.

## 7. Final Readiness
**A — REPLAY HARNESS VALIDATED**
The replay observation harness successfully passed all invariant and parity checks. However, G6 forward validation remains blocked.
