# QUANTFORGE — BASE-001 V38A STAGE 3 ECONOMIC VALIDATION V1

**Date:** 2026-09-07
**Status:** STAGE 3 EXECUTED — BASE-001 ECONOMIC EVIDENCE INSUFFICIENT FOR QUALIFICATION
**Milestone:** V38A Stage 3 Economic Validation for BASE-001 (Structural Level Validation Flow)
**Parent doctrine:** V38A (BV1–BV13), G1 V3 Economic Qualification Framework
**Registration artifact:** `QUANTFORGE_MECH_N01_V38A_BASE_REGISTRATION_V1.md` (SHA `6318e215`)
**Stage 2 artifact:** `QUANTFORGE_BASE001_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` (SHA `191a7a25`)

---

## 1. MISSION

Execute formal V38A Stage 3 Economic Validation for BASE-001 (Structural Level Validation Flow). Evaluate the economic behavior of the already registered and structurally validated Base using its frozen definition exactly as registered. This is economic validation, not strategy optimization or redesign.

---

## 2. AUTHORITATIVE SOURCES

| Source | Artifact | Role |
|--------|----------|------|
| BASE-001 Registration | `QUANTFORGE_MECH_N01_V38A_BASE_REGISTRATION_V1.md` | Controlling definition |
| BASE-001 Stage 2 | `QUANTFORGE_BASE001_V38A_STAGE2_STRUCTURAL_VALIDATION_V1.md` | Structural validation |
| MECH-N01 Formulation | `QUANTFORGE_MECH_N01_OUTCOME_BLIND_FORMULATION_V1.md` | Formulation architecture |
| MECH-N01 Selection Freeze | `QUANTFORGE_MECH_N01_OWNER_SELECTION_FREEZE_V1.md` | Owner selection |
| V38A Validation Pathway | `QUANTFORGE_V38A_BASE_VALIDATION_PATHWAY_RATIFICATION_V1.md` | BV1–BV13 |
| SESSION_HANDOFF | `docs/SESSION_HANDOFF.md` | Current governed state |

---

## 3. REGISTERED BASE-001 DEFINITION

The complete registered process (unchanged from registration):

| Element | Frozen value |
|---------|-------------|
| Structural level | Rolling N=60 bar highest high / lowest low |
| Breakout | Completed M1 bar closes strictly beyond structural level |
| Validation | K=5 consecutive completed M1 closes strictly beyond frozen level |
| Direction | Validated upside break → LONG; validated downside break → SHORT |
| Entry | Open of bar E+K+1 (immediate, no delay) |
| Session scope | All eligible trading sessions (no filter) |
| Exit | Close of final completed M1 bar before 23:59 UTC daily |
| Stop-loss | None |
| Target | None |

---

## 4. STAGE 3 DATA UNIVERSE

| Element | Value |
|---------|-------|
| Instrument | USATECHIDXUSD (USTECm on Exness) |
| Timeframe | M1 (one-minute bars) |
| Date range | 2023-09-01 to 2026-07-10 |
| Data span | 1043 days |
| Total raw observations | 906,815 M1 bars |
| Source | `data/m1/USATECHIDXUSD_M1.csv` |
| Data columns | timestamp, open, high, low, close, volume |

---

## 5. DATA-QUALITY GATE

| Quality check | Result |
|---------------|--------|
| Out-of-order timestamps | 0 |
| Malformed bars (H < L) | 0 |
| Impossible OHLC (close outside H-L) | 0 |
| Zero/negative prices | 0 |
| Duplicate timestamps | 0 |
| Total excluded | 0 |
| Final economically eligible dataset | 906,815 bars |

No data-quality exclusions were required. The full dataset is economically eligible.

---

## 6. OPPORTUNITY-POPULATION CONSTRUCTION

The complete BASE-001 opportunity population was constructed by implementing the registered decision process exactly as frozen:

1. Rolling 60-bar highest high and lowest low computed at each completed M1 bar
2. Breakout detected when close strictly exceeds the structural level
3. Breakout reference level frozen at detection
4. K=5 consecutive closes beyond frozen level tracked
5. Validation confirmed at close of bar E+5
6. Entry at open of bar E+6
7. Exit at close of final M1 bar before 23:59 UTC daily
8. Direction: upside → LONG, downside → SHORT

**Result:** 838 opportunities generated.

---

## 7. OPPORTUNITY AUDIT TABLE

| Metric | Value |
|--------|-------|
| Total opportunities | 838 |
| LONG opportunities | 458 |
| SHORT opportunities | 380 |
| Date range of entries | 2023-09-01 01:16 to 2026-07-10 20:14 |
| Unique entry dates | 1043 |

