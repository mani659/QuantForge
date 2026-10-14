# TASK127 — Decision Report

## Decision: B — DATA GAP

No suitable existing universe is available for a cross-sectional momentum
evaluation over a materially broader universe than SPY/VEU/AGG/BIL.

## Evidence

- Largest available universe: _t37 cache with 11 FX symbols (2021-01→
  2026-10). No cost inputs. No point-in-time membership.
- Only universe with cost inputs: Batch-1 ETF panel (4 assets). Already
  consumed. Reuse requires new authorization.
- No CRSP-like equity cross-section exists in the repository.
- No dataset provides ≥50 assets with compatible overlapping history and
  credible cost inputs.

## Implication for the XSM design

The TASK126 conclusion (A — CALIBRATED, LOW-POWER) was based on the 4-asset
ETF panel. A broader universe could change the detectability assessment —
but no such universe exists in the repository. The data gap is the binding
constraint, not the statistical method.

## What this does NOT mean

- It does not mean cross-sectional momentum is untestable in principle.
- It does not mean the 4-asset XSM result is wrong.
- It does not authorize data collection or downloading.
- It does not authorize any strategy test or evaluation.

## Recommended next action

If the owner wants to pursue cross-sectional momentum, the required next
step is **data acquisition** (a verified multi-stock return panel with
≥50 assets, compatible history, point-in-time membership, and credible
costs). This requires a separate explicit owner authorization for data
collection, which TASK127 does not provide.

Alternatively, the owner may select a different hypothesis-testing
direction that does not require a broad cross-sectional universe.

TASK127 authorized this read-only inventory only. It does not authorize
data collection, strategy testing, or any subsequent task.
