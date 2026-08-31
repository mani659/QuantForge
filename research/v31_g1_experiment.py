"""
V31 G1 — ECONOMIC PLAUSIBILITY SCREEN
CAND-092: Event-Information Decay
CAND-093: Price-Discovery Friction Gradient

Frozen definitions from V31 G0.
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
# CAND-092: EVENT-INFORMATION DECAY
# =============================================================================

def run_cand092(df):
    """
    CAND-092: Event-Information Decay

    Hypothesis: Structural events occurring during high-information-remaining
    conditions (recent prior event) produce different downstream economics
    than events during low-information-remaining conditions (older prior event).
    """
    print("\n" + "="*70)
    print("CAND-092: EVENT-INFORMATION DECAY")
    print("="*70)

    df = compute_structural_levels(df)
    close = df['close'].values
    n = len(close)

    # Step 1: Detect all structural breaks
    print("\nStep 1: Detecting structural level breaks...")
    up_breaks, dn_breaks = detect_breaks_vectorized(df)
    print(f"  Raw up breaks: {len(up_breaks)}, Raw down breaks: {len(dn_breaks)}")

    # Combine and sort all breaks (before rearm, to compute time-since-event)
    all_breaks_raw = np.sort(np.concatenate([up_breaks, dn_breaks]))
    break_direction = {}
    for b in up_breaks:
        break_direction[b] = 1
    for b in dn_breaks:
        break_direction[b] = -1

    print(f"  Total raw breaks: {len(all_breaks_raw)}")

    # Step 2: Apply rearm
    all_breaks_rearm = apply_rearm(all_breaks_raw, n)
    print(f"  After rearm: {len(all_breaks_rearm)}")

    # Step 3: Compute time since prior event for each break
    print("\nStep 2: Computing time since prior event...")
    t0 = time.time()

    events = []
    for i, b_idx in enumerate(all_breaks_rearm):
        if b_idx + HOLDING_PERIOD >= n:
            continue

        # Time since previous break
        if i > 0:
            time_since = b_idx - all_breaks_rearm[i - 1]
        else:
            time_since = b_idx  # first break — use distance from start

        direction = break_direction[b_idx]

        # Forward returns
        entry = close[b_idx]
        exit_p = close[b_idx + HOLDING_PERIOD]
        gross_bps = (exit_p - entry) / entry * 10000.0 * direction
        net_bps = gross_bps - FRICTION_BPS

        events.append({
            'break_idx': int(b_idx),
            'direction': direction,
            'time_since': int(time_since),
            'gross_bps': gross_bps,
            'net_bps': net_bps,
        })

    print(f"  Events with time-since: {len(events)} ({time.time()-t0:.1f}s)")

    events_df = pd.DataFrame(events)

    # Step 4: Classify by median time-since-event
    median_time = events_df['time_since'].median()
    print(f"\n  Median time-since-event: {median_time:.0f} bars")

    high_info = events_df[events_df['time_since'] < median_time]  # recent = high info remaining
    low_info = events_df[events_df['time_since'] >= median_time]  # old = low info remaining

    print(f"  High information remaining (recent): N = {len(high_info)}")
    print(f"  Low information remaining (old):     N = {len(low_info)}")

    # Step 5: Report results
    print("\n" + "-"*70)
    print("CAND-092 RESULTS")
    print("-"*70)

    if len(high_info) == 0 or len(low_info) == 0:
        print("  INSUFFICIENT DATA")
        return None

    total_days = (df.index[-1] - df.index[0]).days
    years = total_days / 365.25

    print(f"\n  Coverage: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')} ({years:.1f} years)")

    for label, subdf in [("High Info Remaining (Treatment)", high_info), ("Low Info Remaining (Control)", low_info)]:
        print(f"\n  Economics — {label}:")
        print(f"    Gross Mean:   {subdf['gross_bps'].mean():+.2f} bps")
        print(f"    Gross Median: {subdf['gross_bps'].median():+.2f} bps")
        print(f"    Net Mean:     {subdf['net_bps'].mean():+.2f} bps")
        print(f"    Net Median:   {subdf['net_bps'].median():+.2f} bps")
        print(f"    Win Rate:     {(subdf['net_bps'] > 0).mean()*100:.1f}%")
        print(f"    Std Dev:      {subdf['net_bps'].std():.2f} bps")

    delta_mean = high_info['net_bps'].mean() - low_info['net_bps'].mean()
    delta_median = high_info['net_bps'].median() - low_info['net_bps'].median()
    print(f"\n  Conditional Delta (High - Low Info):")
    print(f"    Mean Delta:   {delta_mean:+.2f} bps")
    print(f"    Median Delta: {delta_median:+.2f} bps")
    print(f"    WR Delta:     {(high_info['net_bps'] > 0).mean() - (low_info['net_bps'] > 0).mean():+.1%}")

    print(f"\n  Frequency:")
    print(f"    High info events/year: {len(high_info) / years:.0f}")
    print(f"    Low info events/year:  {len(low_info) / years:.0f}")

    for label, subdf in [("High Info", high_info), ("Low Info", low_info)]:
        print(f"\n  Distribution — {label}:")
        for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
            print(f"    P{int(q*100):02d}: {subdf['net_bps'].quantile(q):+.2f} bps")

    top10_high = high_info.nlargest(max(1, len(high_info)//10), 'net_bps')
    top10_low = low_info.nlargest(max(1, len(low_info)//10), 'net_bps')
    print(f"\n  Top 10% contribution:")
    h_sum = high_info['net_bps'].sum()
    l_sum = low_info['net_bps'].sum()
    print(f"    High info: {top10_high['net_bps'].sum():+.1f} of {h_sum:+.1f} total")
    print(f"    Low info:  {top10_low['net_bps'].sum():+.1f} of {l_sum:+.1f} total")

    for label, subdf in [("High Info", high_info), ("Low Info", low_info)]:
        if len(subdf) > 1:
            excl_best = subdf.nlargest(1, 'net_bps').index
            print(f"  Exclude-best-event mean ({label}): {subdf.drop(excl_best)['net_bps'].mean():+.2f} bps")

    print(f"\n  Worst event:")
    print(f"    High info: {high_info['net_bps'].min():+.2f} bps")
    print(f"    Low info:  {low_info['net_bps'].min():+.2f} bps")

    # Direction breakdown
    print(f"\n  Direction-specific:")
    for label, subdf in [("High Info", high_info), ("Low Info", low_info)]:
        longs = subdf[subdf['direction'] == 1]
        shorts = subdf[subdf['direction'] == -1]
        if len(longs) > 0:
            print(f"    {label} Long:  N={len(longs):4d}, Mean={longs['net_bps'].mean():+.2f}, Median={longs['net_bps'].median():+.2f}, WR={longs['net_bps'].gt(0).mean()*100:.1f}%")
        if len(shorts) > 0:
            print(f"    {label} Short: N={len(shorts):4d}, Mean={shorts['net_bps'].mean():+.2f}, Median={shorts['net_bps'].median():+.2f}, WR={shorts['net_bps'].gt(0).mean()*100:.1f}%")

    # Time-since distribution (exploratory)
    print(f"\n  Time-since-event distribution (exploratory):")
    print(f"    Mean:   {events_df['time_since'].mean():.0f} bars")
    print(f"    Median: {events_df['time_since'].median():.0f} bars")
    print(f"    P25:    {events_df['time_since'].quantile(0.25):.0f} bars")
    print(f"    P75:    {events_df['time_since'].quantile(0.75):.0f} bars")

    return {
        'treatment_n': len(high_info),
        'control_n': len(low_info),
        'treatment_net_mean': high_info['net_bps'].mean(),
        'treatment_net_median': high_info['net_bps'].median(),
        'treatment_wr': (high_info['net_bps'] > 0).mean(),
        'control_net_mean': low_info['net_bps'].mean(),
        'control_net_median': low_info['net_bps'].median(),
        'control_wr': (low_info['net_bps'] > 0).mean(),
        'delta_mean': delta_mean,
        'delta_median': delta_median,
        'years': years,
        'median_time': median_time,
    }


# =============================================================================
# CAND-093: PRICE-DISCOVERY FRICTION GRADIENT
# =============================================================================

def run_cand093(df):
    """
    CAND-093: Price-Discovery Friction Gradient

    Hypothesis: Structural level breaks preceded by low-friction (clean,
    monotonic) price approach produce larger directional moves than breaks
    preceded by high-friction (choppy, oscillatory) price approach.
    """
    print("\n" + "="*70)
    print("CAND-093: PRICE-DISCOVERY FRICTION GRADIENT")
    print("="*70)

    df = compute_structural_levels(df)
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    struct_h = df['struct_high'].values
    struct_l = df['struct_low'].values
    n = len(close)

    # Step 1: Detect breaks
    print("\nStep 1: Detecting structural level breaks...")
    up_breaks, dn_breaks = detect_breaks_vectorized(df)
    up_breaks = apply_rearm(up_breaks, n)
    dn_breaks = apply_rearm(dn_breaks, n)
    print(f"  After rearm: up={len(up_breaks)}, down={len(dn_breaks)}")

    # Step 2: For each break, compute approach smoothness
    print("\nStep 2: Computing approach smoothness for each break...")
    t0 = time.time()

    bar_returns = np.zeros(n)
    bar_returns[1:] = (close[1:] - close[:-1]) / close[:-1]

    events = []
    for b_idx in np.concatenate([up_breaks, dn_breaks]):
        if b_idx + HOLDING_PERIOD >= n:
            continue

        direction = 1 if b_idx in up_breaks else -1

        # Find the structural level at the time of break
        if direction == 1:
            level = struct_h[b_idx] if not np.isnan(struct_h[b_idx]) else close[b_idx]
        else:
            level = struct_l[b_idx] if not np.isnan(struct_l[b_idx]) else close[b_idx]

        # Approach window: from the bar where price first came within 10 bps of the level
        # to the break bar. Use up to 20 bars before the break.
        approach_start = max(0, b_idx - STRUCTURAL_LOOKBACK)
        approach_returns = bar_returns[approach_start:b_idx]

        if len(approach_returns) < 3:
            continue

        # Approach smoothness: std of returns (lower = smoother)
        smoothness = np.std(approach_returns)

        # Approach monotonicity: fraction of returns in break direction
        monotonicity = np.mean(approach_returns * direction > 0)

        # Approach duration: number of bars from approach_start to break
        duration = b_idx - approach_start

        # Composite score: low friction = low smoothness + high monotonicity
        # Normalize: smoothness is already in return units; monotonicity is 0-1
        # Use monotonicity as primary (it's bounded), smoothness as secondary
        friction_score = monotonicity  # higher = lower friction

        # Forward returns
        entry = close[b_idx]
        exit_p = close[b_idx + HOLDING_PERIOD]
        gross_bps = (exit_p - entry) / entry * 10000.0 * direction
        net_bps = gross_bps - FRICTION_BPS

        events.append({
            'break_idx': int(b_idx),
            'direction': direction,
            'smoothness': smoothness,
            'monotonicity': monotonicity,
            'friction_score': friction_score,
            'duration': duration,
            'gross_bps': gross_bps,
            'net_bps': net_bps,
        })

    print(f"  Events with approach data: {len(events)} ({time.time()-t0:.1f}s)")

    events_df = pd.DataFrame(events)

    # Step 3: Classify by friction score (monotonicity)
    median_score = events_df['friction_score'].median()
    print(f"\n  Median friction score (monotonicity): {median_score:.3f}")

    low_friction = events_df[events_df['friction_score'] >= median_score]  # high monotonicity = low friction
    high_friction = events_df[events_df['friction_score'] < median_score]  # low monotonicity = high friction

    print(f"  Low friction (clean approach): N = {len(low_friction)}")
    print(f"  High friction (choppy approach): N = {len(high_friction)}")

    # Step 4: Report results
    print("\n" + "-"*70)
    print("CAND-093 RESULTS")
    print("-"*70)

    if len(low_friction) == 0 or len(high_friction) == 0:
        print("  INSUFFICIENT DATA")
        return None

    total_days = (df.index[-1] - df.index[0]).days
    years = total_days / 365.25

    print(f"\n  Coverage: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')} ({years:.1f} years)")

    for label, subdf in [("Low Friction (Treatment)", low_friction), ("High Friction (Control)", high_friction)]:
        print(f"\n  Economics — {label}:")
        print(f"    Gross Mean:   {subdf['gross_bps'].mean():+.2f} bps")
        print(f"    Gross Median: {subdf['gross_bps'].median():+.2f} bps")
        print(f"    Net Mean:     {subdf['net_bps'].mean():+.2f} bps")
        print(f"    Net Median:   {subdf['net_bps'].median():+.2f} bps")
        print(f"    Win Rate:     {(subdf['net_bps'] > 0).mean()*100:.1f}%")
        print(f"    Std Dev:      {subdf['net_bps'].std():.2f} bps")
        print(f"    Mean Smoothness: {subdf['smoothness'].mean():.6f}")
        print(f"    Mean Monotonicity: {subdf['monotonicity'].mean():.3f}")

    delta_mean = low_friction['net_bps'].mean() - high_friction['net_bps'].mean()
    delta_median = low_friction['net_bps'].median() - high_friction['net_bps'].median()
    print(f"\n  Conditional Delta (Low - High Friction):")
    print(f"    Mean Delta:   {delta_mean:+.2f} bps")
    print(f"    Median Delta: {delta_median:+.2f} bps")
    print(f"    WR Delta:     {(low_friction['net_bps'] > 0).mean() - (high_friction['net_bps'] > 0).mean():+.1%}")

    print(f"\n  Frequency:")
    print(f"    Low friction events/year:  {len(low_friction) / years:.0f}")
    print(f"    High friction events/year: {len(high_friction) / years:.0f}")

    for label, subdf in [("Low Friction", low_friction), ("High Friction", high_friction)]:
        print(f"\n  Distribution — {label}:")
        for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
            print(f"    P{int(q*100):02d}: {subdf['net_bps'].quantile(q):+.2f} bps")

    top10_low = low_friction.nlargest(max(1, len(low_friction)//10), 'net_bps')
    top10_high = high_friction.nlargest(max(1, len(high_friction)//10), 'net_bps')
    print(f"\n  Top 10% contribution:")
    lf_sum = low_friction['net_bps'].sum()
    hf_sum = high_friction['net_bps'].sum()
    print(f"    Low friction:  {top10_low['net_bps'].sum():+.1f} of {lf_sum:+.1f} total")
    print(f"    High friction: {top10_high['net_bps'].sum():+.1f} of {hf_sum:+.1f} total")

    for label, subdf in [("Low Friction", low_friction), ("High Friction", high_friction)]:
        if len(subdf) > 1:
            excl_best = subdf.nlargest(1, 'net_bps').index
            print(f"  Exclude-best-event mean ({label}): {subdf.drop(excl_best)['net_bps'].mean():+.2f} bps")

    print(f"\n  Worst event:")
    print(f"    Low friction:  {low_friction['net_bps'].min():+.2f} bps")
    print(f"    High friction: {high_friction['net_bps'].min():+.2f} bps")

    # Direction breakdown
    print(f"\n  Direction-specific:")
    for label, subdf in [("Low Friction", low_friction), ("High Friction", high_friction)]:
        longs = subdf[subdf['direction'] == 1]
        shorts = subdf[subdf['direction'] == -1]
        if len(longs) > 0:
            print(f"    {label} Long:  N={len(longs):4d}, Mean={longs['net_bps'].mean():+.2f}, Median={longs['net_bps'].median():+.2f}, WR={longs['net_bps'].gt(0).mean()*100:.1f}%")
        if len(shorts) > 0:
            print(f"    {label} Short: N={len(shorts):4d}, Mean={shorts['net_bps'].mean():+.2f}, Median={shorts['net_bps'].median():+.2f}, WR={shorts['net_bps'].gt(0).mean()*100:.1f}%")

    return {
        'treatment_n': len(low_friction),
        'control_n': len(high_friction),
        'treatment_net_mean': low_friction['net_bps'].mean(),
        'treatment_net_median': low_friction['net_bps'].median(),
        'treatment_wr': (low_friction['net_bps'] > 0).mean(),
        'control_net_mean': high_friction['net_bps'].mean(),
        'control_net_median': high_friction['net_bps'].median(),
        'control_wr': (high_friction['net_bps'] > 0).mean(),
        'delta_mean': delta_mean,
        'delta_median': delta_median,
        'years': years,
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    df = load_data()

    print("\n" + "#"*70)
    print("# V31 G1 — ECONOMIC PLAUSIBILITY SCREEN")
    print("# CAND-092 + CAND-093")
    print("#"*70)

    cand092_results = run_cand092(df.copy())
    cand093_results = run_cand093(df.copy())

    print("\n\n" + "#"*70)
    print("# SUMMARY")
    print("#"*70)

    if cand092_results:
        r = cand092_results
        print(f"\nCAND-092:")
        print(f"  Treatment N={r['treatment_n']}, Control N={r['control_n']}")
        print(f"  Treatment Net Mean={r['treatment_net_mean']:+.2f} bps, Median={r['treatment_net_median']:+.2f} bps, WR={r['treatment_wr']*100:.1f}%")
        print(f"  Control   Net Mean={r['control_net_mean']:+.2f} bps, Median={r['control_net_median']:+.2f} bps, WR={r['control_wr']*100:.1f}%")
        print(f"  Delta Mean={r['delta_mean']:+.2f} bps, Median={r['delta_median']:+.2f} bps")
    else:
        print("\nCAND-092: INSUFFICIENT DATA")

    if cand093_results:
        r = cand093_results
        print(f"\nCAND-093:")
        print(f"  Treatment N={r['treatment_n']}, Control N={r['control_n']}")
        print(f"  Treatment Net Mean={r['treatment_net_mean']:+.2f} bps, Median={r['treatment_net_median']:+.2f} bps, WR={r['treatment_wr']*100:.1f}%")
        print(f"  Control   Net Mean={r['control_net_mean']:+.2f} bps, Median={r['control_net_median']:+.2f} bps, WR={r['control_wr']*100:.1f}%")
        print(f"  Delta Mean={r['delta_mean']:+.2f} bps, Median={r['delta_median']:+.2f} bps")
    else:
        print("\nCAND-093: INSUFFICIENT DATA")
