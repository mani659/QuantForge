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

## 27. CAND-015 V6 G1-G5 Validation (2026-08-25)

- **Record:** CAND-015 completed G5 historical production-style replay.
- **Record:** 2026-08-25 — CAND-015 G6 replay harness independently validated; 10/10 behavioral tests passed; historical signal parity passed; true forward validation remains blocked pending data-source authorization.

## 28. Parallel Forward Validation and Discovery

- **Record:** CAND-015 7-day forward validation continues as a protected track while the Research Factory V2 simultaneously resumes G0 candidate discovery.

## 29. G0 Candidate Generation V7 (2026-08-26)

- **Record:** V7 G0 candidate generation completed in parallel with protected CAND-015 forward observation.

## 30. G1 Economic Plausibility Screen V7 (2026-08-26)

- **Record:** V7 G1 Economic Plausibility Screen completed. Original CAND-018 invalidated (leakage); Corrected CAND-018 Final Adjudication: RETURN TO G0 (Structurally negative expectancy). CAND-019 blocked. CAND-020 killed.

## 31. G0 Candidate Generation V8 (2026-08-26)

- **Record:** V8 G0 candidate generation completed. V8 focuses on pre-entry state conditioning. Promoted: CAND-G0-021, CAND-G0-022, CAND-G0-023, CAND-G0-024.

## 32. G1 Economic Plausibility Screen V8 (2026-08-26)

- **Record:** V8 G1 Economic Plausibility Screen completed. CAND-021 Final Adjudication: G2 READY. CAND-022: BLOCKED. CAND-023: INSUFFICIENT. CAND-024: INSUFFICIENT.

## 33. G2 Cheap Empirical Pilot (2026-08-26)

- **Record:** CAND-021 G2 Cheap Empirical Pilot completed. Effect validated in chronological holdout. Final Adjudication: G3 READY (Scientific effect empirically validated).

## 34. G3 Scientific Validation (2026-08-26)

- **Record:** CAND-021 G3 Scientific Validation completed. Formal permutation test yielded p=0.90. Scientific Classification: CONTRADICTED. CAND-021 G3 CONTRADICTED; line closed; no G4.

## 35. G0 Candidate Generation V9 (2026-08-26)

- **Record:** V9 G0 candidate generation completed. V9 focuses on mechanistic market-structure events without arbitrary condition filters. Promoted: CAND-G0-025, CAND-G0-026, CAND-G0-027.

## 36. G1 Economic Plausibility Screen V9 (2026-08-26)

- **Record:** V9 G1 Economic Plausibility Screen completed. CAND-025: PASS — MARGINAL. CAND-026: INSUFFICIENT. CAND-027: INSUFFICIENT.

## 37. G1 Final Adjudication (2026-08-26)

- **Record:** CAND-025 G1 independently adjudicated. Verdict: HOLD. The mechanism is observable, but the unhedged left tail creates a standard deviation (~50 pts) too massive to pilot the thin +1.25 mean net expectancy. Line closed; returned to G0.

## 38. Governance Amendment — Artifacts vs Systems (2026-08-26)

- **Record:** Formally distinguished between Research Artifacts and Strategy Systems. Low frequency is no longer an automatic kill condition for scientifically valid artifacts. Created COMPONENT-CANDIDATE classification for artifacts banked for future SYSTEM ASSEMBLY. CAND-024 and CAND-025 are considered COMPONENT-CANDIDATES.

## 39. Historical Artifact Reintroduction Audit (2026-08-26)

- **Record:** Retrospective audit of historical lines (DISC-021-026, CAND-018-027) completed. CAND-024 was designated COMPONENT-ELIGIBLE and retained for future SYSTEM ASSEMBLY. CAND-025 was designated COMPONENT-CANDIDATE (CONDITIONAL). No failed or scientifically contradicted artifacts were rescued. All economically non-viable and scientifically invalid lines remain permanently closed.

## 40. System Assembly Candidate Register (2026-08-26)

- **Record:** Established the System Assembly Candidate Register to govern the formal integration of independently qualified artifacts into deployable architectures. CAND-024 is formally retained as a COMPONENT-CANDIDATE / EVENT OPPORTUNIST. Its standalone status remains CLOSED. CAND-025 is retained but UNQUALIFIED.

## 41. G0 Candidate Generation V10 (2026-08-26)

- **Record:** V10 G0 candidate-generation cycle completed. The cycle focused on discovering independent behavioral artifacts across distinct mechanistic families (Liquidity, Dispersion, Value Area Structure, Cross-Market Volatility) for potential future system assembly. Promoted candidates: CAND-G0-028, CAND-G0-029, CAND-G0-030, CAND-G0-031.

## 42. G1 Economic Plausibility Screen V10 (2026-08-26)

