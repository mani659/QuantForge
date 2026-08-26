"""Stage 1 — Frozen economic-input preparation (V2.0.1 §4).

Converts, ONE market at a time, the raw tick file into a compact, immutable,
hashable intermediate containing only the deterministic inputs the economic
simulation requires.  Performs NO PnL / viability / profit-factor / economic
classification.

Bounded-memory model (§4.1, W1):
  * a single line-buffered pass over the tick file;
  * at most the CURRENT minute's tick observations are resident; on
    minute-rollover the minute is reduced to its aggregates, appended to disk,
    and DISCARDED;
  * a bounded deterministic event-join state drives structural-stop fill
    discovery (per-event watch, not a minutes table);
  * the market-median universe (W2) — ALL eligible observed minutes — is kept on
    disk (minute index + `minute_quotes.csv.gz`), never as an in-RAM table; the
    exact market median is computed by bounded external quickselect.

Preparation identity (W4): `PREP_<market>_<FULL_SHA256>` over the canonical
nine-field manifest of `_identity.build_canonical_manifest`.

Reuse rule (§5 / mission §9): a completed `PREP_<market>_<hash>` directory is
reused only when its persisted manifest + artifact hashes match the current
frozen identity exactly; otherwise it must be regenerated.  A crashed/partial
directory is never reused; regeneration materializes into the same
content-addressed name only after the failed directory has been reconciled and,
under an explicit `force_rebuild`, moved aside (preserved, never overwritten).
"""

from __future__ import annotations

import gc
import gzip
import json
import math
import os
import struct
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import psutil

from ._failure import ExecutionInfrastructureFailure, classify_infrastructure_failure
from ._identity import (
    MINUTE_RECORD_FORMAT,
    MINUTE_RECORD_SIZE,
    PREP_CODE_SCHEMA_VERSION,
    STAGE1_SCHEMA_VERSION,
    MinuteIndex,
    build_canonical_manifest,
    canonical_stage1_parameters,
    prep_identity,
    preparation_implementation_sha256,
    sha256_file,
)
from ._stage_recorder import StageRunRecorder

EPOCH = datetime(2000, 1, 1)
NY = ZoneInfo("America/New_York")
HORIZON_MIN = 120
FALLBACK_MIN = 5

PREP_ARTIFACTS = {
    "prep_manifest.json",
    "minute_quotes.csv.gz",
    "event_inputs.csv",
    "event_paths.csv",
    "minute_index.bin",
}

EVENT_INPUT_COLUMNS = [
    "market", "trading_day", "direction", "event_id", "breakout_ts",
    "breakout_close", "T_B", "horizon_ts",
    "or_high", "or_low", "or_width", "range_width_persisted",
    "range_check_status", "horizon_complete",
    "exclusion_status",
    "structural_invalidation_level",
    "trigger_bar_minute",
    "stop_fill_minute", "stop_fill_ts",
    "stop_fill_bid", "stop_fill_ask", "stop_exec_quote", "stop_spread_bp",
    "entry_minute", "entry_bid", "entry_ask", "executable_entry_quote",
    "entry_spread_bp", "quote_lookup_entry",
    "exit_lookup_minute", "exit_bid", "exit_ask", "executable_exit_quote",
    "exit_spread_bp", "quote_lookup_exit",
    "exit_minute", "exit_ts", "hit_minute",
    "exit_reason", "data_quality_flag",
]


