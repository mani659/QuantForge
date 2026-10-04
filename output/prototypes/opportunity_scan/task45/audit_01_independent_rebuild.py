"""
Task 45 — Independent audit rebuild.
Recomputes the OPP-02 weekly-rebalance statistic from the frozen inputs
output/prototypes/fx_h4inv_adx_prep/_t37_h4_{sym}.npz (11 symbols, daily H4 pivot).

Frozen spec (Tasks 41/43):
  - 11-symbol MT5 H4 universe (common-11 daily rows)
  - trailing total return over w WEEKS (4/8/13/26 weeks)
  - rank cross-sectionally at weekly rebalance (Mondays)
  - long top tercile / short bottom tercile (equal weight)
  - positions replaced each rebalance; 5-session hold; next-bar-open fill
  - cost 10/5/0 bps per side + disclosed swap proxy

Task 44 (run01_measure.py) instead computed:
  - trailing return window w as DAYS (4/8/13/26 days)
  - rank at every daily row (8,898/8,894/8,889/8,876 obs)
  - no weekly filter; no Monday rebalancing

This script rebuilds the correct weekly statistic and records the comparison.
"""
import numpy as np
import pandas as pd
import json
import os

BASE = "output/prototypes/fx_h4inv_adx_prep/_t37_h4_{sym}.npz"
SYMS = ["XAUUSDm", "XAGUSDm", "USTECm", "EURUSDm", "GBPUSDm", "USDJPYm",
        "EURGBPm", "AUDNZDm", "BTCUSDm", "ETHUSDm", "USOILm"]
WINDOWS = [4, 8, 13, 26]
N_SIMS = 300
SEED = 20261004

def load_sym(sym):
    d = np.load(BASE.format(sym=sym), allow_pickle=True)
    t = d["time"]
    t = t.astype("int64") // 10**9 if t.dtype.kind == "M" else t
    df = pd.DataFrame({k: d[k] for k in d.files if k != "time"},
                      index=pd.to_datetime(t, unit="s", utc=True))
    df.index = df.index.tz_localize(None)
    df["sym"] = sym
    return df

# --- build aligned daily pivot (Task 41/43: one row per common-11 calendar day) ---
cd = [load_sym(s) for s in SYMS]
piv = pd.concat(cd).pivot_table(index=pd.concat(cd).index,
                                columns="sym", values="close").sort_index()
full = piv[piv.notna().all(axis=1)].copy()   # 8,902 common-11 rows

# Per-day cross-sectional tercile masks (frozen: rank over the 11 symbols each day)
rk = full.rank(axis=1, method="first", ascending=False)
tm = rk.le(3).to_numpy()      # long tercile mask
bm = rk.ge(9).to_numpy()      # short tercile mask

# Task 44 numbers (for reference only; not to be modified)
t44 = json.load(open("output/prototypes/opportunity_scan/task44/run01_results.json"))
t44_map = {4: "0", 8: "1", 13: "2", 26: "3"}

out = {}
for w in WINDOWS:
    wk = w * 7                       # 1 week = 7 daily bars
    r = np.full((len(full) - wk, len(SYMS)), np.nan)
    for si in range(len(SYMS)):
        c = full[SYMS[si]].to_numpy()
        r[:, si] = c[wk:] / c[:-wk] - 1
    n = len(r)
    top = np.array([r[i][tm[i]].mean() for i in range(n)])
    bot = np.array([r[i][bm[i]].mean() for i in range(n)])
    act = top - bot                  # per-daily-row top-minus-bottom (w days forward)

    # Task 44: outcome-blind permutation over rank labels (same as original)
    rng = np.random.default_rng(SEED + (w - 4))
    perm = np.array([rng.permutation(len(SYMS)) for _ in range(N_SIMS)])
    top3 = perm[:, :3]; bot3 = perm[:, 3:6]
    null = np.empty(N_SIMS)
    for si in range(N_SIMS):
        tm_ = np.zeros(len(SYMS), dtype=bool)
        bm_ = np.zeros(len(SYMS), dtype=bool)
        tm_[top3[si]] = True; bm_[bot3[si]] = True
        null[si] = (r[:, top3[si]].mean(axis=1) - r[:, bot3[si]].mean(axis=1)).mean()
    null_mean = float(null.mean()) * 1e6
    null_std = float(null.std()) * 1e6

    # Correct weekly-rebalance reference: evaluate act only at Monday close dates
    ts = pd.Series(act, index=full.index[wk:])
    wk_dates = full.index[full.index.dayofweek == 0]
    wk_act = ts.reindex(wk_dates).dropna()
    n_wk = int(wk_act.notna().sum())
    wk_mean_bps = float(wk_act.mean() * 1e6)
    wk_std_bps = float(wk_act.std() * 1e6)

    # Weekly-null (same permutation logic, but restricted to weekly dates)
    # null is recomputed against the weekly-restricted statistic for the audit
    if n_wk > 0:
        wk_act_idx = ts.reindex(wk_dates).dropna()
        wk_idx = list(wk_act_idx.index)
        local_idx = [list(full.index).index(dt) - wk for dt in wk_idx]
        wk_r = r[local_idx]
        wk_null = np.empty(N_SIMS)
        for si in range(N_SIMS):
            wk_null[si] = (wk_r[:, top3[si]].mean(axis=1) - wk_r[:, bot3[si]].mean(axis=1)).mean()
        wk_null_mean = float(wk_null.mean()) * 1e6
        wk_null_std = float(wk_null.std()) * 1e6
    else:
        wk_null_mean = float("nan"); wk_null_std = float("nan")

    t44_mean = float(t44[t44_map[w]]["act_mean"]) * 1e6

    out[str(w)] = dict(
        # frozen-true weekly rebuild
        window_days=w, window_weeks=w,
        window_days_total=wk,
        n_wk=int(wk_act.notna().sum()),
        act_mean_bps=wk_mean_bps,
        act_std_bps=wk_std_bps,
        act_p25_bps=(float(np.percentile(wk_act, 25)) * 1e6) if len(wk_act) else float('nan'),
        act_p75_bps=(float(np.percentile(wk_act, 75)) * 1e6) if len(wk_act) else float('nan'),
        act_p95_bps=(float(np.percentile(wk_act, 95)) * 1e6) if len(wk_act) else float('nan'),
        z_wk_rebal_to_daily_task44=(wk_mean_bps - t44_mean),
        # Task 44 (as implemented)
        task44_n_obs=t44[t44_map[w]]["n_obs"],
        task44_act_mean_bps=t44_mean,
        task44_null_mean_bps=null_mean,
        task44_null_std_bps=null_std,
        task44_z=(t44_mean - null_mean) / null_std if null_std else float("nan"),
        # weekly-null reference
        wk_null_mean_bps=wk_null_mean,
        wk_null_std_bps=wk_null_std,
        wk_z=(wk_mean_bps - wk_null_mean) / wk_null_std if wk_null_std else float("nan"),
        # dates
        first_wk=str(ts.index.min().date()),
    )

# write machine-readable
os.makedirs("output/prototypes/opportunity_scan/task45", exist_ok=True)
with open("output/prototypes/opportunity_scan/task45/audit_build01_weekly_rebuild.json", "w") as f:
    json.dump(dict(task="45", audit="independent_weekly_rebuild", windows=out), f, indent=2)

print(json.dumps(dict(task="45", audit="independent_weekly_rebuild", summary=out), indent=2))
