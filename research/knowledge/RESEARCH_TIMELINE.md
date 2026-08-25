# QuantForge Research Timeline

This timeline is organized by scientific progression rather than file dates.

## 1. Initial behavioral mean-reversion hypothesis

Research began with the proposition that unusually deep short-term displacement might reverse asymmetrically. The early factor set was z-score depth, momentum exhaustion, ATR/volatility and session timing.

**Knowledge retained:** extreme displacement is the candidate event, not a standalone trading rule.

## 2. Factor isolation and confluence

Separate studies examined depth, volatility, momentum and time-of-day, then combined them. The journals report that deeper extremes, high volatility, panic momentum and favorable sessions improved selected outcomes while reducing frequency.

**Scientific transition:** from indicator conditions to a behavioral-dislocation hypothesis.

## 3. Exit architecture experiments

Fixed, ATR-based, trailing, breakeven, partial and time-based exit concepts were evaluated. Quick snap/adaptive exits were retained; trailing/runners were de-emphasized.

**Scientific transition:** the edge was characterized as a fast response, not a trend-capture system.

## 4. Virtual signal architecture

The project separated observation of a panic condition from permission to enter. A virtual candidate had to prove recovery before becoming a real entry.

**Scientific transition:** fewer trades in exchange for quality control.

## 5. Recoil discovery

Forensic work (`entry_forensics.py`, `tick_entry_forensics.py`, `recoil_profile_analysis.csv`) focused on what happens immediately after the event. Strong winners show positive early recoil; scratch events do not.

**Scientific transition:** recoil became an observable confirmation variable.

## 6. Persistence discovery

Recoil alone was found insufficient. The research added a requirement that price hold after recovery. Expansion outputs retain separate recoil and persistence failure counts.

**Scientific transition:** two-stage confirmation: recoil, then stabilization.

## 7. Controlled recovery, basket and MAE/MFE forensics

Scripts reconstructed EA trades, grouped baskets/clusters, examined spacing, depth, lot progression, MAE/MFE and catastrophic clusters. This exposed concentration/tail-risk properties alongside high average cluster profitability.

**Scientific transition:** distinction between behavioral edge and recovery-mechanics risk.

## 8. Regime and failure-condition research

Regime classifier/matrix work tested volatility, trend persistence and adverse environments. It preserved the idea that degradation is identifiable, but retained subgroup evidence is too small for a deployable rule.

**Scientific transition:** from “does it work?” to “where does it fail?”

## 9. Robustness expansion and execution friction

Rules were loosened to test scale sensitivity, then stressed with entry/exit delays, wider spread, slippage and full-chaos conditions. The archived scenarios remain positive with PF 6.31–13.31 and drawdown from -3.00 to -4.57.

**Scientific transition:** reduced concern that the result depends only on ideal execution or one narrow parameter point.

## 10. Walk-forward and temporal checks

Yearly and walk-forward outputs were produced. Later years are positive; early-year data is sparse and mixed. This qualification belongs permanently alongside the stronger 2025–2026 results.

**Scientific transition:** evidence shifted from in-sample discovery to temporal challenge.

## 11. Monte Carlo validation

Synthetic and real-trade Monte Carlo variants reshuffled outcomes and added modeled skipped trades/slippage. Both distributions are favorable but conditional on the originating trade stream.

**Scientific transition:** sequence-risk challenge, not proof of live execution quality.

## 12. Cross-market universality

The consolidated journal reports transfer beyond Gold: EURUSD 329 trades/PF about 4.5, BTC 2,665/PF about 6.0, and preliminary NASDAQ 14/PF 2.37. The hypothesis became that markets differ in normalization speed more than in the existence of the behavioral effect.

**Scientific transition:** from instrument-specific strategy to universal behavioral framework.

## 13. Current QuantForge framework

The current framework preserves the pipeline implied by the research: validated data → market characterization → adaptive strategy → signal → risk → execution. Its outstanding scientific work is to operationalize the virtual-signal/recoil/persistence state machine, resolve recovery tail risk, and collect live forward evidence.

