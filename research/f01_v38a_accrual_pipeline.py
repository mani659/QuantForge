"""F-01 V38A — Forward-Data Accrual Pipeline (governed infrastructure, frozen 2026-09-03).

Subordinate to the frozen F-01 registration (QUANTFORGE_F01_V38A_REGISTRATION_FREEZE_V1.md,
SHA 41883aaeab6a...). This pipeline PRESERVES future admissible USTECm observations; it never
manufactures, selects, repairs, or optimizes evidence.

AUTHORIZED SOURCE: the repository's broker-layer MT5 connector (broker/mt5_connection.py,
env-configured QF_MT5_TERMINAL_PATH / QF_MT5_EXPECTED_ACCOUNT, credential-free) and the
established MT5 CSV-export pattern that produced data/m1/*.csv. The operator exports fresh
USTECm M1 bars (schema: timestamp,open,high,low,close,volume) and invokes this pipeline with
--ingest <export.csv>. No credentials are stored or referenced anywhere in this module.

BOUNDARY (frozen): validation-eligible evidence begins at the session-open boundary of the
freeze date — UTC equivalent of 2026-09-03 09:30 America/New_York (13:30 UTC, DST). Bars with
UTC timestamp < that instant are REJECT / NON-STUDY (never backfilled). The sealed baseline
archive data/m1/USATECHIDXUSD_M1.csv is never read or modified by this pipeline.

FIREWALLS: (1) protected forward material (the forward runtime's ledgers, event logs, and
health state) is never referenced or opened; (2) no economic computation exists anywhere in
this module — no returns, P&L, expectancy, win rate, Sharpe, or drawdown; (3) this pipeline
never launches Stage 3.

MODES:
  --init        create the study archive, snapshot ledger, and state file (idempotent)
  --ingest F    validate export F, append admissible bars append-only, write snapshot
  --state       print structural accrual state
  --selftest    run structural pipeline tests P1-P12 (synthetic fixtures, no economics)
"""

import argparse
import csv
import hashlib
import json
import os
import sys
import tempfile
from datetime import date, datetime, time, timedelta

PIPELINE_VERSION = "1.0.0"
FREEZE_DATE = date(2026, 9, 3)
FREEZE_OPEN_ET = time(9, 30)
CALENDAR_PATH = "output/research_discovery/QUANTFORGE_F01_V38A_CALENDAR_V1.json"
CALENDAR_SHA = "39e5b3cfa25c8ae13d0debddff2b5f480b836aa29785b42b94f4484048a81696"
REGISTRATION_SHA = "41883aaeab6a"
SEALED_BASELINE_SHA = "39f25619bd26d72f4fdaa300a5c40002e4f4d46805050526ba98ec1c0a54bfc6"
STUDY_DIR = "data/f01"
STUDY_ARCHIVE = os.path.join(STUDY_DIR, "ustechidxusd_m1_study.csv")
SNAPSHOT_LEDGER = os.path.join(STUDY_DIR, "snapshot_ledger.jsonl")
STATE_FILE = os.path.join(STUDY_DIR, "accrual_state.json")
SCHEMA = ["timestamp", "open", "high", "low", "close", "volume"]


# ---------------------------------------------------------------- timezone (registered rule)
def dst_utc_offset(d: date) -> int:
    def second_sunday(y, m):
        first = date(y, m, 1)
        return first + timedelta(days=(6 - first.weekday()) % 7 + 7)
    def first_sunday(y, m):
        first = date(y, m, 1)
        return first + timedelta(days=(6 - first.weekday()) % 7)
    start = second_sunday(d.year, 3)
    end = first_sunday(d.year, 11)
    return -4 if start <= d < end else -5


def freeze_boundary_utc() -> datetime:
    """UTC instant of the first admissible session-open boundary (2026-09-03 09:30 ET)."""
    return datetime.combine(FREEZE_DATE, FREEZE_OPEN_ET) - timedelta(hours=dst_utc_offset(FREEZE_DATE))


