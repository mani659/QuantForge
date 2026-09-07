# QUANTFORGE — TSMOM V1 CONTROLLED EXPERIMENT — SCIENTIFIC REPORT

**Protocol:** EVENT_STUDY_PROTOCOL_TSMOM_V1.md v1.0.3 (frozen) — executed 2026-08-12T13:27:43.894847Z
**Elapsed:** 3.5 s

## 1. Scientific Classification
**INCONCLUSIVE**

## 2. Economic Classification
**NOT CONFIRMED**

## 3. Sample

| Market | N usable | Assessments span |
|---|---|---|
| XAUUSD | 48 | 2022-05..2026-04 |
| EURUSD | 53 | 2022-02..2026-06 |
| BTCUSD | 48 | 2022-06..2026-05 |
| XAGUSD | 48 | 2022-08..2026-07 |
| USATECHIDXUSD | 22 | 2024-10..2026-07 |
| **Pooled** | **219** | |

Pooled calendar months: 54 (T_F1 = 50, T_TEST = 11)
Pooled usable assessments: 219; pooled sign flips: 21.

## 4. Primary F1 Result (TRAIN+VALIDATION, first 85%)

| Series | Mean/month | 95% CI | one-sided p | T | blocks |
|---|---|---|---|---|---|
| F1 gross | 0.0151 | [-0.0253, 0.0454] | 0.2375 | 50 | 39 |
| F1 net | 0.0148 | [-0.0258, 0.0452] | 0.2436 | 50 | 39 |

## 5. Protected F2 Result (TEST, final 15%, single use)

Pooled TEST mean (gross): 0.0670; sign: 1; exact sign-flip one-sided p: 0.1274 (T = 11, 2048 assignments).
Pooled TEST mean (net): 0.0668; sign: 1; exact sign-flip one-sided p: 0.1274.

## 6. Holm Multiple-Comparison Control (family {F1, F2}, alpha 0.05)

Gross: F1 raw p 0.2375 -> Holm 0.2549; F2 raw p 0.1274 -> Holm 0.2549.
Net:   F1 raw p 0.2436 -> Holm 0.2549; F2 raw p 0.1274 -> Holm 0.2549.

## 7. Per-Market Results (full sample)

| Market | N | L/S | mean r | net mean | hit | ann mean | Sharpe | mean cost/mo | break-even bp |
|---|---|---|---|---|---|---|---|---|---|
| XAUUSD | 48 | 40/8 | 0.0609 | 0.0606 | 64.58% | 0.7307 | 1.1666 | 0.0003 | 345.1410 |
| EURUSD | 53 | 27/26 | -0.0203 | -0.0204 | 45.28% | -0.2440 | -0.5697 | 0.0000 | -66.0967 |
| BTCUSD | 48 | 31/17 | 0.0186 | 0.0182 | 54.17% | 0.2237 | 0.3425 | 0.0005 | 365.0162 |
| XAGUSD | 48 | 39/9 | 0.0174 | 0.0169 | 47.92% | 0.2090 | 0.3667 | 0.0005 | 220.2207 |
| USATECHIDXUSD | 22 | 22/0 | 0.0514 | 0.0514 | 59.09% | 0.6170 | 1.4018 | 0.0000 | 450.9665 |

## 8. Pooled / Portfolio

Full-sample pooled gross mean: 0.0192 (ann. 0.2300); months 54.
Portfolio gross: ann mean 0.2300, Sharpe 0.6896, max DD -0.6112, hit 55.56%, equity end 2.2037.
Portfolio net:   ann mean 0.2264, Sharpe 0.6785, max DD -0.6153, hit 55.56%, equity end 2.1684.

## 9. Transaction Costs

Observed pooled median one-way half-spread (4 bid/ask markets): 3.2430 bp. Bid/ask cost-match coverage: 100.00% (166/166 legs).
EURUSD spread: UNOBSERVED — registered 0.1 bp/side ASSUMPTION (band E10).

## 10. Break-Even

