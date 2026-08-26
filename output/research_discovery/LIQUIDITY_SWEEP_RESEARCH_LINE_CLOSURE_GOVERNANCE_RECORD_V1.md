# QUANTFORGE — LIQUIDITY SWEEP / REVERSAL
# RESEARCH-LINE CLOSURE GOVERNANCE RECORD V1

## 1. Final Status

**CLOSED** (2026-08-17). Permanent record: behavioral discovery **supported**; minimal executable translation **economically non-viable**; line formally closed with the discovery preserved. Registered as **DISC-025** in the research discovery database.

## 2. Behavioral Discovery (preserved)

The registered sweep → rejection → confirmation behavior — a strict breach of a prior Asian-session extreme, wick rejection (close-failure), and deterministic micro-structural confirmation (first later close beyond the frozen sweep-candle extreme) — was statistically supported in all four evaluable markets:

| Market | Treatment/Control | ΔM_obs | 95% CI | p_Holm | Verdict |
|---|---|---|---|---|---|
| XAUUSD | 1527 / 93 | 4.057 | [3.477, 4.582] | 3.9996e-04 | SUPPORT |
| XAGUSD | 1517 / 85 | 0.101 | [0.086, 0.114] | 3.9996e-04 | SUPPORT |
| USATECHIDXUSD | 984 / 39 | 39.787 | [32.805, 47.219] | 3.9996e-04 | SUPPORT |
| BTCUSD | 1960 / 117 | 229.100 | [188.699, 263.300] | 3.9996e-04 | SUPPORT |

Protocol v1.2.0 (SHA-256 `c6b8fbd4…`), B = 10,000, L = 10, seed = 20260817; null-imposing recentered bootstrap; Holm family = eligible markets. EURUSD: **DATA-LIMITED / NOT ADJUDICATED** (16.96% invalid-day fraction > 10% gate; halt before inference).

## 3. Cross-Market Validation

Three economically distinct mechanisms validated: precious metals (XAUUSD, XAGUSD), equity-index CFD (USATECHIDXUSD), crypto spot (BTCUSD). Evidence level: Level 2 (asset-class) established; Level 3 (cross-market) preliminary (one instrument per non-metals class); Level 4 (universal) NOT established. XAUUSD was the discovery instrument and was not given special statistical treatment (remained in the Holm family).

## 4. Economic Translation (single registered baseline, no tuning)

- Entry: close of the confirmation bar; direction: reversal side; stop: frozen sweep-candle extreme (structural invalidation); exit: close of the 120-minute behavioral horizon; risk: fixed notional; costs: **observed** MT5 per-minute median bid/ask spreads (exact-minute ≥ 98.3% of lookups).
- Result: **ECONOMICALLY NON-VIABLE in all four markets, gross-negative BEFORE transaction costs** — median gross per trade: XAUUSD −5.3, XAGUSD −11.6, USATECHIDXUSD −5.0, BTCUSD −11.8 bp; win rates 19–26%; stop-out rates 70–80%; negative in every year and both chronological halves of every market; net after observed costs (Model A) negative everywhere; cumulative net (A+4) −5,929 to −39,553 bp.

## 5. Failure Mechanism

**TRANSLATION FAILURE** (not cost failure, not behavioral failure). The validated excursion is anchored at the swept Asian level (median MFE from the level 23.0–55.8 bp); the confirmation-close entry sits 4.7–13.2 bp beyond the level; the structural stop converts the intra-window reversion into losses (70–80% stop-outs); the horizon-close exit captures the close, not the extreme. Costs are secondary. Behavioral failure (C) is not established — and that unknown does not authorize a rescue.

## 6. EURUSD Disposition

**DATA-LIMITED / NOT ADJUDICATED** — preserved verbatim. Not an economic failure, not a hypothesis result; excluded from all sweep economic work until its data-quality operationalization is separately resolved.

## 7. Why the Line Is Closed

Under the strict alternative-selection rule, no alternative translation (limit entry at the Asian level; next-bar-open entry; Asian opposite-boundary target; structural trailing exit) has a scientific/market-mechanics justification that **predates the economic result and derives from the frozen behavioral object**. Each was either a generic technique or generated in response to the failure. Therefore **no new economic protocol is authorized**, and the candidate line is formally closed with the discovery archived — consistent with the project's treatment of adjudicated closed lines (DISC-021, DISC-024).

## 8. Prohibited Rescue

For this candidate, permanently prohibited: limit entry at the Asian level; next-bar-open entry; alternate targets; trailing exits; stop optimization; ATR buffers; horizon changes; indicator confluence; ML/K-means rescue; market selection; EA construction; inverting or reinterpreting the hypothesis; merging with any other closed line. The alternatives may be useful ideas in general, but they are NOT authorized for this closed research line.

## 9. Updated Research Position

Closed lines: Mean Reversion (DISC-021), fixed 12/1 TSMOM (DISC-022), H01 broad universal formulation (closed in that form), Session-Anchored Range Expansion (DISC-024), **Liquidity Sweep / Reversal (DISC-025)**. Open: H01 Equity Track A (narrowed US-equity program; broad-US historical evidence gap remains). Active objective: **Tradeable Edge Discovery Screening** for a new, independent candidate.

## 10. Next Legitimate Task

**TRADEABLE EDGE DISCOVERY SCREENING** — screen a new, independent candidate with an explicit path from behavior → economics → trading implementation, no dependency on any closed candidate's outcome, and rapid closure of failed candidates. No demo/live/EA work is authorized by anything in this record.

## 11. Integrity

Governance update completed: `research/knowledge/RESEARCH_DISCOVERY_DATABASE.md` (DISC-025 added; Top 24 → Top 25), `research/knowledge/RESEARCH_TIMELINE.md` (§18 added; final conclusion updated to four closed lines), `docs/SESSION_HANDOFF.md` (Start-Here, research status, project position, forbidden work). No protocol changed, no experiment ran, no dataset changed, no BOE/Assembly/Deployment artifact changed, no new candidate selected. This record is the permanent scientific and economic summary of the line.

---

### Reference artifacts

- `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL_EVENT_STUDY_PROTOCOL_V1.md` (v1.2.0)
- `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL_FINAL_CLEARANCE_AUDIT_V1.md` / `_V2.md`
- `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL/SCIENTIFIC_REPORT_V1.md` + event CSVs (XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD)
- `output/research_discovery/XAUUSD_LIQUIDITY_SWEEP_REVERSAL_SCIENTIFIC_ADJUDICATION_V1.md`
- `output/research_discovery/LIQUIDITY_SWEEP_STRATEGY_ECONOMIC_TRANSLATION_V1.md`
- `output/research_discovery/LIQUIDITY_SWEEP_POST_ECONOMIC_GOVERNANCE_ADJUDICATION_V1.md`
- Data: `data/m1/*_M1.csv`; `data/tick/{XAUUSD,XAGUSD,USATECHIDXUSD,BTCUSD}_mt5_ticks.csv`; `output/xagusd_cost_viability_v1/xagusd_minute_aggregates.csv`
