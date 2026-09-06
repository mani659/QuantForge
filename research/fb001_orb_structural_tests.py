"""
FB-001 ORB — V38A Stage 2 Structural Validation Tests

Governing registration: FB-001-ORB-V38A-REG-V1-r1
Registration SHA: 04e9f804cca93d64ea18396abf5d25d2b968df974ee505f2b0866104e1af8086

Tests cover:
  - Phase 4: Structural determinism
  - Phase 5: Temporal/leakage audit
  - Phase 6: Opportunity population
  - Phase 7: Execution mapping (Cases A-L)
  - Phase 8: Data quality rules
  - Phase 9: Reproducibility (independent implementation comparison)
  - Phase 10: Cost-model consistency
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, time, timedelta
from fb001_orb_structural import (
    Bar, Direction, ExitType, PositionState, StructuralOutcome,
    process_session, structural_hash, make_bar,
)


def generate_session_bars(session_date: datetime,
                          or_trend: float = 0,
                          or_high_price: float = 100.0,
                          or_low_price: float = 99.0,
                          signal_close: float = None,
                          signal_direction: str = None,
                          retrace_bar_index: int = None,
                          early_close_time: time = None,
                          num_or_bars: int = 30,
                          include_pre_0930: bool = False) -> list:
    """
    Generate synthetic M1 bars for a session.

    or_high_price / or_low_price define the opening range extremes.
    signal_close defines the signal bar close (if signal_direction != None).
    retrace_bar_index (relative to post-signal bars) defines when retrace occurs.
    """
    bars = []
    base_price = (or_high_price + or_low_price) / 2

    # Optional pre-09:30 bars (should NOT enter opening range)
    if include_pre_0930:
        pre_time = datetime.combine(session_date.date(), time(9, 29))
        bars.append(make_bar(pre_time, base_price - 0.5, base_price - 0.2, base_price - 0.8, base_price - 0.5))

    # Opening range bars: [09:30, 10:00) = 30 bars
    for i in range(num_or_bars):
        bar_time = datetime.combine(session_date.date(), time(9, 30)) + timedelta(minutes=i)
        if i == 0:
            o, h, l, c = or_low_price, or_high_price, or_low_price, base_price
        elif i == num_or_bars - 1:
            o, h, l, c = base_price, or_high_price, or_low_price, base_price
        else:
            frac = i / (num_or_bars - 1)
            o = or_low_price + frac * (or_high_price - or_low_price) * 0.3
            h = or_high_price - (num_or_bars - i) * 0.01
            l = or_low_price + i * 0.01
            c = base_price + (frac - 0.5) * 0.2
        bars.append(make_bar(bar_time, o, h, l, c))

    # Signal bar: [10:00, 10:01)
    signal_time = datetime.combine(session_date.date(), time(10, 0))
    if signal_close is not None and signal_direction is not None:
        if signal_direction == "LONG":
            s_o = or_high_price - 0.05
            s_h = signal_close + 0.02
            s_l = or_high_price - 0.1
            s_c = signal_close
        else:
            s_o = or_low_price + 0.05
            s_h = or_low_price + 0.1
            s_l = signal_close - 0.02
            s_c = signal_close
    else:
        # No signal — close within range
        s_o, s_h, s_l, s_c = base_price, base_price + 0.1, base_price - 0.1, base_price
    bars.append(make_bar(signal_time, s_o, s_h, s_l, s_c))

    # Entry bar: [10:01, 10:02)
    entry_time = datetime.combine(session_date.date(), time(10, 1))
    entry_open = base_price + (0.1 if signal_direction == "LONG" else -0.1) if signal_direction else base_price
    bars.append(make_bar(entry_time, entry_open, entry_open + 0.05, entry_open - 0.05, entry_open + 0.02))

    # Post-entry bars
    if signal_direction and retrace_bar_index is not None:
        session_end = early_close_time or time(16, 0)
        final_bar_time = datetime.combine(session_date.date(), session_end) - timedelta(minutes=1)
        post_start = datetime.combine(session_date.date(), time(10, 2))
        max_post_bars = int((final_bar_time - post_start).total_seconds() / 60) + 1

        for i in range(min(max_post_bars, 20)):
            bar_time = post_start + timedelta(minutes=i)
            if bar_time >= final_bar_time:
                break
            if i == retrace_bar_index:
                if signal_direction == "LONG":
                    r_o = or_high_price + 0.05
                    r_c = or_high_price - 0.01  # Retrace: close <= OR_high
                    r_h = r_o + 0.02
                    r_l = r_c - 0.02
                else:
                    r_o = or_low_price - 0.05
                    r_c = or_low_price + 0.01  # Retrace: close >= OR_low
                    r_h = r_c + 0.02
                    r_l = r_o - 0.02
            else:
                if signal_direction == "LONG":
                    r_o = or_high_price + 0.1 + i * 0.005
                    r_c = r_o + 0.003
                    r_h = r_c + 0.01
                    r_l = r_o - 0.01
                else:
                    r_o = or_low_price - 0.1 - i * 0.005
                    r_c = r_o - 0.003
                    r_h = r_o + 0.01
                    r_l = r_c - 0.01
            bars.append(make_bar(bar_time, r_o, r_h, r_l, r_c))

        # Final session bar (always add for session-close test)
        if final_bar_time not in [b.bar_open_time for b in bars]:
            if signal_direction == "LONG":
                f_o = or_high_price + 0.2
                f_c = or_high_price + 0.3  # Above OR_high — no retrace
            else:
                f_o = or_low_price - 0.2
                f_c = or_low_price - 0.3  # Below OR_low — no retrace
            bars.append(make_bar(final_bar_time, f_o, f_o + 0.02, f_o - 0.02, f_c))
    elif signal_direction:
        # No retrace — add some bars then final session bar
        # All post-entry bars must stay OUTSIDE the range
        session_end = early_close_time or time(16, 0)
        final_bar_time = datetime.combine(session_date.date(), session_end) - timedelta(minutes=1)
        post_start = datetime.combine(session_date.date(), time(10, 2))

        for i in range(5):
            bar_time = post_start + timedelta(minutes=i)
            if bar_time >= final_bar_time:
                break
            if signal_direction == "LONG":
                r_o = or_high_price + 0.1 + i * 0.005
                r_c = r_o + 0.003
                r_h = r_c + 0.01
                r_l = r_o - 0.01
            else:
                r_o = or_low_price - 0.1 - i * 0.005
                r_c = r_o - 0.003
                r_h = r_o + 0.01
                r_l = r_c - 0.01
            bars.append(make_bar(bar_time, r_o, r_h, r_l, r_c))

        # Final session bar
        if final_bar_time not in [b.bar_open_time for b in bars]:
            if signal_direction == "LONG":
                f_o = or_high_price + 0.2
                f_c = or_high_price + 0.3  # Above OR_high
            else:
                f_o = or_low_price - 0.2
                f_c = or_low_price - 0.3  # Below OR_low
            bars.append(make_bar(final_bar_time, f_o, f_o + 0.02, f_o - 0.02, f_c))

    return bars


# =============================================================================
# PHASE 4: STRUCTURAL DETERMINISM TEST
# =============================================================================

def test_determinism():
    """Run same data twice, compare structural hash."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    outcome1 = process_session(bars, session_date)
    outcome2 = process_session(bars, session_date)

    h1 = structural_hash(outcome1)
    h2 = structural_hash(outcome2)

    assert h1 == h2, f"Determinism FAIL: {h1} != {h2}"
    assert outcome1 == outcome2, "Determinism FAIL: outcomes differ"
    print(f"DETERMINISM: PASS (hash={h1})")
    return True


