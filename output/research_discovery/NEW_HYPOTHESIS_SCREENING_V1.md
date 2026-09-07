# QuantForge — New Research Hypothesis Discovery & Screening V1

> **GOVERNANCE AMENDMENT (2026-08-24): ECONOMIC-FIRST PIPELINE INTEGRATION**
> Following the Program-Level Research Audit, all future candidate intake from hypothesis discovery must adhere to the `QUANTFORGE_RESEARCH_FACTORY_V2.md` operating doctrine.
> 
> Specifically:
> 1. Any future candidate must pass the **G1 (Economic Plausibility Screen)** and **G2 (Cheap Empirical Pilot)** before expensive research escalation (e.g. Parquet conversion, staged execution, definition lock).
> 2. The next legitimate task after this or any subsequent hypothesis screening is NO LONGER "independent research-readiness audit." The exact next tasks are:
>    - G1: Economic Plausibility Gate
>    - G2: Cheap Empirical Pilot
> 3. Only if both G1 and G2 pass may the candidate proceed to scientific validation. Candidate-selection language remains outcome-blind.

**Date:** 2026-08-13
**Scope:** DISCOVERY + SCREENING ONLY. No experiments, no clustering execution, no ML fitting, no protocols, no backtests, no BOE/Assembly/Deployment/StrategyManifest changes.
**Status:** COMPLETE — decision recorded below.
**Single decision format:** **A — CANDIDATE READY** (primary candidate recorded).

---

## 1. Scientific Rule Applied

This screening began with the required question:

> **"What observable market behaviour is sufficiently supported by independent evidence to justify a falsifiable research hypothesis?"**

— never with "what strategy can we make profitable?".

## 2. Current Project Position

- CASE1 / Mean-Reversion research line: **CLOSED — ECONOMICALLY NON-VIABLE** (DISC-021).
- Fixed 12/1 TSMOM research line: **CLOSED — NOT PROMOTABLE** after V2 (DISC-022); classified PARTIALLY REPRODUCED.
- Current milestone: **NEW HYPOTHESIS DISCOVERY & SELECTION**.
- THIS TASK produces exactly one artifact: `output/research_discovery/NEW_HYPOTHESIS_SCREENING_V1.md`.
- No experiment authorization is granted by this task, even for Level-2 candidates. The next tasks are: (1) independent research-readiness audit, (2) pre-registration, (3) independent protocol audit, (4) experiment.

## 3. Closed Research Lines (verbatim essential claims — any new candidate must be independent of these)

**Closed MR family (DISC-021) essential claims — NOT reopenable, in any recombination, at any horizon/logic:**
extreme displacement (deep z-score overextension), recoil, panic momentum, quick snap exits, MAE/MFE, MR regime/session filter, MR confirmation.

**Closed fixed 12/1 TSMOM family (DISC-022) essential claims — NOT reopenable:**
12-month trend persistence, 12/1 continuation (1-month skip, 1-month hold), same signal with a different optimizer, different weighting, different market selection, or a regime filter added to rescue 12/1.

**Independence rule applied:** A new hypothesis must not reduce to any of the above claims. Trend may appear in a hypothesis only if the scientific claim is *substantially different* (a different statistical object, causal claim, or state variable, not a re-specification of the closed signal).

## 4. Candidate Inventory

Candidates were generated from (a) the QuantForge research corpus (RESEARCH_DISCOVERY_DATABASE.md DISC-001..022, research journal evidence map) and (b) an external peer-reviewed literature scan (2026-08-13). Each candidate is a **scientific hypothesis**, not a strategy and not a method.

