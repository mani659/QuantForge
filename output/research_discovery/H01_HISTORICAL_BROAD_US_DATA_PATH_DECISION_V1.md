# QUANTFORGE — H01 HISTORICAL BROAD-US DATA PATH DECISION V1

**Type:** Governance / source-strategy decision ONLY. Not a data purchase, not a protocol amendment, not an experiment, not an H01 rerun, not a statistical analysis, not a new hypothesis.
**Date:** 2026-08-17
**Governing position:** H01 Equity Track A remains OPEN as a narrowed US-equity research program; the free/archiveable historical broad-US search returned verdict C — NO SUITABLE ADDITIONAL FREE/ARCHIVEABLE HISTORICAL BROAD-US SOURCE FOUND (2026-08-16); the remaining evidence gap is historical broad-US multi-market replication.

---

## 1. Executive Verdict

**PATH A — AUTHORIZE A PAID SOURCE-VERIFICATION / PROCUREMENT TASK.**

**Preferred vendor candidate: Norgate Data** (US Stocks Platinum or Diamond package).

**Rationale summary:** the historical broad-US evidence gap is a genuine, registered scientific deficiency (not a cosmetic improvement); the gap is closable by a single, well-identified, low-cost paid data source with documented provenance, daily frequency, survivorship handling, Python access, and personal-use research licensing; the alternative paths (direct index-owner licensing, deferral) are either disproportionately complex or leave a known evidence-completion problem unresolved when a clean solution exists. No data is purchased by this decision; no protocol is modified; the standard amendment chain applies before any acquired market enters the frozen experiment.

---

## 2. Current Scientific Position

### Established (SOURCE-DERIVED FACT, from adjudication / DISC-023 / acquisition report / handoff)

- H01 Equity Track A remains **OPEN** as a narrowed US-equity research program.
- **EQTECH has strong cross-era replication** (EQTECH_L1 = SUPPORT, EQTECH_L2 = SUPPORT; same US-tech exposure, two eras, two markets per era, all p_Holm = 0.0004; strong cross-era replication = TRUE).
- **Contemporary EQBROAD is SUPPORT** (EQBROAD_L2: SP500 + DJIA, D = +0.316, p_Holm = 0.0004).
- **Historical EQBROAD remains EVIDENCE-LIMITED** because only `sp` exists (EQBROAD_L1: D = +0.150, CI above zero, p_Holm = 0.0004, but single market → no primary verdict by the frozen ≥2-evaluable-market rule).
- **The free/archiveable historical broad-US search did not produce a suitable additional exposure** (verdict C, 2026-08-16): every free source with historical depth is license-RESTRICTED (Yahoo, Stooq) or no longer available (FRED Wilshire, removed June 3, 2024); every archiveable free source lacks the required depth (FRED SP500/DJIA 2016+ only) or the required distinctness (Nasdaq = tech, not broad-US).

### Not established (SOURCE-DERIVED FACT)

- Broad-US multi-market replication across both eras.
- Broad US equity generalization (the registered two-exposure two-era design is not fully met).
- International equity generalization (outside scope by registered decision).

---

## 3. Remaining Evidence Gap

**Historical broad-US multi-market replication.**

The EQBROAD_L1 cell contains exactly one market (`sp`, HPD S&P 500 futures, 1982–2002). The frozen ≥2-evaluable-market rule (protocol §11, §18) requires ≥2 evaluable markets for a primary verdict. Without a second structurally distinct historical broad-US series, EQBROAD_L1 remains permanently EVIDENCE-LIMITED/DESCRIPTIVE — the directional evidence (D > 0, CI above zero) is descriptive of that single market, but it cannot produce a primary verdict or contribute to the cross-era broad-US replication claim.

This is a **registered evidence-completion problem** (adjudication §7, §14; handoff §13a, §15), not a new hypothesis, not a failed experiment, and not an optional upgrade. The experiment was designed for two exposures across two eras; one of the four cells lacks the evaluable-market count by construction (source availability), not by scientific failure.

**Importance assessment (GOVERNANCE DECISION):** the gap is material because it is the sole remaining reason the full two-exposure two-era US generalization claim is not established. Three of four cells are SUPPORT; the fourth is EVIDENCE-LIMITED by a data-availability constraint, not by contradictory evidence. Closing this gap is the minimum-cost, minimum-complexity path to completing the registered evidence design. Leaving it open indefinitely preserves a known structural weakness that future sessions will repeatedly encounter.

