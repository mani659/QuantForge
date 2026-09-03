"""F-01 Live Observation Recorder — governed data-capture sidecar (v1.0.0).

Infrastructure milestone: F-01 LIVE MARKET-OBSERVATION RECORDER
(QUANTFORGE_F01_LIVE_OBSERVATION_RECORDER_V1.md).

PURPOSE (only):
  Preserve genuine raw USTECm M1 observations from the already-running MT5
  environment so the governed F-01 accrual pipeline can accumulate the
  registered post-freeze study evidence.

THE RECORDER IS NOT A TRADING MODULE:
  - it never places, modifies, or manages orders or positions;
  - it never computes returns, P&L, or any economic performance quantity;
  - it never makes F-01 decisions and never filters observations by expected
    profitability;
  - it never launches the registered economic validation stage;
  - it never alters the F-01 registration, calendar, session logic, cost
    model, or validation scope.

ARCHITECTURE (attachment, not duplication):
  Attaches to the Unified Runner supervisor's own MT5MarketFeed instance
  (scripts/forward/market_data.py) — the same feed used by the three paper
  modules — and polls the latest COMPLETED M1 bar once per loop tick.
  Raw observations are appended to an isolated raw recorder archive under
  data/f01/raw/ (gitignored data area), never into the study archive. The
  governed accrual pipeline (research/f01_v38a_accrual_pipeline.py) remains
  the sole authority for study admission, boundary enforcement, snapshot
  hashing, ledger, and state.

DATA BOUNDARY:
  The registered study begins at the frozen boundary 2026-09-03. This
  recorder PRESERVES raw source observations regardless of timestamp; the
  accrual pipeline rejects pre-freeze rows from entering the study. Only the
  newest M1 bar is ever fetched (copy_rates_from_pos count=1), so no
  historical window is retrieved by this module.

TIMESTAMP GOVERNANCE:
  The MT5 source epoch timestamp is preserved exactly and rendered to a
  deterministic UTC ISO representation, following the existing runner
  convention that treats MT5 epochs as UTC. The local clock is recorded only
  as an acquisition timestamp and never replaces the source bar timestamp.

CLI MODES:
  --smoke-test   isolated structural tests T1-T15 (synthetic feed, temp root)
  --verify       live non-economic smoke: connect, check USTECm, capture the
                 latest completed M1 bar into the raw recorder archive
  --handoff      invoke the governed accrual pipeline on the raw archive
  --status       print operational status (no economics)
"""

import argparse
import csv
import hashlib
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone

VERSION = "1.0.0"
LOGICAL_SYMBOL = "USATECHIDXUSD"
BROKER_SYMBOL = "USTECm"
TIMEFRAME = "M1"
SCHEMA = ["timestamp", "open", "high", "low", "close", "volume"]
RAW_DIR_NAME = "raw"
RAW_ARCHIVE_NAME = "ustechidxusd_m1_raw.csv"
EVENTS_LOG_NAME = "recorder_events.jsonl"
STATUS_FILE_NAME = "recorder_status.json"


def _project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _default_raw_dir():
    return os.path.join(_project_root(), "data", "f01", RAW_DIR_NAME)


