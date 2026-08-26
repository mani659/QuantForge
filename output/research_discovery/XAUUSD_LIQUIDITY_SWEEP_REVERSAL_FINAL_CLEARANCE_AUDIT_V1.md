# QUANTFORGE — CROSS-MARKET LIQUIDITY SWEEP / REVERSAL
# FINAL INDEPENDENT EXECUTION CLEARANCE AUDIT V1

- **Audit object:** `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL_EVENT_STUDY_PROTOCOL_V1.md`
- **Protocol version audited:** v1.1.0
- **Audit type:** FINAL, adversarial, READ-ONLY pre-registration clearance audit
- **Audit date:** 2026-08-17
- **Control set read:** protocol v1.1.0; definition screening V1; prior independent protocol audit V1 (CONDITIONAL PASS, three blockers); `docs/SESSION_HANDOFF.md`; `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-021/022/024 closed lines); `research/knowledge/RESEARCH_TIMELINE.md`; `data/m1/` inventory (all five M1 files, schema `timestamp,open,high,low,close,volume`, UTC-labeled).
- **Data inventory (source-level only, no scientific statistic computed):**

  | File | Rows | Coverage (UTC) |
  |---|---|---|
  | XAUUSD_M1.csv | 1,768,123 | 2021-04-12 11:00 → 2026-04-10 20:59 |
  | XAGUSD_M1.csv | 1,729,136 | 2021-07-13 00:00 → 2026-07-12 23:59 |
  | EURUSD_M1.csv | 2,041,613 | 2021-01-04 00:00 → 2026-06-30 23:59 |
  | BTCUSD_M1.csv | 2,539,807 | 2021-05-23 00:00 → 2026-05-22 23:59 |
  | USATECHIDXUSD_M1.csv | 906,815 | 2023-09-01 00:00 → 2026-07-10 20:14 |

---

## 1. Executive Verdict

**CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED.**

The three prior blocking defects (F1 control-event timestamp mechanics, F2 event/day bootstrap mapping, F3 null-inference construction) are **resolved in v1.1.0 and verified below**. The null-inference construction is **mathematically justified** (a genuine null-imposing recentered bootstrap for a difference of medians, proven by location equivariance — §7 below). The scientific object, sessions, sweep/rejection/confirmation geometry, MFE anchoring, day-cluster bootstrap mapping, Holm family, and all firewalls are sound and outcome-blind.

However, under the governing audit standard — *"a detail is acceptable only if it is explicitly stated, OR follows mathematically and uniquely from the stated rule; if two reasonable implementations could differ materially, flag it"* — **five precision items remain non-unique in the current text** and would force an executor to make an unregistered decision:

1. Exact stationary-bootstrap mechanics (continuation probability, block-start selection, circular wrapping, replicate length N, final truncation) — §13/§15.
2. MFE horizon behavior when the 120-minute window crosses the 17:00 ET trading-day boundary, and handling of incomplete horizons near data end — §10/§11.
3. The identity of "the sweep candle" when multiple sweep+reject candles precede confirmation — §8/§9.
4. Data-gate definitions: the invalid-day denominator, "required session bars," duplicate/missing-bar handling, and when the gate is assessed — §17.
5. The registered mapping from (Holm-adjusted p, sign of ΔM_obs) to the three required labels Support/Contradicted/Inconclusive, and the even-n median convention — §14/§16/§18/§12.

Each has a deterministic, uniquely resolvable wording fix (the same class of correction as the previous v1.1.0 round). **No execution is authorized from this verdict.** A v1.2.0 precision amendment plus a final re-audit is required before multi-market execution may be authorized.

---

## 2. Protocol Integrity

- **Version/history:** v1.1.0 is current; v1.0.0 history preserved; §0 documents exactly the three v1.1.0 corrections (control absence window + MFE anchor; day-cluster flattening mapping; null-imposing p-value). PASS.
- **No scientific object changed by v1.1.0:** hypothesis, universe, sessions, sweep/rejection/confirmation, MFE, ΔM, B/L/seed, Holm family all unchanged. PASS.
- **No outcome-derived parameter:** sessions, 120-min horizon, B=10,000, L=10, seed=20260817, α=0.05, N≥100 are all structural. No effect value, p-value, event count, or favorable date appears anywhere in the protocol. PASS.
- **Prior audit's §18 claim:** the prior audit stated the protocol "defines distinct tiers of success (Instrument-specific vs Cross-market support)." v1.1.0 §2 frames the three tiers at scope level but §14 registers only per-market verdict labels — no explicit outcome→claim-tier mapping table exists. Report-stage note (see §9); not an execution blocker.

## 3. Scientific Object

**PASS.** Primary question (v1.1.0 §1): does a deterministic sweep of a prior Asian-session extreme, followed by rejection and micro-structural reversal confirmation, produce a statistically larger subsequent directional price excursion than the pre-registered control group? Behavioral volatility/excursion hypothesis; MFE only; no PnL/expectancy/spread/slippage/entry/stop/target/sizing (§19, §21); distinct from Mean Reversion (DISC-021), TSMOM (DISC-022), H01, and Session-Anchored Range Expansion (DISC-024) per screening §3 — not a renamed closed line. Later path (behavior → economic → strategy translation → demo → forward monitoring → live) is preserved and deferred (§19–§21).

## 4. Discovery vs Validation

**PASS.** Discovery instrument = XAUUSD only (§2). Validation universe = the five locally available M1 markets; eligibility by data availability, timestamp integrity, and minimum event count only (§3, §17) — never by performance. XAUUSD remains inside the validation universe and its p-value must clear Holm like any other market (§16) — conservative, prevents a single-market claim from auto-generalizing.

## 5. Control Event (prior blocker F1)

**RESOLVED in v1.1.0.** §11 now uniquely specifies:

- **Control** = an eligible rejected sweep with **no qualifying reversal confirmation from the end of the sweep-rejection candle through 17:00:00 ET**.
- **Control MFE anchor** = the close timestamp of the rejection/sweep candle.
- **Control MFE horizon** = the next 120 minutes after that anchor.

Edge-case checks:

- *Confirmation on the same candle:* impossible — §8 requires the "first **subsequent** M1 candle." Deterministic.
- *Confirmation at exactly 17:00:00:* "through 17:00:00 ET" is inclusive → the event is a **treatment**, not a control. Deterministic (no boundary ambiguity in classification).
- *No confirmation:* control. Deterministic.
- *Event crossing the London/NY boundary:* the 120-minute horizon is read as continuous M1 data; no session labels needed. Deterministic under the literal reading.
- *Events near 17:00 / incomplete 120-minute horizon:* **REMAINING AMBIGUITY.** The protocol does not state whether the 120-minute horizon continues literally past 17:00 ET (through the unassigned 17:00–18:00 ET hour and into the next trading day's Asian session, where 24/5 data exists) or truncates at the trading-day boundary; nor how events whose full 120-minute horizon is not contained in the available data (dataset end) are handled (drop vs. partial horizon). Two reasonable implementations differ materially for late-day events. **REQUIRED CORRECTION (item 2).**

## 6. Event-Day Bootstrap (prior blocker F2)

**RESOLVED in v1.1.0.** §13 now defines the hierarchy exactly: market → chronological trading days → events within each day → day-cluster bootstrap → flattened treatment/control arrays → replicate ΔM*. Verified point-by-point against the audit mandate:

| # | Requirement | Status |
|---|---|---|
| 1 | Every event has unique market + trading-day identity | ✓ §13.1 (market, day id, direction, event type, anchor, MFE) |
| 2 | Events attached to their original day cluster | ✓ §13.2 |
| 3 | Bootstrap samples day clusters, never individual events | ✓ §13.3 |
| 4 | Day sampled twice ⇒ all events duplicated twice | ✓ §13.4 ("in their entirety") |
| 5 | Upper/lower events on same day remain together | ✓ §9, §15 |
| 6 | Treatment flattened separately from controls | ✓ §13.5 |
| 7 | Replicate statistic uses the flattened arrays | ✓ §13.6 |
| 8 | No event independently resampled | ✓ §13.4 |
| 9 | Empty replicate behavior deterministic | ✓ §13.7 (replicate needs ≥1 finite treatment AND ≥1 finite control MFE, else invalid; B_valid = count of valid; denominator 1+B_valid — deterministic given seed) |
| 10 | Observed ΔM from complete original set, same aggregation | ✓ §13 "Observed Statistic" |

**Event-weighting:** a day with two events contributes two event-MFEs to the flattened array each time its cluster is sampled — days with multiple events carry proportionally more weight in the **event-level** median. This is an explicit, registered consequence of the event-level statistic under day-cluster resampling (the protocol's dependence control); it is not an ambiguity and no correction is invented. Note: §15's "high-frequency event days do not silently inflate statistical significance" is accurate as a *dependence* claim (day-cluster resampling fixes the independence violation that iid event resampling would cause); the event-count weighting itself is a registered property. PASS.

## 7. Null-Inference (prior blocker F3 — highest priority)

**RESOLVED and MATHEMATICALLY JUSTIFIED.** §16 registers H₀: ΔM = 0, the recentered null `ΔM*_null = ΔM* − ΔM_obs`, and `p = (1 + count)/(1 + B_valid)` with `count = #{b : |ΔM*_null,b| ≥ |ΔM_obs|}` (inclusive ≥).

