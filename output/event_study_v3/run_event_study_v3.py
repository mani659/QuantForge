"""
QuantForge — Canonical Mean-Reversion Event Study V3 (XAGUSD confirmation)
Implements EVENT_STUDY_PROTOCOL_V3.md exactly. Research artifact; not production code.
Deterministic (fixed seeds). Outputs written to output/event_study_v3/.

Cluster bootstrap: clusters are connected components of the window-overlap
graph over ALL events (both directions) in the analysis window; a resample
draws clusters and pools the *included* (direction-selected) events within
them, preserving cross-direction dependence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
DATA = Path(__file__).resolve().parents[2] / "data" / "m1"

# ---- Pre-registered protocol parameters (V3.0.0) ----
W = 120
H = 120
K = 60                 # confirmation point (bars after event)
S_SEP = 240
THRESH_PRIMARY = 3.0
NEIGHBORHOOD = [2.5, 3.0, 3.5]
PERSIST_Q = 0.6
QUANT_MATCH = 0.005
TRAIN_END, VAL_END = 0.70, 0.85
B_BOOT = 2000
SEED = 20260814
LEAD = "XAGUSD"
CONTROL = "EURUSD"
NORMALIZATIONS = ["N1", "N2", "N3"]
COST_BANDS_BP = [0, 5, 10, 20, 30]
FOLDS = [
    ("A", 0.40, 0.50),
    ("B", 0.50, 0.60),
    ("C", 0.60, 0.70),
    ("D", 0.70, 0.85),  # == V1/V2 VALIDATION window
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
    return df.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)


def data_manifest(df: pd.DataFrame, market: str) -> dict:
    dups = int(df["timestamp"].duplicated().sum())
    diffs = df["timestamp"].diff().dt.total_seconds().dropna()
    return {
        "market": market,
        "rows": int(len(df)),
        "start": str(df["timestamp"].iloc[0]),
        "end": str(df["timestamp"].iloc[-1]),
        "duplicate_timestamps": dups,
        "gaps_gt_2min": int((diffs > 120).sum()),
        "missing_ohlcv": int(df[["open", "high", "low", "close"]].isna().sum().sum()),
        "zero_volume_rows": int((df["volume"] == 0).sum()),
    }


def compute_norm(df: pd.DataFrame, method: str) -> np.ndarray:
    close = df["close"]
    sma = close.rolling(W, min_periods=W).mean()
    if method == "N1":
        std = close.rolling(W, min_periods=W).std()
        return ((close - sma) / std).to_numpy()
    if method == "N2":
        prev_close = close.shift(1)
        tr = pd.concat([(df["high"] - df["low"]),
                        (df["high"] - prev_close).abs(),
                        (df["low"] - prev_close).abs()], axis=1).max(axis=1)
        atr = tr.rolling(W, min_periods=W).mean()
        return ((close - sma) / atr).to_numpy()
    if method == "N3":
        ret1 = close.pct_change()
        sigma = ret1.rolling(W, min_periods=W).std()
        wbar = close / close.shift(W) - 1.0
        return (wbar / (sigma * np.sqrt(W))).to_numpy()
    raise ValueError(method)


def partitions(n: int) -> dict:
    return {"TRAIN": (0, int(n * TRAIN_END)),
            "VALIDATION": (int(n * TRAIN_END), int(n * VAL_END)),
            "TEST": (int(n * VAL_END), n)}


def extract_events(norm: np.ndarray, direction: str, thresh: float,
                   part: tuple, signed: bool = False) -> np.ndarray:
    start, end = part
    lo = start + W
    hi = end - H
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
                  direction: str, offset: int = 0) -> dict:
    n = len(idxs)
    close = df["close"].to_numpy()
    high = df["high"].to_numpy()
    low = df["low"].to_numpy()
    if n == 0:
        return {"ret": np.array([]), "adverse": np.array([]),
                "favorable": np.array([]), "rec_ratio": np.array([]),
                "rec_time": np.array([]), "retention": np.array([])}
    c0 = close[idxs + offset]
    fwd = (idxs + offset)[:, None] + np.arange(1, h + 1)[None, :]
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
    return {"ret": ret, "adverse": adverse, "favorable": favorable,
            "rec_ratio": rec_ratio, "rec_time": rec_time.astype(int),
            "retention": above.mean(axis=1)}


def make_clusters(idxs: np.ndarray, h: int) -> np.ndarray:
    """Connected components of the window-overlap graph (|i-j| < h).
    Events are clustered across BOTH directions."""
    if len(idxs) == 0:
        return np.array([], dtype=int)
    s = np.sort(idxs)
    labels = np.empty(len(s), dtype=int)
    cur, last_end = 0, -10**9
    for k, i in enumerate(s):
        if i < last_end:
            labels[k] = cur
            last_end = max(last_end, i + h)
        else:
            cur += 1
            labels[k] = cur
            last_end = i + h
    order = np.argsort(idxs)
    out = np.empty(len(idxs), dtype=int)
    out[order] = labels
    return out


def cluster_boot(rets_all: np.ndarray, cids_all: np.ndarray, include: np.ndarray,
                 b: int = B_BOOT, seed: int = SEED) -> tuple:
    """Cluster bootstrap over the FULL event set; `include` selects the events
    entering the statistic (preserves cross-direction dependence)."""
    if include.sum() == 0:
        return (np.nan, (np.nan, np.nan), np.nan)
    uniq = np.unique(cids_all)
    cs = np.array([rets_all[(cids_all == c) & include].sum() for c in uniq])
    cc = np.array([((cids_all == c) & include).sum() for c in uniq])
    n_c = len(uniq)
    r = np.random.default_rng(seed)
    draw = r.integers(0, n_c, size=(b, n_c))
    S = cs[draw].sum(axis=1)
    N = cc[draw].sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        means = S / N
    means = means[~np.isnan(means)]
    obs = float(rets_all[include].mean())
    if len(means) == 0:
        return obs, (np.nan, np.nan), np.nan
    ci = (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))
    centered = means - obs
    p = float((1.0 + np.sum(np.abs(centered) >= abs(obs))) / (1.0 + len(means)))
    return obs, ci, p


def cluster_boot_2g(rets_all: np.ndarray, cids_all: np.ndarray,
                    flags: np.ndarray, b: int = B_BOOT, seed: int = SEED) -> tuple:
    if (flags == 1).sum() == 0 or (flags == 0).sum() == 0:
        return (np.nan, (np.nan, np.nan), np.nan, 0)
    uniq = np.unique(cids_all)
    cs = np.array([rets_all[(cids_all == c) & (flags == 1)].sum() for c in uniq])
    cc = np.array([((cids_all == c) & (flags == 1)).sum() for c in uniq])
    us = np.array([rets_all[(cids_all == c) & (flags == 0)].sum() for c in uniq])
    uc = np.array([((cids_all == c) & (flags == 0)).sum() for c in uniq])
    n_c = len(uniq)
    r = np.random.default_rng(seed)
    draw = r.integers(0, n_c, size=(b, n_c))
    with np.errstate(invalid="ignore", divide="ignore"):
        cm = cs[draw].sum(axis=1) / cc[draw].sum(axis=1)
        um = us[draw].sum(axis=1) / uc[draw].sum(axis=1)
    d = (cm - um)[~np.isnan(cm - um)]
    obs = float(rets_all[flags == 1].mean() - rets_all[flags == 0].mean())
    if len(d) == 0:
        return obs, (np.nan, np.nan), np.nan, 0
    ci = (float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)))
    centered = d - obs
    p = float((1.0 + np.sum(np.abs(centered) >= abs(obs))) / (1.0 + len(d)))
    return obs, ci, p, int(len(d))


def holm(pvals: list) -> list:
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        v = min(1.0, (m - rank) * pvals[idx])
        running = max(running, v)
        adj[idx] = running
    return [float(a) for a in adj]


def serial_corr(rets: np.ndarray, idxs: np.ndarray) -> float:
    if len(rets) < 3:
        return np.nan
    o = np.argsort(idxs)
    x = rets[o]
    x = x - x.mean()
    denom = (x * x).sum()
    return float((x[:-1] * x[1:]).sum() / denom) if denom > 0 else np.nan


def event_set(df: pd.DataFrame, ns: np.ndarray, direction: str, thresh: float,
              part: tuple, signed: bool = False) -> tuple:
    """Extract events for both directions in a window and return
    (ev_all, cids_all, rets_all, n_down) where rets_all are direction-adjusted
    H-bar returns for all events (DOWN block first, then UP block)."""
    ev_d = extract_events(ns, "DOWN", thresh, part, signed=signed)
    ev_u = extract_events(ns, "UP", thresh, part, signed=signed)
    ev_all = np.concatenate([ev_d, ev_u])
    if len(ev_all) == 0:
        return ev_all, np.array([], dtype=int), np.array([]), len(ev_d)
    cids = make_clusters(ev_all, H)
    rets_d = outcomes_bulk(df, ev_d, H, "DOWN")["ret"]
    rets_u = -outcomes_bulk(df, ev_u, H, "UP")["ret"]
    return ev_all, cids, np.concatenate([rets_d, rets_u]), len(ev_d)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    versions = {"pandas": pd.__version__, "numpy": np.__version__}
    fingerprints, manifest_rows = {}, []
    event_rows = []
    family_rows, dep_rows, cost_rows = [], [], []
    thresh_rows, norm_rows, wf_rows, chrono_rows, holdout_rows = [], [], [], [], []

    frames, norms = {}, {}
    for market in [LEAD, CONTROL]:
        df = load_market(market)
        frames[market] = df
        fingerprints[market] = sha256(DATA / f"{market}_M1.csv")
        manifest_rows.append(data_manifest(df, market))
        norms[market] = {m: compute_norm(df, m) for m in NORMALIZATIONS}
        print(f"[{market}] loaded ({len(df)} rows).", flush=True)

    dfL, dfC = frames[LEAD], frames[CONTROL]
    nL, nC = len(dfL), len(dfC)
    partsL, partsC = partitions(nL), partitions(nC)
    vL, vC, tL = partsL["VALIDATION"], partsC["VALIDATION"], partsL["TEST"]

    # =====================================================================
    # Event dataset + dependence analysis (primary threshold, all partitions)
    # =====================================================================
    for market in [LEAD, CONTROL]:
        df = frames[market]
        close = df["close"].to_numpy()
        n_total = len(df)
        parts = partitions(n_total)
        times = df["timestamp"]
        for norm in NORMALIZATIONS:
            ns = norms[market][norm]
            for direction in ["DOWN", "UP"]:
                for part_name in ["TRAIN", "VALIDATION", "TEST"]:
                    ev = extract_events(ns, direction, THRESH_PRIMARY, parts[part_name])
                    if len(ev) == 0:
                        continue
                    o = outcomes_bulk(df, ev, H, direction)
                    o60 = outcomes_bulk(df, ev, K, direction)
                    ret_confirm = (o60["retention"] if direction == "DOWN"
                                   else 1.0 - o60["retention"])
                    ok_room = ev + K + H <= parts[part_name][1]
                    retK = np.full(len(ev), np.nan)
                    m = ok_room
                    if m.any():
                        c0k = close[ev[m] + K]
                        retK[m] = close[ev[m] + K + H] / c0k - 1.0
                    dret = o["ret"] if direction == "DOWN" else -o["ret"]
                    dretK = np.full(len(ev), np.nan)
                    dretK[m] = retK[m] if direction == "DOWN" else -retK[m]
                    for k in range(len(ev)):
                        i = int(ev[k])
                        event_rows.append({
                            "instrument": market, "timeframe": "M1",
                            "normalization": norm, "direction": direction,
                            "partition": part_name,
                            "event_timestamp": str(times.iloc[i]),
                            "event_definition_version": "V3.0.0",
                            "norm_value": round(float(ns[i]), 4),
                            "threshold": THRESH_PRIMARY,
                            "mae_h120": round(float(o["adverse"][k]), 5),
                            "mfe_h120": round(float(o["favorable"][k]), 5),
                            "recovery_ratio_h120": round(float(o["rec_ratio"][k]), 4)
                            if not np.isnan(o["rec_ratio"][k]) else None,
                            "retention_h120": round(float(o["retention"][k]), 4),
                            "retention_confirm_h60": round(float(ret_confirm[k]), 4),
                            "confirmation_pass": bool(m[k] and ret_confirm[k] >= PERSIST_Q),
                            "dir_adj_return_h120": round(float(dret[k]), 5),
                            "dir_adj_return_post_conf_h120": round(float(dretK[k]), 5)
                            if m[k] else None,
                        })
            # dependence table: true all-events cluster structure (VALIDATION)
            ev_all, cids, _r, n_down = event_set(df, ns, None, THRESH_PRIMARY,
                                                 parts["VALIDATION"])
            for direction, lo_i, hi_i in [("DOWN", 0, n_down), ("UP", n_down, len(ev_all))]:
                if hi_i <= lo_i:
                    continue
                ev = ev_all[lo_i:hi_i]
                rets_dir = _r[lo_i:hi_i]
                cids_dir = cids[lo_i:hi_i]
                uniq = np.unique(cids)
                # cluster sizes as seen by this direction's events
                sizes_seen = np.array([(cids == c).sum() for c in cids_dir])
                mixed = sum(1 for c in np.unique(cids_dir)
                            if ((cids == c) & (np.arange(len(cids)) < n_down)).any()
                            and ((cids == c) & (np.arange(len(cids)) >= n_down)).any())
                dep_rows.append({
                    "instrument": market, "normalization": norm,
                    "direction": direction, "partition": "VALIDATION",
                    "raw_events": int(len(ev)),
                    "all_events_clusters": int(len(uniq)),
                    "mean_cluster_size_seen": round(float(sizes_seen.mean()), 2),
                    "max_cluster_size_seen": int(sizes_seen.max()),
                    "clusters_mixing_directions": int(mixed),
                    "serial_corr_returns": round(serial_corr(rets_dir, ev), 4),
                })

    # =====================================================================
    # Confirmatory family (12 pre-registered tests)
    # =====================================================================
    # F1-F4: lead, primary threshold, VALIDATION, direction-resolved
    for norm in ["N1", "N2"]:
        ns = norms[LEAD][norm]
        ev_all, cids, rets_all, n_down = event_set(dfL, ns, None, THRESH_PRIMARY, vL)
        for direction, lo_i, hi_i in [("DOWN", 0, n_down), ("UP", n_down, len(ev_all))]:
            inc = np.zeros(len(ev_all), dtype=bool)
            inc[lo_i:hi_i] = True
            obs, ci, p = cluster_boot(rets_all, cids, inc)
            fnum = 1 + (0 if norm == "N1" else 2) + (1 if direction == "UP" else 0)
            family_rows.append({
                "test_id": f"F{fnum}", "family": "primary_lead",
                "instrument": LEAD, "normalization": norm, "direction": direction,
                "partition": "VALIDATION", "n_events": int(inc.sum()),
                "effect": round(obs, 5), "ci95_low": round(ci[0], 5),
                "ci95_high": round(ci[1], 5), "p_value_raw": round(p, 5),
                "expected_sign": "+",
            })

    # F5-F8: entry-at-confirmation, VALIDATION
    for idx, norm in enumerate(["N1", "N2"]):
        ns = norms[LEAD][norm]
        ev_all_c, rets_all_c, flags_c = [], [], []
        for direction in ["DOWN", "UP"]:
            ev = extract_events(ns, direction, THRESH_PRIMARY, vL)
            ev = ev[ev + K + H <= vL[1]]
            if len(ev) == 0:
                continue
            oK = outcomes_bulk(dfL, ev, H, direction, offset=K)
            oK60 = outcomes_bulk(dfL, ev, K, direction)
            ret_confirm = (oK60["retention"] if direction == "DOWN"
                           else 1.0 - oK60["retention"])
            dretK = oK["ret"] if direction == "DOWN" else -oK["ret"]
            ev_all_c.append(ev)
            rets_all_c.append(dretK)
            flags_c.append(ret_confirm >= PERSIST_Q)
        if not ev_all_c:
            continue
        ev_all_c = np.concatenate(ev_all_c)
        rets_all_c = np.concatenate(rets_all_c)
        flags_c = np.concatenate(flags_c)
        cids_all_c = make_clusters(ev_all_c, H)
        obs, ci, p = cluster_boot(rets_all_c, cids_all_c, flags_c)
        family_rows.append({
            "test_id": f"F{5 + 2 * idx}", "family": "confirmation_entry",
            "instrument": LEAD, "normalization": norm, "direction": "BOTH",
            "partition": "VALIDATION", "n_events": int(flags_c.sum()),
            "effect": round(obs, 5), "ci95_low": round(ci[0], 5),
            "ci95_high": round(ci[1], 5), "p_value_raw": round(p, 5),
            "expected_sign": "+",
        })
        obs2, ci2, p2, b_eff = cluster_boot_2g(rets_all_c, cids_all_c, flags_c.astype(int))
        family_rows.append({
            "test_id": f"F{6 + 2 * idx}", "family": "confirmation_discrimination",
            "instrument": LEAD, "normalization": norm, "direction": "BOTH",
            "partition": "VALIDATION", "n_events": int(len(rets_all_c)),
            "effect": round(obs2, 5), "ci95_low": round(ci2[0], 5),
            "ci95_high": round(ci2[1], 5), "p_value_raw": round(p2, 5),
            "expected_sign": "+", "bootstrap_effective": b_eff,
        })

    # C1-C4: negative control (EURUSD), primary threshold, VALIDATION
    for norm in ["N1", "N2"]:
        ns = norms[CONTROL][norm]
        ev_all, cids, rets_all, n_down = event_set(dfC, ns, None, THRESH_PRIMARY, vC)
        for direction, lo_i, hi_i in [("DOWN", 0, n_down), ("UP", n_down, len(ev_all))]:
            inc = np.zeros(len(ev_all), dtype=bool)
            inc[lo_i:hi_i] = True
            obs, ci, p = cluster_boot(rets_all, cids, inc)
            cnum = 1 + (0 if norm == "N1" else 2) + (1 if direction == "UP" else 0)
            family_rows.append({
                "test_id": f"C{cnum}", "family": "negative_control",
                "instrument": CONTROL, "normalization": norm, "direction": direction,
                "partition": "VALIDATION", "n_events": int(inc.sum()),
                "effect": round(obs, 5), "ci95_low": round(ci[0], 5),
                "ci95_high": round(ci[1], 5), "p_value_raw": round(p, 5),
                "expected_sign": "0 (null)",
            })

    fam = pd.DataFrame(family_rows)
    pvals = fam["p_value_raw"].fillna(1.0).to_list()
    fam["p_holm"] = [round(v, 5) for v in holm(pvals)]
    fam["holm_significant"] = fam["p_holm"] < 0.05

    # =====================================================================
    # Holdout layer (TEST, lead, primary threshold, Holm within layer)
    # =====================================================================
    for norm in ["N1", "N2"]:
        ns = norms[LEAD][norm]
        ev_all, cids, rets_all, n_down = event_set(dfL, ns, None, THRESH_PRIMARY, tL)
        for direction, lo_i, hi_i in [("DOWN", 0, n_down), ("UP", n_down, len(ev_all))]:
            inc = np.zeros(len(ev_all), dtype=bool)
            inc[lo_i:hi_i] = True
            obs, ci, p = cluster_boot(rets_all, cids, inc)
            holdout_rows.append({
                "test_id": f"H{1 + (0 if norm == 'N1' else 2) + (1 if direction == 'UP' else 0)}",
                "instrument": LEAD, "normalization": norm, "direction": direction,
                "partition": "TEST", "n_events": int(inc.sum()),
                "effect": round(obs, 5), "ci95_low": round(ci[0], 5),
                "ci95_high": round(ci[1], 5), "p_value_raw": round(p, 5),
            })
    ho = pd.DataFrame(holdout_rows)
    ho["p_holm"] = [round(v, 5) for v in holm(ho["p_value_raw"].fillna(1.0).to_list())]
    ho["holm_significant"] = ho["p_holm"] < 0.05

    # =====================================================================
    # Threshold robustness (lead, VALIDATION)
    # =====================================================================
    for norm in ["N1", "N2"]:
        ns = norms[LEAD][norm]
        for th in NEIGHBORHOOD:
            ev_all, cids, rets_all, n_down = event_set(dfL, ns, None, th, vL)
            for direction, lo_i, hi_i in [("DOWN", 0, n_down), ("UP", n_down, len(ev_all))]:
                inc = np.zeros(len(ev_all), dtype=bool)
                inc[lo_i:hi_i] = True
                obs, ci, p = cluster_boot(rets_all, cids, inc)
                thresh_rows.append({
                    "normalization": norm, "direction": direction,
                    "threshold": th, "n_events": int(inc.sum()),
                    "mean_dir_adj": round(obs, 5),
                    "ci95_low": round(ci[0], 5), "ci95_high": round(ci[1], 5),
                    "p_value": round(p, 5),
                })

    # =====================================================================
    # Normalization comparison incl. matched rarity (lead, VALIDATION)
    # =====================================================================
    for norm in NORMALIZATIONS:
        ns = norms[LEAD][norm]
        tr = ns[partsL["TRAIN"][0]: partsL["TRAIN"][1]]
        tr = tr[~np.isnan(tr)]
        qlo, qhi = float(np.quantile(tr, QUANT_MATCH)), float(np.quantile(tr, 1 - QUANT_MATCH))
        for direction, th, signed in [("DOWN", THRESH_PRIMARY, False),
                                      ("UP", THRESH_PRIMARY, False),
                                      ("DOWN", qlo, True),
                                      ("UP", qhi, True)]:
            ev_all, cids, rets_all, n_down = event_set(dfL, ns, None, th, vL, signed=signed)
            lo_i, hi_i = (0, n_down) if direction == "DOWN" else (n_down, len(ev_all))
            inc = np.zeros(len(ev_all), dtype=bool)
            inc[lo_i:hi_i] = True
            obs, ci, p = cluster_boot(rets_all, cids, inc)
            norm_rows.append({
                "normalization": norm, "direction": direction,
                "threshold_type": "PRIMARY" if not signed else "MATCHED_Q",
                "threshold": round(th, 3), "n_events": int(inc.sum()),
                "mean_dir_adj": round(obs, 5),
                "ci95_low": round(ci[0], 5), "ci95_high": round(ci[1], 5),
                "p_value": round(p, 5),
            })

    # =====================================================================
    # Walk-forward folds + chronological thirds (lead, cluster bootstrap)
    # =====================================================================
    for norm in ["N1", "N2"]:
        ns = norms[LEAD][norm]
        for fold_name, e0, e1 in FOLDS:
            ev_part = (int(nL * e0), int(nL * e1))
            ev_all, cids, rets_all, n_down = event_set(dfL, ns, None, THRESH_PRIMARY, ev_part)
            for direction, lo_i, hi_i in [("DOWN", 0, n_down), ("UP", n_down, len(ev_all))]:
                inc = np.zeros(len(ev_all), dtype=bool)
                inc[lo_i:hi_i] = True
                obs, ci, p = cluster_boot(rets_all, cids, inc)
                wf_rows.append({
                    "normalization": norm, "fold": fold_name,
                    "eval_window": f"[{e0:.2f},{e1:.2f})", "direction": direction,
                    "n_events": int(inc.sum()),
                    "mean_dir_adj": round(obs, 5),
                    "ci95_low": round(ci[0], 5), "ci95_high": round(ci[1], 5),
                })
        third_edges = [int(nL * k / 3) for k in range(4)]
        for direction in ["DOWN", "UP"]:
            for k in range(3):
                lo_i = max(third_edges[k], W)
                hi_i = min(third_edges[k + 1], nL)
                if hi_i <= lo_i + H:
                    continue
                ev_all, cids, rets_all, n_down = event_set(
                    dfL, ns, None, THRESH_PRIMARY, (lo_i, hi_i))
                lo2, hi2 = (0, n_down) if direction == "DOWN" else (n_down, len(ev_all))
                inc = np.zeros(len(ev_all), dtype=bool)
                inc[lo2:hi2] = True
                obs, ci, p = cluster_boot(rets_all, cids, inc)
                chrono_rows.append({
                    "normalization": norm, "direction": direction,
                    "chrono_third": k, "n_events": int(inc.sum()),
                    "mean_dir_adj": round(obs, 5),
                    "ci95_low": round(ci[0], 5), "ci95_high": round(ci[1], 5),
                })

    # =====================================================================
    # Cost sensitivity (lead, N1/N2, DOWN/UP, VALIDATION + TEST)
    # =====================================================================
    for norm in ["N1", "N2"]:
        ns = norms[LEAD][norm]
        for direction in ["DOWN", "UP"]:
            for part_name in ["VALIDATION", "TEST"]:
                ev = extract_events(ns, direction, THRESH_PRIMARY, partsL[part_name])
                o = outcomes_bulk(dfL, ev, H, direction)
                dret = o["ret"] if direction == "DOWN" else -o["ret"]
                gross_bp = float(dret.mean()) * 10000.0 if len(dret) else np.nan
                row = {
                    "normalization": norm, "direction": direction,
                    "partition": part_name, "n_events": int(len(dret)),
                    "gross_effect_bp": round(gross_bp, 2),
                }
                for band in COST_BANDS_BP:
                    row[f"net_bp_cost{band}"] = round(gross_bp - band, 2)
                row["break_even_cost_bp"] = round(gross_bp, 2)
                cost_rows.append(row)

    # =====================================================================
    # Write outputs
    # =====================================================================
    pd.DataFrame(manifest_rows).to_csv(OUT / "data_manifest_V3.csv", index=False)
    pd.DataFrame(event_rows).to_csv(OUT / "event_dataset_V3.csv", index=False)
    fam.to_csv(OUT / "confirmatory_results.csv", index=False)
    ho.to_csv(OUT / "holdout_results.csv", index=False)
    pd.DataFrame(dep_rows).to_csv(OUT / "dependence_analysis.csv", index=False)
    pd.DataFrame(cost_rows).to_csv(OUT / "cost_sensitivity.csv", index=False)
    pd.DataFrame(thresh_rows).to_csv(OUT / "threshold_robustness.csv", index=False)
    pd.DataFrame(norm_rows).to_csv(OUT / "normalization_comparison.csv", index=False)
    pd.DataFrame(wf_rows).to_csv(OUT / "walk_forward.csv", index=False)
    pd.DataFrame(chrono_rows).to_csv(OUT / "chrono_thirds.csv", index=False)

    report = {
        "protocol_version": "V3.0.0",
        "normalization_definitions": NORM_DEFS,
        "seeds": {"cluster_bootstrap": SEED},
        "parameters": {"W": W, "H": H, "K": K, "S_sep": S_SEP,
                       "threshold_primary": THRESH_PRIMARY,
                       "threshold_neighborhood": NEIGHBORHOOD,
                       "persist_q": PERSIST_Q, "matched_quantile": QUANT_MATCH,
                       "partitions": {"TRAIN": TRAIN_END, "VALIDATION": VAL_END},
                       "b_boot": B_BOOT, "alpha": 0.05,
                       "family_size": len(fam),
                       "cost_bands_bp": COST_BANDS_BP},
        "dataset_fingerprints_sha256": fingerprints,
        "library_versions": versions,
        "event_dataset_rows": len(event_rows),
        "event_dataset_sha256": hashlib.sha256(
            pd.DataFrame(event_rows).to_csv(index=False).encode("utf-8")).hexdigest(),
    }
    (OUT / "experiment_metadata_V3.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("Wrote outputs to", OUT)


if __name__ == "__main__":
    main()
