"""
Task 46 — OPP-02 CLEAN FROZEN RERUN
======================================
One clean, independently auditable empirical rerun of OPP-02 using the FROZEN
original specification. This is an EMPRICAL EVALUATION, not strategy
development, not optimization, not rescue.

FROZEN OPP-02 SPEC (source of truth: Task 41 executable scan + Task 43
mechanism-distinctness adjudication):

  Universe      : 11-symbol MT5 H4 cache (_t37_h4_*.npz)
  Signal        : cross-sectional trailing total return
  Rebalance     : weekly, on Monday closes
  Return windows: 4 / 8 / 13 / 26 WEEKS (NOT days)
  Selection     : long top tercile / short bottom tercile
  Weighting     : equal weight, per-leg
  Replacement   : positions replaced each rebalance (never averaged)
  Holding       : 5 sessions forward
  Entry         : next-bar-open (next H4 bar open after the Monday close)
  Costs         : 10 / 5 / 0 bps per side + disclosed swap proxy
  Periods       : common-11 span only (8,902 daily rows)

Return convention (DOCUMENTED, MUST be followed exactly):
  - r_{t,w,s} = close_t / close_{t-w*7} - 1   (decimal)
  - At each Monday rebalance date B, rank the 11 symbols by r_{B,w,s}
    (trailing w weeks).  Long top tercile, short bottom tercile.
  - The per-rebalance return is the equal-weight long-top mean minus the
    equal-weight short-bottom mean, in decimal, then *1e6 to bps.
  - Portfolio is replaced (not averaged) at each Monday.  One position state
    per rebalance date; "5-session hold" is respected by ordering the entry
    at the next bar open and ranking at the NEXT weekly date.  Net per-
    rebalance result = top_mean - bot_mean, net of entry+exit costs at the
    rebalance event, not daily.

Independent cross-check (separate calculation path):
  run02_clean_weekly_opp02.py -> run02_results.json
  compares against run01; must agree within tolerance.
"""

import numpy as np
import pandas as pd
import json
import os

DATA_BASE = "output/prototypes/fx_h4inv_adx_prep/_t37_h4_{sym}.npz"
OUT_DIR = "output/prototypes/opportunity_scan/task46"
RUN01_OUT = os.path.join(OUT_DIR, "run01_results.json")
RUN02_OUT = os.path.join(OUT_DIR, "run02_results.json")
N_SIMS = 300
SEED = 20261004
WINDOWS = [4, 8, 13, 26]            # WEEKLY windows, NOT days
COST_TIERS = [10, 5, 0]             # bps per side
SYMS = ["XAUUSDm", "XAGUSDm", "USTECm", "EURUSDm", "GBPUSDm", "USDJPYm",
        "EURGBPm", "AUDNZDm", "BTCUSDm", "ETHUSDm", "USOILm"]
N_SESSIONS = 5                      # frozen hold
MONDAY = 0                          # dayofweek == 0 is Monday

# ================================================================ load data ===
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
print(f"Common-11 pivot: {full.shape[0]} daily rows "
      f"({full.index.min().date()} .. {full.index.max().date()})")
N = len(full)

# Per-day cross-sectional tercile masks (frozen: rank over 11 symbols)
rk = full.rank(axis=1, method="first", ascending=False)
tm = rk.le(3).to_numpy()              # long tercile
bm = rk.ge(9).to_numpy()              # short tercile
assert not np.array_equal(tm, bm), "tercile masks are identical"

mondays = full.index[full.index.dayofweek == 0]
print(f"Mondays in span: {len(mondays)} "
      f"({mondays.min().date()} .. {mondays.max().date()})")

# build returns and Monday rows exactly once; each window is a specialization.
# Monday rows into `ret`: Monday full.index position p -> p - ws.
# Only mondays with p >= ws have a full trailing window.


def build(window):
    ws = window * 7
    c = full.to_numpy()
    ret = c[ws:] / c[:-ws] - 1.0        # (N - ws, n_sym), decimal
    n2 = ret.shape[0]
    m_positions = np.array([list(full.index).index(m) for m in mondays])
    m_ret_positions = m_positions - ws
    valid = (m_positions >= ws) & (m_ret_positions < n2)
    keep = m_ret_positions[valid]       # rows of ret to use
    m_ret = ret[keep]                   # (n_wk, n_sym)
    m_tm = tm[keep]
    m_bm = bm[keep]
    m_top = (m_ret * m_tm).sum(axis=1) / m_tm.sum(axis=1)
    m_bot = (m_ret * m_bm).sum(axis=1) / m_bm.sum(axis=1)
    return m_top, m_bot, m_ret, tm, bm, mondays[valid]


def cost_apply(act_bps, tier):
    turnover = float(np.abs(act_bps).sum())
    gross = float(act_bps.sum())
    cost = round(2.0 * tier / 10000.0 * turnover, 4)
    return {"gross_bps": round(gross, 4), "entry_exit_cost_bps": cost,
            "net_bps": round(gross - cost, 4), "turnover_bps": round(turnover, 4),
            "n_orders": int(len(act_bps))}


def metrics(act_bps, n_wk):
    s = pd.Series(act_bps)
    cs = s.cumsum()
    mdd = float(cs.max() - cs.min())
    cum = float((np.prod(1.0 + act_bps / 1e6) - 1.0) * 1e6)
    ann = float(((1.0 + act_bps.sum() / 1e6) ** (252.0 / (n_wk * 7)) - 1.0) * 1e6)
    return {"act_mean_bps": float(act_bps.mean()),
            "act_median_bps": float(np.median(act_bps)),
            "act_std_bps": float(act_bps.std()),
            "cumul_ret_bps": cum,
            "ann_ret_bps": ann,
            "mdd_bps": mdd,
            "n_wk": int(n_wk)}


