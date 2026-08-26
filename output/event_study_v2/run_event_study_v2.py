"""
QuantForge — Canonical Mean-Reversion Event Study V2
Implements EVENT_STUDY_PROTOCOL_V2.md exactly. Research artifact; not production code.
Deterministic (fixed seeds). Outputs written to output/event_study_v2/.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
DATA = Path(__file__).resolve().parents[2] / "data" / "m1"

# ---- Pre-registered protocol parameters (V2.0.0) ----
W = 120                 # displacement window (bars, M1)
M_MOM = 30              # momentum lookback (bars; metadata only in V2)
THRESH_PRIMARY = 3.0    # primary threshold, all three normalizations
THRESH_GRID = [2.5, 3.0, 3.5]
QUANT_MATCH = 0.005     # matched-quantile comparability check (0.5% tails)
S_SEP = 240             # same-direction minimum separation (bars)
H = 120                 # outcome horizon (bars)
TRAIN_END, VAL_END = 0.70, 0.85
PERSIST_H = 60          # persistence measurement window
PERSIST_Q = 0.6         # persistence retention criterion
ALPHA = 0.05
B_BOOT = 2000           # bootstrap resamples / permutation draws
SEED = 20260813
MARKETS = ["XAUUSD", "EURUSD", "BTCUSD", "XAGUSD", "USATECHIDXUSD"]
NORMALIZATIONS = ["N1", "N2", "N3"]
FOLDS = [
    ("A", 0.00, 0.40, 0.40, 0.50),
    ("B", 0.00, 0.50, 0.50, 0.60),
    ("C", 0.00, 0.60, 0.60, 0.70),
    ("D", 0.00, 0.70, 0.70, 0.85),  # == V1 VALIDATION window
]

NORM_DEFS = {
    "N1": "z=(close-SMA120)/std120(close)",
    "N2": "z=(close-SMA120)/ATR120(mean true range)",
    "N3": "z=(close/close[-120]-1)/(std120(1b returns)*sqrt(120))",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_market(market: str) -> pd.DataFrame:
    path = DATA / f"{market}_M1.csv"
    df = pd.read_csv(path, parse_dates=["timestamp"])
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
    return df


def data_manifest(df: pd.DataFrame, market: str) -> dict:
    dups = int(df["timestamp"].duplicated().sum())
    diffs = df["timestamp"].diff().dt.total_seconds().dropna()
    big_gaps = int((diffs > 120).sum())
    max_gap_min = float(diffs.max() / 60.0) if len(diffs) else 0.0
    return {
        "market": market,
        "rows": int(len(df)),
        "start": str(df["timestamp"].iloc[0]),
        "end": str(df["timestamp"].iloc[-1]),
        "duplicate_timestamps": dups,
        "gaps_gt_2min": big_gaps,
        "max_gap_minutes": round(max_gap_min, 1),
        "missing_ohlcv": int(df[["open", "high", "low", "close"]].isna().sum().sum()),
        "zero_volume_rows": int((df["volume"] == 0).sum()) if "volume" in df else None,
    }


def compute_norm(df: pd.DataFrame, method: str) -> pd.Series:
    """Pre-registered normalizations; information up to and including bar t only."""
    close = df["close"]
    sma = close.rolling(W, min_periods=W).mean()
    if method == "N1":
        std = close.rolling(W, min_periods=W).std()
        return (close - sma) / std
    if method == "N2":
        prev_close = close.shift(1)
        tr = pd.concat(
            [(df["high"] - df["low"]),
             (df["high"] - prev_close).abs(),
             (df["low"] - prev_close).abs()],
            axis=1,
        ).max(axis=1)
        atr = tr.rolling(W, min_periods=W).mean()
        return (close - sma) / atr
    if method == "N3":
        ret1 = close.pct_change()
        sigma = ret1.rolling(W, min_periods=W).std()
        wbar = close / close.shift(W) - 1.0
        return wbar / (sigma * np.sqrt(W))
    raise ValueError(method)


def partitions(n: int) -> dict:
    return {
        "TRAIN": (0, int(n * TRAIN_END)),
        "VALIDATION": (int(n * TRAIN_END), int(n * VAL_END)),
        "TEST": (int(n * VAL_END), n),
    }


def extract_events(norm: np.ndarray, direction: str, thresh: float,
                   part: tuple, signed: bool = False) -> np.ndarray:
    """Pre-registered extraction: threshold + same-direction separation S.
    signed=True uses thresh directly (DOWN: norm<=thresh; UP: norm>=thresh)."""
    start, end = part
    lo = start + W           # warm-up
    hi = end - H             # forward horizon within partition
    if hi <= lo:
        return np.array([], dtype=np.int64)
    if direction == "DOWN":
        mask = norm <= (thresh if signed else -thresh)
    else:
        mask = norm >= (thresh if signed else +thresh)
    idxs = np.flatnonzero(mask)
    idxs = idxs[(idxs >= lo) & (idxs < hi)]
    kept, last = [], -10**9
    for i in idxs:
        if i - last >= S_SEP:
            kept.append(int(i))
            last = i
    return np.array(kept, dtype=np.int64)


def outcomes_bulk(df: pd.DataFrame, idxs: np.ndarray, h: int,
                  direction: str) -> dict:
    """Vectorized outcomes for a batch of event indices (bars t+1..t+h)."""
    n = len(idxs)
    close = df["close"].to_numpy()
    high = df["high"].to_numpy()
    low = df["low"].to_numpy()
    if n == 0:
        return {"ret": np.array([]), "adverse": np.array([]),
                "favorable": np.array([]), "rec_ratio": np.array([]),
                "rec_time": np.array([]), "retention": np.array([])}
    c0 = close[idxs]
    fwd = idxs[:, None] + np.arange(1, h + 1)[None, :]
    cseg, hseg, lseg = close[fwd], high[fwd], low[fwd]
    ret = cseg[:, -1] / c0 - 1.0
    if direction == "DOWN":
        adverse = (c0 - lseg.min(axis=1)) / c0
        favorable = (hseg.max(axis=1) - c0) / c0
    else:
        adverse = (hseg.max(axis=1) - c0) / c0
        favorable = (c0 - lseg.min(axis=1)) / c0
    denom = favorable + adverse
    rec_ratio = np.where(denom > 0, favorable / np.where(denom > 0, denom, 1.0), np.nan)
    above = cseg > c0[:, None]
    rec_time = np.argmax(above, axis=1) + 1
    rec_time[~above.any(axis=1)] = h + 1
    retention = above.mean(axis=1)
    return {"ret": ret, "adverse": adverse, "favorable": favorable,
            "rec_ratio": rec_ratio, "rec_time": rec_time.astype(int),
            "retention": retention}


def bootstrap_ci(values: np.ndarray, b: int = B_BOOT, seed: int = SEED) -> tuple:
    if len(values) == 0:
        return (np.nan, np.nan)
    # Tractability bound: resample from a seeded subsample when the population
    # is very large (documented implementation detail; does not change the
    # estimator, only its Monte-Carlo noise).
    if len(values) > 20000:
        r0 = np.random.default_rng(seed + 777)
        values = r0.choice(values, size=20000, replace=False)
    r = np.random.default_rng(seed)
    idx = r.integers(0, len(values), size=(b, len(values)))
    means = values[idx].mean(axis=1)
    return (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


def perm_pvalue_2s(x: np.ndarray, y: np.ndarray,
                   b: int = B_BOOT, seed: int = SEED) -> float:
    """Two-sided permutation p-value for difference of means (mean(x) - mean(y)).
    y is size-capped at 10,000 (seeded, replace=False) for tractability."""
    n, m = len(x), len(y)
    if n == 0 or m == 0:
        return float("nan")
    if m > 10000:
        rc = np.random.default_rng(seed + 999)
        y = rc.choice(y, size=10000, replace=False)
        m = 10000
    obs = float(x.mean() - y.mean())
    r = np.random.default_rng(seed)
    xy = np.concatenate([x, y])
    d = np.empty(b)
    for k in range(b):
        r.shuffle(xy)
        d[k] = xy[:n].mean() - xy[n:].mean()
    return float((1.0 + np.sum(np.abs(d) >= abs(obs))) / (1.0 + b))


def holm(pvals: list) -> list:
    """Holm-Bonferroni adjusted p-values (FWER control)."""
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        v = min(1.0, (m - rank) * pvals[idx])
        running = max(running, v)
        adj[idx] = running
    return [float(a) for a in adj]


def baseline_diradj(df: pd.DataFrame, part: tuple, direction: str) -> np.ndarray:
    start, end = part
    hi = end - H
    if hi <= start:
        return np.array([])
    close = df["close"].to_numpy()
    j = np.arange(start, hi)
    ret = (close[j + H] / close[j]) - 1.0
    return ret if direction == "DOWN" else -ret


def pool_diradj(df: pd.DataFrame, part: tuple) -> np.ndarray:
    return np.concatenate([baseline_diradj(df, part, "DOWN"),
                           baseline_diradj(df, part, "UP")])


def diradj(rets: np.ndarray, direction: str) -> np.ndarray:
    return rets if direction == "DOWN" else -rets


def count_cross_overlap(times: pd.Series, dirs: np.ndarray, h_min: int) -> int:
    t = times.values.astype("int64") // 10**9
    order = np.argsort(t)
    ts, ds = t[order], dirs[order]
    win = h_min * 60
    total = 0
    for i in range(len(ts)):
        lo = int(np.searchsorted(ts, ts[i] - win, side="left"))
        hi = int(np.searchsorted(ts, ts[i] + win, side="right"))
        if hi - lo > 0:
            total += int((ds[lo:hi] != ds[i]).sum())
    return total // 2


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    manifest_rows, event_rows = [], []
    norm_rows, cross_rows, wf_rows = [], [], []
    regime_rows, chrono_rows, persist_rows, thresh_rows = [], [], [], []
    overlap_rows = []
    versions = {"pandas": pd.__version__, "numpy": np.__version__}
    fingerprints = {}

    # Confirmatory inputs per market, aggregated at the end.
    pooled_ev, pooled_base = {}, {}
    dir_ev, dir_base = {}, {}
    pers_ev = {}
    permarket_ev, permarket_base = {}, {}

    for norm in NORMALIZATIONS:
        pooled_ev[norm], pooled_base[norm] = [], []
        pers_ev[norm] = {"pass": [], "fail": []}
        for direction in ["DOWN", "UP"]:
            dir_ev[(norm, direction)], dir_base[(norm, direction)] = [], []
        for market in MARKETS:
            permarket_ev[(norm, market)], permarket_base[(norm, market)] = [], []

    for market in MARKETS:
        print(f"[{market}] loading…", flush=True)
        df = load_market(market)
        fingerprints[market] = sha256(DATA / f"{market}_M1.csv")
        manifest_rows.append(data_manifest(df, market))
        n_total = len(df)
        parts = partitions(n_total)
        ret1 = df["close"].pct_change()
        vol = ret1.rolling(W, min_periods=W).std().to_numpy()
        tr_vol = vol[parts["TRAIN"][0]: parts["TRAIN"][1]]
        tr_vol = tr_vol[~np.isnan(tr_vol)]
        q33, q66 = float(np.quantile(tr_vol, 1 / 3)), float(np.quantile(tr_vol, 2 / 3))
        third_edges = [int(n_total * k / 3) for k in range(4)]
        mom = df["close"].pct_change(M_MOM).to_numpy() * 100.0
        tr_mom = mom[parts["TRAIN"][0]: parts["TRAIN"][1]]
        tr_mom = tr_mom[~np.isnan(tr_mom)]
        p25, p75 = float(np.quantile(tr_mom, 0.25)), float(np.quantile(tr_mom, 0.75))
        times = df["timestamp"]
        close = df["close"].to_numpy()

        for norm in NORMALIZATIONS:
            print(f"[{market}] normalization {norm}…", flush=True)
            ns = compute_norm(df, norm).to_numpy()

            # Pre-extract primary events per (direction, partition)
            ev_primary = {(d, p): extract_events(ns, d, THRESH_PRIMARY, parts[p])
                          for d in ["DOWN", "UP"] for p in parts}

            # ---- Event dataset rows (primary threshold, all partitions) ----
            for direction in ["DOWN", "UP"]:
                for part_name in ["TRAIN", "VALIDATION", "TEST"]:
                    ev = ev_primary[(direction, part_name)]
                    if len(ev) == 0:
                        continue
                    o = outcomes_bulk(df, ev, H, direction)
                    o60 = outcomes_bulk(df, ev, PERSIST_H, direction)
                    momv = mom[ev]
                    cls = np.full(len(ev), None, dtype=object)
                    if direction == "DOWN":
                        cls = np.where(momv <= p25, "D+P", "D")
                    else:
                        cls = np.where(momv >= p75, "D+P", "D")
                    v = vol[ev]
                    vreg = np.where(v < q33, "LOW", np.where(v >= q66, "HIGH", "MID"))
                    chrono = np.digitize(ev, third_edges[1:-1], right=False)  # 0,1,2
                    dret = diradj(o["ret"], direction)
                    for k in range(len(ev)):
                        i = int(ev[k])
                        event_rows.append({
                            "instrument": market, "timeframe": "M1",
                            "normalization": norm, "direction": direction,
                            "partition": part_name,
                            "event_timestamp": str(times.iloc[i]),
                            "event_definition_version": "V2.0.0",
                            "norm_value": round(float(ns[i]), 4),
                            "threshold": THRESH_PRIMARY,
                            "momentum_pct": round(float(momv[k]), 3) if not np.isnan(momv[k]) else None,
                            "candidate_class": str(cls[k]),
                            "vol_regime": str(vreg[k]),
                            "chrono_third": int(chrono[k]),
                            "volatility_at_event": round(float(v[k]), 8) if not np.isnan(v[k]) else None,
                            "mae_h120": round(float(o["adverse"][k]), 5),
                            "mfe_h120": round(float(o["favorable"][k]), 5),
                            "recovery_ratio_h120": round(float(o["rec_ratio"][k]), 4)
                            if not np.isnan(o["rec_ratio"][k]) else None,
                            "recovery_time_h120": int(o["rec_time"][k]),
                            "retention_h120": round(float(o["retention"][k]), 4),
                            "retention_h60": round(float(o60["retention"][k]), 4),
                            "persistence_pass": bool(o60["retention"][k] >= PERSIST_Q),
                            "event_return_h120": round(float(o["ret"][k]), 5),
                            "dir_adj_return_h120": round(float(dret[k]), 5),
                        })

            # ---- Primary descriptive results per direction per partition ----
            for direction in ["DOWN", "UP"]:
                for part_name, part in parts.items():
                    ev = ev_primary[(direction, part_name)]
                    o = outcomes_bulk(df, ev, H, direction)
                    dret = diradj(o["ret"], direction)
                    base = baseline_diradj(df, part, direction)
                    ci = bootstrap_ci(dret)
                    if len(dret) and len(base):
                        r = np.random.default_rng(SEED + len(dret) + (7 if direction == "UP" else 0))
                        sample = r.choice(base, size=len(dret), replace=False)
                        diff = float(dret.mean() - sample.mean())
                        diff_ci = bootstrap_ci(dret - r.choice(base, size=len(dret), replace=False))
                    else:
                        diff, diff_ci = np.nan, (np.nan, np.nan)
                    norm_rows.append({
                        "normalization": norm, "instrument": market,
                        "direction": direction, "partition": part_name,
                        "threshold": THRESH_PRIMARY,
                        "event_count": int(len(dret)),
                        "mean_dir_adj_return": round(float(dret.mean()), 5) if len(dret) else None,
                        "median_dir_adj_return": round(float(np.median(dret)), 5) if len(dret) else None,
                        "ci95_low": round(ci[0], 5) if len(dret) else None,
                        "ci95_high": round(ci[1], 5) if len(dret) else None,
                        "baseline_mean": round(float(base.mean()), 5) if len(base) else None,
                        "diff_vs_baseline": round(diff, 5) if len(dret) and len(base) else None,
                        "diff_ci95_low": round(diff_ci[0], 5) if len(dret) and len(base) else None,
                        "diff_ci95_high": round(diff_ci[1], 5) if len(dret) and len(base) else None,
                    })

            # ---- Confirmatory inputs (VALIDATION) ----
            vpart = parts["VALIDATION"]
            base_pool = pool_diradj(df, vpart)
            ev_pool = []
            for direction in ["DOWN", "UP"]:
                ev = ev_primary[(direction, "VALIDATION")]
                o = outcomes_bulk(df, ev, H, direction)
                o60 = outcomes_bulk(df, ev, PERSIST_H, direction)
                dret = diradj(o["ret"], direction)
                ev_pool.append(dret)
                dir_ev[(norm, direction)].append(dret)
                dir_base[(norm, direction)].append(baseline_diradj(df, vpart, direction))
                pers_ev[norm]["pass"].append(dret[o60["retention"] >= PERSIST_Q])
                pers_ev[norm]["fail"].append(dret[o60["retention"] < PERSIST_Q])
            ev_pool = np.concatenate(ev_pool) if ev_pool else np.array([])
            pooled_ev[norm].append(ev_pool)
            pooled_base[norm].append(base_pool)
            permarket_ev[(norm, market)].append(ev_pool)
            permarket_base[(norm, market)].append(base_pool)

            # ---- Cross-market descriptive (VALIDATION + TEST, per direction) ----
            for direction in ["DOWN", "UP"]:
                for part_name in ["VALIDATION", "TEST"]:
                    ev = ev_primary[(direction, part_name)]
                    o = outcomes_bulk(df, ev, H, direction)
                    dret = diradj(o["ret"], direction)
                    ci = bootstrap_ci(dret)
                    cross_rows.append({
                        "normalization": norm, "instrument": market,
                        "direction": direction, "partition": part_name,
                        "event_count": int(len(dret)),
                        "mean_dir_adj_return": round(float(dret.mean()), 5) if len(dret) else None,
                        "ci95_low": round(ci[0], 5) if len(dret) else None,
                        "ci95_high": round(ci[1], 5) if len(dret) else None,
                    })

            # ---- Walk-forward folds ----
            for fold_name, _t0, _t1, e0, e1 in FOLDS:
                ev_part = (int(n_total * e0), int(n_total * e1))
                for direction in ["DOWN", "UP"]:
                    ev = extract_events(ns, direction, THRESH_PRIMARY, ev_part)
                    o = outcomes_bulk(df, ev, H, direction)
                    dret = diradj(o["ret"], direction)
                    ci = bootstrap_ci(dret)
                    wf_rows.append({
                        "normalization": norm, "instrument": market,
                        "fold": fold_name, "direction": direction,
                        "eval_window": f"[{e0:.2f},{e1:.2f})",
                        "event_count": int(len(dret)),
                        "mean_dir_adj_return": round(float(dret.mean()), 5) if len(dret) else None,
                        "ci95_low": round(ci[0], 5) if len(dret) else None,
                        "ci95_high": round(ci[1], 5) if len(dret) else None,
                    })

            # ---- Regime: volatility terciles (VALIDATION + TEST) ----
            for direction in ["DOWN", "UP"]:
                for part_name in ["VALIDATION", "TEST"]:
                    ev = ev_primary[(direction, part_name)]
                    v = vol[ev]
                    o = outcomes_bulk(df, ev, H, direction)
                    dret = diradj(o["ret"], direction)
                    for rname, lo_q, hi_q in [("LOW", -np.inf, q33),
                                              ("MID", q33, q66),
                                              ("HIGH", q66, np.inf)]:
                        m = ~np.isnan(v) & (v >= lo_q) & (v < hi_q)
                        sub = dret[m]
                        ci = bootstrap_ci(sub)
                        regime_rows.append({
                            "normalization": norm, "instrument": market,
                            "direction": direction, "partition": part_name,
                            "vol_regime": rname,
                            "event_count": int(len(sub)),
                            "mean_dir_adj_return": round(float(sub.mean()), 5) if len(sub) else None,
                            "ci95_low": round(ci[0], 5) if len(sub) else None,
                            "ci95_high": round(ci[1], 5) if len(sub) else None,
                        })

            # ---- Chronological thirds: primary event definition restricted to
            # each third (stability of the event definition across calendar
            # periods; same S-separation as the primary definition) ----
            for direction in ["DOWN", "UP"]:
                for k in range(3):
                    lo_i = max(third_edges[k], W)
                    hi_i = min(third_edges[k + 1], n_total)
                    if hi_i <= lo_i + H:
                        continue
                    idxs = extract_events(ns, direction, THRESH_PRIMARY, (lo_i, hi_i))
                    o = outcomes_bulk(df, idxs, H, direction)
                    dret = diradj(o["ret"], direction)
                    ci = bootstrap_ci(dret)
                    chrono_rows.append({
                        "normalization": norm, "instrument": market,
                        "direction": direction, "chrono_third": k,
                        "event_count": int(len(dret)),
                        "mean_dir_adj_return": round(float(dret.mean()), 5) if len(dret) else None,
                        "ci95_low": round(ci[0], 5) if len(dret) else None,
                        "ci95_high": round(ci[1], 5) if len(dret) else None,
                    })

            # ---- Persistence table (all partitions) ----
            for direction in ["DOWN", "UP"]:
                for part_name, part in parts.items():
                    ev = ev_primary[(direction, part_name)]
                    o = outcomes_bulk(df, ev, H, direction)
                    o60 = outcomes_bulk(df, ev, PERSIST_H, direction)
                    dret = diradj(o["ret"], direction)
                    pflag = o60["retention"] >= PERSIST_Q
                    for flag, label in [(True, True), (False, False)]:
                        sub = dret[pflag == flag]
                        ci = bootstrap_ci(sub)
                        persist_rows.append({
                            "normalization": norm, "instrument": market,
                            "direction": direction, "partition": part_name,
                            "persistence_pass": label,
                            "event_count": int(len(sub)),
                            "mean_dir_adj_return": round(float(sub.mean()), 5) if len(sub) else None,
                            "ci95_low": round(ci[0], 5) if len(sub) else None,
                            "ci95_high": round(ci[1], 5) if len(sub) else None,
                        })

            # ---- Threshold grid (TRAIN only, exploratory) ----
            for th in THRESH_GRID:
                for direction in ["DOWN", "UP"]:
                    ev = extract_events(ns, direction, th, parts["TRAIN"])
                    o = outcomes_bulk(df, ev, H, direction)
                    dret = diradj(o["ret"], direction)
                    ci = bootstrap_ci(dret)
                    thresh_rows.append({
                        "normalization": norm, "instrument": market,
                        "direction": direction, "threshold": th, "grid": "TRAIN",
                        "event_count": int(len(dret)),
                        "mean_dir_adj_return": round(float(dret.mean()), 5) if len(dret) else None,
                        "ci95_low": round(ci[0], 5) if len(dret) else None,
                        "ci95_high": round(ci[1], 5) if len(dret) else None,
                    })

            # ---- Matched-quantile comparability check (exploratory, VALIDATION) ----
            tr_ns = ns[parts["TRAIN"][0]: parts["TRAIN"][1]]
            tr_ns = tr_ns[~np.isnan(tr_ns)]
            qlo, qhi = float(np.quantile(tr_ns, QUANT_MATCH)), float(np.quantile(tr_ns, 1 - QUANT_MATCH))
            for direction, th in [("DOWN", qlo), ("UP", qhi)]:
                ev = extract_events(ns, direction, th, parts["VALIDATION"], signed=True)
                o = outcomes_bulk(df, ev, H, direction)
                dret = diradj(o["ret"], direction)
                ci = bootstrap_ci(dret)
                thresh_rows.append({
                    "normalization": norm, "instrument": market,
                    "direction": direction, "threshold": round(th, 3),
                    "grid": "MATCHED_Q",
                    "event_count": int(len(dret)),
                    "mean_dir_adj_return": round(float(dret.mean()), 5) if len(dret) else None,
                    "ci95_low": round(ci[0], 5) if len(dret) else None,
                    "ci95_high": round(ci[1], 5) if len(dret) else None,
                })

            # ---- Cross-direction overlap (vectorized) ----
            sub_rows = [r for r in event_rows
                        if r["normalization"] == norm and r["instrument"] == market]
            if sub_rows:
                sub_t = pd.to_datetime([r["event_timestamp"] for r in sub_rows])
                sub_d = np.array([1 if r["direction"] == "DOWN" else 0 for r in sub_rows])
                pairs = count_cross_overlap(sub_t, sub_d, H)
                overlap_rows.append({
                    "normalization": norm, "instrument": market,
                    "total_events": len(sub_rows),
                    "cross_direction_pairs_within_H": pairs,
                })

        print(f"[{market}] done.", flush=True)

    # ================= Confirmatory family (27 pre-registered tests) ==========
    confirm_rows = []

    # 1) pooled effect per normalization (3)
    for norm in NORMALIZATIONS:
        x = np.concatenate([a for a in pooled_ev[norm] if len(a)])
        y = np.concatenate([a for a in pooled_base[norm] if len(a)])
        if len(x) and len(y):
            diff = float(x.mean() - y.mean())
            pval = perm_pvalue_2s(x, y)
        else:
            diff, pval = np.nan, np.nan
        confirm_rows.append({
            "test_id": f"{norm}_pooled", "family": "pooled_effect",
            "normalization": norm, "market": "ALL", "direction": "BOTH",
            "n_events": int(len(x)),
            "effect": round(diff, 5) if not np.isnan(diff) else None,
            "p_value_raw": round(pval, 5) if not np.isnan(pval) else None,
        })

    # 2) direction-resolved per normalization (6)
    for norm in NORMALIZATIONS:
        for direction in ["DOWN", "UP"]:
            x = np.concatenate([a for a in dir_ev[(norm, direction)] if len(a)])
            y = np.concatenate([a for a in dir_base[(norm, direction)] if len(a)])
            if len(x) and len(y):
                diff = float(x.mean() - y.mean())
                pval = perm_pvalue_2s(x, y)
            else:
                diff, pval = np.nan, np.nan
            confirm_rows.append({
                "test_id": f"{norm}_{direction}", "family": "direction_effect",
                "normalization": norm, "market": "ALL", "direction": direction,
                "n_events": int(len(x)),
                "effect": round(diff, 5) if not np.isnan(diff) else None,
                "p_value_raw": round(pval, 5) if not np.isnan(pval) else None,
            })

    # 3) persistence P-pass vs P-fail per normalization (3)
    for norm in NORMALIZATIONS:
        x = np.concatenate([a for a in pers_ev[norm]["pass"] if len(a)])
        y = np.concatenate([a for a in pers_ev[norm]["fail"] if len(a)])
        if len(x) and len(y):
            diff = float(x.mean() - y.mean())
            pval = perm_pvalue_2s(x, y)
        else:
            diff, pval = np.nan, np.nan
        confirm_rows.append({
            "test_id": f"{norm}_persist", "family": "persistence",
            "normalization": norm, "market": "ALL", "direction": "BOTH",
            "n_events": int(len(x) + len(y)),
            "effect": round(diff, 5) if not np.isnan(diff) else None,
            "p_value_raw": round(pval, 5) if not np.isnan(pval) else None,
        })

    # 4) per-market pooled per normalization (15)
    for norm in NORMALIZATIONS:
        for market in MARKETS:
            x = np.concatenate([a for a in permarket_ev[(norm, market)] if len(a)])
            y = np.concatenate([a for a in permarket_base[(norm, market)] if len(a)])
            if len(x) and len(y):
                diff = float(x.mean() - y.mean())
                pval = perm_pvalue_2s(x, y)
            else:
                diff, pval = np.nan, np.nan
            confirm_rows.append({
                "test_id": f"{norm}_{market}", "family": "cross_market",
                "normalization": norm, "market": market, "direction": "BOTH",
                "n_events": int(len(x)),
                "effect": round(diff, 5) if not np.isnan(diff) else None,
                "p_value_raw": round(pval, 5) if not np.isnan(pval) else None,
            })

    conf = pd.DataFrame(confirm_rows)
    pvals = conf["p_value_raw"].fillna(1.0).to_list()
    conf["p_holm"] = [round(v, 5) for v in holm(pvals)]
    conf["holm_significant"] = conf["p_holm"] < ALPHA

    # ---- Write outputs ----
    pd.DataFrame(manifest_rows).to_csv(OUT / "data_manifest_V2.csv", index=False)
    pd.DataFrame(event_rows).to_csv(OUT / "event_dataset_V2.csv", index=False)
    conf.to_csv(OUT / "results_confirmatory_V2.csv", index=False)
    pd.DataFrame(norm_rows).to_csv(OUT / "results_normalization_V2.csv", index=False)
    pd.DataFrame(cross_rows).to_csv(OUT / "results_crossmarket_V2.csv", index=False)
    pd.DataFrame(wf_rows).to_csv(OUT / "results_walkforward_V2.csv", index=False)
    pd.DataFrame(regime_rows).to_csv(OUT / "results_regime_V2.csv", index=False)
    pd.DataFrame(chrono_rows).to_csv(OUT / "results_chrono_V2.csv", index=False)
    pd.DataFrame(persist_rows).to_csv(OUT / "results_persistence_V2.csv", index=False)
    pd.DataFrame(thresh_rows).to_csv(OUT / "results_threshold_V2.csv", index=False)
    pd.DataFrame(overlap_rows).to_csv(OUT / "overlap_report_V2.csv", index=False)

    report = {
        "protocol_version": "V2.0.0",
        "normalization_definitions": NORM_DEFS,
        "seeds": {"bootstrap": SEED, "permutation": SEED},
        "parameters": {"W": W, "threshold_primary": THRESH_PRIMARY,
                       "threshold_grid": THRESH_GRID, "matched_quantile": QUANT_MATCH,
                       "S_sep": S_SEP, "H": H, "persist_h": PERSIST_H,
                       "persist_q": PERSIST_Q, "alpha": ALPHA, "b_boot": B_BOOT,
                       "partitions": {"TRAIN": TRAIN_END, "VALIDATION": VAL_END},
                       "folds": [list(f) for f in FOLDS],
                       "confirmatory_family_size": len(conf)},
        "dataset_fingerprints_sha256": fingerprints,
        "library_versions": versions,
        "event_dataset_rows": len(event_rows),
        "event_dataset_sha256": hashlib.sha256(
            pd.DataFrame(event_rows).to_csv(index=False).encode("utf-8")).hexdigest(),
    }
    (OUT / "experiment_metadata_V2.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("Wrote outputs to", OUT)


if __name__ == "__main__":
    main()
