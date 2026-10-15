# TASK168 — S2 Single-Evaluation Authorization Record (EFFECTIVE)

**Status:** authorization act RECORDED from an explicit owner instruction.
Scope: ONE historical evaluation of frozen `PROTO-S2-001` exactly as
specified in the TASK167 package. No signature fabricated; no repeat
request made.

## 1. Authorization provenance

Owner message, **2026-10-15**, quoted verbatim as delivered to the
technical owner:

> "Daily reminder of you are technical owner, Authorize the single S2
> evaluation as specified in TASK167"

Effect, as stated in the task instruction carrying that message: this
authorizes the single evaluation described in TASK167, including use of
the specified existing SPY dataset solely for this evaluation and the
bounded computation required by the frozen protocol. This record is
filed as the provenance-carrying authorization document for that act
(precedent: TASK166 recorded owner selections by provenance without a
fabricated signature). It is NOT self-authorization: the act originates
from the owner, satisfying the TASK166-reserved evaluation-budget
requirement and closing TASK167's "remaining authorization act."

## 2. Scope and reason

One bounded historical evaluation of the frozen New-Year-week hypothesis
(first empirical test of an audited-clean, fully preregistered seasonal
rule; TASK167 information-gain justification). Reason: obtain the first
decisive PASS/FAIL/INCONCLUSIVE evidence under the frozen criterion.

## 3. Frozen binding (fingerprints verified pre-outcome)

- Spec: `PROTO-S2-001`, `task166/166_s2_frozen_spec.md`,
  SHA-256 `5a318e7e47263c67dc308adf9e326122e56b285e5eaaf585274867525a47eb94`
  (4414 B). Selections file `166_s2_owner_decisions.md`
  `12448126490fd1bbc4b926ac470a53b24a44c81b37fde1e2b7573e57b6ddce7c`.
- Data: `output/prototypes/lane_b_batch1/data/SPY.csv`, SHA-256
  `483919f897326b261a669bc595a37112b4de5222c4ad0ed84da08060f4b71231`
  (794,286 B), Stooq SPY daily 1993-01-29→2026-09-25, close column;
  use limited to this evaluation.
- Implementation: `output/prototypes/s2_newyear_week/s2_engine.py`
  SHA-256 `2892c8b5f3f9c13fe1dd3317d45f5f33725437be1f3936501943699dcff97f7b`
  (4556 B); synthetic suite `test_s2_engine_synthetic.py`
  `508c4e485e05f96150b0af979966692551a34bc1c5c4bb703e8743cd042cdb83`
  (12/12 at TASK166; re-run as preflight).
- Authorization package: `task167/167_s2_evaluation_authorization_package.md`
  `22b8eb46554f7c1437d17b0cf71a54aff3947b3f2b971c8dc398832816278b6e`.

## 4. Permitted computation (exactly one)

Windows FIRST_5_SESSIONS over eligible Januaries (1994–2026, ≈33,
mechanically determined); long 1.0×; ENTER Dec-close ×1.0015, EXIT
5th-January-session close ×0.9985 (10 spread + 5 slippage per side,
commission 0, 30 bps RT); NYSE-holiday/missing endpoints fail-closed
skip + count; primary endpoint = mean annual net return with 95%
bootstrap CI, i.i.d. over annual events, **B=10000, seed 20261015**
(the spec's only resampling procedure); PASS lower>0 / FAIL upper<0 /
INCONCLUSIVE covers zero. `TOM_CONTROL`: buy-and-hold over identical
span (first entry → last exit), same schedule once each, cumulative-net
DESCRIPTIVE only, no paired test. No magnitude bar imposed (owner did
not set one; frozen default stands).

## 5. Validity checks and stops

Pre-outcome stops: data SHA/date-scope mismatch, spec or implementation
fingerprint failure, synthetic preflight failure, TOM/cost/window/
endpoint under-definition, conflict with a mandatory owner-reserved
decision. Post-start: any execution error → preserve logs, report,
no fix-and-rerun. Completion → single report; zero variants, reruns,
tuning, second evaluations, selective exclusion.

## 6. Explicit non-effects

Research Capacity **HOLD** and Active Research **NONE** UNCHANGED — this
is a narrowly scoped, explicitly authorized activity under the governing
rules, not general research reactivation. No candidate registration or
promotion, no Phase IV, no governance change, no other-branch reopening,
no new data acquisition, no holdout access, no dataset substitution, no
deployment/paper/live trading, no commit, no push, no frozen-spec or
prior-artifact modification. A positive result is preliminary historical
evidence only; a negative result stands without rescue.

**Recorded before any outcome-dependent computation.**