### A. Location equivariance — PROVEN (exact, not approximate)

The median is location-equivariant: `Med(X + a) = Med(X) + a` for any constant `a`. Define the data-level null transformation: shift **every** treatment MFE by `−ΔM_obs/2` and **every** control MFE by `+ΔM_obs/2`.

- **Observed statistic on transformed data:** `Med(T − ΔM_obs/2) − Med(C + ΔM_obs/2) = (Med(T) − ΔM_obs/2) − (Med(C) + ΔM_obs/2) = ΔM_obs − ΔM_obs = 0`. The null is imposed on the data exactly.
- **Any bootstrap replicate on transformed data:** because the shift is a constant applied to every sampled value and the median is fully location-equivariant,
  `Med(T* − ΔM_obs/2) − Med(C* + ΔM_obs/2) = (Med(T*) − ΔM_obs/2) − (Med(C*) + ΔM_obs/2) = ΔM* − ΔM_obs = ΔM*_null`
  **exactly, for every replicate** — irrespective of replicate event counts, day multiplicities, or invalid-replicate exclusion.

Therefore the registered statistic-level recentering **is** the data-level null construction; no additional data-level transformation is required. Unlike H01's class statistic (strata aggregation with empty-stratum rules, where the shortcut is only conditional), ΔM is a pure difference of medians with no aggregation structure, so the equivalence is exact in all cases. Under H₀ the null replicates are centered at ≈ 0: `E*[Med(T*)] ≈ Med(T)` and `E*[Med(C*)] ≈ Med(C)`, so `E*[ΔM*_null] ≈ ΔM_obs − ΔM_obs = 0`. This is a genuine **null-imposed bootstrap** (location-family recentering; cf. Davison & Hinkley bootstrap hypothesis testing; Politis–Romano for dependent data), not a mere re-centering of a nonzero-centered sampling distribution.

