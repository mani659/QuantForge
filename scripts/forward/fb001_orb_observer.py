"""FB-001 ORB Live Observation Observer — prospective accrual sidecar (v1.0.0).

Governing registration: FB-001-ORB-V38A-REG-V1-r1
Registration SHA: 04e9f804cca93d64ea18396abf5d25d2b968df974ee505f2b0866104e1af8086

PURPOSE (only):
  Accrue post-freeze prospective ORB observations from live USTECm M1 data.
  Attaches to the Unified Runner supervisor's shared MT5MarketFeed — the same
  feed used by F-01 and the three paper modules. No second MT5 connection.

THIS OBSERVER IS NOT A TRADING MODULE:
  - it never places, modifies, or manages orders or positions;
  - it never computes returns, P&L, or any economic performance quantity;
  - it never launches Stage 3 economic validation;
  - it never alters the FB-001 registration, session logic, cost model, or
    validation scope;
  - it never modifies F-01 behavior, output, or persistence.

ARCHITECTURE (attachment, not duplication):
  Shared MT5MarketFeed -> Unified Runner -> this observer (on_tick sidecar).
  Session records are persisted to a dedicated governed archive under
  data/fb001_orb/ (gitignored data area). F-01 data remains untouched.

FREEZE BOUNDARY:
  Registration frozen: 2026-09-06 08:00 ET.
  Only sessions whose session_date >= 2026-09-07 are eligible for governed
  economic observation accrual. Pre-freeze sessions produce no governed records.

SEMAPHORE:
  SESSION_OBSERVED      — session exists, no opportunity
  OPPORTUNITY_LONG      — long signal fired
  OPPORTUNITY_SHORT     — short signal fired
  POSITION_OPEN         — theoretical position open
  POSITION_CLOSED       — theoretical position closed
  DATA_INCOMPLETE       — required bars unavailable
  DATA_QUALITY_EXCEPTION — malformed/duplicate bars encountered
"""

import json
import os
import time
from datetime import datetime, timezone, timedelta, time as dt_time
from enum import Enum
from typing import Optional, Dict, Any, List

VERSION = "1.0.0"
LOGICAL_SYMBOL = "USATECHIDXUSD"
BROKER_SYMBOL = "USTECm"
TIMEFRAME = "M1"
FREEZE_BOUNDARY_ET = datetime(2026, 9, 6, 8, 0)  # 2026-09-06 08:00 ET
SESSION_START_HOUR = 9
SESSION_START_MINUTE = 30
OR_END_HOUR = 10
OR_END_MINUTE = 0
SESSION_END_HOUR = 16
SESSION_END_MINUTE = 0
OR_BAR_COUNT = 30


def _project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _default_data_dir():
    return os.path.join(_project_root(), "data", "fb001_orb")


def _utc_epoch_to_et(utc_epoch: float) -> datetime:
    """Convert UTC epoch to America/New_York datetime (naive, UTC-4 offset).

    Uses fixed UTC-4 offset (EDT) consistent with the existing codebase
    convention (see f01_observation_recorder.py). Market data from MT5
    represents Eastern Time epochs. Returns naive datetime for comparison
    with naive datetimes from datetime.combine().
    """
    return datetime.fromtimestamp(utc_epoch, tz=timezone(timedelta(hours=-4))).replace(tzinfo=None)


def _et_to_utc_epoch(et_dt: datetime) -> float:
    """Convert naive Eastern Time datetime to UTC epoch."""
    return et_dt.replace(tzinfo=timezone(timedelta(hours=-4))).timestamp()


class SessionPhase(Enum):
    PRE_SESSION = "PRE_SESSION"
    OPENING_RANGE = "OPENING_RANGE"
    POST_RANGE = "POST_RANGE"
    POSITION_OPEN = "POSITION_OPEN"
    SESSION_CLOSED = "SESSION_CLOSED"
    NO_SESSION = "NO_SESSION"


