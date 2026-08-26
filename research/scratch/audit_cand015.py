import pandas as pd
import numpy as np

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

def run_audit():
    df_ndx = pd.read_csv("data/m1/USATECHIDXUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp').resample('5min').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    df_btc = pd.read_csv("data/m1/BTCUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp').resample('5min').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    
    df = df_ndx[['open', 'close', 'high', 'low']].join(df_btc[['open', 'high', 'low', 'close']], rsuffix='_btc', how='inner')
    df.dropna(inplace=True)
    
    atr_ndx, _ = calc_atr(df[['high', 'low', 'close']], 14)
    df['atr'] = atr_ndx
    df['atr_30d'] = df['atr'].rolling(8640).mean()
    
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
    btc_close = df['close_btc'].values
    d1_atr_arr = df['d1_atr'].values
    d1_atr_30d_arr = df['d1_atr_30d'].values
    
    last_event_idx = -100
    friction = 3.0
    
    for i in range(8640, len(df) - 12):
        if shock[i]:
            if i < last_event_idx + 12:
                continue
            if np.isnan(d1_atr_arr[i]) or np.isnan(d1_atr_30d_arr[i]):
                continue
                
            direction = 1 if ndx_close[i] > ndx_open[i] else -1
            entry_price = btc_close[i]
            exit_price = btc_close[i+12]
            
            if direction == 1:
                gross = (exit_price - entry_price) / entry_price * 10000
            else:
                gross = (entry_price - exit_price) / entry_price * 10000
                
            regime = "HIGH VOL" if d1_atr_arr[i] >= d1_atr_30d_arr[i] else "LOW VOL"
            
            trades.append({
                'time': df.index[i],
                'dir': direction,
                'net': gross - friction,
                'regime': regime
            })
            last_event_idx = i
            
    tdf = pd.DataFrame(trades)
    tdf.set_index('time', inplace=True)
    tdf.sort_index(inplace=True)
    
    mid_idx = len(tdf) // 2
    hold_df = tdf.iloc[mid_idx:]
    
    # 1. High Vol Holdout Analysis
    hv = hold_df[hold_df['regime'] == 'HIGH VOL'].copy()
    print("--- HIGH VOL HOLDOUT ---")
    print(f"N: {len(hv)}")
    print(f"Mean: {hv['net'].mean():.2f}")
    print(f"Median: {hv['net'].median():.2f}")
    print(f"StdDev: {hv['net'].std():.2f}")
    print(f"25th: {hv['net'].quantile(0.25):.2f}, 75th: {hv['net'].quantile(0.75):.2f}")
    print(f"Worst 5%: {hv['net'].quantile(0.05):.2f}, Best 5%: {hv['net'].quantile(0.95):.2f}")
    wins = hv[hv['net'] > 0]
    losses = hv[hv['net'] <= 0]
    print(f"Avg Win: {wins['net'].mean():.2f}, Avg Loss: {losses['net'].mean():.2f}")
    print(f"Large Negative Obs (< -100 bp): {len(hv[hv['net'] < -100])}")
    
    total_pnl = hv['net'].sum()
    sorted_losses = losses['net'].sort_values() # ascending, so largest negative first
    
    def loss_contrib(pct):
        n = max(1, int(len(losses) * pct))
        sub_sum = sorted_losses.iloc[:n].sum()
        return sub_sum
        
    print(f"Total Loss Sum: {losses['net'].sum():.2f}")
    print(f"Largest 1% Losses Sum: {loss_contrib(0.01):.2f}")
    print(f"Largest 5% Losses Sum: {loss_contrib(0.05):.2f}")
    print(f"Largest 10% Losses Sum: {loss_contrib(0.10):.2f}")
    
    # 2. Low Vol Full Sample Stability
    lv = tdf[tdf['regime'] == 'LOW VOL'].copy()
    print("\n--- LOW VOL FULL SAMPLE ---")
    print(f"N: {len(lv)}")
    print(f"Mean: {lv['net'].mean():.2f}")
    print(f"Median: {lv['net'].median():.2f}")
    print(f"25th: {lv['net'].quantile(0.25):.2f}, 75th: {lv['net'].quantile(0.75):.2f}")
    print(f"Worst 5%: {lv['net'].quantile(0.05):.2f}, Best 5%: {lv['net'].quantile(0.95):.2f}")
    wins_lv = lv[lv['net'] > 0]
    losses_lv = lv[lv['net'] <= 0]
    print(f"Avg Win: {wins_lv['net'].mean():.2f}, Avg Loss: {losses_lv['net'].mean():.2f}")
    
    sorted_wins = wins_lv['net'].sort_values(ascending=False)
    
    def win_contrib(pct):
        n = max(1, int(len(wins_lv) * pct))
        sub_sum = sorted_wins.iloc[:n].sum()
        return sub_sum
        
    print(f"Total Win Sum: {wins_lv['net'].sum():.2f}")
    print(f"Largest 1% Wins Sum: {win_contrib(0.01):.2f}")
    print(f"Largest 5% Wins Sum: {win_contrib(0.05):.2f}")
    print(f"Largest 10% Wins Sum: {win_contrib(0.10):.2f}")

if __name__ == "__main__":
    run_audit()
