# QuantForge — H01 Volatility Response Asymmetry — Independent Research-Readiness Audit V1

**Date:** 2026-08-13
**Audit type:** INDEPENDENT RESEARCH-READINESS AUDIT — read-only, adversarial, pre-registration gate.
**Subject:** H01 — Volatility Response Asymmetry (leverage effect), primary candidate selected in `NEW_HYPOTHESIS_SCREENING_V1.md`.
**Scope:** AUDIT ONLY. No experiment, no protocol, no model fitting (no GARCH/EGARCH/GJR parameter estimation), no backtests, no K-means, no clustering, no source/test/contract/governance modifications.
**Status:** COMPLETE — decision recorded in §17.

---

## 1. Executive Verdict

**H01 as stated is a genuine, externally well-established phenomenon — but NOT for the market universe the QuantForge data panels actually contain. The candidate is therefore PROMISING BUT NOT READY for pre-registration until its scientific definition is re-scoped by asset class and its primary measurable object is fixed. It must NOT be pre-registered in its current form.**

Three independent findings drive this verdict:

1. **The classic "leverage effect" (volatility rises more after negative shocks) is an EQUITY / index-market phenomenon.** The authoritative commodity literature finds the *opposite* sign — an "inverse leverage effect" (volatility higher after *positive* shocks) in MORE THAN HALF of daily commodity spot prices, with only crude oil showing the classic leverage effect (Chen & Mu 2020/2021, *Journal of Commodity Markets* 22:100139; Baur 2012 for gold; Lucey & Tully 2006; Demiralay & Ulusoy 2014). The QuantForge contemporary M1 panel is `{XAUUSD, XAGUSD, EURUSD, BTCUSD, USATECHIDXUSD}` — 2 metals, 1 FX, 1 crypto, and only 1 equity index. The HPD historical panel (32 manifest rows; screening said 28 markets) has only **2 equity-index roots** (`sp`, `cac`) and is otherwise FX(6)/Metals(5)/Grains(4)/Softs(4)/Energy(2)/Rates(2)/Livestock(2)/UNRESOLVED(5). H01 in its "γ>0 everywhere" form is therefore a directional claim the literature predicts will *fail on the majority of the panels*.

2. **Definition clarity is not yet research-ready.** Exposure variable (raw signed daily return vs standardized vs residual vs market-adjusted), response variable (next-day conditional variance vs realized vol over a horizon vs log-variance change vs |return|-response), and horizon are all **unresolved pre-registration choices** — the literature uses differing conventions and supplies no single canonical pair. H01 cannot be registered until these are fixed *before* outcomes.

3. **The screening's evidence claim over-generalizes.** The screening asserted H01's effect is "Widely replicated across equities, indices, FX, and commodities." The literature audit shows the negative-shock asymmetry is robust in **equities/indices** but is **absent, weak, or inverted in FX and most commodities.** This corrects the screening's A-score basis.

The audit does **not** reject the *possibility* of a legitimate pre-registration: a properly scoped version — per-asset-class expected signs, literature-anchored exposure/response definitions, a confound-controlled event/distributional design — is reachable. But that re-scoping is a scientific definition decision that must be made BEFORE outcomes, and it is not yet made here.

---

## 2. Exact Scientific Hypothesis

**H01 (as declared in screening):** conditional volatility responds more to negative than to positive return shocks of equal absolute magnitude (asymmetry coefficient γ > 0 in GJR/EGARCH form), sign-consistent between the historical (HPD) and contemporary (M1) panels.

**Audit restatement (must this be preserved):**
> **H01-A:** For a given market, a negative daily return shock of magnitude |r| is followed by a larger increase in conditional (or realized-over-horizon) volatility than an equally sized positive return shock.

