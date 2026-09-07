# QUANTFORGE — G0 PROCESS REFINEMENT

## Mechanism-Observable Challenge: Prospective Adversarial Scrutiny Requirement

**Date:** 2026-09-01
**Effective:** V34 G0 onward (prospective only)
**Status:** RATIFIED — PROSPECTIVE GOVERNANCE REFINEMENT
**Authoritative prior:** V29–V33 Research Factory Meta-Audit

---

## 1. Purpose

This document records a prospective refinement to the QuantForge G0 discovery process. It introduces a mandatory **Mechanism-Observable Challenge** — an adversarial evidence requirement applied to every candidate before G1 authorization.

This is NOT:
- A hard rejection gate
- An automatic scoring system
- A replacement for the G0 integrity/prior-art audit
- A post-hoc judgment applied to historical candidates

This IS:
- A mandatory adversarial reasoning exercise
- A structured challenge to the mechanism→observable mapping
- A protection against narrative inflation and proxy substitution
- A prospective requirement beginning with V34

---

## 2. Evidence Basis

The V29–V33 Research Factory diagnostic (completed 2026-09-01) identified a consistent pattern:

**The G0 process correctly rejects redundant and infeasible candidates.**
**The G1 hard gates correctly pass valid measurements.**
**But candidates whose economic mechanisms are theoretically coherent frequently fail to produce economically meaningful effects at G1.**

The dominant failure modes observed were:

1. **Mechanism→observable mapping weakness.** The LLM generates a plausible market narrative, but the observable proxy does not faithfully capture the claimed mechanism, or the mechanism does not produce the hypothesized effect on the observable.

2. **Narrative inflation.** Sophisticated economic language is attached to a weak or insufficiently challenged observable.

3. **Proxy substitution.** The observable measures a different economic process than the one claimed in the hypothesis.

4. **Base-rate insensitivity.** The G0 process does not explicitly require the LLM to justify why THIS candidate should overcome the historically poor success rate.

These failures do NOT indicate LLM incompetence. They indicate a process gap: the G0 does not currently require explicit adversarial scrutiny of the mechanism→observable mapping.

---

## 3. What Changed

### New mandatory section: Mechanism-Observable Challenge

Beginning with V34 G0, every candidate must answer eight explicit challenge questions before G1 authorization. These questions are:

#### A. Mechanism Independence
> What market phenomenon is hypothesized independently of the proposed feature?

Requires the LLM to articulate the economic process in terms independent of the specific indicator or formula being proposed. Prevents circular reasoning where the feature IS the mechanism.

#### B. Proxy Challenge
> How could the observable be generated WITHOUT the claimed mechanism?

Forces the LLM to consider whether the observable could arise from an unrelated process. A candidate where the observable can be fully explained by a known alternative mechanism receives lower proxy confidence.

#### C. Alternative Explanation
> What competing market state or process could create the same observable?

Explicitly requires identification of confounds. Prevents the LLM from ignoring obvious alternative explanations.

#### D. Observable Fidelity
> Why is the proposed observable a reasonable measurement of the claimed mechanism?

Requires the LLM to defend the proxy validity. This is the core mechanism→observable bridge.

#### E. Expected-Effect Bridge
> Why should this observable alter the subsequent outcome distribution?

Requires an explicit economic bridge from mechanism to price outcome. "This is interesting" is not sufficient; the LLM must articulate a causal pathway.

#### F. Falsification
> What result would clearly contradict the mechanism?

Requires the LLM to state a falsification condition. Prevents confirmation-compatible storytelling where any result can be retroactively explained.

#### G. Tradeability Challenge
> What would make the effect disappear after realistic costs?

Requires the LLM to identify fragilities: latency sensitivity, spread sensitivity, execution timing, sample size dependence, regime dependence. Prevents the presentation of marginal effects as obvious opportunities.

#### H. Base-Rate Challenge
> Given the historical QuantForge base rate of 0 G2 promotions across ~90 tested candidates, what specific property makes this candidate sufficiently worth testing?

Requires the LLM to explicitly justify the investment of G1 resources against the poor historical base rate. This is context, not a veto — but it prevents automatic optimism.

