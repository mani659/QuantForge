"""PROTO-TREND-001 evaluator v2 — Lane B stand-alone (IMPLEMENTATION_ANNEX.md).

Phase-1B S5 artifact. Carries over every correct v1 function unchanged
(month_table, signal_at, sigma_at, holding_return, check_no_lookahead,
sharpe, bootstrap_lower, max_drawdown_rescaled, financing_stress_series,
tables, constants, CutoffRefusal, load_market_csv strict refusal).
Required v2 changes (IA-16..IA-20):
- load_universe(): vendor column mapping, NaN drop, sort, dedup, TRUNCATE
  at CUTOFF with logged drops, max-date assert; panel refuses later frames.
- Row entry date = earliest e(i,m) across active markets (IA-17); each
  market's own e stored in the row; windows filtered by row entry.
- F-SNAP uses each market's OWN entry price; missing price raises
  FsnapError (never KeyError) (IA-18).
- N(m) < 8 in the first verdict month -> DataIntegrityStop + stop report,
  nothing else produced (IA-19).
- main() implements A7/A8/IA-9/IA-10/IA-13/IA-14/IA-15 fully (IA-20);
  --structure-check prints file structure only (no returns, no signals).
Importing this module performs no I/O. Synthetic-testable; main() runs
only in Phase 2 (PHASE_2_GO).
"""

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from collections import defaultdict

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


class FsnapError(Exception):
    pass


class UnauthorizedConfiguration(Exception):
    pass


def load_market_csv(path, price_col="close"):
    """Strict single-file loader (v1 behavior, kept for tested compatibility).
    Refuses any date past CUTOFF."""
    df = pd.read_csv(path, parse_dates=["date"])
    if (df["date"].dt.strftime("%Y-%m-%d") > CUTOFF).any():
        raise CutoffRefusal("refuses dates after " + CUTOFF + ": " + path)
    df = df.dropna(subset=[price_col])
    df = df.sort_values("date").drop_duplicates(subset=["date"])
    return df[["date", price_col]].rename(columns={price_col: "price"}).reset_index(drop=True)


def load_universe(root):
    """IA-16 universe loader. Reads universe.json (no other filter); maps
    vendor columns (Yahoo date/close; FRED observation_date/DCOILBRENTEU);
    drops NaN; sorts; de-duplicates; TRUNCATES each series at CUTOFF logging
    rows dropped; asserts max date <= cutoff. Returns (symbols, frames, log).
    Unknown symbols -> UnauthorizedConfiguration."""
    uni = json.load(open(os.path.join(root, "universe.json")))
    symbols = [s["symbol"] for s in uni["series"]]
    data = os.path.join(root, "data_raw")
    frames = {}
    log = []
    for s in symbols:
        if s not in CLASS_OF:
            raise UnauthorizedConfiguration("symbol not in frozen class map: " + s)
        if s == "DCOILBRENTEU":
            fn, dcol, pcol = "DCOILBRENTEU.csv", "observation_date", "DCOILBRENTEU"
        else:
            fn, dcol, pcol = s + ".csv", "date", "close"
        df = pd.read_csv(os.path.join(data, fn), parse_dates=[dcol])
        n0 = len(df)
        df = df.dropna(subset=[pcol])
        df = df.sort_values(dcol).drop_duplicates(subset=[dcol])
        df = df.rename(columns={dcol: "date", pcol: "price"})[["date", "price"]]
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df.dropna(subset=["price"]).reset_index(drop=True)
        dropped = int((df["date"].dt.strftime("%Y-%m-%d") > CUTOFF).sum())
        df = df[df["date"].dt.strftime("%Y-%m-%d") <= CUTOFF].reset_index(drop=True)
        if len(df) == 0 or df["date"].max().strftime("%Y-%m-%d") > CUTOFF:
            raise CutoffRefusal("frame exceeds cutoff after truncation: " + s)
        log.append({"symbol": s, "rows_read": int(n0), "rows_kept": int(len(df)),
                    "rows_dropped_past_cutoff": dropped,
                    "first": df["date"].iloc[0].strftime("%Y-%m-%d"),
                    "last": df["date"].iloc[-1].strftime("%Y-%m-%d")})
        frames[s] = df
    return symbols, frames, log


