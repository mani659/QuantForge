# QUANTFORGE — EVENT STUDY PROTOCOL — TSMOM V2 (DRIFT-CONTROLLED IDENTIFICATION STUDY) — PRE-REGISTRATION

**Protocol version:** 2.0.0 (initial pre-registration; no amendments)
**Status:** FROZEN PRE-REGISTRATION — created before any V2 outcome inspection.
**Date of freeze:** 2026-08-13
**Project state:** QuantForge Engine COMPLETE/FROZEN; Strategy Assembly V1 FROZEN; Mean-Reversion CLOSED (DISC-021); TSMOM V1 EXECUTED — Scientific INCONCLUSIVE / Economic NOT CONFIRMED; V2 resolves the V1 identification failure (TSMOM signal value vs unconditional drift).
**Authorized action:** design and freeze this protocol ONLY. No experiment is executed by this artifact. No outcome is inspected. No script, dataset, or result file exists at pre-registration time.
**Experiment output root (future, at execution):** `output/tsmom_v2/`
**Integrity rule:** until this protocol passes an independent read-only audit, no outcome data, event dataset, result table, or analysis script may exist anywhere in QuantForge.

---

## 0. Preamble — Why V2 Exists

V1 asked: *does the 12/1 TSMOM strategy have positive returns?* The pooled positive point estimates could not be separated from unconditional market drift / long-biased composition; the formal NC2 (6-month-shifted signal) produced a stronger association than the primary result. V2 therefore changes the scientific question, not the mechanism:

> **Controlling for unconditional market drift and long-biased sample composition, does the fixed 12/1 TSMOM signal add incremental predictive value above a same-universe, same-weight all-long benchmark?**

The mechanism (12-month lookback, skip most recent month, sign long/short, one-month hold, monthly rebalance, inverse-vol scaling `0.40/σ_ann` uncapped) is carried over exactly from V1 and is NOT altered anywhere in this protocol. V2 adds: (a) a materially broader validated historical panel (28 core US futures markets, ~1987–2002); (b) a same-universe same-weight all-long drift benchmark; (c) incremental (signal-minus-drift) statistics; (d) dependence-aware paired inference; (e) identification-relevant negative controls replacing the contaminated V1 NC2; (f) a strict two-layer historical/contemporary structure that is never pooled.

---

## 1. Scientific Question (primary, fixed)

> **Operating hypothesis (H1):** the fixed 12/1 TSMOM signal adds incremental predictive value above a same-universe, same-weight all-long benchmark, i.e., the direction choice (long vs short) produces positive excess return over holding the identical universe long.
>
> **Null (H0):** mean incremental signal value ≤ 0 — the direction choice adds no return above the all-long benchmark.

Two structural hypotheses are registered but NOT treated as confirmed:
- **H2 — Drift:** a substantial component of observed TSMOM portfolio return is explained by unconditional market drift and is captured by the all-long benchmark.
- **H3 — Composition/Regime:** apparent TSMOM results are affected by market composition and regime structure, so incremental value must be evaluated relative to the benchmark, not against zero alone.

The central change from V1 (mandatory): the confirmatory inference is on the **incremental signal statistic** `ΔΠ(m)` (TSMOM portfolio minus all-long portfolio), not on raw TSMOM portfolio return.

## 2. Design Type

- Type B — time-series predictive-return study with a fixed monthly assessment population (one assessment per market per position month). No event-trigger machinery is reused from the Mean-Reversion line.
- The population of market-months is defined entirely from the fixed data window (Section 5) and the paused-12-month lookback geometry (Section 4). No cell is selected after outcomes.

## 3. External Scientific Anchors (fixed, unchanged from V1)

- Primary: Moskowitz, Ooi, Pedersen (2012), *Time Series Momentum*, JFE 104(2):228–250.
- Secondary: Hurst, Ooi, Pedersen (2017), *A Century of Evidence on Trend-Following Investing*, JPM 44(1):15–29.
- V1 identification-failure register (the reason this protocol exists): `SCIENTIFIC_REPORT_TSMOM_V1.md` (inconclusive pooled F1 CI including 0; formal NC2 stronger than primary; long-biased composition XAUUSD & USATECHIDXUSD). The external continuation decision memo and external-data suitability audits (AQR/MOP structural audit; external raw TSMOM source discovery; TurtleTrader HPD sample verification & license due-diligence) were reviewed from their external-context records; their conclusions are incorporated: (i) HPD is a conditionally accepted 28-core-market panel; (ii) license PENDING; (iii) cost data unobserved.
- The mechanism `12/1` is **not** fitted here; it comes from published literature and V1 and is frozen.