- The phenomenon is the **statistical response of volatility to the sign of recent returns** — NOT "volatility predicts returns", NOT "high vol predicts returns", NOT "bear markets are more volatile", NOT "short vol is profitable", NOT "GARCH predicts price direction", NOT "vol timing improves trades". Any of those substitutions silently replaces the hypothesis.
- **γ>0 is a model-family parameterization of the phenomenon, not the phenomenon itself.** The hypothesis under test is the response-asymmetry; GJR/EGARCH γ is one measurement technology. This distinction is decisive for §5.

---

## 3. External Evidence Audit

Labels: **[SF] SOURCE-DERIVED FACT** — stated directly in the cited source (paraphrased); **[EI] EXTERNAL INFERENCE** — my inference from what the source demonstrates; **[MI] MODEL INFERENCE** — property demonstrated only within a fitted model family.

| Reference | Market(s) / freq / sample | What was demonstrated | Direction & definition | Status | Transfers to QuantForge panels? |
|---|---|---|---|---|---|
| Black (1976) | US equities | Negative correlation between returns and volatility changes; proposed leverage mechanism | Classic leverage effect; negative shocks → vol up. **Mechanism is a hypothesis**, correlation is the fact. **[SF]** | Correlational | Equities only; mechanism contested (Hasanhodzic & Lo 2011: "leverage effect without leverage"). |
| Christie (1982) | US equities | Coined "leverage effect"; documented asymmetry | Negative-return vol asymmetry **[SF]** | Correlational | Equities only. |
| Nelson (1991) EGARCH | Equity index | Asymmetric conditional vol model; negative shocks raise next-period vol more | γ<0 in EGARCH (asymmetry) **[MI]** | Model-implied | Equities. |
| Glosten–Jagannathan–Runkle (1993) GJR | US equity index | Asymmetric response of conditional variance to sign of lagged shock | γ>0 asymmetry term **[MI]** | Model-implied | Equities. |
| Engle–Ng (1993) | Equity | Sign-bias tests formalize asymmetry as larger vol response to negative shocks | Negative-shock asymmetry **[MI]** | Model-implied | Equities. |
| French–Schwert–Stambaugh (1987); Campbell & Hentschel (1992) | US equity | Volatility **feedback** channel: high ex-ante vol → lower contemporaneous returns | Feedback runs vol→returns, opposite causal direction **[SF]** | Model/causal debate | Confounds any simple return→vol claim (§8). |
| Bekaert & Wu (2000) | Equity portfolios | Leverage vs feedback decomposition | Both channels present; "leverage effect" ≠ pure leverage **[SF]** | Causal decomposition | Conceptual only. |
| Hibbert, Daipler & Dupoyet (2008) | Equity index (SPX return/VIX) | Negative asymmetric return–vol relation; strong on extreme index moves | Behavior/feedback explanation **[SF]** | Correlation + model | Index only. |
| Chen & Mu (2020/2021), *J. Commodity Markets* | 10+ commodities, daily spot + 3-mo futures, pre-2010s & post-mid-2000s | **"INVERSE leverage effect": volatility HIGHER following positive shocks in more than half of daily spot prices; effect weaker in 3-mo futures, weaker after mid-2000s, weaker in monthly vol. Only crude oil shows classic leverage.** | Inverse asymmetry dominant **[SF]** | Correlational + model | **DECISIVE challenge**: most commodity/metal markets in the panels are expected to show the *opposite* sign. |
| Baur (2012), *J. Alternative Investments*; Lucey & Tully (2006); Demiralay & Ulusoy (2014) | Gold (and silver/precious metals), daily, 1982–2002 + later | **Gold exhibits INVERTED asymmetric volatility: positive shocks increase gold vol more than negative shocks**, robust across currencies/frequencies/samples; safe-haven mechanism | Inverse asymmetry in gold/silver **[SF]** | Correlational | **DECISIVE**: XAUUSD and XAGUSD in the M1 panel are gold/silver — literature predicts the opposite sign of classic γ>0. |
| Ait-Sahalia, Fan, Li (2013) "The Leverage Effect Puzzle" | Equity, high-freq | Correct definition is correlation between vol-**changes** and returns; sampling/measurement biases distort the effect | Definitional order **[SF]** | Methodological | Instructive for definition (response = Δvol, not level). |
| Moreira & Muir (2017) | Equities | Vol-managed portfolios; scaling inverse to vol | THIS IS H02's evidence, NOT H01's | — | Cited in screening "where applicable"; does not establish sign of vol response. |

