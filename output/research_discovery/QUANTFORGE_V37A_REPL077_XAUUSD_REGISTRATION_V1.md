# QUANTFORGE — V37A REPLICATION REGISTRATION & EXPERIMENT FREEZE

# REGISTRATION ID: V37A-REPL-077-XAUUSD-M1
# DATE: 2026-09-03
# STATUS: REGISTERED / FROZEN / NOT EXECUTED
# EXPERIMENT NAME: CAND-077 Volatility Compression-to-Expansion — XAUUSD M1 Replication
# PARENT RESEARCH MILESTONE: V37A Controlled Expansion (post V37B pre-execution conformance audit)
# REPLICATION TARGET: CAND-077 (USATECHIDXUSD M1)
# OWNER AUTHORIZATION STATUS: PENDING

---

## 1. Registration Identity

| Field | Value |
|---|---|
| Registration ID | V37A-REPL-077-XAUUSD-M1 |
| Experiment name | CAND-077 volatility compression→expansion replication on XAUUSD M1 |
| Parent milestone | V37A Controlled Expansion — Stage 1 |
| Replication target | CAND-077 (original object) |
| Study class | REPLICATION (NOT a new hypothesis, NOT candidate generation) |
| Status | REGISTERED / FROZEN / NOT EXECUTED |
| Registration artifact | `output/research_discovery/QUANTFORGE_V37A_REPL077_XAUUSD_REGISTRATION_V1.md` |

---

## 2. Formal Research Question (FROZEN)

> Does the CAND-077 volatility compression→expansion condition reproduce on XAUUSD M1 under the exact operational definition used for the original CAND-077 execution, with the instrument as the only experimental change?

The experiment tests **generalization / replication**, not profitability optimization. This question is frozen and may not be weakened or strengthened after execution.

---

## 3. Replication Classification (FROZEN)

| Field | Value |
|---|---|
| Study class | REPLICATION |
| Original object | CAND-077 |
| Original instrument | USATECHIDXUSD (M1) |
| Replication instrument | XAUUSD (M1) |
| Experimental change | INSTRUMENT ONLY |

This experiment is **not a new hypothesis** and must not be interpreted as one. No new candidate ID, no new State ID, no hypothesis inversion, no threshold creation.

---

## 4. Implementation Provenance Freeze (FROZEN DECISION)

Basis (FACT, from V37B conformance audit):

1. The narrative V26 document (`output/research_discovery/RESEARCH_FACTORY_V2_G1_SCREEN_20260830_V26.md`, §6) is under-specified: it omits ATR period, percentile lookback, compression-duration numeric rule, transition tolerance, CF sustained-duration detail, dedup/rearm behavior, and numeric cost-application detail.
2. `research/v26_g1_screen.py` (`run_077` and helpers) contains the complete operational CAND-077 implementation.
3. The implementation file is currently **untracked** in git (`git ls-files` negative; `git log` for the path is empty).
4. No independent second implementation copy exists (`research/v26_cand079_only.py` contains no shared helpers; `output/research_discovery/v26_g1_results.json` was never saved).
5. The published V26 aggregate results are arithmetically consistent only under this implementation's conventions (verified in V37B: gross mean +1.15 − 2.0 = net −0.85; gross median +0.86 − 2.0 = net −1.14; delta mean +1.67 = −0.85 − (−2.52); delta median +0.76 = −1.14 − (−1.90)).

FROZEN DETERMINATION:

> **The V37A replication operational definition is the exact CAND-077 implementation contained in `research/v26_g1_screen.py` as inspected during V37B and hashed in this registration.**

This does not claim the implementation is the only historical interpretation. It states:

> The historical narrative is insufficient to independently reconstruct every constant; therefore replication fidelity is defined against the complete operational implementation associated with the published V26 evidence.

---

## 5. Historical Implementation Hash (FACT)

