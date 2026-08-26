# QUANTFORGE — H01 EQUITY VOLATILITY-ASYMMETRY V1 PRE-REGISTRATION PROTOCOL

**Protocol version:** 1.2.0 (amended 2026-08-23; v1.0.0 and v1.1.0 history preserved below)
**Version history:** v1.0.0 — 2026-08-16, outcome-blind pre-registration. v1.1.0 — 2026-08-16, precision clarification only, applying exactly the three independent-audit corrections: (1) frozen-snapshot execution vs independent reacquisition/truncation verification (§7, §22 gate 1); (2) exact bootstrap missing-market aggregation and NaN/Holm handling (§15, §17, §18, §19); (3) `sp` pinned to the continuous ratio-back-adjusted `adj_close` (§7, §8). v1.2.0 — 2026-08-23, NYA universe amendment: (4) `NYA` added to `EQBROAD_L1` as the second primary-evaluable broad-US market; (5) NYA data input and preprocessing registered. No scientific, statistical, parameter, matching, bootstrap, null-inference, decision-rule, multiple-comparison, or secondary-analysis change.
**Type:** Outcome-blind pre-registration. Not an experiment, not a result, not a trading strategy.
**Registered:** 2026-08-16
**Authoritative definition:** `H01_EQUITY_VOLATILITY_ASYMMETRY_DEFINITION_LOCK_V1.md` (LEVEL 2 — READY FOR PRE-REGISTRATION)
**Predecessor machinery:** H01 v1.2 protocol (`H01_VOLATILITY_RESPONSE_ASYMMETRY_PROTOCOL_V1.md`), whose object, matching, strata, bootstrap, null-inference, and decision machinery are inherited exactly where the definition lock declares object-identity, and re-justified for the new equity design where the definition lock requires an independent justification (§16, §17).

This protocol is **pre-registration only**: it freezes *how the frozen hypothesis will be tested*. Nothing is executed; no result artifact may exist until the independent read-only audit of this protocol passes.

---

## 1. Purpose

Translate the frozen scientific definition (definition lock §2-§18) into a fully executable, deterministic statistical protocol for the US-anchored multi-market equity volatility-response replication. Every choice is fixed outcome-blind; no H01 v1.2 result value appears in this protocol; the v1.2 equity observations are historical motivation only, never design inputs.

## 2. Scientific Question (frozen, unchanged)

> For equity/index markets, the forward change in realized variance following a negative daily return shock differs from that following a positive daily return shock of equal absolute magnitude, after conditioning on the pre-shock realized-variance state.

- Association only: NOT a causal leverage-mechanism test, return prediction, volatility timing, short-volatility strategy, regime detection, or trading signal.
- Expected equity direction (frozen prior): **`D > 0`**, `D = ΔlnRV(negative shock) − ΔlnRV(positive shock)`.

## 3. Equity Prior (frozen)

**CLASSIC EQUITY ASYMMETRY, `D > 0`** — the classic direction (negative shocks → larger subsequent volatility increase). SOURCE-DERIVED FACT: established external literature recorded in the H01 definition lock (Black 1976; Christie 1982; Nelson 1991; GJR 1993; Engle–Ng 1993; Bekaert–Wu 2000; Aït-Sahalia–Fan–Li 2013). No new literature is added; no prior sign is altered.

## 4. Scope (frozen)

**US-anchored only.** Two distinct exposures: **broad US large-cap** and **US technology (Nasdaq family)**. International markets are not part of this protocol. No quarantined HPD root (`aor`, `cac`, `lj`, `ll`) is re-admitted; no market is added or removed for statistical reasons.

## 5. Universe, Layers, and Primary Cells (frozen)

Primary tests are defined per **(exposure × era) cell**. Four primary cells form the confirmatory family (§18).

| Cell | Exposure | Era | Markets (identity) | Instrument | Source |
|---|---|---|---|---|---|
| **EQBROAD_L1** | Broad US large-cap | Historical (1982-04-21 → 2002-10-01) | `sp`, `NYA` | S&P 500 **futures** (front-month, ratio back-adjusted) + NYSE Composite **cash index** (daily close) | HPD (frozen, in-repo) + Yahoo Finance `^NYA` (validated, in-repo, §18a exception) |
| **EQBROAD_L2** | Broad US large-cap | Contemporary (2016-08-15 → 2026-08-14) | SP500, DJIA | S&P 500 / Dow **cash indices**, daily close | FRED |
| **EQTECH_L1** | US technology | Historical (within 1982-04-21 → 2002-10-01) | NASDAQ100, NASDAQCOM | Nasdaq-100 / Nasdaq Composite **cash indices**, daily close | FRED |
| **EQTECH_L2** | US technology | Contemporary (2016-08-15 → 2026-08-14) | NASDAQ100, NASDAQCOM | Nasdaq-100 / Nasdaq Composite **cash indices**, daily close | FRED |