- **Record:** V10 G1 completed. CAND-028, CAND-029, and CAND-031 were blocked due to unavailable data or proxy requirements violating V2 doctrine. CAND-030 was evaluable but exhibited a structurally fatal left tail (positive median gross but negative mean net). Verdict for all V10 candidates: INSUFFICIENT / BLOCKED. G2 NOT EXECUTED.

## 43. G1 Closure V10 (2026-08-26)

- **Record:** V10 G1 cycle formally closed. Zero candidates promoted to G2. Emphasized two strict governance lessons: 1) High win rate and positive median do NOT establish positive economic expectancy; 2) Missing data must produce BLOCKED, not proxy substitution. Next G0 cycle must prioritize mechanisms with naturally asymmetric positive payoffs.

## 44. G0 Candidate Generation V11 (2026-08-26)

- **Record:** V11 G0 candidate-generation cycle completed. Focused exclusively on discovering mechanisms whose economic structure naturally supports positive expectancy (asymmetric payoff, bounded risk) rather than mere high win rates. Promoted 3 new candidates spanning Breakout Continuation, Forced Flow, and Cross-Market Repricing families: CAND-G0-032, CAND-G0-033, CAND-G0-034.

## 45. G1 Economic Plausibility Screen V11 (2026-08-26)

- **Record:** V11 G1 completed. CAND-032 (NY Open Structural Momentum) passed clearly with broad-based positive expectancy (+12.02 points mean net, N=257). CAND-033 captured the flow phenomenon but lacked magnitude to beat friction. CAND-034 failed due to a severe unhedged left tail (positive median but negative mean net). CAND-032 promoted to G2.

## 46. CAND-032 Final G1 Adjudication (2026-08-26)

- **Record:** Final independent adjudication of CAND-032 G1 results completed. Validated strict absence of look-ahead bias and verified that the strong expected value (+12.02 points net) was broad-based across the mid-distribution, not dependent on outliers. G1 verdict confirmed: G2 READY.

## 47. G2 Cheap Empirical Pilot CAND-032 (2026-08-26)

- **Record:** G2 executed for CAND-032 (NY Open Structural Momentum). The mechanism reproduced strongly in the chronological holdout (+10.61 points mean net, median +42.60) and proved robust against 2x friction stress (+8.61 points mean net). It demonstrated stable temporal behavior across multiple years (2023-2026) without reliance on exceptional tail winners. Verdict: PROMOTE TO G3.

## 48. G3 Scientific Validation CAND-032 (2026-08-26)

- **Record:** G3 executed for CAND-032. Despite strong economic performance in G1/G2, the mechanism failed the scientific standard. The massive unhedged left-tail variance (worst trade -1134 points) caused a direction-sign permutation placebo test to yield an extremely wide null 95% CI ([-24.79, +20.94]). The observed effect (+12.02) was statistically indistinguishable from chance (p=0.1133). Verdict: INCONCLUSIVE. Pipeline blocked. Return to G0.

## 49. CAND-032 G3 Closure (2026-08-26)

- **Record:** CAND-032 research line formally closed (G3 INCONCLUSIVE). G4 blocked. No rescue authorized. This establishes the critical distinction between out-of-sample descriptive economics (G2) and scientific mechanism isolation (G3). Return to G0 Candidate Generation.

## 50. G0 Candidate Generation V12 (2026-08-26)

- **Record:** V12 G0 candidate-generation cycle completed. Focused exclusively on mechanisms with pre-declared, testable counterfactuals to ensure scientific adjudicability. Promoted 3 new candidates: CAND-G0-035 (Month-End Imbalance Acceleration), CAND-G0-036 (Structural PDH Pre-Market Acceptance), and CAND-G0-037 (Cross-Index Tech Leadership Divergence). G1 pending.

## 51. G1 Economic Plausibility Screen V12 (2026-08-26)

- **Record:** V12 G1 completed. CAND-035 (Month-End Imbalance) showed massive per-event economics (+62.36 mean net) and a flawless counterfactual validation, but low opportunity frequency limits it to COMPONENT-CANDIDATE (Event Opportunist). CAND-036 (Structural PDH) yielded negative expectancy (-16.15), contradicted by its unverified gap-up counterfactual (+13.95), and is INSUFFICIENT. CAND-037 (Tech Divergence) was BLOCKED due to missing USA500 data. Zero standalone G2 promotions.

## 52. G0 Candidate Generation V13 (2026-08-26)

- **Record:** V13 G0 candidate-generation cycle completed. Focused on diversifying the Component Register with low-frequency, structurally robust, positive-expectancy hypotheses. Promoted 3 new candidates: CAND-G0-038 (Mid-Day Counter-Trend Reload), CAND-G0-039 (Structural Gap-Fill Rejection), and CAND-G0-040 (Volatility Compression Expansion). G1 pending.

## 53. G1 Economic Plausibility Screen V13 (2026-08-26)

