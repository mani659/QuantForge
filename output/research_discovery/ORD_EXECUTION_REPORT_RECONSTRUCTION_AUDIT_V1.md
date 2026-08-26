# QUANTFORGE — ORD V1.1.0
# COMPLETED EXECUTION REPORT RECONSTRUCTION AUDIT V1

## 1. Reconstruction Scope

Reconstructed the single missing presentation artifact of the already-completed
execution:

`output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/SCIENTIFIC_REPORT_V1.md`

This was a report-reconstruction task only. No rerun, no data reprocessing, no
event regeneration, no bootstrap/null regeneration, and no scientific-value
changes occurred.

## 2. Source Artifacts Used

Only persisted artifacts inside the completed execution directory were used,
together with the frozen ORD V1.1.0 protocol (section terminology only) and the
prior completeness audit:

- `execution_journal.json` — state/timestamps
- `execution_manifest.json` — final state, market status, artifact inventory
- `implementation_manifest.json` — protocol/definition identities, Git HEAD,
  Python/package versions, entry-script SHA-256, input fingerprints
- `metadata.json` — seed, B, L, alpha, halt parameters, market order, halts,
  environment, timestamps, duration
- `statistics.json` — all scientific primary/secondary values
- event table — eligibility/count inventory (persisted finite eligible series)
- persisted bootstrap arrays and null arrays — existence and size (length 10000;
  B_valid 10000) per evaluated market
- artifact manifest/inventory — presence/absence and on-disk hashes
- `process_identity.json` / `execution_heartbeat.json` — infrastructure identity
- `ORD_EXECUTION_REPORT_COMPLETENESS_AUDIT_V1.md` — classification of each
  report section and the not-persisted resource telemetry finding

## 3. Values Reconstructed

Every reported scientific value was transcribed from the persisted artifacts,
section by section:

- **Identity:** execution ID, start/end UTC, duration 70.0 s, Git HEAD
  `a6c62edf…`, protocol V1.1.0 SHA `85263b84…`, definition lock `b5810540…`,
  entry-script SHA `ab145252…`, seed `20260818`, B `10000`, L `10`, Python
  `3.11.9`, numpy `2.4.4`, pandas `3.0.2`, state COMPLETED.
- **Dataset fingerprints:** the four persisted `input_manifest_hash` values;
  EURUSD reported as NOT REGISTERED / NOT EVALUATED (absent from the execution's
  persisted input fingerprints).
- **Disposition:** XAUUSD/XAGUSD/USATECHIDXUSD EVALUATED — SUPPORT; BTCUSD
  HALTED (invalid-fraction `0.11945205479452055` > halt fraction `0.1`), no
  scientific arrays.
- **Primary results:** treatment/control counts, DeltaM, 95% CI, raw p, Holm p,
  classification exactly as persisted (e.g., XAUUSD +30.901704157243934,
  Holm 0.00029997000299970003; XAGUSD +71.0428969879628,
  Holm 0.00029997000299970003; USATECHIDXUSD +49.51962303222475,
  Holm 0.0004999500049995).
- **Bootstrap/null verification:** B=10000, B_valid=10000, arrays length 10000
  per evaluated market; null/p/CI construction described from protocol + persisted
  values; no draws regenerated.
- **Chronological and secondary descriptives:** half-year and per-year DeltaM and
  all secondary metrics transcribed exactly; no missing secondaries invented.

## 4. Missing Information

- Per-market duration, peak RSS, and peak CPU — **not captured in the completed
  execution artifacts**. Reported verbatim as such (report Section 11); not
  estimated, not inferred from logs, not invented.
- EURUSD — not registered in this execution's persisted fingerprints; reported
  as NOT REGISTERED / NOT EVALUATED rather than assigning any hash or result.

## 5. Verification

- The report exists at the path above (created by this reconstruction).
- All numerical values in the report correspond to persisted artifacts
  (spot-checked against `statistics.json`, `metadata.json`, and both manifests;
  no value derived from the original M1 datasets).
- No new statistical calculation was introduced (reconstruction transcribes
  persisted values; the only arithmetic in the reconstruction process was
  deterministic verification already documented in the prior completeness
  audit, and none altered any persisted value).
- No source dataset was reprocessed or loaded.
- No scientific artifact was changed — all 13 observed artifacts and their
  hashes are untouched; `SCIENTIFIC_REPORT_V1.md` was added only.
- Report hash (computed for traceability; the manifest system does not support
  post-hoc artifact-hash registration and the finalized manifest was not
  modified):
  `SCIENTIFIC_REPORT_V1.md` — hash `9BBC7C58799CBE96C46BC60189FA27FAEF97AE90F8B941964F27E550F986CF9B`.
- Execution journal remains `COMPLETED`; it was **not** modified because the
  report was reconstructed.

## 6. Scientific Integrity

- The reconstruction preserves the completed execution's scientific evidence
  verbatim; it introduces no new claims, interpretations, parameters, or
  market classifications.
- The BTCUSD halt and its absent arrays are presented exactly as persisted.
- Missing resource telemetry is declared, not filled from general knowledge.
- This reconstruction does not constitute a rerun and confers no new scientific
  standing; the execution's existing governance artifacts remain authoritative.

## 7. Final Status

**REPORT RECONSTRUCTED FROM PERSISTED ARTIFACTS — NO RERUN**
