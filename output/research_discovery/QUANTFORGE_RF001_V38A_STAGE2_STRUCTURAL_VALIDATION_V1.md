# QUANTFORGE — RF-001 V38A STAGE 2 STRUCTURAL VALIDATION

**Date:** 2026-09-07
**Status:** STRUCTURALLY VALID — STAGE 3 AUTHORIZED
**Purpose:** Determine whether the frozen RF-001 process is deterministic, temporally causal, synchronized, independently reproducible, free of look-ahead, structurally faithful, and mechanically consistent.

---

## 1. GOVERNING REGISTRATION

| Field | Value |
|-------|-------|
| Registration ID | RF-001-V38A-REG-V1 |
| Title | Cross-Market Confirmation Failure Process |
| Registration SHA | `3ea88d6772a45dd387ce940c6bbdd6678adedcf1bd6484b7c77d7322a15770ea` |
| Registration commit | `709673f` |
| Registration artifact | `output/research_discovery/QUANTFORGE_RF001_V38A_REGISTRATION_V1.md` |

---

## 2. FROZEN VALUES

| Parameter | Value |
|-----------|-------|
| Primary market | USATECHIDXUSD |
| Confirmation market | US500 |
| Timeframe | M1 |
| N (lookback) | 30 completed M1 bars |
| M (confirmation window) | 15 completed M1 bars |
| Session | US regular session (09:30–16:00 ET) |
| Cost model | 2 bps round-trip |
| Data domain | Forward-only prospective from 2026-09-06 08:00 ET |

---

## 3. IMPLEMENTATION PROVENANCE

| Implementation | Purpose | Source |
|----------------|---------|--------|
| `research/rf001_v38a_stage2_structural.py` | Primary Stage 2 validation | Derived from registration text |
| `research/rf001_v38a_stage2_independent.py` | Independent reproducibility check | Derived independently from registration text |

Both implementations were created from the frozen registration text. The independent implementation was written separately and does not share code with the primary implementation.

---

## 4. DATA PROVENANCE

Stage 2 validation used synthetic test data constructed from the registration specification. No historical USATECHIDXUSD or US500 M1 data was used for economic validation. No FB-001, F-01, or protected-forward data was used.

USATECHIDXUSD M1 data exists in the repository (`data/m1/USATECHIDXUSD_M1.csv`, 906,815 bars). US500 M1 data is NOT available in the repository (only FRED daily S&P 500 data exists). Production Stage 3 validation will require US500 M1 data from the forward pipeline.

---

## 5. PRIMARY STRUCTURAL EVENT VALIDATION

| Test | Description | Result |
|------|-------------|--------|
| Bullish detection | Close > highest high of prior 30 bars | PASS |
| Bearish detection | Close < lowest low of prior 30 bars | PASS |
| Equality | Close = highest high or lowest low → NO EVENT | PASS |
| Reference window | Current bar excluded from prior-N-bar window | PASS |
| History requirement | Bars before N are insufficient for event detection | PASS |

The primary event detection correctly uses the N=30 completed-bar construction with strict inequality. The event bar itself is never included in its own reference window.

---

## 6. CROSS-MARKET SYNCHRONIZATION VALIDATION

| Aspect | Implementation | Result |
|--------|---------------|--------|
| Event bar counting | Event bar = bar E (not counted toward M) | PASS |
| Confirmation bar 1 | Bar E+1 | PASS |
| Confirmation bar 15 | Bar E+15 (final eligible) | PASS |
| Decision bar | Bar E+16 | PASS |
| Entry bar | Bar E+17 (open) | PASS |
| Timestamp alignment | Both markets aligned by bar open timestamp | PASS |

The 15-bar confirmation window is unambiguously defined:
- Event bar E is bar 0
- Confirmation bar 1 = E+1
- Confirmation bar 15 = E+15
- Decision = E+16
- Entry = E+17

---

## 7. CONFIRMATION EVENT VALIDATION

| Test | Description | Result |
|------|-------------|--------|
| Bullish confirmation | US500 close > its own 30-bar highest high | PASS |
| Bearish confirmation | US500 close < its own 30-bar lowest low | PASS |
| N-bar construction | Identical breakout logic applied to US500's own data | PASS |
| Completed bars only | Only completed bars checked | PASS |
| Strict inequality | Close must strictly exceed/penetrate | PASS |

