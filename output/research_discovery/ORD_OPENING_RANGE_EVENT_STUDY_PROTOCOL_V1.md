# QUANTFORGE — OPENING-RANGE DIRECTIONAL BREAK (ORD)
# EVENT-STUDY PRE-REGISTRATION PROTOCOL V1

## 0. Identity and Version

- **Protocol version:** V1.0.0 (outcome-blind pre-registration).
- **Authoritative scientific definition:** `output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md` (Definition Lock V1). Where any conflict exists, the Definition Lock is authoritative.
- **Candidate origin:** `output/research_discovery/TRADEABLE_EDGE_DISCOVERY_SCREENING_V3.md` (primary candidate).
- **Protocol SHA-256 (self-hash, computed at finalization):** to be recorded at execution per §26; the pre-registration copy is byte-frozen from this writing.
- **Status:** PRE-REGISTRATION ONLY. No execution is authorized by this document. The exact next task is an independent read-only pre-registration audit; execution proceeds only after PASS.

## 1. Scientific Question

> Does a deterministic break of a pre-defined market opening range produce a statistically and economically meaningful **directional continuation after the breakout entry** across a multi-market validation universe?

Association/behavior only. No causal institutional-intent claim, no profitability claim, no strategy claim.

## 2. Version History

- **V1.0.0:** Initial outcome-blind pre-registration translating Definition Lock V1. No parameters tuned; no historical outcome inspected.

## 3. Frozen Universe

Primary validation markets (M1):

- **XAUUSD**
- **XAGUSD**
- **USATECHIDXUSD**
- **BTCUSD**

**EURUSD is EXCLUDED** from the primary family until its invalid-day data-quality gate is independently resolved (recorded DISC-025). No market may be added because of historical results. Markets below the evaluability threshold (§13) are reported EVIDENCE-LIMITED and contribute no primary verdict.

## 4. Session / Opening Range (frozen)

- Canonical timezone: **America/New_York** (DST via `zoneinfo`); M1 timestamps are UTC and converted deterministically.
- **XAUUSD, XAGUSD, BTCUSD — opening anchor:** London reference, window **03:00:00–03:29:59 ET inclusive** = exactly **30 M1 timestamps**.
- **USATECHIDXUSD — opening anchor:** US cash open, window **09:30:00–09:59:59 ET inclusive** = exactly **30 M1 timestamps**.
- **Range:** `High_OR = max(high)` and `Low_OR = min(low)` over the 30 window bars; range width `W = High_OR − Low_OR` (descriptive/eligibility only).
- **Day eligibility (deterministic):** all 30 window timestamps present with valid OHLC (> 0) and `W > 0`. Days failing any condition are ineligible (no event, counted per §20 invalid-day rule).
- **Immutability:** the range is fixed at the window close and never includes evaluation-phase bars (no look-ahead).

## 5. Breakout Event (frozen)

- **Long breakout:** the first M1 bar after the opening window (through **17:00:00 ET inclusive** of the same NY calendar day) with `Close_t > High_OR` (strict).
- **Short breakout:** the first M1 bar with `Close_t < Low_OR` (strict).
- Close-based (executable at detection); high/low penetration alone does not qualify; touching the boundary (`Close == edge`) does not qualify.
- **First per direction per day;** a failed break (close beyond, then close back inside) does not reset the already-defined first-event structure; later attempts create no new event.
- **Simultaneous upper/lower:** impossible on one bar (`High > Low`); both directions may occur on the same day (§11).

## 6. Entry (frozen)

- **Entry price = the breakout candle close** (the close of the first qualifying bar). The breakout candle IS the entry event.
- No confirmation lag, no next-bar substitution, no intrabar assumptions beyond the registered close-based event.
- The primary response is anchored at this price (mandatory Definition-Lock rule).

## 7. Invalidation (frozen)

