# QUANTFORGE — INDEPENDENT H01 EQUITY V1 SCIENTIFIC-RESULTS ADJUDICATION

**Adjudicated object:** the completed H01 Equity V1 experiment (protocol v1.1.0; `SCIENTIFIC_REPORT_H01_EQ_V1.md`; artifact set under `H01_EQUITY_VOLATILITY_ASYMMETRY/`).
**Mode:** strict, independent, READ-ONLY. No experiment rerun, no bootstrap, no new statistic, no protocol change, no data acquisition, no new hypothesis. Uses only persisted execution results and the frozen registered rules.
**Question asked:** *What scientific claim has this exact registered experiment actually earned the right to make?*

---

## 1. Execution Integrity (verified from persisted artifacts)

- Protocol v1.1.0; protocol SHA-256 `a97cd0e27394cb83cce1a37e5369a182aad407a11e450b9385d30f9390f0d6ab` matches the frozen file.
- seed = 20260816, B = 10,000, L = 11 — recorded in `experiment_metadata_H01_EQ_V1.json` and reproduced in the results.
- Single invocation, serial (1 worker), no checkpoint/resume, no concurrent runs (metadata `single_invocation: true`, `workers: 1`); duration 1,296.7 s, peak RSS 78.2 MB, no resource-pressure events.
- All five input fingerprints matched the registered hashes (GATE 1 PASS); all other gates passed.
- Post-execution independent recomputation from persisted artifacts reproduces every p-value (all = 0.000100, count = 0/10,000), every percentile CI, every Holm value (all = 0.000400), every D_obs, and every verdict label exactly (to 1e-12). Decision labels match the protocol §23 rules.

## 2. Primary Results (persisted, unchanged)

| Cell | D_cell | CI 95% | count/10,000 | p_raw | p_Holm | Evaluable markets | Verdict |
|---|---|---|---|---|---|---|---|
| EQBROAD_L1 | +0.150 | [0.079, 0.193] | 0 | 0.00010 | 0.00040 | sp (1) | **EVIDENCE-LIMITED/DESCRIPTIVE** |
| EQBROAD_L2 | +0.316 | [0.234, 0.389] | 0 | 0.00010 | 0.00040 | SP500, DJIA (2) | **SUPPORT** |
| EQTECH_L1 | +0.208 | [0.154, 0.264] | 0 | 0.00010 | 0.00040 | NASDAQ100, NASDAQCOM (2) | **SUPPORT** |
| EQTECH_L2 | +0.330 | [0.236, 0.392] | 0 | 0.00010 | 0.00040 | NASDAQ100, NASDAQCOM (2) | **SUPPORT** |

All 7 market-level d_m are positive (classic direction); within-cell directional consistency = 1.0 everywhere; EQTECH strong cross-era replication = **TRUE** (persisted `strong_replication_eqtech`). The frozen v1.2 firewall holds: no v1.1/v1.2 result was merged, no v1.2 value selected any market or method, and this result stands on its own corrected inference (data-level null construction, `(1+count)/(B+1)`, Holm over the 4-cell family).

## 3. What the Experiment Establishes — the Core Distinction

**The protocol establishes the second, narrower statement, not the first:**

> "Classic asymmetry is strongly supported in the tested US equity exposures, with one broad-US historical cell evidence-limited and the tech exposure replicated across eras."

**It does not establish** — as a formal, registered conclusion — "classic asymmetry generalizes across US equity-index markets." Reasons, all from frozen rules: (i) the definition lock registers that the generalization claim rests on **exposure count**, not market count, and only **two** exposures were tested; (ii) the broad-US exposure has **no strong two-era support** (historical leg is single-market → EVIDENCE-LIMITED by construction, §16/§20); (iii) the scope decision explicitly frames even the US-only claim as "US-anchored but generalization-framed: multiple independent exposures per era" — a two-exposure design with one replicated exposure does not complete that framing.

The directional statement "consistent classic direction in every tested cell, all significant" is true and strong; the *generalization* content is narrower than the sentence "across US equity-index markets" implies.

## 4. Exposure-Level Evidence

**Broad-US exposure (SP500/DJIA family; `sp` futures historically):**
- Historical: `sp` only → **EVIDENCE-LIMITED/DESCRIPTIVE** (D = +0.150, CI above zero, p_Holm = 0.0004, but no primary verdict by the frozen ≥2-market rule).
- Contemporary: SP500 + DJIA → **SUPPORT** (D = +0.316, both markets classic, consistency 1.0).
- Cross-era: descriptive directional consistency only; **EVIDENCE-LIMITED, never strong replication** (§20). No strong two-era broad-US replication is established.

