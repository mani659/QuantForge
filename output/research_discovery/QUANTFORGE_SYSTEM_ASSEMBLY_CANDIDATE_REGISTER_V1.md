# QUANTFORGE — SYSTEM ASSEMBLY CANDIDATE REGISTER V1
# GOVERNANCE DESIGN
# DATE: 2026-08-26

## 1. Purpose
To establish the formal governance register for historical research artifacts that may eventually participate in a QuantForge Strategy System. This framework dictates how individual validated components are governed prior to and during integration into a unified executable architecture.

## 2. System Assembly Definition
**SYSTEM ASSEMBLY** is defined as the formal process of combining independently qualified research artifacts into a single executable strategy architecture. System assembly is **NOT** a mechanism for rescuing failed research by combining it.

## 3. Component Qualification
An artifact must independently demonstrate the following minimum evidence before entering the System Assembly Candidate Register:
- Formally defined mechanism;
- Executable capture;
- Deterministic exit;
- No unresolved look-ahead;
- No unresolved implementation defects;
- Credible historical evidence;
- Economically meaningful per-event behavior;
- Documented intended component role.

High standalone frequency is **NOT** required for component qualification.

## 4. Component Roles
Components must be assigned a role based on evidence:
- **EVENT OPPORTUNIST:** Rare but high-value event.
- **SESSION COMPONENT:** Operates in a specific session/time window.
- **REGIME SPECIALIST:** Relevant only in a particular market regime.
- **CROSS-MARKET COMPONENT:** Responds to a separate market/information mechanism.
- **DIVERSIFIER:** Potentially valuable because its return profile is behaviorally distinct from another component.
- **CORE COMPONENT:** Higher-frequency component capable of forming a larger share of system opportunity flow.

Roles must not be assigned without supporting evidence.

## 5. Opportunity Union
**SYSTEM OPPORTUNITY FREQUENCY** is the frequency of unique executable opportunities produced by the **UNION** of qualified components. It is not a simple addition (Component A + Component B) because components may overlap, trigger simultaneously, be mutually exclusive, or conflict directionally.

## 6. Overlap Policy
System assembly must enforce a deterministic overlap policy defining how the system handles:
- Simultaneous signals;
- Same-instrument signals;
- Opposing signals;
- Same-event signals;
- Different-market simultaneous signals.
Priority must be deterministic and **MUST NOT** be optimized after seeing returns.

## 7. Capital/Risk Requirements
The assembled system must predefine its risk model before validation, including:
- Capital allocation;
- Maximum concurrent positions;
- Per-component risk;
- Aggregate risk cap;
- Correlation/interaction handling;
- Drawdown controls.

## 8. Cost Requirements
System assembly must account for systemic transaction costs, including:
- Component-specific friction;
- Turnover;
- Simultaneous trades;
- Duplicated exposure;
- Portfolio-level transaction cost.
Transaction costs must not be simply averaged across components.

## 9. Diversification
System assembly requires **MECHANISM DIVERSITY**, not merely parameter diversity. There must be evidence that components represent genuinely different underlying mechanisms (e.g., session/inventory behavior should not be combined with another artifact that is simply a parameter variant of the same behavior).

## 10. Assembly Firewalls
System composition must be defined before system-level validation. The following are strictly prohibited:
- Cherry-picking only profitable components;
- Dropping weak components after seeing combined results;
- Dynamic component switching based on historical performance;
- Arbitrary weighting;
- Post-hoc correlation selection;
- Optimization of component inclusion.

## 11. Future S0–S7 Stages
System Assembly will follow a governed sequence:
- **S0 — Component Register:** Identify independently qualified artifacts.
- **S1 — System Architecture:** Define how components interact.
- **S2 — Opportunity Union:** Determine combined event stream and overlap.
- **S3 — Capital/Risk Specification:** Freeze portfolio/risk rules.
- **S4 — System Historical Validation:** Test the preregistered system.
- **S5 — System Economic Validation:** Validate realistic costs and drawdown.
- **S6 — System Forward Validation:** Observe the complete assembled system.
- **S7 — Bot Construction:** Only after system-level evidence warrants implementation.

## 12. Current Component Register

| Field | Description | CAND-024 |
|---|---|---|
| Component ID | Original research object | CAND-024 (Friday De-Risking) |
| Mechanism | Mechanism family | Friday Afternoon Positional De-Risking |
| Scientific Status | Current scientific state | Credible historical evidence |
| Economic Status | Current economic state | Strong positive per-event economics |
| Frequency | Standalone frequency | ~4.55 opportunities/year |
| Intended Role | Core/event/session/etc. | EVENT OPPORTUNIST / SESSION COMPONENT |
| Markets | Applicable instruments | USATECHIDXUSD |
| Holding Period | Typical lifecycle | Session |
| Overlap Risk | Potential interaction | Time-constrained |
| Cost Profile | Transaction cost characteristics | High expectancy relative to friction |
| Qualification Basis | Why retained | Strong per-event economics, failed G1 solely on standalone frequency |
| Governance Status | Retained / Qualified / Closed | **COMPONENT-CANDIDATE / RETAINED** |

### Additional Artifact Status
- **CAND-025:** RETAINED BUT UNQUALIFIED — THIN ECONOMICS / HIGH FRAGILITY. Not included as an approved component.

## 13. Closed-Artifact Protection
All permanently closed artifacts remain closed. No system assembly may use a scientifically contradicted or economically negative artifact (at the artifact level) as a component.

## 14. CAND-015 Protection
CAND-015 remains **7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED**. Its incomplete results must not be inspected or placed into the system assembly register until its forward validation and required governance gates are formally completed. Historical qualification and forward qualification are distinct.

## 15. Governance Integrity
No rerun, combination, backtest, or weight optimization was performed. This document establishes governance design only.
