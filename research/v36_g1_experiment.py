"""
V36 G1 — ECONOMIC PLAUSIBILITY SCREEN
CAND-105: Cross-Asset Lead-Lag Asymmetry (XAUUSD -> USATECHIDXUSD)
CAND-106: Intra-Bar Price Distribution Quality (USATECHIDXUSD)

Frozen definitions from V36 G0 + V36 G0 integrity audit.
All parameters are STRUCTURAL and predeclared BEFORE execution.
No parameter is selected from observed outcomes.
"""

import pandas as pd
import numpy as np
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =============================================================================
# FROZEN PARAMETERS — DO NOT MODIFY AFTER FIRST EXECUTION
# =============================================================================

TECH_FILE = PROJECT_ROOT / "data/m1/USATECHIDXUSD_M1.csv"
GOLD_FILE = PROJECT_ROOT / "data/m1/XAUUSD_M1.csv"

# Universal G1 conventions (V32-V35 screens)
FRICTION_BPS = 2.0
OUTCOME_HORIZON = 60      # bars on M1 = 60 minutes
REARM_BARS = 60           # minimum separation between sampled observations

# ---------------------------------------------------------------------------
# CAND-105: Cross-Asset Lead-Lag Asymmetry
#
# Frozen G0 construct: rolling correlation of returns between XAUUSD and
# USATECHIDXUSD + DIRECTION OF LEAD.  The G0 integrity audit requires G1 to
# measure temporal lead/lag structure, not merely contemporaneous co-movement.
#
# Implementation (predeclared, no lag optimization):
#   - Aligned M1 bars where BOTH assets have a completed 1-minute return
#     (inner join on exact timestamps, returns only over 1-minute-adjacent
#     bars of each asset, contiguous aligned runs preserved).
#   - Directional lead measure at frozen lag = 1 aligned minute, computed over
#     a trailing window of C105_WINDOW completed pairs ending at the signal
#     bar (all information <= close of signal bar):
#       rho_g2t = corr( gold_ret[s] , tech_ret[s+1] )   s in trailing window
#       rho_t2g = corr( tech_ret[s] , gold_ret[s+1] )   s in trailing window
#       lead_asym = rho_g2t - rho_t2g
#     lead_asym > 0 => gold's prior-minute move is more associated with tech's
#                      subsequent-minute move than the reverse (GOLD LEADS)
#     lead_asym < 0 => TECH LEADS
#   - Treatment = top tercile of lead_asym (gold-lead regime)
#     Control   = bottom tercile of lead_asym (tech-lead regime)
#     Middle tercile excluded (regime boundary ambiguity).
#   - Outcome = USATECHIDXUSD forward return over OUTCOME_HORIZON bars of the
#     TECH series (positional, entry at signal-bar close), net of 2 bps.
#   - Deduplication: REARM_BARS between sampled observations.
#
# Contemporaneous (lag-0) correlation is reported only as a REFERENCE
# diagnostic to assess whether any lead-regime effect merely tracks the
# co-movement level.  It is NOT the test.
# ---------------------------------------------------------------------------

C105_LEAD_LAG = 1
C105_WINDOW = 240
C105_TERCILE = (1.0 / 3.0, 2.0 / 3.0)

# ---------------------------------------------------------------------------
# CAND-106: Intra-Bar Price Distribution Quality
#
# Frozen G0 construct: the internal structure of a completed M1 bar --
# where open and close fall within the bar's high-low range -- proxies
# directional conviction (open near one extreme, close near the other) vs
# indecision (open/close near the range middle / small body).
#
# Implementation (predeclared, fixed structural thresholds):
#   - Conviction observable per completed M1 bar:
#       body_frac = |close - open| / (high - low)   in [0, 1]
#     body_frac near 1 => open near one extreme and close near the other
#                         (full-range directional body: conviction)
#     body_frac near 0 => close near open (indecision / doji character)
#   - Treatment = bars with body_frac >= 0.70 (high conviction)
#     Control   = bars with body_frac <= 0.30 (indecision)
#     Middle band excluded (boundary ambiguity).  Fixed thresholds predeclared.
#   - Outcome = USATECHIDXUSD forward return over OUTCOME_HORIZON bars after
#     the completed bar close, net of 2 bps friction (identical long-drift
#     convention for treatment and control).
#   - Deduplication: REARM_BARS between sampled observations.
#
# OHLC limitation (reported in artifact): OHLC does NOT reveal intra-bar
# order flow, bid/ask dynamics, depth, or the full sequence of trades.
# The observable is an OHLC-derived PROXY for intra-bar distribution.
# ---------------------------------------------------------------------------