| Field | Value |
|---|---|
| Path | `research/v26_g1_screen.py` |
| Byte size | 12,310 |
| SHA-256 | `b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b` |
| Git tracking status | UNTRACKED (not in any commit) |
| Repository HEAD at registration | `bbb1c267550e7a1b983abcbc74dab5dd9696a3ec` |

Freeze mechanism: the SHA-256 above is the content pin. Any execution must re-verify this hash against the same path immediately before Phase A; a mismatch = STOP (implementation drift). No archival byte-copy is created by this registration (no explicit repository policy requires one); if governance directs an immutable archival copy at execution authorization, it must be byte-identical to the hashed file, given a new path only, and its SHA-256 recorded.

---

## 6. Complete Frozen Specification (FROZEN)

| Field | Frozen value | Source / verification |
|---|---|---|
| Target | CAND-077 | V26 artifacts; V37A/B |
| Original market | USATECHIDXUSD | verified |
| Replication market | XAUUSD | verified |
| Timeframe | M1 | verified |
| Primary window (entries) | 2023-09-01 → 2026-04-10 | V37A/B; XAUUSD last bar 2026-04-10 20:59 |
| ATR period | 14 | implementation (`compute_atr`) |
| ATR method | TR = max(high−low, \|high−close_prev\|, \|low−close_prev\|); ATR = rolling mean(14, min_periods=1) | implementation |
| ATR percentile lookback | 200 trailing bars (inclusive of current bar) | implementation (`atr_pct`) |
| Percentile ranking method | strict rank: (count of valid ATR < ATR[i]) / count × 100; NaN if <10 valid | implementation |
| Compression threshold | percentile < 25 | implementation + doc |
| Compression duration logic | ≥10 of prior 20 bars (window `[i−20, i)`, current excluded) have percentile <25; comp_high[i] = max close over those compressed bars; else NaN | implementation |
| Transition tolerance | min percentile over bars `[i−5, i]` (inclusive) < 25 at bar i | implementation |
| Expansion threshold | percentile > 50 (strict) at bar i | implementation |
| Breakout rule | close[i] > comp_high[i] (NaN → no event) | implementation |
| Entry timing | close of breakout bar i (entry price = close[i]) | implementation + doc |
| Direction | LONG-ONLY (upward breakouts; no short mirror) | implementation + doc |
| Counterfactual | at bar i: percentile[i] > 50; min percentile over `[i−30, i]` (31 bars) > 50 (strict, no NaN); close[i] > max(close over `[i−20, i−1]`) | implementation + doc |
| CF matching rule | for each treatment i: take the LOWEST-index CF within ±50 bars (exclusive of i); CF sample may contain repeated CF bars; treatments without a nearby CF remain in treatment stats only | implementation |
| Event loop bounds | i ∈ [250, n−30); loop bound n−30 supplies the 30-bar outcome margin | implementation |
| Outcome horizon | 30 M1 bars (bar-index based) | implementation + doc |
| Exit basis | close[i+30] | implementation |
| Friction | 2.0 bps round-trip, applied ONCE as a constant shift at aggregation (net mean = gross mean − 2.0; net median = gross median − 2.0), identical for treatment and control | implementation (`FRIC`, `v3_evidence`) |
| Primary metric | treatment net mean − control net mean (conditional mean delta) | V37A/B; Class-C doctrine |
| Gross metric | required secondary (gross mean, gross median both arms) | implementation |
| Median | required secondary (median delta) | implementation |
| Win rate | required secondary (WR delta) | implementation |
| Distribution diagnostics | pre-specified only: std, worst event, best event, exclude-best mean | implementation |
| Secondary full-window check | 2021-04-12 → 2026-04-10 (entries), consistency evidence only | V37A/B |
| Tick data | PROHIBITED (replication is M1-only) | V37B |
| Volume | UNUSED (zero-filled in source; no reference in implementation) | verified |

---

## 7. Temporal / Warm-Up Freeze (FROZEN)

