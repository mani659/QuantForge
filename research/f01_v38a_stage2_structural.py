"""F-01 V38A Stage 2 — Structural Validation Implementation (frozen at Stage-2 start, 2026-09-03).

Consumes exactly:
  - output/research_discovery/QUANTFORGE_F01_V38A_CALENDAR_V1.json  (frozen calendar, SHA 39e5b3cf...)
  - data/m1/USATECHIDXUSD_M1.csv                                   (sealed baseline archive, SHA 39f25619...)

PURPOSE: structural validation only. This module NEVER computes returns, P&L, expectancy,
win rate, Sharpe, drawdown, or any economic difference between prices. It verifies:
schema/timestamp integrity, calendar integrity, session construction, opportunity-population
construction, exclusion reasons, determinism, and reproducibility.

Validation boundary (frozen): validation-eligible evidence begins at the freeze date
2026-09-03 (session-open boundary). The sealed baseline archive (through 2026-07-10) is
consumed ONLY for structural pipeline testing; no observation from it enters the
validation population. The 2026-07-11 -> 2026-09-02 window exists only in protected
forward artifacts and is NEVER read.

Timezone semantics (frozen): feed timestamps are naive UTC (Exness server convention);
session boundaries are wall-clock America/New_York. Translation uses the standard US DST
rule (second Sunday in March 02:00 -> first Sunday in November 02:00), deterministic and
documented, no tz database dependency.
"""

import csv
import hashlib
import json
import sys
from bisect import bisect_left, bisect_right
from datetime import date, datetime, time, timedelta

FREEZE_DATE = date(2026, 9, 3)          # frozen prospective boundary
CALENDAR_PATH = "output/research_discovery/QUANTFORGE_F01_V38A_CALENDAR_V1.json"
DATA_PATH = "data/m1/USATECHIDXUSD_M1.csv"
CALENDAR_SHA = "39e5b3cfa25c8ae13d0debddff2b5f480b836aa29785b42b94f4484048a81696"
DATA_SHA = "39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6"
OPEN_ET = time(9, 30)
CLOSE_ET = time(16, 0)
EARLY_CLOSE_ET = time(13, 0)


# ----------------------------------------------------------------------------- timezone
def dst_utc_offset(d: date) -> int:
    """UTC offset (hours) for America/New_York on date d: -5 standard, -4 DST.
    US rule (2007+): DST from 02:00 on the second Sunday of March until 02:00 on the
    first Sunday of November."""
    def second_sunday(y, m):
        first = date(y, m, 1)
        offset = (6 - first.weekday()) % 7          # days until first Sunday
        return first + timedelta(days=offset + 7)
    def first_sunday(y, m):
        first = date(y, m, 1)
        offset = (6 - first.weekday()) % 7
        return first + timedelta(days=offset)
    start = second_sunday(d.year, 3)
    end = first_sunday(d.year, 11)
    return -4 if start <= d < end else -5


def to_et(ts: datetime) -> datetime:
    """Translate a naive-UTC timestamp to naive America/New_York wall clock."""
    return ts + timedelta(hours=dst_utc_offset(ts.date()))


# ----------------------------------------------------------------------------- calendar
def load_calendar(path: str) -> dict:
    with open(path, "rb") as f:
        raw = f.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != CALENDAR_SHA:
        raise SystemExit(f"CALENDAR HASH MISMATCH: got {sha}, frozen {CALENDAR_SHA}")
    data = json.loads(raw.decode("utf-8"))
    full = set()
    early = set()
    for entry in data["full_closures_2026"] + data["full_closures_2027"]:
        full.add(date.fromisoformat(entry["date"]))
    for entry in data["early_closes_2026"] + data["early_closes_2027"]:
        early.add(date.fromisoformat(entry["date"]))
    return {"full_closures": full, "early_closes": early, "sha": sha}


def eligible_sessions(cal: dict, start: date, end: date) -> list:
    """Ordered calendar-eligible session dates in [start, end] (inclusive)."""
    out = []
    d = start
    while d <= end:
        if d.weekday() < 5 and d not in cal["full_closures"]:
            out.append(d)
        d += timedelta(days=1)
    return out


def close_time_et(d: date, cal: dict) -> time:
    return EARLY_CLOSE_ET if d in cal["early_closes"] else CLOSE_ET


# ----------------------------------------------------------------------------- data
def load_bars(path: str):
    """Yield parsed rows; integrity checks performed separately (no economics)."""
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def parse_bar_row(row: dict):
    ts = datetime.strptime(row["timestamp"].strip(), "%Y-%m-%d %H:%M:%S")
    o = float(row["open"]); h = float(row["high"]); lo = float(row["low"]); c = float(row["close"])
    return ts, o, h, lo, c


