"""
V26 G1 Economic Plausibility Screen (v4 - fully optimized)
"""
import pandas as pd, numpy as np, os, json, warnings, time
warnings.filterwarnings("ignore")

FRIC = 2.0
DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "m1")
UTC4 = pd.Timedelta(hours=4)

def load(sym):
    df = pd.read_csv(f"{DIR}/{sym}_M1.csv", parse_dates=["timestamp"])
    df["timestamp"] += UTC4; df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True); df["date"] = df.index.date; return df

def compute_atr(df, period=14):
    tr = pd.DataFrame({
        "hl": df["high"] - df["low"],
        "hc": abs(df["high"] - df["close"].shift(1)),
        "lc": abs(df["low"] - df["close"].shift(1))
    }).max(axis=1)
    return tr.rolling(period, min_periods=1).mean().values

def atr_pct(atr, window=200):
    n = len(atr); result = np.full(n, np.nan)
    for i in range(window, n):
        w = atr[max(0,i-window):i+1]; valid = w[~np.isnan(w)]
        if len(valid) < 10: continue
        result[i] = (np.sum(valid < atr[i]) / len(valid)) * 100
    return result

def v3_evidence(name, tl, cf_list):
    result = {"name": name, "N": 0, "freq": 0, "mg": 0, "mdg": 0, "mn": 0, "mdn": 0,
        "wr": 0, "std": 0, "worst": 0, "best": 0, "cf_n": 0, "cf_mn": 0, "cf_mdn": 0,
        "cf_wr": 0, "delta_mean": 0, "delta_median": 0, "excl_best_mean": 0,
        "adjudication": "ZERO-EVENT", "g2_eligible": False}
    if not tl:
        print(f"  NO EVENTS"); return result
    t = pd.DataFrame(tl); n = len(t)
    yrs = max((t["date"].max() - t["date"].min()).days / 365.25, 0.1)
    freq = n / yrs; r = t["ret"]
    mg, mdg = r.mean(), r.median(); mn, mdn = mg - FRIC, mdg - FRIC
    wr = (r > 0).mean() * 100; std = r.std() if n > 1 else 0
    worst, best = r.min(), r.max()
    excl_best = r[r != r.max()].mean() - FRIC if n > 1 else mn
    print(f"  N={n} Freq={freq:.1f}/yr  Gross: Mean={mg:.2f} Med={mdg:.2f}  Net: Mean={mn:.2f} Med={mdn:.2f}")
    print(f"  WR={wr:.1f}%  Std={std:.2f}  Worst={worst:.2f}  Best={best:.2f}")

    if cf_list:
        c = pd.DataFrame(cf_list); cr = c["ret"]
        cf_mn, cf_mdn = cr.mean() - FRIC, cr.median() - FRIC
        cf_wr = (cr > 0).mean() * 100; dm, dd = mn - cf_mn, mdn - cf_mdn
        cfv = "TREATMENT SUPERIOR" if dm > 0 and dd > 0 else ("COUNTERFACTUAL SUPERIOR" if dm < 0 and dd < 0 else "MIXED")
        print(f"  CF: N={len(c)} MN={cf_mn:.2f} MDN={cf_mdn:.2f} WR={cf_wr:.1f}%  Delta: M={dm:.2f} D={dd:.2f}  {cfv}")
    else:
        cf_mn = cf_mdn = cf_wr = dm = dd = None; cfv = "NO-CONTROL-EVENTS"
        print(f"  CF: NO CONTROL EVENTS")
    result.update({"N":n,"freq":round(freq,1),"mg":round(mg,2),"mdg":round(mdg,2),
        "mn":round(mn,2),"mdn":round(mdn,2),"wr":round(wr,1),"std":round(std,2),
        "worst":round(worst,2),"best":round(best,2),"excl_best_mean":round(excl_best,2),
        "cf_n":len(cf_list) if cf_list else 0,
        "cf_mn":round(cf_mn,2) if cf_mn is not None else None,
        "cf_mdn":round(cf_mdn,2) if cf_mdn is not None else None,
        "cf_wr":round(cf_wr,1) if cf_wr is not None else None,
        "delta_mean":round(dm,2) if dm is not None else None,
        "delta_median":round(dd,2) if dd is not None else None,
        "cf_verdict":cfv})
    if cfv == "NO-CONTROL-EVENTS": adj = "INSUFFICIENT -- NO COUNTERFACTUAL"
    elif mn <= -2 and cfv in ("COUNTERFACTUAL SUPERIOR", "MIXED"): adj = "ECONOMICALLY NEGATIVE"
    elif mn <= 0 and cfv == "COUNTERFACTUAL SUPERIOR": adj = "ECONOMICALLY NEGATIVE"
    elif mn <= 0 and dm is not None and dm > 0: adj = "INFORMATIONALLY INTERESTING"
    elif mn > 0 and cfv in ("TREATMENT SUPERIOR", "MIXED"): adj = "ECONOMICALLY PROMISING"; result["g2_eligible"] = True
    elif mn > 0: adj = "ECONOMICALLY PROMISING"; result["g2_eligible"] = True
    else: adj = "INFORMATIONALLY INTERESTING"
    result["adjudication"] = adj; print(f"  ADJUDICATION: {adj}")
    return result