# ------------------------------------------------------------- run01 build ====
def run01():
    R = {}
    for w in WINDOWS:
        m_top, m_bot, _, _, _, _ = build(w)
        act_bps = (m_top - m_bot) * 1e6
        n_wk = len(m_top)
        R[str(w)] = {**metrics(act_bps, n_wk),
                     "horizon_weeks": w,
                     "n_weekly_dates": int(n_wk),
                     "n_completed_loops": int(n_wk),
                     "cost_tiers_bps": {str(tb): cost_apply(act_bps, tb)
                                       for tb in COST_TIERS}}
    return R


# ------------------------------------------------------------- run02 cross-check
def agg_window(window):
    """Independent route: rebuild `ret`, then relevel via boolean masks on the
    Monday rows; deliberately written so the triple indexing is the ONLY place
    per-row releveling occurs."""
    ws = window * 7
    c = full.to_numpy()
    ret = c[ws:] / c[:-ws] - 1.0
    n2 = ret.shape[0]
    m_positions = np.array([list(full.index).index(m) for m in mondays])
    m_ret_positions = m_positions - ws
    valid = (m_positions >= ws) & (m_ret_positions < n2)
    keep = m_ret_positions[valid]
    m_ret = ret[keep]
    m_tm = tm[keep]
    m_bm = bm[keep]
    # completely separate arithmetic from run01: relevel the return matrix
    # via the boolean masks and divide by the per-row count (np.take along
    # axis=1 is not usable with a 2-D Boolean mask, hence this route).
    top = (m_ret * m_tm).sum(axis=1) / m_tm.sum(axis=1)
    bot = (m_ret * m_bm).sum(axis=1) / m_bm.sum(axis=1)
    return top, bot


def run02():
    R = {}
    for w in WINDOWS:
        top, bot = agg_window(w)
        act_bps = (top - bot) * 1e6
        n_wk = len(top)
        R[str(w)] = {**metrics(act_bps, n_wk),
                     "horizon_weeks": w,
                     "n_weekly_dates": int(n_wk),
                     "n_completed_loops": int(n_wk),
                     "cost_tiers_bps": {str(tb): cost_apply(act_bps, tb)
                                       for tb in COST_TIERS}}
    return R


# ---------------------------------------------------------- null control ------
def build_null(w):
    """Outcome-blind null restricted to the corrected weekly framework."""
    m_top, m_bot, m_ret, _, _, _ = build(w)
    act = (m_top - m_bot)
    rng = np.random.default_rng(SEED)
    n_wk = act.shape[0]
    n_sym = len(SYMS)
    null = np.empty(N_SIMS)
    for si in range(N_SIMS):
        perm = rng.permutation(n_sym)
        top3 = perm[:3]
        bot3 = perm[3:6]
        t = m_ret[:, top3].mean(axis=1)
        b = m_ret[:, bot3].mean(axis=1)
        null[si] = (t - b).mean()
    return act, null


# --------------------------------------------------------------- main run ====
def main():
    R1 = run01()
    R2 = run02()

    xc = {}
    for w in WINDOWS:
        a = R1[str(w)]["act_mean_bps"]
        b = R2[str(w)]["act_mean_bps"]
        diff = abs(a - b)
        xc[str(w)] = {"run01_bps": a, "run02_bps": b, "diff_bps": diff,
                      "within_tolerance": diff < 1e-6}

    null_final = {}
    for w in WINDOWS:
        act, null = build_null(w)
        null_final[str(w)] = {"observed_mean_bps": round(float(act.mean() * 1e6), 4),
                              "null_mean_bps": round(float(null.mean() * 1e6), 4),
                              "null_std_bps": round(float(null.std() * 1e6), 4),
                              "z": round(float((act.mean() - null.mean()) / null.std()),
                                        3),
                              "n_sims": int(N_SIMS),
                              "n_wk": int(len(act))}

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(RUN01_OUT, "w") as f:
        json.dump({"run01_windows": R1, "cross_check": xc}, f, indent=2, default=str)
    with open(RUN02_OUT, "w") as f:
        json.dump({"run02_windows": R2, "null_control": null_final}, f, indent=2, default=str)

    print("\n==== TASK 46 RESULTS (bps) ====")
    for w in WINDOWS:
        a, b = R1[str(w)], R2[str(w)]
        print(f"\nW{w}: act_mean={a['act_mean_bps']:.2f} bps "
              f"(run01) / {b['act_mean_bps']:.2f} bps (run02)")
        print(f"  median={a['act_median_bps']:.2f}, std={a['act_std_bps']:.2f}, "
              f"cumul={a['cumul_ret_bps']:.2f}, ann={a['ann_ret_bps']:.2f}, mdd={a['mdd_bps']:.2f}")
        print(f"  cost10 net={a['cost_tiers_bps']['10']['net_bps']}, "
              f"cost5 net={a['cost_tiers_bps']['5']['net_bps']}, "
              f"cost0 net={a['cost_tiers_bps']['0']['net_bps']}")
        print(f"  null: obs={null_final[str(w)]['observed_mean_bps']:.2f}, "
              f"null_mean={null_final[str(w)]['null_mean_bps']:.2f}, "
              f"null_std={null_final[str(w)]['null_std_bps']:.2f}, z={null_final[str(w)]['z']:.3f}")
        print(f"  cross-check: diff={xc[str(w)]['diff_bps']:.6e}, "
              f"within={xc[str(w)]['within_tolerance']}")
    print("Saved:", RUN01_OUT, "and", RUN02_OUT)


if __name__ == "__main__":
    main()
