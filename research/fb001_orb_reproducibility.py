"""
FB-001 ORB — Independent Reproducibility Comparison

Compares the primary implementation (fb001_orb_structural.py) with the
independent implementation (fb001_orb_independent.py) to verify that
two independently coded implementations produce identical structural results.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, time, timedelta
from fb001_orb_structural import (
    process_session as primary_process,
    structural_hash as primary_hash,
    Direction, ExitType,
)
from fb001_orb_independent import (
    process_fb001 as independent_process,
    structural_hash_ind as independent_hash,
)


def make_independent_bars(session_date, or_high, or_low, signal_close, signal_dir,
                          retrace_idx=None, num_or=30, early_close=None):
    """Generate bars in the independent implementation's format."""
    bars = []
    base = (or_high + or_low) / 2

    # OR bars
    for i in range(num_or):
        t = datetime.combine(session_date.date(), time(9, 30)) + timedelta(minutes=i)
        if i == 0:
            o, h, l, c = or_low, or_high, or_low, base
        elif i == num_or - 1:
            o, h, l, c = base, or_high, or_low, base
        else:
            frac = i / (num_or - 1)
            o = or_low + frac * (or_high - or_low) * 0.3
            h = or_high - (num_or - i) * 0.01
            l = or_low + i * 0.01
            c = base + (frac - 0.5) * 0.2
        bars.append({"open_time": t, "o": o, "h": h, "l": l, "c": c})

    # Signal bar
    sig_t = datetime.combine(session_date.date(), time(10, 0))
    if signal_close is not None and signal_dir:
        if signal_dir == "LONG":
            s_o, s_h, s_l, s_c = or_high - 0.05, signal_close + 0.02, or_high - 0.1, signal_close
        else:
            s_o, s_h, s_l, s_c = or_low + 0.05, or_low + 0.1, signal_close - 0.02, signal_close
    else:
        s_o, s_h, s_l, s_c = base, base + 0.1, base - 0.1, base
    bars.append({"open_time": sig_t, "o": s_o, "h": s_h, "l": s_l, "c": s_c})

    # Entry bar
    entry_t = datetime.combine(session_date.date(), time(10, 1))
    entry_o = base + (0.1 if signal_dir == "LONG" else -0.1) if signal_dir else base
    bars.append({"open_time": entry_t, "o": entry_o, "h": entry_o + 0.05,
                 "l": entry_o - 0.05, "c": entry_o + 0.02})

    if signal_dir and retrace_idx is not None:
        sess_end = early_close or time(16, 0)
        final_t = datetime.combine(session_date.date(), sess_end) - timedelta(minutes=1)
        post_start = datetime.combine(session_date.date(), time(10, 2))
        max_bars = int((final_t - post_start).total_seconds() / 60) + 1

        for i in range(min(max_bars, 20)):
            bt = post_start + timedelta(minutes=i)
            if bt >= final_t:
                break
            if i == retrace_idx:
                if signal_dir == "LONG":
                    r_o, r_c = or_high + 0.05, or_high - 0.01
                    r_h, r_l = r_o + 0.02, r_c - 0.02
                else:
                    r_o, r_c = or_low - 0.05, or_low + 0.01
                    r_h, r_l = r_c + 0.02, r_o - 0.02
            else:
                if signal_dir == "LONG":
                    r_o = or_high + 0.1 + i * 0.005
                    r_c = r_o + 0.003
                    r_h, r_l = r_c + 0.01, r_o - 0.01
                else:
                    r_o = or_low - 0.1 - i * 0.005
                    r_c = r_o - 0.003
                    r_h, r_l = r_o + 0.01, r_c - 0.01
            bars.append({"open_time": bt, "o": r_o, "h": r_h, "l": r_l, "c": r_c})

        if final_t not in [b["open_time"] for b in bars]:
            if signal_dir == "LONG":
                f_o, f_c = or_high + 0.2, or_high + 0.3
            else:
                f_o, f_c = or_low - 0.2, or_low - 0.3
            bars.append({"open_time": final_t, "o": f_o, "h": f_o + 0.02,
                         "l": f_o - 0.02, "c": f_c})
    elif signal_dir:
        sess_end = early_close or time(16, 0)
        final_t = datetime.combine(session_date.date(), sess_end) - timedelta(minutes=1)
        post_start = datetime.combine(session_date.date(), time(10, 2))
        for i in range(5):
            bt = post_start + timedelta(minutes=i)
            if bt >= final_t:
                break
            if signal_dir == "LONG":
                r_o = or_high + 0.1 + i * 0.005
                r_c = r_o + 0.003
            else:
                r_o = or_low - 0.1 - i * 0.005
                r_c = r_o - 0.003
            bars.append({"open_time": bt, "o": r_o, "h": r_c + 0.01,
                         "l": r_o - 0.01, "c": r_c})
        if final_t not in [b["open_time"] for b in bars]:
            if signal_dir == "LONG":
                f_o, f_c = or_high + 0.2, or_high + 0.3
            else:
                f_o, f_c = or_low - 0.2, or_low - 0.3
            bars.append({"open_time": final_t, "o": f_o, "h": f_o + 0.02,
                         "l": f_o - 0.02, "c": f_c})

    return bars


