#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUANTFORGE - H01 EQUITY VOLATILITY-ASYMMETRY V1 - CONTROLLED EXECUTION (v1.1.0)
Protocol : output/research_discovery/H01_EQUITY_VOLATILITY_ASYMMETRY_PROTOCOL_V1.md
           (v1.1.0, FROZEN; SHA-256 recorded in experiment_metadata)
Clearance: PASS - APPROVED FOR EXECUTION (final independent H01 Equity V1.1
           execution-clearance audit; precision clarification applied).

This is the ONE authorized H01 Equity V1 experiment. Single uninterrupted
invocation. Serial execution (1 worker) by default - guarantees that serial,
1-worker and 2-worker executions produce identical registered draws for the
same seed (the RNG stream is consumed serially in fixed cell order
EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2 x replicate index). NO
partial-cache resume, NO checkpointing, NO concurrent runs. Runs at
below-normal OS priority (set externally by the launcher).

Frozen parameter summary (protocol v1.1.0):
  shock        = daily close-to-close log return r_t; r_t = 0 excluded
  response     = dlnRV = ln(RV_{t+1..t+5}) - ln(RV_{t-5..t-1}); RV = sum of
                 squared daily log returns; shock day excluded from both windows
  strata       = within-market terciles of ln(RV_back) over the market's full
                 eligible series within its layer window; computed ONCE,
                 frozen constants (np.quantile method='linear')
  matching     = within-(market,stratum) nearest-neighbour caliper on |r|,
                 caliper = 0.25*SD(|r|) computed once on original eligible data
                 and FROZEN; greedy one-to-one, no reuse; stable tie-break
                 (|r| asc, timestamp asc); reference pool = smaller of NEG/POS
                 (equal -> POS)
  statistic    = d_(m,s) = mean over matched pairs of [dlnRV(neg) - dlnRV(pos)];
                 d_m = equal mean over strata with >= 1 pair; D_cell = equal
                 mean over primary-evaluable markets
  evaluability = >= 30 matched pairs in ALL 3 strata (market);
                 >= 2 evaluable markets (cell verdict); otherwise
                 EVIDENCE-LIMITED/DESCRIPTIVE
  family       = 4 cells (EQBROAD_L1, EQBROAD_L2, EQTECH_L1, EQTECH_L2),
                 Holm step-down, alpha = 0.05, two-sided
  bootstrap    = synchronized circular calendar blocks over each cell's union
                 calendar, L = 11, B = 10,000, single master seed 20260816;
                 nblocks = ceil(T/L); wrap-around modulo T; matching rebuilt
                 inside every replicate with FROZEN calipers/terciles;
                 evaluable-market membership fixed at the original-data stage
  null         = data-level construction: c_(m,s) = observed matched-pair mean
                 d_(m,s), FROZEN; null pair difference = d_i - c_(m,s) (the
                 exact equivalent of the registered shock-response
                 +/-c_(m,s)/2 transformation, applied before rebuilt matching
                 to every eligible shock including originally-unmatched ones);
                 statistic-level pivot D*_null = D* - D_obs is never
                 substituted
  p-value      = p = (1 + count)/(B + 1), count = #{finite null draws:
                 |D*_null| >= |D_obs|}, inclusive >=; denominator fixed (B+1)
  CI           = ordinary percentile sampling CI (2.5, 97.5) of D_cell^(b);
                 never replaced by the null distribution
  Holm NaN     = a cell with no finite p is p = 1.0 for Holm ordering and
                 receives no primary scientific verdict

Implementation notes (deterministic; never scientific parameter changes):
  * No pandas: csv-module + numpy only (pandas 3.0.2 is unsafe on this
    platform for large string frames). scipy.optimize is used ONLY for the
    secondary GJR/EGARCH diagnostics (protocol 21.6).
  * Frozen snapshot files are read from the registered 2026-08-16 locations:
    HPD front_sp.csv (CORE VALID) + the four FRED fredgraph CSV files. Every
    input SHA-256 must match protocol 7; otherwise GATE 1 FAILED -> STOP.
  * FRED holiday placeholders in the frozen snapshot are EMPTY value fields
    (not "."); counts must equal the registered 96/96/362/487 rows; they are
    dropped as missing days (protocol 8.1), never imputed.
  * sp daily series is pinned to continuous ratio-back-adjusted adj_close.
  * Historical-layer era window (protocol 5 cell table): all historical
    series are restricted to 1982-04-21 .. 2002-10-01 (the HPD era); NDX
    starts 1986-01-02 within it; the registered CONTEMPORARY window is
    2016-08-15 .. 2026-08-14.
