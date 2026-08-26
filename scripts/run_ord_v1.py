#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUANTFORGE — ORD (Opening-Range Directional Break) V1.1.0 CONTROLLED EXECUTION
Protocol: output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md
SHA-256:  85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06
V1.0.0 Audit: PASS — APPROVED FOR ORD MULTI-MARKET EXECUTION
V1.1.0 Amendment: AMEND-DENOM-1 (denominator); detection boundary corrected
Seed:     20260818 | B = 10,000 | L = 10 (p=0.1 terminate / 0.9 continue) | alpha = 0.05

Frozen parameters (no tuning, no alternatives):
  - Opening windows (America/New_York, inclusive): XAU/XAG/BTC 03:00:00-03:29:59;
    USATECHIDXUSD 09:30:00-09:59:59. Exactly 30 M1 bars; valid OHLC; W > 0.
  - Breakout: first close strictly beyond the edge through 17:00:00 ET, per direction.
  - Entry: breakout-candle close. Control: penetration without qualifying close-break;
    sign = attempt direction (upper -> hypothetical long).
  - Response: bp directional return from entry/anchor close to the complete 120-min
    horizon close. Incomplete horizon -> excluded before inference.
  - Statistic: DeltaM = median(treatment) - median(control); np.median convention.
  - Bootstrap: day-cluster stationary; geometric blocks p=0.1; circular wrap;
    truncate to exactly N; B=10,000; seed 20260818 (fresh Generator per market).
  - Null: DeltaM*_null = DeltaM* - DeltaM_obs; p = (1+count)/(1+B_valid), inclusive >=.
  - CI: ordinary 2.5/97.5 percentiles of DeltaM* draws. Holm step-down alpha=0.05.
  - Evaluability: >=100 treatment events; finite treatment+control.
  - Invalid-day fraction > 10% -> HALT (per protocol s.20).