**US-tech exposure (NASDAQ100/NASDAQCOM; FRED cash both eras):**
- Historical: 2 markets → **SUPPORT** (D = +0.208).
- Contemporary: 2 markets → **SUPPORT** (D = +0.330).
- Same exposure definition across two eras (~30 years apart), both eras multi-market and family-significant → **strong cross-era replication established**.

**Overall:** the result supports a **two-exposure US-equity claim only asymmetrically** — fully for the tech exposure (markets × eras), contemporarily for the broad-US exposure, and descriptively (single market) for historical broad-US. It does **not** support a balanced two-exposure two-era US generalization.

## 5. Nested / Near-Duplicate Interpretation (frozen accounting)

- NASDAQ100 ⊂ NASDAQCOM = **one** technology exposure (registered: market count ≠ exposure count); their mutual agreement corroborates within-exposure reproducibility but adds no exposure count.
- SP500/DJIA = **one** broad-US exposure; same logic.
- The experiment therefore provides **2 independent exposures and 7 market observations**, not 7 independent replications. The two within-exposure pairs each agreeing (consistency 1.0) is genuine corroboration that the effect is not idiosyncratic to a single index, but the *independence* carriers of the generalization claim are the two exposures — and one of them (broad-US) lacks strong historical support.

## 6. Cross-Era Tech Replication — Correctly Used

"EQTECH strong cross-era replication = TRUE" is correctly used under the frozen rules (§20, §23): same underlying exposure definition and source type (FRED cash indices, both eras); both eras have ≥ 2 evaluable markets; both cells SUPPORT; both directions classic (D > 0); both survive Holm (p_Holm = 0.0004 < 0.05); no secondary analysis was involved. This is the strongest registered claim in the experiment and it is valid.

## 7. Broad-US Cross-Era — Correctly Limited

The report's treatment is correct: contemporary-only **SUPPORT**; historical **EVIDENCE-LIMITED/DESCRIPTIVE**; cross-era comparison **EVIDENCE-LIMITED, never "confirmed" or "replicated"** as strong evidence. The frozen single-market rule is not weakened: EQBROAD_L1's tiny p-value does not convert a one-market cell into a primary verdict.

## 8. Secondary Firewall — Intact

Secondaries (1-day, 21-day, standardized, winsorization, absolute-return, common-window, GJR/EGARCH, Engle–Ng, MT5 reference, futures/cash context) were declared non-rescuing and were not used to change any primary verdict. The 21-day historical `sp` descriptive value (−0.067) does not overturn the frozen 5-day primary; the positive 1-day/winsorized/common-window values do not strengthen it. GJR/EGARCH boundary-clamped coefficients remain non-confirmatory per the protocol's mandatory statement. Firewall verified intact.

## 9. V1.2 Firewall — Intact

H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / UNADJUDICATED; the v1.2 broad-class results (including the commodity contradiction) were not merged into this experiment; the v1.1 inference defect is irrelevant to this experiment's corrected null construction; no v1.2 effect selected markets or methods (market choice by identity/provenance; parameters by object-identity and registered constants). The Equity V1 result stands on its own protocol.

## 10. Scientific Claim Boundary

| Claim | Status |
|---|---|
| A — "Classic asymmetry exists in the tested equity indices" | **SUPPORTED** (all 4 cells significant, all classic direction) |
| B — "Generalizes across two US equity exposures" | **PARTIALLY SUPPORTED** — full for US-tech (markets × eras); contemporary-only for broad-US; historical broad-US descriptive single market |
| C — "Generalizes across US equity markets broadly" | **NOT ESTABLISHED** — 2 exposures only; only one exposure has two-era strong replication; market-broad wording overstates the registered evidence |
| D — "Established universal equity-market law" | **NOT ESTABLISHED — overclaim**; no international evidence, no broad-exposure coverage |

No international claim is made or authorized by any frozen document.

## 11. Evidence Strength (distinguished dimensions)

- **Statistical reliability:** maximal at the registered scale — every cell at the Monte-Carlo floor (count = 0/10,000, p = 1/10001), CIs bounded away from zero.
- **Cross-market consistency:** high within exposures (consistency 1.0, all 7 markets classic).
- **Exposure diversity:** **low** — 2 exposures; the historical era contains only one broad-US market.
- **Cross-era replication:** strong for US-tech; absent (evidence-limited) for broad-US.
- **Geographic breadth:** none (US only by registered scope).
- **Market independence:** within-exposure pairs are near-duplicates by registered accounting; the two exposures are the only independent carriers.
- **Conclusion:** tiny p-values do **not** by themselves purchase broad generalization; the strength of this experiment is the *combination* of within-exposure market corroboration, family-level significance, and — for the tech exposure — cross-era replication.

