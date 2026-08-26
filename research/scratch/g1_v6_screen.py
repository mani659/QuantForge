import pandas as pd
import numpy as np
import os
import json

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

def process_cand_015(df_ndx_m5, df_btc_m5, friction=3.0):
    print("Aligning M5 data for CAND-015...")
    df = df_ndx_m5[['open', 'close', 'high', 'low']].join(df_btc_m5[['close']], rsuffix='_btc', how='inner')
    df.dropna(inplace=True)
    
    # NDX M5 ATR
    atr_ndx, tr_ndx = calc_atr(df, 14)
    df['atr'] = atr_ndx
    df['atr_30d'] = df['atr'].rolling(8640).mean() # 12 bars/hr * 24 * 30
    
    # NDX D1 ATR for regime
    df_d1 = df_ndx_m5.resample('1D').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
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
    
    raw_shocks = np.sum(shock)
    valid_opps = 0
    lockout_supp = 0
    
    for i in range(8640, len(df) - 12):
        if shock[i]:
            if i < last_event_idx + 12: # 60-min lockout (12 M5 bars)
                lockout_supp += 1
                continue
                
            if np.isnan(d1_atr_arr[i]) or np.isnan(d1_atr_30d_arr[i]):
                continue
                
            valid_opps += 1
            
            direction = 1 if ndx_close[i] > ndx_open[i] else -1
            entry_price = btc_close[i]
            exit_price = btc_close[i+12]
            
            if direction == 1:
                gross = (exit_price - entry_price) / entry_price * 10000
            else:
                gross = (entry_price - exit_price) / entry_price * 10000
                
            regime = "High Vol" if d1_atr_arr[i] > d1_atr_30d_arr[i] else "Low Vol"
            
            trades.append({
                'time': df.index[i],
                'dir': direction,
                'gross': gross,
                'net': gross - friction,
                'regime': regime
            })
            
            last_event_idx = i
            
    return pd.DataFrame(trades), raw_shocks, valid_opps, lockout_supp

def process_cand_016(df_eur_h1, df_gbp_h1, friction=3.0):
    df = df_eur_h1[['open', 'close', 'high', 'low']].join(df_gbp_h1[['open', 'close', 'high', 'low']], lsuffix='_eur', rsuffix='_gbp', how='inner')
    df.dropna(inplace=True)
    
    _, tr_eur = calc_atr(df.rename(columns={'high_eur':'high', 'low_eur':'low', 'close_eur':'close'}))
    _, tr_gbp = calc_atr(df.rename(columns={'high_gbp':'high', 'low_gbp':'low', 'close_gbp':'close'}))
    
    df['tr_eur'] = tr_eur
    df['tr_gbp'] = tr_gbp
    
    # 30-day mean (720 hours)
    df['eur_mean'] = df['tr_eur'].rolling(720).mean()
    df['eur_std'] = df['tr_eur'].rolling(720).std()
    
    df['gbp_mean'] = df['tr_gbp'].rolling(720).mean()
    df['gbp_std'] = df['tr_gbp'].rolling(720).std()
    
    df['eur_shock'] = df['tr_eur'] > (df['eur_mean'] + 2 * df['eur_std'])
    df['gbp_quiet'] = df['tr_gbp'] < (df['gbp_mean'] + 1 * df['gbp_std'])
    
    df['event'] = df['eur_shock'] & df['gbp_quiet']
    df['quiet_both'] = (df['tr_eur'] < (df['eur_mean'] + 1 * df['eur_std'])) & (df['tr_gbp'] < (df['gbp_mean'] + 1 * df['gbp_std']))
    
    event = df['event'].values
    quiet_both = df['quiet_both'].values
    gbp_close = df['close_gbp'].values
    eur_close = df['close_eur'].values
    eur_open = df['open_eur'].values
    
    raw_events = np.sum(event)
    valid_opps = 0
    suppressed = 0
    
    state = 'ARMED'
    quiet_count = 0
    trades = []
    
    for i in range(720, len(df) - 4):
        if quiet_both[i]:
            quiet_count += 1
        else:
            quiet_count = 0
            
        if state == 'TRIGGERED':
            if quiet_count >= 4:
                state = 'ARMED'
            
        if event[i]:
            if state == 'ARMED':
                valid_opps += 1
                state = 'TRIGGERED'
                quiet_count = 0
                
                direction = 1 if eur_close[i] > eur_open[i] else -1
                entry_price = gbp_close[i]
                exit_price = gbp_close[i+4]
                
                if direction == 1:
                    gross = (exit_price - entry_price) / entry_price * 10000
                else:
                    gross = (entry_price - exit_price) / entry_price * 10000
                    
                hour = df.index[i].hour
                session = 'Asia' if 0 <= hour < 8 else 'London' if 8 <= hour < 13 else 'NY'
                
                trades.append({
                    'time': df.index[i],
                    'dir': direction,
                    'gross': gross,
                    'net': gross - friction,
                    'session': session
                })
            else:
                suppressed += 1
                
    return pd.DataFrame(trades), raw_events, valid_opps, suppressed