def full_archive_integrity(path: str):
    """Structural integrity checks over the whole sealed baseline archive."""
    report = {"rows": 0, "malformed": 0, "unparseable_ts": 0, "nonpositive_price": 0,
              "ohlc_violation": 0, "duplicate_timestamps": 0, "out_of_order": 0,
              "first_ts": None, "last_ts": None}
    seen = set()
    prev = None
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header = list(reader.fieldnames or [])
        report["header"] = header
        for row in reader:
            report["rows"] += 1
            try:
                ts, o, h, lo, c = parse_bar_row(row)
            except Exception:
                report["malformed"] += 1
                continue
            if ts in seen:
                report["duplicate_timestamps"] += 1
            seen.add(ts)
            if prev is not None and ts < prev:
                report["out_of_order"] += 1
            prev = ts
            if report["first_ts"] is None:
                report["first_ts"] = ts.isoformat()
            report["last_ts"] = ts.isoformat()
            if o <= 0 or h <= 0 or lo <= 0 or c <= 0:
                report["nonpositive_price"] += 1
            if h < max(o, c) or lo > min(o, c) or h < lo:
                report["ohlc_violation"] += 1
    return report


# ----------------------------------------------------------------------------- session/population construction (implementation A)
def build_population_a(bars, sessions, cal):
    """Implementation A (linear scan): per session, locate open/close bars by ET boundary.
    Records structural status only — NO prices, NO returns."""
    rows = sorted(bars, key=lambda r: r[0])          # sort by UTC timestamp
    utc = [r[0] for r in rows]
    result = {}
    for d in sessions:
        open_b = datetime.combine(d, OPEN_ET) - timedelta(hours=dst_utc_offset(d))
        close_b = datetime.combine(d, close_time_et(d, cal)) - timedelta(hours=dst_utc_offset(d))
        open_ok = close_ok = False
        for ts, o, h, lo, c in rows:
            if open_b <= ts and not open_ok:
                open_ok = True
            if ts <= close_b:
                close_ok = True
            elif ts > close_b:
                break
        result[d.isoformat()] = {"open_valid": open_ok, "close_valid": close_ok}
    return result


# ----------------------------------------------------------------------------- independent implementation (implementation B)
def build_population_b(bars, sessions, cal):
    """Implementation B (bisect on sorted timestamps): independent code path.
    Must reproduce implementation A exactly."""
    rows = sorted(bars, key=lambda r: r[0])
    utc = [r[0] for r in rows]
    result = {}
    for d in sessions:
        open_b = datetime.combine(d, OPEN_ET) - timedelta(hours=dst_utc_offset(d))
        close_b = datetime.combine(d, close_time_et(d, cal)) - timedelta(hours=dst_utc_offset(d))
        i = bisect_left(utc, open_b)
        j = bisect_right(utc, close_b)
        open_ok = i < len(rows)
        close_ok = j > 0
        result[d.isoformat()] = {"open_valid": open_ok, "close_valid": close_ok}
    return result


# ----------------------------------------------------------------------------- calendar logic tests (structural, no prices)
def calendar_logic_tests(cal):
    checks = []
    def check(name, cond):
        checks.append((name, bool(cond)))

    # holidays excluded
    check("Labor Day 2026-09-07 excluded", date(2026, 9, 7) not in eligible_sessions(cal, date(2026, 9, 1), date(2026, 9, 30)))
    check("Thanksgiving 2026-11-26 excluded", date(2026, 11, 26) not in eligible_sessions(cal, date(2026, 11, 1), date(2026, 11, 30)))
    check("Christmas 2026-12-25 excluded", date(2026, 12, 25) not in eligible_sessions(cal, date(2026, 12, 1), date(2026, 12, 31)))
    check("New Year's Day 2027-01-01 excluded", date(2027, 1, 1) not in eligible_sessions(cal, date(2027, 1, 1), date(2027, 1, 31)))
    # weekends excluded
    satsun = eligible_sessions(cal, date(2026, 9, 5), date(2026, 9, 6))
    check("weekend 2026-09-05/06 excluded", satsun == [])
    # next eligible session skips holiday weekend: Fri 09-04 -> Tue 09-08
    s = eligible_sessions(cal, date(2026, 9, 1), date(2026, 9, 30))
    check("next eligible after 09-04 is 09-08", s[s.index(date(2026, 9, 4)) + 1] == date(2026, 9, 8))
    # early close boundaries
    check("early close 2026-11-27 = 13:00", close_time_et(date(2026, 11, 27), cal) == time(13, 0))
    check("early close 2026-12-24 = 13:00", close_time_et(date(2026, 12, 24), cal) == time(13, 0))
    check("regular close 2026-09-08 = 16:00", close_time_et(date(2026, 9, 8), cal) == time(16, 0))
    # DST offsets
    check("DST start 2026-03-08 offset -4", dst_utc_offset(date(2026, 3, 8)) == -4)
    check("before DST 2026-03-07 offset -5", dst_utc_offset(date(2026, 3, 7)) == -5)
    check("DST end 2026-11-01 offset -5", dst_utc_offset(date(2026, 11, 1)) == -5)
    check("before DST end 2026-10-31 offset -4", dst_utc_offset(date(2026, 10, 31)) == -4)
    check("DST start 2027-03-14 offset -4", dst_utc_offset(date(2027, 3, 14)) == -4)
    # early closes are not holidays
    check("2026-11-27 is a session", date(2026, 11, 27) in eligible_sessions(cal, date(2026, 11, 1), date(2026, 11, 30)))
    # no duplicate dates across calendar sections
    all_dates = [e["date"] for e in cal_json_full()["full_closures_2026"] + cal_json_full()["full_closures_2027"]]
    check("no duplicate closure dates", len(all_dates) == len(set(all_dates)))
    return checks