## 4. Fixed TSMOM Mechanism (identical to V1; no tuning allowed)

For market *i*, position month *m* (`C_{i,m}` = month-end close, defined as the close of the last populated trading day of calendar month *m* on the continuous front* series):

1. **Monthly return:** `R_{i,m} = C_{i,m}/C_{i,m-1} − 1`, defined only when both boundary closes exist.
2. **Lookback cumulative return (signal input):** `L_{i,m} = Π_{k=m-12}^{m-2}(1+R_{i,k}) − 1` (12 months, skipping month *m−1*).
3. **Signal:** `S_{i,m} = +1` if `L_{i,m} > 0`, else `−1` (zero ⇒ −1; fixed for determinism).
4. **Ex-ante vol:** `σ_ann_{i,m}` = annualized stdev of daily returns over the 21 populated trading days ending at assessment month-end *m−1* (`std × sqrt(252)`); if fewer than 5 daily returns exist ⇒ no assessment for month *m* (counted).
5. **Position weight:** `w_{i,m} = 0.40 / σ_ann_{i,m}`, **uncapped** (V1 primary; capped variant is an exploratory sensitivity only).
6. **TSMOM position:** `p_{i,m} = w_{i,m} · S_{i,m}`.
7. **TSMOM contribution:** `r_tsmom(i,m) = p_{i,m} · R_{i,m}`.
8. **All-long benchmark position (same market, month, weight, availability):** `p^{long}_{i,m} = w_{i,m}` (always long; identical vol weight).
9. **All-long contribution:** `r_long(i,m) = w_{i,m} · R_{i,m}`.
10. **Incremental (signal-minus-drift) contribution:** `Δr(i,m) = r_tsmom(i,m) − r_long(i,m) = w_{i,m}·(S_{i,m}−1)·R_{i,m}`.
11. **Monthly portfolio statistics:** `Π_tsmom(m) = mean_i[r_tsmom(i,m)]`, `Π_long(m) = mean_i[r_long(i,m)]`, `ΔΠ(m) = Π_tsmom(m) − Π_long(m)` — means across markets with an eligible assessment in month *m* (identical eligibility for all three).

**FORBIDDEN:** any new lookback; any new horizon; any market-selection rule; any regime filter; any volatility model change; any parameter grid as primary; any imported indicator; any outcome-driven exclusion.

## 5. Fixed Data Universe (read from acquisition fingerprint/manifest)

The universe and dates are taken verbatim from the Full TurtleTrader HPD Acquisition & Ingestion Validation V1 outputs:
- **Fingerprint/manifest:** `C:\Users\User10\AppData\Local\Temp\quantforge_tsmom_hpd_full\HPD_MANIFEST.csv`, `HPD_CONTRACT_HASHES.csv`, `FINAL_CLASSIFICATION.csv`, `PER_MARKET_VALIDATION.csv`, `front_<root>.csv` (28 continuous series), and `INGEST_PIPELINE_SPEC_v1.md`.
- **Core US identification universe (28 markets):**
  `ad (AUS$), bp (GBP), c (Corn), cd (CAD), cl (Crude), cr (CRB Index), ct (Cotton), dx (Dollar Idx), ed (Eurodollar), fc (Feeder Cattle), gc (Gold), hg (Copper), ho (Heating Oil), jo (Orange Juice), jy (Yen), kc (Coffee), lh (Live Hogs), o (Oats), pa (Palladium), pb (Pork Bellies), pl (Platinum), s (Soybeans), sb (Sugar), sf (Swiss Franc), si (Silver), sp (S&P 500), us (T-Bonds), w (Wheat)`.