### B. Null transformation

Specified at statistic level (§16); the equivalent data-level transformation exists and is derived above. The registered construction tests H₀: ΔM = 0 (population median MFE equal across treatment/control), which is exactly the stated null.

### C. Dependence

Preserved: shifts are within-group constants (all treatment events −ΔM_obs/2, all control events +ΔM_obs/2), so day-cluster composition, within-day cross-event dependence, treatment/control grouping, and within-market serial dependence are untouched by the null imposition.

### D. Invalid replicates

Defined (§13.7): a replicate lacking ≥1 finite treatment or ≥1 finite control MFE is invalid and excluded; B_valid is the count of finite valid replicates; the denominator is `1 + B_valid`. Given the fixed seed and algorithm, B_valid is deterministic. The finite-B convention `(1 + count)/(1 + B_valid)` with inclusive `≥` is the standard add-one convention — coherent, p ∈ [1/(1+B_valid), 1], never 0, never NaN. Note (non-blocking): no cap is registered on the invalid-replicate fraction; with ≥100 confirmed events spread over hundreds of days this is practically negligible.

### E. Holm

Each market-level p enters Holm-Bonferroni step-down over the **eligible** markets (EVIDENCE-LIMITED markets with N < 100 are dropped from primary inference per §17, hence outside the family); family-wise α = 0.05; family fixed pre-result. XAUUSD (discovery) is inside the family and must clear Holm (§16) — conservative and explicit. No NaN/undefined p can arise under the registered formula. PASS.

**Overall F3: PASS — the null construction is statistically defensible for H₀: ΔM = 0.**

## 8. P-Value / Holm