The confirmation event uses the identical N-bar breakout construction applied to US500's own data, exactly as specified in the registration.

---

## 8. CONFIRMATION FAILURE TIMING

| Test | Description | Result |
|------|-------------|--------|
| Failure at bar 1 | US500 confirms on bar 1 → no failure | PASS |
| Failure at bar 15 | US500 confirms on bar 15 → no failure | PASS |
| No confirmation | US500 never confirms → failure after bar 15 | PASS |
| Early failure prevention | Failure not declared before bar 15 expires | PASS |

Failure is knowable only after the full 15-bar confirmation window has expired. No premature failure declaration.

---

## 9. INVALIDATION VALIDATION

| Test | Description | Result |
|------|-------------|--------|
| No reversal | Primary survives → opportunity proceeds | PASS |
| Reversal before M | Primary reverses before confirmation window ends → cancelled | PASS |
| Reversal after failure | Primary reverses after failure but before entry → cancelled | PASS |
| Reversal after entry | Primary reverses after entry → not applicable (already in position) | PASS |

Invalidation occurs when USATECHIDXUSD close returns within the N-bar range before entry. Only the registered timing affects cancellation.

---

## 10. DECISION MAPPING VALIDATION

| Test | Description | Result |
|------|-------------|--------|
| Bullish + failure | SHORT US500 | PASS |
| Bearish + failure | LONG US500 | PASS |
| Direction explicit | No "relative direction" ambiguity | PASS |
| Instrument explicit | Position always in US500 | PASS |

Decision mapping is deterministic and explicit. Bullish primary + failed confirmation → SHORT US500. Bearish primary + failed confirmation → LONG US500.

---

## 11. ENTRY TIMING VALIDATION

| Test | Description | Result |
|------|-------------|--------|
| Entry at bar E+17 | Open of bar after decision bar | PASS |
| Temporal causality | All information known before entry | PASS |
| No early entry | Entry does not occur before decision | PASS |
| No late entry | Entry is exactly at registered timing | PASS |

Entry timing: open of bar E+17 (the bar after the decision bar E+16). All information used for the decision is known before execution.

---

## 12. OPPORTUNITY POPULATION VALIDATION

| Test | Description | Result |
|------|-------------|--------|
| One per event | One opportunity per qualifying structural event | PASS |
| Duplicates excluded | Same-direction continuation without reversal = not new | PASS |
| Late events excluded | Events too late for M+2 bars excluded | PASS |
| Confirmed events excluded | Successfully confirmed events not counted | PASS |
| Invalidated events excluded | Cancelled events not counted | PASS |

Opportunity population is determined by the registered process, not by economic outcome.

---

## 13. SESSION/CALENDAR VALIDATION

| Test | Description | Result |
|------|-------------|--------|
| Session hours | 09:30–16:00 ET | PASS |
| Late event exclusion | Events with insufficient time for confirmation/entry excluded | PASS |
| Cross-session isolation | No cross-session confirmation | PASS |

Session boundary enforcement verified. Events in the last 17 bars of the session are excluded.

---

## 14. DATA-QUALITY VALIDATION

| Aspect | Registered Rule | Result |
|--------|----------------|--------|
| Missing primary bar | Skip (no imputation) | PASS |
| Missing confirmation bar | Skip (no imputation) | PASS |
| Duplicate timestamp | First occurrence used | PASS |
| Malformed bar (H<L, C=0) | Skip | PASS |
| Out-of-order data | Sort by timestamp | PASS |
| Proxy data | Not created; BLOCKED/INCOMPLETE | PASS |

---

## 15. LEAKAGE AUDIT

| Check | Result |
|-------|--------|
| Event bar excluded from N-bar reference | PASS |
| Confirmation bar 1 = E+1 (event bar not counted) | PASS |
| Decision at E+16, entry at E+17 | PASS |
| Primary event uses only past N bars | PASS |
| Confirmation uses only past N bars at each check | PASS |
| Invalidation check bounded between event and entry | PASS |
| Session boundary 09:30–16:00 ET enforced | PASS |

