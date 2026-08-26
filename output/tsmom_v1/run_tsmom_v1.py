#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUANTFORGE — TSMOM V1 CONTROLLED EXPERIMENT EXECUTION
Protocol: output/tsmom_v1/EVENT_STUDY_PROTOCOL_TSMOM_V1.md (v1.0.3, FROZEN)
Executes the pre-registered specification exactly; no tuning, no cell selection.
Artifacts written under output/tsmom_v1/ (never overwriting the protocol).
"""
import hashlib, json, math, os, subprocess, sys, time
from datetime import datetime

import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(OUT, '.build_cache')
os.makedirs(CACHE, exist_ok=True)

MARKETS = ['XAUUSD', 'EURUSD', 'BTCUSD', 'XAGUSD', 'USATECHIDXUSD']
BIDASK_MARKETS = ['XAUUSD', 'BTCUSD', 'XAGUSD', 'USATECHIDXUSD']
SEED_F1 = 20260812
SEED_NC1 = 20260813
B_REPL = 10000
L_BLOCK = 12
BP = 0.0001                 # 1 bp in decimal
EURUSD_H_ASSUMED_BP = 0.1   # registered assumption, per side
PROTOCOL_PATH = os.path.join(OUT, 'EVENT_STUDY_PROTOCOL_TSMOM_V1.md')
T0 = time.time()

# ----------------------------------------------------------------------------
# 1. Utils / fingerprints
# ----------------------------------------------------------------------------

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def epoch_of(y, mo, d, h, mi, s):
    y2 = y - (1 if mo <= 2 else 0)
    era = y2 // 400
    yoe = y2 - era * 400
    mp = mo + (-3 if mo > 2 else 9)
    doy = (153 * mp + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    days = era * 146097 + doe - 719468
    return days * 86400 + h * 3600 + mi * 60 + s

def epoch_to_ymd(e):
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
    return y, mo, d

def parse_ts(ts_str):
    return epoch_of(int(ts_str[0:4]), int(ts_str[5:7]), int(ts_str[8:10]),
                    int(ts_str[11:13]), int(ts_str[14:16]), int(ts_str[17:19]))

def dstr_of_epoch(e):
    y, mo, d = epoch_to_ymd(e)
    return f'{y:04d}-{mo:02d}-{d:02d}'

def add_months(ym, k):
    y, mo = ym
    i = y * 12 + (mo - 1) + k
    return (i // 12, i % 12 + 1)

def ym_key(ym):
    return f'{ym[0]:04d}-{ym[1]:02d}'

# ----------------------------------------------------------------------------
# 2. M1 -> daily / monthly (deterministic aggregation, protocol Section 6)
# ----------------------------------------------------------------------------

def build_market(mkt):
    """Return dict with daily and monthly series for one market."""
    cache_m = os.path.join(CACHE, f'{mkt}_monthly.json')
    cache_d = os.path.join(CACHE, f'{mkt}_daily.json')
    cache_s = os.path.join(CACHE, f'{mkt}_stats.json')
    if os.path.exists(cache_m) and os.path.exists(cache_d):
        with open(cache_m) as f:
            monthly = {tuple(map(int, k.split('-'))): v for k, v in json.load(f).items()}
        with open(cache_d) as f:
            daily = json.load(f)
        if os.path.exists(cache_s):
            with open(cache_s) as f:
                stats = json.load(f)
        else:
            stats = {'cached': True}
        return monthly, daily, stats

    path = f'data/m1/{mkt}_M1.csv'
    day_close = {}    # 'YYYY-MM-DD' -> [close, ts]
    month_close = {}  # (y,mo) -> [close, ts]
    nrows = 0
    dup_ts = 0
    bad_close = 0
    first_ts = last_ts = None
    prev_ts = None
    with open(path, newline='') as f:
        header = f.readline()
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
            if first_ts is None:
                first_ts = e
            last_ts = e
    days_sorted = sorted(day_close.keys())
    daily = [[d, day_close[d][0], day_close[d][1]] for d in days_sorted]
    monthly = {f'{y:04d}-{m:02d}': [c, ts, dstr_of_epoch(ts)]
               for (y, m), (c, ts) in sorted(month_close.items())}
    stats = {'rows': nrows, 'dup_ts': dup_ts, 'bad_close': bad_close,
             'first_ts': first_ts, 'last_ts': last_ts, 'n_days': len(days_sorted),
             'n_months': len(monthly)}
    with open(cache_m, 'w') as f:
        json.dump(monthly, f)
    with open(cache_d, 'w') as f:
        json.dump(daily, f)
    with open(cache_s, 'w') as f:
        json.dump(stats, f)
    return monthly, daily, stats

def monthly_returns(monthly):
    months = sorted(monthly.keys())
    R = {}
    for i in range(1, len(months)):
        prev = months[i - 1]
        cur = months[i]
        R[cur] = monthly[cur][0] / monthly[prev][0] - 1.0
    return R

def sigma_ann(daily, end_dstr):
    """21 populated trading days ending at (inclusive) end_dstr; std(daily rets)*sqrt(252)."""
    days = [d[0] for d in daily]
    import bisect
    idx = bisect.bisect_right(days, end_dstr) - 1
    if idx < 0:
        return None
    lo = max(0, idx - 20)
    closes = [daily[i][1] for i in range(lo, idx + 1)]
    if len(closes) < 6:   # fewer than 5 daily returns
        return None
    rets = [closes[i] / closes[i - 1] - 1.0 for i in range(1, len(closes))]
    if len(rets) < 5:
        return None
    return float(np.std(rets, ddof=1) * math.sqrt(252))

# ----------------------------------------------------------------------------
# 3. Assessments (protocol Sections 5, 7, 8)
# ----------------------------------------------------------------------------

def build_assessments(mkt, monthly, daily, lookback=12, horizon=1, step=1,
                      wmode='invvol', hurdle=0.0, outcome_shift=0):
    """Generic assessment builder.
    lookback: number of lookback months (k = m-lookback .. m-2).
    horizon: outcome months m..m+horizon-1.
    step:    1 = every month (primary); >1 = non-overlapping blocks (E3).
    wmode:   'invvol' (primary) | 'flat' (E4) | 'capped' (E9).
    hurdle:  monthly hurdle subtracted inside lookback compounding (E6).
    outcome_shift: shift outcome month by +k (NC2).
    """
    months = sorted(monthly.keys())
    mset = set(months)
    R = monthly_returns(monthly)
    out = []
    first_pos = None
    for pos in months:
        if first_pos is None:
            first_pos = pos
        if (pos[0] * 12 + pos[1] - (first_pos[0] * 12 + first_pos[1])) % step != 0:
            continue
        # lookback months pos-lookback .. pos-2
        ok = True
        L = 1.0
        for k in range(lookback, 1, -1):
            ym = add_months(pos, -k)
            if ym not in R:
                ok = False
                break
            L *= (1.0 + R[ym] - hurdle)
        if not ok:
            continue
        L -= 1.0
        # outcome months pos .. pos+horizon-1 (+shift)
        out_months = []
        for h in range(horizon):
            ym = add_months(pos, h + outcome_shift)
            if ym not in R:
                out_months = None
                break
            out_months.append(ym)
        if out_months is None:
            continue
        outc = 1.0
        for ym in out_months:
            outc *= (1.0 + R[ym])
        outc -= 1.0
        # assessment month-end = end of month pos-1
        am = add_months(pos, -1)
        if am not in monthly:
            continue
        a_ts = monthly[am][2]  # date string of assessment month-end
        sig = sigma_ann(daily, a_ts)
        if sig is None:
            continue
        S = 1 if L > 0 else -1
        if wmode == 'invvol':
            w = 0.40 / sig
        elif wmode == 'flat':
            w = 1.0
        elif wmode == 'capped':
            w = min(0.40 / sig, 2.0)
        p = w * S
        r = p * outc
        out.append({'mkt': mkt, 'pos': pos, 'assess_end': am, 'R': outc,
                    'L': L, 'S': S, 'sigma': sig, 'w': w, 'p': p, 'r': r})
    return out

# ----------------------------------------------------------------------------
# 4. Cost layer (protocol Section 10, Option A v1.0.3)
# ----------------------------------------------------------------------------

def match_quotes(mkt, targets):
    """For each target epoch, nearest tick quote within ±600 s.
    targets: list of (label, epoch). Returns dict label -> best match dict.
    Uses a single grep pass streaming with O(1) memory."""
    cache = os.path.join(CACHE, f'{mkt}_costs.json')
    if os.path.exists(cache):
        with open(cache) as f:
            return {k: (None if v is None else tuple(v)) for k, v in json.load(f).items()}
    tgt = sorted([(e, lab) for lab, e in targets])
    dates8 = sorted({dstr_of_epoch(e).replace('-', '') for e, _ in tgt})
    regex = '^(' + '|'.join(dates8) + '),'
    best = {lab: None for _, lab in tgt}
    lo = 0
    n = len(tgt)
    p = subprocess.Popen(['grep', '-E', regex, f'data/tick/{mkt}_mt5_ticks.csv'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for raw in p.stdout:
        line = raw.decode('ascii', 'replace')
        try:
            bid = float(line.split(',')[2])
            ask = float(line.split(',')[3])
        except (IndexError, ValueError):
            continue
        e = epoch_of(int(line[0:4]), int(line[4:6]), int(line[6:8]),
                     int(line[9:11]), int(line[12:14]), int(line[15:17]))
        while lo < n and tgt[lo][0] + 600 < e:
            lo += 1
        j = lo
        while j < n and tgt[j][0] - 600 <= e:
            lab = tgt[j][1]
            diff = abs(e - tgt[j][0])
            if diff <= 600:
                cur = best[lab]
                if cur is None or diff < cur[0]:
                    best[lab] = (diff, bid, ask)
            j += 1
    p.wait()
    out = {}
    for lab, m in best.items():
        if m is None:
            out[lab] = None
        else:
            diff, bid, ask = m
            mid = (bid + ask) / 2.0
            half_bp = ((ask - bid) / 2.0 / mid) * 10000.0
            out[lab] = (diff, bid, ask, half_bp)
    with open(cache, 'w') as f:
        json.dump({k: (list(v) if v else None) for k, v in out.items()}, f)
    return out

# ----------------------------------------------------------------------------
# 5. Inference (protocol Section 11)
# ----------------------------------------------------------------------------

def block_bootstrap(pi_map, months_sorted, seed, B=B_REPL, L=L_BLOCK):
    T = len(months_sorted)
    vals = np.array([pi_map[m] for m in months_sorted])
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
    return {'T': T, 'nblocks': nblocks, 'obs': obs, 'ci95': ci,
            'p_one_sided': p_one, 'replicates': repl.tolist()}

def sign_flip(pi_vals):
    vals = np.array(pi_vals, dtype=float)
    n = len(vals)
    obs = float(vals.mean())
    cnt = 0
    total = 1 << n
    for mask in range(total):
        s = np.array([1.0 if (mask >> i) & 1 else -1.0 for i in range(n)])
        if float((s * vals).mean()) >= obs:
            cnt += 1
    return {'T': n, 'assignments': total, 'obs': obs, 'sign': 1 if obs > 0 else (-1 if obs < 0 else 0),
            'p_one_sided': cnt / total}

def holm(p1, p2):
    m = 2
    a = sorted([(p1, 1), (p2, 2)])
    adj = {}
    run = 0.0
    for rank, (p, idx) in enumerate(a):
        v = min(1.0, (m - rank) * p)
        run = max(run, v)
        adj[idx] = run
    return {1: adj[1], 2: adj[2]}

# ----------------------------------------------------------------------------
# 6. MAIN
# ----------------------------------------------------------------------------

def main():
    # --- fingerprints (cached; recomputed only when files change) ----------
    fp = {'protocol_sha256': sha256(PROTOCOL_PATH)}
    fp_cache = os.path.join(CACHE, 'fingerprints.json')
    srcs = {}
    if os.path.exists(fp_cache):
        with open(fp_cache) as f:
            prev = json.load(f)
    else:
        prev = {}
    for m in MARKETS:
        for kind, path in [(f'{m}_m1', f'data/m1/{m}_M1.csv'),
                           (f'{m}_ticks', f'data/tick/{m}_mt5_ticks.csv')]:
            prev_h = prev.get(kind)
            if prev_h is not None and prev_h.get('size') == os.path.getsize(path):
                srcs[kind] = prev_h
            else:
                srcs[kind] = {'path': path, 'sha256': sha256(path),
                              'size': os.path.getsize(path)}
                print(f'[hash] {path}', flush=True)
    with open(fp_cache, 'w') as f:
        json.dump(srcs, f, indent=2)
    fp['sources'] = srcs
    fp['python'] = sys.version
    fp['numpy'] = np.__version__
    fp['seed_f1'] = SEED_F1
    fp['seed_nc1'] = SEED_NC1
    fp['B'] = B_REPL
    fp['L_block'] = L_BLOCK
    fp['bp_decimal'] = BP
    fp['eurusd_h_assumed_bp'] = EURUSD_H_ASSUMED_BP

    # --- build markets -----------------------------------------------------
    mkt_data = {}
    m1_stats = {}
    daily_rows = []
    for m in MARKETS:
        monthly, daily, st = build_market(m)
        # monthly keys are already (y, mo) tuples on cache load; convert if strings
        if monthly and isinstance(next(iter(monthly)), str):
            monthly = {(int(k[0:4]), int(k[5:7])): v for k, v in monthly.items()}
        mkt_data[m] = (monthly, daily)
        m1_stats[m] = st
        for row in daily:
            daily_rows.append([m, row[0], row[1]])
        print(f'[build] {m}: {st}', flush=True)

    # --- assessments -------------------------------------------------------
    assess = {}   # mkt -> list of record dicts
    for m in MARKETS:
        monthly, daily = mkt_data[m]
        recs = build_assessments(m, monthly, daily, lookback=12, horizon=1, step=1,
                                 wmode='invvol', hurdle=0.0)
        assess[m] = recs
        print(f'[assess] {m}: {len(recs)} usable assessments '
              f'({recs[0]["pos"]}..{recs[-1]["pos"]})' if recs else f'[assess] {m}: 0', flush=True)

    # --- partitions (protocol Section 8) -----------------------------------
    for m in MARKETS:
        recs = assess[m]
        N = len(recs)
        A = int(math.floor(0.70 * N))
        B = int(math.floor(0.85 * N))
        for j, rec in enumerate(recs, start=1):
            rec['j'] = j
            rec['N'] = N
            if j <= A:
                rec['part'] = 'TRAIN'
            elif j <= B:
                rec['part'] = 'VALIDATION'
            else:
                rec['part'] = 'TEST'

    # --- cost layer --------------------------------------------------------
    print('[cost] matching quotes (single grep pass per bid/ask market)...', flush=True)
    cost_records = []
    spread_by_mkt = {}
    for m in MARKETS:
        recs = assess[m]
        if m in BIDASK_MARKETS:
            # entry target = last M1 bar of month m-1 (assessment month-end);
            # exit target = last M1 bar of the final position month N.
            targets = []
            for rec in recs:
                close_ts = mkt_data[m][0][rec['assess_end']][1]  # epoch of last M1 bar of month m-1
                targets.append((f'entry:{ym_key(rec["pos"])}', close_ts))
            last = recs[-1]
            exit_ts = mkt_data[m][0][last['pos']][1]
            targets.append(('exit', exit_ts))
            matches = match_quotes(m, targets)
            # assign to records
            hs = []
            unobs = 0
            for rec in recs:
                key = f'entry:{ym_key(rec["pos"])}'
                m0 = matches.get(key)
                if m0 is None:
                    rec['cost_status'] = 'UNOBSERVED'
                    rec['entry_half_bp'] = None
                    rec['entry_dist'] = None
                    unobs += 1
                else:
                    rec['cost_status'] = 'OK'
                    rec['entry_half_bp'] = m0[3]
                    rec['entry_dist'] = m0[0]
                    hs.append(m0[3])
            xm = matches.get('exit')
            if xm is not None:
                recs[-1]['exit_half_bp'] = xm[3]
                recs[-1]['exit_dist'] = xm[0]
                hs.append(xm[3])
            else:
                recs[-1]['exit_half_bp'] = None
            spread_by_mkt[m] = sorted(hs)
            print(f'[cost] {m}: {len(recs) - unobs}/{len(recs)} entry legs matched, '
                  f'{unobs} UNOBSERVED', flush=True)
        else:
            for rec in recs:
                rec['cost_status'] = 'OK'
                rec['entry_half_bp'] = EURUSD_H_ASSUMED_BP
                rec['entry_dist'] = 0
            recs[-1]['exit_half_bp'] = EURUSD_H_ASSUMED_BP
            spread_by_mkt[m] = None
            print(f'[cost] {m}: EURUSD spread ASSUMED {EURUSD_H_ASSUMED_BP} bp/side (UNOBSERVED)', flush=True)

    # --- position-change accounting & net contributions (Option A) ---------
    for m in MARKETS:
        recs = assess[m]
        prev_p = 0.0
        for rec in recs:
            rec['delta_p'] = rec['p'] - prev_p
            prev_p = rec['p']
            h = rec['entry_half_bp']
            if h is None:
                rec['C'] = None
                rec['net_contrib'] = None
            else:
                C = abs(rec['delta_p']) * h * BP
                rec['C'] = C
                rec['net_contrib'] = rec['r'] - C
        # final close
        last = recs[-1]
        hx = last.get('exit_half_bp')
        if hx is not None and last['C'] is not None:
            last['C'] += abs(last['p']) * hx * BP
            last['net_contrib'] = last['r'] - last['C']
            last['final_close_cost'] = abs(last['p']) * hx * BP

    # --- build pooled series ----------------------------------------------
    all_recs = [r for m in MARKETS for r in assess[m]]
    months_full = sorted({r['pos'] for r in all_recs})
    pi = {}
    pi_net = {}
    for mo in months_full:
        rs = [r for r in all_recs if r['pos'] == mo]
        pi[mo] = float(np.mean([r['r'] for r in rs]))
        nrs = [r for r in rs if r['net_contrib'] is not None]
        pi_net[mo] = float(np.mean([r['net_contrib'] for r in nrs])) if nrs else None

    # F1 / TEST windows
    f1_recs = [r for m in MARKETS for r in assess[m] if r['part'] != 'TEST']
    test_recs = [r for m in MARKETS for r in assess[m] if r['part'] == 'TEST']
    months_f1 = sorted({r['pos'] for r in f1_recs})
    months_test = sorted({r['pos'] for r in test_recs})
    pi_f1 = {}
    for mo in months_f1:
        rs = [r for r in f1_recs if r['pos'] == mo]
        pi_f1[mo] = float(np.mean([r['r'] for r in rs]))
    pi_net_f1 = {}
    for mo in months_f1:
        rs = [r for r in f1_recs if r['pos'] == mo and r['net_contrib'] is not None]
        if rs:
            pi_net_f1[mo] = float(np.mean([r['net_contrib'] for r in rs]))
    pi_test = {}
    for mo in months_test:
        rs = [r for r in test_recs if r['pos'] == mo]
        pi_test[mo] = float(np.mean([r['r'] for r in rs]))
    pi_net_test = {}
    for mo in months_test:
        rs = [r for r in test_recs if r['pos'] == mo and r['net_contrib'] is not None]
        if rs:
            pi_net_test[mo] = float(np.mean([r['net_contrib'] for r in rs]))

    # --- F1 / F2 inference -------------------------------------------------
    print('[infer] F1 block bootstrap...', flush=True)
    f1_gross = block_bootstrap(pi_f1, months_f1, SEED_F1)
    f1_net = block_bootstrap(pi_net_f1, months_f1, SEED_F1)
    print('[infer] F2 sign-flip...', flush=True)
    f2_gross = sign_flip(list(pi_test.values()))
    f2_net = sign_flip([v for v in pi_net_test.values() if v is not None])
    holm_gross = holm(f1_gross['p_one_sided'], f2_gross['p_one_sided'])
    holm_net = holm(f1_net['p_one_sided'], f2_net['p_one_sided'])

    # --- effective sample / dependence ------------------------------------
    flips = 0
    prev_s = None
    for mo in months_full:
        s = 1 if pi[mo] > 0 else -1
        if prev_s is not None and s != prev_s:
            flips += 1
        prev_s = s
    run_info = {}
    for m in MARKETS:
        signs = [r['S'] for r in assess[m]]
        runs = 1
        for i in range(1, len(signs)):
            if signs[i] != signs[i - 1]:
                runs += 1
        run_info[m] = {'n': len(signs), 'runs': runs,
                       'mean_run_len': len(signs) / runs if runs else None,
                       'n_long': sum(1 for s in signs if s > 0)}
    # market correlation (aligned months)
    corr = {}
    for i in range(len(MARKETS)):
        for j in range(i + 1, len(MARKETS)):
            a, b = MARKETS[i], MARKETS[j]
            ra = {r['pos']: r['r'] for r in assess[a]}
            rb = {r['pos']: r['r'] for r in assess[b]}
            common = sorted(set(ra) & set(rb))
            if len(common) >= 3:
                va = np.array([ra[m] for m in common])
                vb = np.array([rb[m] for m in common])
                corr[f'{a}|{b}'] = float(np.corrcoef(va, vb)[0, 1])
            else:
                corr[f'{a}|{b}'] = None

    # --- break-even (protocol Section 10.9) --------------------------------
    be = {}
    V_total = 0.0
    R_total = 0.0
    for m in MARKETS:
        recs = assess[m]
        Vi = sum(abs(r['delta_p']) for r in recs) + abs(recs[-1]['p'])
        Ri = sum(r['r'] for r in recs)
        be[m] = {'V': Vi, 'sum_r': Ri,
                 'h_star_bp': (Ri / Vi) * 10000.0 if Vi > 0 else None}
        V_total += Vi
        R_total += Ri
    h_star_pooled_bp = (R_total / V_total) * 10000.0 if V_total > 0 else None

    # observed pooled median one-way half-spread (4 bid/ask markets)
    obs_hs = []
    for m in BIDASK_MARKETS:
        if spread_by_mkt.get(m):
            obs_hs.extend(spread_by_mkt[m])
    obs_median_bp = float(np.median(obs_hs)) if obs_hs else None

    # --- negative controls -------------------------------------------------
    print('[control] NC2 (6-month time shift)...', flush=True)
    nc2 = {}
    for m in MARKETS:
        monthly, daily = mkt_data[m]
        recs = build_assessments(m, monthly, daily, lookback=12, horizon=1, step=1,
                                 wmode='invvol', hurdle=0.0, outcome_shift=6)
        nc2[m] = recs
    nc2_recs = [r for m in MARKETS for r in nc2[m]]
    months_nc2 = sorted({r['pos'] for r in nc2_recs})
    pi_nc2 = {}
    for mo in months_nc2:
        rs = [r for r in nc2_recs if r['pos'] == mo]
        pi_nc2[mo] = float(np.mean([r['r'] for r in rs]))
    nc2_res = {}
    if len(months_nc2) >= L_BLOCK:
        nc2_res = block_bootstrap(pi_nc2, months_nc2, SEED_F1)
    else:
        vals = np.array(list(pi_nc2.values()))
        nc2_res = {'T': len(vals), 'obs': float(vals.mean()), 'ci95': None,
                   'p_one_sided': None, 'nblocks': None}

    print('[control] NC1 (run-shuffle, diagnostic)...', flush=True)
    rng = np.random.default_rng(SEED_NC1)
    pooled_obs = float(np.mean(list(pi.values())))
    nulls = []
    for rep in range(1000):
        means = []
        for m in MARKETS:
            recs = assess[m]
            # runs of constant S
            runs = []
            cur_s = recs[0]['S']
            cur = [recs[0]]
            for rec in recs[1:]:
                if rec['S'] == cur_s:
                    cur.append(rec)
                else:
                    runs.append(cur)
                    cur = [rec]
                    cur_s = rec['S']
            runs.append(cur)
            perm = rng.permutation(len(runs))
            seq = [rec for i in perm for rec in runs[i]]
            means.append(float(np.mean([r['r'] for r in seq])))
        nulls.append(float(np.mean(means)))
    nc1 = {'n_shuffles': 1000, 'null_mean': float(np.mean(nulls)),
           'null_p95': float(np.percentile(nulls, 95)),
           'frac_ge_observed': float((np.array(nulls) >= pooled_obs).mean()),
           'observed_pooled_mean': pooled_obs}

    # --- crash diagnostics (protocol Section 13) ---------------------------
    crash = {}
    for m in MARKETS:
        monthly, daily = mkt_data[m]
        months = sorted(monthly.keys())
        idx = {mm: i for i, mm in enumerate(months)}
        prior_sig = []
        states = []
        for rec in assess[m]:
            pos = rec['pos']
            am = rec['assess_end']
            # BEAR: trailing 12-month return at assessment month-end = C(m-1)/C(m-13) - 1
            m13 = add_months(pos, -13)
            if m13 in monthly and am in monthly:
                bear = monthly[am][0] / monthly[m13][0] - 1.0
                is_bear = bear <= -0.20
            else:
                is_bear = False
                bear = None
            sig = rec['sigma']
            if len(prior_sig) >= 24:
                thr = np.percentile(prior_sig, 90)
                panic = sig > thr
            else:
                panic = False
                thr = None
            prior_sig.append(sig)
            states.append({'pos': pos, 'bear': is_bear, 'panic': panic,
                           'bear_ret': bear, 'panic_thr': thr, 'r': rec['r']})
        crash[m] = states
    # pooled state means
    state_means = {'BEAR&PANIC': [], 'BEAR only': [], 'PANIC only': [], 'neither': []}
    state_counts = {k: 0 for k in state_means}
    for m in MARKETS:
        for st in crash[m]:
            if st['bear'] and st['panic']:
                key = 'BEAR&PANIC'
            elif st['bear']:
                key = 'BEAR only'
            elif st['panic']:
                key = 'PANIC only'
            else:
                key = 'neither'
            state_counts[key] += 1
            state_means[key].append(st['r'])
    crash_res = {k: {'n': state_counts[k],
                     'mean': float(np.mean(v)) if v else None}
                 for k, v in state_means.items()}

    # --- walk-forward / temporal stability (protocol Section 12) -----------
    wf = {}
    for m in MARKETS:
        recs = assess[m]
        N = len(recs)
        q = [int(math.floor(N * k / 4)) for k in range(1, 4)]
        bounds = [(1, q[0]), (q[0] + 1, q[1]), (q[1] + 1, q[2]), (q[2] + 1, N)]
        for fi, (lo, hi) in enumerate(bounds, start=1):
            sel = [r for r in recs if lo <= r['j'] <= hi]
            months = sorted({r['pos'] for r in sel})
            pm = {}
            for mo in months:
                rs = [r for r in sel if r['pos'] == mo]
                pm[mo] = float(np.mean([r['r'] for r in rs]))
            vals = np.array(list(pm.values()))
            if len(vals) >= 12:
                bb = block_bootstrap(pm, months, SEED_F1)
                ci = bb['ci95']
            else:
                rng2 = np.random.default_rng(SEED_F1)
                repl = np.array([float(np.mean(rng2.choice(vals, size=len(vals), replace=True)))
                                 for _ in range(10000)])
                ci = [float(x) for x in np.percentile(repl, [2.5, 97.5])]
            wf[f'{m}:fold{fi}'] = {'n': len(sel), 'mean': float(vals.mean()),
                                   'ci95': ci, 'sign': 1 if vals.mean() > 0 else -1}
    # chronological thirds
    thirds = {}
    for m in MARKETS:
        recs = assess[m]
        N = len(recs)
        b1 = int(math.floor(N / 3))
        b2 = int(math.floor(2 * N / 3))
        for ti, (lo, hi) in enumerate([(1, b1), (b1 + 1, b2), (b2 + 1, N)], start=1):
            sel = [r for r in recs if lo <= r['j'] <= hi]
            vals = [r['r'] for r in sel]
            thirds[f'{m}:third{ti}'] = {'n': len(sel), 'mean': float(np.mean(vals))}
    # pooled thirds
    for ti in range(1, 4):
        lo = 1
        # pooled thirds over all markets' j (approximate chronological)
        sel = [r for m in MARKETS for r in assess[m]
               if r['j'] <= int(math.floor(r['N'] * ti / 3)) and
               r['j'] > int(math.floor(r['N'] * (ti - 1) / 3))]
        vals = [r['r'] for r in sel]
        thirds[f'POOLED:third{ti}'] = {'n': len(sel), 'mean': float(np.mean(vals)) if vals else None}

    # --- portfolio metrics (gross and net, full sample) --------------------
    def portfolio_stats(series_map, months):
        vals = np.array([series_map[m] for m in months if series_map[m] is not None])
        if len(vals) == 0:
            return None
        eq = np.cumprod(1.0 + vals)
        peak = np.maximum.accumulate(eq)
        dd = (eq - peak) / peak
        ann_mean = 12.0 * float(vals.mean())
        ann_std = math.sqrt(12.0) * float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
        return {'n': len(vals), 'mean': float(vals.mean()), 'median': float(np.median(vals)),
                'hit_rate': float((vals > 0).mean()), 'std': float(vals.std(ddof=1)),
                'ann_mean': ann_mean, 'ann_std': ann_std,
                'sharpe': ann_mean / ann_std if ann_std > 0 else None,
                'max_dd': float(dd.min()), 'equity_end': float(eq[-1])}

    port_full = portfolio_stats(pi, months_full)
    port_net = portfolio_stats(pi_net, months_full)

    # --- per-market results -------------------------------------------------
    per_mkt = {}
    for m in MARKETS:
        recs = assess[m]
        rs = np.array([r['r'] for r in recs])
        nrs = np.array([r['net_contrib'] for r in recs if r['net_contrib'] is not None])
        costs = np.array([r['C'] for r in recs if r['C'] is not None])
        ann_mean = 12.0 * float(rs.mean())
        ann_std = math.sqrt(12.0) * float(rs.std(ddof=1)) if len(rs) > 1 else 0.0
        per_mkt[m] = {
            'N': len(recs), 'n_long': sum(1 for r in recs if r['S'] > 0),
            'n_short': sum(1 for r in recs if r['S'] < 0),
            'mean': float(rs.mean()), 'median': float(np.median(rs)),
            'hit_rate': float((rs > 0).mean()), 'std': float(rs.std(ddof=1)),
            'ann_mean': ann_mean, 'ann_std': ann_std,
            'sharpe': ann_mean / ann_std if ann_std > 0 else None,
            'gross_sum': float(rs.sum()), 'net_sum': float(nrs.sum()) if len(nrs) else None,
            'net_mean': float(nrs.mean()) if len(nrs) else None,
            'mean_cost': float(costs.mean()) if len(costs) else None,
            'break_even_bp': be[m]['h_star_bp'],
            'V': be[m]['V']}

    # --- sensitivities (protocol Section 15; all EXPLORATORY) ---------------
    sens = {}
    for lb in [6, 24]:
        key = f'E1_LB{lb}' if lb == 6 else f'E2_LB{lb}'
        recs_all = []
        for m in MARKETS:
            monthly, daily = mkt_data[m]
            recs_all.extend(build_assessments(m, monthly, daily, lookback=lb, horizon=1,
                                              step=1, wmode='invvol', hurdle=0.0))
        months = sorted({r['pos'] for r in recs_all})
        pm = {}
        for mo in months:
            rs = [r for r in recs_all if r['pos'] == mo]
            pm[mo] = float(np.mean([r['r'] for r in rs]))
        sens[key] = {'n_assessments': len(recs_all), 'n_months': len(months),
                     'mean': float(np.mean(list(pm.values())))}
    # E3 horizon 3 (non-overlapping)
    recs_e3 = []
    for m in MARKETS:
        monthly, daily = mkt_data[m]
        recs_e3.extend(build_assessments(m, monthly, daily, lookback=12, horizon=3, step=3,
                                         wmode='invvol', hurdle=0.0))
    months_e3 = sorted({r['pos'] for r in recs_e3})
    pm_e3 = {}
    for mo in months_e3:
        rs = [r for r in recs_e3 if r['pos'] == mo]
        pm_e3[mo] = float(np.mean([r['r'] for r in rs]))
    sens['E3_H3'] = {'n_assessments': len(recs_e3), 'n_months': len(months_e3),
                     'mean': float(np.mean(list(pm_e3.values())))}
    # E4 flat weighting
    recs_e4 = []
    for m in MARKETS:
        monthly, daily = mkt_data[m]
        recs_e4.extend(build_assessments(m, monthly, daily, lookback=12, horizon=1,
                                         step=1, wmode='flat', hurdle=0.0))
    months_e4 = sorted({r['pos'] for r in recs_e4})
    pm_e4 = {}
    for mo in months_e4:
        rs = [r for r in recs_e4 if r['pos'] == mo]
        pm_e4[mo] = float(np.mean([r['r'] for r in rs]))
    sens['E4_flat'] = {'n_assessments': len(recs_e4), 'n_months': len(months_e4),
                       'mean': float(np.mean(list(pm_e4.values())))}
    # E6 hurdle 0.25%/month
    recs_e6 = []
    for m in MARKETS:
        monthly, daily = mkt_data[m]
        recs_e6.extend(build_assessments(m, monthly, daily, lookback=12, horizon=1,
                                         step=1, wmode='invvol', hurdle=0.0025))
    months_e6 = sorted({r['pos'] for r in recs_e6})
    pm_e6 = {}
    for mo in months_e6:
        rs = [r for r in recs_e6 if r['pos'] == mo]
        pm_e6[mo] = float(np.mean([r['r'] for r in rs]))
    sens['E6_hurdle'] = {'n_assessments': len(recs_e6), 'n_months': len(months_e6),
                         'mean': float(np.mean(list(pm_e6.values())))}
    # E7 exclude USATECHIDXUSD
    mk7 = [m for m in MARKETS if m != 'USATECHIDXUSD']
    recs_e7 = [r for m in mk7 for r in assess[m]]
    months_e7 = sorted({r['pos'] for r in recs_e7})
    pm_e7 = {}
    for mo in months_e7:
        rs = [r for r in recs_e7 if r['pos'] == mo]
        pm_e7[mo] = float(np.mean([r['r'] for r in rs]))
    sens['E7_noUSATECH'] = {'n_assessments': len(recs_e7), 'n_months': len(months_e7),
                            'mean': float(np.mean(list(pm_e7.values())))}
    # E9 capped
    recs_e9 = []
    for m in MARKETS:
        monthly, daily = mkt_data[m]
        recs_e9.extend(build_assessments(m, monthly, daily, lookback=12, horizon=1,
                                         step=1, wmode='capped', hurdle=0.0))
    months_e9 = sorted({r['pos'] for r in recs_e9})
    pm_e9 = {}
    for mo in months_e9:
        rs = [r for r in recs_e9 if r['pos'] == mo]
        pm_e9[mo] = float(np.mean([r['r'] for r in rs]))
    sens['E9_capped'] = {'n_assessments': len(recs_e9), 'n_months': len(months_e9),
                         'mean': float(np.mean(list(pm_e9.values())))}
    # E8 commission band / E10 EURUSD band (net means, full sample)
    net_sens_rows = []
    for c_bp in [0.0, 0.5, 1.0, 2.0]:
        vals = []
        for m in MARKETS:
            recs = assess[m]
            for rec in recs:
                if rec['C'] is None:
                    continue
                C = abs(rec['delta_p']) * (rec['entry_half_bp'] + c_bp) * BP
                if rec is recs[-1] and rec.get('exit_half_bp') is not None:
                    C += abs(rec['p']) * (rec['exit_half_bp'] + c_bp) * BP
                vals.append(rec['r'] - C)
        net_sens_rows.append({'component': 'commission', 'value_bp': c_bp,
                              'pooled_net_mean': float(np.mean(vals))})
    for h_bp in [0.1, 0.5, 1.0, 2.0]:
        vals = []
        for m in MARKETS:
            recs = assess[m]
            for rec in recs:
                if m == 'EURUSD':
                    h = h_bp
                elif rec['entry_half_bp'] is None:
                    continue
                else:
                    h = rec['entry_half_bp']
                C = abs(rec['delta_p']) * h * BP
                if rec is recs[-1] and m == 'EURUSD':
                    C += abs(rec['p']) * h_bp * BP
                elif rec is recs[-1] and rec.get('exit_half_bp') is not None:
                    C += abs(rec['p']) * rec['exit_half_bp'] * BP
                vals.append(rec['r'] - C)
        net_sens_rows.append({'component': 'EURUSD_assumed_spread', 'value_bp': h_bp,
                              'pooled_net_mean': float(np.mean(vals))})

    # --- UNRESOLVED triggers (protocol Section 16a) -------------------------
    coverage_ok = True
    n_ok = 0
    n_tot = 0
    for m in BIDASK_MARKETS:
        for rec in assess[m]:
            n_tot += 1
            if rec['cost_status'] == 'OK':
                n_ok += 1
    coverage = n_ok / n_tot if n_tot else None
    unresolved = {'pooled_flips': flips, 'bidask_cost_coverage': coverage,
                  'pooled_usable_assessments': len(all_recs)}
    unresolved['triggered'] = (flips < 15) or (coverage is not None and coverage < 0.80) or (len(all_recs) < 30)

    # --- economic gate (protocol Section 16a) -------------------------------
    net_viable = (f1_net['ci95'][0] > 0 and f2_net['obs'] > 0 and
                  h_star_pooled_bp is not None and obs_median_bp is not None and
                  h_star_pooled_bp > obs_median_bp)
    # net at 1 bp/side commission
    vals1 = []
    for m in MARKETS:
        recs = assess[m]
        for rec in recs:
            if rec['C'] is None:
                continue
            C = abs(rec['delta_p']) * (rec['entry_half_bp'] + 1.0) * BP
            if rec is recs[-1] and rec.get('exit_half_bp') is not None:
                C += abs(rec['p']) * (rec['exit_half_bp'] + 1.0) * BP
            vals1.append(rec['r'] - C)
    net_pos_at_1bp = float(np.mean(vals1)) > 0
    gate_viable = net_viable and net_pos_at_1bp
    gross_conf = f1_gross['ci95'][0] > 0
    econ_class = None
    if unresolved['triggered']:
        econ_class = 'UNRESOLVED'
    elif gate_viable:
        econ_class = 'ECONOMICALLY VIABLE'
    elif gross_conf and not (f1_net['ci95'][0] > 0):
        econ_class = 'ECONOMICALLY INSUFFICIENT'
    elif (not gross_conf) or f2_gross['sign'] < 0:
        econ_class = 'NOT CONFIRMED'
    else:
        econ_class = 'ECONOMICALLY INSUFFICIENT'

    # --- scientific classification (protocol Section 16b) -------------------
    sci_class = None
    if unresolved['triggered']:
        sci_class = 'INCONCLUSIVE'
    elif f1_net['ci95'][0] > 0 and f2_gross['sign'] > 0 and gate_viable:
        sci_class = 'REPRODUCED'
    elif f1_gross['ci95'][0] > 0:
        sci_class = 'PARTIALLY REPRODUCED'
    elif f1_gross['ci95'][1] <= 0:
        sci_class = 'CONTRADICTED'
    else:
        sci_class = 'INCONCLUSIVE'

    # ------------------------------------------------------------------------
    # 7. Assemble outputs
    # ------------------------------------------------------------------------
    results = {
        'protocol_version': '1.0.3',
        'executed_at': datetime.utcnow().isoformat() + 'Z',
        'elapsed_seconds': round(time.time() - T0, 1),
        'fingerprints': fp,
        'm1_stats': m1_stats,
        'sample': {
            'per_market_N': {m: len(assess[m]) for m in MARKETS},
            'pooled_N': len(all_recs),
            'months_full': [ym_key(m) for m in months_full],
            'months_f1': [ym_key(m) for m in months_f1],
            'months_test': [ym_key(m) for m in months_test],
            'T_F1': len(months_f1), 'T_TEST': len(months_test)},
        'f1_gross': f1_gross, 'f1_net': f1_net,
        'f2_gross': f2_gross, 'f2_net': f2_net,
        'holm_gross': holm_gross, 'holm_net': holm_net,
        'pooled_full': {'mean': float(np.mean(list(pi.values()))),
                        'months': len(months_full),
                        'flips': flips,
                        'mean_ann': 12.0 * float(np.mean(list(pi.values())))},
        'pi_monthly': {ym_key(m): v for m, v in pi.items()},
        'pi_net_monthly': {ym_key(m): v for m, v in pi_net.items() if v is not None},
        'run_info': run_info,
        'corr': corr,
        'cost': {
            'observed_median_one_way_bp': obs_median_bp,
            'bidask_coverage': coverage,
            'n_ok': n_ok, 'n_total': n_tot,
            'break_even_pooled_bp': h_star_pooled_bp,
            'break_even_per_market_bp': {m: be[m]['h_star_bp'] for m in MARKETS},
            'spread_percentiles': {m: ({'P50': float(np.percentile(v, 50)),
                                        'P75': float(np.percentile(v, 75)),
                                        'P90': float(np.percentile(v, 90)),
                                        'P95': float(np.percentile(v, 95)),
                                        'P99': float(np.percentile(v, 99)),
                                        'n': len(v)} if v else None)
                                   for m, v in spread_by_mkt.items()}},
        'controls': {'NC1': nc1, 'NC2': nc2_res},
        'crash': crash_res,
        'walk_forward': wf,
        'thirds': thirds,
        'portfolio': {'gross': port_full, 'net': port_net},
        'per_market': per_mkt,
        'sensitivities': sens,
        'net_sensitivity': net_sens_rows,
        'unresolved': unresolved,
        'gate': {'gross_confirmed': gross_conf, 'net_viable': gate_viable,
                 'net_pos_at_1bp_commission': net_pos_at_1bp,
                 'f2_net_positive': f2_net['obs'] > 0,
                 'h_star_gt_observed_median': (h_star_pooled_bp is not None and
                                               obs_median_bp is not None and
                                               h_star_pooled_bp > obs_median_bp)},
        'economic_class': econ_class,
        'scientific_class': sci_class,
    }

    # --- CSV artifacts ------------------------------------------------------
    import csv
    def _open(name, mode='w'):
        return open(os.path.join(OUT, name), mode, newline='', encoding='utf-8')
    # daily series
    with _open('daily_series_TSMOM_V1.csv') as f:
        w = csv.writer(f)
        w.writerow(['market', 'date', 'close'])
        w.writerows(daily_rows)
    # assessment events
    with _open('assessment_events_TSMOM_V1.csv') as f:
        w = csv.writer(f)
        w.writerow(['market', 'position_month', 'assess_month_end', 'j', 'N', 'partition',
                    'lookback_return', 'signal', 'sigma_ann', 'weight', 'position',
                    'forward_return', 'r', 'delta_p', 'entry_half_bp', 'cost_status',
                    'exit_half_bp', 'C', 'net_contrib'])
        for m in MARKETS:
            for rec in assess[m]:
                w.writerow([m, ym_key(rec['pos']), ym_key(rec['assess_end']), rec['j'], rec['N'],
                            rec['part'], round(rec['L'], 8), rec['S'], round(rec['sigma'], 8),
                            round(rec['w'], 6), round(rec['p'], 6), round(rec['R'], 8),
                            round(rec['r'], 8), round(rec['delta_p'], 6),
                            rec['entry_half_bp'], rec['cost_status'],
                            rec.get('exit_half_bp'), rec['C'], rec['net_contrib']])
    # cost match
    with _open('cost_match_TSMOM_V1.csv') as f:
        w = csv.writer(f)
        w.writerow(['market', 'leg', 'label', 'dist_seconds', 'bid', 'ask', 'half_spread_bp'])
        for m in BIDASK_MARKETS:
            recs = assess[m]
            for rec in recs:
                w.writerow([m, 'entry', f'entry:{ym_key(rec["pos"])}',
                            rec['entry_dist'],
                            '' if rec['entry_half_bp'] is None else '',
                            '' if rec['entry_half_bp'] is None else '',
                            rec['entry_half_bp']])
            w.writerow([m, 'exit', 'exit', recs[-1].get('exit_dist'),
                        '', '', recs[-1].get('exit_half_bp')])
    # bootstrap replicates
    with _open('bootstrap_TSMOM_V1.csv') as f:
        w = csv.writer(f)
        w.writerow(['series', 'replicate', 'pooled_mean'])
        for i, v in enumerate(f1_gross['replicates'], start=1):
            w.writerow(['F1_gross', i, round(v, 8)])
        for i, v in enumerate(f1_net['replicates'], start=1):
            w.writerow(['F1_net', i, round(v, 8)])
    # spread distributions
    with _open('spread_distributions_TSMOM_V1.csv') as f:
        w = csv.writer(f)
        w.writerow(['market', 'P50', 'P75', 'P90', 'P95', 'P99', 'n_quotes'])
        for m in MARKETS:
            v = spread_by_mkt[m]
            if v:
                w.writerow([m] + [round(float(np.percentile(v, p)), 4) for p in [50, 75, 90, 95, 99]] + [len(v)])
            else:
                w.writerow([m, 'UNOBSERVED', '', '', '', '', 0])
    # net sensitivity
    with _open('net_sensitivity_TSMOM_V1.csv') as f:
        w = csv.writer(f)
        w.writerow(['component', 'value_bp_per_side', 'pooled_net_monthly_mean'])
        for r in net_sens_rows:
            w.writerow([r['component'], r['value_bp'], round(r['pooled_net_mean'], 8)])
    # results JSON
    with open(os.path.join(OUT, 'results_TSMOM_V1.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    # metadata JSON
    meta = {
        'experiment': 'TSMOM V1',
        'protocol_version': '1.0.3',
        'protocol_sha256': fp['protocol_sha256'],
        'source_sha256': {k: v['sha256'] for k, v in fp['sources'].items()},
        'python': fp['python'],
        'numpy': fp['numpy'],
        'seed_f1': SEED_F1, 'seed_nc1': SEED_NC1, 'B': B_REPL, 'L_block': L_BLOCK,
        'bp_decimal': BP, 'eurusd_h_assumed_bp': EURUSD_H_ASSUMED_BP,
        'row_counts': {m: m1_stats[m]['rows'] for m in MARKETS},
        'usable_assessments': {m: len(assess[m]) for m in MARKETS},
        'executed_at': results['executed_at'],
    }
    with open(os.path.join(OUT, 'experiment_metadata_TSMOM_V1.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    # --- scientific report --------------------------------------------------
    def fmt(x, nd=4):
        return 'None' if x is None else f'{x:.{nd}f}'

    def pct(x):
        return 'None' if x is None else f'{x * 100:.2f}%'

    R = results
    lines = []
    A = lines.append
    A('# QUANTFORGE — TSMOM V1 CONTROLLED EXPERIMENT — SCIENTIFIC REPORT')
    A('')
    A(f'**Protocol:** EVENT_STUDY_PROTOCOL_TSMOM_V1.md v1.0.3 (frozen) — executed {R["executed_at"]}')
    A(f'**Elapsed:** {R["elapsed_seconds"]} s')
    A('')
    A('## 1. Scientific Classification')
    A(f'**{R["scientific_class"]}**')
    A('')
    A('## 2. Economic Classification')
    A(f'**{R["economic_class"]}**')
    A('')
    A('## 3. Sample')
    A('')
    A('| Market | N usable | Assessments span |')
    A('|---|---|---|')
    for m in MARKETS:
        recs = assess[m]
        A(f'| {m} | {len(recs)} | {ym_key(recs[0]["pos"])}..{ym_key(recs[-1]["pos"])} |')
    A(f'| **Pooled** | **{len(all_recs)}** | |')
    A('')
    A(f'Pooled calendar months: {len(months_full)} (T_F1 = {len(months_f1)}, T_TEST = {len(months_test)})')
    A(f'Pooled usable assessments: {len(all_recs)}; pooled sign flips: {flips}.')
    A('')
    A('## 4. Primary F1 Result (TRAIN+VALIDATION, first 85%)')
    A('')
    A('| Series | Mean/month | 95% CI | one-sided p | T | blocks |')
    A('|---|---|---|---|---|---|')
    A(f'| F1 gross | {fmt(f1_gross["obs"])} | [{fmt(f1_gross["ci95"][0])}, {fmt(f1_gross["ci95"][1])}] | {fmt(f1_gross["p_one_sided"], 4)} | {f1_gross["T"]} | {f1_gross["nblocks"]} |')
    A(f'| F1 net | {fmt(f1_net["obs"])} | [{fmt(f1_net["ci95"][0])}, {fmt(f1_net["ci95"][1])}] | {fmt(f1_net["p_one_sided"], 4)} | {f1_net["T"]} | {f1_net["nblocks"]} |')
    A('')
    A('## 5. Protected F2 Result (TEST, final 15%, single use)')
    A('')
    A(f'Pooled TEST mean (gross): {fmt(f2_gross["obs"])}; sign: {f2_gross["sign"]}; exact sign-flip one-sided p: {fmt(f2_gross["p_one_sided"], 4)} (T = {f2_gross["T"]}, {f2_gross["assignments"]} assignments).')
    A(f'Pooled TEST mean (net): {fmt(f2_net["obs"])}; sign: {f2_net["sign"]}; exact sign-flip one-sided p: {fmt(f2_net["p_one_sided"], 4)}.')
    A('')
    A('## 6. Holm Multiple-Comparison Control (family {F1, F2}, alpha 0.05)')
    A('')
    A(f'Gross: F1 raw p {fmt(f1_gross["p_one_sided"], 4)} -> Holm {fmt(holm_gross[1], 4)}; F2 raw p {fmt(f2_gross["p_one_sided"], 4)} -> Holm {fmt(holm_gross[2], 4)}.')
    A(f'Net:   F1 raw p {fmt(f1_net["p_one_sided"], 4)} -> Holm {fmt(holm_net[1], 4)}; F2 raw p {fmt(f2_net["p_one_sided"], 4)} -> Holm {fmt(holm_net[2], 4)}.')
    A('')
    A('## 7. Per-Market Results (full sample)')
    A('')
    A('| Market | N | L/S | mean r | net mean | hit | ann mean | Sharpe | mean cost/mo | break-even bp |')
    A('|---|---|---|---|---|---|---|---|---|---|')
    for m in MARKETS:
        pm = per_mkt[m]
        A(f'| {m} | {pm["N"]} | {pm["n_long"]}/{pm["n_short"]} | {fmt(pm["mean"])} | {fmt(pm["net_mean"])} | {pct(pm["hit_rate"])} | {fmt(pm["ann_mean"])} | {fmt(pm["sharpe"])} | {fmt(pm["mean_cost"])} | {fmt(pm["break_even_bp"])} |')
    A('')
    A('## 8. Pooled / Portfolio')
    A('')
    A(f'Full-sample pooled gross mean: {fmt(R["pooled_full"]["mean"])} (ann. {fmt(R["pooled_full"]["mean_ann"])}); months {R["pooled_full"]["months"]}.')
    pg, pn = R['portfolio']['gross'], R['portfolio']['net']
    if pg:
        A(f'Portfolio gross: ann mean {fmt(pg["ann_mean"])}, Sharpe {fmt(pg["sharpe"])}, max DD {fmt(pg["max_dd"])}, hit {pct(pg["hit_rate"])}, equity end {fmt(pg["equity_end"])}.')
    if pn:
        A(f'Portfolio net:   ann mean {fmt(pn["ann_mean"])}, Sharpe {fmt(pn["sharpe"])}, max DD {fmt(pn["max_dd"])}, hit {pct(pn["hit_rate"])}, equity end {fmt(pn["equity_end"])}.')
    A('')
    A('## 9. Transaction Costs')
    A('')
    A(f'Observed pooled median one-way half-spread (4 bid/ask markets): {fmt(obs_median_bp)} bp. Bid/ask cost-match coverage: {pct(coverage)} ({n_ok}/{n_tot} legs).')
    A('EURUSD spread: UNOBSERVED — registered 0.1 bp/side ASSUMPTION (band E10).')
    A('')
    A('## 10. Break-Even')
    A('')
    A(f'Pooled break-even one-way cost h*: {fmt(h_star_pooled_bp)} bp.')
    for m in MARKETS:
        A(f'- {m}: h* = {fmt(be[m]["h_star_bp"])} bp (V = {be[m]["V"]:.2f} units traded).')
    A('')
    A('## 11. Negative Controls')
    A('')
    A(f'NC1 (run-shuffle, diagnostic only, 1000 shuffles): null mean {fmt(nc1["null_mean"])}, P95 {fmt(nc1["null_p95"])}, fraction >= observed {fmt(nc1["frac_ge_observed"], 4)}.')
    A(f'NC2 (6-month time-shift, formal control): mean {fmt(nc2_res["obs"])}, CI {nc2_res.get("ci95")}, T = {nc2_res.get("T")}.')
    A('')
    A('## 12. Crash Diagnostics (descriptive only)')
    A('')
    A('| State | n | mean r |')
    A('|---|---|---|')
    for k, v in crash_res.items():
        A(f'| {k} | {v["n"]} | {fmt(v["mean"])} |')
    A('')
    A('## 13. Walk-Forward / Temporal Stability (descriptive)')
    A('')
    A('| Fold | n | mean | 95% CI | sign |')
    A('|---|---|---|---|---|')
    for k, v in wf.items():
        A(f'| {k} | {v["n"]} | {fmt(v["mean"])} | {v["ci95"]} | {v["sign"]} |')
    A('')
    A('Pooled chronological thirds:')
    for k in ['POOLED:third1', 'POOLED:third2', 'POOLED:third3']:
        v = thirds[k]
        A(f'- {k}: n = {v["n"]}, mean = {fmt(v["mean"])}')
    A('')
    A('## 14. Exploratory Sensitivities (EXPLORATORY — NON-CONFIRMATORY)')
    A('')
    A('| Sensitivity | n assessments | pooled mean |')
    A('|---|---|---|')
    for k, v in sens.items():
        A(f'| {k} | {v["n_assessments"]} | {fmt(v["mean"])} |')
    A('')
    A('Net-sensitivity bands (full sample):')
    A('')
    A('| Component | bp/side | pooled net mean |')
    A('|---|---|---|')
    for r in net_sens_rows:
        A(f'| {r["component"]} | {r["value_bp"]} | {fmt(r["pooled_net_mean"])} |')
    A('')
    A('## 15. Market Correlation (aligned months, direction-adjusted)')
    A('')
    A('| Pair | rho |')
    A('|---|---|')
    for k, v in corr.items():
        A(f'| {k} | {fmt(v)} |')
    A('')
    A('## 16. Unresolved Triggers / Gate')
    A('')
    A(f'pooled flips = {flips} (<15 -> UNRESOLVED); bid/ask cost coverage = {pct(coverage)}; pooled usable assessments = {len(all_recs)} (<30 -> UNRESOLVED). Triggered: {unresolved["triggered"]}.')
    A(f'F1 gross confirmed (CI lower > 0): {gross_conf}. Net viable (F1 net CI>0 & F2 net>0 & h*>median & net>0 @1bp): {gate_viable}.')
    A('')
    A('## 17. Reproducibility')
    A('')
    A(f'- Protocol SHA-256: `{fp["protocol_sha256"]}`')
    for k, v in fp['sources'].items():
        A(f'- {v["path"]}: `{v["sha256"]}`')
    A(f'- python: {fp["python"].split()[0]} {fp["python"].split()[1]}; numpy: {fp["numpy"]}')
    A(f'- seed F1 = {SEED_F1}, B = {B_REPL}, L = {L_BLOCK}; seed NC1 = {SEED_NC1}')
    A(f'- Cost convention: 1 bp = {BP}; Option A net series `pi_net_m = mean_i(p*R - |dp|*h)` with final-close term.')
    A('')
    A('---')
    A('*Research evidence only. No BOE/runtime semantics are created by this experiment.*')
    with open(os.path.join(OUT, 'SCIENTIFIC_REPORT_TSMOM_V1.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print('[done] artifacts written to output/tsmom_v1/', flush=True)
    print(f'[done] scientific_class={sci_class}  economic_class={econ_class}', flush=True)

if __name__ == '__main__':
    main()
