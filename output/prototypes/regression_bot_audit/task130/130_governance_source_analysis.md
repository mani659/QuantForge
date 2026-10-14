# TASK130 — Governance Source Analysis (§99.1 ruling authority)

**Question:** who may record a §99.1 admission ruling for VS-TSMOM-01?

## Exact governing texts (verified from disk this session)

1. **§99.1** (handoff): listed families "must not be re-researched via
   superficial renaming, timeframe change, indicator change, market
   change, session change, threshold change, stop/target change, **sizing
   change**, or execution change. Any genuinely new entry requires a new
   causal claim that survives the mechanism-distinctness gate."
2. **Q1=A** (Task101 §7; Task102 §3.1): "§99.1 applies to Lane B admission
   as a **mandatory owner-ruled** check." General rule, not one-off.
3. **Role addendum:** "nothing in this addendum authorizes any Lane B
   evaluation. Authorization comes **only from an explicit owner
   decision** tied to a frozen prototype/specification."
4. **Role §21:** ChatGPT "does not self-authorize research, governance
   changes, or architectural overrides" and does not substitute its
   judgment for the authorized owner.
5. **TASK130 prompt §5:** "If the owner must personally select an option,
   present the options and recommendation in the report, then STOP. Do
   not select on the owner's behalf."

## Finding

No delegation permits the technical reviewer to record a §99.1 ruling.
Q1=A reserves rulings to the owner expressly; the role contract reserves
all authorization to explicit owner decisions; TASK130 reiterates the
prohibition. The ruling in VS-TSMOM-01's case additionally turns on a
judgment call (sizing change vs new causal claim) that the framework
assigns to owner discretion (cf. Task99 B4 precedent: acceptances are
discretionary owner acts with stated reasons).

**Consequence:** this task presents options + a technical recommendation
and records DECISION_PENDING. Selecting A, B, or C as the ruling would
exceed authority.
