"""
V32 G1 — ECONOMIC PLAUSIBILITY SCREEN
CAND-095: Shock-Magnitude Asymmetry
CAND-096: Volatility Acceleration Gradient

Frozen definitions from V32 G0.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time

# =============================================================================
# FROZEN PARAMETERS — DO NOT MODIFY
# =============================================================================

MARKET = "USATECHIDXUSD"
TIMEFRAME = "M1"
FRICTION_BPS = 2.0
HOLDING_PERIOD = 60  # bars on M1 = 60 min
REARM_BARS = 60

# CAND-095
SHOCK_THRESHOLD_ATR_MULT = 1.5
ATR_LOOKBACK = 100

# CAND-096
STRUCTURAL_LOOKBACK = 20
BREAKOUT_THRESHOLD = 3  # bps
VOL_ATR_LOOKBACK = 100


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


def apply_rearm(indices, n):
    if len(indices) == 0:
        return indices
    filtered = [indices[0]]
    for idx in indices[1:]:
        if idx - filtered[-1] >= REARM_BARS:
            filtered.append(idx)
    return np.array(filtered)


# =============================================================================
# CAND-095: SHOCK-MAGNITUDE ASYMMETRY
# =============================================================================

def run_cand095(df):
    """
    CAND-095: Shock-Magnitude Asymmetry
    
    Hypothesis: Direction of large move (UP vs DOWN) produces different
    downstream economics due to asymmetric participant response.
    
    Frozen definition:
    - Detect bar-to-bar moves > 1.5x rolling 100-bar ATR
    - Classify by direction: UP shock vs DOWN shock
    - Enter WITH shock direction
    - 60-minute holding period
    - 60-bar rearm
    - 2 bps friction
    - Counterfactual: opposite-direction shocks of similar magnitude
    """
    print("\n" + "="*70)
    print("CAND-095: SHOCK-MAGNITUDE ASYMMETRY")
    print("="*70)
    
    df = df.copy()
    
    # Compute rolling ATR
    tr = pd.concat([
        df['high'] - df['low'],
        (df['high'] - df['close'].shift(1)).abs(),
        (df['low'] - df['close'].shift(1)).abs()
    ], axis=1).max(axis=1)
    df['atr'] = tr.rolling(ATR_LOOKBACK).mean()
    
    # Compute bar-to-bar return in bps
    df['bar_return_bps'] = df['close'].pct_change() * 10000  # in bps
    
    # Compute ATR threshold in bps (ATR is in price units, close is in price units)
    # shock_threshold = 1.5 * ATR / close * 10000 (in bps)
    df['atr_threshold_bps'] = df['atr'] / df['close'] * SHOCK_THRESHOLD_ATR_MULT * 10000
    
    # Detect large moves (shocks)
    df['is_up_shock'] = df['bar_return_bps'] > df['atr_threshold_bps']
    df['is_down_shock'] = df['bar_return_bps'] < -df['atr_threshold_bps']
    
    # Get shock indices
    up_shock_idx = np.where(df['is_up_shock'].values)[0]
    dn_shock_idx = np.where(df['is_down_shock'].values)[0]
    
    # Apply rearm
    up_shock_idx = apply_rearm(up_shock_idx, len(df))
    dn_shock_idx = apply_rearm(dn_shock_idx, len(df))
    
    print(f"\nRaw UP shocks: {np.sum(df['is_up_shock'])}")
    print(f"Raw DOWN shocks: {np.sum(df['is_down_shock'])}")
    print(f"After rearm - UP: {len(up_shock_idx)}, DOWN: {len(dn_shock_idx)}")
    
    close = df['close'].values
    n = len(close)
    
    def compute_group_economics(indices, label):
        """Compute forward returns for a group of shocks."""
        returns = []
        for idx in indices:
            if idx + HOLDING_PERIOD < n:
                entry = close[idx]
                exit_price = close[idx + HOLDING_PERIOD]
                ret_bps = (exit_price - entry) / entry * 10000
                returns.append(ret_bps)
        
        if len(returns) == 0:
            return None
        
        returns = np.array(returns)
        net_returns = returns - FRICTION_BPS
        
        result = {
            'N': len(returns),
            'Gross Mean': np.mean(returns),
            'Gross Median': np.median(returns),
            'Net Mean': np.mean(net_returns),
            'Net Median': np.median(net_returns),
            'Win Rate': np.mean(net_returns > 0) * 100,
            'Std': np.std(returns),
            'P10': np.percentile(returns, 10),
            'P25': np.percentile(returns, 25),
            'P75': np.percentile(returns, 75),
            'P90': np.percentile(returns, 90),
        }
        
        print(f"\n{label} (N={result['N']}):")
        print(f"  Gross Mean: {result['Gross Mean']:.2f} bps")
        print(f"  Gross Median: {result['Gross Median']:.2f} bps")
        print(f"  Net Mean: {result['Net Mean']:.2f} bps")
        print(f"  Net Median: {result['Net Median']:.2f} bps")
        print(f"  Win Rate: {result['Win Rate']:.1f}%")
        print(f"  Std: {result['Std']:.2f} bps")
        print(f"  P10/P25/P75/P90: {result['P10']:.1f}/{result['P25']:.1f}/{result['P75']:.1f}/{result['P90']:.1f}")
        
        return result
    
    # Compute economics for both groups
    up_result = compute_group_economics(up_shock_idx, "UP SHOCKS (treatment)")
    dn_result = compute_group_economics(dn_shock_idx, "DOWN SHOCKS (control)")
    
    if up_result is None or dn_result is None:
        print("\nERROR: Insufficient data for one or both groups")
        return
    
    # Conditional delta: UP - DOWN
    mean_delta = up_result['Net Mean'] - dn_result['Net Mean']
    median_delta = up_result['Net Median'] - dn_result['Net Median']
    wr_delta = up_result['Win Rate'] - dn_result['Win Rate']
    
    print(f"\n{'='*50}")
    print(f"CONDITIONAL DELTA (UP minus DOWN):")
    print(f"  Mean Delta: {mean_delta:.2f} bps")
    print(f"  Median Delta: {median_delta:.2f} bps")
    print(f"  WR Delta: {wr_delta:.1f}%")
    print(f"{'='*50}")
    
    # Frequency
    date_range_days = (df.index[-1] - df.index[0]).days
    total_shocks = len(up_shock_idx) + len(dn_shock_idx)
    freq_per_year = total_shocks / (date_range_days / 365.25) if date_range_days > 0 else 0
    print(f"\nFrequency: {freq_per_year:.0f} shocks/year")
    print(f"Date range: {df.index[0]} to {df.index[-1]} ({date_range_days} days)")
    
    return {
        'up': up_result,
        'down': dn_result,
        'mean_delta': mean_delta,
        'median_delta': median_delta,
        'wr_delta': wr_delta,
        'freq_per_year': freq_per_year,
        'date_range': f"{df.index[0]} to {df.index[-1]}",
        'total_events': total_shocks,
    }


# =============================================================================
# CAND-096: VOLATILITY ACCELERATION GRADIENT
# =============================================================================

def run_cand096(df):
    """
    CAND-096: Volatility Acceleration Gradient
    
    Hypothesis: Structural events occurring during periods of volatility
    acceleration produce different downstream economics than events during
    volatility deceleration.
    
    CRITICAL: This must measure VOLATILITY ACCELERATION (second derivative),
    NOT volatility regime transition (CAND-077).
    
    CAND-077 = compressed → expanded (discrete regime transition)
    CAND-096 = volatility acceleration (continuous second derivative)
    
    Frozen definition:
    - Compute rolling 100-bar ATR
    - Compute first difference (vol change) and second difference (acceleration)
    - Detect structural level breaks (20-bar lookback, 3 bps threshold)
    - For each break, classify by volatility acceleration direction
    - Enter WITH break direction
    - 60-minute holding period
    - 60-bar rearm
    - 2 bps friction
    - Counterfactual: breaks during deceleration
    """
    print("\n" + "="*70)
    print("CAND-096: VOLATILITY ACCELERATION GRADIENT")
    print("="*70)
    
    df = df.copy()
    
    # Step 1: Compute rolling ATR
    tr = pd.concat([
        df['high'] - df['low'],
        (df['high'] - df['close'].shift(1)).abs(),
        (df['low'] - df['close'].shift(1)).abs()
    ], axis=1).max(axis=1)
    df['atr'] = tr.rolling(VOL_ATR_LOOKBACK).mean()
    
    # Step 2: Compute volatility change (first difference)
    df['vol_change'] = df['atr'].diff()
    
    # Step 3: Compute volatility acceleration (second difference)
    df['vol_acceleration'] = df['vol_change'].diff()
    
    # Step 4: Detect structural level breaks
    df['struct_high'] = df['high'].rolling(STRUCTURAL_LOOKBACK).max().shift(1)
    df['struct_low'] = df['low'].rolling(STRUCTURAL_LOOKBACK).min().shift(1)
    
    close = df['close'].values
    struct_h = df['struct_high'].values
    struct_l = df['struct_low'].values
    vol_accel = df['vol_acceleration'].values
    n = len(close)
    
    struct_h_bps = struct_h * BREAKOUT_THRESHOLD / 10000.0
    struct_l_bps = struct_l * BREAKOUT_THRESHOLD / 10000.0
    
    up_break = (close > struct_h + struct_h_bps)
    dn_break = (close < struct_l - struct_l_bps)
    
    up_break_idx = np.where(up_break)[0]
    dn_break_idx = np.where(dn_break)[0]
    
    # Combine all breaks
    all_breaks = np.sort(np.concatenate([up_break_idx, dn_break_idx]))
    
    # Apply rearm
    all_breaks = apply_rearm(all_breaks, n)
    
    print(f"\nRaw up breaks: {len(up_break_idx)}")
    print(f"Raw down breaks: {len(dn_break_idx)}")
    print(f"After rearm - total breaks: {len(all_breaks)}")
    
    # Step 5: Classify by volatility acceleration
    # Accelerating: vol_acceleration > 0 (volatility change is increasing)
    # Decelerating: vol_acceleration < 0 (volatility change is decreasing)
    accel_breaks = []
    decel_breaks = []
    
    for idx in all_breaks:
        if not np.isnan(vol_accel[idx]):
            if vol_accel[idx] > 0:
                accel_breaks.append(idx)
            else:
                decel_breaks.append(idx)
    
    accel_breaks = np.array(accel_breaks)
    decel_breaks = np.array(decel_breaks)
    
    print(f"Accelerating breaks: {len(accel_breaks)}")
    print(f"Decelerating breaks: {len(decel_breaks)}")
    
    # Step 6: Compute forward returns
    def compute_group_economics(indices, label):
        """Compute forward returns for a group of breaks."""
        returns = []
        for idx in indices:
            if idx + HOLDING_PERIOD < n:
                entry = close[idx]
                exit_price = close[idx + HOLDING_PERIOD]
                ret_bps = (exit_price - entry) / entry * 10000
                returns.append(ret_bps)
        
        if len(returns) == 0:
            return None
        
        returns = np.array(returns)
        net_returns = returns - FRICTION_BPS
        
        result = {
            'N': len(returns),
            'Gross Mean': np.mean(returns),
            'Gross Median': np.median(returns),
            'Net Mean': np.mean(net_returns),
            'Net Median': np.median(net_returns),
            'Win Rate': np.mean(net_returns > 0) * 100,
            'Std': np.std(returns),
            'P10': np.percentile(returns, 10),
            'P25': np.percentile(returns, 25),
            'P75': np.percentile(returns, 75),
            'P90': np.percentile(returns, 90),
        }
        
        print(f"\n{label} (N={result['N']}):")
        print(f"  Gross Mean: {result['Gross Mean']:.2f} bps")
        print(f"  Gross Median: {result['Gross Median']:.2f} bps")
        print(f"  Net Mean: {result['Net Mean']:.2f} bps")
        print(f"  Net Median: {result['Net Median']:.2f} bps")
        print(f"  Win Rate: {result['Win Rate']:.1f}%")
        print(f"  Std: {result['Std']:.2f} bps")
        print(f"  P10/P25/P75/P90: {result['P10']:.1f}/{result['P25']:.1f}/{result['P75']:.1f}/{result['P90']:.1f}")
        
        return result
    
    accel_result = compute_group_economics(accel_breaks, "ACCELERATING (treatment)")
    decel_result = compute_group_economics(decel_breaks, "DECELERATING (control)")
    
    if accel_result is None or decel_result is None:
        print("\nERROR: Insufficient data for one or both groups")
        return
    
    # Conditional delta: ACCEL - DECEL
    mean_delta = accel_result['Net Mean'] - decel_result['Net Mean']
    median_delta = accel_result['Net Median'] - decel_result['Net Median']
    wr_delta = accel_result['Win Rate'] - decel_result['Win Rate']
    
    print(f"\n{'='*50}")
    print(f"CONDITIONAL DELTA (ACCEL minus DECEL):")
    print(f"  Mean Delta: {mean_delta:.2f} bps")
    print(f"  Median Delta: {median_delta:.2f} bps")
    print(f"  WR Delta: {wr_delta:.1f}%")
    print(f"{'='*50}")
    
    # Frequency
    date_range_days = (df.index[-1] - df.index[0]).days
    total_breaks = len(accel_breaks) + len(decel_breaks)
    freq_per_year = total_breaks / (date_range_days / 365.25) if date_range_days > 0 else 0
    print(f"\nFrequency: {freq_per_year:.0f} breaks/year")
    print(f"Date range: {df.index[0]} to {df.index[-1]} ({date_range_days} days)")
    
    # CAND-077 SEMANTIC CHECK
    # Check if acceleration measure is distinct from regime transition
    print(f"\n{'='*50}")
    print("CAND-077 SEMANTIC CHECK:")
    print("  CAND-077 = discrete regime transition (compressed -> expanded)")
    print("  CAND-096 = continuous acceleration (second derivative of ATR)")
    print("  If acceleration measure collapses into regime transition,")
    print("  this G1 result is INVALID.")
    print(f"{'='*50}")
    
    return {
        'accel': accel_result,
        'decel': decel_result,
        'mean_delta': mean_delta,
        'median_delta': median_delta,
        'wr_delta': wr_delta,
        'freq_per_year': freq_per_year,
        'date_range': f"{df.index[0]} to {df.index[-1]}",
        'total_events': total_breaks,
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    start = time.time()
    
    df = load_data()
    
    # Run CAND-095
    result_095 = run_cand095(df)
    
    # Run CAND-096
    result_096 = run_cand096(df)
    
    elapsed = time.time() - start
    print(f"\nTotal time: {elapsed:.1f}s")