- **Asset classes (9 groups):** FX {ad,bp,cd,dx,jy,sf} · Metals {gc,si,hg,pl,pa} · Grains {c,o,s,w} · Softs {ct,jo,kc,sb} · Livestock {fc,lh,pb} · Energy {cl,ho} · Rates {ed,us} · Equity index {sp} · Index {cr}.
- **Historical common identification window (from manifest):** **1987-01-13 → 2002-08-30** (28/28 markets present within this window; earliest common start 1987-01-13 = ad; latest common end 2002-08-30 = cr). Expected usable **position months** ≈ 175 (Feb-1988 … Aug-2002) after the 13-month warm-up (12-month lookback + most-recent-month skip); exact counts re-derived deterministically at execution from the manifest—no discretionary change.
- **Exclusions are PRE-DEFINED from the acquisition validation, never outcome-based:**
  - Non-US, separately classified (NOT part of the 28-market core; excluded here because universe construction must be the validated core panel): `aor` (All Ordinaries), `cac` (CAC 40), `lj` (Gilt), `ll` (Sterling 3M — **byte-identical duplicate of Gilt, provider error; unusable**).
  - `sf` malformed rows: the broken contract file (`SF00M.txt`, truncated header) contributes 398 malformed rows; these are dropped by the pre-registered parser (documented count) and do not enter the continuous series.
  - No other market may be removed for any reason.
- **Contemporary replication panel (separate, never merged):** QuantForge `data/m1/{XAUUSD,EURUSD,BTCUSD,XAGUSD,USATECHIDXUSD}_M1.csv` (2021–2026; M1 closes aggregated to daily/monthly exactly as V1 §6; observed MT5 bid/ask for 4 markets; EURUSD spread UNOBSERVED, V1-assumed 0.1 bp/side). Expected usable position months ≈ 48–53 per market (V1 universe); the contemporary panel is a **secondary replication layer only**.

## 6. Unit of Analysis and Chronological Partitions

- **Unit:** market-month (assessment i,m as Section 4).
- **Historical partitions (over the ordered list of union position months of the common window, T ≈ 175):**
  - TRAIN = first 70% (A = floor(0.70·T));
  - VALIDATION = next 15% (B = floor(0.85·T));
  - TEST = final 15% (months B+1…T) — **pre-authorized single-use holdout**.
- **F1 (primary, statistical power):** pooled `ΔΠ(m)` over TRAIN+VALIDATION (first 85%). Expected `T_F1 ≈ 148` months.
- **F2 (historical TEST corroboration):** pooled `ΔΠ(m)` over TEST (expected ≈ 27 months ≥ block length 12, so the F1 multivariate block bootstrap is used; single use).
- **Layer B (contemporary replication):** pooled `ΔΠ(m)` over the 2021–2026 panel (expected ≈ 50 position months). Pre-registered; used once; identical mechanism; **never** conditions historical choices.
- Rules: VALIDATION is never inspected-and-retuned; TEST is never revisited; no cell selection anywhere; historical and contemporary are **never pooled into one statistic** (source/universe construction differs — kept separate by design, not to inflate N).

## 7. Primary Confirmatory Specification and Statistic

- **Primary statistic:** `mean_ΔΠ = mean over m in F1 of ΔΠ(m)` (pooled incremental monthly signal value), computed gross. Reported: mean, median, 95% CI (block bootstrap), one-sided p-value, effective independent signal-state count, signal run count, mean run length, proportion of months with `ΔΠ(m) > 0`.
- **Same-universe benchmark rule (mandatory, pre-registered):** every TSMOM observation has its all-long observation using exactly the same market, month, volatility weight, and data availability. Benchmark may not add markets, remove markets, change weights, use hindsight, use a different cost assumption, or use a different history. If a market-month is absent, BOTH the TSMOM and benchmark observations for that market-month are absent.
- **Confirmatory family (multiplicity; Holm, α=0.05, family size = 2):**
  - **F1** — historical incremental: pooled mean `ΔΠ(m)` over TRAIN+VALIDATION (gross).
  - **Layer-B** — contemporary incremental: pooled mean `ΔΠ(m)` over the 2021–2026 panel (gross).
  - Both one-sided in the hypothesized positive direction; Holm-adjusted p-values reported for both.
- **Corroborative, NOT in the confirmatory family:** F2 (historical TEST, single use), per-market and asset-class results, all sensitivities and negative controls (never enter the verdict gates).

