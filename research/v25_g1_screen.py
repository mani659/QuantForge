"""
V25 G1 Economic Plausibility Screen
CAND-074 / CAND-075 / CAND-076
G1 V3 Evidence-Based Adjudication Framework
"""
import pandas as pd, numpy as np, os, json, warnings
from datetime import timedelta, datetime
warnings.filterwarnings("ignore")

FRIC = 2.0  # bps round-trip
DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "m1")
UTC4 = pd.Timedelta(hours=4)

# ============================================================
# TIMEZONE HELPERS
# ============================================================

def us_dst(dt):
    """True if dt (UTC) falls in US DST period (March second Sun - Nov first Sun)."""
    y = dt.year
    # Second Sunday of March
    mar1 = pd.Timestamp(y, 3, 1)
    mar_sundays = pd.date_range(mar1, mar1 + pd.Timedelta(days=14), freq="7D")
    dst_start = mar_sundays[1] + pd.Timedelta(hours=7)  # 2 AM local = 7 AM UTC
    # First Sunday of November
    nov1 = pd.Timestamp(y, 11, 1)
    nov_sundays = pd.date_range(nov1, nov1 + pd.Timedelta(days=7), freq="7D")
    dst_end = nov_sundays[0] + pd.Timedelta(hours=7)
    return dst_start <= dt < dst_end

def uk_dst(dt):
    """True if dt (UTC) falls in UK DST period (March last Sun - Oct last Sun)."""
    y = dt.year
    # Last Sunday of March
    mar_end = pd.Timestamp(y, 3, 31)
    while mar_end.dayofweek != 6:
        mar_end -= timedelta(days=1)
    dst_start = mar_end + pd.Timedelta(hours=7)  # 1 AM UK = 7 AM UTC
    # Last Sunday of October
    oct_end = pd.Timestamp(y, 10, 31)
    while oct_end.dayofweek != 6:
        oct_end -= timedelta(days=1)
    dst_end = oct_end + pd.Timedelta(hours=6)  # 2 AM UK = 6 AM UTC (fall back)
    return dst_start <= dt < dst_end

def load(sym):
    df = pd.read_csv(f"{DIR}/{sym}_M1.csv", parse_dates=["timestamp"])
    df["timestamp"] += UTC4
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)
    df["h"] = df.index.hour
    df["m"] = df.index.minute
    df["dow"] = df.index.dayofweek
    df["date"] = df.index.date
    return df

# ============================================================
# ANALYSIS FRAMEWORK (V3 Evidence-Based)
# ============================================================