- **Record:** V13 G1 completed. CAND-038 (Mid-Day Reload) validated its counterfactual but had weak absolute economics (+4.69 mean net, -18.88 median net) entirely dependent on a single outlier, rendering it INSUFFICIENT. CAND-039 (Gap-Fill Rejection) yielded 0 events due to over-constrained parameters and is INSUFFICIENT. CAND-040 (Volatility Expansion) yielded negative expectancy (-18.99 mean net), contradicting the compression hypothesis, and is INSUFFICIENT. Zero standalone G2 promotions. Zero new Component-Candidates retained.

## 54. V13 G1 Closure (2026-08-26)

- **Record:** V13 G1 formally closed. Established key lessons: an outlier-dependent positive mean (CAND-038) is not evidence of a healthy artifact; zero-event frequency (CAND-039) indicates lack of opportunity, not necessarily a false mechanism; and causal mechanisms (CAND-040 dealer gamma) cannot be claimed without the observational data to test them. Returned to G0 Candidate Generation (V14) with a mandate to search for objective economic constraints.

## 55. G0 Candidate Generation V14 (2026-08-26)

- **Record:** V14 G0 candidate-generation cycle completed. Focused on Objective Economic Constraints instead of generic price patterns. Promoted 3 new candidates: CAND-G0-041 (Post-OPEX Unpinning Drift), CAND-G0-042 (Correlated Liquidity-Shock Reversion), and CAND-G0-043 (European-Close Liquidity Vacuum). G1 pending.

## 56. G1 Economic Plausibility Screen V14 (2026-08-26)

- **Record:** V14 G1 completed. CAND-041 (Post-OPEX Drift) is INSUFFICIENT due to extreme outlier dependence (+35 mean / -10 median). CAND-042 (Correlated Shock Reversion) produced massive structural economics (+63 mean / +228 median) but extremely low sample (N=5), earning COMPONENT-CANDIDATE (Event Opportunist) status rather than standalone G2 promotion. CAND-043 (Liquidity Vacuum) is INSUFFICIENT as it directly contradicted the expected mechanism. Zero standalone G2 promotions.

## 57. V14 G1 Closure & Component Governance Update (2026-08-26)

- **Record:** V14 G1 formally closed. Updated System Assembly governance to explicitly separate COMPONENT-CANDIDATE (interesting descriptive behavior, retained for future study) from QUALIFIED SYSTEM COMPONENT (scientifically validated). Retained CAND-042 under this new Component-Candidate doctrine. Established the lesson that a profitable treatment does not prove a mechanism if the counterfactual is also highly profitable. Next phase: G0 Candidate Generation (V15) focusing on mechanisms with economically constrained counterfactuals.

## 58. G0 Candidate Generation V15 (2026-08-26)

- **Record:** V15 G0 candidate-generation cycle completed. Focused strictly on counterfactual-discriminating mechanisms. Promoted 3 new candidates: CAND-G0-044 (Initial Balance Trap Liquidation), CAND-G0-045 (Safe-Haven Confirmed Risk-Off), and CAND-G0-046 (Opening Print Capitulation Pivot). G1 pending.

## 59. G1 Economic Plausibility Screen V15 (2026-08-26)

- **Record:** V15 G1 completed. All three candidates failed. CAND-044 (Trap Liquidation) and CAND-046 (Capitulation Pivot) produced explicitly negative expectancy. CAND-045 (Confirmed Risk-Off) produced positive expectancy but was severely outperformed by its unconfirmed counterfactual, contradicting the mechanism hypothesis. Validated the new research standard requiring explicit counterfactual benchmarking. Zero standalone G2 promotions.

## 60. V15 G1 Closure & Counterfactual Superiority Doctrine (2026-08-26)

- **Record:** V15 G1 formally closed. Zero new components retained. Established the "Counterfactual Superiority Rule": a highly profitable treatment does not qualify as a valid mechanism artifact if its registered counterfactual is materially more profitable. Mechanism value must be explicitly separated from absolute event economics. Next phase: G0 Candidate Generation (V16) focusing on mechanisms where the condition explicitly adds value relative to a very close counterfactual.

## 61. G0 Candidate Generation V16 (2026-08-27)

- **Record:** V16 G0 candidate-generation cycle completed. Focused strictly on objective economic constraints that change the economic distribution in a predictable way. Promoted 3 new candidates spanning Fixing-Window Liquidity Transfer, Sequential Macro-Release Dislocation, and Cross-Market Lead-Lag Asymmetry families: CAND-G0-047, CAND-G0-048, CAND-G0-049. G1 NOT EXECUTED.

## 62. G1 Economic Plausibility Screen V16 (2026-08-27)

- **Record:** V16 G1 completed. CAND-047 (Fixing-Window Liquidity Transfer) yielded negative expectancy (-43.62 bps mean net) and was outperformed by its counterfactual (-7.04 bps), rendering it INSUFFICIENT. CAND-048 (Sequential Macro-Release Dislocation) and CAND-049 (Cross-Market Lead-Lag Asymmetry) were both INSUFFICIENT due to their strictly defined mechanisms yielding zero events. Zero standalone G2 promotions.

