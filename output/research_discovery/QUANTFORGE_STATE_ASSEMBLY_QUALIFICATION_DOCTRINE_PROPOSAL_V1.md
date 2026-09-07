# QUANTFORGE — STATE ASSEMBLY QUALIFICATION DOCTRINE — PROPOSAL V1

**Status:** PROPOSAL — PENDING OWNER RATIFICATION
**Date:** 2026-09-03
**Nature:** Governance doctrine proposal converting the owner's institutional-posture decision (Governed State / conditional-information pathway, 2026-09-03) into a reviewable, ratifiable framework.
**Repository effect until ratification:** NONE. This artifact is untracked and uncommitted. It does not amend, supersede, or reinterpret any existing governance document, including:
- `QUANTFORGE_G1_ECONOMIC_QUALIFICATION_FRAMEWORK_V3_RATIFICATION_V1.md`
- `QUANTFORGE_V26_CLOSURE_DYNAMIC_STATE_KNOWLEDGE_V1.md`
- `QUANTFORGE_CAND077_CAND081_STATE_GOVERNANCE_REVIEW_V1.md` (+ CAND-077 / CAND-083 reviews)
- `docs/SESSION_HANDOFF.md` (closed-line firewall: DISC-021…DISC-028, CAND closures)

No experiment, no candidate ID, no State ID, no ledger/DB/SESSION_HANDOFF change is authorized by this artifact.

---

## 1. DECISION RECORD

On 2026-09-03 the project owner committed QuantForge to the **Governed State (conditional-information) pathway**:
- The unit of economic qualification becomes the **assembled decision** (base layer + conditional/State layer, one cost charge), not the standalone layer alone.
- The State layer must prove **incremental value over a ratified real base** on the base's own cost schedule.
- The pathway carries **pre-written, evidence-based stop-rules**.

This document makes that commitment precise enough to ratify and, on ratification, to govern the next research cycle.

---

## 2. EVIDENCE BASE FOR THE DOCTRINE

### 2.1 The measured economic ledger (FACT, artifact-cited)

| Line | Expression | Scientific status | Economic status | Key magnitude | Authoritative artifact |
|---|---|---|---|---|---|
| ORD / DISC-026 (V1.1.0) | Opening-range breakout, M1 CFD family, exit 120-min close | SUPPORT (3/3 markets, Holm-adjusted) | **CLOSED — ECONOMICALLY NON-VIABLE / TRANSLATION FAILURE** | gross 1–2 bps vs minimum spread crossing | `ORD_V1_1_0_ECONOMIC_VIABILITY_ADJUDICATION_V1.md` |
| TRADEABLE_EDGE V27–V36 (CAND-080…107) | M1 → 30–60-min holds, USATECHIDXUSD | Valid, 9/9 gates | **0/20 standalone survivors**; both arms of every valid test gross ≈ +0.3–0.6 bps vs 2.0 bps friction | ≈ +0.5 bps gross wall | V27–V36 G1 artifacts; V37A replication |
| H01 / DISC-023 economic translation | Daily US-equity volatility-response asymmetry | SUPPORTED (V1.3.0) | **CLOSED — ECONOMIC FAILURE** overall (historical era strongly negative) | HISTORICAL dm ≈ −0.14%/day; **CONTEMPORARY dm ≈ +0.078%/day (PASS, base and stress)** | `H01_ECONOMIC_V1_EXEC_04/results_H01_ECONOMIC_V1.json`; run log "Final Classification: ECONOMIC FAILURE" |
| CAND-077 / 081 / 083 (SRE pool) | M1 conditional structure, USATECHIDXUSD | Conditional deltas +1.2–4.6 bps (single market) | Never given an economic gate (no base); V37A cross-market replication INCONCLUSIVE/ECONOMICALLY NEGATIVE | conditional only | V26–V28 G1 screens; V37A adjudication `bb73d06` |
| SEED-002 | State × downstream-event interaction | — | NEGATIVE (single governed interaction test) | — | SEED-002 results artifact |

### 2.2 What the ledger demonstrates (INFERENCE)

