# TASK127 — Data Gap Report

## Feasibility screen result

**No existing dataset meets the 50-asset feasibility screen** for a
cross-sectional momentum evaluation with compatible overlapping history and
credible cost inputs.

## Largest available universes

| Universe | Assets | History | Costs | Gap |
|---|---:|---|---|---|
| _t37 cache (FX) | 11 | 2021-01→2026-10 | None | 39 assets short; no costs |
| lane_b_trend001 (mixed) | 15 | Varies by vendor | None | 35 assets short; incompatible vendors; no costs |
| data/m1 (FX/metals) | 5 | 2021-01→2026-10 | None | 45 assets short; no costs |
| lane_b_batch1 (ETFs) | 4 | 2007-05→2026-09 | Yes (Batch-1 frozen) | 46 assets short |

## Specific gaps preventing a 50-asset cross-sectional study

1. **No broad equity cross-section.** The repository contains no CRSP-like
   multi-stock return panel. The only multi-asset equity panel is the
   4-ETF Batch-1 set.

2. **No point-in-time universe membership.** No dataset records which
   assets were eligible at each historical date. Without this, survivorship
   bias cannot be excluded.

3. **No cost inputs for non-Batch-1 universes.** The _t37 cache (11 assets)
   and M1 data (5 assets) have no transaction-cost inputs. Cross-sectional
   momentum is cost-sensitive; a study without credible costs is not
   defensible.

4. **Incompatible return constructions.** The _t37 cache mixes M1 and H4
   frequencies. The lane_b_trend001 data mixes Yahoo and FRED vendors. No
   dataset provides a single construction across ≥50 assets.

5. **No survivorship-bias-free universe.** No dataset documents delisting
   rules or provides a point-in-time eligible-asset list.

## What would be needed to close the gap

- A verified multi-stock daily/monthly return panel with ≥50 assets,
  overlapping history of ≥5 years, total-return construction, and
  point-in-time universe membership
- Credible transaction-cost inputs for the same universe
- Authorization for research use (no evaluation authorization exists for
  any non-Batch-1 dataset)

None of these is present in the repository.
