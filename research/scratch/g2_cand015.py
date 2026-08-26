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
    atr = wilder_smoothing(tr, n)
    return atr, tr

def run_g2():
    print("Loading data...")
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
    btc_high = df['high_btc'].values
    btc_low = df['low_btc'].values
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
            
            # calculate adverse excursion
            sub_high = np.max(btc_high[i+1:i+13])
            sub_low = np.min(btc_low[i+1:i+13])
            
            if direction == 1:
                gross = (exit_price - entry_price) / entry_price * 10000
                mae = (sub_low - entry_price) / entry_price * 10000
            else:
                gross = (entry_price - exit_price) / entry_price * 10000
                mae = (entry_price - sub_high) / entry_price * 10000
                
            regime = "HIGH VOL" if d1_atr_arr[i] >= d1_atr_30d_arr[i] else "LOW VOL"
            
            trades.append({
                'time': df.index[i],
                'dir': direction,
                'gross': gross,
                'net': gross - friction,
                'net_2x': gross - (friction * 2),
                'mae': mae,
                'regime': regime
            })
            last_event_idx = i
            
    tdf = pd.DataFrame(trades)
    tdf.set_index('time', inplace=True)
    tdf.sort_index(inplace=True)
    
    # Time stability split (50/50 chronological)
    mid_idx = len(tdf) // 2
    dev_df = tdf.iloc[:mid_idx]
    hold_df = tdf.iloc[mid_idx:]
    
    def get_metrics(d):
        if len(d) == 0: return {}
        wins = d[d['net'] > 0]
        losses = d[d['net'] <= 0]
        win_rate = len(wins)/len(d)
        avg_win = wins['net'].mean() if len(wins)>0 else 0
        avg_loss = losses['net'].mean() if len(losses)>0 else 0
        pf = abs(wins['net'].sum() / losses['net'].sum()) if losses['net'].sum() != 0 else np.inf
        return {
            'N': len(d),
            'Mean': d['net'].mean(),
            'Median': d['net'].median(),
            'WinRate': win_rate,
            'AvgWin': avg_win,
            'AvgLoss': avg_loss,
            'PF': pf,
            'CumNet': d['net'].sum(),
            'StdDev': d['net'].std(),
            'P25': d['net'].quantile(0.25),
            'P75': d['net'].quantile(0.75),
            'Worst5': d['net'].quantile(0.05),
            'Best5': d['net'].quantile(0.95),
            'MedianMAE': d['mae'].median()
        }

    print("FULL SAMPLE")
    for r in ['LOW VOL', 'HIGH VOL']:
        m = get_metrics(tdf[tdf['regime'] == r])
        print(f"[{r}] {m}")
        
    print("\nDEVELOPMENT")
    for r in ['LOW VOL', 'HIGH VOL']:
        m = get_metrics(dev_df[dev_df['regime'] == r])
        print(f"[{r}] {m}")
        
    print("\nHOLDOUT")
    for r in ['LOW VOL', 'HIGH VOL']:
        m = get_metrics(hold_df[hold_df['regime'] == r])
        print(f"[{r}] {m}")
        
    print("\nYEARLY (LOW VOL)")
    tdf['year'] = tdf.index.year
    for y in sorted(tdf['year'].unique()):
        m = get_metrics(tdf[(tdf['regime'] == 'LOW VOL') & (tdf['year'] == y)])
        print(f"[{y}] {m}")
        
    print("\nEVENT CLUSTERING")
    print(f"Total events/year: {len(tdf) / len(tdf['year'].unique()):.1f}")
    tdf['date'] = tdf.index.date
    tdf['week'] = tdf.index.isocalendar().week
    max_day = tdf.groupby('date').size().max()
    max_week = tdf.groupby(['year', 'week']).size().max()
    print(f"Max events/day: {max_day}")
    print(f"Max events/week: {max_week}")
    
    print("\n2x FRICTION STRESS (LOW VOL)")
    low_df = tdf[tdf['regime'] == 'LOW VOL']
    print(f"Mean Net (2x): {low_df['net_2x'].mean()}")
    print(f"Median Net (2x): {low_df['net_2x'].median()}")

if __name__ == "__main__":
    run_g2()