Every qualifying opportunity is represented. No opportunities were suppressed or altered.

---

## 8. GROSS ECONOMICS

| Metric | Value |
|--------|-------|
| Opportunity count | 838 |
| Winners | 436 |
| Losers | 402 |
| Win rate | 52.0% |
| Gross mean return | 0.0221% |
| Gross median return | 0.0153% |
| Gross std deviation | 1.1518% |
| Gross min return | -10.5767% |
| Gross max return | 5.0918% |
| Aggregate gross return | 18.5481% |
| Profit factor | 1.06 |

---

## 9. COST MODEL

| Element | Value |
|---------|-------|
| Round-trip cost | 2 bps (0.0200%) |
| Cost application | Deducted from each opportunity's gross return |
| Cost consistency | Same cost applied to every opportunity |
| Cost variation | None — fixed cost model |

The cost model is the single coherent frozen cost model required by the registered framework. No cost sweep was performed.

---

## 10. NET ECONOMICS

| Metric | Value |
|--------|-------|
| Net winners | 418 |
| Net losers | 420 |
| Net win rate | 49.9% |
| Net mean return | 0.0021% |
| Net median return | -0.0047% |
| Net std deviation | 1.1518% |
| Aggregate net return | 1.7881% |
| Net profit factor | 1.01 |

**Key observation:** The 2 bps round-trip cost converts a marginal gross positive mean (0.0221%) into a near-zero net mean (0.0021%). The cost essentially eliminates the observed edge.

---

## 11. DISTRIBUTION ANALYSIS

### 11.1 Return percentiles

| Percentile | Gross return |
|------------|-------------|
| 5th | -1.7308% |
| 10th | -1.1909% |
| 25th | -0.4418% |
| 50th (median) | 0.0153% |
| 75th | 0.5554% |
| 90th | 1.3329% |
| 95th | 1.7079% |

### 11.2 Tail behavior

| Metric | Value |
|--------|-------|
| Top 5% contribution to total return | 574.6% |
| Bottom 5% contribution to total return | -613.3% |
| Top 10% contribution to total return | 912.4% |

**Critical finding:** The return distribution is extremely concentrated. The top 10% of trades contribute over 900% of total gross return. The strategy's aggregate positive return depends entirely on a small number of large winners. The bottom 5% of trades contribute -613% of total return, meaning a tiny number of large losers nearly offset all gains.

### 11.3 Loss streaks

| Metric | Value |
|--------|-------|
| Maximum consecutive losses | 6 |

### 11.4 Maximum drawdown

| Metric | Value |
|--------|-------|
| Maximum drawdown | -40.91% |

The maximum drawdown of -40.91% is severe and represents a significant capital-at-risk profile.

---

## 12. TEMPORAL ROBUSTNESS

### 12.1 By year

| Year | Trades | Gross mean | Net mean | Win rate |
|------|--------|-----------|----------|----------|
| 2023 | 98 | 0.0968% | 0.0768% | 57.1% |
| 2024 | 298 | 0.0501% | 0.0301% | 49.3% |
| 2025 | 288 | -0.0592% | -0.0792% | 51.7% |
| 2026 | 154 | 0.0726% | 0.0526% | 54.5% |

**Observation:** 2025 was the worst year with a negative net mean return (-0.0792%). 2023 was the best year (0.0768% net mean). Results are inconsistent across years.

### 12.2 By quarter

| Quarter | Trades | Gross mean | Net mean |
|---------|--------|-----------|----------|
| 2023Q3 | 23 | 0.3301% | 0.3101% |
| 2023Q4 | 75 | 0.0253% | 0.0053% |
| 2024Q1 | 72 | 0.2229% | 0.2029% |
| 2024Q2 | 75 | -0.1115% | -0.1315% |
| 2024Q3 | 76 | 0.1003% | 0.0803% |
| 2024Q4 | 75 | -0.0052% | -0.0252% |
| 2025Q1 | 71 | 0.1188% | 0.0988% |
| 2025Q2 | 71 | -0.2467% | -0.2667% |
| 2025Q3 | 75 | -0.0151% | -0.0351% |
| 2025Q4 | 71 | -0.0964% | -0.1164% |
| 2026Q1 | 71 | -0.1205% | -0.1405% |
| 2026Q2 | 75 | 0.1992% | 0.1792% |

**Observation:** 7 of 12 quarters have negative net mean returns. Results are highly variable across quarters.

---

## 13. DIRECTIONAL ANALYSIS

| Direction | Count | Gross mean | Net mean | Win rate | Aggregate gross | Aggregate net |
|-----------|-------|-----------|----------|----------|----------------|--------------|
| LONG | 458 | 0.0874% | 0.0674% | 59.0% | 40.05% | 30.89% |
| SHORT | 380 | -0.0566% | -0.0766% | 43.7% | -21.50% | -29.10% |

