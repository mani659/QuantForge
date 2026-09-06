"""
FB-001 ORB — V38A Stage 2 Structural Validation Implementation

Governing registration: FB-001-ORB-V38A-REG-V1-r1
Registration SHA: 04e9f804cca93d64ea18396abf5d25d2b968df974ee505f2b0866104e1af8086

This implementation reproduces the frozen FB-001 ORB decision process
exactly as specified in V1-r1. It is used for structural validation only.
No economic metrics are computed or reported.
"""

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from enum import Enum
from typing import List, Optional, Tuple
import hashlib


class Direction(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class ExitType(Enum):
    RETRACE = "RETRACE"
    SESSION_CLOSE = "SESSION_CLOSE"


class PositionState(Enum):
    FLAT = "FLAT"
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass(frozen=True)
class Bar:
    """Canonical M1 bar: [bar_open_time, bar_close_time)"""
    bar_open_time: datetime
    open: float
    high: float
    low: float
    close: float

    @property
    def bar_close_time(self) -> datetime:
        return self.bar_open_time + timedelta(minutes=1)

    def is_malformed(self) -> bool:
        return self.open > self.high or self.close < self.low or self.low > self.high


@dataclass(frozen=True)
class StructuralOutcome:
    """Structural output for one session — no economic metrics."""
    session_date: datetime
    has_opportunity: bool
    direction: Optional[Direction] = None
    signal_bar_open_time: Optional[datetime] = None
    entry_bar_open_time: Optional[datetime] = None
    exit_type: Optional[ExitType] = None
    exit_bar_open_time: Optional[datetime] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    or_high: Optional[float] = None
    or_low: Optional[float] = None
    retrace_barrier: Optional[float] = None
    position_state_transitions: Optional[Tuple[str, ...]] = None


def make_bar(open_time_str: str, o: float, h: float, l: float, c: float) -> Bar:
    """Helper to create a Bar from a time string and prices."""
    if isinstance(open_time_str, datetime):
        return Bar(bar_open_time=open_time_str, open=o, high=h, low=l, close=c)
    return Bar(
        bar_open_time=datetime.strptime(open_time_str, "%Y-%m-%d %H:%M:%S"),
        open=o, high=h, low=l, close=c,
    )


def filter_duplicate_bars(bars: List[Bar]) -> List[Bar]:
    """V1-r1 §15: If two bars share bar_close_time, use first occurrence."""
    seen_close_times = set()
    result = []
    for bar in bars:
        if bar.bar_close_time not in seen_close_times:
            seen_close_times.add(bar.bar_close_time)
            result.append(bar)
    return result


def reorder_bars(bars: List[Bar]) -> List[Bar]:
    """V1-r1 §15: Reorder by bar_close_time before processing."""
    return sorted(bars, key=lambda b: b.bar_close_time)


def process_session(bars: List[Bar], session_date: datetime,
                    early_close_time: Optional[time] = None) -> StructuralOutcome:
    """
    Process one trading session according to FB-001 ORB V1-r1.

    Args:
        bars: All M1 bars for the session (may be out of order, may have duplicates)
        session_date: The trading session date
        early_close_time: If early close, the close time (ET). None = regular 16:00.

    Returns:
        StructuralOutcome with all structural fields.
    """
    # Phase 1: Data quality — filter duplicates, reorder
    bars = filter_duplicate_bars(bars)
    bars = reorder_bars(bars)

    # Determine session boundaries
    session_start = datetime.combine(session_date.date(), time(9, 30))
    if early_close_time is not None:
        session_end = datetime.combine(session_date.date(), early_close_time)
    else:
        session_end = datetime.combine(session_date.date(), time(16, 0))

    # Filter bars to session
    session_bars = [b for b in bars if session_start <= b.bar_open_time < session_end]

    # Filter malformed bars
    valid_bars = [b for b in session_bars if not b.is_malformed()]

    # Phase 2: Opening range [09:30:00, 10:00:00) — need exactly 30 bars
    or_start = datetime.combine(session_date.date(), time(9, 30))
    or_end = datetime.combine(session_date.date(), time(10, 0))

    or_bars = [b for b in valid_bars if or_start <= b.bar_open_time < or_end]

    if len(or_bars) < 30:
        return StructuralOutcome(
            session_date=session_date,
            has_opportunity=False,
        )

    # Calculate OR high/low from exactly 30 bars
    or_high = max(b.high for b in or_bars[:30])
    or_low = min(b.low for b in or_bars[:30])

    # Phase 3: Signal bar — first completed bar with bar_open_time >= 10:00
    signal_candidates = [b for b in valid_bars if b.bar_open_time >= or_end]

    if not signal_candidates:
        return StructuralOutcome(
            session_date=session_date,
            has_opportunity=False,
            or_high=or_high,
            or_low=or_low,
        )

    signal_bar = signal_candidates[0]

    # Signal conditions (strict exceedance required)
    if signal_bar.close > or_high:
        direction = Direction.LONG
        retrace_barrier = or_high
    elif signal_bar.close < or_low:
        direction = Direction.SHORT
        retrace_barrier = or_low
    else:
        # No signal — close within or on range boundary
        return StructuralOutcome(
            session_date=session_date,
            has_opportunity=False,
            or_high=or_high,
            or_low=or_low,
        )

    # Phase 4: Entry — market order at next bar open
    entry_candidates = [b for b in valid_bars if b.bar_open_time >= signal_bar.bar_close_time]

    if not entry_candidates:
        return StructuralOutcome(
            session_date=session_date,
            has_opportunity=False,
            direction=direction,
            signal_bar_open_time=signal_bar.bar_open_time,
            or_high=or_high,
            or_low=or_low,
            retrace_barrier=retrace_barrier,
        )

    entry_bar = entry_candidates[0]
    entry_price = entry_bar.open

    # Phase 5: Exit — scan subsequent bars for retrace or session close
    # "Subsequent" means bar_open_time > entry execution bar's bar_close_time
    exit_scan_start = entry_bar.bar_close_time

    # Identify the final session bar
    if early_close_time is not None:
        final_session_bar_time = datetime.combine(session_date.date(), early_close_time) - timedelta(minutes=1)
    else:
        final_session_bar_time = datetime.combine(session_date.date(), time(15, 59))

    # Find the actual final session bar (may be malformed → use last valid bar)
    final_session_bar = None
    for bar in reversed(valid_bars):
        if bar.bar_open_time <= final_session_bar_time:
            final_session_bar = bar
            break

    exit_bar = None
    exit_type = None

    for bar in valid_bars:
        if bar.bar_open_time <= exit_scan_start:
            continue

        # Check if this is the final session bar
        is_final_session_bar = (final_session_bar is not None and bar.bar_open_time == final_session_bar.bar_open_time)

        # Check retrace condition
        if direction == Direction.LONG:
            retrace_trigger = bar.close <= or_high
        else:
            retrace_trigger = bar.close >= or_low

        if is_final_session_bar:
            # Session close governs — regardless of retrace
            exit_bar = bar
            exit_type = ExitType.SESSION_CLOSE
            break

        if retrace_trigger:
            # Retrace detected — but check if session close also applies
            # If this bar IS the final session bar, session close governs
            # (already handled above since is_final_session_bar would be True)
            exit_bar = bar
            exit_type = ExitType.RETRACE
            break

    if exit_bar is None:
        # No exit found — structurally incomplete (should not happen in normal data)
        return StructuralOutcome(
            session_date=session_date,
            has_opportunity=False,
            direction=direction,
            signal_bar_open_time=signal_bar.bar_open_time,
            entry_bar_open_time=entry_bar.bar_open_time,
            or_high=or_high,
            or_low=or_low,
            retrace_barrier=retrace_barrier,
        )

    exit_price = exit_bar.open

    # Phase 6: State transitions
    transitions = ("FLAT", direction.value, "FLAT")

    return StructuralOutcome(
        session_date=session_date,
        has_opportunity=True,
        direction=direction,
        signal_bar_open_time=signal_bar.bar_open_time,
        entry_bar_open_time=entry_bar.bar_open_time,
        exit_type=exit_type,
        exit_bar_open_time=exit_bar.bar_open_time,
        entry_price=entry_price,
        exit_price=exit_price,
        or_high=or_high,
        or_low=or_low,
        retrace_barrier=retrace_barrier,
        position_state_transitions=transitions,
    )


def structural_hash(outcome: StructuralOutcome) -> str:
    """Compute a deterministic hash of a structural outcome."""
    parts = [
        str(outcome.session_date),
        str(outcome.has_opportunity),
        str(outcome.direction),
        str(outcome.signal_bar_open_time),
        str(outcome.entry_bar_open_time),
        str(outcome.exit_type),
        str(outcome.exit_bar_open_time),
        f"{outcome.entry_price:.10f}" if outcome.entry_price else "None",
        f"{outcome.exit_price:.10f}" if outcome.exit_price else "None",
        f"{outcome.or_high:.10f}" if outcome.or_high else "None",
        f"{outcome.or_low:.10f}" if outcome.or_low else "None",
    ]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]
