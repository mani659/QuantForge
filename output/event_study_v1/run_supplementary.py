"""
QuantForge — Event Study V1 supplementary analyses (pre-registered in protocol §5, §7, §9).
Reads event_dataset_V1.csv; recomputes volatility regimes from source M1 data.
Research artifact; deterministic.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
DATA = Path(__file__).resolve().parents[2] / "data" / "m1"
SEED = 20260812
W = 120

ev = pd.read_csv(OUT / "event_dataset_V1.csv", parse_dates=["event_timestamp"])
ev["hour"] = ev["event_timestamp"].dt.hour

# ---------- 1. D vs D+P comparison (VALIDATION, primary DOWN/UP) ----------
rows = []
for direction in ["DOWN", "UP"]:
    for market in ev["instrument"].unique():
        sub = ev[(ev["direction"] == direction) & (ev["partition"] == "VALIDATION")
                 & (ev["instrument"] == market)]
        for cls in ["D", "D+P"]:
            g = sub[sub["candidate_class"] == cls]["event_return_h120"]
            if len(g) == 0:
                continue
            r = np.random.default_rng(SEED)
            means = np.array([r.choice(g.to_numpy(), size=len(g), replace=True).mean()
                              for _ in range(2000)])
            rows.append({
                "instrument": market, "direction": direction, "candidate_class": cls,
                "event_count": int(len(g)),
                "mean_return_h120": round(float(g.mean()), 5),
                "median_return_h120": round(float(g.median()), 5),
                "ci95_low": round(float(np.percentile(means, 2.5)), 5),
                "ci95_high": round(float(np.percentile(means, 97.5)), 5),
            })
pd.DataFrame(rows).to_csv(OUT / "d_vs_dp_validation_V1.csv", index=False)

# ---------- 2. Outcome distributions (MAE/MFE/recovery/persistence), VALIDATION+TEST ----------
out_rows = []
for direction in ["DOWN", "UP"]:
    for market in ev["instrument"].unique():
        g = ev[(ev["direction"] == direction) & (ev["instrument"] == market)
               & (ev["partition"].isin(["VALIDATION", "TEST"]))]
        if len(g) == 0:
            continue
        out_rows.append({
            "instrument": market, "direction": direction, "events": int(len(g)),
            "mean_mae_h120": round(g["mae_h120"].mean(), 5),
            "median_mae_h120": round(g["mae_h120"].median(), 5),
            "mean_mfe_h120": round(g["mfe_h120"].mean(), 5),
            "median_mfe_h120": round(g["mfe_h120"].median(), 5),
            "mean_recovery_ratio": round(g["recovery_ratio_h120"].mean(), 4),
            "median_recovery_ratio": round(g["recovery_ratio_h120"].median(), 4),
            "mean_recovery_time": round(g["recovery_time_h120"].mean(), 1),
            "mean_retention": round(g["retention_h120"].mean(), 4),
            "pct_recovered_within_H": round(float((g["recovery_time_h120"] <= 120).mean()), 4),
        })
pd.DataFrame(out_rows).to_csv(OUT / "outcome_distributions_V1.csv", index=False)

# ---------- 3. Hour-of-day buckets (TRAIN only, exploratory) ----------
hr_rows = []
for market in ev["instrument"].unique():
    g = ev[(ev["instrument"] == market) & (ev["partition"] == "TRAIN")
           & (ev["direction"] == "DOWN")]
    if len(g) == 0:
        continue
    g = g.copy()
    g["bucket"] = (g["hour"] // 4) * 4
    for b, gg in g.groupby("bucket"):
        hr_rows.append({
            "instrument": market, "hour_bucket": f"{int(b):02d}-{int(b)+3:02d}",
            "event_count": int(len(gg)), "mean_return_h120": round(float(gg["event_return_h120"].mean()), 5),
        })
pd.DataFrame(hr_rows).to_csv(OUT / "hour_of_day_train_V1.csv", index=False)

# ---------- 4. Volatility regime (TRAIN only, exploratory) ----------
reg_rows = []
for market in ["XAUUSD", "EURUSD", "BTCUSD", "XAGUSD", "USATECHIDXUSD"]:
    df = pd.read_csv(DATA / f"{market}_M1.csv", parse_dates=["timestamp"])
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
    df["vol"] = df["close"].pct_change().rolling(W).std()
    tr_vol = df["vol"].quantile([1 / 3, 2 / 3])
    g = ev[(ev["instrument"] == market) & (ev["partition"] == "TRAIN")
           & (ev["direction"] == "DOWN")]
    if len(g) == 0:
        continue
    merged = g.merge(df[["timestamp", "vol"]], left_on="event_timestamp",
                     right_on="timestamp", how="left")
    def tercile(v):
        if pd.isna(v):
            return "NA"
        return "LOW" if v <= tr_vol.iloc[0] else ("MID" if v <= tr_vol.iloc[1] else "HIGH")
    merged["regime"] = merged["vol"].apply(tercile)
    for reg, gg in merged.groupby("regime"):
        reg_rows.append({
            "instrument": market, "volatility_regime": reg,
            "event_count": int(len(gg)), "mean_return_h120": round(float(gg["event_return_h120"].mean()), 5),
        })
pd.DataFrame(reg_rows).to_csv(OUT / "regime_train_V1.csv", index=False)

print("Supplementary outputs written to", OUT)