- B = 10,000; seed = 20260817; L = 10; inclusive `≥`; add-one convention — all registered (§13, §16). PASS.
- CI: two-sided 95% **percentile** CI from the ordinary ΔM* sampling draws (§13) — kept separate from the null-test p-value; no studentization; no null draws substituted for the CI. PASS.
- Holm applied exactly once to the eligible market family. PASS.

## 9. Cross-Market Design

- Per-market independent scientific units with mandated labels Support/Contradicted/Inconclusive (§14). PASS as far as it goes.
- **Gap:** the mapping from (Holm-adjusted p, sign of ΔM_obs) to those three labels is **not registered** — the protocol requires each market to "definitively report" one of the three but never states the rule. Deterministic resolution exists (e.g., Support iff p_Holm < 0.05 and ΔM_obs > 0; Contradiction iff p_Holm < 0.05 and ΔM_obs < 0; Inconclusive otherwise). **REQUIRED CORRECTION (item 5).**
- A strong XAUUSD result cannot become an automatic universal claim: markets are independent units, Holm gates the family, and §18 falsification requires the effect to survive family-level inference. A failure on one market does not auto-falsify the behavior globally (per-market reporting permits mixed verdicts). The four-tier claim vocabulary (instrument-specific / asset-class-specific / cross-market / universal) exists at scope level (§2) but no explicit outcome→tier mapping table is registered — recommend adding it at report stage (note, not an execution blocker).

## 10. Data Gates

- **PASS items:** invalid prices ≤ 0 halt; N ≥ 100 confirmed events required per market else EVIDENCE-LIMITED and dropped from primary inference; >10% invalid-day fraction halts for anomaly audit; missing terminal data / corrupted timestamps halt.
- **REMAINING AMBIGUITIES (REQUIRED CORRECTION — item 4):**
  - *Invalid-day denominator:* ">10% of calendar days" is undefined. If taken literally as *all calendar days in the dataset range*, weekend days with no bars would count as invalid for the 24/5 markets (XAUUSD/XAGUSD/EURUSD), tripping the gate by construction. The denominator must be pinned (e.g., calendar days containing at least one M1 bar).
  - *"Required session bars":* what a day must contain to be valid (Asian session reference bars? London/NY bars? minimum counts?) is not quantified.
  - *Duplicate timestamps / missing bars within sessions / partial first-day sessions* (e.g., XAUUSD starts 2021-04-12 07:00 ET): no deterministic rule registered (recommend keep-first, consistent with repo convention).
  - *Assessment timing:* the gate is not stated to be assessed before primary inference.
- *Minimum control count:* only confirmed events are gated (N ≥ 100). Controls are rejected sweeps without confirmation and in practice outnumber treatments; non-blocking note.

## 11. SMC / ML Firewall

**PASS.** Objective session highs/lows, price penetrations, wicks (close vs level), deterministic fractal breaks only (§6–§8, §20). Prohibited: subjective order blocks, manual FVGs, discretionary "smart money" narratives, retrospective HMM/K-means rescue (§20). No ML anywhere in the primary design.

## 12. Outcome-Blindness

**PASS.** Complete scan: no effect values, MFE magnitudes, p-values, event counts, favorable dates, market rankings, or performance-driven parameter choices anywhere in the protocol. All parameters are structural (sessions, 120-min, B, L, seed, α, N≥100). No code, no data processing, no statistics were performed by this audit; only schema/coverage-level inspection of the M1 files.

## 13. Findings Table