### 3.1 Net evidence position

- **Strong, replicated for equities/indices** (Black 1976 → Engle–Ng 1993 → Bekaert–Wu 2000; continuous replication). This is one of the most robust stylized facts in *equity* finance. **[SF/EI]**
- **Inverted or absent for most commodities/metals; mixed/weak for FX and crypto.** Chen & Mu (2021): inverse leverage in >half of daily spot prices; only crude oil classic. Baur (2012): gold inverted. FX asymmetry is documented but the sign robustness is weaker and horizon/frequency dependent. **[SF]**
- **Replication reality:** the classic sign is replicated across *equities*; the commodity literature replicates an *inverse* sign. The screening's "replicated across equities, indices, FX, and commodities" is **incorrect** as written and must be corrected.
- **Causal status:** the relation is correlational/model-implied; causal channel (leverage vs feedback vs behavioral) is contested. An audit-friendly hypothesis must therefore claim the *statistical regularity conditional on past volatility*, not a mechanism.

---

## 4. Definition Clarity

| Element | Screening status | Audit finding | Pre-registration readiness |
|---|---|---|---|
| Exposure variable | "recent return shock", sign-symmetric magnitude | **Unresolved**: raw daily log-return? standardized return (r/σ)? residual after AR? market-adjusted? | Must be fixed BEFORE outcomes — no canonical literature choice; literature spans raw daily returns (GJR/EGARCH) and standardized returns (event studies). |
| Response variable | "conditional volatility", γ in GJR/EGARCH | **Unresolved**: next-day conditional variance? realized vol over horizon? log-variance change? | Literature canonical is next-period conditional vol (GARCH) vs realized vol over window (absolute-return response). **No single canonical pair.** Must be frozen. |
| Horizon | "recent" / next-day implicitly | **Unresolved**: 1-day? multi-day realized window? Helpful anchor: Ait-Sahalia et al. define the effect on vol-**changes** over a short horizon; GARCH family implies next-period. | Unresolved pre-registration choice; must be declared. |
| Sign expectation | γ>0 (negative-shock asymmetry), "sign-consistent" across panels | **Wrong as a universal claim**: sign is asset-class dependent (equities +, metals −/inverted, FX/crypto ±). "Sign-consistent between HPD and M1" bundles heterogeneous classes into one test. | Must be re-scoped **per asset class** with pre-declared expected signs. |

**Verdict:** H01's definition is NOT research-ready. The exposure/response/horizon triple and the asset-class-dependent sign are all open choices that must be locked before any outcome is seen. **Definition clarity: partial.**

---

## 5. Model Necessity

- **The scientific hypothesis is the phenomenon, not γ.** The question is: *"Is the scientific hypothesis the phenomenon itself (negative shocks → larger vol response), or is γ>0 specifically the hypothesis?"* Answer: the phenomenon. γ>0 is one measurement technology (GJR/EGARCH point-estimate). The literature demonstrates the phenomenon via **both** event-style comparisons (Hibbert et al.; realized-vol-after-shock studies) and parametric GARCH families (Engle–Ng; GJR).
- **An over-parametrized claim would be invented here, not sourced:** mandating "GJR/EGARCH γ is THE primary" is a model-choice that must be justified, and GARCH estimation yields point estimates with standard-error fragility and spec-dependence. The audit cannot bless γ as primary without the pre-registered specification.
- **Simplest-valid-design principle (Constitution; screening §13):** the simplest design that can falsify the phenomenon is an **event/comparison design**: compare the change in realized volatility (e.g., log-vol change over a pre-declared post-horizon) following negative vs positive shocks of matched magnitude, **conditioned on lagged volatility** — with the parametric GJR/EGARCH γ as a **secondary confirmatory** statistic only if its complete spec (lags, distribution, horizon) can be frozen. This is the minimal valid architecture; the audit requires the pre-registration to so classify primary vs secondary.
- **Falsification must not depend on an un-estimable or spec-fragile parameter.**

