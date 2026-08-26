# QUANTFORGE — ORD OPENING-RANGE DIRECTIONAL BREAK
# SCIENTIFIC EXECUTION REPORT V1

## 1. Execution Identity

- **Execution ID:** `EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532`
- **Execution timestamp (start UTC):** `2026-08-18T14:12:02.127591+00:00`
- **Execution timestamp (end UTC):** `2026-08-18T14:13:11.100284+00:00`
- **Execution duration:** 70.0 s
- **Git HEAD:** `a6c62edf9666f59eb8a044da2d0497f9a366e0a0` (`git_dirty_state: True`)
- **Protocol version:** ORD V1.1.0
- **Protocol SHA-256:** `85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06`
- **Definition lock (dataset governfile) identity:** `b58105404d277560eec31a8b08c5b1997b86a03904fc4a804e87beaac448ab30`
- **Implementation (entry script) SHA-256:** `ab145252afa8645213b02a6ba4e22d3a185bf37adff3294f34b47e1f75e3baac`
- **Entry script path:** `scripts\run_ord_v1.py`
- **Seed:** `20260818`
- **B (bootstrap replicates):** `10000`
- **L (integer time-lag):** `10`
- **Software environment:** Python `3.11.9`; numpy `2.4.4`; pandas `3.0.2`; platform `Windows-10-10.0.19045-SP0`
- **Final execution state:** `COMPLETED` (journal state `COMPLETED` at `2026-08-18T14:13:11.135827+00:00`; manifest `final_state=COMPLETED`)

---

## 2. Dataset Integrity

Persisted input fingerprints (from `implementation_manifest.json` → `input_manifest_hash`):

| Dataset | Persisted SHA-256 |
| --- | --- |
| XAUUSD_M1.csv | `54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c` |
| XAGUSD_M1.csv | `69444be954a869ebc831cd1253849222d8babc7a02940b2bb908a5179bcf5999` |
| USATECHIDXUSD_M1.csv | `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6` |
| BTCUSD_M1.csv | `97b853854d8f650d80e3972f159deab0b15911e19dd437e1dd10b3bab098409b` |

**EURUSD:** NOT registered in the persisted input fingerprints of this execution. The completed execution registered and evaluated the four markets listed above; no EURUSD fingerprint is present in `implementation_manifest.json`. Consistent with that persisted disposition, EURUSD is reported as `NOT REGISTERED / NOT EVALUATED` in this execution. No absent hash is invented.

---

## 3. Execution Architecture

- **Execution style:** sequential, per-market processing (market order `XAUUSD → XAGUSD → BTCUSD → USATECHIDXUSD`).
- **Execution infrastructure identity:** execution recorder `process_identity.json` recorded PID `7700`, `platform=Windows-10-10.0.19045-SP0`, `process_start_time=1787062320.3344803`, `boot_time=1784457878.6748967`.
- **Crash-safe recorder:** heartbeat mechanism present — `execution_heartbeat.json` (5 s interval) persisted; latest recorded heartbeat `utc=2026-08-18T14:13:09.118`, `rss_bytes=245616640`.
- **Execution directory:** the directory containing this report, identified by the execution ID above.
- **Finalization state:** `COMPLETED` — manifest `final_state=COMPLETED`, `expected_artifacts=9`, `infra_artifacts=5`, `observed_artifacts=13`, `missing_artifacts=[]`, `unexpected_artifacts=[]`.
- Per-market duration, peak RSS, and peak CPU are NOT captured in the persisted artifacts and are not claimed here.

---

## 4. Data Quality / Market Disposition

Per persisted market disposition and statistics (exact persisted values):

| Market | Disposition | Event count | Treatment count | Control count | Data-quality disposition |
| --- | --- | --- | --- | --- | --- |
| XAUUSD | EVALUATED — SUPPORT | (finite eligible series) | 2184 | 62 | Evaluated; missing-value/eligibility fraction per secondary record `0.003105590062111801` |
| XAGUSD | EVALUATED — SUPPORT | (finite eligible series) | 2177 | 56 | Evaluated; missing-value/eligibility fraction per secondary record `0.00858034321372855` |
| USATECHIDXUSD | EVALUATED — SUPPORT | (finite eligible series) | 839 | 25 | Evaluated; missing-value/eligibility fraction per secondary record `0.03824362606232295` |
| BTCUSD | HALTED | (halted — not scientifically evaluated) | — | — | Halted: expected deprecation-rate / invalid-fraction `0.11945205479452055` exceeds the halt threshold (halt fraction `0.1`) |

**BTCUSD:** halted. It therefore has no scientific bootstrap arrays and no scientific null arrays. This is stated exactly as the persisted artifacts establish.

---

## 5. Primary Results

Persisted values exactly as recorded in `statistics.json`. **No raw market-unit magnitude across different markets is compared as economically equivalent.**

| Market | Treatment events | Control events | Observed DeltaM | 95% CI | Raw p-value | Holm-adjusted p-value | Final classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| XAUUSD | 2184 | 62 | +30.901704157243934 | [23.216857953960513, 36.5353289810984] | 0.00009999 | 0.00029997000299970003 | SUPPORT |
| XAGUSD | 2177 | 56 | +71.0428969879628 | [57.840627740888365, 86.95092296030565] | 0.00009999 | 0.00029997000299970003 | SUPPORT |
| USATECHIDXUSD | 839 | 25 | +49.51962303222475 | [33.459428586263954, 79.01079869236179] | 0.0004999500049995 | 0.0004999500049995 | SUPPORT |

