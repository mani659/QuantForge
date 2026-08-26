# QUANTFORGE — CROSS-MARKET LIQUIDITY SWEEP / REVERSAL
# INDEPENDENT PRE-REGISTRATION AUDIT V1

## 1. Executive Verdict
**CONDITIONAL PASS — SPECIFIC CORRECTIONS REQUIRED**
The protocol successfully eliminates subjective SMC ambiguity, replacing discretionary chart-reading with deterministic market-structure geometry. The scientific object, session definitions, and primary event boundaries are extremely robust. However, severe ambiguities remain in the **Control Group timestamp mechanics**, **Bootstrap event-flattening logic**, and **P-value computation**. These must be resolved before the protocol is scientifically executable.

## 2. Scientific Object
**PASS**. The protocol rigorously isolates a behavioral price excursion rather than a profitability or institutional-intent claim.

## 3. Discovery vs Validation
**PASS**. `XAUUSD` is properly isolated as the discovery origin. The validation universe explicitly prevents a single-market success from being falsely generalized.

## 4. Market Universe
**PASS**. Eligibility is cleanly defined via objective M1 data requirements, not historical performance.

## 5. Session Definitions
**PASS**. Fixed to `America/New_York` using standard institutional phase boundaries. DST handling is deterministic.

## 6. Asian Reference Level
**PASS**. Reference levels are generated exclusively from the strictly defined Asian window with no look-ahead.

## 7. Sweep
**PASS**. Deterministic inequality (`> High` / `< Low`) completely prevents arbitrary ATR or tick threshold optimization.

## 8. Rejection
**PASS**. Defined objectively via intrabar wick metrics (Price penetration vs Close failure).

## 9. Reversal Confirmation
**PASS**. The protocol uses the first M1 close beyond the exact sweep candle's opposite extreme. This is a highly robust, objective proxy for a Market Structure Shift.

## 10. Event Uniqueness
**PASS**. Restricted to the first confirmed upper and lower sweep per market, per calendar day, explicitly avoiding dependency cascades from repetitive intra-session sweeps.

## 11. Primary MFE
**PASS**. 120-minute forward horizon, properly anchored to the swept structural level rather than a hypothetical entry fill.

## 12. Control Group
**FAIL (BLOCKING)**. 
- *Ambiguity 1*: The protocol states confirmation must not occur "within the standard observation window," but this window is undefined. (Is it the remainder of the NY session? 2 hours? 12 hours?)
- *Ambiguity 2*: Treatment MFE explicitly begins at the "reversal confirmation" timestamp. Control events, by definition, lack a reversal confirmation. Therefore, the exact timestamp where the 120-minute MFE horizon begins for a control event is entirely undefined. Does it start at the close of the sweep candle?

## 13. Multiple Events / Day
**FAIL (BLOCKING)**.
- *Ambiguity*: The protocol states days can have up to two events (one upper, one lower) and that days are resampled as blocks. It fails to define how those events are evaluated across the block. When 10,000 day-blocks are resampled, are all contained events simply flattened into a single 1D array to compute the overall median MFE? The mapping between the day-level resampling and the event-level median is completely undefined.

## 14. Primary Statistic
**PASS**. Difference in medians ($\Delta M$) is robust against heavy-tailed MFE distributions.

## 15. Bootstrap / Dependence
**PASS (Conditional on flattening logic)**. The Stationary Block Bootstrap parameters ($L=10$, $B=10,000$) perfectly address the serial dependence and volatility clustering inherent to these time series.

## 16. Inference
**FAIL (BLOCKING)**.
- *Ambiguity*: The protocol requires reporting market-level p-values for Holm-Bonferroni correction but fails to specify how the p-value is computed from the bootstrap distribution. Is it the raw empirical fraction of replicates crossing zero, or a mean-recentered null distribution?

## 17. Multiple Comparisons
**PASS**. Family-wise error rate control via Holm-Bonferroni correctly prevents cross-market data mining.

## 18. Cross-Market Interpretation
**PASS**. The protocol defines distinct tiers of success (Instrument-specific vs Cross-market support).

## 19. SMC Firewall
**PASS**. Complete removal of subjective Smart Money interpretation. No order blocks or manual imbalance zones.

## 20. Strategy Firewall
**PASS**. Excursion is measured independently of stop-losses, trailing logic, and risk models.

## 21. ML Firewall
**PASS**. Explicitly excluded.

## 22. Data Gates
**PASS**. The minimum 100-event threshold and invalid-day limit correctly prevent small-sample statistical noise.

## 23. Outcome-Blindness
**PASS**. No historical inspection or result-driven parameter selection is present.

## 24. Findings Table

| Section | Status | Severity | Issue | Resolution Required |
|---|---|---|---|---|
| 12. Control Group | FAIL | HIGH | Missing confirmation-absence window and undefined MFE anchor timestamp | Define exactly when the control event's 120-minute window begins. |
| 13. Multiple Events/Day | FAIL | HIGH | Undefined mapping between day-level bootstrap and event-level median | Specify the flattening logic for events inside resampled days. |
| 16. Inference | FAIL | HIGH | Missing p-value formulation | Provide the exact mathematical formula for the empirical two-sided p-value. |

## 25. Required Corrections
To achieve full executability, the protocol must be amended to state:
1. **Control Definition**: A control event requires that no confirmation occurs before the end of the NY session (17:00 ET). The 120-minute MFE window for control events begins exactly at the **close of the initial sweep-rejection candle**.
2. **Bootstrap Aggregation**: During each bootstrap iteration, all treatment events contained within the resampled day-tuples are flattened into a single treatment array, and all control events are flattened into a single control array, from which the replicate's $\Delta M^*$ is calculated.
3. **P-value Construction**: The two-sided empirical p-value is computed directly from the uncentered bootstrap distribution as: $p = 2 \times \min(P(\Delta M^* \le 0), P(\Delta M^* \ge 0))$.

## 26. Final Execution Recommendation
**DO NOT EXECUTE.**
Apply the three deterministic corrections listed in Section 25. Once amended, the protocol is fully authorized for multi-market execution.

## 27. Integrity
This audit was performed strictly as an adversarial, read-only process. No code was written. No data was processed. No p-values or event counts were observed to influence the audit verdict.
