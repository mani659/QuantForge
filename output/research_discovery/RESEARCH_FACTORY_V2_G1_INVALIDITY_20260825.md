# QuantForge — RESEARCH FACTORY V2
# G1 INVALIDITY REPORT

## 1. Executive Verdict

**INVALID G1 SCREEN — NON-ADJUDICABLE**

The G1 Economic Plausibility Screen executed on 2026-08-25 has been formally invalidated. The reported headroom values are not admissible evidence. No scientific or economic conclusion about the underlying candidate mechanisms can be drawn from this execution.

## 2. Affected G1 Cycle

- **Date:** 2026-08-25
- **G1 Report:** `RESEARCH_FACTORY_V2_G1_SCREEN_20260825.md`
- **Execution Scripts:** `g1_screen.py`, `g1_screen_2.py`
- **Integrity Audit:** `RESEARCH_FACTORY_V2_G1_INTEGRITY_AUDIT_20260825.md`

## 3. Candidates Affected

- **CAND-G0-001** (Cross-Asset Volatility Spillover)
- **CAND-G0-002** (Session-Transition Imbalance Continuation)
- **CAND-G0-003** (Nested Volatility Compression Breakout)
- **CAND-G0-004** (Transient Volume-Impact Reversal)

## 4. Exact Defects

The independent integrity audit identified the following systemic defects in the G1 implementation:

- **MFE Endpoint:** All four candidates calculated "Gross Opportunity" using the Maximum Favorable Excursion (MFE) over the holding period rather than a deterministic executable exit.
- **Pre-Entry Capture:** Breakout candidates (CAND-G0-001, CAND-G0-003) were evaluated by assuming entry at the pre-breakout close price, falsely capturing the breakout threshold distance for free.
- **Invalid Exit:** CAND-G0-002 and CAND-G0-004 utilized non-deterministic perfect-foresight exits (session max, 60-min peak) instead of the frozen horizon targets.
- **R² → Efficiency Ratio Substitution:** CAND-G0-002 silently replaced the registered `linear R-squared > 0.85` parameter with an undocumented `Efficiency Ratio > 0.6` proxy.
- **Undocumented Down-sampling:** CAND-G0-003 employed an undocumented `events[::10]` down-sampling artifact.

## 5. Why Results Are Non-Adjudicable

Because the implementation used Maximum Favorable Excursion (MFE) and pre-entry capture, the reported gross opportunities (e.g., 115.19 bps, 88.16 bps) do not represent executable returns. A valid screen must measure from a realistic entry trigger to a deterministic, rule-based exit. Since the implementation failed to honor the definition-lock and executable-capture requirements, the output is null and void.

## 6. Candidate Disposition

For this screening cycle:

- CAND-G0-001: CLOSED FOR THIS SCREENING CYCLE — G1 INVALID
- CAND-G0-002: CLOSED FOR THIS SCREENING CYCLE — G1 INVALID
- CAND-G0-003: CLOSED FOR THIS SCREENING CYCLE — G1 INVALID
- CAND-G0-004: CLOSED FOR THIS SCREENING CYCLE — G1 INVALID

These mechanisms are NOT scientifically disproven. They simply did not receive a valid G1 assessment. They must not be silently rerun under repaired definitions. Any future candidate exploring these mechanisms must enter as a new candidate through the normal G0 process.

## 7. G1 Contract Changes

To prevent repetition, the Research Factory V2 doctrine has been hardened with the following components:
1. **G1 Executable-Capture Contract:** Requires explicit definition of trigger, executable entry price, post-entry measurement window, deterministic exit, and friction. Explicitly prohibits free breakout capture and MFE substitution.
2. **G1 Definition-Lock Rule:** Requires exact adherence to the G0 candidate definition.
3. **No Undocumented Proxies:** Prohibits replacing registered parameters with proxies.
4. **No Undocumented Downsampling:** Prohibits silent event thinning.
5. **G1 Pre-Run Static Assertion Contract:** Requires static checklist validation before execution.
6. **G1 Output Contract:** Standardizes reporting of all trade parameters.
7. **G1 Validity Check:** Defines PASS, CONDITIONAL, and INVALID outcomes.
8. **New Implementation Audit Checklist:** Enforces pre-execution integrity checks.

## 8. Research-Factory Lesson

- **G1 cannot merely be a cheap screen; it must be a cheap VALID screen.**
- **The purpose of G1 is early economic discrimination, not permission to introduce approximate substitutes for the candidate definition.**
- **Speed is not valuable if the economic object is invalid.**

## 9. Next Authorized Milestone

> G0 CANDIDATE GENERATION

## 10. Integrity

- No G1 rerun was attempted.
- No G2 execution occurred.
- The invalid candidates were not repaired or rescued.
- No source code was modified.
