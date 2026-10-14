"""VS-TSMOM-01 measurement engine (TASK146, approved chain; v5 frozen spec).

Implements EXACTLY v5 (task144/144_preregistration_v5.md) + CLOSE-01
next-close convention. No variants, no search, no adaptation. Fixed leg is
the COMP-01 benchmark-only comparator (never standalone). Passive leg is
buy-and-hold.

v5 frozen points (with provenance):
- r12 = P(T)/P(T-12m)-1, T = last available row date of month; ties flat
  (TASK134 §3).
- Vol = prior calendar month realized vol, std of daily simple returns
  (ddof=1: pandas default + VM-001 n-1 precedent) x sqrt(252). Months with
  <2 valid bars yield NaN -> skip (counted); no other minimum exists on
  record, none invented.
- w = sign(r12) x min(1, 0.10/target sigma); fixed leg f = sign(r12) x 1.0;
  passive p = 1.0 always. Bounds [-1,+1]. First month builds from zero
  (flat -> target IS a target change per "trade only on target change").
- Entry E(m) = first daily close strictly after T(m) (CLOSE-01 next-close
  rule); holding return R(m) = E(m+1)/E(m) - 1. Same-close fills prohibited.
- Costs: Batch-1 family 10/5/0 bps per side on |Delta w| (declared
  assumption, not broker fact); grid x0.5/1/2/4; financing stress 0/2/4%
  per year on gross notional |w| (stress-only).
- Missing: yearly NaN rate >5% -> STOP; timestamp duplicates -> STOP
  (fail closed); no fill. Months lacking anchor/vol/entry -> excluded
  from ALL series (paired integrity), counted.
- Inference: circular block bootstrap block 12, B=10000, seed 20261014;
  one-sided 95% lower bound (5th pct); upper bound = 95th pct (the matching
  end of the stated interval; predeclared reading); one-sided bootstrap
  p-values; Holm alpha 0.05 across {D1, D2}.
- PASS: D1 lower>0 (Holm-adj p<0.05) AND ratio>=2 (CONFIRMED ACTIVE).
  FAIL: D1 upper<0. Else INCONCLUSIVE (incl. lower>0 + ratio<2: statically
  positive, economically immaterial per the bar — TASK139/140 fix).
"""

import hashlib
import math

import numpy as np
import pandas as pd

SPEC = {
    "rule": "VS-TSMOM-01 v5",
    "lookback_months": 12,
    "vol_window": "prior calendar month",
    "target_vol": 0.10,
    "rebalance": "monthly",
    "entry": "first daily close strictly after T(m)",
    "tie": "flat (0.0)",
    "bounds": [-1.0, 1.0],
    "spread_bps": 10.0,
    "slippage_bps": 5.0,
    "commission_bps": 0.0,
    "cost_grid": [0.5, 1.0, 2.0, 4.0],
    "financing_stress": [0.0, 0.02, 0.04],
    "boot_block": 12,
    "boot_b": 10000,
    "seed": 20261014,
    "holm_alpha": 0.05,
    "upper_pct": 95.0,
    "ratio_bar": 2.0,
}

RATE = (SPEC["spread_bps"] + SPEC["slippage_bps"]
        + SPEC["commission_bps"]) / 10000.0


class IntegrityStop(Exception):
    """Fail-closed data integrity stop. No measurement proceeds."""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_fred(path):
    """Read FRED daily closes (date + value). Returns (series, meta)."""
    df = pd.read_csv(path)
    dcol = df.columns[0]
    vcol = [c for c in df.columns if c != dcol][0]
    dates = pd.to_datetime(df[dcol])
    vals = pd.to_numeric(df[vcol], errors="coerce")
    s = pd.Series(vals.values, index=dates).sort_index()
    meta = {"rows": int(len(s)), "first": str(s.index[0].date()),
            "last": str(s.index[-1].date()),
            "missing": int(s.isna().sum())}
    return s, meta


