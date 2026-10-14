"""PROTO-TREND-001 evaluator — Lane B stand-alone script (IMPLEMENTATION_ANNEX.md).

Phase-1 S5 artifact. Pure functions operate on in-memory price frames;
nothing here loads real vendor series except main(), which runs ONLY in
Phase 2 (PHASE_2_GO). Importing this module performs no I/O.

Conventions (frozen, IA-1..IA-11):
- prices: vendor Close column (auto_adjusted Yahoo) / FRED value; NaN rows dropped.
- signal month m: s = last observation in m; e = first observation after s.
- signal = sign(P(s)/P(s-L)-1), L in {252 primary; 63, 126 diagnostic}; 0 -> flat.
- sigma_hat = daily-simple-return ewm(com=60, adjust=False, min_periods=60).std()*sqrt(252) at s.
- p = signal * 0.10 / sigma_hat; ACTIVE iff L+1 obs, sigma>0, holding return with e(m+1) <= CUTOFF.
- w = p / N(active); G = sum(w*R); Cost = sum c(i)*|w-w_prev| (w=0 if not held prior).
- verdict months: entry >= 2010-01-01; reported-only 2004-01-01..2009-12-31;
  last month with e(m+1) <= CUTOFF; N<8 in first verdict month -> DATA-INTEGRITY STOP.
- Sharpe = mean/std(ddof=1)*sqrt(12), no rf; circular block bootstrap block=12,
  B=10000, seed 20261007, lower = 5th pct of bootstrap means.
- Drawdown on series rescaled by 0.10/(std*sqrt(12)), compounded monthly.
- Financing stress subtracts (f/12)*sum|w| for f in (0, 0.02, 0.04, 0.06); criterion at 0.04.
- F-SNAP per IA-11 swap table (Brent excluded); side by sign of p.
- Control: all signs +1, same costs/timing.
"""

import csv
import hashlib
import json
import math
import os
import sys

import numpy as np
import pandas as pd

CUTOFF = "2026-09-30"
SEED = 20261007
BOOT_B = 10000
BOOT_BLOCK = 12
PRIMARY_L = 252
DIAG_L = (63, 126)
COST_MULTS = (0.5, 1.0, 2.0, 4.0)
VOL_TARGET = 0.10

COST_BY_CLASS = {
    "fx": 0.0001,
    "gold": 0.00015,
    "silver": 0.0007,
    "equity": 0.0002,
    "brent": 0.0004,
    "bitcoin": 0.0007,
}
CLASS_OF = {
    "^GSPC": "equity", "^NDX": "equity", "^GDAXI": "equity",
    "^FTSE": "equity", "^N225": "equity",
    "EURUSD=X": "fx", "GBPUSD=X": "fx", "USDJPY=X": "fx",
    "AUDUSD=X": "fx", "USDCAD=X": "fx", "USDCHF=X": "fx",
    "GC=F": "gold", "SI=F": "silver",
    "DCOILBRENTEU": "brent", "BTC-USD": "bitcoin",
}
# swap_long / swap_short / point per IA-11 (G0 2026-10-07). Brent excluded.
SWAP = {
    "^GSPC": (-164.9, 0.0, 0.01), "^NDX": (-696.4, 0.0, 0.01),
    "^GDAXI": (-42.8, 0.0, 0.1), "^FTSE": (-168.6, 0.0, 0.01),
    "^N225": (0.0, 0.0, 0.1),
    "EURUSD=X": (-5.7, 0.0, 1e-5), "GBPUSD=X": (-2.2, -0.5, 1e-5),
    "USDJPY=X": (0.0, -13.9, 0.001), "AUDUSD=X": (0.0, -2.0, 1e-5),
    "USDCAD=X": (0.0, -8.9, 1e-5), "USDCHF=X": (0.0, -10.3, 1e-5),
    "GC=F": (-536.7, 0.0, 0.001), "SI=F": (-7.9, 0.0, 0.001),
    "BTC-USD": (-1886.4, 0.0, 0.01),
}


class DataIntegrityStop(Exception):
    pass


class LookaheadError(Exception):
    pass


class CutoffRefusal(Exception):
    pass


def load_market_csv(path, price_col="close"):
    """Read one vendor CSV into date->price frame. Refuses dates past CUTOFF."""
    df = pd.read_csv(path, parse_dates=["date"])
    if (df["date"].dt.strftime("%Y-%m-%d") > CUTOFF).any():
        raise CutoffRefusal("refuses dates after " + CUTOFF + ": " + path)
    df = df.dropna(subset=[price_col])
    df = df.sort_values("date").drop_duplicates(subset=["date"])
    return df[["date", price_col]].rename(columns={price_col: "price"}).reset_index(drop=True)


