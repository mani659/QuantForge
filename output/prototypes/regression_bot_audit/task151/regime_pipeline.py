"""K-means volatility-regime pipeline (TASK151, approved TASK148 chain).

Implements EXACTLY the frozen preregistration
(task148/148_kmeans_regime_preregistration.md); no variants, no search,
no adaptation. Descriptive characterization only: no signals, no returns,
no P&L, no candidates.

Frozen points (with provenance):
- Panel: 11 _t37_m1_{SYM}.npz (row counts in prereg section 2).
- Grid: DAILY from M1. Zero-bar days excluded + counted; no fill.
- Features (OHLC+spread only): (1) log realized variance = log(sum of
  squared M1 log returns); (2) Parkinson = (ln(H/L))^2/(4 ln 2) from
  daily high/low; (3) vol-of-vol = 20-day rolling std of log-RV;
  (4) spread percentile = 20-day rolling rank of daily mean spread.
  Zero-variance days excluded + counted (log undefined; fail-closed,
  consistent with the no-fill rule). Warmup NaNs (first 19 days per
  feature) dropped + counted.
- Normalization: per-symbol z-score with TRAINING-segment mean/std only.
- FENCED OUT: returns/slopes/MA/breakouts/session/calendar/ADX/ATR-
  triggers/adxcache files/volume (no volume column exists anywhere).
- KMeans: scikit-learn, kmeans++ init, k in {2,3}, n_init=1 x seeds 0-9
  (10 restarts), lowest inertia wins, first wins ties. Deterministic.
- Segments: TRAIN 2021-01->2023-12, VALIDATION 2024, TEST 2025->panel end
  (calendar boundaries; assignment by timestamp, frozen).
- Stability: Hungarian-matched centroid ARI (own-fit vs mapped) on val
  and test; persistence = mean dwell days; prevalence = TEST shares.
- Baselines: pooled-vol tertile split (deterministic); shuffled null
  (seed 0, fixed) expecting ARI ~= 0.
- Budgets: 2 k-configs + 2 baselines + 1 null = 5 fits max, single run.
"""

import hashlib
import math

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

SYMBOLS = ["AUDNZDm", "BTCUSDm", "ETHUSDm", "EURGBPm", "EURUSDm",
           "GBPUSDm", "USDJPYm", "USOILm", "USTECm", "XAGUSDm", "XAUUSDm"]
EXPECTED_ROWS = {"AUDNZDm": 2132968, "BTCUSDm": 3017792, "ETHUSDm": 3017787,
                 "EURGBPm": 2120964, "EURUSDm": 2120306, "GBPUSDm": 2125500,
                 "USDJPYm": 2126055, "USOILm": 1994318, "USTECm": 1970042,
                 "XAGUSDm": 2009865, "XAUUSDm": 2029174}
KS = [2, 3]
SEEDS = list(range(10))
TRAIN_END = "2023-12-31"
VAL_END = "2024-12-31"
ROLL = 20


class IntegrityStop(Exception):
    """Fail-closed integrity stop. No measurement proceeds."""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_symbol(path, symbol):
    """Load one NPZ (OHLC+spread + timestamps). Returns daily frame."""
    z = np.load(path, allow_pickle=True)
    keys = set(str(k) for k in z.keys())
    for k in ("time", "open", "high", "low", "close", "spread"):
        if k not in keys:
            raise IntegrityStop("missing field %s in %s" % (k, symbol))
    ts = pd.to_datetime(z["time"].astype("int64"), unit="s", utc=True)
    df = pd.DataFrame({"open": np.asarray(z["open"], dtype=float),
                       "high": np.asarray(z["high"], dtype=float),
                       "low": np.asarray(z["low"], dtype=float),
                       "close": np.asarray(z["close"], dtype=float),
                       "spread": np.asarray(z["spread"], dtype=float)},
                      index=ts).sort_index()
    if bool(df.index.duplicated().any()):
        raise IntegrityStop("duplicate timestamps in " + symbol)
    return df


