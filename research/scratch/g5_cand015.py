import pandas as pd
import numpy as np
import time

def wilder_smoothing(s, n):
    res = np.zeros(len(s))
    res[0] = np.nan
    first_valid = s.first_valid_index()
    if first_valid is None:
        return pd.Series(res, index=s.index)
    idx_start = s.index.get_loc(first_valid)
    first_val = s.iloc[idx_start:idx_start+n].mean()
    idx_start = idx_start + n - 1
    if idx_start >= len(res):
        return pd.Series(res, index=s.index)
    res[idx_start] = first_val
    for i in range(idx_start + 1, len(s)):
        res[i] = res[i-1] + (s.iloc[i] - res[i-1]) / n
    return pd.Series(res, index=s.index)

def calc_atr(df, n=14):
    high = df['high']
    low = df['low']
    close = df['close']
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return wilder_smoothing(tr, n), tr

def run_g5():
    print("Loading Production Data (M1)...")
    
    # Load M1 raw data first
    raw_ndx = pd.read_csv("data/m1/USATECHIDXUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp')
    raw_btc = pd.read_csv("data/m1/BTCUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp')
    
    # Create the identical M5 view for signal generation
    df_ndx = raw_ndx.resample('5min', label='left', closed='left').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    df_btc = raw_btc.resample('5min', label='left', closed='left').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    
    df = df_ndx[['open', 'close', 'high', 'low']].join(df_btc[['open', 'high', 'low', 'close']], rsuffix='_btc', how='inner')
    df.dropna(inplace=True)
    
    atr_ndx, _ = calc_atr(df[['high', 'low', 'close']], 14)
    df['atr'] = atr_ndx
    df['atr_30d'] = df['atr'].rolling(8640).mean() # 8640 M5 bars = 30 days
    
    df_d1 = df_ndx.resample('1D').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    d1_atr, _ = calc_atr(df_d1, 14)
    df_d1['d1_atr'] = d1_atr
    df_d1['d1_atr_30d'] = df_d1['d1_atr'].rolling(30).mean()
    df_d1_shifted = df_d1.shift(1)[['d1_atr', 'd1_atr_30d']]
    df_d1_shifted.index = df_d1_shifted.index.date
    
    df['date'] = df.index.date
    df = df.merge(df_d1_shifted, left_on='date', right_index=True, how='left')
    
    df['ndx_ret'] = (df['close'] - df['open']).abs()
    df['shock'] = df['ndx_ret'] > (3 * df['atr_30d'])
    
    trades = []
    
    shock = df['shock'].values
    ndx_close = df['close'].values
    ndx_open = df['open'].values
    
    # Research values
    btc_close = df['close_btc'].values
    
    d1_atr_arr = df['d1_atr'].values
    d1_atr_30d_arr = df['d1_atr_30d'].values
    
    last_event_idx = -100
    friction = 3.0
    
    latency_ms = 50 # Assumed generic network/processing latency
    
    production_ready = True
    
    for i in range(8640, len(df) - 12):
        if shock[i]:
            if i < last_event_idx + 12:
                continue
            if np.isnan(d1_atr_arr[i]) or np.isnan(d1_atr_30d_arr[i]):
                continue
                
            direction = 1 if ndx_close[i] > ndx_open[i] else -1
            regime = "HIGH VOL" if d1_atr_arr[i] >= d1_atr_30d_arr[i] else "LOW VOL"
            
            trigger_time = df.index[i] + pd.Timedelta(minutes=5) # 10:00 bar finishes at 10:05
            
            # Simulated entry
            # Because we lack tick data, the closest production execution price is the OPEN of the NEXT M1 bar
            # (which is exactly at trigger_time). 
            entry_m1_idx = raw_btc.index.searchsorted(trigger_time)
            
            if entry_m1_idx < len(raw_btc):
                prod_entry_price = raw_btc.iloc[entry_m1_idx]['open']
            else:
                continue
                
            exit_time = trigger_time + pd.Timedelta(minutes=60)
            exit_m1_idx = raw_btc.index.searchsorted(exit_time)
            
            if exit_m1_idx < len(raw_btc):
                prod_exit_price = raw_btc.iloc[exit_m1_idx]['open']
            else:
                continue
                
            # Research prices (M5 close)
            res_entry_price = btc_close[i]
            res_exit_price = btc_close[i+12]
            
            # Production Gross
            if direction == 1:
                prod_gross = (prod_exit_price - prod_entry_price) / prod_entry_price * 10000
                res_gross = (res_exit_price - res_entry_price) / res_entry_price * 10000
            else:
                prod_gross = (prod_entry_price - prod_exit_price) / prod_entry_price * 10000
                res_gross = (res_entry_price - res_exit_price) / res_entry_price * 10000
                
            # Slippage calculation
            slippage_entry = abs(prod_entry_price - res_entry_price) / res_entry_price * 10000
            if direction == -1: slippage_entry *= -1 # Wait, slippage depends on direction.
            # actually, slippage is the difference in returns. 
            slippage = res_gross - prod_gross
            
            trades.append({
                'trigger_time': trigger_time,
                'regime': regime,
                'direction': direction,
                'prod_entry': prod_entry_price,
                'prod_exit': prod_exit_price,
                'res_entry': res_entry_price,
                'res_exit': res_exit_price,
                'prod_gross': prod_gross,
                'prod_net': prod_gross - friction,
                'res_net': res_gross - friction,
                'slippage': slippage,
                'latency_ms': latency_ms
            })
            last_event_idx = i
            
    tdf = pd.DataFrame(trades)
    
    print(f"Total production events processed: {len(tdf)}")
    print(f"Average Slippage (Research Net - Production Net): {tdf['slippage'].mean():.2f} bps")
    
    # Compare
    for regime in ['LOW VOL', 'HIGH VOL']:
        sub = tdf[tdf['regime'] == regime]
        print(f"\n--- {regime} ---")
        
        prod_wins = sub[sub['prod_net'] > 0]
        prod_loss = sub[sub['prod_net'] <= 0]
        prod_pf = abs(prod_wins['prod_net'].sum() / prod_loss['prod_net'].sum()) if len(prod_loss) > 0 else 0
        
        print(f"Production N: {len(sub)}")
        print(f"Production Mean Net: {sub['prod_net'].mean():.2f} bps")
        print(f"Production Median Net: {sub['prod_net'].median():.2f} bps")
        print(f"Production PF: {prod_pf:.2f}")
        print(f"Production Cumulative: {sub['prod_net'].sum():.2f} bps")
        
        cum = sub['prod_net'].cumsum()
        max_dd = (cum - cum.cummax()).min()
        print(f"Production Max DD: {max_dd:.2f} bps")
        
        print(f"Research Mean Net (Baseline): {sub['res_net'].mean():.2f} bps")
        print(f"Divergence (Prod - Res): {sub['prod_net'].mean() - sub['res_net'].mean():.2f} bps")

if __name__ == "__main__":
    run_g5()