- Primary outcome window: entries with date ∈ [2023-09-01, 2026-04-10].
- Warm-up: the **full XAUUSD file must be loaded before any event filtering** so historical state calculations (ATR percentile 200-bar lookback; 250-bar event-loop start; 30-bar outcome margin) behave identically to the original implementation.
- FROZEN RULE: the event date filter occurs **after** signal-state computation; it must **not** be implemented by truncating the source data before computing indicator state.
- Full-history consistency check: entries 2021-04-12 → 2026-04-10 — **secondary consistency evidence only**. It may not replace the primary result because it appears more favorable. No additional windows may be introduced after seeing results.

---

## 8. Treatment / Control Definition (FROZEN — full operational detail)

**Treatment** = CAND-077 treatment condition as implemented in V26 (`run_077`), i.e. bars i ∈ [250, n−30) where ALL of: (a) atr_pct[i] > 50 (strict); (b) min(atr_pct[i−5..i]) < 25 (transition within the last ≤5 bars); (c) close[i] > comp_high[i], where comp_high[i] = max close of bars in the prior 20 with atr_pct < 25 and at least 10 such bars exist (else no event).

**Control** = CAND-077 counterfactual condition as implemented in V26, i.e. bars i ∈ [250, n−30) where ALL of: (a) atr_pct[i] > 50 (strict); (b) min(atr_pct[i−30..i]) > 50 (strict; none NaN) — sustained expansion ≥31 bars; (c) close[i] > max(close[i−20..i−1]) — new 20-bar high close.

**Matching** (frozen, verbatim): per treatment, the lowest-index control bar within [i−50, i+50], excluding i; control returns recorded for matched pairs only; treatment statistics use all treatment bars.

FROZEN: no threshold relaxation; no alternate or replacement control; no post-hoc matching changes; no favorable-event exclusion; no deduplication or rearm introduced (the original had none).

---

## 9. Outcome and Metric Freeze (FROZEN)

- entry = close[i]; exit = close[i+30].
- gross_return_bps = ((close[i+30] − close[i]) / close[i]) × 10,000.
- net = gross − 2.0 bps (constant shift at aggregation, per the frozen implementation; NOT a per-trade split).
- The experiment is **bar-index based (30-bar forward outcome)** — NOT elapsed-calendar-time. This matches the original implementation's timing convention including across scheduled market closures.

**Primary metric:** conditional mean delta = mean(net treatment) − mean(net control).
**Secondary metrics (closed list, no additions after results):** treatment N; control N (matched); treatment/control gross mean; treatment/control net mean; treatment/control median (gross and net); mean delta; median delta; win-rate delta; standard deviation; worst event; best event; exclude-best mean. Frequency (events/year) as reported by the frozen implementation. No metric may be added after seeing the result.

---

## 10. No Numeric Replication Gate (FROZEN)

There is **NO hard numeric replication threshold**. Explicitly prohibited as gates: "delta must exceed 0.7 bps", "delta must reproduce 1.67 bps", "win rate must exceed X%", "t-stat must exceed X". The historical CAND-077 result (+1.67 bps) is contextual evidence, not a pass/fail threshold. The ~0.7 bps historical null band may be mentioned only as contextual background. Final adjudication occurs after execution under the G1 V3 holistic doctrine.

---

## 11. Expected Direction / Headroom (FROZEN)

- Expected direction: positive conditional delta.
- Expected hypothesis: transition-state treatment > already-expanded control.
- Economic headroom (ex-ante): the observed conditional information must be sufficiently large, stable, and credible to warrant further economic investigation; no universal numeric threshold is imposed.
- This is an ex-ante expectation. It must never be rewritten after execution.

---

## 12. Falsification Logic (FROZEN — qualitative)