- **Market identity (frozen):** `sp` = HPD S&P 500 futures (CORE VALID, 82 rolls, continuity_ok=True); `NYA` = NYSE Composite cash index (daily close, price-type, Yahoo Finance `^NYA`, FRED-validated, definition lock §18a exception); NASDAQ100 = Nasdaq-100 price index (daily close, price-type); NASDAQCOM = Nasdaq Composite price index (daily close, price-type); SP500 = S&P 500 price index; DJIA = Dow Jones Industrial Average price index. All are **price-type** daily-close series (no total-return series, no ETFs, no CFDs in the primary universe).
- **Era windows (frozen constants):** HISTORICAL_END = 2002-10-01 (the HPD-era boundary; NDX/NCOMP data after this date is **not** used in the historical layer). CONTEMPORARY_START = 2016-08-15; CONTEMPORARY_END = 2026-08-14 (the last verified FRED observation at pre-registration; the contemporary window does not extend even if execution is delayed). The era-gap 2002-10-02 → 2016-08-14 is **structurally excluded** from both layers (registered; no validated broad-US cash series exists there).
- **`USATECHIDXUSD` is excluded from the primary universe** (definition lock §8: CFD-style instrument, US-tech — a near-duplicate of the tech exposure, MT5 provenance). It is declared as a secondary cross-provider reference only (§21), never a primary market.

## 6. Source-Type / Futures-Cash Rule (frozen; definition-lock Option A)

- The historical broad-US exposure is measured on the **S&P 500 futures complex** (`sp`); the contemporary broad-US exposure is measured on **FRED cash indices** (SP500, DJIA).
- **Futures-vs-cash is a registered source-type difference, not a defect.** No artificial conversion of futures into cash; no return-level adjustment based on any observed discrepancy; no use of the acquisition-report validation numbers as design inputs.
- **Registered rule:** (i) each market is its own statistical unit — shocks, matching, strata, and responses are computed entirely within the market's own series; (ii) source type is a recorded market attribute (market-identity table, §5); (iii) the object is applied identically to every series; (iv) futures/cash divergence is an interpretation limitation, recorded and reported, never adjusted away.
- **Cross-source validation is documentary/secondary only:** the futures-vs-cash comparability evidence (daily-return corr ≈ 0.95, median daily difference ≈ 16 bp, crisis-period divergences attributable to genuine futures/cash basis behavior; acquisition report §6, §10) is recorded as interpretation context. It is **not** recomputed inside the experiment from restricted sources, and it cannot alter any verdict.

## 7. Data Inputs and Fingerprints (frozen)

### Historical
- `sp`: in-repository `front_sp.csv` (`date, sym, close, adj_close`), frozen HPD validation (CORE VALID, continuity_ok=True). **SHA-256: `09451cdb44e09a453fc40888d8f0e9ba6b8ad79a9e45a4a05128683e2f2e721b`** (frozen HPD record). **The `sp` daily series is pinned to the continuous ratio-back-adjusted `adj_close` field** (the existing H01 construction): daily returns are computed from `adj_close`; roll-day exclusion remains unchanged (§9); no raw-`close` substitution is permitted; no adjustment based on any observed futures/cash difference is allowed.
- `NYA`: in-repository `docs/NYA_DATA.html` (Yahoo Finance `^NYA`, NYSE Composite daily Close), FRED-validated (definition lock §18a exception, owner-approved 2026-08-23). **SHA-256: `367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f`**. **The `NYA` series is pinned to the `Close` field** (price-type index level): daily returns are computed from `Close`; no `Adj Close` substitution; no raw-`close` or `Open`/`High`/`Low` use. NYA coverage: 1982-04-21 → 2002-09-30 (5,163 rows). The 1-day terminal gap (2002-09-30 vs HISTORICAL_END 2002-10-01) is handled by the missing-day policy (§9). Independent FRED validation: 80 quarterly observations; 76 exact matches; maximum discrepancy 0.51% (bounded, not full daily-series validation).