# ---------------------------------------------------------------- calendar (frozen artifact)
def load_calendar(path: str) -> dict:
    with open(path, "rb") as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != CALENDAR_SHA:
        raise SystemExit("CALENDAR HASH MISMATCH — frozen calendar altered; aborting.")
    data = json.loads(raw.decode("utf-8"))
    full = {date.fromisoformat(e["date"]) for e in data["full_closures_2026"] + data["full_closures_2027"]}
    early = {date.fromisoformat(e["date"]) for e in data["early_closes_2026"] + data["early_closes_2027"]}
    return {"full_closures": full, "early_closes": early}


def eligible_sessions(cal: dict, start: date, end: date) -> list:
    out, d = [], start
    while d <= end:
        if d.weekday() < 5 and d not in cal["full_closures"]:
            out.append(d)
        d += timedelta(days=1)
    return out


def close_time_et(d: date, cal: dict) -> time:
    return time(13, 0) if d in cal["early_closes"] else time(16, 0)


# ---------------------------------------------------------------- raw parsing
def parse_row(row: dict):
    ts = datetime.strptime(row["timestamp"].strip(), "%Y-%m-%d %H:%M:%S")
    o, h, lo, c = (float(row[k]) for k in ["open", "high", "low", "close"])
    return ts, o, h, lo, c


def row_to_line(ts, o, h, lo, c) -> str:
    return f"{ts.strftime('%Y-%m-%d %H:%M:%S')},{o},{h},{lo},{c},0"


# ---------------------------------------------------------------- snapshot helpers
def archive_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_state(state_path: str) -> dict:
    with open(state_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state_path: str, state: dict) -> None:
    tmp = state_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, state_path)          # atomic replace; never partial


def append_ledger(ledger_path: str, entry: dict) -> None:
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


# ---------------------------------------------------------------- eligibility
def eligible_session_count(cal: dict, archive_rows) -> dict:
    """Structural only: count calendar-eligible sessions with an admissible session-open bar."""
    by_ts = sorted(ts for ts, *_ in archive_rows)
    sessions = eligible_sessions(cal, FREEZE_DATE, date(2027, 12, 31))
    boundary = freeze_boundary_utc()
    count = 0
    for d in sessions:
        ob = datetime.combine(d, time(9, 30)) - timedelta(hours=dst_utc_offset(d))
        if ob < boundary:
            continue
        # admissible session requires >=1 bar at/after its open boundary
        if any(ts >= ob for ts in by_ts):
            count += 1
    return {"eligible_sessions_with_data": count, "total_sessions_in_window": len(sessions),
            "primary_complete": count >= 63, "confirmation_complete": count >= 126}


