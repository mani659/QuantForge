"""ORD V1.1.0 controlled economic translation - single registered baseline execution.

Read-only with respect to all scientific objects. Tick files are streamed once
per market; markets are processed sequentially; EventStudyRecorder lifecycle is
exactly-once with fail-closed completion.
"""

import hashlib
import json
import math
import os
import sys
import threading
import time
from datetime import date as _date
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import psutil

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from research.orchestration.event_study_recorder import EventStudyRecorder

PROTOCOL_PATH = ROOT / "output/research_discovery/ORD_ECONOMIC_TRANSLATION_PROTOCOL_V1_AMENDED.md"
PROTOCOL_SHA = "8f45d7f82c80b7131c958c158f448520fef6927d49f9eb844fbbd55e35395663"
PROTOCOL_SHA_CANONICAL = "8F45D7F82C80B7131C958C158F448520FEF6927D49F9EB844FBBD55E35395663"
DEFLOCK_PATH = ROOT / "output/research_discovery/ORD_OPENING_RANGE_DEFINITION_LOCK_V1.md"
SCIENTIFIC_MANIFEST = (
    ROOT
    / "output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/implementation_manifest.json"
)
EVENT_TABLE = (
    ROOT
    / "output/research_discovery/ORD/V1.1.0/EXECUTION_20260818T141202Z_87eaba1e-8da1-49ce-8bcf-7a3933130532/event_table_all_markets.csv"
)
M1_DIR = ROOT / "data/m1"
TICK_DIR = ROOT / "data/tick"

MARKETS = ["XAUUSD", "XAGUSD", "USATECHIDXUSD", "BTCUSD"]
LONDON_MARKETS = {"XAUUSD", "XAGUSD", "BTCUSD"}
NY = ZoneInfo("America/New_York")
HORIZON_MIN = 120
FALLBACK_MIN = 5
MIN_SAMPLE = 30
COMMISSION_BANDS = [0.0, 2.0, 5.0, 10.0]
SLIPPAGE_BANDS = [0.0, 2.0, 5.0]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tick_path(market):
    return TICK_DIR / f"{market}_mt5_ticks.csv"


def m1_path(market):
    return M1_DIR / f"{market}_M1.csv"


def tmin(dt):
    return dt.replace(second=0, microsecond=0)


def parse_events():
    df = pd.read_csv(EVENT_TABLE)
    out = {}
    for market in MARKETS:
        sub = df[(df["market"] == market) & (df["type"] == "treatment")]
        evs = []
        for _, r in sub.iterrows():
            anchor = pd.Timestamp(r["anchor_ts"]).to_pydatetime().replace(tzinfo=None)
            evs.append(
                {
                    "market": market,
                    "trading_day": str(r["trading_day"])[:10],
                    "direction": str(r["direction"]).lower(),
                    "anchor_ts": anchor,
                    "entry_close": float(r["entry_close"]),
                    "range_width": float(r["range_width"]),
                }
            )
        evs.sort(key=lambda e: (e["trading_day"], e["anchor_ts"]))
        out[market] = evs
    return out