### Contemporary and historical Nasdaq series — FRED (deterministic re-acquisition)
Source URL: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>` (no API key required). Registered input snapshot acquired 2026-08-16; **SHA-256 (full):**

| File | SHA-256 | Rows | Coverage |
|---|---|---|---|
| fred_SP500.csv | `351555b5556f3437a50e594deb6988433b705285a7a54786820ef4382944ae7a` | 2,610 | 2016-08-15 → 2026-08-14 |
| fred_DJIA.csv | `29c8ca59469de81b79041ff3cb5888cee0468c2529705270be207b91fb4c2d5d` | 2,610 | 2016-08-15 → 2026-08-14 |
| fred_NASDAQCOM.csv | `51187aa6f103f27d34963008a3e43329dd60bae0c7243500927fcc064beaf3db` | 14,486 | 1971-02-05 → 2026-08-14 |
| fred_NASDAQ100.csv | `aeacca4f6472dd56aa32fa3a67d948822d8172288597624d0fd9ddf67fcf6a3a` | 10,597 | 1986-01-02 → 2026-08-14 |

**Frozen input snapshot (execution):** the execution inputs are the **exact frozen snapshot files registered on 2026-08-16**, whose SHA-256 hashes are recorded above. At execution, every input file must match these hashes exactly; a mismatch (e.g., a FRED data revision in the snapshot files) → **STOP** and re-engage the audit chain; no re-hashing improvisation.

**Independent reproducibility (reacquisition):** a researcher who reacquires live FRED data does **not** need the live file itself to SHA-match the frozen snapshot. Instead: (1) reacquire the FRED series; (2) restrict/truncate it to the registered `CONTEMPORARY_END`; (3) verify the registered date window; (4) verify values within the registered window against the frozen snapshot; (5) record any revision/mismatch; (6) **STOP if the registered historical window has changed**. A live FRED file that has merely grown after the registration date cannot invalidate the frozen experiment snapshot because it contains later observations. This does **not** weaken the frozen-input integrity gate: execution always uses the frozen snapshot files exactly as fingerprinted, and changed FRED history is never silently accepted.

## 8. Preprocessing (frozen, deterministic)

1. **FRED parsing:** read `observation_date,<ID>`; rows whose value is `.` (US exchange-holiday placeholders) are **dropped** as missing days (registered; these are exactly the 96/96/487/362 holiday rows verified at acquisition). No imputation.
2. **Daily close series:** for each market, `close_t` = the index value on date `t`; log return `r_t = ln(close_t / close_{t−1})`. For `sp`, `close_t` is the **continuous ratio-back-adjusted `adj_close`** field of the frozen HPD series (§7, the existing H01 construction); no raw-`close` substitution. FRED series have no duplicates, no weekend rows, no non-positive values (verified at acquisition); any violation found at execution → STOP (gate 4).
3. **Era truncation:** NDX/NCOMP historical series are truncated to ≤ HISTORICAL_END (2002-10-01); all four FRED series are truncated to CONTEMPORARY_START..CONTEMPORARY_END for the contemporary layer. `sp` uses its full validated history (1982-04-21 → 2002-10-01). `NYA` uses its full validated history (1982-04-21 → 2002-09-30); observations beyond 2002-09-30 do not exist in the source. The 1-day terminal gap is handled by the missing-day policy (§9) — any shock requiring 2002-10-01 in its window is dropped.
4. **Eligibility (inherited, frozen):** a shock day `t` is eligible iff `r_t ≠ 0` and all window rules (§9) pass. A zero-return day is neither NEG nor POS, excluded from matching, counted and reported.

## 9. Roll-Day, Missing-Day, and Zero-RV Rules (inherited; frozen)

- **Roll days (`sp` only):** a roll day is a day on which `sym` changes vs the previous day in the continuous series. A shock day `t` is **excluded** if `t`, or any of the 10 window days (`t−5..t−1`, `t+1..t+5`), is a roll day. **FRED cash indices and NYA have no roll days** (no contract symbol); the rule applies only to `sp`. Excluded-count fraction reported as a diagnostic.
- **Missing-day policy:** a shock day `t` is excluded unless **all 5 days** of each window are present in the market's daily series (incomplete windows dropped, not imputed).
- **Zero-RV policy:** a shock day `t` is **ineligible** if either `RV_{t−5..t−1} = 0` or `RV_{t+1..t+5} = 0`. Such days are counted and reported; no epsilon is added.
- **Invalid rows:** any non-positive close, or (for `sp`) rows inconsistent with the frozen manifest discipline, are excluded and treated as missing.

## 10. Shock Definition (inherited; frozen)

- **Primary exposure:** daily close-to-close log return `r_t`, signed scalar, market-local computation.
- Zero-return shocks excluded (§8.4). No standardization/residualization in the primary; standardized shocks are secondary-only (§21).

## 11. Volatility Response (inherited; frozen)

- `RV_back = Σ_{t−5..t−1} r²`; `RV_forward = Σ_{t+1..t+5} r²`; `ΔlnRV = ln(RV_forward) − ln(RV_back)`; shock day excluded from both windows.
- RV = sum of squared daily log returns (identical construction across all series; comparable object by construction).
- Literature anchor: Aït-Sahalia, Fan & Li (2013) document the effect at 5-day and 21-day horizons.

## 12. Horizon (frozen by object-identity)

**`h = 5 trading days`** — inherited as object-identity (definition lock §12): the replication tests whether the frozen H01 object generalizes; 5 days was registered pre-outcome in H01 v1.1 and is not an outcome-derived choice. 1-day and 21-day horizons are secondary-only, non-rescuing (§21).

## 13. Volatility-State Conditioning (inherited; frozen)

- **Strata:** within-market **terciles of `ln(RV_back)`** over the market's full eligible series, computed **once** on the original data (`ξ_low, ξ_mid, ξ_high`), **frozen constants** — never re-estimated inside any bootstrap replicate (the same frozen-constant treatment as the calipers).
- **Boundary population:** the market's full eligible series within its layer window (§8.3), including shocks later excluded by matching. Missing/zero-RV days are excluded before boundary computation per §9.
- No new state model (regime/HMM/GARCH-state) is introduced.

## 14. Matching (inherited; frozen, one deterministic implementation)

Within each (market, stratum), on the eligible shocks of that cell's layer window:

1. Split eligible shocks into `NEG` (`r_t < 0`) and `POS` (`r_t > 0`). If either pool is empty, the (market, stratum) yields 0 matched pairs.
2. **Caliper** `c = 0.25 × SD(|r|)` over **all eligible shocks in that (market, stratum)** (Austin 2011 standard caliper). If fewer than 2 eligible shocks, `c` is undefined → 0 matched pairs. `c` is frozen, never re-estimated or tuned.
3. **Reference pool** = the smaller of NEG/POS (equal sizes → POS, frozen); match pool = the other. Both ordered by the frozen stable key `(|r_t| ascending, timestamp ascending)`.
4. **Greedy one-to-one matching:** for each reference observation in order, select the unmatched match-pool observation minimizing `| |r_ref| − |r_match| |` subject to `≤ c`; ties broken by smaller `|r|`, then earlier timestamp. Pair and remove both.
5. One-to-one, no reuse; strictly within (market, stratum) — no cross-market, cross-stratum, or cross-era matching.
6. Unmatched shocks counted and reported per (market, stratum); no adaptive trimming.
7. **Balance diagnostic (QC-only):** per (market, stratum), report mean `|r|` of matched NEG vs POS and the standardized mean difference. Reported; never triggers re-matching, re-weighting, or verdict changes.
8. **Matching is rebuilt inside bootstrap replicates** with the frozen calipers and tercile bounds (response-blind — pairing depends only on the shock-side variables `|r|`, stratum, dates).

## 15. Statistics (inherited; frozen)

- Per-market, per-stratum: `d_{m,s} = mean over matched pairs in (m, s) of [ΔlnRV(negative-shock day) − ΔlnRV(positive-shock day)]`.
- Per-market: `d_m = mean over the 3 strata of d_{m,s}` (equal 1/3 stratum weights; a large stratum cannot dominate).
- **Empty-stratum rule (inherited §9.3):** the per-market mean is over strata yielding ≥ 1 matched pair in the relevant data (original for `d_m`; replicate for `d_m^(b)`); if no stratum yields pairs, the market contributes no draw to that replicate.
- **Replicate aggregation rule (inherited v1.2 execution semantics; frozen):** within a bootstrap replicate, (i) each market's `d_m^(b)` is computed by the registered three-stratum rule; (ii) a market with no valid stratum result produces no `d_m^(b)` and is **excluded from that replicate's market mean** — missing markets are never replaced by zero and never implicitly carried forward; (iii) `D_cell^(b)` is the arithmetic mean over the markets that produced a finite `d_m^(b)`; (iv) a replicate with no finite market result yields `D_cell^(b) = NaN`; (v) null-draw p-value accumulation uses only finite null draws (§18); (vi) the p-value denominator remains the fixed `(B + 1)`; (vii) a cell with no finite p-value is treated as `p = 1.0` for Holm ordering and receives no primary scientific verdict (§19).
- Per-cell: `D_cell = mean over the cell's primary-evaluable markets of d_m` (equal market weights; a large market cannot dominate).
- **Primary unit of inference:** the per-market statistic `d_m`; no pooled raw shocks, no cross-market pooled estimator in the primary.