## 8. Statistical Inference (dependence-aware, pre-registered)

- **Dependence structure:** monthly market-month rows exhibit (a) serial dependence from overlapping 12-month lookbacks and persistent sign runs; (b) contemporaneous cross-market dependence (shared episodes). Both are preserved by the inference below.
- **PRIMARY inference — multivariate calendar block bootstrap (identical draw mechanics to V1 §11, applied to the historical panel):**
  1. **Union panel:** ordered F1 calendar months with ≥1 contributing market (ragged representation as V1; no synthetic months).
  2. **Block length (FIXED, justified pre-outcome):** `L = 12` months. Justification: the signal's informational horizon is 12 months (lookback window m−12…m−2); serial dependence in the monthly series is induced by 12-month overlapping construction windows, so blocks must be at least the construction horizon. L=12 is adopted because it equals that horizon (NOT merely because V1 used 12; V1's L was the same horizon argument). `L = 12 < T_F1 ≈ 148` ⇒ ≈137 overlapping blocks, sufficient for B=10,000 with replacement.
  3. **Draw:** sample overlapping 12-month calendar blocks with replacement until concatenated length ≥ `T_F1`; truncate to first `T_F1` months. Seed fixed: **20260813**.
  4. **Multivariate preservation:** each resampled calendar month carries ALL markets' observations for that original calendar month (a month-vector); absence contributes nothing.
  5. **Statistic per replicate:** compute `ΔΠ(m)` for every resampled month (using the SAME paired structure: Π_tsmom, Π_long, ΔΠ from identical market sets), then `mean_ΔΠ` over the resampled F1 panel.
  6. **Replicates:** B = 10,000. 95% percentile interval + one-sided p = fraction of replicates with `mean_ΔΠ ≤ 0`.
- **F2 (historical TEST, T≈27 ≥ 12):** same mechanics on the TEST union panel; L=12 (16 blocks); report point estimate, sign, CI, one-sided p. Corroborative only.
- **Layer B (contemporary, T≈50 ≥ 12):** same mechanics on the contemporary panel; L=12; B=10,000; seed **20260814**. Corroborative as a replication of direction, primary as the confirmatory family member via its p-value/CI.
- **Paired-bootstrap rule (mandatory):** TSMOM portfolio, all-long portfolio, and incremental difference are computed from the SAME replicate resampled blocks — never bootstrapped independently.
- **Cross-market reporting:** pairwise correlation matrix of `r_tsmom(i,m)` and of `R(i,m)` across markets (aligned months); effective market count; concentration by asset class. **The ≈4,900 market-month rows are NOT treated as independent observations.**

## 9. Signal Run / Independence Analysis (mandatory before interpretation)

Report per market and pooled:
- number of signal flips (S transitions) per market; mean/median/max run length; pooled flip count;
- effective independent-state estimate = pooled flips (V1 precedent: 219 assessments / ~21 flips);
- explicit comparison: **V1 219 assessments / ~21 flips** vs the V2 historical panel dimensions (expected >~300 pooled flips across 28 markets × ~175 months).
- Do not claim power from total row count alone.

## 10. Negative Controls (replace contaminated V1 NC2; fixed before outcomes)

- **NC1 — paired direction permutation:** within each market, preserve the market's ordered signal run-length structure and long/short counts exactly, but randomize which calendar months receive the direction, while preserving (i) the market-month return panel and (ii) within-market contemporaneous calendar structure. Implementation: circular rotation of each market's signal sequence over its own position months (random uniform shift per market), keeping returns pinned to their calendar months. Recompute the paired `ΔΠ(m)` with the rotated signals (all-long book unchanged by construction). B=10,000; seed **20260815**. Expected null: `mean_ΔΠ ≈ 0`.
- **NC2 — drift benchmark = central scientific null:** the all-long book is the null; its paired inference is the primary test (Section 8). Reported as a distinct benchmark, not as evidence of signal.
- **NC3 — long-lag shift (extends beyond signal persistence):** apply the month-*m* signal to outcome month *m+LAG*, truncated at window end. `LAG = 24` months — **fixed, justified pre-outcome**: 24 > 12 (construction horizon) and > plausible sustained signal run lengths; NOT the V1 6-month shift (which overlapped the 12-month lookback). Expected null. B=10,000; seed **20260816**.
- **NC4 — calendar block null (timing-scrambled, cross-market preserving):** resample calendar blocks exactly as the primary bootstrap, but replace each drawn block's signal matrix with the signal matrix of a randomly drawn *different* original block (returns stay in place; multivariate structure per block preserved; signal→return link broken at block scale). B=10,000; seed **20260817**. Expected null.