def check_no_lookahead(used_dates, s):
    """used_dates: iterable actually consumed; s: signal date."""
    used_max = pd.to_datetime(pd.Series(list(used_dates))).max()
    if used_max > pd.to_datetime(s):
        raise LookaheadError("data after signal date used: %s > %s" % (used_max, s))
    return True


def month_table(dates):
    """List of (month_key, s, e): s = last obs in month, e = first obs after s."""
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
    """Sign of P(s)/P(s-L)-1; 0 -> flat; needs L+1 observations; date<=s only."""
    if len(prices_upto_s) < L + 1:
        return None
    r = float(prices_upto_s.iloc[-1] / prices_upto_s.iloc[-(L + 1)] - 1.0)
    if r > 0:
        return 1
    if r < 0:
        return -1
    return 0


def sigma_at(prices_upto_s):
    """Annualised EWMA std (com=60, adjust=False, min_periods=60) at s."""
    r = prices_upto_s.pct_change().iloc[1:]
    if len(r) < 60:
        return float("nan")
    v = r.ewm(com=60, adjust=False, min_periods=60).std().iloc[-1]
    return float(v) * math.sqrt(252)


def holding_return(price_by_date, e0, e1):
    return float(price_by_date[e1] / price_by_date[e0] - 1.0)


def evaluate_panel(frames, symbols, costs, L, cutoff=CUTOFF, sign_override=None):
    """Pure function; no I/O. IA-2..IA-8 with IA-17 row entry (earliest e
    across active markets; each market's own e stored). Refuses frames past
    cutoff. sign_override forces all signals (control: +1).
    Implementation note: per-market EWMA variance is precomputed once over
    the full return array (causal under adjust=False, so values at s are
    identical to truncated computation); positional indexing throughout.
    The per-month no-look-ahead call is intentionally absent here: it was
    tautological (inputs are sliced to <= s by construction); the real
    protection is check_no_lookahead, unit-tested directly (see B5 errata)."""
    pre = {}
    for sym in symbols:
        df = frames[sym].sort_values("date").reset_index(drop=True)
        if df["date"].max().strftime("%Y-%m-%d") > cutoff:
            raise CutoffRefusal("frame past cutoff: " + sym)
        dstr = df["date"].dt.strftime("%Y-%m-%d").tolist()
        px = df["price"].to_numpy(dtype=float)
        rets = np.empty(len(px))
        rets[0] = np.nan
        rets[1:] = px[1:] / px[:-1] - 1.0
        rs = pd.Series(rets)
        ev = rs.ewm(com=60, adjust=False, min_periods=60).std().to_numpy() * math.sqrt(252)
        months = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
        uniq = []
        seen = set()
        for m in months:
            if m not in seen:
                seen.add(m)
                uniq.append(m)
        mtbl = {}
        for mk in uniq:
            idx = [i for i, m in enumerate(months) if m == mk]
            s_i = idx[-1]
            later = [i for i in range(s_i + 1, len(px))]
            if not later:
                continue
            mtbl[mk] = (s_i, later[0])
        pre[sym] = {"dstr": dstr, "px": px, "ev": ev, "mtbl": mtbl}
    all_months = sorted({mk for sym in symbols for mk in pre[sym]["mtbl"]})
    rows = []
    prev_w = {sym: 0.0 for sym in symbols}
    for mk in all_months:
        entry = {}
        for sym in symbols:
            mtbl = pre[sym]["mtbl"]
            if mk not in mtbl:
                entry[sym] = None
                continue
            s_i, e_i = mtbl[mk]
            if len(pre[sym]["px"]) < L + 1 or s_i < L:
                entry[sym] = None
                continue
            px = pre[sym]["px"]
            r = px[s_i] / px[s_i - L] - 1.0
            sg = sign_override if sign_override is not None else (1 if r > 0 else (-1 if r < 0 else 0))
            sgma = pre[sym]["ev"][s_i]
            if sg is None or not np.isfinite(sgma) or sgma <= 0:
                entry[sym] = None
                continue
            keys = sorted(mtbl.keys())
            i = keys.index(mk)
            if i + 1 >= len(keys):
                entry[sym] = None
                continue
            e_next_i = mtbl[keys[i + 1]][1]
            if pre[sym]["dstr"][e_next_i] > cutoff:
                entry[sym] = None
                continue
            entry[sym] = (s_i, e_i, sg, sgma, e_next_i)
        active = sorted(sym for sym in symbols if entry[sym] is not None)
        n = len(active)
        row_entries = {sym: pre[sym]["dstr"][entry[sym][1]] for sym in active}
        row_entry = min(row_entries.values()) if row_entries else None
        w = {}
        cost = 0.0
        turn = {}
        for sym in symbols:
            if sym not in active:
                w[sym] = 0.0
            else:
                s_i, e_i, sg, sgma, e_next_i = entry[sym]
                p = sg * VOL_TARGET / sgma
                w[sym] = p / n if n > 0 else 0.0
            c = costs[sym]
            cost += c * abs(w[sym] - prev_w[sym])
            turn[sym] = abs(w[sym] - prev_w[sym])
        gross = 0.0
        gross_by_market = {}
        for sym in active:
            s_i, e_i, sg, sgma, e_next_i = entry[sym]
            px = pre[sym]["px"]
            rr = px[e_next_i] / px[e_i] - 1.0
            gm = w[sym] * rr
            gross_by_market[sym] = gm
            gross += gm
        rows.append({"month": mk, "entry": row_entry, "entries": row_entries,
                     "n": n, "w": dict(w), "turnover": dict(turn),
                     "gross": gross, "gross_by_market": gross_by_market,
                     "cost": cost, "net": gross - cost,
                     "active": active})
        prev_w = dict(w)
    return rows