class Direction(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class ExitType(Enum):
    RETRACE = "RETRACE"
    SESSION_CLOSE = "SESSION_CLOSE"


class ObservationStatus(Enum):
    SESSION_OBSERVED = "SESSION_OBSERVED"
    OPPORTUNITY_LONG = "OPPORTUNITY_LONG"
    OPPORTUNITY_SHORT = "OPPORTUNITY_SHORT"
    POSITION_OPEN = "POSITION_OPEN"
    POSITION_CLOSED = "POSITION_CLOSED"
    DATA_INCOMPLETE = "DATA_INCOMPLETE"
    DATA_QUALITY_EXCEPTION = "DATA_QUALITY_EXCEPTION"


class SessionRecord:
    """Governed record for one eligible US trading session."""

    def __init__(self, session_date: datetime):
        self.session_date = session_date
        self.session_start = session_date.replace(
            hour=SESSION_START_HOUR, minute=SESSION_START_MINUTE, second=0, microsecond=0
        )
        self.session_end = session_date.replace(
            hour=SESSION_END_HOUR, minute=SESSION_END_MINUTE, second=0, microsecond=0
        )
        self.or_end = session_date.replace(
            hour=OR_END_HOUR, minute=OR_END_MINUTE, second=0, microsecond=0
        )

        self.phase = SessionPhase.PRE_SESSION
        self.or_bars: List[Dict] = []
        self.or_high: Optional[float] = None
        self.or_low: Optional[float] = None
        self.signal_bar: Optional[Dict] = None
        self.direction: Optional[Direction] = None
        self.entry_bar: Optional[Dict] = None
        self.entry_price: Optional[float] = None
        self.exit_bar: Optional[Dict] = None
        self.exit_price: Optional[float] = None
        self.exit_type: Optional[ExitType] = None
        self.status = ObservationStatus.SESSION_OBSERVED
        self.data_quality_events: List[str] = []
        self.bars_processed = 0

    def to_dict(self) -> dict:
        return {
            "session_date": self.session_date.strftime("%Y-%m-%d"),
            "session_start_et": self.session_start.strftime("%Y-%m-%d %H:%M:%S"),
            "session_end_et": self.session_end.strftime("%Y-%m-%d %H:%M:%S"),
            "phase": self.phase.value,
            "or_high": self.or_high,
            "or_low": self.or_low,
            "or_bar_count": len(self.or_bars),
            "signal_direction": self.direction.value if self.direction else None,
            "signal_bar_time": self.signal_bar["time_str"] if self.signal_bar else None,
            "entry_bar_time": self.entry_bar["time_str"] if self.entry_bar else None,
            "entry_price": self.entry_price,
            "exit_bar_time": self.exit_bar["time_str"] if self.exit_bar else None,
            "exit_price": self.exit_price,
            "exit_type": self.exit_type.value if self.exit_type else None,
            "status": self.status.value,
            "bars_processed": self.bars_processed,
            "data_quality_events": self.data_quality_events,
        }


class FB001ORBObserver:
    """Live prospective ORB observation accrual — passive, non-trading.

    Exception-safe by contract: on_tick() never raises, so an observer fault
    cannot alter the behavior of the trading modules sharing the supervisor loop.
    """

    def __init__(self, feed=None, data_dir=None):
        self.feed = feed
        self.data_dir = data_dir if data_dir is not None else _default_data_dir()
        self.sessions_dir = os.path.join(self.data_dir, "sessions")
        self.status_file = os.path.join(self.data_dir, "observer_status.json")
        self.events_log = os.path.join(self.data_dir, "observer_events.jsonl")

        self._current_session: Optional[SessionRecord] = None
        self._last_bar_time: Optional[int] = None
        self._active_session_date: Optional[str] = None

        self.stats = {
            "total_bars_received": 0,
            "bars_after_freeze": 0,
            "sessions_observed": 0,
            "opportunities_detected": 0,
            "positions_opened": 0,
            "positions_closed": 0,
            "data_incomplete": 0,
            "data_quality_exceptions": 0,
            "feed_unavailable": 0,
            "errors": 0,
            "pre_freeze_bars_skipped": 0,
            "asian_session_bars_skipped": 0,
        }
        self.last_error = None
        self._load_status()

    # ------------------------------------------------------------------ state

    def _load_status(self):
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.stats.update(data.get("stats", {}))
                self.last_error = data.get("last_error")
                self._last_bar_time = data.get("last_bar_time")
            except Exception:
                pass

    def _save_status(self):
        os.makedirs(self.data_dir, exist_ok=True)
        data = {
            "observer_version": VERSION,
            "logical_symbol": LOGICAL_SYMBOL,
            "broker_symbol": BROKER_SYMBOL,
            "timeframe": TIMEFRAME,
            "freeze_boundary_et": FREEZE_BOUNDARY_ET.strftime("%Y-%m-%d %H:%M:%S"),
            "stats": self.stats,
            "last_bar_time": self._last_bar_time,
            "last_error": self.last_error,
            "last_status_write_utc": datetime.now(timezone.utc).isoformat(),
        }
        tmp = self.status_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, self.status_file)

    def _log_event(self, event: dict):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.events_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")

    def _persist_session(self, record: SessionRecord):
        os.makedirs(self.sessions_dir, exist_ok=True)
        filename = f"{record.session_date.strftime('%Y-%m-%d')}.json"
        filepath = os.path.join(self.sessions_dir, filename)
        tmp = filepath + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, indent=2)
        os.replace(tmp, filepath)

    # --------------------------------------------------------- bar processing

    def _validate_bar(self, bar: dict) -> tuple:
        """Structural validation. Returns (ok, reason)."""
        if bar.get("status") != "DATA_FRESH":
            return False, "feed_status:" + str(bar.get("status"))
        if bar.get("symbol") != BROKER_SYMBOL:
            return False, "symbol_mismatch:" + str(bar.get("symbol"))
        try:
            t = int(bar["time"])
            o = float(bar["open"])
            h = float(bar["high"])
            lo = float(bar["low"])
            c = float(bar["close"])
        except Exception:
            return False, "unparseable_bar"
        if t <= 0:
            return False, "invalid_time"
        if t % 60 != 0:
            return False, "not_m1_aligned"
        if not (o > 0 and h > 0 and lo > 0 and c > 0):
            return False, "non_positive_price"
        if h < max(o, c) or lo > min(o, c) or h < lo:
            return False, "ohlc_violation"
        return True, None

    def _bar_to_dict(self, bar: dict) -> dict:
        """Convert MT5 bar to canonical dict with ET timestamp string."""
        t = int(bar["time"])
        et_dt = _utc_epoch_to_et(t)
        return {
            "time": t,
            "time_str": et_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "open": float(bar["open"]),
            "high": float(bar["high"]),
            "low": float(bar["low"]),
            "close": float(bar["close"]),
            "volume": int(bar.get("volume", 0) or 0),
        }

    def _is_us_session(self, et_dt: datetime) -> bool:
        """Check if datetime falls within US session [09:30, 16:00) ET."""
        session_start = et_dt.replace(
            hour=SESSION_START_HOUR, minute=SESSION_START_MINUTE, second=0, microsecond=0
        )
        session_end = et_dt.replace(
            hour=SESSION_END_HOUR, minute=SESSION_END_MINUTE, second=0, microsecond=0
        )
        return session_start <= et_dt < session_end

    def _is_or_window(self, et_dt: datetime) -> bool:
        """Check if datetime falls within OR window [09:30, 10:00) ET."""
        or_start = et_dt.replace(
            hour=SESSION_START_HOUR, minute=SESSION_START_MINUTE, second=0, microsecond=0
        )
        or_end = et_dt.replace(
            hour=OR_END_HOUR, minute=OR_END_MINUTE, second=0, microsecond=0
        )
        return or_start <= et_dt < or_end

    def _get_session_date(self, et_dt: datetime) -> datetime:
        """Get the session date (midnight) for a bar's ET datetime."""
        return et_dt.replace(hour=0, minute=0, second=0, microsecond=0)

    def _finalize_session(self, record: SessionRecord):
        """Finalize a session record and persist it."""
        if record.phase in (SessionPhase.POSITION_OPEN, SessionPhase.POST_RANGE):
            record.status = ObservationStatus.POSITION_OPEN
        elif record.status == ObservationStatus.SESSION_OBSERVED:
            if record.direction is not None:
                if record.direction == Direction.LONG:
                    record.status = ObservationStatus.OPPORTUNITY_LONG
                else:
                    record.status = ObservationStatus.OPPORTUNITY_SHORT
                self.stats["opportunities_detected"] += 1
            else:
                record.status = ObservationStatus.SESSION_OBSERVED
        self.stats["sessions_observed"] += 1
        self._persist_session(record)
        self._log_event({
            "event": "SESSION_FINALIZED",
            "session_date": record.session_date.strftime("%Y-%m-%d"),
            "status": record.status.value,
            "direction": record.direction.value if record.direction else None,
            "or_high": record.or_high,
            "or_low": record.or_low,
            "entry_price": record.entry_price,
            "exit_price": record.exit_price,
            "exit_type": record.exit_type.value if record.exit_type else None,
            "bars_processed": record.bars_processed,
            "utc": datetime.now(timezone.utc).isoformat(),
        })

    def _process_or_bar(self, record: SessionRecord, bar_dict: dict):
        """Process a bar during the opening range window."""
        record.or_bars.append(bar_dict)
        if len(record.or_bars) >= OR_BAR_COUNT:
            record.or_high = max(b["high"] for b in record.or_bars[:OR_BAR_COUNT])
            record.or_low = min(b["low"] for b in record.or_bars[:OR_BAR_COUNT])
            record.phase = SessionPhase.POST_RANGE
            self._log_event({
                "event": "OPENING_RANGE_COMPLETE",
                "session_date": record.session_date.strftime("%Y-%m-%d"),
                "or_high": record.or_high,
                "or_low": record.or_low,
                "bar_count": len(record.or_bars),
                "utc": datetime.now(timezone.utc).isoformat(),
            })

    def _process_post_range_bar(self, record: SessionRecord, bar_dict: dict):
        """Process a bar after the opening range is complete."""
        if record.direction is not None:
            self._process_exit_check(record, bar_dict)
            return

        if record.or_high is None or record.or_low is None:
            return

        c = bar_dict["close"]
        if c > record.or_high:
            record.direction = Direction.LONG
            record.signal_bar = bar_dict
            record.phase = SessionPhase.POST_RANGE
            self._log_event({
                "event": "SIGNAL_LONG",
                "session_date": record.session_date.strftime("%Y-%m-%d"),
                "signal_bar_time": bar_dict["time_str"],
                "close": c,
                "or_high": record.or_high,
                "utc": datetime.now(timezone.utc).isoformat(),
            })
            self._attempt_entry(record, bar_dict)
        elif c < record.or_low:
            record.direction = Direction.SHORT
            record.signal_bar = bar_dict
            record.phase = SessionPhase.POST_RANGE
            self._log_event({
                "event": "SIGNAL_SHORT",
                "session_date": record.session_date.strftime("%Y-%m-%d"),
                "signal_bar_time": bar_dict["time_str"],
                "close": c,
                "or_low": record.or_low,
                "utc": datetime.now(timezone.utc).isoformat(),
            })
            self._attempt_entry(record, bar_dict)

    def _attempt_entry(self, record: SessionRecord, signal_bar: dict):
        """Attempt theoretical entry at next bar open (observation only)."""
        signal_close_time = signal_bar["time"] + 60
        entry_et = _utc_epoch_to_et(signal_close_time)
        entry_session_date = self._get_session_date(entry_et)
        if entry_session_date != record.session_date:
            return
        record.entry_bar = {"time": signal_close_time, "time_str": entry_et.strftime("%Y-%m-%d %H:%M:%S")}
        record.entry_price = None
        record.phase = SessionPhase.POSITION_OPEN
        self.stats["positions_opened"] += 1
        self._log_event({
            "event": "ENTRY_PENDING",
            "session_date": record.session_date.strftime("%Y-%m-%d"),
            "entry_bar_time": entry_et.strftime("%Y-%m-%d %H:%M:%S"),
            "direction": record.direction.value,
            "utc": datetime.now(timezone.utc).isoformat(),
        })

    def _process_position_bar(self, record: SessionRecord, bar_dict: dict):
        """Process a bar while a theoretical position is open."""
        if record.entry_price is None and record.entry_bar is not None:
            if bar_dict["time"] == record.entry_bar["time"]:
                record.entry_price = bar_dict["open"]
                self._log_event({
                    "event": "ENTRY_EXECUTED",
                    "session_date": record.session_date.strftime("%Y-%m-%d"),
                    "entry_price": record.entry_price,
                    "entry_bar_time": bar_dict["time_str"],
                    "direction": record.direction.value,
                    "utc": datetime.now(timezone.utc).isoformat(),
                })
        if record.entry_price is None:
            return
        self._process_exit_check(record, bar_dict)

    def _process_exit_check(self, record: SessionRecord, bar_dict: dict):
        """Check exit conditions for an open position."""
        if record.entry_bar is None:
            return
        if bar_dict["time"] <= record.entry_bar["time"] + 60:
            return
        final_bar_time_et = record.session_end - timedelta(minutes=1)
        final_bar_time_epoch = int(_et_to_utc_epoch(final_bar_time_et))
        is_final = bar_dict["time"] == final_bar_time_epoch
        retrace = False
        if record.direction == Direction.LONG:
            retrace = bar_dict["close"] <= record.or_high
        elif record.direction == Direction.SHORT:
            retrace = bar_dict["close"] >= record.or_low
        if is_final:
            record.exit_bar = bar_dict
            record.exit_price = bar_dict["open"]
            record.exit_type = ExitType.SESSION_CLOSE
            record.phase = SessionPhase.SESSION_CLOSED
            record.status = ObservationStatus.POSITION_CLOSED
            self.stats["positions_closed"] += 1
            self._log_event({
                "event": "EXIT_SESSION_CLOSE",
                "session_date": record.session_date.strftime("%Y-%m-%d"),
                "exit_price": record.exit_price,
                "exit_bar_time": bar_dict["time_str"],
                "direction": record.direction.value,
                "utc": datetime.now(timezone.utc).isoformat(),
            })
            return
        if retrace:
            record.exit_bar = bar_dict
            record.exit_price = bar_dict["open"]
            record.exit_type = ExitType.RETRACE
            record.phase = SessionPhase.SESSION_CLOSED
            record.status = ObservationStatus.POSITION_CLOSED
            self.stats["positions_closed"] += 1
            self._log_event({
                "event": "EXIT_RETRACE",
                "session_date": record.session_date.strftime("%Y-%m-%d"),
                "exit_price": record.exit_price,
                "exit_bar_time": bar_dict["time_str"],
                "direction": record.direction.value,
                "utc": datetime.now(timezone.utc).isoformat(),
            })

    # --------------------------------------------------------- public interface

    def on_tick(self, quote=None):
        """Called once per supervisor loop tick. Never raises."""
        try:
            if self.feed is None:
                return
            bar = self.feed.latest_completed_bar(BROKER_SYMBOL, TIMEFRAME)
            if bar is None:
                self.stats["feed_unavailable"] += 1
                self._save_status()
                return
            self._process_bar(bar)
        except Exception as e:
            self.stats["errors"] += 1
            self.last_error = repr(e)
            self._save_status()
            self._log_event({
                "event": "OBSERVER_ERROR",
                "error": repr(e),
                "utc": datetime.now(timezone.utc).isoformat(),
            })

    def _process_bar(self, bar: dict):
        """Process a single completed M1 bar."""
        ok, reason = self._validate_bar(bar)
        if not ok:
            if reason.startswith("feed_status:"):
                self.stats["feed_unavailable"] += 1
            else:
                self.stats["data_quality_exceptions"] += 1
                self._log_event({
                    "event": "BAR_REJECTED",
                    "reason": reason,
                    "bar_time": bar.get("time"),
                    "utc": datetime.now(timezone.utc).isoformat(),
                })
            self._save_status()
            return

        t = int(bar["time"])
        if self._last_bar_time is not None and t <= self._last_bar_time:
            return
        self._last_bar_time = t
        self.stats["total_bars_received"] += 1

        et_dt = _utc_epoch_to_et(t)
        session_date = self._get_session_date(et_dt)

        freeze_date = FREEZE_BOUNDARY_ET.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        if session_date < freeze_date:
            self.stats["pre_freeze_bars_skipped"] += 1
            self._save_status()
            return

        self.stats["bars_after_freeze"] += 1

        if not self._is_us_session(et_dt):
            self.stats["asian_session_bars_skipped"] += 1
            if self._current_session is not None:
                self._finalize_session(self._current_session)
                self._current_session = None
                self._active_session_date = None
            self._save_status()
            return

        bar_dict = self._bar_to_dict(bar)

        session_key = session_date.strftime("%Y-%m-%d")
        if self._current_session is None or self._active_session_date != session_key:
            if self._current_session is not None:
                self._finalize_session(self._current_session)
            self._current_session = SessionRecord(session_date)
            self._active_session_date = session_key
            self._log_event({
                "event": "SESSION_STARTED",
                "session_date": session_key,
                "utc": datetime.now(timezone.utc).isoformat(),
            })

        record = self._current_session
        record.bars_processed += 1

        if record.phase == SessionPhase.SESSION_CLOSED:
            return

        if self._is_or_window(et_dt):
            if record.phase in (SessionPhase.PRE_SESSION, SessionPhase.OPENING_RANGE):
                record.phase = SessionPhase.OPENING_RANGE
                self._process_or_bar(record, bar_dict)
        else:
            if record.phase == SessionPhase.OPENING_RANGE:
                if record.or_high is None:
                    record.status = ObservationStatus.DATA_INCOMPLETE
                    self.stats["data_incomplete"] += 1
                    self._finalize_session(record)
                    self._current_session = None
                    self._active_session_date = None
                    self._save_status()
                    return
            if record.phase in (SessionPhase.POST_RANGE, SessionPhase.POSITION_OPEN):
                if record.direction is not None:
                    self._process_position_bar(record, bar_dict)
                else:
                    self._process_post_range_bar(record, bar_dict)

        self._save_status()

    def status(self):
        """Print operational status."""
        print("=== FB-001 ORB OBSERVER STATUS ===")
        print(f"version: {VERSION}")
        print(f"registration: FB-001-ORB-V38A-REG-V1-r1")
        print(f"registration_sha: 04e9f804cca93d64ea18396abf5d25d2b968df974ee505f2b0866104e1af8086")
        print(f"broker_symbol: {BROKER_SYMBOL} | timeframe: {TIMEFRAME}")
        print(f"data_dir: {self.data_dir}")
        print(f"sessions_dir: {self.sessions_dir}")
        print(f"freeze_boundary_et: {FREEZE_BOUNDARY_ET.strftime('%Y-%m-%d %H:%M:%S')}")
        for k, v in self.stats.items():
            print(f"stats.{k}: {v}")
        print(f"last_bar_time: {self._last_bar_time}")
        print(f"last_error: {self.last_error}")
        if self._current_session:
            print(f"current_session: {self._current_session.session_date.strftime('%Y-%m-%d')} "
                  f"phase={self._current_session.phase.value}")
        else:
            print("current_session: None")