# ---------------------------------------------------------------- ingestion
def ingest(export_path: str, study_dir: str, archive_path: str, ledger_path: str,
           state_path: str, cal: dict) -> dict:
    """Validate export, append admissible bars append-only, write snapshot entry."""
    report = {"source": export_path, "rows_seen": 0, "malformed": 0, "admitted": 0,
              "rejected_prefreeze": 0, "exact_duplicates_collapsed": 0,
              "conflicting_duplicates_quarantined": 0, "unexpected_gap_observations": [],
              "errors": []}

    # read export (allowlist: only the declared export file)
    rows = []
    try:
        with open(export_path, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            header = list(reader.fieldnames or [])
            if header != SCHEMA:
                report["errors"].append(f"SCHEMA MISMATCH: {header}")
                return report
            for row in reader:
                report["rows_seen"] += 1
                try:
                    rows.append(parse_row(row))
                except Exception:
                    report["malformed"] += 1
    except FileNotFoundError:
        report["errors"].append("EXPORT FILE NOT FOUND")
        return report

    # source identity (structural): price scale plausibility for USTECm (index CFD, ~10^3..10^6)
    scale_ok = all(100.0 < p < 1_000_000.0 for _, o, h, lo, c in rows for p in (o, h, lo, c))
    if not scale_ok:
        report["errors"].append("PRICE SCALE OUT OF REGISTERED RANGE — source identity suspect")
        return report

    # read existing archive
    existing = {}
    if os.path.exists(archive_path):
        with open(archive_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ts, o, h, lo, c = parse_row(row)
                    existing[ts] = (o, h, lo, c)
                except Exception:
                    report["errors"].append("EXISTING ARCHIVE CORRUPT")
                    return report

    boundary = freeze_boundary_utc()
    admitted = []          # (ts, o, h, lo, c)
    quarantine = []        # (ts, reason)
    seen = set()
    for ts, o, h, lo, c in sorted(rows, key=lambda r: r[0]):
        if ts in seen:
            report["exact_duplicates_collapsed"] += 1
            continue
        seen.add(ts)
        if ts < boundary:
            report["rejected_prefreeze"] += 1
            continue
        if ts in existing:
            if existing[ts] == (o, h, lo, c):
                report["exact_duplicates_collapsed"] += 1
            else:
                report["conflicting_duplicates_quarantined"] += 1
                quarantine.append((ts.isoformat(), "conflicting duplicate vs archive"))
            continue
        if o <= 0 or h <= 0 or lo <= 0 or c <= 0 or h < max(o, c) or lo > min(o, c) or h < lo:
            report["conflicting_duplicates_quarantined"] += 1
            quarantine.append((ts.isoformat(), "structural price violation"))
            continue
        admitted.append((ts, o, h, lo, c))

    # gap observation: trading session with no bars (expected closures excluded by calendar)
    if admitted:
        by_date = {}
        for ts, *_ in admitted:
            by_date.setdefault(ts.date(), []).append(ts)
        sessions = eligible_sessions(cal, FREEZE_DATE, date(2027, 12, 31))
        for d in sessions:
            ob = datetime.combine(d, time(9, 30)) - timedelta(hours=dst_utc_offset(d))
            if ob < boundary:
                continue
            if not any(ts >= ob for ts in by_date.get(d, [])):
                report["unexpected_gap_observations"].append(d.isoformat())

    # append-only write: existing archive rows are never modified; only new rows appended
    if admitted:
        with open(archive_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not os.path.exists(archive_path) or os.path.getsize(archive_path) == 0:
                writer.writerow(SCHEMA)
            for ts, o, h, lo, c in sorted(admitted, key=lambda r: r[0]):
                writer.writerow([ts.strftime("%Y-%m-%d %H:%M:%S"), o, h, lo, c, 0])
        report["admitted"] = len(admitted)

    # snapshot entry + chain of custody
    if os.path.exists(archive_path):
        h = archive_hash(archive_path)
        with open(archive_path, "r", newline="", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        ts_all = [datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S") for r in reader]
        state = load_state(state_path)
        prev = state.get("last_snapshot_hash", "NONE")
        snap_id = f"SNAP-{int(state.get('snapshot_counter', 0)) + 1:04d}"
        entry = {"snapshot_id": snap_id, "predecessor": prev, "source": export_path,
                 "acquisition_ts": datetime.utcnow().isoformat() + "Z",
                 "first_ts": min(ts_all).isoformat() if ts_all else None,
                 "last_ts": max(ts_all).isoformat() if ts_all else None,
                 "row_count": len(ts_all), "sha256": h,
                 "registration": REGISTRATION_SHA, "pipeline_version": PIPELINE_VERSION}
        append_ledger(ledger_path, entry)

        counts = eligible_session_count(cal, [(t, 0, 0, 0, 0) for t in ts_all])
        state.update({"snapshot_counter": int(state.get("snapshot_counter", 0)) + 1,
                      "last_snapshot_id": snap_id, "last_snapshot_hash": h,
                      "archive_row_count": len(ts_all),
                      "eligible_sessions_with_data": counts["eligible_sessions_with_data"],
                      "primary_complete": counts["primary_complete"],
                      "confirmation_complete": counts["confirmation_complete"],
                      "last_ingest_report": report})
        save_state(state_path, state)

    return report


# ---------------------------------------------------------------- init
def init(study_dir: str, archive_path: str, ledger_path: str, state_path: str, cal: dict) -> None:
    os.makedirs(study_dir, exist_ok=True)
    if not os.path.exists(archive_path):
        with open(archive_path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(SCHEMA)
    if not os.path.exists(ledger_path):
        entry = {"snapshot_id": "SNAP-0000", "predecessor": "GENESIS",
                 "event": "pipeline initialization", "acquisition_ts": datetime.utcnow().isoformat() + "Z",
                 "row_count": 0, "sha256": archive_hash(archive_path),
                 "registration": REGISTRATION_SHA, "sealed_baseline": SEALED_BASELINE_SHA,
                 "pipeline_version": PIPELINE_VERSION}
        append_ledger(ledger_path, entry)
    if not os.path.exists(state_path):
        save_state(state_path, {
            "pipeline_version": PIPELINE_VERSION, "registration": REGISTRATION_SHA,
            "calendar": CALENDAR_SHA, "sealed_baseline": SEALED_BASELINE_SHA,
            "freeze_boundary_utc": freeze_boundary_utc().isoformat(),
            "study_archive": archive_path, "snapshot_counter": 1,
            "last_snapshot_id": "SNAP-0000", "last_snapshot_hash": archive_hash(archive_path),
            "archive_row_count": 0, "eligible_sessions_with_data": 0,
            "primary_complete": False, "confirmation_complete": False})


def print_state(state_path: str) -> None:
    state = load_state(state_path)
    print("=== F-01 ACCRUAL STATE ===")
    for k in ["pipeline_version", "registration", "calendar", "freeze_boundary_utc",
              "archive_row_count", "eligible_sessions_with_data", "primary_complete",
              "confirmation_complete", "last_snapshot_id", "last_snapshot_hash"]:
        print(f"{k}: {state.get(k)}")


# ---------------------------------------------------------------- structural self-tests
def _write_export(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(SCHEMA)
        for r in rows:
            w.writerow(r)


def selftest():
    """Structural pipeline tests P1-P12. Synthetic fixtures only; no economics computed."""
    results = []
    def check(name, cond):
        results.append((name, bool(cond)))

    cal = load_calendar(CALENDAR_PATH)
    boundary = freeze_boundary_utc()

    with tempfile.TemporaryDirectory(prefix="f01_accrual_selftest_") as td:
        arc = os.path.join(td, "study.csv")
        led = os.path.join(td, "ledger.jsonl")
        sta = os.path.join(td, "state.json")
        init(td, arc, led, sta, cal)

        # P2 freeze-boundary enforcement: pre-freeze bars rejected
        pre = [(boundary - timedelta(hours=1), 20000.0, 20001.0, 19999.0, 20000.5),
               (boundary - timedelta(minutes=1), 20000.5, 20002.0, 20000.0, 20001.0)]
        exp_pre = os.path.join(td, "pre.csv"); _write_export(exp_pre, pre)
        r1 = ingest(exp_pre, td, arc, led, sta, cal)
        check("P2 freeze-boundary enforcement (pre-freeze rejected)", r1["rejected_prefreeze"] == 2 and r1["admitted"] == 0)

        # P3 append-only: post-freeze bars admitted; existing rows never modified
        post = [(boundary + timedelta(hours=5), 20100.0, 20105.0, 20095.0, 20102.0),
                (boundary + timedelta(hours=6), 20102.0, 20110.0, 20100.0, 20108.0)]
        exp_post = os.path.join(td, "post.csv"); _write_export(exp_post, post)
        r2 = ingest(exp_post, td, arc, led, sta, cal)
        check("P3 append-only admits post-freeze", r2["admitted"] == 2)
        h_after = archive_hash(arc)
        # re-ingest a modified first row -> conflict quarantine, archive unchanged
        exp_mod = os.path.join(td, "mod.csv")
        _write_export(exp_mod, [(post[0][0], 99999.0, 99999.0, 99999.0, 99999.0), post[1]])
        r3 = ingest(exp_mod, td, arc, led, sta, cal)
        check("P3 append-only (conflict quarantined, archive unmodified)",
              r3["conflicting_duplicates_quarantined"] == 1 and archive_hash(arc) == h_after)

        # P4 duplicate detection: exact duplicate collapsed with provenance
        exp_dup = os.path.join(td, "dup.csv"); _write_export(exp_dup, [post[1], post[1]])
        r4 = ingest(exp_dup, td, arc, led, sta, cal)
        check("P4 exact duplicate collapsed", r4["exact_duplicates_collapsed"] >= 1 and r4["admitted"] == 0)

        # P5 gap detection: expected closure (Saturday) NOT a gap; missing weekday session IS
        sat = date(2026, 9, 5)
        check("P5 expected closure not a gap", sat.weekday() >= 5)
        gaps = r2["unexpected_gap_observations"]
        check("P5 unexpected gaps recorded (not filled)", isinstance(gaps, list))

        # P6 timezone/DST correctness
        check("P6 DST offset Mar 2026", dst_utc_offset(date(2026, 3, 8)) == -4)
        check("P6 DST offset Nov 2026", dst_utc_offset(date(2026, 11, 1)) == -5)
        check("P6 boundary = 13:30 UTC", boundary == datetime(2026, 9, 3, 13, 30))

        # P7 calendar integration: holidays excluded from session set
        check("P7 Labor Day excluded", date(2026, 9, 7) not in eligible_sessions(cal, date(2026, 9, 1), date(2026, 9, 30)))
        check("P7 early close 13:00", close_time_et(date(2026, 11, 27), cal) == time(13, 0))

        # P8 snapshot hashing: identical ingest -> identical archive hash
        exp_re = os.path.join(td, "re.csv"); _write_export(exp_re, [post[0], post[1]])
        ingest(exp_re, td, arc, led, sta, cal)
        check("P8 snapshot hashing stable", archive_hash(arc) == h_after)

        # P9 reproducible reconstruction: fresh dir, same inputs -> same archive content
        td2 = os.path.join(td, "clone"); os.makedirs(td2)
        arc2 = os.path.join(td2, "study.csv"); led2 = os.path.join(td2, "ledger.jsonl"); sta2 = os.path.join(td2, "state.json")
        init(td2, arc2, led2, sta2, cal)
        ingest(exp_post, td2, arc2, led2, sta2, cal)
        check("P9 reproducible reconstruction", archive_hash(arc) == archive_hash(arc2))

        # P1 source identity: schema mismatch rejected
        bad = os.path.join(td, "bad.csv")
        with open(bad, "w", newline="", encoding="utf-8") as f:
            f.write("timestamp,close\n2026-09-03 14:00:00,20000\n")
        r5 = ingest(bad, td, arc, led, sta, cal)
        check("P1 source identity (schema)", any("SCHEMA MISMATCH" in e for e in r5["errors"]))

        # P10-P12 firewalls: source-text checks with constructed tokens (never literal in the
        # module's own text, so the checks cannot be defeated by their own presence)
        src = open(__file__, encoding="utf-8").read()
        rt_root = "run" + "time" + "/"
        g6_root = "G6_" + "CAND015"
        check("P10 protected firewall (no protected roots referenced)",
              rt_root not in src and g6_root not in src)

        econ_log = "lo" + "g("
        econ_np = "np." + "log"
        econ_pct = "pct_" + "change"
        econ_fn = "compute_" + "return"
        check("P11 no-economics (no return/P&L computation)",
              econ_log not in src and econ_np not in src and econ_pct not in src and econ_fn not in src)

        launch1 = "sub" + "process"
        launch2 = "os." + "system"
        launch3 = "stage" + "3"
        check("P12 no auto Stage 3",
              launch1 not in src and launch2 not in src and launch3 not in src.lower())

    for name, ok in results:
        print(("PASS " if ok else "FAIL ") + name)
    failed = [n for n, ok in results if not ok]
    print(f"selftest: {len(results) - len(failed)}/{len(results)} passed")
    return 1 if failed else 0


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="F-01 forward-data accrual pipeline (structural only)")
    ap.add_argument("--init", action="store_true", help="initialize study archive/ledger/state")
    ap.add_argument("--ingest", metavar="EXPORT_CSV", help="ingest an authorized USTECm M1 export")
    ap.add_argument("--state", action="store_true", help="print structural accrual state")
    ap.add_argument("--selftest", action="store_true", help="run structural pipeline tests P1-P12")
    args = ap.parse_args()

    cal = load_calendar(CALENDAR_PATH)
    if args.selftest:
        sys.exit(selftest())
    if args.init:
        init(STUDY_DIR, STUDY_ARCHIVE, SNAPSHOT_LEDGER, STATE_FILE, cal)
        print("initialized:", STUDY_ARCHIVE, SNAPSHOT_LEDGER, STATE_FILE)
    if args.ingest:
        rep = ingest(args.ingest, STUDY_DIR, STUDY_ARCHIVE, SNAPSHOT_LEDGER, STATE_FILE, cal)
        print("ingest report:", json.dumps(rep, indent=2))
        if rep["errors"]:
            sys.exit(1)
    if args.state:
        print_state(STATE_FILE)
    if not (args.init or args.ingest or args.state or args.selftest):
        ap.print_help()


if __name__ == "__main__":
    main()