Pooled break-even one-way cost h*: 140.4061 bp.
- XAUUSD: h* = 345.1410 bp (V = 84.68 units traded).
- EURUSD: h* = -66.0967 bp (V = 163.01 units traded).
- BTCUSD: h* = 365.0162 bp (V = 24.51 units traded).
- XAGUSD: h* = 220.2207 bp (V = 37.97 units traded).
- USATECHIDXUSD: h* = 450.9665 bp (V = 25.08 units traded).

## 11. Negative Controls

NC1 (run-shuffle, diagnostic only, 1000 shuffles): null mean 0.0256, P95 0.0256, fraction >= observed 1.0000.
NC2 (6-month time-shift, formal control): mean 0.0393, CI [0.006865832604733523, 0.07450526726821485], T = 48.

## 12. Crash Diagnostics (descriptive only)

| State | n | mean r |
|---|---|---|
| BEAR&PANIC | 0 | None |
| BEAR only | 15 | -0.0167 |
| PANIC only | 23 | 0.0434 |
| neither | 181 | 0.0219 |

## 13. Walk-Forward / Temporal Stability (descriptive)

| Fold | n | mean | 95% CI | sign |
|---|---|---|---|---|
| XAUUSD:fold1 | 12 | -0.0086 | [-0.008597368941876576, -0.008597368941876576] | -1 |
| XAUUSD:fold2 | 12 | 0.0639 | [0.06392224502512646, 0.06392224502512646] | 1 |
| XAUUSD:fold3 | 12 | 0.0922 | [0.09222533913669283, 0.09222533913669283] | 1 |
| XAUUSD:fold4 | 12 | 0.0960 | [0.09601397805989688, 0.09601397805989688] | 1 |
| EURUSD:fold1 | 13 | 0.0231 | [0.012299501373649973, 0.02788470508234553] | 1 |
| EURUSD:fold2 | 13 | -0.0205 | [-0.029423663621296312, -0.01576039620621799] | -1 |
| EURUSD:fold3 | 13 | -0.0811 | [-0.09649575096702914, -0.05722807970752761] | -1 |
| EURUSD:fold4 | 14 | -0.0041 | [-0.02207766578349915, 0.025012095278335044] | -1 |
| BTCUSD:fold1 | 12 | -0.0590 | [-0.059015942861848365, -0.059015942861848365] | -1 |
| BTCUSD:fold2 | 12 | 0.0777 | [0.07770156605454893, 0.07770156605454893] | 1 |
| BTCUSD:fold3 | 12 | 0.0600 | [0.060045951979477624, 0.060045951979477624] | 1 |
| BTCUSD:fold4 | 12 | -0.0042 | [-0.00417925204813734, -0.00417925204813734] | -1 |
| XAGUSD:fold1 | 12 | -0.0895 | [-0.08948308772797729, -0.08948308772797729] | -1 |
| XAGUSD:fold2 | 12 | 0.0144 | [0.014391816445449956, 0.014391816445449956] | 1 |
| XAGUSD:fold3 | 12 | 0.0468 | [0.046794388770334615, 0.046794388770334615] | 1 |
| XAGUSD:fold4 | 12 | 0.0980 | [0.09797143651261288, 0.09797143651261288] | 1 |
| USATECHIDXUSD:fold1 | 5 | 0.0253 | [-0.030763984577378296, 0.09542805155194214] | 1 |
| USATECHIDXUSD:fold2 | 6 | 0.0320 | [-0.06867402030608122, 0.0989929337323282] | 1 |
| USATECHIDXUSD:fold3 | 5 | 0.0968 | [-0.012100646223858738, 0.22772005079934945] | 1 |
| USATECHIDXUSD:fold4 | 6 | 0.0547 | [-0.057121782635853234, 0.17837671261071306] | 1 |

Pooled chronological thirds:
- POOLED:third1: n = 72, mean = -0.0301
- POOLED:third2: n = 73, mean = 0.0516
- POOLED:third3: n = 74, mean = 0.0420

## 14. Exploratory Sensitivities (EXPLORATORY — NON-CONFIRMATORY)