---

## 4. Scoring: Proxy Confidence (NOT a hard gate)

Each candidate receives a **Proxy Confidence** assessment:

| Level | Meaning |
|---|---|
| **STRONG** | Observable clearly captures the claimed mechanism; alternative explanations are implausible |
| **MODERATE** | Observable is a reasonable proxy but alternative explanations exist; mechanism bridge is plausible |
| **WEAK / UNCERTAIN** | Observable may not capture the claimed mechanism; alternative explanations are strong; mechanism bridge is speculative |

**Proxy Confidence does NOT determine G1 eligibility.**

A candidate with WEAK proxy confidence may still proceed to G1 if:
- The mechanism is genuinely novel
- The observable is at least defensible
- No data infeasibility exists
- No direct redundancy exists

But weak proxy confidence must be **explicitly recorded** in the G0 artifact.

The CAND-099 lesson is critical here: **a mechanism explanation can be wrong or incomplete while the observable may still contain economically informative structure.** The G0 process must preserve this possibility.

---

## 5. What Did NOT Change

The following governance elements remain unchanged:

- **G0 integrity/prior-art audit** — unchanged
- **G1 V3 two-layer architecture** (hard validity gates + economic evidence adjudication) — unchanged
- **Nine hard validity gates** — unchanged
- **Economic adjudication classes** — unchanged
- **Four artifact classes** (Alpha, Rare-Event, State, Regime) — unchanged
- **Closed-line firewalls** — unchanged
- **State library classifications** — unchanged
- **Relational governance** — unchanged
- **Forward runtime protection** — unchanged
- **APEX modular branch governance** — unchanged
- **No universal hard economic thresholds** — unchanged
- **Prior-art novelty process** — unchanged (mechanism-level, not keyword/formula)

---

## 6. Why This Is NOT a Hard Gate

The Mechanism-Observable Challenge is designed to **surface weaknesses**, not to **automatically reject candidates**.

The reasons against a hard gate:

1. **CAND-099 demonstrated that mechanism falsification does not imply observable invalidity.** A hard mechanism-quality gate might have rejected CAND-099 before G1, losing the genuinely informative finding about transition quality.

2. **Economic discovery is inherently uncertain.** The value of G1 is precisely to test whether a plausible mechanism produces real economics. Pre-filtering too aggressively risks losing potentially valuable discoveries.

3. **Simple observables can be novel.** A candidate with a simple formula may represent a genuinely new mechanism. The challenge surfaces whether the simplicity is a strength (clean measurement) or a weakness (insufficient mechanism).

4. **The existing G0 integrity audit already handles true failures.** Data infeasibility, redundancy, semantic contradiction, and undefined temporal structure are already caught by the integrity audit. The Mechanism-Observable Challenge adds adversarial scrutiny to the mechanism→observable mapping specifically.

---

## 7. How CAND-099 Informed the Design

CAND-099 (Volatility Regime Transition Quality) was registered with the mechanism: "smooth transitions indicate orderly repricing; sharp transitions indicate stress." The G1 result **contradicted the hypothesis direction** — sharp transitions massively outperformed smooth transitions (+18.08 bps, 99% WR vs 40% WR, N=100 per group).

This finding has two important implications:

### A. The mechanism explanation was wrong
The LLM's proposed causal pathway (smooth → orderly → better) was incorrect. A hard mechanism-quality gate might have caught this weakness.

### B. The observable was genuinely informative
Despite the wrong mechanism explanation, the transition-quality observable captured a real economic phenomenon. A hard gate that rejected CAND-099 based on mechanism weakness would have lost this finding.

### The design compromise
The Mechanism-Observable Challenge surfaces the weakness (via proxy confidence and falsification) but does not automatically reject. This preserves the ability to discover that an observable is informative even when the mechanism explanation is incomplete or wrong.

The G0 artifact must explicitly record:

```
MECHANISM CONFIDENCE: [assessment]
OBSERVABLE INFORMATION POTENTIAL: [assessment]
```

as separate dimensions.

---

## 8. How False-Rejection Risk Is Controlled

