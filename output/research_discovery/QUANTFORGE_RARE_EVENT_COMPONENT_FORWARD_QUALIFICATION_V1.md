# QUANTFORGE — RARE-EVENT COMPONENT FORWARD QUALIFICATION
# CAND-024 / CAND-035
# DATE: 2026-08-27

## 1. Purpose
The purpose of this track is to formally operationalize and adjudicate the Rare-Event Component Qualification for CAND-024 and CAND-035. The objective is not to improve these strategies or re-litigate their historical economics, but to verify that the exact frozen historical events can be detected and represented prospectively under real/demo market conditions without semantic drift.

## 2. CAND-024 Frozen Identity
- **Name:** Friday Afternoon Positional De-Risking
- **Mechanism Family:** Session / Market-Mechanics Behavior
- **Exact Event Definition:** Friday 12:00 NY time (EST).
- **Exact Preconditions:** The High printed between 08:00 EST and 12:00 EST must exceed the Weekly High (prior to Friday), AND the 12:00 EST open price must be lower than the 08:00 EST open price (Morning Exhaustion State).
- **Exact Entry:** Market order short on USATECHIDXUSD exactly at 12:00:00 EST open.
- **Exact Exit:** 15:45:00 EST open.
- **Exact Direction:** Short.
- **Exact Duplicate / Re-Arm Rule:** Maximum one event per week. Re-arms next Friday.
- **Exact Friction Assumption:** 2.0 index points round-trip.
- **Exact Historical Measurement Window:** M1/M5/H1 data tested at G1.
- **Historical N:** 13
- **Historical Frequency:** 4.55 events/year
- **Historical Mean Net:** +40.59 bps
- **Historical Median Net:** +34.00 bps
- **Historical Scientific Status:** Qualified (Failed standalone promotion purely on frequency).

## 3. CAND-035 Frozen Identity
- **Name:** Month-End Final-Hour Imbalance Acceleration
- **Mechanism Family:** Forced Flow / Scheduled Mechanics
- **Exact Event Definition:** Last trading day of the month at 15:00 ET.
- **Exact Preconditions:** USATECHIDXUSD 15:00 ET open is > 09:30 ET open (Up Day).
- **Exact Entry:** Market order long on USATECHIDXUSD exactly at 15:00 ET.
- **Exact Exit:** 16:00 ET (Market close).
- **Exact Direction:** Long.
- **Exact Duplicate / Re-Arm Rule:** 1 event per month maximum. No overlap.
- **Exact Friction Assumption:** 2.0 index points round-trip (Standard for USATECHIDXUSD).
- **Exact Historical Measurement Window:** Tested at G1 over ~3 years.
- **Historical N:** ~13
- **Historical Frequency:** 4.09 events/year
- **Historical Mean Net:** +62.36 bps
- **Historical Median Net:** Positive (strong right skew).
- **Historical Scientific Status:** Qualified (Cleanly mapped and passed mid-month counterfactual).

## 4. Historical Qualification Evidence
Both candidates possess massive historical per-event economics (+40.59 bps and +62.36 bps mean net, respectively) and have cleanly passed their scientific counterfactual validations. Their failure to promote to standalone strategies in G2 was explicitly and exclusively attributable to their low calendar frequency (~4.5 opportunities per year), which makes chronological holdout testing mathematically invalid.

## 5. Event-Count Doctrine
Calendar duration is NOT the primary qualification unit for rare events. A 4-event/year mechanism cannot be judged by a fixed 7-day or 30-day paper observation. The forward qualification track is **EVENT-COUNT BASED** and **OPEN-ENDED / EVENT-DEPENDENT**. The primary unit of measurement is ONE INDEPENDENT QUALIFYING EVENT.

## 6. Minimum Event Count
- **Minimum:** 3 independent, qualified prospective events per candidate.
- **Rationale:** A minimum of 3 events is an operational evidence requirement to prove that the detection and execution infrastructure can consistently identify the semantic event without system outages, slippage anomalies, or semantic drift, while maintaining directional consistency with the historical artifact.

## 7. Target Event Count
- **Target:** 5 independent, qualified prospective events per candidate.
- **Rationale:** 5 events provide a stronger adjudication baseline to verify that the historical mean/median expectations are carrying forward into live market data realistically.

## 8. Calendar Window Policy
Calendar time is subordinate to event count. The observation window is open-ended until the minimum event count is achieved. A maximum calendar window of 18 months is established merely as an operational safety boundary, not an adjudication threshold.

## 9. Event Independence
For each event, we require:
- Unique qualifying episode.
- No duplicate triggers.
- No overlapping duplicate representation.
- Re-arm rules strictly respected (weekly for CAND-024, monthly for CAND-035).
- No reuse of a single market episode as multiple samples.
Exact event IDs and UTC timestamps must be formally recorded.

