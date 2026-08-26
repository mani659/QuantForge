# QUANTFORGE — CROSS-MARKET LIQUIDITY SWEEP / REVERSAL
# FINAL INDEPENDENT EXECUTION CLEARANCE AUDIT V2

- **Audit object:** `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL_EVENT_STUDY_PROTOCOL_V1.md`
- **Protocol version audited:** v1.2.0 (protocol SHA-256 `c6b8fbd45dc8ffc33307346fb0d8e28bf6953792dbfd7635199af4f8b774ee06`)
- **Audit type:** FINAL, adversarial, READ-ONLY execution-clearance gate (last pre-execution gate)
- **Audit date:** 2026-08-17
- **Lineage read:** v1.2.0 protocol (authoritative); v1.2 precision-amendment record (five corrections); final clearance audit V1 (CONDITIONAL PASS, five required corrections); independent pre-registration audit V1 (three blockers); definition screening V1; `docs/SESSION_HANDOFF.md`; `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-001..024); `research/knowledge/RESEARCH_TIMELINE.md`; `data/m1/` five-market inventory.
- **Data inventory (schema/coverage only; no statistic computed):**

  | File | Rows | Coverage (UTC) |
  |---|---|---|
  | XAUUSD_M1.csv | 1,768,123 | 2021-04-12 11:00 → 2026-04-10 20:59 |
  | XAGUSD_M1.csv | 1,729,136 | 2021-07-13 00:00 → 2026-07-12 23:59 |
  | EURUSD_M1.csv | 2,041,613 | 2021-01-04 00:00 → 2026-06-30 23:59 |
  | BTCUSD_M1.csv | 2,539,807 | 2021-05-23 00:00 → 2026-05-22 23:59 |
  | USATECHIDXUSD_M1.csv | 906,815 | 2023-09-01 00:00 → 2026-07-10 20:14 |

---

## 1. Executive Verdict

**PASS — APPROVED FOR MULTI-MARKET EXECUTION.**

The v1.2.0 protocol is fully deterministic, statistically defensible, and executable from the protocol text alone without any new scientific, statistical, or data-treatment decision. All five corrections required by the V1 clearance audit are applied and verified; the null-inference construction is mathematically proven (median location equivariance); every gate, boundary, and classification rule is uniquely pinned. No material ambiguity remains. The only residual items are non-blocking numerical/reporting conventions that cannot alter any scientific verdict.

## 2. Protocol Integrity

- v1.2.0 is the current version (header §title and §0); v1.0.0 and v1.1.0 history preserved verbatim; §0 documents exactly the five v1.2.0 clarifications. PASS.
- No scientific object, universe, parameter (B = 10,000; L = 10; seed = 20260817; α = 0.05; 120-minute horizon; N ≥ 100), event definition, or firewall changed by the amendment. PASS.
- No result value, event count, MFE, p-value, market ranking, or favorable date appears anywhere in the protocol. PASS.

## 3. Scientific Object

**PASS.** The frozen object is exactly: deterministic breach of the prior Asian-session extreme → rejection (wick close-failure) → deterministic micro-structural reversal confirmation (first later close beyond the frozen sweep-candle extreme) → measurement of directional MFE over a fixed 120-minute horizon. Behavioral hypothesis only: no causal institutional-intent claim (the screening's stop-liquidity narrative is motivation, not an assertion the experiment tests), no profitability claim, no strategy claim, no ML claim.

## 4. Discovery vs Validation

**PASS.** Discovery instrument = `XAUUSD` (§2). Validation universe = the five locally available M1 markets (§3), all present with sufficient depth (see inventory). Eligibility rests only on data availability, timestamp integrity, session coverage, and minimum event count (§3, §17) — never performance. Markets are independent scientific units (§14): a failure on one market does not globally falsify the behavioral family, and a success on one market (including XAUUSD, which must clear Holm like any other) does not globally establish it.

## 5. Session Definitions

**PASS.** Asian 18:00:00 ET (prior day) → 02:59:00 ET inclusive; London 03:00:00 → 07:59:00 inclusive; NY 08:00:00 → 17:00:00 inclusive; all under `America/New_York` (DST deterministic). No overlap (adjacent boundaries); no gap within the trading-day partition (the union covers 18:00 prior-day → 17:00 current-day continuously; the 17:00–18:00 hour is the deliberate inter-day rollover, outside event evaluation and explicitly handled by the MFE horizon rule). Monday construction is deterministic (Monday's Asian reference = Sunday 18:00 → Monday 02:59 under the literal prior-calendar-day reading); a day with no valid Asian reference bars is an invalid day per §17 (weekends with no data are excluded from the denominator by the registered definition).

## 6. Asian Reference

**PASS.** AsianHigh = max(high), AsianLow = min(low) over the Asian session (§5), computed and frozen before any London/NY bar is evaluated (§5). No future information enters the reference.

## 7. Sweep / Rejection

**PASS.** Upper sweep `High_t > AsianHigh`, lower sweep `Low_t < AsianLow` — strict inequalities; touching alone does not qualify; no ATR/tick/minimum-penetration threshold (§6). Rejection: `High_t > AsianHigh AND Close_t <= AsianHigh` / `Low_t < AsianLow AND Close_t >= AsianLow` (§7). All deterministic.

## 8. Sweep-Candle Reference

**PASS (v1.2.0 correction 3).** §8 registers: the first qualifying sweep-and-rejection candle opens the pending confirmation state; its opposite extreme is frozen (upper: freeze that candle's `Low`; lower: freeze that candle's `High`); later sweep candles do NOT reset or replace the reference; confirmation is the first later close strictly beyond the frozen reference. No ambiguity remains between multiple preceding sweep candles.

## 9. Event Uniqueness

**PASS.** First confirmed upper and first confirmed lower per market per calendar trading day are retained (§9); if both occur on the same day they remain attached to the same day cluster (§9, §15); events are never independently resampled (§13); the frozen-reference rule (§8) removes any competing-candidate ambiguity. Control counting is deterministic under the registered rules: a rejected sweep is a control iff no qualifying close beyond the frozen direction reference occurs within [its own rejection-candle end, 17:00:00 ET] (§11, §8); sweep candles subsumed by the day's confirmation are neither treatment nor control; post-confirmation sweeps with no qualifying confirmation in their own window are controls. Verified convergent across literal readings — no scientific decision required.

## 10. Treatment / Control MFE

**PASS (v1.2.0 correction 2).** Treatment: Upper `AsianHigh − min(low)`, Lower `max(high) − AsianLow` over the complete 120-minute horizon (§10). Control: rejected sweep with no qualifying confirmation through 17:00:00 ET, anchored at the rejection-candle close, over the same complete 120-minute wall-clock interval (§11). §10 registers: the window is literal wall-clock beginning at the event anchor timestamp, may cross 17:00 ET into 24/5 data, is never truncated at session boundaries, never imputed, never partial; events whose full 120-minute window is unavailable are excluded before primary inference; the rule is identical for treatment and control. Treatment and control are therefore measured on a deterministic, comparable temporal basis. (Registered property: treatment MFE is strictly positive by construction while control MFE may be negative — an anchoring consequence of the swept-level reference, not a defect; the difference-of-medians statistic handles signed values.)

## 11. Day/Event Bootstrap

**PASS (v1.2.0 correction 1).** Full hierarchy registered (§13): market → chronological trading days → events attached to days → day-cluster stationary bootstrap → flattened treatment arrays → flattened control arrays → replicate ΔM*. Repeated day selection duplicates all its events in their entirety; upper/lower same-day events move together; no event is independently resampled; the observed statistic uses all eligible original events with the same aggregation; the replicate statistic uses all events contained in the sampled days. Two-event days receive two observations in the event-level median — an explicit, registered weighting consequence of the event-level statistic under day-cluster resampling; clearly defined, therefore PASS (not a defect).

## 12. Stationary Bootstrap

**PASS (v1.2.0 correction 1).** §13 registers: sampling unit = chronological day-cluster sequence; N fixed once from the original eligible sequence (identical for every replicate, never recomputed); per replicate — uniform first block start over the N positions; emit the day cluster with its full event array; termination probability p = 0.1 / continuation 0.9 (geometric blocks, expected length 1/p = 10 = L); on termination a new uniform start; on continuation advance chronologically with circular wrap at sequence end; continue until length ≥ N then truncate the final block to exactly N. B = 10,000; seed = 20260817. All event payloads remain attached to their sampled day.

## 13. Null-Inference

**PASS — mathematically proven.** The registered construction is `ΔM*_null = ΔM* − ΔM_obs` under H₀: ΔM = 0 (§16). By median location equivariance (`Med(X+a) = Med(X)+a` for constant a), the data-level transformation "shift every treatment MFE by −ΔM_obs/2 and every control MFE by +ΔM_obs/2" yields, for **arbitrary** treatment/control samples (any composition, unequal sizes):

`Med(T − ΔM_obs/2) − Med(C + ΔM_obs/2) = (Med(T) − ΔM_obs/2) − (Med(C) + ΔM_obs/2) = ΔM* − ΔM_obs = ΔM*_null`

exactly, for every replicate — because the shift is a within-group constant and the finite-sample median is fully location-equivariant. The observed statistic on the transformed data is exactly 0 (null imposed); dependence is preserved (day clusters intact, within-day cross-event dependence intact, treatment/control membership unchanged, within-market serial dependence preserved through day-cluster blocks); the null replicates are centered at ≈0 under H₀. This is a genuine null-imposing bootstrap, not a mere re-centering of a nonzero-centered sampling distribution, and no H01-specific assumption is imported — H01's strata aggregation made its shortcut only conditional; here the statistic is a pure difference of medians, so the equivalence is exact in all cases. Per the audit standard, no separate data-level transformation is demanded.

## 14. P-Value / CI

**PASS.** P-value: `count = #{b valid : |ΔM*_null,b| ≥ |ΔM_obs|}` (inclusive `≥`); `p = (1 + count)/(1 + B_valid)`; valid replicate = at least one finite treatment and one finite control MFE (§13.7); B_valid = count of valid replicates, deterministic given seed; p ∈ [1/(1+B_valid), 1] — never zero, never NaN for an eligible market. CI: two-sided 95% percentile CI (2.5th/97.5th percentiles) from the ordinary ΔM* sampling draws (§13), distinct from the null-test p-value (§16), not the null distribution, not studentized. Non-blocking note: the percentile interpolation convention is not pinned; as a descriptive interval (verdicts come from the Holm p-value, not the CI), this cannot change any classification and should simply be recorded in the execution report.

