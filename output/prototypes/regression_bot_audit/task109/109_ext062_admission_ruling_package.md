# TASK109 — EXT-062 §99.1 Admission Ruling Package (PREPARED, NOT RULED)

**Status:** ruling package prepared for the owner. No ruling is recorded
here; preparation is not admission. If the owner makes no ruling, the
governing default (closure stands) is unchanged.

## 1. Mechanism identity and causal claim

- EXT-062 = Maximum Diversification Portfolio (Choueifaty–Coignard 2008;
  long-only form 2013): choose weights maximizing DR(w) = wᵀσ/√(wᵀΣw).
  Risk-based weighting rule; no directional market-timing signal of any kind.
- Causal claim (concept's own): diversification-ratio maximization harvests
  asset risk premia more efficiently than cap-weighting (in-sample source
  claim, UNVERIFIED).

## 2. Evidence supporting distinctness (mechanism-identity prong)

- TASK108 family-by-family check (verified this session against handoff
  §99.1 read from disk): no overlap with mean-reversion, TSMOM 12/1, session
  expansion, sweep/reversal, breakout/follow, session-sequential quality,
  HTF→LTF, grid/basket/recovery (no lot multiplier/averaging-down/recovery —
  "basket" shared only as a word), ATR breakout, Zone Recovery, Q01–Q06,
  RF-001 confirmation-failure protocol, R1/R2, EXT-054, PROTO-TREND-001, or
  Batch 1 prototypes; ledger search found no weighting-optimization entry.
- Corroboration: task57 §4 ran its own distinctness audit before evaluation;
  task51 rated EXT-062 DISTINCT; task95 ranking row 9 concurs (DISTINCT).

## 3. Applicable existing rulings and comparisons

- Q1=A: §99.1 check mandatory and owner-ruled before specification-freeze
  (Task101 §7; Task102 §3.1–§3.2). The check is done (§2 above); the ruling
  is outstanding.
- Task99 (EXT-054): B4-style acceptance is prototype-specific and
  non-transferable; discretionary owner acts do not create entitlements.
- Task102 R1/R2 bars: mechanism-identity exclusions, not empirical failures
  — same character any EXT-062 ruling must preserve.
- **Dispositive records (evaluated-closure prong):** TASK57-MDP-001 is
  EXT-062's concept by explicit lineage ("EXT-062-MDP lineage (Task 51
  spec)... on {SPY, VEU, AGG, BIL}", task57 §3; engine implements the
  Choueifaty–Coignard long-only objective). It was evaluated (12-config
  discovery + validation + M1 gate) and closed: task74 CLOSED / NOT
  PROMOTABLE, rescue_authorized false, conclusion frozen (task77 status
  JSON). Library rule: evaluated items are hard exclusions; EXT-062 marked
  CONSUMED (task95 §5.2, ranking row 9: "Already evaluated → excluded").
  §3B: exhausted budgets require a new decision; nothing may be added
  because earlier results were weak.

## 4. What distinctness does and does not establish

- Establishes: no §99.1 mechanism-identity bar applies to the concept.
- Does NOT establish: profitability, testability, admissibility,
  specification completeness (B1–B6 open), data availability, or any right
  to re-evaluation. Distinctness is necessary and far from sufficient.

## 5. Sufficiency for admission under the exact §99.1 requirements

§99.1 bars re-research of protected families via superficial change. The
applicable bar for EXT-062 is narrower and harder: the concept-as-evaluated
is a CLOSED evaluated line. Admission of a new MDP specification would be
rescue/re-run without authorization. **On this record the concept is not
admissible**: the mechanism-identity prong is satisfied but the
evaluated-closure prong fails, and the latter is dispositive. A complete
specification could not cure it; only an explicit owner reopen act could.

## 6. Precise decisions and required rationales

- **REJECT (closure stands).** Rationale: TASK57-MDP-001 evaluated and
  closed the MDP concept; rescue unauthorized and frozen; library marks
  EXT-062 consumed/excluded. Effect: TASK108 draft remains an unadmitted
  proposal of historical interest only; no freeze, no data, no evaluation.
- **DEFER.** Rationale: take no admission decision now; closure intact
  meanwhile; revisit only upon an explicit owner reopen proposal with
  stated reason. Effect: identical to REJECT until such a proposal exists.
- **APPROVE (admit).** Supportable ONLY in the form of an explicit reasoned
  reopen act naming the TASK57-MDP-001 closure, lifting the rescue bar,
  and setting fresh prototype-count/complexity budgets plus data scope.
  Rationale must state why the closed result does not bind. Without these
  elements an approval would contradict rescue_authorized:false, the
  evaluated-hard-exclusion rule, and §3B — and is therefore not supported
  on the current record.

No ruling recorded. The governing default (CLOSED) holds unless and until
the owner rules otherwise.