def check_integrity(s):
    """Fail-closed gates: duplicates STOP; yearly NaN rate >5% STOPS."""
    if bool(s.index.duplicated().any()):
        raise IntegrityStop("duplicate timestamps present")
    years = sorted(set(s.index.year))
    for y in years:
        g = s[s.index.year == y]
        rate = float(g.isna().sum()) / max(len(g), 1)
        if rate > 0.05:
            raise IntegrityStop("year %d NaN rate %.3f > 0.05" % (y, rate))
    return {"years": [int(y) for y in years]}


def month_closes(s):
    """Last non-missing close per calendar month -> {Period: (date, price)}."""
    out = {}
    for per, grp in s.groupby(s.index.to_period("M")):
        g = grp.dropna()
        if len(g):
            out[str(per)] = (g.index[-1], float(g.iloc[-1]))
    return out


def evaluate_panel(s, mult=1.0):
    """Frozen arithmetic for one cost multiplier. Returns (rows, skips)."""
    mc = month_closes(s)
    months = sorted(mc.keys())
    daily = s.dropna()
    rows, skips = [], {"no_anchor": 0, "no_vol": 0, "no_entry": 0}
    sig = {}
    for k in months:
        y, m = int(k[:4]), int(k[5:7])
        akey = "%04d-%02d" % (y - 1, m)
        vy, vm = (y, m - 1) if m > 1 else (y - 1, 12)
        if akey not in mc:
            skips["no_anchor"] += 1
            continue
        vd = daily[(daily.index.year == vy) & (daily.index.month == vm)]
        vr = vd.pct_change().dropna()
        vol = float(vr.std(ddof=1) * math.sqrt(252)) if len(vr) else float("nan")
        if not np.isfinite(vol) or vol <= 0:
            skips["no_vol"] += 1
            continue
        r12 = mc[k][1] / mc[akey][1] - 1.0
        if not np.isfinite(r12):
            skips["no_anchor"] += 1
            continue
        direction = float(np.sign(r12))
        sig[k] = {"dir": direction,
                  "w": direction * min(1.0, SPEC["target_vol"] / vol),
                  "f": direction * 1.0, "vol": vol, "r12": r12}
    skeys = sorted(sig.keys())
    order = list(daily.index)
    pos = {d: i for i, d in enumerate(order)}
    closes = dict(zip(order, daily.values))
    prev = {"s": 0.0, "f": 0.0, "p": 0.0}
    for i, k in enumerate(skeys[:-1]):
        k2 = skeys[i + 1]
        tk = mc[k][0]
        e1 = order[pos[tk] + 1] if pos[tk] + 1 < len(order) else None
        tk2 = mc[k2][0]
        e2 = order[pos[tk2] + 1] if pos[tk2] + 1 < len(order) else None
        if e1 is None or e2 is None:
            skips["no_entry"] += 1
            continue
        R = float(closes[e2] / closes[e1] - 1.0)
        w, f = sig[k]["w"], sig[k]["f"]
        c = RATE * mult
        cs = c * abs(w - prev["s"])
        cf = c * abs(f - prev["f"])
        cp = c * abs(1.0 - prev["p"])
        rows.append({"month": k2, "w": w, "f": f, "R": R,
                     "gross_s": w * R, "gross_f": f * R, "gross_p": 1.0 * R,
                     "cost_s": cs, "cost_f": cf, "cost_p": cp,
                     "net_s": w * R - cs, "net_f": f * R - cf,
                     "net_p": 1.0 * R - cp})
        prev = {"s": w, "f": f, "p": 1.0}
    return rows, skips