All controls are fixed now; no control may be added, removed, or re-weighted after outcomes.

## 11. Market / Asset-Class Diagnostics (exploratory, non-confirmatory)

Per market: incremental mean `mean_m Δr(i,m)`, sign, sample size, signal flips, CI, asset class.
Asset-class aggregates: FX; Metals; Energy; Grains; Softs; Livestock; Rates; Equity index; Index; plus the four canonical classes (FX / Commodities & metals / Equity / Rates).
Rules: no market is selected or removed because its result is negative; the 28-market universe is fixed. Leave-one-market-out and leave-one-class-out influence checks are reported as robustness ONLY.

## 12. Drift / Composition Diagnostics (diagnostics only, never selection tools)

- D1 All-long benchmark `Π_long(m)` — primary drift measure.
- D2 Incremental `ΔΠ(m)` — primary signal-minus-drift measure.
- D3 Sign contribution — the effect of direction choices relative to the benchmark.
- D4 Long exposure — % of market-months where `S=+1`.
- D5 Market contribution to `ΔΠ`.
- D6 Asset-class contribution to `ΔΠ`.

## 13. Economic Accounting (two distinct cost regimes — never equated)

### 13a. Historical HPD panel — **COST DATA UNOBSERVED**
- The HPD archive has **no bid/ask, spread, commission, or transaction-cost series** (volume & open interest only). Verified by the acquisition audit (`FINAL_REPORT_V1.md` §17).
- **No synthetic spread may be invented.**
- Treatment: the primary scientific identification is **gross** `mean_ΔΠ`. Economic viability for the historical panel is reported as **UNRESOLVED** unless legitimate historical cost evidence is separately obtained (e.g., archived futures manuals, exchange margin/commission tables, academic transaction-cost series) — none is assumed now.
- Pre-registered sensitivity-only cost bands (ONLY as a reported table, never a verdict and never part of the confirmatory family): one-way cost `h ∈ {0, 5, 10, 20, 50}` bp applied dimensionally as `Σ_m Σ_i |Δp_{i,m}|·h` per V1.0.3 Option-A accounting (`π_net = mean_i(p·R − |Δp|·h)`, final-close term included). Each row labelled ASSUMPTION.

### 13b. Contemporary QuantForge panel — observed MT5 costs
- Reuse V1.0.3 **Option A** dimensional accounting (`C_{i,m} = |Δp_{i,m}|·h_{i,m}` + final-close term) with **observed** matched MT5 bid/ask half-spreads for BTCUSD, XAGUSD, XAUUSD, USATECHIDXUSD; EURUSD spread **UNOBSERVED** → 0.1 bp/side assumption with band {0.1, 0.5, 1.0, 2.0}.
- Net incremental: `ΔΠ^net(m) = mean_i[Δr(i,m) − (C_tsmom(i,m) − C_long(i,m))]`.
- The two cost regimes are reported separately and never compared as if equivalent.

## 14. Data-Quality Gates (required before execution proceeds)

- Validated source manifest (SHA-256 for all 32 archives) present.
- Per-contract SHA-256 fingerprints recorded (`HPD_CONTRACT_HASHES.csv`).
- No silent market removal; exclusions are exactly those listed in Section 5 and are logged.
- Quarantined markets explicitly listed (aor, cac, lj, ll; ll duplicate noted).
- Fixed roll methodology = ratio back-adjustment per `INGEST_PIPELINE_SPEC_v1.md` §4.
- Fixed panel construction (front_<root>.csv as produced by the acquisition task).
- Fixed missing-data policy (V1 §6: a market with no data in a month simply has no assessment; counts reported).
- Reproducible monthly aggregation from month-end closes of the continuous series.
- If a source market fails the acquisition/ingestion validation after this freeze, it is excluded BEFORE execution with a logged reason, never outcome-based.