# ============================================================
def run_077(tech):
    print("\n--- CAND-077: Volatility Compression -> Expansion ---")
    t0 = time.time()
    closes = tech["close"].values; dates = tech["date"].values; n = len(tech)
    atr_vals = compute_atr(tech, 14); atr_p = atr_pct(atr_vals, 200)

    # Precompute: is bar i a valid breakout? (compressed recently + now expanding + breaks high)
    is_breakout = np.zeros(n, dtype=bool)
    comp_high = np.full(n, np.nan)
    for i in range(20, n):
        lb_pct = atr_p[max(0,i-20):i]; lb_close = closes[max(0,i-20):i]
        mask = lb_pct < 25
        if np.sum(mask) >= 10: comp_high[i] = np.max(lb_close[mask])

    for i in range(250, n - 30):
        if np.isnan(atr_p[i]) or atr_p[i] <= 50: continue
        recent_min = np.nanmin(atr_p[max(0,i-5):i+1])
        if np.isnan(recent_min) or recent_min >= 25: continue
        if np.isnan(comp_high[i]) or closes[i] <= comp_high[i]: continue
        is_breakout[i] = True

    # Precompute: is bar i a valid CF? (already expanded, breaks high)
    is_cf = np.zeros(n, dtype=bool)
    for i in range(250, n - 30):
        if np.isnan(atr_p[i]) or atr_p[i] <= 50: continue
        # Check that ATR pct has been >50 for 30+ bars
        preceding = atr_p[max(0,i-30):i+1]
        if np.any(np.isnan(preceding)) or np.nanmin(preceding) <= 50: continue
        c_h = np.max(closes[max(0,i-20):i]) if i >= 20 else 0
        if closes[i] > c_h:
            is_cf[i] = True

    # Match treatments to counterfactuals (by proximity)
    treat_indices = np.where(is_breakout)[0]
    cf_indices = np.where(is_cf)[0]
    print(f"  Treatment events: {len(treat_indices)}  CF events: {len(cf_indices)}  ({time.time()-t0:.1f}s)")

    t_list, cf_list = [], []
    for ti in treat_indices:
        treat_ret = (closes[ti+30] - closes[ti]) / closes[ti] * 10000
        t_list.append({"date": dates[ti], "ret": treat_ret})
        # Find nearest CF
        nearby = cf_indices[(cf_indices >= ti - 50) & (cf_indices <= ti + 50) & (cf_indices != ti)]
        if len(nearby) > 0:
            ci = nearby[0]
            cf_ret = (closes[ci+30] - closes[ci]) / closes[ci] * 10000
            cf_list.append({"date": dates[ci], "ret": cf_ret})

    print(f"  Match time: {time.time()-t0:.1f}s")
    return v3_evidence("CAND-077", t_list, cf_list)

