"""PROTO-TREND-001 unit tests + IA-12 synthetic self-test.

Synthetic data ONLY. Never loads real vendor series, never touches the
network, never reads data_raw/. Run: python test_evaluate.py (exit 0 iff
every check passes). No third-party test framework required.
"""

import math
import os
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evaluate as ev

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail and not cond else ""))


def frame(dates, prices):
    return pd.DataFrame({"date": pd.to_datetime(dates), "price": [float(p) for p in prices]})


def bizdays(start, end):
    return pd.bdate_range(start, end).strftime("%Y-%m-%d").tolist()


# ---- IA-12a: toy calendar date logic -------------------------------------
def test_a_date_logic():
    dates = bizdays("2020-01-27", "2020-04-03")
    tbl = dict((m, (s, e)) for (m, s, e) in ev.month_table(pd.to_datetime(dates)))
    g = lambda m, k: tbl[m][k].strftime("%Y-%m-%d")
    check("a s(Jan)==2020-01-31", g("2020-01", 0) == "2020-01-31")
    check("a e(Jan)==2020-02-03", g("2020-01", 1) == "2020-02-03")
    check("a s(Feb)==2020-02-28", g("2020-02", 0) == "2020-02-28")
    check("a e(Feb)==2020-03-02", g("2020-02", 1) == "2020-03-02")
    check("a s(Mar)==2020-03-31", g("2020-03", 0) == "2020-03-31")
    check("a e(Mar)==2020-04-01", g("2020-03", 1) == "2020-04-01")
    check("a Apr has no entry (no obs after)", "2020-04" not in tbl)


def test_a_last_month_cutoff():
    dates = bizdays("2019-10-01", "2020-05-15")
    prices = np.linspace(100.0, 120.0, len(dates))
    f = {"M": frame(dates, prices)}
    rows_all = ev.evaluate_panel(f, ["M"], {"M": 0.0}, 5, cutoff="2020-12-31")
    months_all = [r["month"] for r in rows_all]
    check("a Mar evaluable with far cutoff", "2020-03" in months_all, months_all)
    rows_cut = ev.evaluate_panel(f, ["M"], {"M": 0.0}, 5, cutoff="2020-03-31")
    bym = dict((r["month"], r) for r in rows_cut)
    check("a Mar row present but empty (n==0) when e(next)>cutoff",
          bym["2020-03"]["n"] == 0 and bym["2020-03"]["net"] == 0.0, bym["2020-03"]["n"])
    check("a Feb empty too (its holding exits Apr 1 > cutoff)",
          bym["2020-02"]["n"] == 0, bym["2020-02"]["n"])
    check("a Jan kept with n>0 (holding exits Mar 2 <= cutoff)",
          bym["2020-01"]["n"] > 0, bym["2020-01"]["n"])


# ---- units: signal / sigma / holding ------------------------------------
def test_units():
    p = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0])
    check("signal up +1", ev.signal_at(p, 2) == 1)
    check("signal down -1", ev.signal_at(pd.Series([104.0, 103.0, 102.0]), 2) == -1)
    check("signal zero -> flat", ev.signal_at(pd.Series([100.0, 101.0, 100.0]), 2) == 0)
    check("signal insufficient history -> None", ev.signal_at(p, 5) is None)
    check("sigma <60 obs -> NaN", not np.isfinite(ev.sigma_at(pd.Series(np.linspace(100, 110, 30)))))
    check("sigma constant -> 0.0", ev.sigma_at(pd.Series([100.0] * 80)) == 0.0)
    check("sigma noisy > 0", ev.sigma_at(pd.Series(100 + np.random.default_rng(0).normal(0, 1, 80))) > 0)
    check("sharpe positive drift", ev.sharpe([0.01] * 23 + [0.02]) > 0)
    check("sharpe constant -> 0 by convention", ev.sharpe([0.01] * 24) == 0.0)
    check("drawdown of gains is 0", ev.max_drawdown_rescaled([0.01] * 24) == 0.0)
    check("bootstrap lower <= mean", ev.bootstrap_lower([0.01, -0.005, 0.02] * 20, B=500, seed=1) <= np.mean([0.01, -0.005, 0.02] * 20) + 1e-12)


# ---- IA-12b: no look-ahead ----------------------------------------------
def test_b_no_lookahead():
    rng = np.random.default_rng(7)
    dates = bizdays("2021-01-01", "2021-12-31")
    px = 100 * np.exp(np.cumsum(rng.normal(0.0005, 0.01, len(dates))))
    f = {"M": frame(dates, px)}
    rows = ev.evaluate_panel(f, ["M"], {"M": 0.0}, 20, cutoff="2021-12-31")
    check("b panel evaluates", len(rows) > 3, len(rows))
    tbl = dict((m, (s, e)) for (m, s, e) in ev.month_table(f["M"]["date"]))
    for m0 in [r["month"] for r in rows[:3]]:
        s, e = tbl[m0]
        sub = f["M"][f["M"]["date"] <= s].reset_index(drop=True)
        check("b check passes on truncated %s" % m0,
              ev.check_no_lookahead(sub["date"], s) is True)
        check("b truncated signal finite %s" % m0,
              ev.signal_at(sub["price"], 20) in (-1, 0, 1))
    leaked = pd.concat([sub, f["M"][f["M"]["date"] > s].head(1)], ignore_index=True)
    try:
        ev.check_no_lookahead(leaked["date"], s)
        check("b planted leak FAILS check", False, "no exception raised")
    except ev.LookaheadError:
        check("b planted leak FAILS check", True)


