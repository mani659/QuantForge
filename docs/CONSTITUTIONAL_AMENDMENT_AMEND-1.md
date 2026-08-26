# QuantForge Constitutional Amendment — AMEND-1

**Title:** Formal Authorization of Stateful Deployment Orchestration and the `DeploymentDependencies.observation_policy` Dependency

**Constitution:** QuantForge Constitution v1.0 (PERMANENTLY FROZEN)
**Status:** **APPROVED — RATIFIED** (owner approval)
**Prepared:** 2026-08-12
**Approved:** 2026-08-12 (project owner)
**Amending:** `docs/PHASE7_FREEZE_APPROVED.md` (Phase 7 Deployment Layer freeze); associated descriptive documentation

---

## 1. Amendment Identifier / Version

- **Identifier:** AMEND-1
- **Version:** 1.0.0
- **Authorized items:** exactly two —
  - **Amendment A** — Stateful multi-snapshot `DeploymentOrchestrator`
  - **Amendment B** — `DeploymentDependencies.observation_policy` required dependency

Both items were introduced by commit `b67a3cc` (`feat: implement strategy packaging, admission controller, and deployment updates`) and are ratified as a single governance action.

---

## 2. Date

Prepared 2026-08-12. **Formally approved by the project owner on 2026-08-12** (owner approval recorded in the ratification instruction for this amendment). The resulting freeze record is reflected in `docs/PHASE7_FREEZE_APPROVED.md` and `docs/CONSTITUTION_v1.0.md`.

---

## 3. Constitutional Authority

The following provisions establish both the prohibition and the amendment mechanism:

- **`docs/CONSTITUTION_v1.0.md` §3:** "No future sprint may modify these phases directly. Only constitutional amendments may change frozen architecture."
- **`docs/CONSTITUTION_v1.0.md` §4.14:** "Frozen Layers Are Immutable. Once frozen, no layer may be modified without a constitutional amendment."
- **`docs/CONSTITUTION_v1.0.md` §8 — Constitutional Amendment Process:** (1) architecture proposal; (2) independent constitutional audit; (3) documentation approval; (4) permanent freeze update. "**No implementation may occur before constitutional approval.**"
- **`docs/CORE_FREEZE.md`:** Phase 7 frozen; future work extends the platform via new implementations of existing contracts; foundational changes require formal architecture review.
- **`docs/PHASE7_FREEZE_APPROVED.md` §6:** the listed components "must NOT be modified unless a Constitutional Review explicitly approves it"; **§8:** deficiencies "must be addressed through formal constitutional review — not through ad hoc modification during implementation."
- **`docs/ROADMAP.md`:** "No modification of Deployment contracts is permitted without a formal Constitutional Review."

---

## 4. Original Frozen Rule (exact wording)

From `docs/PHASE7_FREEZE_APPROVED.md`:

- **§2 Scope:** "**Deployment Orchestrator** — The stateless coordinator that routes each market observation sequentially through the complete scientific pipeline — Observation → Evidence → Behaviour → Interpretation → Decision → Risk — terminating at the position specification boundary."
- **§4 Statelessness:** "**Deployment remains stateless.** All deployment components hold no mutable state between calls. State resides exclusively in the Execution Domain."
- **§4 Behavioural History:** "**Deployment never stores behavioural history.** No timeline, window, or historical accumulation exists in the Deployment Layer. Behavioural history remains exclusively in the Behavioural Reality domain."
- **§4 Coordination Only:** "Every Deployment component is a coordinator, translator, assembler, or factory. None is a decision-maker."
- **§6 Prohibited Modifications:** `DeploymentRuntime`, `DeploymentContext`, `DeploymentAssembler`, `DeploymentBootstrap`, **`DeploymentOrchestrator`**, `MarketDataAdapterContract`, `GenericMarketDataAdapter`, `PaperTradingRunner`, `RunnerResult`, `DeployedPipeline`, `DeploymentConfiguration`, `DeploymentRegistries`, **`DeploymentDependencies`** — "constitutionally frozen and must NOT be modified unless a Constitutional Review explicitly approves it."
- **`docs/ARCHITECTURE.md` (descriptive):** "**DeploymentOrchestrator**: Coordinates the full BOE pipeline per EnvironmentSnapshot. It maintains no internal state. It routes data perfectly sequentially from observation through to risk calculation."

---

## 5. Proposed Amended Rule

The constitutional language of the Deployment Layer boundary is restated precisely as follows:

> **Behavioural Reality owns behavioural history.**
> Deployment may coordinate the lifecycle of Behavioural-Reality-owned observation state across multiple snapshots.
> Deployment does not become the owner of behavioural history and does not define behavioural science.

**Amendment A (rule change):** The clause "The stateless coordinator…" and "All deployment components hold no mutable state between calls. State resides exclusively in the Execution Domain." are amended to:

> **Deployment coordinates; it does not own.** The `DeploymentOrchestrator` routes observations sequentially through the complete scientific pipeline and may retain references to, and coordinate the lifecycle of, Behavioural-Reality-owned observation windows (`BehaviorObservationWindow` / `ActiveObservationTimeline`) across multiple `EnvironmentSnapshot` calls. Deployment holds **no behavioural history of its own**: accumulated frames, timelines, and observation policy decisions remain owned by the Behavioral Reality domain. Deployment introduces no scientific interpretation, no detector semantics, and no decision-making.

**Amendment B (rule change):** The frozen dependency set of `DeploymentDependencies` is extended by exactly one required field:

> `observation_policy: ObservationPolicyContract`

with the semantics that Deployment receives the policy as an injected dependency (constructed by the deployment actor), threads it deterministically through `DeploymentBootstrap`, and consumes it exclusively through the existing `BehaviorObservationWindow.evaluate_policy(...)` mechanism. Deployment embeds no observation-policy semantics.

All other Phase 7 frozen responsibilities, the canonical deployment pipeline order, and the remainder of the prohibited-modifications list remain unchanged.

---

## 6. Exact Affected Components

- `boe/deployment/orchestrator.py` — `DeploymentOrchestrator` (Amendment A; committed in `b67a3cc`).
- `boe/deployment/bootstrap.py` — `DeploymentDependencies` + `DeploymentBootstrap.create` threading (Amendment B; committed in `b67a3cc`).
- Supporting test updates required by the constructor change (already committed in `b67a3cc`): `tests/test_bootstrap.py`, `tests/test_historical_adapter.py`, `tests/test_deployment_orchestrator.py`.
- Documentation affected by the restated boundary (pending the documentation-approval step): `docs/PHASE7_FREEZE_APPROVED.md`, `docs/ARCHITECTURE.md` (orchestrator description), `docs/CONSTITUTION_v1.0.md` (amendment register), `docs/ROADMAP.md`, `docs/CHANGELOG.md`.

---

## 7. Architectural Rationale

- The Phase 7 closure record (`phase78_content.txt`, "Remaining Known Debt — Future Enhancements") explicitly anticipated the need: "The current `DeploymentOrchestrator` is stateless and processes each snapshot in total isolation (instantiating a new Candidate and BOW per snapshot). It cannot observe phenomena *across* snapshots (such as recoil over multiple candles). The orchestrator will need stateful extensions to handle temporal evidence."
- Multi-frame temporal evidence (recoil, persistence, compression observation) is impossible under the one-frame-per-snapshot model; the stateful orchestrator supplies the cross-snapshot lifecycle the Behavioral Reality temporal ontology was designed to support.
- The change is confined to the coordinator's lifecycle management; the scientific pipeline stages (observation → evidence → profile → interpretation → decision → risk → position specification) are unchanged in order and responsibility.

---

## 8. Domain-Ownership Analysis

- **Behavioral history owner:** `BehaviorObservationWindow` (boe/observation/bow.py) accumulates `BehaviorFrame` objects into its internal `ActiveObservationTimeline`; `evaluate_policy` and `freeze` operate on that timeline. Both contracts live in the Behavioral Reality domain and are **unmodified**.
- **Policy ownership:** `ObservationPolicyContract` / `ObservationDecision` / `TerminationReason` remain owned by the frozen observation contracts (Behavioral Reality); `DefaultObservationPolicy` is a production implementation of that contract.
- **Deployment role:** the orchestrator holds references to Candidate / BOW / ObservationDecision objects across calls purely to coordinate lifecycle and routing. It stores no frames and reconstructs no behavioural meaning. This preserves the constitutional principles of Single Ownership (§4.3) and No Duplicate Responsibilities (§4.16).

---

## 9. Research-Semantics Firewall Confirmation

Verified against the committed implementation: no z-score, momentum, recoil, persistence, ATR, scientific threshold, detector scoring, or inferred detector parameter appears anywhere in `boe/deployment/` or `assembly/`. `config/recoil_rules.json` is not referenced by either path. `behavior_strength` values written by the orchestrator are categorical tokens consistent with the `BehaviorFrame` contract ("an architectural category supplied by the caller, never a numerical indicator, threshold, or internal detector score"). The detector remains the sole trigger via `BehaviorDetectorContract.observe(...)`.