def make_primary_bars(session_date, or_high, or_low, signal_close, signal_dir,
                      retrace_idx=None, num_or=30, early_close=None):
    """Generate bars for the primary implementation (using make_bar)."""
    from fb001_orb_structural import make_bar
    bars = []
    base = (or_high + or_low) / 2

    for i in range(num_or):
        t = datetime.combine(session_date.date(), time(9, 30)) + timedelta(minutes=i)
        if i == 0:
            o, h, l, c = or_low, or_high, or_low, base
        elif i == num_or - 1:
            o, h, l, c = base, or_high, or_low, base
        else:
            frac = i / (num_or - 1)
            o = or_low + frac * (or_high - or_low) * 0.3
            h = or_high - (num_or - i) * 0.01
            l = or_low + i * 0.01
            c = base + (frac - 0.5) * 0.2
        bars.append(make_bar(t, o, h, l, c))

    sig_t = datetime.combine(session_date.date(), time(10, 0))
    if signal_close is not None and signal_dir:
        if signal_dir == "LONG":
            s_o, s_h, s_l, s_c = or_high - 0.05, signal_close + 0.02, or_high - 0.1, signal_close
        else:
            s_o, s_h, s_l, s_c = or_low + 0.05, or_low + 0.1, signal_close - 0.02, signal_close
    else:
        s_o, s_h, s_l, s_c = base, base + 0.1, base - 0.1, base
    bars.append(make_bar(sig_t, s_o, s_h, s_l, s_c))

    entry_t = datetime.combine(session_date.date(), time(10, 1))
    entry_o = base + (0.1 if signal_dir == "LONG" else -0.1) if signal_dir else base
    bars.append(make_bar(entry_t, entry_o, entry_o + 0.05, entry_o - 0.05, entry_o + 0.02))

    if signal_dir and retrace_idx is not None:
        sess_end = early_close or time(16, 0)
        final_t = datetime.combine(session_date.date(), sess_end) - timedelta(minutes=1)
        post_start = datetime.combine(session_date.date(), time(10, 2))
        max_bars = int((final_t - post_start).total_seconds() / 60) + 1
        for i in range(min(max_bars, 20)):
            bt = post_start + timedelta(minutes=i)
            if bt >= final_t:
                break
            if i == retrace_idx:
                if signal_dir == "LONG":
                    r_o, r_c = or_high + 0.05, or_high - 0.01
                    r_h, r_l = r_o + 0.02, r_c - 0.02
                else:
                    r_o, r_c = or_low - 0.05, or_low + 0.01
                    r_h, r_l = r_c + 0.02, r_o - 0.02
            else:
                if signal_dir == "LONG":
                    r_o = or_high + 0.1 + i * 0.005
                    r_c = r_o + 0.003
                    r_h, r_l = r_c + 0.01, r_o - 0.01
                else:
                    r_o = or_low - 0.1 - i * 0.005
                    r_c = r_o - 0.003
                    r_h, r_l = r_o + 0.01, r_c - 0.01
            bars.append(make_bar(bt, r_o, r_h, r_l, r_c))
        if final_t not in [b.bar_open_time for b in bars]:
            if signal_dir == "LONG":
                f_o, f_c = or_high + 0.2, or_high + 0.3
            else:
                f_o, f_c = or_low - 0.2, or_low - 0.3
            bars.append(make_bar(final_t, f_o, f_o + 0.02, f_o - 0.02, f_c))
    elif signal_dir:
        sess_end = early_close or time(16, 0)
        final_t = datetime.combine(session_date.date(), sess_end) - timedelta(minutes=1)
        post_start = datetime.combine(session_date.date(), time(10, 2))
        for i in range(5):
            bt = post_start + timedelta(minutes=i)
            if bt >= final_t:
                break
            if signal_dir == "LONG":
                r_o = or_high + 0.1 + i * 0.005
                r_c = r_o + 0.003
            else:
                r_o = or_low - 0.1 - i * 0.005
                r_c = r_o - 0.003
            bars.append(make_bar(bt, r_o, r_c + 0.01, r_o - 0.01, r_c))
        if final_t not in [b.bar_open_time for b in bars]:
            if signal_dir == "LONG":
                f_o, f_c = or_high + 0.2, or_high + 0.3
            else:
                f_o, f_c = or_low - 0.2, or_low - 0.3
            bars.append(make_bar(final_t, f_o, f_o + 0.02, f_o - 0.02, f_c))

    return bars