"""
import csv
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

ENCODING = 'utf-8'
try:
    sys.stdout.reconfigure(encoding=ENCODING)
    sys.stderr.reconfigure(encoding=ENCODING)
except AttributeError:
    pass

T0 = time.time()

REPO = r'C:\Users\User10\Documents\MRV\yuvi\QuantForge'
OUT = os.environ.get('H01EQ_OUT') or os.path.join(REPO, 'output', 'research_discovery',
                                                  'H01_EQUITY_VOLATILITY_ASYMMETRY')
HPD = os.path.join(REPO, 'output', 'research_discovery', 'H01_EQUITY_VOLATILITY_ASYMMETRY', 'daily_series')
FREDDIR = os.path.join(REPO, 'data', 'fred')
M1DIR = os.path.join(REPO, 'data', 'm1')
PROTOCOL_PATH = os.path.join(REPO, 'output', 'research_discovery',
                             'H01_EQUITY_VOLATILITY_ASYMMETRY_PROTOCOL_V1.md')

# ---------------------------------------------------------------------------
# Frozen constants (protocol v1.1.0)
# ---------------------------------------------------------------------------
PROTOCOL_VERSION = '1.3.0'
SEED = 20260816
B_REPL = int(os.environ.get('H01EQ_B', 10000))
L_BLOCK = 11
CALIPER_RATIO = 0.25
MIN_PAIRS = 30
MIN_EVALUABLE = 2
ALPHA = 0.05

HIST_START = '1982-04-21'
HIST_END = '2002-10-01'
CONT_START = '2016-08-15'
CONT_END = '2026-08-14'
COMMON_WIN = ('1986-01-02', '2002-10-01')

# cell order is FROZEN (protocol 17.6): (cell, era, exposure, markets)
CELLS = [
    ('EQBROAD_L1', 'HISTORICAL', 'broad', [('sp', 'HPD'), ('NYA', 'HTML')]),
    ('EQBROAD_L2', 'CONTEMPORARY', 'broad', [('SP500', 'FRED'), ('DJIA', 'FRED')]),
    ('EQTECH_L1', 'HISTORICAL', 'tech', [('NASDAQ100', 'FRED'), ('NASDAQCOM', 'FRED')]),
    ('EQTECH_L2', 'CONTEMPORARY', 'tech', [('NASDAQ100', 'FRED'), ('NASDAQCOM', 'FRED')]),
]
CELL_ORDER = [c[0] for c in CELLS]
CROSS_ERA_CELLS = {'EQTECH_L1': 'EQTECH_L2', 'EQTECH_L2': 'EQTECH_L1'}
# EQBROAD cross-era comparison is EVIDENCE-LIMITED by construction (L1 is
# single-market); the cross-era gate never applies to EQBROAD cells (protocol 20).

FINGERPRINTS = {
    'sp_historical.csv': 'dd35661826279d786c3acec08446e7f0c99137b6a349ad367461851b61148bd8',
    'NYA_DATA.html': '367b1037791f534318f46c5694df77ad2dc990b52409dadc0bd609714ffbca6f',
    'fred_SP500.csv': '4b6c37f3477a4f3454009e500eb1b4d7844b38b0aaad10097b5fe6a5f8ae0db7',
    'fred_DJIA.csv': '6a274816b3ed64956346c10dc8decb5eb585155ac16af410cd2306048d290ee2',
    'fred_NASDAQCOM.csv': '377af7dec4b1a01486cc9e2db48fbe0538e024d58ed258eedbd01e98494358d6',
    'fred_NASDAQ100.csv': '1196c3f2dca171c1b56b4bbe2cc1fcd51ec7ea1f30bb74d7c3cfc2a313ffe52f',
}
FRED_HOLIDAY_COUNTS = {'SP500': 96, 'DJIA': 96, 'NASDAQ100': 362, 'NASDAQCOM': 487}

LOG_PATH = os.path.join(OUT, 'run_h01_equity_v1.log')
_logfh = None


def log(msg):
    line = f'[{time.strftime("%H:%M:%S")}] {msg}'
    print(line, flush=True)
    if _logfh:
        _logfh.write(line + '\n')
        _logfh.flush()


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def mem_rss_mb():
    """Current process working set (MB); -1 if unavailable."""
    try:
        import psutil
        return float(psutil.Process().memory_info().rss) / (1024.0 * 1024.0)
    except Exception:
        return -1.0


# ---------------------------------------------------------------------------
# Loaders (frozen snapshot inputs)
# ---------------------------------------------------------------------------

def load_hpd(root, win=None):
    """HPD front series: date, sym, close, adj_close. Returns from adj_close.
    Roll day = sym change vs previous row. Gates: dup dates, non-positive."""
    dates, syms, close_v, adj_v = [], [], [], []
    with open(os.path.join(HPD, f'{root}_historical.csv'), newline='', encoding=ENCODING) as f:
        rd = csv.reader(f)
        header = next(rd, None)
        if header != ['date', 'sym', 'close', 'adj_close'] and header != ['date', 'sym', 'close', 'adj_close', 'is_roll_day', 'log_return']:
            raise SystemExit(f'{root}: unexpected header {header}')
        for p in rd:
            if not p or len(p) < 4:
                continue
            try:
                c = float(p[2])
                a = float(p[3])
            except ValueError:
                raise SystemExit(f'GATE 6 (validity) FAILED: non-numeric row in {root}_historical.csv: {p}')
            if not (c > 0 and a > 0):
                raise SystemExit(f'GATE 6 (validity) FAILED: nonpositive close in {root}_historical.csv: {p}')
            dates.append(p[0])
            syms.append(p[1])
            close_v.append(c)
            adj_v.append(a)
    if win:
        lo, hi = win
        idx = [i for i, d in enumerate(dates) if lo <= d <= hi]
        dates = [dates[i] for i in idx]
        syms = [syms[i] for i in idx]
        close_v = [close_v[i] for i in idx]
        adj_v = [adj_v[i] for i in idx]
    n = len(dates)
    seen = set()
    for d in dates:
        if d in seen:
            raise SystemExit(f'GATE 4 (duplicate) FAILED: duplicate date {d} in {root}_historical.csv')
        seen.add(d)
    r = [None] * n
    is_roll = [False] * n
    for i in range(1, n):
        r[i] = math.log(adj_v[i] / adj_v[i - 1])
        is_roll[i] = (syms[i] != syms[i - 1])
    return {'root': root, 'dates': dates, 'syms': syms, 'r': r, 'is_roll': is_roll,
            'closes': close_v, 'adj': adj_v, 'n_rows': n}


def load_fred(sym, win):
    """FRED fredgraph CSV -> daily series within era window.
    Holiday placeholders (empty/'.'/non-numeric values) are dropped as missing
    days; their count must equal the registered FRED_HOLIDAY_COUNTS. Gates:
    duplicate dates, non-positive values, weekend rows."""
    path = os.path.join(FREDDIR, f'fred_{sym}.csv')
    rows = []
    holidays = 0
    with open(path, newline='', encoding=ENCODING) as f:
        rd = csv.reader(f)
        header = next(rd, None)
        if header is None or header[0].strip().lower() != 'observation_date':
            raise SystemExit(f'GATE 1 FAILED: unexpected FRED header {header} for {sym}')
        for p in rd:
            if not p or len(p) < 2:
                continue
            d = p[0].strip()
            v = p[1].strip()
            if v == '' or v == '.':
                holidays += 1
                continue
            try:
                x = float(v)
            except ValueError:
                # non-numeric placeholder -> holiday row (registered count below)
                holidays += 1
                continue
            if not (x > 0):
                raise SystemExit(f'GATE 4 (validity) FAILED: nonpositive value {v} for {sym} on {d}')
            rows.append((d, x))
    if holidays != FRED_HOLIDAY_COUNTS[sym]:
        raise SystemExit(f'GATE 1/8 FAILED: {sym} holiday placeholder count {holidays} != registered {FRED_HOLIDAY_COUNTS[sym]}')
    lo, hi = win
    rows = [(d, x) for (d, x) in rows if lo <= d <= hi]
    seen = set()
    for d, _ in rows:
        if d in seen:
            raise SystemExit(f'GATE 4 (duplicate) FAILED: duplicate date {d} for {sym}')
        seen.add(d)
    prev_d = None
    for d, _ in rows:
        if prev_d is not None:
            # weekend check: FRED has no weekend rows; verify
            import datetime as _dt
            dt = _dt.date.fromisoformat(d)
            if dt.weekday() >= 5:
                raise SystemExit(f'GATE 4 (weekend) FAILED: weekend row {d} for {sym}')
        prev_d = d
    n = len(rows)
    dates = [d for d, _ in rows]
    closes = [x for _, x in rows]
    r = [None] * n
    for i in range(1, n):
        r[i] = math.log(closes[i] / closes[i - 1])
    return {'root': sym, 'dates': dates, 'syms': [sym] * n, 'r': r,
            'is_roll': [False] * n, 'closes': closes, 'adj': closes, 'n_rows': n}


def load_nya(win):
    """HTML extraction -> standardized daily NYA Close series."""
    import re
    import datetime
    path = os.path.join(REPO, 'docs', 'NYA_DATA.html')
    with open(path, 'r', encoding=ENCODING) as f:
        content = f.read()

    tbody_match = re.search(r'<tbody>(.*?)</tbody>', content, re.IGNORECASE | re.DOTALL)
    if not tbody_match:
        raise SystemExit('GATE 6 FAILED: NYA tbody not found')
    tbody = tbody_match.group(1)

    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody, re.IGNORECASE | re.DOTALL)
    data = []
    seen = set()
    for row in rows:
        cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.IGNORECASE | re.DOTALL)
        if len(cols) >= 5:
            date_str = cols[0].strip()
            close_str = cols[4].strip().replace(',', '')
            if close_str in ('-', ''):
                continue
            try:
                dt = datetime.datetime.strptime(date_str, '%b %d, %Y').strftime('%Y-%m-%d')
                close_val = float(close_str)
                if close_val <= 0:
                    raise SystemExit(f'GATE 6 FAILED: nonpositive close in NYA: {close_val}')
                if dt in seen:
                    raise SystemExit(f'GATE 4 FAILED: duplicate date in NYA: {dt}')
                seen.add(dt)
                data.append((dt, close_val))
            except ValueError:
                pass

    data.sort()
    
    lo, hi = win
    data = [(d, c) for (d, c) in data if lo <= d <= hi]
    
    n = len(data)
    dates = [d for d, _ in data]
    closes = [c for _, c in data]
    r = [None] * n
    for i in range(1, n):
        r[i] = math.log(closes[i] / closes[i - 1])
        
    return {'root': 'NYA', 'dates': dates, 'syms': ['NYA'] * n, 'r': r,
            'is_roll': [False] * n, 'closes': closes, 'adj': closes, 'n_rows': n}


def load_m1_daily(mkt):
    """M1 -> daily close (last bar per UTC day, last-wins dedup), streaming
    csv-module pass (O(#days) memory). Mirrors the v1.2 registered load_m1."""
    path = os.path.join(M1DIR, f'{mkt}_M1.csv')
    best = {}
    n_valid = 0
    bad_close = 0
    prev_ts = None
    n_unsorted = 0
    dup_raw = 0
    with open(path, newline='', encoding=ENCODING) as f:
        rd = csv.reader(f)
        next(rd, None)
        for row in rd:
            if not row or len(row) < 5:
                continue
            ts = row[0]
            try:
                cv = float(row[4])
            except ValueError:
                bad_close += 1
                continue
            n_valid += 1
            if prev_ts is not None:
                if ts < prev_ts:
                    n_unsorted += 1
                elif ts == prev_ts:
                    dup_raw += 1
            prev_ts = ts
            d = ts[:10]
            cur = best.get(d)
            if cur is None or ts >= cur[0]:
                best[d] = (ts, cv)
    if n_unsorted:
        raise SystemExit(f'GATE 4 FAILED for {mkt}: {n_unsorted} out-of-order timestamps')
    if dup_raw:
        raise SystemExit(f'GATE 4 FAILED for {mkt}: ambiguous duplicate timestamps ({dup_raw})')
    daily = [(d, c) for d, (_, c) in sorted(best.items())]
    n = len(daily)
    dates = [d for d, _ in daily]
    closes = [c for _, c in daily]
    r = [None] * n
    for i in range(1, n):
        r[i] = math.log(closes[i] / closes[i - 1])
    return {'root': mkt, 'dates': dates, 'syms': [mkt] * n, 'r': r,
            'is_roll': [False] * n, 'closes': closes, 'adj': closes, 'n_rows': n}


# ---------------------------------------------------------------------------
# Eligible-shock construction (protocol 8-11)
# ---------------------------------------------------------------------------

def build_records(daily, win=(5, 5)):
    dates, r, is_roll = daily['dates'], daily['r'], daily['is_roll']
    n = len(dates)
    BL, FL = win
    records = []
    cnt = {'roll_day': 0, 'roll_window': 0, 'incomplete_window': 0, 'zero_rv': 0,
           'zero_return': 0}
    for i in range(1, n):
        if r[i] is None:
            continue
        if is_roll[i]:
            cnt['roll_day'] += 1
            continue
        if i - BL < 0 or i + FL >= n:
            cnt['incomplete_window'] += 1
            continue
        back = range(i - BL, i)
        fwd = range(i + 1, i + 1 + FL)
        if any(is_roll[j] for j in back) or any(is_roll[j] for j in fwd):
            cnt['roll_window'] += 1
            continue
        if any(r[j] is None for j in back) or any(r[j] is None for j in fwd):
            cnt['incomplete_window'] += 1
            continue
        rvb = sum(r[j] * r[j] for j in back)
        rvf = sum(r[j] * r[j] for j in fwd)
        if rvb <= 0.0 or rvf <= 0.0:
            cnt['zero_rv'] += 1
            continue
        if r[i] == 0.0:
            cnt['zero_return'] += 1
            continue
        records.append({'date': dates[i], 'r': r[i],
                        'lnrv_back': math.log(rvb),
                        'dlnrv': math.log(rvf) - math.log(rvb)})
    return records, cnt


def add_secondary_stores(records, daily):
    dates, r, is_roll = daily['dates'], daily['r'], daily['is_roll']
    idx = {d: k for k, d in enumerate(dates)}
    rr = np.array([x for x in r[1:] if x is not None], dtype=float)
    full_sigma = float(rr.std(ddof=1)) if len(rr) > 1 else float('nan')
    for rec in records:
        i = idx[rec['date']]
        rec['r_prev1'] = r[i - 1]
        rec['r_next1'] = r[i + 1]
        lo = max(0, i - 21)
        seg = [x for x in r[lo:i] if x is not None]
        if len(seg) >= 5:
            m = sum(seg) / len(seg)
            rec['sigma_hat'] = math.sqrt(sum((x - m) ** 2 for x in seg) / (len(seg) - 1))
        else:
            rec['sigma_hat'] = full_sigma
        if i - 21 < 0 or i + 21 >= len(dates):
            rec['rv21_ok'] = False
        elif any(is_roll[j] for j in range(i - 21, i)) or any(is_roll[j] for j in range(i + 1, i + 22)):
            rec['rv21_ok'] = False
        else:
            if any(r[j] is None for j in range(i - 21, i)) or any(r[j] is None for j in range(i + 1, i + 22)):
                rec['rv21_ok'] = False
            else:
                rvb = sum(r[j] * r[j] for j in range(i - 21, i))
                rvf = sum(r[j] * r[j] for j in range(i + 1, i + 22))
                if rvb <= 0.0 or rvf <= 0.0:
                    rec['rv21_ok'] = False
                else:
                    rec['rv21_ok'] = True
                    rec['dlnrv21'] = math.log(rvf) - math.log(rvb)
        rec['fwd_abs_mean'] = sum(abs(r[j]) for j in range(i + 1, i + 6)) / 5.0


def compute_terciles(records):
    vals = np.array([rec['lnrv_back'] for rec in records])
    return (float(np.quantile(vals, 1.0 / 3.0, method='linear')),
            float(np.quantile(vals, 2.0 / 3.0, method='linear')))


def stratum_of(lnrv, q1, q2):
    if lnrv < q1:
        return 0
    if lnrv < q2:
        return 1
    return 2


# ---------------------------------------------------------------------------
# Greedy caliper matching (protocol 14)
# ---------------------------------------------------------------------------

def greedy_diff(magR, respR, magM, respM, c, ref_is_neg):
    """Per-pair response diffs (resp_neg - resp_pos). magR/magM pre-sorted
    ASCENDING by |r| with stable chronological order (tie-break)."""
    nR = len(magR)
    if nR == 0 or len(magM) == 0:
        return np.zeros(0, dtype=np.float64)
    used = np.zeros(len(magM), dtype=bool)
    out = np.empty(nR, dtype=np.float64)
    npairs = 0
    searchsorted = np.searchsorted
    nonzero = np.nonzero
    argmin = np.argmin
    for i in range(nR):
        x = magR[i]
        lo = searchsorted(magM, x - c, side='left')
        hi = searchsorted(magM, x + c, side='right')
        seg = used[lo:hi]
        if seg.all():
            continue
        w = nonzero(~seg)[0] + lo
        d = np.abs(magM[w] - x)
        k = w[int(argmin(d))]
        used[k] = True
        if ref_is_neg:
            out[npairs] = respR[i] - respM[k]
        else:
            out[npairs] = respM[k] - respR[i]
        npairs += 1
    return out[:npairs]


def split_stratum(mag, resp, neg, q1, q2, records):
    strata = np.array([stratum_of(r['lnrv_back'], q1, q2) for r in records], dtype=np.int8)
    out = {}
    for s in range(3):
        idx = np.nonzero(strata == s)[0]
        o = np.argsort(mag[idx], kind='stable')
        mag_s = mag[idx][o]
        resp_s = resp[idx][o]
        neg_s = neg[idx][o]
        out[s] = {'mag_neg': mag_s[neg_s], 'resp_neg': resp_s[neg_s],
                  'mag_pos': mag_s[~neg_s], 'resp_pos': resp_s[~neg_s],
                  'idx': idx}
    return out


def match_stratum(dat, c):
    n_neg = len(dat['mag_neg'])
    n_pos = len(dat['mag_pos'])
    if n_neg == 0 or n_pos == 0:
        return np.zeros(0, dtype=np.float64), n_neg, n_pos
    if not (np.isfinite(c) and c > 0):
        return np.zeros(0, dtype=np.float64), n_neg, n_pos
    ref_is_neg = (n_neg < n_pos)   # equal -> POS
    if ref_is_neg:
        diffs = greedy_diff(dat['mag_neg'], dat['resp_neg'],
                            dat['mag_pos'], dat['resp_pos'], c, True)
    else:
        diffs = greedy_diff(dat['mag_pos'], dat['resp_pos'],
                            dat['mag_neg'], dat['resp_neg'], c, False)
    return diffs, n_neg, n_pos


def market_stats(records, q1, q2):
    mag = np.abs(np.array([r['r'] for r in records], dtype=np.float64))
    resp = np.array([r['dlnrv'] for r in records], dtype=np.float64)
    neg = np.array([r['r'] < 0 for r in records], dtype=bool)
    stdata = split_stratum(mag, resp, neg, q1, q2, records)
    out = {}
    npairs_tot = 0
    for s in range(3):
        dat = stdata[s]
        mag_all = (np.concatenate([dat['mag_neg'], dat['mag_pos']])
                   if (len(dat['mag_neg']) or len(dat['mag_pos'])) else np.zeros(0))
        if len(mag_all) < 2:
            out[s] = {'npairs': 0, 'd_ms': None, 'unmatched_neg': len(dat['mag_neg']),
                      'unmatched_pos': len(dat['mag_pos']), 'balance': None, 'caliper': None}
            continue
        c = CALIPER_RATIO * float(np.std(mag_all, ddof=1))
        diffs, n_neg, n_pos = match_stratum(dat, c)
        npairs = len(diffs)
        npairs_tot += npairs
        d_ms = float(diffs.mean()) if npairs else None
        mn_neg = float(dat['mag_neg'].mean() if len(dat['mag_neg']) else math.nan)
        mn_pos = float(dat['mag_pos'].mean() if len(dat['mag_pos']) else math.nan)
        sd_neg = float(dat['mag_neg'].std(ddof=1)) if len(dat['mag_neg']) > 1 else math.nan
        sd_pos = float(dat['mag_pos'].std(ddof=1)) if len(dat['mag_pos']) > 1 else math.nan
        smd = ((mn_neg - mn_pos) / math.sqrt((sd_neg ** 2 + sd_pos ** 2) / 2.0)
               if (sd_neg and sd_pos and (sd_neg + sd_pos) > 0) else math.nan)
        out[s] = {'npairs': npairs, 'd_ms': d_ms, 'unmatched_neg': n_neg - npairs,
                  'unmatched_pos': n_pos - npairs,
                  'balance': {'mean_absr_neg': mn_neg, 'mean_absr_pos': mn_pos,
                              'sd_absr_neg': sd_neg, 'sd_absr_pos': sd_pos, 'smd': smd},
                  'caliper': c}
    return out, npairs_tot


def _match_pairs_with_dates(records, mag, resp, neg, strata, s, c):
    idx = np.nonzero(strata == s)[0]
    order = np.argsort(mag[idx], kind='stable')
    rec_i = idx[order]
    mag_s = mag[idx][order]
    resp_s = resp[idx][order]
    pairs = []
    if len(mag_s) < 2:
        return pairs
    ref_is_neg = (neg[rec_i].sum() < len(rec_i) - neg[rec_i].sum())
    if ref_is_neg:
        ref_mask = neg[rec_i]
        mt_mask = ~neg[rec_i]
    else:
        ref_mask = ~neg[rec_i]
        mt_mask = neg[rec_i]
    magR = mag_s[ref_mask]
    respR = resp_s[ref_mask]
    recR = rec_i[ref_mask]
    magM = mag_s[mt_mask]
    respM = resp_s[mt_mask]
    recM = rec_i[mt_mask]
    used = np.zeros(len(magM), dtype=bool)
    for i in range(len(magR)):
        x = magR[i]
        lo = int(np.searchsorted(magM, x - c, side='left'))
        hi = int(np.searchsorted(magM, x + c, side='right'))
        seg = used[lo:hi]
        if seg.all():
            continue
        w = np.nonzero(~seg)[0] + lo
        d = np.abs(magM[w] - x)
        k = w[int(np.argmin(d))]
        used[k] = True
        if ref_is_neg:
            pos_rec = recM[k]
            neg_rec = recR[i]
            neg_resp = respR[i]
            pos_resp = respM[k]
        else:
            pos_rec = recR[i]
            neg_rec = recM[k]
            neg_resp = respM[k]
            pos_resp = respR[i]
        pairs.append({'neg_date': records[neg_rec]['date'], 'pos_date': records[pos_rec]['date'],
                      'dlnrv_neg': float(neg_resp), 'dlnrv_pos': float(pos_resp),
                      'delta': float(neg_resp - pos_resp)})
    return pairs


def collect_pair_table(records, q1, q2):
    mag = np.abs(np.array([r['r'] for r in records], dtype=np.float64))
    resp = np.array([r['dlnrv'] for r in records], dtype=np.float64)
    neg = np.array([r['r'] < 0 for r in records], dtype=bool)
    strata = np.array([stratum_of(r['lnrv_back'], q1, q2) for r in records], dtype=np.int8)
    pairs = []
    for s in range(3):
        idx = np.nonzero(strata == s)[0]
        if len(idx) < 2:
            continue
        c = CALIPER_RATIO * float(np.std(mag[idx], ddof=1))
        if not (np.isfinite(c) and c > 0):
            continue
        for mp in _match_pairs_with_dates(records, mag, resp, neg, strata, s, c):
            mp['stratum'] = s
            pairs.append(mp)
    return pairs


# ---------------------------------------------------------------------------
# Bootstrap replicate (mirrors v1.2 rep_class_dm2 exactly)
# ---------------------------------------------------------------------------

def rep_cell(pack, starts):
    """Per-replicate draws (D_cell^b sampling, D_cell^b null) for a frozen cell
    pack and sampled circular-block start positions (protocol 17/18).

    Null draw = data-level construction on the SAME replicate pairs (matching
    is response-blind): pair null difference = raw difference - c_(m,s), which
    is mathematically identical to the registered shock-response +/-c_(m,s)/2
    transformation (protocol 18). Empty-stratum rule exactly as registered
    (mean over strata yielding >= 1 pair); a market with no paired strata
    contributes no draw; a replicate with no finite market draw is NaN."""
    ridx = (starts[:, None] + pack['ar']) % pack['T']
    counts = np.bincount(ridx.reshape(-1), minlength=pack['T'])
    dm_vals = []
    dn_vals = []
    for m in pack['markets']:
        rec = pack['m'][m]
        keep = counts[rec['tind']]
        sel = keep > 0
        if not sel.any():
            continue
        mag = np.repeat(rec['mag'][sel], keep[sel])
        rsp = np.repeat(rec['resp'][sel], keep[sel])
        st2 = np.repeat(rec['stratum'][sel], keep[sel])
        ng2 = np.repeat(rec['neg'][sel], keep[sel])
        s_diffs = []
        s_null = []
        for s in range(3):
            m2 = st2 == s
            if not m2.any():
                continue
            ni = ng2[m2]
            n_neg = int(ni.sum())
            n_pos = int(len(ni) - n_neg)
            if n_neg == 0 or n_pos == 0:
                continue
            c = rec['calipers'][s]
            if not (np.isfinite(c) and c > 0):
                continue
            mags = mag[m2]
            rsp2 = rsp[m2]
            o = np.argsort(mags, kind='stable')
            mags = mags[o]
            rsp2 = rsp2[o]
            ni2 = ni[o]
            mag_neg = mags[ni2]; resp_neg = rsp2[ni2]
            mag_pos = mags[~ni2]; resp_pos = rsp2[~ni2]
            if n_neg < n_pos:
                diffs = greedy_diff(mag_neg, resp_neg, mag_pos, resp_pos, c, True)
            else:
                diffs = greedy_diff(mag_pos, resp_pos, mag_neg, resp_neg, c, False)
            if len(diffs) > 0:
                mean_d = float(diffs.mean())
                s_diffs.append(mean_d)
                s_null.append(mean_d - rec['c_ms'][s])
        if s_diffs:
            dm_vals.append(float(np.mean(s_diffs)))
        if s_null:
            dn_vals.append(float(np.mean(s_null)))
    dm = float(np.mean(dm_vals)) if dm_vals else math.nan
    dn = float(np.mean(dn_vals)) if dn_vals else math.nan
    return dm, dn


# ---------------------------------------------------------------------------
# GJR/EGARCH + Engle-Ng (secondary 21.6/21.7; deterministic L-BFGS-B)
# ---------------------------------------------------------------------------

def engle_ng_sign_bias(r, z):
    rl = np.asarray(r)[:-1]
    z2 = np.asarray(z)[1:] ** 2
    out = {}
    lstsq = np.linalg.lstsq
    for name, xcol in [
        ('sign_bias', (rl < 0).astype(float)),
        ('negative_size_bias', (rl < 0).astype(float) * np.abs(rl)),
        ('positive_size_bias', (rl > 0).astype(float) * np.abs(rl)),
    ]:
        X = np.column_stack([np.ones(len(z2)), xcol])
        beta, _, _, _ = lstsq(X, z2, rcond=None)
        resid = z2 - X @ beta
        n = len(z2)
        p = X.shape[1]
        s2 = float((resid ** 2).sum()) / max(1, n - p)
        se = math.sqrt(s2 * float(np.linalg.inv(X.T @ X)[1, 1])) if (n - p) > 0 else math.nan
        out[name] = {'coef': float(beta[1]),
                     't': float(beta[1] / se) if se and se > 0 else math.nan,
                     'n': n}
    return out


def numeric_hessian(f, x0, eps=1e-4):
    x0 = np.asarray(x0, dtype=float)
    n = len(x0)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            xpp = x0.copy(); xpp[i] += eps; xpp[j] += eps
            xmm = x0.copy(); xmm[i] -= eps; xmm[j] -= eps
            xpm = x0.copy(); xpm[i] += eps; xpm[j] -= eps
            xmp = x0.copy(); xmp[i] -= eps; xmp[j] += eps
            H[i, j] = H[j, i] = (f(xpp) + f(xmm) - f(xpm) - f(xmp)) / (4 * eps * eps)
    return H


def _clamp(x, lo=-50.0, hi=50.0):
    return max(lo, min(hi, x))


def _logit(p):
    p = max(1e-6, min(1.0 - 1e-6, p))
    return math.log(p / (1.0 - p))


def _softplus_inv(y):
    y = max(1e-6, y)
    return math.log(math.expm1(y))


def _sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def _softplus(x):
    if x > 50.0:
        return x
    if x < -50.0:
        return math.exp(x)
    return math.log1p(math.exp(x))


def gjr_loglik(theta, r_in):
    a_alpha, logit_beta, g_gamma, lv = theta
    alpha = _sigmoid(a_alpha)
    beta = _sigmoid(logit_beta)
    gamma = g_gamma
    persist = alpha + beta + 0.5 * gamma
    if persist >= 0.9995:
        return 1e12
    omega = (1.0 - persist) * math.exp(lv)
    n = len(r_in)
    sig2 = np.empty(n)
    sig2[0] = math.exp(lv)
    r2 = r_in ** 2
    nz = r_in < 0
    for t in range(1, n):
        sig2[t] = omega + alpha * r2[t - 1] + gamma * r2[t - 1] * nz[t - 1] + beta * sig2[t - 1]
        if not math.isfinite(sig2[t]) or sig2[t] <= 1e-15:
            return 1e12
    return float(-0.5 * np.sum(np.log(sig2) + r2 / sig2))


def egarch_loglik(theta, r_in):
    v0, logit_beta, log_alpha, g_gamma = theta
    beta = _sigmoid(logit_beta)
    alpha = _softplus(log_alpha)
    gamma = g_gamma
    E = math.sqrt(2.0 / math.pi)
    omega = (1.0 - beta) * v0
    n = len(r_in)
    lsig2 = np.empty(n)
    z = np.empty(n)
    lsig2[0] = v0
    z[0] = r_in[0] / math.exp(0.5 * v0)
    for t in range(1, n):
        lsig2[t] = omega + beta * lsig2[t - 1] + alpha * (abs(z[t - 1]) - E) + gamma * z[t - 1]
        if not math.isfinite(lsig2[t]) or lsig2[t] > 700.0 or lsig2[t] < -700.0:
            return 1e12
        s2 = math.exp(lsig2[t])
        if not math.isfinite(s2):
            return 1e12
        z[t] = r_in[t] / math.sqrt(max(s2, 1e-300))
    r2 = r_in ** 2
    return float(-0.5 * np.sum(lsig2 + r2 / np.exp(np.clip(lsig2, -700.0, 700.0))))


def fit_garch(r_in):
    from scipy.optimize import minimize
    n = len(r_in)
    scale = float(np.std(r_in))
    scale = scale if scale > 0.0 else 1.0
    rz = r_in / scale
    var0 = max(float(np.var(rz)), 1e-14)
    lv0 = 0.0
    res = {}
    # ---------------- GJR(1,1)
    bounds = [(-8.0, 8.0), (-8.0, 8.0), (-0.3, 0.3), (-2.0, 2.0)]
    starts = [
        [_logit(0.05), _logit(0.90), 0.0, lv0],
        [_logit(0.03), _logit(0.93), 0.05, lv0],
        [_logit(0.08), _logit(0.88), -0.05, lv0],
        [_logit(0.04), _logit(0.90), -0.03, lv0],
    ]
    best = None
    for s0 in starts:
        r = minimize(gjr_loglik, s0, args=(rz,), method='L-BFGS-B', bounds=bounds,
                     options={'maxiter': 4000, 'ftol': 1e-12, 'gtol': 1e-6})
        if r.fun is not None and (best is None or r.fun < best.fun):
            best = r
    r1 = best
    a_alpha, b_beta, g_gamma, lv = r1.x
    alpha = _sigmoid(a_alpha)
    beta = _sigmoid(b_beta)
    gamma = g_gamma
    persist = alpha + beta + 0.5 * gamma
    persist = min(max(persist, 1e-12), 0.9995)
    omega = max((1.0 - persist) * math.exp(lv), 1e-16)
    at_bound = bool(abs(gamma - (-0.3)) < 1e-3 or abs(gamma - 0.3) < 1e-3)
    r2 = rz ** 2
    nz = rz < 0
    sig2 = np.empty(n)
    sig2[0] = math.exp(lv)
    for t in range(1, n):
        sig2[t] = omega + alpha * r2[t - 1] + gamma * r2[t - 1] * nz[t - 1] + beta * sig2[t - 1]
        sig2[t] = max(sig2[t], 1e-12)
    sig = np.sqrt(sig2)
    z = rz / sig
    H = numeric_hessian(lambda th: gjr_loglik(th, rz), r1.x)
    try:
        cov = np.linalg.inv(H)
        se_gamma = math.sqrt(abs(cov[2, 2])) if np.isfinite(cov[2, 2]) else math.nan
    except Exception:
        se_gamma = math.nan
    res['gjr'] = {'omega': float(omega * scale * scale), 'alpha': float(alpha), 'beta': float(beta),
                  'gamma': float(gamma), 'se_gamma': float(se_gamma),
                  'nll': float(r1.fun), 'converged': bool(r1.success),
                  'gamma_at_bound': at_bound,
                  'engle_ng': engle_ng_sign_bias(r_in, z)}
    # ---------------- EGARCH(1,1)
    bounds = [(-2.0, 2.0), (-8.0, 8.0), (-10.0, 8.0), (-0.3, 0.3)]
    starts = [
        [lv0, _logit(0.95), math.log(0.1), -0.05],
        [lv0, _logit(0.97), math.log(0.06), 0.02],
        [lv0, _logit(0.93), math.log(0.12), -0.08],
        [lv0, _logit(0.96), math.log(0.08), 0.06],
    ]
    best = None
    for s0 in starts:
        r = minimize(egarch_loglik, s0, args=(rz,), method='L-BFGS-B', bounds=bounds,
                     options={'maxiter': 4000, 'ftol': 1e-12, 'gtol': 1e-6})
        if r.fun is not None and (best is None or r.fun < best.fun):
            best = r
    r2_ = best
    v0, b_beta, a_alpha, g_gamma = r2_.x
    beta = _sigmoid(b_beta)
    alpha = _softplus(a_alpha)
    gamma = g_gamma
    at_bound = bool(abs(gamma - (-0.3)) < 1e-3 or abs(gamma - 0.3) < 1e-3)
    omega = float((1.0 - beta) * v0)
    E = math.sqrt(2.0 / math.pi)
    lsig2 = np.empty(n)
    z2 = np.empty(n)
    lsig2[0] = v0
    z2[0] = rz[0] / math.exp(0.5 * v0)
    for t in range(1, n):
        lsig2[t] = omega + beta * lsig2[t - 1] + alpha * (abs(z2[t - 1]) - E) + gamma * z2[t - 1]
        lsig2[t] = _clamp(lsig2[t], -700.0, 700.0)
        s2 = math.exp(lsig2[t])
        z2[t] = rz[t] / math.sqrt(max(s2, 1e-300))
    H = numeric_hessian(lambda th: egarch_loglik(th, rz), r2_.x)
    try:
        cov = np.linalg.inv(H)
        se_gamma = math.sqrt(abs(cov[2, 2])) if np.isfinite(cov[2, 2]) else math.nan
    except Exception:
        se_gamma = math.nan
    res['egarch'] = {'omega': float(omega), 'alpha': float(alpha), 'beta': float(beta),
                     'gamma': float(gamma), 'se_gamma': float(se_gamma),
                     'nll': float(r2_.fun), 'converged': bool(r2_.success),
                     'gamma_at_bound': at_bound}
    return res


# ---------------------------------------------------------------------------
# Holm + verdicts (protocol 19/23)
# ---------------------------------------------------------------------------

def holm(ps):
    ps = [1.0 if (p is None or (isinstance(p, float) and math.isnan(p))) else max(0.0, min(1.0, p))
          for p in ps]
    order = sorted(range(len(ps)), key=lambda i: (ps[i], i))
    adj = [None] * len(ps)
    run = 0.0
    for rank, i in enumerate(order, start=1):
        v = min(1.0, (len(ps) - rank + 1) * ps[i])
        run = max(run, v)
        adj[i] = run
    return adj


def sign(x):
    if x is None:
        return 0
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return 0
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def cell_verdict(cell, D_obs, p_holm, dm_by_market, eval_flags, other_info):
    """(verdict, n_evaluable). other_info = (n_ev_other, rel_sign_other) for
    cross-era cells; None for EQBROAD (cross-era EVIDENCE-LIMITED)."""
    ev = [m for m, flag in eval_flags.items() if flag and dm_by_market.get(m) is not None]
    n_ev = len(ev)
    if n_ev < MIN_EVALUABLE:
        return 'EVIDENCE-LIMITED/DESCRIPTIVE', n_ev
    reliable = p_holm is not None and not math.isnan(p_holm) and p_holm < ALPHA
    sg = sign(D_obs)
    frac_same = 0.0
    if sg != 0 and ev:
        frac_same = sum(1 for m in ev if sign(dm_by_market[m]) == sg) / float(len(ev))
    consistent = frac_same >= (2.0 / 3.0)
    sign_match = (sg == 1)   # classic prior D > 0 for every cell
    if cell in CROSS_ERA_CELLS:
        n_ev_other, rel_sign_other = other_info
        cross_ok = (n_ev_other >= MIN_EVALUABLE) and bool(rel_sign_other)
    else:
        cross_ok = True
    if reliable and sign_match and consistent and cross_ok:
        return 'SUPPORT', n_ev
    if reliable and (not sign_match or not consistent):
        return 'CONTRADICTION', n_ev
    return 'INCONCLUSIVE', n_ev


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUT, exist_ok=True)
    global _logfh
    _logfh = open(LOG_PATH, 'w', encoding=ENCODING)
    log(f'H01 EQUITY V1 CONTROLLED EXECUTION — protocol {PROTOCOL_VERSION}, serial, single invocation')
    log(f'python={sys.version.split()[0]} numpy={np.__version__}')
    try:
        import scipy
        log(f'scipy={scipy.__version__}')
    except Exception:
        log('scipy unavailable')

    import datetime
    ts_start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    resource_events = []

    # ----- protocol hash
    proto_sha = sha256(PROTOCOL_PATH)
    log(f'protocol sha256 = {proto_sha}')

    # ===== GATE 1: fingerprints =====
    gates = {}
    for fname, exp in FINGERPRINTS.items():
        if fname == 'sp_historical.csv':
            path = os.path.join(HPD, fname)
        elif fname == 'NYA_DATA.html':
            path = os.path.join(REPO, 'docs', fname)
        else:
            path = os.path.join(FREDDIR, fname)
        got = sha256(path)
        gates[fname] = (got == exp)
        log(f'  gate1 {fname}: {"OK" if got == exp else "MISMATCH"}')
    bad = [k for k, v in gates.items() if not v]
    if bad:
        raise SystemExit(f'GATE 1 (fingerprint) FAILED for: {bad}')
    log(f'[gate1] fingerprints OK ({len(FINGERPRINTS)} files)')

    # ===== GATE 2/3: universe + date range (implicit by construction) =====
    # ===== GATE 6: sp roll consistency =====
    val_rolls = {}
    with open(os.path.join(REPO, 'data', 'PER_MARKET_VALIDATION.csv'), newline='', encoding=ENCODING) as f:
        for row in csv.DictReader(f):
            val_rolls[row['root']] = int(row['n_rolls'])
    sp_daily_full = load_hpd('sp')
    gate7 = sum(1 for i in range(1, len(sp_daily_full['syms'])) if sp_daily_full['syms'][i] != sp_daily_full['syms'][i - 1])
    if gate7 != val_rolls.get('sp', -1):
        raise SystemExit(f'GATE 6 (roll consistency) FAILED: sp sym-changes={gate7} vs {val_rolls.get("sp")}')
    log(f'[gate6] sp roll consistency OK (n_rolls={gate7})')

    # ===== load market instances =====
    # market instance key: (symbol, era) — NDX/NCOMP appear in both eras
    instances = {}
    for cell, era, exposure, mkts in CELLS:
        win = (HIST_START, HIST_END) if era == 'HISTORICAL' else (CONT_START, CONT_END)
        for sym, src in mkts:
            key = (sym, era)
            if key in instances:
                continue
            if src == 'HPD':
                daily = load_hpd('sp', win=win)
            elif src == 'HTML':
                daily = load_nya(win=win)
            else:
                daily = load_fred(sym, win=win)
            rec, cnt = build_records(daily)
            add_secondary_stores(rec, daily)
            q1, q2 = compute_terciles(rec)
            instances[key] = {'sym': sym, 'era': era, 'source': src,
                              'daily': daily, 'records': rec, 'cnt': cnt,
                              'q1': q1, 'q2': q2}
            log(f'  load {sym}[{era}]: days={daily["n_rows"]} rows={daily["n_rows"]} '
                f'({daily["dates"][0]}..{daily["dates"][-1]}) eligible={len(rec)} excl={cnt}')

    # ----- observed per-market stats
    log('== primary statistic (observed) ==')
    per_market = {}
    for (sym, era), v in instances.items():
        st, npairs_tot = market_stats(v['records'], v['q1'], v['q2'])
        dvals = [st[s]['d_ms'] for s in range(3) if st[s]['d_ms'] is not None]
        d_m = float(np.mean(dvals)) if dvals else None
        evaluable = all(st[s]['npairs'] >= MIN_PAIRS for s in range(3))
        per_market[(sym, era)] = {'sym': sym, 'era': era, 'source': v['source'],
                                  'd_m': d_m, 'evaluable': evaluable,
                                  'pairs_per_stratum': {s: st[s]['npairs'] for s in range(3)},
                                  'c_stratum': {s: st[s]['d_ms'] for s in range(3)},
                                  'n_pairs_total': npairs_tot, 'eligible': len(v['records']),
                                  'exclusions': v['cnt'], 'strata': st,
                                  'terciles': {'q1': v['q1'], 'q2': v['q2']},
                                  'n_rolls': gate7 if v['source'] == 'HPD' else 0,
                                  'window': (v['daily']['dates'][0], v['daily']['dates'][-1])}
        log(f'  {sym}[{era}]: pairs={npairs_tot} evaluable={int(evaluable)} '
            f'd_m={"" if d_m is None else round(d_m, 6)}')

    # ----- cell observed statistics
    cell_results = {}
    for cell, era, exposure, mkts in CELLS:
        ev = [m for m in mkts if per_market[(m[0], era)]['evaluable']]
        vals = [per_market[(m[0], era)]['d_m'] for m in ev
                if per_market[(m[0], era)]['d_m'] is not None]
        D_obs = float(np.mean(vals)) if vals else None
        cell_results[cell] = {'cell': cell, 'era': era, 'exposure': exposure,
                              'markets': [m[0] for m in mkts],
                              'evaluable_markets': [m[0] for m in ev],
                              'n_evaluable': len(ev), 'D_obs': D_obs,
                              'per_market_dm': {m[0]: per_market[(m[0], era)]['d_m'] for m in mkts}}
        log(f'  {cell}: evaluable={len(ev)} D_obs={D_obs}')

    # ----- bootstrap (single master RNG, serial, fixed cell order)
    log(f'== synchronized cell-level circular calendar-block bootstrap '
        f'(B={B_REPL}, L={L_BLOCK}, seed={SEED}) — serial, single invocation ==')
    rng = np.random.default_rng(SEED)
    repl = {}
    for (sym, era), v in instances.items():
        recs = v['records']
        mag = np.abs(np.array([x['r'] for x in recs], dtype=np.float64))
        resp = np.array([x['dlnrv'] for x in recs], dtype=np.float64)
        stv = np.array([stratum_of(x['lnrv_back'], v['q1'], v['q2']) for x in recs], dtype=np.int8)
        ng = np.array([x['r'] < 0 for x in recs], dtype=bool)
        dates = [x['date'] for x in recs]
        cal = {}
        for s in range(3):
            idx = np.nonzero(stv == s)[0]
            if len(idx) < 2:
                cal[s] = math.nan
            else:
                cal[s] = CALIPER_RATIO * float(np.std(mag[idx], ddof=1))
        repl[(sym, era)] = {'mag': mag, 'resp': resp, 'stratum': stv, 'neg': ng,
                            'dates': dates, 'calipers': cal}

    packs = {}
    draws_all = {}
    bootstrap = {}
    for cell, era, exposure, mkts in CELLS:
        ev = [m[0] for m in mkts if per_market[(m[0], era)]['evaluable']]
        if not ev:
            bootstrap[cell] = {'T': None, 'nblocks': None, 'p_null': math.nan,
                               'ci95': [math.nan, math.nan], 'n_draws': 0,
                               'null_mean': None, 'sampling_mean': None,
                               'D_cell_star': [], 'D_cell_null': []}
            draws_all[cell] = None
            log(f'  {cell}: no evaluable markets -> no bootstrap draws')
            continue
        union_dates = set()
        for m in mkts:
            union_dates.update(repl[(m[0], era)]['dates'])
        union_dates = sorted(union_dates)
        tind = {d: k for k, d in enumerate(union_dates)}
        T = len(union_dates)
        nblocks = int(math.ceil(T / float(L_BLOCK)))
        for m in mkts:
            repl[(m[0], era)]['tind'] = np.array([tind[d] for d in repl[(m[0], era)]['dates']],
                                                 dtype=np.int64)
        pm = {}
        for sym in ev:
            rec = repl[(sym, era)]
            c_ms = per_market[(sym, era)]['c_stratum']
            if any(c is None for c in c_ms.values()):
                raise SystemExit(f'STOP (protocol 22): evaluable market {sym}[{era}] has undefined c_(m,s)')
            pm[sym] = {k: rec[k] for k in ('mag', 'resp', 'stratum', 'neg', 'tind', 'calipers')}
            pm[sym]['c_ms'] = {s: float(c_ms[s]) for s in range(3)}
        packs[cell] = {'cell': cell, 'markets': ev, 'm': pm, 'T': T, 'nblocks': nblocks,
                       'ar': np.arange(L_BLOCK, dtype=np.int64)}
        draws_all[cell] = np.full((B_REPL, 2), math.nan)
        log(f'  {cell}: T={T} nblocks={nblocks} evaluable={ev}')

    peak_mb = 0.0
    for cell in CELL_ORDER:
        if packs.get(cell) is None:
            continue
        pk = packs[cell]
        T = pk['T']
        nblocks = pk['nblocks']
        arr = draws_all[cell]
        for b in range(B_REPL):
            starts = rng.integers(0, T, size=nblocks)
            dm, dn = rep_cell(pk, starts)
            arr[b, 0] = dm
            arr[b, 1] = dn
            if (b + 1) % 2000 == 0 or (b + 1) == B_REPL:
                mb = mem_rss_mb()
                peak_mb = max(peak_mb, mb)
                log(f'  {cell}: b={b + 1}/{B_REPL} rss={mb:.0f}MB')

    # ----- p-values, CI, Holm
    raw_ps = {}
    ci = {}
    for cell in CELL_ORDER:
        obs = cell_results[cell]['D_obs']
        if draws_all.get(cell) is None:
            raw_ps[cell] = math.nan
            ci[cell] = [math.nan, math.nan]
            continue
        d2 = draws_all[cell]
        raw = d2[:, 0]
        null = d2[:, 1]
        finite_raw = raw[np.isfinite(raw)]
        finite_null = null[np.isfinite(null)]
        if obs is not None and finite_null.size:
            count = int((np.abs(finite_null) >= abs(obs)).sum())
            p = (1.0 + count) / (B_REPL + 1.0)
        else:
            p = math.nan
        raw_ps[cell] = p
        if finite_raw.size:
            ci[cell] = [float(np.percentile(finite_raw, 2.5)), float(np.percentile(finite_raw, 97.5))]
        else:
            ci[cell] = [math.nan, math.nan]
        bootstrap[cell] = {'T': packs.get(cell, {}).get('T'),
                           'nblocks': packs.get(cell, {}).get('nblocks'),
                           'p_null': p, 'ci95': ci[cell],
                           'n_draws': int(finite_null.size),
                           'null_mean': float(finite_null.mean()) if finite_null.size else None,
                           'sampling_mean': float(finite_raw.mean()) if finite_raw.size else None,
                           'D_cell_star': raw.tolist(), 'D_cell_null': null.tolist()}
        log(f'  {cell}: p_null={p:.5f} CI={ci[cell][0]:.5f}..{ci[cell][1]:.5f} '
            f'null_mean={bootstrap[cell]["null_mean"]}')

    adj = holm([raw_ps[c] for c in CELL_ORDER])
    holm_res = {c: adj[i] for i, c in enumerate(CELL_ORDER)}
    log('== Holm step-down (4-member family) ==')
    for c in CELL_ORDER:
        log(f'  {c}: p_raw={raw_ps[c]:.5f} p_holm={holm_res[c]:.5f}')

    # ----- verdicts
    rel_sign = {}
    n_ev_any = {}
    for cell in CELL_ORDER:
        n_ev_any[cell] = cell_results[cell]['n_evaluable']
        D = cell_results[cell]['D_obs']
        p = holm_res[cell]
        rel = (p is not None and not math.isnan(p) and p < ALPHA)
        rel_sign[cell] = rel and (sign(D) == 1)
    verdicts = {}
    for cell in CELL_ORDER:
        if cell in CROSS_ERA_CELLS:
            other = CROSS_ERA_CELLS[cell]
            other_info = (n_ev_any.get(other, 0), rel_sign.get(other, False))
        else:
            other_info = None
        v, n_ev = cell_verdict(cell, cell_results[cell]['D_obs'], holm_res[cell],
                               cell_results[cell]['per_market_dm'],
                               {m[0]: per_market[(m[0], cell_results[cell]['era'])]['evaluable']
                                for m in CELLS[[c[0] for c in CELLS].index(cell)][3]},
                               other_info)
        ev = [m[0] for m in CELLS[[c[0] for c in CELLS].index(cell)][3]
              if per_market[(m[0], cell_results[cell]['era'])]['evaluable']]
        sg = sign(cell_results[cell]['D_obs'])
        frac = None
        if sg != 0 and ev:
            frac = round(sum(1 for m in ev if sign(per_market[(m, cell_results[cell]['era'])]['d_m']) == sg)
                         / float(len(ev)), 4)
        verdicts[cell] = {'cell': cell, 'D_obs': cell_results[cell]['D_obs'],
                          'p_raw': raw_ps[cell], 'p_holm': holm_res[cell],
                          'ci95': ci[cell], 'n_evaluable_markets': n_ev,
                          'evaluable_markets': ev,
                          'consistency_frac': frac, 'verdict': v}
        log(f'  {cell}: D={cell_results[cell]["D_obs"]} p_holm={holm_res[cell]:.4f} -> {v}')

    strong_replication = all(verdicts[c]['verdict'] == 'SUPPORT' for c in ('EQTECH_L1', 'EQTECH_L2'))
    log(f'EQTECH strong replication (both eras SUPPORT): {strong_replication}')

    # ===== secondaries (protocol 21; NON-RESCUING) =====
    log('== secondary analyses (protocol 21; non-rescuing) ==')
    secondaries = {}

    # 21.1 1-day horizon (primary pairs)
    pair_cache = {}
    for (sym, era), v in instances.items():
        pair_cache[(sym, era)] = collect_pair_table(v['records'], v['q1'], v['q2'])
    all_pairs = []
    for (sym, era), pairs in pair_cache.items():
        for p in pairs:
            p['market'] = sym
            p['era'] = era
            all_pairs.append(p)
    log(f'  [21.1/21.2/21.4] total matched pairs = {len(all_pairs)}')

    def sec1(records, pairs):
        rmap = {r['date']: r for r in records}
        sm = {}
        for s in range(3):
            diffs = []
            for p in pairs:
                if p['stratum'] != s:
                    continue
                nr, pr = rmap.get(p['neg_date']), rmap.get(p['pos_date'])
                if nr is None or pr is None:
                    continue
                if nr['r_prev1'] == 0 or nr['r_next1'] == 0 or pr['r_prev1'] == 0 or pr['r_next1'] == 0:
                    continue
                nv = math.log(nr['r_next1'] ** 2) - math.log(nr['r_prev1'] ** 2)
                pv = math.log(pr['r_next1'] ** 2) - math.log(pr['r_prev1'] ** 2)
                diffs.append(nv - pv)
            sm[s] = {'npairs': len(diffs), 'mean': float(np.mean(diffs)) if diffs else None}
        return sm

    sec1_by_mkt = {k: sec1(v['records'], pair_cache[k]) for k, v in instances.items()}

    # 21.2 21-day horizon
    sec21_by_mkt = {}
    for k, v in instances.items():
        rmap = {r['date']: r for r in v['records']}
        sm = {}
        for s in range(3):
            diffs = []
            for p in pair_cache[k]:
                if p['stratum'] != s:
                    continue
                nr, pr = rmap.get(p['neg_date']), rmap.get(p['pos_date'])
                if nr is None or pr is None:
                    continue
                if nr.get('rv21_ok') and pr.get('rv21_ok'):
                    diffs.append(nr['dlnrv21'] - pr['dlnrv21'])
            sm[s] = {'npairs': len(diffs), 'mean': float(np.mean(diffs)) if diffs else None}
        sec21_by_mkt[k] = sm

    # 21.4 absolute-return response
    sec4_by_mkt = {}
    for k, v in instances.items():
        rmap = {r['date']: r for r in v['records']}
        sm = {}
        for s in range(3):
            diffs = []
            for p in pair_cache[k]:
                if p['stratum'] != s:
                    continue
                nr, pr = rmap.get(p['neg_date']), rmap.get(p['pos_date'])
                if nr is not None and pr is not None:
                    diffs.append(nr['fwd_abs_mean'] - pr['fwd_abs_mean'])
            sm[s] = {'npairs': len(diffs), 'mean': float(np.mean(diffs)) if diffs else None}
        sec4_by_mkt[k] = sm

    def _cell_agg(d_by_mkt, ev_only=True):
        out = {}
        for cell, era, exposure, mkts in CELLS:
            ev = [m[0] for m in mkts if per_market[(m[0], era)]['evaluable']]
            dm_list = []
            for sym in ev:
                vals = [d_by_mkt[(sym, era)][s]['mean'] for s in range(3)
                        if d_by_mkt[(sym, era)][s]['mean'] is not None]
                if vals:
                    dm_list.append(float(np.mean(vals)))
            out[cell] = {'D': float(np.mean(dm_list)) if dm_list else None,
                         'n_markets': len(dm_list)}
        return out

    sec1_class = _cell_agg(sec1_by_mkt)
    sec21_class = _cell_agg(sec21_by_mkt)
    sec4_class = _cell_agg(sec4_by_mkt)
    secondaries['21.1_1day'] = {'by_market': {f'{k[0]}[{k[1]}]': sec1_by_mkt[k] for k in instances},
                                'by_cell': sec1_class}
    secondaries['21.2_21day'] = {'by_market': {f'{k[0]}[{k[1]}]': sec21_by_mkt[k] for k in instances},
                                 'by_cell': sec21_class}
    secondaries['21.4_absreturn'] = {'by_market': {f'{k[0]}[{k[1]}]': sec4_by_mkt[k] for k in instances},
                                     'by_cell': sec4_class}

    # 21.3 standardized-shock matching
    log('  [21.3] standardized-shock matching...')
    sec3_by_mkt = {}
    for k, v in instances.items():
        recs = v['records']
        valid = [(i, x) for i, x in enumerate(recs) if x.get('sigma_hat') and x['sigma_hat'] > 0]
        if len(valid) < 2:
            sec3_by_mkt[k] = {'d_m': None}
            continue
        mag_s = np.abs(np.array([x['r'] / x['sigma_hat'] for _, x in valid], dtype=np.float64))
        resp = np.array([x['dlnrv'] for _, x in valid], dtype=np.float64)
        neg = np.array([x['r'] < 0 for _, x in valid], dtype=bool)
        stv = np.array([stratum_of(x['lnrv_back'], v['q1'], v['q2']) for _, x in valid], dtype=np.int8)
        s_diffs = []
        for s in range(3):
            idx = np.nonzero(stv == s)[0]
            if len(idx) < 2:
                continue
            o = np.argsort(mag_s[idx], kind='stable')
            mags = mag_s[idx][o]; rsp = resp[idx][o]; ni = neg[idx][o]
            mn = mags[ni]; rn = rsp[ni]; mp = mags[~ni]; rp = rsp[~ni]
            n_neg, n_pos = len(mn), len(mp)
            if n_neg == 0 or n_pos == 0:
                continue
            c = CALIPER_RATIO * float(np.std(mag_s[idx], ddof=1))
            if not (np.isfinite(c) and c > 0):
                continue
            if n_neg < n_pos:
                diffs = greedy_diff(mn, rn, mp, rp, c, True)
            else:
                diffs = greedy_diff(mp, rp, mn, rn, c, False)
            if len(diffs):
                s_diffs.append(float(diffs.mean()))
        sec3_by_mkt[k] = {'d_m': float(np.mean(s_diffs)) if s_diffs else None}
    sec3_class = {}
    for cell, era, exposure, mkts in CELLS:
        ev = [m[0] for m in mkts if per_market[(m[0], era)]['evaluable']]
        dm_list = [sec3_by_mkt[(m, era)]['d_m'] for m in ev if sec3_by_mkt[(m, era)]['d_m'] is not None]
        sec3_class[cell] = {'D': float(np.mean(dm_list)) if dm_list else None,
                            'n_markets': len(dm_list)}
    secondaries['21.3_standardized'] = {'by_market': {f'{k[0]}[{k[1]}]': sec3_by_mkt[k] for k in instances},
                                        'by_cell': sec3_class}

    # 21.5 winsorization sensitivity (cap |r| at market 95th pct)
    log('  [21.5] winsorization sensitivity...')
    win_by_mkt = {}
    for k, v in instances.items():
        recs = v['records']
        mag0 = np.abs(np.array([x['r'] for x in recs], dtype=np.float64))
        cap = float(np.percentile(mag0, 95))
        magw = np.minimum(mag0, cap)
        resp = np.array([x['dlnrv'] for x in recs], dtype=np.float64)
        neg = np.array([x['r'] < 0 for x in recs], dtype=bool)
        stv = np.array([stratum_of(x['lnrv_back'], v['q1'], v['q2']) for x in recs], dtype=np.int8)
        s_diffs = []
        for s in range(3):
            idx = np.nonzero(stv == s)[0]
            if len(idx) < 2:
                continue
            o = np.argsort(magw[idx], kind='stable')
            mags = magw[idx][o]; rsp = resp[idx][o]; ni = neg[idx][o]
            mn = mags[ni]; rn = rsp[ni]; mp = mags[~ni]; rp = rsp[~ni]
            n_neg, n_pos = len(mn), len(mp)
            if n_neg == 0 or n_pos == 0:
                continue
            c = CALIPER_RATIO * float(np.std(magw[idx], ddof=1))
            if not (np.isfinite(c) and c > 0):
                continue
            if n_neg < n_pos:
                diffs = greedy_diff(mn, rn, mp, rp, c, True)
            else:
                diffs = greedy_diff(mp, rp, mn, rn, c, False)
            if len(diffs):
                s_diffs.append(float(diffs.mean()))
        win_by_mkt[k] = {'d_m': float(np.mean(s_diffs)) if s_diffs else None, 'cap': cap}
    win_class = {}
    for cell, era, exposure, mkts in CELLS:
        ev = [m[0] for m in mkts if per_market[(m[0], era)]['evaluable']]
        dm_list = [win_by_mkt[(m, era)]['d_m'] for m in ev if win_by_mkt[(m, era)]['d_m'] is not None]
        win_class[cell] = {'D': float(np.mean(dm_list)) if dm_list else None,
                           'n_markets': len(dm_list)}
    secondaries['21.5_winsorization'] = {'by_market': {f'{k[0]}[{k[1]}]': win_by_mkt[k] for k in instances},
                                         'by_cell': win_class}

    # 21.6/21.7 GJR/EGARCH + Engle-Ng
    log('  [21.6/21.7] GJR/EGARCH + Engle-Ng...')
    garch = {}
    for (sym, era), v in instances.items():
        d = v['daily']
        r_in = np.array([x for k, x in enumerate(d['r']) if x is not None and not d['is_roll'][k]],
                        dtype=np.float64)
        garch[f'{sym}[{era}]'] = fit_garch(r_in)
        g = garch[f'{sym}[{era}]']
        log(f'    {sym}[{era}]: GJR gamma={g["gjr"]["gamma"]:.4f} EGARCH gamma={g["egarch"]["gamma"]:.4f}')
    secondaries['21.6_21.7_gjr_egarch_engle_ng'] = garch

    # 21.8 common-window sensitivity (1986-01-02 .. 2002-10-01)
    log(f'  [21.8] common-window sensitivity {COMMON_WIN[0]}..{COMMON_WIN[1]}...')
    cw_pm = {}
    for (sym, era), v in instances.items():
        if era != 'HISTORICAL':
            continue
        if v['source'] == 'HPD':
            daily = load_hpd('sp', win=COMMON_WIN)
        elif v['source'] == 'HTML':
            daily = load_nya(win=COMMON_WIN)
        else:
            daily = load_fred(sym, win=COMMON_WIN)
        rec, _ = build_records(daily)
        q1, q2 = compute_terciles(rec)
        st, npairs = market_stats(rec, q1, q2)
        dvals = [st[s]['d_ms'] for s in range(3) if st[s]['d_ms'] is not None]
        d_m = float(np.mean(dvals)) if dvals else None
        evaluable = all(st[s]['npairs'] >= MIN_PAIRS for s in range(3))
        cw_pm[(sym, era)] = {'d_m': d_m, 'evaluable': evaluable,
                             'pairs_per_stratum': {s: st[s]['npairs'] for s in range(3)},
                             'n_eligible': len(rec)}
    cw_class = {}
    for cell, era, exposure, mkts in CELLS:
        if era != 'HISTORICAL':
            continue
        ev = [m[0] for m in mkts if cw_pm[(m[0], era)]['evaluable']]
        vals = [cw_pm[(m, era)]['d_m'] for m in ev if cw_pm[(m, era)]['d_m'] is not None]
        cw_class[cell] = {'D': float(np.mean(vals)) if vals else None,
                          'n_evaluable': len(ev),
                          'per_market_dm': {m[0]: cw_pm[(m[0], era)]['d_m'] for m in mkts}}
    secondaries['21.8_common_window'] = {'by_market': {f'{k[0]}[{k[1]}]': cw_pm[k] for k in cw_pm},
                                         'by_cell': cw_class}

    # 21.9 MT5 cross-provider reference (USATECHIDXUSD, contemporary; descriptive)
    log('  [21.9] MT5 cross-provider reference USATECHIDXUSD...')
    try:
        m5 = load_m1_daily('USATECHIDXUSD')
        win = (CONT_START, CONT_END)
        idx = [i for i, d in enumerate(m5['dates']) if win[0] <= d <= win[1]]
        m5d = {k: [v2[i] for i in idx] for k, v2 in m5.items() if isinstance(v2, list)}
        m5d['root'] = m5['root']
        m5d['n_rows'] = len(idx)
        m5r, _ = build_records(m5d)
        m5q1, m5q2 = compute_terciles(m5r)
        st5, np5 = market_stats(m5r, m5q1, m5q2)
        dvals5 = [st5[s]['d_ms'] for s in range(3) if st5[s]['d_ms'] is not None]
        d_m5 = float(np.mean(dvals5)) if dvals5 else None
        secondaries['21.9_mt5_usatechidxusd'] = {
            'd_m': d_m5, 'eligible': len(m5r), 'n_pairs_total': np5,
            'pairs_per_stratum': {s: st5[s]['npairs'] for s in range(3)},
            'window': (m5d['dates'][0], m5d['dates'][-1]),
            'caveat': 'different provider (MT5), different instrument (CFD-style); '
                      'descriptive cross-provider reference only, never a primary market'}
        log(f'    USATECHIDXUSD: eligible={len(m5r)} d_m={d_m5}')
    except Exception as e:
        secondaries['21.9_mt5_usatechidxusd'] = {'error': str(e)}
        log(f'    USATECHIDXUSD reference unavailable: {e}')

    # 21.10 cross-source futures/cash context (documentary; no recomputation)
    secondaries['21.10_futures_cash_context'] = {
        'source': 'H01_EQUITY_DATA_ACQUISITION_V1.md (documentary; not recomputed inside '
                  'the experiment from restricted sources)',
        'context': 'sp (S&P 500 futures, HPD) vs cash S&P 500 (^GSPC): daily-return '
                   'corr ~= 0.95, median |diff| ~= 16 bp, 1987-10-19 and 1982-09-22 '
                   'divergences verified as genuine futures/cash behavior. Recorded as '
                   'interpretation context for EQBROAD_L1 only; cannot alter any verdict.'}

    # ===== write artifacts =====
    log('== writing artifacts ==')
    series_dir = os.path.join(OUT, 'daily_series')
    os.makedirs(series_dir, exist_ok=True)
    for (sym, era), v in instances.items():
        tag = f'{sym}_{"historical" if era == "HISTORICAL" else "contemporary"}'
        d = v['daily']
        with open(os.path.join(series_dir, f'{tag}.csv'), 'w', newline='', encoding=ENCODING) as f:
            w = csv.writer(f)
            if v['source'] == 'HPD':
                w.writerow(['date', 'sym', 'close', 'adj_close', 'is_roll_day', 'log_return'])
                for i in range(len(d['dates'])):
                    w.writerow([d['dates'][i], d['syms'][i], repr(d['closes'][i]),
                                repr(d['adj'][i]), 1 if d['is_roll'][i] else 0,
                                '' if d['r'][i] is None else repr(d['r'][i])])
            else:
                w.writerow(['date', 'close', 'log_return'])
                for i in range(len(d['dates'])):
                    w.writerow([d['dates'][i], repr(d['closes'][i]),
                                '' if d['r'][i] is None else repr(d['r'][i])])

    with open(os.path.join(OUT, 'matched_pairs_H01_EQ_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['cell', 'era', 'market', 'stratum', 'neg_date', 'pos_date',
                    'dlnrv_neg', 'dlnrv_pos', 'delta'])
        cell_of = {}
        for cell, era, exposure, mkts in CELLS:
            for sym, src in mkts:
                cell_of[(sym, era)] = cell
        for p in all_pairs:
            w.writerow([cell_of[(p['market'], p['era'])], p['era'], p['market'],
                        p['stratum'], p['neg_date'], p['pos_date'],
                        repr(p['dlnrv_neg']), repr(p['dlnrv_pos']), repr(p['delta'])])

    with open(os.path.join(OUT, 'per_market_stats_H01_EQ_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['cell', 'era', 'market', 'source', 'evaluable', 'eligible', 'n_rolls',
                    'window_start', 'window_end',
                    'pairs_low', 'pairs_mid', 'pairs_high',
                    'd_low', 'd_mid', 'd_high', 'd_m',
                    'smd_low', 'smd_mid', 'smd_high'])
        for cell, era, exposure, mkts in CELLS:
            for sym, src in mkts:
                pm = per_market[(sym, era)]
                st = pm['strata']
                w.writerow([cell, era, sym, src, int(pm['evaluable']), pm['eligible'],
                            pm['n_rolls'], pm['window'][0], pm['window'][1],
                            st[0]['npairs'], st[1]['npairs'], st[2]['npairs'],
                            '' if st[0]['d_ms'] is None else repr(st[0]['d_ms']),
                            '' if st[1]['d_ms'] is None else repr(st[1]['d_ms']),
                            '' if st[2]['d_ms'] is None else repr(st[2]['d_ms']),
                            '' if pm['d_m'] is None else repr(pm['d_m']),
                            '' if st[0]['balance'] is None else repr(st[0]['balance']['smd']),
                            '' if st[1]['balance'] is None else repr(st[1]['balance']['smd']),
                            '' if st[2]['balance'] is None else repr(st[2]['balance']['smd'])])

    with open(os.path.join(OUT, 'class_stats_H01_EQ_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['cell', 'exposure', 'era', 'markets', 'evaluable_markets', 'n_evaluable',
                    'D_cell', 'ci_lo', 'ci_hi', 'p_null', 'p_holm', 'consistency_frac', 'verdict'])
        for cell in CELL_ORDER:
            v = verdicts[cell]
            w.writerow([cell, cell_results[cell]['exposure'], cell_results[cell]['era'],
                        ' '.join(cell_results[cell]['markets']),
                        ' '.join(v['evaluable_markets']), v['n_evaluable_markets'],
                        '' if v['D_obs'] is None else repr(v['D_obs']),
                        '' if v['ci95'][0] is None or (isinstance(v['ci95'][0], float) and math.isnan(v['ci95'][0])) else repr(v['ci95'][0]),
                        '' if v['ci95'][1] is None or (isinstance(v['ci95'][1], float) and math.isnan(v['ci95'][1])) else repr(v['ci95'][1]),
                        '' if v['p_raw'] is None or (isinstance(v['p_raw'], float) and math.isnan(v['p_raw'])) else repr(v['p_raw']),
                        '' if v['p_holm'] is None or (isinstance(v['p_holm'], float) and math.isnan(v['p_holm'])) else repr(v['p_holm']),
                        v['consistency_frac'], v['verdict']])

    with open(os.path.join(OUT, 'bootstrap_replicates_H01_EQ_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['cell', 'replicate', 'D_cell_star', 'D_cell_null'])
        for cell in CELL_ORDER:
            if draws_all.get(cell) is None:
                continue
            arr = draws_all[cell]
            for b in range(B_REPL):
                w.writerow([cell, b + 1, repr(arr[b, 0]), repr(arr[b, 1])])

    ts_end = datetime.datetime.now(datetime.timezone.utc).isoformat()
    duration_s = time.time() - T0

    results = {
        'protocol': {'version': PROTOCOL_VERSION, 'sha256': proto_sha,
                     'path': PROTOCOL_PATH},
        'execution': {'single_invocation': True, 'workers': 1,
                      'resource_mode': 'serial (conservative)',
                      'started_utc': ts_start, 'ended_utc': ts_end,
                      'duration_seconds': round(duration_s, 2),
                      'peak_rss_mb': round(peak_mb, 1),
                      'resource_pressure_events': resource_events,
                      'priority': 'below-normal (set by launcher)'},
        'params': {'seed': SEED, 'B': B_REPL, 'L': L_BLOCK,
                   'caliper_ratio': CALIPER_RATIO, 'min_pairs': MIN_PAIRS,
                   'min_evaluable': MIN_EVALUABLE, 'alpha': ALPHA,
                   'era_windows': {'historical': [HIST_START, HIST_END],
                                   'contemporary': [CONT_START, CONT_END]}},
        'gates': {'fingerprints': gates,
                  'sp_roll_count': gate7,
                  'fred_holiday_rows': FRED_HOLIDAY_COUNTS,
                  'all_pass': True},
        'daily_series': {f'{k[0]}[{k[1]}]': {
            'rows': v['daily']['n_rows'],
            'first': v['daily']['dates'][0], 'last': v['daily']['dates'][-1],
            'eligible': len(v['records']), 'exclusions': v['cnt']}
            for k, v in instances.items()},
        'per_market': {f'{k[0]}[{k[1]}]': {
            'd_m': per_market[k]['d_m'], 'evaluable': per_market[k]['evaluable'],
            'pairs_per_stratum': per_market[k]['pairs_per_stratum'],
            'c_stratum': {str(s): per_market[k]['c_stratum'][s] for s in range(3)},
            'terciles': per_market[k]['terciles'],
            'balance': {str(s): per_market[k]['strata'][s]['balance'] for s in range(3)},
            'n_pairs_total': per_market[k]['n_pairs_total'],
            'eligible': per_market[k]['eligible'],
            'n_rolls': per_market[k]['n_rolls']}
            for k in per_market},
        'cells': {cell: {
            'exposure': cell_results[cell]['exposure'],
            'era': cell_results[cell]['era'],
            'markets': cell_results[cell]['markets'],
            'evaluable_markets': cell_results[cell]['evaluable_markets'],
            'D_obs': cell_results[cell]['D_obs'],
            'per_market_dm': cell_results[cell]['per_market_dm'],
            'p_null': raw_ps[cell], 'p_holm': holm_res[cell],
            'ci95': ci[cell], 'n_draws': bootstrap.get(cell, {}).get('n_draws', 0),
            'null_mean': bootstrap.get(cell, {}).get('null_mean'),
            'sampling_mean': bootstrap.get(cell, {}).get('sampling_mean'),
            'verdict': verdicts[cell]['verdict'],
            'consistency_frac': verdicts[cell]['consistency_frac']}
            for cell in CELL_ORDER},
        'strong_replication_eqtech': strong_replication,
        'secondaries': secondaries,
        'hol_missing_p_treated_as_1': True,
        'v11_firewall': 'H01 v1.1 remains CONFIRMATORY INFERENCE INVALID / '
                        'SCIENTIFIC RESULT UNADJUDICATED; no v1.1 p-value is used '
                        'or mixed with this result.',
    }

    with open(os.path.join(OUT, 'results_H01_EQ_V1.json'), 'w', encoding=ENCODING) as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    import platform
    meta = {
        'experiment': 'H01 EQUITY VOLATILITY-ASYMMETRY V1',
        'protocol_version': PROTOCOL_VERSION,
        'protocol_sha256': proto_sha,
        'protocol_path': PROTOCOL_PATH,
        'final_clearance': 'PASS - APPROVED FOR EXECUTION '
                           '(final independent H01 Equity V1.1 execution-clearance audit)',
        'execution': results['execution'],
        'params': results['params'],
        'python': {'version': sys.version.split()[0], 'executable': sys.executable,
                   'platform': platform.platform()},
        'libraries': {'numpy': np.__version__},
        'inputs': {'fingerprints': FINGERPRINTS,
                   'fred_holiday_placeholder_representation':
                       'empty value field in frozen snapshot (registered count '
                       '96/96/362/487 verified at execution; protocol 8.1)',
                   'sp_price_field': 'continuous ratio-back-adjusted adj_close '
                                     '(protocol 7/8; no raw-close substitution)',
                   'historical_window_reading':
                       'all historical-layer series restricted to the registered '
                       'era window 1982-04-21..2002-10-01 (protocol 5 cell table); '
                       'NDX begins 1986-01-02 within it'},
        'seed': SEED, 'B': B_REPL, 'L': L_BLOCK,
        'licensing': {
            'HPD sp': 'PENDING',
            'FRED platform access': 'CLEAR (attribution required)',
            'FRED underlying index archival rights': 'PENDING (S&P DJI / Nasdaq)',
            'permission_requests': 'PREPARED, NOT SENT'},
    }
    try:
        import scipy
        meta['libraries']['scipy'] = scipy.__version__
    except Exception:
        pass
    with open(os.path.join(OUT, 'experiment_metadata_H01_EQ_V1.json'), 'w', encoding=ENCODING) as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    log(f'== DONE == duration={duration_s:.1f}s peak_rss={peak_mb:.0f}MB')
    _logfh.close()


if __name__ == '__main__':
    main()
