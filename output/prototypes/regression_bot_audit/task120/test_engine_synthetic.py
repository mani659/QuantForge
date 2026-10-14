"""Synthetic self-test for cand025_engine (TASK120 G4). Synthetic CSVs only.
No market data. Asserts rule semantics, fail-closed handling, determinism.
"""
import os
import sys
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cand025_engine as E


def m1_series(day, start_hhmm, n_min, base, shocks):
    """Build minute bars: base price random-walk-ish flat + shock list.

    shocks: list of (minute_offset, o,h,l,c). Returns list of rows.
    """
    rows = []
    px = base
    shock = {m: v for m, v in shocks}
    for m in range(n_min):
        hh = int(start_hhmm[:2]) + (int(start_hhmm[3:]) + m) // 60
        mm = (int(start_hhmm[3:]) + m) % 60
        t = "%s %02d:%02d:00+00:00" % (day, hh, mm)
        if m in shock:
            o, h, l, c = shock[m]
        else:
            o, h, l, c = px, px + 0.05, px - 0.05, px + 0.01
            px = c
        rows.append({"time": t, "open": o, "high": h, "low": l, "close": c})
    return rows


def save(path, rows):
    pd.DataFrame(rows).to_csv(path, index=False)


def run(path):
    m1, meta = E.load_m1(path)
    m5 = E.to_m5_complete(m1)
    return E.enumerate_events(m5), E.to_m5_complete(m1)


