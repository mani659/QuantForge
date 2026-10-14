"""TASK151 single bounded measurement run (approved TASK148 chain).
Gates first; ONE run; bounded outputs. No rescue, no refit, no reseed.
"""
import csv
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regime_pipeline as P

ROOT = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", "output",
                                     "prototypes", "fx_h4inv_adx_prep"))


def main():
    from sklearn.cluster import KMeans  # gate: import must succeed
    assert P.KS == [2, 3] and P.SEEDS == list(range(10))
    # ---- Phase 0: pre-use gates ----
    gate = {"files": {}, "sha": {}}
    for sym in P.SYMBOLS:
        p = os.path.join(PANEL, "_t37_m1_" + sym + ".npz")
        assert os.path.isfile(p), "missing file: " + sym
        gate["files"][sym] = os.path.getsize(p)
        gate["sha"][sym] = P.sha256_file(p)
    print("gate: 11 files present", flush=True)
    # ---- Phase 1: load + integrity + features ----
    syms = {}
    for sym in P.SYMBOLS:
        df = P.load_symbol(os.path.join(PANEL, "_t37_m1_" + sym + ".npz"), sym)
        n = len(df)
        assert n == P.EXPECTED_ROWS[sym], (sym, n, P.EXPECTED_ROWS[sym])
        syms[sym] = df
    print("gate: row counts match prereg table", flush=True)
    full, drop = P.build_matrix({s: P.daily_features(d)[0] for s, d in syms.items()})
    print("matrix rows: %d symbols: %d drops: %s" % (
        len(full), full["sym"].nunique(), drop), flush=True)
    tr, va, te = P.split_segments(full)
    assert len(tr) > 0 and len(va) > 0 and len(te) > 0
    Xtr, Xva, Xte, mu, sd = P.standardize(tr, va, te)
    # ---- Phase 2: fits (budget: 2 k + tertile + null = 5) ----
    out = {"gates": gate, "drops": drop,
           "n": {"train": len(tr), "val": len(va), "test": len(te)},
           "configs": {}, "test_labels": {}}
    for k in P.KS:
        km, _ = P.fit_kmeans(Xtr, k)
        lab_va = km.predict(Xva.values)
        lab_te = km.predict(Xte.values)
        out["test_labels"][str(k)] = [int(x) for x in lab_te]
        km_va, lab_vaown = P.fit_kmeans(Xva, k)
        ari_va = P.match_ari(km_va.cluster_centers_, lab_vaown,
                             km.cluster_centers_, lab_va)
        km_te, lab_teown = P.fit_kmeans(Xte, k)
        ari_te = P.match_ari(km_te.cluster_centers_, lab_teown,
                             km.cluster_centers_, lab_te)
        prev = P.prevalence(lab_te, k)
        dwell = P.dwell(np.asarray(lab_te))
        out["configs"][str(k)] = {
            "ari_val": ari_va, "ari_test": ari_te,
            "prevalence_test": prev, "dwell_test": dwell,
            "centroids": km.cluster_centers_.tolist()}
        print("k=%d ari_val=%.3f ari_test=%.3f prev=%s dwell=%.1f" % (
            k, ari_va, ari_te,
            {c: round(v, 3) for c, v in prev.items()}, dwell), flush=True)
    # tertile baseline on pooled log_rv (TRAIN cut points, deterministic)
    cuts = Xtr["log_rv"].quantile([1 / 3, 2 / 3]).tolist()
    t_te = pd.cut(Xte["log_rv"], [-np.inf] + cuts + [np.inf], labels=[0, 1, 2])
    t_te = np.asarray(t_te.tolist(), dtype=int)
    out["tertile"] = {
        "prevalence_test": {int(c): float((t_te == c).mean()) for c in [0, 1, 2]},
        "dwell_test": P.dwell(t_te)}
    print("tertile prev=%s dwell=%.1f" % (
        {c: round(v, 3) for c, v in out["tertile"]["prevalence_test"].items()},
        out["tertile"]["dwell_test"]), flush=True)
    # shuffled null: permute TRAIN rows (seed 0), fit k=3, map val
    prng = np.random.default_rng(0)
    Xp = Xtr.iloc[prng.permutation(len(Xtr))].reset_index(drop=True)
    kmn, _ = P.fit_kmeans(Xp, 3)
    labn_va = kmn.predict(Xva.values)
    kmv, labv = P.fit_kmeans(Xva, 3)
    out["null_ari_val"] = P.match_ari(kmv.cluster_centers_, labv,
                                      kmn.cluster_centers_, labn_va)
    print("null ARI (expect ~=0): %.3f" % out["null_ari_val"], flush=True)
    # ---- Phase 3: verdict per frozen rules ----
    def verdict(ari_v, ari_t, prev):
        if ari_v >= 0.5 and ari_t >= 0.5 and all(v >= 0.10 for v in prev.values()):
            return "CONTINUE"
        if ari_v < 0.3 or ari_t < 0.3 or any(v < 0.05 for v in prev.values()):
            return "FAIL"
        return "INCONCLUSIVE"
    vs = {}
    for k in P.KS:
        c = out["configs"][str(k)]
        vs[str(k)] = verdict(c["ari_val"], c["ari_test"], c["prevalence_test"])
    order = {"CONTINUE": 2, "INCONCLUSIVE": 1, "FAIL": 0}
    best = max(vs, key=lambda k: order[vs[k]])
    if vs[best] == "CONTINUE" and out["null_ari_val"] >= 0.2:
        out["verdict"] = {"k": best, "label": "INCONCLUSIVE",
                          "note": "null override: null ARI >= 0.2"}
    else:
        out["verdict"] = {"k": best, "label": vs[best]}
    out["verdicts"] = vs
    # ---- write bounded outputs ----
    te_reset = te.reset_index(drop=True)
    with open(os.path.join(ROOT, "assignments.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "sym", "cluster_k2", "cluster_k3"])
        for i, r in te_reset.iterrows():
            w.writerow([r["date"], r["sym"],
                        out["test_labels"]["2"][i],
                        out["test_labels"]["3"][i]])
    with open(os.path.join(ROOT, "metrics.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True,
                  default=lambda o: float(o) if isinstance(o, np.floating) else o)
    print("verdict: %s" % (out["verdict"],), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