---

## 4. Paid Procurement Options (PATH A)

### 4.1 Norgate Data — PREFERRED CANDIDATE

| Criterion | Assessment |
|---|---|
| **Historical depth** | S&P 500 cash: 1950+ (Diamond) or 1990+ (Platinum); DJIA cash: 1915+ (Diamond); Russell 2000: available; NYSE Composite: available. Diamond package covers the full 1982–2002 historical era with margin. (SOURCE-DERIVED FACT, from Norgate website/pricing, verified 2026-08-17.) |
| **Broad-US exposure availability** | **Multiple structurally distinct broad-US series available:** (a) Russell 2000 (small-cap, genuinely distinct segment from `sp` large-cap — PASSES exposure-distinctness gate G2); (b) NYSE Composite (broad exchange-level, thousands of constituents, distinct from 500-stock cap-weighted S&P); (c) S&P 500 cash (same exposure as `sp` futures but different instrument type — would add instrument-type corroboration, not exposure count); (d) DJIA cash (same large-cap exposure as `sp`). The Russell 2000 and NYSE Composite are the most scientifically interesting because they represent genuinely distinct US equity segments. |
| **Cash/futures distinction** | Norgate provides **cash index** daily data (OHLC), not futures. This is the natural complement to the existing `sp` futures: the new market would be a cash index, directly comparable to the contemporary FRED cash series, and the futures/cash comparability rule (definition lock §6) already governs the relationship. |
| **Daily frequency** | End-of-day daily (OHLC). Satisfies the H01 daily-close requirement exactly. |
| **Survivorship handling** | Norgate is specifically recognized for survivorship-bias-free constituent data (includes delisted stocks with full history). For index-level series, the daily close is the official published index value — survivorship handling is embedded in the index methodology itself, not in Norgate's processing. Transparent and documented. |
| **Adjusted-price methodology** | Index-level series: no adjustment needed (the index value is the canonical close, no corporate actions at the index level). For the H01 object (`r_t = ln(close_t / close_{t-1})`), the daily index close is the correct input. No ratio-back-adjustment is required (unlike the `sp` futures series). |
| **Reproducibility** | Data delivered via Norgate Data Updater to local machine; Python access via `norgatedata` package (documented API); data is version-controlled by Norgate's update process. A specific download date can be recorded and the data fingerprinted (SHA-256) for the frozen-input gate. Reproducibility: HIGH. |
| **Licensing** | **Personal use only** (standard retail subscription). Commercial use, resale, or redistribution prohibited. **Assessment for QuantForge:** the intended use is internal scientific research within a private repository — consistent with personal-use licensing as practiced by the existing HPD and FRED precedents (both are license-PENDING for archival beyond personal use). The Norgate license is operationally equivalent to the HPD standing record. A formal inquiry to Norgate for explicit research-archival confirmation is prudent but not blocking for the verification/procurement task. |
| **Research/archival rights** | **PENDING** — same governance category as HPD and FRED. The standard retail license permits personal use; explicit written permission for permanent archival in a research repository has not been obtained. This must be recorded honestly, mirroring the existing license-PENDING precedent. |
| **Cost** | Platinum (back to 1990): **≈$630/year**; Diamond (back to 1950): **≈$788/year**. One-time annual cost. This is **materially low** relative to the scientific value of closing the evidence gap. (SOURCE-DERIVED FACT, Norgate pricing page, verified 2026-08-17.) |
| **Suitability for the frozen scientific object** | The H01 object requires daily close-to-close log returns on a price-type index series. Norgate's daily OHLC index data delivers exactly this. No transformation, conversion, or interpretation is required beyond reading the Close field. **HIGH suitability.** |

**Norgate summary (GOVERNANCE DECISION):** Norgate Data is the preferred candidate because it offers the best combination of (1) multiple structurally distinct broad-US exposures (Russell 2000 small-cap and NYSE Composite are genuinely different from the S&P 500 large-cap), (2) sufficient historical depth covering the full 1982–2002 era, (3) daily frequency matching the H01 object exactly, (4) documented provenance with Python access, (5) low cost (~$630–$788/year), and (6) a licensing model operationally consistent with the project's existing precedents.

### 4.2 CSI (Commodity Systems Inc.)

