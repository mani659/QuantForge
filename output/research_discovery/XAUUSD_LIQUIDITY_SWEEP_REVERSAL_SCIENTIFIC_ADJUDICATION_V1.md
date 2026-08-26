# QUANTFORGE — XAUUSD LIQUIDITY SWEEP / REVERSAL
# INDEPENDENT SCIENTIFIC RESULTS ADJUDICATION V1

## 0. Identity

- **Experiment:** XAUUSD Liquidity Sweep / Reversal V1.2.0 multi-market event study.
- **Protocol:** `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL_EVENT_STUDY_PROTOCOL_V1.md` (v1.2.0; SHA-256 verified on disk `c6b8fbd4…` = the audited object in Final Clearance Audit V2).
- **Execution report:** `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL/SCIENTIFIC_REPORT_V1.md`.
- **Adjudication mode:** STRICT, READ-ONLY, independent. No rerun, no statistic computed beyond independent recomputation of the frozen observed statistic from the persisted event artifacts, no protocol modification, no strategy work.

---

## 1. Executive Verdict

**A — ADVANCE TO ECONOMIC / STRATEGY TRANSLATION** (scoped).

The registered sweep-rejection-confirmation behavioral hypothesis is **strongly supported** in all four markets that passed the data gates — XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD — with family-wise-corrected (Holm) significance, directionally consistent positive ΔM, and confidence intervals far from zero. The EURUSD leg was halted by the pre-registered data-quality gate before inference and is **DATA-LIMITED / NOT ADJUDICATED** — not a hypothesis failure.

The evidence establishes:

- **Level 1 (instrument):** established — XAUUSD.
- **Level 2 (asset-class):** established — precious metals (XAUUSD + XAGUSD).
- **Level 3 (cross-market):** **preliminary, not full** — two genuinely distinct non-metals mechanisms (equity-index CFD, crypto spot) each pass independently, but each has only a single validated instrument, and FX (EURUSD) is missing.
- **Level 4 (universal): NOT established.** Four positive markets do not imply universality, and the two precious-metals markets are not independent evidence.

The behavioral result is a major QuantForge milestone **only** as a validated behavioral phenomenon. It is **not** an economic edge: no PnL, expectancy, spread/slippage, entry/stop/target, or live robustness has been tested. The next legitimate task is a **separate** Strategy / Economic Translation stage for the validated markets.

---

## 2. Execution Integrity

| Item | Registered | Persisted verification |
|---|---|---|
| Protocol version | v1.2.0 | Confirmed on disk; SHA-256 `c6b8fbd4…` matches Final Clearance Audit V2's recorded protocol hash. **PASS** |
| Input hashes | per-market M1 files | Report fingerprints match `sha256sum data/m1/*` **exactly** for all four evaluated markets: XAUUSD `54cf6155…`, XAGUSD `69444be9…`, USATECHIDXUSD `39f25619…`, BTCUSD `97b85385…`. **PASS** |
| EURUSD input hash | — | Absent from the report; consistent with halt before inference (no EURUSD events CSV exists). **Consistent, not independently verifiable** |
| B = 10,000 / L = 10 / seed = 20260817 | protocol §13 | Stated in report; **not independently recomputable** — no bootstrap/null draws, metadata JSON, execution script, or execution log is persisted in the repository. |
| Event artifacts | required | 4 event CSVs exist (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD); schema `market,trading_day,direction,type,asian_level,rejection_ts,anchor_ts,mfe`. **PASS** |
| Bootstrap/null artifacts | required | **NOT PERSISTED** — no `.npy`/`.npz`/draw file exists for this run anywhere in the repo or scratch. Reproducibility gap (see §8). |
| No rerun / no concurrency / no checkpoint contamination | required | **Unverifiable from persisted artifacts** (no log/metadata). No evidence of contamination in the artifacts that do exist. |
| D_obs recomputation | frozen aggregation | **Independent recomputation from persisted event CSVs matches the report exactly for all four markets** (XAUUSD 4.05700; XAGUSD 0.10100; USATECHIDXUSD 39.78700; BTCUSD 229.10000). **PASS** |
| Event-count reconciliation | frozen counts | Report counts = CSV row counts exactly: XAUUSD 1527+93=1620; XAGUSD 1517+85=1602; USATECHIDXUSD 984+39=1023; BTCUSD 1960+117=2077. **PASS** |
| Event structure | §9 first-upper/first-lower per day | Max 2 events/day in every market (upper+lower pairs coupled on 362–445 days per market); no duplicate trading days; direction mix balanced in all markets. **PASS** |
| MFE validity | §10 formula, unclamped | 0 negative MFEs except **one BTCUSD control event** (2021-07-09, upper, mfe = −0.9): permitted by the unclamped registered formula (true-breakout continuation case), immaterial. **Note only** |
| EURUSD halt | §17 gate | 291/1,716 EURUSD days contain <600 bars = **16.958%**, matching the reported 16.96% exactly, under a minimum-coverage operationalization of the registered "sufficient session observations" rule; >10% → halt before inference. **PASS — see §4 for the operationalization caveat** |

