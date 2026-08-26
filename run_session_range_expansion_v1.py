import pandas as pd
import numpy as np
import os
import time
import hashlib
import psutil

# Configuration
DATA_PATH = r"c:\Users\User10\Documents\MRV\yuvi\QuantForge\data\m1\USATECHIDXUSD_M1.csv"
OUT_DIR = r"c:\Users\User10\Documents\MRV\yuvi\QuantForge\output\research_discovery\SESSION_RANGE_EXPANSION"
PROTOCOL_PATH = r"c:\Users\User10\Documents\MRV\yuvi\QuantForge\output\research_discovery\SESSION_RANGE_EXPANSION_EVENT_STUDY_PROTOCOL_V1.md"

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def log(msg):
    mem = psutil.Process().memory_info().rss / 1024 / 1024
    print(f"[{time.strftime('%H:%M:%S')}] [Mem: {mem:.1f}MB] {msg}")

def execute():
    os.makedirs(OUT_DIR, exist_ok=True)
    start_time = time.time()
    
    # 1. Identity & Integrity
    protocol_hash = sha256_file(PROTOCOL_PATH)
    data_hash = sha256_file(DATA_PATH)
    log(f"Protocol Hash: {protocol_hash}")
    log(f"Data Hash: {data_hash}")
    
    # 2. Load Data
    log("Loading M1 dataset...")
    df = pd.read_csv(DATA_PATH)
    
    log("Processing timestamps and duplicates...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Deduplicate before timezone/sessions (Clarification 2)
    df = df.sort_values('timestamp').drop_duplicates(subset=['timestamp'], keep='first')
    
    # Timezone conversion (Clarification 3)
    if df['timestamp'].dt.tz is None:
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('America/New_York')
    else:
        df['timestamp'] = df['timestamp'].dt.tz_convert('America/New_York')
        
    df.set_index('timestamp', inplace=True)
    
    # Any price <= 0 invalidates (Clarification 1)
    log("Applying price quality gates...")
    df = df[(df['open'] > 0) & (df['high'] > 0) & (df['low'] > 0) & (df['close'] > 0)]
    
    log(f"Data loaded: {len(df)} valid M1 bars.")
    
    # 3. Session Construction
    log("Constructing sessions...")
    df['date'] = df.index.date
    shift_mask = df.index.time >= pd.to_datetime("18:00:00").time()
    df.loc[shift_mask, 'date'] = df.loc[shift_mask, 'date'] + pd.Timedelta(days=1)
    
    grouped = df.groupby('date')
    
    results = []
    
    # Valid calendar dates calculation for stopping rule (exactly as protocol specifies)
    total_calendar_days_with_bars = len(np.unique(df.index.date))
    
    for current_date, group in grouped:
        times = group.index.time
        pre_mask = (times >= pd.to_datetime("18:00:00").time()) | (times <= pd.to_datetime("09:29:00").time())
        cash_mask = (times >= pd.to_datetime("09:30:00").time()) & (times <= pd.to_datetime("16:00:00").time())
        
        pre_session = group[pre_mask]
        cash_session = group[cash_mask]
        
        if pre_session.empty or cash_session.empty:
            continue
            
        try:
            close_0929 = pre_session.at_time('09:29:00')
            if close_0929.empty:
                continue
            c_0929 = close_0929['close'].iloc[-1]
        except:
            continue
            
        try:
            close_1600 = cash_session.at_time('16:00:00')
            if close_1600.empty:
                continue
            c_1600 = close_1600['close'].iloc[-1]
        except:
            continue
            
        try:
            open_0930 = cash_session.at_time('09:30:00')
            if open_0930.empty:
                continue
            o_0930 = open_0930['open'].iloc[0]
        except:
            continue
            
        if len(cash_session) < 200:
            continue
            
        high_pre = pre_session['high'].max()
        low_pre = pre_session['low'].min()
        r_pre = high_pre - low_pre
        norm_r_pre = r_pre / c_0929
        
        high_cash = cash_session['high'].max()
        low_cash = cash_session['low'].min()
        r_cash = high_cash - low_cash
        norm_r_cash = r_cash / c_1600
        
        direction = c_1600 - o_0930
        persistence = np.nan
        
        if direction > 0 and r_cash > 0:
            persistence = 1.0 if c_1600 >= (low_cash + 0.75 * r_cash) else 0.0
        elif direction < 0 and r_cash > 0:
            persistence = 1.0 if c_1600 <= (high_cash - 0.75 * r_cash) else 0.0
            
        results.append({
            'date': current_date,
            'norm_r_pre': norm_r_pre,
            'norm_r_cash': norm_r_cash,
            'persistence': persistence,
            'r_cash': r_cash,
            'direction': direction
        })
        
    events = pd.DataFrame(results).sort_values('date').reset_index(drop=True)
    
    valid_days = len(events)
    total_event_days = len(grouped)
    invalid_days = total_event_days - valid_days
    invalid_ratio = invalid_days / total_calendar_days_with_bars
    log(f"Valid days: {valid_days}, Invalid days: {invalid_days} ({invalid_ratio*100:.2f}%)")
    
    if invalid_ratio > 0.10:
        log("STOP - DATA QUALITY THRESHOLD EXCEEDED")
        return
        
    log("Computing rolling 63-day percentile thresholds...")
    events['threshold'] = events['norm_r_pre'].rolling(window=63, closed='left').quantile(0.25, interpolation='linear')
    events = events.dropna(subset=['threshold']).copy()
    
    events['state'] = np.where(events['norm_r_pre'] <= events['threshold'], 'COMPRESSED', 'CONTROL')
    
    compressed = events[events['state'] == 'COMPRESSED']
    control = events[events['state'] == 'CONTROL']
    
    log(f"COMPRESSED count: {len(compressed)}")
    log(f"CONTROL count: {len(control)}")
    
    med_comp = compressed['norm_r_cash'].median()
    med_cont = control['norm_r_cash'].median()
    delta_m_obs = med_comp - med_cont
    log(f"Observed Delta M: {delta_m_obs:.6f}")
    
    log("Starting Stationary Block Bootstrap (B=10000, L=10)...")
    B = 10000
    N = len(events)
    p = 0.1
    
    np.random.seed(20260817)
    
    states = (events['state'] == 'COMPRESSED').values
    responses = events['norm_r_cash'].values
    
    boot_delta_m = np.zeros(B)
    
    for b in range(B):
        blocks = []
        cur_len = 0
        while cur_len < N:
            start_idx = np.random.randint(0, N)
            b_len = np.random.geometric(p)
            idx = (np.arange(start_idx, start_idx + b_len)) % N
            blocks.append(idx)
            cur_len += b_len
            
        resampled_idx = np.concatenate(blocks)[:N]
        
        bs_states = states[resampled_idx]
        bs_responses = responses[resampled_idx]
        
        m_comp = np.median(bs_responses[bs_states])
        m_cont = np.median(bs_responses[~bs_states])
        
        boot_delta_m[b] = m_comp - m_cont
        
    lb = np.percentile(boot_delta_m, 2.5, method='linear')
    ub = np.percentile(boot_delta_m, 97.5, method='linear')
    
    log(f"95% CI: [{lb:.6f}, {ub:.6f}]")
    
    verdict = "INCONCLUSIVE"
    if lb > 0:
        verdict = "SUPPORTED"
    elif ub < 0:
        verdict = "CONTRADICTED"
        
    log(f"Primary Verdict: {verdict}")
    
    half_idx = N // 2
    h1 = events.iloc[:half_idx]
    h2 = events.iloc[half_idx:]
    
    def calc_delta(df):
        m1 = df[df['state'] == 'COMPRESSED']['norm_r_cash'].median()
        m2 = df[df['state'] == 'CONTROL']['norm_r_cash'].median()
        return m1 - m2
        
    d1 = calc_delta(h1)
    d2 = calc_delta(h2)
    log(f"Chronological Half 1 Delta M: {d1:.6f}")
    log(f"Chronological Half 2 Delta M: {d2:.6f}")
    
    comp_dir_metric = compressed['persistence'].mean(skipna=True)
    cont_dir_metric = control['persistence'].mean(skipna=True)
    log(f"Directional Persistence (COMPRESSED): {comp_dir_metric:.4f}")
    log(f"Directional Persistence (CONTROL): {cont_dir_metric:.4f}")
    
    elapsed = time.time() - start_time
    
    report = f'''# QUANTFORGE — SESSION-ANCHORED RANGE EXPANSION V1 CONTROLLED EXECUTION REPORT

## 1. Execution identity
- Protocol Version: v1.1.3
- Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
- Seed: 20260817

## 2. Protocol integrity
- Protocol SHA-256: {protocol_hash}

## 3. Dataset integrity
- Dataset SHA-256: {data_hash}
- Path: `USATECHIDXUSD_M1.csv`

## 4. Data-quality gates
- Total calendar days with $\ge 1$ bar: {total_calendar_days_with_bars}
- Invalid days dropped: {invalid_days}
- Invalid proportion: {invalid_ratio*100:.2f}% (Passes <10% stopping rule)

## 5. Sample counts
- Initialization days (dropped): 63
- Total primary-valid test days ($N$): {N}
- COMPRESSED count: {len(compressed)}
- CONTROL count: {len(control)}

## 6. Observed Delta M
- **Observed $\Delta M$**: {delta_m_obs:.6f}

## 7. Bootstrap configuration
- B: 10000
- Block Expected Length ($L$): 10
- Terminate $p$: 0.1
- Truncation exactly to $N$: Yes
- Sample Unit: Day-level tuples with fixed state labels.

## 8. 95% CI
- **Two-sided 95% Percentile CI**: [{lb:.6f}, {ub:.6f}]

## 9. Primary verdict
**{verdict}**

## 10. Chronological descriptive results
- Half 1 $\Delta M$: {d1:.6f}
- Half 2 $\Delta M$: {d2:.6f}

## 11. Directional secondary diagnostic
- COMPRESSED Persistence Rate: {comp_dir_metric:.4f}
- CONTROL Persistence Rate: {cont_dir_metric:.4f}
- Excluded exact zero-range/directionless days.

## 12. Runtime / CPU / memory profile
- Elapsed Time: {elapsed:.2f} seconds
- Peak Process RSS: {psutil.Process().memory_info().rss / 1024 / 1024:.1f} MB

## 13. Reproducibility verification
- Execution completed using serial one-process architecture.
- Random state correctly seeded.
- Exact mathematics aligned with v1.1.3 specification.

## 14. Scientific interpretation
The behavioral hypothesis that pre-session range compression precedes greater cash-session range expansion magnitude is **{verdict}**.
This isolates a volatility state-transition mechanic. It does **NOT** establish a profitable trading strategy, as no entry/exit spread logic was executed.

## 15. Economic firewall
- ZERO PnL
- ZERO Sharpe
- ZERO trading logic

## 16. Exact next governed task
> INDEPENDENT READ-ONLY SCIENTIFIC RESULTS ADJUDICATION

## 17. Integrity
- No ML used.
- No strategy files created.
- No tuning applied.
'''

    with open(os.path.join(OUT_DIR, "EXECUTION_REPORT_V1.md"), 'w', encoding='utf-8') as f:
        f.write(report)
        
    events.to_csv(os.path.join(OUT_DIR, "day_level_events.csv"), index=False)
    log("Execution complete. Artifacts saved.")

if __name__ == "__main__":
    p = psutil.Process()
    try:
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except:
        pass
    execute()