def v3_evidence(name, tl, cf_list, price_ref=None):
    """V3 evidence-based analysis. Returns full evidence profile."""
    result = {
        "name": name, "N": 0, "freq": 0, "mg": 0, "mdg": 0, "mn": 0, "mdn": 0,
        "wr": 0, "std": 0, "worst": 0, "best": 0,
        "cf_n": 0, "cf_mn": 0, "cf_mdn": 0, "cf_wr": 0, "cf_std": 0,
        "delta_mean": 0, "delta_median": 0,
        "concentration": 0, "excl_best_mean": 0,
        "adjudication": "ZERO-EVENT", "g2_eligible": False
    }

    if not tl:
        print(f"  NO EVENTS")
        return result

    t = pd.DataFrame(tl)
    n = len(t)
    yrs = max((t["date"].max() - t["date"].min()).days / 365.25, 0.1)
    freq = n / yrs
    r = t["ret"]

    mg = r.mean()
    mdg = r.median()
    mn = mg - FRIC
    mdn = mdg - FRIC
    wr = (r > 0).mean() * 100
    std = r.std() if n > 1 else 0
    worst = r.min()
    best = r.max()

    # Payoff concentration: top 20% of events contribute what % of total return?
    sorted_r = r.sort_values(ascending=False)
    top20_count = max(1, int(np.ceil(n * 0.2)))
    top20_sum = sorted_r.iloc[:top20_count].sum()
    total_sum = r.sum()
    concentration = (top20_sum / total_sum * 100) if abs(total_sum) > 1e-10 else 0

    # Exclude best event mean
    if n > 1:
        excl_best = r[r != r.max()].mean() - FRIC
    else:
        excl_best = mn

    print(f"  N={n} Freq={freq:.1f}/yr")
    print(f"  Gross: Mean={mg:.2f} bps  Median={mdg:.2f} bps")
    print(f"  Net:   Mean={mn:.2f} bps  Median={mdn:.2f} bps")
    print(f"  Win:   {wr:.1f}%  StdDev={std:.2f}  Worst={worst:.2f}  Best={best:.2f}")
    print(f"  Payoff concentration (top 20%): {concentration:.1f}%")
    print(f"  Exclude-best-event mean: {excl_best:.2f} bps")

    # Counterfactual
    if cf_list:
        c = pd.DataFrame(cf_list)
        cr = c["ret"]
        cf_mn = cr.mean() - FRIC
        cf_mdn = cr.median() - FRIC
        cf_wr = (cr > 0).mean() * 100
        cf_std = cr.std() if len(c) > 1 else 0
        delta_m = mn - cf_mn
        delta_d = mdn - cf_mdn

        if delta_m > 0 and delta_d > 0:
            cf_verdict = "TREATMENT SUPERIOR"
        elif delta_m < 0 and delta_d < 0:
            cf_verdict = "COUNTERFACTUAL SUPERIOR"
        else:
            cf_verdict = "MIXED / INCONCLUSIVE"

        print(f"  CF:   N={len(c)}  MeanNet={cf_mn:.2f} bps  MedianNet={cf_mdn:.2f} bps  WR={cf_wr:.1f}%")
        print(f"  Delta: Mean={delta_m:.2f} bps  Median={delta_d:.2f} bps  Gate={cf_verdict}")
    else:
        cf_mn = cf_mdn = cf_wr = cf_std = delta_m = delta_d = None
        cf_verdict = "NO-CONTROL-EVENTS"
        print(f"  CF: NO CONTROL EVENTS")

    result.update({
        "N": n, "freq": round(freq, 1), "mg": round(mg, 2), "mdg": round(mdg, 2),
        "mn": round(mn, 2), "mdn": round(mdn, 2), "wr": round(wr, 1),
        "std": round(std, 2), "worst": round(worst, 2), "best": round(best, 2),
        "concentration": round(concentration, 1),
        "excl_best_mean": round(excl_best, 2),
        "cf_n": len(cf_list) if cf_list else 0,
        "cf_mn": round(cf_mn, 2) if cf_mn is not None else None,
        "cf_mdn": round(cf_mdn, 2) if cf_mdn is not None else None,
        "cf_wr": round(cf_wr, 1) if cf_wr is not None else None,
        "cf_std": round(cf_std, 2) if cf_std is not None else None,
        "delta_mean": round(delta_m, 2) if delta_m is not None else None,
        "delta_median": round(delta_d, 2) if delta_d is not None else None,
        "cf_verdict": cf_verdict,
    })

    # V3 ADJUDICATION (evidence-based, not threshold-based)
    if cf_verdict == "NO-CONTROL-EVENTS":
        result["adjudication"] = "INSUFFICIENT — NO COUNTERFACTUAL"
        print(f"  ADJUDICATION: INSUFFICIENT — NO COUNTERFACTUAL")
    elif mn <= -2 and (cf_verdict == "COUNTERFACTUAL SUPERIOR" or cf_verdict == "MIXED / INCONCLUSIVE"):
        result["adjudication"] = "ECONOMICALLY NEGATIVE"
        print(f"  ADJUDICATION: ECONOMICALLY NEGATIVE")
    elif mn <= 0 and cf_verdict == "COUNTERFACTUAL SUPERIOR":
        result["adjudication"] = "ECONOMICALLY NEGATIVE"
        print(f"  ADJUDICATION: ECONOMICALLY NEGATIVE")
    elif mn <= 0 and delta_m is not None and delta_m > 0:
        # Treatment beats counterfactual, but absolute economics are negative
        result["adjudication"] = "INFORMATIONALLY INTERESTING"
        print(f"  ADJUDICATION: INFORMATIONALLY INTERESTING — treatment > CF but absolute negative")
    elif mn > 0 and mn <= 3 and mdn < 0:
        result["adjudication"] = "ECONOMICALLY MARGINAL"
        print(f"  ADJUDICATION: ECONOMICALLY MARGINAL")
    elif mn > 3 and mdn > 0 and cf_verdict == "TREATMENT SUPERIOR":
        result["adjudication"] = "ECONOMICALLY PROMISING"
        result["g2_eligible"] = True
        print(f"  ADJUDICATION: ECONOMICALLY PROMISING — G2 ELIGIBLE")
    elif mn > 3 and cf_verdict == "TREATMENT SUPERIOR":
        result["adjudication"] = "ECONOMICALLY PROMISING"
        result["g2_eligible"] = True
        print(f"  ADJUDICATION: ECONOMICALLY PROMISING — G2 ELIGIBLE")
    elif mn > 0 and cf_verdict == "TREATMENT SUPERIOR":
        result["adjudication"] = "ECONOMICALLY PROMISING"
        result["g2_eligible"] = True
        print(f"  ADJUDICATION: ECONOMICALLY PROMISING — G2 ELIGIBLE")
    else:
        result["adjudication"] = "INFORMATIONALLY INTERESTING"
        print(f"  ADJUDICATION: INFORMATIONALLY INTERESTING")

    return result