No leakage detected. Information from US500 cannot enter the primary event calculation. Information after confirmation bar 15 cannot alter whether failure occurred. Future session data cannot modify an earlier opportunity.

---

## 16. DETERMINISM

The primary implementation was run 5 times with identical inputs for Test D (bullish failure). All 5 runs produced identical outputs: same event identity, same event direction, same confirmation failure, same decision, same entry bar.

**Determinism: PASS**

---

## 17. INDEPENDENT REPRODUCIBILITY

A second, independently written implementation (`research/rf001_v38a_stage2_independent.py`) was created from the registration text. It was tested against 7 synthetic cases:

| Test | Result |
|------|--------|
| No event | PASS |
| Confirm on bar 1 | PASS |
| Confirm on bar 15 | PASS |
| Bullish failure → SHORT | PASS |
| Bearish failure → LONG | PASS |
| Exact entry bar | PASS |
| Determinism (5 runs) | PASS |

All 7 independent reproducibility tests pass. The independent implementation produces identical structural results.

**Independent reproducibility: PASS**

---

## 18. SYNTHETIC EDGE-CASE SUITE

| Test | Description | Result |
|------|-------------|--------|
| A | No primary event | PASS |
| B | Bullish primary, US500 confirms on bar 1 | PASS |
| C | Bullish primary, US500 confirms on bar 15 | PASS |
| D | Bullish primary, no US500 confirmation → SHORT | PASS |
| E | Bearish primary, no confirmation → LONG | PASS |
| F | Primary invalidated before M expires | PASS |
| G | Primary invalidated after failure before entry | PASS |
| H | Primary survives, failure, entry at exact bar | PASS |
| I | Duplicate same-direction breakout (continuation) | PASS |
| J | Event too late for confirmation/entry | PASS |
| K | Determinism (5 runs) | PASS |
| L | Leakage audit (7 checks) | PASS |
| M | Decision mapping exactness | PASS |
| N | Cost model consistency (no economic calculation) | PASS |

**14/14 tests passed.**

---

## 19. COST-MODEL CONSISTENCY

The registered 2 bps round-trip cost model is mechanically represented. No economic performance was calculated, computed, or inspected. No expectancy, P&L, win rate, Sharpe, drawdown, or profit factor was produced.

---

## 20. DISTINCTNESS

The implementation remains structurally distinct from all prior closed work:

| Prior work | Distinct? | Structural reason |
|------------|-----------|-------------------|
| F-02 (pairs spread) | YES | Confirmation failure, not spread trading |
| F-03 (rank rotation) | YES | Event detection, not ranking |
| Mean reversion | YES | Cross-market failure, not single-asset displacement |
| TSMOM | YES | Cross-market, not own-history trend |
| CAND-083 | YES | Cross-market, not single-market rejection |
| CAND-105 | YES | Failure detection, not lead-lag timing |
| ORB/Breakout | YES | Failure detection, not breakout trading |

No implementation drift detected. The process remains the registered Cross-Market Confirmation Failure Process.

---

## 21. DEVIATIONS / ISSUES

| Item | Status |
|------|--------|
| US500 M1 data | NOT AVAILABLE in repository. Production Stage 3 will require US500 M1 data from the forward MT5 pipeline. |
| Synthetic-only validation | All Stage 2 tests used synthetic data. This is by design — Stage 2 validates structure, not economics. |
| No deviations from registration | All frozen values implemented exactly as registered. |

---

## 22. FINAL STAGE 2 VERDICT

**STRUCTURALLY VALID**

The frozen RF-001 process is:
- Deterministic
- Temporally causal
- Correctly synchronized across markets
- Independently reproducible
- Free of look-ahead
- Structurally faithful to the frozen opportunity population
- Mechanically consistent with the registered execution model

Stage 3 Economic Validation is AUTHORIZED.

---

## 23. ECONOMIC FIREWALL CERTIFICATION

- **Economic validation performed:** NO
- **Backtesting:** NO
- **Returns computed:** NO
- **Profitability inspected:** NO
- **FB-001 economics inspected:** NO
- **F-01 economics inspected:** NO
- **Protected-forward economics inspected:** NO
- **Optimization performed:** NO
- **Historical economics used:** NO

---

**END OF STAGE 2 STRUCTURAL VALIDATION**
