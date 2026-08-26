# QUANTFORGE — ORD V1.1.0 ECONOMIC TRANSLATION REPORT

# STAGED EXECUTION — V2.0.1 STAGE 2 (THE ONE CONTROLLED ECONOMIC EXECUTION)

## 1. Execution Identity

- Execution ID: `EXECUTION_20260824T130709Z_0c18d950-aa99-4e90-af55-6847f8134542`
- Started (UTC): 2026-08-24T13:07:09.661278+00:00
- Output directory: `output\research_discovery\ORD_STAGE2_XAGUSD_EXEC_01\ORD_ECONOMIC\V1.1.0\EXECUTION_20260824T130709Z_0c18d950-aa99-4e90-af55-6847f8134542`
- Journal final state: COMPLETED (verified by EventStudyRecorder completion gate).

## 2. Protocol / Implementation Fingerprints

- Staged economic protocol (V2.0.1): `1D3EE7A6A9FD747CB57A716B43C5EB80BB7D6016011D2C4DF9F0814CC196968D`
- Economic base protocol (V1.1.0): `1d3ee7a6a9fd747cb57a716b43c5eb80bb7d6016011d2c4df9f0814cc196968d`
- Scientific protocol (V1.1.0): `85263B848E49E718A099CAFE8FA7FE6F8AE0C74EC04C46477A0FCD1D9E759C06`
- Stage-1 preparation hashes (full, unabbreviated): {'XAGUSD': '07BACB1E396BBA517E0F46F461C3CB48B94E5E9ABB2F30D67A025B810A67C736'}
- Stage-1 preparation identities: {'XAGUSD': 'PREP_XAGUSD_07BACB1E396BBA517E0F46F461C3CB48B94E5E9ABB2F30D67A025B810A67C736'}
- Definition lock SHA-256: `b58105404d277560eec31a8b08c5b1997b86a03904fc4a804e87beaac448ab30`
- Runner SHA-256: `974184bc26c973d4e485662bdc5e48a97be3b429f7bbc5ad0b71dbe8347f1aae`
- Git HEAD: `3921cf1f778c36c351b8b9662672afd1514188fe` (dirty=True)
- Python 3.11.9; pandas 3.0.2; numpy 2.4.4

## 3. Input Data Integrity

- Stage-2 consumed ONLY frozen Stage-1 preparations; each was re-verified
  byte-exact (full `PREP_<market>_<hash>` identity recomputed from current
  source hashes + artifact hashes) before any economic calculation.
  - XAGUSD: M1 `69444be954a869ebc831cd1253849222d8babc7a02940b2bb908a5179bcf5999`; tick `edccad88ed5b74caf16a14203f3cf743306c65f2ebc5004cf566ed61deeb6e17`

## 4. Cost Model

- Model A (PRIMARY): RT(A) = (s_entry + s_exit) / 2; Net_A = Gross - RT(A), where s is the per-minute observed MT5 spread in bp.
- Model B (DESCRIPTIVE): Net_B = Gross - (s_entry + s_exit); commission [0.0, 2.0, 5.0, 10.0] bp and slippage [0.0, 2.0, 5.0] bp bands are additive in the Model-B sensitivity table only.
- No assumed spread; no invented commission in Model A.
  - XAGUSD: observed-minute spread median 12.158 bp (p25 9.55231484429763, p75 13.18739285243201, p90 14.438000818153926); median Model-A cost 12.0791222032407 bp over 1729136 observed minutes.

## 5. Trade Population

- XAGUSD: traded 2176; exclusions {'EXCLUDED_HORIZON_INCOMPLETE': 18, 'HORIZON': 199, 'STRUCTURAL_INVALIDATION': 1977}.

## 6. Primary Economic Metrics (Model A, bp)

- **XAGUSD** — n=2176 (35.67/mo); median net -12.404; mean -9.064; win rate 9.1%; median win 30.104; median loss -13.107; PF 0.3560359392465996; cumulative -19723.0; max drawdown 20721.3; invalidation 90.9%; horizon exit 9.1%.

## 7. Development / OOS (chronological floor(N/2) event days)

- XAGUSD: 1271 event days, dev 635. Dev: n=1092, median -14.162, cumulative -11024.7, PF 0.2877058014481633. OOS: n=1084, median -10.355, cumulative -8698.3, PF 0.42584556772914467.

## 8. Yearly Results

- XAGUSD 2021: n=211, cumulative -1913.8, median -13.247, PF 0.31634358999396117.
- XAGUSD 2022: n=436, cumulative -4053.6, median -15.122, PF 0.3728939311179515.
- XAGUSD 2023: n=448, cumulative -5092.5, median -13.813, PF 0.18514771428226817.
- XAGUSD 2024: n=455, cumulative -4351.3, median -12.244, PF 0.22647897042469592.
- XAGUSD 2025: n=418, cumulative -4352.6, median -9.237, PF 0.39225996642967886.
- XAGUSD 2026: n=208, cumulative 40.8, median -8.098, PF 1.0175423206859036.

## 9. Market Classifications

- XAGUSD: **ECONOMICALLY NON-VIABLE**
  - Gates: {'gate1_median_net_gt_0': False, 'gate2_cumulative_net_gt_0': False, 'gate3_pf_gt_1': False, 'gate4_year_concentration_le_60pct': True, 'gate5_oos_independently_positive': False}
- EURUSD: NOT SIMULATED (NOT REGISTERED / DATA-LIMITED).

## 10. Resource Usage

- Peak process RSS: 117493760; peak CPU: 0.0%.
- Market durations (s): {'XAGUSD': 23.87014651298523}; total wall clock: 25.2 s.

## 11. Artifact Integrity

- EventStudyRecorder completion gate verified: journal COMPLETED; no missing/unexpected artifacts.
- Ledger retains all rows including EXCLUDED_* rows (no trade removed for being unfavourable).

## 12. Scientific Boundary

- No scientific object, protocol, execution artifact, or adjudication was modified.
- This report records the execution results only; it performs no adjudication and states no verdict on whether any strategy works, fails, or is profitable.

## 13. Exact Next Governance Task

> **INDEPENDENT ECONOMIC RESULTS ADJUDICATION** of this single controlled execution: determine whether the baseline economically survives, fails, or requires governance escalation.
