# TASK121 — Reproducibility and Limitation Audit (inspection only)

**Method:** read-only inspection of TASK120 artifacts. No rerun, no
recalculation of any outcome statistic, no inference. Decision logic was
checked against REPORTED values only (rule applied to stored numbers, never
recomputed from market data).

## 1. Artifact integrity (all hashes match the TASK120 manifest)

All 11 task120 files present with identical hashes (engine, self-test,
run config, runner, phase1_count, events.csv, summary.json, and all four
gate/result/decision/report docs). V9 triple, TASK119 package, handoff,
and role doc unmodified.

## 2. Structural consistency (read, not recomputed)

- events.csv: 158 rows; columns date/entry_open/exit_open/dir/gross/net2/
  net3; dates ascending 2023-09-01→2026-07-02; dir ∈ {−1.0, 1.0} only.
- summary.json: all required keys present (n, halves×2, both CI keys, both
  Holm keys, t4 denom/continued/flag, config, count_disposition, skips).
- Cross-file: summary n == events rows (158); phase1 count == n; skips
  identical across files; T4 denom == n.
- Logic application to reported values: both halves > 0 → t1_pass true;
  lower bounds < 0 with p ≥ 0.05 → t3_pass false; 84 > 158/2 → flag true.
  The preregistered rules were applied as written.
- Config-vs-code: SPEC dict (14, 3.0, 08:30/08:35/09:30, 1/day,
  America/New_York, 2.0/3.0, seed 20261013, B=10000, α=0.05) matches
  run_config.md and the frozen preregistration exactly.

## 3. Lineage defects (unresolved; inherent, all previously disclosed)

1. Verification-subset subclause unexecutable — no G1 event list exists on
   any record (disclosed in TASK120 docs; unresolvable within authority).
2. N=158 vs frozen N=157: one-event delta, extra event unidentifiable
   (follows from defect 1); handled per predeclared contingency.
3. tz mapping (naive-as-UTC) and ATR micro-conventions (Wilder, window
   edges) are principled readings, not G1-documented facts; protected by
   the single-attempt count gate, residual uncertainty disclosed.
4. Filename-vs-G1-input identity rests on name + SHA-reference + span
   match, not byte-proof of G1's input (stated in preregistration §2).

## 4. Verdict

**No unresolved reporting defects.** Every required artifact, field,
cross-check, and disclosure is present and consistent. Lineage caveats
1–4 are inherent to the records, fully disclosed, and unresolvable without
evidence that does not exist (G1 event list) or authority not granted
(re-execution variants). No recalculation was performed to reach this
verdict.