## 15. Holm / Market Classification

**PASS (v1.2.0 correction 5).** Holm-Bonferroni step-down over the pre-registered eligible-market family, α = 0.05, no market removed after results, no secondary test enters the family, XAUUSD remains inside the family (§16). Market-level classification (§14): SUPPORT iff Holm p < 0.05 AND ΔM_obs > 0; CONTRADICTED iff Holm p < 0.05 AND ΔM_obs < 0; INCONCLUSIVE otherwise; EVIDENCE-LIMITED = fewer than 100 eligible confirmed treatment events → descriptive results only, no primary classification, no artificial failure. Median convention pinned (even-n = arithmetic mean of the two central ordered observations; identical for observed and replicate statistics).

## 16. Cross-Market Interpretation

**PASS.** Per-market independent units with the registered classification rule; the four-tier claim vocabulary (instrument-specific / asset-class-specific / cross-market / universal) is explicitly a report-stage matter kept separate from per-market classification (§14); universal is never claimed merely because several markets pass (Holm family + independent units). No automatic generalization in either direction.

## 17. Data Gates

**PASS (v1.2.0 correction 4).** §17 registers: duplicate timestamps → chronological sort, keep-first, then construct sessions/events; invalid required OHLC (any value ≤ 0) invalidates the observation; missing bars not automatically fatal unless an explicit gate fails (no hidden gapless-session requirement); required session coverage per role (Asian ≥ 1 valid bar for reference formation; London/NY ≥ 1 valid bar for sweep evaluation; complete 120-minute MFE window per §10); invalid-day denominator = calendar trading dates containing at least one M1 observation after timestamp normalization and duplicate removal (weekends with no data are not invalid days); invalid-day fraction evaluated BEFORE primary inference; > 10% → stop for anomaly audit; minimum 100 confirmed treatment events for evaluability; explicit three-way distinction between invalid day / eligible day with zero qualifying events / event with incomplete MFE horizon. All gates occur before inference.