## 16. Evaluability (inherited; frozen)

- A market is **primary-evaluable** iff **all 3 strata** yield **≥ 30 matched pairs** in the original (pre-bootstrap) data (frozen structural rule of thumb, pre-outcome, not data-inspected). A market failing the floor is excluded from `D_cell` but fully retained in per-market diagnostics.
- A cell supports a **primary verdict** iff it has **≥ 2 primary-evaluable markets**. A cell with 0-1 evaluable markets is **EVIDENCE-LIMITED/DESCRIPTIVE**: its statistics and Holm-adjusted p-value are reported and it remains in the family, but no primary verdict is assigned and it cannot anchor strong cross-era claims.
- **Consequence for this design (structural, pre-outcome):** `EQBROAD_L1` contains two primary-evaluable markets (`sp` and `NYA`, subject to ≥30-pairs floors) → **primary-eligible** (no longer EVIDENCE-LIMITED by construction). All four cells are primary-eligible in principle (subject to the ≥30-pairs floors).

## 17. Dependence-Aware Inference (frozen; machinery inherited, re-justified for this design)

**Problem:** overlapping 5-day forward windows create serial dependence within each market; markets within a cell share contemporaneous news → cross-market dependence must be preserved at the cell level.

- **Primary inference — synchronized cell-level circular calendar-block bootstrap** (identical machinery to the validated H01 v1.2 §9/§16, applied per cell):
  1. **Union calendar per cell:** the sorted set of dates on which ≥ 1 market in the cell has an eligible shock record. **Block length `L = 11` trading days** — the full span of the response windows (`t−5..t+5`). Justification for this design: the response DGP is unchanged (5-day windows); a block of 11 consecutive union-calendar days preserves all serial dependence that overlapping 11-day response windows create, and synchronized blocks keep same-date shocks across markets together (contemporaneous cross-market dependence). `L = 11` is inherited from the frozen H01 object and is the minimal block length covering the full window span; it is frozen, not tuned. **`B = 10,000` replicates; single master seed `20260816`** (a fresh registered constant for this experiment, outcome-blind; distinct from the H01 seed by design).
  2. **Block resampling (circular, with replacement):** each replicate samples union-calendar positions uniformly with replacement and concatenates the circular blocks of `L` consecutive union-calendar days starting at those positions (wrap-around covers the grid end; no truncation, no padding).
  3. **Per-market replicate statistics:** for each market, the replicate stream is the market's eligible shock records whose dates fall in the sampled blocks, ordered by date; recompute within each (market, stratum) the caliper matching and per-stratum statistic using the **frozen** tercile bounds and calipers; yield `d_m^(b)` (mean over strata with ≥ 1 pair in the replicate). A market with no paired strata contributes no draw to that replicate.
  4. **Cell level:** `D_cell^(b)` = equally weighted mean of `d_m^(b)` over the cell's primary-evaluable markets, per the frozen replicate-aggregation rule (§15): a market producing no finite `d_m^(b)` is excluded from that replicate's mean; a replicate with no finite market result is `NaN`. **Evaluable-market membership is fixed at the original-data stage and never re-selected inside a replicate.**
  5. **Missing-market behavior:** a market has no record for union days on which it did not trade — inherent to the union grid, never imputed.
  6. **Execution determinism (frozen, pre-registered):** execution is a **single uninterrupted invocation**; fixed cell processing order (EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2); the master seed drives the entire stream. **No partial-cache resume is permitted** (resume-by-skip is a documented defect of the H01 v1.2 execution); an interrupted run is restarted from scratch, which reproduces the same stream by determinism.
