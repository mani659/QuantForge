"""
SEED-002 Relational Discovery Experiment (Vectorized)
CAND-083 × CAND-081

Frozen hypothesis:
Does a structural failure preceded by CAND-083 accumulated rejection
condition produce materially different downstream economics when the
CAND-081 post-failure trapped-participant condition occurs?

Input A: CAND-083 (pre-failure accumulated rejection pressure)
Input B: CAND-081 (post-failure trapped participant condition)

Frozen definitions from V28 G1 and V27 G1 artifacts.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import time

# =============================================================================
# FROZEN PARAMETERS — DO NOT MODIFY
# =============================================================================

# CAND-083 Parameters
STRUCTURAL_LOOKBACK = 20
REJECTION_WINDOW = 50
REJECTION_TOLERANCE = 1  # bps
REJECTION_CONFIRM_BARS = 5
CAND083_TREATMENT_REJ_COUNT = 3

# CAND-081 Parameters
CAND081_BREAKOUT_THRESHOLD = 3  # bps
CAND081_FAILURE_WINDOW = 5

# Common
HOLDING_PERIOD = 60  # 60 bars on M1 = 60 min
FRICTION_BPS = 2.0
MARKET = "USATECHIDXUSD"
TIMEFRAME = "M1"

# SEED-002
CAND083_PRECEDENCE_WINDOW = 50


def load_data():
    """Load USATECHIDXUSD M1 data."""
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "m1" / "USATECHIDXUSD_M1.csv"
    print(f"Loading data from: {data_path}")
    df = pd.read_csv(data_path)
    df.columns = [c.lower().strip() for c in df.columns]

    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
    elif 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime').sort_index()
    elif 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time').sort_index()

    print(f"Data shape: {df.shape}")
    print(f"Date range: {df.index[0]} to {df.index[-1]}")
    return df


def compute_structural_levels(df):
    """Vectorized 20-bar rolling high/low from PRIOR bars only.
    
    The structural level must exclude the current bar so that
    the current bar can break above/below the level.
    We use .shift(1) to look back at the prior 20 bars.
    """
    df = df.copy()
    # shift(1): the level is the max/min of the 20 bars BEFORE the current bar
    df['struct_high'] = df['high'].rolling(STRUCTURAL_LOOKBACK).max().shift(1)
    df['struct_low'] = df['low'].rolling(STRUCTURAL_LOOKBACK).min().shift(1)
    return df


def detect_cand081_events_vectorized(df):
    """
    Vectorized CAND-081 detection: structural breakout followed by failure.

    For each bar, check if within the last FAILURE_WINDOW bars:
      - a bar broke struct_high by >= breakout threshold (long_failure setup)
      - and the current bar closes back below struct_high

    Same logic for struct_low.
    """
    print("  Computing structural levels...")
    df = compute_structural_levels(df)

    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    struct_h = df['struct_high'].values
    struct_l = df['struct_low'].values
    n = len(df)

    events = []

    print(f"  Scanning {n} bars for CAND-081 events...")

    # Pre-compute breakout signals vectorized
    # Upside breakout: close > struct_high + threshold in bps
    up_breakout_bps = np.where(
        struct_h > 0,
        (close - struct_h) / struct_h * 10000,
        0
    )
    up_breakout = up_breakout_bps >= CAND081_BREAKOUT_THRESHOLD

    # Downside breakout: close < struct_low - threshold in bps
    dn_breakout_bps = np.where(
        struct_l > 0,
        (struct_l - close) / struct_l * 10000,
        0
    )
    dn_breakout = dn_breakout_bps >= CAND081_BREAKOUT_THRESHOLD

    # For each bar, look back up to FAILURE_WINDOW bars
    # to see if a breakout occurred and now the price failed back
    for i in range(STRUCTURAL_LOOKBACK + CAND081_FAILURE_WINDOW, n):
        sh = struct_h[i]
        sl = struct_l[i]
        if np.isnan(sh) or np.isnan(sl):
            continue

        # Check upside breakout failure
        for j in range(1, min(CAND081_FAILURE_WINDOW + 1, i - STRUCTURAL_LOOKBACK + 1)):
            bi = i - j
            if up_breakout[bi]:
                # Current bar closes back below struct_high (failure confirmed)
                if close[i] < sh:
                    events.append({
                        'event_idx': i,
                        'level': sh,
                        'direction': 'long_failure',
                        'breakout_idx': bi,
                        'breakout_bps': float(up_breakout_bps[bi])
                    })
                    break

        # Check downside breakout failure
        for j in range(1, min(CAND081_FAILURE_WINDOW + 1, i - STRUCTURAL_LOOKBACK + 1)):
            bi = i - j
            if dn_breakout[bi]:
                # Current bar closes back above struct_low (failure confirmed)
                if close[i] > sl:
                    events.append({
                        'event_idx': i,
                        'level': sl,
                        'direction': 'short_failure',
                        'breakout_idx': bi,
                        'breakout_bps': float(dn_breakout_bps[bi])
                    })
                    break

    return events


def count_rejections_vectorized(df, event_idx, level, direction):
    """
    Vectorized rejection count at a structural level.

    A rejection = price touches level (within tolerance) and closes back
    through level within REJECTION_CONFIRM_BARS.

    Counts within REJECTION_WINDOW bars ending at event_idx.
    """
    start = max(0, event_idx - REJECTION_WINDOW)
    end = event_idx

    if start >= end:
        return 0

    if direction == 'above':
        # Resistance rejection: high touches level, then close < level within confirm bars
        highs = df['high'].iloc[start:end].values
        closes = df['close'].iloc[start:end].values
        tol = REJECTION_TOLERANCE * 0.001 * level
        touched = np.abs(highs - level) <= tol

        count = 0
        for k in range(len(touched)):
            if touched[k]:
                # Check if any subsequent bar closes back through level
                confirm_end = min(k + REJECTION_CONFIRM_BARS + 1, len(closes))
                if k + 1 < confirm_end:
                    if np.any(closes[k+1:confirm_end] < level):
                        count += 1
        return count
    else:
        # Support rejection: low touches level, then close > level within confirm bars
        lows = df['low'].iloc[start:end].values
        closes = df['close'].iloc[start:end].values
        tol = REJECTION_TOLERANCE * 0.001 * level
        touched = np.abs(lows - level) <= tol

        count = 0
        for k in range(len(touched)):
            if touched[k]:
                confirm_end = min(k + REJECTION_CONFIRM_BARS + 1, len(closes))
                if k + 1 < confirm_end:
                    if np.any(closes[k+1:confirm_end] > level):
                        count += 1
        return count


def deduplicate_events(events, min_gap=HOLDING_PERIOD):
    """Remove overlapping events (keep first occurrence)."""
    if not events:
        return []
    deduped = [events[0]]
    for evt in events[1:]:
        if evt['event_idx'] - deduped[-1]['event_idx'] >= min_gap:
            deduped.append(evt)
    return deduped


def run_experiment():
    """Execute the SEED-002 relational discovery experiment."""
    t0 = time.time()

    print("=" * 70)
    print("SEED-002 RELATIONAL DISCOVERY EXPERIMENT")
    print("CAND-083 × CAND-081")
    print("=" * 70)

    # Load data
    df = load_data()

    # Detect CAND-081 events
    print("\nDetecting CAND-081 events (structural failure trap)...")
    events = detect_cand081_events_vectorized(df)
    print(f"Raw CAND-081 events: {len(events)}")

    # Deduplicate
    events = deduplicate_events(events)
    print(f"After deduplication: {len(events)}")

    # Classify events by CAND-083 precondition
    treatment_events = []
    control_events = []

    print("\nChecking CAND-083 preconditions...")
    t1 = time.time()
    for idx, evt in enumerate(events):
        if (idx + 1) % 100 == 0:
            elapsed = time.time() - t1
            print(f"  ... processed {idx+1}/{len(events)} ({elapsed:.1f}s)")

        direction_for_rejection = 'above' if evt['direction'] == 'long_failure' else 'below'
        rej_count = count_rejections_vectorized(
            df, evt['event_idx'], evt['level'], direction_for_rejection
        )
        evt['rejection_count'] = rej_count
        evt['has_cand083'] = rej_count >= CAND083_TREATMENT_REJ_COUNT

        if evt['has_cand083']:
            treatment_events.append(evt)
        else:
            control_events.append(evt)

    print(f"\nCAND-081 WITH CAND-083 (treatment): {len(treatment_events)}")
    print(f"CAND-081 WITHOUT CAND-083 (control): {len(control_events)}")
    print(f"Total classified: {len(treatment_events) + len(control_events)}")

    # Compute downstream returns
    print("\nComputing downstream returns...")

    close_vals = df['close'].values

    treatment_returns = []
    for evt in treatment_events:
        eidx = evt['event_idx']
        if eidx + HOLDING_PERIOD >= len(close_vals):
            continue
        entry = close_vals[eidx]
        exit_ = close_vals[eidx + HOLDING_PERIOD]
        if evt['direction'] == 'long_failure':
            ret_bps = (entry - exit_) / entry * 10000
        else:
            ret_bps = (exit_ - entry) / entry * 10000
        net = ret_bps - FRICTION_BPS
        treatment_returns.append(net)
        evt['net_return_bps'] = net
        evt['gross_return_bps'] = ret_bps

    control_returns = []
    for evt in control_events:
        eidx = evt['event_idx']
        if eidx + HOLDING_PERIOD >= len(close_vals):
            continue
        entry = close_vals[eidx]
        exit_ = close_vals[eidx + HOLDING_PERIOD]
        if evt['direction'] == 'long_failure':
            ret_bps = (entry - exit_) / entry * 10000
        else:
            ret_bps = (exit_ - entry) / entry * 10000
        net = ret_bps - FRICTION_BPS
        control_returns.append(net)
        evt['net_return_bps'] = net
        evt['gross_return_bps'] = ret_bps

    treatment_returns = np.array(treatment_returns)
    control_returns = np.array(control_returns)

    elapsed_total = time.time() - t0

    # =============================================================================
    # RESULTS
    # =============================================================================
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    # Population counts
    print(f"\n--- POPULATION COUNTS ---")
    print(f"CAND-081 Baseline (all events): {len(events)}")
    print(f"CAND-081 WITHOUT CAND-083 (control): {len(control_returns)}")
    print(f"CAND-081 WITH CAND-083 (treatment): {len(treatment_returns)}")

    delta_mean = None
    delta_median = None

    # Treatment statistics
    print(f"\n--- TREATMENT (CAND-081 WITH CAND-083) ---")
    print(f"N: {len(treatment_returns)}")
    if len(treatment_returns) > 0:
        print(f"Net Mean: {np.mean(treatment_returns):.2f} bps")
        print(f"Net Median: {np.median(treatment_returns):.2f} bps")
        print(f"Win Rate: {np.mean(treatment_returns > 0) * 100:.1f}%")
        print(f"Std: {np.std(treatment_returns):.2f} bps")
        print(f"Worst: {np.min(treatment_returns):.2f} bps")
        print(f"Best: {np.max(treatment_returns):.2f} bps")

        # Gross treatment stats
        t_gross = [e['gross_return_bps'] for e in treatment_events if 'gross_return_bps' in e]
        print(f"Gross Mean: {np.mean(t_gross):.2f} bps")
        print(f"Gross Median: {np.median(t_gross):.2f} bps")

    # Control statistics
    print(f"\n--- CONTROL (CAND-081 WITHOUT CAND-083) ---")
    print(f"N: {len(control_returns)}")
    if len(control_returns) > 0:
        print(f"Net Mean: {np.mean(control_returns):.2f} bps")
        print(f"Net Median: {np.median(control_returns):.2f} bps")
        print(f"Win Rate: {np.mean(control_returns > 0) * 100:.1f}%")
        print(f"Std: {np.std(control_returns):.2f} bps")
        print(f"Worst: {np.min(control_returns):.2f} bps")
        print(f"Best: {np.max(control_returns):.2f} bps")

        # Gross control stats
        c_gross = [e['gross_return_bps'] for e in control_events if 'gross_return_bps' in e]
        print(f"Gross Mean: {np.mean(c_gross):.2f} bps")
        print(f"Gross Median: {np.median(c_gross):.2f} bps")

    # Delta
    print(f"\n--- TREATMENT VS CONTROL DELTA ---")
    if len(treatment_returns) > 0 and len(control_returns) > 0:
        delta_mean = float(np.mean(treatment_returns) - np.mean(control_returns))
        delta_median = float(np.median(treatment_returns) - np.median(control_returns))
        print(f"Delta Mean: {delta_mean:+.2f} bps")
        print(f"Delta Median: {delta_median:+.2f} bps")

        if delta_mean > 0 and delta_median > 0:
            print("Classification: TREATMENT SUPERIOR (both mean and median)")
        elif delta_mean > 0:
            print("Classification: MIXED (mean positive, median negative)")
        elif delta_median > 0:
            print("Classification: MIXED (mean negative, median positive)")
        else:
            print("Classification: CONTROL SUPERIOR")

    # Baseline comparison
    all_returns = np.concatenate([treatment_returns, control_returns]) if len(treatment_returns) > 0 or len(control_returns) > 0 else np.array([])
    print(f"\n--- BASELINE (ALL CAND-081 EVENTS WITH RETURNS) ---")
    print(f"N: {len(all_returns)}")
    if len(all_returns) > 0:
        print(f"Net Mean: {np.mean(all_returns):.2f} bps")
        print(f"Net Median: {np.median(all_returns):.2f} bps")
        print(f"Win Rate: {np.mean(all_returns > 0) * 100:.1f}%")

    # Treatment vs baseline
    if len(treatment_returns) > 0 and len(all_returns) > 0:
        d_mean = float(np.mean(treatment_returns) - np.mean(all_returns))
        d_median = float(np.median(treatment_returns) - np.median(all_returns))
        print(f"\nTreatment vs Baseline Delta Mean: {d_mean:+.2f} bps")
        print(f"Treatment vs Baseline Delta Median: {d_median:+.2f} bps")

    # Distribution assessment
    print(f"\n--- DISTRIBUTION ASSESSMENT ---")
    if len(treatment_returns) > 1:
        sorted_t = np.sort(treatment_returns)
        print(f"Treatment excluding best: Mean={np.mean(sorted_t[:-1]):.2f} bps, Median={np.median(sorted_t[:-1]):.2f} bps")
        # Quartile analysis
        q25, q50, q75 = np.percentile(treatment_returns, [25, 50, 75])
        print(f"Treatment quartiles: Q25={q25:.2f}, Q50={q50:.2f}, Q75={q75:.2f}")

    if len(control_returns) > 1:
        sorted_c = np.sort(control_returns)
        print(f"Control excluding best: Mean={np.mean(sorted_c[:-1]):.2f} bps, Median={np.median(sorted_c[:-1]):.2f} bps")
        q25, q50, q75 = np.percentile(control_returns, [25, 50, 75])
        print(f"Control quartiles: Q25={q25:.2f}, Q50={q50:.2f}, Q75={q75:.2f}")

    # Rejection count distribution in treatment
    if treatment_events:
        rej_counts = [e['rejection_count'] for e in treatment_events]
        print(f"\n--- REJECTION COUNT DISTRIBUTION (TREATMENT) ---")
        print(f"Mean rejection count: {np.mean(rej_counts):.1f}")
        print(f"Median rejection count: {np.median(rej_counts):.1f}")
        print(f"Min: {min(rej_counts)}, Max: {max(rej_counts)}")

    # Direction breakdown
    print(f"\n--- DIRECTION BREAKDOWN ---")
    for direction in ['long_failure', 'short_failure']:
        t_dir = [r for r, e in zip(treatment_returns, treatment_events) if e['direction'] == direction]
        c_dir = [r for r, e in zip(control_returns, control_events) if e['direction'] == direction]
        if t_dir:
            print(f"  {direction} treatment: N={len(t_dir)}, Mean={np.mean(t_dir):.2f}, Median={np.median(t_dir):.2f}")
        if c_dir:
            print(f"  {direction} control: N={len(c_dir)}, Mean={np.mean(c_dir):.2f}, Median={np.median(c_dir):.2f}")

    # Summary
    print(f"\n{'=' * 70}")
    print("SEED-002 DISCOVERY SUMMARY")
    print(f"{'=' * 70}")
    print(f"Hypothesis: Does CAND-083 add information to CAND-081?")
    print(f"Treatment N: {len(treatment_returns)}")
    print(f"Control N: {len(control_returns)}")
    if delta_mean is not None:
        print(f"Delta Mean: {delta_mean:+.2f} bps")
        print(f"Delta Median: {delta_median:+.2f} bps")
    if len(treatment_returns) > 0:
        print(f"Treatment Net Mean: {np.mean(treatment_returns):.2f} bps")
    if len(control_returns) > 0:
        print(f"Control Net Mean: {np.mean(control_returns):.2f} bps")
    print(f"Elapsed: {elapsed_total:.1f}s")

    return {
        'treatment_n': len(treatment_returns),
        'control_n': len(control_returns),
        'baseline_n': len(all_returns),
        'treatment_mean': float(np.mean(treatment_returns)) if len(treatment_returns) > 0 else None,
        'control_mean': float(np.mean(control_returns)) if len(control_returns) > 0 else None,
        'treatment_median': float(np.median(treatment_returns)) if len(treatment_returns) > 0 else None,
        'control_median': float(np.median(control_returns)) if len(control_returns) > 0 else None,
        'delta_mean': delta_mean,
        'delta_median': delta_median,
        'treatment_wr': float(np.mean(treatment_returns > 0)) if len(treatment_returns) > 0 else None,
        'control_wr': float(np.mean(control_returns > 0)) if len(control_returns) > 0 else None,
        'treatment_std': float(np.std(treatment_returns)) if len(treatment_returns) > 0 else None,
        'control_std': float(np.std(control_returns)) if len(control_returns) > 0 else None,
    }


if __name__ == "__main__":
    results = run_experiment()
    print("\n\nResults dict:", results)
