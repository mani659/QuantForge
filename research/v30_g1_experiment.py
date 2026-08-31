"""
V30 G1 — ECONOMIC PLAUSIBILITY SCREEN
CAND-089: Acceptance Velocity Decay
CAND-091: Cumulative Directional Exhaustion

Frozen definitions from V30 G0 and V30 G0 Integrity Audit.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time

# =============================================================================
# FROZEN PARAMETERS — DO NOT MODIFY
# =============================================================================

# Common
STRUCTURAL_LOOKBACK = 20
BREAKOUT_THRESHOLD = 3  # bps
HOLDING_PERIOD = 60  # bars on M1 = 60 min
FRICTION_BPS = 2.0
MARKET = "USATECHIDXUSD"
TIMEFRAME = "M1"

# CAND-089 specific
# Acceptance velocity = rate of range convergence before a break
# Measured over the PRECEDING_WINDOW bars before each break
PRECEDING_WINDOW = 20  # bars before the break to measure velocity
VELOCITY_DECAY_WINDOW = 3  # sub-windows to compare (early vs late)

# CAND-091 specific
EXHAUSTION_WINDOW = 100  # bars

# Rearm
REARM_BARS = 60


def load_data():
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "m1" / "USATECHIDXUSD_M1.csv"
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    df.columns = [c.lower().strip() for c in df.columns]
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
    print(f"Data shape: {df.shape}")
    print(f"Date range: {df.index[0]} to {df.index[-1]}")
    return df


def compute_structural_levels(df):
    df = df.copy()
    df['struct_high'] = df['high'].rolling(STRUCTURAL_LOOKBACK).max().shift(1)
    df['struct_low'] = df['low'].rolling(STRUCTURAL_LOOKBACK).min().shift(1)
    return df


def detect_breaks_vectorized(df):
    """Detect structural level breaks (up and down)."""
    close = df['close'].values
    struct_h = df['struct_high'].values
    struct_l = df['struct_low'].values
    n = len(close)
    struct_h_bps = struct_h * BREAKOUT_THRESHOLD / 10000.0
    struct_l_bps = struct_l * BREAKOUT_THRESHOLD / 10000.0
    up_break = (close > struct_h + struct_h_bps)
    dn_break = (close < struct_l - struct_l_bps)
    return np.where(up_break)[0], np.where(dn_break)[0]


def apply_rearm(indices, n):
    if len(indices) == 0:
        return indices
    filtered = [indices[0]]
    for idx in indices[1:]:
        if idx - filtered[-1] >= REARM_BARS:
            filtered.append(idx)
    return np.array(filtered)


# =============================================================================
# CAND-089: ACCEPTANCE VELOCITY DECAY
# =============================================================================

def run_cand089(df):
    """
    CAND-089: Acceptance Velocity Decay
    
    Simplified approach: For each structural break, measure the "acceptance
    velocity" by looking at the range convergence in the bars BEFORE the break.
    
    If the range was converging toward the level before the break → high velocity
    If the range was stable/expanding before the break → low velocity
    
    Decay = late-window range is WIDER than early-window range (velocity declining)
    """
    print("\n" + "="*70)
    print("CAND-089: ACCEPTANCE VELOCITY DECAY")
    print("="*70)
    
    df = compute_structural_levels(df)
    
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    struct_h = df['struct_high'].values
    struct_l = df['struct_low'].values
    n = len(close)
    
    # Detect breaks
    print("\nStep 1: Detecting structural level breaks...")
    up_breaks, dn_breaks = detect_breaks_vectorized(df)
    print(f"  Raw up breaks: {len(up_breaks)}, Raw down breaks: {len(dn_breaks)}")
    
    up_breaks = apply_rearm(up_breaks, n)
    dn_breaks = apply_rearm(dn_breaks, n)
    print(f"  After rearm: up={len(up_breaks)}, down={len(dn_breaks)}")
    
    # For each break, compute acceptance velocity in the preceding window
    print("\nStep 2: Computing acceptance velocity at each break...")
    t0 = time.time()
    
    bar_range = high - low  # range of each bar
    
    # Velocity = slope of bar_range regression over preceding window
    # Negative slope = range shrinking = high acceptance (price stabilizing)
    # Positive slope = range expanding = low acceptance
    
    events = []
    for b_idx in np.concatenate([up_breaks, dn_breaks]):
        if b_idx < PRECEDING_WINDOW + 2:
            continue
        
        # Direction: +1 for up break, -1 for down break
        direction = 1 if b_idx in up_breaks else -1
        
        # Preceding window ranges
        start = max(0, b_idx - PRECEDING_WINDOW)
        window_ranges = bar_range[start:b_idx]
        
        if len(window_ranges) < 5:
            continue
        
        # Mean range in the preceding window
        mean_range = window_ranges.mean()
        if mean_range <= 0:
            continue
        
        # Linear regression slope of range over time
        x = np.arange(len(window_ranges), dtype=float)
        slope = np.polyfit(x, window_ranges, 1)[0]
        
        # Normalized velocity: slope / mean_range
        # Negative = range shrinking (accepting), Positive = range expanding
        velocity = slope / mean_range
        
        # Decay: compare early half vs late half velocity
        mid = len(window_ranges) // 2
        if mid < 2:
            continue
        
        early_range = window_ranges[:mid]
        late_range = window_ranges[mid:]
        early_mean = early_range.mean()
        late_mean = late_range.mean()
        
        # Decay = late_mean > early_mean means range is expanding → velocity declining
        decay = (late_mean - early_mean) / max(mean_range, 1e-12)
        
        # Structural level proximity at break time
        if direction == 1:
            level = struct_h[b_idx] if not np.isnan(struct_h[b_idx]) else close[b_idx]
        else:
            level = struct_l[b_idx] if not np.isnan(struct_l[b_idx]) else close[b_idx]
        
        events.append({
            'break_idx': int(b_idx),
            'direction': direction,
            'velocity': velocity,
            'decay': decay,
            'mean_range': mean_range,
            'early_range': early_mean,
            'late_range': late_mean,
        })
    
    print(f"  Total events with velocity: {len(events)} ({time.time()-t0:.1f}s)")
    
    # Classify: decaying velocity (decay > 0 = late range wider = velocity declining)
    decaying = [e for e in events if e['decay'] > 0]
    stable = [e for e in events if e['decay'] <= 0]
    
    print(f"  Decaying velocity: {len(decaying)} ({len(decaying)/max(len(events),1)*100:.1f}%)")
    print(f"  Stable velocity:   {len(stable)} ({len(stable)/max(len(events),1)*100:.1f}%)")
    
    # Compute forward returns
    print("\nStep 3: Computing forward returns...")
    
    def compute_returns(event_list):
        results = []
        for e in event_list:
            b_idx = e['break_idx']
            d = e['direction']
            if b_idx + HOLDING_PERIOD < n:
                entry = close[b_idx]
                exit_p = close[b_idx + HOLDING_PERIOD]
                gross_bps = (exit_p - entry) / entry * 10000.0 * d
                net_bps = gross_bps - FRICTION_BPS
                results.append({**e, 'gross_bps': gross_bps, 'net_bps': net_bps})
        return pd.DataFrame(results)
    
    decaying_df = compute_returns(decaying)
    stable_df = compute_returns(stable)
    
    # Report
    print("\n" + "-"*70)
    print("CAND-089 RESULTS")
    print("-"*70)
    
    if len(decaying_df) == 0 or len(stable_df) == 0:
        print("  INSUFFICIENT DATA — one or both groups empty")
        return None
    
    total_days = (df.index[-1] - df.index[0]).days
    years = total_days / 365.25
    
    print(f"\n  Coverage: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')} ({years:.1f} years)")
    
    print(f"\n  Population:")
    print(f"    Decaying velocity (treatment): N = {len(decaying_df)}")
    print(f"    Stable velocity (control):     N = {len(stable_df)}")
    
    # Economics
    for label, subdf in [("Decaying (Treatment)", decaying_df), ("Stable (Control)", stable_df)]:
        print(f"\n  Economics — {label}:")
        print(f"    Gross Mean:   {subdf['gross_bps'].mean():+.2f} bps")
        print(f"    Gross Median: {subdf['gross_bps'].median():+.2f} bps")
        print(f"    Net Mean:     {subdf['net_bps'].mean():+.2f} bps")
        print(f"    Net Median:   {subdf['net_bps'].median():+.2f} bps")
        print(f"    Win Rate:     {(subdf['net_bps'] > 0).mean()*100:.1f}%")
        print(f"    Std Dev:      {subdf['net_bps'].std():.2f} bps")
    
    # Delta
    delta_mean = decaying_df['net_bps'].mean() - stable_df['net_bps'].mean()
    delta_median = decaying_df['net_bps'].median() - stable_df['net_bps'].median()
    print(f"\n  Conditional Delta (Decaying - Stable):")
    print(f"    Mean Delta:   {delta_mean:+.2f} bps")
    print(f"    Median Delta: {delta_median:+.2f} bps")
    print(f"    WR Delta:     {(decaying_df['net_bps'] > 0).mean() - (stable_df['net_bps'] > 0).mean():+.1%}")
    
    # Frequency
    print(f"\n  Frequency:")
    print(f"    Decaying events/year: {len(decaying_df) / years:.0f}")
    print(f"    Stable events/year:   {len(stable_df) / years:.0f}")
    
    # Distribution
    for label, subdf in [("Decaying", decaying_df), ("Stable", stable_df)]:
        print(f"\n  Distribution — {label}:")
        for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
            print(f"    P{int(q*100):02d}: {subdf['net_bps'].quantile(q):+.2f} bps")
    
    # Tail analysis
    top10_decaying = decaying_df.nlargest(max(1, len(decaying_df)//10), 'net_bps')
    top10_stable = stable_df.nlargest(max(1, len(stable_df)//10), 'net_bps')
    print(f"\n  Top 10% contribution:")
    d_sum = decaying_df['net_bps'].sum()
    s_sum = stable_df['net_bps'].sum()
    print(f"    Decaying: {top10_decaying['net_bps'].sum():+.1f} of {d_sum:+.1f} total ({top10_decaying['net_bps'].sum() / max(abs(d_sum), 0.01) * 100:.1f}% share)")
    print(f"    Stable:   {top10_stable['net_bps'].sum():+.1f} of {s_sum:+.1f} total ({top10_stable['net_bps'].sum() / max(abs(s_sum), 0.01) * 100:.1f}% share)")
    
    # Exclude best event
    for label, subdf in [("Decaying", decaying_df), ("Stable", stable_df)]:
        if len(subdf) > 1:
            excl_best = subdf.nlargest(1, 'net_bps').index
            print(f"  Exclude-best-event mean ({label}): {subdf.drop(excl_best)['net_bps'].mean():+.2f} bps")
    
    # Worst event
    print(f"\n  Worst event:")
    print(f"    Decaying: {decaying_df['net_bps'].min():+.2f} bps")
    print(f"    Stable:   {stable_df['net_bps'].min():+.2f} bps")
    
    # Direction breakdown
    print(f"\n  Direction-specific:")
    for label, subdf in [("Decaying", decaying_df), ("Stable", stable_df)]:
        longs = subdf[subdf['direction'] == 1]
        shorts = subdf[subdf['direction'] == -1]
        if len(longs) > 0:
            print(f"    {label} Long:  N={len(longs):4d}, Mean={longs['net_bps'].mean():+.2f}, Median={longs['net_bps'].median():+.2f}, WR={longs['net_bps'].gt(0).mean()*100:.1f}%")
        if len(shorts) > 0:
            print(f"    {label} Short: N={len(shorts):4d}, Mean={shorts['net_bps'].mean():+.2f}, Median={shorts['net_bps'].median():+.2f}, WR={shorts['net_bps'].gt(0).mean()*100:.1f}%")
    
    # Decay magnitude analysis (exploratory)
    print(f"\n  Decay magnitude (exploratory — not a filter):")
    decay_values = [e['decay'] for e in decaying]
    if decay_values:
        print(f"    Mean decay:   {np.mean(decay_values):.4f}")
        print(f"    Median decay: {np.median(decay_values):.4f}")
        print(f"    Std decay:    {np.std(decay_values):.4f}")
        print(f"    P25: {np.percentile(decay_values, 25):.4f}")
        print(f"    P75: {np.percentile(decay_values, 75):.4f}")
    
    return {
        'treatment_n': len(decaying_df),
        'control_n': len(stable_df),
        'treatment_net_mean': decaying_df['net_bps'].mean(),
        'treatment_net_median': decaying_df['net_bps'].median(),
        'treatment_wr': (decaying_df['net_bps'] > 0).mean(),
        'control_net_mean': stable_df['net_bps'].mean(),
        'control_net_median': stable_df['net_bps'].median(),
        'control_wr': (stable_df['net_bps'] > 0).mean(),
        'delta_mean': delta_mean,
        'delta_median': delta_median,
        'years': years,
    }


# =============================================================================
# CAND-091: CUMULATIVE DIRECTIONAL EXHAUSTION
# =============================================================================

def compute_cumulative_distance(df):
    """Vectorized rolling cumulative directional distance."""
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    n = len(close)
    
    returns = np.zeros(n)
    returns[1:] = (close[1:] - close[:-1]) / close[:-1]
    
    # Rolling cumulative return
    cum_sum = np.cumsum(returns)
    cum_return = np.zeros(n)
    cum_return[EXHAUSTION_WINDOW:] = cum_sum[EXHAUSTION_WINDOW:] - cum_sum[:n - EXHAUSTION_WINDOW]
    
    # Rolling range
    rolling_high = pd.Series(high).rolling(EXHAUSTION_WINDOW).max().values
    rolling_low = pd.Series(low).rolling(EXHAUSTION_WINDOW).min().values
    
    rolling_range = rolling_high - rolling_low
    with np.errstate(divide='ignore', invalid='ignore'):
        rolling_range_bps = np.where(rolling_range > 0, rolling_range / close * 10000.0, 0)
    
    cum_return_bps = cum_return * 10000.0
    with np.errstate(divide='ignore', invalid='ignore'):
        dist_to_range = np.where(rolling_range_bps > 0, cum_return_bps / rolling_range_bps, 0)
    
    dominant_dir = np.sign(cum_return)
    
    # Trend consistency (simplified vectorized)
    pos_ret = (returns > 0).astype(float)
    neg_ret = (returns < 0).astype(float)
    cum_pos = np.cumsum(pos_ret)
    cum_neg = np.cumsum(neg_ret)
    trend_consistency = np.full(n, 0.5)
    for i in range(EXHAUSTION_WINDOW, n):
        if dominant_dir[i] > 0:
            trend_consistency[i] = (cum_pos[i] - cum_pos[i - EXHAUSTION_WINDOW]) / EXHAUSTION_WINDOW
        elif dominant_dir[i] < 0:
            trend_consistency[i] = (cum_neg[i] - cum_neg[i - EXHAUSTION_WINDOW]) / EXHAUSTION_WINDOW
    
    return cum_return_bps, dist_to_range, trend_consistency, dominant_dir


def run_cand091(df):
    """CAND-091: Cumulative Directional Exhaustion."""
    print("\n" + "="*70)
    print("CAND-091: CUMULATIVE DIRECTIONAL EXHAUSTION")
    print("="*70)
    
    df = compute_structural_levels(df)
    
    close = df['close'].values
    n = len(close)
    
    print("\nStep 1: Computing cumulative directional distance...")
    t0 = time.time()
    cum_return_bps, dist_to_range, trend_consistency, dominant_dir = compute_cumulative_distance(df)
    print(f"  Done ({time.time()-t0:.1f}s)")
    
    print("Step 2: Detecting structural level breaks...")
    up_breaks, dn_breaks = detect_breaks_vectorized(df)
    print(f"  Raw up breaks: {len(up_breaks)}, Raw down breaks: {len(dn_breaks)}")
    up_breaks = apply_rearm(up_breaks, n)
    dn_breaks = apply_rearm(dn_breaks, n)
    print(f"  After rearm: up={len(up_breaks)}, down={len(dn_breaks)}")
    
    # Exhaustion threshold: 70th percentile of |cumulative distance|
    abs_cum_dist = np.abs(cum_return_bps)
    valid_mask = abs_cum_dist > 0
    exhaustion_threshold = np.percentile(abs_cum_dist[valid_mask], 70)
    print(f"\n  Exhaustion threshold (70th pct): {exhaustion_threshold:.1f} bps")
    
    print("Step 3: Computing forward returns for both groups...")
    t0 = time.time()
    
    exhausted_results = []
    non_exhausted_results = []
    
    all_breaks_combined = []
    for b in up_breaks:
        all_breaks_combined.append((b, 1))
    for b in dn_breaks:
        all_breaks_combined.append((b, -1))
    all_breaks_combined.sort()
    
    for b_idx, direction in all_breaks_combined:
        if b_idx + HOLDING_PERIOD >= n:
            continue
        
        exhaustion_level = abs_cum_dist[b_idx]
        cum_dist = cum_return_bps[b_idx]
        dom_dir = dominant_dir[b_idx]
        
        entry = close[b_idx]
        exit_price = close[b_idx + HOLDING_PERIOD]
        gross_bps = (exit_price - entry) / entry * 10000.0 * direction
        net_bps = gross_bps - FRICTION_BPS
        
        event = {
            'break_idx': int(b_idx),
            'direction': direction,
            'exhaustion_level': exhaustion_level,
            'cum_dist_bps': cum_dist,
            'dominant_dir': dom_dir,
            'dist_to_range': dist_to_range[b_idx],
            'trend_consistency': trend_consistency[b_idx],
            'gross_bps': gross_bps,
            'net_bps': net_bps
        }
        
        if exhaustion_level >= exhaustion_threshold:
            exhausted_results.append(event)
        else:
            non_exhausted_results.append(event)
    
    exhausted_df = pd.DataFrame(exhausted_results)
    non_exhausted_df = pd.DataFrame(non_exhausted_results)
    
    print(f"  Exhausted:     N = {len(exhausted_df)} ({time.time()-t0:.1f}s)")
    print(f"  Non-exhausted: N = {len(non_exhausted_df)}")
    
    print("\n" + "-"*70)
    print("CAND-091 RESULTS")
    print("-"*70)
    
    if len(exhausted_df) == 0 or len(non_exhausted_df) == 0:
        print("  INSUFFICIENT DATA")
        return None
    
    total_days = (df.index[-1] - df.index[0]).days
    years = total_days / 365.25
    
    print(f"\n  Coverage: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')} ({years:.1f} years)")
    
    print(f"\n  Population:")
    print(f"    Exhausted (treatment):     N = {len(exhausted_df)}")
    print(f"    Non-exhausted (control):   N = {len(non_exhausted_df)}")
    
    print(f"\n  Direction breakdown:")
    print(f"    Exhausted:     long={sum(exhausted_df['direction']==1)}, short={sum(exhausted_df['direction']==-1)}")
    print(f"    Non-exhausted: long={sum(non_exhausted_df['direction']==1)}, short={sum(non_exhausted_df['direction']==-1)}")
    
    for label, subdf in [("Exhausted (Treatment)", exhausted_df), ("Non-exhausted (Control)", non_exhausted_df)]:
        print(f"\n  Economics — {label}:")
        print(f"    Gross Mean:   {subdf['gross_bps'].mean():+.2f} bps")
        print(f"    Gross Median: {subdf['gross_bps'].median():+.2f} bps")
        print(f"    Net Mean:     {subdf['net_bps'].mean():+.2f} bps")
        print(f"    Net Median:   {subdf['net_bps'].median():+.2f} bps")
        print(f"    Win Rate:     {(subdf['net_bps'] > 0).mean()*100:.1f}%")
        print(f"    Std Dev:      {subdf['net_bps'].std():.2f} bps")
    
    delta_mean = exhausted_df['net_bps'].mean() - non_exhausted_df['net_bps'].mean()
    delta_median = exhausted_df['net_bps'].median() - non_exhausted_df['net_bps'].median()
    print(f"\n  Conditional Delta (Exhausted - Non-exhausted):")
    print(f"    Mean Delta:   {delta_mean:+.2f} bps")
    print(f"    Median Delta: {delta_median:+.2f} bps")
    print(f"    WR Delta:     {(exhausted_df['net_bps'] > 0).mean() - (non_exhausted_df['net_bps'] > 0).mean():+.1%}")
    
    print(f"\n  Frequency:")
    print(f"    Exhausted events/year:     {len(exhausted_df) / years:.0f}")
    print(f"    Non-exhausted events/year: {len(non_exhausted_df) / years:.0f}")
    
    for label, subdf in [("Exhausted", exhausted_df), ("Non-exhausted", non_exhausted_df)]:
        print(f"\n  Distribution — {label}:")
        for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
            print(f"    P{int(q*100):02d}: {subdf['net_bps'].quantile(q):+.2f} bps")
    
    top10_exh = exhausted_df.nlargest(max(1, len(exhausted_df)//10), 'net_bps')
    top10_non = non_exhausted_df.nlargest(max(1, len(non_exhausted_df)//10), 'net_bps')
    print(f"\n  Top 10% contribution:")
    e_sum = exhausted_df['net_bps'].sum()
    n_sum = non_exhausted_df['net_bps'].sum()
    print(f"    Exhausted:     {top10_exh['net_bps'].sum():+.1f} of {e_sum:+.1f} total")
    print(f"    Non-exhausted: {top10_non['net_bps'].sum():+.1f} of {n_sum:+.1f} total")
    
    for label, subdf in [("Exhausted", exhausted_df), ("Non-exhausted", non_exhausted_df)]:
        if len(subdf) > 1:
            excl_best = subdf.nlargest(1, 'net_bps').index
            print(f"  Exclude-best-event mean ({label}): {subdf.drop(excl_best)['net_bps'].mean():+.2f} bps")
    
    print(f"\n  Worst event:")
    print(f"    Exhausted:     {exhausted_df['net_bps'].min():+.2f} bps")
    print(f"    Non-exhausted: {non_exhausted_df['net_bps'].min():+.2f} bps")
    
    print(f"\n  Direction-specific:")
    for label, subdf in [("Exhausted", exhausted_df), ("Non-exhausted", non_exhausted_df)]:
        longs = subdf[subdf['direction'] == 1]
        shorts = subdf[subdf['direction'] == -1]
        if len(longs) > 0:
            print(f"    {label} Long:  N={len(longs):4d}, Mean={longs['net_bps'].mean():+.2f}, Median={longs['net_bps'].median():+.2f}, WR={longs['net_bps'].gt(0).mean()*100:.1f}%")
        if len(shorts) > 0:
            print(f"    {label} Short: N={len(shorts):4d}, Mean={shorts['net_bps'].mean():+.2f}, Median={shorts['net_bps'].median():+.2f}, WR={shorts['net_bps'].gt(0).mean()*100:.1f}%")
    
    return {
        'treatment_n': len(exhausted_df),
        'control_n': len(non_exhausted_df),
        'treatment_net_mean': exhausted_df['net_bps'].mean(),
        'treatment_net_median': exhausted_df['net_bps'].median(),
        'treatment_wr': (exhausted_df['net_bps'] > 0).mean(),
        'control_net_mean': non_exhausted_df['net_bps'].mean(),
        'control_net_median': non_exhausted_df['net_bps'].median(),
        'control_wr': (non_exhausted_df['net_bps'] > 0).mean(),
        'delta_mean': delta_mean,
        'delta_median': delta_median,
        'years': years,
        'exhaustion_threshold': exhaustion_threshold,
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    df = load_data()
    
    print("\n" + "#"*70)
    print("# V30 G1 — ECONOMIC PLAUSIBILITY SCREEN")
    print("# CAND-089 + CAND-091")
    print("#"*70)
    
    cand089_results = run_cand089(df.copy())
    cand091_results = run_cand091(df.copy())
    
    print("\n\n" + "#"*70)
    print("# SUMMARY")
    print("#"*70)
    
    if cand089_results:
        r = cand089_results
        print(f"\nCAND-089:")
        print(f"  Treatment N={r['treatment_n']}, Control N={r['control_n']}")
        print(f"  Treatment Net Mean={r['treatment_net_mean']:+.2f} bps, Median={r['treatment_net_median']:+.2f} bps, WR={r['treatment_wr']*100:.1f}%")
        print(f"  Control   Net Mean={r['control_net_mean']:+.2f} bps, Median={r['control_net_median']:+.2f} bps, WR={r['control_wr']*100:.1f}%")
        print(f"  Delta Mean={r['delta_mean']:+.2f} bps, Median={r['delta_median']:+.2f} bps")
    else:
        print("\nCAND-089: INSUFFICIENT DATA")
    
    if cand091_results:
        r = cand091_results
        print(f"\nCAND-091:")
        print(f"  Treatment N={r['treatment_n']}, Control N={r['control_n']}")
        print(f"  Treatment Net Mean={r['treatment_net_mean']:+.2f} bps, Median={r['treatment_net_median']:+.2f} bps, WR={r['treatment_wr']*100:.1f}%")
        print(f"  Control   Net Mean={r['control_net_mean']:+.2f} bps, Median={r['control_net_median']:+.2f} bps, WR={r['control_wr']*100:.1f}%")
        print(f"  Delta Mean={r['delta_mean']:+.2f} bps, Median={r['delta_median']:+.2f} bps")
    else:
        print("\nCAND-091: INSUFFICIENT DATA")
