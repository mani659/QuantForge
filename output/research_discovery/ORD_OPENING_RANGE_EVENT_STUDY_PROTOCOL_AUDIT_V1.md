# QUANTFORGE — ORD OPENING-RANGE DIRECTIONAL BREAK
# INDEPENDENT PRE-REGISTRATION AUDIT V1

*Strictly read-only, adversarial audit. No protocol modification; no execution; no PnL; no statistics; no Git operation. Protocol: V1.0.0, SHA-256 `cc01b23cf213abc906750d7ec1d238089047baa3b6fb9bf0beb733bf1b0649a7` (verified on disk).*

---

## 1. Executive Verdict

**PASS — APPROVED FOR ORD MULTI-MARKET EXECUTION.**

The protocol is fully deterministic and executable from the protocol text alone: every scientific object matches the authoritative Definition Lock, every statistical machine is precisely registered, and no new scientific, statistical, or implementation decision is required. The critical control-direction question resolves cleanly in the protocol's favor (§8). Three non-blocking INFO findings are recorded; none can materially change event selection, response, treatment/control assignment, inference, or classification.

---

## 2. Protocol Integrity

- **Version V1.0.0** on disk; SHA-256 verified = **`cc01b23c…`** (matches the registered pre-registration hash; repository remediation did not touch it).
- Definition Lock V1 present and unchanged (content matches the definition-lock session verbatim; SHA recorded for the record).
- **No ORD execution artifacts exist** (no event tables, no bootstrap/null draws, no report, no PnL) — verified by repository scan.
- Protocol §0 hierarchy: Definition Lock authoritative — respected throughout.
- Governance note (INFO, non-blocking): `docs/SESSION_HANDOFF.md` still reflects the DISC-025 closure (the interrupted session-close task never recorded the ORD milestone). No protocol impact; the handoff is a governance artifact.

---

## 3. Scientific Object

The frozen object is exactly: **opening range → close-break → entry at the breakout close → structural invalidation → post-entry directional movement**. Behavioral, cross-market, entry-anchored, non-profitability, non-intent, non-ML. Matches the lock §1–2. PASS.

---

## 4. Universe

XAUUSD, XAGUSD, USATECHIDXUSD, BTCUSD frozen; **EURUSD excluded** (DISC-025 data gate, hash still registered at §26 for provenance); no post-result removal; same object in every market (structural anchors only). PASS.

---

## 5. Opening Range

XAU/XAG/BTC: `03:00:00–03:29:59 ET` inclusive = exactly 30 M1 bars; USATECHIDXUSD: `09:30:00–09:59:59 ET` inclusive = exactly 30 bars; `High_OR = max(high)`, `Low_OR = min(low)`; all-30-bars + valid OHLC + `W > 0` eligibility; range frozen at window close (no look-ahead); no hidden gap rule. Matches lock §6. PASS.

---

## 6. Breakout / Entry / Invalidation

- **Breakout:** first bar after the window through `17:00:00 ET` inclusive with `Close > High_OR` / `Close < Low_OR` (strict); touching excluded; close-based; first-per-direction-per-day; no ATR/tick threshold; simultaneous upper/lower impossible on one bar. Matches lock §7.
- **Entry:** breakout candle close; event = entry; no lag, no next-bar, no intrabar. Matches lock §8 (mandatory economic-capture anchor).
- **Invalidation:** subsequent close `≤ High_OR` / `≥ Low_OR`; no buffer; primary response **unconditional** (not truncated); invalidation is a descriptive flag; stop-first precedence registered and explicitly scoped to the future economic stage only. This is an explicit, deterministic resolution of the lock's §9 same-bar note — coherent, not a new scientific decision.
- PASS.

---

## 7. Primary Response

`R_long = 10000·(Close[entry+120] − EntryClose)/EntryClose`; `R_short = 10000·(EntryClose − Close[entry+120])/EntryClose`; measured from the actual entry close; H = 120 min wall-clock (may cross session boundaries); complete horizon required (excluded otherwise); not MFE; no prior-reference anchoring. The mandatory anti-Sweep property holds by construction. PASS.

---

## 8. Control — CRITICAL CHECK