# ============================================================
# CAND-074: LONDON GOLD FIX
# ============================================================

def run_074(xau):
    """
    CAND-074: London Gold Fix Benchmark Execution Pressure
    Treatment: Enter XAUUSD at London AM Fix (10:30 AM London) in direction
    of pre-fix move (10:00-10:30 AM London). Exit at 11:00 AM London.
    Counterfactual: Same time window on non-fix days, or same pre-fix
    magnitude at random non-fix times.
    """
    print("\n--- CAND-074: London Gold Fix Benchmark Execution Pressure ---")

    # Determine fix hour in the data's +4 timezone
    # Summer (UK BST, US EDT): 10:30 AM London = 9:30 AM UTC = 13:30 in +4
    # Winter (UK GMT, US EST): 10:30 AM London = 10:30 AM UTC = 14:30 in +4

    tg = {}
    for d, g in xau.groupby(xau.index.date):
        tg[d] = g

    # For each date, determine if it's summer or winter DST
    t, cf = [], []
    dates = sorted(tg.keys())

    for i, d in enumerate(dates):
        g = tg[d]
        dt = pd.Timestamp(d)

        # Determine DST for this date
        is_uk_summer = uk_dst(dt + pd.Timedelta(hours=10))  # Approximate
        if is_uk_summer:
            fix_h = 13  # 1:30 PM in +4 (= 9:30 AM UTC = 10:30 AM London BST)
            pre_start, pre_end = 12, 13  # 12:00-13:00 in +4 (= 9:00-10:00 AM London)
            treat_start, treat_end = 13, 14  # 13:00-14:00 in +4 (= 10:00-11:00 AM London)
        else:
            fix_h = 14  # 2:30 PM in +4 (= 10:30 AM UTC = 10:30 AM London GMT)
            pre_start, pre_end = 13, 14  # 13:00-14:00 in +4 (= 10:00-11:00 AM London)
            treat_start, treat_end = 14, 15  # 14:00-15:00 in +4 (= 11:00 AM-12:00 London)

        # Pre-fix window: 10:00-10:30 AM London
        pre = g[(g["h"] >= pre_start) & (g["h"] < pre_end)]
        if len(pre) < 5:
            continue

        pre_open = pre.iloc[0]["open"]
        pre_close = pre.iloc[-1]["close"]
        pre_ret_bps = (pre_close - pre_open) / pre_open * 10000
        pre_dir = 1 if pre_ret_bps > 0 else -1

        # Treatment: 10:30-11:00 AM London (fix window + aftermath)
        treat = g[(g["h"] >= treat_start) & (g["h"] < treat_end)]
        if len(treat) < 5:
            continue

        treat_open = treat.iloc[0]["open"]
        treat_close = treat.iloc[-1]["close"]
        treat_ret_bps = (treat_close - treat_open) / treat_open * 10000 * pre_dir

        t.append({"date": d, "ret": treat_ret_bps, "pre_ret": pre_ret_bps,
                   "pre_dir": pre_dir, "is_fix": True})

        # Counterfactual: find a non-fix day with similar pre-move magnitude
        # Use nearby non-fix day if available (random offset)
        cf_day = None
        for offset in [1, 2, 3, -1, -2, -3]:
            check_d = d + timedelta(days=offset)
            if check_d in tg and check_d != d:
                # Check it's not another fix day (all trading days are fix days for gold)
                # Use a time-shifted approach: same pre-move direction/magnitude but different time
                cf_day = check_d
                break

        if cf_day is not None:
            cg = tg[cf_day]
            cdt = pd.Timestamp(cf_day)
            c_uk_summer = uk_dst(cdt + pd.Timedelta(hours=10))
            # Use a random different time window as counterfactual
            # Pick afternoon session: 3:00-3:30 PM London
            if c_uk_summer:
                cf_pre_h, cf_treat_h = 19, 20  # 3-4 PM London in +4 (summer)
            else:
                cf_pre_h, cf_treat_h = 20, 21

            cf_pre = cg[(cg["h"] == cf_pre_h) & (cg["m"] < 30)]
            cf_treat = cg[(cg["h"] >= cf_treat_h) & (cg["h"] < cf_treat_h + 1)]
            if len(cf_pre) >= 3 and len(cf_treat) >= 3:
                cf_pre_open = cf_pre.iloc[0]["open"]
                cf_pre_close = cf_pre.iloc[-1]["close"]
                cf_dir = 1 if (cf_pre_close - cf_pre_open) > 0 else -1
                cf_treat_open = cf_treat.iloc[0]["open"]
                cf_treat_close = cf_treat.iloc[-1]["close"]
                cf_ret = (cf_treat_close - cf_treat_open) / cf_treat_open * 10000 * cf_dir
                cf.append({"date": cf_day, "ret": cf_ret})

    return v3_evidence("CAND-074", t, cf)