| Sensitivity | n assessments | pooled mean |
|---|---|---|
| E1_LB6 | 249 | 0.0081 |
| E2_LB24 | 159 | 0.0209 |
| E3_H3 | 68 | 0.0782 |
| E4_flat | 219 | 0.0076 |
| E6_hurdle | 219 | 0.0185 |
| E7_noUSATECH | 197 | 0.0173 |
| E9_capped | 219 | 0.0143 |

Net-sensitivity bands (full sample):

| Component | bp/side | pooled net mean |
|---|---|---|
| commission | 0.0 | 0.0212 |
| commission | 0.5 | 0.0211 |
| commission | 1.0 | 0.0210 |
| commission | 2.0 | 0.0209 |
| EURUSD_assumed_spread | 0.1 | 0.0212 |
| EURUSD_assumed_spread | 0.5 | 0.0212 |
| EURUSD_assumed_spread | 1.0 | 0.0211 |
| EURUSD_assumed_spread | 2.0 | 0.0211 |

## 15. Market Correlation (aligned months, direction-adjusted)

| Pair | rho |
|---|---|
| XAUUSD|EURUSD | 0.0826 |
| XAUUSD|BTCUSD | 0.1563 |
| XAUUSD|XAGUSD | 0.4525 |
| XAUUSD|USATECHIDXUSD | -0.0176 |
| EURUSD|BTCUSD | -0.1871 |
| EURUSD|XAGUSD | 0.3040 |
| EURUSD|USATECHIDXUSD | 0.1625 |
| BTCUSD|XAGUSD | 0.0537 |
| BTCUSD|USATECHIDXUSD | 0.1007 |
| XAGUSD|USATECHIDXUSD | 0.0624 |

## 16. Unresolved Triggers / Gate

pooled flips = 21 (<15 -> UNRESOLVED); bid/ask cost coverage = 100.00%; pooled usable assessments = 219 (<30 -> UNRESOLVED). Triggered: False.
F1 gross confirmed (CI lower > 0): False. Net viable (F1 net CI>0 & F2 net>0 & h*>median & net>0 @1bp): False.

## 17. Reproducibility

- Protocol SHA-256: `2d60cb7158dbce6e0e31df2305f506b909be7a431c9ee83002de4518d00292c5`
- data/m1/XAUUSD_M1.csv: `54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c`
- data/tick/XAUUSD_mt5_ticks.csv: `637087df5cbe13a3c5c270c32b115691e7c7e53a4f9a92ac51fb78b35bfbd82e`
- data/m1/EURUSD_M1.csv: `5106a518e65a9d3f4c8bfc74c14fad81240a9de278bd1c4577799a6f1b79813f`
- data/tick/EURUSD_mt5_ticks.csv: `75225d0404fd97b39cb5ffe333a898e6a7e450616df7e6733bf9ec2dc916fc24`
- data/m1/BTCUSD_M1.csv: `97b853854d8f650d80e3972f159deab0b15911e19dd437e1dd10b3bab098409b`
- data/tick/BTCUSD_mt5_ticks.csv: `811fd055fcf33f14c6315f0e7625fd98c60b2184439188e8fcac783e72914014`
- data/m1/XAGUSD_M1.csv: `69444be954a869ebc831cd1253849222d8babc7a02940b2bb908a5179bcf5999`
- data/tick/XAGUSD_mt5_ticks.csv: `edccad88ed5b74caf16a14203f3cf743306c65f2ebc5004cf566ed61deeb6e17`
- data/m1/USATECHIDXUSD_M1.csv: `39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6`
- data/tick/USATECHIDXUSD_mt5_ticks.csv: `56105bda21aa88270f77c2bc26afabca4e6e37095ac2ec45ccc40764781841ba`
- python: 3.11.9 (tags/v3.11.9:de54cf5,; numpy: 2.4.4
- seed F1 = 20260812, B = 10000, L = 12; seed NC1 = 20260813
- Cost convention: 1 bp = 0.0001; Option A net series `pi_net_m = mean_i(p*R - |dp|*h)` with final-close term.

---
*Research evidence only. No BOE/runtime semantics are created by this experiment.*