| Outcome | Interpretation |
|---|---|
| Replication-supported | Positive conditional information with adequate data integrity and evidence coherent across the primary/secondary diagnostics |
| Non-replication | No positive conditional separation under a valid frozen replication |
| Inconclusive | Evidence insufficient to adjudicate due to data-quality, population, or statistical limitations |
| Data-infeasible | Frozen treatment/control definitions cannot be evaluated correctly on XAUUSD |

These are not numeric gates. No translation into arbitrary thresholds.

---

## 13. Phase A / Phase B Execution Boundary (FROZEN)

**Phase A (permitted):** load XAUUSD M1 (full file); verify frozen schema; apply +4h UTC shift; calculate signal state (ATR, percentile, comp_high, treatment flags, control flags); identify treatment events; identify control events; report counts; verify data integrity (monotonic timestamps, no duplicates, OHLC validity, window coverage). Phase A must NOT calculate or reveal forward returns, gross outcomes, net outcomes, or any treatment/control economics.

**Governance checkpoint (between phases):** review data integrity, population existence, event construction, counterfactual existence, and adherence to the frozen implementation. No parameter modification is permitted at this checkpoint.

**Phase B (only after Phase-A authorization):** calculate frozen 30-bar outcomes; compute gross; apply frozen 2.0 bps; compute net; produce the frozen metric set.

---

## 14. Result Blinding and Rerun Protection (FROZEN)

- Phase-A population information may be used ONLY to establish data feasibility. It may NOT be used to modify the experiment. Explicitly forbidden: reducing thresholds; changing compression duration; changing transition tolerance; choosing another date range; changing control definition; dropping sparse regimes; selecting a preferred market window.
- If Phase A is unexpectedly sparse, classify the experiment under the frozen feasibility rules (INCONCLUSIVE / DATA-INFEASIBLE). Do not rescue it.
- A rerun is prohibited unless a method-independent implementation defect is proven. Permitted rerun circumstances: (1) code/data-ingestion defect demonstrably present before outcome inspection; (2) defect documented; (3) correction independently justified; (4) corrected specification versioned; (5) rerun authorized by governance. NOT permitted: weak results; unexpected direction; low effect; "almost significant"; desire for more trades; desire to test another threshold; desire to inspect a more favorable period.

---

## 15. Multiple-Testing Protection (FROZEN)

This is a replication: no alternative thresholds, horizons, controls, date windows, cost models, or market substitutions. A later replication on another instrument must be a separately registered study and must not be appended to this registration.

---

## 16. State-Governance Protection (FROZEN)

This registration does not qualify CAND-077 as State. It does not: create an Alpha; qualify the State; authorize relational research; modify SEED-002; revive closed candidates; promote a State Review Eligible object. If the replication succeeds, its result becomes evidence that may later support a separate State-qualification decision requiring its own governance.

---

## 17. Re-Execution Policy (FROZEN)

See §14. A second run requires a proven, documented, independently-justified implementation defect, a versioned corrected specification, and governance authorization. Weak or surprising results grant no rerun.

---

## 18. Owner Authorization Block

```
OWNER AUTHORIZATION STATUS:
PENDING
```

Execution of Phase A is NOT authorized by this registration. The separate task "V37A CONTROLLED REPLICATION EXECUTION — PHASE A ONLY" may begin only after the owner explicitly authorizes execution. This registration prepares the frozen specification; it does not self-authorize.

---

## 19. Repository / Handoff Status

- `docs/SESSION_HANDOFF.md`: inspected; **intentionally unchanged** — no existing governance rule was found that requires registration-only milestones to be recorded there, and execution has not occurred. If such a rule exists, it should be reported as a conflict; none was identified in this audit.
- Research discovery database, candidate ledger, G1 framework, State governance: **unchanged**.
- No candidate ID, State ID, threshold, or parameter created or modified.
- No experiment, backtest, or outcome calculation performed.

---

*Registration complete. Frozen specification v1.0. NOT EXECUTED. Owner authorization PENDING.*