| # | Candidate (H0x, working label) | Scientific claim (observable behaviour) |
|---|---|---|
| H01 | Volatility response asymmetry (leverage effect) | The conditional volatility of a market responds asymmetrically to the sign of recent returns: a negative return shock raises forecast volatility more than a positive shock of equal absolute magnitude. |
| H02 | Volatility-state persistence / vol-managed scaling | Volatility strongly persists (vol clusters; shocks decay slowly), and the expected-return-per-unit-volatility is lower in high-volatility states, such that scaling exposure inversely to recent volatility changes the risk-return profile. |
| H03 | Market-state regime transitions (trend/vol/dispersion states) | Markets occupy recurring statistical states characterised by trend, volatility and dispersion; states persist, and transitions between states coincide with a measurable change in the forward-return distribution. |
| H04 | Cross-asset volatility spillover / connectedness | The volatility of a given market is in part forecastable from the recent volatility of other markets; connectedness is time-varying and rises in stressed periods. |
| H05 | Bear-market correlation / co-movement state dependence | Cross-asset co-movement is asymmetric: correlations between assets increase in falling (or high-volatility) market states relative to rising states. |
| H06 | Short-horizon (weekly) reversal in index futures | Weekly-horizon returns exhibit reversal (L1 negative autocorrelation) distinct from both intraday displacement-recoil and 12/1 continuation. |
| H07 | Turnover/volume–price interaction (transient impact) | Above-normal volume/turnover episodes are followed by measurable price implications consistent with transient price impact that partially reverses. |
| H08 | Cross-sectional dispersion across the futures panel | The dispersion of returns across the futures cross-section predicts future market-level volatility beyond each market's own history. |

**Screened OUT (with reason):**
- Variance risk premium / jump-tail premia (Bollerslev–Tauchen–Zhou 2009; Bollerslev–Todorov–Xu 2015) — requires **option-implied volatility**, which does not exist in the QuantForge data inventory. **Data incompatibility.**
- Intraday time-of-day / U-shape / session effects — overlaps the closed MR **"session filter"** essential claim; high independence rejection risk. Also intraday momentum (first half-hour predicts last half-hour; Gao et al.) is an intraday continuation claim adjacent to both closed families. **Deferred until a substantially different claim can be stated.**
- Structural-break detection, K-means, HMM, DBSCAN, PCA, random forests, XGBoost, neural nets, "change-point" — these are **methods, not hypotheses**; none is a candidate.
- "Model the market with clustering and make it profitable" — not a hypothesis (no falsifiable behavioural claim, cluster count/features/horizon undefined).
- Breakout / threshold-trigger behaviour — overlaps MR extreme-displacement and 12/1 trend families. **Dependence rejection.**
- Any "12/1 signal + vol/regime/session filter" — explicit forbidden rescue of the closed line. **Prohibited.**

## 5. Independence Assessment

| Candidate | Independent of closed MR family? | Independent of closed 12/1 TSMOM family? | Verdict |
|---|---|---|---|
| H01 | Yes — MR used volatility as a *condition on a discrete displacement signal* (DISC-002); H01 claims an asymmetric *property of the return distribution itself* (sign → conditional vol), a substantially different statistical object. | Yes — no trend claim, no return-persistence claim. | **INDEPENDENT** |
| H02 | Yes — vol persistence is a property of the return process, not an MR entry filter. | Yes — no 12-month prediction claim; if tested via scaling of a *neutral/no* base it is not a rescue of 12/1. Caveat: scaling the *closed 12/1 signal* is forbidden and will not be proposed. | **INDEPENDENT** (with explicit no-12/1-scaling caveat) |
| H03 | Reasonably — state/session overlap must be managed; the claim is about *state structure and transitions*, not displacement/recoil entries. | PARTIAL — the "trend" state dimension could degenerate into the closed 12/1 claim. Must be stated as: state membership is defined by multiple jointly-observed statistics and transitions are associated with forward-return-distribution change; **no 12/1 signal re-specification**. | **INDEPENDENT ONLY IF** trend is treated as a conditioning state variable, never as the 12/1 entry signal; see §11. |
| H04 | Yes | Yes | **INDEPENDENT** |
| H05 | Yes — correlation asymmetry is a joint-distribution property, not a displacement-entry claim. | Yes | **INDEPENDENT** |
| H06 | Horizon- and mechanism-distinct from extreme displacement/recoil (minutes) and snap exits; statistical object is weekly L1 autocorrelation. Reversal is, however, in the reversion *family* — must be defended as substantially different (horizon + mechanism). | Yes — opposite sign to continuation, distinct horizon. | **MOSTLY INDEPENDENT** (must be defended in pre-registration; kept in shortlist, not selected). |
| H07 | Yes | Yes | **INDEPENDENT** |
| H08 | Yes | Yes | **INDEPENDENT** |

## 6. Candidate Scoring Matrix (0–5 each)