## 12. Overall Scientific Classification

**No global classification statistic was pre-registered** — the protocol defines per-cell verdicts (§23) and per-exposure cross-era strong replication (§20) only. This audit therefore gives a governance interpretation, not a new formal statistic:

- Cells: **3 SUPPORT, 1 EVIDENCE-LIMITED, 0 CONTRADICTION, 0 INCONCLUSIVE**; EQTECH strong replication TRUE.
- Track-A question as registered ("does the classic negative-shock volatility-response asymmetry generalize beyond the two single-market observations?"): **SUPPORTED WITHIN THE US-ANCHORED SCOPE AS EXECUTED** — the tech exposure generalizes across markets and eras; the broad-US exposure generalizes contemporarily with a descriptive historical confirmation.
- The **full two-exposure two-era US generalization** and any broader/international claim are **NOT established**.

## 13. Research-Line Governance Decision

**B — CONTINUED AS A NARROWED EQUITY RESEARCH PROGRAM.**

The track is neither closed (C) nor inconclusive (D): three of four cells support the registered prior at the significance floor, the tech exposure replicates across eras, and no contradiction appeared anywhere. It is not promoted (A) beyond its registered scope: the historical broad-US leg is single-market, exposure diversity is two, and the definition lock's generalization framing ("multiple independent exposures per era") is not fully met. The correct status is an evidence-backed, scope-limited continuation whose strongest surviving claim is the **US-tech cross-era replication** (with contemporary broad-US support as the second leg).

## 14. Historical Broad-US Evidence Gap — Governance Category

The question "should a second historical broad-US series be pursued?" is **a legitimate evidence-completion continuation**, governed as follows:

- **Category:** (a) a **data-acquisition / source-verification task** to fill the EQBROAD_L1 evidence gap — acquisition is independent of the frozen experiment and needs no protocol change; and, if acquisition succeeds, (b) a **registered definition/universe amendment decision** (the frozen universe is "exactly the markets of §5; no market added/removed" — GATE 2), which would require the full definition → pre-registration → independent audit → execution chain.
- It is **not** a silent addition to the frozen experiment and **not** a new hypothesis. It is completing an existing, registered evidence gap in the narrowest possible way (historical broad-US replication).
- **Not authorized here:** no acquisition, no source selection, no amendment. Only the governance category is determined.

## 15. Exact Next Legitimate Task

The narrowest next legitimate task is the **H01 Equity V1 adjudication acceptance** (this audit's outcome recorded to the research timeline/handoff), followed — if the operator so decides — by a **data-acquisition/source-verification task for a second validated historical broad-US series** (outcome-blind; no market selected from this result; the existing FRED/historical-cash/paid-vendor sourcing paths already documented in `H01_EQUITY_DATA_ACQUISITION_V1.md`). Any subsequent universe change would require a separate registered amendment cycle. International expansion is **not** justified by this evidence and remains closed by the scope decision until a separately authorized acquisition path exists.

## 16. Prohibited Follow-Up

- Re-running or tuning the executed experiment; recomputing alternative p-values or bootstraps.
- Converting EQBROAD_L1 into a primary verdict by any means (no single-market promotion).
- Using secondaries (especially the 1-day or common-window results) to upgrade the primary classification.
- Adding markets to the frozen universe without a registered amendment chain.
- Claiming US-market-broad or international generalization.
- Using the result as a trading signal, regime filter, volatility detector, or TSMOM overlay.
- Merging with H01 v1.1/v1.2 results; reopening commodities; reviving the universal H01 claim.

## 17. Runtime Firewall — Confirmed

No volatility detector, BOE, StrategyManifest, Assembly, Deployment, production threshold, trading, or live-strategy connection exists or is implied by this result. The finding is research evidence only; any future scientific-to-runtime transfer would require a separate Scientific Specification Readiness Review per project governance.

## 18. Integrity

This adjudication was strictly read-only: no experiment was rerun, no bootstrap or statistic computed, no file other than this adjudication artifact was created or modified, no market/parameter/rule changed, and no outcome was used to select anything. All scientific claims in this document are drawn from the persisted execution artifacts and the frozen registered rules (definition lock §5/§7/§15/§16; protocol §16/§20/§23; scope decision; acquisition report), which were read only. The H01 Equity V1 artifact set, the H01 v1.1/v1.2 records, and all BOE/Assembly/Deployment/governance files are untouched.