def run_078(tech):
    print("\n--- CAND-078: Trend Exhaustion Transition ---")
    t0 = time.time()
    closes = tech["close"].values; dates = tech["date"].values; n = len(tech)

    consec = np.zeros(n, dtype=int)
    for i in range(1, n):
        d = 1 if closes[i] > closes[i-1] else (-1 if closes[i] < closes[i-1] else 0)
        pd_ = 1 if (i >= 2 and closes[i-1] > closes[i-2]) else (-1 if (i >= 2 and closes[i-1] < closes[i-2]) else 0)
        consec[i] = (consec[i-1] + 1) if (d == pd_ and d != 0) else (1 if d != 0 else 0)

    # Treatment: exhaustion after 8+ consecutive
    is_treat = np.zeros(n, dtype=bool)
    for i in range(10, n - 15):
        if consec[i-1] < 8: continue
        trend_dir = 1 if closes[i-1] > closes[i-2] else -1
        bar_dir = 1 if closes[i] > closes[i-1] else -1
        if bar_dir != trend_dir: is_treat[i] = True

    # CF: counter-trend after 2-4 consecutive
    is_cf = np.zeros(n, dtype=bool)
    for i in range(5, n - 15):
        if consec[i-1] < 2 or consec[i-1] > 4: continue
        if i < 2: continue
        c_trend_dir = 1 if closes[i-1] > closes[i-2] else -1
        c_bar_dir = 1 if closes[i] > closes[i-1] else -1
        if c_bar_dir != c_trend_dir: is_cf[i] = True

    treat_idx = np.where(is_treat)[0]
    cf_idx = np.where(is_cf)[0]
    print(f"  Treatment: {len(treat_idx)}  CF: {len(cf_idx)}  ({time.time()-t0:.1f}s)")

    t_list, cf_list = [], []
    for ti in treat_idx:
        trend_dir = 1 if closes[ti-1] > closes[ti-2] else -1
        treat_ret = (closes[ti+15] - closes[ti]) / closes[ti] * 10000 * (-trend_dir)
        t_list.append({"date": dates[ti], "ret": treat_ret})
        nearby = cf_idx[(cf_idx >= ti - 30) & (cf_idx <= ti + 30) & (cf_idx != ti)]
        if len(nearby) > 0:
            ci = nearby[0]
            c_trend_dir = 1 if closes[ci-1] > closes[ci-2] else -1
            cf_ret = (closes[ci+15] - closes[ci]) / closes[ci] * 10000 * (-c_trend_dir)
            cf_list.append({"date": dates[ci], "ret": cf_ret})

    return v3_evidence("CAND-078", t_list, cf_list)

