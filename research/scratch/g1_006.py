import pandas as pd
import numpy as np

print("Loading data...")
btc = pd.read_csv('data/m1/BTCUSD_M1.csv')
usa = pd.read_csv('data/m1/USATECHIDXUSD_M1.csv')

btc['timestamp'] = pd.to_datetime(btc['timestamp']).dt.tz_localize('UTC')
usa['timestamp'] = pd.to_datetime(usa['timestamp']).dt.tz_localize('UTC')

# CAND-G0-006: Crypto-to-Equity Risk-On Impulse Lead
print("Processing CAND-G0-006...")
btc_ny = btc.copy()
btc_ny['ts_ny'] = btc_ny['timestamp'].dt.tz_convert('America/New_York')
btc_ny = btc_ny.set_index('ts_ny')

btc_daily = btc_ny.resample('D').agg({'high': 'max', 'low': 'min', 'close': 'last'}).dropna()
btc_daily['atr'] = (btc_daily['high'] - btc_daily['low']).rolling(14).mean()
btc_daily['date'] = btc_daily.index.date

btc_0730 = btc_ny.between_time('07:30', '07:30').copy()
btc_0930 = btc_ny.between_time('09:30', '09:30').copy()
btc_0730['date'] = btc_0730.index.date
btc_0930['date'] = btc_0930.index.date

btc_move = btc_0930.merge(btc_0730, on='date', suffixes=('_0930', '_0730'))
btc_move['move'] = btc_move['close_0930'] - btc_move['open_0730']
btc_move = btc_move.merge(btc_daily[['date', 'atr']], on='date')
btc_move['trigger'] = btc_move['move'].abs() > 3 * btc_move['atr']

usa_ny = usa.copy()
usa_ny['ts_ny'] = usa_ny['timestamp'].dt.tz_convert('America/New_York')
usa_ny = usa_ny.set_index('ts_ny')
usa_0930 = usa_ny.between_time('09:30', '09:30').copy()
usa_1600 = usa_ny.between_time('16:00', '16:00').copy()
usa_0930['date'] = usa_0930.index.date
usa_1600['date'] = usa_1600.index.date

c6_events = btc_move[btc_move['trigger']].copy()
usa_trade = usa_0930.merge(usa_1600, on='date', suffixes=('_entry', '_exit'))
c6 = c6_events.merge(usa_trade, on='date')
c6['direction'] = np.where(c6['move'] > 0, 1, -1)
c6['gross_return'] = (c6['close_exit'] - c6['close_entry']) * c6['direction'] / c6['close_entry']

print(f"CAND-G0-006 Events: {len(c6)}")
if len(c6) > 0:
    print(f"CAND-G0-006 Median Gross: {c6['gross_return'].median() * 10000:.2f} bps")
    print(f"CAND-G0-006 Mean Gross: {c6['gross_return'].mean() * 10000:.2f} bps")
    print(f"CAND-G0-006 Lower Quartile: {c6['gross_return'].quantile(0.25) * 10000:.2f} bps")