## 18. Outcome-Blindness

**PASS.** Complete scan: no historical MFE values, event counts, p-values, market rankings, favorable dates, or performance-derived parameters. All parameters are structural. This audit computed no statistics (schema/coverage inspection only).

## 19. Firewalls

**PASS.** Economic: no PnL, expectancy, spread, slippage, entry, stop, target, or sizing (§19, §21 — verified these appear only as prohibitions). SMC: objective geometry only (sessions, penetrations, wicks, deterministic fractal breaks) (§20). ML: no K-means/HMM/ML rescue (§20). Strategy: no EA/strategy construction during the behavioral experiment (§21).

## 20. Project-End-Goal Alignment

**PASS.** This is a candidate-validation stage, not the final product. Success path: behavioral validation → separate strategy/economic translation → cost-aware validation → demo forward test → months of monitoring → live consideration (§19, §21; screening V1 §12). Failure path: the candidate/instrument result is adjudicated objectively under the registered classification and the next candidate is screened (per the session handoff's Tradeable Edge Discovery focus). No forced strategy construction.

## 21. Findings Table

| Area | Verdict | Severity | Finding |
|---|---|---|---|
| Scientific object | PASS | — | Behavioral directional-excursion hypothesis, MFE only, no intent/profit/strategy/ML claim |
| Discovery/validation | PASS | — | XAUUSD discovery; 5-market validation; per-market independent units; XAUUSD in family |
| Market eligibility | PASS | — | Data availability + timestamp integrity + session coverage + N≥100; no performance filter; all five M1 files present |
| Session definitions | PASS | — | 18:00–02:59 / 03:00–07:59 / 08:00–17:00 ET, inclusive, `America/New_York`, no overlap, no trading-day gap; Monday/weekend deterministic |
| Sweep | PASS | — | Strict inequalities; touching excluded; no ATR/tick threshold |
| Rejection | PASS | — | Penetration + close-failure; deterministic |
| Confirmation | PASS | — | Frozen first-candle reference (§8); first later qualifying close; later sweeps cannot reset |
| Event uniqueness | PASS | — | First confirmed upper/lower per day; same-day coupling; no competing-candidate ambiguity; control counting deterministic |
| Treatment MFE | PASS | — | AsianHigh−min(low) / max(high)−AsianLow; complete literal wall-clock 120-min; may cross 17:00; incomplete → excluded |
| Control | PASS | — | Rejected sweep, no qualifying confirmation through 17:00 ET, anchor = rejection-candle close, same horizon rule; comparable basis |
| Day/event bootstrap | PASS | — | Full hierarchy; repeated-day duplication; no independent resampling; two-event-day weighting is a registered consequence |
| Null construction | PASS | — | Med(T−ΔM_obs/2) − Med(C+ΔM_obs/2) = ΔM* − ΔM_obs by location equivariance; exact for all replicates; dependence preserved; no H01 assumption imported |
| P-value | PASS | — | (1+count)/(1+B_valid), inclusive ≥, p ∈ (0,1], never NaN |
| CI | PASS | — | Percentile 95% from sampling ΔM* draws; separate from null test; not studentized (interpolation convention = non-blocking record note) |
| Holm | PASS | — | Eligible-market family, step-down, α=0.05, pre-result, XAUUSD included, no secondary entry |
| Classification | PASS | — | SUPPORT / CONTRADICTED / INCONCLUSIVE / EVIDENCE-LIMITED fully mapped; median convention pinned |
| Data gates | PASS | — | Duplicates keep-first; invalid OHLC; session coverage; invalid-day denominator; >10% stop; all before inference; three-way distinction |
| Outcome-blindness | PASS | — | No outcome values anywhere |
| Firewalls | PASS | — | Economic/SMC/ML/strategy all intact |
| Executability | PASS | — | Implementable from the protocol alone; no new scientific/statistical/data decision required |

## 22. Final Execution Recommendation

**PASS — APPROVED FOR MULTI-MARKET EXECUTION.** The v1.2.0 protocol is scientifically closed, deterministic, and statistically defensible. No scientific, statistical, or methodological decision remains unresolved; the residual items are a descriptive-CI interpolation convention (record in the execution report) and descriptive reporting for EVIDENCE-LIMITED markets (permitted; classification already deterministic). Multi-market execution may begin for the five registered markets under the frozen protocol (B = 10,000; L = 10; seed = 20260817; α = 0.05; Holm family = eligible markets; null-imposing recentered bootstrap; percentile sampling CI).

## 23. Integrity

Strictly read-only: no file modified; no script written; no data processed beyond schema/coverage inspection; no ΔM, MFE, p-value, bootstrap draw, or event statistic computed; no historical outcome inspected; no parameter tuned. The only new artifact is this audit. Protocol (SHA-256 `c6b8fbd4…`), governance records, closed-line records, and BOE/Assembly/Deployment are untouched.
