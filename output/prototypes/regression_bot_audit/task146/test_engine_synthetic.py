"""Synthetic self-test for vs_tsmom_engine (TASK146 G4). Synthetic data only."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vs_tsmom_engine as E


def synth_months(start, n_months, monthly_ret, daily_noise=0.0, seed=1):
    rng = np.random.default_rng(seed)
    rows = []
    px = 100.0
    d = pd.Timestamp(start)
    made, target = 0, n_months * 22
    while made < target:
        if d.weekday() < 5:
            r = (1 + monthly_ret) ** (1 / 21) - 1 + rng.normal(0, daily_noise)
            px = px * (1 + r)
            rows.append({"date": d.strftime("%Y-%m-%d"), "v": px})
            made += 1
        d += pd.Timedelta(days=1)
    return pd.DataFrame(rows)


def run_df(df):
    s = pd.Series(df["v"].values, index=pd.to_datetime(df["date"]))
    return E.evaluate_panel(s)


def tie_frame(start, n_months):
    rows = []
    d = pd.Timestamp(start)
    made, target = 0, n_months * 22
    k = 0
    while made < target:
        if d.weekday() < 5:
            v = 101.0 if (made % 22 == 10) else 100.0
            rows.append({"date": d.strftime("%Y-%m-%d"), "v": v})
            made += 1
        d += pd.Timedelta(days=1)
        k += 1
        if k > n_months * 40:
            break
    return pd.DataFrame(rows)


def main():
    # (a) planted uptrend: +1 weights, bounds hold
    df = synth_months("2020-01-01", 15, 0.08, daily_noise=0.002)
    rows, sk = run_df(df)
    assert len(rows) > 0 and all(r["w"] == 1.0 for r in rows), (len(rows), sk)
    assert all(r["f"] == 1.0 for r in rows)
    assert all(-1.0 <= r["w"] <= 1.0 for r in rows)
    print("PASS a: planted uptrend -> +1 weights, bounds hold")
    # (e) cost arithmetic exact, first-month build from zero
    r0 = rows[0]
    assert abs(r0["net_s"] - (r0["gross_s"] - r0["cost_s"])) < 1e-12
    assert abs(r0["cost_s"] - 0.0015 * abs(r0["w"] - 0.0)) < 1e-12, r0
    print("PASS e: cost arithmetic exact")
    # (b) ties (month-end closes equal) -> zero weights
    df0 = tie_frame("2020-01-01", 15)
    rows0, _ = run_df(df0)
    assert len(rows0) > 0, "tie test produced no rows"
    assert all(r["w"] == 0.0 and r["f"] == 0.0 for r in rows0), rows0[:2]
    print("PASS b: ties -> zero weights")
    # (c) short history -> skipped + counted
    dfs = synth_months("2020-01-01", 5, 0.05, daily_noise=0.002)
    rowss, sks = run_df(dfs)
    assert rowss == [] and sks["no_anchor"] > 0, (rowss, sks)
    print("PASS c/d: insufficient history skipped + counted")
    # (f) determinism incl. analyze
    a1 = E.analyze([dict(r) for r in rows])
    a2 = E.analyze([dict(r) for r in rows])
    assert a1 == a2
    print("PASS f: determinism (analyze byte-identical)")
    # (g) analyze machinery on hand-made differentials
    mk = lambda s, f, p, n: [{"net_s": s, "net_f": f, "net_p": p,
                              "cost_s": 0.001, "w": 1.0,
                              "gross_s": s, "month": "2020-01"} for _ in range(n)]
    apos = E.analyze(mk(0.02, 0.01, 0.0, 30))
    assert apos["holm_p"]["d1"] < 0.05 and apos["holm_p"]["d2"] < 0.05
    assert apos["ratio"] > 0 and "ub" in apos and "lb" in apos
    aneg = E.analyze(mk(-0.02, 0.01, 0.0, 30))
    assert aneg["holm_p"]["d1"] == 1.0
    print("PASS g: analyze machinery (positive->pass, negative->fail)")
    # (h) decide_label branches incl. the TASK139 fix branch
    base = {"lb": {"d1": 0.01, "d2": 0.01}, "ub": {"d1": 0.05, "d2": 0.05},
            "holm_p": {"d1": 0.01, "d2": 0.02}, "ratio": 3.0}
    assert E.decide_label(dict(base)) == "PASS"
    assert E.decide_label(dict(base, lb={"d1": -0.02, "d2": -0.01},
                               ub={"d1": -0.01, "d2": 0.05},
                               holm_p={"d1": 0.9, "d2": 0.8})) == "FAIL"
    assert E.decide_label(dict(base, lb={"d1": -0.01, "d2": 0.01})) == "INCONCLUSIVE"
    assert E.decide_label(dict(base, ratio=1.5)) == "INCONCLUSIVE"
    print("PASS h: decide_label trichotomy incl. lower>0+ratio<2 branch")
    # (i) duplicate timestamps -> IntegrityStop
    s = pd.Series([100.0, 101.0, 102.0],
                  index=pd.to_datetime(["2020-01-01", "2020-01-01", "2020-01-02"]))
    try:
        E.check_integrity(s)
        raise AssertionError("duplicates did not raise")
    except E.IntegrityStop:
        print("PASS i: duplicates fail closed")
    # (j) yearly NaN rate >5% -> IntegrityStop; clean passes
    idx = pd.bdate_range("2020-01-01", "2020-12-31")
    vals = np.full(len(idx), 100.0)
    vals[:20] = np.nan  # ~8% missing
    try:
        E.check_integrity(pd.Series(vals, index=idx))
        raise AssertionError("yearly missing did not raise")
    except E.IntegrityStop:
        print("PASS j: yearly missing >5% fails closed")
    E.check_integrity(pd.Series(np.full(len(idx), 100.0), index=idx))
    print("PASS k: clean series passes integrity")
    # (l) diagnostics/grid/stress smoke on synthetic rows
    d = E.diagnostics(rows)
    assert set(d) >= {"yearly", "turnover", "total_cost_s", "vol_tracking"}
    g = E.cost_grid(pd.Series(df["v"].values, index=pd.to_datetime(df["date"])))
    assert set(g) == {"0.5", "1.0", "2.0", "4.0"} and g["1.0"]["n"] == len(rows)
    st = E.financing_stress(rows)
    assert set(st) == {"0.0", "0.02", "0.04"}
    print("PASS l: diagnostics/grid/stress smoke")
    print("ALL SYNTHETIC SELF-TESTS PASS")


if __name__ == "__main__":
    main()
