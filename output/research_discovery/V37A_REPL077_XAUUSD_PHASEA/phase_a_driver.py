"""
V37A REPL077 XAUUSD — PHASE A DRIVER (detection / feasibility only)
Registration: V37A-REPL-077-XAUUSD-M1
NO OUTCOME COMPUTATION IS PERFORMED. No close[i+30], no returns, no economics.

Frozen helpers (load / compute_atr / atr_pct) are imported from the immutable
archival copy research/archive/v26/CAND-077/v26_g1_screen.py (SHA-256
b320c42d67e909634ec5d1cde829b6d6bab975fb88119d82da2ba8c283cae80b) so the
signal-state semantics are byte-identical to the frozen operational definition.

The treatment/control DETECTION loops below are copied verbatim from run_077 of
that archival module (lines computing `is_breakout` and `is_cf`), with the
outcome/matching/return computation of the original deliberately NOT executed.
Matching is accounted index-only (no prices, no returns).
"""
import hashlib, importlib.util, json, os, time

ARCHIVAL = os.path.abspath("research/archive/v26/CAND-077/v26_g1_screen.py")
spec = importlib.util.spec_from_file_location("v26_frozen", ARCHIVAL)
frozen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frozen)   # module level: definitions + constants only (__main__ guarded)

# Path-resolution fix only: frozen load() derives DIR from its own file location,
# which resolves to the wrong tree from the archival path. The registered data
# path is data/m1 (per execution manifest). Function body semantics unchanged
# (read CSV, +4h UTC shift, set_index, sort, date column).
frozen.DIR = os.path.abspath("data/m1")

import numpy as np
import pandas as pd

load = frozen.load
compute_atr = frozen.compute_atr
atr_pct = frozen.atr_pct
FRIC = frozen.FRIC