---

## 6. Data Compatibility (structural, feasibility only — NO effect computed)

**Contemporary M1 panel (5 markets, daily OHLCV):**
| Market | First | Last | Rows | Class |
|---|---|---|---|---|
| EURUSD_M1 | 2021-01-04 | 2026-06-30 | 2,041,613 | FX |
| XAUUSD_M1 | 2021-04-12 | 2026-04-10 | 1,768,123 | Metal (gold) |
| XAGUSD_M1 | 2021-07-13 | 2026-07-12 | 1,729,136 | Metal (silver) |
| BTCUSD_M1 | 2021-05-23 | 2026-05-22 | 2,539,807 | Crypto |
| USATECHIDXUSD_M1 | 2023-09-01 | 2026-07-10 | 906,815 | **Equity index** |
- **Only 1 of 5 contemporary markets is an equity index**, and its history is the shortest (~2.9y). The classic leverage sign is *expected* only there.
- **Gold and silver** (2 of 5) are inverted-asymmetry per Baur (2012)/Demiralay & Ulusoy (2014). EURUSD (FX) and BTCUSD (crypto) have weaker/mix-known asymmetry.
- M1 files span ~2021–2026, ~5y; a daily-granularity panel gives ~1,200–1,800 trading days per market; daily data is **sufficient** for the exposure/response definitions above. Intraday (tick) is **not required** to test the daily-level phenomenon; tick files exist for cost/economics only.

**Historical HPD panel (28 markets used by TSMOM_V2; 32 manifest rows):**
- Panel asset-class distribution (manifest): FX 6, Metals 5, Grains 4, Softs 4, **Equity index 2 (`sp` 1982–2002 24,207 rows; `cac` 1999–2002 4,902 rows)**, Energy 2, Rates 2, Livestock 2, UNRESOLVED 5.
- Common window 1987-01-13 → 2002-08-30 (TSMOM_V2: 175 position months).
- **Only 2 equity-index roots** carry the classic expected sign; ~24 non-equity roots (FX/metals/grains/softs/energy/rates/livestock) are classes where the literature predicts inverse/weak/mixed asymmetry.

**Structural conclusions:**
1. **The panels exist and daily OHLC is sufficient** to register a daily-horizon vol-response asymmetry test — data compatibility is *feasible* in a purely data-availability sense.
2. **The panel mix does NOT match the classic-sign hypothesis.** A "γ>0 sign-consistent everywhere" test is structurally mis-targeted: the literature's expected sign differs by asset class, and the panels are dominated by classes where the classic sign is *not* expected.
3. **HPD continuous-series methodology**: HPD daily front series can contain contract rolls and OI/vol metadata flags (manifest tracks `n_contracts`, `max_gap_days`, `ohlc_inconsistent`, `weekend_rows`, `zero_oi_rows`, `zero_vol_rows`, `quarantine`); continuous-series construction can distort volatility estimates around rolls/gaps. A registerable HPD test must pre-declare roll/gap handling. This is a **methodology fix that must be frozen** — noted now, to be made concrete only in pre-registration.
4. Survivorship/roll limitations: HPD covers mature contract markets only; `UNRESOLVED`/quarantine rows must be excluded explicitly.

---

## 7. Normalization (per audit spec)

