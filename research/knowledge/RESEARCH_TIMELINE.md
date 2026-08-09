# QuantForge Research Timeline

This timeline is organized by scientific progression rather than file dates.

## 1. Initial behavioral mean-reversion hypothesis

Research began with the proposition that unusually deep short-term displacement might reverse asymmetrically. The early factor set was z-score depth, momentum exhaustion, ATR/volatility and session timing.

**Knowledge retained:** extreme displacement is the candidate event, not a standalone trading rule.

## 2. Factor isolation and confluence

Separate studies examined depth, volatility, momentum and time-of-day, then combined them. The journals report that deeper extremes, high volatility, panic momentum and favorable sessions improved selected outcomes while reducing frequency.

**Scientific transition:** from indicator conditions to a behavioral-dislocation hypothesis.

## 3. Exit architecture experiments

Fixed, ATR-based, trailing, breakeven, partial and time-based exit concepts were evaluated. Quick snap/adaptive exits were retained; trailing/runners were de-emphasized.

**Scientific transition:** the edge was characterized as a fast response, not a trend-capture system.

## 4. Virtual signal architecture

The project separated observation of a panic condition from permission to enter. A virtual candidate had to prove recovery before becoming a real entry.

**Scientific transition:** fewer trades in exchange for quality control.

## 5. Recoil discovery

Forensic work (`entry_forensics.py`, `tick_entry_forensics.py`, `recoil_profile_analysis.csv`) focused on what happens immediately after the event. Strong winners show positive early recoil; scratch events do not.

**Scientific transition:** recoil became an observable confirmation variable.

## 6. Persistence discovery

Recoil alone was found insufficient. The research added a requirement that price hold after recovery. Expansion outputs retain separate recoil and persistence failure counts.

**Scientific transition:** two-stage confirmation: recoil, then stabilization.

## 7. Controlled recovery, basket and MAE/MFE forensics

Scripts reconstructed EA trades, grouped baskets/clusters, examined spacing, depth, lot progression, MAE/MFE and catastrophic clusters. This exposed concentration/tail-risk properties alongside high average cluster profitability.

**Scientific transition:** distinction between behavioral edge and recovery-mechanics risk.

## 8. Regime and failure-condition research

Regime classifier/matrix work tested volatility, trend persistence and adverse environments. It preserved the idea that degradation is identifiable, but retained subgroup evidence is too small for a deployable rule.

**Scientific transition:** from “does it work?” to “where does it fail?”

## 9. Robustness expansion and execution friction

Rules were loosened to test scale sensitivity, then stressed with entry/exit delays, wider spread, slippage and full-chaos conditions. The archived scenarios remain positive with PF 6.31–13.31 and drawdown from -3.00 to -4.57.

**Scientific transition:** reduced concern that the result depends only on ideal execution or one narrow parameter point.

## 10. Walk-forward and temporal checks

Yearly and walk-forward outputs were produced. Later years are positive; early-year data is sparse and mixed. This qualification belongs permanently alongside the stronger 2025–2026 results.

**Scientific transition:** evidence shifted from in-sample discovery to temporal challenge.

## 11. Monte Carlo validation

Synthetic and real-trade Monte Carlo variants reshuffled outcomes and added modeled skipped trades/slippage. Both distributions are favorable but conditional on the originating trade stream.

**Scientific transition:** sequence-risk challenge, not proof of live execution quality.

## 12. Cross-market universality

The consolidated journal reports transfer beyond Gold: EURUSD 329 trades/PF about 4.5, BTC 2,665/PF about 6.0, and preliminary NASDAQ 14/PF 2.37. The hypothesis became that markets differ in normalization speed more than in the existence of the behavioral effect.

**Scientific transition:** from instrument-specific strategy to universal behavioral framework.

## 13. Current QuantForge framework

The current framework preserves the pipeline implied by the research: validated data → market characterization → adaptive strategy → signal → risk → execution. Its outstanding scientific work is to operationalize the virtual-signal/recoil/persistence state machine, resolve recovery tail risk, and collect live forward evidence.

## Timeline conclusion

The surviving corpus supports a coherent progression: **mean reversion → volatility/panic confluence → virtual candidate → recoil → persistence → quick exit → robustness → cross-market hypothesis → execution validation need.** The next scientific milestone is not more indicator invention; it is reproducible, live-aware validation of this already identified behavior.
