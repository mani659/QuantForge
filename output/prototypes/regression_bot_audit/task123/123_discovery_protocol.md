# TASK123 — Discovery Protocol (information-efficient staged design)

**Principle:** Maximize information gained per unit of engineering and data
cost. Every stage must produce a decision that is either (a) a definitive
advance or (b) a definitive stop — never an ambiguous continuation.

## Stage 0 — Hypothesis intake (hours, no data)

**Entry:** A named hypothesis with (i) a one-sentence economic mechanism,
(ii) a concrete falsifiable prediction, (iii) a named implementation route.

**Gate 0 (admission):**
- Similarity check against §99.1 families and closed candidates using the
  repository's mechanism-identity test.
- **If similarity is flagged:** require a *confirmatory test* (Stage 1)
  before final exclusion. The burden of proof shifts: the exclusion must
  show the implementation is empirically equivalent to a closed mechanism,
  not merely that it shares surface features.
- **If no similarity flag:** proceed to Stage 1.

**Stop criterion:** The hypothesis cannot state a falsifiable prediction,
or no implementation route exists using verified available resources.

## Stage 1 — Confirmatory screening (days, minimal data)

**Entry:** Admitted hypothesis.

**Activities:**
1. Data integrity check: SHA-256 verification of the target file against
   its reference hash; span/bar/monotonicity validation; instrument
   identity confirmation. Fail-closed on any mismatch.
2. Synthetic self-test of the implementation: planted-data tests verifying
   exact rule semantics, no look-ahead, fail-closed handling, determinism.
3. **Preregistered screening test:** smallest possible empirical test with
   explicit costs, adequate power, and predeclared stop/advance criteria.

**Gate 1 (screening):**
- **Stop:** data integrity fails, or screening result is clearly negative
  under the predeclared cost assumptions.
- **Advance:** screening result is positive AND the effect size exceeds the
  predeclared minimum detectable effect (MDE) at the assumed costs.
- **Inconclusive:** screening result is ambiguous. **Stop** — do not
  proceed to a larger test without a new decision (this prevents
  underpowered escalation).

**Budget:** One screening run, fixed config, no variants.

## Stage 2 — Confirmatory test (days, bounded)

**Entry:** Stage 1 passed.

**Activities:**
1. Preregister the full test design: primary outcome, statistical method,
   multiplicity treatment, power analysis, stop criteria, reporting
   requirements. Freeze before any outcome access.
2. Implement the exact frozen specification (minimal, no extra logic).
3. Execute the bounded test with owner-frozen costs.
4. Independent review of implementation conformance.

**Gate 2 (confirmatory):**
- **Stop:** preregistered bars not met. Record the result; no rescue.
- **Advance:** preregistered bars met. Proceed to Stage 3.

**Budget:** One test, fixed config. Exhausted budget requires a new
decision (§3B).

## Stage 3 — Validation and robustness (weeks, only if Stage 2 passed)

**Entry:** Stage 2 passed.

**Activities:**
1. Out-of-sample confirmation on a sealed holdout (if one exists and is
   authorized).
2. Parameter-neighborhood check (bounded, predeclared, multiplicity-
   controlled).
3. Robustness checks: sub-period stability, alternative cost assumptions,
   alternative execution assumptions.

**Gate 3 (validation):**
- **Advance:** confirmation result meets predeclared criteria.
- **Stop:** confirmation fails. Record; no rescue.

## Stage 4 — Controlled validation (only if Stage 3 passed)

**Entry:** Stage 3 passed.

**Activities:**
1. Paper trading or controlled forward evaluation with independent
   recording.
2. Pre-registered primary outcome, stop criteria, and reporting.
3. Operational readiness checklist.

**Authorization required before Stage 4:** Separate owner act. No
automatic progression.

## Protections (all stages)

- **Multiple testing:** Holm or equivalent family-wise control across all
  preregistered comparisons; no unregistered analyses.
- **Leakage:** synthetic self-test before any market data; no post-outcome
  specification changes; single tz mapping, single ATR convention, single
  resample rule.
- **Post-hoc changes:** any change after outcome access creates a new
  preregistration version; the previous result stands.
- **Stopping:** budget exhaustion stops all work; no "just one more run."

## What this protocol fixes

| Current defect | Protocol fix |
|---|---|
| Mechanism-identity exclusion without testing | Confirmatory test required before exclusion |
| Single-shot, no power analysis | Stage 1 screening with MDE and power |
| Cost blindness (79% UNKNOWN) | Owner-frozen costs required at every stage |
| No inferential statistics | Preregistered method with multiplicity control |
| Ambiguous continuation | Explicit stop/inconclusive/advance at every gate |
