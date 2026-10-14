"""CAND-025 re-measurement engine (TASK120, approved chain CAND025-RM-01).

Implements EXACTLY the frozen V9 rule; no variants, no search, no adaptation:
  signal : 08:30-08:35 America/New_York M5 bar True Range > 3.0 x M5 ATR(14),
           ATR over the 14 M5 bars with close_time <= 08:30:00 (Wilder RMA,
           standard ATR definition), TR uses prev close = 08:30:00 close.
  entry  : reversal at 08:35 open, dir = -sign(sig_close - sig_open);
           zero direction -> skip (counted).
  exit   : 09:30 open. gross_pts = dir * (exit_open - entry_open).
  costs  : net = gross - 2.0 (primary), gross - 3.0 (stress), points/round-trip.
Completeness (fail-closed, counted): signal bar needs 5/5 M1 bars; ATR needs
14 prior M5 bars; 08:35-bar open and 09:30-bar open must exist; otherwise skip.
Causality: every input bar is complete with timestamps <= its use point.
No RNG in enumeration/evaluation (bootstrap seeding fixed at analysis call).
Reads ONLY the caller-supplied M1 CSV. No network, no MT5, no other files.
"""

import hashlib
import json
import math
import os

import numpy as np
import pandas as pd

SPEC = {
    "rule": "V9 CAND-G0-025",
    "atr_len": 14,
    "tr_mult": 3.0,
    "signal_open": "08:30",
    "entry_open": "08:35",
    "exit_open": "09:30",
    "max_per_day": 1,
    "tz": "America/New_York",
    "cost_primary": 2.0,
    "cost_stress": 3.0,
    "seed": 20261013,
    "boot_b": 10000,
    "holm_alpha": 0.05,
}

REQUIRED_COLS = ("open", "high", "low", "close")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_m1(path):
    """Read M1 CSV (metadata + OHLC). Returns (df_utc, meta). No analysis."""
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    tcol = (cols.get("timestamp") or cols.get("time") or cols.get("date")
            or cols.get("datetime"))
    if tcol is None:
        raise ValueError("no time column")
    for c in REQUIRED_COLS:
        if c not in cols:
            raise ValueError("missing column: " + c)
    ts = pd.to_datetime(df[tcol], utc=True)
    out = pd.DataFrame({
        "open": pd.to_numeric(df[cols["open"]], errors="coerce").to_numpy(),
        "high": pd.to_numeric(df[cols["high"]], errors="coerce").to_numpy(),
        "low": pd.to_numeric(df[cols["low"]], errors="coerce").to_numpy(),
        "close": pd.to_numeric(df[cols["close"]], errors="coerce").to_numpy(),
    }, index=ts)
    out = out.sort_index()
    meta = {"rows": int(len(out)), "first": str(out.index[0]),
            "last": str(out.index[-1])}
    return out, meta


def to_m5_complete(m1):
    """Left-labeled M5 bars having all 5 M1 bars. Causal: complete bars only."""
    cnt = m1["close"].resample("5min", label="left", closed="left").count()
    g = m1.resample("5min", label="left", closed="left")
    m5 = pd.DataFrame({"open": g["open"].first(), "high": g["high"].max(),
                       "low": g["low"].min(), "close": g["close"].last()})
    m5 = m5[cnt == 5].dropna()
    return m5