## 15. TEST Protection and Stopping Rules

**TEST (F2) protection:** single authorized use; never revisited after the pre-registered verdict; never used to select parameters. Any need to reuse TEST ⇒ new protocol version, prohibited within V2.

**Execution STOPS immediately and reports the ambiguity without improvising if:**
- roll ambiguity reappears at execution;
- panel construction requires discretionary market exclusion;
- data leakage is discovered;
- a statistical method is under-specified at execution;
- a cost-accounting ambiguity appears;
- benchmark units become inconsistent (`w`, `p`, `Δr` dimensional mismatch);
- the external source changes meaning (HPD page / files differ from fingerprints);
- any parameter must be chosen after inspecting results;
- the TEST definition changes;
- a new methodological choice becomes necessary.

## 16. AQR/MOP and MT5 Constraints

- AQR workbook: external contextual benchmark / published-factor reference ONLY; never a member of the test universe (no raw market prices).
- MT5/Exness: no historical-HPD extension; contemporary broker cost validation, contemporary replication, and future-forward evidence only. No broker CFD/spot substitution for historical futures.

## 17. Research-to-Runtime Firewall

This protocol authorizes **research only**. It does NOT authorize: `MeanReversionDetector` or `TSMOMDetector`; BOE changes; StrategyManifest changes; Assembly/Deployment changes; runtime TSMOM parameters; production thresholds; live trading; portfolio deployment. A successful V2 requires a separate **Scientific Specification Readiness Review** before any runtime promotion.

## 18. Power / Sample Adequacy (outcome-blind estimate; no V2 outcomes)