## 63. V16 G1 Closure (2026-08-27)

- **Record:** V16 G1 formally closed. Zero new components retained. Demonstrated that overconstrained mechanism definitions (CAND-048, CAND-049) fail to provide sufficient opportunity frequency for empirical validation, while mechanisms claiming institutional necessity (CAND-047) can easily underperform simple unconstrained chop. Next action: Return to G0 Candidate Generation (V17).

## 64. G0 Candidate Generation V17 (2026-08-27)

- **Record:** V17 G0 candidate-generation cycle completed. Focused strictly on highly observable, mechanism-specific market behaviors where the causal variable itself is directly measurable. Promoted 3 new candidates: CAND-G0-050 (Cash-Session PDH Liquidity Sweep), CAND-G0-051 (Precious Metals Ratio Dislocation), and CAND-G0-052 (Lunch-Window Volatility Contraction Breakout). G1 NOT EXECUTED.

## 65. G1 Economic Plausibility Screen V17 (2026-08-27)

- **Record:** V17 G1 completed. CAND-050 (PDH Liquidity Sweep) produced +26.15 bps mean net but was outperformed by its counterfactual (+39.86 bps), meaning the mechanism actively degrades opportunity. CAND-051 (Ratio Dislocation) yielded zero frequency (N=1). CAND-052 (Lunch Contraction Breakout) passed the counterfactual gate but absolute economics were completely flat (+0.01 bps mean net). Zero standalone G2 promotions. Next action: Return to G0 Candidate Generation.

## 66. V17 G1 Closure (2026-08-27)

- **Record:** V17 G1 formally closed. Zero new components retained. Demonstrated that informational value (filtering chop) does not equal tradeable economic value (sufficient headroom). Next action: V18 G0 Candidate Generation.

## 67. G0 Candidate Generation V18 (2026-08-27)

- **Record:** V18 G0 candidate-generation cycle completed. Focused strictly on candidates demonstrating Counterfactual Superiority AND Economic Headroom AND Sufficient Frequency. Promoted 3 new candidates: CAND-G0-053 (Friday Cash-Close Settlement Reversion), CAND-G0-054 (Post-Shock Volatility Absorption), and CAND-G0-055 (Initial Balance False Breakout). G1 NOT EXECUTED.

## 68. G1 Economic Plausibility Screen V18 (2026-08-27)

- **Record:** V18 G1 completed. CAND-053 (Friday Settlement) was evidence-limited (N=3) with negative absolute economics. CAND-054 (Volatility Absorption) yielded zero frequency. CAND-055 (IB False Breakout) produced strong absolute economics (+17.93 bps) but was materially outperformed by its counterfactual (+23.65 bps), resulting in a Type 1 failure. Zero standalone G2 promotions. Next action: Return to G0 Candidate Generation.

## 69. V18 G1 Closure & Component Register Review (2026-08-27)

- **Record:** V18 G1 formally closed. Zero new components retained. Documented the crucial distinction between Event Economics (overall profitability) and Condition Value (incremental improvement over the counterfactual). Reviewed the component register (CAND-024, 035, 042) and determined it lacks sufficient independent, scientifically-qualified mechanisms for System Assembly. Recommended Path A (Return to G0) for V19 to discover new, structurally independent mechanisms.

## 70. Dual-Path Strategy & System Governance Amendment (2026-08-27)

- **Record:** Amended the Research Factory V2 doctrine to explicitly support two paths: Path A (Single Killer Strategy) and Path B (Modular Multi-Artifact System). Established that standalone insufficiency does not automatically disqualify a valid component. However, explicitly firewalled System Assembly from being used to rescue scientifically or economically failed research. Defined explicit qualification levels (Component-Candidate, Scientifically Qualified Component, Economically Qualified Component, System-Qualified Component).

## 71. G0 Candidate Generation V19 (2026-08-27)

- **Record:** V19 G0 candidate-generation cycle completed. Deliberately translated SMC concepts into explicitly observable, strictly falsifiable mathematical state transitions. Evaluated candidates on both standalone and component potential. Promoted 3 new candidates: CAND-G0-056 (Post-Sweep Structural Shift Confirmation), CAND-G0-057 (Weekly Opening Gap Fade Exhaustion), and CAND-G0-058 (Large-Range Expansion First Pullback Trap). G1 NOT EXECUTED.

## 72. G1 Economic Plausibility Screen V19 (2026-08-27)

- **Record:** V19 G1 completed. CAND-056 (Structural Shift) demonstrated a Type 1 counterfactual failure; demanding a market structure shift actively degraded the simple sweep mechanism. CAND-057 (Gap Fade Exhaustion) yielded zero frequency due to strict anchor requirement. CAND-058 (First Pullback Trap) was evidence-limited (N=2) due to strict continuous expansion requirement. Zero candidates promoted to G2 or added to Component Register. Next Action: Return to G0.

