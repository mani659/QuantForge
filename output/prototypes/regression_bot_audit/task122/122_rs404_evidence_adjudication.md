# TASK122 — RS-404 (a)/(b)/(c) Evidence Adjudication (records only)

**Sources:** frozen spec `proto_rs404_v1/00_frozen_specification.md`
(46 lines; rules 1–14, amendments 1–5, fail-closed list, no-rescue lock);
stop record `04_evaluation_stop_record.md` (61 lines; STOPPED BEFORE
EXECUTION, data-integrity failure, options (a)/(b)/(c)); task95 §5.2
pending-status line. No backtest, remeasurement, data work, or new
candidate activity performed here.

## 1. Branch structure (from the records, not assumed)

(a)/(b)/(c) are mutually exclusive paths, not implementation variants:
(a) proceeds under the frozen methodology given owner-supplied input;
(b) exits to a separately governed new specification (stop record: "new
specification, not a silent repair"; spec lock: any change = different
governed object); (c) terminal closure as invalid. Only one can happen;
(a)/(c) dispose of this evaluation, (b) creates a different object.

## 2. Evidence against each branch

- **(a) owner-supplied archive:** unfulfilled. Established on record:
  broker publishes upcoming-only weekly tables (no historical per-event
  archive retrievable); MT5 holds no dividend-adjustment ledger;
  reconstruction from constituent data prohibited as wrong-methodology;
  omission non-conservative (~60–80 bps vs plausible edge). No archive
  supplied or on record. Fulfillable only by owner-side production —
  isolated as the sole remainder (see §4).
- **(b) spec amendment:** unavailable in this adjudication. Requires a
  separately governed new specification + admission scrutiny; calendar
  seasonal sits in the exhausted class (task51 EXT-060 precedent); the
  frozen no-rescue lock bars silent repair. No such authorization exists;
  none is created here.
- **(c) close as invalid:** supported. Triggered by the spec's own
  fail-closed machinery (rule 8, amendment 3, fail-closed list:
  unestablishable dividends → FAIL CLOSED) and the stop record's
  established conclusion (required input CANNOT BE ESTABLISHED). No result
  exists, so nothing is rescued or reinterpreted.

## 3. Selected disposition

**(c) — close PROTO-RS404-V1 as INVALID on data-integrity grounds.**
Current record fails the evaluation's own admission criteria (required
dividend input unestablishable under frozen §§8/amendment-3). No rescue
path invented. Negative knowledge preserved with precision: this closure
makes NO claim about Sell-in-May returns (no outcome exists — not a
negative economic result, per the stop record). RS-404 status: CLOSED.

## 4. Isolated owner-side remainder (not a pending decision)

The single theoretical override: the owner produces a documented broker
dividend archive. That would vacate (c) only under a new explicit
authorization to proceed — it does not automatically revive anything, and
absent such production (a) remains unfulfilled. No routine or technical
choice is returned to the owner.