def epoch_minutes(dt: datetime) -> int:
    return int(int((dt - EPOCH).total_seconds()) // 60)


def from_epoch_minutes(m: int) -> datetime:
    return EPOCH + timedelta(minutes=int(m))


def tmin(dt: datetime) -> datetime:
    return dt.replace(second=0, microsecond=0)


def spread_bp(bid: float, ask: float) -> float | None:
    mid = (bid + ask) / 2.0
    if mid <= 0:
        return None
    return (ask - bid) / mid * 1.0e4


def _parse_tick_line(line: str):
    """Parses one tick line -> (date, hh, mm, ss, bid, ask) or None.

    Returns None for malformed / invalid-quote rows (never economic).
    """
    stripped = line.rstrip("\n").rstrip("\r")
    if not stripped:
        return None
    parts = stripped.split(",")
    if len(parts) < 4:
        return None
    date_s, tm_s, bid_s, ask_s = parts[0], parts[1], parts[2], parts[3]
    if not (len(date_s) == 8 and date_s.isdigit()):
        return None
    hms = tm_s.split(":")
    if len(hms) != 3:
        return None
    try:
        hh, mm, ss = int(hms[0]), int(hms[1]), int(hms[2])
        bid = float(bid_s)
        ask = float(ask_s)
    except ValueError:
        return None
    if not (math.isfinite(bid) and math.isfinite(ask)):
        return None
    if not (bid > 0 and ask > 0 and bid <= ask):
        return None
    return date_s, hh, mm, ss, bid, ask


class TickSource:
    def iter_ticks(self):
        raise NotImplementedError


class CsvTickSource(TickSource):
    def __init__(self, path: Path):
        self.path = path

    def iter_ticks(self):
        with open(self.path, "r", newline="") as f:
            for line in f:
                parsed = _parse_tick_line(line)
                yield (parsed is not None, parsed)


class ParquetTickSource(TickSource):
    def __init__(self, path: Path):
        self.path = path

    def iter_ticks(self):
        import pyarrow.parquet as pq
        for part in sorted(self.path.glob("*.parquet")):
            table = pq.read_table(part, columns=["date", "time", "bid", "ask"])
            for batch in table.to_batches(max_chunksize=100000):
                d_arr = batch["date"].to_pylist()
                t_arr = batch["time"].to_pylist()
                b_arr = batch["bid"].to_pylist()
                a_arr = batch["ask"].to_pylist()
                for i in range(len(d_arr)):
                    t_str = t_arr[i]
                    hms = t_str.split(":")
                    if len(hms) >= 3:
                        yield True, (d_arr[i], int(hms[0]), int(hms[1]), int(hms[2]), float(b_arr[i]), float(a_arr[i]))
                    else:
                        yield False, None


class _StreamTracker:
    """Structural bounded-state evidence for W1 (no market-wide minutes table)."""

    def __init__(self):
        self.max_minute_ticks = 0
        self.rows = 0
        self.minutes_flushed = 0
        self.last_minute_flushed = None

    def observe(self, current_minute_ticks: int):
        self.max_minute_ticks = max(self.max_minute_ticks, current_minute_ticks)


def load_m1(path: Path, market: str) -> pd.DataFrame:
    """Mirror of run_ord_econ_v1.load_m1 (naive-UTC M1 projected to ET)."""
    df = pd.read_csv(path)
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


def or_window(market: str, et_hour: int, et_minute: int) -> bool:
    if market in ("XAUUSD", "XAGUSD", "BTCUSD"):
        return (et_hour == 3) and (et_minute <= 29)
    return (et_hour == 9) and (et_minute >= 30)


def parse_events_for_market(df: pd.DataFrame, market: str) -> list[dict]:
    sub = df[(df["market"] == market) & (df["type"] == "treatment")]
    events = []
    for _, r in sub.iterrows():
        anchor = pd.Timestamp(r["anchor_ts"]).to_pydatetime().replace(tzinfo=None)
        events.append(
            {
                "market": market,
                "trading_day": str(r["trading_day"])[:10],
                "direction": str(r["direction"]).lower(),
                "anchor_ts": anchor,
                "entry_close": float(r["entry_close"]),
                "range_width": float(r["range_width"]),
            }
        )
    events.sort(key=lambda e: (e["trading_day"], e["anchor_ts"]))
    return events


def _event_id(market: str, trading_day: str, direction: str, breakout_ts: str) -> str:
    return f"{market}|{trading_day}|{direction}|{breakout_ts}"


# ---------------------------------------------------------------------------
# Stream pass (bounded)
# ---------------------------------------------------------------------------

class _StopWatches:
    """Bounded deterministic event-join state for structural-stop discovery.

    Holds per-event scan windows; the current-minute search iterates only
    unfilled watches whose window contains the current minute.  Items are
    removed as soon as they are filled or their horizon passes.
    """

    def __init__(self, watches: list):
        self.items = []  # (trigger_min, horizon_min, direction, level, event_idx)
        for w in sorted(watches, key=lambda w: w["trigger_min"]):
            self.items.append(
                (
                    w["trigger_min"],
                    w["horizon_min"],
                    w["direction"],
                    w["level"],
                    w["event_index"],
                )
            )
        self.fills = {w["event_index"]: None for w in watches}

    def scan_tick(self, cur_epoch: int, bid: float, ask: float,
                  date_s: str, hh: int, mm: int, ss: int):
        i = 0
        n = len(self.items)
        while i < n:
            trig, horz, direction, level, idx = self.items[i]
            if cur_epoch >= horz:
                self.items[i] = self.items[n - 1]
                self.items.pop()
                n -= 1
                continue
            if cur_epoch >= trig:
                hit = (bid <= level) if direction == "long" else (ask >= level)
                if hit:
                    fill_ts = datetime(
                        int(date_s[0:4]), int(date_s[4:6]), int(date_s[6:8]),
                        hh, mm, ss,
                    )
                    exec_quote = bid if direction == "long" else ask
                    self.fills[idx] = {
                        "exit_ts": fill_ts,
                        "exit_minute": cur_epoch,
                        "exec_quote": exec_quote,
                        "bid": bid,
                        "ask": ask,
                    }
                    self.items[i] = self.items[n - 1]
                    self.items.pop()
                    n -= 1
                    continue
            i += 1


def _stream_minutes(
    tick_source: TickSource,
    idx_path: Path,
    quotes_path: Path,
    watches: _StopWatches,
    tracker: _StreamTracker,
) -> int:
    """Single bounded pass.  Returns invalid-row count.

    Minute rollover flushes aggregates to the minute index + quote stream and
    discards the minute buffer; the final (last) minute is flushed at EOF.
    Structural-stop fills are discovered in tick order (first qualifying
    trigger-side tick at/after the trigger-bar start, gap-through at the actual
    quote, capped at the horizon minute — V1.1.0 §5).
    """
    invalid = 0
    buf = []            # current-minute ticks only: (hh,mm,ss,bid,ask)
    cur_key = None
    cur_epoch = None
    cur_date = None
    record = bytearray(MINUTE_RECORD_SIZE)

    with open(idx_path, "wb") as idxf, gzip.open(
        quotes_path, "wt", newline="", encoding="utf-8"
    ) as gz:
        gz.write("epoch_min,minute_utc,bid_median,ask_median,nticks\n")

        def flush_minute():
            nonlocal buf, cur_key
            if cur_key is None:
                return
            if buf:
                bids = [t[3] for t in buf]
                asks = [t[4] for t in buf]
                bmed = float(np.median(bids))
                amed = float(np.median(asks))
                tracker.observe(len(buf))
                struct.pack_into(MINUTE_RECORD_FORMAT, record, 0,
                                 cur_epoch, bmed, amed, len(buf))
                idxf.write(memoryview(record))
                utc = from_epoch_minutes(cur_epoch)
                gz.write(
                    f"{cur_epoch},{utc.strftime('%Y-%m-%d %H:%M:00')},"
                    f"{repr(bmed)},{repr(amed)},{len(buf)}\n"
                )
                buf.clear()
                tracker.minutes_flushed += 1
                tracker.last_minute_flushed = cur_key
            cur_key = None

        for is_valid, parsed in tick_source.iter_ticks():
            tracker.rows += 1
            if not is_valid or parsed is None:
                invalid += 1
                continue
            date_s, hh, mm, ss, bid, ask = parsed
            key = date_s + "," + f"{hh:02d}:{mm:02d}"
            if key != cur_key:
                flush_minute()
                cur_key = key
                cur_date = date_s
                y, m, d = int(date_s[0:4]), int(date_s[4:6]), int(date_s[6:8])
                cur_epoch = epoch_minutes(datetime(y, m, d, hh, mm))
            buf.append((hh, mm, ss, bid, ask))
            watches.scan_tick(cur_epoch, bid, ask, date_s, hh, mm, ss)

        flush_minute()  # last-minute flush (never dropped)

    return invalid


# ---------------------------------------------------------------------------
# Event skeleton (M1-derived, before streaming)
# ---------------------------------------------------------------------------

def _build_event_skeletons(events: list[dict], m1df: pd.DataFrame,
                           market: str) -> list[dict]:
    """Per-event: OR levels + range cross-check + horizon completeness +
    trigger-bar minute.  All values deterministic from frozen M1/event data."""
    skeletons = []
    london = market in ("XAUUSD", "XAGUSD", "BTCUSD")
    for idx, ev in enumerate(events):
        anchor = ev["anchor_ts"]
        tb = tmin(anchor + timedelta(seconds=60))
        hz = tb + timedelta(minutes=HORIZON_MIN)
        td = anchor.date()

        high_or, low_or = None, None
        if london:
            mask = (
                (m1df["et_date"] == td)
                & (m1df["et_hour"] == 3)
                & (m1df["et_minute"] <= 29)
            )
        else:
            mask = (
                (m1df["et_date"] == td)
                & (m1df["et_hour"] == 9)
                & (m1df["et_minute"] >= 30)
            )
        window = m1df[mask]
        if len(window) >= 30:
            high_or = float(window["high"].max())
            low_or = float(window["low"].min())

        exclusion = ""
        if high_or is None or low_or is None:
            exclusion = "EXCLUDED_RANGE_RECONSTRUCTION"
        else:
            tol = max(1.0e-4, abs(ev["range_width"]) * 1.0e-6)
            if abs((high_or - low_or) - ev["range_width"]) > tol:
                exclusion = "EXCLUDED_RANGE_MISMATCH"

        hkey = pd.Timestamp(hz, tz="UTC")
        horizon_complete = bool(hkey in m1df.index)
        if exclusion == "" and not horizon_complete:
            exclusion = "EXCLUDED_HORIZON_INCOMPLETE"

        trigger_minute = None
        if exclusion == "":
            direction = ev["direction"]
            for k in range(1, HORIZON_MIN + 1):
                bar_start = anchor + timedelta(minutes=k)
                ts = pd.Timestamp(bar_start, tz="UTC")
                if ts not in m1df.index:
                    continue
                close = float(m1df.at[ts, "close"])
                if (direction == "long" and close <= high_or) or (
                    direction == "short" and close >= low_or
                ):
                    trigger_minute = bar_start
                    break
        skeletons.append(
            {
                "index": idx,
                "event": ev,
                "tb": tb,
                "hz": hz,
                "high_or": high_or,
                "low_or": low_or,
                "exclusion": exclusion,
                "horizon_complete": horizon_complete,
                "trigger_minute": trigger_minute,
            }
        )
    return skeletons


# ---------------------------------------------------------------------------
# Entry / exit resolution (exact -> fallback+k -> market-median -> exclusion)
# ---------------------------------------------------------------------------

def _resolve_entry(idx: MinuteIndex, tb: datetime, mb_bid, mb_ask):
    for k in range(FALLBACK_MIN + 1):
        cand = tb + timedelta(minutes=k)
        rec = idx.get(epoch_minutes(cand))
        if rec is not None:
            return cand, ("exact" if k == 0 else f"fallback+{k}"), rec
    if mb_bid is not None:
        return "market-median", "market-median", None
    return None, None, None


def _resolve_exit(idx: MinuteIndex, hz: datetime, mb_bid, mb_ask):
    rec = idx.get(epoch_minutes(hz))
    if rec is not None:
        return hz, "exact", rec
    best = None
    bestd = None
    best_rec = None
    for k in range(1, FALLBACK_MIN + 1):
        for cand, dist in ((hz - timedelta(minutes=k), k),
                           (hz + timedelta(minutes=k), k)):
            r = idx.get(epoch_minutes(cand))
            if r is not None and (best is None or dist < bestd):
                best = cand
                bestd = dist
                best_rec = r
    if best is not None:
        return best, f"fallback+{bestd}", best_rec
    if mb_bid is not None:
        return "market-median", "market-median", None
    return None, None, None


# ---------------------------------------------------------------------------
# Finalization: event inputs + paths + manifest
# ---------------------------------------------------------------------------

def _finalize_prep(
    prep_dir: Path,
    identity: "PrepIdentity",
    skeletons: list[dict],
    market: str,
    mb_bid: float,
    mb_ask: float,
    idx: MinuteIndex,
    tracker: _StreamTracker,
    stop_fills: dict,
    environment: dict,
    peak_rss: int,
    invalid_rows: int,
    elapsed_s: float,
) -> None:
    header = ",".join(EVENT_INPUT_COLUMNS)
    rows = []
    path_rows = []

    def row_of(sk):
        ev = sk["event"]
        direction = ev["direction"]
        return {
            "market": market,
            "trading_day": ev["trading_day"],
            "direction": direction,
            "event_id": _event_id(market, ev["trading_day"], direction,
                                  ev["anchor_ts"].isoformat()),
            "breakout_ts": ev["anchor_ts"].isoformat(),
            "breakout_close": ev["entry_close"],
            "T_B": sk["tb"].isoformat(),
            "horizon_ts": sk["hz"].isoformat(),
            "or_high": sk["high_or"],
            "or_low": sk["low_or"],
            "or_width": (sk["high_or"] - sk["low_or"])
            if sk["high_or"] is not None else None,
            "range_width_persisted": ev["range_width"],
            "range_check_status": "OK" if sk["exclusion"] == ""
            else sk["exclusion"],
            "horizon_complete": sk["horizon_complete"],
            "exclusion_status": sk["exclusion"],
            "structural_invalidation_level": None,
            "trigger_bar_minute": "",
            "stop_fill_minute": "", "stop_fill_ts": "",
            "stop_fill_bid": "", "stop_fill_ask": "",
            "stop_exec_quote": "", "stop_spread_bp": "",
            "entry_minute": "", "entry_bid": "", "entry_ask": "",
            "executable_entry_quote": "", "entry_spread_bp": "",
            "quote_lookup_entry": "",
            "exit_lookup_minute": "", "exit_bid": "", "exit_ask": "",
            "executable_exit_quote": "", "exit_spread_bp": "",
            "quote_lookup_exit": "",
            "exit_minute": "", "exit_ts": "", "hit_minute": "",
            "exit_reason": "", "data_quality_flag": "",
        }

    for sk in skeletons:
        ev = sk["event"]
        direction = ev["direction"]
        row = row_of(sk)
        if sk["exclusion"] != "":
            row["exit_reason"] = sk["exclusion"]
            row["data_quality_flag"] = sk["exclusion"]
            rows.append(row)
            continue

        row["structural_invalidation_level"] = (
            sk["high_or"] if direction == "long" else sk["low_or"]
        )
        if sk["trigger_minute"] is not None:
            row["trigger_bar_minute"] = epoch_minutes(sk["trigger_minute"])

        entry_min, entry_lookup, entry_rec = _resolve_entry(idx, sk["tb"],
                                                            mb_bid, mb_ask)
        if entry_min is None:
            row["exit_reason"] = "EXCLUDED_NO_QUOTE_COVERAGE"
            row["data_quality_flag"] = "EXCLUDED_NO_QUOTE_COVERAGE"
            rows.append(row)
            continue
        if entry_min == "market-median":
            entry_bid, entry_ask = mb_bid, mb_ask
            entry_label = "market-median"
        else:
            entry_bid, entry_ask, _ = entry_rec
            entry_label = entry_min.isoformat()
        entry_exec = entry_ask if direction == "long" else entry_bid
        row["entry_minute"] = entry_label
        row["entry_bid"] = entry_bid
        row["entry_ask"] = entry_ask
        row["executable_entry_quote"] = entry_exec
        row["entry_spread_bp"] = spread_bp(entry_bid, entry_ask)
        row["quote_lookup_entry"] = entry_lookup

        fill = stop_fills.get(sk["index"])
        if fill is not None:
            row["stop_fill_minute"] = fill["exit_minute"]
            row["stop_fill_ts"] = fill["exit_ts"].isoformat()
            row["stop_fill_bid"] = fill["bid"]
            row["stop_fill_ask"] = fill["ask"]
            row["stop_exec_quote"] = fill["exec_quote"]
            row["stop_spread_bp"] = spread_bp(fill["bid"], fill["ask"])
            exit_ts = fill["exit_ts"]
            hit_min = int(fill["exit_minute"])
            exit_exec = fill["exec_quote"]
            exit_bid, exit_ask = fill["bid"], fill["ask"]
            exit_sp = row["stop_spread_bp"]
            exit_lookup = "exact"
            exit_lookup_label = "structural-invalidation"
            exit_reason = "STRUCTURAL_INVALIDATION"
        else:
            exit_min, exit_lookup, exit_rec = _resolve_exit(idx, sk["hz"],
                                                            mb_bid, mb_ask)
            if exit_min is None:
                row["exit_reason"] = "EXCLUDED_NO_QUOTE_COVERAGE"
                row["data_quality_flag"] = "EXCLUDED_NO_QUOTE_COVERAGE"
                rows.append(row)
                continue
            if exit_min == "market-median":
                exit_bid, exit_ask = mb_bid, mb_ask
                exit_lookup_label = "market-median"
            else:
                exit_bid, exit_ask, _ = exit_rec
                exit_lookup_label = exit_min.isoformat()
            exit_exec = exit_bid if direction == "long" else exit_ask
            exit_sp = spread_bp(exit_bid, exit_ask)
            exit_ts = sk["hz"]
            hit_min = epoch_minutes(sk["hz"])
            exit_reason = "HORIZON"

        row["exit_lookup_minute"] = exit_lookup_label
        row["exit_bid"] = exit_bid
        row["exit_ask"] = exit_ask
        row["executable_exit_quote"] = exit_exec
        row["exit_spread_bp"] = exit_sp
        row["quote_lookup_exit"] = exit_lookup
        row["exit_minute"] = (
            epoch_minutes(exit_ts) if isinstance(exit_ts, datetime) else hit_min
        )
        row["exit_ts"] = exit_ts.isoformat()
        row["hit_minute"] = hit_min
        row["exit_reason"] = exit_reason
        row["data_quality_flag"] = ""

        tb_e = epoch_minutes(sk["tb"])
        for m in range(tb_e, hit_min + 1):
            rec = idx.get(m)
            if rec is not None:
                path_rows.append((row["event_id"], m, repr(rec[0]), repr(rec[1])))
        rows.append(row)

    df = pd.DataFrame(rows, columns=EVENT_INPUT_COLUMNS)
    with open(prep_dir / "event_inputs.csv", "w", newline="", encoding="utf-8") as f:
        f.write(header + "\n")
        df.to_csv(f, index=False, header=False)

    with open(prep_dir / "event_paths.csv", "w", newline="", encoding="utf-8") as f:
        f.write("event_id,epoch_min,bid_median,ask_median\n")
        for event_id, m, b, a in sorted(path_rows, key=lambda r: (r[0], r[1])):
            f.write(f"{event_id},{m},{b},{a}\n")

    artifact_hashes = {}
    for name in ("minute_quotes.csv.gz", "event_inputs.csv",
                 "event_paths.csv", "minute_index.bin"):
        artifact_hashes[name] = sha256_file(prep_dir / name)

    manifest = {
        "preparation_identity": identity.identity,
        "preparation_hash": identity.hash,
        "market": market,
        "stage": "STAGE1",
        "schema_stage1": identity.schema_stage1,
        "code_schema_prep": identity.code_schema_prep,
        "economic_protocol_sha256": identity.economic_protocol_sha256,
        "scientific_protocol_sha256": identity.scientific_protocol_sha256,
        "source_m1_sha256": identity.source_m1_sha256,
        "source_tick_sha256": identity.source_tick_sha256,
        "implementation_sha256": identity.implementation_sha256,
        "parameter_manifest": identity.param_manifest,
        "market_median_bid": mb_bid,
        "market_median_ask": mb_ask,
        "observed_minutes": len(idx),
        "tick_rows_streamed": tracker.rows,
        "invalid_tick_rows": invalid_rows,
        "minutes_flushed": tracker.minutes_flushed,
        "last_minute_flushed": tracker.last_minute_flushed,
        "max_minute_ticks_resident": tracker.max_minute_ticks,
        "n_events": len(skeletons),
        "n_excluded_events": sum(1 for s in skeletons if s["exclusion"] != ""),
        "n_stop_fills": sum(1 for v in stop_fills.values() if v is not None),
        "peak_process_rss_bytes": peak_rss,
        "elapsed_seconds": round(elapsed_s, 3),
        "environment": environment,
        "artifact_hashes": artifact_hashes,
        "reused": False,
        "canonical_manifest_sha256": identity.hash.lower(),
    }
    (prep_dir / "prep_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Identity + reuse gate
# ---------------------------------------------------------------------------

class PrepIdentity:
    """Canonical W4 identity for one market's preparation."""

    def __init__(
        self,
        market: str,
        economic_protocol_sha256: str,
        scientific_protocol_sha256: str,
        source_m1_sha256: str,
        source_tick_sha256: str,
        repo_root: Path,
        parameter_manifest: str | None = None,
        schema_stage1: str = STAGE1_SCHEMA_VERSION,
        code_schema_prep: str = PREP_CODE_SCHEMA_VERSION,
    ):
        self.market = market.upper()
        self.economic_protocol_sha256 = economic_protocol_sha256.lower()
        self.scientific_protocol_sha256 = scientific_protocol_sha256.lower()
        self.source_m1_sha256 = source_m1_sha256.lower()
        self.source_tick_sha256 = source_tick_sha256.lower()
        self.param_manifest = parameter_manifest or canonical_stage1_parameters()
        self.schema_stage1 = schema_stage1
        self.code_schema_prep = code_schema_prep
        self.implementation_sha256 = preparation_implementation_sha256(repo_root)
        self.canonical_bytes = build_canonical_manifest(
            self.market,
            self.economic_protocol_sha256,
            self.scientific_protocol_sha256,
            self.source_m1_sha256,
            self.source_tick_sha256,
            self.implementation_sha256,
            stage1_parameter_manifest=self.param_manifest,
            schema_stage1=self.schema_stage1,
            code_schema_prep=self.code_schema_prep,
        )
        self.identity = prep_identity(self.market, self.canonical_bytes)
        self.hash = self.identity.split("_")[-1]

    def fields(self) -> dict:
        return {
            "market": self.market,
            "economic_protocol_sha256": self.economic_protocol_sha256,
            "scientific_protocol_sha256": self.scientific_protocol_sha256,
            "source_m1_sha256": self.source_m1_sha256,
            "source_tick_sha256": self.source_tick_sha256,
            "implementation_sha256": self.implementation_sha256,
            "parameter_manifest": self.param_manifest,
            "schema_stage1": self.schema_stage1,
            "code_schema_prep": self.code_schema_prep,
            "preparation_hash": self.hash,
            "preparation_identity": self.identity,
        }


def is_valid_prep(prep_dir: Path, identity: "PrepIdentity") -> tuple[bool, str]:
    """Reuse check (§5): journal COMPLETED + manifest identity match + artifacts
    byte-exact.  Returns (valid, reason_string)."""
    if not prep_dir.is_dir():
        return False, "directory missing"
    journal = prep_dir / "execution_journal.json"
    if not journal.is_file():
        return False, "execution_journal.json missing"
    try:
        state = json.loads(journal.read_text(encoding="utf-8")).get("state")
    except Exception:
        return False, "execution_journal.json malformed"
    if state != "COMPLETED":
        return False, f"prep not completed (journal state={state})"
    manifest_p = prep_dir / "prep_manifest.json"
    if not manifest_p.is_file():
        return False, "prep_manifest.json missing"
    try:
        m = json.loads(manifest_p.read_text(encoding="utf-8"))
    except Exception:
        return False, "prep_manifest.json malformed"
    for key, expect in identity.fields().items():
        if key in ("preparation_identity", "preparation_hash"):
            continue
        if m.get(key) != expect:
            return False, f"identity field mismatch: {key}"
    if m.get("preparation_identity") != identity.identity:
        return False, "preparation_identity mismatch"
    if m.get("preparation_hash") != identity.hash:
        return False, "preparation_hash mismatch"
    for name in PREP_ARTIFACTS - {"prep_manifest.json"}:
        p = prep_dir / name
        if not p.is_file():
            return False, f"artifact missing: {name}"
        if sha256_file(p) != m.get("artifact_hashes", {}).get(name):
            return False, f"artifact hash mismatch: {name}"
    return True, "valid"


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def run_stage1_prepare(
    out_root: Path,
    repo_root: Path,
    market: str,
    m1_path: Path,
    tick_path: Path,
    event_table_path: Path,
    economic_protocol_sha256: str,
    scientific_protocol_sha256: str,
    v2_0_1_protocol_sha256: str = "",
    force_rebuild: bool = False,
    entry_script_path: Path | None = None,
    helper_module_paths: list[Path] | None = None,
) -> dict:
    """Prepares one market's frozen Stage-1 intermediate.  Returns a result
    dict with mode in {"built", "reused"}."""
    market = market.upper()
    t0 = time.time()
    try:
        m1_sha = sha256_file(m1_path)
        if tick_path.is_dir():
            manifest_path = tick_path.parent / "manifest.json"
            if manifest_path.exists():
                import json
                tick_sha = json.loads(manifest_path.read_text(encoding="utf-8")).get("source_csv_sha256", "UNKNOWN")
            else:
                tick_sha = "UNKNOWN_PARQUET_CSV_SHA"
        else:
            tick_sha = sha256_file(tick_path)
    except Exception as exc:
        raise ExecutionInfrastructureFailure(
            classify_infrastructure_failure(exc),
            f"Stage 1 source unreadable for {market}: {exc}",
        ) from exc
    identity = PrepIdentity(
        market=market,
        economic_protocol_sha256=economic_protocol_sha256,
        scientific_protocol_sha256=scientific_protocol_sha256,
        source_m1_sha256=m1_sha,
        source_tick_sha256=tick_sha,
        repo_root=repo_root,
    )
    canonical_dir = out_root / identity.identity

    valid, reason = is_valid_prep(canonical_dir, identity)
    if valid:
        return {
            "market": market,
            "mode": "reused",
            "prep_dir": str(canonical_dir),
            "preparation_identity": identity.identity,
            "preparation_hash": identity.hash,
            "reason": "completed preparation matches frozen identity exactly",
        }

    if canonical_dir.exists() and not force_rebuild:
        raise ExecutionInfrastructureFailure(
            "PREPARATION_INTEGRITY_FAILURE",
            f"{canonical_dir} exists but is not a valid completed preparation "
            f"({reason}).  Reconcile any crashed run, then re-run with "
            f"--force-rebuild to regenerate the content-addressed preparation.",
        )

    if canonical_dir.exists() and force_rebuild:
        moved = out_root / (
            f"{identity.identity}_RECONCILED_"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_"
            f"{uuid.uuid4().hex[:8]}"
        )
        os.rename(canonical_dir, moved)
        archive = {
            "archived_from": str(canonical_dir),
            "archived_to": str(moved),
            "reason": "invalid preparation regenerated (never overwritten)",
            "prior_state_reason": reason,
        }
        (moved / "archival_note.json").write_text(
            json.dumps(archive, indent=2), encoding="utf-8"
        )
        jpath = moved / "execution_journal.json"
        if jpath.is_file():
            try:
                j = json.loads(jpath.read_text(encoding="utf-8"))
                j["state"] = "CRASHED"
                j["reason"] = "PREPARATION REGENERATED AFTER INVALIDATION (archived)"
                jpath.write_text(json.dumps(j, indent=2), encoding="utf-8")
            except Exception:
                pass

    run_dir = out_root / (
        f"{identity.identity}_IN_PROGRESS_{uuid.uuid4().hex[:8]}"
    )
    rec = StageRunRecorder(
        directory=run_dir,
        stage_name="STAGE1",
        protocol_sha=economic_protocol_sha256,
        entry_script_path=entry_script_path or Path(__file__),
        helper_module_paths=helper_module_paths or [],
        extra_identity={
            "market": market,
            "preparation_identity": identity.identity,
            "preparation_hash": identity.hash,
        },
    )
    rec.start()

    invalid_rows = 0
    try:
        events_df = pd.read_csv(event_table_path)
        events = parse_events_for_market(events_df, market)
        m1df = load_m1(m1_path, market)

        high_or_low = {}
        skeletons = _build_event_skeletons(events, m1df, market)
        for sk in skeletons:
            high_or_low[sk["index"]] = (
                sk["high_or"] if sk["event"]["direction"] == "long" else sk["low_or"]
            )

        tracker = _StreamTracker()
        watches = _StopWatches(
            [
                {
                    "trigger_min": epoch_minutes(s["trigger_minute"]),
                    "horizon_min": epoch_minutes(s["hz"]),
                    "direction": s["event"]["direction"],
                    "level": high_or_low[s["index"]],
                    "event_index": s["index"],
                }
                for s in skeletons
                if s["exclusion"] == "" and s["trigger_minute"] is not None
            ]
        )

        tick_source = ParquetTickSource(tick_path) if tick_path.is_dir() else CsvTickSource(tick_path)

        invalid_rows = _stream_minutes(
            tick_source,
            run_dir / "minute_index.bin",
            run_dir / "minute_quotes.csv.gz",
            watches,
            tracker,
        )

        idx = MinuteIndex(run_dir / "minute_index.bin")
        mb_bid = idx.median_of_column("bid")
        mb_ask = idx.median_of_column("ask")
        observed_minutes = len(idx)

        del m1df, events, events_df
        gc.collect()
        try:
            peak_rss = psutil.Process().memory_info().rss
        except Exception:
            peak_rss = None

        vm = psutil.virtual_memory()
        disk = psutil.disk_usage(str(run_dir))
        environment = {
            "memory_total_bytes": vm.total,
            "memory_available_bytes": vm.available,
            "disk_free_bytes": disk.free,
            "tick_timezone_convention": "naive UTC",
            "m1_timezone_convention": "naive UTC bars",
            "projection_timezone": "America/New_York",
        }

        _finalize_prep(
            prep_dir=run_dir,
            identity=identity,
            skeletons=skeletons,
            market=market,
            mb_bid=mb_bid,
            mb_ask=mb_ask,
            idx=idx,
            tracker=tracker,
            stop_fills=watches.fills,
            environment=environment,
            peak_rss=peak_rss,
            invalid_rows=invalid_rows,
            elapsed_s=time.time() - t0,
        )
        del idx
        gc.collect()

        rec.complete(
            extra={
                "preparation_identity": identity.identity,
                "preparation_hash": identity.hash,
                "mode": "built",
            }
        )

        os.rename(run_dir, canonical_dir)
    except BaseException as exc:
        category = classify_infrastructure_failure(exc)
        if rec.state == "RUNNING":
            rec.invalidate(reason=category)
        raise ExecutionInfrastructureFailure(
            category, f"Stage 1 failed for {market}: {exc}"
        ) from exc

    valid_after, reason_after = is_valid_prep(canonical_dir, identity)
    if not valid_after:
        raise ExecutionInfrastructureFailure(
            "PREPARATION_INTEGRITY_FAILURE",
            f"materialized prep failed post-build validation: {reason_after}",
        )

    return {
        "market": market,
        "mode": "built",
        "prep_dir": str(canonical_dir),
        "preparation_identity": identity.identity,
        "preparation_hash": identity.hash,
        "v2_0_1_protocol_sha256": v2_0_1_protocol_sha256,
        "peak_rss_bytes": peak_rss,
        "observed_minutes": observed_minutes,
    }