## 73. V19 Closure (2026-08-27)

- **Record:** V19 formally closed with zero component candidates retained. Established permanent governance lessons: A structurally observable confirmation condition can actively reduce predictive value (CAND-056). Removing a failed condition constitutes a new hypothesis, not a rescue.

## 74. G0 Candidate Generation V20 (2026-08-27)

- **Record:** V20 G0 completed. Focused on discovering simple, observable economic mechanisms whose intrinsic condition adds information without requiring stacked confirmation filters. Promoted 3 new candidates: CAND-G0-059 (Fresh Structural Break First Retest), CAND-G0-060 (NY Equity Close Imbalance Expansion), and CAND-G0-061 (Consecutive 15-Minute Rejection Sequence). G1 NOT EXECUTED.

## 75. G1 Economic Plausibility Screen V20 (2026-08-27)

- **Record:** V20 G1 completed. CAND-059 (First Retest) proved massively superior to its counterfactual (Second Retest), confirming the informational value of SMC Freshness, but failed absolute economics (negative net expectancy). CAND-060 (NY Close) and CAND-061 (Rejection Sequence) both failed due to extremely low evidence availability (N=5 and N=2) and negative expectancy. Zero standalone G2 promotions. Zero component candidates added. Next Action: Return to G0.

## 76. V20 Closure (2026-08-27)

- **Record:** V20 formally closed. Established the new governance distinction between ALPHA/EVENT ARTIFACTS (must possess standalone expectancy) and STATE/CONDITION ARTIFACTS (informational value without standalone profitability). CAND-059 was preserved as the factory's first State Artifact (RESEARCH-VALIDATED STATE INFORMATION).

## 77. G0 Candidate Generation V21 (2026-08-27)

- **Record:** V21 G0 completed. Generated explicitly separated Alpha and State candidates. Promoted CAND-G0-062 (Late-Session Trend Exhaustion Fade - Alpha), CAND-G0-063 (Asian Session Volatility Compression - State), and CAND-G0-064 (Structural Acceptance Time-State - State). G1 NOT EXECUTED.

## 78. G1 Economic Plausibility Screen V21 (2026-08-27)

- **Record:** V21 G1 completed. Evaluated separated Alpha and State candidates. CAND-062 (Late-Session Fade) failed absolute expectancy and counterfactual tests. CAND-063 (Asian Compression State) was non-adjudicable (N=2) for the specific target event combo. CAND-064 (Structural Acceptance Time-State) showed massive separation (Treatment N=2302, Counterfactual N=1564) but strongly falsified the hypothesis: a brief 'Sweep' makes a level dramatically safer to retest than a sustained 'Acceptance'. All candidates failed G1. Zero standalone G2 promotions. Zero components added. Next Action: Return to G0.

## 79. V21 Closure (2026-08-27)

- **Record:** V21 formally closed. CAND-064's falsification of the "Acceptance > Sweep" hypothesis was accepted. The inverse observation ("Sweep > Acceptance") was correctly quarantined as a research observation, enforcing the governance rule that Falsified Hypothesis ≠ Validated Inverse Hypothesis.

## 80. G0 Candidate Generation V22 (2026-08-27)

- **Record:** V22 G0 completed. Focused on constructing completely new hypotheses investigating structural sweeps, rather than just inverting CAND-064. Promoted CAND-G0-065 (Structural Sweep Depth Rejection State - State), CAND-G0-066 (Fresh Sweep vs Mitigated Sweep - Alpha), and CAND-G0-067 (Cross-Session Reference Sweep State - State). G1 NOT EXECUTED.

## 81. G1 Economic Plausibility Screen V22 (2026-08-27)

- **Record:** V22 G1 completed. Evaluated separated Alpha and State candidates. CAND-065 (Sweep Depth State) demonstrated the hypothesized right-tail effect for Deep Sweeps (+10.81 bps) vs Shallow Sweeps (-0.65 bps) but failed on extreme evidence limitation (N=27). CAND-066 (Fresh vs Mitigated Sweep) failed absolute expectancy and counterfactual tests, providing the valuable inverse finding to CAND-059: fresh levels are better to retest (bounce), but mitigated levels are slightly better to fade (sweep). CAND-067 (Cross-Session Sweep State) yielded exactly zero events. All candidates failed G1. Zero standalone G2 promotions. Zero components added. Next Action: Return to G0.

## 82. V22 Closure (2026-08-27)

- **Record:** V22 formally closed. Established the critical "State-vs-Alpha Dependency" lesson: State Information is not universally monotonic. Freshness is a powerful positive filter for retests (CAND-059) but a negative filter for fading sweeps (CAND-066). State artifacts cannot be declared "good filters" in isolation; their interaction with specific Alphas must be validated independently. CAND-065 is preserved strictly as an evidence-limited observation.

## 83. G0 Candidate Generation V23 (2026-08-27)