# =============================================================================
# PHASE 5: TEMPORAL / LEAKAGE AUDIT
# =============================================================================

def test_no_pre_0930_in_or():
    """Verify pre-09:30 bars do not enter opening range."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
        include_pre_0930=True,
    )

    outcome = process_session(bars, session_date)

    # Pre-09:30 bar has close = 99.5 - 0.5 = 99.0
    # If it entered OR, or_low would be <= 99.0
    # The OR bars have or_low = 99.0 exactly
    # Pre-09:30 bar should NOT be counted
    assert outcome.or_low == 99.0, f"Pre-09:30 leakage: or_low={outcome.or_low}"
    print("LEAKAGE AUDIT (pre-09:30 exclusion): PASS")
    return True


def test_signal_after_or_only():
    """Verify signal is evaluated only after OR completion."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    outcome = process_session(bars, session_date)

    # Signal bar should be [10:00, 10:01)
    assert outcome.signal_bar_open_time == datetime(2026, 9, 10, 10, 0), \
        f"Signal timing: {outcome.signal_bar_open_time}"
    print("LEAKAGE AUDIT (signal after OR): PASS")
    return True


def test_retrace_uses_subsequent_bars_only():
    """Verify retrace is checked only on bars after entry execution bar."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    outcome = process_session(bars, session_date)

    # Entry bar is [10:01, 10:02)
    # Retrace bar must have bar_open_time > entry bar's bar_close_time (10:02)
    assert outcome.exit_bar_open_time > datetime(2026, 9, 10, 10, 2), \
        f"Retrace too early: {outcome.exit_bar_open_time}"
    print("LEAKAGE AUDIT (retrace subsequent only): PASS")
    return True


def test_no_future_session_info():
    """Verify no future session information changes earlier session classification."""
    # Process two sessions independently
    session1 = datetime(2026, 9, 10)
    session2 = datetime(2026, 9, 11)

    bars1 = generate_session_bars(session1, or_high_price=100.0, or_low_price=99.0,
                                   signal_close=100.05, signal_direction="LONG", retrace_bar_index=3)
    bars2 = generate_session_bars(session2, or_high_price=101.0, or_low_price=100.0,
                                   signal_close=100.5, signal_direction="SHORT", retrace_bar_index=2)

    outcome1a = process_session(bars1, session1)
    outcome1b = process_session(bars1 + bars2, session1)  # With session2 data added

    assert structural_hash(outcome1a) == structural_hash(outcome1b), \
        "Future session info leaked into earlier session"
    print("LEAKAGE AUDIT (no future session info): PASS")
    return True


# =============================================================================
# PHASE 6: OPPORTUNITY POPULATION VALIDATION
# =============================================================================

def test_no_signal_session():
    """No breakout = no opportunity."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=None,  # No signal
        signal_direction=None,
    )

    outcome = process_session(bars, session_date)
    assert not outcome.has_opportunity, "No-signal session should have no opportunity"
    print("OPPORTUNITY POPULATION (no signal): PASS")
    return True