def run_079(xau, tech):
    print("\n--- CAND-079: Gold Volatility Regime Transition -> Tech ---")
    t0 = time.time()
    xau_atr = compute_atr(xau, 14); xau_p = atr_pct(xau_atr, 200)
    xau_c = xau["close"].values; xau_o = xau["open"].values
    xau_d = xau["date"].values; xau_idx = xau.index; xau_n = len(xau)
    tech_c = tech["close"].values; tech_idx = tech.index

    # Precompute Gold volatility transitions
    is_trans = np.zeros(xau_n, dtype=bool)
    gold_moves = np.zeros(xau_n)
    for i in range(250, xau_n - 30):
        if np.isnan(xau_p[i]) or xau_p[i] <= 50: continue
        recent = xau_p[max(0,i-30):i+1]
        if np.all(np.isnan(recent)) or np.nanmin(recent) >= 25: continue
        gm = (xau_c[i] - xau_o[max(0,i-30)]) / xau_o[max(0,i-30)] * 10000
        if abs(gm) < 5: continue
        is_trans[i] = True; gold_moves[i] = gm

    # Precompute: is bar i a valid CF? (already-expanded Gold vol, stable for 30 bars)
    is_cf_gold = np.zeros(xau_n, dtype=bool)
    for i in range(250, xau_n - 30):
        if np.isnan(xau_p[i]) or xau_p[i] <= 50: continue
        preceding = xau_p[max(0,i-30):i+1]
        if np.any(np.isnan(preceding)) or np.nanmin(preceding) <= 50: continue
        is_cf_gold[i] = True

    trans_idx = np.where(is_trans)[0]
    cf_gold_idx = np.where(is_cf_gold)[0]
    print(f"  Gold transitions: {len(trans_idx)}  CF candidates: {len(cf_gold_idx)}  ({time.time()-t0:.1f}s)")

    t_list, cf_list = [], []
    for ti in trans_idx:
        gold_dir = 1 if gold_moves[ti] > 0 else -1
        g_ts = xau_idx[ti]
        e_ts, x_ts = g_ts + pd.Timedelta(minutes=30), g_ts + pd.Timedelta(minutes=60)
        te = np.where((tech_idx >= e_ts - pd.Timedelta(minutes=3)) & (tech_idx <= e_ts + pd.Timedelta(minutes=3)))[0]
        tx = np.where((tech_idx >= x_ts - pd.Timedelta(minutes=3)) & (tech_idx <= x_ts + pd.Timedelta(minutes=3)))[0]
        if len(te) < 1 or len(tx) < 1: continue
        treat_ret = (tech_c[tx[0]] - tech_c[te[0]]) / tech_c[te[0]] * 10000 * gold_dir
        t_list.append({"date": xau_d[ti], "ret": treat_ret})

        nearby = cf_gold_idx[(cf_gold_idx >= ti - 50) & (cf_gold_idx <= ti + 50) & (cf_gold_idx != ti)]
        if len(nearby) > 0:
            ci = nearby[0]
            c_ts = xau_idx[ci]
            c_e = c_ts + pd.Timedelta(minutes=30); c_x = c_ts + pd.Timedelta(minutes=60)
            c_te = np.where((tech_idx >= c_e - pd.Timedelta(minutes=3)) & (tech_idx <= c_e + pd.Timedelta(minutes=3)))[0]
            c_tx = np.where((tech_idx >= c_x - pd.Timedelta(minutes=3)) & (tech_idx <= c_x + pd.Timedelta(minutes=3)))[0]
            if len(c_te) >= 1 and len(c_tx) >= 1:
                cf_ret = (tech_c[c_tx[0]] - tech_c[c_te[0]]) / tech_c[c_te[0]] * 10000 * gold_dir
                cf_list.append({"date": xau_d[ci], "ret": cf_ret})

    print(f"  Match time: {time.time()-t0:.1f}s")
    return v3_evidence("CAND-079", t_list, cf_list)

if __name__ == "__main__":
    t_total = time.time()
    print("=" * 70)
    print("V26 G1 ECONOMIC PLAUSIBILITY SCREEN")
    print("=" * 70)
    print("\nLoading data...")
    xau = load("XAUUSD"); tech = load("USATECHIDXUSD")
    print(f"XAUUSD: {len(xau)} bars | USATECHIDXUSD: {len(tech)} bars")
    print("NOTE: Volume data is all zeros for both instruments. Volume filter removed.")

    r = {}
    r["CAND-077"] = run_077(tech)
    r["CAND-078"] = run_078(tech)
    r["CAND-079"] = run_079(xau, tech)

    print(f"\n{'='*70}\nSUMMARY\n{'='*70}")
    for c, v in r.items():
        g2 = "G2-ELIGIBLE" if v["g2_eligible"] else "NOT-ELIGIBLE"
        print(f"  {c}: N={v['N']} Net={v['mn']:.2f}bps {v['adjudication']} {g2}")
    print(f"\nTotal: {time.time()-t_total:.1f}s")
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "output", "research_discovery", "v26_g1_results.json")
    with open(out, "w") as f: json.dump(r, f, indent=2, default=str)
    print(f"Saved: {out}")