- **CI:** percentile interval (2.5%, 97.5%) of the ordinary sampling replicate distribution `D_cell^(b)` — the sampling interval only, never replaced by the null distribution.

## 18. Null-Inference (frozen; the corrected, null-imposing construction — inherited from the validated H01 v1.2 §9A)

**The v1.1 defect is not repeated.** The v1.1 formula (2 × min of one-sided sampling-tail probabilities against `D_obs`) is **retired** and must never be used.

- **Null:** `H0: D_cell = 0` per cell — the vol-state-conditioned, magnitude-matched difference in forward ΔlnRV between negative and positive shocks is zero (mean/class-location null, not expanded).
- **Data-level null construction (authoritative):** per (market, stratum):
  1. `c_(m,s) = mean(d_i)` over the matched pairs in (m, s), `d_i = ΔlnRV(neg) − ΔlnRV(pos)` — computed once on the full original matched data, **frozen for all replicates**, never re-estimated inside a replicate.
  2. **Shock-response-level null transformation (registered implementation):** subtract `c_(m,s)/2` from the ΔlnRV response of every eligible negative-shock day in (m, s) and add `c_(m,s)/2` to every eligible positive-shock day in (m, s) — applied to **every eligible shock, including shocks unmatched in the original sample that may become matched after bootstrap resampling**, before rebuilt matching in each replicate. Equivalently every pair difference becomes `d_i^0 = d_i − c_(m,s)`; any deterministic sign-split producing that difference is mathematically equivalent; the ±`c_(m,s)/2` form is the registered implementation. The transformation is additive within (market, stratum), preserving variances, covariances, serial dependence, and synchronized cross-market dependence.
  3. Run the registered resampling (§17) on the null-transformed response process (same union calendars, L, B, seed, circular wrap-around; matching rebuilt with frozen calipers/terciles; evaluable-market membership fixed; empty-stratum rule as §15). Draws `D*_null` are centered at zero by construction.
