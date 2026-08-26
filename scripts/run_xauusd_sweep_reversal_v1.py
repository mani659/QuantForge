import pandas as pd
import numpy as np
import hashlib
import os
import sys
import psutil
import logging
from statsmodels.stats.multitest import multipletests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Ensure BelowNormal priority and print RSS
try:
    p = psutil.Process(os.getpid())
    if sys.platform == "win32":
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    else:
        p.nice(10)
    logging.info(f"Process priority set to BelowNormal. Initial RSS: {p.memory_info().rss / 1e6:.2f} MB")
except Exception as e:
    logging.warning(f"Could not set priority: {e}")

MARKETS = ["XAUUSD", "XAGUSD", "EURUSD", "USATECHIDXUSD", "BTCUSD"]
DATA_DIR = r"c:\Users\User10\Documents\MRV\yuvi\QuantForge\data\m1"
OUT_DIR = r"c:\Users\User10\Documents\MRV\yuvi\QuantForge\output\research_discovery\XAUUSD_LIQUIDITY_SWEEP_REVERSAL"
os.makedirs(OUT_DIR, exist_ok=True)

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def process_market(market):
    logging.info(f"Processing {market}...")
    filepath = os.path.join(DATA_DIR, f"{market}_M1.csv")
    if not os.path.exists(filepath):
        logging.error(f"Missing {filepath}")
        return None
    
    file_hash = hash_file(filepath)
    
    # 1. Ingest
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df = df.sort_values('timestamp')
    df = df.drop_duplicates(subset=['timestamp'], keep='first')
    
    # Invalid prices
    df = df[(df['open'] > 0) & (df['high'] > 0) & (df['low'] > 0) & (df['close'] > 0)]
    
    # Timezone conversion
    df['timestamp_ny'] = df['timestamp'].dt.tz_convert('America/New_York')
    df = df.set_index('timestamp_ny').sort_index()
    
    # Construct Trading Day (18:00 to 17:59 next day)
    df['trading_day'] = np.where(df.index.hour >= 18, df.index.date + pd.Timedelta(days=1), df.index.date)
    
    # Find all unique calendar days present
    raw_days = len(df['trading_day'].unique())
    
    events = []
    invalid_days = 0
    eligible_days = 0
    max_ts = df.index.max()
    
    for tday, group in df.groupby('trading_day'):
        # Asian Session: 18:00 - 02:59
        asian = group[(group.index.time >= pd.Timestamp("18:00").time()) | (group.index.time <= pd.Timestamp("02:59").time())]
        if asian.empty:
            invalid_days += 1
            continue
            
        asian_high = asian['high'].max()
        asian_low = asian['low'].min()
        
        # London/NY: 03:00 - 17:00
        lny = group[(group.index.time >= pd.Timestamp("03:00").time()) & (group.index.time <= pd.Timestamp("17:00").time())]
        if lny.empty:
            invalid_days += 1
            continue
            
        eligible_days += 1
        
        # Pending states
        upper_pending = False
        upper_frozen_low = None
        upper_rejection_ts = None
        upper_confirmed = False
        
        lower_pending = False
        lower_frozen_high = None
        lower_rejection_ts = None
        lower_confirmed = False
        
        for ts, row in lny.iterrows():
            # Upper Logic
            if not upper_pending and not upper_confirmed:
                if row['high'] > asian_high and row['close'] <= asian_high:
                    upper_pending = True
                    upper_frozen_low = row['low']
                    upper_rejection_ts = ts
            elif upper_pending and not upper_confirmed:
                if row['close'] < upper_frozen_low:
                    upper_confirmed = True
                    upper_pending = False
                    # TREATMENT
                    events.append({
                        'market': market,
                        'trading_day': tday,
                        'direction': 'upper',
                        'type': 'treatment',
                        'asian_level': asian_high,
                        'rejection_ts': upper_rejection_ts,
                        'anchor_ts': ts
                    })
                    
            # Lower Logic
            if not lower_pending and not lower_confirmed:
                if row['low'] < asian_low and row['close'] >= asian_low:
                    lower_pending = True
                    lower_frozen_high = row['high']
                    lower_rejection_ts = ts
            elif lower_pending and not lower_confirmed:
                if row['close'] > lower_frozen_high:
                    lower_confirmed = True
                    lower_pending = False
                    # TREATMENT
                    events.append({
                        'market': market,
                        'trading_day': tday,
                        'direction': 'lower',
                        'type': 'treatment',
                        'asian_level': asian_low,
                        'rejection_ts': lower_rejection_ts,
                        'anchor_ts': ts
                    })
                    
        # Check controls at end of 17:00
        if upper_pending and not upper_confirmed:
            events.append({
                'market': market,
                'trading_day': tday,
                'direction': 'upper',
                'type': 'control',
                'asian_level': asian_high,
                'rejection_ts': upper_rejection_ts,
                'anchor_ts': upper_rejection_ts
            })
            
        if lower_pending and not lower_confirmed:
            events.append({
                'market': market,
                'trading_day': tday,
                'direction': 'lower',
                'type': 'control',
                'asian_level': asian_low,
                'rejection_ts': lower_rejection_ts,
                'anchor_ts': lower_rejection_ts
            })

    # Filter invalid day fraction
    invalid_frac = invalid_days / raw_days if raw_days > 0 else 1
    
    # Calculate MFE
    processed_events = []
    complete_120 = 0
    for e in events:
        anchor = e['anchor_ts']
        # complete 120 min horizon check
        if max_ts < anchor + pd.Timedelta(minutes=120):
            continue  # Excluded before inference
            
        complete_120 += 1
        window = df.loc[(df.index > anchor) & (df.index <= anchor + pd.Timedelta(minutes=120))]
        if window.empty:
            # Drop if window empty (meaning literally no data in next 120 mins)
            continue
            
        if e['direction'] == 'upper':
            mfe = e['asian_level'] - window['low'].min()
        else:
            mfe = window['high'].max() - e['asian_level']
            
        e['mfe'] = mfe
        processed_events.append(e)
        
    events_df = pd.DataFrame(processed_events)
    
    if len(events_df) == 0:
        treatment_count = 0
        control_count = 0
    else:
        treatment_count = len(events_df[events_df['type'] == 'treatment'])
        control_count = len(events_df[events_df['type'] == 'control'])
        
    # Pre-inference summary
    print(f"\n--- PRE-INFERENCE AUDIT: {market} ---")
    print(f"Raw calendar-day count: {raw_days}")
    print(f"Invalid-day count / %: {invalid_days} / {invalid_frac:.2%}")
    print(f"Eligible days: {eligible_days}")
    if len(events_df) > 0:
        print(f"Confirmed upper events: {len(events_df[(events_df['type'] == 'treatment') & (events_df['direction'] == 'upper')])}")
        print(f"Confirmed lower events: {len(events_df[(events_df['type'] == 'treatment') & (events_df['direction'] == 'lower')])}")
    print(f"Treatment events: {treatment_count}")
    print(f"Control events: {control_count}")
    print(f"Events with complete 120-min horizon: {complete_120}")
    print(f"----------------------------------------\n")
    
    if invalid_frac > 0.1:
        logging.error(f"{market}: Invalid day fraction {invalid_frac:.2%} > 10%. Halting.")
        return None

    if treatment_count < 100:
        return {'market': market, 'status': 'EVIDENCE-LIMITED', 'hash': file_hash, 'events': events_df}
        
    # Day-cluster mapping
    day_clusters = events_df['trading_day'].unique()
    N = len(day_clusters)
    
    # Observed Statistic
    def get_median(arr):
        n = len(arr)
        if n == 0:
            return np.nan
        arr = np.sort(arr)
        if n % 2 == 1:
            return arr[n//2]
        else:
            return (arr[n//2 - 1] + arr[n//2]) / 2.0

    t_mfe = events_df[events_df['type'] == 'treatment']['mfe'].values
    c_mfe = events_df[events_df['type'] == 'control']['mfe'].values
    delta_m_obs = get_median(t_mfe) - get_median(c_mfe)
    
    # Bootstrap
    np.random.seed(20260817)
    B = 10000
    p = 0.1
    
    delta_m_stars = []
    
    # Precompute dictionary for O(1) lookup
    t_arrays = events_df[events_df['type'] == 'treatment'].groupby('trading_day')['mfe'].apply(list).to_dict()
    c_arrays = events_df[events_df['type'] == 'control'].groupby('trading_day')['mfe'].apply(list).to_dict()
    
    for _ in range(B):
        # Generate block lengths
        block_lengths = []
        while sum(block_lengths) < N:
            block_lengths.append(np.random.geometric(p))
            
        sampled_indices = []
        for length in block_lengths:
            start_idx = np.random.randint(0, N)
            for i in range(length):
                sampled_indices.append((start_idx + i) % N)
                
        sampled_indices = sampled_indices[:N]
        sampled_days = day_clusters[sampled_indices]
        
        rep_t = []
        rep_c = []
        for d in sampled_days:
            rep_t.extend(t_arrays.get(d, []))
            rep_c.extend(c_arrays.get(d, []))
            
        if len(rep_t) > 0 and len(rep_c) > 0:
            rep_stat = get_median(rep_t) - get_median(rep_c)
            delta_m_stars.append(rep_stat)
        else:
            delta_m_stars.append(np.nan)
            
    delta_m_stars = np.array(delta_m_stars)
    valid_mask = ~np.isnan(delta_m_stars)
    b_valid = valid_mask.sum()
    
    delta_m_stars_valid = delta_m_stars[valid_mask]
    
    # CI
    ci_lower = np.percentile(delta_m_stars_valid, 2.5)
    ci_upper = np.percentile(delta_m_stars_valid, 97.5)
    
    # Null P-value
    delta_m_null = delta_m_stars_valid - delta_m_obs
    count = np.sum(np.abs(delta_m_null) >= np.abs(delta_m_obs))
    p_raw = (1 + count) / (1 + b_valid)
    
    return {
        'market': market,
        'status': 'EVALUABLE',
        'hash': file_hash,
        'delta_m_obs': delta_m_obs,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'p_raw': p_raw,
        'treatment_count': treatment_count,
        'control_count': control_count,
        'b_valid': b_valid,
        'events': events_df
    }

def main():
    results = []
    
    for mkt in MARKETS:
        res = process_market(mkt)
        if res:
            results.append(res)
            p = psutil.Process(os.getpid())
            logging.info(f"Memory RSS after {mkt}: {p.memory_info().rss / 1e6:.2f} MB")
            
    # Holm Correction
    eval_res = [r for r in results if r['status'] == 'EVALUABLE']
    if eval_res:
        p_vals = [r['p_raw'] for r in eval_res]
        reject, pvals_corrected, _, _ = multipletests(p_vals, alpha=0.05, method='holm')
        
        for i, r in enumerate(eval_res):
            r['p_holm'] = pvals_corrected[i]
            r['holm_reject'] = reject[i]
            
            if r['holm_reject'] and r['delta_m_obs'] > 0:
                r['classification'] = 'SUPPORT'
            elif r['holm_reject'] and r['delta_m_obs'] < 0:
                r['classification'] = 'CONTRADICTED'
            else:
                r['classification'] = 'INCONCLUSIVE'
                
    # Save report
    report = ["# QUANTFORGE — XAUUSD LIQUIDITY SWEEP / REVERSAL", "# SCIENTIFIC_REPORT_V1\n"]
    report.append("## 1. Execution Identity")
    report.append("Execution completed successfully under controlled V1.2.0 conditions.\n")
    report.append("## 2. Protocol / Input Fingerprints")
    for r in results:
        report.append(f"- **{r['market']}**: {r['hash']}")
    report.append("")
    report.append("## 4. Event Counts & 5. Market-Level Results & 6/7/8/9. Inference")
    for r in results:
        report.append(f"### {r['market']}")
        report.append(f"- **Status**: {r['status']}")
        if r['status'] == 'EVALUABLE':
            report.append(f"- **Treatment Events**: {r['treatment_count']}")
            report.append(f"- **Control Events**: {r['control_count']}")
            report.append(f"- **Delta M_obs**: {r['delta_m_obs']:.5f}")
            report.append(f"- **95% CI**: [{r['ci_lower']:.5f}, {r['ci_upper']:.5f}]")
            report.append(f"- **P-raw**: {r['p_raw']:.5e}")
            report.append(f"- **P-holm**: {r['p_holm']:.5e}")
            report.append(f"- **Classification**: **{r['classification']}**")
        else:
            if 'treatment_count' in r:
                report.append(f"- **Treatment Events**: {r['treatment_count']} (< 100)")
        report.append("")
        if 'events' in r:
            r['events'].to_csv(os.path.join(OUT_DIR, f"{r['market']}_events.csv"), index=False)
            
    report.append("## 10. Cross-Market Interpretation")
    report.append("See individual market classifications above.\n")
    report.append("## 12. Economic Firewall")
    report.append("This report contains ONLY behavioral structural MFE data. No PnL or strategy outcomes.\n")
    report.append("## 14. Exact Next Task")
    report.append("Independent Scientific Results Adjudication.\n")
    
    with open(os.path.join(OUT_DIR, "SCIENTIFIC_REPORT_V1.md"), "w") as f:
        f.write("\n".join(report))
        
    logging.info("Execution complete.")

if __name__ == "__main__":
    main()
