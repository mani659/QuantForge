# TASK128 — Closed Mechanism Distinction

## Selected direction: volatility-scaled time-series momentum on NASDAQ100

**Mechanism:** signal = sign(r12) × (target_vol / realized_vol), where r12
is the trailing 12-month return and realized_vol is the trailing realized
volatility. The position is long when r12 > 0 and short when r12 < 0,
scaled inversely by realized volatility.

## Distinction from closed mechanisms

| Closed mechanism | What it tested | Why this is different |
|---|---|---|
| DISC-022 (fixed 12/1 TSMOM) | Unconditional momentum with fixed lookback and fixed sizing | This is **regime-conditional**: the position size varies with realized volatility. The signal is the same (r12) but the sizing is vol-scaled, producing a different risk profile and different return stream. Fixed TSMOM is a special case where target_vol / realized_vol = 1. |
| VM-001 (volatility targeting) | Fixed volatility target regardless of signal | VM targets a constant vol level. This uses volatility to scale the **momentum signal** — it does not target a vol level, it adjusts signal strength. The economic question is different: "does vol-scaling improve momentum?" vs "does vol-targeting produce acceptable returns?" |
| DISC-021/NEG-065 (mean reversion) | Deviation-from-baseline reversal | This is continuation (momentum), not reversal. Opposite signal direction. |
| PROTO-TREND-001 (daily TSMOM) | 12/1 TSMOM on 14 markets | Different instrument (single index vs multi-market), different sizing (vol-scaled vs fixed), different frequency (daily signal vs monthly). |
| CAND-025 (macro shock void) | Post-shock liquidity reversal | Different trigger (statistical vol regime vs scheduled macro event). |

## The critical distinction: DISC-022

DISC-022 tested **fixed** 12/1 TSMOM — unconditional momentum with a fixed
lookback and no volatility adjustment. The proposed direction is
**volatility-scaled** momentum — the signal is conditioned on the volatility
regime, and the position size is inversely proportional to realized
volatility.

This is a **materially different mechanism**, not a renaming:
- Fixed TSMOM: position = sign(r12) × constant
- Vol-scaled TSMOM: position = sign(r12) × (target_vol / realized_vol)

The vol-scaling changes both the timing (the signal is stronger in low-vol
regimes) and the sizing (positions are smaller in high-vol regimes). This
produces a different return stream with different risk characteristics.

**However**, this distinction must be formally established via a §99.1
ruling before any experiment. The §99.1 firewall bars "Fixed TSMOM / 12-1
trend continuation." Whether vol-scaled TSMOM is a "superficial renaming" or
a "genuinely new causal claim" is an owner ruling, not a technical
determination.

## What new evidence could justify reconsideration

If the owner rules that vol-scaled TSMOM is distinct from fixed TSMOM, the
proposed experiment would be the first empirical test of this specific
mechanism on a single instrument with adequate power (40 years daily data)
and explicit costs.

If the owner rules that vol-scaled TSMOM is a variant of fixed TSMOM, the
direction is barred and no single-instrument momentum direction is available.