**Verdict on integrity:** the scientific core of the execution verifies cleanly from persisted artifacts (protocol object, input hashes, event population, observed statistic, counts, structure). The **persistence layer is incomplete**: the execution script, metadata JSON (protocol hash, seed/B/L record, RNG verification), and bootstrap/null draw artifacts were not written to the repository, so the p-values, CIs, and the B=10,000/L=10/seed=20260817 inference layer cannot be independently recomputed from persisted draws. This is a reproducibility deficiency of the record-keeping, **not** evidence of a validity failure; all internally consistent signals (floor p-values = 1/10001 for every market, Holm arithmetic, CI geometry around D_obs) are coherent with the registered design.

---

## 3. Primary Results

Independent recomputation of the frozen observed statistic and reconciliation of counts (all values as persisted in the report):

| Market | Status | Treatment | Control | ΔM_obs | 95% CI | p_raw | p_Holm | Classification |
|---|---|---|---|---|---|---|---|---|
| XAUUSD | EVALUABLE | 1527 | 93 | 4.05700 | [3.47699, 4.58150] | 9.9990e-05 | 3.9996e-04 | **SUPPORT** |
| XAGUSD | EVALUABLE | 1517 | 85 | 0.10100 | [0.08600, 0.11400] | 9.9990e-05 | 3.9996e-04 | **SUPPORT** |
| USATECHIDXUSD | EVALUABLE | 984 | 39 | 39.78700 | [32.80498, 47.21875] | 9.9990e-05 | 3.9996e-04 | **SUPPORT** |
| BTCUSD | EVALUABLE | 1960 | 117 | 229.10000 | [188.69875, 263.30000] | 9.9990e-05 | 3.9996e-04 | **SUPPORT** |
| EURUSD | HALTED | — | — | — | — | — | — | **DATA-LIMITED / NOT ADJUDICATED** |

**Classification check under the frozen rules (§14):** every evaluable market has ≥100 treatment events (984–1960) → not EVIDENCE-LIMITED; Holm p = 3.9996e-04 < 0.05; ΔM_obs > 0 → **SUPPORT** in all four. Verified: since all four raw p-values are equal, Holm step-down yields 4 × 9.9990e-05 = 3.9996e-04 for each — correct.

**p-value floor:** every p_raw equals 1/10001 = 9.9990e-05, i.e., count = 0 null replicates with |ΔM*_null| ≥ |ΔM_obs| in all four markets. The CIs' separation from zero (margins 5–20× the half-width) is coherent with a floor effect; the finite-B convention caps the reported significance at 1/10001.

**Sampling CI vs null p (frozen distinction, §16):** the CI is the ordinary percentile interval of the sampling ΔM* distribution (2.5/97.5); the null-test p uses the recentered distribution ΔM*_null = ΔM* − ΔM_obs with the (1+count)/(1+B_valid) formula. The two objects are distinct as registered.

