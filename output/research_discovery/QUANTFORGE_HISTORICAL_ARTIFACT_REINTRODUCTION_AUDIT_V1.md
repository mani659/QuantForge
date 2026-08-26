# QUANTFORGE — HISTORICAL ARTIFACT REINTRODUCTION AUDIT V1
# READ-ONLY HISTORICAL SCAN
# DATE: 2026-08-26

## 1. Purpose
To perform a comprehensive retrospective read-only reassessment of historical QuantForge research artifacts under the newly adopted **Artifact vs Strategy System Governance V1**. The objective is to identify scientifically credible and economically interesting behavioral artifacts that were previously rejected solely because they failed to qualify as high-frequency standalone trading systems, and to designate them as COMPONENT-CANDIDATES for future System Assembly.

## 2. Governance Context
Under Research Factory V2 Governance Amendment (Artifact vs System), low standalone frequency is NO LONGER an automatic kill condition. Artifacts with strong per-event economics but low frequency are retained as `COMPONENT-CANDIDATES`. Combination in a system cannot be used to rescue negative-expectancy or contradicted artifacts.

## 3. Artifact vs Strategy Distinction
- **Research Artifact:** A validated conditional behavioral phenomenon with positive per-event economics.
- **Strategy System:** An assembled portfolio of artifacts that provides sufficient frequency, capital utilization, and execution logic for standalone deployment.

## 4. Historical Research Scope
The audit examined registered candidates CAND-018 through CAND-027, and canonical discovery tracks DISC-021 through DISC-026, relying purely on persisted historical evidence and adjudications. No experiments were rerun.

## 5. Artifact Evidence Table

| Object | Mechanism | Scientific Status | Economic Status | Frequency | Primary Failure Reason | Per-Event Economics | Component Eligibility | Reason |
|---|---|---|---|---:|---|---|---|---|
| DISC-021 | Mean Reversion (XAGUSD) | Supported | Non-Viable | High | Bid/ask consumes gross | Negative net | E | Non-viable at artifact level |
| DISC-022 | 12/1 TSMOM | Contradicted | Unresolved | Medium | Cross-era inconsistency | N/A | D | Contradicted in contemporary era |
| DISC-023 | H01 Volatility Asymmetry | Supported | Non-Viable | Medium | Hist. translation failed | Negative net (Hist) | E | Translation non-viable |
| DISC-024 | Session Range Expansion | Contradicted | N/A | N/A | Falsified | N/A | D | Statistically Contradicted |
| DISC-025 | Liquidity Sweep / Reversal | Supported | Non-Viable | Medium | Translation gross-negative | Negative gross | E | Non-viable at artifact level |
| DISC-026 | ORD (XAGUSD) | Supported | Non-Viable | High | Translation non-viable | Negative net | E | Non-viable at artifact level |
| CAND-018 | Trend-Pullback Re-Accel | N/A | Non-Viable | High | Severe left tail | Negative mean net | E | Negative expectancy |
| CAND-019 | Fixed Income Benchmark | N/A | Blocked | N/A | Missing Data | N/A | F | Inconclusive |
| CAND-020 | V7 Screen | N/A | Insufficient | N/A | Killed at G1 | Negative | E | Non-viable |
| CAND-021 | Pre-Auction Liq Vacuum | Contradicted | Positive (G1) | 111.0/yr | G3 Contradiction | +2.25 net | D | Scientifically contradicted |
| CAND-022 | Euro Close Reversal | N/A | Blocked | N/A | Missing Data | N/A | F | Inconclusive |
| CAND-023 | London Open Momentum | N/A | Insufficient | 157.8/yr | Microscopic magnitude | -0.27 net | E | Non-viable at artifact level |
| CAND-024 | Friday De-Risking | N/A | Positive | 4.55/yr | Low standalone frequency | +40.59 net | A | High expectancy, failed on freq |
| CAND-025 | Macro Shock Liq Void | N/A | Marginal | 55.0/yr | Fragile economics vs tail | +1.25 net | B | Interesting but fragile |
| CAND-026 | US Open IB Trap | N/A | Insufficient | N/A | Negative G1 | Negative net | E | Non-viable at artifact level |
| CAND-027 | Intraday Trend Unwind | N/A | Insufficient | Low | Negative G1 | Negative net | E | Non-viable at artifact level |