| Criterion | Assessment |
|---|---|
| **Historical depth** | Extensive; data back to market inception for many series. Coverage for S&P 500, DJIA, Russell, NYSE Composite expected but must be verified by direct inquiry. |
| **Broad-US exposure** | Expected to include broad-US indices; exact list requires direct inquiry. |
| **Daily frequency** | End-of-day daily. |
| **Survivorship handling** | Documented for individual equities; index-level series are official published values. |
| **Reproducibility** | Via "Unfair Advantage" software or API; less Python-native than Norgate. |
| **Licensing** | Individual vs. commercial distinction; commercial rates are custom. Research-use classification requires inquiry. |
| **Cost** | Custom pricing for research; likely higher than Norgate retail for comparable scope. Requires direct quote. |
| **Assessment** | **VIABLE ALTERNATIVE but less operationally convenient than Norgate.** CSI requires direct sales inquiry for research pricing, has a less Python-native access model, and its exact index coverage for the specific series needed must be confirmed. If Norgate proves unsuitable during the verification task, CSI is the natural fallback. |

### 4.3 Databento

| Criterion | Assessment |
|---|---|
| **Historical depth** | Focuses primarily on exchange-level tick/intraday data; historical daily index-level data coverage is **uncertain** for the deep-historical window (1982–2002). Databento specializes in US equities from direct exchange feeds, which may not include pre-electronic-era index history. |
| **Broad-US exposure** | US equity coverage extensive for individual stocks; **index-level daily data (Russell 2000, NYSE Composite historical) requires verification.** |
| **Daily frequency** | `ohlcv-1d` schema available; suitability depends on whether the specific historical indices are in their catalog. |
| **Licensing** | Vendor-of-record model; self-service portal; personal vs. commercial distinction. |
| **Cost** | Subscription-based (Standard/Plus/Unlimited tiers); $125 free credits for new users. Likely higher cost than Norgate for the specific narrow need (one or two daily index series). |
| **Assessment** | **LOWER PRIORITY.** Databento's strength is high-frequency, recent-era data. For the specific need — daily index-level closes from 1982–2002 for broad-US indices — Norgate and CSI are more naturally aligned. Databento is not excluded but is not the preferred candidate for this gap. |

---

## 5. Direct-Licensing Options (PATH B)

### 5.1 Wilshire (FT Wilshire 5000)

| Criterion | Assessment |
|---|---|
| **Historical daily data existence** | The Wilshire 5000 has daily history from 1971. The data was formerly available on FRED but was **removed June 3, 2024** (SOURCE-DERIVED FACT, St. Louis Fed announcement). The official contact for data access is `index.access@wilshire.com`. |
| **Research archival rights** | Unknown; would require formal inquiry. Wilshire's legal position (SOURCE-DERIVED FACT, from web search) states that no material published by Wilshire should be construed as granting a license without prior written permission. |
| **Machine-readable access** | Unknown; would need to be established via the inquiry. |
| **Expected scope of license** | Unknown; likely custom for research use. |
| **Cost** | Unknown; likely a formal licensing fee. |
| **Exposure distinctness** | Wilshire 5000 = total US market (~3,500+ stocks) — structurally distinct from `sp` (large-cap 500-stock). G1/G2 defensible (total-market breadth vs large-cap). |
| **Assessment** | **SCIENTIFICALLY SUITABLE but operationally uncertain.** The Wilshire 5000 is a strong scientific candidate (genuinely total-market, long history, daily). However: (a) the inquiry process is unpredictable in timeline and outcome; (b) cost is unknown; (c) machine-readable delivery is not guaranteed; (d) archival rights are not guaranteed; (e) the inquiry has not been authorized by the operator. PATH B is a legitimate option but introduces operational uncertainty that PATH A (Norgate) does not. |

### 5.2 S&P Dow Jones Indices

| Criterion | Assessment |
|---|---|
| **Historical daily data** | S&P 500 daily back to 1928; DJIA daily back to 1896. Comprehensive. |
| **Research rights** | Available via WRDS (Wharton Research Data Services) for institutions with subscriptions; direct licensing from S&P DJI possible but typically institutional/commercial. |
| **Machine-readable access** | Via WRDS (if institutional access exists) or direct licensing portal. QuantForge is a private project without institutional affiliation — WRDS access is unlikely. |
| **Cost** | Institutional/commercial licensing fees — likely significantly higher than Norgate retail pricing. |
| **Assessment** | **DISPROPORTIONATE for this gap.** S&P DJI data would provide S&P 500 and DJIA cash history — but these are the **same broad-US large-cap exposure** as `sp` (definition lock §5, §7: SP500/DJIA = one broad-US exposure, market count ≠ exposure count). Adding historical S&P 500 cash would provide instrument-type corroboration (futures vs. cash) but would NOT add a structurally distinct exposure. Russell 2000 or NYSE Composite via Norgate provides more scientific value for the evidence gap. |