- **Statistic-level pivot:** `D*_null = D* − D_obs` is the equivalent representation only when every evaluable market has all three strata represented in the replicate (equal weights make the recentering constant exactly `D_obs`); where the empty-stratum rule creates a difference, the data-level form controls. The shortcut is never silently substituted. Execution implements the data-level form.
- **p-value (frozen):** two-sided null-test `p = Pr*( |D*_null| ≥ |D_obs| )` over the B null draws; Monte-Carlo convention `p = (1 + count)/(B + 1)`, `count = #{b : |D*_null,b| ≥ |D_obs|}` (inclusive `≥`). Accumulation uses **only finite null draws** (a replicate yielding `D*_null = NaN` per §15 is excluded from `count` but not from the denominator); the denominator remains the fixed `(B + 1)`.
- **CI:** the ordinary percentile sampling CI (§17) — separate from the null test, never substituted.
- **Limitations (disclosure, not invalidity):** block-bootstrap consistency is assumed for the registered dependence structure; the estimator contains greedy nearest-neighbour caliper matching with rebuilt matching in replicates; Abadie–Imbens-style nearest-neighbour bootstrap caveats apply; the construction is not claimed to have a dedicated published theorem. Same caveats as the validated H01 v1.2 inference.

## 19. Multiple Comparisons (frozen)

- **Primary family:** the **4 cells** of §5 — EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2.
- **Correction:** Holm step-down across the 4-member family at family-wise **α = 0.05**, two-sided p per member (§18). Precedent: DISC-021/TSMOM V2/H01 family discipline.
- **Evidence-limited cells remain in the family** (statistics and Holm-adjusted p reported; no primary verdict; H01 §15/§18 inheritance).
- **NaN p handling:** a cell with no finite p-value (no finite null draws, §15) is treated as `p = 1.0` for Holm ordering and receives **no primary scientific verdict** (its statistics remain reported).
- No post-hoc family expansion; any new test requires a protocol amendment.

## 20. Cross-Era Design (frozen)