- **Record:** V23 G0 completed. Executed a strict reset directive: ALPHA EVENT FIRST. Exclusively searched for intrinsically profitable, independently observable events before applying specialized state filters. Promoted CAND-G0-068 (Post-Shock Absorption Reversal - Alpha), CAND-G0-069 (NY Mid-Session Reversal Anchor - Alpha), and CAND-G0-070 (Sustained Momentum Micro-Structure Failure - Alpha). Generated zero State candidates. G1 NOT EXECUTED.

## 84. G1 Economic Plausibility Screen V23 (2026-08-27)

- **Record:** V23 G1 completed. Evaluated three Alpha candidates for absolute expectancy and counterfactual superiority. CAND-068 (Post-Shock Absorption Reversal) failed due to extreme evidence limitation (N=7). CAND-069 (NY Mid-Session Reversal Anchor) generated a virtually flat net expectancy (+0.75 bps), failing to clear the >5 bps friction hurdle, despite slightly outperforming morning anchors. CAND-070 (Momentum Micro-Structure Failure) failed absolute expectancy and falsified its hypothesis: fading the first structure break in an overheated trend performs significantly worse than fading chop. All candidates failed G1. Zero standalone G2 promotions. Zero components added. Next Action: Return to G0.

## 85. V23 Closure & Component/State Qualification Readiness Review (2026-08-27)

- **Record:** V23 formally closed. Conducted a repository-wide evidence audit to determine if QuantForge should return to G0 or begin formally qualifying existing components. Determined that CAND-024 and CAND-035 possess massive historical expectancy and have passed scientific counterfactual validation, failing G2 promotion exclusively on calendar frequency. Defined the "Rare-Event Validation Doctrine" (event-counts vs calendar duration). Decided to suspend G0 and G1 to pursue RARE-EVENT COMPONENT QUALIFICATION for CAND-024 and CAND-035. System Assembly (S0) remains NOT YET EXECUTABLE.

## 86. Rare-Event Component Forward Qualification Protocol (2026-08-27)

- **Record:** Formalized the event-count-based forward qualification protocol for CAND-024 (Friday De-Risking) and CAND-035 (Month-End Imbalance). Reconstructed their exact frozen identities to prevent semantic drift. Established a minimum threshold of 3 independent forward events and a target of 5 forward events. Defined strict paper execution metrics, identity matching rules, and failure conditions. Verified that CAND-042, CAND-059, and System Assembly remain expressly excluded. Authorized the explicit launch of the qualification track, pending dedicated infrastructure provision.

## 87. Rare-Event Forward Infrastructure Provisioning (2026-08-27)

- **Record:** Provisioned the dedicated, isolated forward-observation infrastructure for CAND-024 and CAND-035. Enforced frozen contracts via deterministic hashing to prevent semantic drift. Implemented strict event/outcome ledgers, a paper execution firewall, exponential backoff reconnect logic, and timezone-aware session mechanics. Verified infrastructure readiness via pytest and a synthetic smoke test. Observation launch is formally authorized but pending broker feed configuration.

## 88. Rare-Event Forward Qualification Launched (2026-08-27)

- **Record:** RARE-EVENT FORWARD QUALIFICATION LAUNCHED — CAND-024 + CAND-035. Initiated the event-count based qualification track. Thresholds: MINIMUM = 3, TARGET = 5, MAXIMUM CALENDAR BOUNDARY = 18 MONTHS. Confirmed CAND-015 remains independent and protected. Verified paper-only execution layer strictly enforces no real or demo API order submission. Observation tracking relies purely on frozen contract evaluation and historical logic.

## 89. Rare-Event Forward Launch Integrity Audit (2026-08-27)

- **Record:** Audited the running forward qualification daemon for CAND-024 and CAND-035. Confirmed rigorous isolation of the paper execution layer. However, discovered the runner is actively fed by a deterministic synthetic market price generator (`time.sleep(1)` loop with canned quotes) rather than a live broker feed adapter. **Status:** OPERATIONAL BUT NOT TRUE FORWARD VALIDATION (BLOCKED). Observation clock cannot officially start until a live market-data adapter replaces the placeholder synthetic feed.

## 90. Rare-Event Market Feed Remediation (2026-08-27)

- **Record:** Refactored the rare-event runner to consume a clean `MarketDataFeed` interface and implemented a read-only MT5 adapter (`mt5_market_feed.py`). Enforced explicit `--mode forward` and blocked synthetic data from triggering forward mode. Tests verify strict isolation of `PaperExecutionFirewall` and proper handling of `DATA_STALE` states to avoid fabricating `NO_EVENT` records. The MT5 verification smoke test was executed but live ticks were unavailable for `USATECHIDXUSD`. **Status:** REAL MARKET FEED NOT VERIFIED — QUALIFICATION BLOCKED. Observation is fully provisioned but awaits a live MT5 terminal environment.

## 91. Rare-Event MT5 Read-Only Market Data Environment Diagnostic (2026-08-27)