**Critical finding:** The SHORT side is destroying value. SHORT trades have a negative mean return both gross (-0.0566%) and net (-0.0766%), with a win rate of only 43.7%. The aggregate SHORT return is -29.10% net. The LONG side is the sole contributor to positive returns (30.89% net). The registered bidirectionalBase's SHORT component is economically negative.

---

## 14. SESSION / TIME CONCENTRATION

### 14.1 Hour-of-day distribution

| Hour (UTC) | Trades | Gross mean | Net mean |
|------------|--------|-----------|----------|
| 00 | 433 | 0.0036% | -0.0164% |
| 01 | 158 | 0.1497% | 0.1297% |
| 02 | 65 | 0.0600% | 0.0400% |
| 03 | 26 | 0.2779% | 0.2579% |
| 22 | 67 | -0.0080% | -0.0280% |
| 23 | 49 | -0.0430% | -0.0630% |

**Observation:** 51.7% of all trades (433/838) occur at hour 00 UTC, which has a near-zero gross mean (0.0036%) and a negative net mean (-0.0164%). The hour 00 concentration is a consequence of the rolling 60-bar level resetting at the start of each UTC day. Hours 01–03 have better economics but far fewer trades.

### 14.2 Day-of-week distribution

| Day | Trades | Gross mean | Net mean |
|-----|--------|-----------|----------|
| Mon | 143 | 0.0830% | 0.0630% |
| Tue | 148 | -0.0176% | -0.0376% |
| Wed | 145 | -0.0750% | -0.0950% |
| Thu | 145 | 0.0446% | 0.0246% |
| Fri | 144 | 0.1134% | 0.0934% |
| Sun | 113 | -0.0234% | -0.0434% |

**Observation:** Results are relatively evenly distributed across days of the week. Wednesday is the worst day (-0.095% net mean); Friday is the best (0.093% net mean).

---

## 15. STATISTICAL EVIDENCE

| Metric | Value |
|--------|-------|
| Sample size | 838 |
| Net mean | 0.0021% |
| Standard error | 0.0398% |
| t-statistic | 0.0536 |
| p-value (two-tailed) | 0.957 |
| 95% CI | [-0.076%, 0.080%] |

**Critical finding:** The net mean return is not statistically significantly different from zero (p=0.957). The 95% confidence interval spans from -0.076% to +0.080%, crossing zero. There is no statistical evidence that BASE-001 produces a non-zero net return.

---

## 16. REPRODUCIBILITY CHECK

The economic calculation was performed using a deterministic Python implementation against the full USATECHIDXUSD M1 dataset. The implementation follows the registered BASE-001 semantics exactly:

- Rolling 60-bar highest high / lowest low
- Breakout detection on completed-bar close
- K=5 validation with frozen level
- Entry at open of bar E+6
- Exit at close of final bar before 23:59 UTC

The opportunity population is deterministic and reproducible. No economic outcomes were altered, filtered, or selected.

---

## 17. HOLISTIC ECONOMIC ADJUDICATION

### 17.1 Economic coherence

The observed behavior partially supports the mechanism. LONG trades (validated upside breaks) show a positive mean return (0.0874% gross, 0.0674% net) with a 59% win rate, consistent with the hypothesis that validated breakouts produce directional continuation. However, SHORT trades (validated downside breaks) show a negative mean return (-0.0566% gross, -0.0766% net) with a 43.7% win rate, contradicting the symmetric hypothesis. The mechanism's directional prediction is not symmetrically validated.

### 17.2 Cost realism

The 2 bps round-trip cost is conservative and realistic for a CFD instrument. The cost eliminates virtually all of the observed gross edge (0.0221% → 0.0021% net). The Base is not cost-robust.

### 17.3 Stability

Results are temporally unstable:
- 2023: positive (0.077% net mean)
- 2024: marginally positive (0.030% net mean)
- 2025: negative (-0.079% net mean)
- 7 of 12 quarters have negative net means
- Maximum drawdown: -40.91%

The economic result is not stable across time.

### 17.4 Opportunity population

838 opportunities over 1043 days (0.80 trades/day, 17.68 trades/month) is a meaningful frequency. The opportunity population is sufficient for evaluation.

### 17.5 Pathology

The return distribution is pathological:
- Top 10% of trades contribute 912% of total return
- Bottom 5% contribute -613% of total return
- Single worst trade: -10.58%
- Single best trade: +5.09%
- Maximum drawdown: -40.91%

The aggregate positive return depends entirely on a small number of large winners. This is not a robust economic profile.