Based only on data dimensions and mechanism geometry:
- Historical panel: ≈28 markets × ≈175 position months ≈ **≈4,900 market-months**; F1 window ≈148 months; expected pooled signal flips ≈300+ (vs V1's 21) — a ~15× expansion of independent signal-state information.
- Effective independent blocks at `L = 12`: `⌈148/12⌉ ≈ 13` overlapping-draw information units at the portfolio-month level; the confirmatory load rests on the block bootstrap, which respects the true (lower) independence — the report must frame power in block units, not row counts.
- Contemporary replication: ≈5 markets × ≈50 months (V1 universe), reported as replication only.
- Expected CI precision (dimension-based, illustrative): with ~148 portfolio-months and realistic cross-market diversification, a one-sample pooled `mean_ΔΠ` standard error on the order of a few tenths of a percent per month is plausible; power detection of an effect ≈0.5%/month (≈6%/yr) should be achievable if the effect is real and not consumed by drift; the protocol makes no claim that an effect exists — it only establishes that the panel is materially larger and demonstrably better-conditioned than V1.
- If the historical panel still proves underpowered after execution, that must be stated explicitly; it does not change the verdict categories.

## 19. Verdict / Promotion Criteria (pre-registered)

### Scientific identification (historical, Layer A — primary)
TSMOM is promoted **only if ALL** of:
1. historical incremental `mean_ΔΠ > 0` (F1, TRAIN+VALIDATION);
2. F1 95% CI lower bound > 0;
3. F1 one-sided p passes the Holm-adjusted threshold for the family {F1, Layer-B} at α = 0.05;
4. signal contribution is positive relative to the all-long benchmark (by construction, 1–3 assert the same incremental object; redundant restatement is retained for audit clarity);
5. result is not dominated by a single market (leave-one-out robustness);
6. result is not driven solely by one asset class (leave-one-class-out robustness);
7. result survives the negative-control framework (NC1/NC3/NC4 nulls do not reproduce the incremental effect);
8. historical result remains **directionally consistent** (same sign; does not require contemporary significance) in the contemporary replication layer (Layer B).

### Failure
If any of 1–8 fails: **TSMOM remains UNRESOLVED / NOT ESTABLISHED.** Promotion is never based on positive absolute TSMOM returns.

### Economic layer
- Historical panel: **UNRESOLVED by default** (cost data unobserved); gross identification is the primary scientific object; any cost figure is derived solely from the pre-registered assumption bands (Section 13a) and cannot be a verdict.
- Contemporary panel: report net incremental CI with observed MT5 costs under Section 13b; economic gate for the contemporary layer = net 95% CI lower bound > 0.

## 20. Multiplicity (fixed)

Confirmatory family = {F1 historical incremental, Layer-B contemporary incremental}; family size 2; Holm α = 0.05; both one-sided. Per-market, asset-class, F2, controls, and sensitivities are exploratory and excluded from the verdict. No sensitivity may select the primary result.

## 21. Reproducibility Requirements (execution-time, to be recorded later — NOT performed now)

- Record SHA-256 of all 28 `front_*.csv` + manifest CSVs; record the 5 contemporary M1/tick fingerprints (V1 metadata already pins them).
- Record python/pandas/numpy/scipy versions; seeds (20260813 F1, 20260814 Layer-B, 20260815 NC1, 20260816 NC3, 20260817 NC4); B=10,000; L=12; LAG=24; cost conventions (bp=0.0001; Option A).
- Artifacts planned at execution (created ONLY after the independent read-only pre-registration audit): `experiment_metadata_TSMOM_V2.json`, `incremental_monthly_TSMOM_V2.csv`, `assessment_events_TSMOM_V2.csv`, `bootstrap_TSMOM_V2.csv`, `results_TSMOM_V2.json`, `SCIENTIFIC_REPORT_TSMOM_V2.md`.
- No hidden manual filtering; every exclusion counted and reported; the experiment must be replayable from this protocol alone.

## 22. Explicit Non-Goals (at pre-registration)

- No experiment execution; no outcome inspection; no TSMOM return or drift benchmark computed from observed outcomes; no regression; no protected-TEST consumption.
- No detector implementation; no BOE/Assembly/Deployment/StrategyManifest change; no runtime semantics; no crash-avoidance; no optimization grid; no best-cell selection; no added markets; no Mean-Reversion machinery reuse.
- No modification of SESSION_HANDOFF or any frozen contract.
- No V2 outcome artifact exists at pre-registration time.

## 23. Outcome-Blind Self-Audit (performed, see Section 24)

1. 12/1 mechanism unchanged from V1 — PASS (Section 4 is V1 verbatim geometry).
2. All-long benchmark uses identical market/weight/availability observations — PASS (Section 4.8–4.11, Section 7).
3. Incremental statistic explicitly defined — PASS (Δr, ΔΠ).
4. Bootstrap preserves paired structure — PASS (Section 8.5–8.6).
5. Cross-market dependence preserved — PASS (month-vector blocks).
6. No parameter tuning — PASS (Section 1/4; sensitivities explicitly exploratory).
7. Negative controls not contaminated by signal persistence — PASS (NC3 LAG=24 > construction horizon; NC1 rotation preserves structure; NC4 block-level mismatch).
8. Historical and contemporary samples not silently merged — PASS (Section 6 Layer structure; explicit never-pool rule).
9. Historical costs not fabricated — PASS (Section 13a COST DATA UNOBSERVED; assumption bands labelled).
10. HPD factor data not treated as raw market data — PASS (CRB Index `cr` retained as an index in the universe per the acquisition classification; no AQR factor member).
11. TEST remains protected — PASS (Section 15 single-use).
12. No BOE/runtime change implied — PASS (Section 17).
13. No outcome inspected — PASS (only manifest dimensions and formats read).
14. No experiment executed — PASS (no script/run in this task).

## 24. Deliverables Constraint

The ONLY artifact created by this task is this protocol: `output/tsmom_v2/EVENT_STUDY_PROTOCOL_TSMOM_V2_DRIFT_CONTROL.md`. No script, no data transformation, no result file, no event dataset, no benchmark result, no outcome report exists in `output/tsmom_v2/` or anywhere else at pre-registration time (verified by this task).

## 25. Next Task (sole authorized successor)

**INDEPENDENT READ-ONLY AUDIT OF TSMOM V2 PRE-REGISTRATION.** No experiment execution, no outcome inspection, and no protocol modification are authorized by the audit beyond the read-only review and the audit deliverable.

---

*Frozen at 2026-08-13 as the sole pre-registration artifact for TSMOM V2 (drift-controlled identification study). No V2 outcome data has been inspected; the identification question — separating TSMOM signal value from unconditional market drift — is deliberately kept un-resolved until execution.*