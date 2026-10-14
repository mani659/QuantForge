"""PROTO-TREND-001 v2 tests (B2). Keeps all 41 v1 checks; adds v2 branch coverage.

Synthetic data ONLY (tempdir CSVs in exact real layouts + in-memory frames).
Never loads data_raw/, never touches the network. Run:
python test_evaluate_v2.py  (exit 0 iff every check passes; no pytest needed)
"""

import json
import os
import sys
import tempfile

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".."))
sys.path.insert(0, _HERE)
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

import evaluate_v2 as ev2
import test_evaluate as t1

PASS = []
FAIL = []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail and not cond else ""))


def run_v1_suite():
    t1.test_a_date_logic()
    t1.test_a_last_month_cutoff()
    t1.test_units()
    t1.test_b_no_lookahead()
    t1.test_e_costs()
    t1.test_c_planted_effect()
    t1.test_d_null()
    t1.test_f_cutoff_refusal()
    check("v1 suite: 41 checks kept green", len(t1.PASS) == 41 and len(t1.FAIL) == 0,
          "pass=%d fail=%d" % (len(t1.PASS), len(t1.FAIL)))


# ---------- synthetic market builders (seeded, deterministic) -------------
def bizdays(start, end):
    return pd.bdate_range(start, end).strftime("%Y-%m-%d").tolist()


def daily(start, end):
    return pd.date_range(start, end, freq="D").strftime("%Y-%m-%d").tolist()


def gbm(dates, drift, vol, seed, start_price=100.0):
    rng = np.random.default_rng(seed)
    px = start_price * np.exp(np.cumsum(rng.normal(drift, vol, len(dates))))
    return pd.DataFrame({"date": pd.to_datetime(dates), "price": px})


def write_yahoo_csv(path, dates, prices):
    pd.DataFrame({"date": dates, "open": prices, "high": prices, "low": prices,
                  "close": prices, "volume": [1000] * len(prices)}).to_csv(path, index=False)


def write_fred_csv(path, dates, values):
    pd.DataFrame({"observation_date": dates, "DCOILBRENTEU": values}).to_csv(path, index=False)


def materialize(root, specs):
    """specs: {symbol: (dates, prices_or_values)}. Writes exact real layouts
    + universe.json listing them. Returns symbols list."""
    import tempfile
    data = os.path.join(root, "data_raw")
    os.makedirs(data, exist_ok=True)
    syms = []
    for sym, (dates, vals) in specs.items():
        syms.append(sym)
        if sym == "DCOILBRENTEU":
            write_fred_csv(os.path.join(data, "DCOILBRENTEU.csv"), dates, vals)
        else:
            write_yahoo_csv(os.path.join(data, sym + ".csv"), dates, vals)
    with open(os.path.join(root, "universe.json"), "w") as fh:
        json.dump({"series": [{"symbol": s, "status": "PASS", "reasons": []} for s in syms]}, fh)
    return syms


def trend_panel(n_years_days, drift, vol, seed0, markets, seven_day=()):
    dates_b = bizdays("2015-01-01", "2021-12-31")
    frames = {}
    for k, sym in enumerate(markets):
        dd = daily("2015-01-01", "2021-12-31") if sym in seven_day else dates_b
        frames[sym] = gbm(dd, drift, vol, seed0 + k)
    return frames


# ---------- closure decision branches (unit level) -------------------------
def test_closure_branches():
    base = {"sharpe_ge_030": True, "boot_lb_gt_0": True, "subperiods": True,
            "neighbourhood": True, "drawdown": True, "stress": True,
            "gross_sharpe_ge_030": True, "gross_boot_lb_gt_0": True}
    check("label PASS", ev2.decide_closure(dict(base), 0.5) == "PASS-TO-FORWARD")
    check("label PASS+WARNING", ev2.decide_closure(dict(base), 0.0) == "PASS-TO-FORWARD (FINANCING WARNING)")
    check("label WARNING needs all-six-pass", ev2.decide_closure(dict(base, stress=False), -1.0) != "PASS-TO-FORWARD (FINANCING WARNING)")
    g = dict(base, sharpe_ge_030=False)
    check("label INSUFFICIENT (net fail, gross ok)",
          ev2.decide_closure(g, 0.5) == "ECONOMICALLY INSUFFICIENT")
    n = dict(base, sharpe_ge_030=False, gross_sharpe_ge_030=False, gross_boot_lb_gt_0=False)
    check("label NEGATIVE", ev2.decide_closure(n, 0.5) == "NEGATIVE")
    keys = ["sharpe_ge_030", "boot_lb_gt_0", "subperiods", "neighbourhood", "drawdown", "stress"]
    for k in keys:
        solo = dict(base)
        solo[k] = False
        if k == "sharpe_ge_030":
            solo["gross_sharpe_ge_030"] = False
            solo["gross_boot_lb_gt_0"] = False
        got = ev2.decide_closure(solo, 0.5)
        check("single-failure %s -> non-PASS (%s)" % (k, got), got != "PASS-TO-FORWARD")