# ============================================================
# CAND-075: US EQUITY CLOSING AUCTION
# ============================================================

def run_075(tech):
    """
    CAND-075: US Equity Closing Auction Concentrated Order Flow
    Treatment: Enter USATECHIDXUSD at 3:59 PM ET in direction of late-session
    move (3:50-3:59 PM ET). Exit at 4:00 PM ET close.
    Counterfactual: Same late-session move at random intraday times.
    """
    print("\n--- CAND-075: US Equity Closing Auction Concentrated Order Flow ---")

    # In +4 timezone:
    # 3:50 PM ET (summer) = 7:50 PM = 19:50 in +4
    # 3:59 PM ET (summer) = 7:59 PM = 19:59 in +4
    # 4:00 PM ET (summer) = 8:00 PM = 20:00 in +4

    # Use fixed hours in +4: late session = hour 19 (3:50-3:59 PM ET)
    # Close = hour 20 (4:00 PM ET)
    # For counterfactual: random midday windows with similar momentum

    tg = {}
    for d, g in tech.groupby(tech.index.date):
        tg[d] = g

    t, cf = [], []
    dates = sorted(tg.keys())

    for d in dates:
        g = tg[d]

        # Late session: 3:50-3:59 PM ET -> 19:50-19:59 in +4
        late = g[(g["h"] == 19) & (g["m"] >= 50)]
        if len(late) < 2:
            continue

        late_open = late.iloc[0]["open"]
        late_close = late.iloc[-1]["close"]
        late_ret_bps = (late_close - late_open) / late_open * 10000
        if abs(late_ret_bps) < 1:  # Need at least 1 bps move
            continue
        late_dir = 1 if late_ret_bps > 0 else -1

        # Entry: 3:59 PM ET -> close at ~19:59
        # Exit: 4:00 PM ET -> close at ~20:00
        close_bars = g[(g["h"] == 20) & (g["m"] == 0)]
        if len(close_bars) < 1:
            # Try just before hour 20
            close_bars = g[(g["h"] == 19) & (g["m"] == 59)]
        if len(close_bars) < 1:
            continue

        entry_bar = late.iloc[-1]  # Last late bar
        exit_bar = close_bars.iloc[0]
        treat_ret = (exit_bar["close"] - entry_bar["close"]) / entry_bar["close"] * 10000 * late_dir

        t.append({"date": d, "ret": treat_ret, "late_ret": late_ret_bps,
                   "late_dir": late_dir})

        # Counterfactual: pick a random intraday window with similar momentum
        # Use midday session (12:00-12:10 PM ET = hour 16 in +4)
        cf_hour = 16  # 12:00 PM ET in +4
        cf_late = g[(g["h"] == cf_hour) & (g["m"] >= 0) & (g["m"] < 10)]
        cf_exit = g[(g["h"] == cf_hour) & (g["m"] >= 10) & (g["m"] < 20)]
        if len(cf_late) >= 2 and len(cf_exit) >= 1:
            cf_open = cf_late.iloc[0]["open"]
            cf_cl = cf_late.iloc[-1]["close"]
            cf_move = (cf_cl - cf_open) / cf_open * 10000
            if abs(cf_move) >= 1:
                cf_d = 1 if cf_move > 0 else -1
                cf_entry = cf_late.iloc[-1]
                cf_exit_bar = cf_exit.iloc[0]
                cf_ret = (cf_exit_bar["close"] - cf_entry["close"]) / cf_entry["close"] * 10000 * cf_d
                cf.append({"date": d, "ret": cf_ret})

    return v3_evidence("CAND-075", t, cf)