A scientific evidence · B definition clarity · C parameter clarity · D data compatibility · E reproducibility · F OOS testability · G economic plausibility · H independence · I minimalism.

| # | A | B | C | D | E | F | G | H | I | **Total (max 45)** |
|---|---|---|---|---|---|---|---|---|---|---|
| H01 | 5 | 5 | 4 | 5 | 5 | 4 | 3 | 5 | 4 | **40** |
| H02 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 5 | 4 | **39** |
| H05 | 5 | 5 | 4 | 4 | 4 | 4 | 3 | 5 | 5 | **39** |
| H04 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 5 | 4 | **36** |
| H06 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | **34** |
| H07 | 3 | 3 | 4 | 5 | 4 | 4 | 3 | 5 | 4 | **35** |
| H08 | 3 | 4 | 4 | 3 | 4 | 4 | 3 | 5 | 4 | **34** |
| H03 | 3 | 2 | 1 | 5 | 3 | 3 | 3 | 2 | 2 | **24** |

Notes:
- Profitability is NOT a scoring axis. G (economic plausibility) is about whether a *true* version of the hypothesis could plausibly survive real execution costs — not about demonstrated returns.
- H03's low current scores reflect its current **definitional immaturity** (K, feature set, forecast horizon, and state operationalization are open by design), NOT a verdict on the phenomenon's existence.

## 7. Top-3 Deep Review

### H01 — Volatility Response Asymmetry (leverage effect)

- **Scientific statement (falsifiable):** *For each market in the panel, the coefficient on lagged negative return shocks in the conditional-volatility regression is positive and greater than the coefficient on lagged positive shocks of equal magnitude (asymmetry γ > 0), and this asymmetry is sign-consistent out-of-sample.*
- **Existing evidence:** Black (1976); Nelson (1991, EGARCH); Glosten–Jagannathan–Runkle (1993, GJR); Engle–Ng (1993). One of the most robust stylized facts in empirical finance: volatility rises on bad news. Widely replicated across equities, indices, FX, and commodities.
- **Data requirements:** Daily returns from `data/m1/{XAUUSD,EURUSD,BTCUSD,XAGUSD,USATECHIDXUSD}_M1.csv` (2021–2026, 5 markets) and daily/monthly series from the 28-market HPD panel (historical). No new downloads.
- **Potential experiment (high level, NOT authorized now):** pre-registered GJR/EGARCH asymmetric-volatility regression per market on a locked specification; primary statistic = asymmetry coefficient; sign/direction pre-registered; multiverse of admissible lag specifications fixed *before* results.
- **Falsification route:** γ ≤ 0, or asymmetry direction flips across eras/markets, or OOS test statistic fails the pre-registered decision rule.
- **Confounders:** volatility clustering itself (must condition on past vol, not just past shocks); leverage vs. vol-feedback interpretations (not resolved by the test — acceptable: the hypothesis is about the *statistical fact*, not the transmission channel); data errors in M1.
- **Economic risk:** the effect is a property of the volatility process, not directly a standalone trade; economic value is realised via risk conditioning. Not a failure — the hypothesis is a market-behaviour claim, not a strategy.

### H02 — Volatility-State Persistence / Vol-Managed Scaling

- **Scientific statement (falsifiable):** *Realized volatility is strongly persistent (first-order autocorrelation largely positive at daily/weekly horizon) AND inverse-volatility scaling of a fixed exposure improves the risk-return trade-off relative to unscaled exposure, consistent with expected returns not rising proportionally with vol.*
- **Existing evidence:** GARCH persistence (α+β ≈ 0.9–0.99 across markets; volatility clustering, Mandelbrot 1963; Cont 2005); Moreira & Muir (2017) "Volatility-Managed Portfolios" (NBER w22208) and related momentum-crash scaling work (Barroso–Santa-Clara 2015; Daniel–Moskowitz 2016). Evidence of vol persistence is overwhelming; evidence on the *scaling* element is strong but more debated.
- **Data requirements:** same M1 + HPD panels as H01.
- **Potential experiment:** pre-registered persistence test + a pre-registered scaling comparison on a *neutral fixed exposure* (never on the closed 12/1 signal) with observed-cost netting where costs are observed.
- **Falsification route:** no significant persistence; scaling provides no OOS improvement; scaling gains vanish net of real costs.
- **Confounders:** vol-of-vol; measurement of vol (realized vs. model); overfitting the scaling window.
- **Economic risk:** scaling raises turnover, which must be netted against observed contemporary costs (available) and historical costs (UNOBSERVED by design → sensitivity bands labelled ASSUMPTION, no invented spreads).