# ---------- end-to-end main() on synthetic real-format files ---------------
# 11 markets (>= 8 active so the IA-19 N<8 stop does not fire here).
PASS_SYMS = ["^GSPC", "^NDX", "^GDAXI", "^FTSE", "^N225", "EURUSD=X",
             "GBPUSD=X", "USDJPY=X", "GC=F", "DCOILBRENTEU", "BTC-USD"]


def build_synth_root(tmp, drift=0.0012, vol=0.008, seed=777, btc_scale=1.0, gaps=True,
                     start_price=100.0):
    dates_b = bizdays("2008-01-01", "2021-12-31")
    specs = {}
    for k, sym in enumerate(PASS_SYMS):
        if sym == "BTC-USD":
            dd = daily("2008-01-01", "2021-12-31")
            px = start_price * btc_scale * np.exp(np.cumsum(
                np.random.default_rng(seed + k).normal(drift, vol, len(dd))))
            specs[sym] = (dd, px.tolist())
        elif sym == "DCOILBRENTEU":
            dd = list(dates_b)
            vals = (0.6 * start_price * np.exp(np.cumsum(
                np.random.default_rng(seed + k).normal(drift, vol, len(dd))))).tolist()
            if gaps:
                vals[100] = ""
                vals[500] = ""
            specs[sym] = (dd, vals)
        else:
            dd = list(dates_b)
            if gaps and sym == "^N225":
                drop = set(pd.bdate_range("2019-04-29", "2019-05-06").strftime("%Y-%m-%d").tolist())
                dd = [d for d in dd if d not in drop]
            if gaps and sym == "EURUSD=X":
                drop = set(pd.bdate_range("2020-03-09", "2020-03-20").strftime("%Y-%m-%d").tolist())
                dd = [d for d in dd if d not in drop]
            px = start_price * np.exp(np.cumsum(
                np.random.default_rng(seed + k).normal(drift, vol, len(dd))))
            specs[sym] = (dd, px.tolist())
    materialize(tmp, specs)
    return tmp