## 6. Candidate-by-Candidate Assessment

### Required Artifact-Level Questions:
1. **What was the actual behavioral claim?** Outlined in table.
2. **Was the event formally defined?** Yes, for all listed objects.
3. **Was executable capture valid?** Yes, strictly enforced in V2 (CAND-018+).
4. **Was there any look-ahead / MFE / implementation defect?** Addressed and corrected prior to these final verdicts.
5. **Did the artifact show positive per-event economics?** Only CAND-021, CAND-024, CAND-025.
6. **Did it fail because of frequency/utilization?** CAND-024.
7. **Did it fail because of negative expectancy?** DISC-021, DISC-023, DISC-025, DISC-026, CAND-018, CAND-023, CAND-026, CAND-027.
8. **Did it fail scientifically?** DISC-022, DISC-024, CAND-021.
9. **Could it theoretically complement another independent artifact?** CAND-024, CAND-025.
10. **Would considering it as a component constitute a rescue?** No for CAND-024/025. Yes for all others.

## 7. Potential Component Artifacts
See LIST A below.

## 8. Rejected Artifacts
See LIST C below.

## 9. Scientific Contradictions
DISC-022, DISC-024, CAND-021.

## 10. Economic Non-Viability
DISC-021, DISC-023, DISC-025, DISC-026, CAND-018, CAND-023, CAND-026, CAND-027.

## 11. Low-Frequency Artifacts
CAND-024 (4.55/year).

## 12. System-Assembly Candidates
CAND-024 (Component-Eligible).

## 13. Rescue Firewall
No failed artifacts were rescued. Negative expectancy and scientific contradiction remain absolute kill conditions.

## 14. Final Recommendations
Retain CAND-024 for future System Assembly. Leave all other lines formally closed.

## 15. Integrity
No experiments were rerun. No new parameters were searched. All findings are derived strictly from persisted historical evidence.

---

# FINAL ARTIFACT LISTS

## LIST A — POTENTIALLY REINTRODUCIBLE COMPONENT ARTIFACTS
**CAND-024: Friday De-Risking Conditioned by Morning Exhaustion**
- **Evidence:** Mean Net: +40.59 pts, Median Net: +34.00 pts, Win Rate: 61.54%, Frequency: ~4.55/year.
- **Why it qualifies:** Excellent per-event expectancy and gross magnitude. Failed G1 solely because 4.5 opportunities per year is mathematically insufficient for a standalone intraday strategy.
- **Intended Component Role:** Event Opportunist / Session Component. (High-value, rare event that provides uncorrelated positive expected value).

## LIST B — RETAINED BUT NOT QUALIFIED
**CAND-025: Macro Shock Liquidity Void Reversal**
- **Evidence:** Mean Net: +1.25, Median Net: +2.64, Frequency: ~55.0/year.
- **Reasoning:** Interesting evidence, but the massive standard deviation (~50 pts) makes the thin mean net too fragile for independent qualification. Retained for visibility as a potential tail/risk component, but requires further structural resolution before it can be considered qualified.

## LIST C — PERMANENTLY CLOSED
- **DISC-021 (XAGUSD Reversal):** Economically non-viable (costs consume gross).
- **DISC-022 (TSMOM):** Scientifically contradicted (cross-era).
- **DISC-023 (H01 Equity):** Economically non-viable (historical translation failure).
- **DISC-024 (Session Range Expansion):** Scientifically contradicted.
- **DISC-025 (Liquidity Sweep):** Economically non-viable (translation gross-negative).
- **DISC-026 (ORD XAGUSD):** Economically non-viable.
- **CAND-018:** Economically non-viable (severe left tail / negative net).
- **CAND-019 & CAND-022:** Invalid/Inconclusive (missing data).
- **CAND-020, CAND-023, CAND-026, CAND-027:** Economically non-viable (negative or microscopic net).
- **CAND-021:** Scientifically contradicted in G3.