### H05 — Bear Market Correlation / Co-Movement State Dependence

- **Scientific statement (falsifiable):** *Conditional correlation between asset pairs is higher in down-market / high-volatility states than in up-market / low-volatility states, and this asymmetry is sign-consistent out-of-sample.*
- **Existing evidence:** Longin & Solnik (2001) — correlation increases in bear markets, not bull markets (extreme value theory, 5 largest markets, 1958–1996); Ang & Chen (2002) — asymmetric correlations of equity portfolios; Cappiello–Engle–Sheppard (2006) — asymmetric dynamics in global equity/bond correlations. Extremely well established.
- **State definition (needs pre-registration, not assumed here):** e.g., down-state = market return below a fixed percentile or below zero over the measurement window.
- **Data requirements:** cross-asset panels — contemporary M1 (5 markets, 2021–2026) and HPD (28 markets). No new downloads.
- **Potential experiment:** pre-registered state-conditional correlation test with a fixed state rule; direction (down-state correlation higher) pre-registered.
- **Falsification route:** no significant state-dependent difference, or direction flips across eras/markets.
- **Confounders:** volatility-correlation relationship (Longin–Solnik warn correlation and vol are spuriously related; must test correlation given trend, not vol); sample-dependence of tail definitions.
- **Economic risk:** correlation is a risk property; economic value is via diversification/risk management rather than a direct return edge.

## 8. Trend / Regime / K-Means Candidate Review (H03) — explicit as required

**Scientific statement (falsifiable, working form):** *Markets occupy a small number of recurring statistical states jointly characterised by trend, volatility, and dispersion; state membership is persistent (autocorrelated); and transitions between states coincide with a measurable change in the forward-return distribution (means and/or dispersion), consistent between historical and contemporary panels.*

**Status under the screening rules:** This is a legitimate REGIME/STATE hypothesis — NOT a method. It is NOT "(run K-means on the data)". It passes the "observable behaviour first" test: the behaviour is "market behaviour clusters into recurring, persistent statistical states."

**What is deliberately NOT assumed (per instruction — do NOT assume):**
- the number of clusters/states (K) — not assumed, not 2, not 3;
- the feature set (which statistics define the state) — not assumed;
- the forecast horizon — not assumed;
- whether the effect is profitable — not assumed;
- its direction — not assumed.

**Independence (the decisive gate):** The trend dimension of the state variable must not degenerate into the closed 12/1 claim. Safeguard rule for any future operationalization: *the state variable is a joint multivariate description (trend + vol + dispersion); the hypothesis under test is the association between state membership/transition and the forward-return distribution — never "state X signals the 12/1 entry direction."* Under that rule the candidate is independent of the closed lines. Without that rule it is a forbidden rescue. Verdict: **conditionally independent — condition must be encoded in the pre-registration.**

**Evidence:** strong that regime structure exists and is persistent (Hamilton 1989; Ang & Bekaert 2002 show a two-state model with a high-volatility, lower-mean regime and persistent transitions; Ang & Timmermann 2012 survey). Evidence is **thinner** for robust *forward-return* prediction from states — a well-known difficulty because state inference must be real-time (filtered, not full-sample smoothed) to be legitimate OOS.

**Critical methodological note (OOS integrity):** full-sample-smoothed regime classification leaks future information and is a classic source of false confidence. Any legitimate pre-registration must require **filtered/one-sided state inference** with the experimental partition (TRAIN/VALIDATION/TEST) declared before any inference. This is a well-understood requirement (not optional).