def test_e2e_scenarios():
    import tempfile
    # PASS scenario (start prices x10 keep F-SNAP charges small vs drift)
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "out")
        os.makedirs(out)
        build_synth_root(td, start_price=1000.0)
        rc = ev2.main(["--root", td, "--out", out])
        res = json.load(open(os.path.join(out, "results.json")))
        check("e2e PASS run rc==0", rc == 0)
        check("e2e PASS label", res["closure"] == "PASS-TO-FORWARD", res["closure"])
        check("e2e REPORT has all diagnostics", all(
            m in open(os.path.join(out, "REPORT.md")).read() for m in
            ["## A7 criteria", "## Primary outcome", "## Closure label",
             "### control", "### worst_10_months", "### n_over_time",
             "### cost_grid", "### financing_stress", "### ex_bitcoin",
             "### neighbourhood", "### subperiods", "### leverage",
             "## A12 power statement", "## F-SNAP"]))
        check("e2e monthly_series columns", open(
            os.path.join(out, "monthly_series.csv")).readline().strip().split(",")[:6] ==
            ["month", "entry", "n", "gross", "cost", "net"])
    # WARNING scenario (tiny BTC price -> huge F-SNAP charge, criteria intact)
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "out")
        os.makedirs(out)
        build_synth_root(td, btc_scale=0.02)
        rc = ev2.main(["--root", td, "--out", out])
        res = json.load(open(os.path.join(out, "results.json")))
        check("e2e WARNING label",
              res["closure"] == "PASS-TO-FORWARD (FINANCING WARNING)", res["closure"])
    # NEGATIVE scenario (driftless noise)
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "out")
        os.makedirs(out)
        build_synth_root(td, drift=0.0, vol=0.02, seed=4242)
        rc = ev2.main(["--root", td, "--out", out])
        res = json.load(open(os.path.join(out, "results.json")))
        check("e2e NEGATIVE label", res["closure"] == "NEGATIVE", res["closure"])
    # INSUFFICIENT scenario (tuned synthetic: gross passes, subperiods fail)
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "out")
        os.makedirs(out)
        build_synth_root(td, drift=0.0007, vol=0.02, seed=999)
        rc = ev2.main(["--root", td, "--out", out])
        res = json.load(open(os.path.join(out, "results.json")))
        c = res["criteria"]
        if c["gross_sharpe_ge_030"] and c["gross_boot_lb_gt_0"] and not (
                c["sharpe_ge_030"] and c["boot_lb_gt_0"] and c["subperiods"]
                and c["neighbourhood"] and c["drawdown"] and c["stress"]):
            check("e2e INSUFFICIENT label",
                  res["closure"] == "ECONOMICALLY INSUFFICIENT", res["closure"])
        else:
            check("e2e INSUFFICIENT setup valid (gross ok, net fails)",
                  False, json.dumps(c))
    # N<8 stop (3 late-start markets)
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "out")
        os.makedirs(out)
        dd = bizdays("2015-01-01", "2021-12-31")
        specs = {}
        for k, sym in enumerate(["^GSPC", "EURUSD=X", "GC=F"]):
            px = 100 * np.exp(np.cumsum(
                np.random.default_rng(31 + k).normal(0.001, 0.01, len(dd))))
            specs[sym] = (list(dd), px.tolist())
        materialize(td, specs)
        try:
            ev2.main(["--root", td, "--out", out])
            check("e2e N<8 raises DataIntegrityStop", False, "no exception")
        except ev2.DataIntegrityStop:
            check("e2e N<8 raises DataIntegrityStop", True)
        check("e2e N<8 writes stop report only",
              os.path.exists(os.path.join(out, "STOP_REPORT.md"))
              and not os.path.exists(os.path.join(out, "results.json"))
              and not os.path.exists(os.path.join(out, "REPORT.md")))
    # determinism (two runs, byte-identical results.json)
    with tempfile.TemporaryDirectory() as td:
        o1 = os.path.join(td, "o1")
        o2 = os.path.join(td, "o2")
        os.makedirs(o1)
        os.makedirs(o2)
        build_synth_root(td)
        ev2.main(["--root", td, "--out", o1])
        ev2.main(["--root", td, "--out", o2])
        b1 = open(os.path.join(o1, "results.json"), "rb").read()
        b2 = open(os.path.join(o2, "results.json"), "rb").read()
        check("e2e determinism (byte-identical results.json)", b1 == b2)


def test_cutoff_truncation_and_fsnap_error():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        data = os.path.join(td, "data_raw")
        os.makedirs(data)
        dd = bizdays("2020-01-01", "2026-10-08")
        px = np.linspace(100.0, 130.0, len(dd))
        pd.DataFrame({"date": dd, "open": px, "high": px, "low": px,
                      "close": px, "volume": 1000}).to_csv(
            os.path.join(data, "^GSPC.csv"), index=False)
        with open(os.path.join(td, "universe.json"), "w") as fh:
            json.dump({"series": [{"symbol": "^GSPC", "status": "PASS", "reasons": []}]}, fh)
        syms, frames, log = ev2.load_universe(td)
        check("truncation drops post-cutoff rows", log[0]["rows_dropped_past_cutoff"] > 0,
              log[0]["rows_dropped_past_cutoff"])
        check("truncation asserts max<=cutoff",
              frames["^GSPC"]["date"].max().strftime("%Y-%m-%d") <= "2026-09-30")
    # F-SNAP missing price -> FsnapError, never KeyError
    # F-SNAP missing price -> FsnapError, never KeyError (uses a SWAP-mapped symbol)
    dates = bizdays("2021-01-01", "2021-06-30")
    f = {"GC=F": pd.DataFrame({"date": pd.to_datetime(dates),
                               "price": np.linspace(1800.0, 1900.0, len(dates))})}
    rows = ev2.evaluate_panel(f, ["GC=F"], {"GC=F": 0.0}, 20, cutoff="2021-12-31")
    f2 = {"GC=F": f["GC=F"][f["GC=F"]["date"] < "2021-03-01"].reset_index(drop=True)}
    try:
        ev2.fsnap_monthly(rows, {"GC=F": f2["GC=F"].assign(
            price=f2["GC=F"]["price"])})
        check("fsnap missing price raises FsnapError", False, "no exception")
    except ev2.FsnapError:
        check("fsnap missing price raises FsnapError", True)
    except KeyError as e:
        check("fsnap missing price raises FsnapError (got KeyError)", False, e)


if __name__ == "__main__":
    run_v1_suite()
    test_closure_branches()
    test_e2e_scenarios()
    test_cutoff_truncation_and_fsnap_error()
    print("----")
    print("PASS: %d  FAIL: %d" % (len(PASS), len(FAIL)))
    if FAIL:
        print("FAILED:", FAIL)
        sys.exit(1)
