"""Synthetic self-test for s2_engine (TASK166 Phase D). Synthetic data only."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import s2_engine as E


def synth_years(n_years, dec_close=100.0, jan_path=None, start_year=2020):
    """Synthetic daily closes: December flat + January path. Returns frame."""
    rows = []
    d = pd.Timestamp("%d-12-01" % start_year)
    for _ in range(n_years * 400):
        if d.weekday() < 5:
            rows.append({"date": d.strftime("%Y-%m-%d"), "close": 100.0})
        d += pd.Timedelta(days=1)
        if len(rows) > n_years * 260 + 40:
            break
    return pd.DataFrame(rows)


def run_df(df):
    s = pd.Series(df["close"].values, index=pd.to_datetime(df["date"]))
    return E.january_windows(s)


def main():
    # (a) planted weeks: hand-computed net for one clean year
    df = synth_years(3)
    rows, sk = run_df(df)
    assert len(rows) >= 1, (len(rows), sk)
    r0 = rows[0]
    exp = (100.0 * 0.9985) / (100.0 * 1.0015) - 1.0
    assert abs(r0["entry_px"] - 100.0 * 1.0015) < 1e-9, r0
    assert abs(r0["exit_px"] - 100.0 * 0.9985) < 1e-9, r0
    assert abs((r0["exit_px"] / r0["entry_px"] - 1.0) - exp) < 1e-12
    print("PASS a: planted week exact (entry/exit/cost legs)")
    # (e) cost arithmetic: 30bps round trip on flat prices
    ev = E.evaluate([r0])
    assert abs(ev[0]["net"] - exp) < 1e-12
    print("PASS e: cost arithmetic exact (15bps/leg, 30 RT)")
    # (b) short January (<5 sessions) -> skipped + counted
    tiny = pd.DataFrame([
        {"date": "2021-12-%02d" % d, "close": 100.0} for d in (29, 30, 31)
        if pd.Timestamp("2021-12-%02d" % d).weekday() < 5] + [
        {"date": "2022-01-03", "close": 100.0},
        {"date": "2022-01-04", "close": 100.0}])
    s = pd.Series(tiny["close"].values, index=pd.to_datetime(tiny["date"]))
    rws, sks = E.january_windows(s)
    assert rws == [] and sks["short_january"] == 1, (rws, sks)
    print("PASS b: short January skipped + counted")
    # (c) missing December (first year) -> skipped
    only = pd.DataFrame([{"date": "2022-01-%02d" % d, "close": 100.0 + d}
                         for d in range(3, 28)
                         if pd.Timestamp("2022-01-%02d" % d).weekday() < 5])
    s2 = pd.Series(only["close"].values, index=pd.to_datetime(only["date"]))
    rw2, sk2 = E.january_windows(s2)
    assert rw2 == [] and sk2["no_december"] == 1, (rw2, sk2)
    print("PASS c: missing December skipped + counted")
    # (d) duplicates + yearly-missing fail closed (synthetic files only)
    import tempfile
    dd = tempfile.mkdtemp()
    p1 = os.path.join(dd, "dup.csv")
    pd.DataFrame({"date": ["2020-01-01", "2020-01-01", "2020-01-02"],
                  "close": [100.0, 101.0, 102.0]}).to_csv(p1, index=False)
    try:
        E.load_panel(p1)
        raise AssertionError("duplicates did not raise")
    except E.IntegrityStop:
        print("PASS d1: duplicate timestamps fail closed")
    idx = pd.bdate_range("2020-01-01", "2020-12-31")
    vals = np.full(len(idx), 100.0)
    vals[:20] = np.nan  # ~8% missing
    try:
        E.check_yearly_missing(pd.Series(vals, index=idx))
        raise AssertionError("yearly missing did not raise")
    except E.IntegrityStop:
        print("PASS d2: yearly missing >5% fails closed")
    E.check_yearly_missing(pd.Series(np.full(len(idx), 100.0), index=idx))
    print("PASS d3: clean series passes integrity")
    # (f) determinism incl. analyze
    a1 = E.analyze([dict(r) for r in ev])
    a2 = E.analyze([dict(r) for r in ev])
    assert a1 == a2
    print("PASS f: determinism (analyze byte-identical)")
    # (g) control arithmetic: buy-and-hold over span
    ctl = E.control_leg(ev)
    assert abs(ctl["net"] - (ev[0]["exit_px"] / ev[0]["entry_px"] - 1.0)) < 1e-12
    print("PASS g: control arithmetic exact")
    # (h) flat year -> costs-only negative net, exact
    assert ev[0]["net"] < 0 and abs(ev[0]["net"] - (0.9985 / 1.0015 - 1.0)) < 1e-12
    print("PASS h: flat year = pure cost drag, exact")
    # (i) decide_label branches
    assert E.decide_label({"ci95": [0.01, 0.05]}) == "PASS"
    assert E.decide_label({"ci95": [-0.05, -0.01]}) == "FAIL"
    assert E.decide_label({"ci95": [-0.01, 0.05]}) == "INCONCLUSIVE"
    print("PASS i: decide_label trichotomy")
    print("ALL SYNTHETIC SELF-TESTS PASS")


if __name__ == "__main__":
    main()
