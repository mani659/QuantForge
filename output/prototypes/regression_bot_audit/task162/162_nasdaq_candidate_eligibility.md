# TASK162 — NASDAQ Fixed-Time Long: Eligibility (Phase A)

**Candidate (frozen as received, no tuning):** long NASDAQ index/CFD
exposure, open 01:05 broker time → close 23:50 same day, every eligible
trading day; no stops/targets/filters. Rationale on record: capture
index drift while avoiding overnight financing. External performance
claims (57.7% win, PF 1.24, DD 0.19%) treated as unverified and used for
nothing.

## Family-collision assessment (records only)

| Family / rule | Overlap? | Finding |
|---|---|---|
| S2 + its 5 reserved decisions | None — different timescale (daily hold vs annual week), mechanism (drift capture vs seasonal), window. S2 reservations untouched; nothing here pre-empts them. | Separable |
| SCR / RS-302 | None — Dec–Jan multi-day window vs daily holding rule. No shared window or mechanism. | Separable |
| DISC-024 session range expansion | None — no range/breakout logic of any kind; fixed time-based exposure, not a range trigger. | Distinct object |
| Session-mining prohibitions (§99.3, BASE-002 freeze, TASK128) | Applicable as METHOD constraint only. The window comes from an external source, fixed pre-outcome; no mining occurs provided times are never tuned. Any future variant/optimization would violate it. | Compliant iff frozen |
| DISC-021 mean reversion, DISC-022 TSMOM, R1/R2, BASE-001/002, TOM/OPEX/RS | None — no reversal, momentum-signal, breakout, or calendar-window logic. Unconditional holding rule. | Distinct |
| S1 clock exposure | None — S1 was outcome-contaminated state selection; this rule is fixed-clock from an external source, not state-selected. | Distinct |

**Phase A conclusion: ELIGIBLE in principle.** No family collision, no
S2 entanglement, no reopening. The video's clock or performance claims
grant nothing and change nothing — eligibility rests solely on mechanism
distinctness above. (Eligibility is not feasibility; see the data file.)