C106_HIGH_CONVICTION = 0.70
C106_INDECISION = 0.30

# =============================================================================
# DATA LOADING + ALIGNMENT
# =============================================================================

def load_ohlc(path):
    df = pd.read_csv(path)
    df.columns = [c.lower().strip() for c in df.columns]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df


def one_minute_returns(df):
    """Close-to-close log returns only where consecutive bars are exactly 1 minute apart."""
    dt = df['timestamp'].diff()
    ret = np.log(df['close'] / df['close'].shift(1))
    ret[dt != pd.Timedelta(minutes=1)] = np.nan
    return ret


def align_assets():
    tech = load_ohlc(TECH_FILE)
    gold = load_ohlc(GOLD_FILE)

    tech['tech_ret'] = one_minute_returns(tech)
    gold['gold_ret'] = one_minute_returns(gold)
    tech['tech_pos'] = np.arange(len(tech))  # position in tech's OWN bar series

    merged = tech[['timestamp', 'tech_pos', 'close', 'tech_ret']].merge(
        gold[['timestamp', 'gold_ret']], on='timestamp', how='inner'
    ).dropna()
    merged = merged.sort_values('timestamp').reset_index(drop=True)

    # contiguous aligned runs: consecutive timestamps exactly 1 minute apart
    d = merged['timestamp'].diff()
    contig = d == pd.Timedelta(minutes=1)
    merged['run_id'] = (contig != True).cumsum()
    return tech, merged


def split_runs(df):
    """Split into contiguous aligned runs (each row keeps its global position)."""
    runs = []
    for _, group in df.groupby('run_id'):
        runs.append(group)
    return runs


# =============================================================================
# CAND-105 — CROSS-ASSET LEAD-LAG ASYMMETRY
# =============================================================================