class F01ObservationRecorder:
    """Captures completed USTECm M1 bars into an append-only raw archive.

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
        self.last_bar = None      # {"time": epoch, "o":.., "h":.., "l":.., "c":..}
        self.last_error = None
        self._load_state()

    # ------------------------------------------------------------- state
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
                        "o": float(lb["o"]), "h": float(lb["h"]),
                        "l": float(lb["l"]), "c": float(lb["c"]),
                    }
            except Exception:
                pass
        if self.last_bar is None and os.path.exists(self.raw_archive):
            tail = self._tail_row()
            if tail:
                try:
                    self.last_bar = {
                        "time": int(datetime.strptime(tail["timestamp"], "%Y-%m-%d %H:%M:%S").timestamp()),
                        "o": float(tail["open"]), "h": float(tail["high"]),
                        "l": float(tail["low"]), "c": float(tail["close"]),
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

    # ------------------------------------------------------------- capture
    def _validate_bar(self, bar):
        """Deterministic structural validation. Returns (ok, reason)."""
        if bar.get("status") != "DATA_FRESH":
            return False, "feed_status:" + str(bar.get("status"))
        if bar.get("symbol") != BROKER_SYMBOL:
            return False, "symbol_mismatch:" + str(bar.get("symbol"))
        try:
            t = int(bar["time"])
            o = float(bar["open"]); h = float(bar["high"])
            lo = float(bar["low"]); c = float(bar["close"])
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
                self._log_event({"event": "SYMBOL_MISMATCH_REJECTED", "symbol": bar.get("symbol"),
                                 "reason": reason, "utc": datetime.now(timezone.utc).isoformat()})
            else:
                self.stats["malformed"] += 1
                self._log_event({"event": "MALFORMED_BAR_REJECTED", "reason": reason,
                                 "bar_time": bar.get("time"), "utc": datetime.now(timezone.utc).isoformat()})
            self._save_status()
            return

        t = int(bar["time"]); o = float(bar["open"]); h = float(bar["high"])
        lo = float(bar["low"]); c = float(bar["close"])
        volume = int(bar.get("volume", 0) or 0)

        if self.last_bar is not None and t < self.last_bar["time"]:
            self._log_event({"event": "STALE_BAR_SKIPPED", "bar_time": t,
                             "last_time": self.last_bar["time"], "utc": datetime.now(timezone.utc).isoformat()})
            return
        if self.last_bar is not None and t == self.last_bar["time"]:
            same = (o == self.last_bar["o"] and h == self.last_bar["h"]
                    and lo == self.last_bar["l"] and c == self.last_bar["c"])
            if same:
                self.stats["exact_duplicates"] += 1
                self._save_status()
                return
            self.stats["conflicting_duplicates"] += 1
            self._log_event({"event": "CONFLICTING_DUPLICATE_QUARANTINED",
                             "bar_time": t, "received": {"o": o, "h": h, "l": lo, "c": c},
                             "existing": self.last_bar,
                             "utc": datetime.now(timezone.utc).isoformat()})
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
            self._log_event({"event": "RECORDER_ERROR", "error": repr(e),
                             "utc": datetime.now(timezone.utc).isoformat()})

    # ------------------------------------------------------------- handoff
    def handoff(self, ingest_path=None, archive_path=None, ledger_path=None, state_path=None):
        """Invoke the governed accrual pipeline on the raw archive.

        The accrual pipeline remains authoritative for admission, boundary,
        snapshot, ledger, and state. This method only hands the raw file to
        that governed interface.
        """
        sys.path.insert(0, os.path.join(_project_root(), "research"))
        import f01_v38a_accrual_pipeline as pipe

        raw = ingest_path if ingest_path is not None else self.raw_archive
        if not os.path.exists(raw):
            return {"errors": ["RAW ARCHIVE NOT FOUND"], "source": raw}
        base = os.path.join(_project_root(), "data", "f01")
        arc = archive_path if archive_path is not None else os.path.join(base, "ustechidxusd_m1_study.csv")
        led = ledger_path if ledger_path is not None else os.path.join(base, "snapshot_ledger.jsonl")
        sta = state_path if state_path is not None else os.path.join(base, "accrual_state.json")
        cal = pipe.load_calendar(pipe.CALENDAR_PATH)
        return pipe.ingest(raw, base, arc, led, sta, cal)

    def status(self):
        print("=== F-01 OBSERVATION RECORDER STATUS ===")
        print("version:", VERSION)
        print("broker_symbol:", BROKER_SYMBOL, "| timeframe:", TIMEFRAME)
        print("raw_archive:", self.raw_archive)
        for k, v in self.stats.items():
            print("stats." + k + ":", v)
        print("last_bar:", self.last_bar)
        print("last_error:", self.last_error)

    # ------------------------------------------------------------- tests
    def smoke_test(self):
        """Structural tests T1-T15. Synthetic feed, isolated temp root only."""
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

        def bar(t, o=20000.0, h=20005.0, l=19995.0, c=20002.0, symbol=BROKER_SYMBOL):
            return {"status": "DATA_FRESH", "symbol": symbol, "time": t,
                    "open": o, "high": h, "low": l, "close": c, "volume": 100}

        base_t = int(time.time()) // 60 * 60 - 3600  # one hour ago, minute-aligned

        with tempfile.TemporaryDirectory(prefix="f01_recorder_test_") as td:
            # T2: M1-only request
            feed = FakeFeed([bar(base_t)])
            rec = F01ObservationRecorder(feed=feed, raw_dir=td)
            rec.on_tick({})
            check("T2 M1-only capture (requests M1)", feed.last_tf == "M1")
            check("T2 first bar captured", rec.stats["total_captured"] == 1)

            # T1: symbol identity
            feed2 = FakeFeed([bar(base_t + 60, symbol="EURUSD")])
            rec2 = F01ObservationRecorder(feed=feed2, raw_dir=os.path.join(td, "r2"))
            rec2.on_tick({})
            check("T1 symbol mismatch rejected", rec2.stats["symbol_mismatch"] == 1
                  and rec2.stats["total_captured"] == 0)

            # T3/T4: closed-bar policy + exact duplicate idempotency
            feed3 = FakeFeed([bar(base_t + 120), bar(base_t + 120)])
            rec3 = F01ObservationRecorder(feed=feed3, raw_dir=os.path.join(td, "r3"))
            rec3.on_tick({}); rec3.on_tick({})
            check("T3 closed-bar policy (same bar not re-persisted)", rec3.stats["total_captured"] == 1)
            check("T4 exact duplicate idempotent", rec3.stats["exact_duplicates"] == 1)

            # T5: conflicting duplicate quarantined, archive unchanged
            feed5 = FakeFeed([bar(base_t + 180, c=20003.0), bar(base_t + 180, c=20004.0)])
            rec5 = F01ObservationRecorder(feed=feed5, raw_dir=os.path.join(td, "r5"))
            rec5.on_tick({})
            h_before = hashlib.sha256(open(rec5.raw_archive, "rb").read()).hexdigest()
            rec5.on_tick({})
            h_after = hashlib.sha256(open(rec5.raw_archive, "rb").read()).hexdigest()
            check("T5 conflicting duplicate quarantined, archive unchanged",
                  rec5.stats["conflicting_duplicates"] == 1 and h_before == h_after)

            # T6: malformed bar rejected
            feed6 = FakeFeed([bar(base_t + 240, o=-5.0)])
            rec6 = F01ObservationRecorder(feed=feed6, raw_dir=os.path.join(td, "r6"))
            rec6.on_tick({})
            check("T6 malformed bar rejected", rec6.stats["malformed"] == 1
                  and rec6.stats["total_captured"] == 0)

            # T7: append-only (archive stable when no new bar)
            feed7 = FakeFeed([bar(base_t + 300), bar(base_t + 300)])
            rec7 = F01ObservationRecorder(feed=feed7, raw_dir=os.path.join(td, "r7"))
            rec7.on_tick({})
            h1 = hashlib.sha256(open(rec7.raw_archive, "rb").read()).hexdigest()
            rec7.on_tick({})
            h2 = hashlib.sha256(open(rec7.raw_archive, "rb").read()).hexdigest()
            check("T7 append-only (no rewrite on duplicates)", h1 == h2)

            # T8: restart recovery
            feed8a = FakeFeed([bar(base_t + 360)])
            rec8 = F01ObservationRecorder(feed=feed8a, raw_dir=os.path.join(td, "r8"))
            rec8.on_tick({})
            feed8b = FakeFeed([bar(base_t + 360), bar(base_t + 420)])
            rec8b = F01ObservationRecorder(feed=feed8b, raw_dir=os.path.join(td, "r8"))
            rec8b.on_tick({}); rec8b.on_tick({})
            check("T8 restart recovery (old bar skipped, newer appended)",
                  rec8b.stats["exact_duplicates"] == 1 and rec8b.stats["total_captured"] == 2)

            # T9: feed reconnect behavior
            feed9 = FakeFeed([bar(base_t + 480)])
            rec9 = F01ObservationRecorder(feed=feed9, raw_dir=os.path.join(td, "r9"))
            rec9.on_tick({})
            feed9.bars = []  # unavailable
            rec9.on_tick({})
            feed9.bars = [bar(base_t + 540)]
            rec9.on_tick({})
            check("T9 reconnect survival (unavailable -> recover)", rec9.stats["feed_unavailable"] == 1
                  and rec9.stats["total_captured"] == 2)

            # T10: source timestamp preserved as UTC ISO in archive
            import csv as _csv
            with open(rec9.raw_archive, "r", newline="", encoding="utf-8") as f:
                rows = list(_csv.DictReader(f))
            first_ts = datetime.utcfromtimestamp(base_t + 480).strftime("%Y-%m-%d %H:%M:%S")
            check("T10 source timestamp preserved", rows[0]["timestamp"] == first_ts)

            # T13: recorder failure cannot alter trading-module behavior
            received = []
            class StubModule:
                def process_quote(self, quote, instance_id):
                    received.append(quote)
            rec13 = F01ObservationRecorder(feed=FakeFeed(fail=True), raw_dir=os.path.join(td, "r13"))
            for _ in range(3):
                for mod in (StubModule(),):
                    mod.process_quote({"x": 1}, "test")
                rec13.on_tick({})
            check("T13 recorder failure does not affect modules (loop survived)",
                  len(received) == 3 and rec13.stats["errors"] == 3)

            # T14/T11: fresh observations reach the accrual interface; pre-freeze rejected
            sys.path.insert(0, os.path.join(_project_root(), "research"))
            import f01_v38a_accrual_pipeline as pipe
            from datetime import date as _date, timedelta as _td
            cal = pipe.load_calendar(pipe.CALENDAR_PATH)
            bnd = pipe.freeze_boundary_utc()
            raw = os.path.join(td, "handoff_raw.csv")
            with open(raw, "w", newline="", encoding="utf-8") as f:
                w = _csv.writer(f); w.writerow(pipe.SCHEMA)
                w.writerow([(bnd - _td(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"), 20000.0, 20001.0, 19999.0, 20000.5, 0])
                w.writerow([(bnd + _td(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"), 20100.0, 20105.0, 20095.0, 20102.0, 0])
            arc = os.path.join(td, "study.csv"); led = os.path.join(td, "ledger.jsonl"); sta = os.path.join(td, "state.json")
            pipe.init(td, arc, led, sta, cal)
            rep = pipe.ingest(raw, td, arc, led, sta, cal)
            check("T11 pre-freeze cannot enter study (rejected by governed interface)",
                  rep["rejected_prefreeze"] == 1 and rep["admitted"] == 1)
            st = pipe.load_state(sta)
            check("T14 fresh observations reach accrual interface (state updated)",
                  st["archive_row_count"] == 1 and st["eligible_sessions_with_data"] == 1)

            # T12/T15: source-text firewall checks (constructed tokens only)
            src = open(os.path.abspath(__file__), encoding="utf-8").read()
            rt_root = "run" + "time" + "/"
            g6 = "G6_" + "CAND015"
            check("T12 protected data never referenced", rt_root not in src and g6 not in src)
            econ = ["np." + "log", "pct_" + "change", "compute_" + "return",
                    "expect" + "ancy", "sharp" + "e", "draw" + "down"]
            trades = ["order_" + "send", "place_" + "order", "position_" + "open",
                      "B" + "UY", "S" + "ELL", "stage" + "3"]
            check("T15 no economics and no trading tokens in source",
                  all(tok not in src for tok in econ + trades))

        print("---")
        failed = [n for n, c in results if not c]
        print("recorder smoke-test: %d/%d passed" % (len(results) - len(failed), len(results)))
        return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description="F-01 live observation recorder (structural only)")
    ap.add_argument("--smoke-test", action="store_true", help="isolated structural tests T1-T15")
    ap.add_argument("--verify", action="store_true", help="live non-economic smoke + genuine capture")
    ap.add_argument("--handoff", action="store_true", help="invoke governed accrual pipeline on raw archive")
    ap.add_argument("--status", action="store_true", help="print operational status")
    args = ap.parse_args()

    if args.smoke_test:
        sys.exit(F01ObservationRecorder().smoke_test())

    if args.verify:
        from market_data import MT5MarketFeed
        feed = MT5MarketFeed()
        print("=== F-01 RECORDER LIVE VERIFY (non-economic) ===")
        print("initialize:", feed.initialize())
        print("connection:", feed.connection_state())
        info = feed.terminal_info()
        print("terminal:", info)
        if feed.connection_state() != "CONNECTED":
            print("LIVE VERIFY BLOCKED — MT5 feed unavailable")
            feed.shutdown()
            sys.exit(1)
        quote = feed.latest_quote(BROKER_SYMBOL)
        print("latest_quote_status:", quote.get("status"))
        if quote.get("status") == "DATA_FRESH":
            print("quote_source_epoch:", quote.get("source_timestamp"))
            print("local_utc_epoch:", int(time.time()))
            print("observed_clock_offset_s:", int(time.time()) - int(quote.get("source_timestamp")))
        bar = feed.latest_completed_bar(BROKER_SYMBOL, TIMEFRAME)
        print("latest_completed_bar:", bar)
        if bar and bar.get("status") == "DATA_FRESH":
            rec = F01ObservationRecorder(feed=feed)
            rec._capture(bar)  # genuine bar -> raw recorder archive (governed)
            print("capture_result: total_captured:", rec.stats["total_captured"])
            print("raw_archive:", rec.raw_archive)
        else:
            print("NO FRESH M1 BAR AVAILABLE — nothing captured")
        feed.shutdown()
        return

    if args.handoff:
        rec = F01ObservationRecorder()
        rep = rec.handoff()
        print("handoff report:", json.dumps(rep, indent=2))
        sys.exit(0 if not rep.get("errors") else 1)

    if args.status:
        F01ObservationRecorder().status()
        return

    ap.print_help()


if __name__ == "__main__":
    main()