1. **Three independent lines** — different instruments, horizons, data types, cost regimes — all produced the same outcome at the economic gate: scientific/behavioral plausibility survived; economics did not. This is the program's strongest empirical regularity.
2. **The standalone-first qualification rule is the program's least-tested assumption.** Every layer was required to survive costs alone before assembly was permitted; assembly (base + conditional layer under one cost charge) has **never once been tested** in the repository's history.
3. **The only economically passing cell in the entire record** is the H01 contemporary-era daily US-equity result (+0.078%/day incremental, CI excluding zero, passing in both base and stress cases). It sits inside a line whose overall registered verdict is ECONOMIC FAILURE because the historical era contradicts at −0.14%/day.
4. **The CAND-077/081/083 conditional observations do not transfer** to the only surviving base candidate: they are M1-CFD-family structures; the H01 contemporary cell is a daily US-equity decision context. Posture 2 therefore commits to **relocating conditional characterization to the equity decision context**, not recycling the CFD state pool.

### 2.3 Consequences the doctrine must respect (FACT)

- The CFD/M1 family has **no ratified base** and, per ORD's and the TRADEABLE_EDGE line's measured economics, is unlikely to produce one at ≥2 bps friction. State work anchored to that family would violate the real-base rule before it started.
- H01's translation line is **CLOSED with rerun prohibited** (`POST_H01_ORD_GOVERNANCE_RECONCILIATION_V1.md`: "Rerun prohibited?: YES"). Anchoring to the contemporary-era cell therefore requires a **governed era-scope decision** that amends the closed line's disposition — an owner act, not a research act.
- Any new conditional characterization on the equity context is a **new hypothesis** under G0 rules (fresh provenance, Mechanism–Observable Challenge, registration) — not a reuse of CAND-077/081/083 definitions.

---

## 3. PROPOSED DOCTRINE CHANGES

Ratification adopts the following four provisions, expressed as amendments to the *qualification layer* of the existing doctrine (G1 V3 + State knowledge framework). Existing hard gates, validity doctrine, and the closed-line firewall are untouched.

### D1 — Assembled unit of economic qualification

Current rule (implicit): a State object qualifies only against a *downstream Alpha that itself qualified standalone*.
Proposed rule: the unit of economic qualification is the **assembled decision** — a ratified base layer plus a conditional/State layer, executed under **one cost charge** on the base's own trade schedule. A State object may earn qualification by producing a **registered incremental economic result over the ratified base**, without the base having first qualified as standalone Alpha — provided the base carries a **positive, cost-registered economic cell** (see D2).

This does NOT weaken standalone Alpha claims: a candidate claiming Alpha must still pass G1 V3 standalone. It creates a second, explicitly governed path for State objects.

### D2 — Real-base rule (the OBS-001 firewall)

A State layer may only be evaluated against a **ratified base**: a decision context with (a) an authoritative, cost-registered economic measurement in the record, (b) at least one economically positive cell, and (c) a frozen, registered operational definition.

Explicitly prohibited bases: hypothetical P&L, unregistered event families, M1-CFD decision contexts whose measured gross headroom (ORD ≈1–2 bps; TRADEABLE_EDGE ≈0.5 bps) is below the ≥2 bps cost floor, retroactively designated downstream objects (CAND-024/035 bar retained), and any base invented to make a State observation look useful (the documented `OBS-001` / STATE_DISGUISED_AS_ALPHA failure mode).

### D3 — Incremental-value requirement

