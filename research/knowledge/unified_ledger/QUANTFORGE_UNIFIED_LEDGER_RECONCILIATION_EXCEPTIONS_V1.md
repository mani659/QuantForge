# QUANTFORGE — UNIFIED LEDGER RECONCILIATION EXCEPTIONS V1

## Purpose

Document all unresolved discrepancies, ambiguities, and conflicts discovered during construction of the Unified Research History CSV Ledger V1.

---

## Exception 1: CAND-042 Component Status Discrepancy

**Issue:** CAND-042 (Correlated Shock Reversion) is classified as COMPONENT-CANDIDATE in the SESSION_HANDOFF and Research Timeline, but the Unified Knowledge Ledger V1 (Markdown) does not include it in the V19-V29 reconciliation scope (V19 starts at CAND-056).

**Sources:**
- SESSION_HANDOFF.md: CAND-042 listed as COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED
- RESEARCH_TIMELINE.md §56: CAND-042 COMPONENT-CANDIDATE with N=5
- Unified Knowledge Ledger V1: Not in V19-V29 scope (V14 predates V19)

**Conflict:** CAND-042 exists in the repository but was created in V14 (pre-V19 scope of the original Unified Knowledge Ledger). The CSV Ledger expands scope to cover all research history.

**Resolution:** CAND-042 is included in the CSV Master Candidate Ledger with full provenance. Classification: COMPONENT-CANDIDATE. Standalone status: CLOSED. N=5 is extremely small; classification as COMPONENT-CANDIDATE may be generous but is preserved per original governance.

**Unresolved component:** Whether CAND-042's N=5 is sufficient for any future use remains a governance question.

---

## Exception 2: CAND-077 Exploratory Filter vs Governance Classification

**Issue:** Post-closure >15 bps breakout observation was initially treated as strengthening the State case but was later explicitly classified as EXPLORATORY EVIDENCE ONLY.

**Sources:**
- V26 G1 artifact: Baseline N=2084, Net=-0.85 bps, CF delta=+1.67 bps
- CAND-077 governance review: Post-closure filter exploration found >15 bps = 64.8% WR, +8.41 bps
- SESSION_HANDOFF §7: "These are NOT validated filters. Filter selected AFTER observing baseline outcome = selection bias."

**Conflict:** The exploratory observation is real data but was discovered through post-hoc analysis, creating selection bias.

**Resolution:** The ledger records the observation in the Exploratory Observations Ledger (OBS-001) with explicit provenance: "discovered post-closure, selection bias present." The governance classification (STATE REVIEW ELIGIBLE) is preserved. No threshold is ratified.

**Unresolved component:** Whether a formally pre-registered threshold hypothesis could validate the breakout-magnitude relationship remains a future governance question.

---

## Exception 3: CAND-083 Asymmetric Counterfactual Sample Size

**Issue:** CAND-083 treatment N=2,318 but counterfactual N=316. The asymmetric sample sizes could affect reliability of the +4.60 bps conditional delta.

**Sources:**
- V28 G1 artifact: Treatment N=2,318; CF N=316; CF net=-6.93 bps
- G1 V3 framework: No explicit minimum sample size asymmetry rule

**Conflict:** The CF sample is 7.3x smaller than the treatment sample. While the G1 V3 framework validated this as sufficient, the asymmetry is unusual.

**Resolution:** The ledger records the asymmetry in both the Candidate Ledger (EVID-009/010) and Evidence Ledger with explicit notes. The +4.60 bps conditional delta is preserved as reported. The asymmetry is documented as a limitation, not a disqualification.

**Unresolved component:** Whether a minimum CF sample size relative to treatment should be formally established in the G1 framework is an open governance question.

---

## Exception 4: Unified Knowledge Ledger Behavioral Knowledge Count Discrepancy

**Issue:** The Unified Knowledge Ledger V1 (Markdown) summary states "6 behavioural knowledge records" in §21 but lists 7 Knowledge IDs (K-V20-001 through K-V28-001).

**Sources:**
- Unified Knowledge Ledger V1 §21: "6 behavioural knowledge records"
- Unified Knowledge Ledger V1 §6: Lists K-V20-001, K-V22-001, K-V23-001, K-V26-001, K-V26-002, K-V27-001, K-V28-001 = 7 IDs