def process_cand_017(df_xau_d1, df_xau_h4, friction=3.0):
    df_d1 = df_xau_d1.copy()
    df_d1['sma_20'] = df_d1['close'].rolling(20).mean()
    df_d1['std_20'] = df_d1['close'].rolling(20).std()
    df_d1['bb_upper'] = df_d1['sma_20'] + 2 * df_d1['std_20']
    df_d1['bb_lower'] = df_d1['sma_20'] - 2 * df_d1['std_20']
    df_d1['bb_width'] = (df_d1['bb_upper'] - df_d1['bb_lower']) / df_d1['sma_20']
    
    # Percentile over 252 days
    df_d1['bb_width_10p'] = df_d1['bb_width'].rolling(252).quantile(0.10)
    df_d1['compression'] = df_d1['bb_width'] < df_d1['bb_width_10p']
    
    df_d1['sma_200'] = df_d1['close'].rolling(200).mean()
    df_d1['sma_200_slope'] = df_d1['sma_200'] - df_d1['sma_200'].shift(5)
    
    df_d1_shifted = df_d1.shift(1)[['bb_upper', 'bb_lower', 'compression', 'sma_200_slope']]
    df_d1_shifted.index = df_d1_shifted.index.date
    
    df_h4 = df_xau_h4.copy()
    df_h4['date'] = df_h4.index.date
    df_h4 = df_h4.merge(df_d1_shifted, left_on='date', right_index=True, how='left')
    
    df_h4['ema_20'] = df_h4['close'].ewm(span=20, adjust=False).mean()
    
    comp = df_h4['compression'].values
    upper = df_h4['bb_upper'].values
    lower = df_h4['bb_lower'].values
    close = df_h4['close'].values
    slope = df_h4['sma_200_slope'].values
    ema20 = df_h4['ema_20'].values
    
    trades = []
    
    raw_breaks = 0
    valid_opps = 0
    suppressed = 0
    
    state = 'ARMED'
    
    for i in range(252 * 6, len(df_h4) - 18): # 18 H4 bars = 72 hours
        if pd.isna(comp[i]) or pd.isna(upper[i]):
            continue
            
        is_breakout_up = comp[i] and close[i] > upper[i]
        is_breakout_dn = comp[i] and close[i] < lower[i]
        
        if is_breakout_up or is_breakout_dn:
            raw_breaks += 1
            
            if state == 'ARMED':
                valid_opps += 1
                state = 'TRIGGERED'
                
                direction = 1 if is_breakout_up else -1
                entry_price = close[i]
                exit_price = close[i+18]
                
                if direction == 1:
                    gross = (exit_price - entry_price) / entry_price * 10000
                else:
                    gross = (entry_price - exit_price) / entry_price * 10000
                    
                align = "Aligned" if (direction == 1 and slope[i] > 0) or (direction == -1 and slope[i] < 0) else "Counter"
                
                trades.append({
                    'time': df_h4.index[i],
                    'dir': direction,
                    'gross': gross,
                    'net': gross - friction,
                    'align': align
                })
            else:
                suppressed += 1
                
        elif state == 'TRIGGERED':
            # Re-arm logic: price must revert to H4 20-SMA and close inside (or cross it)
            if (close[i-1] > ema20[i-1] and close[i] < ema20[i]) or (close[i-1] < ema20[i-1] and close[i] > ema20[i]):
                state = 'ARMED'
                
    return pd.DataFrame(trades), raw_breaks, valid_opps, suppressed