- **No pooled estimator spanning both eras** in the primary; eras are separate cells (§5).
- **Cross-era consistency is a descriptive directional-consistency comparison** per exposure, evaluated only where the exposure exists in both eras: **EQBROAD** (L1 evidence-limited by construction → cross-era comparison is **EVIDENCE-LIMITED**, never strong replication) and **EQTECH** (both eras primary-eligible → cross-era directional consistency testable; **strong replication** requires both eras' cells to be primary-reliable in the expected direction per §23).
- A one-market cell is never called "confirmed replication" (§23; the frozen ≥2-market rule and the EVIDENCE-LIMITED label govern).

## 21. Secondary Analyses (pre-declared; segregated; NON-RESCUING)

Declared before outcomes; none may redefine the primary, its family, or its verdicts:
1. 1-day horizon (`RV_{t+1}` vs `RV_{t−1}`).
2. 21-day horizon (3-week windows).
3. Standardized shock `|r_t|/σ̂_{t−1}` variants of matching.
4. Alternative response: absolute-return `E[|r_{t+h}|]` difference.
5. Winsorization sensitivity (pre-registered cap: 95th percentile of |r| within market) — sensitivity, not primary.
6. GJR(1,1) and EGARCH(1,1) γ diagnostics — with the mandatory statement reproduced verbatim: *"A GJR/EGARCH coefficient does not replace the primary empirical response statistic and cannot rescue a failed primary result."* Known boundary/clamp behavior in this environment means GJR/EGARCH output is non-confirmatory and its signs are not scientific evidence.
7. Engle–Ng sign-bias regressions on standardized residuals.
8. Common-window sensitivity: restrict the historical layer to the common exposure window 1986-01-02 → 2002-10-01.
9. **Cross-provider MT5 reference (non-primary):** report the US-tech exposure's asymmetry pattern as delivered by `USATECHIDXUSD` (MT5) as a different-provider, different-instrument reference — explicitly non-rescuing, never entering the primary family, and requiring the source-comparability caveat of the definition lock §8.
10. **Cross-source futures/cash context (documentary):** the acquisition-report validation (not recomputed inside the experiment from restricted sources) is recorded as interpretation context for EQBROAD_L1 (§6).

## 22. Data-Quality Gates and Stopping Rules (frozen)

**Gates (any failure → STOP, no improvisation):**
1. **Fingerprint gate:** execution uses the **frozen snapshot files of §7 exactly as fingerprinted** — SHA-256 of every execution input matches §7 (HPD `front_sp.csv`; the four FRED files). Mismatch (including a FRED data revision in the snapshot files) → STOP, re-engage the audit chain. Independent reacquisition/truncation verification (§7) is a separate reproducibility procedure that never substitutes different files into the execution; a live FRED file that grew after registration does not invalidate the frozen snapshot.
2. **Universe gate:** exactly the frozen markets of §5; no market added/removed; era windows per §5.
3. **Date-range gate:** no data beyond the recorded coverage boundaries (§7).
4. **Duplicate / validity gate:** duplicate dates, non-positive prices, weekend rows in FRED inputs → STOP (violations were absent at acquisition).
5. **Missingness gate:** per-market completeness and gap summary reported; incomplete windows dropped per §9.
6. **Roll-consistency gate (`sp`):** `sym`-change detection reviewed against the frozen `PER_MARKET_VALIDATION.csv` roll count (82); mismatch → STOP.
7. **RV-construction gate:** response windows reproducible from the daily series; leakage-free (windows defined strictly on past/future daily data, shock day excluded).
8. **Leakage gate:** no forward-looking data in conditioning (strata from backward RV only).
9. **Determinism gate:** single-invocation execution, fixed cell order, seed 20260816; no partial-cache resume.
10. **Licensing gate:** the PENDING licensing record (§24) is carried into execution metadata; nothing is represented as CLEAR.

**Stopping rules (inherited from the validated H01 §23, adapted):** STOP if (a) matching is ambiguous for any market's data; (b) the RV construction differs materially between sources in a way not covered by §8-§11; (c) `sp` roll handling is unclear; (d) L = 11 cannot preserve within-market dependence or the cell union calendar cannot be constructed; (e) any market's cell membership is ambiguous; (f) any choice is observed to depend on inspected outcomes; (g) any new scientific choice arises that this protocol did not anticipate; (h) any gate fails in a way requiring a new scientific choice; (i) an unrecognized duplicate is found among primary markets.

## 23. Scientific Decision Rules per Cell (frozen)

For each cell, based on the family-adjusted two-sided null-test p (§18-§19) and the sign of `D_cell` vs the frozen prior (`D > 0`), subject first to evaluability (§16):

- **Evaluability gate:** a cell supports a primary verdict only if it has ≥ 2 primary-evaluable markets; otherwise **EVIDENCE-LIMITED/DESCRIPTIVE** (statistics and Holm p reported; cell remains in the family; no primary verdict; cannot anchor strong cross-era claims).
- **SUPPORT (primary-evaluable cells):** `D_cell` reliable (Holm-adjusted two-sided p < 0.05) with sign **matching** the expected direction (`D_cell > 0`); AND ≥ 2/3 of the cell's evaluable markets show the class sign (for exactly 2 evaluable markets both must agree — never vacuous); AND (cross-era requirement where applicable, §20) both eras' cells reliable in the expected direction for a strong replication claim.
- **CONTRADICTION:** `D_cell` reliable (p < 0.05) in the **opposite** direction (`D_cell < 0`); or evaluable markets within the cell disagree in sign while the cell effect is reliable.
- **INCONCLUSIVE:** otherwise (not reliable; CI includes null; inconsistent-but-unreliable; or not primary-evaluable — EVIDENCE-LIMITED label then applies).
- No non-pre-registered effect-size thresholds; α = 0.05; family = §19.

## 24. Licensing (recorded honestly)

| Component | Status |
|---|---|
| HPD `sp` | **PENDING** (standing frozen HPD record; local research use per repo precedent) |
| FRED SP500, DJIA | platform access CLEAR (attribution required); underlying index series (© S&P Dow Jones Indices) archival rights **PENDING** |
| FRED NASDAQ100, NASDAQCOM | platform access CLEAR; underlying series (© Nasdaq) archival rights **PENDING** |
| Yahoo Finance `^NYA` | **EXCEPTION GRANTED** (definition lock §18a; owner-approved 2026-08-23); archival rights **PENDING** (requires owner acceptance for archival persistence) |
| Permission requests | **PREPARED, NOT SENT** (operator dispatch required; acquisition report §11) |

**Execution-governance statement:** execution may proceed under the project's current internal-use governance (the HPD PENDING precedent and the NYA Yahoo exception), with the PENDING records and NOT-SENT status carried into execution metadata. If the operator requires CLEAR archival rights before execution, permission must be resolved first — a governance gate, not a scientific one.

## 25. Outcome-Blind Self-Audit (completed at pre-registration)

1. No H01 v1.2 result value is copied into this protocol (verified: no effect-size, p-value, CI, or class ranking appears).
2. No market is chosen because of observed v1.2 performance — markets are selected by identity/provenance (definition lock §5).
3. No parameter is chosen from v1.2 secondary results — the horizon (5-day) is object-identity (§12); L=11 is the response-window span (§17); the seed is an arbitrary fresh constant (§17).
4. The scientific definition matches the definition lock exactly (§2-§6, §10-§16).
5. The universe matches the scope decision (US-anchored; no international claim; `USATECHIDXUSD` excluded structurally).
6. Null inference is the corrected null-imposing construction (§18); the v1.1 defect is retired.
7. All choices are deterministic and pre-registered; the protocol can be executed without asking the author a new scientific question (any ambiguity → §22 STOP).
8. The frozen H01 v1.2 protocol and artifacts, and all governance records, are untouched by this pre-registration.

## 26. Authorized Next Action

**INDEPENDENT READ-ONLY AUDIT OF THE H01-EQUITY V1 PRE-REGISTRATION.** No execution may begin before that audit passes. After the audit: **execution** under this protocol, producing the registered artifact set (execution script, metadata with fingerprints/versions/seeds, daily series, matched-pair table, per-market and per-cell tables, bootstrap replicates, null draws, results JSON, scientific report).

## 27. Integrity Statement

- **Outcome-blind:** no H01 statistic was computed; no experiment run; no GARCH/EGARCH/GJR fitted; no threshold optimized; no restriction imposed from any QuantForge outcome. Choices rest on the frozen definition lock, the external literature recorded there, the validated H01 v1.2 machinery, and structural data facts (fingerprints, coverage, continuity).
- **Artifact only:** this protocol is the sole file created by this pre-registration task. No scripts, datasets, models, or result files were created; none may exist until the independent read-only audit passes.
- **Firewall:** no BOE, Assembly, Deployment, tests, contracts, or governance files modified (verified via `git status`).
- **Heritage:** the H01 v1.2 result remains historical motivation only; the v1.1 invalid-inference status and the v1.2 adjudication are untouched by this protocol.
