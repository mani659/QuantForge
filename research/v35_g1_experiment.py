"""
V35 G1 — ECONOMIC PLAUSIBILITY SCREEN
CAND-103: Multi-Timeframe Break Coordination
CAND-104: Post-Magnitude Directional Drift

Frozen definitions from V35 G0.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# =============================================================================
# FROZEN PARAMETERS — DO NOT MODIFY
# =============================================================================

MARKET = "USATECHIDXUSD"
TIMEFRAME = "M1"
FRICTION_BPS = 2.0
HOLDING_PERIOD = 60  # bars on M1 = 60 min

# CAND-103: Multi-Timeframe Break Coordination
C103_ATR_LOOKBACK = 100
C103_BREAKOUT_THRESHOLD_ATR_MULT = 1.5
C103_TIMEFRAMES = [15, 60, 240]  # minutes: M15, H1, H4
C103_OUTCOME_HORIZON = 60  # bars
C103_MIN_EVENT_SEPARATION = 60  # min bars between events

# CAND-104: Post-Magnitude Directional Drift
C104_ATR_LOOKBACK = 100
C104_MAGNITUDE_THRESHOLDS = [2.0, 3.0, 4.0, 5.0]  # ATR multiples
C104_OUTCOME_HORIZON = 60  # bars
C104_MIN_EVENT_SEPARATION = 60  # min bars between events


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


def compute_atr(df, lookback=100):
    tr = pd.concat([
        df['high'] - df['low'],
        (df['high'] - df['close'].shift(1)).abs(),
        (df['low'] - df['close'].shift(1)).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(lookback).mean()


def compute_forward_returns(df, idx, period=C103_OUTCOME_HORIZON):
    """Compute forward return in bps from bar idx."""
    if idx + period >= len(df):
        return np.nan
    entry = df.iloc[idx]['close']
    exit_ = df.iloc[idx + period]['close']
    return (exit_ - entry) / entry * 10000


def aggregate_to_timeframe(df, tf_minutes):
    """Aggregate M1 data to higher timeframe."""
    rule = f'{tf_minutes}min'
    agg = df.resample(rule).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    }).dropna()
    return agg


def detect_breaks(df, atr, threshold_mult=C103_BREAKOUT_THRESHOLD_ATR_MULT):
    """Detect structural breaks: bars where range > threshold * ATR."""
    bar_range = df['high'] - df['low']
    threshold = atr * threshold_mult
    break_mask = bar_range > threshold
    
    breaks = []
    for i in range(len(df)):
        if break_mask.iloc[i]:
            direction = 'up' if df.iloc[i]['close'] > df.iloc[i]['open'] else 'down'
            breaks.append({
                'bar_idx': i,
                'timestamp': df.index[i],
                'direction': direction,
                'close': df.iloc[i]['close'],
                'high': df.iloc[i]['high'],
                'low': df.iloc[i]['low'],
                'range': bar_range.iloc[i],
                'atr': atr.iloc[i]
            })
    return breaks


def run_cand103(df, atr):
    """Run CAND-103: Multi-Timeframe Break Coordination."""
    print("\n=== CAND-103: MULTI-TIMEFRAME BREAK COORDINATION ===")
    
    # Vectorized approach: for each timeframe, compute rolling high/low
    # and check if current M1 bar breaks it
    m1_tf_breaks = {}
    for tf in C103_TIMEFRAMES:
        # Compute rolling high/low for each timeframe using M1 aggregation
        rolling_high = df['high'].rolling(tf).max().shift(1)
        rolling_low = df['low'].rolling(tf).min().shift(1)
        
        # Check if current bar breaks the rolling level
        breaks_up = df['high'] > rolling_high
        breaks_down = df['low'] < rolling_low
        tf_breaks = (breaks_up | breaks_down).astype(int).fillna(0)
        m1_tf_breaks[tf] = tf_breaks.values
        print(f"  {tf}-min breaks: {tf_breaks.sum():.0f}")
    
    # Count how many timeframes are broken at each M1 bar
    n_bars = len(df)
    multi_tf_counts = np.zeros(n_bars)
    for tf in C103_TIMEFRAMES:
        multi_tf_counts += np.array(m1_tf_breaks[tf])
    
    # Remove unused lines after the vectorized approach
    
    # Classify events by multi-timeframe coordination
    # Treatment: 2+ timeframes broken simultaneously
    # Control: only 1 timeframe broken
    
    events = []
    for i in range(n_bars):
        if i + C103_OUTCOME_HORIZON >= n_bars:
            continue
        if i < C103_ATR_LOOKBACK:
            continue
        
        count = int(multi_tf_counts[i])
        if count >= 1:  # at least one timeframe broken
            direction = 'up' if df.iloc[i]['close'] > df.iloc[i]['open'] else 'down'
            events.append({
                'bar_idx': i,
                'timestamp': df.index[i],
                'tf_count': count,
                'direction': direction,
                'multi_tf': count >= 2
            })
    
    # Deduplicate: keep only one event per cluster
    deduped = []
    for e in events:
        if not deduped or e['bar_idx'] - deduped[-1]['bar_idx'] >= C103_MIN_EVENT_SEPARATION:
            deduped.append(e)
    
    # Split into treatment (multi-TF) and control (single-TF)
    treatment = [e for e in deduped if e['multi_tf']]
    control = [e for e in deduped if not e['multi_tf']]
    
    # Remove unused lines
    
    print(f"\nTotal events (deduped): {len(deduped)}")
    print(f"Treatment (2+ timeframes): {len(treatment)}")
    print(f"Control (1 timeframe): {len(control)}")
    
    if len(treatment) == 0 or len(control) == 0:
        print("ERROR: One or both groups have zero events.")
        return None
    
    # Compute forward returns
    treatment_returns = np.array([
        compute_forward_returns(df, e['bar_idx'], C103_OUTCOME_HORIZON)
        for e in treatment
    ])
    control_returns = np.array([
        compute_forward_returns(df, e['bar_idx'], C103_OUTCOME_HORIZON)
        for e in control
    ])
    
    # Remove NaN
    treatment_returns = treatment_returns[~np.isnan(treatment_returns)]
    control_returns = control_returns[~np.isnan(control_returns)]
    
    print(f"\nTreatment (Multi-TF) — N={len(treatment_returns)}:")
    print(f"  Gross Mean: {np.mean(treatment_returns):.2f} bps")
    print(f"  Gross Median: {np.median(treatment_returns):.2f} bps")
    print(f"  Net Mean: {np.mean(treatment_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Net Median: {np.median(treatment_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Win Rate: {np.mean(treatment_returns > 0) * 100:.1f}%")
    print(f"  Std Dev: {np.std(treatment_returns):.2f} bps")
    
    print(f"\nControl (Single-TF) — N={len(control_returns)}:")
    print(f"  Gross Mean: {np.mean(control_returns):.2f} bps")
    print(f"  Gross Median: {np.median(control_returns):.2f} bps")
    print(f"  Net Mean: {np.mean(control_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Net Median: {np.median(control_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Win Rate: {np.mean(control_returns > 0) * 100:.1f}%")
    print(f"  Std Dev: {np.std(control_returns):.2f} bps")
    
    # Delta
    mean_delta = np.mean(treatment_returns) - np.mean(control_returns)
    median_delta = np.median(treatment_returns) - np.median(control_returns)
    wr_delta = np.mean(treatment_returns > 0) - np.mean(control_returns > 0)
    
    print(f"\nDelta (Multi-TF minus Single-TF):")
    print(f"  Mean Delta: {mean_delta:.2f} bps")
    print(f"  Median Delta: {median_delta:.2f} bps")
    print(f"  WR Delta: {wr_delta * 100:.1f}%")
    
    # Distribution width comparison
    print(f"\nDistribution width (std):")
    print(f"  Treatment: {np.std(treatment_returns):.2f} bps")
    print(f"  Control: {np.std(control_returns):.2f} bps")
    
    # Direction-specific analysis
    print(f"\nDirection-specific analysis:")
    for group_name, group in [('Treatment', treatment), ('Control', control)]:
        up_rets = np.array([
            compute_forward_returns(df, e['bar_idx'], C103_OUTCOME_HORIZON)
            for e in group if e['direction'] == 'up'
        ])
        down_rets = np.array([
            compute_forward_returns(df, e['bar_idx'], C103_OUTCOME_HORIZON)
            for e in group if e['direction'] == 'down'
        ])
        up_rets = up_rets[~np.isnan(up_rets)]
        down_rets = down_rets[~np.isnan(down_rets)]
        if len(up_rets) > 0:
            print(f"  {group_name} UP: N={len(up_rets)}, Mean={np.mean(up_rets):.2f}, WR={np.mean(up_rets > 0)*100:.1f}%")
        if len(down_rets) > 0:
            print(f"  {group_name} DOWN: N={len(down_rets)}, Mean={np.mean(down_rets):.2f}, WR={np.mean(down_rets > 0)*100:.1f}%")
    
    return {
        'treatment_n': len(treatment_returns),
        'control_n': len(control_returns),
        'treatment_gross_mean': np.mean(treatment_returns),
        'treatment_gross_median': np.median(treatment_returns),
        'treatment_net_mean': np.mean(treatment_returns) - FRICTION_BPS,
        'treatment_net_median': np.median(treatment_returns) - FRICTION_BPS,
        'treatment_wr': np.mean(treatment_returns > 0) * 100,
        'treatment_std': np.std(treatment_returns),
        'control_gross_mean': np.mean(control_returns),
        'control_gross_median': np.median(control_returns),
        'control_net_mean': np.mean(control_returns) - FRICTION_BPS,
        'control_net_median': np.median(control_returns) - FRICTION_BPS,
        'control_wr': np.mean(control_returns > 0) * 100,
        'control_std': np.std(control_returns),
        'mean_delta': mean_delta,
        'median_delta': median_delta,
        'wr_delta': wr_delta * 100,
    }


def run_cand104(df, atr):
    """Run CAND-104: Post-Magnitude Directional Drift."""
    print("\n=== CAND-104: POST-MAGNITUDE DIRECTIONAL DRIFT ===")
    
    # Compute move magnitude (absolute return / ATR)
    bar_return = (df['close'] - df['open']).abs()
    magnitude = bar_return / atr
    
    print(f"\nMagnitude distribution:")
    for thresh in C104_MAGNITUDE_THRESHOLDS:
        count = np.sum(magnitude > thresh)
        print(f"  > {thresh}x ATR: {count} bars ({count/len(df)*100:.2f}%)")
    
    # Detect large moves
    events = []
    for i in range(len(df)):
        if i + C104_OUTCOME_HORIZON >= len(df):
            continue
        if i < C104_ATR_LOOKBACK:
            continue
        if np.isnan(magnitude.iloc[i]):
            continue
        
        mag = magnitude.iloc[i]
        direction = 'up' if df.iloc[i]['close'] > df.iloc[i]['open'] else 'down'
        events.append({
            'bar_idx': i,
            'timestamp': df.index[i],
            'magnitude': mag,
            'direction': direction,
        })
    
    # Deduplicate
    deduped = []
    for e in events:
        if not deduped or e['bar_idx'] - deduped[-1]['bar_idx'] >= C104_MIN_EVENT_SEPARATION:
            deduped.append(e)
    
    print(f"\nTotal events (deduped): {len(deduped)}")
    
    # Group by magnitude threshold
    results = {}
    for thresh in C104_MAGNITUDE_THRESHOLDS:
        treatment = [e for e in deduped if e['magnitude'] >= thresh]
        control = [e for e in deduped if e['magnitude'] < thresh]
        
        if len(treatment) < 10 or len(control) < 10:
            continue
        
        treatment_returns = np.array([
            compute_forward_returns(df, e['bar_idx'], C104_OUTCOME_HORIZON)
            for e in treatment
        ])
        control_returns = np.array([
            compute_forward_returns(df, e['bar_idx'], C104_OUTCOME_HORIZON)
            for e in control
        ])
        
        treatment_returns = treatment_returns[~np.isnan(treatment_returns)]
        control_returns = control_returns[~np.isnan(control_returns)]
        
        mean_delta = np.mean(treatment_returns) - np.mean(control_returns)
        median_delta = np.median(treatment_returns) - np.median(control_returns)
        wr_delta = np.mean(treatment_returns > 0) - np.mean(control_returns > 0)
        
        results[thresh] = {
            'treatment_n': len(treatment_returns),
            'control_n': len(control_returns),
            'treatment_gross_mean': np.mean(treatment_returns),
            'treatment_gross_median': np.median(treatment_returns),
            'treatment_net_mean': np.mean(treatment_returns) - FRICTION_BPS,
            'treatment_net_median': np.median(treatment_returns) - FRICTION_BPS,
            'treatment_wr': np.mean(treatment_returns > 0) * 100,
            'treatment_std': np.std(treatment_returns),
            'control_gross_mean': np.mean(control_returns),
            'control_gross_median': np.median(control_returns),
            'control_net_mean': np.mean(control_returns) - FRICTION_BPS,
            'control_net_median': np.median(control_returns) - FRICTION_BPS,
            'control_wr': np.mean(control_returns > 0) * 100,
            'control_std': np.std(control_returns),
            'mean_delta': mean_delta,
            'median_delta': median_delta,
            'wr_delta': wr_delta * 100,
        }
        
        print(f"\nThreshold >= {thresh}x ATR:")
        print(f"  Treatment N={len(treatment_returns)}, Control N={len(control_returns)}")
        print(f"  Treatment Gross Mean: {np.mean(treatment_returns):.2f} bps, Net Mean: {np.mean(treatment_returns) - FRICTION_BPS:.2f} bps")
        print(f"  Control Gross Mean: {np.mean(control_returns):.2f} bps, Net Mean: {np.mean(control_returns) - FRICTION_BPS:.2f} bps")
        print(f"  Mean Delta: {mean_delta:.2f} bps, Median Delta: {median_delta:.2f} bps")
        print(f"  Treatment WR: {np.mean(treatment_returns > 0)*100:.1f}%, Control WR: {np.mean(control_returns > 0)*100:.1f}%")
        print(f"  Treatment Std: {np.std(treatment_returns):.2f}, Control Std: {np.std(control_returns):.2f}")
    
    # Direction-specific analysis for largest threshold
    if results:
        best_thresh = max(results.keys())
        print(f"\nDirection-specific analysis (>= {best_thresh}x ATR):")
        treatment = [e for e in deduped if e['magnitude'] >= best_thresh]
        for direction in ['up', 'down']:
            dir_events = [e for e in treatment if e['direction'] == direction]
            dir_returns = np.array([
                compute_forward_returns(df, e['bar_idx'], C104_OUTCOME_HORIZON)
                for e in dir_events
            ])
            dir_returns = dir_returns[~np.isnan(dir_returns)]
            if len(dir_returns) > 0:
                print(f"  {direction.upper()}: N={len(dir_returns)}, Mean={np.mean(dir_returns):.2f}, WR={np.mean(dir_returns > 0)*100:.1f}%")
    
    return results


def main():
    print("=" * 70)
    print("V35 G1 — ECONOMIC PLAUSIBILITY SCREEN")
    print("CAND-103: Multi-Timeframe Break Coordination")
    print("CAND-104: Post-Magnitude Directional Drift")
    print("=" * 70)
    
    # Load data
    df = load_data()
    atr = compute_atr(df, C103_ATR_LOOKBACK)
    
    # Run CAND-103
    cand103_results = run_cand103(df, atr)
    
    # Run CAND-104
    cand104_results = run_cand104(df, atr)
    
    print("\n" + "=" * 70)
    print("V35 G1 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
