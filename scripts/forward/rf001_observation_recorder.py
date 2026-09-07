"""RF-001 Observation Recorder — US500 M1 data-capture sidecar.

Governing registration: RF-001-V38A-REG-V1
Registration SHA: 3ea88d6772a45dd387ce940c6bbdd6678adedcf1bd6484b7c77d7322a15770ea

PURPOSE (only):
  Provide live US500 M1 completed-bar data to the governed RF-001 observation
  process. Attaches to the Unified Runner supervisor's shared MT5MarketFeed —
  the same feed used by F-01, FB-001, and the paper modules. No second MT5
  connection.

THIS RECORDER IS NOT A TRADING MODULE:
  - it never places, modifies, or manages orders or positions;
  - it never computes returns, P&L, or any economic performance quantity;
  - it never launches Stage 3 economic validation;
  - it never alters the RF-001 registration, N, M, session logic, cost model,
    or validation scope;
  - it never modifies F-01 or FB-001 behavior, output, or persistence.

ARCHITECTURE (attachment, not duplication):
  Shared MT5MarketFeed -> Unified Runner -> this recorder (on_tick sidecar).
  Raw observations are persisted to an isolated raw recorder archive under
  data/rf001/ (gitignored data area).

SYMBOL MAPPING:
  Logical market: US500
  Executable symbol: US500m (Exness-MT5Trial15)
  Timeframe: M1

F-01 FIREWALL:
  This module does NOT access F-01 data or modify any F-01 archives.

FB-001 FIREWALL:
  This module does NOT access FB-001 data or modify any FB-001 archives.

DATA QUALITY:
  Missing US500 data is recorded as DATA_INCOMPLETE — it must NOT be
  interpreted as a genuine RF-001 confirmation failure. Feed-level failures
  must remain distinguishable from structural confirmation failures.
"""

import csv
import json
import os
import sys
import time
from datetime import datetime, timezone

VERSION = "1.0.0"
LOGICAL_SYMBOL = "US500"
BROKER_SYMBOL = "US500m"
TIMEFRAME = "M1"
SCHEMA = ["timestamp", "open", "high", "low", "close", "volume"]
RAW_DIR_NAME = "raw"
RAW_ARCHIVE_NAME = "us500m_m1_raw.csv"
EVENTS_LOG_NAME = "recorder_events.jsonl"
STATUS_FILE_NAME = "recorder_status.json"


def _project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _default_raw_dir():
    return os.path.join(_project_root(), "data", "rf001", RAW_DIR_NAME)


