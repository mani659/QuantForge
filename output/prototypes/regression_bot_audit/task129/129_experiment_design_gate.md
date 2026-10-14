# TASK129 — Experiment Design Gate Review (design only, not executed)

**Scope:** review the TASK128 preregistration draft for validity defects.
No execution, no tuning, no parameter choice.

## Defect 1 (blocking): fixed-TSMOM comparator executes a closed rule

The primary comparison requires running fixed 12/1 TSMOM — the DISC-022
rule itself — as the benchmark leg. Executing a closed mechanism, even as
a control, is re-execution of a closed line. PROTO-TREND-001's lawful
control precedent was all-signs-+1 (not a closed strategy). **Resolution
required:** replace the comparator (e.g., buy-and-hold NASDAQ100, which
tests momentum-vs-passive without running DISC-022) or obtain explicit
authorization to execute the closed rule as a benchmark. The current design
cannot proceed as written.

## Defect 2 (blocking if unaddressed): t-test without dependence robustness

Monthly paired momentum differentials are serially correlated; a plain
one-sample t-test overstates significance. **Required:** Newey-West
standard errors or block-bootstrap CIs, predeclared. The draft's bare
t-test + 95% CI is insufficient as specified.

## Defect 3 (non-blocking, disclosed): target_vol = 10% unsourced

The 10% target has no source basis; it is a chosen parameter. Predeclared
(good), but its arbitrariness must be recorded, and sensitivity to the
choice (e.g., 10% vs 15%) must either be predeclared or explicitly
excluded. Additionally the scaled leg usually holds |w| < 1 while the
fixed leg holds ±1 — the comparison confounds signal and leverage; disclose.

## Defect 4 (correctly marked, carried): MDE unresolved

Draft §7 properly marks the minimum effect unresolved rather than
inventing a threshold. Carried forward: the owner must set it (or accept a
structural sign-agreement-style criterion) before any test.

## Defect 5 (correctly marked, carried): cost model unresolved

Batch-1 family named as starting point; NASDAQ100-specific (CFD) costs to
be frozen. Carried forward — index-CFD spreads differ from ETF spreads.

## Defect 6 (design flaw): development-informed threshold

Draft §7 contemplates setting the MDE "based on the development-period
results." A threshold conditioned on development outcomes is a post-outcome
parameter for the final test. **Required:** fix all decision thresholds
before ANY period's outcomes are observed, or wall the final evaluation
behind a frozen respecification that the development results cannot alter.

## Defect 7 (limitation, disclosed): dividend omission

Price-only returns omit ~1%/yr distributions. Largely cancels in a paired
differential but not fully (legs differ in sign/size over time). Disclose;
do not adjust without a sourced total-return series (none exists for this
span in-repo).

## Chronological split: structurally sound

1986–2005 / 2006–2015 / 2016–2026 is genuinely chronological. No holdout
exists; protection is procedural only (freeze before final evaluation) —
acceptable if enforced, stated plainly.

## Gate verdict

Design is NOT valid as written (Defects 1–2 block). Defects 3–7 are
manageable via disclosure, predeclared robustness, and owner-set
thresholds. Even repaired, the design needs the §99.1 ruling (separate file).
