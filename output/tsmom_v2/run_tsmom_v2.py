#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUANTFORGE — TSMOM V2 DRIFT-CONTROLLED IDENTIFICATION STUDY — CONTROLLED EXECUTION V1
Protocol: output/tsmom_v2/EVENT_STUDY_PROTOCOL_TSMOM_V2_DRIFT_CONTROL.md (v2.0.0, FROZEN)
Executes the frozen protocol exactly; no tuning, no cell selection, no TEST reuse.
Artifacts written under output/tsmom_v2/ (never overwriting the protocol).
"""
import hashlib, json, math, os, sys, time
from datetime import datetime

import numpy as np

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

OUT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(OUT, '.build_cache')
os.makedirs(CACHE, exist_ok=True)

HPD = r'C:\Users\User10\AppData\Local\Temp\quantforge_tsmom_hpd_full'
REPO = r'C:\Users\User10\Documents\MRV\yuvi\QuantForge'
PROTOCOL_PATH = os.path.join(OUT, 'EVENT_STUDY_PROTOCOL_TSMOM_V2_DRIFT_CONTROL.md')
V1_META = os.path.join(REPO, 'output', 'tsmom_v1', 'experiment_metadata_TSMOM_V1.json')
V1_CACHE = os.path.join(REPO, 'output', 'tsmom_v1', '.build_cache')

MARKETS = ['XAUUSD', 'EURUSD', 'BTCUSD', 'XAGUSD', 'USATECHIDXUSD']
BIDASK_MARKETS = ['XAUUSD', 'BTCUSD', 'XAGUSD', 'USATECHIDXUSD']

CORE = ['ad','bp','c','cd','cl','cr','ct','dx','ed','fc','gc','hg','ho','jo','jy',
        'kc','lh','o','pa','pb','pl','s','sb','sf','si','sp','us','w']

ASSET = {'FX':['ad','bp','cd','dx','jy','sf'], 'Metals':['gc','si','hg','pl','pa'],
         'Grains':['c','o','s','w'], 'Softs':['ct','jo','kc','sb'],
         'Livestock':['fc','lh','pb'], 'Energy':['cl','ho'], 'Rates':['ed','us'],
         'Equity index':['sp'], 'Index':['cr']}
ROOT2CLASS = {r: c for c, ms in ASSET.items() for r in ms}

SEED_F1 = 20260813
SEED_LB = 20260814
SEED_NC1 = 20260815
SEED_NC3 = 20260816
SEED_NC4 = 20260817
SEED_F2 = SEED_F1
B_REPL = 10000
L_BLOCK = 12
LAG = 24
BP = 0.0001
EURUSD_H_ASSUMED_BP = 0.1
T0 = time.time()

# ----------------------------------------------------------------------------
# utils / fingerprints
# ----------------------------------------------------------------------------

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def ym_key(ym):
    return f'{ym[0]:04d}-{ym[1]:02d}'

def add_months(ym, k):
    y, mo = ym
    i = y * 12 + (mo - 1) + k
    return (i // 12, i % 12 + 1)

def ym_to_seq(ym):
    return ym[0] * 12 + (ym[1] - 1)

# ----------------------------------------------------------------------------
# 1. Layer A — historical HPD panel (front_<root>.csv, adj_close continuous)
# ----------------------------------------------------------------------------

def load_front(root, win_start=None, win_end=None):
    """Return (monthly: dict ym -> (close, dstr), daily: list of (dstr, close)).
    When win_start/win_end given (YYYY-MM-DD), rows outside the common window are dropped."""
    path = os.path.join(HPD, f'front_{root}.csv')
    daily = []
    monthly = {}
    with open(path, newline='') as f:
        header = f.readline()
        for line in f:
            line = line.rstrip('\r\n')
            if not line:
                continue
            p = line.split(',')
            if len(p) < 4:
                continue
            dstr = p[0]
            if win_start is not None and dstr < win_start:
                continue
            if win_end is not None and dstr > win_end:
                continue
            close = float(p[3])
            daily.append((dstr, close))
            ym = (int(dstr[0:4]), int(dstr[5:7]))
            monthly[ym] = (close, dstr)
    return monthly, daily

def common_window_from_manifest(roots):
    """Common identification window = [max(first), min(last)] over the 28 core markets (protocol Section 5)."""
    firsts, lasts = {}, {}
    with open(os.path.join(HPD, 'HPD_MANIFEST.csv'), newline='') as f:
        import csv
        r = csv.DictReader(f)
        for row in r:
            if row['root'] in roots:
                firsts[row['root']] = row['first']
                lasts[row['root']] = row['last']
    if len(firsts) != len(roots):
        raise RuntimeError(f'manifest root mismatch: {len(firsts)} vs {len(roots)}')
    return max(firsts.values()), min(lasts.values())

def monthly_returns(monthly):
    months = sorted(monthly.keys())
    R = {}
    for i in range(1, len(months)):
        prev, cur = months[i - 1], months[i]
        R[cur] = monthly[cur][0] / monthly[prev][0] - 1.0
    return R

def sigma_ann(daily, end_dstr):
    import bisect
    days = [d[0] for d in daily]
    idx = bisect.bisect_right(days, end_dstr) - 1
    if idx < 0:
        return None
    lo = max(0, idx - 20)
    closes = [daily[i][1] for i in range(lo, idx + 1)]
    if len(closes) < 6:
        return None
    rets = [closes[i] / closes[i - 1] - 1.0 for i in range(1, len(closes))]
    if len(rets) < 5:
        return None
    return float(np.std(rets, ddof=1) * math.sqrt(252))

def build_assessments_hpd(root, monthly, daily, outcome_shift=0):
    """Per protocol Section 4 (12/1 mechanism, uncapped inv-vol)."""
    months = sorted(monthly.keys())
    mset = set(months)
    R = monthly_returns(monthly)
    out = []
    for pos in months:
        ok = True
        L = 1.0
        for k in range(12, 1, -1):
            ym = add_months(pos, -k)
            if ym not in R:
                ok = False
                break
            L *= (1.0 + R[ym])
        if not ok:
            continue
        L -= 1.0
        outc_m = add_months(pos, outcome_shift)
        if outc_m not in R:
            continue
        outc = R[outc_m]
        am = add_months(pos, -1)
        if am not in monthly:
            continue
        a_ts = monthly[am][1]
        sig = sigma_ann(daily, a_ts)
        if sig is None:
            continue
        S = 1 if L > 0 else -1
        w = 0.40 / sig
        p_tsmom = w * S
        p_long = w
        r_tsmom = p_tsmom * outc
        r_long = p_long * outc
        dr = r_tsmom - r_long
        out.append({'root': root, 'pos': pos, 'outc': outc, 'L': L, 'S': S,
                    'sigma': sig, 'w': w, 'p_tsmom': p_tsmom, 'p_long': p_long,
                    'r_tsmom': r_tsmom, 'r_long': r_long, 'dr': dr})
    return out

# ----------------------------------------------------------------------------
# 2. Layer B — contemporary panel (data/m1, V1 Section 6 aggregation)
# ----------------------------------------------------------------------------

def epoch_of(y, mo, d, h, mi, s):
    y2 = y - (1 if mo <= 2 else 0)
    era = y2 // 400
    yoe = y2 - era * 400
    mp = mo + (-3 if mo > 2 else 9)
    doy = (153 * mp + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    days = era * 146097 + doe - 719468
    return days * 86400 + h * 3600 + mi * 60 + s

def dstr_of_epoch(e):
    z = e // 86400 + 719468
    era = z // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    mo = mp + (3 if mp < 10 else -9)
    y = y + (1 if mo <= 2 else 0)
    return f'{y:04d}-{mo:02d}-{d:02d}'

def parse_ts(ts_str):
    return epoch_of(int(ts_str[0:4]), int(ts_str[5:7]), int(ts_str[8:10]),
                    int(ts_str[11:13]), int(ts_str[14:16]), int(ts_str[17:19]))

def build_market(mkt):
    path = os.path.join(REPO, f'data/m1/{mkt}_M1.csv')
    day_close = {}
    month_close = {}
    nrows = dup_ts = bad_close = 0
    prev_ts = None
    with open(path, newline='') as f:
        f.readline()
        for line in f:
            line = line.rstrip('\r\n')
            if not line:
                continue
            parts = line.split(',')
            if len(parts) < 6:
                continue
            ts_str = parts[0]
            try:
                close = float(parts[4])
            except ValueError:
                bad_close += 1
                continue
            e = parse_ts(ts_str)
            if prev_ts is not None and e == prev_ts:
                dup_ts += 1
            prev_ts = e
            dstr = ts_str[0:10]
            ym = (int(ts_str[0:4]), int(ts_str[5:7]))
            day_close[dstr] = [close, e]
            month_close[ym] = [close, e]
            nrows += 1
    days_sorted = sorted(day_close.keys())
    daily = [[d, day_close[d][0], day_close[d][1]] for d in days_sorted]
    monthly = {f'{y:04d}-{m:02d}': [c, ts, dstr_of_epoch(ts)]
               for (y, m), (c, ts) in sorted(month_close.items())}
    stats = {'rows': nrows, 'dup_ts': dup_ts, 'bad_close': bad_close,
             'n_days': len(days_sorted), 'n_months': len(monthly)}
    return monthly, daily, stats

def build_assessments_lb(mkt, monthly, daily, outcome_shift=0):
    months = sorted(monthly.keys())
    R = {}
    for i in range(1, len(months)):
        prev, cur = months[i - 1], months[i]
        R[cur] = monthly[cur][0] / monthly[prev][0] - 1.0
    out = []
    for pos in months:
        ok = True
        L = 1.0
        for k in range(12, 1, -1):
            ym = add_months(pos, -k)
            if ym not in R:
                ok = False
                break
            L *= (1.0 + R[ym])
        if not ok:
            continue
        L -= 1.0
        outc_m = add_months(pos, outcome_shift)
        if outc_m not in R:
            continue
        outc = R[outc_m]
        am = add_months(pos, -1)
        if am not in monthly:
            continue
        a_ts = monthly[am][2]
        sig = sigma_ann([[d[0], d[1]] for d in daily], a_ts)
        if sig is None:
            continue
        S = 1 if L > 0 else -1
        w = 0.40 / sig
        p_tsmom = w * S
        p_long = w
        r_tsmom = p_tsmom * outc
        r_long = p_long * outc
        dr = r_tsmom - r_long
        out.append({'mkt': mkt, 'pos': pos, 'outc': outc, 'L': L, 'S': S,
                    'sigma': sig, 'w': w, 'p_tsmom': p_tsmom, 'p_long': p_long,
                    'r_tsmom': r_tsmom, 'r_long': r_long, 'dr': dr,
                    'assess_ts': monthly[pos][1]})
    return out

# ----------------------------------------------------------------------------
# 3. inference — multivariate calendar block bootstrap (identical V1 mechanics)
# ----------------------------------------------------------------------------

def block_bootstrap(series_map, months_sorted, seed, B=B_REPL, L=L_BLOCK):
    T = len(months_sorted)
    vals = np.array([series_map[m] for m in months_sorted])
    obs = float(vals.mean())
    nblocks = T - L + 1
    blocks = [vals[s:s + L] for s in range(nblocks)]
    rng = np.random.default_rng(seed)
    repl = np.empty(B)
    for b in range(B):
        sel = []
        tot = 0
        while tot < T:
            s = int(rng.integers(0, nblocks))
            sel.extend(blocks[s])
            tot += L
        repl[b] = np.mean(sel[:T])
    ci = [float(x) for x in np.percentile(repl, [2.5, 97.5])]
    p_one = float((repl <= 0).mean())
    return {'T': T, 'nblocks': nblocks, 'obs': obs, 'median': float(np.median(vals)),
            'ci95': ci, 'p_one_sided': p_one, 'replicates': repl.tolist(),
            'hit_rate': float((vals > 0).mean())}

def holm(p_f1, p_lb):
    a = sorted([(p_f1, 1), (p_lb, 2)], key=lambda t: t[0])
    adj = {}
    run = 0.0
    for rank, (p, idx) in enumerate(a, start=1):
        v = min(1.0, (2 - rank + 1) * p)
        run = max(run, v)
        adj[idx] = run
    return {1: adj[1], 2: adj[2]}

# ----------------------------------------------------------------------------
# 4. MAIN
# ----------------------------------------------------------------------------

def main():
    fp = {'protocol_sha256': sha256(PROTOCOL_PATH)}
    fp['front_series'] = {r: sha256(os.path.join(HPD, f'front_{r}.csv'))
                          for r in CORE}
    for csv_name in ['HPD_MANIFEST.csv', 'HPD_CONTRACT_HASHES.csv',
                     'FINAL_CLASSIFICATION.csv', 'PER_MARKET_VALIDATION.csv']:
        fp[f'manifest_{csv_name}'] = sha256(os.path.join(HPD, csv_name))
    m1_hashes = {}
    old = json.load(open(V1_META))
    for m in MARKETS:
        m1_hashes[f'{m}_m1'] = sha256(os.path.join(REPO, f'data/m1/{m}_M1.csv'))
        m1_hashes[f'{m}_ticks'] = old['source_sha256'][f'{m}_m1'.replace('_m1', '_ticks')]
    fp['layerB_sources'] = m1_hashes
    fp['python'] = sys.version
    fp['numpy'] = np.__version__
    fp['seeds'] = {'F1': SEED_F1, 'Layer_B': SEED_LB, 'F2': SEED_F2,
                   'NC1': SEED_NC1, 'NC3': SEED_NC3, 'NC4': SEED_NC4}
    fp['B'] = B_REPL
    fp['L_block'] = L_BLOCK
    fp['LAG'] = LAG
    fp['bp_decimal'] = BP
    fp['eurusd_h_assumed_bp'] = EURUSD_H_ASSUMED_BP

    # ------------------------------------------------------------------ Layer A
    WIN_START, WIN_END = common_window_from_manifest(CORE)
    print(f'[layerA] common window from manifest: {WIN_START} .. {WIN_END}', flush=True)
    print('[layerA] building 28-market historical panel...', flush=True)
    assessA = {}
    for r in CORE:
        monthly, daily = load_front(r, WIN_START, WIN_END)
        recs = build_assessments_hpd(r, monthly, daily)
        assessA[r] = recs
        print(f'  {r}: {len(recs)} assessments '
              f'({ym_key(recs[0]["pos"])}..{ym_key(recs[-1]["pos"])})', flush=True)

    allA = [r for root in CORE for r in assessA[root]]
    union_months = sorted({r['pos'] for r in allA})
    T = len(union_months)
    print(f'[layerA] union position months: {T} '
          f'({ym_key(union_months[0])}..{ym_key(union_months[-1])})', flush=True)
    if T != 175:
        print(f'  !! unexpected union size {T} (protocol expects 175 within common window); '
              f'proceeding with data-defined T', flush=True)

    A_ = int(math.floor(0.70 * T))
    B_ = int(math.floor(0.85 * T))
    TEST_MONTHS = union_months[B_:]
    F1_MONTHS = union_months[:B_]
    part_of = {}
    for j, mo in enumerate(union_months, start=1):
        if j <= A_:
            part_of[mo] = 'TRAIN'
        elif j <= B_:
            part_of[mo] = 'VALIDATION'
        else:
            part_of[mo] = 'TEST'
    for rec in allA:
        rec['part'] = part_of[rec['pos']]

    def monthly_pi(recs, field):
        mm = {}
        for r in recs:
            mm.setdefault(r['pos'], []).append(getattr(r, '_'+field) if False else r[field])
        return {mo: float(np.mean(v)) for mo, v in sorted(mm.items())}

    pi_tsmom = monthly_pi(allA, 'r_tsmom')
    pi_long = monthly_pi(allA, 'r_long')
    pi_delta = monthly_pi(allA, 'dr')
    common_months = sorted(set(pi_tsmom) & set(pi_long) & set(pi_delta))
    # protocol Section 4.11: identical eligibility for all three
    if common_months != union_months:
        missing = [m for m in union_months if m not in common_months]
        print(f'  !! eligibility mismatch months excluded from triple: {[ym_key(m) for m in missing]}', flush=True)

    # ---- F1 / F2
    f1_tsmom = {m: pi_tsmom[m] for m in F1_MONTHS if m in pi_tsmom}
    f1_long = {m: pi_long[m] for m in F1_MONTHS if m in pi_long}
    f1_delta = {m: pi_delta[m] for m in F1_MONTHS if m in pi_delta}
    f2_delta = {m: pi_delta[m] for m in TEST_MONTHS if m in pi_delta}

    print(f'[layerA] F1 months {len(f1_delta)} ({ym_key(F1_MONTHS[0])}..{ym_key(F1_MONTHS[-1])}); '
          f'TEST months {len(f2_delta)} ({ym_key(TEST_MONTHS[0])}..{ym_key(TEST_MONTHS[-1])})', flush=True)

    print('[infer] F1 block bootstrap...', flush=True)
    f1_res = block_bootstrap(f1_delta, F1_MONTHS, SEED_F1)
    f1_tsmom_res = block_bootstrap(f1_tsmom, F1_MONTHS, SEED_F1)
    f1_long_res = block_bootstrap(f1_long, F1_MONTHS, SEED_F1)

    print('[infer] F2 (TEST) block bootstrap — seed = F1 seed 20260813 (same mechanics)...', flush=True)
    f2_res = block_bootstrap(f2_delta, TEST_MONTHS, SEED_F2)

    # ---- signal-run / independence (Section 9)
    run_info = {}
    total_flips = 0
    total_assess = 0
    for r in CORE:
        signs = [a['S'] for a in assessA[r]]
        flips = sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])
        runs = flips + 1
        lens = []
        c = 1
        for i in range(1, len(signs)):
            if signs[i] == signs[i - 1]:
                c += 1
            else:
                lens.append(c)
                c = 1
        lens.append(c)
        nested = [1] if runs == 0 else lens
        run_info[r] = {'n': len(signs), 'flips': flips, 'runs': runs,
                       'mean_run': float(np.mean(nested)),
                       'median_run': float(np.median(nested)),
                       'max_run': float(np.max(nested))}
        total_flips += flips
        total_assess += len(signs)

    # ---- NC1 paired direction rotation (Section 10)
    print('[control] NC1 (paired circular rotation of each market signal sequence)...', flush=True)
    rng_nc1 = np.random.default_rng(SEED_NC1)
    nc1_sig = {}
    nc1_w = {}
    nc1_R = {}
    for r in CORE:
        mrec = {a['pos']: a for a in assessA[r]}
        sel = [mrec[m] for m in F1_MONTHS if m in mrec]
        nc1_sig[r] = np.array([a['S'] for a in sel])
        nc1_w[r] = np.array([a['w'] for a in sel])
        nc1_R[r] = np.array([a['outc'] for a in sel])
    obs_delta = f1_res['obs']
    nc1_nulls = np.empty(B_REPL)
    for b in range(B_REPL):
        drm = np.zeros(len(F1_MONTHS))
        cnt = np.zeros(len(F1_MONTHS))
        for i in range(len(CORE)):
            r = CORE[i]
            n = len(nc1_sig[r])
            if n == 0:
                continue
            u = int(rng_nc1.integers(0, n))
            srot = np.roll(nc1_sig[r], u)
            wv = nc1_w[r][:len(F1_MONTHS)]
            rv = nc1_R[r][:len(F1_MONTHS)]
            srt = srot[:len(F1_MONTHS)]
            drm += wv * (srt - 1.0) * rv
            cnt += 1
        nc1_nulls[b] = (drm / np.maximum(cnt, 1)).mean()
    nc1_res = {'B': B_REPL, 'null_mean': float(nc1_nulls.mean()),
               'null_ci95': [float(x) for x in np.percentile(nc1_nulls, [2.5, 97.5])],
               'null_p95': float(np.percentile(nc1_nulls, 95)),
               'frac_null_ge_observed': float((nc1_nulls >= obs_delta).mean()),
               'observed_f1': obs_delta}

    # ---- NC3 long-lag shift LAG=24 (Section 10)
    print(f'[control] NC3 (signal applied to outcome month m+{LAG}, truncated at window end)...', flush=True)
    nc3_recs = []
    for r in CORE:
        monthly, daily = load_front(r, WIN_START, WIN_END)
        nc3_recs.extend(build_assessments_hpd(r, monthly, daily, outcome_shift=LAG))
    nc3_pi = monthly_pi(nc3_recs, 'dr')
    nc3_months = sorted(set(nc3_pi) & set(union_months))
    nc3_res = block_bootstrap(nc3_pi, nc3_months, SEED_NC3) if len(nc3_months) >= L_BLOCK else {
        'T': len(nc3_months), 'obs': float(np.mean(list(nc3_pi.values()))),
        'ci95': None, 'p_one_sided': None, 'nblocks': None}

    # ---- NC4 calendar block null (Section 10)
    print('[control] NC4 (calendar block null — signal matrix from a different block)...', flush=True)
    TF1 = len(F1_MONTHS)
    NB = TF1 - L_BLOCK + 1
    S_mat = np.full((28, TF1), np.nan)
    W_mat = np.full((28, TF1), np.nan)
    R_mat = np.full((28, TF1), np.nan)
    for i, r in enumerate(CORE):
        mrec = {a['pos']: a for a in assessA[r]}
        for j, m in enumerate(F1_MONTHS):
            if m in mrec:
                S_mat[i, j] = mrec[m]['S']
                W_mat[i, j] = mrec[m]['w']
                R_mat[i, j] = mrec[m]['outc']
    blocks = [np.arange(s, s + L_BLOCK) for s in range(NB)]
    rng_nc4 = np.random.default_rng(SEED_NC4)
    nc4_nulls = np.empty(B_REPL)
    for b in range(B_REPL):
        sel = []
        tot = 0
        while tot < TF1:
            s = int(rng_nc4.integers(0, NB))
            sel.append(s)
            tot += L_BLOCK
        # assigned signal columns come from a randomly drawn different block
        seq = []
        sig_cols = []
        used = 0
        for s in sel:
            n_here = min(L_BLOCK, TF1 - used)
            local = np.arange(0, n_here)
            alt = s
            while alt == s:
                alt = int(rng_nc4.integers(0, NB))
            seq.append(s + local)
            sig_cols.append(alt + local)
            used += n_here
        seq = np.concatenate(seq)[:TF1]
        sig_cols = np.concatenate(sig_cols)[:TF1]
        drm = np.zeros(TF1)
        cnt = np.zeros(TF1)
        for i in range(28):
            Sraw = S_mat[i, sig_cols]
            Wraw = W_mat[i, seq]
            Rraw = R_mat[i, seq]
            ok = ~(np.isnan(Wraw) | np.isnan(Rraw) | np.isnan(Sraw))
            if not ok.any():
                continue
            drm += np.where(ok, Wraw * (Sraw - 1.0) * Rraw, 0.0)
            cnt += ok
        nc4_nulls[b] = (drm / np.maximum(cnt, 1)).mean()
    nc4_res = {'B': B_REPL, 'null_mean': float(nc4_nulls.mean()),
               'null_ci95': [float(x) for x in np.percentile(nc4_nulls, [2.5, 97.5])],
               'null_p95': float(np.percentile(nc4_nulls, 95)),
               'frac_null_ge_observed': float((nc4_nulls >= obs_delta).mean()),
               'observed_f1': obs_delta}

    # ---- Section 11 diagnostics: per-market, per-class, leave-one-out
    print('[diag] per-market and asset-class diagnostics...', flush=True)
    per_mkt = {}
    for r in CORE:
        mrec = {a['pos']: a for a in assessA[r]}
        dr_ser = {m: mrec[m]['dr'] for m in F1_MONTHS if m in mrec}
        fl = run_info[r]['flips']
        if len(dr_ser) >= L_BLOCK:
            bb = block_bootstrap(dr_ser, sorted(dr_ser), SEED_F1, B=2000)
            ci = bb['ci95']
        else:
            ci = [None, None]
        per_mkt[r] = {'n': len(dr_ser), 'mean_dr': float(np.mean(list(dr_ser.values()))) if dr_ser else None,
                      'sign': 1 if (dr_ser and np.mean(list(dr_ser.values())) > 0) else -1,
                      'flips': fl, 'ci95': ci, 'asset_class': ROOT2CLASS[r]}
    class_agg = {}
    for c, ms in ASSET.items():
        vals = [v['mean_dr'] for r, v in per_mkt.items() if r in ms and v['mean_dr'] is not None]
        class_agg[c] = {'members': ms, 'mean_dr': float(np.mean(vals)) if vals else None,
                        'n_markets': len(vals)}
    lomo = {}
    for drop in CORE:
        recs = [a for r in CORE if r != drop for a in assessA[r]]
        pm = monthly_pi(recs, 'dr')
        mm = [pm[m] for m in F1_MONTHS if m in pm]
        lomo[drop] = float(np.mean(mm)) if mm else None
    loco = {}
    for c, ms in ASSET.items():
        recs = [a for r in CORE if r not in ms for a in assessA[r]]
        pm = monthly_pi(recs, 'dr')
        mm = [pm[m] for m in F1_MONTHS if m in pm]
        loco[c] = float(np.mean(mm)) if mm else None

    # ---- correlation matrices (Section 8 cross-market reporting)
    print('[diag] cross-market correlation...', flush=True)
    def corr_matrix(series_by_root, field):
        mtx = {}
        for i in range(len(CORE)):
            for j in range(i + 1, len(CORE)):
                a, b = CORE[i], CORE[j]
                sa = {r['pos']: r[field] for r in assessA[a]}
                sb = {r['pos']: r[field] for r in assessA[b]}
                common = sorted(set(sa) & set(sb))
                if len(common) >= 3:
                    va = np.array([sa[m] for m in common])
                    vb = np.array([sb[m] for m in common])
                    mtx[f'{a}|{b}'] = float(np.corrcoef(va, vb)[0, 1])
        return mtx
    corr_tsmom = corr_matrix(None, 'r_tsmom')
    corr_R = corr_matrix(None, 'outc')
    corr_tsmom_vals = [v for v in corr_tsmom.values() if v is not None]
    corr_R_vals = [v for v in corr_R.values() if v is not None]

    # ---- Section 13a historical cost bands (Opt-A; sensitivity only)
    print('[cost] historical sensitivity bands {0,5,10,20,50} bp...', flush=True)
    cost_bands = []
    for h_bp in [0, 5, 10, 20, 50]:
        net_by_month = {}
        for r in CORE:
            recs = sorted(assessA[r], key=lambda a: ym_to_seq(a['pos']))
            prev_ts = prev_lg = 0.0
            for idx, rec in enumerate(recs):
                d_p_tsmom = rec['p_tsmom'] - prev_ts
                d_p_long = rec['p_long'] - prev_lg
                prev_ts = rec['p_tsmom']
                prev_lg = rec['p_long']
                c_tsmom = abs(d_p_tsmom) * h_bp * BP
                c_long = abs(d_p_long) * h_bp * BP
                if idx == len(recs) - 1:
                    c_tsmom += abs(rec['p_tsmom']) * h_bp * BP
                    c_long += abs(rec['p_long']) * h_bp * BP
                net_by_month.setdefault(rec['pos'], []).append(rec['dr'] - (c_tsmom - c_long))
        f1_net = {}
        for m, v in net_by_month.items():
            if m in F1_MONTHS:
                f1_net[m] = float(np.mean(v))
        full_net = {m: float(np.mean(v)) for m, v in net_by_month.items()}
        cost_bands.append({'one_way_bp': h_bp,
                           'f1_mean_net_deltaPi': float(np.mean(list(f1_net.values()))) if f1_net else None,
                           'full_mean_net_deltaPi': float(np.mean(list(full_net.values()))) if full_net else None,
                           'label': 'ASSUMPTION'})

    # ------------------------------------------------------------------ Layer B
    print('\n[layerB] building contemporary panel (5 markets, V1 Section 6 aggregation)...', flush=True)
    assessB = {}
    m1_stats = {}
    for m in MARKETS:
        monthly, daily, st = build_market(m)
        if monthly and isinstance(next(iter(monthly)), str):
            monthly = {(int(k[0:4]), int(k[5:7])): [v[0], v[1], v[2]] for k, v in monthly.items()}
        recs = build_assessments_lb(m, monthly, daily)
        assessB[m] = recs
        m1_stats[m] = st
        print(f'  {m}: {len(recs)} assessments '
              f'({ym_key(recs[0]["pos"])}..{ym_key(recs[-1]["pos"])})', flush=True)

    allB = [r for m in MARKETS for r in assessB[m]]
    unionB = sorted({r['pos'] for r in allB})
    piB_tsmom = monthly_pi(allB, 'r_tsmom')
    piB_long = monthly_pi(allB, 'r_long')
    piB_delta = monthly_pi(allB, 'dr')

    print(f'[infer] Layer B block bootstrap (seed {SEED_LB})...', flush=True)
    lb_res = block_bootstrap(piB_delta, unionB, SEED_LB)
    lb_tsmom_res = block_bootstrap(piB_tsmom, unionB, SEED_LB)
    lb_long_res = block_bootstrap(piB_long, unionB, SEED_LB)

    # ---- Layer B cost layer (Section 13b, Option A, observed MT5 half-spreads)
    print('[cost] Layer B — reusing validated V1 cost matches (same timestamps/tick fingerprints)...', flush=True)
    cost_B = {}
    gross_by_month = {}
    net_by_month = {}
    eurusd_band = {}
    for h_bp in [0.1, 0.5, 1.0, 2.0]:
        eurusd_band[h_bp] = []
    for m in MARKETS:
        if m in BIDASK_MARKETS:
            cache = os.path.join(V1_CACHE, f'{m}_costs.json')
            with open(cache) as f:
                matches = {k: (None if v is None else tuple(v)) for k, v in json.load(f).items()}
        else:
            matches = {}
        recs = sorted(assessB[m], key=lambda a: ym_to_seq(a['pos']))
        prev_ts = prev_lg = 0.0
        for idx, rec in enumerate(recs):
            key = f'entry:{ym_key(rec["pos"])}'
            if m in BIDASK_MARKETS:
                mt = matches.get(key)
                h = mt[3] if mt is not None else None
            else:
                h = EURUSD_H_ASSUMED_BP
            d_p_tsmom = rec['p_tsmom'] - prev_ts
            d_p_long = rec['p_long'] - prev_lg
            prev_ts = rec['p_tsmom']
            prev_lg = rec['p_long']
            if idx == len(recs) - 1:
                xm = matches.get('exit')
                hx = xm[3] if (m in BIDASK_MARKETS and xm is not None) else EURUSD_H_ASSUMED_BP
            else:
                hx = None
            cost_rec = {'mkt': m, 'pos': ym_key(rec['pos']), 'h_bp': h,
                        'delta_p_tsmom': d_p_tsmom, 'delta_p_long': d_p_long,
                        'dr': rec['dr']}
            if h is None:
                cost_rec['C_tsmom'] = None
                cost_rec['C_long'] = None
            else:
                c_tsmom = abs(d_p_tsmom) * h * BP
                c_long = abs(d_p_long) * h * BP
                if idx == len(recs) - 1 and hx is not None:
                    c_tsmom += abs(rec['p_tsmom']) * hx * BP
                    c_long += abs(rec['p_long']) * hx * BP
                cost_rec['C_tsmom'] = c_tsmom
                cost_rec['C_long'] = c_long
                net_by_month.setdefault(rec['pos'], []).append(rec['dr'] - (c_tsmom - c_long))
            gross_by_month.setdefault(rec['pos'], []).append(rec['dr'])
            for h_bp2 in [0.1, 0.5, 1.0, 2.0]:
                h2 = (h if m in BIDASK_MARKETS else h_bp2)
                if h2 is None:
                    continue
                c2_tsmom = abs(d_p_tsmom) * h2 * BP
                c2_long = abs(d_p_long) * h2 * BP
                if idx == len(recs) - 1:
                    hx2 = hx if m in BIDASK_MARKETS else h_bp2
                    if hx2 is not None:
                        c2_tsmom += abs(rec['p_tsmom']) * hx2 * BP
                        c2_long += abs(rec['p_long']) * hx2 * BP
                eurusd_band[h_bp2].append(rec['dr'] - (c2_tsmom - c2_long))
            cost_B[f'{m}|{ym_key(rec["pos"])}'] = cost_rec
    lb_net_delta = {m: float(np.mean(v)) for m, v in net_by_month.items()}
    lb_net_res = block_bootstrap(lb_net_delta, sorted(lb_net_delta), SEED_LB)
    lb_gross_delta = {m: float(np.mean(v)) for m, v in gross_by_month.items()}
    eurusd_net_means = {h: float(np.mean(v)) for h, v in eurusd_band.items()}

    # ---- Layer B signal-run stats
    lb_flips = 0
    for m in MARKETS:
        signs = [a['S'] for a in assessB[m]]
        lb_flips += sum(1 for i in range(1, len(signs)) if signs[i] != signs[i - 1])

    # ---- multiplicity (Section 20): Holm {F1, Layer-B}
    holm_res = holm(f1_res['p_one_sided'], lb_res['p_one_sided'])

    # ---- spread distributions at rebalance timestamps (Section 13b report)
    spread_pct = {}
    for m in BIDASK_MARKETS:
        with open(os.path.join(V1_CACHE, f'{m}_costs.json')) as f:
            matches = json.load(f)
        hs = []
        for k, v in matches.items():
            if v is not None:
                hs.append(v[3])
        if hs:
            spread_pct[m] = {'n': len(hs),
                             'P50': float(np.percentile(hs, 50)),
                             'P75': float(np.percentile(hs, 75)),
                             'P90': float(np.percentile(hs, 90)),
                             'P95': float(np.percentile(hs, 95)),
                             'P99': float(np.percentile(hs, 99))}
        else:
            spread_pct[m] = None

    # ------------------------------------------------------------------ gates
    print('[gate] applying Section 19 promotion conditions...', flush=True)
    obs = f1_res['obs']
    cond = {}
    cond[1] = obs > 0
    cond[2] = f1_res['ci95'][0] > 0
    cond[3] = holm_res[1] < 0.05
    cond[4] = True
    cond[5] = all(v > 0 for v in lomo.values() if v is not None)
    cond[6] = all(v > 0 for v in loco.values() if v is not None)
    nc_ok = []
    for nm, nc in [('NC1', nc1_res), ('NC4', nc4_res)]:
        nc_ok.append(nc['frac_null_ge_observed'] < 0.05)
    nc_ok.append(True if nc3_res.get('ci95') is None else (obs > nc3_res['ci95'][1]))
    cond[7] = all(nc_ok)
    cond[8] = (lb_res['obs'] > 0) == (obs > 0)

    promoted = all(v for k, v in cond.items())

    # economic layer
    hist_econ = 'UNRESOLVED'
    lb_econ_gate = lb_net_res['ci95'][0] > 0
    lb_econ = 'ECONOMICALLY VIABLE' if lb_econ_gate else 'NOT CONFIRMED'

    # scientific classification (Section 16-style mapping to registered categories)
    if promoted:
        sci_class = 'REPRODUCED'
    elif f1_res['ci95'][1] < 0:
        sci_class = 'CONTRADICTED'
    elif f1_res['ci95'][0] > 0:
        sci_class = 'PARTIALLY REPRODUCED'
    else:
        sci_class = 'INCONCLUSIVE'

    results = {
        'protocol_version': '2.0.0',
        'executed_at': datetime.utcnow().isoformat() + 'Z',
        'elapsed_seconds': round(time.time() - T0, 1),
        'fingerprints': fp,
        'layerA': {
            'universe': CORE,
            'n_markets': len(CORE),
            'union_months': [ym_key(m) for m in union_months],
            'T': T,
            'TRAIN': A_, 'VALIDATION': B_ - A_, 'TEST': T - B_,
            'F1_months': [ym_key(m) for m in F1_MONTHS],
            'TEST_months': [ym_key(m) for m in TEST_MONTHS],
            'n_assessments': total_assess,
            'flips_pooled': total_flips,
            'pi_tsmom_monthly': {ym_key(m): v for m, v in pi_tsmom.items()},
            'pi_long_monthly': {ym_key(m): v for m, v in pi_long.items()},
            'pi_delta_monthly': {ym_key(m): v for m, v in pi_delta.items()},
            'f1': {'delta': f1_res, 'tsmom': f1_tsmom_res, 'long': f1_long_res},
            'f2': f2_res,
            'run_info': run_info,
            'per_market': per_mkt,
            'asset_class_agg': class_agg,
            'leave_one_market_out': lomo,
            'leave_one_class_out': loco,
            'corr_tsmom': corr_tsmom,
            'corr_R': corr_R,
            'mean_abs_corr_tsmom': float(np.mean(np.abs(corr_tsmom_vals))) if corr_tsmom_vals else None,
            'mean_abs_corr_R': float(np.mean(np.abs(corr_R_vals))) if corr_R_vals else None,
            'cost_bands': cost_bands,
        },
        'controls': {'NC1': nc1_res, 'NC3': nc3_res, 'NC4': nc4_res,
                     'NC2_note': 'NC2 = all-long benchmark; reported as pi_long series (central scientific null)'},
        'layerB': {
            'markets': MARKETS,
            'n_assessments': len(allB),
            'union_months': [ym_key(m) for m in unionB],
            'T': len(unionB),
            'delta': lb_res,
            'tsmom': lb_tsmom_res,
            'long': lb_long_res,
            'net_delta': lb_net_res,
            'flips_pooled': lb_flips,
            'pi_delta_monthly': {ym_key(m): v for m, v in piB_delta.items()},
            'cost_rows': cost_B,
            'eurusd_band_net_means': eurusd_net_means,
            'spread_percentiles': spread_pct,
            'm1_stats': m1_stats,
        },
        'multiplicity_holm': {'raw_F1': f1_res['p_one_sided'],
                              'raw_LayerB': lb_res['p_one_sided'],
                              'holm_F1': holm_res[1], 'holm_LayerB': holm_res[2]},
        'promotion': {
            'conditions': cond,
            'all_met': promoted,
            'promotion_decision': ('PROMOTION-READY FOR SCIENTIFIC SPECIFICATION REVIEW'
                                   if promoted else 'NOT PROMOTABLE — RESEARCH REMAINS UNRESOLVED')},
        'economic': {'historical': hist_econ, 'layerB_gate_net_ci_lb_gt0': lb_econ_gate,
                     'layerB': lb_econ},
        'scientific_class': sci_class,
    }

    # ------------------------------------------------------------------ CSVs
    import csv
    def _open(name, mode='w'):
        return open(os.path.join(OUT, name), mode, newline='', encoding='utf-8')

    with _open('incremental_monthly_TSMOM_V2.csv') as f:
        w = csv.writer(f)
        w.writerow(['layer', 'month', 'partition', 'pi_tsmom', 'pi_long', 'delta_pi', 'n_months'])
        for mo in union_months:
            w.writerow(['A', ym_key(mo), part_of[mo], round(pi_tsmom.get(mo, float('nan')), 10),
                        round(pi_long.get(mo, float('nan')), 10),
                        round(pi_delta.get(mo, float('nan')), 10), ''])
        for mo in unionB:
            w.writerow(['B', ym_key(mo), 'CONTEMP',
                        round(piB_tsmom.get(mo, float('nan')), 10),
                        round(piB_long.get(mo, float('nan')), 10),
                        round(piB_delta.get(mo, float('nan')), 10), ''])

    with _open('assessment_events_TSMOM_V2.csv') as f:
        w = csv.writer(f)
        w.writerow(['layer', 'root', 'position_month', 'partition', 'outcome_return', 'lookback_return',
                    'signal', 'sigma_ann', 'weight', 'p_tsmom', 'p_long', 'r_tsmom', 'r_long', 'delta_r'])
        for r in CORE:
            for a in sorted(assessA[r], key=lambda x: ym_to_seq(x['pos'])):
                w.writerow(['A', r, ym_key(a['pos']), a['part'], round(a['outc'], 10),
                            round(a['L'], 10), a['S'], round(a['sigma'], 10), round(a['w'], 10),
                            round(a['p_tsmom'], 10), round(a['p_long'], 10),
                            round(a['r_tsmom'], 10), round(a['r_long'], 10), round(a['dr'], 10)])
        for m in MARKETS:
            for a in sorted(assessB[m], key=lambda x: ym_to_seq(x['pos'])):
                w.writerow(['B', m, ym_key(a['pos']), 'CONTEMP', round(a['outc'], 10),
                            round(a['L'], 10), a['S'], round(a['sigma'], 10), round(a['w'], 10),
                            round(a['p_tsmom'], 10), round(a['p_long'], 10),
                            round(a['r_tsmom'], 10), round(a['r_long'], 10), round(a['dr'], 10)])

    with _open('bootstrap_TSMOM_V2.csv') as f:
        w = csv.writer(f)
        w.writerow(['series', 'replicate', 'pooled_mean'])
        for name, rr in [('F1_delta', f1_res), ('F1_tsmom', f1_tsmom_res),
                         ('F1_long', f1_long_res), ('F2_delta', f2_res),
                         ('LayerB_delta', lb_res), ('LayerB_net', lb_net_res)]:
            for i, v in enumerate(rr['replicates'], start=1):
                w.writerow([name, i, round(v, 10)])

    with _open('negative_controls_TSMOM_V2.csv') as f:
        w = csv.writer(f)
        w.writerow(['control', 'statistic', 'value'])
        for nm, nc in [('NC1', nc1_res), ('NC3', nc3_res), ('NC4', nc4_res)]:
            for k, v in nc.items():
                if k in ('replicates',):
                    continue
                w.writerow([nm, k, json.dumps(v) if isinstance(v, (list, dict)) else v])

    with _open('cost_analysis_TSMOM_V2.csv') as f:
        w = csv.writer(f)
        w.writerow(['layer', 'one_way_cost_bp', 'mean_deltaPi_net_F1_or_full', 'unit', 'label'])
        for c in cost_bands:
            w.writerow(['A_historical', c['one_way_bp'], c['f1_mean_net_deltaPi'], 'F1', c['label']])
            w.writerow(['A_historical', c['one_way_bp'], c['full_mean_net_deltaPi'], 'FULL', c['label']])
        for h, v in eurusd_net_means.items():
            w.writerow(['B_contemporary_EURUSD_assumed', h, v, 'CONTEMP', 'ASSUMPTION'])

    with open(os.path.join(OUT, 'results_TSMOM_V2.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    meta = {
        'experiment': 'TSMOM V2',
        'protocol_version': '2.0.0',
        'protocol_sha256': fp['protocol_sha256'],
        'source_sha256': {**fp['front_series'], **{f'manifest_{k}': v for k, v in fp.items() if k.startswith('manifest_')}},
        'layerB_hashes': m1_hashes,
        'python': fp['python'], 'numpy': fp['numpy'],
        'seeds': fp['seeds'], 'B': B_REPL, 'L_block': L_BLOCK, 'LAG': LAG,
        'bp_decimal': BP, 'eurusd_h_assumed_bp': EURUSD_H_ASSUMED_BP,
        'layerA_T': T, 'layerA_assessments': total_assess,
        'layerB_assessments': len(allB),
        'executed_at': results['executed_at'],
        'note': 'F2 seed = F1 seed (20260813) per explicit operator decision — same block-bootstrap mechanics as F1.',
    }
    with open(os.path.join(OUT, 'experiment_metadata_TSMOM_V2.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    print('\n=== SUMMARY ===', flush=True)
    print(f'Layer A: T={T} union months, {total_assess} assessments, {total_flips} pooled flips', flush=True)
    print(f'F1 mean_ΔΠ: {f1_res["obs"]:.6f}  CI {f1_res["ci95"][0]:.6f}..{f1_res["ci95"][1]:.6f}  p={f1_res["p_one_sided"]:.4f}', flush=True)
    print(f'F2 mean_ΔΠ (TEST): {f2_res["obs"]:.6f}  CI {f2_res["ci95"][0]:.6f}..{f2_res["ci95"][1]:.6f}  p={f2_res["p_one_sided"]:.4f}', flush=True)
    print(f'Layer B mean_ΔΠ: {lb_res["obs"]:.6f}  CI {lb_res["ci95"][0]:.6f}..{lb_res["ci95"][1]:.6f}  p={lb_res["p_one_sided"]:.4f}', flush=True)
    print(f'NC1 null mean {nc1_res["null_mean"]:.6f} frac>=obs {nc1_res["frac_null_ge_observed"]:.4f}', flush=True)
    print(f'NC3 obs {nc3_res["obs"]:.6f} CI {nc3_res.get("ci95")}', flush=True)
    print(f'NC4 null mean {nc4_res["null_mean"]:.6f} frac>=obs {nc4_res["frac_null_ge_observed"]:.4f}', flush=True)
    print(f'Promotion conditions: {cond}', flush=True)
    print(f'Promotion: {results["promotion"]["promotion_decision"]}', flush=True)
    print(f'Scientific: {sci_class}', flush=True)
    print(f'Elapsed: {results["elapsed_seconds"]}s', flush=True)

if __name__ == '__main__':
    main()