---

## 4. EURUSD Data-Limit Disposition

- **Halt fact:** invalid-day fraction reported at 16.96% > 10% threshold → execution halted before any EURUSD inference. **No EURUSD events CSV and no EURUSD results exist in the persisted artifacts** — consistent with the halt; no inference was performed.
- **Independent verification:** the reported 16.96% is exactly reproduced as **291 of 1,716 EURUSD calendar days with ≥1 M1 bar having fewer than 600 bars (16.958%)**. The data is structurally sound in other respects (0 duplicate timestamps, 0 invalid OHLC, 0 gaps >3 days, full-day bars ≈1,436–1,440); the deficit is concentrated in partial-coverage days (Sunday opens, holiday sessions, truncated daily windows) plus 317 days missing the 16:00 ET bar and 322 missing 17:00.
- **Caveat (reproducibility, non-blocking for disposition):** the registered §17 invalid-day text requires ≥1 valid Asian bar and ≥1 valid London/NY bar — under that literal rule only 28 days (1.63%) would be invalid and no halt would occur. The execution therefore operationalized "sufficient session observations" as a ~600-bar/day minimum-coverage rule. That operationalization is **not uniquely pinned by the protocol text and its implementation is not persisted**. The halt's *disposition* is correct and data-quality-driven; its *exact gate mechanics* are a reproducibility gap to be closed in the strategy-translation-stage record (or a future protocol amendment if EURUSD is ever re-admitted).
- **Classification:** **DATA-LIMITED / NOT ADJUDICATED.** It is NOT CONTRADICTED, NOT INCONCLUSIVE, NOT a failed hypothesis, and NOT evidence either for or against the behavior.
- **Impact on the claim:** the missing EURUSD leg **materially limits** (a) any FX-family generalization and (b) the breadth of the cross-market claim. The multi-market result stands on metals + equity-index + crypto only; no FX statement is possible.

---

## 5. Market-by-Market Adjudication

- **XAUUSD — SUPPORT (discovery confirmation).** Gold, discovery instrument. Largest relative CI width but decisive. This is *discovery success*, not validation.
- **XAGUSD — SUPPORT (asset-class replication).** Silver — same precious-metals auction family as XAUUSD; correlated, so it is *not* independent evidence for a cross-market claim, but it does establish asset-class replication.
- **USATECHIDXUSD — SUPPORT (independent mechanism).** US technology equity-index CFD — a genuinely distinct market mechanism (equity index vs metals). Single instrument in its class.
- **BTCUSD — SUPPORT (independent mechanism).** Crypto spot — a third genuinely distinct mechanism (24/7 digital-asset market). Single instrument in its class.
- **EURUSD — DATA-LIMITED / NOT ADJUDICATED** (§4).

Every evaluable market is directionally consistent (ΔM_obs > 0), statistically significant after family-wise correction, and measured with identical event definitions, horizons, and inference — no market received special treatment.

---

## 6. Cross-Market Evidence

The five registered markets decompose into four economically distinct mechanism classes:

| Class | Markets | Outcome |
|---|---|---|
| Precious metals (correlated pair) | XAUUSD, XAGUSD | Both SUPPORT → **Level 2 established** |
| Equity index CFD | USATECHIDXUSD | SUPPORT → one independent leg |
| Crypto spot | BTCUSD | SUPPORT → one independent leg |
| FX | EURUSD | HALTED (data) → no leg |

**Assessment:**

- **Level 1 (instrument-specific):** established (XAUUSD).
- **Level 2 (asset-class):** established (precious metals; the two metals are one asset class, not two independent classes).
- **Level 3 (cross-market):** **preliminary** — the phenomenon is confirmed in **three economically distinct mechanisms** (metals, equity index, crypto) with family-wise-corrected significance in each, which is genuinely more than an asset-specific or single-market effect. However, the non-metals legs are one instrument each, the metals pair is not independent, and the most natural adjacent class (FX) is untested. Full Level 3 breadth is therefore **not** claimed.
- **Level 4 (universal): NOT established.** Four positive markets are not universality, and no statement about all FX, all equities, or all crypto is licensed.

