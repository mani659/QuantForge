"""RF-001 Observation Recorder — Two-market raw M1 data-capture sidecar.

Governing registration: RF-001-V38A-REG-V1
Registration SHA: 3ea88d6772a45dd387ce940c6bbdd6678adedcf1bd6484b7c77d7322a15770ea

PURPOSE (only):
  Capture raw completed M1 observations for BOTH markets required by the
  frozen RF-001 registration:
    Primary:      USATECHIDXUSD / USTECm
    Confirmation: US500 / US500m
  through the shared MT5TimeoutMarketFeed. No second MT5 connection.

THIS RECORDER IS NOT A TRADING MODULE:
  - it never places, modifies, or manages orders or positions;
  - it never computes returns, P&L, or any economic performance quantity;
  - it never launches Stage 3 economic validation;
  - it never alters the RF-001 registration, N, M, session logic, cost model,
    or validation scope;
  - it never modifies F-01 or FB-001 behavior, output, or persistence.

ARCHITECTURE (attachment, not duplication):
  Shared MT5TimeoutMarketFeed -> Unified Runner -> this recorder (on_tick sidecar).
  Both USTECm and US500m are polled through the same shared feed instance.
  Raw synchronized observations are persisted to data/rf001/raw/.

SYMBOL MAPPING:
  Primary market:      USATECHIDXUSD / USTECm (Exness-MT5Trial15)
  Confirmation market: US500 / US500m (Exness-MT5Trial15)
  Timeframe: M1

F-01 FIREWALL:
  This module does NOT access F-01 data or modify any F-01 archives.

FB-001 FIREWALL:
  This module does NOT access FB-001 data or modify any FB-001 archives.

DATA QUALITY:
  Missing data is recorded as a synchronization state (PRIMARY_ONLY,
  CONFIRMATION_ONLY, MISALIGNED) — it must NEVER be interpreted as
  a genuine RF-001 confirmation failure or primary event absence.
  Feed-level failures must remain distinguishable from structural
  confirmation failures.

SYNCHRONIZATION:
  Each tick polls both symbols. Timestamps are compared deterministically.
  Only MATCHED observations (both markets, same M1 interval) produce
  persisted synchronized rows. All other states are logged as events.
"""

import csv
import json
import os
import sys
import time
from datetime import datetime, timezone

VERSION = "2.0.0"
PRIMARY_SYMBOL = "USTECm"
PRIMARY_LOGICAL = "USATECHIDXUSD"
CONFIRMATION_SYMBOL = "US500m"
CONFIRMATION_LOGICAL = "US500"
TIMEFRAME = "M1"

SCHEMA = [
    "timestamp",
    "primary_open", "primary_high", "primary_low", "primary_close", "primary_volume",
    "confirmation_open", "confirmation_high", "confirmation_low", "confirmation_close", "confirmation_volume",
    "sync_state",
]

RAW_DIR_NAME = "raw"
RAW_ARCHIVE_NAME = "rf001_two_market_m1_raw.csv"
EVENTS_LOG_NAME = "recorder_events.jsonl"
STATUS_FILE_NAME = "recorder_status.json"


def _project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _default_raw_dir():
    return os.path.join(_project_root(), "data", "rf001", RAW_DIR_NAME)