if __name__ == "__main__":
    print("Loading data...")
    # Read M5 data for CAND-015
    df_ndx = pd.read_csv("data/m1/USATECHIDXUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp').resample('5min').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    df_btc = pd.read_csv("data/m1/BTCUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp').resample('5min').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    
    if not os.path.exists("data/m1/GBPUSD_M1.csv"):
        print("Missing GBPUSD data, aborting 016 temporarily.")
    else:
        # Read H1 data for CAND-016
        df_eur_h1 = pd.read_csv("data/m1/EURUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp').resample('1h').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
        df_gbp_h1 = pd.read_csv("data/m1/GBPUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp').resample('1h').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
        res_016, raw_016, valid_016, supp_016 = process_cand_016(df_eur_h1, df_gbp_h1, friction=3.0)

    res_015, raw_015, valid_015, supp_015 = process_cand_015(df_ndx, df_btc, friction=3.0)
    
    # Read H4/D1 for CAND-017
    df_xau_m1 = pd.read_csv("data/m1/XAUUSD_M1.csv", parse_dates=['timestamp'], index_col='timestamp')
    df_xau_h4 = df_xau_m1.resample('4h').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    df_xau_d1 = df_xau_m1.resample('1D').agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'}).dropna()
    
    res_017, raw_017, valid_017, supp_017 = process_cand_017(df_xau_d1, df_xau_h4, friction=3.0)
    
    # Print reports
    print(f"\nCAND-015 Integrity: Raw Shocks={raw_015}, Valid Opps={valid_015}, Lockout Supp={supp_015}")
    if len(res_015) > 0:
        for r in ['High Vol', 'Low Vol']:
            df_r = res_015[res_015['regime'] == r]
            if len(df_r) > 0:
                print(f"CAND-015 Regime {r}: N={len(df_r)}, Median Net={df_r['net'].median():.2f}, Mean Net={df_r['net'].mean():.2f}")
                wins = df_r[df_r['net'] > 0]
                losses = df_r[df_r['net'] <= 0]
                avg_win = wins['net'].mean() if len(wins)>0 else 0
                avg_loss = losses['net'].mean() if len(losses)>0 else 0
                print(f"  Win%: {len(wins)/len(df_r)*100:.1f}%, Avg Win: {avg_win:.2f}, Avg Loss: {avg_loss:.2f}")

    if os.path.exists("data/m1/GBPUSD_M1.csv"):
        print(f"\nCAND-016 Integrity: Raw Events={raw_016}, Valid Opps={valid_016}, Suppressed={supp_016}")
        if len(res_016) > 0:
            for s in ['Asia', 'London', 'NY']:
                df_s = res_016[res_016['session'] == s]
                if len(df_s) > 0:
                    print(f"CAND-016 Session {s}: N={len(df_s)}, Median Net={df_s['net'].median():.2f}, Mean Net={df_s['net'].mean():.2f}")
                    wins = df_s[df_s['net'] > 0]
                    losses = df_s[df_s['net'] <= 0]
                    avg_win = wins['net'].mean() if len(wins)>0 else 0
                    avg_loss = losses['net'].mean() if len(losses)>0 else 0
                    print(f"  Win%: {len(wins)/len(df_s)*100:.1f}%, Avg Win: {avg_win:.2f}, Avg Loss: {avg_loss:.2f}")

    print(f"\nCAND-017 Integrity: Raw Breaks={raw_017}, Valid Opps={valid_017}, Suppressed={supp_017}")
    if len(res_017) > 0:
        for a in ['Aligned', 'Counter']:
            df_a = res_017[res_017['align'] == a]
            if len(df_a) > 0:
                print(f"CAND-017 Align {a}: N={len(df_a)}, Median Net={df_a['net'].median():.2f}, Mean Net={df_a['net'].mean():.2f}")
                wins = df_a[df_a['net'] > 0]
                losses = df_a[df_a['net'] <= 0]
                avg_win = wins['net'].mean() if len(wins)>0 else 0
                avg_loss = losses['net'].mean() if len(losses)>0 else 0
                print(f"  Win%: {len(wins)/len(df_a)*100:.1f}%, Avg Win: {avg_win:.2f}, Avg Loss: {avg_loss:.2f}")