- BTCUSD: HALTED — no bootstrap/null arrays, no primary results (see Section 4).
- Observed median treatment response values persisted: XAUUSD `-0.12843904309117762`, XAGUSD `-1.752080595707988`, USATECHIDXUSD `1.241798761359251`.
- Observed median control response values persisted: XAUUSD `-31.03014320033511`, XAGUSD `-72.7949775836708`, USATECHIDXUSD `-48.2778242708655`.

---

## 6. Bootstrap / Null Verification

Per persisted metadata and statistics (`B=10000`, `L=10`):

- **B:** `10000`
- **B_valid:** `10000` for XAUUSD, `10000` for XAGUSD, `10000` for USATECHIDXUSD (all bootstrap/null draws finite and valid for the evaluated markets).
- **Bootstrap array existence and size:** persisted; length `10000` for each evaluated market (XAUUSD, XAGUSD, USATECHIDXUSD). Not present for BTCUSD (halted).
- **Null array existence and size:** persisted; length `10000` for each evaluated market (XAUUSD, XAGUSD, USATECHIDXUSD). Not present for BTCUSD (halted).
- **Null construction:** per the frozen protocol (fixed-seed `20260818`, time-lag `L=10`, market-dependent GRS cross-sectional naïve null draws). No draws were regenerated for this report.
- **p-value construction:** from persisted null arrays — XAUUSD null exceedance count `0` → p `9.999e-05`; XAGUSD null exceedance count `0` → p `9.999e-05`; USATECHIDXUSD null exceedance count `4` → p `4.999500049995e-04` (as `p_raw`). Holm adjustment across evaluated markets applied as persisted (`p_holm`).
- **CI source:** 2.5/97.5 percentile bootstrap interval from the persisted bootstrap arrays, matching the persisted `ci_95` intervals in Section 5.

---

## 7. Chronological Stability

Only the already-persisted chronological-half and per-year descriptives are reported. No additional robustness tests were created.

| Market | First-half DeltaM | Second-half DeltaM | Persisted per-year DeltaM |
| --- | --- | --- | --- |
| XAUUSD | 33.70118241915733 | 28.05587749143095 | 2021: 33.992275491456624; 2022: 33.63085115536209; 2023: 19.123836317387482; 2024: 26.471721231118988; 2025: 31.059348783752746; 2026: 34.62529586573193 |
| XAGUSD | 67.32300568694681 | 73.98683077059532 | 2021: 72.75192046995092; 2022: 80.40573973280566; 2023: 48.6673139063394; 2024: 69.09143711946221; 2025: 85.98566107392331; 2026: 82.35202801102447 |
| USATECHIDXUSD | 36.80343550963096 | 75.80348755451857 | 2023: 39.62704617437381; 2024: 33.83569451961994; 2025: 77.24381532408123; 2026: 75.94426923199197 |

---

## 8. Secondary Descriptives

Only the secondary metrics already present in the completed execution artifacts are reported.

| Market | Missing/eligibility fraction | Mean favorable excursion (MFE) | Range-normalized return | Long treatment | Short treatment | Long control | Short control |
| --- | --- | --- | --- | --- | --- | --- | --- |
| XAUUSD | 0.8891941391941391 | 15.468463779156512 | -0.02236200252991575 | 1092 | 1092 | 28 | 34 |
| XAGUSD | 0.9085898024804777 | 30.66741990154165 | -11.106684891503035 | 1093 | 1084 | 28 | 28 |
| USATECHIDXUSD | 0.8927294398092968 | 26.231313225359507 | 0.016467553414418884 | 437 | 402 | 11 | 14 |

No secondary metrics absent from the completed execution artifacts are invented.

---

## 9. Cross-Market Interpretation

This execution, evaluated through the frozen ORD V1.1.0 protocol on gold (XAUUSD), silver (XAGUSD), and the US technology index (USATECHIDXUSD), produced statistically supported positive observed DeltaM treatment-vs-control directional responses. The fourth registered market, BTCUSD, was halted on data-quality grounds (persisted invalid-fraction `0.11945205479452055` exceeding the `0.1` halt threshold). The section stays descriptive, at the scientific level of the persisted statistics.

This section does **not** claim: profitability, economic viability, a universal market law, institutional intent, or live-trading readiness.

---

## 10. Scientific Boundary

This report explicitly records:

- this is a **behavioral research result** at the statistical/indicator level;
- economic translation (e.g., costs, spreads, slippage, PnL-equivalent study) is a **separate, later stage**;
- **no PnL / spread / slippage conclusion is established by this execution**;
- evidence-limited/halting decisions (BTCUSD HALTED) remain exactly as recorded.

---

## 11. Resource Usage

**Not captured in the completed execution artifacts.**

The completeness audit (`ORD_EXECUTION_REPORT_COMPLETENESS_AUDIT_V1.md`) established that per-market duration, peak RSS, and peak CPU were not persisted. These values are not estimated, not inferred from logs, and not invented.

---

## 12. Artifact / Reproducibility Status

- All 14 other required artifacts are present and valid inside the execution directory.
- `SCIENTIFIC_REPORT_V1.md` is the reconstructed presentation artifact described by this document, reconstructed from persisted artifacts only.
- Hashes and manifests are consistent (journal state `COMPLETED`; manifest `missing_artifacts=[]`, `unexpected_artifacts=[]`; on-disk hashes match the manifest `artifact_hashes`).
- No scientific artifact was regenerated.
- BTCUSD missing arrays are consistent with its halted status.
- This report reconstruction does **not** constitute a rerun.

---

## 13. Exact Next Governance Task

The next task after report reconstruction is:

**INDEPENDENT SCIENTIFIC RESULTS ADJUDICATION OF ORD V1.1.0.**

The sequence remains:

execution → scientific adjudication → if supported, economic translation → cost-aware validation → demo/forward validation → months of monitoring → live consideration.

No jump directly to economic translation is authorized by this report.