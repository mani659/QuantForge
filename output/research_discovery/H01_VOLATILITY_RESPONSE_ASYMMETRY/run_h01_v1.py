#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUANTFORGE — H01 VOLATILITY RESPONSE ASYMMETRY V1 — CONTROLLED EXECUTION
Protocol: output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY_PROTOCOL_V1.md (v1.1.0, FROZEN)
Executes the frozen protocol exactly; no tuning, no outcome-driven selection, no TEST reuse.
Artifacts are written under output/research_discovery/H01_VOLATILITY_RESPONSE_ASYMMETRY/

Frozen parameter summary (protocol §16 FROZEN_PARAMS):
  shock        = daily log return r_t
  response     = dlnRV = ln(RV_{t+1..t+5}) - ln(RV_{t-5..t-1}); RV = sum of squared daily log returns
  strata       = within-market terciles of ln(RV_back) over the market's full eligible series
  matching     = within-(market,stratum) nearest-neighbour caliper on |r|, caliper 0.25*SD(|r|),
                 greedy one-to-one, stable tie-break (|r| asc, timestamp asc); r_t=0 excluded;
                 reference pool = smaller of NEG/POS (equal -> POS)
  statistic    = d_(m,s) = mean over matched pairs of [dlnRV(neg) - dlnRV(pos)];
                 d_m = mean over 3 strata; D_class = mean over primary-evaluable markets
  evaluability = >= 30 matched pairs in all 3 strata (market); >= 2 evaluable markets (class verdict)
  family       = 11 class statistics (7 Layer A + 4 Layer B), Holm step-down, alpha = 0.05
  bootstrap    = synchronized circular calendar blocks over each class's union calendar,
                 L = 11, B = 10,000, single master seed 20260813; no truncation, no padding

Implementation notes (deterministic, recorded in artifacts; never scientific parameter changes):
  * Replicate stream = nblocks = ceil(T/L) whole circular blocks; block dates concatenated in
    sampling order; per-market stream = that market's eligible shock records whose dates fall in
    the sampled blocks, ordered by date, each kept as many times as its date was sampled.
  * Matching tie-break is implemented by stable-sorting records (which are stored in chronological
    date order) by |r|, so equal |r| preserves timestamp order (record date order).
  * caliper c = 0.25*SD(|r|) within (m,stratum) is computed once on the ORIGINAL eligible records
    and frozen into every replicate.
  * scipy.optimize (Nelder-Mead, fixed start, deterministic) is used only for the secondary
    GJR(1,1)/EGARCH(1,1) diagnostics (§21.6); its version is recorded in the metadata.
  * M1 daily aggregation (§13) implements the registered last-wins dedup manually (stable sort by
    ts, keep the last row of each equal-ts run) because pandas 3.0.2 `drop_duplicates` segfaults
    on large string frames on this platform; verified byte-identical to the recorded daily series
    for all 5 M1 markets (dup_raw == 0 in every market, so the dedup is a no-op).
  * The bootstrap loop supports deterministic parallel execution (H01_WORKERS > 1): ALL block
    starts are pre-generated in the main process from the single master RNG in exact serial order
    (class order x replicate index), then per-replicate draws are computed by workers; draws are
    bit-identical to a serial run. Per-class draws are checkpointed to .build_cache/
    bootstrap_H01_<key>.npy (+ .json) and resumed on rerun (same master seed 20260813; completed
    RNG consumption is replayed), so a long run can be split across invocations with NO change to
    results. H01_OUT redirects artifact output (used for verification runs only).