def check_no_lookahead(used_dates, s):
    """used_dates: iterable of date-likes actually consumed; s: signal date."""
    used_max = pd.to_datetime(pd.Series(list(used_dates))).max()
    if used_max > pd.to_datetime(s):
        raise LookaheadError("data after signal date used: %s > %s" % (used_max, s))
    return True


def month_table(dates):
    """Return list of (month_key, s, e): s = last obs in month, e = first obs after s."""
    dates = pd.to_datetime(pd.Series(dates)).reset_index(drop=True)
    months = dates.dt.strftime("%Y-%m")
    out = []
    uniq = months.drop_duplicates().tolist()
    for mk in uniq:
        idx = months[months == mk].index
        s = dates.loc[idx[-1]]
        after = dates[dates > s]
        if len(after) == 0:
            continue
        out.append((mk, s, after.iloc[0]))
    return out


def signal_at(prices_upto_s, L):
    """prices_upto_s: Series indexed 0..n-1 ending at s (date <= s only).
    Returns -1/0/+1 of P(s)/P(s-L)-1; needs L+1 observations."""
    if len(prices_upto_s) < L + 1:
        return None
    r = float(prices_upto_s.iloc[-1] / prices_upto_s.iloc[-(L + 1)] - 1.0)
    if r > 0:
        return 1
    if r < 0:
        return -1
    return 0


def sigma_at(prices_upto_s):
    """Annualised EWMA std (com=60, adjust=False, min_periods=60) at s; NaN if <60 returns."""
    r = prices_upto_s.pct_change().iloc[1:]
    if len(r) < 60:
        return float("nan")
    v = r.ewm(com=60, adjust=False, min_periods=60).std().iloc[-1]
    return float(v) * math.sqrt(252)


def holding_return(prices, e0, e1, price_by_date):
    return float(price_by_date[e1] / price_by_date[e0] - 1.0)


def evaluate_panel(frames, symbols, costs, L, cutoff=CUTOFF, sign_override=None):
    """frames: {symbol: DataFrame[date, price] sorted}. Returns monthly rows list of dicts.
    Pure function; no I/O. Implements IA-2..IA-8. sign_override forces all
    signals (control leg: +1)."""
    months_index = {}
    for sym in symbols:
        df = frames[sym]
        months_index[sym] = month_table(df["date"])
    # signal months = union over markets of months having s and e
    all_months = sorted({mk for sym in symbols for (mk, _, _) in months_index[sym]})
    rows = []
    prev_w = {sym: 0.0 for sym in symbols}
    for mk in all_months:
        entry = {}
        sig = {}
        ok = True
        for sym in symbols:
            tbl = {m: (s, e) for (m, s, e) in months_index[sym]}
            if mk not in tbl:
                entry[sym] = None
                continue
            s, e = tbl[mk]
            sub = frames[sym][frames[sym]["date"] <= s].reset_index(drop=True)
            check_no_lookahead(sub["date"], s)
            if len(sub) < L + 1:
                entry[sym] = None
                continue
            sg = (signal_at(sub["price"], L) if sign_override is None
                  else (sign_override if len(sub) >= L + 1 else None))
            sgma = sigma_at(sub["price"])
            if sg is None or not np.isfinite(sgma) or sgma <= 0:
                entry[sym] = None
                continue
            # holding return needs e of NEXT month
            entry[sym] = (s, e, sg, sgma, sub)
            sig[sym] = sg
        # holding returns need next month entry per market
        nxt = {}
        for sym in symbols:
            if entry[sym] is None:
                continue
            tbl = {m: (s, e) for (m, s, e) in months_index[sym]}
            keys = sorted(tbl.keys())
            i = keys.index(mk)
            if i + 1 >= len(keys):
                entry[sym] = None
                continue
            e_next = tbl[keys[i + 1]][1]
            if e_next.strftime("%Y-%m-%d") > cutoff:
                entry[sym] = None
                continue
            nxt[sym] = e_next
        active = [sym for sym in symbols if entry[sym] is not None]
        n = len(active)
        w = {}
        gross = 0.0
        cost = 0.0
        turn = {}
        for sym in symbols:
            if sym not in active:
                w[sym] = 0.0
            else:
                s, e, sg, sgma, sub = entry[sym]
                p = sg * VOL_TARGET / sgma
                w[sym] = p / n if n > 0 else 0.0
            c = costs[sym]
            cost += c * abs(w[sym] - prev_w[sym])
            turn[sym] = abs(w[sym] - prev_w[sym])
        for sym in active:
            s, e, sg, sgma, sub = entry[sym]
            pb = dict(zip(frames[sym]["date"].dt.strftime("%Y-%m-%d"), frames[sym]["price"]))
            rr = holding_return(None, e.strftime("%Y-%m-%d"), nxt[sym].strftime("%Y-%m-%d"), pb)
            gross += w[sym] * rr
        rows.append({"month": mk, "entry": str(entry[active[0]][1].date()) if active else None,
                     "n": n, "w": dict(w), "turnover": dict(turn),
                     "gross": gross, "cost": cost, "net": gross - cost,
                     "active": sorted(active)})
        # NOTE: months with n == 0 are KEPT as zero rows so N(m) is recorded
        # for every month (IA-7); verdict/window filtering happens downstream.
        prev_w = dict(w)
    return rows


