"""Synthetic self-test for regime_pipeline (TASK151 G4). Synthetic OHLC only."""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regime_pipeline as P


def synth_m1(day, n_min, base, ret_std, seed):
    rng = np.random.default_rng(seed)
    rows = []
    px = base
    t0 = pd.Timestamp(day, tz="UTC")
    for m in range(n_min):
        r = rng.normal(0, ret_std)
        o, c = px, px * (1 + r)
        h, l = max(o, c) * 1.0005, min(o, c) * 0.9995
        rows.append({"t": t0 + pd.Timedelta(minutes=m), "o": o, "h": h,
                     "l": l, "c": c, "s": 0.0002})
        px = c
    return pd.DataFrame(rows)


def frame_from_days(specs):
    """specs: list of (day_str, ret_std, seed). Returns M1-style frame."""
    parts = []
    for day, rs, sd in specs:
        m = synth_m1(day, 600, 100.0, rs, sd)
        parts.append(m)
    f = pd.concat(parts, ignore_index=True)
    return pd.DataFrame({"open": f["o"].values, "high": f["h"].values,
                         "low": f["l"].values, "close": f["c"].values,
                         "spread": f["s"].values}, index=pd.to_datetime(f["t"], utc=True))


def main():
    # (a) planted 2-regime blocks: 20 calm days + 20 wild days, k=2
    specs = ([("2024-01-%02d" % d, 0.0005, d) for d in range(1, 21)]
             + [("2024-02-%02d" % d, 0.01, 100 + d) for d in range(1, 21)])
    m1 = frame_from_days(specs)
    full, drop = P.build_matrix({"SYN": P.daily_features(m1)[0]})
    assert len(full) == 21, (len(full), drop)  # 40 days minus 19 warmup rows
    X = full[["log_rv", "log_park"]].copy()
    mu, sd = X.mean(), X.std(ddof=1)
    Xs = (X - mu) / sd
    km1, lab1 = P.fit_kmeans(Xs, 2)
    km2, lab2 = P.fit_kmeans(Xs, 2)
    assert list(lab1) == list(lab2), "nondeterministic"
    truth = np.array([0] + [1] * 20)  # kept days 19-39: 1 calm + 20 wild
    ari = P.match_ari(km1.cluster_centers_, lab1,
                      km1.cluster_centers_, truth)
    assert ari > 0.8, ari
    print("PASS a: planted regimes recovered, ARI=%.3f, deterministic" % ari)
    # (b) constant data runs without crash (degeneracy caught downstream)
    mc = frame_from_days([("2024-03-%02d" % d, 0.0, 7) for d in range(1, 11)])
    dc, _ = P.daily_features(mc)
    print("PASS b: constant-data handling, rows=%d" % len(dc))
    # (c) zero-bar day dropped + counted (gap day present)
    g1 = frame_from_days([("2024-04-0%d" % d, 0.002, d) for d in range(1, 5)])
    g2 = frame_from_days([("2024-04-0%d" % d, 0.002, 50 + d) for d in range(7, 10)])
    g = pd.concat([g1, g2])
    dg, dropg = P.daily_features(g)
    assert len(dg) == 7, (len(dg), dropg)
    print("PASS c: gap days absent from output (7 daily rows, no fill)")
    # (d) match_ari identity + prevalence/dwell units
    assert abs(P.match_ari(np.array([[0.0], [5.0]]), np.array([0, 0, 1, 1]),
                           np.array([[0.1], [4.9]]), np.array([0, 0, 1, 1])) - 1.0) < 1e-9
    pr = P.prevalence(np.array([0, 0, 0, 1]), 2)
    assert abs(pr[0] - 0.75) < 1e-9 and abs(pr[1] - 0.25) < 1e-9
    assert abs(P.dwell(np.array([0, 0, 1, 1, 1, 0])) - 2.0) < 1e-9
    print("PASS d: match_ari/prevalence/dwell units exact")
    # (e) tertile + null smoke on synthetic features
    Xt = pd.DataFrame({"log_rv": np.concatenate([np.random.default_rng(0).normal(-2, 0.3, 60),
                                                  np.random.default_rng(1).normal(1, 0.3, 60)])})
    q = Xt["log_rv"].quantile([1/3, 2/3]).tolist()
    tl = pd.cut(Xt["log_rv"], [-np.inf] + q + [np.inf], labels=[0, 1, 2])
    assert set(tl.dropna().unique()) == {0, 1, 2}
    print("PASS e: tertile baseline smoke")
    print("ALL SYNTHETIC SELF-TESTS PASS")


if __name__ == "__main__":
    main()
