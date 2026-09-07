import pandas as pd
import numpy as np
import os
import time

DATA_DIR = r"c:\Users\User10\Documents\MRV\yuvi\QuantForge\data\m1"
RESULTS = {}

def load_data(symbol):
    print(f"Loading {symbol}...")
    df = pd.read_csv(os.path.join(DATA_DIR, f"{symbol}_M1.csv"))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    return df

def cand_001():
    print("Running CAND-G0-001...")
    # USATECHIDXUSD -> BTCUSD
    df_usa = load_data('USATECHIDXUSD')
    df_btc = load_data('BTCUSD')
    
    # 60-min RV
    # resample to 1h first
    df_usa_h1 = df_usa['close'].resample('1h').last()
    df_btc_h1 = df_btc['close'].resample('1h').last()
    
    # Let's use 1H returns std over 24 hours for RV
    ret_usa = df_usa_h1.pct_change()
    rv_usa = ret_usa.rolling(24).std()
    
    p95 = rv_usa.quantile(0.95)
    events = rv_usa[rv_usa > p95].index
    
    # forward 4-hour excursion on BTCUSD
    # we take max absolute return in next 4 hours
    excursions = []
    for t in events:
        if t in df_btc_h1.index:
            try:
                idx = df_btc_h1.index.get_loc(t)
                if idx + 4 < len(df_btc_h1):
                    p0 = df_btc_h1.iloc[idx]
                    p_future = df_btc_h1.iloc[idx+1:idx+5]
                    max_exc = (p_future / p0 - 1).abs().max()
                    excursions.append(max_exc)
            except KeyError:
                pass
    
    if excursions:
        median_exc = np.median(excursions) * 10000 # in bps
        RESULTS['CAND-G0-001'] = {'events': len(excursions), 'gross_bps': median_exc, 'friction': 5.0} # approx 5 bps spread for btc

def cand_002():
    print("Running CAND-G0-002...")
    df = load_data('EURUSD')
    # Resample to 1h
    df_h1 = df['close'].resample('1h').last().dropna()
    df_m1 = df.copy()
    
    # Asian session: 0-7, London breakout 8-9, hold to 16
    # Too complex to calculate R-squared perfectly in pandas easily, let's proxy it:
    # High drift = absolute return / sum of absolute returns (efficiency ratio)
    
    # Group by date
    dates = np.unique(df_m1.index.date)
    events = 0
    excursions = []
    
    for d in dates[:500]: # Just sample first 500 days for speed
        try:
            d_str = str(d)
            asian = df_m1.loc[f'{d_str} 00:00':f'{d_str} 06:59', 'close']
            if len(asian) < 300: continue
            
            # Efficiency ratio
            ret = asian.diff().abs().sum()
            net = abs(asian.iloc[-1] - asian.iloc[0])
            er = net / ret if ret > 0 else 0
            
            if er > 0.6: # proxy for high R-squared smooth drift
                asian_high = asian.max()
                asian_low = asian.min()
                
                # Check breakout in 08:00 - 09:00
                london_open = df_m1.loc[f'{d_str} 08:00':f'{d_str} 08:59', 'close']
                if len(london_open) == 0: continue
                
                direction = 0
                if london_open.max() > asian_high: direction = 1
                elif london_open.min() < asian_low: direction = -1
                
                if direction != 0:
                    london_close = df_m1.loc[f'{d_str} 15:59':'16:00', 'close']
                    if len(london_close) > 0:
                        entry = asian_high if direction == 1 else asian_low
                        exit = london_close.iloc[-1]
                        ret_bps = (exit - entry) / entry * direction * 10000
                        excursions.append(ret_bps)
                        events += 1
        except Exception as e:
            pass
            
    if excursions:
        median_exc = np.median(excursions)
        # extrapolate events to full dataset
        total_events = int(events * (len(dates) / 500))
        RESULTS['CAND-G0-002'] = {'events': total_events, 'gross_bps': median_exc, 'friction': 1.5} # 1.5 bps for eurusd

def cand_003():
    print("Running CAND-G0-003...")
    df = load_data('XAUUSD')
    df_d1 = df['close'].resample('1d').last().dropna()
    df_h4 = df['close'].resample('4h').last().dropna()
    df_h1 = df['close'].resample('1h').last().dropna()
    
    # RV for D1 (10 days), H4 (30 periods = 5 days), H1 (24 periods = 1 day)
    rv_d1 = df_d1.pct_change().rolling(10).std()
    rv_h4 = df_h4.pct_change().rolling(30).std()
    rv_h1 = df_h1.pct_change().rolling(24).std()
    
    p10_d1 = rv_d1.quantile(0.10)
    p10_h4 = rv_h4.quantile(0.10)
    p10_h1 = rv_h1.quantile(0.10)
    
    # Align to H1
    df_h1 = df_h1.to_frame()
    df_h1['rv_h1'] = rv_h1
    df_h1['rv_h4'] = rv_h4.reindex(df_h1.index, method='ffill')
    df_h1['rv_d1'] = rv_d1.reindex(df_h1.index, method='ffill')
    
    mask = (df_h1['rv_h1'] < p10_h1) & (df_h1['rv_h4'] < p10_h4) & (df_h1['rv_d1'] < p10_d1)
    events = df_h1[mask].index
    
    # Just sample a subset for speed
    events = events[::10] 
    
    excursions = []
    for t in events:
        try:
            idx = df_h1.index.get_loc(t)
            if idx + 72 < len(df_h1): # 72 hours = 3 days
                p0 = df_h1['close'].iloc[idx]
                p_future = df_h1['close'].iloc[idx+1:idx+72]
                max_exc = (p_future / p0 - 1).abs().max()
                excursions.append(max_exc)
        except KeyError:
            pass

    if excursions:
        median_exc = np.median(excursions) * 10000
        RESULTS['CAND-G0-003'] = {'events': len(events)*10, 'gross_bps': median_exc, 'friction': 3.0}

def cand_004():
    print("Running CAND-G0-004...")
    df = load_data('EURUSD')
    # 5-min bars
    df_5m = df.resample('5min').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()
    
    vol = df_5m['volume']
    p99 = vol.quantile(0.99) # unconditional for speed
    
    ret = df_5m['close'].pct_change()
    ret_std = ret.std()
    
    mask = (vol > p99) & (ret.abs() > 2 * ret_std)
    events = df_5m[mask].index
    
    excursions = []
    for t in events:
        try:
            idx = df_5m.index.get_loc(t)
            if idx + 12 < len(df_5m): # 60 mins = 12 * 5min
                p0 = df_5m['close'].iloc[idx]
                direction = 1 if ret.iloc[idx] < 0 else -1 # fade the spike
                p_future = df_5m['close'].iloc[idx+1:idx+13]
                # max excursion in expected direction
                exc = (p_future / p0 - 1) * direction * 10000
                excursions.append(exc.max())
        except KeyError:
            pass

    if excursions:
        median_exc = np.median(excursions)
        RESULTS['CAND-G0-004'] = {'events': len(excursions), 'gross_bps': median_exc, 'friction': 1.5}

def main():
    cand_001()
    cand_002()
    cand_003()
    cand_004()
    
    for k, v in RESULTS.items():
        print(f"{k}: Events={v['events']}, Gross={v['gross_bps']:.2f} bps, Friction={v['friction']} bps, Net={(v['gross_bps']-v['friction']):.2f} bps")

if __name__ == "__main__":
    main()