- **Control event:** first penetration of an opening-range edge (≥1 bar `high > High_OR` / `low < Low_OR`) with **no qualifying close-break in that direction through 17:00:00 ET**; anchor = first penetration close; same 120-min horizon and completeness rules; no matching.
- **Control sign (the decisive question):** the protocol signs the control response in the **continuation (attempt) direction** — upper penetration → hypothetical LONG, lower penetration → hypothetical SHORT. This is **exactly the authoritative Definition Lock §12** ("signed by the attempt direction — upper attempt → hypothetical long"). The pre-registration instruction's example sign (upper → short) conflicts with the lock; the protocol correctly follows the lock (§0 hierarchy), and its Resolution Note documents the conflict transparently for this audit.
- **Internal consistency with the registered question:** `ΔM = median(treatment) − median(control)` pools treatment and control responses under the **same direction convention** (both signed by break/attempt direction), so ΔM isolates *directional continuation after a close-break vs after a mere penetration* — the direct counterfactual for "does the break produce directional continuation." An opposite-signed control would measure continuation-vs-fade, conflating two effects and answering a different question. **The protocol's sign is internally consistent with its registered scientific question.** No blocker.
- PASS.

---

## 9. Event / Day Structure

≤ 2 events per market-day (first long + first short, each treatment-or-control by the deterministic partition); same-day long/short events coupled inside the day cluster; failed breaks create no new events; hierarchy market → day → events(≤2) → day-cluster bootstrap. PASS.

---

## 10. Bootstrap

Inherited day-cluster stationary bootstrap, documented precisely (not silently copied): N day-clusters fixed once; per replicate uniform block start; terminate with p=0.1 / continue 0.9 (geometric, expected length 10 = L); chronological continuation with circular wrap; build to ≥N then truncate to exactly N; day events attached; repeated days duplicate all events; treatment/control flattening; replicate valid iff ≥1 finite treatment AND ≥1 finite control (`B_valid`); **B = 10,000; L = 10; seed = 20260818** (date convention, documented). Matches the mission's registered machinery exactly. PASS.

---

## 11. Null / Inference

`H0: ΔM = 0`; `ΔM*_null = ΔM* − ΔM_obs`; exact null-imposing construction for a difference of medians by **location equivariance of the median** (validated construction; nothing re-matched or reclassified in the null); `count = #{b : |ΔM*_null| ≥ |ΔM_obs|}` (inclusive `≥`); `p = (1 + count)/(1 + B_valid)`; p never zero; p defined iff `B_valid ≥ 1`. PASS.

---

## 12. Holm / Classification

Family = all **evaluable** markets (per the frozen ≥100 rule); Holm step-down α = 0.05; no post-result culling; evidence-limited markets retained in reporting with no verdict; classification rules (SUPPORT / CONTRADICTED / INCONCLUSIVE / EVIDENCE-LIMITED) match the mission verbatim; no equivalence margin. PASS.

---

## 13. Data Gates

UTC M1 OHLC; deterministic UTC→ET (`zoneinfo`); duplicates keep-first after chronological sort; invalid OHLC (≤0) invalidates bar/day; 30-bar opening completeness; detection coverage through 17:00 ET; 120-min horizon completeness; explicit invalid-day denominator (calendar dates with ≥1 observation; weekends/empty days excluded); invalid day = opening-window gate failure; **>10% invalid-day fraction → HALT** (inherited project convention, registered explicitly, correcting the DISC-025 ambiguity); three-way distinction (invalid day / eligible-zero-event day / incomplete-horizon event). Deterministic throughout.

- **INFO (non-blocking):** the invalid-day gate covers **opening-window** failures only; a day with a complete opening window but a truncated post-opening session yields zero events silently (deterministic, no decision required, but a weaker coverage gate than the sweep's session-coverage rule). No registered market is expected to trigger it (all four passed the sweep's data gates).

---

## 14. Stability / Secondaries

Halves = first `floor(N/2)` eligible event days, remainder second; no date midpoint; descriptive only, cannot alter verdict/family/classification. Secondaries (MFE-from-entry, range-normalized return, invalidation rate, frequency, halves, year-by-year) are descriptive, non-rescuing, run after the primary is frozen, excluded from the family. PASS.

---

## 15. Cross-Market Interpretation

Instrument-specific / asset-class / cross-market / universal ladder preserved; the protocol cannot turn several positive markets into a universal claim; validation across the registered universe only. PASS.

---

## 16. Closed-Line Independence