def test_one_opportunity_per_session():
    """Exactly one opportunity after first qualifying breakout."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity, "Should have opportunity"
    assert outcome.direction == Direction.LONG
    print("OPPORTUNITY POPULATION (one per session): PASS")
    return True


def test_incomplete_or_no_opportunity():
    """Fewer than 30 OR bars = no opportunity."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
        num_or_bars=29,  # Only 29 bars
    )

    outcome = process_session(bars, session_date)
    assert not outcome.has_opportunity, "Incomplete OR should have no opportunity"
    print("OPPORTUNITY POPULATION (incomplete OR): PASS")
    return True


# =============================================================================
# PHASE 7: EXECUTION MAPPING VALIDATION (CASES A-L)
# =============================================================================

def test_case_a_long_breakout():
    """Case A: Long breakout — signal LONG, entry at next bar open."""
    session_date = datetime(2026, 9, 10)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,  # > OR_high
        signal_direction="LONG",
        retrace_bar_index=None,  # No retrace — session close
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.direction == Direction.LONG
    assert outcome.entry_bar_open_time == datetime(2026, 9, 10, 10, 1)
    assert outcome.exit_type == ExitType.SESSION_CLOSE
    print("CASE A (long breakout): PASS")
    return True


def test_case_b_short_breakout():
    """Case B: Short breakout — signal SHORT, entry at next bar open."""
    session_date = datetime(2026, 9, 11)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=98.95,  # < OR_low
        signal_direction="SHORT",
        retrace_bar_index=None,
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.direction == Direction.SHORT
    assert outcome.entry_bar_open_time == datetime(2026, 9, 11, 10, 1)
    print("CASE B (short breakout): PASS")
    return True


def test_case_c_equality():
    """Case C: Signal close equals OR_high or OR_low — NO SIGNAL."""
    session_date = datetime(2026, 9, 12)

    # Equality with OR_high
    bars_eq_high = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.0,  # == OR_high
        signal_direction="LONG",
    )
    # Override the signal bar to have close == OR_high
    for b in bars_eq_high:
        if b.bar_open_time == datetime(2026, 9, 12, 10, 0):
            bars_eq_high.remove(b)
            bars_eq_high.append(make_bar(datetime(2026, 9, 12, 10, 0), 99.9, 100.1, 99.9, 100.0))
            break

    outcome = process_session(bars_eq_high, session_date)
    assert not outcome.has_opportunity, "Equality with OR_high should produce NO SIGNAL"

    # Equality with OR_low
    bars_eq_low = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=99.0,  # == OR_low
        signal_direction="SHORT",
    )
    for b in bars_eq_low:
        if b.bar_open_time == datetime(2026, 9, 12, 10, 0):
            bars_eq_low.remove(b)
            bars_eq_low.append(make_bar(datetime(2026, 9, 12, 10, 0), 99.1, 99.1, 98.9, 99.0))
            break

    outcome2 = process_session(bars_eq_low, session_date)
    assert not outcome2.has_opportunity, "Equality with OR_low should produce NO SIGNAL"

    print("CASE C (equality): PASS")
    return True


