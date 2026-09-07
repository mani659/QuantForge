"""
V37A REPL077 XAUUSD — PHASE B DRIVER (outcome computation, single run)
Registration: V37A-REPL-077-XAUUSD-M1
Executes the frozen 30-bar outcome over the Phase-A event population exactly once.
No adjudication, no rerun, no subsetting, no extra robustness filters.
"""
import hashlib, importlib.util, json, os, time

import numpy as np
import pandas as pd

ARCHIVAL = os.path.abspath("research/archive/v26/CAND-077/v26_g1_screen.py")
spec = importlib.util.spec_from_file_location("v26_frozen", ARCHIVAL)
frozen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frozen)

# Path-resolution fix only (identical to Phase A): frozen load() derives DIR from
# its own file location; point it at the registered data path. Semantics unchanged.
frozen.DIR = os.path.abspath("data/m1")

load = frozen.load
compute_atr = frozen.compute_atr
atr_pct = frozen.atr_pct
FRIC = frozen.FRIC   # 2.0 bps

WINDOW_START = pd.Timestamp("2023-09-01")
WINDOW_END = pd.Timestamp("2026-04-10 23:59:59")
OUTDIR = os.path.dirname(os.path.abspath(__file__))

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def stats(gross):
    """Frozen aggregation semantics from v3_evidence: net = gross - FRIC (linear
    shift, so per-event net mean/median equal the frozen constant-shift values);
    WR/std/worst/best on gross; exclude-best = mean of gross excluding all events
    equal to the max, minus FRIC."""
    g = np.asarray(gross, dtype=float)
    n = len(g)
    gm, gmed = float(np.mean(g)), float(np.median(g))
    nm, nmed = gm - FRIC, gmed - FRIC
    wr = float((g > 0).mean()) * 100.0
    sd = float(np.std(g)) if n > 1 else 0.0
    worst, best = float(np.min(g)), float(np.max(g))
    excl = float(g[g != np.max(g)].mean()) - FRIC if n > 1 else nm
    return {"N": n, "gross_mean": round(gm, 2), "gross_median": round(gmed, 2),
            "net_mean": round(nm, 2), "net_median": round(nmed, 2),
            "win_rate": round(wr, 1), "std_gross": round(sd, 2),
            "worst": round(worst, 2), "best": round(best, 2),
            "exclude_best_net_mean": round(excl, 2)}

def aggregate_rows(list_of_gross):
    return stats(list_of_gross)

def run(window_only):
    df = load("XAUUSD")
    raw = pd.read_csv(os.path.abspath("data/m1/XAUUSD_M1.csv"), parse_dates=["timestamp"])
    raw_ts = pd.DatetimeIndex(raw["timestamp"]).sort_values()

    closes = df["close"].values
    n = len(df)
    atr_vals = compute_atr(df, 14)
    atr_p = atr_pct(atr_vals, 200)

    # ---- VERBATIM frozen detection (identical to Phase A) ----
    is_breakout = np.zeros(n, dtype=bool)
    comp_high = np.full(n, np.nan)
    for i in range(20, n):
        lb_pct = atr_p[max(0, i - 20):i]
        lb_close = closes[max(0, i - 20):i]
        mask = lb_pct < 25
        if np.sum(mask) >= 10:
            comp_high[i] = np.max(lb_close[mask])
    for i in range(250, n - 30):
        if np.isnan(atr_p[i]) or atr_p[i] <= 50:
            continue
        recent_min = np.nanmin(atr_p[max(0, i - 5):i + 1])
        if np.isnan(recent_min) or recent_min >= 25:
            continue
        if np.isnan(comp_high[i]) or closes[i] <= comp_high[i]:
            continue
        is_breakout[i] = True
    is_cf = np.zeros(n, dtype=bool)
    for i in range(250, n - 30):
        if np.isnan(atr_p[i]) or atr_p[i] <= 50:
            continue
        preceding = atr_p[max(0, i - 30):i + 1]
        if np.any(np.isnan(preceding)) or np.nanmin(preceding) <= 50:
            continue
        c_h = np.max(closes[max(0, i - 20):i]) if i >= 20 else 0
        if closes[i] > c_h:
            is_cf[i] = True

    treat_all = np.where(is_breakout)[0]
    cf_all = np.where(is_cf)[0]
    cf_set = set(cf_all.tolist())

    if window_only:
        raw_dates = raw_ts
        in_win = (raw_dates >= WINDOW_START) & (raw_dates <= WINDOW_END)
        treat = np.array([i for i in treat_all if bool(in_win[i])])
        label = "PRIMARY WINDOW"
    else:
        treat = treat_all
        label = "SECONDARY CONSISTENCY CHECK (full history)"

    # Frozen matching: earliest CF within [ti-50, ti+50], excluding ti.
    pairs = []          # (ti, ci)
    matched_cf = []
    for ti in treat:
        found = None
        lo, hi = ti - 50, ti + 50
        for ci in range(lo, hi + 1):
            if ci in cf_set and ci != ti:
                found = ci
                break
        if found is not None:
            pairs.append((int(ti), int(found)))
            matched_cf.append(found)

    # Outcomes
    def outcome(i):
        g = (closes[i + 30] - closes[i]) / closes[i] * 10000.0
        return g, g - FRIC

    rows = []
    t_gross = []
    for ti in treat:
        g, nn = outcome(ti)
        t_gross.append(g)
        rows.append({"experiment_id": "V37A-REPL-077-XAUUSD-M1",
                     "phase": "B", "market": "XAUUSD",
                     "timestamp": str(raw_ts[ti]), "bar_index": int(ti),
                     "classification": "treatment", "treatment_event_id": f"TREAT_{int(ti)}",
                     "control_event_id": None,
                     "matched_control_bar_index": None, "matched_control_timestamp": None,
                     "control_reuse_indicator": None,
                     "entry_price": float(closes[ti]), "exit_price": float(closes[ti + 30]),
                     "gross_return_bps": round(g, 4), "net_return_bps": round(nn, 4),
                     "primary_window_indicator": label})
    c_gross = []
    for ti, ci in pairs:
        g, nn = outcome(ci)
        c_gross.append(g)
        rows.append({"experiment_id": "V37A-REPL-077-XAUUSD-M1",
                     "phase": "B", "market": "XAUUSD",
                     "timestamp": str(raw_ts[ci]), "bar_index": int(ci),
                     "classification": "control", "treatment_event_id": f"TREAT_{ti}",
                     "control_event_id": f"CONTROL_{int(ci)}",
                     "matched_control_bar_index": int(ci), "matched_control_timestamp": str(raw_ts[ci]),
                     "control_reuse_indicator": int(ci),
                     "entry_price": float(closes[ci]), "exit_price": float(closes[ci + 30]),
                     "gross_return_bps": round(g, 4), "net_return_bps": round(nn, 4),
                     "primary_window_indicator": label})

    use_count = {}
    for ci in matched_cf:
        use_count[ci] = use_count.get(ci, 0) + 1
    reuse = sum(1 for c in use_count.values() if c > 1)

    t_stat = aggregate_rows(t_gross)
    c_stat = aggregate_rows(c_gross)
    delta_mean = round(t_stat["net_mean"] - c_stat["net_mean"], 2)
    delta_median = round(t_stat["net_median"] - c_stat["net_median"], 2)
    delta_gross = round(t_stat["gross_mean"] - c_stat["gross_mean"], 2)
    delta_wr = round(t_stat["win_rate"] - c_stat["win_rate"], 1)

    res = {
        "label": label,
        "treatment": t_stat,
        "control": c_stat,
        "gross_mean_delta": delta_gross,
        "net_mean_delta": delta_mean,
        "median_delta": delta_median,
        "win_rate_delta": delta_wr,
        "matched_control_observations": len(pairs),
        "unique_control_events": len(use_count),
        "reused_control_events": reuse,
        "unmatched_treatments": int(len(treat) - len(pairs)),
    }
    return res, rows

