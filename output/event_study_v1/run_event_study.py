"""
QuantForge — Canonical Mean-Reversion Event Study V1
Implements EVENT_STUDY_PROTOCOL_V1.md exactly. Research artifact; not production code.
Deterministic (fixed seeds). Outputs written to output/event_study_v1/.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
DATA = Path(__file__).resolve().parents[2] / "data" / "m1"

# ---- Pre-registered protocol parameters (V1.0.0) ----
W_PRIMARY = 120          # displacement window (bars, M1)
W_SENS = [60, 240]       # sensitivity windows
M_MOM = 30               # momentum lookback (bars)
Z_PRIMARY = 3.0          # primary displacement threshold
Z_GRID = [2.0, 2.5, 3.0, 3.5, 4.0]
S_SEP = 240              # same-direction minimum separation (bars)
H_PRIMARY = 120          # outcome horizon
H_SENS = [60, 240]
TRAIN_END = 0.70         # chronological partition fractions
VAL_END = 0.85
P25 = 0.25               # panic-momentum quantile (DOWN); 0.75 mirrored (UP)
B_BOOT = 2000            # bootstrap resamples
SEED = 20260812
MARKETS = ["XAUUSD", "EURUSD", "BTCUSD", "XAGUSD", "USATECHIDXUSD"]

rng = np.random.default_rng(SEED)


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
    # gaps > 2 minutes (i.e., >1 missing M1 bar)
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


def compute_measures(df: pd.DataFrame, w: int) -> pd.DataFrame:
    roll = df["close"].rolling(w, min_periods=w)
    df = df.copy()
    df["z"] = (df["close"] - roll.mean()) / roll.std()
    df["mom"] = df["close"].pct_change(M_MOM) * 100.0
    return df


def partitions(df: pd.DataFrame) -> dict:
    n = len(df)
    return {
        "TRAIN": (0, int(n * TRAIN_END)),
        "VALIDATION": (int(n * TRAIN_END), int(n * VAL_END)),
        "TEST": (int(n * VAL_END), n),
    }


def extract_events(df: pd.DataFrame, direction: str, z_thresh: float, w: int,
                   part: tuple, h: int) -> list:
    """Pre-registered event extraction: threshold + same-direction separation S."""
    start, end = part
    lo = start + w + M_MOM          # warm-up for z and mom
    hi = end - h                     # need h forward bars within partition
    if hi <= lo:
        return []
    if direction == "DOWN":
        mask = (df["z"] <= -z_thresh)
    else:
        mask = (df["z"] >= +z_thresh)
    idxs = np.flatnonzero(mask.to_numpy())
    idxs = idxs[(idxs >= lo) & (idxs < hi)]
    kept = []
    last = -10**9
    for i in idxs:
        if i - last >= S_SEP:
            kept.append(int(i))
            last = i
    return kept


def outcomes(df: pd.DataFrame, i: int, h: int, direction: str) -> dict:
    close = df["close"]
    high = df["high"]
    low = df["low"]
    c0 = close.iloc[i]
    seg = slice(i + 1, i + h + 1)
    cseg = close.iloc[seg]
    hseg = high.iloc[seg]
    lseg = low.iloc[seg]
    ret = cseg.iloc[-1] / c0 - 1.0
    if direction == "DOWN":
        adverse = (c0 - lseg.min()) / c0
        favorable = (hseg.max() - c0) / c0
    else:
        adverse = (hseg.max() - c0) / c0
        favorable = (c0 - lseg.min()) / c0
    denom = favorable + adverse
    rec_ratio = favorable / denom if denom > 0 else np.nan
    above = (cseg > c0)
    rec_time = int(np.argmax(above.to_numpy()) + 1) if above.any() else h + 1
    retention = float(above.mean())
    return {
        "event_return": ret,
        "adverse": float(adverse),
        "favorable": float(favorable),
        "recovery_ratio": float(rec_ratio) if not np.isnan(rec_ratio) else None,
        "recovery_time": rec_time,
        "retention": retention,
    }


def bootstrap_ci(values: np.ndarray, b: int = B_BOOT, seed: int = SEED) -> tuple:
    r = np.random.default_rng(seed)
    if len(values) == 0:
        return (np.nan, np.nan)
    means = np.array([r.choice(values, size=len(values), replace=True).mean()
                      for _ in range(b)])
    return (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


def baseline_returns(df: pd.DataFrame, part: tuple, h: int) -> np.ndarray:
    start, end = part
    lo = start
    hi = end - h
    if hi <= lo:
        return np.array([])
    close = df["close"]
    j = np.arange(lo, hi)
    return (close.iloc[j + h].to_numpy() / close.iloc[j].to_numpy()) - 1.0


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    event_rows = []
    summary = []
    thresh_rows = []
    cross_rows = []
    versions = {"pandas": pd.__version__, "numpy": np.__version__}
    fingerprints = {}

    for market in MARKETS:
        print(f"[{market}] loading…", flush=True)
        df = load_market(market)
        fingerprints[market] = sha256(DATA / f"{market}_M1.csv")
        manifest_rows.append(data_manifest(df, market))

        dfm = compute_measures(df, W_PRIMARY)
        parts = partitions(dfm)

        # Panic-momentum quantiles from TRAIN only (pre-registered)
        tr = dfm.iloc[parts["TRAIN"][0]: parts["TRAIN"][1]]
        p25 = float(tr["mom"].quantile(P25))
        p75 = float(tr["mom"].quantile(1 - P25))

        for direction in ["DOWN", "UP"]:
            for part_name, part in parts.items():
                ev = extract_events(dfm, direction, Z_PRIMARY, W_PRIMARY, part, H_PRIMARY)
                for i in ev:
                    o120 = outcomes(dfm, i, H_PRIMARY, direction)
                    o60 = outcomes(dfm, i, 60, direction) if i + 60 <= part[1] else None
                    o240 = outcomes(dfm, i, 240, direction) if i + 240 <= part[1] else None
                    mom = float(dfm["mom"].iloc[i])
                    if direction == "DOWN":
                        cls = "D+P" if mom <= p25 else "D"
                    else:
                        cls = "D+P" if mom >= p75 else "D"
                    event_rows.append({
                        "instrument": market, "timeframe": "M1", "direction": direction,
                        "partition": part_name,
                        "event_timestamp": str(dfm["timestamp"].iloc[i]),
                        "event_definition_version": "V1.0.0",
                        "z_score": round(float(dfm["z"].iloc[i]), 3),
                        "momentum_pct": round(mom, 3),
                        "candidate_class": cls,
                        "mae_h120": round(o120["adverse"], 5),
                        "mfe_h120": round(o120["favorable"], 5),
                        "recovery_ratio_h120": round(o120["recovery_ratio"], 4)
                        if o120["recovery_ratio"] is not None else None,
                        "recovery_time_h120": o120["recovery_time"],
                        "retention_h120": round(o120["retention"], 4),
                        "event_return_h120": round(o120["event_return"], 5),
                        "event_return_h60": round(o60["event_return"], 5) if o60 else None,
                        "event_return_h240": round(o240["event_return"], 5) if o240 else None,
                    })

        # ---- Confirmatory statistics at primary Z=3.0, H=120 ----
        for direction in ["DOWN", "UP"]:
            for part_name, part in parts.items():
                ev = extract_events(dfm, direction, Z_PRIMARY, W_PRIMARY, part, H_PRIMARY)
                rets = np.array([outcomes(dfm, i, H_PRIMARY, direction)["event_return"]
                                 for i in ev])
                base = baseline_returns(dfm, part, H_PRIMARY)
                n_rand = min(len(rets), max(0, len(base) - 1))
                ci = bootstrap_ci(rets) if len(rets) else (np.nan, np.nan)
                if len(rets) and len(base) > 0:
                    r = np.random.default_rng(SEED + len(rets))
                    sample = r.choice(base, size=len(rets), replace=False)
                    diff = rets.mean() - sample.mean()
                    diff_ci = bootstrap_ci(rets - r.choice(base, size=len(rets), replace=False))
                else:
                    diff, diff_ci = np.nan, (np.nan, np.nan)
                distinguishable = bool(
                    len(rets) >= 30 and ci[0] > 0 and not np.isnan(diff_ci[0])
                    and diff_ci[0] > 0
                )
                summary.append({
                    "instrument": market, "direction": direction, "partition": part_name,
                    "Z": Z_PRIMARY, "W": W_PRIMARY, "H": H_PRIMARY,
                    "event_count": int(len(rets)),
                    "mean_return": round(float(rets.mean()), 5) if len(rets) else None,
                    "median_return": round(float(np.median(rets)), 5) if len(rets) else None,
                    "ci95_low": round(ci[0], 5) if len(rets) else None,
                    "ci95_high": round(ci[1], 5) if len(rets) else None,
                    "baseline_mean": round(float(base.mean()), 5) if len(base) else None,
                    "diff_vs_baseline": round(diff, 5) if len(rets) and len(base) else None,
                    "diff_ci95_low": round(diff_ci[0], 5) if len(rets) and len(base) else None,
                    "diff_ci95_high": round(diff_ci[1], 5) if len(rets) and len(base) else None,
                    "distinguishable_from_chance": distinguishable,
                })

        # ---- Threshold stability grid: TRAIN only (exploratory) ----
        for z in Z_GRID:
            for direction in ["DOWN", "UP"]:
                ev = extract_events(dfm, direction, z, W_PRIMARY,
                                    parts["TRAIN"], H_PRIMARY)
                rets = np.array([outcomes(dfm, i, H_PRIMARY, direction)["event_return"]
                                 for i in ev])
                ci = bootstrap_ci(rets) if len(rets) else (np.nan, np.nan)
                thresh_rows.append({
                    "instrument": market, "direction": direction, "Z": z,
                    "event_count": int(len(rets)),
                    "mean_return": round(float(rets.mean()), 5) if len(rets) else None,
                    "ci95_low": round(ci[0], 5) if len(rets) else None,
                    "ci95_high": round(ci[1], 5) if len(rets) else None,
                })

        # ---- Window sensitivity (W) at primary Z on VALIDATION ----
        for w in W_SENS:
            dfw = compute_measures(df, w)
            for direction in ["DOWN", "UP"]:
                ev = extract_events(dfw, direction, Z_PRIMARY, w,
                                    parts["VALIDATION"], H_PRIMARY)
                rets = np.array([outcomes(dfw, i, H_PRIMARY, direction)["event_return"]
                                 for i in ev])
                ci = bootstrap_ci(rets) if len(rets) else (np.nan, np.nan)
                thresh_rows.append({
                    "instrument": market, "direction": direction, "Z": Z_PRIMARY,
                    "sensitivity": f"W={w}",
                    "event_count": int(len(rets)),
                    "mean_return": round(float(rets.mean()), 5) if len(rets) else None,
                    "ci95_low": round(ci[0], 5) if len(rets) else None,
                    "ci95_high": round(ci[1], 5) if len(rets) else None,
                })

        print(f"[{market}] done.", flush=True)

    # ---- Cross-market pooled table (primary Z=3.0, VALIDATION + TEST) ----
    for direction in ["DOWN", "UP"]:
        for part_name in ["VALIDATION", "TEST"]:
            pooled = [s for s in summary
                      if s["direction"] == direction and s["partition"] == part_name
                      and s["event_count"] > 0]
            if not pooled:
                continue
            n = sum(s["event_count"] for s in pooled)
            wmean = sum(s["mean_return"] * s["event_count"] for s in pooled) / n
            cross_rows.append({
                "direction": direction, "partition": part_name,
                "markets_present": len(pooled),
                "total_events": n,
                "weighted_mean_return": round(wmean, 5),
                "markets_positive_ci": sum(1 for s in pooled if s["ci95_low"] > 0),
                "markets_negative_ci": sum(1 for s in pooled if s["ci95_high"] < 0),
            })

    pd.DataFrame(manifest_rows).to_csv(OUT / "data_manifest_V1.csv", index=False)
    pd.DataFrame(event_rows).to_csv(OUT / "event_dataset_V1.csv", index=False)
    pd.DataFrame(summary).to_csv(OUT / "results_summary_V1.csv", index=False)
    pd.DataFrame(thresh_rows).to_csv(OUT / "threshold_stability_V1.csv", index=False)
    pd.DataFrame(cross_rows).to_csv(OUT / "cross_market_V1.csv", index=False)

    report = {
        "protocol_version": "V1.0.0",
        "seeds": {"bootstrap": SEED, "random_sample": SEED},
        "parameters": {"W_primary": W_PRIMARY, "m_mom": M_MOM, "Z_primary": Z_PRIMARY,
                       "S_sep": S_SEP, "H_primary": H_PRIMARY,
                       "partitions": {"TRAIN": TRAIN_END, "VALIDATION": VAL_END}},
        "dataset_fingerprints_sha256": fingerprints,
        "library_versions": versions,
        "event_dataset_rows": len(event_rows),
        "event_dataset_sha256": hashlib.sha256(
            pd.DataFrame(event_rows).to_csv(index=False).encode("utf-8")).hexdigest(),
    }
    (OUT / "experiment_metadata_V1.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("Wrote outputs to", OUT)


if __name__ == "__main__":
    main()