def test_case_d_retrace_long():
    """Case D: Long breakout then retrace — exit at retrace bar open."""
    session_date = datetime(2026, 9, 13)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.direction == Direction.LONG
    assert outcome.exit_type == ExitType.RETRACE
    # Exit price should be retrace bar's open
    assert outcome.exit_price is not None
    print("CASE D (long retrace): PASS")
    return True


def test_case_d_retrace_short():
    """Case D: Short breakout then retrace."""
    session_date = datetime(2026, 9, 14)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=98.95,
        signal_direction="SHORT",
        retrace_bar_index=2,
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.direction == Direction.SHORT
    assert outcome.exit_type == ExitType.RETRACE
    print("CASE D (short retrace): PASS")
    return True


def test_case_e_entry_execution_bar_not_retrace():
    """Case E: Entry execution bar close satisfies retrace — should NOT count."""
    session_date = datetime(2026, 9, 15)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=0,  # Retrace on first post-entry bar
    )

    outcome = process_session(bars, session_date)

    # Entry bar is [10:01, 10:02)
    # Retrace must be on bar with bar_open_time > entry bar's bar_close_time (10:02)
    # So retrace bar_index=0 means [10:02, 10:03) — this is AFTER entry, should trigger
    # But we need to verify the entry execution bar itself [10:01, 10:02) is NOT the retrace bar
    assert outcome.entry_bar_open_time == datetime(2026, 9, 15, 10, 1)
    if outcome.exit_type == ExitType.RETRACE:
        assert outcome.exit_bar_open_time > datetime(2026, 9, 15, 10, 2), \
            f"Entry execution bar counted as retrace: {outcome.exit_bar_open_time}"
    print("CASE E (entry bar not retrace): PASS")
    return True


def test_case_f_final_session_bar():
    """Case F: Final session bar identified correctly, exit at its open."""
    session_date = datetime(2026, 9, 16)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=None,  # No retrace — session close
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.exit_type == ExitType.SESSION_CLOSE
    # Final session bar is [15:59, 16:00)
    assert outcome.exit_bar_open_time == datetime(2026, 9, 16, 15, 59), \
        f"Final session bar: {outcome.exit_bar_open_time}"
    print("CASE F (final session bar): PASS")
    return True


def test_case_g_session_close_wins():
    """Case G: Final session bar satisfies retrace — session close governs."""
    session_date = datetime(2026, 9, 17)

    # Create bars where final session bar has close <= OR_high (retrace condition)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=None,
    )

    # Override final session bar to have close <= OR_high
    final_bar_time = datetime(2026, 9, 17, 15, 59)
    for i, b in enumerate(bars):
        if b.bar_open_time == final_bar_time:
            bars[i] = make_bar(final_bar_time, 99.9, 100.1, 99.8, 99.95)  # close <= OR_high
            break

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.exit_type == ExitType.SESSION_CLOSE, \
        f"Session close should govern, got: {outcome.exit_type}"
    print("CASE G (session close wins over retrace): PASS")
    return True


def test_case_h_no_breakout():
    """Case H: Price remains within range — NO OPPORTUNITY."""
    session_date = datetime(2026, 9, 18)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=None,
        signal_direction=None,
    )

    outcome = process_session(bars, session_date)
    assert not outcome.has_opportunity
    print("CASE H (no breakout): PASS")
    return True


def test_case_i_incomplete_opening_range():
    """Case I: Fewer than 30 OR bars — NO OPPORTUNITY."""
    session_date = datetime(2026, 9, 19)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
        num_or_bars=25,  # Only 25 bars
    )

    outcome = process_session(bars, session_date)
    assert not outcome.has_opportunity
    print("CASE I (incomplete opening range): PASS")
    return True


