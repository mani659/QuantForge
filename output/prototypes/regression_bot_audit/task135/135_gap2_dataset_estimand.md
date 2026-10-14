# TASK135 — Gap 2 Decision: Dataset/Estimand Compatibility

## Finding

The FRED NASDAQ-100 price-index series CAN support the preregistered
claim ONLY in narrowed form. It CANNOT support a tradable net-return
claim. ^NDX/total-return substitution is not permitted by the approved
scope (different object; needs a separate owner decision, not made here).

## Narrowed claim (adopted as a restriction, not an expansion)

- **Supported:** index-level paired net differential under declared cost
  assumptions — both legs computed on the same price series with the
  identical cost schedule, so the comparison is internally consistent as
  a measure of scaling value *on price returns*.
- **Explicitly out of scope:** tradable P&L (dividends ~1%/yr omitted,
  financing unmeasured, lot granularity unaddressed). No statement in any
  future report may present the result as executable-trading evidence;
  that belongs to a forward/demo stage with its own authorization.
- Ranking/signal use is unaffected (dividends are smooth relative to the
  12-month formation window).

## Consequence for the preregistration

Primary outcome relabeled "index-level net differential"; a tradability
caveat section is mandatory in any future report. No owner act needed for
this narrowing (it restricts, not expands, the claim).