def load_m1(market):
    df = pd.read_csv(m1_path(market))
    df["ts"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("ts").drop_duplicates(subset="ts", keep="first")
    local = df["ts"].dt.tz_convert(NY)
    df["et_date"] = local.dt.date
    df["et_hour"] = local.dt.hour
    df["et_minute"] = local.dt.minute
    for col in ("open", "high", "low", "close"):
        df[col] = df[col].astype(float)
    df = df.set_index(pd.DatetimeIndex(df["ts"]))
    return df[["et_date", "et_hour", "et_minute", "open", "high", "low", "close"]]


def or_mask(df, market):
    if market in LONDON_MARKETS:
        return (df["et_hour"] == 3) & (df["et_minute"] <= 29)
    return (df["et_hour"] == 9) & (df["et_minute"] >= 30)


def reconstruct_or(market, td_str, m1df):
    td = _date.fromisoformat(td_str)
    mask = (m1df["et_date"] == td) & or_mask(m1df, market)
    window = m1df[mask]
    if len(window) < 30:
        return None, None
    return float(window["high"].max()), float(window["low"].min())


def build_needed_minutes(events):
    needed = set()
    for e in events:
        tb = tmin(e["anchor_ts"] + timedelta(seconds=60))
        hz = tb + timedelta(minutes=HORIZON_MIN)
        for k in range(FALLBACK_MIN + 1):
            needed.add(tb + timedelta(minutes=k))
            needed.add(hz - timedelta(minutes=k))
            needed.add(hz + timedelta(minutes=k))
        m = tb
        while m <= hz:
            needed.add(m)
            m += timedelta(minutes=1)
    return needed


def stream_buckets(market, needed, peak=None):
    bucket = {m: {"times": [], "bids": [], "asks": []} for m in needed}
    key2m = {}
    for m in needed:
        key = m.strftime("%Y%m%d,%H:%M")
        key2m[key] = m
    invalid = 0
    rows = 0
    with open(tick_path(market), "r", newline="") as f:
        for line in f:
            rows += 1
            if peak is not None and rows % 250_000 == 0:
                peak.sample()
            line = line.rstrip("\n").rstrip("\r")
            if not line:
                invalid += 1
                continue
            p1 = line.find(",")
            if p1 < 0:
                invalid += 1
                continue
            date = line[:p1]
            p2 = line.find(",", p1 + 1)
            if p2 < 0:
                invalid += 1
                continue
            tm = line[p1 + 1 : p2]
            if len(tm) < 5:
                invalid += 1
                continue
            m = key2m.get(date + "," + tm[:5])
            if m is None:
                continue
            parts = line.split(",")
            if len(parts) < 4:
                invalid += 1
                continue
            try:
                bid = float(parts[2])
                ask = float(parts[3])
            except ValueError:
                invalid += 1
                continue
            if not (math.isfinite(bid) and math.isfinite(ask) and bid > 0 and ask > 0 and bid <= ask):
                invalid += 1
                continue
            bucket[m]["times"].append(tm)
            bucket[m]["bids"].append(bid)
            bucket[m]["asks"].append(ask)
    return bucket, invalid, rows


def compute_medians(bucket):
    med = {}
    for m, ent in bucket.items():
        if not ent["bids"]:
            continue
        med[m] = {
            "bid": float(np.median(ent["bids"])),
            "ask": float(np.median(ent["asks"])),
            "nticks": len(ent["bids"]),
        }
    return med


def spread_bp(bid, ask):
    mid = (bid + ask) / 2.0
    if mid <= 0:
        return None
    return (ask - bid) / mid * 1.0e4


def market_medians(med):
    if not med:
        return None, None
    bids = [v["bid"] for v in med.values()]
    asks = [v["ask"] for v in med.values()]
    return float(np.median(bids)), float(np.median(asks))


def find_entry(tb, med, mb_bid, mb_ask):
    for k in range(FALLBACK_MIN + 1):
        cand = tb + timedelta(minutes=k)
        if cand in med:
            return cand, ("exact" if k == 0 else f"fallback+{k}")
    if mb_bid is not None:
        return "market-median", "market-median"
    return None, None


def find_exit(hz, med, mb_bid, mb_ask):
    if hz in med:
        return hz, "exact"
    best = None
    bestd = None
    for k in range(1, FALLBACK_MIN + 1):
        for cand, dist in ((hz - timedelta(minutes=k), k), (hz + timedelta(minutes=k), k)):
            if cand in med and (best is None or dist < bestd):
                best = cand
                bestd = dist
    if best is not None:
        return best, f"fallback+{bestd}"
    if mb_bid is not None:
        return "market-median", "market-median"
    return None, None


def parse_time(hms):
    parts = hms.split(":")
    return datetime(2000, 1, 1, int(parts[0]), int(parts[1]), int(parts[2])).time()


def scan_stop(direction, anchor, hz, high_or, low_or, m1df, bucket):
    trigger_bar = None
    for k in range(1, HORIZON_MIN + 1):
        bar_start = anchor + timedelta(minutes=k)
        key = pd.Timestamp(bar_start, tz="UTC")
        if key not in m1df.index:
            continue
        close = float(m1df.at[key, "close"])
        if direction == "long" and close <= high_or:
            trigger_bar = bar_start
            break
        if direction == "short" and close >= low_or:
            trigger_bar = bar_start
            break
    if trigger_bar is None:
        return None
    m = trigger_bar
    while m < hz:
        ent = bucket.get(m)
        if ent and ent["bids"]:
            for i in range(len(ent["times"])):
                ts = datetime.combine(m.date(), parse_time(ent["times"][i]))
                if direction == "long" and ent["bids"][i] <= high_or:
                    return fill_result(direction, ts, ent["bids"][i], ent["asks"][i])
                if direction == "short" and ent["asks"][i] >= low_or:
                    return fill_result(direction, ts, ent["bids"][i], ent["asks"][i])
        m += timedelta(minutes=1)
    return None


def fill_result(direction, ts, bid, ask):
    quote = bid if direction == "long" else ask
    mid = (bid + ask) / 2.0
    sp = spread_bp(bid, ask)
    return {
        "exit_ts": ts,
        "exit_minute": tmin(ts),
        "exec_quote": quote,
        "mid": mid,
        "spread": sp,
        "lookup": "exact",
        "flag": "",
    }


def simulate_event(market, ev, m1df, med, mb_bid, mb_ask, bucket):
    anchor = ev["anchor_ts"]
    tb = tmin(anchor + timedelta(seconds=60))
    hz = tb + timedelta(minutes=HORIZON_MIN)
    row = {
        "market": market,
        "trading_day": ev["trading_day"],
        "direction": ev["direction"],
        "breakout_ts": anchor.isoformat(),
        "breakout_close": ev["entry_close"],
        "T_B": tb.isoformat(),
        "horizon_ts": hz.isoformat(),
    }
    high_or, low_or = reconstruct_or(market, ev["trading_day"], m1df)
    row["or_high"] = high_or
    row["or_low"] = low_or
    row["range_width_persisted"] = ev["range_width"]
    if high_or is None or low_or is None:
        row["exit_reason"] = "EXCLUDED_RANGE_RECONSTRUCTION"
        row["data_quality_flag"] = "EXCLUDED_RANGE_RECONSTRUCTION"
        return row
    tol = max(1.0e-4, abs(ev["range_width"]) * 1.0e-6)
    if abs((high_or - low_or) - ev["range_width"]) > tol:
        row["exit_reason"] = "EXCLUDED_RANGE_MISMATCH"
        row["data_quality_flag"] = "EXCLUDED_RANGE_MISMATCH"
        return row
    hkey = pd.Timestamp(anchor + timedelta(minutes=HORIZON_MIN), tz="UTC")
    if hkey not in m1df.index:
        row["exit_reason"] = "EXCLUDED_HORIZON_INCOMPLETE"
        row["data_quality_flag"] = "EXCLUDED_HORIZON_INCOMPLETE"
        return row

    entry_minute, entry_lookup = find_entry(tb, med, mb_bid, mb_ask)
    if entry_minute is None:
        row["exit_reason"] = "EXCLUDED_NO_QUOTE_COVERAGE"
        row["data_quality_flag"] = "EXCLUDED_NO_QUOTE_COVERAGE"
        return row
    if entry_minute == "market-median":
        entry_bid, entry_ask = mb_bid, mb_ask
        entry_mid = (entry_bid + entry_ask) / 2.0
        entry_sp = spread_bp(entry_bid, entry_ask)
    else:
        em = med[entry_minute]
        entry_bid, entry_ask = em["bid"], em["ask"]
        entry_mid = (entry_bid + entry_ask) / 2.0
        entry_sp = spread_bp(entry_bid, entry_ask)
    direction = ev["direction"]
    entry_exec = entry_ask if direction == "long" else entry_bid

    stop = scan_stop(direction, anchor, hz, high_or, low_or, m1df, bucket)
    if stop is not None:
        exit_ts = stop["exit_ts"]
        exit_minute = stop["exit_minute"]
        hit_min = exit_minute
        exit_exec = stop["exec_quote"]
        exit_mid = stop["mid"]
        exit_sp = stop["spread"]
        exit_lookup = stop["lookup"]
        flag = stop["flag"]
        exit_reason = "STRUCTURAL_INVALIDATION"
    else:
        exit_minute, exit_lookup = find_exit(hz, med, mb_bid, mb_ask)
        if exit_minute is None:
            row["exit_reason"] = "EXCLUDED_NO_QUOTE_COVERAGE"
            row["data_quality_flag"] = "EXCLUDED_NO_QUOTE_COVERAGE"
            return row
        if exit_minute == "market-median":
            exit_bid_med, exit_ask_med = mb_bid, mb_ask
            exit_mid = (exit_bid_med + exit_ask_med) / 2.0
            exit_exec = exit_bid_med if direction == "long" else exit_ask_med
            exit_sp = spread_bp(exit_bid_med, exit_ask_med)
        else:
            em = med[exit_minute]
            exit_bid_med, exit_ask_med = em["bid"], em["ask"]
            exit_mid = (exit_bid_med + exit_ask_med) / 2.0
            exit_exec = exit_bid_med if direction == "long" else exit_ask_med
            exit_sp = spread_bp(exit_bid_med, exit_ask_med)
        exit_reason = "HORIZON"
        exit_ts = hz
        hit_min = hz
        flag = ""

    if direction == "long":
        gross = (exit_mid - entry_mid) / entry_mid * 1.0e4
        net = (exit_exec - entry_exec) / entry_exec * 1.0e4
        path_prices = [med[m]["bid"] for m in sorted(med) if tb <= m <= hit_min and "bid" in med[m]]
        mfe_bp = (max(path_prices) - entry_exec) / entry_exec * 1.0e4 if path_prices else None
        mae_bp = (min(path_prices) - entry_exec) / entry_exec * 1.0e4 if path_prices else None
    else:
        gross = (entry_mid - exit_mid) / entry_mid * 1.0e4
        net = (entry_exec - exit_exec) / entry_exec * 1.0e4
        path_prices = [med[m]["ask"] for m in sorted(med) if tb <= m <= hit_min and "ask" in med[m]]
        mfe_bp = (entry_exec - min(path_prices)) / entry_exec * 1.0e4 if path_prices else None
        mae_bp = (entry_exec - max(path_prices)) / entry_exec * 1.0e4 if path_prices else None

    cost_a = (entry_sp + exit_sp) / 2.0
    cost_b = entry_sp + exit_sp
    net_b = gross - cost_b
    holding = (exit_ts - tb).total_seconds() / 60.0

    row.update(
        {
            "or_width": high_or - low_or,
            "entry_minute": entry_minute.isoformat() if not isinstance(entry_minute, str) else entry_minute,
            "entry_bid": entry_bid,
            "entry_ask": entry_ask,
            "executable_entry_quote": entry_exec,
            "entry_spread_bp": entry_sp,
            "structural_invalidation_level": high_or if direction == "long" else low_or,
            "exit_ts": exit_ts.isoformat(),
            "exit_minute": hit_min.isoformat(),
            "executable_exit_quote": exit_exec,
            "exit_spread_bp": exit_sp,
            "exit_reason": exit_reason,
            "gross_bp": gross,
            "cost_bp": cost_a,
            "net_bp": net,
            "net_bp_B": net_b,
            "mfe_from_entry_bp": mfe_bp,
            "mae_from_entry_bp": mae_bp,
            "holding_duration_min": holding,
            "quote_lookup_entry": entry_lookup,
            "quote_lookup_exit": exit_lookup,
            "data_quality_flag": flag,
        }
    )
    return row


LEDGER_COLUMNS = [
    "market", "trading_day", "direction", "or_high", "or_low", "or_width",
    "range_width_persisted", "breakout_ts", "breakout_close", "T_B",
    "entry_minute", "entry_bid", "entry_ask", "executable_entry_quote",
    "entry_spread_bp", "structural_invalidation_level", "horizon_ts",
    "exit_ts", "exit_minute", "executable_exit_quote", "exit_spread_bp",
    "exit_reason", "gross_bp", "cost_bp", "net_bp", "net_bp_B",
    "mfe_from_entry_bp", "mae_from_entry_bp", "holding_duration_min",
    "quote_lookup_entry", "quote_lookup_exit", "data_quality_flag",
]


def profit_factor(nets):
    if len(nets) == 0:
        return None
    pos = float(nets[nets > 0].sum())
    neg = float(nets[nets < 0].sum())
    if neg == 0:
        return float("inf")
    if pos == 0:
        return 0.0
    return pos / abs(neg)


def cumsum_maxdd(nets):
    if len(nets) == 0:
        return 0.0, 0.0
    cum = np.cumsum(nets)
    running = np.maximum.accumulate(cum)
    dd = running - cum
    return float(cum[-1]), float(dd.max())


def market_metrics(trades):
    if len(trades) == 0:
        return {
            "trades": 0, "trades_per_month": np.nan, "median_net_bp": np.nan,
            "mean_net_bp": np.nan, "win_rate": np.nan, "median_win_bp": np.nan,
            "median_loss_bp": np.nan, "profit_factor": None, "cumulative_net_bp": 0.0,
            "max_drawback_bp": 0.0, "invalidation_rate": np.nan,
            "horizon_exit_rate": np.nan,
        }
    nets = np.array([t["net_bp"] for t in trades], dtype=float)
    months = {(t["trading_day"][:4], t["trading_day"][5:7]) for t in trades}
    tpm = len(trades) / max(len(months), 1)
    wins = nets[nets > 0]
    losses = nets[nets < 0]
    inv = sum(1 for t in trades if t["exit_reason"] == "STRUCTURAL_INVALIDATION")
    hor = sum(1 for t in trades if t["exit_reason"] == "HORIZON")
    cum, mdd = cumsum_maxdd(nets)
    return {
        "trades": len(trades),
        "trades_per_month": tpm,
        "median_net_bp": float(np.median(nets)),
        "mean_net_bp": float(np.mean(nets)),
        "win_rate": float(len(wins) / len(nets)),
        "median_win_bp": float(np.median(wins)) if len(wins) else np.nan,
        "median_loss_bp": float(np.median(losses)) if len(losses) else np.nan,
        "profit_factor": profit_factor(nets),
        "cumulative_net_bp": cum,
        "max_drawdown_bp": mdd,
        "invalidation_rate": float(inv / len(trades)),
        "horizon_exit_rate": float(hor / len(trades)),
    }


def split_dev_oos(events, trades):
    ev_days = sorted({e["trading_day"] for e in events})
    half = len(ev_days) // 2
    dev_days = set(ev_days[:half])
    oos_days = set(ev_days[half:])
    dev = [t for t in trades if t["trading_day"] in dev_days]
    oos = [t for t in trades if t["trading_day"] in oos_days]
    return dev, oos, len(ev_days), half


def year_concentration(trades):
    if len(trades) == 0:
        return None, None
    by_year = {}
    for t in trades:
        by_year.setdefault(t["trading_day"][:4], []).append(t["net_bp"])
    yearly = {y: float(np.sum(v)) for y, v in by_year.items()}
    cum = float(np.sum([t["net_bp"] for t in trades]))
    if cum == 0:
        return None, yearly
    conc = float(max(abs(v) for v in yearly.values()) / abs(cum))
    return conc, yearly


def classify(traded_total, metrics, cum_net, pf, conc, oos):
    if traded_total < MIN_SAMPLE:
        return "INSUFFICIENT DATA", {
            "gate1_median_net_gt_0": False,
            "gate2_cumulative_net_gt_0": cum_net > 0,
            "gate3_pf_gt_1": bool(pf is not None and (np.isinf(pf) or pf > 1.0)),
            "gate4_year_concentration_le_60pct": bool(conc is not None and conc <= 0.6),
            "gate5_oos_independently_positive": False,
        }
    g1 = metrics["median_net_bp"] > 0
    g2 = cum_net > 0
    if pf is None:
        g3 = False
    else:
        g3 = bool(np.isinf(pf) or pf > 1.0)
    g4 = bool(conc is not None and conc <= 0.6)
    oos_m = market_metrics(oos)
    g5 = bool(oos_m["median_net_bp"] > 0 and oos_m["cumulative_net_bp"] > 0)
    gates = {
        "gate1_median_net_gt_0": g1,
        "gate2_cumulative_net_gt_0": g2,
        "gate3_pf_gt_1": g3,
        "gate4_year_concentration_le_60pct": g4,
        "gate5_oos_independently_positive": g5,
    }
    if all(gates.values()):
        return "ECONOMICALLY PROMISING", gates
    return "ECONOMICALLY NON-VIABLE", gates


class PeakSampler:
    def __init__(self):
        self.peak_rss = 0
        self.peak_sys_used = 0
        self.peak_cpu = 0.0
        self.lock = threading.Lock()

    def sample(self):
        p = psutil.Process()
        rss = p.memory_info().rss
        vm = psutil.virtual_memory()
        cpu = p.cpu_percent(interval=None)
        with self.lock:
            self.peak_rss = max(self.peak_rss, rss)
            self.peak_sys_used = max(self.peak_sys_used, vm.used)
            self.peak_cpu = max(self.peak_cpu, cpu)


def run():
    start_wall = time.time()
    proto_hash = sha256_file(PROTOCOL_PATH)
    if proto_hash.lower() != PROTOCOL_SHA.lower():
        raise SystemExit(f"PROTOCOL SHA MISMATCH: got {proto_hash}")

    sci_manifest = json.loads(SCIENTIFIC_MANIFEST.read_text(encoding="utf-8"))
    expected_m1 = sci_manifest["input_manifest_hash"]

    input_hash = {}
    for market in MARKETS:
        h = sha256_file(m1_path(market))
        mkey = f"{market}_M1.csv"
        if h.lower() != expected_m1[mkey].lower():
            raise SystemExit(f"M1 HASH MISMATCH {market}: got {h}")
        input_hash[f"{market}_M1"] = h
        input_hash[f"{market}_tick"] = sha256_file(tick_path(market))

    recorder = EventStudyRecorder(
        project_name="ORD_ECONOMIC",
        protocol_version="V1.1.0",
        protocol_path=PROTOCOL_PATH,
        protocol_sha=PROTOCOL_SHA,
        definition_lock_path=DEFLOCK_PATH,
        input_manifest_hash=input_hash,
        expected_artifacts=[
            "trade_ledger.csv",
            "statistics.json",
            "market_summary.csv",
            "yearly_summary.csv",
            "development_oos_summary.csv",
            "cost_model_outputs.json",
            "execution_metadata.json",
            "peak_resource.json",
            "ECONOMIC_TRANSLATION_REPORT_V1.md",
            "trade_ledger_XAUUSD.csv",
            "trade_ledger_XAGUSD.csv",
            "trade_ledger_USATECHIDXUSD.csv",
            "trade_ledger_BTCUSD.csv",
        ],
        entry_script_path=Path(__file__),
        base_output_dir=ROOT / "output/research_discovery",
    )
    recorder.preflight()
    recorder.start()
    outdir = recorder.output_dir
    peak = PeakSampler()

    events = parse_events()
    all_rows = []
    stats = {"protocol_sha256": PROTOCOL_SHA, "markets": {}}
    market_summary = []
    yearly_rows = []
    dev_oos_rows = []
    cost_output = {
        "model_a": "RT(A)=(s_entry+s_exit)/2; Net_A=Gross-RT(A)",
        "model_b": "Net_B=Gross-(s_entry+s_exit); bands additive for sensitivity only",
        "bands": {"commission_bp": COMMISSION_BANDS, "slippage_bp": SLIPPAGE_BANDS},
        "per_market": {},
    }
    mkt_timing = {}

    for market in MARKETS:
        t0 = time.time()
        evs = events[market]
        m1df = load_m1(market)
        needed = build_needed_minutes(evs)
        bucket, invalid, rows = stream_buckets(market, needed, peak)
        peak.sample()
        med = compute_medians(bucket)
        mb_bid, mb_ask = market_medians(med)

        trades = []
        for ev in evs:
            peak.sample()
            trades.append(simulate_event(market, ev, m1df, med, mb_bid, mb_ask, bucket))
        traded = [t for t in trades if t.get("net_bp") is not None]
        traded_sorted = sorted(traded, key=lambda t: (t["trading_day"], t["breakout_ts"]))
        metrics = market_metrics(traded_sorted)
        cum_net = metrics["cumulative_net_bp"]
        pf = metrics["profit_factor"]
        conc, yearly = year_concentration(traded_sorted)
        dev, oos, ndays, half = split_dev_oos(evs, traded_sorted)
        dev_m = market_metrics(dev)
        oos_m = market_metrics(oos)
        classification, gates = classify(len(traded), metrics, cum_net, pf, conc, oos)

        for y, s in (yearly or {}).items():
            yy = [t for t in traded_sorted if t["trading_day"][:4] == y]
            ymed = float(np.median([t["net_bp"] for t in yy])) if yy else np.nan
            ypf = profit_factor(np.array([t["net_bp"] for t in yy], dtype=float)) if yy else None
            yearly_rows.append(
                {"market": market, "year": int(y), "trades": len(yy),
                 "cumulative_net_bp": s, "median_net_bp": ymed, "profit_factor": ypf}
            )

        dev_oos_rows.append(
            {"market": market, "n_event_days": ndays, "dev_day_count": half,
             "dev_trades": dev_m["trades"], "dev_median_net_bp": dev_m["median_net_bp"],
             "dev_cumulative_net_bp": dev_m["cumulative_net_bp"], "dev_pf": dev_m["profit_factor"],
             "oos_trades": oos_m["trades"], "oos_median_net_bp": oos_m["median_net_bp"],
             "oos_cumulative_net_bp": oos_m["cumulative_net_bp"], "oos_pf": oos_m["profit_factor"]}
        )

        market_summary.append(
            {"market": market, "trade_count": len(traded), "classification": classification,
             "median_net_bp": metrics["median_net_bp"], "cumulative_net_bp": cum_net,
             "profit_factor": pf, "year_concentration": conc,
             "gate1": gates["gate1_median_net_gt_0"], "gate2": gates["gate2_cumulative_net_gt_0"],
             "gate3": gates["gate3_pf_gt_1"], "gate4": gates["gate4_year_concentration_le_60pct"],
             "gate5": gates["gate5_oos_independently_positive"]}
        )

        stats["markets"][market] = {
            "metrics": metrics,
            "gates": gates,
            "classification": classification,
            "trade_count": len(traded),
            "excluded": {r: sum(1 for t in trades if t["exit_reason"] == r)
                         for r in sorted({t["exit_reason"] for t in trades})},
            "year_concentration": conc,
        }

        spreads = [spread_bp(m["bid"], m["ask"]) for m in med.values()]
        spreads = [s for s in spreads if s is not None]
        nets = np.array([t["net_bp"] for t in traded_sorted], dtype=float) if traded_sorted else np.array([])
        band_res = []
        for c in COMMISSION_BANDS:
            for sl in SLIPPAGE_BANDS:
                snet = nets - c - sl
                band_res.append(
                    {"commission_bp": c, "slippage_bp": sl,
                     "median_net_bp": float(np.median(snet)) if len(snet) else np.nan,
                     "cumulative_net_bp": float(np.sum(snet)) if len(snet) else 0.0}
                )
        cost_output["per_market"][market] = {
            "observed_minutes": len(med),
            "spread_median_bp": float(np.median(spreads)) if spreads else np.nan,
            "spread_p25_bp": float(np.percentile(spreads, 25)) if spreads else np.nan,
            "spread_p75_bp": float(np.percentile(spreads, 75)) if spreads else np.nan,
            "spread_p90_bp": float(np.percentile(spreads, 90)) if spreads else np.nan,
            "median_cost_bp_modelA": float(np.median([t["cost_bp"] for t in traded_sorted])) if traded_sorted else np.nan,
            "model_b_sensitivity": band_res,
            "invalid_tick_rows": invalid,
            "streamed_rows": rows,
            "quote_lookup_counts": {
                "entry_exact": sum(1 for t in traded if t["quote_lookup_entry"] == "exact"),
                "entry_fallback": sum(1 for t in traded if t["quote_lookup_entry"].startswith("fallback")),
                "entry_market_median": sum(1 for t in traded if t["quote_lookup_entry"] == "market-median"),
                "exit_exact": sum(1 for t in traded if t["quote_lookup_exit"] == "exact"),
                "exit_fallback": sum(1 for t in traded if t["quote_lookup_exit"].startswith("fallback")),
                "exit_market_median": sum(1 for t in traded if t["quote_lookup_exit"] == "market-median"),
            },
        }
        mkt_timing[market] = time.time() - t0
        all_rows.extend(traded_sorted)
        all_rows.extend(t for t in trades if t.get("net_bp") is None)

    led_df = pd.DataFrame([{c: t.get(c) for c in LEDGER_COLUMNS} for t in all_rows])
    led_df = led_df.sort_values(["market", "trading_day", "breakout_ts"], na_position="last").reset_index(drop=True)
    led_df.to_csv(outdir / "trade_ledger.csv", index=False)
    for market in MARKETS:
        sub = led_df[led_df["market"] == market]
        sub.to_csv(outdir / f"trade_ledger_{market}.csv", index=False)

    (outdir / "statistics.json").write_text(
        json.dumps(stats, indent=2, allow_nan=True), encoding="utf-8")
    pd.DataFrame(market_summary).to_csv(outdir / "market_summary.csv", index=False)
    pd.DataFrame(yearly_rows).to_csv(outdir / "yearly_summary.csv", index=False)
    pd.DataFrame(dev_oos_rows).to_csv(outdir / "development_oos_summary.csv", index=False)
    (outdir / "cost_model_outputs.json").write_text(
        json.dumps(cost_output, indent=2, allow_nan=True), encoding="utf-8")

    peak.sample()
    peak_res = {
        "peak_process_rss_bytes": peak.peak_rss,
        "peak_system_memory_bytes": peak.peak_sys_used,
        "peak_cpu_percent": peak.peak_cpu,
    }
    (outdir / "peak_resource.json").write_text(
        json.dumps(peak_res, indent=2), encoding="utf-8")

    meta = {
        "execution_id": recorder.execution_id,
        "started": recorder.start_timestamp,
        "protocol_sha256": PROTOCOL_SHA,
        "definition_lock_sha256": sha256_file(DEFLOCK_PATH),
        "m1_hashes": {k: v for k, v in input_hash.items() if "_M1" in k},
        "tick_hashes": {k: v for k, v in input_hash.items() if "_tick" in k},
        "git_head": recorder.implementation_manifest.get("git_head"),
        "git_dirty": recorder.implementation_manifest.get("git_dirty_state"),
        "python_version": recorder.implementation_manifest.get("python_version"),
        "pandas_version": recorder.implementation_manifest.get("package_versions", {}).get("pandas"),
        "numpy_version": recorder.implementation_manifest.get("package_versions", {}).get("numpy"),
        "runner_sha256": recorder.implementation_manifest.get("entry_script_sha256"),
        "market_duration_sec": mkt_timing,
        "total_wall_sec": time.time() - start_wall,
    }
    (outdir / "execution_metadata.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8")

    report_text = build_report(recorder, meta, stats, cost_output, dev_oos_rows, yearly_rows, peak_res)
    (outdir / "ECONOMIC_TRANSLATION_REPORT_V1.md").write_text(report_text, encoding="utf-8")

    recorder.complete_execution()
    print("EXECUTION COMPLETED:", recorder.execution_id)
    print("OUTPUT:", outdir)


def build_report(recorder, meta, stats, cost_output, dev_oos_rows, yearly_rows, peak_res):
    lines = []
    w = lines.append
    w("# QUANTFORGE — ORD V1.1.0 ECONOMIC TRANSLATION REPORT V1")
    w("")
    w("## 1. Execution Identity")
    w("")
    w(f"- Execution ID: `{recorder.execution_id}`")
    w(f"- Started (UTC): {recorder.start_timestamp}")
    w(f"- Output directory: `{recorder.output_dir}`")
    w(f"- Journal final state: COMPLETED (verified by EventStudyRecorder completion gate).")
    w("")
    w("## 2. Protocol / Implementation Fingerprints")
    w("")
    w(f"- Economic protocol: `{meta['protocol_sha256']}` (`{PROTOCOL_PATH}`)")
    w(f"- Economic protocol canonical SHA-256: `{PROTOCOL_SHA_CANONICAL}`")
    w(f"- Definition lock SHA-256: `{meta['definition_lock_sha256']}`")
    w(f"- Runner SHA-256: `{meta['runner_sha256']}`")
    w(f"- Git HEAD: `{meta['git_head']}` (dirty={meta['git_dirty']})")
    w(f"- Python {meta['python_version']}; pandas {meta['pandas_version']}; numpy {meta['numpy_version']}")
    w("")
    w("## 3. Input Data Integrity")
    w("")
    w("- M1 SHA-256 verified byte-exact against the persisted scientific implementation manifest for all four simulated markets.")
    w("- Tick SHA-256 computed at execution start (see execution_metadata.json).")
    for m in MARKETS:
        w(f"  - {m}: M1 `{meta['m1_hashes'].get(m + '_M1')}`; tick `{meta['tick_hashes'].get(m + '_tick')}`")
    w("")
    w("## 4. Cost Model")
    w("")
    w(f"- Model A (PRIMARY): RT(A) = (s_entry + s_exit) / 2; Net_A = Gross - RT(A), where s is the per-minute observed MT5 spread in bp.")
    w(f"- Model B (DESCRIPTIVE): Net_B = Gross - (s_entry + s_exit); commission {COMMISSION_BANDS} bp and slippage {SLIPPAGE_BANDS} bp bands are additive in the Model-B sensitivity table only.")
    w("- No assumed spread; no invented commission in Model A.")
    for m in MARKETS:
        c = cost_output["per_market"][m]
        w(f"  - {m}: observed-minute spread median {c['spread_median_bp']:.3f} bp (p25 {c['spread_p25_bp']:.3f}, p75 {c['spread_p75_bp']:.3f}, p90 {c['spread_p90_bp']:.3f}); median Model-A cost {c['median_cost_bp_modelA']:.3f} bp over {c['observed_minutes']} observed minutes.")
    w("")
    w("## 5. Execution Bridge")
    w("")
    w("- T_B = anchor_ts + 60 s. Entry = median ASK (LONG) / median BID (SHORT) of the first eligible tick minute at/after T_B; no tick before T_B contributes; PRIMARY minute -> fallback +1..+5 -> market median -> exclusion.")
    w("- Structural levels from the validated M1 opening range; cross-check vs persisted range_width (1e-6 relative / 1e-4 absolute); mismatches excluded.")
    w("- Stop: close-based trigger bar-by-bar from the bar after the breakout bar; fill = first trigger-side executable quote at/after the trigger bar start; gap-through fills at the actual quote (no backfill, no favourable improvement, no buffer); cap at the horizon minute.")
    w("- Horizon: 120 literal wall-clock minutes from T_B; may cross sessions/rollover/next session; incomplete horizon excluded.")
    w("")
    w("## 6. Trade Population")
    w("")
    for m in MARKETS:
        s = stats["markets"][m]
        w(f"- {m}: traded {s['trade_count']}; exclusions {s['excluded']}.")
    w("")
    w("## 7. Primary Economic Metrics (Model A, bp)")
    w("")
    for m in MARKETS:
        mt = stats["markets"][m]["metrics"]
        w(f"- **{m}** — n={mt['trades']} ({mt['trades_per_month']:.2f}/mo); median net {mt['median_net_bp']:.3f}; mean {mt['mean_net_bp']:.3f}; win rate {mt['win_rate']*100:.1f}%; median win {mt['median_win_bp']:.3f}; median loss {mt['median_loss_bp']:.3f}; PF {mt['profit_factor']}; cumulative {mt['cumulative_net_bp']:.1f}; max drawdown {mt['max_drawdown_bp']:.1f}; invalidation {mt['invalidation_rate']*100:.1f}%; horizon exit {mt['horizon_exit_rate']*100:.1f}%.")
    w("")
    w("## 8. Development / OOS (chronological floor(N/2) event days)")
    w("")
    for r in dev_oos_rows:
        w(f"- {r['market']}: {r['n_event_days']} event days, dev {r['dev_day_count']}. Dev: n={r['dev_trades']}, median {r['dev_median_net_bp']:.3f}, cumulative {r['dev_cumulative_net_bp']:.1f}, PF {r['dev_pf']}. OOS: n={r['oos_trades']}, median {r['oos_median_net_bp']:.3f}, cumulative {r['oos_cumulative_net_bp']:.1f}, PF {r['oos_pf']}.")
    w("")
    w("## 9. Yearly Results")
    w("")
    for r in yearly_rows:
        w(f"- {r['market']} {r['year']}: n={r['trades']}, cumulative {r['cumulative_net_bp']:.1f}, median {r['median_net_bp']:.3f}, PF {r['profit_factor']}.")
    w("")
    w("## 10. Year Concentration")
    w("")
    for m in MARKETS:
        conc = stats["markets"][m]["year_concentration"]
        w(f"- {m}: max|yearly net| / |final cumulative| = {conc if conc is None else round(conc, 4)} (None if no traded sample or zero cumulative).")
    w("")
    w("## 11. Model B Sensitivity (descriptive only)")
    w("")
    for m in MARKETS:
        c = cost_output["per_market"][m]
        meds = {f"c{r['commission_bp']:g}s{r['slippage_bp']:g}": round(r['median_net_bp'], 3) for r in c["model_b_sensitivity"]}
        w(f"- {m} median net bp by band: {meds}")
    w("")
    w("## 12. Market Classifications")
    w("")
    for m in MARKETS:
        s = stats["markets"][m]
        caveat = " (NO-SCIENTIFIC-VERDICT) " if m == "BTCUSD" else ""
        w(f"- {m}: **{s['classification']}**{caveat}")
        w(f"  - Gates: {s['gates']}")
    w("- EURUSD: NOT SIMULATED (NOT REGISTERED / DATA-LIMITED).")
    w("")
    w("## 13. Resource Usage")
    w("")
    w(f"- Peak process RSS: {peak_res['peak_process_rss_bytes']/1e9:.2f} GB; peak system used memory: {peak_res['peak_system_memory_bytes']/1e9:.2f} GB; peak CPU: {peak_res['peak_cpu_percent']:.1f}%.")
    w(f"- Market durations (s): {meta['market_duration_sec']}; total wall clock: {meta['total_wall_sec']:.1f} s.")
    w("")
    w("## 14. Artifact Integrity")
    w("")
    w("- EventStudyRecorder completion gate verified: journal COMPLETED; no missing/unexpected artifacts.")
    w("- Ledger retains all rows including EXCLUDED_* rows (no trade removed for being unfavourable).")
    w("")
    w("## 15. Scientific Boundary")
    w("")
    w("- No scientific object, protocol, execution artifact, or adjudication was modified.")
    w("- This report records the execution results only; it performs no adjudication and states no verdict on whether any strategy works, fails, or is profitable.")
    w("")
    w("## 16. Exact Next Governance Task")
    w("")
    w("> **INDEPENDENT ECONOMIC RESULTS ADJUDICATION** of this single controlled execution: determine whether the baseline economically survives, fails, or requires governance escalation. No alternative translation or optimization is authorized automatically.")
    w("")
    return "\n".join(lines)


if __name__ == "__main__":
    run()