This is the ONE authorized execution. No adjudication is performed here.
"""

import csv
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

PROTOCOL_PATH = Path("output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_V1_AMENDED.md")
DEFLOCK_PATH = Path("output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md")
AUDIT_PATH = Path("output/research_discovery/ORD_OPENING_RANGE_EVENT_STUDY_PROTOCOL_AUDIT_V1.md")

PROTOCOL_SHA = "85263b848e49e718a099cafe8fa7fe6f8ae0c74ec04c46477a0fcd1d9e759c06"
SEED = 20260818
B = 10_000
ALPHA = 0.05
MIN_TREATMENT = 100
HALT_FRACTION = 0.10
HORIZON_MIN = 120
ET = ZoneInfo("America/New_York")

MARKETS = {
    "XAUUSD": {"start": 3 * 60, "end": 3 * 60 + 29},        # 03:00:00-03:29:59 ET
    "XAGUSD": {"start": 3 * 60, "end": 3 * 60 + 29},
    "BTCUSD": {"start": 3 * 60, "end": 3 * 60 + 29},
    "USATECHIDXUSD": {"start": 9 * 60 + 30, "end": 9 * 60 + 59},  # 09:30:00-09:59:59 ET
}
DETECT_END = 17 * 60  # 17:00:00 ET inclusive

DATA_HASHES = {
    "XAUUSD_M1.csv": "54cf61559673adc7f6917f086bd4ef8d71808c3834f2faa82cd9323ee119311c",
    "XAGUSD_M1.csv": "69444be954a869ebc831cd1253849222d8babc7a02940b2bb908a5179bcf5999",
    "USATECHIDXUSD_M1.csv": "39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6",
    "BTCUSD_M1.csv": "97b853854d8f650d80e3972f159deab0b15911e19dd437e1dd10b3bab098409b",
}

DATA_DIR = Path("data/m1")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def median_convention(x: np.ndarray) -> float:
    """Frozen median: odd -> middle; even -> mean of the two central. == np.median."""
    return float(np.median(x))


def pre_execution_gate():
    checks = {}
    checks["protocol_exists"] = PROTOCOL_PATH.is_file()
    checks["protocol_sha"] = sha256_file(PROTOCOL_PATH) if PROTOCOL_PATH.is_file() else None
    checks["deflock_exists"] = DEFLOCK_PATH.is_file()
    checks["audit_exists"] = AUDIT_PATH.is_file()
    checks["audit_pass"] = False
    if AUDIT_PATH.is_file():
        txt = AUDIT_PATH.read_text(encoding="utf-8")
        checks["audit_pass"] = "PASS — APPROVED FOR ORD MULTI-MARKET EXECUTION" in txt
    checks["data_hashes"] = {}
    for name, expected in DATA_HASHES.items():
        p = DATA_DIR / name
        actual = sha256_file(p) if p.is_file() else None
        checks["data_hashes"][name] = {"expected": expected, "actual": actual, "ok": actual == expected}
    ok = (
        checks["protocol_exists"]
        and checks["protocol_sha"] == PROTOCOL_SHA
        and checks["deflock_exists"]
        and checks["audit_exists"]
        and checks["audit_pass"]
        and all(v["ok"] for v in checks["data_hashes"].values())
    )
    return checks, ok


def load_market(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}_M1.csv"
    df = pd.read_csv(
        path,
        usecols=["timestamp", "open", "high", "low", "close"],
        dtype={"open": float, "high": float, "low": float, "close": float}
    )
    df["ts"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    df.drop(columns=["timestamp"], inplace=True)
    df.dropna(subset=["ts"], inplace=True)
    df.sort_values("ts", inplace=True)
    df.drop_duplicates(subset="ts", keep="first", inplace=True)
    df.reset_index(drop=True, inplace=True)
    et = df["ts"].dt.tz_localize("UTC").dt.tz_convert(ET)
    df["et_min"] = et.dt.hour * 60 + et.dt.minute
    # Memory-efficient: use datetime64[D] for grouping instead of Python date objects
    # This avoids allocating 2.5M+ Python date objects in memory
    df["date"] = et.dt.floor("D")
    df.rename(columns={"open": "o", "high": "h", "low": "l", "close": "c"}, inplace=True)
    return df


def build_events(df: pd.DataFrame, win_start: int, win_end: int):
    """Deterministic event construction per protocol ss.4-11. Returns (events, diag)."""
    ts_arr = df["ts"].values.astype("datetime64[s]")
    o = df["o"].values
    h = df["h"].values
    l = df["l"].values
    c = df["c"].values
    et_min = df["et_min"].values

    events = []

    # V1.1.0 denominator: dates with >= 1 observation in the detection window
    # (after opening window through 17:00 ET inclusive)
    det_window_mask = (et_min > win_end) & (et_min <= DETECT_END)
    dates_with_det_obs = set(df.loc[det_window_mask, "date"].unique())
    n_total_dates = len(dates_with_det_obs)
    n_invalid_days = 0

    g = df.groupby("date", sort=True)
    for date, grp in g:
        rows = grp.index.values  # positions in df
        emin = et_min[rows]
        wmask = (emin >= win_start) & (emin <= win_end)
        wrows = rows[wmask]
        # Opening-window completeness gate
        win_ok = len(wrows) == 30
        if win_ok:
            wc = c[wrows]
            wo = o[wrows]
            wh = h[wrows]
            wl = l[wrows]
            win_ok = bool(np.all(wo > 0) and np.all(wh > 0) and np.all(wl > 0) and np.all(wc > 0))
            hi_or = float(np.max(wh))
            lo_or = float(np.min(wl))
            win_ok = win_ok and (hi_or > lo_or)
        else:
            hi_or = lo_or = None
        if not win_ok:
            if date in dates_with_det_obs:
                n_invalid_days += 1  # denominator date that fails opening-window gate
            continue  # ineligible day -> no events

        # Event-session completeness: data through 17:00:00 ET required for detection
        det_mask = (emin > win_end) & (emin <= DETECT_END)
        det_pos = np.nonzero(det_mask)[0]
        det_rows = rows[det_pos]
        if len(det_pos) == 0:
            continue  # no detection-window bars -> zero events this day

        dc = c[det_rows]
        dh = h[det_rows]
        dl = l[det_rows]
        # Long side
        long_break_rows = det_rows[dc > hi_or]
        if len(long_break_rows) > 0:
            long_event_row = int(long_break_rows[0])
            long_type = "treatment"
        else:
            long_pen_rows = det_rows[dh > hi_or]
            if len(long_pen_rows) > 0:
                long_event_row = int(long_pen_rows[0])
                long_type = "control"
            else:
                long_event_row = None
                long_type = None
        # Short side
        short_break_rows = det_rows[dc < lo_or]
        if len(short_break_rows) > 0:
            short_event_row = int(short_break_rows[0])
            short_type = "treatment"
        else:
            short_pen_rows = det_rows[dl < lo_or]
            if len(short_pen_rows) > 0:
                short_event_row = int(short_pen_rows[0])
                short_type = "control"
            else:
                short_event_row = None
                short_type = None

        for direction, ev_row, ev_type in (
            ("long", long_event_row, long_type),
            ("short", short_event_row, short_type),
        ):
            if ev_row is None:
                continue
            entry_ts = ts_arr[ev_row]
            entry_close = float(c[ev_row])
            if entry_close <= 0:
                continue
            if direction == "long":
                response_sign = 1.0
                inval_edge = hi_or
            else:
                response_sign = -1.0
                inval_edge = lo_or

            # Horizon: exact bar at entry + 120 min
            target = entry_ts + np.timedelta64(HORIZON_MIN, "m")
            i = int(np.searchsorted(ts_arr, target))
            horizon_complete = i < len(ts_arr) and ts_arr[i] == target and c[i] > 0
            response = None
            horizon_close = None
            if horizon_complete:
                horizon_close = float(c[i])
                if direction == "long":
                    response = (horizon_close - entry_close) / entry_close * 1e4
                else:
                    response = (entry_close - horizon_close) / entry_close * 1e4

            # Invalidation flag (descriptive; response unconditional): close back
            # through the broken edge within [entry+1, entry+120] minutes.
            invalidated = False
            if horizon_complete:
                s0 = int(np.searchsorted(ts_arr, entry_ts + np.timedelta64(1, "m")))
                s1 = i  # horizon bar index inclusive
                if s0 <= s1:
                    win_closes = c[s0 : s1 + 1]
                    if direction == "long":
                        invalidated = bool(np.any(win_closes <= inval_edge))
                    else:
                        invalidated = bool(np.any(win_closes >= inval_edge))

            # MFE from entry over (entry, entry+120] (descriptive secondary)
            mfe = None
            if horizon_complete:
                s0 = int(np.searchsorted(ts_arr, entry_ts + np.timedelta64(1, "m")))
                s1 = i
                if s0 <= s1:
                    if direction == "long":
                        mfe = float((np.max(h[s0 : s1 + 1]) - entry_close) / entry_close * 1e4)
                    else:
                        mfe = float((entry_close - np.min(l[s0 : s1 + 1])) / entry_close * 1e4)

            events.append(
                {
                    "market": None,  # filled by caller
                    "trading_day": str(date),
                    "direction": direction,
                    "type": ev_type,
                    "anchor_ts": str(entry_ts),
                    "entry_close": entry_close,
                    "horizon_close": horizon_close,
                    "response": response,
                    "invalidated": invalidated,
                    "horizon_complete": horizon_complete,
                    "mfe_from_entry": mfe,
                    "range_width": hi_or - lo_or,
                    "range_norm_return": (response / (hi_or - lo_or)) if (response is not None and (hi_or - lo_or) > 0) else None,
                }
            )

    diag = {
        "total_dates": n_total_dates,
        "invalid_days": n_invalid_days,
        "invalid_fraction": (n_invalid_days / n_total_dates) if n_total_dates else 0.0,
    }
    return events, diag


def run_bootstrap(days_treat, days_control, N, seed):
    """Day-cluster stationary bootstrap. Returns (draws, B_valid)."""
    tr = np.full((N, 2), np.nan)
    co = np.full((N, 2), np.nan)
    for d, vals in days_treat.items():
        vals = [v for v in vals if v is not None]
        for k, v in enumerate(vals[:2]):
            tr[d, k] = v
    for d, vals in days_control.items():
        vals = [v for v in vals if v is not None]
        for k, v in enumerate(vals[:2]):
            co[d, k] = v

    rng = np.random.default_rng(seed)
    # Pre-generate a geometric(p=0.1) block-length pool and uniform starts.
    # Per replicate: consume blocks until cumulative length >= N, truncate to N.
    blocks_est = 260
    pool_len = rng.geometric(0.1, size=B * blocks_est).astype(np.int64)
    pool_start = rng.integers(0, N, size=B * blocks_est, dtype=np.int64)
    draws = np.full(B, np.nan)
    idx = 0
    ar = np.arange
    for b in range(B):
        total = 0
        nb = 0
        while total < N:
            total += int(pool_len[idx + nb])
            nb += 1
        sl = pool_start[idx : idx + nb]
        ll = pool_len[idx : idx + nb]
        idx += nb
        m = int(ll.max())
        off = ar(m)[None, :]
        walk = (sl[:, None] + off) % N
        mask = off < ll[:, None]
        seq = walk[mask][:N]
        tvals = np.concatenate([tr[seq, 0], tr[seq, 1]])
        cvals = np.concatenate([co[seq, 0], co[seq, 1]])
        mt = np.nanmedian(tvals)
        mc = np.nanmedian(cvals)
        if np.isnan(mt) or np.isnan(mc):
            continue
        draws[b] = mt - mc
    valid = ~np.isnan(draws)
    B_valid = int(np.sum(valid))
    return draws, B_valid


def main():
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from research.orchestration.event_study_recorder import EventStudyRecorder

    t0 = time.time()
    checks, ok = pre_execution_gate()
    print("[gate]", json.dumps({"ok": ok, "protocol_sha_ok": checks["protocol_sha"] == PROTOCOL_SHA}, default=str))
    if not ok:
        print("PRE-EXECUTION GATE FAILED — STOP")
        sys.exit(2)

    recorder = EventStudyRecorder(
        project_name="ORD",
        protocol_version="V1.1.0",
        protocol_path=PROTOCOL_PATH,
        protocol_sha=PROTOCOL_SHA,
        definition_lock_path=DEFLOCK_PATH,
        input_manifest_hash=DATA_HASHES,
        entry_script_path=Path(__file__).resolve()
    )

    recorder.preflight()

    try:
        recorder.start()
        OUT_DIR = recorder.output_dir

        env_info = {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "seed": SEED,
            "B": B,
            "L": 10,
            "p_terminate": 0.1,
            "alpha": ALPHA,
            "horizon_min": HORIZON_MIN,
            "min_treatment": MIN_TREATMENT,
            "halt_fraction": HALT_FRACTION,
            "protocol_sha": PROTOCOL_SHA,
            "protocol_path": str(PROTOCOL_PATH),
            "execution_start_utc": datetime.now(timezone.utc).isoformat(),
        }
        try:
                env_info["git_head"] = subprocess.run(
                    ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
                ).stdout.strip()
                env_info["git_status_short"] = subprocess.run(
                    ["git", "status", "--short"], capture_output=True, text=True, check=True
                ).stdout.strip()
        except Exception as e:
            env_info["git"] = f"unavailable: {e}"

        market_results = {}
        all_event_rows = []
        halted = []
        import gc
        for mkt, spec in MARKETS.items():
            df = None
            try:
                print(f"[{mkt}] loading ...", flush=True)
                df = load_market(mkt)
                events, diag = build_events(df, spec["start"], spec["end"])
                for e in events:
                    e["market"] = mkt
                all_event_rows.extend(events)
                print(f"[{mkt}] total_dates={diag['total_dates']} invalid_days={diag['invalid_days']} "
                      f"invalid_fraction={diag['invalid_fraction']:.4f} events_raw={len(events)}", flush=True)
                if diag["invalid_fraction"] > HALT_FRACTION:
                    halted.append(mkt)
                    market_results[mkt] = {"halted": True, "diag": diag}
                    continue

                # Eligible events only (complete horizon) for inference
                elig = [e for e in events if e["horizon_complete"] and e["response"] is not None]
                n_treat = sum(1 for e in elig if e["type"] == "treatment")
                n_control = sum(1 for e in elig if e["type"] == "control")
                # Day clusters (chronological)
                day_order = sorted({e["trading_day"] for e in elig})
                N = len(day_order)
                day_idx = {d: i for i, d in enumerate(day_order)}
                days_treat = {}
                days_control = {}
                for e in elig:
                    di = day_idx[e["trading_day"]]
                    (days_treat if e["type"] == "treatment" else days_control).setdefault(di, []).append(e["response"])

                treat_all = np.array([e["response"] for e in elig if e["type"] == "treatment"])
                control_all = np.array([e["response"] for e in elig if e["type"] == "control"])
                dm_obs = median_convention(treat_all) - median_convention(control_all)

                draws, B_valid = run_bootstrap(days_treat, days_control, N, SEED)
                valid_draws = draws[~np.isnan(draws)]
                null_draws = valid_draws - dm_obs
                count = int(np.sum(np.abs(null_draws) >= abs(dm_obs)))
                p_raw = (1 + count) / (1 + B_valid)
                ci = (float(np.percentile(valid_draws, 2.5)), float(np.percentile(valid_draws, 97.5)))

                # Secondaries (descriptive)
                inv_rate = None
                mfe_med = None
                rn_med = None
                if n_treat > 0:
                    inv_rate = sum(1 for e in elig if e["type"] == "treatment" and e["invalidated"]) / n_treat
                    mfe_med = float(np.median([e["mfe_from_entry"] for e in elig if e["type"] == "treatment"]))
                    rn_vals = [e["range_norm_return"] for e in elig if e["type"] == "treatment" and e["range_norm_return"] is not None]
                    if rn_vals:
                        rn_med = float(np.median(rn_vals))
                # Halves by floor(N/2) eligible event days
                half1_days = set(day_order[: N // 2])
                half2_days = set(day_order[N // 2 :])
                def half_dm(hd):
                    ht = [e["response"] for e in elig if e["type"] == "treatment" and e["trading_day"] in hd]
                    hc = [e["response"] for e in elig if e["type"] == "control" and e["trading_day"] in hd]
                    if ht and hc:
                        return median_convention(np.array(ht)) - median_convention(np.array(hc))
                    return None
                half1 = half_dm(half1_days)
                half2 = half_dm(half2_days)
                years = {}
                for e in elig:
                    y = e["trading_day"][:4]
                    years.setdefault(y, {"t": [], "c": []})
                    years[y]["t" if e["type"] == "treatment" else "c"].append(e["response"])
                year_dm = {}
                for y, d in sorted(years.items()):
                    if d["t"] and d["c"]:
                        year_dm[y] = median_convention(np.array(d["t"])) - median_convention(np.array(d["c"]))

                evaluable = n_treat >= MIN_TREATMENT and n_treat > 0 and n_control > 0 and B_valid >= 1
                market_results[mkt] = {
                    "halted": False,
                    "diag": diag,
                    "n_treatment": n_treat,
                    "n_control": n_control,
                    "N_days": N,
                    "evaluable": evaluable,
                    "deltaM_obs": dm_obs,
                    "median_treatment": float(median_convention(treat_all)) if len(treat_all) else None,
                    "median_control": float(median_convention(control_all)) if len(control_all) else None,
                    "B_valid": B_valid,
                    "p_raw": p_raw if (evaluable and B_valid >= 1) else None,
                    "ci_95": list(ci) if B_valid >= 1 else None,
                    "p_holm": None,
                    "classification": None,
                    "invalid_rate_treatment": inv_rate,
                    "mfe_median_treatment": mfe_med,
                    "range_norm_median_treatment": rn_med,
                    "half1_dm": half1,
                    "half2_dm": half2,
                    "year_dm": year_dm,
                    "n_long_treatment": sum(1 for e in elig if e["type"] == "treatment" and e["direction"] == "long"),
                    "n_short_treatment": sum(1 for e in elig if e["type"] == "treatment" and e["direction"] == "short"),
                    "n_long_control": sum(1 for e in elig if e["type"] == "control" and e["direction"] == "long"),
                    "n_short_control": sum(1 for e in elig if e["type"] == "control" and e["direction"] == "short"),
                }
                print(f"[{mkt}] n_treat={n_treat} n_control={n_control} N_days={N} B_valid={B_valid} "
                      f"deltaM_obs={dm_obs:.4f} p_raw={market_results[mkt]['p_raw']}", flush=True)

                # Persist draws / null draws (protocol s.26: must be written to disk)
                np.save(OUT_DIR / f"bootstrap_{mkt}.npy", draws)
                null_full = np.full(B, np.nan)
                null_full[~np.isnan(draws)] = draws[~np.isnan(draws)] - dm_obs
                np.save(OUT_DIR / f"null_{mkt}.npy", null_full)

            finally:
                if df is not None:
                    del df
                gc.collect()

        # Holm across evaluable markets
        fam = [m for m, r in market_results.items() if not r.get("halted") and r.get("evaluable")]
        if fam:
            ps = np.array([market_results[m]["p_raw"] for m in fam])
            order = np.argsort(ps)
            m_count = len(fam)
            adj = np.minimum(1.0, (m_count - np.arange(m_count)) * ps[order])
            adj = np.maximum.accumulate(adj)
            for rank, mi in enumerate(order):
                market_results[fam[mi]]["p_holm"] = float(adj[rank])
                ph = adj[rank]
                dm = market_results[fam[mi]]["deltaM_obs"]
                if ph < ALPHA and dm > 0:
                    market_results[fam[mi]]["classification"] = "SUPPORT"
                elif ph < ALPHA and dm < 0:
                    market_results[fam[mi]]["classification"] = "CONTRADICTED"
                else:
                    market_results[fam[mi]]["classification"] = "INCONCLUSIVE"
        for m, r in market_results.items():
            if not r.get("halted") and not r.get("evaluable"):
                r["classification"] = "EVIDENCE-LIMITED"

        # Persist event table
        event_path = OUT_DIR / "event_table_all_markets.csv"
        with open(event_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=[
                "market", "trading_day", "direction", "type", "anchor_ts", "entry_close",
                "horizon_close", "response", "invalidated", "horizon_complete",
                "mfe_from_entry", "range_width", "range_norm_return",
            ])
            w.writeheader()
            for e in sorted(all_event_rows, key=lambda x: (x["market"], x["trading_day"], x["direction"])):
                w.writerow({k: ("" if v is None else v) for k, v in e.items()})

        # Persist stats + metadata
        stats_path = OUT_DIR / "statistics.json"
        with open(stats_path, "w", encoding="utf-8") as f:
            json.dump(market_results, f, indent=2, default=str)

        metadata_path = OUT_DIR / "metadata.json"
        artifact_hashes = {}
        for p in sorted(OUT_DIR.iterdir()):
            if p.is_file():
                artifact_hashes[p.name] = sha256_file(p)
        metadata = {
            **env_info,
            "execution_end_utc": datetime.now(timezone.utc).isoformat(),
            "execution_duration_s": round(time.time() - t0, 1),
            "market_order": list(MARKETS.keys()),
            "halted_markets": halted,
            "artifact_sha256": artifact_hashes,
        }
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, default=str)

        # Recompute artifact hashes including metadata, update metadata with its own hash
        artifact_hashes[metadata_path.name] = sha256_file(metadata_path)
        metadata["artifact_sha256"] = artifact_hashes
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, default=str)

        print(json.dumps({m: {k: r.get(k) for k in ("halted", "n_treatment", "n_control", "evaluable",
                                                    "deltaM_obs", "p_raw", "p_holm", "classification")}
                          for m, r in market_results.items()}, indent=1))
        print("ARTIFACTS:", sorted(p.name for p in OUT_DIR.iterdir() if p.is_file()))
    except MemoryError as exc:
        recorder.interrupt_execution(reason="MemoryError during execution")
        raise
    except Exception as exc:
        recorder.invalidate_execution(reason=str(exc))
        raise

    # Declare final artifact contract based on actual completion status
    scientific_expected = [
        "event_table_all_markets.csv",
        "metadata.json",
        "statistics.json",
    ]
    market_status = {}
    for mkt in MARKETS:
        if mkt in halted:
            market_status[mkt] = "HALTED"
        else:
            market_status[mkt] = "COMPLETED"
            scientific_expected.append(f"bootstrap_{mkt}.npy")
            scientific_expected.append(f"null_{mkt}.npy")

    recorder.set_final_artifact_contract(
        expected_scientific_artifacts=scientific_expected,
        market_status=market_status
    )
    recorder.complete_execution()
    print("EXECUTION COMPLETE — adjudication NOT performed.")


if __name__ == "__main__":
    main()
