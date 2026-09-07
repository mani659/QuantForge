# QUANTFORGE — NORGATE ARCHIVAL LICENSING DECISION V1

## 1. Executive Verdict
**PENDING — WRITTEN CLARIFICATION REQUIRED BEFORE PROCUREMENT**

While Norgate explicitly permits private research analysis, local extraction via Python, and CSV export for individual workflow use, the published End User License Agreement (EULA) lacks explicit clearance for permanent raw-data repository archival (especially post-subscription) and researcher-to-researcher sharing of raw data snapshots. Because the QuantForge reproducibility standard requires freezing a permanent SHA-256 fingerprinted snapshot of the raw data, formal written clarification must be obtained before committing funds.

## 2. Exact Licensing Question
**GOVERNANCE DECISION:**
Does Norgate's license permit the permanent local archival and private repository storage of an extracted raw NYSE Composite data snapshot (CSV), and its sharing with a co-researcher who holds their own active Norgate subscription, for the strict purpose of guaranteeing scientific reproducibility?

## 3. Authoritative Norgate Terms
**SOURCE-DERIVED FACT:**
- The license is granted to one individual natural person.
- Redistribution of Norgate’s raw "Content" is generally prohibited.
- Access to the proprietary NDU database requires an active subscription.
- Export to ASCII (CSV) and Python API usage is explicitly supported for analysis workflows.
- "Derived Data" (results that cannot be reverse-engineered into the original price series) may be retained/published freely.

## 4. Research Use
**MODEL INFERENCE:**
- **Status:** **CLEAR**
- **Reasoning:** The EULA explicitly supports use for personal analysis, systematic trading development, and backtesting (which encompasses private scientific research).

## 5. CSV Export / Local Storage
**SOURCE-DERIVED FACT:**
- **Status:** **CLEAR** (during active subscription).
- **Reasoning:** Norgate officially supports ASCII export and Python DataFrame export for the user's local analytical workflow. Temporary local storage of these extracts is inherently permitted to facilitate analysis.

## 6. SHA-256 / Fingerprinting
**MODEL INFERENCE:**
- **Status:** **CLEAR**
- **Reasoning:** Hashing a local file is a mathematical operation on the researcher's local machine and does not involve redistribution or EULA violation.

## 7. Private Repository Archival
**MODEL INFERENCE:**
- **Status:** **PENDING**
- **Reasoning:** Standard financial data EULAs (including Norgate's DRM design) often require purging raw extracts if a subscription lapses. The EULA does not explicitly grant the right to freeze and indefinitely store raw CSV snapshots in a private git repository as a permanent research artifact.

## 8. Derived Scientific Results
**SOURCE-DERIVED FACT:**
- **Status:** **CLEAR**
- **Reasoning:** The EULA specifically exempts "Derived Data" (metrics, results, statistical outputs like H01 that cannot be reverse-engineered into the original index prices) from restrictions. Publishing these results in research notes is fully permitted.

## 9. Researcher-to-Researcher Sharing
**MODEL INFERENCE:**
- **Status:** **PENDING**
- **Reasoning:** Redistribution is strictly prohibited. It is unclear if transferring a frozen raw CSV snapshot to a specific co-researcher who independently holds their own active Norgate Diamond subscription qualifies as prohibited "redistribution" or permitted collaborative workflow.

## 10. Required Written Clarification
**GOVERNANCE DECISION:**
The following inquiry must be sent to Norgate Data Support by the operator:

> **Subject:** Licensing clarification for private scientific research and reproducibility
> 
> Hello Norgate Support,
> 
> I am conducting private, non-commercial scientific research on broad-US equity behavior. I plan to subscribe to the US Stocks Diamond package. Before subscribing, I need to ensure my workflow complies with your EULA.
> 
> To guarantee the strict scientific reproducibility of my research, I must extract a historical snapshot of the NYSE Composite ($NYA) to a CSV file via your Python API, hash it (SHA-256), and store this CSV permanently in my private, local git repository. 
> 
> 1. Does the EULA permit me to retain this frozen raw CSV snapshot in my private local repository permanently (even if my subscription were to eventually lapse in the future), purely to maintain the integrity of my past research?
> 2. May I share this specific raw CSV snapshot privately with one co-researcher, provided they also independently hold an active Norgate US Stocks Diamond subscription?
> 
> To be clear, no raw data will ever be published, sold, or distributed publicly. Only derived statistical metrics (which cannot be reverse-engineered) will be published.
> 
> Thank you for your clarification.

## 11. Final Licensing Classification
**GOVERNANCE DECISION:**
**PENDING** — The core analytical use case is CLEAR, but the specific reproducibility/archival mechanics require explicit written confirmation.

## 12. Procurement Consequence
**GOVERNANCE DECISION:**
Do not purchase the ~$788 Norgate Diamond subscription yet, unless the operator explicitly accepts the residual licensing risk (e.g., willing to delete the raw CSV if the subscription lapses, relying solely on the Python script and active subscriptions for reproducibility).

## 13. Exact Next Legitimate Task
> **SUBMIT NORGATE CLARIFICATION INQUIRY OR ACCEPT RESIDUAL RISK**

The operator must either email the drafted inquiry to Norgate Support and await a response, or formally record a decision to accept the archival restriction and proceed with procurement.

## 14. Prohibited Follow-Up
- Purchasing the subscription automatically.
- Emailing Norgate Support automatically.
- Assuming archival is permitted because export is permitted.
- Modifying the H01 protocol.

## 15. Integrity
- No files were modified.
- No purchases were made.
- No H01 computations were performed.
- Authoritative terms were prioritized over technical feasibility.