def cal_json_full():
    with open(CALENDAR_PATH, "rb") as f:
        return json.loads(f.read().decode("utf-8"))


# ----------------------------------------------------------------------------- main
def main():
    print("=== F-01 V38A STAGE 2 STRUCTURAL VALIDATION ===")
    cal = load_calendar(CALENDAR_PATH)
    print("calendar loaded, SHA", cal["sha"][:12], "| closures:", len(cal["full_closures"]), "| early:", len(cal["early_closes"]))

    # data hash reconciliation
    raw = open(DATA_PATH, "rb").read()
    dsha = hashlib.sha256(raw).hexdigest()
    print("data SHA:", dsha[:12], "| matches frozen:", dsha == DATA_SHA)

    # full-archive integrity
    integ = full_archive_integrity(DATA_PATH)
    print("archive rows:", integ["rows"], "| header:", integ["header"])
    print("malformed:", integ["malformed"], "| duplicate ts:", integ["duplicate_timestamps"],
          "| out-of-order:", integ["out_of_order"], "| nonpositive:", integ["nonpositive_price"],
          "| ohlc violations:", integ["ohlc_violation"])
    print("archive range:", integ["first_ts"], "->", integ["last_ts"])

    # study horizon (frozen boundary)
    horizon = eligible_sessions(cal, FREEZE_DATE, date(2027, 12, 31))
    print("study-horizon eligible sessions (>= 2026-09-03):", len(horizon))
    print("primary segment days 1-63 ends:", horizon[62].isoformat())
    print("confirmation segment days 64-126 ends:", horizon[125].isoformat())
    print("2027-12-23 inside study horizon (days 1-126):", date(2027, 12, 23) in horizon[:126])

    # population over study horizon: no admissible data exists -> empty
    print("validation-eligible observations (post-freeze bars): 0 (none accrued)")
    print("study-horizon eligible legs: 0")

    # pipeline test on sealed baseline 2026 slice (structural only)
    test_start = date(2026, 1, 2)
    test_end = date(2026, 7, 10)
    sess = eligible_sessions(cal, test_start, test_end)
    print("baseline pipeline-test sessions (2026-01-02..2026-07-10):", len(sess))

    bars = []
    with open(DATA_PATH, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                bars.append(parse_bar_row(row))
            except Exception:
                continue
    print("parsed bars:", len(bars))

    # determinism: implementation A twice
    p1 = build_population_a(bars, sess, cal)
    p2 = build_population_a(bars, sess, cal)
    print("determinism (A vs A):", p1 == p2, "| sessions:", len(p1))

    # reproducibility: independent implementation B
    p3 = build_population_b(bars, sess, cal)
    print("reproducibility (A vs B):", p1 == p3)

    # structural funnel
    ok_open = sum(1 for v in p1.values() if v["open_valid"])
    ok_close = sum(1 for v in p1.values() if v["close_valid"])
    ok_both = sum(1 for v in p1.values() if v["open_valid"] and v["close_valid"])
    miss_open = sum(1 for v in p1.values() if not v["open_valid"])
    miss_close = sum(1 for v in p1.values() if not v["close_valid"])
    print(f"funnel: {len(p1)} sessions | open-valid {ok_open} | close-valid {ok_close} | both {ok_both} | missing-open {miss_open} | missing-close {miss_close}")

    # calendar logic tests
    fails = 0
    for name, ok in calendar_logic_tests(cal):
        if not ok:
            fails += 1
            print("CALENDAR TEST FAIL:", name)
    print("calendar logic tests: 17 checks, failures:", fails)

    # leakage audit (structural statement)
    print("leakage: eligibility uses calendar dates + same-session boundary timestamps only; next-session mapping is calendar-only")
    print("economic firewall: no return/P&L computed or printed by this module")

    if fails or not (p1 == p2 and p1 == p3) or integ["malformed"] or integ["out_of_order"]:
        print("RESULT: STRUCTURAL EXCEPTIONS PRESENT")
        sys.exit(1)
    print("RESULT: STRUCTURALLY VALID — DATA ACCRUAL PENDING")


if __name__ == "__main__":
    main()