def boot_dist(v, rng):
    """Circular block bootstrap means. Deterministic given rng state."""
    n = len(v)
    L = SPEC["boot_block"]
    out = np.empty(SPEC["boot_b"])
    for b in range(SPEC["boot_b"]):
        starts = rng.integers(0, n, size=(n // L + 1))
        take = np.concatenate([(s + np.arange(L)) % n for s in starts])[:n]
        out[b] = v[take].mean()
    return out


def analyze(rows):
    """Adopted inferential procedure (D1, D2 + Holm). Deterministic."""
    rng = np.random.default_rng(SPEC["seed"])
    d1 = np.array([r["net_s"] - r["net_f"] for r in rows])
    d2 = np.array([r["net_s"] - r["net_p"] for r in rows])
    n = len(d1)
    res = {"n": n}
    if n == 0:
        return res
    lbs, ubs, ps = {}, {}, {}
    for key, v in (("d1", d1), ("d2", d2)):
        bm = boot_dist(v, rng)
        lbs[key] = float(np.percentile(bm, 5.0))
        ubs[key] = float(np.percentile(bm, SPEC["upper_pct"]))
        ps[key] = float((bm <= 0).mean())
    res["lb"] = lbs
    res["ub"] = ubs
    ordered = sorted(ps.items(), key=lambda kv: kv[1])
    adj, prev, m = {}, 0.0, len(ordered)
    for rank, (k, p) in enumerate(ordered, 1):
        prev = max(prev, p * (m - rank + 1))
        adj[k] = min(prev, 1.0)
    res["holm_p"] = adj
    res["mean_d1"] = float(d1.mean())
    res["mean_d2"] = float(d2.mean())
    res["friction"] = float(np.mean([r["cost_s"] for r in rows]))
    res["ratio"] = (float(d1.mean() / res["friction"])
                    if res["friction"] > 0 else float("nan"))
    res["turnover_s"] = float(np.mean([abs(r["w"]) for r in rows]))
    return res


def decide_label(res):
    """Frozen trichotomy (v4 fix incorporated). Ratio bar CONFIRMED ACTIVE."""
    lb = res["lb"]["d1"] > 0 and res["holm_p"]["d1"] < SPEC["holm_alpha"]
    ratio_ok = np.isfinite(res["ratio"]) and res["ratio"] >= SPEC["ratio_bar"]
    if lb and ratio_ok:
        return "PASS"
    if res["ub"]["d1"] < 0:
        return "FAIL"
    return "INCONCLUSIVE"


def diagnostics(rows):
    """Descriptive diagnostics (non-inferential)."""
    out = {}
    out["yearly"] = {}
    for r in rows:
        y = r["month"][:4]
        out["yearly"].setdefault(y, []).append(r)
    out["yearly"] = {y: {"d1": float(np.mean([x["net_s"] - x["net_f"] for x in v])),
                         "d2": float(np.mean([x["net_s"] - x["net_p"] for x in v])),
                         "n": len(v)} for y, v in out["yearly"].items()}
    out["turnover"] = {k: float(np.mean([abs(r[w]) for r in rows]))
                       for k, w in (("scaled", "w"),)}
    out["total_cost_s"] = float(sum(r["cost_s"] for r in rows))
    gross_s = np.array([r["gross_s"] for r in rows])
    out["vol_tracking"] = {"realized_ann_vol": float(gross_s.std(ddof=1)
                                                     * math.sqrt(12))
                                                  if len(gross_s) > 1 else float("nan"),
                           "target": SPEC["target_vol"]}
    return out


def cost_grid(s):
    """Mean D1/D2 at each cost multiplier (sensitivity, descriptive)."""
    grid = {}
    for m in SPEC["cost_grid"]:
        rows, _ = evaluate_panel(s, mult=m)
        if rows:
            d1 = np.array([r["net_s"] - r["net_f"] for r in rows])
            d2 = np.array([r["net_s"] - r["net_p"] for r in rows])
            grid[str(m)] = {"mean_d1": float(d1.mean()),
                            "mean_d2": float(d2.mean()), "n": len(rows)}
        else:
            grid[str(m)] = {"mean_d1": None, "mean_d2": None, "n": 0}
    return grid


def financing_stress(rows):
    """Generic rate stress on gross notional (stress-only, descriptive)."""
    out = {}
    for f in SPEC["financing_stress"]:
        stressed = [r["net_s"] - f / 12.0 * abs(r["w"]) for r in rows]
        out[str(f)] = {"mean": float(np.mean(stressed)) if stressed else None,
                       "n": len(stressed)}
    return out
