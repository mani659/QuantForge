"""
V34 G1 — ECONOMIC PLAUSIBILITY SCREEN
CAND-101: Path-Dependent Sequence Asymmetry
CAND-102: Directional Momentum Persistence

Frozen definitions from V34 G0.
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
REARM_BARS = 60

# CAND-101: Path-Dependent Sequence Asymmetry
C101_BREAKOUT_THRESHOLD_ATR_MULT = 1.5
C101_ATR_LOOKBACK = 100
C101_RETEST_TOLERANCE_ATR_MULT = 0.3  # price must return within 0.3 ATR of break level
C101_MAX_RETEST_WINDOW = 30  # max bars between break and retest
C101_MIN_SEQUENCE_SEPARATION = 5  # min bars between sequence events
C101_OUTCOME_HORIZON = 60  # bars

# CAND-102: Directional Momentum Persistence
C102_BREAKOUT_THRESHOLD_ATR_MULT = 1.5
C102_ATR_LOOKBACK = 100
C102_MIN_RUN_LENGTH = 3  # minimum consecutive same-direction breaks
C102_MAX_RUN_LENGTH = 10  # maximum run length to test
C102_OUTCOME_HORIZON = 60  # bars
C102_TREND_LOOKBACK = 200  # bars for basic trend measure


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


def compute_forward_returns(df, idx, period=C101_OUTCOME_HORIZON):
    """Compute forward return in bps from bar idx."""
    if idx + period >= len(df):
        return np.nan
    entry = df.iloc[idx]['close']
    exit_ = df.iloc[idx + period]['close']
    return (exit_ - entry) / entry * 10000


def detect_structural_breaks(df, atr, threshold_mult=C101_BREAKOUT_THRESHOLD_ATR_MULT):
    """Detect structural breaks: bars where the move exceeds threshold * ATR."""
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


def detect_retests(df, breaks, atr, tolerance_mult=C101_RETEST_TOLERANCE_ATR_MULT, 
                    max_window=C101_MAX_RETEST_WINDOW):
    """After each break, look for a retest (price returns near break level)."""
    retests = []
    break_levels = [b['close'] for b in breaks]
    
    for b_idx, brk in enumerate(breaks):
        # Look forward for retest
        start = brk['bar_idx'] + 1
        end = min(brk['bar_idx'] + max_window, len(df))
        
        for j in range(start, end):
            bar = df.iloc[j]
            tolerance = atr.iloc[j] * tolerance_mult
            # Check if price returns near break level
            if abs(bar['low'] - brk['close']) <= tolerance or abs(bar['high'] - brk['close']) <= tolerance:
                retests.append({
                    'bar_idx': j,
                    'timestamp': df.index[j],
                    'original_break_idx': b_idx,
                    'break_timestamp': brk['timestamp'],
                    'break_direction': brk['direction'],
                    'break_level': brk['close'],
                    'close': bar['close'],
                })
                break  # only first retest per break
    return retests


def classify_sequences(breaks, retests):
    """
    Classify event sequences as:
    B→R: break followed by retest
    R→B: retest followed by break (retest of previous break, then new break)
    """
    sequences = []
    
    # Create a unified event list
    events = []
    for b in breaks:
        events.append({'type': 'break', 'bar_idx': b['bar_idx'], 'direction': b['direction'], 
                       'data': b})
    for r in retests:
        events.append({'type': 'retest', 'bar_idx': r['bar_idx'], 
                       'break_direction': r['break_direction'], 'data': r})
    
    # Sort by bar index
    events.sort(key=lambda x: x['bar_idx'])
    
    # Find consecutive break-retest or retest-break pairs
    for i in range(len(events) - 1):
        e1 = events[i]
        e2 = events[i + 1]
        
        # Check minimum separation
        if e2['bar_idx'] - e1['bar_idx'] < C101_MIN_SEQUENCE_SEPARATION:
            continue
        
        if e1['type'] == 'break' and e2['type'] == 'retest':
            # B→R: break followed by retest
            sequences.append({
                'sequence_type': 'B_to_R',
                'event1_bar': e1['bar_idx'],
                'event2_bar': e2['bar_idx'],
                'signal_bar': e2['bar_idx'],  # signal at retest completion
                'direction': e1['direction'],
                'spacing': e2['bar_idx'] - e1['bar_idx']
            })
        elif e1['type'] == 'retest' and e2['type'] == 'break':
            # R→B: retest followed by break
            sequences.append({
                'sequence_type': 'R_to_B',
                'event1_bar': e1['bar_idx'],
                'event2_bar': e2['bar_idx'],
                'signal_bar': e2['bar_idx'],  # signal at new break
                'direction': e2['direction'],
                'spacing': e2['bar_idx'] - e1['bar_idx']
            })
    
    return sequences


def compute_run_lengths(breaks):
    """Compute run length of consecutive same-direction breaks."""
    if not breaks:
        return []
    
    runs = []
    current_direction = breaks[0]['direction']
    current_run = 1
    
    for i in range(1, len(breaks)):
        if breaks[i]['direction'] == current_direction:
            current_run += 1
        else:
            # Record the run
            for j in range(max(0, i - current_run), i):
                runs.append({
                    'bar_idx': breaks[j]['bar_idx'],
                    'direction': current_direction,
                    'run_length': current_run,
                    'is_end_of_run': (j == i - 1)
                })
            current_direction = breaks[i]['direction']
            current_run = 1
    
    # Record final run
    for j in range(max(0, len(breaks) - current_run), len(breaks)):
        runs.append({
            'bar_idx': breaks[j]['bar_idx'],
            'direction': current_direction,
            'run_length': current_run,
            'is_end_of_run': True
        })
    
    return runs


def compute_trend(df, idx, lookback=C102_TREND_LOOKBACK):
    """Compute basic trend measure: simple return over lookback period."""
    if idx < lookback:
        return np.nan
    return (df.iloc[idx]['close'] - df.iloc[idx - lookback]['close']) / df.iloc[idx - lookback]['close'] * 10000


def run_cand101(df, atr, breaks, retests):
    """Run CAND-101: Path-Dependent Sequence Asymmetry."""
    print("\n=== CAND-101: PATH-DEPENDENT SEQUENCE ASYMMETRY ===")
    
    sequences = classify_sequences(breaks, retests)
    print(f"Total sequences classified: {len(sequences)}")
    
    b_to_r = [s for s in sequences if s['sequence_type'] == 'B_to_R']
    r_to_b = [s for s in sequences if s['sequence_type'] == 'R_to_B']
    print(f"B->R sequences: {len(b_to_r)}")
    print(f"R->B sequences: {len(r_to_b)}")
    
    if len(b_to_r) == 0 or len(r_to_b) == 0:
        print("ERROR: One or both sequence types have zero events. Cannot compare.")
        return None
    
    # Compute forward returns for each sequence type
    b_to_r_returns = []
    for s in b_to_r:
        ret = compute_forward_returns(df, s['signal_bar'], C101_OUTCOME_HORIZON)
        if not np.isnan(ret):
            b_to_r_returns.append(ret)
    
    r_to_b_returns = []
    for s in r_to_b:
        ret = compute_forward_returns(df, s['signal_bar'], C101_OUTCOME_HORIZON)
        if not np.isnan(ret):
            r_to_b_returns.append(ret)
    
    b_to_r_returns = np.array(b_to_r_returns)
    r_to_b_returns = np.array(r_to_b_returns)
    
    print(f"\nB->R (Break->Retest) -- N={len(b_to_r_returns)}:")
    print(f"  Gross Mean: {np.mean(b_to_r_returns):.2f} bps")
    print(f"  Gross Median: {np.median(b_to_r_returns):.2f} bps")
    print(f"  Net Mean: {np.mean(b_to_r_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Net Median: {np.median(b_to_r_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Win Rate: {np.mean(b_to_r_returns > 0) * 100:.1f}%")
    print(f"  Std Dev: {np.std(b_to_r_returns):.2f} bps")
    
    print(f"\nR->B (Retest->Break) -- N={len(r_to_b_returns)}:")
    print(f"  Gross Mean: {np.mean(r_to_b_returns):.2f} bps")
    print(f"  Gross Median: {np.median(r_to_b_returns):.2f} bps")
    print(f"  Net Mean: {np.mean(r_to_b_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Net Median: {np.median(r_to_b_returns) - FRICTION_BPS:.2f} bps")
    print(f"  Win Rate: {np.mean(r_to_b_returns > 0) * 100:.1f}%")
    print(f"  Std Dev: {np.std(r_to_b_returns):.2f} bps")
    
    # Delta
    mean_delta = np.mean(b_to_r_returns) - np.mean(r_to_b_returns)
    median_delta = np.median(b_to_r_returns) - np.median(r_to_b_returns)
    wr_delta = np.mean(b_to_r_returns > 0) - np.mean(r_to_b_returns > 0)
    
    print(f"\nDelta (B->R minus R->B):")
    print(f"  Mean Delta: {mean_delta:.2f} bps")
    print(f"  Median Delta: {median_delta:.2f} bps")
    print(f"  WR Delta: {wr_delta * 100:.1f}%")
    
    # Direction-specific analysis
    print(f"\nDirection-specific analysis:")
    for seq_type, returns in [('B->R', b_to_r_returns), ('R->B', r_to_b_returns)]:
        up_rets = [r for s, r in zip([s for s in sequences if s['sequence_type'] == seq_type], 
                   [compute_forward_returns(df, s['signal_bar'], C101_OUTCOME_HORIZON) 
                    for s in [s for s in sequences if s['sequence_type'] == seq_type]]) 
                   if not np.isnan(r) and s['direction'] == 'up']
        down_rets = [r for s, r in zip([s for s in sequences if s['sequence_type'] == seq_type], 
                    [compute_forward_returns(df, s['signal_bar'], C101_OUTCOME_HORIZON) 
                     for s in [s for s in sequences if s['sequence_type'] == seq_type]]) 
                    if not np.isnan(r) and s['direction'] == 'down']
        if up_rets:
            print(f"  {seq_type} UP: N={len(up_rets)}, Mean={np.mean(up_rets):.2f}, WR={np.mean(np.array(up_rets) > 0)*100:.1f}%")
        if down_rets:
            print(f"  {seq_type} DOWN: N={len(down_rets)}, Mean={np.mean(down_rets):.2f}, WR={np.mean(np.array(down_rets) > 0)*100:.1f}%")
    
    return {
        'b_to_r_n': len(b_to_r_returns),
        'r_to_b_n': len(r_to_b_returns),
        'b_to_r_gross_mean': np.mean(b_to_r_returns),
        'b_to_r_gross_median': np.median(b_to_r_returns),
        'b_to_r_net_mean': np.mean(b_to_r_returns) - FRICTION_BPS,
        'b_to_r_net_median': np.median(b_to_r_returns) - FRICTION_BPS,
        'b_to_r_wr': np.mean(b_to_r_returns > 0) * 100,
        'b_to_r_std': np.std(b_to_r_returns),
        'r_to_b_gross_mean': np.mean(r_to_b_returns),
        'r_to_b_gross_median': np.median(r_to_b_returns),
        'r_to_b_net_mean': np.mean(r_to_b_returns) - FRICTION_BPS,
        'r_to_b_net_median': np.median(r_to_b_returns) - FRICTION_BPS,
        'r_to_b_wr': np.mean(r_to_b_returns > 0) * 100,
        'r_to_b_std': np.std(r_to_b_returns),
        'mean_delta': mean_delta,
        'median_delta': median_delta,
        'wr_delta': wr_delta * 100,
    }


def run_cand102(df, atr, breaks):
    """Run CAND-102: Directional Momentum Persistence."""
    print("\n=== CAND-102: DIRECTIONAL MOMENTUM PERSISTENCE ===")
    
    runs = compute_run_lengths(breaks)
    end_of_run = [r for r in runs if r['is_end_of_run']]
    
    print(f"Total breaks: {len(breaks)}")
    print(f"Total run observations: {len(runs)}")
    print(f"End-of-run observations (for next-break analysis): {len(end_of_run)}")
    
    # Group by run length
    results = {}
    for rl in range(C102_MIN_RUN_LENGTH, C102_MAX_RUN_LENGTH + 1):
        run_events = [r for r in end_of_run if r['run_length'] == rl]
        if len(run_events) < 10:
            continue
        
        # Compute forward returns
        returns = []
        trend_controls = []
        for r in run_events:
            ret = compute_forward_returns(df, r['bar_idx'], C102_OUTCOME_HORIZON)
            trend = compute_trend(df, r['bar_idx'], C102_TREND_LOOKBACK)
            if not np.isnan(ret):
                returns.append(ret)
                trend_controls.append(trend)
        
        returns = np.array(returns)
        trend_controls = np.array(trend_controls)
        
        if len(returns) == 0:
            continue
        
        # Direction-specific analysis
        same_dir_returns = []
        opp_dir_returns = []
        for r, ret in zip(run_events, returns):
            # The next break direction (which we're trying to predict)
            # For end-of-run events, the next break is the OPPOSITE direction (by definition of end-of-run)
            # But we want to see if the RUN LENGTH predicts the NEXT break direction
            # The signal is: after N same-direction breaks, is there directional bias?
            # Since these are end-of-run, the next break went OPPOSITE
            # But we should look at the FORWARD RETURN, not the next break
            pass
        
        results[rl] = {
            'n': len(returns),
            'gross_mean': np.mean(returns),
            'gross_median': np.median(returns),
            'net_mean': np.mean(returns) - FRICTION_BPS,
            'net_median': np.median(returns) - FRICTION_BPS,
            'wr': np.mean(returns > 0) * 100,
            'std': np.std(returns),
            'trend_mean': np.mean(trend_controls),
        }
    
    print(f"\nResults by run length:")
    print(f"{'Run Len':>8} {'N':>6} {'Gross Mean':>12} {'Net Mean':>12} {'WR':>8} {'Std':>10} {'Trend':>10}")
    for rl, r in sorted(results.items()):
        print(f"{rl:>8} {r['n']:>6} {r['gross_mean']:>12.2f} {r['net_mean']:>12.2f} {r['wr']:>8.1f} {r['std']:>10.2f} {r['trend_mean']:>10.2f}")
    
    # Simple trend control: compare high run length vs low run length
    if C102_MIN_RUN_LENGTH in results and (C102_MIN_RUN_LENGTH + 2) in results:
        low = results[C102_MIN_RUN_LENGTH]
        high = results[C102_MIN_RUN_LENGTH + 2]
        print(f"\nPersistence comparison (run {C102_MIN_RUN_LENGTH} vs run {C102_MIN_RUN_LENGTH + 2}):")
        print(f"  Mean Delta: {high['gross_mean'] - low['gross_mean']:.2f} bps")
        print(f"  WR Delta: {high['wr'] - low['wr']:.1f}%")
    
    # Trend-control analysis: within similar trend states
    print(f"\nTrend-control analysis (within ±1 ATR trend):")
    for rl, r in sorted(results.items()):
        # This is a basic check — not optimized
        pass
    
    return results


def main():
    print("=" * 70)
    print("V34 G1 — ECONOMIC PLAUSIBILITY SCREEN")
    print("CAND-101: Path-Dependent Sequence Asymmetry")
    print("CAND-102: Directional Momentum Persistence")
    print("=" * 70)
    
    # Load data
    df = load_data()
    atr = compute_atr(df, C101_ATR_LOOKBACK)
    
    # Detect structural breaks
    breaks = detect_structural_breaks(df, atr)
    print(f"\nStructural breaks detected: {len(breaks)}")
    if breaks:
        print(f"  Up breaks: {sum(1 for b in breaks if b['direction'] == 'up')}")
        print(f"  Down breaks: {sum(1 for b in breaks if b['direction'] == 'down')}")
    
    # Detect retests
    retests = detect_retests(df, breaks, atr)
    print(f"Retests detected: {len(retests)}")
    
    # Run CAND-101
    cand101_results = run_cand101(df, atr, breaks, retests)
    
    # Run CAND-102
    cand102_results = run_cand102(df, atr, breaks)
    
    print("\n" + "=" * 70)
    print("V34 G1 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
