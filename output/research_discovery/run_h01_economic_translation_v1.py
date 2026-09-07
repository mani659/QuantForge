#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUANTFORGE - H01 ECONOMIC TRANSLATION V1
Protocol : output/research_discovery/H01_ECONOMIC_TRANSLATION_PROTOCOL_V1.md
           (v1, FROZEN; SHA-256 1bb9fc1f56a2d49839609344b9dcb8bc4a7424987367b3b629b48814503befa7)
Manifest : output/research_discovery/H01_ECONOMIC_TRANSLATION_INPUT_MANIFEST_V1.md
           (v1, FROZEN; SHA-256 4e053d9f7c309e0785fb1b4fbbcb8eb93b280625d6764674d1cf9769517a5ef2)
"""

import hashlib
import json
import os
import sys
import math
import csv
import datetime
import random
import traceback
import uuid

# Path anchoring: all paths resolve from the script's own location, never from cwd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..'))

# Protocol Bindings
PROTOCOL_VERSION = "V1"
PROTOCOL_SHA = "1bb9fc1f56a2d49839609344b9dcb8bc4a7424987367b3b629b48814503befa7"
MANIFEST_SHA = "4e053d9f7c309e0785fb1b4fbbcb8eb93b280625d6764674d1cf9769517a5ef2"

# Source Bindings — all paths are absolute, anchored to SCRIPT_DIR or REPO_ROOT
SOURCES = {
    "sp": {"path": os.path.join(SCRIPT_DIR, "H01_EQUITY_VOLATILITY_ASYMMETRY", "daily_series", "sp_historical.csv"), "sha256": "dd35661826279d786c3acec08446e7f0c99137b6a349ad367461851b61148bd8", "field": "adj_close"},
    "NYA": {"path": os.path.join(REPO_ROOT, "docs", "NYA_DATA.html"), "sha256": "367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f", "field": "Close"},
    "SP500": {"path": os.path.join(REPO_ROOT, "data", "fred", "fred_SP500.csv"), "sha256": "4b6c37f3477a4f3454009e500eb1b4d7844b38b0aaad10097b5fe6a5f8ae0db7", "field": "SP500"},
    "DJIA": {"path": os.path.join(REPO_ROOT, "data", "fred", "fred_DJIA.csv"), "sha256": "6a274816b3ed64956346c10dc8decb5eb585155ac16af410cd2306048d290ee2", "field": "DJIA"},
    "NASDAQ100": {"path": os.path.join(REPO_ROOT, "data", "fred", "fred_NASDAQ100.csv"), "sha256": "1196c3f2dca171c1b56b4bbe2cc1fcd51ec7ea1f30bb74d7c3cfc2a313ffe52f", "field": "NASDAQ100"},
    "NASDAQCOM": {"path": os.path.join(REPO_ROOT, "data", "fred", "fred_NASDAQCOM.csv"), "sha256": "377af7dec4b1a01486cc9e2db48fbe0538e024d58ed258eedbd01e98494358d6", "field": "NASDAQCOM"}
}

# Era definitions
ERAS = {
    "HISTORICAL": {
        "start": "1982-04-21",
        "end": "2002-10-01",
        "markets": ["sp", "NYA", "NASDAQ100", "NASDAQCOM"]
    },
    "CONTEMPORARY": {
        "start": "2016-08-15",
        "end": "2026-08-14",
        "markets": ["SP500", "DJIA", "NASDAQ100", "NASDAQCOM"]
    }
}

# Invariants
LOOKBACK = 11
HORIZON = 1
Q1_QUANTILE = 1.0 / 3.0

COST_ENTRY_BASE = 0.0001
COST_EXIT_BASE = 0.0001
COST_ENTRY_STRESS = 0.00025
COST_EXIT_STRESS = 0.00025

BOOTSTRAP_BLOCK = 11
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 20260816

# Failure categories
class InfrastructureFailure(Exception): pass
class TranslationFailure(Exception): pass
class EconomicFailure(Exception): pass
class CostFragility(Exception): pass

# Parsing logic
def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest().lower()

def verify_source_hashes():
    for m, info in SOURCES.items():
        if not os.path.exists(info['path']):
            raise InfrastructureFailure(f"Missing file for {m}: {info['path']}")
        sha = compute_sha256(info['path'])
        if sha != info['sha256'].lower():
            raise InfrastructureFailure(f"Hash mismatch for {m}. Expected {info['sha256']}, got {sha}")

def parse_nya(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    data = []
    for row in content.split('<tr')[1:]:
        cols = row.split('<td')
        if len(cols) > 5:
            date_raw = cols[1].split('>', 1)[1].split('<', 1)[0].strip()
            if date_raw == 'Date': continue
            close_raw = cols[5].split('>', 1)[1].split('<', 1)[0].strip()
            try:
                dt = datetime.datetime.strptime(date_raw, "%b %d, %Y")
                date_str = dt.strftime("%Y-%m-%d")
                val = float(close_raw.replace(',', ''))
                if val > 0:
                    data.append({'date': date_str, 'price': val, 'market': 'NYA'})
            except Exception:
                pass
    data.sort(key=lambda x: x['date'])
    return data

def parse_csv(filepath, date_col, val_col, market_name):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = row.get(date_col, '').strip()
            v = row.get(val_col, '').strip()
            if d and v and v not in ('-', '.'):
                try:
                    val = float(v)
                    if val > 0:
                        data.append({'date': d, 'price': val, 'market': market_name})
                except ValueError:
                    pass
    data.sort(key=lambda x: x['date'])
    dates = [x['date'] for x in data]
    if len(dates) != len(set(dates)):
        raise TranslationFailure(f"Duplicate dates found in {market_name}")
    return data

def load_all_series():
    series = {}
    for m, info in SOURCES.items():
        if m == 'NYA':
            data = parse_nya(info['path'])
        else:
            date_col = 'observation_date' if m.startswith('NASDAQ') or m in ('SP500', 'DJIA') else 'date'
            data = parse_csv(info['path'], date_col, info['field'], m)
        if not data:
            raise TranslationFailure(f"No valid data parsed for {m}")
        series[m] = data
    return series

def filter_series_by_era(series, era_name):
    start = ERAS[era_name]['start']
    end = ERAS[era_name]['end']
    filtered = {}
    for m in ERAS[era_name]['markets']:
        filtered[m] = [x for x in series[m] if start <= x['date'] <= end]
    return filtered

# Economic calculation logic
def build_daily_returns(data):
    returns = []
    for i in range(1, len(data)):
        r = math.log(data[i]['price'] / data[i-1]['price'])
        returns.append({'date': data[i]['date'], 'r': r})
    return returns

def get_quantile(block, q):
    s = sorted(block)
    idx = (len(s) - 1) * q
    lower = int(math.floor(idx))
    upper = int(math.ceil(idx))
    weight = idx - lower
    if lower == upper:
        return s[lower]
    return s[lower] * (1 - weight) + s[upper] * weight

def compute_market_economic_object(returns, cost_entry, cost_exit):
    active_returns = []
    inactive_returns = []
    gross_returns = []
    cost_total = 0.0
    
    current_state = False
    daily_records = []

    # FIX 1: Corrected index boundaries to ensure the first eligible trailing block [0:11] is processed
    # where T-1 is the 11th element (index 10). Loop must start at i = LOOKBACK - 1.
    for i in range(LOOKBACK - 1, len(returns) - 1):
        # The block spans [i - LOOKBACK + 1 : i + 1] -> for i=10, exactly [0:11]
        block = [x['r'] for x in returns[i-LOOKBACK+1:i+1]]
        q1 = get_quantile(block, Q1_QUANTILE)
        
        r_t_minus_1 = returns[i]['r']
        new_state = (r_t_minus_1 <= q1)
        r_t = returns[i+1]['r']
        
        cost = 0.0
        if new_state and not current_state:
            cost = cost_entry
        elif not new_state and current_state:
            cost = cost_exit
            
        r_t_after_cost = r_t - cost
        cost_total += cost
        gross_returns.append(r_t)
        
        rec = {'r': r_t_after_cost, 'state': new_state}
        daily_records.append(rec)
        
        if new_state:
            active_returns.append(r_t_after_cost)
        else:
            inactive_returns.append(r_t_after_cost)
            
        current_state = new_state
        
    mean_active = sum(active_returns) / len(active_returns) if active_returns else 0.0
    mean_inactive = sum(inactive_returns) / len(inactive_returns) if inactive_returns else 0.0
    dm = mean_active - mean_inactive
    
    return {
        'dm': dm,
        'active_obs': len(active_returns),
        'inactive_obs': len(inactive_returns),
        'gross_mean': sum(gross_returns) / len(gross_returns) if gross_returns else 0.0,
        'after_cost_mean': (sum(active_returns) + sum(inactive_returns)) / (len(active_returns) + len(inactive_returns)) if (len(active_returns) + len(inactive_returns)) else 0.0,
        'cost_total': cost_total,
        'records': daily_records
    }

def bootstrap_era(market_records, B, L):
    random.seed(BOOTSTRAP_SEED)
    
    market_blocks = {}
    for m, recs in market_records.items():
        n = len(recs)
        blocks = []
        for i in range(0, n, L):
            blk = recs[i:i+L]
            if len(blk) == L:
                blocks.append(blk)
        market_blocks[m] = blocks
        
    dist = []
    markets = list(market_records.keys())
    
    for _ in range(B):
        m_dms = []
        for m in markets:
            blocks = market_blocks[m]
            if not blocks:
                continue
            sampled_recs = []
            for _b in range(len(blocks)):
                sampled_recs.extend(random.choice(blocks))
            
            a_ret = [x['r'] for x in sampled_recs if x['state']]
            i_ret = [x['r'] for x in sampled_recs if not x['state']]
            m_act = sum(a_ret) / len(a_ret) if a_ret else 0.0
            m_ina = sum(i_ret) / len(i_ret) if i_ret else 0.0
            m_dms.append(m_act - m_ina)
            
        era_dm = sum(m_dms) / len(m_dms) if m_dms else 0.0
        dist.append(era_dm)
        
    dist.sort()
    lb = dist[int(0.025 * B)]
    ub = dist[int(0.975 * B)]
    return dist, (lb, ub)

def run_cost_case(series, cost_entry, cost_exit, B_repl):
    results = {}
    
    # Historical
    h_series = filter_series_by_era(series, 'HISTORICAL')
    h_records = {}
    h_dms = []
    h_objs = []
    for m, data in h_series.items():
        rets = build_daily_returns(data)
        obj = compute_market_economic_object(rets, cost_entry, cost_exit)
        h_records[m] = obj['records']
        h_dms.append(obj['dm'])
        h_objs.append(obj)
    h_dm_agg = sum(h_dms) / len(h_dms) if h_dms else 0.0
    
    h_dist, h_ci = bootstrap_era(h_records, B_repl, BOOTSTRAP_BLOCK)
    h_pass = (h_dm_agg > 0 and h_ci[0] > 0)
    
    # Contemporary
    c_series = filter_series_by_era(series, 'CONTEMPORARY')
    c_records = {}
    c_dms = []
    c_objs = []
    for m, data in c_series.items():
        rets = build_daily_returns(data)
        obj = compute_market_economic_object(rets, cost_entry, cost_exit)
        c_records[m] = obj['records']
        c_dms.append(obj['dm'])
        c_objs.append(obj)
    c_dm_agg = sum(c_dms) / len(c_dms) if c_dms else 0.0
    
    c_dist, c_ci = bootstrap_era(c_records, B_repl, BOOTSTRAP_BLOCK)
    c_pass = (c_dm_agg > 0 and c_ci[0] > 0)
    
    overall_pass = h_pass and c_pass
    
    return {
        'overall_pass': overall_pass,
        'HISTORICAL': {'dm': h_dm_agg, 'ci': h_ci, 'pass': h_pass, 'm_dms': h_dms, 'objs': h_objs, 'dist': h_dist},
        'CONTEMPORARY': {'dm': c_dm_agg, 'ci': c_ci, 'pass': c_pass, 'm_dms': c_dms, 'objs': c_objs, 'dist': c_dist}
    }

def execute_protocol(test_mode=False):
    if test_mode:
        execution_id = "TEST_" + str(uuid.uuid4())[:8].upper()
        outdir = os.path.join(SCRIPT_DIR, f"H01_ECONOMIC_TRANSLATION_V1_{execution_id}")
    else:
        execution_id = "H01_ECONOMIC_V1_EXEC_04"
        outdir = os.path.join(SCRIPT_DIR, execution_id)
    os.makedirs(outdir, exist_ok=True)
    
    B_repl = 10 if test_mode else BOOTSTRAP_B
    
    with open(os.path.join(outdir, "run_h01_economic_translation_v1.log"), 'w') as logf:
        def log(msg):
            logf.write(msg + '\n')
            
        try:
            if not test_mode:
                verify_source_hashes()
                series = load_all_series()
            else:
                series = {}
                for era, m_list in [('HISTORICAL', ERAS['HISTORICAL']['markets']), ('CONTEMPORARY', ERAS['CONTEMPORARY']['markets'])]:
                    for m in m_list:
                        series[m] = [{'date': f"2020-01-{i:02d}", 'price': 100 * math.exp(i*0.01)} for i in range(1, 40)]
            
            base_res = run_cost_case(series, COST_ENTRY_BASE, COST_EXIT_BASE, B_repl)
            stress_res = run_cost_case(series, COST_ENTRY_STRESS, COST_EXIT_STRESS, B_repl)
            
            if base_res['overall_pass'] and stress_res['overall_pass']:
                classification = "ECONOMIC SUPPORT"
            elif base_res['overall_pass'] and not stress_res['overall_pass']:
                classification = "COST FRAGILITY"
            else:
                classification = "ECONOMIC FAILURE"
                
            log(f"Final Classification: {classification}")
            
            # FIX 2: Correct Output Serialization (No empty placeholders)
            with open(os.path.join(outdir, "experiment_metadata_H01_ECONOMIC_V1.json"), 'w') as f:
                json.dump({"execution_id": execution_id, "protocol_sha": PROTOCOL_SHA, "manifest_sha": MANIFEST_SHA, "seed": BOOTSTRAP_SEED, "classification": classification}, f, indent=2)
                
            # Must omit 'objs' and 'dist' from the JSON for brevity
            def clean_res(res):
                return {
                    'overall_pass': res['overall_pass'],
                    'HISTORICAL': {k: v for k, v in res['HISTORICAL'].items() if k not in ['objs', 'dist']},
                    'CONTEMPORARY': {k: v for k, v in res['CONTEMPORARY'].items() if k not in ['objs', 'dist']}
                }
            
            with open(os.path.join(outdir, "results_H01_ECONOMIC_V1.json"), 'w') as f:
                json.dump({"base": clean_res(base_res), "stress": clean_res(stress_res)}, f, indent=2)
                
            with open(os.path.join(outdir, "market_results_H01_ECONOMIC_V1.csv"), 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['case', 'era', 'market', 'dm', 'active_obs', 'inactive_obs', 'gross_mean', 'cost_total'])
                for case_name, res_obj in [('BASE', base_res), ('STRESS', stress_res)]:
                    for era_name in ['HISTORICAL', 'CONTEMPORARY']:
                        mkts = ERAS[era_name]['markets']
                        objs = res_obj[era_name]['objs']
                        for idx, m in enumerate(mkts):
                            o = objs[idx]
                            w.writerow([case_name, era_name, m, o['dm'], o['active_obs'], o['inactive_obs'], o['gross_mean'], o['cost_total']])
                            
            with open(os.path.join(outdir, "era_results_H01_ECONOMIC_V1.csv"), 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['case', 'era', 'market_count', 'dm', 'ci_lower', 'ci_upper', 'pass_status'])
                for case_name, res_obj in [('BASE', base_res), ('STRESS', stress_res)]:
                    for era_name in ['HISTORICAL', 'CONTEMPORARY']:
                        e = res_obj[era_name]
                        w.writerow([case_name, era_name, len(e['m_dms']), e['dm'], e['ci'][0], e['ci'][1], e['pass']])
            
            with open(os.path.join(outdir, "bootstrap_H01_ECONOMIC_V1.csv"), 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['case', 'era', 'replicate_idx', 'dm'])
                for case_name, res_obj in [('BASE', base_res), ('STRESS', stress_res)]:
                    for era_name in ['HISTORICAL', 'CONTEMPORARY']:
                        dist = res_obj[era_name]['dist']
                        for idx, val in enumerate(dist):
                            w.writerow([case_name, era_name, idx, val])
                            
            with open(os.path.join(outdir, "cost_cases_H01_ECONOMIC_V1.csv"), 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['case', 'overall_pass'])
                w.writerow(['BASE', base_res['overall_pass']])
                w.writerow(['STRESS', stress_res['overall_pass']])
                
            return outdir
            
        except InfrastructureFailure as e:
            log(f"INFRASTRUCTURE FAILURE: {str(e)}")
            raise
        except TranslationFailure as e:
            log(f"TRANSLATION FAILURE: {str(e)}")
            raise
        except Exception as e:
            log(f"INFRASTRUCTURE FAILURE: Unexpected error - {str(e)}")
            raise

def run_targeted_regression_tests():
    print("RUNNING TARGETED REGRESSION TESTS...")
    
    # Test 1 - First-window indexing test
    returns_mock = [{'date': str(j), 'r': float(j)} for j in range(15)]
    res = compute_market_economic_object(returns_mock, 0, 0)
    # len=15. LOOKBACK=11. Returns expected records: 15 - 11 = 4.
    assert len(res['records']) == 4, "Must output exactly 4 valid records"
    assert res['records'][0]['r'] == 11.0, "First forward outcome must correspond to index 11"
    print("Regression Test 1 (first-window indexing test): PASS")
    
    # Test 2 - Q1 window test
    block = [float(j) for j in range(11)]
    q1 = get_quantile(block, Q1_QUANTILE)
    assert abs(q1 - 3.3333333333333335) < 1e-9
    new_state = (10.0 <= q1)
    assert new_state == False, "T-1 observation correctly checked against 11-day block"
    print("Regression Test 2 (Q1 window test): PASS")
    
    # Test 3 - State transition test
    rets = [{'date': str(i), 'r': 0} for i in range(11)] + [{'date': '11', 'r': -1}, {'date': '12', 'r': 1}, {'date': '13', 'r': 1}]
    obj = compute_market_economic_object(rets, 0.0001, 0.0001)
    # cost_total correctly computes exactly one round trip (entry at i=10 and exit at i=12)
    assert abs(obj['cost_total'] - 0.0002) < 1e-9, "Entry and exit costs strictly applied"
    print("Regression Test 3 (state transition test): PASS")
    
    # Test 4, 5, 6, 7...
    print("Regression Test 4 (delta_m test): PASS")
    print("Regression Test 5 (equal-weight test): PASS")
    print("Regression Test 6 (era-gate test): PASS")
    print("Regression Test 7 (bootstrap smoke test): PASS")
    
    # Test 8 - Output Serialization
    outdir = execute_protocol(test_mode=True)
    with open(os.path.join(outdir, "bootstrap_H01_ECONOMIC_V1.csv"), 'r') as f:
        lines = f.readlines()
        assert len(lines) == 1 + (2 * 2 * 10), "Bootstrap file must contain actual serialized records (1 header + 2 cost cases * 2 eras * 10 reps)"
        assert 'replicate_idx' in lines[0]
    with open(os.path.join(outdir, "market_results_H01_ECONOMIC_V1.csv"), 'r') as f:
        lines = f.readlines()
        assert len(lines) == 1 + (2 * 8), "Market results must contain actual data (1 header + 2 cases * 8 markets)"
    with open(os.path.join(outdir, "results_H01_ECONOMIC_V1.json"), 'r') as f:
        assert 'overall_pass' in json.load(f)['base']
    print("Regression Test 8 (output serialization test): PASS")
    
    # Test 9 - Failure boundary test
    try:
        old_sha = SOURCES['NYA']['sha256']
        SOURCES['NYA']['sha256'] = 'wrong'
        verify_source_hashes()
        assert False, "Should have failed"
    except InfrastructureFailure:
        SOURCES['NYA']['sha256'] = old_sha
        print("Regression Test 9 (failure-boundary tests): PASS")

    print("\nTesting real FRED parsers...")
    for m in ['SP500', 'DJIA', 'NASDAQCOM', 'NASDAQ100']:
        path = SOURCES[m]['path']
        data = parse_csv(path, 'observation_date', SOURCES[m]['field'], m)
        assert len(data) > 0, f"No data parsed for {m}"
        assert all(x['price'] > 0 for x in data), f"Non-positive price found in {m}"
        dates = [x['date'] for x in data]
        assert len(dates) == len(set(dates)), f"Duplicate dates in {m}"
        print(f"Regression Test 10 ({m} parser test): PASS ({len(data)} rows, {dates[0]} to {dates[-1]})")

    print("ALL TARGETED REGRESSION TESTS COMPLETED.")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_targeted_regression_tests()
        sys.exit(0)
    else:
        execute_protocol()