- **Record:** Diagnosed the root cause of the missing `USATECHIDXUSD` feed data. Verified that MT5 and Python IPC are functioning correctly. Confirmed the local MT5 terminal is connected to an Exness trial server that does not provide `USATECHIDXUSD`. It offers alias instruments (e.g., `USTECm`), but the frozen contracts enforce strict instrument identity matching. **Status:** REAL MARKET FEED NOT VERIFIED — QUALIFICATION BLOCKED. The environment requires explicit architectural authorization to implement a symbol alias map or provision the correct broker environment before qualification can proceed.

## 92. Frozen Instrument Identity / MT5 Symbol Mapping Audit (2026-08-27)

- **Record:** Conducted an evidence-based audit of candidate mapping aliases (`USTECm`, `USTEC_x100m`) for the missing `USATECHIDXUSD` symbol. Determined that while price translation is deterministic, the exact Friday closing behavior and Month-End 16:00 ET closing imbalance mechanics of Exness CFDs cannot be guaranteed to perfectly match the frozen research dataset without historical verification. **Status:** MAPPING NOT SAFE — QUALIFICATION BLOCKED.

## 93. Explicit Frozen-Instrument Normalization Review (2026-08-27)

- **Record:** Conducted a formal governance review to re-evaluate the previous mapping rejection. Confirmed through direct MT5 M1 bar extraction that Exness `USTECm` provides dense, continuous quoting at the critical event thresholds (Fridays through 15:45 ET and month-ends through 16:00 ET). Established that all CAND-024 and CAND-035 event logic is structurally invariant under deterministic 1:1 price scaling. **Status:** APPROVED WITH NORMALIZATION. Explicit USTECm environment mapping approved for future CAND-024/CAND-035 forward qualification (Mapping ID: `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`). Historical candidate identities and contract hashes remain frozen; `USTECm` is declared strictly as an authorized execution environment representation.

## 94. Rare-Event Forward Qualification Launch & Integrity Check (2026-08-27)

- **Record:** Explicitly launched the CAND-024 and CAND-035 rare-event qualification daemon leveraging the approved `MAPPING:USATECHIDXUSD->EXNESS:USTECM:1.0`. Following the launch, conducted a read-only post-launch integrity check. Verified exactly one running process, correct telemetry logging (broker_symbol, logical_symbol, mapping_id), unchanged candidate/engine logic, synthetic paper-only isolation, and absence of data failures recorded as NO_EVENT. **Status:** POST-LAUNCH INTEGRITY CHECK PASSED. Qualification track officially frozen and moved into protected forward observation status.

## 95. Unified Forward Supervisor Implementation (2026-08-27)

- **Record:** Successfully migrated the ad-hoc rare event runner into a persistent, unified Windows Forward Supervisor (`quantforge_forward_supervisor.py`). Implemented a shared MT5 read-only connection supporting isolated module registries, independent event/outcome ledgers per candidate, graceful shutdown signaling, singleton `msvcrt` locking, and a Windows Scheduled Task configuration. Legacy ledgers were migrated seamlessly into `runtime/forward/history/` to preserve historical provenance, and the qualification clock continuity was strictly preserved. **Status:** UNIFIED FORWARD SUPERVISOR ACTIVE. CAND-024 and CAND-035 are in active protected observation. CAND-015 remains PROTECTED / EXTERNAL.

## 96. Canonical Contract Ratification & Qualification Resume (2026-08-27)

- **Record:** Discovered and resolved phantom hash problem. CAND-024 (`c49c5bb0`) and CAND-035 (`a7c2132d`) were not reproducible from any stored definition. Established canonical architecture: `FrozenStrategyContract` (executable semantics only, hash input) / `HistoricalEvidence` (research results, NOT in hash) / `EnvironmentMapping` (broker/runtime, NOT in hash). Canonical hashes: CAND-024 = `925495a8`, CAND-035 = `ddc5d0e9`. 78/78 contract tests pass. Engine consistency verified. Supervisor contract firewall verified. Pre-ratification period classified as INTEGRITY GAP (2026-08-27T09:44:58Z → 2026-08-27T10:10:08Z). Zero qualifying events accepted during gap. Valid canonical qualification resume: 2026-08-27T12:05:15Z. Original intended start preserved: 2026-08-27T09:44:58Z. Supervisor RUNNING (PID 6924), MT5 CONNECTED, both modules ACTIVE. Task Scheduler requires Administrator to install. **Status:** CANONICAL RARE-EVENT QUALIFICATION RESUMED — PROTECTED. CAND-015 remains PROTECTED / EXTERNAL. System Assembly remains NOT EXECUTED.

## 97. Forward Runtime Simplified to One Manual Unified Launcher (2026-08-27)