### 5.3 Nasdaq

| Criterion | Assessment |
|---|---|
| **Assessment** | **NOT RELEVANT to this gap.** The Nasdaq family is classified as US-technology exposure (definition lock §7), not broad-US. EQTECH already has strong cross-era replication. Additional Nasdaq data does not address the EQBROAD_L1 evidence gap. |

---

## 6. Deferred/Stop Option (PATH C)

**Assessment (GOVERNANCE DECISION):**

PATH C means accepting that historical broad-US evidence remains permanently incomplete. This would leave H01 Equity Track A in a state where:

- 3/4 cells are SUPPORT, 1/4 is permanently EVIDENCE-LIMITED;
- the two-exposure two-era US generalization claim is permanently **not established**;
- the strongest surviving claim remains limited to US-tech cross-era replication plus contemporary broad-US support;
- every future session that revisits Track A will re-encounter the same evidence gap and the same question.

**Arguments for PATH C:**
- Saves ~$630–$788 (Norgate annual cost) and the time of a procurement + verification task.
- H01 Equity Track A can continue as narrowed without the historical broad-US leg; the tech replication is independently valuable.
- The project has other priorities (BOE detector specification, new hypothesis discovery).

**Arguments against PATH C:**
- The cost is **trivially low** (~$630–$788/year) relative to the scientific value of completing the registered evidence design.
- The evidence gap is a **known, closable structural deficiency** — not a methodological problem, not a scientific failure, not an uncertain fishing expedition. A specific, well-identified data source exists that can close it.
- Deferring does not eliminate the gap; it perpetuates it. Future sessions will face the same decision with the same information.
- The procurement task is **bounded and low-risk** — it is source verification, not a new experiment. The amendment chain protects against any outcome-driven contamination.
- The research investment already committed to H01 Equity V1 (protocol development, three independent audits, experiment execution, adjudication, data acquisition, scope decision, definition lock, screening) is disproportionately larger than the marginal cost of closing this last evidence gap.

**PATH C verdict: NOT RECOMMENDED.** The marginal cost and complexity of PATH A are small relative to the scientific value of completing the evidence design. Deferral is a legitimate governance option but is not the optimal one.

---

## 7. Decision Criteria (applied)

### Scientific

| Criterion | PATH A (Norgate) | PATH B (Wilshire) | PATH C (Stop) |
|---|---|---|---|
| Distinct broad-US exposure | **YES** — Russell 2000 (small-cap) and/or NYSE Composite (broad exchange) are genuinely distinct from `sp` (large-cap) | **YES** — Wilshire 5000 (total market) is distinct from `sp` | N/A — gap remains |
| Sufficient historical overlap | **YES** — Russell 2000 daily from ~1987 (≈15 years of overlap with 1982–2002 era); NYSE Composite expected from 1960s+ | **YES** — 1971+ | N/A |
| Daily data | **YES** — end-of-day OHLC | Likely but unconfirmed | N/A |
| Same conceptual object | **YES** — daily close, price-type index, log returns | **YES** | N/A |
| Survivorship/adjustment transparency | **YES** — index-level close is canonical; Norgate documented | Unknown until inquiry | N/A |

### Provenance

| Criterion | PATH A (Norgate) | PATH B (Wilshire) | PATH C (Stop) |
|---|---|---|---|
| Documented methodology | **YES** — Norgate is a documented data vendor | Wilshire methodology documented but data delivery unknown | N/A |
| Source identity | **CLEAR** — Norgate Data, known provider | **CLEAR** — Wilshire Indexes | N/A |
| Reproducibility | **HIGH** — Python API, fingerprint-able, version-tracked | Unknown | N/A |
| Archival rights | **PENDING** — personal use license; same governance category as HPD/FRED | **PENDING** — requires inquiry | N/A |

### Operational