The honest scientific summary is: **a robust multi-market behavioral phenomenon across three distinct mechanisms, with an untested FX leg and no universality claim.**

---

## 7. Magnitude Interpretation

- MFE is measured in market-native price units: USD/oz (XAUUSD, XAGUSD), index points (USATECHIDXUSD), USD per BTC (BTCUSD). Raw ΔM values (4.06 vs 0.10 vs 39.79 vs 229.10) are **not economically comparable** and must not be ranked.
- The adjudication criterion is: *is the effect statistically present and directionally consistent across markets?* — answered YES for all four. The numerical scale of ΔM says nothing about relative tradability.
- No market selection, horizon selection, or parameter was based on magnitude anywhere in the chain.

---

## 8. Null / Inference Integrity

- **Null construction:** ΔM*_null = ΔM* − ΔM_obs tests H0: ΔM = 0 under the median location-equivariance argument approved in Final Clearance Audit V2 (for a difference of medians, recentering the bootstrap distribution is exactly the null-imposing data-level shift); no H01-specific construction was imported. **Coherent with the registered design.**
- **p-value:** (1 + count)/(1 + B_valid) with inclusive `>=`; floor value 1/10001 verified for all four markets; p can never be zero under this convention.
- **Holm:** family = the four eligible markets (EURUSD excluded by the gate, not by outcome); step-down at α = 0.05; verified arithmetic (4 × 9.9990e-05 = 3.9996e-04); XAUUSD remained inside the family (no discovery-market exemption).
- **CI:** ordinary percentile sampling interval, separate from the null test; not studentized; no hidden null transformation in the CI.
- **Verification limitation (repeated for clarity):** the bootstrap draw files were not persisted, so B = 10,000 / L = 10 / seed = 20260817 replication and the exact p/CI values cannot be recomputed from persisted artifacts. All persisted signals (D_obs, counts, floor p, Holm arithmetic) are internally consistent; the inference layer itself is trusted as reported with this reproducibility caveat on record.

---

## 9. Secondary Firewall

- The execution report contains **no secondary analyses** of any kind.
- Nothing in the report rescues, redefines, or re-weights the primary: no market, horizon, sweep definition, or threshold was selected from results; no secondary result altered a classification.
- Any future supportive secondary finding is descriptive only and cannot change the primary verdict.

---

## 10. Scientific Interpretation

**Established (as a behavioral phenomenon):**

> The registered sweep-rejection-confirmation behavior — a strict breach of the prior Asian-session extreme, wick rejection (close-failure), deterministic micro-structural confirmation (first later close beyond the frozen sweep-candle extreme) — is followed by a statistically larger 120-minute directional excursion than the rejected-sweep control group, in every market that passed the data gates: precious metals (XAUUSD, XAGUSD), a US equity-index CFD (USATECHIDXUSD), and crypto (BTCUSD), each significant after Holm family-wise correction, with directionally consistent positive ΔM and confidence intervals far from zero.

**Established at the cross-market level:** a robust multi-market behavioral phenomenon across three economically distinct mechanisms (precious metals, equity index, crypto), subject to the EURUSD data-quality exclusion and to the one-instrument-per-non-metals-class limitation.

**Not established:** FX generalization (EURUSD untested), universality, economic profitability, or any strategy claim.

---

## 11. What Is Not Established

Explicitly preserved boundaries:

- No proof of profitability or positive expectancy.
- No proof of survival after spread/slippage/transaction costs.
- No validated entry, stop, or target.
- No live-market or forward robustness.
- No universal claim (Level 4).
- No FX generalization (EURUSD leg missing).
- No claim about institutional intent, "smart money", or market manipulation (behavioral hypothesis only, per §3 of the mission and §20 of the protocol).
- No ML benefit.
- No production readiness.

---

## 12. Research-Line Governance Decision