The challenge is designed with specific false-rejection controls:

1. **No automatic scoring threshold.** Proxy confidence is qualitative (STRONG/MODERATE/WEAK), not a numeric score that could be gamed.

2. **Weak proxy confidence does not prevent G1.** Only clearly invalid cases (data infeasibility, redundancy, semantic contradiction) prevent G1 under existing governance.

3. **The challenge is adversarial, not eliminative.** Its purpose is to make weaknesses visible, not to create a rejection list.

4. **Simple observables are not penalized.** A simple formula may have STRONG proxy confidence if it clearly measures the claimed mechanism.

5. **The LLM may argue against its own challenge.** If the LLM can provide a strong defense of the mechanism→observable mapping, that defense is recorded as part of the candidate's evidence profile.

6. **The base-rate challenge provides context, not a veto.** "The base rate is poor" does not prevent testing; it requires explicit justification for why THIS candidate deserves G1 investment.

---

## 9. Implementation Specification

### Where the challenge appears in the G0 artifact

The Mechanism-Observable Challenge is a **mandatory section within each candidate's G0 definition**, inserted after the Core Hypothesis and before the Observable Variables / Measurement sections.

The exact G0 artifact structure for each candidate becomes:

```
Candidate ID
Name
Expression Class
Mechanism Family
Why This Gap Exists
Prior Research Coverage
Pre-State
Transition / Evolution
Post-State
Participant / Market Constraint
Economic Mechanism
Economic Consequence
Core Hypothesis
→ NEW: Mechanism-Observable Challenge (8 questions + proxy confidence)
→ NEW: Mechanism Confidence / Observable Information Potential (separate)
Observable Variables
Measurement / Implementation
Temporal Structure
Parameter Audit
```

### What the LLM must produce

For each candidate, the G0 artifact must include:

1. Explicit answers to all 8 challenge questions (A through H)
2. A Proxy Confidence rating (STRONG / MODERATE / WEAK)
3. Separate Mechanism Confidence and Observable Information Potential assessments
4. An explicit statement of what would falsify the hypothesis
5. An explicit justification for why this candidate deserves G1 testing given the base rate

### What is NOT required

- No numeric scoring
- No automatic rejection
- No optimization of the challenge answers
- No post-G1 revision of the challenge answers

---

## 10. Effective Version

| Element | Applies From |
|---|---|
| Mechanism-Observable Challenge | V34 G0 onward |
| Proxy Confidence rating | V34 G0 onward |
| Mechanism Confidence / Observable Information Potential separation | V34 G0 onward |
| Base-rate challenge | V34 G0 onward |
| All other governance | Unchanged |

Historical candidates (V19–V33) are NOT retroactively scored against this framework.

---

## 11. Relationship to Existing Governance

```
G0 KNOWLEDGE-GAP DISCOVERY
        ↓
CANDIDATE DEFINITION
        ↓
→ MECHANISM-OBSERVABLE CHALLENGE (NEW)
        ↓
G0 INTEGRITY / PRIOR-ART AUDIT (unchanged)
        ↓
G1 ECONOMIC PLAUSIBILITY SCREEN (unchanged)
        ↓
G1 V3 ADJUDICATION (unchanged)
        ↓
G2 QUALIFICATION (if applicable)
```

The challenge sits between candidate definition and integrity audit. It is a pre-audit adversarial exercise, not a replacement for any existing governance layer.

---

## 12. Verification

Confirm:
- ✅ No hard mechanism-quality gate introduced
- ✅ No automatic rejection system introduced
- ✅ No numeric scoring introduced
- ✅ CAND-099 lesson preserved (mechanism ≠ observable)
- ✅ Historical candidates not retroactively scored
- ✅ G1 V3 framework unchanged
- ✅ G0 integrity audit unchanged
- ✅ State library unchanged
- ✅ Relational governance unchanged
- ✅ Forward runtime unchanged
- ✅ APEX RB001–RB004 unchanged
- ✅ Closed-line firewalls unchanged

---

*Governance refinement recorded. Effective V34 G0 onward. 2026-09-01.*