def run_cand105(tech, merged):
    print("\n" + "=" * 72)
    print("CAND-105: CROSS-ASSET LEAD-LAG ASYMMETRY")
    print("=" * 72)
    print(f"Frozen: lag={C105_LEAD_LAG} min, window={C105_WINDOW} aligned min, "
          f"tercile split, horizon={OUTCOME_HORIZON} tech bars, friction={FRICTION_BPS} bps")

    tech_close = tech['close'].values
    n_tech = len(tech)
    n_aligned = len(merged)

    runs = split_runs(merged)
    print(f"Aligned M1 bars (both assets, completed 1-min returns): {n_aligned}")
    print(f"Contiguous aligned runs: {len(runs)}")

    # Preallocate lead_asym and lag-0 corr for every aligned row
    asym = np.full(n_aligned, np.nan)
    corr0 = np.full(n_aligned, np.nan)
    valid_flag = np.zeros(n_aligned, dtype=bool)

    def rolling_pair_corr(x, y_shift1, window):
        """corr(x[p], y_shift1[p]) over trailing `window` values."""
        return x.rolling(window).corr(y_shift1)

    for run in runs:
        n_run = len(run)
        if n_run < C105_WINDOW + C105_LEAD_LAG + 2:
            continue
        gold_ret = run['gold_ret']
        tech_ret = run['tech_ret']
        # shifted series: g_lead[s] = gold[s+1], t_lead[s] = tech[s+1]
        g_lead = gold_ret.shift(-1)
        t_lead = tech_ret.shift(-1)

        # For signal at aligned index i:
        #   rho_g2t[i] = corr(gold[p], tech[p+1]) for p in [i-W, i-1]
        #              = rolling corr(gold, t_lead) at position i-1
        #   rho_t2g[i] = rolling corr(tech, g_lead) at position i-1
        rc_gt = rolling_pair_corr(gold_ret, t_lead, C105_WINDOW).values  # gold -> tech
        rc_tg = rolling_pair_corr(tech_ret, g_lead, C105_WINDOW).values  # tech -> gold
        rc_00 = rolling_pair_corr(gold_ret, tech_ret, C105_WINDOW).values  # lag-0 reference

        # signal bar index i must satisfy: i >= W (window) and the forward
        # outcome exists on the TECH series
        pos = run.index.values            # global aligned positions
        tpos = run['tech_pos'].values     # tech-series positions
        i_arr = np.arange(n_run)
        usable = (i_arr >= C105_WINDOW) & (tpos + OUTCOME_HORIZON < n_tech)
        sel = i_arr[usable] - 1           # rolling value position (i-1)
        gpos = pos[usable]
        a_gt = rc_gt[sel]
        a_tg = rc_tg[sel]
        ok = ~(np.isnan(a_gt) | np.isnan(a_tg))
        asym[gpos[ok]] = a_gt[ok] - a_tg[ok]
        c0 = rc_00[sel]
        c0_ok = ~np.isnan(c0)
        corr0[gpos[c0_ok]] = c0[c0_ok]
        valid_flag[gpos[ok]] = True

    n_valid = int(valid_flag.sum())
    print(f"Aligned bars with fully computable lead_asym + forward window: {n_valid}")

    v = asym[valid_flag]
    p10, p50, p90 = np.nanpercentile(v, 10), np.nanpercentile(v, 50), np.nanpercentile(v, 90)
    print(f"lead_asym percentiles: P10={p10:.4f} P50={p50:.4f} P90={p90:.4f}")

    lo, hi = np.nanpercentile(v, [C105_TERCILE[0] * 100, C105_TERCILE[1] * 100])
    print(f"Tercile boundaries: lo={lo:.4f} hi={hi:.4f}")

    all_idx = np.where(valid_flag)[0]
    treatment_raw = all_idx[asym[all_idx] > hi]
    control_raw = all_idx[asym[all_idx] < lo]
    print(f"Raw treatment (gold-lead top tercile): {len(treatment_raw)}")
    print(f"Raw control (tech-lead bottom tercile): {len(control_raw)}")

    def rearm(indices):
        if len(indices) == 0:
            return indices
        indices = np.sort(indices)
        kept = [indices[0]]
        for idx in indices[1:]:
            if idx - kept[-1] >= REARM_BARS:
                kept.append(idx)
        return np.array(kept)

    treatment_idx = rearm(treatment_raw)
    control_idx = rearm(control_raw)
    print(f"After rearm ({REARM_BARS} bars): treatment={len(treatment_idx)}, control={len(control_idx)}")

    all_tpos = merged['tech_pos'].values

    def forward_returns(align_positions):
        """Tech forward returns over OUTCOME_HORIZON tech bars, entry at signal-bar close."""
        if len(align_positions) == 0:
            return np.array([])
        tp = all_tpos[align_positions]
        valid = tp + OUTCOME_HORIZON < n_tech
        tp = tp[valid]
        if len(tp) == 0:
            return np.array([])
        entry = tech_close[tp]
        exit_ = tech_close[tp + OUTCOME_HORIZON]
        return (exit_ - entry) / entry * 10000

    treat_rets = forward_returns(treatment_idx)
    ctrl_rets = forward_returns(control_idx)

    if len(treat_rets) == 0 or len(ctrl_rets) == 0:
        print("ERROR: empty group")
        return None

    def stats(rets, label):
        net = rets - FRICTION_BPS
        out = {
            'N': len(rets),
            'gross_mean': float(np.mean(rets)),
            'gross_median': float(np.median(rets)),
            'net_mean': float(np.mean(net)),
            'net_median': float(np.median(net)),
            'wr_gross': float(np.mean(rets > 0) * 100),
            'wr_net': float(np.mean(net > 0) * 100),
            'std': float(np.std(rets)),
            'p10': float(np.percentile(rets, 10)),
            'p25': float(np.percentile(rets, 25)),
            'p75': float(np.percentile(rets, 75)),
            'p90': float(np.percentile(rets, 90)),
        }
        print(f"\n{label} (N={out['N']}):")
        print(f"  Gross Mean={out['gross_mean']:.2f} bps  Gross Median={out['gross_median']:.2f} bps")
        print(f"  Net Mean={out['net_mean']:.2f} bps  Net Median={out['net_median']:.2f} bps")
        print(f"  WR (gross>0)={out['wr_gross']:.1f}%  WR (net>0)={out['wr_net']:.1f}%")
        print(f"  Std={out['std']:.2f}  P10/P25/P75/P90="
              f"{out['p10']:.1f}/{out['p25']:.1f}/{out['p75']:.1f}/{out['p90']:.1f}")
        return out

    treat_stats = stats(treat_rets, "TREATMENT — GOLD-LEAD regime")
    ctrl_stats = stats(ctrl_rets, "CONTROL — TECH-LEAD regime")

    mean_delta = treat_stats['gross_mean'] - ctrl_stats['gross_mean']
    median_delta = treat_stats['gross_median'] - ctrl_stats['gross_median']
    wr_delta = treat_stats['wr_gross'] - ctrl_stats['wr_gross']

    print(f"\nDELTA (treatment minus control):")
    print(f"  Mean Delta={mean_delta:.2f} bps")
    print(f"  Median Delta={median_delta:.2f} bps")
    print(f"  WR Delta={wr_delta:.1f}%")

    t_corr0 = float(np.nanmean(corr0[treatment_idx])) if len(treatment_idx) else np.nan
    c_corr0 = float(np.nanmean(corr0[control_idx])) if len(control_idx) else np.nan
    print(f"\nContemporaneous (lag-0) corr reference over sampled bars:")
    print(f"  Treatment (gold-lead): {t_corr0:.4f}")
    print(f"  Control (tech-lead):   {c_corr0:.4f}")

    se = np.sqrt(np.var(treat_rets) / len(treat_rets) + np.var(ctrl_rets) / len(ctrl_rets))
    t_stat = mean_delta / se if se > 0 else np.nan
    print(f"  Welch t-statistic (descriptive): {t_stat:.2f}")

    return {
        'treatment': treat_stats,
        'control': ctrl_stats,
        'mean_delta': mean_delta,
        'median_delta': median_delta,
        'wr_delta': wr_delta,
        't_corr0': t_corr0,
        'c_corr0': c_corr0,
        't_stat': t_stat,
        'n_aligned': n_aligned,
        'n_valid': n_valid,
        'n_treatment': len(treat_rets),
        'n_control': len(ctrl_rets),
    }