**ML / clustering safety rule (10 questions) — applied and recorded (this is the honest checklist for future work):**
1. Could a simpler statistical method achieve the same scientific purpose? — Possibly; a two/three-state description is testable with Markov-switching and threshold classifiers before any clustering. **Prefer the simpler method.**
2. Is the number of clusters specified a priori by theory or discovered by fitting? — Must be pre-registered as a hypothesis family, not discovered on the full sample.
3. Is the feature set chosen blind to the outcome? — Must be fixed before TRAIN.
4. Is state inference real-time (filtered), not full-sample? — Required.
5. Are partitions (TRAIN/VALIDATION/TEST) declared before any inference? — Required.
6. Is the forecast horizon pre-registered? — Required.
7. Is the evaluation statistic pre-registered? — Required.
8. Is drift over eras a confounder? — Must be controlled (the HPD historical and contemporary M1 panels are different eras; cross-era consistency is the decisive test — mirroring Condition 8 of the TSMOM gate).
9. Does the model select parameters by optimizing the outcome on the validation set? — Prohibited (validation overfitting — see RESEARCH_FACTORY_PIPELINE.md validation caveat).
10. Would the claim survive if the clustering were replaced by fixed thresholds? — A strong, honest pre-registration should include a threshold-sanity robustness check.

**Verdict on H03:** scientifically plausible, conditionally independent, **currently READINESS LEVEL 1** — it is a hypothesis, but not yet research-ready because its definitional degrees of freedom (K, features, horizon, state rule) must first be pinned by a pre-registration, and because filtered-inference discipline is required. **Do NOT run clustering in this task.** H03 is retained in the shortlist and is the recommended candidate to mature in a subsequent pre-registration task if the primary selection is not promoted.

## 9. Data Compatibility

| Data asset | Exists in inventory? | Used by |
|---|---|---|
| M1 OHLC — XAUUSD, XAGUSD, EURUSD, BTCUSD, USATECHIDXUSD (2021–2026) | yes | H01, H02, H04, H05, H06, H07, H08 |
| MT5 tick/bid-ask — same 5 markets (contemporary, incl. XAGUSD 2021-07→2026-07 observed spreads) | yes | cost netting for H01/H02/H06/H07 |
| HPD 28-market historical panel (1987→2002, 28 markets, monthly + daily front series) | yes (external temp path, referenced by TSMOM_V2) | H01, H02, H03, H04, H05, H06, H08 |
| AQR "Time Series Momentum Original Paper Data".xlsx (TSMOM factors, 1985+) | yes | context only (closed line) — not reused for a new hypothesis experiment |
| Options / implied-volatility series | **no** | required by VRP/tail candidates → **EXCLUDED** |
| Broad equity cross-section (hundreds of stocks) | **no** | required by the canonical dispersion-evidence design → H08 downgraded (28-market panel is the only usable cross-section) |

No new data downloads authorized or needed.

## 10. Economic Screening

- **Observed contemporary costs:** MT5 half-spreads exist for the 5 contemporary markets; any annualised effect must be netted against observed spread costs (Option-A accounting precedent from TSMOM_V2). P90-cost checks required (XAGUSD precedent: median 9 bp round trip, P90 11 bp — see DISC-021).
- **Historical costs:** UNOBSERVED unless genuine. No invented spreads. Any historical experiment must report gross + sensitivity bands {0,5,10,20,50} bp labelled **ASSUMPTION** (TSMOM_V2 precedent).
- **Hypothesis-level economics:** H01/H05 are distributional properties; their economic plausibility is via risk conditioning / risk management, and the experiment must not require a positive net edge to be "confirmed" — the hypothesis is about behaviour, and confirmation is a statistical decision on the stated statistic, not a Profit Factor.
- **Gate:** tiny effects vs realistic costs → downgrade. H06/H07 reversed effects would be small vs weekly turnover; kept in shortlist only.

## 11. Research-Readiness Levels

| Level | Definition | Candidates |
|---|---|---|
| 0 | Narrative only | — |
| 1 | Hypothesis stated | H03, H06, H07, H08 |
| 2 | Research-ready (pre-registrable) | **H01**, H02, H05, H04 |
| 3 | Experiment-ready | — (next stage after pre-registration + protocol audit) |
| 4 | Promotion candidate | — |

Only Level 2+ may proceed to pre-registration. **NO protocol is written in this task** for any candidate (including Level 2).

## 12. Selected Candidate or No-Candidate Decision

### DECISION: **A — CANDIDATE READY**

**Primary candidate:** **H01 — Volatility Response Asymmetry (leverage effect)**

