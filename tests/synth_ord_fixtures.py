"""Synthetic, deterministic ORD staged-execution fixtures (test-only).

Generates frozen-format M1 / tick / event-table inputs for a single London
market (XAUUSD) across five event scenarios on four trading days:

  E1  2024-06-10  long  -> HORIZON exit (entry 07:31 exact, exit 09:31 exact)
  E2  2024-06-11  long  -> STRUCTURAL_INVALIDATION stop (trigger 07:32, fill
                           at first tick bid <= high_or in the trigger minute)
  E3  2024-06-11  long  -> EXCLUDED_RANGE_MISMATCH (persisted width 2.5 vs 2.0)
  E4  2024-06-12  long  -> EXCLUDED_RANGE_RECONSTRUCTION (no M1 bars)
  E5  2024-06-13  long  -> EXCLUDED_HORIZON_INCOMPLETE (OR bars only)

Dates are chosen in EDT (UTC-4), so the London OR window 03:00-03:29 ET maps to
UTC 07:00-07:29; anchors are at UTC 07:30; T_B = 07:31; horizon = 09:31.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

OR_HIGH_TOL_SMALL = 1.0e-4

EVENT_COLUMNS = [
    "market", "trading_day", "direction", "type", "anchor_ts", "entry_close",
    "horizon_close", "response", "invalidated", "horizon_complete",
    "mfe_from_entry", "range_width", "range_norm_return",
]

TICK_HEADERLESS = True


def _or_bars(day: str, low: float, high: float, close: float) -> list[tuple]:
    bars = []
    for minute in range(0, 30):
        ts = datetime(int(day[:4]), int(day[4:6]), int(day[6:8]), 7, minute)
        bars.append((ts, close, high, low, close))
    return bars


def build_m1_file(path: Path) -> None:
    bars = []
    # Day 1 (2024-06-10): OR 100..110 (width 10), anchor close 115, horizon
    # closes 115 (no trigger).
    bars += _or_bars("20240610", 100.0, 110.0, 105.0)
    bars.append((datetime(2024, 6, 10, 7, 30), 110.1, 115.0, 110.1, 115.0))
    for minute in range(31, 151):  # 07:31 .. 09:30
        bars.append((datetime(2024, 6, 10, 7, 0) + timedelta(minutes=minute),
                     115.0, 121.0, 114.9, 115.0))
    bars.append((datetime(2024, 6, 10, 9, 31), 115.0, 121.0, 114.9, 115.0))
    # Day 2 (2024-06-11): OR 200..202 (width 2), anchor close 203, trigger bar
    # at 07:32 (close 201.5 <= high_or 202), full horizon present.
    bars += _or_bars("20240611", 200.0, 202.0, 201.0)
    bars.append((datetime(2024, 6, 11, 7, 30), 202.5, 204.0, 202.5, 203.0))
    bars.append((datetime(2024, 6, 11, 7, 31), 203.0, 203.5, 202.8, 203.2))
    bars.append((datetime(2024, 6, 11, 7, 32), 203.0, 203.0, 201.0, 201.5))
    for minute in range(33, 151):  # 07:33 .. 09:30
        bars.append((datetime(2024, 6, 11, 7, 0) + timedelta(minutes=minute),
                     201.0, 201.5, 200.5, 201.0))
    bars.append((datetime(2024, 6, 11, 9, 31), 201.0, 201.5, 200.5, 201.0))
    # Day 4 (2024-06-13): OR only (no anchor / no horizon bars).
    bars += _or_bars("20240613", 50.0, 60.0, 55.0)

    bars.sort(key=lambda b: b[0])
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write("timestamp,open,high,low,close,volume\n")
        for ts, o, h, l, c in bars:
            f.write(f"{ts.strftime('%Y-%m-%d %H:%M:%S')},{o},{h},{l},{c},10\n")


def build_tick_file(path: Path) -> None:
    lines = []
    for minute in range(31, 152):  # 07:31 .. 09:31 UTC
        ts = datetime(2024, 6, 10, 7, 31) + timedelta(minutes=minute - 31)
        lines.append(
            f"{ts.strftime('%Y%m%d')},{ts.strftime('%H:%M:%S')},"
            f"120.0,120.1,120.05,1"
        )
    lines.append("20240611,07:31:00,203.0,203.1,203.05,1")
    lines.append("20240611,07:32:00,200.5,200.6,200.55,1")
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_event_table(path: Path, market: str = "XAUUSD") -> None:
    rows = [
        {
            "market": market, "trading_day": "2024-06-10 00:00:00-04:00",
            "direction": "long", "type": "treatment",
            "anchor_ts": "2024-06-10T07:30:00", "entry_close": 115.0,
            "horizon_close": 115.0, "response": 0.0, "invalidated": False,
            "horizon_complete": True, "mfe_from_entry": 0.0, "range_width": 10.0,
            "range_norm_return": 0.0,
        },
        {
            "market": market, "trading_day": "2024-06-11 00:00:00-04:00",
            "direction": "long", "type": "treatment",
            "anchor_ts": "2024-06-11T07:30:00", "entry_close": 203.0,
            "horizon_close": 202.0, "response": 0.0, "invalidated": True,
            "horizon_complete": True, "mfe_from_entry": 0.0, "range_width": 2.0,
            "range_norm_return": 0.0,
        },
        {
            "market": market, "trading_day": "2024-06-11 00:00:00-04:00",
            "direction": "long", "type": "treatment",
            "anchor_ts": "2024-06-11T07:45:00", "entry_close": 203.0,
            "horizon_close": 203.0, "response": 0.0, "invalidated": True,
            "horizon_complete": True, "mfe_from_entry": 0.0, "range_width": 2.5,
            "range_norm_return": 0.0,
        },
        {
            "market": market, "trading_day": "2024-06-12 00:00:00-04:00",
            "direction": "long", "type": "treatment",
            "anchor_ts": "2024-06-12T07:30:00", "entry_close": 100.0,
            "horizon_close": 100.0, "response": 0.0, "invalidated": True,
            "horizon_complete": True, "mfe_from_entry": 0.0, "range_width": 10.0,
            "range_norm_return": 0.0,
        },
        {
            "market": market, "trading_day": "2024-06-13 00:00:00-04:00",
            "direction": "long", "type": "treatment",
            "anchor_ts": "2024-06-13T07:30:00", "entry_close": 55.0,
            "horizon_close": 55.0, "response": 0.0, "invalidated": True,
            "horizon_complete": False, "mfe_from_entry": 0.0, "range_width": 10.0,
            "range_norm_return": 0.0,
        },
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(",".join(EVENT_COLUMNS) + "\n")
        for r in rows:
            f.write(",".join(str(r[c]) for c in EVENT_COLUMNS) + "\n")


def build_fixture(base: Path, market: str = "XAUUSD") -> dict:
    """Writes m1.csv / <market>_mt5_ticks.csv / event_table_all_markets.csv and
    returns the paths + expected facts used by the assertions."""
    base = Path(base)
    m1_path = base / f"{market}_M1.csv"
    tick_path = base / f"{market}_mt5_ticks.csv"
    event_path = base / "event_table_all_markets.csv"
    build_m1_file(m1_path)
    build_tick_file(tick_path)
    build_event_table(event_path, market)
    return {
        "market": market,
        "m1": m1_path,
        "tick": tick_path,
        "events": event_path,
        "n_events": 5,
        "n_traded": 2,
        "n_excluded": 3,
        "n_minutes": 123,
        "market_median_bid": 120.0,
        "market_median_ask": 120.1,
        "or_high_day1": 110.0,
        "or_low_day1": 100.0,
    }