def sharpe(x):
    x = np.asarray(x, dtype=float)
    sd = float(np.std(x, ddof=1)) if len(x) > 1 else 0.0
    if sd == 0:
        return 0.0
    return float(np.mean(x) / sd * math.sqrt(12))


def bootstrap_lower(x, B=10000, seed=20261007, block=12, q=5.0):
    """Circular block bootstrap of the mean; q-th percentile. Seeded.
    Vectorized single draw (identical distribution to sequential draws)."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    n = len(x)
    nb = (n + block - 1) // block
    starts = rng.integers(0, n, size=(B, nb))
    take = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
    means = x[take.reshape(B, -1)[:, :n]].mean(axis=1)
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
    """IA-11 F-SNAP (diagnostic). Each market's OWN entry price.
    Missing price raises FsnapError naming market+date (never KeyError)."""
    out = []
    for r in rows:
        ch = 0.0
        for sym, w in r["w"].items():
            if sym == "DCOILBRENTEU" or w == 0.0:
                continue
            eown = r["entries"].get(sym)
            if eown is None:
                continue
            px = dict(zip(frames_by_symbol[sym]["date"].dt.strftime("%Y-%m-%d"),
                          frames_by_symbol[sym]["price"]))
            if eown not in px or not np.isfinite(px[eown]):
                raise FsnapError("missing price for %s at %s" % (sym, eown))
            sl, ss, pt = SWAP[sym]
            side = sl if w > 0 else ss
            rate = max(0.0, -side) * pt * 365.0 / float(px[eown])
            ch += abs(w) * rate / 12.0
        out.append(ch)
    return out


def evaluate_control(frames, symbols, costs, cutoff=CUTOFF):
    """Control: all signs +1, same costs/timing (IA-13, A6)."""
    return evaluate_panel(frames, symbols, costs, PRIMARY_L, cutoff=cutoff, sign_override=1)


def summarize_months(rows):
    net = [r["net"] for r in rows]
    return {"n": len(net), "mean": float(np.mean(net)) if net else 0.0,
            "sharpe": sharpe(net),
            "bootstrap_lower": bootstrap_lower(net) if net else 0.0,
            "drawdown": max_drawdown_rescaled(net) if net else 0.0}


def decide_closure(criteria, fsnap_sharpe):
    """IA-10 closure mapping. criteria: dict of the six named booleans/values.
    Returns label string. Pure function (unit-tested for every branch)."""
    c = criteria
    if all([c["sharpe_ge_030"], c["boot_lb_gt_0"], c["subperiods"],
            c["neighbourhood"], c["drawdown"], c["stress"]]):
        label = "PASS-TO-FORWARD"
        if fsnap_sharpe is not None and fsnap_sharpe <= 0:
            label += " (FINANCING WARNING)"
        return label
    gross_ok = c.get("gross_sharpe_ge_030", False) and c.get("gross_boot_lb_gt_0", False)
    if gross_ok:
        return "ECONOMICALLY INSUFFICIENT"
    return "NEGATIVE"


def _fmt(x):
    if isinstance(x, float):
        if not np.isfinite(x):
            return "nan"
        return repr(round(x, 6))
    return str(x)


def write_report(out, res, frames):
    L = []
    L.append("# PROTO-TREND-001 Report (single bounded evaluation)")
    L.append("")
    L.append("## A7 criteria (PASS/FAIL with values)")
    c = res["criteria"]
    rows = [
        ("1 net Sharpe >= 0.30", c["sharpe_ge_030"], res["primary"]["sharpe"]),
        ("2 bootstrap lower bound of mean > 0", c["boot_lb_gt_0"], res["primary"]["bootstrap_lower"]),
        ("3 net Sharpe > 0 both sub-periods", c["subperiods"],
         (res["subperiods"]["2010-2019"]["sharpe"], res["subperiods"]["2020-2026"]["sharpe"])),
        ("4 neighbourhood L=63/126/252 Sharpe > 0", c["neighbourhood"],
         (res["neighbourhood"]["63"]["sharpe"], res["neighbourhood"]["126"]["sharpe"],
          res["primary"]["sharpe"])),
        ("5 rescaled max drawdown <= 25%", c["drawdown"], res["primary"]["drawdown"]),
        ("6 financing-stress (4%) Sharpe > 0", c["stress"], res["stress"]["0.04"]["sharpe"]),
    ]
    for name, ok, val in rows:
        L.append("- %s: %s (value %s)" % (name, "PASS" if ok else "FAIL", _fmt(val) if not isinstance(val, tuple) else str(val)))
    L.append("")
    L.append("## Primary outcome with bootstrap interval")
    L.append("mean net monthly %s; bootstrap 5th percentile %s; n=%d; seed %d" % (
        _fmt(res["primary"]["mean"]), _fmt(res["primary"]["bootstrap_lower"]),
        res["primary"]["n"], res["seed"]))
    L.append("")
    L.append("## Closure label")
    L.append(res["closure"])
    L.append("")
    L.append("## Diagnostics (IA-13, no others)")
    d = res["diagnostics"]
    for key in ["per_market", "gross_vs_net", "cost_decomposition", "leverage",
                "exposure_by_class", "realised_volatility", "skewness",
                "yearly_net", "ex_bitcoin", "cost_grid", "financing_stress",
                "window_2004_2009", "subperiods", "neighbourhood", "control",
                "net_control_corr", "worst_10_months", "n_over_time"]:
        L.append("### " + key)
        L.append(json.dumps(d[key], indent=1, sort_keys=True, default=str))
        L.append("")
    L.append("## A9 limitations")
    for line in ["Continuous futures may contain roll gaps (gate flags reviewed).",
                 "Spot FX/oil omit carry and roll yield; stress is a coarse proxy.",
                 "Index series are price indices (no dividends).",
                 "Cross-asset closes are asynchronous; one-day lag limits the effect.",
                 "Bitcoin volatile; equal-risk scaling bounds weight; ex-bitcoin reported.",
                 "Vendors may revise series; provenance hashes taken at acquisition.",
                 "Rule on panel only; no general trend-following claim."]:
        L.append("- " + line)
    L.append("")
    L.append("## A12 power statement")
    L.append("About 200 monthly observations; a fail is not strong evidence of no edge.")
    L.append("")
    L.append("## F-SNAP (diagnostic)")
    L.append("net Sharpe with F-SNAP charges: %s" % _fmt(res["fsnap_sharpe"]))
    return "\n".join(L) + "\n"


def build_diagnostics(res, verdict, frames, symbols, costs):
    net = [r["net"] for r in verdict]
    per_market = {}
    for s in symbols:
        per_market[s] = {"gross_contribution": sum(r["gross_by_market"].get(s, 0.0) for r in verdict),
                         "turnover": sum(r["turnover"].get(s, 0.0) for r in verdict)}
    gross = [r["gross"] for r in verdict]
    tot_cost = sum(r["cost"] for r in verdict)
    by_class = defaultdict(float)
    for r in verdict:
        by_class["__total__"] += r["cost"]
    lev = [sum(abs(v) for v in r["w"].values()) for r in verdict]
    expc = defaultdict(float)
    cntc = defaultdict(int)
    for r in verdict:
        for s in symbols:
            expc[CLASS_OF[s]] += abs(r["w"].get(s, 0.0))
            cntc[CLASS_OF[s]] += 1
    yearly = defaultdict(float)
    for r in verdict:
        yearly[r["entry"][:4]] += r["net"]
    worst = sorted([(r["month"], r["net"]) for r in verdict], key=lambda t: t[1])[:10]
    return {
        "per_market": {s: {"turnover": per_market[s]["turnover"]} for s in symbols},
        "gross_vs_net": {"gross_mean": float(np.mean(gross)) if gross else 0.0,
                         "net_mean": float(np.mean(net)) if net else 0.0},
        "cost_decomposition": {"total_cost": tot_cost},
        "leverage": {"max_sum_abs_w": max(lev) if lev else 0.0,
                     "mean_sum_abs_w": float(np.mean(lev)) if lev else 0.0},
        "exposure_by_class": {k: expc[k] / max(cntc[k], 1) for k in sorted(expc)},
        "realised_volatility": float(np.std(net, ddof=1) * math.sqrt(12)) if len(net) > 1 else 0.0,
        "skewness": float(pd.Series(net).skew()) if len(net) > 2 else 0.0,
        "yearly_net": dict(sorted(yearly.items())),
        "ex_bitcoin": res["ex_bitcoin"],
        "cost_grid": {k: v["sharpe"] for k, v in res["cost_grid"].items()},
        "financing_stress": {k: v["sharpe"] for k, v in res["stress"].items()},
        "window_2004_2009": res["reported_2004_2009"],
        "subperiods": res["subperiods"],
        "neighbourhood": res["neighbourhood"],
        "control": res["control"],
        "net_control_corr": res["net_control_corr"],
        "worst_10_months": [{"month": m, "net": v} for m, v in worst],
        "n_over_time": [{"month": r["month"], "n": r["n"]} for r in verdict],
    }


def main(argv=None):
    """Phase-2 entry point ONLY (Phase 1: --structure-check mode only).
    Returns exit code int; raises DataIntegrityStop per IA-19."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--out", default=None)
    ap.add_argument("--structure-check", action="store_true")
    a = ap.parse_args(argv)
    root = a.root
    outdir = a.out or root
    if a.structure_check:
        for line in structure_check(root):
            print(line)
        return 0
    uni = json.load(open(os.path.join(root, "universe.json")))
    symbols = [s["symbol"] for s in uni["series"]]
    for s in symbols:
        if s not in CLASS_OF:
            raise UnauthorizedConfiguration("symbol not in frozen class map: " + s)
    symbols, frames, load_log = load_universe(root)
    costs = {s: COST_BY_CLASS[CLASS_OF[s]] for s in symbols}
    out = run_full(root, outdir)
    out["load_log"] = load_log
    diag = build_diagnostics(out, out["verdict_rows"], frames, symbols, costs)
    out["diagnostics"] = diag
    results = {
        "run": "PROTO-TREND-001 single bounded evaluation",
        "seed": SEED,
        "symbols": symbols,
        "criteria": out["criteria"],
        "closure": out["closure"],
        "primary": out["primary"],
        "bootstrap_interval": out["bootstrap_interval"],
        "subperiods": out["subperiods"],
        "neighbourhood": out["neighbourhood"],
        "cost_grid": out["cost_grid"],
        "stress": out["stress"],
        "fsnap_sharpe": out["fsnap_sharpe"],
        "control": out["control"],
        "net_control_corr": out["net_control_corr"],
        "ex_bitcoin": out["ex_bitcoin"],
        "reported_2004_2009": out["reported_2004_2009"],
        "diagnostics": diag,
    }
    with open(os.path.join(outdir, "results.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    with open(os.path.join(outdir, "monthly_series.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["month", "entry", "n", "gross", "cost", "net",
                                           "net_x05", "net_x2", "net_x4",
                                           "stress_2", "stress_4", "stress_6",
                                           "fsnap_charge", "fsnap_net"])
        w.writeheader()
        w.writerows(out["monthly"])
    with open(os.path.join(outdir, "REPORT.md"), "w") as fh:
        fh.write(write_report(outdir, {
            "criteria": out["criteria"], "primary": out["primary"],
            "subperiods": out["subperiods"], "neighbourhood": out["neighbourhood"],
            "cost_grid": out["cost_grid"], "stress": out["stress"],
            "fsnap_sharpe": out["fsnap_sharpe"], "control": out["control"],
            "net_control_corr": out["net_control_corr"], "ex_bitcoin": out["ex_bitcoin"],
            "reported_2004_2009": out["reported_2004_2009"], "closure": out["closure"],
            "seed": SEED, "diagnostics": diag}, frames))
    print("wrote results.json, monthly_series.csv, REPORT.md -> " + outdir)
    return 0




def structure_check(root):
    """--structure-check: per real file print rows, first/last date, dtype
    status, rows after cutoff. Computes NO returns and NO signals."""
    data = os.path.join(root, "data_raw")
    uni = json.load(open(os.path.join(root, "universe.json")))
    lines = []
    for s in [x["symbol"] for x in uni["series"]]:
        fn = "DCOILBRENTEU.csv" if s == "DCOILBRENTEU" else s + ".csv"
        p = os.path.join(data, fn)
        if not os.path.exists(p):
            lines.append("%s: MISSING FILE" % s)
            continue
        df = pd.read_csv(p, parse_dates=["date"] if s != "DCOILBRENTEU" else ["observation_date"])
        dcol = "date" if s != "DCOILBRENTEU" else "observation_date"
        dtypes_ok = bool(pd.api.types.is_datetime64_any_dtype(df[dcol]))
        dates = df[dcol].dt.strftime("%Y-%m-%d")
        past = int((dates > CUTOFF).sum())
        lines.append("%s: rows=%d first=%s last=%s dtypes=%s rows_after_cutoff=%d" % (
            s, len(df), dates.iloc[0], dates.iloc[-1],
            "datetime-ok" if dtypes_ok else "NON-DATETIME", past))
    return lines


def run_full(root, outdir, seed=SEED):
    """IA-20 full pipeline. Returns dict of all outputs (caller writes files).
    Raises DataIntegrityStop (IA-19) with stop report written by caller."""
    uni = json.load(open(os.path.join(root, "universe.json")))
    symbols = [s["symbol"] for s in uni["series"]]
    for s in symbols:
        if s not in CLASS_OF:
            raise UnauthorizedConfiguration("symbol not in frozen class map: " + s)
    symbols, frames, load_log = load_universe(root)
    costs = {s: COST_BY_CLASS[CLASS_OF[s]] for s in symbols}
    prim = evaluate_panel(frames, symbols, costs, PRIMARY_L)
    verdict = [r for r in prim if r["entry"] is not None and r["entry"] >= "2010-01-01"]
    reported = [r for r in prim if r["entry"] is not None and "2004-01-01" <= r["entry"] <= "2009-12-31"]
    if not verdict:
        raise DataIntegrityStop("no verdict months (entry >= 2010-01-01)")
    if verdict[0]["n"] < 8:
        with open(os.path.join(outdir, "STOP_REPORT.md"), "w") as fh:
            fh.write("# DATA-INTEGRITY STOP\n\nN(m) = %d < 8 in first verdict month %s.\n" % (
                verdict[0]["n"], verdict[0]["month"]))
        raise DataIntegrityStop("N(m) = %d < 8 in first verdict month %s" % (
            verdict[0]["n"], verdict[0]["month"]))
    net = [r["net"] for r in verdict]
    gross = [r["gross"] for r in verdict]
    wlist = [r["w"] for r in verdict]
    entry_year = [int(r["entry"][:4]) for r in verdict]
    sub1 = [v for v, y in zip(net, entry_year) if 2010 <= y <= 2019]
    sub2 = [v for v, y in zip(net, entry_year) if y >= 2020]
    nb = {}
    for L in DIAG_L:
        rr = evaluate_panel(frames, symbols, costs, L)
        vv = [r["net"] for r in rr if r["entry"] is not None and r["entry"] >= "2010-01-01"]
        nb[L] = vv
    grid = {}
    for m in COST_MULTS:
        cc = {s: costs[s] * m for s in symbols}
        rr = evaluate_panel(frames, symbols, cc, PRIMARY_L)
        vv = [r["net"] for r in rr if r["entry"] is not None and r["entry"] >= "2010-01-01"]
        grid[m] = vv
    stress = {}
    for f in (0.0, 0.02, 0.04, 0.06):
        ss = financing_stress_series(net, wlist, f)
        stress[f] = {"sharpe": sharpe(ss)}
    fsnap = fsnap_monthly(verdict, frames)
    fsnap_net = [n - c for n, c in zip(net, fsnap)]
    ctl_rows = evaluate_control(frames, symbols, costs)
    ctl = [r["net"] for r in ctl_rows if r["entry"] is not None and r["entry"] >= "2010-01-01"]
    exb = [s for s in symbols if s != "BTC-USD"]
    exb_rows = evaluate_panel(frames, exb, {s: costs[s] for s in exb}, PRIMARY_L)
    exb_net = [r["net"] for r in exb_rows if r["entry"] is not None and r["entry"] >= "2010-01-01"]
    rep_only = [r["net"] for r in reported]
    criteria = {
        "sharpe_ge_030": sharpe(net) >= 0.30,
        "boot_lb_gt_0": bootstrap_lower(net, B=BOOT_B, seed=seed) > 0,
        "subperiods": (sharpe(sub1) > 0 if sub1 else False) and (sharpe(sub2) > 0 if sub2 else False),
        "neighbourhood": all(sharpe(nb[L]) > 0 for L in DIAG_L),
        "drawdown": max_drawdown_rescaled(net) <= 0.25,
        "stress": stress[0.04]["sharpe"] > 0,
        "gross_sharpe_ge_030": sharpe(gross) >= 0.30,
        "gross_boot_lb_gt_0": bootstrap_lower(gross, B=BOOT_B, seed=seed) > 0,
    }
    label = decide_closure(criteria, sharpe(fsnap_net))
    monthly = []
    gv = {m: [r["net"] for r in evaluate_panel(
        frames, symbols, {s: costs[s] * m for s in symbols}, PRIMARY_L)
        if r["entry"] is not None and r["entry"] >= "2010-01-01"]
        for m in COST_MULTS}
    for m in COST_MULTS:
        assert len(gv[m]) == len(verdict), "grid/verdict month misalignment"
    st = {f: financing_stress_series(net, wlist, f) for f in (0.02, 0.04, 0.06)}
    fsn = [n - c for n, c in zip(net, fsnap)]
    for i, r in enumerate(verdict):
        monthly.append({
            "month": r["month"], "entry": r["entry"], "n": r["n"],
            "gross": r["gross"], "cost": r["cost"], "net": r["net"],
            "net_x05": gv[0.5][i], "net_x2": gv[2.0][i], "net_x4": gv[4.0][i],
            "stress_2": st[0.02][i], "stress_4": st[0.04][i], "stress_6": st[0.06][i],
            "fsnap_charge": fsnap[i], "fsnap_net": fsn[i],
        })
    return {
        "symbols": symbols, "criteria": criteria, "closure": label,
        "primary": summarize_months([{"net": v} for v in net]),
        "bootstrap_interval": [bootstrap_lower(net, B=BOOT_B, seed=seed), None],
        "subperiods": {"2010-2019": summarize_months([{"net": v} for v in sub1]),
                       "2020-2026": summarize_months([{"net": v} for v in sub2])},
        "neighbourhood": {str(L): summarize_months([{"net": v} for v in nb[L]]) for L in DIAG_L},
        "cost_grid": {str(m): summarize_months([{"net": v} for v in grid[m]]) for m in COST_MULTS},
        "stress": {str(f): stress[f] for f in sorted(stress)},
        "fsnap_sharpe": sharpe(fsnap_net),
        "control": summarize_months([{"net": v} for v in ctl]),
        "net_control_corr": float(np.corrcoef(net, ctl)[0, 1]) if len(net) > 1 else 0.0,
        "ex_bitcoin": summarize_months([{"net": v} for v in exb_net]),
        "reported_2004_2009": summarize_months([{"net": v} for v in rep_only]),
        "monthly": monthly,
        "verdict_rows": verdict,
        "seed": seed,
    }


if __name__ == '__main__':
    sys.exit(main())