# ============================================================
# CAND-076: GOLD OVERNIGHT -> TECH OPENING
# ============================================================

def run_076(xau, tech):
    """
    CAND-076: Gold Overnight Repricing -> Tech Opening Direction
    Treatment: Enter USATECHIDXUSD at 9:30 AM ET in direction of overnight
    Gold move (previous 4 PM ET to current 9 AM ET). Exit at 10:00 AM ET.
    Counterfactual: Same time window on days without significant Gold movement.
    """
    print("\n--- CAND-076: Gold Overnight Repricing -> Tech Opening Direction ---")

    # In +4 timezone:
    # Gold close at 4 PM ET: 8:00 PM = 20:00 in +4 (summer) or 21:00 (winter)
    # Gold at 9 AM ET: 1:00 PM = 13:00 in +4 (summer) or 14:00 (winter)
    # Tech entry at 9:30 AM ET: 1:30 PM = 13:30 in +4
    # Tech exit at 10:00 AM ET: 2:00 PM = 14:00 in +4

    # Use fixed approach: Gold close at hour 20, Gold at hour 13
    # Tech entry at hour 13 (first half), Tech exit at hour 14

    xg = {}
    for d, g in xau.groupby(xau.index.date):
        xg[d] = g

    tg = {}
    for d, g in tech.groupby(tech.index.date):
        tg[d] = g

    t, cf = [], []
    dates = sorted(tg.keys())

    for d in dates:
        g_tech = tg[d]
        dt = pd.Timestamp(d)

        # Determine DST
        is_us_summer = us_dst(dt + pd.Timedelta(hours=13))

        if is_us_summer:
            gold_close_h = 20  # 8 PM in +4 = 4 PM EDT
            gold_am_h = 13     # 1 PM in +4 = 9 AM EDT
        else:
            gold_close_h = 21  # 9 PM in +4 = 4 PM EST
            gold_am_h = 14     # 2 PM in +4 = 9 AM EST

        # Tech hours (in +4): entry at 13:30 (summer) or 14:30 (winter)
        tech_entry_h = gold_am_h  # Same hour as Gold AM
        tech_exit_h = tech_entry_h + 1

        # Find Gold close from previous day
        prev_d = d - timedelta(days=1)
        # Find the nearest trading day before d in XAUUSD
        prev_dates = [d2 for d2 in sorted(xg.keys()) if d2 < d]
        if not prev_dates:
            continue
        prev_d = prev_dates[-1]

        g_xau_prev = xg[prev_d]
        g_xau_today = xg.get(d)
        if g_xau_today is None:
            continue

        gold_close_bars = g_xau_prev[g_xau_prev["h"] == gold_close_h]
        if len(gold_close_bars) < 1:
            continue
        gold_close = gold_close_bars.iloc[-1]["close"]

        gold_am_bars = g_xau_today[(g_xau_today["h"] == gold_am_h) & (g_xau_today["m"] <= 30)]
        if len(gold_am_bars) < 1:
            continue
        gold_am = gold_am_bars.iloc[-1]["close"]

        overnight_ret_bps = (gold_am - gold_close) / gold_close * 10000
        if abs(overnight_ret_bps) < 5:  # Need at least 5 bps overnight move
            continue

        gold_dir = 1 if overnight_ret_bps > 0 else -1

        # Tech entry at 9:30 AM ET (tech_entry_h in +4)
        tech_entry_bars = g_tech[(g_tech["h"] == tech_entry_h) & (g_tech["m"] >= 30)]
        if len(tech_entry_bars) < 1:
            continue
        tech_entry = tech_entry_bars.iloc[0]

        # Tech exit at 10:00 AM ET (tech_exit_h in +4)
        tech_exit_bars = g_tech[(g_tech["h"] == tech_exit_h)]
        if len(tech_exit_bars) < 1:
            continue
        tech_exit = tech_exit_bars.iloc[-1]

        treat_ret = (tech_exit["close"] - tech_entry["close"]) / tech_entry["close"] * 10000 * gold_dir
        t.append({"date": d, "ret": treat_ret, "gold_overnight": overnight_ret_bps,
                   "gold_dir": gold_dir})

        # Counterfactual: same time window on days with small overnight Gold move
        # (counterfactual = entry at 9:30 AM in direction of a random small move)
        if abs(overnight_ret_bps) >= 5:
            # Find a day with small Gold move for counterfactual
            for cd in prev_dates[-5:]:
                if cd == d:
                    continue
                cg_tech = tg.get(cd)
                if cg_tech is None:
                    continue
                cg_xau_prev_dates = [d3 for d3 in sorted(xg.keys()) if d3 < cd]
                if not cg_xau_prev_dates:
                    continue
                cg_xau_prev = xg[cg_xau_prev_dates[-1]]
                cg_xau_today = xg.get(cd)
                if cg_xau_today is None:
                    continue

                cg_gold_close_bars = cg_xau_prev[cg_xau_prev["h"] == gold_close_h]
                cg_gold_am_bars = cg_xau_today[(cg_xau_today["h"] == gold_am_h) & (cg_xau_today["m"] <= 30)]
                if len(cg_gold_close_bars) < 1 or len(cg_gold_am_bars) < 1:
                    continue

                cg_gold_close = cg_gold_close_bars.iloc[-1]["close"]
                cg_gold_am = cg_gold_am_bars.iloc[-1]["close"]
                cg_overnight = (cg_gold_am - cg_gold_close) / cg_gold_close * 10000

                if abs(cg_overnight) < 5:  # Small Gold move day
                    cg_dir = 1 if cg_overnight > 0 else (-1 if cg_overnight < 0 else 1)
                    cg_tech_entry_bars = cg_tech[(cg_tech["h"] == tech_entry_h) & (cg_tech["m"] >= 30)]
                    cg_tech_exit_bars = cg_tech[(cg_tech["h"] == tech_exit_h)]
                    if len(cg_tech_entry_bars) >= 1 and len(cg_tech_exit_bars) >= 1:
                        cg_te = cg_tech_entry_bars.iloc[0]
                        cg_tx = cg_tech_exit_bars.iloc[-1]
                        cg_ret = (cg_tx["close"] - cg_te["close"]) / cg_te["close"] * 10000 * gold_dir
                        cf.append({"date": cd, "ret": cg_ret})
                    break

    return v3_evidence("CAND-076", t, cf)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("V25 G1 ECONOMIC PLAUSIBILITY SCREEN")
    print("G1 V3 Evidence-Based Adjudication Framework")
    print("=" * 70)

    print("\nLoading data...")
    xau = load("XAUUSD")
    tech = load("USATECHIDXUSD")
    print(f"XAUUSD: {len(xau)} bars | USATECHIDXUSD: {len(tech)} bars")

    r = {}
    r["CAND-074"] = run_074(xau)
    r["CAND-075"] = run_075(tech)
    r["CAND-076"] = run_076(xau, tech)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for c, v in r.items():
        g2 = "G2-ELIGIBLE" if v["g2_eligible"] else "NOT-ELIGIBLE"
        print(f"  {c}: N={v['N']} Net={v['mn']:.2f}bps Adjudication={v['adjudication']} {g2}")

    # Save results
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "output", "research_discovery", "v25_g1_results.json")
    with open(out, "w") as f:
        json.dump(r, f, indent=2, default=str)
    print(f"\nSaved: {out}")