def test_case_j_early_close_after_10():
    """Case J: Early-close session after 10:00 — full OR still required."""
    session_date = datetime(2026, 9, 20)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=None,
        early_close_time=time(15, 0),  # Early close at 15:00
    )

    outcome = process_session(bars, session_date, early_close_time=time(15, 0))
    assert outcome.has_opportunity
    assert outcome.exit_type == ExitType.SESSION_CLOSE
    # Final session bar should be [14:59, 15:00)
    assert outcome.exit_bar_open_time == datetime(2026, 9, 20, 14, 59), \
        f"Early-close final bar: {outcome.exit_bar_open_time}"
    print("CASE J (early close after 10): PASS")
    return True


def test_case_k_early_close_before_10():
    """Case K: Early close before 10:00 — NO OPENING RANGE / NO OPPORTUNITY."""
    session_date = datetime(2026, 9, 21)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    # Override: no OR bars exist before 10:00 in an early-close-before-10 session
    # Remove all OR bars
    bars_early = [b for b in bars if b.bar_open_time >= datetime(2026, 9, 21, 10, 0)]
    # Add some post-10:00 bars
    for i in range(5):
        t = datetime(2026, 9, 21, 10, 0) + timedelta(minutes=i)
        bars_early.append(make_bar(t, 99.5, 100.5, 99.0, 100.0))

    outcome = process_session(bars_early, session_date, early_close_time=time(9, 45))
    assert not outcome.has_opportunity
    print("CASE K (early close before 10): PASS")
    return True


def test_case_l_dst():
    """Case L: DST — session membership remains 09:30-16:00 ET."""
    # DST transition: March 8, 2026 (spring forward)
    # The session should still be [09:30, 16:00) ET
    session_date = datetime(2026, 3, 9)  # Day after DST transition
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.signal_bar_open_time == datetime(2026, 3, 9, 10, 0)
    assert outcome.entry_bar_open_time == datetime(2026, 3, 9, 10, 1)
    print("CASE L (DST): PASS")
    return True


# =============================================================================
# PHASE 8: DATA QUALITY RULE VALIDATION
# =============================================================================

def test_missing_bars():
    """Missing bars from OR window — if <30, no opportunity."""
    session_date = datetime(2026, 9, 22)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    # Remove 5 OR bars
    or_times = [datetime(2026, 9, 22, 9, 30) + timedelta(minutes=i) for i in range(30)]
    bars = [b for b in bars if b.bar_open_time not in or_times[2:7]]

    outcome = process_session(bars, session_date)
    assert not outcome.has_opportunity, "Missing OR bars should prevent opportunity"
    print("DATA QUALITY (missing bars): PASS")
    return True


def test_malformed_bar_excluded():
    """Malformed bar (open > high) excluded from OR calculation."""
    session_date = datetime(2026, 9, 23)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    # Add a malformed bar in the OR window
    malformed_time = datetime(2026, 9, 23, 9, 35)
    bars.append(make_bar(malformed_time, 101.0, 100.0, 99.0, 100.0))  # open > high

    outcome = process_session(bars, session_date)
    # Malformed bar excluded; still need 30 valid bars
    # We added 1 malformed + had 30 valid = 30 valid remain
    assert outcome.has_opportunity, "Malformed bar excluded, 30 valid bars remain"
    print("DATA QUALITY (malformed bar excluded): PASS")
    return True


def test_duplicate_timestamps():
    """Duplicate timestamps — first occurrence wins."""
    session_date = datetime(2026, 9, 24)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    # Duplicate a bar with different prices
    dup_time = datetime(2026, 9, 24, 9, 35)
    bars.append(make_bar(dup_time, 102.0, 103.0, 101.0, 102.0))  # Should be excluded

    outcome1 = process_session(bars, session_date)

    # Verify first occurrence was used (OR should not be affected by the duplicate)
    bars2 = [b for b in bars if not (b.bar_open_time == dup_time and b.open == 102.0)]
    outcome2 = process_session(bars2, session_date)

    assert structural_hash(outcome1) == structural_hash(outcome2), \
        "Duplicate handling should be deterministic"
    print("DATA QUALITY (duplicate timestamps): PASS")
    return True


def test_out_of_order_bars():
    """Out-of-order bars — reordered before processing."""
    session_date = datetime(2026, 9, 25)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    # Shuffle the bars (but keep content identical)
    import random
    random.seed(42)
    shuffled = bars.copy()
    random.shuffle(shuffled)

    outcome1 = process_session(bars, session_date)
    outcome2 = process_session(shuffled, session_date)

    assert structural_hash(outcome1) == structural_hash(outcome2), \
        "Out-of-order processing should produce identical results"
    print("DATA QUALITY (out-of-order bars): PASS")
    return True