# ---- IA-12e: cost arithmetic ---------------------------------------------
def test_e_costs():
    check("e zero change -> zero cost", 0.001 * abs(0.4 - 0.4) == 0.0)
    check("e full flip charged 2|w|", abs(0.001 * abs(-0.5 - 0.5) - 0.001 * 2 * 0.5) < 1e-15)
    # hand-computed 3-month toy: w = [0.0, 0.4, 0.4, -0.2], c = 0.002
    w = [0.0, 0.4, 0.4, -0.2]
    c = 0.002
    costs = [c * abs(w[i] - w[i - 1]) for i in range(1, 4)]
    check("e hand toy month costs",
          all(abs(a - b) < 1e-12 for a, b in zip(costs, [0.0008, 0.0, 0.0012])), costs)
    check("e hand toy total", abs(sum(costs) - 0.002) < 1e-15, sum(costs))
    # end-to-end structural: net == gross - cost; grid scales exactly
    rng = np.random.default_rng(11)
    dates = bizdays("2021-01-01", "2021-08-31")
    frames = {"A": frame(dates, 100 * np.exp(np.cumsum(rng.normal(0.001, 0.01, len(dates))))),
              "B": frame(dates, 50 * np.exp(np.cumsum(rng.normal(-0.001, 0.012, len(dates)))))}
    r1 = ev.evaluate_panel(frames, ["A", "B"], {"A": 0.001, "B": 0.001}, 20, cutoff="2021-12-31")
    r2 = ev.evaluate_panel(frames, ["A", "B"], {"A": 0.002, "B": 0.002}, 20, cutoff="2021-12-31")
    ok = True
    for a, b in zip(r1, r2):
        ok = ok and abs(a["net"] - (a["gross"] - a["cost"])) < 1e-12
        ok = ok and abs(b["cost"] - 2.0 * a["cost"]) < 1e-12
        ok = ok and abs(b["gross"] - a["gross"]) < 1e-12
    check("e net==gross-cost; grid x2 exact; gross invariant", ok and any(r["n"] > 0 for r in r1), len(r1))


# ---- IA-12c: planted effect ----------------------------------------------
def test_c_planted_effect():
    rng = np.random.default_rng(20261007)
    dates = bizdays("2019-01-01", "2021-12-31")
    frames = {}
    for k in range(15):
        px = 100 * np.exp(np.cumsum(rng.normal(0.0012, 0.008, len(dates))))
        frames["M%02d" % k] = frame(dates, px)
    syms = sorted(frames)
    rows = ev.evaluate_panel(frames, syms, {s: 0.0 for s in syms}, 252, cutoff="2021-12-31")
    net = [r["net"] for r in rows if r["n"] > 0]
    check("c months evaluated", len(net) >= 15, len(net))
    check("c net mean > 0", float(np.mean(net)) > 0, float(np.mean(net)))
    lo = ev.bootstrap_lower(net, B=10000, seed=20261007)
    check("c bootstrap lower > 0", lo > 0, lo)


# ---- IA-12d: null ---------------------------------------------------------
def test_d_null():
    hits = 0
    reps = 100
    for rep in range(reps):
        rng = np.random.default_rng(9000 + rep)
        dates = bizdays("2019-01-01", "2021-12-31")
        frames = {}
        for k in range(5):
            px = 100 * np.exp(np.cumsum(rng.normal(0.0, 0.01, len(dates))))
            frames["Z%02d" % k] = frame(dates, px)
        syms = sorted(frames)
        rows = ev.evaluate_panel(frames, syms, {s: 0.0 for s in syms}, 60, cutoff="2021-12-31")
        net = [r["net"] for r in rows if r["n"] > 0]
        if not net:
            continue
        if ev.bootstrap_lower(net, B=2000, seed=9000 + rep) > 0:
            hits += 1
    check("d null false-positive fraction <= 10%", hits <= 10, "%d/100" % hits)


# ---- IA-12f: cutoff refusal ------------------------------------------------
def test_f_cutoff_refusal():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "x.csv")
        pd.DataFrame({"date": ["2026-09-29", "2026-09-30", "2026-10-01"],
                      "close": [1.0, 1.0, 1.0]}).to_csv(p, index=False)
        try:
            ev.load_market_csv(p)
            check("f refuses dates after cutoff", False, "no exception")
        except ev.CutoffRefusal:
            check("f refuses dates after cutoff", True)
        p2 = os.path.join(td, "y.csv")
        pd.DataFrame({"date": ["2026-09-29", "2026-09-30"],
                      "close": [1.0, 1.0]}).to_csv(p2, index=False)
        check("f loads within cutoff", len(ev.load_market_csv(p2)) == 2)


if __name__ == "__main__":
    test_a_date_logic()
    test_a_last_month_cutoff()
    test_units()
    test_b_no_lookahead()
    test_e_costs()
    test_c_planted_effect()
    test_d_null()
    test_f_cutoff_refusal()
    print("----")
    print("PASS: %d  FAIL: %d" % (len(PASS), len(FAIL)))
    if FAIL:
        print("FAILED:", FAIL)
        sys.exit(1)