**Conflict:** Summary says 6 but detailed list shows 7.

**Resolution:** The CSV Behavioral Knowledge Ledger contains 12 knowledge records (including additional records for CAND-024, CAND-035, CAND-032, CAND-021, and CAND-064 that were not in the original V19-V29 scope). The correct count for V19-V29 scope is 7. The discrepancy in the original ledger summary is recorded as a documentation error.

**Unresolved component:** The summary count should be corrected to 7 in future documentation updates.

---

## Exception 5: Pre-V19 Candidate Numbering Gap

**Issue:** The research timeline and discovery database reference candidates CAND-010 through CAND-015 (pre-Research Factory era) but candidates CAND-001 through CAND-009 are not documented in any surviving artifact.

**Sources:**
- RESEARCH_TIMELINE.md: References CAND-010 (event-state duplication failure)
- RESEARCH_DISCOVERY_DATABASE.md: References CAND-012, CAND-013, CAND-015
- No artifacts reference CAND-001 through CAND-009

**Conflict:** The numbering implies CAND-001 through CAND-009 existed, but no evidence survives.

**Resolution:** The CSV Ledger documents CAND-010 as the earliest recoverable candidate. CAND-001 through CAND-009 are recorded as UNKNOWN/NOT_RECONSTRUCTABLE. No inference is made about their content.

**Unresolved component:** Whether CAND-001 through CAND-009 existed and what they contained is permanently unknown from current repository evidence.

---

## Exception 6: CAND-025 Component-Candidate vs UNQUALIFIED Status

**Issue:** CAND-025 is classified as both COMPONENT-CANDIDATE (CONDITIONAL) and UNQUALIFIED in different parts of the repository.

**Sources:**
- DISC-037: "CAND-025 is designated COMPONENT-CANDIDATE (CONDITIONAL)"
- SESSION_HANDOFF §40: "CAND-025 retained but UNQUALIFIED"
- RESEARCH_TIMELINE §38: "CAND-025 is considered COMPONENT-CANDIDATE"

**Conflict:** The terms COMPONENT-CANDIDATE (CONDITIONAL) and UNQUALIFIED appear to describe the same status differently.

**Resolution:** The ledger records CAND-025 as CLOSED (not in the active component register). The standalone status is CLOSED. The component status is UNQUALIFIED / not retained in the current component register (SESSION_HANDOFF does not list CAND-025 in §6 active components).

**Unresolved component:** Whether CAND-025 could be reconsidered for component status is a governance question that requires owner authorization.

---

## Exception 7: Historical G0 Naming Convention Inconsistency

**Issue:** Early Research Factory cycles used CAND-G0-XXX naming (e.g., CAND-G0-021) while later cycles dropped the G0 prefix (e.g., CAND-077).

**Sources:**
- V7-V16 artifacts: CAND-G0-018, CAND-G0-021, etc.
- V19+ artifacts: CAND-056, CAND-057, etc.

**Conflict:** Naming convention changed mid-project without explicit governance documentation.

**Resolution:** The CSV Ledger normalizes all candidate IDs to the CAND-XXX format (dropping the G0 prefix). The original G0-prefixed IDs are noted in the source artifact references.

**Unresolved component:** The naming normalization is a ledger-internal decision and does not alter any governance classification.

---

## Exception 8: SESSION_HANDOFF Commit Count Discrepancy

**Issue:** SESSION_HANDOFF.md states "14 commits total" for 2026-08-30 but git log shows 17 commits on that date (including V25 G1, V25 closure, and an earlier session consolidation).

**Sources:**
- SESSION_HANDOFF.md §0: "14 commits total"
- Git log: 17 commits dated 2026-08-30

**Conflict:** The commit count in SESSION_HANDOFF is understated.

**Resolution:** The ledger does not alter SESSION_HANDOFF. The actual commit count is 17. This discrepancy is noted but does not affect governance.

**Unresolved component:** SESSION_HANDOFF commit count should be corrected in a future documentation update.

---

*End of Reconciliation Exceptions V1.*