- **Cross-market raw-quantity comparability is invalid**: gold, currencies, rates, agriculturals, and equity indices trade at different volatility levels, units, and spreads. Comparing raw conditional-variance responses across them is meaningless.
- **Literature canonical choice is WITHIN-market:** GARCH/EGARCH/GJR and event designs are estimated **per market** (each market its own model/vol). There is **no cross-sectional canonical normalization** in the leverage-effect literature because the effect is per-market.
- **Options for the panel:** per-market standardization (volt-scaled shocks, i.e., r_t/σ_{t-1}), %-change in variance (Δln σ²), or within-market rolling z-score of the response. Standardized-shock event designs (Engle–Ng sign-bias; risk-parity-of-shock logic) are the literature-consistent default; %-change in variance handles vol-level differences unit-free.
- **Therefore:** normalization is **partially literature-derived** (within-market; standardized shocks) but the *specific* choice among defensible variants is a **must-be-frozen pre-registration choice** — NOT something to be selected from QuantForge outcomes.
- **Cross-market pooling danger:** pooling all markets into one γ>0 claim invites a sign-heterogeneity washout because classes disagree. Pooling may only be done **within asset class**, and even then the panel has tiny N per class (e.g., 1 equity index contemporary, 2 HPD). Observation count is not a substitute for sign-consistency.

---

## 8. Confound Control (conceptual, no computation)

- **Volatility persistence/leverage confound:** the question the audit raises — *can a symmetric vol process + persistence mechanically produce an apparent asymmetry?* — is real. If shocks correlate with vol-level states, or if the regressor is standardized inconsistently, a symmetric process can look asymmetric. **Required control (conceptual):** the primary test must be **conditional on lagged volatility** (e.g., test the diff-in-diff of Δln σ² between negative/positive shocks of equal magnitude *given* σ_{t-1}), and/or include a sign-bias regression on residualized returns. This is the standard Engle–Ng sign-bias discipline.
- **Volatility-feedback confound (French–Schwert–Stambaugh; Campbell–Hentschel):** part of the negative return/vol relation may run vol→return, not return→vol. The pre-registration must state the claim as **the statistical response-asymmetry conditional on lagged vol**, explicitly NOT as a causal "returns CAUSE volatility" claim.
- **Regime leverage-vs-regime:** must be able to distinguish a *persistent-volatility-regime* artifact from a *sign-based response*. Conditioning on σ_{t-1} plus a pre-declared drift check addresses this.
- **Herding / extreme-move confounding:** Hibbert et al. note asymmetry concentrates on extreme index moves; the test must decide whether "equal magnitude" bins are fixed in absolute or standardized return units, and whether extreme events are handled (do NOT silently drop them).
- **Adsorbing no new designs here:** only the *requirement set* is recorded; the design is for pre-registration.

---

## 9. Independence from Closed Research Lines

- **Closed MR family (DISC-021) — essential claims:** displacement/recoil/panic-momentum/exits/MAE-MFE/session-filter. H01 is a property of the **return→volatility process**, not an entry signal or displacement condition. **INDEPENDENT.**
- **Closed fixed 12/1 TSMOM (DISC-022) — essential claims:** 12/1 trend persistence/continuation. H01 claims **no return predictability direction**; it is about vol response to return sign, not "returns continue/reverse." **INDEPENDENT.**
- **Prohibited reductions (must be defended in pre-registration):**
  1. H01 must NOT be converted into "negative returns predict returns" (reversal or continuation claim). It predicts *volatility response*, not return direction.
  2. H01 must NOT be used to justify a *trade* on negative returns (that would be a strategy on the closed MR idea).
  3. H01 must NOT be folded into "vol-state improves TSMOM" or "vol-regime filter rescues 12/1" — the closed 12/1 is not reopenable by adding a vol condition; H01 must stand alone as a measurement claim on the vol process.