WINDOW_START = pd.Timestamp("2023-09-01")
WINDOW_END = pd.Timestamp("2026-04-10 23:59:59")   # raw-file calendar day 2026-04-10

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    t0 = time.time()
    out = {}

    # ---- input identity (re-verified at execution) ----
    out["execution"] = {
        "registration": "V37A-REPL-077-XAUUSD-M1",
        "phase": "A",
        "archival_impl_sha256": sha256_file(ARCHIVAL),
    }

    # ---- load FULL XAUUSD file via frozen load() (applies +4h UTC shift, sorts) ----
    df = load("XAUUSD")                     # path built inside frozen load() -> data/m1/XAUUSD_M1.csv
    out["data"] = {"n_bars_full": int(len(df)),
                   "first_shifted_ts": str(df.index[0]),
                   "last_shifted_ts": str(df.index[-1])}

    # raw (unshifted) timestamps retained only for the registered calendar-window filter
    raw = pd.read_csv(os.path.abspath("data/m1/XAUUSD_M1.csv"), parse_dates=["timestamp"])
    raw_ts = pd.DatetimeIndex(raw["timestamp"]).sort_values()

    # ---- data integrity ----
    mono = bool(df.index.is_monotonic_increasing)
    dup = int(df.index.duplicated().sum())
    hl = int((df["high"] < df["low"]).sum())
    hc = int((df["high"] < df[["open", "close"]].max(axis=1)).sum())
    lc = int((df["low"] > df[["open", "close"]].min(axis=1)).sum())
    nz = int((df[["open", "high", "low", "close"]] <= 0).sum().sum())
    vol_zero = bool((df["volume"] == 0).all())
    out["integrity"] = {
        "monotonic": mono, "duplicate_timestamps": dup,
        "high_lt_low": hl, "high_lt_max_oc": hc, "low_gt_min_oc": lc,
        "nonpositive_prices": nz, "volume_all_zero": vol_zero,
        "n_nan_atr_pct_full": None,  # filled below
    }

    # ---- signal state (frozen semantics, full history for warm-up) ----
    closes = df["close"].values
    n = len(df)
    atr_vals = compute_atr(df, 14)
    atr_p = atr_pct(atr_vals, 200)
    out["integrity"]["n_nan_atr_pct_full"] = int(np.isnan(atr_p).sum())

    # ---- TREATMENT detection — VERBATIM from frozen run_077 (detection only) ----
    is_breakout = np.zeros(n, dtype=bool)
    comp_high = np.full(n, np.nan)
    for i in range(20, n):
        lb_pct = atr_p[max(0, i - 20):i]
        lb_close = closes[max(0, i - 20):i]
        mask = lb_pct < 25
        if np.sum(mask) >= 10:
            comp_high[i] = np.max(lb_close[mask])

    for i in range(250, n - 30):
        if np.isnan(atr_p[i]) or atr_p[i] <= 50:
            continue
        recent_min = np.nanmin(atr_p[max(0, i - 5):i + 1])
        if np.isnan(recent_min) or recent_min >= 25:
            continue
        if np.isnan(comp_high[i]) or closes[i] <= comp_high[i]:
            continue
        is_breakout[i] = True

    # ---- CONTROL detection — VERBATIM from frozen run_077 (detection only) ----
    is_cf = np.zeros(n, dtype=bool)
    for i in range(250, n - 30):
        if np.isnan(atr_p[i]) or atr_p[i] <= 50:
            continue
        preceding = atr_p[max(0, i - 30):i + 1]
        if np.any(np.isnan(preceding)) or np.nanmin(preceding) <= 50:
            continue
        c_h = np.max(closes[max(0, i - 20):i]) if i >= 20 else 0
        if closes[i] > c_h:
            is_cf[i] = True

    # ---- primary-window filter (registered calendar window on RAW timestamps) ----
    # raw row i corresponds to shifted row i (constant +4h shift, rows sorted identically)
    raw_dates = raw_ts
    in_window = (raw_dates >= WINDOW_START) & (raw_dates <= WINDOW_END)
    treat_all = np.where(is_breakout)[0]
    cf_all = np.where(is_cf)[0]
    treat_win = np.array([i for i in treat_all if bool(in_window[i])])
    cf_win = np.array([i for i in cf_all if bool(in_window[i])])

    # ---- index-only matching accounting for window treatments (frozen rule:
    #      lowest-index CF within [ti-50, ti+50], excluding ti) ----
    cf_set = set(cf_all.tolist())
    matched_count = 0
    matched_cf_indices = []
    unmatched = []
    for ti in treat_win:
        lo, hi = ti - 50, ti + 50
        found = None
        for ci in range(lo, hi + 1):
            if ci in cf_set and ci != ti:
                found = ci
                break
        if found is not None:
            matched_count += 1
            matched_cf_indices.append(found)
        else:
            unmatched.append(int(ti))

    dup_cf_use = int(len(matched_cf_indices) - len(set(matched_cf_indices)))
    unique_cf_used = int(len(set(matched_cf_indices)))

    out["populations"] = {
        "treatment_events_full_file": int(len(treat_all)),
        "control_events_full_file": int(len(cf_all)),
        "treatment_events_primary_window": int(len(treat_win)),
        "control_events_primary_window": int(len(cf_win)),
        "matched_control_entries_produced_for_window_treatments": matched_count,
        "unique_control_events_used_in_matching": unique_cf_used,
        "duplicate_control_reuse_in_matched_sample": dup_cf_use,
        "unmatched_window_treatments": len(unmatched),
        "window_treatment_first_entry_ts": str(raw_dates[treat_win[0]]) if len(treat_win) else None,
        "window_treatment_last_entry_ts": str(raw_dates[treat_win[-1]]) if len(treat_win) else None,
        "window_control_first_entry_ts": str(raw_dates[cf_win[0]]) if len(cf_win) else None,
        "window_control_last_entry_ts": str(raw_dates[cf_win[-1]]) if len(cf_win) else None,
    }
    out["timing_seconds"] = round(time.time() - t0, 1)

    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "phase_a_report.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
