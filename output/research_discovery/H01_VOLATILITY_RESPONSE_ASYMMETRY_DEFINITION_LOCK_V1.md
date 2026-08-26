# QuantForge — H01 Volatility Response Asymmetry — Scientific Definition Lock V1

**Date:** 2026-08-13
**Task type:** OUTCOME-BLIND SCIENTIFIC DEFINITION LOCK — resolves the definitional gaps raised by `H01_VOLATILITY_RESPONSE_ASYMMETRY_READINESS_AUDIT_V1.md`.
**Status:** COMPLETE — decision recorded in §18.
**Firewall:** No experiment, no GARCH/EGARCH/GJR fitting, no effect calculation, no backtest, no clustering, no threshold optimization, no BOE/Assembly/Deployment/test/contract/governance modification. Only this artifact was created.

---

## 1. Executive Verdict

**H01 CAN be locked to LEVEL 2 — RESEARCH-READY — without observing any QuantForge outcome.**

The audit's blockers are resolved as follows:
- The universal "γ>0 everywhere" claim is **abandoned** in favour of an **asset-class-specific asymmetry** formulation (audit Option C), which is the form the external literature actually supports.
- Primary exposure, primary response, primary horizon, normalization, confound control, and falsification rule are each fixed **before outcomes** from literature precedent + measurement logic.
- The decisive honesty point: **equity indices are expected to show the classic leverage sign; precious metals are expected to show the INVERSE sign; FX/rates/crypto have no established directional prior (two-sided claim).** These priors come from the external literature (Black 1976; GJR 1993; Engle–Ng 1993; Baur 2012; Chen & Mu 2021), not from QuantForge data.
- GJR/EGARCH γ is re-classified as a **secondary model representation / robustness diagnostic**, NOT the primary hypothesis. The primary object is a non-parametric event/comparison response — the log change in realized variance — which matches the definition of the leverage effect used by Aït-Sahalia, Fan & Li (2013) ("correlation between a return and the change in its volatility").

**Next task (only): H01 V1 PRE-REGISTRATION.**

---

## 2. Final Scientific Statement

> **H01-L2 (locked):** *For each market, the forward change in realized variance following a negative daily return shock differs from that following a positive daily return shock of equal absolute magnitude, after conditioning on the pre-shock realized-variance state. The expected direction of this asymmetry is asset-class specific: (a) equity and equity-index markets are expected to exhibit the classic leverage sign — a larger volatility increase after negative shocks; (b) precious-metals markets are expected to exhibit the inverse sign — a larger volatility increase after positive shocks; (c) FX, rates, and crypto markets have no established directional prior, and for these the claim is two-sided (sign-dependent response exists; direction is not fixed a priori).*

This statement is:
- a **return → volatility** relationship (exposure = return; response = volatility change);
- **not** return prediction, vol timing, short-vol, regime filter, trend filter, or a mean-reversion signal;
- an **association** claim (see §10 causal-language firewall).

---

## 3. Asset-Class Scope

Formulation chosen: **Option B/C (asset-class-specific asymmetry with literature-derived expected directions per class)** — the formulation actually supported by the literature. Universal one-sign framing (Option A) is rejected because the literature contradicts it.

| Class | Expected direction | Primary source evidence | Status |
|---|---|---|---|
| Equity / equity indices | **Classic leverage** (negative shock → larger vol increase) | Black (1976); Christie (1982); Nelson (1991, EGARCH); GJR (1993); Engle–Ng (1993); Bekaert–Wu (2000); Aït-Sahalia–Fan–Li (2013) | **ESTABLISHED** (robust, daily–monthly) |
| Precious metals (gold, silver) | **Inverse leverage** (positive shock → larger vol increase) | Baur (2012, gold, robust across currencies/frequencies/samples); Lucey & Tully (2006, gold/silver); Demiralay & Ulusoy (2014, precious metals); Chen & Mu (2021) | **ESTABLISHED** (inverse) |
| Energy — crude (HPD `cl`) | **Classic leverage** | Chen & Mu (2021): only crude oil exhibits the classic leverage effect (daily spot) | **ESTABLISHED (narrow)** |
| Other commodities — grains, softs, livestock, industrial metals (HPD) | **Inverse leverage** | Chen & Mu (2021): inverse leverage effect in more than half of daily commodity spot prices; weaker in 3-month futures, weaker post-mid-2000s, weaker in monthly measures | **ESTABLISHED (broad)** |
| FX (EURUSD, HPD FX roots) | No established prior — sign varies by market/period | Osei-Assibey (2014): FX asymmetry sign differs across markets (Tanzania appreciation→higher vol; Ghana opposite); McKenzie (2002) review; Cho & Rho (2022) | **GENUINELY UNRESOLVED** |
| Rates (HPD `ed`, `us`) | No established prior | No strong asymmetric-vol literature for rates in this direction | **NO ESTABLISHED PRIOR** |
| Crypto (BTCUSD) | No established prior — scale-dependent, time-varying | Kakinaka & Umeno (2022): scale-dependent asymmetric volatility in cryptos; 2025 IRFA study: leverage in cryptos more pronounced post-Covid | **GENUINELY UNRESOLVED** |

