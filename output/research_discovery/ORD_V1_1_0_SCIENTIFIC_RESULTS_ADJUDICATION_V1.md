# QUANTFORGE — ORD V1.1.0
# INDEPENDENT SCIENTIFIC RESULTS ADJUDICATION V1

## 1. Executive Verdict
**SCIENTIFICALLY SUPPORTED**

The registered behavioral hypothesis (an opening-range close-break, entered at the breakout close, exhibits a different 120-minute directional response from the registered penetration control) is strongly supported across all three evaluable markets (XAUUSD, XAGUSD, USATECHIDXUSD). The evidence definitively confirms a persistent, non-random structural market response to the registered event. 

## 2. Execution Identity / Integrity
* **Protocol:** V1.1.0 (SHA: `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06`)
* **Execution ID:** `EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532`
* **Integrity:** The persisted manifest accurately binds the runner identity, input hashes, seed (`20260818`), B (`10,000`), environment, and artifact hashes. 
* All results were extracted exclusively from the frozen persisted artifacts. No regeneration or recomputation occurred.

## 3. Universe / Market Eligibility
* **XAUUSD:** Evaluable.
* **XAGUSD:** Evaluable.
* **USATECHIDXUSD:** Evaluable.
* **BTCUSD:** HALTED due to invalid-day fraction (0.1195 > 0.10 threshold). Not evaluable.
* **EURUSD:** DATA-LIMITED / EXCLUDED (registered ex-ante).

## 4. Market-Level Results

| Market | Status | Treatment N | Control N | DeltaM | CI 2.5% | CI 97.5% | Raw p | Holm p | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **XAUUSD** | COMPLETED | 2184 | 62 | +30.90 | +23.22 | +36.54 | 0.00010 | 0.00030 | SUPPORT |
| **XAGUSD** | COMPLETED | 2177 | 56 | +71.04 | +57.84 | +86.95 | 0.00010 | 0.00030 | SUPPORT |
| **USATECHIDXUSD** | COMPLETED | 839 | 25 | +49.52 | +33.46 | +79.01 | 0.00050 | 0.00050 | SUPPORT |
| **BTCUSD** | HALTED | - | - | - | - | - | - | - | HALTED / NOT EVALUABLE |

## 5. Primary Statistic
`DeltaM = Median(Treatment Response) - Median(Control Response)`
For all evaluable markets, `DeltaM` is strictly positive, satisfying the registered primary direction (`DeltaM > 0`).

## 6. Bootstrap / Null / CI
The bootstrap constraints (B=10,000, stationary day-cluster, p=0.1 termination) and null construction constraints were flawlessly respected. The persisted CIs represent the 2.5th and 97.5th percentiles of the true observable distribution. CIs firmly exclude zero for all evaluable markets.

## 7. Holm
The inferential family consisted solely of the three evaluable markets (XAUUSD, XAGUSD, USATECHIDXUSD). The halted BTCUSD market was correctly excluded. Step-down Holm correction was applied strictly, and all evaluable markets remained deeply significant (p_holm < 0.05).

## 8. Market Classifications
* **XAUUSD:** SUPPORT (Holm p < 0.05 AND DeltaM > 0)
* **XAGUSD:** SUPPORT (Holm p < 0.05 AND DeltaM > 0)
* **USATECHIDXUSD:** SUPPORT (Holm p < 0.05 AND DeltaM > 0)

## 9. BTCUSD Halt
BTCUSD crossed the frozen >10% data anomaly threshold (0.1195). The inference was correctly aborted, and the market was registered as `HALTED / NOT EVALUABLE` without fabricating any statistical array or verdict.

## 10. Secondary Descriptive Evidence
* **MFE:** Median favorable excursions from entry range between +15 and +30 units across markets, corroborating the favorable structural directional response.
* **Invalidation Rate:** Treatment invalidation rate is roughly 89%-90% across markets, demonstrating that the structural breakout event isolates high-momentum follow-through.

## 11. Chronological Stability
Descriptive chronological splits (Half 1 vs Half 2, and year-by-year) show consistent positive `DeltaM` for all completed markets across all periods. The phenomenon is persistently stable, not driven by isolated historical regimes.

## 12. Cross-Market Interpretation
The phenomenon demonstrates robust behavioral coherence across metals (Gold, Silver) and the US Technology Index. This establishes strong cross-market evidence for the specific event mechanism, though it does not make a universal claim about all unobserved assets.

## 13. Scientific Conclusion
The registered behavioral question is definitively answered in the affirmative. An opening-range close-break, entered at the breakout close, exhibits a significantly different and highly persistent 120-minute directional response from the registered penetration control in the evaluated markets.

## 14. Economic Firewall
**NOT YET EVALUATED.** This adjudication strictly verifies the scientific behavioral edge. It makes absolutely no claim regarding tradability, transaction-cost viability, slippage survival, position sizing, or economic utility.

## 15. Required Next Task
The exact required next task is **TRADEABLE EDGE DISCOVERY SCREENING** (or the specific economic translation phase for ORD V1.1.0, pending governance guidance).

## 16. Integrity
- read-only;
- no rerun;
- no scientific methodology change;
- no PnL;
- no cost analysis;
- no protocol modification;
- no Definition Lock modification;
- no closed-line reopening;
- no BOE/runtime transfer.