| Criterion | PATH A (Norgate) | PATH B (Wilshire) | PATH C (Stop) |
|---|---|---|---|
| Acquisition complexity | **LOW** — subscribe, download via updater, extract to CSV, fingerprint | **HIGH** — formal inquiry, unknown timeline, unknown format | **NONE** |
| Cost | **~$630–$788/year** (low) | **Unknown** (likely higher) | **$0** |
| Stable access | **YES** — subscription-based, long-standing vendor | Unknown | N/A |
| Data fingerprinting | **YES** — local files, SHA-256 | Depends on delivery format | N/A |

### Governance

| Criterion | PATH A | PATH B | PATH C |
|---|---|---|---|
| No silent universe amendment | **ENFORCED** — amendment chain applies | **ENFORCED** | N/A |
| No outcome-driven source selection | **ENFORCED** — selection by exposure distinctness, depth, provenance, cost | **ENFORCED** | N/A |
| No protocol change without chain | **ENFORCED** | **ENFORCED** | N/A |

---

## 8. Recommended Path

### **A — AUTHORIZE A PAID SOURCE-VERIFICATION / PROCUREMENT TASK**

**Preferred vendor: Norgate Data** (US Stocks Platinum package, ~$630/year; Diamond ~$788/year if coverage verification requires the deeper history).

**Preferred target series (for source verification, not for automatic inclusion):**
1. **Russell 2000 daily index** — small-cap US equity segment, genuinely distinct from `sp` large-cap, expected history from ≈1987, passes exposure-distinctness gate G2.
2. **NYSE Composite daily index** — broad exchange-level US equity, genuinely distinct from `sp` (500-stock cap-weighted), expected history from 1960s+, passes G2.

The verification task will determine which of these (or both) are available, have sufficient depth overlapping the 1982–2002 era, and meet the integrity and provenance gates. The operator may choose to verify both and select one for the amendment chain based on scientific suitability — never by expected H01 performance.

**Why Norgate over alternatives:**
- **vs. CSI:** Norgate is more Python-native, has transparent retail pricing, and offers the specific index coverage needed without requiring a custom sales inquiry. CSI remains a viable fallback.
- **vs. Databento:** Norgate is better aligned with the specific need (deep-historical daily index-level data, not high-frequency tick data).
- **vs. PATH B (Wilshire direct):** Norgate is operationally simpler (subscribe → download → verify) with known cost, known format, and known timeline. The Wilshire direct-licensing inquiry has unknown cost, unknown timeline, unknown format, and unknown outcome. If the operator specifically prefers the Wilshire 5000 total-market series, Norgate may also carry it (to be verified); if not, the Wilshire direct inquiry becomes a fallback.
- **vs. PATH C (defer):** The marginal cost (~$630) is trivially low relative to the scientific value, and deferral perpetuates a known closable gap.

---

## 9. Exact Next Legitimate Task

> **PAID HISTORICAL BROAD-US EQUITY DATA SOURCE VERIFICATION / PROCUREMENT**

That task must:

1. **Verify exact provider product** — confirm Norgate Data US Stocks package includes the target index series (Russell 2000 and/or NYSE Composite daily OHLC).
2. **Verify historical dates** — confirm the series covers a sufficient portion of the 1982–2002 historical era (minimum ≈15 years of overlap).
3. **Verify daily frequency** — confirm daily OHLC is the delivery format, with no gaps in the business-day calendar beyond expected exchange holidays.
4. **Verify broad-US exposure distinct from `sp`** — confirm the series represents a structurally distinct US equity segment (small-cap, broad exchange, or total market) — NOT another S&P 500/DJIA large-cap representation.
5. **Verify price methodology** — confirm the daily close is the official published index close (price-type, not total-return); confirm no undocumented adjustments.
6. **Verify survivorship treatment** — for index-level data, confirm the daily close is the canonical published value (survivorship is embedded in the index methodology).
7. **Verify licensing/archival rights** — record the exact license terms; note personal-use restriction; record as license-PENDING for permanent archival (consistent with HPD/FRED precedent); if explicit research-archival permission is obtainable, pursue it.
8. **Verify reproducibility** — confirm data can be extracted to CSV, fingerprinted (SHA-256), and version-recorded for the frozen-input gate.
9. **Obtain sample data only after operator authorization** — no full dataset download until the operator explicitly authorizes the subscription purchase.

