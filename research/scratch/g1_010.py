import pandas as pd
import numpy as np
from datetime import timedelta

print("Loading EURUSD data for CAND-G0-010...")
df = pd.read_csv('data/m1/EURUSD_M1.csv')
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC').dt.tz_convert('America/New_York')
df = df.set_index('timestamp').sort_index()

# Resample to M5
print("Resampling to M5...")
df_m5 = df.resample('5min').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()

# Daily High/Low
print("Computing Daily High/Low...")
df_daily = df.resample('D').agg({'high':'max', 'low':'min'}).shift(1).dropna()
df_daily.columns = ['prev_high', 'prev_low']

# Merge Daily H/L into M5
df_m5['date'] = df_m5.index.date
df_daily.index = df_daily.index.date
df_m5 = df_m5.reset_index().merge(df_daily, left_on='date', right_index=True, how='left').set_index('timestamp')

# Define Swings
# Central bar higher than 3 before and 3 after
print("Detecting Swings...")
df_m5['swing_high'] = df_m5['high'] == df_m5['high'].rolling(7, center=True).max()
df_m5['swing_low'] = df_m5['low'] == df_m5['low'].rolling(7, center=True).min()

df_m5['swing_high_val'] = np.where(df_m5['swing_high'], df_m5['high'], np.nan)
df_m5['swing_low_val'] = np.where(df_m5['swing_low'], df_m5['low'], np.nan)

# Forward fill previous swing highs and lows
# Because a swing is only confirmed 3 bars later, the actual *known* value is delayed by 3 bars.
df_m5['known_swing_high'] = df_m5['swing_high_val'].shift(3).ffill()
df_m5['known_swing_low'] = df_m5['swing_low_val'].shift(3).ffill()

# Detect sweeps
# Price crosses the POI (previous high/low)
df_m5['sweep_high'] = df_m5['high'] > df_m5['prev_high']
df_m5['sweep_low'] = df_m5['low'] < df_m5['prev_low']

# State machine for CHOCH
# Once a sweep occurs, look for a CHOCH
# CHOCH down: price sweeps high, then closes below the immediately preceding M5 swing low
# CHOCH up: price sweeps low, then closes above the immediately preceding M5 swing high

# We will just do a simplified window search to keep it fast and deterministic.
# We look for rows where close < known_swing_low and there was a sweep_high in the recent N bars (e.g. 12 bars = 1 hour)
# Wait, "The M5 close breaks (closes beyond) the immediately preceding M5 opposing swing."

print("Detecting CHOCH events...")
results = []
df_m5_reset = df_m5.reset_index()

# Keep track of recent sweeps
recent_sweep_high_idx = -1
recent_sweep_low_idx = -1

valid_entries = 0
events = 0

for i in range(12, len(df_m5_reset) - 24): # 24 bars is 2 hours
    row = df_m5_reset.iloc[i]
    
    if row['sweep_high']:
        recent_sweep_high_idx = i
    if row['sweep_low']:
        recent_sweep_low_idx = i
        
    # Check CHOCH down
    if recent_sweep_high_idx > 0 and (i - recent_sweep_high_idx) <= 24:
        # Swept high recently
        if row['close'] < row['known_swing_low']:
            # CHOCH down!
            events += 1
            entry_price = df_m5_reset.iloc[i+1]['open']
            # Exit 2 hours later (24 bars)
            exit_price = df_m5_reset.iloc[i+24]['close']
            ret = (entry_price - exit_price) / entry_price # Short
            results.append(ret)
            valid_entries += 1
            recent_sweep_high_idx = -1 # Reset state
            
    # Check CHOCH up
    if recent_sweep_low_idx > 0 and (i - recent_sweep_low_idx) <= 24:
        if row['close'] > row['known_swing_high']:
            # CHOCH up!
            events += 1
            entry_price = df_m5_reset.iloc[i+1]['open']
            exit_price = df_m5_reset.iloc[i+24]['close']
            ret = (exit_price - entry_price) / entry_price # Long
            results.append(ret)
            valid_entries += 1
            recent_sweep_low_idx = -1

print(f"CAND-G0-010 Total POI/CHOCH Events: {events}")
print(f"CAND-G0-010 Valid Entries: {valid_entries}")

if results:
    res = np.array(results)
    print(f"CAND-G0-010 Median Gross: {np.median(res) * 10000:.2f} bps")
    print(f"CAND-G0-010 Mean Gross: {np.mean(res) * 10000:.2f} bps")
    print(f"CAND-G0-010 Lower Quartile: {np.percentile(res, 25) * 10000:.2f} bps")
else:
    print("CAND-G0-010 Events: 0")