---

## 10. Compatibility Analysis

Against Constitution v1.0 §4 principles: downward information flow (§4.2) — preserved; single ownership (§4.3) — preserved (history owned by Behavioral Reality); one responsibility per phase (§4.4) — preserved; research never executes (§4.5) — preserved; identity transition at deployment construction (§4.10) — preserved; frozen layers immutable except by amendment (§4.14) — this amendment is that instrument; no duplicate responsibilities (§4.16) — preserved; no circular dependencies (§4.17) — preserved. The restated boundary introduces no new architectural layer, no new registry, and no new identity system.

---

## 11. Test Evidence

- `python -m pytest tests/ -q` → **614 passed**
- `python -m pytest tests/ -q -W error` → **614 passed**
- Temporal/orchestrator tests assert genuine invariants: multi-frame accumulation across snapshots, policy-controlled continuation and termination, candidate isolation, same-snapshot terminate + new trigger, deterministic cleanup, and fail-closed exception handling.

---

## 12. Procedural Irregularity Acknowledgment

The implementation of the two items appeared in commit `b67a3cc` **before** formal constitutional approval, contrary to Constitution v1.0 §8's requirement that "No implementation may occur before constitutional approval." This history is not concealed or rewritten. The purpose of AMEND-1 is to formally regularize and authorize the architecture **prospectively**. AMEND-1 does not describe approval as having preceded `b67a3cc`.

---

## 13. Explicitly Excluded Changes

AMEND-1 authorizes **nothing** beyond the two items in §6. Explicitly not authorized: implementation of `BehaviorDetectorContract` or `ObserverContract`; recoil/persistence/threshold semantics; research-semantics reconstruction; modification of evidence/temporal/detector/lifecycle/research contracts; expansion of Strategy Assembly or its admission gates; observer registry; fingerprint expansion; serialization; broker/live infrastructure; Research Factory changes; redesign or reversion of the temporal architecture beyond the ratifying scope.

---

## 14. Approval Status

**APPROVED — RATIFIED.**

- **Approving authority:** the project owner.
- **Approval date:** 2026-08-12.
- **Basis:** the owner's explicit ratification instruction for this amendment, issued after the independent Constitutional Review concluded the changes were architecturally legitimate and ratifiable under Constitution v1.0 §8.
- **Scope:** exactly the two items in §6 (Amendment A — stateful multi-snapshot `DeploymentOrchestrator`; Amendment B — `DeploymentDependencies.observation_policy`). Nothing else is authorized by this amendment.

Per the repository's governance convention, ratification is recorded here and reflected in the permanent freeze record (`docs/PHASE7_FREEZE_APPROVED.md`) and the constitutional register (`docs/CONSTITUTION_v1.0.md`). Passing tests and prior audits informed the decision but did not constitute approval; the approval itself is the owner's act recorded above.

---

## 15. Resulting Freeze Status

**Ratified 2026-08-12.** The Deployment Layer remains constitutionally frozen, with the boundary restated as in §5. The §8 documentation-approval and permanent-freeze-update steps are complete (see §16). **Strategy Assembly V1 is FROZEN** as of the ratification, with its admission boundary, package-consumption boundary, research-semantics firewall, fail-closed dependency boundary, and deployment-artifact construction boundary frozen; no further Assembly expansion occurs without a new architectural decision. End-to-end deployment remains separately blocked by the missing genuine `BehaviorDetectorContract` implementation, which is **DESIGN BLOCKED — scientific specification unavailable; no detector semantics or thresholds may be invented from existing research artifacts.**

---

## 16. §8 Process Completion Record

1. **Architecture proposal** — COMPLETE (this record, §4–§10).
2. **Independent constitutional audit** — COMPLETE (independent Constitutional Review of the `b67a3cc` changes; verdict B — RATIFIABLE EXTENSION).
3. **Documentation approval** — COMPLETE (owner approval, 2026-08-12); restated boundary applied to `docs/PHASE7_FREEZE_APPROVED.md`, `docs/ARCHITECTURE.md`, `docs/CONSTITUTION_v1.0.md`, `docs/ROADMAP.md`, `docs/CHANGELOG.md`.
4. **Permanent freeze update** — COMPLETE: AMEND-1 recorded in the Phase 7 permanent freeze record and the Constitution v1.0 amendment register.

---

*Record prepared pursuant to Constitution v1.0 §8. Read-only governance task; no source code was modified by this record.*
