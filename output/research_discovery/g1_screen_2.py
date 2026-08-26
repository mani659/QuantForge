import pandas as pd
import numpy as np
import os

DATA_DIR = r"c:\Users\User10\Documents\MRV\yuvi\QuantForge\data\m1"
RESULTS = {}

def load_data(symbol):
    df = pd.read_csv(os.path.join(DATA_DIR, f"{symbol}_M1.csv"))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    return df

def cand_001():
    try:
        df_usa = load_data('USATECHIDXUSD')
        df_btc = load_data('BTCUSD')
        df_usa_h1 = df_usa['close'].resample('1h').last().dropna()
        df_btc_h1 = df_btc['close'].resample('1h').last().dropna()
        rv = df_usa_h1.pct_change().rolling(24).std()
        p95 = rv.quantile(0.95)
        events = rv[rv > p95].index
        
        # intersect with btc
        valid_events = events.intersection(df_btc_h1.index)
        excursions = []
        for t in valid_events:
            idx = df_btc_h1.index.get_indexer([t])[0]
            if idx != -1 and idx + 4 < len(df_btc_h1):
                p0 = df_btc_h1.iloc[idx]
                p_future = df_btc_h1.iloc[idx+1:idx+5]
                exc = (p_future / p0 - 1).abs().max() * 10000
                excursions.append(exc)
        
        if excursions:
            RESULTS['CAND-G0-001'] = {'events': len(excursions), 'gross_bps': np.median(excursions), 'friction': 5.0}
        else:
            RESULTS['CAND-G0-001'] = {'events': 0, 'gross_bps': 0, 'friction': 5.0}
    except Exception as e:
        print("CAND-001 error:", e)

def cand_002():
    try:
        df = load_data('EURUSD')
        df_h1 = df['close'].resample('1h').last().dropna()
        # simplified 00:00 to 07:00 drift using H1 bars
        # 00:00 is hour 0, 06:00 is hour 6
        df_h1 = df_h1.to_frame()
        df_h1['hour'] = df_h1.index.hour
        df_h1['date'] = df_h1.index.date
        
        asian = df_h1[df_h1['hour'].isin([0,1,2,3,4,5,6])]
        asian_grp = asian.groupby('date')['close'].agg(['first', 'max', 'min', 'last', 'count'])
        asian_grp = asian_grp[asian_grp['count'] >= 6]
        
        # breakout at 8:00
        london = df_h1[df_h1['hour'].isin([8,9,10,11,12,13,14,15])]
        london_grp = london.groupby('date')['close'].agg(['first', 'max', 'min', 'last', 'count'])
        london_grp = london_grp[london_grp['count'] >= 6]
        
        common = asian_grp.index.intersection(london_grp.index)
        excursions = []
        for d in common:
            a = asian_grp.loc[d]
            l = london_grp.loc[d]
            # strict drift proxy
            net = abs(a['last'] - a['first'])
            hl = a['max'] - a['min']
            if hl > 0 and net/hl > 0.6:
                if l['first'] > a['max']: # upward breakout
                    exc = (l['max'] / l['first'] - 1) * 10000
                    excursions.append(exc)
                elif l['first'] < a['min']: # downward breakout
                    exc = (l['first'] / l['min'] - 1) * 10000
                    excursions.append(exc)
        
        if excursions:
            RESULTS['CAND-G0-002'] = {'events': len(excursions), 'gross_bps': np.median(excursions), 'friction': 1.5}
        else:
            RESULTS['CAND-G0-002'] = {'events': 0, 'gross_bps': 0, 'friction': 1.5}
    except Exception as e:
        print("CAND-002 error:", e)

def main():
    cand_001()
    cand_002()
    for k, v in RESULTS.items():
        print(f"{k}: Events={v['events']}, Gross={v['gross_bps']:.2f} bps, Friction={v['friction']} bps, Net={(v['gross_bps']-v['friction']):.2f} bps")

if __name__ == "__main__":
    main()
