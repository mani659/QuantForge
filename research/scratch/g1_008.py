import pandas as pd
import numpy as np

print("Loading data for CAND-008...")
xau = pd.read_csv('data/m1/XAUUSD_M1.csv')
xag = pd.read_csv('data/m1/XAGUSD_M1.csv')

xau['timestamp'] = pd.to_datetime(xau['timestamp']).dt.tz_localize('UTC')
xag['timestamp'] = pd.to_datetime(xag['timestamp']).dt.tz_localize('UTC')

xau_ny = xau.copy()
xau_ny['ts_ny'] = xau_ny['timestamp'].dt.tz_convert('America/New_York')
xau_ny = xau_ny.set_index('ts_ny')

xag_ny = xag.copy()
xag_ny['ts_ny'] = xag_ny['timestamp'].dt.tz_convert('America/New_York')
xag_ny = xag_ny.set_index('ts_ny')

xau_d = xau_ny.resample('D').agg({'close': 'last'}).dropna()
xag_d = xag_ny.resample('D').agg({'close': 'last'}).dropna()

xau_d['ret'] = xau_d['close'].pct_change()
xag_d['ret'] = xag_d['close'].pct_change()

df = xau_d.join(xag_d, lsuffix='_xau', rsuffix='_xag', how='inner')
df['trigger'] = (df['ret_xau'] > 0.015) & (df['ret_xag'] < -0.010)

triggers = df[df['trigger']].copy()
print(f"Total triggers found: {len(triggers)}")

results = []
for date, row in triggers.iterrows():
    idx = df.index.get_loc(date)
    if idx + 5 < len(df):
        exit_row = df.iloc[idx + 5]
        ret_xau = (exit_row['close_xau'] - row['close_xau']) / row['close_xau']
        ret_xag = (row['close_xag'] - exit_row['close_xag']) / row['close_xag']
        results.append((ret_xau + ret_xag)) # Not dividing by 2 as the instruction says "long XAU return + short XAG return"

if results:
    res = np.array(results)
    print(f"CAND-G0-008 Events: {len(res)}")
    print(f"CAND-G0-008 Median Gross: {np.median(res) * 10000:.2f} bps")
    print(f"CAND-G0-008 Mean Gross: {np.mean(res) * 10000:.2f} bps")
    print(f"CAND-G0-008 Lower Quartile: {np.percentile(res, 25) * 10000:.2f} bps")
else:
    print("CAND-G0-008 Events: 0")
