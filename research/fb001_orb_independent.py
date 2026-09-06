"""
FB-001 ORB — Independent Reproducibility Implementation

Governing registration: FB-001-ORB-V38A-REG-V1-r1
Registration SHA: 04e9f804cca93d64ea18396abf5d25d2b968df974ee505f2b0866104e1af8086

This is a SECOND, INDEPENDENT implementation derived from V1-r1 directly,
NOT from fb001_orb_structural.py. Different code structure, same logic.
Used only for reproducibility comparison.
"""

from datetime import datetime, time, timedelta
from typing import List, Dict, Optional, Tuple
import hashlib


def _bar_close_time(bar_open_time: datetime) -> datetime:
    """V1-r1 §3: bar_close_time = bar_open_time + 1 minute."""
    return bar_open_time + timedelta(minutes=1)


def _is_malformed(o: float, h: float, l: float, c: float) -> bool:
    """V1-r1 §15: open > high or close < low."""
    return o > h or c < l


def _deduplicate(bars: List[Dict]) -> List[Dict]:
    """V1-r1 §15: first occurrence wins for duplicate bar_close_time."""
    seen = set()
    result = []
    for b in bars:
        close_t = _bar_close_time(b["open_time"])
        if close_t not in seen:
            seen.add(close_t)
            result.append(b)
    return result


def _reorder(bars: List[Dict]) -> List[Dict]:
    """V1-r1 §15: reorder by bar_close_time."""
    return sorted(bars, key=lambda b: _bar_close_time(b["open_time"]))


def process_fb001(bars: List[Dict], session_date: datetime,
                  early_close: Optional[time] = None) -> Dict:
    """
    Independent FB-001 ORB processor.

    Args:
        bars: list of dicts with keys: open_time (datetime), o, h, l, c
        session_date: trading date
        early_close: early close time (ET) or None for regular

    Returns:
        dict with structural outcome fields
    """
    # Phase 1: Data quality
    bars = _deduplicate(bars)
    bars = _reorder(bars)

    # Session boundaries
    sess_start = datetime.combine(session_date.date(), time(9, 30))
    sess_end = datetime.combine(session_date.date(), early_close or time(16, 0))

    # Filter to session, exclude malformed
    session = []
    for b in bars:
        if sess_start <= b["open_time"] < sess_end:
            if not _is_malformed(b["o"], b["h"], b["l"], b["c"]):
                session.append(b)

    # Phase 2: Opening range [09:30, 10:00) — exactly 30 bars
    or_start = datetime.combine(session_date.date(), time(9, 30))
    or_end = datetime.combine(session_date.date(), time(10, 0))
    or_bars = [b for b in session if or_start <= b["open_time"] < or_end]

    if len(or_bars) < 30:
        return {"session_date": session_date, "has_opportunity": False}

    or_high = max(b["h"] for b in or_bars[:30])
    or_low = min(b["l"] for b in or_bars[:30])

    # Phase 3: Signal — first bar with open_time >= 10:00
    sig_candidates = [b for b in session if b["open_time"] >= or_end]
    if not sig_candidates:
        return {"session_date": session_date, "has_opportunity": False,
                "or_high": or_high, "or_low": or_low}

    sig = sig_candidates[0]

    if sig["c"] > or_high:
        direction = "LONG"
        retrace_barrier = or_high
    elif sig["c"] < or_low:
        direction = "SHORT"
        retrace_barrier = or_low
    else:
        return {"session_date": session_date, "has_opportunity": False,
                "or_high": or_high, "or_low": or_low}

    # Phase 4: Entry — next bar open (bar with open_time >= signal bar close time)
    sig_close = _bar_close_time(sig["open_time"])
    entry_candidates = [b for b in session if b["open_time"] >= sig_close]
    if not entry_candidates:
        return {"session_date": session_date, "has_opportunity": False,
                "direction": direction, "signal_bar": sig["open_time"],
                "or_high": or_high, "or_low": or_low,
                "retrace_barrier": retrace_barrier}

    entry = entry_candidates[0]
    entry_price = entry["o"]

    # Phase 5: Exit scan
    entry_close = _bar_close_time(entry["open_time"])

    # Final session bar
    if early_close is not None:
        final_time = datetime.combine(session_date.date(), early_close) - timedelta(minutes=1)
    else:
        final_time = datetime.combine(session_date.date(), time(15, 59))

    # Find last valid bar at or before final_time
    final_bar = None
    for b in reversed(session):
        if b["open_time"] <= final_time:
            final_bar = b
            break

    exit_bar = None
    exit_type = None

    for b in session:
        if b["open_time"] <= entry_close:
            continue

        is_final = (final_bar is not None and b["open_time"] == final_bar["open_time"])

        if direction == "LONG":
            retrace = b["c"] <= or_high
        else:
            retrace = b["c"] >= or_low

        if is_final:
            exit_bar = b
            exit_type = "SESSION_CLOSE"
            break

        if retrace:
            exit_bar = b
            exit_type = "RETRACE"
            break

    if exit_bar is None:
        return {"session_date": session_date, "has_opportunity": False,
                "direction": direction, "signal_bar": sig["open_time"],
                "entry_bar": entry["open_time"],
                "or_high": or_high, "or_low": or_low,
                "retrace_barrier": retrace_barrier}

    return {
        "session_date": session_date,
        "has_opportunity": True,
        "direction": direction,
        "signal_bar": sig["open_time"],
        "entry_bar": entry["open_time"],
        "exit_type": exit_type,
        "exit_bar": exit_bar["open_time"],
        "entry_price": entry_price,
        "exit_price": exit_bar["o"],
        "or_high": or_high,
        "or_low": or_low,
        "retrace_barrier": retrace_barrier,
        "transitions": ("FLAT", direction, "FLAT"),
    }


def structural_hash_ind(outcome: Dict) -> str:
    """Deterministic hash of independent implementation output."""
    parts = [
        str(outcome.get("session_date")),
        str(outcome.get("has_opportunity")),
        str(outcome.get("direction")),
        str(outcome.get("signal_bar")),
        str(outcome.get("entry_bar")),
        str(outcome.get("exit_type")),
        str(outcome.get("exit_bar")),
        f"{outcome.get('entry_price', 0):.10f}",
        f"{outcome.get('exit_price', 0):.10f}",
        f"{outcome.get('or_high', 0):.10f}",
        f"{outcome.get('or_low', 0):.10f}",
    ]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
