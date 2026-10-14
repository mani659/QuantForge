# TASK143 — Close-Only Convention Decision Report

**Status:** records-only adjudication. No execution, no data reads, no
amendment applied. Verdict below; anything beyond it needs owner acts.

## 1. Source references (exact)

- v4 requires "execution next session open" (TASK134 draft §3, carried
  into v4). Dependency: open prices, which the bound file lacks
  (columns: observation_date, NASDAQ100 — TASK129 metadata).
- Frozen timestamps: signal uses closes ≤ T (T = last trading day of
  month); vol uses strictly prior month; position effective next session
  open; holding interval entry-open → next entry-open (v4 §3 + TASK134 §3).
- Gate failure: task142 (`a2233eea…`) — implementation impossible as
  written; no substitution attempted.

## 2. Convention analysis (no inferred conventions)

- **Same-close execution (trade at T's close): REJECTED.** T's close is
  known only after it prints; executing at it assumes closing-auction
  fills the frozen spec never establishes. This is the paper-close
  substitution the GEM precedent explicitly prohibits. Look-ahead-tainted.
- **Next-close execution (trade at first close strictly after T):
  VIABLE.** Every element exists in the bound file (date-ordered closes).
  Holding interval becomes close-to-close (clean for a price index);
  monthly cadence, paired structure, cost application, tie/flat rules,
  and fail-closed missing-data handling all transfer unchanged. One
  genuine semantic shift, disclosed: the signal-to-execution lag grows by
  ~1 session and overnight-gap capture moves from entry-open to holding
  return — the rule stays a monthly momentum rule, but it is not the same
  executable object. Hence an amendment (new version), never a silent
  reinterpretation.

## 3. Verdict: CLOSE_ONLY_AMENDMENT_VIABLE

**Proposed convention (for owner approval, not applied):** entry/exit at
the first daily close strictly after the signal month-end / prior exit
reference; all else frozen. Disclosed as a close-to-close price-index
test — not next-open execution and not evidence of tradable net
profitability (dividends, financing, spreads, and granularity caveats
carry over undiminished).

## 4. Approval status consequences

- B4 exception: REMAINS VALID (same investigation, dataset, and overlap;
  the convention change alters execution timing, not the admitted question).
- COMP-01 paired baseline: REMAINS VALID (identical-conventions clause
  holds: both legs move to next-close together).
- v4 execution authorization: DOES NOT TRANSFER (different frozen object
  once amended). Required next, in order: (i) owner approval of the
  close-only amendment as a new preregistration version; (ii) fresh
  execution authorization citing that version. Neither exists.
- Unresolved facts: none blocking this determination; the only unknowns
  are owner decisions (i) and (ii).

## 5. Smallest next action

Owner verdict on the close-only amendment (approve-as-v5 with the §4
wording, or reject/defer). If approved, a fresh execution authorization
citing v5. Nothing else may proceed meanwhile.