def wilder_atr(m5, n):
    """Wilder ATR; atr[i] uses bars <= i only (causal)."""
    prev = m5["close"].shift(1)
    tr = pd.concat([m5["high"] - m5["low"], (m5["high"] - prev).abs(),
                    (m5["low"] - prev).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1.0 / n, min_periods=n, adjust=False).mean()
    return atr, tr


def enumerate_events(m5):
    """Outcome-blind event enumeration (no returns). Returns (events, skips)."""
    atr, tr = wilder_atr(m5, SPEC["atr_len"])
    local = m5.tz_convert(SPEC["tz"])
    opens = {ts: o for ts, o in zip(m5.index, m5["open"])}
    closes = {ts: c for ts, c in zip(m5.index, m5["close"])}
    events, skips = [], {"no_atr": 0, "incomplete": 0, "zero_dir": 0}
    for day, grp in local.groupby(local.index.date):
        sig_ts = [t for t in grp.index if t.strftime("%H:%M") == SPEC["signal_open"]]
        if not sig_ts:
            continue
        s = sig_ts[0]
        su = s.tz_convert("UTC")
        a = atr.loc[:su]
        if len(a.dropna()) < 1 or math.isnan(a.iloc[-1]):
            skips["no_atr"] += 1
            continue
        # ATR window: 14 bars with close_time <= 08:30, signal bar excluded.
        hist = m5.loc[:su].iloc[:-1]
        if len(hist) < SPEC["atr_len"]:
            skips["no_atr"] += 1
            continue
        aval = atr.loc[hist.index].iloc[-1]
        if math.isnan(aval):
            skips["no_atr"] += 1
            continue
        tval = tr.loc[su]
        if not (tval > SPEC["tr_mult"] * aval):
            continue
        entry_ts = su + pd.Timedelta(minutes=5)
        exit_ts = su + pd.Timedelta(minutes=60)
        if entry_ts not in opens or exit_ts not in opens:
            skips["incomplete"] += 1
            continue
        direction = -float(np.sign(closes[su] - opens[su]))
        if direction == 0.0:
            skips["zero_dir"] += 1
            continue
        events.append({"date": str(day), "entry_open": float(opens[entry_ts]),
                       "exit_open": float(opens[exit_ts]), "dir": direction})
        if len([e for e in events if e["date"] == str(day)]) > SPEC["max_per_day"]:
            events.pop()
    events.sort(key=lambda e: e["date"])
    return events, skips


def evaluate(events):
    """Frozen arithmetic only: gross/net points per event. No statistics."""
    out = []
    for e in events:
        gross = e["dir"] * (e["exit_open"] - e["entry_open"])
        out.append({"date": e["date"], "entry_open": e["entry_open"],
                    "exit_open": e["exit_open"], "dir": e["dir"],
                    "gross": gross, "net2": gross - SPEC["cost_primary"],
                    "net3": gross - SPEC["cost_stress"]})
    return out


def analyze(rows):
    """Adopted inferential procedure (T1-T4). Deterministic given seed."""
    rng = np.random.default_rng(SPEC["seed"])
    n = len(rows)
    res = {"n": n}
    if n == 0:
        return res
    net2 = np.array([r["net2"] for r in rows])
    net3 = np.array([r["net3"] for r in rows])
    dates = np.array([r["date"] for r in rows])
    cut = dates[n // 2] if n > 1 else dates[0]
    h1, h2 = net2[dates < cut], net2[dates >= cut]
    res["t1_halves"] = [float(h1.mean()) if len(h1) else float("nan"),
                        float(h2.mean()) if len(h2) else float("nan")]
    res["t1_pass"] = bool(len(h1) > 0 and len(h2) > 0
                          and h1.mean() > 0 and h2.mean() > 0)
    res["mean_net2"] = float(net2.mean())
    res["mean_net3"] = float(net3.mean())
    cis, ps = {}, {}
    for key, v in (("net2", net2), ("net3", net3)):
        bm = np.array([rng.choice(v, size=n, replace=True).mean()
                       for _ in range(SPEC["boot_b"])])
        cis[key] = [float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))]
        ps[key] = float((bm <= 0).mean())
    res["ci95"] = cis
    ordered = sorted(ps.items(), key=lambda kv: kv[1])
    adj, prev = {}, 0.0
    m = len(ordered)
    for rank, (k, p) in enumerate(ordered, 1):
        prev = max(prev, p * (m - rank + 1))
        adj[k] = min(prev, 1.0)
    res["holm_p"] = adj
    res["t3_pass"] = bool(cis["net2"][0] > 0 and cis["net3"][0] > 0
                          and adj["net2"] < SPEC["holm_alpha"]
                          and adj["net3"] < SPEC["holm_alpha"])
    return res


def t4_flag(m5, events):
    """V9 falsification direction (ADOPTED majority form). Predeclared."""
    local = m5.tz_convert(SPEC["tz"])
    by_ts = {t: (o, c) for t, o, c in
             zip(m5.index, m5["open"], m5["close"])}
    cont, denom = 0, 0
    for e in events:
        day = pd.Timestamp(e["date"]).date()
        grp = local[local.index.date == day]
        post = [t for t in grp.index if t.strftime("%H:%M") == "08:35"]
        sig = [t for t in grp.index if t.strftime("%H:%M") == "08:30"]
        if not post or not sig:
            continue
        su = sig[0].tz_convert("UTC")
        pu = post[0].tz_convert("UTC")
        if su not in by_ts or pu not in by_ts:
            continue
        shock = float(np.sign(by_ts[su][1] - by_ts[su][0]))
        move = float(np.sign(by_ts[pu][1] - by_ts[pu][0]))
        if shock == 0.0:
            continue
        denom += 1
        if move == shock:
            cont += 1
    return {"denom": denom, "continued": cont,
            "flag": bool(denom > 0 and cont > denom / 2.0)}
