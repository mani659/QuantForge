import pandas as pd
import numpy as np
from datetime import timedelta

print("Loading data for CAND-007...")
# We use EURUSD for this as per scope (EURUSD, XAUUSD, XAGUSD)
eur = pd.read_csv('data/m1/EURUSD_M1.csv')
eur['timestamp'] = pd.to_datetime(eur['timestamp']).dt.tz_localize('UTC')

df_ny = eur.copy()
df_ny['ts_ny'] = df_ny['timestamp'].dt.tz_convert('America/New_York')
df_ny = df_ny.set_index('ts_ny')
df_ny = df_ny.sort_index()

# Daily ATR
df_daily = df_ny.resample('D').agg({'high': 'max', 'low': 'min', 'close': 'last'}).dropna()
df_daily['atr'] = (df_daily['high'] - df_daily['low']).rolling(14).mean()

df_ny['prev_time'] = df_ny.index.to_series().shift(1)
df_ny['prev_close'] = df_ny['close'].shift(1)
df_ny['time_diff'] = (df_ny.index - df_ny['prev_time']).dt.total_seconds() / 3600

# Identify weekends (gaps > 24h)
gaps = df_ny[df_ny['time_diff'] > 24].copy()
gaps['gap_size'] = (gaps['open'] - gaps['prev_close']).abs()
gaps['gap_dir'] = np.where(gaps['open'] > gaps['prev_close'], 1, -1)
gaps['date'] = gaps.index.date
gaps['prev_date'] = gaps['prev_time'].dt.date

# Merge ATR
atr_df = df_daily[['atr']].reset_index()
atr_df['prev_date'] = atr_df['ts_ny'].dt.date
gaps['ts_ny'] = gaps.index
gaps = gaps.merge(atr_df[['prev_date', 'atr']], on='prev_date')
gaps['trigger'] = gaps['gap_size'] > 1.5 * gaps['atr']
gaps = gaps[gaps['trigger']].copy()

print(f"Total triggers found: {len(gaps)}")

results = []
for idx, row in gaps.iterrows():
    t_open = row['ts_ny']
    t_end = t_open + timedelta(hours=2)
    t_fri = t_open + timedelta(days=5 - t_open.weekday()) # Friday
    t_fri_close = t_fri.replace(hour=16, minute=59, second=0) # NY time Friday close
    
    # Check if filled
    window = df_ny.loc[t_open:t_end]
    if row['gap_dir'] == 1:
        filled = window['low'].min() <= row['prev_close']
    else:
        filled = window['high'].max() >= row['prev_close']
        
    if not filled:
        # Entry is hour-2 close
        entry_bar = window.iloc[-1]
        
        # Exit is Friday close
        future_window = df_ny.loc[t_end:t_fri_close]
        if len(future_window) > 0:
            exit_bar = future_window.iloc[-1]
            ret = (exit_bar['close'] - entry_bar['close']) * row['gap_dir'] / entry_bar['close']
            results.append(ret)

if results:
    res = np.array(results)
    print(f"CAND-G0-007 Events: {len(res)}")
    print(f"CAND-G0-007 Median Gross: {np.median(res) * 10000:.2f} bps")
    print(f"CAND-G0-007 Mean Gross: {np.mean(res) * 10000:.2f} bps")
    print(f"CAND-G0-007 Lower Quartile: {np.percentile(res, 25) * 10000:.2f} bps")
else:
    print("CAND-G0-007 Events: 0")
