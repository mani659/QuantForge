import pandas as pd
from datetime import timezone
from research.g6_forward.tests_g6 import generate_synthetic_data
from research.g6_forward.signal_engine import Cand015SignalEngine
from research.g6_forward.cand015_identity import FROZEN_CAND015_IDENTITY

engine = Cand015SignalEngine(FROZEN_CAND015_IDENTITY)
df_ndx, _ = generate_synthetic_data()
records = df_ndx.iloc[:69905].to_dict('records')
for row in records:
    row['symbol'] = "USATECHIDXUSD"
    row['observation_timestamp'] = row['timestamp']
engine.m1_buffer_ndx = records

eval_time = df_ndx.iloc[69905]['timestamp']
signal = engine._evaluate_signal(eval_time)
print("Signal 1:", signal)

future_tick = df_ndx.iloc[69905].copy()
future_tick['timestamp'] = future_tick['timestamp'] + pd.Timedelta(hours=4)
future_tick['high'] += 500000
future_tick['low'] -= 500000

future_record = future_tick.to_dict()
future_record['symbol'] = "USATECHIDXUSD"
future_record['observation_timestamp'] = future_record['timestamp']
engine.m1_buffer_ndx.append(future_record)

print("eval_time:", eval_time)
# Stepping through
df = pd.DataFrame(engine.m1_buffer_ndx)
df.set_index('observation_timestamp', inplace=True)
df_m5 = df.resample('5min', label='left', closed='left').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()

df_d1 = df.resample('1D').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
print("df_d1 tail:\n", df_d1.tail())

from research.scratch.g5_cand015 import calc_atr
atr_ndx, _ = calc_atr(df_m5[['high', 'low', 'close']], 14)
df_m5['atr'] = atr_ndx
df_m5['atr_30d'] = df_m5['atr'].rolling(8640).mean()

d1_atr, _ = calc_atr(df_d1, 14)
df_d1['d1_atr'] = d1_atr
df_d1['d1_atr_30d'] = df_d1['d1_atr'].rolling(30).mean()

latest_complete_idx = None
for idx in reversed(df_m5.index):
    if eval_time >= idx + pd.Timedelta(minutes=5):
        latest_complete_idx = idx
        break

print("latest_complete_idx:", latest_complete_idx)
latest_m5 = df_m5.loc[latest_complete_idx]
print("latest_m5 atr_30d:", latest_m5['atr_30d'])
print("ndx_ret:", abs(latest_m5['close'] - latest_m5['open']))
print("shock:", abs(latest_m5['close'] - latest_m5['open']) > (3 * latest_m5['atr_30d']))

latest_date = latest_complete_idx.date()
d1_shifted = df_d1[df_d1.index.date < latest_date]
print("d1_shifted length:", len(d1_shifted))

latest_d1 = d1_shifted.iloc[-1]
d1_atr = latest_d1['d1_atr']
d1_atr_30d = latest_d1['d1_atr_30d']
print("d1_atr:", d1_atr, "d1_atr_30d:", d1_atr_30d)

if pd.isna(d1_atr) or pd.isna(d1_atr_30d):
    print("isna returns none")
else:
    print("returns signal")

signal2 = engine._evaluate_signal(eval_time)
print("Signal 2:", signal2)