State-layer qualification evidence is **delta-over-base measured on the base's matched population under the base's cost schedule** — never standalone-looking conditional group-mean deltas measured on the State layer's own population. The State layer must shift the base's conditional economics (mean/median/WR on the base's outcome definition) by a registered, pre-specified magnitude rationale. Group-mean deltas of the CAND-077/081/083 style are characterization evidence only — they never become qualification evidence by themselves.

### D4 — Pre-written stop-rules

The State pathway closes on evidence when any of the following occurs (each adjudicated under G1 V3 holistic doctrine, none a numerical hard gate):
1. The ratified base fails re-verification on its own registered economics.
2. The first registered assembled test shows no positive incremental delta over the base with adequate data integrity.
3. Incremental deltas are temporally inconsistent across the base's pre-registered windows (mirror of the V37A Level-4 failure).
4. No base can be ratified within one governed decision cycle.
5. Data quality or cost-model integrity cannot be established for the assembled test.

Closure under D4 is recorded as negative knowledge; it does not erase base or State characterization evidence.

---

## 4. BASE-ANCHOR DETERMINATION

### 4.1 Candidates screened (FACT)

| Candidate base | Verdict | Reason |
|---|---|---|
| ORD V1.1.0 (CFD M1 breakout) | **NOT RATIFIABLE** | Closed — ECONOMICALLY NON-VIABLE; 1–2 bps gross vs spread |
| TRADEABLE_EDGE family (USATECHIDXUSD M1) | **NOT RATIFIABLE** | 0/20; ≈0.5 bps gross wall at 2 bps friction; V37A replication non-robust |
| H01 full program (historical + contemporary) | **NOT RATIFIABLE AS-IS** | Overall ECONOMIC FAILURE; rerun prohibited |
| **H01 contemporary-era cell** | **SOLE RATIFIABLE CANDIDATE** | +0.078%/day incremental, CI excluding zero, PASS in base and stress; modern-era execution cost context |

### 4.2 Recommendation

The sole base candidate is the **H01 contemporary-era daily US-equity decision context** (post-shock volatility-response signal, one-day forward outcome, modern-era cost schedule). Ratification of the doctrine is **conditional** on a separate owner decision (Ratification Item B) authorizing the **era-scoped amendment** of the H01 translation disposition from "CLOSED — ECONOMIC FAILURE (rerun prohibited)" to "closed as a full-program claim; contemporary era preserved as a ratified base candidate," with the historical-era contradiction recorded as negative knowledge and never re-litigated as a standalone claim.

### 4.3 Honest consequence, stated explicitly

Under this anchor, the existing CAND-077/081/083 M1-CFD state observations are **archived single-market knowledge**; they cannot be carried into the assembled test because no CFD-family base is ratifiable on current evidence. Posture 2 therefore funds **new conditional characterization on the equity decision context** (fresh G0 provenance, fresh registration) — relocation, not recycling. If the owner is unwilling to fund relocation, the honest reading is that Posture 2 has no executable first test and the doctrine should not be ratified in this form.

---

## 5. FIRST GOVERNED TEST — ARCHITECTURE SKELETON (design only; nothing executed)

```text
Stage A — Base era-scope governance decision (owner; Ratification Item B)
Stage B — Registered re-verification of the H01 contemporary-era base economics
          on its own frozen universe, eras, and cost cases (replication of the
          passing cell; NOT a new signal)
Stage C — New governed conditional hypothesis on the equity decision context
          (fresh G0: mechanism, observable, counterfactual; CAND-099 lesson
          applied — no hard mechanism gate)
Stage D — Assembled incremental test: base outcomes conditioned on the Stage-C
          state, one cost charge, matched populations, pre-registered metrics
Adjudication — D3 incremental evidence; G1 V3 holistic classification;
          D4 stop-rules apply at every stage boundary
```

Stage B requires no re-opening of the closed H01 claim (it re-measures the passing cell under the frozen definition). Stage C and D are separately registered experiments with zero methodological discretion; each stage halts for governance between stages.

---

## 6. WHAT IS NOT AUTHORIZED (until/unless ratified)

- No assembled test, no Stage A–D execution, no base re-verification run.
- No CAND or State ID creation; no ledger/DB/timeline/SESSION_HANDOFF modification.
- No re-opening of H01's full-program economic claim; the historical-era negative stands as recorded.
- No re-opening of ORD, the TRADEABLE_EDGE closures, or any DISC line.
- No State-layer work on the M1-CFD family in the absence of a ratified base.
- No numerical qualification gates invented (D4 is qualitative/governance-based).

---

## 7. RATIFICATION ITEMS (owner)

- **Item A — Doctrine:** Adopt D1–D4 as the qualification-layer amendment (assembled unit; real-base rule; incremental-value requirement; stop-rules).
- **Item B — Era-scope amendment:** Authorize the H01 contemporary-era cell as the ratified base candidate, amending the H01 translation disposition as specified in §4.2, with the historical-era contradiction preserved as negative knowledge.
- **Item C — Relocation mandate:** Confirm that Posture 2 funds new conditional characterization on the equity decision context (Stage C provenance), with the CAND-077/081/083 M1-CFD observations archived as single-market knowledge.

---

## 8. OWNER RATIFICATION BLOCK

```text
OWNER RATIFICATION STATUS: PENDING
Item A (doctrine):   [ ]
Item B (era-scope):  [ ]
Item C (relocation): [ ]
```

On ratification: this document becomes `…_DOCTRINE_V1` (ratified), a commit is made containing only this artifact, and the DB/timeline/SESSION_HANDOFF updates occur as a separate governed milestone. On rejection or material amendment, this proposal is revised or withdrawn; no research consequences follow either way.

**Git integrity (this task):** HEAD unchanged; no authoritative file modified; only this untracked proposal artifact created; pre-existing dirty/untracked files untouched.