**Locking rule:** no invented prior sign for any class. Classes without a literature-supported direction are tested **two-sided** (H01 for those classes = "sign-dependent volatility response exists," direction undetermined a priori). Equities and precious metals carry the **signed** primary claims.

---

## 4. Literature Evidence

### Established (genuinely demonstrated)
- **Equities/indices:** negative shocks raise subsequent conditional/realized volatility more than positive shocks of equal size. Daily-to-monthly, robust across samples and markets (Black 1976; Christie 1982; Nelson 1991; GJR 1993; Engle–Ng 1993; Bekaert–Wu 2000). Aït-Sahalia–Fan–Li (2013) formalize it as the correlation between the return and the **change** in volatility; present at 5-day and 21-day horizons, weak near the high-frequency limit.
- **Commodities/metals (inverse):** positive shocks raise volatility more than negative shocks in more than half of daily commodity spot prices; gold shows a robust inverted asymmetry; only crude oil shows the classic sign (Chen & Mu 2021; Baur 2012; Lucey & Tully 2006; Demiralay & Ulusoy 2014).

### Context-dependent (changes with asset class, horizon, market structure, vol regime)
- **Frequency/horizon:** asymmetry is frequency- and horizon-dependent (Aït-Sahalia–Fan–Li 2013: effect weak at high-frequency/short horizon, present at 5–21 days; Chen & Mu: weaker in monthly measures).
- **Futures vs spot:** inverse commodity effect weaker in 3-month futures (Chen & Mu 2021).
- **Era:** commodity inverse effect weaker after mid-2000s (Chen & Mu 2021); crypto leverage more pronounced post-Covid (2025 IRFA).
- **Market microstructure/vol regime:** asymmetry concentrates on extreme index moves (Hibbert et al. 2008); sign can differ by market structure (Chen & Mu crude-oil special structure).