| Area | Verdict | Severity | Finding |
|---|---|---|---|
| Scientific object | PASS | — | Behavioral excursion hypothesis, MFE only, distinct from all closed lines |
| Discovery/validation scope | PASS | — | XAUUSD discovery; 5-market validation; eligibility by data only; XAUUSD p must clear Holm |
| Market universe | PASS | — | All five M1 files present with sufficient depth; eligibility deterministic |
| Sessions/timezone | PASS | — | 18:00–02:59 / 03:00–07:59 / 08:00–17:00 ET; contiguous; no overlap; `America/New_York`; 17:00–18:00 is the deliberate inter-day rollover hour (relevant only to item 2) |
| Sweep | PASS | — | Strict inequalities, London/NY only, no ATR/tick filter |
| Rejection | PASS | — | Penetration + close-failure, deterministic |
| Confirmation | CONDITIONAL | MEDIUM | "The sweep candle" ambiguous when multiple sweep+reject candles precede confirmation (item 3) |
| Event uniqueness | PASS | — | First confirmed upper/lower per market/day; both retained in one daily cluster |
| Control | CONDITIONAL | MEDIUM | Core fixed (absence window through 17:00 ET, anchor = rejection-candle close, 120-min horizon); horizon boundary at 17:00/trading-day end and incomplete horizons undefined (item 2) |
| MFE | CONDITIONAL | MEDIUM | Anchoring and formulas exact; horizon boundary/incomplete-horizon semantics undefined (item 2); note: treatment MFE strictly positive by construction while control MFE can be negative — registered anchoring property, not a defect |
| Event/day bootstrap mapping | PASS | — | §13 fully specifies flattening; event weighting is a registered consequence |
| Null construction | PASS | — | Location-equivariance proof: ΔM*_null = ΔM* − ΔM_obs is exactly the null-imposed data-level transformation |
| P-value | PASS | — | (1+count)/(1+B_valid), inclusive ≥, add-one convention, deterministic |
| Holm | PASS | — | Eligible-market family, α = 0.05, pre-result, no NaN possible |
| Data quality | CONDITIONAL | MEDIUM | Invalid-day denominator, "required session bars", duplicate/missing-bar handling, gate timing undefined (item 4) |
| Outcome-blindness | PASS | — | No outcome values anywhere |
| Strategy firewall | PASS | — | MFE only; no PnL/expectancy/spread/slippage/entry/stop/target/sizing |
| ML firewall | PASS | — | Objective geometry only; no K-means/HMM/ML rescue |
| Executability | CONDITIONAL | HIGH | Five precision items force an unregistered implementation choice today (items 1–5) |

## 14. Required Corrections (deterministic, uniquely resolvable — a v1.2.0 precision amendment)

1. **Stationary-bootstrap mechanics (§13/§15):** register the exact algorithm — continuation probability p = 1/L = 0.1; block start index uniform over day-cluster positions; circular wrap at the end of the chronological day sequence; continue until length ≥ N then truncate to exactly N, where N = number of day clusters (days containing ≥1 eligible event), fixed for all replicates; state labels stay attached to sampled day-cluster tuples; no rerun of any rolling classifier (none exists here); no iid event-level resampling. (This is the same class of explicit wording that the Session Range Expansion protocol required in v1.1.1/v1.1.2.)
2. **MFE horizon semantics (§10/§11):** state that the 120-minute horizon is the literal wall-clock window of M1 bars strictly after the anchor timestamp (continuing past 17:00 ET and into the next trading day's Asian session where data exists) OR truncating at the trading-day boundary — one of these must be registered — and define the incomplete-horizon rule for events whose full 120 minutes are not contained in the available data (recommend: require the complete horizon, else exclude the event).
3. **Sweep-candle reference (§8/§9):** pin that the first qualifying sweep+reject candle of the day opens the pending state, its opposite extreme is the fixed confirmation reference, and later sweep candles before confirmation do not reset the reference; confirmation = first subsequent close beyond that fixed reference.
4. **Data gates (§17):** pin the invalid-day denominator (e.g., calendar days containing at least one M1 bar), quantify "required session bars" per day, register duplicate (keep-first) and missing-bar handling, and state that the gate is assessed before primary inference.
5. **Classification rule (§14/§16/§18) + median convention (§12):** register the exact mapping from (p_Holm, sign of ΔM_obs) to Support/Contradicted/Inconclusive, and the even-n median definition (average of the two middle order statistics) applied identically to observed and replicate statistics. Optionally add the outcome→claim-tier mapping table at report stage.

## 15. Final Execution Recommendation

**DO NOT EXECUTE.** Apply the five deterministic corrections listed in §14. After a v1.2.0 amendment and a final independent re-audit, the protocol is then fully executable: another researcher can implement it from the text alone without asking the author any scientific question. The null-inference construction is already mathematically justified and does not need to change.

## 16. Integrity

Strictly read-only: no file modified; no script written; no data processed beyond schema/coverage inspection of the five M1 files (headers, row counts, date ranges); no ΔM, MFE, p-value, bootstrap, or event statistic computed; no historical outcome inspected; no parameter tuned. The only new artifact is this audit. Governance, protocol, screening, prior audit, closed-line records (DISC-021/022/024), BOE/Assembly/Deployment, and all frozen research artifacts are untouched.