## 14. Canonical event studies and economic closure

QuantForge-internal canonical studies operationalized the hypothesis on the repository's own M1 data with pre-registered protocols, dependence-aware inference, walk-forward, cross-market and cost-aware checks (`output/event_study_v1/`, `output/event_study_v2/`, `output/event_study_v3/`, `output/xagusd_cost_viability_v1/`). V1 found no robust out-of-sample cross-market effect; V2 isolated a coherent XAGUSD down-displacement lead; V3 confirmed it as a narrow, direction-specific, threshold-stable statistical asymmetry but failed the promotion gates; the cost study then showed observed tick-level bid/ask spreads (median round-trip ≈ 9.1 bp vs gross ≈ 10.9 bp/2h; P90 11.4 bp) consume essentially the entire effect. **The Mean-Reversion research line is formally CLOSED as economically non-viable — see DISC-021.**

## Timeline conclusion

The surviving corpus supports a coherent progression: **mean reversion → volatility/panic confluence → virtual candidate → recoil → persistence → quick exit → robustness → cross-market hypothesis → execution validation need.** The next scientific milestone is not more indicator invention; it is reproducible, live-aware validation of this already identified behavior.

**Update (2026-08):** the canonical event studies (V1–V3) and the XAGUSD cost viability study closed the Mean-Reversion line as **economically non-viable** under observed transaction costs (DISC-021). The next milestone is **next research hypothesis selection**, not further Mean-Reversion work; no V4 and no Mean-Reversion detector implementation are planned.

## 15. TSMOM 12/1 line: V1 inconclusive → V2 drift-controlled → cross-era replication failure → closure

- **TSMOM V1 executed** (5-market contemporary panel, 219 assessments): scientific **INCONCLUSIVE** / economic **NOT CONFIRMED** — F1 absolute-return CI included zero and the formal NC2 (time-shifted signal) was contaminated by signal persistence / drift, so positive point estimates could not be separated from unconditional market drift.
- **TSMOM V2 drift-controlled** (28-market validated historical HPD panel, common window 1987-01-13 → 2002-08-30, 175 position months, 4,900 market-months): the same-universe all-long benchmark explicitly isolates the signal contribution via incremental `ΔΠ = Π_tsmom − Π_long`.
- **Historical incremental effect observed:** F1 `ΔΠ` ≈ **+0.67%/month**, 95% CI lower bound positive, Holm-adjusted p ≈ 0.038; broad across markets and asset classes; all three negative-control families clean.
- **Contemporary replication FAILED:** 2021–2026 panel (5 markets, T = 54) `ΔΠ` ≈ **−1.10%/month** — direction opposite the historical panel; the all-long drift benchmark was strongly positive.
- **Promotion:** 7 of 8 frozen conditions pass; **Condition 8 (contemporary directional consistency) FAILS** → **NOT PROMOTABLE / TSMOM REMAINS UNRESOLVED**; scientific classification **PARTIALLY REPRODUCED** (see DISC-022).
- **Candidate CLOSED.** TEST consumed exactly once; no rerun; no methodology changed after results.
- **No detector / runtime promotion:** no TSMOM detector, no BOE semantics, no runtime parameters, no Assembly/Deployment/StrategyManifest changes.
- The closure does **not** generalise to "trend following does not work" — external AQR/MOP and HOP literature remains historical context and is not disproven. Only the QuantForge fixed 12/1 candidate is closed.

## Timeline conclusion (updated)

The surviving corpus records **two closed research lines** — Mean Reversion (economically non-viable under observed costs, DISC-021) and the fixed 12/1 TSMOM candidate (no stable incremental edge above drift across eras, DISC-022) — plus the V2 methodological advance (drift-controlled incremental identification with dependence-aware inference) and, subsequently, the H01 volatility-response program (H01 v1.1 invalid inference → v1.2 corrected null construction → the US-anchored H01 Equity V1 replication, DISC-023). The H01 Equity Track A result is preserved but the track is now **CLOSED — EVIDENCE-LIMITED / DATA-ACCESS TERMINATION** (see §19).