### Contested (cannot be treated as established)
- **Causal mechanism:** leverage vs volatility feedback vs behavioral explanations are unresolved (Black 1976's leverage mechanism; French–Schwert–Stambaugh 1987 and Campbell–Hentschel 1992 feedback channel; Hasanhodzic & Lo 2011 "leverage effect without leverage"). H01 therefore claims the **statistical regularity**, not a mechanism.
- **Universality:** Aït-Sahalia–Fan–Li (2013) "leverage effect puzzle" — near-zero correlation at high frequency/short horizons for many assets despite theoretical expectations. Universal presence is contested.
- **FX sign:** mixed/opposing sign results across markets (Osei-Assibey 2014).

**No universal statement is made; the literature is kept class-specific (§3).**

---

## 5. Primary Shock (Exposure) Definition

- **PRIMARY exposure: the daily log return** `r_t` (close-to-close), as a signed scalar. **Rationale:** the leverage effect is canonically defined on returns — the raw shock in GJR/EGARCH variance equations and the "return" in the Aït-Sahalia et al. (2013) definition (correlation between return and change in volatility). Literature precedence → raw daily log return.
- **Equal-magnitude matching:** shocks are compared **within-market** at matched absolute magnitude |r_t| (bins or matched pairs), so a −x% move is compared with a +x% move. Magnitudes are matched within-market only; no cross-market magnitude pooling in the primary.
- **SECONDARY (pre-declared, cannot rescue primary):** standardized return `r_t/σ̂_{t-1}` and residual/market-adjusted return variants, used only as robustness diagnostics (Engle–Ng sign-bias methodology).
- **Not outcome-selected:** the raw log return is chosen for definitional precedence, not because of any QuantForge result.

---

## 6. Primary Response Definition

- **PRIMARY response: the log change in realized variance** over the forward horizon relative to the pre-shock window:
  `Δln RV_t = ln(RV_{t+1..t+5}) − ln(RV_{t−5..t−1})`,
  where realized variance over a window is the sum of squared daily log returns in that window.
- **Rationale:** Aït-Sahalia, Fan & Li (2013) define the leverage effect as the correlation between the return and the **change** in volatility — making the response object a volatility **change**, not a level. The log-change form is scale-invariant (unit-free), which resolves the cross-market comparability problem by construction and is the standard empirical target of the realized-volatility literature.
- **GJR/EGARCH γ status (explicit):** γ is a **SECONDARY model representation / robustness diagnostic** — NOT the primary hypothesis. The phenomenon (vol response asymmetry) is not equated with γ unless the literature supports that equivalence, which it does not universally.
- **Absolute-return response** (E[|r_{t+h}|]) is retained as an alternative secondary measure, NOT primary.

---

## 7. Primary Horizon

- **PRIMARY horizon: h = 5 trading days** (one trading week), forward window `[t+1, t+5]` vs pre-shock window `[t−5, t−1]`.
- **Literature support:** the effect is documented at 5-day and 21-day horizons in the realized-volatility literature (Aït-Sahalia–Fan–Li 2013 use 5-day and 21-day horizons; weekly is a standard volatility-measurement convention). The GARCH next-period (1-day) convention is preserved as the **secondary** horizon; 21-day (monthly) is also secondary.
- **QuantForge data resolution:** daily OHLC exists in both layers (M1 and HPD); 5-day windows yield ~260 non-overlapping windows per market on the ~5-year contemporary M1 layer — sufficient without inflating family size. Data-resolution feasibility, not effect size, guides this choice.
- **Dependence implications:** overlapping forward windows create serial dependence; the pre-registration must specify non-overlapping sampling or block/bootstrap inference. Recorded here as a pre-registration requirement, not a parameter.
- **Horizon is fixable a priori** (literature-backed, resolution-feasible) → not a Level-1 blocker.

---

## 8. Normalization

- **PRIMARY: within-market normalization.** Each market is analyzed on its own scale; the log-change response is already unit-free; equal-|r| shock matching is within-market. No cross-market scaling is required for the primary.
- **Within-asset-class** and **pooled-standardized-response** schemes are **secondary only**, used solely to aggregate *signed per-market results* (e.g., count/mean of within-market asymmetries per class) — never to pool raw responses across markets or classes.
- **No invented cross-market normalization** is introduced to enable pooling. The literature provides no canonical cross-asset normalization, so none is adopted for the primary.

---

## 9. Confound Controls (minimum scientifically justified)

**Confound:** a symmetric volatility-clustering process can appear asymmetric if negative and positive shocks occur in different volatility states.

- **PRIMARY control: conditioning on the pre-shock realized-variance state.** The response is already a vol-**change** (Δln RV) whose backward term (`RV_{t−5..t−1}`) is the pre-shock state; in addition, the comparison of negative vs positive shocks must be performed **within matched pre-shock volatility states** (stratification on `RV_back`, or inclusion of `ln RV_back` as a covariate). This isolates **sign of shock** from **pre-existing volatility state** — the Engle–Ng sign-bias discipline, applied in non-parametric form.
- **Secondary controls (pre-declared, robustness only):** EGARCH/GJR conditional specification (γ) and sign-bias regressions on standardized residuals.
- **Do not overbuild:** no multiple-regime state modeling, no clustering, no HMM in the primary. The minimum control is the pre-shock vol-state conditioning above.

---

## 10. Causal-Language Firewall

- **Locked terminology (mandatory in the pre-registration):**
  > "negative and positive return shocks are **associated** with asymmetric subsequent volatility responses."
- **Forbidden:** "negative returns **cause** higher volatility," or any mechanism claim (leverage/feedback/behavioral). The statistical-regularity framing is locked because causal identification is contested in the literature (§4 Contested).
- **Mechanism hypotheses** (leverage vs feedback) are explicitly out of scope for H01.

---

## 11. Extreme-Move Treatment

- **PRIMARY: use ALL eligible shocks.** No winsorization, no invented percentile/z-score threshold, no event-threshold strategy. The equal-magnitude matching handles magnitude comparability; extreme days are not silently dropped.
- **Secondary (pre-declared, robustness only):** a literature-standard winsorization if and only if it can be specified a priori (none is adopted as primary). Any trimming threshold must be pre-registered before outcomes.
- H01 is explicitly **not** converted into an event-threshold trading rule.

---

## 12. Cross-Market Structure

- **PRIMARY: separate per-market analysis.** Each market is tested individually; the scientific object is the within-market response asymmetry.
- **Aggregation (secondary, signed only):** within-asset-class aggregation of *per-market signed results* (e.g., proportion of markets showing the expected sign within a class), weighted so that a large class cannot dominate purely by observation count. Cross-class pooling is prohibited (classes carry different expected signs).
- No hierarchical panel model is required; one is not proposed. The structure preserves the per-class sign distinctions from §3.

---

## 13. HPD Historical Treatment

- **Roll construction:** HPD continuous front series are ratio-back-adjusted. Ratio back-adjustment is multiplicative in prices and therefore **does not change the log-return sequence's sign structure or its volatility response** — it preserves the return↔vol asymmetry object. This is a structural property, not an outcome claim.
- **Roll-day handling (pre-registration decision, NOT implemented here):** roll days can create artificial 1-day return spikes; the pre-registration must **exclude declared roll days** from the shock set and/or from RV windows. Recorded as a decision for the pre-registration, not executed now.
- **Known data-quality exclusions are sufficient:** quarantine/UNRESOLVED roots, zero-vol rows, zero-OI rows, `ohlc_inconsistent` and `weekend_rows` flags in `HPD_MANIFEST.csv` are excluded per the existing manifest discipline (already structural in the pipeline).
- **No additional volatility-treatment rule** is introduced; if one proves necessary it must be a documented pre-registration decision, not an implementation in this task. The ingestion pipeline is not modified.

---

## 14. Contemporary M1 Treatment

- **Two-layer structure (locked):**
  - **Historical Layer:** HPD multi-asset panel (1987–2002 common window).
  - **Contemporary Layer:** 2021–2026 M1 panel (5 markets: XAUUSD, XAGUSD, EURUSD, BTCUSD, USATECHIDXUSD; daily OHLCV; distinct coverage windows per market as recorded in the audit).
- **No combined statistic** (no single pooled estimator spanning both layers) unless scientifically justified in the pre-registration; the default is **per-class directional-consistency comparison across eras**.
- **Contemporary layer role:** test whether the phenomenon is **directionally consistent in a different era** — mirroring the Condition-8 discipline from the TSMOM gate, but at the class level and on a distributional (not return-predictive) object.
- **Class coverage in the two layers:** precious metals exist in both layers (M1 XAU/XAG; HPD metals); equity indices exist in both layers (M1 USATECHIDXUSD; HPD `sp`, `cac`); FX exists in both (M1 EURUSD; HPD 6 FX roots). Directional consistency per class is therefore testable for metals and equity indices; FX is two-sided.

---

## 15. Falsification Rule (no numerical tuning)

The primary inference object is the **within-market, vol-state-conditioned difference in Δln RV between negative and positive shocks of equal magnitude**, aggregated as signed per-market results, evaluated per asset class.

Classification (per class, against the §3 expected direction):
- **SUPPORT:** the pre-registered primary statistic shows a statistically reliable asymmetry in the class's expected direction, is directionally consistent across markets within the class, and — where the class exists in both eras — is directionally consistent across historical and contemporary layers.
- **CONTRADICTION:** a statistically reliable asymmetry in the **opposite** of the class's expected direction, or directionally inconsistent within the class (markets disagree in sign).
- **INCONCLUSIVE:** insufficient power, unstable direction, or failure to reject symmetry — with no claim made in either direction.

For classes with **no established prior** (FX, rates, crypto): SUPPORT = reliable sign-dependent asymmetry in *either* direction; CONTRADICTION = reliable evidence of **symmetric** response (no sign dependence); INCONCLUSIVE = otherwise.

**No arbitrary effect-size thresholds are invented** in this task; decision-rule cutoffs (significance level, family) are pre-registration choices. The classification is directional + consistency-based, per the audit's requirement.

---

## 16. Multiple-Comparison Boundary

Locked primary family (one each):
- one primary shock definition: signed daily log return, matched |r| within-market;
- one primary response: Δln RV (5-day forward vs 5-day pre-shock);
- one primary horizon: 5 trading days;
- one primary normalization: within-market;
- one primary inference object: the vol-state-conditioned signed Δln RV comparison per market, aggregated per class.

Secondary models (GJR/EGARCH γ, sign-bias regressions, standardized/residual exposures, 1-day and 21-day horizons, absolute-return response) are **identified as robustness diagnostics only** and **cannot rescue the primary result** if the primary fails. Multiplicity control for the pre-registered family is to be declared in the pre-registration (Holm-style family control; precedent DISC-021).

---

## 17. Independence from Closed Research

- **Mean Reversion (DISC-021):** H01 does not define displacement thresholds, recoil, persistence, recovery, entry confirmation, or reversal. It is a property of the **return→volatility process**, not an entry/exit signal. **INDEPENDENT.**
- **Fixed 12/1 TSMOM (DISC-022):** H01 does not define trend signals, directional return prediction, or volatility filters for TSMOM; it is not a TSMOM optimization or rescue. **INDEPENDENT.**
- **Firewall language:** H01 is exclusively a **volatility-behavior hypothesis**. Any future use of its findings as a filter, timing rule, or trade signal is a separate hypothesis requiring its own discovery/selection cycle.

**Trading-strategy firewall (audit §18):** the scientific question ("Does asymmetric volatility response exist?") is fully separated from the future strategy question ("Can someone exploit it economically?"). The strategy question is **not authorized** by this task and receives no definition here.

---

## 18. Level-1 / Level-2 Decision

### **A — H01 LEVEL 2 / RESEARCH-READY**

The final-definition test (§19 of the task) is passed **without observing any QuantForge outcome**:

| Item | Status |
|---|---|
| 1. Exact scientific statement | LOCKED (§2) |
| 2. Asset-class scope | LOCKED — Option B/C (§3) |
| 3. Expected direction by class | LOCKED from literature (§3) — equities classic, metals inverse, FX/rates/crypto two-sided |
| 4. Primary shock | LOCKED — signed daily log return (§5) |
| 5. Primary volatility-response measure | LOCKED — Δln RV (§6) |
| 6. Primary horizon | LOCKED — 5 trading days (§7) |
| 7. Normalization | LOCKED — within-market (§8) |
| 8. Minimum confound control | LOCKED — pre-shock vol-state conditioning (§9) |
| 9. Falsification rule | LOCKED — directional SUPPORT/CONTRADICTION/INCONCLUSIVE (§15) |
| 10. Historical vs contemporary structure | LOCKED — two layers, per-class era consistency (§14) |

**No item depends on QuantForge outcomes.** Every choice is anchored to the external literature or to a structural data-resolution/measurement fact. Level 2 is therefore reached legitimately.

---

## 19. Exact Next Task

**H01 V1 PRE-REGISTRATION** (the ONLY authorized next step):
- translate §2–§16 into a frozen pre-registration: locked statement, per-class expected directions, primary/secondary statistics, horizon and windows, normalization, confound-control procedure, falsification decision rule with declared family and significance level, roll-day exclusion rule for HPD, and two-layer era-consistency design;
- followed by the independent protocol audit before any experiment.

If the pre-registration cannot fix the decision rule without outcome knowledge, it must return for re-audit — but no such blocker is identified by this definition lock.

---

## 20. Integrity

- **Outcome-blind:** no QuantForge effect was computed, no experiment run, no GARCH/EGARCH/GJR fitted, no backtest, no clustering, no threshold optimized. Choices were made from external literature and structural data facts (file coverage, HPD manifest flags, daily resolution).
- **Artifact only:** this is the sole file created by this task. No scripts, datasets, models, protocols, or result files.
- **Literature:** all direction priors trace to the cited primary sources (Black 1976; Christie 1982; Nelson 1991; GJR 1993; Engle–Ng 1993; Bekaert–Wu 2000; French–Schwert–Stambaugh 1987; Campbell–Hentschel 1992; Aït-Sahalia–Fan–Li 2013; Baur 2012; Lucey & Tully 2006; Demiralay & Ulusoy 2014; Chen & Mu 2021; Osei-Assibey 2014; McKenzie 2002; Kakinaka & Umeno 2022; Hasanhodzic & Lo 2011; Hibbert et al. 2008). Where a class has no defensible prior, none is invented.
- **Firewall:** no BOE, Assembly, Deployment, tests, contracts, or governance files modified. Research never executes. The decision here is a research-domain classification only.
- **Standing:** this lock supersedes the audit's Level-1 classification specifically by resolving the audit's listed missing decisions; it does not reopen any closed research line and does not authorize any experiment.