class RF001ObservationRecorder:
    """Captures synchronized USTECm + US500m M1 bars into a raw archive.

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
            "total_ticks": 0,
            "matched_captures": 0,
            "primary_only_events": 0,
            "confirmation_only_events": 0,
            "misaligned_events": 0,
            "primary_unavailable": 0,
            "confirmation_unavailable": 0,
            "primary_malformed": 0,
            "confirmation_malformed": 0,
            "primary_exact_duplicates": 0,
            "confirmation_exact_duplicates": 0,
            "primary_conflicting_duplicates": 0,
            "confirmation_conflicting_duplicates": 0,
            "errors": 0,
        }
        self.last_primary_bar = None
        self.last_confirmation_bar = None
        self.last_error = None
        self._load_state()

    # ------------------------------------------------------------------ state

    def _load_state(self):
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.stats.update(data.get("stats", {}))
                lp = data.get("last_primary_bar")
                if lp:
                    self.last_primary_bar = {
                        "time": int(lp["time"]),
                        "o": float(lp["o"]), "h": float(lp["h"]),
                        "l": float(lp["l"]), "c": float(lp["c"]),
                    }
                lc = data.get("last_confirmation_bar")
                if lc:
                    self.last_confirmation_bar = {
                        "time": int(lc["time"]),
                        "o": float(lc["o"]), "h": float(lc["h"]),
                        "l": float(lc["l"]), "c": float(lc["c"]),
                    }
            except Exception:
                pass

    def _save_status(self):
        if not os.path.isdir(self.raw_dir):
            return
        data = {
            "recorder_version": VERSION,
            "primary_symbol": PRIMARY_SYMBOL,
            "confirmation_symbol": CONFIRMATION_SYMBOL,
            "timeframe": TIMEFRAME,
            "stats": self.stats,
            "last_primary_bar": self.last_primary_bar,
            "last_confirmation_bar": self.last_confirmation_bar,
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

    # ------------------------------------------------------------------ bars

    def _validate_bar(self, bar, expected_symbol):
        """Deterministic structural validation. Returns (ok, reason)."""
        if bar.get("status") != "DATA_FRESH":
            return False, "feed_status:" + str(bar.get("status"))
        if bar.get("symbol") != expected_symbol:
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

    def _bar_to_values(self, bar):
        """Extract OHLCV from validated bar."""
        return {
            "time": int(bar["time"]),
            "o": float(bar["open"]),
            "h": float(bar["high"]),
            "l": float(bar["low"]),
            "c": float(bar["close"]),
            "v": int(bar.get("volume", 0) or 0),
        }

    def _is_duplicate(self, new_bar, last_bar):
        """Check if new_bar is a duplicate of last_bar. Returns (is_dup, is_exact)."""
        if last_bar is None:
            return False, False
        if new_bar["time"] < last_bar["time"]:
            return True, False
        if new_bar["time"] == last_bar["time"]:
            same = (
                new_bar["o"] == last_bar["o"]
                and new_bar["h"] == last_bar["h"]
                and new_bar["l"] == last_bar["l"]
                and new_bar["c"] == last_bar["c"]
            )
            return True, same
        return False, False

    # --------------------------------------------------------- synchronization

    def _classify_sync(self, primary_bar, confirmation_bar, primary_ok, confirmation_ok):
        """Classify the synchronization state deterministically."""
        if primary_ok and confirmation_ok:
            if primary_bar["time"] == confirmation_bar["time"]:
                return "MATCHED"
            else:
                return "MISALIGNED"
        if primary_ok and not confirmation_ok:
            return "PRIMARY_ONLY"
        if not primary_ok and confirmation_ok:
            return "CONFIRMATION_ONLY"
        return "BOTH_UNAVAILABLE"

    # ------------------------------------------------------------ persistence

    def _persist_matched(self, ts, prim, conf):
        """Persist a MATCHED two-market observation."""
        os.makedirs(self.raw_dir, exist_ok=True)
        ts_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        row = [
            ts_str,
            prim["o"], prim["h"], prim["l"], prim["c"], prim["v"],
            conf["o"], conf["h"], conf["l"], conf["c"], conf["v"],
            "MATCHED",
        ]
        with open(self.raw_archive, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if os.path.getsize(self.raw_archive) == 0:
                writer.writerow(SCHEMA)
            writer.writerow(row)
        self.stats["matched_captures"] += 1
        self.last_primary_bar = prim
        self.last_confirmation_bar = conf
        self._save_status()

    # -------------------------------------------------------------- tick

    def on_tick(self, quote=None):
        """Called once per supervisor loop tick. Never raises."""
        try:
            if self.feed is None:
                return

            self.stats["total_ticks"] += 1

            # Poll both markets through shared feed
            prim_raw = self.feed.latest_completed_bar(PRIMARY_SYMBOL, TIMEFRAME)
            conf_raw = self.feed.latest_completed_bar(CONFIRMATION_SYMBOL, TIMEFRAME)

            # Validate primary
            primary_bar = None
            primary_ok = False
            if prim_raw is not None:
                ok, reason = self._validate_bar(prim_raw, PRIMARY_SYMBOL)
                if ok:
                    primary_bar = self._bar_to_values(prim_raw)
                    is_dup, is_exact = self._is_duplicate(primary_bar, self.last_primary_bar)
                    if is_dup:
                        if is_exact:
                            self.stats["primary_exact_duplicates"] += 1
                        else:
                            self.stats["primary_conflicting_duplicates"] += 1
                            self._log_event({
                                "event": "PRIMARY_CONFLICTING_DUPLICATE",
                                "bar_time": primary_bar["time"],
                                "utc": datetime.now(timezone.utc).isoformat(),
                            })
                    else:
                        primary_ok = True
                else:
                    if reason.startswith("feed_status:"):
                        self.stats["primary_unavailable"] += 1
                    else:
                        self.stats["primary_malformed"] += 1

            # Validate confirmation
            confirmation_bar = None
            confirmation_ok = False
            if conf_raw is not None:
                ok, reason = self._validate_bar(conf_raw, CONFIRMATION_SYMBOL)
                if ok:
                    confirmation_bar = self._bar_to_values(conf_raw)
                    is_dup, is_exact = self._is_duplicate(confirmation_bar, self.last_confirmation_bar)
                    if is_dup:
                        if is_exact:
                            self.stats["confirmation_exact_duplicates"] += 1
                        else:
                            self.stats["confirmation_conflicting_duplicates"] += 1
                            self._log_event({
                                "event": "CONFIRMATION_CONFLICTING_DUPLICATE",
                                "bar_time": confirmation_bar["time"],
                                "utc": datetime.now(timezone.utc).isoformat(),
                            })
                    else:
                        confirmation_ok = True
                else:
                    if reason.startswith("feed_status:"):
                        self.stats["confirmation_unavailable"] += 1
                    else:
                        self.stats["confirmation_malformed"] += 1

            # Classify synchronization
            sync_state = self._classify_sync(
                primary_bar, confirmation_bar, primary_ok, confirmation_ok
            )

            # Persist only MATCHED observations
            if sync_state == "MATCHED":
                self._persist_matched(primary_bar["time"], primary_bar, confirmation_bar)
            elif sync_state == "PRIMARY_ONLY":
                self.stats["primary_only_events"] += 1
                self._log_event({
                    "event": "PRIMARY_ONLY",
                    "primary_time": primary_bar["time"] if primary_bar else None,
                    "utc": datetime.now(timezone.utc).isoformat(),
                })
            elif sync_state == "CONFIRMATION_ONLY":
                self.stats["confirmation_only_events"] += 1
                self._log_event({
                    "event": "CONFIRMATION_ONLY",
                    "confirmation_time": confirmation_bar["time"] if confirmation_bar else None,
                    "utc": datetime.now(timezone.utc).isoformat(),
                })
            elif sync_state == "MISALIGNED":
                self.stats["misaligned_events"] += 1
                self._log_event({
                    "event": "MISALIGNED",
                    "primary_time": primary_bar["time"] if primary_bar else None,
                    "confirmation_time": confirmation_bar["time"] if confirmation_bar else None,
                    "utc": datetime.now(timezone.utc).isoformat(),
                })

        except Exception as e:
            self.stats["errors"] += 1
            self.last_error = repr(e)
            self._save_status()
            self._log_event({
                "event": "RECORDER_ERROR",
                "error": repr(e),
                "utc": datetime.now(timezone.utc).isoformat(),
            })

    # ------------------------------------------------------------ status

    def status(self):
        print("=== RF-001 TWO-MARKET OBSERVATION RECORDER STATUS ===")
        print(f"version: {VERSION}")
        print(f"primary: {PRIMARY_SYMBOL} ({PRIMARY_LOGICAL})")
        print(f"confirmation: {CONFIRMATION_SYMBOL} ({CONFIRMATION_LOGICAL})")
        print(f"timeframe: {TIMEFRAME}")
        print(f"raw_archive: {self.raw_archive}")
        for k, v in self.stats.items():
            print(f"stats.{k}: {v}")
        print(f"last_primary_bar: {self.last_primary_bar}")
        print(f"last_confirmation_bar: {self.last_confirmation_bar}")
        print(f"last_error: {self.last_error}")

    # ------------------------------------------------------------ tests

    def smoke_test(self):
        """Structural tests T1-T14. Synthetic feed, isolated temp root only."""
        results = []

        def check(name, cond):
            results.append((name, bool(cond)))
            print(("PASS " if cond else "FAIL ") + name)

        class FakeFeed:
            def __init__(self, bars_map=None, fail=False):
                self._bars_map = bars_map or {}
                self.fail = fail
                self.queries = []

            def latest_completed_bar(self, symbol, timeframe):
                self.queries.append((symbol, timeframe))
                if self.fail:
                    raise RuntimeError("synthetic feed failure")
                bars = self._bars_map.get(symbol, [])
                if not bars:
                    return {"status": "FEED_UNAVAILABLE"}
                return bars.pop(0)

        def sym_bar(symbol, t, o=5000.0, h=5005.0, l=4995.0, c=5002.0):
            return {
                "status": "DATA_FRESH",
                "symbol": symbol,
                "time": t,
                "open": o, "high": h, "low": l, "close": c,
                "volume": 100,
            }

        base_t = int(time.time()) // 60 * 60 - 3600

        import tempfile, hashlib, csv as _csv

        with tempfile.TemporaryDirectory(prefix="rf001_two_mkt_test_") as td:
            # T1: both symbols requested through shared feed
            feed1 = FakeFeed({
                PRIMARY_SYMBOL: [sym_bar(PRIMARY_SYMBOL, base_t)],
                CONFIRMATION_SYMBOL: [sym_bar(CONFIRMATION_SYMBOL, base_t)],
            })
            rec1 = RF001ObservationRecorder(feed=feed1, raw_dir=os.path.join(td, "r1"))
            rec1.on_tick({})
            check(
                "T1 both symbols requested",
                (PRIMARY_SYMBOL, "M1") in feed1.queries
                and (CONFIRMATION_SYMBOL, "M1") in feed1.queries,
            )

            # T2: same timestamps produce MATCHED
            feed2 = FakeFeed({
                PRIMARY_SYMBOL: [sym_bar(PRIMARY_SYMBOL, base_t + 60)],
                CONFIRMATION_SYMBOL: [sym_bar(CONFIRMATION_SYMBOL, base_t + 60)],
            })
            rec2 = RF001ObservationRecorder(feed=feed2, raw_dir=os.path.join(td, "r2"))
            rec2.on_tick({})
            check(
                "T2 MATCHED state",
                rec2.stats["matched_captures"] == 1,
            )

            # T3: USTECm-only produces PRIMARY_ONLY
            feed3 = FakeFeed({
                PRIMARY_SYMBOL: [sym_bar(PRIMARY_SYMBOL, base_t + 120)],
                CONFIRMATION_SYMBOL: [{"status": "FEED_UNAVAILABLE"}],
            })
            rec3 = RF001ObservationRecorder(feed=feed3, raw_dir=os.path.join(td, "r3"))
            rec3.on_tick({})
            check(
                "T3 PRIMARY_ONLY state",
                rec3.stats["primary_only_events"] == 1
                and rec3.stats["matched_captures"] == 0,
            )

            # T4: US500m-only produces CONFIRMATION_ONLY
            feed4 = FakeFeed({
                PRIMARY_SYMBOL: [{"status": "FEED_UNAVAILABLE"}],
                CONFIRMATION_SYMBOL: [sym_bar(CONFIRMATION_SYMBOL, base_t + 180)],
            })
            rec4 = RF001ObservationRecorder(feed=feed4, raw_dir=os.path.join(td, "r4"))
            rec4.on_tick({})
            check(
                "T4 CONFIRMATION_ONLY state",
                rec4.stats["confirmation_only_events"] == 1
                and rec4.stats["matched_captures"] == 0,
            )

            # T5: mismatched timestamps produce MISALIGNED
            feed5 = FakeFeed({
                PRIMARY_SYMBOL: [sym_bar(PRIMARY_SYMBOL, base_t + 240)],
                CONFIRMATION_SYMBOL: [sym_bar(CONFIRMATION_SYMBOL, base_t + 300)],
            })
            rec5 = RF001ObservationRecorder(feed=feed5, raw_dir=os.path.join(td, "r5"))
            rec5.on_tick({})
            check(
                "T5 MISALIGNED state",
                rec5.stats["misaligned_events"] == 1
                and rec5.stats["matched_captures"] == 0,
            )

            # T6: no forward-fill occurs (MISALIGNED does not persist partial data)
            check(
                "T6 no forward-fill",
                rec5.stats["matched_captures"] == 0,
            )

            # T7: missing US500m cannot become confirmation failure
            feed7 = FakeFeed({
                PRIMARY_SYMBOL: [sym_bar(PRIMARY_SYMBOL, base_t + 360)],
                CONFIRMATION_SYMBOL: [{"status": "FEED_UNAVAILABLE"}],
            })
            rec7 = RF001ObservationRecorder(feed=feed7, raw_dir=os.path.join(td, "r7"))
            rec7.on_tick({})
            # Confirm no "confirmation_failure" or similar economic event
            events_path = os.path.join(td, "r7", "recorder_events.jsonl")
            if os.path.exists(events_path):
                with open(events_path) as f:
                    events = [json.loads(line) for line in f if line.strip()]
                has_failure = any("failure" in e.get("event", "").lower() for e in events)
            else:
                has_failure = False
            check(
                "T7 missing US500m not interpreted as confirmation failure",
                not has_failure and rec7.stats["primary_only_events"] == 1,
            )

            # T8: missing USTECm cannot become no primary event
            feed8 = FakeFeed({
                PRIMARY_SYMBOL: [{"status": "FEED_UNAVAILABLE"}],
                CONFIRMATION_SYMBOL: [sym_bar(CONFIRMATION_SYMBOL, base_t + 420)],
            })
            rec8 = RF001ObservationRecorder(feed=feed8, raw_dir=os.path.join(td, "r8"))
            rec8.on_tick({})
            check(
                "T8 missing USTECm not interpreted as no primary event",
                rec8.stats["confirmation_only_events"] == 1,
            )

            # T9: duplicate observations do not produce duplicate rows
            feed9 = FakeFeed({
                PRIMARY_SYMBOL: [sym_bar(PRIMARY_SYMBOL, base_t + 480), sym_bar(PRIMARY_SYMBOL, base_t + 480)],
                CONFIRMATION_SYMBOL: [sym_bar(CONFIRMATION_SYMBOL, base_t + 480), sym_bar(CONFIRMATION_SYMBOL, base_t + 480)],
            })
            rec9 = RF001ObservationRecorder(feed=feed9, raw_dir=os.path.join(td, "r9"))
            rec9.on_tick({})
            rec9.on_tick({})
            check(
                "T9 duplicate observations idempotent",
                rec9.stats["matched_captures"] == 1
                and rec9.stats["primary_exact_duplicates"] == 1
                and rec9.stats["confirmation_exact_duplicates"] == 1,
            )

            # T10: canonical timestamps preserved
            with open(rec9.raw_archive, "r", newline="", encoding="utf-8") as f:
                rows = list(_csv.DictReader(f))
            expected_ts = datetime.utcfromtimestamp(base_t + 480).strftime("%Y-%m-%d %H:%M:%S")
            check(
                "T10 canonical timestamps preserved",
                len(rows) == 1 and rows[0]["timestamp"] == expected_ts,
            )

            # T11-T14: source-text firewall checks using AST (actual imports only)
            import ast as _ast
            tree = _ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
            actual_imports = set()
            for node in _ast.walk(tree):
                if isinstance(node, _ast.Import):
                    for alias in node.names:
                        actual_imports.add(alias.name.lower())
                elif isinstance(node, _ast.ImportFrom):
                    if node.module:
                        actual_imports.add(node.module.lower())

            check(
                "T11 no F-01 import",
                not any("f01" in imp for imp in actual_imports),
            )
            check(
                "T12 no FB-001 import",
                not any("fb001" in imp for imp in actual_imports),
            )
            check(
                "T13 no direct MT5 calls",
                "metatrader5" not in actual_imports,
            )

            # T14: no broker order calls in module source (exclude test method)
            module_src = open(os.path.abspath(__file__), encoding="utf-8").read()
            # Extract only the class definition, not the smoke_test method
            class_start = module_src.find("class RF001ObservationRecorder:")
            test_start = module_src.find("def smoke_test(self):")
            if class_start >= 0 and test_start >= 0:
                module_body = module_src[class_start:test_start]
            else:
                module_body = module_src
            check(
                "T14 no broker order calls",
                "order_send" not in module_body and "place_order" not in module_body,
            )

        print("---")
        failed = [n for n, c in results if not c]
        print(
            "rf001 two-market smoke-test: %d/%d passed"
            % (len(results) - len(failed), len(results))
        )
        return 1 if failed else 0


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(
        description="RF-001 two-market M1 observation recorder (structural only)"
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
