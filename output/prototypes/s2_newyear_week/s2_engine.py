"""S2 New-Year week engine (TASK166; frozen spec 166_s2_frozen_spec.md).

Implements EXACTLY the frozen rule; no variants, no search, no adaptation.
Unconditional January-week long; buy-and-hold control for descriptive
comparison only (never a paired test — S4 degeneracy avoided by design).
"""
import hashlib
import math

import numpy as np
import pandas as pd

SPEC = {
    "rule": "PROTO-S2-001 v1-frozen",
    "window": "first-5 January row-dates (J1..J5)",
    "direction": "long 1.0",
    "entry_mult": 1.0015,
    "exit_mult": 0.9985,
    "commission": 0.0,
    "seed": 20261015,
    "boot_b": 10000,
}

RATE_ONE_WAY = 0.0015


class IntegrityStop(Exception):
    """Fail-closed data integrity stop. No measurement proceeds."""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_panel(path):
    """Read date + close columns. Returns (series, meta). No analysis."""
    df = pd.read_csv(path)
    dcol = df.columns[0]
    cands = [c for c in df.columns if c.lower() in ("close", "adj close",
                                                   "adj_close", "price")]
    vcol = cands[0] if cands else df.columns[1]
    dates = pd.to_datetime(df[dcol])
    vals = pd.to_numeric(df[vcol], errors="coerce")
    s = pd.Series(vals.values, index=dates).sort_index()
    if bool(s.index.duplicated().any()):
        raise IntegrityStop("duplicate timestamps present")
    meta = {"rows": int(len(s)), "first": str(s.index[0].date()),
            "last": str(s.index[-1].date()),
            "missing": int(s.isna().sum())}
    return s, meta


def check_yearly_missing(s):
    """NaN-rate per calendar year >5% -> STOP (pattern precedent)."""
    for y in sorted(set(s.index.year)):
        g = s[s.index.year == y]
        if float(g.isna().sum()) / max(len(g), 1) > 0.05:
            raise IntegrityStop("year %d missing rate > 0.05" % y)


def january_windows(s):
    """Yield (year, entry_date, exit_date, entry_px, exit_px) per rule.

    Entry = last December row-date close x 1.0015; exit = 5th January
    row-date close x 0.9985. Years lacking either endpoint are SKIPPED
    (fail-closed) with counts — never filled or shifted.
    """
    rows, skips = [], {"no_december": 0, "short_january": 0}
    years = sorted(set(s.index.year))
    for y in years:
        dec = s[(s.index.year == y - 1) & (s.index.month == 12)].dropna()
        jan = s[(s.index.year == y) & (s.index.month == 1)].dropna()
        if len(dec) == 0:
            skips["no_december"] += 1
            continue
        if len(jan) < 5:
            skips["short_january"] += 1
            continue
        entry_date = dec.index[-1]
        exit_date = jan.index[4]
        rows.append({"year": y, "entry_date": entry_date,
                     "exit_date": exit_date,
                     "entry_px": float(dec.iloc[-1]) * 1.0015,
                     "exit_px": float(jan.iloc[4]) * 0.9985})
    return rows, skips


def evaluate(windows):
    """Frozen arithmetic: net return per January window + control legs."""
    out = []
    for w in windows:
        net = w["exit_px"] / w["entry_px"] - 1.0
        out.append({"year": w["year"], "net": net,
                    "entry_px": w["entry_px"], "exit_px": w["exit_px"]})
    return out


def control_leg(windows):
    """Buy-and-hold over identical span (first entry -> last exit)."""
    if not windows:
        return {"entry_px": None, "exit_px": None, "net": None}
    # Same multipliers as strategy legs (entry ask-side, exit bid-side),
    # charged once each over the full span — identical cost schedule.
    e0 = windows[0]["entry_px"]
    x1 = windows[-1]["exit_px"]
    return {"entry_px": e0, "exit_px": x1, "net": x1 / e0 - 1.0}


def analyze(rows):
    """Primary: mean annual net + 95% bootstrap CI. Deterministic."""
    rng = np.random.default_rng(SPEC["seed"])
    v = np.array([r["net"] for r in rows])
    n = len(v)
    res = {"n": n}
    if n == 0:
        return res
    bm = np.array([rng.choice(v, size=n, replace=True).mean()
                   for _ in range(SPEC["boot_b"])])
    res["mean"] = float(v.mean())
    res["ci95"] = [float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))]
    return res


def decide_label(res):
    """Frozen trichotomy: PASS lower>0; FAIL upper<0; else INCONCLUSIVE."""
    lo, hi = res["ci95"]
    if lo > 0:
        return "PASS"
    if hi < 0:
        return "FAIL"
    return "INCONCLUSIVE"