- **Hypothesis (falsifiable):** conditional volatility responds more to negative than to positive return shocks of equal magnitude (γ > 0 in GJR/EGARCH form), sign-consistent between the historical (HPD) and contemporary (M1) panels.
- **Independence:** independent of both closed research lines (MR essential claims and 12/1 TSMOM essential claims); volatility seen as a *property of the return distribution* rather than a filter on a displacement/discrete signal.
- **Evidence:** among the most robust established findings in empirical finance (Black 1976; Nelson 1991; GJR 1993; Engle–Ng 1993; broadly replicated, cross-market).
- **Data:** M1 daily (5 markets, contemporary) + HPD (28 markets, historical). No new downloads.
- **First experiment question (for the next task, NOT executed here):** *"Within the QuantForge M1 and HPD panels, is the asymmetry coefficient γ reliably positive and sign-consistent across markets and eras under the pre-registered GJR/EGARCH specification, with OOS direction preserved?"*

**Co-research-ready candidates (Level 2, not selected):** H02 (vol-state persistence / scaling) and H05 (bear-state correlation); H04 (spillover) borderline Level 2.

**Shortlist retained (Level 1):** H03 (regime/trend — needs pre-registration to pin K/features/horizon and to encode the independence safeguard), H06, H07, H08.

**Intentionally NOT selected:** H03-as-selection would have been forced given its open definitional degrees of freedom; per the instruction "do not force selection", the candidate with the cleanest, most evidence-backed, fully-defined, independent, pre-registrable claim (H01) is selected instead.

## 13. Why the Selection Is Not Curve-Fitted

- No parameter was tuned; no backtest was run; no outcome was inspected.
- H01's statistics (asymmetry coefficient, sign, cross-era consistency) are pre-registrable; the specification family is chosen from the established literature (GJR/EGARCH), which predates and is independent of this project's data.
- Cross-era consistency (HPD historical vs M1 contemporary) is the decisive test, mirroring the discipline that failed Condition 8 for TSMOM — the design forces the candidate to survive an *era shift*, the standard that the previous line could not meet.
- The decision is an evidence-weighted selection from a pre-declared shortlist, with the closed-line independence rule applied before scoring. H01 won on A (evidence), B (definition clarity), D/F (data and OOS), and H (independence) — the properties that resist curve-fitting.

## 14. Exact Next Task

**Independent Research-Readiness Audit** of H01 (and optionally H02/H05 in the same audit), covering: hypothesis statement preciseness, pre-registration readiness, data-panel verification (including HPD daily-series availability and M1 integrity), and the economics screen. Only after a clean audit does the pipeline move to **Pre-Registration** → **Independent Protocol Audit** → **Experiment**.
**This task authorizes no experiment and no protocol.**

## 15. Runtime Firewall

- No modifications to `boe/`, `research/lifecycle/`, `research/engine/`, `research/dataset/`, Strategy Assembly, Deployment, StrategyManifest, or any frozen contract.
- No scripts, datasets, ML models, cluster files, backtests, protocols, or result files were created.
- The only artifact produced by this task is this screening document.
- No TEST partition is reused, no closed candidate is revived.
- Next-task handoff: SESSION_HANDOFF.md and ROADMAP.md CURRENT MILESTONE may reference this decision when the next task is authorized.

## 16. Integrity

- All literature cited above (Black 1976; Nelson 1991; Glosten–Jagannathan–Runkle 1993; Engle–Ng 1993; Mandelbrot 1963; Cont 2005; Moreira–Muir 2017; Barroso–Santa-Clara 2015; Daniel–Moskowitz 2016; Longin–Solnik 2001; Ang–Chen 2002; Cappiello–Engle–Sheppard 2006; Hamilton 1989; Ang–Bekaert 2002; Ang–Timmermann 2012; Diebold–Yilmaz 2009/2012) reflects the external evidence scan performed on 2026-08-13 via the web-search tool; where a claim's empirical basis is in QuantForge files, the specific path is cited.
- No profitability claim is made for any candidate; H01/H05 are market-behaviour hypotheses about the return/volatility process and the joint return distribution.
- Screenings, scores, readiness levels, and the decision are recorded here and are immutable inputs to the next task (research-readiness audit).