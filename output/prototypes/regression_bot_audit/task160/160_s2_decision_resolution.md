# TASK160 — S2 Decision Resolution (delegated findings + reserved selections)

**Authority note:** this file records delegated technical findings (read,
transcribed, and verified from source records) and isolates owner-reserved
selections. No selection is made here. Delegation claimed is routine
technical judgment only; the S2 audit's explicit reservations stand
unmodified. HEAD `666c1a9`; HOLD/NONE (re-verified post-write; see chat).

## 1. Delegated confirmations (source-grounded, no selection involved)

Verified from the S2 audit §§1–2, task95 rows, and Batch-1 conventions —
each confirmed as RECOVERED (transcribed, provenance cited), not chosen:
- **Instrument:** SPY-class ETF daily closes (Batch-1 convention; file
  `lane_b_batch1/data/SPY.csv`, SHA `483919f8`, verified).
- **Direction:** long-only (recovered proposal; §5 outcome-blindness test).
- **Entry/exit mechanics:** executable close ask (entry) / bid (exit),
  RS-404 clock precedent pattern; max-1-window-per-year; windows disjoint
  across years by construction (verified arithmetically from the rule).
- **Friction:** 10/5/0 bps per side (recovered proposal; Batch-1 family).
- **No-outcome-contamination finding:** no RS-302 result existed to borrow
  from; S2's weaknesses are sourcing/specification, not contamination
  (audit §5; preserved as found).
- **New material finding for the owner decisions (from source records,
  not new research):** per the audit §2 source anatomy, January sessions
  1–2 sit INSIDE Hirsch's canonical SCR window — the RS-302 phenomenon
  family — while sessions 3–5 have no source claim anywhere. RS-302's
  closure was data-integrity (venue/feed), NOT economic falsification, so
  this is an adjacency question for the owner (Q1-A pattern), not a bar.
  A sessions-3–5-only variant is NOT offered (unsourced invention,
  prohibited).

## 2. Reserved selections (owner acts; recommendations, not selections)

1. **Window:** first-5-sessions vs calendar-week. Recommended:
   first-5-sessions (exchange-governed, deterministic). Downside: none
   evidentiary. **Requires owner selection.**
2. **Identity:** unconditional week exposure vs barometer-conditional
   timing (different strategies; conditional needs its own source-quality
   + DISC-022-adjacency track). Recommended: unconditional (smaller
   falsifiable unit; conditional is a separate unadjudicated hypothesis).
   Downside: may dilute a conditional effect. **Requires owner selection —
   this selects the hypothesis itself.**
3. **Control/comparison:** TOM-convention (unconditional long, cumulative-
   net) vs alternatives; S4-degenerate paired form prohibited. Recommended:
   TOM convention (avoids documented degeneracy). Binding it is a
   specification act. **Requires owner selection.**
4. **Budget:** ~34 events worth a slot (RS-302 precedent: ask first).
   No technical recommendation for/against spending is offered —
   resource commitment is owner prerogative. **Requires owner judgment.**
5. **Holiday handling:** NYSE rule governs short sessions (determinable);
   ADHOC_CLOSURES list adoption outstanding. **Requires owner selection**
   (rides with the same act).

## 3. Provenance and scope of this file

Basis: S2 audit §§1–9, task95 §5.2/§7, Batch-1 data registry, TASK153–155
records (hashes re-verified). Scope: findings + isolated questions only.
No frozen spec (blocked — see verdict line in chat message), no
implementation, no data use, no registration, no governance change.
