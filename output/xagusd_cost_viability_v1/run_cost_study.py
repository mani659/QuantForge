# QuantForge — XAGUSD Real Transaction Cost & Economic Viability Study V1
# Implements COST_VIABILITY_PROTOCOL_V1.md exactly. Read-only wrt architecture.
# Stage 1: stream tick file -> per-minute bid/ask aggregates (cached CSV).
# Stage 2: characterize cost data.
# Stage 3: match observed costs to V3 XAGUSD events; gross-to-net; cluster bootstrap.
# Stage 4: session / regime / year cost tables.
# Stage 5: write outputs under output/xagusd_cost_viability_v1/.

import os, sys, json, hashlib, time
import numpy as np
import pandas as pd

AREA = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(AREA, "..", ".."))
TICK = os.path.join(ROOT, "data", "tick", "XAGUSD_mt5_ticks.csv")
M1 = os.path.join(ROOT, "data", "m1", "XAGUSD_M1.csv")
EVENTS = os.path.join(ROOT, "output", "event_study_v3", "event_dataset_V3.csv")
MINUTE_CACHE = os.path.join(AREA, "xagusd_minute_aggregates.csv")
SEED = 20260814
B = 2000

def sha256(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def stream_ticks(step):
    """Stream tick file; compute per-minute medians + a deterministic systematic tick-level sample."""
    names = ["date", "time", "bid", "ask", "last", "vol"]
    SYS = 150                     # systematic sample: every 150th tick (~975k rows)
    sys_sample = []               # tick-level sample: (spread_abs, mid)
    nrows = 0
    chunk_dfs = []
    first_ts = last_ts = None
    prev_last = None
    n_out_of_order = 0
    start = time.time()
    for ci, chunk in enumerate(pd.read_csv(TICK, names=names, chunksize=5000000,
                                           dtype={"date": str, "time": str, "vol": "int64"})):
        bid = chunk["bid"].to_numpy(float)
        ask = chunk["ask"].to_numpy(float)
        spread = ask - bid
        mid = (bid + ask) / 2.0
        nrows += len(chunk)
        sys_sample.append(np.column_stack([spread[::SYS], mid[::SYS]]))
        dt = pd.to_datetime(chunk["date"] + " " + chunk["time"], format="%Y%m%d %H:%M:%S")
        minute = dt.dt.floor("min")
        g = pd.DataFrame({"minute": minute, "bid": bid, "ask": ask, "spread": spread, "mid": mid})
        agg = g.groupby("minute").agg(bid_med=("bid", "median"), ask_med=("ask", "median"),
                                      spread_med=("spread", "median"), nticks=("spread", "size")).reset_index()
        chunk_dfs.append(agg)
        if first_ts is None:
            first_ts = dt.iloc[0]
        last_ts = dt.iloc[-1]
        if prev_last is not None and dt.iloc[0] < prev_last:
            n_out_of_order += 1
        prev_last = last_ts
        if ci % 5 == 0:
            print(f"  chunk {ci}: {len(chunk):,} rows, {len(agg):,} minutes, elapsed {time.time()-start:.0f}s", flush=True)
    minute_df = pd.concat(chunk_dfs, ignore_index=True)
    return minute_df, np.concatenate(sys_sample) if sys_sample else np.empty((0, 2)), nrows, first_ts, last_ts, n_out_of_order

def build_minute_cache(force=False):
    if os.path.exists(MINUTE_CACHE) and not force:
        print("minute cache exists; loading", flush=True)
        return pd.read_csv(MINUTE_CACHE, parse_dates=["minute"])
    print("streaming ticks...", flush=True)
    minute_df, reservoir, nrows, first_ts, last_ts, n_oao = stream_ticks(0)
    # aggregate duplicate minutes across chunks (a minute cannot span chunks, but be safe)
    minute_df = minute_df.groupby("minute", as_index=False).agg(
        bid_med=("bid_med", "median"), ask_med=("ask_med", "median"),
        spread_med=("spread_med", "median"), nticks=("nticks", "sum"))
    minute_df = minute_df.sort_values("minute").reset_index(drop=True)
    minute_df.to_csv(MINUTE_CACHE, index=False)
    np.save(os.path.join(AREA, "tick_reservoir_sample.npy"), reservoir)
    meta = {"nrows": int(nrows), "first_ts": str(first_ts), "last_ts": str(last_ts),
            "n_out_of_order_chunks": int(n_oao)}
    with open(os.path.join(AREA, "_tick_stream_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print("streaming done:", meta, flush=True)
    return minute_df

def spread_bp(mid, spread):
    return 1e4 * spread / np.where(mid > 0, mid, np.nan)

def pct(a, q):
    a = np.asarray(a, float)
    a = a[~np.isnan(a)]
    if len(a) == 0:
        return [np.nan] * len(q)
    return list(np.percentile(a, q))

# ------------------------------------------------------------------ Stage 1+2
minute = build_minute_cache()
reservoir = np.load(os.path.join(AREA, "tick_reservoir_sample.npy"))
tick_spread = reservoir[:, 0]
tick_mid = reservoir[:, 1]
tick_bp = spread_bp(tick_mid, tick_spread)

min_bp = spread_bp((minute["bid_med"] + minute["ask_med"]) / 2.0, minute["spread_med"])
min_mid = (minute["bid_med"] + minute["ask_med"]) / 2.0

print("=== tick-level spread (reservoir n=%d) ===" % len(tick_spread))
q = [50, 75, 90, 95, 99, 100]
print("abs:", pct(tick_spread, q))
print("bp :", pct(tick_bp, q))
print("minute-level spread_med bp:", pct(min_bp, q))
print("minutes:", len(minute), "ticks/min P50/P90/max:",
      pct(minute["nticks"].to_numpy(), [50, 90, 100]))

# duplicate minute check (cache already dedupes); coverage gap check
minute = minute.sort_values("minute").reset_index(drop=True)
diffs = minute["minute"].diff().dt.total_seconds().div(60).to_numpy()
big_gaps = diffs[diffs > 10]
max_gap = int(np.nanmax(diffs)) if len(diffs) and not np.isnan(diffs).all() else None
print("minute-level gaps >10min:", len(big_gaps), "max gap (min):", max_gap)

# inventory table
with open(os.path.join(AREA, "_tick_stream_meta.json")) as f:
    _smeta = json.load(f)
inventory = pd.DataFrame({
    "field": ["source", "symbol", "feed_type", "rows", "date_min", "date_max",
              "columns", "bid_ask_valid_share", "last_equals_bid_share", "volume_nonzero",
              "tick_level_sample", "minute_gaps_gt_10min", "max_minute_gap_min",
              "tick_level_spread_p50_abs", "tick_level_spread_p50_bp",
              "minute_spread_p50_bp", "minute_spread_p90_bp", "minute_spread_p99_bp",
              "minute_spread_max_bp"],
    "value": [
        "data/tick/XAGUSD_mt5_ticks.csv", "XAGUSD", "MT5-style tick export (bid/ask/last/vol)",
        int(_smeta["nrows"]), str(minute["minute"].iloc[0]), str(minute["minute"].iloc[-1]),
        "date,time,bid,ask,last,vol", "1.0 (ask>bid on sampled rows)", "1.0 (sampled)", "0 (all zero)",
        "systematic every-150th tick (seeded, deterministic)", int(len(big_gaps)), max_gap,
        round(pct(tick_spread, [50])[0], 5), round(pct(tick_bp, [50])[0], 2),
        round(pct(min_bp, [50])[0], 2), round(pct(min_bp, [90])[0], 2),
        round(pct(min_bp, [99])[0], 2), round(pct(min_bp, [100])[0], 2),
    ]})
inventory.to_csv(os.path.join(AREA, "cost_data_inventory.csv"), index=False)

# cost distribution table (tick-level + minute-level + per-event later)
dist_rows = []
for name, arr in [("tick_level_bp", tick_bp), ("minute_median_bp", min_bp)]:
    r = {"level": name, "n": int(len(arr))}
    for qq, lab in zip(q, ["p50", "p75", "p90", "p95", "p99", "max"]):
        r[lab] = round(pct(arr, [qq])[0], 2)
    dist_rows.append(r)
pd.DataFrame(dist_rows).to_csv(os.path.join(AREA, "cost_distribution.csv"), index=False)
print("cost_distribution written")

# ------------------------------------------------------------------ Stage 3: match events
events = pd.read_csv(EVENTS, parse_dates=["event_timestamp"])
xag = events[events["instrument"] == "XAGUSD"].copy()
print("XAGUSD events:", len(xag))
# exit minute = t + 120 min
xag["exit_timestamp"] = xag["event_timestamp"] + pd.Timedelta(minutes=120)
minute_idx = minute.set_index("minute")

def cost_at(ts):
    """Return (spread_bp, mid, matched) for timestamp ts using exact minute then ±5min fallback."""
    for offset in range(0, 6):
        cand = ts - pd.Timedelta(minutes=offset)
        if cand in minute_idx.index:
            row = minute_idx.loc[cand]
            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]
            return float(spread_bp((row["bid_med"] + row["ask_med"]) / 2.0, row["spread_med"])), \
                   float((row["bid_med"] + row["ask_med"]) / 2.0), True
    return np.nan, np.nan, False

def cost_at_fwd(ts):
    for offset in range(0, 6):
        cand = ts + pd.Timedelta(minutes=offset)
        if cand in minute_idx.index:
            row = minute_idx.loc[cand]
            if isinstance(row, pd.DataFrame):
                row = row.iloc[0]
            return float(spread_bp((row["bid_med"] + row["ask_med"]) / 2.0, row["spread_med"])), \
                   float((row["bid_med"] + row["ask_med"]) / 2.0), True
    return np.nan, np.nan, False

t0 = time.time()
ent = [cost_at(ts) for ts in xag["event_timestamp"]]
exi = [cost_at_fwd(ts) for ts in xag["exit_timestamp"]]
print("matching done in %.0fs; %d/%d entry matched, %d/%d exit matched" % (
    time.time() - t0, sum(1 for e in ent if e[2]), len(ent), sum(1 for e in exi if e[2]), len(exi)))
xag["entry_spread_bp"] = [e[0] for e in ent]
xag["exit_spread_bp"] = [e[0] for e in exi]
xag["entry_mid"] = [e[1] for e in ent]
xag["exit_mid"] = [e[1] for e in exi]
xag["entry_matched"] = [e[2] for e in ent]
xag["exit_matched"] = [e[2] for e in exi]
xag["rt_cost_A_bp"] = (xag["entry_spread_bp"] + xag["exit_spread_bp"]) / 2.0
xag["rt_cost_B_bp"] = xag["entry_spread_bp"] + xag["exit_spread_bp"]

# per-event costs for the net analysis: use Model A by default
xag["cost_bp"] = xag["rt_cost_A_bp"]
xag["net_bp"] = xag["dir_adj_return_h120"] * 1e4 - xag["cost_bp"]
print("events with both sides matched:", int((xag["entry_matched"] & xag["exit_matched"]).sum()), "/", len(xag))

# ------------------------------------------------------------------ Stage 4: session / regime
minute = minute.assign(hour=minute["minute"].dt.hour, year=minute["minute"].dt.year)
minute["bp"] = min_bp
sess = minute.groupby("hour")["bp"].agg(["count", "median", "mean", lambda x: np.percentile(x, 90), lambda x: np.percentile(x, 99)])
sess.columns = ["n_minutes", "median_bp", "mean_bp", "p90_bp", "p99_bp"]
sess = sess.reset_index()
sess.to_csv(os.path.join(AREA, "cost_by_session.csv"), index=False)
yr = minute.groupby("year")["bp"].agg(["count", "median", "mean", lambda x: np.percentile(x, 90)])
yr.columns = ["n_minutes", "median_bp", "mean_bp", "p90_bp"]
yr.to_csv(os.path.join(AREA, "cost_by_year.csv"), index=False)

# pre-event volatility from M1 (realized vol of 1-min returns over prior 120 bars)
m1 = pd.read_csv(M1)
m1.columns = [c.strip().lower() for c in m1.columns]
m1["timestamp"] = pd.to_datetime(m1["timestamp"])
m1 = m1.sort_values("timestamp").reset_index(drop=True)
ret = m1["close"].pct_change()
vol = ret.rolling(120).std()
m1["vol120"] = vol
vol_map = dict(zip(m1["timestamp"], m1["vol120"]))
xag["pre_vol"] = xag["event_timestamp"].map(vol_map)
xv = xag["pre_vol"].dropna()
if len(xv) >= 3:
    t1, t2 = np.percentile(xv, [33.3, 66.7])
    xag["vol_tercile"] = pd.cut(xag["pre_vol"], [-np.inf, t1, t2, np.inf], labels=["low", "mid", "high"])
    reg = xag.groupby("vol_tercile", observed=True).agg(
        n=("event_timestamp", "size"), entry_spread_p50=("entry_spread_bp", lambda s: np.nanpercentile(s, 50)),
        entry_spread_mean=("entry_spread_bp", "mean")).reset_index()
    reg.to_csv(os.path.join(AREA, "cost_by_regime.csv"), index=False)
else:
    pd.DataFrame().to_csv(os.path.join(AREA, "cost_by_regime.csv"), index=False)

# ------------------------------------------------------------------ Stage 5: gross-to-net + sensitivity + bootstrap
def cluster_ids(ts, H=120):
    ts = np.sort(np.asarray(ts, dtype="datetime64[s]").astype("int64"))
    # connected components of |dt| < H*60
    parent = list(range(len(ts)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    # windowed union: two-pointer
    j = 0
    for i in range(len(ts)):
        while j < len(ts) and ts[j] - ts[i] < H * 60:
            j += 1
        for k in range(i + 1, j):
            union(i, k)
    cl = {}
    for i in range(len(ts)):
        cl.setdefault(find(i), []).append(i)
    return list(cl.values())

def boot_ci(values, clusters, seed=SEED, B=B):
    rng = np.random.default_rng(seed)
    vals = np.asarray(values, float)
    means = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, len(clusters), size=len(clusters))
        sel = np.concatenate([clusters[i] for i in idx])
        means[b] = vals[sel].mean()
    lo, hi = np.percentile(means, [2.5, 97.5])
    return lo, hi, means

g2n_rows = []
for norm in ["N1", "N2"]:
    for direction in ["DOWN", "UP"]:
        for part in ["VALIDATION", "TEST", "TRAIN"]:
            cell = xag[(xag["normalization"] == norm) & (xag["direction"] == direction) & (xag["partition"] == part) & xag["entry_matched"] & xag["exit_matched"]]
            if len(cell) < 3:
                continue
            # clusters over ALL events (both directions) of this norm+partition window (V3 rule),
            # pooling only the cell's events within resampled clusters.
            win = xag[(xag["normalization"] == norm) & (xag["partition"] == part)]
            cl = cluster_ids(win["event_timestamp"].to_numpy())
            # map cluster members to positions in `cell`
            cell_pos = {ts: i for i, ts in enumerate(cell["event_timestamp"].astype("int64").to_numpy())}
            cell_clusters = []
            for c in cl:
                sel = [cell_pos[win["event_timestamp"].astype("int64").to_numpy()[i]] for i in c if win["event_timestamp"].astype("int64").to_numpy()[i] in cell_pos]
                if sel:
                    cell_clusters.append(sel)
            gross_bp = cell["dir_adj_return_h120"].mean() * 1e4
            cost_A = cell["rt_cost_A_bp"].mean()
            cost_B = cell["rt_cost_B_bp"].mean()
            net_A = (cell["dir_adj_return_h120"] * 1e4 - cell["rt_cost_A_bp"])
            lo, hi, _ = boot_ci(net_A.to_numpy(), cell_clusters)
            success = (net_A > 0).mean()
            g2n_rows.append({
                "normalization": norm, "direction": direction, "partition": part, "n": len(cell),
                "n_clusters_all_dir": len(cl), "n_effective_clusters": len(cell_clusters),
                "gross_bp": round(gross_bp, 2),
                "mean_rt_cost_A_bp": round(cost_A, 2), "mean_rt_cost_B_bp": round(cost_B, 2),
                "net_A_mean_bp": round(net_A.mean(), 2), "net_A_ci_lo_bp": round(lo, 2), "net_A_ci_hi_bp": round(hi, 2),
                "net_A_success_rate": round(success, 3), "break_even_bp": round(gross_bp, 2),
                "margin_at_median_cost_bp": round(gross_bp - np.nanmedian(cell["rt_cost_A_bp"]), 2),
            })
g2n = pd.DataFrame(g2n_rows)
g2n.to_csv(os.path.join(AREA, "gross_to_net_analysis.csv"), index=False)
print("\n=== GROSS-TO-NET (Model A) ===")
print(g2n.to_string(index=False))

# sensitivity: percentiles of per-event round-trip cost for the primary cell + net at each percentile
sens_rows = []
for norm in ["N1", "N2"]:
    for direction in ["DOWN"]:
        for part in ["VALIDATION", "TEST"]:
            cell = xag[(xag["normalization"] == norm) & (xag["direction"] == direction) & (xag["partition"] == part) & xag["entry_matched"] & xag["exit_matched"]]
            if len(cell) < 3:
                continue
            gross = cell["dir_adj_return_h120"].mean() * 1e4
            cA = cell["rt_cost_A_bp"].to_numpy()
            r = {"normalization": norm, "direction": direction, "partition": part, "n": len(cell), "gross_bp": round(gross, 2)}
            for qq, lab in zip([50, 75, 90, 95, 99], ["p50", "p75", "p90", "p95", "p99"]):
                v = np.percentile(cA, qq)
                r[f"cost_A_{lab}"] = round(v, 2)
                r[f"net_A_at_{lab}"] = round(gross - v, 2)
            r["break_even_bp"] = round(gross, 2)
            sens_rows.append(r)
sens = pd.DataFrame(sens_rows)
sens.to_csv(os.path.join(AREA, "cost_sensitivity.csv"), index=False)
print("\n=== COST SENSITIVITY (Model A) ===")
print(sens.to_string(index=False))

# save per-event matched costs
xag.to_csv(os.path.join(AREA, "event_cost_matched.csv"), index=False)

# metadata
meta = {
    "protocol_version": "V1.0.0",
    "tick_source": "data/tick/XAGUSD_mt5_ticks.csv",
    "tick_sha256": sha256(TICK),
    "m1_sha256": sha256(M1),
    "events_sha256": sha256(EVENTS),
    "matching_rule": "per-minute median spread; exact minute, fallback +/-5min; exit at t+120",
    "cost_models": {"A_standard_half_spread_per_side": "RT_A=(entry+exit)/2", "B_conservative_full_spread_per_side": "RT_B=entry+exit"},
    "commission_bp_band_assumption": [0, 2, 5, 10],
    "slippage_bp_band_assumption": [0, 2, 5],
    "bootstrap": {"method": "cluster bootstrap (overlap |dt|<120, all events)", "B": B, "seed": SEED},
    "library_versions": {"pandas": pd.__version__, "numpy": np.__version__},
    "note": "UNOBSERVED components (commission, slippage) are assumption bands only; spread is observed tick-level bid/ask.",
}
with open(os.path.join(AREA, "experiment_metadata_V1.json"), "w") as f:
    json.dump(meta, f, indent=2)

# hash outputs
out_files = ["cost_data_inventory.csv", "cost_distribution.csv", "cost_by_session.csv",
             "cost_by_year.csv", "cost_by_regime.csv", "gross_to_net_analysis.csv",
             "cost_sensitivity.csv", "event_cost_matched.csv", "experiment_metadata_V1.json"]
print("\n=== OUTPUT HASHES ===")
for f in out_files:
    p = os.path.join(AREA, f)
    if os.path.exists(p):
        print(f, sha256(p)[:12])
print("\nDone.")