## 16. H01 volatility-response program: broad H01 closed → H01 Equity V1 executed and adjudicated (2026-08-16)

- **H01 broad universal formulation: NOT ESTABLISHED / closed in that form.** H01 v1.1's registered inference was invalid (D_obs-centered bootstrap p ≈ 1 by construction); the v1.2 correction (null-imposing recentered bootstrap, protocol v1.2.0) was executed and independently adjudicated — the universal cross-asset claim was not supported; COMMODITIES_OTHER produced a formal contradiction of its registered inverse prior; the equity observations (historical `sp`, contemporary `USATECHIDXUSD`) showed classic direction but were EVIDENCE-LIMITED (one evaluable market per layer). H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / UNADJUDICATED.
- **Track A (equity) earned screening** → scope decision (broader data required) → data-source audit → data acquisition (composite: HPD `sp` + FRED cash indices; licensing PENDING/NOT-SENT) → outcome-blind definition lock (US-anchored, two exposures) → pre-registration (protocol v1.1.0, audited PASS after three precision corrections) → **H01 Equity V1 EXECUTED** exactly once (seed 20260816, B = 10,000, L = 11, single invocation, serial; protocol SHA-256 `a97cd0e2…`; artifact set under `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/`).
- **Adjudicated classification (independent, read-only):** EQBROAD_L1 = **EVIDENCE-LIMITED** (single historical market); EQBROAD_L2 = **SUPPORT** (SP500 + DJIA); EQTECH_L1 = **SUPPORT**; EQTECH_L2 = **SUPPORT**; 3 SUPPORT / 1 EVIDENCE-LIMITED / 0 CONTRADICTION / 0 INCONCLUSIVE; **EQTECH strong cross-era replication = TRUE** (same US-tech exposure, two eras, all p_Holm = 0.0004).
- **Strongest surviving scientific claim:** classic volatility-response asymmetry is strongly supported in the tested US-tech exposure and replicates across two eras.
- **Economic translation (Q1 / 11-day):** Executed and adjudicated (2026-08-23). The translation failed the mandatory dual-era gate. Historical era: FAIL (Δ = -0.00143921). Contemporary era: PASS (Δ = +0.00077702). Overall: ECONOMIC FAILURE.
- **Track A status: ECONOMIC TRANSLATION CLOSED — ECONOMIC FAILURE (DISC-023).** The historical/contemporary divergence is preserved. The failure of the economic translation does not invalidate the H01 scientific finding. 
- **Firewall:** no rerun of H01 Equity V1; no universe change without amendment; no secondary rescue; no threshold or horizon search; no post-hoc market selection; no trading strategy; no BOE/runtime transfer.
- **Key artifacts:** `output/research_discovery/H01_EQUITY_V1_SCIENTIFIC_ADJUDICATION.md` (scientific adjudication), `output/research_discovery/H01_ECONOMIC_V1_EXEC_04` (economic output), protocol, definition lock, scope decision, screening, data-source audit, data acquisition report (DISC-023).

## 19. H01 Equity Track A closure — ECONOMIC FAILURE (2026-08-23)