- **Long:** a subsequent close `≤ High_OR` (re-entry through the broken upper edge).
- **Short:** a subsequent close `≥ Low_OR` (re-entry through the broken lower edge).
- Evaluated bar-by-bar from the bar after entry; **no price buffer**.
- **Primary-response interaction (registered):** the primary behavioral response (§8) is the **unconditional** 120-minute horizon return from the entry close and is **not truncated by the invalidation**. The invalidation is recorded as a per-event flag (descriptive secondary; the future economic translation's structural stop). For that future economic use, if invalidation and a terminal exit coincide on the same bar, **invalidation is evaluated first** (stop-first, conservative); this precedence is inherited by the economic stage only.

## 8. Primary Response (frozen)

Directional return from the **actual entry close** to the **complete 120-minute horizon close**, in basis points of the entry price:

- Long: `R = 10000 × (Close[entry+120min] − EntryClose) / EntryClose`
- Short: `R = 10000 × (EntryClose − Close[entry+120min]) / EntryClose`

**Primary scientific response.** Entry-anchored by construction (Definition-Lock mandatory rule). MFE is never substituted for the primary response.

## 9. Horizon (frozen)

- `H = 120 minutes`, literal wall-clock from the entry close; may cross session boundaries into subsequent 24/5 data.
- **Complete horizon required:** the M1 bar at entry+120 min must exist; otherwise the event is **excluded before primary inference**. No imputation, no truncation, no partial windows, no alternative horizons (no grid).

## 10. Control Group (frozen)

- **Control event (per direction per day):** the **first penetration** of an opening-range edge followed by the **absence of any qualifying close-break** in that direction through 17:00:00 ET — i.e., ≥1 bar with `high > High_OR` (upper attempt) or `low < Low_OR` (lower attempt), and no `Close > High_OR` (respectively `Close < Low_OR`) anywhere through 17:00:00 ET.
- **Control anchor:** the close of the **first penetration candle**.
- **Control directional response (frozen — see Resolution Note):** measured in the **continuation (attempt) direction**:
  - upper penetration control → hypothetical **LONG** response (up-move from the anchor close, same 120-min horizon);
  - lower penetration control → hypothetical **SHORT** response (down-move from the anchor close, same 120-min horizon).
- Same 120-minute horizon and completeness requirements as treatment. No matching; no post-result control selection.

### Resolution Note (documented for the independent audit)

The pre-registration instruction's example mapping ("upper penetration control = hypothetical short-direction response; lower penetration control = hypothetical long-direction response") conflicts with the authoritative Definition Lock (§12: control response "signed by the attempt direction"). Per §0, the Definition Lock is authoritative. The continuation-direction mapping is the coherent one for the frozen statistic `ΔM = median(treatment) − median(control)`: the treatment for an upper close-break is a LONG response, so the comparable control (same geometry, absent the registered event) must also be a LONG response; an opposite-signed control would measure the fade (down-move after a failed upside attempt), conflating continuation-after-break with reversion-after-failure and no longer isolating the registered question. This resolution is definitional (first principles), not outcome-derived; it is flagged here explicitly so the independent pre-registration audit can verify it.

## 11. Event Uniqueness / Hierarchy (frozen)

- Per market per trading day, at most **two** directional events:
  - long side: first qualifying close-break → **treatment**, else first penetration → **control**, else none;
  - short side: same, independently.
- Long/short events on the same day remain **coupled inside the day cluster**; no event is independently resampled.
- Hierarchy: market → chronological trading day → events (≤ 2) → day-cluster bootstrap.

## 12. Market-Level Primary Statistic (frozen)

- `ΔM_market = Median(Response_treatment) − Median(Response_control)`
- **Primary direction:** `ΔM_market > 0`.
- **Median convention (frozen):** odd n → middle ordered observation; even n → arithmetic mean of the two central ordered observations. Identical for observed and bootstrap statistics.
- Observed statistic computed from the complete original event set before any resampling.

## 13. Evaluability (frozen)

- A market is **EVALUABLE** iff it has **≥ 100 confirmed treatment events**; otherwise **EVIDENCE-LIMITED** (descriptive reporting only; no primary verdict).
- **Treatment and control must both contain finite observations.** A market with zero finite control observations is NOT EVALUABLE (all replicates invalid → `B_valid = 0` → no p-value) and is reported under the EVIDENCE-LIMITED regime with the reason recorded.
- **No separate minimum control count is registered**, with the following explicit justification: scarce controls are already accounted for deterministically by the replicate-validity rule (§14) and the finite-`B_valid` p-convention (§15); a market with very few controls yields a small `B_valid`, raising the p-value floor and preventing spurious significance, without manufacturing an additional threshold. As a reporting-only flag, markets with `B_valid < 1000` receive a **LOW-CONTROL-RELIABILITY** note (deterministic; cannot by itself change a verdict).

## 14. Dependence / Bootstrap (inherited, documented)

The project's validated **day-cluster stationary bootstrap** machinery is inherited from the Liquidity-Sweep v1.2.0 protocol (§13), documented precisely:

- **Sampling unit:** the chronological sequence of trading-day clusters (days containing ≥1 eligible event). `N` = the number of day clusters in the original eligible sequence, fixed once, identical for every replicate, never recomputed inside a replicate.
- **Per replicate:** (1) uniform block start over the N positions; (2) emit the day cluster with its full event array; (3) block-termination decision: terminate with probability `p = 0.1`, continue with probability `0.9` (geometric block length, expected length `1/p = 10 = L`); (4) on termination, new uniform start; (5) on continuation, advance chronologically with **circular wrap** at sequence end; (6) continue until length ≥ N, then **truncate the final block to exactly N** day clusters.
- **Event flattening:** after the day sequence is formed, treatment responses are flattened into one array and control responses into another; the replicate statistic is `ΔM* = Median(treatment*) − Median(control*)`.
- **Replicate validity:** a replicate is valid iff it contains ≥ 1 finite treatment and ≥ 1 finite control observation; `B_valid` = number of valid replicates.
- **B = 10,000; L = 10; seed = 20260818** (date-convention seed fixed at pre-registration, the day after the definition-lock session; documented, not outcome-derived).
- Repeated day selection duplicates all its events; long/short same-day events move together; no event is independently resampled.

## 15. Null-Inference (inherited, justified)

- **H0: ΔM = 0.**
- **Null construction (inherited and justified):** because the median is location-equivariant, the recentered bootstrap `ΔM*_null = ΔM* − ΔM_obs` is exactly the null-imposed distribution for a difference of medians (validated in the Liquidity-Sweep Final Clearance Audit V2; no alternative construction is used). Dependence, day clusters, and treatment/control membership are preserved; nothing is re-matched or reclassified inside the null.
- **p-value:** `p = (1 + count) / (1 + B_valid)` with `count = #{b : |ΔM*_null,b| ≥ |ΔM_obs|}` (inclusive `≥`). `p` can never be zero; `p` is defined iff `B_valid ≥ 1`.

## 16. Confidence Interval (frozen)

- Ordinary **percentile sampling CI** of the `ΔM*` distribution: **2.5th and 97.5th percentiles** (95% two-sided).
- Computed from the ordinary sampling draws, **separate from the null distribution**; no studentization; no null transformation in the CI.

## 17. Multiple Comparisons (frozen)

- **Primary family:** all **evaluable** markets (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD, subject to §13).
- **Holm step-down** at family-wise **α = 0.05** over the exact market-level p-values.
- Evidence-limited markets are retained in reporting but produce no primary verdict; **no post-result market removal**; no secondary test enters the family.

## 18. Market Classification (frozen)

- **SUPPORT:** Holm p < 0.05 AND `ΔM_obs > 0`.
- **CONTRADICTED:** Holm p < 0.05 AND `ΔM_obs < 0`.
- **INCONCLUSIVE:** otherwise.
- **EVIDENCE-LIMITED:** < 100 treatment events (no primary verdict).
- No equivalence margin.

## 19. Cross-Market Interpretation (frozen)

The protocol distinguishes: **instrument-specific** (one market); **asset-class** (multiple related instruments); **cross-market** (distinct mechanisms); **universal** (never claimed merely because several markets pass). The experiment validates across the registered universe; forced universality is excluded.

## 20. Data Gates (frozen)

- **Input:** UTC M1 OHLC (`timestamp, open, high, low, close, volume`; volume unused).
- **Duplicate timestamps:** sort chronologically, **keep-first**; then construct windows/events.
- **Invalid OHLC:** any required OHLC value ≤ 0 invalidates the affected bar/day.
- **Opening-range completeness:** all 30 window M1 bars required (day ineligible otherwise).
- **Event-session completeness:** breakout/penetration detection requires data through 17:00:00 ET (bars may be missing inside the window without automatic failure — no hidden gapless-session requirement — but the specific required bars must exist for the event and horizon rules).
- **Horizon completeness:** full 120-minute window required per §9.
- **Invalid-day denominator (explicit, not silently borrowed):** all calendar dates containing ≥ 1 M1 observation after timestamp normalization and duplicate removal; weekends/holidays with no data are not counted. An **invalid day** = a date with ≥ 1 observation that fails the opening-window completeness gate (missing/zero-width/§20-invalid window). The **invalid-day fraction** is computed BEFORE primary inference; **if it exceeds 10%, execution HALTS for an anomaly audit** (the 10% threshold is inherited from the project's data-gate convention; the invalid-day definition is registered here explicitly, correcting the ambiguity recorded in DISC-025).
- **Three-way distinction (not conflated):** invalid day; eligible day with zero events; event with incomplete horizon (excluded pre-inference).

## 21. Chronological Stability (descriptive)

- **Halves:** first `floor(N/2)` eligible event days = first half; the remaining days = second half. **No date-based midpoint.**
- Halves are descriptive only; they cannot alter the primary verdict, family, or classification.

## 22. Secondary Analyses (descriptive, non-rescuing)

- MFE from entry (over [entry, entry+120]); range-width-normalized continuation (`R / W`); invalidation rate; event frequency (per market, per direction); chronological halves; year-by-year stability.
- No secondary can rescue a failed primary, a failed market, or a failed universe; no parameter may be selected using secondaries; secondaries run only after the primary is frozen.

## 23. Economic Capture Boundary

- This behavioral protocol calculates **no PnL, spread, slippage, commission, or position sizing**.
- **Design rationale recorded (not economic evidence):** the primary response is measured from the actual executable breakout close, so the measured object is capturable in principle; this is the Definition-Lock design constraint, and economic viability is tested in a separate later stage with observed MT5 costs.

## 24. Closed-Line Independence (frozen)

- **vs Mean Reversion (DISC-021):** ORD is a directional continuation object; response signed by break direction; no reversion response, no displacement/recoil/persistence machinery.
- **vs TSMOM (DISC-022):** intraday, event-driven, session-structure object; no rolling lookback window, no drift benchmark, single fixed-horizon post-entry move.
- **vs Session Range Expansion (DISC-024):** tests whether an opening-range **close-break** precedes **directional continuation** (direction object), not whether compression precedes larger range size (volatility object, contradicted).
- **vs Liquidity Sweep / Reversal (DISC-025):** current-session opening range + close-break + **no rejection, no confirmation lag** + response from the entry close (trend object), versus prior-Asian-extreme breach + rejection + confirmation + excursion from the Asian level (reversal object). ORD is not a repaired sweep; no prior-extreme reference, no rejection, no confirmation lag, entry-anchored response.

## 25. ML Firewall

No ML, K-means, HMM, clustering, or regime classifier in this protocol. Future ML is a separate research object after the deterministic ORD object is established.

## 26. Reproducibility (mandatory, correcting DISC-025 persistence gaps)

Execution MUST persist, under `output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY/`:

- protocol SHA-256 (self-hash of this document) and dataset SHA-256 fingerprints:
  - XAUUSD_M1.csv `54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c`
  - XAGUSD_M1.csv `69444be954a869ebc831cd1253849222d8babc7a02940b2bb908a5179bcf5999`
  - USATECHIDXUSD_M1.csv `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`
  - BTCUSD_M1.csv `97b853854d8f650d80e3972f159deab0b15911e19dd437e1dd10b3bab098409b`
  - EURUSD_M1.csv `5106a518e65a9d3f4c8bfc74c14fad81240a9de278bd1c4577799a6f1b79813f` (gated; not in the primary family)
- market list and parameter manifest (30-min window, anchors, strict-break conditions, entry = breakout close, invalidation edges, H = 120, B = 10,000, L = 10, seed = 20260818, α = 0.05, ≥100 threshold, >10% halt);
- software environment (Python/numpy/pandas versions), execution timestamp;
- **event tables (persisted CSV: market, trading_day, direction, type, anchor_ts, entry_close, horizon_close, response, invalidated, horizon_complete)**;
- **bootstrap draw files and null draw files (persisted — the DISC-025 gap is explicitly corrected: B = 10,000 sampling and null draws per market must be written to disk)**;
- observed statistics, p-values, CIs, Holm values;
- metadata JSON and the scientific report. UTF-8 for text.

## 27. Outcome-Blind Self-Audit

Verified: no historical ORD results, no PnL values, no historical event counts, no market ranking, no parameter optimization, no market chosen by performance appear in this protocol. All parameters are frozen from the Definition Lock (market mechanics) or the inherited validated machinery; the seed is a date convention; the control-direction resolution (§10) is definitional and flagged for the audit.

## 28. Exact Next Task

> **INDEPENDENT READ-ONLY ORD PRE-REGISTRATION AUDIT.** No execution before audit PASS. After PASS: one controlled multi-market execution → scientific adjudication → economic translation with observed MT5 costs.

## 29. Integrity

Strictly read-only and outcome-blind; the only new repository artifact is this protocol. No code, no experiment, no PnL, no backtest, no governance modification. Inherited machinery is documented precisely rather than silently copied; the control-direction resolution and the explicit invalid-day definition are registered transparently for the independent audit.