Documented against all four closed lines (MR, TSMOM, Session Range, Sweep) with explicit non-similarities: directional continuation object vs reversion; intraday event vs rolling momentum; direction object vs contradicted volatility-size object; current-session opening range + close-break + no rejection/confirmation lag + entry-anchored response vs prior-Asian-extreme reversal object. Not a repaired sweep. PASS.

---

## 17. Reproducibility

Mandatory persistence list is complete and **corrects the DISC-025 gap**: protocol SHA + all five dataset SHA-256 fingerprints (**verified byte-exact against `data/m1/*` on disk**), parameter manifest, environment, event tables (registered CSV schema), **bootstrap draw files AND null draw files (B = 10,000 per market, written to disk)**, observed statistics, p-values, CIs, Holm, metadata JSON, scientific report; UTF-8. An independent researcher can reproduce the run. PASS.

---

## 18. Outcome-Blindness

Full text scan: no ORD results, no PnL, no event counts, no market rankings, no favorable dates, no performance-derived parameters. The only "contradicted" mention is the DISC-024 closed-line description. Seed is a date convention; the control-direction resolution is definitional and flagged. PASS.

---

## 19. Findings Table

| Area | Verdict | Severity | Finding |
|---|---|---|---|
| Scientific object | PASS | — | Lock-consistent; behavioral/cross-market/entry-anchored |
| Universe | PASS | — | 4 markets frozen; EURUSD excluded; no post-result removal |
| Opening range | PASS | — | 30-min anchors, 30 bars, W>0, frozen at window close |
| Breakout | PASS | — | Strict close-beyond-edge; touching excluded; through 17:00 ET; first-per-direction |
| Entry | PASS | — | Breakout-candle close; event = entry; no lag |
| Invalidation | PASS | — | Close back through broken edge; no buffer; response unconditional; stop-first scoped to economic stage |
| Primary response | PASS | — | bp return from entry close to 120-min close; anti-sweep by construction |
| Control | PASS | — | Penetration-without-close-break; sign = attempt direction per Lock §12; internally consistent with the question |
| Event uniqueness | PASS | — | ≤2/day; day-cluster coupling; no reset on failed breaks |
| Statistic | PASS | — | ΔM = median(T) − median(C); frozen median convention |
| Evaluability | PASS | — | ≥100 treatments; finite T+C; B_valid=0 → not evaluable; no control minimum, justified |
| Bootstrap | PASS | — | Day-cluster stationary; p=0.1/0.9; circular wrap; truncate to N; B=10,000; L=10; seed=20260818 |
| Null | PASS | — | Recentered pivot exact by median location-equivariance |
| P-value | PASS | — | (1+count)/(1+B_valid); inclusive ≥; never zero |
| CI | PASS | — | Ordinary percentile 2.5/97.5; separate from null; no studentization |
| Holm | PASS | — | Evaluable-market family; α=0.05; no culling |
| Classification | PASS | — | Frozen rules; no equivalence margin |
| Data gates | PASS (INFO) | Low | Invalid-day gate covers opening-window failures; truncated post-opening sessions yield zero events silently — deterministic, not a decision |
| Stability | PASS | — | floor(N/2) halves; no date midpoint; descriptive |
| Secondaries | PASS | — | Descriptive; non-rescuing; excluded from family |
| Cross-market interpretation | PASS | — | Instrument/asset-class/cross-market/universal ladder |
| Reproducibility | PASS | — | Full persistence incl. bootstrap+null draws; hashes verified vs files |
| Outcome-blindness | PASS | — | No results/PnL/counts/rankings |
| Executability | PASS | — | Two independent researchers produce identical results; no new decision |

---

## 20. Final Execution Recommendation

**PASS — APPROVED FOR ORD MULTI-MARKET EXECUTION.**

- Exactly one controlled multi-market execution of the V1.0.0 protocol (B = 10,000; L = 10; seed = 20260818; α = 0.05; Holm family = evaluable markets; null-imposing recentered bootstrap; ordinary percentile CI).
- EURUSD excluded; halted/anomaly paths follow the registered gates.
- No protocol modification, no parameter change, no new secondary, no ML, no closed-line reuse, no BOE/Assembly/Deployment change.

---

## 21. Integrity

Strictly read-only: the only new artifact is this audit; the protocol, definition lock, governance files, and Git history were not modified; no execution, no statistics, no PnL. All findings are derived from the protocol text, the authoritative Definition Lock, and verified repository state (SHA hashes, dataset fingerprints, artifact absence).