- **Closure decision:** H01 Equity Track A is **CLOSED — ECONOMIC FAILURE (DISC-023)**.
- **Closure reason:** The registered Q1/11-day economic translation failed the mandatory dual-era stability gate. It produced negative returns across all market segments in the Historical era (1982–2002) and uniformly positive returns in the Contemporary era (2016–2026). The registered rule is not a stable cross-era economic edge.
- **This is NOT a scientific contradiction.** The classic volatility-response asymmetry remains scientifically supported. The economic failure does not invalidate the H01 scientific finding. 
- **Preserved scientific findings:** US-tech strong cross-era replication = TRUE. Classic volatility-response asymmetry is strongly supported in the tested US-tech exposure and replicates across two eras.
- **What is NOT established:** broad-US historical generalization; universal US-equity generalization; international generalization; economic viability; tradeability; strategy profitability.
- **Firewall:** no reopening of H01 Equity Track A; no reinterpretation of the scientific SUPPORT results; no rescue translation; no contemporary-only strategy; no threshold search; no horizon search; no trading strategy from H01; no BOE semantics; no reopening of any closed line. Next task: **TRADEABLE EDGE DISCOVERY SCREENING**.

## 17. Session-Anchored Range Expansion (USATECHIDXUSD): Contradicted and Closed

- **Definition & Audits**: Candidate screened for behavioral mechanism (extreme pre-session range compression preceding cash-session expansion). Outcome-blind definition lock and deterministic pre-registered protocol (v1.1.3) passed rigorous independent read-only adversarial audits.
- **Controlled Execution**: Executed exactly once. Deterministic 63-day rolling 25th percentile classifier applied. Stationary block bootstrap (B=10,000, L=10) completed over 873 calendar days of M1 data.
- **Scientific Adjudication**: Independent read-only adjudication confirmed execution integrity. The result was **CONTRADICTED**. Observed $\Delta M = -0.004367$, with a strictly negative 95% CI `[-0.005533, -0.002754]`. Pre-session compression was associated with significantly LOWER subsequent normalized cash-session range than the registered control group.
- **Candidate CLOSED**: The behavioral hypothesis failed the primary test. No further tuning, hypothesis inversion, K-means application, or trading strategy rescue is authorized.
- **Next Stage**: Project returned to **Tradeable Edge Discovery**. The goal remains discovering a defensible trading edge, and failed candidates are closed quickly to maintain that focus.

## 18. Liquidity Sweep / Reversal: behavioral discovery supported → minimal translation economically non-viable → closure (2026-08-17)

- **Discovery origin:** XAUUSD (candidate: deterministic sweep of a prior Asian-session extreme → wick rejection → micro-structural reversal confirmation → larger directional excursion than the rejected-sweep control group). Outcome-blind definition screening → cross-market pre-registration (protocol v1.2.0 after precision clarification + amendment) → final independent clearance PASS → controlled multi-market execution (B = 10,000, L = 10, seed 20260817; stationary day-cluster bootstrap; null-imposing recentered p; Holm family = eligible markets).
- **Behavioral adjudication:** SUPPORT in all four evaluable markets — XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD (all p_Holm = 3.9996e-04; ΔM_obs > 0; CIs far from zero; three economically distinct mechanisms: precious metals, equity-index CFD, crypto). EURUSD **DATA-LIMITED / NOT ADJUDICATED** (16.96% invalid-day fraction > 10% gate; no inference). Cross-market level: Level 2 established (precious metals) + preliminary Level 3 (three distinct mechanisms); Level 4 (universal) NOT established.
- **Economic translation (single registered baseline, no tuning):** confirmation-close entry, reversal-direction trade, structural sweep-extreme stop, 120-minute-close exit, fixed notional, observed MT5 bid/ask spreads (exact-minute ≥ 98.3%). **ECONOMICALLY NON-VIABLE in all four markets, gross-negative BEFORE costs** (median gross: XAUUSD −5.3, XAGUSD −11.6, USATECHIDXUSD −5.0, BTCUSD −11.8 bp; win rates 19–26%; stop-out 70–80%; negative in every year and both halves of every market). Failure mechanism: **TRANSLATION FAILURE** — the validated excursion is anchored at the swept Asian level; the confirmation-close entry (4.7–13.2 bp beyond the level) and the structural stop / horizon-close exit cannot capture it. Costs secondary; behavioral failure not established.
- **Governance adjudication:** under the strict alternative-selection rule, no alternative translation (limit entry at the Asian level, next-bar-open entry, Asian opposite-boundary target, trailing exit) has a pre-existing justification derived from the frozen behavioral object → **no new economic protocol authorized** → research line **CLOSED** (DISC-025). The behavioral discovery is preserved as a permanent record; the candidate does not become a bot.
- **Firewall:** no reopening of the economic translation; no retesting of unused alternatives; no inversion/rescue of the hypothesis; no EA from the closed translation; no market selection; no ML/K-means rescue; no merging with closed lines (DISC-021/022/023/024); EURUSD excluded until its data-quality operationalization is separately resolved.
- **Key artifacts:** `XAUUSD_LIQUIDITY_SWEEP_REVERSAL_SCIENTIFIC_ADJUDICATION_V1.md`, `LIQUIDITY_SWEEP_STRATEGY_ECONOMIC_TRANSLATION_V1.md`, `LIQUIDITY_SWEEP_POST_ECONOMIC_GOVERNANCE_ADJUDICATION_V1.md`, `LIQUIDITY_SWEEP_RESEARCH_LINE_CLOSURE_GOVERNANCE_RECORD_V1.md`, event CSVs + scientific report under `XAUUSD_LIQUIDITY_SWEEP_REVERSAL/`, protocol v1.2.0 (DISC-025).