def main():
    td = tempfile.mkdtemp()
    # Quiet history: 20 calm UTC days to seed ATR (08:00-10:00 ET = 12:00-14:00 UTC).
    base_rows = []
    day0 = pd.Timestamp("2024-01-08")
    for d in range(20):
        day = (day0 + pd.Timedelta(days=d)).strftime("%Y-%m-%d")
        base_rows += m1_series(day, "12:00", 150, 100.0, [])
    # Event day 2024-02-05 (Monday): calm until 13:30 UTC bar (08:30 ET),
    # which spikes: open 100, high 104, low 99.5, close 103.5 (TR=4.5 vs ATR~0.2).
    ev = m1_series("2024-02-05", "12:00", 90, 100.0, [])  # 12:00-13:29 UTC
    # overwrite 13:30-13:34 minutes to form shock M5 bar: o=100,h=104,l=99.5,c=103.5
    ev += [{"time": "2024-02-05 13:30:00+00:00", "open": 100.0, "high": 101.0,
            "low": 99.8, "close": 100.5},
           {"time": "2024-02-05 13:31:00+00:00", "open": 100.5, "high": 102.0,
            "low": 100.0, "close": 101.5},
           {"time": "2024-02-05 13:32:00+00:00", "open": 101.5, "high": 104.0,
            "low": 101.0, "close": 103.0},
           {"time": "2024-02-05 13:33:00+00:00", "open": 103.0, "high": 103.5,
            "low": 99.5, "close": 100.0},
           {"time": "2024-02-05 13:34:00+00:00", "open": 100.0, "high": 101.0,
            "low": 99.9, "close": 103.5}]
    # 13:35 open = 104.0 (entry), drift to 13:35+60min exit open 102.0
    ev += m1_series("2024-02-05", "13:35", 65, 104.0, [])  # flat ~104
    p1 = os.path.join(td, "synth1.csv")
    save(p1, base_rows + ev)
    (events, skips), m5b = run(p1)
    assert len(events) == 1, events
    e = events[0]
    assert e["date"] == "2024-02-05", e
    # shock bar: o=100,c=103.5 -> dir = -1; entry 104.0; exit = open of
    # 14:30 UTC bar = first row of the 13:35+65 block end? exit open check:
    assert e["dir"] == -1.0, e
    assert abs(e["entry_open"] - 104.0) < 1e-9, e
    rows = E.evaluate(events)
    assert abs(rows[0]["gross"] - (-1.0 * (rows[0]["exit_open"] - 104.0))) < 1e-9
    assert abs(rows[0]["net2"] - (rows[0]["gross"] - 2.0)) < 1e-9
    assert abs(rows[0]["net3"] - (rows[0]["gross"] - 3.0)) < 1e-9
    print("PASS a: planted event exact (dir/entry/costs)")
    # T4 smoke: runs, returns denom/flag ints
    f = E.t4_flag(m5b, events)
    assert set(f) == {"denom", "continued", "flag"}, f
    print("PASS t4: structure ok", f)
    # determinism: rerun byte-identical event JSON
    (events2, _), _ = run(p1)
    assert events == events2
    print("PASS determinism")
    # analyze smoke on synthetic nets
    a = E.analyze(rows * 12)
    assert a["n"] == 12 and "holm_p" in a and "ci95" in a
    print("PASS analyze smoke")
    # quiet-only file -> zero events
    p2 = os.path.join(td, "synth2.csv")
    save(p2, base_rows)
    (ev0, _), _ = run(p2)
    assert ev0 == [], ev0
    print("PASS b: quiet days -> no events")
    # zero-direction shock bar (close == open, big range) -> skipped
    zrows = list(base_rows)
    zrows += m1_series("2024-02-06", "12:00", 90, 100.0, [])
    zrows += [{"time": "2024-02-06 13:30:00+00:00", "open": 100.0, "high": 103.0,
               "low": 97.0, "close": 100.5},
              {"time": "2024-02-06 13:31:00+00:00", "open": 100.5, "high": 101.0,
               "low": 99.0, "close": 100.2},
              {"time": "2024-02-06 13:32:00+00:00", "open": 100.2, "high": 102.0,
               "low": 98.0, "close": 100.8},
              {"time": "2024-02-06 13:33:00+00:00", "open": 100.8, "high": 101.5,
               "low": 97.5, "close": 100.1},
              {"time": "2024-02-06 13:34:00+00:00", "open": 100.1, "high": 100.5,
               "low": 99.5, "close": 100.0}]
    zrows += m1_series("2024-02-06", "13:35", 65, 100.0, [])
    p3 = os.path.join(td, "synth3.csv")
    save(p3, zrows)
    m3, _ = E.load_m1(p3)
    (ev3, sk3) = E.enumerate_events(E.to_m5_complete(m3))
    assert ev3 == [] and sk3["zero_dir"] == 1, (ev3, sk3)
    print("PASS c: zero-direction shock -> skipped, counted")
    # missing 09:30 bar -> skipped incomplete
    irows = list(base_rows)
    irows += m1_series("2024-02-07", "12:00", 90, 100.0, [])
    irows += [{"time": "2024-02-07 13:30:00+00:00", "open": 100.0, "high": 101.0,
               "low": 99.8, "close": 100.5},
              {"time": "2024-02-07 13:31:00+00:00", "open": 100.5, "high": 102.0,
               "low": 100.0, "close": 101.5},
              {"time": "2024-02-07 13:32:00+00:00", "open": 101.5, "high": 104.0,
               "low": 101.0, "close": 103.0},
              {"time": "2024-02-07 13:33:00+00:00", "open": 103.0, "high": 103.5,
               "low": 99.5, "close": 100.0},
              {"time": "2024-02-07 13:34:00+00:00", "open": 100.0, "high": 101.0,
               "low": 99.9, "close": 103.5}]
    irows += m1_series("2024-02-07", "13:35", 55, 104.0, [])  # ends 14:29, no 14:30 bar
    p4 = os.path.join(td, "synth4.csv")
    save(p4, irows)
    m4, _ = E.load_m1(p4)
    (ev4, sk4) = E.enumerate_events(E.to_m5_complete(m4))
    assert ev4 == [] and sk4["incomplete"] == 1, (ev4, sk4)
    print("PASS d: missing 09:30 bar -> skipped, counted")
    print("ALL SYNTHETIC SELF-TESTS PASS")


if __name__ == "__main__":
    main()