# =============================================================================
# CAND-106 — INTRA-BAR PRICE DISTRIBUTION QUALITY
# =============================================================================

def run_cand106(tech):
    print("\n" + "=" * 72)
    print("CAND-106: INTRA-BAR PRICE DISTRIBUTION QUALITY")
    print("=" * 72)
    print(f"Frozen: body fraction |C-O|/(H-L), thresholds >=0.70 (conviction) / "
          f"<=0.30 (indecision), horizon={OUTCOME_HORIZON}, friction={FRICTION_BPS} bps")

    n_total = len(tech)
    rng = (tech['high'] - tech['low']).values
    body = (tech['close'] - tech['open']).abs().values
    with np.errstate(divide='ignore', invalid='ignore'):
        body_frac = np.where(rng > 0, body / np.where(rng > 0, rng, np.nan), np.nan)

    close = tech['close'].values
    valid = ~np.isnan(body_frac) & (np.arange(n_total) + OUTCOME_HORIZON < n_total)
    frac_valid = body_frac[valid]
    print(f"\nTotal M1 bars: {n_total}")
    print(f"Bars with computable body fraction AND forward window: {int(valid.sum())}")
    print(f"body_frac percentiles: P10={np.nanpercentile(frac_valid,10):.3f} "
          f"P50={np.nanpercentile(frac_valid,50):.3f} P90={np.nanpercentile(frac_valid,90):.3f}")

    cand_idx = np.arange(n_total)[valid]
    treatment_raw = cand_idx[body_frac[cand_idx] >= C106_HIGH_CONVICTION]
    control_raw = cand_idx[body_frac[cand_idx] <= C106_INDECISION]
    print(f"Raw treatment (conviction >= {C106_HIGH_CONVICTION}): {len(treatment_raw)}")
    print(f"Raw control (indecision <= {C106_INDECISION}): {len(control_raw)}")

    def rearm(indices):
        if len(indices) == 0:
            return indices
        indices = np.sort(indices)
        kept = [indices[0]]
        for idx in indices[1:]:
            if idx - kept[-1] >= REARM_BARS:
                kept.append(idx)
        return np.array(kept)

    treatment_idx = rearm(treatment_raw)
    control_idx = rearm(control_raw)
    print(f"After rearm ({REARM_BARS} bars): treatment={len(treatment_idx)}, control={len(control_idx)}")

    def forward_returns(indices):
        rets = []
        for i in indices:
            entry = close[i]
            exit_ = close[i + OUTCOME_HORIZON]
            rets.append((exit_ - entry) / entry * 10000)
        return np.array(rets)

    treat_rets = forward_returns(treatment_idx)
    ctrl_rets = forward_returns(control_idx)

    if len(treat_rets) == 0 or len(ctrl_rets) == 0:
        print("ERROR: empty group")
        return None

    def stats(rets, label):
        net = rets - FRICTION_BPS
        out = {
            'N': len(rets),
            'gross_mean': float(np.mean(rets)),
            'gross_median': float(np.median(rets)),
            'net_mean': float(np.mean(net)),
            'net_median': float(np.median(net)),
            'wr_gross': float(np.mean(rets > 0) * 100),
            'wr_net': float(np.mean(net > 0) * 100),
            'std': float(np.std(rets)),
            'p10': float(np.percentile(rets, 10)),
            'p25': float(np.percentile(rets, 25)),
            'p75': float(np.percentile(rets, 75)),
            'p90': float(np.percentile(rets, 90)),
        }
        print(f"\n{label} (N={out['N']}):")
        print(f"  Gross Mean={out['gross_mean']:.2f} bps  Gross Median={out['gross_median']:.2f} bps")
        print(f"  Net Mean={out['net_mean']:.2f} bps  Net Median={out['net_median']:.2f} bps")
        print(f"  WR (gross>0)={out['wr_gross']:.1f}%  WR (net>0)={out['wr_net']:.1f}%")
        print(f"  Std={out['std']:.2f}  P10/P25/P75/P90="
              f"{out['p10']:.1f}/{out['p25']:.1f}/{out['p75']:.1f}/{out['p90']:.1f}")
        return out

    treat_stats = stats(treat_rets, "TREATMENT — HIGH CONVICTION bars")
    ctrl_stats = stats(ctrl_rets, "CONTROL — INDECISION bars")

    mean_delta = treat_stats['gross_mean'] - ctrl_stats['gross_mean']
    median_delta = treat_stats['gross_median'] - ctrl_stats['gross_median']
    wr_delta = treat_stats['wr_gross'] - ctrl_stats['wr_gross']

    print(f"\nDELTA (treatment minus control):")
    print(f"  Mean Delta={mean_delta:.2f} bps")
    print(f"  Median Delta={median_delta:.2f} bps")
    print(f"  WR Delta={wr_delta:.1f}%")

    se = np.sqrt(np.var(treat_rets) / len(treat_rets) + np.var(ctrl_rets) / len(ctrl_rets))
    t_stat = mean_delta / se if se > 0 else np.nan
    print(f"  Welch t-statistic (descriptive): {t_stat:.2f}")

    # Direction decomposition (diagnostic only): does any separation merely
    # reflect bar direction (up vs down body)?
    print(f"\nDirection decomposition (diagnostic):")
    up_mask_t = (tech['close'].values[treatment_idx] > tech['open'].values[treatment_idx])
    dn_mask_t = ~up_mask_t
    if up_mask_t.sum() > 10 and dn_mask_t.sum() > 10:
        up_t = treat_rets[up_mask_t]
        dn_t = treat_rets[dn_mask_t]
        print(f"  Treatment UP bars:   N={len(up_t)}, mean={np.mean(up_t):.2f} bps")
        print(f"  Treatment DOWN bars: N={len(dn_t)}, mean={np.mean(dn_t):.2f} bps")
    up_mask_c = (tech['close'].values[control_idx] > tech['open'].values[control_idx])
    dn_mask_c = ~up_mask_c
    if up_mask_c.sum() > 10 and dn_mask_c.sum() > 10:
        up_c = ctrl_rets[up_mask_c]
        dn_c = ctrl_rets[dn_mask_c]
        print(f"  Control UP bars:   N={len(up_c)}, mean={np.mean(up_c):.2f} bps")
        print(f"  Control DOWN bars: N={len(dn_c)}, mean={np.mean(dn_c):.2f} bps")

    return {
        'treatment': treat_stats,
        'control': ctrl_stats,
        'mean_delta': mean_delta,
        'median_delta': median_delta,
        'wr_delta': wr_delta,
        't_stat': t_stat,
        'n_total': n_total,
        'n_valid': int(valid.sum()),
        'n_treatment': len(treat_rets),
        'n_control': len(ctrl_rets),
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    t0 = time.time()

    tech, merged = align_assets()
    print(f"Loaded tech M1: {len(tech)} bars; aligned overlap bars: {len(merged)}")

    res105 = run_cand105(tech, merged)
    res106 = run_cand106(tech)

    print(f"\nTotal elapsed: {time.time() - t0:.1f}s")