## Timeline conclusion (updated)

The surviving corpus now records **six closed research lines** — Mean Reversion (DISC-021), fixed 12/1 TSMOM (DISC-022), Session-Anchored Range Expansion (DISC-024), Liquidity Sweep / Reversal (DISC-025), **H01 Equity Track A (DISC-023, economic failure)**, and **Opening Range Breakout (ORD / DISC-026) XAGUSD economic translation (economic failure)**. The H01 broad universal formulation is closed in that form.

## 20. Opening Range Breakout (ORD / DISC-026): Scientifically Supported / Economic Translation Closed

- **Scientific Execution and Adjudication:** Executed successfully. 3/3 evaluable registered markets passed the Holm-adjusted threshold. Classification: SCIENTIFICALLY SUPPORTED.
- **Economic Protocol and Chronological Sequence:**
  - M-ORD-ECO-01 specification PASS;
  - M-ORD-ECO-02 converter implementation;
  - M-ORD-ECO-03 converter audit;
  - M-ORD-ECO-04 production Parquet conversion;
  - post-conversion integrity PASS;
  - M-ORD-ECO-05 Stage-1 adapter/preparation;
  - M-ORD-ECO-06 Stage-1 production execution;
  - M-ORD-ECO-07 Stage-1 output audit;
  - M-ORD-ECO-08 Stage-2 economic execution;
  - M-ORD-ECO-09 independent economic adjudication;
  - final XAGUSD economic closure.
- **Economic Adjudication:** The execution (ORD_STAGE2_XAGUSD_EXEC_01) was strictly negative. Median net -12.404 bp, Win Rate 9.1%. Protocol gates uniformly failed.
- **Candidate CLOSED:** The registered XAGUSD economic translation is ECONOMICALLY NON-VIABLE and CLOSED. The scientific finding remains SUPPORTED. No rerun or rescue is authorized.
- **Next Stage:** Project returned to **TRADEABLE EDGE DISCOVERY SCREENING**.

## 21. Research Factory V2: Economic-First Discovery Pipeline

- **Program-Level Audit:** After the closure of six research lines yielding zero positive economic results despite strong scientific governance, an independent read-only program-level audit (`QUANTFORGE_PROGRAM_LEVEL_RESEARCH_ARCHITECTURE_AUDIT_V1.md`) was conducted.
- **Key Finding:** The project was operating as an excellent scientific laboratory but an inefficient discovery machine, repeatedly applying expensive engineering infrastructure to candidates whose gross signals were structurally incapable of surviving retail friction.
- **Governance Amendment:** The project formally adopted the **Economic-First Discovery Pipeline** (`QUANTFORGE_RESEARCH_FACTORY_V2.md`).
- **Core Changes:** 
  1. Mandatory **Economic Plausibility Gate (G1)** before scientific definition lock.
  2. Mandatory **Cheap Empirical Pilot (G2)** before expensive infrastructure allocation.
  3. Strict diversification requirement across mechanism families during candidate generation.
