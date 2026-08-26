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

def run_g3():
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
    
    # Primary Endpoint: LOW_VOL mean - HIGH_VOL mean
    lv = tdf[tdf['regime'] == 'LOW VOL']['net'].values
    hv = tdf[tdf['regime'] == 'HIGH VOL']['net'].values
    
    mean_diff = lv.mean() - hv.mean()
    median_diff = np.median(lv) - np.median(hv)
    
    print(f"Primary Endpoint (Mean Diff): {mean_diff:.2f} bps")
    print(f"Median Diff: {median_diff:.2f} bps")
    
    # Statistical Test: Permutation test on labels
    np.random.seed(42)
    n_permutations = 10000
    all_returns = np.concatenate([lv, hv])
    n_lv = len(lv)
    
    perm_diffs = []
    for _ in range(n_permutations):
        np.random.shuffle(all_returns)
        perm_lv = all_returns[:n_lv]
        perm_hv = all_returns[n_lv:]
        perm_diffs.append(perm_lv.mean() - perm_hv.mean())
        
    perm_diffs = np.array(perm_diffs)
    p_value = np.mean(perm_diffs >= mean_diff)
    print(f"Permutation p-value (1-sided): {p_value:.4f}")
    
    # Confidence Interval via Bootstrap
    np.random.seed(42)
    boot_diffs = []
    for _ in range(10000):
        b_lv = np.random.choice(lv, size=len(lv), replace=True)
        b_hv = np.random.choice(hv, size=len(hv), replace=True)
        boot_diffs.append(b_lv.mean() - b_hv.mean())
        
    ci_lower = np.percentile(boot_diffs, 2.5)
    ci_upper = np.percentile(boot_diffs, 97.5)
    print(f"95% CI for Mean Diff: [{ci_lower:.2f}, {ci_upper:.2f}]")
    
    # Placebo Test: Shuffled labels using frozen seed 4242
    np.random.seed(4242)
    shuffled_regimes = np.array(tdf['regime'].tolist())
    np.random.shuffle(shuffled_regimes)
    tdf['placebo_regime'] = shuffled_regimes
    
    p_lv = tdf[tdf['placebo_regime'] == 'LOW VOL']['net'].values
    p_hv = tdf[tdf['placebo_regime'] == 'HIGH VOL']['net'].values
    placebo_diff = p_lv.mean() - p_hv.mean()
    print(f"Placebo Test (Shuffled Labels) Mean Diff: {placebo_diff:.2f} bps")

if __name__ == "__main__":
    run_g3()
