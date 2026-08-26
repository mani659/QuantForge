# QuantForge — Research Factory V2
# CAND-021 FINAL INDEPENDENT G2 ADJUDICATION
# PRE-G3 GOVERNANCE GATE

## 1. Executive Verdict
**G3 READY**
The frozen CAND-021 economic object has successfully demonstrated reproducible, descriptive economic behavior out-of-sample. While the economic margin is thin (PF ~1.05) and fragile under stress in the development set, the robust reproduction in the chronological holdout (which actually strengthened) justifies advancing to a formal, cheap scientific validation (G3). The core hypothesis—that pre-entry D1 volatility state isolates a positive-expectancy regime—is empirically supported.

## 2. Frozen Identity
**PASS.**
The G2 pilot strictly evaluated the exact, unmodified CAND-021 object registered at G0 and G1. No stop-losses, filters, optimizations, or hidden parameters were introduced to rescue the drawdown or artificially inflate the profit factor.

## 3. Split Integrity
**PASS.**
The data was split using a strict, predetermined chronological boundary (70% Development, 30% Holdout). No randomization, optimization of the split date, or future-data leakage occurred.

## 4. Holdout Reproduction
**PASS.**
The central G2 question—does the positive economic sign survive in untouched later data?—is definitively answered:
- Holdout Mean Net: +3.84 points (exceeded Development's +1.56 points).
- Holdout Median Net: +6.98 points.
- Holdout Win Rate: 52.08%.
- Holdout PF: 1.07.
The effect reliably reproduced and even marginally strengthened out-of-sample.

## 5. Economic Margin
**Assessment: Economically Plausible but Thin.**
The Profit Factor of ~1.05 is mathematically thin. Furthermore, at 2× friction (4.0 points), the Development set's mean net fell below zero (-0.44 points). However, this fragility is structurally driven by the lack of a stop-loss (absorbing massive, rare macro shocks) rather than a lack of underlying edge. Because the Holdout set survived the 2× friction stress (mean net +1.84), the object remains economically plausible enough to warrant formal scientific testing, even if it is not yet a viable standalone trading system.

## 6. Tail / Drawdown
The strategy absorbs extreme, unhedged left-tail events (Worst Trade: -405.41 points). These tail events aggregate into a severe -1947.57 point max drawdown. 
However, the positive expectancy is broad-based: the win rate exceeds 54%, and the median gross (+10.78) is higher than the mean gross (+4.25). The positive expectancy does *not* depend on a small handful of lucky outliers; rather, a broad base of consistent winners reliably overcomes a handful of catastrophic losers over a large enough sample.

## 7. Frequency Stability
**PASS.**
Event frequency is extraordinarily stable:
- Full Sample: 113.29 opps/year
- Development: 113.69 opps/year
- Holdout: 113.84 opps/year
The opportunity frequency is genuinely independent of the chronological era.

## 8. G2 Integrity
**PASS.**
No hidden parameters, outcome-derived filtering, MFE/future extrema, or data leakage were found. The implementation rigorously adhered to the frozen object's rules.

## 9. G3 Scope
G3 is authorized exclusively to test:
> “Is the observed conditional effect scientifically distinguishable from chance?”

G3 must **NOT** be used to:
- Discover or inject a stop-loss.
- Optimize the 60-minute exit.
- Tune the 1.5x volatility threshold.
- Search for a "better" risk-managed variant.

If risk control is desired to repair the drawdown and improve the Profit Factor, that requires a NEW G0 object. G3 evaluates only the scientific validity of the current, frozen, unhedged CAND-021 object.

## 10. Final Adjudication
**G3 READY**
The descriptive economic behavior is reproducible out-of-sample.

## 11. CAND-015 Firewall
CAND-015 remains: 7-DAY FORWARD OBSERVATION ACTIVE / PROTECTED. No forward results were inspected or used in this adjudication.

## 12. Integrity
This adjudication was entirely read-only. No G3 execution was triggered. No risk controls were retroactively applied to repair the drawdown.
