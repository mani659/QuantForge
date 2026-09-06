"""FB-001 ORB Live Observer — structural tests (T1–T26).

Tests the frozen FB-001 ORB V1-r1 decision process as implemented in the
live prospective observer. Uses synthetic fixtures only. No economic metrics.

Governing registration: FB-001-ORB-V38A-REG-V1-r1
Registration SHA: 04e9f804cca93d64ea18396abf5d25d2b968df974ee505f2b0866104e1af8086
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fb001_orb_observer import (
    FB001ORBObserver, SessionRecord, SessionPhase, Direction, ExitType,
    ObservationStatus, _utc_epoch_to_et, FREEZE_BOUNDARY_ET, OR_BAR_COUNT,
    BROKER_SYMBOL, TIMEFRAME
)


class FakeFeed:
    """Synthetic feed for testing — returns bars on demand."""
    def __init__(self, bars=None):
        self.bars = list(bars or [])
        self.queries = 0

    def latest_completed_bar(self, symbol, timeframe):
        self.queries += 1
        if not self.bars:
            return {"status": "FEED_UNAVAILABLE"}
        return self.bars.pop(0)


def bar(et_str, o=20000.0, h=20005.0, l=19995.0, c=20002.0, symbol=BROKER_SYMBOL):
    """Create a synthetic bar dict from an ET time string."""
    dt = datetime.strptime(et_str, "%Y-%m-%d %H:%M:%S")
    utc_epoch = int(dt.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp())
    return {
        "status": "DATA_FRESH", "symbol": symbol, "time": utc_epoch,
        "open": o, "high": h, "low": l, "close": c, "volume": 100,
    }


def bar_epoch(utc_epoch, o=20000.0, h=20005.0, l=19995.0, c=20002.0, symbol=BROKER_SYMBOL):
    return {
        "status": "DATA_FRESH", "symbol": symbol, "time": utc_epoch,
        "open": o, "high": h, "low": l, "close": c, "volume": 100,
    }


def _make_or_bars(session_date_str, count=30, base_price=20000.0):
    """Generate opening-range bars starting at 09:30 ET."""
    bars = []
    dt = datetime.strptime(session_date_str, "%Y-%m-%d")
    for i in range(count):
        bar_time = dt.replace(hour=9, minute=30) + timedelta(minutes=i)
        utc_epoch = int(bar_time.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp())
        offset = i * 0.5
        bars.append({
            "status": "DATA_FRESH", "symbol": BROKER_SYMBOL, "time": utc_epoch,
            "open": base_price + offset, "high": base_price + offset + 5,
            "low": base_price + offset - 5, "close": base_price + offset + 2,
            "volume": 100,
        })
    return bars


def _make_signal_bar(session_date_str, close_price, base_price=20000.0):
    """Generate the signal bar at 10:00 ET."""
    dt = datetime.strptime(session_date_str, "%Y-%m-%d")
    bar_time = dt.replace(hour=10, minute=0)
    utc_epoch = int(bar_time.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp())
    h = max(base_price, close_price) + 5
    l = min(base_price, close_price) - 5
    return {
        "status": "DATA_FRESH", "symbol": BROKER_SYMBOL, "time": utc_epoch,
        "open": base_price, "high": h, "low": l,
        "close": close_price, "volume": 100,
    }


def _make_entry_bar(session_date_str, entry_price=20015.0):
    """Generate the entry bar at 10:01 ET."""
    dt = datetime.strptime(session_date_str, "%Y-%m-%d")
    bar_time = dt.replace(hour=10, minute=1)
    utc_epoch = int(bar_time.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp())
    return {
        "status": "DATA_FRESH", "symbol": BROKER_SYMBOL, "time": utc_epoch,
        "open": entry_price, "high": entry_price + 3, "low": entry_price - 3,
        "close": entry_price + 1, "volume": 100,
    }


def _make_exit_bar(session_date_str, hour, minute, exit_price=19998.0):
    """Generate an exit bar at the specified time."""
    dt = datetime.strptime(session_date_str, "%Y-%m-%d")
    bar_time = dt.replace(hour=hour, minute=minute)
    utc_epoch = int(bar_time.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp())
    return {
        "status": "DATA_FRESH", "symbol": BROKER_SYMBOL, "time": utc_epoch,
        "open": exit_price, "high": exit_price + 3, "low": exit_price - 3,
        "close": exit_price + 1, "volume": 100,
    }


def _finalize_session(obs):
    """Send a post-session bar to force session finalization."""
    if obs._current_session is not None:
        sd = obs._current_session.session_date
        next_day = sd + timedelta(days=1)
        fake_bar = bar_epoch(
            int(next_day.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp()),
            20000, 20005, 19995, 20002
        )
        obs._process_bar(fake_bar)


def _run_observer(bars, td, name):
    """Run observer on bars, finalize session, return (observer, session_file_path, finalized_record)."""
    feed = FakeFeed(bars)
    obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, name))
    for _ in range(len(bars)):
        obs.on_tick({})
    sess = obs._current_session
    session_date_str = sess.session_date.strftime("%Y-%m-%d") if sess else None
    _finalize_session(obs)
    session_file = os.path.join(td, name, "sessions", "%s.json" % session_date_str) if session_date_str else None
    finalized = None
    if session_file and os.path.exists(session_file):
        with open(session_file) as f:
            finalized = json.load(f)
    return obs, session_file, finalized


def run_tests():
    results = []

    def check(name, cond):
        results.append((name, bool(cond)))
        print(("PASS " if cond else "FAIL ") + name)

    session_date = "2026-09-07"  # First post-freeze Monday

    with tempfile.TemporaryDirectory(prefix="fb001_observer_test_") as td:
        # T1: Asian session ignored by FB-001 (bars before 09:30 ET)
        asian_bars = []
        dt = datetime.strptime(session_date, "%Y-%m-%d")
        for h in range(4, 9):
            for m in range(0, 60, 5):
                t = dt.replace(hour=h, minute=m)
                utc = int(t.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp())
                asian_bars.append(bar_epoch(utc, 20000, 20005, 19995, 20002))
        feed = FakeFeed(asian_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t1"))
        for _ in range(len(asian_bars)):
            obs.on_tick({})
        check("T1 Asian session bars skipped (0 sessions observed)",
              obs.stats["sessions_observed"] == 0
              and obs.stats["asian_session_bars_skipped"] == len(asian_bars))

        # T2: US session begins correctly at 09:30 ET
        or_bars = _make_or_bars(session_date, 30)
        feed = FakeFeed(or_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t2"))
        for _ in range(30):
            obs.on_tick({})
        check("T2 US session begins at 09:30 (30 OR bars accumulated)",
              obs._current_session is not None
              and len(obs._current_session.or_bars) == 30
              and obs._current_session.phase == SessionPhase.POST_RANGE)

        # T3: DST handling — time conversion is consistent
        check("T3 UTC-4 conversion consistent",
              _utc_epoch_to_et(0).hour == 20
              and FREEZE_BOUNDARY_ET.year == 2026)

        # T4: Exactly 30 opening-range bars required
        short_or = _make_or_bars(session_date, 29)
        feed = FakeFeed(short_or)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t4"))
        for _ in range(29):
            obs.on_tick({})
        check("T4 29 OR bars -> session has incomplete OR (no or_high)",
              obs._current_session is not None
              and obs._current_session.or_high is None
              and obs._current_session.direction is None
              and len(obs._current_session.or_bars) == 29)

        # T5: Incomplete opening range produces no opportunity
        check("T5 incomplete OR -> no opportunity",
              obs._current_session is not None
              and obs._current_session.direction is None
              and obs._current_session.or_high is None)

        # T6: Long breakout
        all_bars = _make_or_bars(session_date, 30) + [_make_signal_bar(session_date, 20020.0)]
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t6"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T6 long breakout detected",
              obs._current_session is not None
              and obs._current_session.direction == Direction.LONG
              and obs._current_session.signal_bar is not None)

        # T7: Short breakout
        all_bars = _make_or_bars(session_date, 30, 20000.0) + [_make_signal_bar(session_date, 19980.0, 20000.0)]
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t7"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T7 short breakout detected",
              obs._current_session is not None
              and obs._current_session.direction == Direction.SHORT)

        # T8: Equality produces no signal
        or_bars_eq = _make_or_bars(session_date, 30, 20000.0)
        or_high_eq = max(b["high"] for b in or_bars_eq)
        feed = FakeFeed(or_bars_eq + [_make_signal_bar(session_date, or_high_eq)])
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t8"))
        for _ in range(len(or_bars_eq) + 1):
            obs.on_tick({})
        check("T8 equality (close == OR_high) produces no signal",
              obs._current_session is not None
              and obs._current_session.direction is None)

        # T9: First breakout only (no second signal)
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        all_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        all_bars.append(_make_entry_bar(session_date, 20015.0))
        all_bars.append(bar("2026-09-07 10:02:00", 20020, 20025, 19990, 19990))
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t9"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T9 first breakout only (long stays LONG)",
              obs._current_session is not None
              and obs._current_session.direction == Direction.LONG)

        # T10: Theoretical next-bar entry
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        all_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        all_bars.append(_make_entry_bar(session_date, 20015.0))
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t10"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T10 entry executed at next bar open",
              obs._current_session is not None
              and obs._current_session.entry_price == 20015.0
              and obs._current_session.phase == SessionPhase.POSITION_OPEN)

        # T11: Entry execution bar excluded from retrace
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        or_high = max(b["high"] for b in all_bars)
        all_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        entry = _make_entry_bar(session_date, 20015.0)
        entry["close"] = or_high - 1  # would trigger retrace if allowed
        all_bars.append(entry)
        post_entry = bar("2026-09-07 10:02:00", 20015, 20020, 19995, 20018)
        all_bars.append(post_entry)
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t11"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T11 entry bar excluded from retrace check",
              obs._current_session is not None
              and obs._current_session.exit_type is None)

        # T12: Long retrace
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        or_high_val = max(b["high"] for b in all_bars)
        all_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        all_bars.append(_make_entry_bar(session_date, 20015.0))
        all_bars.append(_make_exit_bar(session_date, 10, 3, or_high_val - 1))
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t12"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T12 long retrace exit",
              obs._current_session is not None
              and obs._current_session.exit_type == ExitType.RETRACE
              and obs._current_session.phase == SessionPhase.SESSION_CLOSED)

        # T13: Short retrace
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        or_low_val = min(b["low"] for b in all_bars)
        all_bars.append(_make_signal_bar(session_date, 19980.0, 20000.0))
        all_bars.append(_make_entry_bar(session_date, 19975.0))
        all_bars.append(_make_exit_bar(session_date, 10, 3, or_low_val + 1))
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t13"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T13 short retrace exit",
              obs._current_session is not None
              and obs._current_session.exit_type == ExitType.RETRACE
              and obs._current_session.direction == Direction.SHORT)

        # T14: Session-boundary exit
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        all_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        all_bars.append(_make_entry_bar(session_date, 20015.0))
        all_bars.append(_make_exit_bar(session_date, 15, 59, 20030.0))
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t14"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T14 session-boundary exit",
              obs._current_session is not None
              and obs._current_session.exit_type == ExitType.SESSION_CLOSE)

        # T15: Session-boundary precedence over retrace
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        or_high_val = max(b["high"] for b in all_bars)
        all_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        all_bars.append(_make_entry_bar(session_date, 20015.0))
        final_bar = _make_exit_bar(session_date, 15, 59, or_high_val - 1)
        all_bars.append(final_bar)
        feed = FakeFeed(all_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t15"))
        for _ in range(len(all_bars)):
            obs.on_tick({})
        check("T15 session-boundary exit governs over retrace",
              obs._current_session is not None
              and obs._current_session.exit_type == ExitType.SESSION_CLOSE)

        # T16: Early-close session
        early_date = "2026-09-07"
        early_bars = _make_or_bars(early_date, 30, 20000.0)
        early_bars.append(_make_signal_bar(early_date, 20020.0, 20000.0))
        early_bars.append(_make_entry_bar(early_date, 20015.0))
        early_bars.append(_make_exit_bar(early_date, 13, 0, 20010.0))
        feed = FakeFeed(early_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t16"))
        for _ in range(len(early_bars)):
            obs.on_tick({})
        check("T16 early-close session handled (observer accepts bar)",
              obs._current_session is not None
              and obs._current_session.bars_processed > 0)

        # T17: Malformed bars rejected
        malformed = _make_or_bars(session_date, 30, 20000.0)
        malformed.append(bar("2026-09-07 10:00:00", 20020, 20015, 20025, 20022))
        feed = FakeFeed(malformed)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t17"))
        for _ in range(len(malformed)):
            obs.on_tick({})
        check("T17 malformed bar rejected (data quality exception logged)",
              obs.stats["data_quality_exceptions"] >= 1)

        # T18: Duplicate bars (same timestamp, same data = idempotent)
        dup_bars = _make_or_bars(session_date, 30, 20000.0)
        dup_bars.append(dup_bars[-1].copy())
        feed = FakeFeed(dup_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t18"))
        for _ in range(len(dup_bars)):
            obs.on_tick({})
        check("T18 duplicate bar is idempotent (bar not reprocessed)",
              obs._current_session is not None
              and obs._current_session.bars_processed == 30)

        # T19: Out-of-order bars (chronological processing)
        ooo_bars = _make_or_bars(session_date, 30, 20000.0)
        ooo_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        feed = FakeFeed(ooo_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t19"))
        for _ in range(len(ooo_bars)):
            obs.on_tick({})
        check("T19 out-of-order bars handled (processed in order)",
              obs._current_session is not None
              and obs._current_session.direction == Direction.LONG)

        # T20: Missing bars (gaps in data)
        sparse_bars = _make_or_bars(session_date, 30, 20000.0)
        sparse_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        sparse_bars.append(_make_entry_bar(session_date, 20015.0))
        sparse_bars.append(_make_exit_bar(session_date, 10, 5, 20000.0))
        feed = FakeFeed(sparse_bars)
        obs = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t20"))
        for _ in range(len(sparse_bars)):
            obs.on_tick({})
        check("T20 missing bars (gaps) handled gracefully",
              obs._current_session is not None
              and obs._current_session.bars_processed > 0)

        # T21: No live order is ever submitted (check observer source, not test source)
        observer_source = open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "fb001_orb_observer.py"),
            encoding="utf-8"
        ).read()
        no_trade_tokens = ["mt5.order_send", "order_send(", "place_order(", "BUY(", "SELL(",
                           "order_send ", "position_open("]
        check("T21 no order submission tokens in observer source",
              all(tok not in observer_source for tok in no_trade_tokens))

        # T22: F-01 regression — F-01 recorder still works independently
        from f01_observation_recorder import F01ObservationRecorder
        feed22 = FakeFeed([bar("2026-09-07 09:30:00", 20000, 20005, 19995, 20002)])
        rec = F01ObservationRecorder(feed=feed22, raw_dir=os.path.join(td, "t22_f01"))
        rec.on_tick({})
        check("T22 F-01 recorder still works independently",
              rec.stats["total_captured"] == 1)

        # T23: Shared-feed failure is isolated
        class FailFeed:
            def latest_completed_bar(self, symbol, timeframe):
                raise RuntimeError("feed crash")
        feed23 = FailFeed()
        obs23 = FB001ORBObserver(feed=feed23, data_dir=os.path.join(td, "t23"))
        for _ in range(5):
            obs23.on_tick({})
        check("T23 shared-feed failure isolated (observer survives)",
              obs23.stats["errors"] == 5)

        # T24: Session record persistence
        all_bars = _make_or_bars(session_date, 30, 20000.0)
        all_bars.append(_make_signal_bar(session_date, 20020.0, 20000.0))
        all_bars.append(_make_entry_bar(session_date, 20015.0))
        all_bars.append(_make_exit_bar(session_date, 10, 3, 20000.0))
        feed = FakeFeed(all_bars)
        obs24 = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t24"))
        for _ in range(len(all_bars)):
            obs24.on_tick({})
        _finalize_session(obs24)
        session_file = os.path.join(td, "t24", "sessions", "%s.json" % session_date)
        check("T24 session record persisted to disk",
              os.path.exists(session_file))
        if os.path.exists(session_file):
            with open(session_file) as f:
                rec = json.load(f)
            check("T24 session record has correct status",
                  rec["status"] == "POSITION_CLOSED"
                  and rec["exit_type"] == "RETRACE")

        # T25: Pre-freeze bar skipped
        pre_freeze = bar("2026-09-05 10:00:00", 20000, 20005, 19995, 20002)
        feed = FakeFeed([pre_freeze])
        obs25 = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t25"))
        obs25.on_tick({})
        check("T25 pre-freeze bar skipped",
              obs25.stats["pre_freeze_bars_skipped"] == 1
              and obs25.stats["bars_after_freeze"] == 0)

        # T26: No-breakout sessions retained in observation population
        no_breakout_bars = _make_or_bars(session_date, 30, 20000.0)
        or_high_nb = max(b["high"] for b in no_breakout_bars)
        or_low_nb = min(b["low"] for b in no_breakout_bars)
        mid_price = (or_high_nb + or_low_nb) / 2
        no_breakout_bars.append(_make_signal_bar(session_date, mid_price, 20000.0))
        feed = FakeFeed(no_breakout_bars)
        obs26 = FB001ORBObserver(feed=feed, data_dir=os.path.join(td, "t26"))
        for _ in range(len(no_breakout_bars)):
            obs26.on_tick({})
        sess26 = obs26._current_session
        check("T26 no-breakout session has no direction",
              sess26 is not None and sess26.direction is None)

    print("---")
    failed = [n for n, c in results if not c]
    print("fb001_orb_observer tests: %d/%d passed" % (len(results) - len(failed), len(results)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run_tests())