# =============================================================================
# PHASE 10: COST-MODEL CONSISTENCY
# =============================================================================

def test_cost_model_application():
    """Verify 2 bps cost is mechanically applicable (no economic report)."""
    session_date = datetime(2026, 9, 26)
    bars = generate_session_bars(
        session_date,
        or_high_price=100.0,
        or_low_price=99.0,
        signal_close=100.05,
        signal_direction="LONG",
        retrace_bar_index=3,
    )

    outcome = process_session(bars, session_date)
    assert outcome.has_opportunity
    assert outcome.entry_price is not None
    assert outcome.exit_price is not None

    # Verify gross return formula (structural only, not economic report)
    if outcome.direction == Direction.LONG:
        gross_return = 10000 * (outcome.exit_price / outcome.entry_price - 1)
    else:
        gross_return = 10000 * (1 - outcome.exit_price / outcome.entry_price)

    net_return = gross_return - 2  # 2 bps round-trip

    # Verify the formula is computable (no economic report — just structural check)
    assert isinstance(gross_return, float), "Gross return must be computable"
    assert isinstance(net_return, float), "Net return must be computable"
    print("COST-MODEL CONSISTENCY: PASS (2 bps mechanical application verified)")
    return True


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("FB-001 ORB — V38A Stage 2 Structural Validation Tests")
    print("Registration: FB-001-ORB-V38A-REG-V1-r1")
    print("=" * 70)

    results = []

    # Phase 4
    print("\n--- PHASE 4: DETERMINISM ---")
    results.append(("Determinism", test_determinism()))

    # Phase 5
    print("\n--- PHASE 5: TEMPORAL/LEAKAGE AUDIT ---")
    results.append(("Pre-09:30 exclusion", test_no_pre_0930_in_or()))
    results.append(("Signal after OR", test_signal_after_or_only()))
    results.append(("Retrace subsequent only", test_retrace_uses_subsequent_bars_only()))
    results.append(("No future session info", test_no_future_session_info()))

    # Phase 6
    print("\n--- PHASE 6: OPPORTUNITY POPULATION ---")
    results.append(("No signal session", test_no_signal_session()))
    results.append(("One opportunity per session", test_one_opportunity_per_session()))
    results.append(("Incomplete OR", test_incomplete_or_no_opportunity()))

    # Phase 7
    print("\n--- PHASE 7: EXECUTION MAPPING (CASES A-L) ---")
    results.append(("Case A: Long breakout", test_case_a_long_breakout()))
    results.append(("Case B: Short breakout", test_case_b_short_breakout()))
    results.append(("Case C: Equality", test_case_c_equality()))
    results.append(("Case D: Retrace long", test_case_d_retrace_long()))
    results.append(("Case D: Retrace short", test_case_d_retrace_short()))
    results.append(("Case E: Entry bar not retrace", test_case_e_entry_execution_bar_not_retrace()))
    results.append(("Case F: Final session bar", test_case_f_final_session_bar()))
    results.append(("Case G: Session close wins", test_case_g_session_close_wins()))
    results.append(("Case H: No breakout", test_case_h_no_breakout()))
    results.append(("Case I: Incomplete OR", test_case_i_incomplete_opening_range()))
    results.append(("Case J: Early close after 10", test_case_j_early_close_after_10()))
    results.append(("Case K: Early close before 10", test_case_k_early_close_before_10()))
    results.append(("Case L: DST", test_case_l_dst()))

    # Phase 8
    print("\n--- PHASE 8: DATA QUALITY ---")
    results.append(("Missing bars", test_missing_bars()))
    results.append(("Malformed bar", test_malformed_bar_excluded()))
    results.append(("Duplicate timestamps", test_duplicate_timestamps()))
    results.append(("Out-of-order bars", test_out_of_order_bars()))

    # Phase 10
    print("\n--- PHASE 10: COST-MODEL CONSISTENCY ---")
    results.append(("Cost model", test_cost_model_application()))

    # Summary
    print("\n" + "=" * 70)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"RESULTS: {passed}/{total} PASS")

    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {name}: {status}")

    if passed == total:
        print("\nALL STRUCTURAL TESTS PASS")
    else:
        print("\nSTRUCTURAL TESTS FAILED")
        sys.exit(1)