- **Status:** QuantForge now operates as an Economic-First Tradeable-Edge Discovery Factory. Future candidate screening resumes under this doctrine.

## 22. First G1 Screening Cycle: Invalidated / Contract Hardened (2026-08-25)

- **Execution:** The first formal G1 Economic Plausibility Screen (`RESEARCH_FACTORY_V2_G1_SCREEN_20260825.md`) was executed on four candidates (CAND-G0-001 to CAND-G0-004).
- **Audit & Invalidation:** An independent integrity audit found systemic methodological failures across all four candidates. The implementation calculated Maximum Favorable Excursion (MFE) instead of deterministic executable exit, falsely captured pre-entry breakout excursion, and employed undocumented proxy substitution and down-sampling. The execution was formally invalidated (`RESEARCH_FACTORY_V2_G1_INVALIDITY_20260825.md`).
- **Doctrine Update:** The Research Factory V2 doctrine was hardened. The G1 executable-capture contract now requires explicit deterministic exit, post-entry-only measurement, exact candidate-definition adherence, and explicit prohibition of MFE/proxy/down-sampling substitutions.
- **Candidate Status:** CAND-G0-001 through CAND-G0-004 are CLOSED for this screening cycle (G1 INVALID). No G2 execution occurred.
- **Next Stage:** Project returned to **G0 CANDIDATE GENERATION**.

## 23. Research Factory refined (2026-08-25)

- **Methodological Refinement:** Research Factory refined around conditional market behavior, mathematical expectancy, and opportunity-integrity protection after CAND-010 event-state duplication failure. The primary research objective is to estimate conditional post-event behavior and determine whether that conditional distribution produces positive mathematical expectancy after executable costs.

## 24. G0 Candidate Generation V5 (2026-08-25)

- **Execution:** Executed the fifth G0 candidate generation cycle under the new Conditional Market Behavior and Opportunity Integrity principles (`TRADEABLE_EDGE_DISCOVERY_SCREENING_V5.md`).
- **Promoted Candidates:** CAND-G0-012 (Trend-Pullback Re-Acceleration) and CAND-G0-013 (Macro-Shock Volatility Reset Continuation). Both explicitly define re-arm mechanisms and conditional KPIs.
- **Rejected Candidates:** CAND-G0-014 killed as a closed-line rescue attempt.
- **Next Stage:** **G1 ECONOMIC PLAUSIBILITY SCREEN** for CAND-012 and CAND-013.

## 25. G1 Economic Plausibility Screen V5 (2026-08-25)

- **Execution:** Executed deterministic G1 extraction for CAND-G0-012 and CAND-G0-013 (`RESEARCH_FACTORY_V2_G1_SCREEN_20260825_V5.md`).
- **Opportunity Integrity Confirmed:** Sequential state machine and 24-hour lockouts successfully prevented overlapping event cascades (suppressing 4,820 duplicate touches for CAND-012 and 212 overlapping lockouts for CAND-013).
- **Result (CAND-G0-012):** INSUFFICIENT. The conditional post-event behavior produced negative expectancy across both low-volatility and high-volatility states.
- **Result (CAND-G0-013):** INSUFFICIENT. The shock-reset condition proved extremely rare (67 valid opportunities in 5 years). The most populated liquidity session state (NY) generated strictly negative expectancy.
- **Next Stage:** **G0 CANDIDATE GENERATION** (Return to discovery).

## 26. Closure of V5 G1 Screening Cycle (2026-08-25)

- **Record:** Research Factory V2 V5 G1 screening completed; CAND-012 and CAND-013 failed economic plausibility; no G2 execution; factory returned to G0.