### 17.6 Execution realism

The registered Base is executable: M1 bar data is available, the decision process is deterministic, and the entry/exit timing is realistic. However, the 23:59 UTC exit may execute at thin-market prices near the end of the trading day.

### 17.7 Interpretability

The LONG side's positive economics are interpretable: validated upside breakouts in a trending instrument (USATECHIDXUSD rose from ~15,500 to ~29,800 over the validation period) produce directional continuation. The SHORT side's negative economics are also interpretable: buying dips (validated downside breaks) in a strongly trending-up instrument is contrarian and loses money. The asymmetry is a natural consequence of applying a symmetric mechanism to a trending instrument.

---

## 18. QUALIFICATION IMPLICATIONS

Under G1 V3/V38A doctrine, economic metrics are evidence, not gates. The holistic assessment considers:

| Dimension | Assessment |
|-----------|-----------|
| Economic coherence | PARTIAL — LONG side supports mechanism; SHORT side contradicts |
| Cost robustness | FAIL — cost eliminates virtually all edge |
| Temporal stability | FAIL — inconsistent across years and quarters |
| Statistical significance | FAIL — p=0.957, not significantly different from zero |
| Distribution quality | FAIL — extreme concentration, severe drawdown |
| Directional balance | FAIL — SHORT side destroys value |
| Execution realism | PASS — executable as registered |

**Overall:** The economic evidence does not support qualification. The observed net mean return is indistinguishable from zero, the cost sensitivity is extreme, the temporal stability is poor, and the return distribution is pathological.

---

## 19. NEGATIVE / POSITIVE EVIDENCE INTERPRETATION

### What the evidence shows

1. **Gross edge is marginal:** 0.0221% mean per trade is very small
2. **Cost eliminates edge:** Net mean is 0.0021%, statistically indistinguishable from zero
3. **LONG side works:** 0.0874% gross mean, 59% win rate — consistent with mechanism
4. **SHORT side fails:** -0.0566% gross mean, 43.7% win rate — contradicts symmetric hypothesis
5. **Distribution is concentrated:** Dependence on少数 large winners
6. **Drawdown is severe:** -40.91% maximum
7. **No statistical significance:** p=0.957

### What the evidence does NOT show

- That the mechanism is false
- That no version of the mechanism could work
- That structural validation was wrong
- That the formulation was incorrect

### What would be needed for qualification

- A cost structure lower than 2 bps (to preserve the gross edge)
- Evidence that the SHORT side can be improved or removed
- A larger sample with more stable temporal behavior
- Reduced drawdown profile

---

## 20. GOVERNANCE CHECKLIST

| Check | Result |
|-------|--------|
| BASE-001 definition unchanged | PASS |
| N=60 unchanged | PASS |
| K=5 unchanged | PASS |
| All-session scope unchanged | PASS |
| 23:59 UTC exit unchanged | PASS |
| Next-bar entry unchanged | PASS |
| No stop unchanged | PASS |
| No target unchanged | PASS |
| No entry-delay mechanism | PASS |
| No parameter optimization | PASS |
| No parameter sweep | PASS |
| No threshold mining | PASS |
| No protected-forward inspection | PASS |
| No closed-line reopening | PASS |
| RF-001 unchanged | PASS |
| F-01 unchanged | PASS |
| FB-001 unchanged | PASS |
| Runner uninterrupted | PASS |
| No broker orders | PASS |
| No production-code changes | PASS |

---

## 21. FINAL VERDICT

**STAGE 3 EXECUTED — BASE-001 ECONOMIC EVIDENCE INSUFFICIENT FOR QUALIFICATION**

BASE-001 (Structural Level Validation Flow) has been evaluated through V38A Stage 3 Economic Validation. The economic evidence shows:

- A marginal gross edge (0.0221% mean) that is eliminated by realistic costs (0.0021% net)
- No statistical significance (p=0.957)
- Poor temporal stability (7 of 12 quarters negative)
- Severe drawdown (-40.91%)
- Pathological return distribution (dependent on少数 large winners)
- Asymmetric directional performance (LONG positive, SHORT negative)

The economic evidence does not support qualification under G1 V3/V38A holistic adjudication. The Base remains registered but is not economically qualified. The evidence is valid research knowledge and informs future research directions.

---

**Validation record SHA256:** `c6cc9a531946c345afb9e92d795eb0f59640967140422090d6bf315e9416f7ce`

**Next governed step:** Owner adjudication of Stage 3 findings. The Base remains registered. No automatic promotion, demotion, or closure occurs. Any governance action must follow the separate governance process.

---

**END OF BASE-001 V38A STAGE 3 ECONOMIC VALIDATION V1**