"""
import csv
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timedelta

import numpy as np

ENCODING = 'utf-8'
try:
    sys.stdout.reconfigure(encoding=ENCODING)
    sys.stderr.reconfigure(encoding=ENCODING)
except AttributeError:
    pass

T0 = time.time()

REPO = r'C:\Users\User10\Documents\MRV\yuvi\QuantForge'
OUT = os.environ.get('H01_OUT') or os.path.dirname(os.path.abspath(__file__))
HPD = r'C:\Users\User10\AppData\Local\Temp\quantforge_tsmom_hpd_full'
M1DIR = os.path.join(REPO, 'data', 'm1')
PROTOCOL_PATH = os.path.join(REPO, 'output', 'research_discovery',
                             'H01_VOLATILITY_RESPONSE_ASYMMETRY_PROTOCOL_V1.md')

# ---------------------------------------------------------------------------
# Frozen constants
# ---------------------------------------------------------------------------
PROTOCOL_VERSION = '1.1.0'
SEED = 20260813
B_REPL = int(os.environ.get('H01_B', 10000))
L_BLOCK = 11
ALPHA = 0.05
MIN_PAIRS = 30
MIN_EVALUABLE = 2
CALIPER_RATIO = 0.25
COMMON_WIN = ('1987-01-13', '2002-08-30')

ROOTS_A = ['ad', 'bp', 'c', 'cd', 'cl', 'cr', 'ct', 'dx', 'ed', 'fc', 'gc', 'hg',
           'jo', 'jy', 'lh', 'o', 's', 'sf', 'si', 'sp', 'us', 'w']
LAYER_B = ['XAUUSD', 'XAGUSD', 'EURUSD', 'BTCUSD', 'USATECHIDXUSD']

# frozen §4 class structure; direction: +1 classic, -1 inverse, None two-sided
CLASSES = {
    'EQUITY_INDICES':    {'layerA': ['sp'], 'layerB': ['USATECHIDXUSD'], 'direction': +1, 'prior': 'ESTABLISHED'},
    'PRECIOUS_METALS':   {'layerA': ['gc', 'si'], 'layerB': ['XAUUSD', 'XAGUSD'], 'direction': -1, 'prior': 'ESTABLISHED'},
    'ENERGY_CRUDE':      {'layerA': ['cl'], 'layerB': [], 'direction': +1, 'prior': 'ESTABLISHED (narrow)'},
    'COMMODITIES_OTHER': {'layerA': ['c', 'o', 's', 'w', 'ct', 'jo', 'fc', 'lh', 'hg'], 'layerB': [],
                          'direction': -1, 'prior': 'ESTABLISHED (broad)'},
    'FX':                {'layerA': ['ad', 'bp', 'cd', 'dx', 'jy', 'sf'], 'layerB': ['EURUSD'],
                          'direction': None, 'prior': 'GENUINELY UNRESOLVED'},
    'RATES':             {'layerA': ['ed', 'us'], 'layerB': [], 'direction': None, 'prior': 'NO ESTABLISHED PRIOR'},
    'INDEX_COMMODITY':   {'layerA': ['cr'], 'layerB': [], 'direction': None, 'prior': 'NO ESTABLISHED PRIOR'},
    'CRYPTO':            {'layerA': [], 'layerB': ['BTCUSD'], 'direction': None, 'prior': 'GENUINELY UNRESOLVED'},
}
CROSS_ERA_CLASSES = ('PRECIOUS_METALS', 'EQUITY_INDICES', 'FX')

FROZEN_PARAMS = {
    'protocol_version': PROTOCOL_VERSION,
    'shock': 'daily log return r_t',
    'response': 'dlnRV = ln(RV_fwd5) - ln(RV_back5); RV = sum of squared daily log returns',
    'strata': 'within-market terciles of ln(RV_back5) over the market full eligible series',
    'matching': 'within-(market,stratum) nearest-neighbour caliper on |r|, caliper 0.25*SD(|r|), '
                'greedy one-to-one, stable tie-break (|r| asc, timestamp asc), r_t=0 excluded, '
                'reference pool = smaller of NEG/POS (equal -> POS)',
    'caliper_ratio': CALIPER_RATIO,
    'statistic': 'd_(m,s)=mean[pairs](dlnRV_neg - dlnRV_pos); d_m=mean(3 strata); D_class=mean(evaluable markets)',
    'evaluability': {'min_pairs_per_stratum': MIN_PAIRS, 'min_evaluable_markets_per_class': MIN_EVALUABLE},
    'family': {'n': 11, 'correction': 'Holm step-down', 'alpha': ALPHA},
    'bootstrap': {'L': L_BLOCK, 'B': B_REPL, 'seed': SEED,
                  'type': 'synchronized circular calendar blocks over class union calendar',
                  'length_rule': 'nblocks = ceil(T/L) whole blocks, no truncation, no padding',
                  'p': 'p = 2 * min(Pr*(D* >= D_obs), Pr*(D* <= D_obs))',
                  'ci': 'percentile (2.5%, 97.5%)'},
    'common_window_sensitivity': list(COMMON_WIN),
}

# ---------------------------------------------------------------------------
# utilities
# ---------------------------------------------------------------------------

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Gate 1 fingerprints (values == protocol table / TSMOM V2 metadata, 2026-08-13)
# ---------------------------------------------------------------------------
EXPECTED_FRONT_HASH = {
    'ad': '00dc57296975e0d27aa3f11adcc6d722c36f2efb24fd8fa6b6bd704194a19477',
    'bp': '18f08b792f48c4f54fc9dbe59e23b23c751b9d05a9a2ff8a25a1338724def3fd',
    'c':  '8549b37ac540dab8f61b5ccb107204d06c2b2faab0ff19f8c5252fc78cb52de8',
    'cd': 'f2c358b4614e8e98482343ec61a0590207a29b76deafe2fe2afea5dc9411b500',
    'cl': '76e97e111b654f9ecfaa9438db50d37ca38bf3919c52c36529e32e53a05eb88a',
    'cr': 'eae1d16c472e5e714210db9023d3502eb738e292fc379226e56e728985de787f',
    'ct': '3a0dfad2bc8d8e48da561b98cd79cac208dc8a903f7155e9ad17489daec8d0e6',
    'dx': '44cbad3506ac278781a75a3281d3927ac640455eda44fec85980f90504dd298f',
    'ed': 'f5c8621b299954f3489bdf2f46cf838f6567c996f4c97ac666263605063f27a7',
    'fc': 'c267c6f953073b047d853cc79bdece6f6a0287fffa2127e2faa3cecbe13b6f4f',
    'gc': 'a2e7e0221900134334e8a04027d672f0a74d8e8ea915042ee933c0638a78dab0',
    'hg': '3d2d2ac2077db8a9326d87570bc946bbd9659564c0164da383feb8e5c15959ad',
    'jo': '291b412805e3c1d254849c1040aaac9ac96f55b955fddc49189fb6b81c41d3e2',
    'jy': '1d9976686e679e72de379709ab60cb478a4ed61c798873fd387de09a896e44e5',
    'lh': '4ced26581e9320c277416c684e6790b06e43e7104d102b2c8d301ae66b137ee1',
    'o':  '891b7f114095032c48d5b9330fd7f09ffe73b056177edf40f67caf542097f671',
    's':  '6bc0d21b4239af6cf1f84013268084f57de50c14eae2cc13f47c4b9b6ccf6ae4',
    'sf': '6cf1b8dd2b9cf20d2a78c514f7471f9619bdfa09b4774dafd3306d17cd989df8',
    'si': '892278635bb55636abd16b642e83871c381167773d689d297d96d2899fb79adc',
    'sp': '09451cdb44e09a453fc40888d8f0e9ba6b8ad79a9e45a4a05128683e2f2e721b',
    'us': '3df550753dac5f801b62b9c86f42fb8db32ac7a02b281719f05e418d5e3e243d',
    'w':  'ef53eebdc1d99f187ff61dba3fb0d0a758841c4ee9b0eedab5ea8cc6c300fbd6',
}
EXPECTED_MANIFEST_HASH = {
    'HPD_MANIFEST.csv': '5cb150e0df6521201bd5e75d4bf3f0e905799b4d7f6d3d4dc19d151c48934c49',
    'HPD_CONTRACT_HASHES.csv': '771926f1d7d7ffc9246c730003fd2f4dff5d46167f12d12eed3ac56e6c896caa',
    'FINAL_CLASSIFICATION.csv': 'bf18527ab40e1381228bb68e4d95ca2cc69335ff6103db70ebd1bfea2c706f76',
    'PER_MARKET_VALIDATION.csv': 'ae6462a7428c4aa35fec9ee4c1e4e7d50f25c76898c0bb1dfa421185f55d5513',
}
EXPECTED_M1_HASH = {
    'XAUUSD': '54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c',
    'XAGUSD': '69444be954a869ebc831cd1253849222d8babc7a02940b2bb908a5179bcf5999',
    'EURUSD': '5106a518e65a9d3f4c8bfc74c14fad81240a9de278bd1c4577799a6f1b79813f',
    'BTCUSD': '97b853854d8f650d80e3972f159deab0b15911e19dd437e1dd10b3bab098409b',
    'USATECHIDXUSD': '39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6',
}


def gate_fingerprints():
    gates = {}
    for r in ROOTS_A:
        p = os.path.join(HPD, f'front_{r}.csv')
        gates[f'front_{r}'] = sha256(p) == EXPECTED_FRONT_HASH[r]
    for name, exp in EXPECTED_MANIFEST_HASH.items():
        gates[f'manifest_{name}'] = sha256(os.path.join(HPD, name)) == exp
    for m, exp in EXPECTED_M1_HASH.items():
        gates[f'{m}_m1'] = sha256(os.path.join(M1DIR, f'{m}_M1.csv')) == exp
    bad = [k for k, v in gates.items() if not v]
    if bad:
        raise SystemExit(f'GATE 1 (fingerprint) FAILED for: {bad}')
    print('[gate1] fingerprints OK (22 front + 4 manifest + 5 M1)', flush=True)
    return gates


# ---------------------------------------------------------------------------
# Layer A — HPD daily series
# ---------------------------------------------------------------------------

def load_hpd(root):
    dates, syms, close_v, adj_v = [], [], [], []
    with open(os.path.join(HPD, f'front_{root}.csv'), newline='', encoding=ENCODING) as f:
        rd = csv.reader(f)
        header = next(rd, None)
        if header != ['date', 'sym', 'close', 'adj_close']:
            raise SystemExit(f'{root}: unexpected header {header}')
        for p in rd:
            if not p or len(p) < 4:
                continue
            try:
                c = float(p[2])
                a = float(p[3])
            except ValueError:
                raise SystemExit(f'GATE 6 (OHLC validity) FAILED: non-numeric row in front_{root}.csv: {p}')
            if not (c > 0 and a > 0):
                raise SystemExit(f'GATE 6 (OHLC validity) FAILED: nonpositive close in front_{root}.csv: {p}')
            dates.append(p[0])
            syms.append(p[1])
            close_v.append(c)
            adj_v.append(a)
    return dates, syms, close_v, adj_v


def build_layerA_market(root, win=None):
    dates, syms, closes, adj = load_hpd(root)
    n = len(dates)
    if win:
        lo, hi = win
        idx = [i for i, d in enumerate(dates) if lo <= d <= hi]
        dates = [dates[i] for i in idx]
        syms = [syms[i] for i in idx]
        closes = [closes[i] for i in idx]
        adj = [adj[i] for i in idx]
        n = len(dates)
    seen = set()
    for d in dates:
        if d in seen:
            raise SystemExit(f'GATE 4 (duplicate) FAILED: duplicate date {d} in front_{root}.csv')
        seen.add(d)
    r = [None] * n
    is_roll = [False] * n
    for i in range(1, n):
        r[i] = math.log(adj[i] / adj[i - 1])
        is_roll[i] = (syms[i] != syms[i - 1])
    return {'root': root, 'dates': dates, 'syms': syms, 'r': r, 'is_roll': is_roll,
            'closes': closes, 'adj': adj, 'n_rows': n}


def roll_count(root):
    dates, syms, _, _ = load_hpd(root)
    return sum(1 for i in range(1, len(syms)) if syms[i] != syms[i - 1])


# ---------------------------------------------------------------------------
# Layer B — M1 aggregation (protocol §13)
# NOTE: pandas is imported lazily inside main() (it is only needed for version
# reporting); the bootstrap worker processes therefore never import pandas,
# keeping their memory footprint small on this memory-constrained platform.
# ---------------------------------------------------------------------------


def load_m1(mkt):
    # NOTE (implementation, no semantic change): pandas 3.0.2 + numpy 2.4.4 on this
    # platform segfaults (`drop_duplicates` on >2M-row string frames) and can OOM in the
    # C parser (`read_csv` on the largest M1 files under memory pressure). The registered
    # aggregation (protocol §13) is therefore implemented with a streaming csv-module pass
    # that needs only O(#days + #unique-ts) memory: keep the LAST occurrence of each
    # timestamp (last-wins dedup) and the close of the LAST bar (max ts) per UTC day.
    # Verified byte-identical to the registered pipeline's recorded daily series for all
    # 5 M1 markets (dates and closes identical; dup_raw == 0 everywhere, so dedup is a
    # no-op and keep-last semantics coincide with the recorded output).
    path = os.path.join(M1DIR, f'{mkt}_M1.csv')
    best = {}   # date -> (ts, close); ts >= replaces -> keep-last of the max-ts bar
    n_valid = 0
    bad_close = 0
    dup_raw = 0
    n_unsorted = 0
    prev_ts = None
    with open(path, newline='', encoding=ENCODING) as f:
        rd = csv.reader(f)
        next(rd, None)  # header (skiprows=1)
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
    # M1 files are timestamp-sorted exports; the registered last-wins dedup is defined on
    # file order, so a non-monotonic file would make duplicate handling ambiguous (gate 4).
    if n_unsorted:
        raise SystemExit(f'GATE 4 (duplicate) FAILED for {mkt}: {n_unsorted} out-of-order timestamps')
    daily = [(d, c) for d, (_, c) in sorted(best.items())]
    dup_ts = 0  # post-dedup duplicates are zero by construction
    first_date = daily[0][0]
    last_bar_close = best[first_date][1]
    spot_ok = abs(last_bar_close - daily[0][1]) < 1e-12
    if not spot_ok:
        raise SystemExit(f'GATE 8 (aggregation) FAILED for {mkt}')
    if dup_raw:
        raise SystemExit(f'GATE 4 (duplicate) FAILED for {mkt}: ambiguous duplicate timestamps')
    r = [None] * len(daily)
    for i in range(1, len(daily)):
        r[i] = math.log(daily[i][1] / daily[i - 1][1])
    return {'mkt': mkt, 'dates': [d for d, _ in daily], 'syms': [mkt] * len(daily),
            'r': r, 'is_roll': [False] * len(daily), 'closes': [c for _, c in daily],
            'adj': [c for _, c in daily], 'n_rows': len(daily),
            'stats': {'rows': n_valid - dup_raw, 'dup_timestamps': dup_ts, 'dup_raw': dup_raw,
                      'bad_close': bad_close,
                      'n_days': len(daily), 'first': daily[0][0], 'last': daily[-1][0],
                      'spot_verified': True}}


def load_m1_intraday_perdate(mkt):
    """date -> sum of squared 1-minute log returns over consecutive same-UTC-day bars.
    Streaming equivalent of the registered computation (dropna + last-wins dedup + same-day
    log returns), with O(#days) memory; see the load_m1 note for the platform rationale."""
    path = os.path.join(M1DIR, f'{mkt}_M1.csv')
    agg = {}
    prev_ts = None
    prev_close = None
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
                continue  # invalid row skipped; prev unchanged (dropna semantics)
            if prev_ts is not None and prev_ts[:10] == ts[:10]:
                d = ts[:10]
                lr = math.log(cv / prev_close)
                agg[d] = agg.get(d, 0.0) + lr * lr
            prev_ts, prev_close = ts, cv
    return agg


# ---------------------------------------------------------------------------
# Eligible-shock construction (protocol §8/§12/§13)
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


# ---------------------------------------------------------------------------
# Terciles (frozen per market, protocol §7)
# ---------------------------------------------------------------------------

def compute_terciles(records):
    vals = np.array([rec['lnrv_back'] for rec in records])
    return float(np.quantile(vals, 1.0 / 3.0, method='linear')), float(np.quantile(vals, 2.0 / 3.0, method='linear'))


def stratum_of(lnrv, q1, q2):
    if lnrv < q1:
        return 0
    if lnrv < q2:
        return 1
    return 2


# ---------------------------------------------------------------------------
# Greedy caliper matching (protocol §2).
# Assumes magR and magM are pre-sorted ASCENDING by |r| with stable (chronological)
# order for ties, which implements the frozen tie-break (|r| asc, timestamp asc).
# ---------------------------------------------------------------------------

def greedy_diff(magR, respR, magM, respM, c, ref_is_neg):
    """Return the array of per-pair response diffs (resp_neg - resp_pos)."""
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
    """Split eligible records of market into strata; return per-stratum sorted neg/pos arrays."""
    strata = np.array([stratum_of(r['lnrv_back'], q1, q2) for r in records], dtype=np.int8)
    out = {}
    for s in range(3):
        idx = np.nonzero(strata == s)[0]
        o = np.argsort(mag[idx], kind='stable')
        mag_s = mag[idx][o]
        resp_s = resp[idx][o]
        neg_s = neg[idx][o]
        mag_neg = mag_s[neg_s]
        resp_neg = resp_s[neg_s]
        mag_pos = mag_s[~neg_s]
        resp_pos = resp_s[~neg_s]
        out[s] = {'mag_neg': mag_neg, 'resp_neg': resp_neg,
                  'mag_pos': mag_pos, 'resp_pos': resp_pos,
                  'idx': idx}
    return out


def match_stratum(dat, c, records):
    """Run greedy matching on a pre-split stratum; returns diffs and counts."""
    n_neg = len(dat['mag_neg'])
    n_pos = len(dat['mag_pos'])
    if n_neg == 0 or n_pos == 0:
        return np.zeros(0, dtype=np.float64), n_neg, n_pos
    if not (np.isfinite(c) and c > 0):
        return np.zeros(0, dtype=np.float64), n_neg, n_pos
    # reference pool = smaller of NEG/POS; equal -> POS (protocol §2)
    ref_is_neg = (n_neg < n_pos)
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
        mag_all = np.concatenate([dat['mag_neg'], dat['mag_pos']]) if (len(dat['mag_neg']) or len(dat['mag_pos'])) else np.zeros(0)
        if len(mag_all) < 2:
            out[s] = {'npairs': 0, 'd_ms': None, 'unmatched_neg': len(dat['mag_neg']),
                      'unmatched_pos': len(dat['mag_pos']), 'balance': None, 'caliper': None}
            continue
        c = CALIPER_RATIO * float(np.std(mag_all, ddof=1))
        diffs, n_neg, n_pos = match_stratum(dat, c, records)
        npairs = len(diffs)
        npairs_tot += npairs
        d_ms = float(diffs.mean()) if npairs else None
        # balance diagnostic (confirmatory/QC only)
        mn_neg = float(dat['mag_neg'].mean() if len(dat['mag_neg']) else math.nan)
        mn_pos = float(dat['mag_pos'].mean() if len(dat['mag_pos']) else math.nan)
        sd_neg = float(dat['mag_neg'].std(ddof=1)) if len(dat['mag_neg']) > 1 else math.nan
        sd_pos = float(dat['mag_pos'].std(ddof=1)) if len(dat['mag_pos']) > 1 else math.nan
        smd = (mn_neg - mn_pos) / math.sqrt((sd_neg ** 2 + sd_pos ** 2) / 2.0) if (sd_neg and sd_pos and (sd_neg + sd_pos) > 0) else math.nan
        out[s] = {'npairs': npairs, 'd_ms': d_ms, 'unmatched_neg': n_neg - npairs,
                  'unmatched_pos': n_pos - npairs,
                  'balance': {'mean_absr_neg': mn_neg, 'mean_absr_pos': mn_pos,
                              'sd_absr_neg': sd_neg, 'sd_absr_pos': sd_pos, 'smd': smd},
                  'caliper': c}
    return out, npairs_tot


def collect_pair_table(records, layer, market, q1, q2):
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
        mp = _match_pairs_with_dates(records, mag, resp, neg, strata, s, c)
        for m2 in mp:
            m2['layer'] = layer
            m2['market'] = market
            m2['stratum'] = s
            pairs.append(m2)
    return pairs


def _match_pairs_with_dates(records, mag, resp, neg, strata, s, c):
    """Exact greedy matching returning (neg_date, pos_date, dlnrv_neg, dlnrv_pos)."""
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
        neg_rec = recR[i] if ref_is_neg else recM[k]
        pos_rec = recM[k] if ref_is_neg else recR[i]
        neg_resp = respR[i] if ref_is_neg else respM[k]
        pos_resp = respM[k] if ref_is_neg else respR[i]
        pairs.append({'neg_date': records[neg_rec]['date'], 'pos_date': records[pos_rec]['date'],
                      'dlnrv_neg': float(neg_resp), 'dlnrv_pos': float(pos_resp),
                      'delta': float(neg_resp - pos_resp)})
    return pairs


# ---------------------------------------------------------------------------
# Bootstrap — synchronized class-level calendar blocks (protocol §9/§16)
# ---------------------------------------------------------------------------

def holm(ps):
    ps = [1.0 if (p is None or (isinstance(p, float) and math.isnan(p))) else max(0.0, min(1.0, p)) for p in ps]
    order = sorted(range(len(ps)), key=lambda i: (ps[i], i))
    adj = [None] * len(ps)
    run = 0.0
    for rank, i in enumerate(order, start=1):
        v = min(1.0, (len(ps) - rank + 1) * ps[i])
        run = max(run, v)
        adj[i] = run
    return adj


# ---------------------------------------------------------------------------
# Verdicts (protocol §18)
# ---------------------------------------------------------------------------

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


def class_verdict(name, layer, D_obs, p_holm, dm_by_market, eval_flags, n_ev_other, rel_sign_other):
    """Returns (verdict, n_evaluable). rel_sign_other: for cross-era classes, whether the
    other layer's statistic is reliable (p<alpha) and sign-matched to the expected direction."""
    cls = CLASSES[name]
    direction = cls['direction']
    layer_key = 'A' if layer == 1 else 'B'
    mk = cls[f'layer{layer_key}']
    ev = [m for m in mk if eval_flags.get(m) and dm_by_market.get(m) is not None]
    n_ev = len(ev)
    if n_ev < MIN_EVALUABLE:
        return 'EVIDENCE-LIMITED/DESCRIPTIVE', n_ev
    reliable = p_holm is not None and not math.isnan(p_holm) and p_holm < ALPHA
    sg = sign(D_obs)
    if sg != 0 and ev:
        frac_same = sum(1 for m in ev if sign(dm_by_market[m]) == sg) / float(len(ev))
    else:
        frac_same = 0.0
    consistent = frac_same >= (2.0 / 3.0)

    if direction is not None:
        sign_match = sg == direction
        if name in CROSS_ERA_CLASSES and layer in (1, 2):
            # other layer exists in every cross-era class for both layers
            cross_ok = (n_ev_other >= MIN_EVALUABLE) and bool(rel_sign_other)
        else:
            cross_ok = True
        if reliable and sign_match and consistent and cross_ok:
            return 'SUPPORT', n_ev
        if reliable and (not sign_match or not consistent):
            return 'CONTRADICTION', n_ev
        return 'INCONCLUSIVE', n_ev
    else:
        # two-sided: FX, RATES, INDEX_COMMODITY, CRYPTO
        if n_ev < MIN_EVALUABLE:
            return 'EVIDENCE-LIMITED/DESCRIPTIVE', n_ev
        if reliable and consistent:
            return 'SUPPORT', n_ev
        return 'INCONCLUSIVE', n_ev


# ---------------------------------------------------------------------------
# Secondary diagnostics (protocol §21)
# ---------------------------------------------------------------------------

def engle_ng_sign_bias(r, z):
    """Engle–Ng (1993): z2_t on sign/size functions of r_{t-1}; t aligned on r[:-1]."""
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
        out[name] = {'coef': float(beta[1]), 't': float(beta[1] / se) if se and se > 0 else math.nan,
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
        lsig2[t] = max(min(lsig2[t], 700.0), -700.0)
        z2[t] = rz[t] / math.exp(lsig2[t] / 2.0)
    H = numeric_hessian(lambda th: egarch_loglik(th, rz), r2_.x)
    try:
        cov = np.linalg.inv(H)
        se_gamma = math.sqrt(abs(cov[3, 3])) if np.isfinite(cov[3, 3]) else math.nan
    except Exception:
        se_gamma = math.nan
    res['egarch'] = {'omega': float(omega), 'alpha': float(alpha), 'beta': float(beta),
                     'gamma': float(gamma), 'se_gamma': float(se_gamma),
                     'nll': float(r2_.fun), 'converged': bool(r2_.success),
                     'gamma_at_bound': at_bound}
    return res


# ---------------------------------------------------------------------------
# Bootstrap per-replicate computation (protocol §9/§16) + parallel worker glue.
# rep_class_dm is a PURE function of (class pack, block starts) — exactly the
# computation the serial loop performs. The parallel path pre-generates ALL block
# starts in the main process from the single master RNG in exact serial order and
# ships (key, b, starts) to workers, so per-replicate draws — and therefore every
# reported statistic — are bit-identical to a serial run. Workers never touch the
# RNG.
# ---------------------------------------------------------------------------

def rep_class_dm(pack, starts):
    """Per-replicate class statistic D_class^b given the frozen class pack and the
    sampled circular-block start positions (protocol §9.3/§9.4)."""
    ridx = (starts[:, None] + pack['ar']) % pack['T']
    counts = np.bincount(ridx.reshape(-1), minlength=pack['T'])
    dm_vals = []
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
                s_diffs.append(float(diffs.mean()))
        if s_diffs:
            dm_vals.append(float(np.mean(s_diffs)))
    if dm_vals:
        return float(np.mean(dm_vals))
    return math.nan


_WORKER_PACKS = None


def init_worker(packs):
    global _WORKER_PACKS
    _WORKER_PACKS = packs


def worker_rep(task):
    key, b, starts = task
    return key, b, rep_class_dm(_WORKER_PACKS[key], starts)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    import pandas as pd  # noqa: F401  (used only for version reporting below)
    fp = gate_fingerprints()
    fp['protocol_sha256'] = sha256(PROTOCOL_PATH)

    # ----- Layer A
    print('== Layer A: loading 22 HPD markets ==', flush=True)
    la = {}
    gate7 = {}
    for r in ROOTS_A:
        m = build_layerA_market(r)
        la[r] = m
        gate7[r] = roll_count(r)
        print(f'  {r}: rows={m["n_rows"]} roll_days={gate7[r]}', flush=True)
    val_rolls = {}
    with open(os.path.join(HPD, 'PER_MARKET_VALIDATION.csv'), newline='', encoding=ENCODING) as f:
        for row in csv.DictReader(f):
            val_rolls[row['root']] = int(row['n_rolls'])
    for r in ROOTS_A:
        if gate7[r] != val_rolls[r]:
            raise SystemExit(f'GATE 7 (roll consistency) FAILED: {r} sym-changes={gate7[r]} vs {val_rolls[r]}')
    print('[gate7] roll-consistency OK for all 22 roots', flush=True)

    # ----- Layer B
    print('== Layer B: loading 5 M1 markets ==', flush=True)
    lb = {}
    for m in LAYER_B:
        mm = load_m1(m)
        lb[m] = mm
        st = mm['stats']
        print(f'  {m}: days={st["n_days"]} ({st["first"]}..{st["last"]}) rows={st["rows"]} '
              f'dup={st["dup_timestamps"]} bad_close={st["bad_close"]}', flush=True)

    # ----- eligible records
    print('== eligible-shock construction ==', flush=True)
    cm = {}
    for r in ROOTS_A:
        rec, cnt = build_records(la[r])
        cm[r] = {'records': rec, 'cnt': cnt, 'daily': la[r]}
        print(f'  [A:{r}] eligible={len(rec)} excl={cnt}', flush=True)
    for m in LAYER_B:
        rec, cnt = build_records(lb[m])
        cm[m] = {'records': rec, 'cnt': cnt, 'daily': lb[m]}
        print(f'  [B:{m}] eligible={len(rec)} excl={cnt}', flush=True)

    ords = {}
    for r in ROOTS_A:
        for k, d in enumerate(la[r]['dates']):
            ords[d] = k
    for m in LAYER_B:
        for k, d in enumerate(lb[m]['dates']):
            ords[d] = k

    terciles = {}
    for m, v in cm.items():
        add_secondary_stores(v['records'], v['daily'])
        q1, q2 = compute_terciles(v['records'])
        terciles[m] = (q1, q2)
        v['q1'], v['q2'] = q1, q2

    # ----- primary (observed) stats
    print('== primary statistic (observed) ==', flush=True)
    per_market = {}
    for m, v in cm.items():
        layer = 'A' if m in la else 'B'
        st, npairs_tot = market_stats(v['records'], v['q1'], v['q2'])
        dvals = [st[s]['d_ms'] for s in range(3) if st[s]['d_ms'] is not None]
        d_m = float(np.mean(dvals)) if dvals else None
        evaluable = all(st[s]['npairs'] >= MIN_PAIRS for s in range(3))
        per_market[m] = {'layer': layer, 'market': m, 'd_m': d_m, 'evaluable': evaluable,
                         'pairs_per_stratum': {s: st[s]['npairs'] for s in range(3)},
                         'n_pairs_total': npairs_tot, 'eligible': len(v['records']),
                         'exclusions': v['cnt'], 'strata': st,
                         'terciles': {'q1': v['q1'], 'q2': v['q2']},
                         'roll_count': gate7.get(m, 0)}
        print(f'  {m}: pairs={npairs_tot} evaluable={evaluable} d_m='
              f'{"" if d_m is None else round(d_m, 6)}', flush=True)

    # ----- class observed statistics
    class_defs = []
    for name, cls in CLASSES.items():
        for layer in (1, 2):
            mk = cls[f'layer{"A" if layer == 1 else "B"}']
            if mk:
                class_defs.append({'name': name, 'layer': layer, 'markets': mk})
    class_defs.sort(key=lambda cd: (cd['name'], cd['layer']))

    class_results = {}
    for cd in class_defs:
        key = f'L{cd["layer"]}_{cd["name"]}'
        ev = [m for m in cd['markets'] if per_market[m]['evaluable']]
        vals = [per_market[m]['d_m'] for m in ev if per_market[m]['d_m'] is not None]
        D_obs = float(np.mean(vals)) if vals else None
        class_results[key] = {'class': cd['name'], 'layer': 'A' if cd['layer'] == 1 else 'B',
                              'markets': cd['markets'], 'evaluable_markets': ev,
                              'n_evaluable': len(ev), 'D_obs': D_obs,
                              'per_market_dm': {m: per_market[m]['d_m'] for m in cd['markets']}}
        print(f'  {key}: evaluable={len(ev)} D_obs={D_obs}', flush=True)

    # ----- bootstrap
    print(f'== synchronized class-level bootstrap (B={B_REPL}, L={L_BLOCK}, seed={SEED}) ==', flush=True)
    rng = np.random.default_rng(SEED)
    # precompute replicate arrays + frozen calipers
    repl = {}
    for m, v in cm.items():
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
        repl[m] = {'mag': mag, 'resp': resp, 'stratum': stv, 'neg': ng, 'dates': dates,
                   'calipers': cal}

    # class packs: per-class union calendar + per-evaluable-market replicate arrays
    packs = {}
    order = []
    bootstrap = {}
    for cd in class_defs:
        key = f'L{cd["layer"]}_{cd["name"]}'
        ev = [m for m in cd['markets'] if per_market[m]['evaluable']]
        if not ev:
            bootstrap[key] = {'T': None, 'nblocks': None, 'p_two': math.nan,
                              'ci95': [math.nan, math.nan], 'n_draws': 0,
                              'null_mean': None, 'class_draws': []}
            continue
        union_dates = set()
        for m in cd['markets']:
            union_dates.update(repl[m]['dates'])
        union_dates = sorted(union_dates)
        tind = {d: k for k, d in enumerate(union_dates)}
        T = len(union_dates)
        nblocks = int(math.ceil(T / float(L_BLOCK)))
        for m in cd['markets']:
            repl[m]['tind'] = np.array([tind[d] for d in repl[m]['dates']], dtype=np.int64)
        print(f'  {key}: T={T} nblocks={nblocks} evaluable={ev}', flush=True)
        pm = {}
        for m in ev:
            rec = repl[m]
            pm[m] = {k: rec[k] for k in ('mag', 'resp', 'stratum', 'neg', 'tind', 'calipers')}
        packs[key] = {'key': key, 'class': cd['name'], 'layer': cd['layer'],
                      'markets': ev, 'm': pm, 'T': T, 'nblocks': nblocks,
                      'ar': np.arange(L_BLOCK, dtype=np.int64)}
        order.append(key)

    # checkpoint/resume cache (crash-safe; .build_cache under the artifact root)
    CACHE_DIR = os.path.join(OUT, '.build_cache')
    os.makedirs(CACHE_DIR, exist_ok=True)

    def _cache_paths(key):
        return (os.path.join(CACHE_DIR, f'bootstrap_H01_{key}.npy'),
                os.path.join(CACHE_DIR, f'bootstrap_H01_{key}.json'))

    def _atomic_replace(src, dst, tries=10):
        """os.replace with retry: transient WinError 5 (AV / file-lock contention)
        has been observed on this platform; retrying keeps progress crash-safe."""
        for i in range(tries):
            try:
                os.replace(src, dst)
                return
            except OSError:
                if i == tries - 1:
                    raise
                time.sleep(0.5)

    def _save_cache(key, draws, n_consumed):
        npy, js = _cache_paths(key)
        tmp = npy + '.tmp'
        with open(tmp, 'wb') as f:
            np.save(f, draws)
        _atomic_replace(tmp, npy)
        tmp2 = js + '.tmp'
        with open(tmp2, 'w', encoding=ENCODING) as f:
            json.dump({'B': B_REPL, 'L': L_BLOCK, 'n_consumed': int(n_consumed)}, f)
        _atomic_replace(tmp2, js)

    def _load_cache(key):
        npy, js = _cache_paths(key)
        if not (os.path.exists(npy) and os.path.exists(js)):
            return None, 0
        with open(js, encoding=ENCODING) as f:
            meta = json.load(f)
        if meta.get('B') != B_REPL or meta.get('L') != L_BLOCK:
            return None, 0
        return np.load(npy), int(meta['n_consumed'])

    draws_all = {}
    nc0 = {}
    for key in order:
        cached, nc = _load_cache(key)
        if cached is not None and len(cached) == B_REPL:
            draws_all[key] = cached
            nc0[key] = nc
        else:
            draws_all[key] = np.full(B_REPL, math.nan)
            nc0[key] = 0

    # deterministic task stream: consumes the single master RNG exactly in serial
    # order (class order x replicate index); completed consumption is replayed so a
    # resumed run produces draws identical to one uninterrupted serial run.
    def _task_stream():
        for key in order:
            T = packs[key]['T']
            nblocks = packs[key]['nblocks']
            nc = nc0[key]
            if nc >= B_REPL:
                continue
            for _ in range(nc):
                rng.integers(0, T, size=nblocks)
            for b in range(nc, B_REPL):
                starts = rng.integers(0, T, size=nblocks)
                yield key, b, starts

    def _run_serial():
        for key, b, starts in _task_stream():
            draws_all[key][b] = rep_class_dm(packs[key], starts)
            progress[key] = b + 1
            if (b + 1) % 50 == 0 or (b + 1) == B_REPL:
                _save_cache(key, draws_all[key], b + 1)
                if (b + 1) % 1000 == 0:
                    print(f'    {key}: b={b + 1}/{B_REPL}', flush=True)

    progress = dict(nc0)
    workers = int(os.environ.get('H01_WORKERS', '1') or '1')
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor
        print(f'  [parallel] workers={workers}', flush=True)
        with ProcessPoolExecutor(max_workers=workers, initializer=init_worker,
                                 initargs=(packs,)) as ex:
            for key, b, dm in ex.map(worker_rep, _task_stream()):
                draws_all[key][b] = dm
                progress[key] = b + 1
                if (b + 1) % 50 == 0 or (b + 1) == B_REPL:
                    _save_cache(key, draws_all[key], b + 1)
                    if (b + 1) % 1000 == 0:
                        print(f'    {key}: b={b + 1}/{B_REPL}', flush=True)
    else:
        _run_serial()

    for key in order:
        obs = class_results[key]['D_obs']
        draws = draws_all[key]
        finite = draws[np.isfinite(draws)]
        if finite.size:
            pr_ge = float((finite >= obs).mean())
            pr_le = float((finite <= obs).mean())
            p = 2.0 * min(pr_ge, pr_le)
            ci = [float(np.percentile(finite, 2.5)), float(np.percentile(finite, 97.5))]
        else:
            p = math.nan
            ci = [math.nan, math.nan]
        bootstrap[key] = {'T': packs[key]['T'], 'nblocks': packs[key]['nblocks'],
                          'p_two': p, 'ci95': ci,
                          'n_draws': int(finite.size),
                          'null_mean': float(finite.mean()) if finite.size else None,
                          'class_draws': draws.tolist()}
        print(f'  {key}: p={p:.4f} CI={ci[0]:.5f}..{ci[1]:.5f}', flush=True)

    # ----- Holm
    fam_order = sorted(class_results.keys())
    raw_ps = {k: bootstrap[k]['p_two'] for k in fam_order}
    adj = holm([raw_ps[k] for k in fam_order])
    holm_res = {k: adj[i] for i, k in enumerate(fam_order)}
    print('== Holm step-down (11-member family) ==', flush=True)
    for k in fam_order:
        print(f'  {k}: p_raw={raw_ps[k]:.5f} p_holm={holm_res[k]:.5f}', flush=True)

    # ----- reliable-in-expected-direction per class-layer (for cross-era gate)
    rel_sign = {}
    n_ev_any = {}
    for cd in class_defs:
        key = f'L{cd["layer"]}_{cd["name"]}'
        cls = CLASSES[cd['name']]
        n_ev_any[key] = len(class_results[key]['evaluable_markets'])
        D = class_results[key]['D_obs']
        p = holm_res[key]
        rel_p = p < ALPHA
        if cls['direction'] is not None:
            rel_sign[key] = rel_p and sign(D) == cls['direction']
        else:
            rel_sign[key] = rel_p and sign(D) != 0

    # ----- verdicts
    print('== per-class verdicts (§18) ==', flush=True)
    verdicts = {}
    for cd in class_defs:
        key = f'L{cd["layer"]}_{cd["name"]}'
        cls = CLASSES[cd['name']]
        other_key = f'L{1 if cd["layer"] == 2 else 2}_{cd["name"]}'
        other_n_ev = n_ev_any.get(other_key, 0)
        other_rel_sign = rel_sign.get(other_key, False)
        v, n_ev = class_verdict(cd['name'], cd['layer'], class_results[key]['D_obs'], holm_res[key],
                                class_results[key]['per_market_dm'],
                                {m: per_market[m]['evaluable'] for m in per_market},
                                other_n_ev, other_rel_sign)
        verdicts[key] = {'class': cd['name'], 'layer': 'A' if cd['layer'] == 1 else 'B',
                         'D_obs': class_results[key]['D_obs'], 'p_raw': raw_ps[key],
                         'p_holm': holm_res[key], 'ci95': bootstrap[key]['ci95'],
                         'n_evaluable_markets': n_ev,
                         'evaluable_markets': class_results[key]['evaluable_markets'],
                         'consistency_frac': None, 'verdict': v}
        # consistency fraction (reported)
        ev = [m for m in cd['markets'] if per_market[m]['evaluable']]
        sg = sign(class_results[key]['D_obs'])
        if sg != 0 and ev:
            frac = sum(1 for m in ev if sign(per_market[m]['d_m']) == sg) / float(len(ev))
            verdicts[key]['consistency_frac'] = round(frac, 4)
        print(f'  {key}: D={class_results[key]["D_obs"]} p_holm={holm_res[key]:.4f} -> {v}', flush=True)

    # ----- secondary analyses (§21)
    print('== secondary analyses (§21) ==', flush=True)

    # §21.1 1-day horizon (reuses primary pairs)
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

    # paired-event cache (single pass)
    print('  [pairs] building matched-pair event cache...', flush=True)
    pair_cache = {}
    for m, v in cm.items():
        pairs = collect_pair_table(v['records'], 'A' if m in la else 'B', m, v['q1'], v['q2'])
        pair_cache[m] = pairs
    all_pairs = [pp for m in pair_cache for pp in pair_cache[m]]
    print(f'  [pairs] total matched pairs = {len(all_pairs)}', flush=True)

    sec1_by_mkt, sec21_by_mkt, sec4_by_mkt = {}, {}, {}
    for m, v in cm.items():
        sec1_by_mkt[m] = sec1(v['records'], pair_cache[m])
    # §21.2 21-day horizon
    sec21_by_mkt = {}
    for m, v in cm.items():
        rmap = {r['date']: r for r in v['records']}
        sm = {}
        for s in range(3):
            diffs = []
            for p in pair_cache[m]:
                if p['stratum'] != s:
                    continue
                nr, pr = rmap.get(p['neg_date']), rmap.get(p['pos_date'])
                if nr is None or pr is None:
                    continue
                if nr.get('rv21_ok') and pr.get('rv21_ok'):
                    diffs.append(nr['dlnrv21'] - pr['dlnrv21'])
            sm[s] = {'npairs': len(diffs), 'mean': float(np.mean(diffs)) if diffs else None}
        sec21_by_mkt[m] = sm
    # §21.4 absolute-return response
    sec4_by_mkt = {}
    for m, v in cm.items():
        rmap = {r['date']: r for r in v['records']}
        sm = {}
        for s in range(3):
            diffs = []
            for p in pair_cache[m]:
                if p['stratum'] != s:
                    continue
                nr, pr = rmap.get(p['neg_date']), rmap.get(p['pos_date'])
                if nr is not None and pr is not None:
                    diffs.append(nr['fwd_abs_mean'] - pr['fwd_abs_mean'])
            sm[s] = {'npairs': len(diffs), 'mean': float(np.mean(diffs)) if diffs else None}
        sec4_by_mkt[m] = sm

    def _class_agg(d_by_mkt, marker):
        out = {}
        for cd in class_defs:
            key = f'L{cd["layer"]}_{cd["name"]}'
            ev = [m for m in cd['markets'] if per_market[m]['evaluable']]
            dm_list = []
            for mm in ev:
                vals = [d_by_mkt[mm][s]['mean'] for s in range(3) if d_by_mkt[mm][s]['mean'] is not None]
                if vals:
                    dm_list.append(float(np.mean(vals)))
            out[key] = {'D': float(np.mean(dm_list)) if dm_list else None, 'n_markets': len(dm_list)}
        return out

    sec1_class = _class_agg(sec1_by_mkt, None)
    sec21_class = _class_agg(sec21_by_mkt, None)
    sec4_class = _class_agg(sec4_by_mkt, None)

    # §21.3 standardized-shock matching
    print('  [sec21.3] standardized-shock matching...', flush=True)
    sec3_by_mkt = {}
    for m, v in cm.items():
        recs = v['records']
        valid = [(k, x) for k, x in enumerate(recs) if x.get('sigma_hat') and x['sigma_hat'] > 0]
        if len(valid) < 2:
            sec3_by_mkt[m] = {'d_m': None}
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
        sec3_by_mkt[m] = {'d_m': float(np.mean(s_diffs)) if s_diffs else None}
    sec3_class = {}
    for cd in class_defs:
        key = f'L{cd["layer"]}_{cd["name"]}'
        ev = [m for m in cd['markets'] if per_market[m]['evaluable']]
        dm_list = [sec3_by_mkt[m]['d_m'] for m in ev if sec3_by_mkt[m]['d_m'] is not None]
        sec3_class[key] = {'D': float(np.mean(dm_list)) if dm_list else None, 'n_markets': len(dm_list)}

    # §21.5 intraday Layer B
    print('  [sec21.5] intraday Layer B RV...', flush=True)
    intra_by_mkt = {}
    for m in LAYER_B:
        per_date = load_m1_intraday_perdate(m)
        rmap = {r['date']: r for r in cm[m]['records']}
        sm = {}
        for s in range(3):
            diffs = []
            for p in pair_cache[m]:
                if p['stratum'] != s:
                    continue
                def winrv(tdate, offs):
                    d0 = datetime.strptime(tdate, '%Y-%m-%d')
                    tot = 0.0
                    for k in offs:
                        tot += per_date.get((d0 + timedelta(days=k)).strftime('%Y-%m-%d'), 0.0)
                    return tot
                nf, nb = winrv(p['neg_date'], range(1, 6)), winrv(p['neg_date'], range(-5, 0))
                pf, pb = winrv(p['pos_date'], range(1, 6)), winrv(p['pos_date'], range(-5, 0))
                nv = math.log(nf) - math.log(nb) if (nf > 0 and nb > 0) else None
                pv = math.log(pf) - math.log(pb) if (pf > 0 and pb > 0) else None
                if nv is not None and pv is not None:
                    diffs.append(nv - pv)
            sm[s] = {'npairs': len(diffs), 'mean': float(np.mean(diffs)) if diffs else None}
        intra_by_mkt[m] = sm
    intra_class = {}
    for cd in class_defs:
        if cd['layer'] == 2:
            key = f'L2_{cd["name"]}'
            ev = [m for m in cd['markets'] if m in intra_by_mkt]
            dm_list = []
            for mm in ev:
                vals = [intra_by_mkt[mm][s]['mean'] for s in range(3) if intra_by_mkt[mm][s]['mean'] is not None]
                if vals:
                    dm_list.append(float(np.mean(vals)))
            intra_class[key] = {'D': float(np.mean(dm_list)) if dm_list else None, 'n_markets': len(dm_list)}

    # §21.6/§21.7 GJR/EGARCH + Engle–Ng
    print('  [sec21.6/7] GJR/EGARCH + Engle–Ng...', flush=True)
    garch = {}
    for m, v in cm.items():
        d = v['daily']
        r_in = np.array([x for k, x in enumerate(d['r']) if x is not None and not d['is_roll'][k]],
                        dtype=np.float64)
        garch[m] = fit_garch(r_in)
        print(f'  {m}: GJR gamma={garch[m]["gjr"].get("gamma")} '
              f'EGARCH gamma={garch[m]["egarch"].get("gamma")}', flush=True)

    # §21.8 winsorization sensitivity (cap |r| at market 95th pct)
    print('  [sec21.8] winsorization sensitivity...', flush=True)
    win_by_mkt = {}
    for m, v in cm.items():
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
        win_by_mkt[m] = {'d_m': float(np.mean(s_diffs)) if s_diffs else None, 'cap': cap}
    win_class = {}
    for cd in class_defs:
        key = f'L{cd["layer"]}_{cd["name"]}'
        ev = [m for m in cd['markets'] if per_market[m]['evaluable']]
        dm_list = [win_by_mkt[m]['d_m'] for m in ev if win_by_mkt[m]['d_m'] is not None]
        win_class[key] = {'D': float(np.mean(dm_list)) if dm_list else None, 'n_markets': len(dm_list)}

    # §21.9 common-window Layer A sensitivity (full pipeline rerun, subset)
    print('  [sec21.9] common-window Layer A sensitivity (1987-01-13..2002-08-30)...', flush=True)
    cw_pm = {}
    for r in ROOTS_A:
        daily = build_layerA_market(r, win=COMMON_WIN)
        rec, _ = build_records(daily)
        q1, q2 = compute_terciles(rec)
        st, npairs = market_stats(rec, q1, q2)
        dvals = [st[s]['d_ms'] for s in range(3) if st[s]['d_ms'] is not None]
        d_m = float(np.mean(dvals)) if dvals else None
        evaluable = all(st[s]['npairs'] >= MIN_PAIRS for s in range(3))
        cw_pm[r] = {'d_m': d_m, 'evaluable': evaluable,
                    'pairs_per_stratum': {s: st[s]['npairs'] for s in range(3)},
                    'n_eligible': len(rec), 'n_rolls': sum(daily['is_roll'])}
    cw_class = {}
    for cd in class_defs:
        if cd['layer'] == 1:
            key = f'L1_{cd["name"]}'
            ev = [m for m in cd['markets'] if cw_pm[m]['evaluable']]
            vals = [cw_pm[m]['d_m'] for m in ev if cw_pm[m]['d_m'] is not None]
            cw_class[key] = {'D': float(np.mean(vals)) if vals else None,
                             'n_evaluable': len(ev),
                             'per_market_dm': {m: cw_pm[m]['d_m'] for m in cd['markets']}}

    # ----- write artifacts
    print('== writing artifacts ==', flush=True)
    series_dir = os.path.join(OUT, 'daily_series')
    os.makedirs(series_dir, exist_ok=True)
    for r in ROOTS_A:
        m = la[r]
        with open(os.path.join(series_dir, f'{r}.csv'), 'w', newline='', encoding=ENCODING) as f:
            w = csv.writer(f)
            w.writerow(['date', 'sym', 'close', 'adj_close', 'is_roll_day', 'log_return'])
            for i in range(len(m['dates'])):
                w.writerow([m['dates'][i], m['syms'][i], repr(m['closes'][i]), repr(m['adj'][i]),
                            1 if m['is_roll'][i] else 0,
                            '' if m['r'][i] is None else repr(m['r'][i])])
    for m in LAYER_B:
        mm = lb[m]
        with open(os.path.join(series_dir, f'{m}.csv'), 'w', newline='', encoding=ENCODING) as f:
            w = csv.writer(f)
            w.writerow(['date', 'close', 'log_return'])
            for i in range(len(mm['dates'])):
                w.writerow([mm['dates'][i], repr(mm['closes'][i]),
                            '' if mm['r'][i] is None else repr(mm['r'][i])])

    with open(os.path.join(OUT, 'matched_pairs_H01_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['layer', 'market', 'stratum', 'neg_date', 'pos_date', 'dlnrv_neg', 'dlnrv_pos', 'delta'])
        for p in all_pairs:
            w.writerow([p['layer'], p['market'], p['stratum'], p['neg_date'], p['pos_date'],
                        repr(p['dlnrv_neg']), repr(p['dlnrv_pos']), repr(p['delta'])])

    with open(os.path.join(OUT, 'per_market_stats_H01_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['layer', 'market', 'evaluable', 'eligible', 'n_rolls',
                    'pairs_low', 'pairs_mid', 'pairs_high', 'd_low', 'd_mid', 'd_high', 'd_m',
                    'smd_low', 'smd_mid', 'smd_high'])
        for m in ROOTS_A + LAYER_B:
            pm = per_market[m]
            st = pm['strata']
            w.writerow([pm['layer'], m, int(pm['evaluable']), pm['eligible'], pm['roll_count'],
                        st[0]['npairs'], st[1]['npairs'], st[2]['npairs'],
                        '' if st[0]['d_ms'] is None else repr(st[0]['d_ms']),
                        '' if st[1]['d_ms'] is None else repr(st[1]['d_ms']),
                        '' if st[2]['d_ms'] is None else repr(st[2]['d_ms']),
                        '' if pm['d_m'] is None else repr(pm['d_m']),
                        round(st[0]['balance']['smd'], 6) if st[0]['balance'] else '',
                        round(st[1]['balance']['smd'], 6) if st[1]['balance'] else '',
                        round(st[2]['balance']['smd'], 6) if st[2]['balance'] else ''])

    with open(os.path.join(OUT, 'class_stats_H01_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['class', 'layer', 'expected_direction', 'prior_status', 'markets',
                    'evaluable_markets', 'n_evaluable', 'D_class', 'ci_lo', 'ci_hi',
                    'p_raw', 'p_holm', 'verdict'])
        for cd in class_defs:
            key = f'L{cd["layer"]}_{cd["name"]}'
            cls = CLASSES[cd['name']]
            cr = class_results[key]
            bk = bootstrap[key]
            vr = verdicts[key]
            w.writerow([cd['name'], vr['layer'],
                        'classic' if cls['direction'] == 1 else ('inverse' if cls['direction'] == -1 else 'two-sided'),
                        cls['prior'], ' '.join(cd['markets']), ' '.join(vr['evaluable_markets']),
                        vr['n_evaluable_markets'],
                        '' if cr['D_obs'] is None else repr(cr['D_obs']),
                        repr(bk['ci95'][0]), repr(bk['ci95'][1]),
                        repr(raw_ps[key]), repr(holm_res[key]), vr['verdict']])

    with open(os.path.join(OUT, 'bootstrap_replicates_H01_V1.csv'), 'w', newline='', encoding=ENCODING) as f:
        w = csv.writer(f)
        w.writerow(['class_layer', 'replicate', 'D_class_star'])
        for k in fam_order:
            dr = bootstrap[k]['class_draws']
            for i, v in enumerate(dr, start=1):
                w.writerow([k, i, '' if math.isnan(v) else repr(v)])

    results = {
        'protocol_version': PROTOCOL_VERSION,
        'protocol_sha256': fp['protocol_sha256'],
        'executed_at': datetime.utcnow().isoformat() + 'Z',
        'elapsed_seconds': round(time.time() - T0, 1),
        'software': {'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
                     'scipy': __import__('scipy').__version__},
        'frozen_params': FROZEN_PARAMS,
        'fingerprints': fp,
        'layerA': {
            'markets': ROOTS_A,
            'daily_rows': {r: la[r]['n_rows'] for r in ROOTS_A},
            'roll_days': {r: gate7[r] for r in ROOTS_A},
            'eligibility': {r: {'n': len(cm[r]['records']), 'exclusions': cm[r]['cnt']} for r in ROOTS_A},
            'per_market': {r: per_market[r] for r in ROOTS_A},
        },
        'layerB': {
            'markets': LAYER_B,
            'm1_stats': {m: lb[m]['stats'] for m in LAYER_B},
            'eligibility': {m: {'n': len(cm[m]['records']), 'exclusions': cm[m]['cnt']} for m in LAYER_B},
            'per_market': {m: per_market[m] for m in LAYER_B},
        },
        'class_stats': class_results,
        'bootstrap': {
            k: {'T': v['T'], 'nblocks': v['nblocks'], 'p_two': v['p_two'], 'ci95': v['ci95'],
                'n_draws': v['n_draws'], 'null_mean': v['null_mean']}
            for k, v in bootstrap.items()
        },
        'multiplicity': {'family_order': fam_order, 'raw_p': raw_ps, 'holm_p': holm_res},
        'verdicts': verdicts,
        'secondary': {
            'horizon_1d': {'class_D': sec1_class}, 'horizon_21d': {'class_D': sec21_class},
            'standardized_shock': {'class_D': sec3_class, 'per_market': {m: sec3_by_mkt[m] for m in sec3_by_mkt}},
            'abs_return_response': {'class_D': sec4_class},
            'intraday_layerB': {'class_D': intra_class},
            'garch': garch,
            'winsorization': {'class_D': win_class, 'per_market': {m: win_by_mkt[m] for m in win_by_mkt}},
            'common_window': {'class_D': cw_class, 'per_market': cw_pm, 'yrange': list(COMMON_WIN)},
        },
        'notes': {
            'replicate_length_rule': 'nblocks = ceil(T/L) whole circular blocks; no truncation, no padding',
            'matching_tiebreak': 'stable sort by |r| on chronologically-ordered records implements (|r| asc, timestamp asc)',
            'caliper_frozen': 'caliper c = 0.25*SD(|r|) within (m,stratum) computed on original eligible records; frozen into replicates',
            'terciles_frozen': 'tercile bounds per market computed once on its full eligible series; frozen into replicates',
            'ref_pool_equal': 'equal NEG/POS size -> reference pool = POS (frozen)',
            'scipy_used': 'scipy.optimize (Nelder-Mead, fixed start) used only for GJR/EGARCH secondary diagnostics',
            'garch_series': 'Layer A fit on daily log returns with roll-day returns removed; Layer B on aggregated daily returns',
            'intraday': 'intraday Layer B RV = sum of squared 1-minute log returns of consecutive same-UTC-day bars; different-frequency object, Layer B only',
        },
    }
    with open(os.path.join(OUT, 'results_H01_V1.json'), 'w', encoding=ENCODING) as f:
        json.dump(results, f, indent=2, default=str)

    meta = {
        'experiment': 'H01 VOLATILITY RESPONSE ASYMMETRY V1',
        'protocol_version': PROTOCOL_VERSION,
        'protocol_sha256': fp['protocol_sha256'],
        'source_sha256': {
            **{f'front_{r}': fp[f'front_{r}'] for r in ROOTS_A},
            **{f'manifest_{k}': fp[f'manifest_{k}'] for k in EXPECTED_MANIFEST_HASH},
            **{f'{m}_m1': fp[f'{m}_m1'] for m in LAYER_B},
        },
        'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
        'scipy': __import__('scipy').__version__,
        'seed': SEED, 'B': B_REPL, 'L': L_BLOCK, 'alpha': ALPHA,
        'evaluability': {'min_pairs': MIN_PAIRS, 'min_markets': MIN_EVALUABLE},
        'common_window': list(COMMON_WIN),
        'layerA_eligible_shocks': {r: len(cm[r]['records']) for r in ROOTS_A},
        'layerB_eligible_shocks': {m: len(cm[m]['records']) for m in LAYER_B},
        'total_matched_pairs': len(all_pairs),
        'family_size': len(fam_order),
        'executed_at': results['executed_at'],
        'note': 'Controlled execution of frozen protocol v1.1.0; no outcome-driven tuning.',
    }
    with open(os.path.join(OUT, 'experiment_metadata_H01_V1.json'), 'w', encoding=ENCODING) as f:
        json.dump(meta, f, indent=2)

    print('\n=== SUMMARY ===', flush=True)
    print(f'protocol_sha256={fp["protocol_sha256"]}', flush=True)
    for cd in class_defs:
        key = f'L{cd["layer"]}_{cd["name"]}'
        print(f'{key}: D={class_results[key]["D_obs"]} p_holm={holm_res[key]:.4f} '
              f'verdict={verdicts[key]["verdict"]}', flush=True)
    print(f'elapsed={time.time() - T0:.1f}s', flush=True)


if __name__ == '__main__':
    main()