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

The surviving corpus now records **two closed research lines** — Mean Reversion (economically non-viable under observed costs, DISC-021) and the fixed 12/1 TSMOM candidate (no stable incremental edge above drift across eras, DISC-022) — plus the V2 methodological advance (drift-controlled incremental identification with dependence-aware inference) and, subsequently, the H01 volatility-response program (H01 v1.1 invalid inference → v1.2 corrected null construction → the US-anchored H01 Equity V1 replication, DISC-023). The research factory's active line is **H01 Equity Track A (OPEN, narrowed US-equity program)**; the next milestone is **historical broad-US equity data acquisition / source verification** — not a new experiment, not a universe change, and not reopening either closed line.

## 16. H01 volatility-response program: broad H01 closed → H01 Equity V1 executed and adjudicated (2026-08-16)

- **H01 broad universal formulation: NOT ESTABLISHED / closed in that form.** H01 v1.1's registered inference was invalid (D_obs-centered bootstrap p ≈ 1 by construction); the v1.2 correction (null-imposing recentered bootstrap, protocol v1.2.0) was executed and independently adjudicated — the universal cross-asset claim was not supported; COMMODITIES_OTHER produced a formal contradiction of its registered inverse prior; the equity observations (historical `sp`, contemporary `USATECHIDXUSD`) showed classic direction but were EVIDENCE-LIMITED (one evaluable market per layer). H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / UNADJUDICATED.
- **Track A (equity) earned screening** → scope decision (broader data required) → data-source audit → data acquisition (composite: HPD `sp` + FRED cash indices; licensing PENDING/NOT-SENT) → outcome-blind definition lock (US-anchored, two exposures) → pre-registration (protocol v1.1.0, audited PASS after three precision corrections) → **H01 Equity V1 EXECUTED** exactly once (seed 20260816, B = 10,000, L = 11, single invocation, serial; protocol SHA-256 `a97cd0e2…`; artifact set under `output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY/`).
- **Adjudicated classification (independent, read-only):** EQBROAD_L1 = **EVIDENCE-LIMITED** (single historical market); EQBROAD_L2 = **SUPPORT** (SP500 + DJIA); EQTECH_L1 = **SUPPORT**; EQTECH_L2 = **SUPPORT**; 3 SUPPORT / 1 EVIDENCE-LIMITED / 0 CONTRADICTION / 0 INCONCLUSIVE; **EQTECH strong cross-era replication = TRUE** (same US-tech exposure, two eras, all p_Holm = 0.0004).
- **Strongest surviving claim:** classic volatility-response asymmetry is strongly supported in the tested US-tech exposure and replicates across two eras. **Not established:** generalization across US equity-index markets broadly; international generalization (outside scope).
- **Track A status: OPEN as a narrowed US-equity research program.** Remaining evidence gap: historical broad-US multi-market replication incomplete (`sp` only → EQBROAD_L1 evidence-limited).
- **Next legitimate task:** historical broad-US equity data acquisition / source verification (outcome-blind; NOT an experiment; any new market enters only via source verification → definition/universe amendment → pre-registration → independent audit → execution).
- **Firewall:** no rerun of H01 Equity V1; no universe change without amendment; no secondary rescue; no trading strategy; no BOE/runtime transfer; no merging with H01 v1.1/v1.2 results; commodities not reopened; universal H01 not revived.
- **Key artifacts:** `output/research_discovery/H01_EQUITY_V1_SCIENTIFIC_ADJUDICATION.md` (adjudication), `H01_EQUITY_VOLATILITY_ASYMMETRY/SCIENTIFIC_REPORT_H01_EQ_V1.md` + full artifact set, protocol, definition lock, scope decision, screening, data-source audit, data acquisition report (DISC-023).