def sharpe(x):
    x = np.asarray(x, dtype=float)
    sd = float(np.std(x, ddof=1)) if len(x) > 1 else 0.0
    if sd == 0:
        return 0.0
    return float(np.mean(x) / sd * math.sqrt(12))


def bootstrap_lower(x, B=10000, seed=20261007, block=12, q=5.0):
    """Circular block bootstrap of the mean; q-th percentile. Seeded."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    n = len(x)
    idx = np.arange(n)
    means = np.empty(B)
    for b in range(B):
        starts = rng.integers(0, n, size=(n + block - 1) // block)
        take = np.concatenate([(s + np.arange(block)) % n for s in starts])[:n]
        means[b] = x[take].mean()
    return float(np.percentile(means, q))


def max_drawdown_rescaled(x):
    x = np.asarray(x, dtype=float)
    sd = float(np.std(x, ddof=1)) if len(x) > 1 else 0.0
    if sd == 0:
        return 0.0
    k = 0.10 / (sd * math.sqrt(12))
    eq = np.cumprod(1.0 + x * k)
    peak = np.maximum.accumulate(eq)
    dd = (peak - eq) / peak
    return float(dd.max())


def financing_stress_series(net, weights_list, f):
    """net(m) - (f/12)*sum|w| per IA-10/IA-13 stress levels."""
    return [n - (f / 12.0) * sum(abs(v) for v in w.values()) for n, w in zip(net, weights_list)]


def fsnap_monthly(rows, frames_by_symbol):
    """IA-11 F-SNAP diagnostic (not a criterion). Brent excluded.
    rate = max(0,-swap)*point*365/price; charge = sum|w|*rate/12, side by sign of p."""
    out = []
    for r in rows:
        ch = 0.0
        for sym, w in r["w"].items():
            if sym == "DCOILBRENTEU" or w == 0.0:
                continue
            sl, ss, pt = SWAP[sym]
            side = sl if w > 0 else ss
            price = float(frames_by_symbol[sym].set_index("date").loc[r["entry"], "price"]) \
                if r["entry"] is not None else float("nan")
            rate = max(0.0, -side) * pt * 365.0 / price
            ch += abs(w) * rate / 12.0
        out.append(ch)
    return out


def evaluate_control(frames, symbols, costs, cutoff=CUTOFF):
    """Control: all signs +1, same costs/timing (IA-13, A6). Returns monthly rows."""
    return evaluate_panel(frames, symbols, costs, PRIMARY_L, cutoff=cutoff, sign_override=1)


def summarize_months(rows):
    net = [r["net"] for r in rows]
    return {"n": len(net), "mean": float(np.mean(net)) if net else 0.0,
            "sharpe": sharpe(net),
            "bootstrap_lower": bootstrap_lower(net) if net else 0.0,
            "drawdown": max_drawdown_rescaled(net) if net else 0.0}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def main():
    """Phase-2 entry point ONLY. Reads universe.json + data_raw, writes
    results.json, monthly_series.csv, REPORT.md. Never called in Phase 1."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root = a.root
    outdir = a.out or root
    uni = json.load(open(os.path.join(root, "universe.json")))
    symbols = [s["symbol"] for s in uni["series"]]
    data = os.path.join(root, "data_raw")
    frames = {}
    for s in symbols:
        fn = s + ".csv" if s != "DCOILBRENTEU" else "DCOILBRENTEU.csv"
        col = "close" if s != "DCOILBRENTEU" else "DCOILBRENTEU"
        df = pd.read_csv(os.path.join(data, fn), parse_dates=["date"])
        frames[s] = df.rename(columns={col: "price"})[["date", "price"]].dropna(
            subset=["price"]).sort_values("date").reset_index(drop=True)
    costs = {s: COST_BY_CLASS[CLASS_OF[s]] for s in symbols}
    log = []
    log.append("universe: %d series" % len(symbols))
    # verdict + reported windows, neighbourhood, control, criteria, diagnostics,
    # results.json / monthly_series.csv / REPORT.md per IA-13/IA-14/IA-15.
    raise SystemExit("main() executes only in Phase 2 (PHASE_2_GO).")


if __name__ == "__main__":
    main()