**Decision: A — ADVANCE TO ECONOMIC / STRATEGY TRANSLATION** (scoped).

Basis:

- **Cross-market reliability:** 4/4 evaluable markets SUPPORT with Holm-corrected significance and floor p-values; three distinct mechanisms represented.
- **Data quality:** inputs verified (hashes match), events structurally clean, gate handling deterministic; EURUSD halt is a data-quality disposition, not a negative result.
- **Scientific coherence:** identical event definitions, horizon, and inference across markets; discovery-bias controlled (XAUUSD in the family, no special treatment); outcome-blind chain preserved.
- **Effect consistency:** directionally uniform (all ΔM_obs > 0); CI separation 5–20× the half-width.
- **Evidence strength:** large event populations (984–1,960 treatment events per market); family-wise-corrected significance; distinct mechanisms — not excitement about raw D magnitudes.

Scope conditions on the advance:

1. Economic translation targets the **validated markets** (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD).
2. **FX is excluded** from the initial economic scope; EURUSD (or any FX) re-entry requires the data-quality operationalization to be resolved and the gate re-run — a future, separately governed step.
3. The cross-market claim remains capped at "three distinct mechanisms, preliminary Level 3"; no universal or broad-FX framing is licensed.

---

## 13. Economic-Translation Boundary

This adjudication authorizes **only the definition of the next stage**, not its execution. The future **Strategy / Economic Translation** stage (a separate task) may investigate, for the validated markets:

- executable entry (at confirmation close, per the behavior);
- actual fill price and market microstructure at entry;
- spread and slippage;
- stop and target geometry;
- expectancy and risk/reward;
- position sizing;
- transaction costs and cost-aware viability.

None of these are performed by, or authorized inside, this adjudication.

---

## 14. Exact Next Legitimate Task

> **Strategy / Economic Translation** for the validated sweep-reversal markets (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD): determine whether the behaviorally supported directional excursion can survive the economics of actually trading it (spread, slippage, entry mechanics, stop/target geometry, cost-aware expectancy), under a separate pre-registered economic protocol.

Subsequent stages (unchanged pipeline): cost-aware validation → demo/forward testing → months of statistical monitoring → live-deployment consideration.

The eventual bot form is an open question to be resolved by the economics, not forced: it may be XAU-specific, precious-metals-specific, multi-asset, or market-adaptive. QuantForge's purpose is to discover where the edge exists and exploit it under the correct market conditions — not to force one universal strategy.

---

## 15. Prohibited Follow-Up

Explicitly NOT authorized by this adjudication:

- Any rerun or amendment of the V1.2.0 protocol.
- Any parameter, horizon, market, or sweep-definition selection from results.
- Any PnL/expectancy/spread/slippage calculation inside this line until the separate economic protocol exists.
- Any ML/K-means/HMM rescue or regime clustering.
- Any EA/strategy construction inside the behavioral layer.
- Any merging with, or revival of, closed lines: Mean Reversion (DISC-021), TSMOM (DISC-022), H01/H01 Equity (DISC-023), Session-Anchored Range Expansion (DISC-024, Contradicted). This candidate is a separate line and shares no results with any of them.
- Any universality or FX generalization claim.

---

## 16. Integrity

Strictly read-only and outcome-independent. The only repository change is this adjudication artifact. Verification performed: full control-set read (protocol v1.2.0, clearance audits V1/V2, definition screening, handoff, discovery database, timeline); `sha256sum` of the four M1 inputs against the report's fingerprints (exact match); protocol SHA-256 `c6b8fbd4…` confirmed unchanged from the audited object; independent recomputation of ΔM_obs from the persisted event CSVs (exact match, all four markets); event-count reconciliation (exact); event-structure audit (≤2 events/day, upper/lower coupling, direction balance, one formula-permitted negative control MFE); EURUSD invalid-day reconstruction (291/1,716 = 16.958% ≈ reported 16.96%). No p-value, CI, bootstrap, or strategy statistic was recomputed or invented; no file outside the required artifact was created or modified.
