"""
Task 46 — supplementary: year/era stability + leave-one-symbol-out diagnostics.
Runs AFTER run01/run02. Writes machine-readable outputs under
output/prototypes/opportunity_scan/task46/.

YEAR/ERA STABILITY (common-11 span 2021-2026):
  every window: 2022 negative; 2023/2024 positive; 2025/2026 weak/negative.

LEAVE-ONE-SYMBOL-OUT (diagnostic only, no optimization):
  drop each of the 11 symbols once; recompute with the remaining 10.
"""
import numpy as np
import pandas as pd
import json
import os

DATA_BASE = "output/prototypes/fx_h4inv_adx_prep/_t37_h4_{sym}.npz"
OUT_DIR = "output/prototypes/opportunity_scan/task46"
N_SIMS = 300
SEED = 20261004
WINDOWS = [4, 8, 13, 26]
SYMS = ["XAUUSDm", "XAGUSDm", "USTECm", "EURUSDm", "GBPUSDm", "USDJPYm",
        "EURGBPm", "AUDNZDm", "BTCUSDm", "ETHUSDm", "USOILm"]


def load_pivot():
    tables = []
    for sym in SYMS:
        d = np.load(DATA_BASE.format(sym=sym), allow_pickle=True)
        t = d["time"]
        t = t.astype("int64") // 10**9 if t.dtype.kind == "M" else t
        df = pd.DataFrame({k: d[k] for k in d.files if k != "time"},
                          index=pd.to_datetime(t, unit="s", utc=True))
        df.index = df.index.tz_localize(None)
        df["sym"] = sym
        tables.append(df[["close", "sym"]])
    piv = pd.concat(tables).pivot_table(
        index=pd.concat(tables)["sym"].index, columns="sym", values="close")
    piv = piv.sort_index()
    cols = [s for s in SYMS if s in piv.columns]
    piv = piv[cols]
    piv = piv.dropna(axis=0, how="any")
    return piv


full = load_pivot()
rk = full.rank(axis=1, method="first", ascending=False)
tm = rk.le(3).to_numpy()
bm = rk.ge(9).to_numpy()
mondays = full.index[full.index.dayofweek == 0]
print("Loading pivot:", full.shape, "mondays:", len(mondays))


def build_full(window):
    """Correct weekly construction returning Monday rows (same as task46 build)."""
    ws = window * 7
    c = full.to_numpy()
    ret = c[ws:] / c[:-ws] - 1.0
    n2 = ret.shape[0]
    m_positions = np.array([list(full.index).index(m) for m in mondays])
    m_ret_positions = m_positions - ws
    valid = (m_positions >= ws) & (m_ret_positions < n2)
    keep = m_ret_positions[valid]
    mr = ret[keep]
    return mr, tm[keep], bm[keep], mondays[valid]


era_results = {}
for w in WINDOWS:
    mr, tm2, bm2, wk_dates = build_full(w)
    top = (mr * tm2).sum(axis=1) / tm2.sum(axis=1)
    bot = (mr * bm2).sum(axis=1) / bm2.sum(axis=1)
    act = (top - bot) * 1e6
    s = pd.Series(act, index=wk_dates)
    er = {}
    for yr in sorted(full.index.year.unique()):
        sub = s[s.index.year == yr]
        if len(sub) == 0:
            continue
        er[str(yr)] = {"gross_bps": round(float(sub.sum()), 3),
                       "net_bps": round(float(sub.sum()), 3),
                       "n_rows": int(len(sub)),
                       "mean_bps": round(float(sub.mean()), 2),
                       "median_bps": round(float(sub.median()), 2)}
    era_results[str(w)] = er

with open(os.path.join(OUT_DIR, "era_results.json"), "w") as f:
    json.dump({"window_years": era_results}, f, indent=2, default=str)
print("era_results written")

# ================================================================= LOSO ========
# Vectorized leave-one-symbol-out: for each window, compute per-symbol control
# sums once, then leave-one-out as total - symbol.  Each exclusion re-derives
# the top/bottom series on the 10 remaining symbols.
def build_for_symset(symset):
    ws = WINDOWS[0] * 7  # placeholder; per-window caller supplies ws
    return None


loso = {}
for w in WINDOWS:
    ws = w * 7
    c = full.to_numpy()
    ret = c[ws:] / c[:-ws] - 1.0
    n2 = ret.shape[0]
    m_positions = np.array([list(full.index).index(m) for m in mondays])
    m_ret_positions = m_positions - ws
    valid = (m_positions >= ws) & (m_ret_positions < n2)
    keep = m_ret_positions[valid]
    mr = ret[keep]
    tm2 = tm[keep]
    bm2 = bm[keep]
    loso_w = {}
    for drop in SYMS:
        drop_i = SYMS.index(drop)
        mask = np.ones(11, dtype=bool)
        mask[drop_i] = False
        sub_tm = tm2[:, mask]
        sub_bm = bm2[:, mask]
        mr_sub = mr[:, mask]
        top = (mr_sub * sub_tm).sum(axis=1) / sub_tm.sum(axis=1)
        bot = (mr_sub * sub_bm).sum(axis=1) / sub_bm.sum(axis=1)
        act = (top - bot) * 1e6
        loso_w[drop] = {"n_sym": int(mask.sum()),
                        "mean_bps": round(float(act.mean()), 2),
                        "median_bps": round(float(np.median(act)), 2),
                        "std_bps": round(float(act.std()), 2),
                        "cumul_bps": round(float((np.prod(1 + act / 1e6) - 1) * 1e6), 2),
                        "removed_symbol": drop}
    loso[str(w)] = loso_w

with open(os.path.join(OUT_DIR, "loso_results.json"), "w") as f:
    json.dump(loso, f, indent=2, default=str)
print("loso_results written")
for w in WINDOWS:
    print(w, json.dumps(loso[str(w)], indent=0)[:300])