def main():
    t0 = time.time()
    # Phase-A population reconciliation guard: recompute primary-window counts and
    # require exact equality with the locked Phase-A artifact before computing outcomes.
    pa = json.load(open(os.path.join(OUTDIR, "phase_a_report.json")))
    expect_treat = pa["populations"]["treatment_events_primary_window"]

    # Dry detection pass to confirm count (no outcomes computed here).
    df_check = load("XAUUSD")
    rawc = pd.read_csv(os.path.abspath("data/m1/XAUUSD_M1.csv"), parse_dates=["timestamp"])
    raw_ts_c = pd.DatetimeIndex(rawc["timestamp"]).sort_values()
    closes_c = df_check["close"].values
    nn = len(df_check)
    atr_c = compute_atr(df_check, 14)
    atr_pc = atr_pct(atr_c, 200)
    ib = np.zeros(nn, dtype=bool)
    ch = np.full(nn, np.nan)
    for i in range(20, nn):
        lbp = atr_pc[max(0, i - 20):i]; lbc = closes_c[max(0, i - 20):i]
        m = lbp < 25
        if np.sum(m) >= 10:
            ch[i] = np.max(lbc[m])
    for i in range(250, nn - 30):
        if np.isnan(atr_pc[i]) or atr_pc[i] <= 50: continue
        if np.isnan(np.nanmin(atr_pc[max(0, i - 5):i + 1])) or np.nanmin(atr_pc[max(0, i - 5):i + 1]) >= 25: continue
        if np.isnan(ch[i]) or closes_c[i] <= ch[i]: continue
        ib[i] = True
    ta = np.where(ib)[0]
    inw = (raw_ts_c >= WINDOW_START) & (raw_ts_c <= WINDOW_END)
    tw = np.array([i for i in ta if bool(inw[i])])
    if int(len(tw)) != int(expect_treat):
        print(f"POPULATION RECONCILIATION FAILURE: expected {expect_treat}, got {len(tw)}")
        raise SystemExit(2)
    print(f"Population reconciled with Phase A: {len(tw)} treatment events (primary window).")

    primary, rows_p = run(window_only=True)
    secondary, rows_s = run(window_only=False)

    # event-level rows: primary window treatment+matched-control rows (secondary kept separate)
    ev = pd.DataFrame(rows_p)
    ev.to_csv(os.path.join(OUTDIR, "phase_b_event_level_primary.csv"), index=False)
    pd.DataFrame(rows_s).to_csv(os.path.join(OUTDIR, "phase_b_event_level_secondary.csv"), index=False)

    report = {
        "execution": {"registration": "V37A-REPL-077-XAUUSD-M1", "phase": "B",
                      "archival_impl_sha256": sha256_file(ARCHIVAL),
                      "head": "f192f3d283779164d79a84fed212e2bc13ca9f0a"},
        "primary_window": {"window": "2023-09-01 -> 2026-04-10", **primary},
        "secondary_full_history": {"window": "2021-04-12 -> 2026-04-10", **secondary},
        "timing_seconds": round(time.time() - t0, 1),
    }
    with open(os.path.join(OUTDIR, "phase_b_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