- **Keep-clean rule:** the "conditional volatility responds to sign" object is fine; "conditional *return* responds to vol" (H02's neighbor) is a different hypothesis and must not be absorbed into H01's phrasing.

---

## 10. Falsification

- **Primary null (registerable):** conditional on lagged volatility, the change in post-horizon log-variance after negative shocks equals that after positive shocks of equal magnitude (no sign asymmetry) — and, per-class where classic expected, γ ≤ 0.
- **Expected direction:** defined **per asset class from the literature** (equities/indices: negative-shock asymmetry; metals/gold/silver: positive-shock ("inverse") asymmetry — the *opposite* of the screening's universal γ>0; FX/crypto: direction left pre-declared OR two-sided exploratory).
- **Sufficient evidence:** a pre-registered statistic/value/monotonicity rule; cross-market and cross-era sign-consistency **within asset class** (do NOT pool classes). Audit does NOT invent numerical thresholds — none are imposed here; any decision-rule cutoff is a pre-registration decision, not an audit invention.
- **Cross-market inconsistency classification:** a failed sign within a class under a sufficiently powered, correctly conditioned test is **evidence against** the class-level claim; inconsistency across classes is **expected** (sign heterogeneity), NOT a failure. Only *within-class* instability or within-class null results falsify.
- **Era (HPD vs M1) requirement:** the screening demanded sign-consistency across panels. At the daily-horizon vol-response level, HPD (1987–2002) vs M1 (2021–2026) uses **different markets** (barely overlapping roots), different eras, and different sampling structures — so "sign-consistent across panels" is answerable only class-by-class, and classes are thin (see §6/§7). The audit therefore requires the pre-registration to define *what counts as cross-era confirmation for each class*, including how the sole contemporary equity index (USATECHIDXUSD) can be compared against HPD's `sp`/`cac` honestly.

---

## 11. OOS / Chronological Validation Design

- **Do NOT auto-copy the TSMOM TRAIN/VALIDATION/TEST architecture.** The vol-response question is a distributional-statistical test, not a machine-learning/parameter-selection problem. The simplest scientifically appropriate structure is:
  - **Primary:** a pre-registered single statistic computed on the full contemporary M1 window and, separately, on the HPD window — with explicit chronological sub-splits (early/late halves within M1; within HPD) used only for *stability inspection*, not model selection.
  - **Chronological replication:** because the panels are short (~5y contemporary), the honest evidence is (a) statistical significance per market, (b) **cross-market within-class sign consistency**, (c) **era replication** (HPD historical vs M1 contemporary) per class. If a TEST holdout is declared, it is the *last* portion of M1 and is inspected exactly once.
- **Class replication = the OOS:** with N per class tiny (1 equity index contemporary; 2 HPD equity indices), the audit flags that **equity-sign power is structurally limited** in this inventory; a high-confidence equity-H01 test may not be feasible with the contemporary inventory alone. This is a data-compatibility cost, not a test-machinery problem.

---

## 12. Multiple Comparisons

- **H01 must NOT be turned into a grid.** Recommended frozen structure:
  - ONE primary exposure (e.g., standardized signed daily return), ONE primary response (Δln σ² over declared post-horizon or GJR-γ under a fully frozen spec), ONE primary horizon, ONE decision rule. Everything else (alt.-standardization, alt. horizons, GJR-vs-event versions, per-class sub-samples) is EXPLICITLY SECONDARY/EXPLORATORY and is declared as a family with a pre-registered multiplicity control (e.g., Holm on the primary family) — mirroring the DISC-021 discipline that surfaced exactly one survivor in a 12-test family.
- **Do not test "all four exposure variants × four responses × three horizons"** — that is a grid, prohibited.

---

## 13. Parameter Readiness Scoring

| Parameter | Source type | Audit assessment |
|---|---|---|
| Sign expectation per asset class | `SOURCE-DERIVED` via literature (Black; Baur 2012; Chen & Mu 2021) | **Ready if** assigned per class; NOT as universal γ>0. |
| Exposure: standardized signed return | Partially source-derived (Engle–Ng sign-bias uses standardized/residualized returns); choice among defensible variants arbitrary | **Must be frozen**; not outcome-selected. |
| Response: Δln σ² vs GJR-γ | Δln σ² is data-construction-derived but design-selected; GJR-γ is MODEL INFERENCE with spec choices | **Must be frozen**; primary/secondary ordering justified. |
| Horizon (1-day vs multi-day realized) | No canonical literature value | **Unresolved pre-registration choice**. |
| Roll/gap handling on HPD | Data-construction-derived | **Must be frozen** before outcomes. |
| Multiplicity control family | Scientific-justification (Holm precedent from DISC-021) | Ready. |
| Any threshold/cutoff values | Non-invented rule only; literature does not supply a universal numeric cutoff | **Must be a declared pre-registration choice**, not an audit invention. |

**Assessment:** the central definition still requires arbitrary-choice-free locking; per the readiness-level rule, H01 is **NOT at Level 2** because the central definition (sign-by-class, exposure, response, horizon) cannot yet be fixed without additional *scientific* decisions — not because outcomes are unknown, but because the choices are not yet made.

---

## 14. H01 vs K-Means / Regime Work — no compound hypothesis

- H01 is and remains a **univariate, per-market, return-sign → volatility-response** claim.
- **H01 must NOT become "K-means predicts leverage-effect regimes."** The K-means/regime candidate (H03) is a *separate* hypothesis about state structure. Any claim of the form "the leverage effect differs across K-means-derived regimes" is a **compound hypothesis requiring its own screening** — it is not H01 and must not ride H01 into pre-registration. **No clustering is authorized by this audit or its outcome.**

---

## 15. Readiness Score (axes same as screening, 0–5)

| Axis | Screening H01 | Audit H01 | Audit rationale |
|---|---|---|---|
| A evidence | 5 | 4 | Robust for equities; **not** "across FX and commodities" — inverted commodity/metal evidence (Baur 2012; Chen & Mu 2021). |
| B definition clarity | 5 | 3 | Exposure/response/horizon unresolved; universal sign mis-scoped. |
| C parameter clarity | 4 | 3 | Standard GARCH family known, but core definition params (horizon, response, sign-by-class) not frozen. |
| D data compatibility | 5 | 3 | Data exists (daily OHLC sufficient), but class mix mismatches classic sign; equity-index N structurally tiny. |
| E reproducibility | 5 | 5 | Deterministic, local M1/tick/HPD files; pre-registrable. |
| F OOS testability | 4 | 3 | Era split exists but per-class N tiny; equity-sign OOS structurally limited. |
| G economic plausibility | 3 | 3 | Distributional property; economic value via risk conditioning, not standalone trade (unchanged). |
| H independence | 5 | 5 | Independent of MR and 12/1 closed lines when kept as a vol-response claim. |
| I experimental minimalism | 4 | 3 | Event design simple, but GJR-spec freedom and multi-horizon risk add machinery; must be pruned in pre-registration. |
| **Total** | **40 / 45** | **32 / 45** | Down 8 points, driven by corrected evidence scope, definition openness, class-mix data mismatch, and OOS thinness. **Not inflated.** |

---

## 16. Readiness Level

- **Current: LEVEL 1** (hypothesis stated; NOT yet pre-registrable). The scientific definition cannot yet be fixed before outcomes because the sign-by-class, exposure, response, and horizon choices remain open.
- Level 2 (research-ready/pre-registrable) is **reachable** after the open scientific decisions in §17 are made — but it is not granted by this audit.

---

## 17. Decision

### **B — PROMISING BUT NOT READY**

H01 is not rejected: the underlying phenomenon is real and well-documented in equity markets, the data exists, and a properly scoped pre-registration is achievable. But H01 **in its current form** is not research-ready, and any registration keyed to a universal "γ>0 sign-consistent everywhere" claim would be scientifically mis-specified and would likely fail on the panel's actual class composition.

**Exact missing scientific decisions (must be made BEFORE any pre-registration — an outcome-free decision task, e.g., "H01 Scientific Definition Lock"):**
1. **Asset-class re-scoping of H01 with pre-declared expected signs per class** (equities/indices: classic negative-shock asymmetry; gold/silver: inverse/positive-shock asymmetry; FX/crypto: declared direction or two-sided). Reject the universal "γ>0 everywhere" framing.
2. **Primary exposure variable** (proposed: standardized signed daily return; justification + frozen form).
3. **Primary response variable + horizon** (proposed: Δln σ² over a declared post-horizon; GJR-γ as secondary ONLY under a fully frozen spec). Ait–Sahalia et al. (2013) definitional framing: response is a vol-**change**, not a level.
4. **Normalization rule** (within-market only; specific variant frozen).
5. **Conditioning/confound controls** (lagged-vol conditioning; feedback caveat wording; extreme-move handling).
6. **Falsification decision rule + family** (primary statistic, per-class pass/fail definition, multiplicity control).
7. **Cross-era interpretation rule** (what counts as sign-consistent between HPD and M1 per class, given thin per-class N).
8. **HPD continuous-series handling** (rolls/gaps/quarantine exclusion) — frozen, not discovered.

**This audit authorizes NO experiment and NO protocol.** Decision is B, not A. If the definition-lock decisions are made cleanly, the pipeline proceeds to a **re-audit** → **pre-registration**. If H01 is not re-scoped, the Research Factory returns to candidate screening (H02/H05/H04 Level-2 co-candidates and Level-1 shortlist remain available). **H02/H05 are NOT selected here.**

---

## 18. Required Next Task

**H01 SCIENTIFIC DEFINITION LOCK** — an outcome-free task that:
- re-scopes H01 per asset class with literature-sourced expected signs (Baur 2012; Chen & Mu 2021; Black; Engle–Ng; GJR);
- freezes exposure, response, horizon, normalization, confounding controls, falsification rule, cross-era rule, and HPD handling;
- produces a pre-registration-grade definition for H01 **or** a written rationale that a class-specific subset (e.g., equity-index-only over HPD's `sp`/`cac` and M1's USATECHIDXUSD) is the honest scope;
- then a RE-AUDIT of the locked definition.

**If at any point the definition cannot be fixed without outcome knowledge: return to candidate screening (§3.4 pipeline).**

---

## 19. Integrity

- **Read-only audit.** No files were modified. No experiments, parameter-fitting (GARCH/EGARCH/GJR), backtests, clustering, or code were executed. External evidence was gathered via web search on 2026-08-13; all cited references were found in the search results of this audit session (Black 1976; Christie 1982; Nelson 1991; GJR 1993; Engle–Ng 1993; French–Schwert–Stambaugh 1987; Campbell & Hentschel 1992; Bekaert & Wu 2000; Hibbert et al. 2008; Ait-Sahalia, Fan & Li 2013; Moreira & Muir 2017; Chen & Mu 2020/2021 (J. Commodity Markets 22:100139); Baur 2012 (J. Alternative Investments 14(4)); Lucey & Tully 2006; Demiralay & Ulusoy 2014; Hasanhodzic & Lo 2011).
- **Data statements** are structural manifest checks only: M1 schemas (timestamp/open/high/low/close/volume; coverage ranges listed in §6), tick file sizes, HPD_MANIFEST columns/root dates. No effect was computed.
- **This audit does not inflate** the screening's score: total 40 → 32 with explicit per-axis deltas (§15).
- **Firewall:** only this artifact was created; no boe/**, assembly/**, research/engine/**, research/dataset/**, research/analytics/**, research/packaging/**, tests, StrategyManifest, Deployment, or closed governance files were touched and no such change is authorized by this audit.
- **Standing constitutional rules respected:** research never executes; the decision here is a research-domain classification; runtime/Deployment identity is untouched.