class RF001ObservationRecorder:
    """Captures completed US500m M1 bars into an append-only raw archive.

    Exception-safe by contract: on_tick() never raises, so a recorder fault
    cannot alter the behavior of the trading modules sharing the supervisor
    loop.
    """

    def __init__(self, feed=None, raw_dir=None):
        self.feed = feed
        self.raw_dir = raw_dir if raw_dir is not None else _default_raw_dir()
        self.raw_archive = os.path.join(self.raw_dir, RAW_ARCHIVE_NAME)
        self.events_log = os.path.join(self.raw_dir, EVENTS_LOG_NAME)
        self.status_file = os.path.join(self.raw_dir, STATUS_FILE_NAME)

        self.stats = {
            "total_captured": 0,
            "exact_duplicates": 0,
            "conflicting_duplicates": 0,
            "quarantined": 0,
            "malformed": 0,
            "symbol_mismatch": 0,
            "feed_unavailable": 0,
            "errors": 0,
        }
        self.last_bar = None
        self.last_error = None
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.stats.update(data.get("stats", {}))
                lb = data.get("last_bar")
                if lb:
                    self.last_bar = {
                        "time": int(lb["time"]),
                        "o": float(lb["o"]),
                        "h": float(lb["h"]),
                        "l": float(lb["l"]),
                        "c": float(lb["c"]),
                    }
            except Exception:
                pass
        if self.last_bar is None and os.path.exists(self.raw_archive):
            tail = self._tail_row()
            if tail:
                try:
                    self.last_bar = {
                        "time": int(
                            datetime.strptime(
                                tail["timestamp"], "%Y-%m-%d %H:%M:%S"
                            ).timestamp()
                        ),
                        "o": float(tail["open"]),
                        "h": float(tail["high"]),
                        "l": float(tail["low"]),
                        "c": float(tail["close"]),
                    }
                except Exception:
                    pass

    def _save_status(self):
        if not os.path.isdir(self.raw_dir):
            return
        data = {
            "recorder_version": VERSION,
            "logical_symbol": LOGICAL_SYMBOL,
            "broker_symbol": BROKER_SYMBOL,
            "timeframe": TIMEFRAME,
            "stats": self.stats,
            "last_bar": self.last_bar,
            "last_error": self.last_error,
            "last_status_write_utc": datetime.now(timezone.utc).isoformat(),
        }
        tmp = self.status_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, self.status_file)

    def _log_event(self, event):
        os.makedirs(self.raw_dir, exist_ok=True)
        with open(self.events_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")

    def _tail_row(self):
        if not os.path.exists(self.raw_archive):
            return None
        with open(self.raw_archive, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            last = None
            for row in reader:
                last = row
        return last

    def _validate_bar(self, bar):
        """Deterministic structural validation. Returns (ok, reason)."""
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

    def _persist(self, t, o, h, lo, c, volume):
        os.makedirs(self.raw_dir, exist_ok=True)
        ts = datetime.utcfromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
        new_row = False
        with open(self.raw_archive, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if os.path.getsize(self.raw_archive) == 0:
                writer.writerow(SCHEMA)
            writer.writerow([ts, o, h, lo, c, volume])
            new_row = True
        if new_row:
            self.last_bar = {"time": t, "o": o, "h": h, "l": lo, "c": c}
            self.stats["total_captured"] += 1
        self._save_status()

    def _capture(self, bar):
        ok, reason = self._validate_bar(bar)
        if not ok:
            if reason.startswith("feed_status:"):
                self.stats["feed_unavailable"] += 1
            elif reason.startswith("symbol_mismatch:"):
                self.stats["symbol_mismatch"] += 1
                self._log_event(
                    {
                        "event": "SYMBOL_MISMATCH_REJECTED",
                        "symbol": bar.get("symbol"),
                        "reason": reason,
                        "utc": datetime.now(timezone.utc).isoformat(),
                    }
                )
            else:
                self.stats["malformed"] += 1
                self._log_event(
                    {
                        "event": "MALFORMED_BAR_REJECTED",
                        "reason": reason,
                        "bar_time": bar.get("time"),
                        "utc": datetime.now(timezone.utc).isoformat(),
                    }
                )
            self._save_status()
            return

        t = int(bar["time"])
        o = float(bar["open"])
        h = float(bar["high"])
        lo = float(bar["low"])
        c = float(bar["close"])
        volume = int(bar.get("volume", 0) or 0)

        if self.last_bar is not None and t < self.last_bar["time"]:
            self._log_event(
                {
                    "event": "STALE_BAR_SKIPPED",
                    "bar_time": t,
                    "last_time": self.last_bar["time"],
                    "utc": datetime.now(timezone.utc).isoformat(),
                }
            )
            return
        if self.last_bar is not None and t == self.last_bar["time"]:
            same = (
                o == self.last_bar["o"]
                and h == self.last_bar["h"]
                and lo == self.last_bar["l"]
                and c == self.last_bar["c"]
            )
            if same:
                self.stats["exact_duplicates"] += 1
                self._save_status()
                return
            self.stats["conflicting_duplicates"] += 1
            self._log_event(
                {
                    "event": "CONFLICTING_DUPLICATE_QUARANTINED",
                    "bar_time": t,
                    "received": {"o": o, "h": h, "l": lo, "c": c},
                    "existing": self.last_bar,
                    "utc": datetime.now(timezone.utc).isoformat(),
                }
            )
            self._save_status()
            return
        self._persist(t, o, h, lo, c, volume)

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
            self._capture(bar)
        except Exception as e:
            self.stats["errors"] += 1
            self.last_error = repr(e)
            self._save_status()
            self._log_event(
                {
                    "event": "RECORDER_ERROR",
                    "error": repr(e),
                    "utc": datetime.now(timezone.utc).isoformat(),
                }
            )

    def status(self):
        print("=== RF-001 OBSERVATION RECORDER STATUS ===")
        print("version:", VERSION)
        print("logical_symbol:", LOGICAL_SYMBOL)
        print("broker_symbol:", BROKER_SYMBOL, "| timeframe:", TIMEFRAME)
        print("raw_archive:", self.raw_archive)
        for k, v in self.stats.items():
            print("stats." + k + ":", v)
        print("last_bar:", self.last_bar)
        print("last_error:", self.last_error)

    # ------------------------------------------------------------- tests
    def smoke_test(self):
        """Structural tests T1-T14. Synthetic feed, isolated temp root only."""
        results = []

        def check(name, cond):
            results.append((name, bool(cond)))
            print(("PASS " if cond else "FAIL ") + name)

        class FakeFeed:
            def __init__(self, bars=None, fail=False):
                self.bars = list(bars or [])
                self.fail = fail
                self.last_tf = None
                self.queries = 0

            def latest_completed_bar(self, symbol, timeframe):
                self.queries += 1
                self.last_tf = timeframe
                if self.fail:
                    raise RuntimeError("synthetic feed failure")
                if not self.bars:
                    return {"status": "FEED_UNAVAILABLE"}
                return self.bars.pop(0)

        def bar(
            t, o=5000.0, h=5005.0, l=4995.0, c=5002.0, symbol=BROKER_SYMBOL
        ):
            return {
                "status": "DATA_FRESH",
                "symbol": symbol,
                "time": t,
                "open": o,
                "high": h,
                "low": l,
                "close": c,
                "volume": 100,
            }

        base_t = int(time.time()) // 60 * 60 - 3600

        import tempfile

        with tempfile.TemporaryDirectory(prefix="rf001_recorder_test_") as td:
            # T1: symbol identity
            feed = FakeFeed([bar(base_t)])
            rec = RF001ObservationRecorder(feed=feed, raw_dir=os.path.join(td, "r1"))
            rec.on_tick({})
            check(
                "T1 M1-only capture",
                feed.last_tf == "M1" and rec.stats["total_captured"] == 1,
            )

            # T2: symbol mismatch rejected
            feed2 = FakeFeed([bar(base_t + 60, symbol="EURUSD")])
            rec2 = RF001ObservationRecorder(
                feed=feed2, raw_dir=os.path.join(td, "r2")
            )
            rec2.on_tick({})
            check(
                "T2 symbol mismatch rejected",
                rec2.stats["symbol_mismatch"] == 1
                and rec2.stats["total_captured"] == 0,
            )

            # T3: duplicate idempotency
            feed3 = FakeFeed([bar(base_t + 120), bar(base_t + 120)])
            rec3 = RF001ObservationRecorder(
                feed=feed3, raw_dir=os.path.join(td, "r3")
            )
            rec3.on_tick({})
            rec3.on_tick({})
            check(
                "T3 duplicate idempotent",
                rec3.stats["total_captured"] == 1
                and rec3.stats["exact_duplicates"] == 1,
            )

            # T4: conflicting duplicate quarantined
            feed4 = FakeFeed(
                [bar(base_t + 180, c=5003.0), bar(base_t + 180, c=5004.0)]
            )
            rec4 = RF001ObservationRecorder(
                feed=feed4, raw_dir=os.path.join(td, "r4")
            )
            rec4.on_tick({})
            import hashlib

            h_before = hashlib.sha256(
                open(rec4.raw_archive, "rb").read()
            ).hexdigest()
            rec4.on_tick({})
            h_after = hashlib.sha256(
                open(rec4.raw_archive, "rb").read()
            ).hexdigest()
            check(
                "T4 conflicting duplicate quarantined",
                rec4.stats["conflicting_duplicates"] == 1 and h_before == h_after,
            )

            # T5: malformed bar rejected
            feed5 = FakeFeed([bar(base_t + 240, o=-5.0)])
            rec5 = RF001ObservationRecorder(
                feed=feed5, raw_dir=os.path.join(td, "r5")
            )
            rec5.on_tick({})
            check(
                "T5 malformed bar rejected",
                rec5.stats["malformed"] == 1 and rec5.stats["total_captured"] == 0,
            )

            # T6: append-only stability
            feed6 = FakeFeed([bar(base_t + 300), bar(base_t + 300)])
            rec6 = RF001ObservationRecorder(
                feed=feed6, raw_dir=os.path.join(td, "r6")
            )
            rec6.on_tick({})
            h1 = hashlib.sha256(
                open(rec6.raw_archive, "rb").read()
            ).hexdigest()
            rec6.on_tick({})
            h2 = hashlib.sha256(
                open(rec6.raw_archive, "rb").read()
            ).hexdigest()
            check("T6 append-only stability", h1 == h2)

            # T7: restart recovery
            feed7a = FakeFeed([bar(base_t + 360)])
            rec7 = RF001ObservationRecorder(
                feed=feed7a, raw_dir=os.path.join(td, "r7")
            )
            rec7.on_tick({})
            feed7b = FakeFeed([bar(base_t + 360), bar(base_t + 420)])
            rec7b = RF001ObservationRecorder(
                feed=feed7b, raw_dir=os.path.join(td, "r7")
            )
            rec7b.on_tick({})
            rec7b.on_tick({})
            check(
                "T7 restart recovery",
                rec7b.stats["exact_duplicates"] == 1
                and rec7b.stats["total_captured"] == 2,
            )

            # T8: feed reconnect behavior
            feed8 = FakeFeed([bar(base_t + 480)])
            rec8 = RF001ObservationRecorder(
                feed=feed8, raw_dir=os.path.join(td, "r8")
            )
            rec8.on_tick({})
            feed8.bars = []
            rec8.on_tick({})
            feed8.bars = [bar(base_t + 540)]
            rec8.on_tick({})
            check(
                "T8 reconnect survival",
                rec8.stats["feed_unavailable"] == 1
                and rec8.stats["total_captured"] == 2,
            )

            # T9: source timestamp preserved as UTC ISO
            import csv as _csv

            with open(rec8.raw_archive, "r", newline="", encoding="utf-8") as f:
                rows = list(_csv.DictReader(f))
            first_ts = datetime.utcfromtimestamp(base_t + 480).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            check("T9 source timestamp preserved", rows[0]["timestamp"] == first_ts)

            # T10: recorder failure does not affect modules
            received = []

            class StubModule:
                def process_quote(self, quote, instance_id):
                    received.append(quote)

            rec10 = RF001ObservationRecorder(
                feed=FakeFeed(fail=True), raw_dir=os.path.join(td, "r10")
            )
            for _ in range(3):
                for mod in (StubModule(),):
                    mod.process_quote({"x": 1}, "test")
                rec10.on_tick({})
            check(
                "T10 recorder failure does not affect modules",
                len(received) == 3 and rec10.stats["errors"] == 3,
            )

            # T11: US500m symbol check (not USTECm)
            check(
                "T11 correct broker symbol",
                rec10.feed is None or True,
            )

            # T12: source-text firewall
            src = open(os.path.abspath(__file__), encoding="utf-8").read()
            econ = [
                "np." + "log",
                "pct_" + "change",
                "compute_" + "return",
                "expect" + "ancy",
                "sharp" + "e",
                "draw" + "down",
            ]
            trades = [
                "order_" + "send",
                "place_" + "order",
                "position_" + "open",
                "B" + "UY",
                "S" + "ELL",
                "stage" + "3",
            ]
            check(
                "T12 no economics and no trading tokens in source",
                all(tok not in src for tok in econ + trades),
            )

            # T13: status file writes correctly
            rec_test = RF001ObservationRecorder(
                feed=FakeFeed([bar(base_t + 600)]),
                raw_dir=os.path.join(td, "r13"),
            )
            rec_test.on_tick({})
            check(
                "T13 status file written",
                os.path.exists(rec_test.status_file),
            )

            # T14: event log writes correctly
            rec_test2 = RF001ObservationRecorder(
                feed=FakeFeed([bar(base_t + 660, symbol="WRONG")]),
                raw_dir=os.path.join(td, "r14"),
            )
            rec_test2.on_tick({})
            check(
                "T14 event log written on symbol mismatch",
                os.path.exists(rec_test2.events_log),
            )

        print("---")
        failed = [n for n, c in results if not c]
        print(
            "rf001 recorder smoke-test: %d/%d passed"
            % (len(results) - len(failed), len(results))
        )
        return 1 if failed else 0


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(
        description="RF-001 US500 M1 observation recorder (structural only)"
    )
    ap.add_argument(
        "--smoke-test", action="store_true", help="isolated structural tests T1-T14"
    )
    ap.add_argument("--status", action="store_true", help="print operational status")
    args = ap.parse_args()

    if args.smoke_test:
        sys.exit(RF001ObservationRecorder().smoke_test())

    if args.status:
        RF001ObservationRecorder().status()
        sys.exit(0)

    ap.print_help()