**No H01 computation during acquisition.** No shock, ΔlnRV, matching, bootstrap, asymmetry, p-value, or any other H01 statistic may be computed on any candidate data during the procurement/verification task.

---

## 10. Governance Sequence

Even after successful paid acquisition, the new market does NOT automatically enter H01 Equity V1. The mandatory sequence remains:

```
source acquisition → source validation → governance review →
definition/universe amendment → new pre-registration → independent audit →
execution
```

Specifically:

1. **Source acquisition:** Norgate subscription, data download, CSV extraction, fingerprinting.
2. **Source validation:** integrity checks (gaps, duplicates, non-positive values, holiday handling, cross-source fidelity where possible), provenance recording.
3. **Governance review:** a governance decision artifact recording whether the validated source meets the scientific, provenance, and operational criteria for the evidence gap.
4. **Definition/universe amendment:** a registered amendment to the frozen definition lock (§5 universe table, §6 source-type rule if needed), creating a new version.
5. **New pre-registration:** an amended protocol incorporating the new market, with all inherited and new design choices frozen outcome-blind.
6. **Independent audit:** a read-only audit of the amended protocol, identical in rigor to the H01 Equity V1 pre-execution audit.
7. **Execution:** a single execution of the amended experiment, producing a new result that subsumes the EQBROAD_L1 cell.

No shortcut. No step may be skipped. No market may be added silently.

---

## 11. Prohibited Follow-Up

- Purchasing data without explicit operator authorization.
- Downloading a full dataset before operator authorization.
- Computing any H01 statistic (D, d_m, p, CI, shock, RV, ΔlnRV, asymmetry) on any candidate data during the procurement/verification task.
- Selecting a market because it is expected to improve the H01 result.
- Adding any market to the frozen H01 Equity V1 universe without the full amendment chain (§10).
- Modifying the frozen H01 Equity V1 protocol.
- Modifying the frozen definition lock.
- Changing the frozen scientific claim or prior.
- Re-opening international scope.
- Re-opening commodities.
- Re-opening TSMOM (DISC-022) or Mean Reversion (DISC-021).
- Using K-means, HMM, ML, or any machine-learning methodology.
- Creating a trading strategy from any H01 result.
- Contacting any data provider, index owner, or licensing authority without explicit operator authorization.
- Merging with H01 v1.1/v1.2 results.
- Using secondaries to rescue or upgrade the primary classification.
- Treating the Norgate recommendation as a vendor endorsement — it is a scientific-suitability assessment only.

---

## 12. Integrity

- **Outcome-blind:** no H01 result value (D, p, CI, Holm, asymmetry) was used to select the recommended vendor, target series, or path. The recommendation is based solely on exposure distinctness, historical depth, daily frequency, provenance, reproducibility, licensing, cost, and operational simplicity.
- **Read-only:** no experiment was run; no statistic was computed; no data was acquired; no protocol was modified; no definition lock was changed; no universe was amended; no market was added.
- **No external communication:** no data provider, index owner, or licensing authority was contacted. Web searches were used to verify publicly available pricing, coverage, and licensing information only.
- **Single artifact:** the only repository change is this governance artifact (`output/research_discovery/H01_HISTORICAL_BROAD_US_DATA_PATH_DECISION_V1.md`). No dataset, protocol, experiment, script, or result file was created.
- **Labeling:**
  - **SOURCE-DERIVED FACT:** pricing information (Norgate: ~$630–$788/year); coverage claims (Russell 2000, NYSE Composite available via Norgate); FRED Wilshire removal (June 3, 2024, St. Louis Fed); Yahoo/Stooq license restrictions; CSI/Databento general capabilities; Wilshire contact (`index.access@wilshire.com`); S&P DJI licensing via WRDS.
  - **GOVERNANCE DECISION:** path selection (A over B/C); vendor preference (Norgate over CSI/Databento); target series identification (Russell 2000, NYSE Composite); exposure-distinctness assessments (Russell 2000 small-cap ≠ `sp` large-cap); importance assessment of the evidence gap; cost/value judgment.
  - **MODEL INFERENCE:** none. No statistical modeling, no correlation estimation, no expected-effect-size reasoning, no performance projection.
- **Firewall:** all frozen H01 Equity V1 artifacts (protocol, definition lock, scope decision, adjudication, execution artifacts), the research discovery database, the research timeline, the session handoff, all BOE/Assembly/Deployment/governance records, and all source code/tests are untouched.