- **Record:** Simplified the forward-observation architecture to one manual BAT launcher, one supervisor, one MT5 read-only connection, and all currently authorized forward modules. CAND-015 integration assessed: CANNOT be safely integrated without semantic changes (dictionary-based identity, dual-market data, pandas/ATR engine). Decision: EXTERNAL / PROTECTED. BAT launcher modified for detached process launch. Singleton lock prevents duplicate supervisors. Task Scheduler declared NOT REQUIRED. 49/49 forward runtime tests pass. Operator workflow: `run_quantforge_forward.bat` → `status_quantforge_forward.bat` → `stop_quantforge_forward.bat`. After PC restart: operator manually runs `run_quantforge_forward.bat`. No automatic startup required. **Status:** FORWARD RUNTIME SIMPLIFIED — ONE BAT, ONE SUPERVISOR, ONE MT5 FEED. CAND-024 + CAND-035 under unified supervisor. CAND-015 remains PROTECTED / EXTERNAL. System Assembly remains NOT EXECUTED.

## 98. CAND-015 Adapter-Based Integration into Unified Runner (2026-08-27)

- **Record:** CAND-015 successfully integrated into unified forward runner via adapter pattern. Adapter translates shared MT5 feed into CAND-015's `process_tick()` interface. Key finding: CAND-015 engine only uses USATECHIDXUSD M1 data (BTCUSD buffered but unused). Adapter fetches latest completed M1 bar, maps USTECm → USATECHIDXUSD. Engine internals preserved (pandas, Wilder's ATR, M5/D1). Cold start accumulates M1 bars over time. 52/52 forward runtime tests pass. Architecture: ONE BAT → ONE RUNNER → ONE MT5 FEED → THREE INDEPENDENT OBSERVERS. No signal combination. No portfolio logic. **Status:** CAND-015 INTEGRATED VIA ADAPTER. ONE RUNNER, THREE INDEPENDENT OBSERVERS. System Assembly remains NOT EXECUTED.

## 99. Project Cleanup and Obsolete Infrastructure Pruning (2026-08-27)

- **Record:** Comprehensive cleanup of QuantForge repository. Removed root scratch .py (4 files), root .txt dumps (3 files), diagnostic scripts (2), stale logs (2), research/scratch/ (11 files), empty directories (4), __pycache__ (50 dirs, ~4 MB), .pytest_cache (2 dirs). Removed superseded infrastructure: run_cand015_forward.bat, install_quantforge_forward_task.bat, rare_event_runner.py, run_long_observation.py. Task Scheduler removal deferred (requires Administrator). ALL authoritative research preserved (271+ entries). ALL active forward runtime preserved. Tests: 130/130 pass. Supervisor RUNNING throughout. V24 readiness: READY. **Status:** PROJECT CLEANUP COMPLETED. OBSOLETE INFRASTRUCTURE PRUNED. UNIFIED MANUAL FORWARD RUNNER REMAINS CANONICAL.

## 100. End-of-Day Forward Runtime Freeze (2026-08-27)

- **Record:** Forward runtime stabilized for overnight observation. Added minimal event console notifications (DETECTED/CAPTURED/COMPLETED) with deduplication. CAND-015 adapter interface repaired (config + engine.state). 3 modules running under unified observer. One shared MT5 read-only connection. Qualification timeline preserved. Event counters: CAND-024 0/3/5, CAND-035 0/3/5. Next milestone: V24 G0 candidate generation. **Status:** FORWARD RUNTIME FROZEN FOR OVERNIGHT OBSERVATION. ONE RUNNER, ONE MT5 FEED, THREE INDEPENDENT MODULES.

## 101. Operator Workflow Correction — Stale Status / Process Authority (2026-08-29)

- **Record:** After PC reboot, `status_quantforge_forward.bat` reported RUNNING for a dead PID (5080). The persisted `status.json` was stale and was incorrectly treated as authoritative runtime state. Root cause: status script and launcher used file existence as proof of process liveness without verifying the actual Windows process. **Correction:** Created `process_validation.py` with robust PID verification via `wmic` command-line scanning. Fixed `status.py` to verify actual process before reporting RUNNING. Fixed `run_quantforge_forward.bat` to scan for real supervisor process (not just lock file). Fixed `stop_quantforge_forward.bat` to verify process exists before sending shutdown. Fixed supervisor to clean stale locks on startup. Added 63 regression tests covering process validation, stale status, stale lock, event console, BAT content, startup banner, uptime, paper safety, candidate independence, and contract firewall. All 117 tests pass (63 new + 54 existing). **Status:** MANUAL UNIFIED FORWARD RUNNER OPERATOR WORKFLOW CORRECTED. ACTUAL PROCESS STATE IS AUTHORITATIVE. STALE STATUS CANNOT REPORT RUNNING. TASK SCHEDULER NOT REQUIRED. ONE BAT LAUNCHER. ONE VISIBLE COMMAND PROMPT. ONE SHARED READ-ONLY MT5 CONNECTION. CAND-015 / CAND-024 / CAND-035 INDEPENDENT.
