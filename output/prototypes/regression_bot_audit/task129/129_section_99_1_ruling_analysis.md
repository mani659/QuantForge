# TASK129 — §99.1 Ruling Analysis: Volatility-Scaled TSMOM on NASDAQ100

**Status:** ruling proposal prepared, not recorded. No experiment authorized.

## 1. What §99.1 actually prohibits or permits

§99.1 (handoff line 1880) bars re-research of listed families — including
"Fixed TSMOM / 12-1 trend continuation" (DISC-022) — "via superficial
renaming, timeframe change, indicator change, market change, session
change, threshold change, stop/target change, **sizing change**, or
execution change." A new entry requires "a new causal claim that survives
the mechanism-distinctness gate." Per Q1=A (Task101 §7; Task102 §3.1),
family adjacency requires a recorded owner ruling — not automatic
exclusion, not automatic admission.

## 2. Sizing change vs new causal claim

The proposed strategy uses the IDENTICAL signal to DISC-022 (sign of
trailing 12-month return). The sole difference is the position-size
multiplier (target_vol/realized_vol vs constant). Under the governing
text, this is a **sizing change** on its face — an explicitly listed
superficial-change category.

The counterargument (TASK128): vol-scaling changes risk exposure and asks
a different question (does risk management improve momentum?). Against it:
the market mechanism exploited (return persistence) is unchanged, and the
Task99 REDUNDANT precedent holds that changed measurement of the same
phenomenon ("a different way to detect the same phenomenon") does not
create a new mechanism. If "different return stream" sufficed, the sizing-
change bar would be vacuous, since every sizing change alters returns.

The proposed H1 (scaled Sharpe > fixed Sharpe) is a claim about portfolio
construction efficacy, not a new claim about why prices behave as they do.
No new market mechanism is articulated.

## 3. Rescue-test analysis

The design's primary comparison executes fixed 12/1 TSMOM as its
comparator. That is the closed DISC-022 rule itself, run for comparison
purposes. Whether or not the vol-scaled leg is novel, the test *requires*
executing a closed mechanism — functionally a re-run of DISC-022 with an
added overlay leg. This weighs independently against admission: the test
cannot be run without touching the closed line.

## 4. Existing-rule conclusion

No existing rule permits this direction without a new act: §99.1's
sizing-change bar applies on its face; Q1=A reserves family-adjacent
admission to owner ruling; no B4-style acceptance exists for this concept
(Task99: such acceptances are prototype-specific and non-transferable).

## 5. Ruling proposal: OWNER/GOVERNANCE DECISION REQUIRED

**Recommended ruling content: REJECT admission under existing rules**
(the sizing-change bar applies; the comparator executes a closed rule).
This is NOT a no-recourse bar: consistent with Q1=A and the Task99 B4
precedent, the owner retains full discretion to grant B4-style acceptance
with a stated reason (e.g., an affirmative finding that risk-managed
momentum states a new causal claim). That acceptance, if granted, must be
recorded explicitly with its reason — it cannot be inferred from this
analysis, from TASK128, or from silence.