## 10. Detection Contract
For every detected event, the system must record:
- UTC timestamp
- Local timestamp
- Instrument (USATECHIDXUSD)
- Event identity (CAND-024 or CAND-035)
- Event direction
- Event completion time
- Theoretical entry
- Paper entry
- Bid, Ask, Spread
- Slippage estimate (if available)
- Detection latency
- Whether event was actually captured
- Reason for any missed event

## 11. Paper Execution Contract
Execution is strictly paper/demo. No live money. No production deployment. The paper execution layer must definitively prove the sequence: `event → detection → prescribed entry → prescribed exit` without altering the frozen strategy logic to match hindsight.

## 12. Execution Metrics
To be measured globally during the forward run:
- **Detection Rate:** Detected / genuine qualifying events.
- **Capture Rate:** Successfully paper-entered / detected events.
- **Miss Rate:** Detected but not captured.
- **False Activation Rate:** Signals incorrectly classified as qualifying events.
- **Entry Deviation:** Actual paper entry vs frozen theoretical entry.
- **Spread & Slippage:** Observed at entry.
- **Operational Interruptions:** Outages, disconnections, malformed data, clock drift.

## 13. Forward Outcome Metrics
For each completed forward event, record:
- Entry, Exit
- Gross result, Friction, Net result
- Maximum adverse movement (MAE) only if it is part of the frozen contract (neither CAND has an intra-trade stop).
- Whether exit occurred exactly according to the frozen rule (time-based).
No other MFE/MAE analytics are authorized. Validation, not optimization, is the goal.

## 14. Identity Matching
For every forward event, we must verify: *Would this exact event have qualified under the historical frozen definition?* If not, it is an EVENT IDENTITY MISMATCH and does not count toward the qualification event total.

## 15. Failure Conditions
Early termination is triggered ONLY by objective operational failures, including:
- Definition integrity failure (semantic drift).
- Runtime instability.
- Impossible event reconstruction in real-time.
- Symbol/data feed failure.
Negative early returns are NOT a valid condition for early termination.

## 16. Adjudication Rules
At the end of the predefined event-count threshold (3 to 5 events), adjudication evaluates:
- **A — OBJECT IDENTITY:** Was the event definition preserved?
- **B — DETECTION INTEGRITY:** Were genuine qualifying events captured?
- **C — EXECUTION INTEGRITY:** Could the prescribed entry/exit be represented faithfully?
- **D — COST REALISM:** Were observed spread/slippage compatible with historical assumptions?
- **E — DIRECTIONAL CONSISTENCY:** Was forward behavior broadly consistent with historical artifact?
- **F — EVENT COUNT:** Was the predefined event threshold reached?

## 17. Component Qualification States
Following adjudication, candidates may be assigned one of three statuses:
1. RARE-EVENT COMPONENT — FORWARD QUALIFIED
2. FORWARD VALIDATION INSUFFICIENT
3. FORWARD VALIDATION FAILED

A successful forward track yields a "FORWARD QUALIFIED" rare-event component. It does NOT automatically mean "SYSTEM-QUALIFIED COMPONENT" (System Assembly remains a distinct future gate).

## 18. CAND-042 Exclusion
CAND-042 (Correlated Shock Reversion) retains its status as COMPONENT-CANDIDATE — EVENT OPPORTUNIST / NOT SCIENTIFICALLY QUALIFIED. It is explicitly EXCLUDED from this forward qualification track because its causal mechanism (margin call/forced liquidation) remains unproven.

## 19. CAND-059 Exclusion
CAND-059 (Freshness/First-Touch) retains its status as STATE-ARTIFACT — INFORMATIONALLY SUPPORTED / NOT STANDALONE PROFITABLE. It is explicitly EXCLUDED from this forward qualification track because it requires an interaction study with a fully qualified Alpha target.

## 20. CAND-015 Independence
The CAND-015 forward observation (7-day duration) is ACTIVE / PROTECTED and entirely separate. Its logs, runner, and infrastructure will not be merged, inspected, or utilized by this track.

## 21. System Assembly Exclusion
SYSTEM ASSEMBLY DEFINED — NOT YET EXECUTABLE.
This track qualifies independent rare-event components. No portfolio construction, risk sharing, or combined module scoring will occur.

## 22. Next Authorized Action
The next authorized task is the **EXPLICIT LAUNCH OF RARE-EVENT FORWARD QUALIFICATION**. 
*Infrastructure Note:* Current repository inspection reveals no existing standalone forward-runner infrastructure distinct from whatever black-box environment CAND-015 is operating in. A dedicated paper execution runner for CAND-024 and CAND-035 will need to be developed or provisioned at launch.

## 23. Integrity
No historical research was rerun. No parameters were optimized. Entry/exit thresholds were perfectly preserved. The candidates remain strictly independent.