def daily_features(m1):
    """Daily feature rows from M1 bars. Returns (frame, dropped_counts)."""
    dropped = {"zero_bar_days": 0}
    m1 = m1[m1["close"] > 0]
    days = m1.groupby(m1.index.date)
    recs = []
    for day, g in days:
        if len(g) == 0:
            dropped["zero_bar_days"] += 1
            continue
        lr = np.log(g["close"] / g["close"].shift(1)).dropna()
        rv = float((lr ** 2).sum())
        hi, lo, cl = float(g["high"].max()), float(g["low"].min()), float(g["close"].iloc[-1])
        park = ((math.log(hi / lo) ** 2) / (4.0 * math.log(2.0))
                if hi > 0 and lo > 0 and hi >= lo else float("nan"))
        recs.append({"date": pd.Timestamp(day, tz="UTC"), "rv": rv,
                     "park": park, "spread": float(g["spread"].mean())})
    return pd.DataFrame(recs), dropped


def build_matrix(symbols_data):
    """Pooled daily feature matrix + warmup handling. Returns (X_raw, index)."""
    feats = []
    for sym, d in symbols_data.items():
        f = d.copy()
        f["log_rv"] = np.log(f["rv"].where(f["rv"] > 0))
        f["log_park"] = np.log(f["park"].where(f["park"] > 0))
        f["volvol"] = f["log_rv"].rolling(ROLL).std()
        f["spread_pct"] = f["spread"].rolling(ROLL).apply(
            lambda w: pd.Series(w).rank(pct=True).iloc[-1], raw=False)
        f["sym"] = sym
        feats.append(f)
    full = pd.concat(feats, ignore_index=True)
    before = len(full)
    full = full.dropna(subset=["log_rv", "log_park", "volvol", "spread_pct"])
    dropped = {"zero_var_or_warmup": before - len(full)}
    return full, dropped


def split_segments(full):
    tr = full[full["date"] <= TRAIN_END]
    va = full[(full["date"] > TRAIN_END) & (full["date"] <= VAL_END)]
    te = full[full["date"] > VAL_END]
    return tr, va, te


COLS = ["log_rv", "log_park", "volvol", "spread_pct"]


def standardize(tr, va, te):
    mu = tr[COLS].mean()
    sd = tr[COLS].std(ddof=1).replace(0.0, 1.0)
    return ((tr[COLS] - mu) / sd, (va[COLS] - mu) / sd,
            (te[COLS] - mu) / sd, mu, sd)


def fit_kmeans(X, k):
    best, best_inertia = None, None
    for s in SEEDS:
        km = KMeans(n_clusters=k, init="k-means++", n_init=1,
                    random_state=s)
        lab = km.fit_predict(X.values)
        if best is None or km.inertia_ < best_inertia:
            best, best_inertia = (km, lab), km.inertia_
    return best


def match_ari(cent_a, lab_a, cent_b, lab_b):
    """ARI between lab_b and lab_a after Hungarian-matching centroids."""
    import numpy as np
    d = np.linalg.norm(cent_a[:, None, :] - cent_b[None, :, :], axis=2)
    row, col = linear_sum_assignment(d)
    remap = {c: r for r, c in zip(row, col)}
    mapped = np.array([remap.get(x, -1) for x in lab_b])
    return float(adjusted_rand_score(lab_a, mapped))


def dwell(labels):
    """Mean consecutive-run length in days."""
    if len(labels) == 0:
        return 0.0
    runs, cur, n = [], labels[0], 1
    for x in labels[1:]:
        if x == cur:
            n += 1
        else:
            runs.append(n)
            cur, n = x, 1
    runs.append(n)
    return float(sum(runs) / len(runs))


def prevalence(labels, k):
    labels = np.asarray(labels)
    return {int(c): float((labels == c).mean()) for c in range(k)}
