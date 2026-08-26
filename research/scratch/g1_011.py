import pandas as pd
import numpy as np

print("Loading XAUUSD data for CAND-G0-011...")
df = pd.read_csv('data/m1/XAUUSD_M1.csv')
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC').dt.tz_convert('America/New_York')
df = df.set_index('timestamp').sort_index()

print("Resampling to M5...")
df_m5 = df.resample('5min').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()

print("Computing Indicators...")
df_m5['sma10'] = df_m5['close'].rolling(10).mean()

# RSI(14)
delta = df_m5['close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df_m5['rsi'] = 100 - (100 / (1 + rs))

# 20-bar rolling extrema
df_m5['swing_high'] = df_m5['high'] == df_m5['high'].rolling(21, center=True).max()
df_m5['swing_low'] = df_m5['low'] == df_m5['low'].rolling(21, center=True).min()

df_m5['swing_high_val'] = np.where(df_m5['swing_high'], df_m5['high'], np.nan)
df_m5['swing_low_val'] = np.where(df_m5['swing_low'], df_m5['low'], np.nan)

# Only evaluate swings once confirmed (10 bars after the extreme)
df_m5_reset = df_m5.reset_index()

print("Searching for Double Tops/Bottoms...")
events = 0
valid_entries = 0
results = []

recent_highs = []
recent_lows = []

for i in range(21, len(df_m5_reset) - 48): # 48 bars is 4 hours on M5
    row = df_m5_reset.iloc[i]
    
    # We check if 10 bars ago was a swing
    idx_10_ago = i - 10
    row_10_ago = df_m5_reset.iloc[idx_10_ago]
    
    if row_10_ago['swing_high']:
        recent_highs.append((idx_10_ago, row_10_ago['high'], row_10_ago['rsi']))
        # Keep only those within 100 bars
        recent_highs = [h for h in recent_highs if i - h[0] <= 100]
        
        # Check for double top
        for h in recent_highs[:-1]: # Don't check against self
            dist = idx_10_ago - h[0]
            if 20 <= dist <= 100:
                price_diff_pct = abs(row_10_ago['high'] - h[1]) / h[1]
                if price_diff_pct <= 0.001: # 0.1%
                    rsi_diff = h[2] - row_10_ago['rsi']
                    if rsi_diff >= 5: # Divergence (lower high on RSI)
                        # Wait for confirmation: close < sma10
                        # Since i is currently 10 bars past the second top, we check if price is already confirmed
                        # Or we search forward from i to i+20 for a close < sma10
                        for j in range(i, i+20):
                            if j < len(df_m5_reset)-48 and df_m5_reset.iloc[j]['close'] < df_m5_reset.iloc[j]['sma10']:
                                events += 1
                                valid_entries += 1
                                entry_price = df_m5_reset.iloc[j]['close']
                                exit_price = df_m5_reset.iloc[j+48]['close']
                                ret = (entry_price - exit_price) / entry_price # Short
                                results.append(ret)
                                recent_highs.clear() # Prevent double counting
                                break

    if row_10_ago['swing_low']:
        recent_lows.append((idx_10_ago, row_10_ago['low'], row_10_ago['rsi']))
        recent_lows = [l for l in recent_lows if i - l[0] <= 100]
        
        for l in recent_lows[:-1]:
            dist = idx_10_ago - l[0]
            if 20 <= dist <= 100:
                price_diff_pct = abs(row_10_ago['low'] - l[1]) / l[1]
                if price_diff_pct <= 0.001:
                    rsi_diff = row_10_ago['rsi'] - l[2]
                    if rsi_diff >= 5: # Higher low on RSI
                        for j in range(i, i+20):
                            if j < len(df_m5_reset)-48 and df_m5_reset.iloc[j]['close'] > df_m5_reset.iloc[j]['sma10']:
                                events += 1
                                valid_entries += 1
                                entry_price = df_m5_reset.iloc[j]['close']
                                exit_price = df_m5_reset.iloc[j+48]['close']
                                ret = (exit_price - entry_price) / entry_price # Long
                                results.append(ret)
                                recent_lows.clear()
                                break

print(f"CAND-G0-011 Total Setups: {events}")
print(f"CAND-G0-011 Valid Entries: {valid_entries}")

if results:
    res = np.array(results)
    print(f"CAND-G0-011 Median Gross: {np.median(res) * 10000:.2f} bps")
    print(f"CAND-G0-011 Mean Gross: {np.mean(res) * 10000:.2f} bps")
    print(f"CAND-G0-011 Lower Quartile: {np.percentile(res, 25) * 10000:.2f} bps")
else:
    print("CAND-G0-011 Events: 0")
