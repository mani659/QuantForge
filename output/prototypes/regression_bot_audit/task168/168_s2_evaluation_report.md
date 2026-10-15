# TASK168 — S2 Single-Evaluation Report (PROTO-S2-001)

**Protocol verdict: INCONCLUSIVE** (frozen spec §8: CI includes zero).
**Task verdict: `SINGLE_EVALUATION_COMPLETED_INCONCLUSIVE`.**
Executed exactly once, under `168_s2_evaluation_authorization.md`.

## 1. Primary result

| Item | Value |
|---|---|
| Endpoint | mean annual net return (frozen §8) |
| N (eligible windows) | **33** (1994–2026; matches predeclared ≈33) |
| Mean annual net | **+0.3381%** (0.00338054) |
| 95% bootstrap CI | **[−0.4308%, +1.0285%]** (B=10000, seed 20261015, i.i.d. annual events) |
| PASS rule (lower > 0) | not met |
| FAIL rule (upper < 0) | not met |
| **Verdict** | **INCONCLUSIVE** — interval includes zero |

Frozen decision consequence (spec §8 "minimum evidence to continue"):
only PASS continues the line. INCONCLUSIVE and FAIL both **end the line
with this record — no rescue, no variant** (stated as the frozen rule
requires; not a reinterpretation).

## 2. Sample and exclusion accounting

- 34 candidate January years in panel span; **1 fail-closed skip**
  (`no_december`: 1993 candidate needs Dec-1992, panel starts
  1993-01-29); `short_january`: **0**. 34 − 1 = **33 evaluated**.
- No imputation, substitution, or selective exclusion; skips counted and
  preserved in `168_s2_evaluation_results.json`.
- Chronology: first entry **1993-12-31**, last exit **2026-01-08**;
  windows are the first five January row-dates each year (holidays
  skipped by date order).

## 3. Diagnostics (from the single run)

- Yearly hit rate: **22 positive / 11 negative** of 33 (66.7%).
- Best years: 1999 +3.29%, 2003 +3.27%, 2006 +3.11%.
- Worst years: 2016 −6.14%, 2008 −5.28%, 2005 −2.30%.
- Strategy cumulative net across all windows: **+10.95%** (compounded,
  costs included; ~5 sessions/yr exposure).

## 4. Frozen-control comparison (DESCRIPTIVE only, per spec §4)

| Leg | Net |
|---|---|
| Strategy (33 windows, 30 bps RT each) | +10.95% cumulative |
| TOM_CONTROL buy-and-hold, identical span (1993-12-31 entry 26.1876 → 2026-01-08 exit 683.1400), same schedule once each | **+2508.6%** (net 25.0864, ≈26.1×) |

No paired test performed (S4 degeneracy avoided by frozen construction).
The comparison answers only "what the same span's buy-and-hold did";
it is not a strategy-ranking claim.

## 5. Data integrity and reproducibility

- Input SHA-256 verified pre-start: `483919f8…f4b71231` (MATCH);
  panel 8472 rows, 1993-01-29→2026-09-25, 0 NaN, no yearly >5%,
  timestamps monotonic unique.
- Implementation SHA `2892c8b5…` verified pre-start; synthetic preflight
  **12/12 PASS**; engine spec dictionary matches frozen params.
- Bootstrap regeneration cross-check: re-running the frozen RNG loop
  reproduced the engine's CI **exactly** (byte-identical assertion
  passed) before artifacts were written.
- Machine-readable evidence: `168_s2_event_results.csv` (33 events),
  `168_s2_bootstrap_replicates.csv` (10000 replicates),
  `168_s2_evaluation_results.json`, `168_s2_execution_log.txt`.

## 6. Limitations

- Preliminary historical evidence only — never proof of durable
  profitability, never permission to trade. Costs are a declared
  research assumption (10/5/0), not broker fact. Cash-settled
  assumption disclosed (no financing leg).
- The frozen panel appears **dividend-adjusted** (control ≈26× over the
  span vs price-only history): windows capture ex-dividend effects via
  adjusted closes. This was not distinguished by the frozen spec, which
  fixed this exact file — disclosed, not amended post-result.
- N=33 with per-event σ ≈2.7%: power is inherently limited for a
  ~30bps-cost seasonal; the wide CI is the honest state of evidence.
- A residual mean slightly positive but CI spanning zero is precisely
  what INCONCLUSIVE means under the frozen rule; no threshold was
  invented or moved after seeing results.

## 7. Non-effects confirmation

HOLD / Active Research NONE unchanged; no candidate registration, no
variants/tuning/reruns/rescue, no second evaluation, no holdout, no new
data, no deployment, no frozen-spec or prior-artifact edits, no commit,
no push. **S2 line ends here per frozen §8** unless the owner opens a
separate, newly justified effort in a future task.
