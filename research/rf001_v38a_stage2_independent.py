"""RF-001 V38A Stage 2 — Independent Reproducibility Implementation.

Governing registration: RF-001-V38A-REG-V1
Registration SHA: 3ea88d6772a45dd387ce940c6bbdd6678adedcf1bd6484b7c77d7322a15770ea

This is an INDEPENDENT implementation derived from the registration text alone.
It is NOT derived from the primary implementation.
It verifies that the registration text produces a deterministic, reproducible result.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# FROZEN CONSTANTS (from registration)
N_LOOKBACK = 30
M_CONFIRM = 15
SESSION_OPEN = (9, 30)
SESSION_CLOSE = (16, 0)


def _highest_high(bars: List[Dict], end_idx: int, lookback: int) -> float:
    """Highest high of lookback bars ending at end_idx (exclusive)."""
    return max(bars[i]["high"] for i in range(end_idx - lookback, end_idx))


def _lowest_low(bars: List[Dict], end_idx: int, lookback: int) -> float:
    """Lowest low of lookback bars ending at end_idx (exclusive)."""
    return min(bars[i]["low"] for i in range(end_idx - lookback, end_idx))


def is_breakout_up(bars: List[Dict], idx: int, lookback: int) -> bool:
    """Close at idx > highest high of lookback bars ending at idx."""
    if idx < lookback:
        return False
    return bars[idx]["close"] > _highest_high(bars, idx, lookback)


def is_breakout_down(bars: List[Dict], idx: int, lookback: int) -> bool:
    """Close at idx < lowest low of lookback bars ending at idx."""
    if idx < lookback:
        return False
    return bars[idx]["close"] < _lowest_low(bars, idx, lookback)


def run_independent(
    prim: List[Dict], prim_ts: List[datetime],
    conf: List[Dict], conf_ts: List[datetime]
) -> List[Dict]:
    """Independent RF-001 implementation. Returns list of opportunity dicts."""
    opps = []
    in_session = lambda ts: SESSION_OPEN <= (ts.hour, ts.minute) < SESSION_CLOSE

    # Timestamp to index maps for synchronization
    prim_map = {ts: i for i, ts in enumerate(prim_ts)}
    conf_map = {ts: i for i, ts in enumerate(conf_ts)}

    i = N_LOOKBACK  # earliest possible event bar
    while i < len(prim):
        bar = prim[i]
        ts = prim_ts[i]

        # Determine event direction
        event_dir = None
        if is_breakout_up(prim, i, N_LOOKBACK):
            event_dir = "BULLISH"
        elif is_breakout_down(prim, i, N_LOOKBACK):
            event_dir = "BEARISH"

        if event_dir is None:
            i += 1
            continue

        # Check: enough session time for M+2 bars after event
        entry_ts = ts + timedelta(minutes=M_CONFIRM + 2)
        close_ts = ts.replace(hour=SESSION_CLOSE[0], minute=SESSION_CLOSE[1],
                              second=0, microsecond=0)
        if entry_ts >= close_ts:
            i += 1
            continue

        # Find confirmation bar 1 (bar E+1) in confirmation market
        conf_bar1_ts = ts + timedelta(minutes=1)
        if conf_bar1_ts not in conf_map:
            i += 1
            continue
        conf_start = conf_map[conf_bar1_ts]

        # Scan M confirmation bars
        confirmed = False
        for k in range(M_CONFIRM):
            cidx = conf_start + k
            if cidx >= len(conf):
                break
            if cidx < N_LOOKBACK:
                continue
            if event_dir == "BULLISH" and is_breakout_up(conf, cidx, N_LOOKBACK):
                confirmed = True
                break
            elif event_dir == "BEARISH" and is_breakout_down(conf, cidx, N_LOOKBACK):
                confirmed = True
                break

        if confirmed:
            i += 1
            continue

        # Confirmation failure — check invalidation before entry
        entry_idx = prim_map.get(entry_ts)
        if entry_idx is None:
            i += 1
            continue

        # Invalidation: primary reverses before entry
        hh = _highest_high(prim, i, N_LOOKBACK)
        ll = _lowest_low(prim, i, N_LOOKBACK)
        invalidated = False
        for j in range(i + 1, entry_idx):
            if j >= len(prim):
                break
            c = prim[j]["close"]
            if event_dir == "BULLISH" and c <= hh:
                invalidated = True
                break
            elif event_dir == "BEARISH" and c >= ll:
                invalidated = True
                break

        if invalidated:
            i += 1
            continue

        # Decision
        direction = "SHORT" if event_dir == "BULLISH" else "LONG"
        opps.append({
            "event_idx": i,
            "event_ts": ts,
            "event_dir": event_dir,
            "decision_ts": ts + timedelta(minutes=M_CONFIRM + 1),
            "entry_ts": entry_ts,
            "direction": direction,
            "instrument": "US500",
        })
        i += 1

    return opps


# === Test data generators (independent from primary) ===

def gen_flat_primary(n=60):
    """Flat primary bars — no breakout."""
    bars, ts = [], []
    base = datetime(2026, 9, 7, 9, 30)
    for i in range(n):
        bars.append({"open": 100, "high": 101, "low": 99, "close": 100})
        ts.append(base + timedelta(minutes=i))
    return bars, ts


def gen_flat_confirm(n=60):
    """Flat confirmation bars — no breakout."""
    bars, ts = [], []
    base = datetime(2026, 9, 7, 9, 30)
    for i in range(n):
        bars.append({"open": 200, "high": 201, "low": 199, "close": 200})
        ts.append(base + timedelta(minutes=i))
    return bars, ts


def gen_bullish_breakout_at(idx=30):
    """Primary bars with bullish breakout at given index."""
    bars, ts = [], []
    base = datetime(2026, 9, 7, 9, 30)
    for i in range(60):
        if i < idx:
            bars.append({"open": 100, "high": 101, "low": 99, "close": 100})
        elif i == idx:
            bars.append({"open": 101.5, "high": 102, "low": 101, "close": 101.5})
        else:
            bars.append({"open": 101.5, "high": 102, "low": 101, "close": 101.5})
        ts.append(base + timedelta(minutes=i))
    return bars, ts


def gen_bearish_breakdown_at(idx=30):
    """Primary bars with bearish breakdown at given index."""
    bars, ts = [], []
    base = datetime(2026, 9, 7, 9, 30)
    for i in range(60):
        if i < idx:
            bars.append({"open": 100, "high": 101, "low": 99, "close": 100})
        elif i == idx:
            bars.append({"open": 98.5, "high": 99, "low": 98, "close": 98.5})
        else:
            bars.append({"open": 98.5, "high": 99, "low": 98, "close": 98.5})
        ts.append(base + timedelta(minutes=i))
    return bars, ts


def gen_confirm_at(confirm_idx):
    """Confirmation bars with breakout at given index."""
    bars, ts = [], []
    base = datetime(2026, 9, 7, 9, 30)
    for i in range(60):
        if i < confirm_idx:
            bars.append({"open": 200, "high": 201, "low": 199, "close": 200})
        elif i == confirm_idx:
            bars.append({"open": 201.5, "high": 202, "low": 201, "close": 201.5})
        else:
            bars.append({"open": 201.5, "high": 202, "low": 201, "close": 201.5})
        ts.append(base + timedelta(minutes=i))
    return bars, ts


def run_cross_check():
    """Cross-check independent implementation against known expected results."""
    results = {}

    # Test A: No event
    pb, pt = gen_flat_primary()
    cb, ct = gen_flat_confirm()
    opps = run_independent(pb, pt, cb, ct)
    results["A_no_event"] = len(opps) == 0

    # Test B: Event at bar 30, confirm at bar 31 (bar 1)
    pb, pt = gen_bullish_breakout_at(30)
    cb, ct = gen_confirm_at(31)
    opps = run_independent(pb, pt, cb, ct)
    results["B_confirm_bar1"] = len(opps) == 0

    # Test C: Event at bar 30, confirm at bar 45 (bar 15)
    pb, pt = gen_bullish_breakout_at(30)
    cb, ct = gen_confirm_at(45)
    opps = run_independent(pb, pt, cb, ct)
    results["C_confirm_bar15"] = len(opps) == 0

    # Test D: Event at bar 30, no confirm
    pb, pt = gen_bullish_breakout_at(30)
    cb, ct = gen_flat_confirm()
    opps = run_independent(pb, pt, cb, ct)
    results["D_bullish_failure"] = (
        len(opps) == 1 and
        opps[0]["event_dir"] == "BULLISH" and
        opps[0]["direction"] == "SHORT" and
        opps[0]["instrument"] == "US500"
    )

    # Test E: Bearish event, no confirm
    pb, pt = gen_bearish_breakdown_at(30)
    cb, ct = gen_flat_confirm()
    opps = run_independent(pb, pt, cb, ct)
    results["E_bearish_failure"] = (
        len(opps) == 1 and
        opps[0]["event_dir"] == "BEARISH" and
        opps[0]["direction"] == "LONG"
    )

    # Test H: Verify exact entry bar
    pb, pt = gen_bullish_breakout_at(30)
    cb, ct = gen_flat_confirm()
    opps = run_independent(pb, pt, cb, ct)
    expected_entry = datetime(2026, 9, 7, 10, 17)  # 09:30 + 47 min = 10:17
    results["H_entry_bar"] = (
        len(opps) == 1 and opps[0]["entry_ts"] == expected_entry
    )

    # Test K: Determinism
    results["K_determinism"] = True
    for _ in range(5):
        o = run_independent(pb, pt, cb, ct)
        if len(o) != len(opps) or any(
            o[j]["entry_ts"] != opps[j]["entry_ts"] for j in range(len(opps))
        ):
            results["K_determinism"] = False
            break

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("RF-001 INDEPENDENT REPRODUCIBILITY CHECK")
    print("=" * 60)

    results = run_cross_check()
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test}: {status}")

    print("-" * 60)
    print(f"  Total: {passed}/{total} passed")

    if passed == total:
        print("  INDEPENDENT REPRODUCIBILITY: PASS")
    else:
        print("  INDEPENDENT REPRODUCIBILITY: FAIL")
        print(f"  Failed: {[k for k, v in results.items() if not v]}")