def outcome_to_dict(outcome):
    """Convert StructuralOutcome dataclass to dict for comparison."""
    if hasattr(outcome, '__dict__'):
        return {k: v for k, v in outcome.__dict__.items()}
    return outcome


def compare(outcome1, outcome2, label):
    """Compare two structural outcomes."""
    d1 = outcome_to_dict(outcome1)
    d2 = outcome_to_dict(outcome2)

    # Map field names between implementations
    # Primary: signal_bar_open_time, entry_bar_open_time, exit_bar_open_time
    # Independent: signal_bar, entry_bar, exit_bar
    field_map = [
        ("has_opportunity", "has_opportunity"),
        ("direction", "direction"),
        ("signal_bar_open_time", "signal_bar"),
        ("entry_bar_open_time", "entry_bar"),
        ("exit_type", "exit_type"),
        ("exit_bar_open_time", "exit_bar"),
    ]

    for f1, f2 in field_map:
        v1 = d1.get(f1)
        v2 = d2.get(f2)
        # Normalize enum/None values
        if hasattr(v1, 'value'):
            v1 = v1.value
        if hasattr(v2, 'value'):
            v2 = v2.value
        if v1 != v2:
            print(f"  MISMATCH {label} field=({f1} vs {f2}): primary={v1} independent={v2}")
            return False

    for f in ["entry_price", "exit_price", "or_high", "or_low"]:
        v1 = d1.get(f)
        v2 = d2.get(f)
        if v1 is not None and v2 is not None:
            if abs(v1 - v2) > 1e-10:
                print(f"  MISMATCH {label} field={f}: primary={v1} independent={v2}")
                return False
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("FB-001 ORB — Independent Reproducibility Comparison")
    print("=" * 70)

    test_cases = [
        ("Long breakout, session close", datetime(2026, 9, 10), 100.0, 99.0, 100.05, "LONG", None),
        ("Short breakout, session close", datetime(2026, 9, 11), 100.0, 99.0, 98.95, "SHORT", None),
        ("Long breakout, retrace", datetime(2026, 9, 12), 100.0, 99.0, 100.05, "LONG", 3),
        ("Short breakout, retrace", datetime(2026, 9, 13), 100.0, 99.0, 98.95, "SHORT", 2),
        ("No breakout", datetime(2026, 9, 14), 100.0, 99.0, None, None, None),
        ("Incomplete OR", datetime(2026, 9, 15), 100.0, 99.0, 100.05, "LONG", 3),
    ]

    all_pass = True
    for label, sess_date, or_h, or_l, sig_c, sig_d, ret_idx in test_cases:
        num_or = 25 if "Incomplete" in label else 30
        primary_bars = make_primary_bars(sess_date, or_h, or_l, sig_c, sig_d, ret_idx, num_or)
        independent_bars = make_independent_bars(sess_date, or_h, or_l, sig_c, sig_d, ret_idx, num_or)

        p_outcome = primary_process(primary_bars, sess_date)
        i_outcome = independent_process(independent_bars, sess_date)

        p_hash = primary_hash(p_outcome)
        i_hash = independent_hash(i_outcome)

        # Compare using mapped field names
        p_map = {"signal_bar_open_time": "signal_bar", "entry_bar_open_time": "entry_bar",
                 "exit_bar_open_time": "exit_bar"}
        p_norm = {}
        for k, v in outcome_to_dict(p_outcome).items():
            nk = p_map.get(k, k)
            if hasattr(v, 'value'):
                v = v.value
            p_norm[nk] = v

        match = True
        for f in ["has_opportunity", "direction", "signal_bar", "entry_bar",
                  "exit_type", "exit_bar"]:
            pv = p_norm.get(f)
            iv = i_outcome.get(f)
            if pv != iv:
                print(f"  MISMATCH {label} field={f}: primary={pv} independent={iv}")
                match = False
                break
        if match:
            for f in ["entry_price", "exit_price", "or_high", "or_low"]:
                pv = p_norm.get(f)
                iv = i_outcome.get(f)
                if pv is not None and iv is not None and abs(pv - iv) > 1e-10:
                    print(f"  MISMATCH {label} field={f}: primary={pv} independent={iv}")
                    match = False
                    break
        status = "PASS" if match else "FAIL"
        print(f"  {label}: {status} (primary={p_hash}, independent={i_hash})")
        if not match:
            all_pass = False

    print()
    if all_pass:
        print("REPRODUCIBILITY: PASS — Both implementations produce identical structural results")
    else:
        print("REPRODUCIBILITY: FAIL — Implementations disagree")
        sys.exit(1)
